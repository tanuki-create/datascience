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
