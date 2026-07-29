# 第9章 ログと監視

障害対応で最もコストの高い行為は、根拠のない推測に基づいて手を動かすことである。

ログとメトリクスが揃い、複数ホストの時刻が一致していれば、仮説を立てて棄却する速度が上がり、真の原因へ最短距離で到達できる。

本章では、Linuxのjournald・`/var/log`・rsyslogと、Windowsのイベントログ・イベントビューアー・パフォーマンスカウンターを対比しながら、資源監視、ログローテーション、時刻同期、証跡保全までを扱う。

---

## 1. 学習目標

1. Linuxのjournald、`/var/log`、rsyslogの役割分担を説明できる
2. Windowsイベントログを、イベントビューアーとPowerShellの`Get-WinEvent`の両方で検索できる
3. CPU、メモリ、ディスク、ネットワークの基本的な監視項目を挙げ、両OSで確認できる
4. パフォーマンスカウンターの概念と代表的な確認方法を説明できる
5. ログローテーションの仕組みと設定の要点を実践できる
6. 時刻同期がログ突合に不可欠な理由を説明できる
7. インシデント発生時に証跡を保全する基本手順を実行できる

---

## 2. 基本概念

### 2.1 ログの種類

| 種類 | 例 |
|------|----|
| システムログ | 起動処理、サービスの起動・停止、認証イベント |
| アプリケーションログ | Webサーバー、業務アプリケーションの動作記録 |
| セキュリティ/監査ログ | ログオンの成否、権限変更、監査ポリシーに基づく記録 |
| メトリクス（性能データ） | CPU使用率、メモリ使用量、ディスクI/O、ネットワーク遅延 |

ログは「何が起きたか」を離散的なイベントとして記録するのに対し、メトリクスは「どういう状態が続いているか」を連続的な数値として記録するという性質の違いがある。

障害調査では、この両方を組み合わせることで、単発のログだけでは見えないトレンド（じわじわとしたメモリリークなど）を把握できる。

### 2.2 監視の目的

監視の目的は大きく3つに分けられる。

1. **異常検知**：閾値を超えた、あるいは想定外の状態になったことを即座に検知する。
2. **トレンド把握**：時系列での変化を追い、悪化の兆候を早期に発見する。
3. **キャパシティ予測**：将来的なリソース不足を事前に見積もり、増強計画を立てる。

アラート設計では、「人が実際に起こされてでも対応する価値があるか」という基準で閾値と通知先を決めることが重要であり、これを怠ると**アラート疲れ**（通知が多すぎて重要な通知が埋もれる状態）を招く。

### 2.3 時刻同期の重要性

複数ホストのログを時系列で並べて因果関係を調べるとき、各ホストの時刻がずれていると、実際には後に起きた事象が先に起きたように見えてしまい、調査の方向を誤らせる。

第2章で扱ったNTP（Network Time Protocol）による時刻同期は、単なる時計合わせではなく、監視・ログ基盤全体の前提条件である。

タイムゾーンの表記統一（UTCで記録し表示時にローカル変換する、またはログ全体を一つのタイムゾーンに統一するなど）も、複数拠点・複数OSが混在する環境では欠かせない運用ルールである。

### 2.4 証跡保全

障害対応やセキュリティインシデント対応では、再起動や不用意な後片付けを行う前に、揮発性の高い情報（実行中プロセス一覧、ネットワーク接続状況、メモリの内容など）を先に採取する。

これは、再起動によって攻撃者の痕跡やクラッシュ直前の状態を示す情報が失われてしまうためであり、**証跡保全（フォレンジック的な初動対応）**の基本原則である。

証跡保全の対象には、ログファイルのコピー、プロセス一覧、ネットワーク接続一覧、直近の設定変更履歴、必要に応じてディスクイメージやメモリダンプが含まれる。

---

## 3. Linuxでの実現方法

### 3.1 journald

**journald**は、systemdに組み込まれたログ収集デーモンであり、テキストではなくバイナリ形式で構造化されたログを保存する。

```bash
journalctl -b --no-pager | tail -n 30
journalctl -u sshd -n 100 --no-pager
journalctl --since '1 hour ago' -p err
journalctl -k -n 50
journalctl -f
```

- `-b`：今回の起動（boot）以降のログのみを表示する
- `-u <ユニット名>`：特定のsystemdユニットに関するログのみを表示する
- `--since`：指定した時刻以降のログを表示する（`'2026-07-30 09:00:00'` のような絶対指定も可能）
- `-p err`：指定した優先度（priority）以上のログのみを表示する（`err` はエラー以上）
- `-k`：カーネルメッセージ（`dmesg`相当）のみを表示する
- `-f`：`tail -f` のようにログをリアルタイムで追跡する

想定出力の一例を示す。

```text
Jul 30 03:12:01 web01 sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 51422 ssh2
Jul 30 03:12:04 web01 sshd[1234]: Failed password for invalid user admin from 203.0.113.5 port 51430 ssh2
```

同一IPからの連続した認証失敗は、パスワード推測攻撃（ブルートフォース攻撃）の兆候として注目すべきパターンである。

journaldの永続化は既定では無効な場合があり、`/etc/systemd/journald.conf` の `Storage=persistent` 設定や `/var/log/journal` ディレクトリの有無で確認できる。

```bash
cat /etc/systemd/journald.conf | grep -i storage
ls -ld /var/log/journal 2>/dev/null || echo "永続化ディレクトリ未作成（揮発性の可能性）"
```

永続化されていない場合、再起動によって過去のログが失われるため、障害調査やセキュリティ監査の要件によっては明示的に有効化する必要がある。

### 3.2 `/var/log` とrsyslog

伝統的なテキスト形式のログの置き場が `/var/log` ディレクトリである。

**rsyslog**（または後継のsyslog-ng）は、syslogプロトコルに基づくメッセージを受け取り、設定に従って適切なファイルへ振り分けて書き込むデーモンである。

```bash
ls -la /var/log
sudo tail -n 50 /var/log/messages 2>/dev/null || sudo tail -n 50 /var/log/syslog
sudo grep -i error /var/log/secure 2>/dev/null | tail -n 30
sudo grep -i 'failed password' /var/log/auth.log 2>/dev/null | tail -n 30
```

RHEL系では認証関連ログが `/var/log/secure` に、Ubuntu系では `/var/log/auth.log` に記録されるという配置の違いがある点に注意する。

多くの現行ディストリビューションでは、journaldが一次的にログを収集し、rsyslogがjournaldからログを受け取って伝統的なテキストファイルへ書き出す、または直接syslogメッセージを受けて書き出す構成が併存している。

`/etc/rsyslog.conf` と `/etc/rsyslog.d/*.conf` に、どのファシリティ（種別）・プライオリティのログをどのファイルへ振り分けるかのルールが定義されている。

```bash
cat /etc/rsyslog.conf | grep -v '^#' | grep -v '^$'
ls /etc/rsyslog.d/
```

リモートのログサーバーへ転送する設定も、この`rsyslog.conf`に記述する（例: `*.* @@logserver.lab.local:514`、`@@`はTCP転送を意味する）。

### 3.3 ログローテーション

ログファイルが際限なく肥大化すると、ディスク容量を圧迫し、最悪の場合はディスクフルによってシステム全体が不安定になる。

**logrotate**は、ファイルサイズや日付を基準にログファイルを切り替え（ローテーション）、圧縮、そして一定世代数を超えたものを削除するツールである。

```bash
cat /etc/logrotate.conf
ls /etc/logrotate.d
cat /etc/logrotate.d/nginx 2>/dev/null
sudo logrotate --debug /etc/logrotate.conf
sudo logrotate --force /etc/logrotate.d/nginx
```

`--debug` は実際にローテーションを行わずに、何が行われるかをシミュレーションするオプションであり、設定確認に有用である。

`--force` は本来の条件を満たしていなくても強制的にローテーションを実行するオプションで、動作確認や緊急のログ肥大化対応に使う。

journald側は、ファイルベースのlogrotateとは別に、`/etc/systemd/journald.conf` の `SystemMaxUse=` や `SystemKeepFree=` といった設定で、独自にディスク使用量の上限を管理する。

```bash
grep -E 'SystemMaxUse|SystemKeepFree|MaxRetentionSec' /etc/systemd/journald.conf
journalctl --disk-usage
```

### 3.4 資源監視の入口

```bash
uptime
free -h
df -h
df -i
ss -s
vmstat 1 5
sar -u 1 5 2>/dev/null || echo "sysstatパッケージ未導入の可能性"
iostat -xz 1 3 2>/dev/null
```

- `uptime`：稼働時間とロードアベレージ（負荷平均）を表示する
- `free -h`：メモリとスワップの使用状況を人間が読みやすい単位で表示する
- `df -h` / `df -i`：ディスク使用量とinode使用量をそれぞれ表示する
- `vmstat 1 5`：1秒間隔で5回、CPU・メモリ・スワップ・I/Oの概況を表示する
- `sar -u`：CPU使用率の推移を表示する（sysstatパッケージが必要）
- `iostat -xz`：ディスクI/Oの詳細な統計を表示する

ロードアベレージがCPUコア数を大きく超えて高い状態が続く場合は、CPU待ちのプロセスが滞留していることを示し、単なるCPU使用率だけでは見えない負荷状況を把握する手がかりになる。

継続的な監視には、これらのコマンドを都度実行するのではなく、Prometheus + node_exporter、Zabbix、Datadogなどの監視基盤へメトリクスを集約する構成が実務では一般的である。

---

## 4. Windowsでの実現方法

### 4.1 イベントログとイベントビューアー

Windowsのイベントログは、主に **Application**、**System**、**Security**、**Setup** という標準チャネルに分かれ、加えてアプリケーションやサービスごとの専用ログ（Applications and Services Logs）が存在する。

**イベントビューアー**（`eventvwr.msc`）は、これらのログをGUIで参照・フィルタするための標準ツールである。

```powershell
Get-WinEvent -ListLog * | Where-Object RecordCount -gt 0 |
  Sort-Object RecordCount -Descending |
  Select-Object -First 15 LogName, RecordCount
```

このコマンドは、レコード数の多いログチャネルを優先的に表示し、どのチャネルが活発に記録されているかを俯瞰する助けになる。

### 4.2 PowerShellによるイベントログ検索

```powershell
Get-WinEvent -LogName System -MaxEvents 30 |
  Where-Object { $_.LevelDisplayName -in 'Error','Critical' } |
  Format-Table TimeCreated, Id, ProviderName -AutoSize

Get-WinEvent -FilterHashtable @{
  LogName   = 'System'
  StartTime = (Get-Date).AddHours(-2)
  Level     = 2
} | Select-Object -First 20

Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20 -ErrorAction SilentlyContinue
```

`Get-WinEvent` は、旧来の `Get-EventLog` の後継となるコマンドレットであり、`-FilterHashtable` を使うと、ログの取得元（イベントログサービス）側でフィルタが行われるため、大量ログの検索でも高速に動作する。

`Level` の値は、1（Critical）、2（Error）、3（Warning）、4（Information）に対応する。

代表的なセキュリティイベントIDには、次のようなものがある。

| イベントID | 意味 |
|------------|------|
| 4624 | ログオン成功 |
| 4625 | ログオン失敗 |
| 4634 | ログオフ |
| 4720 | ユーザーアカウントの作成 |
| 4732 | セキュリティグループへのメンバー追加 |

これらのイベントは、対象サーバーの監査ポリシー（`auditpol` やGPOで設定）が有効になっていない場合は記録されない点に注意する。

```powershell
auditpol /get /category:*
```

想定出力の一例（4625の抜粋）は次のようになる。

```text
TimeCreated          Id   LevelDisplayName Message
-----------          --   ---------------- -------
2026/07/30 3:14:22   4625 Information      アカウントがログオンに失敗しました。...
```

同一の送信元IPアドレスから短時間に大量の4625が記録される場合、ブルートフォース攻撃の兆候として扱う。

### 4.3 パフォーマンスカウンター

**パフォーマンスカウンター**は、Windowsが提供する、CPU・メモリ・ディスク・ネットワークなどのリソース使用状況を数値として取得する仕組みである。

```powershell
Get-Counter '\Processor(_Total)\% Processor Time'
Get-Counter '\Memory\Available MBytes'
Get-Counter '\LogicalDisk(_Total)\% Free Space'
Get-Counter '\Network Interface(*)\Bytes Total/sec'
Get-Counter -Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5
```

`-SampleInterval` と `-MaxSamples` を指定すると、指定間隔で複数回サンプリングでき、Linuxの `vmstat 1 5` に近い使い方ができる。

GUIツールとしては、**パフォーマンスモニター（perfmon）**でカウンターをグラフ表示したり、**リソースモニター（Resource Monitor）**でリアルタイムのプロセス別リソース使用状況を確認したりできる。

```powershell
perfmon
resmon
```

継続的な性能データの収集には、**データコレクターセット**をパフォーマンスモニターで構成し、定期的にログを記録する運用が一般的である。

### 4.4 ログのサイズと保持

イベントログはログごとにサイズ上限を持ち、上限に達すると古いイベントから上書きされる（設定によっては新規記録を停止する）動作になる。

```powershell
Get-WinEvent -ListLog System | Format-List LogName, MaximumSizeInBytes, RecordCount, LogMode

wevtutil sl System /ms:104857600
wevtutil gl Security
```

`wevtutil sl <ログ名> /ms:<バイト数>` でログの最大サイズを変更できる。

`LogMode` が `Circular`（既定）の場合は上限到達で上書きされ、`Retain` や `AutoBackup` を設定すると、上書き前に古いログを別ファイルへ退避する動作にできる。

上書きによってセキュリティ調査に必要な過去ログが消失する事故を防ぐため、重要な環境では中央ログ収集基盤（Windows Event Forwarding、SIEM製品など）へ転送する構成を検討する。

---

## 5. 両OSの比較

| 目的 | Linux | Windows |
|------|-------|---------|
| 直近エラーの検索 | `journalctl -p err` | `Get-WinEvent` で`Level`が Error 以下 |
| サービス単位のログ | `journalctl -u <ユニット名>` | Application/Systemログ + プロバイダー名で絞込 |
| 認証失敗の確認 | `/var/log/secure` または `auth.log` | セキュリティログのイベントID 4625 |
| リアルタイム追跡 | `journalctl -f` | `Get-WinEvent`のポーリング、またはイベントビューアーのライブ表示 |
| 資源監視（瞬間値） | `vmstat` / `free` / `df` | `Get-Counter` / タスクマネージャー |
| 資源監視（GUI） | 監視基盤のダッシュボード | パフォーマンスモニター、リソースモニター |
| ログローテーション | logrotate / journaldの上限設定 | イベントログのサイズ設定、中央収集 |
| ログの構造 | テキスト（syslog形式）＋journaldのバイナリ構造化ログ | XML構造化イベント |
| 中央集約の代表例 | rsyslog転送、Fluentd、Prometheus | Windows Event Forwarding、SIEM連携 |

構造という観点では、journaldとWindowsイベントログはどちらも「構造化されたフィールドを持つイベント」を扱う点で似ており、テキストのgrepに頼らずフィールド単位で検索できるという共通の利点がある。

---

## 6. コマンド例

### 6.1 直近のエラー・失敗ログを検索する

**目的**: 直近に発生したエラーレベルのログを横断的に検索する。

```bash
sudo journalctl --since today | grep -i fail | tail -n 30
```

```powershell
Get-WinEvent -LogName Application -MaxEvents 200 |
  Where-Object { $_.Message -match 'fail|error' } |
  Select-Object -First 20 TimeCreated, Id, Message
```

**権限**: セキュリティログや一部のシステムログの参照には、管理者相当の権限が必要になることが多い。

**リスク**: 参照自体のリスクは低いが、ログに機密情報（認証情報の一部、個人情報）が含まれる場合があるため、共有や保存時の取り扱いに注意する。

### 6.2 CPUとメモリの瞬間値を取得する

**目的**: 現在のCPU・メモリ使用状況を一度だけ確認する。

```bash
top -b -n 1 | head -n 20
```

```powershell
Get-Counter '\Processor(_Total)\% Processor Time','\Memory\Available MBytes'
```

**権限**: 一般ユーザーで実行可能。

**リスク**: 低。

### 6.3 特定サービスのログのみを継続監視する

**目的**: 障害調査中に、特定サービスのログをリアルタイムで追跡する。

```bash
sudo journalctl -u sshd -f
```

```powershell
Register-ObjectEvent -InputObject (
  New-Object System.Diagnostics.Eventing.Reader.EventLogWatcher(
    [System.Diagnostics.Eventing.Reader.EventLogQuery]::new('Security', [System.Diagnostics.Eventing.Reader.PathType]::LogName)
  )
) -EventName EventRecordWritten -Action { Write-Host $Event.SourceEventArgs.EventRecord.FormatDescription() }
```

Windowsでのリアルタイム監視は、簡易的には数秒間隔で `Get-WinEvent` をポーリングする方法でも代替できる。

```powershell
while ($true) {
  Get-WinEvent -LogName Security -MaxEvents 5 | Select-Object TimeCreated, Id, Message
  Start-Sleep -Seconds 10
}
```

**権限**: セキュリティログの継続監視には管理者権限が必要になる。

**リスク**: 低〜中。ポーリング間隔が短すぎるとシステム負荷やログサービスへの負荷が増える。

### 6.4 ログローテーションを手動で実行する

**目的**: 設定を変更した際に、想定どおりローテーションが動くか確認する。

```bash
sudo logrotate --debug /etc/logrotate.d/nginx
# 問題なければ
sudo logrotate --force /etc/logrotate.d/nginx
```

> **警告**: `--force` は条件を満たしていなくても強制実行するため、想定より早いタイミングで既存ログが切り替わる（アプリケーションがファイルディスクリプタを保持したままになる場合、再読み込みシグナルの送信が必要になることがある）。

**権限**: root（sudo）。

**リスク**: 中。強制ローテーション後にアプリケーションがログファイルへ書き込めなくなる場合があるため、対象アプリケーションのログハンドリング方式（コピー&トランケート方式か、シグナルによる再オープン方式か）を事前に確認する。

---

## 7. 実務上の注意点

1. アプリケーションログとOSログの両方を確認する。アプリケーションだけが「正常」に見えても、OSレベルでリソース枯渇が起きていることがある。
2. ログをローカルディスクにしか保存しない構成は、そのディスク障害でログごと失われるリスクがある。
3. アラート疲れを避けるため、閾値設定と抑制（同一アラートの再通知間隔、重複排除）を設計段階から組み込む。
4. 障害調査手順書に、「採取すべきコマンド一覧」をあらかじめ明記しておくと、初動対応の速度と質が安定する。
5. ログの保持期間は、コンプライアンス要件やインシデント調査に必要な期間を踏まえて設定し、短すぎる保持期間による証跡消失を避ける。
6. 複数ホストのログを横断検索する運用を想定するなら、早い段階で中央ログ収集基盤の導入を検討する。

---

## 8. セキュリティ上の注意点

1. ログへの不正な改ざんや削除を検知できるよう、ログ自体の変更を監査する仕組み（改ざん検知、ログの外部転送）を持つ。
2. 管理者以外がセキュリティログを削除・無効化できる状態にしない。
3. 個人情報や認証情報がログに平文で出力されていないか点検し、必要に応じてマスキング方針を定める。
4. インシデント対応時は、証跡保全のための情報採取と、復旧のための作業ログを明確に分離して記録する。
5. ログ収集エージェントや転送経路自体もセキュリティ対象であり、転送経路の暗号化（TLS）や認証を適用する。
6. 監査ポリシー（Windowsの`auditpol`、Linuxの`auditd`）が意図した項目を確実に記録しているか、定期的に検証する。

---

## 9. よくある障害

| 症状 | 典型的な原因 |
|------|--------------|
| 期待したログが記録されていない | チャネル/監査ポリシーの無効化、権限不足、ディスク満杯、ログレベル設定 |
| 複数ホストのログの時系列が噛み合わない | NTP未同期、タイムゾーン設定の不一致、UTC表示とローカル表示の混在 |
| 古いログが上書きで消えている | イベントログ/journalのサイズ上限不足、収集エージェントの転送遅延 |
| アラートは来るが原因調査に使える情報が乏しい | メッセージ内容、イベントID、相関ID（トランザクションID）などの設計不足 |
| ログローテーション後にアプリがログを書けなくなる | シグナルによる再オープン処理の欠如、ファイルディスクリプタの保持 |
| ディスク使用量アラートの直後にログ自体が止まる | ログ書き込み先ディスクの満杯によるログサービス自体の書き込み失敗 |

---

## 10. 切り分け手順

1. **対象時間帯を確定する**: 障害発生の推定時刻を、関係者の申告と最初の異常ログ・メトリクスの両方から確定する。
2. **時刻同期状態を確認する**: 調査対象ホスト全ての時刻同期状態（`timedatectl`/`w32tm /query /status`）を確認し、ずれがあれば補正して読み替える。
3. **OSレベルのログを確認する**: journald/`/var/log`、またはSystem/Applicationイベントログで、対象時間帯のエラー・警告を洗い出す。
4. **アプリケーションログを確認する**: OSレベルで異常がなければ、アプリケーション固有のログを確認する。
5. **リソースメトリクスを確認する**: CPU、メモリ、ディスク、ネットワークの推移を確認し、リソース枯渇が引き金になっていないか調べる。
6. **セキュリティログを確認する**: 意図しないアクセスや設定変更が引き金になっていないか、認証ログ・監査ログを確認する。
7. **証跡を保全してから復旧に着手する**: 再起動やサービス再起動を行う前に、必要な情報を採取し終えているか最終確認する。

証跡保全の最低限のセットとして、次の情報を優先して採取する。

1. 調査時点の時刻とホスト名
2. 実行中プロセス一覧、待ち受けポート一覧
3. 直近のログのエクスポート（journald、イベントログ）
4. 直近の変更履歴（パッケージ更新、設定変更、デプロイ記録）

```bash
# Linuxでの証跡採取例
date -u
hostname
ps auxf > /tmp/evidence_ps_$(date +%Y%m%d%H%M%S).txt
ss -tulpn > /tmp/evidence_ss_$(date +%Y%m%d%H%M%S).txt
journalctl --since '2 hours ago' > /tmp/evidence_journal_$(date +%Y%m%d%H%M%S).txt
```

```powershell
# Windowsでの証跡採取例
Get-Date -AsUTC
$env:COMPUTERNAME
Get-Process | Export-Csv C:\evidence\ps_$(Get-Date -Format yyyyMMddHHmmss).csv -NoTypeInformation
Get-NetTCPConnection | Export-Csv C:\evidence\netconn_$(Get-Date -Format yyyyMMddHHmmss).csv -NoTypeInformation
Get-WinEvent -LogName System -MaxEvents 500 | Export-Csv C:\evidence\sysevt_$(Get-Date -Format yyyyMMddHHmmss).csv -NoTypeInformation
```

---

## 11. 章末問題

1. journaldと `/var/log` 配下のテキストログの関係を説明せよ。
2. 複数ホストのログを突合する前に必ず確認すべきホスト設定は何か。
3. セキュリティイベントID 4625の一般的な意味は何か。
4. ディスク満杯がログの欠落を引き起こす経路を説明せよ。
5. 証跡保全において、システムの再起動より先に採取すべき情報の例を2つ挙げよ。
6. アラート疲れとは何か、またその対策として考えられることを1つ挙げよ。
7. パフォーマンスカウンターとイベントログの、記録する情報の性質の違いを説明せよ。

---

## 12. 解答と解説

1. journaldがまずログを収集・保持し、多くの環境ではrsyslogがjournaldからログを受け取って伝統的なテキストファイルへも書き出す構成が併存している。障害調査では両方を確認するのが安全である。
2. 各ホストのタイムゾーン設定とNTPによる時刻同期状態。
3. アカウントのログオンに失敗したことを示すイベント。
4. ディスクが満杯になると新規ログの書き込みが失敗し、ローテーションやjournaldの新規記録が止まり、以降のイベントが記録されなくなる。
5. 実行中プロセス一覧、ネットワーク接続状況（他に、メモリダンプ方針に沿った情報や直近ログのエクスポートも該当する）。
6. 通知が多すぎて重要な通知が他の通知に埋もれ、対応が遅れたり見落とされたりする状態。対策としては、閾値の見直しや、同一アラートの重複抑制、重要度によるエスカレーション経路の分離が挙げられる。
7. パフォーマンスカウンターは連続的な数値（状態の推移）を記録するのに対し、イベントログは離散的な出来事（何が起きたか）を記録する。

---

## 13. ハンズオン演習

### 演習9-1 エラー・失敗ログの横断抽出

**前提**: `web01`（Linux）と `winapp01`（Windows）が稼働しており、通常運用中であること。

**実行**:

1. `web01` で `sudo journalctl --since '2 hours ago' -p err > /tmp/error_linux.txt` を実行する。
2. `winapp01` で `Get-WinEvent -LogName System,Application -MaxEvents 500 | Where-Object LevelDisplayName -in 'Error','Critical' | Export-Csv C:\temp\error_windows.csv -NoTypeInformation` を実行する。

**確認**: 両方のファイルを開き、記録件数と主要なエラー内容を比較する。

**元に戻す**: 演習で作成した一時ファイル（`/tmp/error_linux.txt`、`C:\temp\error_windows.csv`）を削除する。

### 演習9-2 監視ベースラインの記録

**前提**: 対象ホストがアイドル状態（通常運用の負荷のみ）であること。

**実行**:

1. Linuxで `uptime`、`free -h`、`df -h`、`ss -s` の結果を1つのテキストファイルに記録する。
2. Windowsで `Get-Counter '\Processor(_Total)\% Processor Time','\Memory\Available MBytes'` と `Get-NetTCPConnection -State Listen | Measure-Object` の結果を記録する。

**確認**: 記録した数値が、それぞれのホストの通常時の目安として妥当な範囲かをチームで確認し、平常値メモとして残す。

**元に戻す**: 本演習は参照系のみのため、元に戻す操作は不要である。記録したメモは今後の障害対応のために保管する。

### 演習9-3 時刻ずれが与える影響の体験（ラボ限定）

**前提**: 本演習は本番環境では絶対に行わない。ラボ専用のホストであり、スナップショットを取得済みであること。

**実行**:

1. 対象ホストの時刻同期を一時的に無効化する（Linux: `sudo timedatectl set-ntp false`、Windows: `Stop-Service w32time`）。
2. 手動で時刻を数分ずらす（Linux: `sudo timedatectl set-time '2026-07-30 09:00:00'`、Windows: `Set-Date`）。
3. その状態で複数ホストのログを採取し、時系列を突き合わせてみる。

**確認**: 時刻がずれた状態でログを並べると、因果関係が実際とは逆に見えたり、時間差が不自然になったりすることを確認する。

**元に戻す**: 直ちに時刻同期を再度有効化する（Linux: `sudo timedatectl set-ntp true`、Windows: `Start-Service w32time; w32tm /resync`）。同期完了後、`timedatectl status` / `w32tm /query /status` で正常な同期状態に戻ったことを必ず確認する。

---

## 14. 本章のまとめ

観測できないものは運用できないという原則のとおり、ログとメトリクスの整備、時刻同期、証跡保全の徹底は、障害対応の速度と質を根本から左右する。

LinuxのjournaldとWindowsのイベントログは仕組みこそ異なるが、どちらも構造化されたイベントとして検索・フィルタできる点は共通しており、両OSの検索コマンドを併せて押さえておくことが、混在環境での実務対応力につながる。

次章では、ディレクトリサービスであるActive DirectoryとLinuxとの連携について扱う。

次章: [第10章 Active DirectoryとLinux連携](10_active_directory_and_linux.md)
