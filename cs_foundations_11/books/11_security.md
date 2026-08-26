# 情報セキュリティ――安全なシステムを設計する思考モデル

本書は攻撃手順集ではない。資産、攻撃者能力、信頼境界、許容リスクを明示し、予防・検知・対応・回復を設計する。暗号アルゴリズムや製品設定は陳腐化するため、2026-08-27時点の一次資料を末尾に示し、採用時は常に最新版を再確認する。

**関連巻:** policyの形式化は [離散数学](02_discrete_math.md)、process・memory・権限境界は [オペレーティングシステム](05_operating_systems.md)、分散したidentityとfailureは [並行・並列・分散システム](06_concurrency_distributed.md)、DBの制約・分離・暗号化は [データベース理論](07_database.md)、secure lifecycleとincident改善は [ソフトウェア工学](09_software_engineering.md)、利用者の誤操作を誘発しない設計は [HCI](10_hci.md) を参照する。

## 第1章 Securityとは何か
### 章を学ぶ理由
securityを機能ではなく、敵対的環境で望ましくない状態遷移を抑える継続的リスク管理として捉える。
### 現場の問題
脆弱性ゼロ、監査合格、TLS導入を「安全」と同一視する。
### 中心概念と正式定義
system、asset、adversary、policy、mechanism、assumptionを区別する。安全性は絶対値でなく、攻撃者能力Aと環境Eの下でpolicy P違反確率・影響を受容範囲に保つ性質。security objectiveを検証可能な不変条件へする。
### 直感→図解→数式→例
`asset→trust boundary→mechanism→evidence`。例: 「他tenantの行を読めない」を `∀u,r. tenant(u)≠tenant(r)⇒¬CanRead(u,r)` と書く。
### 実装または疑似コード
```text
define assets, adversary_capabilities, invariants, boundaries
design prevent/detect/respond/recover controls; test counterexamples
```
### よくある誤解
securityは二値の完成状態でもsecurity teamだけの責任でもない。security through obscurity単独は境界にならない。
### 実務接続
要件、architecture review、SLO、incident、調達、廃棄まで全lifecycleに現れる。
### 要点
- 敵対者を前提にする。 - 資産とpolicyを明示。 - 仮定を記録。 - 証拠で保証を評価。 - 継続的に更新する。
### 誤解チェック（5問）
1. 脆弱性ゼロを証明できるか。2. TLSだけで認可も解決か。3. 監査合格は将来攻撃も保証か。4. 隠蔽だけで安全か。5. securityは運用後だけか。
### 基礎問題（5問）
1. assetを5つ挙げよ。2. adversaryを定義せよ。3. policyを書け。4. mechanismとobjectiveを分けよ。5. evidenceを挙げよ。
### 応用問題（3問）
1. tenant不変条件を書け。2. abuse caseを作れ。3. securityとsafetyを比較せよ。
### 設計問題（1問）
ファイル共有APIのsecurity objectiveと検証証拠を設計せよ。
### 調査課題（1問）
NIST CSF 2.0の6機能を自systemへmappingせよ。
### 知らないとする誤判断
一つのcontrol導入を、system全体の安全性証明とみなす。
### 次章接続
守るべき性質をCIAへ分解する。

## 第2章 CIA Triad
### 章を学ぶ理由
機密性・完全性・可用性のどれを誰に対して守るかを分離する。
### 現場の問題
暗号化で可用性や正当な更新まで守れたと思う。
### 中心概念と正式定義
Confidentialityは許可されない情報開示の防止、Integrityは許可されない変更・破壊の防止と真正性、Availabilityは許可主体が必要時に利用できる性質。authenticity、accountability、privacy等を補助目的とする。
### 直感→図解→数式→例
`read→C, write→I, service→A`。ransomwareはIとA、漏えいはC、改ざんbackupはIと回復性を侵す。
### 実装または疑似コード
```text
for each asset: owner; C requirement; I requirement; A/SLO; evidence; recovery
```
### よくある誤解
CIAの優先度はsystemごとに異なり、相互に独立でもない。availabilityは単なるuptimeでない。
### 実務接続
data classification、checksum/signature、redundancy、DR、rate limitの設計軸となる。
### 要点
- C/I/Aを別要件化。 - 主体と時間を明示。 - privacyをCだけに還元しない。 - recoveryもA。 - trade-offを記録。
### 誤解チェック（5問）
1. 暗号化でIも自動保証か。2. backupはCに無関係か。3. Aは100% uptimeか。4. ログ改ざんはIか。5. privacy=Cだけか。
### 基礎問題（5問）
1. 三性質を定義せよ。2. 事故を分類せよ。3. asset別優先度を付けよ。4. evidenceを示せ。5. conflict例を挙げよ。
### 応用問題（3問）
1. 医療とSNSを比較せよ。2. ransomware対策をCIAで整理せよ。3. rate limit trade-offを論ぜよ。
### 設計問題（1問）
監査ログのCIA要件と保持を設計せよ。
### 調査課題（1問）
自社SLOがavailability security要件をどう含むか調べよ。
### 知らないとする誤判断
機密化を強めれば全security指標が改善すると考える。
### 次章接続
CIAを適用する対象、assetを洗い出す。

## 第3章 Asset
### 章を学ぶ理由
守る対象と所有者がなければcontrolの費用対効果を判断できない。
### 現場の問題
顧客データだけ見て、credential、build pipeline、availability、評判、派生metadataを落とす。
### 中心概念と正式定義
assetは組織・利用者に価値を持ち損失が影響を生むもの。data、service、identity、key、code、model、process、人、評判を含む。owner、classification、lifecycle、dependency、impactを記録する。
### 直感→図解→数式→例
`source data→derived data→backup→logs` とcopyを追う。資産価値は金額だけでなく法的・安全・信頼・業務停止影響を含む。
### 実装または疑似コード
```text
Asset{id,owner,location,copies,classification,retention,dependencies,CIA_impact}
```
### よくある誤解
CMDB itemだけがassetではない。暗号化後dataもkeyと組み合わせれば依然assetである。
### 実務接続
data inventory、DLP、backup、IAM、SBOM、BCPに接続する。
### 要点
- 価値と影響で定義。 - ownerを置く。 - copy/派生を追う。 - lifecycleを持つ。 - dependencyを記録。
### 誤解チェック（5問）
1. public dataはassetでないか。2. keyはassetか。3. availabilityはasset価値か。4. 削除済みならbackupにもないか。5. owner不在で分類可能か。
### 基礎問題（5問）
1. asset inventoryを作れ。2. ownerを割当てよ。3. copyを追え。4. impactを分類せよ。5. retentionを書け。
### 応用問題（3問）
1. derived featureを分類せよ。2. build system assetを列挙せよ。3. shadow dataを発見せよ。
### 設計問題（1問）
MLサービスのdata/model/pipeline asset台帳を設計せよ。
### 調査課題（1問）
実systemのdata flowから未登録assetを探せ。
### 知らないとする誤判断
production DBだけを守り、log・export・backupの同じ秘密を放置する。
### 次章接続
assetへ損害を与え得る状況、threatを定義する。

## 第4章 Threat
### 章を学ぶ理由
攻撃者の意図・能力・機会と偶発事象を具体化する。
### 現場の問題
「hacker」を万能存在にして優先順位を失うか、既知攻撃名だけ見て内部者や誤操作を落とす。
### 中心概念と正式定義
threatはassetへ損害を与え得る潜在的原因。threat actor、capability、intent、access、precondition、action、impactを分ける。adversary modelは攻撃者が制御・観測できる境界を定義する。
### 直感→図解→数式→例
`actor + capability + opportunity → threat event → impact`。internet attackerとcloud adminでは利用可能経路が違う。
### 実装または疑似コード
```text
Threat{actor,goal,capabilities,entry,preconditions,target,impact,evidence}
```
### よくある誤解
threatとvulnerability、threat actorと実在人物の断定を混同しない。自然災害もavailability threatになり得る。
### 実務接続
abuse case、fraud、insider risk、DDoS、供給者評価に使う。
### 要点
- actor能力を具体化。 - 意図と偶発を含む。 - 前提を列挙。 - assetへ結ぶ。 - intelligenceで更新。
### 誤解チェック（5問）
1. threat=vulnerabilityか。2. 全攻撃者は同能力か。3. 誤操作はthreatか。4. intentなしなら除外か。5. actor名だけでモデル完成か。
### 基礎問題（5問）
1. actorを3種挙げよ。2. 能力を定義せよ。3. entryを書け。4. preconditionを示せ。5. impactへ結べ。
### 応用問題（3問）
1. insiderをモデル化せよ。2. DDoS能力を段階化せよ。3. supplier compromiseを描け。
### 設計問題（1問）
CI/CDに対する三actorのthreat modelを作れ。
### 調査課題（1問）
実incidentのactor能力を公開証拠だけで再構成せよ。
### 知らないとする誤判断
攻撃者能力を無限大と置き、実行可能なcountermeasureの優先度を失う。
### 次章接続
threatが利用するsystem側の弱点を扱う。

## 第5章 Vulnerability
### 章を学ぶ理由
欠陥がどの前提・経路で悪用可能かを根因まで追う。
### 現場の問題
CVE数をsecurity水準とし、misconfiguration、design flaw、弱いprocessを落とす。
### 中心概念と正式定義
vulnerabilityはthreatがsecurity policy違反に利用できるsystem・設計・実装・運用上の弱点。exposure、exploitability、reachability、preconditionを伴う。CWEは弱点類型、CVEは公開脆弱性識別、severityはcontextual riskと別。
### 直感→図解→数式→例
`weakness + reachable path + capability → exploit → impact`。脆弱libraryが存在しても対象code path不使用なら直近exploitabilityは違うが、inventoryと更新責務は残る。
### 実装または疑似コード
```text
triage(v): affected? reachable? attacker prerequisites? compensating controls? asset impact?
```
### よくある誤解
scanner未検出は不存在証明でない。patchだけで設計根因や盗まれたcredentialは戻らない。
### 実務接続
SAST/DAST/SCA、patch、bug bounty、configuration review、root cause analysisに接続。
### 要点
- 弱点と利用経路を分ける。 - CVE/CWE/riskを区別。 - reachabilityを見る。 - 根因を直す。 - 再検証する。
### 誤解チェック（5問）
1. CVSS=riskか。2. CVEなしなら安全か。3. patchで侵害影響も消えるか。4. unreachableは永遠に安全か。5. misconfigurationもvulnerabilityか。
### 基礎問題（5問）
1. 三用語を分けよ。2. preconditionを書け。3. reachabilityを確認せよ。4. controlを列挙せよ。5. 根因を述べよ。
### 応用問題（3問）
1. scanner結果をtriageせよ。2. design flaw例を分析せよ。3. patch SLAをrisk化せよ。
### 設計問題（1問）
脆弱性受付から検証・修正・開示のworkflowを設計せよ。
### 調査課題（1問）
一CVEをCWE、到達性、asset contextまで追え。
### 知らないとする誤判断
severity最高の未到達componentへ全資源を使い、現に露出した弱点を後回しにする。
### 次章接続
threat、vulnerability、impactをriskとして優先順位化する。

## 第6章 Risk
### 章を学ぶ理由
有限資源で、最も重要なsecurity判断を説明可能にする。
### 現場の問題
単純な色付きmatrixやCVSSだけで事業固有の損失と不確実性を消す。
### 中心概念と正式定義
riskは不確実性が目的へ与える影響。簡略に `Risk≈Likelihood×Impact` だが独立・線形とは限らない。inherent、residual、risk appetite/toleranceを区別し、avoid/mitigate/transfer/acceptを選ぶ。
### 直感→図解→数式→例
`scenario→frequency distribution×loss distribution→control→residual`。期待損失だけでtail catastropheを捨てずrangeと信頼度を記録する。
### 実装または疑似コード
```text
Risk{scenario,assets,likelihood_range,impact_range,confidence,controls,residual,owner,due}
```
### よくある誤解
定量値は精密さを保証しない。低確率・壊滅影響を平均だけで落とさない。
### 実務接続
roadmap、exception、insurance、vendor、board reportingに使う。
### 要点
- scenario単位。 - likelihood/impactを分ける。 - 不確実性を表示。 - residualをownerが受容。 - 定期更新する。
### 誤解チェック（5問）
1. CVSS=riskか。2. 低確率なら無視か。3. control後riskゼロか。4. acceptは放置か。5. matrix色は客観値か。
### 基礎問題（5問）
1. scenarioを書け。2. impactを分類せよ。3. rangeを置け。4. residualを述べよ。5. responseを選べ。
### 応用問題（3問）
1. 二riskを比較せよ。2. tailを扱え。3. control効果を測れ。
### 設計問題（1問）
risk registerと例外期限・ownerを設計せよ。
### 調査課題（1問）
NIST CSF 2.0 Governがrisk管理へ追加した観点を調べよ。
### 知らないとする誤判断
スコア小数点の精密さを根拠の確かさと誤認する。
### 次章接続
設計段階でscenarioとcontrolを反復するthreat modelingへ進む。

## 第7章 Threat Modeling
### 章を学ぶ理由
実装前にattack pathとtrust assumptionを共有し、設計変更で根因を除く。
### 現場の問題
リリース直前のcheckbox会議、図だけ、脅威列挙だけで検証・ownerがない。
### 中心概念と正式定義
範囲・asset・DFD・boundary・actorを定め、脅威を列挙、risk評価、mitigation、verificationを追跡する反復process。STRIDE等はpromptであり完全性証明ではない。misuse/abuse caseとattack treeも使う。
### 直感→図解→数式→例
`browser→API→DB`, `API→payment` の各data flowとboundaryへspoof/tamper等を問う。attack treeはroot goalをAND/OR分解する。
### 実装または疑似コード
```text
model = draw(processes,stores,flows,boundaries)
for element: enumerate threats; connect asset/control/test/owner
review on architecture or assumption change
```
### よくある誤解
テンプレートを埋めれば完成ではない。diagram外のCI、operator、recovery経路も範囲に入れる。
### 実務接続
design review、ADR、penetration test scope、security acceptance criteriaに接続。
### 要点
- 範囲と仮定を固定。 - data flowを描く。 - actor能力を置く。 - controlとtestへ追跡。 - 変更時更新。
### 誤解チェック（5問）
1. STRIDEで完全証明か。2. production flowだけでよいか。3. controlなし脅威一覧で完了か。4. 一度で永久有効か。5. data storeだけが対象か。
### 基礎問題（5問）
1. DFDを描け。2. boundaryを置け。3. actorを置け。4. threatsを挙げよ。5. testへ結べ。
### 応用問題（3問）
1. attack treeを作れ。2. abuse caseを優先化せよ。3. architecture差分をreviewせよ。
### 設計問題（1問）
ファイルupload機能をend-to-end threat modelせよ。
### 調査課題（1問）
OWASP Threat ModelingまたはNIST資料の手法を比較せよ。
### 知らないとする誤判断
脅威を多く列挙した文書を、設計変更と検証のないまま成果とみなす。
### 次章接続
攻撃者が触れ得る入口の総体、attack surfaceを縮める。

## 総合演習A（第1〜7章）
新規ファイル共有SaaSについてasset台帳、CIA要件、三actor、vulnerability仮説、risk scenario、DFDを作れ。tenant越境を不変条件で表し、control・verification・residual risk ownerまで追跡せよ。

## 第8章 Attack Surface
### 章を学ぶ理由
入口・出口・権限・データ処理の数と複雑さを減らし、防御対象を制御する。
### 現場の問題
public endpointだけ見てadmin plane、metadata、debug port、egress、dependencyを落とす。
### 中心概念と正式定義
attack surfaceは攻撃者がsystemへ影響を与え得るinteraction pointと信頼仮定の集合。network、software、human、physical、supply chainを含む。露出度×複雑性×privilegeで優先化するが単純個数だけではない。
### 直感→図解→数式→例
`inputs/APIs/files/events/admin → privileged processes → outputs/egress`。使わないport削除はsurfaceを除去し、WAF追加は残したsurfaceへcontrolを置く。
### 実装または疑似コード
```text
inventory listeners,routes,parsers,identities,egress,admin,dependencies
remove > isolate > constrain > monitor
```
### よくある誤解
microservice化はsurfaceを自動縮小しない。内部networkも侵害後は攻撃面になる。
### 実務接続
service catalog、API gateway、firewall、feature retirement、egress policyに現れる。
### 要点
- 全interactionを棚卸し。 - 未使用を削除。 - privilege近傍を優先。 - internalも含む。 - 変更差分を監視。
### 誤解チェック（5問）
1. endpoint数だけか。2. internalは除外か。3. WAFでsurface消滅か。4. dependencyも含むか。5. outboundは無関係か。
### 基礎問題（5問）
1. surfaceを列挙せよ。2. unusedを探せ。3. privilegeを付けよ。4. egressを描け。5. exposureを順位化せよ。
### 応用問題（3問）
1. microservice前後を比較せよ。2. admin planeを隔離せよ。3. parser surfaceを減らせ。
### 設計問題（1問）
plugin systemのsurface budgetを設計せよ。
### 調査課題（1問）
実環境の外部露出とcatalog差分を調べよ。
### 知らないとする誤判断
内部APIはinternet非公開なので認証・入力検証不要とする。
### 次章接続
surfaceを越える際に仮定が変わるtrust boundaryを明示する。

## 第9章 Trust Boundary
### 章を学ぶ理由
信頼度が変わる場所へ認証・検証・記録を置く。
### 現場の問題
VPC、社内network、signed token内claimを一枚岩に信頼する。
### 中心概念と正式定義
trust boundaryは主体、データ、実行環境の保証・管理権限が変わる境界。越境時にprovenance、authenticity、authorization、schema、freshnessを検証する。trustは二値でなく目的別。
### 直感→図解→数式→例
`untrusted browser | API | service identity | DB`。APIがtoken署名を検証してもissuer/audience/expiry/subjectを検証しなければ目的別trustは成立しない。
### 実装または疑似コード
```text
on boundary crossing: authenticate source; validate syntax+semantics;
authorize action; normalize once; log decision; minimize data
```
### よくある誤解
network locationはidentityでない。zero trustは「誰も信じない」でなく都度明示的に検証し権限を最小化する設計原則。
### 実務接続
API gateway、service mesh、CI runner、cloud account、browser/server境界に現れる。
### 要点
- 管理権限差を描く。 - 目的別trust。 - 越境で検証。 - network位置に依存しない。 - decisionを監査。
### 誤解チェック（5問）
1. VPC内=trustedか。2. 署名validなら全claim信頼か。3. boundaryはnetworkだけか。4. validation一回で全表現安全か。5. zero trustは通信禁止か。
### 基礎問題（5問）
1. boundaryを描け。2. ownerを示せ。3. 検証を列挙せよ。4. claimを検証せよ。5. log項目を書け。
### 応用問題（3問）
1. CI boundaryを分析せよ。2. webhookを設計せよ。3. cross-account trustを検討せよ。
### 設計問題（1問）
第三者plugin実行環境のboundaryとsandboxを設計せよ。
### 調査課題（1問）
一cloud architectureの暗黙trustを抽出せよ。
### 知らないとする誤判断
通信元IPが内部なので主体と意図も正当とみなす。
### 次章接続
boundaryを越えた主体へ必要最小限だけ能力を与える。

## 第10章 Principle of Least Privilege
### 章を学ぶ理由
侵害・誤操作時のblast radiusを権限構造で制限する。
### 現場の問題
共有admin、`*:*`、長期credential、build/runtime権限混在が常態化する。
### 中心概念と正式定義
主体sがtask tに必要な期間dだけ必要操作aを対象rへ行える最小capabilityを与える。`Granted(s)⊇Required(s)`を満たし差 `Granted\Required` を最小化。time、resource、operation、contextで絞る。
### 直感→図解→数式→例
`developer→deploy role(15min)→one service`。read/write/adminを分離し、break-glassは通常権限でなく監査付き例外にする。
### 実装または疑似コード
```text
derive permissions from observed+declared tasks; deny by default;
issue short-lived credential; review unused grants; revoke on lifecycle event
```
### よくある誤解
細粒度policyを増やすだけでは、理解不能で実質過剰になる。可用性のための緊急経路も設計する。
### 実務接続
IAM、DB role、Linux capability、container、CI token、JIT accessに現れる。
### 要点
- taskから導く。 - deny by default。 - 時間を絞る。 - shared identityを避ける。 - unusedを削除。
### 誤解チェック（5問）
1. read-onlyは無害か。2. 短期tokenならscope不要か。3. admin共有でaccountability可か。4. policy細分化だけで達成か。5. break-glass不要か。
### 基礎問題（5問）
1. taskを列挙せよ。2. required権限を書け。3. excessを求めよ。4. durationを定めよ。5. revoke eventを挙げよ。
### 応用問題（3問）
1. CI roleを縮小せよ。2. data analyst権限を設計せよ。3. JIT accessを評価せよ。
### 設計問題（1問）
production supportの通常・緊急権限を設計せよ。
### 調査課題（1問）
cloud IAM access analyzer等で未使用権限を調べよ。
### 知らないとする誤判断
業務を止めないため全員へadminを配ることを可用性対策と呼ぶ。
### 次章接続
一control破綻を前提に異種controlを重ねる。

## 第11章 Defense in Depth
### 章を学ぶ理由
単一防御の欠陥・誤設定・bypassが即侵害にならない構造を作る。
### 現場の問題
WAF、EDR、MFAの一つを万能境界とみなし、同じ共通原因で全層が破れる。
### 中心概念と正式定義
defense in depthはprevent/detect/respond/recoverの独立または多様なcontrolをattack path上に置く。層数でなく、異なるfailure mode、検知可能性、residual pathを評価する。
### 直感→図解→数式→例
`input validation→parameter binding→DB least privilege→anomaly detection→backup`。各層が同じ誤ったidentity providerへ依存すれば独立性は低い。
### 実装または疑似コード
```text
for attack_path: controls; bypass assumptions; common dependencies;
detection; containment; recovery evidence
```
### よくある誤解
controlの重複購入や同型scannerの追加はdepthとは限らない。複雑性も新attack surfaceになる。
### 実務接続
segmentation、secure coding、runtime control、monitoring、backupに接続。
### 要点
- 一層破綻を仮定。 - 異種failure mode。 - common causeを探す。 - 検知・回復を含む。 - 複雑性を管理。
### 誤解チェック（5問）
1. control数が多ければdepthか。2. WAFでcode修正不要か。3. 同一IdP依存は独立か。4. detectionは防御外か。5. backupは層か。
### 基礎問題（5問）
1. attack pathを書け。2. controlを配置せよ。3. bypassを挙げよ。4. common causeを探せ。5. recoveryを示せ。
### 応用問題（3問）
1. injection防御を重ねよ。2. credential theft pathを分析せよ。3. control複雑性を評価せよ。
### 設計問題（1問）
admin account takeoverに対する多層防御を設計せよ。
### 調査課題（1問）
既存systemで同一故障点へ依存するcontrol群を調べよ。
### 知らないとする誤判断
入口controlがあるので内部の権限・検知・回復を省く。
### 次章接続
主体が誰であるかの証拠を扱うauthenticationへ進む。

## 総合演習B（第8〜11章）
CI/CD基盤のattack surfaceとtrust boundaryを描き、通常開発者・runner・release signerのleast privilegeを集合で示せ。credential theftとdependency compromiseの二経路に、共通原因を避けた予防・検知・回復controlを配置せよ。

## 第12章 Authentication
### 章を学ぶ理由
提示されたidentity claimを、必要なassuranceで主体へ結び付ける。
### 現場の問題
login成功、session継続、identity proofing、MFA、federationを混同する。
### 中心概念と正式定義
authenticationはclaimantがidentity/controlを持つ証拠を検証するprocess。知識・所持・生体要素、authenticator lifecycle、verifier、IdP、sessionを分ける。MFAは独立要素、phishing resistanceは別性質。
### 直感→図解→数式→例
`enrollment→credential binding→authentication ceremony→session`。password+SMSは二要素でもrelay耐性を自動に持たない。riskに応じstep-upする。
### 実装または疑似コード
```text
verify protocol, origin binding, freshness, authenticator status;
rotate session id; bind assurance+time; reauthenticate sensitive actions
```
### よくある誤解
authenticationはauthorizationでない。生体情報は秘密passwordのように交換できずrevocation特性が異なる。
### 実務接続
passkey/WebAuthn、OIDC、service identity、session管理に現れる。
### 要点
- proofingとauthを分離。 - protocol全体を検証。 - MFA独立性を見る。 - session lifecycleを設計。 - assuranceをactionへ結ぶ。
### 誤解チェック（5問）
1. login済み=全操作許可か。2. 二passwordはMFAか。3. MFA=phishing resistantか。4. sessionは永続identityか。5. 生体は変更容易か。
### 基礎問題（5問）
1. actorを描け。2. factorを分類せよ。3. session eventを列挙せよ。4. reauth条件を決めよ。5. assuranceを定義せよ。
### 応用問題（3問）
1. account recoveryを脅威分析せよ。2. passkey導入を設計せよ。3. federation claimを検証せよ。
### 設計問題（1問）
金融操作のenrollmentからrecoveryまで設計せよ。
### 調査課題（1問）
NIST SP 800-63-4/63B-4のassurance要求を調べよ。
### 知らないとする誤判断
MFA表示があればfactorの独立性・recovery・session theftを調べない。
### 次章接続
認証した主体が何をしてよいかをauthorizationで決める。

## 第13章 Authorization
### 章を学ぶ理由
主体・資源・操作・contextごとに許可を一貫して決定する。
### 現場の問題
UI非表示を認可にする、object IDを知れば読める、service間でpolicyがずれる。
### 中心概念と正式定義
authorization decision `Allow(subject,action,resource,context)→{permit,deny}`。policy decision point(PDP)、enforcement point(PEP)、information point(PIP)を分離。default deny、complete mediation、object-level checkを行う。
### 直感→図解→数式→例
`request→PEP→PDP(policy+attributes)→decision`。`owner(resource)=subject ∨ role=admin`でもtenant境界を別conjunctとして必須化する。
### 実装または疑似コード
```python
def can_read(s,r): return s.tenant_id==r.tenant_id and (r.owner_id==s.id or 'auditor' in s.roles)
```
### よくある誤解
authentication済みtokenやUUID難読性はauthorizationでない。cacheしたdecisionの失効も設計する。
### 実務接続
API middleware、policy engine、row-level security、signed URLに現れる。
### 要点
- 毎resource/actionで判定。 - server側PEP。 - deny default。 - tenant境界を不変条件化。 - decisionを監査。
### 誤解チェック（5問）
1. UI非表示で十分か。2. UUIDはpermissionか。3. roleだけで全context表現か。4. GETだけ確認でよいか。5. decision cacheは永久か。
### 基礎問題（5問）
1. decision関数を書け。2. PEP/PDPを示せ。3. deny defaultを実装せよ。4. object checkを書け。5. audit項目を決めよ。
### 応用問題（3問）
1. BOLA反例を作れ。2. bulk APIを検査せよ。3. stale policyを扱え。
### 設計問題（1問）
multi-tenant document共有のpolicyを設計せよ。
### 調査課題（1問）
利用frameworkの認可enforcement漏れを調べよ。
### 知らないとする誤判断
route単位role checkでobject単位tenant越境も防げると思う。
### 次章接続
authorizationを実現する代表的なaccess control modelを比較する。

## 第14章 Access Control
### 章を学ぶ理由
RBAC、ABAC、ACL、capabilityを制約に応じて選び、policy explosionを避ける。
### 現場の問題
roleを増殖させる、deny/継承競合、共有URLを無期限bearer secretにする。
### 中心概念と正式定義
ACLはobject→subject/permission、capabilityはsubjectが保持する偽造困難な権限、RBACはuser-role-permission関係、ABACは属性述語、MAC/DACはpolicy管理権限が異なる。Separation of Dutiesも制約化する。
### 直感→図解→数式→例
`U↔Roles↔Permissions`。RBACで地域×部署×tierをrole直積にすると爆発し、ABAC predicateへ分解できるが属性信頼性が必要。
### 実装または疑似コード
```text
permit if subject.department=resource.department AND action∈subject.job_permissions
AND context.device_trust>=required
```
### よくある誤解
モデル名で安全性は決まらない。deny precedence、継承、attribute source、revocationを明示する。
### 実務接続
filesystem ACL、cloud IAM、DB grants、Kubernetes RBAC、macaroonsに現れる。
### 要点
- policy形でmodel選択。 - attribute provenance。 - conflict規則。 - SoDを制約化。 - revocationを試験。
### 誤解チェック（5問）
1. RBACは全contextに最適か。2. ABAC属性は常に信頼可か。3. capabilityは推測困難だけで十分か。4. deny競合は自明か。5. role数は無限に増やせるか。
### 基礎問題（5問）
1. 四modelを比較せよ。2. role graphを描け。3. predicateを書け。4. SoDを示せ。5. conflictを解け。
### 応用問題（3問）
1. role explosionを解消せよ。2. signed URLを設計せよ。3. revocation latencyを論ぜよ。
### 設計問題（1問）
医療記録の通常・緊急access controlを設計せよ。
### 調査課題（1問）
cloud IAMのdeny/allow評価logicを公式文書で調べよ。
### 知らないとする誤判断
role名を細かく増やすことをleast privilege達成とみなす。
### 次章接続
最も普及するauthenticatorの一つpasswordを安全に扱う。

## 第15章 Password
### 章を学ぶ理由
人間が選ぶ低entropy secretをonline/offline攻撃と漏えいから守る。
### 現場の問題
高速hash、固定salt、複雑性規則、秘密の質問、平文resetで防御を弱める。
### 中心概念と正式定義
password verifierは一意saltとmemory-hard KDF（例Argon2id）で保存し、parameterとalgorithmを併記。saltは同一passwordの同一hashを防ぎ、pepperは別管理secret。rate limitはonline、KDF costはoffline攻撃へ効く。
### 直感→図解→数式→例
`password+salt --KDF(m,t,p)→verifier`。攻撃費用は候補数×一試行費用。entropyを文字種規則だけで測らず、漏えいpassword blocklistと長さ・managerを重視する。
### 実装または疑似コード
```text
salt=random(); verifier=Argon2id(password,salt,calibrated_params)
verify constant-time library; rehash on login when params obsolete
```
### よくある誤解
saltは秘密でなく、暗号化とhashは別。独自KDFや比較を実装しない。具体parameterは環境と最新標準で校正する。
### 実務接続
password manager、breach response、account recovery、credential stuffingに接続。
### 要点
- memory-hard KDF。 - unique salt。 - parameter versioning。 - online制限。 - recovery/MFAを同時設計。
### 誤解チェック（5問）
1. saltは秘密か。2. SHA-256一回で十分か。3. pepper=saltか。4. 複雑性規則だけで強いか。5. KDFでonline攻撃も十分防げるか。
### 基礎問題（5問）
1. 保存fieldを列挙せよ。2. salt目的を述べよ。3. pepperを配置せよ。4. rate limitを設計せよ。5. rehash時点を決めよ。
### 応用問題（3問）
1. credential stuffingを防げ。2. parameter migrationを設計せよ。3. reset flowを脅威分析せよ。
### 設計問題（1問）
password漏えい後の検知・失効・通知・回復を設計せよ。
### 調査課題（1問）
RFC 9106とNIST SP 800-63B-4の現行推奨を確認せよ。
### 知らないとする誤判断
salt付き高速hashでoffline総当たりが十分遅いと思う。
### 次章接続
password以外も含むcryptographyの保証と前提を整理する。

## 第16章 Cryptographyの考え方
### 章を学ぶ理由
暗号primitiveを目的・threat model・key lifecycleに正しく組み合わせる。
### 現場の問題
独自暗号、algorithm名だけ選定、nonce再利用、key保護なし、暗号化と署名の混同。
### 中心概念と正式定義
cryptographic schemeはkey generation、algorithm、security notion、adversary modelから成る。Kerckhoffsの原則では安全性をalgorithm秘密でなくkey秘密へ置く。confidentiality、integrity、authenticity、freshnessを別に要求する。
### 直感→図解→数式→例
`plaintext --Enc_K(nonce,AAD)→ciphertext,tag`。modern AEADはCとIを合わせるがnonce一意性等の契約がある。暗号強度は弱いkey管理・endpointで上限が決まる。
### 実装または疑似コード
```text
use reviewed high-level library/protocol; generate keys with CSPRNG;
enforce nonce contract; bind context as AAD; version envelope; plan rotation
```
### よくある誤解
「軍用級」やkey長だけで安全は決まらない。base64は暗号でない。自作しないはprimitiveだけでなくprotocol compositionにも当てはまる。
### 実務接続
TLS、disk/data encryption、tokens、signing、secretsに接続する。
### 要点
- 目的を分離。 - adversaryを定義。 - 標準protocol使用。 - key lifecycleが核心。 - algorithm agilityを持つ。
### 誤解チェック（5問）
1. base64は暗号か。2. 秘密algorithmで安全か。3. 長いkeyならnonce再利用可か。4. encryption=authenticityか。5. library利用だけでprotocol安全か。
### 基礎問題（5問）
1. 目的を分類せよ。2. adversaryを書け。3. key lifecycleを列挙せよ。4. nonce契約を述べよ。5. AAD例を挙げよ。
### 応用問題（3問）
1. envelope formatを設計せよ。2. crypto agilityを論ぜよ。3. endpoint compromiseを分析せよ。
### 設計問題（1問）
PII field encryptionをkey rotation・検索・backup込みで設計せよ。
### 調査課題（1問）
利用crypto libraryの高水準APIと安全なdefaultを調べよ。
### 知らないとする誤判断
強いalgorithm名を選べばkey生成・nonce・context bindingの誤りを相殺できると思う。
### 次章接続
同一secretを共有する対称暗号を具体化する。

## 第17章 Symmetric Encryption
### 章を学ぶ理由
大量データを効率よく秘匿し完全性を保つAEADを正しく使う。
### 現場の問題
ECB、unauthenticated encryption、nonce/IV再利用、同じkeyの多用途使用。
### 中心概念と正式定義
対称暗号は同一または容易に導出可能なsecret keyで暗号化・復号。AEADは `Enc(K,N,A,M)→(C,T)`、`Dec`はtag不正ならfailure。IND-CPA/CCA等のsecurity notionとnonce条件がある。KDFで用途別keyを分離する。
### 直感→図解→数式→例
`key+unique nonce+AAD+message→ciphertext+tag`。AADにtenant/id/versionを束縛すればciphertextの別context移植を検知できる。
### 実装または疑似コード
```text
data_key=random(); (c,tag)=AEAD.encrypt(data_key,nonce,aad,plaintext)
store version,nonce,aad,c,tag,wrapped_data_key
```
### よくある誤解
IV/nonceは常に秘密である必要はないが、一意性・予測不能性要件はschemeごとに違う。tag失敗時にplaintextを使わない。
### 実務接続
object encryption、database field、backup、messaging、envelope encryptionに現れる。
### 要点
- AEADを使う。 - nonce契約厳守。 - tagを必ず検証。 - key用途分離。 - envelopeをversion化。
### 誤解チェック（5問）
1. encryptionだけで改ざん検知か。2. nonceはkeyと同じ秘密か。3. tag失敗後も部分利用可か。4. 一keyを全用途で使えるか。5. ECBはpatternを隠すか。
### 基礎問題（5問）
1. API要素を定義せよ。2. AADを選べ。3. envelope fieldを書け。4. failure処理を示せ。5. rotationを描け。
### 応用問題（3問）
1. nonce衝突を防げ。2. streamingを設計せよ。3. backup key lossを分析せよ。
### 設計問題（1問）
multi-tenant object暗号化をtenant key隔離込みで設計せよ。
### 調査課題（1問）
採用AEADのnonce要件を標準から確認せよ。
### 知らないとする誤判断
復号できたことを正当な送信者と改ざんなしの証拠にする。
### 次章接続
事前共有secretなしにkey合意・暗号化を行う公開鍵暗号へ進む。

## 第18章 Public-key Cryptography
### 章を学ぶ理由
公開鍵と秘密鍵の非対称性をkey establishmentとidentityへ使う。
### 現場の問題
公開鍵取得経路を検証せず中間者を許す、巨大dataを直接暗号化、古いpaddingを使う。
### 中心概念と正式定義
key pair `(pk,sk)` を生成し、encryptionまたはsignature/key agreementに使う。機密性は適切なpadding/標準schemeとauthenticated keyが前提。hybrid encryptionはpublic-keyでdata keyを保護し対称AEADでdataを処理する。forward secrecyは長期key漏えい後も過去session keyを守る性質。
### 直感→図解→数式→例
`authenticated pk → ephemeral key agreement → session key → AEAD`。公開鍵は公開できても、その鍵が誰のものかはPKI等で確認する。
### 実装または疑似コード
```text
peer_pk = authenticate(certificate/name)
shared = approved_key_agreement(ephemeral_sk, peer_pk)
keys = HKDF(shared, transcript); use AEAD
```
### よくある誤解
public-keyは「公開だから信頼済み」ではない。RSA/ECという語だけでmode・parameter・validationは決まらない。
### 実務接続
TLS、SSH、age/PGP、KMS envelope、software signingに接続。
### 要点
- pkのbindingを認証。 - hybridを使う。 - 標準scheme。 - key validation。 - forward secrecyを評価。
### 誤解チェック（5問）
1. public keyは真正性を自動保証か。2. 大容量dataを直接処理が普通か。3. encryptionとsignatureは同操作か。4. 長期key漏えいで過去session必ず漏れるか。5. parameter検証不要か。
### 基礎問題（5問）
1. pairを説明せよ。2. hybrid flowを描け。3. binding方法を挙げよ。4. PFSを定義せよ。5. lifecycleを書け。
### 応用問題（3問）
1. MITMを説明せよ。2. key agreement transcriptを論ぜよ。3. rotationを設計せよ。
### 設計問題（1問）
client-side encrypted backupのkey recoveryを設計せよ。
### 調査課題（1問）
採用protocolのapproved cipher suiteと移行計画を調べよ。
### 知らないとする誤判断
公開鍵をAPIから取得した事実だけで所有者bindingも成立したと思う。
### 次章接続
可変長入力を固定長digestへ写すhashを学ぶ。

## 第19章 Hash
### 章を学ぶ理由
integrity、識別、KDF構成要素に必要な性質と非目的を区別する。
### 現場の問題
hashを暗号化、password保存、signature、完全一意IDとして誤用する。
### 中心概念と正式定義
cryptographic hash `H:{0,1}*→{0,1}^n`。preimage、second-preimage、collision resistanceを区別。pigeonholeによりcollisionは必ず存在し、理想n-bit hashのbirthday collision仕事量は概ね `2^(n/2)`。
### 直感→図解→数式→例
`任意長message→n-bit digest`。改ざん者もdigestを書換えられる場所ではhash単独はauthenticityを与えない。content addressingはcollision handlingを含める。
### 実装または疑似コード
```text
digest = approved_hash(domain_separator || canonical_bytes)
compare trusted_expected_digest with constant-time primitive when relevant
```
### よくある誤解
hashは不可逆を数学的に保証するのでなく、preimage探索が計算困難。低entropy入力はdictionaryで戻せる。
### 実務接続
artifact digest、Merkle tree、dedup、Git、integrity manifestに現れる。
### 要点
- 三抵抗性を区別。 - collisionは存在。 - trust anchorが必要。 - canonicalizationを固定。 - passwordには専用KDF。
### 誤解チェック（5問）
1. collisionは存在しないか。2. hash=暗号化か。3. 低entropyも安全か。4. digest同梱だけで改ざん検知か。5. n-bit collision強度は2^nか。
### 基礎問題（5問）
1. 三性質を定義せよ。2. pigeonholeを説明せよ。3. birthday強度を求めよ。4. trust anchorを示せ。5. canonical bytesを定めよ。
### 応用問題（3問）
1. artifact verificationを設計せよ。2. content address衝突を扱え。3. Merkle treeを説明せよ。
### 設計問題（1問）
大規模object storeのintegrity検証とalgorithm migrationを設計せよ。
### 調査課題（1問）
利用systemのhash algorithmとcollision対応を調べよ。
### 知らないとする誤判断
同じ保存場所にfileとhashを置くだけで悪意ある改ざんを検知できると思う。
### 次章接続
共有secretを加えてmessage authenticityを与えるMACへ進む。

## 第20章 MAC
### 章を学ぶ理由
共有keyを持つ当事者間でmessageの完全性と真正性を検証する。
### 現場の問題
`hash(secret||message)`を独自構成し、replay、canonicalization、key分離を忘れる。
### 中心概念と正式定義
MACは `Tag(K,M)→t`、`Verify(K,M,t)`。EUF-CMA等の偽造困難性を目標にし、HMACやAEAD tagなど標準構成を使う。MACは第三者へ誰が生成したかを証明しない。freshnessはnonce/timestamp/sequenceをmessageへ含める。
### 直感→図解→数式→例
`shared K + canonical request → tag`。senderとreceiver双方がKを持つため、どちらもtagを作れる。webhookではmethod/path/body/timeを一つのcanonical messageへ束縛する。
### 実装または疑似コード
```text
m = version||timestamp||nonce||method||path||body_digest
reject stale/reused nonce; verify HMAC with constant-time library
```
### よくある誤解
MACだけでは暗号化・replay防止・non-repudiationを与えない。文字列連結の曖昧性を避ける。
### 実務接続
webhook、API request signing、cookie、storage integrity、key confirmationに現れる。
### 要点
- 標準MAC。 - canonical化。 - contextを束縛。 - freshnessを別設計。 - key用途分離。
### 誤解チェック（5問）
1. MACで秘匿か。2. replay防止を内包か。3. 第三者証明か。4. hash単独で同等か。5. 順序なしfield連結は安全か。
### 基礎問題（5問）
1. APIを定義せよ。2. messageをcanonical化せよ。3. freshnessを追加せよ。4. keyを分離せよ。5. failure処理を書け。
### 応用問題（3問）
1. webhook検証を設計せよ。2. key rotationを行え。3. proxy書換えを扱え。
### 設計問題（1問）
multi-provider webhookのversion付き署名検証を設計せよ。
### 調査課題（1問）
実webhook protocolの署名範囲とreplay対策を調べよ。
### 知らないとする誤判断
正しいMACが一度付いたrequestなら、いつ何回処理しても安全と考える。
### 次章接続
検証者と署名者のkeyを分けるdigital signatureへ進む。

## 第21章 Digital Signature
### 章を学ぶ理由
秘密鍵保持者がmessageを承認したことと改ざんなしを公開検証可能にする。
### 現場の問題
署名対象の曖昧化、algorithm confusion、key失効、replay、署名した意味の過大解釈がある。
### 中心概念と正式定義
`KeyGen→(pk,sk)`, `Sign(sk,m)→σ`, `Verify(pk,m,σ)`。署名はunforgeabilityを目標とし、秘匿しない。署名対象はdomain separation、version、context、canonical encodingを含める。法的non-repudiationはkey custody・本人確認・processも必要。
### 直感→図解→数式→例
`artifact digest+identity+purpose+time --sk→signature --pk→valid/invalid`。validは「このkeyでこのbytesへ署名」と示すが、内容が安全・真実とは示さない。
### 実装または疑似コード
```text
m=canonical(version,purpose,artifact_digest,metadata)
σ=library.sign(sk,m); verify allowed_alg, trusted_pk, m, σ, key_status
```
### よくある誤解
署名検証成功はsigner authorizationやartifact安全性を自動保証しない。signing/decryption keyを兼用しない。
### 実務接続
software release、document、token、certificate、audit checkpointに現れる。
### 要点
- bytesとpurposeを束縛。 - algorithmをallowlist。 - key custodyを守る。 - revocation/timeを扱う。 - 署名の意味を限定。
### 誤解チェック（5問）
1. 署名は秘匿するか。2. validなら内容は安全か。3. key失効後も無条件有効か。4. JSON順序は無関係か。5. MACと第三者検証性は同じか。
### 基礎問題（5問）
1. 三algorithmを定義せよ。2. message範囲を書け。3. canonical化せよ。4. trust keyを示せ。5. failureを処理せよ。
### 応用問題（3問）
1. release signingを設計せよ。2. key compromiseを処理せよ。3. timestampingを論ぜよ。
### 設計問題（1問）
複数承認者が必要な本番release署名を設計せよ。
### 調査課題（1問）
採用署名formatのalgorithm・canonicalization・失効を調べよ。
### 知らないとする誤判断
署名validなartifactを、署名者権限とbuild provenanceを確認せず実行する。
### 次章接続
公開鍵をidentityへ束縛するPKIを扱う。

## 第22章 PKI
### 章を学ぶ理由
公開鍵の所有者、名前、用途、有効期間を信頼anchorから検証する。
### 現場の問題
証明書があるだけでhostname・chain・usage・revocationを確認したと思う。
### 中心概念と正式定義
PKIはCA、RA、certificate、trust store、path validation、revocation、policyのsystem。X.509 certificateはsubject/public key等をissuerが署名。検証はchain、time、name、key usage、policy constraintsを含む。
### 直感→図解→数式→例
`trust anchor→intermediate→leaf(name,key,usage,validity)`。rootを信頼する理由は自己署名でなくtrust storeへの安全な配置。
### 実装または疑似コード
```text
build path to configured anchor; verify every signature+constraint;
match reference identity; check time/usage/status; fail closed
```
### よくある誤解
certificate=暗号化ではない。revocationは常に即時・完全ではなく、短命certificate等と合わせる。
### 実務接続
Web PKI、mTLS、code signing、device identity、private CAに現れる。
### 要点
- anchor配布が信頼根。 - path全体を検証。 - 名前・用途を確認。 - lifecycleを自動化。 - revocation限界を設計。
### 誤解チェック（5問）
1. 自己署名rootは署名ゆえ信頼か。2. chain validならhostname不問か。3. expiryだけ見ればよいか。4. revocationは瞬時か。5. private CAは自動安全か。
### 基礎問題（5問）
1. chainを描け。2. anchorを示せ。3. identity matchを書け。4. usageを確認せよ。5. renewalを設計せよ。
### 応用問題（3問）
1. CA compromiseを分析せよ。2. mTLS identityを設計せよ。3. short-lived certを評価せよ。
### 設計問題（1問）
内部service PKIの発行・更新・失効・監査を設計せよ。
### 調査課題（1問）
利用TLS libraryのpath/hostname validation defaultを調べよ。
### 知らないとする誤判断
private CA署名なので証明書内の任意identity claimを信頼する。
### 次章接続
PKI、key agreement、AEADを組み合わせるTLSへ進む。

## 第23章 TLS
### 章を学ぶ理由
通信路のauthentication・confidentiality・integrityと、その境界外を理解する。
### 現場の問題
certificate検証無効化、TLS終端後平文、token漏えい、0-RTT replay、古いversionを放置する。
### 中心概念と正式定義
TLS 1.3はhandshakeでparameter・peer identity・traffic keyを確立しrecordをAEAD保護する。serverは通常認証、clientは任意。transcript bindingでdowngrade/tamperへ対抗。application authorizationとendpoint侵害は範囲外。
### 直感→図解→数式→例
`client --authenticated handshake--> server; HKDF(shared, transcript)→traffic keys; records→AEAD`。reverse proxy終端はbrowser-proxyだけを保護しproxy-backendを別途設計する。
### 実装または疑似コード
```text
use maintained TLS stack; verify reference identity; require current policy;
protect private keys; automate renewal; inventory every termination hop
```
### よくある誤解
TLSはpayloadをserver処理後も暗号化し続けない。TLS 1.3の0-RTTはreplay可能性を考慮して冪等操作へ限定する。
### 実務接続
HTTPS、service mesh、DB connection、load balancer、certificate monitoringに現れる。
### 要点
- endpoint identity検証。 - 全hopを描く。 - maintained default。 - key/cert lifecycle。 - replay/application層は別。
### 誤解チェック（5問）
1. TLSでserver内dataも保護か。2. encryptionだけで認可か。3. cert検証offでも機密か。4. 0-RTTは任意writeへ安全か。5. proxy後も自動TLSか。
### 基礎問題（5問）
1. handshake目的を列挙せよ。2. endpointを描け。3. identityを検証せよ。4. terminationを探せ。5. renewalを監視せよ。
### 応用問題（3問）
1. mTLSを設計せよ。2. downgrade policyを調べよ。3. 0-RTT適用を判定せよ。
### 設計問題（1問）
internet→CDN→LB→service→DBの各hopを保護せよ。
### 調査課題（1問）
RFC 8446とBCP 195（RFC 9325等）から現行設定を確認せよ。
### 知らないとする誤判断
URLがhttpsなので全経路・保存・認可も安全と結論する。
### 次章接続
TLSの内側で起きるWeb固有のtrust境界を扱う。

## 総合演習C（第12〜23章）
OIDC login、RBAC/ABAC認可、password fallback、session、TLS、webhook MAC、release signature、内部PKIを持つSaaSを設計せよ。factor recovery、JWT issuer/audience、key rotation、replay、certificate expiry、tenant object認可の反例をテストにする。

## 第24章 Web Security
### 章を学ぶ理由
browserのsame-origin、cookie、URL、HTML/JS実行モデルをsecurity境界として理解する。
### 現場の問題
server側Web開発の感覚で、browserがcredentialを自動送信しuntrusted contentを実行する事実を落とす。
### 中心概念と正式定義
originは概ねscheme/host/portの組。Same-Origin Policyはorigin間read等を制限し、CORSはserverが一部を緩和するprotocol。cookie属性Secure/HttpOnly/SameSite、CSP、frame制御、content type、cache policyを組み合わせる。
### 直感→図解→数式→例
`site A page→browser security model→site B request`。CORSはbrowser読取policyでありserver-to-server requestやCSRFを単独で止めない。
### 実装または疑似コード
```text
set secure session cookie; explicit CORS origins/methods/credentials;
contextual output encoding; CSP; no secrets in URL; safe cache headers
```
### よくある誤解
CORSは認証・firewallでない。HttpOnlyはXSSによるsession利用を全て防がず、CSPはencodingの代替でない。
### 実務接続
SPA、BFF、OAuth redirect、third-party script、CDN cacheに現れる。
### 要点
- browserを主体としてモデル化。 - originを理解。 - cookie属性。 - CORSを限定。 - content/cacheを明示。
### 誤解チェック（5問）
1. CORSでserver間request防止か。2. HttpOnlyでXSS無害か。3. SameSiteだけで全CSRF防止か。4. URLへtoken可か。5. CSPでencoding不要か。
### 基礎問題（5問）
1. originを比較せよ。2. cookie属性を選べ。3. preflightを説明せよ。4. cache leakを示せ。5. CSP目的を述べよ。
### 応用問題（3問）
1. SPA authを設計せよ。2. CDN cache keyを監査せよ。3. third-party scriptを隔離せよ。
### 設計問題（1問）
機密dashboardのbrowser security headerとsessionを設計せよ。
### 調査課題（1問）
OWASP ASVS 5.0のWeb要件へ現systemをmappingせよ。
### 知らないとする誤判断
CORS allowlistがあるのでAPI側authorizationを省く。
### 次章接続
入力を別言語のcodeとして解釈させるinjectionを扱う。

## 第25章 Injection
### 章を学ぶ理由
dataと命令の境界が崩れる共通根因をSQL、shell、template、LDAP等へ一般化する。
### 現場の問題
blacklist escaping、文字列連結、二重decode、入力源をformだけと考える。
### 中心概念と正式定義
injectionはuntrusted dataがinterpreterの構文として解釈され、意図しない命令・構造を生むこと。data/code分離、parameterization、allowlisted grammar、least privilegeを使う。validationとoutput encodingはcontext依存。
### 直感→図解→数式→例
`template + untrusted bytes --parse→ unexpected AST`。安全なbindingは値をAST構造から分離する。escapingは対象言語・contextが違えば無効。
### 実装または疑似コード
```python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
# shell=Trueや動的identifierは避け、必要なら固定allowlistから選ぶ
```
### よくある誤解
入力が内部DB・queue・header由来でもuntrusted。stored payloadは後段interpreterで発火する。
### 実務接続
SQLi、command、template、log、formula injectionに現れる。
### 要点
- parser境界を探す。 - parameter化。 - context別encoding。 - grammar allowlist。 - interpreter権限を絞る。
### 誤解チェック（5問）
1. blacklistで完全か。2. ORMなら常に安全か。3. 内部入力はtrustedか。4. escape関数は全context共通か。5. parameterでidentifierも扱えるか。
### 基礎問題（5問）
1. interpreterを列挙せよ。2. 連結箇所を探せ。3. bindingへ直せ。4. allowlistを作れ。5. 権限を縮めよ。
### 応用問題（3問）
1. second-order injectionを分析せよ。2. dynamic sortを安全化せよ。3. log injectionを防げ。
### 設計問題（1問）
利用者定義filter DSLを安全なASTへcompileせよ。
### 調査課題（1問）
利用frameworkのraw query/shell/template escape hatchを監査せよ。
### 知らないとする誤判断
入力validation一回で、後段の異なるinterpreter contextも安全と思う。
### 次章接続
browserのHTML/JS contextへ起こるXSSを掘る。

## 第26章 XSS
### 章を学ぶ理由
untrusted contentが被害者origin権限でscriptとして実行される構造を防ぐ。
### 現場の問題
stored/reflected/DOM XSS、危険sink、framework escape bypass、third-party scriptを見落とす。
### 中心概念と正式定義
XSSはdataがHTML/attribute/URL/JS/CSS contextでexecutable codeとなるinjection。source→transform→sinkを追跡し、contextual encoding、safe DOM API、sanitization（HTMLを許す場合）、CSPを使う。
### 直感→図解→数式→例
`attacker input→stored DB→victim page→innerHTML→origin code execution`。同じ文字列でもtext nodeとscript literalで必要処理が違う。
### 実装または疑似コード
```javascript
element.textContent = untrusted; // innerHTMLではなくtextとして挿入
// HTML許可時は維持された専用sanitizerとTrusted Types等を検討
```
### よくある誤解
HttpOnlyはDOM操作・正規request送信を防がない。CSPは補助層で、unsafe設定や既存gadgetで破れる。
### 実務接続
CMS、markdown、rich text、template、SPA DOM、support toolに現れる。
### 要点
- contextを特定。 - safe sinkを選ぶ。 - encodingを自動化。 - HTML許可はsanitize。 - CSPで被害を制限。
### 誤解チェック（5問）
1. `<script>`だけがXSSか。2. HttpOnlyで全被害なしか。3. URL contextも同じescapeか。4. framework利用でゼロか。5. CSPだけで根治か。
### 基礎問題（5問）
1. sourceを探せ。2. sinkを探せ。3. contextを分類せよ。4. safe APIへ直せ。5. CSP違反を読め。
### 応用問題（3問）
1. markdownを安全化せよ。2. DOM XSSを追跡せよ。3. third-party scriptを隔離せよ。
### 設計問題（1問）
rich-text comment機能の許可要素・sanitization・CSPを設計せよ。
### 調査課題（1問）
利用frontend frameworkのescape bypass APIを監査せよ。
### 知らないとする誤判断
cookieがHttpOnlyなのでXSSはsecurity impactを持たないと考える。
### 次章接続
browserのcredential自動送信を悪用するCSRFへ進む。

## 第27章 CSRF
### 章を学ぶ理由
攻撃siteから被害者browserへ意図しないstate-changing requestを送らせる構造を防ぐ。
### 現場の問題
POST、CORS、Referer、JSONだけで防止したと思い、login CSRFやsubdomainを落とす。
### 中心概念と正式定義
CSRF成立にはbrowserがcredentialを自動付与し、serverがrequestの利用者意図を検証しないことが必要。synchronizer token、double-submitの正しいbinding、SameSite、Origin検証、custom header等をsystem特性に合わせる。
### 直感→図解→数式→例
`attacker page→victim browser(+session cookie)→target state change`。anti-CSRF tokenはattackerが読めないsession/ requestへ結び付ける。
### 実装または疑似コード
```text
for unsafe method: verify session-bound unpredictable token and Origin;
use SameSite cookie; never mutate on GET; reauth high-risk actions
```
### よくある誤解
CORSは単純request送信を止めない。XSSがあれば同origin tokenを取得できるためXSS対策も必要。
### 実務接続
cookie session、admin panel、OAuth redirect、account linkingに現れる。
### 要点
- credential自動付与を確認。 - unsafe methodを守る。 - tokenをsessionへbinding。 - SameSiteを層に。 - high-riskは再確認。
### 誤解チェック（5問）
1. POSTだけで安全か。2. CORSで全送信阻止か。3. SameSiteで全browser/flow安全か。4. GET更新はよいか。5. XSSと独立か。
### 基礎問題（5問）
1. 成立条件を書け。2. flowを描け。3. tokenを設計せよ。4. cookie属性を選べ。5. mutation routeを列挙せよ。
### 応用問題（3問）
1. login CSRFを分析せよ。2. APIとbrowserを分けよ。3. subdomain trustを監査せよ。
### 設計問題（1問）
OAuth account linkingのstate/nonce/CSRF防御を設計せよ。
### 調査課題（1問）
利用frameworkのCSRF middleware適用範囲を調べよ。
### 知らないとする誤判断
JSON APIはHTML formから呼びにくいのでCSRF不可能と断定する。
### 次章接続
server自身を代理にして内部・metadataへ接続させるSSRFを扱う。

## 第28章 SSRF
### 章を学ぶ理由
untrusted URL/hostがserverのnetwork権限とidentityを借りるのを防ぐ。
### 現場の問題
文字列host allowlistだけでredirect、DNS rebinding、IPv6、credential付きURL、別protocolを落とす。
### 中心概念と正式定義
SSRFは攻撃者がserver-side requestの宛先・一部を制御し、通常到達不能なresourceへ接続させる。URL parse→name resolution→IP classification→connect→redirect各段を制約し、egressとdownstream authでも防ぐ。
### 直感→図解→数式→例
`attacker URL→fetcher(service identity)→internal API/cloud metadata`。application validationと実際のconnection先が一致する必要がある。
### 実装または疑似コード
```text
prefer opaque resource IDs; otherwise strict scheme/port allowlist;
resolve then reject private/reserved; pin destination; disable/revalidate redirects;
egress proxy; no ambient credentials
```
### よくある誤解
`localhost`文字列だけ拒否しても数値表現・DNS・IPv6がある。URL parserを自作しない。
### 実務接続
webhook tester、image/PDF fetch、import、proxy、cloud metadataに現れる。
### 要点
- URL入力を避ける。 - parse/resolve/connectを一貫。 - redirect再検証。 - egress制限。 - ambient authorityを除く。
### 誤解チェック（5問）
1. host文字列checkで十分か。2. DNS結果は固定か。3. redirectは同宛先か。4. outbound firewall不要か。5. service credentialは無関係か。
### 基礎問題（5問）
1. flowを描け。2. schemeを限定せよ。3. IP rangeを分類せよ。4. redirect policyを書け。5. egressを設計せよ。
### 応用問題（3問）
1. DNS rebindingを説明せよ。2. metadata accessを防げ。3. blind SSRFを検知せよ。
### 設計問題（1問）
外部URL preview serviceをsandbox/queue/egress込みで設計せよ。
### 調査課題（1問）
cloud metadata serviceの現行防御仕様を一次資料で調べよ。
### 知らないとする誤判断
URLがHTTP形式なのでfile、internal network、redirect先も安全と考える。
### 次章接続
Web境界から、process内のmemory corruptionへ移る。

## 総合演習D（第24〜28章）
URL preview付きrich-text管理画面を題材に、origin/cookie/CORS、SQL injection、stored/DOM XSS、CSRF、SSRFを一つのdata-flowで分析せよ。各脅威にsafe API、browser control、least privilege、egress、検知を割り当て、control共通原因を示せ。

## 第29章 Memory Safety
### 章を学ぶ理由
境界外read/write、use-after-free、data raceが任意code実行へつながる構造を理解する。
### 現場の問題
入力長check追加やcrash抑止で根因を残し、unsafe境界とownershipを管理しない。
### 中心概念と正式定義
spatial safetyはobject境界、temporal safetyはlifetime、type safetyは値解釈、thread safetyは並行access規則を守ること。C/C++の未定義動作、Rustのownership/borrow、managed runtime、sandbox、CFI/ASLR等を層として使う。
### 直感→図解→数式→例
`allocation [0..n) | out-of-bounds`、`free→dangling pointer→reuse`。bounds checkは空間、GCは一部時間安全性を助けるがnative/logic flawを消さない。
### 実装または疑似コード
```rust
fn first(xs: &[u8]) -> Option<u8> { xs.first().copied() }
// unsafeは小境界に隔離し、契約・fuzz・sanitizerで検証
```
### よくある誤解
memory-safe言語でsecurity bugゼロにはならない。ASLR/canaryは根因除去でなくexploit mitigation。
### 実務接続
parser、codec、kernel、FFI、embedded、browser sandboxに現れる。
### 要点
- 空間/時間を区別。 - memory-safe default。 - unsafeを隔離。 - mitigationを重ねる。 - fuzz/sanitizerで境界検証。
### 誤解チェック（5問）
1. crashだけがimpactか。2. GCで全memory safetyか。3. ASLRでbug消滅か。4. Rust unsafe不要か。5. FFIは安全保証内か。
### 基礎問題（5問）
1. bugを分類せよ。2. lifetimeを描け。3. safe APIへ直せ。4. unsafe境界を探せ。5. mitigationを列挙せよ。
### 応用問題（3問）
1. UAFを分析せよ。2. parser fuzzを設計せよ。3. language migrationを評価せよ。
### 設計問題（1問）
untrusted media parserをprocess isolation込みで設計せよ。
### 調査課題（1問）
一memory corruption CVEの根因とmitigation bypassを調べよ。
### 知らないとする誤判断
canaryを有効化したので境界外writeの修正優先度を下げる。
### 次章接続
自分が書かないcode・toolchainの信頼を供給網として扱う。

## 第30章 Supply Chain Security
### 章を学ぶ理由
dependency、build、artifact、publisher、update経路の侵害をend-to-endで抑える。
### 現場の問題
SCA scanだけで、typosquat、maintainer takeover、CI改ざん、署名key窃取、provenance欠落を見ない。
### 中心概念と正式定義
software supply chainはsource→dependency→build→artifact→distribution→deployment。SBOMはcomponent inventory、provenanceは誰が何からどう生成したかのattestation。reproducibility、hermetic build、signature、two-person control、dependency minimizationを組み合わせる。
### 直感→図解→数式→例
`source(commit) + builder(identity,policy) → artifact(digest) + signed provenance → verifier`。署名済みでも侵害builderが悪性artifactを正規署名できるためsource/build policyを検証する。
### 実装または疑似コード
```text
pin dependencies+digests; isolated build; least-privileged CI;
emit SBOM/provenance; sign in protected service; verify policy before deploy
```
### よくある誤解
lockfile、SBOM、署名の一つだけでは安全でない。自動updateと固定versionは別riskを持つ。
### 実務接続
package registry、CI/CD、container image、firmware update、vendor riskに現れる。
### 要点
- chain全体を描く。 - dependencyを減らす。 - buildを隔離。 - provenanceを検証。 - compromise時revoke/rebuild。
### 誤解チェック（5問）
1. SBOMは安全性証明か。2. 署名でbuilder無害か。3. lockfileでpublisher takeover防止か。4. scannerだけで十分か。5. update停止が安全か。
### 基礎問題（5問）
1. chainを描け。2. identitiesを列挙せよ。3. SBOMを生成せよ。4. digestをpinせよ。5. verifier policyを書け。
### 応用問題（3問）
1. maintainer takeoverを分析せよ。2. CI secret theftを防げ。3. rebuild手順を設計せよ。
### 設計問題（1問）
production artifactのsource-to-deploy policyを設計せよ。
### 調査課題（1問）
NIST SSDF 1.1と、2025-12-17公開・2026-08-27時点でDraftのSSDF 1.2、SLSA等を比較し、draftを組織基準へ採用する場合の追随方針も定めよ。
### 知らないとする誤判断
dependency CVEがゼロなら供給網riskもゼロとする。
### 次章接続
credentialとkeyを安全に生成・配布・更新・破棄する。

## 第31章 Secrets Management
### 章を学ぶ理由
secretの平文copy、長期化、過剰scopeを減らし、侵害時に失効できるようにする。
### 現場の問題
Git、image、log、environment、ticketへsecretが複製され、rotationが停止を伴う。
### 中心概念と正式定義
secret lifecycleはgenerate、store、distribute、use、rotate、revoke、destroy、audit。可能ならstatic secretよりworkload identityから短期credentialを発行。envelope encryptionとKMS/HSMはkey hierarchyを作るが利用者認可が核心。
### 直感→図解→数式→例
`workload identity→broker→short-lived scoped credential→resource`。secret managerへ移すだけで、取得権限が全員なら改善しない。
### 実装または疑似コード
```text
authenticate workload; issue scoped short TTL credential;
never log; support overlapping keys; rotate automatically; detect access anomalies
```
### よくある誤解
environment variableはsecret managerではない。暗号化済みsecretと復号権限を同じ広い主体へ与えない。
### 実務接続
DB password、API key、TLS key、CI token、cloud roleに現れる。
### 要点
- staticを減らす。 - 短期・scope。 - copyを追う。 - rotationを無停止化。 - accessを監査。
### 誤解チェック（5問）
1. envなら漏れないか。2. base64で保護か。3. vault移行だけで最小権限か。4. rotationは生成だけか。5. 削除でlog copyも消えるか。
### 基礎問題（5問）
1. inventoryを作れ。2. ownerを置け。3. TTLを決めよ。4. rotate flowを描け。5. leak先を探せ。
### 応用問題（3問）
1. zero-downtime rotationを設計せよ。2. CI secretを除去せよ。3. break-glass keyを扱え。
### 設計問題（1問）
multi-cloud workload identityとsecret brokerを設計せよ。
### 調査課題（1問）
Git history/image/logのsecret exposureを許可範囲で監査せよ。
### 知らないとする誤判断
secretをvaultへ置けば、その取得identity侵害や平文利用時copyも解決すると考える。
### 次章接続
共有責任とcontrol planeを持つcloud securityへ進む。

## 第32章 Cloud Security
### 章を学ぶ理由
APIでprogrammableなinfrastructure、共有責任、identity中心境界を安全に設計する。
### 現場の問題
provider認証取得を自構成の安全性と同一視し、public exposure、IAM、account境界、control plane logを落とす。
### 中心概念と正式定義
shared responsibilityはservice modelごとにprovider/customer責任を分ける。cloud control plane API、IAM、organization/account/project、network、data plane、metadata、managed service設定をboundaryとして扱う。landing zoneとpolicy-as-codeでguardrailを置く。
### 直感→図解→数式→例
`organization→accounts/projects→VPC/services→resources`。account境界はblast radiusとbilling/ownershipを分けるがcross-account trustが新境界になる。
### 実装または疑似コード
```text
deny public by default; federated short-lived admin; org guardrails;
central immutable audit; config drift detection; tested backup outside failure domain
```
### よくある誤解
cloudはproviderが全securityを担当しない。private subnetだけでidentity・egress・data policyは不要にならない。
### 実務接続
IAM、KMS、object storage、serverless、IaC、CSPMに現れる。
### 要点
- 責任境界を確認。 - identity first。 - accountで隔離。 - guardrailをcode化。 - control planeを監視。
### 誤解チェック（5問）
1. provider認証=自設定安全か。2. private subnet=trustedか。3. managed DBでbackup不要か。4. root共有可か。5. region別copyで誤削除耐性か。
### 基礎問題（5問）
1. 責任表を作れ。2. account構造を描け。3. public resourceを探せ。4. IAMを縮めよ。5. logを集約せよ。
### 応用問題（3問）
1. cross-account trustを分析せよ。2. region outageを設計せよ。3. IaC driftを防げ。
### 設計問題（1問）
production landing zoneをidentity、network、log、backup込みで設計せよ。
### 調査課題（1問）
利用cloudの最新shared responsibilityとroot保護を調べよ。
### 知らないとする誤判断
managed serviceなのでcustomer側identity・data・network設定ミスは起こらないと思う。
### 次章接続
cloud上でprocess隔離を提供するcontainerの境界を検証する。

## 第33章 Container Security
### 章を学ぶ理由
image供給網、host kernel共有、runtime privilege、orchestrator control planeを一体で守る。
### 現場の問題
containerをVM境界とみなし、root、host mount、privileged、image tag、cluster secretを放置する。
### 中心概念と正式定義
containerはnamespace/cgroup等でprocessを隔離するが通常host kernelを共有。image、registry、runtime、host、orchestrator、workload identityを別boundaryとして扱う。seccomp、capabilities、LSM、read-only FS、user namespace等で縮小する。
### 直感→図解→数式→例
`signed image→admission→pod(identity,policy)→shared kernel→node`。privileged/hostPathは隔離を大きく弱める。
### 実装または疑似コード
```text
pin image digest; run non-root; drop all capabilities then add minimum;
read-only FS; no host mounts; seccomp; resource limits; network policy
```
### よくある誤解
image scanでruntime安全は決まらない。non-rootだけでもkernel exploit・service account過権限は残る。
### 実務接続
Kubernetes、CI runner、multi-tenant cluster、sidecar、admission policyに現れる。
### 要点
- kernel共有を認識。 - image provenance。 - runtime権限削減。 - workload identity最小化。 - node/control plane隔離。
### 誤解チェック（5問）
1. container=VMか。2. non-rootで十分か。3. latest tagはimmutableか。4. resource limitはsecurityか。5. cluster内networkはtrustedか。
### 基礎問題（5問）
1. boundariesを描け。2. capabilitiesを削れ。3. mountを監査せよ。4. digestをpinせよ。5. identityを確認せよ。
### 応用問題（3問）
1. escape影響を制限せよ。2. admission policyを設計せよ。3. multi-tenancyを評価せよ。
### 設計問題（1問）
untrusted build jobの隔離基盤をcontainer/VM選択込みで設計せよ。
### 調査課題（1問）
利用orchestratorのpod security標準とruntime profileを調べよ。
### 知らないとする誤判断
namespaceが別なのでhost kernel・node identity・network policyを検討しない。
### 次章接続
予防を破る活動を観測し判断するlogging/detectionへ進む。

## 総合演習E（第29〜33章）
native image parserをcontainer化してcloudで提供するpipelineを設計せよ。memory-safe rewrite優先度、unsafe sandbox、dependency provenance、signing、secretless build、cloud account、runtime capability、egress、node compromiseの検知・回復までattack pathで示せ。

## 第34章 LoggingとDetection
### 章を学ぶ理由
侵害を完全予防できない前提で、判断に必要な高品質eventと検出logicを作る。
### 現場の問題
全log収集で安心し、identity、decision、time、integrity、retention、alert responseを設計しない。
### 中心概念と正式定義
security eventは誰が何をどのresourceへどの結果で行ったかを相関可能に記録。detectionは観測Oから仮説Hを判定しfalse positive/negative、base rate、latency、coverageを持つ。secret/PII最小化とtamper resistanceが必要。
### 直感→図解→数式→例
`sources→normalize→correlate→rule/model→alert→triage→case`。precision=`TP/(TP+FP)`、recall=`TP/(TP+FN)`。低base-rateでは高精度ruleでもFPが支配し得る。
### 実装または疑似コード
```text
log event_id,time,actor,auth_context,action,resource,decision,result,trace,source
centralize append-only; detect; test with known scenarios; assign owner/runbook
```
### よくある誤解
log量はcoverageでない。password/token/bodyを無差別に記録すると新しい漏えい面になる。
### 実務接続
SIEM、audit、EDR、cloud trail、fraud、SLOに接続。
### 要点
- detection use caseからlog設計。 - identity/decisionを記録。 - 機密を最小化。 - integrity/timeを守る。 - alertを演習。
### 誤解チェック（5問）
1. log全量で検知完成か。2. FPゼロが最善か。3. secret記録は調査に有利か。4. alertにowner不要か。5. timestampだけで順序確定か。
### 基礎問題（5問）
1. event schemaを書け。2. use caseを定義せよ。3. precisionを計算せよ。4. sensitive fieldを除け。5. retentionを決めよ。
### 応用問題（3問）
1. account takeover ruleを設計せよ。2. canary eventを作れ。3. log tamperを検知せよ。
### 設計問題（1問）
tenant越境試行のend-to-end detectionとrunbookを設計せよ。
### 調査課題（1問）
過去incidentを現logで検知可能かgap分析せよ。
### 知らないとする誤判断
収集TB数を検知能力とみなし、必要eventの欠落を見ない。
### 次章接続
検知した疑いを封じ、根絶し、回復し、学習するincident responseへ進む。

## 第35章 Incident Response
### 章を学ぶ理由
不確実・時間制約下で影響を限定し証拠を守り安全に回復する。
### 現場の問題
即reimage、即公表、即遮断の単一反応で証拠・可用性・法務要件を壊す。
### 中心概念と正式定義
IRは準備、検知/分析、封じ込め、根絶、回復、改善をrisk管理全体へ統合する。incident severity、commander、technical/legal/privacy/comms役割、evidence chain of custody、decision logを定義する。
### 直感→図解→数式→例
`signal→triage→scope→contain→eradicate→recover→learn`。containmentはcredential revoke、network隔離、機能停止等から事業impactと攻撃継続を比較する。
### 実装または疑似コード
```text
preserve evidence; establish timeline/scope; rotate clean-root credentials;
contain with explicit risk; rebuild from trusted source; validate; monitor recurrence
```
### よくある誤解
containmentと根絶、復旧と安全確認は別。侵害環境内でcredential rotationすると再窃取され得る。
### 実務接続
on-call、forensics、breach notification、BCP、postmortemに現れる。
### 要点
- 準備が速度を決める。 - commandを一本化。 - 証拠を保全。 - clean rootから回復。 - 学習をcontrolへ固定。
### 誤解チェック（5問）
1. rebootで根絶か。2. 最初のalertが全scopeか。3. 侵害hostでkey再発行可か。4. IRはsecurity teamだけか。5. 復旧で終了か。
### 基礎問題（5問）
1. 役割を割当てよ。2. severityを定めよ。3. evidenceを列挙せよ。4. containmentを比較せよ。5. recovery criteriaを書け。
### 応用問題（3問）
1. token theftを対応せよ。2. supply-chain incidentをscopeせよ。3. ransomware復旧を設計せよ。
### 設計問題（1問）
cloud admin key compromise tabletopを作成せよ。
### 調査課題（1問）
NIST SP 800-61 Rev.3を自runbookへmappingせよ。
### 知らないとする誤判断
侵害nodeを消すことを優先し、scope判定と再侵入根因の証拠を失う。
### 次章接続
局所controlをsystem全体のsecurity architectureへ統合する。

## 第36章 Security Architecture
### 章を学ぶ理由
security propertyをboundary、identity、data、control、evidenceの構造へ固定する。
### 現場の問題
個別tool導入が重なり、control gap、重複、common failure、owner不在が生じる。
### 中心概念と正式定義
security architectureはbusiness objectiveからsecurity invariantを導き、zone/boundary、identity、data flow、control plane、key、logging、recoveryへ割り当てる。reference architectureとassurance caseでclaim→argument→evidenceを追う。
### 直感→図解→数式→例
`objective→invariant→threat→control→verification→runtime evidence`。preventだけでなくdetect/respond/recoverを同じattack pathへ置く。
### 実装または疑似コード
```text
for invariant: owners; boundaries; enforcement points; dependencies;
tests; telemetry; failure mode; recovery; exception expiry
```
### よくある誤解
architecture diagramのnetwork boxだけではidentity・data lifecycle・operator pathが見えない。zero trust製品導入はarchitecture完成でない。
### 実務接続
platform engineering、landing zone、reference service、paved road、ADRに現れる。
### 要点
- objectiveから導く。 - invariantを配置。 - common causeを探す。 - evidenceを接続。 - exceptionを期限化。
### 誤解チェック（5問）
1. tool一覧=architectureか。2. networkだけ描けばよいか。3. control owner不要か。4. recoveryは外部か。5. referenceは例外不要か。
### 基礎問題（5問）
1. invariantを書け。2. PEPを配置せよ。3. dependencyを描け。4. evidenceを選べ。5. exceptionを記録せよ。
### 応用問題（3問）
1. common IdP failureを分析せよ。2. platform guardrailを設計せよ。3. assurance caseを作れ。
### 設計問題（1問）
multi-tenant analytics platformのsecurity architectureを設計せよ。
### 調査課題（1問）
現行architectureのcontrol-to-evidence traceabilityを監査せよ。
### 知らないとする誤判断
security製品を増やしたので、control間の依存と失敗時経路を確認しない。
### 次章接続
security controlがavailabilityを壊す場合の判断原則を扱う。

## 第37章 安全性と可用性のトレードオフ
### 章を学ぶ理由
fail-open/fail-closed、rate limit、key loss、緊急accessをriskに応じて設計する。
### 現場の問題
「securityのため停止」または「availabilityのため全許可」の二択になる。
### 中心概念と正式定義
control dependency故障時のpolicyを操作・asset・時間で分ける。fail-closedは不正許可を防ぐがdenialを生み、fail-openはサービスを保つがpolicy違反を許す。degraded mode、cached decisionの最大年齢、break-glass、graceful recoveryを定義する。
### 直感→図解→数式→例
`PDP unavailable→{deny, cached limited permit, emergency local operation}`。閲覧と送金、一般利用者と医療緊急者で選択を変える。
### 実装または疑似コード
```text
classify operation impact; precompute degraded policy; bound duration/scope;
require explicit activation; log immutably; reconcile and review afterward
```
### よくある誤解
全操作同一failure policyは不要。break-glassが通常経路化すればcontrolを無効化する。
### 実務接続
IdP outage、KMS outage、WAF failure、emergency healthcare、DDoS防御に現れる。
### 要点
- 操作別に判断。 - degraded modeを事前設計。 - 時間/scopeを制限。 - break-glassを監査。 - 復旧後reconcile。
### 誤解チェック（5問）
1. fail-closedは常に最善か。2. cacheは無期限可か。3. emergency access不要か。4. availabilityはsecurity外か。5. break-glass共有passwordでよいか。
### 基礎問題（5問）
1. 操作を分類せよ。2. failureを列挙せよ。3. modeを選べ。4. TTLを決めよ。5. reconcileを書け。
### 応用問題（3問）
1. IdP outageを設計せよ。2. KMS outageを扱え。3. DDoS false positiveを論ぜよ。
### 設計問題（1問）
病院systemの通常・災害・侵害時accessを設計せよ。
### 調査課題（1問）
既存control plane outage時の実挙動を演習せよ。
### 知らないとする誤判断
availabilityを守る名目で、範囲・時間・監査なしのbypassを常設する。
### 次章接続
複数control failureがどう事故へ連鎖するか事例で分析する。

## 第38章 セキュリティ事故ケーススタディ
### 章を学ぶ理由
単一脆弱性ではなく、潜在条件・侵入・横展開・検知遅延・回復の因果鎖を読む。
### 現場の問題
「人為ミス」「patch漏れ」で終え、architectureとprocessの再発構造を残す。
### 中心概念と正式定義
事故をtimeline、attack path、control expected/actual、decision context、latent conditionへ分解する。root causeは一個に固定せず、必要条件・増幅器・検知gapを因果graph化する。
### 直感→図解→数式→例
ケース: CI token窃取→過剰cloud role→artifact改ざん→署名→監視対象外registry→deploy。initial accessだけpatchしてもprivilege/provenance/detectionが残る。
### 実装または疑似コード
```text
evidence timeline → competing hypotheses → attack graph → failed assumptions
→ countermeasures ordered by causal leverage → verification owner/date
```
### よくある誤解
hindsightで当時の不確実性を消さない。個人責任化はsystem改善を妨げるが、accountability不要という意味でもない。
### 実務接続
postmortem、audit、risk register、roadmap、tabletopに使う。
### 要点
- 証拠timeline。 - 仮説を競合。 - 必要条件と増幅器を分ける。 - control期待/実際を比較。 - 対策を検証する。
### 誤解チェック（5問）
1. 最初の侵入口だけがrootか。2. 人為ミスで分析終了か。3. 全対策を同優先度か。4. 公開情報で断定可か。5. 再発防止にowner不要か。
### 基礎問題（5問）
1. timelineを作れ。2. 仮説を3つ置け。3. control gapを示せ。4. latent conditionを挙げよ。5. evidence不足を書け。
### 応用問題（3問）
1. supply-chain事故を分析せよ。2. credential theft事故を分析せよ。3. detection delay影響を算定せよ。
### 設計問題（1問）
ケースのcountermeasureを仮説優先度・検証証拠付きで設計せよ。
### 調査課題（1問）
一次情報のある公開incidentを一件因果graph化せよ。
### 知らないとする誤判断
最後に変更した担当者の注意不足を唯一原因とし、過剰権限と検知不能性を残す。
### 次章接続
全領域を一つのthreat modeling演習へ統合する。

## 第39章 Threat Modeling総合演習
### 章を学ぶ理由
assetから回復までを一つの検証可能なsecurity設計へ統合する。
### 現場の問題
認証、暗号、cloud、loggingが個別最適で、system-level invariantへ追跡できない。
### 中心概念と正式定義
題材はcode実行型AI/データ分析SaaS。成果物を `Scope, Assets, Actors, DFD, Boundaries, Invariants, Threats, Risks, Controls, Tests, Telemetry, IR` とする。各riskはownerとresidual acceptanceを持つ。
### 直感→図解→数式→例
`browser→API→job queue→untrusted worker→object store`, `CI→registry→cluster`。不変条件はtenant隔離、workerのhost非到達、artifact provenance、secret非注入、監査欠落なし。
### 実装または疑似コード
```text
enumerate abuse cases; build attack trees; map preventive/detective/recovery controls;
write negative tests and failure injection; record assumptions and expiry
```
### よくある誤解
diagramを精緻化し続けてもverificationがなければ保証は増えない。範囲外は安全ではなく依存として記録する。
### 実務接続
architecture gate、penetration test、red team、SLO、DR、release policyを統合する。
### 要点
- invariant中心。 - actor能力を明記。 - 全boundaryを追う。 - controlをtest/telemetryへ結ぶ。 - residual riskを承認。
### 誤解チェック（5問）
1. 範囲外=無関係か。2. threat一覧で完了か。3. penetration test=証明か。4. ownerなしrisk可か。5. recoveryは後付けか。
### 基礎問題（5問）
1. assetを列挙せよ。2. DFDを描け。3. invariantを書け。4. threatを挙げよ。5. control/testを結べ。
### 応用問題（3問）
1. worker escape pathを分析せよ。2. model exfiltrationを防げ。3. supply-chain侵害を検知せよ。
### 設計問題（1問）
上記SaaSの完全なthreat modelと90日改善roadmapを作れ。
### 調査課題（1問）
red-team/tabletopで仮説を反証しmodelを更新せよ。
### 知らないとする誤判断
control欄が埋まったので、bypass・common cause・運用時failureを試験しない。
### 次章接続
最後に繰り返し現れる誤判断を仮説とcountermeasureの形で整理する。

## 第40章 この分野を知らないエンジニアが陥りやすい誤判断
### 章を学ぶ理由
症状別patchでなく、暗黙の誤仮説を識別し構造的countermeasureへ変える。
### 現場の問題
security reviewが脆弱性名のcheckboxとなり、資産・境界・権限・証拠・回復が抜ける。
### 中心概念と正式定義
優先度は一般的な発生可能性と影響、attack path上の因果レバレッジで並べる。各項目は「Countermeasure: 作業（assumed cause）」で比較可能にする。
### 直感→図解→数式→例
`誤仮説→危険な設計→attack path→反証→根本対策`。対策採用前にsystem固有の証拠で仮説を確認する。
### 実装または疑似コード
```text
for decision: state assumed cause; collect disconfirming evidence;
prefer remove/isolate/minimize over exception; bind control to test+telemetry+owner
```
### よくある誤解
以下の順序は万能でない。systemのasset、actor、failure modelで再優先化する。
### 誤判断カタログ（優先度順、25例）
1. **Countermeasure: server側でobject/actionごとに認可する**（認証済み・UI非表示なら許可済みという想定原因）。
2. **Countermeasure: tenant分離をDB制約・policy・negative testへ固定する**（全queryに担当者がtenant filterを書くという想定原因）。
3. **Countermeasure: secretを短期workload identityへ置換し漏えいcopyを失効する**（vaultへ置けば利用時も漏れないという想定原因）。
4. **Countermeasure: parameter bindingとsafe sinkでdata/codeを構造分離する**（入力blacklistで全interpreter contextを覆えるという想定原因）。
5. **Countermeasure: memory-safe実装またはunsafe parser隔離へ移行する**（canary/ASLRがmemory bugを除去するという想定原因）。
6. **Countermeasure: CI権限最小化とsource-to-artifact provenance検証を導入する**（署名済みartifactならbuildも正当という想定原因）。
7. **Countermeasure: account recoveryを主認証同等にthreat modelする**（MFAがあれば弱いrecoveryは利用されないという想定原因）。
8. **Countermeasure: passwordは最新のmemory-hard KDFと一意saltで保存する**（高速hash+saltでoffline攻撃を抑えられるという想定原因）。
9. **Countermeasure: TLS全hopでidentity検証し終端後の境界を再設計する**（https表示が全経路・保存・認可を守るという想定原因）。
10. **Countermeasure: URL fetchをopaque ID化しresolve/connect/redirectとegressを拘束する**（host文字列allowlistでSSRFを防げるという想定原因）。
11. **Countermeasure: context別encoding/safe DOM APIとCSPを重ねる**（HttpOnlyまたはframeworkがXSS impactを消すという想定原因）。
12. **Countermeasure: session-bound CSRF token・Origin・SameSiteを組み合わせる**（POST/JSON/CORSだけで利用者意図を証明できるという想定原因）。
13. **Countermeasure: key生成・nonce・用途分離・rotationを高水準library契約で管理する**（強いalgorithm名がcrypto compositionミスを相殺するという想定原因）。
14. **Countermeasure: hash/MAC/signatureの目的を分けtrust anchorとfreshnessを設計する**（digest/署名validが安全な内容・replay不可能性も示すという想定原因）。
15. **Countermeasure: public/internal全interactionをattack surface inventoryへ入れる**（VPC・cluster内はtrustedという想定原因）。
16. **Countermeasure: task・resource・timeで権限差分を最小化する**（業務継続には共有adminが必要という想定原因）。
17. **Countermeasure: 異種controlと検知・回復をattack pathへ配置する**（WAF/MFA/EDRの一製品が万能境界という想定原因）。
18. **Countermeasure: logをdetection use caseから設計しsecretを除きalertを演習する**（収集量が検知coverageという想定原因）。
19. **Countermeasure: clean rootからcredentialを更新しscope確認後に復旧する**（侵害nodeのrebootが根絶という想定原因）。
20. **Countermeasure: backupを別failure domain・別identityで保持しrestoreを演習する**（replica/backup job成功が回復可能性を証明するという想定原因）。
21. **Countermeasure: cloud共有責任をservice別に割当てorg guardrailで強制する**（managed serviceのsecurityはprovider責任だけという想定原因）。
22. **Countermeasure: containerのkernel共有を前提にcapability・mount・identityを削る**（containerがVM相当境界という想定原因）。
23. **Countermeasure: fail-open/closedを操作別に時間・scope付きdegraded modeとして定義する**（安全性と可用性は全systemで一律二択という想定原因）。
24. **Countermeasure: incidentを必要条件・増幅器・検知gapの因果graphで分析する**（最後の担当者のミスが唯一root causeという想定原因）。
25. **Countermeasure: threat modelをarchitecture差分ごとにtest・telemetryへ更新する**（年一回の文書作成が継続保証という想定原因）。
### 実務接続
design review、security exception、release gate、incident、DR、roadmapで、該当仮説を証拠付きで選ぶ。
### 要点
- 目的・asset・actorから始める。 - boundaryで検証。 - 権限とsurfaceを最小化。 - 予防だけでなく検知回復。 - controlをtestとownerへ結ぶ。
### 誤解チェック（5問）
1. TLSで認可も完了か。2. 署名validならartifact安全か。3. VPC内はtrustedか。4. vaultでsecret問題完了か。5. backup成功=restore成功か。
### 基礎問題（5問）
1. 自systemで5仮説を選べ。2. 反証証拠を書け。3. attack pathを描け。4. root countermeasureを選べ。5. owner/testを置け。
### 応用問題（3問）
1. 過去incidentを25例へ対応付けよ。2. 共通原因で三controlが破る例を作れ。3. 対策のresidual riskを評価せよ。
### 設計問題（1問）
security review templateをassumed cause、反証、invariant、control、test、telemetry、ownerで設計せよ。
### 調査課題（1問）
OWASP Top 10:2025と本カタログの根因・検証可能性を比較せよ。
### 知らないとする誤判断
このカタログを新しいcheckboxにし、system固有のactor能力と証拠を検討しない。
### 次章接続
本書の思考モデルをsoftware engineering、OS、network、DB、HCIへ持ち込み、securityを分離された工程にしない。

## 参考文献・一次資料（2026-08-27確認）

- [NIST Cybersecurity Framework 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final)
- [NIST SP 800-63-4 Digital Identity Guidelines（Final, 2025）](https://csrc.nist.gov/pubs/sp/800/63/4/final)
- [NIST SP 800-61 Rev.3 Incident Response（Final, 2025）](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-218 SSDF 1.1（Final）](https://csrc.nist.gov/pubs/sp/800/218/final) および [NIST SSDF Publications](https://csrc.nist.gov/Projects/ssdf/publications)（SP 800-218 Rev.1 / SSDF 1.2は2025-12-17公開、2026-08-27時点Draft。採用時にstatusを再確認する）。
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [RFC 9325 / BCP 195: Secure Use of TLS and DTLS](https://www.rfc-editor.org/rfc/rfc9325)
- [RFC 9106: Argon2](https://www.rfc-editor.org/rfc/rfc9106)
- [RFC 8725: JWT Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725)
- [RFC 9700 / BCP 240: OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700)
- [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Top 10:2025](https://owasp.org/Top10/)
- [CISA Secure by Design](https://www.cisa.gov/securebydesign)
- Ross Anderson, *Security Engineering*; Adam Shostack, *Threat Modeling*; Saltzer and Schroeder, “The Protection of Information in Computer Systems.”

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **securityは能力を持つ相手とのsystem game:** 脅威は脆弱性名の一覧ではなく、asset、actorの能力と目的、attack path、守る不変条件の組合せで決まる。攻撃者は防御側の想定経路に従わず、最も安い連鎖と正規機能の悪用を選ぶ。実務ではcontrolから始めず、誰が何へ到達できれば何が破れるかを置き、仮定が変わるたびにthreat modelを更新する。
2. **すべてのtrust boundaryで再検証する:** identityや入力の信頼は一度の認証でsystem全体へ伝播せず、process、tenant、network、cloud account、CI、運用者などの境界ごとに意味が変わる。正式には各boundaryでprincipal、object、action、contextを結び直し、dataとcodeを構造的に分離する。実務では「内部」「署名済み」「認証済み」を許可の根拠にせず、server側認可、provenance、safe sink、egress制御へ落とす。
3. **権限とattack surfaceは使う時・場所・量まで最小化する:** least privilegeはrole名を細かくするだけでなく、到達可能な対象、操作、期間、実行環境、delegationを削る設計原理である。権限を持たないcomponentは、その脆弱性が侵害されても該当能力を攻撃者へ渡せない。実務では共有adminや長期secretを、短期identity、task別権限、isolation、不要機能の削除へ置換する。
4. **controlはattack path上の独立した障壁として評価する:** control数ではなく、どの前提でどの辺を切り、bypassや共通原因があるかが防御の強さを決める。予防・検知・封じ込め・回復を異種の仕組みで重ね、各controlをnegative test、telemetry、ownerへ結ぶ。実務ではMFA、WAF、EDRなどの製品名を保証とせず、一つを破った後の到達可能性と検知時間を演習する。
5. **侵害と失敗を前提に証拠と回復可能性を設計する:** 完全予防は保証できないため、侵害範囲を限定し、信頼できる証拠から判定し、clean rootへ戻る能力が必要になる。復旧はrebootやbackup保有ではなく、credential更新、provenance確認、別failure domainからのrestore、再侵入検知を含む検証済み手続きである。実務ではdetection use case、改ざん耐性のあるlog、IR権限、restore/tabletopを平時のarchitectureに組み込む。

### 専門家の意見が根本的に分かれる3つの論点

1. **限られた資源を予防へ集中するか、検知・封じ込め・回復へ厚く配るか。** **立場A（予防優先）の最も強い主張:** exploit可能な経路や過剰権限を構造から除けば事故そのものとblast radiusを減らせ、常時対応要員に依存する検知より確実である。**立場B（resilience優先）の最も強い主張:** 未知の脆弱性、正規credential悪用、supply-chain侵害を完全には防げず、早期検知とclean recoveryがなければ一度の突破が長期・全社侵害になる。判断はasset価値、攻撃者能力、attack surfaceを除去できる度合い、検知可能性、response staffing、許容dwell timeとRTOによって変わる。
2. **組織共通の強制guardrailを中央集約するか、各teamへsecurity判断を委ねるか。** **立場A（中央guardrail）の最も強い主張:** identity、artifact provenance、logging、tenant分離のような横断不変条件は、任意遵守では必ず抜けるため、platformとpolicyで一貫して強制すべきである。**立場B（teamの局所自律）の最も強い主張:** 脅威と業務制約を最も理解するのは所有teamであり、画一的controlは誤った境界、例外の常態化、delivery停滞を生みうる。判断は、共通不変条件を機械検査できるか、teamの専門性、変更速度、service間blast radius、例外の期限と観測性によって変わる。
3. **障害時にfail-closedを貫くか、制限付きdegraded modeを許すか。** **立場A（fail-closed）の最も強い主張:** 認可・key・監査など信頼根拠を確認できない状態で処理を続けると、可用性障害を機密性・完全性侵害へ不可逆に拡大する。**立場B（risk-calibrated availability）の最も強い主張:** 医療・安全・基幹運用では停止自体が最大の損害になり、低権限・短時間・限定scope・後日照合という縮退処理の方が総riskを下げる場合がある。判断は操作の可逆性、asset、停止損失、offlineで検証できる情報、縮退権限のscopeと期限、後続監査・reconciliationの確実性によって変わる。

### 深い理解と暗記を見分ける10の質問

1. 強いMFAを導入済みなのにaccount takeoverが起こるattack pathを、recovery、session、OAuth委任、support運用の少なくとも二つを使って構成し、根本controlを選べ。
2. 「VPC内通信は信頼する」という設計を、侵害済みworkloadと過剰service identityを仮定して評価せよ。どのboundaryで何を再検証し、何をnetworkだけでは保証できないか説明せよ。
3. 署名検証に成功したartifactが悪性である二つの異なる原因を挙げよ。sourceからbuild、署名、registry、deployまで、必要なprovenanceと権限分離を設計せよ。
4. 三つのsecurity製品が同じidentity providerまたは管理planeへ依存し、同時に無効化される例を作れ。controlの独立性をどの証拠と演習で評価するか述べよ。
5. URL allowlistだけのSSRF対策を、名前解決変更、redirect、複数表記、接続先検証の観点から破る思考実験をせよ。特殊caseのblacklistでなく構造的にsurfaceを除く案を示せ。
6. auth service停止時の処理を、送金、医療記録閲覧、公開記事閲覧の三操作で別々に決めよ。各degraded modeの権限、期限、記録、reconciliationと停止条件を説明せよ。
7. secret managerを導入してもsecret漏えいriskが残る経路を、取得時、memory、log、権限委任、rotationから三つ選んで示し、長期secret自体を減らす設計へ直せ。
8. 大量のlogを収集しているのに侵害を検知できないsystemを構成せよ。検知したいattack pathから必要なevent、相関、欠落検知、alertの応答責任を逆算せよ。
9. backup jobが毎日成功しているsystemで、ransomware後に復旧不能となる反例を作れ。failure domain、identity、保持、復号key、restore test、clean rootの各仮定を検査せよ。
10. 侵入口となった一つの脆弱性をpatchした後も重大riskが残るincidentを分析せよ。必要条件、増幅器、検知gapを分離し、countermeasureを因果レバレッジと反証可能な完了条件で優先付けよ。
