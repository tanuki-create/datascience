# 第12章 設定ファイルとCLIツール

## 学習目標

- 設定とコードを分離し、JSON/YAML/TOML/環境変数の使い分けを説明できる
- 引数、ヘルプ、サブコマンド、デフォルト値、優先順位を備えたCLIを設計できる
- 終了コード、dry-run、verbose、quietの一貫した扱いを実装できる
- 実行結果サマリーを出力し、`opsctl` のCLI設計へ接続できる

前提: 第1章（引数、終了コード）、第9章（ログ）、第10章（秘密情報）。

サンプルコードは学習用である。
本番のCLIでは、対象組織の運用ルール（承認フロー、変更管理番号の必須化など）に合わせて拡張すること。

---

## 12.1 基本概念

**設定とコードの分離**は、実行のたびに変わりうる値（閾値、対象ホスト、出力先）をコード本体から切り離し、外部ファイルや引数で与える設計である。

分離しないと、環境ごとにソースコードを書き換える運用になり、変更履歴とコードの変更履歴が混ざる。

`opsctl` は、コード（サブコマンドの実装）と設定（`config/opsctl.yaml`）を分離し、実行のたびに引数と環境変数で上書きできる構成にする。

---

## 12.2 設定形式の比較

| 形式 | 長所 | 短所 | 向く用途 |
|------|------|------|----------|
| JSON | 言語間で扱いやすい。パーサーが標準的 | コメントが書けない | API連携、機械生成の設定 |
| YAML | 人が読み書きしやすい。コメント可 | インデント依存、暗黙型変換の罠がある（第3章） | 人が編集する運用設定 |
| TOML | 型が明確。セクション構造が読みやすい | Bash/PowerShellでの標準サポートが薄い | Python中心のツール設定（`pyproject.toml`など） |
| 環境変数 | 秘密情報や実行環境ごとの値に向く | 構造化データには不向き。一覧性が低い | 秘密情報、実行環境の切り替えフラグ |

`opsctl` は、階層的な既定値をYAML、秘密情報を環境変数、単発の上書きをCLI引数に割り当てる。

---

## 12.3 優先順位

複数の設定源がある場合、値が競合したときの優先順位を先に決める。
`opsctl` は次の順で解決する（上ほど優先度が高い）。

1. コマンドライン引数
2. 環境変数
3. 設定ファイル（`config/opsctl.yaml`）
4. コード内蔵のデフォルト値

```python
def resolve_timeout(cli_value: int | None, config: dict) -> int:
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get("OPSCTL_TIMEOUT_SECONDS")
    if env_value:
        return int(env_value)
    configured = config.get("defaults", {}).get("timeout_seconds")
    if configured is not None:
        return int(configured)
    return DEFAULT_TIMEOUT_SECONDS
```

優先順位を決めていないと、「設定ファイルを直したのに反映されない」という調査に時間を取られる。
CLIのヘルプや `--verbose` ログに、実際に採用した値の出所を残すと調査が速くなる。

---

## 12.4 最小構成のCLI

Python（`argparse`）:

```python
#!/usr/bin/env python3
import argparse
import sys


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal CLI example")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    print(f"timeout={args.timeout} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash（`getopts` は長いオプションを扱いにくいため、第1章と同じ手書きパーサーを使う）:

```bash
#!/usr/bin/env bash
set -euo pipefail

timeout=30
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timeout) timeout="${2:-}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help)
      echo "Usage: $0 [--timeout SECONDS] [--dry-run]" >&2
      exit 0
      ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

echo "timeout=${timeout} dry_run=${dry_run}"
```

PowerShell（`param()` は標準でヘルプと型検証を持つ）:

```powershell
#!/usr/bin/env pwsh
param(
    [int]$Timeout = 30,
    [switch]$DryRun
)

Write-Output "timeout=$Timeout dry_run=$($DryRun.IsPresent)"
```

---

## 12.5 サブコマンド設計

**サブコマンド**は、1つのCLIの中に複数の操作を持たせ、`ツール名 サブコマンド名 [オプション]` の形で呼び出す構成である。

Python（`argparse` のサブパーサー）:

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opsctl")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    ping_parser = subparsers.add_parser("ping-check", help="check connectivity to hosts")
    ping_parser.add_argument("--hosts-file", type=Path, default=None)

    subparsers.add_parser("disk-check", help="check disk usage thresholds")
    return parser
```

サブコマンドごとに固有のオプションを持たせつつ、`--config`、`--dry-run`、`--verbose`、`--quiet` のような共通オプションは親パーサーに置く。

---

## 12.6 ヘルプとデフォルト値の提示

利用者が `--help` を見ただけで既定値を判断できるように、ヘルプ文字列へデフォルト値を含める。

```python
parser.add_argument(
    "--timeout",
    type=int,
    default=30,
    help="request timeout in seconds (default: 30)",
)
```

Bashでは、`usage()` 関数に既定値を明記する。

```bash
usage() {
  cat <<'EOF' >&2
Usage: opsctl.sh ping-check [--timeout SECONDS] [--dry-run]
  --timeout SECONDS   default: 30
  --dry-run           show planned actions without making changes
EOF
}
```

---

## 12.7 dry-run、verbose、quietの実装

三つの共通オプションは、`opsctl` の全サブコマンドで意味を統一する。

| オプション | 効果 |
|------------|------|
| `--dry-run` | 変更を伴う操作を実行せず、実行予定だけをログとサマリーに出す |
| `--verbose` | DEBUGレベルまでログを出す（第9章） |
| `--quiet` | WARNING以上のみ出す |

```python
if args.verbose and args.quiet:
    parser.error("--verbose and --quiet are mutually exclusive")
```

`--dry-run` は、読み取り専用の処理では実質的に通常実行と同じ結果になってよい。
書き込み・削除・外部への変更APIを呼ぶ処理では、必ず実行前に分岐させる。

```python
if args.dry_run:
    logger.info("dry-run: would delete %s", target_path)
else:
    target_path.unlink()
```

---

## 12.8 終了コードと実行結果サマリー

`opsctl` 共通の終了コード（README参照）を、CLIスケルトンでも一貫して使う。

| コード | 意味 |
|--------|------|
| 0 | 成功（警告なし） |
| 1 | 使い方誤り、設定誤り |
| 2 | 実行時エラー（一部失敗を含む） |
| 3 | 閾値超過などのCRITICAL |
| 4 | タイムアウト |
| 130 | ユーザーによる中断 |

**実行結果サマリー**は、対象件数・成功件数・警告件数・失敗件数を1行にまとめた出力である。
終了コードだけでは「何件中何件失敗したか」が分からないため、ログの最後に必ず出す。

```python
@dataclass
class RunSummary:
    subcommand: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    failed: int = 0

    def exit_code(self) -> int:
        if self.critical:
            return EXIT_CRITICAL
        if self.failed:
            return EXIT_RUNTIME
        return EXIT_OK

    def render(self) -> str:
        return (
            f"summary subcommand={self.subcommand} total={self.total} "
            f"ok={self.ok} warning={self.warning} critical={self.critical} failed={self.failed}"
        )
```

---

## 12.9 実務向け改善: opsctl CLIスケルトン

`samples/python/12_opsctl_cli.py` に、設定読み込み、優先順位解決、サブコマンド、dry-run、サマリー出力をまとめたスケルトンを置く。

```python
#!/usr/bin/env python3
"""opsctlのCLIスケルトン: 設定優先順位、サブコマンド、dry-run、サマリー出力。

ping-check と disk-check は説明用の簡略実装であり、実際の疎通確認や
ディスク使用率取得は第15章で実装する。
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
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
EXIT_TIMEOUT = 4

logger = logging.getLogger("opsctl")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_TIMEOUT_SECONDS = 30


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def resolve_timeout(cli_value: int | None, config: dict[str, Any]) -> int:
    """CLI引数 > 環境変数 > 設定ファイル > デフォルトの順で解決する。"""
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get("OPSCTL_TIMEOUT_SECONDS")
    if env_value:
        return int(env_value)
    configured = config.get("defaults", {}).get("timeout_seconds")
    if configured is not None:
        return int(configured)
    return DEFAULT_TIMEOUT_SECONDS


@dataclass
class RunSummary:
    subcommand: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    failed: int = 0

    def exit_code(self) -> int:
        if self.critical:
            return EXIT_CRITICAL
        if self.failed:
            return EXIT_RUNTIME
        return EXIT_OK

    def render(self) -> str:
        return (
            f"summary subcommand={self.subcommand} total={self.total} "
            f"ok={self.ok} warning={self.warning} critical={self.critical} failed={self.failed}"
        )


def configure_logging(*, verbose: bool, quiet: bool) -> None:
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)


def run_ping_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    timeout = resolve_timeout(args.timeout, config)
    hosts_file = args.hosts_file or Path(config.get("paths", {}).get("hosts_file", "config/hosts.txt"))
    summary = RunSummary(subcommand="ping-check")

    if not hosts_file.is_file():
        logger.error("hosts file not found: %s", hosts_file)
        summary.failed = 1
        return summary

    hosts = [
        line.strip()
        for line in hosts_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    summary.total = len(hosts)

    for host in hosts:
        if args.dry_run:
            logger.info("dry-run: would ping host=%s timeout=%s", host, timeout)
        else:
            logger.info("checked host=%s timeout=%s", host, timeout)
        summary.ok += 1

    return summary


def run_disk_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    warn_percent = config.get("defaults", {}).get("disk_warn_percent", 80)
    crit_percent = config.get("defaults", {}).get("disk_crit_percent", 90)
    summary = RunSummary(subcommand="disk-check")
    summary.total = 1

    if args.dry_run:
        logger.info("dry-run: would check disk usage warn=%s crit=%s", warn_percent, crit_percent)
    else:
        logger.info("disk usage checked warn=%s crit=%s", warn_percent, crit_percent)
    summary.ok = 1
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opsctl", description="Operations control CLI (teaching skeleton)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without making changes")
    parser.add_argument("--verbose", action="store_true", help="enable DEBUG logging")
    parser.add_argument("--quiet", action="store_true", help="only show WARNING and above")
    parser.add_argument("--timeout", type=int, default=None, help="override timeout in seconds")

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    ping_parser = subparsers.add_parser("ping-check", help="check connectivity to hosts")
    ping_parser.add_argument("--hosts-file", type=Path, default=None)

    subparsers.add_parser("disk-check", help="check disk usage thresholds")

    return parser


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet are mutually exclusive")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    if args.subcommand == "ping-check":
        summary = run_ping_check(args, config)
    elif args.subcommand == "disk-check":
        summary = run_disk_check(args, config)
    else:  # pragma: no cover
        logger.error("unknown subcommand: %s", args.subcommand)
        return EXIT_USAGE

    print(summary.render(), file=sys.stderr)
    if not args.quiet:
        print(json.dumps(summary.__dict__))
    return summary.exit_code()


if __name__ == "__main__":
    sys.exit(main())
```

実行例:

```bash
python3 samples/python/12_opsctl_cli.py --config config/opsctl.yaml --dry-run ping-check --hosts-file config/hosts.txt
# stderr: ... summary subcommand=ping-check total=3 ok=3 warning=0 critical=0 failed=0
# stdout: {"subcommand": "ping-check", "total": 3, "ok": 3, "warning": 0, "critical": 0, "failed": 0}
# exit code: 0

python3 samples/python/12_opsctl_cli.py disk-check --config config/does_not_exist.yaml
# config/does_not_exist.yaml が無い場合は空設定として扱われ、デフォルト値で実行する
```

---

## 12.10 悪い例と問題点

```python
#!/usr/bin/env python3
import sys

# 設定値がコードに直書きされている
TIMEOUT = 30
HOSTS = ["web01.example.invalid", "web02.example.invalid"]

action = sys.argv[1] if len(sys.argv) > 1 else "ping"

if action == "ping":
    for h in HOSTS:
        print(f"pinging {h} with timeout {TIMEOUT}")
elif action == "disk":
    print("checking disk")
else:
    print("unknown action")
    # 終了コードを返さず、そのまま正常終了してしまう
```

問題点:

- ホスト一覧と閾値がコードに直書きされ、環境ごとにソースを書き換える運用になる
- サブコマンドが `if/elif` の連鎖で、ヘルプや型検証、必須引数チェックが無い
- 不明な操作でもメッセージを出すだけで終了コード0のまま終わり、CIや監視が失敗を検知できない
- `--dry-run`、`--verbose`、`--quiet` に相当する仕組みが無い

---

## 12.11 改善後のコード

12.9の `12_opsctl_cli.py` が改善後にあたる。
設定分離、`argparse` によるサブコマンドとヘルプ、優先順位解決、dry-run、終了コードとサマリーのすべてを満たす。

Bashで同等の骨格を作る場合は、サブコマンドをcase文で分岐し、共通オプションを親スクリプトで解析してから個別関数へ渡す。

```bash
#!/usr/bin/env bash
set -euo pipefail

dry_run=0
verbose=0
quiet=0
subcommand="${1:-}"
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) dry_run=1; shift ;;
    --verbose) verbose=1; shift ;;
    --quiet) quiet=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

case "${subcommand}" in
  ping-check)
    echo "dry_run=${dry_run} verbose=${verbose} quiet=${quiet}: running ping-check" >&2
    ;;
  disk-check)
    echo "dry_run=${dry_run} verbose=${verbose} quiet=${quiet}: running disk-check" >&2
    ;;
  "")
    echo "subcommand is required" >&2
    exit 1
    ;;
  *)
    echo "unknown subcommand: ${subcommand}" >&2
    exit 1
    ;;
esac
```

---

## 12.12 セキュリティ上の注意点

- 設定ファイルに秘密情報を書かない。`config/opsctl.yaml` のコメントにあるとおり、トークンは環境変数から読む（第10章）
- 設定ファイルのパーミッションを絞る。他ユーザーに読み取り可能な設定ファイルへ、将来誰かが誤って秘密情報を書き足すリスクを減らす
- `--verbose` で解決済みの設定値をログに出す際、秘密情報に該当するキーは値をマスキングする（第9章）
- YAML読み込みは `yaml.safe_load` を使う（第3章）。任意コード実行につながる `yaml.load` を使わない

---

## 12.13 テスト方法

```python
import pytest
from pathlib import Path

from samples.python.opsctl_cli import main, resolve_timeout


def test_resolve_timeout_prefers_cli_value() -> None:
    assert resolve_timeout(15, {"defaults": {"timeout_seconds": 30}}) == 15


def test_resolve_timeout_falls_back_to_config() -> None:
    assert resolve_timeout(None, {"defaults": {"timeout_seconds": 45}}) == 45


def test_resolve_timeout_env_overrides_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPSCTL_TIMEOUT_SECONDS", "20")
    assert resolve_timeout(None, {"defaults": {"timeout_seconds": 45}}) == 20


def test_main_ping_check_dry_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    hosts_file = tmp_path / "hosts.txt"
    hosts_file.write_text("a.example.invalid\nb.example.invalid\n", encoding="utf-8")
    exit_code = main(
        ["--dry-run", "--quiet", "ping-check", "--hosts-file", str(hosts_file)]
    )
    assert exit_code == 0


def test_main_rejects_verbose_and_quiet_together() -> None:
    with pytest.raises(SystemExit):
        main(["--verbose", "--quiet", "disk-check"])
```

---

## 章末問題

### 問題1

設定とコードを分離すべき理由を、環境差分の管理という観点から説明せよ。

### 問題2

`opsctl` の設定優先順位（CLI引数 > 環境変数 > 設定ファイル > デフォルト）を採用する利点を一つ述べよ。

### 問題3

`--dry-run` を、読み取り専用の処理と書き込みを伴う処理で同じように実装してよいか、理由とともに述べよ。

### 問題4

終了コードだけでなく実行結果サマリーを出力すべき理由を述べよ。

### 問題5

`--verbose` と `--quiet` を同時に指定できてしまう設計の問題点を述べよ。

---

## 解答と解説

### 問題1

環境ごとにコードを書き換えると、コードの変更履歴に環境固有の差分が混ざり、レビューとロールバックが難しくなる。
設定を分離すれば、コードは環境に依存せず一つに保てる。

### 問題2

その場限りの調整（CLI引数）を最優先にしつつ、通常運用は設定ファイルで管理でき、秘密情報や環境固有値は環境変数で分離できる。
優先順位が明確だと、値の出所を追跡しやすい。

### 問題3

読み取り専用の処理では通常実行と同じ結果でよい場合が多い。
書き込み・削除・外部への変更APIを伴う処理では、必ず分岐し、実際の変更を止める実装が必要である。

### 問題4

終了コードは成否の大枠しか示さない。
対象件数・成功件数・失敗件数が分からないと、部分的な失敗の規模を把握できない。

### 問題5

出力レベルの意図が矛盾し、どちらが優先されるか実装依存になる。
利用者の意図を確認できないため、引数解析の時点でエラーにするべきである。

---

## 実装演習

### 演習A

`12_opsctl_cli.py` に `log-search` サブコマンドを追加せよ。
オプションは `--pattern`（必須）と `--log-dir`（既定値は設定ファイルの `paths.report_dir`）とする。

### 演習B

Bashで、`--config` オプションからYAMLファイルのパスを受け取り、`yq` があれば使い、無ければ「PyYAMLで代替する」旨をエラーメッセージに含めて終了コード1にするスクリプトを書け。

### 演習C

`resolve_timeout` と同じ優先順位の考え方で、`disk_warn_percent` を解決する関数を実装し、CLI引数・環境変数・設定ファイル・デフォルトそれぞれのテストを書け。

---

## 次章予告

第13章では、テストと品質管理を扱う。
ユニットテストと結合テスト、境界値、モック、静的解析、CIへの組み込みを通じて、ここまでのサンプルを検証可能にする。
