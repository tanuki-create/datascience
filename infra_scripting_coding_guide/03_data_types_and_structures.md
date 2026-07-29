# 第3章 データ型とデータ構造

## 学習目標

この章を終えると、次ができるようになる。

- Python、Bash、PowerShellの基本型の違いを説明できる
- 文字列、数値、真偽、配列、辞書、null相当を用途に応じて選べる
- 文字コードと改行を意識してテキストを扱える
- JSON / CSV を読み書きし、YAMLの位置づけを説明できる

前提: 第1章〜第2章の入出力と問題分解。

サンプルコードは学習用である。本番の文字コードやロケールは対象システムで確認すること。

---

## 3.1 基本概念

**データ型**は、値がどのような種類かを示す分類である。

**データ構造**は、複数の値をどう束ねるかを示す形である。

スクリプトでは、OSコマンドやファイルが返す「文字列」を、必要なら数値や構造化データへ変換する。変換を省略すると、`"10"` と `10` の比較ミスや、CSVの列ずれが起きる。

---

## 3.2 文字列

| 言語 | 型の呼び方 | 主な特徴 |
|------|------------|----------|
| Python | `str` | Unicode文字列。スライスやメソッドが豊富 |
| Bash | 文字列が基本 | 型宣言がほぼ無い。引用符が安全の要 |
| PowerShell | `System.String` | .NET文字列。単一/二重引用符で展開が異なる |

Python:

```python
host = "web01.example.invalid"
assert host.startswith("web")
assert host.split(".")[0] == "web01"
```

Bash:

```bash
host="web01.example.invalid"
prefix="${host%%.*}"
echo "${prefix}"   # web01
# 必ず引用する
echo "${host}"
```

PowerShell:

```powershell
$hostName = 'web01.example.invalid'
$hostName.Split('.')[0]   # web01
```

PowerShellの二重引用符は変数展開する。意図しない展開を避けるなら単一引用符を使う。

---

## 3.3 整数と小数

| 言語 | 整数 | 小数 |
|------|------|------|
| Python | `int`（桁数制限が実質ゆるい） | `float`（IEEE754）、正確さが要るなら `decimal` |
| Bash | 算術展開 `$(( ))` は整数 | 小数は `bc` や外部へ委譲することが多い |
| PowerShell | `[int]`, `[long]` など | `[double]`, `[decimal]` |

Python:

```python
used = 85
total = 100
percent = used / total * 100
assert percent == 85.0
```

Bash（整数パーセント）:

```bash
used=85
total=100
percent=$(( used * 100 / total ))
echo "${percent}"
```

PowerShell:

```powershell
[double]$used = 85
[double]$total = 100
$percent = $used / $total * 100
```

ディスク使用率のような閾値判定は、最初から整数パーセントに揃えると三言語で比較が安定する。

---

## 3.4 真偽値

| 言語 | 真 / 偽 | 注意 |
|------|---------|------|
| Python | `True` / `False` | 空文字、空リスト、0は偽と評価される |
| Bash | コマンドの終了コード0が成功 | 文字列 `true` はただの文字列 |
| PowerShell | `$true` / `$false` | 多くの値が真偽に変換されうる |

Bashで真偽を変数に持つなら、`0`/`1` か `yes`/`no` を決め、文字列比較する。

```bash
dry_run=1
if [[ "${dry_run}" -eq 1 ]]; then
  echo "dry-run" >&2
fi
```

---

## 3.5 配列、リスト

| 言語 | 代表 | 特徴 |
|------|------|------|
| Python | `list` | 可変、異型要素可。順序あり |
| Bash | 配列 `arr=(a b)` | 単語分割と引用が難しい |
| PowerShell | `Object[]` / `List` | パイプラインと相性が良い |

Python:

```python
hosts = ["web01.example.invalid", "web02.example.invalid"]
hosts.append("db01.example.invalid")
```

Bash:

```bash
hosts=("web01.example.invalid" "web02.example.invalid")
hosts+=("db01.example.invalid")
for host in "${hosts[@]}"; do
  echo "${host}"
done
```

PowerShell:

```powershell
$hosts = @('web01.example.invalid', 'web02.example.invalid')
$hosts += 'db01.example.invalid'
```

Bashで `for host in $(cat file)` は使わない。第1章の `while read` を使う。

---

## 3.6 辞書、ハッシュテーブル

| 言語 | 代表 | 用途 |
|------|------|------|
| Python | `dict` | 設定、集計、JSONとの相互変換 |
| Bash | 連想配列 `declare -A`（Bash 4+） | 簡易マップ。複雑ならPythonへ |
| PowerShell | `hashtable` `@{ }` | 設定とJSON変換 |

Python:

```python
thresholds = {"warn": 80, "crit": 90}
assert thresholds["warn"] == 80
```

Bash 4+:

```bash
declare -A thresholds=([warn]=80 [crit]=90)
echo "${thresholds[warn]}"
```

PowerShell:

```powershell
$thresholds = @{ warn = 80; crit = 90 }
$thresholds['warn']
```

macOSの古いBash 3.xでは連想配列が使えない。可搬性が要るならPythonかPowerShell 7へ寄せる。

---

## 3.7 null相当値

| 言語 | 無いことを表す値 | 判定 |
|------|------------------|------|
| Python | `None` | `is None` |
| Bash | 空文字、未設定変数 | `${var:-}`, `[[ -z ]]`。`set -u` 下では未設定参照がエラー |
| PowerShell | `$null` | `$null -eq $value` |

取得失敗を `0` と表現しない。使用率0%と取得失敗が区別できなくなる。

```python
usage: float | None
if usage is None:
    status = "ERROR"
```

---

## 3.8 型変換

明示変換を基本にする。

Python:

```python
percent = int(float("85.7"))  # 85
```

Bash:

```bash
n="42"
expr=$(( n + 1 ))
```

PowerShell:

```powershell
[int]'42' + 1
[double]'85.7'
```

悪い例（暗黙依存）:

```python
# "90" >= 80 は Python 3 では TypeError
# 古い感覚や他言語の癖で書いてしまう
```

改善:

```python
if int(value) >= 80:
    ...
```

---

## 3.9 文字コード

**文字コード**は、文字をバイト列へ対応づける規則である。現代の既定は UTF-8 が多い。

事故例:

- WindowsのCP932（Shift_JIS系）のログを、UTF-8前提で読む
- 赤シートが `���` になる
- ある1行だけ壊れてCSV全体が読えない

方針:

1. 入出力の encoding を明示する（Pythonは `encoding="utf-8"`）
2. 既存ログのコードページを調べてから読む
3. 新規成果物はUTF-8（必要ならBOM付きを相手に合わせる）

Python:

```python
text = path.read_text(encoding="utf-8")
path.write_text(text, encoding="utf-8", newline="\n")
```

PowerShell 7:

```powershell
Get-Content -LiteralPath $path -Encoding utf8
Set-Content -LiteralPath $path -Value $text -Encoding utf8
```

Windows PowerShell 5.1の `Set-Content` 既定はUTF-8と限らない。本書は PowerShell 7 を主とし、5.1では `-Encoding` を明示する。

---

## 3.10 日付と時刻

運用では「いつ」が監査と期限判定の中心になる。

推奨:

- 内部計算はUTCまたはモノトニック時計
- 表示はISO 8601（例: `2026-07-30T04:09:00+09:00`）
- タイムゾーンを省略した文字列をサーバ間で共有しない

Python:

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
print(now.isoformat())
```

Bash（GNU date）:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

macOSの `date` はGNUとフラグが違う。可搬な日付処理はPythonが安全である。

PowerShell:

```powershell
[DateTimeOffset]::UtcNow.ToString('o')
```

証明書期限などは第15章で扱う。

---

## 3.11 JSON

**JSON**は、オブジェクトと配列をテキストで表す共通形式である。API連携の標準に近い。

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def main() -> int:
    path = Path(sys.argv[1])
    try:
        data = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 2
    print(data.get("defaults", {}).get("timeout_seconds"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

PowerShell:

```powershell
$data = Get-Content -LiteralPath .\config\sample.json -Raw | ConvertFrom-Json
$data.defaults.timeout_seconds
```

Bashは `jq` を使う。

```bash
jq -r '.defaults.timeout_seconds' config/sample.json
```

`jq` が無い環境では Python に寄せる。

---

## 3.12 CSV

**CSV**は表形式のテキストである。报表や棚卸しに向く。

注意:

- カンマや改行を含むフィールドは引用符が必要
- 自前の `split(",")` は壊れる
- 言語標準のCSVライブラリを使う

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    out = Path(sys.argv[1])
    rows = [
        {"host": "web01.example.invalid", "status": "OK", "detail": "85"},
        {"host": "web02.example.invalid", "status": "CRITICAL", "detail": "95"},
    ]
    write_report(out, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

PowerShell:

```powershell
$rows = @(
  [pscustomobject]@{ host = 'web01.example.invalid'; status = 'OK'; detail = '85' }
  [pscustomobject]@{ host = 'web02.example.invalid'; status = 'CRITICAL'; detail = '95' }
)
$rows | Export-Csv -LiteralPath .\reports\disk.csv -NoTypeInformation -Encoding utf8
```

---

## 3.13 YAMLの概要

**YAML**は設定ファイルでよく使う、インデント基調の形式である。

長所: 人が読みやすい。コメントが書ける。

短所: 暗黙型変換やアンカーなど、罠がある。`YES`/`NO` が真偽になる歴史的問題など、実装依存に注意する。

Python（PyYAML）:

```python
import yaml
from pathlib import Path

data = yaml.safe_load(Path("config/opsctl.yaml").read_text(encoding="utf-8"))
timeout = data["defaults"]["timeout_seconds"]
```

`yaml.load` ではなく **`safe_load`** を使う。任意コード実行のリスクを避けるためである。

PowerShellでは `powershell-yaml` モジュールや、設定をJSONに寄せる選択がある。本書の `opsctl` 設定はYAMLとし、読み込みはPythonを主とする。

BashでYAMLを本格処理しない。`yq` がある場合のみ補助的に使う。

---

## 3.14 最小構成から実務へ

### 悪いコード

```bash
# 自前CSV、文字コード無視、型なし
echo $host,$usage >> report.csv
```

問題点:

- フィールドにカンマがあると列が壊れる
- 文字コードと改行が環境依存
- ヘッダー欠落や追記競合

### 改善後（Pythonで安全にCSV）

`samples/python/03_write_status_csv.py` を参照。

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

logger = logging.getLogger("write_status_csv")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write status CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--status", required=True, choices=["OK", "WARNING", "CRITICAL", "ERROR"])
    parser.add_argument("--detail", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(message)s")

    if any(ch.isspace() for ch in args.host):
        logger.error("host must not contain whitespace")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.output.exists()
    with args.output.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "status", "detail"])
        if write_header:
            writer.writeheader()
        writer.writerow(
            {"host": args.host, "status": args.status, "detail": args.detail}
        )

    logger.info("appended row to %s", args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

並列追記ではファイルロックが必要になる（第6章）。単一プロセス追記に限定する。

---

## 3.15 セキュリティ上の注意点

- YAMLの危険なタグや `!!python/object` を有効にしない（`safe_load`）
- 利用者入力をJSONに埋め込むとき、文字列連結ではなくライブラリのシリアライズを使う
- CSVインジェクション（セル先頭の `=` など）が表計算ソフトで問題になる場合がある。外部公開レポートではサニタイズ方針を決める

---

## 3.16 テスト方法

```python
import json
from pathlib import Path


def test_json_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    path.write_text(json.dumps({"defaults": {"timeout_seconds": 30}}), encoding="utf-8")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["defaults"]["timeout_seconds"] == 30
```

文字コードテストでは、意図的に不正UTF-8を渡し、例外または置換方針を固定する。

---

## 章末問題

### 問題1

Bashで小数のディスク使用率を直接比較するのが難しい理由と、代替を二つ述べよ。

### 問題2

`None` / 空文字 / `0` を混同すると起きる運用事故を一つ具体的に書け。

### 問題3

次のCSV行を自前splitするとどう壊れるか説明せよ。

```text
web01,"disk full, needs cleanup",CRITICAL
```

### 問題4

PowerShell 5.1と7でファイル書き込みの文字コードに差が出る理由を述べよ。

### 問題5

設定にYAMLを選ぶ理由と、JSONを選ぶ理由をそれぞれ一つずつ書け。

---

## 解答と解説

### 問題1

`$(( ))` が整数だから。代替: 整数パーセントに丸める、`bc`、Python/PowerShellへ処理を移す。

### 問題2

ディスク取得失敗を0%と記録し、正常と誤認してアラートが出ない。

### 問題3

カンマが列区切りとフィールド内の両方に現れ、列数がずれる。

### 問題4

既定エンコーディングの歴史的差がある。`-Encoding` を明示し、可能ならPowerShell 7に揃える。

### 問題5

YAML: コメントと人が読む設定向き。JSON: 型が単純でツール共通、コメント不要な機械生成向き。

---

## 実装演習

### 演習A

`config/opsctl.yaml` を読み、`defaults.timeout_seconds` をstdoutへ出すPythonスクリプトを書け。失敗時は終了コード2。

### 演習B

ホストと使用率の組を受け取り、CSVを書くPowerShellスクリプトを書け。UTF-8を明示すること。

### 演習C

不正なUTF-8バイトを含むファイルを用意し、Pythonで `errors="strict"` と `errors="replace"` の差を観察せよ。運用ではどちらを選ぶか理由を書け。

---

## 次章予告

第4章では、条件分岐と反復を読みやすく保つ技法（早期リターン、異常系先行）を三言語で扱う。
