# 第15章 インフラ自動化の実践

## 学習目標

この章を終えると、次ができるようになる。

- 運用題材を要件・入出力・失敗時・dry-run・再実行性まで落として実装できる
- Python / Bash / PowerShell の適性に応じて主実装言語を選べる
- `opsctl` の終了コード、設定ファイル、ログ規約に沿ったサブコマンドを運用できる
- 破壊的操作を、確認とロールバックを前提に扱える

前提:

- 第1章〜第14章の内容
- `config/opsctl.yaml` と `config/hosts.txt` がリポジトリ直下にあること
- 作業ディレクトリは `infra_scripting_coding_guide/` を想定する

> **警告**: 本章の削除、設定上書き、バックアップ整理、サービス再起動系の例は学習用である。対象パスは `./work`、`./backups`、`/tmp/opsctl-lab` などに限定している。本番パスへ向けて `--execute` を付けないこと。

サンプルは本番環境でそのまま安全とは限らない。投入前に付録Cのチェックリストを通すこと。

---

## 基本概念

**インフラ自動化スクリプト**は、手作業の運用手順を、入力・処理・出力・失敗時挙動・再実行性まで固定した実行可能手続きである。

本章では、前章までの部品を組み合わせ、言語適性に応じて題材を実装する。各題材は「動くデモ」ではなく、dry-run、終了コード、監査可能なログを備えた運用単位として扱う。

### 悪いコードの型（共通）

```bash
# 確認なし、ログなし、終了コードなし、パス検証なし
find /var/log -mtime +30 -delete
```

問題点:

- dry-runがない
- 対象範囲が広い
- 失敗しても気づきにくい
- 再実行や監査ができない

### 改善後の型（共通）

1. 対象パスを allowlist で制限する
2. 既定は報告のみ（`--execute` で実作業）
3. 実施前後をCSVまたはログに残す
4. 部分失敗は非0終了コードにする

具体例は 15.4（古いファイル整理）の `samples/python/15_cleanup_old.py` を参照する。

---

## 15.0 章の進め方と共通規約

各節は次の項目で揃える。

1. 要件
2. 入力
3. 出力
4. 処理フロー
5. エラー処理
6. ログ
7. 設定ファイル
8. dry-run
9. 再実行性
10. テスト
11. 実行例
12. 運用上の注意点

共通終了コード（README / 付録B）:

| コード | 意味 |
|--------|------|
| 0 | 成功（警告方針は各コマンドで定義） |
| 1 | 使い方・設定誤り |
| 2 | 実行時エラー（部分失敗を含む） |
| 3 | 監視上の CRITICAL |
| 4 | タイムアウト |
| 130 | Ctrl+C |

統合入口（任意）:

```bash
python3 samples/python/15_opsctl_dispatch.py --help
```

各サブコマンドは独立スクリプトとしても動く。学習時は独立実行を先に確認する。

ラボ用ディレクトリの準備:

```bash
mkdir -p work/logs work/tmp work/quarantine work/reports backups reports /tmp/opsctl-lab
printf 'ERROR connection refused\nINFO started\n' > work/logs/app.log
printf 'old\n' > work/tmp/stale.tmp
touch -d '40 days ago' work/tmp/stale.tmp 2>/dev/null || touch -t 202601010000 work/tmp/stale.tmp
```

---

## 15.1 複数サーバーへの疎通確認

主言語: Python（並列と集計が楽）。補助: Bash。

実装: `samples/python/15_ping_check.py`、`samples/bash/15_ping_check.sh`、基礎版 `samples/python/02_ping_check.py`

### 要件

1. `config/hosts.txt` のホストへ疎通確認する
2. 1ホストあたりのタイムアウトと全体デッドラインを持つ
3. 重要ホスト不通は CRITICAL（終了コード3）として扱う
4. 結果をCSVへ残す
5. dry-runでは ping を送らず予定だけ出す

### 入力

- `--hosts-file` または設定の `ping_check.hosts_file`
- `--timeout`、`--max-workers`、`--deadline-seconds`
- `ping_check.critical_hosts`

### 出力

- CSV: `host,ok,detail,elapsed_ms,critical`
- stderr: 構造化に近いテキストログ
- 終了コード: 全成功0、部分失敗2、重要ホスト失敗3

### 処理フロー

```text
load config and hosts
if dry-run:
  log each planned ping; write dry-run rows; exit 0
ping hosts with limited workers under deadline
classify failures; mark critical hosts
write CSV
return exit code
```

### エラー処理

- ホスト一覧空 / 不正行 → 終了コード1
- `ping` コマンド不存在 → そのホストを ERROR、全体は2
- 全体デッドライン超過 → 未完了を TIMEOUT 扱い、必要なら4または2

### ログ

`INFO host=... ok=... elapsed_ms=...` を stderr へ出す。

### 設定ファイル

```yaml
ping_check:
  hosts_file: ./config/hosts.txt
  timeout_seconds: 3
  max_workers: 8
  deadline_seconds: 60
  critical_hosts:
    - db01.example.invalid
```

### dry-run

実際の ICMP を送らない。レポートには `ok=dry-run` を書く。

### 再実行性

読み取りのみ。何度実行しても副作用はない。

### テスト

- 空ファイルで終了コード1
- dry-runで外部コマンド未呼び出し
- critical ホスト不通で終了コード3

### 実行例

```bash
python3 samples/python/15_ping_check.py --dry-run --report reports/ping-dry.csv --verbose

python3 samples/python/15_ping_check.py \
  --hosts-file config/hosts.txt \
  --timeout 2 \
  --report reports/ping.csv
echo $?
```

Bash補助:

```bash
bash samples/bash/15_ping_check.sh --hosts-file config/hosts.txt --report reports/ping-bash.csv --dry-run
```

### 運用上の注意点

- ICMPが塞がれた網では失敗が増える。TCPポート確認へ切り替える判断が必要
- 大量ホストへの無計画な並列pingは監視やセキュリティ機器に検知されることがある
- macOSとLinuxで `ping -W` の単位が違う。可搬性が要るならPython版を主にする

---

## 15.2 ディスク使用率監視

主言語: Bash / PowerShell（OSの容量情報取得が素直）。補助: Pythonの判定関数（第4章、第13章）。

実装: `samples/bash/15_disk_check.sh`、`samples/powershell/15_disk_check.ps1`

### 要件

1. 指定パスの使用率を取得する
2. warn / crit 閾値で分類する
3. CRITICALが1つでもあれば終了コード3
4. 取得失敗は継続し、終了コード2
5. dry-runではレポート書き込みとアラートコマンドを行わない

### 入力

- `--paths`（複数可、既定 `/`）
- `--warn`、`--crit`
- `--report`、`--alert-command`（信頼できる固定コマンドのみ）

### 出力

- CSV: `path,percent,status,detail`
- 終了コード 0 / 2 / 3

### 処理フロー

```text
validate thresholds
for path in paths:
  get usage via df / Get-PSDrive
  classify
  append row
if not dry-run: write report; maybe run alert command
compute exit code
```

### エラー処理

- 閾値の型・大小不正 → 1
- パスが存在しない / df失敗 → その行 ERROR、全体2
- alertコマンド失敗 → 2（監視通知失敗も失敗）

### ログ

`run_id` 付きで stderr へ INFO/ERROR。

### 設定ファイル

```yaml
defaults:
  disk_warn_percent: 80
  disk_crit_percent: 90
```

### dry-run

閾値判定までは行う。ファイル書き込みと `--alert-command` はスキップ。

### 再実行性

読み取り中心。レポートはタイムスタンプ付きパスを推奨。

### テスト

```bash
bash samples/bash/15_disk_check.sh --paths / --warn 80 --crit 90 --dry-run --verbose
```

境界値は第4章の `classify` を単体テストする。

### 実行例

```bash
bash samples/bash/15_disk_check.sh \
  --paths / --paths /var \
  --warn 80 --crit 90 \
  --report reports/disk.csv
```

```powershell
pwsh samples/powershell/15_disk_check.ps1 -Paths C:\ -Warn 80 -Crit 90 -DryRun
```

### 運用上の注意点

- `/` だけ見てデータパーティションを見落とさない
- `--alert-command` に利用者入力を連結しない（コマンドインジェクション）
- inode不足は使用率と別問題。必要なら別チェックを足す

---

## 15.3 ログファイル検索

主言語: Python（正規表現、大きなファイルのストリーム処理）。

実装: `samples/python/15_log_search.py`

### 要件

1. 複数ディレクトリ配下のログを正規表現で検索する
2. ファイル全体をメモリに載せない
3. バイナリや権限エラーは警告してスキップする
4. マッチ上限とファイル上限を持つ
5. dry-runでは対象ファイル一覧だけ出す

### 入力

- `--pattern`（必須）
- `--target-dir`、`--glob`（既定 `*.log`）
- `--max-files`、`--max-matches`
- 設定 `log_search`

### 出力

- CSV: `path,line_no,line`
- マッチ0でも検索成功なら終了コード0
- 対象ディレクトリ不正は1、読み取り多発失敗は2

### 処理フロー

```text
compile regex
enumerate files under target dirs with glob, up to max-files
if dry-run: list files; exit
for each file, stream lines; collect matches up to max-matches
write report
```

### エラー処理

- 不正正規表現 → 1
- ファイル上限超過 → 警告し打ち切り（仕様としてINFO）
- 個別ファイルの UnicodeDecodeError → 置換またはスキップをログ

### ログ

検索開始、スキップ理由、マッチ件数を INFO/WARNING で残す。

### 設定ファイル

```yaml
log_search:
  target_dirs:
    - ./work/logs
  max_files: 200
  max_matches: 5000
```

### dry-run

パターン適用前に、走査対象ファイルを列挙する。

### 再実行性

読み取りのみ。

### テスト

小さなログを `work/logs` に置き、既知行がマッチすることを確認する。

### 実行例

```bash
python3 samples/python/15_log_search.py \
  --pattern 'ERROR' \
  --target-dir work/logs \
  --report reports/log-search.csv \
  --verbose

python3 samples/python/15_log_search.py \
  --pattern 'ERROR' \
  --target-dir work/logs \
  --dry-run
```

### 運用上の注意点

- 本番ログに個人情報が含まれる場合、レポート保管場所と権限を制限する
- 巨大ディレクトリでは `--max-files` を先に絞る
- 文字コード不明ログは別エンコーディング指定が必要になることがある

---

## 15.4 古いファイルの整理

主言語: Python。

実装: `samples/python/15_cleanup_old.py`

> **警告**: `--action delete --execute` は復元できない削除を行う。既定は dry-run（報告のみ）である。まず `--action quarantine` で隔離運用する。

### 要件

1. 指定日数より古いファイルを候補にする
2. 対象ルートはラボ用パスに限定する（`./work`、`./backups`、`/tmp/opsctl-lab`）
3. 既定は実行せず報告のみ。`--execute` で実作業
4. 削除より隔離を推奨する
5. 実施結果をCSVに残す

### 入力

- `--target-dir`、`--max-age-days`、`--extension`
- `--action quarantine|delete`
- `--quarantine-dir`、`--report`、`--execute`

### 出力

- CSV: `path,action,status,detail`
- 終了コード: 設定誤り1、部分失敗2、成功0

### 処理フロー

```text
validate roots are inside lab allowlist
list candidates by mtime and extension
if not --execute: write planned actions; exit 0
for each candidate:
  quarantine (move) or delete
  append audit row
```

### エラー処理

- allowlist外のパス → 1（拒否）
- 移動/削除失敗 → その行 ERROR、全体2
- 隔離先が対象配下で循環する場合 → 1

### ログ

計画件数、実施件数、拒否パスを残す。

### 設定ファイル

```yaml
cleanup:
  target_dirs:
    - ./work/tmp
  max_age_days: 30
  extensions:
    - ".tmp"
    - ".log"
  quarantine_dir: ./work/quarantine
```

### dry-run

フラグ名は「実行しないのが既定」。`--execute` が無い限り変更しない。

### 再実行性

隔離済みファイルは対象から消える。削除は冪等に近いが、監査CSVは追記または時刻付き新規にする。

### テスト

```bash
python3 samples/python/15_cleanup_old.py --target-dir work/tmp --max-age-days 30 --verbose
# 変更なし

python3 samples/python/15_cleanup_old.py \
  --target-dir /etc --execute
# 拒否され終了コード1であること
```

### 実行例

```bash
python3 samples/python/15_cleanup_old.py \
  --target-dir work/tmp \
  --max-age-days 30 \
  --action quarantine \
  --report reports/cleanup.csv

python3 samples/python/15_cleanup_old.py \
  --target-dir work/tmp \
  --action quarantine \
  --execute \
  --report reports/cleanup-exec.csv
```

### 運用上の注意点

- バックアップ保持と掃除の保持日数を矛盾させない
- cron化する場合も最初の数週間は quarantine のみ
- NFSや共有ディスクでは mtime の解釈差に注意

---

## 15.5 ユーザーアカウント棚卸し

主言語: PowerShell（Windowsローカルユーザー）。補助: Bash（Linuxの passwd 系）。

実装: `samples/powershell/15_user_audit.ps1`、`samples/bash/15_user_audit.sh`

### 要件

1. 有効アカウントを一覧化する
2. パスワード期限なし、長期未ログイン、許可外シェルなどを検出する
3. アカウント変更は行わない（読み取り専用）
4. リスク検出時は終了コード3（方針で2でもよい。実装に従う）

### 入力

- 非アクティブ日数閾値
- 除外アカウント
- Linuxなら `uid_min`、`allowed_shells`

### 出力

- CSV: アカウント名、状態、findings
- dry-runでは列挙予定のみ

### 処理フロー

```text
enumerate accounts
filter excluded / system accounts
evaluate findings
write report
exit non-zero if findings exceed policy
```

### エラー処理

- コマンド非対応OS → 1（案内メッセージ）
- 列挙権限不足 → 2

### ログ

監査対象件数と、検出した finding を INFO/WARNING で残す。パスワード自体は出さない。

### 設定ファイル

```yaml
user_audit:
  uid_min: 1000
  allowed_shells:
    - /bin/bash
    - /usr/sbin/nologin
    - /bin/false
  inactive_days_warn: 90
```

### dry-run

アカウントへの問い合わせをせず、対象名の列挙方針だけを出すか、読み取りのみでレポートを書かない実装にする。各スクリプトのヘルプに従う。

### 再実行性

読み取りのみ。

### テスト

除外リストに入れたアカウントが findings に出ないこと。

### 実行例

```powershell
pwsh samples/powershell/15_user_audit.ps1 -DryRun
pwsh samples/powershell/15_user_audit.ps1 -InactiveDaysWarn 90 -ReportPath work/reports/user_audit.csv
```

```bash
bash samples/bash/15_user_audit.sh --dry-run
bash samples/bash/15_user_audit.sh --report reports/user-audit.csv
```

### 運用上の注意点

- ドメインアカウントは別API（Get-ADUserなど）が必要
- 棚卸し結果は権限情報を含む。レポートのACLを制限する
- 自動無効化までは本章の範囲外。変更は承認後の別手順にする

---

## 15.6 サービス稼働確認

主言語: Bash（systemd）、PowerShell（Windowsサービス）。

実装: `samples/bash/15_service_check.sh`、`samples/powershell/15_service_check.ps1`

### 要件

1. 指定サービスの稼働状態を確認する
2. 停止を検出したら終了コード3（または2。実装の定義に従う）
3. 再起動オプションがある場合は明示フラグでのみ実行する
4. dry-runでは再起動しない

> **警告**: `--restart-on-failure` はサービスに影響する。本番では変更管理なしで定期実行しない。

### 入力

- `--service`（複数）
- init系（systemd/sysv）または Windows サービス名
- `--restart-on-failure`、`--report`、`--dry-run`

### 出力

- CSV: `service,status,detail`
- 終了コード

### 処理フロー

```text
for service:
  query status
  if inactive and restart requested and not dry-run:
    restart and re-query
  record result
write report
```

### エラー処理

- 未知サービス → ERROR行、全体2または3
- 権限不足 → 2
- 再起動失敗 → 3

### ログ

照会結果と、再起動を行ったかどうかを残す。

### 設定ファイル

```yaml
service_check:
  services:
    - sshd
    - cron
```

### dry-run

状態取得は可。再起動は不可。

### 再実行性

確認のみなら安全。再起動付きは「停止時のみ起動」にすると冪等に近づく。

### テスト

存在しないサービス名で ERROR になること。dry-runで restart が呼ばれないこと。

### 実行例

```bash
bash samples/bash/15_service_check.sh --service sshd --dry-run --verbose
bash samples/bash/15_service_check.sh --service sshd --service cron --report reports/services.csv
```

```powershell
pwsh samples/powershell/15_service_check.ps1 -Service Spooler -DryRun
```

### 運用上の注意点

- コンテナや systemd user サービスでは単位名が異なる
- クラスタ管理下のサービスをスクリプトで単独再起動しない
- 起動直後の一時的な inactive を CRITICAL にしないための猶予が必要な場合がある

---

## 15.7 設定ファイルの一括変更

主言語: Python。

実装: `samples/python/15_config_bulk_edit.py`、`samples/python/15_config_patch.py`

> **警告**: 一括置換は影響範囲が広い。必ず差分を確認し、バックアップを取り、変更管理の承認後に `--execute` する。

### 要件

1. 複数ファイルへパターン置換を適用する
2. 書き込み前にタイムスタンプ付きバックアップを取る
3. 既定は dry-run（差分表示のみ）
4. 対象はラボ用ルートに限定する
5. 結果CSVを残す

### 入力

- 対象ディレクトリ、ファイルglob
- 置換ルール（CLIまたはYAMLルールファイル）
- `--execute`

### 出力

- unified diff（dry-run）
- バックアップディレクトリ
- CSV: `path,changed,status`

### 処理フロー

```text
validate roots
load rules
for each file:
  render new content
  if unchanged: skip
  if not execute: show diff
  else: backup; atomic write
```

### エラー処理

- ルール不正 → 1
- バックアップ失敗 → 中断（2）。中途半端な適用を避ける
- 個別書き込み失敗 → 2、適用済み一覧をレポート

### ログ

変更予定数、適用数、バックアップ先を出す。

### 設定ファイル

ルール例は `samples/shared/config_patch_rules.example.yaml` を参照。

### dry-run

書き込みもバックアップも行わない実装（`15_config_patch.py`）と、方針をヘルプで明示する。

### 再実行性

既に置換済みなら差分ゼロでスキップできるルールにする。

### テスト

一時ディレクトリにサンプル設定を置き、dry-run差分 → execute → 再実行で差分ゼロを確認する。

### 実行例

```bash
python3 samples/python/15_config_bulk_edit.py --help
python3 samples/python/15_config_patch.py --help
```

ラボで試す場合も、先にコピーを `work/` 配下へ置いてから対象にする。

### 運用上の注意点

- テンプレート管理（Ansible等）があるなら、そちらの正本を先に直す
- バイナリや証明書ファイルを置換対象に含めない
- ロールバックはバックアップからの復元手順を先に書いてから実行する

---

## 15.8 APIから情報を取得してCSVに出力

主言語: Python。補助: PowerShell。

実装: `samples/python/15_api_to_csv.py`、`samples/python/15_api_export.py`、`samples/powershell/11_api_export.ps1`

### 要件

1. 認証付きHTTP GETでページネーションを辿る
2. タイムアウト、リトライ、429尊重を行う
3. 結果をCSVへ書く
4. トークンは `OPSCTL_API_TOKEN` から読む
5. 既定ベースURLは `https://api.example.invalid`（到達しない）

### 入力

- `--base-url`、`--endpoint`、`--config`
- 環境変数 `OPSCTL_API_TOKEN`
- `--timeout`、`--report`、`--dry-run`

### 出力

- CSV（設定の fields）
- 終了コード 0/1/2/4

### 処理フロー

```text
load config; require token unless dry-run
if dry-run: print planned requests; exit 0
for page in pages:
  GET with timeout and retry
  yield rows
write CSV
```

### エラー処理

- トークン未設定 → 1
- 4xx（401/403等）→ 2（リトライしない）
- 5xx/429 → リトライ後に失敗なら2または4
- JSON不正 → 2

### ログ

URLにトークンを出さない。`Authorization` はマスクする（第9章、第11章）。

### 設定ファイル

```yaml
api:
  base_url: "https://api.example.invalid"
api_to_csv:
  endpoint: /v1/incidents
  fields:
    - incident_id
    - severity
    - host
    - opened_at
```

### dry-run

ネットワーク接続せず、組み立てたURLとページ方針だけを出す。

### 再実行性

同じAPIを再取得する。出力は時刻付きファイルにして上書きしない。

### テスト

`responses` や手書きモックでページ2枚と429を擬似する（第11章、第13章）。

### 実行例

```bash
python3 samples/python/15_api_to_csv.py --dry-run --verbose --output reports/incidents.csv

export OPSCTL_API_TOKEN='replace-me'
python3 samples/python/15_api_to_csv.py \
  --base-url "https://api.example.invalid" \
  --output reports/incidents.csv
# example.invalid は名前解決に失敗するのが正常な学習結果
```

### 運用上の注意点

- 利用規約とレート制限を確認する
- トークンをシェル履歴に残さない（`export` の運用ルールを決める）
- ページサイズを大きくしすぎるとメモリと相手負荷が増える

---

## 15.9 バックアップ処理

主言語: Bash（tarが強い） / Python（検証と整理）。

実装: `samples/bash/15_backup.sh`、`samples/python/15_backup.py`

> **警告**: 保持期間を超えたバックアップ削除は破壊的である。`--prune` や削除処理は dry-runで対象確認してから行う。

### 要件

1. ソースディレクトリをタイムスタンプ付きアーカイブにする
2. バックアップ先は `./backups` など明示パス
3. 保持日数を超えた古い世代を整理できる
4. dry-runでは作成も削除もしない
5. 可能ならチェックサムを記録する

### 入力

- `--source`（複数可）
- `--backup-dir`、`--retention-days`
- `--prune`、`--dry-run`

### 出力

- `backups/backup-YYYYMMDDTHHMMSS.tar.gz` など
- マニフェスト（任意）
- 終了コード

### 処理フロー

```text
validate sources exist
if dry-run: show archive name and prune candidates; exit
create archive atomically (temp then rename)
write checksum
if prune: delete older than retention
```

### エラー処理

- ソース無し → 1
- ディスク満杯 → 2、不完全ファイルを残さない
- 削除失敗 → 2（新規バックアップ成功と分けて報告）

### ログ

アーカイブパス、サイズ、削除した世代を残す。

### 設定ファイル

```yaml
backup:
  source_dirs:
    - ./config
  retention_days: 14
paths:
  backup_dir: ./backups
```

### dry-run

作成予定名と prune 候補だけ表示する。

### 再実行性

毎回新しいタイムスタンプファイルを作る。pruneは保持政策に対して収束する。

### テスト

小さな `config/` をソースに dry-run → 実行 → ファイル存在確認。

### 実行例

```bash
bash samples/bash/15_backup.sh --source config --backup-dir backups --dry-run
bash samples/bash/15_backup.sh --source config --backup-dir backups --retention-days 14

python3 samples/python/15_backup.py --dry-run --verbose
```

### 運用上の注意点

- バックアップ成功とリストア成功は別である。定期的に復元試験する
- 秘密鍵や `.env` を同じtarに入れるなら権限と保管先を分ける
- リモートコピーは本章の次段（rclone等）として別要件にする

---

## 15.10 証明書期限確認

主言語: Python。

実装: `samples/python/15_cert_check.py`

### 要件

1. ホスト:ポートへTLS接続し、証明書の残日数を計算する
2. warn / crit 日数で分類する
3. ローカルPEM（`--cert-file`）でも検証できる
4. 1件でも crit なら終了コード3
5. dry-runでは接続せず対象一覧を出す

### 入力

- `--host host:port`（複数）
- `--cert-file`
- `--warn-days`、`--crit-days`、`--timeout`
- 設定 `cert_check`

### 出力

- CSV: `target,not_after,days_left,status,detail`
- 終了コード 0/1/2/3

### 処理フロー

```text
load targets
if dry-run: list targets; exit 0
for target:
  fetch cert (TLS or PEM)
  compute days_left
  classify
write report
```

### エラー処理

- 接続失敗 → ERROR行、全体2（全件ERRORなら2）
- 証明書解析失敗 → 2
- crit 到達 → 3

### ログ

ホスト、残日数、status を出す。秘密鍵は扱わない。

### 設定ファイル

```yaml
cert_check:
  targets:
    - host: web01.example.invalid
      port: 443
  warn_days: 30
  crit_days: 7
```

### dry-run

TLS接続しない。

### 再実行性

読み取りのみ。

### テスト

自己署名PEMを `--cert-file` で渡し、残日数計算を固定時計で検証する（第14章の `14_cert_report.py` も参照）。

### 実行例

```bash
python3 samples/python/15_cert_check.py --dry-run --verbose

# ラボのPEMがある場合
python3 samples/python/15_cert_check.py \
  --cert-file /tmp/opsctl-lab/example.pem \
  --warn-days 30 --crit-days 7 \
  --report reports/certs.csv
```

### 運用上の注意点

- SNIが必要なサイトでは server_hostname を正しく渡す
- 中間証明書不足はブラウザと結果が違うことがある
- 自動更新（ACME）環境では、本チェックは監視であり発行そのものではない

---

## 15.11 定期レポート生成

主言語: Python。

実装: `samples/python/15_report.py`

### 要件

1. ping / disk / cert などのCSV結果を集約する
2. セクションごとに件数と最悪ステータスを要約する
3. Markdownまたはテキストレポートを `reports/` へ書く
4. dry-runでは集約結果をstderrに出しファイルを書かない
5. メール送信は本文では「宛先設定のみ」とし、送信は別途承認付きにする

### 入力

- `--report-dir`（入力CSV置き場）
- `--section`（複数）
- `--output`
- 設定 `report.sections`

### 出力

- サマリーレポートファイル
- 終了コード: 集約成功0、入力欠落は方針により0（欠落をWARNING）または2

### 処理フロー

```text
discover latest CSVs per section
aggregate counts
render report
if dry-run: print; else write output
```

### エラー処理

- 未知セクション → 1
- CSV破損 → そのセクション ERROR、全体2

### ログ

読んだファイルパスと集計件数を残す。

### 設定ファイル

```yaml
report:
  sections:
    - ping
    - disk
    - cert
  recipients:
    - ops-team@example.invalid
```

### dry-run

ファイルを書かない。

### 再実行性

出力は時刻付きファイル名にすると安全。

### テスト

fixture CSVを `work/reports` に置き、要約行が期待どおりか検証する。

### 実行例

```bash
python3 samples/python/15_report.py --dry-run --verbose
python3 samples/python/15_report.py \
  --report-dir reports \
  --output reports/summary.md
```

### 運用上の注意点

- 定期実行は「各チェック成功後にレポート」の依存順を決める
- 受信者リストをコードに直書きしない
- 要約だけ送ると詳細調査ができない。CSV保管期間を別に決める

---

## 15.12 題材と言語適性の整理

| 題材 | 主言語 | 理由 |
|------|--------|------|
| 疎通確認 | Python | 並列、集計、テスト |
| ディスク監視 | Bash / PowerShell | OSコマンドが近い |
| ログ検索 | Python | 正規表現とストリーム |
| 古いファイル整理 | Python | パス検証と安全策 |
| ユーザー棚卸し | PowerShell（Win）/ Bash（Linux） | 管理APIが近い |
| サービス確認 | Bash / PowerShell | サービス管理が近い |
| 設定一括変更 | Python | 差分、テスト、原子的更新 |
| API→CSV | Python | HTTPライブラリとテスト |
| バックアップ | Bash / Python | tarと検証の役割分担 |
| 証明書期限 | Python | TLSと日付計算 |
| レポート | Python | 複数形式の集約 |

---

## 15.13 セキュリティ上の注意点（章共通）

- 秘密情報を設定ファイルとレポートに書かない
- 破壊的操作は allowlist、dry-run既定、監査CSVを揃える
- アラート用シェルコマンドに外部入力を連結しない
- レポートにパスワードやトークンが混入していないか定期点検する

---

## 15.14 テスト方法（章共通）

1. 各スクリプトの `--help` が落ちないこと
2. dry-runが副作用ゼロであること
3. 不正入力で終了コード1であること
4. ラボパス外への変更が拒否されること（cleanup / config-patch）
5. pytest / シェルテストで純粋関数と集計を固定すること（`tests/`）

例:

```bash
cd infra_scripting_coding_guide
python3 -m pytest tests/ -q
bash samples/bash/15_disk_check.sh --paths / --dry-run
python3 samples/python/15_cleanup_old.py --target-dir work/tmp
```

---

## 章末問題

1. 疎通確認で「重要ホスト」をCRITICALにする要件を、終了コード表に落として書け。
2. cleanup を既定 dry-run にする理由を、運用事故のシナリオで説明せよ。
3. ディスク監視の `--alert-command` が危険になりうる入力例を一つ書け。
4. API取得で 401 をリトライすべきでない理由を述べよ。
5. バックアップの「取得成功」と「リストア成功」を分ける監視項目を提案せよ。

## 解答と解説

1. 重要ホスト不通 → 3。それ以外の不通のみ → 2。全成功 → 0。
2. cronや引数ミスで本番ディレクトリを消す事故を、報告モードで止められる。
3. `'; rm -rf /` を連結される、または利用者入力をそのまま `sh -c` に渡す。
4. 認証失敗は再試行で治らない。ロックや監査ノイズを増やす。
5. 取得ジョブの終了コード、アーカイブサイズ下限、月次リストア試験の成功記録。

## 実装演習

### 演習A

`15_ping_check.py` に「連続失敗がN回でCRITICAL」を足す設計だけ書け（実装は任意）。状態ファイルの置き場と再実行性も述べる。

### 演習B

`work/logs` に日本語を含むログを置き、`15_log_search.py` で検索せよ。文字コード問題が起きたら方針を記録する。

### 演習C

`15_opsctl_dispatch.py` 経由で `disk-check` と `cert-check` の dry-run を連続実行し、終了コードの伝播を確認せよ。

---

## 次章予告

第16章では、これらのスクリプトを秘密情報なしでGit管理し、レビューとリリース、ロールバック可能な共同開発へつなぐ。
