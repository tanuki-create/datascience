#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import sys

logger = logging.getLogger("classify_usage")


def classify(usage: float, warn: float, crit: float) -> str:
    if usage < 0 or usage > 100:
        raise ValueError("usage must be between 0 and 100")
    if warn < 0 or crit < 0 or warn > 100 or crit > 100:
        raise ValueError("thresholds must be between 0 and 100")
    if warn > crit:
        raise ValueError("warn must be <= crit")
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


def status_to_exit(status: str) -> int:
    if status == "CRITICAL":
        return 3
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify disk usage percent")
    parser.add_argument("--usage", type=float, required=True)
    parser.add_argument("--warn", type=float, default=80)
    parser.add_argument("--crit", type=float, default=90)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s %(message)s",
    )
    try:
        status = classify(args.usage, args.warn, args.crit)
    except ValueError as exc:
        logger.error("%s", exc)
        return 1
    print(status)
    return status_to_exit(status)


if __name__ == "__main__":
    sys.exit(main())
