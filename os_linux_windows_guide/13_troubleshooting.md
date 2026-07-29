# 第13章 トラブルシューティング

ここまでの章は、部品ごとの理解を積み上げる章だった。

本章は、症状から入り、層を一つずつ下りていくための手順書である。

10種類の典型症状（OS起動不能、ログイン不可、CPU高負荷、メモリ不足、ディスク不足、サービス起動失敗、ネットワーク接続不可、DNS解決不可、ファイルアクセス不可、更新プログラム適用後の不具合）について、LinuxとWindowsの双方で調査手順を示す。

---

## 1. 学習目標

1. 典型10症状について、初動、仮説の立て方、確認コマンド、回復の流れを説明できる。
2. 変更履歴と観測情報（ログ、メトリクス）を先に保全する習慣を持てる。
3. 両OSで同等の切り分けツリーを自力で組み立てられる。
4. 症状ごとの調査コマンドをLinux・Windowsで対応づけて即座に引き出せる。

---

## 2. 基本概念（共通手順）

どの症状であっても、次の順序を崩さずに進める。

1. **影響範囲の特定**：1台だけか全体か、いつから発生しているかを確認する。
2. **状態の保全**：時刻、プロセス一覧、接続状態、ログのスナップショットを、対処を始める前に取得しておく。
3. **直近の変更の洗い出し**：パッチ適用、設定変更、デプロイ、権限変更、ネットワーク変更のうち、直近に行われたものを確認する。
4. **層別の仮説立て**：ハードウェア・仮想化層、OS層、サービス層、アプリケーション層、利用者側という順で仮説を立てる。
5. **一つずつ変更して試す**：複数の変更を同時に行うと、何が効いたのか分からなくなる。
6. **確認と記録**：復旧を確認したら、原因、対処、所要時間を記録する。

保全を後回しにして先に対処を始めると、対処自体が原因調査に必要な証跡を消してしまうことがある。

障害対応では、直そうとする前に、まず何が起きているかを記録する。

### 2.1 エスカレーションの基準

一次対応者だけで解決できない場合に備え、次のような基準をあらかじめ決めておくと判断が速くなる。

1. **所要時間の上限**：一次対応で一定時間（例えば30分）以内に切り分けが進まない場合、二次対応者へ引き継ぐ。
2. **影響範囲の拡大**：単一ホストの問題だと思っていたものが、複数ホストや複数サービスへ広がった場合。
3. **復旧不能の疑い**：バックアップからの復元やベアメタル復旧が必要と判断される場合。
4. **セキュリティ侵害の疑い**：不正アクセスやマルウェアの痕跡が見つかった場合は、通常の障害対応とは別のセキュリティ対応手順に切り替える。

これらの基準を個々の対応者の判断だけに委ねず、チームとして事前に合意しておく。

---

## 3. OSが起動しない

### 3.1 Linux

兆候として、GRUB（ブートローダー）でのエラー、カーネルパニック、emergency modeへの落下、画面が真っ黒のまま進まない、といった状態が挙げられる。

調査の流れは次のとおりである。

1. ハイパーバイザーやクラウドのコンソールで、実際にどこで停止しているかを目視で確認する。
2. GRUBメニューから、直前の世代のカーネルや、レスキューモードでの起動を試す。
3. 起動できた場合、`journalctl -xb` と `systemctl --failed` で失敗したユニットを確認する。
4. `/etc/fstab` の記述誤り、ルートファイルシステムの破損、ディスク満杯を疑う。

```bash
# レスキュー環境やemergency mode内での例
mount -o remount,rw /
journalctl -xb | less
systemctl --failed
cat /etc/fstab
df -h
```

**想定出力**：

```text
UNIT           LOAD   ACTIVE SUB    DESCRIPTION
● local-fs.target loaded failed failed Local File Systems
```

**読み方**：`systemctl --failed` に表示されるユニットが、起動を止めている直接の原因であることが多い。
上記の例では `local-fs.target` の失敗が示されており、`fstab` に記載されたマウントのいずれかが失敗していることを示唆する。

`/etc/fstab` に存在しないデバイスやマウントポイントが記載されていると、起動プロセスがそこで待機し続け、結果として起動が完了しないという症状につながる。

回復例として、問題のある行を`fstab`から一時的にコメントアウトする、対象ディスクを拡張する、壊れたユニットを無効化する、といった対応がある。

**警告**：`fstab` を編集する際は、必ずコピーを取ってから変更する。
誤った記述のまま再起動すると、同じ症状を再現してしまう。

### 3.2 Windows

兆候として、自動修復画面、Boot Manager（起動マネージャー）の失敗、Bug Check（いわゆるブルースクリーン）、ログイン画面の手前でのループ、といった状態が挙げられる。

調査の流れは次のとおりである。

1. **WinRE（Windows回復環境）**を起動し、詳細オプションへ進む。
2. スタートアップ修復、セーフモードでの起動を試す。
3. 起動構成に問題がある場合、`bootrec` や `bcdedit` で修復を試みる（事前知識とバックアップが前提になる）。
4. オフラインの状態でイベントログを参照する手段（別マシンへディスクを接続するなど）を検討する。

```powershell
# 起動できるようになった後の確認
Get-WinEvent -LogName System -MaxEvents 50 |
  Where-Object { $_.LevelDisplayName -in 'Error', 'Critical' }
```

**想定出力**：

```text
TimeCreated          Id LevelDisplayName Message
-----------          -- ---------------- -------
2026/07/29 3:12:05 41  Critical         The system has rebooted without cleanly shutting down first.
```

**読み方**：`LevelDisplayName` が `Critical` のイベントは、システムの継続動作に影響する重大なエラーであり、直前の時刻のイベントから原因を絞り込む。
イベントID 41は、電源断や強制リセットのように正常なシャットダウン処理を経ずに再起動したことを示す代表的なIDである。

回復例として、直前に適用したドライバーや更新プログラムの削除、ディスクのオンライン化、バックアップからの復元がある。

**警告**：`bootrec /fixmbr` のようなブート関連の修復コマンドは、誤ったディスクに対して実行すると別の問題を引き起こす。
対象ディスクを必ず確認してから実行する。

---

## 4. ログインできない

### 4.1 Linux

1. コンソールからは入れるか、SSH経由でのログインだけが失敗しているかを切り分ける。
2. ディスク満杯によって、シェルの初期化処理自体が失敗していないかを確認する。
3. `/etc/passwd`、ログインシェルの設定、`sudoers`、PAM（Pluggable Authentication Modules）、`sshd`の設定を確認する。
4. AD（Active Directory）連携環境では、SSSD（System Security Services Daemon）の状態と時刻同期を確認する。

```bash
df -h /
sudo journalctl -u sshd -n 50 --no-pager
sudo journalctl -u sssd -n 50 --no-pager
```

**想定出力**：

```text
sshd[2044]: Failed password for operator from 192.168.56.40 port 51322 ssh2
sshd[2044]: Connection closed by authenticating user operator 192.168.56.40 port 51322 [preauth]
```

**読み方**：`journalctl -u sshd` に `Failed password` や `Connection closed` が繰り返されている場合、認証方式や鍵の設定に問題がある可能性が高い。
同一の送信元から短時間に大量の失敗が続く場合は、正規利用者の設定誤りだけでなく、総当たり攻撃の可能性も並行して疑う。

ディスクが満杯だと、ログイン時に一時ファイルを作成できず、ログイン処理自体が失敗するという分かりにくい症状になる。

### 4.2 Windows

1. ローカル管理者アカウントでは入れるか、ドメインアカウントだけが失敗しているかを切り分ける。
2. 時刻のずれ、DNSの誤り、DC（ドメインコントローラー）への到達性、セキュアチャネルの状態を確認する。
3. アカウントロックアウト、ユーザープロファイルの破損を確認する。

```powershell
Test-ComputerSecureChannel -Verbose
nltest /dsgetdc:lab.local
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20 -ErrorAction SilentlyContinue
```

**読み方**：イベントID 4625は「アカウントのログオンに失敗した」ことを示し、`Failure Reason`（失敗理由）の欄でパスワード誤りかロックアウトかを判別できる。

`Test-ComputerSecureChannel` が `False` を返す場合、マシン自体とDCの信頼関係が壊れており、ドメインユーザー全員がそのマシンでログインできなくなる（第10章参照）。

---

## 5. CPU使用率が高い

共通して、上位プロセスのPID、開始時刻、コマンドライン、直近のデプロイ内容を確認する。

### 5.1 Linux

```bash
ps -eo pid,ppid,user,%cpu,%mem,cmd --sort=-%cpu | head -n 15
top
pidstat 1 5
```

**読み方**：`ps` の `%cpu` が突出して高いプロセスのPIDを控え、そのプロセスがいつ起動したか（`ps -o lstart -p PID`）を確認する。

`pidstat 1 5` は1秒間隔で5回サンプリングし、瞬間的なスパイクか継続的な高負荷かを見分ける材料になる。

**想定出力**：

```text
PID PPID USER  %CPU %MEM CMD
812    1 root  87.3  1.2 /usr/sbin/nginx
```

単発の値だけでは瞬間的な負荷かどうか判断できないため、`pidstat`のように時系列で複数回観測する。

### 5.2 Windows

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 15 Id, ProcessName, CPU, StartTime
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 5
```

**読み方**：`Get-Process` の `CPU` 列は起動時からの累積使用時間であり、瞬間的な使用率ではない点に注意する。

瞬間値を見たい場合は `Get-Counter` のようなパフォーマンスカウンターを使う。

**想定出力**：

```text
Id ProcessName CPU      StartTime
-- ----------- ---      ---------
4820 w3wp       1523.44 2026/07/28 9:02:11
```

`CPU`が非常に大きい値であっても、起動からの経過時間が長ければ平均的な負荷は低いことがあるため、`StartTime`と合わせて評価する。

両OSに共通する切り分けの候補として、無限ループに陥ったアプリケーション、バックアップジョブの多重実行、マルウェア対策製品の再スキャン、意図しない暗号資産マイニングプロセスなどが挙げられる。

---

## 6. メモリが不足している

### 6.1 Linux

```bash
free -h
ps -eo pid,user,%mem,rss,cmd --sort=-%mem | head -n 15
dmesg -T | grep -i 'out of memory\|oom'
sudo journalctl -k | grep -i oom
```

**想定出力**：

```text
              total        used        free      shared  buff/cache   available
Mem:           3.8Gi       3.5Gi        89Mi        12Mi       210Mi       120Mi
```

```text
kernel: Out of memory: Killed process 2044 (java) total-vm:4123456kB
```

**読み方**：`free -h` の `available` が小さく、かつ `dmesg` にOOM（Out Of Memory）関連のメッセージがあれば、**OOM Killer**が動作し、いずれかのプロセスを強制終了した可能性が高い。

OOM Killerが働くと、対象プロセスが前触れなく突然終了する。
上記のようなメッセージが見つかった場合、`total-vm`（要求していた仮想メモリ量）と実際に搭載されている物理メモリ量を比較し、要求自体が過大だったのか、他プロセスとの合計が超過したのかを見分ける。

### 6.2 Windows

```powershell
Get-Counter '\Memory\Available MBytes'
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Id, ProcessName, WorkingSet
Get-CimInstance Win32_PageFileUsage
```

**読み方**：`Available MBytes` が小さい状態が続いている場合、メモリリークや同時実行数の過多、ページファイルの不足を疑う。

`Win32_PageFileUsage` の `CurrentUsage` がページファイルのサイズに近づいている場合、物理メモリ不足を仮想メモリで補い切れなくなりつつある兆候である。

**想定出力**：

```text
CounterSamples : {\\winapp01\memory\available mbytes :
                  CookedValue : 87.234}
```

`Available MBytes`が数百MB未満まで低下した状態が継続していれば、メモリ不足として扱い、プロセスの見直しかメモリ増設を検討する。

---

## 7. ディスク容量が不足している

### 7.1 Linux

```bash
df -h
df -i
du -xhd1 / | sort -h
du -xhd1 /var | sort -h
sudo lsof | grep -i '(deleted)' | head -n 20
```

**読み方**：`df -h` の `Use%` が高くても、`lsof` に `(deleted)` と表示されるファイルが多い場合、削除済みだがプロセスが開いたままのファイルが実体容量を占有し続けている可能性がある。

この場合、該当ファイルを掴んでいるプロセスを再起動すると領域が解放される。

`df -i` でinode（Linuxファイルシステムのメタデータ構造）の枯渇も確認する。
容量に余裕があってもinodeが枯渇していると、新規ファイルを作成できなくなる。

**想定出力**：

```text
Filesystem      Inodes  IUsed   IFree IUse% Mounted on
/dev/sda1      1310720 1310720      0  100% /
```

`IUse%`が100%に達している場合、`df -h`側の容量に余裕があっても新規ファイル作成がすべて失敗する。
小さなファイルを大量に作成するアプリケーション（セッションファイル、キャッシュなど）でよく見られる。

### 7.2 Windows

```powershell
Get-Volume
vssadmin list shadowstorage
```

大きなディレクトリの調査は第6章で扱ったコマンドを使う。

**読み方**：`vssadmin list shadowstorage` の `Used Shadow Copy Storage space` が大きい場合、シャドウコピー（VSSのスナップショット領域）の肥大化がディスク容量を圧迫している可能性がある。

**想定出力**：

```text
DriveLetter FriendlyName    FileSystemType Size   SizeRemaining
----------- ------------    -------------- ----   -------------
C           OS               NTFS          80 GB  2.1 GB
```

`SizeRemaining`が極端に小さい場合、ログファイルの肥大化、一時ファイルの蓄積、シャドウコピー領域の圧迫のいずれかを疑い、大きなディレクトリから順に確認する。

---

## 8. サービスが起動しない

### 8.1 Linux

```bash
systemctl status nginx -l
journalctl -u nginx -b --no-pager
systemctl cat nginx
nginx -t
```

**読み方**：`systemctl status` の `Active` 行が `failed` であれば起動失敗を示し、直後の数行に失敗理由の要約が表示されることが多い。

`nginx -t` のような設定検証コマンドは、多くのサービスに用意されており、設定ファイルの構文誤りを起動前に発見できる。

代表的な原因として、依存サービスの未起動、実行ユーザーの権限不足、ポートの競合、SELinuxによる拒否、実行バイナリの欠落が挙げられる。

**想定出力**：

```text
● nginx.service - The nginx HTTP and reverse proxy server
     Active: failed (Result: exit-code) since Wed 2026-07-29 09:12:03 JST
    Process: 1122 ExecStart=/usr/sbin/nginx (code=exited, status=1/FAILURE)
```

**読み方**：`Result: exit-code` は、プロセス自体が起動を試みたが異常終了したことを示し、権限やポート競合よりも設定内容自体に問題がある可能性が高い。
これに対し `Result: timeout` であれば、起動処理が既定時間内に完了しなかったことを示し、依存先の応答待ちなどを疑う。

### 8.2 Windows

```powershell
Get-Service W3SVC | Format-List *
sc.exe qc W3SVC
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Service Control Manager'} -MaxEvents 30
```

**読み方**：`sc.exe qc` の `SERVICE_START_NAME` は、そのサービスが実行時に使うログオンアカウントを示し、このアカウントのパスワードが期限切れになっていると起動に失敗する。

SCM（Service Control Manager）関連のイベントには、依存サービスが起動していないために失敗した、といった具体的な理由が記録されることが多い。

依存サービスの停止、ログオンアカウントのパスワード期限切れが、Windowsサービス起動失敗の定番の原因である。

**想定出力**：

```text
Status   Name    DisplayName
------   ----    -----------
Stopped  W3SVC   World Wide Web Publishing Service
```

`Get-Service`だけでは`Stopped`であることしか分からないため、原因の特定には必ずイベントログとの突き合わせが必要になる。

---

## 9. ネットワークに接続できない

第7章で扱った層別の切り分け（物理・リンク層、IP層、ルーティング、ファイアウォール、アプリケーション層）をそのまま適用する。

### 9.1 Linux

```bash
ip -br link
ip -br addr
ip route
ping -c 2 <ゲートウェイ>
ping -c 2 <宛先>
sudo firewall-cmd --list-all
```

**読み方**：`ip -br link` で対象インターフェースが `UP` になっているか、`ip -br addr` でIPアドレスが正しく割り当てられているかを確認する。

ゲートウェイへの `ping` が失敗する場合は同一セグメント内の問題、ゲートウェイには到達するが宛先には届かない場合はルーティングやその先のネットワークの問題を疑う。

**想定出力**：

```text
2: eth0             UP             192.168.56.30/24
default via 192.168.56.1 dev eth0
```

`ip route`の`default via`が表示されない場合、デフォルトゲートウェイ自体が設定されておらず、同一セグメント外への通信がすべて失敗する状態になっている。

### 9.2 Windows

```powershell
Get-NetIPConfiguration
Get-NetRoute -DestinationPrefix '0.0.0.0/0'
Test-NetConnection <宛先> -Port 443
Get-NetFirewallProfile
```

**読み方**：`Test-NetConnection` の `TcpTestSucceeded` が `False` の場合、宛先までのIP到達性、または対象ポートでのアプリケーション応答のいずれかに問題がある。

クラウド環境では、OS側のファイアウォールに加え、セキュリティグループ（AWS）やNSG（Network Security Group、Azure）のようなクラウド側のフィルタも併せて確認する。

OS側の設定だけを何度確認しても、クラウド側で遮断されていれば疎通しない。

**想定出力**：

```text
ComputerName     : winapp01
RemotePort       : 443
TcpTestSucceeded : False
```

`TcpTestSucceeded`が`False`であっても、`PingSucceeded`（ICMP）が`True`であれば、ネットワーク経路自体は生きており、対象ポートまたはアプリケーション側の問題に絞り込める。

---

## 10. DNS名前解決ができない

### 10.1 Linux

```bash
cat /etc/resolv.conf
getent hosts dc01.lab.local
dig dc01.lab.local @192.168.56.10
resolvectl status
```

**読み方**：`dig` で明示的にDNSサーバーを指定した問い合わせが成功し、`getent hosts`（システムの名前解決全体）が失敗する場合、`nsswitch.conf` の設定やローカルキャッシュ側に問題がある可能性が高い。

`resolvectl status` では、インターフェースごとに実際に使われているDNSサーバーとサーチドメインを確認できる。

**想定出力**：

```text
;; connection timed out; no servers could be reached
```

`dig`がこのように応答した場合、DNSサーバー自体への到達性がない状態を示し、名前解決の設定ではなくネットワーク疎通の問題である可能性が高い。

### 10.2 Windows

```powershell
Get-DnsClientServerAddress
Resolve-DnsName dc01.lab.local
Resolve-DnsName dc01.lab.local -Server 192.168.56.10
ipconfig /flushdns
```

**読み方**：`-Server` を指定した問い合わせが成功し、指定しない問い合わせが失敗する場合、クライアントに設定されているDNSサーバー自体か、そこまでの経路に問題がある。

`ipconfig /flushdns` はローカルのDNSキャッシュを消去するコマンドであり、古いキャッシュが残っていることが疑われる場合に使う。

**想定出力**：

```text
Name           : dc01.lab.local
QueryType      : A
IPAddress      : 192.168.56.10
```

指定したDNSサーバーへの問い合わせでのみ正しい結果が返る場合、クライアントの既定DNSサーバー設定自体を疑う。

両OSに共通して、DNSサーバー自体の停止、名前解決の設定誤り（サーチドメイン、スタブリゾルバー）、キャッシュの陳腐化を切り分けの軸にする。

---

## 11. ファイルにアクセスできない

### 11.1 Linux

```bash
namei -l /path/to/file
getfacl /path/to/file
ls -lZ /path/to/file
getenforce
```

**読み方**：`namei -l` はパスの各階層ごとの権限を表示するため、途中のディレクトリに実行権限（`x`）がなく、目的のファイルへたどり着けないという原因を発見しやすい。

`ls -lZ` でSELinuxコンテキストを表示し、SELinuxが `Enforcing` の場合はコンテキスト不一致による拒否も候補に入れる。

**想定出力**：

```text
f: /var/www/html/index.html
 uid: 0 gid: 0 mode:0644
 owner: root  group: root
d: /var/www/html
 uid: 0 gid: 0 mode:0750
```

`namei -l`の出力を上から順にたどり、目的のファイルにたどり着くまでの各ディレクトリの権限を確認する。
途中のディレクトリの`mode`に実行権限（`x`）がなければ、ファイル自体の権限が正しくてもアクセスは拒否される。

### 11.2 Windows

```powershell
icacls C:\path\to\file
whoami /groups
Get-SmbShare -ErrorAction SilentlyContinue
```

**読み方**：`icacls` の出力にある `(F)`（フルコントロール）、`(M)`（変更）、`(R)`（読み取り）などの略号で、対象アカウントに付与された権限の種類を確認する。

共有フォルダー経由でのアクセスでは、NTFSアクセス許可に加えて共有権限も重なって評価されるため、両方を確認する。

ファイルロック、暗号化属性、オフライン属性、マルウェア対策製品による隔離も、アクセス不能の候補として挙げられる。

**想定出力**：

```text
C:\app\config.yml BUILTIN\Administrators:(F)
                   LAB\app-admins:(M)
                   LAB\operator:(R)
```

**読み方**：`icacls`の各行末尾にある略号（`F`はフルコントロール、`M`は変更、`R`は読み取り）で、対象アカウントごとの権限を確認する。
対象アカウントが一覧に存在しない場合、そもそも権限が付与されていないことを意味する。

---

## 12. 更新プログラム適用後に不具合が発生した

共通の手順は次のとおりである。

1. 何を適用したかを一覧化する（適用日時とKB番号、またはパッケージ名とバージョン）。
2. 症状が、更新されたコンポーネントと関連しているかを確認する。
3. 一時的な回避策（サービスの設定変更、機能の無効化）を検討する。
4. ベンダーが公開している既知の不具合情報を確認する。
5. 切り戻し（アンインストール、前回のカーネルでの起動、バックアップやスナップショットからの復元）を判断する。

### 12.1 Linux

```bash
rpm -qa --last | head -n 20
grep -i upgrade /var/log/dnf.log | tail -n 20
# Ubuntu系: /var/log/apt/history.log
```

**読み方**：`rpm -qa --last` は最近インストール・更新されたパッケージを新しい順に表示し、症状発生時刻に近いパッケージを絞り込める。

カーネル更新が疑われる場合は、GRUBメニューから前回のカーネルで起動し、症状が再現するかを確認する。

**想定出力**：

```text
kernel-5.14.0-503.el9   Tue 29 Jul 2026 02:16:40 AM JST
nginx-1.24.0-1.el9      Tue 29 Jul 2026 02:16:12 AM JST
```

症状発生の直前に更新されたパッケージが複数ある場合は、影響が大きい順（カーネルやミドルウェアなど土台に近いもの）から検証する。

### 12.2 Windows

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20
Get-WinEvent -LogName Setup -MaxEvents 50
```

**読み方**：`InstalledOn` を症状発生時刻と突き合わせ、直前に適用された`HotFixID`（KB番号）を候補として絞り込む。

切り戻しは、コントロールパネルの更新履歴、または `wusa /uninstall /kb:番号` のようなコマンドで行う。

**想定出力**：

```text
Source     Description      HotFixID      InstalledOn
------     -----------      --------      -----------
WINAPP01   Security Update  KB5031354     2026/7/28
```

`InstalledOn`が症状発生日の前日や当日と一致する場合、その`HotFixID`を最優先の調査対象として、ベンダーの既知不具合情報を確認する。

**警告**：ドメインコントローラーやクラスタ構成での切り戻しは、単独のメンバーサーバーとは手順が異なる場合がある。
単独のラボ環境以外では、影響範囲を確認せずに安易に切り戻さない。

---

## 13. 両OSの比較（調査コマンド早見）

| 症状 | Linux | Windows |
|------|-------|---------|
| OS起動不能 | `journalctl -xb`、rescueモード | WinRE、System/Setupログ |
| ログイン不可 | `journalctl -u sshd/sssd` | イベントID 4625、セキュアチャネル |
| CPU高負荷 | `ps`、`top`、`pidstat` | `Get-Process`、`Get-Counter` |
| メモリ不足 | `free`、`dmesg`のOOM記録 | `Available MBytes`、`Win32_PageFileUsage` |
| ディスク不足 | `df`、`du`、inode確認 | `Get-Volume`、シャドウコピー |
| サービス起動失敗 | `systemctl status`、`journalctl -u` | `Get-Service`、SCMイベント |
| ネットワーク不可 | `ip`、`ss`、`firewall-cmd` | `Get-Net*`、`Test-NetConnection` |
| DNS解決不可 | `resolv.conf`、`dig`、`resolvectl` | `Resolve-DnsName`、`ipconfig /flushdns` |
| ファイルアクセス不可 | `namei`、`getfacl`、SELinux | `icacls`、`whoami /groups` |
| 更新後不具合 | `rpm -qa --last`、dnf/aptログ | `Get-HotFix`、Setupログ |

---

## 14. 実務上の注意点とセキュリティ上の注意点

1. 本番環境で、破壊的な可能性があるコマンドを確認なしに試し打ちしない。
2. 「掃除」と称してログや証跡を先に消してから調査を始めない。証跡は原因究明の唯一の手がかりになることが多い。
3. 共有の管理者アカウントで変更を行うと、誰が何をしたか追跡できなくなる。
4. 切り戻しに成功した後も、再発防止のための根本原因分析を省略しない。
5. 障害対応中の一時的な権限昇格やファイアウォール緩和は、対応終了後に必ず元へ戻す。
6. 障害対応の記録には、調査に使った実際のコマンドと出力を残し、次回以降の初動を早められるようにする。

---

## 15. 章末問題

1. ディスク不足の調査で、`df -h` の次に確認すべき指標は何か。
2. ドメイン環境でログインだけが失敗するとき、最初に切り分けるべき分岐は何か。
3. LinuxでOOM Killerの痕跡を探すコマンド例を一つ挙げよ。
4. Windowsで、自動起動のはずのサービスが停止しているとき、まず確認すべき情報は何か。
5. 更新プログラム適用後の不具合調査で、最初に保全すべき情報を三つ挙げよ。
6. クラウド環境でOS側のファイアウォール設定を確認しても疎通しない場合、次に確認すべきものは何か。
7. ファイルアクセス拒否の原因調査で、NTFSアクセス許可以外に確認すべきWindows固有の項目は何か。

---

## 16. 解答と解説

1. inode（`df -i`）。容量に余裕があってもinodeが枯渇していると新規ファイルを作成できない。
2. ローカルアカウントでは入れるかどうか。入れる場合はドメイン基盤（DNS、時刻、DCへの到達性、セキュアチャネル）側の問題を疑う。
3. `dmesg -T | grep -i oom` または `journalctl -k | grep -i oom`。
4. SCM（Service Control Manager）関連のイベント、依存サービスの状態、サービスのログオンアカウントのパスワード期限。
5. 例として、適用した更新の一覧、発生しているエラーログ、現在のプロセスや接続状態、直前との設定差分が挙げられる。
6. クラウドプロバイダー側のセキュリティグループやNSGのようなクラウド側フィルタ。
7. 共有フォルダー経由の場合の共有権限、ファイルの暗号化・オフライン属性、マルウェア対策製品による隔離状態。

---

## 17. ハンズオン演習

### 演習13-1 障害カードによる再現訓練

**前提**：ラボ環境の対象ホストで、作業前にスナップショットを取得していること。

**実行**：チームまたは個人で、次の障害を意図的に再現し、手順書どおりに復旧する。

1. `/etc/fstab` に存在しないデバイスを追記し、起動遅延または起動失敗を再現する。
2. ファイアウォールでSSH（22番）またはRDP（3389番）を一時的に遮断し、コンソール経由で復帰する。
3. ディスクを意図的に埋め、アプリケーションの書き込み失敗を再現したうえで清掃する。

**確認**：各回、発生させた症状、使用したコマンド、所要時間を記録する。

**元に戻す**：各演習後、対象ホストをスナップショットへ戻すか、加えた変更を手動で取り消す。

### 演習13-2 総合シナリオ演習

**前提**：付録Bの実務シナリオに沿った環境が構築済みであること。

**実行**：パッチ適用翌日を想定し、「ポータルの応答が遅い、または開かない」という申告に対して、CPU、ディスク、サービス、DNS、権限の順に仮説を検証していく。

**確認**：最終的にどの層に問題があったかを特定し、記録テンプレート（付録B参照）へまとめる。

**元に戻す**：検証のために停止・変更したサービスや設定を元の状態へ戻す。

---

## 18. 本章のまとめ

トラブルシューティングは記憶力の勝負ではなく、手順と保全と層別の切り分けによって成り立つ作業である。

10種類の典型症状はいずれも、影響範囲の特定、状態の保全、直近変更の確認、層別の仮説立てという同じ骨格の上に成り立っている。

付録では、これまでの章で扱ってきたコマンドの対照表、実務シナリオ、用語集を補う。

次: [付録A コマンド対照表](A_command_comparison.md)
