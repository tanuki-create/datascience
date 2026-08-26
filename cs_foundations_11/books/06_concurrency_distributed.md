# 並行・並列・分散システム――障害時から正しさを組み立てる

本書は共有メモリからネットワーク越しの複製までを、「観測できる順序」「保持すべき不変条件」「失敗後にも言える保証」で統一する。正常系のsequence diagramだけで設計を終えず、任意の命令間での停止、遅延、重複、再順序化を先に置く。記述は2026-08-27時点の一次資料を確認したが、特定製品より長寿命な原理を中心にする。

**関連巻:** scheduler・virtual memory・同期primitiveの下層は [オペレーティングシステム](05_operating_systems.md)、transaction・MVCC・replicationの具体化は [データベース理論](07_database.md)、failure率とtailの定量化は [確率・統計](08_probability_statistics.md)、脅威下のidentity・fencing・incidentは [情報セキュリティ](11_security.md) を参照する。

## 第1章 順番どおりには動かない世界

### この章を学ぶ理由
ソースの行順、実行順、他threadからの観測順、外部効果の確定順が異なることを設計の出発点にする。
### 現場の問題
ログ順を原因順と誤認し、再現しない残高不整合を「偶発」と処理する。
### 中心概念と正式定義
executionはevent集合Eと、program order、read-from、synchronizes-with等の関係からなる。happens-before `→` は順序関係の推移閉包で、`a→b` でなければ同時刻という意味でなく順序を確定できない。interleaving数は二threadが各m,n stepなら `C(m+n,m)`。
### 直感→図解→数式→例→実装または疑似コード
`T1: read x; write x+1` と `T2: read x; write x+1` は `R1,R2,W1,W2` となり更新を失う。`x += 1` を一つの原子的stepだと思わない。
### よくある誤解
単一coreなら競合しない、ログtimestampが全順序を与える、低頻度なら正しさ問題でない、はいずれも誤り。
### 実務接続
thread、signal、async callback、DB transaction、message consumerのすべてに順序の未確定性が現れる。
### 要点
- 行順と観測順を分ける。- event間の関係でexecutionを表す。- 非原子的操作を分解する。- 未順序は同時刻を意味しない。- 全interleavingを想像する。- 障害注入で境界を試す。
### 誤解チェック
1. 一行は原子的か。2. 単一coreならraceはないか。3. timestampは因果順か。4. 再現率は正しさか。5. `a↛b`ならb→aか。
### 基礎問題
1. 二incrementのinterleavingを列挙せよ。2. lost updateを説明せよ。3. event graphを書け。4. 外部I/Oをstep分割せよ。5. 終了点を5箇所置け。
### 応用問題
1. 三threadの順序数を求めよ。2. replay logの限界を述べよ。3. deterministic scheduler試験を設計せよ。
### 設計問題
在庫減算について、不変条件と全停止点、観測可能な中間状態を定義せよ。
### 調査課題
任意runtimeのthread/async scheduling保証を仕様から調べよ。
### 知らないとする誤判断
ログに先に出た処理が原因としても先だと断定する。
### 次章接続
重なりを扱うconcurrencyと同時実行資源を使うparallelismを分ける。

## 第2章 ConcurrencyとParallelism

### この章を学ぶ理由
正しさの構造と速度向上の構造を混ぜず、別々に設計する。
### 現場の問題
async化をCPU高速化だと期待し、core追加を競合解決だと思う。
### 中心概念と正式定義
concurrencyは複数taskの進行期間が重なる構成、parallelismは物理的に同時実行する性質。work `T1` とcritical path `T∞` に対し、p processor時間は下界 `Tp≥max(T1/p,T∞)`。Amdahl則は直列割合sでspeedup `≤1/(s+(1-s)/p)`。
### 直感→図解→数式→例→実装または疑似コード
一人の料理人が鍋待ち中に切るのがconcurrency、二人が同時に作るのがparallelism。I/O taskはasync、独立CPU chunkはworker pool候補。
### よくある誤解
concurrentならparallel、threadを増やせば速い、順次版より結果が同じなら安全、とは限らない。
### 実務接続
event loop、OS thread、GPU、build graph、web request poolでwork/spanを使う。
### 要点
- concurrencyは構成。- parallelismは実行資源。- 正しさと性能を分ける。- workとspanを測る。- 直列部が上限を作る。- 粒度とoverheadを含める。
### 誤解チェック
1. asyncはCPU parallelか。2. 1coreでconcurrency可能か。3. p倍coreで必ずp倍か。4. spanは総仕事か。5. thread数は最適化変数か。
### 基礎問題
1. task DAGを描け。2. T1,T∞を求めよ。3. Amdahl速度を計算せよ。4. I/O/CPU taskを分類せよ。5. overheadを列挙せよ。
### 応用問題
1. pipeline parallelismを分析せよ。2. oversubscriptionを説明せよ。3. Gustafson則と比較せよ。
### 設計問題
画像変換serviceの受付、download、CPU変換、uploadの実行モデルを設計せよ。
### 調査課題
利用言語runtimeのworker/thread/event loop構成を一次資料で調べよ。
### 知らないとする誤判断
async構文へ書き換えればCPU処理も自動で高速化すると考える。
### 次章接続
進行が重なると、共有状態の複合操作にraceが生じる。

## 第3章 Race Condition

### この章を学ぶ理由
結果がtimingに依存する状態を、再現性でなく競合関係から検出する。
### 現場の問題
check-then-act、lazy initialization、counter更新が負荷時だけ壊れる。
### 中心概念と正式定義
race conditionはeventの相対順で正しさが変わる状態。data raceは言語memory model上、同じlocationへの競合access（少なくとも一方write）がhappens-beforeで順序付けられないこと。data race-freeでも複数resourceのlogical raceはあり得る。
### 直感→図解→数式→例→実装または疑似コード
`if stock>0` と `stock-=1` の間へ別処理が入る。安全性不変条件 `stock≥0` が崩れる。
```text
bad(): if not exists(k): create(k)  # atomic unique insertが境界
```
### よくある誤解
GIL、single event loop、atomic counterだけで業務race全体が消えるわけではない。
### 実務接続
DB unique constraint、compare-and-swap、idempotency tableがcheck/actを同一境界へ寄せる。
### 要点
- timing依存をraceとみる。- dataとlogical raceを分ける。- 複合操作を分解する。- 不変条件で影響を示す。- 原子境界を一か所に置く。- stressだけに頼らない。
### 誤解チェック
1. data raceなしなら全raceがないか。2. 読取同士は競合か。3. GILでDB raceも消えるか。4. sleepで順序を固定できるか。5. unique制約は境界になれるか。
### 基礎問題
1. check-act例を分解せよ。2. lost updateを描け。3. 不変条件を書け。4. access conflictを分類せよ。5. atomic SQLへ直せ。
### 応用問題
1. ABA問題を説明せよ。2. snapshotでのwrite skewを分析せよ。3. race detectorの限界を述べよ。
### 設計問題
coupon一回利用をprocess/DB/crashを跨いで設計せよ。
### 調査課題
利用言語のdata race定義とrace detectorを調べよ。
### 知らないとする誤判断
再現testが1000回通ったことをrace不存在の証明にする。
### 次章接続
共有不変条件を守るために排他的なcritical sectionを定義する。

## 第4章 Critical Section

### この章を学ぶ理由
lockを先に選ばず、不可分に守る状態と操作範囲を決める。
### 現場の問題
個別fieldにlockして複数field不変条件を壊す、network I/Oをlock内に置く。
### 中心概念と正式定義
critical sectionは共有不変条件を一時的に破って回復するため、相互排他を要するコード領域。要件はmutual exclusion、progress、bounded waiting等。linearization pointは操作が瞬時に生じたと見なせる一点。
### 直感→図解→数式→例→実装または疑似コード
`lock → read a,b → update both → invariant restored → unlock`。不変条件 `a+b=C` をfield別lockでは守れない。
### よくある誤解
critical sectionを短くすれば常に正しい、変数ごとにlockすれば十分、readは無害、ではない。
### 実務接続
account transfer、cache metadata、allocator free list、DB row groupに現れる。
### 要点
- 保護対象は不変条件。- 境界は状態集合に合わせる。- linearization pointを置く。- I/Oを安易に含めない。- 例外時も解放する。- 粒度は競合と複雑性のtrade-off。
### 誤解チェック
1. 一行がcritical sectionか。2. field単位で十分か。3. read-onlyは常に安全か。4. 短さが正しさを決めるか。5. linearization pointは実時計時刻か。
### 基礎問題
1. transfer境界を示せ。2. 不変条件を書け。3. 例外経路を追え。4. 粗粒度/細粒度を比較せよ。5. I/Oを外へ出せ。
### 応用問題
1. lock stripingを評価せよ。2. read-copy-updateを調べよ。3. composability問題を説明せよ。
### 設計問題
LRU cacheのmapとlistを一貫して更新する境界を設計せよ。
### 調査課題
OSS一件のcritical sectionと保護不変条件をコードから復元せよ。
### 知らないとする誤判断
lockの存在を安全性の証拠とし、何を守るか確認しない。
### 次章接続
critical sectionを実装するmutexの所有権と可視性を扱う。

## 第5章 Mutex

### この章を学ぶ理由
mutexを単なる同時実行数1の道具でなく、所有権と同期順序の契約として使う。
### 現場の問題
二重unlock、再入可能性への依存、lock順逆転、callback中のlock保持が起きる。
### 中心概念と正式定義
mutexは同時に一ownerだけが保持する同期primitive。成功unlockは後続lockとのhappens-beforeを形成する（具体保証は言語仕様に従う）。公平性・再入性・priority inheritanceは別特性。contention下待ち時間はcritical section長とqueueingに依存する。
### 直感→図解→数式→例→実装または疑似コード
`acquire(M); try { mutate } finally { release(M) }`。複数mutexは全箇所で同じ全順序に取得する。
### よくある誤解
mutexは速さを保証せず、公平とも限らず、process crashを跨ぐtransactionでもない。
### 実務接続
runtime lock、DB advisory lock、file lockは名前が同じでも故障モデルと所有権が違う。
### 要点
- 一ownerの相互排他。- 可視性契約も確認。- finally/RAIIで解放。- lock順を固定。- callbackを境界外へ。- 公平性を仮定しない。
### 誤解チェック
1. mutexはprocess crash後もtransactionalか。2. unlockは誰でも可能か。3. 公平性は標準保証か。4. 再入mutexは設計問題を消すか。5. 取得順はdeadlockに関係するか。
### 基礎問題
1. RAII例を書け。2. lock順を作れ。3. contentionを測れ。4. owner違反を示せ。5. callback経路を分析せよ。
### 応用問題
1. convoyを説明せよ。2. priority inversion対策を比較せよ。3. sharded lockを設計せよ。
### 設計問題
多口座transferでlock集合と取得順、timeout、rollbackを設計せよ。
### 調査課題
OS/runtime mutexの公平性とmemory orderingを一次資料で調べよ。
### 知らないとする誤判断
mutexを一つ足せば、範囲と順序を考えず安全になると思う。
### 次章接続
所有者ではなく許可数を管理するsemaphoreへ進む。

## 第6章 Semaphore

### この章を学ぶ理由
有限resourceと待機数を明示し、過負荷を無限queueへ隠さない。
### 現場の問題
connection pool以上の処理を開始する、release漏れ、binary semaphoreをmutex同様に扱う。
### 中心概念と正式定義
counting semaphoreは非負許可数を持ち、P/acquireは正なら減らし、0なら待ち、V/releaseは増やし待者を起こす。binary semaphoreは値0/1だがowner概念がない点でmutexと異なる。容量Kは同時利用上限。
### 直感→図解→数式→例→実装または疑似コード
K枚の入場券を取得し必ず返す。Little則 `L=λW` により到着率λ、滞在Wから必要同時数Lを概算する。
### よくある誤解
semaphoreはrate limiterそのものではない。許可数を増やせばthroughputが必ず増えるわけでもない。
### 実務接続
DB connection、download concurrency、bounded producer-consumer、file descriptorを制限する。
### 要点
- 許可数を管理。- ownerはない。- 容量は下流から決める。- 必ずrelease。- queue上限も別に設計。- rateとconcurrencyを分ける。
### 誤解チェック
1. binary semaphore=mutexか。2. concurrency limit=QPS limitか。3. K増加で常に速いか。4. cancellation時releaseは必要か。5. queueは自動でboundedか。
### 基礎問題
1. P/Vを追跡せよ。2. Kを算定せよ。3. leakを見つけよ。4. mutexとの差を述べよ。5. overload方針を選べ。
### 応用問題
1. weighted semaphoreを設計せよ。2. adaptive concurrencyを評価せよ。3. fairnessを検討せよ。
### 設計問題
外部API呼出しの同時数、queue、deadline、拒否を設計せよ。
### 調査課題
利用runtimeのsemaphore cancellation契約を調べよ。
### 知らないとする誤判断
許可数を増やして飽和を解決し、下流障害を増幅する。
### 次章接続
共有状態を不可分に更新するatomic operationへ進む。

## 第7章 Atomic operation

### この章を学ぶ理由
原子性の範囲とmemory orderingを確認し、複合不変条件へ過大適用しない。
### 現場の問題
atomic counterで残高と履歴を同時に守ったと思う、CAS retryが高競合でCPUを焼く。
### 中心概念と正式定義
atomic operationは他threadから途中状態を観測できない操作。compare-and-swapは `if *p==expected then *p=new` を不可分に行い成功可否を返す。linearizabilityは各操作がinvocationとresponse間の一点で実行されたような全順序を持ち、実時間順序を保つ性質。memory orderは原子性とは別。
### 直感→図解→数式→例→実装または疑似コード
```text
do:
  old = atomic_load(p)
  new = f(old)
while !CAS(p, old, new)
```
競合確率が上がるとretry仕事が増える。
### よくある誤解
atomic型の各操作が原子的でも、複数操作のsequenceは原子的でない。CASはABAを自動検出しない。
### 実務接続
counter、reference count、lock-free stack、DB conditional update、ETagに対応概念がある。
### 要点
- 原子性は操作境界。- CASは条件付き更新。- linearization pointを示す。- memory orderは別軸。- retry費用を測る。- 複数状態は別設計。
### 誤解チェック
1. 二atomic更新は一transactionか。2. relaxedでも原子的か。3. CASは必ず一回成功か。4. linearizableは速さか。5. ABAを検出するか。
### 基礎問題
1. CAS loopを追え。2. linearization pointを示せ。3. atomic sequenceのraceを作れ。4. ABA例を描け。5. retry数を測れ。
### 応用問題
1. tagged pointerを説明せよ。2. fetch-add scalabilityを評価せよ。3. DB CASをSQLで表せ。
### 設計問題
quota counterをatomic、lock、DB transactionで比較せよ。
### 調査課題
C++/Rust等のatomic ordering仕様を一次資料で調べよ。
### 知らないとする誤判断
変数をatomic型へ替えれば業務transaction全体も原子的だと思う。
### 次章接続
atomic operationの観測順を規定するmemory modelを扱う。

## 第8章 Memory Model

### この章を学ぶ理由
compiler、CPU、runtimeが許す再順序化の範囲内で、portableな同期を書く。
### 現場の問題
debug buildでは動くpublish、`volatile`を同期だと思う、data race時の挙動を経験則で決める。
### 中心概念と正式定義
memory modelはexecutionのどのreadがどのwriteを観測できるかを定める。sequenced-before、synchronizes-with、happens-beforeを区別する。release writeを対応するacquire readが観測すると、それ以前のwriteが後側へ可視になる。sequential consistency（SC）は全threadの操作が各threadのprogram orderと整合する一つの全順序で実行されたように見えるモデルである。C/C++等では `seq_cst` 操作の単一全順序と、relaxed/acquire/releaseを含む残りの規則を区別する。
### 直感→図解→数式→例→実装または疑似コード
producerがdataを書き、releaseでready=true、consumerがacquireでreadyを読んだ後dataを読む。flagだけ原子的でもorderingが弱ければpublish保証を欠く。
### よくある誤解
CPUが順番に実行して見える、`volatile`が相互排他を与える、x86で動けばportable、ではない。
### 実務接続
language atomics、kernel barrier、device I/O、lock implementationの契約に現れる。
### 要点
- 観測可能executionの規則。- compiler/CPU最適化を含む。- HBで可視性を述べる。- acquire/releaseでpublish。- SCは強いが費用あり。- data race規則は言語別。
### 誤解チェック
1. volatile=mutexか。2. atomicity=orderingか。3. release/acquireは関係を作るか。4. SCは実時計順か。5. 未定義動作をhardwareで説明できるか。
### 基礎問題
1. publish graphを描け。2. HBを列挙せよ。3. reorder可能性を示せ。4. barrier位置を選べ。5. data raceを判定せよ。
### 応用問題
1. store buffering litmusを分析せよ。2. consume orderingの問題を調べよ。3. false sharingと区別せよ。
### 設計問題
read-mostly設定snapshotの安全なpublishを設計せよ。
### 調査課題
使用言語memory modelのnormative sectionを読み、lock保証をまとめよ。
### 知らないとする誤判断
ソース順をそのまま全threadの観測順だと扱う。
### 次章接続
複数同期が互いの進行を妨げるliveness障害へ進む。

## 総合演習A（第1〜8章）

高負荷時だけ設定snapshotとcounterが不整合になるserviceを題材に、event graph、data/logical race、不変条件、critical section、mutex/semaphore/CAS候補、memory orderingを比較する。再現待ちをせず、各仮説の反証testとobservabilityを設計せよ。

## 第9章 Deadlock・Livelock・Starvation

### この章を学ぶ理由
safetyだけでなく「いつか進む」というlivenessを設計・監視する。
### 現場の問題
相互待ちで停止、retry同士が譲り続ける、低優先jobが永久に実行されない。
### 中心概念と正式定義
deadlockのCoffman条件は相互排他、hold-and-wait、no preemption、circular waitの同時成立。livelockは状態は変わるが有用な進捗なし。starvationは特定処理が無期限にresourceを得ない。wait-for graphのcycleは単一instance resourceでdeadlockを示す。
### 直感→図解→数式→例→実装または疑似コード
`T1 holds A→waits B; T2 holds B→waits A`。全lockへ全順序rankを付け昇順取得すればcycleを除く。
### よくある誤解
timeoutはdeadlockの根治ではなく、中途効果とretry stormを生む。CPU使用があるから進捗しているとも限らない。
### 実務接続
thread dump、DB lock graph、distributed lease、scheduler公平性で検出する。
### 要点
- safetyとlivenessを分ける。- 四条件で原因を切る。- lock順でcycleを防ぐ。- livelockは進捗metricで見る。- fairnessなしにstarvation可能。- timeout後の整合性を決める。
### 誤解チェック
1. CPU0%=deadlockか。2. timeoutで根治か。3. cycleは常に必要か。4. fairnessはmutex標準か。5. retry成功率だけでlivelock検出か。
### 基礎問題
1. wait graphを描け。2. 四条件を指摘せよ。3. lock rankを付けよ。4. livelock例を作れ。5. starvation metricを定義せよ。
### 応用問題
1. Banker's algorithmを調べよ。2. wound-waitを説明せよ。3. priority inversionとの関係を述べよ。
### 設計問題
複数DB row更新の順序、deadlock retry、idempotencyを設計せよ。
### 調査課題
実DBのdeadlock検出とvictim選択を一次資料で調べよ。
### 知らないとする誤判断
timeoutを追加して相互待ちの構造を残し、再発をretryで増幅する。
### 次章接続
blockingなしのprogress保証を段階的に理解する。

## 第10章 Lock-free programming入門

### この章を学ぶ理由
lock-freeを「lockより速い」とせず、progress保証、memory reclamation、検証費用を理解する。
### 現場の問題
CAS loopでABA/use-after-free、競合retry、保守不能な独自queueを作る。
### 中心概念と正式定義
wait-freeは各operationが有限stepで完了、lock-freeはsystem全体として有限step内に誰かが完了、obstruction-freeは単独実行なら完了。強さは wait-free⇒lock-free⇒obstruction-free。個々threadのstarvationはlock-freeでも可能。linearizabilityと安全なreclamationが要る。
### 直感→図解→数式→例→実装または疑似コード
CAS失敗は他者が進んだ証拠なので全体進捗はある。stack popでnodeを読む間に他者が解放すると危険。hazard pointer/epoch等で寿命を守る。
### よくある誤解
lock-freeはlock不使用と同義でも、常に高速・公平でもない。GC言語でも論理ABAは残る。
### 実務接続
runtime queue、allocator、metrics counterでは実績あるprimitiveを優先する。
### 要点
- progress保証を区別。- linearizationを証明。- reclamationが核心。- ABAを扱う。- contention retryを測る。- 標準実装を優先。
### 誤解チェック
1. lock-freeなら各thread完了か。2. wait-freeが最強か。3. CAS失敗は全体停止か。4. GCでABA皆無か。5. 常にmutexより速いか。
### 基礎問題
1. 三保証を分類せよ。2. CAS stackを追え。3. ABAを描け。4. linearization点を示せ。5. retry metricを決めよ。
### 応用問題
1. hazard pointerを説明せよ。2. epoch reclamationを比較せよ。3. Michael–Scott queueの不変条件を調べよ。
### 設計問題
metrics集計をmutex、sharded counter、atomicで比較し選定条件を示せ。
### 調査課題
利用runtimeのlock-free containerが主張するprogress保証を一次資料で確認せよ。
### 知らないとする誤判断
lockという語を消すことを目的化し、寿命と検証可能性を悪化させる。
### 次章接続
待ち時間中にthreadを占有しないasync programmingへ進む。

## 第11章 Async programming

### この章を学ぶ理由
非同期I/Oの継続、構造化concurrency、cancellationを正しさの一部として扱う。
### 現場の問題
fire-and-forget例外消失、deadline伝播漏れ、blocking callでevent loop停止、無制限task生成。
### 中心概念と正式定義
async taskは停止可能な継続としてevent loop等にscheduleされる。awaitは通常threadをblockせずtaskをsuspendする。structured concurrencyはchild taskの寿命をlexical scopeへ束ね、完了・失敗・cancelを親へ伝播する。backpressureはproducer rateをconsumer capacityへ結ぶ。
### 直感→図解→数式→例→実装または疑似コード
`scope { start A; start B; await both }`。Little則でconcurrency `L=λW`。deadlineは各下流へremaining budgetを渡す。
### よくある誤解
asyncは自動parallel、awaitすればraceなし、cancelは任意行で安全にrollback、ではない。
### 実務接続
HTTP server、stream pipeline、GUI loopでbounded queue、timeout、cleanupを設計する。
### 要点
- awaitは継続を分割。- CPU仕事は別executor。- task寿命をscopeへ束ねる。- cancel点で不変条件を守る。- deadlineを伝播。- backpressureを設ける。
### 誤解チェック
1. async=parallelか。2. event loopでblockingしてよいか。3. cancelで外部効果が戻るか。4. task数は無制限でよいか。5. deadline=各hop同じtimeoutか。
### 基礎問題
1. state machineへ展開せよ。2. blocking箇所を探せ。3. cancel点を列挙せよ。4. Lを計算せよ。5. bounded pipelineを書け。
### 応用問題
1. structured concurrencyをcallbackと比較せよ。2. head-of-line blockingを分析せよ。3. deadline budgetを配分せよ。
### 設計問題
1000URL fetcherを容量、rate、cancel、retry、順序まで設計せよ。
### 調査課題
利用runtimeのtask group/cancellation仕様を一次資料で調べよ。
### 知らないとする誤判断
taskを大量生成して待ちを隠し、容量上限と失敗伝播を失う。
### 次章接続
共有memoryも共通clockもない分散systemへ境界を広げる。

## 第12章 Distributed Systemとは何か

### この章を学ぶ理由
remote callを遅いlocal callと見なさず、独立故障・不確かな通信・局所知識を前提にする。
### 現場の問題
一つのrequest IDで全体を原子的と思う、相手の無応答を停止と断定する。
### 中心概念と正式定義
分散systemはnetworkで結ばれ、共有memoryを持たずmessageで協調する複数processの集合。asynchronous modelはmessage/processing遅延に既知上限を置かない。synchronous modelは上限を仮定し、partial synchronyは一定条件以後などに上限が成立する。safetyは悪いことが起きない、livenessは良いことがいつか起きる性質。
### 直感→図解→数式→例→実装または疑似コード
`A -- request? --> B` でtimeout後、request未着・処理中・response紛失を区別できない。local stateだけでは真相を一意に決められない。
### よくある誤解
microservice化=分散耐障害化、timeout=相手停止、LAN=信頼可能、ではない。
### 実務接続
DB replica、Kubernetes control plane、service mesh、browser-serverに同じ故障モデルがある。
### 要点
- 独立processとmessage。- 局所知識しかない。- modelの時間仮定を明示。- safety/livenessを分離。- remote ambiguityを保持。- 状態機械で設計。
### 誤解チェック
1. remote callは例外付き関数か。2. timeoutは失敗証明か。3. safety違反は待てば直るか。4. asyncはasync/awaitか。5. node数増加で自動高可用か。
### 基礎問題
1. 故障modelを書け。2. safety/livenessを分類せよ。3. timeout三場合を列挙せよ。4. 局所観測を示せ。5. state machineを描け。
### 応用問題
1. FLPの主張を調べよ。2. failure detectorを説明せよ。3. partial synchronyの役割を述べよ。
### 設計問題
remote job実行APIの受理、実行、照会、cancel契約を設計せよ。
### 調査課題
実RPC frameworkのdeadline/retry契約を一次資料で調べよ。
### 知らないとする誤判断
timeoutを相手側の未実行と同義にする。
### 次章接続
networkが作る欠落、遅延、重複、再順序化を具体化する。

## 第13章 Network failure

### この章を学ぶ理由
packet損失からDNS、load balancer、connection半開までをmessage deliveryの保証として扱う。
### 現場の問題
自動retryで二重処理、長いtimeoutでresource枯渇、短いtimeoutで擬似障害を増幅する。
### 中心概念と正式定義
networkはmessageをdrop、delay、duplicate、reorder、corruptし得る（corruptionは下層checksumで低減）。request/responseでは少なくとも二方向のdeliveryが必要。独立packet成功確率pと仮定したk packet全成功は `p^k` だが現実の障害は相関する。
### 直感→図解→数式→例→実装または疑似コード
`send→[request lost | executed,response lost | success]`。retry policyはdeadline内のattempt budget、backoff、jitter、idempotencyを一体設計する。
### よくある誤解
TCPならapplication messageが一回だけ届く、connection closeで相手処理結果が分かる、retryは可用性だけを上げる、ではない。
### 実務接続
HTTP、gRPC、DNS、NAT、LB、TLS handshakeで別々のtimeoutと再試行が重なる。
### 要点
- deliveryは不確実。- TCP streamと業務operationを分ける。- retryは重複を作る。- deadlineで総時間を制限。- jitterで同期を崩す。- 相関障害を試す。
### 誤解チェック
1. TCP=exactly onceか。2. timeout後は未実行か。3. retry回数だけ決めればよいか。4. packet lossは独立か。5. connection成功=service成功か。
### 基礎問題
1. response lossを描け。2. attempt budgetを計算せよ。3. exponential backoffを書け。4. timeout層を列挙せよ。5. duplicate効果を示せ。
### 応用問題
1. hedged requestを評価せよ。2. retry stormをモデル化せよ。3. circuit breakerの限界を述べよ。
### 設計問題
決済RPCのdeadline、retry、idempotency、照会を設計せよ。
### 調査課題
RFC 9293等でTCPが保証するもの・しないものを確認せよ。
### 知らないとする誤判断
transportの信頼性を業務operationの一回性へ拡張する。
### 次章接続
一部だけ壊れ、他は動くpartial failureを扱う。

## 第14章 Partial failure

### この章を学ぶ理由
全体停止より難しい「一部成功・一部不明」を状態として設計する。
### 現場の問題
三下流の二つだけ更新しrollbackも失敗、health checkだけ成功するzombie node。
### 中心概念と正式定義
partial failureはcomponentsの一部が失敗し残りが動作する状態。failure domainは共通原因で同時に失敗し得る集合。availabilityを独立と仮定して直列依存なら積、冗長系なら組合せで計算できるが、共有電源・region等の相関を含める。
### 直感→図解→数式→例→実装または疑似コード
`orchestrator→A✓, B?, C✗`。単一success/failでなく各sub-operationと補償状態を永続化するsaga state machineが必要。
### よくある誤解
冗長化で可用性は必ず上がる、health endpoint成功なら正しい、compensationはrollbackと同じ、ではない。
### 実務接続
multi-AZ、fan-out API、saga、control/data plane分離、bulkheadへつながる。
### 要点
- 一部成功を通常状態にする。- failure domainを図示。- 相関を含める。- 不明状態を保持。- 補償も失敗する。- degraded modeを契約。
### 誤解チェック
1. partial failureは全停止か。2. replicaは独立か。3. compensation=完全取消か。4. health=correctnessか。5. 不明を失敗へ丸めてよいか。
### 基礎問題
1. failure domainを描け。2. 状態表を作れ。3. 直列availabilityを計算せよ。4. degraded responseを定義せよ。5. 補償失敗を追加せよ。
### 応用問題
1. correlated failureをモデル化せよ。2. bulkheadを説明せよ。3. Byzantine failureと区別せよ。
### 設計問題
旅行予約sagaを全停止点・再開・手動介入込みで設計せよ。
### 調査課題
公開cloud障害報告からfailure domainの誤仮定を抽出せよ。
### 知らないとする誤判断
全処理を成功/失敗の二値に丸め、既に生じた外部効果を失う。
### 次章接続
順序と期限を決めるclock自体が一致しない問題へ進む。

## 第15章 Timeという難題

### この章を学ぶ理由
物理clockの時刻と因果順序を分け、lease・TTL・監査を正しい仮定で設計する。
### 現場の問題
NTP補正で時刻が戻る、clock skewでlease ownerが二重になる、timestampだけで因果を断定する。
### 中心概念と正式定義
physical clock `C_i(t)` のoffset、driftを区別し、真時刻tに対し `|C_i(t)-t|≤ε` のような誤差boundがある場合だけ期限を安全に論じられる。monotonic clockは経過時間、wall clockは暦時刻向け。logical clockは因果関係を表し暦時刻を表さない。
### 直感→図解→数式→例→実装または疑似コード
二clock差が最大2εならlease safety marginを含める。`wall: 01:59→01:00` でもmonotonic elapsedは増える。
### よくある誤解
NTPで完全同期、UTCなら単調、timestamp大=因果的後、ではない。
### 実務接続
certificate期限、token exp、DB commit timestamp、log correlation、schedulerに異なるclockを選ぶ。
### 要点
- wall/monotonicを分ける。- offset/driftを測る。- clock boundを明示。- timestampは因果証明でない。- leap/adjustmentを扱う。- logical clockを使い分ける。
### 誤解チェック
1. UTCは単調か。2. NTPでε=0か。3. elapsedにwall clockか。4. timestamp順=因果順か。5. leaseにskew margin要るか。
### 基礎問題
1. 最大clock差を求めよ。2. DST例を分析せよ。3. clock用途を分類せよ。4. lease余裕を算定せよ。5. log順の反例を作れ。
### 応用問題
1. TrueTimeの考え方を調べよ。2. hybrid logical clockを説明せよ。3. leap second影響を分析せよ。
### 設計問題
複数regionのlicense leaseをclock仮定・fencing込みで設計せよ。
### 調査課題
OSのmonotonic/wall clock API契約を一次資料で調べよ。
### 知らないとする誤判断
時刻同期serviceの存在だけで全nodeの全順序を仮定する。
### 次章接続
因果に整合するscalar logical clockを構成する。

## 第16章 Lamport Clock

### この章を学ぶ理由
物理時刻なしでhappens-beforeに整合する順序labelを得る。
### 現場の問題
分散logを単一timestampで並べ、因果逆転を作る。
### 中心概念と正式定義
各processはcounter Lを持つ。local/send eventで `L:=L+1`、messageへ付与。受信時 `L:=max(L,L_msg)+1`。clock conditionは `a→b ⇒ L(a)<L(b)`。逆 `L(a)<L(b)⇒a→b` は成り立たない。process IDとのlexicographic pairで全順序を作れるが因果と同値ではない。
### 直感→図解→数式→例→実装または疑似コード
`P1:1 --msg(1)→ P2:max(0,1)+1=2`。独立eventにも1,2が付く可能性があり、数値差は時間差でない。
### よくある誤解
Lamport値が大きいeventは必ず因果的後、差が経過時間、全順序が真の時系列、ではない。
### 実務接続
event ordering、distributed mutual exclusion、replication metadataの基礎になる。
### 要点
- scalar counter。- sendで付与。- receiveでmax+1。- HBなら値増加。- 逆は不可。- tie-break全順序は人工的。
### 誤解チェック
1. 逆命題は真か。2. 値差=秒か。3. 同値は同時か。4. receiveは+1か。5. 全順序は作れるか。
### 基礎問題
1. diagramへ値を振れ。2. clock conditionを確認せよ。3. converse反例を作れ。4. tie-breakを書け。5. message遅延を追え。
### 応用問題
1. Lamport mutual exclusionを調べよ。2. total-order broadcastとの関係を述べよ。3. overflowを設計せよ。
### 設計問題
監査eventの因果整合表示をLamport値と実時刻で設計せよ。
### 調査課題
Lamport 1978論文のhappened-before定義を読む。
### 知らないとする誤判断
logical clockを精密なwall clockとして利用する。
### 次章接続
因果と並行を区別できるvector clockへ拡張する。

## 第17章 Vector Clock

### この章を学ぶ理由
二eventの因果順序とconcurrencyをmetadataから判定する。
### 現場の問題
同時更新の一方をlast-write-winsで黙って失う。
### 中心概念と正式定義
N processのvector Vを持ち、local eventで自身成分をincrement、sendで添付、receiveでcomponent-wise max後自身をincrement。`V(a)<V(b)` は全成分≤かつ一つ以上<。理想条件で `a→b ⇔ V(a)<V(b)`。比較不能ならconcurrent。
### 直感→図解→数式→例→実装または疑似コード
`[2,0]` と `[0,3]` は比較不能、mergeは `[2,3]`。metadataはparticipant数に比例する。
### よくある誤解
concurrentは実時間同時、vector長が常に固定可能、conflict検出が自動解決、ではない。
### 実務接続
version vector、multi-master store、offline syncでsiblingを検出する。
### 要点
- component-wise更新。- 因果を双方向判定。- 比較不能=因果未確定。- mergeはmax。- metadata成長。- 解決policyは別。
### 誤解チェック
1. `[1,2]<[2,2]`か。2. 比較不能=同時刻か。3. conflictを解決するか。4. node churnは無料か。5. Lamportよりmetadata小か。
### 基礎問題
1. vectorを割当てよ。2. 三組を比較せよ。3. mergeせよ。4. conflictを示せ。5. node追加を考えよ。
### 応用問題
1. dotted version vectorを調べよ。2. vector compressionを評価せよ。3. causal consistencyへ接続せよ。
### 設計問題
offline編集可能なdocument metadataとmerge UXを設計せよ。
### 調査課題
実在DBのversion vector利用・不採用理由を一次資料で調べよ。
### 知らないとする誤判断
conflictを検出しただけで業務上の統合が済んだと思う。
### 次章接続
同じstateを複数nodeへ持つreplicationへ進む。

## 第18章 Replication

### この章を学ぶ理由
複製をbackupと同一視せず、読み書き経路、lag、quorum、failoverの不変条件を設計する。
### 現場の問題
非同期replicaへ切替えて確定済みwriteを失う、read-your-writesが壊れる。
### 中心概念と正式定義
replicationは同一論理stateのcopyを複数failure domainに保持する。leader-based、multi-leader、leaderlessがある。N replica、write quorum W、read quorum Rで `W+R>N` は読取集合とwrite集合の交差を保証するが、version比較・sloppy quorum・障害範囲次第で最新読取を自動保証しない。
### 直感→図解→数式→例→実装または疑似コード
`client→leader→followers`。commit条件がlocal、one follower、majorityでdurability/latencyが変わる。lagは時間だけでなくoffset差で測る。
### よくある誤解
replica数=可用性、quorum式だけでstrong consistency、非同期replica=backup、ではない。
### 実務接続
DB read replica、object store、Kafka partition replica、control planeに現れる。
### 要点
- failure domainを分離。- commit条件を明示。- lagを観測。- failover時lossを定義。- quorum交差は必要条件の一部。- backup/replicaを分ける。
### 誤解チェック
1. replica=backupか。2. W+R>Nだけでlinearizableか。3. lag0は永続か。4. failoverは無損失か。5. multi-leaderならconflictはないか。
### 基礎問題
1. N,R,Wを選べ。2. failover時系列を描け。3. lag metricを定義せよ。4. leader lossを分析せよ。5. failure domainを配置せよ。
### 応用問題
1. read repairを説明せよ。2. chain replicationを調べよ。3. quorum latencyをモデル化せよ。
### 設計問題
商品catalogの読取地域性、更新、staleness、切替を設計せよ。
### 調査課題
利用DBのreplication commit/lag/failover契約を一次資料で調べよ。
### 知らないとする誤判断
copyが三つあれば、どのack後もdataを失わないと考える。
### 次章接続
replica利用者へ見せる観測保証をconsistency modelとして定義する。

## 第19章 Consistency model

### この章を学ぶ理由
「強い/弱い」を曖昧に言わず、許されるhistoryの集合としてAPI保証を選ぶ。
### 現場の問題
eventualを乱読と説明する、serializableとlinearizableを混同、session保証を無視する。
### 中心概念と正式定義
consistency modelはconcurrent historyのうち許容される集合。linearizabilityは各operationを呼出し-応答間へ置き実時間順を保つ単一objectの性質。sequential consistencyは各process orderを保つ全順序だが実時間制約なし。serializabilityはtransaction結果が何らかの直列順と等価。causal consistencyは因果関係を全observerが同順に見る。session guaranteeにはread-your-writes、monotonic reads等がある。
### 直感→図解→数式→例→実装または疑似コード
history `w(1) completes; later r→0` は同object linearizabilityに反する。serializable DBでもreal-time順が逆ならstrict serializableでない。
### よくある誤解
ACID Cとdistributed consistencyは同義でない。強い保証は全操作に一律必須でもない。
### 実務接続
balance、timeline、DNS、feature flagで操作ごとに必要保証が異なる。
### 要点
- modelは許容history集合。- linearizableは実時間制約。- sequentialはprocess順。- serializableはtransaction分離。- causalは因果順。- session保証はUXに効く。
### 誤解チェック
1. serializable=linearizableか。2. sequentialは実時間を守るか。3. eventual=任意値か。4. ACID Cと同じか。5. 操作別に選べるか。
### 基礎問題
1. historyを判定せよ。2. RYW違反を作れ。3. 三modelを比較せよ。4. transaction順を直列化せよ。5. API保証を書け。
### 応用問題
1. strict serializabilityを説明せよ。2. PRAM consistencyを調べよ。3. invariant confluenceを概説せよ。
### 設計問題
SNS投稿、like数、block関係に別々のconsistencyを割り当てよ。
### 調査課題
実在DBのconsistency claimをformal definitionへ翻訳せよ。
### 知らないとする誤判断
製品の「strong consistency」というmarketing語だけでhistory保証を決める。
### 次章接続
network partition時に実現できるavailabilityとの制約をCAPで正確に読む。

## 総合演習B（第12〜19章）

三regionのprofile serviceで更新消失と古い読取が発生した。network ambiguity、partial failure、clock、Lamport/vector、replication commit、consistency historyを用い、原因仮説を優先順位化する。Countermeasureは「作業（assumed cause）」形式で、各反証logとfailure injectionを付けよ。

## 第20章 CAP theorem

### この章を学ぶ理由
CAPを「三つから二つ」の製品分類でなく、partitionを含むexecutionでの応答と単一copy保証の両立限界として理解する。
### 現場の問題
平常時latency trade-offをCAPで説明、CA databaseと固定分類、Pを任意選択と誤解する。
### 中心概念と正式定義
Gilbert–Lynch形式では、network partition中も各non-failing nodeが受理したrequestへ最終的に応答するavailabilityと、atomic/linearizable registerのconsistencyを同時には保証できない。このavailabilityは特定deadlineや年間稼働率を定めず、無応答を許さない定義である。partition toleranceは「選ぶfeature」より、分断をfailure modelに含めるかという前提。PACELCはpartition時だけでなくelse時のlatency-consistency trade-offを示す補助的視点。
### 直感→図解→数式→例→実装または疑似コード
分断されたA,B双方が同じkeyへwriteを受理すると単一順序が壊れ得る。一方を拒否すればavailability定義を満たさない。第三案は保証を弱める。
### よくある誤解
常に三つ中二つ、availability=SLA稼働率、consistency=ACID C、partition時だけでなく全設計を一文字分類、は誤り。
### 実務接続
quorum read/write、region failover、control plane minority partitionの応答policyを決める。
### 要点
- theoremの定義を読む。- partition executionが対象。- Cはlinearizable相当。- Aは全request有限応答。- Pは故障前提。- 平常時trade-offは別に分析。
### 誤解チェック
1. 三つから二つか。2. A=99.99%か。3. Pを選ばなくてよいか。4. RDBはCA固定か。5. partition外latencyもCAPか。
### 基礎問題
1. 二node反例を描け。2. Cを保つ応答を示せ。3. Aを保つ応答を示せ。4. 用語を定義せよ。5. SLAと区別せよ。
### 応用問題
1. Gilbert–Lynch proof sketchを読め。2. PACELCを適用せよ。3. quorumのpartition挙動を分析せよ。
### 設計問題
地域分断時の残高参照/更新policyを操作別に設計せよ。
### 調査課題
Brewer 2000とGilbert–Lynch論文を読み、通俗説明との差をまとめよ。
### 知らないとする誤判断
CAP文字を製品へ貼り、実際の分断時operation contractを確認しない。
### 次章接続
複数nodeが一つの決定へ合意するconsensusを扱う。

## 第21章 Consensus

### この章を学ぶ理由
leader選出、複製log、membership変更の根にある合意問題と成立仮定を知る。
### 現場の問題
多数決ならconsensusと考える、二つのleaderが一時存在しただけで即safety違反とする、liveness仮定を無視する。
### 中心概念と正式定義
consensusは各processが値を提案し、agreement（正しいprocessは異なる値を決定しない）、validity（決定値は許された提案由来）、termination（所定仮定下で正しいprocessが決定）を満たす。crash faultとByzantine faultを分ける。majority quorumの任意二集合が交差することが過去の決定を運ぶが、投票規則・epochも必要。
### 直感→図解→数式→例→実装または疑似コード
crash fault下でN=2f+1なら、残るf+1台が互いに通信できるときmajorityによる進捗をf台の停止まで維持でき、任意の二majorityは少なくとも一nodeで交差する。交差だけで安全になるのではなく、term/ballotと投票規則で交差nodeが過去の決定を伝える。split voteは未決定であってagreement違反ではない。
### よくある誤解
consensusは値が同じになるeventual convergenceそのものでも、leader electionだけでもない。FLPは「実用不能」を意味しない。
### 実務接続
metadata、lock service、replicated state machine、configurationへ使う。大量data本体ではなく決定logを合意することが多い。
### 要点
- agreement/validity/termination。- fault modelを明示。- quorum交差を使う。- epochで古いactorを区別。- safety/liveness仮定を分ける。- consensus対象を小さくする。
### 誤解チェック
1. majority countだけで十分か。2. split voteはagreement違反か。3. FLP=解けないか。4. Byzantineとcrashは同じか。5. 全dataを合意する必要か。
### 基礎問題
1. 三性質を分類せよ。2. Nとfを計算せよ。3. quorum交差を示せ。4. epochなし反例を作れ。5. 未決定と不一致を分けよ。
### 応用問題
1. failure detectorとの関係を調べよ。2. Byzantine quorumを比較せよ。3. reconfigurationの難しさを述べよ。
### 設計問題
leader lease serviceの合意対象、fencing、client semanticsを設計せよ。
### 調査課題
PaxosまたはViewstamped Replication一次論文を読み性質を対応付けよ。
### 知らないとする誤判断
投票を一回集めただけで、古いleaderのwriteを排除できると思う。
### 次章接続
合意を理解しやすい役割へ分解したRaftを学ぶ。

## 第22章 Raftを概念から理解する

### この章を学ぶ理由
leader election、log replication、safetyを分離し、replicated state machineの不変条件を具体化する。
### 現場の問題
heartbeatが届くleaderを常に正しいとする、replicateされたentryとcommitted entryを混同、5node中2node故障後に勝手な再構成をする。
### 中心概念と正式定義
Raft serverはfollower/candidate/leader、単調増加termを持つ。Election Safetyはtermごとに高々一leader。Log Matchingは同じindex/term entryを持てばそれ以前も一致。Leader Completenessはcommitted entryが後続leader logに存在。current-term entryがmajorityへ複製されたときcommitを進める規則が過去term entryも安全に含める。state machineは同じcommitted log順で適用する。
### 直感→図解→数式→例→実装または疑似コード
`client→leader append→followers; majority ack→commit→apply`。electionではcandidate logのlast term/indexが十分新しい場合だけ投票。randomized timeoutでsplit voteを解く。
### よくある誤解
Raftは二phase commit、heartbeat ackでentry commit、minorityを強制昇格しても安全、ではない。membership変更はoverlapping majorityが要る。
### 実務接続
etcd等のmetadata storeで使われ、client重複排除やsnapshot/compactionはcore合意に加えて必要。
### 要点
- termはlogical epoch。- 一term一投票。- log freshnessで投票。- majority複製とcommitを区別。- 適用順を統一。- membershipも合意する。
### 誤解チェック
1. replica1台でcommitか。2. old-term majorityだけで直ちにcommitか。3. 二candidateはsafety違反か。4. snapshotはconsensus不要か。5. minority昇格は安全か。
### 基礎問題
1. electionを追跡せよ。2. log比較を行え。3. commitIndexを求めよ。4. partitionを描け。5. apply順を示せ。
### 応用問題
1. Raft safety proofを要約せよ。2. joint consensusを説明せよ。3. linearizable read方式を調べよ。
### 設計問題
三node Raft clusterの配置、故障、backup、client retry、監視を設計せよ。
### 調査課題
[Raft原論文](https://raft.github.io/raft.pdf)のFigure 2を読み、各規則が守る不変条件を対応付けよ。
### 知らないとする誤判断
障害時に「データが多いnode」を人手leaderにして安全性を壊す。
### 次章接続
複数resource managerを跨ぐtransactionと合意の違いへ進む。

## 第23章 Distributed transaction

### この章を学ぶ理由
複数境界のall-or-nothing、隔離、durabilityを、停止点と調停者故障から理解する。
### 現場の問題
二DBを順次commit、2PCを高可用consensusと混同、saga補償を完全rollbackと思う。
### 中心概念と正式定義
two-phase commitはcoordinatorがprepareを集め、全yesならcommit、それ以外abortを記録・通知するatomic commitment protocol。participantはprepare後決定までin-doubtでresourceを保持し得る。2PCは単独coordinator故障でblockingし得て、consensusのterminationを自動提供しない。sagaは局所transaction列とsemantic compensation列でありisolationは別途設計する。
### 直感→図解→数式→例→実装または疑似コード
`prepare all → durable decision → commit all`。任意message前後にcrashを置き、recovery logから同じ決定を再送する。
### よくある誤解
2PCなら高可用、compensationなら元状態、outboxだけでconsumer effectもatomic、ではない。
### 実務接続
XA、database coordinator、outbox/inbox、saga orchestrationで保証範囲が違う。
### 要点
- atomic commitmentを定義。- prepare後はin-doubt。- decisionをdurable化。- 2PCはblocking可能。- sagaは意味的補償。- isolationを別設計。
### 誤解チェック
1. 2PC=consensusか。2. prepare後自由にabortか。3. compensation=物理rollbackか。4. coordinator log不要か。5. sagaはisolationを保証か。
### 基礎問題
1. 2PC stateを描け。2. crash点を列挙せよ。3. in-doubtを説明せよ。4. saga補償を書け。5. outbox境界を示せ。
### 応用問題
1. three-phase commitの仮定を調べよ。2. presumed abortを説明せよ。3. TCCとsagaを比較せよ。
### 設計問題
注文・決済・在庫を2PC/saga/単一DBで比較し、失敗UXも設計せよ。
### 調査課題
実DBのprepared transaction recovery手順を一次資料で調べよ。
### 知らないとする誤判断
複数systemへの順次成功を一つのtransactionと呼ぶ。
### 次章接続
時間的結合を緩めるmessage queueとdelivery状態を扱う。

## 第24章 Message queue

### この章を学ぶ理由
queueを「投げれば届く箱」でなく、順序、再配信、容量、ack、保持のprotocolとして設計する。
### 現場の問題
ack前後のcrashで重複/損失、単一global順序を仮定、consumer lagを無限に許す。
### 中心概念と正式定義
message systemはproducer、broker/log、consumer、delivery/ack protocolからなる。at-most-onceは重複を抑え損失可能、at-least-onceは損失を抑え重複可能。順序は通常partition等のscope内。consumer lagは `produced offset-consumed offset`、保持上限を越えればreplay不能。
### 直感→図解→数式→例→実装または疑似コード
`produce→persist→deliver→process→ack`。process後ack前crashで再配信。先ack後processでcrashなら損失。
### よくある誤解
queueがあるだけで負荷制御、順序が全messageで一意、DLQへ送れば解決、ではない。
### 実務接続
job queue、event log、CDC、notification。key partitioningは順序と並列性のtrade-off。
### 要点
- ack境界を描く。- delivery保証を明示。- 順序scopeを定義。- lag/retentionを監視。- bounded capacityを決める。- poison messageを扱う。
### 誤解チェック
1. at-least-onceは損失ゼロか。2. global orderか。3. ack=effect commitか。4. queue=backpressureか。5. DLQ=処理完了か。
### 基礎問題
1. crash点を追え。2. deliveryを分類せよ。3. lagを計算せよ。4. partition keyを選べ。5. retentionを算定せよ。
### 応用問題
1. rebalancing中の重複を分析せよ。2. logとqueueを比較せよ。3. poison retry budgetを設計せよ。
### 設計問題
メール送信pipelineの順序、重複、DLQ、監査、消費能力を設計せよ。
### 調査課題
使用brokerのack/offset/rebalance/retention保証を一次資料で調べよ。
### 知らないとする誤判断
brokerへのpublish成功を利用者への効果成功と同義にする。
### 次章接続
再試行可能にするoperationのidempotencyを定式化する。

## 第25章 Idempotency

### この章を学ぶ理由
不明結果を安全に再試行できるAPIと状態境界を作る。
### 現場の問題
HTTP PUTなら業務上も自動idempotent、keyだけ保存してresponse/expiry/concurrencyを未定義にする。
### 中心概念と正式定義
operation fがidempotentとは `f(f(x))=f(x)`。effect idempotencyでは同じlogical requestの反復が観測可能効果を一回分にする。idempotency keyはprincipal、operation、payload hash等へscopeし、同key異payloadをrejectする。記録と効果を同一atomic boundaryへ置く必要がある。
### 直感→図解→数式→例→実装または疑似コード
```text
transaction:
  row = get(key)
  if row: return stored_response
  result = apply(payload)
  insert(key, hash(payload), result)
```
### よくある誤解
自然にidempotentなset操作でも通知等の副作用は重複し得る。TTL後の再試行契約も必要。
### 実務接続
payment、webhook、job consumer、provisioning APIに用いる。
### 要点
- 数学的定義をeffectへ翻訳。- logical requestを識別。- payload mismatchを拒否。- 記録と効果を原子的に。- responseを再現。- TTL/容量を契約。
### 誤解チェック
1. POSTは必ず非idempotentか。2. keyだけで十分か。3. 同key異payloadを受理か。4. TTL後も保証か。5. DB外通知も一回か。
### 基礎問題
1. 操作を分類せよ。2. key scopeを書け。3. schemaを設計せよ。4. concurrent duplicateを追え。5. TTLを決めよ。
### 応用問題
1. commutativityと比較せよ。2. dedup storageを容量計算せよ。3. multi-region key raceを分析せよ。
### 設計問題
課金APIのidempotency契約と照会APIを設計せよ。
### 調査課題
実決済APIのidempotency仕様を一次資料で調べ保証範囲を表にせよ。
### 知らないとする誤判断
同じkeyをheaderへ付けただけで全副作用が一回になると思う。
### 次章接続
「exactly-once」という省略語をend-to-end効果へ分解する。

## 第26章 Exactly-onceという表現の注意点

### この章を学ぶ理由
delivery、processing、state update、external effectのscopeを分け、誇張された保証を避ける。
### 現場の問題
brokerのexactly-once modeを、メール・決済まで一回と説明する。
### 中心概念と正式定義
exactly-once effectは少なくとも一回と高々一回の両方。lossy/asynchronous communicationだけで受信者の外部効果をsend側が知ることはできず、通常はat-least-once delivery＋dedup/transactionにより定義したstate boundary内で一回相当を作る。scope、failure model、retention、client retryを明記する。
### 直感→図解→数式→例→実装または疑似コード
`broker transaction {consume offsets; write output records}` はbroker内read-process-writeを束ね得るが、外部HTTP effectは同じatomic boundary外。
### よくある誤解
exactly-onceは無意味という極論も誤り。厳密なscope内では有用だがend-to-endへ自動拡張できない。
### 実務接続
stream processing、CDC sink、outbox/inbox、transactional producerで契約を分解する。
### 要点
- at-least＋at-most。- delivery/effectを分離。- boundaryを明示。- dedupは保持期限あり。- 外部effectを別扱い。- recoveryを含め試す。
### 誤解チェック
1. broker設定でメールも一回か。2. dedup期限外も一回か。3. exactly-onceは常に虚偽か。4. offset commit=DB commitか。5. scope明示が必要か。
### 基礎問題
1. pipeline境界を描け。2. crash点を列挙せよ。3. guaranteeを分類せよ。4. dedup容量を求めよ。5. 外部effectを指摘せよ。
### 応用問題
1. transactional outboxを評価せよ。2. end-to-end argumentを調べよ。3. sink fencingを設計せよ。
### 設計問題
Kafka→DB→webhook pipelineの各区間保証と最終UXを設計せよ。
### 調査課題
Apache Kafka公式design/documentationのexactly-once scopeを確認せよ。
### 知らないとする誤判断
中間systemの保証名を、利用者が観測する最終効果へ無条件に広げる。
### 次章接続
即時一致を要求しないeventual consistencyの収束条件を扱う。

## 第27章 Eventual Consistency

### この章を学ぶ理由
「いつか合う」を願望でなく、更新停止、伝播、公平な再試行、conflict解決の条件として定義する。
### 現場の問題
永続的conflictやpoison eventを放置しeventualと呼ぶ、収束中UXを設計しない。
### 中心概念と正式定義
eventual consistencyは新規updateが止まり、communication/reconciliationが継続すれば全replicaが最終的に同じ値へ収束する保証。strong eventual consistencyは同じupdate集合を受けたreplicaが同じstateになる。CRDTはjoin-semilatticeの単調merge（state-basedならcommutative、associative、idempotentなjoin等）で収束を構成する。
### 直感→図解→数式→例→実装または疑似コード
G-counterはnode別非減少counter vectorをcomponent-wise maxでmergeし、valueは総和。削除や制約は単純でなくtombstone等が要る。
### よくある誤解
eventualは期限なしでよい、last-write-winsは因果を保存、CRDTで任意業務制約を自動解決、ではない。
### 実務接続
DNS、cache、shopping cart、multi-region metadata、Kubernetes controllerのreconciliationに現れる。
### 要点
- 収束条件を明示。- stalenessを測る。- anti-entropyを設計。- merge代数則を守る。- conflict UXを決める。- invariant制約は別検討。
### 誤解チェック
1. 更新継続中も同値必須か。2. 収束期限は自動か。3. LWWは因果保存か。4. merge順に依存してよいか。5. CRDTで残高非負を容易に守れるか。
### 基礎問題
1. G-counterをmergeせよ。2. 三法則を確認せよ。3. lag metricを作れ。4. tombstone問題を説明せよ。5. conflict UXを書け。
### 応用問題
1. OR-setを調べよ。2. invariant confluenceを適用せよ。3. delta-CRDTを説明せよ。
### 設計問題
offline shopping cartのmerge、削除、在庫制約、利用者表示を設計せよ。
### 調査課題
CRDT原論文または実装の収束条件を検証せよ。
### 知らないとする誤判断
収束を保証する機構なしに、時間が解決すると期待する。
### 次章接続
原理をKubernetes、DB、Kafkaの具体構成へ写像する。

## 第28章 Kubernetes・DB・Kafka等への接続

### この章を学ぶ理由
製品用語を暗記せず、control loop、consensus、replication、log、idempotencyへ分解する。
### 現場の問題
Kubernetes restartをapplication correctnessと同一視、DB replicaをbackup扱い、Kafka partition順序をglobal順序と誤認する。
### 中心概念と正式定義
Kubernetes controllerはdesired stateとobserved stateの差を反復的・idempotentに縮めるcontrol loop。etcdはRaft系合意でmetadataを複製する。DBはWAL/replication/transaction/consistencyを別層に持つ。Kafkaはpartitioned replicated logで、offsetとconsumer groupにより処理位置を管理する。各保証はfailure domainとoperation scopeに相対的。
### 直感→図解→数式→例→実装または疑似コード
`spec → controller observe → act → status → repeat`。controllerは一回成功を仮定せず、現在stateから再実行可能にする。
### よくある誤解
orchestratorが業務transactionを保証、replica=backup、broker retention=永久監査、ではない。
### 実務接続
readiness、lease、operator、DB failover、consumer rebalanceを本書の状態機械でレビューする。
### 要点
- 製品をprimitiveへ分解。- desired/current差を収束。- metadata合意を識別。- log順序scopeを確認。- backupを独立化。- application invariantは自分で守る。
### 誤解チェック
1. restart=rollbackか。2. etcdが全app stateを合意か。3. Kafkaはglobal orderか。4. read replica=backupか。5. controllerは一回実行か。
### 基礎問題
1. reconcile pseudocodeを書け。2. component mapを作れ。3. failure domainを描け。4. offsetを追跡せよ。5. readiness限界を述べよ。
### 応用問題
1. operator split-brainを分析せよ。2. DB fencingを設計せよ。3. rebalance重複を説明せよ。
### 設計問題
Kubernetes上のstateful consumerをDB/Kafka含め復旧設計せよ。
### 調査課題
[Kubernetes Controllers公式文書](https://kubernetes.io/docs/concepts/architecture/controller/)と利用製品の一次資料を対応付けよ。
### 知らないとする誤判断
platformが再起動するからapplicationも障害安全だと思う。
### 次章接続
複数原理が連鎖した障害事例を仮説優先で分析する。

## 総合演習C（第20〜28章）

multi-region order pipelineをCAP、consensus/Raft、saga、queue、idempotency、exactly-once scope、eventual convergence、Kubernetes reconciliationでレビューせよ。partition、leader交代、consumer rebalance、DB commit後response lossを同時注入し、安全性・liveness・UXを評価する。

## 第29章 障害事例分析――retry stormとsplit brain

### この章を学ぶ理由
時系列の後付け物語でなく、不変条件と競合仮説から根本原因を隔離する。
### 現場の問題
短いpacket loss→timeout→全client即retry→queue飽和→heartbeat遅延→leader交代→重複処理、というfeedback loopが起きた。
### 中心概念と正式定義
offered load `λ'=λ(1+r+r²+…) = λ/(1-r)`（各attempt再試行確率rの単純model）で、rが1へ近づくと増幅する。safety不変条件は「同orderの確定請求高々一回」、livenessは「期限内に成功または確定失敗」。fencing tokenなしの旧leaderが外部storageへwriteしsplit-brain effectを作った。
### 直感→図解→数式→例→実装または疑似コード
因果loopを `loss↑→latency↑→timeout↑→retry↑→load↑` と描く。Countermeasure: retry budget+jitter+admission control（assumed cause: client同期再試行）。Countermeasure: fencing付きwrite（assumed cause: 旧leaderが外部effect可能）。
### よくある誤解
packet lossだけをroot causeにする、timeout延長だけで直す、node追加だけで直す、はいずれもfeedback構造を残す。
### 実務接続
circuit breaker、load shedding、retry budget、fencing、idempotency、SLO burn alertを一体化する。
### 要点
- feedback loopを描く。- 原因仮説を優先。- retry増幅を計算。- fencingでepochを強制。- safety/livenessを測る。- compound failureを試す。
### 誤解チェック
1. 最初のevent=root causeか。2. timeout延長でloop消滅か。3. electionで旧leader停止保証か。4. idempotencyだけでload低下か。5. 相関故障testは必要か。
### 基礎問題
1. λ'を求めよ。2. 因果graphを書け。3. 不変条件を示せ。4. fencing tokenを追え。5. metricを選べ。
### 応用問題
1. queueing collapseを分析せよ。2. retry budgetを算定せよ。3. chaos実験を設計せよ。
### 設計問題
本事例の構造的改修、移行、回帰試験、rollback条件を作れ。
### 調査課題
公開分散障害報告一件を同じ仮説形式で再分析せよ。
### 知らないとする誤判断
最初に観測されたnetwork errorを唯一原因として修正を終える。
### 次章接続
障害時から始める総合設計を実践する。

## 第30章 分散システム設計演習

### この章を学ぶ理由
機能一覧より先に、failure model、不変条件、recovery、観測を確定する習慣を得る。
### 現場の問題
正常sequenceだけの設計書で、timeout後のAPI回答、再処理、手動復旧が空白になる。
### 中心概念と正式定義
設計を `(state machine, safety invariant, liveness target, failure model, consistency history, capacity, recovery, observability)` の八項組として表す。RTOは復旧時間目標、RPOは許容data loss point。保証はoperation scopeとassumptionに相対的。
### 直感→図解→数式→例→実装または疑似コード
`不変条件→全停止点→曖昧結果→再実行→収束→監査` の順に書く。正常系はその一pathにすぎない。
### よくある誤解
multi-region=DR完了、chaos test=無計画停止、監視=CPU dashboard、ではない。
### 実務接続
ADR、runbook、SLO、capacity test、game day、data reconciliationへ成果物をつなぐ。
### 要点
- 障害modelから開始。- 不変条件を少数定義。- 曖昧状態を保持。- recoveryを通常path化。- RPO/RTOを測る。- 人手操作もprotocol化。
### 誤解チェック
1. backupだけでRTO達成か。2. timeout=abortか。3. monitoring=safety証明か。4. chaosは仮説必要か。5. runbook操作もfencing要るか。
### 基礎問題
1. 八項を埋めよ。2. crash matrixを作れ。3. RPO/RTOを定義せよ。4. reconciliationを書け。5. alertを選べ。
### 応用問題
1. global unique ID serviceを設計せよ。2. feature flag control planeを設計せよ。3. object storage metadataを設計せよ。
### 設計問題
決済ledgerを、二重請求禁止、地域分断、監査、再処理、災害復旧、容量まで完全にレビューせよ。
### 調査課題
Jepsen等のhistory-based testingを調べ、対象systemのcheckerを設計せよ。
### 知らないとする誤判断
構成図に冗長nodeを描けば耐障害設計が完了したと思う。
### 次章接続
最後に頻出誤判断を原因仮説とcountermeasureへ圧縮する。

## 第31章 この分野を知らないエンジニアが陥りやすい誤判断

### この章を学ぶ理由
高頻度・高影響の誤判断を、採否を判断できる原因仮説付きcountermeasureへ変える。
### 現場の問題
対策の容易さで順序を決めると、retryやtimeoutの小修正で根本不変条件を放置する。
### 中心概念と正式定義
優先度は概ね `発生確率×影響×反証までの時間`。以下は典型順で、各項目を「Countermeasure: 作業（assumed cause）」として示す。
### 直感→図解→数式→例→実装または疑似コード
`symptom→ranked hypothesis→disconfirming evidence→structural repair→fault regression`。最低限、history checkerとfault injectionを自動化する。

1. Countermeasure: 不変条件と原子境界を定義する（assumed cause: raceを再現性問題としている）。
2. Countermeasure: deadline・retry budget・jitterを一体化する（assumed cause: timeout時に全clientが同期再試行する）。
3. Countermeasure: operationをidempotentにしresponseを保存する（assumed cause: response loss後の再試行が効果を重複する）。
4. Countermeasure: bounded queueとload sheddingを設ける（assumed cause: backlogが容量不足を隠している）。
5. Countermeasure: ack/commit/crash点をstate machine化する（assumed cause: message受信と業務効果を同一視する）。
6. Countermeasure: consistencyを許容historyで記述する（assumed cause: strong/eventualという形容詞だけで合意している）。
7. Countermeasure: commit条件とfailover lossを検証する（assumed cause: replica数をdurability保証と見なす）。
8. Countermeasure: fencing tokenを外部resourceで検証する（assumed cause: election後に旧leaderが必ず停止すると考える）。
9. Countermeasure: lock順とwait-for graphを整備する（assumed cause: timeoutでdeadlockを治そうとしている）。
10. Countermeasure: cancellationを構造化しchild寿命を束ねる（assumed cause: fire-and-forget taskが孤児化している）。
11. Countermeasure: critical sectionを不変条件単位に再設計する（assumed cause: fieldごとのlockで複合stateを守っている）。
12. Countermeasure: memory model上のHBを作る（assumed cause: source order/volatileを可視性保証と見なす）。
13. Countermeasure: semaphore容量を下流能力から算定する（assumed cause: concurrencyを増やせばthroughputが上がると思う）。
14. Countermeasure: progress保証とreclamationを検証する（assumed cause: lock-freeを単なる高速化として導入した）。
15. Countermeasure: wall/monotonic/logical clockを分離する（assumed cause: timestampを期限と因果の両方に使う）。
16. Countermeasure: vector等でconflictを検出し業務mergeを設計する（assumed cause: last-write-winsで更新消失を許す）。
17. Countermeasure: CAPをpartition時operation contractへ落とす（assumed cause: 製品へAP/CP labelを貼って終える）。
18. Countermeasure: 2PCのin-doubt recoveryを設計する（assumed cause: coordinator failureでも自動progressすると考える）。
19. Countermeasure: exactly-onceのboundaryを図示する（assumed cause: broker内部保証を外部effectへ広げる）。
20. Countermeasure: 収束条件とstaleness SLOを定義する（assumed cause: eventualを時間任せにしている）。
21. Countermeasure: failure domainの相関を配置・試験へ反映する（assumed cause: replica failureを独立と仮定する）。
22. Countermeasure: quorum交差にversion/epoch規則を加える（assumed cause: `R+W>N` だけで最新読取を保証したと思う）。
23. Countermeasure: membership変更をconsensus対象にする（assumed cause: 故障時にnode集合を手作業で書き換える）。
24. Countermeasure: compensation失敗を含むsaga状態を永続化する（assumed cause: 補償を完全rollbackと考える）。
25. Countermeasure: poison messageの有限retryと隔離・再投入を設計する（assumed cause: 無限retryをreliabilityと思う）。
26. Countermeasure: controllerをidempotent reconciliationにする（assumed cause: Kubernetes再起動を業務復旧と同義にする）。
27. Countermeasure: backup restoreとreplica failoverを別々に試す（assumed cause: replicaを履歴backupと考える）。
28. Countermeasure: safety/liveness metricを分ける（assumed cause: 高availability数値だけで正しさを判断する）。
29. Countermeasure: correlated faultをgame dayで注入する（assumed cause: 単一node故障testだけで分散耐性を評価する）。
30. **rare** Countermeasure: Byzantine modelと暗号認証を導入する（assumed cause: crashでなく悪意・任意故障がscopeにある）。

### よくある誤解
一覧の上から盲目的に実装するのではなく、現状証拠で仮説priorityを更新する。
### 実務接続
architecture review、incident command、runbook、chaos planへ「仮説・反証・countermeasure・回帰」を記入する。
### 要点
- 不変条件が最優先。- 曖昧結果を消さない。- retryに予算を置く。- 保証scopeを明示。- failure domainを試す。- 構造的対策を回帰する。
### 誤解チェック
1. 上位項目は全案件同順か。2. timeoutだけで原因修正か。3. replicaとbackupは同じか。4. exactly-onceはscope不要か。5. rare仮説を最初に深掘りすべきか。
### 基礎問題
1. 自systemの上位5仮説を選べ。2. 反証metricを書け。3. fault matrixを作れ。4. 不変条件を一つ書け。5. retry budgetを求めよ。
### 応用問題
1. 複合障害の因果loopを描け。2. history checkerを設計せよ。3. countermeasureの撤回条件を決めよ。
### 設計問題
既存systemを一覧でauditし、最優先三原因の構造改修と段階移行を提案せよ。
### 調査課題
公開障害報告を一件選び、著者の原因順位と自分の順位を証拠で比較せよ。
### 知らないとする誤判断
分散障害を個別製品のbugとだけ捉え、再利用可能なfailure modelを残さない。
### 次章接続
DB理論、OS、確率統計を併読し、storage isolation、scheduler、tail確率を精密化する。

## 参考文献

- Lamport, [Time, Clocks, and the Ordering of Events in a Distributed System](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
- Fischer, Lynch, Paterson, *Impossibility of Distributed Consensus with One Faulty Process*.
- Gilbert, Lynch, *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*.
- Ongaro, Ousterhout, [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf).
- Kleppmann, *Designing Data-Intensive Applications*.
- Kubernetes, [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)（参照日2026-08-27）。
- Apache Kafka, [Design / Message Delivery Semantics](https://kafka.apache.org/documentation/#semantics)（参照日2026-08-27）。
- Java Community Process, [Java Language Specification SE 26, Chapter 17: Threads and Locks](https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html)（memory modelの現行一次仕様、参照日2026-08-27）。

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **同時実行の正しさは実行順ではなく、不変条件と happens-before で捉える。** 直感的には、ログで一度見えた順番は可能な interleaving の一例にすぎない。正式には共有状態の不変条件、原子的な遷移、可視性を与える同期辺、許される history を定義する。実務では、再現率の低い race を sleep で調整せず、所有権か同期関係を構造として作る。
2. **分散 system では部分故障と知識の不完全性が通常状態である。** timeout は相手の失敗ではなく、応答を期限内に観測できなかったという局所的事実にすぎない。正式には crash、omission、partition、遅延などの failure model と、各 process が観測できる情報を区別する。実務では、成功したか不明な operation を結果型と recovery protocol に残し、安易に失敗へ丸めない。
3. **複製は状態ではなく、順序付けられた決定を共有する問題である。** 同じ replica 数でも、どの operation をどの epoch・順序で commit したかが一致しなければ一つの system にはならない。正式には log、quorum intersection、leader term、state-machine replication で safety を説明する。製品選定では replica 数という外形でなく、ack 条件、failover 時の loss、membership 変更を確認する。
4. **待ち行列は負荷を消さず、時間へ移す。** 到着率が処理能力を持続的に超えれば、無限 queue、retry、worker 追加のいずれでも安定性は回復しない。正式には utilization、Little の法則、queue bound、deadline budget を使って latency と backlog の関係を見る。実務では backpressure、admission control、load shedding を API contract の一部にする。
5. **保証は failure model、system boundary、進捗条件を伴う条件文である。** 「exactly once」「available」「lock-free」は、何が故障し得るか、どの効果まで含むか、公平性や最終的応答を仮定するかで意味が変わる。正式には safety と liveness、処理保証と外部 effect、crash と Byzantine を分ける。設計判断では強い用語を採用する前に、その仮定と反例を failure injection へ落とす。

### 専門家の意見が根本的に分かれる3つの論点

1. **一貫性のために coordination を払うか、可用性と局所 autonomy のために競合を受け入れるか。** **立場A（強い整合性）の steelman:** 業務不変条件を一箇所で直列化すれば、全利用者へ単純な意味論を提供でき、後処理で修復不能な二重支出や権限違反を防げる。**立場B（coordination 回避）の steelman:** partition や地理的遅延下で全操作を同期すると system 自体が仕事を止めるため、単調な操作、CRDT、補償可能な業務へ再設計して局所 progress を守る方がよい。不変条件の種類、競合頻度、遅延予算、offline 要件、補償可能性によって選択が変わる。
2. **共有状態を lock と thread で協調させるか、所有権を分け message passing で連携させるか。** **立場A（共有メモリ）の steelman:** 同一 process 内の密結合な data structure では直接参照と適切な同期が最小 overhead であり、actor 化は protocol、copy、mailbox failure を増やす。**立場B（所有権・message）の steelman:** mutable state の所有者を一つにすれば race の組合せを構造的に減らせ、隔離、backpressure、failure supervision を明示できる。共有粒度、latency、data size、failure containment、言語の型・memory model により適解が変わる。
3. **分散正しさへの主要投資を形式仕様・証明へ置くか、実 history と故障注入による検証へ置くか。** **立場A（形式手法）の steelman:** 稀な interleaving や quorum 境界は本番観測を待てず、抽象 model の全状態探索が protocol 設計段階で safety violation を最短に発見する。**立場B（実行時検証）の steelman:** 抽象 model が除いた client、storage、clock、deployment の挙動こそ事故原因になり、Jepsen 型 checker、chaos、observability が実装と運用を含む保証を与える。system の重大性、model と code の乖離、状態空間、変更頻度、実環境で安全に fault を注入できるかで配分が変わる。

### 深い理解と暗記を見分ける10の質問

1. 二つの account を更新する処理で各 field を別々の lock が守っている。それでも総額不変条件が破れる interleaving を作り、自然な原子境界をどう再設計するか説明せよ。
2. client が timeout 後に決済を retry する。server が成功したが response だけ失われた場合を含め、idempotency key、結果保存、期限、利用者表示の contract を設計せよ。
3. `R + W > N` を満たす quorum store でも最新値を返さない history を、sloppy quorum、複数 version、membership 変更のいずれかを使って構成せよ。追加で必要な規則は何か。
4. 平均 utilization が70%の service で tail latency が急増した。平均値だけでは説明できない理由を、burst、service-time 分布、queue bound、retry feedback から仮説順位付きで述べよ。
5. partition 中も「在庫を負にしない」と「全拠点で注文を受け続ける」を同時に要求された。CAP の標語だけで終えず、どの業務操作なら権利分割や補償で両立範囲を広げられるか。
6. broker が exactly-once processing を掲げているのに、外部メールが二通送られた。保証境界を図示する代わりに文章で列挙し、重複を防ぐか受容する設計を比較せよ。
7. lock-free stack が benchmark で高速だった。progress guarantee、ABA、memory reclamation、公平性、contention の仮定が変わると採否がどう変わるか。
8. wall clock が逆行する環境で lease と event ordering を同じ timestamp に依存させた。起こり得る safety/liveness failure を分け、monotonic clock、logical clock、fencing token の役割を割り当てよ。
9. 三つの replica が別 availability zone にあるのに同時停止した。「独立故障」という仮定を反証する情報を何から集め、placement と game day をどう変えるか。
10. model checker では安全、chaos test でも違反なしだった protocol が本番で更新を失った。証明が誤りと即断せず、仕様、refinement、checker、観測、failure model のどこに反例を探すか順序立てて説明せよ。
