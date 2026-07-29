# 第4章 制御構文

## 学習目標

- if / switch(case) / for / while / break / continue を三言語で使える
- 比較演算子と論理演算子の言語差を説明できる
- ネストを浅くし、早期リターンと異常系先行で読める分岐を書ける

---

## 4.1 基本概念

**制御構文**は、実行の流れを分岐・反復させる構文である。

運用スクリプトでは、正常系より異常系の分岐が多い。深くなる前に、関数の入口で不正を弾く。

---

## 4.2 最小構成のコード

閾値判定だけの最小例である。入力検証と終了コードはまだ薄い。

Python:

```python
#!/usr/bin/env python3
import sys

usage = float(sys.argv[1])
if usage >= 90:
    print("CRITICAL")
elif usage >= 80:
    print("WARNING")
else:
    print("OK")
```

Bash:

```bash
#!/usr/bin/env bash
usage="$1"
if (( usage >= 90 )); then
  echo CRITICAL
elif (( usage >= 80 )); then
  echo WARNING
else
  echo OK
fi
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
param([int]$Usage)
if ($Usage -ge 90) { 'CRITICAL' }
elseif ($Usage -ge 80) { 'WARNING' }
else { 'OK' }
```

問題点（この最小構成）:

- 引数不足や非数値が未処理
- 終了コードが常に0に近い
- ログがない
- warn/crit を変更できない

実務向けの改善は 4.9 節と `samples/` を参照する。

---

## 4.3 if

Python:

```python
if usage >= crit:
    status = "CRITICAL"
elif usage >= warn:
    status = "WARNING"
else:
    status = "OK"
```

Bash:

```bash
if [[ "${usage}" -ge "${crit}" ]]; then
  status=CRITICAL
elif [[ "${usage}" -ge "${warn}" ]]; then
  status=WARNING
else
  status=OK
fi
```

PowerShell:

```powershell
if ($Usage -ge $Crit) {
    $status = 'CRITICAL'
}
elseif ($Usage -ge $Warn) {
    $status = 'WARNING'
}
else {
    $status = 'OK'
}
```

Bashの `[[ ]]` を使う。古い `[ ]` より安全で機能が多い。

---

## 4.4 switch / case

Bashの `case`:

```bash
case "${status}" in
  OK) echo 0 ;;
  WARNING) echo 0 ;;
  CRITICAL) echo 3 ;;
  *) echo 2 ;;
esac
```

PowerShellの `switch`:

```powershell
switch ($status) {
    'OK' { 0 }
    'WARNING' { 0 }
    'CRITICAL' { 3 }
    default { 2 }
}
```

Pythonは 3.10以降で `match` がある。単純な対応表なら辞書でもよい。

```python
EXIT_BY_STATUS = {"OK": 0, "WARNING": 0, "CRITICAL": 3}
code = EXIT_BY_STATUS.get(status, 2)
```

---

## 4.5 for / while / break / continue

Python:

```python
for host in hosts:
    if host in skip:
        continue
    if hard_fail(host):
        break
```

Bash:

```bash
for host in "${hosts[@]}"; do
  [[ -n "${skip[${host}]+x}" ]] && continue
  ping -c1 "${host}" || break
done
```

PowerShell:

```powershell
foreach ($host in $hosts) {
    if ($skip -contains $host) { continue }
    if (-not (Test-Connection -ComputerName $host -Count 1 -Quiet)) { break }
}
```

`while` は条件が先に立つ反復である。ファイル読み込みの `while read` が代表例である。

無限ループには必ず打ち切り条件（回数上限、タイムアウト、フラグ）を入れる。

---

## 4.6 条件式、比較、論理演算

| 意味 | Python | Bash `[[ ]]` | PowerShell |
|------|--------|--------------|------------|
| 等しい | `==` | `=` または `==` | `-eq` |
| 異なる | `!=` | `!=` | `-ne` |
| 数値比較 | `<` `>` など | `-lt` `-gt` など | `-lt` `-gt` |
| 論理積 | `and` | `&&` | `-and` |
| 論理和 | `or` | `\|\|` | `-or` |
| 否定 | `not` | `!` | `-not` |

PowerShellで `==` を使うと別意味になる場面がある。比較演算子は `-eq` 系を使う。

文字列と数値の比較を混ぜない。先に型を揃える（第3章）。

---

## 4.7 ネストを深くしない方法

深いネストの徴候:

- 右端にコードが寄っていく
- `else` の対応が目で追えない
- 同じ条件を二重に書いている

対策:

1. 異常を先に `return` / `exit`
2. 判定を関数に切り出す
3. ガード節で階層を減らす
4. 複雑なら表駆動（辞書やcase）にする

---

## 4.8 早期リターンと異常系先行

### 悪いコード

```python
def deploy(config, dry_run: bool) -> int:
    if config is not None:
        if config.get("target"):
            if validate(config):
                if dry_run:
                    print("would deploy")
                    return 0
                else:
                    run_deploy(config)
                    return 0
            else:
                print("invalid")
                return 1
        else:
            print("no target")
            return 1
    else:
        print("no config")
        return 1
```

問題点: 正常系がネストの最深部に埋もれる。失敗経路が散る。

### 改善後

```python
def deploy(config: dict | None, dry_run: bool) -> int:
    if config is None:
        print("no config", file=sys.stderr)
        return 1
    if not config.get("target"):
        print("no target", file=sys.stderr)
        return 1
    if not validate(config):
        print("invalid", file=sys.stderr)
        return 1
    if dry_run:
        print("would deploy", file=sys.stderr)
        return 0
    run_deploy(config)
    return 0
```

Bashでも同じ発想で早期 `exit` する。

```bash
[[ -n "${config_file}" ]] || { echo "no config" >&2; exit 1; }
[[ -f "${config_file}" ]] || { echo "missing file" >&2; exit 1; }
```

PowerShell:

```powershell
function Invoke-Deploy {
    param($Config, [switch]$DryRun)
    if ($null -eq $Config) {
        [Console]::Error.WriteLine('no config')
        return 1
    }
    if (-not $Config.target) {
        [Console]::Error.WriteLine('no target')
        return 1
    }
    if ($DryRun) {
        [Console]::Error.WriteLine('would deploy')
        return 0
    }
    # run deploy
    return 0
}
```

---

## 4.9 実務向けに改善したコード

全文は次を参照する。

- `samples/python/04_classify_usage.py`
- `samples/bash/04_classify_usage.sh`
- `samples/powershell/04_classify_usage.ps1`

改善点:

- 引数の型と範囲を検証する
- warn <= crit を強制する
- CRITICAL は終了コード3、設定誤りは1
- 進捗・エラーは stderr、判定結果は stdout

実行例:

```bash
python3 samples/python/04_classify_usage.py --usage 95
# CRITICAL ; exit 3

python3 samples/python/04_classify_usage.py --usage 85
# WARNING ; exit 0

python3 samples/python/04_classify_usage.py --usage 10 --warn 90 --crit 80
# stderr: warn must be <= crit ; exit 1

bash samples/bash/04_classify_usage.sh --usage 95
pwsh samples/powershell/04_classify_usage.ps1 -Usage 95
```

---

## 4.10 セキュリティ上の注意点

- 利用者入力を条件式に埋め込む前に型と範囲を検証する
- Bashで `eval` による動的分岐を作らない
- PowerShellで `Invoke-Expression` による動的分岐を作らない

---

## 4.11 テスト方法

境界値を表で固定する。実装は `samples/python/04_classify_usage.py` の `classify` を対象にする。

```python
import pytest
from importlib.machinery import SourceFileLoader

mod = SourceFileLoader(
    "classify_usage",
    "samples/python/04_classify_usage.py",
).load_module()


@pytest.mark.parametrize(
    ("usage", "expected"),
    [(79.9, "OK"), (80.0, "WARNING"), (90.0, "CRITICAL")],
)
def test_boundaries(usage, expected):
    assert mod.classify(usage, 80, 90) == expected


def test_warn_gt_crit():
    with pytest.raises(ValueError):
        mod.classify(10, warn=90, crit=80)
```

`tests/test_classify_usage.py` も参照する。

---

## 章末問題

1. ネスト4段の if を、早期リターンで書き直せ（題材は任意でよい）。
2. PowerShellで文字列比較に `==` を使ったときのリスクを調べて書け。
3. `continue` と `break` の違いを、ホスト疎通ループの例で説明せよ。
4. WARNINGを終了コード0にする方針の利点と欠点を述べよ。
5. Bashの `[[ a = b ]]` と `[[ a == b ]]` について、チーム内の統一方針を一つ提案せよ。

## 解答と解説

1. 異常条件を先に return し、最後に正常処理を置く。
2. 代入や意図しない型変換と読み違えやすい。`-eq` を使う。
3. `continue` は次ホストへ。`break` はループ全体を終了。
4. 利点: 監視のCRITICALと分離できる。欠点: WARNING放置が成功扱いになる。レポート必須。
5. 可読性のため `==` に統一する、など。どちらか一方に固定する。

## 実装演習

- `04_classify_usage.py` と同等の判定をBash（整数）とPowerShellで実装する。
- 異常系テストを3本以上書く。

## 次章予告

第5章では関数とモジュールで責務を分け、副作用と純粋関数を意識した再利用を扱う。
