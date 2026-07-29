# 第10章 入力値検証とセキュリティ

## 学習目標

- 型・必須・範囲・パスの検証を三言語で実装できる
- コマンドインジェクションとパストラバーサルの成立条件と対策を説明できる
- 秘密情報を環境変数とシークレット管理で扱い、コードに書かない設計にできる
- TLS検証、一時ファイル、最小権限、監査ログの基本方針を実装できる

前提: 第1章（環境変数）、第7章（コマンド実行）、第9章（ログ）。

サンプルコードは学習用である。
本番投入前には、対象システムでの侵入テストや脆弱性診断に相当する確認、権限設計のレビューを別途行うこと。

---

## 10.1 基本概念

**入力値検証**は、外部から受け取った値が、想定する型・範囲・形式に収まっているかを確認する処理である。

運用スクリプトへの入力は、コマンドライン引数、設定ファイル、環境変数、API応答、他プロセスの出力など多岐にわたる。
これらはすべて「信頼できない入力」として扱い、使う前に検証する。

検証を省略すると、誤操作や悪意ある入力が、意図しないコマンド実行やファイルアクセスに直結する。

---

## 10.2 最小構成の検証: 型・必須・範囲

第4章の `classify_usage` を例に、必須・範囲の検証を確認する。

```python
def classify(usage: float, warn: float, crit: float) -> str:
    if usage < 0 or usage > 100:
        raise ValueError("usage must be between 0 and 100")
    if warn < 0 or crit < 0 or warn > 100 or crit > 100:
        raise ValueError("thresholds must be between 0 and 100")
    if warn > crit:
        raise ValueError("warn must be <= crit")
    ...
```

辞書形式の設定値を検証する場合は、必須キーの欠落と型不一致を分けて報告すると、利用者が直しやすい。

```python
def validate_target_config(config: dict) -> None:
    required = ["host", "port"]
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError(f"missing required keys: {missing}")
    if not isinstance(config["port"], int):
        raise TypeError("port must be an integer")
    if not (1 <= config["port"] <= 65535):
        raise ValueError("port must be between 1 and 65535")
```

Bash（整数と範囲）:

```bash
validate_port() {
  local port="$1"
  if ! [[ "${port}" =~ ^[0-9]+$ ]]; then
    echo "port must be numeric: ${port}" >&2
    return 1
  fi
  if (( port < 1 || port > 65535 )); then
    echo "port out of range: ${port}" >&2
    return 1
  fi
}
```

PowerShell:

```powershell
function Assert-ValidPort {
    param([Parameter(Mandatory = $true)][int]$Port)
    if ($Port -lt 1 -or $Port -gt 65535) {
        throw "port out of range: $Port"
    }
}
```

---

## 10.3 パス検証とパストラバーサル対策

**パストラバーサル**は、`../` などを含む入力によって、想定した範囲外のファイルへアクセスさせる攻撃である。

### 悪いコード

```python
from pathlib import Path

def read_report(base_dir: str, filename: str) -> str:
    path = Path(base_dir) / filename
    return path.read_text(encoding="utf-8")

# filename = "../../../../etc/passwd" を渡すと base_dir の外を読んでしまう
```

### 改善後

```python
from pathlib import Path


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    """base_dir 配下に解決できないパスは拒否する。"""
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def read_report(base_dir: Path, filename: str) -> str:
    path = safe_resolve_path(base_dir, filename)
    return path.read_text(encoding="utf-8")
```

`resolve()` はシンボリックリンクを解決したうえで絶対パスにする。
`base_dir` 配下に見えるシンボリックリンクが外部を指している場合、この検証だけでは不十分になる場合がある。
公開範囲が広い用途では、シンボリックリンクの追跡自体を禁止する、あるいは対象ディレクトリの書き込み権限を管理者以外に与えない、といった追加の防御を検討する。

Bash（`realpath` で解決してから前方一致を確認する）:

```bash
safe_resolve_path() {
  local base_dir="$1"
  local relative_path="$2"
  local base_resolved candidate

  base_resolved="$(realpath -e "${base_dir}")" || return 1
  candidate="$(realpath -m "${base_resolved}/${relative_path}")"

  case "${candidate}" in
    "${base_resolved}"/*|"${base_resolved}")
      printf '%s\n' "${candidate}"
      ;;
    *)
      echo "path escapes base directory: ${relative_path}" >&2
      return 1
      ;;
  esac
}
```

PowerShell:

```powershell
function Get-SafeResolvedPath {
    param(
        [Parameter(Mandatory = $true)][string]$BaseDir,
        [Parameter(Mandatory = $true)][string]$RelativePath
    )
    $baseResolved = (Resolve-Path -LiteralPath $BaseDir).Path
    $candidate = [System.IO.Path]::GetFullPath((Join-Path $baseResolved $RelativePath))
    if (-not ($candidate -eq $baseResolved -or $candidate.StartsWith($baseResolved + [System.IO.Path]::DirectorySeparatorChar))) {
        throw "path escapes base directory: $RelativePath"
    }
    return $candidate
}
```

---

## 10.4 コマンドインジェクション対策

**コマンドインジェクション**は、外部入力を通じて、意図しないコマンドをシェルに実行させる攻撃である。

### 悪いコード

```python
import subprocess

def ping(host: str) -> str:
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return result.stdout

# host = "web01.example.invalid; rm -rf /tmp/work" のような入力で
# セミコロン以降が別コマンドとして実行される
```

### 改善後

```python
import re
import subprocess

HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def ping(host: str, timeout: int = 3) -> str:
    validate_hostname(host)
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), host],
        capture_output=True,
        text=True,
        timeout=timeout + 2,
        shell=False,
    )
    return result.stdout
```

対策の骨子は二つある。

1. `shell=True` を使わず、コマンドと引数をリストで渡す（第7章）
2. リストで渡す場合でも、値そのものが想定形式であることを検証する（コマンド名やオプションのすり替えを防ぐ）

Bashでは、`eval` と、引用符を欠いた変数展開が主な原因になる。

```bash
# 悪い例: evalで動的にコマンドを組み立てる
eval "ping -c 1 ${host}"

# 改善: 配列と引用符で引数を分離する
cmd=(ping -c 1 -- "${host}")
"${cmd[@]}"
```

PowerShellでは `Invoke-Expression` が同種のリスクを持つ。

```powershell
# 悪い例
Invoke-Expression "ping -n 1 $HostName"

# 改善: 呼び出し演算子と配列引数
$pingArgs = @('-n', '1', $HostName)
& ping @pingArgs
```

---

## 10.5 権限と最小権限

**最小権限の原則**は、処理の実行に必要な最小限の権限だけを与える考え方である。

実務上の指針:

- スクリプト全体をroot/Administratorで実行せず、必要な一操作だけを昇格する（`sudo` を特定コマンドに限定する、Windowsではタスクの実行アカウントを分ける）
- 秘密情報を含むファイルはパーミッションを絞る（`chmod 600`）
- サービスアカウントには、対象リソースへの読み書きなど、必要な操作のみを許可する
- 一時的な昇格は、目的と期間を監査ログに残す

```bash
chmod 600 /etc/opsctl/secrets.env
chown opsctl:opsctl /etc/opsctl/secrets.env
```

---

## 10.6 秘密情報と環境変数

秘密情報（APIトークン、パスワード、秘密鍵）は、次の場所に置かない。

- ソースコード中のリテラル
- Gitリポジトリにコミットする設定ファイル
- コマンドライン引数（`ps` や プロセス一覧で他ユーザーに見える場合がある）

環境変数、または後述のシークレット管理サービスから実行時に読み込む。

```python
import os
import sys

token = os.environ.get("OPSCTL_API_TOKEN")
if not token:
    print("OPSCTL_API_TOKEN is required", file=sys.stderr)
    sys.exit(1)
```

> **警告**: 秘密情報を `--token xxxx` のような引数で渡す設計は、`ps aux` や監査ログに値が残る場合がある。
> 環境変数か、値を含まないファイルパス渡し（ファイル自体の権限で保護する）を優先する。

---

## 10.7 シークレット管理

**シークレット管理**は、秘密情報の保存・配布・失効を一元的に扱う仕組みである。

方針:

- 秘密情報をリポジトリへコミットしない（`.gitignore` に環境変数ファイルを含める。第16章）
- 本番の秘密情報はHashiCorp Vault、AWS Secrets Manager、Azure Key Vaultのような専用サービス、またはCIの秘密変数機能で管理する
- 定期的にローテーション（値の更新と旧値の失効）する
- 漏えいが疑われたら、即座に失効し、影響範囲を監査ログから確認する

学習用の値は、必ず無効なダミー（`replace-me` など）にする。

```bash
export OPSCTL_API_TOKEN='replace-me'
```

---

## 10.8 TLS検証

**TLS検証**は、通信先の証明書が信頼できる認証局によって発行され、想定したホスト名と一致するかを確認する処理である。
検証を無効化すると、通信内容の盗聴や改ざん（中間者攻撃）を検出できなくなる。

> **警告**: `requests` の `verify=False`、curlの `-k`/`--insecure`、PowerShellの `-SkipCertificateCheck` は、TLS証明書検証を無効化する。
> 自己署名証明書の検証環境であっても、検証を無効化するのではなく、その環境のCA証明書をシステムまたはライブラリの信頼ストアへ登録する方法を優先する。

```python
import requests

# 悪い例
requests.get("https://api.example.invalid/v1/hosts", verify=False)

# 改善: 既定の検証を有効のままにし、社内CAが必要なら証明書バンドルを指定する
requests.get(
    "https://api.example.invalid/v1/hosts",
    verify="/etc/ssl/certs/internal-ca-bundle.pem",
)
```

第11章で、TLSを含むAPI呼び出しの全体像を扱う。

---

## 10.9 安全でない一時ファイル

予測可能な名前の一時ファイル（`/tmp/report.txt` など）は、他プロセスによる先読み・上書き・シンボリックリンク攻撃の対象になりうる。

Python:

```python
import tempfile
from pathlib import Path


def write_temp_report(content: str) -> Path:
    fd, name = tempfile.mkstemp(prefix="opsctl_", suffix=".txt")
    path = Path(name)
    try:
        with path.open("w", encoding="utf-8") as fh:
            fh.write(content)
    finally:
        import os

        os.close(fd)
    path.chmod(0o600)
    return path
```

`tempfile.mkstemp` は、他プロセスと衝突しないランダムな名前で、所有者のみアクセス可能なファイルを作る。

Bash:

```bash
tmp_file="$(mktemp /tmp/opsctl.XXXXXX)"
trap 'rm -f "${tmp_file}"' EXIT
```

PowerShell:

```powershell
$tmpFile = New-TemporaryFile
try {
    Set-Content -LiteralPath $tmpFile -Value 'report body' -Encoding utf8
}
finally {
    Remove-Item -LiteralPath $tmpFile -ErrorAction SilentlyContinue
}
```

---

## 10.10 監査ログ

**監査ログ**は、誰が・いつ・何を実行したかを、後から検証できる形で残す記録である。
デバッグ用のログと目的が異なるため、分離して扱う。

満たすべき条件:

- 実行者（サービスアカウント名、ログイン名）を含む
- 実行した操作、対象、結果（成功/失敗）を含む
- 改ざんされにくい保存先に送る（追記専用ストレージ、集約基盤）
- 保持期間をコンプライアンス要件に合わせて設定する

```python
audit_logger.info(
    "operation=%s actor=%s target=%s result=%s run_id=%s",
    "config-patch",
    os.environ.get("USER", "unknown"),
    target_host,
    "success",
    run_id,
)
```

破壊的操作（削除、設定変更、権限変更）を実行するサブコマンドは、監査ログを必須とし、dry-runでない実行のみ記録する。

---

## 10.11 悪い例と問題点（統合）

```python
#!/usr/bin/env python3
import subprocess
import sys

base_dir = "/var/opsctl/configs"


def patch_config(filename: str, host: str) -> None:
    path = base_dir + "/" + filename          # パス検証なし
    subprocess.run(f"scp {path} {host}:/etc/app.conf", shell=True)  # shell=True + 文字列連結
    print(f"patched {host}")                  # 成否を確認せず成功と表示


if __name__ == "__main__":
    patch_config(sys.argv[1], sys.argv[2])
```

問題点:

- `filename` にパストラバーサル文字列を渡すと `base_dir` 外のファイルを送信できる
- `host` や `filename` に `;` や `` ` `` を含めるとコマンドインジェクションが成立する
- `subprocess.run` の戻り値を確認しておらず、失敗しても成功と表示する
- 秘密情報や監査ログが無く、誰がいつ何を変更したか後から追えない

---

## 10.12 改善後のコード

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

BASE_DIR = Path("/var/opsctl/configs")
HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)

logger = logging.getLogger("config_patch")
audit_logger = logging.getLogger("config_patch.audit")


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def patch_config(filename: str, host: str, *, dry_run: bool) -> int:
    try:
        source = safe_resolve_path(BASE_DIR, filename)
        validate_hostname(host)
    except (OSError, ValueError) as exc:
        logger.error("validation failed: %s", exc)
        return EXIT_USAGE

    if not source.is_file():
        logger.error("config file not found: %s", source)
        return EXIT_USAGE

    if dry_run:
        logger.info("dry-run: would copy %s to %s:/etc/app.conf", source, host)
        return EXIT_OK

    result = subprocess.run(
        ["scp", str(source), f"{host}:/etc/app.conf"],
        capture_output=True,
        text=True,
        timeout=30,
        shell=False,
        check=False,
    )
    actor = os.environ.get("USER", "unknown")
    if result.returncode != 0:
        logger.error("scp failed host=%s stderr=%s", host, result.stderr.strip())
        audit_logger.info(
            "operation=config-patch actor=%s target=%s result=failure", actor, host
        )
        return EXIT_RUNTIME

    logger.info("patched host=%s", host)
    audit_logger.info(
        "operation=config-patch actor=%s target=%s result=success", actor, host
    )
    return EXIT_OK


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy a config file to a target host")
    parser.add_argument("--filename", required=True)
    parser.add_argument("--host", required=True)
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
    return patch_config(args.filename, args.host, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

改善点は、パス検証、ホスト名検証、`shell=True` の排除、戻り値確認、dry-run、監査ログの六つである。

---

## 10.13 テスト方法

```python
import pytest
from pathlib import Path

from samples.python.safe_path_and_exec import safe_resolve_path, validate_hostname


def test_safe_resolve_path_rejects_traversal(tmp_path: Path) -> None:
    base = tmp_path / "configs"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_resolve_path(base, "../../etc/passwd")


def test_safe_resolve_path_allows_nested_file(tmp_path: Path) -> None:
    base = tmp_path / "configs"
    (base / "sub").mkdir(parents=True)
    resolved = safe_resolve_path(base, "sub/app.conf")
    assert resolved == (base / "sub" / "app.conf").resolve()


@pytest.mark.parametrize("host", ["web01.example.invalid", "db-1.example.invalid"])
def test_validate_hostname_accepts_valid(host: str) -> None:
    assert validate_hostname(host) == host


@pytest.mark.parametrize("host", ["web01; rm -rf /", "$(whoami)", "web01 && id"])
def test_validate_hostname_rejects_injection(host: str) -> None:
    with pytest.raises(ValueError):
        validate_hostname(host)
```

---

## 章末問題

### 問題1

パストラバーサルが成立する条件を、入力例を挙げて説明せよ。

### 問題2

`subprocess.run(cmd, shell=True)` に文字列連結でホスト名を渡す設計の危険を述べ、安全な書き換えを示せ。

### 問題3

APIトークンをコマンドライン引数で渡してはいけない理由を、`ps` コマンドの挙動に触れて説明せよ。

### 問題4

TLS証明書検証を無効化することで防げなくなる攻撃を一つ挙げよ。

### 問題5

監査ログとデバッグログを分離すべき理由を二つ述べよ。

---

## 解答と解説

### 問題1

`../` を含む入力で、`base_dir` の外にあるファイルへパスが解決されると成立する。
例: `filename="../../etc/passwd"`。

### 問題2

ホスト名にシェルのメタ文字（`;`、`` ` ``、`$()`）を含めると、別コマンドとして実行される。
改善: `shell=True` をやめ、リスト引数で渡し、ホスト名を正規表現で検証する。

### 問題3

`ps aux` や `/proc/<pid>/cmdline` から、同一ホスト上の他ユーザーが起動時の引数を閲覧できる場合がある。
環境変数やファイル権限で保護した受け渡しに切り替える。

### 問題4

中間者攻撃（通信の盗聴・改ざん）を検出できなくなる。

### 問題5

監査ログは改ざん耐性と長期保持が求められ、デバッグログは詳細度と揮発性が高い。
目的と保持要件が異なるため、混在させると必要な情報の抽出とアクセス制御が難しくなる。

---

## 実装演習

### 演習A

`safe_resolve_path` を使い、指定ディレクトリ配下のファイル一覧を安全に列挙するPythonスクリプトを書け。
`../` を含む入力で終了コード1になることを確認せよ。

### 演習B

Bashで `validate_hostname` 相当の関数を実装し、ホスト名にセミコロンを含む入力を拒否するテストを書け。

### 演習C

`10_safe_path_and_exec.py` の監査ログ出力を、9章のJSONロガーへ差し替え、`operation`/`actor`/`target`/`result` フィールドを持つJSON行として出力せよ。

---

## 次章予告

第11章では、APIとネットワーク処理を扱う。
HTTPメソッドとステータスコード、認証、タイムアウトとリトライ、ページネーション、レート制限、TLSを含むAPI呼び出しを三言語で実装する。
