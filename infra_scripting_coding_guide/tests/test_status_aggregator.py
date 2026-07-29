"""samples/python/13_status_aggregator.py の単体テストと結合テスト。

第13章 13.7 の三層構成(純粋関数のユニットテスト、副作用関数のモック、
I/Oを含む結合テスト)に対応する。
"""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def status_aggregator(load_sample):
    return load_sample("13_status_aggregator.py")


# 1. 純粋関数のユニットテスト: 正常系・異常系・境界値


@pytest.mark.parametrize(
    ("ping_ok", "disk_status", "expected"),
    [
        (True, "OK", "OK"),
        (True, "WARNING", "WARNING"),
        (False, "OK", "WARNING"),
        (True, "CRITICAL", "CRITICAL"),
        (False, "CRITICAL", "CRITICAL"),
        (False, "WARNING", "WARNING"),
    ],
)
def test_aggregate_status(status_aggregator, ping_ok: bool, disk_status: str, expected: str) -> None:
    assert status_aggregator.aggregate_status(ping_ok, disk_status) == expected


def test_aggregate_status_rejects_unknown_disk_status(status_aggregator) -> None:
    with pytest.raises(ValueError):
        status_aggregator.aggregate_status(True, "UNKNOWN")


# 2. 副作用関数のユニットテスト: 通知先を差し替える


def test_notify_if_critical_calls_notifier_only_when_critical(status_aggregator) -> None:
    calls: list[str] = []
    notified = status_aggregator.notify_if_critical(
        "web01.example.invalid", "CRITICAL", notifier=calls.append
    )
    assert notified is True
    assert calls == ["CRITICAL: web01.example.invalid requires attention"]


@pytest.mark.parametrize("overall", ["OK", "WARNING"])
def test_notify_if_critical_skips_non_critical(status_aggregator, overall: str) -> None:
    calls: list[str] = []
    notified = status_aggregator.notify_if_critical(
        "web01.example.invalid", overall, notifier=calls.append
    )
    assert notified is False
    assert calls == []


# 3. I/Oを含む結合テスト: tmp_path に実ファイルを作る


def test_load_and_aggregate_combines_reports(status_aggregator, tmp_path: Path) -> None:
    ping_report = tmp_path / "ping.csv"
    ping_report.write_text(
        "host,ok\nweb01.example.invalid,true\nweb02.example.invalid,false\n",
        encoding="utf-8",
    )
    disk_report = tmp_path / "disk.csv"
    disk_report.write_text(
        "host,status\nweb01.example.invalid,OK\nweb02.example.invalid,CRITICAL\n",
        encoding="utf-8",
    )

    statuses = status_aggregator.load_and_aggregate(ping_report, disk_report)

    by_host = {s.host: s.overall for s in statuses}
    assert by_host["web01.example.invalid"] == "OK"
    assert by_host["web02.example.invalid"] == "CRITICAL"


def test_load_and_aggregate_treats_missing_disk_entry_as_warning(status_aggregator, tmp_path: Path) -> None:
    ping_report = tmp_path / "ping.csv"
    ping_report.write_text("host,ok\nweb03.example.invalid,true\n", encoding="utf-8")
    disk_report = tmp_path / "disk.csv"
    disk_report.write_text("host,status\n", encoding="utf-8")

    statuses = status_aggregator.load_and_aggregate(ping_report, disk_report)

    assert len(statuses) == 1
    assert statuses[0].disk_status == "WARNING"
    assert statuses[0].overall == "WARNING"


def test_main_exits_critical_when_any_host_critical(status_aggregator, tmp_path: Path) -> None:
    ping_report = tmp_path / "ping.csv"
    ping_report.write_text("host,ok\nweb01.example.invalid,true\n", encoding="utf-8")
    disk_report = tmp_path / "disk.csv"
    disk_report.write_text("host,status\nweb01.example.invalid,CRITICAL\n", encoding="utf-8")

    exit_code = status_aggregator.main(
        ["--ping-report", str(ping_report), "--disk-report", str(disk_report)]
    )
    assert exit_code == status_aggregator.EXIT_CRITICAL


def test_main_returns_usage_error_when_report_missing(status_aggregator, tmp_path: Path) -> None:
    missing_report = tmp_path / "does_not_exist.csv"
    disk_report = tmp_path / "disk.csv"
    disk_report.write_text("host,status\n", encoding="utf-8")

    exit_code = status_aggregator.main(
        ["--ping-report", str(missing_report), "--disk-report", str(disk_report)]
    )
    assert exit_code == status_aggregator.EXIT_USAGE
