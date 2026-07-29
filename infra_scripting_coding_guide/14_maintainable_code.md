# 第14章 保守しやすいコード

## 学習目標

この章を終えると、次ができるようになる。

- 命名、関数の長さ、責務分離の観点から、変更しやすいコードとしにくいコードを見分けられる
- 重複したロジックを見つけ、共通化して保守箇所を一つにできる
- マジックナンバーを設定値や名前付き定数に置き換えられる
- 依存関係のバージョンを固定する理由と、固定しすぎることの副作用を説明できる
- 後方互換性を保ちながら機能を非推奨化し、安全にリファクタリングを進められる

前提: 第5章（関数とモジュール、責務分離）、第12章（設定とコードの分離）、第13章（テスト）。

サンプルコードは学習用である。
本番コードのリファクタリングは、必ずテストで現状の挙動を固定してから着手すること。
テストが無い状態での大規模な書き換えは、意図しない挙動変化を検出できないまま本番へ出る危険がある。

---

## 14.1 基本概念

**保守性**は、コードを書いた本人以外が、時間が経ってからでも安全に読み、変更できる度合いである。

保守性は、動いているかどうかとは別の軸である。
正しく動くコードでも、半年後に見て意図が分からなければ、変更のたびに調査コストがかかり、誤った変更を入れるリスクが上がる。

保守性を左右する要素は、突き詰めると「読み手が正しく推測できるか」に集約される。

- 名前から処理内容を推測できるか
- 関数やモジュールの範囲から責務を推測できるか
- 値の意味をコードの外（設定、定数名）から推測できるか
- 依存するライブラリのバージョンが、実行のたびに変わらず推測できるか

推測できない箇所が増えるほど、変更前に読むコード量が増え、変更後の確認範囲も広がる。

---

## 14.2 命名

**命名**は、変数・関数・モジュールに、その役割を表す名前を付けることである。

良い名前は、コメントを読まなくても処理内容を推測させる。
悪い名前は、実装を読まないと何のための値か分からない。

| 悪い例 | 改善後 | 理由 |
|--------|--------|------|
| `d` | `disk_usage_percent` | 単位と意味が分かる |
| `chk()` | `check_disk_usage()` | 何を確認する処理か分かる |
| `flag` | `is_dry_run` | 真偽値であることと意味が分かる |
| `data` | `host_usage_rows` | 何のデータかが分かる |
| `tmp` | `retry_delay_seconds` | 一時変数でも、意味と単位を示せる |
| `process()` | `classify_disk_usage()` | 汎用的すぎる名前を避ける |

三言語ごとの命名規約は次のとおりである。
規約が違っても、目的（意味の推測しやすさ）は共通している。

| 言語 | 変数・関数 | 慣例 |
|------|------------|------|
| Python | `snake_case` | PEP 8。クラスは `PascalCase` |
| Bash | `snake_case`、関数はモジュール名で名前空間化（第5章の `hostlib::load_hosts`） | Bashには言語標準の命名規約が無いが、`snake_case` が広く使われる |
| PowerShell | 関数は`動詞-名詞`の`PascalCase`（`Get-DiskStatus`） | `Get-Verb` で承認済み動詞を確認できる |

真偽値の変数・関数は、`is_`、`has_`、`should_` のような接頭辞を付けると、値の意味が読み取りやすくなる。

```python
# 悪い例: 真偽値なのか処理なのか名前から分からない
def dry_run(args) -> bool:
    ...

# 改善後
def is_dry_run(args: argparse.Namespace) -> bool:
    ...
```

省略形は、チーム全体で意味が通じる場合に限定する。
`cfg`（config）や `msg`（message）のような広く定着した省略形は問題にならないが、個人的な省略（`husg` のような造語）は避ける。

---

## 14.3 関数の長さと責務

第5章で分割の判断基準を扱った。
ここでは、既に大きくなってしまった関数を見つけ、直す観点を扱う。

関数が大きくなりすぎているサインは次のとおりである。

- 1画面でスクロールしないと全体を読めない（目安として40〜60行を超える）
- 関数の中に、明確に段落分けできる処理のまとまりが複数ある（読み込み、検証、判定、書き込みなど）
- 変更するとき、関数名が示す責務と関係ない部分まで読む必要がある
- テストを書こうとすると、無関係な前提条件まで用意しないと呼び出せない

```python
# 悪い例: 1つの関数に「引数解析」「検証」「読み込み」「判定」「書き込み」「通知」が全部入っている
def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--warn", type=float, default=80)
    parser.add_argument("--crit", type=float, default=90)
    args = parser.parse_args(argv)

    if args.warn > args.crit:
        print("invalid thresholds", file=sys.stderr)
        return 1

    rows = []
    with open(args.input, encoding="utf-8") as fh:
        for line in fh:
            host, usage = line.strip().split(",")
            rows.append((host, float(usage)))

    results = []
    for host, usage in rows:
        if usage >= args.crit:
            status = "CRITICAL"
        elif usage >= args.warn:
            status = "WARNING"
        else:
            status = "OK"
        results.append((host, usage, status))
        if status == "CRITICAL":
            requests.post("https://hooks.example.invalid/notify", json={"host": host})

    with open("report.csv", "w", encoding="utf-8") as fh:
        for host, usage, status in results:
            fh.write(f"{host},{usage},{status}\n")

    return 0
```

この関数は、引数解析・検証・入力読み込み・判定・通知・出力という6つの責務を持つ。
`classify` 相当の判定だけをテストしたくても、ファイル読み込みとHTTP呼び出しが必ず実行される。

責務ごとに分けると、次のようになる。

```python
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--warn", type=float, default=80)
    parser.add_argument("--crit", type=float, default=90)
    return parser.parse_args(argv)


def validate_thresholds(warn: float, crit: float) -> None:
    if warn > crit:
        raise ValueError("--warn must be <= --crit")


def load_usage_rows(path: Path) -> list[tuple[str, float]]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            host, usage = line.strip().split(",")
            rows.append((host, float(usage)))
    return rows


def classify(usage: float, warn: float, crit: float) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


def notify_critical(host: str, *, notifier: Callable[[str], None]) -> None:
    notifier(host)


def write_report(path: Path, results: list[tuple[str, float, str]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for host, usage, status in results:
            fh.write(f"{host},{usage},{status}\n")
```

分割後は、`classify` を単体でテストでき、`validate_thresholds` の異常系も個別に確認できる。
`main` は、これらを呼び出す薄い調整役になる（第5章の考え方と同じ）。

---

## 14.4 重複排除

**重複**は、同じ、または本質的に同じロジックが、複数箇所に存在する状態である。

重複の何が問題かというと、修正漏れである。
バグ修正や仕様変更のとき、コピーされた箇所の一つを直し忘れると、直した箇所と直していない箇所で挙動が食い違う。

```python
# 悪い例: 3つのサービス確認関数が、タイムアウト値以外ほぼ同じ処理をコピーしている
def check_web(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "5", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0


def check_db(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "10", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0


def check_cache(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "3", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0
```

タイムアウト値の意味（なぜwebは5秒でdbは10秒か）もコード中に残らず、`--max-time` の書式を変えたくなったとき3箇所を直す必要がある。

共通処理を1つの関数にまとめ、違いだけを引数にする。

```python
def check_service(host: str, *, timeout_seconds: int) -> bool:
    result = subprocess.run(
        ["curl", "-sf", "--max-time", str(timeout_seconds), f"http://{host}/health"],
        capture_output=True,
        timeout=timeout_seconds + 2,
    )
    return result.returncode == 0
```

重複排除は、似ているコードを闇雲に一つへ統合することではない。
「たまたま似ているが、将来別々に変化する可能性が高い処理」を無理に共通化すると、片方の変更がもう片方に影響し、条件分岐だらけの関数になる。
共通化するかどうかは、変更される理由が同じかどうかで判断する。

---

## 14.5 マジックナンバーと設定値

**マジックナンバー**は、コード中に直接書かれた、意味の説明が無い数値や文字列リテラルである。

```python
# 悪い例
if usage >= 90:
    return "CRITICAL"
if usage >= 80:
    return "WARNING"

time.sleep(0.5 * (2 ** attempt))  # 0.5 の意味がコードから読み取れない
```

`90`、`80`、`0.5` が何を意味するか、コードを読むだけでは分からない。
同じ値が別の場所に散らばっていると、一方だけ変更して不整合を起こしやすい。

名前付き定数にすると、意味と変更箇所が一つになる。

```python
DEFAULT_WARN_PERCENT = 80.0
DEFAULT_CRIT_PERCENT = 90.0
RETRY_BASE_DELAY_SECONDS = 0.5

if usage >= DEFAULT_CRIT_PERCENT:
    return "CRITICAL"
if usage >= DEFAULT_WARN_PERCENT:
    return "WARNING"

time.sleep(RETRY_BASE_DELAY_SECONDS * (2 ** attempt))
```

さらに、実行環境ごとに変わりうる値（第12章の「設定とコードの分離」）は、定数のままコードに置かず、設定ファイルや環境変数から解決する。

```python
warn_percent = resolve_threshold(cli_value=args.warn, config=config, key="disk_warn_percent", default=DEFAULT_WARN_PERCENT)
```

定数化すべきものと、設定化すべきものは区別する。

- 変更されないが意味を明示したい値（HTTPステータスコードの200など） → 名前付き定数
- 環境やチームによって変わりうる値（しきい値、タイムアウト、対象ホスト） → 設定ファイルや環境変数

---

## 14.6 コメントとドキュメント

**コメント**は、コードだけでは伝わらない意図や制約を補足する文章である。

コメントを書くべき場面と、書くべきでない場面がある。

```python
# 悪い例: コードをそのまま日本語に翻訳しただけ
i = i + 1  # iに1を足す

# 良い例: なぜそうするのか、コードだけでは分からない理由を書く
attempt += 1  # 初回リクエストも1回に数える(ログの attempt=1 がAPI呼び出し1回目と一致するように)
```

書くべきコメントの例:

- なぜその実装を選んだか（別の実装をあえて避けた理由）
- 一見不要に見えるが、外部要因のために必要な処理（特定OSのバグ回避など）
- TODOやFIXME（担当者や期限、関連チケット番号を添える）

```python
# WORKAROUND: macOSのbash 3.2では配列の空展開が異なる挙動をするため、
# 明示的に長さチェックを入れている。Bash 4以降では不要。
if [[ ${#hosts[@]} -gt 0 ]]; then
```

**ドキュメント**は、コードの外、またはdocstring・コメントブロックとして、使い方や設計方針をまとめたものである。
関数単位の使い方はdocstringに、モジュール全体の設計方針や運用手順はREADMEやこの種の解説書に書く。

```python
def resolve_timeout(cli_value: int | None, config: dict[str, Any]) -> int:
    """CLI引数 > 環境変数 > 設定ファイル > デフォルトの順で解決する。

    Args:
        cli_value: --timeout で指定された値。未指定なら None。
        config: 読み込み済みの設定辞書。

    Returns:
        解決済みのタイムアウト秒数。
    """
```

コメントとドキュメントは、コードの変更に追従しないと嘘の情報源になる。
コードレビューでロジックを変更したときは、関連するコメントとdocstringも同時に見直す。

---

## 14.7 依存関係とバージョン固定

**依存関係**は、自分のコードが動くために必要な、外部のライブラリやツールである。

**バージョン固定**は、依存関係のバージョンを明示的に指定し、実行のたびに異なるバージョンが入らないようにすることである。

```text
# requirements.txt: 悪い例
requests
pyyaml
```

バージョンを指定しないと、`pip install` を実行するタイミングによって異なるバージョンが入る。
ライブラリ側の破壊的変更（メジャーバージョンアップでの仕様変更）が、何もコードを変えていないのに突然ビルドを壊す原因になる。

```text
# requirements.txt: 改善後
requests==2.32.3
PyYAML==6.0.2
```

`==` による完全固定は再現性が最も高いが、セキュリティ修正を含む更新にも自分で追従する必要がある。
運用方針として、次のいずれかを選ぶ。

| 方針 | 書き方 | 向く場面 |
|------|--------|----------|
| 完全固定 | `requests==2.32.3` | 本番環境、再現性を最優先する場合 |
| 下限指定 | `requests>=2.32` | ライブラリ、互換範囲が分かっている場合 |
| 範囲指定 | `requests>=2.32,<3.0` | メジャーバージョンの破壊的変更だけ避けたい場合 |

Pythonでは `pip freeze > requirements-lock.txt` のようなロックファイル、またはPoetryやuvといったツールで依存関係全体（間接的な依存も含む）を固定できる。
PowerShellの `Install-Module` も `-RequiredVersion` でバージョンを固定できる。

```powershell
Install-Module -Name Pester -RequiredVersion 5.5.0 -Scope CurrentUser -Force
```

Bashは、外部コマンド（`curl`、`jq` など）のバージョンをOSのパッケージマネージャーに委ねることが多い。
バージョン差異が問題になる場合は、スクリプト内でバージョンを確認し、要件を満たさなければ早期にエラーにする。

```bash
if ! jq --version | grep -qE 'jq-1\.[6-9]'; then
  echo "jq 1.6 or later is required" >&2
  exit 1
fi
```

> **警告**: 古いバージョンに固定したまま長期間放置すると、既知の脆弱性が修正されないまま使われ続ける。
> バージョン固定は「勝手に変わらないこと」を保証する仕組みであり、「更新しなくてよい」という意味ではない。定期的な棚卸しと更新を運用に組み込む。

---

## 14.8 後方互換性と非推奨化

**後方互換性**は、新しいバージョンのコードが、古い呼び出し方や設定でも動き続ける性質である。

**非推奨化**は、古いインターフェースを即座に削除せず、警告を出しながら一定期間残す進め方である。

CLIのオプション名を変更する例で考える。

```python
# 悪い例: 予告なく --host を削除し、--target-host に変更する
parser.add_argument("--target-host", required=True)
# 既存の運用スクリプトが --host を渡していると、いきなり動かなくなる
```

既存の呼び出し元（他チームのスクリプト、cron、CIジョブ）が突然壊れると、影響範囲の調査に時間を取られる。
非推奨化を挟むと、移行期間を確保できる。

```python
import warnings

parser.add_argument("--target-host", default=None)
parser.add_argument("--host", default=None, help=argparse.SUPPRESS)  # 非推奨。ヘルプには出さない

args = parser.parse_args(argv)

if args.host is not None and args.target_host is None:
    warnings.warn(
        "--host is deprecated and will be removed in a future release; use --target-host instead",
        DeprecationWarning,
        stacklevel=2,
    )
    args.target_host = args.host

if args.target_host is None:
    parser.error("--target-host is required")
```

関数名を変更する場合も同様に、古い名前をラッパーとして残す。

```python
def check_service(host: str, *, timeout_seconds: int) -> bool:
    """新しい統一実装(14.4参照)。"""
    ...


def check_web(host: str) -> bool:
    """非推奨。check_service を使うこと。

    次のメジャーリリースで削除予定。
    """
    warnings.warn(
        "check_web is deprecated; use check_service(host, timeout_seconds=5) instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, timeout_seconds=5)
```

非推奨化の運用は、次の順序で進める。

1. 新しいインターフェースを追加し、既存のインターフェースはそのまま残す
2. 古いインターフェースを呼ぶと警告が出るようにする
3. 移行期間（リリースノートで告知した期間）を設ける
4. 移行が完了したことを確認してから、古いインターフェースを削除する

削除を急ぐと、把握していなかった利用箇所を壊す。
猶予を置きすぎると、非推奨のコードが増え続け、保守負担が下がらない。
どちらもチームの運用規模に応じて期間を決める。

---

## 14.9 リファクタリングの進め方

**リファクタリング**は、外部から見た挙動を変えずに、内部の実装を改善する作業である。

挙動を変えないことが前提のため、リファクタリング前にテストが無いと、変えていないつもりの挙動が変わったことに気づけない。

安全な進め方:

1. 対象コードに対するテストが無ければ、現状の挙動をそのまま固定するテスト（**特性化テスト**）を先に書く
2. 一度に一つの変更だけを行う（命名変更だけ、関数分割だけ、というように分ける）
3. 各変更のあとにテストを実行し、失敗しないことを確認してからコミットする
4. 大きな変更は、小さくレビュー可能な単位に分けてコミットする（第16章）

```python
# リファクタリング前の挙動を固定する特性化テスト
def test_legacy_run_behavior_before_refactor(tmp_path):
    input_path = tmp_path / "usage.csv"
    input_path.write_text("web01.example.invalid,95\n", encoding="utf-8")
    exit_code = run(["--input", str(input_path)])
    assert exit_code == 0
    # このテストは「正しい仕様」ではなく「今の挙動」を記録する。
    # リファクタリング後も同じ結果になることを確認してから、
    # 必要ならテストの期待値自体を仕様として見直す。
```

リファクタリングと機能追加は、同じコミットで混ぜない。
挙動が変わったとき、原因がリファクタリングによるものか機能追加によるものか切り分けられなくなる。

---

## 14.10 技術的負債

**技術的負債**は、その場をしのぐ実装や先送りにした設計判断が積み重なり、将来の変更コストを増やしている状態である。

負債という比喩が示すとおり、放置すると「利息」が発生する。
場当たり的な修正がさらに場当たり的な修正を呼び、変更のたびに影響範囲の調査が難しくなる。

技術的負債が生まれる典型的な状況:

- 締め切りに追われ、テストや検証を後回しにしたまま本番投入した
- 一時的なつもりだった回避策（14.6の`WORKAROUND`コメントのようなもの）が、恒久的な実装として残り続けた
- 依存関係を長期間更新せず、更新作業自体が大掛かりになってしまった
- ドキュメントが実装から乖離し、正しい情報がコードを読まないと分からない

技術的負債は、ゼロにすることを目指す性質のものではない。
締め切りに間に合わせるために意図的に負債を選ぶ判断もありうる。
重要なのは、負債を可視化し、あとで返済する計画を持つことである。

実務での扱い方:

- `TODO`/`FIXME`コメントに、内容だけでなく担当や関連チケット番号を添える
- 課題管理システムに負債専用のラベルを付け、棚卸しの対象にする
- 新機能の開発と並行して、負債返済の時間を定期的に確保する（スプリントの一定割合を割り当てるなど）
- 「動いているから触らない」判断と、「危険だから早期に返済する」判断を、影響範囲とリスクで区別する（セキュリティに関わる負債は優先度を上げる）

---

## 14.11 実務向け改善: サービス確認モジュールのリファクタリング

`samples/python/14_health_checks.py` に、14.3〜14.8の考え方をまとめて適用したモジュールを置く。
重複していた3つの確認関数を1つに統合し、マジックナンバーを定数化し、既存の関数名は非推奨警告付きで残す。

```python
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
    resolved_timeout = timeout_seconds if timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS.get(
        service, FALLBACK_TIMEOUT_SECONDS
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
```

`check_service` は、タイムアウトの意味をコメントで明示し、値そのものは辞書（設定に近い形）にまとめている。
旧関数は挙動を変えずに残し、呼び出し元には警告だけを出す。
呼び出し元の移行が完了した時点で、旧関数と`DEFAULT_TIMEOUT_SECONDS`の`web`/`db`/`cache`固定値依存を削除する判断ができる。

---

## 14.12 悪い例と問題点

```python
#!/usr/bin/env python3
import subprocess


def chk1(h):
    r = subprocess.run(["curl", "-sf", "--max-time", "5", f"http://{h}/health"], capture_output=True)
    return r.returncode == 0


def chk2(h):
    # chk1とほぼ同じ処理をコピーしている。タイムアウト値だけ違う
    r = subprocess.run(["curl", "-sf", "--max-time", "10", f"http://{h}/health"], capture_output=True)
    return r.returncode == 0


def process(hosts):
    results = []
    for h in hosts:
        ok = chk1(h)  # なぜchk1が呼ばれるのか、名前から推測できない
        results.append((h, ok))
        if not ok:
            # 0.5, 3 の意味が不明なマジックナンバー
            import time
            time.sleep(0.5)
            ok = chk1(h)
            if not ok:
                time.sleep(3)
    return results
```

問題点:

- `chk1`、`chk2`、`process` という名前から処理内容を推測できない
- `chk1` と `chk2` がタイムアウト値以外ほぼ同じ処理を重複させている
- `0.5`、`3` の意味が説明されておらず、リトライ間隔の設計意図が失われている
- `process` 関数の中に、確認・リトライ・待機という複数の責務が混在している
- `import time` が関数の中にあり、依存関係がファイル冒頭から見えない
- バージョン固定や後方互換性への配慮が無く、`chk1`/`chk2`の呼び出し元を洗い出さないと安全に変更できない

---

## 14.13 改善後のコード

14.11の `check_service` と、名前付き定数、非推奨ラッパーの組み合わせが改善後にあたる。
呼び出し側は次のように書き換わる。

```python
from samples.python.health_checks import check_service

RETRY_DELAY_SECONDS = 0.5
MAX_RETRIES = 2


def check_with_simple_retry(host: str, service: str) -> bool:
    """1回失敗したら固定間隔で再試行する簡易版(第8章のリトライとは別に、
    ヘルスチェックの表面的な揺らぎだけを吸収する用途)。
    """
    for attempt in range(MAX_RETRIES + 1):
        result = check_service(host, service)
        if result.ok:
            return True
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)
    return False
```

`check_service`、`RETRY_DELAY_SECONDS`、`MAX_RETRIES` という名前だけで、処理の見通しが立つ。
リトライの間隔や回数を変えたくなったときも、変更箇所は定数の1箇所で済む。

---

## 14.14 セキュリティ上の注意点

- 依存関係のバージョンを固定したまま更新を止めると、既知の脆弱性が残り続ける。定期的な依存関係の棚卸しを運用に組み込む（14.7）
- 非推奨化の期間中、古いインターフェースにも新しいインターフェースと同じ入力検証を適用する。移行期間中だけ検証が緩い経路が残ると、そこが攻撃対象になる
- リファクタリングで認証・認可・入力検証のコードを触るときは、通常のリファクタリング以上に慎重にテストを増やす。挙動を変えないつもりの変更が、意図せずチェックを弱める場合がある
- `TODO`/`FIXME`コメントに、修正されていない既知の危険（検証未実装など）を書く場合、その情報が公開リポジトリや配布物に含まれてよいかを確認する。攻撃者へのヒントになりうる

---

## 14.15 テスト方法

重複排除やリファクタリングでは、変更前後で挙動が変わっていないことをテストで確認する。

```python
import pytest

from samples.python.health_checks import DEFAULT_TIMEOUT_SECONDS, check_service


@pytest.mark.parametrize(
    ("service", "expected_timeout"),
    [("web", 5), ("db", 10), ("cache", 3), ("unknown-service", 5)],
)
def test_check_service_resolves_timeout_by_service(service, expected_timeout, monkeypatch):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["timeout"] = kwargs.get("timeout")

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr("samples.python.health_checks.subprocess.run", fake_run)
    result = check_service("web01.example.invalid", service)

    assert result.timeout_seconds == expected_timeout
    assert "--max-time" in captured["cmd"]
    assert str(expected_timeout) in captured["cmd"]


def test_deprecated_check_web_still_works_but_warns(monkeypatch):
    from samples.python.health_checks import check_web

    monkeypatch.setattr(
        "samples.python.health_checks.subprocess.run",
        lambda *a, **k: type("R", (), {"returncode": 0})(),
    )
    with pytest.warns(DeprecationWarning):
        assert check_web("web01.example.invalid") is True
```

`test_deprecated_check_web_still_works_but_warns` は、後方互換性のテストの典型例である。
「警告が出ること」と「結果が変わらないこと」の両方を確認する。
どちらか一方だけでは、非推奨化の意図（動き続けるが移行を促す）を検証したことにならない。

---

## 章末問題

### 問題1

`chk1`、`process` のような名前が保守性を下げる理由を、レビューする側の視点で説明せよ。

### 問題2

似た処理を重複させたまま残すべき場合があるとすれば、どのような条件のときか説明せよ。

### 問題3

マジックナンバーと設定値の違いを、「値が変わる理由」の観点から説明せよ。

### 問題4

依存関係を`==`で完全固定した場合に生じるリスクを一つ挙げ、対策を述べよ。

### 問題5

リファクタリング前にテストが無い場合、まず何をすべきか、その理由とともに述べよ。

---

## 解答と解説

### 問題1

名前から処理内容を推測できないと、レビューする側は実装を最初から最後まで読まないと妥当性を判断できない。
名前が適切なら、実装の細部を読む前に「意図どおりか」の見当がつき、レビューの負担が下がる。

### 問題2

将来、変更される理由が異なる可能性が高い場合である。
現時点でロジックが似ていても、片方だけ仕様変更が入る見込みが高いなら、無理に共通化すると条件分岐だらけの関数になり、かえって保守性が下がる。

### 問題3

マジックナンバーは、意味を明示していないだけで、値自体はコードの一部として固定でよい場合が多い（名前付き定数で解決する）。
設定値は、実行環境やチームの方針によって変わりうる値であり、コードの外（設定ファイル、環境変数）に置くべきものである。

### 問題4

リスク: 既知の脆弱性を修正した新バージョンが出ても、固定したままだと自動的には取り込まれない。
対策: 完全固定を維持しつつ、定期的な棚卸し(依存関係の脆弱性スキャン、更新確認)を運用に組み込む。

### 問題5

現状の挙動をそのまま固定する特性化テストを先に書く。
テストが無い状態でリファクタリングすると、変えていないつもりの挙動変化を検出する手段が無く、リファクタリングそのものが新たなバグの原因になりうる。

---

## 実装演習

### 演習A

`samples/python/14_health_checks.py` に `check_queue`（サービス名`"queue"`、既定タイムアウト15秒）を追加せよ。
`DEFAULT_TIMEOUT_SECONDS`辞書へ値を追加するだけで済む設計になっていることを確認せよ。

### 演習B

14.12の悪いコードから、責務ごとに関数を分割し、`chk1`/`chk2`/`process`に代わる名前を提案して書き換えよ。
書き換え後、14.15のテストパターンを参考に、正常系・異常系のテストを最低2つ追加せよ。

### 演習C

架空のCLIオプション`--legacy-mode`が非推奨だと仮定し、14.8の非推奨化の手順（新旧併存、警告、移行期間、削除）を、実際のコード変更案として4段階（4つのコミット相当）に分けて書け。
各段階でどのテストが必要かも述べること。

---

## 次章予告

第15章では、ここまでの知識を使い、疎通確認、ディスク監視、ログ検索、証明書期限確認など11個の運用題材を実装する。
言語適性（付録A）に応じて主実装言語を選び、テスト（第13章）と保守性（本章）を備えた形で仕上げる。
