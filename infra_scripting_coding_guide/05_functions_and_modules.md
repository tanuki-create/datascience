# 第5章 関数とモジュール

## 学習目標

この章を終えると、次ができるようになる。

- 関数の目的、引数、戻り値、スコープ、副作用を三言語で説明できる
- 純粋関数と副作用のある関数を見分け、境界を意識して分割できる
- モジュール化と名前空間の役割を説明し、責務ごとにファイルを分けられる
- 「関数に切り出すべきか」を具体的な判断基準で決められる
- Pythonモジュール、Bash関数、PowerShell関数とモジュールの書き方を実装できる

前提: 第1章〜第4章の入出力、終了コード、データ型、制御構文。

---

## 5.1 基本概念

**関数**は、入力を受け取り、決まった処理を行い、結果を返すコードのまとまりである。
名前を付けることで、呼び出し側は内部の実装を読まなくても、その関数が何をするか推測できる。
同じ処理を複数箇所に書く代わりに関数を一つ用意すれば、修正箇所も一つで済む。

**引数**は、関数の呼び出し時に渡す入力である。
**戻り値**は、関数が呼び出し元へ返す結果である。
戻り値を持たない関数もあるが、その場合は副作用（後述）が処理の本体になる。

**モジュール**は、関数や変数をひとまとめにして、他のコードから再利用できるようにした単位である。
Pythonの `.py` ファイル、PowerShellの `.psm1` ファイルが典型例である。
Bashには言語標準のモジュール機構が無く、ファイルを `source` することで代用する。

関数とモジュールは、どちらも「境界を作る」ための道具である。
境界がはっきりしていれば、変更の影響範囲を予測でき、テストも単独で書ける。
境界が曖昧なコードは、一箇所の修正が予期しない場所へ波及する。

---

## 5.2 引数と戻り値

三言語とも、引数には位置引数と名前付き引数がある。

Python:

```python
def classify(usage: float, warn: float = 80.0, crit: float = 90.0) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


result_a = classify(95.0)
result_b = classify(usage=95.0, warn=70.0, crit=85.0)
```

Bash:

```bash
classify() {
  local usage="$1"
  local warn="${2:-80}"
  local crit="${3:-90}"
  if (( usage >= crit )); then
    echo CRITICAL
  elif (( usage >= warn )); then
    echo WARNING
  else
    echo OK
  fi
}

result_a="$(classify 95)"
result_b="$(classify 95 70 85)"
```

Bashの関数は、戻り値として整数の終了コード（`return`）しか返せない。
文字列を返したいときは、標準出力へ `echo` し、呼び出し側でコマンド置換（`$( )`）を使う。
この違いを忘れると、`return "OK"` のような書き方をしてしまい、意図しない終了コードになる。

PowerShell:

```powershell
function Get-UsageStatus {
    param(
        [double]$Usage,
        [double]$Warn = 80,
        [double]$Crit = 90
    )
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}

$resultA = Get-UsageStatus -Usage 95
$resultB = Get-UsageStatus -Usage 95 -Warn 70 -Crit 85
```

PowerShellの関数は、`return` した値だけでなく、パイプラインへ出力した値もすべて戻り値として扱う。
関数内で `Write-Output` や素の式を書くと、呼び出し元には配列として渡ることがある。
デバッグ用の出力を関数内に残すと、戻り値が汚れる原因になる。

```powershell
function Get-UsageStatusBad {
    param([double]$Usage)
    Write-Output "debug: usage=$Usage"
    if ($Usage -ge 90) { return 'CRITICAL' }
    return 'OK'
}

# $status には "debug: usage=95" と "CRITICAL" の配列が入ってしまう
$status = Get-UsageStatusBad -Usage 95
```

デバッグ表示は `Write-Verbose` や `[Console]::Error.WriteLine()` を使い、標準出力（パイプライン）を汚さない。

---

## 5.3 スコープ

**スコープ**は、変数や関数の名前が有効な範囲である。

Python:

```python
warn_default = 80.0


def classify(usage: float) -> str:
    local_note = "temporary"  # この関数の中だけで有効
    if usage >= warn_default:  # 関数の外の変数を読める
        return "WARNING"
    return "OK"


print(local_note)  # NameError: local_note は関数の外から見えない
```

Bashの関数は、既定では変数を共有する。
`local` を付けない限り、関数内の代入がグローバルへ漏れる。

```bash
warn_default=80

classify() {
  local usage="$1"
  # local を付けないと呼び出し元のスコープを汚染する
  note="temporary"
  if (( usage >= warn_default )); then
    echo WARNING
  else
    echo OK
  fi
}

classify 95
echo "${note}"  # local を忘れると呼び出し元に "temporary" が漏れる
```

PowerShellのスコープはやや独特である。
関数内で変数を読むことはできるが、代入は既定で関数ローカルのスコープに作られる。

```powershell
$warnDefault = 80

function Get-UsageStatus2 {
    param([double]$Usage)
    $note = 'temporary'  # 関数ローカル
    if ($Usage -ge $warnDefault) { return 'WARNING' }
    return 'OK'
}

Get-UsageStatus2 -Usage 95 | Out-Null
# $note は呼び出し元には存在しない
```

三言語に共通する方針は、関数の外の変数を暗黙に書き換えないことである。
必要な値は引数として渡し、結果は戻り値として返す。
Bashで `local` を書き忘れないことは、レビューで必ず確認する項目にする。

---

## 5.4 副作用と純粋関数

**副作用**は、関数が戻り値を返す以外に、外部の状態を変更することである。
ファイル書き込み、ネットワーク呼び出し、グローバル変数の変更、標準出力への表示はすべて副作用である。

**純粋関数**は、同じ引数に対して常に同じ結果を返し、副作用を持たない関数である。
純粋関数は、外部環境やタイミングに依存しないため、単体テストが書きやすい。

判定と入出力を一つの関数に混ぜると、テストのたびにファイルやネットワークを用意する必要が出る。

### 悪いコード

```python
from __future__ import annotations

import sys
from pathlib import Path


def check_and_report(usage: float, warn: float, crit: float, report_path: Path) -> int:
    if usage >= crit:
        status = "CRITICAL"
    elif usage >= warn:
        status = "WARNING"
    else:
        status = "OK"

    # 判定とファイル書き込みが同じ関数に混在している
    with report_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{usage},{status}\n")

    if status == "CRITICAL":
        return 3
    return 0
```

問題点:

- `classify` 相当の判定だけを単体テストしたくても、ファイルI/Oが必ず走る
- テストのたびに一時ファイルの後始末が必要になる
- 判定ロジックを他のコマンドから再利用しづらい

### 改善後

```python
from __future__ import annotations

from pathlib import Path


def classify(usage: float, warn: float, crit: float) -> str:
    """純粋関数。I/Oを一切行わない。"""
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


def status_to_exit(status: str) -> int:
    """純粋関数。"""
    return 3 if status == "CRITICAL" else 0


def append_report(report_path: Path, usage: float, status: str) -> None:
    """副作用を持つ関数。ファイルへ追記する。"""
    with report_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{usage},{status}\n")


def check_and_report(usage: float, warn: float, crit: float, report_path: Path) -> int:
    """純粋関数と副作用のある関数を組み合わせる薄い層。"""
    status = classify(usage, warn, crit)
    append_report(report_path, usage, status)
    return status_to_exit(status)
```

`classify` と `status_to_exit` は、引数だけから結果が決まる。
モックもファイルも要らず、値を入れて結果を比べるだけでテストできる。
`append_report` は副作用を持つが、役割が一つに絞られているため、書き込み形式を変えるときもここだけを直せばよい。

Bashでも同じ発想で分ける。

```bash
classify() {
  local usage="$1" warn="$2" crit="$3"
  if (( usage >= crit )); then
    echo CRITICAL
  elif (( usage >= warn )); then
    echo WARNING
  else
    echo OK
  fi
}

append_report() {
  local report_path="$1" usage="$2" status="$3"
  echo "${usage},${status}" >> "${report_path}"
}
```

PowerShellでも同様である。

```powershell
function Get-UsageStatus3 {
    param([double]$Usage, [double]$Warn, [double]$Crit)
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}

function Add-ReportLine {
    param([string]$ReportPath, [double]$Usage, [string]$Status)
    Add-Content -LiteralPath $ReportPath -Value "$Usage,$Status" -Encoding utf8
}
```

判定を純粋関数に、I/Oを別の関数に分けておくと、単体テストの範囲を判定側だけに絞れる。
I/O側は結合テストや実行例で確認する方針にできる（第13章）。

---

## 5.5 モジュール化と名前空間

**名前空間**は、同じ名前の関数や変数が衝突しないように分けるための区画である。

Pythonでは、ファイル（モジュール）やパッケージが名前空間になる。

```python
# hostlib.py
def load_hosts(path):
    ...

# main.py
import hostlib

hosts = hostlib.load_hosts("config/hosts.txt")
```

`import hostlib` としておけば、`hostlib.load_hosts` と他のモジュールの `load_hosts` が衝突しない。
`from hostlib import *` は名前空間を潰してしまうため、運用スクリプトでは避ける。

Bashには名前空間が無い。
関数名がすべて一つのフラットな空間に置かれるため、`source` した複数のファイルで同名関数を定義すると、後から読み込んだ方で上書きされる。

```bash
source lib/hostlib.sh
source lib/disklib.sh
# 両方に classify() があると、後から source した方が有効になる
```

対策として、関数名にプレフィックスを付ける運用が現実的である。

```bash
hostlib::load_hosts() { ... }
disklib::classify() { ... }
```

PowerShellのモジュール（`.psm1`）は、既定でエクスポートした関数だけを呼び出し元の名前空間に見せる。

```powershell
# HostLib.psm1
function Get-Hosts {
    param([string]$Path)
    Get-Content -LiteralPath $Path | Where-Object { $_ -and -not $_.StartsWith('#') }
}

Export-ModuleMember -Function Get-Hosts
```

```powershell
Import-Module ./HostLib.psm1
Get-Hosts -Path config/hosts.txt
```

`Export-ModuleMember` を書かないと、モジュール内のすべての関数が公開される。
内部だけで使う補助関数は、意図してエクスポートから外す。

---

## 5.6 責務分離と分割の判断基準

**責務**は、そのコードが担う一つの役割である。

一つの関数やモジュールに複数の責務が混ざると、片方の都合の変更がもう片方を壊す。

分割すべきかどうかを、次の基準で判断する。

1. 同じ処理が二箇所以上に現れている、または現れそうである
2. 名前を付けたほうが、呼び出し側のコードが読みやすくなる
3. 単体でテストしたい処理である
4. 外部I/O（ファイル、ネットワーク、外部コマンド）と、判定や計算が混在している
5. 一つの関数の行数が、画面をスクロールしないと読めない長さになっている
6. 関数名に「and」が要る（例: `load_and_validate_and_report`）

6番目の兆候が出たら、関数を分ける具体的な合図である。
`load_and_validate_and_report` は、`load`、`validate`、`report` の三つに分けられる。

過剰分割にも注意する。
一度しか呼ばれず、内容が数行で、単体テストの必要も薄い処理まで無理に切り出すと、呼び出しをたどるだけで時間を取られる。
分割の目的は行数の削減ではなく、読解とテストの単位を明確にすることである。

---

## 5.7 Pythonのモジュール

Pythonでは、ファイルがそのままモジュールになる。

```text
project/
  opsctl/
    __init__.py
    hostlib.py
    disklib.py
  main.py
```

```python
# opsctl/hostlib.py
from __future__ import annotations

from pathlib import Path


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        hosts.append(line)
    return hosts
```

```python
# main.py
from __future__ import annotations

import sys
from pathlib import Path

from opsctl.hostlib import load_hosts


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    hosts = load_hosts(Path(args[0]))
    print(len(hosts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`__init__.py` を置くと `opsctl` がパッケージとして扱われ、`from opsctl.hostlib import load_hosts` のように階層を持ったモジュール構成にできる。
テストからも同じ書き方で `import` できるため、第13章のテストと相性がよい。

相対importと絶対importが混在すると、実行方法（`python main.py` か `python -m opsctl.main` か）によって壊れることがある。
運用スクリプトでは絶対import（`from opsctl.hostlib import ...`）を基本にし、実行はパッケージのルートから行う。

---

## 5.8 Bashの関数

Bashの関数定義は二通りの書き方があるが、意味は同じである。

```bash
function greet {
  echo "hello, $1"
}

greet2() {
  echo "hello, $1"
}
```

本書では `name() { ... }` の形式に統一する。
`function` キーワードは省略しても動くため、記述を減らせる。

関数を別ファイルへ分け、`source` で読み込むと、Bashなりのモジュール化ができる。

```bash
# lib/hostlib.sh
hostlib::load_hosts() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "hosts file not found: ${path}" >&2
    return 1
  fi
  grep -v '^\s*#' "${path}" | grep -v '^\s*$'
}
```

```bash
#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/hostlib.sh"

hosts="$(hostlib::load_hosts config/hosts.txt)"
echo "${hosts}" | wc -l
```

`source` するパスは、実行時のカレントディレクトリに依存させない。
`BASH_SOURCE[0]` からスクリプト自身の場所を求め、そこからの相対パスで `lib/` を指す。

Bashの関数は、`local` を付けた変数以外はすべてグローバルになる。
第4章までの規約と同様、関数の先頭で受け取る引数を `local` 変数に写してから使うと、事故が減る。

---

## 5.9 PowerShellの関数とモジュール

PowerShellの関数は、`param()` ブロックで型付きの引数を受け取れる。

```powershell
function Get-DiskStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [double]$Usage,

        [double]$Warn = 80,
        [double]$Crit = 90
    )

    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}
```

`[CmdletBinding()]` を付けると、`-Verbose` や `-ErrorAction` など共通パラメータが自動的に使えるようになる。
関数名は動詞-名詞の形式（`Get-DiskStatus` など）にするのがPowerShellの慣例であり、`Get-Verb` で承認済みの動詞一覧を確認できる。

モジュール化には `.psm1` ファイルを使う。

```powershell
# modules/HostLib.psm1
function Get-HostList {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "hosts file not found: $Path"
    }
    Get-Content -LiteralPath $Path |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -and -not $_.StartsWith('#') }
}

Export-ModuleMember -Function Get-HostList
```

```powershell
Import-Module (Join-Path $PSScriptRoot 'modules/HostLib.psm1') -Force

$hosts = Get-HostList -Path 'config/hosts.txt'
Write-Output $hosts.Count
```

`$PSScriptRoot` は、実行中のスクリプトファイルが置かれているディレクトリを指す組み込み変数である。
これを基準にモジュールを読み込むと、カレントディレクトリに依存しない。

`Import-Module` に `-Force` を付けると、開発中にモジュールを編集したあとの再読み込みが確実になる。
本番運用では、意図しないバージョンでの上書きを避けるため、モジュールのバージョン管理も検討する。

---

## 5.10 実務向けサンプル: ディスク監視ロジックの関数分割

要件は第2章、第4章のディスク監視と同じ判定を使う。
ここでは、責務ごとに関数を分けたPython実装を示す。

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CRITICAL = 3

logger = logging.getLogger("disk_report")


@dataclass
class HostUsage:
    host: str
    usage_percent: float


def load_usages(path: Path) -> list[HostUsage]:
    """副作用: ファイル読み込み。"""
    if not path.is_file():
        raise FileNotFoundError(f"usage file not found: {path}")
    usages: list[HostUsage] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            usages.append(HostUsage(host=row["host"], usage_percent=float(row["usage_percent"])))
    return usages


def classify(usage_percent: float, warn: float, crit: float) -> str:
    """純粋関数。"""
    if usage_percent >= crit:
        return "CRITICAL"
    if usage_percent >= warn:
        return "WARNING"
    return "OK"


def summarize_exit_code(statuses: list[str]) -> int:
    """純粋関数。"""
    if "CRITICAL" in statuses:
        return EXIT_CRITICAL
    return EXIT_OK


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    """副作用: ファイル書き込み。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "usage_percent", "status"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify disk usage and write a report")
    parser.add_argument("--input", type=Path, required=True, help="host,usage_percent CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warn", type=float, default=80.0)
    parser.add_argument("--crit", type=float, default=90.0)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if args.warn > args.crit:
        logger.error("--warn must be <= --crit")
        return EXIT_USAGE

    try:
        usages = load_usages(args.input)
    except (OSError, ValueError, KeyError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    rows: list[dict[str, str]] = []
    statuses: list[str] = []
    for item in usages:
        status = classify(item.usage_percent, args.warn, args.crit)
        statuses.append(status)
        rows.append(
            {
                "host": item.host,
                "usage_percent": str(item.usage_percent),
                "status": status,
            }
        )

    write_report(args.output, rows)
    logger.info("wrote %s rows to %s", len(rows), args.output)
    return summarize_exit_code(statuses)


if __name__ == "__main__":
    sys.exit(main())
```

`load_usages` と `write_report` はI/Oを持つ関数、`classify` と `summarize_exit_code` は純粋関数として明確に分かれている。
`main` は、それらを順番に呼び出す薄い調整役に徹している。

完全な実行可能ファイルは `samples/python/05_disk_report.py` に置く。
対応するBash版は `samples/bash/05_disk_report.sh`、PowerShell版は `samples/powershell/05_disk_report.ps1` を参照する。

---

## 5.11 セキュリティ上の注意点

- 関数の引数に秘密情報（トークン、パスワード）を渡すときは、ログ関数や例外メッセージにそのまま埋め込まない
- Bashで `source` するファイルパスを利用者入力から組み立てない。任意のファイルを読み込ませる経路になる
- PowerShellの `Import-Module` にも同様の注意が要る。信頼できないパスからモジュールを読み込まない
- 副作用を持つ関数（削除、上書き、外部API呼び出し）は名前や配置を分け、レビューで見つけやすくする
- モジュール分割によって「どこかで検証しているはず」という思い込みが生まれやすい。入力検証の責務がどの関数にあるかをコメントや設計で明示する

---

## 5.12 テスト方法

純粋関数はテストしやすい。

```python
import pytest

from samples.python.disk_report import classify, summarize_exit_code


@pytest.mark.parametrize(
    ("usage", "expected"),
    [(79.9, "OK"), (80.0, "WARNING"), (90.0, "CRITICAL")],
)
def test_classify(usage: float, expected: str) -> None:
    assert classify(usage, warn=80.0, crit=90.0) == expected


def test_summarize_exit_code_critical() -> None:
    assert summarize_exit_code(["OK", "CRITICAL", "WARNING"]) == 3


def test_summarize_exit_code_ok() -> None:
    assert summarize_exit_code(["OK", "WARNING"]) == 0
```

副作用を持つ関数は、一時ディレクトリを使って結合的にテストする。

```python
from pathlib import Path

from samples.python.disk_report import load_usages, write_report


def test_load_and_write_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "in.csv"
    src.write_text("host,usage_percent\nweb01.example.invalid,95\n", encoding="utf-8")

    usages = load_usages(src)
    assert usages[0].host == "web01.example.invalid"

    out = tmp_path / "out.csv"
    write_report(out, [{"host": "web01.example.invalid", "usage_percent": "95", "status": "CRITICAL"}])
    assert out.exists()
```

Bashの関数は、`source` してから直接呼び出してテストできる。

```bash
source samples/bash/05_disk_report.sh

result="$(classify 95 80 90)"
[[ "${result}" == "CRITICAL" ]] || { echo "test failed: ${result}" >&2; exit 1; }
echo "ok"
```

PowerShellでは、関数定義部分だけをドットソース（`. path`）で読み込み、Pesterでテストする。

```powershell
BeforeAll {
    . (Join-Path $PSScriptRoot '../samples/powershell/05_disk_report.ps1') -TestMode
}

Describe 'Get-DiskStatus' {
    It 'returns CRITICAL at threshold' {
        Get-DiskStatus -Usage 90 -Warn 80 -Crit 90 | Should -Be 'CRITICAL'
    }
}
```

`-TestMode` は、スクリプト本体（`main`相当の実行部）を止め、関数定義だけを読み込むための独自スイッチである。
テストから読み込まれるスクリプトには、この種の「実行を止める入口」を用意しておくと、ドットソースでも安全に関数だけを取り出せる。

---

## 章末問題

1. 「純粋関数」と「副作用のある関数」を、それぞれ運用スクリプトの具体例で一つずつ挙げよ。
2. Bashの関数で `local` を付け忘れたときに起きる事故を、変数名の衝突を例に説明せよ。
3. PowerShellの関数内で `Write-Output` をデバッグ目的に残してしまうと何が起きるか説明せよ。
4. 「関数名に `and` が要る」状態を解消する分割案を、任意の処理を例に書け。
5. Pythonのモジュールを `from module import *` で読み込むことの問題点を二つ挙げよ。

## 解答と解説

1. 純粋関数の例: 使用率としきい値からステータス文字列を返す判定関数。副作用のある関数の例: レポートファイルへ追記する関数。
2. 呼び出し元や他の関数が同名の変数を使っていた場合、意図せず値が上書きされる。原因の特定に時間がかかる。
3. 関数の戻り値に、デバッグ用の出力とパイプラインの本来の戻り値が混ざって配列になる。呼び出し元のロジックが壊れる。
4. 例: `load_and_validate_and_report(path)` を `load(path)`、`validate(data)`、`report(data)` の三関数に分ける。
5. どの名前がどのモジュール由来か分からなくなる。同名の関数や変数が衝突しても気づきにくい。

---

## 実装演習

1. `05_disk_report.py` の `load_usages` と `write_report` を、モックを使わずに一時ディレクトリでテストするコードを書け。
2. Bashで `lib/hostlib.sh` を作り、`hostlib::load_hosts` を別スクリプトから `source` して呼び出せ。
3. PowerShellで `HostLib.psm1` を作り、`Export-ModuleMember` で公開する関数と、公開しない補助関数を最低一つずつ用意せよ。
4. 自分が最近書いたスクリプトから、10行を超える関数を一つ選び、責務ごとに二つ以上へ分割せよ。

---

## 次章予告

第6章では、ファイルの読み書きと安全な更新を扱う。
文字コードと改行を意識したテキスト処理、バックアップしてから変更する手順、ロックを使った競合回避を三言語で実装する。
