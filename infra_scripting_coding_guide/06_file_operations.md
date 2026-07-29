# 第6章 ファイル操作

## 学習目標

この章を終えると、次ができるようになる。

- テキストとバイナリの違いを理解し、目的に応じたモードでファイルを開ける
- 読み込み、書き込み、追記、ディレクトリ操作、検索を三言語で実装できる
- 一時ファイルとロックを使い、競合を避けたファイル操作を書ける
- 大容量ファイルをメモリに全展開せず処理できる
- 文字コードと改行を意識し、バックアップと原子的な置き換えで安全に更新できる

前提: 第3章の文字コード、第5章の関数分割。

サンプルコードは学習用である。本番のパスやアクセス権限は対象システムで確認すること。

---

## 6.1 基本概念

**テキストファイル**は、文字として解釈できるバイト列を持つファイルである。
**バイナリファイル**は、文字としての解釈を前提としないバイト列を持つファイルである。
画像、証明書、圧縮ファイルはバイナリとして扱う。

テキストとして開くべきファイルをバイナリモードで扱うと、改行の変換が起きずOS間で表示が崩れる。
逆にバイナリファイルをテキストモードで開くと、文字コード変換によってバイト列が壊れる。

Python:

```python
# テキスト
with open("config.yaml", encoding="utf-8") as fh:
    text = fh.read()

# バイナリ
with open("server.crt", "rb") as fh:
    raw = fh.read()
```

Bashは基本的にすべてをバイト列やテキスト行として扱う。
バイナリを厳密に扱う操作（ハッシュ計算、切り出し）は `dd`、`od`、`sha256sum` などの外部コマンドに委ねることが多い。

PowerShell:

```powershell
# テキスト
$text = Get-Content -LiteralPath 'config.yaml' -Raw -Encoding utf8

# バイナリ
$bytes = [System.IO.File]::ReadAllBytes('server.crt')
```

---

## 6.2 読み書き追記

**追記**は、既存の内容を残したまま末尾へ書き加える操作である。

Python:

```python
from pathlib import Path

path = Path("work/events.log")
path.parent.mkdir(parents=True, exist_ok=True)

# 上書き
path.write_text("first\n", encoding="utf-8")

# 追記
with path.open("a", encoding="utf-8") as fh:
    fh.write("second\n")

# 読み込み
lines = path.read_text(encoding="utf-8").splitlines()
```

Bash:

```bash
mkdir -p work
echo "first" > work/events.log     # 上書き
echo "second" >> work/events.log   # 追記
mapfile -t lines < work/events.log
```

PowerShell:

```powershell
New-Item -ItemType Directory -Path 'work' -Force | Out-Null

'first' | Set-Content -LiteralPath 'work/events.log' -Encoding utf8   # 上書き
'second' | Add-Content -LiteralPath 'work/events.log' -Encoding utf8  # 追記

$lines = Get-Content -LiteralPath 'work/events.log'
```

複数プロセスが同じファイルへ同時に追記すると、行の途中で書き込みが混ざることがある。
単一プロセスからの追記に限定するか、6.7節のロックを使う。

---

## 6.3 ディレクトリ操作

Python:

```python
from pathlib import Path

work_dir = Path("work/2026-07-30")
work_dir.mkdir(parents=True, exist_ok=True)

for entry in work_dir.iterdir():
    print(entry.name, entry.is_dir())

work_dir.rmdir()  # 空でなければ失敗する
```

Bash:

```bash
mkdir -p work/2026-07-30
ls -la work/2026-07-30
rmdir work/2026-07-30   # 空でなければ失敗する
```

PowerShell:

```powershell
New-Item -ItemType Directory -Path 'work/2026-07-30' -Force | Out-Null
Get-ChildItem -LiteralPath 'work/2026-07-30'
Remove-Item -LiteralPath 'work/2026-07-30'   # 空でなければ失敗する
```

再帰的な削除（`rm -rf` 相当）は破壊的操作である。

> **警告**: `Path.rmdir()` は空ディレクトリしか消せないが、Pythonの `shutil.rmtree`、PowerShellの `Remove-Item -Recurse`、Bashの `rm -rf` は中身ごと削除する。利用者入力をそのままパスに使わない。対象パスが想定ディレクトリ配下にあることを検証してから呼び出す。

```python
import shutil
from pathlib import Path

base = Path("work").resolve()
target = Path("work/2026-07-30").resolve()

if base not in target.parents and target != base:
    raise ValueError(f"refusing to delete outside of work dir: {target}")

shutil.rmtree(target)
```

---

## 6.4 検索

Python:

```python
from pathlib import Path

root = Path("/var/log/myapp")
for path in root.rglob("*.log"):
    if path.stat().st_size > 0:
        print(path)
```

Bash:

```bash
find /var/log/myapp -type f -name '*.log' -size +0c
```

PowerShell:

```powershell
Get-ChildItem -LiteralPath '/var/log/myapp' -Filter '*.log' -Recurse -File |
    Where-Object { $_.Length -gt 0 }
```

`find` や `Get-ChildItem` の結果をそのまま `rm` や `Remove-Item` に流し込む前に、件数と一覧を確認する運用にする。
第15章の「古いファイルの整理」で、検索と削除を安全に組み合わせる設計を扱う。

---

## 6.5 権限

Python:

```python
import os
import stat
from pathlib import Path

path = Path("work/secret.tmp")
path.write_text("data", encoding="utf-8")
os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 所有者のみ読み書き（0600相当）

mode = path.stat().st_mode
print(oct(stat.S_IMODE(mode)))
```

Bash:

```bash
touch work/secret.tmp
chmod 600 work/secret.tmp
stat -c '%a' work/secret.tmp 2>/dev/null || stat -f '%Lp' work/secret.tmp
```

PowerShell（Windowsのアクセス制御はUnixパーミッションと構造が異なる）:

```powershell
New-Item -ItemType File -Path 'work/secret.tmp' -Force | Out-Null

# Windows: ACLで所有者のみアクセス許可にする例
$acl = Get-Acl -LiteralPath 'work/secret.tmp'
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $env:USERNAME, 'FullControl', 'Allow')
$acl.SetAccessRule($rule)
Set-Acl -LiteralPath 'work/secret.tmp' -AclObject $acl
```

Linux/macOSとWindowsでは権限モデルが異なる。
Unix系はパーミッションビット（所有者/グループ/その他）、Windowsはアクセス制御リスト（ACL）が基本になる。
秘密情報を含むファイルは、作成直後に権限を絞ることを既定の手順にする。

---

## 6.6 一時ファイル

**一時ファイル**は、処理の途中経過を保持するための、短命なファイルである。

自前でファイル名を組み立てると、他プロセスと衝突したり、推測されやすい名前になったりする。
言語標準の一時ファイル機能を使う。

Python:

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, dir="work") as tmp:
    tmp.write("draft content\n")
    tmp_path = Path(tmp.name)

# 検証やコピーが終わってから削除する
tmp_path.unlink()
```

Bash:

```bash
tmp_file="$(mktemp work/tmp.XXXXXX)"
trap 'rm -f "${tmp_file}"' EXIT

echo "draft content" > "${tmp_file}"
# 処理...
```

PowerShell:

```powershell
$tmpFile = [System.IO.Path]::Combine('work', [System.IO.Path]::GetRandomFileName())
try {
    'draft content' | Set-Content -LiteralPath $tmpFile -Encoding utf8
    # 処理...
}
finally {
    Remove-Item -LiteralPath $tmpFile -ErrorAction SilentlyContinue
}
```

一時ファイルは、作成した関数やスクリプトが責任を持って削除する。
Bashの `trap ... EXIT`、Pythonの `try/finally`、PowerShellの `finally` を使い、途中で例外が起きても後始末する（第8章で詳しく扱う）。

---

## 6.7 ファイルロック

**ファイルロック**は、複数プロセスが同じファイルへ同時にアクセスするのを防ぐ仕組みである。

Bashでは `flock` が代表的である。

```bash
#!/usr/bin/env bash
set -euo pipefail

lock_file="work/report.lock"
mkdir -p work

exec 9> "${lock_file}"
if ! flock -n 9; then
  echo "another process holds the lock" >&2
  exit 2
fi

echo "critical section" >> work/report.csv
# ファイルディスクリプタ9が閉じると自動的に解放される
```

Pythonでは、標準ライブラリだけではOS間で統一的なロックAPIが無い。
Unix系では `fcntl.flock`、Windowsでは別のAPIが必要になる。
運用スクリプトでは、対象OSを絞るか、`filelock` のような外部ライブラリを使う判断をする。

```python
import fcntl
from pathlib import Path

lock_path = Path("work/report.lock")
lock_path.parent.mkdir(parents=True, exist_ok=True)

with lock_path.open("w") as lock_fh:
    fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    # クリティカルセクション
    with open("work/report.csv", "a", encoding="utf-8") as report_fh:
        report_fh.write("row\n")
    # withブロックを抜けるとファイルが閉じ、ロックも解放される
```

PowerShellでは、ファイルを排他モードで開くこと自体がロックとして働く。

```powershell
$reportPath = 'work/report.csv'
$stream = [System.IO.File]::Open(
    $reportPath,
    [System.IO.FileMode]::Append,
    [System.IO.FileAccess]::Write,
    [System.IO.FileShare]::None)
try {
    $writer = New-Object System.IO.StreamWriter($stream)
    $writer.WriteLine('row')
    $writer.Flush()
}
finally {
    $stream.Dispose()
}
```

ロックはタイムアウト無しで待ち続けると、障害時にプロセスが詰まる原因になる。
`flock -n`（即座に失敗）や、待ち時間の上限を決めておく。

---

## 6.8 大容量ファイル

数百MBを超えるログを `read()` で一括読み込みすると、メモリを圧迫し、処理開始まで時間がかかる。

Python（1行ずつストリーム処理）:

```python
from pathlib import Path

path = Path("/var/log/myapp/access.log")
error_count = 0
with path.open(encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if "ERROR" in line:
            error_count += 1
print(error_count)
```

Bash:

```bash
grep -c 'ERROR' /var/log/myapp/access.log
```

PowerShell（`Get-Content` は既定で行単位のパイプラインになる。ただし内部実装によっては速度差が出るため、巨大ファイルでは `-ReadCount` や `.NET` のストリームAPIを検討する）:

```powershell
$errorCount = 0
Get-Content -LiteralPath '/var/log/myapp/access.log' -ReadCount 1000 | ForEach-Object {
    $errorCount += ($_ | Select-String -Pattern 'ERROR').Count
}
$errorCount
```

大容量ファイルを扱う設計では、次を先に決める。

1. 全件を保持する必要があるか、集計値だけでよいか
2. 1回のスキャンで済むか、複数回読む必要があるか
3. 途中経過を報告するか（長時間ジョブでの進捗ログ）

---

## 6.9 文字コードと改行

第3章で触れたとおり、文字コードは明示する。
ファイル操作ではさらに、**改行コード**（LF、CRLF）の扱いが重要になる。

| 環境 | 既定の改行 |
|------|------------|
| Linux / macOS | LF (`\n`) |
| Windows | CRLF (`\r\n`) |

Python:

```python
from pathlib import Path

# 読み込み時に自動でLFへ正規化される（universal newlines、既定で有効）
text = Path("config.yaml").read_text(encoding="utf-8")

# 書き込み時の改行を明示する
Path("config.yaml").write_text(text, encoding="utf-8", newline="\n")
```

Bashのテキスト処理は、CRLFが混ざっていると行末に `\r` が残り、比較や正規表現が失敗する原因になる。

```bash
# CRLFをLFへ変換する
sed -i 's/\r$//' config.yaml
```

PowerShell 7の `Set-Content` は既定でOSに応じた改行を使う。
クロスプラットフォームで固定したい場合は、書き込む文字列の改行を明示的に統一する。

```powershell
$normalized = (Get-Content -LiteralPath 'config.yaml' -Raw) -replace "`r`n", "`n"
[System.IO.File]::WriteAllText('config.yaml', $normalized, [System.Text.Encoding]::UTF8)
```

Gitの `core.autocrlf` 設定次第で、コミットとチェックアウトの間に改行が変換される場合がある。
チーム全員が同じ設定を使うよう、`.gitattributes` で改行を固定する運用が安全である。

---

## 6.10 安全な更新: バックアップしてから変更、原子的な置き換え

設定ファイルの更新は、次の二つの事故を避ける設計にする。

1. 書き込み途中でプロセスが落ち、ファイルが壊れたまま残る
2. 変更を戻したいのに、変更前の内容が残っていない

対策は二つある。

- **バックアップ**: 変更前に、日時付きの別名でコピーを残す
- **原子的な置き換え**: 直接上書きせず、一時ファイルに書いてから、OSのリネーム操作で本番ファイルへ差し替える

同一ファイルシステム内でのリネーム（Pythonの `os.replace`、Bashの `mv`、PowerShellの `Move-Item`）は、多くのOSで単一の操作として扱われる。
書き込み途中の中間状態が外部から見えない。

### 悪いコード

```python
from pathlib import Path

def update_config_bad(path: Path, new_content: str) -> None:
    # 直接上書き。書き込み中に失敗すると内容が欠損する。
    # バックアップも無い。
    path.write_text(new_content, encoding="utf-8")
```

問題点:

- 書き込み中にディスク満杯やプロセス強制終了が起きると、ファイルが壊れたまま残る
- 変更前の内容を取り戻す手段が無い
- 変更後の構文チェックをしていない

### 改善後

```python
from __future__ import annotations

import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def backup_path(path: Path, backup_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir / f"{path.name}.{timestamp}.bak"


def update_config(
    path: Path,
    new_content: str,
    backup_dir: Path,
    validate=None,
) -> Path:
    """バックアップを取り、一時ファイル経由で原子的に置き換える。

    validate が渡されれば、書き込み前に新内容を検証する。
    """
    if validate is not None:
        validate(new_content)

    backup = backup_path(path, backup_dir)
    if path.exists():
        shutil.copy2(path, backup)

    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new_content)
        os.replace(tmp_path, path)  # 同一ファイルシステム内で原子的
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    return backup
```

`tempfile.mkstemp` を更新対象と同じディレクトリに作ることが重要である。
別ドライブや別ファイルシステムに作ると、`os.replace` が単純なリネームにならず、コピーと削除に分解されて原子性が失われる場合がある。

Bashでも同じ手順を踏む。

```bash
#!/usr/bin/env bash
set -euo pipefail

update_config() {
  local path="$1" new_content_file="$2" backup_dir="$3"
  local timestamp
  timestamp="$(date -u +%Y%m%dT%H%M%SZ)"

  mkdir -p "${backup_dir}"
  if [[ -f "${path}" ]]; then
    cp -p "${path}" "${backup_dir}/$(basename "${path}").${timestamp}.bak"
  fi

  local tmp_file
  tmp_file="$(mktemp "$(dirname "${path}")/.$(basename "${path}").XXXXXX")"
  trap 'rm -f "${tmp_file}"' RETURN

  cp "${new_content_file}" "${tmp_file}"
  mv "${tmp_file}" "${path}"   # 同一ファイルシステム内でのmvは原子的
  trap - RETURN
}
```

PowerShellでも同様である。

```powershell
function Update-Config {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$NewContent,
        [Parameter(Mandatory = $true)][string]$BackupDir
    )

    $timestamp = [DateTimeOffset]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

    if (Test-Path -LiteralPath $Path) {
        $name = Split-Path -Leaf $Path
        Copy-Item -LiteralPath $Path -Destination (Join-Path $BackupDir "$name.$timestamp.bak")
    }

    $dir = Split-Path -Parent $Path
    $tmpPath = Join-Path $dir ("." + [System.IO.Path]::GetFileName($Path) + "." + [System.IO.Path]::GetRandomFileName())

    try {
        [System.IO.File]::WriteAllText($tmpPath, $NewContent, [System.Text.Encoding]::UTF8)
        Move-Item -LiteralPath $tmpPath -Destination $Path -Force
    }
    catch {
        Remove-Item -LiteralPath $tmpPath -ErrorAction SilentlyContinue
        throw
    }
}
```

完全な実行可能ファイルは `samples/python/06_safe_config_update.py`、`samples/bash/06_safe_config_update.sh`、`samples/powershell/06_safe_config_update.ps1` に置く。

---

## 6.11 セキュリティ上の注意点

- バックアップにも秘密情報が含まれる場合がある。バックアップ先の権限を本体と同等以上に絞る
- 一時ファイルを予測可能な名前や `/tmp` 直下の固定名で作らない。`mktemp` や `tempfile` を使う
- 一時ファイルにも、最終ファイルと同じ権限を設定してからリネームする。既定権限のまま作成すると、一瞬でも緩い権限で内容が露出する
- 検索結果をそのまま削除や上書きに使う前に、対象パスが想定ディレクトリの配下にあるか検証する（パストラバーサル対策の詳細は第10章）
- ロック取得の失敗を握りつぶさない。取得できなければ処理を止め、原因を記録する

> **警告**: この章のコード例は学習用である。本番の設定ファイルを直接対象に実行する前に、バックアップ先の空き容量、権限、対象システムでの動作確認を行うこと。

---

## 6.12 テスト方法

一時ディレクトリを使い、実ファイルシステムに対して検証する。

```python
from pathlib import Path

from samples.python.safe_config_update import update_config


def test_update_config_creates_backup(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    target.write_text("old\n", encoding="utf-8")
    backup_dir = tmp_path / "backups"

    backup = update_config(target, "new\n", backup_dir)

    assert target.read_text(encoding="utf-8") == "new\n"
    assert backup.read_text(encoding="utf-8") == "old\n"


def test_update_config_first_time_no_backup(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    backup_dir = tmp_path / "backups"

    update_config(target, "new\n", backup_dir)

    assert target.read_text(encoding="utf-8") == "new\n"
    assert list(backup_dir.glob("*.bak")) == []


def test_update_config_validation_failure_keeps_original(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    target.write_text("old\n", encoding="utf-8")
    backup_dir = tmp_path / "backups"

    def validate(content: str) -> None:
        if "bad" in content:
            raise ValueError("invalid content")

    try:
        update_config(target, "bad\n", backup_dir, validate=validate)
    except ValueError:
        pass

    assert target.read_text(encoding="utf-8") == "old\n"
```

途中で例外を起こす検証（`validate`）を組み込み、更新前のファイルが変わらないことを確認する点が、この章のテストの要になる。

Bash:

```bash
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

echo "old" > "${tmp_dir}/app.conf"
echo "new" > "${tmp_dir}/new_content.txt"

source samples/bash/06_safe_config_update.sh
update_config "${tmp_dir}/app.conf" "${tmp_dir}/new_content.txt" "${tmp_dir}/backups"

[[ "$(cat "${tmp_dir}/app.conf")" == "new" ]] || { echo "content mismatch" >&2; exit 1; }
ls "${tmp_dir}/backups"/*.bak >/dev/null 2>&1 || { echo "backup missing" >&2; exit 1; }
echo "ok"
```

---

## 章末問題

1. 一時ファイルを対象ファイルと別のファイルシステムに作ると、原子的な置き換えが崩れる理由を説明せよ。
2. `find` の結果をそのまま `rm -rf $(find ...)` に渡す設計の危険を、ファイル名に空白がある場合を例に説明せよ。
3. `flock -n` を使わず、無制限に待つ実装にした場合、障害発生時にどのような問題が起きるか述べよ。
4. WindowsとLinux/macOSで改行コードが異なることが、テキスト処理スクリプトに与える具体的な影響を一つ挙げよ。
5. バックアップ先ディレクトリの権限を本体より緩くしてはいけない理由を述べよ。

## 解答と解説

1. 別ファイルシステムへのリネームは、OSによってコピーと削除に分解されることがあり、その間にファイルが存在しない、または不完全な状態が生じうる。
2. 空白を含むファイル名が単語分割され、意図しないパスや複数の引数に分裂して削除される。`find -print0` と `xargs -0`、または `-exec` を使う。
3. ロック保持プロセスが異常終了しないままハングすると、待機側が永久に処理を進められず、監視やcronジョブが詰まる。
4. 行末に `\r` が残り、正規表現の `$` 一致や文字列完全一致が失敗する。
5. バックアップにも秘密情報や機微な設定が含まれる場合があり、権限が緩いと本体より先に漏えい経路になる。

---

## 実装演習

1. `06_safe_config_update.py` に、直近5世代を超えるバックアップを削除する機能を追加せよ。削除前に一覧をログへ出すこと。
2. Bash版の `update_config` に、書き込み後に任意の検証コマンド（例: `jq empty` でJSON構文チェック）を実行し、失敗時はバックアップから復元する処理を追加せよ。
3. PowerShell版で、`-WhatIf` 相当のドライラン機能（実際には書き込まず、バックアップ先と一時ファイル名だけを表示する）を追加せよ。

---

## 次章予告

第7章では、外部コマンドの安全な実行を扱う。
引数の渡し方、標準出力と標準エラーの分離、終了コード、タイムアウト、並列実行、シェルインジェクション対策を三言語で実装する。
