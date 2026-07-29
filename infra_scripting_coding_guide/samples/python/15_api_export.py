#!/usr/bin/env python3
"""opsctl api-export: ページネーション付きAPIから情報を取得しCSVへ出力する。

第11章のAPI呼び出しパターン（タイムアウト、リトライ、指数バックオフ、
429/5xxでのRetry-After尊重）を、opsctlの設定ファイルとdry-run規約に
統合したサブコマンド実装である。

DEFAULT_BASE_URL は example.invalid（実在しないドメイン）である。
このスクリプトをそのまま実行すると名前解決に失敗するので、--dry-run
で組み立てとロジックだけを確認するか、--base-url で到達可能な
テスト用APIに向けること。実際のAPIへ接続する場合は、対象APIの
利用規約とレート制限を事前に確認すること。
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Iterator

import requests

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_TIMEOUT = 4

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_BASE_URL = "https://api.example.invalid"
TOKEN_ENV_VAR = "OPSCTL_API_TOKEN"

logger = logging.getLogger("opsctl.api_export")


class ApiError(RuntimeError):
    pass


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def build_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
    return session


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None,
    timeout: float,
    max_retries: int,
) -> requests.Response:
    """GETを有限回リトライする。接続エラー・タイムアウト・429・5xxが対象。"""
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise ApiError(f"request failed after {attempt} attempts: {exc}") from exc
            backoff = min(2**attempt, 30)
            logger.warning(
                "request error (attempt %s/%s): %s; retrying in %ss", attempt, max_retries, exc, backoff
            )
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                raise ApiError(
                    f"request failed with status {response.status_code} after {attempt} attempts"
                )
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2**attempt, 30)
            logger.warning(
                "status=%s (attempt %s/%s); retrying in %ss", response.status_code, attempt, max_retries, backoff
            )
            time.sleep(backoff)
            continue

        return response


def iter_records(
    session: requests.Session,
    base_url: str,
    endpoint: str,
    *,
    timeout: float,
    max_retries: int,
    page_size: int,
) -> Iterator[dict[str, Any]]:
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session, f"{base_url}{endpoint}", params=params, timeout=timeout, max_retries=max_retries
        )
        if response.status_code != 200:
            raise ApiError(f"unexpected status {response.status_code}: {response.text[:200]}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise ApiError(f"response was not valid JSON: {exc}") from exc
        items = payload.get("items", [])
        if not isinstance(items, list):
            raise ApiError("response 'items' field must be a list")
        yield from items
        cursor = payload.get("next_cursor")
        if not cursor:
            return


def write_csv(path: Path, records: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in fields})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl api-export: export API records to CSV")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--endpoint", default="/v1/hosts")
    parser.add_argument("--fields", default="host,status,last_seen", help="comma separated CSV columns")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    run_id = str(uuid.uuid4())
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format=f"%(asctime)s %(levelname)s run_id={run_id} %(message)s",
        stream=sys.stderr,
        force=True,
    )

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    api_config = config.get("api", {})
    base_url = args.base_url or api_config.get("base_url", DEFAULT_BASE_URL)
    timeout = args.timeout or float(config.get("defaults", {}).get("timeout_seconds", 10))
    fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    if not fields:
        logger.error("--fields must include at least one column name")
        return EXIT_USAGE

    token = os.environ.get(TOKEN_ENV_VAR)

    if args.dry_run:
        logger.info(
            "dry-run: would GET %s%s (fields=%s) and write to %s (token_env=%s)",
            base_url,
            args.endpoint,
            fields,
            args.output,
            TOKEN_ENV_VAR,
        )
        print(json.dumps({"run_id": run_id, "subcommand": "api-export", "dry_run": True}))
        return EXIT_OK

    if not token:
        logger.error("%s environment variable is required", TOKEN_ENV_VAR)
        return EXIT_USAGE

    session = build_session(token)
    try:
        records = list(
            iter_records(
                session,
                base_url,
                args.endpoint,
                timeout=timeout,
                max_retries=args.max_retries,
                page_size=args.page_size,
            )
        )
    except ApiError as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME
    except requests.Timeout:
        logger.error("request timed out")
        return EXIT_TIMEOUT

    write_csv(args.output, records, fields)
    logger.info("wrote %s record(s) to %s", len(records), args.output)
    print(
        json.dumps(
            {"run_id": run_id, "subcommand": "api-export", "records": len(records), "output": str(args.output)}
        )
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
