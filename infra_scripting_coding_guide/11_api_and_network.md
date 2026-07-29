# 第11章 APIとネットワーク処理

## 学習目標

- HTTPの主要メソッドとステータスコードの分類を説明できる
- APIキーとOAuthの概要を理解し、認証付きHTTP呼び出しを実装できる
- タイムアウト、リトライ、ページネーション、レート制限を備えたAPI連携を三言語で書ける
- TLSを有効にしたまま、秘密情報を安全に扱うAPIクライアントを設計できる

前提: 第9章（ログ）、第10章（入力検証、TLS検証、秘密情報）。

サンプルコードは学習用である。
本番のAPIへ接続する前に、対象APIの利用規約、レート制限、認証方式を提供元のドキュメントで確認すること。
本章のAPIホストはすべて `example.invalid` を使う実在しないドメインであり、実行してもネットワーク応答は返らない。

---

## 11.1 基本概念

**HTTP**は、クライアントとサーバーがリクエストとレスポンスをやり取りする通信プロトコルである。

**REST**は、リソースをURLで表し、HTTPメソッドで操作するAPI設計の様式である。
`opsctl` の `api-export` サブコマンドは、REST形式のAPIからホスト情報を取得する想定である。

---

## 11.2 メソッドとステータスコード

| メソッド | 意味 | 冪等性 |
|----------|------|--------|
| `GET` | リソースの取得 | 冪等 |
| `POST` | リソースの新規作成、または処理の実行 | 非冪等 |
| `PUT` | リソースの全体置き換え | 冪等 |
| `PATCH` | リソースの部分更新 | 実装依存（非冪等が多い） |
| `DELETE` | リソースの削除 | 冪等（削除済みへの再実行は成功扱いが多い） |

| ステータス範囲 | 分類 | 代表例 |
|----------------|------|--------|
| 2xx | 成功 | `200 OK`、`201 Created`、`204 No Content` |
| 3xx | リダイレクト | `301 Moved Permanently` |
| 4xx | クライアントエラー | `400 Bad Request`、`401 Unauthorized`、`403 Forbidden`、`404 Not Found`、`429 Too Many Requests` |
| 5xx | サーバーエラー | `500 Internal Server Error`、`503 Service Unavailable` |

`opsctl` のAPI呼び出しでは、4xxを利用者・設定エラー（終了コード1）、5xxと通信断をリトライ対象の実行時エラー（終了コード2、上限超過はタイムアウトで終了コード4）に分類する。

---

## 11.3 JSON入出力の基本

APIのリクエスト本文とレスポンス本文は、JSONで表すことが多い（第3章）。

```python
import json

payload = {"host": "web01.example.invalid", "status": "OK"}
body = json.dumps(payload)
parsed = json.loads(body)
```

---

## 11.4 認証: APIキーとOAuthの概要

**APIキー**は、リクエストに添付する固定の文字列で、送信者を識別・認可する方式である。
`Authorization` ヘッダーやクエリパラメータで送ることが多い。

```text
Authorization: Bearer <token>
```

**OAuth**は、利用者の認可を得たうえで、有効期限付きのアクセストークンを発行する仕組みである。
代表的な流れの一つに、サーバー間連携で使う **クライアントクレデンシャルズフロー**がある。

1. クライアントIDとクライアントシークレットを使い、認可サーバーへトークンを要求する
2. 認可サーバーが、有効期限付きのアクセストークンを返す
3. アクセストークンを `Authorization: Bearer <token>` としてAPIへ送る
4. 期限切れ前に再取得する

本書では、`opsctl` の認証をAPIキー方式（環境変数 `OPSCTL_API_TOKEN`）に統一し、OAuthは概要にとどめる。
OAuthを採用するAPIへ接続する場合は、トークン取得処理を独立した関数にまとめ、有効期限とリフレッシュを管理する。

---

## 11.5 最小構成のAPI呼び出し

Python（`requests`）:

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import requests


def main() -> int:
    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        print("OPSCTL_API_TOKEN is required", file=sys.stderr)
        return 1

    response = requests.get(
        "https://api.example.invalid/v1/hosts",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    print(response.json())
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

PowerShell（`Invoke-RestMethod`）:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

$token = $env:OPSCTL_API_TOKEN
if ([string]::IsNullOrWhiteSpace($token)) {
    [Console]::Error.WriteLine('OPSCTL_API_TOKEN is required')
    exit 1
}

$headers = @{ Authorization = "Bearer $token" }
$result = Invoke-RestMethod -Uri 'https://api.example.invalid/v1/hosts' -Headers $headers -TimeoutSec 10
$result | ConvertTo-Json -Depth 5
```

Bash（curl）:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPSCTL_API_TOKEN:-}" ]]; then
  echo "OPSCTL_API_TOKEN is required" >&2
  exit 1
fi

curl --silent --show-error --fail \
  --max-time 10 \
  -H "Authorization: Bearer ${OPSCTL_API_TOKEN}" \
  "https://api.example.invalid/v1/hosts"
```

三例とも、タイムアウトを明示し、トークンを環境変数から読み、URLとトークンをログへそのまま出さない。

---

## 11.6 タイムアウトとリトライ

タイムアウトを指定しない呼び出しは、相手の応答が無いとき無期限に待ち続ける。
すべてのHTTP呼び出しにタイムアウトを設定する。

**指数バックオフ**は、リトライ間隔を試行のたびに指数関数的に伸ばす方式である。
輻輳している相手へ間隔を空けずに再送すると、状況を悪化させる。

```python
import time

import requests


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    timeout: float,
    max_retries: int,
) -> requests.Response:
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise
            backoff = min(2 ** attempt, 30)
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                return response
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2 ** attempt, 30)
            time.sleep(backoff)
            continue

        return response
```

リトライしてよいのは、通信断・タイムアウト・429・5xxに限る。
400番台の大半（`400`、`401`、`403`、`404`）は入力や認証の誤りであり、再送しても結果は変わらない。

---

## 11.7 ページネーション

**ページネーション**は、大量の結果を複数回のリクエストへ分割して取得する方式である。

カーソル方式の例:

```python
def iter_records(session, base_url, *, timeout, max_retries, page_size=100):
    cursor = None
    while True:
        params = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session, f"{base_url}/v1/hosts", timeout=timeout, max_retries=max_retries
        )
        payload = response.json()
        yield from payload.get("items", [])
        cursor = payload.get("next_cursor")
        if not cursor:
            return
```

オフセット方式のAPIでは、`offset` と `limit` を毎回進め、返却件数が `limit` 未満になった時点で終了する。
どちらの方式でも、上限件数や最大ページ数を設け、想定外に無限ループしないようにする。

---

## 11.8 レート制限対応

**レート制限**は、一定時間内に許可するリクエスト数をサーバー側が制限する仕組みである。
超過すると `429 Too Many Requests` が返り、`Retry-After` ヘッダーで再試行までの待機時間を示すAPIが多い。

```python
if response.status_code == 429:
    retry_after = response.headers.get("Retry-After")
    wait_seconds = float(retry_after) if retry_after else 10.0
    time.sleep(wait_seconds)
```

高頻度に呼ぶ処理では、事前にリクエスト間隔を空ける（クライアント側スロットリング）ことで、429の発生自体を減らせる。

---

## 11.9 TLS

APIホストは `https://` を使い、証明書検証を有効のまま呼び出す（第10章参照）。

```python
# 検証を無効化しない
requests.get("https://api.example.invalid/v1/hosts", timeout=10)

# 社内CAが必要な場合は証明書バンドルを指定する
requests.get(
    "https://api.example.invalid/v1/hosts",
    timeout=10,
    verify="/etc/ssl/certs/internal-ca-bundle.pem",
)
```

---

## 11.10 実務向け改善: opsctl api-exportサブコマンド

`samples/python/11_api_export.py` に、タイムアウト、リトライ、ページネーション、CSV出力をまとめたクライアントを置く。

```python
#!/usr/bin/env python3
"""ページ分割APIからホスト情報を取得し、CSVへ書き出す。

APIホストは example.invalid（実在しないドメイン）を既定にしている。
実際のAPIへ向ける場合は --base-url で上書きし、対象APIの利用規約と
レート制限を事前に確認すること。
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterator

import requests

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_TIMEOUT = 4

logger = logging.getLogger("api_export")

DEFAULT_BASE_URL = "https://api.example.invalid"
TOKEN_ENV_VAR = "OPSCTL_API_TOKEN"


class ApiError(RuntimeError):
    pass


def build_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    return session


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None,
    timeout: float,
    max_retries: int,
) -> requests.Response:
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise ApiError(f"request failed after {attempt} attempts: {exc}") from exc
            backoff = min(2 ** attempt, 30)
            logger.warning(
                "request error (attempt %s/%s): %s; retrying in %ss",
                attempt, max_retries, exc, backoff,
            )
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                raise ApiError(
                    f"request failed with status {response.status_code} after {attempt} attempts"
                )
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2 ** attempt, 30)
            logger.warning(
                "status=%s (attempt %s/%s); retrying in %ss",
                response.status_code, attempt, max_retries, backoff,
            )
            time.sleep(backoff)
            continue

        return response


def iter_records(
    session: requests.Session,
    base_url: str,
    *,
    timeout: float,
    max_retries: int,
    page_size: int = 100,
) -> Iterator[dict[str, Any]]:
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session,
            f"{base_url}/v1/hosts",
            params=params,
            timeout=timeout,
            max_retries=max_retries,
        )
        if response.status_code != 200:
            raise ApiError(f"unexpected status {response.status_code}: {response.text[:200]}")
        payload = response.json()
        for record in payload.get("items", []):
            yield record
        cursor = payload.get("next_cursor")
        if not cursor:
            return


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["host", "status", "last_seen"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in fieldnames})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export host records from an API to CSV")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-retries", type=int, default=3)
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

    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        logger.error("%s is required", TOKEN_ENV_VAR)
        return EXIT_USAGE

    if args.dry_run:
        logger.info("dry-run: would GET %s/v1/hosts and write %s", args.base_url, args.output)
        return EXIT_OK

    session = build_session(token)
    try:
        records = list(
            iter_records(
                session, args.base_url, timeout=args.timeout, max_retries=args.max_retries
            )
        )
    except ApiError as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME
    except requests.Timeout:
        logger.error("request timed out")
        return EXIT_TIMEOUT

    write_csv(args.output, records)
    logger.info("wrote %s records to %s", len(records), args.output)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

`--dry-run` を指定しても、`OPSCTL_API_TOKEN` の存在は確認する。
設定不備を早期に検知するためであり、実際のリクエストは送らない。

---

## 11.11 悪い例と問題点

```python
#!/usr/bin/env python3
import requests

def get_hosts(token, host_filter):
    url = f"https://api.example.invalid/v1/hosts?token={token}&filter={host_filter}"
    response = requests.get(url, verify=False)
    return response.json()
```

問題点:

- トークンをクエリ文字列に埋め込んでおり、アクセスログやブラウザ履歴に残る
- `verify=False` でTLS証明書検証を無効化している
- タイムアウトが無く、応答が無いと無期限に待つ
- ステータスコードを確認せず、失敗時も `response.json()` を呼んで例外の原因が分かりにくい
- リトライが無く、一時的な通信断で処理全体が落ちる

## 11.12 改善後のコード

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import requests


def get_hosts(token: str, host_filter: str, *, timeout: float = 10.0) -> dict:
    response = requests.get(
        "https://api.example.invalid/v1/hosts",
        headers={"Authorization": f"Bearer {token}"},
        params={"filter": host_filter},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        print("OPSCTL_API_TOKEN is required", file=sys.stderr)
        return 1
    try:
        data = get_hosts(token, host_filter="web")
    except requests.HTTPError as exc:
        print(f"api error: {exc}", file=sys.stderr)
        return 2
    except requests.Timeout:
        print("request timed out", file=sys.stderr)
        return 4
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

改善点は、トークンをヘッダーへ移したこと、TLS検証を有効のままにしたこと、タイムアウトの明示、`raise_for_status` によるエラー分岐である。
リトライは11.6・11.10の `get_with_retry` を組み込むことで追加する。

---

## 11.13 セキュリティ上の注意点

- 秘密情報をURLのクエリ文字列に含めない。アクセスログやプロキシのログに残る
- TLS証明書検証を無効化しない（第10章）
- レスポンス本文をそのままログへ出さない。個人情報や内部識別子を含む場合がある（第9章）
- 想定外のフィールドを含むJSON応答をそのまま外部コマンドや別APIへ転送しない。必要なフィールドだけを取り出す
- APIキーやトークンには、必要な操作のみを許可する権限（読み取り専用など）を割り当てる

---

## 11.14 テスト方法

外部APIへ実際に接続せず、HTTP層をモックしてテストする。

```python
import pytest
import requests

from samples.python.api_export import ApiError, get_with_retry


class FakeResponse:
    def __init__(self, status_code: int, payload: dict, headers: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}
        self.text = str(payload)

    def json(self) -> dict:
        return self._payload


class FakeSession:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self._responses = responses
        self.calls = 0

    def get(self, url, params=None, timeout=None):
        response = self._responses[self.calls]
        self.calls += 1
        return response


def test_get_with_retry_succeeds_after_500(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    session = FakeSession(
        [FakeResponse(500, {}), FakeResponse(200, {"items": []})]
    )
    response = get_with_retry(
        session, "https://api.example.invalid/v1/hosts", params=None, timeout=1, max_retries=3
    )
    assert response.status_code == 200
    assert session.calls == 2


def test_get_with_retry_raises_after_exhausting_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    session = FakeSession([FakeResponse(500, {}), FakeResponse(500, {})])
    with pytest.raises(ApiError):
        get_with_retry(
            session, "https://api.example.invalid/v1/hosts", params=None, timeout=1, max_retries=1
        )
```

PowerShellでは、`Invoke-RestMethod` をラップした関数を作り、Pesterの `Mock` で差し替える。

```powershell
Describe 'Get-WithRetry' {
    It 'retries on 500 and succeeds' {
        Mock Invoke-RestMethod { throw 'simulated 500' } -ParameterFilter { $script:CallCount -eq 0 }
        # 実運用のテストでは、モックの呼び出し回数に応じて戻り値を変える実装にする
    }
}
```

---

## 章末問題

### 問題1

`GET` と `POST` の冪等性の違いを、リトライしてよいかどうかの観点から説明せよ。

### 問題2

`429 Too Many Requests` を受け取ったとき、即座に同じ間隔でリトライすることの問題点を述べよ。

### 問題3

APIキーをクエリ文字列に含める設計の危険を、ログの観点から説明せよ。

### 問題4

カーソル方式のページネーションで、`next_cursor` の終了条件を確認しない実装が起こしうる問題を述べよ。

### 問題5

タイムアウトを設定しないHTTP呼び出しが、監視スクリプト全体に与える影響を述べよ。

---

## 解答と解説

### 問題1

`GET` は冪等なので安全にリトライできる。
`POST` は新規作成など副作用を伴うことが多く、無条件のリトライは二重作成を招く。
冪等性キーの付与など、追加の設計が要る。

### 問題2

サーバー側の輻輳を悪化させ、429が続く悪循環になる。
指数バックオフや `Retry-After` の尊重で間隔を空ける。

### 問題3

クエリ文字列はアクセスログやプロキシログに平文で残ることが多く、ログを読める人にトークンが漏れる。
ヘッダーでの送信に切り替える。

### 問題4

終了条件を誤ると無限ループになり、同じページを取得し続けるか、メモリを消費し続ける。
上限ページ数や最大件数を設ける。

### 問題5

相手の応答が無いとき、スクリプト全体が無期限に停止し、後続のホストやサブコマンドの処理が進まなくなる。
監視自体が機能しなくなる。

---

## 実装演習

### 演習A

`11_api_export.py` の `get_with_retry` に、最大待機時間の上限（例: 60秒）を設けるオプションを追加せよ。

### 演習B

Bashでcurlを使い、`429` を受け取った場合に `Retry-After` ヘッダーを読み取って待機するリトライ処理を実装せよ。

### 演習C

PowerShellで `Invoke-RestMethod` をラップし、タイムアウトとリトライを備えたページネーション取得関数を実装せよ。

---

## 次章予告

第12章では、設定ファイルとCLIツールを扱う。
設定とコードの分離、優先順位、サブコマンド設計を通じて、`opsctl` のCLI全体を組み立てる。
