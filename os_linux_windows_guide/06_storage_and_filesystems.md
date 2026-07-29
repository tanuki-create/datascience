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
