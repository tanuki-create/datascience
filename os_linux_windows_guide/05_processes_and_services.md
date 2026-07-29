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
