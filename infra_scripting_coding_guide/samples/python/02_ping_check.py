#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import platform
import subprocess
import sys
import time
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("ping_check")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ping hosts from a list file")
    parser.add_argument("--hosts-file", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {line_no}")
        hosts.append(line)
    if not hosts:
        raise ValueError("hosts file is empty")
    return hosts


def ping_host(host: str, timeout: int) -> tuple[bool, str]:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        # Linux: -W seconds. macOS: -W is milliseconds; prefer Python on macOS labs.
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "ping process timeout"
    except FileNotFoundError:
        return False, "ping command not found"

    if completed.returncode == 0:
        return True, "ok"
    detail = (completed.stderr or completed.stdout or "ping failed").strip().splitlines()
    return False, detail[0] if detail else "ping failed"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if args.timeout <= 0:
        logger.error("--timeout must be positive")
        return EXIT_USAGE

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    args.report.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    failures = 0

    for host in hosts:
        if args.dry_run:
            logger.info("dry-run: would ping %s timeout=%s", host, args.timeout)
            rows.append({"host": host, "ok": "dry-run", "detail": "skipped"})
            continue

        started = time.monotonic()
        ok, detail = ping_host(host, args.timeout)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        logger.info("host=%s ok=%s elapsed_ms=%s detail=%s", host, ok, elapsed_ms, detail)
        rows.append({"host": host, "ok": "true" if ok else "false", "detail": detail})
        if not ok:
            failures += 1

    with args.report.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "ok", "detail"])
        writer.writeheader()
        writer.writerows(rows)

    if args.dry_run:
        return EXIT_OK
    return EXIT_OK if failures == 0 else EXIT_RUNTIME


if __name__ == "__main__":
    sys.exit(main())
