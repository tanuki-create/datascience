# 第10章 Active DirectoryとLinux連携

アカウントを各サーバーで個別に管理すると、入社・異動・退職のたびに設定漏れが発生し、権限が野放図に肥大化していく。

**Active Directory（AD）**は、認証と認可の中心を1か所に寄せ、組織全体で一貫したアカウント管理を実現する仕組みである。

Windows環境が主戦場のディレクトリサービスであるが、Linux側からもこの認証基盤を利用できる。

本章では、AD DS（Active Directory Domain Services）の基本構成要素から、ドメイン参加、グループポリシー、LinuxのAD連携、そして認証障害の切り分け手順までを扱う。

---

## 1. 学習目標

1. ワークグループとドメインの違いを説明できる
2. AD DS、ドメインコントローラー（DC）、ユーザー、グループ、OU（Organizational Unit）の関係を説明できる
3. ADとDNSの関係、KerberosとLDAP（Lightweight Directory Access Protocol）の役割を概説できる
4. グループポリシー（GPO）の基本と、ドメイン参加の手順を実行できる
5. LinuxからADを利用する概要（SSSD、realmd、Winbindなど）を説明できる
6. 認証障害が発生した際の初動切り分けができる

---

## 2. 基本概念

### 2.1 ワークグループとドメイン

| 方式 | 特徴 |
|------|------|
| **ワークグループ** | 各マシンがローカルにアカウント情報を個別に持つ。小規模環境向け |
| **ドメイン** | 中央のディレクトリサービスがアカウントとポリシーを一元管理する |

ワークグループ構成では、10台のサーバーに同じユーザーを作りたい場合、10台それぞれで個別にアカウントを作成・管理する必要があり、パスワード変更や退職時の無効化も個別対応になる。

ドメイン構成では、ディレクトリ上で1度アカウントを作成すれば、そのアカウントをドメインに参加した全マシンで共通して利用できる。

### 2.2 Active Directory Domain Services

**AD DS（Active Directory Domain Services）**は、Windowsドメインの中核となるディレクトリサービスであり、ユーザー、コンピューター、グループ、組織単位などの「オブジェクト」を階層構造で保持する。

このオブジェクトの集合を**ディレクトリ**または**ドメインパーティション**と呼び、LDAPプロトコルを通じて検索・変更が行われる。

AD DSは単なるアカウント台帳ではなく、Kerberos認証局、グループポリシーの配布基盤、DNSサーバーとしての役割も同時に担うことが多い。

### 2.3 ドメインコントローラー

**ドメインコントローラー（DC）**は、AD DSのデータベース（NTDS.dit）を保持し、クライアントからの認証要求やディレクトリ検索要求に応答するサーバーである。

可用性のため、本番環境では通常2台以上のDCを配置し、ディレクトリ情報を相互に複製（レプリケーション）する。

DCが1台しかない構成（シングルDC構成）は、そのDCが停止すると組織全体の認証が機能しなくなるという重大な単一障害点（SPOF: Single Point of Failure）になるため、ラボや検証用の最小構成を除き、本番では避けるべき構成である。

### 2.4 ユーザー、グループ、OU

- **ユーザー**：人間やサービスを表すアカウントであり、認証情報（パスワードやKerberosの鍵）と属性（氏名、部署など）を持つ。
- **グループ**：複数のユーザーやコンピューターをまとめ、権限をまとめて付与するための単位。用途によって「配布グループ」（メール配布用）と「セキュリティグループ」（権限付与用）に分かれる。
- **OU（Organizational Unit、組織単位）**：ユーザーやコンピューターを整理するための入れ物であり、管理権限の委任やGPOの適用単位として使う。

OUとグループはどちらも「まとめる」仕組みだが、OUは主に管理構造とポリシー適用のための箱であり、グループは主に権限付与のための単位という役割分担がある。

### 2.5 DNSとの関係

ADはDNSに強く依存しており、両者は切り離して考えることができない。

ドメインコントローラーは、自身の役割をSRVレコード（`_ldap._tcp.lab.local` や `_kerberos._tcp.lab.local` など）としてDNSに登録し、クライアントはこのSRVレコードを検索することでDCの所在を知る。

このため、DNSが正しく機能していない環境では、実際にはDC自体は正常に稼働していても、クライアントがDCを発見できず、「ADが壊れた」ように見える障害が発生する。

```powershell
nslookup -type=SRV _ldap._tcp.lab.local
Resolve-DnsName -Type SRV _kerberos._tcp.dc._msdcs.lab.local
```

### 2.6 Kerberosと LDAP

- **Kerberos**：チケットに基づくネットワーク認証プロトコルであり、パスワードそのものをネットワーク上でやり取りせず、有効期限付きのチケットで認証を成立させる。時刻の同期が認証の成否に直結する。
- **LDAP（Lightweight Directory Access Protocol）**：ディレクトリに対して検索や変更を行うためのプロトコルであり、ポート389（平文）と636（LDAPS、暗号化）が使われる。

初学者にとっての入り口として、「認証（ログオンの成否そのもの）の主役はKerberos」「検索やアプリケーション連携（ユーザー属性の参照など）の主役はLDAP」という整理が分かりやすい。

Kerberosの認証フローは、大まかに次の順序で進む。

1. クライアントがKDC（鍵配布センター、DC上で動作）へ認証チケット（TGT: Ticket Granting Ticket）を要求する。
2. クライアントはTGTを使い、特定サービスへアクセスするためのサービスチケットを要求する。
3. クライアントはサービスチケットを対象サーバーへ提示し、サーバー側がチケットを検証して認可する。

このチケットには有効期限（既定で数時間程度）が設定されており、クライアントとDCの時刻が一定以上（既定は5分）ずれていると、チケットが無効と判定され認証が失敗する。

### 2.7 グループポリシー

**グループポリシー（GPO: Group Policy Object）**は、ドメインに参加したマシンやユーザーへ、設定を一括配布する仕組みである。

パスワードポリシー、ログオンスクリプト、セキュリティ設定、ソフトウェア配布、ファイアウォール規則など、幅広い設定をGPOで統制できる。

GPOはOUに「リンク」することで適用対象を制御し、複数のGPOが同一OUにリンクされている場合は、リンク順、継承、ブロック設定、セキュリティフィルタリングなどの要素によって最終的な適用結果が決まる。

---

## 3. Linuxでの実現方法

LinuxホストをADのメンバーとして扱う方法にはいくつかの選択肢があり、ディストリビューションやバージョンによって推奨構成が異なる。

| 方式 | 概要 |
|------|------|
| SSSD + realmd | 近年の主要ディストリビューションでの定番に近い構成。`realm join` で簡易にドメイン参加できる |
| Winbind（Samba経由） | Sambaのコンポーネントを使ってドメイン参加する、歴史的に長く使われてきた方式 |
| 直接LDAP照会 | アプリケーションが個別にLDAPバインドしてユーザー情報を参照する（OSログインとは別の層の話） |

### 3.1 SSSDとrealmdによるドメイン参加

**SSSD（System Security Services Daemon）**は、AD/LDAP/Kerberosなどのバックエンドと連携し、ローカルのPAM（Pluggable Authentication Modules）/NSS（Name Service Switch）にユーザー・グループ情報を提供するデーモンである。

**realmd**は、`realm` コマンドを通じて、ドメイン参加に必要な複雑な設定を簡易化するラッパーである。

```bash
# パッケージ名はディストリビューションにより異なる（RHEL系の例）
sudo dnf install -y realmd sssd adcli oddjob oddjob-mkhomedir samba-common-tools krb5-workstation

# ドメインが発見できるか事前確認
sudo realm discover lab.local
```

`realm discover` の想定出力は次のようになる。

```text
lab.local
  type: kerberos
  realm-name: LAB.LOCAL
  domain-name: lab.local
  configured: no
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: adcli
  required-package: samba-common-tools
```

`configured: no` は、まだこのホストがこのドメインに参加していないことを示す。

ドメイン参加を実行する例を示す。

```bash
# 警告: 本番環境での参加は設計レビュー後に行う。事前にDNSと時刻同期を必ず確認する
sudo realm join lab.local -U Administrator
```

参加後の確認例を示す。

```bash
id 'LAB\operator'
getent passwd 'LAB\operator'
realm list
```

Ubuntu系でも `realmd`/`sssd` 系のパッケージが利用できるが、パッケージ名（`sssd-ad`、`sssd-tools`など）が異なる場合があるため、ディストリビューションの公式ドキュメントで確認する。

### 3.2 sudoやSSHでのAD連携

ドメイン参加が完了すると、次のような利用パターンが一般的になる。

1. OSへのログオン認証を、ローカルユーザーではなくADユーザーへ寄せる。
2. `sudo` の権限付与を、ローカルの`/etc/sudoers`ではなくADグループ単位で制御する（`sss_cache`と`sudoers`のSSSD統合、またはLDAPベースのsudoers）。
3. SSHのアクセス制御をADグループで行う（`sshd_config`の`AllowGroups`にADグループを指定するなど）。

```bash
# ADグループに基づくsudo権限の例（/etc/sudoers.d/ad-admins などに記載）
%LAB\\app-admins ALL=(ALL) ALL

# SSHでADグループのみ許可する例（/etc/ssh/sshd_config）
# AllowGroups "LAB\app-admins" localadmins
```

SSSDのキャッシュ関連コマンドも押さえておく。

```bash
sudo sss_cache -E
sudo systemctl restart sssd
journalctl -u sssd -n 100 --no-pager
```

`sss_cache -E` はSSSDのキャッシュを無効化（強制的に再取得させる）するコマンドであり、AD側でユーザー情報やグループメンバーシップを変更したのにLinux側へ反映されない場合に使う。

### 3.3 ドメインからの離脱

```bash
sudo realm leave lab.local
```

離脱後は、ADユーザーでのログオンができなくなるため、離脱前にローカル管理者アカウントでログインできることを確認しておく。

---

## 4. Windowsでの実現方法

### 4.1 ドメインコントローラーの構築（概要）

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
```

```powershell
# 警告: 新規フォレスト/ドメインの作成は、ホスト名・DNS・IPアドレスが確定してから実行する
Install-ADDSForest `
  -DomainName 'lab.local' `
  -InstallDns `
  -DomainNetbiosName 'LAB' `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString -Prompt 'DSRMパスワード')
```

`Install-ADDSForest` は、新しいADフォレスト（最上位の管理境界）とドメインを作成するコマンドレットであり、`-InstallDns` を指定するとDNSサーバー役割も同時に導入される。

`-SafeModeAdministratorPassword` は、**DSRM（Directory Services Restore Mode）**でDCを起動する際に使う特別なパスワードであり、通常のドメインアカウントとは別に厳重に管理する必要がある。

コマンド実行後、サーバーは自動的に再起動し、DCとしての機能が有効になる。

### 4.2 ユーザー・グループ・OUの作成

```powershell
Import-Module ActiveDirectory

New-ADOrganizationalUnit -Name 'Servers' -Path 'DC=lab,DC=local'
New-ADOrganizationalUnit -Name 'Users' -Path 'DC=lab,DC=local'

New-ADUser -Name 'Operator' `
  -SamAccountName 'operator' `
  -Path 'OU=Users,DC=lab,DC=local' `
  -AccountPassword (Read-Host -AsSecureString -Prompt 'パスワード') `
  -Enabled $true

New-ADGroup -Name 'AppAdmins' -GroupScope Global -Path 'OU=Users,DC=lab,DC=local'
Add-ADGroupMember -Identity 'AppAdmins' -Members 'operator'

Get-ADUser operator -Properties *
Get-ADGroupMember -Identity 'AppAdmins'
```

`-GroupScope` には `DomainLocal`、`Global`、`Universal` があり、権限付与の対象範囲（同一ドメイン内か、フォレスト全体かなど）によって使い分ける。

一般的な指針として、「アカウントをGlobalグループへまとめ、Globalグループをリソースに近いDomainLocalグループへ入れ、DomainLocalグループへ実際の権限を付与する」という、いわゆるAGDLP（Account, Global, Domain Local, Permission）というパターンが広く使われる。

### 4.3 メンバーサーバーのドメイン参加

```powershell
# DNSサーバーをDC（192.168.56.10）向けに設定してから実施する
Get-DnsClientServerAddress
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses 192.168.56.10

Add-Computer -DomainName 'lab.local' -Credential (Get-Credential) -Restart
```

`Add-Computer` の実行には、ドメインへコンピューターオブジェクトを追加できる権限を持つアカウント（既定ではDomain Adminsか、委任された権限を持つアカウント）が必要である。

参加後の確認は次のように行う。

```powershell
(Get-CimInstance Win32_ComputerSystem).Domain
Test-ComputerSecureChannel -Verbose
```

### 4.4 グループポリシーの操作

グループポリシーの編集は、**Group Policy Management（GPMC）**コンソールで行うのが一般的である。

```powershell
gpupdate /force
gpresult /r
gpresult /h C:\temp\gpresult.html
```

`gpupdate /force` はクライアント側でGPOの再適用を強制する。

`gpresult /r` は、現在適用されているGPOの概要（Resultant Set of Policy、RSoP）をコマンドラインで表示し、`gpresult /h` はHTML形式のレポートを出力する。

GPOが期待通り適用されない場合は、リンク先のOU、セキュリティフィルタリング、WMIフィルター、継承のブロック設定を順に確認する。

---

## 5. 両OSの比較

| 観点 | Windows中心の視点 | Linux連携時の視点 |
|------|--------------------|---------------------|
| アカウントの正本（マスター） | AD | SSSD等がADを参照するのみで正本は持たない |
| ログオンの仕組み | Winlogon + Kerberos | sshd + PAM + SSSD などの組み合わせ |
| ポリシー配布 | GPO | GPOの多くはWindowsエージェント前提のため一部のみ有効。sudoersやSSH設定は別管理が多い |
| 管理用CLI | AD PowerShellモジュール（`Get-ADUser`など） | `realm`、`id`、`getent`、`sss_cache` |
| 名前解決の前提 | DNSサーバー役割をDC自身が兼務することが多い | 参加前にDNS参照先をDC向けに設定する必要がある |
| 時刻同期の重要度 | Kerberosチケットの検証に直結（既定許容差5分） | 同様にKerberosチケット検証に直結する |

WindowsのGPOは「Windowsのレジストリベースのポリシーエンジン」を前提に設計されているため、Linuxホストへそのまま適用できるわけではなく、Linux側は独自にsudoers、SSH設定、PAM設定などをAD経由で制御する構成を組む必要がある点が、実務上の大きな注意点になる。

---

## 6. コマンド例

### 6.1 ドメインユーザーの一覧・確認

**目的**: 有効なドメインユーザーを確認する。

```powershell
Get-ADUser -Filter 'Enabled -eq $true' | Select-Object -First 10 SamAccountName
```

```bash
getent passwd operator@lab.local 2>/dev/null || getent passwd 'LAB\operator'
id operator@lab.local
```

**権限**: Windowsは対象OUへの参照権限（既定のドメインユーザーでも多くは可能）、Linuxは一般ユーザーで実行可能（SSSD経由でADへ問い合わせる）。

**リスク**: 低（参照のみ）。

### 6.2 セキュアチャネルの確認（Windows）

**目的**: メンバーサーバーとDC間の信頼関係（セキュアチャネル）が健全かを確認する。

```powershell
Test-ComputerSecureChannel -Verbose
nltest /sc_query:lab.local
```

**想定出力**:

```text
VERBOSE: The secure channel between the local computer and the domain lab.local is in good condition.
True
```

`False` が返る場合、コンピューターアカウントのパスワードとDC側の記録が不一致になっている可能性が高く、`Test-ComputerSecureChannel -Repair` での修復や、再度のドメイン参加が必要になる。

**権限**: ローカル管理者。修復には該当コンピューターオブジェクトへの権限を持つドメインアカウントが必要になる場合がある。

**リスク**: 低（確認のみ）。修復操作自体は中リスク。

### 6.3 パスワードポリシーの確認

**目的**: ドメインのパスワードポリシー（複雑性要件、有効期限など）を確認する。

```powershell
Get-ADDefaultDomainPasswordPolicy
```

```bash
# Linux側からLDAP経由で確認する例（ldap-utilsが必要）
ldapsearch -x -H ldap://dc01.lab.local -b 'DC=lab,DC=local' -D 'LAB\operator' -W '(objectClass=domainDNS)' minPwdLength maxPwdAge
```

**権限**: 通常のドメインユーザーでも参照可能。

**リスク**: 低。

### 6.4 グループメンバーの一括変更（Windows）

**目的**: セキュリティグループへ複数ユーザーを一括追加する。

```powershell
# 警告: 誤ったグループへの追加は権限の過剰付与につながる
$members = 'operator','app-svc01','app-svc02'
Add-ADGroupMember -Identity 'AppAdmins' -Members $members
Get-ADGroupMember -Identity 'AppAdmins' | Select-Object Name, SamAccountName
```

**権限**: 対象グループへの書き込み権限を持つアカウント（委任されたグループ管理者、またはDomain Admins）。

**リスク**: 中〜高。過剰な権限付与や、意図しないメンバーの混入がセキュリティリスクに直結する。

---

## 7. 実務上の注意点

1. DCを構築する前に、DNS設計（ゾーン名、DC自身のDNS参照先、逆引きゾーンの要否）を固める。
2. Kerberos認証のため、全メンバーの時刻ずれを既定の許容差（5分）よりも十分に厳しい範囲（例: 1分以内）に保つ運用を目指す。
3. 単一DC構成は避け、最低2台のDCで冗長化する。ラボの最小構成は例外として明示的に認識しておく。
4. `.local` は学習用の慣習的なドメインサフィックスであり、本番では組織が所有する公開ドメインのサブドメインなど、名前空間の衝突が起きない名前を使う。
5. 特権グループ（Domain Admins、Enterprise Adminsなど）のメンバーを最小限にし、定期的な棚卸し（メンバーレビュー）を行う。
6. OU設計は、部署や地理ではなく「管理委任の単位」と「GPO適用の単位」を軸に考えると運用しやすくなる。
7. ドメイン参加・離脱・コンピューターアカウントのリセットは、対象マシンの再起動やサービス断を伴うことがあるため、事前に周知する。

---

## 8. セキュリティ上の注意点

1. Domain Adminsのようなドメイン全体への強い権限を持つアカウントで、日常的なサーバー管理作業を行わない。
2. LDAPS（暗号化されたLDAP、ポート636）を使い、平文LDAP（ポート389での認証情報のやり取り）を段階的に減らす。
3. サービスアカウントのパスワード管理とSPN（Service Principal Name）の適切な設定を行い、Kerberoasting攻撃のような手法への耐性を高める。
4. 古い認証プロトコル（NTLMv1、無防備なNTLM依存の放置）を見直し、可能な限りKerberos優先の構成へ移行する。
5. DCへのRDP（リモートデスクトップ）アクセス経路を最小限の管理端末・管理者に限定する。
6. AD監査ポリシーを有効化し、アカウント作成・グループ変更・DC構成変更などの重要イベントを記録・監視する。
7. LinuxホストのSSSDキャッシュや設定ファイルに、平文の資格情報を残さない。

---

## 9. よくある障害

| 症状 | 典型的な原因 |
|------|--------------|
| ドメイン参加が失敗する | DNSの誤り（DC向けに設定されていない）、ファイアウォールによるポート遮断、資格情報の誤り、時刻ずれ |
| ドメインユーザーでログオンできない | アカウントロックアウト、パスワード期限切れ、時刻ずれ、DCへの到達性喪失、セキュアチャネル不整合 |
| Linuxからのログオン・IDの引き当てのみ失敗する | SSSDのキャッシュ・接続不良、realmの状態異常、PAM設定の誤り、ホームディレクトリ未作成、ADグループ名の形式（`LAB\name`か`name@lab.local`か）の不一致 |
| GPOが適用されない | リンク先OUの誤り、セキュリティフィルタリングの範囲、継承のブロック、`gpupdate`未実行 |
| 特定のDCとだけ通信できない | 個別DCのサービス停止、レプリケーション障害、ネットワーク経路上の障害 |
| コンピューターアカウントのパスワード不整合 | 長期間のオフライン、スナップショットからの巻き戻し、複数回のドメイン再参加 |

---

## 10. 切り分け手順

認証障害の切り分けは、DNS、時刻、ネットワーク到達性、資格情報、セキュアチャネルという順序で確認すると効率的である。

1. **DNS解決を確認する**：`Resolve-DnsName lab.local`（Windows）または `getent hosts lab.local` / `resolvectl query lab.local`（Linux）で、ドメイン名とDC自体が正しく解決できるか確認する。
2. **必要なポートへの到達性を確認する**：ICMPの疎通だけでなく、389（LDAP）、636（LDAPS）、88（Kerberos）、53（DNS）、445（SMB）などの必要ポートへ到達できるか、`Test-NetConnection`や`nc -zv`で確認する。
3. **時刻同期を確認する**：Windowsは `w32tm /query /status`、Linuxは `timedatectl status` で、DCとのずれが許容範囲内かを確認する。
4. **セキュアチャネル・realm状態を確認する**：Windowsは `Test-ComputerSecureChannel`、Linuxは `realm list` とSSSDの状態（`systemctl status sssd`）を確認する。
5. **イベントログ/デーモンログを確認する**：Windowsはセキュリティログの4625/4771等の関連イベントID、Linuxは `journalctl -u sssd` でエラーメッセージを確認する。
6. **アカウント自体の状態を確認する**：アカウントロックアウト、パスワード期限、無効化フラグを `Get-ADUser -Properties LockedOut,PasswordExpired` などで確認する。

```powershell
Get-ADUser operator -Properties LockedOut, PasswordExpired, Enabled, LastLogonDate
w32tm /query /status
Test-ComputerSecureChannel -Verbose
```

```bash
sudo realm list
sudo systemctl status sssd
sudo journalctl -u sssd -n 100 --no-pager
timedatectl status
getent passwd 'LAB\operator'
id 'LAB\operator'
```

Windowsのロックアウトの原因調査には、複数DCでの認証試行が記録される可能性があるため、**Lockout Status ツール**やイベントID 4740（アカウントロックアウト）の記録元DCを特定することが有効である。

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4740} -MaxEvents 20 -ErrorAction SilentlyContinue
```

---

## 11. 章末問題

1. ADがDNSに強く依存する理由を説明せよ。
2. Kerberos認証において時刻同期が重要である理由を説明せよ。
3. OUを使う主な目的を2つ挙げよ。
4. ワークグループ構成の限界を説明せよ。
5. LinuxがADドメインに参加しても、GPOのすべてが有効に機能するとは限らない理由を説明せよ。
6. LDAPとLDAPSの違いを説明せよ。
7. 単一DC構成が本番環境で避けられるべき理由を説明せよ。

---

## 12. 解答と解説

1. クライアントがSRVレコードなどを通じてDCの所在を発見する仕組みになっており、ADの名前空間自体がDNSのドメイン名と結びついているため。DNSが機能しないと、DC自体が正常でもクライアントがDCを発見できない。
2. Kerberosのチケットには有効期間の検証が組み込まれており、クライアントとDCの時刻が既定の許容差（5分）を超えてずれると、チケットが無効と判定され認証が失敗するため。
3. 管理権限の委任単位として使うことと、グループポリシー（GPO）の適用単位として使うこと（加えてオブジェクトの整理という目的もある）。
4. アカウント情報とポリシーが各マシンに分散するため、組織規模が大きくなるほど一貫した認証・認可の管理が難しくなること。
5. GPOの多くはWindowsのレジストリベースのポリシーエンジンを前提に設計されているため、Linux側はこれをそのまま解釈できず、sudoersやSSH、PAM設定など、Linux固有の別の仕組みで制御する必要があるため。
6. LDAPはポート389を使う平文（暗号化されない）プロトコルであり、LDAPSはポート636を使いTLSで暗号化された通信を行う。
7. 唯一のDCが停止すると、組織全体の認証機能が完全に失われる単一障害点（SPOF）になるため。

---

## 13. ハンズオン演習

### 演習10-1 ADフォレストの作成

**前提**: `dc01`（Windows Server 2022）にDNSと時刻同期の設定が完了しており、固定IPアドレス（192.168.56.10）が割り当てられていること。作業前にスナップショットを取得する。

**実行**:

1. `dc01` で `Install-WindowsFeature AD-Domain-Services -IncludeManagementTools` を実行する。
2. `Install-ADDSForest -DomainName 'lab.local' -InstallDns -DomainNetbiosName 'LAB'` を実行し、DSRMパスワードを設定する。
3. 自動再起動後、管理者としてドメインへログオンできることを確認する。

**確認**: `Get-ADDomain` でドメイン情報を表示し、`nslookup -type=SOA lab.local` でDNSのSOAレコード、`nslookup -type=SRV _ldap._tcp.lab.local` でSRVレコードが登録されていることを確認する。

**元に戻す**: 本演習は取り消しが難しい変更（フォレスト作成）を含むため、問題があれば作業前のスナップショットへ復元する。

### 演習10-2 メンバーサーバーのドメイン参加

**前提**: 演習10-1が完了しており、`winapp01` が起動していること。

**実行**:

1. `winapp01` のDNSサーバー設定を `192.168.56.10`（`dc01`）へ変更する。
2. `Add-Computer -DomainName 'lab.local' -Credential (Get-Credential) -Restart` を実行する。
3. 再起動後、ドメインユーザー（例: `LAB\operator`）でログオンできることを確認する。

**確認**: `(Get-CimInstance Win32_ComputerSystem).Domain` が `lab.local` になっていること、`Test-ComputerSecureChannel` が `True` を返すことを確認する。

**元に戻す**: ドメインから離脱する場合は、ローカル管理者でログオンしたうえで `Remove-Computer -UnjoinDomainCredential (Get-Credential) -PassThru -Restart` を実行する。

### 演習10-3 Linuxホストのドメイン参加（任意）

**前提**: `web01`（RHEL系）のDNS参照先が `dc01` へ設定されており、時刻同期が取れていること。事前にスナップショットを取得する。

**実行**:

1. 必要パッケージを導入する：`sudo dnf install -y realmd sssd adcli oddjob oddjob-mkhomedir samba-common-tools krb5-workstation`
2. `sudo realm discover lab.local` でドメインが発見できることを確認する。
3. `sudo realm join lab.local -U Administrator` でドメインへ参加する。
4. `id 'LAB\operator'` でADユーザーのID解決ができることを確認する。

**確認**: `realm list` で参加済みドメインとして `lab.local` が表示されること、`getent passwd 'LAB\operator'` でユーザー情報が取得できることを確認する。

**元に戻す**: `sudo realm leave lab.local` でドメインから離脱し、`realm list` に何も表示されないことを確認する。離脱後にADユーザーでログオンできなくなることを踏まえ、ローカル管理者アカウントでのログイン手段を確保しておく。

失敗した場合は、まずDNS設定（`resolvectl status`）と時刻同期（`timedatectl status`）を疑う。

---

## 14. 本章のまとめ

Active Directoryは組織における認証・認可の中心であり、その足元にはDNSと時刻同期という一見地味だが欠かせない基盤技術がある。

LinuxからもSSSDとrealmdを使えばADの認証基盤へ参加できるが、GPOのような一部の仕組みはWindows前提であるため、Linux固有の代替手段（sudoers、SSH設定、PAM）と組み合わせて運用する必要がある。

次章では、ここまで扱ってきたネットワーク・ソフトウェア・ログ・ディレクトリサービスを踏まえ、両OSのセキュリティ強化について扱う。

次章: [第11章 セキュリティ](11_security.md)
