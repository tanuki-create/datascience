#!/usr/bin/env python3
"""opsctl ping-check（発展版）: 複数ホストへ並列に疎通確認を行う。

第2章の samples/python/02_ping_check.py を、設定ファイル対応・並列実行・
重要ホスト判定・全体デッドラインに拡張したものである。

このスクリプトは ping コマンドを外部プロセスとして呼び出す。
対象ホストが実在しない、またはICMPをブロックする環境では、
失敗が正しい結果として報告される。
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import logging
import platform
import subprocess
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
EXIT_CRITICAL = 3
EXIT_TIMEOUT = 4

logger = logging.getLogger("opsctl.ping_check")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_TIMEOUT_SECONDS = 3
DEFAULT_MAX_WORKERS = 8
DEFAULT_DEADLINE_SECONDS = 60.0


@dataclass
class PingResult:
    host: str
    ok: bool
    elapsed_ms: int
    detail: str


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {line_no}: {line!r}")
        hosts.append(line)
    if not hosts:
        raise ValueError(f"hosts file is empty: {path}")
    return hosts


def ping_host(host: str, timeout: int) -> PingResult:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        # Linuxの -W は秒指定。macOSの -W はミリ秒指定であり挙動が異なる。
        # ラボ環境はLinuxを前提にする。
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]

    started = time.monotonic()
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        elapsed_ms = int((time.monotonic() - started) * 1000)
        return PingResult(host, False, elapsed_ms, "ping process timeout")
    except FileNotFoundError:
        elapsed_ms = int((time.monotonic() - started) * 1000)
        return PingResult(host, False, elapsed_ms, "ping command not found")

    elapsed_ms = int((time.monotonic() - started) * 1000)
    if completed.returncode == 0:
        return PingResult(host, True, elapsed_ms, "ok")
    detail_lines = (completed.stderr or completed.stdout or "ping failed").strip().splitlines()
    return PingResult(host, False, elapsed_ms, detail_lines[0] if detail_lines else "ping failed")


def run_checks(
    hosts: list[str], *, timeout: int, max_workers: int, deadline_seconds: float
) -> tuple[list[PingResult], bool]:
    """全ホストを並列に確認する。deadline_seconds以内に終わらないホストはタイムアウト扱いにする。"""
    results: dict[str, PingResult] = {}
    deadline_hit = False

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping_host, host, timeout): host for host in hosts}
        try:
            for future in concurrent.futures.as_completed(futures, timeout=deadline_seconds):
                host = futures[future]
                results[host] = future.result()
        except concurrent.futures.TimeoutError:
            deadline_hit = True
            for future, host in futures.items():
                if host not in results:
                    future.cancel()
                    results[host] = PingResult(
                        host, False, int(deadline_seconds * 1000), "overall deadline exceeded"
                    )

    return [results[h] for h in hosts], deadline_hit


def write_report(path: Path, results: list[PingResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "ok", "elapsed_ms", "detail"])
        writer.writeheader()
        for r in results:
            writer.writerow(
                {"host": r.host, "ok": "true" if r.ok else "false", "elapsed_ms": r.elapsed_ms, "detail": r.detail}
            )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl ping-check: parallel connectivity check")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--hosts-file", type=Path, default=None)
    parser.add_argument("--timeout", type=int, default=None, help="per-host timeout in seconds")
    parser.add_argument("--max-workers", type=int, default=None)
    parser.add_argument("--deadline", type=float, default=None, help="overall deadline in seconds")
    parser.add_argument("--report", type=Path, default=Path("work/reports/ping_check.csv"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.verbose and args.quiet:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
        logger.error("--verbose and --quiet are mutually exclusive")
        return EXIT_USAGE
    level = logging.WARNING if args.quiet else (logging.DEBUG if args.verbose else logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    ping_cfg = config.get("ping_check", {})
    hosts_file = args.hosts_file or Path(
        ping_cfg.get("hosts_file", config.get("paths", {}).get("hosts_file", "config/hosts.txt"))
    )
    timeout = (
        args.timeout
        if args.timeout is not None
        else int(ping_cfg.get("timeout_seconds", config.get("defaults", {}).get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)))
    )
    max_workers = args.max_workers if args.max_workers is not None else int(ping_cfg.get("max_workers", DEFAULT_MAX_WORKERS))
    deadline_seconds = (
        args.deadline if args.deadline is not None else float(ping_cfg.get("deadline_seconds", DEFAULT_DEADLINE_SECONDS))
    )
    critical_hosts = set(ping_cfg.get("critical_hosts", []))

    if timeout <= 0:
        logger.error("--timeout must be positive")
        return EXIT_USAGE
    if max_workers <= 0:
        logger.error("--max-workers must be positive")
        return EXIT_USAGE

    try:
        hosts = load_hosts(hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    if args.dry_run:
        for host in hosts:
            logger.info("dry-run: would ping host=%s timeout=%s", host, timeout)
        logger.info("dry-run: %s host(s), max_workers=%s, deadline=%ss", len(hosts), max_workers, deadline_seconds)
        return EXIT_OK

    results, deadline_hit = run_checks(
        hosts, timeout=timeout, max_workers=max_workers, deadline_seconds=deadline_seconds
    )

    for r in results:
        logger.info("host=%s ok=%s elapsed_ms=%s detail=%s", r.host, r.ok, r.elapsed_ms, r.detail)

    write_report(args.report, results)
    logger.info("wrote report to %s", args.report)

    failed_hosts = [r.host for r in results if not r.ok]

    if deadline_hit:
        completed = sum(1 for r in results if r.detail != "overall deadline exceeded")
        logger.error("deadline exceeded before all hosts finished (%s/%s completed)", completed, len(hosts))
        return EXIT_TIMEOUT
    if not failed_hosts:
        return EXIT_OK
    hit_critical = critical_hosts.intersection(failed_hosts)
    if hit_critical:
        logger.error("critical host(s) unreachable: %s", ", ".join(sorted(hit_critical)))
        return EXIT_CRITICAL
    logger.warning("some hosts unreachable: %s", ", ".join(failed_hosts))
    return EXIT_RUNTIME


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
