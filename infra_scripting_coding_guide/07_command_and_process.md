# 第7章 コマンド実行とプロセス制御

## 学習目標

この章を終えると、次ができるようになる。

- 外部コマンドの引数を安全に渡し、シェルインジェクションを避けられる
- 標準出力と標準エラーを分離して取得し、終了コードで成否を判定できる
- タイムアウトと並列実行数の制限を付けて外部コマンドを呼べる
- コマンドが存在しない場合を検出し、利用者向けに分かりやすく報告できる
- Python subprocess、Bashのパイプとリダイレクト、PowerShellパイプラインを使い分けられる

前提: 第1章の終了コード、第5章の関数分割、第6章のファイル操作。

サンプルコードは学習用である。本番で実行するコマンドと権限は、対象システムで事前に確認すること。

---

## 7.1 基本概念

**外部コマンド実行**は、スクリプトが自分自身とは別のプロセスを起動し、その結果を利用することである。

インフラ運用スクリプトは、OS標準コマンド（`ping`、`systemctl`、`ssh`）や、他社製CLIツールを呼び出すことが多い。
すべてを自前で再実装するのではなく、既にあるコマンドと組み合わせる発想が土台になる。

外部コマンドを呼ぶたびに、次を意識する。

1. 引数はどう安全に渡すか
2. 標準出力・標準エラーをどう受け取るか
3. 終了コードをどう判定するか
4. いつまで待つか（タイムアウト）
5. コマンドが無い場合にどう振る舞うか

---

## 7.2 安全な引数渡し

**シェル文字列連結**は、コマンドと引数を一つの文字列として組み立て、シェルに解釈させる方式である。
**リスト渡し**（配列渡し）は、コマンド名と各引数を別々の要素として渡し、シェルの解釈を経由しない方式である。

リスト渡しでは、引数の中に空白や特殊文字が含まれても、それが一つの値として扱われる。
シェル文字列連結では、値の中身次第でコマンドの構造そのものが変わってしまう。

### 悪いコード

```python
import subprocess

hostname = "web01.example.invalid; rm -rf /tmp/work"
subprocess.run(f"ping -c 1 {hostname}", shell=True)  # 危険
```

`hostname` に `;` 以降のコマンドが混ざっていると、`ping` の後に別コマンドとして実行されてしまう。
利用者入力や設定ファイルから取得した値を、そのままシェル文字列へ埋め込むと同じ危険がある。

### 改善後

```python
import subprocess

hostname = "web01.example.invalid; rm -rf /tmp/work"
result = subprocess.run(
    ["ping", "-c", "1", hostname],
    capture_output=True,
    text=True,
    check=False,
)
# hostname 全体が1つの引数として ping に渡る。シェルは介在しない。
```

`shell=True` を使わない限り、`;` や `$( )` はシェルのメタ文字として解釈されない。
`hostname` はそのまま `ping` コマンドの一つの引数として渡り、意図しないコマンド実行は起きない。

Bashでは、変数展開の際に必ず引用符で囲む。

```bash
hostname='web01.example.invalid; rm -rf /tmp/work'

# 悪い例: 引用符なし。単語分割とグロブ展開が起きる
ping -c 1 $hostname

# 改善: 必ず引用符で囲む
ping -c 1 "${hostname}"
```

引用符で囲んでも、`hostname` の値そのものが `ping` の引数として渡るだけであり、シェルコマンドとして再解釈はされない。
ただし、値を `eval` や `bash -c "..."` に渡す設計は、引用符の有無に関わらず危険である（7.8節）。

PowerShell:

```powershell
$hostName = 'web01.example.invalid; Remove-Item C:\work -Recurse'

# 外部コマンド呼び出しでは、引数は配列として渡す
& ping -n 1 $hostName

# Invoke-Expression には絶対に文字列連結を渡さない
# Invoke-Expression "ping -n 1 $hostName"  # 危険。書いてはいけない
```

`&`（呼び出し演算子）で外部コマンドを実行すると、以降の引数はそれぞれ独立した値として渡る。
`Invoke-Expression` は文字列をPowerShellのコードとして評価するため、`eval` と同種の危険を持つ。

---

## 7.3 stdout/stderrの取得

Python:

```python
import subprocess

result = subprocess.run(
    ["df", "-h", "/"],
    capture_output=True,
    text=True,
    check=False,
)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("returncode:", result.returncode)
```

`capture_output=True` は `stdout=subprocess.PIPE, stderr=subprocess.PIPE` の短縮形である。
`text=True` を付けると、結果がバイト列ではなく文字列として得られる。

Bash:

```bash
# stdoutとstderrを別々の変数に取る
stdout="$(df -h / 2>/tmp/df_stderr.$$)"
stderr="$(cat /tmp/df_stderr.$$)"
rm -f "/tmp/df_stderr.$$"
exit_code=$?

echo "stdout: ${stdout}"
echo "stderr: ${stderr}"
```

Bashでコマンド置換 `$( )` を使うと標準出力だけが取れる。
標準エラーも変数に取りたい場合は、一時ファイルへリダイレクトするか、`{stdout,stderr}` を両方使うプロセス置換を使う。

```bash
# プロセス置換を使う方法（Bash 4以降）
exec 3>&1
stdout="$(df -h / 2>&2 1>&3)"
exec 3>&-
```

複雑になりやすいので、両方を厳密に分離したい場合は一時ファイル方式のほうが読みやすいことが多い。

PowerShell:

```powershell
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = 'df'
$psi.ArgumentList.Add('-h')
$psi.ArgumentList.Add('/')
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false

$process = [System.Diagnostics.Process]::Start($psi)
$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()

Write-Output "stdout: $stdout"
Write-Output "stderr: $stderr"
Write-Output "exit code: $($process.ExitCode)"
```

`& command 2>&1` のような単純な呼び出しでも動くが、標準出力と標準エラーが混ざってしまう。
両方を分離して扱いたい場合は `System.Diagnostics.Process` を直接使うほうが確実である。

---

## 7.4 終了コード

各言語で、直前に実行した外部コマンドの終了コードを取得する方法が異なる。

| 言語 | 取得方法 |
|------|----------|
| Python | `subprocess.run(...).returncode` |
| Bash | `$?`（直前のコマンド）、`${PIPESTATUS[@]}`（パイプの各段階） |
| PowerShell | `$LASTEXITCODE`（ネイティブコマンド）、`$?`（成功/失敗の真偽） |

Bashのパイプでは、最後のコマンドの終了コードだけが `$?` に入る。
途中のコマンドが失敗しても、最後が成功すれば `$?` は0になる。

```bash
false | true
echo "$?"          # 0 になる（最後の true の結果）
echo "${PIPESTATUS[@]}"   # 1 0 （各段階の結果）
```

パイプの途中の失敗を検知したい場合は `set -o pipefail` を有効にする（第1章から本書で使っている `set -euo pipefail` に含まれる）。

```bash
set -euo pipefail
false | true
# pipefail により、パイプ全体が失敗として扱われスクリプトが止まる
```

PowerShellのネイティブコマンド呼び出しは、成功しても `$LASTEXITCODE` が更新されないことがある点に注意する。
呼び出し直後に必ず確認する。

```powershell
& ping -n 1 'web01.example.invalid' | Out-Null
if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("ping failed with exit code $LASTEXITCODE")
}
```

---

## 7.5 タイムアウト

タイムアウトの無い外部コマンド呼び出しは、応答しないホストやハングしたプロセスに引きずられ、スクリプト全体を止める。

Python:

```python
import subprocess

try:
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "web01.example.invalid", "uptime"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
except subprocess.TimeoutExpired:
    print("command timed out")
```

`timeout` を超えるとプロセスは強制終了され、`TimeoutExpired` 例外が発生する。

Bash:

```bash
if ! timeout 10 ssh -o BatchMode=yes web01.example.invalid uptime; then
  echo "command failed or timed out" >&2
fi
```

`timeout` コマンドの終了コード124は、タイムアウトによる強制終了を意味する。

```bash
timeout 10 sleep 30
echo "$?"   # 124
```

macOS標準の `/usr/bin` には `timeout` が入っていない。
Homebrewの `coreutils`（`brew install coreutils`）を入れると `gtimeout` として使えるが、常に入っているとは限らない。
`timeout` が無い環境向けに、バックグラウンド実行と `kill` で代替する移植性の高い実装を用意しておくと安全である。

```bash
# timeout コマンドが無い環境向けの代替実装
# 戻り値は GNU timeout に合わせ、打ち切り時は124を返す
portable_timeout() {
  local secs="$1"
  shift
  "$@" &
  local cmd_pid=$!

  (
    sleep "${secs}"
    kill -0 "${cmd_pid}" 2>/dev/null && kill -TERM "${cmd_pid}" 2>/dev/null
  ) &
  local watcher_pid=$!

  local rc
  wait "${cmd_pid}"
  rc=$?

  # watcherがまだ生きていればコマンドはタイムアウト前に終わっている
  if kill -0 "${watcher_pid}" 2>/dev/null; then
    kill "${watcher_pid}" 2>/dev/null
    wait "${watcher_pid}" 2>/dev/null || true
    return "${rc}"
  fi
  return 124
}
```

PowerShell（`.NET` のプロセスAPIでタイムアウトを実装する）:

```powershell
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = 'ssh'
foreach ($a in @('-o', 'BatchMode=yes', 'web01.example.invalid', 'uptime')) {
    $psi.ArgumentList.Add($a)
}
$psi.UseShellExecute = $false

$process = [System.Diagnostics.Process]::Start($psi)
if (-not $process.WaitForExit(10000)) {
    $process.Kill()
    [Console]::Error.WriteLine('command timed out')
}
```

`Start-Process -Wait` にはタイムアウト引数が無いため、`WaitForExit(milliseconds)` を使う方法が確実である。

---

## 7.6 並列実行

多数のホストへ直列で処理を行うと、1台あたり数秒の遅延でも合計時間が大きくなる。
同時実行数を制限した並列化で短縮できる。

Python（`concurrent.futures`）:

```python
from __future__ import annotations

import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping_host(host: str, timeout: int) -> tuple[str, bool]:
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), host],
        capture_output=True,
        timeout=timeout + 2,
        check=False,
    )
    return host, result.returncode == 0


def ping_all(hosts: list[str], timeout: int, max_workers: int = 8) -> dict[str, bool]:
    results: dict[str, bool] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(ping_host, host, timeout): host for host in hosts}
        for future in as_completed(futures):
            host, ok = future.result()
            results[host] = ok
    return results
```

`max_workers` で同時実行数を絞る。
無制限に並列化すると、対象ホスト側やネットワーク帯域を圧迫する場合がある。

Bash（`xargs -P` で並列化する）:

```bash
cat config/hosts.txt | grep -v '^#' | grep -v '^\s*$' | \
  xargs -P 8 -I{} timeout 3 ping -c 1 {} >/tmp/ping_out.$$ 2>&1
```

`xargs -P N` は、1行につき1コマンドを起動し、同時実行数をNに制限する。
結果の集計や終了コードの合成は別途必要になる（`xargs` 自体は各コマンドの終了コードを合成しない）。

PowerShell 7（`ForEach-Object -Parallel`）:

```powershell
$hosts = Get-Content -LiteralPath 'config/hosts.txt' | Where-Object { $_ -and -not $_.StartsWith('#') }

$results = $hosts | ForEach-Object -Parallel {
    $h = $_
    $ok = Test-Connection -ComputerName $h -Count 1 -Quiet -TimeoutSeconds 3
    [pscustomobject]@{ Host = $h; Ok = $ok }
} -ThrottleLimit 8

$results
```

`-ThrottleLimit` が同時実行数の上限である。
`ForEach-Object -Parallel` はPowerShell 7以降の機能であり、Windows PowerShell 5.1には無い。

---

## 7.7 子プロセスと後始末

タイムアウトで親プロセスが待つのをやめても、子プロセス（および孫プロセス）が生き残ることがある。
特にシェル経由で起動した場合、シェルプロセスだけが終了し、その配下のコマンドが残るケースがある。

Python:

```python
import subprocess

process = subprocess.Popen(
    ["long_running_tool", "--arg", "value"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
try:
    stdout, stderr = process.communicate(timeout=30)
except subprocess.TimeoutExpired:
    process.kill()
    stdout, stderr = process.communicate()
    raise
```

`process.kill()` は直接の子プロセスを止める。
子プロセスがさらに孫プロセスを起動している構成では、プロセスグループごと止める必要がある場合がある（`os.killpg` など、OS依存の対応が要る）。

Bashでは、`trap` でスクリプト終了時に子プロセスを確実に片付ける。

```bash
#!/usr/bin/env bash
set -euo pipefail

long_running_tool --arg value &
child_pid=$!

cleanup() {
  kill "${child_pid}" 2>/dev/null || true
}
trap cleanup EXIT

wait "${child_pid}"
```

PowerShellでは、`finally` で確実に `Stop-Process` する。

```powershell
$process = Start-Process -FilePath 'long_running_tool' -ArgumentList '--arg', 'value' -PassThru
try {
    if (-not $process.WaitForExit(30000)) {
        throw 'timed out'
    }
}
finally {
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
    }
}
```

---

## 7.8 シェルインジェクション対策

**シェルインジェクション**は、利用者が制御できる入力がシェルコマンドの一部として解釈され、意図しない処理を実行させられる脆弱性である。

対策の優先順位:

1. 可能な限りシェルを経由しない（Pythonの `shell=False`、PowerShellの `&` 呼び出し演算子）
2. どうしてもシェル文字列を組み立てる必要がある場合、言語のクォート関数を使う（`shlex.quote` など）
3. 利用者入力は、コマンドではなく引数の値としてのみ渡す
4. 許可された値の集合（ホスト名の形式、既知のサブコマンド名）で検証してから使う

```python
import shlex

hostname = "web01.example.invalid"
quoted = shlex.quote(hostname)
# それでも shell=True 自体を避けるのが最善である
```

`shlex.quote` はBash向けのクォートである。
PowerShellやWindowsのコマンド解釈規則は異なるため、そのまま流用できない。
最も安全なのは、どの言語でも「シェル文字列を組み立てない」ことである。

---

## 7.9 コマンド不存在の検出

対象環境にコマンドが無い場合、分かりにくいエラーで落ちるより、明示的に検出して報告するほうが運用しやすい。

Python:

```python
import shutil
import subprocess

def run_if_available(cmd: str, args: list[str]) -> subprocess.CompletedProcess[str] | None:
    if shutil.which(cmd) is None:
        return None
    return subprocess.run([cmd, *args], capture_output=True, text=True, check=False)
```

`shutil.which` はPATH上にコマンドがあるかを確認する。
呼び出す前に確認すれば、`FileNotFoundError` を捕まえる代わりに、事前分岐で処理できる。

Bash:

```bash
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required but not installed" >&2
  exit 1
fi
```

`command -v` はBash組み込みであり、`which` の外部コマンドに依存しない分、環境差が少ない。

PowerShell:

```powershell
if (-not (Get-Command -Name 'jq' -ErrorAction SilentlyContinue)) {
    [Console]::Error.WriteLine('jq is required but not installed')
    exit 1
}
```

---

## 7.10 実務向けサンプル: 汎用コマンドランナー

要件:

- 任意の外部コマンドを、引数リストとタイムアウト付きで実行する
- 標準出力と標準エラーを分離して返す
- コマンドが存在しない、タイムアウトした、非0で終了した、をそれぞれ区別できる終了コードにする

### 悪いコード

```python
import subprocess

def run_bad(cmd_string: str) -> str:
    # shell=True + 文字列連結。タイムアウトも無い。
    return subprocess.check_output(cmd_string, shell=True, text=True)
```

問題点:

- `cmd_string` に利用者由来の値が混ざるとシェルインジェクションになる
- タイムアウトが無く、応答しないコマンドで無限に待つ
- 標準エラーと終了コードの扱いが呼び出し側に委ねられていない
- コマンド不存在時の挙動が `CalledProcessError` 任せで分かりにくい

### 改善後

完全な実行可能ファイルは `samples/python/07_run_command.py`、`samples/bash/07_run_command.sh`、`samples/powershell/07_run_command.ps1` に置く。
骨子は次のとおりである。

```python
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

EXIT_OK = 0
EXIT_COMMAND_NOT_FOUND = 1
EXIT_NONZERO = 2
EXIT_TIMEOUT = 4


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    returncode: int
    exit_code: int


def run_command(args: list[str], timeout: int) -> CommandResult:
    if not args:
        raise ValueError("args must not be empty")
    if shutil.which(args[0]) is None:
        return CommandResult(stdout="", stderr=f"command not found: {args[0]}", returncode=-1, exit_code=EXIT_COMMAND_NOT_FOUND)

    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CommandResult(stdout="", stderr=f"timed out after {timeout}s", returncode=-1, exit_code=EXIT_TIMEOUT)

    exit_code = EXIT_OK if completed.returncode == 0 else EXIT_NONZERO
    return CommandResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
        exit_code=exit_code,
    )
```

`run_command` は引数をリストで受け取り、`shell=True` を一切使わない。
呼び出し元は `exit_code` を見るだけで、コマンド不存在・非0終了・タイムアウトを区別できる。

---

## 7.11 セキュリティ上の注意点

- `shell=True`、`Invoke-Expression`、Bashの `eval` に利用者入力を渡さない
- 引数に秘密情報を渡すと、`ps` や `Get-Process` のコマンドライン表示で見える場合がある。環境変数や標準入力経由の方が安全なことが多い
- 外部コマンドの標準出力をそのまま別のコマンドへ渡す前に、想定した形式かを検証する
- タイムアウトを必ず設定する。特に外部ネットワーク越しのコマンドは、対象側の障害が自スクリプトの障害に伝播しやすい
- 並列実行数を無制限にしない。対象システムへの意図しない高負荷を避ける

> **警告**: 本章のコマンド不存在検出やタイムアウトの例は学習用の簡略構成である。本番の並列実行数やタイムアウト値は、対象システムの許容量に応じて個別に検討すること。

---

## 7.12 テスト方法

外部コマンドをテストするときは、実コマンドに依存しない部分と依存する部分を分ける。

```python
from samples.python.run_command import run_command


def test_command_not_found() -> None:
    result = run_command(["definitely-not-a-real-command-xyz"], timeout=5)
    assert result.exit_code == 1


def test_nonzero_exit() -> None:
    result = run_command(["false"], timeout=5)
    assert result.exit_code == 2


def test_success() -> None:
    result = run_command(["echo", "hello"], timeout=5)
    assert result.exit_code == 0
    assert "hello" in result.stdout


def test_timeout() -> None:
    result = run_command(["sleep", "5"], timeout=1)
    assert result.exit_code == 4
```

`echo`、`false`、`sleep` はほぼ全環境に存在するため、実コマンドへの依存を許容してテストを書く。
移植性が必要な場合は、`sys.executable` でPython自身を子プロセスとして起動し、テスト専用の疑似コマンドとして使う方法もある。

Bash:

```bash
source samples/bash/07_run_command.sh
# サンプルは set -euo pipefail を含むため、source した側にも
# errexit が伝播する。個々の呼び出しの終了コードを判定したいテスト
# コードでは、いったん set +e で無効化する。
set +e

run_command 5 definitely-not-a-real-command-xyz
[[ "$?" -eq 1 ]] || { echo "fail: not found" >&2; exit 1; }

run_command 5 false
[[ "$?" -eq 2 ]] || { echo "fail: nonzero" >&2; exit 1; }

run_command 5 echo hello
[[ "$?" -eq 0 ]] || { echo "fail: success" >&2; exit 1; }

echo ok
```

---

## 章末問題

1. `subprocess.run(f"ping {host}", shell=True)` と `subprocess.run(["ping", host])` の違いを、シェルインジェクションの観点で説明せよ。
2. `set -o pipefail` を付けない場合、パイプの途中で失敗したコマンドがどのように無視されるか例を挙げよ。
3. `ForEach-Object -Parallel` の `-ThrottleLimit` を大きくしすぎたときに起きうる問題を述べよ。
4. `shutil.which` や `command -v` で事前にコマンドの有無を確認する利点を、例外処理だけに頼る場合と比較して述べよ。
5. `process.kill()` を呼んでも子プロセスの孫プロセスが残ることがある理由を説明せよ。

## 解答と解説

1. `shell=True` はシェルに文字列を渡して解釈させるため、`host` にメタ文字が含まれると別コマンドとして実行されうる。リスト渡しはシェルを経由せず、値がそのまま1引数になる。
2. 途中のコマンドが失敗しても、パイプ全体の終了コードは最後のコマンドの結果になり、失敗が握りつぶされる。
3. 対象ホストやAPIへの同時接続数が増えすぎ、相手側のリソースを圧迫したり、レート制限に引っかかったりする。
4. 事前確認は、失敗の原因が「コマンド不存在」であることを明示的に分岐でき、例外の種類を都度判定する必要が無い。エラーメッセージも利用者向けに整えやすい。
5. `kill()` は直接の子プロセスにしかシグナルを送らない。孫プロセスは別のプロセスグループやセッションに属している場合があり、明示的にプロセスツリーごと止める処理が必要になる。

---

## 実装演習

1. `07_run_command.py` に、標準出力を1万行を超えたら打ち切るオプションを追加せよ。理由と挙動をログに残すこと。
2. Bash版の `run_command` を使い、`config/hosts.txt` の各ホストへ `ping` をタイムアウト付きで並列実行し、結果をCSVへ集計するスクリプトを書け。
3. PowerShell版で、`Start-Process` ベースの実装と `System.Diagnostics.Process` ベースの実装を両方書き、標準出力・標準エラーの扱いの違いを確認せよ。

---

## 次章予告

第8章では、エラー処理を体系的に扱う。
例外と終了コードの使い分け、リトライと指数バックオフ、部分成功とロールバック、利用者向けメッセージと調査用ログの分離を三言語で実装する。
