#!/usr/bin/env python3
"""証明書の有効期限を確認し、レポートを作成する（第14章: 保守しやすいコードの例）。

opsctl の `cert-check` サブコマンド相当の処理を、責務ごとに小さな関数へ分割し、
マジックナンバーを設定値（既定値定数、CLI引数）として外出しした構成にしてある。
"""
from __future__ import annotations

import argparse
import socket
import ssl
import sys
from dataclasses import dataclass
from datetime import datetime, timezone

DEFAULT_WARN_DAYS = 30
DEFAULT_CRIT_DAYS = 7
DEFAULT_PORT = 443
DEFAULT_TIMEOUT_SECONDS = 10

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3


@dataclass
class CertificateInfo:
    host: str
    not_after: datetime


@dataclass
class CertificateStatus:
    host: str
    days_remaining: int
    status: str


def parse_not_after(not_after_text: str) -> datetime:
    """OpenSSLの``notAfter``形式（例: ``'Jan  1 00:00:00 2030 GMT'``）をdatetimeへ変換する。"""
    parsed = datetime.strptime(not_after_text, "%b %d %H:%M:%S %Y %Z")
    return parsed.replace(tzinfo=timezone.utc)


def fetch_certificate_info(
    host: str, port: int = DEFAULT_PORT, timeout: int = DEFAULT_TIMEOUT_SECONDS
) -> CertificateInfo:
    """TLSハンドシェイクを行い、サーバー証明書の失効日時を取得する。

    ネットワークI/Oをこの関数だけに閉じ込めることで、以降の計算ロジックを
    ネットワークなしでテストできる（第13章のモックの考え方と同じ）。
    """
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            cert = tls_sock.getpeercert()

    not_after_text = cert.get("notAfter") if cert else None
    if not isinstance(not_after_text, str) or not not_after_text:
        raise RuntimeError(f"certificate for {host} has no notAfter field")
    return CertificateInfo(host=host, not_after=parse_not_after(not_after_text))


def compute_days_remaining(not_after: datetime, *, now: datetime | None = None) -> int:
    """有効期限までの残り日数を計算する（切り捨て）。"""
    reference = now if now is not None else datetime.now(timezone.utc)
    delta = not_after - reference
    return delta.days


def classify_certificate(days_remaining: int, warn_days: int, crit_days: int) -> str:
    """残り日数を ``ok``/``warning``/``critical`` に分類する。"""
    if warn_days < crit_days:
        raise ValueError(f"warn_days ({warn_days}) must be >= crit_days ({crit_days})")
    if days_remaining <= crit_days:
        return "critical"
    if days_remaining <= warn_days:
        return "warning"
    return "ok"


def build_status(
    info: CertificateInfo,
    warn_days: int,
    crit_days: int,
    *,
    now: datetime | None = None,
) -> CertificateStatus:
    days_remaining = compute_days_remaining(info.not_after, now=now)
    status = classify_certificate(days_remaining, warn_days, crit_days)
    return CertificateStatus(host=info.host, days_remaining=days_remaining, status=status)


def format_report_line(status: CertificateStatus) -> str:
    return f"host={status.host} days_remaining={status.days_remaining} status={status.status}"


def build_report(statuses: list[CertificateStatus]) -> str:
    return "\n".join(format_report_line(status) for status in statuses)


def worst_status(statuses: list[CertificateStatus]) -> str:
    severity = {"ok": 0, "warning": 1, "critical": 2}
    worst = "ok"
    for status in statuses:
        if severity[status.status] > severity[worst]:
            worst = status.status
    return worst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cert_report", description="Check TLS certificate expiry for hosts")
    parser.add_argument("hosts", nargs="+", help="hostnames to check")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"default: {DEFAULT_PORT}")
    parser.add_argument("--warn-days", type=int, default=DEFAULT_WARN_DAYS, help=f"default: {DEFAULT_WARN_DAYS}")
    parser.add_argument("--crit-days", type=int, default=DEFAULT_CRIT_DAYS, help=f"default: {DEFAULT_CRIT_DAYS}")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help=f"default: {DEFAULT_TIMEOUT_SECONDS}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    try:
        statuses = [
            build_status(
                fetch_certificate_info(host, port=args.port, timeout=args.timeout),
                args.warn_days,
                args.crit_days,
            )
            for host in args.hosts
        ]
    except ValueError as exc:
        print(f"invalid arguments: {exc}", file=sys.stderr)
        return EXIT_USAGE
    except (OSError, ssl.SSLError) as exc:
        print(f"failed to fetch certificate: {exc}", file=sys.stderr)
        return EXIT_RUNTIME

    print(build_report(statuses))
    return EXIT_CRITICAL if worst_status(statuses) == "critical" else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
