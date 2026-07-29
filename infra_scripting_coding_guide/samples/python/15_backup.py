#!/usr/bin/env python3
"""opsctl backup: ソースディレクトリをtarballへ固め、保持期間を過ぎた
古いバックアップを整理する（Python実装）。

危険な操作を含む: 保持期間を超えた古いバックアップの削除。
必ず --dry-run で削除対象を確認してから実行すること。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import sys
import tarfile
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")

logger = logging.getLogger("opsctl.backup")


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_archive(source_dirs: list[Path], backup_dir: Path, timestamp: str) -> tuple[Path, Path]:
    """一時ファイルにアーカイブを作成してから原子的にリネームする。

    途中で失敗しても、backup_dir に半端なアーカイブが残らないようにする。
    """
    backup_dir.mkdir(parents=True, exist_ok=True)
    archive_path = backup_dir / f"backup_{timestamp}.tar.gz"

    fd, tmp_name = tempfile.mkstemp(dir=backup_dir, prefix=f".backup_{timestamp}.", suffix=".tar.gz")
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        with tarfile.open(tmp_path, "w:gz") as tar:
            for source in source_dirs:
                tar.add(source, arcname=source.name)
        tmp_path.replace(archive_path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    checksum = sha256_of(archive_path)
    checksum_path = archive_path.with_name(archive_path.name + ".sha256")
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n", encoding="utf-8")
    return archive_path, checksum_path


def find_old_backups(backup_dir: Path, retention_days: int, *, now: float | None = None) -> list[Path]:
    if not backup_dir.is_dir():
        return []
    cutoff = (now if now is not None else time.time()) - retention_days * 86400
    old: list[Path] = []
    for path in sorted(backup_dir.glob("backup_*.tar.gz")):
        try:
            if path.stat().st_mtime < cutoff:
                old.append(path)
        except OSError:
            continue
    return old


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl backup: archive directories and enforce retention")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--source", type=Path, action="append", default=None, help="repeatable")
    parser.add_argument("--backup-dir", type=Path, default=None)
    parser.add_argument("--retention-days", type=int, default=None)
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

    backup_config = config.get("backup", {})
    source_dirs = args.source or [Path(p) for p in backup_config.get("source_dirs", ["./config"])]
    backup_dir = args.backup_dir or Path(config.get("paths", {}).get("backup_dir", "./backups"))
    retention_days = args.retention_days or int(backup_config.get("retention_days", 14))

    for source in source_dirs:
        if not source.is_dir():
            logger.error("source directory not found: %s", source)
            return EXIT_USAGE

    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    if args.dry_run:
        logger.info(
            "dry-run: would create backup_%s.tar.gz from %s", timestamp, [str(s) for s in source_dirs]
        )
    else:
        try:
            archive_path, checksum_path = create_archive(source_dirs, backup_dir, timestamp)
        except OSError as exc:
            logger.error("failed to create archive: %s", exc)
            return EXIT_RUNTIME
        size_mb = archive_path.stat().st_size / (1024 * 1024)
        logger.info("created backup %s (%.2f MiB), checksum=%s", archive_path, size_mb, checksum_path)

    old_backups = find_old_backups(backup_dir, retention_days)
    if old_backups:
        logger.warning("%s backup(s) older than %s day(s) found", len(old_backups), retention_days)
    for path in old_backups:
        if args.dry_run:
            logger.info("dry-run: would delete %s", path)
        else:
            path.unlink(missing_ok=True)
            checksum_path = path.with_name(path.name + ".sha256")
            checksum_path.unlink(missing_ok=True)
            logger.info("deleted old backup %s", path)

    summary = {
        "run_id": run_id,
        "subcommand": "backup",
        "sources": len(source_dirs),
        "old_backups": len(old_backups),
        "dry_run": args.dry_run,
    }
    print(json.dumps(summary))
    logger.info(
        "finished sources=%s old_backups=%s dry_run=%s", len(source_dirs), len(old_backups), args.dry_run
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
