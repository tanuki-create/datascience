#!/usr/bin/env python3
"""opsctl config-bulk-edit: 複数の設定ファイルへパターン置換を一括適用する。

書き込み前に必ずバックアップを取り、既定では常にdry-runとして動作する。
--execute を明示指定したときだけ実際にファイルを書き換える。
対象は ./work、./backups、/tmp/opsctl-lab 配下に限定する。

警告: 設定ファイルの一括置換は影響範囲が広い破壊的操作である。
本番相当の設定ディレクトリに向けて実行する前に、--dry-run の出力を
必ず確認し、変更管理の承認を得ること。
"""
from __future__ import annotations

import argparse
import csv
import difflib
import logging
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("opsctl.config_bulk_edit")

LAB_RELATIVE_ROOTS = ("work", "backups")
LAB_ABSOLUTE_ROOTS = ("/tmp/opsctl-lab",)


@dataclass
class EditResult:
    path: str
    changed: bool
    status: str
    backup_path: str = ""
    detail: str = ""


def assert_lab_path(path: Path) -> Path:
    resolved = path.resolve()
    cwd = Path.cwd().resolve()
    for rel_root in LAB_RELATIVE_ROOTS:
        allowed_root = (cwd / rel_root).resolve()
        if resolved == allowed_root or allowed_root in resolved.parents:
            return resolved
    for abs_root in LAB_ABSOLUTE_ROOTS:
        allowed_root = Path(abs_root).resolve()
        if resolved == allowed_root or allowed_root in resolved.parents:
            return resolved
    allowed_display = ", ".join(LAB_RELATIVE_ROOTS + LAB_ABSOLUTE_ROOTS)
    raise ValueError(f"path is outside allowed lab locations ({allowed_display}): {resolved}")


def backup_file(path: Path, base_dir: Path, backup_dir: Path) -> Path:
    relative = path.relative_to(base_dir)
    destination = backup_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    return destination


def apply_pattern(text: str, pattern: re.Pattern[str], replacement: str) -> tuple[str, int]:
    return pattern.subn(replacement, text)


def atomic_write(path: Path, content: str) -> None:
    tmp_path = path.with_name(path.name + f".tmp{os.getpid()}")
    tmp_path.write_text(content, encoding="utf-8")
    os.replace(tmp_path, path)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="opsctl config-bulk-edit: apply a pattern replacement across config files"
    )
    parser.add_argument("--base-dir", type=Path, required=True)
    parser.add_argument("--glob", default="*.conf")
    parser.add_argument("--pattern", required=True, help="regular expression to search for")
    parser.add_argument("--replacement", required=True, help=r"replacement text (re.sub syntax, e.g. \1)")
    parser.add_argument("--backup-dir", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=Path("work/reports/config_bulk_edit.csv"))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually rewrite files; without this flag the script only previews changes",
    )
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
        pattern = re.compile(args.pattern)
    except re.error as exc:
        logger.error("invalid --pattern: %s", exc)
        return EXIT_USAGE

    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    backup_dir = args.backup_dir or Path("backups") / "config_bulk_edit" / timestamp

    try:
        base_dir = assert_lab_path(args.base_dir)
        backup_dir = assert_lab_path(backup_dir)
    except ValueError as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    if not base_dir.is_dir():
        logger.error("base directory not found: %s", base_dir)
        return EXIT_USAGE

    if not args.execute:
        logger.warning("running in dry-run mode (default); pass --execute to actually rewrite files")

    files = sorted(p for p in base_dir.rglob(args.glob) if p.is_file())
    logger.info("found %s file(s) matching %s under %s", len(files), args.glob, base_dir)

    results: list[EditResult] = []
    had_failure = False

    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            logger.warning("failed to read %s: %s", path, exc)
            results.append(EditResult(str(path), False, "read-failed", detail=str(exc)))
            had_failure = True
            continue

        new_text, count = apply_pattern(original, pattern, args.replacement)
        if count == 0:
            results.append(EditResult(str(path), False, "no-match"))
            continue

        diff = "\n".join(
            difflib.unified_diff(
                original.splitlines(), new_text.splitlines(), fromfile=str(path), tofile=str(path), lineterm=""
            )
        )
        logger.debug("diff for %s:\n%s", path, diff)

        if not args.execute:
            logger.info("dry-run: %s replacement(s) would be applied to %s", count, path)
            results.append(EditResult(str(path), True, "dry-run", detail=f"{count} replacement(s)"))
            continue

        try:
            backup_path = backup_file(path, base_dir, backup_dir)
            atomic_write(path, new_text)
            logger.info("updated %s (%s replacement(s), backup=%s)", path, count, backup_path)
            results.append(
                EditResult(str(path), True, "updated", backup_path=str(backup_path), detail=f"{count} replacement(s)")
            )
        except OSError as exc:
            logger.error("failed to update %s: %s", path, exc)
            results.append(EditResult(str(path), True, "write-failed", detail=str(exc)))
            had_failure = True

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "changed", "status", "backup_path", "detail"])
        writer.writeheader()
        for r in results:
            writer.writerow(
                {
                    "path": r.path,
                    "changed": r.changed,
                    "status": r.status,
                    "backup_path": r.backup_path,
                    "detail": r.detail,
                }
            )

    changed_count = sum(1 for r in results if r.changed)
    logger.info("processed %s file(s), %s changed; report=%s", len(results), changed_count, args.report)
    return EXIT_RUNTIME if had_failure else EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
