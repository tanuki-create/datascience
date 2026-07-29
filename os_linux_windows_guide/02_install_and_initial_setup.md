# 第2章 インストールと初期設定

OSのインストールは、あとから変更しにくい決定を最初に固める作業でもある。
ディスクの分け方、ホスト名、時刻、管理用ネットワークを雑に決めると、第10章のドメイン参加や第12章の復旧で利子がつく。

本章では、LinuxとWindows Serverを仮想マシンへ入れ、運用の前提条件をCLI中心で整える。

---

## 1. 学習目標

1. RHEL系とUbuntu系、Windows Serverのインストール時に決める項目を説明できる
2. パーティション（またはボリューム）設計の基本方針を立てられる
3. ホスト名、タイムゾーン、NTP、ネットワーク、更新を両OSで設定・確認できる
4. 初期セキュリティ（不要サービスの抑制、管理経路、ファイアウォールの入口）を点検できる
5. 仮想マシン固有の注意点（ドライバー、時刻、ディスク、スナップショット）を列挙できる

---

## 2. 基本概念

### 2.1 インストールで決まるものと、あとで変えやすいもの

| 種別 | 例 | 備考 |
|------|----|------|
| あとから重い | ディスク分割の思想、ファイルシステム種別、ドメイン名設計 | 再作成やデータ移行が要ることがある |
| 手順を踏めば変更可 | ホスト名、IP、DNS、タイムゾーン | 依存サービスへの影響確認が必要 |
| 継続的に追随 | 更新プログラム、証明書、アカウント | 運用プロセス側 |

### 2.2 パーティション設計の考え方

**パーティション**は、ディスク上の区画である。
その上にファイルシステムを作り、Linuxではマウント、Windowsではドライブレターやマウントポイントで使う。

サーバーでよく使う方針は次だ。

1. **OS領域とデータ領域を分ける**  
   ログやバックアップ書き込みでルートが満杯になり、OS自体が管理不能になるのを防ぐ。
2. **将来の拡張を見込む**  
   クラウドならデータ用ディスクを後付けしやすい。最初から一本化しない選択肢がある。
3. **バックアップ単位を意識する**  
   復旧したい粒度とボリューム境界を揃える。

Linuxの例（学習用の素直な案）：

| マウント | サイズ目安 | 用途 |
|----------|------------|------|
| `/boot` または `/boot/efi` | 1 GB前後 | ブート |
| `/` | 20〜30 GB | OSとパッケージ |
| `/var` | 10 GB以上 | ログ、スプール |
| `/home` またはデータ用 | 残り | ユーザーやアプリデータ |
| swap | メモリとポリシー次第 | 必須ではない場合もある |

Windowsの例：

| ボリューム | 用途 |
|------------|------|
| `C:` | OS、役割と機能、ページファイル方針に注意 |
| `D:` など | アプリケーション、データ、ログ |

Evaluation環境でディスクが小さい場合は、まず単一ボリュームで始め、第6章で分割と拡張を学び直してよい。

### 2.3 ホスト名

**ホスト名**は、そのマシンを人間と他システムが指す名前である。
DNS名、証明書のCN/SAN、監視のインスタンス名、ログの識別子に効く。

方針：

- ASCIIの小文字、ハイフンまで、短く一意
- 役割が分かる名前（`web01`、`dc01`）
- あとでDNSのAレコードと一致させる

### 2.4 時刻とNTP

**NTP（Network Time Protocol）**は、時刻をネットワーク経由で合わせる仕組みである。
認証（Kerberos）、ログ突合、証明書の有効期間判定が時刻に依存する。
Active Directory環境では、数分のずれが認証失敗として表面化しやすい。

### 2.5 ネットワークの初期値

最低限そろえる項目は次だ。

- IPアドレスとプレフィックス（またはサブネットマスク）
- デフォルトゲートウェイ（外部通信が要る場合）
- DNSサーバー
- 検索ドメイン（任意だがAD連携で重要）

クラウドでは、メタデータサービスやDHCPで渡る値と、OS内の静的設定が競合しないかを確認する。

---

## 3. Linuxでの実現方法

### 3.1 インストールの流れ（概要）

1. ISOからブートする
2. 言語、キーボード、ディスク、ホスト名、ネットワーク、ユーザーを設定する
3. RHEL系ではサブスクリプションやリポジトリ接続を後で整えることがある
4. 初回起動後にSSH鍵、更新、時刻、ファイアウォールを確認する

インストーラーはAnaconda（RHEL系）やUbuntuのSubiquityなど。
本書はGUIウィザードの画面解説より、入ったあとの確認とCLI設定を重視する。

### 3.2 ホスト名

```bash
# 確認
hostnamectl

# 設定（要sudo）
sudo hostnamectl set-hostname web01
```

反映後、シェルを開き直すか、プロンプト再表示で確認する。
`/etc/hosts` に古い名前が残っていないかも見る。

```bash
getent hosts web01
grep -E 'web01|localhost' /etc/hosts
```

### 3.3 タイムゾーンとNTP

```bash
timedatectl
sudo timedatectl set-timezone Asia/Tokyo
```

RHEL系（chrony）：

```bash
sudo dnf install -y chrony
sudo systemctl enable --now chronyd
chronyc tracking
```

Ubuntu系（systemd-timesyncd または chrony）：

```bash
timedatectl status
# timesyncdを使う例
sudo systemctl enable --now systemd-timesyncd
```

クラウドイメージですでにchronyが入っていることが多い。
二重に競合するNTPクライアントを動かさない。

### 3.4 ネットワーク

**NetworkManager**がある環境では `nmcli` が扱いやすい。

```bash
nmcli general status
nmcli connection show
nmcli device status
ip addr
ip route
```

静的IPの例（接続名は環境で異なる）：

```bash
# 警告: リモート接続中のNIC設定変更は、接続断のリスクがある
sudo nmcli connection modify 'System eth0' \
  ipv4.method manual \
  ipv4.addresses 192.168.56.30/24 \
  ipv4.gateway 192.168.56.1 \
  ipv4.dns '192.168.56.10' \
  ipv4.dns-search 'lab.local'
sudo nmcli connection up 'System eth0'
```

UbuntuのNetplanを使う場合は `/etc/netplan/*.yaml` を編集し、`netplan try` で確認する。

```bash
sudo netplan try
sudo netplan apply
```

`netplan try` は一定時間で自動ロールバックできるため、リモート変更に向く。

### 3.5 更新プログラム

RHEL系：

```bash
sudo dnf check-update
sudo dnf upgrade -y
```

Ubuntu系：

```bash
sudo apt update
sudo apt upgrade -y
```

カーネル更新後は再起動が必要になることが多い。

```bash
needs-restarting -r   # RHEL系（yum-utils/dnf-utils）
# Ubuntuは update-notifier のチェックや /var/run/reboot-required を見る
test -f /var/run/reboot-required && cat /var/run/reboot-required
```

### 3.6 初期セキュリティ

```bash
# SSH設定の確認（変更前にバックアップ）
sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo sshd -t
sudo systemctl status sshd || sudo systemctl status ssh

# ファイアウォール
sudo systemctl status firewalld   # RHEL系で多い
sudo ufw status                   # Ubuntuで使う場合
```

方針の例：

- rootのパスワードSSHログインを無効化し、鍵認証へ
- 管理用IPからのみSSHを許可（firewalldのrich ruleやクラウドSG）
- 不要なサービスを `systemctl disable --now` で止める

---

## 4. Windowsでの実現方法

### 4.1 インストールの流れ（概要）

1. ISOからブートし、言語とキーボードを選ぶ
2. 「カスタム」でディスクを指定する（学習では1ディスクでも可）
3. 管理者パスワードを設定する（Server）
4. 初回ログイン後、ホスト名、ネットワーク、更新、役割追加前のベースラインを取る

Windows 11クライアントはOOBEの流れが異なるが、サーバー運用の本線はWindows Server側にある。

### 4.2 ホスト名

```powershell
# 確認
hostname
Get-ComputerInfo | Select-Object CsName

# 変更（再起動が必要）
# 警告: ドメイン参加済みホストの改名は手順が別。参加前に決めるのが安全
Rename-Computer -NewName 'winapp01' -Restart
```

### 4.3 タイムゾーンとNTP

```powershell
Get-TimeZone
Set-TimeZone -Id 'Tokyo Standard Time'
w32tm /query /status
w32tm /query /configuration
```

ワークグループ段階では、インターネット上のNTPやハイパーバイザー経由の時刻に寄せる。
ドメイン参加後は、メンバーがDCの階層に乗るのが基本になる（第10章）。

手動でピアを見る例：

```powershell
w32tm /resync
```

### 4.4 ネットワーク

```powershell
Get-NetIPConfiguration
Get-NetIPAddress -AddressFamily IPv4
Get-NetRoute -DestinationPrefix '0.0.0.0/0'
Get-DnsClientServerAddress
```

静的IPの例：

```powershell
# 警告: リモートデスクトップ接続中のIP変更は切断のリスクがある
$ifIndex = (Get-NetAdapter -Name 'Ethernet*').ifIndex
New-NetIPAddress -InterfaceIndex $ifIndex -IPAddress 192.168.56.20 -PrefixLength 24 -DefaultGateway 192.168.56.1
Set-DnsClientServerAddress -InterfaceIndex $ifIndex -ServerAddresses '192.168.56.10'
```

既存アドレスがある場合は `Remove-NetIPAddress` が先に必要になることがある。
コンソールアクセスを確保してから行う。

従来コマンド：

```powershell
ipconfig /all
route print
```

### 4.5 更新プログラム

```powershell
# Windows Update の状態確認（環境によりモジュールが異なる）
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10

# Server向け: 役割追加前に最新化することが多い
# 対話GUIの「設定 > Windows Update」または Windows Admin Center も併用可
```

PowerShellでの更新自動化は、環境（WSUS、Microsoft Update、クラウドのパッチ機構）に依存する。
第8章でパッチ管理として詳しく扱う。

### 4.6 初期セキュリティ

```powershell
Get-NetFirewallProfile | Format-Table Name, Enabled
Get-LocalUser
Get-LocalGroupMember -Group 'Administrators'
Enable-NetFirewallRule -DisplayGroup 'Remote Desktop'   # 必要なときだけ
```

方針の例：

- ビルトインAdministratorのパスワードを長く複雑にし、日常は別アカウント
- RDPは管理用ネットワークまたはジャンプホスト経由
- Windows Defenderのリアルタイム保護が有効か確認
- 不要な役割を入れない（入れたら第8章の手順で管理）

Server Coreの場合は、`sconfig` も初期設定の入口になる。

---

## 5. 両OSの比較

| 項目 | Linux | Windows Server |
|------|-------|----------------|
| ホスト名変更 | `hostnamectl` | `Rename-Computer`（再起動） |
| 時刻 | `timedatectl` + chrony/timesyncd | タイムゾーン設定 + W32Time |
| ネットワークCLI | `nmcli` / `ip` / netplan | `NetTCPIP` モジュール / `ipconfig` |
| 更新 | dnf / apt | Windows Update / Get-HotFix |
| 初期FW | firewalld / nftables / ufw | Windows Defender Firewall |
| 遠隔管理 | SSHが標準的 | RDP、WinRM、SSH（近年） |

仮想マシンではどちらも次が共通する。

- 準仮想化ドライバーまたは統合サービスの導入
- ホストとの時刻ずれ対策
- 管理用ネットワークと公開用ネットワークの分離（本番思想）

---

## 6. コマンド例

### 6.1 ホスト名を設定する

| 項目 | Linux | Windows |
|------|-------|---------|
| 目的 | マシン識別名の設定 | 同左 |
| 基本構文 | `hostnamectl set-hostname <name>` | `Rename-Computer -NewName <name>` |
| 権限 | root相当（sudo） | 管理者 |
| リスク | DNS・証明書・監視の名前ずれ | ドメイン参加後の改名失敗、再起動 |

### 6.2 IPアドレスを確認する

**Linux**

```bash
ip -br addr
ip route
resolvectl status 2>/dev/null || cat /etc/resolv.conf
```

**Windows**

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*'}
Get-DnsClientServerAddress -AddressFamily IPv4
```

### 6.3 時刻同期状態を確認する

**Linux**

```bash
timedatectl show
chronyc tracking 2>/dev/null || timedatectl timesync-status
```

**Windows**

```powershell
w32tm /query /status
Get-Date
```

出力の読み方：

- Linuxの `System clock synchronized: yes` または chrony の `Leap status : Normal`
- Windowsの `Stratum` と `Last Successful Sync Time`

### 6.4 更新の要否を見る

**Linux（RHEL系）**

```bash
sudo dnf check-update
```

**Linux（Ubuntu）**

```bash
sudo apt update
apt list --upgradable
```

**Windows**

```powershell
Get-HotFix | Measure-Object
# 追加の更新有無は GUI または管理基盤側で確認
```

---

## 7. 実務上の注意点

1. **名前とIPは設計表を先に書く**  
   インストール画面で思いつき命名しない。

2. **リモート設定変更はコンソールを確保してから**  
   IPやFWの変更で自分を締め出すのが初期構築あるあるである。

3. **更新とスナップショットの順序**  
   ラボでは「初期設定完了スナップショット → 更新 → 再スナップショット」が安全。

4. **クラウドのメタデータと静的設定**  
   DHCP前提イメージに静的IPを混在させると、再起動後に意図しない値へ戻ることがある。

5. **Windowsのホスト名は15文字制約を意識**  
   NetBIOS由来の制限で、長いDNS名の左15文字が切れる。最初から短くする。

---

## 8. セキュリティ上の注意点

1. インストーラーやクラウドの初期パスワードを放置しない
2. 公開ネットワークにRDP/SSHを無制限開放しない
3. 評価版でも、ラボ外から到達できるなら本番並みに扱う
4. セットアップ完了後、不要アカウントと自動ログオンを消す
5. 初期設定手順書にパスワードを平文で残さない

---

## 9. よくある障害

| 症状 | 典型原因 |
|------|----------|
| 入れた直後にSSH/RDPできない | FW、公開鍵未登録、ユーザー誤、ネットワーク未設定 |
| 名前解決だけ失敗 | DNS未設定、検索ドメイン不足 |
| 時刻がずれ続ける | NTP未起動、VMのホスト時刻同期の競合 |
| 更新できない | リポジトリ/プロキシ、Windows Update到達不可 |
| 再起動後にIPが消える | NetworkManagerとnetplanの競合、クラウドDHCP |

---

## 10. 切り分け手順

### ログインできない

1. ハイパーバイザーコンソールでローカルログインを試す
2. リンク状態とIPを確認する（`ip addr` / `Get-NetIPAddress`）
3. 疎通（pingはICMP許可に依存）と管理ポートを確認する
4. FWプロファイルを確認する
5. 認証方式（パスワード/鍵、ローカル/ドメイン）を切り分ける

### 更新できない

1. 外部またはリポジトリへの名前解決とHTTPS到達
2. プロキシ環境変数 / Windowsのプロキシ設定
3. ディスク空き容量
4. 時刻ずれによるTLS失敗

### 元に戻す方法

- netplanは `netplan try` の自動戻しを使う
- nmcliは変更前に `nmcli connection show <name>` を保存
- Windowsは変更前に現在の `Get-NetIPConfiguration` をファイルへリダイレクト
- ラボはスナップショットへ戻す

---

## 11. 章末問題

1. OS領域とデータ領域を分ける主目的を述べよ。
2. Active Directory利用時にNTPが重要な理由を述べよ。
3. リモートでLinuxのIPを変えるとき、`netplan try` が望ましい理由は何か。
4. Windowsで `Rename-Computer` 後に必要な操作は何か。
5. 仮想マシンに統合サービスやゲストツールを入れる理由を二つ挙げよ。

---

## 12. 解答と解説

1. ログやデータ増殖でルート/システムボリュームが満杯になり、OS管理自体が不能になるリスクを下げるため。  
2. Kerberos認証が時刻同期に依存するため。ずれが大きいとログオンやサービスチケット取得に失敗する。  
3. 一定時間内に確認できなければ自動で以前の設定に戻せるため、遠隔での締め出しを避けやすい。  
4. 再起動。完全に新ホスト名でサービスやチャネルが揃うのは再起動後である。  
5. 例：準仮想化によるI/O性能向上、優雅なシャットダウンや時刻・ハートビート連携の安定化。

---

## 13. ハンズオン演習

### 演習2-1 インストールとベースライン

**前提**

- READMEのVM構成に従い、`web01` と `winapp01` を新規作成できる
- スナップショット名 `before-ch02-install` を取得済み

**実行内容**

1. 各OSをインストールする
2. ホスト名を設計表どおりにする
3. タイムゾーンを `Asia/Tokyo` にする
4. IPとDNSをラボアドレスにする
5. 更新を適用し、必要なら再起動する

**確認方法**

Linux：

```bash
hostnamectl
timedatectl
ip -br addr
date
```

Windows：

```powershell
hostname
Get-TimeZone
Get-NetIPConfiguration
Get-Date
```

**元に戻す方法**

- 失敗時は `before-ch02-install` へ戻す
- 成功後は `after-ch02-baseline` を取る

### 演習2-2 自分を締め出す前のリハーサル

1. コンソールアクセスがある状態で、一時的に誤ったDNSを入れる
2. 名前解決失敗を確認する
3. 元のDNSへ戻す手順を実測する

Linux例：

```bash
resolvectl status 2>/dev/null || cat /etc/resolv.conf
# 変更と復元は接続名に合わせて実施
```

Windows例：

```powershell
Get-DnsClientServerAddress
# Set-DnsClientServerAddress で戻す
```

### 演習2-3 初期セキュリティチェックリスト

両OSで次をYes/Noで埋める。

- [ ] 初期パスワードを変更した
- [ ] 管理ポートの公開範囲を制限した
- [ ] 不要サービスを止めた（または次章以降で止める対象を列挙した）
- [ ] ホスト名とDNS設計が一致している
- [ ] 時刻同期が有効である

---

## 本章のまとめ

インストール後に揃えるべきは、名前、時刻、ネットワーク、更新、管理経路の五点セットである。
これらが欠けると、あとの権限、AD、証明書、ログ調査がことごとく不安定になる。

次章では、ファイルとディレクトリという「最も日常的な操作対象」を両OSで扱う。

次章: [第3章 ファイルとディレクトリ](03_files_and_directories.md)
