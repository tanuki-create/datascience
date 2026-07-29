#!/usr/bin/env python3
"""疎通確認とディスク使用率の結果を突き合わせ、ホスト単位の総合ステータスを出す。

判定(aggregate_status)は純粋関数、通知(notify_if_critical)は外部呼び出しを
差し替え可能にした副作用関数、集計(load_and_aggregate)はI/Oを持つ関数として
責務を分ける(第5章)。第13章のテスト設計サンプルとして使う。
"""
from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3

logger = logging.getLogger("status_aggregator")


@dataclass
class HostStatus:
    host: str
    ping_ok: bool
    disk_status: str
    overall: str


def aggregate_status(ping_ok: bool, disk_status: str) -> str:
    """純粋関数。疎通確認とディスク判定を総合ステータスへまとめる。

    disk_status は "OK" | "WARNING" | "CRITICAL" を想定する。
    """
    if disk_status not in ("OK", "WARNING", "CRITICAL"):
        raise ValueError(f"invalid disk_status: {disk_status!r}")
    if disk_status == "CRITICAL":
        return "CRITICAL"
    if not ping_ok:
        return "WARNING"
    if disk_status == "WARNING":
        return "WARNING"
    return "OK"


def notify_if_critical(
    host: str,
    overall: str,
    *,
    notifier: Callable[[str], None],
) -> bool:
    """副作用のある関数。CRITICALのときだけ notifier を呼ぶ。

    notifier の実装(Slack通知、メール送信など)はテスト時に差し替える。
    """
    if overall != "CRITICAL":
        return False
    notifier(f"CRITICAL: {host} requires attention")
    return True


def load_ping_results(path: Path) -> dict[str, bool]:
    """副作用: ファイル読み込み。host,ok の2列CSVを読む。"""
    results: dict[str, bool] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            results[row["host"]] = row["ok"].strip().lower() in ("1", "true", "ok")
    return results


def load_disk_results(path: Path) -> dict[str, str]:
    """副作用: ファイル読み込み。host,status の2列CSVを読む。"""
    results: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            results[row["host"]] = row["status"].strip().upper()
    return results


def load_and_aggregate(ping_report: Path, disk_report: Path) -> list[HostStatus]:
    """副作用: 2つのレポートを読み、判定を突き合わせる。"""
    ping_results = load_ping_results(ping_report)
    disk_results = load_disk_results(disk_report)
    all_hosts = sorted(set(ping_results) | set(disk_results))

    statuses: list[HostStatus] = []
    for host in all_hosts:
        ping_ok = ping_results.get(host, False)
        disk_status = disk_results.get(host, "WARNING")  # 片方に情報が無ければ警告扱い
        overall = aggregate_status(ping_ok, disk_status)
        statuses.append(HostStatus(host=host, ping_ok=ping_ok, disk_status=disk_status, overall=overall))
    return statuses


def console_notifier(message: str) -> None:
    """既定のnotifier実装。標準エラーへ出すだけの最小実装。

    実運用ではSlack Webhookやメール送信に差し替える(第11章)。
    """
    logger.error("notify: %s", message)


def summarize_exit_code(statuses: list[HostStatus]) -> int:
    """純粋関数。"""
    if any(s.overall == "CRITICAL" for s in statuses):
        return EXIT_CRITICAL
    return EXIT_OK


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate ping and disk check results")
    parser.add_argument("--ping-report", type=Path, required=True)
    parser.add_argument("--disk-report", type=Path, required=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        statuses = load_and_aggregate(args.ping_report, args.disk_report)
    except (OSError, KeyError, ValueError) as exc:
        logger.error("failed to load reports: %s", exc)
        return EXIT_USAGE

    for status in statuses:
        notify_if_critical(status.host, status.overall, notifier=console_notifier)
        logger.info(
            "host=%s ping_ok=%s disk_status=%s overall=%s",
            status.host,
            status.ping_ok,
            status.disk_status,
            status.overall,
        )

    return summarize_exit_code(statuses)


if __name__ == "__main__":
    sys.exit(main())
