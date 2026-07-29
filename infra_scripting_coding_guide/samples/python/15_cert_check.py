#!/usr/bin/env python3
"""opsctl cert-check: TLS証明書の有効期限を確認する。

config/opsctl.yaml の cert_check.targets（host, port）を既定の対象にする。
--cert-file を指定すると、ネットワーク接続をせずローカルのPEM証明書
ファイルを openssl コマンドで検査できる。オフラインでのテストや
--dry-run の代替として使える。

対象ホストへ実際にTLS接続するため、ラボ環境で到達できないホストを
指定すると接続エラーになる。到達できないことは異常ではなく、
その旨をERRORとして報告する設計である。
"""
from __future__ import annotations

import argparse
import csv
import datetime
import logging
import socket
import ssl
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3

logger = logging.getLogger("opsctl.cert_check")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_WARN_DAYS = 30
DEFAULT_CRIT_DAYS = 7
DEFAULT_CONNECT_TIMEOUT = 10.0


@dataclass
class CertTarget:
    host: str
    port: int


@dataclass
class CertResult:
    target: str
    not_after: str
    days_remaining: int | None
    status: str
    detail: str = ""


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def parse_asn1_time(value: str) -> datetime.datetime:
    return datetime.datetime.strptime(value.strip(), "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=datetime.timezone.utc
    )


def fetch_remote_not_after(host: str, port: int, timeout: float) -> datetime.datetime:
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            cert = tls_sock.getpeercert()
    if not cert or "notAfter" not in cert:
        raise ValueError("certificate response did not include notAfter")
    return parse_asn1_time(cert["notAfter"])


def read_local_not_after(cert_file: Path) -> datetime.datetime:
    try:
        completed = subprocess.run(
            ["openssl", "x509", "-enddate", "-noout", "-in", str(cert_file)],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("openssl command not found") from exc
    if completed.returncode != 0:
        raise ValueError(f"openssl failed: {completed.stderr.strip()}")
    # 出力例: "notAfter=Jan  1 00:00:00 2030 GMT"
    _, _, value = completed.stdout.strip().partition("=")
    if not value:
        raise ValueError(f"unexpected openssl output: {completed.stdout!r}")
    return parse_asn1_time(value)


def classify(days_remaining: int, warn_days: int, crit_days: int) -> str:
    if days_remaining <= crit_days:
        return "CRITICAL"
    if days_remaining <= warn_days:
        return "WARNING"
    return "OK"


def check_target(
    label: str, get_not_after: Callable[[], datetime.datetime], *, warn_days: int, crit_days: int
) -> CertResult:
    try:
        not_after = get_not_after()
    except (OSError, ssl.SSLError, socket.timeout, ValueError, RuntimeError) as exc:
        logger.warning("failed to check %s: %s", label, exc)
        return CertResult(label, "", None, "ERROR", detail=str(exc))

    days_remaining = (not_after - datetime.datetime.now(datetime.timezone.utc)).days
    status = classify(days_remaining, warn_days, crit_days)
    return CertResult(label, not_after.isoformat(), days_remaining, status)


def write_report(path: Path, results: list[CertResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["target", "not_after", "days_remaining", "status", "detail"])
        writer.writeheader()
        for r in results:
            writer.writerow(
                {
                    "target": r.target,
                    "not_after": r.not_after,
                    "days_remaining": r.days_remaining if r.days_remaining is not None else "",
                    "status": r.status,
                    "detail": r.detail,
                }
            )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="opsctl cert-check: check TLS certificate expiry")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--host", action="append", default=None, help="host:port, can be repeated")
    parser.add_argument("--cert-file", type=Path, action="append", default=None, dest="cert_files")
    parser.add_argument("--warn-days", type=int, default=None)
    parser.add_argument("--crit-days", type=int, default=None)
    parser.add_argument("--timeout", type=float, default=DEFAULT_CONNECT_TIMEOUT)
    parser.add_argument("--report", type=Path, default=Path("work/reports/cert_check.csv"))
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

    cert_cfg = config.get("cert_check", {})
    warn_days = args.warn_days if args.warn_days is not None else int(cert_cfg.get("warn_days", DEFAULT_WARN_DAYS))
    crit_days = args.crit_days if args.crit_days is not None else int(cert_cfg.get("crit_days", DEFAULT_CRIT_DAYS))

    if warn_days < crit_days:
        logger.error("--warn-days must be >= --crit-days")
        return EXIT_USAGE

    targets: list[CertTarget] = []
    if args.host:
        for h in args.host:
            host, _, port_str = h.partition(":")
            targets.append(CertTarget(host, int(port_str) if port_str else 443))
    elif not args.cert_files:
        for t in cert_cfg.get("targets", []):
            targets.append(CertTarget(t["host"], int(t.get("port", 443))))

    cert_files = args.cert_files or []

    if not targets and not cert_files:
        logger.error("no targets: specify --host, --cert-file, or cert_check.targets in config")
        return EXIT_USAGE

    if args.dry_run:
        for t in targets:
            logger.info("dry-run: would check %s:%s", t.host, t.port)
        for f in cert_files:
            logger.info("dry-run: would check local cert file %s", f)
        return EXIT_OK

    results: list[CertResult] = []
    for t in targets:
        label = f"{t.host}:{t.port}"
        results.append(
            check_target(
                label,
                lambda t=t: fetch_remote_not_after(t.host, t.port, args.timeout),
                warn_days=warn_days,
                crit_days=crit_days,
            )
        )
    for f in cert_files:
        results.append(
            check_target(str(f), lambda f=f: read_local_not_after(f), warn_days=warn_days, crit_days=crit_days)
        )

    for r in results:
        logger.info("target=%s days_remaining=%s status=%s", r.target, r.days_remaining, r.status)

    write_report(args.report, results)
    logger.info("wrote report to %s", args.report)

    if any(r.status == "CRITICAL" for r in results):
        return EXIT_CRITICAL
    if any(r.status == "ERROR" for r in results):
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("interrupted by user")
        sys.exit(130)
