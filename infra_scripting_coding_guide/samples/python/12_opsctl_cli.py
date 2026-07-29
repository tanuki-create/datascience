#!/usr/bin/env python3
"""opsctlのCLIスケルトン: 設定優先順位、サブコマンド、dry-run、サマリー出力。

ping-check と disk-check は説明用の簡略実装であり、実際の疎通確認や
ディスク使用率取得は第15章で実装する。
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - guidance for missing dependency
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3
EXIT_TIMEOUT = 4

logger = logging.getLogger("opsctl")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_TIMEOUT_SECONDS = 30


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def resolve_timeout(cli_value: int | None, config: dict[str, Any]) -> int:
    """CLI引数 > 環境変数 > 設定ファイル > デフォルトの順で解決する。"""
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get("OPSCTL_TIMEOUT_SECONDS")
    if env_value:
        return int(env_value)
    configured = config.get("defaults", {}).get("timeout_seconds")
    if configured is not None:
        return int(configured)
    return DEFAULT_TIMEOUT_SECONDS


@dataclass
class RunSummary:
    subcommand: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    failed: int = 0

    def exit_code(self) -> int:
        if self.critical:
            return EXIT_CRITICAL
        if self.failed:
            return EXIT_RUNTIME
        return EXIT_OK

    def render(self) -> str:
        return (
            f"summary subcommand={self.subcommand} total={self.total} "
            f"ok={self.ok} warning={self.warning} critical={self.critical} failed={self.failed}"
        )


def configure_logging(*, verbose: bool, quiet: bool) -> None:
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)


def run_ping_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    timeout = resolve_timeout(args.timeout, config)
    hosts_file = args.hosts_file or Path(config.get("paths", {}).get("hosts_file", "config/hosts.txt"))
    summary = RunSummary(subcommand="ping-check")

    if not hosts_file.is_file():
        logger.error("hosts file not found: %s", hosts_file)
        summary.failed = 1
        return summary

    hosts = [
        line.strip()
        for line in hosts_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    summary.total = len(hosts)

    for host in hosts:
        if args.dry_run:
            logger.info("dry-run: would ping host=%s timeout=%s", host, timeout)
        else:
            # 実際の疎通確認は第15章で実装する。ここでは常に成功扱いにする。
            logger.info("checked host=%s timeout=%s", host, timeout)
        summary.ok += 1

    return summary


def run_disk_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    warn_percent = config.get("defaults", {}).get("disk_warn_percent", 80)
    crit_percent = config.get("defaults", {}).get("disk_crit_percent", 90)
    summary = RunSummary(subcommand="disk-check")
    summary.total = 1

    if args.dry_run:
        logger.info("dry-run: would check disk usage warn=%s crit=%s", warn_percent, crit_percent)
    else:
        # 実際のディスク使用率取得は第15章で実装する。ここでは常にOK扱いにする。
        logger.info("disk usage checked warn=%s crit=%s", warn_percent, crit_percent)
    summary.ok = 1
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opsctl", description="Operations control CLI (teaching skeleton)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without making changes")
    parser.add_argument("--verbose", action="store_true", help="enable DEBUG logging")
    parser.add_argument("--quiet", action="store_true", help="only show WARNING and above")
    parser.add_argument("--timeout", type=int, default=None, help="override timeout in seconds")

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    ping_parser = subparsers.add_parser("ping-check", help="check connectivity to hosts")
    ping_parser.add_argument("--hosts-file", type=Path, default=None)

    subparsers.add_parser("disk-check", help="check disk usage thresholds")

    return parser


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet are mutually exclusive")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    if args.subcommand == "ping-check":
        summary = run_ping_check(args, config)
    elif args.subcommand == "disk-check":
        summary = run_disk_check(args, config)
    else:  # pragma: no cover - argparse enforces valid subcommand
        logger.error("unknown subcommand: %s", args.subcommand)
        return EXIT_USAGE

    print(summary.render(), file=sys.stderr)
    if not args.quiet:
        print(json.dumps(summary.__dict__))
    return summary.exit_code()


if __name__ == "__main__":
    sys.exit(main())
