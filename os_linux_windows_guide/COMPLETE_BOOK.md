# LinuxとWindowsを体系的に理解するOS解説書（合本）

本書は分冊ファイルを結合した合本である。最新の編集は各分冊を正とする。

---


<!-- source: README.md -->

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

### 推奨読み順

1. 本READMEでラボ構成を確認する
2. [第1章](01_os_role_and_architecture.md) から第13章まで順に読む
3. 通し演習は [付録B](B_lab_scenarios.md)
4. 日々の対照は [付録A](A_command_comparison.md)、用語は [付録C](C_glossary.md)

次は [第1章 OSの役割と基本構造](01_os_role_and_architecture.md) から読み進める。


---


<!-- source: 01_os_role_and_architecture.md -->

# 第1章 OSの役割と基本構造

サーバー障害の連絡が来たとき、最初に見る画面はログでもメトリクスでもなく、「そのマシンがまだOSとして動いているか」であることが多い。
アプリケーションが遅いのか、ディスクが満杯なのか、認証が落ちているのかを切り分ける前に、OSがハードウェアとプロセスをどう束ねているかを頭に置いておく必要がある。

本章では、LinuxとWindowsを横断して使うための共通語彙を作る。
カーネル、プロセス、システムコール、ファイルシステム、起動シーケンスは、以後のすべての章の土台になる。

---

## 1. 学習目標

本章を終えると、次ができるようになる。

1. OSの役割を、ハードウェア抽象化、資源管理、隔離、サービスの提供という観点で説明できる
2. カーネル空間とユーザー空間の境界、システムコールの意味を説明できる
3. プロセスとスレッドの違い、PIDの役割を両OSで確認できる
4. ファイルシステムが「名前」と「実体」をどう結ぶかを概説できる
5. Linux（モノリシック寄りの設計とユーザー空間ツール群）とWindows（NTカーネルと実行サブシステム）の違いを対比できる
6. 電源投入からログイン可能になるまでの流れを、両OSで大まかに追える

---

## 2. 基本概念

### 2.1 OSの役割

**オペレーティングシステム（Operating System, OS）**は、ハードウェアとアプリケーションの間に立ち、次を担うソフトウェアの集まりである。

| 役割 | 内容 | 運用での見え方 |
|------|------|----------------|
| ハードウェア抽象化 | CPU、メモリ、ディスク、NICを共通の操作に落とす | 機種が違っても同じコマンドで管理できる |
| 資源管理 | CPU時間、メモリ、I/O帯域を配分する | 高負荷時にどのプロセスが奪っているかを見る |
| 隔離と保護 | プロセス同士、ユーザー同士の干渉を防ぐ | 権限エラー、アクセス拒否として表面化する |
| 共通サービス | ファイル、ネットワーク、時刻、認証の基盤を提供する | アプリはOSのAPIやシステムコール経由で使う |

OSを「アプリを動かす箱」とだけ捉えると、障害対応で手が止まる。
実際には、アプリの異常の多くは、権限、ディスク、ネットワーク、時刻、サービスの状態といったOS側の前提条件の崩れとして現れる。

### 2.2 カーネルとユーザー空間

**カーネル（kernel）**は、OSの中核であり、特権モードで動作する。
メモリ保護、プロセス切替、デバイスへの直接アクセス、割り込み処理はカーネルが担う。

**ユーザー空間（user space）**は、一般のアプリケーションと多くの管理ツールが動く領域である。
ここからハードウェアへ直接触ることはできず、カーネルが公開する窓口を通す。

この境界がある理由は単純で、誤ったアプリや悪意あるコードが、他プロセスのメモリやディスクを好き勝手に壊せないようにするためだ。
運用者が触るシェルやPowerShellも、基本的にはユーザー空間のプログラムである。
管理者権限で動かしても、「カーネルそのもの」になるわけではない。

```text
+--------------------------------------+
| ユーザー空間                          |
|  bash / pwsh / アプリ / 管理ツール     |
+------------------+-------------------+
                   | システムコール / Win32 API など
+------------------+-------------------+
| カーネル空間                          |
|  スケジューラ / メモリ管理 / ドライバ  |
+------------------+-------------------+
| ハードウェア（CPU, RAM, Disk, NIC）   |
+--------------------------------------+
```

### 2.3 プロセス

**プロセス（process）**は、実行中のプログラムの実体である。
OSから見ると、次をまとめた管理単位だ。

- 実行中の機械語と命令ポインタ
- 専用の仮想アドレス空間（メモリ空間）
- 開いているファイルやソケットなどのハンドル（Linuxではファイルディスクリプタ）
- セキュリティ文脈（どのユーザーとして動いているか）
- プロセス識別子（**PID**: Process ID）

同じ実行ファイルを二つ起動すれば、プロセスは二つになる。
設定ファイルを読み間違えた「怪しい挙動」を追うときは、バイナリ名ではなくPID単位で見る。

### 2.4 スレッド

**スレッド（thread）**は、プロセス内の実行の流れである。
一つのプロセスが複数スレッドを持てば、同じアドレス空間を共有しながら並列に処理できる。

| 項目 | プロセス | スレッド |
|------|----------|----------|
| アドレス空間 | 基本的に独立 | 同一プロセス内で共有 |
| 生成コスト | 相対的に高い | 相対的に低い |
| 障害の影響 | 他プロセスへ直接は波及しにくい | 同一プロセスの他スレッドへ影響しやすい |
| 運用での見方 | PIDで追跡 | スレッド数やCPU時間の内訳で見る |

Webサーバーが高CPUになるとき、「プロセスが一つでもスレッドが暴れている」ことは珍しくない。
逆に、ワーカープロセスを複数起動する設計では、PIDが並ぶこと自体が正常である。

### 2.5 システムコール

**システムコール（system call）**は、ユーザー空間からカーネルへ依頼するための公式な入口である。
ファイルを開く、プロセスを作る、ネットワークへ送信する、といった操作は、最終的にシステムコール経由でカーネルに渡る。

ライブラリやAPIは、その手前の便利な包み紙だ。

- Linuxでは、Cライブラリ（glibcなど）が `open` や `read` を提供し、内部でシステムコールを発行する
- Windowsでは、Win32 APIや .NET のAPIが同様の役割を果たし、最終的にNTカーネルのサービスへ到達する

運用者がシステムコールを直接叩くことは少ない。
それでも、「権限エラーはカーネルが拒否した結果」「ディスク満杯は書き込みシステムコールの失敗」という見方を持つと、ログの意味が読みやすくなる。

### 2.6 デバイスドライバー

**デバイスドライバー（device driver）**は、特定のハードウェアや仮想デバイスをカーネルが扱うためのソフトウェアだ。
NIC、ディスクコントローラー、GPU、ハイパーバイザーが提供する仮想ディスクなどが対象になる。

ドライバーに不具合があると、次のような症状が出る。

- 特定デバイスだけ認識しない
- 高負荷時にカーネルパニックやブルースクリーン（Bug Check）へ進む
- 更新後にだけネットワークやストレージが消える

仮想マシンでは、ゲストOSに「仮想化対応ドライバー」（VirtIO、VMware Tools、Hyper-V統合サービスなど）が入っているかが性能と安定性を左右する。

### 2.7 ファイルシステム

**ファイルシステム（file system）**は、ディスク上の領域に「名前付きのファイルとディレクトリ」という構造を与える仕組みである。
OSは、パスという人間向けの名前を、ブロック番号やレコードといった物理的な配置へ変換する。

ファイルシステムが扱う主な情報は次のとおりだ。

- ファイル本体のデータ
- メタデータ（所有者、権限、サイズ、時刻、リンク情報）
- ディレクトリ（名前から実体への対応表）
- 空き領域の管理情報

Linuxではext4やXFS、WindowsではNTFSやReFSが代表例である。
詳細は第6章で扱う。
ここでは、「パスが見える＝その裏にファイルシステムとマウント（またはドライブレター）がある」と押さえる。

### 2.8 ユーザーモードと特権モード

CPUには、命令の実行権限を分けるモードがある。
おおまかには次の二層で考えてよい。

- **特権モード（kernel mode）**：ハードウェア制御や保護機能を含む命令を実行できる
- **ユーザーモード（user mode）**：制限された命令のみ。権限外の操作はトラップされる

プロセスがシステムコールを発行すると、CPUは一時的に特権モードへ移り、カーネルが処理したあとユーザーモードへ戻る。
この往復は性能上も重要で、過剰なシステムコールはI/O待ちとは別にCPUを消費する。

---

## 3. Linuxでの実現方法

### 3.1 アーキテクチャの見取り図

Linuxは、Linuxカーネルと、その上のユーザー空間（GNUツール、systemd、シェル、パッケージなど）を合わせて一つのOS環境として使う。
厳密には「Linux」はカーネル名だが、運用の現場ではディストリビューション全体をLinuxと呼ぶ。

本書が対象とする現代的なサーバーLinuxは、次を前提にする。

- カーネル：Linux
- init系：systemd
- パッケージ：RHEL系はdnf/rpm、Ubuntu系はapt/dpkg
- シェル：bashを標準として扱う

カーネルはデバイスドライバやファイルシステム実装の多くをカーネル空間に持つ、いわゆるモノリシック寄りの設計である。
モジュール（`.ko`）としてドライバを後から読み込む仕組みもあり、すべてを一つの巨大バイナリに固定するわけではない。

### 3.2 プロセスモデル

Linuxでは、新しいプロセスは多くの場合 `fork`（または `clone`）で親の複製を作り、続けて `exec` 系で別プログラムへ切り替える。
このため、親子関係（PPID）が明確で、セッションやプロセスグループといった単位も管理に使われる。

確認の基本は次だ。

```bash
ps -ef
```

主な列の読み方は次のとおりである。

| 列 | 意味 |
|----|------|
| UID | 実行ユーザー |
| PID | プロセスID |
| PPID | 親プロセスID |
| C | CPU使用の目安 |
| STIME | 開始時刻 |
| TTY | 制御端末。デーモンは `?` になりやすい |
| TIME | 累積CPU時間 |
| CMD | コマンド行 |

### 3.3 システムコールと観測

トレースしたいときは `strace` を使う。
権限やファイル不存在の調査で、「どのパスを開こうとして失敗したか」が直接見える。

```bash
strace -e openat,connect -p <PID>
```

本番で長時間付けると負荷と情報漏洩のリスクがある。
短時間、対象を絞って使う。

### 3.4 ファイルシステムの見え方

Linuxでは、すべてが一つのディレクトリツリーの下に見える。
ディスクを追加しても、ドライブレターではなく、既存ツリー上のマウントポイントに接続する。

```bash
findmnt
df -hT
```

`/` がルートであり、`/etc`、`/var`、`/home`、`/proc`、`/sys` などが続く。
`/proc` と `/sys` はディスク上の通常ファイルではなく、カーネルが提供する仮想ファイルシステムである。

### 3.5 起動からログインまで（systemd系）

電源投入からの大まかな流れは次のとおりだ。

1. ファームウェア（BIOS/UEFI）が起動デバイスを選ぶ
2. ブートローダー（GRUB2など）がカーネルとinitramfsを読み込む
3. カーネルが初期化し、必要ならinitramfs内でルートファイルシステムを準備する
4. 実ルートへ切り替わり、PID 1として `systemd` が起動する
5. systemdが依存関係に従い、ローカルファイルシステム、ネットワーク、sshdなどのユニットを起こす
6. gettyやディスプレイマネージャ、SSH経由でログイン可能になる

確認例：

```bash
systemctl list-units --type=service --state=running
who -b
uptime
```

---

## 4. Windowsでの実現方法

### 4.1 アーキテクチャの見取り図

Windows（現代のサーバー/クライアント）は、**Windows NT**系アーキテクチャを基盤にする。
中核はNTカーネルとエグゼクティブであり、その上にWin32サブシステムなどの環境サブシステムが載る。

運用で意識する層は次だ。

| 層 | 例 | 役割 |
|----|----|------|
| ユーザーモードアプリ | 業務アプリ、PowerShell、MMC | 実際の作業 |
| サブシステム / API | Win32、.NET | アプリからOS機能への窓口 |
| カーネルモード | NTOS、ドライバ | 資源管理とデバイス制御 |
| ハードウェア抽象化 | HAL | 機種差の吸収 |

Linuxの「すべてがファイル」に対し、Windowsはオブジェクトマネージャ配下のオブジェクト（プロセス、ファイル、レジストリキー、デバイスなど）として資源を扱うイメージが近い。

### 4.2 プロセスモデル

Windowsでも実行単位の基本はプロセスとスレッドである。
PIDに相当するプロセスIDがあり、PowerShellから確認できる。

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
```

サービスとして動くプロセスは、Session 0で動くなど、対話セッションとは分離される。
タスクマネージャーの「詳細」タブや `Get-CimInstance Win32_Process` で、親プロセスやコマンドラインを追う。

```powershell
Get-CimInstance Win32_Process |
  Select-Object ProcessId, ParentProcessId, Name, CommandLine |
  Format-Table -AutoSize
```

### 4.3 APIとカーネルへの到達

アプリは通常、Win32 APIや .NET APIを呼ぶ。
管理者であっても、任意のカーネルメモリを直接書き換えることはできない。
権限昇格（UAC）、アクセストークン、特権（Se系）が、どこまでできるかを決める。

トラブル時に「管理者で開いたPowerShellか」「通常ユーザーか」で見える世界が変わるのは、このアクセストークンの違いによる。

### 4.4 ファイルシステムの見え方

Windowsでは、ボリュームにドライブレター（`C:` など）やマウントポイントを割り当てる。
NTFSが標準的で、権限はACL（Access Control List）で表現する。

```powershell
Get-Volume
Get-PSDrive -PSProvider FileSystem
```

レジストリも重要な設定ストアだが、本章では「カーネルとユーザー空間の設定の一部がファイル以外にも存在する」点だけ押さえる。

### 4.5 起動からログインまで

Windows Server / Windows 11の大まかな流れは次のとおりだ。

1. UEFIがブートマネージャを起動する
2. Windows Boot ManagerがBCD（Boot Configuration Data）を参照し、Windowsを読み込む
3. winload などがカーネル（ntoskrnl）と必要なドライバを載せる
4. カーネル初期化の後、**Session Manager（smss.exe）**が動く
5. **Windowsサブシステム**や**Service Control Manager（services.exe）**がサービスを起動する
6. **Winlogon**と**LogonUI**がログイン画面を出し、資格情報を受け取る
7. ドメイン参加済みなら、Active Directoryへの認証（第10章）が絡む

確認例：

```powershell
Get-Service | Where-Object Status -eq 'Running' | Select-Object -First 20
systeminfo | Select-String "Boot Time","System Boot Time"
Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime
```

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| 中核 | Linuxカーネル | NTカーネル / エグゼクティブ |
| ユーザー空間の起点 | systemd（PID 1）が代表的 | smss / services / winlogon などの役割分担 |
| 資源の見せ方 | 単一ディレクトリツリー＋仮想FS（proc/sys） | ドライブレター、レジストリ、オブジェクト名前空間 |
| プロセス生成の典型 | fork + exec | CreateProcess 系 |
| 管理CLI | シェル（bashなど） | PowerShell / cmd |
| サービス管理 | systemdユニット | SCMとサービス |
| 権限の基本単位 | UID/GID＋POSIX権限（＋ACL） | SID＋アクセストークン＋DACL |
| 障害時の代表症状 | kernel panic、OOM killer、unit失敗 | Bug Check（ブルースクリーン）、サービス失敗、イベントログ |

共通点も多い。

- どちらもカーネルとユーザー空間を分ける
- どちらもプロセスとスレッドで実行を管理する
- どちらもファイルシステムとネットワークをOSサービスとして提供する
- どちらも起動後に常駐サービスを立ち上げ、ログインや遠隔管理を可能にする

違うのは「同じ目的をどの部品名で呼ぶか」と「設定の置き場」であることが多い。

---

## 6. コマンド例

### 6.1 今のOSとカーネルを確認する

**目的**：調査対象マシンの系統を誤認しない。

#### Linux

基本構文：

```bash
uname -a
cat /etc/os-release
```

主要オプション：

- `uname -r`：カーネルリリース
- `uname -m`：アーキテクチャ

実行例：

```bash
uname -r
. /etc/os-release && echo "$NAME $VERSION"
```

想定出力の読み方：

- `5.14.0-...el9` のように `el9` があればRHEL系9世代の目安
- Ubuntuなら `VERSION_ID` が `22.04` や `24.04`

必要な権限：一般ユーザーで可。

リスク：なし（参照のみ）。

#### Windows

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsHardwareAbstractionLayer
[System.Environment]::OSVersion.Version
```

あるいは：

```powershell
systeminfo
```

必要な権限：一般ユーザーで多くの情報は取得可。一部は管理者向け。

リスク：なし（参照のみ）。

### 6.2 プロセス一覧を確認する

**目的**：高負荷や残存プロセスの有無を見る。

#### Linux

```bash
ps -eo pid,ppid,user,stat,%cpu,%mem,cmd --sort=-%cpu | head
```

主要列：

- `STAT`：状態。`R`走行、`S`割込可スリープ、`D`不可分スリープ、`Z`ゾンビなど
- `%CPU` / `%MEM`：使用率の目安

必要な権限：自分のプロセスは一般ユーザー、他ユーザー詳細は状況により制限。

リスク：なし（参照のみ）。続けて `kill` する段階で誤停止リスクが出る。

#### Windows

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Id, ProcessName, CPU, WorkingSet
```

`WorkingSet`は物理メモリ使用の目安（バイト）。

必要な権限：一般ユーザーで可。他ユーザーセッションの詳細は制限されうる。

リスク：参照のみなら低。`Stop-Process`は別途注意。

### 6.3 カーネルが公開する情報を見る（Linux） / OS情報を見る（Windows）

#### Linux

```bash
# 警告: 参照は安全だが、/proc 配下への書き込みは挙動を変える
cat /proc/cpuinfo | head
cat /proc/meminfo | head
ls /proc/1/
```

`/proc/1`は通常systemd（またはPID 1）の情報。

#### Windows

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory
```

### 6.4 起動からの経過とログインセッション

#### Linux

```bash
who
who -b
last -n 5
```

#### Windows

```powershell
quser
Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 5 -ErrorAction SilentlyContinue
```

セキュリティログの閲覧は権限と監査設定に依存する。

### 6.5 同一目的の対照

| 目的 | Linux | Windows PowerShell |
|------|-------|--------------------|
| OS名と版 | `cat /etc/os-release` | `Get-ComputerInfo` |
| カーネル/ビルド | `uname -r` | `winver` / `Get-ComputerInfo` |
| プロセス上位 | `ps` / `top` | `Get-Process` |
| 起動時刻 | `who -b` / `uptime -s` | `LastBootUpTime` |
| サービス状態 | `systemctl` | `Get-Service` |

---

## 7. 実務上の注意点

1. **まず正体を確認する**  
   クラウドのテンプレート名と、中のOSリリースが一致しないことがある。調査前に `os-release` や `Get-ComputerInfo` を取る。

2. **PIDをメモする**  
   名前だけだと、再起動後や多重起動で別物になる。時刻とPIDをセットで残す。

3. **仮想化ドライバーを見落とさない**  
   準仮想化ドライバー未導入のままでは、ディスクとネットワークの症状がアプリ問題に見せかけられる。

4. **PID 1の異常は影響範囲が広い**  
   Linuxでsystemdが落ちる、WindowsでSCM周りが壊れると、単一サービス障害より復旧が重い。

5. **GUIの有無で本質は変わらない**  
   Server CoreやSSHのみのLinuxでも、カーネルとプロセスの見方は同じである。CLIで同等の情報を取れるようにする。

---

## 8. セキュリティ上の注意点

1. **カーネルとドライバーは信頼境界そのもの**  
   署名のないドライバーや来歴不明のカーネルモジュールは、権限制御を内側から崩しうる。

2. **デバッグツールの権限**  
   `strace`、プロセスダンプ、ETW取得は秘情報（環境変数、トークン、通信先）を吸い出しうる。取得物の扱いを決める。

3. **情報収集と権限の最小化**  
   調査用に常時Domain Adminやrootでログインしない。読むだけなら読む権限のアカウントで足りることが多い。

4. **起動系の改ざん**  
   GRUB設定、BCD、ブートローダーは、侵入後の永続化に使われる。変更監査とSecure Bootの方針を組織で決める。

---

## 9. よくある障害

| 症状 | 起きやすい層 | 初動の問い |
|------|--------------|------------|
| 電源は入るがログイン画面まで出ない | ブートローダー、カーネル、初期ドライバ | どの段階で止まったか |
| ログイン後すぐセッションが切れる | プロファイル、シェル初期化、GPO/ログインスクリプト | ローカルとドメインどちらで失敗するか |
| 特定デバイスだけ無い | ドライバー、仮想化統合ツール | ゲストツールは入っているか |
| 全体が極端に遅い | CPUスケジューリング、メモリ不足、ディスクI/O | プロセスかI/O待ちか |
| 再起動ループ | 起動サービス失敗、カーネルパニック/Bug Check | 直前の変更は何か |

---

## 10. 切り分け手順

障害対応の初期は、アプリの設定をいじる前にOSの生存を確認する。

### 手順A：到達性の確認

1. ICMPや管理ポート（SSH 22 / RDP 3389）へ疎通するか
2. ハイパーバイザー上でコンソールが操作できるか
3. ゲストが起動中か、カーネルパニック/Bug Check表示か

### 手順B：起動段階の特定

**Linux**

1. GRUBメニューは出るか
2. カーネルメッセージの途中で止まるか
3. emergency/rescueターゲットに入れるか
4. `journalctl -b` で今回起動の失敗ユニットを見る

**Windows**

1. ブートメニューや修復環境に入れるか
2. セーフモードで起動するか
3. イベントビューアーの System ログで Critical/Error を見る
4. 直前のドライバー更新、Windows Update、ディスク不足を疑う

### 手順C：資源とプロセス

1. CPU、メモリ、ディスクの飽和を確認する
2. 上位プロセスのPIDと開始時刻を記録する
3. サービス一覧でFailedを拾う
4. 変更履歴（更新、設定、デプロイ）と突き合わせる

元に戻す方法の原則：

- 設定変更は一件ずつ、前後の記録付きで行う
- ブート設定を触る前にラボならスナップショット、本番なら復旧手段を確認する
- プロセス停止は依存サービスを確認してから行う

---

## 11. 章末問題

### 問題1

ユーザー空間のアプリケーションが、NICのレジスタを直接操作できないのはなぜか。
カーネルとシステムコールの言葉で答えよ。

### 問題2

プロセスとスレッドの違いを、アドレス空間の共有可否に触れて説明せよ。

### 問題3

Linuxで `ps -ef` を実行し、PID 1のコマンド名を確認した。
現代のサーバーLinuxで多い名前は何か。また、それが担う役割を一文で述べよ。

### 問題4

Windowsでサービスが起動しないとき、プロセス一覧だけ見て不足しやすい情報は何か。
どの仕組みを併せて見るべきか。

### 問題5

Linuxは単一のディレクトリツリー、Windowsはドライブレターが基本、という違いが、ディスク追加作業の手順にどう影響するかを述べよ。

### 問題6

次の対応関係のうち、誤っているものを選べ。

1. Linuxのsystemd ≒ WindowsのService Control Manager（役割としての対比）
2. LinuxのPID ≒ WindowsのプロセスID
3. Linuxの `/proc` ≒ Windowsのレジストリ（完全に同一の仕組み）
4. LinuxのUEFI+GRUB ≒ WindowsのUEFI+Boot Manager

---

## 12. 解答と解説

### 問題1

特権命令とハードウェア直接制御はカーネル空間に閉じているからである。
アプリはシステムコール（やその上位API）を通じてカーネルに依頼し、カーネルがドライバー経由でNICを操作する。

### 問題2

プロセスは原則として独自のアドレス空間を持つ実行単位である。
スレッドは同一プロセス内でアドレス空間を共有する実行の流れであり、生成コストは低いが互いのメモリ破壊の影響を受けやすい。

### 問題3

`systemd` が多い（一部の特殊環境を除く）。
PID 1としてユーザー空間の初期化とサービス（ユニット）の依存関係管理を担う。

### 問題4

サービスとしての開始失敗理由、依存関係、開始モード（自動/手動/無効）が見えにくい。
Service Control Managerの状態、つまり `Get-Service` やサービスMMC、イベントログを併せて見る。

### 問題5

Linuxでは空きディレクトリを作り、そこにマウントして既存パスへ接続する設計が基本になる。
Windowsでは新しいボリュームへドライブレターを割り当てるか、NTFSフォルダーへマウントするかを選ぶ。
アプリ設定に書くパスの慣習が、この差の影響を受ける。

### 問題6

誤りは 3。
`/proc` はカーネル状態をファイルのように見せる仮想FSであり、レジストリは設定データベースとして別物である。
情報を調べる「置き場」がある、という意味での緩い対比以上に同一視しない。

---

## 13. ハンズオン演習

### 演習1-1 両OSの正体確認

**前提条件**

- `web01`（Linux）と `winapp01`（Windows）にログインできる
- ラボのスナップショット取得済みが望ましい

**実行内容（Linux）**

```bash
uname -a
cat /etc/os-release
ps -p 1 -o pid,cmd
findmnt -n -o SOURCE,TARGET,FSTYPE /
```

**実行内容（Windows）**

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, LastBootUpTime
Get-Process -Id 4
Get-Volume
```

WindowsのPID 4は `System` プロセスとして見えることが多い。

**確認方法**

- OS名、版、起動時刻、ルート（またはC:）のファイルシステム種別をメモする
- 両者で「今動いている中核」が何かを一文で書き比べる

**元に戻す方法**

- 参照のみのため変更はない

### 演習1-2 プロセスの親子を追う

**目的**：PIDとPPIDの見方を身体で覚える。

**Linux**

```bash
sleep 300 &
ps -o pid,ppid,cmd -p $!
pstree -p | head
# 終了
kill $!
```

**Windows**

```powershell
$p = Start-Process notepad -PassThru
Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)" |
  Select-Object ProcessId, ParentProcessId, Name
Stop-Process -Id $p.Id
```

Server Coreでnotepadが無い場合は `Timeout` や `pwsh` の子プロセスで代替する。

**確認方法**

- 子のPPID/ParentProcessIdが、起動元シェルのPIDと一致する（または近い起動元になる）ことを確認する

**元に戻す方法**

- 起動した一時プロセスを必ず終了する

### 演習1-3 起動ログの入口を開く

**Linux**

```bash
journalctl -b -n 50 --no-pager
systemctl --failed
```

**Windows**

```powershell
Get-WinEvent -LogName System -MaxEvents 30 |
  Where-Object { $_.LevelDisplayName -in 'Error','Critical','Warning' } |
  Format-Table TimeCreated, Id, ProviderName, Message -Wrap
```

**確認方法**

- FailedユニットやErrorイベントが「常にある／無い」の基準線を記録する
- 後章の障害演習で、平常時との差分を取るために使う

**元に戻す方法**

- 参照のみ

### 演習1-4 観察メモの型を作る

次のテンプレートを埋め、リポジトリ外の作業メモに残す。

```text
日時:
ホスト:
OS版:
カーネル/ビルド:
最終起動時刻:
PID 1 または主要常駐:
特記（仮想化ツール、最近の変更）:
```

このメモの型は、第13章の切り分けでもそのまま使う。

---

## 本章のまとめ

OSは、ハードウェア抽象化、資源管理、隔離、共通サービスの提供を担う。
その中核がカーネルであり、アプリはシステムコールやAPIを通じてだけ特権的な操作へ届く。

Linuxは単一ディレクトリツリーとsystemdを中心に、WindowsはNTカーネルとSCM/Winlogonを中心に、同じ目的を別の部品名で実現している。
次章では、実際にOSを入れ、ホスト名や時刻、ネットワークといった「運用の前提条件」を整える。

次章: [第2章 インストールと初期設定](02_install_and_initial_setup.md)


---


<!-- source: 02_install_and_initial_setup.md -->

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


---


<!-- source: 03_files_and_directories.md -->

# 第3章 ファイルとディレクトリ

サーバー作業の大半は、設定ファイルを開き、ログを追い、配置を直し、権限を確認することに帰着する。
パスの読み方、リンクの種類、隠しファイルや属性の意味を両OSで揃えておくと、同じ障害を二度調べずに済む。

ファイル操作は一見単純な作業に見える。
しかし「そのパスは絶対パスか相対パスか」「シンボリックリンクの先はどこか」「隠しファイルは含まれているか」を取り違えるだけで、調査は簡単に長引く。

---

## 1. 学習目標

本章を終えると、次ができるようになる。

1. Linuxのディレクトリ構造（FHS: Filesystem Hierarchy Standard、ファイルシステム階層標準）と、Windowsのドライブ・フォルダー構成を説明できる
2. 絶対パスと相対パスを使い分け、両OSのパス表記の違いを説明できる
3. 作成、複製、移動、削除、内容確認をCLIで安全に実行できる
4. ハードリンクとシンボリックリンク、NTFS（New Technology File System）のリンク機能の違いを概説できる
5. 隠しファイルと基本的なファイル属性の見方、変更方法を説明できる
6. 検索コマンドと圧縮・展開コマンドを両OSで使い分けられる

---

## 2. 基本概念

### 2.1 パスとは何か

**パス（path）**は、ファイルやディレクトリの位置を一意に示す文字列である。

OSは、人間が読むパス文字列を、内部的なファイルシステム上の位置情報へ変換して、実際のデータへたどり着く。
この変換の入口になるのがパスであり、調査でも構築でも最初に確定させる情報になる。

### 2.2 絶対パスと相対パス

パスの書き方には二種類ある。

- **絶対パス（absolute path）**：起点（Linuxの `/`、Windowsのドライブレターなど）から全経路を書く
- **相対パス（relative path）**：現在の作業ディレクトリ（カレントディレクトリ）からの相対位置で書く

相対パスは短く書けて便利だが、実行するディレクトリを勘違いすると、意図しない場所を操作する。
スクリプトや自動化タスクでは、原則として絶対パスを使うか、スクリプト冒頭で作業ディレクトリを固定しておくと事故が減る。

両OSとも、次の特殊表記を共有する。

| 表記 | 意味 |
|------|------|
| `.` | 現在のディレクトリ |
| `..` | 一つ上の親ディレクトリ |
| `~`（Linux） | 現在のユーザーのホームディレクトリ |
| `$HOME`（PowerShell） | 現在のユーザーのホームディレクトリに相当する変数 |

### 2.3 ディレクトリツリーとファイルシステムの関係

Linuxは、ルート `/` を頂点にした単一のディレクトリツリーにすべてのファイルシステムをマウントで接続する。
ディスクを追加しても、ドライブレターは増えず、既存ツリー上の空ディレクトリへ接続先が増えるだけである。

Windowsは、ボリュームごとにドライブレター（`C:`、`D:` など）またはマウントポイントを割り当てる。
ボリュームが増えると、原則としてドライブレターやマウントフォルダーが増える。

この違いは、第6章で扱うストレージの話とも直結する。
「パスが見える」ことの裏には、必ずファイルシステムとマウント（またはボリューム）が存在する。

### 2.4 ディレクトリとフォルダー

実体は同じ「名前とファイルの対応を持つ入れ物」だが、呼び方が異なる。

Linuxでは伝統的に**ディレクトリ（directory）**と呼ぶ。
WindowsのGUI（グラフィカルユーザーインターフェース）では**フォルダー（folder）**と呼ぶことが多いが、コマンドラインやAPIの内部ではディレクトリという用語も使われる。

以降は、CLI（コマンドラインインターフェース）の文脈ではディレクトリ、GUIの文脈ではフォルダーという言葉を使い分ける。

### 2.5 リンクという仕組み

一つの実体（データ）に、複数の名前や参照経路を与える仕組みが**リンク（link）**である。

| 種類 | 概要 | 特徴 |
|------|------|------|
| ハードリンク（hard link） | 同じ実体（Linuxではinode）を複数の名前で指す | 同一ファイルシステム内が基本。実体は一つ |
| シンボリックリンク（symbolic link、ソフトリンク） | 別パスへの参照そのものを持つ小さなファイル | リンク先が消えると壊れたリンク（ダングリングリンク）になる |
| ショートカット（.lnk、Windows） | シェル（エクスプローラー）向けの参照ファイル | POSIX（Portable Operating System Interface）のシンボリックリンクとは仕組みが異なる |
| NTFSシンボリックリンク／ジャンクション／ハードリンク | NTFS上のリンク機能群 | 種類によって対象（ファイルかディレクトリか）や必要な権限が異なる |

ハードリンクは「同じ実体を指す別の名札」であり、片方を削除しても実体はもう一方の名前から生き続ける。
シンボリックリンクは「別のパスを指し示す矢印」であり、矢印の先が無くなればリンクだけが残って壊れる。

### 2.6 隠しファイルと属性

**隠しファイル（hidden file）**は、通常の一覧表示では表示されないファイルである。

- Linux：ファイル名の先頭が `.` で始まるものを慣習的に隠しファイルとして扱う（`.bashrc` など）。特別なフラグではなく、命名規則にすぎない
- Windows：**属性（attribute）**として Hidden が設定されているファイル。命名規則ではなくメタデータで管理する

**属性（attribute）**は、ファイルの性質を示す追加情報である。
Windowsでは Read-only（読み取り専用）、Hidden（隠し）、System（システム）、Archive（アーカイブ）などが代表例になる。
Linuxにも `chattr` で設定する拡張属性（immutable など）があるが、日常運用での使用頻度はWindowsの属性ほど高くない。

### 2.7 検索と圧縮の位置づけ

大量のファイルから目的の一件を探す作業と、複数ファイルを一つにまとめて転送・保管する作業は、運用で頻繁に発生する。
検索はトラブルシューティングの初動、圧縮はバックアップや配布の基礎になるため、両方とも早い段階でCLIでの操作を身につけておく価値が大きい。

---

## 3. Linuxでの実現方法

### 3.1 ディレクトリ構造（実務で覚える場所）

Linuxのディレクトリ配置は、FHSという標準にゆるく従う。
すべてのディストリビューションが完全に一致するわけではないが、代表的なパスの役割は共通している。

| パス | 主な役割 |
|------|----------|
| `/` | ルート。すべての起点 |
| `/bin`, `/sbin` | 基本的な実行コマンド（多くのディストリビューションで `/usr` 配下へ統合済み） |
| `/etc` | 設定ファイル |
| `/var` | 可変データ（ログ、キャッシュ、スプールなど） |
| `/var/log` | ログファイル |
| `/var/lib` | アプリケーションが持続的に使う状態データ |
| `/home` | 一般ユーザーのホームディレクトリ |
| `/root` | rootユーザー専用のホームディレクトリ |
| `/usr` | ユーザーランドのプログラムや共有データ |
| `/usr/local` | ローカルに追加したソフトウェア |
| `/opt` | パッケージ管理外の追加ソフトウェア |
| `/tmp` | 一時ファイル。再起動で消えることが多い |
| `/boot` | カーネルやブートローダー関連ファイル |
| `/dev` | デバイスファイル |
| `/proc`, `/sys` | カーネルが提供する仮想ファイルシステム。ディスク上の実体を持たない |
| `/media`, `/mnt` | リムーバブルメディアや一時マウント先の慣習的な置き場 |

`/proc` と `/sys` は特別で、カーネルの内部状態をファイルのように見せているだけである。
`cat /proc/cpuinfo` のような参照はできるが、これは通常のディスク上ファイルの読み書きとは性質が異なる。

### 3.2 絶対パスと相対パスの操作

現在地を確認し、移動する基本コマンドは次のとおりである。

```bash
pwd
ls -la
cd /var/log
cd ..
cd ~
```

`pwd`（print working directory）は現在の作業ディレクトリを絶対パスで表示する。
`cd`（change directory）は引数なしで実行するとホームディレクトリへ戻る。

### 3.3 基本的なファイル操作

```bash
mkdir -p ~/lab/ch3
touch ~/lab/ch3/sample.txt
cp ~/lab/ch3/sample.txt ~/lab/ch3/sample.bak
mv ~/lab/ch3/sample.bak ~/lab/ch3/renamed.txt
cat ~/lab/ch3/renamed.txt
stat ~/lab/ch3/renamed.txt
# 警告: rm -rf は取り消しが困難。対象パスを必ず確認してから実行する
rm ~/lab/ch3/renamed.txt
```

`mkdir -p` は、途中の親ディレクトリが無ければまとめて作成する。
`stat` は、権限、所有者、更新時刻などのメタデータを一括表示するため、権限調査の初動に向く。

### 3.4 ハードリンクとシンボリックリンク

Linuxのファイルシステムでは、ファイルの実体は**inode**という管理番号に紐づく。
ディレクトリエントリ（ファイル名）は、このinodeへの参照にすぎない。

```bash
echo hello > ~/lab/ch3/a.txt
ln ~/lab/ch3/a.txt ~/lab/ch3/a-hard.txt      # ハードリンク
ln -s ~/lab/ch3/a.txt ~/lab/ch3/a-soft.txt   # シンボリックリンク
ls -li ~/lab/ch3/
readlink -f ~/lab/ch3/a-soft.txt
```

`ls -li` の左端に表示されるinode番号が一致していれば、それらは同じ実体を指すハードリンクである。
シンボリックリンクは別のinodeを持ち、中身はリンク先パスの文字列そのものになる。

ハードリンクには制約がある。

- 同一ファイルシステム内でのみ作成できる
- ディレクトリに対しては通常のユーザーが作成できない（循環参照を防ぐため）

### 3.5 隠しファイルと属性

```bash
ls -la ~
ls -A ~
lsattr ~/lab/ch3/a.txt
# 警告: chattr +i を付けたファイルは root でも上書き・削除できなくなる
sudo chattr +i ~/lab/ch3/a.txt
lsattr ~/lab/ch3/a.txt
sudo chattr -i ~/lab/ch3/a.txt
```

`ls -la` は `.` で始まる名前も含めて一覧表示する。
`chattr +i` は immutable（変更不可）フラグを付与し、rootであっても変更・削除を拒否させる強い制御であるため、恒久的な設定変更よりも一時的な保護に限定して使う。

### 3.6 検索

```bash
find /etc -name 'ssh*' 2>/dev/null | head
find /var/log -mtime -1 -type f
grep -R "PermitRootLogin" /etc/ssh/ 2>/dev/null
locate sshd_config 2>/dev/null
```

`find` はファイルシステムを直接たどるため常に最新結果を返すが、大規模ディレクトリでは低速になりやすい。
`locate` は事前に作成されたデータベース（`updatedb` で更新）を検索するため高速だが、直近の変更を反映していないことがある。

### 3.7 圧縮と展開

```bash
tar -czf ~/lab/ch3/etc-ssh.tgz -C /etc ssh
tar -tzf ~/lab/ch3/etc-ssh.tgz | head
tar -xzf ~/lab/ch3/etc-ssh.tgz -C ~/lab/ch3/extracted
gzip -k ~/lab/ch3/sample.txt
gunzip ~/lab/ch3/sample.txt.gz
```

`tar` は複数ファイルを一つにまとめる（アーカイブ化する）だけの機能であり、圧縮は `-z`（gzip）や `-J`（xz）で組み合わせる。
`-C` オプションは、アーカイブ内の相対パスを短く保つために、実行前にディレクトリを移動する働きを持つ。

---

## 4. Windowsでの実現方法

### 4.1 ドライブと主なフォルダー

Windowsでは、ボリュームにドライブレター（`C:` など）を割り当て、その配下にフォルダー構造を持つ。

| パス | 主な役割 |
|------|----------|
| `C:\` | 通常はシステムドライブ |
| `C:\Windows` | OS本体 |
| `C:\Windows\System32` | 主要な実行ファイルとライブラリ |
| `C:\Program Files` | 64ビットアプリケーション |
| `C:\Program Files (x86)` | 32ビットアプリケーション（64ビット版Windowsの場合） |
| `C:\ProgramData` | マシン共通のアプリケーションデータ |
| `C:\Users\<user>` | 各ユーザーのプロファイル |
| `C:\Users\<user>\AppData` | ユーザー単位のアプリケーション設定・キャッシュ |
| `C:\Users\Public` | 全ユーザーで共有しやすい場所 |

`AppData` の配下はさらに Local、LocalLow、Roaming に分かれ、それぞれ同期方針や永続性が異なる。
アプリの設定が消える、別マシンで復元されないといった調査では、この分類を知っているかどうかで速さが変わる。

### 4.2 絶対パスと相対パスの操作（PowerShell）

```powershell
Get-Location
Set-Location C:\Windows\Temp
Set-Location ..
Set-Location $HOME
```

`Get-Location` は現在の作業ディレクトリを表示し、`Set-Location` は移動する。
`cd` はこれらのエイリアス（別名）として使えるが、本書はPowerShellの正式なコマンドレット（cmdlet）名を基準に説明する。

### 4.3 基本的なファイル操作

```powershell
New-Item -ItemType Directory -Path $HOME\lab\ch3 -Force
'hello' | Out-File $HOME\lab\ch3\sample.txt -Encoding utf8
Copy-Item $HOME\lab\ch3\sample.txt $HOME\lab\ch3\sample.bak
Rename-Item $HOME\lab\ch3\sample.bak renamed.txt
Get-Content $HOME\lab\ch3\renamed.txt
Get-Item $HOME\lab\ch3\renamed.txt | Format-List *
# 警告: Remove-Item -Recurse -Force は取り消しが困難
Remove-Item $HOME\lab\ch3\renamed.txt
Get-ChildItem $HOME\lab\ch3 -Force
```

従来コマンドの `dir`、`copy`、`move`、`del` も内部的にはPowerShellのエイリアスとして動くか、cmd.exe互換として使えるが、本書はPowerShellのコマンドレットを主に扱う。
`Get-Item` は `stat` に近く、属性やタイムスタンプをまとめて確認できる。

### 4.4 NTFSリンクの概要

```powershell
# ハードリンク
New-Item -ItemType HardLink -Path $HOME\lab\ch3\a-hard.txt -Target $HOME\lab\ch3\sample.txt

# シンボリックリンク（権限や開発者モード設定が必要な場合がある）
New-Item -ItemType SymbolicLink -Path $HOME\lab\ch3\a-soft.txt -Target $HOME\lab\ch3\sample.txt

# ディレクトリジャンクション（例。管理者権限は不要だが対象パスに注意）
# New-Item -ItemType Junction -Path D:\data-link -Target D:\data
```

NTFSは、ハードリンク、シンボリックリンク、ジャンクションという三種類のリンク機能を持つ。

| 種類 | 対象 | 必要な権限の目安 |
|------|------|------------------|
| ハードリンク | ファイルのみ | 通常ユーザーで可（同一ボリューム内） |
| シンボリックリンク | ファイル・ディレクトリ | 既定では管理者権限、または「開発者モード」の有効化 |
| ジャンクション | ディレクトリのみ | 通常ユーザーで可 |

シンボリックリンク作成が権限エラーで失敗する場合は、`SeCreateSymbolicLinkPrivilege` という特権の有無を疑う。
Windows 10以降は、開発者モードを有効にすると管理者権限なしでもシンボリックリンクを作成できるようになる。

### 4.5 隠しファイルと属性

```powershell
Get-ChildItem $HOME\lab\ch3 -Force
attrib $HOME\lab\ch3\sample.txt
# 隠し属性と読み取り専用属性を付与する例
attrib +h +r $HOME\lab\ch3\sample.txt
attrib -h -r $HOME\lab\ch3\sample.txt
(Get-Item $HOME\lab\ch3\sample.txt).Attributes
```

`Get-ChildItem` は既定で隠しファイルとシステムファイルを除外するため、`-Force` を付けて初めて全件が見える。
`attrib` は古くからあるコマンドだが、属性確認・変更の定番として今も使われる。

代表的な属性は次のとおりである。

| 記号 | 属性名 | 意味 |
|------|--------|------|
| R | Read-only | 上書き・削除に警告や制限が付く |
| H | Hidden | 通常表示では見えない |
| S | System | OSが使うファイルであることを示す |
| A | Archive | バックアップ済みかどうかの目印に使われることがある |

### 4.6 検索

```powershell
Get-ChildItem C:\Windows\System32 -Filter *.dll -Recurse -ErrorAction SilentlyContinue |
  Select-Object -First 5 FullName
Select-String -Path C:\Windows\System32\drivers\etc\hosts -Pattern 'localhost'
Get-ChildItem C:\ -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object LastWriteTime -gt (Get-Date).AddDays(-1) |
  Select-Object -First 20 FullName, LastWriteTime
```

`Get-ChildItem -Recurse` はディレクトリツリーを再帰的にたどる。
`Select-String` はLinuxの `grep` に近く、テキスト内のパターン一致行を返す。
`-ErrorAction SilentlyContinue` は、権限不足で読めないディレクトリのエラーを握りつぶして検索を継続する目的で使う。

### 4.7 圧縮と展開

```powershell
Compress-Archive -Path $HOME\lab\ch3\* -DestinationPath $HOME\lab\ch3\backup.zip -Force
Expand-Archive -Path $HOME\lab\ch3\backup.zip -DestinationPath $HOME\lab\ch3\expanded -Force
```

Windows 10以降には `tar.exe` も同梱されており、Linuxで作られた `.tar.gz` をそのまま展開できる。

```powershell
tar -xzf etc-ssh.tgz -C C:\lab\ch3\extracted
```

`Compress-Archive` はZip形式に限定される点に注意する。
tarやgzip形式のアーカイブを作りたい場合は同梱の `tar.exe` を使うか、別途ツールを導入する。

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| 起点 | `/` の単一ツリー | ドライブレター＋UNC（Universal Naming Convention） |
| 区切り文字 | `/` | `\`（PowerShellでは `/` も多くの場面で使える） |
| 大文字小文字の区別 | 区別する（一般的） | 区別しない（一般的。NTFS内部は大文字小文字を保持するが比較時は区別しない） |
| 隠しの仕組み | 命名規則（先頭 `.`） | メタデータとしてのHidden属性 |
| 追加の属性管理 | `chattr`（拡張属性） | `attrib`（R/H/S/A） |
| リンクの種類 | ハードリンク、シンボリックリンク | ハードリンク、シンボリックリンク、ジャンクション |
| 検索CLI | `find`、`locate`、`grep` | `Get-ChildItem`、`Select-String` |
| 圧縮CLI | `tar`、`gzip`、`xz` | `Compress-Archive`、同梱の`tar.exe` |

### 5.1 パス表記の違い

```text
Linux:   /var/log/messages
Windows: C:\Windows\System32\winevt\Logs\System.evtx
UNC:     \\dc01\share\docs\readme.txt
```

**UNC（Universal Naming Convention）**は、ドライブレターを介さずにネットワーク上の共有資源を指すWindows独自の表記である。
`\\サーバー名\共有名\パス` の形式を取り、ドライブレターを割り当てなくても直接アクセスできる。

パスの長さにも歴史的な違いがある。
Windowsは伝統的に **MAX_PATH**（合計260文字）という制限を持っていたが、Windows 10以降はレジストリまたはグループポリシーで長いパスのサポートを有効化できる。
Linuxのパス長制限はディストリビューションやファイルシステムに依存するが、実務で問題になる頻度はWindowsのMAX_PATH制限より低い。

Windowsには、ファイル名として使えない予約語もある。
`CON`、`PRN`、`AUX`、`NUL`、`COM1`〜`COM9`、`LPT1`〜`LPT9` は、拡張子を付けても単体のファイル名として作成できない。
また `\ / : * ? " < > |` はパス区切りやワイルドカードと衝突するため、ファイル名には使えない。
Linux由来のファイルをWindowsへ移行する際、これらの文字や名前が含まれていると失敗する原因になる。

---

## 6. コマンド例

### 6.1 現在地と一覧を確認する

**目的**：現在の作業ディレクトリと、その中身（隠しファイルを含む）を確認する。

#### Linux

基本構文：

```bash
pwd
ls -la
```

主要オプション：

- `-l`：詳細情報（権限、所有者、サイズ、更新時刻）を表示
- `-a`：`.`、`..` を含むすべてのエントリを表示
- `-A`：`.`、`..` を除いた隠しファイルを表示

実行例：

```bash
cd ~/lab/ch3
pwd
ls -la
```

想定出力と読み方：

```text
/home/operator/lab/ch3
total 8
drwxr-xr-x 2 operator operator 4096 Jul 30 04:00 .
drwxr-xr-x 3 operator operator 4096 Jul 30 04:00 ..
-rw-r--r-- 1 operator operator    6 Jul 30 04:00 sample.txt
```

先頭の `d` はディレクトリ、`-` は通常ファイルを示す。
続く9文字が所有者・グループ・その他のrwx権限である（詳細は第4章）。

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

#### Windows

```powershell
Get-Location
Get-ChildItem -Force
```

想定出力と読み方：

```text
Path
----
C:\Users\operator\lab\ch3


    Directory: C:\Users\operator\lab\ch3

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          7/30/2026   4:00 AM              6 sample.txt
```

`Mode` 列の `a` はArchive、`h` があればHidden、`r` があればRead-onlyを示す。

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

### 6.2 再帰削除（危険操作）

**目的**：ディレクトリを配下ごと削除する。

> **警告**：この操作は取り消せない。対象パスを必ず事前に確認し、可能ならバックアップまたはスナップショットを取得してから実行する。

#### Linux

基本構文：

```bash
rm -rf /path/to/dir
```

主要オプション：

- `-r`：ディレクトリを再帰的に処理
- `-f`：確認なしで強制実行し、存在しないファイルのエラーも無視

実行例：

```bash
rm -rf ~/lab/ch3/tmp-work
```

想定出力と読み方：正常終了時は出力なし。
存在しないパスでも `-f` があればエラーを表示しない点に注意する。

必要な権限：対象への書き込み権限、または該当する管理者権限。

誤操作リスク：システムディレクトリやルート近辺を指定すると、OSそのものが起動不能になる。
実行前に必ず `pwd` と対象パスの `ls` で存在確認を行う。

#### Windows

基本構文：

```powershell
Remove-Item -Recurse -Force C:\path\to\dir
```

主要オプション：

- `-Recurse`：配下を再帰的に削除
- `-Force`：読み取り専用や隠しファイルも含めて削除

実行例：

```powershell
Remove-Item -Recurse -Force $HOME\lab\ch3\tmp-work
```

想定出力と読み方：正常終了時は出力なし。

必要な権限：対象への書き込み権限、システムディレクトリは管理者権限。

誤操作リスク：`C:\Windows` のような対象を誤って指定すると、OSが起動不能になる。
`-WhatIf` オプションを先に付けて、削除対象を確認してから本実行することを推奨する。

### 6.3 リンクを作成して実体を確認する

**目的**：ハードリンクとシンボリックリンクの違いを実際に確認する。

#### Linux

```bash
echo hello > ~/lab/ch3/a.txt
ln ~/lab/ch3/a.txt ~/lab/ch3/a-hard.txt
ln -s ~/lab/ch3/a.txt ~/lab/ch3/a-soft.txt
ls -li ~/lab/ch3/
```

想定出力と読み方：

```text
123456 -rw-r--r-- 2 operator operator 6 ... a-hard.txt
123456 -rw-r--r-- 2 operator operator 6 ... a.txt
123789 lrwxrwxrwx 1 operator operator 20 ... a-soft.txt -> /home/operator/lab/ch3/a.txt
```

`a.txt` と `a-hard.txt` は同じinode番号（`123456`）とリンク数`2`を持つため、実体は一つである。
`a-soft.txt` は別のinodeで、内容がリンク先パスの文字列になっている。

必要な権限：同一ファイルシステム内での作成は一般ユーザーで可。

誤操作リスク：低い。ただし削除対象を間違えると意図した実体まで消える。

#### Windows

```powershell
New-Item -ItemType HardLink -Path $HOME\lab\ch3\a-hard.txt -Target $HOME\lab\ch3\a.txt
New-Item -ItemType SymbolicLink -Path $HOME\lab\ch3\a-soft.txt -Target $HOME\lab\ch3\a.txt
Get-Item $HOME\lab\ch3\a-soft.txt | Select-Object LinkType, Target
```

必要な権限：ハードリンクは一般ユーザーで可。
シンボリックリンクは既定で管理者権限、または開発者モードの有効化が必要。

誤操作リスク：低い。作成失敗時のエラーメッセージから権限不足かどうかを判断する。

### 6.4 検索の入口

**目的**：設定ファイルや特定文字列を含むファイルを素早く見つける。

#### Linux

```bash
find /etc -name 'ssh*' 2>/dev/null
grep -R "PermitRootLogin" /etc/ssh/ 2>/dev/null
```

必要な権限：一般ユーザーで多くの範囲を確認可能。`/etc` 配下の一部は権限で制限される。

誤操作リスク：なし（参照のみ）。

#### Windows

```powershell
Get-ChildItem C:\ProgramData -Filter '*.conf' -Recurse -ErrorAction SilentlyContinue
Select-String -Path C:\inetpub\logs\LogFiles\*\*.log -Pattern '500' -ErrorAction SilentlyContinue
```

必要な権限：一般ユーザーで多くの範囲を確認可能。

誤操作リスク：なし（参照のみ）。

### 6.5 圧縮と展開

**目的**：複数ファイルを一つにまとめ、別の場所で展開する。

#### Linux

```bash
tar -czf backup.tgz -C ~/lab/ch3 .
tar -tzf backup.tgz | head
```

必要な権限：対象ディレクトリの読み取り権限。

誤操作リスク：出力先を誤ると既存ファイルを上書きする可能性がある。

#### Windows

```powershell
Compress-Archive -Path $HOME\lab\ch3\* -DestinationPath backup.zip -Force
Expand-Archive -Path backup.zip -DestinationPath expanded -Force
```

必要な権限：対象ディレクトリの読み取り権限、出力先への書き込み権限。

誤操作リスク：`-Force` は既存の出力先を上書きするため、意図しない上書きに注意する。
ディスク使用量の詳しい調査とinodeの確認は第6章で扱う。

---

## 7. 実務上の注意点

1. **本番設定を直す前にコピーを取る**
   タイムスタンプ付きのファイル名でコピーしておけば、変更前の状態にすぐ戻せる。

2. **改行コードと文字コードに注意する**
   LinuxはLF（改行）、WindowsはCRLF（復帰＋改行）を標準とする。
   UTF-8とUTF-16の混在も、スクリプトの実行エラーやログの文字化けにつながる。

3. **空白を含むパスは引用符で囲む**
   Windowsの `Program Files` のように空白を含むパスは、引用符を省略するとコマンドが引数を誤解釈する。

4. **シンボリックリンクをバックアップツールがどう扱うかを事前確認する**
   リンクそのものをコピーするのか、リンク先の実体を展開するのかで、復元結果が大きく変わる。

5. **一時ディレクトリの掃除は使用中ファイルに注意する**
   `/tmp` や `Temp` を無条件に空にすると、実行中のプロセスが使っているファイルを壊すことがある。

6. **相対パスに依存したスクリプトを共有しない**
   実行するディレクトリが変わると、同じスクリプトでも別の結果になる。

7. **大文字小文字の扱いの違いを意識する**
   Linux由来のファイルをWindowsへコピーすると、大文字小文字だけが異なる二つのファイルが一つに衝突することがある。

8. **長いパスによる操作失敗を想定しておく**
   Windowsで深い階層のディレクトリを扱うときは、長いパスのサポート状況を事前に確認する。

---

## 8. セキュリティ上の注意点

1. **世界読み取り可能な場所へ秘密情報を置かない**
   認証情報や鍵ファイルは、他ユーザーが読めるディレクトリに置かない。

2. **共有ディレクトリの権限を定期的に見直す**
   一時的に緩めた権限が、そのまま放置されるケースは多い。

3. **ダウンロードしたアーカイブは展開先を限定してから確認する**
   展開結果がどこに何を作るか事前に把握していないと、意図しない場所へファイルが展開される（パストラバーサル的な事故）。

4. **ジャンクションやシンボリックリンクによる経路の見せかけに注意する**
   信頼できるパスに見えて、実際には別の場所を指すリンクが攻撃の足がかりになることがある。

5. **隠しファイルや属性だけに頼ったアクセス制御をしない**
   Hiddenや先頭ドットは表示上の抑制にすぎず、アクセス権限の代わりにはならない。

---

## 9. よくある障害

| 症状 | 起きやすい原因 |
|------|----------------|
| ファイルが見当たらない | 隠し属性、先頭ドット、別ユーザーのホーム、別ドライブを見ている |
| Permission denied / Access denied | 権限不足（第4章）、SELinux/AppArmorなどの追加制御、ファイルロック |
| シンボリックリンクが壊れている | リンク先の削除・移動、相対リンクの基準ディレクトリの誤解 |
| パスが長すぎるというエラー | WindowsのMAX_PATH制限、UNCパスの長さ、長いパスの未有効化 |
| 改行差でスクリプトが動かない | LF/CRLFの混在、エディタの改行設定 |
| 文字化けしたファイル名 | 文字コードの不一致、コピー元と先のロケール差 |

---

## 10. 切り分け手順

ファイル関連の障害では、パスの実在確認から始め、属性、リンク、文字コードの順に絞り込む。

### 手順A：存在と表記の確認

1. 絶対パスで対象が本当に存在するかを確認する
2. 大文字小文字の違いがないかを確認する
3. 隠し属性や先頭ドットで除外されていないかを確認する

### 手順B：権限と属性の確認

1. `ls -l` または `Get-Item` で権限と属性を確認する
2. Linuxなら追加のアクセス制御（SELinux、AppArmor）を疑う
3. Windowsなら読み取り専用、Hidden、System属性を確認する

### 手順C：リンクをたどる

1. `readlink -f` または `Get-Item` の `Target` プロパティでリンク先を確認する
2. リンク先が存在するか、権限があるかを確認する
3. 相対リンクの場合、基準ディレクトリが想定と一致しているかを確認する

### 手順D：文字コードと改行

1. `file` コマンドやエディタの表示でエンコーディングを確認する
2. 改行コードがLFかCRLFかを確認する
3. 必要であれば `dos2unix`／`unix2dos` 相当の変換を行う

元に戻す方法の原則：

- 調査目的の操作は読み取りのみに留め、対象ファイルを直接書き換えない
- 属性やパーミッションを変更した場合は、変更前の値を記録しておき、調査後に戻す
- 削除を伴う検証はラボ環境のコピーで行う

---

## 11. 章末問題

### 問題1

`/var/log` と `C:\Windows\System32\winevt\Logs` は、それぞれ何のためのディレクトリか。
一文ずつ述べよ。

### 問題2

ハードリンクとシンボリックリンクの違いを、inodeという言葉を使って説明せよ。

### 問題3

Linuxで隠しファイルも含めてすべて一覧するコマンドは何か。
Windowsで同等の結果を得るコマンドレットは何か。

### 問題4

`C:\` と `/` という起点の違いが、追加ディスクをマウントする作業にどう影響するかを述べよ。

### 問題5

`rm -rf /` や `Remove-Item C:\Windows -Recurse -Force` が危険な理由を、取り消し可否の観点から述べよ。

### 問題6

Windowsのシンボリックリンク作成が権限エラーで失敗した。
確認すべき設定を二つ挙げよ。

### 問題7

次のうち、Windowsのファイル名として単体では使用できないものを選べ。

1. `report.txt`
2. `CON`
3. `data-2026.csv`
4. `archive.tar.gz`

---

## 12. 解答と解説

### 問題1

`/var/log` はLinuxのシステムやアプリケーションのログを格納するディレクトリである。
`C:\Windows\System32\winevt\Logs` はWindowsイベントログ（`.evtx`形式）を格納するディレクトリである。

### 問題2

ハードリンクは同じinode（実体）を複数の名前で参照する仕組みであり、どの名前を消しても他の名前から実体へアクセスできる。
シンボリックリンクは別のinodeを持つ独立したファイルで、中身がリンク先パスの文字列であるため、リンク先が消えると参照が壊れる。

### 問題3

Linuxは `ls -la`（または `ls -A`）。
Windowsは `Get-ChildItem -Force`。

### 問題4

Linuxでは空のディレクトリを作成し、そこへ追加ディスクをマウントして既存のツリーへ接続する設計が基本になる。
Windowsでは新しいボリュームへドライブレターを割り当てるか、既存のNTFSフォルダーへマウントポイントとして接続するかを選ぶ。

### 問題5

どちらも確認なしの再帰削除であり、実行後に元へ戻す標準的な手段（ゴミ箱やUndo）が存在しない。
対象がシステムディレクトリであれば、OSそのものが起動不能になる。

### 問題6

管理者権限でPowerShellを実行しているか、および開発者モードが有効になっているかを確認する。

### 問題7

正解は 2。
`CON` はWindowsの予約デバイス名であり、拡張子を付けても単体のファイル名としては作成できない。

---

## 13. ハンズオン演習

### 演習3-1 作業ディレクトリの作成とファイル操作

**前提条件**

- LinuxとWindowsの両方に一般ユーザーでログインできる
- ホームディレクトリへの書き込み権限がある

**実行内容（Linux）**

```bash
mkdir -p ~/lab/ch3/{src,dst}
echo 'ch3' > ~/lab/ch3/src/note.txt
cp -a ~/lab/ch3/src/note.txt ~/lab/ch3/dst/
ln -s ~/lab/ch3/src/note.txt ~/lab/ch3/dst/note-link
ls -la ~/lab/ch3/dst
```

**実行内容（Windows）**

```powershell
New-Item -ItemType Directory -Force -Path $HOME\lab\ch3\src, $HOME\lab\ch3\dst | Out-Null
'ch3' | Out-File $HOME\lab\ch3\src\note.txt -Encoding utf8
Copy-Item $HOME\lab\ch3\src\note.txt $HOME\lab\ch3\dst\
New-Item -ItemType SymbolicLink -Path $HOME\lab\ch3\dst\note-link -Target $HOME\lab\ch3\src\note.txt -Force
Get-ChildItem $HOME\lab\ch3\dst -Force
```

**確認方法**

- リンク経由でファイルの内容が読めることを確認する
- コピーとリンクの違いを、リンク先の元ファイルを書き換えて確認する

**元に戻す方法**

```bash
rm -rf ~/lab/ch3
```

```powershell
Remove-Item -Recurse -Force $HOME\lab\ch3
```

### 演習3-2 隠しファイルと属性、検索、圧縮の一連操作

**前提条件**：演習3-1で作成した `~/lab/ch3` または `$HOME\lab\ch3` が存在する。

**実行内容（Linux）**

```bash
touch ~/lab/ch3/.secret
ls ~/lab/ch3 && ls -a ~/lab/ch3
grep -R "ch3" ~/lab/ch3 2>/dev/null
tar -czf ~/lab/ch3-backup.tgz -C ~/lab ch3
mkdir -p ~/lab/ch3-restore
tar -xzf ~/lab/ch3-backup.tgz -C ~/lab/ch3-restore
```

**実行内容（Windows）**

```powershell
New-Item -ItemType File -Path $HOME\lab\ch3\secret.txt -Force
attrib +h $HOME\lab\ch3\secret.txt
Get-ChildItem $HOME\lab\ch3; Get-ChildItem $HOME\lab\ch3 -Force
Select-String -Path $HOME\lab\ch3\**\*.txt -Pattern 'ch3'
Compress-Archive -Path $HOME\lab\ch3 -DestinationPath $HOME\lab\ch3-backup.zip -Force
Expand-Archive -Path $HOME\lab\ch3-backup.zip -DestinationPath $HOME\lab\ch3-restore -Force
```

**確認方法**

- 通常表示では隠しファイルが見えず、`-a`／`-Force` を付けると見えること
- 展開後のディレクトリに元と同じファイルが存在すること

**元に戻す方法**

```bash
rm -rf ~/lab/ch3-backup.tgz ~/lab/ch3-restore ~/lab/ch3/.secret
```

```powershell
attrib -h $HOME\lab\ch3\secret.txt
Remove-Item -Recurse -Force $HOME\lab\ch3-backup.zip, $HOME\lab\ch3-restore, $HOME\lab\ch3\secret.txt
```

---

## 14. 本章のまとめ

ファイル操作は単純に見えるが、パスの思想、リンクの種類、隠し属性、文字コードの違いが障害の温床になる。
Linuxは単一ディレクトリツリーと命名規則ベースの隠しファイル、Windowsはドライブレターとメタデータベースの属性という、別々の設計思想の上に成り立っている。

次章では、そのファイルへ「誰が何をできるか」を決める権限モデルへ進む。

次章: [第4章 ユーザー、グループ、権限](04_users_groups_permissions.md)


---


<!-- source: 04_users_groups_permissions.md -->

# 第4章 ユーザー、グループ、権限

「ファイルはあるのに開けない」「昨日まで動いたサービスが Permission denied になる」という報告は、権限モデルの理解不足で調査が長引く典型である。
LinuxのrwxとWindowsのACL（Access Control List、アクセス制御リスト）は見た目が違うが、どちらも「誰が・何に・どの操作を許されているか」を定義している点は同じである。

権限の障害は、原因が一つに絞られていることが多い。
主体（誰として動いているか）、対象（どのファイルやサービスか）、権限（何が許可・拒否されているか）の三点を順に確認すれば、たいていは早期に切り分けられる。

---

## 1. 学習目標

本章を終えると、次ができるようになる。

1. LinuxのUID（User ID）/GID（Group ID）、root、sudoの役割を説明できる
2. 所有者、所有グループ、その他という三枠と、rwx（read/write/execute）権限を読み書きできる
3. `chmod`、`chown`、`umask`を使った権限操作と、ACLによる拡張ができる
4. WindowsのSID（Security Identifier）、ローカルユーザー/グループ、NTFSアクセス許可、継承、UAC（User Account Control）を説明できる
5. 最小権限の原則に沿って、管理用アカウントと日常用アカウントを分けられる
6. 権限エラーの切り分け手順を両OSで実行できる

---

## 2. 基本概念

### 2.1 主体、対象、権限という三点組

権限は次の三点組で考えると整理しやすい。

1. **主体（誰）**：ユーザー、グループ、サービスアカウント
2. **対象（何に）**：ファイル、ディレクトリ、レジストリキー、サービス
3. **権限（何ができる）**：読み取り、書き込み、実行、変更、フルコントロールなど

トラブルシューティングでは、この三点のどれが崩れているかを順に確認する。
「誰として動いているか」を確認せずに権限設定だけを疑うと、原因を見誤ることが多い。

### 2.2 最小権限の原則

**最小権限の原則（principle of least privilege）**は、作業に必要な権限だけを与える考え方である。

常時Domain Adminsや常時rootで作業すると、次の二つのリスクが最大化する。

- 誤操作の影響範囲が広がる（タイプミス一つでシステム全体に影響しうる）
- 侵害されたときの被害半径（blast radius）が広がる

日常業務は権限を絞ったアカウントで行い、必要なときだけ昇格するのが基本方針になる。

### 2.3 識別子という考え方

OSは、人が読む名前ではなく、内部的な識別子で権限を管理する。

| OS | 人が読む名前 | 内部の識別子 |
|----|--------------|--------------|
| Linux | ユーザー名／グループ名 | **UID**／**GID** |
| Windows | アカウント名 | **SID**（Security Identifier） |

ユーザー名やアカウント名は変更できても、権限の実体は識別子側に紐づいている。
同じ名前で作り直したアカウントが、以前とは異なるUIDやSIDを持ち、以前の所有ファイルへアクセスできなくなる事故は珍しくない。
調査では、名前と識別子の両方を確認する習慣を持つ。

### 2.4 権限モデルの二つの系統

権限の表現方法には大きく二つの系統がある。

- **簡易モデル**：対象ごとに「所有者」「グループ」「その他」という限られた枠で権限を割り当てる。Linuxの伝統的なパーミッションが代表例
- **ACLモデル**：対象ごとに任意の主体（複数のユーザーやグループ）へ個別に権限を割り当てられる。WindowsのNTFS権限、およびLinuxの拡張ACLが該当する

簡易モデルは把握しやすい反面、細かい権限分けには向かない。
ACLモデルは柔軟だが、エントリが増えると全体像を追いにくくなる。

---

## 3. Linuxでの実現方法

### 3.1 ユーザーとグループの基本操作

```bash
id
getent passwd operator
getent group wheel
sudo useradd -m -s /bin/bash operator
sudo passwd operator
sudo groupadd appadmins
sudo usermod -aG appadmins operator
```

`id` は自分自身のUID、GID、所属グループを表示する。
`getent` はローカルファイルだけでなく、LDAP（Lightweight Directory Access Protocol）などのネームサービス経由の情報も含めて確認できる。

**root**はUID 0を持つ特権ユーザーであり、多くの権限チェックを実質的にバイパスできる。
直接ログインは避け、**sudo**（superuser do）で必要なコマンドだけを一時的に昇格させる運用が一般的である。

### 3.2 所有者、グループ、その他

Linuxの伝統的な権限モデルは、ファイルごとに三つの枠を持つ。

```bash
ls -l ~/lab/ch3/sample.txt
```

```text
-rw-r--r-- 1 operator appadmins 6 Jul 30 04:00 sample.txt
```

先頭10文字の内訳は次のとおりである。

| 位置 | 意味 |
|------|------|
| 1文字目 | ファイル種別（`-`は通常ファイル、`d`はディレクトリ、`l`はシンボリックリンク） |
| 2〜4文字目 | 所有者（owner）の権限 |
| 5〜7文字目 | 所有グループ（group）の権限 |
| 8〜10文字目 | その他（other）の権限 |

### 3.3 rwxとchmod／chown／umask

| 記号 | ファイルでの意味 | ディレクトリでの意味 |
|------|------------------|----------------------|
| r（read） | 内容を読む | 一覧を取得する |
| w（write） | 内容を書き換える | 配下のファイルを作成・削除する |
| x（execute） | プログラムとして実行する | 配下へ入る（traverse、通過） |

ディレクトリのxビットは特に見落とされやすい。
xが無いディレクトリは、中のファイル権限が正しくても「そこへ入れない」ために操作できない。

```bash
chmod 640 file.txt
chmod u=rw,g=r,o= file.txt
sudo chown operator:appadmins file.txt
sudo chown operator file.txt
sudo chgrp appadmins file.txt
umask
umask 027
```

`chmod` は数値表記（`640` のような3桁の8進数）とシンボル表記（`u=rw,g=r,o=`）のどちらでも指定できる。
数値表記は r=4、w=2、x=1 の合計値で各枠を表す。

**umask**は、新規作成されるファイルやディレクトリの既定権限から、どのビットを落とすかを決めるマスクである。
`umask 027` を設定すると、以降に作成するファイルはグループの書き込みとその他の全権限が既定で落ちる。

### 3.4 ACLによる拡張

三枠（所有者・グループ・その他）だけでは表現できない権限分けが必要なとき、**ACL（Access Control List）**を使う。

```bash
sudo dnf install -y acl    # 未導入の場合。Ubuntu系は apt install -y acl
setfacl -m u:operator:rw file.txt
setfacl -m g:appadmins:rx /opt/app
getfacl file.txt
setfacl -x u:operator file.txt
```

`getfacl` の出力に `+` が付いたパーミッション表示（`ls -l` の末尾）は、そのファイルにACLエントリが追加されていることを示す。
ACLは強力だが、設定を忘れると後任者が権限構造を追えなくなるため、変更履歴を残す運用が望ましい。

### 3.5 sudoの仕組みと設定

```bash
sudo -l
sudo visudo
```

`sudo -l` は、自分がどのコマンドをどの権限で実行できるかを確認する。
`/etc/sudoers` は直接編集せず、必ず `visudo` を使う。

`visudo` は構文エラーを保存前に検知する仕組みを持つ。
直接エディタで編集して構文を壊すと、sudoそのものが機能しなくなり、管理者への昇格手段を失う。

---

## 4. Windowsでの実現方法

### 4.1 ローカルユーザーとグループ

```powershell
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember -Group 'Administrators'
New-LocalUser -Name 'operator' -Password (Read-Host -AsSecureString) -FullName 'Operator'
Add-LocalGroupMember -Group 'Remote Desktop Users' -Member 'operator'
```

ドメイン環境では `Get-ADUser` などActive Directory向けのコマンドレットを使う（第10章で扱う）。
`Get-LocalUser` はドメインに参加していてもローカルアカウントのみを対象にする。

### 4.2 SIDという識別子

```powershell
whoami /user
whoami /groups
Get-LocalUser operator | Select-Object Name, SID
```

組み込みアカウントには、環境が変わっても値が同じ、よく知られたSID（well-known SID）がある。

| SID | 対応するアカウント |
|-----|---------------------|
| S-1-5-18 | Local System |
| S-1-5-19 | Local Service |
| S-1-5-20 | Network Service |
| S-1-5-32-544 | 組み込みのAdministratorsグループ |

ユーザーのSIDは、アカウント作成時に一意に発行され、アカウントを削除すると再利用されない。
同じ名前でアカウントを作り直しても、SIDが異なれば以前の権限設定は引き継がれない。

### 4.3 NTFSアクセス許可と継承

NTFSは、ACLを使って許可・拒否を細かく設定する。
ディレクトリに設定した権限は、既定で配下のファイルやサブディレクトリへ**継承**される。

```powershell
icacls C:\data
icacls C:\data /grant operator:(OI)(CI)M
Get-Acl C:\data | Format-List
(Get-Acl C:\data).Access
```

> **警告**：`/reset` や範囲指定を誤った `/grant:r` は、既存のACLエントリを丸ごと置き換える。実行前に必ず現状を保存する。

`icacls` の `(OI)(CI)` は、それぞれObject Inherit（ファイルへの継承）とContainer Inherit（サブディレクトリへの継承）を示す。

代表的な権限のイメージは次のとおりである。

| 権限 | 意味の目安 |
|------|------------|
| Read | 読み取り |
| Write | 内容の変更、新規ファイル作成 |
| Modify | Read、Write、削除を含む中間的な権限 |
| Full Control | 権限変更を含む最も強い権限 |
| Read & Execute | 実行を含む読み取り |

拒否（Deny）エントリは、原則として許可（Allow）エントリより優先して評価される。
このため拒否エントリを安易に追加すると、意図しない広範囲でアクセス不能になり、トラブルシュートを難しくする。

### 4.4 UACと管理者権限

**UAC（User Account Control、ユーザーアカウント制御）**は、管理者権限を要する操作の前に昇格確認を挟む仕組みである。

Administratorsグループのメンバーであっても、通常のログオン時に発行されるトークンは権限がフィルタされたもの（filtered token）であり、フル権限のトークンは昇格操作を経て初めて使われる。

```powershell
whoami /priv
```

管理者として起動したPowerShellと、通常権限のPowerShellでは、同じユーザーでも実行できる操作の範囲が異なる。
トラブル対応の初動で「管理者として実行しているか」を確認するのは、この仕組みに由来する。

### 4.5 ローカルセキュリティポリシーとパスワードポリシー

```powershell
secedit /export /cfg C:\temp\secpol.cfg
Get-Content C:\temp\secpol.cfg | Select-String "PasswordComplexity","MinimumPasswordLength"
```

ローカルグループポリシーやセキュリティポリシーで、パスワードの複雑さ、有効期限、アカウントロックアウトのしきい値を設定できる。
ドメイン環境ではグループポリシーオブジェクト（GPO）が優先されることが多く、詳細は第10章と第11章で扱う。

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| 基本モデル | 所有者／グループ／その他＋ACL拡張 | SIDベースのDACL（Discretionary ACL）が基本 |
| 特権アカウント | root（UID 0） | Administrators、SYSTEMなど |
| 日常の昇格 | sudo | UAC昇格、Run as |
| 実行権限の表現 | xビットが明確に分離 | 拡張子とACL、実行ポリシーが絡む |
| 継承の扱い | ACLで個別指定、伝統的権限は継承概念を持たない | NTFS継承が既定で有効 |
| 権限の優先順位 | 所有者→グループ→その他の順で評価（最初に一致した枠を採用） | 明示的な拒否が許可より優先 |
| 識別子 | UID／GID | SID |

同じ目的でも実現方法が異なる例として、「特定グループにだけ読み取りを許可する」を挙げる。

- Linux：グループ所有を対象グループへ揃えて `chmod 640` にするか、`setfacl -m g:group:r` を使う
- Windows：`icacls path /grant "DOMAIN\group:R"` のようにグループへ直接権限を付与する

---

## 6. コマンド例

### 6.1 ユーザー一覧を確認する

**目的**：ローカルに存在するアカウントを洗い出す。

#### Linux

基本構文：

```bash
getent passwd | cut -d: -f1,3,7
```

主要オプション：`getent` はデータベース名（`passwd`、`group` など）を指定して問い合わせる。

実行例：

```bash
getent passwd | cut -d: -f1,3,7 | head
```

想定出力と読み方：

```text
root:0:/bin/bash
operator:1001:/bin/bash
```

コロン区切りの各フィールドは「ユーザー名:UID:ログインシェル」に対応する。
UIDが1000未満は多くのディストリビューションでシステムアカウントを示す。

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

#### Windows

```powershell
Get-LocalUser | Select-Object Name, Enabled, SID
```

ドメイン環境：

```powershell
Get-ADUser -Filter * | Select-Object -First 10 SamAccountName
```

必要な権限：`Get-LocalUser` は一般ユーザーで可。`Get-ADUser` はドメインへの読み取り権限が必要。

誤操作リスク：なし（参照のみ）。

### 6.2 権限を変更する

**目的**：ディレクトリ配下の所有者と権限をまとめて変更する。

> **警告**：再帰的な権限変更は、対象範囲を誤ると広範囲のサービスやアプリが権限エラーで停止する。

#### Linux

```bash
chmod 750 /opt/app
chown -R appuser:appadmins /opt/app
```

主要オプション：`-R` は配下を再帰的に処理する。

必要な権限：対象の所有者、または管理者権限（sudo）。

誤操作リスク：`-R` の対象範囲を誤ると、サービスが自分の設定ファイルを読めなくなる。
事前に `getfacl -R` や `find /opt/app -printf '%m %u %g %p\n'` で現状を保存しておく。

#### Windows

```powershell
icacls C:\app /grant appadmins:(OI)(CI)M /T
```

主要オプション：`/T` は配下を再帰的に処理する。

必要な権限：対象の所有者、または管理者権限。

誤操作リスク：`/T` は広範囲に伝播するため、事前に現状を保存する。

```powershell
icacls C:\app /save C:\temp\acl-app.txt /T
# 復元する場合
# icacls C:\ /restore C:\temp\acl-app.txt
```

### 6.3 今の実効権限を確認する

**目的**：自分（またはプロセス）が実際にどの権限で動いているかを確認する。

#### Linux

```bash
id
sudo -l
namei -l /var/log/app/app.log
```

`namei -l` は、パスの構成要素ごとに権限を一行ずつ表示するため、どの階層でアクセスが拒否されているかを特定しやすい。

必要な権限：一般ユーザーで可。`sudo -l` は自分に許可された昇格範囲のみ表示。

誤操作リスク：なし（参照のみ）。

#### Windows

```powershell
whoami /all
icacls C:\logs\app.log
```

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

### 6.4 グループへユーザーを追加する

**目的**：特定の権限セットをまとめて付与する。

#### Linux

```bash
sudo usermod -aG appadmins operator
groups operator
```

必要な権限：管理者権限（sudo）。

誤操作リスク：`-a` を付け忘れると既存の所属グループが上書きされ、意図せず他のグループから外れる。

#### Windows

```powershell
Add-LocalGroupMember -Group 'appadmins' -Member 'operator'
Get-LocalGroupMember -Group 'appadmins'
```

必要な権限：管理者権限。

誤操作リスク：低い。ただし反映には再ログオンが必要な場合がある。

---

## 7. 実務上の注意点

1. **アプリ専用ユーザーを作る**
   個人アカウントでサービスを動かすと、退職・異動時にサービスごと止まるリスクがある。

2. **権限変更は一件ずつ、前後の状態を保存する**
   `getfacl` や `icacls` の出力を変更前後で保存しておけば、問題発生時に切り戻せる。

3. **ディレクトリの実行ビット／traverseを忘れない**
   「中のファイル権限は正しいのに親ディレクトリに入れない」という事象の多くはここに原因がある。

4. **共有権限とNTFS権限の二重構造を混同しない**
   Windowsのファイル共有には、共有自体の権限とNTFS権限という別々の層があり、両方の積集合が実効権限になる。

5. **サービスアカウントのパスワードローテーションを計画する**
   長期間変更されないサービスアカウントは、侵害後の永続化に使われやすい。

6. **グループの反映タイミングを確認する**
   Linuxは新しいシェルまたは再ログイン、Windowsは再ログオンやトークンの再取得が必要な場合が多い。

---

## 8. セキュリティ上の注意点

1. **777やEveryone: Full Controlを常態化しない**
   一時的な検証で緩めた権限を戻し忘れる事故は多い。

2. **sudoersに`ALL=(ALL) NOPASSWD:ALL`を安易に広げない**
   パスワードなしの全権限昇格は、アカウント侵害の被害を即座に拡大させる。

3. **サービスアカウントに対話ログインを付けない**
   バッチやサービス専用のアカウントは、シェルログインやRDP（Remote Desktop Protocol）ログオンを無効化する。

4. **監査ポリシーを権限変更に合わせて設計する**
   誰が、いつ、どの権限を変更したかを追跡できるようにする（詳細は第11章）。

5. **特権グループのメンバーを定期的に棚卸しする**
   Administrators、Domain Admins、wheel、sudoグループのメンバーは定期的に見直す。

---

## 9. よくある障害

| 症状 | 起きやすい原因 |
|------|----------------|
| Permission denied | 主体の勘違い、パス上のディレクトリ権限不足、SELinux/AppArmorなどの追加制御 |
| Access is denied | UACによるトークン制限、ACL不足、継承切れ、共有権限の制約 |
| sudoが使えなくなった | sudoersの構文破損、対象ユーザーがsudoグループから外れた |
| グループに追加したのに反映されない | 再ログインしていない、プライマリグループの誤解、トークンの未更新 |
| ACL変更後にアプリが動かない | サービスアカウントの権限を誤って除外した、継承の無効化 |

---

## 10. 切り分け手順

権限障害は「誰で動いているか」の確認から始め、経路上の各階層、拡張制御の順に絞り込む。

### 手順A：主体の確認

1. `id` または `whoami /all` で、実行中の主体とその所属グループを確認する
2. サービスの場合、サービス起動アカウントを個別に確認する

### 手順B：経路上の権限確認

**Linux**

1. `namei -l` でパスの各階層の権限を確認する
2. 対象ファイルの所有者、グループ、rwxを確認する
3. ACLが付いていないか `getfacl` で確認する

**Windows**

1. `icacls` または `Get-Acl` で対象の権限を確認する
2. 継承が有効かどうかを確認する
3. 拒否エントリが存在しないかを確認する

### 手順C：追加のアクセス制御

1. LinuxはSELinuxまたはAppArmorの拒否ログを確認する（`ausearch`、`journalctl` など）
2. WindowsはUACの昇格状態、グループポリシーによる制限を確認する

### 手順D：復旧手段の確保

1. sudoやAdministratorsが機能しない場合の代替復旧手段（コンソールアクセス、セーフモード、クラウドのroot/管理者リセット機能）を事前に把握しておく

元に戻す方法の原則：

- 権限調査中の一時的な変更は、変更前の値を必ず記録してから行う
- 検証はラボ環境で行い、本番では既存のACL/権限をバックアップしてから変更する
- 昇格系の設定（sudoers、Administratorsメンバー）の変更は、必ず他の管理経路を残した状態で行う

---

## 11. 章末問題

### 問題1

UID 0が持つ特別な意味を述べよ。

### 問題2

ディレクトリにxビットが必要な理由を、traverseという言葉を使って説明せよ。

### 問題3

UACが存在することで、Administratorsグループのメンバーであっても得られる利点は何か。

### 問題4

NTFSの継承を無効化したディレクトリで起きやすい運用事故を一つ挙げよ。

### 問題5

最小権限の原則に反する運用例を一つ挙げよ。

### 問題6

Linuxで `setfacl` を使う場面と、伝統的な `chmod` だけで足りる場面の違いを述べよ。

---

## 12. 解答と解説

### 問題1

root特権ユーザーであることを示す。
多くの権限チェックを実質的にバイパスできるため、直接ログインを避け、sudo経由での限定的な昇格が推奨される。

### 問題2

ディレクトリへ「入る」ためにxビットが必要である。
xが無いと、たとえ配下のファイルに読み取り権限があっても、そこへ到達（traverse）できない。

### 問題3

マルウェアや誤操作がログオン直後の通常権限で動くため、意図しない特権操作が即座には実行されない。
昇格には明示的な確認操作が挟まる。

### 問題4

上位ディレクトリでの権限変更が配下へ伝播せず、一部のファイルだけ古い権限のまま残る事故が起きやすい。

### 問題5

例：全社員にDomain Adminsを付与する、アプリケーションをroot権限で常時実行する。

### 問題6

三枠（所有者・グループ・その他）で表現できる範囲なら `chmod` で十分である。
複数の異なるユーザーやグループへ個別に異なる権限を割り当てたい場合は、ACL（`setfacl`）が必要になる。

---

## 13. ハンズオン演習

### 演習4-1 専用グループとアプリ用ディレクトリの作成

**前提条件**

- sudoまたは管理者権限がある
- ラボ環境でスナップショットを取得済みであることが望ましい

**実行内容（Linux）**

```bash
sudo groupadd labops
sudo useradd -m -s /bin/bash -G labops labuser || sudo usermod -aG labops labuser
id labuser
sudo mkdir -p /opt/labdata
echo data | sudo tee /opt/labdata/readme.txt
sudo chown root:labops /opt/labdata /opt/labdata/readme.txt
sudo chmod 750 /opt/labdata
sudo chmod 640 /opt/labdata/readme.txt
```

**実行内容（Windows）**

```powershell
New-LocalGroup -Name labops -ErrorAction SilentlyContinue
New-LocalUser -Name labuser -Password (Read-Host 'Password' -AsSecureString) -ErrorAction SilentlyContinue
Add-LocalGroupMember -Group labops -Member labuser
New-Item -ItemType Directory -Path C:\labdata -Force
'data' | Out-File C:\labdata\readme.txt
icacls C:\labdata /inheritance:r
icacls C:\labdata /grant:r Administrators:F
icacls C:\labdata /grant labops:R
```

**確認方法**

- `labuser`（または対応するWindowsアカウント）でログインし、対象ファイルが読み取れることを確認する
- labops以外のユーザーではアクセスできないことを確認する

**元に戻す方法**

```bash
sudo userdel -r labuser
sudo groupdel labops
sudo rm -rf /opt/labdata
```

```powershell
Remove-LocalUser -Name labuser
Remove-LocalGroup -Name labops
Remove-Item -Recurse -Force C:\labdata
```

### 演習4-2 権限エラーの再現と解消

**前提条件**：演習4-1の環境が残っている。

**実行内容**

1. わざと対象ユーザーをグループから外し、読めなくなることを確認する
2. グループへ戻し、読めるようになることを確認する
3. 前後の `id` / `whoami` / `getfacl` / `icacls` の出力を保存する

**確認方法**：グループ除外時に Permission denied（または Access is denied）が発生し、復帰後に解消することを確認する。

**元に戻す方法**：演習4-1の元に戻す方法と同じ手順を実行する。

---

## 14. 本章のまとめ

権限は、表示上の名前ではなく、UID/GIDやSIDと、それらに紐づくACLの評価結果である。
Linuxは所有者・グループ・その他の三枠を基本に、必要に応じてACLで拡張する。
Windowsは最初からSIDベースのACLを基本に、UACという昇格の仕組みを組み合わせる。

次章では、その主体として実際に動くプロセスと、それを管理するサービスの仕組みを扱う。

次章: [第5章 プロセスとサービス](05_processes_and_services.md)


---


<!-- source: 05_processes_and_services.md -->

# 第5章 プロセスとサービス

CPUが高い、ポートが開かない、再起動したらアプリが戻らない。
現場からの問い合わせの多くは、プロセスの状態と、サービスとしての自動起動設定に帰着する。

プロセスは「今動いているもの」、サービスは「起動方法と寿命を管理する仕組み」であり、この二つを分けて考えると調査が速くなる。
手動で起動したプロセスがサービスとして登録されていなければ、再起動後に戻らないのは設定不足ではなく、そもそも登録されていないことが原因になる。

---

## 1. 学習目標

本章を終えると、次ができるようになる。

1. プロセスの状態、PID（Process ID）、親子関係、ジョブ制御、シグナルを説明できる
2. systemdユニットの起動・停止・自動起動設定と、journalの見方を使える
3. WindowsのService Control Manager（SCM）とPowerShellによるサービス管理を使える
4. 自動起動の有無を両OSで確認・変更できる
5. ハングと高負荷の初動調査を両OSで実行できる

---

## 2. 基本概念

### 2.1 プロセスの識別と状態

**プロセス（process）**は、実行中のプログラムの実体である。
各プロセスには一意の**PID（Process ID）**が割り当てられ、OSはPID単位で資源とスケジューリングを管理する。

Linuxの `ps` コマンドで見る代表的な状態は次のとおりである。

| 状態 | 意味の目安 |
|------|------------|
| R（Running） | 走行中、または走行待ち |
| S（Sleeping） | 割り込み可能なスリープ（イベント待ち） |
| D（Uninterruptible Sleep） | 不可分スリープ。I/O待ちで、シグナルでも中断できないことが多い |
| T（Stopped） | ジョブ制御などで停止中 |
| Z（Zombie） | 終了したが、親プロセスが終了ステータスを回収（wait）していない |

Windowsのプロセスにも稼働中・一時停止・終了処理中といった状態はあるが、Linuxほど詳細な状態記号を日常的に参照することは少なく、応答の有無（Responding / Not Responding）で観察することが多い。

### 2.2 親子関係とプロセスツリー

Linuxのプロセスは、必ず親プロセスを持つ（最上位のPID 1を除く）。
親のPID（PPID: Parent Process ID）をたどれば、どのプロセスがどこから起動されたかを追跡できる。

Windowsにも親プロセスIDの概念はあるが、親プロセスが終了しても子プロセスの追跡情報（ParentProcessId）は残り続ける点がLinuxと異なる。
つまりWindowsでは、表示されているParentProcessIdの親プロセスがすでに存在しない、という状況が起こりうる。

### 2.3 サービスとは何か

**サービス**は、バックグラウンドで常駐し、システムやネットワークからの要求に応えるプロセスを、起動方法・依存関係・再起動方針込みで管理する単位である。

- Linux（systemd）：**ユニット（unit）**、特に `.service` ユニット
- Windows：**サービス（service）**、Service Control Manager（SCM）が管理

サービスという概念があることで、単なる「起動しているプロセス」以上の情報（自動起動するか、失敗時に再起動するか、何に依存しているか）をOSが一元管理できる。

### 2.4 自動起動という別軸

「今動いているか」と「次回起動時にも動くか」は別の軸である。
プロセスを手動で起動しただけでは、サービスとして登録・有効化されていない限り、再起動後には戻らない。

障害対応では、この二つを混同して「起動できたから直った」と判断すると、次回の再起動で同じ問題が再発する。

---

## 3. Linuxでの実現方法

### 3.1 プロセスの観察

```bash
ps -ef
ps -eo pid,ppid,user,stat,%cpu,%mem,cmd --sort=-%cpu | head
top
```

`ps -ef` はすべてのプロセスをフルフォーマットで表示する。
`--sort=-%cpu` はCPU使用率降順に並べ替える指定であり、高負荷調査の定番になる。
`top` は対話的にリアルタイム更新される一覧を表示し、`htop` が導入されていればより視覚的に確認できる。

### 3.2 ジョブ管理とシグナル

対話シェルでは、`Ctrl+Z` でジョブを停止し、`bg` で背景実行へ切り替え、`fg` で前面に戻せる。
`&` を末尾に付けて実行すると、最初から背景実行になる。

**シグナル（signal）**は、プロセスへ送る非同期の通知である。

| シグナル | 番号 | よく使う意味 |
|----------|------|--------------|
| HUP | 1 | ハングアップ。設定再読み込みに使う流儀もある |
| INT | 2 | 割り込み（Ctrl+C相当） |
| TERM | 15 | 優雅な終了依頼。既定のシグナル |
| KILL | 9 | 強制終了。プロセス側で捕捉・無視できない |

```bash
kill -TERM <PID>
kill -HUP <PID>
# 警告: kill -9 は最終手段。後始末の機会を奪い、データ不整合や一時ファイル残留を招く
kill -KILL <PID>
```

TERMはプロセスが自身の終了処理（ファイルのクローズ、ロックの解放など）を行う機会を与える。
KILLはカーネルが即座にプロセスを消去するため、後始末の余地がない。

### 3.3 systemd／systemctl／journalctl

**systemd**は、多くの現代的なLinuxディストリビューションで採用されているPID 1（init）の実装であり、サービスの起動・依存関係・ログ収集を統合的に扱う。

```bash
systemctl status sshd || systemctl status ssh
systemctl list-units --type=service --state=failed
```

サービスの操作：

```bash
# 警告: 本番稼働中のサービス停止は業務影響が出る
sudo systemctl stop sshd
sudo systemctl start sshd
sudo systemctl restart sshd
sudo systemctl reload sshd
sudo systemctl enable sshd
sudo systemctl disable sshd
systemctl is-enabled sshd
systemctl is-active sshd
systemctl cat sshd
```

`restart` は一度完全に停止してから起動し直すのに対し、`reload` は多くのサービスで無停止のまま設定を再読み込みする。
`enable`/`disable` は自動起動の有無を切り替えるだけで、現在の稼働状態には影響しない。

ログの確認：

```bash
journalctl -u sshd -n 50 --no-pager
journalctl -b -p err --no-pager | head
journalctl --since "1 hour ago" -u sshd
```

`journalctl -u` はユニット単位でログを絞り込む。
`-p err` は優先度がエラー以上のログに絞る。
`--since` は時間範囲での絞り込みに使い、障害発生時刻付近のログを効率よく抽出できる。

### 3.4 プロセスとユニットの対応関係を確認する

```bash
systemctl status sshd
ps -ef | grep sshd
systemd-cgls
```

`systemctl status` の出力にはPIDと直近のログ数行が含まれるため、単独の `ps` より状況把握が速いことが多い。
`systemd-cgls` はcgroup（コントロールグループ）階層を表示し、あるユニットに属する全プロセスを確認できる。

---

## 4. Windowsでの実現方法

### 4.1 プロセスの観察

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
Get-CimInstance Win32_Process |
  Select-Object ProcessId, ParentProcessId, Name, CommandLine |
  Where-Object { $_.Name -match 'svchost|nginx|httpd|w3wp' }
```

`Get-Process` は稼働中のプロセスをオブジェクトとして返し、CPU時間やメモリ使用量でソートできる。
`Get-CimInstance Win32_Process` は `Get-Process` より多くの情報（親プロセスID、コマンドライン全体）を持つが、取得がやや遅い。

タスクマネージャーはGUIの入口として併用する。
「詳細」タブでコマンドラインや親プロセスを表示させる設定に変更しておくと、CLIとの相互確認がしやすい。

### 4.2 プロセスの停止

```powershell
Stop-Process -Id <PID> -Confirm
Stop-Process -Name notepad -ErrorAction SilentlyContinue
```

> **警告**：`-Force` は最終手段である。対話的な確認を省略し、保存されていないデータの喪失につながることがある。

```powershell
Stop-Process -Name notepad -Force -ErrorAction SilentlyContinue
```

### 4.3 Service Control ManagerとPowerShell

**Service Control Manager（SCM）**は、サービスの登録、開始、停止、失敗時の動作方針を一元管理するWindowsのコンポーネントである。

```powershell
Get-Service | Where-Object Status -ne 'Running' | Select-Object -First 20
Get-Service wuauserv | Format-List *
```

サービスの操作：

```powershell
Start-Service wuauserv
Stop-Service wuauserv -Force
Restart-Service wuauserv
Set-Service wuauserv -StartupType Automatic
Set-Service wuauserv -StartupType Manual
Set-Service wuauserv -StartupType Disabled
Get-Service wuauserv | Select-Object Name, Status, StartType
```

`StartType` には Automatic、Manual、Disabled のほか、`Automatic (Delayed Start)` という遅延自動開始もある。
起動直後の輻輳を避けたいサービスに使われる。

従来の `sc.exe` も、より詳細な設定確認に使われる。

```powershell
sc.exe qc wuauserv
sc.exe query wuauserv
sc.exe queryex wuauserv
```

失敗時の再起動方針も設定できる。

```powershell
sc.exe failure wuauserv reset= 86400 actions= restart/60000/restart/60000/""/0
```

### 4.4 サービス失敗のイベント確認

```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; ProviderName='Service Control Manager'} -MaxEvents 20
```

SCM関連のイベントはSystemログに記録される。
サービスが起動直後に落ちる場合、このログと、サービス自身が出すApplicationログの両方を確認する。

### 4.5 タスクマネージャーとリソースモニター

GUIでの確認手段として、タスクマネージャーの「パフォーマンス」タブと、リソースモニター（`resmon`）がある。
CLIでの数値確認と、GUIでの傾向把握を組み合わせると、単発の高負荷か継続的な高負荷かを見分けやすい。

```powershell
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5
```

`Get-Counter` はパフォーマンスカウンターを取得するコマンドレットであり、継続的な傾向をスクリプトで記録したいときに使う。

---

## 5. 両OSの比較

| 目的 | Linux | Windows |
|------|-------|---------|
| プロセス一覧 | `ps`、`top` | `Get-Process`、タスクマネージャー |
| サービス状態 | `systemctl status` | `Get-Service` |
| 開始／停止 | `systemctl start`／`stop` | `Start-Service`／`Stop-Service` |
| 自動起動設定 | `enable`／`disable` | `Set-Service -StartupType` |
| ログ | `journalctl -u` | イベントログ（System、Application） |
| 強制終了 | `kill -9` | `Stop-Process -Force` |
| 失敗時再起動 | ユニットファイルの`Restart=`設定 | `sc.exe failure` |
| 親子関係の追跡 | PPIDが常に有効 | ParentProcessIdは親終了後も残存しうる |

自動起動の考え方は両OSで似ているが、粒度が異なる。
systemdは `enable` するだけで多くの依存関係を自動解決するのに対し、Windowsサービスは `StartupType` に加え、依存サービス（`DependentServices`）を個別に確認する必要がある場面がある。

---

## 6. コマンド例

### 6.1 サービスを起動する

**目的**：停止しているサービスを起動し、稼働状態を確認する。

#### Linux

基本構文：

```bash
sudo systemctl start nginx
systemctl is-active nginx
```

主要オプション：`start`は今すぐの起動、`enable`は自動起動の登録であり、両者は別操作である。

実行例：

```bash
sudo systemctl start nginx
systemctl is-active nginx
systemctl status nginx --no-pager
```

想定出力と読み方：`is-active` は `active` または `inactive`、`failed` などの状態文字列を1行返す。
スクリプトでの条件分岐に使いやすい。

必要な権限：root相当（sudo）。

誤操作リスク：設定ファイルに誤りがあると、起動直後にエラー応答や高負荷につながることがある。

#### Windows

```powershell
Start-Service W3SVC
Get-Service W3SVC
```

必要な権限：管理者権限。

誤操作リスク：依存サービスを巻き込んで一緒に起動・停止することがある。
`Get-Service W3SVC | Select-Object -ExpandProperty DependentServices` で事前確認する。

### 6.2 サービスを止める（危険操作）

**目的**：不要または異常なサービスを停止する。

> **警告**：本番稼働中のサービス停止は、依存する他サービスやアプリの障害につながる。事前に影響範囲を確認する。

#### Linux

```bash
sudo systemctl stop nginx
```

必要な権限：root相当。

誤操作リスク：SSH（Secure Shell）サービス自体を誤って停止すると、リモート接続そのものが切断される。

#### Windows

```powershell
Stop-Service W3SVC -Force
```

必要な権限：管理者権限。

誤操作リスク：RDP（Remote Desktop Protocol）のサービスを誤って止めると、リモート接続が切断される。

### 6.3 待ち受けプロセスの入口

**目的**：どのプロセスがどのポートを使っているかを確認する。

```bash
ss -tulpn | head
```

```powershell
Get-NetTCPConnection -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess |
  Sort-Object LocalPort
```

必要な権限：一般ユーザーでも多くの情報を確認できるが、他ユーザーのプロセス詳細は制限される場合がある。

誤操作リスク：なし（参照のみ）。詳細は第7章のネットワーク管理で扱う。

### 6.4 高CPUプロセスを特定する

**目的**：CPU使用率上位のプロセスとその実行コマンドを特定する。

```bash
ps -eo pid,user,%cpu,%mem,cmd --sort=-%cpu | head -n 15
```

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 15 Id, ProcessName, CPU, WorkingSet
```

想定出力と読み方：Linuxの `%CPU` は複数コアを考慮すると100%を超えることがある（マルチスレッド利用時）。
Windowsの `CPU` 列は起動からの累積CPU時間（秒）であり、瞬間値ではない点に注意する。

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

### 6.5 自動起動設定を変更する

**目的**：再起動後にサービスが自動で立ち上がるようにする、または止める。

```bash
sudo systemctl enable nginx
sudo systemctl disable nginx
systemctl is-enabled nginx
```

必要な権限：root相当。

誤操作リスク：無効化した重要サービス（sshdなど）を戻し忘れると、次回再起動時に接続手段を失う。

```powershell
Set-Service W3SVC -StartupType Automatic
Set-Service W3SVC -StartupType Disabled
Get-Service W3SVC | Select-Object StartType
```

必要な権限：管理者権限。

誤操作リスク：Linuxと同様、リモート管理系サービスの無効化には特に注意する。

---

## 7. 実務上の注意点

1. **手動起動と自動起動を混同しない**
   実際に再起動試験を行い、意図した挙動になっているかを確認する。

2. **依存関係をサービス定義側で持つ**
   「データベースが先、アプリが後」のような順序性は、起動スクリプトではなくユニットやサービスの依存設定で表現する。

3. **安易に強制終了しない**
   まずログ、設定、ディスク空き容量を確認し、それでも応答しない場合にTERM、さらに応答しなければKILLへ進む。

4. **コンテナやオーケストレータ配下では別の管理層がある**
   ホストの `systemctl` だけでは、コンテナ内プロセスの状態を正確に把握できない。

5. **再起動試験を定期的に行う**
   長期間再起動していないサーバーは、設定変更が反映されない状態で自動起動設定が壊れていることに気づきにくい。

6. **PIDだけでなく開始時刻もセットで記録する**
   同じPIDが別プロセスに再利用されることがあるため、開始時刻と合わせて記録する。

---

## 8. セキュリティ上の注意点

1. **不要サービスは停止し、自動起動を無効化する**
   攻撃対象領域（アタックサーフェス）を減らす基本策になる。

2. **サービスアカウントは最小権限にする**
   root/SYSTEM権限で動かす必要が本当にあるかを都度確認する。

3. **書き込み可能なディレクトリから高権限サービスを実行しない**
   一般ユーザーが書き換え可能なパスの実行ファイルを高権限サービスが呼ぶと、権限昇格の足がかりになる。

4. **クラッシュループを放置しない**
   失敗時の自動再起動が繰り返される状態は、攻撃や設定ミスの兆候であり、そのまま放置すると調査の手がかりを失う。

5. **サービスの実行ファイルパスを監視する**
   正規のパスに見えて別の実行ファイルへ差し替えられていないかを、ハッシュ値や署名で確認する。

---

## 9. よくある障害

| 症状 | 起きやすい原因 |
|------|----------------|
| サービスが起動しない | 設定ファイルの構文誤り、依存サービス未起動、ポート競合、権限不足 |
| 起動するがすぐ落ちる | 終了コード異常、必須ファイルの欠落、権限不足 |
| CPU使用率が高止まりする | 無限ループ、想定外の高負荷リクエスト、バックアップ処理の二重実行 |
| プロセスが応答しない（ハング） | D状態やディスク待ち、ロック競合、デッドロック、アプリ側のフルGC（ガベージコレクション） |
| ゾンビプロセスが増え続ける | 親プロセスが子の終了をwaitしていない実装上の不備 |

---

## 10. 切り分け手順

サービス障害は、まず状態を確認し、次にログ、依存関係、資源競合の順に絞り込む。

### 手順A：サービス状態の確認

**Linux**

```bash
systemctl status <name> -l
systemctl is-failed <name>
```

**Windows**

```powershell
Get-Service <name> | Format-List *
```

### 手順B：ログの確認

**Linux**

```bash
journalctl -u <name> -b --no-pager
```

**Windows**

```powershell
Get-WinEvent -LogName Application -MaxEvents 50 |
  Where-Object { $_.LevelDisplayName -eq 'Error' }
```

### 手順C：依存関係と起動順序

1. 依存するサービス（データベース、認証基盤など）が先に起動しているかを確認する
2. Linuxは `systemctl list-dependencies <name>`、Windowsは `Get-Service <name> | Select-Object -ExpandProperty ServicesDependedOn` で確認する

### 手順D：資源とプロセスの状態

1. CPU、メモリ、ディスクI/Oの飽和を確認する
2. 上位プロセスのPIDと開始時刻を記録する
3. Linuxは `systemd-analyze blame` で起動時間の内訳を確認する

```bash
systemd-analyze blame | head
```

元に戻す方法の原則：

- サービス停止は、依存する他サービスへの影響を確認してから行う
- 設定変更は一件ずつ行い、変更前の設定ファイルやレジストリ値を保存する
- 自動起動設定を変更した場合は、再起動試験まで含めて検証する

---

## 11. 章末問題

### 問題1

`kill -9` を最初の選択肢にしない理由を述べよ。

### 問題2

`systemctl enable` と `systemctl start` の違いを述べよ。

### 問題3

Windowsサービスの `StartType` が `Manual` のとき、再起動後にそのサービスはどうなるか。

### 問題4

ゾンビプロセスが示す問題の本質はどこにあるか。

### 問題5

SCM関連の失敗を追うとき、まず確認すべきログはどれか。

### 問題6

D状態のプロセスにTERMシグナルを送っても反応しないことがある理由を述べよ。

---

## 12. 解答と解説

### 問題1

TERMと違い、KILLはプロセスに後始末の機会を与えない。
データ不整合や一時ファイルの残留を招く可能性があるため、まずTERMを試し、それでも終了しない場合の最終手段としてKILLを使う。

### 問題2

`enable` は次回起動時に自動的に開始されるよう登録する操作であり、`start` は現在の状態にかかわらず今すぐ開始する操作である。
どちらか一方だけでは、意図した挙動にならないことがある。

### 問題3

自動では起動しない。
手動での起動操作、または他のサービスからの依存関係による起動を待つ状態のままになる。

### 問題4

親プロセスが子プロセスの終了ステータスをwaitで回収していないことが本質的な原因である。

### 問題5

Systemログの Service Control Manager プロバイダーによるイベントを確認する。

### 問題6

D状態は不可分スリープであり、多くの場合カーネル内部のI/O待ちに入っている。
シグナルの配送はユーザー空間へ戻るタイミングで処理されるため、I/Oが完了するまでシグナルへ応答できない。

---

## 13. ハンズオン演習

### 演習5-1 一時プロセスの起動とシグナルによる停止

**前提条件**：LinuxとWindowsの両方に一般ユーザーでログインできる。

**実行内容（Linux）**

```bash
sleep 600 &
PID=$!
ps -o pid,ppid,stat,cmd -p $PID
kill -TERM $PID
```

**実行内容（Windows）**

```powershell
$p = Start-Process powershell -ArgumentList '-NoExit','-Command','Start-Sleep -Seconds 600' -PassThru
Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)" |
  Select-Object ProcessId, ParentProcessId, Name
Stop-Process -Id $p.Id
```

**確認方法**：シグナル送信後、プロセスが一覧から消えていることを確認する。

**元に戻す方法**：起動した一時プロセスは本演習内で終了済みのため、追加の後始末は不要である。

### 演習5-2 サービスの起動・停止・自動起動設定の確認

> **警告**：SSHやRDPなど、現在の接続に使っているサービス自体は止めない。ラボ専用のWebサーバーやテスト用サービスを対象にする。

**前提条件**：ラボに `nginx`／`httpd` に相当するテスト用サービスが導入済みであること。

**実行内容（Linux）**

```bash
sudo systemctl status nginx || sudo systemctl status httpd
sudo systemctl restart nginx || sudo systemctl restart httpd
systemctl is-enabled nginx || systemctl is-enabled httpd
```

**実行内容（Windows）**

```powershell
Get-Service | Where-Object Name -match 'W3SVC|Spooler' | Format-Table Name, Status, StartType
```

**確認方法**：`restart` 後にサービスが `active`／`Running` に戻っていることを確認する。

**元に戻す方法**：意図的に変更した `StartType` や `enable`／`disable` は演習前の値に戻す。

### 演習5-3 失敗ユニット／停止サービスの洗い出し

**実行内容（Linux）**

```bash
systemctl --failed
```

**実行内容（Windows）**

```powershell
Get-Service | Where-Object Status -eq 'Stopped' | Where-Object StartType -eq 'Automatic'
```

**確認方法**：自動起動のはずが停止しているサービスをリストし、そのうち一件のログを確認する。

**元に戻す方法**：調査目的の参照のみであり、変更は発生しない。

---

## 14. 本章のまとめ

プロセスは今この瞬間の実行状態を表し、サービスは寿命と自動起動を含めた管理単位を表す。
LinuxはPID、PPID、シグナル、systemdユニットという体系で、WindowsはプロセスID、Service Control Manager、StartTypeという体系で、同じ目的を別々の部品で実現している。

次章では、そのプロセスが読み書きするストレージ側の仕組みを扱う。

次章: [第6章 ストレージとファイルシステム](06_storage_and_filesystems.md)


---


<!-- source: 06_storage_and_filesystems.md -->

# 第6章 ストレージとファイルシステム

ディスクが満杯になった、inodeが枯渇した、拡張したのにマウントできない。
ストレージ障害はアプリケーションのログだけでは原因が見えないことが多く、ブロックデバイスからファイルシステムまでの層を一段ずつ確認する必要がある。

ストレージは、物理的なディスクという実体と、その上にパーティション、ファイルシステム、マウントという論理的な層を積み重ねた構造を持つ。
どの層で問題が起きているかを特定できないまま設定を変更すると、原因を悪化させることがある。

---

## 1. 学習目標

本章を終えると、次ができるようになる。

1. ブロックデバイス、パーティション、MBR（Master Boot Record）/GPT（GUID Partition Table）の役割を説明できる
2. ext4/XFSとNTFS/ReFSの用途の違いを概説できる
3. LinuxのマウントとfstabとLVM（Logical Volume Manager）、Windowsのディスクの管理とStorage Spacesの基本操作ができる
4. 容量、inode、クォータを両OSで確認できる
5. ディスク拡張の手順と、ストレージ障害の初動調査ができる

---

## 2. 基本概念

### 2.1 ブロックデバイス

**ブロックデバイス（block device）**は、固定長のブロック単位で読み書きする記憶装置の抽象である。
HDD（Hard Disk Drive）、SSD（Solid State Drive）、仮想ディスク、ネットワーク越しのLUN（Logical Unit Number）などが、OSからはブロックデバイスとして見える。

ブロックデバイスは、それ単体ではまだ「ファイル」という概念を持たない。
その上にパーティションとファイルシステムを載せて初めて、名前付きのファイルを扱えるようになる。

### 2.2 パーティションとパーティションテーブル

ディスクを論理的に区切る仕組みが**パーティション（partition）**であり、その区切り方を記録する表がパーティションテーブルである。

| 方式 | 特徴 |
|------|------|
| **MBR（Master Boot Record）** | 古い形式。ディスク容量2TiBまで、基本パーティション数4個までという制約がある |
| **GPT（GUID Partition Table）** | 現代の標準。大容量ディスクと多数のパーティションに対応し、パーティション情報の冗長化も持つ |

UEFI（Unified Extensible Firmware Interface）起動とGPTの組み合わせが、現在のサーバー・クライアント双方で主流になっている。

### 2.3 ファイルシステムの種類

**ファイルシステム（file system）**は、ブロックデバイス上の領域に、名前付きのファイルとディレクトリという構造を与える仕組みである。

| ファイルシステム | 主な環境 | 特徴 |
|------------------|----------|------|
| ext4 | Linux汎用 | 実績が長く、安定した既定選択肢 |
| XFS | RHEL系でルートにも採用例が多い | 大容量、高い並列I/O性能に強み |
| NTFS | Windows標準 | ACL、圧縮、暗号化（EFS）、ジャーナリングに対応 |
| ReFS（Resilient File System） | Windows Serverなど | データ破損への耐性を重視。用途はバージョンや構成に依存 |

ファイルシステムが管理する情報は、ファイル本体のデータだけではない。
所有者、権限、サイズ、タイムスタンプ、リンク情報といったメタデータ、ディレクトリという名前と実体の対応表、空き領域の管理情報もあわせて持つ。

### 2.4 マウントとドライブレター

Linuxは、ファイルシステムをディレクトリへ**マウント（mount）**して接続する。
既存の単一ディレクトリツリーへ、新しい区画を挿し木のようにつなぐ発想である。

Windowsは、ボリュームへドライブレター（`C:` など）を割り当てるか、既存のNTFSフォルダーへマウントポイントとして接続する。
既定の運用はドライブレター方式であり、フォルダーマウントは特定用途で使われる。

### 2.5 LVMとStorage Spaces

複数の物理ディスクをまとめてプールし、そこから必要なサイズの論理ボリュームを切り出す、という発想は両OSに共通する。

- **LVM（Logical Volume Manager）**：Linuxで標準的に使われる論理ボリューム管理の仕組み
- **Storage Spaces**：Windowsのソフトウェア定義ストレージ機能。ミラーやパリティによる冗長化を選べる

どちらも、物理ディスクの追加・交換をアプリケーションから隠蔽し、運用上の柔軟性を高める狙いを持つ。

### 2.6 inodeとメタデータ管理

Linuxのファイルシステムは、ファイルのメタデータを**inode**という管理構造に格納する。
ディスクの空き容量が十分にあっても、inodeの数が足りなくなると新規ファイルを作成できなくなる。

Windowsにも同様のメタデータ管理構造(NTFSのMFT: Master File Table)が存在するが、運用上「容量はあるのに作成できない」という形で問題が顕在化する頻度は、Linuxのinode枯渇ほど話題にならない。

### 2.7 クォータという考え方

**クォータ（quota）**は、ユーザーやグループ、ディレクトリ単位で使用できる容量やファイル数の上限を設ける仕組みである。
共有環境で特定の利用者が容量を占有し、他の利用者に影響することを防ぐ目的で使われる。

---

## 3. Linuxでの実現方法

### 3.1 デバイスの確認

```bash
lsblk -f
sudo fdisk -l
sudo ls -l /dev/sd* /dev/nvme* /dev/vd* 2>/dev/null
```

`lsblk -f` はブロックデバイスの階層とファイルシステム種別、UUIDを一覧表示する。
仮想化環境では、準仮想化ドライバー（VirtIOなど）を使う構成で `/dev/vd*`、Xen系で `/dev/xvd*` のような名前になる。

### 3.2 パーティションとファイルシステムの作成

> **警告**：パーティション操作とフォーマットはデータ消失に直結する。対象デバイス名を必ず複数回確認し、ラボ環境以外では十分な検証を経てから実行する。

```bash
sudo parted /dev/sdb print
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary 0% 100%
sudo mkfs.xfs /dev/sdb1
# または
sudo mkfs.ext4 /dev/sdb1
```

`parted` はGPT/MBR双方を扱えるパーティション編集ツールである。
`mkfs.xfs` や `mkfs.ext4` は、パーティション上にファイルシステムの構造を書き込む操作であり、既存データを消去する。

### 3.3 マウントとfstab

```bash
sudo mkdir -p /data
sudo mount /dev/sdb1 /data
findmnt /data
df -hT /data
```

再起動後も自動的にマウントされるようにするには、**`/etc/fstab`**へ設定を追記する。
デバイス名（`/dev/sdb1`）は環境によって変わりうるため、UUIDでの指定が推奨される。

```bash
blkid /dev/sdb1
echo 'UUID=xxxx-xxxx /data xfs defaults 0 2' | sudo tee -a /etc/fstab
```

> **警告**：fstabの記述誤りは、次回起動時のemergencyモード突入という定番の障害原因になる。追記後は必ず試験する。

```bash
sudo findmnt --verify
sudo mount -a
```

`mount -a` はfstabに書かれた未マウントのエントリをすべてマウントし、記述誤りがあればこの時点でエラーとして検出できる。

### 3.4 LVMの基本操作

```bash
sudo pvcreate /dev/sdb
sudo vgcreate vgdata /dev/sdb
sudo lvcreate -n lvdata -L 10G vgdata
sudo mkfs.xfs /dev/vgdata/lvdata
sudo mkdir -p /data
sudo mount /dev/vgdata/lvdata /data
```

LVMは、物理ボリューム（PV: Physical Volume）、ボリュームグループ（VG: Volume Group）、論理ボリューム（LV: Logical Volume）という三層構造を持つ。
物理ディスクを直接パーティション分割するのではなく、いったんVGへプールしてからLVを切り出すため、後からの拡張が容易になる。

拡張の例：

```bash
sudo lvextend -L +5G /dev/vgdata/lvdata
sudo xfs_growfs /data
# ext4の場合は resize2fs を使う
# sudo resize2fs /dev/vgdata/lvdata
```

`lvextend` は論理ボリュームのサイズを広げるだけであり、ファイルシステム自体を広げる `xfs_growfs`（XFS用）または `resize2fs`（ext4用）を別途実行する必要がある。
この二段階を混同すると、「LVMは拡張したのに `df` の容量が変わらない」という事象になる。

### 3.5 容量とinodeの確認

```bash
df -h
df -i
du -sh /var/* 2>/dev/null | sort -h | tail
```

`df -h` は容量、`df -i` はinode使用状況を表示する。
**inode**が枯渇すると、容量に余裕があってもファイル作成が `No space left on device` で失敗する。
小さいファイルを大量に生成するワークロード（メールスプール、コンテナのレイヤーキャッシュ、セッションファイルなど）で発生しやすい。

### 3.6 クォータの設定概要

ユーザー・グループ単位のクォータは、ファイルシステム側でクォータ機能を有効化し、専用ツールで上限を設定する。

```bash
# 例: ext4でのユーザークォータ有効化の流れ（詳細はディストリビューションの手順に従う）
sudo mount -o remount,usrquota,grpquota /data
sudo quotacheck -cug /data
sudo quotaon /data
sudo setquota -u operator 5G 6G 0 0 /data
```

XFSではマウントオプションに `uquota`/`gquota` を指定し、`xfs_quota` コマンドで管理する方式が使われる。
ファイルシステムの種類によって手順が異なるため、対象環境のドキュメントで確認する。

---

## 4. Windowsでの実現方法

### 4.1 ディスク管理の基本操作

```powershell
Get-Disk
Get-Partition
Get-Volume
Get-PhysicalDisk
```

GUIの「ディスクの管理」（diskmgmt.msc）も同様の情報を視覚的に確認できるため、CLIと併用すると理解しやすい。

> **警告**：初期化、パーティション作成、フォーマットは破壊的な操作である。対象ディスク番号を必ず確認する。

```powershell
# 初期化からフォーマットまでの例。対象ディスク番号は Get-Disk で必ず事前確認する
# Initialize-Disk -Number 1 -PartitionStyle GPT
# New-Partition -DiskNumber 1 -UseMaximumSize -AssignDriveLetter |
#   Format-Volume -FileSystem NTFS -NewFileSystemLabel Data
```

### 4.2 Storage Spacesの概要

複数の物理ディスクをプールし、そこから仮想ディスクを切り出す機能である。
ミラー（複製による冗長化）やパリティ（誤り訂正符号による冗長化）など、回復性のレベルを選べる。

```powershell
Get-StoragePool
Get-VirtualDisk
New-StoragePool -FriendlyName "Pool1" -StorageSubsystemFriendlyName "Windows Storage*" -PhysicalDisks (Get-PhysicalDisk -CanPool $true)
```

本番導入前には、性能要件、容量効率、障害ドメイン（同時に故障しうる範囲）を設計段階で検討する必要がある。

### 4.3 容量の確認

```powershell
Get-Volume | Select-Object DriveLetter, FileSystemLabel, FileSystem, Size, SizeRemaining
Get-PSDrive -PSProvider FileSystem
```

大きなディレクトリを特定する例：

```powershell
Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue | ForEach-Object {
  $sum = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue |
    Measure-Object Length -Sum).Sum
  [PSCustomObject]@{ Path = $_.FullName; SizeGB = [math]::Round(($sum/1GB),2) }
} | Sort-Object SizeGB -Descending | Select-Object -First 10
```

このスクリプトは、直下のディレクトリごとに合計サイズを計算し、大きい順に並べる。
`du -sh` に相当する処理を、既定のコマンドレットだけで再現した例である。

### 4.4 クォータの管理

NTFSの標準機能としてのディスククォータと、より高機能な**FSRM（File Server Resource Manager）**の二つの選択肢がある。

```powershell
# NTFS標準クォータの有効化例（ボリューム単位）
Enable-FSRMQuota -ErrorAction SilentlyContinue
```

FSRMはファイルサーバーとしての役割（Windows機能）を追加インストールしていることが前提になる場合が多く、より柔軟なポリシー（フォルダー単位の上限、ファイルスクリーニング）を設定できる。

### 4.5 ディスク拡張

仮想ディスクをハイパーバイザー側で拡張したあと、ゲストOS側でパーティションとボリュームを広げる必要がある。

```powershell
Get-Partition -DiskNumber 0
Get-PartitionSupportedSize -DiskNumber 0 -PartitionNumber 3
```

> **警告**：対象のディスク番号とパーティション番号を取り違えると、意図しない領域を操作する。

```powershell
Resize-Partition -DiskNumber 0 -PartitionNumber 3 `
  -Size (Get-PartitionSupportedSize -DiskNumber 0 -PartitionNumber 3).SizeMax
```

構成によってディスク番号やパーティション番号は変わるため、実行の都度 `Get-Partition` で確認する。

### 4.6 ボリュームの健全性確認

```powershell
Get-Volume | Format-Table DriveLetter, FileSystem, HealthStatus, OperationalStatus
Repair-Volume -DriveLetter D -Scan
```

`HealthStatus` が `Healthy` 以外を示す場合、ファイルシステムレベルの不整合が疑われる。
`Repair-Volume` はLinuxの `fsck` に近い役割を持つ。

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| デバイス列挙 | `lsblk`、`/dev` 配下のノード | `Get-Disk` |
| パーティション方式 | MBR／GPT | MBR／GPT |
| 代表的なファイルシステム | ext4、XFS | NTFS、ReFS |
| 永続マウント設定 | `/etc/fstab` | ドライブレターの割り当て情報（システム内部で管理） |
| 論理ボリューム管理 | LVM | Storage Spaces、動的ディスク（レガシー） |
| 容量確認 | `df`、`du` | `Get-Volume` |
| メタデータ枯渇の症状 | inode枯渇による作成失敗 | MFTを含む内部構造は存在するが、同様の症状は目立ちにくい |
| クォータ | ファイルシステム機能＋`quota`系ツール | NTFSクォータ、FSRM |
| 拡張の手順 | `lvextend` → `xfs_growfs`／`resize2fs` | `Resize-Partition` |
| 整合性チェック | `fsck` | `chkdsk`、`Repair-Volume` |

両OSとも「ブロックデバイス → パーティション → ファイルシステム → マウント／ボリューム」という積み重ねの構造は共通している。
違いは、この積み重ねをどこまで自動化・隠蔽するか、永続化の設定をどこに書くか、という運用面に現れる。

---

## 6. コマンド例

### 6.1 ディスク使用量を確認する

**目的**：容量逼迫の有無を素早く把握する。

#### Linux

基本構文：

```bash
df -hT
du -sh /var/log
```

主要オプション：

- `-h`：人間が読みやすい単位（K/M/G）で表示
- `-T`：ファイルシステム種別を併記
- `-s`：合計のみ表示（`du`）

実行例：

```bash
df -hT /
du -sh /var/log
```

想定出力と読み方：

```text
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/sdb1      xfs    20G   15G  5.0G  75% /
```

`Use%` が90%を超えると、多くの運用基準で警戒水準に達する。

必要な権限：一般ユーザーで多くの情報を確認できる。他ユーザー領域は権限で一部制限される。

誤操作リスク：なし（参照のみ）。

#### Windows

```powershell
Get-Volume
```

想定出力と読み方：`SizeRemaining` を `Size` で割った値が空き容量比率に相当する。

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

### 6.2 マウント状況を確認する

```bash
findmnt -D
```

```powershell
Get-Volume | Format-Table DriveLetter, Path, FileSystem, HealthStatus
```

必要な権限：一般ユーザーで可。

誤操作リスク：なし（参照のみ）。

### 6.3 パーティションを作成する（危険操作）

**目的**：新しいディスクへパーティションを作成し、ファイルシステムを構築する。

> **警告**：対象デバイス名やディスク番号を誤ると、稼働中のデータを消失する。必ず複数のコマンドで対象を確認してから実行する。

#### Linux

```bash
lsblk
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary 0% 100%
sudo mkfs.xfs /dev/sdb1
```

必要な権限：root相当。

誤操作リスク：対象デバイスを取り違えると、稼働中のディスクを初期化してしまう。

#### Windows

```powershell
Get-Disk
Initialize-Disk -Number 1 -PartitionStyle GPT
New-Partition -DiskNumber 1 -UseMaximumSize -AssignDriveLetter |
  Format-Volume -FileSystem NTFS -NewFileSystemLabel Data
```

必要な権限：管理者権限。

誤操作リスク：ディスク番号の取り違えは、Linuxと同様に致命的なデータ消失につながる。

### 6.4 ボリュームを拡張する

```bash
sudo lvextend -L +5G /dev/vgdata/lvdata
sudo xfs_growfs /data
```

```powershell
Resize-Partition -DiskNumber 0 -PartitionNumber 3 `
  -Size (Get-PartitionSupportedSize -DiskNumber 0 -PartitionNumber 3).SizeMax
```

必要な権限：両OSとも管理者権限相当。

誤操作リスク：対象のボリューム・パーティションの取り違えは、意図しない領域を変更するリスクにつながる。

---

## 7. 実務上の注意点

1. **fstabやパーティション変更前にコンソールとバックアップを確保する**
   起動不能になった場合の復旧手段を、変更前に必ず確認する。

2. **UUIDで固定し、デバイス名の直書きを避ける**
   `/dev/sdb` のようなデバイス名は、ディスク構成の変化で入れ替わることがある。

3. **クラウド環境ではデータディスクを分離する**
   OSディスクとデータディスクを分けておくと、拡張やスナップショットの単位を柔軟に選べる。

4. **スナップショットはバックアップの代替ではない**
   同一ストレージ基盤の障害には、スナップショットも道連れになりうる（詳細は第12章）。

5. **LVMやStorage Spacesの拡張は二段階であることを覚えておく**
   論理ボリュームの拡張とファイルシステムの拡張は別操作であり、片方だけでは容量が反映されない。

6. **inodeの使用状況も定期的に監視する**
   容量監視だけでは、inode枯渇による障害を事前に検知できない。

---

## 8. セキュリティ上の注意点

1. **世界書き込み可能なデータ領域を作らない**
   共有ディレクトリの権限設計は第4章の内容と合わせて確認する。

2. **機密データを含むディスクは暗号化を検討する**
   LinuxはLUKS（Linux Unified Key Setup）、WindowsはBitLockerが代表的な選択肢になる（詳細は第11章）。

3. **アンマウント済みディスクの再利用前に消去方針を決める**
   退役したディスクや仮想ディスクをそのまま再割り当てすると、以前のデータが残存するリスクがある。

4. **クォータを活用して単一ユーザーによる容量占有を防ぐ**
   共有ストレージでは、容量枯渇そのものがサービス停止（可用性侵害）につながる。

---

## 9. よくある障害

| 症状 | 起きやすい原因 |
|------|----------------|
| No space left on device | 容量枯渇、またはinode枯渇（`df -h`だけでは見抜けない） |
| 起動時にemergencyモードへ入る | fstabの記述誤り、UUID不一致、デバイス未認識 |
| ディスクがOffline表示になる | Windowsのポリシー設定、SAN（Storage Area Network）経路の問題、権限不足 |
| 拡張したのに容量が増えない | パーティションまたはファイルシステムの拡張漏れ | 
| I/O遅延が発生する | キューの詰まり、ハイパーバイザー側のストレージ競合、物理ディスクの劣化 |

---

## 10. 切り分け手順

ストレージ障害は、容量とinodeの確認から始め、デバイス、マウント、カーネルログの順に絞り込む。

### 手順A：容量とメタデータの確認

**Linux**

```bash
df -h
df -i
lsblk -f
```

**Windows**

```powershell
Get-Volume
Get-PhysicalDisk | Format-Table FriendlyName, HealthStatus, OperationalStatus, Size
```

### 手順B：カーネル／システムログの確認

**Linux**

```bash
dmesg -T | tail -n 50
sudo journalctl -b -p err | grep -iE 'i/o|xfs|ext4|disk|nvme|sd'
```

**Windows**

```powershell
Get-WinEvent -LogName System -MaxEvents 50 |
  Where-Object { $_.ProviderName -match 'disk|ntfs|stor' }
```

### 手順C：マウント／ボリューム状態の確認

1. 期待するマウントポイントまたはドライブレターが実在するかを確認する
2. fstabまたはボリューム設定と、実際の状態が一致しているかを確認する

### 手順D：物理層の健全性

1. 物理ディスクやハイパーバイザー側の警告がないかを確認する
2. SMART（Self-Monitoring, Analysis, and Reporting Technology）情報が取得できる環境であれば併せて確認する

元に戻す方法の原則：

- 調査コマンドは読み取りのみに限定し、書き込みを伴う修復コマンド（`fsck`、`chkdsk`、`Repair-Volume`）はバックアップ確認後に実行する
- fstabやディスク構成を変更した場合は、変更前の設定を保存しておく
- パーティション操作を伴う検証はラボ環境で行う

---

## 11. 章末問題

### 問題1

GPTがMBRより選ばれる一般的な理由を述べよ。

### 問題2

`df -h` では空き容量があるのに、ファイル作成が失敗した。
次に確認すべき指標は何か。

### 問題3

fstab変更後に必ず行うべき確認は何か。

### 問題4

LVMでボリュームを拡張したあと、XFSで必要になる追加操作は何か。

### 問題5

仮想ディスクをハイパーバイザー側で拡張したあと、ゲストOS側で不足しがちな手順を述べよ。

### 問題6

inode枯渇が起きやすいワークロードの特徴を述べよ。

---

## 12. 解答と解説

### 問題1

大容量ディスクや多数のパーティションへの対応、UEFI起動との親和性、パーティション情報の冗長化による耐障害性が理由として挙げられる。

### 問題2

inodeの使用率（`df -i`）を確認する。

### 問題3

`findmnt --verify` や `mount -a` のような試験的な適用を行い、記述誤りがないかを事前に検出する。

### 問題4

`xfs_growfs`（ext4の場合は`resize2fs`）でファイルシステム自体を拡張する操作が必要である。
論理ボリュームの拡張だけでは、ファイルシステムが認識する容量は変わらない。

### 問題5

ゲストOS側でのパーティション拡張とボリューム拡張（`Resize-Partition` など）を忘れがちである。

### 問題6

小さなファイルを大量に生成するワークロード（メールスプール、コンテナのレイヤーキャッシュ、セッションファイルの蓄積など）で起きやすい。

---

## 13. ハンズオン演習

### 演習6-1 追加ディスクをマウントする

**前提条件**

- ハイパーバイザーで第二ディスクを付与済みであること
- スナップショットを取得済みであること

**実行内容（Linux）**

```bash
lsblk
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary 0% 100%
sudo mkfs.xfs /dev/sdb1
sudo mkdir -p /data
sudo mount /dev/sdb1 /data
blkid /dev/sdb1
echo 'UUID=<取得したUUID> /data xfs defaults 0 2' | sudo tee -a /etc/fstab
sudo findmnt --verify
sudo mount -a
```

**実行内容（Windows）**

```powershell
Get-Disk
Initialize-Disk -Number 1 -PartitionStyle GPT
New-Partition -DiskNumber 1 -UseMaximumSize -AssignDriveLetter |
  Format-Volume -FileSystem NTFS -NewFileSystemLabel Data
Get-Volume
```

**確認方法**

- 再起動後もマウント（またはドライブ割り当て）が維持されていることを確認する
- `df -hT` または `Get-Volume` で新しい領域が見えることを確認する

**元に戻す方法**

- ラボ環境であればディスクを切り離し、スナップショットへ戻す
- fstabへ追記した行を削除してから `sudo mount -a` で確認する

### 演習6-2 満杯予兆の調査

**前提条件**：演習対象のマシンに一般ユーザーでログインできる。

**実行内容（Linux）**

```bash
df -h
df -i
du -sh /var/* 2>/dev/null | sort -h | tail
```

**実行内容（Windows）**

```powershell
Get-Volume
Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue | ForEach-Object {
  $sum = (Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue |
    Measure-Object Length -Sum).Sum
  [PSCustomObject]@{ Path = $_.FullName; SizeGB = [math]::Round(($sum/1GB),2) }
} | Sort-Object SizeGB -Descending | Select-Object -First 10
```

**確認方法**：容量を多く占めるディレクトリと、古いログや一時ファイルなど削除候補を洗い出す。

**元に戻す方法**：本演習は参照のみであり、本番データの削除は行わない。

---

## 14. 本章のまとめ

ストレージは、デバイス、パーティション、ファイルシステム、マウントという層の積み重ねで成り立つ。
Linuxはfstabによる明示的なマウント設定とinode管理、WindowsはドライブレターとMFTベースの管理という別々の実装で、同じ課題に対応している。

次章では、この上で動くネットワーク管理の仕組みを扱う。

次章: [第7章 ネットワーク管理](07_network_management.md)


---


<!-- source: 07_network_management.md -->

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


---


<!-- source: 08_software_and_updates.md -->

# 第8章 ソフトウェアと更新管理

未適用のセキュリティパッチ、壊れた依存関係、検証を経ない本番更新。

ソフトウェア管理は、単なる機能追加の手段ではなく、可用性とセキュリティを左右する変更管理そのものである。

本章では、Linuxのパッケージ管理（RHEL系のrpm/dnf、Ubuntu系のdpkg/apt）と、Windowsの役割・機能・Windows Updateの仕組みを対比しながら、再起動判断、ロールバック、検証環境と本番環境の分離という運用上の要点までを扱う。

---

## 1. 学習目標

1. Linuxのパッケージ管理（rpm/dnf/apt/dpkg）の役割分担とリポジトリ、依存関係の考え方を説明できる
2. Windows Updateと、役割（Role）・機能（Feature）の追加・削除方法を説明できる
3. PowerShellを使った機能追加・削除、更新状況の確認ができる
4. パッチ適用の要否判断、再起動判断、ロールバックの選択肢を説明できる
5. 検証環境と本番環境を分離する理由と、その運用パターンを説明できる
6. 同一の管理目的を持つ操作を、両OSでそれぞれ実行できる

---

## 2. 基本概念

### 2.1 パッケージと依存関係

**パッケージ**とは、実行ファイル、設定ファイル、ドキュメント、インストール/アンインストール用のスクリプトなどを、配布しやすい単位でひとまとめにしたものである。

パッケージには通常、名前、バージョン、アーキテクチャ（x86_64など）、そして動作に必要な他のパッケージを示す**依存関係（Dependency）**の情報が含まれる。

依存関係の解決に失敗すると、そのパッケージ自体の導入や更新が止まる。

複数のパッケージが互いに異なるバージョンの同じライブラリを要求する状態を**依存関係の衝突**と呼び、大規模な環境ほど発生しやすい問題である。

### 2.2 リポジトリ

**リポジトリ**は、パッケージを配布するためのサーバー（またはその集合）であり、パッケージ管理ツールはリポジトリのメタデータ（パッケージ一覧、バージョン、依存関係、署名情報）を参照して動作する。

リポジトリには、OSベンダーが公式に提供するもの、組織が内部に構築するミラーやプロキシ、サードパーティが提供するものがあり、それぞれ信頼の度合いが異なる。

リポジトリは一種の**信頼境界**であり、署名検証を無効化したり、出所不明のリポジトリを無条件に追加したりすることは、サプライチェーンリスクを増大させる。

### 2.3 パッチ管理

**パッチ管理**とは、脆弱性修正や不具合修正を、検証したうえで計画的に本番環境へ展開していく一連の活動を指す。

パッチ管理には、影響範囲の特定、メンテナンス時間帯（メンテナンスウィンドウ）の確保、再起動の要否判断、問題発生時の切り戻し（ロールバック）手順が含まれる。

パッチを「とりあえず全部適用する」という運用は、短期的には脆弱性を減らせても、動作検証が不十分なまま本番へ適用すると、可用性を損なうリスクを孕む。

### 2.4 検証環境と本番環境の分離

同じ変更を、まず検証環境（ステージング環境）に適用して問題がないことを確認してから、本番環境へ展開するという原則が**検証と本番の分離**である。

「本番だけ特別な手順で手作業を行う」という運用は、再現性がなく、ヒューマンエラーの温床になりやすい。

理想的には、検証環境は本番環境とできるだけ近い構成（同一OSバージョン、同一パッチレベル、同等のミドルウェア構成）を保つ。

### 2.5 バージョン管理と対象範囲

本章で扱うコマンドや挙動は、RHEL系（RHEL 8/9、Rocky Linux、AlmaLinuxなど、dnfを標準採用）、Ubuntu系（20.04/22.04/24.04 LTS、apt/dpkgを採用）、Windows Server 2022以降を前提とする。

古いRHEL 7系までは `dnf` ではなく `yum` が標準であった点、Windows Serverのバージョンによって役割・機能の名称やWindows Updateの仕組み（WSUSやMicrosoft Updateとの連携）が異なる点に注意する。

---

## 3. Linuxでの実現方法

### 3.1 RHEL系のパッケージ管理（rpm / dnf）

**rpm（RPM Package Manager）**は、個々のパッケージファイル（`.rpm`）を直接操作する低レベルなツールである。

**dnf（Dandified YUM）**は、rpmを内部で使いながら、リポジトリからの依存関係解決、ダウンロード、インストールをまとめて行う高レベルなパッケージマネージャーである。

```bash
rpm -qa | head
rpm -qi openssh-server
rpm -ql openssh-server | head
rpm -qf /usr/sbin/sshd
```

- `rpm -qa`：インストール済みの全パッケージを一覧表示する（`-q` は問い合わせ、`-a` は全件の意味）
- `rpm -qi <パッケージ名>`：パッケージの詳細情報（バージョン、ベンダー、インストール日時など）を表示する
- `rpm -ql <パッケージ名>`：そのパッケージが配置したファイルの一覧を表示する
- `rpm -qf <ファイルパス>`：あるファイルがどのパッケージに属するかを逆引きする

dnfによる更新・導入・削除の例を示す。

```bash
sudo dnf check-update
sudo dnf install -y nginx
sudo dnf upgrade -y
sudo dnf remove -y nginx
dnf repolist
dnf repolist --all
dnf history
```

- `dnf check-update`：更新可能なパッケージの一覧を表示する（更新は行わない）
- `dnf install -y <パッケージ名>`：パッケージを導入する。`-y` は確認プロンプトを自動でyesにする
- `dnf upgrade -y`：導入済みパッケージ全体を最新版へ更新する（旧`yum update`に相当）
- `dnf history`：これまでのdnf操作履歴を表示し、`dnf history undo <ID>` で特定操作を取り消せる場合がある

```text
Last metadata expiration check: 0:12:41 ago on Thu 30 Jul 2026 03:50:12 AM JST.
Dependencies resolved.
================================================================================
 Package          Arch      Version              Repository        Size
================================================================================
Installing:
 nginx             x86_64    1:1.24.0-1.el9       appstream         600 k
Installing dependencies:
 nginx-filesystem   noarch    1:1.24.0-1.el9       appstream          25 k
```

この出力の「Installing dependencies」欄は、指定したパッケージ以外に自動導入される依存パッケージであり、想定外の追加パッケージがないか確認する習慣が重要である。

### 3.2 Ubuntu系のパッケージ管理（dpkg / apt）

**dpkg（Debian Package）**は、rpmに相当する低レベルなパッケージ操作ツールである。

**apt（Advanced Package Tool）**は、dpkgを内部で使いながら依存関係解決とリポジトリ管理を行う高レベルなツールである。

```bash
dpkg -l | head
dpkg -L nginx | head
dpkg -S /usr/sbin/nginx
```

- `dpkg -l`：インストール済みパッケージの一覧を表示する
- `dpkg -L <パッケージ名>`：そのパッケージが配置したファイル一覧を表示する
- `dpkg -S <ファイルパス>`：ファイルからパッケージを逆引きする

aptによる更新・導入・削除の例を示す。

```bash
sudo apt update
sudo apt list --upgradable
sudo apt install -y nginx
sudo apt upgrade -y
sudo apt full-upgrade -y
sudo apt remove -y nginx
sudo apt autoremove -y
apt-cache policy nginx
```

- `apt update`：リポジトリのメタデータ（パッケージ一覧）を最新化する。パッケージ自体は更新しない
- `apt upgrade -y`：導入済みパッケージを更新するが、依存関係の都合でパッケージの削除が必要な更新はスキップする
- `apt full-upgrade -y`：必要であればパッケージの削除も伴いながら更新する（旧`dist-upgrade`に相当）
- `apt autoremove -y`：不要になった依存パッケージを削除する
- `apt-cache policy <パッケージ名>`：導入済みバージョンと候補バージョン、リポジトリの優先度を表示する

`apt update` を実行せずに `apt install` を行うと、古いメタデータのままパッケージ解決を試みてしまい、実際には存在しないバージョンを要求してエラーになることがある。

### 3.3 リポジトリの管理

RHEL系では `/etc/yum.repos.d/*.repo`、Ubuntu系では `/etc/apt/sources.list` や `/etc/apt/sources.list.d/*.list` にリポジトリ定義がある。

```bash
# RHEL系
cat /etc/yum.repos.d/*.repo | head -n 20
sudo dnf config-manager --add-repo https://example.com/repo/example.repo
sudo dnf config-manager --set-disabled example-repo

# Ubuntu系
cat /etc/apt/sources.list
ls /etc/apt/sources.list.d/
sudo add-apt-repository ppa:example/example
```

> **警告**: 出所が不明なサードパーティリポジトリやPPA（Personal Package Archive）の追加は、意図しないパッケージの上書きや、悪意あるパッケージの混入リスクを伴う。追加前に提供元の信頼性を確認する。

署名検証（GPGキー）を無効化してのパッケージ導入は、緊急時であっても原則として避け、正規の鍵登録手順を踏む。

### 3.4 再起動要否の判断

```bash
# RHEL系
sudo dnf install -y dnf-utils
needs-restarting -r
needs-restarting -s

# 共通
uname -r
rpm -q kernel 2>/dev/null || dpkg -l | grep linux-image
test -f /var/run/reboot-required && echo "REBOOT_REQUIRED" || echo "no reboot flag"
cat /var/run/reboot-required.pkgs 2>/dev/null
```

`needs-restarting -r` は、システム全体の再起動が必要かどうかを判定し、終了コードでも結果を返す（RHEL系）。

`needs-restarting -s` は、再起動ではなく個別サービスの再起動が必要かどうかを判定する。

Ubuntu系では `/var/run/reboot-required` の存在自体が、カーネルなど基盤コンポーネント更新後に再起動が必要であることを示すフラグになっている。

`uname -r` で表示される実行中のカーネルバージョンと、`rpm -q kernel`/`dpkg -l | grep linux-image` で確認できる導入済み最新カーネルのバージョンが異なる場合、再起動するまで新しいカーネルは有効にならない。

カーネル、glibc、systemd、OpenSSLなど、システムの基盤に関わるコンポーネントを更新した場合は、原則として再起動を計画する。

### 3.5 ロールバックの考え方

Linuxのパッケージ管理には、Windowsのシステムの復元に相当する統一的な巻き戻し機構は標準では存在しないため、複数の手段を組み合わせて考える。

1. **パッケージのダウングレード**：リポジトリに旧バージョンのパッケージが残っている場合、`dnf downgrade <パッケージ名>` や、明示的なバージョン指定でのインストールで戻せる。
2. **dnfのトランザクション取り消し**：`dnf history` で操作履歴を確認し、`dnf history undo <ID>` で直前のトランザクションを取り消せる場合がある。
3. **設定ファイルのバックアップからの復元**：更新前に `/etc` 配下の設定を退避しておき、問題発生時に戻す。
4. **スナップショットやイメージへの復元**：仮想マシンやコンテナ基盤であれば、更新前のスナップショットへ戻すのが最も確実である。

```bash
sudo dnf history
sudo dnf history undo 42
sudo dnf downgrade -y nginx
```

完全な時系列ロールバックを実現できるかどうかは、事前の構成管理（Ansible等でのコード化）とバックアップ設計に強く依存する。

---

## 4. Windowsでの実現方法

### 4.1 Windows Updateの確認

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 15
Get-HotFix -Id KB5034441 -ErrorAction SilentlyContinue
```

`Get-HotFix` は、導入済みの更新プログラム（QFE: Quick Fix Engineering）を一覧表示する。

実際の企業環境では、Windows Updateの承認・配布経路が、Microsoft Update（単体運用）、**WSUS（Windows Server Update Services）**、クラウドのパッチ管理基盤（Azure Update Managerなど）、Microsoft Intuneなど、組織方針によって大きく異なる。

そのため、「今どのポリシーで更新が配布されているか」を、`Get-HotFix` の結果だけでなく、組織のパッチ管理基盤側でも必ず確認する。

PowerShellモジュール `PSWindowsUpdate`（Windows標準搭載ではなく別途導入が必要）を使うと、更新の検索・適用までPowerShellから行えるが、標準機能ではない点に注意する。

```powershell
# 例（標準搭載外のモジュールを使う場合の参考）
# Install-Module PSWindowsUpdate -Force
# Get-WindowsUpdate
# Install-WindowsUpdate -AcceptAll -AutoReboot
```

> **警告**: `-AutoReboot` を伴う自動適用は、業務時間中に実行すると無予告の再起動につながるため、メンテナンスウィンドウ内でのみ実行する。

### 4.2 役割（Role）と機能（Feature）

Windows Serverでは、サーバーが提供する機能を**役割（Role）**と**機能（Feature）**という単位で管理する。

役割の例には、Active Directory Domain Services、DNS Server、Web Server（IIS）などがあり、機能の例には、.NET Framework、Telnetクライアント、SNMPサービスなどがある。

```powershell
Get-WindowsFeature | Where-Object Installed -eq $true
Get-WindowsFeature Web-Server
```

導入例を示す。

```powershell
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
```

`-IncludeManagementTools` を付けると、対応する管理ツール（GUIコンソールなど）も同時に導入される。

削除の例を示す。

```powershell
Uninstall-WindowsFeature -Name Web-Server
```

想定出力の例を示す。

```text
Success Restart Needed Exit Code      Feature Result
------- -------------- ---------      --------------
True    No             Success        {Web Server (IIS), Web Server, ...}
```

`Restart Needed` が `Yes` の場合、機能自体は導入済みでも、再起動を行うまで完全には有効化されない場合がある。

Windows 11などクライアント版では、役割・機能ではなく「オプション機能」という単位で管理し、`Get-WindowsOptionalFeature` / `Enable-WindowsOptionalFeature` を使う。

```powershell
Get-WindowsOptionalFeature -Online | Where-Object State -eq 'Enabled'
Enable-WindowsOptionalFeature -Online -FeatureName TelnetClient
```

### 4.3 PowerShellによる機能追加の注意点

```powershell
# 警告: 本番環境での役割追加は、設計レビューを経てから実施する
Install-WindowsFeature -Name DNS -IncludeManagementTools
```

役割・機能の追加では、依存する他の機能が自動的に追加されることがある。

追加前後で `Get-WindowsFeature` の出力を保存しておくと、意図した変更のみが行われたことを確認でき、後日の切り戻し検討にも役立つ。

```powershell
Get-WindowsFeature | Where-Object Installed -eq $true |
  Export-Csv -Path C:\logs\features_before.csv -NoTypeInformation

# 変更実施後
Get-WindowsFeature | Where-Object Installed -eq $true |
  Export-Csv -Path C:\logs\features_after.csv -NoTypeInformation
```

### 4.4 再起動判断と切り戻し

Windowsでは、更新プログラムの適用結果や役割追加の結果として、明示的に再起動要否が示されることが多い。

```powershell
$sysInfo = Get-CimInstance -ClassName Win32_OperatingSystem
$sysInfo.LastBootUpTime

Get-WindowsFeature | Where-Object {$_.Installed -and $_.RestartNeeded -eq 'Yes'}
```

クラスタ環境では、ノードを順番に更新し自動的にフェイルオーバーさせながらパッチを適用する**Cluster-Aware Updating (CAU)** のような仕組みも存在する。

切り戻しの選択肢としては、次のようなものがある。

1. 更新プログラムのアンインストール（`wusa /uninstall /kb:<番号>` や設定アプリからの削除）
2. システムの復元ポイントの利用（クライアントOSで一般的）
3. バックアップからのシステム状態復元
4. 仮想マシンの直前スナップショットへの復元（ラボや検証環境）

```powershell
# 特定の更新プログラムをアンインストールする例
wusa /uninstall /kb:5034441 /quiet /norestart
```

> **警告**: 本番でスナップショットに依存した切り戻しを常用すると、アプリケーションデータの整合性やサポートポリシー上の問題（データベース製品などでスナップショット復元がサポート外とされる場合がある）に注意する必要がある。

---

## 5. 両OSの比較

| 目的 | Linux | Windows |
|------|-------|---------|
| 導入済み一覧 | `rpm -qa` / `dpkg -l` | `Get-HotFix` / `Get-WindowsFeature` |
| 更新の有無確認 | `dnf check-update` / `apt list --upgradable` | 更新プログラムの確認（設定アプリ、WSUS、`Get-HotFix`との突合） |
| 導入 | `dnf install` / `apt install` | `Install-WindowsFeature` / インストーラー |
| 更新 | `dnf upgrade` / `apt upgrade` | Windows Update系（単体・WSUS・Intune等） |
| 削除 | `dnf remove` / `apt remove` | `Uninstall-WindowsFeature` / アプリのアンインストール |
| リポジトリ相当 | `/etc/yum.repos.d`、`/etc/apt/sources.list` | Microsoft Update、WSUS、Intune |
| 依存関係解決 | dnf/aptが自動解決 | 役割・機能の依存は自動追加、アプリは個別対応 |
| 再起動要否判定 | `needs-restarting`、`/var/run/reboot-required` | 更新結果の`RestartNeeded`、システム設定アプリの通知 |
| 操作履歴・取り消し | `dnf history` / `dnf history undo` | 更新プログラムのアンインストール、復元ポイント |

Linuxは「パッケージ単位」の粒度で更新・削除を扱うのに対し、Windowsは「役割・機能」という機能単位と、「更新プログラム（KB番号）」という差分パッチ単位の、2つの管理軸が併存している点が構造的な違いである。

---

## 6. コマンド例

### 6.1 パッケージ/機能を導入する

**目的**: 追加のソフトウェアコンポーネントを導入する。

```bash
sudo dnf install -y git
# Ubuntu系: sudo apt install -y git
```

```powershell
Install-WindowsFeature -Name Telnet-Client
```

**権限**: Linuxはroot（sudo）、Windowsは管理者。

**リスク**: 中。依存パッケージの追加、再起動の必要性、攻撃対象領域（アタックサーフェス）の拡大を伴う可能性がある。

### 6.2 更新の有無を確認する

**目的**: 適用可能な更新の件数と内容を事前に把握する。

```bash
sudo dnf check-update
```

```powershell
Get-HotFix | Measure-Object
# 未適用の更新一覧は、WSUS/Intuneなど管理基盤側で確認するのが確実
```

**権限**: 一般ユーザーでも参照可能なことが多いが、環境によっては制限される。

**リスク**: 低（参照のみ）。

### 6.3 特定パッケージのバージョンを固定する

**目的**: 特定パッケージだけを自動更新の対象から外し、意図しないバージョンアップを防ぐ。

```bash
# RHEL系（dnf-plugins-coreが必要）
sudo dnf install -y dnf-plugins-core
sudo dnf versionlock add nginx
sudo dnf versionlock list

# Ubuntu系
sudo apt-mark hold nginx
sudo apt-mark showhold
```

**権限**: root（sudo）。

**リスク**: 中。固定を忘れると、セキュリティ修正が長期間未適用のまま放置されるリスクに転じる。固定には必ず解除条件・見直し時期を決めておく。

### 6.4 役割の導入と依存の確認（Windows）

**目的**: 特定の役割を導入し、依存関係を含めた変更内容を把握する。

```powershell
# 警告: 本番での役割追加は設計レビュー後に実施する
Install-WindowsFeature -Name Web-Server -IncludeManagementTools -WhatIf
Install-WindowsFeature -Name Web-Server -IncludeManagementTools
```

`-WhatIf` を先に付けて実行すると、実際には変更を加えずに、何が行われるかのプレビューだけを確認できる。

**権限**: 管理者。

**リスク**: 中〜高。依存関係で追加される役割・機能や、再起動要否を事前に把握しておく必要がある。

### 6.5 更新プログラムを個別にアンインストールする

**目的**: 特定の更新プログラム適用後に問題が発生した場合、その更新のみを取り消す。

```powershell
# 警告: 対象KB番号を誤ると別の修正まで取り消してしまう
wusa /uninstall /kb:5034441 /quiet /norestart
```

**権限**: 管理者。

**リスク**: 高。取り消した修正に含まれる脆弱性対策も同時に無効化される点に注意する。

---

## 7. 実務上の注意点

1. パッチ適用前に、メンテナンスウィンドウ、影響を受けるサービス、連絡先（エスカレーション先）を明確にしておく。
2. 検証環境 → ステージング環境 → 本番環境という順序を、緊急時であっても可能な限り守る。
3. 更新前後で、バージョン情報と主要な設定ファイルの差分を記録しておく。
4. サードパーティリポジトリは、署名検証と優先度（Ubuntu系のAPT Pinningなど）を管理し、意図しないバージョンでの上書きを防ぐ。
5. アプリケーションのサポートマトリクス（どのOSパッチレベルまで動作保証されているか）を、パッチ適用前に確認する。
6. 大量のサーバーに展開する場合は、一部のサーバーから段階的に適用する（カナリア方式）ことで、問題の影響範囲を限定できる。

---

## 8. セキュリティ上の注意点

1. サポート終了（EOL: End Of Life）となったディストリビューションやWindowsのバージョンを放置しない。セキュリティ修正が提供されなくなる。
2. 内部ミラーリポジトリを使い、各サーバーが直接インターネットへ出る必要性を減らす選択肢も検討する。
3. パッケージの署名検証（GPGキー、Windowsのコード署名）を無効化しない。
4. 一時的に導入したデバッグツールや診断パッケージを、調査終了後に削除し忘れると、恒久的な攻撃対象領域の拡大につながる。
5. 更新の適用状況を可視化する仕組み（レポート、ダッシュボード）を持ち、未適用ホストを放置しない体制を作る。
6. 緊急のゼロデイ脆弱性対応では、検証を最小限にしてでも先行適用する判断基準を、事前に組織として合意しておく。

---

## 9. よくある障害

| 症状 | 典型的な原因 |
|------|--------------|
| 依存関係エラーで導入・更新が止まる | リポジトリの混在、手動でのrpm/dpkg直接操作による整合性破壊、バージョン固定（ピン留め）の残存 |
| 更新自体が失敗する | ディスク容量不足、リポジトリミラーの障害、プロキシ設定の誤り、GPG署名検証エラー |
| 更新後に対象サービスが起動しない | 設定ファイルの非互換、モジュールパスの変更、SELinux/AppArmorによる新規パスの拒否 |
| 更新後に再起動ループへ陥る | ドライバーの非互換、ブートローダー設定の破損、直前パッチの不具合 |
| Windowsの役割追加が完了しない | 依存する役割の不足、ソースファイルの取得失敗（DISMソースの構成不足） |
| Windows Updateが特定のKBだけ繰り返し失敗する | コンポーネントストアの破損、ディスク容量不足、以前の更新プログラムとの競合 |

---

## 10. 切り分け手順

1. **エラーメッセージの全文を保存する**: 一部だけを見て早合点せず、コマンド出力全体、ログファイル、イベントIDを控える。
2. **直前の変更を特定する**: いつ、何を、誰が変更したかを、`dnf history`/`apt history`相当のログや変更管理台帳から確認する。
3. **影響範囲を切り分ける**: 単一サービスの問題か、OS全体の問題か、特定ホストのみの問題か、複数ホストで再現するかを確認する。
4. **戻すか進めるかを判断する**: 直前のパッチを切り戻すか、追加のパッチで修正するか、リスクと復旧時間を比較して決める。
5. **検証環境で再現を確認する**: 可能であれば、本番へ手を加える前に、同一条件の検証環境で問題を再現させ、修正案を試す。
6. **恒久対策を反映する**: 応急処置で終わらせず、根本原因（リポジトリ設定、依存管理、テスト不足など）に対する恒久対策を検討する。

Windows特有の追加確認として、DISM（Deployment Image Servicing and Management）によるコンポーネントストアの健全性チェックがある。

```powershell
DISM /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```

`DISM /RestoreHealth` は、Windows Updateのコンポーネントストア自体が破損している疑いがある場合の修復手段であり、`sfc /scannow` はシステムファイルの整合性チェックと修復を行う。

Linux側での関連する健全性確認として、パッケージデータベース自体の整合性チェックがある。

```bash
sudo rpm --verify --all 2>&1 | head -n 30
sudo dpkg --audit
```

---

## 11. 章末問題

1. `rpm` と `dnf` の役割の違いを述べよ。
2. `apt update` と `apt upgrade` の違いを説明せよ。
3. 検証環境と本番環境を分離する主な目的を述べよ。
4. カーネル更新後に再起動が必要になる理由を説明せよ。
5. `Install-WindowsFeature` の実行前後で保存しておくべき情報を挙げよ。
6. ロールバック手段が用意されていない状態で本番環境に更新を適用してはいけない理由を述べよ。
7. サードパーティリポジトリを追加する際に確認すべき事項を2つ挙げよ。

---

## 12. 解答と解説

1. rpmは個々のパッケージファイルを直接操作する低レベルなツールであり、dnfはリポジトリからの依存関係解決とダウンロードを含む高レベルな管理ツールである。
2. `apt update` はリポジトリのメタデータ（パッケージ一覧や依存関係情報）を最新化するだけで、パッケージ自体は更新しない。`apt upgrade` は実際に導入済みパッケージを更新する。
3. 本番環境へ影響を与える前に、互換性、手順の妥当性、ロールバック手段の有効性を安全に確認するため。
4. 実行中のカーネルはメモリに読み込まれたまま動作しており、ディスク上の新しいカーネルイメージへ切り替えるには、システムの再起動によるカーネルの再読み込みが必要なため。
5. インストール済みの役割・機能一覧、再起動要否のフラグ、依存関係で自動追加された役割・機能の一覧。
6. 適用後に問題が発生した際、業務停止が長期化するだけでなく、原因の切り分けも困難になり、復旧までの時間が予測不能になるため。
7. 提供元の信頼性・実績、署名鍵の入手経路の正当性、既存パッケージとのバージョン競合の有無。

---

## 13. ハンズオン演習

### 演習8-1 パッケージ・役割の導入と削除、記録の取得

**前提**: `web01`（Linux）と `winapp01`（Windows）が稼働しており、演習用にスナップショットを取得済みであること。

**実行**:

1. `web01` で、`sudo dnf install -y git` （Ubuntu系なら `sudo apt install -y git`）を実行し、バージョンを `git --version` で記録する。
2. `winapp01` で、`Install-WindowsFeature -Name Telnet-Client` を実行し、結果を記録する。

**確認**: `rpm -qi git`（またはUbuntu系で`dpkg -l git`）と `Get-WindowsFeature Telnet-Client` で、それぞれ導入済みであることを確認する。

**元に戻す**: `sudo dnf remove -y git` と `Uninstall-WindowsFeature -Name Telnet-Client` を実行し、削除されたことを再確認する。

### 演習8-2 パッチ適用リハーサル

**前提**: `web01` の仮想マシンスナップショットを事前に取得していること。

**実行**:

1. 更新前スナップショットを取得する（ラベル例: `before-ch08-patch`）。
2. `sudo dnf upgrade -y`（またはUbuntu系で`sudo apt upgrade -y`）を実行する。
3. 主要サービス（SSH、Webサーバーなど）が正常に稼働しているか確認する。

**確認**: `systemctl status sshd`（または該当サービス）が `active (running)` であることを確認する。問題があれば、`journalctl -u <サービス名> -n 50` でエラーを確認する。

**元に戻す**: 問題が発生した場合を想定し、スナップショットへ戻す操作を実際に実行し、所要時間を計測してRTO（目標復旧時間）の感覚を養う。問題がなければスナップショットは保持したまま次の演習へ進んでよい。

### 演習8-3 バージョン固定と解除

**前提**: 演習8-1で `git` が導入済みであること。

**実行**:

1. RHEL系: `sudo dnf versionlock add git`。Ubuntu系: `sudo apt-mark hold git`。
2. 固定状態で `sudo dnf upgrade -y`（または `sudo apt upgrade -y`）を実行し、`git` が更新対象から除外されることを確認する。

**確認**: `dnf versionlock list`（または `apt-mark showhold`）で、`git` が固定リストに含まれることを確認する。

**元に戻す**: RHEL系は `sudo dnf versionlock delete git`、Ubuntu系は `sudo apt-mark unhold git` で固定を解除し、解除されたことを再度一覧で確認する。

---

## 14. 本章のまとめ

ソフトウェア管理は機能を増やす作業である以前に、可用性とセキュリティに直結する変更管理であり、リポジトリの信頼性、依存関係、再起動判断、ロールバック手段を常にセットで考える必要がある。

LinuxとWindowsは操作コマンドこそ異なるが、「導入・更新・削除・再起動判断・切り戻し」という管理の骨格は共通しており、どちらの環境でも同じ判断軸で運用できる。

次章では、その変更や障害を実際に観測するための手段として、ログと監視の仕組みを扱う。

次章: [第9章 ログと監視](09_logs_and_monitoring.md)


---


<!-- source: 09_logs_and_monitoring.md -->

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


---


<!-- source: 10_active_directory_and_linux.md -->

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


---


<!-- source: 11_security.md -->

# 第11章 セキュリティ

境界だけを固め、内部を素のままにしておく構成は長く持たない。
攻撃者は境界を突破したあと、内部の緩い設定を足がかりにして権限を拡大していく。

**OSハードニング**とは、不要な入口を閉じ、残した入口を強くし、何が起きたかの痕跡を残す作業である。
本章では、不要サービスの停止、パッチ適用、パスワードポリシー、SSH（Secure Shell）とRDP（Remote Desktop Protocol）、公開鍵認証、強制アクセス制御、ディスク暗号化、監査ログ、マルウェア対策、管理用アカウントの分離を、LinuxとWindowsの両方で扱う。

これらは単発の設定変更ではなく、新規サーバーを作るたびに同じ状態を再現できる基準として運用する対象である。

---

## 1. 学習目標

1. OSハードニングの観点（サービス、パッチ、アカウント、遠隔管理、暗号化、監査）を列挙できる。
2. 不要サービスの棚卸しとパッチ適用の考え方を説明できる。
3. パスワードポリシーの要素と、SSH・RDPを安全に運用するための要点を説明できる。
4. 公開鍵認証の仕組みと導入手順を実行できる。
5. SELinux（Security-Enhanced Linux）とAppArmor、Windows Defender、BitLocker、Linuxのディスク暗号化の位置づけを説明できる。
6. 監査ログとマルウェア対策の基本を実行できる。
7. 管理用アカウントを日常アカウントから分離する設計ができる。

---

## 2. 基本概念

### 2.1 OSハードニングの考え方

**OSハードニング**は、出荷時や初期導入のまま残っている攻撃面を、用途に合わせて減らす作業である。

主な観点は次のとおりである。

1. 不要サービスの停止
2. パッチ適用
3. パスワードポリシー
4. 遠隔管理経路の制限
5. ホストファイアウォール（第7章参照）
6. 強制アクセス制御やマルウェア対策
7. ディスク暗号化
8. 監査ログ
9. 管理用アカウントの分離

これらは互いに独立した対策ではなく、どれか一つが崩れると他の対策の効果も下がるという関係にある。
監査ログを整えても、管理用アカウントが日常アカウントと共用されていれば、誰が何をしたかを追跡できない。

### 2.2 認証の強化

パスワードだけに頼る認証は、推測、使い回し、フィッシングに弱い。

**公開鍵認証**は、秘密鍵を本人だけが保持し、公開鍵をサーバー側に登録しておく認証方式であり、パスワードそのものをネットワーク上でやり取りしない。

**多要素認証（MFA: Multi-Factor Authentication）**は、パスワードなどの知識要素に加え、端末やトークンなどの所持要素、指紋などの生体要素を組み合わせる方式であり、導入の要否は組織の方針による。

認証を強化する際は、パスワード、公開鍵、多要素の順に段階を上げていくと理解しやすい。

### 2.3 強制アクセス制御という考え方

従来のユーザー権限（読み書き実行の許可）だけでは、正規のプロセスが本来意図しないファイルへアクセスすることを防げない。

**強制アクセス制御（MAC: Mandatory Access Control）**は、ユーザー権限とは別の層で、プロセスごとに何にアクセスしてよいかをポリシーとして定義し、root（Linuxの最高権限アカウント）や管理者権限で動くプロセスであっても、ポリシーで許可されていない操作を拒否する仕組みである。

LinuxではSELinuxとAppArmorが代表的な実装であり、Windowsには完全に同等な必須機構はなく、AppLockerのような用途別の仕組みで補う。

### 2.4 防御の多層化

単一の製品や設定に依存する防御は、その一点が突破されると全体が崩れる。

**多層防御（Defense in Depth）**は、入口（ネットワーク、認証）、権限（最小権限、アクセス制御）、検知（監査ログ、マルウェア対策）という複数の層を重ね、一つの層が突破されても他の層で被害を抑える考え方である。

本章で扱う項目は、いずれもこの多層防御のどこか一つの層に対応している。

---

## 3. Linuxでの実現方法

### 3.1 不要サービスの棚卸しと停止

サービスは、有効化されているだけでも攻撃対象になり得る。

```bash
systemctl list-unit-files --type=service --state=enabled
sudo ss -tulpn
```

用途に不要と判断したサービスは、依存関係を確認したうえで無効化する。

```bash
# 警告: 停止対象を誤ると、他のサービスやリモート接続が道連れで止まることがある
sudo systemctl stop cups
sudo systemctl disable cups
```

`disable` は次回起動時からの自動起動を止めるだけであり、稼働中のプロセスは止まらないため、即時に止めたい場合は `stop` と組み合わせる。

### 3.2 パッチ適用

既知の脆弱性は、公開された時点から悪用が始まる。

```bash
# RHEL系
sudo dnf upgrade -y
rpm -qa --last | head -n 20

# Ubuntu系
sudo apt update && sudo apt upgrade -y
grep -i upgrade /var/log/apt/history.log
```

カーネルを更新した場合は、再起動しないと新しいカーネルが有効にならない。

```bash
sudo dnf needs-restarting -r
```

### 3.3 パスワードポリシー

パスワードポリシーは、**PAM（Pluggable Authentication Modules）**の設定を通じて強制する。

```bash
# 複雑性要件の例（pam_pwquality、RHEL系）
sudo cat /etc/security/pwquality.conf
```

有効期限は `chage`、連続失敗によるロックアウトはPAMの `pam_faillock` で制御する。

```bash
sudo chage -l operator
sudo chage -M 90 operator
```

`chage -l` はアカウントごとのパスワード有効期限や最終変更日を一覧表示し、`-M` は最大有効日数を設定する。
一覧表示は一般ユーザーでも自身の情報を確認できるが、他人の情報の参照や設定変更にはroot権限が必要である。

### 3.4 SSHの強化

**SSH（Secure Shell）**は、Linuxサーバーへの標準的な遠隔ログイン手段であり、通信は暗号化される。

設定を変更する前に、必ず設定ファイルを退避し構文を確認する。

```bash
sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%F)
sudo sshd -t
```

`sshd -t` は設定ファイルの構文だけを検査し、サービスを再起動しないコマンドである。

主要な強化項目は次のとおりである。

```text
# /etc/ssh/sshd_config の抜粋
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 4
AllowGroups sshusers
```

`PermitRootLogin no` は、rootアカウントでの直接ログインを禁止し、個人アカウントでログインしてから `sudo` を使う運用へ寄せる設定である。

設定変更は、再起動ではなく再読み込みで反映すると、接続中のセッションを維持したまま反映できる。

```bash
sudo sshd -t && sudo systemctl reload sshd
```

**警告**：`PasswordAuthentication no` を有効化する前に、公開鍵でログインできることを別のセッションで確認する。
確認せずに反映すると、鍵が正しく設定されていない場合にサーバーへ二度とログインできなくなる。

### 3.5 公開鍵認証の設定

クライアント側で鍵ペアを生成し、公開鍵をサーバーへ登録する。

```bash
ssh-keygen -t ed25519 -a 100 -C 'operator@mgmt01'
ssh-copy-id operator@web01
```

`-t` は鍵の種類、`-a` は鍵導出の反復回数（大きいほど総当たりに強くなる）を指定するオプションである。

**想定出力**：`Number of key(s) added: 1` が表示されれば、公開鍵が `~/.ssh/authorized_keys` へ追記されたことを意味する。

登録後は、鍵だけでログインできることを確認する。

```bash
ssh -o PasswordAuthentication=no operator@web01
```

`~/.ssh` ディレクトリとファイルの権限は、緩すぎるとSSH自体がログインを拒否する。

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

秘密鍵の管理を誤ると、鍵の窃取がそのままなりすましにつながるため、パスフレーズを付け、共有ストレージへ平文で置かない。

### 3.6 SELinuxによる強制アクセス制御

**SELinux（Security-Enhanced Linux）**は、RHEL系ディストリビューションで既定有効になっていることが多い強制アクセス制御の実装である。

```bash
getenforce
```

`Enforcing` はポリシー違反を実際に拒否する状態、`Permissive` は拒否せずログにのみ記録する状態、`Disabled` は機能そのものが無効な状態を示す。

アプリケーションが原因不明で失敗する場合、SELinuxによる拒否（AVC: Access Vector Cache 拒否）が疑わしい候補になる。

```bash
sudo ausearch -m AVC -ts recent
sudo ausearch -m AVC -ts recent | audit2why
```

`audit2why` は拒否理由を平易な文章として表示するコマンドである。
原因がポリシーとの不整合であり、意図した動作だと判断できる場合は、ブール値の調整で対応する。

```bash
sudo setsebool -P httpd_can_network_connect on
```

**警告**：`setenforce 0` でSELinuxを一時的に無効化して原因調査を済ませたつもりになると、本当の設定ミスを見落としたまま `Enforcing` へ戻し忘れる事故につながる。
原因は監査ログから特定し、無効化は最終手段として扱う。

### 3.7 AppArmorによる強制アクセス制御

**AppArmor**は、Ubuntu系ディストリビューションで既定有効になっていることが多い強制アクセス制御の実装であり、SELinuxとは異なりファイルパスを基準にポリシーを記述する。

```bash
sudo aa-status
```

`enforce mode` のプロファイル数は実際に制限を強制しているプロセス数、`complain mode` は違反をログに残すだけのプロセス数を示す。

特定プロファイルを一時的に緩めて調査する場合は、次のように切り替え、調査後は必ず戻す。

```bash
sudo aa-complain /usr/sbin/nginx
sudo aa-enforce /usr/sbin/nginx
```

### 3.8 Linuxのディスク暗号化

**LUKS（Linux Unified Key Setup）**は、Linuxで広く使われるディスク暗号化の標準規格である。

```bash
# 警告: 対象デバイスの既存データは失われる。新規ボリューム以外では特に慎重に扱う
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 data_crypt
sudo mkfs.xfs /dev/mapper/data_crypt
sudo mount /dev/mapper/data_crypt /mnt/data
```

実行にはroot権限が必要であり、復号鍵（パスフレーズやキーファイル）を失うとデータそのものへ二度とアクセスできなくなるという高いリスクを伴う。

クラウド環境の仮想マシンでは、ハイパーバイザー側やクラウドプロバイダー側の暗号化機能とLUKSの役割分担を事前に整理しておく。
両方を無計画に重ねると、鍵管理の窓口が増え、復旧手順が複雑になる。

### 3.9 監査ログ

Linuxの認証関連ログは、ディストリビューションによって保存先が異なる。

```bash
sudo grep -i failed /var/log/secure | tail -n 20   # RHEL系
sudo journalctl -u sshd --since today | grep -i fail
```

より詳細な監査が必要な場合は、**auditd**でシステムコールやファイルアクセスを監視する。

```bash
sudo auditctl -w /etc/passwd -p wa -k passwd_watch
sudo ausearch -k passwd_watch
```

`-w` は監視対象パス、`-p` は監視する操作（`r` 読み取り、`w` 書き込み、`x` 実行、`a` 属性変更）、`-k` は検索用のラベルを指定するオプションであり、root権限が必要である。
監視の追加自体は動作に影響しないが、監査ログの肥大化には注意する。

### 3.10 マルウェア対策

Linuxサーバーは伝統的にマルウェア対策製品の導入率が低いが、Windowsクライアントへファイルを経由させるサーバー（メール中継、ファイル共有など）では導入の要否を明示的に検討する。

```bash
sudo dnf install -y clamav clamav-update
sudo freshclam
sudo clamscan -r /var/www --infected --log=/var/log/clamscan.log
```

導入していない場合は、その事実自体を組織のリスク台帳へ明記しておく。
未導入を放置したまま記録もしないことが、最も避けるべき状態である。

### 3.11 管理用アカウントの分離

Linuxでは、`root` への直接ログインを避け、個人アカウントで `sudo` を使う運用が一般的である。

```bash
sudo visudo
```

```text
# /etc/sudoers.d/app-admins の例
%app-admins ALL=(ALL) ALL
operator ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

`visudo` は保存時に構文チェックを行うため、直接エディタでファイルを開いて保存するより安全である。
構文誤りは `sudo` そのものを使えなくする事故につながるため、必ず `visudo` 経由で編集する。

個々のコマンドに絞った許可（`NOPASSWD` 行）は利便性を上げる一方、対象コマンドの引数を悪用されると意図しない操作に使われる余地が残るため、対象コマンドは慎重に選ぶ。

---

## 4. Windowsでの実現方法

### 4.1 不要サービスの棚卸しと停止

```powershell
Get-Service | Where-Object { $_.StartType -eq 'Automatic' } |
  Select-Object Name, Status, StartType
```

`StartType` が `Automatic` のサービスは次回起動時にも自動的に立ち上がるため、不要であれば `Disabled` へ変更する。

```powershell
# 警告: 依存サービスへの影響を確認してから実施する
Stop-Service -Name Spooler
Set-Service -Name Spooler -StartupType Disabled
```

実行には管理者権限が必要であり、印刷スプーラーのように一見不要に見えても他の業務システムが依存している場合があるため、リスクは中程度と見積もる。

### 4.2 パッチ適用

小規模環境ではWindows Updateをそのまま使い、組織規模ではWSUS（Windows Server Update Services）やパッチ管理製品で統制する。

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
```

`HotFixID`（KB番号）は個々の修正プログラムを示す識別子であり、既知の不具合情報を調べる際にこの番号で検索する。

`PSWindowsUpdate` モジュールなど専用のモジュールを導入していれば、確認と適用をコマンドラインで完結できる。

```powershell
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot
```

**警告**：`-AutoReboot` を本番サーバーで無条件に使うと、業務時間中の予期しない再起動につながる。
メンテナンスウィンドウ内での実行に限定する。

### 4.3 パスワードポリシー

ドメイン環境では、既定のドメインパスワードポリシーをGPO（Group Policy Object）で管理する。

```powershell
Get-ADDefaultDomainPasswordPolicy
```

`LockoutThreshold` は連続失敗が何回でロックアウトするか、`MaxPasswordAge` はパスワードの最大有効期間を示す。

スタンドアロン機やワークグループ構成では、ローカルセキュリティポリシーで同等の設定を行う。

```powershell
net accounts
```

確認は一般ユーザーでも可能だが、変更には管理者権限が必要である。

### 4.4 RDPの強化

**RDP（Remote Desktop Protocol）**は、Windowsの標準的な遠隔デスクトップ接続プロトコルである。

```powershell
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections
```

`fDenyTSConnections` が `0` であればRDP接続が許可されている状態、`1` であれば拒否されている状態を示す。

**NLA（Network Level Authentication）**を有効にすると、フルのデスクトップセッションを確立する前に認証を要求するため、未認証のセッションがサーバー側の処理を消費することを防げる。

インターネットから直接RDPへ到達できる構成は、ブルートフォース攻撃の標的になりやすいため、次のいずれかで管理経路を絞る。

1. VPNまたは専用のジャンプホスト経由に限定する。
2. ファイアウォールで管理用ネットワークのみ許可する。
3. アカウントロックアウトポリシーを有効にする。

Windows ServerではOpenSSHも標準機能として選択肢に入るが、バージョンによって既定の有効・無効が異なる。

**警告**：RDPポート（既定3389）をインターネットへ直接公開したまま放置しない。

### 4.5 Windows Defenderによるマルウェア対策

```powershell
Get-MpComputerStatus |
  Select-Object AMServiceEnabled, AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated
Update-MpSignature
```

`AntivirusSignatureLastUpdated` が数日以上前であれば、定義ファイルの更新経路（インターネット到達性やWSUS経由の配信）に問題がある可能性を疑う。

確認は一般ユーザーでも可能な項目が多いが、更新の強制実行や設定変更には管理者権限が必要である。

### 4.6 BitLockerによるディスク暗号化

**BitLocker**は、Windowsの標準的なボリューム暗号化機能である。

```powershell
Get-BitLockerVolume
```

`ProtectionStatus` が `On` であれば暗号化保護が有効な状態、`VolumeStatus` はボリューム全体の暗号化進捗を示す。

**TPM（Trusted Platform Module）**の有無、仮想マシンでの対応状況は環境によって異なるため、導入前に対象ハードウェア・ハイパーバイザーの対応状況を確認する。

回復キーは、AD環境であればADへエスクロー（保管委託）する構成が一般的である。

**警告**：回復キーを暗号化対象ディスクの内部だけに保管しない。
ディスクを紛失・故障した場合、鍵ごと失われ復旧できなくなる。

### 4.7 監査ログとアカウント分離

```powershell
auditpol /get /category:*
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4672} -MaxEvents 10
```

イベントID 4672は「特別な権限が新しいログオンに割り当てられた」ことを示し、管理者権限でのログオンを追跡する手がかりになる。

管理用アカウントの分離は、日常業務用アカウントとは別に管理用アカウントを用意し、Administratorsグループへの所属を管理用アカウントに限定する形で行う。

```powershell
Get-LocalGroupMember -Group Administrators
```

確認には管理者権限が必要であり、メンバー変更は高リスクであるため、変更前後で棚卸しを行う。

組織によっては、ローカル管理者パスワードをホストごとに一意化する**LAPS（Local Administrator Password Solution）**を導入し、使い回されたパスワードが横展開の足がかりになることを防ぐ。

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| 遠隔管理の主な手段 | SSH | RDP、WinRM、Windows ServerではSSHも選択肢 |
| 公開鍵認証の位置づけ | SSH鍵が標準的な認証手段 | 証明書やWindows Helloなど、用途に応じた別手段 |
| 強制アクセス制御 | SELinux（RHEL系）、AppArmor（Ubuntu系） | 同等の必須機構はなく、AppLockerなど用途別の仕組みで代替 |
| マルウェア対策 | 追加導入が前提（ClamAVなど） | Windows Defenderが標準搭載 |
| ディスク暗号化 | LUKSなど | BitLocker |
| パッチ適用 | dnf/apt | Windows Update、WSUS |
| パスワードポリシーの管理 | PAM（pwquality、faillock） | ローカルセキュリティポリシー、GPO |
| 管理用アカウントの分離 | root直接ログイン禁止＋sudo | Administrators分離、LAPS |

強制アクセス制御は、Windowsに完全に同等な機構がないという非対称性がある。
このためWindows環境では、アプリケーション制御（AppLockerなど）やEDR（Endpoint Detection and Response）製品など、別の仕組みで同じ役割を補うことが多い。

---

## 6. コマンド例

### 6.1 遠隔管理ポートの露出を確認する

**目的**：SSHやRDPなど、遠隔管理用ポートがどのアドレスへ待ち受けているかを確認する。

**構文**：`ss [オプション]`、`Get-NetTCPConnection [パラメーター]`

```bash
sudo ss -tulpn | grep -E ':22|:3389'
```

```powershell
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 22, 3389
```

**主要オプション**：`-t`（TCP）、`-u`（UDP）、`-l`（待受のみ）、`-p`（プロセス情報）、`-n`（名前解決しない）。

**想定出力（Linux）**：

```text
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=812,fd=3))
```

**読み方**：ローカルアドレスが `0.0.0.0` であれば全インターフェースからの接続を受け付けている状態を示し、管理用ネットワークに限定していない可能性を疑う。

**権限**：プロセス情報を含めた表示には管理者権限（Linuxはroot、Windowsは管理者）が必要な場合がある。

**リスク**：低（参照のみ）。

### 6.2 SSHの有効設定を確認する

**目的**：パスワード認証やroot直接ログインが無効化されているかを、実際に適用されている設定値で確認する。

**構文**：`sshd -T`

```bash
sudo sshd -T | grep -iE 'passwordauthentication|permitrootlogin'
```

**主要オプション**：`-T`（テストモードで有効設定を展開して出力）、`-t`（構文チェックのみ）。

**想定出力**：

```text
passwordauthentication no
permitrootlogin no
```

**読み方**：設定ファイルに書いた値そのものではなく、複数ファイルや既定値を反映した最終的な有効値が表示される。

**権限**：root権限が必要である。

**リスク**：低（参照のみ）。

### 6.3 SELinuxの拒否イベントを調べる

**目的**：直近のSELinux拒否イベントを特定し、原因を平易な文章で確認する。

**構文**：`ausearch -m AVC -ts recent`

```bash
sudo ausearch -m AVC -ts recent
sudo ausearch -m AVC -ts recent | audit2why
```

**主要オプション**：`-m`（メッセージ種別）、`-ts`（開始時刻、`recent` は直近10分）。

**想定出力**：

```text
type=AVC msg=audit(1720000000.123:456): avc:  denied  { name_connect } for  pid=1234 comm="httpd"
```

**読み方**：`denied` の後ろの操作名（例では `name_connect`）が拒否された操作、`comm` が拒否されたプロセス名を示す。

**権限**：root権限が必要である。

**リスク**：低（参照のみ）。ブール値やポリシーの変更は中リスクであり、変更前に現状を記録する。

### 6.4 BitLockerの状態と回復キーを確認する

**目的**：暗号化状態と、回復キーの保護方式を確認する。

**構文**：`Get-BitLockerVolume [-MountPoint ドライブ文字]`

```powershell
Get-BitLockerVolume -MountPoint C: | Format-List *
```

**主要オプション**：`-MountPoint`（対象ドライブ）。

**想定出力**：

```text
MountPoint           : C:
VolumeStatus         : FullyEncrypted
ProtectionStatus     : On
EncryptionMethod     : XtsAes256
KeyProtector         : {Tpm, RecoveryPassword}
```

**読み方**：`EncryptionMethod` は暗号方式、`KeyProtector` は鍵の保護方法（TPMや回復パスワード）の一覧を示す。

**権限**：管理者権限が必要である。

**リスク**：低（参照のみ）。保護の一時停止や解除は高リスクであり、対象ボリュームを明示的に指定して行う。

### 6.5 管理者グループのメンバーを棚卸しする

**目的**：想定外のアカウントが管理者権限を持っていないかを点検する。

**構文**：`Get-LocalGroupMember -Group グループ名`、`getent group グループ名`

```powershell
Get-LocalGroupMember -Group Administrators | Select-Object Name, ObjectClass, PrincipalSource
```

```bash
getent group wheel
```

**想定出力（Windows）**：

```text
Name                    ObjectClass PrincipalSource
----                    ----------- ---------------
WINAPP01\Administrator  User        Local
LAB\svc-backup          User        ActiveDirectory
```

**読み方**：`PrincipalSource` が `ActiveDirectory` のアカウントは、ドメイン側での棚卸しも必要になる。

**権限**：Windowsは管理者権限、Linuxはグループ情報の参照自体は一般ユーザーで可能である。

**リスク**：低（参照のみ）。メンバー変更は中〜高リスクであり、変更前後で差分を記録する。

---

## 7. 実務上の注意点

1. 一時的に許可した「Any/Any」のようなファイアウォール例外は、期限を決めて管理し、期限切れ後に自動で見直す仕組みを持つ。
2. ハードニング手順は個々のサーバーへ手作業で適用するのではなく、テンプレート化されたイメージや構成管理ツールを通じて新規VMへ同じ状態を再現する。
3. セキュリティ設定の変更も、他の設定変更と同じく変更管理の対象に含める。
4. ディスク暗号化とバックアップは両立させる。暗号化鍵とバックアップの両方を同時に失うと、データは完全に復旧不能になる。
5. パッチ適用前には検証環境での動作確認を行い、本番への一括適用を避ける（詳細は第8章参照）。
6. 強制アクセス制御を無効化したまま長期間放置しない。原因調査後は必ず元の強制モードへ戻す。

---

## 8. セキュリティ上の注意点

1. 共有の管理者アカウント（複数人が同じID・パスワードを使う運用）は、操作の追跡を不可能にするため避ける。
2. LAPSなど、ホストごとにローカル管理者パスワードを一意化する仕組みの導入を組織方針として検討する。
3. 監査ログは、改ざんや削除への耐性を持たせるため、生成元とは別のサーバーへ転送・保管する。
4. 管理用のWeb管理画面やAPIを、必要な範囲を超えて外部へ公開しない。
5. 公開鍵の秘密鍵は、パスフレーズを付けたうえで、共有ストレージや構成管理ツールのリポジトリへ平文で置かない。
6. マルウェア対策を導入していないサーバーがある場合、その事実を組織のリスク台帳に明記し、代替の検知手段（ログ監視など）を検討する。

---

## 9. よくある障害

| 症状 | 典型的な原因 |
|------|--------------|
| SELinux有効環境でアプリだけが失敗する | AVC拒否、ブール値の未設定、ファイルコンテキストの不一致 |
| SSHの公開鍵認証でログインできない | `~/.ssh` や `authorized_keys` の権限過剰、パス誤り、SELinuxコンテキスト、鍵の不一致 |
| RDP接続ができない | NLA要件と接続元クライアントの不一致、ファイアウォール遮断、ネットワークレベルの疎通不良、アカウントロックアウト |
| BitLockerが回復キーを要求する | ハードウェア構成変更、TPMのクリア、UEFI設定変更、ファームウェア更新 |
| Windows Defenderの定義が更新されない | インターネット到達性の欠如、WSUS配信設定の不備、サービス停止 |
| sudo/管理者操作が急に使えなくなる | sudoersファイルの構文誤り、グループメンバーシップの変更、GPO配布によるローカルポリシー上書き |

---

## 10. 切り分け手順

1. **症状の再現条件を確認する**：特定ユーザーだけか、特定ホストだけか、全体的な現象かを切り分ける。
2. **直近の変更を確認する**：設定変更、パッチ適用、GPO配布、証明書更新など、直近の変更履歴を洗い出す。
3. **ログを確認する**：Linuxは `journalctl` や `/var/log/secure`、Windowsはセキュリティログとシステムログを確認する。
4. **強制アクセス制御の状態を確認する**：SELinuxは `getenforce` と `ausearch`、AppArmorは `aa-status` を確認する。
5. **権限とグループメンバーシップを確認する**：対象アカウントが期待どおりのグループに属しているかを確認する。
6. **一時的に強制モードを緩めて再現するかを確認する**（可能な場合のみ）：緩めた状態で再現しなくなれば、強制アクセス制御が原因である可能性が高まる。
7. **確認後は必ず元の状態へ戻す**：緩めた設定、無効化した機能は、調査終了後にすべて復元する。

```bash
getenforce
sudo ausearch -m AVC -ts recent | tail -n 20
sudo journalctl -u sshd -n 50 --no-pager
```

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20 -ErrorAction SilentlyContinue
Get-NetFirewallRule -DisplayGroup 'Remote Desktop' | Get-NetFirewallPortFilter
Get-BitLockerVolume
```

イベントID 4625は「アカウントのログオンに失敗した」ことを示し、失敗が集中している場合はロックアウトポリシーとの関係も確認する。

---

## 11. 章末問題

1. `PermitRootLogin no` にする目的を説明せよ。
2. SELinuxを原因不明のまま `Disabled` にしてはいけない理由を説明せよ。
3. 管理用アカウントを日常アカウントから分離する利点を説明せよ。
4. BitLockerの回復キーを暗号化対象のディスク内部だけに保管してはいけない理由を説明せよ。
5. パッチ未適用の状態が、他のハードニング対策を無効化しうる理由を説明せよ。
6. NLAがRDPのセキュリティにおいて果たす役割を説明せよ。
7. LAPSのようなローカル管理者パスワード一意化の仕組みが必要とされる理由を説明せよ。

---

## 12. 解答と解説

1. rootアカウントへの直接攻撃面を減らし、個人アカウントでログインしたうえで`sudo`を使わせることで、操作を個人に紐づけて追跡可能にするため。
2. `Disabled` にすると本当の設定ミスやポリシー不備が隠れたままになり、再度`Enforcing`へ戻したときに同じ問題が再発するため。原因は監査ログから特定すべきである。
3. 侵害や誤操作が発生した際の被害範囲を限定でき、誰がいつ管理操作を行ったかという監査可能性も高まるため。
4. ディスクを紛失・故障した場合、暗号化されたデータと回復キーの両方を同時に失い、復旧の手段がなくなるため。
5. パッチ未適用の状態は既知の脆弱性が残っている状態であり、他の対策（強制アクセス制御や監査ログなど）を迂回する入口として悪用されうるため。
6. NLAは、フルのリモートデスクトップセッションを確立する前段階で認証を要求するため、未認証の接続がサーバーのリソースを消費することを防ぎ、一部の攻撃手法への耐性を高める。
7. ローカル管理者パスワードが複数ホストで使い回されていると、1台の侵害がそのまま他の全ホストへの横展開につながるため、ホストごとに一意化することでその被害範囲を限定する。

---

## 13. ハンズオン演習

### 演習11-1 SSH公開鍵認証への切り替え

**前提**：`web01` へパスワード認証でログインできる状態であり、事前にスナップショット `before-ch11-ssh` を取得していること。

**実行**：

1. `mgmt01`（またはクライアント端末）で `ssh-keygen -t ed25519 -a 100` を実行し、鍵ペアを生成する。
2. `ssh-copy-id operator@web01` を実行し、公開鍵を登録する。
3. 別のターミナルを開いたまま、`ssh -o PasswordAuthentication=no operator@web01` でログインできることを確認する。
4. `web01` で `/etc/ssh/sshd_config` を編集し、`PasswordAuthentication no` へ変更する。
5. `sudo sshd -t && sudo systemctl reload sshd` で反映する。

**確認**：既存セッションを切断せずに新しいターミナルから鍵ログインできること、パスワードログインが拒否されることを確認する。

**元に戻す**：`sudo cp /etc/ssh/sshd_config.bak.<日付> /etc/ssh/sshd_config` と `sudo systemctl reload sshd` で復元する。

### 演習11-2 SELinux拒否イベントの調査

**前提**：`web01` がSELinux `Enforcing` モードで稼働しており、`httpd` または `nginx` が導入済みであること。

**実行**：

1. `getenforce` で現在のモードを確認する。
2. Webサーバーの設定ディレクトリを標準以外の場所（例：`/data/www`）に変更し、意図的にSELinuxコンテキスト不整合を発生させる。
3. `sudo ausearch -m AVC -ts recent` で拒否イベントを確認する。
4. `audit2why` で拒否理由を確認する。
5. `semanage fcontext` と `restorecon` で正しいコンテキストを付与する。

**確認**：修正後にWebサーバーが正常応答すること、`ausearch` に新規の拒否イベントが記録されないことを確認する。

**元に戻す**：設定ディレクトリを標準の場所へ戻すか、演習前のスナップショットへ復元する。

### 演習11-3 管理者グループの棚卸しとBitLocker確認

**前提**：`winapp01` が起動しており、ローカル管理者権限でログオンできること。

**実行**：

1. `Get-LocalGroupMember -Group Administrators` を実行し、現在のメンバーを記録する。
2. `Get-BitLockerVolume` を実行し、暗号化状態を記録する。
3. 想定外のメンバーが含まれていた場合、削除の要否を検討する（演習では削除せず記録のみでもよい）。

**確認**：記録した内容をベースラインシートとして保存し、次回棚卸し時の比較対象にする。

**元に戻す**：メンバー変更を行った場合は、記録した元の状態へ戻す。

---

## 14. 本章のまとめ

セキュリティは一度整えて終わる設定の集合ではなく、日々の運用のなかで維持し続ける状態である。

サービスの棚卸し、パッチ適用、認証の強化、強制アクセス制御、暗号化、監査ログ、管理用アカウントの分離は、どれか一つを緩めると他の対策の効果も下がるという関係にある。

次章では、それでもなお発生する障害に備え、バックアップと復旧の考え方を扱う。

次章: [第12章 バックアップと復旧](12_backup_and_recovery.md)


---


<!-- source: 12_backup_and_recovery.md -->

# 第12章 バックアップと復旧

バックアップは取っているが、戻したことは一度もない。

この状態は、実務上バックアップが存在しないのとほぼ同じである。

本章では、バックアップの目的、フル・差分・増分の違い、ファイルバックアップとシステムバックアップの違い、スナップショットとの違い、RPO（Recovery Point Objective）とRTO（Recovery Time Objective）、LinuxとWindows Server Backupでの実装、復旧テスト、障害復旧手順書までを扱う。

---

## 1. 学習目標

1. バックアップの目的を、単なるコピーの保持ではなく復元可能性として説明できる。
2. フル・差分・増分の違いと、それぞれの長所・短所を説明できる。
3. ファイルバックアップとシステムバックアップ、スナップショットの違いを説明できる。
4. RPOとRTOを要件として定義し、バックアップ方針へ落とし込める。
5. LinuxとWindows Server Backupで、基本的なバックアップと復元を実行できる。
6. 復旧テストの必要性と、障害復旧手順書に含めるべき項目を説明できる。

---

## 2. 基本概念

### 2.1 バックアップの目的

**バックアップ**は、障害、誤削除、ランサムウェア、サイト災害などが発生した際に、データを合意した時点の状態へ戻すための仕組みである。

バックアップの完了条件は「コピーが存在すること」ではなく「そのコピーから実際に復元できること」である。

コピーを取得しただけで復元を試したことがない状態は、いざというときに媒体の破損、権限の不足、手順の欠落といった問題が発覚し、復元できないという事態を招きやすい。

### 2.2 フル、差分、増分

| 方式 | 内容 | 長所 | 短所 |
|------|------|------|------|
| **フルバックアップ** | 毎回すべてのデータを取得する | 復旧の手順が単純（1世代を戻すだけ） | 取得に時間と容量がかかる |
| **差分バックアップ** | 直近のフルバックアップ以降に変更されたデータを取得する | 復旧はフル1世代＋最新の差分1世代で済む | フルからの経過日数が長いほど差分が肥大化する |
| **増分バックアップ** | 直近のバックアップ（フルまたは増分）以降に変更されたデータを取得する | 日々の取得が軽量で済む | 復旧にはフル以降のすべての増分が必要になり、途中の1世代が欠けると復旧できない |

差分と増分は、どちらも「変更分だけを取得する」という点では似ているが、増分は前回の増分からの差分、差分は常にフルからの差分という点で参照点が異なる。

実務では、フルと差分・増分を組み合わせ、容量と復旧手順の複雑さのバランスを取る運用が一般的である。

### 2.3 ファイルバックアップとシステムバックアップ

**ファイルバックアップ**は、指定したファイルやディレクトリを対象に保全する方式であり、個別ファイルの誤削除や上書きへの対応に向いている。

**システムバックアップ**は、OS自体の復旧に必要なボリュームや状態（ブート情報、レジストリ、システムファイルなど）を含めて取得する方式であり、ハードウェア障害時に別のマシンへ丸ごと復元する**ベアメタル復旧（Bare Metal Recovery）**を目的とする。

両者は排他的ではなく、多くの環境では業務データはファイルバックアップ、OS自体はシステムバックアップやイメージ取得という形で使い分ける。

### 2.4 スナップショットとの違い

**スナップショット**は、ある時点のディスク状態への参照を高速に作成する仕組みであり、仮想化基盤やストレージ側の機能として提供されることが多い。

スナップショットはバックアップの代替にはならない場合が多い。

理由は次のとおりである。

1. スナップショットの多くは元のディスクと同じストレージ上に存在するため、そのストレージ自体が壊れると、元データとスナップショットの両方を同時に失う。
2. ランサムウェアによる暗号化のように、書き込みそのものが破壊行為である障害では、スナップショットの取得タイミングによっては被害後の状態しか残らない。
3. スナップショットは長期間保持する設計になっていないことが多く、容量圧迫の原因にもなる。

退避先が元データと同一の障害領域にある時点で、それはバックアップの代替にならないと考えるのが安全である。

### 2.5 RPOとRTO

**RPO（Recovery Point Objective）**は、障害発生時にどれだけ古い時点までのデータ損失を許容するかを示す指標である。

**RTO（Recovery Time Objective）**は、障害発生からサービスを復旧させるまでにどれだけの時間を許容するかを示す指標である。

たとえばRPOが24時間、RTOが4時間という要件であれば、少なくとも日次のバックアップと、4時間以内に復旧を完了できる手順・人員・媒体を用意する必要がある。

RPOとRTOは技術者が独自に決めるものではなく、業務側の許容度をもとに合意し、文書として残す。

### 2.6 障害復旧手順書

**障害復旧手順書（DRP: Disaster Recovery Plan）**は、実際に障害が発生した際、担当者が迷わず復旧作業へ着手できるようにするための文書である。

手順書がないまま復旧を試みると、平常時であれば当たり前に思い出せる手順も、緊張した状況では抜け落ちやすい。

最低限、次の項目を含める。

1. 手順書の発動条件（どのような事象で本手順を使うか）
2. 連絡体制（誰にいつ連絡するか、エスカレーション経路)
3. 合意済みのRPOとRTO
4. 直近成功したバックアップの確認方法
5. 復旧手順そのもの（実行するコマンドを含む）
6. 復旧後の確認試験項目
7. 復旧に失敗した場合の切り戻し手順
8. 事後報告の様式

手順書は一度書いて終わりにせず、復旧テストのたびに実態と照らし合わせて更新する。

---

## 3. Linuxでの実現方法

### 3.1 ファイルバックアップの取得

```bash
# 警告: 本番では専用ツール、権限設計、暗号化を別途検討する
sudo mkdir -p /backup/web01
sudo tar -czf /backup/web01/etc-$(date +%F).tgz -C / etc
sudo rsync -aHAX --delete /var/www/ /backup/web01/www/
```

`tar` は指定ディレクトリをアーカイブ化する定番コマンドであり、`rsync` は差分転送に対応し、繰り返し実行しても変更分のみを効率よく同期する。

`rsync` の `--delete` オプションは、転送先にあって転送元にないファイルを削除するため、意図せず必要なファイルまで消してしまわないよう、対象ディレクトリを慎重に指定する。

取得したバックアップは、同一ホスト内に置くだけでなく、別ホストへ転送しておく。

```bash
rsync -a /backup/web01/ backup@backup-host:/srv/backups/web01/
```

### 3.2 システム寄りの保全

Linuxではシステム全体を単一の製品でイメージ化する文化がWindowsほど一般的ではなく、次のような組み合わせで代替することが多い。

1. 構成管理ツール（Ansibleなど）でOS設定を再現可能にしておき、障害時は「データを戻す」より「作り直して戻す」を選択肢に含める。
2. データベースなど整合性が必要なデータは、サービス停止時のダンプ取得、またはアプリケーション側のスナップショット連携機能を使う。
3. クラウドやハイパーバイザーのイメージ取得機能を使い、ボリューム単位でシステムを保全する。

### 3.3 cronによる定期実行

```bash
sudo crontab -e
```

```text
# 毎日2時15分にバックアップスクリプトを実行する例
15 2 * * * /usr/local/bin/backup-web01.sh >> /var/log/backup-web01.log 2>&1
```

定期実行は、実行されたことだけでなく、成功したことまで監視する。

終了コード、ログの内容、バックアップサイズの推移を確認し、静かに失敗し続けるバックアップジョブを放置しない。

### 3.4 バックアップの暗号化と整合性確認

バックアップデータをそのまま平文で保管すると、媒体の紛失や不正アクセスがそのまま情報漏えいにつながる。

```bash
# GPGでアーカイブを暗号化する例
gpg --symmetric --cipher-algo AES256 /backup/web01/etc-2026-07-29.tgz
```

`--cipher-algo` は使用する暗号方式を指定するオプションであり、復号にはパスフレーズまたは対応する鍵が必要になる。

暗号化したバックアップは、復号鍵を失うと復元不能になるため、鍵の保管場所をバックアップ本体とは別に管理する。

取得したアーカイブが壊れていないかは、チェックサムで確認できる。

```bash
sha256sum /backup/web01/etc-2026-07-29.tgz > /backup/web01/etc-2026-07-29.tgz.sha256
sha256sum -c /backup/web01/etc-2026-07-29.tgz.sha256
```

`borg` や `restic` のような専用バックアップツールでは、重複排除、暗号化、整合性検証が組み込み機能として提供されており、`tar`や`rsync`の組み合わせより運用の手間が少ない。

---

## 4. Windowsでの実現方法

### 4.1 Windows Server Backupの導入

```powershell
Install-WindowsFeature Windows-Server-Backup -IncludeManagementTools
```

**Windows Server Backup（WSB）**は、Windows Serverに標準で搭載されているバックアップ機能であり、ボリューム単位のバックアップとベアメタル復旧に対応する。

バックアップ先ディスクは、専用に用意したボリュームを指定する。

```powershell
# 警告: ターゲットボリュームの選択を誤るとデータ消失につながる
$policy = New-WBPolicy
$volume = Get-WBVolume -VolumePath 'C:'
Add-WBVolume -Policy $policy -Volume $volume
$target = New-WBBackupTarget -VolumePath 'E:'
Add-WBBackupTarget -Policy $policy -Target $target
Start-WBBackup -Policy $policy
```

`New-WBPolicy` はバックアップの設定（対象、宛先、スケジュール）をまとめたポリシーオブジェクトを作成し、`Start-WBBackup` はそのポリシーに従ってバックアップジョブを実行する。

実行状況は次のコマンドで確認する。

```powershell
Get-WBJob
```

GUIの「Windows Server Backup」コンソールからも同様の操作ができ、スケジュール設定、ベアメタル復旧、システム状態の選択などは要件に合わせて構成する。

### 4.2 ファイル単位のコピー

```powershell
robocopy C:\app\data D:\backup\appdata /MIR /R:2 /W:5 /LOG:C:\temp\robocopy.log
```

`robocopy` はファイル・フォルダーのミラーリングに強いコマンドであり、`/MIR` は宛先を送信元と完全に一致させるミラーリングオプションである。

**警告**：`/MIR` は、宛先にあって送信元にないファイルを削除するため、送信元と宛先のディレクトリ指定を取り違えると、想定していなかったファイルが削除される。

`/R`（リトライ回数）と `/W`（リトライ間隔秒数）は、ネットワークドライブなど一時的なアクセス不能を想定したオプションである。

### 4.3 クラウド・仮想化基盤のバックアップ

ハイパーバイザーやクラウドのバックアップサービスを利用する場合でも、ゲストOS内部のアプリケーション整合性を確認する必要がある。

**VSS（Volume Shadow Copy Service）**は、Windows上でアプリケーションに整合性のあるスナップショットを取得するための基盤であり、対応したVSSライターを持つアプリケーション（SQL Serverなど）であれば、バックアップ取得時に整合性のある状態でスナップショットが作られる。

VSS非対応のアプリケーションでは、バックアップ取得のタイミングでデータが中途半端な状態になっている可能性があるため、対応状況を事前に確認する。

### 4.4 タスクスケジューラによる定期実行

WSBのGUIからスケジュールを組む方法に加え、`wbadmin`をタスクスケジューラへ登録して独自のタイミングで実行する方法もある。

```powershell
Get-ScheduledTask -TaskName '*Backup*' -ErrorAction SilentlyContinue |
  Select-Object TaskName, State
```

**目的**：バックアップ関連のスケジュールタスクが有効な状態で登録されているかを確認する。

**読み方**：`State` が `Ready` であれば次回実行を待機している状態、`Disabled` であれば無効化されている状態を示す。

スケジュールが無効化されたまま放置されると、バックアップが長期間取得されない状態に気づけない。

---

## 5. 両OSの比較

| 観点 | Linux | Windows |
|------|-------|---------|
| 定番のファイル系ツール | tar、rsync、borg、restic等 | robocopy、Windows Server Backup |
| システム復旧の主な手段 | 構成管理による再構築＋データ復元、またはイメージ製品 | WSBのベアメタル復旧、イメージバックアップ |
| アプリケーション整合性 | サービス停止やダンプ取得との連携 | VSSライターとの連携 |
| スケジューラ | cron、systemdタイマー | タスクスケジューラ、WSBの予定機能 |
| 標準搭載のバックアップ機能 | ディストリビューション標準では限定的 | Windows Server Backupが標準搭載 |

LinuxはOS標準のバックアップ機能が薄い分、`tar`や`rsync`のような汎用ツールを組み合わせて構築する自由度が高く、Windowsは標準機能で一通りの流れが完結しやすいという違いがある。

---

## 6. コマンド例

### 6.1 バックアップジョブの実行結果を確認する

**目的**：直近のバックアップが成功したか、サイズと所要時間はどうだったかを確認する。

**構文**：`Get-WBJob [-Previous 件数]`

```bash
ls -lh /backup/web01 | tail -n 5
tail -n 50 /var/log/backup-web01.log
```

```powershell
Get-WBBackupSet
Get-WBJob -Previous 1
```

**主要オプション**：`-Previous`（直近何件分の履歴を表示するか）。

**想定出力（Windows）**：

```text
JobState        : Completed
StartTime       : 2026/07/29 2:15:03
EndTime         : 2026/07/29 2:31:47
Percentage      : 100
```

**読み方**：`JobState` が `Completed` であれば正常終了、`Failed` であれば失敗しており、詳細はイベントログを確認する。

**権限**：Linuxはログファイルの読み取り権限、Windowsは管理者権限が必要である。

**リスク**：低（参照のみ）。

### 6.2 復旧のドライランを行う

**目的**：本番データへ直接上書きする前に、別のパスへ復元して差分を確認する。

**構文**：`tar -xzf アーカイブ -C 復元先`、`Start-WBFileRecovery -RecoveryTarget 復元先`

```bash
sudo tar -xzf /backup/web01/etc-2026-07-29.tgz -C /tmp/restore-test
diff -r /tmp/restore-test/etc /etc | head -n 40
```

```powershell
# WSBのGUIまたはWbadminでの復元では、復元先を別フォルダーに指定できる
wbadmin start recovery -version:07/29/2026-02:15 -itemtype:File -items:C:\app\data -recoverytarget:D:\restore-test
```

**主要オプション**：`-version`（復元対象の世代を指定するタイムスタンプ）、`-recoverytarget`（復元先パス）。

**権限**：Linuxは対象ディレクトリへの読み取り権限、Windowsは管理者権限が必要である。

**リスク**：中。復元先を誤って本番パスに指定すると、意図せず上書きが発生する。

**想定出力の読み方**：`diff` で差分が出力されなければ、バックアップと現行状態が一致していることを意味する。

### 6.3 バックアップ先の空き容量を確認する

**目的**：宛先ストレージの空き容量が、次回以降のバックアップ取得に十分残っているかを確認する。

**構文**：`df -h パス`、`Get-Volume -DriveLetter ドライブ文字`

```bash
df -h /backup
```

```powershell
Get-Volume -DriveLetter E | Select-Object DriveLetter, SizeRemaining, Size
```

**想定出力（Linux）**：

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb1        50G   38G   12G  77% /backup
```

**読み方**：`Avail`（Windowsは`SizeRemaining`）が保持世代数×1回あたりの想定サイズを下回っている場合、近いうちにバックアップが容量不足で失敗する可能性が高い。

**権限**：一般ユーザーで実行可能である。

**リスク**：低（参照のみ）。

---

## 7. 実務上の注意点

1. **3-2-1ルール**（コピーを3つ、2種類以上の媒体、うち1つはオフサイト）を基本方針として意識する。
2. バックアップデータの暗号化と、暗号鍵の管理方法をセットで設計する。
3. バックアップを実行する専用アカウントは、日常の管理者権限アカウントとは分離する。
4. 保持世代数（何日分、何週分残すか）とそれに必要な容量を、運用開始前に見積もっておく。
5. バックアップのカタログ（管理台帳）が破損した場合に備え、復旧手順そのものを別途文書化しておく。
6. スケジュール失敗の見逃しを防ぐため、成功だけでなく失敗の通知経路も用意する。

---

## 8. セキュリティ上の注意点

1. バックアップデータへの書き換え・削除権限を、攻撃者に渡さないようにする。**不変ストレージ（Immutable Storage）**や、バックアップ専用アカウントへの権限分離が有効である。
2. バックアップ媒体上に、暗号化されていない機密情報（パスワード、鍵など）を残さない。
3. 復旧訓練を行う際、本番の資格情報をそのまま演習環境へ漏らさない。
4. ランサムウェア対策として、バックアップをオンラインで常時書き込み可能な共有だけに置かない。オフラインまたはオフサイトの保管先を必ず併用する。
5. バックアップ取得・復元の操作ログを記録し、誰がいつ実行したかを追跡できるようにする。

---

## 9. よくある障害

| 症状 | 確認すべき点 |
|------|--------------|
| バックアップジョブが失敗する | 宛先の空き容量、実行アカウントの権限、VSSの状態（Windows）、除外設定の誤り、ネットワーク到達性 |
| 復元したがアプリケーションが起動しない | 設定ファイルのパス依存、実行権限、環境変数や秘密情報の欠落、データベースの整合性 |
| バックアップの取得時点が想定より古い | スケジュール失敗の見逃し、RPO要件と実際の取得間隔の乖離 |
| 復旧に想定以上の時間がかかる | RTOが未検証のまま設定されている、媒体やネットワークの転送速度、手順書の不足による手戻り |
| 増分チェーンの一部が壊れている | 途中世代の削除・破損、保持ポリシーとチェーン依存の設計不備 |

---

## 10. 切り分け手順

1. **失敗の範囲を確認する**：特定ジョブだけか、全体のスケジュールが止まっているかを確認する。
2. **直近の変更を確認する**：バックアップ対象パスの変更、権限変更、ストレージの空き容量変化を確認する。
3. **ログを確認する**：Linuxはバックアップスクリプトのログ、Windowsはイベントログとバックアップ専用のログを確認する。
4. **宛先の状態を確認する**：ディスク容量、ネットワーク共有への到達性、権限を確認する。
5. **復元を実小規模で試す**：本番へ影響しない範囲で、実際に1ファイルでも復元できるかを確認する。
6. **RPO・RTOとの乖離を評価する**：確認した実際の取得間隔・所要時間が、要件を満たしているかを評価する。

```bash
tail -n 100 /var/log/backup-web01.log
df -h /backup
crontab -l
```

```powershell
Get-WBJob -Previous 5
Get-WinEvent -LogName 'Microsoft-Windows-Backup' -MaxEvents 30 -ErrorAction SilentlyContinue
Get-Volume -DriveLetter E
```

---

## 11. 章末問題

1. RPOとRTOの違いを説明せよ。
2. 増分バックアップだけを長期間続けることのリスクを説明せよ。
3. スナップショットをバックアップと呼んではいけない典型的な理由を説明せよ。
4. `robocopy` の `/MIR` オプションを使う際に注意すべき点を説明せよ。
5. 復旧テストを一度も実施していないバックアップに、どのようなリスクがあるかを説明せよ。
6. VSSがWindowsのバックアップにおいて果たす役割を説明せよ。
7. 3-2-1ルールの3つの要素を説明せよ。

---

## 12. 解答と解説

1. RPOは障害発生時に失ってよいデータ量の上限（どれだけ古い時点まで許容するか）を示し、RTOは復旧までに許容できる停止時間の上限を示す。
2. 増分の連鎖のどこか一世代でも欠損・破損すると、その時点以降のすべての復元ができなくなり、復旧手順も世代数が増えるほど複雑化するため。
3. スナップショットの多くは元データと同一のストレージ障害領域にあり、独立した退避先になっていないことが多いため。
4. `/MIR` は宛先にあって送信元にないファイルを削除するため、送信元と宛先の指定を取り違えると、意図しないファイル削除が発生する。
5. 実際に復元できるかどうかが未検証であり、媒体の破損、権限不足、手順の欠陥といった問題がいざというときに初めて発覚するリスクがある。
6. VSSは、アプリケーションが稼働中のままでも整合性のあるスナップショットを取得できるようにする基盤であり、対応するVSSライターを持つアプリケーションのデータを壊れていない状態で保全できる。
7. コピーを3つ保持すること、2種類以上の異なる媒体に保存すること、うち少なくとも1つをオフサイト（別の場所）に保管すること。

---

## 13. ハンズオン演習

### 演習12-1 ファイルバックアップと復元

**前提**：`web01` に重要でない検証用ディレクトリ（例：`/opt/sample-data`）が存在すること。

**実行**：

1. `sudo tar -czf /backup/sample-$(date +%F).tgz -C /opt sample-data` でバックアップを取得する。
2. `sudo tar -xzf /backup/sample-$(date +%F).tgz -C /tmp/restore-test` で別パスへ復元する。
3. `diff -r /opt/sample-data /tmp/restore-test/sample-data` で差分を確認する。

**確認**：`diff` の出力が空であること（差分がないこと）を確認する。

**元に戻す**：`/tmp/restore-test` を削除する。元データには変更を加えていないため、追加の戻し作業は不要である。

### 演習12-2 Windows Server Backupの取得と復元

**前提**：`winapp01` にバックアップ先として使える予備ボリューム（例：`E:`）があること。作業前にスナップショット `before-ch12-backup` を取得する。

**実行**：

1. `Install-WindowsFeature Windows-Server-Backup -IncludeManagementTools` を実行する。
2. `C:\app\data` のような検証用フォルダーを作成し、テストファイルを配置する。
3. WSBのポリシーを作成し、`E:` を宛先としてバックアップを実行する。
4. テストファイルを削除したうえで、ファイル単位の復元を実行する。

**確認**：削除したファイルが復元されること、`Get-WBJob` でジョブが `Completed` になっていることを確認する。

**元に戻す**：検証用フォルダーとバックアップポリシーを削除するか、`before-ch12-backup` スナップショットへ戻す。

### 演習12-3 RTOの計測

**前提**：演習12-1または12-2の復元手順が一度成功していること。

**実行**：

1. 復元操作の開始時刻と終了時刻を記録する。
2. 復元にかかった実際の時間を、事前に想定していたRTOと比較する。
3. 手順書に実測時間を追記する。

**確認**：手順書に実測値が反映されていることを確認する。

**元に戻す**：破壊的な検証を行った場合は、作業前のスナップショットへ復元する。

---

## 14. 本章のまとめ

バックアップの完了条件は、コピーの存在ではなく復元の成功である。

フル・差分・増分の使い分け、ファイルバックアップとシステムバックアップの違い、スナップショットとの違いを理解したうえで、RPOとRTOという業務要件に沿った方針を立て、復旧テストと障害復旧手順書の整備までを運用に組み込む。

次章では、ここまでの各章で扱ってきた要素を踏まえ、典型的な障害ごとの調査手順を両OSで整理する。

次章: [第13章 トラブルシューティング](13_troubleshooting.md)


---


<!-- source: 13_troubleshooting.md -->

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


---


<!-- source: A_command_comparison.md -->

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


---


<!-- source: B_lab_scenarios.md -->

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


---


<!-- source: C_glossary.md -->

# 付録C 用語集

本文初出でも展開しているが、検索用に再掲する。
アルファベット語を先に置き、続いて日本語術語を置く。

---

## C.1 アルファベット・略語

| 用語 | 説明 |
|------|------|
| ACL（Access Control List） | 主体ごとに許可や拒否を列挙するアクセス制御リスト |
| AD / AD DS（Active Directory Domain Services） | Windowsドメインのディレクトリサービス |
| AGDLP | アカウントをグローバルグループへ、それをドメインローカルへ、そこに権限を付ける設計パターン |
| API（Application Programming Interface） | プログラムがOSや他コンポーネントの機能を呼ぶ窓口 |
| AppArmor | Linuxの強制アクセス制御の実装の一つ。Ubuntuで一般的 |
| AVC（Access Vector Cache）拒否 | SELinuxが操作を拒否した記録 |
| BCD（Boot Configuration Data） | Windowsの起動設定データ |
| BitLocker | Windowsのボリューム暗号化機能 |
| Bug Check | Windowsカーネルが続行不能と判断した停止。いわゆるブルースクリーン |
| CA（Certificate Authority） | 証明書を発行する認証局 |
| CIDR | プレフィックス長でネットワーク範囲を書く表記（例: /24） |
| CLI（Command Line Interface） | 文字による操作インタフェース |
| CPU（Central Processing Unit） | 中央演算装置。使用率監視の主対象の一つ |
| cron / systemd timer | Linuxの定期実行の仕組み |
| DC（Domain Controller） | AD DSを提供し認証に応答するサーバー |
| DACL（Discretionary Access Control List） | オブジェクトの随意アクセス制御リスト（Windows） |
| DHCP（Dynamic Host Configuration Protocol） | IP等を自動配布するプロトコル |
| DNS（Domain Name System） | 名前とIPアドレスなどを対応づけるシステム |
| ETW（Event Tracing for Windows） | Windowsの詳細なイベント追跡基盤 |
| FHS（Filesystem Hierarchy Standard） | Linuxディレクトリ配置の標準的な考え方 |
| firewalld | RHEL系で多いファイアウォール管理サービス |
| FQDN（Fully Qualified Domain Name） | ホスト名をドメインまで含めて書いた名前 |
| FS（File System） | ファイルシステム |
| GPT（GUID Partition Table） | 現代的なパーティションテーブル方式 |
| GPO（Group Policy Object） | Active Directoryのグループポリシー設定単位 |
| GRUB / GRUB2 | Linuxで一般的なブートローダー |
| GUID | グローバル一意識別子 |
| HAL（Hardware Abstraction Layer） | ハードウェア差を吸収する層（Windows） |
| ICMP | ping等で使う制御メッセージプロトコル |
| IIS（Internet Information Services） | WindowsのWebサーバー役割 |
| inode | Linuxファイルシステム上のメタデータ構造。数の枯渇に注意 |
| IP（Internet Protocol） | パケット配送の基盤アドレス体系 |
| journald | systemdのログ収集コンポーネント |
| KB（Knowledge Base） | Microsoft更新の識別に使われる番号の通称 |
| Kerberos | チケットベースの認証プロトコル。時刻同期が重要 |
| LDAP / LDAPS | ディレクトリ照会のプロトコル。後者はTLS保護 |
| LVM（Logical Volume Manager） | Linuxの論理ボリューム管理 |
| LUKS | Linuxディスク暗号化の代表的仕組み |
| MAC（Mandatory Access Control） | 強制アクセス制御（SELinux/AppArmor等） |
| MBR（Master Boot Record） | 旧来のパーティションおよび起動方式 |
| MFA（Multi-Factor Authentication） | 多要素認証 |
| NAT（Network Address Translation） | アドレス変換。ラボの外部接続でよく使う |
| NIC（Network Interface Card） | ネットワークインタフェース |
| NLA（Network Level Authentication） | RDP接続前の認証強化 |
| NTP（Network Time Protocol） | ネットワーク経由の時刻同期 |
| NTFS | Windowsの標準的ファイルシステム |
| NTLM | Windowsの認証プロトコルの一つ。移行・制限の対象になりやすい |
| OOM Killer | Linuxでメモリ逼迫時にプロセスを強制終了する仕組み |
| OU（Organizational Unit） | AD内の管理用コンテナ |
| PAM（Pluggable Authentication Modules） | Linux認証の差し替え可能モジュール群 |
| PID（Process ID） | プロセス識別子 |
| PPID | 親プロセスのPID |
| PowerShell | Windows中心に使うコマンドラインシェルおよび言語 |
| RAID | 複数ディスクの冗長・性能構成（本編では概要レベル） |
| RDP（Remote Desktop Protocol） | Windowsの遠隔デスクトッププロトコル |
| ReFS | Windowsの耐性志向ファイルシステム。用途はバージョン依存 |
| RPO（Recovery Point Objective） | 許容できる最大データ損失（時間幅で表すことが多い） |
| RTO（Recovery Time Objective） | 許容できる最大停止時間 |
| rpm / dnf / apt / dpkg | Linuxのパッケージ管理ツール群 |
| rsyslog | syslog系のログ転送・記録デーモン |
| SAN / NAS | ストレージネットワークの形態。本編では概念として言及 |
| SCM（Service Control Manager） | Windowsサービスの管理機構 |
| Secure Boot | 署名付きブートチェーンを検証するファームウェア機能 |
| SELinux | Linuxの強制アクセス制御の実装の一つ。RHEL系で一般的 |
| SID（Security Identifier） | Windowsセキュリティ主体の識別子 |
| SMB | Windowsファイル共有などで使うプロトコル |
| SPN（Service Principal Name） | Kerberosでサービスを識別する名前 |
| SRVレコード | サービスの場所を示すDNSレコード。ADが利用 |
| SSD / HDD | ソリッドステートドライブ / ハードディスクドライブ |
| SSSD | Linuxでディレクトリ認証を仲介するサービス |
| SSH（Secure Shell） | 暗号化された遠隔ログインおよび転送 |
| Storage Spaces | Windowsのソフトウェア定義ストレージ機能 |
| sudo | 特定コマンドを別ユーザー（多くはroot）権限で実行する仕組み |
| systemd | 現代Linuxで一般的なinitおよびサービス管理 |
| TCP / UDP | トランスポート層プロトコル |
| TLS | 通信の暗号化と相手認証のプロトコル |
| TPM（Trusted Platform Module） | 鍵や測定値を守るセキュリティチップ |
| UAC（User Account Control） | Windowsの特権昇格確認の仕組み |
| UEFI | 現代のファームウェア仕様。起動処理に関与 |
| UID / GID | Linuxのユーザーおよびグループの数値ID |
| UNC経路 | `\\server\share` 形式のネットワークパス |
| VSS（Volume Shadow Copy Service） | Windowsの整合性あるスナップショット基盤 |
| WinRE | Windows回復環境 |
| WinRM | Windowsの遠隔管理プロトコル |
| WSB（Windows Server Backup） | Windows Serverのバックアップ機能 |
| WSUS | 組織内で更新を承認・配布するサーバー役割 |

---

## C.2 日本語術語

| 用語 | 説明 |
|------|------|
| アクセストークン | Windowsでログオン後の主体の権限情報 |
| 依存関係 | パッケージやサービスが他コンポーネントを必要とする関係 |
| インシデント | 想定外の障害やセキュリティ事象 |
| オペレーティングシステム（OS） | ハードウェアとアプリの間で資源管理と共通サービスを提供する基盤 |
| カーネル | OSの中核。特権モードで資源とデバイスを管理する |
| カーネルパニック | Linuxカーネルが続行不能になった状態 |
| クォータ | ユーザーやグループごとの使用量上限 |
| グループポリシー | AD配下へ設定を配布する仕組み |
| 権限の継承 | 上位オブジェクトのACLが配下へ伝播すること |
| 公開鍵認証 | 秘密鍵と公開鍵のペアで本人性を確認する方式 |
| ハードニング | 攻撃面を減らすための強化作業 |
| ハードリンク | 同一実体を複数の名前で指すリンク |
| バックアップ（フル） | 対象全体を保存する方式 |
| バックアップ（差分） | 直近フル以降の変更を保存する方式 |
| バックアップ（増分） | 直近バックアップ以降の変更を保存する方式 |
| パーティション | ディスク上の区画 |
| ファイアウォール | 通信の許可と拒否を制御するフィルタ |
| フォレスト | ADの最上位の境界。複数ドメインを含みうる |
| プロセス | 実行中プログラムの管理単位 |
| スレッド | プロセス内の実行の流れ |
| スナップショット | ある時点の状態への高速な参照。退避先が同じだとバックアップ代替にならないことが多い |
| セカンダリグループ | Linuxで追加所属するグループ |
| 絶対パス / 相対パス | 起点から全て書く経路 / 現在位置からの経路 |
| システムコール | ユーザー空間からカーネルへ依頼する公式な入口 |
| シンボリックリンク | 別パスへの参照。実体欠落でダングリングしうる |
| ゾーン（DNS） | DNSが管理する名前空間の単位 |
| タイムゾーン | 地域の標準時の設定 |
| デバイスドライバー | ハードウェアや仮想デバイスをカーネルが扱うためのソフトウェア |
| デフォルトゲートウェイ | 自サブネット外へ出すときの次の転送先 |
| ドメイン | 中央ディレクトリ配下で認証とポリシーを共有する構成 |
| ドメイン参加 | コンピュータアカウントをADへ登録しポリシーと認証を受けること |
| マウント | ファイルシステムをディレクトリツリーへ接続すること |
| メタデータ | 所有者、権限、時刻、サイズなど実データ以外の属性情報 |
| ユーザー空間 | 一般アプリケーションが動く、特権の低い領域 |
| ユニット（systemd） | systemdが管理する起動単位。`.service`など |
| リポジトリ | パッケージの配布元 |
| ルート（UID 0） | Linuxの特権ユーザー |
| レジストリ | Windowsの階層的な設定データベース |
| ローカルユーザー | そのマシン内だけで定義されるアカウント |
| ログローテーション | ログを世代管理し、肥大化を防ぐ仕組み |
| ワークグループ | 各ホストがローカルにアカウントを持つ構成 |
| 最小権限の原則 | 作業に必要な権限だけを与える考え方 |
| 証跡保全 | 障害やインシデント時にログや揮発情報を先に残すこと |
| 疎通 | 通信が届くこと。ICMP到達とTCPポート到達は別物として扱う |
| 待ち受け（Listen） | サービスが特定ポートで接続を受け付ける状態 |
| 名前解決 | ホスト名などをIPアドレスへ変換すること |
| 強制アクセス制御 | 従来の所有者権限に加え、ポリシーで行動を制限する制御 |

---

## C.3 改訂メモ

- 対象の中心：RHEL系、Ubuntu系（systemd）、Windows 11、Windows Server 2022以降、PowerShell、Active Directoryの基礎
- バージョン依存機能は本文でその旨を明記している
- コマンドの出力例は環境差があるため、読み方の説明を優先している
- 学習用ドメイン名 `lab.local` は本番設計にそのまま使わない

---

## C.4 本書のファイル一覧

| ファイル | 内容 |
|----------|------|
| [README.md](README.md) | 目的、目次、到達目標、ハンズオン構成 |
| [01_os_role_and_architecture.md](01_os_role_and_architecture.md) | 第1章 OSの役割と基本構造 |
| [02_install_and_initial_setup.md](02_install_and_initial_setup.md) | 第2章 インストールと初期設定 |
| [03_files_and_directories.md](03_files_and_directories.md) | 第3章 ファイルとディレクトリ |
| [04_users_groups_permissions.md](04_users_groups_permissions.md) | 第4章 ユーザー、グループ、権限 |
| [05_processes_and_services.md](05_processes_and_services.md) | 第5章 プロセスとサービス |
| [06_storage_and_filesystems.md](06_storage_and_filesystems.md) | 第6章 ストレージとファイルシステム |
| [07_network_management.md](07_network_management.md) | 第7章 ネットワーク管理 |
| [08_software_and_updates.md](08_software_and_updates.md) | 第8章 ソフトウェアと更新管理 |
| [09_logs_and_monitoring.md](09_logs_and_monitoring.md) | 第9章 ログと監視 |
| [10_active_directory_and_linux.md](10_active_directory_and_linux.md) | 第10章 Active DirectoryとLinux連携 |
| [11_security.md](11_security.md) | 第11章 セキュリティ |
| [12_backup_and_recovery.md](12_backup_and_recovery.md) | 第12章 バックアップと復旧 |
| [13_troubleshooting.md](13_troubleshooting.md) | 第13章 トラブルシューティング |
| [A_command_comparison.md](A_command_comparison.md) | 付録A コマンド対照表 |
| [B_lab_scenarios.md](B_lab_scenarios.md) | 付録B 実務シナリオ |
| [C_glossary.md](C_glossary.md) | 付録C 用語集 |

以上が本書の一式である。


---

