# 付録B 実務シナリオ

社内向けポータルシステムを想定した、設計から障害対応までの通しシナリオである。

README記載のVM構成（`dc01`、`winapp01`、`web01`）を前提に、Linux Webサーバー、Windowsアプリケーションサーバー、Active Directory、DNS、複数管理者、定期バックアップ、監視とログ収集、パッチ適用、障害復旧を一連の流れとして扱う。

各フェーズには、前提条件、実行内容、確認方法、元に戻す方法を含める。
章番号は本編への参照である。

---

## B.1 シナリオ概要

| 項目 | 内容 |
|------|------|
| システム | 社内ポータル（Webフロント + アプリケーション + AD認証） |
| 利用者 | 社員（ドメインユーザー） |
| 管理者 | ドメイン管理、サーバー管理、バックアップ担当（役割分離） |
| 非機能要件 | 平日日中の可用性、日次バックアップ（RPO 24時間）、復旧目標RTO 4時間、月次パッチ |

構成：

```text
[利用者 / mgmt01]
        |
        v
   web01 (Linux Web: nginx または httpd)
        |
        v
   winapp01 (Windows アプリ / IIS 想定)
        |
        v
   dc01 (AD DS + DNS)
```

| ホスト | OS | 役割 | IP例 |
|--------|-----|------|------|
| `dc01` | Windows Server 2022 | AD DS / DNS | 192.168.56.10 |
| `winapp01` | Windows Server 2022 | アプリケーション | 192.168.56.20 |
| `web01` | Rocky/Alma 9 または Ubuntu 22.04/24.04 | Web | 192.168.56.30 |
| `mgmt01` | Windows 11 または Ubuntu Desktop（任意） | 管理クライアント | 192.168.56.40 |

ドメイン名は学習用に `lab.local` とする。
本番では公開サフィックスと衝突しない名前空間を使う。

---

## B.2 設計フェーズ

### 前提条件

- READMEのハンズオン構成案を読んでいる
- 設計成果物を置く場所（リポジトリ外の作業メモでも可）がある

### 実行内容

次を文書化する。

1. **命名とアドレス**  
   ホスト名、`lab.local`、Aレコード、逆引きの要否
2. **ディスク**  
   OSとデータの分離、バックアップ先ボリューム、暗号化の要否（第6章、第11章）
3. **ネットワーク**  
   管理用とサービス用の通信経路、開放ポート一覧（22/3389/53/80/443/アプリポート）
4. **権限**  
   Domain Admins最小化、`AppAdmins`、`BackupOperators`、Linuxの `sudo` グループ
5. **バックアップ**  
   RPO 24時間、RTO 4時間、世代数、オフホスト保管
6. **監視**  
   CPU、メモリ、ディスク、サービス死活、HTTP応答、バックアップ成否
7. **パッチ**  
   メンテ窓、適用順（検証 → アプリ → Web。DCは別枠で慎重に）、切り戻し期限

### 確認方法

- 構成図、アドレス表、アカウント表、バックアップ表、監視項目表の5点が揃う
- IPとホスト名の重複がない

### 元に戻す方法

- 文書のみのためシステム変更はない

参照章：1, 2, 4, 6, 7, 11, 12

---

## B.3 構築フェーズ

### 前提条件

- スナップショット名 `before-build` を取得済み
- 評価ライセンス条件を確認済み
- コンソールアクセスを確保済み（遠隔締め出し対策）

### 実行内容

#### B.3.1 dc01

```powershell
Rename-Computer -NewName 'dc01' -Restart
# 再起動後
New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 192.168.56.10 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses '127.0.0.1'
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
# 警告: ドメイン新規作成はホスト名・IP・DNS確定後に行う
Install-ADDSForest -DomainName 'lab.local' -InstallDns -Force
```

再起動後：

```powershell
Get-ADDomain
Get-Service NTDS, DNS, ADWS | Format-Table Name, Status, StartType
w32tm /query /status
```

#### B.3.2 ディレクトリオブジェクト

```powershell
Import-Module ActiveDirectory
New-ADOrganizationalUnit -Name 'Servers' -Path 'DC=lab,DC=local'
New-ADOrganizationalUnit -Name 'Users' -Path 'DC=lab,DC=local'
New-ADOrganizationalUnit -Name 'Groups' -Path 'DC=lab,DC=local'
New-ADGroup -Name 'AppAdmins' -GroupScope Global -Path 'OU=Groups,DC=lab,DC=local'
New-ADGroup -Name 'BackupOperatorsLab' -GroupScope Global -Path 'OU=Groups,DC=lab,DC=local'
New-ADUser -Name 'App Operator' -SamAccountName 'appop' `
  -Path 'OU=Users,DC=lab,DC=local' -AccountPassword (Read-Host -AsSecureString) -Enabled $true
Add-ADGroupMember 'AppAdmins' -Members 'appop'
```

#### B.3.3 winapp01

```powershell
Rename-Computer -NewName 'winapp01'
# DNSをDCへ
Set-DnsClientServerAddress -InterfaceAlias 'Ethernet' -ServerAddresses '192.168.56.10'
New-NetIPAddress -InterfaceAlias 'Ethernet' -IPAddress 192.168.56.20 -PrefixLength 24
Add-Computer -DomainName 'lab.local' -Credential (Get-Credential) -Restart
```

再起動後：

```powershell
Install-WindowsFeature Web-Server -IncludeManagementTools
Get-Service W3SVC
New-NetFirewallRule -DisplayName 'Allow HTTP Lab' -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

ローカル管理者へ `AppAdmins` を追加する（必要最小限）。

#### B.3.4 web01

```bash
sudo hostnamectl set-hostname web01
sudo timedatectl set-timezone Asia/Tokyo
# NetworkManager または netplan で 192.168.56.30/24、DNS 192.168.56.10
ip -br addr
getent hosts dc01.lab.local
```

Web導入例（RHEL系）：

```bash
sudo dnf install -y nginx
echo '<h1>web01 lab</h1>' | sudo tee /usr/share/nginx/html/index.html
sudo systemctl enable --now nginx
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
curl -I http://127.0.0.1/
```

Ubuntu系は `apt install nginx` と `ufw allow OpenSSH` / `ufw allow http` に読み替える。

任意でAD参加：

```bash
sudo realm discover lab.local
sudo realm join lab.local -U Administrator
id appop@lab.local
```

#### B.3.5 複数管理者の分離

| 役割 | 例 | 権限の目安 |
|------|----|------------|
| ドメイン管理 | 極少数の Domain Admins | AD変更のみ |
| サーバー管理 | AppAdmins | winapp01 / web01 の日常運用 |
| バックアップ | BackupOperatorsLab | バックアップ実行と読み取り |

Linuxでは `sudo` をグループ単位で限定する。

```bash
# 例: /etc/sudoers.d/appadmins （visudo -f で編集）
# %appadmins ALL=(ALL) /bin/systemctl restart nginx, /bin/journalctl
```

### 確認方法

```powershell
Resolve-DnsName web01.lab.local
Resolve-DnsName winapp01.lab.local
Test-NetConnection 192.168.56.30 -Port 80
Test-NetConnection 192.168.56.20 -Port 80
```

```bash
curl -I http://192.168.56.30/
dig @192.168.56.10 winapp01.lab.local +short
```

### 元に戻す方法

- 失敗時は `before-build` へ戻す
- 成功後は `after-build` スナップショットを取る

参照章：2, 3, 4, 5, 7, 8, 10

---

## B.4 テストフェーズ

### 前提条件

- `after-build` 時点で3台が起動している

### 実行内容

| 試験 | 手順の要点 | 合格基準 |
|------|------------|----------|
| 疎通 | IPと必要ポート | 22/3389/53/80等が設計どおり |
| 名前解決 | 相互の A レコード | 名前で到達できる |
| 認証 | ドメインユーザーで winapp01 ログオン | 成功。失敗は監査に残る |
| 権限 | 一般ユーザーで管理ディレクトリへ書込 | Access denied / Permission denied |
| サービス自動起動 | 各ホストを再起動 | nginx/W3SVC/NTDS/DNS が戻る |
| バックアップ | 取得→別名復元 | 内容一致、所要時間を記録 |
| パッチ試験 | 検証適用→スモークテスト | 主要応答が復帰 |

バックアップ試験（例）：

```bash
sudo mkdir -p /backup/web01
sudo tar -czf /backup/web01/html-$(date +%F).tgz -C /usr/share/nginx html
sudo mkdir -p /tmp/restore-test
sudo tar -xzf /backup/web01/html-$(date +%F).tgz -C /tmp/restore-test
diff -r /usr/share/nginx/html /tmp/restore-test/html
```

```powershell
Install-WindowsFeature Windows-Server-Backup -IncludeManagementTools
# 別ボリュームへバックアップ（ラボのディスク構成に合わせる）
# 復元は別名フォルダーへ
```

### 確認方法

- 試験記録（日時、実施者、合否、不合格原因）を残す

### 元に戻す方法

- 試験で緩めた権限・FW・停止サービスを元に戻す
- 不合格は設計/構築へフィードバック

参照章：7, 9, 10, 12

---

## B.5 運用フェーズ

### 前提条件

- テスト合格
- 運用チェックリストがある

### 実行内容

#### 日常点検（日次）

| 項目 | Linux例 | Windows例 |
|------|---------|-----------|
| ディスク | `df -h` / `df -i` | `Get-Volume` |
| サービス | `systemctl is-active nginx` | `Get-Service W3SVC, NTDS, DNS` |
| エラーログ | `journalctl -p err --since today` | `Get-WinEvent` Error |
| バックアップ成否 | ログと成果物サイズ | `Get-WBJob` / バックアップ履歴 |
| 時刻 | `timedatectl` | `w32tm /query /status` |

#### 定期バックアップ（日次）

1. web01のコンテンツと `/etc` の必要部分
2. winapp01のアプリデータとシステム状態（方針に応じて）
3. オフホストへ複製
4. 週次でファイル1つの復元ドライラン

#### 監視とログ

- 最低: CPU、メモリ、ディスク、死活、HTTP
- 可能なら journal / イベントを外部保管（証跡保全）

#### 月次パッチ

1. メンテ告知と切り戻し期限の宣言
2. 検証機へ先行
3. スナップショット取得
4. 適用順の例: winapp01 → web01。dc01は別窓で慎重に
5. スモークテスト（HTTP、ログオン、DNS）
6. 問題時は期限までに切り戻し

```bash
sudo dnf check-update || sudo apt update
# 適用はメンテ窓内
```

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

### 確認方法

- 点検記録とバックアップ成功が台帳と一致する
- パッチ後のサービス状態が Running

### 元に戻す方法

- パッチ失敗時は第8章・第13章の切り戻し
- ラボはスナップショット

参照章：5, 8, 9, 11, 12

---

## B.6 障害対応フェーズ

### 前提条件

- 監視または利用者申告で異常を検知できる
- コンソールアクセス手段がある

### 事象例

月次パッチ翌営業日、「ポータルが開かない／遅い」と申告。

### 実行内容（標準フロー）

1. **保全**（再起動より先）  
   時刻、ホスト、`curl -I`、サービス状態、Listenポート、ディスク、直近 Error ログ、直近変更
2. **影響範囲**  
   web01のみか、winapp01か、認証（dc01）か、ネットワーク全体か
3. **仮説を一つずつ棄却**

| 仮説 | Linux確認 | Windows確認 |
|------|-----------|-------------|
| DNS | `getent hosts` / `dig` | `Resolve-DnsName` |
| サービス停止 | `systemctl status` | `Get-Service` |
| ポート/FW | `ss -tulpn`, firewall-cmd | `Get-NetTCPConnection`, FW規則 |
| CPU/メモリ/ディスク | `ps`, `free`, `df`/`df -i` | `Get-Process`, `Get-Volume` |
| 権限 | `namei -l`, `getfacl` | `icacls`, `whoami` |
| 更新回帰 | dnf/apt履歴 | `Get-HotFix` |

4. **応急**  
   サービス再起動、ディスク清掃、FW誤設定の戻し、問題パッチ/カーネルの切り戻し
5. **恒久**  
   監視追加、手順書更新、再発条件の除去

### 確認方法

- 利用者視点の回復（HTTP 200、ログイン）
- 内部指標（サービス、リソース）が平常範囲

### 元に戻す方法

- 応急で広げた穴（Any許可、777等）は恒久対応後に必ず閉じる

### 記録テンプレート

```text
申告時刻:
検知手段:
影響範囲:
直近の変更:
仮説と棄却結果:
応急処置:
根本原因:
再発防止:
復旧完了時刻:
所要時間（RTO比較）:
```

参照章：13（主）, 5, 7, 8, 9

---

## B.7 エンドツーエンド演習の進め方

1. B.2の設計表を埋める（30〜60分）
2. B.3を実施し `after-build` を取る
3. B.4の表をすべて実施する
4. B.5の日次点検を3日分シミュレーション記録する
5. B.6を意図的に1つ再現して復旧する（例: nginx停止、DNS誤り、ディスク圧迫）

所要の目安（個人ラボ）: 構築半日〜1日、テスト半日、障害演習1〜2時間。

---

## B.8 フェーズと参照章

| フェーズ | 章 |
|----------|----|
| 設計 | 1, 2, 4, 6, 7, 11, 12 |
| 構築 | 2〜8, 10 |
| テスト | 7, 9, 10, 12 |
| 運用 | 5, 8, 9, 11, 12 |
| 障害対応 | 13 |

---

## B.9 ハンズオン合格チェックリスト

- [ ] 3台が名前で相互解決できる
- [ ] ドメインユーザーで `winapp01` にログオンできる
- [ ] `web01` が HTTP で応答する
- [ ] 管理者役割（ドメイン / サーバー / バックアップ）がグループに反映されている
- [ ] バックアップ1回成功 + 復元試験済み（所要時間記録）
- [ ] パッチ手順書（切り戻し含む）がある
- [ ] 監視項目（CPU、メモリ、ディスク、死活、HTTP）を確認できる
- [ ] 障害1件を手順どおり復旧し、記録テンプレートを埋めた
- [ ] スナップショット `after-build` と `known-good-baseline` がある

次: [付録C 用語集](C_glossary.md)
