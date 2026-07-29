#!/usr/bin/env python3
"""opsctl: 第15章の全サブコマンドを束ねる統合ディスパッチャ（学習用）。

各サブコマンドは、本章で個別に実装・テストした独立スクリプト
（samples/python, samples/bash, samples/powershell）を子プロセスとして
呼び出す。実運用のCLIでは、第12章のスケルトンのように argparse の
サブパーサーへ直接ロジックを実装するほうが、引数のヘルプやエラー
メッセージが一貫し好ましい。本スクリプトは、独立に動作確認した
スクリプト群を1つの入口へ束ねる設計（ファサード）を示す教材である。

実行例:
    python3 samples/python/15_opsctl_dispatch.py ping-check --dry-run
    python3 samples/python/15_opsctl_dispatch.py disk-check --dry-run --paths /
"""
from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable


def _python_script(name: str) -> list[str]:
    return [PYTHON, str(REPO_ROOT / "samples" / "python" / name)]


def _bash_script(name: str) -> list[str]:
    return ["bash", str(REPO_ROOT / "samples" / "bash" / name)]


def _pwsh_script(name: str) -> list[str]:
    return ["pwsh", str(REPO_ROOT / "samples" / "powershell" / name)]


def _is_windows() -> bool:
    return platform.system() == "Windows"


# サブコマンド名 -> 実行コマンドを組み立てる関数。
# disk-check / service-check はOSにより実装言語を切り替える。
# backup はLinux/macOSではBash、WindowsではPython実装を使う。
SUBCOMMANDS: dict[str, Callable[[], list[str]]] = {
    "ping-check": lambda: _python_script("15_ping_check.py"),
    "disk-check": lambda: _pwsh_script("15_disk_check.ps1") if _is_windows() else _bash_script("15_disk_check.sh"),
    "log-search": lambda: _python_script("15_log_search.py"),
    "cleanup-old": lambda: _python_script("15_cleanup_old.py"),
    "user-audit": lambda: _pwsh_script("15_user_audit.ps1"),
    "service-check": lambda: (
        _pwsh_script("15_service_check.ps1") if _is_windows() else _bash_script("15_service_check.sh")
    ),
    "config-patch": lambda: _python_script("15_config_patch.py"),
    "api-export": lambda: _python_script("15_api_export.py"),
    "backup": lambda: _python_script("15_backup.py") if _is_windows() else _bash_script("15_backup.sh"),
    "cert-check": lambda: _python_script("15_cert_check.py"),
    "report": lambda: _python_script("15_report.py"),
}


def build_command(subcommand: str, extra_args: list[str]) -> list[str]:
    if subcommand not in SUBCOMMANDS:
        raise KeyError(subcommand)
    return SUBCOMMANDS[subcommand]() + extra_args


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="opsctl",
        description="opsctl: dispatch chapter 15 subcommands to their language-specific implementation",
        add_help=False,
    )
    parser.add_argument("subcommand", choices=sorted(SUBCOMMANDS), nargs="?")
    args, remaining = parser.parse_known_args(argv)

    if args.subcommand is None:
        print("usage: opsctl <subcommand> [options...]", file=sys.stderr)
        print("subcommands: " + ", ".join(sorted(SUBCOMMANDS)), file=sys.stderr)
        return 1

    command = build_command(args.subcommand, remaining)
    print(f"+ {' '.join(command)}", file=sys.stderr)
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
