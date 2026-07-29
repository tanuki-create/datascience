#!/usr/bin/env python3
"""opsctl cleanup-old: 一定日数より古いファイルを隔離または削除する。

安全側に倒すため、既定では常にdry-runとして動作し、--execute を明示
指定したときだけ実際にファイルを動かす。対象は ./work、./backups、
/tmp/opsctl-lab 配下に限定し、それ以外のパスは拒否する。

警告: --action delete --execute は元に戻せない削除を行う。
本番相当のパスに向けて実行しないこと。
まず --action quarantine（隔離）で運用し、問題が無いことを確認してから
削除に切り替えることを推奨する。
"""
from __future__ import annotations

import argparse
import csv
import logging
import shutil
import sys
import time
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

logger = logging.getLogger("opsctl.cleanup_old")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_MAX_AGE_DAYS = 30

LAB_RELATIVE_ROOTS = ("work", "backups")
LAB_ABSOLUTE_ROOTS = ("/tmp/opsctl-lab",)


@dataclass
class CleanupAction:
    path: str
    age_days: int
    action: str
    status: str
    detail: str = ""


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def assert_lab_path(path: Path) -> Path:
    """対象パスがラボ用ディレクトリ配下にあることを確認する。

    本番のルートや /var のような場所を誤って指定した場合に、
    処理を先へ進めないための安全弁である。
    """
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


def find_old_files(target_dir: Path, *, max_age_days: int, extensions: list[str] | None) -> list[Path]:
    cutoff = time.time() - (max_age_days * 86400)
    candidates: list[Path] = []
    for path in sorted(target_dir.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        if extensions and path.suffix not in extensions:
            continue
        try:
            mtime = path.stat().st_mtime
        except OSError as exc:
            logger.warning("failed to stat %s: %s", path, exc)
            continue
        if mtime <= cutoff:
            candidates.append(path)
    return candidates


def quarantine_file(path: Path, target_dir: Path, quarantine_dir: Path) -> Path:
    relative = path.relative_to(target_dir)
    destination = quarantine_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination = destination.with_name(f"{destination.name}.{int(time.time())}")
    shutil.move(str(path), str(destination))
    return destination


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="opsctl cleanup-old: quarantine or delete files older than a threshold"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--target-dir", type=Path, action="append", default=None, dest="target_dirs")
    parser.add_argument("--max-age-days", type=int, default=None)
    parser.add_argument("--extension", action="append", default=None, dest="extensions")
    parser.add_argument("--action", choices=["quarantine", "delete"], default="quarantine")
    parser.add_argument("--quarantine-dir", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=Path("work/reports/cleanup_old.csv"))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="actually move/delete files; without this flag the script only reports planned actions",
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
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    cleanup_cfg = config.get("cleanup", {})
    target_dirs = args.target_dirs or [Path(p) for p in cleanup_cfg.get("target_dirs", ["./work/tmp"])]
    max_age_days = (
        args.max_age_days if args.max_age_days is not None else int(cleanup_cfg.get("max_age_days", DEFAULT_MAX_AGE_DAYS))
    )
    extensions = args.extensions if args.extensions is not None else (cleanup_cfg.get("extensions") or None)
    quarantine_dir = args.quarantine_dir or Path(cleanup_cfg.get("quarantine_dir", "./work/quarantine"))

    if max_age_days <= 0:
        logger.error("--max-age-days must be positive")
        return EXIT_USAGE

    try:
        validated_targets = [assert_lab_path(d) for d in target_dirs]
        validated_quarantine = assert_lab_path(quarantine_dir) if args.action == "quarantine" else None
    except ValueError as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    if not args.execute:
        logger.warning("running in dry-run mode (default); pass --execute to actually %s files", args.action)
    elif args.action == "delete":
        logger.warning("--action delete --execute will permanently remove files; this cannot be undone")

    actions: list[CleanupAction] = []
    had_failure = False

    for resolved_target in validated_targets:
        if not resolved_target.is_dir():
            logger.warning("target directory not found, skipping: %s", resolved_target)
            continue
        for path in find_old_files(resolved_target, max_age_days=max_age_days, extensions=extensions):
            age_days = int((time.time() - path.stat().st_mtime) / 86400)

            if not args.execute:
                logger.info("dry-run: would %s %s (age=%sd)", args.action, path, age_days)
                actions.append(CleanupAction(str(path), age_days, args.action, "dry-run"))
                continue

            try:
                if args.action == "quarantine":
                    assert validated_quarantine is not None
                    destination = quarantine_file(path, resolved_target, validated_quarantine)
                    logger.info("quarantined %s -> %s", path, destination)
                    actions.append(CleanupAction(str(path), age_days, "quarantine", "done", str(destination)))
                else:
                    path.unlink()
                    logger.warning("deleted %s (age=%sd)", path, age_days)
                    actions.append(CleanupAction(str(path), age_days, "delete", "done"))
            except OSError as exc:
                logger.error("failed to %s %s: %s", args.action, path, exc)
                actions.append(CleanupAction(str(path), age_days, args.action, "failed", str(exc)))
                had_failure = True

    args.report.parent.mkdir(parents=True, exist_ok=True)
    with args.report.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "age_days", "action", "status", "detail"])
        writer.writeheader()
        for a in actions:
            writer.writerow(
                {"path": a.path, "age_days": a.age_days, "action": a.action, "status": a.status, "detail": a.detail}
            )

    logger.info("processed %s file(s); report=%s", len(actions), args.report)
    return EXIT_RUNTIME if had_failure else EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
