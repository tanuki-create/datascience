"""第13章のテスト例: ユニット、境界値、モック、結合、CLIテストを一通り含む。

実行方法:

    cd infra_scripting_coding_guide
    pytest tests/test_13_disk_classifier.py -v
"""
from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

import pytest

from conftest import load_sample_module

disk_classifier = load_sample_module("13_disk_classifier.py")

DiskUsage = disk_classifier.DiskUsage
InvalidThresholdError = disk_classifier.InvalidThresholdError
classify_disk_usage = disk_classifier.classify_disk_usage
classify_all = disk_classifier.classify_all
parse_df_output = disk_classifier.parse_df_output
fetch_disk_report = disk_classifier.fetch_disk_report
main = disk_classifier.main

SAMPLE_DF_OUTPUT = """Filesystem     1024-blocks     Used Available Capacity Mounted on
/dev/sda1         51475068 42787876   6045808      88% /
/dev/sda2        104845292 34567890  65432100      35% /var
/dev/sda3         20971520 19951616    524288      98% /data
"""


# --- ユニットテスト: 正常系 ---------------------------------------------


def test_classify_disk_usage_ok() -> None:
    assert classify_disk_usage(50.0, warn_percent=80.0, crit_percent=90.0) == "ok"


def test_classify_disk_usage_warning() -> None:
    assert classify_disk_usage(85.0, warn_percent=80.0, crit_percent=90.0) == "warning"


def test_classify_disk_usage_critical() -> None:
    assert classify_disk_usage(95.0, warn_percent=80.0, crit_percent=90.0) == "critical"


# --- 境界値テスト ---------------------------------------------------------


@pytest.mark.parametrize(
    ("used_percent", "expected"),
    [
        (79.9, "ok"),
        (80.0, "warning"),  # warn_percentちょうどはwarning
        (89.9, "warning"),
        (90.0, "critical"),  # crit_percentちょうどはcritical
        (100.0, "critical"),  # 上限
        (0.0, "ok"),  # 下限
    ],
)
def test_classify_disk_usage_boundaries(used_percent: float, expected: str) -> None:
    assert classify_disk_usage(used_percent, warn_percent=80.0, crit_percent=90.0) == expected


# --- 異常系テスト ---------------------------------------------------------


def test_classify_disk_usage_rejects_inverted_thresholds() -> None:
    with pytest.raises(InvalidThresholdError):
        classify_disk_usage(85.0, warn_percent=90.0, crit_percent=80.0)


@pytest.mark.parametrize("used_percent", [-1.0, 100.1, 200.0])
def test_classify_disk_usage_rejects_out_of_range(used_percent: float) -> None:
    with pytest.raises(ValueError):
        classify_disk_usage(used_percent, warn_percent=80.0, crit_percent=90.0)


# --- テストデータを使ったパーステスト -------------------------------------


def test_parse_df_output_parses_all_lines() -> None:
    usages = parse_df_output(SAMPLE_DF_OUTPUT)
    assert usages == [
        DiskUsage(mount_point="/", used_percent=88.0),
        DiskUsage(mount_point="/var", used_percent=35.0),
        DiskUsage(mount_point="/data", used_percent=98.0),
    ]


def test_parse_df_output_skips_malformed_line(caplog: pytest.LogCaptureFixture) -> None:
    text = "Filesystem 1024-blocks Used Available Capacity Mounted-on\nbroken line\n"
    with caplog.at_level(logging.WARNING, logger="opsctl.disk_classifier"):
        usages = parse_df_output(text)
    assert usages == []
    assert "malformed" in caplog.text


def test_parse_df_output_empty_input_returns_empty_list() -> None:
    assert parse_df_output("") == []


# --- classify_all: 複数件から最悪ステータスを求める ------------------------


def test_classify_all_returns_worst_status() -> None:
    usages = parse_df_output(SAMPLE_DF_OUTPUT)
    results, worst = classify_all(usages, warn_percent=80.0, crit_percent=90.0)
    assert worst == "critical"
    assert [r.status for r in results] == ["warning", "ok", "critical"]


# --- モック: 外部プロセス呼び出しを差し替える結合テスト ---------------------


def test_fetch_disk_report_mocks_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    """subprocess.run をモックし、実際のsshを使わずにfetch_disk_reportを検証する。"""

    def fake_run(cmd, **kwargs):  # noqa: ANN001, ANN003 - テスト用の簡略シグネチャ
        assert cmd == ["ssh", "web01.example.invalid", "df", "-P"]
        assert kwargs.get("timeout") == 5
        return subprocess.CompletedProcess(cmd, returncode=0, stdout=SAMPLE_DF_OUTPUT, stderr="")

    monkeypatch.setattr(disk_classifier.subprocess, "run", fake_run)

    usages = fetch_disk_report("web01.example.invalid", timeout=5)
    assert len(usages) == 3
    assert usages[0].mount_point == "/"


def test_fetch_disk_report_raises_on_nonzero_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):  # noqa: ANN001, ANN003
        return subprocess.CompletedProcess(cmd, returncode=255, stdout="", stderr="ssh: connection refused")

    monkeypatch.setattr(disk_classifier.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="connection refused"):
        fetch_disk_report("unreachable.example.invalid")


def test_fetch_disk_report_propagates_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):  # noqa: ANN001, ANN003
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=kwargs.get("timeout", 10))

    monkeypatch.setattr(disk_classifier.subprocess, "run", fake_run)

    with pytest.raises(subprocess.TimeoutExpired):
        fetch_disk_report("slow.example.invalid", timeout=3)


# --- CLI全体の結合テスト ---------------------------------------------------


def test_main_with_input_file_reports_critical(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    input_file = tmp_path / "df.txt"
    input_file.write_text(SAMPLE_DF_OUTPUT, encoding="utf-8")

    exit_code = main(["--input-file", str(input_file)])

    assert exit_code == disk_classifier.EXIT_CRITICAL
    payload = json.loads(capsys.readouterr().out)
    assert payload["worst"] == "critical"
    assert len(payload["results"]) == 3


def test_main_with_all_ok_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    text = (
        "Filesystem 1024-blocks Used Available Capacity Mounted-on\n"
        "/dev/sda1 100 10 90 10% /\n"
    )
    input_file = tmp_path / "df.txt"
    input_file.write_text(text, encoding="utf-8")

    exit_code = main(["--input-file", str(input_file)])

    assert exit_code == disk_classifier.EXIT_OK


def test_main_requires_host_or_input_file() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([])
    assert exc_info.value.code == 2  # argparseのエラー終了コード


def test_main_reports_usage_error_on_inverted_thresholds(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    input_file = tmp_path / "df.txt"
    input_file.write_text(SAMPLE_DF_OUTPUT, encoding="utf-8")

    exit_code = main(
        ["--input-file", str(input_file), "--warn-percent", "90", "--crit-percent", "80"]
    )

    assert exit_code == disk_classifier.EXIT_USAGE
