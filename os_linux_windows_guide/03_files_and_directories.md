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
