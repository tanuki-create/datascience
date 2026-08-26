# データベース理論――状態・整合性・並行性を設計する

SQLの書き方ではなく、データモデル、制約、実行、並行履歴、故障回復、分散配置を一貫したモデルで学ぶ。製品の既定値は変わるため、2026-08-27時点の公式文書も参照しつつ、永続する原理を中心にする。

**関連巻:** 関係・関数・証明の記法は [離散数学](02_discrete_math.md)、indexとplanの費用は [アルゴリズムと計算量](01_algorithms.md)、lock・MVCC・WALの下層は [オペレーティングシステム](05_operating_systems.md)、複製・合意・partial failureは [並行・並列・分散システム](06_concurrency_distributed.md)、権限と暗号化は [情報セキュリティ](11_security.md) を参照する。

## 第1章 DBは何を解決する装置なのか
### 章を学ぶ理由
DBを「保存先」でなく、複数主体が共有状態を安全かつ効率的に更新する装置として捉える。
### 現場の問題
アプリ内チェックとファイル保存だけでは、同時更新、クラッシュ、検索、制約、監査を一体で扱えない。
### 中心概念と正式定義
DBMSは論理データ、制約、問い合わせ、トランザクション、永続化、回復を提供する。状態Dが制約集合Cを満たすことを `D⊨C` と書く。正しい更新Tは `D⊨C ⇒ T(D)⊨C` を保つ。
### 直感→図解→数式→例
`利用者群 → DBMS〔制約・並行制御・ログ〕→ storage`。銀行残高の和を一定にする送金は二行更新を一単位にする。可用性、レイテンシ、整合性は同時に無限には得られない。
### 実装または疑似コード
```sql
BEGIN; UPDATE accounts SET balance=balance-100 WHERE id=1;
UPDATE accounts SET balance=balance+100 WHERE id=2; COMMIT;
```
### よくある誤解
DBは無条件に整合性を保証しない。schema、制約、分離レベル、故障モデルを設計して初めて必要な保証になる。
### 実務接続
決済、在庫、監査ログ、設定管理、ジョブキューの共有状態に現れる。
### 要点
- DBMSは共有状態の規則を実行する。 - 論理と物理を分離する。 - 制約はDB状態の述語である。 - 並行履歴も正しさの対象である。 - 故障回復を正常系と同時に設計する。
### 誤解チェック（5問）
1. DBは単なるファイルか。2. アプリ検証だけで全writerを拘束できるか。3. COMMIT応答前後の故障は同じか。4. 永続化はbackupと同義か。5. 制約なしでも業務整合性は自動保証か。
### 基礎問題（5問）
1. 状態と制約を書け。2. writerを列挙せよ。3. 原子的単位を定めよ。4. 故障を3種挙げよ。5. 論理・物理を分けよ。
### 応用問題（3問）
1. 二重予約の不変条件を示せ。2. file保存との差を論ぜよ。3. queueをDBで実装する保証を列挙せよ。
### 設計問題（1問）
口座振替の状態、制約、並行性、回復目標を設計せよ。
### 調査課題（1問）
利用DBのdurability設定を公式文書で調べよ。
### 知らないとする誤判断
「DBを使った」ことを「業務不変条件を保証した」ことと同一視する。
### 次章接続
何をデータとして表せるかを決めるデータモデルへ進む。

## 第2章 Data Model
### 章を学ぶ理由
現実をどの構造・操作・制約へ写すかが、クエリと変更可能性を決める。
### 現場の問題
JSON、表、グラフを製品機能として選び、問い合わせと不変条件への適合を検討しない。
### 中心概念と正式定義
データモデルは構造S、演算O、制約Cの組 `M=(S,O,C)`。概念モデル、論理モデル、物理モデルを区別する。schemaは許される状態集合、instanceはその一状態。
### 直感→図解→数式→例
`現実 → 概念(注文/顧客) → 論理(関係/文書) → 物理(page/index)`。同じ注文を関係行または集約文書にできるが、跨ぐ制約の表現力が違う。
### 実装または疑似コード
```text
Entity Order(id, customer, items)
Constraint: total(Order)=Σ item.price*item.qty
Queries: customer履歴、期間売上、単一注文取得
```
### よくある誤解
現実に「自然な」唯一のschemaはない。アクセスパターンだけでも不変条件だけでも不十分である。
### 実務接続
RDB、document store、graph DB、event log、分析warehouseの選択に直結する。
### 要点
- modelは構造・演算・制約の組。 - schemaとinstanceを分ける。 - 概念・論理・物理を分ける。 - 捨象を記録する。 - 変更と問い合わせで評価する。
### 誤解チェック（5問）
1. schemaは現在の行集合か。2. 物理indexは概念モデルか。3. modelは値の形だけか。4. JSONならschema不要か。5. 一業務に唯一の正解modelがあるか。
### 基礎問題（5問）
1. 三層を例示せよ。2. 構造を定義せよ。3. 演算を列挙せよ。4. 制約を書け。5. 捨象を挙げよ。
### 応用問題（3問）
1. 注文を関係と文書で比較せよ。2. 時系列をmodel化せよ。3. schema evolutionを論ぜよ。
### 設計問題（1問）
IoT計測値の保持・集約・訂正をmodel設計せよ。
### 調査課題（1問）
利用DBの論理型と物理格納の差を調べよ。
### 知らないとする誤判断
データ形式が同じなら制約・演算能力も同じと考える。
### 次章接続
最も重要な論理モデルの一つ、関係モデルを定義する。

## 第3章 Relational Model
### 章を学ぶ理由
表の見た目でなく、関係・属性・候補キー・制約としてRDBを理解する。
### 現場の問題
行番号、格納順、NULL、重複を数学的関係の性質と混同する。
### 中心概念と正式定義
関係schema `R(A1:D1,…,An:Dn)` のinstanceは直積 `D1×…×Dn` の有限部分集合。tupleは属性→値の写像。superkey KはK値がtupleを一意化し、最小superkeyがcandidate key。純粋な関係モデルの参照整合性は、参照元の外部キー値が参照先候補キーに存在する制約である。SQLではNULLと`MATCH`方式が加わり、既定の`MATCH SIMPLE`は複合外部キーの一列でもNULLならその行の参照検査を要求しない。この差をDDLごとに確認する。
### 直感→図解→数式→例
関係は「列名付きtupleの集合」。`User(id,email)`で `{id}` と `{email}` が候補キーなら片方をprimaryに選んでも理論上の候補性は残る。順序は`ORDER BY`まで意味にない。
### 実装または疑似コード
```sql
CREATE TABLE users(id bigint PRIMARY KEY, email text NOT NULL UNIQUE);
CREATE TABLE orders(id bigint PRIMARY KEY, user_id bigint NOT NULL REFERENCES users(id));
```
### よくある誤解
primary keyは候補キーの一選択。SQLは重複・NULL・順序など純粋な関係モデルを拡張する。
### 実務接続
entity integrity、foreign key、unique制約、migration reviewの基礎となる。
### 要点
- relationはtuple集合。 - 属性名で値を捉える。 - keyは最小一意化集合。 - 順序は関係に含まれない。 - 参照整合性は状態制約である。
### 誤解チェック（5問）
1. 行順は関係の一部か。2. primary以外の候補キーは無意味か。3. superkeyは最小か。4. 重複tupleを許すか。5. NULLは通常のdomain値か。
### 基礎問題（5問）
1. domainを書け。2. tupleを写像で示せ。3. superkeyを列挙せよ。4. candidateを選べ。5. FK制約を書け。
### 応用問題（3問）
1. NULLがkey推論へ与える影響を論ぜよ。2. 複合keyを設計せよ。3. bag結果との差を示せ。
### 設計問題（1問）
ユーザーの変更可能emailと不変IDを候補キー観点で設計せよ。
### 調査課題（1問）
SQL標準と利用DBのUNIQUEにおけるNULL扱いを調べよ。
### 知らないとする誤判断
連番IDを付けたので自然キーの重複制約は不要と判断する。
### 次章接続
関係を閉じた演算で変換する関係代数を学ぶ。

## 第4章 Relational Algebra
### 章を学ぶ理由
SQL文面でなく、どの関係演算を組み立てているかを理解する。
### 現場の問題
JOIN後の行増加、射影による情報損失、選択のpushdown可能性を見誤る。
### 中心概念と正式定義
選択 `σ_p(R)`、射影 `π_A(R)`、直積 `R×S`、和・差、rename `ρ`、join `R⋈_pS`。演算結果も関係という閉包性を持つ。自然joinは同名属性の等値を暗黙に使う。
### 直感→図解→数式→例
`Orders --σ status='paid'--> --⋈Users--> --π email,total--> result`。選択は行、射影は属性を絞る。join cardinalityは0から`|R||S|`まであり得る。
### 実装または疑似コード
```sql
SELECT DISTINCT u.email,o.total FROM orders o JOIN users u ON u.id=o.user_id WHERE o.status='paid';
```
### よくある誤解
JOINはlookup一回とは限らない。射影は集合意味では重複を除くが、SQL `SELECT` は通常bagを返す。
### 実務接続
query plan、view、optimizerの同値変換、authorization queryに現れる。
### 要点
- 基本演算を合成する。 - 結果も関係。 - 選択と射影を区別。 - join条件を明示。 - cardinalityを追跡する。
### 誤解チェック（5問）
1. 射影は行filterか。2. join結果は常に入力以下か。3. 自然joinは安全な既定か。4. SQL SELECTは集合射影か。5. 差は可換か。
### 基礎問題（5問）
1. 選択式を書け。2. 射影式を書け。3. joinを積と選択で表せ。4. rename理由を述べよ。5. 差を計算せよ。
### 応用問題（3問）
1. SQLを代数木へ直せ。2. 選択pushdownを証明せよ。3. outer joinが基本代数と違う点を論ぜよ。
### 設計問題（1問）
レポート要求を代数へ分解し、中間cardinalityを見積もれ。
### 調査課題（1問）
利用DBのEXPLAINで演算子対応を調べよ。
### 知らないとする誤判断
JOIN列にindexがあるだけで、中間結果増大を無視して高速と判断する。
### 次章接続
SQLが関係モデルをどのように拡張・逸脱するかを見る。

## 第5章 SQLと関係モデルの違い
### 章を学ぶ理由
理論から実装へ移る際の重複、NULL、順序、更新、型の差を管理する。
### 現場の問題
`NOT IN`とNULL、`LIMIT`と未指定順序、重複集計で本番結果が変わる。
### 中心概念と正式定義
SQLはbag semantics、三値論理`{TRUE,FALSE,UNKNOWN}`、NULL、順序・集約・副作用更新を持つ。`WHERE`はTRUEだけを残す。`NULL=x`も`NULL<>x`もUNKNOWN。
### 直感→図解→数式→例
二値論理の集合演算へ「不明」と「重複個数」を足す。`NOT (x=1)`はx=NULLでTRUEにならない。`COUNT(*)`と`COUNT(col)`はNULLを数える範囲が違う。
### 実装または疑似コード
```sql
-- NULL安全な反存在
SELECT * FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.key=a.key);
```
### よくある誤解
NULLは空文字でも0でもない。`ORDER BY`なしの行順、集約時の代表行は保証されない。
### 実務接続
ORM、pagination、anti-join、集計、unique制約、データ品質に直結する。
### 要点
- SQLは純粋関係代数ではない。 - bagを既定とする。 - NULLは三値論理を生む。 - 順序は明示する。 - dialect差を確認する。
### 誤解チェック（5問）
1. NULL=NULLはTRUEか。2. SELECTは重複排除するか。3. LIMITの結果は安定か。4. COUNT(col)は全行か。5. UNKNOWNはFALSEと同一か。
### 基礎問題（5問）
1. 三値表を作れ。2. DISTINCT効果を示せ。3. 二COUNTを比較せよ。4. ORDER BYを足せ。5. NOT EXISTSへ直せ。
### 応用問題（3問）
1. cursor paginationを設計せよ。2. outer join filterの位置を比較せよ。3. UNIQUE NULL差を分析せよ。
### 設計問題（1問）
欠測・不適用・未入力をNULL一値で潰さないschemaを設計せよ。
### 調査課題（1問）
利用DBのNULL順序と`IS DISTINCT FROM`を調べよ。
### 知らないとする誤判断
関係代数で同値な書換えをSQLのNULL・bagにも無条件で同値とみなす。
### 次章接続
schema内の属性間制約を関数従属性として捉える。

## 総合演習A（第1〜5章）
注文・顧客・配送を概念→論理schemaへ写し、候補キーと参照制約を定め、未配送注文のqueryを関係代数とNULL安全なSQLで書け。JOIN各段のcardinality上界と、bagにより集計が倍増する反例を示せ。

## 第6章 Functional Dependency
### 章を学ぶ理由
属性間の意味的依存を使い、冗長性と異常を機械的に発見する。
### 現場の問題
「現在のデータで重複がない」ことを永続的な業務制約と取り違える。
### 中心概念と正式定義
関係Rで `X→Y` は任意tuple t1,t2について `t1[X]=t2[X]⇒t1[Y]=t2[Y]`。自明依存、閉包`X+`、Armstrong公理（反射・増加・推移）を使う。X+が全属性を含めばXはsuperkey。
### 直感→図解→数式→例
`employee_id → department_id` は同じ社員IDなら部署が同じという状態制約。サンプルの偶然でなく、許される全instanceに対する主張である。
### 実装または疑似コード
```text
closure := X
while ∃(A→B) with A⊆closure and B⊄closure: closure := closure∪B
```
### よくある誤解
FDは因果・時系列・関数コードではない。値がたまたま一意でも意味上のFDとは限らない。
### 実務接続
候補キー発見、正規化、重複データ、cache invalidation範囲に使う。
### 要点
- FDは全許容状態の制約。 - 左辺一致が右辺一致を含意。 - 属性閉包で導出を調べる。 - keyはFDで特徴づく。 - 業務意味から定める。
### 誤解チェック（5問）
1. 現在値だけでFDを確定できるか。2. X→YならY→Xか。3. 因果関係か。4. superkeyは最小か。5. NULL込みで理論どおりか。
### 基礎問題（5問）
1. FDを書け。2. 自明依存を挙げよ。3. 閉包を計算せよ。4. keyを求めよ。5. 推移依存を示せ。
### 応用問題（3問）
1. 最小被覆を求めよ。2. 反例instanceを作れ。3. 時点付き属性のFDを再設計せよ。
### 設計問題（1問）
社員の部署履歴を時点込みのFDで設計せよ。
### 調査課題（1問）
DB profilerのFD推定と意味上制約の差を調べよ。
### 知らないとする誤判断
観測データで一意だった列へ業務的根拠なくunique制約を置く。
### 次章接続
FDを使って損失なくschemaを分解する。

## 第7章 Normalization
### 章を学ぶ理由
更新・挿入・削除異常を構造から除き、事実を一箇所で表す。
### 現場の問題
顧客住所を全注文行へ複製し、一部更新で矛盾する。
### 中心概念と正式定義
1NFは属性値を関係domainの単一値として扱う。2NFは非prime属性の候補キー真部分集合への依存を除く。3NFは各非自明FD `X→A` でXがsuperkeyまたはAがprime。BCNFはXが常にsuperkey。分解はlossless joinとdependency preservationを評価する。
### 直感→図解→数式→例
`Order(order_id,customer_id,customer_name)` の `order_id→customer_id→customer_name` をOrderとCustomerへ分ける。共通属性が片側を決定すれば二分解はlossless。
### 実装または疑似コード
```sql
CREATE TABLE customers(id bigint PRIMARY KEY,name text NOT NULL);
CREATE TABLE orders(id bigint PRIMARY KEY,customer_id bigint NOT NULL REFERENCES customers);
```
### よくある誤解
正規化はtable数を増やす儀式ではない。JSONを含めば即1NF違反、非正規化すれば即悪、でもない。依存と更新意味で判断する。
### 実務接続
OLTP schema、master data、履歴、denormalizationの同期責務に関わる。
### 要点
- 異常は事実の重複から生じる。 - 2NFは複合keyで顕在化。 - 3NFとBCNFを区別。 - losslessを必ず検査。 - 非正規化は派生値管理である。
### 誤解チェック（5問）
1. 3NFなら必ずBCNFか。2. 分解は常にlosslessか。3. table数が正規度か。4. 非正規化はindexと同じか。5. dependency preservationはlosslessと同じか。
### 基礎問題（5問）
1. 異常を3種示せ。2. 2NF違反を探せ。3. 3NF判定せよ。4. BCNF判定せよ。5. losslessを検査せよ。
### 応用問題（3問）
1. BCNF分解せよ。2. 依存保存性を評価せよ。3. 履歴schemaを正規化せよ。
### 設計問題（1問）
価格snapshotと現在価格を混同しない注文schemaを設計せよ。
### 調査課題（1問）
自社schema一つのFDと正規形を監査せよ。
### 知らないとする誤判断
JOINを減らすため複製した事実の整合責務を設計しない。
### 次章接続
論理schemaを高速に探索する物理的補助構造へ進む。

## 第8章 Index
### 章を学ぶ理由
indexを魔法の高速化でなく、追加write・容量と交換する探索構造として選ぶ。
### 現場の問題
全列index化、低選択性index、複合列順序ミス、更新負荷を見落とす。
### 中心概念と正式定義
indexはsearch keyからrow locator/tupleへの補助写像。selectivityは概ね `該当行/全行`。covering indexは問い合わせ属性を含みheap参照を省ける場合がある。clustered性、partial、expression indexは製品依存。
### 直感→図解→数式→例
`key → tree/hash → page → row`。costは木探索だけでなくrandom I/O、heap fetch、cache、返却行数。100万行中50万行なら逐次scanが有利な場合がある。
### 実装または疑似コード
```sql
CREATE INDEX orders_customer_created ON orders(customer_id,created_at DESC);
EXPLAIN SELECT * FROM orders WHERE customer_id=? ORDER BY created_at DESC LIMIT 20;
```
### よくある誤解
indexが存在してもoptimizerは使わない。複合index `(a,b)` は一般にb単独検索と同等でない。
### 実務接続
API pagination、unique制約、検索、write amplification、vacuumに接続する。
### 要点
- indexは冗長な物理構造。 - read/write/spaceを交換。 - 選択性と返却量を見る。 - 複合順序はquery形で決める。 - EXPLAINと実測で検証。
### 誤解チェック（5問）
1. indexは必ず使われるか。2. 全列追加が最適か。3. key順は無関係か。4. writeは無料か。5. coveringなら常にheap不要か。
### 基礎問題（5問）
1. selectivityを求めよ。2. query形を列挙せよ。3. 複合順を選べ。4. write費用を挙げよ。5. planを読め。
### 応用問題（3問）
1. partial indexを設計せよ。2. cursor pagination indexを作れ。3. index-only条件を調べよ。
### 設計問題（1問）
write-heavyなイベント表の保持・検索indexを予算付きで設計せよ。
### 調査課題（1問）
利用DBのindex typeとoperator対応を公式文書で調べよ。
### 知らないとする誤判断
遅いqueryへ無条件にindexを足し、writeとcache悪化を無視する。
### 次章接続
代表的な範囲探索構造B-tree/B+treeを内部から見る。

## 第9章 B-tree / B+tree
### 章を学ぶ理由
page I/O、分岐数、range scan、splitがindex性能をどう生むか理解する。
### 現場の問題
ランダムkey挿入や長大keyがpage分割・局所性へ与える影響を見ない。
### 中心概念と正式定義
B-treeは全leafが同深さの平衡多分木。orderに応じ各nodeは範囲内のkey/child数を持つ。B+treeはdata pointerを主にleafへ置きleafを連結する。高さ `h=O(log_m N)`、mは高いfan-out。
### 直感→図解→数式→例
`root [30|70] → pages → linked leaves`。4KiB以上のpageに多数keyを置くため数百万件でも高さは小さい。rangeは開始leaf探索後に連結leafを走査する。
### 実装または疑似コード
```text
search(k): rootからseparatorと比較しchildへ
insert(k): leafへ挿入; overflowならsplitしseparatorを親へ伝播
```
### よくある誤解
binary treeではない。`O(log N)`だけでrandom I/O、fill factor、cache、key幅の差は消えない。
### 実務接続
RDB index、filesystem、LSMとの比較、sequential key設計に関わる。
### 要点
- page単位の多分木。 - 高fan-outで浅い。 - 常に平衡。 - B+tree leaf連結がrangeに効く。 - splitと局所性を考える。
### 誤解チェック（5問）
1. 二分木か。2. leaf深さは異なるか。3. rangeは毎行rootへ戻るか。4. key幅は高さに無関係か。5. splitはreadだけの問題か。
### 基礎問題（5問）
1. 探索経路を辿れ。2. splitを描け。3. fan-outを概算せよ。4. 高さを見積もれ。5. range scanを説明せよ。
### 応用問題（3問）
1. UUID挿入を比較せよ。2. fill factorを論ぜよ。3. B-treeとhash indexを比較せよ。
### 設計問題（1問）
時系列IDの局所性と情報露出を両立するkeyを設計せよ。
### 調査課題（1問）
利用DBのB-tree page inspectorまたは公式内部文書を調べよ。
### 知らないとする誤判断
漸近計算量が同じindexは実運用性能も同じと判断する。
### 次章接続
論理queryが物理operator列へ変換される過程を学ぶ。

## 第10章 Query execution
### 章を学ぶ理由
遅さをSQL文字列でなく、scan・join・sort・aggregateとデータ流で診断する。
### 現場の問題
行数見積り、spill、nested loop内側の反復、返却待ちを見落とす。
### 中心概念と正式定義
実行計画は物理operatorの木/DAG。iterator modelでは各operatorがnextを提供。scan、nested-loop/hash/merge join、sort、aggregate、materializeがある。costはCPU、I/O、memory、network、blockingを含む。
### 直感→図解→数式→例
`scan A ↘ hash join → aggregate → sort`。nested loop概算 `|outer|×inner_lookup_cost`。hash joinはbuild側memory超過でpartition/spillする。
### 実装または疑似コード
```text
for r in outer:
  for s in lookup(inner, r.key):
    emit(r,s)
```
### よくある誤解
plan costは時間単位とは限らず、推定。`EXPLAIN ANALYZE`はqueryを実行するため副作用と負荷に注意。
### 実務接続
N+1、work_mem、parallel query、columnar/vectorized executionの理解に使う。
### 要点
- queryはoperator treeで実行。 - cardinalityが費用を支配。 - join方式に適条件。 - blocking/spillを見る。 - estimatedとactualを比較。
### 誤解チェック（5問）
1. costはmsか。2. hash joinは常に最速か。3. sortはstreamingか。4. N+1はnetworkだけか。5. actual rowsは推定か。
### 基礎問題（5問）
1. plan木を読め。2. operatorを分類せよ。3. nested費用を求めよ。4. build側を選べ。5. spill兆候を挙げよ。
### 応用問題（3問）
1. 三join順を比較せよ。2. N+1を集合query化せよ。3. pagination planを比較せよ。
### 設計問題（1問）
OLTPと分析の混在workloadを隔離・実行設計せよ。
### 調査課題（1問）
実queryのEXPLAIN estimated/actual差を分析せよ。
### 知らないとする誤判断
SQLが短いので計算も小さいと判断する。
### 次章接続
多数の同値planから実行器へ渡す一つを選ぶoptimizerを扱う。

## 第11章 Query optimizer
### 章を学ぶ理由
統計とcost modelの誤差がplan選択へ増幅する仕組みを知る。
### 現場の問題
相関列、skew、古い統計、parameter sensitivityで推定行数が外れplanが反転する。
### 中心概念と正式定義
optimizerは関係代数の同値変換と物理operator選択を探索し、推定cost最小planを選ぶ。join順は組合せ的に増える。cardinality推定はhistogram、distinct count、相関仮定などに依存する。
### 直感→図解→数式→例
`SQL→parse→logical plan→rewrite→costed physical plans→chosen plan`。独立仮定なら `sel(A∧B)≈sel(A)sel(B)` だが、郵便番号と都道府県は相関する。
### 実装または疑似コード
```text
for candidate in enumerate_plans(logical):
  cost = estimate(candidate, statistics)
choose argmin(cost)
```
### よくある誤解
optimizerはデータの意味を知らず、常に最適でもない。hint固定は統計変化へ脆い。
### 実務接続
ANALYZE、extended statistics、plan cache、query rewrite、regression監視に関わる。
### 要点
- 同値planを探索。 - costは統計依存推定。 - join順は巨大。 - 相関が誤差を生む。 - 根因は推定差から調べる。
### 誤解チェック（5問）
1. optimizerは意味制約を全て知るか。2. 最適保証か。3. 統計は自動で常に新鮮か。4. 列は常に独立か。5. hintは恒久解か。
### 基礎問題（5問）
1. pipelineを描け。2. 選択率を計算せよ。3. 相関例を挙げよ。4. join順を数えよ。5. 推定差を探せ。
### 応用問題（3問）
1. skewを再現せよ。2. parameter-sensitive planを論ぜよ。3. 統計更新前後を比較せよ。
### 設計問題（1問）
plan regressionの検知・rollback・再分析を設計せよ。
### 調査課題（1問）
利用DBの統計収集とplan cache仕様を調べよ。
### 知らないとする誤判断
plan変更をDBの気まぐれとみなし、入力分布と推定誤差を調べない。
### 次章接続
単一queryから複数更新の論理単位、transactionへ進む。

## 総合演習B（第6〜11章）
受注明細schemaのFDを列挙して3NF/BCNFへlossless分解し、顧客別直近20件queryのindexとoperator planを設計せよ。データskewでoptimizerが誤る反例、非正規化する場合の同期責務と測定基準も示せ。

## 第12章 Transaction
### 章を学ぶ理由
複数操作を一つの状態遷移として扱い、途中状態を外部へ漏らさない。
### 現場の問題
外部APIとDBを一transactionと思う、長時間transactionで競合・肥大化を起こす。
### 中心概念と正式定義
transaction TはDB状態DをD'へ写す部分関数。BEGINからCOMMIT/ABORTまでのread/write列で、commitした効果だけが確定する。DB transactionの原子性境界は通常外部systemを含まない。
### 直感→図解→数式→例
`D --T tentative--> D' --commit--> visible`、abortならDへ論理的に戻す。送金は引落しと入金を一境界に置く。
### 実装または疑似コード
```sql
BEGIN; SELECT balance FROM accounts WHERE id=1 FOR UPDATE;
UPDATE accounts SET balance=balance-100 WHERE id=1; COMMIT;
```
### よくある誤解
transactionは並行競合を全て自動解決しない。例外時rollbackと外部副作用補償を別に設計する。
### 実務接続
unit of work、outbox、idempotency、batch、DDL migrationに現れる。
### 要点
- 論理状態遷移を囲う。 - commit/abortを区別。 - 境界外副作用を認識。 - 短く保つ。 - retry意味を設計。
### 誤解チェック（5問）
1. HTTP送信も自動rollbackか。2. BEGINで直列化されるか。3. abortはログ不要か。4. 長いほど安全か。5. commit応答消失時に結果を断定できるか。
### 基礎問題（5問）
1. 境界を決めよ。2. read/write setを列挙せよ。3. abort経路を書け。4. 外部副作用を分けよ。5. retry条件を示せ。
### 応用問題（3問）
1. outboxを説明せよ。2. unknown commitを処理せよ。3. savepointの限界を論ぜよ。
### 設計問題（1問）
注文確定とメール送信を整合させる設計をせよ。
### 調査課題（1問）
driverのautocommitとconnection pool resetを調べよ。
### 知らないとする誤判断
DB rollbackが既送信メールや決済も取り消すと思う。
### 次章接続
transactionが約束する性質をACIDとして分解する。

## 第13章 ACID
### 章を学ぶ理由
曖昧な「transactional」を原子性・整合性・分離性・永続性へ分けて確認する。
### 現場の問題
ACID対応という製品表示だけで業務制約や分離履歴を保証したと思う。
### 中心概念と正式定義
Atomicityはall-or-nothing、Consistencyはtransactionが定義済み制約を保存、Isolationは並行履歴の観測制約、Durabilityはcommit後の効果が規定故障後も残ること。Cは業務正しさそのものをDBが発見する意味でない。
### 直感→図解→数式→例
`valid D --valid T--> valid D'`。AとDはrecovery、Iはconcurrency、Cはschema/transaction設計と結びつく。durabilityの故障範囲はprocess/crash/disk/siteで異なる。
### 実装または疑似コード
```text
assert constraints(before)
execute T atomically under chosen isolation
commit only after durability point
assert constraints(after)
```
### よくある誤解
ACIDとCAPのConsistencyは別。Durableは地理災害・操作ミスからの復元を無条件に意味しない。
### 実務接続
DB選定、SLA、backup、fsync設定、transaction testの質問表になる。
### 要点
- 四性質を別々に問う。 - Cは制約定義が前提。 - Iには強弱がある。 - Dは故障モデル依存。 - ACIDラベルだけで判断しない。
### 誤解チェック（5問）
1. Cは業務仕様を自動発見か。2. Dはbackupか。3. Iは常にserializableか。4. Aは外部APIも含むか。5. CAP Cと同じか。
### 基礎問題（5問）
1. 各文字を説明せよ。2. 故障範囲を書け。3. 制約を一つ示せ。4. isolation例を挙げよ。5. backupとの差を述べよ。
### 応用問題（3問）
1. 非同期commitを評価せよ。2. replica durabilityを論ぜよ。3. ACID保証表を作れ。
### 設計問題（1問）
監査ログのACID要件とsite loss要件を分離設計せよ。
### 調査課題（1問）
利用DBのcommit durability設定を調べよ。
### 知らないとする誤判断
ACID対応なのでserializableかつ災害耐性ありと解釈する。
### 次章接続
Isolationを具体的な許容現象と履歴で学ぶ。

## 第14章 Isolation Level
### 章を学ぶ理由
名前でなく、アプリの不変条件を壊す並行現象を選択的に防ぐ。
### 現場の問題
lost update、write skew、phantomをRead Committedで防げると思う。
### 中心概念と正式定義
標準のRead Uncommitted、Read Committed、Repeatable Read、Serializableは許す現象で区別されるが製品実装差がある。dirty read、nonrepeatable read、phantom、lost update、write skewを具体的履歴で評価する。
### 直感→図解→数式→例
`T1:R(x=0) ... W(x=1)` と `T2:R(x=0)...W(x=1)` はlost update。二人の医師が互いをon-callと読み各自offにするwrite skewは別行更新でも集合制約を破る。
### 実装または疑似コード
```text
T1: R(A=on,B=on) W(A=off)
T2: R(A=on,B=on) W(B=off)
結果 A=off,B=off  # 不変条件破壊
```
### よくある誤解
Repeatable Readという名前だけでpredicate全体が安全とは限らない。分離レベルの挙動はDB公式文書で確認する。
### 実務接続
在庫、予約、quota、on-call、残高、job claimに現れる。
### 要点
- anomalyを履歴で表す。 - 製品差を確認。 - lost updateとwrite skewを区別。 - 不変条件からlevelを選ぶ。 - serialization failureをretryする。
### 誤解チェック（5問）
1. Read Committedでlost update皆無か。2. RRは全DB同じか。3. 行lockでpredicate制約は常に守れるか。4. Serializableは障害なしを意味するか。5. retry不要か。
### 基礎問題（5問）
1. dirty readを描け。2. nonrepeatableを描け。3. phantomを描け。4. lost updateを描け。5. write skewを描け。
### 応用問題（3問）
1. 在庫履歴を分析せよ。2. optimistic updateを設計せよ。3. retry loopを安全にせよ。
### 設計問題（1問）
会議室予約の重複禁止を分離level・制約・lockで設計せよ。
### 調査課題（1問）
利用DBの各level実装を公式文書で表にせよ。
### 知らないとする誤判断
level名が同じなら全DBで同じ履歴を許すと思う。
### 次章接続
最強の基準となる直列化可能性を形式化する。

## 第15章 Serializability
### 章を学ぶ理由
並行実行結果が何らかの直列順序と同値かを正しさの基準にする。
### 現場の問題
最終値だけ比較し、途中readや制約違反を含む非直列化履歴を見逃す。
### 中心概念と正式定義
履歴Hが同じtransactionのある直列履歴とconflict-equivalentならconflict-serializable。precedence graphの頂点はtransaction、競合操作順に辺を張り、非巡回なら直列化可能。view serializabilityはより一般だが判定が難しい。
### 直感→図解→数式→例
`T1→T2`はT1のwriteがT2のread/writeに先行。両方向辺ならcycleで直列順を作れない。serial orderは実時間順とは限らず、strict serializabilityは実時間制約も加える。
### 実装または疑似コード
```text
for conflicting ops oi in Ti, oj in Tj with oi before oj: add edge Ti→Tj
return acyclic(graph)
```
### よくある誤解
serializableは一つずつ実行する意味ではない。snapshot isolationは一般にserializableでない。
### 実務接続
SSI、2PL、transaction testing、distributed serializabilityに接続する。
### 要点
- 履歴を比較。 - 競合graphで判定。 - cycleが反例。 - 並行性と両立。 - strict性を区別。
### 誤解チェック（5問）
1. 並行実行を禁止するか。2. SIは常にserializableか。3. 最終値だけで判定か。4. graph cycleは許容か。5. strictは実時間を含むか。
### 基礎問題（5問）
1. 履歴を書け。2. 競合を列挙せよ。3. graphを作れ。4. cycle判定せよ。5. 直列順を求めよ。
### 応用問題（3問）
1. write skew graphを作れ。2. recoverabilityと比較せよ。3. strict serializabilityを論ぜよ。
### 設計問題（1問）
業務transaction群のserialization conflictとretry境界を設計せよ。
### 調査課題（1問）
PostgreSQL SSIの危険構造を調べよ。
### 知らないとする誤判断
同じ最終行値なら履歴も正しいと判断する。
### 次章接続
直列化を実現する主要手段の一つ、lockを扱う。

## 第16章 Lock
### 章を学ぶ理由
競合操作の順序を制御し、待ち・deadlock・granularityを設計する。
### 現場の問題
lock範囲、取得順、保持時間が不明なままtimeoutを増やす。
### 中心概念と正式定義
shared/exclusive lockのcompatibility matrix、行・page・table・predicate粒度。2PLは成長期に取得、縮小期に解放しconflict serializabilityを保証する。strict 2PLはwrite lockをcommitまで保持。wait-for graph cycleはdeadlock。
### 直感→図解→数式→例
`T1 holds A waits B`、`T2 holds B waits A`でcycle。lock粒度が粗いほど管理費は減るが偽競合が増える。
### 実装または疑似コード
```sql
SELECT * FROM accounts WHERE id IN (1,2) ORDER BY id FOR UPDATE;
```
### よくある誤解
行lockだけ見てもindex探索やFK検査で別資源をlockする。deadlockはバグ隠蔽でなく検出後片方abortが通常。
### 実務接続
`FOR UPDATE`、DDL、advisory lock、job claim、deadlock logに現れる。
### 要点
- compatibilityを理解。 - 粒度を選ぶ。 - 順序を統一。 - 保持時間を短く。 - deadlock victimはretry。
### 誤解チェック（5問）
1. read lockとwrite lockは常に互換か。2. timeout増加が根治か。3. 行だけが資源か。4. 2PLはdeadlockなしを保証か。5. lock取得順は無関係か。
### 基礎問題（5問）
1. matrixを書け。2. wait graphを作れ。3. cycleを探せ。4. 粒度比較せよ。5. 取得順を直せ。
### 応用問題（3問）
1. FK deadlockを分析せよ。2. queue claimを設計せよ。3. lock escalationを論ぜよ。
### 設計問題（1問）
複数口座更新の全経路でlock順を統一せよ。
### 調査課題（1問）
利用DBのlock viewとdeadlock reportを調べよ。
### 知らないとする誤判断
deadlock timeoutだけ増やし、wait-for cycleの取得順根因を直さない。
### 次章接続
readとwriteの競合をversionで減らすMVCCへ進む。

## 第17章 MVCC
### 章を学ぶ理由
snapshot、可視性、古いversion、vacuumを一つのモデルで理解する。
### 現場の問題
長いtransactionがcleanupを妨げる、snapshotが最新値と思う、write skewを見落とす。
### 中心概念と正式定義
MVCCは論理行の複数versionに作成・失効transaction情報を持ち、snapshotの可視性規則でreadする。抽象的には `Visible(v,S)` を「version vの作成transactionがsnapshot Sから見てcommit済みで、削除transactionはSから見て未commitまたは未開始」と定義する。PostgreSQLのsnapshotは単一の数値時刻ではなく、`xmin`、`xmax`、進行中transaction集合などを持つため、単純な `xmin(v)≤S<xmax(v)` だけでは可視性を判定できない。規則の詳細はDB実装に依存する。
### 直感→図解→数式→例
`row: v1 [T1,T3), v2 [T3,∞)`。readerは自分のsnapshotに対応するversionを見るためreader/writer競合を減らすが、writer同士やpredicate制約は残る。
### 実装または疑似コード
```text
read(row,snapshot): newest version visible(snapshot)
update: create new version; mark old version obsolete
vacuum: reclaim versions no active snapshot can see
```
### よくある誤解
MVCCはlock-freeでもserializable保証でもない。versionは無限に無料で残らない。
### 実務接続
PostgreSQL vacuum、InnoDB undo、snapshot export、replica lagに関わる。
### 要点
- snapshotで可視性を決定。 - versionを追加。 - reader/writer競合を削減。 - write競合は残る。 - cleanup horizonを監視。
### 誤解チェック（5問）
1. 常に最新を読むか。2. lock不要か。3. storage増加なしか。4. SIはserializableか。5. 長期readerは無害か。
### 基礎問題（5問）
1. version列を描け。2. snapshot可視性を判定せよ。3. obsoleteを選べ。4. writer競合を示せ。5. cleanup条件を書け。
### 応用問題（3問）
1. long transaction障害を分析せよ。2. write skewを再現せよ。3. vacuum指標を選べ。
### 設計問題（1問）
長時間分析queryをOLTP snapshot寿命から隔離せよ。
### 調査課題（1問）
利用DBのMVCC metadataとcleanupを調べよ。
### 知らないとする誤判断
readがblockしないので長期transactionに運用コストがないと考える。
### 次章接続
commitした変更を故障後に再構成するWALを学ぶ。

## 第18章 WAL
### 章を学ぶ理由
data pageより先にlogを永続化することでatomicity/durabilityを実現する原理を知る。
### 現場の問題
fsync、checkpoint、log retention、replication slotの意味を混同する。
### 中心概念と正式定義
Write-Ahead Logging規則は、変更data pageを永続化する前に対応log recordを安定記憶へ置くこと。同期durabilityを契約する設定では、commit成功応答前にcommit recordを規定のdurability pointへ到達させる。非同期commitは応答latencyと、process/OS/power failure時に直近commitを失い得る範囲を明示的に交換する。LSNはlog順位置を表す。
### 直感→図解→数式→例
`update → WAL buffer → durable WAL → data page later`。random data page書込みを順次logへ先行記録し、crash後redo可能にする。
### 実装または疑似コード
```text
append log(before/after, page, tx)
flush WAL through LSN
then allow dirty page flush; on commit flush commit LSN
```
### よくある誤解
WALはbackupそのものではない。OSへwriteしただけとstable storageへflushしたことを区別する。
### 実務接続
group commit、PITR、streaming replication、checkpoint、write amplificationに接続。
### 要点
- logがdataに先行。 - LSNで順序化。 - commit durability pointを知る。 - redo材料となる。 - retentionを容量設計。
### 誤解チェック（5問）
1. data pageが先でよいか。2. write syscallで必ず耐電断か。3. WALは完全backupか。4. checkpointでWAL不要になるか。5. async commitは同保証か。
### 基礎問題（5問）
1. 書込み順を示せ。2. LSNを説明せよ。3. flush点を示せ。4. group commitを説明せよ。5. retention要因を挙げよ。
### 応用問題（3問）
1. fsync無効の故障を分析せよ。2. log bottleneckを論ぜよ。3. replica lagとretentionを結べ。
### 設計問題（1問）
RPO要件からcommitとWAL archiveを設計せよ。
### 調査課題（1問）
利用DBのWAL/redo log設定を公式文書で調べよ。
### 知らないとする誤判断
COMMIT応答前後のdurability pointを確認せず、応答消失を単純失敗扱いする。
### 次章接続
WALとcheckpointを使ったcrash recovery全体へ進む。

## 第19章 Crash Recovery
### 章を学ぶ理由
crash後にどのtransactionをredo/undoし、どこまで復旧できるか説明する。
### 現場の問題
再起動成功を整合性確認とみなし、corruption、unknown commit、長いrecoveryを考えない。
### 中心概念と正式定義
steal/no-steal、force/no-force方針によりundo/redo要否が決まる。ARIES系ではanalysis、redo（repeat history）、undoを行い、compensation log recordでundoを再実行可能にする。checkpointは開始点を狭めるが瞬間snapshotとは限らない。
### 直感→図解→数式→例
crash時にcommit済みだがpage未反映はredo、未commitだがpage反映はundo。`log→analysis→redo→undo→consistent open`。
### 実装または疑似コード
```text
losers,winners = analyze(log)
redo records after recoveryLSN
undo losers in reverse order, logging compensation
```
### よくある誤解
recoveryとbackup restoreは別。DB crash、media loss、site loss、論理誤操作で手段が違う。
### 実務接続
startup recovery、PITR、crash loop、recovery time、chaos testに現れる。
### 要点
- 故障種類を分ける。 - redo/undo条件を知る。 - checkpointは作業短縮。 - unknown outcomeを扱う。 - 復旧を定期演習。
### 誤解チェック（5問）
1. crashはmedia lossと同じか。2. commit済みはredo不要か。3. 未commitはpageへ出ないか。4. checkpointはbackupか。5. restart成功で論理正しさ確定か。
### 基礎問題（5問）
1. winner/loserを分類せよ。2. redoを選べ。3. undoを選べ。4. checkpoint効果を述べよ。5. 故障を分類せよ。
### 応用問題（3問）
1. crash履歴を復旧せよ。2. RTOを見積もれ。3. unknown commit APIを設計せよ。
### 設計問題（1問）
DB crash・disk loss・誤DELETE別のrunbookを作れ。
### 調査課題（1問）
利用DBでrestore rehearsalを実施し時間を測れ。
### 知らないとする誤判断
replicaがあるので誤DELETEも自動的に元へ戻ると思う。
### 次章接続
一台の故障を越えるため、状態を複数nodeへ複製する。

## 総合演習C（第12〜19章）
座席予約の不変条件を定義し、write skewを起こす履歴、serializableでのabort、lock順、MVCC version、WAL record、crash直後のredo/undoを一続きで示せ。commit応答消失時の冪等なAPI応答も設計せよ。

## 第20章 Replication
### 章を学ぶ理由
可用性・read scaling・災害耐性と、lag・failover・一貫性の代償を理解する。
### 現場の問題
非同期replicaへ最新readを期待し、failoverで確定writeを失う。
### 中心概念と正式定義
leader-follower、multi-leader、leaderlessがある。同期複製はack条件にreplicaを含め、非同期はlag/RPOを許す。quorumは典型にN replicasでread R、write W、`R+W>N`なら重なりを持つが、version解決等の仮定が必要。
### 直感→図解→数式→例
`client→leader→log→followers`。ack後にleader単独故障しても残したいならack集合を設計。read-after-writeをreplica routingだけで壊し得る。
### 実装または疑似コード
```text
write: append version; wait for required acknowledgements
read: choose replica satisfying session's minimum version
```
### よくある誤解
replicaはbackupでも自動的な一貫readでもない。quorum式だけでpartition・clock・conflict解決は済まない。
### 実務接続
read replica、HA、CDC、geo replication、failover fencingに現れる。
### 要点
- 複製目的を分ける。 - ack意味を定義。 - lagを観測。 - session保証を設計。 - failover時split brainを防ぐ。
### 誤解チェック（5問）
1. replicaはbackupか。2. 非同期ackは全copy済みか。3. followerは常に最新か。4. quorum式だけで十分か。5. failbackは無害か。
### 基礎問題（5問）
1. topologyを描け。2. ack点を示せ。3. RPOを求めよ。4. lag影響を挙げよ。5. session保証を書け。
### 応用問題（3問）
1. read-your-writesを設計せよ。2. promotion lossを分析せよ。3. fencingを説明せよ。
### 設計問題（1問）
決済と検索で異なるreplication要件を設計せよ。
### 調査課題（1問）
利用DBの同期commit modeを調べよ。
### 知らないとする誤判断
replica台数を増やせばdurability、一貫性、backupが同時に解決すると考える。
### 次章接続
データを複製でなく分割配置するshardingへ進む。

## 第21章 Sharding
### 章を学ぶ理由
単一node限界を越える際、配置関数と再配置・跨ぎ操作の代償を設計する。
### 現場の問題
hot shard、fan-out、global unique、rebalancing、tenant偏りを後から発見する。
### 中心概念と正式定義
shard関数 `s:key→{0,…,n-1}`。range、hash、directory方式。均等性だけでなくlocality、単調拡張、failure domainを評価。consistent hashingはnode増減時の移動割合を抑えるが均等を自動保証しない。
### 直感→図解→数式→例
`tenant_id --s--> shard`。queryがshard keyを持てば一箇所、なければfan-out n。最大tenantが容量を超えるとtenant単位分割は破綻する。
### 実装または疑似コード
```text
sid = hash(tenant_id) mod N
route(sid, query); reject cross-shard transaction unless protocol defined
```
### よくある誤解
hashで常に均等、shard追加はmod N変更だけ、とは限らない。早すぎるshardingは運用複雑性を増す。
### 実務接続
multi-tenant SaaS、time partition、rebalancer、routing layerに現れる。
### 要点
- shard keyが境界を決める。 - skewを測る。 - fan-outを避ける。 - migrationを設計。 - global制約の代価を払う。
### 誤解チェック（5問）
1. hashでhotspot皆無か。2. shard keyなしqueryは一箇所か。3. N変更は移動なしに可能か。4. FKは全shardで同じか。5. shardはreplicaか。
### 基礎問題（5問）
1. 関数を書け。2. keyを選べ。3. fan-out数を求めよ。4. skewを算出せよ。5. migration手順を書け。
### 応用問題（3問）
1. celebrity tenantを処理せよ。2. global IDを設計せよ。3. reshard二重writeを論ぜよ。
### 設計問題（1問）
tenant成長分布を前提に段階的shardingを設計せよ。
### 調査課題（1問）
実DBのpartitioning/sharding境界を調べよ。
### 知らないとする誤判断
平均tenantサイズからshard容量を決め、最大値と成長偏りを無視する。
### 次章接続
複数nodeを一DBとして見せる分散DB全体を扱う。

## 第22章 Distributed Database
### 章を学ぶ理由
network partitionとpartial failure下でtransaction・配置・合意を設計する。
### 現場の問題
単一node ACIDをそのまま地域分散へ期待し、遅延と不確実な結果を無視する。
### 中心概念と正式定義
分散DBは複数failure domain上の複製・分割データへ統一interfaceを提供。原子commitに2PC、replica順序合意にconsensus等を使う。2PCはprepare/commitで全参加者を揃えるがcoordinator故障時blockし得る。
### 直感→図解→数式→例
`client→coordinator→participants`。network timeoutは「失敗」ではなく結果不明。latency下界には必要なremote round tripが入る。
### 実装または疑似コード
```text
prepare all participants
if all YES: durably decide COMMIT; notify all
else: decide ABORT
```
### よくある誤解
2PCとconsensusは同じでない。CAPは「三つから二つ」製品分類でなくpartition時の応答と一貫性の選択を述べる。
### 実務接続
distributed SQL、global tables、saga、transaction coordinator、clock uncertaintyに接続。
### 要点
- partial failureが基本。 - timeoutは不確実。 - commitとreplication合意を区別。 - RTT予算を見る。 - retry/idempotencyを組込む。
### 誤解チェック（5問）
1. timeoutはabort確定か。2. 2PCはconsensusか。3. networkは可靠か。4. CAPは常時二択か。5. global transactionはlocal同等latencyか。
### 基礎問題（5問）
1. failureを列挙せよ。2. 2PC状態を描け。3. unknownを示せ。4. RTTを数えよ。5. coordinator logを説明せよ。
### 応用問題（3問）
1. in-doubtを処理せよ。2. sagaと比較せよ。3. region partition方針を設計せよ。
### 設計問題（1問）
地域跨ぎ在庫引当を不変条件とavailabilityから設計せよ。
### 調査課題（1問）
一つのdistributed DBのtransaction protocolを一次資料で調べよ。
### 知らないとする誤判断
HTTP retryだけで分散transactionの不確実性が消えると考える。
### 次章接続
関係以外のモデルを採用するNoSQLを能力と制約で比較する。

## 第23章 NoSQL
### 章を学ぶ理由
製品カテゴリでなく、data model・query・consistency・partition特性から選ぶ。
### 現場の問題
「schema-less」「無限scale」「JOINなし」を設計不要と解釈する。
### 中心概念と正式定義
key-valueはkey→opaque value、documentは構造化集約、wide-columnはpartition/sort key付き疎な列、graphは頂点・辺・property。各モデルは主要操作を局所化する代わりに別操作・制約を難しくする。
### 直感→図解→数式→例
`query pattern→必要局所性→model`。注文集約を文書に埋めれば一取得だが、商品名一括更新は多数文書へ伝播する。
### 実装または疑似コード
```text
get(key); put(key,version,value)
query partitionKey + sortKeyRange
traverse (user)-[FOLLOWS]->(user)
```
### よくある誤解
NoSQLは一保証集合ではない。schemaは消えずwriter/readerコードへ移る。category内でもtransaction能力が異なる。
### 実務接続
cache、catalog、time-series、social graph、event storeに現れる。
### 要点
- 主要操作から選ぶ。 - schema責務は残る。 - partition keyが重要。 - 制約範囲を確認。 - categoryで保証を断定しない。
### 誤解チェック（5問）
1. schema不要か。2. NoSQLは全てeventualか。3. documentはjoin不要を保証か。4. graphは全query最速か。5. key-valueはvalueを検索できるか。
### 基礎問題（5問）
1. 四modelを定義せよ。2. 操作を対応付けよ。3. keyを選べ。4. 制約を列挙せよ。5. 更新範囲を示せ。
### 応用問題（3問）
1. product catalogを比較せよ。2. time-seriesを設計せよ。3. graph traverseをRDBと比較せよ。
### 設計問題（1問）
チャット履歴の順序、検索、保持、削除からmodelを選べ。
### 調査課題（1問）
候補製品の公式consistency/transaction仕様を比較せよ。
### 知らないとする誤判断
SQLを使わないこと自体をscalability根拠にする。
### 次章接続
複製・分散環境でread/writeが観測する順序保証を整理する。

## 第24章 Consistency
### 章を学ぶ理由
曖昧な「強い／弱い」を、操作履歴へ課す具体的保証に直す。
### 現場の問題
eventual consistencyを「数秒後に必ず最新」、strongを「業務上正しい」と誤る。
### 中心概念と正式定義
linearizabilityは各操作が呼出しと応答の間の一点で原子的に起きたように見え実時間順を保つ。sequential consistencyは全processで一つの順序だが実時間制約なし。causal consistencyは因果順を保つ。eventualは更新停止後replicaが収束する性質で、期限は別保証。
### 直感→図解→数式→例
`W(x=1) complete → R(x)`が必ず1以上を見るのはlinearizable registerの要請。session保証にはread-your-writes、monotonic reads等がある。
### 実装または疑似コード
```text
client stores last_seen_version
read from replica only if applied_version >= last_seen_version
```
### よくある誤解
ACID C、CAP C、replica consistencyは別の問い。収束しても競合解決結果が業務上正しいとは限らない。
### 実務接続
profile更新、timeline、DNS、cache、distributed DBのAPI契約に現れる。
### 要点
- 履歴保証を命名。 - 実時間と因果を区別。 - session保証を選ぶ。 - 収束期限は別。 - 不変条件と結ぶ。
### 誤解チェック（5問）
1. eventualに時間上限が含まれるか。2. sequentialは実時間順か。3. causalは全操作全順序か。4. strongは業務正しさか。5. cacheは常にmonotonicか。
### 基礎問題（5問）
1. linearizable履歴を判定せよ。2. stale readを描け。3. causal edgeを書け。4. session保証を列挙せよ。5. convergenceを定義せよ。
### 応用問題（3問）
1. profile UX保証を選べ。2. counter conflictを解決せよ。3. bounded stalenessを設計せよ。
### 設計問題（1問）
在庫表示と決済確定に別々のconsistencyを割り当てよ。
### 調査課題（1問）
利用serviceのconsistency SLAを一次資料で調べよ。
### 知らないとする誤判断
「eventualだから仕方ない」と無期限stalenessや単調性違反まで許す。
### 次章接続
ここまでの理論を変更に強いschema判断へ統合する。

## 総合演習D（第20〜24章）
三地域の在庫DBについて、replication ack、shard key、2PC要否、partition時方針、read-your-writesを設計せよ。timeout後のunknown write、hot tenant、failover data loss、収束したが在庫負数になる反例を必ず扱う。

## 第25章 Schema設計
### 章を学ぶ理由
現在queryだけでなく不変条件、履歴、変更、所有権、削除を長期設計する。
### 現場の問題
万能table、意味不明NULL、mutable natural key、時刻上書き、soft delete乱用が蓄積する。
### 中心概念と正式定義
schemaは許容状態集合と遷移の境界。entity identity、fact、event、snapshotを分ける。temporal dataではvalid timeとtransaction timeを区別。派生値にはsource of truthと再構築規則を持つ。
### 直感→図解→数式→例
`Event (何が起きた) → projection (現在像)`、`effective_from≤t<effective_to`。注文時価格は商品現在価格の参照でなく注文事実のsnapshot。
### 実装または疑似コード
```sql
CREATE TABLE price_history(product_id bigint, valid_from timestamptz, valid_to timestamptz,
 price numeric NOT NULL, CHECK(valid_to IS NULL OR valid_from < valid_to));
```
### よくある誤解
soft deleteは監査・復元・法令削除を自動解決しない。ORM modelはdomain modelそのものではない。
### 実務接続
GDPR等の保持、audit、schema migration、CDC、analyticsに接続する。
### 要点
- identityと属性を分ける。 - 時間意味を明示。 - 制約をDBへ置く。 - 派生元を定義。 - evolutionを計画。
### 誤解チェック（5問）
1. created_atは全履歴か。2. soft deleteは物理削除か。3. natural keyは不変か。4. JSONで変更容易性が自動向上か。5. 派生列はsourceか。
### 基礎問題（5問）
1. entity/factを分けよ。2. keyを定めよ。3. temporal intervalを書け。4. constraintを置け。5. sourceを示せ。
### 応用問題（3問）
1. bitemporalを設計せよ。2. online migrationを論ぜよ。3. deletion policyを設計せよ。
### 設計問題（1問）
契約の改訂・遡及訂正・監査を保持するschemaを設計せよ。
### 調査課題（1問）
実schemaの暗黙制約を抽出せよ。
### 知らないとする誤判断
履歴を上書きし、監査ログがあれば任意時点を再構築できると思う。
### 次章接続
理論の欠落がどのような障害連鎖になるか事例で追う。

## 第26章 DB障害事例
### 章を学ぶ理由
症状でなく、仮説の優先順位を付けて構造的根因を隔離する。
### 現場の問題
CPU高騰へindex追加、deadlockへtimeout延長、lagへreplica追加と症状を抑える。
### 中心概念と正式定義
障害分析は `invariant violation / saturation / contention / estimation error / durability failure / operator error` に分類し、timeline、変更、待ち、plan、WAL、replica位置から反証する。
### 直感→図解→数式→例
ケース: deploy後p99急増。`schema変更→統計ずれ→join順反転→spill→I/O飽和→replica lag`。原因と増幅器を区別する。
### 実装または疑似コード
```text
1 影響/時刻を固定 2 wait/eventとplan差を取得 3 仮説を反証順に並べる
4 負荷を止める 5 根因を修正 6 再発防止を制約・監視へ固定
```
### よくある誤解
最後に出たエラーが根因とは限らない。相関指標だけで因果を決めない。
### 実務接続
incident command、slow query、lock graph、PITR、capacity reviewに使う。
### 要点
- timelineを作る。 - waitから見る。 - 仮説を反証。 - 原因と増幅器を分ける。 - countermeasureを構造へ固定。
### 誤解チェック（5問）
1. CPU高=CPU根因か。2. timeout増加は根治か。3. replica追加でwrite改善か。4. 最後の変更が必ず原因か。5. restartで解析完了か。
### 基礎問題（5問）
1. timelineを作れ。2. 仮説を3つ挙げよ。3. 反証指標を選べ。4. 待ちを分類せよ。5. 根因を記述せよ。
### 応用問題（3問）
1. deadlock事故を分析せよ。2. WAL満杯を分析せよ。3. failover data lossを分析せよ。
### 設計問題（1問）
DB incident runbookと証拠保全を設計せよ。
### 調査課題（1問）
公開DB障害postmortemを因果graphへ直せ。
### 知らないとする誤判断
症状を消す変更を根本対策と呼び、同じ構造を残す。
### 次章接続
障害前にworkloadと資源を定量設計する。

## 第27章 性能設計
### 章を学ぶ理由
単query最適化を越え、throughput、latency、queue、I/O、cache、成長を予算化する。
### 現場の問題
平均値、開発データ、cache温状態だけでcapacityを決める。
### 中心概念と正式定義
Littleの法則 `L=λW`（安定系の平均同時数=到着率×滞在時間）。利用率が1へ近づくと待ちが急増。working set、IOPS/帯域、write amplification、connection数、p95/p99をworkload別に測る。
### 直感→図解→数式→例
1000 req/s、平均50msなら平均in-flight 50。接続100を無条件に増やしてもCPU/I/O service rateは増えずqueue位置が移るだけ。
### 実装または疑似コード
```text
for workload_class: record arrival_rate, service_time, rows, IO, locks
load test with production distribution; observe saturation knee and tails
```
### よくある誤解
connection pool増加、cache hit率、平均latency単独では性能を説明できない。benchmarkは負荷分布込みのモデル検証。
### 実務接続
capacity planning、SLO、pool、batch、rate limit、partition lifecycleに使う。
### 要点
- workloadを分類。 - tailを見る。 - queueを計測。 - bottleneck資源を特定。 - 成長と劣化点を試験。
### 誤解チェック（5問）
1. 平均だけでSLO可か。2. connection増で容量も比例か。3. cache hit率高なら高速か。4. 開発データで十分か。5. throughput最大点が安全運用点か。
### 基礎問題（5問）
1. Little則を計算せよ。2. workloadを分類せよ。3. tailを求めよ。4. resource budgetを書け。5. saturation兆候を挙げよ。
### 応用問題（3問）
1. pool sizeを実験設計せよ。2. write amplificationを見積もれ。3. queue collapseを防げ。
### 設計問題（1問）
10倍成長するSaaS DBの負荷試験と段階的容量計画を作れ。
### 調査課題（1問）
利用DBの主要wait eventを調べdashboardへ対応付けよ。
### 知らないとする誤判断
負荷を増やしてthroughputが最大になった点を安全な定常運用点とする。
### 次章接続
全概念を一つのデータモデリング設計レビューへ統合する。

## 第28章 総合データモデリング演習
### 章を学ぶ理由
要件からschema、transaction、index、回復、分散、運用まで一貫して導く。
### 現場の問題
schema担当と運用担当の境界で、不変条件・failure semantics・capacity前提が失われる。
### 中心概念と正式定義
設計成果物を `M=(Entities,FDs,Constraints,Transactions,Queries,Failures,SLOs)` とする。各transactionは制約保存、各queryはconsistency契約、各failureはRPO/RTOと検証手段を持つ。
### 直感→図解→数式→例
題材は座席販売。`Seat(show,number)`、`Reservation`、`Payment`。不変条件 `∀show,seat: active_reservation≤1`。決済外部副作用はoutbox/idempotencyでDB境界と接続。
### 実装または疑似コード
```sql
CREATE UNIQUE INDEX one_active_seat ON reservations(show_id,seat_no)
WHERE status IN ('held','paid');
```
### よくある誤解
ER図完成は設計完了でない。並行履歴、失敗、migration、観測、削除、負荷まで必要。
### 実務接続
ADR、schema migration、load test、DR drill、security reviewを統合する。
### 要点
- 不変条件から始める。 - FDで正規化。 - transaction履歴を試す。 - queryから物理設計。 - failureと運用を検証。
### 誤解チェック（5問）
1. ER図だけで並行性が決まるか。2. uniqueは外部決済も一意化するか。3. replicaはDR全体か。4. SLOなしで性能設計可か。5. migrationは平時操作か。
### 基礎問題（5問）
1. entityを列挙せよ。2. FDを書け。3. constraintを書け。4. queryを列挙せよ。5. failureを分類せよ。
### 応用問題（3問）
1. write skewを防げ。2. payment unknownを処理せよ。3. 地域展開を設計せよ。
### 設計問題（1問）
チケット販売をschema、API、transaction、index、replication、backup、SLOまで設計レビューせよ。
### 調査課題（1問）
選んだDBでprototypeを作り、concurrency testとEXPLAINを記録せよ。
### 知らないとする誤判断
正規化されたschemaだけで、並行性・外部副作用・災害回復も正しいと思う。
### 次章接続
最後に、理論不足から生じる典型的な設計判断を反省可能な形にする。

## 第29章 この分野を知らないエンジニアが陥りやすい誤判断
### 章を学ぶ理由
製品別tipsでなく、再発する誤った仮説を優先度順に除く。
### 現場の問題
局所症状へ対処しても、データモデル・履歴・故障モデルの欠落が残る。
### 中心概念と正式定義
判断は `不変条件、許容履歴、failure model、workload` の四前提を明示して評価する。
### 直感→図解→数式→例
`症状→仮説→反証証拠→構造的対策`。例えば遅延なら「index不足」より前にwait、actual/estimate、I/O、lockを切り分ける。
### 実装または疑似コード
```text
assert invariants; replay concurrent histories; inject failures;
measure workload distribution; record assumptions in ADR
```
### よくある誤解
以下は万能規則でなく、括弧内の仮説を現場証拠で採否判断する。
### 誤判断カタログ（優先度順、24例）
1. **Countermeasure: DB制約へ不変条件を置く**（全writerが同じアプリ検証を通るという誤仮説）。
2. **Countermeasure: 許容履歴から分離levelを選ぶ**（transactionなら全実行が直列化されるという誤仮説）。
3. **Countermeasure: commit結果不明を冪等に照会する**（timeoutはabort確定という誤仮説）。
4. **Countermeasure: 外部副作用をoutbox等で接続する**（DB rollbackが外部APIも戻すという誤仮説）。
5. **Countermeasure: 業務FDからkeyを定める**（連番PKが自然キー重複も防ぐという誤仮説）。
6. **Countermeasure: 事実を正規化し派生同期を設計する**（JOIN削減の複製が無料という誤仮説）。
7. **Countermeasure: NULL・bag込みでSQL同値性を検証する**（関係代数の書換えがSQLでも無条件同値という誤仮説）。
8. **Countermeasure: `ORDER BY`と一意tie-breakerを置く**（格納順が安定という誤仮説）。
9. **Countermeasure: actual/estimated rowsとwaitを調べる**（短いSQLは小さい計算という誤仮説）。
10. **Countermeasure: workload全体でindex費用を測る**（index追加はreadだけ改善しwriteへ無影響という誤仮説）。
11. **Countermeasure: 複合indexをpredicate/order形で設計する**（列を含めば順序不問という誤仮説）。
12. **Countermeasure: 統計・相関・skewを更新する**（optimizerは常に最適planを知るという誤仮説）。
13. **Countermeasure: wait-for graphと取得順を直す**（deadlock timeout増加が根治という誤仮説）。
14. **Countermeasure: 長期snapshotを隔離する**（MVCC readは運用コストなしという誤仮説）。
15. **Countermeasure: durability pointと故障範囲を定義する**（ACID Dがsite lossと誤削除も守るという誤仮説）。
16. **Countermeasure: restoreを定期実演する**（backup成功ログが復旧可能性を証明するという誤仮説）。
17. **Countermeasure: replica lagとsession保証を契約化する**（read replicaは常に最新という誤仮説）。
18. **Countermeasure: backupを複製と別系統にする**（replicaが論理誤操作にも耐えるという誤仮説）。
19. **Countermeasure: shardの最大値・skew・再配置を試算する**（hashすれば常に均等という誤仮説）。
20. **Countermeasure: timeoutをunknown outcomeとして扱う**（分散呼出しの失敗は確定状態という誤仮説）。
21. **Countermeasure: consistencyを履歴で指定する**（eventualは一定秒後最新という誤仮説）。
22. **Countermeasure: schema evolution契約を持つ**（schema-lessはschema管理不要という誤仮説）。
23. **Countermeasure: tailとsaturation kneeで容量化する**（平均latencyと平均tenantが代表という誤仮説）。
24. **Countermeasure: 原因・増幅器・症状を因果graphで分ける**（最後のエラーが根因という誤仮説）。
### 実務接続
設計レビュー、incident、migration、capacity、DRで四前提とカタログを使う。
### 要点
- 制約を状態述語で書く。 - 履歴を具体化する。 - 故障範囲を分ける。 - workload分布で測る。 - 対策をschema/protocol/運用へ固定する。
### 誤解チェック（5問）
1. ACIDなら業務制約自動か。2. timeoutなら失敗確定か。3. replicaはbackupか。4. indexは無料か。5. eventualに期限があるか。
### 基礎問題（5問）
1. 自systemの不変条件を書け。2. anomalyを一つ描け。3. durability範囲を書け。4. workload分布を示せ。5. restore証拠を確認せよ。
### 応用問題（3問）
1. 過去障害を24項目へ分類せよ。2. 一誤仮説を反証する実験を作れ。3. 構造的countermeasureをADR化せよ。
### 設計問題（1問）
DB設計レビューtemplateを四前提、反例、検証証拠付きで作成せよ。
### 調査課題（1問）
公開postmortemを読み、当時暗黙だったDB仮説を抽出せよ。
### 知らないとする誤判断
このカタログ自体を製品横断の絶対解とし、実装仕様と証拠を確認しない。
### 次章接続
分散システム編では、DBで現れた合意・時間・partial failureを一般化する。

## 参考文献・一次資料（2026-08-27確認）

- E. F. Codd, “A Relational Model of Data for Large Shared Data Banks,” *CACM*, 1970.
- Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*.
- Philip A. Bernstein, Vassos Hadzilacos, Nathan Goodman, *Concurrency Control and Recovery in Database Systems*.
- [PostgreSQL 18: SQL Language（index、transaction、EXPLAIN等）](https://www.postgresql.org/docs/current/sql.html)
- [PostgreSQL 18: Concurrency Control / MVCC](https://www.postgresql.org/docs/18/mvcc.html)
- [PostgreSQL 18: Write-Ahead Log](https://www.postgresql.org/docs/current/wal.html)
- [PostgreSQL 18: Index Types](https://www.postgresql.org/docs/current/indexes-types.html)
- ISO/IEC 9075（SQL。版・適合範囲は各DBの公式適合表で確認すること）。

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **データベースは不変条件の執行者:** DBは単なる永続化先ではなく、許される状態の集合を制約で定義し、すべてのwriterに対して守る境界である。正式にはschema・key・参照整合性・述語制約が状態空間を狭め、transactionが許容状態間の遷移になる。実務ではAPIの都合から表を作る前に業務不変条件を書き、DB制約・protocol・外部副作用のどこが各条件を執行するか割り当てる。
2. **transactionはコードブロックでなく履歴:** 正しさは個々のtransactionを単独で読むだけでなく、複数実行のread/writeが交差した履歴で判定する。serializability、snapshot isolation、read committedなどは許容する履歴の集合が異なり、commitは業務上の一括成功や外部APIの成功まで自動では意味しない。実務では具体的な競合履歴とunknown outcomeを描いてから分離level、lock、冪等性、outboxを選ぶ。
3. **論理モデルと物理実行を分離する:** relationとqueryの意味は、heap、B-tree、join順、partition、replicaといった物理配置から独立して記述できる一方、性能は物理実行に依存する。optimizerは同値な候補から統計に基づいてplanを選ぶため、SQLの短さやindexの存在だけでは費用は決まらない。実務では正しい論理schemaを保ちつつ、実workloadのpredicate・順序・cardinality・waitから物理設計を反復する。
4. **workloadは平均でなく分布と相関:** DB負荷はquery種類、tenant skew、hot key、burst、read/write比、長期transactionの混合で決まる。Littleの法則やqueueingの見方では、saturationへ近づくと小さな到着率増加がtail latencyを急増させ、平均的な行やtenantは代表にならない。実務では上位頻度だけでなく重い少数query、最大tenant、相関したpeak、write amplificationを測って容量とindexを決める。
5. **永続性は故障モデルと復旧証拠の契約:** 「保存した」は、process crash、node loss、site loss、誤削除、credential侵害のどれに耐えるかで意味が変わる。WAL、replication、backup、PITRは異なるfailure domainを覆い、RPO/RTOはrestore演習で初めて検証される。実務ではdurability point、ack条件、copyの独立性、復旧手順、結果不明時の照会方法を一つの契約として設計する。

### 専門家の意見が根本的に分かれる3つの論点

1. **serializableな履歴を既定にするか、弱い分離を意図的に使うか。** **立場A（serializability-first）の最も強い主張:** application開発者が全anomalyを局所的に推論するのは困難であり、DBに直列実行相当の契約を任せる方が不変条件と保守性を長期に守れる。**立場B（必要最小限の分離）の最も強い主張:** 競合が高いworkloadではabort、lock待ち、coordinationが事業上のthroughputや可用性を損ね、交換可能な操作や許容anomalyまで強く直列化する必要はない。判断は、守る不変条件、競合率、retry可能性、latency SLO、操作の可換性、anomalyを制約やprotocolで局所化できるかによって変わる。
2. **正規化された単一の事実を優先するか、読み取り用の重複を積極利用するか。** **立場A（正規化中心）の最も強い主張:** FDに従う単一表現は更新異常を構造的に除き、未知の将来queryにも一貫した意味を提供する。**立場B（意図的な非正規化・materialization）の最も強い主張:** 読み取り形が安定し規模が大きいsystemでは、事前計算と局所配置がlatency・費用・障害分離を桁違いに改善し、同期規約を明示すれば重複は管理可能である。判断は、source of truthを一意に定められるか、staleness許容、更新頻度、再構築可能性、fan-out、運用観測性によって変わる。
3. **単一の強整合な権威へ集約するか、地域・serviceへ状態を分散するか。** **立場A（集約・強整合）の最も強い主張:** 一つの順序と制約執行点は、重複・競合解決・利用者に見える逆行を減らし、障害時の意味を説明可能にする。**立場B（分散・局所自律）の最も強い主張:** 遠距離coordinationは物理的なlatencyとpartition時の停止を避けられず、業務が許すなら局所writeと非同期収束の方が可用性・地域独立性・拡張性を得られる。判断は、操作の可換性、競合頻度、法域とdata locality、partition時に停止できるか、利用者が必要とするsession保証、補償可能性によって変わる。

### 深い理解と暗記を見分ける10の質問

1. 座席予約で「残席を読んでから更新する」二つのtransactionが同時実行される履歴を描き、どの不変条件がどの分離levelで破れうるかを示せ。分離levelの名称だけで挙動を断定せず、採用DBのlocking/MVCCと競合検出の仕様を明記したうえで、制約とprotocolの候補を比較せよ。
2. APIがtimeoutを返した直後、DB側ではcommit済みかもしれない。再試行で二重請求を起こさず、成功も失わない契約を、識別子・照会・状態遷移・外部決済の境界まで設計せよ。
3. 第3正規形のschemaが性能問題を起こしているという主張に対し、正規化を崩す前に集める証拠を挙げよ。非正規化する場合、どちらを真実とし、ずれをどう検出・修復するか示せ。
4. ある複合indexがquery Aを高速化する一方、system全体を遅くするworkloadを構成せよ。列順、write amplification、cache、selectivity、競合を含めて因果を説明せよ。
5. 平均tenantでは十分な容量なのに、一つのtenant追加でtail latencyが崩壊する例を作れ。どの分布と相関を測り、admissionまたは分離をどう設計するか述べよ。
6. read replicaからの読み取りが「たまに古い」という説明では不十分な業務を一つ選び、必要なsession保証と、それを実現するroutingまたはtokenの契約を定義せよ。
7. replicaが3台あり全台正常でも、誤削除から復旧できない理由を説明せよ。同じ設計をnode loss、site loss、操作ミス、credential侵害の4故障で評価し直せ。
8. optimizerのestimated rowsとactual rowsが1000倍違うplanを想定し、統計不足、相関、parameter skewという競合仮説を区別する観測・実験を設計せよ。
9. 二地域からwrite可能な在庫systemについて、強整合を必要とする不変条件と、収束でよい情報を分離せよ。partition中の受付可否を、売り越し損失と停止損失から決めよ。
10. schema migrationがSQL上はrollback可能でも業務上は不可逆になる例を示せ。旧新applicationの共存、data backfill、外部consumer、観測、cutoverの各段階で停止条件を定義せよ。
