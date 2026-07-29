# 付録A 同一管理目的のコマンド対照表

同一の管理目的について、Linuxのシェルコマンドと、Windowsの主にPowerShellコマンドレットを対照させる。

各項目について、目的、基本構文、主要オプション、実行例、想定される出力とその読み方、実行に必要な権限、誤操作時のリスクを示す。

より詳細な文脈は、本編の該当章を参照する。

---

## A.1 ユーザー一覧を確認する

**目的**：ローカルまたはドメインの有効なアカウント一覧を確認する。

**構文**：`getent passwd`、`Get-LocalUser`、`Get-ADUser -Filter *`

```bash
getent passwd | cut -d: -f1,3,7 | head -n 10
```

```powershell
Get-LocalUser | Select-Object Name, Enabled, SID
Get-ADUser -Filter * | Select-Object -First 10 SamAccountName
```

**主要オプション**：Linuxは `cut` で必要な列（ユーザー名、UID、シェル）だけを抜き出す。
Windowsは `-Filter`、`Select-Object` で対象と表示列を絞り込む。

**想定出力（Linux）**：

```text
root:0:/bin/bash
operator:1001:/bin/bash
```

**読み方**：コロン区切りで「ユーザー名：UID：ログインシェル」を示す。
シェルが `/sbin/nologin` や `/bin/false` になっているアカウントは、対話ログイン用ではなくサービス用アカウントであることが多い。

**権限**：一般ユーザーで実行可能である。ADの参照権限はドメインの既定設定に依存する。

**リスク**：低（参照のみ）。

---

## A.2 プロセスを確認する

**目的**：CPUやメモリ使用量の上位プロセス、または特定の残存プロセスを特定する。

**構文**：`ps [オプション]`、`Get-Process`

```bash
ps -eo pid,ppid,user,stat,%cpu,%mem,cmd --sort=-%cpu | head -n 10
```

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Id, ProcessName, CPU, WorkingSet
```

**主要オプション**：`-e`（全プロセス）、`-o`（出力列の指定）、`--sort`（並び替え）。
Windowsは `Sort-Object` と `Select-Object` を組み合わせて同等の並び替え・列選択を行う。

**想定出力（Linux）**：

```text
PID PPID USER  STAT %CPU %MEM CMD
812    1 root  Ssl  12.3  1.1 /usr/sbin/nginx
```

**読み方**：`STAT`列の`S`は割り込み可能な待機、`R`は実行中、`Z`はゾンビ状態を示す。
PIDを控え、名前だけで対象プロセスを判断しない。同名プロセスが複数存在することは珍しくない。

**権限**：他ユーザーの詳細情報の参照には制限がある場合がある。

**リスク**：参照自体は低リスクだが、続けて`kill`や`Stop-Process`で終了させる操作は中〜高リスクになる。

---

## A.3 サービスを起動する

**目的**：停止しているサービスを起動する。

**構文**：`systemctl start サービス名`、`Start-Service サービス名`

```bash
sudo systemctl start nginx
systemctl is-active nginx
```

```powershell
Start-Service W3SVC
Get-Service W3SVC
```

**主要オプション**：`status`（状態確認）、`enable`（自動起動の有効化）。
Windowsは`-Force`、`Set-Service -StartupType`で起動種別を制御する。

**想定出力**：

```text
active
```

**読み方**：`systemctl is-active`は`active`、`inactive`、`failed`のいずれかを1語で返し、スクリプトからの判定に使いやすい。

**権限**：Linuxはroot相当（`sudo`）、Windowsは管理者権限が必要である。

**リスク**：設定誤りのあるサービスを起動すると、依存関係にある他のサービスにも影響が及ぶことがある。
SSHサービス自体を誤って停止しないよう、遠隔操作中は特に注意する。

---

## A.4 IPアドレスを確認する

**目的**：ネットワークインターフェースに割り当てられたIPアドレスと、既定のルートを確認する。

**構文**：`ip addr`、`Get-NetIPAddress`、`ipconfig`

```bash
ip -br addr
ip route
```

```powershell
Get-NetIPAddress -AddressFamily IPv4
Get-NetIPConfiguration
ipconfig /all
```

**主要オプション**：`-br`（簡潔表示）。Windowsは`-AddressFamily`でIPv4/IPv6を絞り込む。

**想定出力（Linux）**：

```text
eth0             UP             192.168.56.30/24
```

**読み方**：インターフェース名、状態（`UP`/`DOWN`）、アドレスとプレフィックス長を確認する。
`DOWN`のままであれば、上位のIP設定が正しくてもリンク自体が確立していない。

**権限**：一般ユーザーで実行可能である。

**リスク**：低（参照のみ）。

---

## A.5 待ち受けポートを確認する

**目的**：どのプロセスがどのポートで接続を待ち受けているかを確認する。

**構文**：`ss -tulpn`、`Get-NetTCPConnection -State Listen`

```bash
ss -tulpn
```

```powershell
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess |
  Sort-Object LocalPort
```

**主要オプション**：`-t`（TCP）、`-u`（UDP）、`-l`（待受のみ）、`-p`（プロセス情報）、`-n`（名前解決なし）。

**想定出力（Linux）**：

```text
tcp   LISTEN 0      128    0.0.0.0:22      0.0.0.0:*   users:(("sshd",pid=812))
```

**読み方**：`LocalAddress`が`0.0.0.0`であれば全インターフェースからの接続を受け付けている状態を示す。
`OwningProcess`（Windows）や`pid`（Linux）から、実際にそのポートを保持しているプロセスを特定できる。

**権限**：プロセス名の表示には管理者権限（Linuxはroot、Windowsは管理者）が必要な場合がある。

**リスク**：低（参照のみ）。

---

## A.6 ログを検索する

**目的**：直近の時間帯のエラーや失敗イベントを検索する。

**構文**：`journalctl [オプション]`、`Get-WinEvent -FilterHashtable @{...}`

```bash
journalctl --since '2 hours ago' -p err --no-pager
sudo grep -i fail /var/log/secure | tail -n 20
```

```powershell
Get-WinEvent -FilterHashtable @{
  LogName   = 'System'
  StartTime = (Get-Date).AddHours(-2)
  Level     = 2
} | Select-Object -First 30 TimeCreated, Id, ProviderName
```

**主要オプション**：`--since`（開始時刻）、`-p`（優先度、`err`はエラー以上）。
Windowsの`Level`は1（重大）〜5（詳細）の数値でフィルタする。

**想定出力**：

```text
Jul 29 09:12:03 web01 sshd[2044]: Failed password for operator from 192.168.56.40
```

**読み方**：時刻、ホスト名、プロセス名とPID、メッセージ本文の順に読み進める。
繰り返し出現するメッセージは、単発の事象か継続的な問題かを判断する材料になる。

**権限**：セキュリティ関連ログの参照には管理者相当の権限が必要な場合が多い。

**リスク**：低（参照のみ）。ログ内に含まれる機密情報の取り扱いには注意する。

---

## A.7 ディスク使用量を確認する

**目的**：ボリュームの空き容量、およびディレクトリごとの使用量を確認する。

**構文**：`df -h`、`du -sh パス`、`Get-Volume`

```bash
df -hT
df -i
du -xhd1 /var/log | sort -h
```

```powershell
Get-Volume | Select-Object DriveLetter, FileSystem, Size, SizeRemaining
```

**主要オプション**：`-h`（人が読みやすい単位）、`-T`（ファイルシステム種別も表示）、`-i`（inode表示）、`-x`（別ファイルシステムを跨がない）、`-d1`（深さ1階層まで）。

**想定出力（Linux）**：

```text
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/sda1      xfs    40G   32G  8.0G  81% /
```

**読み方**：`Use%`が高くても、`df -i`のinode使用率が別途100%近い場合があるため、両方を確認する。

**権限**：他ユーザー領域の詳細な参照には制限がある場合がある。

**リスク**：低（参照のみ）。

---

## A.8 ファイルの権限を変更する

**目的**：ファイルやディレクトリへのアクセス許可を変更する。

**構文**：`chmod モード パス`、`chown 所有者:グループ パス`、`icacls パス /grant アカウント:権限`

```bash
chmod 640 /opt/app/config.yml
chown appuser:appadmins /opt/app/config.yml
setfacl -m u:operator:r /opt/app/config.yml
```

```powershell
icacls C:\app\config.yml /grant operator:R
icacls C:\app\config.yml /save C:\temp\acl-config.txt
```

**主要オプション**：Linuxは数値モード（例：`640`）またはシンボリックモード。`setfacl`はACL（Access Control List）による個別付与に使う。
Windowsは`/grant`（付与）、`/remove`（削除）、`/save`（現状の保存）。

**想定出力**：

```text
config.yml: 処理に成功しました
```

**読み方**：`icacls`の実行結果は対象ごとの成否が1行ずつ表示され、`失敗しました`が含まれる場合はパスや権限指定の誤りを疑う。

**権限**：所有者または管理者権限が必要である。

**リスク**：高。過剰な権限付与や、サービスが読み取れなくなる権限剥奪につながりやすい。

**戻し方**：変更前に取得した`getfacl`（Linux）や`icacls /save`（Windows）の出力から復元する。

**警告**：`chmod -R 777` や `icacls ... /grant Everyone:F` は、緊急時の一時対応であっても原則として使わない。

---

## A.9 ホスト名を確認・変更する

**目的**：ホスト名を確認し、必要であれば変更する。

**構文**：`hostnamectl`、`Rename-Computer`

```bash
hostnamectl
sudo hostnamectl set-hostname web01
```

```powershell
hostname
Rename-Computer -NewName 'winapp01' -Restart
```

**主要オプション**：`set-hostname`（変更）。Windowsの`-Restart`は変更後に即座に再起動する。

**想定出力（Linux）**：

```text
 Static hostname: web01
       Icon name: computer-vm
         Chassis: vm
```

**読み方**：`Static hostname`が恒久的に設定されているホスト名であり、DHCPなどで一時的に付与される名前とは区別される。

**権限**：変更にはroot権限（Linux）または管理者権限（Windows）が必要である。

**リスク**：中。DNS登録、証明書のCN（Common Name）、監視設定など、ホスト名に依存する複数の設定と不整合が生じる。
ドメイン参加後の改名は、通常のホスト名変更とは別の手順を要する。

---

## A.10 時刻同期を確認する

**目的**：システム時刻が正しく同期されているかを確認する。

**構文**：`timedatectl`、`w32tm /query /status`

```bash
timedatectl
chronyc tracking
```

```powershell
Get-Date
w32tm /query /status
```

**主要オプション**：`chronyc tracking`は同期先との誤差（オフセット）を表示する。

**想定出力（Linux）**：

```text
System clock synchronized: yes
              NTP service: active
```

**読み方**：`synchronized: yes`であっても、`chronyc tracking`のオフセット値が大きい場合は、同期はしているが精度が低い状態を示す。

**権限**：参照は一般ユーザーで可能、設定変更にはroot権限または管理者権限が必要である。

**リスク**：低（参照のみ）。AD環境では、既定の許容差（5分）を超えるずれがKerberos認証の失敗に直結する（第10章参照）。

---

## A.11 ファイアウォールの状態を確認する

**目的**：ホストファイアウォールの有効状態と、許可されている通信を確認する。

**構文**：`firewall-cmd --list-all`、`Get-NetFirewallRule`

```bash
sudo firewall-cmd --list-all
# または
sudo ufw status verbose
```

```powershell
Get-NetFirewallProfile
Get-NetFirewallRule -Enabled True -Direction Inbound |
  Select-Object -First 20 DisplayName, Action, Profile
```

**主要オプション**：`--list-all`（ゾーンの全設定表示）。Windowsは`-Direction`（方向）、`-Enabled`（有効なもののみ）で絞り込む。

**想定出力（Linux）**：

```text
public (active)
  services: dhcpv6-client ssh
  ports: 80/tcp 443/tcp
```

**読み方**：`services`は事前定義されたサービス名での許可、`ports`は個別ポート番号での許可を示す。

**権限**：確認は一般ユーザーでも可能な場合が多いが、変更にはroot権限または管理者権限が必要である。

**リスク**：高。全拒否への変更は、リモート作業中であれば自分自身を締め出す事故につながる。

**警告**：ルール変更後は、必ず別セッションで接続確認をしてから作業セッションを閉じる。

---

## A.12 経路（ルーティング）を確認する

**目的**：宛先ネットワークへどのゲートウェイ・インターフェース経由で到達するかを確認する。

**構文**：`ip route`、`Get-NetRoute`

```bash
ip route
ip route get 8.8.8.8
```

```powershell
Get-NetRoute -DestinationPrefix '0.0.0.0/0'
Get-NetRoute | Sort-Object RouteMetric
```

**主要オプション**：`ip route get`は、指定した宛先に対して実際に使われる経路をその場で解決する。

**想定出力（Linux）**：

```text
default via 192.168.56.1 dev eth0 proto static metric 100
192.168.56.0/24 dev eth0 proto kernel scope link src 192.168.56.30
```

**読み方**：`default via`の行がデフォルトゲートウェイであり、この行が存在しない、または誤ったアドレスを指している場合、同一セグメント外への通信がすべて失敗する。

**権限**：参照は一般ユーザーで可能である。

**リスク**：経路変更は中〜高リスクであり、誤った設定でリモート接続経路自体を失うことがある。

---

## A.13 DNS解決を試験する

**目的**：名前解決が正しいIPアドレスへ到達するかを確認する。

**構文**：`dig 名前 @DNSサーバー`、`Resolve-DnsName 名前 -Server DNSサーバー`

```bash
getent hosts dc01.lab.local
dig dc01.lab.local @192.168.56.10
```

```powershell
Resolve-DnsName dc01.lab.local
Resolve-DnsName dc01.lab.local -Server 192.168.56.10
```

**主要オプション**：`@サーバー`（問い合わせ先を明示的に指定）。Windowsの`-Server`も同様の役割を持つ。

**想定出力**：

```text
;; ANSWER SECTION:
dc01.lab.local.  3600 IN A  192.168.56.10
```

**読み方**：`ANSWER SECTION`に期待するアドレスが含まれていれば正常応答である。
応答がタイムアウトする場合はDNSサーバーへの到達性、誤ったアドレスが返る場合はゾーンデータやキャッシュの問題を疑う。

**権限**：一般ユーザーで実行可能である。

**リスク**：低（参照のみ）。

---

## A.14 疎通を確認する

**目的**：対象ホストまでの到達性と、特定ポートでのアプリケーション応答を確認する。

**構文**：`ping 宛先`、`curl 宛先`、`Test-NetConnection 宛先 -Port ポート番号`

```bash
ping -c 2 192.168.56.20
curl -I http://web01/
nc -zv web01 443
```

```powershell
Test-NetConnection winapp01 -Port 443
Test-NetConnection 192.168.56.10 -Port 389
```

**主要オプション**：`-c`（送信回数）、`-I`（HTTPヘッダーのみ取得）、`-z`（接続確認のみ、データ送信なし）。
Windowsの`-Port`はTCPポートへの接続試行を追加で行う。

**想定出力**：

```text
ComputerName     : winapp01
RemotePort       : 443
PingSucceeded    : True
TcpTestSucceeded : True
```

**読み方**：`PingSucceeded`（ICMP到達性）と`TcpTestSucceeded`（対象ポートでの接続成立）を分けて確認することで、ネットワーク層の問題かアプリケーション層の問題かを切り分けられる。

**権限**：一般ユーザーで実行可能である。ICMPが環境によって遮断されている点に注意する。

**リスク**：低（参照のみ）。

---

## A.15 パッケージ・役割の一覧を確認する

**目的**：導入済みのパッケージやWindowsの役割・機能を確認する。

**構文**：`dnf list installed`、`dpkg -l`、`Get-WindowsFeature`

```bash
rpm -qa | wc -l
dnf list installed | head -n 10
# Ubuntu系: dpkg -l | head -n 10
```

```powershell
Get-WindowsFeature | Where-Object Installed
Get-HotFix | Select-Object -First 10
```

**主要オプション**：`Where-Object Installed`で導入済みの役割・機能のみに絞り込む。

**権限**：参照は一般ユーザーで可能である。

**リスク**：低（参照のみ）。導入・削除操作は依存関係を伴うため中リスクになる。

---

## A.16 早見表

| 管理目的 | Linux | Windows PowerShell |
|----------|-------|---------------------|
| ユーザー一覧 | `getent passwd` | `Get-LocalUser` / `Get-ADUser` |
| プロセス確認 | `ps`, `top` | `Get-Process` |
| サービス起動 | `systemctl start` | `Start-Service` |
| IP確認 | `ip addr` | `Get-NetIPAddress` |
| 待ち受けポート | `ss -tulpn` | `Get-NetTCPConnection` |
| ログ検索 | `journalctl`, `grep` | `Get-WinEvent` |
| ディスク使用量 | `df`, `du` | `Get-Volume` |
| 権限変更 | `chmod`, `chown`, `setfacl` | `icacls`, `Set-Acl` |
| ホスト名 | `hostnamectl` | `Rename-Computer` |
| 時刻同期 | `timedatectl`, `chronyc` | `w32tm` |
| ファイアウォール | `firewall-cmd`, `ufw` | `Get-NetFirewallRule` |
| 経路 | `ip route` | `Get-NetRoute` |
| DNS試験 | `getent`, `dig` | `Resolve-DnsName` |
| 疎通確認 | `ping`, `curl`, `nc` | `Test-NetConnection` |
| パッケージ/役割 | `dnf`, `dpkg` | `Get-WindowsFeature` |

早見表の各行に対応する詳細は、A.1からA.15を参照する。

次: [付録B 実務シナリオ](B_lab_scenarios.md)
