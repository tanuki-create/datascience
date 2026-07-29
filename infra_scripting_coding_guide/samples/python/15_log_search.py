#!/usr/bin/env python3
"""opsctl log-search: 複数ディレクトリのログファイルを正規表現で検索する。

大きなログファイルでも全体をメモリに載せないよう、1行ずつストリームで
読み込む。バイナリファイルや読み取り権限のないファイルは警告して
スキップし、全体の失敗にはしない。
"""
from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("opsctl.log_search")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_MAX_FILES = 200
DEFAULT_MAX_MATCHES = 5000


@dataclass
class Match:
    path: str
    line_no: int
    line: str


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def iter_candidate_files(target_dirs: list[Path], glob_pattern: str, max_files: int) -> list[Path]:
    files: list[Path] = []
    for target_dir in target_dirs:
        if not target_dir.is_dir():
            logger.warning("target directory not found, skipping: %s", target_dir)
            continue
        for path in sorted(target_dir.rglob(glob_pattern)):
            if not path.is_file():
                continue
            files.append(path)
            if len(files) >= max_files:
                logger.warning("max_files=%s reached, remaining files are ignored", max_files)
                return files
    return files


def is_probably_binary(path: Path, sample_size: int = 2048) -> bool:
    try:
        with path.open("rb") as fh:
            chunk = fh.read(sample_size)
    except OSError:
        return True
    return b"\x00" in chunk


def search_file(
    path: Path, pattern: re.Pattern[str], max_matches: int, matches_so_far: int
) -> tuple[list[Match], bool]:
    """1ファイルを検索する。戻り値は (マッチ一覧, 読み取りエラーの有無)。"""
    matches: list[Match] = []
    if is_probably_binary(path):
        logger.debug("skipping binary-looking file: %s", path)
        return matches, False
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line_no, line in enumerate(fh, start=1):
                if matches_so_far + len(matches) >= max_matches:
                    logger.warning("max_matches=%s reached, stopping search", max_matches)
                    return matches, False
                if pattern.search(line):
                    matches.append(Match(str(path), line_no, line.rstrip("\n")))
    except OSError as exc:
        logger.warning("failed to read %s: %s", path, exc)
        return matches, True
    return matches, False


def write_report(path: Path, matches: list[Match]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "line_no", "line"])
        writer.writeheader()
        for m in matches:
            writer.writerow({"path": m.path, "line_no": m.line_no, "line": m.line})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl log-search: search log files for a pattern")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--pattern", required=True, help="regular expression to search for")
    parser.add_argument("--target-dir", type=Path, action="append", default=None, dest="target_dirs")
    parser.add_argument("--glob", default="*.log", help="filename glob under each target dir (default: *.log)")
    parser.add_argument("--max-files", type=int, default=None)
    parser.add_argument("--max-matches", type=int, default=None)
    parser.add_argument("--report", type=Path, default=Path("work/reports/log_search.csv"))
    parser.add_argument("--ignore-case", action="store_true")
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

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    log_search_cfg = config.get("log_search", {})
    target_dirs = args.target_dirs or [Path(p) for p in log_search_cfg.get("target_dirs", ["./work/logs"])]
    max_files = args.max_files if args.max_files is not None else int(log_search_cfg.get("max_files", DEFAULT_MAX_FILES))
    max_matches = (
        args.max_matches if args.max_matches is not None else int(log_search_cfg.get("max_matches", DEFAULT_MAX_MATCHES))
    )

    try:
        flags = re.IGNORECASE if args.ignore_case else 0
        pattern = re.compile(args.pattern, flags)
    except re.error as exc:
        logger.error("invalid --pattern: %s", exc)
        return EXIT_USAGE

    files = iter_candidate_files(target_dirs, args.glob, max_files)
    logger.info("found %s candidate file(s) under %s", len(files), ", ".join(str(d) for d in target_dirs))

    if args.dry_run:
        for f in files:
            logger.info("dry-run: would search %s", f)
        return EXIT_OK

    all_matches: list[Match] = []
    had_read_error = False
    for f in files:
        matches, read_error = search_file(f, pattern, max_matches, len(all_matches))
        all_matches.extend(matches)
        had_read_error = had_read_error or read_error
        if len(all_matches) >= max_matches:
            break

    write_report(args.report, all_matches)
    logger.info("matched %s line(s) across %s file(s); report=%s", len(all_matches), len(files), args.report)

    if had_read_error:
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
