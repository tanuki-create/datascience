# LinuxとWindowsを体系的に理解するOS解説書

インフラエンジニア向けに、LinuxとWindowsの基本構造、管理方式、コマンド、権限、サービス、ストレージ、ネットワーク、ログ、セキュリティを対比しながら学ぶ解説書である。

目的は、コマンドの暗記ではなく、OS内部で何が起きているかを理解し、両OSの違いを踏まえて基本的な構築・運用・障害対応ができるようになることだ。

## 想定読者

- インフラエンジニアを目指す初学者
- LinuxまたはWindowsの片方しか経験がない人
- サーバー運用の実務知識を身につけたい人
- クラウド上の仮想マシンを管理する人

## 対象環境

| 系統 | 対象 |
|------|------|
| Linux | Red Hat Enterprise Linux（RHEL）系、Ubuntu系、systemdを採用した一般的なLinux |
| Windows | Windows 11、Windows Server 2022以降、PowerShell、Active Directoryの基礎 |

バージョン依存の機能は、その旨を本文中で明記する。

## 読み方

各章は次の順で構成する。

1. 学習目標
2. 基本概念
3. Linuxでの実現方法
4. Windowsでの実現方法
5. 両OSの比較
6. コマンド例
7. 実務上の注意点
8. セキュリティ上の注意点
9. よくある障害と切り分け手順
10. 章末問題と解答
11. ハンズオン演習

LinuxとWindowsを別々に説明したあとで比較する。
GUI操作だけでなく、Linuxではシェル、WindowsではPowerShellによるCLI管理を中心に扱う。

---

## 詳細目次

### 第0部 導入

- [README（本書）](README.md)
  - 目的と想定読者
  - 対象環境
  - 各章の到達目標
  - ハンズオン環境の構成案
  - 実務シナリオの全体像

### 第1章 OSの役割と基本構造

- [01_os_role_and_architecture.md](01_os_role_and_architecture.md)
  - OSの役割
  - カーネルとユーザー空間
  - プロセスとスレッド
  - システムコール
  - デバイスドライバー
  - ファイルシステム
  - LinuxとWindowsのアーキテクチャの違い
  - 起動からログインまでの流れ

### 第2章 インストールと初期設定

- [02_install_and_initial_setup.md](02_install_and_initial_setup.md)
  - Linux / Windows Serverのインストール
  - パーティション設計
  - ホスト名、タイムゾーン、NTP
  - ネットワーク設定と更新プログラム
  - 初期セキュリティ設定
  - 仮想マシンとして構築する際の注意点

### 第3章 ファイルとディレクトリ

- [03_files_and_directories.md](03_files_and_directories.md)
  - Linuxのディレクトリ構造とWindowsのドライブ・フォルダー
  - 絶対パスと相対パス
  - ファイル操作、リンク、隠しファイル、属性
  - 検索、圧縮と展開
  - パス表記の違い

### 第4章 ユーザー、グループ、権限

- [04_users_groups_permissions.md](04_users_groups_permissions.md)
  - LinuxのUID/GID、root、sudo、rwx、ACL
  - WindowsのSID、NTFSアクセス許可、継承、UAC
  - 最小権限の原則と比較

### 第5章 プロセスとサービス

- [05_processes_and_services.md](05_processes_and_services.md)
  - プロセス状態、PID、シグナル、ジョブ管理
  - systemd / systemctl / journalctl
  - Windowsサービス、SCM、PowerShell管理
  - ハングや高負荷の調査

### 第6章 ストレージとファイルシステム

- [06_storage_and_filesystems.md](06_storage_and_filesystems.md)
  - ブロックデバイス、MBR/GPT、ext4/XFS、NTFS/ReFS
  - マウント、fstab、LVM、Storage Spaces
  - inode、クォータ、ディスク拡張と障害調査

### 第7章 ネットワーク管理

- [07_network_management.md](07_network_management.md)
  - IP、サブネット、ゲートウェイ、DNS、ルーティング
  - Linuxのip / NetworkManager、Windowsのipconfig / NetTCPIP
  - ファイアウォールと疎通障害の切り分け

### 第8章 ソフトウェアと更新管理

- [08_software_and_updates.md](08_software_and_updates.md)
  - rpm/dnf/apt/dpkg、リポジトリ、依存関係
  - Windows Update、役割と機能、パッチ管理
  - 再起動判断、ロールバック、検証と本番の分離

### 第9章 ログと監視

- [09_logs_and_monitoring.md](09_logs_and_monitoring.md)
  - journald、/var/log、rsyslog
  - Windowsイベントログ、パフォーマンスカウンター
  - ログローテーション、時刻同期、証跡保全

### 第10章 Active DirectoryとLinux連携

- [10_active_directory_and_linux.md](10_active_directory_and_linux.md)
  - ワークグループとドメイン、AD DS、DC
  - ユーザー・グループ・OU、DNS、Kerberos、LDAP
  - グループポリシー、ドメイン参加、Linux連携、認証障害

### 第11章 セキュリティ

- [11_security.md](11_security.md)
  - ハードニング、パッチ、パスワードポリシー
  - SSH / RDP、公開鍵認証
  - SELinux / AppArmor、Defender、BitLocker、ディスク暗号化
  - 監査ログ、マルウェア対策、管理アカウント分離

### 第12章 バックアップと復旧

- [12_backup_and_recovery.md](12_backup_and_recovery.md)
  - フル・差分・増分、ファイル/システムバックアップ
  - スナップショットとの違い、RPO/RTO
  - Linux例、Windows Server Backup、復旧テストと手順書

### 第13章 トラブルシューティング

- [13_troubleshooting.md](13_troubleshooting.md)
  - 起動不能、ログイン不可、CPU/メモリ/ディスク不足
  - サービス起動失敗、ネットワーク/DNS障害
  - ファイルアクセス拒否、更新後の不具合

### 付録

- [A_command_comparison.md](A_command_comparison.md) … 同一管理目的のLinux/Windowsコマンド対照表
- [B_lab_scenarios.md](B_lab_scenarios.md) … 実務シナリオ（設計から障害対応まで）
- [C_glossary.md](C_glossary.md) … 用語集

---

## 各章の到達目標

| 章 | 到達目標 |
|----|----------|
| 第1章 | カーネル、プロセス、システムコール、ファイルシステムの役割を説明でき、LinuxとWindowsのアーキテクチャ差と起動〜ログインの流れを対比できる |
| 第2章 | 両OSを仮想マシン上にインストールし、ホスト名、時刻、ネットワーク、更新、初期セキュリティをCLI中心で整えられる |
| 第3章 | パス、ファイル操作、リンク、属性、検索、圧縮を両OSで実行し、パス表記と権限表現の違いを説明できる |
| 第4章 | ユーザー・グループ・権限モデルを比較し、最小権限でアカウントとACLを設計・確認できる |
| 第5章 | プロセスとサービスの状態を調査し、起動・停止・自動起動設定と高負荷調査ができる |
| 第6章 | パーティション、ファイルシステム、マウント/ボリューム、容量とinodeを確認し、拡張と障害の初動ができる |
| 第7章 | IP/DNS/ルーティング/ファイアウォールを設定・確認し、疎通障害を層ごとに切り分けられる |
| 第8章 | パッケージ/役割の追加とパッチ適用の流れを理解し、再起動判断とロールバック方針を立てられる |
| 第9章 | ログとメトリクスから障害の手がかりを拾い、時刻同期と証跡保全の重要性を実践できる |
| 第10章 | ADの構成要素と認証の流れを説明し、ドメイン参加と基本的な認証障害の切り分けができる |
| 第11章 | ハードニングの観点で不要サービス、リモート管理、暗号化、監査を点検できる |
| 第12章 | RPO/RTOに沿ったバックアップ方針を立て、復旧テストまで含めて運用できる |
| 第13章 | 典型障害に対し、両OSで調査手順を組み立てて原因候補を絞り込める |

---

## ハンズオン環境の構成案

クラウドでもオンプレのハイパーバイザーでもよい。
本書の演習は、次の仮想マシン構成を前提にする。

### 推奨スペック（合計）

| 項目 | 目安 |
|------|------|
| ホストCPU | 4コア以上（理想は6〜8コア） |
| ホストメモリ | 16 GB以上（理想は24 GB以上） |
| ディスク | 120 GB以上の空き |
| ネットワーク | ホストオンリーまたはNAT＋内部ネットワーク |

### 仮想マシン一覧

| ホスト名 | OS | 役割 | vCPU | メモリ | ディスク | IP例（lab.local） |
|----------|----|------|------|--------|----------|-------------------|
| `dc01` | Windows Server 2022 | Active Directory Domain Services / DNS | 2 | 4 GB | 60 GB | 192.168.56.10 |
| `winapp01` | Windows Server 2022 | アプリケーションサーバー | 2 | 4 GB | 60 GB | 192.168.56.20 |
| `web01` | Rocky Linux 9 または AlmaLinux 9（RHEL系） | Webサーバー（httpd/nginx） | 2 | 2 GB | 40 GB | 192.168.56.30 |
| `web02` | Ubuntu Server 22.04 LTS または 24.04 LTS | Webサーバー比較用（任意） | 2 | 2 GB | 40 GB | 192.168.56.31 |
| `mgmt01` | Windows 11 または Ubuntu Desktop | 管理用クライアント | 2 | 4 GB | 60 GB | 192.168.56.40 |

リソースが不足する場合の最小構成は次のとおりとする。

1. `dc01`
2. `winapp01`
3. `web01`
4. 管理はホストOSからSSH/RDPで行う（`mgmt01`省略可）

### ネットワーク設計

```text
[Host / Hypervisor]
        |
   +----+----+------------------+
   |         |                  |
 lab-net  (192.168.56.0/24)   NAT (任意・外部取得用)
   |
   +-- dc01      192.168.56.10
   +-- winapp01  192.168.56.20
   +-- web01     192.168.56.30
   +-- web02     192.168.56.31  (任意)
   +-- mgmt01    192.168.56.40
```

- ドメイン名：`lab.local`（学習用。本番では公開サフィックスと衝突しない名前を使う）
- DNS：`dc01`を権威DNSとし、メンバーはDNS先を`192.168.56.10`にする
- ゲートウェイ：NAT側がある場合はそのアドレス。隔離ラボなら省略可
- 時刻同期：全ノードでNTPを揃え、AD環境では特に時刻ずれを5分以内に保つ

### ソフトウェア前提

| 用途 | 推奨 |
|------|------|
| ハイパーバイザー | VirtualBox、VMware Workstation/Fusion、Hyper-V、クラウドVMのいずれか |
| Linux ISO | Rocky/Alma 9、Ubuntu Server 22.04/24.04 |
| Windows ISO | Windows Server 2022 Evaluation、Windows 11（検証ライセンスに注意） |
| 管理ツール | OpenSSH、PowerShell 7（任意）、Windows Admin Center（任意） |

### アカウント方針（演習用）

| 種別 | 例 | 用途 |
|------|----|------|
| Linux一般ユーザー | `operator` | 日常操作。sudoは限定付与 |
| Linux root | 直接ログイン禁止を推奨 | 緊急時のみ |
| Windowsローカル管理者 | 初期セットアップ後は使用を最小化 | ドメイン参加前 |
| ドメイン管理者 | `LAB\DomainAdmins` メンバー | AD変更作業のみ |
| サーバー管理者 | 委任されたグループ | 日常のサービス管理 |
| バックアップ実行アカウント | 専用サービスアカウント | バックアップ専用 |

演習でもパスワードをドキュメントに平文で残さない。
各自のパスワードマネージャか、ラボ専用の秘密管理に置く。

### スナップショット方針

各章のハンズオン開始前にスナップショットを取得する。

推奨ラベル例：

- `before-ch02-install`
- `before-ch10-domain-join`
- `before-ch12-backup-test`
- `known-good-baseline`

スナップショットはバックアップではない。
本番相当の復旧演習では、バックアップからの復元を別途実施する。

---

## 実務シナリオの全体像

付録Bで詳細化する。概要のみ示す。

### シナリオ概要

中規模社内向けの社内ポータルを想定する。

1. `dc01`でActive DirectoryとDNSを提供する
2. `winapp01`で業務アプリケーション（IISまたは.NET系サービスを想定）を動かす
3. `web01`で公開用または社内向けWebフロント（nginx/httpd）を動かす
4. 複数管理者が役割分担する（ドメイン管理、サーバー管理、バックアップ担当）
5. 定期バックアップ、監視とログ収集、月次パッチ、障害時復旧を運用する

### フェーズ

| フェーズ | 内容 | 主に参照する章 |
|----------|------|----------------|
| 設計 | 役割分担、IP、ディスク、権限、監視、バックアップ方針 | 1, 2, 4, 6, 7, 11, 12 |
| 構築 | OSインストール、初期設定、AD、アプリ、Web | 2〜8, 10 |
| テスト | 疎通、認証、権限、バックアップ復旧、パッチ試験 | 7, 9, 10, 12 |
| 運用 | 監視、ログ、更新、アカウント管理 | 5, 8, 9, 11 |
| 障害対応 | 起動・ログイン・資源・サービス・ネットワーク障害 | 13 |

---

## コマンド比較の扱い

同一の管理目的について、Linux（シェル）とWindows（PowerShell）の双方で次を併記する。

- コマンドの目的
- 基本構文
- 主要オプション
- 実行例
- 想定される出力と読み方
- 実行に必要な権限
- 誤操作時のリスク

代表的な対照例は付録Aに集約し、各章でも必要箇所で繰り返す。

| 管理目的 | Linuxの例 | Windows（PowerShell）の例 |
|----------|-----------|---------------------------|
| ユーザー一覧 | `getent passwd` / `cat /etc/passwd` | `Get-LocalUser` / `Get-ADUser` |
| プロセス確認 | `ps`, `top`, `htop` | `Get-Process`, Task Manager |
| サービス起動 | `systemctl start` | `Start-Service` |
| IP確認 | `ip addr` | `Get-NetIPAddress`, `ipconfig` |
| 待ち受けポート | `ss -tulpn` | `Get-NetTCPConnection` |
| ログ検索 | `journalctl`, `grep` | `Get-WinEvent` |
| ディスク使用量 | `df -h`, `du -sh` | `Get-PSDrive`, `Get-Volume` |
| 権限変更 | `chmod`, `chown`, `setfacl` | `icacls`, `Set-Acl` |

---

## 危険操作についての共通注意

次の操作はデータ消失や接続断につながる。

- ディスクの初期化、パーティション削除、フォーマット
- ルートやシステムディレクトリの再帰削除
- ファイアウォールの一括遮断（リモート管理中）
- ドメインコントローラーの降格や強制削除
- 本番での検証未実施のパッチ一括適用

手順には、前提条件、実行内容、確認方法、元に戻す方法を記載する。
警告付きのコマンドは、ラボのスナップショット取得後に実行すること。

---

## 執筆・利用上の注意

- Evaluation版や検証ライセンスの利用条件を守ること
- 本番ドメイン名、本番IP、本番パスワードを演習に使わないこと
- クラウドVMではセキュリティグループやNSGもOSファイアウォールと合わせて確認すること
- 本書の設定値は学習用であり、組織の標準にそのまま適用しないこと

## 収録状況（完了）

要求仕様どおり、全章・付録の執筆は完了している。
追加の未執筆ファイルはない。

| 区分 | 状態 | 備考 |
|------|------|------|
| 第1章〜第13章 | 完了 | 各章に学習目標・概念・Linux・Windows・比較・コマンド・注意・障害・切り分け・問題・解答・ハンズオン |
| 付録A | 完了 | 同一管理目的の Linux / PowerShell 対照 |
| 付録B | 完了 | 設計→構築→テスト→運用→障害対応の通しシナリオ |
| 付録C | 完了 | 用語集 |
| 合本 | 完了 | [COMPLETE_BOOK.md](COMPLETE_BOOK.md)（約10,000行） |
| 相互リンク | 確認済み | 章間リンクの欠落なし |

### ファイルインベントリ

| ファイル | 内容 |
|----------|------|
| [README.md](README.md) | 本書（目次・到達目標・ラボ構成） |
| [01_os_role_and_architecture.md](01_os_role_and_architecture.md) | 第1章 |
| [02_install_and_initial_setup.md](02_install_and_initial_setup.md) | 第2章 |
| [03_files_and_directories.md](03_files_and_directories.md) | 第3章 |
| [04_users_groups_permissions.md](04_users_groups_permissions.md) | 第4章 |
| [05_processes_and_services.md](05_processes_and_services.md) | 第5章 |
| [06_storage_and_filesystems.md](06_storage_and_filesystems.md) | 第6章 |
| [07_network_management.md](07_network_management.md) | 第7章 |
| [08_software_and_updates.md](08_software_and_updates.md) | 第8章 |
| [09_logs_and_monitoring.md](09_logs_and_monitoring.md) | 第9章 |
| [10_active_directory_and_linux.md](10_active_directory_and_linux.md) | 第10章 |
| [11_security.md](11_security.md) | 第11章 |
| [12_backup_and_recovery.md](12_backup_and_recovery.md) | 第12章 |
| [13_troubleshooting.md](13_troubleshooting.md) | 第13章 |
| [A_command_comparison.md](A_command_comparison.md) | 付録A |
| [B_lab_scenarios.md](B_lab_scenarios.md) | 付録B |
| [C_glossary.md](C_glossary.md) | 付録C |
| [COMPLETE_BOOK.md](COMPLETE_BOOK.md) | 全章合本 |

### 推奨読み順

1. 本READMEでラボ構成を確認する
2. [第1章](01_os_role_and_architecture.md) から第13章まで順に読む
3. 通し演習は [付録B](B_lab_scenarios.md)
4. 日々の対照は [付録A](A_command_comparison.md)、用語は [付録C](C_glossary.md)

次は [第1章 OSの役割と基本構造](01_os_role_and_architecture.md) から読み進める。
