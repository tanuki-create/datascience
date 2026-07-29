#!/usr/bin/env python3
"""安全なパス検証と、安全な外部コマンド実行のデモ。

パストラバーサル対策として、指定ディレクトリ配下に解決できないパスを
拒否する。コマンドインジェクション対策として、ホスト名を検証したうえで
引数リスト形式（shell=False）で外部コマンドを呼ぶ。
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("safe_path_and_exec")

HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    """base_dir 配下に解決できないパスは拒否する。

    シンボリックリンクが base_dir の外を指している場合、この検証だけ
    では不十分になりうる。公開範囲が広い用途では、対象ディレクトリの
    書き込み権限を管理者以外に与えない運用と組み合わせること。
    """
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def safe_ping(host: str, timeout: int) -> tuple[bool, str]:
    """引数リストのみで ping を呼ぶ。シェル文字列を組み立てない。"""
    validate_hostname(host)
    cmd = ["ping", "-c", "1", "-W", str(timeout), host]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "ping process timeout"
    except FileNotFoundError:
        return False, "ping command not found"
    detail = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode == 0, detail


def write_temp_report(content: str) -> Path:
    """予測可能な名前を避け、所有者のみ読み書き可能な一時ファイルを作る。"""
    fd, name = tempfile.mkstemp(prefix="opsctl_", suffix=".txt")
    tmp_path = Path(name)
    try:
        with tmp_path.open("w", encoding="utf-8") as fh:
            fh.write(content)
    finally:
        os.close(fd)
    tmp_path.chmod(0o600)
    return tmp_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demonstrate safe path and command handling")
    parser.add_argument("--base-dir", type=Path, required=True)
    parser.add_argument("--relative-path", required=True)
    parser.add_argument("--host", default=None)
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        resolved = safe_resolve_path(args.base_dir, args.relative_path)
    except (OSError, ValueError) as exc:
        logger.error("path validation failed: %s", exc)
        return EXIT_USAGE
    logger.info("resolved path: %s", resolved)

    if args.host:
        try:
            ok, detail = safe_ping(args.host, args.timeout)
        except ValueError as exc:
            logger.error("host validation failed: %s", exc)
            return EXIT_USAGE
        logger.info("ping host=%s ok=%s detail=%s", args.host, ok, detail)
        if not ok:
            return EXIT_RUNTIME

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
