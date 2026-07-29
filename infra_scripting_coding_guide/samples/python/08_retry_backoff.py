#!/usr/bin/env python3
"""Ping hosts with retry and exponential backoff.

Distinguishes PermanentError (do not retry: e.g. command missing) from
RetryableError (retry with exponential backoff up to a limit), and
reports partial success without hiding failed hosts.
"""
from __future__ import annotations

import argparse
import csv
import logging
import random
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("retry_backoff")


class PermanentError(Exception):
    """Failure that will not be fixed by retrying."""


class RetryableError(Exception):
    """Failure that may succeed if attempted again."""


@dataclass
class HealthResult:
    host: str
    ok: bool
    attempts: int
    detail: str


def check_once(host: str, command: str, timeout: int) -> None:
    if shutil.which(command) is None:
        raise PermanentError(f"command not found: {command}")

    try:
        completed = subprocess.run(
            [command, "-c", "1", "-W", str(timeout), host],
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RetryableError(f"process timeout: {exc}") from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "check failed").strip()
        raise RetryableError(detail)


def check_with_retry(
    host: str,
    command: str,
    timeout: int,
    max_attempts: int,
    base_delay: float,
) -> HealthResult:
    attempt = 0
    while True:
        attempt += 1
        try:
            check_once(host, command, timeout)
            return HealthResult(host=host, ok=True, attempts=attempt, detail="ok")
        except PermanentError as exc:
            return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
        except RetryableError as exc:
            if attempt >= max_attempts:
                return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay * 0.1)
            sleep_for = delay + jitter
            logger.debug(
                "host=%s attempt=%s/%s retrying in %.2fs: %s",
                host,
                attempt,
                max_attempts,
                sleep_for,
                exc,
            )
            time.sleep(sleep_for)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        hosts.append(line)
    return hosts


def write_report(path: Path, results: list[HealthResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "ok", "attempts", "detail"])
        writer.writeheader()
        for r in results:
            writer.writerow({"host": r.host, "ok": r.ok, "attempts": r.attempts, "detail": r.detail})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Health-check hosts with retry and backoff")
    parser.add_argument("--hosts-file", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--command", default="ping")
    parser.add_argument("--timeout", type=int, default=2)
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--base-delay", type=float, default=0.5)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    run_id = str(uuid.uuid4())
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format=f"%(levelname)s run_id={run_id} %(message)s",
        stream=sys.stderr,
    )

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        print(f"設定が不正です。--hosts-file の内容を確認してください (run_id={run_id})", file=sys.stderr)
        logger.error("%s", exc)
        return EXIT_USAGE

    results = [
        check_with_retry(host, args.command, args.timeout, args.max_attempts, args.base_delay)
        for host in hosts
    ]

    write_report(args.report, results)
    failed = [r for r in results if not r.ok]
    for r in failed:
        logger.error("host=%s failed after %s attempts: %s", r.host, r.attempts, r.detail)

    logger.info("wrote %s results to %s (%s failed)", len(results), args.report, len(failed))
    return EXIT_RUNTIME if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
