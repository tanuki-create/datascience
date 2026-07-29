# 第9章 ログ

## 学習目標

- printとログの違いを説明し、ログレベルを用途で使い分けられる
- タイムスタンプと実行ID付きの構造化ログを三言語で出力できる
- JSONログを設計し、ローテーションと出力先を運用に合わせて設定できる
- 秘密情報とPIIをログからマスキングし、過剰ログを抑制できる

前提: 第1章（標準出力・標準エラー・終了コード）、第3章（JSON）。

サンプルコードは学習用である。
本番のログ基盤（集約先、保持期間、アクセス権）は対象システムの方針に従って別途設計すること。

---

## 9.1 基本概念

**ログ**は、実行中の出来事を時系列で記録した情報である。

`print` は、開発中の一時的な確認に向く。
呼び出すたびに標準出力へ無条件で書き、レベルや出力先を後から制御できない。

**ロギング**は、レベル、出力先、フォーマットを実行時に切り替えられる仕組みである。
Pythonの `logging` モジュール、PowerShellの `Write-Verbose`/`Write-Information`、Bashの自作関数がこれにあたる。

運用スクリプトでprintだけを使うと、次の問題が起きる。

- 調査に必要なログと進捗表示が同じ形式で混在する
- 本番で静かにしたくても、コード中の `print` を探して消す以外に方法がない
- 出力にタイムスタンプや実行元の情報が付かない

---

## 9.2 ログレベル

**ログレベル**は、メッセージの重大度を段階で表す分類である。

| レベル | 用途 | 例 |
|--------|------|-----|
| DEBUG | 開発時の詳細な追跡情報 | 個々のリクエストの中身、変数の値 |
| INFO | 正常な進行の記録 | ホストの処理開始、処理件数 |
| WARNING | 異常ではないが注意が要る事象 | リトライ発生、非推奨設定の使用 |
| ERROR | 個別処理の失敗 | 1ホストへの接続失敗 |
| CRITICAL | 続行不能な致命的事象、または監視上のCRITICAL | 全ホスト不通、設定ファイル破損 |

`opsctl` の `--verbose`/`--quiet` は、レベルの下限を切り替える。

| オプション | 出力される最低レベル |
|------------|----------------------|
| （既定） | INFO |
| `--verbose` | DEBUG |
| `--quiet` | WARNING |

`--verbose` と `--quiet` は同時指定を許可しない。
両方が指定された場合は、引数解析の時点で終了コード1にする（第1章のusageエラーと同じ扱い）。

---

## 9.3 タイムスタンプと実行ID

**実行ID**（`run_id`）は、1回の実行を一意に識別する値である。
UUIDを使うと、他システムとの衝突をほぼ避けられる。

実行IDが無いと、同時に動いた複数のプロセスのログが交ざったとき、どの行がどの実行に属すか追えなくなる。

タイムスタンプは第3章の方針に従い、UTCまたはタイムゾーン付きISO 8601で記録する。

Python:

```python
import uuid
from datetime import datetime, timezone

run_id = str(uuid.uuid4())
timestamp = datetime.now(timezone.utc).isoformat()
```

Bash:

```bash
run_id="$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')"
timestamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
```

PowerShell:

```powershell
$runId = [guid]::NewGuid().ToString()
$timestamp = [DateTimeOffset]::UtcNow.ToString('o')
```

実行IDは、開始時に一度だけ生成し、その実行の全ログ行へ付与する。
サブプロセスへ引き継ぐ場合は、環境変数（例: `OPSCTL_RUN_ID`）で渡す。

---

## 9.4 最小構成のログ

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys

logger = logging.getLogger("minimal_demo")


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    logger.info("starting")
    logger.warning("disk usage high: %s%%", 85)
    logger.info("finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash（タイムスタンプ付き関数）:

```bash
#!/usr/bin/env bash
set -euo pipefail

log() {
  local level="$1"
  shift
  printf '%s %s %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "${level}" "$*" >&2
}

log INFO "starting"
log WARNING "disk usage high: 85%"
log INFO "finished"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
function Write-Log {
    param(
        [Parameter(Mandatory = $true)][string]$Level,
        [Parameter(Mandatory = $true)][string]$Message
    )
    $ts = [DateTimeOffset]::UtcNow.ToString('o')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

Write-Log -Level INFO -Message 'starting'
Write-Log -Level WARNING -Message 'disk usage high: 85%'
Write-Log -Level INFO -Message 'finished'
```

三言語とも、ログは標準エラーへ出す。
標準出力は、第1章の方針どおり機械可読な結果専用にする。

---

## 9.5 構造化ログとJSONログ

**構造化ログ**は、メッセージを自由文ではなく、決まったフィールドの組として記録する方式である。

**JSONログ**は、構造化ログを1行1JSONオブジェクトで書く形式である。
`grep`、`jq`、ログ集約基盤のいずれでも扱いやすい。

`opsctl` の設定（README参照）は、JSONログと実行ID付与を既定にしている。

```yaml
logging:
  format: json
  include_run_id: true
```

推奨フィールド:

| フィールド | 内容 |
|------------|------|
| `ts` | ISO 8601形式のタイムスタンプ |
| `level` | ログレベル |
| `run_id` | 実行ID |
| `event` | ロガー名やイベント種別 |
| `host` | 対象ホスト（該当する場合） |
| `message` | 人が読む本文 |

Python（`logging.Formatter` を継承した最小実装）:

```python
import json
import logging


class JsonFormatter(logging.Formatter):
    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "run_id": self.run_id,
            "event": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)
```

Bash（`jq -n` で1行のJSONを組み立てる）:

```bash
log_json() {
  local level="$1"
  local message="$2"
  jq -n -c \
    --arg ts "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --arg level "$level" \
    --arg run_id "${RUN_ID:-unknown}" \
    --arg message "$message" \
    '{ts: $ts, level: $level, run_id: $run_id, event: "opsctl", message: $message}' >&2
}

log_json INFO "starting"
```

PowerShell（`ConvertTo-Json` で1行にする）:

```powershell
function Write-JsonLog {
    param(
        [string]$Level,
        [string]$Message,
        [string]$RunId
    )
    [pscustomobject]@{
        ts      = [DateTimeOffset]::UtcNow.ToString('o')
        level   = $Level
        run_id  = $RunId
        event   = 'opsctl'
        message = $Message
    } | ConvertTo-Json -Compress | ForEach-Object { [Console]::Error.WriteLine($_) }
}

Write-JsonLog -Level 'INFO' -Message 'starting' -RunId ([guid]::NewGuid().ToString())
```

---

## 9.6 実務向け改善: opsctl共通ロガー

`samples/python/09_json_logger.py` に、実行ID付与、JSONフォーマット、ファイル出力、秘密情報マスキングをまとめたヘルパーを置く。

```python
#!/usr/bin/env python3
"""opsctl向けの共通JSONロギングヘルパー。

logger, run_id = configure_json_logging("opsctl.ping_check", verbose=args.verbose)
のように、各サブコマンドの先頭で呼び出す想定である。
"""
from __future__ import annotations

import json
import logging
import re
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path

_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)(authorization\s*:\s*)(.+)"),
    re.compile(r"(?i)\b(token=)([^&\s]+)"),
    re.compile(r"(?i)\b(password=)([^&\s]+)"),
    re.compile(r"(?i)\b(api[_-]?key=)([^&\s]+)"),
]


def mask_secrets(message: str) -> str:
    """既知の秘密情報パターンを ``***`` へ置き換える。

    完全な検出は保証できない。ログ出力前に、そもそも秘密情報を
    メッセージへ含めない設計を優先する。
    """
    masked = message
    for pattern in _SECRET_PATTERNS:
        masked = pattern.sub(lambda m: f"{m.group(1)}***", masked)
    return masked


class JsonFormatter(logging.Formatter):
    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        message = mask_secrets(record.getMessage())
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "run_id": self.run_id,
            "event": record.name,
            "message": message,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_json_logging(
    logger_name: str,
    *,
    verbose: bool = False,
    quiet: bool = False,
    log_file: Path | None = None,
) -> tuple[logging.Logger, str]:
    if verbose and quiet:
        raise ValueError("verbose and quiet are mutually exclusive")

    run_id = str(uuid.uuid4())
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()  # 二重呼び出しで行が重複するのを防ぐ
    logger.propagate = False

    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)

    formatter = JsonFormatter(run_id)

    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, run_id


def main() -> int:
    logger, run_id = configure_json_logging(
        "opsctl.demo", verbose=True, log_file=Path("work/logs/demo.log")
    )
    logger.info("run started")
    logger.debug("connecting host=web01.example.invalid")
    logger.warning("Authorization: Bearer sk-do-not-log-this-value")
    logger.error("host unreachable host=web02.example.invalid")
    logger.info("run finished run_id=%s", run_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`mask_secrets` は、レンダリング後の完成メッセージに対して呼ぶ。
`record.msg`（`%s` などを含むテンプレート文字列）へ先に適用すると、引数側に埋め込まれた秘密情報を見逃す。

実行例:

```bash
python3 samples/python/09_json_logger.py
# stderr（抜粋、実際は1行1JSON）:
# {"ts": "...", "level": "WARNING", "run_id": "...", "event": "opsctl.demo", "message": "Authorization: ***"}
```

---

## 9.7 ログローテーション

**ログローテーション**は、ログファイルを一定の条件で切り替え、古いものを退避または削除する運用である。
無制限にログを追記し続けると、ディスクを圧迫する。

Python（サイズ基準、9.6の `RotatingFileHandler` と同じ仕組み）:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "work/logs/opsctl.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
```

時間基準でローテーションしたい場合は `TimedRotatingFileHandler` を使う。

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    "work/logs/opsctl.log",
    when="midnight",
    backupCount=14,
    encoding="utf-8",
)
```

Linuxでは、アプリケーション側に実装せず `logrotate` へ委ねる選択もある。

```text
# /etc/logrotate.d/opsctl
/var/log/opsctl/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
    copytruncate
}
```

`copytruncate` は、ログを書き続けるプロセスがファイルディスクリプタを再オープンしない場合に使う。
プロセス側でSIGHUPを受けて再オープンできるなら、`copytruncate` を外し、`postrotate` でシグナル送信する方が欠損が少ない。

Windowsでは `logrotate` 相当の標準ツールがない。
`TimedRotatingFileHandler` などアプリケーション側での実装か、イベントログへの記録を検討する。

---

## 9.8 悪い例と問題点

### 悪いコード

```python
#!/usr/bin/env python3
import subprocess
import sys

token = sys.argv[1]
host = sys.argv[2]

print(f"calling api with token={token}")
result = subprocess.run(
    f"curl -H 'Authorization: Bearer {token}' https://api.example.invalid/v1/hosts/{host}",
    shell=True,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    print("failed")
```

問題点:

- トークンをそのまま標準出力へ出しており、ターミナル履歴やCI実行ログに残る
- `print` だけでレベルが無く、本番で静かにする手段がない
- タイムスタンプと実行IDが無く、複数実行のログが混ざると追跡できない
- 失敗時のメッセージが `"failed"` のみで、原因調査に必要な情報が残らない
- `shell=True` と文字列連結でコマンドを組み立てている（第10章で扱うコマンドインジェクションの温床）

### 改善後

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, str((__file__.rsplit("/", 2)[0])))  # samples/python を解決するための最小限の調整
from json_logger import configure_json_logging  # noqa: E402  (09_json_logger.py を想定)

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2


def main(argv: list[str]) -> int:
    logger, run_id = configure_json_logging("opsctl.api_call")

    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        logger.error("OPSCTL_API_TOKEN is required")
        return EXIT_USAGE
    if len(argv) < 1:
        logger.error("usage: api_call.py HOST")
        return EXIT_USAGE
    host = argv[0]

    logger.info("calling api host=%s run_id=%s", host, run_id)
    result = subprocess.run(
        ["curl", "-sS", "-H", f"Authorization: Bearer {token}",
         f"https://api.example.invalid/v1/hosts/{host}"],
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )
    if result.returncode != 0:
        logger.error("api call failed host=%s returncode=%s", host, result.returncode)
        return EXIT_RUNTIME

    logger.info("api call succeeded host=%s", host)
    print(result.stdout)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

改善後は、トークンをログへ出さず、レベルと実行IDを持ち、`shell=True` を使わずリスト引数で `curl` を呼ぶ。
`import` パスの調整はサンプル間の依存を示す簡略表現であり、実務では `samples/python` をパッケージとして整え、通常の `import` で解決する（第5章）。

---

## 9.9 過剰ログの抑制

大量のホストや繰り返し処理をすべてINFOで記録すると、ログ量が増え、重要な行が埋もれる。

対策:

1. ループ内の個別成功はDEBUGにし、INFOは集計行（開始・終了・件数）に絞る
2. 同一エラーが連続する場合は、件数をまとめて1行で報告する
3. ポーリングや定期チェックの「変化なし」を毎回記録しない。状態が変わった時だけ記録する
4. `logging.basicConfig` や `configure_json_logging` を1実行につき1回だけ呼ぶ。複数回呼ぶとハンドラが重複し、同じ行が複数回出力される

```python
failures = 0
for host in hosts:
    ok, detail = check(host)
    if ok:
        logger.debug("host=%s ok", host)
    else:
        failures += 1
        logger.error("host=%s failed detail=%s", host, detail)

logger.info("summary total=%s failures=%s", len(hosts), failures)
```

---

## 9.10 PII/秘密のマスキング

**マスキング**は、ログに残すべきでない値を、判読できない代替表現に置き換える処理である。

対象になりやすい値:

- APIトークン、パスワード、秘密鍵
- `Authorization` ヘッダー全体
- 個人を特定できる情報（メールアドレス、電話番号、氏名などのPII）
- クエリ文字列に含まれるトークン（`?token=...`）

> **警告**: リクエスト・レスポンスの本文をそのままログに出す実装は、意図せず秘密情報やPIIを記録する。
> デバッグ目的でも、本文全体のダンプは既定で無効にし、必要な項目だけを選んで記録する。

9.6の `mask_secrets` は正規表現によるマスキングであり、想定外の形式は見逃す。
確実性を上げるには、次を組み合わせる。

- ログに渡す前の時点で、秘密情報を持つオブジェクトから除外する（マスキングに頼らない設計）
- URLを記録するときはクエリ文字列を除去するか、既知のキーだけを除去する
- ログ集約基盤側でも、既知パターンの再マスキングやアクセス制御を設定する

---

## 9.11 調査可能なログ

**調査可能なログ**は、障害発生後に「いつ・どこで・何が起きたか」を、ログだけから再構成できるログである。

満たすべき条件:

- 実行ID、タイムスタンプ、対象ホスト、処理名、結果を含む
- エラー時は、原因になった例外の型とメッセージを含む（スタックトレース全体はDEBUGでもよい）
- 成功と失敗を同じフィールド構成で記録し、集計しやすくする
- 時刻はUTC、または常に同じタイムゾーン表記で統一する

```python
logger.error(
    "disk check failed host=%s error_type=%s error=%s",
    host,
    type(exc).__name__,
    exc,
)
```

---

## 9.12 セキュリティ上の注意点

- トークン、パスワード、秘密鍵をログへ書かない。9.10のマスキングは補助であり、根本対策は「そもそも記録しない設計」である
- リクエスト全文やレスポンス全文の無条件ログを避ける
- ログファイルの権限を絞る（例: `chmod 640`）。誰でも読めるパーミッションにしない
- ログ集約先への転送経路はTLSを使う（第11章）
- 監査目的のログ（誰が何を実行したか）は、デバッグログと分離し、改ざん検知や保持期間の要件を満たす場所へ送る（第10章の監査ログ）

---

## 9.13 テスト方法

Python（`caplog` でログ出力を検証する）:

```python
import logging

from samples.python.json_logger import mask_secrets


def test_mask_secrets_authorization_header() -> None:
    masked = mask_secrets("Authorization: Bearer sk-abcdef123456")
    assert "sk-abcdef123456" not in masked
    assert masked.startswith("Authorization: ")


def test_logger_emits_info(caplog) -> None:
    logger = logging.getLogger("test_logger_demo")
    logger.setLevel(logging.INFO)
    with caplog.at_level(logging.INFO):
        logger.info("host=%s ok", "web01.example.invalid")
    assert "web01.example.invalid" in caplog.text
```

Bash（出力形式の検証）:

```bash
output="$(bash -c 'source samples/bash/09_log_helpers.sh; log INFO "hello"' 2>&1)"
[[ "${output}" == *"INFO hello"* ]]
```

PowerShell（Pesterの骨格）:

```powershell
Describe 'Write-Log' {
    It 'writes level and message to stderr' {
        $err = & pwsh -NoProfile -Command {
            . ./samples/powershell/09_log_helpers.ps1
            Write-Log -Level 'INFO' -Message 'hello'
        } 2>&1
        $err | Should -Match 'INFO hello'
    }
}
```

---

## 章末問題

### 問題1

`print` とロギングモジュールの違いを、レベル・出力先・切り替え可能性の三点で説明せよ。

### 問題2

`Authorization: Bearer xxxx` をログに残した場合の具体的な被害を一つ挙げ、防止策を二つ述べよ。

### 問題3

`logging.basicConfig` を1実行の中で複数回呼ぶと何が起きるか説明し、防止方法を書け。

### 問題4

ポーリング型の監視スクリプトで、毎回のチェックをすべてINFOで出すと何が問題になるか述べ、改善方針を書け。

### 問題5

ログローテーションを実装しない場合に起きる運用上の問題を一つ挙げよ。

---

## 解答と解説

### 問題1

`print` はレベルが無く常に標準出力へ出る。
ロギングは、レベルで出力可否を制御し、出力先（標準エラー、ファイル、外部基盤）を実行時に切り替えられる。

### 問題2

被害例: 漏えいしたトークンで第三者がAPIを呼び、想定外の操作や情報取得をされる。
防止策: ログへ出す前にマスキングする、そもそもトークンを引数やログの対象文字列に含めない設計にする。

### 問題3

呼ぶたびにハンドラが追加され、同じログ行が複数回出力される。
防止方法: 設定関数の先頭で既存ハンドラをクリアするか、設定済みかどうかをフラグで管理して二重設定を防ぐ。

### 問題4

ログ量が増え、異常発生時の行が埋もれる。
改善方針: 個別の正常結果はDEBUGにし、INFOは開始・終了・集計に絞る。
状態変化時のみ記録する方式も有効である。

### 問題5

ディスクを圧迫し、最悪の場合はディスク枯渇で他の処理まで失敗する。
古いログの保持期間も管理できなくなる。

---

## 実装演習

### 演習A

`samples/python/09_json_logger.py` の `configure_json_logging` を使い、3台のホスト名を受け取って疎通確認の体裁（ダミーでよい）をログに残すスクリプトを書け。
DEBUGとINFOの使い分けを明示すること。

### 演習B

`mask_secrets` に、クエリ文字列 `?token=...` を検出して置換するパターンを追加し、テストを書け。

### 演習C

Bashで `log_json` 関数を作り、`RUN_ID` 環境変数を実行開始時に一度だけ生成して全ログ行へ付与するスクリプトを書け。

---

## 次章予告

第10章では、入力値検証とセキュリティを扱う。
型・範囲・パスの検証、コマンドインジェクションとパストラバーサルの対策、秘密情報の扱いを実装する。
