# Human–Computer Interaction――人間を含む系を工学する

HCIは美観の講座ではない。人間の知覚・認知・運動・社会的文脈と、計算機の状態・feedback・制約が閉loopを作る系の工学である。本書では「利用者が注意しなかった」を最終原因にせず、観測可能な行動とsystem条件から仮説を反証する。アクセシビリティは2026-08-27時点のW3C WCAG 2.2を参照する。

**関連巻:** 実験の推定・検定は [確率・統計](08_probability_statistics.md)、変更可能性・incident学習は [ソフトウェア工学](09_software_engineering.md)、認証・同意・警告のsecure usabilityは [情報セキュリティ](11_security.md) を参照する。

## 第1章 なぜ正しく動くだけでは不十分なのか

### この章を学ぶ理由
内部仕様どおりでも、利用者が目標を達成できなければsystem全体は失敗だと捉える。
### 現場の問題
保存済みなのに保存されていないと思って再送、危険なdefaultのまま確定、supportへ回避作業が集中する。
### 中心概念と正式定義
interactive systemの有効性は人間＋interface＋task＋environmentに相対的。ISO 9241-11のusabilityは指定利用者が指定contextでgoalを達成するeffectiveness、efficiency、satisfactionの程度。人間側のactionとsystem stateの間にはexecution gulfとevaluation gulfがある。
### 直感→図解→数式→例→実装または疑似コード
`goal→intent→action→system→feedback→perception→interpretation→goal評価`。checkout成功率を `completed/eligible sessions`、efficiencyを完了時間・操作数、errorを回復可否込みで測る。
### よくある誤解
bugがなければusable、利用者教育で解決、好みは測れない、ではない。
### 実務接続
API、CLI、admin console、alert、runbookもinteractive systemである。
### 要点
- system境界に人間を含める。- goal達成を測る。- contextを明示。- execution/evaluation gapを縮める。- error recoveryを設計。- 内部正しさと利用正しさを分ける。
### 誤解チェック
1. 仕様適合=usabilityか。2. satisfactionだけ測ればよいか。3. contextは結果に影響するか。4. APIもHCIか。5. support件数はinterface signalか。
### 基礎問題
1. 自作UIのgoalを三つ書け。2. gulfを指摘せよ。3. effectiveness metricを定義せよ。4. contextを列挙せよ。5. recovery pathを描け。
### 応用問題
1. efficiencyと安全性のtrade-offを分析せよ。2. proxy metricのずれを示せ。3. socio-technical boundaryを描け。
### 設計問題
請求取消flowを人間＋systemのstate machineとして設計せよ。
### 調査課題
ISO 9241-11の定義と任意製品metricを対応付けよ。
### 知らないとする誤判断
backendが正しいので、誤操作は利用者責任だと結論する。
### 次章接続
人間側の情報処理を、能力と制約の両方から見る。

## 第2章 人間の認知

### この章を学ぶ理由
人を一定速度の入出力装置とせず、知覚・記憶・判断・運動の資源配分からinterfaceを説明する。
### 現場の問題
説明を増やせば理解が増えると思う、熟練者の自動化を初心者へ前提とする。
### 中心概念と正式定義
認知は知覚、attention、memory、learning、decision、motor actionを含む過程。bottom-up signalとtop-down expectationが相互作用する。bounded rationalityでは情報・時間・計算能力が有限なため満足化する。cognitive loadはtask固有負荷とpresentation由来負荷を区別して扱う。
### 直感→図解→数式→例→実装または疑似コード
`stimulus↔prior knowledge→attention→working memory↔long-term memory→action`。同じiconでも文脈と経験で解釈が変わる。
### よくある誤解
脳を単純なcomputerに等置、万人に共通の直観、認知biasを個人の欠陥とする、は不適切。
### 実務接続
onboarding、dashboard、alarm、configurationで情報量と既知schemaを整合させる。
### 要点
- 認知は複数過程。- expectationが知覚へ影響。- 資源は有限。- 熟練でchunk化。- context差を測る。- presentation負荷を減らす。
### 誤解チェック
1. 見えた情報は全処理されるか。2. 認知は利用者間で同じか。3. 熟練手順を初心者へ移せるか。4. loadは情報量だけか。5. biasは教育だけで消えるか。
### 基礎問題
1. 一flowを認知段階へ分解せよ。2. top-down例を示せ。3. chunkを作れ。4. 外在負荷を特定せよ。5. context差を挙げよ。
### 応用問題
1. dual-process説明の限界を調べよ。2. automation biasを分析せよ。3. distributed cognitionを説明せよ。
### 設計問題
運用dashboardをnovice/expert両方へ設計せよ。
### 調査課題
認知負荷測定法を一次研究から三つ比較せよ。
### 知らないとする誤判断
説明文を追加するほど誤操作が単調に減ると考える。
### 次章接続
有限な認知資源の選択機構attentionへ進む。

## 第3章 Attention

### この章を学ぶ理由
重要情報を「置いた」ことと、task中に検出・選択されたことを分ける。
### 現場の問題
全alertを赤にしてsignalを埋没、modal interruptで入力を失わせる、変化blindnessを無視する。
### 中心概念と正式定義
attentionは競合情報から処理対象を選択・維持・切替する有限資源。selective、sustained、divided attentionを区別する。signal detectionではhit、miss、false alarm、correct rejectionがあり、感度 `d'` とcriterionを分ける。alert thresholdはmissとfalse alarmの費用に依存する。
### 直感→図解→数式→例→実装または疑似コード
`many signals → filter → attended item`。alert精度 `TP/(TP+FP)`、recall `TP/(TP+FN)`。色だけでなく位置、形、音、文脈を冗長符号化する。
### よくある誤解
目立たせれば必ず気づく、multitaskで並列処理、false alarmは安全側、ではない。
### 実務接続
SRE alert、medical alarm、notification、code review diffでpriorityとactionabilityを対応させる。
### 要点
- attentionは選択資源。- detectionと理解を分ける。- miss/false alarmを測る。- alarm fatigueを防ぐ。- interruption costを含める。- 色だけに依存しない。
### 誤解チェック
1. 画面上にあれば認識か。2. false alarmは無害か。3. 色だけでpriorityか。4. 切替にcostはあるか。5. recall最大化だけでよいか。
### 基礎問題
1. confusion matrixを作れ。2. precision/recallを求めよ。3. alertを三段階化せよ。4. interruptionを列挙せよ。5. inattentional blindness例を作れ。
### 応用問題
1. d'を調べよ。2. change blindness testを設計せよ。3. adaptive alertのriskを評価せよ。
### 設計問題
on-call alertを費用非対称性、escalation、quieting込みで設計せよ。
### 調査課題
alarm fatigueの一次研究または安全規格を調べよ。
### 知らないとする誤判断
重要項目を赤くしたことを、利用者が適時理解した証拠にする。
### 次章接続
選択された情報を一時保持・操作するworking memoryを扱う。

## 第4章 Working Memory

### この章を学ぶ理由
利用者へ状態を記憶させず、認識・外部化・chunkingでtaskを支える。
### 現場の問題
別画面のIDを記憶して入力、長いformの文脈を失う、magic number「7±2」を万能規則にする。
### 中心概念と正式定義
working memoryは情報を短時間保持し操作する容量限定系で、task・modality・chunk化に依存する。単純な固定個数を設計法則にしない。recognitionは候補から同定、recallは手掛かりなしに再生し、一般にrecallの方が負荷が高い。external cognitionは表示や記録へ中間状態を置く。
### 直感→図解→数式→例→実装または疑似コード
`頭内: account ID + amount + source → overload` を `画面: summary card` へ外部化。stepperは全体progressと戻った後の状態を保持する。
### よくある誤解
menu項目は7個以下、若者は容量が大きい、短いlabelなら負荷なし、ではない。
### 実務接続
copy button、breadcrumb、diff preview、command history、form summaryに現れる。
### 要点
- 容量はtask依存。- recallよりrecognition。- 中間状態を外部化。- chunkは知識依存。- interruption後復帰を支援。- 7±2を規則化しない。
### 誤解チェック
1. 容量は常に7か。2. recognitionはrecallより難しいか。3. 熟練chunkは初心者も同じか。4. 外部化は有効か。5. step分割だけで負荷は減るか。
### 基礎問題
1. recall箇所を探せ。2. summaryへ外部化せよ。3. chunkを設計せよ。4. interruption復帰点を作れ。5. 誤った7項目規則を直せ。
### 応用問題
1. modality effectを調べよ。2. progressive disclosureを評価せよ。3. split-attentionを分析せよ。
### 設計問題
multi-step deployment wizardを中断・再開込みで設計せよ。
### 調査課題
working memory capacityの一次研究とHCIでの誤引用を比較せよ。
### 知らないとする誤判断
項目数を7以下にすれば認知設計が完了したと思う。
### 次章接続
利用者がsystemの因果をどう予測するかmental modelへ進む。

## 第5章 Mental Model

### この章を学ぶ理由
利用者の予測モデルと実装modelのずれを観測し、表示・概念・操作を整合させる。
### 現場の問題
cloud保存とlocal保存を混同、permission inheritanceを誤解、戻る操作で副作用も戻ると思う。
### 中心概念と正式定義
mental modelは対象systemの構造・因果・挙動に関する利用者の内的表象。designer's model、system image、user's modelを区別する。良いmodelは完全でなく、task上の予測と説明を支える。conceptual modelはinterfaceが提示するobjects、actions、relationsの体系。
### 直感→図解→数式→例→実装または疑似コード
`designer model → system image(UI/docs) → user model → prediction → feedback`。treeと思っている利用者へDAG共有を見せるなら、alias/owner/propagationを可視化する。
### よくある誤解
利用者の誤解を無知、real-world metaphorなら常に理解、内部構造を全部見せれば正確、ではない。
### 実務接続
Git branch、container、IAM、sync、database transactionの誤解をtask testで検出する。
### 要点
- modelは予測の道具。- system imageが形成する。- taskごとに十分性を見る。- 語彙と因果を一貫。- feedbackで修正可能に。- metaphorの破綻点を示す。
### 誤解チェック
1. 正しいmodelは実装詳細全部か。2. metaphorは無限に拡張可か。3. docsだけがsystem imageか。4. 発話だけでmodelを測れるか。5. 利用者差はあるか。
### 基礎問題
1. 三modelを描け。2. prediction質問を作れ。3. 語彙不一致を探せ。4. metaphor破綻を示せ。5. feedbackを追加せよ。
### 応用問題
1. teach-back法を設計せよ。2. novice/expert modelを比較せよ。3. conceptual integrityを分析せよ。
### 設計問題
Git rebase UIを結果予測とundo可能性中心に設計せよ。
### 調査課題
自社support ticketからmental model mismatchをcodingせよ。
### 知らないとする誤判断
利用者の誤操作をdocs未読で片付け、誤ったsystem imageを残す。
### 次章接続
行為の可能性そのものをaffordanceとして考える。

## 第6章 Affordance

### この章を学ぶ理由
「見た目がbuttonらしい」をaffordance全部とせず、人・環境・対象の関係として操作可能性を分析する。
### 現場の問題
drag可能だがkeyboardでは不可能、touch targetが物理的に押せない、権限上不可能なactionを見せる。
### 中心概念と正式定義
affordanceはactorの能力とenvironment/objectの性質の関係として存在するaction possibility。perceived affordanceは利用者が知覚した可能性。digital UIでは実際のevent handling、権限、device、assistive technologyとの関係がactual affordanceを決める。
### 直感→図解→数式→例→実装または疑似コード
`person capability × control property × context → possible action`。drag-only reorderはpointerにはaffordしてもkeyboard userにはしない。up/down controlを併設する。
### よくある誤解
affordance=見た目の手掛かり、丸角=button、disabledを灰色にすれば理由理解、ではない。
### 実務接続
button、gesture、CLI command、API permissionで実行可能性と発見可能性を分ける。
### 要点
- affordanceは関係。- actual/perceivedを区別。- modality別に確認。- 権限も可能性を制約。- 代替操作を用意。- signifierと混同しない。
### 誤解チェック
1. 見た目だけか。2. 同一controlは万人に同じか。3. drag-onlyは普遍か。4. permissionは関係するか。5. label=affordanceか。
### 基礎問題
1. controlを関係分析せよ。2. actual/perceivedを分けよ。3. keyboard代替を作れ。4. 権限状態を描け。5. device差を挙げよ。
### 応用問題
1. ecological psychology由来を調べよ。2. voice UIへ適用せよ。3. discoverabilityと比較せよ。
### 設計問題
dashboard widget編集をpointer/keyboard/touchで設計せよ。
### 調査課題
実製品の一controlをassistive technologyで検証せよ。
### 知らないとする誤判断
視覚的にbuttonらしいので全利用者が操作可能だとみなす。
### 次章接続
可能な行為を知覚させるsignifierを扱う。

## 第7章 Signifier

### この章を学ぶ理由
どこで何をどう操作できるかを知覚可能にし、隠れgestureや記憶依存を減らす。
### 現場の問題
icon onlyで意味不明、hoverにだけ情報、linkと本文の見分けがつかない。
### 中心概念と正式定義
signifierは行為可能性、場所、方法を伝える知覚可能なsignal。label、形、配置、cursor、音、haptic、状態変化がある。意味は慣習・context・populationに依存するため、認識率と誤解をtestする。
### 直感→図解→数式→例→実装または疑似コード
actual affordanceが「削除」でも、trash iconだけではarchiveとの区別がつかない場合、`削除` labelと結果previewを加える。
### よくある誤解
iconは言語非依存、tooltipで全部解決、minimalismほどusable、ではない。
### 実務接続
navigation、status、gesture tutorial、CLI help、API namingに現れる。
### 要点
- 行為を示すsignal。- affordanceと区別。- 慣習はpopulation依存。- icon+labelを検討。- hover非依存。- 状態もsignifyする。
### 誤解チェック
1. iconは普遍か。2. tooltipはtouchで同じか。3. labelは冗長か。4. signifierがあればaction可能か。5. placementもsignalか。
### 基礎問題
1. 隠れactionを探せ。2. icon理解testを作れ。3. labelを改善せよ。4. hover情報を移せ。5. status signifierを作れ。
### 応用問題
1. cross-cultural symbolを調べよ。2. redundant codingを設計せよ。3. progressive disclosureとのtrade-offを分析せよ。
### 設計問題
権限管理表の編集・継承・保存signifierを設計せよ。
### 調査課題
iconのみnavigationを5人以上で理解度調査せよ。
### 知らないとする誤判断
designerに意味が自明なiconは利用者にも自明だと考える。
### 次章接続
行為の結果と現在stateを返すfeedbackへ進む。

## 第8章 Feedback

### この章を学ぶ理由
操作受理、進行、結果、回復方法を適切な時間とmodalityで返す。
### 現場の問題
二重submit、成功toastが消える、progress barが止まり、失敗理由が「error」だけ。
### 中心概念と正式定義
feedbackは利用者actionまたはsystem変化に対する知覚可能な応答。状態を `idle→accepted→in progress→succeeded|failed|canceled` と明示する。latency distributionに応じ即時ack、progress、completionを分離する。feedbackは実stateと整合し、actionableであるべき。
### 直感→図解→数式→例→実装または疑似コード
`click→button disabled+request ID→progress→durable result`。optimistic UIはrollback/mergeを設計した場合だけ使う。
### よくある誤解
spinnerがあれば十分、toastは監査記録、速ければfeedback不要、ではない。
### 実務接続
form、deployment、payment、CLI exit status、async API job statusで状態機械を共有する。
### 要点
- 受理と完了を分ける。- stateを正確に表示。- progress不明も表現。- persistent resultを用意。- errorをactionableに。- optimistic rollbackを設計。
### 誤解チェック
1. HTTP 202=完了か。2. spinner=progress量か。3. toastは後で確認可か。4. optimistic updateは無料か。5. feedbackは視覚だけか。
### 基礎問題
1. state machineを描け。2. 202表示を直せ。3. error messageを書け。4. duplicate submitを防げ。5. progress不明を表せ。
### 応用問題
1. perceived latency技法を評価せよ。2. optimistic conflictを設計せよ。3. multimodal feedbackを比較せよ。
### 設計問題
10分かかるdata exportの受付、進捗、cancel、再訪を設計せよ。
### 調査課題
実製品の長時間task feedbackを状態遷移と照合せよ。
### 知らないとする誤判断
request送信直後の成功表示を、durable completionと同義にする。
### 次章接続
controlと結果の自然な対応mappingを扱う。

## 第9章 Mapping

### この章を学ぶ理由
操作子と効果の対応を予測可能にし、trial-and-errorを減らす。
### 現場の問題
四buttonがどのdeviceを制御するか不明、左右反転したslider、bulk actionの対象が不明。
### 中心概念と正式定義
mappingはcontrolとeffect、表示とsystem stateの対応関係。spatial、cultural、conceptual compatibilityを利用する。選択肢数nの選択時間を近似するHick–Hyman則 `T=a+b log2(n+1)` は同等選択肢等の条件下の経験modelで、menu項目を機械的削減する規則ではない。
### 直感→図解→数式→例→実装または疑似コード
四口コンロと2×2 knobを同じ配置にする。bulk actionは選択件数と対象sampleをcontrol直近へ表示する。
### よくある誤解
自然mappingは文化非依存、項目数だけで選択時間が決まる、shortcutを増やせば全員速い、ではない。
### 実務接続
settings、dashboard filter、keyboard shortcut、API field-effect mappingに現れる。
### 要点
- control/effect対応。- 空間整合を使う。- 対象scopeを近接表示。- 文化差をtest。- 選択modelの前提確認。- 一貫性を保つ。
### 誤解チェック
1. mapping=layoutだけか。2. 自然性は普遍か。3. Hick則は全taskか。4. bulk対象表示は必要か。5. shortcutは初心者にも自明か。
### 基礎問題
1. 悪いmappingを直せ。2. n増加を計算せよ。3. control/effect表を作れ。4. scopeを表示せよ。5. 文化差を挙げよ。
### 応用問題
1. stimulus-response compatibilityを調べよ。2. adaptive menuを評価せよ。3. mode-dependent mappingを分析せよ。
### 設計問題
multi-region traffic controlのmappingと安全確認を設計せよ。
### 調査課題
物理controlまたはsoftware UIのmapping error事例を分析せよ。
### 知らないとする誤判断
labelがあるからcontrolとeffectの対応は明白だと考える。
### 次章接続
失敗をslipとmistakeへ分け、予防と回復を設計する。

## 第10章 Error

### この章を学ぶ理由
誤りを利用者属性でなく、意図・action・結果のどこでずれたかに分類する。
### 現場の問題
隣button誤clickと、誤った料金plan選択へ同じ「注意」対策を出す。
### 中心概念と正式定義
slipはgoal/planは適切だがexecutionが意図からずれる。mistakeはgoal形成・rule・knowledgeに基づくplan自体が不適切。mode error、capture error、description error等がある。error managementはprevention、detection、containment、recovery、learningを含む。
### 直感→図解→数式→例→実装または疑似コード
`correct intent→wrong action` がslip、`wrong model→intended wrong action` がmistake。slipにはtarget separation/undo、mistakeにはmodel提示/simulationが効く。
### よくある誤解
確認dialogは万能、trainingはslipを消す、error rateだけでseverityを無視、ではない。
### 実務接続
delete、deployment target、medical dose、CLI destructive flagにrisk-based controlを適用する。
### 要点
- slip/mistakeを分ける。- 対策を機序へ合わせる。- undoを優先。- modeを可視化。- severity×frequencyで優先。- near missを学ぶ。
### 誤解チェック
1. typoはmistakeか。2. 確認は全errorに効くか。3. trainingでtarget小ささは解決か。4. near missは無視か。5. undoはrecoveryか。
### 基礎問題
1. 五例を分類せよ。2. mode errorを作れ。3. 対策を対応付けよ。4. severity matrixを作れ。5. undo stateを描け。
### 応用問題
1. Reasonの分類を調べよ。2. confirmation habituationを分析せよ。3. forcing functionを設計せよ。
### 設計問題
production deployのslip/mistake両対策を設計せよ。
### 調査課題
公開事故からerror typeと防護layerを抽出せよ。
### 知らないとする誤判断
すべてのerrorへ確認dialogを足し、habituationを増やす。
### 次章接続
「human error」をroot causeとする組織的問題を掘り下げる。

## 第11章 Human Errorという考え方の問題

### この章を学ぶ理由
最後に操作した人を原因とせず、なぜその行為が当時合理的に見え、防護が捕捉しなかったかを問う。
### 現場の問題
postmortemが「手順違反・注意不足」で終わり、同じ条件を残す。
### 中心概念と正式定義
human errorは説明の終点でなく結果のlabelである。local rationalityは、その時点の情報・goal・制約では行為が合理的だったと仮定して調べる。sharp endのoperatorと、設計・組織・resource配分というblunt endを含むsocio-technical systemを分析する。Just Cultureは故意・reckless・system-induced behaviorを区別する。
### 直感→図解→数式→例→実装または疑似コード
`latent conditions→workload/interface→local cues→action→defense gaps→outcome`。Countermeasure: production targetを物理/視覚分離する（assumed cause: target識別が記憶と注意に依存）。
### よくある誤解
非難しない=責任なし、手順追加=再発防止、違反者除去=system改善、ではない。
### 実務接続
incident review、security ceremony、on-call、healthcare、aviationの安全工学へ接続する。
### 要点
- errorはlabel。- local rationalityを再構成。- latent conditionを見る。- defense gapを調べる。- accountabilityと学習を両立。- 対策をsystemへ置く。
### 誤解チェック
1. 最終操作者=root causeか。2. 非難しないことは基準を設けないことか。3. 手順追加は常に強化か。4. context復元は必要か。5. near missは学習源か。
### 基礎問題
1. five whysの人責任終点を直せ。2. local cuesを書け。3. defenseを列挙せよ。4. latent conditionを探せ。5. Just Culture分類を試せ。
### 応用問題
1. Swiss cheese modelの限界を調べよ。2. Safety-IIを説明せよ。3. drift into failureを分析せよ。
### 設計問題
誤った本番DB削除事故のblamelessかつaccountableな再発防止を設計せよ。
### 調査課題
公開postmortemの「human error」記述をsystem仮説へ書き換えよ。
### 知らないとする誤判断
操作者再教育を最優先にして、同じ誤りを誘発するinterfaceを残す。
### 次章接続
人間とsystemのaction-feedback loopを意図的に設計する。

## 第12章 Interaction Design

### この章を学ぶ理由
screen単体でなく、goal達成までの状態・action・feedback・回復を一貫して設計する。
### 現場の問題
happy pathだけのwireframe、戻るとdata消失、権限変更後の状態が不明。
### 中心概念と正式定義
interaction designは人とinteractive product/serviceの行為系列を設計する。state `S`、user action `A`、transition `δ:S×A→S`、observable output `λ:S→O` でmodel化できる。visibility、constraint、consistency、feedback、undoを状態遷移へ組み込む。
### 直感→図解→数式→例→実装または疑似コード
`draft→validating→submitted→accepted|needs correction`。各stateで可能action、表示、exit、復帰を表にする。
### よくある誤解
interaction design=animation、画面数削減=常に改善、happy path完成=設計完了、ではない。
### 実務接続
form、wizard、chat、voice、CLI、API workflowへ同じstate tableを使う。
### 要点
- goalから始める。- state/actionを明示。- feedbackをtransitionへ対応。- back/cancel/retryを設計。- constraintでerror予防。- cross-channel一貫性。
### 誤解チェック
1. screen list=flowか。2. 戻る意味は自明か。3. animationが中心か。4. error stateも通常stateか。5. API workflowにも適用か。
### 基礎問題
1. state tableを作れ。2. impossible transitionを制約せよ。3. cancelを追加せよ。4. feedbackを対応付けよ。5. resumeを設計せよ。
### 応用問題
1. direct manipulationを評価せよ。2. conversational repairを設計せよ。3. cross-device continuityを分析せよ。
### 設計問題
本人確認flowを保留、再提出、期限、support handoff込みで設計せよ。
### 調査課題
実製品flowをstate machineへreverse engineerせよ。
### 知らないとする誤判断
画面遷移図にerror/recovery stateを描かず完成とする。
### 次章接続
情報の分類・label・navigationという空間構造へ進む。

## 第13章 Information Architecture

### この章を学ぶ理由
利用者の情報探索taskに合わせ、分類・命名・navigation・searchを構造化する。
### 現場の問題
組織図どおりのmenu、同じ用語の意味揺れ、どこにいるか分からないdeep navigation。
### 中心概念と正式定義
information architectureはinformation environmentのorganization、labeling、navigation、search systemの設計。taxonomyは分類体系、ontologyは概念と関係の明示的model。findabilityは利用者が情報を発見できる程度で、known-item search、exploration、refindingを分ける。
### 直感→図解→数式→例→実装または疑似コード
`content inventory→user vocabulary→grouping→label→navigation/search→find test`。treeだけでなくfaceted classificationで複数軸を許す。
### よくある誤解
階層は一つが正解、社内用語は利用者にも通じる、検索があればnavigation不要、ではない。
### 実務接続
docs、admin portal、catalog、API resource hierarchy、error taxonomyに現れる。
### 要点
- task別探索を理解。- 利用者語彙でlabel。- 多軸分類を検討。- locationを示す。- search/navigationを補完。- content lifecycleを管理。
### 誤解チェック
1. 組織構造=利用者modelか。2. treeだけか。3. searchで分類不要か。4. labelは短いほどよいか。5. IAは公開後不変か。
### 基礎問題
1. content inventoryを作れ。2. card sort案を作れ。3. faceted軸を選べ。4. breadcrumbを設計せよ。5. search queryを分類せよ。
### 応用問題
1. tree testingを設計せよ。2. polyhierarchyのriskを分析せよ。3. ontology versioningを調べよ。
### 設計問題
開発者portalのdocs/API/status/support IAを設計せよ。
### 調査課題
search logとsupport問い合わせから語彙gapを分析せよ。
### 知らないとする誤判断
内部team構成をそのままmenu分類にする。
### 次章接続
設計の利用可能性をusabilityの複数尺度で評価する。

## 第14章 Usability

### この章を学ぶ理由
「使いやすい」をcontext付きのeffectiveness、efficiency、satisfaction、error/recoveryへ分解する。
### 現場の問題
平均完了時間だけ改善し失敗者を除外、SUS一値だけで原因を断定する。
### 中心概念と正式定義
usabilityは指定contextに相対的。task success、time-on-task、error率、assistance、satisfactionを併用する。率pの標本推定には不確実性があり、比較は効果量・区間を重視する。completion timeはskewするためmedianや分位点も見る。
### 直感→図解→数式→例→実装または疑似コード
効率を成功者だけの `time` でなく、`successful goals / total person-time` と併記。失敗をtimeoutとして除かない。
### よくある誤解
usability=好み、SUS=診断、平均値=代表、全taskを一指標で比較、ではない。
### 実務接続
release gate、benchmark、support cost、conversion、安全taskにgoal別metricを置く。
### 要点
- context相対。- 多指標で測る。- 失敗者を除外しない。- 分位点を見る。- 不確実性を示す。- 診断は観察と組合せる。
### 誤解チェック
1. satisfactionだけか。2. 平均で十分か。3. success taskを混ぜてよいか。4. SUSで原因判明か。5. context記録は必要か。
### 基礎問題
1. metric setを作れ。2. completion率を求めよ。3. medianを計算せよ。4. failure codingを作れ。5. contextを定義せよ。
### 応用問題
1. survival analysis適用を調べよ。2. composite metricのriskを分析せよ。3. benchmark妥当性を評価せよ。
### 設計問題
admin user作成taskのusability評価protocolを設計せよ。
### 調査課題
ISO 9241-11とSUS原典を読み、用途を区別せよ。
### 知らないとする誤判断
短い平均時間だけで、失敗率と重大errorを隠す。
### 次章接続
初回から熟練までの変化learnabilityを扱う。

## 第15章 Learnability

### この章を学ぶ理由
初回成功だけでなく、反復による獲得、保持、転移を設計・測定する。
### 現場の問題
onboarding完了率を学習とみなす、shortcutを早く教え過ぎる、再訪時の忘却を無視する。
### 中心概念と正式定義
learnabilityは経験によりtask performanceや理解が改善する程度。学習曲線を単純化して `T_n=T_1 n^{-α}` と表せる場合があるが、task変化・ceiling・個人差を確認する。initial learnability、memorability、transferを分ける。scaffoldingは段階的支援で、熟達に応じfadeする。
### 直感→図解→数式→例→実装または疑似コード
trial 1,2,4,8でtime/error/model predictionを測る。guided modeからdirect modeへ同じ概念語彙で移行する。
### よくある誤解
初回だけ簡単=learnable、tooltip=学習、expert効率とnovice理解は必ず対立、ではない。
### 実務接続
IDE、analytics、enterprise workflow、CLIでprogressive pathとshortcut discoveryを設計する。
### 要点
- 反復変化を測る。- 初回/保持/転移を分ける。- scaffoldをfade。- 概念語彙を一貫。- expert pathを用意。- 再訪をtest。
### 誤解チェック
1. onboarding完了=学習か。2. 一回時間だけで測るか。3. transferは自動か。4. scaffoldは永久か。5. shortcutは全員初回提示か。
### 基礎問題
1. 学習曲線を描け。2. retention testを作れ。3. scaffoldを設計せよ。4. transfer taskを作れ。5. expert pathを加えよ。
### 応用問題
1. power law of practiceの限界を調べよ。2. spaced practiceを評価せよ。3. adaptive onboarding biasを分析せよ。
### 設計問題
database query toolのnovice→expert移行を設計せよ。
### 調査課題
実利用telemetryでcohort学習曲線を作り交絡を検討せよ。
### 知らないとする誤判断
初回tutorialを通過した利用者は概念を理解したとみなす。
### 次章接続
能力・device・環境の多様性を権利と品質として扱うaccessibilityへ進む。

## 第16章 Accessibility

### この章を学ぶ理由
障害のある人を例外にせず、知覚・操作・理解・互換性のbarrierをsystematically除く。
### 現場の問題
自動scanner通過を準拠とする、colorだけで状態、keyboard focusを隠す、custom controlのname/role/value欠落。
### 中心概念と正式定義
accessibilityは障害のある人が同等にinformationとfunctionへ到達・操作できる性質。WCAG 2.2はPerceivable、Operable、Understandable、Robustの四原則とtestable success criteriaを持つ。conformanceはlevel A/AA/AAAに加え、full page、complete process、accessibility-supportedな技術利用、non-interference等の規則に従うが、準拠は全利用者needs充足を意味しない。自動、manual、当事者評価を組合せる。
### 直感→図解→数式→例→実装または疑似コード
native buttonはkeyboard、focus、role、nameを多く提供する。`<div onclick>`を再実装するよりsemantic HTMLを使う。errorは色＋icon＋text＋programmatic associationで示す。
### よくある誤解
accessibility=screen reader、AAAなら万人、overlayで修正、disabled利用者は少数、ではない。
### 実務接続
design system、CI lint、manual keyboard test、screen reader test、procurement、legal riskへ組み込む。
### 要点
- POURでbarrierを見る。- semantic nativeを優先。- keyboard/focusを保証。- 色以外も符号化。- 自動testだけに頼らない。- 当事者を含める。
### 誤解チェック
1. scanner0件=accessibleか。2. WCAG準拠=全needか。3. colorのみで状態か。4. native controlは有利か。5. full page要件はあるか。
### 基礎問題
1. POURへ分類せよ。2. tab orderを検査せよ。3. accessible nameを付けよ。4. contrastを確認せよ。5. error associationを実装せよ。
### 応用問題
1. focus managementを設計せよ。2. cognitive accessibilityを調べよ。3. mobile assistive techを比較せよ。
### 設計問題
data gridをkeyboard、screen reader、zoom、touchで設計せよ。
### 調査課題
[WCAG 2.2](https://www.w3.org/TR/WCAG22/)の新success criteriaと製品gapをauditせよ。
### 知らないとする誤判断
自動testの点数を、障害当事者のtask成功と同義にする。
### 次章接続
特定barrier除去を越え、多様性を初期条件にするUniversal Designへ進む。

## 第17章 Universal Design

### この章を学ぶ理由
後付けaccommodationだけでなく、多様な能力・状況で利用できるflexibleな基盤を初期設計する。
### 現場の問題
「average user」persona一人、字幕を特別機能扱い、柔軟性を理由に危険actionまで自由化する。
### 中心概念と正式定義
Universal Designは可能な最大範囲の人がadaptationなしに使える製品・環境を目指す原則。equitable use、flexibility、simple/intuitive、perceptible information、tolerance for error、low physical effort、size/space等。inclusive designはexcluded interactionを特定し多様な参加で反復するprocess。個別accommodationが不要になるわけではない。
### 直感→図解→数式→例→実装または疑似コード
字幕は聴覚障害、騒音環境、非母語話者に役立つ。複数入力modality＋同等結果を提供する。
### よくある誤解
one-size-fits-all、全員へ同じUI、公平=同一、accessibilityの代替、ではない。
### 実務接続
responsive UI、captions、plain language、adjustable timeout、design system defaultsに埋め込む。
### 要点
- 多様性を初期条件。- 公平と同一を分ける。- 複数手段を用意。- error toleranceを高める。- accommodationも残る。- exclusionを当事者と発見。
### 誤解チェック
1. 全員同一が公平か。2. 個別対応不要か。3. 字幕は一群だけか。4. flexibilityは無制限か。5. processに参加が必要か。
### 基礎問題
1. 七原則へ例を当てよ。2. exclusionを列挙せよ。3. modality代替を作れ。4. timeoutを柔軟化せよ。5. 公平なdefaultを選べ。
### 応用問題
1. curb-cut effectの限界を論じよ。2. personalization privacyを分析せよ。3. safety constraintとのtrade-offを設計せよ。
### 設計問題
公共予約kioskを多言語、車椅子、低視力、時間制約で設計せよ。
### 調査課題
Universal Design原則の一次資料とinclusive design手法を比較せよ。
### 知らないとする誤判断
平均的利用者へ最適化してから例外対応を足せば十分と考える。
### 次章接続
憶測でなく利用者contextを調べるUser Researchへ進む。

## 第18章 User Research

### この章を学ぶ理由
design判断を、声の大きいstakeholderや自分の経験から、対象populationの証拠へ移す。
### 現場の問題
solutionを前提に質問、convenience sampleを全利用者へ一般化、researchを要望収集にする。
### 中心概念と正式定義
user researchは利用者のgoal、behavior、context、constraint、meaningをsystematicに調べる。generative/evaluative、qualitative/quantitative、attitudinal/behavioral、lab/fieldを研究質問に合わせる。sampling frame、inclusion criteria、consent、data minimization、reflexivityを明示する。
### 直感→図解→数式→例→実装または疑似コード
`decision→uncertainty→research question→method/sample→evidence→bounded inference→decision`。nの大きさだけでsampling biasは消えない。
### よくある誤解
5人で全問題発見、interview発言=実行、research=feature投票、persona=事実、ではない。
### 実務接続
discovery、concept test、field study、telemetry、support dataをtriangulateする。
### 要点
- decisionから質問を作る。- 方法を証拠種別へ合わせる。- sample境界を示す。- 発言/行動を区別。- ethics/privacyを守る。- inference限界を書く。
### 誤解チェック
1. 大nでbias消滅か。2. 要望=needか。3. 発言=行動か。4. 5人は法則か。5. consent後何でも収集可か。
### 基礎問題
1. research questionを書け。2. 方法matrixを作れ。3. criteriaを定義せよ。4. consent項目を作れ。5. inference境界を書け。
### 応用問題
1. triangulationを設計せよ。2. survivorship biasを分析せよ。3. research repository governanceを作れ。
### 設計問題
新しいincident toolの4週間research planを意思決定ごとに設計せよ。
### 調査課題
任意HCI論文のsampleと外的妥当性を批判的に読む。
### 知らないとする誤判断
社内の同僚数名を対象利用者の代表とみなす。
### 次章接続
発言から経験と意味を掘るInterviewを扱う。

## 第19章 Interview

### この章を学ぶ理由
誘導せず、抽象意見より具体的な過去行動・context・意味を得る。
### 現場の問題
「この機能ほしいですか」、未来予測、複合質問、同意圧力で肯定回答を集める。
### 中心概念と正式定義
semi-structured interviewはguideを持ちつつ回答に応じprobeする質的方法。研究対象はself-reportであり行動そのものではない。critical incident、timeline reconstruction、artifact elicitationで具体例を得る。analysisではcoding、theme、negative case、researcher reflexivityを残す。
### 直感→図解→数式→例→実装または疑似コード
悪:「通知を改善したら使いますか」。良:「最後に通知を受けた時を、届く前から順に教えてください」。`claim→episode→artifact→consequence` とprobeする。
### よくある誤解
自然な会話ならdata品質十分、頻出発言=重要度、transcript=客観事実、ではない。
### 実務接続
workflow discovery、churn reason、mental model、sensitive experienceを探索する。
### 要点
- 過去の具体例を聞く。- 一問一概念。- neutral probe。- self-report限界を示す。- negative caseを探す。- consentと匿名化。
### 誤解チェック
1. 未来意図=行動か。2. 誘導質問は便利か。3. 頻度=severityか。4. transcriptは解釈不要か。5. artifactは有効か。
### 基礎問題
1. 誘導5問を直せ。2. guideを作れ。3. probeを三つ書け。4. code例を作れ。5. negative caseを探せ。
### 応用問題
1. inter-coder agreementの使い所を論ぜよ。2. cognitive interviewを調べよ。3. sensitive topic protocolを設計せよ。
### 設計問題
退会理由interviewをsampling、guide、safety、analysisまで設計せよ。
### 調査課題
実interview transcriptの匿名化・coding演習を行え。
### 知らないとする誤判断
「使いたい」という回答を将来利用率としてforecastする。
### 次章接続
発言では捉えにくい実際のworkをObservationで調べる。

## 第20章 Observation

### この章を学ぶ理由
人が実際に行うworkaround、artifact、interrupt、collaborationを現場文脈で捉える。
### 現場の問題
規定手順だけを聞き実作業を見ない、observer effectをゼロと仮定、秘匿情報を過収集する。
### 中心概念と正式定義
observationはbehaviorとcontextをsystematicに記録する方法。participant/non-participant、structured/unstructured、field/labを選ぶ。contextual inquiryは作業中のcontextで利用者をexpertとして問い、解釈を確認する。記録単位、時間sampling、event samplingを定義する。
### 直感→図解→数式→例→実装または疑似コード
`official workflow` と `observed workflow` を並べ、handoff、paper note、copy/paste、interruptをevent log化。観察者の解釈と事実記述を分ける。
### よくある誤解
観察=監視、見た一例=一般習慣、発話思考が自然行動を変えない、ではない。
### 実務接続
control room、warehouse、support desk、developer workflow、mobile contextに有効。
### 要点
- behavior/contextを記録。- 方法と単位を事前定義。- 事実/解釈を分離。- observer effectを報告。- privacyを最小化。- interpretationをmember check。
### 誤解チェック
1. 一件で一般化か。2. observationは無介入か。3. 規定手順=実作業か。4. screen録画は無条件可か。5. context inquiryは利用者がexpertか。
### 基礎問題
1. 記録sheetを作れ。2. event単位を定義せよ。3. 事実/解釈を分けよ。4. privacy fieldを削れ。5. workflow gapを描け。
### 応用問題
1. shadowing倫理を検討せよ。2. video codingを設計せよ。3. distributed ethnographyを調べよ。
### 設計問題
on-call引継ぎのfield observationを安全に設計せよ。
### 調査課題
実作業30分を同意の上観察し、artifactとinterruptを分析せよ。
### 知らないとする誤判断
manualに書かれた業務flowを現場の実行flowだと扱う。
### 次章接続
代表taskを実行してもらいinterface問題を検出するUsability Testingへ進む。

## 総合演習A（第1〜20章）

権限管理consoleで「保存したのに反映されない」「誤って全員を管理者にした」というincidentがある。認知、attention、working memory、mental model、affordance/signifier/feedback/mapping、slip/mistake、IA、accessibility、research方法を横断し、原因仮説を優先順位化する。各仮説に反証可能な観察、改善後metric、当事者を含む評価計画を付けよ。

## 第21章 Usability Testing

### この章を学ぶ理由
代表利用者が代表taskを行う過程から、goal達成を妨げるinterface条件を観察する。
### 現場の問題
demo、好み調査、QAをusability testと呼ぶ。moderatorが助け過ぎ、task文がUI語を教える。
### 中心概念と正式定義
usability testingは参加者へtaskを与え、performance、behavior、発話を観察して問題を同定・測定する評価法。formativeは問題発見、summativeはbenchmark。task success criteria、severity、assistance rule、counterbalancing、think-aloudの影響を定義する。小標本は問題発見に有用でも母比率精密推定とは別。
### 直感→図解→数式→例→実装または疑似コード
`scenario（goal）→unassisted attempt→observable behavior→probe→debrief`。「設定menuを開け」でなく「請求通知を止めてください」。
### よくある誤解
5人で85%を常に発見、発言がない=問題なし、moderator救助=成功、ではない。
### 実務接続
prototype、staging、competitor、accessibility flowをrelease前後に評価する。
### 要点
- 代表task/userを選ぶ。- goal文で提示。- successを事前定義。- assistanceを記録。- severityを根拠化。- 発見と推定を分ける。
### 誤解チェック
1. QAと同じか。2. 5人は普遍か。3. 好みだけ聞くか。4. 助言後成功はunassistedか。5. think-aloudは無影響か。
### 基礎問題
1. task文を直せ。2. success criteriaを作れ。3. observer sheetを作れ。4. severityを付けよ。5. moderator scriptを書け。
### 応用問題
1. sample sizeを目的別に設計せよ。2. remote unmoderatedのbiasを分析せよ。3. comparative testをcounterbalanceせよ。
### 設計問題
送金flowの安全critical usability testを中止条件まで設計せよ。
### 調査課題
Nielsen–Landauer modelの前提と批判を一次資料で調べよ。
### 知らないとする誤判断
5人testを一回行えば、全segment・全taskの問題を発見済みとみなす。
### 次章接続
行動logとsurveyを使うQuantitative UXへ進む。

## 第22章 Quantitative UX

### この章を学ぶ理由
行動を数値化しつつ、metricの構成概念妥当性、denominator、分布、交絡を守る。
### 現場の問題
click数をengagement、滞在時間を価値、平均を全員の代表と誤認する。
### 中心概念と正式定義
constructは直接観測できない概念、operationalizationは測定手続きへの翻訳。reliabilityは測定の一貫性、validityは意図したものを測る程度。funnel率は各stageのeligible母数を明示。HEART等の枠組みは選択支援であり、metricの妥当性を自動保証しない。分位点、cohort、segment、欠測を扱う。
### 直感→図解→数式→例→実装または疑似コード
完了率 `completed/started` と `completed/eligible` は違う。latencyはmedian,p90,p99、errorはseverity別。guardrailとcounter-metricを置く。
### よくある誤解
測れるもの=重要なもの、dashboard増加=理解、相関=改善効果、North Star一つで十分、ではない。
### 実務接続
product analytics、SLO、survey、support、quality metricを共通event schemaへ結ぶ。
### 要点
- constructから始める。- denominatorを固定。- 分布/segmentを見る。- missingを分析。- guardrailを置く。- qualitative証拠と接続。
### 誤解チェック
1. click=価値か。2. reliability=validityか。3. 平均でtailを表せるか。4. denominatorは自明か。5. metric向上=因果か。
### 基礎問題
1. constructを操作化せよ。2. funnelを計算せよ。3. denominator違いを示せ。4. guardrailを選べ。5. event schemaを作れ。
### 応用問題
1. Goodhart則を適用せよ。2. missing-not-at-randomを分析せよ。3. latent construct scaleを評価せよ。
### 設計問題
developer toolのUX scorecardを速度、成功、学習、満足、安全で設計せよ。
### 調査課題
既存dashboardのmetric lineageと妥当性をauditせよ。
### 知らないとする誤判断
観測しやすいclickを、利用者goal達成の代理として最適化する。
### 次章接続
介入の因果効果を推定するExperiment Designへ進む。

## 第23章 Experiment Design

### この章を学ぶ理由
UI変更後の差を季節性・選択biasから分け、倫理的に因果推論する。
### 現場の問題
前後比較だけで効果断定、多重metricから有意なものだけ報告、novelty effectを恒久効果とする。
### 中心概念と正式定義
potential outcomesで個体iの効果は `Y_i(1)-Y_i(0)` だが同時観測不能。random assignmentにより期待上のexchangeabilityを作りATEを推定する。割当遵守、attrition、計測欠損、spilloverはrandomization後にもbiasやestimandの変化を生む。primary outcome、unit、sample size/power、alpha、effect size、stopping rule、interferenceを事前定義する。統計的有意性と実務的重要性を分ける。
### 直感→図解→数式→例→実装または疑似コード
`eligible→randomize→A/B→same measurement→difference+CI`。cluster間干渉があるcollaboration UIではuser単位randomizationが汚染される。
### よくある誤解
p<.05=95%で仮説真、randomizationで実装bugも消える、A/Bなら倫理審査不要、ではない。
### 実務接続
feature flag、A/B platform、canary、switchback testでexposureとanalysis unitを一致させる。
### 要点
- estimandを定義。- randomize unitを選ぶ。- primary metricを事前指定。- effect/CIを見る。- interferenceを扱う。- stopping/ethicsを決める。
### 誤解チェック
1. 前後差=因果か。2. p値=仮説確率か。3. sample増加で重要性増すか。4. 干渉は無視できるか。5. harmful patternも実験可か。
### 基礎問題
1. hypothesisを書け。2. unitを選べ。3. primary/guardrailを決めよ。4. attritionを分析せよ。5. CIを解釈せよ。
### 応用問題
1. sequential testingを調べよ。2. CUPEDを説明せよ。3. cluster randomizationを設計せよ。
### 設計問題
checkout確認変更の実験を安全性、power、stoppingまで設計せよ。
### 調査課題
公開A/B事例のestimandとthreats to validityを批評せよ。
### 知らないとする誤判断
有意差の出たmetricだけを後から目的指標にする。
### 次章接続
利用者利益に反して行動を誘導するDark Patternを扱う。

## 第24章 Dark Pattern

### この章を学ぶ理由
短期conversionを利用者自律、privacy、fairness、長期trustより優先するinteractionを識別・防止する。
### 現場の問題
解約を隠す、拒否を薄くする、偽のscarcity、subscriptionをdefaultにする。
### 中心概念と正式定義
deceptive/manipulative designはinterfaceが利用者の情報不足、attention、default bias等を利用し、十分な理解・自由な選択を損なう設計。obstruction、sneaking、interface interference、forced action、nagging等をbehavior mechanismとharmで分類する。conversion上昇はinformed consentを証明しない。
### 直感→図解→数式→例→実装または疑似コード
`business goal→choice architecture→user belief/action→short metric→downstream harm`。accept/rejectを同程度に見つけやすくし、total costと継続条件を決定前に示す。
### よくある誤解
法律違反だけがdark pattern、利用者がclickしたので同意、競合も行うので必要、ではない。
### 実務接続
consent、subscription、privacy、game monetization、notification permission、security warningに現れる。
### 要点
- 自律と理解を守る。- actionだけでなくbeliefを測る。- 拒否/取消を対称化。- total costを事前表示。- vulnerable群のharmを見る。- 長期trustをmetric化。
### 誤解チェック
1. click=同意か。2. 合法=非操作的か。3. defaultは中立か。4. conversionだけで成功か。5. cancel難化はretentionか。
### 基礎問題
1. patternを分類せよ。2. harm chainを描け。3. consent copyを直せ。4. choice symmetryを評価せよ。5. counter-metricを選べ。
### 応用問題
1. vulnerability差を分析せよ。2. recommender manipulationを論ぜよ。3. regulatory原則を調べよ。
### 設計問題
subscription signup/cancelをinformed consentと事業持続性の両方で設計せよ。
### 調査課題
実製品flowを証拠付きでdark pattern auditせよ。
### 知らないとする誤判断
一時的conversion向上を利用者価値の増加とみなす。
### 次章接続
誤りが生命・環境・重大資産へ波及するSafety-critical UIへ進む。

## 第25章 Safety-critical UI

### この章を学ぶ理由
低頻度でも重大なhazardへ、多層防護、明確なauthority、safe recoveryを設計する。
### 現場の問題
alarm洪水、mode confusion、automation bias、confirm疲れ、緊急時に手順を記憶要求する。
### 中心概念と正式定義
hazardはharmへ至り得るsystem状態、riskはseverityとlikelihoodの組合せ。safety constraintはhazardを防ぐsystem-level条件。defense-in-depth、forcing function、interlock、fail-safe、graceful degradationを使う。human reliabilityを単一error probabilityに丸めずtask/context依存で扱う。
### 直感→図解→数式→例→実装または疑似コード
STPA的に `unsafe control action→hazard→loss` を追う。alarmはpriority、原因、必要action、期限を示し、ackとresolutionを分ける。
### よくある誤解
confirm二回=安全、operatorをloop内に置けば責任移転、automationはerror除去、ではない。
### 実務接続
medical、aviation、industrial control、production deploy、finance risk consoleに適用する。
### 要点
- hazardから設計。- severityを優先。- mode/authorityを可視化。- alarmをactionableに。- 多層防護。- degraded/recoveryをtest。
### 誤解チェック
1. error率低=安全か。2. confirm数=安全度か。3. automationには新しいerrorがないか。4. ack=解決か。5. fail-safeは全system同じか。
### 基礎問題
1. hazardを列挙せよ。2. constraintを書け。3. unsafe actionを分析せよ。4. alarmを改善せよ。5. degraded modeを設計せよ。
### 応用問題
1. FMEAとSTPAを比較せよ。2. automation surpriseを分析せよ。3. resilience engineeringを調べよ。
### 設計問題
production traffic切替UIを二人承認、simulation、rollback、監査込みで設計せよ。
### 調査課題
公開安全事故のinterface寄与を一次報告から分析せよ。
### 知らないとする誤判断
危険actionへ確認dialogを重ねるだけでhazardを制御したと思う。
### 次章接続
熟練者の高頻度作業を支えるDeveloper Tool UXへ進む。

## 第26章 Developer ToolのUX

### この章を学ぶ理由
開発者を「複雑さを我慢できるexpert」とせず、認知flow、debuggability、composabilityを生産性と安全性へ結ぶ。
### 現場の問題
曖昧error、破壊的default、hidden state、長いfeedback loop、script不能GUI。
### 中心概念と正式定義
developer experienceはsetup、learn、build、debug、operate、extendのend-to-end interaction品質。information scent、progressive disclosure、locality of information、determinism、inspectability、reversibility、automation surfaceを評価する。time-to-first-successだけでなくtime-to-diagnose/recoverを測る。
### 直感→図解→数式→例→実装または疑似コード
良いerrorは `what failed / why / evidence / next action / stable ID`。CLIはexit code、stdout/stderr、dry-run、idempotent optionを契約する。
### よくある誤解
expertはhelp不要、option数が多いほどpowerful、telemetryで個人をrankすれば生産性、ではない。
### 実務接続
IDE、CLI、SDK、CI、observability、internal platform、error APIに現れる。
### 要点
- 診断時間を測る。- stateをinspect可能に。- safe default/dry-run。- scriptable contract。- stable error identity。- workflow全体を評価。
### 誤解チェック
1. expertにdiscoverability不要か。2. error stackだけでactionableか。3. GUIだけでautomation可か。4. activity=productivityか。5. reversibilityは重要か。
### 基礎問題
1. error messageを直せ。2. CLI contractを書け。3. feedback loopを測れ。4. hidden stateを列挙せよ。5. dry-runを設計せよ。
### 応用問題
1. cognitive dimensions of notationsを適用せよ。2. API discoverabilityを測れ。3. telemetry倫理を分析せよ。
### 設計問題
database migration toolをpreview、approval、resume、rollbackまで設計せよ。
### 調査課題
OSS CLI一つのissueからUX failure taxonomyを作れ。
### 知らないとする誤判断
利用者がengineerなら曖昧な状態やerrorも自力で解決できると考える。
### 次章接続
programmerが利用者となるAPI interfaceをHCIとして扱う。

## 第27章 APIもHCIであるという視点

### この章を学ぶ理由
type、name、default、error、versioningをprogrammerのmental modelと誤用可能性から設計する。
### 現場の問題
boolean引数の意味不明、非対称命名、部分成功が200、retryabilityが不明、SDK間差。
### 中心概念と正式定義
APIは人がコードを通じてsystemと相互作用するinterface。affordanceはtype/signature/permission、signifierはname/docs/example、feedbackはreturn/error/trace、mappingはparameter-effect対応。poka-yokeは不正状態を表現しにくくする。semantic versioning等は互換性のcommunication contractであり意味変化を完全自動判定しない。
### 直感→図解→数式→例→実装または疑似コード
`deploy(env, False, True)` より `deploy(target=Production(), strategy=Canary(percent=10))`。errorにはstable code、context、retryable、request IDを持たせる。
### よくある誤解
docsで悪いsignatureを補える、type-safe=misuse-proof、REST形だけで良API、breakingはcompile errorだけ、ではない。
### 実務接続
SDK、CLI、schema、DB migration、event contract、observabilityを一つのdeveloper journeyで見る。
### 要点
- programmerも利用者。- typesで選択を制約。- name-effectを一致。- errorをactionableに。- safe default。- migration pathをtest。
### 誤解チェック
1. docsで全部補えるか。2. bool列は明瞭か。3. type-safeならsemantic misuseはないか。4. error codeはfeedbackか。5. API変更はsyntaxだけか。
### 基礎問題
1. signatureを改善せよ。2. error schemaを作れ。3. defaultを評価せよ。4. misuse caseを列挙せよ。5. migration guideを書け。
### 応用問題
1. typestate patternを調べよ。2. protocol evolutionを分析せよ。3. API usability testを設計せよ。
### 設計問題
課金APIをidempotency、money type、error、sandbox、versioning込みで設計せよ。
### 調査課題
実SDKのsupport issueをmental model mismatchとして分析せよ。
### 知らないとする誤判断
機械が解釈できるschemaなら人にも安全に使えると考える。
### 次章接続
複数原理を一つのUI事故へ統合するcase studyへ進む。

## 第28章 ケーススタディ――本番削除console

### この章を学ぶ理由
誤削除を「不注意」で終えず、認知・interaction・組織・安全防護の連鎖として改善する。
### 現場の問題
operatorはstagingと思い、production tenantをbulk選択し、曖昧なconfirm後削除。toastは成功、restore不能、監査にはIDだけが残った。
### 中心概念と正式定義
safety invariantは「production bulk deleteは承認済みscope・復元可能期間・明示authorityでのみ確定」。slip仮説（target近接）、mistake仮説（environment model）、attention仮説（warning habituation）、organizational仮説（time pressure）を優先度と証拠で分ける。risk priorityはseverityを第一にfrequency/exposure/detectabilityを併記する。
### 直感→図解→数式→例→実装または疑似コード
`latent pressure→similar environments→weak signifier→scope hidden→generic confirm→irreversible effect`。Countermeasure: reversible tombstone+delayed purge（assumed cause: recovery layer欠落）。Countermeasure: environment-bound credential+fencing（assumed cause: UI表示だけでtarget区別）。
### よくある誤解
赤色追加、文言強化、本人再教育だけでは同じcausal pathを断てない。
### 実務接続
admin tool、cloud console、database client、CI deploy UIのhazard reviewに使う。
### 要点
- invariantから分析。- 仮説を機序別にする。- severityを優先。- irreversibleを減らす。- authorityをsystem強制。- auditをrecoveryへ使う。
### 誤解チェック
1. 赤色だけでtarget分離か。2. typed confirmは万能か。3. soft deleteは防護か。4. operator教育で環境混同消滅か。5. auditはIDだけで十分か。
### 基礎問題
1. causal graphを描け。2. error typeを分類せよ。3. invariantを書け。4. defense layerを五つ作れ。5. metricを決めよ。
### 応用問題
1. two-person controlの共通mode失敗を分析せよ。2. restore drillを設計せよ。3. production access UXを評価せよ。
### 設計問題
consoleをcredential、preview、approval、delay、undo、auditまで再設計せよ。
### 調査課題
公開cloud誤削除事故を同じ仮説順で分析せよ。
### 知らないとする誤判断
warningの色と文言だけ変更して根本対策とする。
### 次章接続
未知UIを改善proposalへまとめる総合演習へ進む。

## 総合演習B（第21〜28章）

developer portalのsignup→API key→first request→error recoveryを対象に、formative test、quantitative scorecard、experiment、dark pattern audit、safety、developer UX、API usabilityを統合せよ。sample/inference境界、WCAG test、primary metric/guardrail、rollbackを含む研究・実装計画を作る。

## 第29章 UI改善演習

### この章を学ぶ理由
見た目の変更案で終えず、仮説、evidence、prototype、評価、rolloutを一貫させる。
### 現場の問題
「buttonを目立たせる」のような原因不明の改修、metric上昇だけでharmを見落とす。
### 中心概念と正式定義
改善単位を `observed problem→assumed cause→design mechanism→predicted outcome→measure→falsification→rollout` とする。countermeasureは必ず「work（assumed cause）」で記録し、causeが否定されたら採用しない。severity、reach、confidence、effortは同列でなく、安全上重大なhypothesisを先に検証する。
### 直感→図解→数式→例→実装または疑似コード
例: Countermeasure: 選択対象summaryをconfirm直前に固定表示（assumed cause: working memoryからscopeが脱落）。成功率だけでなくwrong-target率と取消率を測る。
### よくある誤解
best practiceは調査不要、A/B勝者は全segmentへ安全、prototype fidelityが高いほど早期から良い、ではない。
### 実務接続
design critique、issue、ADR、feature flag、analytics、support feedbackを一つのtraceへする。
### 要点
- 観測と原因を分ける。- mechanismを明記。- falsificationを書く。- safety仮説を優先。- counter-metricを置く。- 段階rolloutする。
### 誤解チェック
1. best practiceで仮説不要か。2. conversionだけで判断か。3. 全segment同効果か。4. 原因否定後も案を実装か。5. rollback条件は必要か。
### 基礎問題
1. 悪い提案5件を仮説形式へ直せ。2. metricを選べ。3. counter-metricを作れ。4. prototype方法を選べ。5. rollout段階を書け。
### 応用問題
1. mixed-method triangulationを設計せよ。2. heterogeneous treatment effectを検討せよ。3. longitudinal effectを測れ。
### 設計問題
利用率低下したnotification設定をresearchからrolloutまで完全に改善せよ。
### 調査課題
実issue一件を選び、証拠のないcause inferenceを洗い出せ。
### 知らないとする誤判断
好みのsolutionを先に決め、後から利用者問題を当てはめる。
### 次章接続
最後に頻出誤判断を原因仮説と構造対策へ圧縮する。

## 第30章 この分野を知らないエンジニアが陥りやすい誤判断

### この章を学ぶ理由
HCI欠如が生む頻出誤判断を、採否を利用者contextで検証できるcountermeasureへ変える。
### 現場の問題
簡単なvisual変更から着手すると、重大hazard、accessibility exclusion、誤mental modelを放置する。
### 中心概念と正式定義
優先順位は原則としてharm severity、exposure、発生可能性、回復可能性、evidence confidenceで決める。以下は典型的な順であり、各案件で反証する。
### 直感→図解→数式→例→実装または疑似コード
`behavior/problem→ranked assumed cause→evidence→countermeasure→task outcome→unintended harm`。screen changeではなくhuman-system loopを直す。

1. Countermeasure: hazardとsafety constraintから再設計する（assumed cause: 重大errorを通常のusability問題として扱っている）。
2. Countermeasure: reversible actionと遅延確定を設ける（assumed cause: 一回のslipが不可逆harmへ直結する）。
3. Countermeasure: authority/targetをcredentialとsystem stateで強制する（assumed cause: 色や注意力だけで本番を区別している）。
4. Countermeasure: 利用者goalのtask successを測る（assumed cause: 内部仕様適合を利用成功と同一視している）。
5. Countermeasure: actual/perceived affordanceをmodality別にtestする（assumed cause: 見た目だけで操作可能性を判断している）。
6. Countermeasure: actionableでpersistentなfeedbackを状態機械へ対応させる（assumed cause: 受理・進行・完了を同じ成功表示にしている）。
7. Countermeasure: mental model予測testを行う（assumed cause: docs未読を誤操作の原因にしている）。
8. Countermeasure: slip/mistakeを分類して別対策を出す（assumed cause: 全errorへ確認dialogを追加している）。
9. Countermeasure: alarmをpriority・action・期限で削減統合する（assumed cause: 重要情報をすべて強調しalarm fatigueを生んでいる）。
10. Countermeasure: 中間stateとscopeを画面へ外部化する（assumed cause: working memoryへIDや対象を保持させている）。
11. Countermeasure: WCAG 2.2＋manual＋当事者task testを行う（assumed cause: 自動scannerをaccessibility証明にしている）。
12. Countermeasure: semantic native controlへ戻す（assumed cause: custom controlがname/role/value/focusを再実装できていない）。
13. Countermeasure: keyboard/touch/voice代替を用意する（assumed cause: drag/hoverだけを操作経路にしている）。
14. Countermeasure: IAを利用者語彙と探索taskで再構成する（assumed cause: 組織図をnavigationにしている）。
15. Countermeasure: completion失敗者を含む分位点・severity metricを使う（assumed cause: 成功者の平均時間だけ見ている）。
16. Countermeasure: 初回・反復・保持・転移を別測定する（assumed cause: onboarding通過を学習と見なす）。
17. Countermeasure: research questionに合うsample/methodを選ぶ（assumed cause: 同僚数名を代表利用者にしている）。
18. Countermeasure: 過去の具体episodeをneutralに聞く（assumed cause: 将来意図と要望を行動forecastにしている）。
19. Countermeasure: 現場観察でworkaroundとinterruptを記録する（assumed cause: manual記載を実作業だと考えている）。
20. Countermeasure: formative testと母比率推定を分ける（assumed cause: 5人testで全問題を発見したと思う）。
21. Countermeasure: construct、denominator、guardrailを定義する（assumed cause: clickや滞在時間を価値と同一視している）。
22. Countermeasure: randomization・primary outcome・stopping ruleを事前登録する（assumed cause: 前後差やp値選別で効果を断定している）。
23. Countermeasure: choice symmetryとinformed understandingを測る（assumed cause: conversion上昇を同意品質と見なす）。
24. Countermeasure: 人を責めずlocal rationalityとdefense gapを分析する（assumed cause: human errorをroot causeにしている）。
25. Countermeasure: novice/expert双方でdeveloper workflowをtestする（assumed cause: engineerなら複雑さを理解できると思う）。
26. Countermeasure: APIをtype/name/default/errorでmisuse-resistantにする（assumed cause: docsで悪いsignatureを補おうとしている）。
27. Countermeasure: inclusive participantを初期設計へ含める（assumed cause: average user向け完成後に例外対応している）。
28. Countermeasure: business metricにtrust、complaint、cancel、harmを併記する（assumed cause: short-term conversionだけ最適化している）。
29. Countermeasure: causeを反証してからsolutionを選ぶ（assumed cause: 好みのUI案を問題へ当てはめている）。
30. **rare** Countermeasure: neuroergonomic/physiological計測を妥当性検証付きで使う（assumed cause: 通常の行動・発話では捉えられない安全critical workloadが主要riskである）。

### よくある誤解
この一覧も万能heuristicではない。対象task・population・environmentのevidenceで原因順位を更新し、低確率仮説を同じ深さで追わない。
### 実務接続
design review、accessibility audit、incident review、research plan、experiment preregistrationへ「仮説・証拠・対策・副作用」を残す。
### 要点
- harmの重大性を優先。- 人間をsystem boundaryへ含める。- 原因を反証可能に。- task outcomeで測る。- 多様な利用者を含める。- 対策の副作用も追う。
### 誤解チェック
1. 上位順は全製品で固定か。2. visual改善だけでHCIか。3. scanner合格でtask成功か。4. p値で実務価値が決まるか。5. rare仮説を先に測るべきか。
### 基礎問題
1. 自製品の上位5仮説を選べ。2. 各反証観察を書け。3. harm matrixを作れ。4. counter-metricを決めよ。5. accessibility taskを一つ作れ。
### 応用問題
1. 二つの誤判断の因果loopを描け。2. segment別副作用を予測せよ。3. longitudinal評価を設計せよ。
### 設計問題
既存admin UIを30項目でauditし、最優先三原因のresearch、改修、評価、rolloutを設計せよ。
### 調査課題
公開UX事故またはregulatory actionを一件選び、想定原因とsystem countermeasureを証拠で再評価せよ。
### 知らないとする誤判断
HCI checklistを満たすことを、対象利用者のgoal達成を検証する代わりにする。
### 次章接続
確率統計、software engineering、securityを併読し、不確実性、変更管理、secure usabilityを深める。

## 参考文献

- Norman, *The Design of Everyday Things*, Revised and Expanded Edition.
- Rogers, Sharp, Preece, *Interaction Design*.
- Wickens et al., *Engineering Psychology and Human Performance*.
- Reason, *Human Error*; Dekker, *The Field Guide to Understanding Human Error*.
- W3C, [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)（2024-12-12 Recommendation、参照日2026-08-27）。
- W3C, [WCAG 2.2 approved as ISO/IEC 40500:2025](https://www.w3.org/press-releases/2025/wcag22-iso-pas/).
- ISO 9241-11, *Ergonomics of human-system interaction — Usability: Definitions and concepts*.

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **設計対象は画面ではなく、人間・道具・環境からなる feedback loop である。** 人は goal を立てて action し、system state を知覚・解釈して次の action を選ぶ。正式には execution と evaluation の gulf、feedback、制約、環境内の interruption を含めて task を捉える。実務では button の見た目だけでなく、受理・進行・結果・回復が loop を閉じているかを評価する。
2. **利用者は system の実装ではなく、経験から作った mental model で予測する。** 説明書の正しさより、「この操作の次に何が起こると思うか」という予測が行動を決める。正式には designer の conceptual model、system image、user model のずれとして扱う。実務では誤操作を注意不足に帰さず、予測質問と teach-back で model のずれを見つける。
3. **認知資源は有限で、情報は環境へ外部化できる。** working memory、注意、知覚は interruption、時間圧、疲労でさらに狭くなる。正式には recognition over recall、外的表象、signal detection、複数 resource の競合として説明する。実務では対象、mode、中間状態、次の action を interface に保持し、利用者の記憶や警戒心を安全機構にしない。
4. **人の error は分類すべき system outcome であり、原因の終点ではない。** slip と mistake、local rationality、latent condition を区別すると対策が変わる。正式には意図・action・結果のどこで乖離したかと、防護層がなぜ通過を許したかを分析する。実務では確認 dialog の乱造を避け、不可逆性、default、authority、feedback、回復可能性を構造から直す。
5. **測定値は構成概念・母集団・文脈・分布を伴う。** click、時間、満足度は利用者価値そのものではなく、その代理指標である。正式には construct validity、sampling、denominator、分位点、因果推論、guardrail を明示する。実務では平均 conversion だけでなく task success、失敗者、accessibility、trust、long-term harm を併せて意思決定する。

### 専門家の意見が根本的に分かれる3つの論点

1. **設計方向を利用者調査から漸進的に導くか、専門家の強い vision で先導するか。** **立場A（participatory / research-led）の steelman:** 利用者は situated work と workaround の専門家であり、初期から意思決定へ参加しなければ、組織権力や身体差を designer の仮定で上書きしてしまう。**立場B（vision-led）の steelman:** 利用者は現状の道具に適応した要求しか語れないことがあり、radical な interaction は技術と design space を知る専門家が一貫した仮説として作らなければ生まれにくい。問題の新規性、被害の重大性、対象者の発言力、試作の可逆性、行動 evidence の質で両者の比重が変わる。
2. **一貫した共通 interface を守るか、個人・文脈へ適応させるか。** **立場A（標準化）の steelman:** predictable な mapping と platform convention は学習転移、共同作業、support、accessibility を支え、予期しない自動変化による mode error を防ぐ。**立場B（適応・personalization）の steelman:** 能力、熟練、言語、device、状況が異なる人へ同じ interface を強いること自体が exclusion であり、適応は不要な認知負荷を大きく下げる。shared workflow、説明可能性、設定負担、privacy、変化の可逆性、個人差の安定性によって判断が変わる。
3. **行動を滑らかに誘導する nudge を積極利用するか、摩擦を残して熟慮と autonomy を守るか。** **立場A（nudge / friction reduction）の steelman:** default と簡潔な flow は認知負荷と先延ばしを減らし、利用者自身が望む健康、安全、完了へ到達させられる。**立場B（autonomy / deliberate friction）の steelman:** 誰の利益を最適化するか不透明な誘導は manipulation になり、重大・不可逆な選択では理解、対称な選択肢、撤回可能性のための摩擦が必要である。stakes、可逆性、利益相反、利用者の既存意図、緊急性、理解を測れるかで許容範囲が変わる。

### 深い理解と暗記を見分ける10の質問

1. 本番 database の削除事故に確認 dialog を追加したが事故が続いた。slip、mistake、mode error、authority、回復可能性の仮説を優先順位付きで比較し、dialog 以外の構造対策を設計せよ。
2. 新機能の平均完了時間は短縮したが、完了率と問い合わせ数が悪化した。この三つを同時に説明できる denominator と survivor bias の反例を作り、次に見る分布を示せ。
3. accessibility scanner が全項目合格した画面で screen reader 利用者が task を完了できない。自動検査の保証範囲を説明し、semantic、focus、dynamic state、利用者 test の順に調査を設計せよ。
4. 熟練者向け shortcut を追加すると novice の発見可能性が下がるという仮説がある。progressive disclosure、consistency、学習転移を使って、両者を同じ interface で支える案と評価指標を示せ。
5. 利用者 interview では「通知を増やしてほしい」が多数だったが、通知追加後に反応率が落ちた。発言と行動が食い違う原因仮説、反証 evidence、alarm fatigue を避ける redesign を述べよ。
6. A/B test で conversion が有意に上昇した consent flow を採用すべきか。randomization が保証することとしないことを分け、理解、choice symmetry、取消、長期 trust の guardrail を設計せよ。
7. 医療 alarm の false positive を減らすと見逃しが増える。signal detection の trade-off を、単一の accuracy ではなく base rate、cost、operator workload、escalation 経路から決めよ。
8. 国際化した navigation で、組織が使う正式用語と利用者が探す語彙が一致しない。card sorting の結果だけに従う場合の反例を挙げ、IA、検索、権限、規制表記をどう両立するか。
9. personalization が操作時間を減らした一方、利用者が「勝手に変わる」と感じた。適応の便益を残しながら predictability、control、privacy、accessibility を検証する interaction contract を作れ。
10. 事故報告に「operator が手順を守らなかった」とある。その場では合理的だった可能性を再構成するため、目標、時間圧、表示、組織 incentive、防護層について何を調べ、どの反例なら interface 原因説を棄却するか。
