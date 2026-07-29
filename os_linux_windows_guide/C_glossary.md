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
