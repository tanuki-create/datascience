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
