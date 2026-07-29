#!/usr/bin/env python3
"""Safely update a text configuration file.

Takes a timestamped backup before writing, and replaces the target file
atomically via a temporary file in the same directory plus os.replace().

WARNING: this script overwrites --target in place (after backing it up).
Do not point --target at a production file without testing in a sandbox
first.
"""
from __future__ import annotations

import argparse
import logging
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("safe_config_update")


def backup_path(path: Path, backup_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir / f"{path.name}.{timestamp}.bak"


def validate_not_empty(content: str) -> None:
    if not content.strip():
        raise ValueError("refusing to write empty content")


def update_config(
    path: Path,
    new_content: str,
    backup_dir: Path,
    validate: Callable[[str], None] | None = None,
) -> Path | None:
    """Back up the existing file (if any), then atomically replace it.

    Returns the backup path, or None if there was nothing to back up.
    """
    if validate is not None:
        validate(new_content)

    backup: Path | None = None
    if path.exists():
        backup = backup_path(path, backup_dir)
        shutil.copy2(path, backup)

    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new_content)
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    return backup


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update a config file")
    parser.add_argument("--target", type=Path, required=True, help="file to update")
    parser.add_argument("--content-file", type=Path, required=True, help="new content source")
    parser.add_argument("--backup-dir", type=Path, required=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if not args.content_file.is_file():
        logger.error("content file not found: %s", args.content_file)
        return EXIT_USAGE

    new_content = args.content_file.read_text(encoding="utf-8")

    try:
        backup = update_config(args.target, new_content, args.backup_dir, validate=validate_not_empty)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME

    if backup is not None:
        logger.info("backed up previous content to %s", backup)
    else:
        logger.info("no previous file; created %s", args.target)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
