# 第7章 ネットワーク管理

疎通しないとき、アプリケーションを疑う前に、アドレス、経路、名前解決、ポート、ファイアウォールを層で切り分ける。

Linuxの `ip` コマンドとWindowsのNetTCPIPモジュールは、見た目のコマンド体系が違っても、確認すべき対象は同じである。

本章では、IPアドレス設計の基礎から、Linux/Windows双方の設定コマンド、ファイアウォール、そして疎通障害の切り分け手順までを、ラボ環境（`dc01`、`winapp01`、`web01`、`web02`）を例に扱う。

---

## 1. 学習目標

1. IPアドレス、サブネットマスク、デフォルトゲートウェイ、DNS（Domain Name System）、ルーティングの役割を説明できる
2. Linuxで `ip` コマンドとNetworkManagerを使ってネットワーク状態を確認・設定できる
3. Windowsで `ipconfig`、`Get-NetIPAddress`、`Get-NetRoute` などを使ってネットワーク状態を確認・設定できる
4. 待ち受けポートと接続状態を両OSで確認できる
5. nftables/firewalldとWindows Defender Firewallの基本操作を理解する
6. 疎通障害を層別（物理/リンク → IP → 名前解決 → ポート → ファイアウォール）に切り分けられる

---

## 2. 基本概念

### 2.1 IPアドレスとサブネット

**IPアドレス**は、ネットワーク上でホストを一意に識別する論理的な住所である。

IPv4では32ビットの数値を、`192.168.56.30` のように4つの10進数（オクテット）で表記する。

**サブネットマスク**（またはプレフィックス長）は、IPアドレスのうちどこまでがネットワーク部で、どこからがホスト部かを決める値である。

`192.168.56.30/24` という表記は、先頭24ビットがネットワーク部であることを示し、マスク表記では `255.255.255.0` と同じ意味になる。

同じ `192.168.56.0/24` に属するホスト同士は、同一セグメント（同一L2ネットワーク）として、ルーターを経由せず直接通信できるという前提がネットワーク設計の基本になる。

サブネットを誤って広く（またはプレフィックス長を短く）設定すると、想定していないホストまで同一セグメントとして扱われ、意図しない直接通信やブロードキャストの範囲拡大につながる。

逆に狭く設定すると、本来同一セグメント内のはずのホストへの通信がルーティング扱いになり、ゲートウェイ経由でしか届かなくなる。

### 2.2 デフォルトゲートウェイ

自分のサブネットに属さない宛先へ通信するとき、パケットを最初に渡す転送先が**デフォルトゲートウェイ**である。

多くの構成では、デフォルトゲートウェイはルーターやレイヤー3スイッチのインターフェースアドレスであり、サブネット内の先頭または末尾に近いアドレス（例: `192.168.56.1`）が割り当てられることが多い。

デフォルトゲートウェイの設定を誤ると、同一セグメント内の通信は成立するのに、外部やほかのセグメントへの通信だけが失敗するという特徴的な症状が出る。

複数のネットワークインターフェースカード（NIC）を持つホストでは、どのインターフェースがデフォルトゲートウェイを持つかによって、経路の優先順位（メトリック）が変わる点に注意する。

### 2.3 DNSと名前解決

**DNS（Domain Name System）**は、人間が扱いやすいホスト名やドメイン名と、機械が扱うIPアドレスを相互に変換する分散型のディレクトリサービスである。

人がブラウザーにドメイン名を入力する場面だけでなく、アプリケーション同士の通信、証明書の検証、ADの動作なども、内部的に名前解決へ依存している。

**名前解決**とは、ホスト名からIPアドレスを得る処理（正引き）、またはIPアドレスからホスト名を得る処理（逆引き）の総称である。

Linuxでは `/etc/resolv.conf` やsystemd-resolvedが、Windowsでは `Get-DnsClientServerAddress` で確認できるDNSクライアント設定が、この名前解決の起点になる。

DNSサーバー自体が停止していたり、誤ったレコードを返したりすると、IPアドレス直接指定では通信できるのに、ホスト名を使った通信だけが失敗するという典型的な症状が現れる。

### 2.4 ルーティング

OSは内部に**経路表（ルーティングテーブル）**を保持しており、宛先ネットワークごとに、どの送出インターフェースへ、どの次ホップ（ネクストホップ）へ転送するかを決定する。

経路表には、直接接続されたネットワークへの経路（自動的に追加される）、デフォルトゲートウェイへの経路（`0.0.0.0/0` またはWindowsでの `0.0.0.0/0`）、そして必要に応じて管理者が追加する静的経路が含まれる。

複数の経路が同じ宛先に一致する場合は、より長いプレフィックス（より詳細な経路）が優先され、同じ詳細度であればメトリック（コスト）が低いほうが優先される。

### 2.5 ポートとファイアウォール

TCP/UDPでは、1つのIPアドレスの中で複数のサービスを区別するために、0番から65535番までの**ポート番号**を使う。

サービスは特定のポートで**待ち受け（Listen）**状態になり、クライアントからの接続要求を待つ。

代表的なポートには、SSH（22番）、HTTP（80番）、HTTPS（443番）、DNS（53番）、RDP（3389番、Remote Desktop Protocol）、LDAP（389番、Lightweight Directory Access Protocol）などがある。

**ファイアウォール**は、許可されていない通信を遮断するフィルタ機能であり、OS単体で動くホストファイアウォールと、ネットワーク経路上に置かれるネットワークファイアウォール（クラウドのセキュリティグループやNSGを含む）の両方が存在する。

疎通が失敗する際は、この両方を確認しないと原因を見誤る。

---

## 3. Linuxでの実現方法

### 3.1 状態確認

現在のネットワーク状態を俯瞰するには、まずアドレスと経路、そして隣接ホストのARP/NDPキャッシュを確認する。

```bash
ip -br addr
ip route
ip neigh
resolvectl status 2>/dev/null || cat /etc/resolv.conf
```

`ip -br addr` は、インターフェースごとのアドレスと状態（UP/DOWN）を簡潔な1行形式で表示する。

`ip route` は経路表を表示し、`default via 192.168.56.1 dev eth0` のような行がデフォルトゲートウェイを示す。

`ip neigh` は、直近に通信した同一セグメント上の相手のMACアドレスとの対応（ARPキャッシュに相当）を表示する。

`resolvectl status` はsystemd-resolvedを使っている環境でのDNS設定を、使っていない環境では `/etc/resolv.conf` を直接確認する。

### 3.2 インターフェース単体の詳細確認

```bash
ip addr show eth0
ip link show eth0
ethtool eth0 2>/dev/null | grep -E 'Speed|Duplex|Link detected'
```

`ip link show` はL2（データリンク層）の状態、MTU、リンクの状態を表示する。

`ethtool` はNICの物理的なリンク速度や全二重/半二重の設定、ケーブルの接続状態を確認するために使う。

物理層やリンク層に問題がある場合、上位のIP設定がどれだけ正しくても通信は成立しない。

### 3.3 NetworkManagerによる設定

RHEL系・Ubuntu系の多くの現行ディストリビューションでは、**NetworkManager**が標準のネットワーク管理サービスである。

```bash
nmcli device status
nmcli connection show
nmcli connection show 'System eth0'
```

`nmcli device status` は物理/仮想インターフェースごとの状態（connected/disconnected）を一覧表示する。

`nmcli connection show` は設定済みの接続プロファイル一覧を表示し、`nmcli connection show <名前>` で特定プロファイルの詳細（IPアドレス、DNS、ゲートウェイなど）を確認する。

固定IPを設定する場合の例を示す。

```bash
# 警告: リモート接続中に実行すると、設定反映時に接続が切れる可能性がある
sudo nmcli connection modify 'System eth0' \
  ipv4.addresses 192.168.56.30/24 \
  ipv4.gateway 192.168.56.1 \
  ipv4.dns 192.168.56.10 \
  ipv4.method manual

sudo nmcli connection up 'System eth0'
```

権限はroot（またはsudo）が必要であり、リスクは接続断である。

リモートでの作業では、コンソールアクセス（クラウドのシリアルコンソールやハイパーバイザーのコンソール）を確保してから実行することが望ましい。

Ubuntu Serverではnetplanのyaml設定がNetworkManagerまたはsystemd-networkdのバックエンドを制御する構成もあるため、`/etc/netplan/*.yaml` の有無とバックエンドの種類を事前に確認する。

固定IP設定の詳細な手順は第2章のインストールと初期設定でも扱っている。

### 3.4 名前解決の確認と疎通試験

```bash
getent hosts dc01.lab.local
dig dc01.lab.local +short 2>/dev/null || nslookup dc01.lab.local
ping -c 3 192.168.56.10
ping -c 3 dc01.lab.local
traceroute 192.168.56.10 2>/dev/null || tracepath 192.168.56.10
```

`getent hosts` はOSの名前解決の仕組み（`/etc/hosts` とDNSの両方を含む `nsswitch.conf` の設定順）に従って名前を解決する。

`dig` や `nslookup` はDNSサーバーへ直接問い合わせるため、`/etc/hosts` の影響を受けずにDNSの応答だけを確認できる。

`ping` はICMP Echoによる到達性確認であり、`-c 3` はLinuxでの回数指定（Windowsでは既定が4回で回数指定は `-n`）である。

IPアドレス指定のpingが通り、ホスト名指定のpingだけ失敗する場合は、名前解決に問題があると強く推測できる。

`traceroute` は宛先までの経路上の各ホップを表示し、途中で応答が途切れる区間を特定する助けになる。

ただし、ICMPやUDPを使ったtracerouteは、経路上のファイアウォールでブロックされて全区間が表示されないこともあるため、あくまで参考情報として扱う。

### 3.5 ポートと接続状態の確認

```bash
ss -tulpn
sudo ss -tulpn | grep -E ':80|:443|:22'
ss -tn state established
```

`ss`（socket statisticsの略）は、`netstat` の後継として広く使われるソケット状態確認コマンドである。

オプションの意味は次のとおりである。

- `-t`：TCPソケットを表示する
- `-u`：UDPソケットを表示する
- `-l`：待ち受け（Listen）状態のソケットのみ表示する
- `-p`：プロセス名とPIDを表示する（root権限が必要な場合が多い）
- `-n`：ポート番号やアドレスを名前解決せず数値のまま表示する

実行例の想定出力は次のような形式になる。

```text
Netid State  Local Address:Port  Peer Address:Port  Process
tcp   LISTEN 0.0.0.0:22          0.0.0.0:*           users:(("sshd",pid=812,fd=3))
tcp   LISTEN 127.0.0.1:3306      0.0.0.0:*           users:(("mysqld",pid=1204,fd=21))
```

`0.0.0.0:22` は全インターフェースで22番ポートを待ち受けていることを示し、`127.0.0.1:3306` はループバックのみで待ち受けており、外部からは到達できないことを示す。

「サービスが起動しているのに外部から繋がらない」という障害では、この待ち受けアドレスの範囲を確認することが第一歩になる。

### 3.6 firewalldによるファイアウォール管理

RHEL系（RHEL 8/9、Rocky Linux、AlmaLinuxなど）では、**firewalld**が既定のファイアウォール管理フレームワークとして使われることが多い。

```bash
sudo firewall-cmd --state
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all
sudo firewall-cmd --list-all --zone=public
```

`firewall-cmd --state` はfirewalldサービス自体の稼働状況を返す。

`--list-all` は現在のゾーンで許可されているサービス、ポート、送信元などを一覧表示する。

サービスを許可する例を示す。

```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --reload
```

`--permanent` を付けないと再起動やreloadで設定が消える一時的な変更になる。

`--reload` を実行すると、`--permanent` で登録した設定が実行中の設定へ反映される。

> **警告**: リモートSSH接続中に、SSHサービスを許可するルールを誤って削除したり、ゾーンをデフォルト拒否に変更したりすると、自分自身が締め出される（ロックアウトされる）リスクがある。作業前に、コンソールアクセスの確保、またはSSHポートの明示的な許可を確認しておく。

権限はroot（sudo）が必須であり、リスクは中〜高（設定ミスで到達不能になる可能性がある）である。

### 3.7 nftablesによる低レベル制御

**nftables**は、Linuxカーネルのパケットフィルタリング機構であり、firewalldやufwの内部でも利用されている、より低レベルな枠組みである。

```bash
sudo nft list ruleset
sudo nft list tables
sudo nft list chain inet firewalld filter_IN_public_allow 2>/dev/null
```

`nft list ruleset` は現在有効な全ルールを表示するが、firewalldやufwを使っている環境では出力が長大かつ自動生成的になるため、直接手で編集することは推奨されない。

nftablesを直接運用する場合は、`/etc/nftables.conf` などの設定ファイルにルールを記述し、`systemctl enable --now nftables` で有効化する構成が一般的である。

firewalldやufwと直接のnftablesルール管理を混在させると、どちらが優先されるか把握しづらくなるため、どちらか一方に管理を統一することが実務上の原則である。

### 3.8 ufw（Ubuntu系での簡易ファイアウォール）

Ubuntu系では、nftables/iptablesを簡単な構文で扱える**ufw（Uncomplicated Firewall）**が使われることも多い。

```bash
sudo ufw status verbose
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow from 192.168.56.0/24 to any port 22
sudo ufw enable
```

`ufw enable` を実行する前に、SSHを許可するルールが入っていることを必ず確認する。

> **警告**: SSHルールを入れずに `ufw enable` を実行すると、その場でリモートセッションが切断され、コンソールアクセスがない限り復旧できなくなる可能性がある。

---

## 4. Windowsでの実現方法

### 4.1 状態確認

```powershell
ipconfig /all
Get-NetIPAddress -AddressFamily IPv4
Get-NetIPConfiguration
Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric
Get-DnsClientServerAddress
```

`ipconfig /all` は伝統的なコマンドラインツールで、インターフェースごとのIPアドレス、サブネットマスク、デフォルトゲートウェイ、DNSサーバー、DHCPの状態、MACアドレスをまとめて表示する。

`Get-NetIPAddress` はPowerShellのNetTCPIPモジュールに含まれるコマンドレットで、オブジェクトとして結果を返すため、`Where-Object` や `Select-Object` でフィルタや整形がしやすい。

`Get-NetIPConfiguration` は、IPアドレス、経路、DNSをまとめて一望できる高レベルなコマンドレットであり、日常の一次確認に向く。

`Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric` は、経路表をメトリック順に並べ、どの経路が優先されるかを確認する。

想定される出力例（`Get-NetIPConfiguration` の抜粋）は次のようになる。

```text
InterfaceAlias       : Ethernet
IPv4Address          : 192.168.56.20
IPv4DefaultGateway    : 192.168.56.1
DNSServer             : 192.168.56.10
```

`IPv4DefaultGateway` が空欄の場合、そのインターフェースからは自セグメント外への通信ができない。

### 4.2 固定IPアドレスの設定

```powershell
# 警告: 既存のIP構成を変更すると、リモート接続が切断される可能性がある
New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 192.168.56.20 -PrefixLength 24 -DefaultGateway 192.168.56.1
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 192.168.56.10
```

`New-NetIPAddress` は新しいIPアドレスを追加するコマンドレットであり、既に同じインターフェースにIPアドレスが設定済みの場合はエラーになることがある。

その場合は、先に `Remove-NetIPAddress` で既存アドレスを削除するか、`Set-NetIPAddress` で変更する。

DHCPへ戻す場合は次のようにする。

```powershell
Set-NetIPInterface -InterfaceAlias 'Ethernet' -Dhcp Enabled
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ResetServerAddresses
```

権限は管理者（Administrator）が必要であり、リスクは接続断である。

### 4.3 名前解決の確認と疎通試験

```powershell
Resolve-DnsName dc01.lab.local
Resolve-DnsName dc01.lab.local -Type A
ping 192.168.56.10
ping dc01.lab.local
tracert 192.168.56.10
Test-NetConnection 192.168.56.10 -Port 53
Test-NetConnection web01.lab.local -Port 80
```

`Resolve-DnsName` はLinuxの `dig`/`nslookup` に相当し、DNSサーバーへ直接問い合わせて結果を確認する。

`Test-NetConnection` はWindows特有の便利なコマンドレットで、ICMPの到達確認だけでなく、`-Port` を指定するとTCPポートへの接続確認まで一度に行える。

想定出力の例を示す。

```text
ComputerName     : dc01.lab.local
RemoteAddress    : 192.168.56.10
RemotePort       : 53
TcpTestSucceeded : True
```

`TcpTestSucceeded : False` の場合、名前解決とICMP到達性は問題なくても、対象ポートへのTCP接続が失敗していることを意味し、ファイアウォールまたはサービス未起動を疑う根拠になる。

### 4.4 ポートと接続状態の確認

```powershell
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess |
  Sort-Object LocalPort

Get-Process -Id (Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue).OwningProcess -ErrorAction SilentlyContinue

Get-NetTCPConnection -State Established | Select-Object -First 10
```

`Get-NetTCPConnection` は `netstat` に相当する情報をオブジェクトとして返す。

`-State Listen` は待ち受け中のソケットのみに絞り込み、`OwningProcess` はそのソケットを所有するプロセスIDを示す。

プロセスIDから実際のプロセス名を得るには、`Get-Process -Id` へ渡す。

### 4.5 Windows Defender Firewallの操作

```powershell
Get-NetFirewallProfile | Format-Table Name, Enabled

Get-NetFirewallRule -Direction Inbound -Enabled True |
  Where-Object {$_.Action -eq 'Allow'} |
  Select-Object -First 20 DisplayName, Profile, Direction, Action
```

Windows Defender Firewallは、**Domain**、**Private**、**Public**という3つのプロファイルを持ち、ネットワークの種別ごとに異なるルールセットを適用できる。

新しい受信許可ルールを追加する例を示す。

```powershell
# 例: HTTP許可（IISなど役割の導入で自動的にルールが追加されることも多い）
New-NetFirewallRule -DisplayName 'Allow HTTP Lab' -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow -Profile Domain,Private
```

> **警告**: `-Profile` を指定せずに作成すると全プロファイルへ適用される。社内ラボであっても、意図しないPublicプロファイルへの適用は避け、必要なプロファイルを明示する。

ルールを無効化・削除する例を示す。

```powershell
Disable-NetFirewallRule -DisplayName 'Allow HTTP Lab'
Remove-NetFirewallRule -DisplayName 'Allow HTTP Lab'
```

権限は管理者が必須であり、リスクは中（意図しない範囲への穴あけ、または誤ったルール削除による障害）である。

プロファイルの取り違え（Publicネットワーク扱いのインターフェースにDomain向けの緩い規則を期待する、など）は、実務でも頻出のミスである。

### 4.6 ネットワークプロファイルの確認と変更

```powershell
Get-NetConnectionProfile
Set-NetConnectionProfile -InterfaceAlias 'Ethernet' -NetworkCategory Private
```

ドメイン参加前のサーバーがPublicプロファイル扱いになっていると、必要な管理ポートがファイアウォールで塞がれたままになることがある。

ドメイン参加後は、DCへ到達できるネットワークが自動的にDomainプロファイルとして認識されるのが一般的な動作である。

---

## 5. 両OSの比較

| 目的 | Linux | Windows |
|------|-------|---------|
| IPアドレス確認 | `ip -br addr` / `ip addr` | `Get-NetIPAddress` / `ipconfig /all` |
| 固定IP設定 | `nmcli connection modify` | `New-NetIPAddress` / `Set-NetIPAddress` |
| 経路確認 | `ip route` | `Get-NetRoute` |
| DNS設定確認 | `resolvectl status` / `/etc/resolv.conf` | `Get-DnsClientServerAddress` |
| 名前解決試験 | `dig` / `getent hosts` | `Resolve-DnsName` |
| 疎通試験（ICMP） | `ping` | `ping` |
| 経路トレース | `traceroute` / `tracepath` | `tracert` |
| ポート込み疎通試験 | `nc -zv` / `curl` | `Test-NetConnection -Port` |
| 待ち受けポート確認 | `ss -tulpn` | `Get-NetTCPConnection -State Listen` |
| ファイアウォール状態 | `firewall-cmd --state` / `ufw status` | `Get-NetFirewallProfile` |
| ファイアウォール規則追加 | `firewall-cmd --add-service` / `ufw allow` | `New-NetFirewallRule` |
| 低レベルフィルタ | `nftables` | Windows Filtering Platform（WFP） |

Linuxは「複数の管理レイヤー（NetworkManager、firewalld、nftables）が積み重なる」構造であるのに対し、Windowsは「NetTCPIP/Defender Firewallという単一のモジュール体系にオブジェクト指向のコマンドレットが揃う」構造という違いがある。

どちらも最終的にはOSカーネルのパケット処理（Linuxのnetfilter、WindowsのWFP）へ行き着く点は共通している。

---

## 6. コマンド例

### 6.1 IPアドレスを確認する

**目的**: ホストに割り当てられているIPv4アドレスを一覧表示する。

**構文（Linux）**: `ip [-br] addr [show [<インターフェース名>]]`

```bash
ip -br addr
```

**構文（Windows）**: `Get-NetIPAddress [-AddressFamily <IPv4|IPv6>] [-InterfaceAlias <名前>]`

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where-Object IPAddress -notlike '127.*'
```

**想定出力（Linux）**:

```text
lo               UNKNOWN        127.0.0.1/8
eth0             UP             192.168.56.30/24
```

`UP` はリンクが有効であることを示し、`UNKNOWN` はループバックなど物理リンクの概念がないインターフェースで見られる正常な表示である。

**権限**: 一般ユーザーで実行可能。

**リスク**: 低（参照系のコマンドで状態を変更しない）。

### 6.2 待ち受けポートを確認する

**目的**: 現在どのポートでサービスが待ち受けているかを確認する。

```bash
ss -tulpn
```

```powershell
Get-NetTCPConnection -State Listen | Sort-Object LocalPort
```

**権限**: プロセス名まで見る場合はLinuxではroot、Windowsでも一部情報の取得に管理者権限が必要な場合がある。

**リスク**: 低。ただし出力にサービスやポートの構成情報が含まれるため、共有時の取り扱いに注意する。

### 6.3 特定ホストへの疎通とポート到達性を確認する

**目的**: IP疎通だけでなく、対象のTCPポートまで到達できるかを確認する。

```bash
nc -zv -w 3 192.168.56.10 389
curl -sv --connect-timeout 3 http://web01.lab.local/ -o /dev/null
```

```powershell
Test-NetConnection 192.168.56.10 -Port 389
```

`nc -z` はデータを送らず接続の成否のみを確認するスキャンモードであり、`-v` は詳細表示、`-w` はタイムアウト秒数を指定する。

**権限**: 一般ユーザーで実行可能なことが多いが、送信元ポートを固定するなど一部オプションはroot権限を要する場合がある。

**リスク**: 低。ただし対象環境やネットワーク機器によっては、スキャン的な挙動としてIDS/IPS（侵入検知・防御システム）のアラートを誘発することがあるため、許可された範囲でのみ実行する。

### 6.4 firewalldでポートを開ける

**目的**: 特定のTCPポートへの受信を恒久的に許可する。

```bash
sudo firewall-cmd --add-port=8443/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

**権限**: root（sudo）。

**リスク**: 中。誤って広い範囲やゾーンに適用すると、意図しない外部公開につながる。

> **警告**: `--permanent` を付け忘れると再起動で設定が消え、逆に一時変更のつもりで `--permanent` を付けると想定より長く穴が残る。両者の違いを常に意識する。

### 6.5 Windows Defender Firewallで受信を許可する

**目的**: 特定のTCPポートへの受信を許可するルールを作成する。

```powershell
New-NetFirewallRule -DisplayName 'Allow App 8443' -Direction Inbound -Protocol TCP -LocalPort 8443 -Action Allow -Profile Domain
```

**権限**: 管理者。

**リスク**: 中。`-Profile` の指定漏れや、削除し忘れた恒久ルールの残置がリスクになる。

### 6.6 経路を静的に追加する

**目的**: デフォルトゲートウェイ以外の経路で特定ネットワークへ到達させる。

```bash
# 警告: 誤った経路追加は既存通信を阻害する可能性がある
sudo ip route add 10.10.0.0/24 via 192.168.56.254 dev eth0
ip route show 10.10.0.0/24
```

```powershell
# 警告: 誤った経路追加は既存通信を阻害する可能性がある
New-NetRoute -DestinationPrefix 10.10.0.0/24 -InterfaceAlias 'Ethernet' -NextHop 192.168.56.254
Get-NetRoute -DestinationPrefix 10.10.0.0/24
```

Linuxでの `ip route add` は再起動で消える一時的な変更であり、恒久化にはNetworkManagerの設定やnetplanへの記載が必要である。

**権限**: Linuxはroot、Windowsは管理者。

**リスク**: 中〜高。既存経路と重複・矛盾すると通信断や意図しない迂回が発生する。

---

## 7. 実務上の注意点

1. クラウド環境では、OSファイアウォールに加えてセキュリティグループやネットワークACL（NSGなど）が二重に存在する。片方だけ開けても通信できない。
2. DNSレコードを修正しても、クライアント側やアプリケーション側のDNSキャッシュが古い応答を保持していることがある。
3. 複数NIC環境では、経路のメトリックと、応答パケットの戻り経路（非対称ルーティング）を必ず確認する。
4. 「pingだけ通る」ことは、対象サービスのTCPポートが開いていることの証拡にはならない。ICMPとTCPは別のプロトコルとして扱われる。
5. 変更前に現在の設定（`ip addr`、`ip route`、`Get-NetIPConfiguration` の出力）を記録しておくと、切り戻しが容易になる。
6. ネットワーク変更はメンテナンス時間帯を確保し、可能であれば帯域外管理（シリアルコンソール、IPMI、クラウドのシリアルコンソール機能）を用意してから実施する。

---

## 8. セキュリティ上の注意点

1. 管理ポート（SSH、RDP、DBの管理ポートなど）を `0.0.0.0/0` のような無制限の送信元へ開けない。
2. 使っていないサービスの待ち受けを放置しない。攻撃対象領域（アタックサーフェス）を不必要に広げる。
3. Windowsで、Publicプロファイル向けに、本来Domain/Private限定であるべき緩い規則を作らない。
4. 検証のために一時的に開けたポートやルールを、恒久化させたまま放置しない。棚卸しの仕組み（定期レビュー、命名規則、有効期限メモ）を持つ。
5. 平文プロトコル（Telnet、平文LDAPなど）でのリモート管理は避け、SSHやLDAPS（LDAP over SSL/TLS）などの暗号化された経路を使う。
6. ファイアウォールログを有効化し、想定外の送信元からの接続試行を検知できるようにする。

---

## 9. よくある障害

| 症状 | 典型的な原因 |
|------|--------------|
| ホスト名だけ通信が失敗し、IP直接指定は成功する | DNS障害、検索ドメインの誤り、`/etc/hosts` やWindowsのhostsファイルの誤記載 |
| 特定のポートだけ通信が失敗する | ファイアウォール、対象サービスの未起動、待ち受けアドレスの制限（127.0.0.1のみなど） |
| 同一セグメント内は通るが、外部だけ失敗する | デフォルトゲートウェイの誤り、NAT設定、上位プロキシの必須化 |
| 再起動後だけ通信ができなくなる | NetworkManagerとnetplanなど複数管理ツールの競合、DHCPでの意図しないアドレス変更 |
| 一部のクライアントからだけ到達できない | クライアント側のARP/経路キャッシュ、クライアント側ファイアウォール、VLAN設定の不一致 |
| pingは通るがアプリケーションが繋がらない | アプリケーション層のポート未許可、サービスクラッシュ、TLSハンドシェイク失敗 |
| DNS登録直後にだけ解決できない | ゾーン転送の遅延、TTL（Time To Live）によるキャッシュ、セカンダリDNSへの反映待ち |

---

## 10. 切り分け手順

疎通障害は、次のように層を下から積み上げて確認すると、原因の所在を効率よく絞り込める。

1. **物理層/リンク層の確認**: `ip -br addr`（Linux）や `Get-NetAdapter`（Windows）でリンクがUP状態か確認する。
2. **自ホストのIP設定確認**: IPアドレス、サブネットマスク、デフォルトゲートウェイが設計どおりか確認する。
3. **同一セグメント内の疎通確認**: 名前を使わず、IPアドレス直接指定で同一セグメントの別ホストへ`ping`する。
4. **デフォルトゲートウェイへの疎通確認**: ゲートウェイのIPアドレスへ直接`ping`する。
5. **名前解決の確認**: `dig`/`Resolve-DnsName` で、期待するIPアドレスが返るか確認する。
6. **対象ポートへの到達性確認**: `nc -zv` や `Test-NetConnection -Port` で、TCPレベルの到達性を確認する。
7. **双方のファイアウォール確認**: 送信元側と宛先側の両方のOSファイアウォール、および経路上のネットワークファイアウォール/セキュリティグループを確認する。
8. **経路の非対称性確認**: 行きは通るが応答が返らない場合、応答パケットが別経路を通って失われていないか確認する。
9. **アプリケーション層の確認**: TCP接続自体が成立するのにアプリケーションが応答しない場合、サービスログ、TLS証明書、設定ファイルを確認する。

この手順を「下位層から確認する」ことが重要であり、いきなりアプリケーションログを疑うと、実際には物理層やDNSの単純な問題を見落としやすい。

複数ホストにまたがる調査では、各ホストでの確認結果を一つの表にまとめると、どの区間で通信が途切れているかが視覚的に把握しやすくなる。

---

## 11. 章末問題

1. `192.168.56.30/24` における `/24` の意味を述べよ。
2. DNSサーバーが停止しているとき、IPアドレスを直接指定した通信は動作するのに、ホスト名を使った通信だけが失敗する理由を説明せよ。
3. `ss -tulpn` の各オプション（`-t`、`-u`、`-l`、`-p`、`-n`）が何を意味するか述べよ。
4. Windowsでファイアウォールの受信規則を追加しても通信できないとき、まず確認すべき項目を2つ挙げよ。
5. クラウド上の仮想マシンで、OSのファイアウォールでは該当ポートを許可したのに、外部から到達できない場合、次に確認すべきものは何か。
6. `traceroute`（または`tracert`）の結果が途中で応答を返さなくなったとき、それだけで「そのホップより先が完全に壊れている」と断定できない理由を述べよ。

---

## 12. 解答と解説

1. IPv4アドレスの先頭24ビットがネットワーク部であることを示すプレフィックス長であり、サブネットマスク `255.255.255.0` と同じ意味を持つ。
2. アプリケーションやOSの名前解決処理が、ホスト名からIPアドレスへの変換をDNSサーバーに依存しているため、DNSサーバーが応答しないと変換自体が失敗し、その後のIP通信に進めなくなるから。
3. `-t` はTCPソケットの表示、`-u` はUDPソケットの表示、`-l` は待ち受け状態のソケットのみの表示、`-p` はプロセス名とPIDの表示、`-n` はポート番号やアドレスを名前解決せず数値のまま表示することを意味する。
4. ファイアウォールルールが適用されているネットワークプロファイル（Domain/Private/Public）が実際の接続状態と一致しているか、また対象サービス自体がそのポートで待ち受けているかを確認する。
5. クラウド側のセキュリティグループ、ネットワークセキュリティグループ（NSG）、ネットワークACLなど、OSの外側にあるネットワークレベルのフィルタ設定。
6. ICMPやUDPベースのtracerouteパケット自体を、経路上の機器がポリシーにより意図的に破棄またはレート制限している場合があり、その場合は応答が見えないだけで実際の通信経路自体は生きていることがあるため。

---

## 13. ハンズオン演習

### 演習7-1 層別疎通切り分けシート作成

**前提**: `web01`（192.168.56.30）、`winapp01`（192.168.56.20）、`dc01`（192.168.56.10）がラボネットワーク上で稼働しており、相互に到達可能な設計になっていること。

**実行**:

1. 各ホストで `ip -br addr`（Linux）または `Get-NetIPConfiguration`（Windows）を実行し、自身のIP設定を記録する。
2. `web01` から `dc01` へ、IPアドレス直接指定で `ping -c 3 192.168.56.10` を実行する。
3. `web01` から `dc01` へ、ホスト名指定で `ping -c 3 dc01.lab.local` を実行する。
4. `web01` から `dc01` の53番ポート（DNS）へ `nc -zv -w 3 192.168.56.10 53` を実行する。
5. `winapp01` から同様に、`Test-NetConnection 192.168.56.10 -Port 53` を実行する。

**確認**: 全ステップの結果を1つの表（ホスト名、宛先、方式、成否）にまとめ、失敗した項目がないことを確認する。

**元に戻す**: 本演習は参照系コマンドのみで設定変更を行っていないため、元に戻す操作は不要である。

### 演習7-2 一時的なHTTP許可と後片付け

**前提**: `web01` にWebサーバー（httpdまたはnginx）が導入されていること。未導入の場合は第8章の内容を先に実施する。

**実行**:

1. `web01` でWebサーバーを起動し、`ss -tulpn | grep :80` で80番ポートの待ち受けを確認する。
2. `sudo firewall-cmd --add-service=http --permanent && sudo firewall-cmd --reload` でHTTPを許可する。
3. 別ホスト（`winapp01` や `mgmt01`）から `Test-NetConnection web01.lab.local -Port 80` またはブラウザーでアクセスする。

**確認**: 外部ホストから80番ポートへの接続が成功することを確認する。

**元に戻す**: 演習用に開けたルールが不要であれば、`sudo firewall-cmd --remove-service=http --permanent && sudo firewall-cmd --reload` で撤去し、`firewall-cmd --list-all` で許可が消えたことを確認する。

### 演習7-3 静的経路の追加と削除（任意、上級）

**前提**: ラボにルーティング検証用の追加セグメントがあるか、仮想の宛先ネットワークで構文確認のみ行う想定であること。事前にスナップショットを取得しておく。

**実行**:

1. 現在の経路表を記録する（`ip route` または `Get-NetRoute`）。
2. 演習7-2で確認したホストで、テスト用の静的経路を1件追加する（6.6節の例を参照）。
3. 経路表に追加された経路が反映されていることを確認する。

**確認**: `ip route show <対象ネットワーク>` または `Get-NetRoute -DestinationPrefix <対象ネットワーク>` で、追加した経路が想定どおりに登録されていることを確認する。

**元に戻す**: `sudo ip route del 10.10.0.0/24` または `Remove-NetRoute -DestinationPrefix 10.10.0.0/24` で削除し、経路表が元の状態に戻ったことを確認する。復旧に不安がある場合はスナップショットへ戻す。

---

## 14. 本章のまとめ

ネットワーク障害の調査は、思い込みで上位層から疑うのではなく、物理層・IP・名前解決・ポート・ファイアウォールという層を下から順に切ることで再現性高く原因へたどり着ける。

LinuxとWindowsはコマンド体系こそ異なるが、確認すべき対象（アドレス、経路、DNS、待ち受け、フィルタ）は共通しており、両OSの対応関係を押さえておけば混在環境でも同じ思考手順が使える。

次章では、そのホストへソフトウェアを導入し、安全に更新していくための、パッケージ管理と更新管理の方法を扱う。

次章: [第8章 ソフトウェアと更新管理](08_software_and_updates.md)
