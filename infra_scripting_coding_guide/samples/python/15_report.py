#!/usr/bin/env python3
"""opsctl report: 各種チェック結果のCSVを集計し、定期レポートを生成する。

config/opsctl.yaml の report.sections（既定: ping, disk, cert）に対応する
CSVレポート（15_ping_check.py、15_disk_check.sh/.ps1、15_cert_check.py の
出力）を読み込み、Markdown形式のサマリーを書き出す。

このスクリプトはメール送信そのものは行わない。report.recipients は、
実際に配信する仕組み（社内のメールリレーやチャット通知）へ接続するための
設定値の置き場所として用意している。
"""
from __future__ import annotations

import argparse
import csv
import datetime
import logging
import sys
import uuid
from dataclasses import dataclass, field
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

logger = logging.getLogger("opsctl.report")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_REPORT_DIR = Path("work/reports")
DEFAULT_SECTIONS = ["ping", "disk", "cert"]

SECTION_FILES = {
    "ping": "ping_check.csv",
    "disk": "disk_check.csv",
    "cert": "cert_check.csv",
}


@dataclass
class SectionSummary:
    name: str
    source: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    error: int = 0
    missing: bool = False
    rows: list[dict[str, str]] = field(default_factory=list)

    def worst_status(self) -> str:
        if self.missing:
            return "UNKNOWN"
        if self.critical:
            return "CRITICAL"
        if self.error:
            return "ERROR"
        if self.warning:
            return "WARNING"
        return "OK"


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def summarize_ping(rows: list[dict[str, str]]) -> tuple[int, int, int, int]:
    ok = sum(1 for r in rows if r.get("ok") == "true")
    failed = len(rows) - ok
    # ping-check には WARNING の概念が無いため、失敗はCRITICAL枠に計上する。
    return len(rows), ok, 0, failed


def summarize_status_column(rows: list[dict[str, str]]) -> tuple[int, int, int, int]:
    ok = sum(1 for r in rows if r.get("status") == "OK")
    warning = sum(1 for r in rows if r.get("status") == "WARNING")
    critical = sum(1 for r in rows if r.get("status") == "CRITICAL")
    return len(rows), ok, warning, critical


def load_section(name: str, report_dir: Path) -> SectionSummary:
    filename = SECTION_FILES.get(name)
    if filename is None:
        raise ValueError(f"unknown report section: {name}")
    source = report_dir / filename
    if not source.is_file():
        logger.warning("report source not found for section=%s: %s", name, source)
        return SectionSummary(name=name, source=str(source), missing=True)

    with source.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if name == "ping":
        total, ok, warning, critical = summarize_ping(rows)
        error = 0
    else:
        total, ok, warning, critical = summarize_status_column(rows)
        error = sum(1 for r in rows if r.get("status") == "ERROR")

    return SectionSummary(
        name=name, source=str(source), total=total, ok=ok, warning=warning, critical=critical, error=error, rows=rows
    )


def render_markdown(run_id: str, generated_at: str, sections: list[SectionSummary]) -> str:
    lines = ["# opsctl 定期レポート", "", f"- run_id: {run_id}", f"- generated_at: {generated_at}", ""]
    lines.append("| セクション | 状態 | 件数 | OK | WARNING | CRITICAL | ERROR |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in sections:
        if s.missing:
            lines.append(f"| {s.name} | UNKNOWN | - | - | - | - | - |")
            continue
        lines.append(f"| {s.name} | {s.worst_status()} | {s.total} | {s.ok} | {s.warning} | {s.critical} | {s.error} |")
    lines.append("")

    for s in sections:
        if s.missing or not s.rows:
            continue
        problem_rows = [r for r in s.rows if r.get("status") not in (None, "OK") and r.get("ok") != "true"]
        if not problem_rows:
            continue
        lines.append(f"## {s.name}: 要確認の項目")
        lines.append("")
        for r in problem_rows[:20]:
            lines.append(f"- {dict(r)}")
        lines.append("")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl report: aggregate check results into a summary report")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--report-dir", type=Path, default=None)
    parser.add_argument("--section", action="append", default=None, dest="sections")
    parser.add_argument("--output", type=Path, default=Path("work/reports/summary.md"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    report_cfg = config.get("report", {})
    report_dir = args.report_dir or Path(config.get("paths", {}).get("report_dir", DEFAULT_REPORT_DIR))
    sections_wanted = args.sections or report_cfg.get("sections", DEFAULT_SECTIONS)
    recipients = report_cfg.get("recipients", [])

    run_id = str(uuid.uuid4())
    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    sections: list[SectionSummary] = []
    had_missing = False
    for name in sections_wanted:
        try:
            summary = load_section(name, report_dir)
        except ValueError as exc:
            logger.error("%s", exc)
            return EXIT_USAGE
        sections.append(summary)
        had_missing = had_missing or summary.missing

    markdown = render_markdown(run_id, generated_at, sections)

    if args.dry_run:
        logger.info("dry-run: would write report to %s (recipients=%s)", args.output, recipients)
        logger.debug("dry-run report preview:\n%s", markdown)
        return EXIT_OK

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    logger.info("wrote report to %s (run_id=%s)", args.output, run_id)

    if recipients:
        logger.info(
            "recipients configured (%s) but this script does not send email; "
            "connect it to your mail relay or chat webhook if notification is required",
            ", ".join(recipients),
        )

    if any(s.critical > 0 for s in sections):
        return EXIT_CRITICAL
    if had_missing or any(s.error > 0 for s in sections):
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
