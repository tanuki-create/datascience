#!/usr/bin/env python3
"""Classify disk usage rows and write a status report.

Demonstrates separating pure functions (classify, summarize_exit_code)
from functions with side effects (load_usages, write_report).
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CRITICAL = 3

logger = logging.getLogger("disk_report")


@dataclass
class HostUsage:
    host: str
    usage_percent: float


def load_usages(path: Path) -> list[HostUsage]:
    """Side effect: reads a file from disk."""
    if not path.is_file():
        raise FileNotFoundError(f"usage file not found: {path}")
    usages: list[HostUsage] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            usages.append(HostUsage(host=row["host"], usage_percent=float(row["usage_percent"])))
    return usages


def classify(usage_percent: float, warn: float, crit: float) -> str:
    """Pure function: no I/O, deterministic output."""
    if usage_percent >= crit:
        return "CRITICAL"
    if usage_percent >= warn:
        return "WARNING"
    return "OK"


def summarize_exit_code(statuses: list[str]) -> int:
    """Pure function."""
    if "CRITICAL" in statuses:
        return EXIT_CRITICAL
    return EXIT_OK


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    """Side effect: writes a file to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "usage_percent", "status"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify disk usage and write a report")
    parser.add_argument("--input", type=Path, required=True, help="host,usage_percent CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warn", type=float, default=80.0)
    parser.add_argument("--crit", type=float, default=90.0)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if args.warn > args.crit:
        logger.error("--warn must be <= --crit")
        return EXIT_USAGE

    try:
        usages = load_usages(args.input)
    except (OSError, ValueError, KeyError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    rows: list[dict[str, str]] = []
    statuses: list[str] = []
    for item in usages:
        status = classify(item.usage_percent, args.warn, args.crit)
        statuses.append(status)
        rows.append(
            {
                "host": item.host,
                "usage_percent": str(item.usage_percent),
                "status": status,
            }
        )

    write_report(args.output, rows)
    logger.info("wrote %s rows to %s", len(rows), args.output)
    return summarize_exit_code(statuses)


if __name__ == "__main__":
    sys.exit(main())
