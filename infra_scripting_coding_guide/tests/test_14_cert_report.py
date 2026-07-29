"""第14章のテスト例: 責務ごとに分割した証明書チェックロジックの検証。

実行方法:

    cd infra_scripting_coding_guide
    pytest tests/test_14_cert_report.py -v
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from conftest import load_sample_module

cert_report = load_sample_module("14_cert_report.py")

CertificateInfo = cert_report.CertificateInfo
parse_not_after = cert_report.parse_not_after
compute_days_remaining = cert_report.compute_days_remaining
classify_certificate = cert_report.classify_certificate
build_status = cert_report.build_status
format_report_line = cert_report.format_report_line
build_report = cert_report.build_report
worst_status = cert_report.worst_status
fetch_certificate_info = cert_report.fetch_certificate_info
main = cert_report.main


def test_parse_not_after_parses_openssl_format() -> None:
    parsed = parse_not_after("Jan  1 00:00:00 2030 GMT")
    assert parsed == datetime(2030, 1, 1, tzinfo=timezone.utc)


def test_compute_days_remaining_with_fixed_now() -> None:
    not_after = datetime(2030, 1, 31, tzinfo=timezone.utc)
    now = datetime(2030, 1, 1, tzinfo=timezone.utc)
    assert compute_days_remaining(not_after, now=now) == 30


@pytest.mark.parametrize(
    ("days_remaining", "expected"),
    [
        (31, "ok"),
        (30, "warning"),  # warn_daysちょうどはwarning
        (8, "warning"),
        (7, "critical"),  # crit_daysちょうどはcritical
        (0, "critical"),
        (-5, "critical"),  # 期限切れ済みもcritical
    ],
)
def test_classify_certificate_boundaries(days_remaining: int, expected: str) -> None:
    assert classify_certificate(days_remaining, warn_days=30, crit_days=7) == expected


def test_classify_certificate_rejects_inverted_thresholds() -> None:
    with pytest.raises(ValueError, match="must be >="):
        classify_certificate(10, warn_days=7, crit_days=30)


def test_build_status_combines_parsing_and_classification() -> None:
    info = CertificateInfo(host="web01.example.invalid", not_after=datetime(2030, 1, 8, tzinfo=timezone.utc))
    now = datetime(2030, 1, 1, tzinfo=timezone.utc)
    status = build_status(info, warn_days=30, crit_days=7, now=now)
    assert status.host == "web01.example.invalid"
    assert status.days_remaining == 7
    assert status.status == "critical"


def test_format_report_line_contains_all_fields() -> None:
    status = cert_report.CertificateStatus(host="a.example.invalid", days_remaining=5, status="critical")
    line = format_report_line(status)
    assert "host=a.example.invalid" in line
    assert "days_remaining=5" in line
    assert "status=critical" in line


def test_build_report_joins_multiple_lines() -> None:
    statuses = [
        cert_report.CertificateStatus(host="a.example.invalid", days_remaining=100, status="ok"),
        cert_report.CertificateStatus(host="b.example.invalid", days_remaining=3, status="critical"),
    ]
    report = build_report(statuses)
    assert report.count("\n") == 1
    assert "a.example.invalid" in report
    assert "b.example.invalid" in report


def test_worst_status_picks_highest_severity() -> None:
    statuses = [
        cert_report.CertificateStatus(host="a.example.invalid", days_remaining=100, status="ok"),
        cert_report.CertificateStatus(host="b.example.invalid", days_remaining=20, status="warning"),
        cert_report.CertificateStatus(host="c.example.invalid", days_remaining=3, status="critical"),
    ]
    assert worst_status(statuses) == "critical"


def test_worst_status_empty_list_is_ok() -> None:
    assert worst_status([]) == "ok"


# --- モック: ネットワークI/Oを分離してmain()を検証する -----------------------


def test_main_reports_critical_with_mocked_fetch(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fake_fetch(host: str, port: int = 443, timeout: int = 10) -> CertificateInfo:
        assert host == "web01.example.invalid"
        return CertificateInfo(host=host, not_after=datetime(2030, 1, 3, tzinfo=timezone.utc))

    fixed_now = datetime(2030, 1, 1, tzinfo=timezone.utc)
    monkeypatch.setattr(cert_report, "fetch_certificate_info", fake_fetch)
    monkeypatch.setattr(
        cert_report,
        "build_status",
        lambda info, warn_days, crit_days: build_status(info, warn_days, crit_days, now=fixed_now),
    )

    exit_code = main(["web01.example.invalid", "--warn-days", "30", "--crit-days", "7"])

    assert exit_code == cert_report.EXIT_CRITICAL
    out = capsys.readouterr().out
    assert "host=web01.example.invalid" in out
    assert "status=critical" in out


def test_main_returns_usage_error_on_inverted_thresholds(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(host: str, port: int = 443, timeout: int = 10) -> CertificateInfo:
        return CertificateInfo(host=host, not_after=datetime(2030, 1, 1, tzinfo=timezone.utc))

    monkeypatch.setattr(cert_report, "fetch_certificate_info", fake_fetch)

    exit_code = main(["web01.example.invalid", "--warn-days", "7", "--crit-days", "30"])

    assert exit_code == cert_report.EXIT_USAGE


def test_main_returns_runtime_error_when_fetch_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(host: str, port: int = 443, timeout: int = 10) -> CertificateInfo:
        raise OSError("connection refused")

    monkeypatch.setattr(cert_report, "fetch_certificate_info", fake_fetch)

    exit_code = main(["unreachable.example.invalid"])

    assert exit_code == cert_report.EXIT_RUNTIME
