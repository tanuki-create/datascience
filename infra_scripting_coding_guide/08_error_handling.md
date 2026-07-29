# 第8章 エラー処理

## 学習目標

この章を終えると、次ができるようになる。

- エラーの種類を分類し、例外と終了コードを適切に使い分けられる
- Pythonのtry/except/finally、Bashのtrap、PowerShellのtry/catch/finallyを実装できる
- 指数バックオフ付きリトライと、リトライしてはいけない場合を区別できる
- 部分成功とロールバックの方針を、実装前に決められる
- 利用者向けメッセージと、調査用の詳細ログを分けて出力できる

前提: 第1章の終了コード、第7章の外部コマンド実行。

サンプルコードは学習用である。本番のリトライ回数や待機時間は、対象システムの許容量に応じて調整すること。

---

## 8.1 基本概念

**エラー**は、処理が期待どおりに完了しなかった状態である。

エラーは、性質によって扱いを変える。

| 種類 | 例 | 対応の方向性 |
|------|-----|--------------|
| 利用者エラー | 引数不正、設定ファイルの構文誤り | 実行前に検証し、即座に分かりやすく報告する |
| 一時的なエラー | ネットワーク断、APIのレート制限 | リトライで回復する可能性がある |
| 恒久的なエラー | 認証失敗、権限不足 | リトライしても直らない。即座に報告する |
| 想定外のエラー | バグ、未処理の例外 | 調査用の詳細を残し、安全側に倒して停止する |

**例外**は、プログラムの通常の流れを中断し、呼び出し元へエラー情報を伝える仕組みである。
Python、PowerShellには例外機構がある。
Bashには例外が無く、終了コードと `trap` で代用する。

エラー処理の設計は、正常系の実装より先に決める。
第2章で述べたとおり、失敗時の挙動を後回しにすると、実装が進むほど直しにくくなる。

---

## 8.2 Pythonのtry/except/finally

```python
from __future__ import annotations

import logging

logger = logging.getLogger("example")


def read_threshold(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"invalid threshold: {text!r}") from exc
    if not (0 <= value <= 100):
        raise ValueError(f"threshold out of range: {value}")
    return value


def load_and_report(text: str) -> int:
    try:
        threshold = read_threshold(text)
    except ValueError as exc:
        logger.error("%s", exc)
        return 1
    finally:
        logger.debug("load_and_report finished for input=%r", text)

    print(threshold)
    return 0
```

`except ValueError as exc` は、`ValueError` という具体的な型だけを捕まえる。
`except Exception` のような広い捕捉は、意図しないバグまで飲み込んでしまう。

`raise ... from exc` は、元の例外を保持したまま新しい例外に読み替える。
トレースバックに両方の情報が残るため、調査がしやすい。

`finally` ブロックは、例外が発生してもしなくても必ず実行される。
リソースの解放やログ出力に使う。

複数の例外型をまとめて捕まえることもできる。

```python
try:
    risky_operation()
except (OSError, ValueError) as exc:
    logger.error("%s", exc)
```

---

## 8.3 Bashのtrap

Bashには例外機構が無いため、**終了コード**と `trap` を組み合わせてエラー処理を行う。

```bash
#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  local exit_code=$?
  echo "cleanup: exit_code=${exit_code}" >&2
  rm -f /tmp/work.$$
}
trap cleanup EXIT

on_error() {
  local line_no=$1
  echo "error occurred at line ${line_no}" >&2
}
trap 'on_error ${LINENO}' ERR

echo "start" > /tmp/work.$$
false   # ここで ERR トラップが発火し、その後 set -e により終了する
echo "unreachable"
```

`trap ... EXIT` は、スクリプトがどのような理由で終了しても実行される。
正常終了、`exit` によるエラー終了、シグナルによる中断のいずれでも呼ばれるため、後始末処理を書く場所として適している。

`trap ... ERR` は、`set -e` が有効な状態でコマンドが失敗したときに呼ばれる。
`if` の条件式や `&&`/`||` の一部として実行されたコマンドの失敗では呼ばれない点に注意する。

```bash
trap 'echo "ERR at line ${LINENO}" >&2' ERR
set -e

false  # ERRトラップが発火する
if false; then :; fi  # 条件式なのでERRトラップは発火しない
```

シグナルごとのトラップも設定できる。

```bash
trap 'echo "interrupted" >&2; exit 130' INT
trap 'echo "terminated" >&2; exit 143' TERM
```

`INT`（Ctrl+C相当）を受けたら終了コード130、`TERM` を受けたら143を返す慣例は、第1章の終了コード表とも整合する。

---

## 8.4 PowerShellのtry/catch/finally

```powershell
$ErrorActionPreference = 'Stop'

function Read-Threshold {
    param([string]$Text)
    try {
        $value = [double]$Text
    }
    catch {
        throw "invalid threshold: $Text"
    }
    if ($value -lt 0 -or $value -gt 100) {
        throw "threshold out of range: $value"
    }
    return $value
}

function Invoke-LoadAndReport {
    param([string]$Text)
    try {
        $threshold = Read-Threshold -Text $Text
    }
    catch {
        [Console]::Error.WriteLine($_.Exception.Message)
        return 1
    }
    finally {
        Write-Verbose "Invoke-LoadAndReport finished for input=$Text"
    }

    Write-Output $threshold
    return 0
}
```

PowerShellの `try/catch` は、`$ErrorActionPreference = 'Stop'` を設定していないと、非終了エラー（non-terminating error）を捕まえられない場合がある。
本書のPowerShellサンプルは、スクリプトの先頭で必ず `$ErrorActionPreference = 'Stop'` を設定する方針にしている。

特定の例外型だけを捕まえたい場合は、`catch` に型を指定する。

```powershell
try {
    Invoke-RestMethod -Uri 'https://api.example.invalid/status' -TimeoutSec 5
}
catch [System.Net.WebException] {
    [Console]::Error.WriteLine("network error: $($_.Exception.Message)")
}
catch {
    [Console]::Error.WriteLine("unexpected error: $($_.Exception.Message)")
    throw
}
```

最後の `catch` で想定外の例外を再度 `throw` している点に注意する。
すべてのエラーを握りつぶさず、想定していないものは上位へ伝える。

---

## 8.5 終了コードとの対応関係

例外や `trap` で捕まえたエラーは、最終的にプロセスの終了コードへ変換する。

本書の `opsctl` 規約（README参照）を、三言語で一貫させる。

Python:

```python
import sys

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3
EXIT_TIMEOUT = 4


def main() -> int:
    try:
        ...
    except ValueError:
        return EXIT_USAGE
    except TimeoutError:
        return EXIT_TIMEOUT
    except Exception:
        logging.exception("unexpected error")
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

`except Exception` を使うのは、この「最上位で捕まえてログを残し、終了コードへ変換する」一箇所に限定する。
途中の関数で `except Exception` を多用すると、原因の特定が難しくなる。

Bash、PowerShellでも、関数内部の判定と、最終的な `exit` / `return` コードの変換は別の場所に置く。

---

## 8.6 リトライと指数バックオフ

**リトライ**は、一時的な失敗に対して、同じ処理をもう一度試みることである。
**指数バックオフ**は、リトライのたびに待機時間を指数的に伸ばす方式である。

すべての失敗をリトライしてよいわけではない。

| 失敗の種類 | リトライすべきか |
|------------|------------------|
| ネットワークタイムアウト | する |
| 5xx系のサーバーエラー | する（回数上限付き） |
| 429（レート制限） | する（`Retry-After` があれば従う） |
| 4xx系（認証失敗、権限不足、不正リクエスト） | しない |
| 入力値そのものが不正 | しない |

恒久的なエラーをリトライし続けると、無駄な待機時間が積み重なり、対象システムへの負荷にもなる。

Python:

```python
from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger("retry")


class RetryableError(Exception):
    """リトライしてよい失敗を表す。"""


class PermanentError(Exception):
    """リトライしても直らない失敗を表す。"""


def retry_with_backoff(
    func: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
) -> T:
    attempt = 0
    while True:
        attempt += 1
        try:
            return func()
        except PermanentError:
            raise
        except RetryableError as exc:
            if attempt >= max_attempts:
                raise
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jitter = random.uniform(0, delay * 0.1)
            sleep_for = delay + jitter
            logger.warning(
                "attempt %s/%s failed: %s; retrying in %.2fs",
                attempt,
                max_attempts,
                exc,
                sleep_for,
            )
            time.sleep(sleep_for)
```

`PermanentError` はそのまま再送出し、リトライループに入らない。
`RetryableError` だけが待機とリトライの対象になる。

**ジッター**（ランダムな揺らぎ）を待機時間に加えることで、複数のクライアントが同時に同じタイミングで再試行し、対象システムへ負荷が集中する事態（サンダリングハード）を緩和する。

Bash:

```bash
retry_with_backoff() {
  local max_attempts="$1"
  local base_delay="$2"
  shift 2

  local attempt=1
  local rc
  while true; do
    # rcの捕捉はelse節に置く。elseが無い「if false; then ...; fi」は
    # それ自体の終了コードが0になり、"$@"の本当の終了コードが消えてしまう。
    if "$@"; then
      return 0
    else
      rc=$?
    fi
    if [[ "${attempt}" -ge "${max_attempts}" ]]; then
      echo "giving up after ${attempt} attempts" >&2
      return "${rc}"
    fi
    local delay=$(( base_delay * (2 ** (attempt - 1)) ))
    echo "attempt ${attempt}/${max_attempts} failed; retrying in ${delay}s" >&2
    sleep "${delay}"
    attempt=$(( attempt + 1 ))
  done
}
```

Bashでは、恒久的なエラーと一時的なエラーの区別を、終了コードの値で判定する設計が現実的である（例: 特定の終了コードだけをリトライ対象にする）。

PowerShell:

```powershell
function Invoke-WithRetry {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Action,
        [int]$MaxAttempts = 5,
        [double]$BaseDelaySeconds = 0.5
    )

    $attempt = 0
    while ($true) {
        $attempt++
        try {
            return & $Action
        }
        catch [PermanentErrorException] {
            throw
        }
        catch {
            if ($attempt -ge $MaxAttempts) {
                throw
            }
            $delay = $BaseDelaySeconds * [Math]::Pow(2, $attempt - 1)
            [Console]::Error.WriteLine("attempt $attempt/$MaxAttempts failed: $($_.Exception.Message); retrying in ${delay}s")
            Start-Sleep -Seconds $delay
        }
    }
}
```

`PermanentErrorException` は、恒久的なエラー用に定義したカスタム例外クラスを想定している。
PowerShellでカスタム例外を作る場合は、`.NET` の `Exception` を継承したクラスをC#やPowerShellクラス構文で定義する。

---

## 8.7 握りつぶし禁止

**握りつぶし**は、エラーを検知したにもかかわらず、記録も再送出もせずに処理を継続することである。

### 悪いコード

```python
def check_all_bad(hosts: list[str]) -> int:
    for host in hosts:
        try:
            check_host(host)
        except Exception:
            pass  # 握りつぶし
    return 0  # 常に成功扱い
```

問題点:

- どのホストが失敗したか記録されない
- 呼び出し側は常に成功したと誤認する
- 想定外のバグ（`TypeError` など）まで同じ `except Exception: pass` で消えてしまう

### 改善後

```python
from dataclasses import dataclass


@dataclass
class CheckFailure:
    host: str
    error: str


def check_all(hosts: list[str]) -> tuple[list[CheckFailure], int]:
    failures: list[CheckFailure] = []
    for host in hosts:
        try:
            check_host(host)
        except (TimeoutError, ConnectionError) as exc:
            failures.append(CheckFailure(host=host, error=str(exc)))

    if failures:
        for failure in failures:
            logger.error("check failed: host=%s error=%s", failure.host, failure.error)
        return failures, 2
    return failures, 0
```

捕まえる例外の型を明示し、失敗を一覧として記録し、終了コードへ反映する。
`Exception` という広い型で握りつぶす代わりに、想定される例外だけを扱い、それ以外は伝播させる。

---

## 8.8 部分成功

**部分成功**は、複数の対象のうち一部だけが成功し、残りが失敗した状態である。

部分成功を「全体成功」として報告すると、失敗した対象が放置される。
第2章、第7章で扱った複数ホスト処理と同様、次を実装前に決める。

1. 1件でも失敗したら、全体をどの終了コードにするか
2. 失敗した対象の一覧を、どこに残すか（レポート、stderr、両方）
3. 一部成功した分の結果を、そのまま使ってよいか、取り消すべきか

```python
from dataclasses import dataclass


@dataclass
class ApplyResult:
    host: str
    ok: bool
    error: str | None = None


def apply_to_all(hosts: list[str], apply) -> tuple[list[ApplyResult], int]:
    results: list[ApplyResult] = []
    for host in hosts:
        try:
            apply(host)
            results.append(ApplyResult(host=host, ok=True))
        except Exception as exc:  # 個々の対象の失敗はここで吸収し、記録する
            results.append(ApplyResult(host=host, ok=False, error=str(exc)))

    failed = [r for r in results if not r.ok]
    exit_code = 2 if failed else 0
    return results, exit_code
```

ここでの `except Exception` は、ループの外側まで伝播させず、対象ごとの結果として記録する意図的な設計である。
8.7節の「握りつぶし」と違い、失敗を `results` に残し、`exit_code` にも反映している点が異なる。

---

## 8.9 ロールバック

**ロールバック**は、失敗した変更を、変更前の状態へ戻す操作である。

すべての操作をロールバック可能にするのは難しい。
設計時に、対象操作を次のように分類する。

| 分類 | 例 | ロールバック方針 |
|------|-----|-------------------|
| 冪等な操作 | 設定ファイルの上書き（バックアップあり） | 第6章のバックアップから復元 |
| 追記のみの操作 | ログ追記、レポート出力 | 通常はロールバック不要 |
| 外部への副作用 | API経由のリソース作成、メール送信 | 打ち消し操作（削除API、取消通知）を用意するか、事前承認制にする |
| 取り消し不能な操作 | 物理的な破棄、通知済みの重要アラート | 実行前の確認を必須にし、失敗時は人手対応に切り替える |

第6章の `update_config` を使った、設定変更のロールバック例:

```python
from pathlib import Path

from samples.python.safe_config_update import update_config


def apply_config_with_rollback(
    target: Path,
    new_content: str,
    backup_dir: Path,
    post_check,
) -> None:
    backup = update_config(target, new_content, backup_dir)
    try:
        post_check(target)
    except Exception:
        if backup is not None:
            target.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
            logger.error("post_check failed; rolled back to %s", backup)
        raise
```

`post_check` は、変更後の設定を検証する関数を想定している（例: 設定の構文チェック、対象サービスへの反映確認）。
検証に失敗したら、バックアップの内容を書き戻し、例外を再送出して呼び出し元に失敗を伝える。

---

## 8.10 利用者向けエラーと調査用エラー

**利用者向けメッセージ**は、実行した人がすぐに理解し、次の行動を取れる短い説明である。
**調査用ログ**は、原因調査に必要な詳細情報（スタックトレース、内部状態、リクエストID）である。

両者を同じ場所に出すと、利用者向けの画面がノイズだらけになるか、調査に必要な情報が欠落するかのどちらかになりやすい。

```python
import logging
import sys
import uuid

logger = logging.getLogger("opsctl")


def main() -> int:
    run_id = str(uuid.uuid4())
    try:
        do_work()
    except ValueError as exc:
        # 利用者向け: 短く、対応方法が分かる
        print(f"設定が不正です。--config の内容を確認してください (run_id={run_id})", file=sys.stderr)
        # 調査用: 詳細と原因
        logger.error("validation failed run_id=%s detail=%s", run_id, exc, exc_info=True)
        return 1
    return 0
```

`run_id` を両方に含めておくと、利用者からの問い合わせと調査用ログを突き合わせられる。
第9章のログ設計で、この `run_id` を構造化ログの必須フィールドとして扱う。

---

## 8.11 実務向けサンプル: リトライ付きヘルスチェック

要件:

- 対象ホストへヘルスチェック相当のコマンドを実行する
- 一時的な失敗は指数バックオフでリトライする
- 恒久的な失敗（コマンド不存在、設定不正）は即座に打ち切る
- 利用者向けメッセージと調査用ログを分離する
- 部分成功を許容し、失敗ホストの一覧を残す

完全な実行可能ファイルは `samples/python/08_retry_backoff.py`、`samples/bash/08_retry_backoff.sh`、`samples/powershell/08_retry_backoff.ps1` に置く。
Python版の骨子:

```python
from __future__ import annotations

import logging
import random
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("retry_backoff")


class PermanentError(Exception):
    pass


class RetryableError(Exception):
    pass


@dataclass
class HealthResult:
    host: str
    ok: bool
    attempts: int
    detail: str


def check_once(host: str, command: str, timeout: int) -> None:
    if shutil.which(command) is None:
        raise PermanentError(f"command not found: {command}")
    try:
        completed = subprocess.run(
            [command, "-c", "1", "-W", str(timeout), host],
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RetryableError(f"process timeout: {exc}") from exc

    if completed.returncode != 0:
        raise RetryableError(f"{command} failed: {(completed.stderr or completed.stdout).strip()}")


def check_with_retry(
    host: str,
    command: str,
    timeout: int,
    max_attempts: int,
    base_delay: float,
) -> HealthResult:
    attempt = 0
    while True:
        attempt += 1
        try:
            check_once(host, command, timeout)
            return HealthResult(host=host, ok=True, attempts=attempt, detail="ok")
        except PermanentError as exc:
            return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
        except RetryableError as exc:
            if attempt >= max_attempts:
                return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay * 0.1)
            logger.debug("host=%s attempt=%s retry in %.2fs: %s", host, attempt, delay + jitter, exc)
            time.sleep(delay + jitter)
```

`PermanentError` はリトライせずに即座に結果へ反映する。
`RetryableError` は上限回数まで指数バックオフで再試行し、上限に達したら失敗として記録する。

---

## 8.12 セキュリティ上の注意点

- 例外メッセージやスタックトレースに、秘密情報（トークン、パスワード、内部パス）を含めない
- 利用者向けメッセージには詳細を出しすぎない。攻撃者にシステム構成のヒントを与える場合がある
- リトライ処理が、認証エラーのような恒久的な失敗を繰り返すと、対象システムのアカウントロックを誘発することがある。恒久的なエラーは即座に打ち切る
- ロールバック処理自体も失敗しうる。ロールバックの失敗は、握りつぶさず別経路で強く警告する
- `trap` や `catch` の中で新たに例外を起こす処理（ログ出力先への書き込み失敗など）を入れる場合、無限ループにならないよう注意する

> **警告**: 本章のロールバック例は学習用の簡略構成である。本番環境でのロールバックは、対象システムの整合性制約（外部連携、キャッシュ、依存サービス）を踏まえて個別に設計すること。

---

## 8.13 テスト方法

リトライロジックは、失敗回数を制御できるダミー関数でテストする。

```python
import pytest

from samples.python.retry_backoff import PermanentError, RetryableError, retry_with_backoff


def test_retry_succeeds_after_failures(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = {"count": 0}

    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] < 3:
            raise RetryableError("temporary")
        return "ok"

    assert retry_with_backoff(flaky, max_attempts=5, base_delay=0.01) == "ok"
    assert calls["count"] == 3


def test_permanent_error_not_retried(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = {"count": 0}

    def always_permanent() -> None:
        calls["count"] += 1
        raise PermanentError("bad credentials")

    with pytest.raises(PermanentError):
        retry_with_backoff(always_permanent, max_attempts=5, base_delay=0.01)
    assert calls["count"] == 1


def test_gives_up_after_max_attempts(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)

    def always_retryable() -> None:
        raise RetryableError("still failing")

    with pytest.raises(RetryableError):
        retry_with_backoff(always_retryable, max_attempts=3, base_delay=0.01)
```

`time.sleep` をモックすることで、指数バックオフのテストが実時間を待たずに実行できる。
`calls["count"]` のように呼び出し回数を数え、リトライ回数と打ち切り条件を検証する。

Bash:

```bash
source samples/bash/08_retry_backoff.sh
set +e

attempt_count=0
flaky() {
  attempt_count=$(( attempt_count + 1 ))
  [[ "${attempt_count}" -ge 3 ]]
}

retry_with_backoff 5 0 flaky
[[ "$?" -eq 0 ]] || { echo "fail: should eventually succeed" >&2; exit 1; }
[[ "${attempt_count}" -eq 3 ]] || { echo "fail: unexpected attempt count ${attempt_count}" >&2; exit 1; }
echo ok
```

---

## 章末問題

1. リトライしてよい失敗と、リトライしてはいけない失敗を、HTTPステータスコードを例に3つずつ挙げよ。
2. `except Exception: pass` がなぜ危険か、想定外のバグを例に説明せよ。
3. Bashの `trap ... ERR` が発火しない条件を、`if` の条件式を例に説明せよ。
4. 部分成功を全体成功として報告した場合、監視やアラートにどのような悪影響が出るか述べよ。
5. 利用者向けメッセージに詳細なスタックトレースを含めるべきでない理由を、セキュリティの観点で述べよ。

## 解答と解説

1. リトライしてよい: 429、502、503。リトライしてはいけない: 400、401、403。
2. 意図した例外だけでなく、`TypeError` や `AttributeError` のようなコードのバグまで握りつぶし、発見が遅れる。
3. `if false; then :; fi` のように、条件式として評価されたコマンドの失敗は、`set -e` による終了もERRトラップも発火しない設計になっている。
4. 失敗が可視化されず、対応が遅れる。監視が「全体成功」を根拠にアラートを出さず、実際には一部の対象が壊れたまま放置される。
5. スタックトレースには内部のファイルパス、使用ライブラリ、時には設定値が含まれ、攻撃者に有用な情報を与える可能性がある。

---

## 実装演習

1. `08_retry_backoff.py` に、`Retry-After` ヘッダー相当の値を受け取り、指数バックオフより優先して待機時間を決める機能を追加せよ。
2. Bash版の `retry_with_backoff` に、特定の終了コード（例: 124のタイムアウト）だけをリトライ対象にし、それ以外は即座に打ち切る分岐を追加せよ。
3. PowerShell版で、`PermanentErrorException` に相当するカスタム例外クラスを定義し、リトライ対象外として扱うテストを書け。

---

## 次章予告

第9章では、ログを扱う。
printとログの違い、ログレベル、構造化ログ、実行ID、秘密情報のマスキングを三言語で実装する。
