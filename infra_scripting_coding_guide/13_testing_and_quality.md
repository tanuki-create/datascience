# 第13章 テストと品質管理

## 学習目標

- テストの目的を説明し、ユニットテストと結合テストを使い分けられる
- 正常系・異常系・境界値の観点で、テストケースを漏れなく設計できる
- モックを使い、外部依存（ネットワーク、外部コマンド、時間）を切り離してテストできる
- pytest、Pester、Bashそれぞれでテストを書き、実行できる
- 型ヒント、lint、フォーマッターを使い、実行前に問題を検出できる
- コードレビューの観点を説明し、CIにテストと静的解析を組み込める

前提: 第1章（終了コード）、第7章（外部コマンド実行）、第8章（例外処理）、第12章（CLI設計）。

サンプルコードは学習用である。
本番のCIパイプラインやカバレッジ目標は、対象チームの品質基準に合わせて調整すること。

---

## 13.1 基本概念

**テスト**は、コードが期待どおりに動くことを、実行して確認する作業である。

インフラ運用スクリプトは、次の理由で特にテストの価値が高い。

- 対象が本番サーバーやネットワーク機器であり、誤動作の影響が大きい
- 削除、上書き、再起動のような破壊的操作を含むことが多く、手動確認だけでは危険が残る
- 定期実行や自動化の一部に組み込まれ、人が毎回結果を見るとは限らない
- 一度書いたら長く使われがちで、書いた本人以外が後から手を入れる

テストが無いコードを変更すると、次のいずれかになりやすい。

1. 変更のたびに手動で全パターンを再確認する（時間がかかり、確認漏れが起きる）
2. 確認を省略して変更を入れる（退行、いわゆるデグレを見逃す）

自動テストは、この二択を避け、変更のたびに機械的に同じ確認を再実行する手段である。

テストには、大きく分けて次の目的がある。

| 目的 | 説明 |
|------|------|
| 正しさの確認 | 実装した処理が仕様どおりに動くことを確認する |
| 退行の防止 | 既存の挙動を壊していないことを、変更のたびに確認する |
| 仕様の明文化 | テストコード自体が「この関数はこう動くべき」という仕様書になる |
| 設計の検証 | テストしにくいコードは、責務が混ざっているサインであることが多い（第5章、第14章） |
| 安心して変更する土台 | リファクタリング（第14章）を、挙動を変えずに進められる根拠になる |

---

## 13.2 ユニットテストと結合テスト

**ユニットテスト**は、関数やクラスなど、コードの最小単位を対象に、他の部分から切り離して検証するテストである。

**結合テスト**は、複数の部品を組み合わせた状態で、部品間の連携を含めて検証するテストである。

| 観点 | ユニットテスト | 結合テスト |
|------|-----------------|-------------|
| 対象範囲 | 1つの関数・クラス | 複数の関数・モジュール・外部システムとの連携 |
| 実行速度 | 速い（ミリ秒単位） | 遅くなりやすい（I/Oを含むため） |
| 外部依存 | モックで切り離すことが多い | 一部、または全部を実物に近い形で使う |
| 見つけやすい不具合 | ロジックの誤り、境界値の誤り | インターフェースの不一致、設定ミス、環境差異 |
| 失敗時の特定しやすさ | 高い（対象が狭い） | 低くなりやすい（原因箇所の絞り込みが必要） |

`opsctl` の `disk-check` 相当の機能を例にすると、次のように対応する。

| テスト対象 | 分類 |
|------------|------|
| `classify_disk_usage`（閾値判定だけ） | ユニットテスト |
| `parse_df_output`（テキスト解析だけ） | ユニットテスト |
| `fetch_disk_report`（外部コマンド呼び出し + パース） | 結合テスト（外部コマンドはモックすることが多い） |
| CLI全体（引数解析 + 収集 + 分類 + 出力） | 結合テスト |

両方が必要である。
ユニットテストだけでは、部品同士の繋ぎ込みの誤りを見逃す。
結合テストだけでは、実行が遅く、失敗時にどの部品が原因か特定しにくい。
一般に、ユニットテストを土台に多く持ち、結合テストで主要な経路を絞って確認する構成にする。

---

## 13.3 正常系・異常系・境界値

テストケースを考えるときは、次の3つの観点で漏れを確認する。

| 観点 | 意味 | 例（ディスク使用率の分類） |
|------|------|------------------------------|
| 正常系 | 想定どおりの入力で、期待どおりの結果になることを確認する | 使用率50%で`ok`になる |
| 異常系 | 不正な入力やエラー状態で、適切にエラー処理されることを確認する | 使用率が101%のとき例外を送出する |
| 境界値 | 判定が切り替わる値のちょうど上下を確認する | 使用率が閾値と同じ80%のとき`warning`になるか |

**境界値**を狙ったテストは特に重要である。
「80%を超えたら警告」なのか「80%以上で警告」なのかは、実装によって揺れやすく、
`>` と `>=` の取り違え（いわゆるoff-by-oneエラー）は典型的なバグの温床である。

境界値のテストは、次の3点をセットで確認するとよい。

1. 閾値のすぐ下（例: 79%） → 変化する前の状態
2. 閾値ちょうど（例: 80%） → 仕様上どちらに転ぶかを明確にする値
3. 閾値のすぐ上（例: 81%） → 変化した後の状態

さらに、値の取りうる範囲の両端（最小値、最大値、0、空文字列、空リストなど）も境界値の一種である。

| 種類 | 例 |
|------|-----|
| 数値の下限・上限 | 0%、100%、負の値 |
| 文字列の空 | 空文字列、空白のみの文字列 |
| コレクションの空・単数・複数 | 空リスト、要素1件、要素多数 |
| 個数の限界 | 上限ちょうどの件数、上限+1件 |

---

## 13.4 テストデータとフィクスチャ

**テストデータ**は、テストの入力として使う、あらかじめ用意した値である。

**フィクスチャ**は、テストの実行前に用意し、実行後に片付ける、テストに必要な準備一式（データ、リソース、モック）を指す。
pytestでは `@pytest.fixture` で定義した関数や、`tmp_path`・`capsys`・`monkeypatch` のような組み込みフィクスチャを使う。

テストデータを選ぶときの方針:

- 本物のホスト名やIPアドレスを使わない。第1章以降のサンプルと同様に `example.invalid` のような予約ドメインを使う
- ランダムなテストデータは再現性を損なう。失敗したときに同じ入力で再実行できることを優先し、固定値を使う
- 境界値・異常系を明示的にカバーする値を用意する。「たまたま通った」ではなく「この値を狙って確認した」と分かる名前や配置にする
- 大きすぎるテストデータは避ける。読む人が意図を追えるサイズに留める

```python
# 固定のテストデータ（df -P 相当の出力）。
# ホスト名やパスは実在しない値（.invalid）を使う。
SAMPLE_DF_OUTPUT = """Filesystem     1024-blocks     Used Available Capacity Mounted on
/dev/sda1         51475068 42787876   6045808      88% /
/dev/sda2        104845292 34567890  65432100      35% /var
/dev/sda3         20971520 19951616    524288      98% /data
"""
```

pytestの組み込みフィクスチャのうち、運用スクリプトのテストで頻繁に使うものを挙げる。

| フィクスチャ | 用途 |
|--------------|------|
| `tmp_path` | テスト専用の一時ディレクトリを提供する。実ファイルへの副作用を避ける |
| `capsys` | 標準出力・標準エラーをキャプチャする。CLIの出力検証に使う |
| `monkeypatch` | 環境変数、属性、関数を一時的に差し替える。テスト終了時に自動で元に戻る |
| `caplog` | ログ出力をキャプチャする。第9章のログ検証に使う |

`tmp_path` を使うと、テストごとに独立したディレクトリが払い出されるため、
複数のテストが同じ固定パス（例: `/tmp/report.txt`）を取り合って干渉する事故を防げる。

---

## 13.5 モック

**モック**は、テスト対象が依存する外部の部品を、制御可能な偽物に置き換える技法である。

モックを使う代表的な対象:

| 対象 | 理由 |
|------|------|
| ネットワーク呼び出し（`requests`、`Invoke-RestMethod`など） | 実際のAPIを毎回叩くと遅く、不安定で、相手側への負荷にもなる |
| 外部コマンド実行（`subprocess.run`、`ssh`など） | 対象ホストが無くてもロジックを検証したい |
| 時間（`time.sleep`、現在時刻） | 待機時間や日付依存の分岐を、実時間を待たずに検証したい（第8章のリトライテスト） |
| ファイルシステム | 実ファイルを汚さずに、様々な入力パターンを試したい（`tmp_path`で代替できる場合はそちらを優先する） |

Pythonでは、`unittest.mock` と、pytestの `monkeypatch` フィクスチャの両方が使える。
`monkeypatch` は、テスト終了時に自動で元の状態へ戻すため、後始末を書き忘れるリスクが低く、本書では基本的にこちらを使う。

```python
import subprocess

import pytest


def run_uptime() -> str:
    completed = subprocess.run(["uptime"], capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def test_run_uptime_returns_stdout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, returncode=0, stdout="up 3 days\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert run_uptime() == "up 3 days"
```

モックを使う際の注意点:

- **モックしすぎない**。全部をモックすると、テストは通っても実際の結合部分の不具合を見逃す。外部I/Oの境界線だけをモックし、自前のロジックは実物のまま通す
- **モック対象のインターフェースを正しく再現する**。実物と異なる形の偽物を作ると、テストは通るのに本番で壊れる「偽陽性」が起きる
- **依存性注入で置き換えられる場合は、それを優先する**。13.15節で示すように、外部依存を引数として受け取る設計にしておくと、モジュールの内部をパッチ（monkeypatch）せずにテストできる

---

## 13.6 pytestの基本

**pytest**は、Pythonの標準的なテストフレームワークである。
`assert` 文だけでテストを書け、実行結果を分かりやすく表示する。

規約:

- テストファイル名は `test_*.py` または `*_test.py`
- テスト関数名は `test_` で始める
- 各テストは `assert` で期待値を検証する。専用のアサーションメソッドは不要

```python
def add(a: int, b: int) -> int:
    return a + b


def test_add_returns_sum_of_two_numbers() -> None:
    assert add(2, 3) == 5


def test_add_handles_negative_numbers() -> None:
    assert add(-1, 1) == 0
```

実行:

```bash
pytest                       # カレントディレクトリ以下のテストをすべて実行
pytest tests/test_foo.py     # 特定のファイルだけ実行
pytest -k "boundary"         # 名前に"boundary"を含むテストだけ実行
pytest -v                    # テストごとの結果を詳細表示
pytest -x                    # 最初の失敗で打ち切る
pytest --maxfail=3           # 3件失敗したら打ち切る
```

**パラメトライズ**（`@pytest.mark.parametrize`）を使うと、同じ検証ロジックを複数の入力値に対して繰り返せる。
境界値テスト（13.3節）と特に相性がよい。

```python
import pytest


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (79, "ok"),
        (80, "warning"),
        (89, "warning"),
        (90, "critical"),
    ],
)
def test_classify_boundaries(value: int, expected: str) -> None:
    assert classify_disk_usage(value, warn_percent=80, crit_percent=90) == expected
```

異常系は `pytest.raises` で、送出される例外の型（と必要ならメッセージ）を検証する。

```python
import pytest


def test_classify_rejects_inverted_thresholds() -> None:
    with pytest.raises(InvalidThresholdError):
        classify_disk_usage(85, warn_percent=90, crit_percent=80)
```

設定は `pyproject.toml` に置ける。

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
```

---

## 13.7 最小構成のコード

テスト対象とテストの最小構成を示す。

```python
"""minimal_example.py: テスト対象の最小関数。"""
from __future__ import annotations


def is_valid_percent(value: float) -> bool:
    """0以上100以下ならTrueを返す。"""
    return 0 <= value <= 100
```

```python
"""test_minimal_example.py: 最小構成のテスト。"""
from minimal_example import is_valid_percent


def test_is_valid_percent_true_for_normal_value() -> None:
    assert is_valid_percent(50) is True


def test_is_valid_percent_false_for_negative_value() -> None:
    assert is_valid_percent(-1) is False


def test_is_valid_percent_true_at_lower_bound() -> None:
    assert is_valid_percent(0) is True


def test_is_valid_percent_true_at_upper_bound() -> None:
    assert is_valid_percent(100) is True
```

`pytest` をこのディレクトリで実行すると、4件のテストがすべて成功する。
関数を1つ、テストを4つ（正常系1、異常系1、境界値2）というバランスが、最小構成として分かりやすい。

---

## 13.8 型ヒントと静的解析

**型ヒント**は、変数や関数の引数・戻り値が、どの型を想定しているかをコードに明示する記法である。
Python自体は実行時に型ヒントを強制しないが、`mypy` のような**静的解析**ツールで、実行前に型の矛盾を検出できる。

```python
def classify_disk_usage(used_percent: float, warn_percent: float, crit_percent: float) -> str:
    ...
```

型ヒントが無いと、次のような誤りが実行するまで分からない。

```python
def bad_example(value):
    return value.strip()  # 呼び出し側が数値を渡すと、実行時まで気づけない
```

型ヒントを付けても、静的解析を実行しなければ検出できない。
mypyを実行する。

```bash
mypy --strict samples/python/13_disk_classifier.py
```

実行結果の例:

```text
Success: no issues found in 1 source file
```

`--strict` は、型ヒントの省略や `Any` への暗黙の依存を厳しく検出するモードである。
新規コードでは `--strict` から始め、既存コードへ段階的に導入する場合は緩いモードから始めて徐々に厳しくする。

設定は `pyproject.toml` にまとめられる。

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_ignores = true
```

型ヒントの効果:

- 呼び出し側の引数の型誤りを、実行前に検出できる
- IDEの補完とリファクタリング支援が効きやすくなる
- 関数のシグネチャ自体が、簡潔なドキュメントになる（第14章のドキュメントの節でも扱う）

---

## 13.9 lintとフォーマッター

**lint（静的解析）**は、コードを実行せずに、構文誤り・未使用変数・危険なパターンなどを検出する仕組みである。
**フォーマッター**は、インデントや空白、改行位置などのスタイルを、ツールで自動的に統一する仕組みである。

| 言語 | lint | フォーマッター |
|------|------|-----------------|
| Python | ruff（旧: flake8 + pylint相当） | ruff format（black相当） |
| Bash | shellcheck | shfmt |
| PowerShell | PSScriptAnalyzer | PowerShellの組み込み整形 |

Python（ruff）:

```bash
ruff check samples/python/13_disk_classifier.py
```

実行結果の例:

```text
All checks passed!
```

フォーマットを揃える:

```bash
ruff format samples/python/13_disk_classifier.py
```

Bash（shellcheck）:

```bash
shellcheck samples/bash/13_classify_disk.sh
```

shellcheckは、クォート漏れ（第7章のシェルインジェクションにも関わる）、未使用変数、
`[ ]` と `[[ ]]` の違いによる罠などを検出する。

PowerShell（PSScriptAnalyzer）:

```powershell
Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force
Invoke-ScriptAnalyzer -Path samples/powershell/13_classify_disk.ps1
```

lintとフォーマッターを使う利点:

- レビューで「スペースが1つ多い」のようなスタイルの指摘をせずに済み、レビュー時間をロジックに集中できる
- 危険なパターン（未クォートの変数展開、broad except、`eval` の使用など）を、実行前に機械的に検出できる
- チーム内でスタイルの好みによる議論を減らせる（フォーマッターの設定がルールそのものになる）

> **警告**: lintとフォーマッターは、コードの意図や仕様の正しさまでは保証しない。
> 「lintが通った」は「正しく動く」の代わりにならない。テストと組み合わせて使う。

---

## 13.10 Bashのテスト

Bashには、pytestやPesterに相当する標準的なテストフレームワークが無い。
本書では、次の方針で手書きのテストを書く。

1. テスト対象のスクリプトを `source` して、関数だけを読み込む
2. `set -euo pipefail` の効果でテストスクリプト自体が途中終了しないよう、失敗を想定する箇所は `set +e` / `set -e` で切り替える
3. 期待値と実際の値を比較し、一致しなければメッセージを出して失敗を記録する
4. 最後に失敗件数を集計し、1件でもあれば終了コード1で終わる

```bash
#!/usr/bin/env bash
set -euo pipefail

source ./samples/bash/13_classify_disk.sh

failures=0

assert_eq() {
  local expected="$1"
  local actual="$2"
  local message="$3"
  if [[ "${expected}" != "${actual}" ]]; then
    echo "FAIL: ${message}: expected=${expected} actual=${actual}" >&2
    failures=$(( failures + 1 ))
  else
    echo "ok: ${message}"
  fi
}

assert_eq "ok" "$(classify_disk_usage 50 80 90)" "50% is ok"
assert_eq "warning" "$(classify_disk_usage 80 80 90)" "80% (=warn) is warning"
assert_eq "critical" "$(classify_disk_usage 90 80 90)" "90% (=crit) is critical"

if [[ "${failures}" -gt 0 ]]; then
  echo "FAILED: ${failures} assertion(s) failed" >&2
  exit 1
fi
echo "all assertions passed"
```

`source` されたときに `main` が自動実行されないよう、対象スクリプト側で次のガードを入れておく。

```bash
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

これが無いと、`source` した瞬間に本処理が実行され、テストのための読み込みのつもりが実際に処理を走らせてしまう。

より本格的なBashテストが必要な場合は、`bats-core`（Bash Automated Testing System）のような外部フレームワークの導入も選択肢になる。
本書では、追加のインストールを前提にしない手書き方式を基本とする。

---

## 13.11 Pesterの基本

**Pester**は、PowerShell用のテストフレームワークである。
`Describe`/`It`/`Should` を使い、pytestに近い書き味でテストを書ける。

導入（README参照）:

```powershell
Install-Module -Name Pester -MinimumVersion 5.5 -Scope CurrentUser -Force
```

基本構造:

```powershell
Describe 'Get-DiskStatus' {
    It 'returns ok for usage below warn threshold' {
        Get-DiskStatus -UsedPercent 50 -WarnPercent 80 -CritPercent 90 | Should -Be 'ok'
    }

    It 'throws when warn threshold exceeds crit threshold' {
        { Get-DiskStatus -UsedPercent 85 -WarnPercent 90 -CritPercent 80 } | Should -Throw
    }
}
```

`BeforeAll` でテスト対象をドットソースし、`Mock` で関数を差し替える。

```powershell
BeforeAll {
    . "$PSScriptRoot/../samples/powershell/13_classify_disk.ps1"
}

Describe 'Invoke-Main' {
    It 'returns exit code 3 when a mocked disk is critical' {
        Mock Get-LocalDiskUsage {
            @([pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 95 })
        }
        Invoke-Main -WarnPercent 80 -CritPercent 90 | Should -Be 3
    }
}
```

`Mock` は、`Describe`/`It` のスコープ内で、指定した名前のコマンドやカスタム関数の呼び出しを横取りする。
実機のディスク構成に依存せず、`Get-LocalDiskUsage` が返す値を自由に設定してテストできる。

実行:

```powershell
Invoke-Pester ./tests/13_classify_disk.Tests.ps1 -Output Detailed
```

---

## 13.12 コードレビュー

**コードレビュー**は、変更を取り込む前に、書いた本人以外が内容を確認するプロセスである。

チェックすべき観点は、これまでの章の内容と対応している。

| 観点 | 確認内容 | 関連章 |
|------|----------|--------|
| 正しさ | 仕様どおりに動くか、テストで裏付けられているか | 本章 |
| 入力検証 | 型・範囲・パスの検証が漏れていないか | 第10章 |
| エラー処理 | 例外の握りつぶしが無いか、部分成功の扱いが明確か | 第8章 |
| セキュリティ | 秘密情報の直書きや、コマンドインジェクションの余地が無いか | 第10章 |
| ログ | 秘密情報のマスキング、過剰ログの抑制ができているか | 第9章 |
| dry-run | 破壊的操作にdry-runが効くか | 第12章 |
| 可読性・保守性 | 命名、関数の長さ、重複が適切か | 第14章 |

レビューを機能させるための実務上のコツ:

- **変更を小さく保つ**。1回のレビュー対象が大きいと、見落としが増え、レビューする側の負担も大きくなる（第16章）
- **指摘をブロッキングか任意か分ける**。「マストで直してほしい」と「気になったが必須ではない」を区別すると、議論が長引きにくい
- **機械的に検出できることは、lintとCIに任せる**。人間のレビューは、仕様の妥当性や設計判断のような、機械では判断しづらい観点に集中する
- **なぜその実装にしたかを、PRの説明やコミットメッセージに書く**。レビューする側が意図を推測する手間を減らす

---

## 13.13 CIへの組み込み

**CI（継続的インテグレーション）**は、コードの変更を取り込むたびに、テストや静的解析を自動実行する仕組みである。

CIに載せる基本的なステップ:

1. 依存関係のインストール
2. lint（ruff、shellcheck、PSScriptAnalyzer）
3. 型チェック（mypy）
4. テスト（pytest、Bashのテストスクリプト、Pester）
5. すべて成功したときだけマージ可能にする

GitHub Actionsの例:

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r infra_scripting_coding_guide/requirements.txt
      - run: ruff check infra_scripting_coding_guide
      - run: mypy --strict infra_scripting_coding_guide/samples/python
      - run: pytest infra_scripting_coding_guide/tests -v

  bash:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get update && sudo apt-get install -y shellcheck
      - run: shellcheck infra_scripting_coding_guide/samples/bash/*.sh
      - run: bash infra_scripting_coding_guide/tests/test_13_classify_disk.sh

  powershell:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: |
          Install-Module -Name Pester -MinimumVersion 5.5 -Force -SkipPublisherCheck
          Invoke-Pester ./infra_scripting_coding_guide/tests -CI
```

CI設計のポイント:

- **言語ごとにジョブを分ける**。1つのジョブに詰め込むと、どの言語の問題で落ちたか分かりにくくなる
- **PowerShellはWindowsランナーで動かす**。`Win32_LogicalDisk` のようなWindows固有APIに依存するコードは、Linux上のpwshでは動かない
- **失敗したらマージをブロックする**。ブランチ保護ルールで、CIが green のPRだけをマージ可能にする
- **実行時間が伸びてきたら、変更されたファイルに関連するテストだけ先に流す等、段階的な最適化を検討する**。ただし本書の規模では、全件実行で十分に速い

> **警告**: CIのSecrets（APIトークンなど）は、ワークフローのログに出さない。
> `set -x` のようなコマンド全体を表示するデバッグオプションを有効にしたまま秘密情報を扱う処理を実行すると、
> CIの実行ログに秘密情報が残ってしまう（第9章、第10章）。

---

## 13.14 実務向け改善: opsctlのディスク分類とテストスイート

`disk-check` 相当の機能を、テストしやすい形に分割した実装を示す。
完全なファイルは `samples/python/13_disk_classifier.py` に置く。

```python
#!/usr/bin/env python3
"""ディスク使用率を分類する opsctl の補助モジュール。

第13章のテスト例（ユニット、境界値、モック、結合）で対象にするコードである。
`df -P` 相当のテキストをパースし、閾値に基づいて ok/warning/critical に分類する。
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import TextIO

logger = logging.getLogger("opsctl.disk_classifier")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3


class InvalidThresholdError(ValueError):
    """warn/crit の閾値関係が不正なときに送出する。"""


@dataclass
class DiskUsage:
    mount_point: str
    used_percent: float


@dataclass
class ClassifiedUsage:
    mount_point: str
    used_percent: float
    status: str


def classify_disk_usage(used_percent: float, warn_percent: float, crit_percent: float) -> str:
    """使用率を ``ok``/``warning``/``critical`` に分類する。

    境界値は「以上」で次の段階に上がる。
    つまり ``used_percent == warn_percent`` は ``warning`` になり、
    ``used_percent == crit_percent`` は ``critical`` になる。
    """
    if warn_percent > crit_percent:
        raise InvalidThresholdError(
            f"warn_percent ({warn_percent}) must be <= crit_percent ({crit_percent})"
        )
    if used_percent < 0 or used_percent > 100:
        raise ValueError(f"used_percent out of range: {used_percent}")

    if used_percent >= crit_percent:
        return "critical"
    if used_percent >= warn_percent:
        return "warning"
    return "ok"


def parse_df_output(text: str) -> list[DiskUsage]:
    """``df -P`` 相当のテキストをパースする。

    先頭行はヘッダーとして無視する。
    列数が不足する行や使用率が数値でない行は、警告ログを出して読み飛ばす。
    """
    results: list[DiskUsage] = []
    lines = text.strip("\n").splitlines()
    if not lines:
        return results

    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 6:
            logger.warning("skipping malformed df line: %r", line)
            continue
        percent_field = fields[4].rstrip("%")
        try:
            used_percent = float(percent_field)
        except ValueError:
            logger.warning("skipping non-numeric percent field: %r", line)
            continue
        mount_point = fields[5]
        results.append(DiskUsage(mount_point=mount_point, used_percent=used_percent))
    return results


def fetch_disk_report(host: str, timeout: int = 10) -> list[DiskUsage]:
    """対象ホストで ``ssh host df -P`` を実行し、結果をパースする。

    外部プロセス呼び出しを ``parse_df_output`` から分離してあるため、
    テストでは ``subprocess.run`` だけをモックすれば、実際の ``ssh`` 接続なしに
    このパースロジックまで通した結合テストができる。
    """
    completed = subprocess.run(
        ["ssh", host, "df", "-P"],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"df on {host} failed: {completed.stderr.strip()}")
    return parse_df_output(completed.stdout)


def classify_all(
    usages: list[DiskUsage], warn_percent: float, crit_percent: float
) -> tuple[list[ClassifiedUsage], str]:
    """複数のディスク使用率をまとめて分類し、最悪ステータスも返す。"""
    results: list[ClassifiedUsage] = []
    worst = "ok"
    severity = {"ok": 0, "warning": 1, "critical": 2}

    for usage in usages:
        status = classify_disk_usage(usage.used_percent, warn_percent, crit_percent)
        results.append(
            ClassifiedUsage(mount_point=usage.mount_point, used_percent=usage.used_percent, status=status)
        )
        if severity[status] > severity[worst]:
            worst = status

    return results, worst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="disk_classifier", description="Classify disk usage from df -P output"
    )
    parser.add_argument("--host", help="remote host to query via ssh")
    parser.add_argument(
        "--input-file",
        type=argparse.FileType("r", encoding="utf-8"),
        help="local df -P output, mainly for testing without ssh",
    )
    parser.add_argument("--warn-percent", type=float, default=80.0)
    parser.add_argument("--crit-percent", type=float, default=90.0)
    parser.add_argument("--timeout", type=int, default=10)
    return parser


def _read_usages(args: argparse.Namespace) -> list[DiskUsage]:
    if args.input_file is not None:
        input_file: TextIO = args.input_file
        try:
            return parse_df_output(input_file.read())
        finally:
            input_file.close()
    return fetch_disk_report(args.host, timeout=args.timeout)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.host and args.input_file is None:
        parser.error("either --host or --input-file is required")

    try:
        usages = _read_usages(args)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        logger.error("failed to collect disk usage: %s", exc)
        return EXIT_RUNTIME

    try:
        results, worst = classify_all(usages, args.warn_percent, args.crit_percent)
    except InvalidThresholdError as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    print(json.dumps({"results": [asdict(r) for r in results], "worst": worst}, ensure_ascii=False))

    if worst == "critical":
        return EXIT_CRITICAL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

設計上のポイント:

- `parse_df_output` は純粋関数（入力だけから出力が決まり、副作用が無い）にしてあり、ユニットテストが書きやすい
- `fetch_disk_report` は外部コマンド呼び出しを持つが、`subprocess.run` だけをモックすれば、実際の `ssh` 接続なしにパースまで通した結合テストができる
- `main` は `--input-file` を持ち、`--host` を経由した実際のネットワーク接続なしにCLI全体を結合テストできる
- 例外の型（`InvalidThresholdError`、`RuntimeError`、`subprocess.TimeoutExpired`）を使い分け、テストで `pytest.raises` により区別して検証できる

実行例:

```bash
printf 'Filesystem 1024-blocks Used Available Capacity Mounted-on\n/dev/sda1 100 88 12 88%% /\n' \
  | python3 samples/python/13_disk_classifier.py --input-file /dev/stdin
# stdout: {"results": [{"mount_point": "/", "used_percent": 88.0, "status": "warning"}], "worst": "warning"}
# exit code: 0
```

---

## 13.15 悪い例と問題点

テストコード自体にも、良し悪しがある。
次は、動くが問題のあるテストの例である。

```python
import time

import requests


def test_disk_check():
    # 実際のAPIを呼んでいる。ネットワークが無い、または相手側が落ちていると失敗する
    response = requests.get("https://api.example.invalid/v1/disks", timeout=5)
    time.sleep(2)  # サーバー処理待ちのための固定スリープ。遅く、待ち時間が本当に十分かも不明
    data = response.json()
    assert data  # 何を検証しているのか名前からも中身からも分からない

    # 別の関心事（ファイル書き込み）を同じテストに詰め込んでいる
    with open("/tmp/disk_report.txt", "w") as f:
        f.write(str(data))
    assert True  # 実質何も検証していない
```

問題点:

- 実際のネットワークとAPIに依存しており、CI環境やオフライン環境では常に失敗する（不安定、いわゆるflaky test）
- `time.sleep(2)` は、実際に2秒で十分か根拠が無く、テスト全体を遅くする（第8章のリトライテストと同様、モックで置き換えるべき箇所）
- `assert data` は「データが何か入っていればよい」というだけで、期待する値を検証していない
- ファイル書き込みという別の関心事を同じテストに混ぜており、失敗したときにAPI呼び出しとファイル書き込みのどちらが原因か切り分けにくい
- `/tmp/disk_report.txt` という固定パスを使っており、並列実行時に他のテストと衝突する可能性がある
- `assert True` は常に成功し、テストとして意味を持たない

---

## 13.16 改善後のコード

13.15の問題点を1つずつ解消し、関心事ごとにテストを分割する。

```python
import json
from pathlib import Path


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def json(self) -> dict:
        return self._payload


def fetch_disk_report_via_api(session, base_url: str, timeout: int = 5) -> dict:
    """APIから取得したJSONをそのまま返す。セッションを引数で受け取ることで、
    テストでは requests.get 自体をモックせず、偽のセッションを渡すだけで済む。
    """
    response = session.get(f"{base_url}/v1/disks", timeout=timeout)
    return response.json()


def test_fetch_disk_report_via_api_returns_parsed_json() -> None:
    class FakeSession:
        def get(self, url: str, timeout: int) -> FakeResponse:
            assert url == "https://api.example.invalid/v1/disks"
            assert timeout == 5
            return FakeResponse({"disks": [{"mount": "/", "used_percent": 42}]})

    result = fetch_disk_report_via_api(FakeSession(), "https://api.example.invalid")

    assert result == {"disks": [{"mount": "/", "used_percent": 42}]}


def test_disk_report_is_written_to_a_temp_file(tmp_path: Path) -> None:
    report_path = tmp_path / "disk_report.json"
    payload = {"disks": [{"mount": "/", "used_percent": 42}]}

    report_path.write_text(json.dumps(payload), encoding="utf-8")

    assert json.loads(report_path.read_text(encoding="utf-8")) == payload
```

改善点:

- 実際のネットワーク呼び出しをせず、`FakeSession` という依存性注入で置き換えている。`monkeypatch` で `requests.get` 自体をパッチする方法もあるが、
  関数がセッションを引数で受け取る設計にしておくと、モックがさらに単純になる
- `time.sleep` を廃止した。非同期処理の完了待ちが本当に必要な場合は、固定スリープではなくポーリングとタイムアウト上限を組み合わせる（第8章のリトライ設計を参照）
- API呼び出しの検証とファイル書き込みの検証を、別々のテスト関数に分離した。どちらかが失敗したとき、テスト名から原因箇所がすぐ分かる
- `tmp_path` を使い、固定パスへの依存と、テスト間の衝突を無くした
- `assert result == {...}` のように、期待する値を具体的に書いている

Bashで同種の問題を避ける改善例（`13_classify_disk.sh` からの抜粋、ソースするだけでは処理が走らないガード）:

```bash
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

このガードが無いBashスクリプトを `source` すると、テストのつもりが本処理まで実行してしまい、
13.15の「意図しない副作用を含むテスト」と同じ問題を引き起こす。

---

## 13.17 セキュリティ上の注意点

- テストコードにも本物の秘密情報を書かない。APIトークンやパスワードのテストデータは、明らかにダミーと分かる値（例: `dummy-token-for-test`）を使う
- モックを使い、テストが実際の本番システムへ誤って書き込み・削除を行わないようにする。特に「モックし忘れた1箇所」が本番へ到達する事故に注意する
- CIのログに、テスト失敗時のスタックトレースが秘密情報を含まないか確認する（第9章のマスキングと同じ考え方）
- 依存パッケージ（pytest、ruff、mypyなど）は、信頼できる配布元から、バージョンを固定して導入する（第14章の依存関係管理を参照）
- CIのSecretsをテストコードやログに出力しない。`print(os.environ)` のような全環境変数のダンプは、CI上では特に危険である

> **警告**: 結合テストやE2Eテストで実際の外部システムに接続する構成を取る場合、
> テスト専用の環境（本番から隔離されたステージング環境など）を用意する。
> 本番のAPIやデータベースに対して、テストのたびに書き込み・削除を行う構成にしない。

---

## 13.18 テスト方法

本章のテスト基盤自体を検証する方法を示す。
完全なテストファイルは `tests/test_13_disk_classifier.py`、`tests/test_13_classify_disk.sh`、`tests/13_classify_disk.Tests.ps1` に置く（抜粋を示す）。

Python（境界値、異常系、モック、CLI結合の代表例）:

```python
import subprocess

import pytest

from conftest import load_sample_module

disk_classifier = load_sample_module("13_disk_classifier.py")


@pytest.mark.parametrize(
    ("used_percent", "expected"),
    [
        (79.9, "ok"),
        (80.0, "warning"),
        (90.0, "critical"),
        (100.0, "critical"),
    ],
)
def test_classify_disk_usage_boundaries(used_percent: float, expected: str) -> None:
    assert disk_classifier.classify_disk_usage(used_percent, warn_percent=80.0, crit_percent=90.0) == expected


def test_classify_disk_usage_rejects_inverted_thresholds() -> None:
    with pytest.raises(disk_classifier.InvalidThresholdError):
        disk_classifier.classify_disk_usage(85.0, warn_percent=90.0, crit_percent=80.0)


def test_fetch_disk_report_mocks_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            cmd,
            returncode=0,
            stdout="Filesystem 1024-blocks Used Available Capacity Mounted-on\n"
            "/dev/sda1 100 88 12 88% /\n",
            stderr="",
        )

    monkeypatch.setattr(disk_classifier.subprocess, "run", fake_run)

    usages = disk_classifier.fetch_disk_report("web01.example.invalid")
    assert usages[0].mount_point == "/"


def test_main_with_input_file_reports_critical(tmp_path, capsys) -> None:
    input_file = tmp_path / "df.txt"
    input_file.write_text(
        "Filesystem 1024-blocks Used Available Capacity Mounted-on\n"
        "/dev/sda1 100 95 5 95% /\n",
        encoding="utf-8",
    )
    exit_code = disk_classifier.main(["--input-file", str(input_file)])
    assert exit_code == disk_classifier.EXIT_CRITICAL
```

`load_sample_module` は `tests/conftest.py` で定義した補助関数である。
`samples/python` 配下のファイルは `13_disk_classifier.py` のように数字で始まる名前であり、
`import 13_disk_classifier` という文は書けない（数字始まりの識別子は文法違反になる）。
`importlib.util` でファイルパスから直接読み込むことで、番号付きファイルのまま実行可能なテストにしている。
実務では、`samples/python` を番号無しのパッケージとして整理し、通常の `import` を使う構成を推奨する（第5章、第12章）。

実行結果の例:

```bash
cd infra_scripting_coding_guide
pytest tests/ -v
# ... 41 passed
```

Bash（抜粋）:

```bash
source samples/bash/13_classify_disk.sh

assert_eq() {
  [[ "$1" == "$2" ]] || { echo "FAIL: $3: expected=$1 actual=$2" >&2; exit 1; }
  echo "ok: $3"
}

assert_eq "warning" "$(classify_disk_usage 80 80 90)" "80%(=warn) is warning"
assert_eq "critical" "$(classify_disk_usage 90 80 90)" "90%(=crit) is critical"
```

PowerShell（Pester、抜粋）:

```powershell
BeforeAll {
    . "$PSScriptRoot/../samples/powershell/13_classify_disk.ps1"
}

Describe 'Get-DiskStatus' {
    It 'returns warning exactly at warn threshold' {
        Get-DiskStatus -UsedPercent 80 -WarnPercent 80 -CritPercent 90 | Should -Be 'warning'
    }

    It 'throws when used percent is out of range' {
        { Get-DiskStatus -UsedPercent 150 -WarnPercent 80 -CritPercent 90 } | Should -Throw
    }
}
```

---

## 章末問題

### 問題1

ユニットテストと結合テストの違いを、対象範囲と実行速度の観点で説明せよ。

### 問題2

`used_percent >= warn_percent` という条件の境界値テストとして、どのような値を選ぶべきか、3点挙げよ。

### 問題3

モックを使いすぎると、どのような問題が起きるか説明せよ。

### 問題4

`time.sleep(2)` を使ったテストの問題点を挙げ、代替方法を1つ述べよ。

### 問題5

lintとテストは、それぞれ何を検出できて何を検出できないか説明せよ。

---

## 解答と解説

### 問題1

ユニットテストは1つの関数やクラスを対象にし、外部依存をモックで切り離すため実行が速い。
結合テストは複数の部品や外部システムとの連携を対象にするため、I/Oを含み実行が遅くなりやすい。

### 問題2

閾値のすぐ下（例: 79%）、閾値ちょうど（例: 80%）、閾値のすぐ上（例: 81%）の3点を選ぶ。
これにより、`>` と `>=` の取り違えのような off-by-one エラーを検出できる。

### 問題3

依存部品の実際の挙動が検証されなくなり、モックした境界の外側で起きる不具合（インターフェースの不一致、実際のAPIレスポンス形式の変化など）を見逃す。
テストは通るが本番で壊れる「偽陽性」が起きやすくなる。

### 問題4

実際に必要な待機時間が分からず、環境によって足りない、または無駄に長くなる。
テスト全体も遅くなる。
代替方法: 完了をポーリングで確認しタイムアウト上限を設ける、または対象のI/Oをモックして待機自体を無くす。

### 問題5

lintは、構文誤り、未使用変数、危険なパターン（クォート漏れ、broad exceptなど）を実行前に検出できるが、
ロジックが仕様どおりかまでは判定できない。
テストは、実際にコードを実行し、期待する結果になるかを検証できるが、テストケースとして書かれていない入力やパスは検出できない。
両方を組み合わせて初めて、実行前の問題と実行時の問題の両方をカバーできる。

---

## 実装演習

### 演習A

`13_disk_classifier.py` の `classify_all` に、`warn_percent` と `crit_percent` が等しい場合（閾値が1段階しかない）の挙動を確認するテストを追加せよ。
境界値としてどう扱うべきか、コメントで理由も書くこと。

### 演習B

`13_classify_disk.sh` に、`--warn-percent` と `--crit-percent` を省略したときのデフォルト値（80、90）が使われることを確認するテストを、`tests/test_13_classify_disk.sh` に追加せよ。

### 演習C

`13_classify_disk.ps1` の `Get-LocalDiskUsage` をモックし、複数のディスクのうち1つだけが `critical` の場合に、`Invoke-Main` の標準出力（JSON）に全ディスクの結果が含まれることを検証するPesterテストを書け。

---

## 次章予告

第14章では、保守しやすいコードを扱う。
命名、関数の長さ、責務分離、マジックナンバーの排除、依存関係の管理、リファクタリングと技術的負債への向き合い方を、
これまでの章のサンプルを題材に実装する。
