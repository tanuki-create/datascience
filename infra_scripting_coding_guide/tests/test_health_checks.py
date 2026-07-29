"""samples/python/14_health_checks.py の単体テスト。

第14章 14.15。重複排除とリファクタリング後の check_service、
および後方互換のための非推奨ラッパーが、警告を出しつつ従来どおりの
結果を返すことを確認する。
"""
from __future__ import annotations

import pytest


@pytest.fixture
def health_checks(load_sample):
    return load_sample("14_health_checks.py")


class _FakeCompletedProcess:
    def __init__(self, returncode: int) -> None:
        self.returncode = returncode


@pytest.mark.parametrize(
    ("service", "expected_timeout"),
    [("web", 5), ("db", 10), ("cache", 3), ("unknown-service", 5)],
)
def test_check_service_resolves_timeout_by_service(
    health_checks, monkeypatch: pytest.MonkeyPatch, service: str, expected_timeout: int
) -> None:
    captured: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["timeout"] = kwargs.get("timeout")
        return _FakeCompletedProcess(returncode=0)

    monkeypatch.setattr(health_checks.subprocess, "run", fake_run)

    result = health_checks.check_service("web01.example.invalid", service)

    assert result.ok is True
    assert result.timeout_seconds == expected_timeout
    assert "--max-time" in captured["cmd"]
    assert str(expected_timeout) in captured["cmd"]


def test_check_service_explicit_timeout_overrides_default(
    health_checks, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        health_checks.subprocess, "run", lambda *a, **k: _FakeCompletedProcess(returncode=0)
    )
    result = health_checks.check_service("web01.example.invalid", "web", timeout_seconds=99)
    assert result.timeout_seconds == 99


def test_check_service_returns_false_on_nonzero_exit(
    health_checks, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        health_checks.subprocess, "run", lambda *a, **k: _FakeCompletedProcess(returncode=7)
    )
    result = health_checks.check_service("web02.example.invalid", "web")
    assert result.ok is False


@pytest.mark.parametrize(
    "deprecated_func_name",
    ["check_web", "check_db", "check_cache"],
)
def test_deprecated_wrappers_still_work_but_warn(
    health_checks, monkeypatch: pytest.MonkeyPatch, deprecated_func_name: str
) -> None:
    monkeypatch.setattr(
        health_checks.subprocess, "run", lambda *a, **k: _FakeCompletedProcess(returncode=0)
    )
    deprecated_func = getattr(health_checks, deprecated_func_name)

    with pytest.warns(DeprecationWarning):
        result = deprecated_func("web01.example.invalid")

    assert result is True
