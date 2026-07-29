"""samples/python/04_classify_usage.py の単体テスト。

第13章 13.3 の正常系・異常系・境界値の三観点でテストケースを設計する。
"""
from __future__ import annotations

import pytest


@pytest.fixture
def classify_usage(load_sample):
    return load_sample("04_classify_usage.py")


# --- 正常系・境界値: classify() ---


@pytest.mark.parametrize(
    ("usage", "warn", "crit", "expected"),
    [
        (0.0, 80.0, 90.0, "OK"),  # 範囲の下端
        (50.0, 80.0, 90.0, "OK"),  # 正常系
        (79.9, 80.0, 90.0, "OK"),  # warnの直前
        (80.0, 80.0, 90.0, "WARNING"),  # 境界値: warnちょうど
        (85.0, 80.0, 90.0, "WARNING"),  # 正常系
        (89.9, 80.0, 90.0, "WARNING"),  # critの直前
        (90.0, 80.0, 90.0, "CRITICAL"),  # 境界値: critちょうど
        (100.0, 80.0, 90.0, "CRITICAL"),  # 範囲の上端
    ],
)
def test_classify_boundaries(classify_usage, usage: float, warn: float, crit: float, expected: str) -> None:
    assert classify_usage.classify(usage, warn, crit) == expected


def test_classify_allows_warn_equal_to_crit(classify_usage) -> None:
    # warn == crit は許容される(等号のみを禁止しているわけではない)
    assert classify_usage.classify(85.0, 80.0, 80.0) == "CRITICAL"
    assert classify_usage.classify(70.0, 80.0, 80.0) == "OK"


# --- 異常系: classify() ---


@pytest.mark.parametrize("usage", [-0.1, 100.1, -50.0, 200.0])
def test_classify_rejects_out_of_range_usage(classify_usage, usage: float) -> None:
    with pytest.raises(ValueError):
        classify_usage.classify(usage, 80.0, 90.0)


@pytest.mark.parametrize(
    ("warn", "crit"),
    [(-1.0, 90.0), (80.0, -1.0), (101.0, 90.0), (80.0, 101.0)],
)
def test_classify_rejects_out_of_range_thresholds(classify_usage, warn: float, crit: float) -> None:
    with pytest.raises(ValueError):
        classify_usage.classify(50.0, warn, crit)


def test_classify_rejects_warn_greater_than_crit(classify_usage) -> None:
    with pytest.raises(ValueError):
        classify_usage.classify(50.0, 90.0, 80.0)


# --- status_to_exit() ---


@pytest.mark.parametrize(
    ("status", "expected_code"),
    [("OK", 0), ("WARNING", 0), ("CRITICAL", 3)],
)
def test_status_to_exit(classify_usage, status: str, expected_code: int) -> None:
    assert classify_usage.status_to_exit(status) == expected_code


# --- main(): CLI全体の結合テスト ---


def test_main_prints_status_and_returns_exit_code(classify_usage, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = classify_usage.main(["--usage", "95", "--warn", "80", "--crit", "90"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "CRITICAL"
    assert exit_code == 3


def test_main_uses_default_thresholds(classify_usage, capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = classify_usage.main(["--usage", "50"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "OK"
    assert exit_code == 0


def test_main_rejects_invalid_usage_with_usage_exit_code(classify_usage) -> None:
    exit_code = classify_usage.main(["--usage", "150", "--warn", "80", "--crit", "90"])
    assert exit_code == 1


def test_main_requires_usage_argument(classify_usage) -> None:
    with pytest.raises(SystemExit):
        classify_usage.main([])
