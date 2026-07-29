#!/usr/bin/env python3
"""ページ分割APIからホスト情報を取得し、CSVへ書き出す。

APIホストは example.invalid（実在しないドメイン）を既定にしている。
このスクリプトをそのまま実行すると名前解決に失敗するので、--dry-run で
組み立てとロジックだけを確認するか、--base-url で到達可能なテスト用API
に向けること。実際のAPIへ接続する場合は、対象APIの利用規約と
レート制限を事前に確認すること。
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterator

import requests

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_TIMEOUT = 4

logger = logging.getLogger("api_export")

DEFAULT_BASE_URL = "https://api.example.invalid"
TOKEN_ENV_VAR = "OPSCTL_API_TOKEN"


class ApiError(RuntimeError):
    pass


def build_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    return session


def get_with_retry(
    session: Any,
    url: str,
    *,
    params: dict[str, Any] | None,
    timeout: float,
    max_retries: int,
) -> Any:
    """GET を有限回リトライする。接続エラー・タイムアウト・429・5xxが対象。"""
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise ApiError(f"request failed after {attempt} attempts: {exc}") from exc
            backoff = min(2 ** attempt, 30)
            logger.warning(
                "request error (attempt %s/%s): %s; retrying in %ss",
                attempt, max_retries, exc, backoff,
            )
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                raise ApiError(
                    f"request failed with status {response.status_code} after {attempt} attempts"
                )
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2 ** attempt, 30)
            logger.warning(
                "status=%s (attempt %s/%s); retrying in %ss",
                response.status_code, attempt, max_retries, backoff,
            )
            time.sleep(backoff)
            continue

        return response


def iter_records(
    session: Any,
    base_url: str,
    *,
    timeout: float,
    max_retries: int,
    page_size: int = 100,
) -> Iterator[dict[str, Any]]:
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session,
            f"{base_url}/v1/hosts",
            params=params,
            timeout=timeout,
            max_retries=max_retries,
        )
        if response.status_code != 200:
            raise ApiError(f"unexpected status {response.status_code}: {response.text[:200]}")
        payload = response.json()
        for record in payload.get("items", []):
            yield record
        cursor = payload.get("next_cursor")
        if not cursor:
            return


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["host", "status", "last_seen"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in fieldnames})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export host records from an API to CSV")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        logger.error("%s is required", TOKEN_ENV_VAR)
        return EXIT_USAGE

    if args.dry_run:
        logger.info("dry-run: would GET %s/v1/hosts and write %s", args.base_url, args.output)
        return EXIT_OK

    session = build_session(token)
    try:
        records = list(
            iter_records(
                session, args.base_url, timeout=args.timeout, max_retries=args.max_retries
            )
        )
    except ApiError as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME
    except requests.Timeout:
        logger.error("request timed out")
        return EXIT_TIMEOUT

    write_csv(args.output, records)
    logger.info("wrote %s records to %s", len(records), args.output)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
