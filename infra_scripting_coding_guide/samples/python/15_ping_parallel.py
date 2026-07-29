#!/usr/bin/env python3
"""opsctl ping-check: concurrent host reachability (learning sample)."""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import logging
import platform
import subprocess
import sys
import uuid
from pathlib import Path

EXIT_OK, EXIT_USAGE, EXIT_RUNTIME, EXIT_WARN = 0, 1, 2, 3
logger = logging.getLogger("opsctl.ping")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Concurrent ping check")
    p.add_argument("--hosts-file", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--timeout", type=int, default=3)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args(argv)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    hosts: list[str] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {i}")
        hosts.append(line)
    if not hosts:
        raise ValueError("empty hosts file")
    return hosts


def ping_one(host: str, timeout: int) -> tuple[str, bool, str]:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 2)
    except subprocess.TimeoutExpired:
        return host, False, "timeout"
    except FileNotFoundError:
        return host, False, "ping not found"
    if cp.returncode == 0:
        return host, True, "ok"
    detail = (cp.stderr or cp.stdout or "fail").strip().splitlines()
    return host, False, detail[0] if detail else "fail"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    run_id = str(uuid.uuid4())
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format=f"%(asctime)s %(levelname)s run_id={run_id} %(message)s",
    )

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("input error: %s", exc)
        return EXIT_USAGE

    if args.dry_run:
        logger.info("dry-run hosts=%s", ",".join(hosts))
        return EXIT_OK

    args.report.parent.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, bool, str]] = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = [ex.submit(ping_one, h, args.timeout) for h in hosts]
            for fut in concurrent.futures.as_completed(futs):
                rows.append(fut.result())
    except Exception as exc:  # noqa: BLE001
        logger.exception("runtime failure: %s", exc)
        return EXIT_RUNTIME

    with args.report.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["host", "ok", "detail"])
        for host, ok, detail in sorted(rows):
            w.writerow([host, "true" if ok else "false", detail])
            if ok:
                logger.info("host=%s result=ok", host)
            else:
                logger.warning("host=%s result=fail detail=%s", host, detail)

    failed = sum(1 for _, ok, _ in rows if not ok)
    return EXIT_WARN if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
