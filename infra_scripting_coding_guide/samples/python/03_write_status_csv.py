#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

logger = logging.getLogger("write_status_csv")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write status CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument(
        "--status",
        required=True,
        choices=["OK", "WARNING", "CRITICAL", "ERROR"],
    )
    parser.add_argument("--detail", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s %(message)s",
    )

    if any(ch.isspace() for ch in args.host):
        logger.error("host must not contain whitespace")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.output.exists()
    with args.output.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "status", "detail"])
        if write_header:
            writer.writeheader()
        writer.writerow(
            {"host": args.host, "status": args.status, "detail": args.detail}
        )

    logger.info("appended row to %s", args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
