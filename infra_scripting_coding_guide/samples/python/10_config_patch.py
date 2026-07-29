#!/usr/bin/env python3
"""設定ファイルをリモートホストへ配布するサブコマンドの安全な実装例。

パス検証、ホスト名検証、shell=True の排除、戻り値確認、dry-run、
監査ログを備える。scp を実際に呼び出すため、対象ホストへの疎通と
鍵配布が済んでいる環境でのみ実行すること。
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)

logger = logging.getLogger("config_patch")
audit_logger = logging.getLogger("config_patch.audit")


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def patch_config(base_dir: Path, filename: str, host: str, *, dry_run: bool) -> int:
    try:
        source = safe_resolve_path(base_dir, filename)
        validate_hostname(host)
    except (OSError, ValueError) as exc:
        logger.error("validation failed: %s", exc)
        return EXIT_USAGE

    if not source.is_file():
        logger.error("config file not found: %s", source)
        return EXIT_USAGE

    if dry_run:
        logger.info("dry-run: would copy %s to %s:/etc/app.conf", source, host)
        return EXIT_OK

    result = subprocess.run(
        ["scp", str(source), f"{host}:/etc/app.conf"],
        capture_output=True,
        text=True,
        timeout=30,
        shell=False,
        check=False,
    )
    actor = os.environ.get("USER", "unknown")
    if result.returncode != 0:
        logger.error("scp failed host=%s stderr=%s", host, result.stderr.strip())
        audit_logger.info(
            "operation=config-patch actor=%s target=%s result=failure", actor, host
        )
        return EXIT_RUNTIME

    logger.info("patched host=%s", host)
    audit_logger.info(
        "operation=config-patch actor=%s target=%s result=success", actor, host
    )
    return EXIT_OK


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy a config file to a target host")
    parser.add_argument("--base-dir", type=Path, default=Path("config"))
    parser.add_argument("--filename", required=True)
    parser.add_argument("--host", required=True)
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
    return patch_config(args.base_dir, args.filename, args.host, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
