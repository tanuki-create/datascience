# 第1章 スクリプトとプログラミングの基本

## 学習目標

この章を終えると、次ができるようになる。

- スクリプトとコンパイル言語の違いを、実行の流れで説明できる
- 標準入力、標準出力、標準エラー、終了コードを使い分けられる
- 環境変数とコマンドライン引数で、設定と秘密情報をコードから分離できる
- 手作業を「入力・処理・出力・失敗時挙動」に分解し、自動化の可否を判断できる

前提:

- Python 3.11以上、Bash 4以上、PowerShell 7.4以上のいずれかが使えること
- ターミナルでカレントディレクトリを変更できること

---

## 基本概念

本章で扱う中心概念は次のとおりである。

- **スクリプト**: インタープリターがソースを読みながら実行するプログラム
- **標準入出力**: stdin / stdout / stderr の役割分担
- **終了コード**: プロセスの成否を整数で返す契約
- **環境変数と引数**: 実行環境の設定と、その実行だけの選択の分離

詳細は以降の節で順に展開する。

---

## 1.1 スクリプトとは何か

**スクリプト**とは、インタープリターがソースコードを読みながら逐次実行するプログラムである。

インフラ運用では、次のような作業をファイルに書いて繰り返せる形にしたものがスクリプトと呼ばれる。

- 複数サーバーへの疎通確認
- ログの検索と集計
- 設定ファイルのバックアップと差し替え
- APIから情報を取得してCSVに落とす

スクリプトの価値は、タイピングの省略だけではない。手順を文章ではなく実行可能な形で固定し、同じ条件なら同じ結果を再現できる点にある。

手作業の手順書が「だいたい同じ」で終わるのに対し、スクリプトは入力が同じなら出力も揃う。揃わないときは、環境差かバグとして調査対象になる。

---

## 1.2 コンパイル言語との違い

**コンパイル言語**では、ソースコードをコンパイラが機械語や中間表現に変換してから実行する。CやGo、Rustが典型である。

**インタープリター言語**では、実行のたびにインタープリターがソースを解釈する。Python、Bash、PowerShellがこれに近い。[^1]

実務上の差は次のとおりである。

| 観点 | スクリプト寄り（Python / Bash / PowerShell） | コンパイル寄り（Go / Rust など） |
|------|-----------------------------------------------|----------------------------------|
| 変更から実行まで | 編集してすぐ実行できる | ビルドが必要 |
| 配布 | ランタイムが必要 | 単一バイナリにしやすい |
| 型や安全性 | 言語と運用で補う | コンパイル時検査が強いことが多い |
| 運用現場での採用 | 既存コマンドとの糊付けに強い | 長期稼働の常駐ツール向き |

インフラ自動化では、既存のOSコマンド、設定ファイル、APIを短期間でつなぐことが多い。そのためスクリプトが選ばれやすい。一方、常駐エージェントや高負荷な収集基盤ではコンパイル言語が選ばれることもある。本書は前者を対象とする。

[^1]: PowerShellは実行前にパースとコンパイル段階を持つ。本書では「ソースを直接実行できる」点をスクリプトとして扱う。

---

## 1.3 インタープリターとソースコード

**ソースコード**は、人が読み書きするプログラムの原文である。

**インタープリター**は、ソースコードを読み、文を解釈して実行するプログラムである。

三言語の起動例:

```bash
python3 hello.py
bash hello.sh
pwsh hello.ps1
```

シバン（shebang）を付けると、Unix系ではファイルを直接実行できる。

```bash
#!/usr/bin/env python3
print("hello")
```

```bash
#!/usr/bin/env bash
echo "hello"
```

```bash
#!/usr/bin/env pwsh
Write-Output "hello"
```

実行権限が必要である。

```bash
chmod +x hello.py
./hello.py
```

Windowsではシバンは使わないことが多い。`python`、`pwsh` を明示して呼び出す。

PowerShellの実行ポリシーが RemoteSigned などの制限だと、ダウンロードしたスクリプトがブロックされる。方針は組織のセキュリティポリシーに従う。学習用ローカルファイルでは、署名なしローカルスクリプトが許可されているかを確認する。

```powershell
Get-ExecutionPolicy -List
```

---

## 1.4 標準入力、標準出力、標準エラー

プロセスは起動時に、少なくとも三つの入出力チャネルを持つ。

- **標準入力（stdin）**: 入力の受け口。番号は 0
- **標準出力（stdout）**: 正常な結果の出し口。番号は 1
- **標準エラー（stderr）**: 診断情報やエラーの出し口。番号は 2

運用スクリプトでは、次の分担が扱いやすい。

- stdout: 機械が次に使う結果（CSV、JSON、ホスト名一覧）
- stderr: 人や監視が読む進捗とエラー

結果とログを同じストリームに混ぜると、パイプの下流が壊れる。

### 最小構成のコード

Python:

```python
#!/usr/bin/env python3
import sys

name = sys.stdin.readline().strip()
if not name:
    print("name is required", file=sys.stderr)
    sys.exit(1)

print(f"hello, {name}")
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

read -r name
if [[ -z "${name}" ]]; then
  echo "name is required" >&2
  exit 1
fi

echo "hello, ${name}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

$name = [Console]::In.ReadLine()
if ([string]::IsNullOrWhiteSpace($name)) {
    [Console]::Error.WriteLine('name is required')
    exit 1
}

Write-Output "hello, $name"
```

実行例（Bash）:

```bash
printf 'ops\n' | bash samples/bash/01_hello_stdin.sh
# stdout: hello, ops
```

エラー例:

```bash
printf '\n' | bash samples/bash/01_hello_stdin.sh
# stderr: name is required
# exit code: 1
```

### リダイレクト

```bash
# stdout をファイルへ
./tool.sh > result.txt

# stderr をファイルへ
./tool.sh 2> error.txt

# 両方
./tool.sh > all.txt 2>&1

# stdin をファイルから
./tool.sh < hosts.txt
```

PowerShell:

```powershell
./tool.ps1 > result.txt
./tool.ps1 2> error.txt
Get-Content hosts.txt | ./tool.ps1
```

---

## 1.5 終了コード

**終了コード**（exit status）は、プロセスが終了したときにOSへ返す整数である。

慣例:

- `0`: 成功
- 非0: 失敗

シェルでは直前のコマンドの終了コードが `$?`（Bash）または `$LASTEXITCODE`（PowerShell）に入る。

```bash
true
echo $?    # 0

false
echo $?    # 1
```

```powershell
pwsh -NoProfile -Command 'exit 3'
echo $LASTEXITCODE
```

監視やCIは終了コードで成否を判定する。メッセージだけ出して終了コード0のままにするのは、失敗の隠蔽である。

本書の `opsctl` では次を使う（README参照）。

| コード | 意味 |
|--------|------|
| 0 | 成功 |
| 1 | 使い方・設定の誤り |
| 2 | 実行時エラー（部分失敗を含む） |
| 3 | 監視上の CRITICAL |
| 4 | タイムアウト |
| 130 | Ctrl+C |

### 悪いコード

```python
#!/usr/bin/env python3
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
print(text.upper())
# ファイルが無くても例外で落ちるが、呼び出し側向けの終了コード設計がない
# 引数不足も IndexError のまま
```

問題点:

- 引数不足が利用者向けメッセージにならない
- 例外がトレースバックのまま終わり、終了コードが言語既定に依存する
- stderr / stdout の役割が不明

### 改善後のコード

```python
#!/usr/bin/env python3
"""Read a text file and print its uppercased contents."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("upperfile")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uppercase a text file")
    parser.add_argument("path", type=Path, help="input text file")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable debug logging",
    )
    return parser.parse_args(argv)


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    if not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(args.verbose)

    try:
        text = read_text_file(args.path)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME

    sys.stdout.write(text.upper())
    if text and not text.endswith("\n"):
        sys.stdout.write("\n")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

実行例:

```bash
echo 'abc' > /tmp/a.txt
python3 samples/python/01_upperfile.py /tmp/a.txt
# ABC

python3 samples/python/01_upperfile.py /tmp/missing.txt
echo $?
# stderr に error、終了コード 2
```

---

## 1.6 環境変数

**環境変数**は、プロセスに渡されるキーと値の組である。子プロセスにも継承される。

用途の分離:

- コード: 手順とロジック
- 引数: その実行だけの選択
- 環境変数: 実行環境ごとの設定や秘密情報の受け渡し口

秘密情報（APIトークン、パスワード）をソースに直書きしない。環境変数、シークレットマネージャ、CIの秘密変数から渡す。

### 読み取り例

Python:

```python
#!/usr/bin/env python3
import os
import sys

token = os.environ.get("OPSCTL_API_TOKEN")
if not token:
    print("OPSCTL_API_TOKEN is required", file=sys.stderr)
    sys.exit(1)

print("token is set", file=sys.stderr)
print(len(token))  # 値そのものは出さない
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPSCTL_API_TOKEN:-}" ]]; then
  echo "OPSCTL_API_TOKEN is required" >&2
  exit 1
fi

echo "token is set" >&2
echo "${#OPSCTL_API_TOKEN}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($env:OPSCTL_API_TOKEN)) {
    [Console]::Error.WriteLine('OPSCTL_API_TOKEN is required')
    exit 1
}

[Console]::Error.WriteLine('token is set')
Write-Output $env:OPSCTL_API_TOKEN.Length
```

設定例:

```bash
export OPSCTL_API_TOKEN='replace-me'
python3 samples/python/01_check_token.py
```

```powershell
$env:OPSCTL_API_TOKEN = 'replace-me'
pwsh samples/powershell/01_check_token.ps1
```

ログや標準出力にトークン本体を出さない。長さや「設定済み」だけを出す。

---

## 1.7 コマンドライン引数

**コマンドライン引数**は、起動時にプロセスへ渡すパラメータである。

```bash
python3 tool.py --hosts-file hosts.txt --timeout 10
```

`sys.argv`、Bashの `$1`、PowerShellの `param()` ブロックで受け取る。

実務では次を最初から決める。

- 必須引数と任意引数
- デフォルト値
- ヘルプ（`--help`）
- 不正値のときの終了コード

### 最小構成（三言語）

Python（argparse）:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Echo hosts file path")
    parser.add_argument("--hosts-file", required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.timeout <= 0:
        print("--timeout must be positive", file=sys.stderr)
        return 1
    print(f"{args.hosts_file},{args.timeout}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

hosts_file=""
timeout=30

usage() {
  cat <<'EOF' >&2
Usage: 01_parse_args.sh --hosts-file PATH [--timeout SECONDS]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hosts-file)
      hosts_file="${2:-}"
      shift 2
      ;;
    --timeout)
      timeout="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${hosts_file}" ]]; then
  echo "--hosts-file is required" >&2
  usage
  exit 1
fi

if ! [[ "${timeout}" =~ ^[1-9][0-9]*$ ]]; then
  echo "--timeout must be a positive integer" >&2
  exit 1
fi

echo "${hosts_file},${timeout}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile,

    [int]$Timeout = 30
)

$ErrorActionPreference = 'Stop'

if ($Timeout -le 0) {
    [Console]::Error.WriteLine('--Timeout must be positive')
    exit 1
}

Write-Output "$HostsFile,$Timeout"
exit 0
```

---

## 1.8 手作業を自動化する際の考え方

自動化は、手順書のタイピング置換ではない。次の順で分解する。

1. **目的**: 何が達成されれば終わりか
2. **入力**: ファイル、引数、環境変数、API、人の確認
3. **出力**: ファイル、標準出力、終了コード、チケット更新
4. **成功条件**: 終了コード0の意味
5. **失敗時**: どこまで戻すか、誰に何を残すか
6. **再実行**: 二度実行しても安全か
7. **権限**: 最小権限で足りるか

例: 「毎朝、各Webサーバーのディスク使用率を見て、90%超なら知らせる」

| 項目 | 内容 |
|------|------|
| 入力 | ホスト一覧、SSH認証、閾値、通知先 |
| 処理 | 各ホストで使用率取得、閾値比較 |
| 出力 | レポート、通知、終了コード |
| 失敗 | 一部ホスト不通でも残りは調べる。不通は一覧化 |
| 再実行 | 読み取りだけなら何度でも可 |
| やってはいけないこと | 閾値超過で即削除や即拡張を自動実行する（要変更管理） |

疑似コードに落とす。

```text
load hosts
for host in hosts:
  try:
    usage = get_disk_usage(host, timeout=30)
    if usage >= critical:
      record critical
    elif usage >= warn:
      record warn
  catch:
    record unreachable
write report
if any critical or unreachable:
  exit non-zero
else:
  exit 0
```

第2章で、この分解をアルゴリズムとして深める。

---

## 1.9 自動化すべき作業とすべきでない作業

### 自動化しやすい作業

- 手順が固定で、判断が規則に落とせる
- 頻度が高く、手作業ミスの損害が大きい
- 結果を終了コードやレポートで機械判定できる
- 失敗時に安全側へ倒せる（読み取り、dry-run、バックアップ付き）

例: 疎通確認、証明書期限の一覧化、ログの定型検索、バックアップ取得。

### 自動化を急がない作業

- 一回限りで、再現条件が残らない
- 判断が政治的・契約的で、コードに落とせない
- 失敗時の影響が大きく、承認なしで進めてはならない
- 対象が不定で、探索的調査が本体である

例: 初回の障害原因仮説の立案、大規模本番の手動フェイルオーバー判断、権限の永久付与。

破壊的操作を自動化する場合の最低条件:

1. dry-runがある
2. バックアップまたはロールバック手順がある
3. 実行前確認（対話または変更チケットID）がある
4. 監査ログが残る
5. 権限が最小である

> **警告**: 削除、上書き、再起動、ファイアウォール変更を、確認なしのcronだけで回さない。まず報告だけを自動化し、変更は承認後に別コマンドで実行する構成が安全である。

---

## 1.10 実務向けの小さな統合例

手作業「ホスト名を1行ずつ読み、空行とコメントを除いて件数を出す」を、三言語で実装する。

入力ファイル例 `config/hosts.txt`:

```text
# web tier
web01.example.invalid
web02.example.invalid

# db tier
db01.example.invalid
```

### Python

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("count_hosts")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Count non-empty host lines")
    parser.add_argument("hosts_file", type=Path)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")

    hosts: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {line_no}: contains whitespace")
        hosts.append(line)
    return hosts


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME

    logger.info("loaded %s hosts", len(hosts))
    print(len(hosts))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

### Bash

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 HOSTS_FILE" >&2
  exit 1
fi

hosts_file="$1"
if [[ ! -f "${hosts_file}" ]]; then
  echo "hosts file not found: ${hosts_file}" >&2
  exit 2
fi

count=0
line_no=0
while IFS= read -r raw || [[ -n "${raw}" ]]; do
  line_no=$((line_no + 1))
  # trim
  line="$(printf '%s' "${raw}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [[ -z "${line}" ]] && continue
  [[ "${line}" == \#* ]] && continue
  if [[ "${line}" =~ [[:space:]] ]]; then
    echo "invalid host at line ${line_no}: contains whitespace" >&2
    exit 2
  fi
  count=$((count + 1))
done < "${hosts_file}"

echo "loaded ${count} hosts" >&2
echo "${count}"
```

### PowerShell

```powershell
#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $HostsFile -PathType Leaf)) {
    [Console]::Error.WriteLine("hosts file not found: $HostsFile")
    exit 2
}

$hosts = @()
$lineNo = 0
foreach ($raw in Get-Content -LiteralPath $HostsFile) {
    $lineNo++
    $line = $raw.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line.StartsWith('#')) { continue }
    if ($line -match '\s') {
        [Console]::Error.WriteLine("invalid host at line ${lineNo}: contains whitespace")
        exit 2
    }
    $hosts += $line
}

[Console]::Error.WriteLine("loaded $($hosts.Count) hosts")
Write-Output $hosts.Count
exit 0
```

実行例:

```bash
python3 samples/python/01_count_hosts.py config/hosts.txt
# stderr: INFO loaded 3 hosts
# stdout: 3
```

---

## 1.11 セキュリティ上の注意点

- パスワード、トークン、秘密鍵をソース、ログ、コミットに含めない
- 引数に秘密情報を渡すと `ps` で見える場合がある。可能なら環境変数やファイル権限付きシークレットを使う
- 利用者入力をそのままシェルに連結しない（第7章、第10章）
- 終了コード0で失敗を隠さない
- 学習用ドメイン例には `example.invalid` など、実在しにくい名前を使う

---

## 1.12 テスト方法

第1章では「終了コード」と「stdout/stderrの分離」を手動でも機械でも確認する。

Python（pytestの骨格）:

```python
# tests/test_01_count_hosts.py
from pathlib import Path

from samples.python.count_hosts import load_hosts, main


def test_load_hosts_skips_comments(tmp_path: Path) -> None:
    path = tmp_path / "hosts.txt"
    path.write_text("# c\na.example.invalid\n\nb.example.invalid\n", encoding="utf-8")
    assert load_hosts(path) == ["a.example.invalid", "b.example.invalid"]


def test_main_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.txt"
    assert main([str(missing)]) == 2
```

Bash:

```bash
bash samples/bash/01_count_hosts.sh config/hosts.txt
test "$(bash samples/bash/01_count_hosts.sh config/hosts.txt 2>/dev/null)" -eq 3
```

PowerShell:

```powershell
$result = pwsh -File samples/powershell/01_count_hosts.ps1 -HostsFile config/hosts.txt
if ($result -ne 3) { throw "unexpected count: $result" }
```

---

## 章末問題

### 問題1

次の手作業を、入力・処理・出力・失敗時・再実行性に分解せよ。

「設定ファイル `app.conf` を編集する前に、同ディレクトリへ日時付きコピーを取り、編集後に `nginx -t` 相当の構文チェックを行う。」

### 問題2

stdoutに進捗メッセージ、結果JSONの両方を出しているスクリプトの問題点を述べ、修正方針を書け。

### 問題3

環境変数 `BACKUP_ROOT` が未設定のとき、デフォルトで `/` 以下を削除対象にしてしまう設計の危険を説明し、安全側のデフォルトを提案せよ。

### 問題4

終了コードが常に0で、失敗はメール本文にだけ書く監視連携の欠点を述べよ。

### 問題5

次のBash断片の問題点を指摘し、改善案を書け。

```bash
hosts=$1
for h in $(cat $hosts); do
  ping -c 1 $h
done
```

---

## 解答と解説

### 問題1

| 項目 | 例 |
|------|-----|
| 入力 | `app.conf` のパス、バックアップ先、チェックコマンド、dry-run可否 |
| 処理 | バックアップ作成 →（非dry-runなら）編集適用 → 構文チェック |
| 出力 | バックアップパス、チェック結果、終了コード |
| 失敗時 | チェック失敗なら編集を戻すか、サービス再読込をしない |
| 再実行 | バックアップ名に時刻を含め、上書きしない |

### 問題2

パイプやリダイレクトで結果だけを渡せない。進捗はstderr、結果はstdoutへ分離する。

### 問題3

未設定時にルート近傍を触ると、誤削除の被害が全域に広がる。未設定は即終了（終了コード1）にし、削除対象は明示引数のみとする。

### 問題4

監視やCIが失敗を検知できない。アラートがメール依存になり、遅延や見逃しが起きる。終了コードとログの両方を使う。

### 問題5

- `cat` と単語分割で、空白やグロブが壊れる
- 変数が引用符なし
- ping失敗でもループが続き、全体の終了コードが最後の結果に依存する
- タイムアウトがない

改善方針: `while read` で1行ずつ、引用符、失敗集計、`ping -W` などのタイムアウト、最後に集計終了コード。

---

## 実装演習

### 演習A: echoツールの三言語実装

要件:

- 引数 `--message` を必須とする
- `--times N`（既定1）で繰り返す
- Nが正の整数でなければ終了コード1
- 進捗はstderr、本文はstdout
- 使用方法を `--help` で出せる（Python/PowerShellは標準機能、Bashは自前）

提出物: 三言語のスクリプト、実行例、失敗例。

### 演習B: 手作業の分解シート

自分が週1回以上やっている手作業を一つ選び、次の表を埋める。

- 目的
- 入力
- 出力
- 成功条件
- 失敗時
- 再実行性
- 自動化する / しない の判断と理由

### 演習C: opsctl設定の読み取り準備

`config/opsctl.yaml` と `config/hosts.txt` を用意し、ホスト件数を数えるスクリプト（本章のcount_hosts）で検証する。次章以降でこの入力を共有する。

---

## 次章予告

第2章では、本章の分解を疑似コード、フローチャート、状態、計算量、エッジケースまで落とし、実装前に失敗時挙動を決める手順を扱う。
