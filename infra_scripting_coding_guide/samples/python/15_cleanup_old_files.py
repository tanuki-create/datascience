#!/usr/bin/env python3
"""opsctl cleanup-old-files (learning sample). Default is quarantine, not delete."""
from __future__ import annotations

import argparse
import logging
import shutil
import sys
import time
from pathlib import Path

EXIT_OK, EXIT_USAGE, EXIT_RUNTIME = 0, 1, 2
logger = logging.getLogger("opsctl.cleanup")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--target-dir", type=Path, required=True)
    p.add_argument("--max-age-days", type=int, default=30)
    p.add_argument("--extension", action="append", default=[".tmp", ".log"])
    p.add_argument("--quarantine-dir", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument(
        "--delete",
        action="store_true",
        help="DANGEROUS: permanently delete instead of quarantine",
    )
    return p.parse_args(argv)


def candidates(root: Path, max_age_days: int, extensions: list[str]) -> list[Path]:
    cutoff = time.time() - max_age_days * 86400
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in extensions:
            continue
        if path.stat().st_mtime < cutoff:
            out.append(path)
    return out


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if not args.target_dir.is_dir():
        return EXIT_USAGE
    files = candidates(args.target_dir, args.max_age_days, args.extension)
    logger.info("candidates=%d", len(files))
    for path in files:
        logger.info("candidate path=%s", path)
    if args.dry_run:
        return EXIT_OK
    try:
        if args.delete:
            logger.warning("DELETE mode enabled")
            for path in files:
                path.unlink()
        else:
            args.quarantine_dir.mkdir(parents=True, exist_ok=True)
            for path in files:
                dest = args.quarantine_dir / path.name
                if dest.exists():
                    dest = args.quarantine_dir / f"{path.stem}-{int(time.time())}{path.suffix}"
                shutil.move(str(path), str(dest))
    except OSError as exc:
        logger.error("cleanup failed: %s", exc)
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
