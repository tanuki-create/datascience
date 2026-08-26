# オペレーティングシステム――Linux現象を内部モデルから説明する

本書はコマンド集ではない。`load average`、page fault、I/O待ち、container隔離を、CPU・memory・deviceを多重化し保護するOSのモデルから説明する。式は直感、図、定義の順で導入する。

---

## 第1章 OSは何をしているのか

### 学ぶ理由・現場の問題
CPUもmemoryも空いて見えるのにserviceが遅い。単一指標でなく、OSが資源を保護・抽象化・多重化する仕組みを読む必要がある。

### 中心概念・正式な定義
OSはhardware資源をprocessへ安全に割り当て、実行・記憶・I/Oの抽象を提供する特権softwareである。図は `application→system call→kernel policy/mechanism→CPU/memory/device`。throughput `X=completed/time`、utilization `U=busy/time`、平均同時滞在数 `L=λW`（Littleの法則）は資源待ちを結ぶ。kernelはpolicy（誰にいつ）とmechanism（どう切替える）を分ける。

```text
apps: process / file / socket
---------------- system-call boundary
kernel: scheduler / VM / VFS / network / drivers
hardware: CPU / RAM / disk / NIC
```

誤解はOSをGUIやLinux distributionと同一視すること。cloud VMでもguest OS、hypervisor、hostの層がある。

### 章末ワーク
**要点:** ①保護 ②抽象化 ③多重化 ④policy/mechanism分離 ⑤待ち時間を資源別に見る。
**誤解チェック:** 1.OS=kernel 2.CPU idleなら遅くない 3.fileは物理diskそのもの 4.system callは普通の関数と同コスト 5.containerにもOS資源が必要。
**基礎問題:** 1.三役を説明 2.抽象を三つ列挙 3.層図を書く 4.L=λWの単位確認 5.policy例。**応用問題:** 1.API遅延の資源仮説 2.VM層を追加 3.multi-tenant脅威分析。**設計問題:** batchとAPIの資源分離を設計。**調査課題:** Linux kernel documentationのsubsystem一覧を読む。
**知らないとする誤判断:** 使用率一つから原因を断定する。**次章:** hardwareとkernelの契約を扱う。

---

## 第2章 HardwareとOSの境界

### 学ぶ理由・現場の問題
memory order、cache、DMAを無視すると、kernelやdriverの挙動をsoftwareだけで説明できない。

### 中心概念・正式な定義
ISAは命令・register・exception等のsoftware-visible contract。MMUは仮想→物理address変換、deviceはregister/queueとinterrupt、DMAでmemoryへ転送する。図は `core↔cache↔memory`, `device --DMA--> RAM --interrupt--> CPU`。CPU時間概算は `T = instructions × CPI / frequency` だがcache missやstallでCPIが変わる。

```text
user instruction -> trap/exception -> kernel handler
device completion -> interrupt -> handler -> deferred work
```

誤解はclock周波数だけで性能を決めること。実務ではNUMA、virtualization、spectre対策、device queueに現れる。

### 章末ワーク
**要点:** ①ISAは境界契約 ②MMUが変換 ③cacheが平均遅延を変える ④DMAはCPU copyを減らす ⑤interruptは非同期通知。
**誤解チェック:** 1.DMAならCPU不要 2.cacheはOSに無関係 3.例外はerrorだけ 4.物理addressをappが直接使う 5.CPIは常に1。
**基礎問題:** 1.ISA定義 2.MMU役割 3.DMA図 4.CPI計算 5.exception/interrupt区別。**応用問題:** 1.NUMA配置 2.cache miss診断 3.IOMMUの保護。**設計問題:** NIC受信経路を層別化。**調査課題:** `/proc/cpuinfo`と公式architecture manualを対応付ける。
**知らないとする誤判断:** core追加に比例して速くなると見積もる。**次章:** 保護を成立させる特権levelへ進む。

---

## 第3章 Privilege Level

### 学ぶ理由・現場の問題
process一つの不具合がmachine全体を壊さない理由と、kernel脆弱性が重大な理由は同じ境界にある。

### 中心概念・正式な定義
CPU modeは実行可能命令とaddress accessを制限する。user modeは直接device設定やpage table変更をできず、kernel modeへは定義済みentry（trap、interrupt）で移る。保護条件は「主体が資源へ操作する前に、hardware強制可能な検査を通る」こと。

```text
user process --trap gate--> kernel --return-from-trap--> user
       no privileged instruction / no kernel pages
```

ring番号の個数はarchitecture依存で、OSは通常user/kernelの主要二層を使う。root userもuser modeのcodeを走らせ、権限とCPU modeは別である。

### 章末ワーク
**要点:** ①hardware強制 ②user/kernel mode分離 ③entry point制限 ④root≠kernel mode ⑤境界越えはattack surface。
**誤解チェック:** 1.sudoで全命令がkernel mode 2.kernel codeは失敗しない 3.mode switch=context switch 4.syscall以外のentryもある 5.user pageは常に安全。
**基礎問題:** 1.禁止命令例 2.trap経路 3.rootとの差 4.attack surface 5.mode bit役割。**応用問題:** 1.eBPF境界 2.hypervisor mode追加 3.kernel exploit影響。**設計問題:** privileged helperを最小化。**調査課題:** Linux capabilityとCPU privilegeを比較。
**知らないとする誤判断:** OSユーザー権限をCPU特権と同一視する。**次章:** 管理された入口system callを見る。

---

## 第4章 System Call

### 学ぶ理由・現場の問題
`read()`一回を「diskを読む」と理解すると、cache、blocking、partial result、copyの挙動を誤る。

### 中心概念・正式な定義
system callはuser processがkernel serviceを要求するABI上のentry。wrapper関数はregisterへ番号・引数を置きtrapし、kernelが検証・実行して結果/errnoを返す。`read(fd,buf,n)` は最大n byteで、短い成功も契約内。

```text
libc wrapper -> syscall instruction -> validate fd/pointer
 -> VFS/cache/device/wait -> return value -> errno mapping
```

式 `total = calls × fixed_boundary_cost + data_cost + wait` は小さいI/Oのbatch効果を示す。誤解はsyscall=library call、1 call=1 physical I/O。`strace`は境界観測で内部因果の全てではない。

### 章末ワーク
**要点:** ①ABI入口 ②kernelが引数検証 ③partial resultを扱う ④blocking可能 ⑤callとdevice I/Oは非対応。
**誤解チェック:** 1.printfは必ず1 syscall 2.read成功はn byte 3.errnoだけ見れば十分 4.syscallはprocess切替必須 5.zero-copyも制御callは要る。
**基礎問題:** 1.経路を描く 2.ABI/API差 3.partial read loop 4.EINTR説明 5.batch効果。**応用問題:** 1.N+1 syscall診断 2.nonblocking contract 3.io_uring比較。**設計問題:** streaming readerの境界処理。**調査課題:** `strace`で小プログラムのcall列を調べる。
**知らないとする誤判断:** function call数だけでI/O回数を推定する。**次章:** kernelが管理する実行単位processへ進む。

### 総合演習A（第1〜4章）
「container内APIのp99が時々10倍」を、hardware、privilege、syscall、queueの四層で仮説化し、各仮説を反証する観測を設計せよ。

---

## 第5章 Process

### 学ぶ理由・現場の問題
PIDをapplicationと同一視すると、fork、exec、zombie、namespace、signalの関係を誤る。

### 中心概念・正式な定義
processは独立した仮想address空間、resource handle、security contextを持つ実行container。programは静的code、processはその実行instance。典型状態は running/runnable/sleeping/stopped/zombie。`fork`は論理的複製、`exec`は同じprocess identityのprogram image置換。

```text
parent --fork--> parent + child --exec--> child(new program)
exit -> zombie(metadata) --wait by parent--> reaped
```

copy-on-writeで全memory即時copyを避ける。PIDは再利用され得る。実務ではsupervisor、signal、FD継承、container PID namespaceに接続する。

### 章末ワーク
**要点:** ①program≠process ②address spaceと資源集合 ③状態遷移 ④fork/exec分離 ⑤waitが終了metadataを回収。
**誤解チェック:** 1.zombieはCPUを消費 2.killは必ず強制終了 3.forkは全page即copy 4.execでPID必ず変化 5.PIDは永続ID。
**基礎問題:** 1.状態図 2.fork/exec説明 3.zombie原因 4.FD継承 5.COW。**応用問題:** 1.orphan処理 2.signal race 3.prefork server分析。**設計問題:** worker supervision設計。**調査課題:** `/proc/<pid>`の主要情報を意味付ける。
**知らないとする誤判断:** process終了を資源・子processの完全終了と同一視する。**次章:** process内のexecution streamを扱う。

---

## 第6章 Thread

### 学ぶ理由・現場の問題
threadを「軽いprocess」とだけ捉えると、共有memoryとstack固有性が生むraceを見落とす。

### 中心概念・正式な定義
threadはprocess資源を共有するschedulable execution context。各threadはprogram counter、register、stackを持ち、address spaceとopen file等を共有する。図は `process {heap/files; T1(stack,regs), T2(stack,regs)}`。作成・切替costは実装依存で、thread数はthroughputを単調増加させない。

```c
// x++ は通常 read-modify-write の複数段階
tmp = x; tmp = tmp + 1; x = tmp;
```

data raceの定義は言語memory modelに依存する。kernel thread、user thread、green threadを区別する。

### 章末ワーク
**要点:** ①実行文脈 ②process資源を共有 ③stack/registerは個別 ④scheduler mappingはruntime依存 ⑤共有が通信と危険を生む。
**誤解チェック:** 1.threadごとheap 2.x++は常にatomic 3.多threadほど高速 4.green threadもkernel threadと1:1 5.thread failureはprocessと無関係。
**基礎問題:** 1.共有/固有分類 2.interleaving列挙 3.stack役割 4.thread model比較 5.race定義。**応用問題:** 1.thread pool sizing 2.TLS leak 3.fork+thread危険。**設計問題:** CPU/I/O混在pool設計。**調査課題:** 使用runtimeのthread mappingを調べる。
**知らないとする誤判断:** threadを増やせば待ちもCPUも同時に解決すると考える。**次章:** 実行文脈を切り替えるcostを見る。

---

## 第7章 Context Switch

### 学ぶ理由・現場の問題
CPU使用率が高くないのにthroughputが落ちるとき、過剰な切替とcache locality喪失が隠れている。

### 中心概念・正式な定義
context switchはCPU上の実行contextを保存し別contextを復元すること。直接cost（scheduler、register、address-space処理）と間接cost（cache/TLB/branch predictorの局所性低下）がある。概算 `useful_fraction = useful_time/(useful_time + switch_overhead)`。

```text
T1 running -> interrupt/trap -> save T1 -> choose T2 -> restore T2
mode switchだけで同じTを継続する場合はcontext switchでないことがある
```

voluntary（block）とinvoluntary（preemption）を分ける。数だけで善悪を決めず、原因とworkloadを対応付ける。

### 章末ワーク
**要点:** ①状態保存復元 ②直接/間接cost ③mode switchと区別 ④voluntary/involuntary ⑤localityも測る。
**誤解チェック:** 1.syscallごと別processへ切替 2.switch costは固定 3.回数ゼロが最適 4.blockはvoluntaryになり得る 5.TLB影響なし。
**基礎問題:** 1.切替項目 2.式計算 3.二分類 4.mode差 5.metric列挙。**応用問題:** 1.lock contentionとの関係 2.vCPU steal追加 3.oversubscription診断。**設計問題:** worker数実験を設計。**調査課題:** `pidstat -w`等の指標定義を確認。
**知らないとする誤判断:** context switch数だけを削減目標にする。**次章:** 誰をいつ走らせるかというschedulingへ進む。

---

## 第8章 Scheduling

### 学ぶ理由・現場の問題
平均throughputを上げてもinteractive p99やdeadlineが悪化し得る。目的関数を決めなければschedulerを評価できない。

### 中心概念・正式な定義
schedulerはrunnable taskからCPU割当を選ぶpolicy。turnaround=`completion-arrival`、response=`first_run-arrival`、waiting=`runnable_not_running time`。公平性、throughput、latency、deadline、energyは競合する。Littleの法則 `L=λW` によりqueue長と待ち時間を結ぶ。

```text
run queue -> policy (priority/fair/deadline) -> CPU
CPU-bound remains runnable; I/O-bound alternates run/sleep
```

priority inversionは低priorityがlockを持ち高priorityを止める現象でpriority inheritance等を使う。nice値は予約CPU量そのものではない。

### 章末ワーク
**要点:** ①目的関数が必要 ②runnableとrunningを分ける ③workload型で挙動差 ④priority inversion ⑤queueがlatencyを作る。
**誤解チェック:** 1.load average=CPU使用率 2.priority高なら常に先 3.fair=同時間 4.I/O wait taskはrunnable 5.deadline policyはcapacity不要。
**基礎問題:** 1.三時間指標計算 2.Gantt chart 3.queue状態 4.inversion例 5.nice説明。**応用問題:** 1.API/batch分離 2.cgroup quota影響 3.convoy分析。**設計問題:** mixed workload policyを設計。**調査課題:** Linux CFS/EEVDFの公式説明を読む。
**知らないとする誤判断:** load average上昇をCPU飽和だけで説明する。**次章:** 各processへ独立memoryの錯覚を与える。

### 総合演習B（第5〜8章）
workerを32から512へ増やしてthroughputが下がった事例を、process/thread、run queue、switch、lock待ちから分析し、countermeasureを原因仮説順に提案せよ。

---

## 第9章 Virtual Memory

### 学ぶ理由・現場の問題
RSS、VSZ、OOMを物理memoryの単純な使用量とみなすと、共有、file mapping、overcommitを誤る。

### 中心概念・正式な定義
virtual memoryはprocessごとのvirtual addressを物理frameまたはbacking storeへ写像し、隔離・再配置・共有・需要割当を可能にする。page table写像 `f:(ASID,VPN) ⇀ (PFN,permissions)`、TLBはそのcache。

```text
VA=[VPN|offset] --TLB/page table--> PA=[PFN|offset]
P1 VPN7 ─┐
         ├-> shared PFN42 (read-only/code)
P2 VPN3 ─┘
```

予約address、committed memory、resident setは別。COW、mmap、shared libraryに現れる。pointer値は同じでもprocessが違えば物理先は異なり得る。

### 章末ワーク
**要点:** ①VA≠PA ②page tableで保護 ③TLBは変換cache ④予約/commit/resident分離 ⑤共有mapping可能。
**誤解チェック:** 1.VSZ=RAM使用 2.全VAにframeがある 3.TLB miss=page fault 4.mmap=即読込 5.共有pageは隔離不能。
**基礎問題:** 1.address分割 2.mapping図 3.RSS定義 4.COW説明 5.permission bit。**応用問題:** 1.overcommit障害 2.TLB reach 3.shared library accounting。**設計問題:** 大file処理方式選択。**調査課題:** `/proc/<pid>/smaps`項目を読む。
**知らないとする誤判断:** VSZの大きさだけでmemory leakと断定する。**次章:** mappingを固定size pageで実現する。

---

## 第10章 Paging

### 学ぶ理由・現場の問題
major/minor faultやswapを理解しないと、latency spikeをGCやdiskだけへ誤帰属する。

### 中心概念・正式な定義
pageはvirtual memory管理単位、frameは物理memory単位。page faultはaddress translationがpresentでない、またはaccess typeがpage permissionに違反したためCPUがkernelへtrapする例外である。前者はdemand allocation/read-inで解決できる場合があり、後者もcopy-on-writeならwrite可能な新frameを作って再開できるが、正当化できないaccessはsignal等になる。minorはbacking I/Oなしで解決、majorはbacking I/Oを要するのが典型。page size `p`ならoffset bitは `log2 p`。

```text
reference -> translation present and permission allows? yes -> access
              no -> valid VMA / COW? allocate, map, or load -> resume
                                  invalid/prohibited -> signal
```

replacementは将来参照不明のonline decision。working setがRAMを超えるとthrashing。huge pageはTLB効率と内部断片化を交換する。

### 章末ワーク
**要点:** ①page/frame分離 ②faultは例外経路 ③minor/major ④working set ⑤huge pageの交換。
**誤解チェック:** 1.page faultは常に異常 2.majorは必ずswap 3.swap無ならOOMだけ 4.LRUを完全実装 5.huge pageは常に有利。
**基礎問題:** 1.offset計算 2.fault経路 3.二分類 4.working set 5.fragmentation。**応用問題:** 1.thrashing診断 2.COW fault分析 3.random access予測。**設計問題:** analytics workloadのpage戦略。**調査課題:** `vmstat`のsi/soとfault指標を確認。
**知らないとする誤判断:** fault数だけでdisk I/O量を推定する。**次章:** processがheap領域を小さなobjectへ分配する。

---

## 第11章 Memory Allocation

### 学ぶ理由・現場の問題
free後もRSSが戻らない現象を即leakとすると、allocator cache、fragmentation、kernel page管理を混同する。

### 中心概念・正式な定義
kernelはpage単位、user allocatorはblock/object単位で管理する。external fragmentationは空き総量はあるが連続要求を満たせず、internalは割当block内の未使用。alignment `a`ではaddressが通常 `addr mod a=0`。arena/slab/size classは速度と局所性を改善する。

```text
runtime malloc -> arena/size class -> pages -> kernel VM
free -> allocator cache (still mapped) -> optionally return pages
```

memory leak、retention、fragmentation、高watermarkを分ける。外部resourceはallocatorの対象外。

### 章末ワーク
**要点:** ①二層allocation ②断片化二種 ③free≠OS返却 ④arenaはcontentionを減らす ⑤profileで保持経路を見る。
**誤解チェック:** 1.freeでRSS即低下 2.空き総量だけで大block可能 3.stackにfragmentationなし 4.allocator交換は意味不変 5.OOM原因はleakだけ。
**基礎問題:** 1.二断片化例 2.alignment計算 3.層図 4.retention差 5.size class。**応用問題:** 1.RSS plateau分析 2.arena増加 3.NUMA allocation。**設計問題:** object pool採否を決める。**調査課題:** 使用allocatorのstats/trim仕様を読む。
**知らないとする誤判断:** allocator内部保持をapplication参照leakと断定する。**次章:** 共有状態の順序を強制する。

---

## 第12章 Synchronization

### 学ぶ理由・現場の問題
lockを足せばraceが消えるという対症療法は、invariant、ordering、待ち条件を隠す。

### 中心概念・正式な定義
critical sectionは共有invariantを一時的に破って更新する領域。mutexは相互排他とhappens-before、semaphoreはpermit数、condition variableはpredicate変化を待つ仕組み。正しさは安全性（悪い状態にならない）とliveness（進捗する）で記述する。

```c
lock(m);
while (!predicate()) wait(cv, m); // release+待機登録は不可分。return前にmを再取得
consume();
unlock(m);
```

`wait` はmutex解放と待機への移行をsignalに対して不可分に行い、起床後にmutexを再取得してからreturnする。解放・sleep・再取得の全期間が一つのatomic sectionなのではない。`while`はspurious wakeupと、再取得までの間に他threadが状態を変える可能性に備える。atomicity、visibility、orderingを分ける。

### 章末ワーク
**要点:** ①invariantから設計 ②mutexはownership ③semaphoreはpermit ④CVはpredicate待ち ⑤safety/liveness両方。
**誤解チェック:** 1.volatileで排他 2.semaphore=mutex 3.signalはevent保存 4.ifでwait十分 5.atomic変数で複合invariant自動保護。
**基礎問題:** 1.critical section特定 2.invariant記述 3.CV loop 4.permit計算 5.happens-before。**応用問題:** 1.lost wakeup分析 2.lock粒度 3.reader-writer tradeoff。**設計問題:** bounded bufferを設計。**調査課題:** pthread/futexの関係を調べる。
**知らないとする誤判断:** data race消失を業務invariant成立と同一視する。**次章:** 待ち関係が循環すると何が起こるかを見る。

---

## 第13章 Deadlock

### 学ぶ理由・現場の問題
timeoutを足して停止を隠すと、部分更新と再試行stormに変わるだけで根本原因は残る。

### 中心概念・正式な定義
deadlockは主体集合が互いに、集合内の他主体だけが起こせるeventを待ち続ける状態。Coffman条件は相互排他、hold-and-wait、no preemption、circular wait。wait-for graphにcycleがあれば単一instance資源ではdeadlock。

```text
T1 holds A -> waits B
T2 holds B -> waits A      T1 -> T2 -> T1
```

countermeasureは優先順に、**Countermeasure: lock順序を全体で固定（assumed cause: circular wait）**、保持中待機を除く、検出後abort、timeoutをfailure boundaryとして扱う。分散DBにも同じgraphが現れる。

### 章末ワーク
**要点:** ①進捗不能 ②四必要条件 ③wait-for graph ④予防/回避/検出 ⑤timeoutは証明でない。
**誤解チェック:** 1.cycleは常にdeadlock 2.CPU 0%ならdeadlock 3.lock-freeならlivelockなし 4.timeoutで整合性自動回復 5.DBにも発生。
**基礎問題:** 1.四条件 2.graph作成 3.cycle検出 4.order提案 5.starvationとの差。**応用問題:** 1.callback lock inversion 2.DB/app lock複合 3.detector設計。**設計問題:** 複数account移動の順序。**調査課題:** Linux lockdepまたはDB deadlock reportを読む。
**知らないとする誤判断:** timeout延長でdeadlockを性能問題として処理する。**次章:** 永続的な名前付きbyte列の抽象へ進む。

### 総合演習C（第9〜13章）
「RSS上昇、major fault、worker停止」が同時に起きたserviceについて、leak、working-set超過、allocator保持、deadlockを原因仮説の優先順に並べ、countermeasureを `Countermeasure: 作業（assumed cause: 原因）` 形式で書け。

---

## 第14章 File System

### 学ぶ理由・現場の問題
`write()`成功を永続化完了と誤ると、crash後のdata lossやrenameの境界を誤設計する。

### 中心概念・正式な定義
file systemは名前→metadata/inode→data blockの写像と、永続状態更新規則を提供する。directoryはnameからobject identifierへのmapping。page cacheによりread/writeとdevice I/Oは分離され、durabilityにはflush/fsyncとdevice保証が関わる。Linux/POSIX系で新規fileやrename後の名前までcrash後に残したい場合、file本体の `fsync(fd)` だけでなく、directory entryを持つ親directoryの `fsync(dirfd)` が必要になり得る。

```text
path -> dentry/name lookup -> inode(metadata) -> page cache -> block layer
write -> dirty page --writeback--> device cache --durable media
```

journalingはmetadata/operation logでcrash consistencyを支えるが、application transaction全体は自動保証しない。典型的なdurable replaceは「同一filesystemの一時fileへwrite→一時fileをfsync→targetへrename→親directoryをfsync」である。renameのatomicityは同一filesystemか、既存targetとの交換かなど契約条件があり、atomic visibilityはdurabilityを意味しない。error処理とstorage/deviceのflush保証も確認する。

### 章末ワーク
**要点:** ①nameとinode分離 ②page cache ③visibility≠durability ④journal≠app transaction ⑤crash整合性を設計。
**誤解チェック:** 1.write成功でmedia永続 2.pathがobject identity 3.deleteでopen FD即無効 4.journalならdata lossなし 5.renameは全環境で同契約。
**基礎問題:** 1.lookup経路 2.hard/symbolic link 3.dirty page 4.fsync役割 5.inode説明。**応用問題:** 1.atomic file replace 2.log rotation 3.disk full crash。**設計問題:** config更新protocol。**調査課題:** ext4/XFSのdurability資料を読む。
**知らないとする誤判断:** fileが見えた時点をdurable commitとする。**次章:** file systemの下のblock requestを見る。

---

## 第15章 Block I/O

### 学ぶ理由・現場の問題
disk使用率100%やIOPSだけでは、queue、request size、latency、device parallelismを説明できない。

### 中心概念・正式な定義
block layerはlogical blockへのread/write requestをqueueing、merging、schedulingしdeviceへ送る。Littleの法則 `concurrency = IOPS × latency`。throughputは `IOPS × average_request_size`。HDDとSSD/NVMeでseek/parallel queue特性が違う。

```text
process -> page cache/fs -> bio/request -> scheduler/queue -> controller -> media
```

utilization高は飽和の手掛かりだがmulti-queue deviceでは解釈が異なる。direct I/Oはcacheを迂回してもalignmentやmetadata処理が残る。

### 章末ワーク
**要点:** ①request queue ②IOPS/size/latencyを組で見る ③Littleの法則 ④device特性 ⑤cache層を区別。
**誤解チェック:** 1.IOPS高=速い 2.SSDにqueue不要 3.direct I/O=zero copy 4.await=service timeだけ 5.sequentialは全device同利点。
**基礎問題:** 1.式計算 2.経路図 3.random/sequential 4.queue depth 5.flush説明。**応用問題:** 1.small write storm 2.NVMe並列性 3.noisy neighbor。**設計問題:** WAL/data I/O分離。**調査課題:** `iostat`列の定義を公式manualで確認。
**知らないとする誤判断:** `%util`単独でdeviceが性能上限と断定する。**次章:** device固有mechanismをkernel抽象へ接続する。

---

## 第16章 Device Driver

### 学ぶ理由・現場の問題
device障害をapplication retryだけで扱うと、queue reset、DMA、firmware、kernel stateの層を見落とす。

### 中心概念・正式な定義
driverはOSの共通subsystem interfaceとdevice固有protocolを接続するkernel component。probe/init、resource mapping、request submission、completion、error recovery、removeを管理する。

```text
VFS/net/block API -> subsystem -> driver -> MMIO/DMA -> device
                                      <- interrupt/completion -
```

driverは未信頼device inputを特権で処理するため重要境界。user-space driverやvirtual driverもある。device fileはhardwareそのものではなくkernel objectへのhandle。

### 章末ワーク
**要点:** ①共通/固有interface変換 ②lifecycle管理 ③DMA/interrupt協調 ④特権attack surface ⑤error recoveryはstate machine。
**誤解チェック:** 1.driverは全てkernel内 2.device file=physical device 3.interruptなしではdriver不可 4.firmware=driver 5.retryは常に安全。
**基礎問題:** 1.driver役割 2.lifecycle 3.MMIO 4.DMA 5.virtual driver例。**応用問題:** 1.hot unplug race 2.reset影響 3.IOMMU保護。**設計問題:** failure recovery state machine。**調査課題:** Linux driver model docsを読む。
**知らないとする誤判断:** device timeoutをnetwork/application層だけで解釈する。**次章:** completionをCPUへ通知するinterruptへ進む。

---

## 第17章 Interrupt

### 学ぶ理由・現場の問題
packet lossやlatency spikeはapplication以前にinterrupt集中、softirq backlog、CPU affinityから生じ得る。

### 中心概念・正式な定義
interruptは現在の命令流と非同期にhardware eventを通知し、保存されたcontextでhandlerへ制御を移す機構。重い処理を短いtop halfと遅延実行bottom halfへ分ける。高rateではinterrupt coalescingやpollingを使い、latencyとCPU効率を交換する。

```text
device event -> interrupt controller -> CPU handler(ack/queue)
                                      -> deferred work -> consumer wakeup
```

exception/trapは同期、interruptは典型的に非同期。割込み禁止区間は共有stateを守れるがlatencyを悪化させる。

### 章末ワーク
**要点:** ①非同期通知 ②context保存 ③top/bottom分割 ④coalescing trade-off ⑤affinity/locality。
**誤解チェック:** 1.interruptごとprocess switch 2.handlerでsleep可能という普遍則 3.多いほど低latency 4.pollingは常に無駄 5.exceptionと同義。
**基礎問題:** 1.経路図 2.二段処理 3.coalescing 4.affinity 5.interrupt storm。**応用問題:** 1.NIC queue mapping 2.priority inversion 3.polling threshold。**設計問題:** low-latency受信戦略。**調査課題:** `/proc/interrupts`をCPU/queueへ対応付ける。
**知らないとする誤判断:** packet処理costをuser process CPUだけで測る。**次章:** packetがsocketへ届くstack全体を見る。

---

## 第18章 Network Stack

### 学ぶ理由・現場の問題
接続timeout、再送、listen backlogを一括して「networkが悪い」とすると、どのqueue/状態か分からない。

### 中心概念・正式な定義
network stackはlink/IP/transport/socketのprotocol state machineを実装する。送信は `app buffer→socket→TCP/IP→qdisc→driver/NIC`、受信は逆。TCPはbyte streamでmessage境界を保たず、flow controlはreceiver、congestion controlはnetwork capacityへ適応する。

```text
accept queue != SYN queue != NIC ring != socket receive buffer
RTT, loss -> retransmission/congestion window -> application latency
```

帯域遅延積 `BDP=bandwidth×RTT` はin-flight必要量の目安。`send()`成功はpeer application受領を意味しない。

### 章末ワーク
**要点:** ①多層state machine ②複数queue ③TCPはstream ④flow/congestion分離 ⑤local success≠remote commit。
**誤解チェック:** 1.一send=一recv 2.listen backlogは一つだけ 3.UDPならlossなし 4.TCP再送でapplication exactly-once 5.bandwidthだけでthroughput決定。
**基礎問題:** 1.経路図 2.BDP計算 3.stream framing 4.二control差 5.handshake状態。**応用問題:** 1.SYN flood 2.small buffer高RTT 3.ephemeral port exhaustion。**設計問題:** length-prefix protocol。**調査課題:** `ss -tin`出力をTCP状態へ対応。
**知らないとする誤判断:** socket write成功を相手の業務処理成功とする。**次章:** kernel機構を組合せ隔離viewを作るcontainerへ進む。

### 総合演習D（第14〜18章）
DBのWAL fsync latencyとAPI送信遅延が同時上昇した事例を、page cache、block queue、driver/interrupt、network queueから分析する。平均だけでなくp99とqueue長を使う。

---

## 第19章 Containers

### 学ぶ理由・現場の問題
containerを小さなVMと思うと、kernel共有、resource accounting、host依存、security boundaryを誤る。

### 中心概念・正式な定義
containerはnamespaceによる資源view隔離、cgroupによるaccounting/limit、capability/seccomp等の権限制限を組み合わせたprocess。VMは通常別kernelを持つ。`usage <= limit`でもCPU quota periodやmemory reclaimでlatencyが出る。

```text
host kernel
 ├─ namespaces: pid,mount,net,user,... -> different views
 ├─ cgroups: cpu,memory,io,pids -> accounting/control
 └─ processes + filesystem image
```

imageは実行中containerではない。root-in-containerはuser namespace等の構成次第でhostへの意味が異なる。

### 章末ワーク
**要点:** ①processである ②kernel共有 ③namespace=view ④cgroup=資源制御 ⑤image/runtime分離。
**誤解チェック:** 1.containerごとkernel 2.namespaceだけでCPU制限 3.limit未満ならthrottleなし 4.imageはimmutable実行状態 5.rootは常にhost root。
**基礎問題:** 1.VM比較 2.namespace列挙 3.cgroup役割 4.layer説明 5.capability。**応用問題:** 1.CPU throttling 2.OOM accounting 3.escape threat。**設計問題:** multi-tenant isolation。**調査課題:** OCI runtime spec/cgroup v2 docsを読む。
**知らないとする誤判断:** container境界をVM同等のsecurity境界と無条件に扱う。**次章:** 内部状態を推測する観測へ進む。

---

## 第20章 Observability

### 学ぶ理由・現場の問題
metricを集めても、状態・event・resource demandの意味を誤ればdashboardは原因を隠す。

### 中心概念・正式な定義
observabilityは外部出力から内部状態を推定できる性質。OSではcounter、gauge、histogram、trace、profileを組み合わせる。CPUはuser/system/iowait/steal、memoryはRSS/cache/reclaim/fault、I/Oはrate/size/queue/latency、schedulerはrun queue/switch/waitを区別する。

```text
request latency
 ├─ runnable wait -> scheduler
 ├─ on-CPU -> profile
 ├─ blocked I/O -> block/network traces
 └─ fault/reclaim -> VM counters
```

USE法（utilization, saturation, errors）とworkload RED（rate, errors, duration）を接続する。iowaitは「CPUがdisk処理をしている割合」ではない。

### 章末ワーク
**要点:** ①意味からmetric選択 ②time accounting分解 ③rateと累積差 ④平均と分布 ⑤相関後にtrace/profile。
**誤解チェック:** 1.CPU100%=原因確定 2.iowait=process別disk待ち 3.RSS=private memory 4.counter値はrate 5.traceは常時無cost。
**基礎問題:** 1.指標分類 2.USE表 3.RED接続 4.rate算出 5.histogram説明。**応用問題:** 1.coordinated omission 2.container/host指標差 3.sampling bias。**設計問題:** OS診断dashboard。**調査課題:** procfs指標のkernel定義を確認。
**知らないとする誤判断:** dashboardの同時上昇を因果関係とする。**次章:** 観測を仮説検証の手順へ組む。

---

## 第21章 Performance Debugging

### 学ぶ理由・現場の問題
思いついたtuningを先に施すと、症状を移動させ再現性と根拠を失う。

### 中心概念・正式な定義
performance debuggingは期待SLOとの差を定義し、資源需要/待ちの仮説を優先し、反証可能な観測と介入を行う過程。response timeを `R = CPU service + runnable wait + memory stall + I/O wait + lock wait + network/application wait` と分解する。

```text
scope -> reproduce -> baseline -> hypotheses(priority)
 -> disconfirm with metrics/traces/profile -> controlled change -> verify/regress
```

countermeasureは原因順に記す: **Countermeasure: queue流入を制御（assumed cause: saturation）**、**Countermeasure: lock責務を分割（assumed cause: contention）**、**Countermeasure: working setを縮小（assumed cause: reclaim/thrashing）**。rareなhardware faultは証拠なしに上位へ置かない。

### 章末ワーク
**要点:** ①SLO差を数値化 ②時間分解 ③仮説優先順位 ④一変更一検証 ⑤再発防止まで。
**誤解チェック:** 1. profileだけでoff-CPU判明 2. 平均改善=p99改善 3. cache追加は常に改善 4. 再起動で原因確定 5. 相関metricは原因。
**基礎問題:** 1. R分解 2. 仮説三つ 3. 反証観測 4. baseline 5. regression。**応用問題:** 1. tail spike 2. noisy neighbor 3. benchmark validity。**設計問題:** 60分incident調査plan。**調査課題:** eBPF/perf/PSIの一つを公式資料で学ぶ。
**知らないとする誤判断:** tuning値変更を原因究明とみなす。**次章:** Linux上で全層を一つの事故として追う。

---

## 第22章 Linuxケーススタディ

### 学ぶ理由・現場の問題
本番障害はCPU、memory、I/O、lockの単一章に収まらない。観測の時系列と因果chainを統合する。

### 中心概念・正式な定義
事例: rollout後p99が80ms→2s、loadとmajor fault、disk latencyが上昇。第一仮説はworking set増加→reclaim/fault→I/O queue→request滞留。第二はthread増加→switch/lock。rare仮説はdevice故障。検査はdeployment相関だけでなくpage fault、PSI、block latency、off-CPU stackを揃える。

```text
larger cache per worker -> memory pressure -> reclaim/major faults
 -> block queue -> workers wait -> queueing -> timeout retries -> amplification
```

**Countermeasure: worker cacheを共有/上限化（assumed cause: working-set超過）**。**Countermeasure: admission controlとretry budget（assumed cause: queue amplification）**。単なるswap無効化は根因を直さない。

### 章末ワーク
**要点:** ①時系列 ②cause chain ③増幅loop ④反証 ⑤恒久策と緩和策を分ける。
**誤解チェック:** 1. rollout相関=code原因 2. major faultは結果だけ 3. retryは負荷軽減 4. cacheは必ずI/O削減 5. 再起動で修復完了。
**基礎問題:** 1. chain再描画 2. 一次/二次metric 3. rare仮説 4. rollback判断 5. SLO検証。**応用問題:** 1. 別仮説で反証plan 2. postmortem 3. capacity model。**設計問題:** overload-safe architecture。**調査課題:** 実在のLinux性能incident公開資料を一件分析。
**知らないとする誤判断:** 最初に改善した操作を根本原因と断定する。**次章:** 同じOS原理からcloudの錯覚を剥がす。

---

## 第23章 OS設計からCloudを理解する

### 学ぶ理由・現場の問題
managed/cloudを物理資源の消失と考えると、steal、quota、multi-tenancy、durability境界を見落とす。

### 中心概念・正式な定義
cloudはresource poolをAPIで割当てる制御planeと、実trafficを処理するdata planeを持つ。VMはhypervisorによるCPU/memory/device仮想化、containerはguest/host kernel機構、serverlessもprocess隔離とscheduler上にある。

```text
cloud API(control plane) -> desired allocation
request(data plane) -> guest OS -> virtual device -> hypervisor/host -> hardware
```

vCPUは専有coreとは限らず、volume flushのdurability boundaryもservice契約に依存する。autoscalingは遅延のあるfeedback controlで、capacity不足を瞬時に消さない。

### 章末ワーク
**要点:** ①物理資源は残る ②control/data plane ③仮想化層 ④共有由来のjitter ⑤service契約で保証確認。
**誤解チェック:** 1.vCPU=physical core 2.managedならOS不要 3.autoscale即応 4.object storage=file system同意味 5.multi-AZでapp整合性自動保証。
**基礎問題:** 1.層図 2.steal説明 3.quota例 4.control plane failure 5.durability境界。**応用問題:** 1.burstable CPU 2.volume latency 3.cold start。**設計問題:** SLO別に隔離/capacityを設計。**調査課題:** 使用cloudのinstance/volume保証文書を読む。
**知らないとする誤判断:** API抽象が下位resource contentionも消すと考える。**次章:** 典型誤判断を横断して総点検する。

### 総合演習E（第19〜23章）
Kubernetes上のserviceでCPU limit未満なのにp99が悪化した。quota period、run queue、memory reclaim、network interrupt、node noisy neighbor、application lockを仮説優先度順に並べ、観測とcountermeasureを設計せよ。

---

## 第24章 この分野を知らないエンジニアが陥りやすい誤判断

### 学ぶ理由・現場の問題
OS障害対応で最も危険なのは、観測語を知っていて内部状態を誤って推論すること。本章は頻度と影響の高い原因仮説から並べる。

### 中心概念・20の誤判断
1. **CPU idleだから資源問題でない**――I/O/lock/fault待ちを無視。時間をon/off CPUへ分解する。
2. **load average=CPU使用率**――runnable等の待ち集合を混同。定義とrun queueを見る。
3. **RSS増加=leak**――allocator/cache/共有を無視。mappingと保持pathを分離する。
4. **VSZ=必要RAM**――予約addressをresidentと混同。commit/RSSを見る。
5. **page fault=異常**――demand pagingを無視。minor/majorとlatencyを分ける。
6. **free=OSへ即返却**――allocator層を無視。arena/trim/fragmentationを確認。
7. **write成功=永続化**――page/device cacheを無視。fsyncとfailure contractを設計。
8. **一write=一disk I/O**――cache/mergeを無視。block traceで確認。
9. **一send=一recv**――TCP streamをmessageと誤認。framingを実装。
10. **socket send成功=相手処理完了**――end-to-end acknowledgment不足。application protocolを持つ。
11. **thread追加=高速化**――queue/switch/contentionを無視。workloadとcapacityでsizeを決める。
12. **lock追加=正しさ**――invariantを未定義。保護対象と順序を明文化する。
13. **timeout=deadlock解消**――部分状態を無視。循環を除き補償を設計する。
14. **context switchは全て悪**――blockingと公平性を無視。原因別に評価する。
15. **nice=CPU予約**――scheduler hintとquotaを混同。resource controllerを使う。
16. **container=軽量VM**――kernel共有を無視。namespace/cgroup/security境界を分ける。
17. **limit未満=throttleなし**――periodic quota/reclaimを無視。throttled time/PSIを見る。
18. **iowait=processのdisk待ち率**――CPU accountingを誤読。process/block traceを結ぶ。
19. **再起動で直った=根因解消**――queue/cache/state resetを原因と混同。再発条件を検証する。
20. **cloudでhardware問題は消える**――仮想化/共有層を無視。provider contractとguest/host指標を分ける。

正式な診断は観測 `O` から原因 `H` を一意に決めず、`P(H|O)` を更新する。図は `symptom→candidate states→discriminating observation→controlled countermeasure→verification`。

### 章末ワーク
**要点:** ①metric定義を読む ②層を分ける ③待ちを分類 ④仮説を反証 ⑤緩和と根治を分ける。
**誤解チェック:** 1.上記20から反証観測を五つ書け 2.visibility/durability差 3.VA/PA差 4.process/thread差 5.container/VM差。
**基礎問題:** 1.20例をCPU/memory/I/O/network/isolationへ分類 2.原因chainを三つ描く 3.rare仮説を一つ下位化 4.単位を確認 5.観測限界を書く。**応用問題:** 1.自社incident再分析 2.誤dashboard改修 3.capacity model。**設計問題:** symptom別runbookを、countermeasureとassumed causeの対で設計。**調査課題:** kernel docs、tool manual、cloud contractを一つの事例で突合する。
**知らないとする誤判断:** metric名を知ることを、内部モデルから因果を説明できることと同一視する。**次の学習:** 並行分散でordering、DBでWAL/MVCC、securityでtrust boundaryを深める。

---

## 最終総合演習
1. 高負荷APIの一requestをCPU命令、syscall、scheduler、page、filesystem、block、networkの時系列で描く。
2. 「DBが遅い」をalgorithm、OS、DB、concurrency、probabilityの五領域で仮説化し、各仮説の識別観測を示す。
3. containerのOOM/CPU throttle/network dropが連鎖するincidentを設計し、SLO、telemetry、admission control、recoveryを提案する。
4. visibility・atomicity・durabilityを持つfile更新protocolを実装し、kill/power-lossを模した試験を設計する。

## 参考文献への道標
- [Linux kernel documentation: EEVDF scheduler](https://docs.kernel.org/scheduler/sched-eevdf.html)――現行実装例。公平性という概念と特定実装を区別して読む。
- [Linux kernel documentation: cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)――階層、controller、weight/limit/protectionの一次資料。
- [Linux man-pages: fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html)――file data/metadataの同期と、directory entryにはdirectory側の明示的 `fsync` が必要という境界を確認する。
- [Linux kernel documentation](https://docs.kernel.org/)（memory management, VFS, block, networking）。
- `man 2` system calls と `man 7` conventions/protocols。
- John L. Hennessy & David A. Patterson, *Computer Architecture: A Quantitative Approach*。
- Remzi H. Arpaci-Dusseau & Andrea C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*。
- Brendan Gregg, *Systems Performance*。

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **仮想化・多重化・隔離** 直感的には、OSは有限のCPU、memory、deviceを、各programが自分専用の資源を持つように見せながら分配する。正式には、address space、process、file、socketなどの抽象を機構へ写し、時間・空間の多重化と保護境界を実現する。実務では、抽象上の値と物理資源の消費を結び、quota、noisy neighbor、権限境界、capacityを判断する。
2. **mechanismとpolicyの分離** 直感的には、「何ができるか」と「誰をいつ優先するか」は別の問題である。正式には、context switch、page mapping、I/O発行などの機構と、scheduler、replacement、admissionなどの方針を分け、方針が最適化する目的と制約を明記する。実務では、metricを改善する設定変更が公平性やtailを悪化させないかを検討し、workloadに応じてpolicyを交換可能にする。
3. **queue・待ち時間・feedback** 直感的には、資源がほぼ満杯になると、小さな到着増加が長い待ち行列へ増幅される。正式には、到着率、service time、utilization、queue lengthを区別し、retry、autoscaling、backpressureを遅延を持つfeedback loopとして扱う。実務では、CPU使用率だけでなくon/off-CPU時間とqueueを観測し、bounded queue、admission control、retry budgetを設計する。
4. **indirection・cache・working set** 直感的には、速く見える抽象の背後には、address translationや複数層cacheがあり、局所性の仮定が崩れると性能が段差状に変わる。正式には、virtual/physical address、page table、buffer/page/device cache、TLBなどの対応関係と、活動中の集合が容量内に収まるかを追う。実務では、RSSやhit率だけで判断せず、保持経路、miss費用、reclaim、writeback、durability境界を調べる。
5. **失敗境界と因果観測** 直感的には、system callの成功、相手の受信、永続化はそれぞれ異なる完了であり、一つのmetricから内部原因は一意に決まらない。正式には、visibility・atomicity・durabilityの保証点を層ごとに定め、観測 `O` から複数仮説 `H` を識別する追加観測を選ぶ。実務では、timeout、crash、power loss、部分書込みを含むprotocolと、時系列・trace・counterfactualに基づく障害診断を設計する。

### 専門家の意見が根本的に分かれる3つの論点

1. **kernelへ機能を集約するか、最小kernelとuser spaceへ分解するか**
   - **立場A――monolithic寄りに主要serviceをkernel内で統合する。** 最も強い主張は、頻繁なIPCとaddress-space crossingを避け、共有された内部状態を用いて高性能かつ一貫したresource管理を実現でき、成熟した統合実装は現実のhardwareを最も広く支えられるというものだ。
   - **立場B――microkernel寄りに最小機構だけを特権化する。** 最も強い主張は、driverやserviceの障害と権限を隔離し、TCBを小さくすれば、安全性の検証、更新、障害回復を構造的に改善できるというものだ。IPC費用は設計とhardware支援で抑えられ、隔離の利益は障害時に現れる。
   - 判断は、性能予算、security/safety認証、driver ecosystem、障害隔離の価値、更新頻度、IPC実装、hardware特性で変わる。
2. **throughputと平均効率を優先するか、予測可能なtailと公平性を優先するか**
   - **立場A――batch化、局所性、総work完了量を最大化する。** 最も強い主張は、switchやcache missを減らして全体capacityを上げれば、多くの利用者の待ち時間も結果的に下がり、有限資源から最大の仕事量を得られるというものだ。
   - **立場B――preemption、reservation、deadlineで予測可能性を守る。** 最も強い主張は、平均が良くても一部taskの飢餓やdeadline missは契約違反であり、interactive、multi-tenant、real-time systemでは余裕を費やしてでも上界と公平性を与える必要があるというものだ。
   - 判断は、workloadのinteractive/batch比、deadlineの硬さ、tenant間の信頼、switch費用、SLOのpercentile、余剰capacityで変わる。
3. **overcommitで利用率を高めるか、reservationと静的隔離で余裕を確保するか**
   - **立場A――統計的多重化と動的回収を活用する。** 最も強い主張は、全taskが同時にpeakへ達することは少なく、memory overcommit、work-conserving scheduling、elastic allocationにより、同じhardwareで大幅に多い仕事を処理できるというものだ。
   - **立場B――必要資源を予約し、干渉を制限する。** 最も強い主張は、相関したpeakや障害時には統計的仮定が同時に崩れ、reclaim、throttling、retryが正のfeedbackを作るため、重要workloadには利用率よりfailure containmentが必要だというものだ。
   - 判断は、peakの相関、overload時の損失、kill/throttle契約、autoscaling遅延、tenant優先度、観測とadmission controlの精度で変わる。

### 深い理解と暗記を見分ける10の質問

1. CPU使用率が40%なのにrequest p99が悪化した。I/O待ち、lock、run queue、quota throttling、page faultの仮説を、互いに識別できる観測とともに優先順位付けせよ。
2. processのRSS増加をmemory leakと断定できない理由を、anonymous/file-backed/shared mapping、allocator、cache、到達可能性に分け、原因別のcountermeasureを設計せよ。
3. `write`が成功した直後に電源断してもfile更新を失わないprotocolを、data、metadata、directory entryの順序とfailure pointを含めて設計し、atomicityとdurabilityの違いを示せ。
4. thread数を2倍にしてthroughputが下がった事例を、service demand、run queue、context switch、cache、lock contentionから構成し、最適値を測る実験を提案せよ。
5. containerがCPU limit未満に見えるのに周期的に停止する。quota period、複数coreでのburst、accounting windowを使って説明し、dashboardの集約方法をどう直すか述べよ。
6. page cacheを増やす最適化が、かえってtail latencyを悪化させる反例を作れ。working set、dirty page、writeback、reclaim、I/O queueの因果chainを示せ。
7. 一回の`send`と一回の`recv`が対応しないことを前提に、message境界、部分送受信、相手processのcrash、再送を扱うapplication protocolを設計せよ。
8. throughputを最大化するschedulerとdeadlineを守るschedulerが同じworkloadで異なる判断をする例を作り、どのSLOなら余剰capacityを予約する価値があるか論じよ。
9. 再起動で症状が消えた障害について、再起動が同時に消したqueue、cache、lock、process stateを分離し、根本原因を再現する安全な実験を設計せよ。
10. cloud VMのvCPU、volume、networkが専用hardwareのように見える一方で共有資源であることを、guest/host/control plane/data planeの層に分け、provider側を直接観測できない条件での反証計画を示せ。
