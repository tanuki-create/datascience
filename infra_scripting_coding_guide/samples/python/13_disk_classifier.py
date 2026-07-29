#!/usr/bin/env python3
"""ディスク使用率を分類する opsctl の補助モジュール。

第13章のテスト例（ユニット、境界値、モック、結合）で対象にするコードである。
`df -P` 相当のテキストをパースし、閾値に基づいて ok/warning/critical に分類する。
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import TextIO

logger = logging.getLogger("opsctl.disk_classifier")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3


class InvalidThresholdError(ValueError):
    """warn/crit の閾値関係が不正なときに送出する。"""


@dataclass
class DiskUsage:
    mount_point: str
    used_percent: float


@dataclass
class ClassifiedUsage:
    mount_point: str
    used_percent: float
    status: str


def classify_disk_usage(used_percent: float, warn_percent: float, crit_percent: float) -> str:
    """使用率を ``ok``/``warning``/``critical`` に分類する。

    境界値は「以上」で次の段階に上がる。
    つまり ``used_percent == warn_percent`` は ``warning`` になり、
    ``used_percent == crit_percent`` は ``critical`` になる。
    """
    if warn_percent > crit_percent:
        raise InvalidThresholdError(
            f"warn_percent ({warn_percent}) must be <= crit_percent ({crit_percent})"
        )
    if used_percent < 0 or used_percent > 100:
        raise ValueError(f"used_percent out of range: {used_percent}")

    if used_percent >= crit_percent:
        return "critical"
    if used_percent >= warn_percent:
        return "warning"
    return "ok"


def parse_df_output(text: str) -> list[DiskUsage]:
    """``df -P`` 相当のテキストをパースする。

    先頭行はヘッダーとして無視する。
    列数が不足する行や使用率が数値でない行は、警告ログを出して読み飛ばす。
    """
    results: list[DiskUsage] = []
    lines = text.strip("\n").splitlines()
    if not lines:
        return results

    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 6:
            logger.warning("skipping malformed df line: %r", line)
            continue
        percent_field = fields[4].rstrip("%")
        try:
            used_percent = float(percent_field)
        except ValueError:
            logger.warning("skipping non-numeric percent field: %r", line)
            continue
        mount_point = fields[5]
        results.append(DiskUsage(mount_point=mount_point, used_percent=used_percent))
    return results


def fetch_disk_report(host: str, timeout: int = 10) -> list[DiskUsage]:
    """対象ホストで ``ssh host df -P`` を実行し、結果をパースする。

    外部プロセス呼び出しを ``parse_df_output`` から分離してあるため、
    テストでは ``subprocess.run`` だけをモックすれば、実際の ``ssh`` 接続なしに
    このパースロジックまで通した結合テストができる。
    """
    completed = subprocess.run(
        ["ssh", host, "df", "-P"],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"df on {host} failed: {completed.stderr.strip()}")
    return parse_df_output(completed.stdout)


def classify_all(
    usages: list[DiskUsage], warn_percent: float, crit_percent: float
) -> tuple[list[ClassifiedUsage], str]:
    """複数のディスク使用率をまとめて分類し、最悪ステータスも返す。"""
    results: list[ClassifiedUsage] = []
    worst = "ok"
    severity = {"ok": 0, "warning": 1, "critical": 2}

    for usage in usages:
        status = classify_disk_usage(usage.used_percent, warn_percent, crit_percent)
        results.append(
            ClassifiedUsage(mount_point=usage.mount_point, used_percent=usage.used_percent, status=status)
        )
        if severity[status] > severity[worst]:
            worst = status

    return results, worst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="disk_classifier", description="Classify disk usage from df -P output"
    )
    parser.add_argument("--host", help="remote host to query via ssh")
    parser.add_argument(
        "--input-file",
        type=argparse.FileType("r", encoding="utf-8"),
        help="local df -P output, mainly for testing without ssh",
    )
    parser.add_argument("--warn-percent", type=float, default=80.0)
    parser.add_argument("--crit-percent", type=float, default=90.0)
    parser.add_argument("--timeout", type=int, default=10)
    return parser


def _read_usages(args: argparse.Namespace) -> list[DiskUsage]:
    if args.input_file is not None:
        input_file: TextIO = args.input_file
        try:
            return parse_df_output(input_file.read())
        finally:
            input_file.close()
    return fetch_disk_report(args.host, timeout=args.timeout)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.host and args.input_file is None:
        parser.error("either --host or --input-file is required")

    try:
        usages = _read_usages(args)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        logger.error("failed to collect disk usage: %s", exc)
        return EXIT_RUNTIME

    try:
        results, worst = classify_all(usages, args.warn_percent, args.crit_percent)
    except InvalidThresholdError as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    print(json.dumps({"results": [asdict(r) for r in results], "worst": worst}, ensure_ascii=False))

    if worst == "critical":
        return EXIT_CRITICAL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
