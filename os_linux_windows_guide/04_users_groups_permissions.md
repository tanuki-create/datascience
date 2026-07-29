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
