#!/usr/bin/env python3
"""サービスのヘルスチェックを行う共通モジュール。

旧来は check_web/check_db/check_cache が個別に重複した実装を持っていた。
本モジュールでは check_service に統合し、旧関数は後方互換のための
非推奨ラッパーとして残す(第14章 14.4, 14.8参照)。
"""
from __future__ import annotations

import logging
import subprocess
import warnings
from dataclasses import dataclass

# サービスごとの既定タイムアウト(秒)。
# web: フロントは応答性が重要なため短め。
# db: 接続確立に時間がかかることがあるため長め。
# cache: 応答が速いことが前提のミドルウェアのため最短。
DEFAULT_TIMEOUT_SECONDS: dict[str, int] = {
    "web": 5,
    "db": 10,
    "cache": 3,
}
FALLBACK_TIMEOUT_SECONDS = 5
CURL_EXTRA_TIMEOUT_MARGIN_SECONDS = 2

logger = logging.getLogger("health_checks")


@dataclass
class HealthCheckResult:
    host: str
    service: str
    ok: bool
    timeout_seconds: int


def check_service(host: str, service: str, *, timeout_seconds: int | None = None) -> HealthCheckResult:
    """統合されたヘルスチェック関数。

    timeout_seconds を省略すると、service名に応じた既定値
    (DEFAULT_TIMEOUT_SECONDS)を使う。未知のservice名は
    FALLBACK_TIMEOUT_SECONDS を使う。
    """
    resolved_timeout = (
        timeout_seconds
        if timeout_seconds is not None
        else DEFAULT_TIMEOUT_SECONDS.get(service, FALLBACK_TIMEOUT_SECONDS)
    )
    result = subprocess.run(
        ["curl", "-sf", "--max-time", str(resolved_timeout), f"http://{host}/health"],
        capture_output=True,
        timeout=resolved_timeout + CURL_EXTRA_TIMEOUT_MARGIN_SECONDS,
        check=False,
    )
    return HealthCheckResult(host=host, service=service, ok=result.returncode == 0, timeout_seconds=resolved_timeout)


def check_web(host: str) -> bool:
    """非推奨。check_service(host, "web") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_web is deprecated; use check_service(host, "web") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "web").ok


def check_db(host: str) -> bool:
    """非推奨。check_service(host, "db") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_db is deprecated; use check_service(host, "db") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "db").ok


def check_cache(host: str) -> bool:
    """非推奨。check_service(host, "cache") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_cache is deprecated; use check_service(host, "cache") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "cache").ok
