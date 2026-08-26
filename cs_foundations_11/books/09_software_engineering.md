# ソフトウェア工学――変更可能性を管理する

## はじめに

Software Engineering は「きれいなコード」の作法集ではない。複数人が長期間、変化する要求と運用環境の下で、社会技術システムの変更リスクを管理する学問である。本書では設計、実装、検証、配備、運用、組織を一つの feedback system として扱う。特定の流行フレームワークでなく、責務、契約、情報流、可逆性、証拠という長寿命の原理を中心にする。

---

## 第1章　Programming と Software Engineering

### この章を学ぶ理由／現場の問題

一人で正しく動くプログラムと、十年変更できるソフトウェアは評価軸が違う。後者ではコードだけでなく人、手順、依存、データ、運用が成果物である。

### 中心概念と正式な定義

programming は計算手続きの実装、software engineering はソフトウェアの指定、開発、検証、配備、運用、進化へ工学的に取り組む活動と捉える。品質を機能適合性だけでなく reliability、maintainability、security、performance 等の quality attribute のベクトル \(Q=(q_1,\dots,q_k)\) とする。変更コストはコード行数でなく、影響範囲、調整、検証、移行、復旧の総費用。

### 直感 → 図解 → 数式 → 例 → 実装

```text
idea -> code -> build -> deploy -> operate -> learn -> changed idea
             people, data, dependencies, controls span all stages
```

```python
@dataclass
class Change:
    code: list[str]; schema: list[str]; rollout: str; rollback: str; owner: str
```

単機能スクリプトをservice化すると、availability、observability、ownership、versioning が要求へ追加される。

### よくある誤解／実務接続

- 行数や抽象化数が少ないこと自体は保守性でない。
- 「動く」は現在の観測例であって契約充足の全証拠ではない。
- process は個人能力の代用品でなく、複数人の情報損失を制御する。
- 開発速度と品質は単純な反対軸ではなく、小さく安全な変更は両方を上げる。

### 要点

1. 対象はコードを含む社会技術システム。 2. ライフサイクル全体の費用を見る。 3. 品質属性は複数。 4. 変更可能性が中心。 5. 証拠とfeedbackで不確実性を減らす。

### 誤解チェック（5問）

1. 良いprogrammerだけで長寿命systemを保証できるか。 2. 行数が少なければ変更容易か。 3. 運用は開発外か。 4. ドキュメントは常にコードより古いか。 5. speedとqualityは必ずtrade-offか。

### 基礎問題（5問）

1. 小scriptのservice化で増える責務を列挙せよ。 2. quality attributeを五つ定義せよ。 3. 変更総費用を分解せよ。 4. 社会技術境界を描け。 5. 成功の証拠を三段階で挙げよ。

### 応用問題（3問）／設計問題／調査課題

1. 高速だが変更不能なsystemを分析せよ。 2. 開発・運用分離のfeedback損失を論ぜよ。 3. 可逆性と速度の関係を説明せよ。 **設計:** 一機能のend-to-end ownershipを設計せよ。 **調査:** 自チームの変更lead timeを構成要素へ分解せよ。

### 知らないとする誤判断／次章への接続

実装完了を価値提供完了とし、移行・監視・復旧を別仕事へ追い出す。次章では価値が生まれて廃止されるまでのライフサイクルを扱う。

---

## 第2章　Software Lifecycle

### この章を学ぶ理由／現場の問題

局所的な実装最適化は、要件誤りや配備失敗、保守費を増やし得る。全段階を一方向の工程でなく、仮説を検証する反復ループとして設計する。

### 中心概念と正式な定義

ライフサイクルは discovery、requirements、architecture/design、implementation、verification、release、operation、evolution、retirement の活動集合。各成果物を baseline とし、変更を traceable にする。feedback latency \(T_f\) は仮説設定から反証可能な観測までの時間、batch size \(B\) が大きいほど一般に統合・復旧リスクが増える。

### 直感 → 図解 → 数式 → 例 → 実装

```text
discover -> specify -> build -> verify -> release -> observe
   ^                                                   |
   +-------------------- learn ------------------------+
```

```yaml
change:
  hypothesis: "checkout abandonment decreases"
  acceptance: "-2% with no error-budget regression"
  rollout: "1% -> 10% -> 50% -> 100%"
  retirement: "remove old path and flag by date"
```

### よくある誤解／実務接続

- lifecycle は必ず waterfall という意味ではない。
- maintenance は完成後の残務でなく総費用の主要部分。
- release と deploy、deploy と exposure を区別する。
- 廃止条件がないfeature flagやAPI versionは永続的分岐になる。

### 要点

1. 活動は反復する。 2. feedback latencyを短くする。 3. baselineとtraceabilityを持つ。 4. deploy/release/exposureを分ける。 5. retirementまで計画する。

### 誤解チェック（5問）

1. lifecycleは一回だけか。 2. deploy=releaseか。 3. maintenanceはbug fixだけか。 4. flagは永続互換層か。 5. 小batchは常に機能価値も小さいか。

### 基礎問題（5問）

1. 一変更を全活動へ写せ。 2. feedback loopを三つ挙げよ。 3. baselineを定義せよ。 4. releaseとexposureを例で分けよ。 5. retirement criteriaを書け。

### 応用問題（3問）／設計問題／調査課題

1. 大batchのfailure modeを分析せよ。 2. schema移行の二世代期間を設計せよ。 3. 廃止不能featureを再設計せよ。 **設計:** 一変更のlifecycle evidence graphを設計せよ。 **調査:** 一機能のidea-to-retirement履歴を追跡せよ。

### 知らないとする誤判断／次章への接続

「mergeしたので完了」とし、利用・効果・旧経路削除を追わない。次章では解くべき問題を合意可能な要求へ変換する。

---

## 第3章　Requirements Engineering

### この章を学ぶ理由／現場の問題

正確に実装した誤った要求は最も高価である。stakeholderの発言をそのまま仕様とせず、目的、制約、競合、検証方法を発見・交渉する。

### 中心概念と正式な定義

requirements engineering は elicitation、analysis、specification、validation、management。stakeholder はsystemに利害を持つ主体。requirement \(r\) は観測可能な必要能力または制約として、source、rationale、priority、acceptance evidence、dependencies、statusを持つ。traceability relation \(T\subseteq R\times D\times C\times Test\) で要求から設計・コード・検証を辿る。

### 直感 → 図解 → 数式 → 例 → 実装

```text
goal "reduce fraud"
 -> assumptions -> capabilities -> measurable acceptance -> evidence
 -> conflicting goals: conversion, privacy, latency
```

```yaml
requirement: "risk score returned within 100ms p99 at 2k rps"
rationale: "checkout timeout budget"
verification: "production-like load test"
owner: "risk-platform"
```

### よくある誤解／実務接続

- 顧客の解決案は要求候補であって唯一解でない。
- user storyだけでは例外・制約・品質属性を十分表さない。
- 曖昧語「高速」「安全」「柔軟」は測定条件へ変換する。
- requirement churn は全て悪でなく学習の結果。ただし影響をtraceする。

### 要点

1. 要求は発見・交渉する。 2. goalとsolutionを分ける。 3. source/rationaleを残す。 4. acceptance evidenceを定義。 5. traceabilityで変更影響を追う。

### 誤解チェック（5問）

1. stakeholderの最初の案が仕様か。 2. user storyだけで十分か。 3. requirement changeは失敗か。 4. acceptance criteriaは実装手順か。 5. 全stakeholderの要求は両立するか。

### 基礎問題（5問）

1. 解決案をgoalへ戻せ。 2. stakeholder mapを作れ。 3. 曖昧要求を測定可能にせよ。 4. conflictを一つ解け。 5. trace linkを書け。

### 応用問題（3問）／設計問題／調査課題

1. hidden stakeholderを発見せよ。 2. regulatory requirementを分解せよ。 3. assumption failureを分析せよ。 **設計:** checkout改善のrequirement modelを設計せよ。 **調査:** 過去障害が破った暗黙要求を抽出せよ。

### 知らないとする誤判断／次章への接続

「CSV exportを追加」が目的だと受け取り、本当の監査要求に不足する機能を作る。次章で機能要求と品質制約を分ける。

---

## 第4章　Functional / Non-functional Requirement

### この章を学ぶ理由／現場の問題

何をするかだけを仕様化すると、遅い・壊れやすい・使えない・監査不能なsystemでも合格する。quality attributeは具体的scenarioとして検証する。

### 中心概念と正式な定義

functional requirementは入力・状態・出力の観測可能な振舞い。non-functional/quality requirementは性能、可用性、保守性、安全性等の制約。quality attribute scenarioを source、stimulus、environment、artifact、response、response measure の六要素で表す。例：通常負荷で依頼を受け、APIが200ms p99以内に応答。

### 直感 → 図解 → 数式 → 例 → 実装

```text
function: transfer money
qualities: authorized, atomic, auditable, p99<300ms, RPO=0
```

可用性を \(A=MTBF/(MTBF+MTTR)\) と近似できる場合もあるが、利用者視点のgood events比の方が適切なことが多い。

```python
def acceptance(result):
    return result.correct and result.p99_ms < 200 and result.audit_complete
```

### よくある誤解／実務接続

- non-functionalは「後で足す」横断機能ではない。
- 99.9%のscope、窓、分母がなければ要求でない。
- quality attributesはtrade-offし、全て最大化できない。
- observabilityやdeployabilityも変更速度を左右する品質属性。

### 要点

1. 機能と品質を両方指定。 2. 品質はscenarioで書く。 3. response measureを定量化。 4. scopeと環境を含める。 5. trade-offをarchitectureへ反映。

### 誤解チェック（5問）

1. securityは一機能か。 2. 「高速」は検証可能か。 3. availabilityに分母は不要か。 4. 全qualityを最大化できるか。 5. maintainabilityは測れないか。

### 基礎問題（5問）

1. 機能要求を三つ書け。 2. 六要素scenarioを書け。 3. availability scopeを定義せよ。 4. trade-offを一つ示せ。 5. acceptance testへ写せ。

### 応用問題（3問）／設計問題／調査課題

1. securityとusabilityを調停せよ。 2. graceful degradation要求を書け。 3. modifiability scenarioを作れ。 **設計:** 認証serviceのquality attribute utility treeを作れ。 **調査:** 現行SLOと契約要求のgapを調べよ。

### 知らないとする誤判断／次章への接続

機能テスト通過だけでリリースし、ピーク負荷で契約を破る。次章では品質属性をsystem構造へ配分するarchitectureを扱う。

---

## 第5章　Software Architecture

### この章を学ぶ理由／現場の問題

architectureは箱図の美観でなく、重要な品質属性と変更制約を左右する高コストな構造判断である。採用技術名だけでは設計理由を検証できない。

### 中心概念と正式な定義

software architectureを、systemを構成するelements、それらのexternally visible properties、relationships、および進化を導くprinciplesの集合とする。viewは特定stakeholder関心に対する表現（module、component-and-connector、deployment等）。architectural decisionはcontext、options、forces、decision、consequencesを持つ。

### 直感 → 図解 → 数式 → 例 → 実装

```text
module view: ownership/dependencies
runtime view: calls/queues/failures
deployment view: processes/zones/data placement
```

modifiabilityの粗いriskを \(R(c)=P(failure|c)\times Impact(c)\) とし、依存fan-outやdata migrationで見積もる。

```yaml
decision: "single deployable with module boundaries"
forces: [team_size, transactionality, operability]
consequences: [simple deploy, shared failure domain]
```

### よくある誤解／実務接続

- microservicesはarchitectureの同義語でない。
- diagramだけでruntime failure、data ownership、decision rationaleは分からない。
- architectureは初期だけの活動でなくfitness functionで継続検証する。
- 分離にはnetwork、consistency、運用の代償がある。

### 要点

1. architectureは重要な構造判断。 2. 品質属性に駆動される。 3. 複数viewが必要。 4. rationale/consequenceを残す。 5. fitness functionで進化を制御。

### 誤解チェック（5問）

1. architecture=cloud製品一覧か。 2. microservicesなら疎結合か。 3. 一枚図で全関心を満たせるか。 4. decisionは永続不変か。 5. 分割は常に信頼性を上げるか。

### 基礎問題（5問）

1. 三viewを描け。 2. quality scenarioを構造へ割り当てよ。 3. ADRを書け。 4. failure domainを示せ。 5. fitness functionを一つ作れ。

### 応用問題（3問）／設計問題／調査課題

1. modular monolithとservicesを比較せよ。 2. data ownership trade-offを論ぜよ。 3. architecture driftを検出せよ。 **設計:** 多tenant SaaSのarchitecture viewsを設計せよ。 **調査:** 現systemの暗黙decisionを三つ復元せよ。

### 知らないとする誤判断／次章への接続

組織規模やtransaction境界を無視してservice分割し、変更を分散transactionへ変える。次章では変更を局所化するmodularityを扱う。

---

## 第6章　Modularity

### この章を学ぶ理由／現場の問題

一変更がsystem全体へ波及するか、少数moduleに閉じるかが長期速度を決める。module境界はファイル数でなく責務と情報隠蔽で定義する。

### 中心概念と正式な定義

moduleは明示interfaceを介して責務を提供し、設計決定を隠す単位。Parnasのinformation hidingでは、変化しそうなdesign decisionを各module内部へ封じる。dependency graph \(G=(V,E)\) で変更影響の到達集合 \(Reach(v)\) を小さくし、cycleを避ける。抽象不安定度原則などは判断補助であって目的でない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
bad: UI -> DB columns -> vendor API details
good: UI -> OrderPort <- Order module -> adapters
```

```python
class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
```

interfaceがvendor型を漏らせば、物理分割しても変更は局所化されない。

### よくある誤解／実務接続

- moduleを細かくするほどmodularとは限らない。
- shared utilityは変更fan-inの高い暗黙moduleになる。
- package-private boundaryだけでdata ownershipは守れない。
- module test、dependency rule、ownershipで境界を実行可能にする。

### 要点

1. moduleは変更決定を隠す。 2. interfaceで責務を公開。 3. 変更軸で分割。 4. cycleは独立進化を妨げる。 5. 境界をtoolで検証する。

### 誤解チェック（5問）

1. ファイル数=module数か。 2. 小moduleほど良いか。 3. interfaceがvendor型を返してよいか。 4. cycleは実行できれば問題なしか。 5. shared libraryは無料か。

### 基礎問題（5問）

1. 隠すdecisionを列挙せよ。 2. dependency graphを描け。 3. cycleを除け。 4. portを定義せよ。 5. public surfaceを縮めよ。

### 応用問題（3問）／設計問題／調査課題

1. change couplingを履歴から測れ。 2. shared kernelを分割せよ。 3. database境界をmodule化せよ。 **設計:** billing domainのmodule boundaryを設計せよ。 **調査:** repoの循環依存を検出せよ。

### 知らないとする誤判断／次章への接続

似た関数を同じutilityへ集約し、異なる変更理由を一つに結合する。次章でmodule内部のまとまりとmodule間依存を評価する。

---

## 第7章　Cohesion と Coupling

### この章を学ぶ理由／現場の問題

責務が散らばり依存が絡むsystemでは、変更理由とテスト範囲を予測できない。cohesion/couplingを構造と変更履歴の両方から見る。

### 中心概念と正式な定義

cohesionはmodule内要素が一つの責務・変更理由へ結びつく程度。couplingはmodule間が相手の知識や同時変更を必要とする程度。structural couplingだけでなく temporal、data/schema、semantic、operational couplingがある。履歴で \(P(change(B)|change(A))\) が高いのに別moduleなら境界不整合の仮説となる。

### 直感 → 図解 → 数式 → 例 → 実装

```text
high cohesion: [invoice calculate, invoice validate, invoice issue]
low cohesion : [date util, invoice SQL, auth retry, CSV]
```

```python
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Currency
```

primitive共有でsemantic couplingを隠すよりdomain型で契約を表す。

### よくある誤解／実務接続

- call数だけでcouplingは測れない。
- message queueは時間結合を弱めてもschema/semantic結合を残す。
- DRYで偶然似た処理を統合するとcohesionを下げ得る。
- deploy coupling、incident同時発生、git co-changeを観測する。

### 要点

1. cohesionは変更理由のまとまり。 2. couplingには多種類。 3. 非同期化で全結合は消えない。 4. 履歴が境界の証拠。 5. semantic契約を型とschemaへ出す。

### 誤解チェック（5問）

1. queueなら疎結合か。 2. callが少なければcoupling低いか。 3. DRYは常に良いか。 4. 同時deployはcoupling信号か。 5. cohesionは行数か。

### 基礎問題（5問）

1. coupling種別を分類せよ。 2. 低cohesion moduleを分けよ。 3. co-change表を読め。 4. primitive obsessionを修正せよ。 5. event contractを定義せよ。

### 応用問題（3問）／設計問題／調査課題

1. temporal couplingをprotocolへ変換せよ。 2. schema couplingをversioningせよ。 3. team couplingを分析せよ。 **設計:** order/payment間の契約を設計せよ。 **調査:** 過去6か月のco-change hotspotを調べよ。

### 知らないとする誤判断／次章への接続

queueを挟んだだけで独立serviceと呼び、順序・schema・同時rollout依存を隠す。次章では不要な詳細を隠すabstractionを扱う。

---

## 第8章　Abstraction

### この章を学ぶ理由／現場の問題

抽象化はコードを短くするためでなく、利用者が正しく考えるのに不要な詳細を隠し、成立する法則を提供する。誤った抽象は変更を難しくする。

### 中心概念と正式な定義

abstractionは具体状態集合 \(C\) から抽象状態 \(A\) への写像 \(\alpha:C\to A\) と、抽象操作が保持するobservable behavior。representation invariant \(I(c)\) と abstraction function により複数表現を同一値として扱う。漏れる抽象とは利用者が正しく使うため隠した詳細を恒常的に知る必要があるもの。

### 直感 → 図解 → 数式 → 例 → 実装

```text
caller sees: Money.add(Money) -> Money
hidden: decimal scale, rounding, storage representation
law: (a+b).currency == a.currency when currencies match
```

```python
class Percentage:
    def __init__(self, value):
        if not 0 <= value <= 1: raise ValueError
        self._value = Decimal(value)
```

境界でinvariantを作れば内部で再検証を繰り返さない。

### よくある誤解／実務接続

- wrapperを一枚増やすことは抽象化と限らない。
- 早すぎる一般化は異なる概念を一契約へ固定する。
- abstraction leakは完全排除でなく、頻度と費用を管理する。
- domain types、storage ports、scheduler、transaction boundaryに現れる。

### 要点

1. 抽象は詳細を隠し法則を公開。 2. invariantを境界で確立。 3. representationとmeaningを分ける。 4. 利用者の認知負荷で評価。 5. 実際の重複から一般化。

### 誤解チェック（5問）

1. interfaceがあれば抽象か。 2. 汎用parameterが多いほど良いか。 3. invariantは全methodで再検証すべきか。 4. leakは必ず失敗か。 5. domain概念をstringで十分表せるか。

### 基礎問題（5問）

1. abstraction functionを書け。 2. invariantを定義せよ。 3. 漏れる詳細を特定せよ。 4. stringをvalue objectへ変えよ。 5. 法則をproperty testにせよ。

### 応用問題（3問）／設計問題／調査課題

1. ORM leakを分析せよ。 2. cache abstractionの限界を書け。 3. 二つの似た概念を統合しない根拠を示せ。 **設計:** rate limit abstractionを設計せよ。 **調査:** repo内のboolean/string引数をdomain型候補として調べよ。

### 知らないとする誤判断／次章への接続

共通引数20個の万能clientを作り、各callerがprovider詳細を知る。次章では抽象が利用者へ現れるinterface契約を設計する。

---

## 第9章　Interface 設計

### この章を学ぶ理由／現場の問題

interfaceは変更の接点であり、公開した曖昧さは全利用者へ伝播する。正しい利用を容易に、無効状態を表現しにくくする。

### 中心概念と正式な定義

interface contractをprecondition \(P\)、postcondition \(Q\)、invariant \(I\)、failure semanticsの組とする。Hoare triple \(\{P\}\ op\ \{Q\}\)。Liskov substitutabilityはsubtypeがclientの証明を壊さず置換可能であること、すなわちpreconditionを強めずpostconditionを弱めない等。command/query、ownership、idempotency、concurrencyも契約に含める。

### 直感 → 図解 → 数式 → 例 → 実装

```text
caller -- valid request --> interface -- result | typed failure --> caller
         ownership/time/retry semantics belong to contract
```

```python
Result = Success[Order] | NotFound | VersionConflict
def update(cmd: UpdateOrder, expected_version: int) -> Result: ...
```

boolean `False` より失敗型が再試行・利用者エラー・競合を区別する。

### よくある誤解／実務接続

- method数を減らすだけでsimple interfaceにはならない。
- nullableは absent/error/not-loaded を混ぜやすい。
- 呼出し順序制約はtypestate等で表すか明示する。
- internal interfaceも組織・test・移行の境界になり得る。

### 要点

1. 契約は成功だけでなく失敗を含む。 2. invariantを型で表現。 3. ownershipとlifetimeを明示。 4. substitutabilityを守る。 5. evolution/compatibilityを計画。

### 誤解チェック（5問）

1. interfaceはsignatureだけか。 2. nullable一つで全不在理由を表せるか。 3. subtypeはpreconditionを強めてよいか。 4. retry semanticsはcallerだけの責任か。 5. 内部APIはversion不要か。

### 基礎問題（5問）

1. pre/postconditionを書け。 2. failure unionを設計せよ。 3. nullableを分解せよ。 4. LSP違反を修正せよ。 5. ownershipを明記せよ。

### 応用問題（3問）／設計問題／調査課題

1. typestate upload APIを設計せよ。 2. streaming backpressure契約を述べよ。 3. cancellation semanticsを設計せよ。 **設計:** inventory reservation interfaceを設計せよ。 **調査:** 一つの内部interfaceの暗黙契約を抽出せよ。

### 知らないとする誤判断／次章への接続

失敗を例外一種へ潰し、callerが文字列でretry可否を判定する。次章ではnetwork越しの公開契約としてAPIを扱う。

---

## 第10章　API Design

### この章を学ぶ理由／現場の問題

network APIは独立配備、部分障害、重複、遅延、互換性を持つinterfaceである。ローカル関数の感覚で設計すると二重実行や移行不能を招く。

### 中心概念と正式な定義

API contractはresource/operation、schema、invariants、authentication/authorization、error taxonomy、idempotency、ordering、pagination、rate limit、version/evolutionから成る。操作 f がidempotentとは \(f(f(s,x),x)=f(s,x)\)。ただし同じresponseや副作用ゼロまで自動保証しない。at-least-once delivery下ではdeduplication identityとatomic effect記録が必要。

### 直感 → 図解 → 数式 → 例 → 実装

```text
client --request k--> server commits --response lost--X
client --retry k----> server must return same logical operation
```

```python
def create_payment(cmd, key):
    return transaction(lambda: get_or_create_by_key(key, lambda: charge(cmd)))
```

pagination tokenはoffset詳細でなくsnapshot/order semanticsを表すopaque cursorにする。

### よくある誤解／実務接続

- HTTP method名だけでbackend副作用はidempotentにならない。
- version追加はcompatibility strategyの代替でない。
- error code 200内の失敗はmiddleware/monitoringを壊す。
- webhook、async job、streamもdeliveryとordering契約を持つ。

### 要点

1. APIは分散契約。 2. retryを正常系に含める。 3. idempotency identityを設計。 4. schema evolutionをadditiveに計画。 5. errors/limits/orderを明記。

### 誤解チェック（5問）

1. POSTは必ず非idempotentか。 2. keyがあればatomicか。 3. timeoutは失敗確定か。 4. offset paginationは変更中も安定か。 5. v2を作れば移行完了か。

### 基礎問題（5問）

1. error taxonomyを作れ。 2. retry sequenceを描け。 3. idempotency invariantを書け。 4. cursor contractを定義せよ。 5. additive schema changeを示せ。

### 応用問題（3問）／設計問題／調査課題

1. webhook deduplicationを設計せよ。 2. partial success batch APIを定義せよ。 3. rate-limit fairnessを論ぜよ。 **設計:** payment APIの完全contractを設計せよ。 **調査:** 現APIのtimeout後状態確認方法を監査せよ。

### 知らないとする誤判断／次章への接続

timeoutを未実行とみなし無条件retryして二重課金する。次章では繰り返し現れる設計問題からpatternを選ぶ。

---

## 総合演習A（第1〜10章）

1. CSV輸出要求をgoalへ戻し、機能・品質scenario、architecture views、module、interface、API contractまでtraceせよ。
2. payment service分割案を、変更軸、transaction、idempotency、failure domain、team ownership、移行・廃止でレビューせよ。
3. shared utility hotspotをgit co-changeとdependency graphから再設計し、消す抽象と残すdomain typeを説明せよ。

---

## 第11章　Design Pattern：暗記ではなく力の均衡

### この章を学ぶ理由／現場の問題

pattern名から実装を始めると、問題のない場所へindirectionを増やす。patternは繰り返すcontext、conflicting forces、構造、consequencesを共有する語彙である。

### 中心概念と正式な定義

design patternを \((context,problem,forces,solution,consequences)\) の再利用可能な設計知識とする。Strategyは変化するalgorithmを交換可能な契約へ、Observerはone-to-many通知を、Adapterは異なるinterfaceを変換する。これらはコードtemplateでなく、結合の位置を変える。選択は予想ではなく既に観測されたvariation pointに基づく。

### 直感 → 図解 → 数式 → 例 → 実装

```text
context: tax rules vary by jurisdiction
force: stable checkout, changing rules
solution: Checkout -> TaxPolicy interface <- rule implementations
cost: more indirection/configuration/testing
```

```python
class TaxPolicy(Protocol):
    def calculate(self, order: Order) -> Money: ...
```

### よくある誤解／実務接続

- pattern数は設計品質でない。
- Factoryでconstructorを隠すだけなら価値がない場合がある。
- Singletonはglobal lifetime/dependencyという高い代償を持つ。
- language機能がpatternを不要・簡素にすることもある。

### 要点

1. contextとforcesを先に書く。 2. solutionには代償がある。 3. variationが観測されてから抽象化。 4. pattern名より契約が重要。 5. 不要なら直接実装する。

### 誤解チェック（5問）

1. patternは必須か。 2. Singletonは共有状態の問題を解くか。 3. Factoryは常に疎結合か。 4. 同名patternは同実装か。 5. 将来予測だけでStrategyを置くべきか。

### 基礎問題（5問）

1. patternの五要素を書け。 2. Strategy候補を示せ。 3. Adapter境界を描け。 4. Observerのfailureを列挙せよ。 5. patternを消して単純化せよ。

### 応用問題（3問）／設計問題／調査課題

1. event busとObserverを比較せよ。 2. decorator順序問題を分析せよ。 3. language機能でpatternを置換せよ。 **設計:** tax variationを最小の抽象で設計せよ。 **調査:** repoのpattern名classがforcesを満たすか監査せよ。

### 知らないとする誤判断／次章への接続

「Factory/Repositoryを入れたからarchitectureが良い」と、変化軸やfailure semanticsを検証しない。次章で振舞いの証拠を作るtestingへ進む。

---

## 第12章　Testing：unit・integration・system・acceptance

### この章を学ぶ理由／現場の問題

testはbugがない証明でなく、選んだ仮説を反証する実験である。levelを実装単位名でなく、観測境界とリスクで選ぶ。

### 中心概念と正式な定義

test caseはprecondition、stimulus、oracle、expected observationを持つ。unit testは狭い設計単位を隔離して検査、integrationはcomponent間契約、systemは配備可能system全体、acceptanceはstakeholder要求充足の証拠。coverage \(C=executed\ elements/total\ elements\) は未実行の発見指標で、correctness確率でない。test pyramidは費用feedback分布のheuristic。

### 直感 → 図解 → 数式 → 例 → 実装

```text
many fast contract/unit checks
fewer integration checks
few critical journey/system/acceptance checks
plus static analysis and production observation
```

```python
def test_transfer_preserves_total():
    before = a.balance + b.balance
    transfer(a, b, Money(10))
    assert a.balance + b.balance == before
```

propertyは例より広い入力空間を表すが、generatorとoracleの欠陥は残る。

### よくある誤解／実務接続

- 100% coverageでもassertion不足なら無意味。
- mockを増やすと実装詳細へcoupleしrefactorを妨げる。
- flaky testは単なる迷惑でなく信号の信頼性を壊す欠陥。
- production canaryとmonitoringも検証層だが事前testの代替ではない。

### 要点

1. testは反証可能な実験。 2. levelは観測境界で選ぶ。 3. riskに応じてportfolio化。 4. coverageは十分条件でない。 5. flaky原因を除く。

### 誤解チェック（5問）

1. coverage100%=正しいか。 2. unitはclass一つか。 3. mockが多いほど隔離が良いか。 4. acceptanceはUIだけか。 5. flakyをretryで隠してよいか。

### 基礎問題（5問）

1. 四levelを分類せよ。 2. oracleを書け。 3. boundary caseを列挙せよ。 4. propertyを一つ書け。 5. coverage gapを分析せよ。

### 応用問題（3問）／設計問題／調査課題

1. mutation testingを説明せよ。 2. contract testの限界を述べよ。 3. nondeterministic testを再設計せよ。 **設計:** payment changeのtest portfolioを設計せよ。 **調査:** flaky上位testの根本原因を分類せよ。

### 知らないとする誤判断／次章への接続

coverage目標達成のためassertionの弱いtestを量産し、安全だと判断する。次章では仕様への適合と目的への妥当性を分ける。

---

## 第13章　Verification と Validation

### この章を学ぶ理由／現場の問題

仕様どおりでも、仕様が利用者課題を誤っていれば失敗する。「正しく作ったか」と「正しいものを作ったか」の証拠を分離する。

### 中心概念と正式な定義

verificationは成果物が指定requirements/designを満たすか、validationは意図した利用・stakeholder needを満たすか。形式検証はモデル \(M\) とproperty \(\varphi\) に対し \(M\models\varphi\) を証明/検査するが、モデル妥当性は別。assurance caseはclaim--argument--evidenceの構造で保証を説明する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
need --validation--> requirement --verification--> implementation
 ^ model/use evidence                         test/proof evidence
```

```yaml
claim: "duplicate charge is prevented"
argument: "idempotency key and atomic uniqueness"
evidence: [model_check, integration_test, production_metric]
```

### よくある誤解／実務接続

- test通過はvalidationを自動保証しない。
- formal proofは仮定・model・compiler/hardwareの境界を持つ。
- acceptance testは両側を橋渡しするが利用調査を置換しない。
- safety/securityではevidenceの独立性とtraceabilityが重要。

### 要点

1. verificationとvalidationを分ける。 2. 証拠の対象を明示。 3. model assumptionを管理。 4. claim-argument-evidenceで保証。 5. 利用後feedbackもvalidation。

### 誤解チェック（5問）

1. spec適合なら価値があるか。 2. proofなら実装も無条件に正しいか。 3. validationはQAだけか。 4. usability testはverificationか。 5. evidence一種で十分か。

### 基礎問題（5問）

1. 五活動をV/Vへ分類せよ。 2. assurance claimを書け。 3. assumptionを列挙せよ。 4. traceを作れ。 5. 誤った仕様例を分析せよ。

### 応用問題（3問）／設計問題／調査課題

1. model-implementation gapを論ぜよ。 2. safety caseを簡略作成せよ。 3. independent evidenceを選べ。 **設計:** duplicate charge保証caseを設計せよ。 **調査:** 障害がverification/validationのどちらを破ったか調べよ。

### 知らないとする誤判断／次章への接続

acceptance criteriaを満たしたため、誰も使わない機能を成功とする。次章では証拠を得やすくするtestabilityを設計する。

---

## 第14章　Testability

### この章を学ぶ理由／現場の問題

test困難はtest codeの技巧不足でなく、観測不能・制御不能・非決定的依存を持つ設計の症状である。system境界を設計し直す。

### 中心概念と正式な定義

testabilityは故障を効率よく刺激・観測・隔離できる程度。controllabilityは入力・状態・依存を設定可能、observabilityは出力・内部効果を意味ある形で観測可能、isolationは対象外変動を制御可能、determinismは同条件の再現性。テスト専用分岐よりclock、randomness、I/Oを明示dependencyにする。

### 直感 → 図解 → 数式 → 例 → 実装

```text
hidden now/random/network -> nondeterministic behavior
explicit Clock/RNG/Port   -> controllable scenario + observable result
```

```python
def expire(session, now: datetime):
    return session.expires_at <= now
```

### よくある誤解／実務接続

- dependency injection frameworkは必須でない。値/関数引数で十分なことが多い。
- private methodを直接testする前に公開behaviorと責務を見直す。
- productionと異なるtest-only pathはconfidenceを下げる。
- trace ID、domain event、health signalもtestabilityを上げる。

### 要点

1. 制御・観測可能性を設計。 2. 非決定性を依存として明示。 3. production pathをtest。 4. 責務分離がisolationを作る。 5. 診断可能性もtestability。

### 誤解チェック（5問）

1. test-only flagは良い設計か。 2. DI containerは必須か。 3. private methodを全てtestすべきか。 4. clockはglobalでよいか。 5. observableとはlogが多いことか。

### 基礎問題（5問）

1. hidden dependencyを探せ。 2. clockを注入せよ。 3. RNGを固定せよ。 4. domain resultを観測可能にせよ。 5. flaky causeを除け。

### 応用問題（3問）／設計問題／調査課題

1. distributed testabilityを設計せよ。 2. fault injection pointを置け。 3. deterministic schedulerの価値を論ぜよ。 **設計:** retry componentを完全にtestableに設計せよ。 **調査:** test-only production分岐を監査せよ。

### 知らないとする誤判断／次章への接続

テストで失敗するためsleepとretryを足し、raceの根を残す。次章では変更履歴と並行作業を支えるversion controlの意味を学ぶ。

---

## 第15章　Version Control の理論的意味

### この章を学ぶ理由／現場の問題

VCSはbackupや共同編集GUIでなく、system状態のimmutable snapshotと変更関係を記録し、並行する仮説を統合・監査・復元する基盤である。

### 中心概念と正式な定義

commitをtree snapshot、metadata、parent commitへの参照を持つnodeとし、historyをDAG \(G=(V,E)\) とする。branchはcommitへの可動参照。mergeは二親を持つ統合snapshotで、text conflictがなくてもsemantic conflictはあり得る。commitはatomicな意味単位としてbuild/test可能にする。

### 直感 → 図解 → 数式 → 例 → 実装

```text
A---B---C  main
     \---D---E feature
          \---M merge (parents C,E)
```

```sh
git show --stat <commit>
git bisect start
```

history rewriteは共有済み参照のidentityを変えるため、協調契約として扱う。

### よくある誤解／実務接続

- merge成功は意味統合成功でない。
- 大commitはreview、bisect、revertの単位を壊す。
- commit messageは差分のwhatでなくwhy/constraintを補う。
- generated artifact、schema、configのversion整合も重要。

### 要点

1. commitはsnapshot node。 2. historyはDAG。 3. branchは参照。 4. semantic conflictをtestする。 5. atomic historyが復旧と学習を助ける。

### 誤解チェック（5問）

1. Gitは差分だけ保存する概念か。 2. conflictなし=安全か。 3. squashは常に良いか。 4. revert=履歴削除か。 5. commit messageにコード説明だけで十分か。

### 基礎問題（5問）

1. DAGを描け。 2. merge baseを特定せよ。 3. semantic conflictを例示せよ。 4. atomic commitへ分けよ。 5. revertを説明せよ。

### 応用問題（3問）／設計問題／調査課題

1. monorepo atomicityを論ぜよ。 2. schema/code commit順序を設計せよ。 3. bisect可能性を改善せよ。 **設計:** trunk-based integration policyを設計せよ。 **調査:** 最近のrevert困難commitを分析せよ。

### 知らないとする誤判断／次章への接続

一週間分を一commitにし、失敗時に安全な部分だけ戻せない。次章ではversion対象をコード外の構成へ広げる。

---

## 第16章　Configuration Management

### この章を学ぶ理由／現場の問題

同じcommitでもdependency、flag、secret、infrastructure、data schemaが違えば別systemである。再現可能な構成identityと変更統制が必要。

### 中心概念と正式な定義

configuration item (CI)はversionと変更管理の対象。system configurationを \(S=(code,deps,config,infrastructure,schema,data assumptions)\) とする。baselineは承認されたCI集合、buildはsourceとtoolchainからartifactへの可能な限り再現可能な関数 \(A=B(S,E)\)。desired stateとobserved stateのdriftを検出する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
commit + lockfile + build image + IaC + runtime config + schema -> release identity
```

```yaml
release:
  image_digest: sha256:...
  config_version: 42
  schema_version: 108
  flags: snapshot-2026-08-27
```

### よくある誤解／実務接続

- environment別手修正は構成を再現不能にする。
- secret値をGitへ入れず、secret参照とrotation policyはversion管理する。
- lockfileだけでOS/toolchainまで再現されない。
- feature flagもownership、期限、auditを持つCI。

### 要点

1. 実行systemはcode以上。 2. CIとbaselineを定義。 3. immutable artifactを昇格。 4. driftを検出。 5. release identityを追跡可能にする。

### 誤解チェック（5問）

1. 同commitなら同systemか。 2. secretをGitへ置くべきか。 3. environmentで再buildしてよいか。 4. flagは一時的だから管理不要か。 5. lockfileだけで完全再現か。

### 基礎問題（5問）

1. CIを列挙せよ。 2. baselineを作れ。 3. artifact identityを定義せよ。 4. driftを例示せよ。 5. flag metadataを設計せよ。

### 応用問題（3問）／設計問題／調査課題

1. hermetic buildの境界を論ぜよ。 2. schema compatibilityを構成へ入れよ。 3. secret rotationを無停止化せよ。 **設計:** release manifestを設計せよ。 **調査:** 本番構成を一commitから再現できるか監査せよ。

### 知らないとする誤判断／次章への接続

本番だけconsoleで修正し、次deployで上書きまたは再現不能にする。次章では構成を反復可能に検証・配備するCI/CDを扱う。

---

## 第17章　CI/CD

### この章を学ぶ理由／現場の問題

CI/CDはserver製品名でなく、小さな変更を頻繁に統合し、自動証拠を得て、安全に価値へ到達させるfeedback disciplineである。

### 中心概念と正式な定義

Continuous Integrationはmainlineへ頻繁に統合し、各変更を自動build/testする実践。Continuous Deliveryは任意時点で本番配備可能、Continuous Deploymentは合格変更を自動本番配備。pipelineはartifactを再buildせず段階間でpromoteし、quality gateは明示policy。lead time、deployment frequency、change failure rate、recovery timeはsystem-level outcome指標。

### 直感 → 図解 → 数式 → 例 → 実装

```text
commit -> fast checks -> artifact -> deeper checks -> staged deploy -> observe
            < minutes feedback >             < automated rollback/stop >
```

```yaml
stages: [lint, unit, contract, build-once, security, canary, promote]
on_canary_slo_violation: stop_and_rollback
```

### よくある誤解／実務接続

- pipeline追加は自動的にdeliveryを速くしない。queueとflakeが遅延を作る。
- 全E2Eを先に実行するとfeedbackが遅い。
- manual approvalはrisk controlになる場合と儀式になる場合を測る。
- rollback不能なdata changeにはforward recoveryとexpand/contractが必要。

### 要点

1. CIは頻繁な統合。 2. delivery/deploymentを分ける。 3. build once, promote。 4. fast feedback順に配置。 5. 配備後観測までpipeline。

### 誤解チェック（5問）

1. Jenkinsを使えばCIか。 2. CDのDは一義か。 3. stageごとにbuildしてよいか。 4. manual gateは必ず安全か。 5. deploy成功=変更成功か。

### 基礎問題（5問）

1. checkを順序づけよ。 2. delivery/deploymentを定義せよ。 3. artifact promotionを書け。 4. canary stop条件を作れ。 5. flaky costを算出せよ。

### 応用問題（3問）／設計問題／調査課題

1. pipeline queueを待ち行列として分析せよ。 2. progressive deliveryを設計せよ。 3. DB migration rollbackを論ぜよ。 **設計:** 10分feedback/安全配備pipelineを設計せよ。 **調査:** CI時間のcritical pathを測れ。

### 知らないとする誤判断／次章への接続

checksを無限に直列追加し、開発者がbatchを大きくして統合頻度を下げる。次章では人間による設計・知識共有の検査を扱う。

---

## 第18章　Code Review

### この章を学ぶ理由／現場の問題

reviewは誤字探しや承認儀式でなく、変更リスクの発見、設計整合、知識伝播、ownership確認の場。大きすぎる差分と不明な目的が効果を下げる。

### 中心概念と正式な定義

change proposalはcontext、intent、risk、evidence、rollout/rollbackを含む。review latency \(T_r=queue+active+rework\)。defect detectionだけでなく knowledge distribution と design governance を目的関数に含める。author/reviewer間の情報非対称を、small coherent changeと自動checkで下げる。

### 直感 → 図解 → 数式 → 例 → 実装

```text
proposal intent -> automated evidence -> human review of design/risk
comments: blocking correctness | question | suggestion | note
```

```markdown
Why / Scope / Invariants / Alternatives / Tests / Rollout / Rollback
```

### よくある誤解／実務接続

- LGTM数は品質尺度でない。
- styleはformatterへ移し、人は意味とriskへ集中。
- reviewer追加は責任分散でなくqueueを増やす場合がある。
- harshnessは精度ではなく、質問と根拠で共同設計する。

### 要点

1. intentとriskを先に示す。 2. 小さく意味あるdiff。 3. 自動化可能事項をtoolへ。 4. comment severityを明示。 5. latencyとknowledge spreadを測る。

### 誤解チェック（5問）

1. reviewerが多いほど安全か。 2. style commentは人がすべきか。 3. approveは責任移転か。 4. 大diffでも丁寧なら同等か。 5. reviewは教育だけか。

### 基礎問題（5問）

1. PR説明を書け。 2. commentを分類せよ。 3. diffを分割せよ。 4. risk checklistを作れ。 5. review latencyを分解せよ。

### 応用問題（3問）／設計問題／調査課題

1. ownership bottleneckを解け。 2. stack reviewを設計せよ。 3. AI reviewの保証境界を論ぜよ。 **設計:** high-risk migration review protocolを設計せよ。 **調査:** review待ち時間と差分量の関係を測れ。

### 知らないとする誤判断／次章への接続

大量diffを複数人へ投げ、誰かが全体を理解したと仮定する。次章では振舞いを保って内部構造を変えるrefactoringを扱う。

---

## 第19章　Refactoring

### この章を学ぶ理由／現場の問題

機能追加と構造改善を混ぜると原因切り分けとreviewが難しい。refactoringを観測可能な振舞いを保持する意味保存変換として行う。

### 中心概念と正式な定義

外部観測集合 O に対し、program PからP'へのrefactoringは \(\forall x\in domain, Obs(P,x)=Obs(P',x)\) を意図する変換。何を観測に含むか（output、error、timing、resource、API、audit）が契約依存。characterization testsは既存behaviorを捕捉し、small stepsとVCSで検証する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
green tests -> one structural step -> green -> commit -> repeat
feature change is a separate semantic delta
```

```python
# before duplicated pricing branches
# after PricePolicy with the same golden/property observations
```

### よくある誤解／実務接続

- 名前変更でもpublic schema/telemetryが変われば外部behaviorになり得る。
- test不足を理由に永久停止せず、characterization seamを作る。
- 大rewriteをrefactorと呼ばない。
- performanceも要求ならbehavior preservation対象。

### 要点

1. 意味保存変換。 2. observation boundaryを定義。 3. small verified steps。 4. feature deltaと分ける。 5. 不要codeを最終的に削除。

### 誤解チェック（5問）

1. compileすれば振舞い保持か。 2. performanceは常に対象外か。 3. rewrite=refactorか。 4. testなしなら不可能か。 5. 旧pathを残すのが安全か。

### 基礎問題（5問）

1. observationを列挙せよ。 2. extract functionを検証せよ。 3. characterization testを書け。 4. feature/refactorを分けよ。 5. dead codeを削除せよ。

### 応用問題（3問）／設計問題／調査課題

1. schema refactoringをexpand/contractせよ。 2. concurrent systemの意味保存を論ぜよ。 3. compiler-assisted refactorを評価せよ。 **設計:** legacy pricingの段階refactorを設計せよ。 **調査:** 過去rewriteの失敗要因を分類せよ。

### 知らないとする誤判断／次章への接続

新旧実装を無期限に併存させ「安全」とし、二重保守と挙動差を増やす。次章では将来変更費用を負債として管理する。

---

## 第20章　Technical Debt

### この章を学ぶ理由／現場の問題

「汚いコード」を一括して負債と呼ぶと優先順位が作れない。短期価値のため将来変更費用を増やす意思決定と、その利息を具体化する。

### 中心概念と正式な定義

technical debt itemを、現在選んだ設計と望ましい設計の差、principal（是正費）、interest（その差が各変更へ加える反復費）、risk（障害確率×影響）で記述する。優先度は美観でなく期待費用 \(E[cost]=P(touched)\times interest + risk\) と戦略適合で決める。意図的/非意図的、慎重/無謀を区別する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
shortcut now saves 2 weeks
each monthly change costs +2 days; migration risk grows
break-even and risk determine repayment, not shame
```

```yaml
debt: "shared customer schema"
interest_evidence: "8 coordinated releases/quarter"
principal: "6 engineer-weeks"
trigger: "second independent product team"
```

### よくある誤解／実務接続

- 古いcodeは自動的にdebtでない。
- TODO数やlint違反だけでbusiness costは分からない。
- 全返済を先にするのも、永遠に延期するのも不合理。
- debt registerはowner、evidence、trigger、retirementを持つ。

### 要点

1. debtは将来変更費増加。 2. principal/interest/riskを分ける。 3. 証拠で優先順位化。 4. triggerを設定。 5. 返済後旧構造を削除。

### 誤解チェック（5問）

1. 古い=debtか。 2. code smell=business priorityか。 3. 全debt返済が最適か。 4. 意図的debtは悪か。 5. ownerなしregisterは機能するか。

### 基礎問題（5問）

1. debt itemを書け。 2. principalを見積もれ。 3. interest evidenceを探せ。 4. triggerを定義せよ。 5. 三項目を優先順位化せよ。

### 応用問題（3問）／設計問題／調査課題

1. portfolioとしてdebtを最適化せよ。 2. platform投資の利息削減を測れ。 3. architecture debtを分析せよ。 **設計:** quarterly debt reviewを設計せよ。 **調査:** high-churn hotspotの変更利息を算出せよ。

### 知らないとする誤判断／次章への接続

不快なcodeを先に書き直し、頻繁な配備障害を生む高利息の構成負債を放置する。次章では内部状態を推論可能にするobservabilityを扱う。

---

## 総合演習B（第11〜20章）

1. flaky E2E suiteにretryを足す提案を、testability、observability、CI feedback、technical debtの根本原因から再設計せよ。
2. 大規模pricing rewriteを、characterization、pattern選択、small steps、review、artifact/config versionまで分割せよ。
3. 「coverage 95%」という保証claimをassurance caseへ変え、不足するevidenceを列挙せよ。

---

## 第21章　Observability

### この章を学ぶ理由／現場の問題

dashboard数を増やすのでなく、未知の問いに外部出力から答え、変更の成否と障害原因を絞り込めるsystemを作る。

### 中心概念と正式な定義

制御理論的には内部状態が出力系列から識別可能な性質。softwareでは logs、metrics、traces、profiles、domain events を相関可能なcontextで生成し、system状態を探索できる能力。signalは目的・owner・保持・cardinality costを持つ。SLIはuser outcome、diagnostic telemetryは原因探索用として分ける。

### 直感 → 図解 → 数式 → 例 → 実装

```text
user request -> trace id -> service spans -> logs/events -> SLI outcome
                        high-cardinality dimensions under controlled cost
```

```python
with span("reserve_inventory", order_id=order.id) as s:
    result = reserve(order)
    s.set_attribute("outcome", result.kind)
```

### よくある誤解／実務接続

- log量=observabilityでない。semantic contextとqueryabilityが要る。
- high cardinalityを全面禁止すると個別traceを失う。保管層を選ぶ。
- PII/secretをtelemetryへ出さない。
- alertは症状・actionability中心、dashboardは所有者とrunbookへ結ぶ。

### 要点

1. 未知の問いに答える能力。 2. outcomeとdiagnosticを分ける。 3. 相関contextを伝播。 4. cardinality/privacy/costを設計。 5. instrumentationを契約としてtest。

### 誤解チェック（5問）

1. 三本柱を導入すればobservableか。 2. logが多いほどよいか。 3. trace idだけで因果順序が分かるか。 4. alertは全異常へ必要か。 5. telemetryにschemaは不要か。

### 基礎問題（5問）

1. user outcome SLIを書け。 2. trace属性を選べ。 3. cardinalityを見積もれ。 4. PIIを除け。 5. alert ownerを定義せよ。

### 応用問題（3問）／設計問題／調査課題

1. sampling下traceを設計せよ。 2. baggage伝播riskを論ぜよ。 3. telemetry schema evolutionを設計せよ。 **設計:** checkoutのobservability contractを設計せよ。 **調査:** 一障害を現telemetryだけで再構成できるか試せ。

### 知らないとする誤判断／次章への接続

CPU dashboardを増やす一方、どのuser operationが失敗したか追えない。次章では観測を使いincidentへの組織的応答を設計する。

---

## 第22章　Incident Management

### この章を学ぶ理由／現場の問題

incident時は情報不足と時間圧力が強い。英雄的な個人対応でなく、役割、通信、意思決定、復旧、学習を再現可能にする。

### 中心概念と正式な定義

incidentはservice objectiveまたは安全な運用を実質的に脅かす事象。response lifecycleは detect、triage、stabilize、diagnose、recover、verify、learn。incident commanderは全修正を行う人でなく、優先順位とcoordinationを所有。severityは原因でなくuser impact、scope、duration、safetyで分類。timelineは事実・時刻・判断・仮説を分ける。

### 直感 → 図解 → 数式 → 例 → 実装

```text
signal -> declare -> roles/channel -> mitigate -> verify user outcome
                                     -> root/contributing conditions -> actions
```

```yaml
roles: [incident_commander, operations, communications, scribe]
update: {impact, current_hypothesis, action, owner, next_update_at}
```

### よくある誤解／実務接続

- 原因特定前の安全なmitigationは敗北でない。
- 「root cause一つ」で社会技術的条件を潰さない。
- blamelessは責任不在でなく、処罰恐怖なしに構造を調べる。
- action itemはowner、期限、検証可能な期待risk reductionを持つ。

### 要点

1. user impactで宣言。 2. rolesと通信を分離。 3. mitigationを優先。 4. timelineを証拠化。 5. 学習をsystem changeへ閉じる。

### 誤解チェック（5問）

1. 最も詳しい人が必ずICか。 2. root causeは常に一つか。 3. rollbackは原因判明後か。 4. blameless=無責任か。 5. postmortem作成で完了か。

### 基礎問題（5問）

1. severityを分類せよ。 2. rolesを割り当てよ。 3. status updateを書け。 4. timelineを作れ。 5. actionを検証可能にせよ。

### 応用問題（3問）／設計問題／調査課題

1. concurrent incidentsを統合判断せよ。 2. vendor outage対応を設計せよ。 3. near miss学習を論ぜよ。 **設計:** incident command protocolを設計せよ。 **調査:** 過去action itemの完了とrisk reductionを追跡せよ。

### 知らないとする誤判断／次章への接続

操作した個人を原因とし、危険な権限・手順・検証不足を残す。次章では障害を前提に信頼性を定量・設計する。

---

## 第23章　Reliability

### この章を学ぶ理由／現場の問題

reliabilityは「落ちない努力」でなく、定義した環境・期間で意図した機能を継続する確率・能力。冗長化だけでは共通原因と運用複雑性を増やす。

### 中心概念と正式な定義

reliability function \(R(t)=P(T>t)\)、availabilityは稼働可能時間割合。直列独立componentは \(R_s=\prod_iR_i\)、並列冗長は \(R_p=1-\prod_i(1-R_i)\) だが独立性仮定が重要。faultは潜在原因、errorは不正内部状態、failureは外部service逸脱。resilienceは故障下で許容serviceを維持・回復する能力。

### 直感 → 図解 → 数式 → 例 → 実装

```text
fault -> error state -> externally visible failure
prevent | detect/isolate | tolerate/degrade/recover
```

```python
def call_with_budget(op, deadline, retry_policy, breaker):
    # retryは成功率だけでなく負荷とdeadlineを消費する
    ...
```

### よくある誤解／実務接続

- availabilityとreliabilityは同じでない。
- retryは独立成功確率でなく相関障害・増幅を考える。
- redundancyが同電源・同regionなら共通原因に弱い。
- error budgetでfeature velocityとriskを運用的に結ぶ。

### 要点

1. failureを外部契約で定義。 2. fault/error/failureを分ける。 3. 独立性仮定を疑う。 4. degrade/recoverを設計。 5. reliabilityを継続測定。

### 誤解チェック（5問）

1. 99.9% availability=同reliabilityか。 2. replica追加で必ず改善か。 3. retryは無料か。 4. fault=incidentか。 5. zero failureが唯一目標か。

### 基礎問題（5問）

1. 直列reliabilityを計算せよ。 2. 独立並列を計算せよ。 3. 共通原因を列挙せよ。 4. failure contractを書け。 5. degradation modeを設計せよ。

### 応用問題（3問）／設計問題／調査課題

1. retry stormをモデル化せよ。 2. chaos experiment仮説を書け。 3. error budget policyを設計せよ。 **設計:** dependency failure下checkoutを設計せよ。 **調査:** 現冗長性のfailure domainを監査せよ。

### 知らないとする誤判断／次章への接続

replica数だけを増やし、共通schema migrationで全台を同時停止する。次章では稼働後の変更を主活動とするmaintenanceを扱う。

---

## 第24章　Maintenance

### この章を学ぶ理由／現場の問題

maintenanceを「古いものの世話」とみなすと予算・人材・設計が軽視される。実際は環境と要求へ適応しsystem価値を維持する継続engineeringである。

### 中心概念と正式な定義

maintenanceを corrective（欠陥修正）、adaptive（環境変化）、perfective（価値/性能改善）、preventive（将来risk低減）に分類する。maintainabilityは意図した変更を効果的・効率的に行える程度。change requestの lead time \(T=understand+modify+verify+coordinate+deploy\) を分解し、hotspotとknowledge concentrationを管理する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
operational feedback -> change -> new baseline
dependencies/regulations/traffic evolve even if business features stop
```

```yaml
maintenance_item:
  category: adaptive
  trigger: "runtime EOL"
  evidence: "unsupported after date"
  migration_and_removal: true
```

### よくある誤解／実務接続

- correctiveだけがmaintenanceでない。
- rewriteはmaintenance費を自動リセットしない。
- owner不在componentは止まっていてもriskが増える。
- dependency upgradeを定常flowとして小batch化する。

### 要点

1. maintenanceは進化活動。 2. 四分類で目的を分ける。 3. lead timeを構成要素化。 4. ownershipと知識を分散。 5. removalも完了条件。

### 誤解チェック（5問）

1. 新機能以外は雑務か。 2. upgradeは価値ゼロか。 3. rewriteで全問題が消えるか。 4. 動いている依存は安全か。 5. deprecationは削除なしで完了か。

### 基礎問題（5問）

1. 作業を四分類せよ。 2. lead timeを分解せよ。 3. hotspotを特定せよ。 4. EOL計画を書け。 5. ownership gapを探せ。

### 応用問題（3問）／設計問題／調査課題

1. upgrade treadmillを自動化せよ。 2. maintainability fitness functionを作れ。 3. knowledge riskを測れ。 **設計:** 年間maintenance capacityを設計せよ。 **調査:** unsupported dependencyとownerを一覧化せよ。

### 知らないとする誤判断／次章への接続

新機能率だけでteamを評価し、依存EOL対応を先送りして緊急移行にする。次章では高制約の既存systemを価値とriskの両面から扱う。

---

## 第25章　Legacy System

### この章を学ぶ理由／現場の問題

legacyを年齢や技術名で判断すると、重要business knowledgeを捨てるrewriteか、恐怖による凍結の二択になる。変更困難性の具体原因を分離する。

### 中心概念と正式な定義

legacy systemを、価値を提供し続ける一方、理解・変更・検証・配備に高い制約/riskを持つsystemとする。制約を knowledge、testability、architecture、data、dependency、deployment、organization に分類。strangler、branch by abstraction、parallel run、expand/contract等でseamを作り、置換単位ごとにtraffic/data ownershipを移す。

### 直感 → 図解 → 数式 → 例 → 実装

```text
clients -> facade/router -> legacy path
                         -> new slice
measure parity -> shift ownership -> delete old slice
```

```python
def route(cmd):
    return new_service(cmd) if cmd.capability in migrated else legacy(cmd)
```

この分岐には期限・owner・削除条件が必要で、永続互換層にしない。

### よくある誤解／実務接続

- legacy=monolith/Cobolではない。新しい変更不能microservicesもlegacy化する。
- complete rewriteは未知仕様を再発見する大規模product project。
- characterization testは奇妙な挙動を全て永久契約にするものではない。
- data migrationとreconciliationが中心riskになりやすい。

### 要点

1. 年齢でなく変更制約で定義。 2. 現在価値を認識。 3. seamから段階移行。 4. parity/reconciliationを測る。 5. 旧path削除まで完了しない。

### 誤解チェック（5問）

1. 古い言語ならrewrite必須か。 2. microservicesはlegacyにならないか。 3. strangler分岐は永久か。 4. parity=同一bugも保存か。 5. code移行だけで完了か。

### 基礎問題（5問）

1. 制約を七分類せよ。 2. seamを探せ。 3. characterization testを書け。 4. reconciliationを設計せよ。 5. deletion criteriaを書け。

### 応用問題（3問）／設計問題／調査課題

1. rewrite business caseを反証せよ。 2. database decompositionを段階化せよ。 3. semantic parityを定義せよ。 **設計:** billing legacyのstrangler計画を設計せよ。 **調査:** 最も恐れられるmoduleの制約を証拠化せよ。

### 知らないとする誤判断／次章への接続

「新stackなら解決」と一括rewriteし、十年分の例外仕様とdata qualityを失う。次章ではsystem境界とteam認知負荷を合わせる。

---

## 第26章　Team Topology と組織構造

### この章を学ぶ理由／現場の問題

architecture境界とownershipが合わないと、日常変更が多team調整になる。teamを一時project resourceでなく、長寿命な価値・platform・能力の単位として設計する。

### 中心概念と正式な定義

Team Topologiesの語彙では stream-aligned、platform、enabling、complicated-subsystem team、interaction modeとして collaboration、X-as-a-Service、facilitating。cognitive loadはteamが安全に保持できるdomain/technology/operation知識の総量。team APIは提供能力、service level、利用方法、support、ownershipを示す。

### 直感 → 図解 → 数式 → 例 → 実装

```text
stream team -> self-service platform capability
            <- enabling team temporarily facilitates
special algorithm owned by complicated-subsystem team
```

```yaml
team_api:
  owns: [checkout-domain, production-outcomes]
  consumes: [deploy-platform]
  interaction: x-as-a-service
```

### よくある誤解／実務接続

- platform teamはticket受付の共通部門でない。
- collaborationを永続化すると調整依存になる。
- component team分割はend-to-end flowを多handoffにしやすい。
- ownershipにはon-call、data、SLO、retirementを含める。

### 要点

1. flowとteam境界を合わせる。 2. cognitive loadを制限。 3. interaction modeを明示。 4. platformはself-service product。 5. end-to-end ownershipを持つ。

### 誤解チェック（5問）

1. platform=infra ticket teamか。 2. collaborationは常に良いか。 3. 全teamが全stackを知るべきか。 4. ownershipはcodeだけか。 5. reorgでarchitectureは即変わるか。

### 基礎問題（5問）

1. team typeを分類せよ。 2. interaction modeを選べ。 3. cognitive loadを列挙せよ。 4. team APIを書け。 5. handoffを数えよ。

### 応用問題（3問）／設計問題／調査課題

1. platform adoptionをproductとして設計せよ。 2. shared ownershipを解消せよ。 3. enabling engagementの終了条件を作れ。 **設計:** 三streamのteam topologyを設計せよ。 **調査:** 一変更のteam handoff graphを描け。

### 知らないとする誤判断／次章への接続

技術layerごとにteamを分け、単一featureに六teamのticketを必要にする。次章で組織通信とsystem構造の相互作用を形式化する。

---

## 総合演習C（第21〜26章）

1. 共有DBを持つ四team systemの障害を、observability、failure domain、incident roles、ownership、team API、legacy migrationから再設計せよ。
2. retry storm incidentのtimelineを作り、個人操作でなくAPI contract、capacity、telemetry、CI、team boundaryの条件を分析せよ。
3. quarterly maintenance計画を、error budget、EOL、technical debt interest、cognitive loadに基づき優先順位化せよ。

---

## 第27章　Conway's Law

### この章を学ぶ理由／現場の問題

system diagramだけ変えても、組織の通信・責任・予算境界が以前のままなら、codeとruntime依存は元の形へ戻る。architectureとorganizationを共設計する。

### 中心概念と正式な定義

Conway's Lawは、systemを設計する組織は組織のcommunication structureを写した設計を生みやすいという観察。組織通信graph \(G_o=(T,C)\) とsoftware dependency graph \(G_s=(M,D)\) の対応が生じる。inverse Conway maneuverは望ましいarchitectureに適したteam/communication境界を意図的に作るが、命令だけでなくownership、incentive、platform能力が必要。

### 直感 → 図解 → 数式 → 例 → 実装

```text
Org: Web team <ticket> API team <ticket> DB team
Code: web ----sync---- API ----shared schema---- DB

Desired flow: stream team owns vertical capability via stable platform APIs
```

```yaml
fitness:
  - "stream team changes its capability without synchronized release"
  - "database ownership has one accountable module"
```

### よくある誤解／実務接続

- 法則は物理的必然や単純一対一対応でない。
- org chartだけで実通信networkは分からない。
- service数をteam数へ機械的に合わせない。
- shared platform、communities of practiceで必要な横断整合を保つ。

### 要点

1. 通信構造が設計へ影響。 2. 実際の協働graphを見る。 3. ownership/incentiveを構造と合わせる。 4. inverse maneuverは継続施策。 5. architecture fitnessで効果を測る。

### 誤解チェック（5問）

1. Conwayは必ず一team一serviceか。 2. reorgだけでcodeが変わるか。 3. org chart=通信graphか。 4. 横断交流は全て悪か。 5. architectureが組織にも影響するか。

### 基礎問題（5問）

1. 二graphを描け。 2. 対応を探せ。 3. coordination edgeを数えよ。 4. desired boundaryを示せ。 5. fitness functionを書け。

### 応用問題（3問）／設計問題／調査課題

1. matrix organizationの影響を論ぜよ。 2. vendor境界をgraphへ入れよ。 3. communitiesの役割を設計せよ。 **設計:** inverse Conway移行を設計せよ。 **調査:** chat/review/incidentから実communication graphを調べよ。

### 知らないとする誤判断／次章への接続

service境界だけ引き直し、毎変更で同じ承認chainと共有DB teamを必要にする。次章では不確実性へ合わせて開発processを選ぶ。

---

## 第28章　開発プロセス：waterfall・iterative・agile

### この章を学ぶ理由／現場の問題

processを宗派や会議templateで選ぶと、riskとfeedbackの性質に合わない。活動の順序、batch、evidence、governanceをcontextに適応させる。

### 中心概念と正式な定義

waterfallは段階とbaselineを順に進めるpredictive model、iterativeは同じ成果物を反復改善、incrementalは利用可能な能力を増分提供。agileは変化への適応、短いfeedback、working software、協働を重視する原則群で、特定frameworkと同義でない。uncertaintyをrequirements \(U_r\)、solution \(U_s\)、operational \(U_o\) に分け、riskの高い仮説を早く検証する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
known need/known solution -> plan-driven may work
unknown need or solution  -> short experiments/iterations
high assurance            -> explicit evidence and controlled baselines
```

```yaml
iteration:
  riskiest_assumption: "users can complete new flow"
  evidence: "prototype observation"
  decision: [continue, change, stop]
```

### よくある誤解／実務接続

- waterfallは文書があること、agileは文書がないことではない。
- sprintで大batchを小分け表示してもfeedbackは短くならない。
- regulatory environmentでも反復検証は可能で、evidence管理を強める。
- process complianceよりflow outcomeを測る。

### 要点

1. context/riskでprocess選択。 2. iterativeとincrementalを分ける。 3. agileは原則。 4. riskiest assumptionを早期検証。 5. evidenceとbaselineを適切に保つ。

### 誤解チェック（5問）

1. sprintがあればagileか。 2. agileでは計画不要か。 3. waterfallは常に失敗か。 4. incrementはiterationか。 5. 規制下でfeedback不能か。

### 基礎問題（5問）

1. 三不確実性を分類せよ。 2. processを選べ。 3. iteration仮説を書け。 4. incrementを定義せよ。 5. outcome metricを作れ。

### 応用問題（3問）／設計問題／調査課題

1. hardware/software複合processを設計せよ。 2. dual-track discoveryを論ぜよ。 3. stage gateをevidence-basedにせよ。 **設計:** 規制SaaSのhybrid processを設計せよ。 **調査:** 現processの実feedback latencyを測れ。

### 知らないとする誤判断／次章への接続

二週間sprint内で分析からreleaseまで完了しない巨大storyを回し、agileだと判断する。次章では未知を一点日付に隠さない見積りを扱う。

---

## 第29章　見積もりと不確実性

### この章を学ぶ理由／現場の問題

見積りを約束値にするとpadding、隠蔽、品質削減を誘発する。意思決定に必要な範囲、仮定、confidence、更新条件を提供する。

### 中心概念と正式な定義

estimateは未知量の分布または区間、commitmentは組織的約束、targetは望ましい値。workをknown、known unknown、unknown unknownへ分ける。三点見積り optimistic O、most likely M、pessimistic P を使う場合、PERT近似 \(E=(O+4M+P)/6\)、\(SD=(P-O)/6\) だが相関・尾を隠すためsimulationと履歴calibrationが望ましい。forecastは新証拠で更新する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
scope assumptions + historical throughput + dependency risk
             -> completion probability by date, updated weekly
```

```python
for _ in range(10000):
    completion = sum(sample_cycle_time(item) for item in backlog)
    forecasts.append(completion)
```

### よくある誤解／実務接続

- story pointは人日への普遍換算単位でない。
- 詳細分解はaleatory variationや未知依存を消さない。
- 一点日付を「90%」に見せてもcalibrationがなければ根拠薄い。
- scope/date/capacity/qualityのどれを調整可能か明示する。

### 要点

1. estimate/target/commitmentを分ける。 2. 範囲とconfidenceで伝える。 3. 仮定・依存を記録。 4. 履歴でcalibrate。 5. rolling forecastとして更新。

### 誤解チェック（5問）

1. estimateは約束か。 2. pointを日へ換算できるか。 3. 分解すれば未知は消えるか。 4. 50%日付をcommitしてよいか。 5. 途中更新は失敗か。

### 基礎問題（5問）

1. 三点見積りを計算せよ。 2. 仮定を列挙せよ。 3. dependency riskを入れよ。 4. confidenceを説明せよ。 5. targetとforecastを分けよ。

### 応用問題（3問）／設計問題／調査課題

1. Monte Carlo forecastを実装せよ。 2. correlated workをモデル化せよ。 3. reference class forecastingを使え。 **設計:** 経営向け確率forecast報告を設計せよ。 **調査:** 過去見積りのcalibration curveを作れ。

### 知らないとする誤判断／次章への接続

50%程度の最尤日を確約し、遅延時にtestとmigrationを削る。次章では十年単位の進化を前提に設計する。

---

## 第30章　長寿命システムの設計

### この章を学ぶ理由／現場の問題

寿命を延ばすのは未来を正確に予言する一般化でなく、変化を観測し、小さく移行し、不要経路を削除できる構造と運用である。

### 中心概念と正式な定義

evolvabilityを、新要求へ許容risk/costで適応できる能力とする。原則は stable domain boundary、information hiding、explicit data ownership、compatible evolution、automated evidence、observability、replaceability、retirement。change budgetは通常開発だけでなくmigration、dual-run、reconciliation、rollback、deletionを含む。option valueは将来選択肢を保持する価値だが、常設抽象の費用と比較する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
old schema -> expand(add) -> dual read/write + reconcile
           -> switch authority -> contract(remove old)
```

```yaml
evolution_contract:
  compatibility_window: "2 releases"
  authority_switch_metric: "parity=100%, lag<1m"
  old_path_removal_owner: "orders"
```

### よくある誤解／実務接続

- 「柔軟な汎用framework」は将来変更を安くするとは限らない。
- backward compatibilityを無期限に守る必要がない単一deployでは、caller同時更新と旧経路削除が自然。
- data寿命はcodeより長く、schema/semanticsを優先設計する。
- dependency選択はadoptionだけでなくexit costとgovernanceを見る。

### 要点

1. 予言より変更mechanism。 2. data ownershipとsemanticsを守る。 3. compatible migrationを段階化。 4. evidenceでauthorityを切替。 5. 古い経路を必ず削除。

### 誤解チェック（5問）

1. 汎用化すればfuture-proofか。 2. compatibilityは永久か。 3. code置換でdata移行も完了か。 4. dual writeは安全か。 5. popular dependencyはexit容易か。

### 基礎問題（5問）

1. expand/contractを書け。 2. authorityを定義せよ。 3. reconciliation invariantを書け。 4. removal conditionを作れ。 5. exit costを評価せよ。

### 応用問題（3問）／設計問題／調査課題

1. semantic versioning限界を論ぜよ。 2. event schema進化を設計せよ。 3. reversible/irreversible decisionを分けよ。 **設計:** 10年保守するledgerの進化機構を設計せよ。 **調査:** 現systemの削除不能経路を列挙せよ。

### 知らないとする誤判断／次章への接続

「将来のため」未使用plugin pointsを多数作り、現在のinvariantを弱める。次章では実際の大規模変更を段階的に組み立てる。

---

## 第31章　大規模変更ケーススタディ

### この章を学ぶ理由／現場の問題

共有customer tableをdomain-owned modelへ移す変更を通じ、architecture、data、API、team、rolloutを一つのmigration systemとして扱う。

### 中心概念と正式な定義

現状：六serviceが同tableへread/write、schema意味が暗黙、deploy協調が必要。目標：Customer moduleがauthoritative、明示API/eventで利用、単一deploy組織なのでcallerを同時更新し旧column/pathを削除する。migration invariantは (1)一顧客一authority、(2)金額/consent不損失、(3)replay idempotent、(4)cutover中もSLO維持。

### 直感 → 図解 → 数式 → 例 → 実装

```text
phase 0 characterize/ownership
phase 1 new model + backfill + continuous reconciliation
phase 2 caller migration + shadow reads
phase 3 authority cutover + monitor
phase 4 delete direct DB access, old columns, dual paths
```

```python
def reconcile(old, new):
    return canonicalize(old) == canonicalize(new)
```

各phaseはentry/exit evidence、blast radius、rollback/forward recoveryを持つ。

### よくある誤解／実務接続

- dual writeはtransaction境界を跨ぎ差分を生む。outbox/replay/reconciliationが要る。
- facadeだけ置いて共有ownershipを残すと構造は変わらない。
- 旧columnを残す「保険」は未知readerを永続化する。
- cutover成功直後でなく安定確認後すみやかに削除する。

### 要点

1. target invariantから設計。 2. 現依存を発見。 3. backfillと継続changeを統合。 4. parityを定量確認。 5. 旧ownershipを削除して完了。

### 誤解チェック（5問）

1. dual writeで自動一致か。 2. API追加だけでownership移行か。 3. backfill中更新を無視できるか。 4. rollbackは常にschemaを戻すことか。 5. 旧column保持は無料か。

### 基礎問題（5問）

1. dependency mapを描け。 2. invariantを列挙せよ。 3. backfill checkpointを設計せよ。 4. parity metricを作れ。 5. deletion listを書け。

### 応用問題（3問）／設計問題／調査課題

1. outboxとCDCを比較せよ。 2. zero-downtime cutoverを設計せよ。 3. semantic mismatchを調停せよ。 **設計:** phaseごとのADR/rolloutを完全設計せよ。 **調査:** repo/DB telemetryから隠れreaderを発見せよ。

### 知らないとする誤判断／次章への接続

新tableへ一度copyして完了とし、移行中更新と隠れwriterで不整合を生む。次章ではこのような判断をADRとして比較・記録する。

---

## 第32章　Architecture Decision Record 演習

### この章を学ぶ理由／現場の問題

decisionの結論だけ残すと、前提変化後も慣性で守られるか、同じ議論を反復する。ADRは当時のcontext、forces、選択肢、結果、再検討triggerを軽量に記録する。

### 中心概念と正式な定義

ADRは Title、Status、Context、Decision drivers、Options、Decision、Consequences、Validation、Review trigger を持つimmutable decision snapshot。supersede時は旧ADRを消さず新ADRへlinkする。decision qualityは結果の幸運でなく、当時利用可能な情報で目的・選択肢・trade-off・evidenceを適切に扱ったかで評価する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
Context/forces -> Options A/B/C -> Decision -> expected consequences
      ^ assumptions                               | fitness evidence
      +------------ review trigger ---------------+
```

```markdown
# ADR-042: Customer data authority
Status: Accepted
Decision: module-owned schema and typed API; migrate all callers; delete shared writes
Validation: dependency rule, parity metric, SLO
Review trigger: >3 independent deploy units or transaction model changes
```

### よくある誤解／実務接続

- ADRは事後の正当化文書でない。
- 全小実装をADRにせず、高影響・高撤回費・横断decisionに使う。
- option listだけでdecision driverの重みがなければ比較不能。
- acceptedは永続不変でなくstatusとtriggerで進化する。

### 要点

1. why/contextを保存。 2. 実在optionを比較。 3. consequenceを負も含める。 4. validation fitnessを定義。 5. supersedeで履歴を保つ。

### 誤解チェック（5問）

1. ADRは会議議事録か。 2. acceptedは変更禁止か。 3. 選択肢一つで十分か。 4. positive consequenceだけでよいか。 5. 古いADRを編集消去すべきか。

### 基礎問題（5問）

1. contextを書け。 2. driversを優先順位化せよ。 3. 三optionを作れ。 4. consequenceを書け。 5. review triggerを定義せよ。

### 応用問題（3問）／設計問題／調査課題

1. decision matrixの偽精密性を論ぜよ。 2. two-way door decisionを簡略化せよ。 3. superseding ADRを書け。 **設計:** 第31章の完全ADRを作れ。 **調査:** 現architectureの理由不明decisionを一件復元せよ。

### 知らないとする誤判断／次章への接続

「以前決まったから」を根拠に、消滅した前提のarchitectureを維持する。最終章で変更可能性を損なう典型誤判断を横断的に点検する。

---

## 総合演習D（第27〜32章）

1. 共有DB分割をinverse Conway、確率forecast、expand/contract、reconciliation、ADR、削除条件まで含むprogramとして設計せよ。
2. 「microservicesへ半年で移行」というtargetを、quality scenario、option、confidence分布、phase evidence、team topologyで再構成せよ。
3. 規制対象systemの開発processを、短いfeedbackとbaseline/evidence管理が両立するよう設計せよ。

---

## 第33章　この分野を知らないエンジニアが陥りやすい誤判断

### この章を学ぶ理由／現場の問題

多くの失敗は個別技法不足でなく、局所最適、暗黙契約、責任分断、移行未完了から起きる。以下は優先度の高い原因仮説から並べた設計レビュー用countermeasureである。

### 中心概念と正式な定義

変更の総riskを概念的に \(R=P(failure)\times Impact\)、総costを \(C=understand+coordinate+implement+verify+migrate+operate+retire\) と分解する。局所diffの小ささでなく、invariant、ownership、feedback、可逆性、旧経路削除まで含む \((R,C)\) を減らす。

### 直感 → 図解 → 数式 → 例 → 実装

```text
requirement -> decision -> code/data/config -> deploy -> user outcome
      traceability + evidence + owner + rollback/forward recovery
      completion includes retirement of the superseded path
```

```python
change_done = (
    acceptance_met and slo_healthy and migration_reconciled
    and old_path_deleted and owner_accepts_operation
)
```

### Countermeasures：誤判断24例

1. **対策: goal、制約、acceptance evidenceを要求に書く（想定原因: stakeholderの最初の解決案を要求そのものとみなす）。** solutionを選ぶ前に問題を検証する。
2. **対策: 機能ごとにquality attribute scenarioを作る（想定原因: 正しく動けば性能・信頼性・安全性は後付けできると思う）。** 刺激、環境、応答尺度を含める。
3. **対策: 変更理由を隠すmodule境界を設計する（想定原因: file/serviceを増やせばmodularになると思う）。** dependency cycleとco-changeを検査する。
4. **対策: service分割前にtransaction、data ownership、failure domain、teamを比較する（想定原因: microservicesが自動的に疎結合を作ると思う）。** modular monolithも実在optionにする。
5. **対策: failure taxonomy、idempotency、ordering、timeout後状態をAPI契約に入れる（想定原因: network callをlocal functionと同じと考える）。** retryを正常系としてtestする。
6. **対策: 変化が二度現れてから責務ごとに抽象化する（想定原因: 将来の柔軟性には万能interfaceが必要と思う）。** 未使用extension pointを削除する。
7. **対策: patternのcontext・forces・代償を書く（想定原因: pattern名の採用を設計品質とみなす）。** 直接実装との比較を残す。
8. **対策: risk別test portfolioと強いoracleを設計する（想定原因: coverage率をcorrectness確率と読む）。** mutation/property/contractを目的に応じて使う。
9. **対策: clock、random、I/Oを明示dependencyにする（想定原因: flaky testは環境問題だからretryすればよいと思う）。** raceと非決定性の根を直す。
10. **対策: verificationとvalidationのclaim/evidenceを分ける（想定原因: 仕様適合が利用価値も保証すると思う）。** 本番利用feedbackへtraceする。
11. **対策: build onceしたimmutable artifactとrelease manifestを昇格する（想定原因: 同じcommitなら全環境で同じsystemと思う）。** config/schema/flag/toolchainをversion化する。
12. **対策: CIのcritical path、queue、flakeを測る（想定原因: checkを追加するほど安全であると思う）。** 速い反証を先にし、小batchを保つ。
13. **対策: PRにwhy、invariant、risk、rollout、rollbackを書く（想定原因: diffだけで変更意図は十分伝わると思う）。** 人reviewを意味判断へ集中させる。
14. **対策: feature変更と意味保存refactorを分離する（想定原因: 大rewriteを一度に行う方が整合的と思う）。** characterizationから小stepで進める。
15. **対策: debtをprincipal、interest、risk、triggerで記録する（想定原因: 汚く見えるcodeが最優先debtと思う）。** 高churn/high-impactから返済する。
16. **対策: user outcome SLIとdiagnostic telemetryを相関可能にする（想定原因: log/metricを大量収集すればobservableと思う）。** telemetry contractをtestする。
17. **対策: incidentを役割分担しmitigationを先行する（想定原因: 原因を知る最強engineerが全部指揮・修正すべきと思う）。** timelineと定時通信を保つ。
18. **対策: 共通原因とretry amplificationをfault modelへ入れる（想定原因: replica/retry追加は単調にreliabilityを上げると思う）。** degradationとbudgetを設計する。
19. **対策: maintenanceをcorrective/adaptive/perfective/preventiveで容量計画する（想定原因: 新機能以外は価値を生まないと思う）。** EOLとupgradeを定常flowにする。
20. **対策: legacyを変更制約別に分解しseamから移行する（想定原因: 古い技術を一括rewriteすれば負債が消えると思う）。** parityとdata reconciliationを証拠にする。
21. **対策: team境界をvalue flow、cognitive load、ownershipに合わせる（想定原因: component専門teamが最も効率的と思う）。** handoffと待ち時間を減らす。
22. **対策: estimateを範囲・confidence・仮定で示す（想定原因: 最尤日を約束に変えても不確実性は消えると思う）。** rolling forecastを更新する。
23. **対策: 大規模移行をauthority、backfill、reconciliation、cutover、deleteへ分ける（想定原因: データcopyと新API追加で移行完了と思う）。** 旧writer/reader/columnを削除する。
24. **対策: ADRにcontext、options、consequences、fitness、review triggerを残す（想定原因: 結論だけ残せば後任も判断を再現できると思う）。** 前提変化時はsupersedeする。

### よくある誤解／実務接続

- checklistの全項目を増やすのではなく、change riskに応じて証拠の深さを選ぶ。
- 小diffはreview容易性の一要素だが、旧経路を残す継ぎ接ぎなら総変更を悪化させる。
- backward compatibilityが不要な単一deployではcallerを同時更新し古い契約を削除する。
- process指標を目標化し、PR数やdeploy数だけを増やすとGoodhart化する。

### 要点

1. 根本の構造原因を直す。 2. 変更総費用とriskで判断。 3. 契約・owner・evidenceを明示。 4. 小さく観測可能に移行。 5. 旧経路削除まで完了させる。

### 誤解チェック（5問）

1. 小diffなら長期保守性も高いか。 2. service分割でdata couplingは消えるか。 3. coverage100%なら本番安全か。 4. deploy成功でchange完了か。 5. 互換経路は多いほど安全か。

### 基礎問題（5問）

1. 一変更の総費用を分解せよ。 2. implicit contractを一つ明示せよ。 3. ownership gapを特定せよ。 4. rollback/forward recoveryを分けよ。 5. deletion criteriaを書け。

### 応用問題（3問）／設計問題／調査課題

1. 小diffだが負債を増やす変更を再設計せよ。 2. 組織とarchitectureのcycleを分析せよ。 3. reliabilityとdelivery speedを同時改善するfeedbackを設計せよ。 **設計:** 要求からretirementまでを結ぶ組織共通change contractを設計せよ。 **調査:** 最近の大変更を24項目で監査し、上位3原因を証拠付きで選べ。

### 知らないとする誤判断／次章への接続

症状を抑えるflag・try/catch・互換分岐を積み重ね、三か月後の変更者へ複雑性を移す。本書の次は、実案件一つで要求、ADR、test、rollout、operation、retirementを同じtraceに結び、feedbackから設計を継続更新する。

## 参考文献

- Ian Sommerville, *Software Engineering*, 10th ed., Pearson, 2015.
- David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, 1972.
- Len Bass, Paul Clements, Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
- Martin Fowler, *Refactoring*, 2nd ed., Addison-Wesley, 2018.
- Michael Nygard, *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018.
- Matthew Skelton, Manuel Pais, *Team Topologies*, IT Revolution, 2019.
- [SWEBOK Guide](https://www.computer.org/education/bodies-of-knowledge/software-engineering)
- [Architecture Decision Records](https://adr.github.io/)
- [Google SRE Books](https://sre.google/books/)
- [ISO/IEC 25010 software product quality model overview](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)

---

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **softwareは変化し続けるsocio-technical systemである。** codeだけでなく、利用者、team、運用、data、規制、供給者を含む系が時間とともに変わる。専門家は初回実装費より、理解・調整・移行・運用・廃止を含む変更総費用を見る。
2. **moduleは「一緒に変わる理由」を封じ込める境界である。** file数やservice数ではなく、隠すべき設計判断と依存方向でmodularityを評価する。変更理由の異なるものを分け、同じ理由で変わるものを近づけることで、変更のblast radiusを抑える。
3. **正しさは契約と不変条件の連鎖である。** requirement、type、API、DB制約、protocol、運用手順は、それぞれ異なる境界で保証を担う。専門家は「testが通った」では止まらず、誰がどの前提の下で何を保証し、失敗時にどの状態が残るかを追う。
4. **開発はfeedback制御系である。** 仮説を小さな変更へ変換し、build、test、review、deploy、telemetry、利用者結果から誤りを早く返す。速度は作業量ではなく、誤った方向へ進んだ時間を短くしながら安全に学べる能力で測る。
5. **設計は不確実性の下でoptionを管理する行為である。** 可逆な決定は遅らせ、小さく試し、不可逆で高影響な決定には深い証拠を要求する。冗長性、abstraction、互換性にも維持費があるため、「将来使うかも」ではなく、具体的な変化と撤回条件に結びつける。

### 専門家の意見が根本的に分かれる3つの論点

1. **どこまで先にarchitectureを設計すべきか。**
   - **up-front architecture側の最も強い主張:** data ownership、security boundary、availability、規制のような後戻り費用の高い性質は、局所的refactoringの積み重ねでは回復できないことがある。品質属性scenarioと全体制約を先に設計しなければ、teamは整合しない局所最適へ進む。
   - **evolutionary design側の最も強い主張:** requirementとworkloadは実装・利用を通して初めて分かる。早期の詳細設計は最も情報の少ない時点の推測を固定するため、単純なarchitecture、fitness function、小さな変更で進化させる方が適応的である。
   - **判断を分ける制約:** 失敗の不可逆性、規制、物理配置、team数、変更可能な境界、feedbackまでの時間。争点は「設計するか」ではなく、いつ何を確定し何を可逆に保つかである。
2. **独立serviceへ分割するか、modular monolithに留めるか。**
   - **service分割側の最も強い主張:** 独立deploy、resource isolation、failure containment、team ownershipが必要な境界はprocessとdata storeまで分けることで初めて強制できる。組織規模が大きいほど調整をinterfaceへ変換できる価値が増す。
   - **monolith側の最も強い主張:** 分散化はnetwork failure、非同期整合性、observability、運用platformという本質的複雑性を導入する。明確なmoduleと単一transactionで十分なら、同一processの方が変更とdebuggingの総費用は小さい。
   - **判断を分ける制約:** 独立した変更頻度、data invariant、failure domain、scaling特性、teamの認知負荷、運用成熟度。service数そのものは品質指標ではない。
3. **保証を形式化・静的制約へ寄せるか、実行時feedbackへ寄せるか。**
   - **formal/static側の最も強い主張:** 型、model checking、証明、静的解析は巨大な入力空間を一般化し、productionで発見してはならない安全性違反を事前に排除できる。high-assurance systemでは経験的成功回数は反例不存在の証明にならない。
   - **empirical/runtime側の最も強い主張:** modelと仕様も誤り得て、現実の依存関係・利用者・負荷を完全には表せない。property test、段階rollout、observability、迅速なrecoveryを組み合わせた方が、未知の失敗に適応できる。
   - **判断を分ける制約:** harm severity、状態空間、仕様可能性、変更頻度、検証費用、回復可能性。成熟したsystemは両者を層として組み合わせ、どちらか一方へ全責任を置かない。

### 深い理解と暗記を見分ける10の質問

1. 請求書生成と税計算は今まで常に同時変更されてきたが、来期から国別税制だけを別teamが毎週releaseする。同一moduleのままか分割するかを、現在と将来の変更理由、共有invariant、依存方向から決め、その判断を覆す証拠も示せ。
2. coverage 100%のsystemでも重大障害が起こる具体例を作り、どのtest oracle・境界保証・本番観測が欠けていたかを示せるか。
3. 注文・決済・在庫を三serviceへ分ける案を、三teamの独立release要求、在庫のhot key、三者をまたぐ業務不変条件の下で評価せよ。process分離が強制する便益と、新たに必要になる失敗時protocol・reconciliation・観測を同じ粒度で比較し、採否を変える計測結果を示せ。
4. 大規模rewriteと段階移行のどちらを選ぶか。状態移行、parity、reconciliation、rollback、旧経路削除まで含む判断基準を示せるか。
5. 「API timeout」という一つのerrorを、再試行可能性、処理結果不明、冪等性、利用者への契約へ分解できるか。
6. release日を一日で約束するよう求められたが、外部APIの適合試験とdata migration速度が未計測である。既知作業と不確実性を分け、範囲・確率・前提・先行実験・判断checkpointを持つforecastへ変換し、新証拠でどう更新するか示せ。
7. deploy回数が増えたのに利用者価値と信頼性が悪化した。どのfeedback loopとGoodhart化を疑い、metricをどう組み直すか。
8. incidentの最終操作が担当者の誤commandだった。「human error」で終えず、再発へ至る必要条件と防護の欠落をどう分析するか。
9. backward compatibilityを維持する場合と破壊的変更で旧経路を消す場合を、利用者数だけでなくauthority、移行可能性、認知負荷、長期riskから比較できるか。
10. 三か月後に不要になる可能性のあるabstractionを今作るべきか。option value、carrying cost、撤回条件、重複の証拠を用いて判断できるか。
