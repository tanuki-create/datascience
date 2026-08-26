# プログラミング言語論――構文の背後にある設計判断

対象は複数言語を使えるが言語理論を体系的に学んでいない実務者である。記法よりも「どの意味を、いつ、誰が保証するか」を学ぶ。コード例は説明用であり、製品選定の宗教論にはしない。

## 本書の読み方

各章は現場の現象から始まり、直感、モデル、定義、例、実装、限界へ進む。式中の `e` は式、`v` は値、`Γ` は名前から型への環境、`τ` は型を表す。章末問題には模範解答をあえて付けない。説明可能性こそ理解の検査だからである。

---

## 第1章 プログラミング言語とは何か

### 学ぶ理由・現場の問題

新言語の評価を「速い」「書きやすい」で済ませると、障害時の挙動や保証範囲を誤る。言語は、許されるプログラムの集合（構文）、その意味（意味論）、意味を実現する処理系の契約である。

### 中心概念・正式な定義

直感的には言語は人と機械の合意である。図にすれば `source -> syntax -> meaning -> implementation -> observation`。形式的には構文集合 `P` と、観測可能な振る舞い集合 `B` への部分関数 `⟦·⟧: P ⇀ B` を考える。未定義は構文エラー、型エラー、未規定動作、非停止など、層を区別する必要がある。

```text
x = 1 + 2       # 表層構文
Assign(x, Add(1, 2))  # 抽象構文
store[x := 3]   # 意味の一例
```

同じ抽象操作でもCは機械に近い制御、Pythonは動的なオブジェクトモデル、SQLは宣言的な関係操作を与える。よくある誤解は「言語=コンパイラ」であること。仕様、処理系、標準ライブラリ、エコシステムは別物だが現実のシステムでは相互作用する。

### 章末ワーク

**要点:** ①言語は構文だけではない ②意味と実装を分ける ③未定義の種類を分ける ④抽象構文が表記差を除く ⑤保証には仕様上の主体がある。

**誤解チェック（正誤と理由）:** 1. コンパイル言語は必ず高速 2. 文法が似れば意味も同じ 3. 標準ライブラリは言語仕様そのもの 4. 同一ソースは全処理系で同じ 5. DSLも言語である。

**基礎問題:** 1. 構文・意味・処理系を定義せよ 2. JSONを言語として分析せよ 3. 未定義と未規定を分けよ 4. ASTを描け 5. SQLの観測結果を述べよ。

**応用問題:** 1. API仕様を言語と見なせ 2. 設定言語の失敗を分類せよ 3. 二つの処理系差を調べよ。**設計問題:** 安全なデプロイDSLの構文と意味を設計せよ。**調査課題:** 任意の言語仕様で normative / informative の区別を確認せよ。

**知らないとする誤判断:** ベンチマークを言語本質の優劣と断定する。**次章:** 構文と意味を別々に記述する方法へ進む。

---

## 第2章 Syntax と Semantics

### 学ぶ理由・現場の問題

リファクタ後に構文は通るのに挙動が変わる。構文解析可能性と意味保存は別の性質だからである。

### 中心概念・正式な定義

構文は文法 `G=(N,Σ,P,S)` が生成する文字列、意味論はプログラムへ意味を与える規則である。操作的意味論は状態遷移 `⟨e,σ⟩ -> ⟨e',σ'⟩`、表示的意味論は数学的対象 `⟦e⟧`、公理的意味論は Hoare triple `{P} C {Q}` で性質を表す。

```text
<expr> ::= <int> | <expr> "+" <expr>
⟨1 + 2, σ⟩ -> ⟨3, σ⟩
{x = 1} x := x + 1 {x = 2}
```

直感図は `text --parse--> AST --evaluate under state--> result/state`。`a+b*c` の曖昧性は優先順位で除く。実装ではparserとevaluatorを分離する。誤解は「テストが意味論を定義する」こと。テストは有限の観測で、契約全体ではない。

### 章末ワーク

**要点:** ①構文と意味は独立 ②文法は文字列集合を定める ③操作的意味論は遷移 ④公理的意味論は前後条件 ⑤意味保存が変換の基準。

**誤解チェック:** 1. ASTが同じなら表層構文も同じ 2. 構文妥当なら実行可能 3. テストが仕様を完全化する 4. 最適化は意味を変えてよい 5. 状態を持たない意味論もある。

**基礎問題:** 1. 小さな式文法を書け 2. 曖昧な導出を示せ 3. 一段遷移を書け 4. 前後条件を書け 5. 構文エラーと意味エラーを分類せよ。

**応用問題:** 1. 短絡評価を意味規則化 2. 例外を状態遷移に追加 3. JSON Schemaの保証を分析。**設計問題:** 単位付き式DSLを定義せよ。**調査課題:** ECMAScript仕様で実行意味の記述を探せ。

**知らないとする誤判断:** formatterや型検査だけで挙動保存を保証したと思う。**次章:** 意味が参照する名前と環境を扱う。

---

## 第3章 名前・束縛・スコープ

### 学ぶ理由・現場の問題

クロージャ、モジュール、コールバックで「どの変数か」を誤ると、値ではなく参照規則がバグになる。

### 中心概念・正式な定義

束縛は名前を実体へ対応付けること、スコープは束縛が参照可能なプログラム領域、寿命は実体が存在する時間である。環境 `ρ: Name ⇀ Location` とストア `σ: Location ⇀ Value` を分ければ、`⟦x⟧ρ,σ = σ(ρ(x))`。字句スコープは定義位置、動的スコープは呼出し列から探索する。

```python
x = 10
def make():
    x = 20
    return lambda: x   # 字句環境の x を捕捉
f = make(); assert f() == 20
```

図は `name -> environment -> location -> store -> value`。shadowingとmutationは別である。誤解はスコープと寿命の同一視。実務では依存性注入、Reactの古いclosure、Goのループ変数、モジュール公開範囲に現れる。

### 章末ワーク

**要点:** ①名前と値を分ける ②環境とストアを分ける ③字句位置が参照を決める ④shadowing≠代入 ⑤スコープ≠寿命。

**誤解チェック:** 1. 同名は同じ場所 2. privateなら短命 3. closureは値だけをコピー 4. 動的スコープは実行順に依存 5. alpha変換は挙動を保つ。

**基礎問題:** 1. 各参照の束縛先を示せ 2. shadowing例を書け 3. 環境表を描け 4. free variableを列挙 5. lifetimeを説明。

**応用問題:** 1. stale closureを修正 2. capture-by-value/reference比較 3. module namespace衝突を分析。**設計問題:** 設定値の可視性と寿命を設計。**調査課題:** Rustのshadowingとmove closureを調べる。

**知らないとする誤判断:** 非同期バグを値の更新だけで説明する。**次章:** 名前に許される値の集合を型で記述する。

---

## 第4章 型

### 学ぶ理由・現場の問題

型を「変換が面倒な注釈」と見ると、API境界の不可能状態や変更影響を表現する機会を失う。

### 中心概念・正式な定義

型は値を分類し、許される操作を制約する論理的記述である。型判断 `Γ ⊢ e : τ` は「環境Γで式eは型τ」を意味する。例: `Γ⊢e1:Int, Γ⊢e2:Int` なら `Γ⊢e1+e2:Int`。静的/動的は検査時点、明示/推論は記述方法であり別軸。「strong/weak」は定義が一定せず、暗黙変換や型安全性を個別に述べるべきである。

```text
Γ(x)=Int
────────  (Var)        Γ⊢e1:Int  Γ⊢e2:Int
Γ⊢x:Int                ─────────────────── (Add)
                              Γ⊢e1+e2:Int
```

Hindley–Milner型推論では制約を単一化する。`id(x)=x` は `∀α. α→α`。実務ではschema、nullable、branded type、IDE支援へ接続する。型は業務妥当性の全てを保証しない。

### 章末ワーク

**要点:** ①型は値と操作の分類 ②型判断は文脈依存 ③検査時点と表記は別軸 ④推論も静的検査 ⑤strong/weakを避け具体化。

**誤解チェック:** 1. 動的型付けは型がない 2. 推論は動的 3. 型が通れば業務的に正しい 4. unionは継承と同じ 5. 暗黙変換は型安全性と同義。

**基礎問題:** 1. 型導出木を書く 2. 型エラー位置を示す 3. nullableを型化 4. 型変数を説明 5. nominal/structuralを比較。

**応用問題:** 1. API状態をunion化 2. 単位混同を防ぐ型 3. gradual typingを評価。**設計問題:** 決済状態機械の型を設計。**調査課題:** TypeScriptのsoundness上の非目標を確認。

**知らないとする誤判断:** 注釈量だけで型システムの強さを評価する。**次章:** 型が実行時事故をどこまで排除するかを見る。

---

## 第5章 型安全性

### 学ぶ理由・現場の問題

「型検査済みだから安全」と無限定に主張すると、境界入力、未定義動作、論理バグを見落とす。

### 中心概念・正式な定義

型安全性の典型的な証明は progress（整形式な閉じた式は値か一歩進める）と preservation（`Γ⊢e:τ` かつ `e→e'` なら `Γ⊢e':τ`）である。合わせて well-typed programs do not get stuck。ただし「stuck」にI/O失敗や無限ループを含めるかは意味論次第。

```text
        progress                     preservation
well typed ───────> value | step     type τ + step ───────> type τ
```

Cの範囲外アクセス、TypeScriptの外部JSON、Rustの`unsafe`は保証境界を示す。実装では外部境界でdecodeし、内部では精密な型を保つ。誤解は型安全性=メモリ安全性=セキュリティという連鎖である。

### 章末ワーク

**要点:** ①progress ②preservation ③stuckの定義が必要 ④保証境界を明示 ⑤型安全と業務安全を分ける。

**誤解チェック:** 1. 型安全なら停止する 2. 型安全なら認可も正しい 3. unsafeがあれば全体が無意味 4. decode後の内部再検査は常に必要 5. null排除は事故クラスを減らす。

**基礎問題:** 1. progressを説明 2. preservationを説明 3. stuck例 4. JSON境界を示す 5. memory safetyとの差。

**応用問題:** 1. FFI境界を監査 2. ORM型とDB制約のずれ 3. refinement typeを評価。**設計問題:** 未信頼イベントのdecode層を設計。**調査課題:** 任意言語のsoundness/unsafe仕様を調べる。

**知らないとする誤判断:** 型検査成功を入力検証や認可の代替にする。**次章:** 関数が環境を値として運ぶ仕組みへ進む。

---

## 第6章 関数・クロージャ・高階関数

### 学ぶ理由・現場の問題

callbackやmiddlewareは関数を値として組み立てる。捕捉環境と副作用を読めなければ制御流を誤る。

### 中心概念・正式な定義

第一級関数は生成・引数化・返却・格納できる。クロージャはコードと字句環境の組 `⟨λx.e,ρ⟩`。高階関数は関数を受け取るか返す関数である。適用は `⟨λx.e,ρ⟩ v → e` を `ρ[x↦v]` で評価する。

```python
def retry(n, op):
    for i in range(n):
        try: return op()
        except TransientError:
            if i + 1 == n: raise
```

図は `function value = code + captured environment`。map/filter/foldは反復の制御を抽象化するが、副作用順序や例外を隠す限界もある。実務ではhandler、DI factory、stream処理に現れる。

### 章末ワーク

**要点:** ①関数は値になれる ②closure=code+environment ③高階関数は制御を抽象化 ④捕捉と副作用を追う ⑤合成可能性は契約次第。

**誤解チェック:** 1. closureは無名関数だけ 2. callbackは必ず非同期 3. mapは常に純粋 4. 関数参照と呼出しは同じ 5. 部分適用とカリー化は同じ。

**基礎問題:** 1. free variable列挙 2. closure環境を描く 3. mapを実装 4. foldで合計 5. 高階関数を定義。

**応用問題:** 1. retryの副作用分析 2. decoratorの順序 3. closureメモリ保持を診断。**設計問題:** middleware合成規約を設計。**調査課題:** Python/JS/Rustのcapture差を比較。

**知らないとする誤判断:** callbackの実行時環境を登録時の値コピーと決めつける。**次章:** 関数計算を最小限の体系に削る。

---

## 第7章 Lambda Calculus

### 学ぶ理由・現場の問題

関数型機能の表面構文は多様だが、束縛・適用・置換へ還元すると共通構造が見える。

### 中心概念・正式な定義

項は `e ::= x | λx.e | e e`。評価戦略をまだ固定しないβ簡約は `(λx.e) a → e[x:=a]`、α変換は束縛名の安全な変更、自由変数を捕捉しない置換が必要である。引数を値 `v` に限定するのはCBVの評価規則を加えた場合である。`λx.x` は恒等関数、`λf.λx.f(f x)` は2回適用。

```text
(λx. x) y -> y
(λx. λy. x) y  -- α変換 --> (λx. λz. x) y -> λz. y
```

図は `application -> substitute argument for bound name -> reduced term`。Church encodingはデータも関数で表せることを示す。ただし実言語は型、効果、評価戦略、資源制約を加える。

### 章末ワーク

**要点:** ①三構文だけ ②β簡約は適用 ③α変換は捕捉回避 ④自由/束縛を区別 ⑤実言語の意味核になる。

**誤解チェック:** 1. 変数名は意味を持つ 2. 置換は文字列置換 3. 全項が停止 4. lambdaは無名関数記法だけ 5. 同じ正規形なら計算結果を同一視できる。

**基礎問題:** 1. 自由変数を求める 2. α変換 3. β簡約 4. capture例 5. Church booleanを読む。

**応用問題:** 1. `let`をlambdaへ変換 2. 再帰の固定点を概説 3. 型付き/型なしを比較。**設計問題:** 小さなevaluatorのASTと置換を設計。**調査課題:** simply typed lambda calculusの型規則を調べる。

**知らないとする誤判断:** スコープバグを単なる名前衝突と捉える。**次章:** 同じ項をどの順で評価するかを扱う。

---

## 第8章 Evaluation Strategy

### 学ぶ理由・現場の問題

同じ式でも評価順序により副作用、例外、停止性、資源使用量が変わる。性能問題を構文だけから予測してはいけない。

### 中心概念・正式な定義

call-by-value (CBV) は引数を値にしてから束縛する。call-by-name (CBN) は未評価式を渡し、使うたびに評価し得る。call-by-need は最初の需要時に評価した結果を共有する遅延評価である。これらは引数をいつ評価するかを定めるが、複数引数を左から右に評価するかまではCBVという名称だけでは決まらない。call-by-reference は評価戦略というより変数の場所を渡す引数渡し機構で、混同しない。

```text
(λx. 1) Ω   where Ω loops
CBV: Ωを先に評価して停止しない
CBN/need: xを使わず1になる
```

図は `expression -> evaluation context E[□] -> next redex`。短絡AND、generator、DB query builderも遅延境界を持つ。遅延は不要計算を省ける一方、例外発生位置とメモリ保持を読みにくくする。

### 章末ワーク

**要点:** ①評価順は意味の一部 ②CBVは引数を先に値化 ③needは結果共有 ④referenceは別軸 ⑤効果があると順序が観測可能。

**誤解チェック:** 1. lazyは常に高速 2. eagerなら左から右 3. reference渡し=遅延 4. 純粋式でも停止性は変わり得る 5. generator本体は生成時に全実行。

**基礎問題:** 1. CBVで簡約 2. CBNで簡約 3. needの共有を描く 4. 短絡評価を説明 5. strictnessを定義。

**応用問題:** 1. 遅延I/Oの例外分析 2. 無限列の消費 3. space leakを診断。**設計問題:** 設定式DSLの評価方式を選べ。**調査課題:** HaskellとPython generatorの遅延を比較。

**知らないとする誤判断:** iterable生成時にDBアクセスが完了したと見なす。**次章:** 状態変化を中心に置く命令型モデルへ進む。

---

### 総合演習A（第1〜8章）

外部入力を読む式DSLについて、文法、操作的意味論、名前解決、型判断、progress/preservationの保証境界、closure環境、CBV/CBN/needを一枚の設計へ統合せよ。副作用する引数を二つ持つ式を反例に、評価戦略と左右の評価順を別々に仕様化する。

---

## 第9章 Imperative Programming

### 学ぶ理由・現場の問題

可変状態は機械資源と自然に対応するが、時間を含むため局所コードだけで挙動を判断しにくい。

### 中心概念・正式な定義

命令型プログラムは状態 `σ` を更新する命令列で、代入は `⟨x:=e,σ⟩→σ[x↦⟦e⟧σ]`。逐次合成、分岐、反復を状態遷移として読む。ループ不変条件 `I` は開始前に成立し、本体で保存され、終了条件と合わせ事後条件を導く。

```text
{n >= 0}
i=0; s=0
while i<n:       # I: s=sum(a[0:i]) and 0<=i<=n
  s+=a[i]; i+=1
{s=sum(a[0:n])}
```

図は `σ0 --C1--> σ1 --C2--> ...`。C、Python、Rustはいずれも命令型記述が可能だが、aliasingとmutationの制約が違う。誤解は「命令型=低水準」である。

### 章末ワーク

**要点:** ①状態が時間で変わる ②代入は環境/ストア更新 ③制御流を遷移で読む ④不変条件が反復を説明 ⑤aliasingが局所推論を壊す。

**誤解チェック:** 1. `x=x+1`は数学の等式 2. mutableなら必ず命令型 3. ループテストは証明 4. aliasがなければ更新影響を局所化しやすい 5. SQLは典型的命令型。

**基礎問題:** 1. 状態列を書く 2. 不変条件を提案 3. alias例 4. 前後条件 5. loopを再帰化。

**応用問題:** 1. off-by-oneを不変条件で診断 2. 共有状態を除去 3. iterator変換。**設計問題:** 在庫更新の状態と不変条件を設計。**調査課題:** C/Rustのalias規則を比較。

**知らないとする誤判断:** 逐次コードの見た目だけで共有可変状態を安全とする。**次章:** 状態変化を値変換へ押し出す関数型を見る。

---

## 第10章 Functional Programming

### 学ぶ理由・現場の問題

並行処理や再試行では副作用の場所が信頼性を左右する。純粋な核と効果境界を分ける考え方が役立つ。

### 中心概念・正式な定義

純粋関数は同じ引数へ同じ結果を返し、外部観測可能な副作用を持たない。参照透過性は式をその値で置換しても意味が変わらない性質。永続データ構造は更新時に旧版を保ち構造共有する。

```python
def price(items, tax):               # pure core
    return sum(x.price*x.qty for x in items) * (1+tax)

items = repository.load()            # effectful shell
emit_invoice(price(items, 0.1))
```

図は `effects -> immutable input -> pure transform -> value -> effects`。再帰、高階関数、ADTが合成を支える。一方I/Oは消えず、型やアーキテクチャで境界へ移す。関数型=再帰のみ、という誤解に注意する。

### 章末ワーク

**要点:** ①純粋性は置換可能性 ②不変値は共有しやすい ③効果を境界へ ④構造共有でコピーを抑える ⑤パラダイムは排他的でない。

**誤解チェック:** 1. pure関数は常に高速 2. immutableは毎回全コピー 3. FPはI/O不可 4. lambda使用だけでFP 5. 例外も観測効果になり得る。

**基礎問題:** 1. 副作用列挙 2. 純粋化 3. fold記述 4. 永続list共有を描く 5. 参照透過性を説明。

**応用問題:** 1. 日時/乱数を引数化 2. event handlerをcore/shell分離 3. immutable cache検討。**設計問題:** 請求計算の純粋核を設計。**調査課題:** 任意言語のpersistent collectionを調べる。

**知らないとする誤判断:** 副作用のある処理を安易に再試行・並列化する。**次章:** 状態と振る舞いをオブジェクト境界でまとめる。

---

### 総合演習B（第9〜10章）

同じ請求処理を命令型の状態遷移と、純粋な値変換＋effectful shellで実装する。両者の不変条件、retry可能範囲、alias、I/O順序、test oracleを比較し、どちらか一方のparadigmを絶対視しないADRを書け。

---

## 第11章 Object-Oriented Programming

### 学ぶ理由・現場の問題

継承階層やクラス数をOOPの質とすると、変更理由の異なる責務が密結合する。

### 中心概念・正式な定義

オブジェクトは識別子、状態、メッセージに対する振る舞いをまとめた実体。動的dispatchは実行時受信者により実装を選ぶ。subtypingの核心は代入可能性で、`S <: T` ならTを期待する文脈でSを使って観測契約を破らないこと。継承はコード再利用機構でありsubtypingと同一ではない。

```text
client --message m--> object
                       state + method table
LSP: preconditionを強めず、postconditionを弱めない
```

compositionは能力を部品として委譲する。実務ではdomain entity、UI widget、driver interfaceに現れる。巨大なshared base classは変更軸を結合する。

### 章末ワーク

**要点:** ①object=identity+state+behavior ②dispatchが多態性を作る ③subtypeは契約 ④継承≠subtyping ⑤compositionで変更軸を分ける。

**誤解チェック:** 1. classがあればOOP 2. privateならカプセル化完了 3. 継承は常にis-a 4. overrideは事前条件を強めてよい 5. interfaceも契約を要する。

**基礎問題:** 1. identity/value比較 2. dispatchを追う 3. LSP違反 4. compositionへ変更 5. encapsulation説明。

**応用問題:** 1. ORM entityの責務分析 2. fragile base診断 3. visitor比較。**設計問題:** 複数決済手段の契約を設計。**調査課題:** Java/Go/Rustの多態性を比較。

**知らないとする誤判断:** 継承による重複除去を設計品質と同一視する。**次章:** 閉じたデータの選択肢を型で表す。

---

## 第12章 Algebraic Data Type

### 学ぶ理由・現場の問題

boolean群やnullable fieldsで状態を表すと、表現可能だが意味のない組合せが増える。

### 中心概念・正式な定義

積型 `A×B` はAとBを同時に持ち、和型 `A+B` はどちらか一方を持つ。値の数は `|A×B|=|A||B|`, `|A+B|=|A|+|B|`。再帰型で木やlistを定義する。pattern matchingの網羅性は全variantを処理したか検査する。

```rust
enum Payment { Pending, Authorized{token:String}, Failed{reason:String} }
// bool authorized + nullable token より不可能状態が少ない
```

図は `sum: branch A | branch B`, `product: field A AND field B`。sealed class、Rust enum、TypeScript discriminated unionに現れる。公開variant追加は利用側への変更になる。

### 章末ワーク

**要点:** ①積はAND ②和はOR ③値数で状態空間を見る ④不可能状態を表現不能に ⑤網羅性が変更を伝播。

**誤解チェック:** 1. enumは整数定数だけ 2. unionは全field同時保持 3. nullable二つは常に4状態必要 4. exhaustive matchは将来変更を検出 5. 再帰型は必ず無限値。

**基礎問題:** 1. 値数計算 2. nullableをOption化 3. JSON状態をsum化 4. tree型 5. matchを書く。

**応用問題:** 1. API resultを設計 2. invalid state削減数を計算 3. versioning影響。**設計問題:** ジョブ状態機械をADT化。**調査課題:** Rust enum/Java sealed/TypeScript union比較。

**知らないとする誤判断:** ランタイムvalidationで矛盾状態を恒常的に補修する。**次章:** 型を横断して再利用する抽象化へ進む。

---

## 第13章 Generic Programming

### 学ぶ理由・現場の問題

型ごとのコピーか`any`への退避か、という二択は再利用と安全性を両方損なう。

### 中心概念・正式な定義

parametric polymorphismは型に依存しない一様な処理 `∀α. α→α`、ad-hoc polymorphismは型ごとに実装を選ぶ。bounded polymorphismは必要能力を制約する。型構築子 `F` のvarianceは、`S<:T` のとき `F<S><:F<T>`（共変）、`F<T><:F<S>`（反変）、どちらも導けない（不変）かを示す。関数型 `A→B` は通常Aに反変、Bに共変である。mutable containerは読書きの両位置にTが現れるため通常不変であり、各言語の宣言側・利用側variance規則を確認する。

```text
map : ∀A,B. (A -> B) -> List[A] -> List[B]
Consumer[T] は入力位置なので通常 contravariant
Producer[T] は出力位置なので通常 covariant
```

実装はerasure、monomorphization、dictionary passingなど。誤解はgenerics=テンプレート文字列。実務ではcollections、serializer、DIに現れる。

### 章末ワーク

**要点:** ①parametricは一様性 ②ad-hocは選択 ③boundは能力契約 ④varianceは代入方向 ⑤実装方式にコスト差。

**誤解チェック:** 1. `∀α.α→α`は任意型を変換できる 2. Listは常に共変 3. erasureなら実行時型情報なし 4. monomorphizationはコード量を増やし得る 5. interface制約はad-hoc実装を支える。

**基礎問題:** 1. generic signature 2. bound追加 3. variance判定 4. map型導出 5. 実装方式説明。

**応用問題:** 1. mutable list共変の危険 2. serializer制約 3. zero-cost主張を分析。**設計問題:** 型安全なrepository interfaceを設計。**調査課題:** Java/Go/Rust generics実装を比較。

**知らないとする誤判断:** 共有APIを`any`化して変更影響を隠す。**次章:** 値が実メモリ上で生きる仕組みへ進む。

---

## 第14章 Memory Management

### 学ぶ理由・現場の問題

メモリリーク、use-after-free、GC pauseを単に「言語が遅い」で説明すると、所有権と到達可能性を誤る。

### 中心概念・正式な定義

stackは典型的に呼出しフレームをLIFO管理し、heapは動的寿命の領域。GCはrootから到達可能なobjectを生存とみなす `Live = Reachable(Roots)`。reference countingは参照数0で回収するがcycleに弱い。所有権は資源の破棄責任を一意化し、borrowは所有権を移さず限定参照する。

```text
roots -> A -> B       C <-> D
          reachable   root非到達なら tracing GCは回収
                      RCだけではcycleが残る
```

stack/heapは仕様上保証されない言語もある。Rustのborrow checker、Cのmanual free、Java/PythonのGCは異なる事故集合とコストを選ぶ。外部資源はGC任せにしない。

### 章末ワーク

**要点:** ①寿命と配置を分ける ②GCは到達可能性 ③RCはcycle課題 ④ownershipは破棄責任 ⑤外部資源は明示管理。

**誤解チェック:** 1. localは必ずstack 2. GCならleakなし 3. RCはGCでない 4. ownershipはメモリ専用 5. finalizer時刻は通常保証される。

**基礎問題:** 1. object graphを描く 2. reachable集合 3. RC計算 4. dangling例 5. move/borrow説明。

**応用問題:** 1. closure保持リーク 2. arena適用 3. GC log解釈。**設計問題:** socketとbufferの所有権を設計。**調査課題:** 任意runtimeのGC方式とbarrierを調べる。

**知らないとする誤判断:** RSS増加を即座に未回収objectと断定する。**次章:** 失敗を制御流と型でどう表すかを扱う。

---

## 第15章 Error Handling

### 学ぶ理由・現場の問題

失敗を例外、戻り値、ログで無秩序に表すと、呼出し側は回復可能性と伝播経路を判断できない。

### 中心概念・正式な定義

例外は通常の戻りとは別の非局所制御移動、`Result<T,E>` は成功と失敗の和型 `T+E`、effectは式が値の計算以外に行う観測可能作用の記述である。型付き効果なら `f: A -> B ! {IO, Fail E}` のように能力を表せる。

```rust
fn parse(s: &str) -> Result<Config, ParseError> {
    let raw = decode(s)?; validate(raw)
}
```

図は `callee --return T | raise E--> caller policy`。回復可能な期待内失敗、契約違反、process障害を分ける。catchして継続すること自体は回復ではない。実務ではHTTP status、transaction rollback、retry policyに接続する。

### 章末ワーク

**要点:** ①失敗を分類 ②例外は非局所制御 ③Resultは明示的和型 ④effectは能力記述 ⑤回復方針は境界で決める。

**誤解チェック:** 1. 例外は異常系専用という普遍則 2. Resultなら無視不可 3. catch後ログで回復完了 4. panicは入力validation 5. retry可能性はerror型の一部。

**基礎問題:** 1. 失敗分類 2. 例外経路を描く 3. Result型設計 4. `?`展開 5. effect列挙。

**応用問題:** 1. 二重ログを除去 2. retryable分類 3. cancellation伝播。**設計問題:** 決済APIのerror taxonomyを設計。**調査課題:** Java checked exception/Rust Result/Go error比較。

**知らないとする誤判断:** 例外を握りつぶして可用性を上げたと思う。**次章:** 複数の計算主体と通信モデルへ進む。

---

### 総合演習C（第11〜15章）

plugin APIを、継承またはcomposition、ADTのclosed variants、generic producer/consumerのvariance、plugin資源のownership、`Result<T,E>`と例外、型付きeffectの各軸で設計せよ。失敗variant追加時にcompilerが検出する利用側と、runtime境界でしか検出できない箇所を分ける。

---

## 第16章 Concurrency Model

### 学ぶ理由・現場の問題

`async`、thread、actorを速度向上の同義語とすると、共有状態・順序・failure isolationを誤設計する。

### 中心概念・正式な定義

thread modelは共有アドレス空間と同期、actorは隔離状態とmailbox、CSPはprocess間のchannel通信、async/awaitは中断可能な計算を継続として表す構文・runtime協調である。並行性は実行が重なり得る構造、並列性は物理的同時実行。

```text
threads: T1 -> shared M <- T2
actors:  A --message--> B(mailbox, private state)
CSP:     P --channel rendezvous--> Q
async:   task --await--> scheduler --resume--> task
```

happens-beforeがなければ観測順序を仮定できない。actorでもmessage順、再入、分散故障は残る。CPU-boundとI/O-boundでruntime選択が違う。

### 章末ワーク

**要点:** ①concurrency≠parallelism ②threadは共有 ③actorはmessage ④CSPはchannel ⑤asyncは待機を構造化。

**誤解チェック:** 1. asyncは別CPUで実行 2. actorならrace皆無 3. channelならdeadlockなし 4. threadはprocessより必ず軽い 5. cancellationもprotocol。

**基礎問題:** 1. 四モデル比較 2. race例 3. mailbox順序 4. await点列挙 5. backpressure説明。

**応用問題:** 1. UI thread freeze診断 2. actor再入事故 3. structured concurrency評価。**設計問題:** crawlerの並行モデルを選べ。**調査課題:** Go/C#/Erlangのschedulerを比較。

**知らないとする誤判断:** async化だけでCPU処理が並列高速化すると期待する。**次章:** 抽象モデルを動かすruntimeを見る。

---

## 第17章 Language Runtime

### 学ぶ理由・現場の問題

起動、warm-up、pause、FFIのコストはソース言語ではなくruntime実装から生じる。

### 中心概念・正式な定義

interpreterは表現を逐次解釈し、VMは抽象命令セットを実行、JITは実行時profileに基づきnative codeへ変換する。AOTは実行前に変換する。典型pipelineは `source→AST→IR/bytecode→profile→optimized machine code`。

```text
hot call site -> type feedback -> speculative optimization
guard failure -> deoptimization -> generic execution
```

JITは仮定をguardし外れればdeoptする。GC、scheduler、loader、FFIもruntimeである。「interpreterだからコンパイルしない」は誤りで内部bytecode化し得る。observabilityではwall time、CPU、allocation、GC、deoptを分離する。

### 章末ワーク

**要点:** ①runtimeは意味実現層 ②VMは抽象機械 ③JITはprofile利用 ④仮定外れでdeopt ⑤性能はpipeline全体。

**誤解チェック:** 1. AOTならruntimeなし 2. JITは必ずAOTより速い 3. bytecodeは機械語 4. warm-upはGCだけ 5. FFIは境界コストを持つ。

**基礎問題:** 1. pipelineを描く 2. VM定義 3. hotness説明 4. deopt理由 5. loader役割。

**応用問題:** 1. tail latencyとJIT 2. benchmark warm-up設計 3. FFI overhead分析。**設計問題:** serverless向けruntime選択。**調査課題:** CPython/V8/JVMの実行pipelineを比較。

**知らないとする誤判断:** microbenchmarkの初回値で言語性能を断定する。**次章:** sourceから実行表現を作るcompilerへ進む。

---

## 第18章 Compiler入門

### 学ぶ理由・現場の問題

compilerを機械語変換器だけと思うと、静的解析、transpiler、query optimizerの共通構造が見えない。

### 中心概念・正式な定義

compilerはsource languageからtarget languageへ意味を保存する変換 `C:P_s→P_t` で、望ましくは `⟦C(p)⟧_t ≈ ⟦p⟧_s`。front endはlex/parse/type、middle endはIR解析・最適化、back endは命令選択・割付・出力を担う。

```text
source -> tokens -> AST -> typed IR -> SSA -> optimized IR -> target
                         def-use / CFG        register allocation
```

SSAでは各変数が一度だけ定義され、data flowが明瞭になる。最適化は観測意味を保たねばならず、浮動小数、並行性、未定義動作が境界となる。source mapやdebug infoも契約である。

### 章末ワーク

**要点:** ①compilerは意味保存変換 ②front/middle/back分離 ③IRが解析基盤 ④最適化には観測同値 ⑤debug情報も成果物。

**誤解チェック:** 1. compiler targetは機械語だけ 2. optimizerは常に高速化 3. dead code判定にeffect不要 4. SSAはsource変数名 5. UBは最適化へ影響。

**基礎問題:** 1. 各phase説明 2. AST作成 3. CFG作成 4. SSA変換 5. constant folding。

**応用問題:** 1. effectful式の除去可否 2. overflow最適化 3. source map設計。**設計問題:** 小DSL compilerのphaseを設計。**調査課題:** LLVM IRまたはWebAssemblyを読む。

**知らないとする誤判断:** 最適化後の低水準挙動をsource順序どおりと断定する。**次章:** 六言語の制約選択を同一軸で比較する。

---

## 第19章 C・Java・Python・JavaScript・Go・Rustの設計比較

### 学ぶ理由・現場の問題

言語比較を構文、人気、単一benchmarkで行うと、保証と運用制約の交換を見誤る。

### 中心概念・正式な定義

同じ軸で比較する: 型検査、メモリ管理、実行モデル、並行モデル、エラー、FFI、互換性。これは優劣表でなく制約表である。

| 言語 | 主な型/実行 | メモリ | 並行性の代表 | 失敗の代表表現 | 主な設計トレードオフ |
|---|---|---|---|---|---|
| C | 静的/典型的にはnative AOT | 手動 | thread | status/`errno`、signal、UB | 制御と移植性、保証境界の責任 |
| Java | 静的/典型的にはJVM | tracing GC | thread/virtual thread | checked/unchecked exception | runtime保証、GC/JIT/warm-up |
| Python | 動的/複数処理系 | CPythonはreference counting＋cycle tracing | async/process/thread | exception | 反復速度、処理系・native extension依存 |
| JavaScript | 動的/host上のengine | tracing GC | event loop/worker | throw/Promise rejection | host差、単一event-loop抽象と非同期 |
| Go | 静的/典型的にはnative | tracing GC | goroutine/channel | `error`/panic | 小さい言語核、runtime/GCとの交換 |
| Rust | 静的/典型的にはnative | ownership＋明示的共有 | thread/async ecosystem | `Result`/panic | 強い静的制約、`unsafe`/FFI境界と学習費用 |

たとえばCの「速さ」は制御可能性であり安全性保証ではない。RustのownershipはGC不在以上のalias制約を与える。JavaScriptのevent loopもhost/runtimeで異なる。この表は仕様が必須化する唯一の実装方式ではなく、代表的処理系の比較である。FFI、binary/source compatibility、package policyは表外の独立軸としてADRに残す。

### 章末ワーク

**要点:** ①同じ評価軸を使う ②仕様と代表処理系を分ける ③保証と責任を対で見る ④ecosystemも制約 ⑤用途から選ぶ。

**誤解チェック:** 1. Cは常に最速 2. Pythonはthread並列不可という言語普遍則 3. JavaScriptは非同期だけ 4. Go channelでrace消滅 5. Rustはunsafeを持たない。

**基礎問題:** 1. 六言語の型軸 2. memory軸 3. error軸 4. runtime軸 5. FFI軸。

**応用問題:** 1. CLI実装選定 2. low-latency server選定 3. data pipeline選定。**設計問題:** 既存組織制約を含むADRを書け。**調査課題:** 各公式仕様で未規定領域を一つ探す。

**知らないとする誤判断:** 機能一覧だけでmigration費用と障害モデルを無視する。**次章:** 未知の言語を評価する再利用可能な方法へ進む。

---

## 第20章 新しい言語を評価する方法

### 学ぶ理由・現場の問題

採用後に初めてtooling、運用、相互運用、semantic versioningの制約が見えると、言語機能以上の負債になる。

### 中心概念・正式な定義

評価を `問題制約→必要保証→言語仕様→処理系→ecosystem→組織能力→実験` の順で行う。評価関数を単純化すれば `fitness = benefits - (runtime risk + integration cost + learning/operation cost)` だが、数値は比較の論点を明示する道具で真理ではない。

```text
workload: latency / throughput / footprint / safety / portability
failure: crash / pause / data race / supply chain / debugability
lifecycle: build / test / deploy / observe / upgrade / retire
```

representative workloadでprototypeし、steady-stateだけでなくbuild、起動、tail、failure injection、profile可用性を測る。採用しない判断も成果である。

### 章末ワーク

**要点:** ①問題から始める ②必要保証を明記 ③仕様/実装/ecosystem分離 ④failureで試す ⑤撤退条件を先に置く。

**誤解チェック:** 1. GitHub人気が保守性 2. benchmarkが全workload代表 3. 型機能が多いほど適合 4. prototype成功で運用検証完了 5. team能力も設計制約。

**基礎問題:** 1. 評価軸作成 2. 保証主体分類 3. lifecycle列挙 4. 撤退条件 5. benchmark脅威。

**応用問題:** 1. 新言語ADR 2. migration pilot設計 3. ecosystem集中リスク。**設計問題:** 3候補のweighted decision recordを作る。**調査課題:** 一言語のrelease/compatibility/security policyを読む。

**知らないとする誤判断:** 構文の生産性をシステム寿命全体の費用と同一視する。**次章:** 全概念を誤判断の形で再点検する。

---

## 第21章 この分野を知らないエンジニアが陥りやすい誤判断

### 学ぶ理由・現場の問題

知識は用語再生でなく判断修正に使う。本章は設計レビューで検出すべき高頻度の誤りを、原因仮説の優先順でまとめる。

### 中心概念・20の誤判断

1. **型検査成功=入力も業務も正しい**――型保証の境界を無視。境界decodeとdomain invariantを分ける。
2. **`async`=CPU並列化**――中断可能性と同時実行を混同。schedulerとworkloadを確認する。
3. **GC=リークしない**――到達可能だが不要なobjectは残る。保持経路を調べる。
4. **例外をcatch=回復**――状態修復と補償がない。回復契約を境界に置く。
5. **classを使えばOOP**――object契約でなく構文を評価。責務と代入可能性を見る。
6. **継承=再利用の標準解**――変更軸を結合。compositionを比較する。
7. **動的型=型がない**――検査時点を混同。runtime分類と失敗地点を述べる。
8. **型推論=動的型**――注釈と検査時点を混同。導出される静的制約を見る。
9. **strong/weakで十分**――定義が曖昧。暗黙変換、soundness、memory safetyを個別化する。
10. **closureは値のsnapshot**――捕捉規則を無視。環境/場所/値を追う。
11. **遅延評価は高速**――再評価・保持・例外遅延を無視。需要と共有を測る。
12. **関数型は副作用禁止**――配置と表現を混同。pure core/effect boundaryで考える。
13. **immutable=全コピー**――構造共有を無視。更新経路とallocationを測る。
14. **generics=`any`の便利版**――parametricityを無視。許される操作の制約を見る。
15. **compiler=sourceから機械語**――target一般性を見落とす。意味保存変換として捉える。
16. **最適化後もsource順**――観測同値とreorderingを無視。memory/effect modelを読む。
17. **interpreter=コンパイルなし**――内部IRを無視。実行pipelineを確認する。
18. **言語benchmark=システム性能**――runtime、library、I/O、warm-upを混在。bottleneck別に測る。
19. **新言語の機能数=適合度**――組織/運用制約を無視。lifecycle全体でADRを書く。
20. **言語が安全ならシステムも安全**――認可、protocol、配置、運用は外部。保証合成を設計する。

図にすると `surface claim -> hidden semantic assumption -> runtime/operation observation` を常に辿る。正式には、採用判断は観測したい性質 `Q` に対し、仕様と実装の仮定集合 `A` から `A ⊢ Q` を説明できるかで検査する。

### 章末ワーク

**要点:** ①保証境界を問う ②構文と意味を分ける ③仕様と処理系を分ける ④正常系とfailureを測る ⑤技術選定は制約適合。

**誤解チェック:** 1. 上記から自分が最近信じたものを一つ反証せよ 2. 型安全とsecurityを区別 3. asyncとparallelを区別 4. GCとresource管理を区別 5. benchmarkの外的妥当性を説明。

**基礎問題:** 1. 20例を保証/実行/運用に分類 2. 三例へ反例 3. 用語の曖昧さを特定 4. 境界図を描く 5. 一例を同僚へ説明。

**応用問題:** 1. 自社障害を意味モデルで再分析 2. 言語migration失敗を分析 3. 二言語の保証合成を比較。**設計問題:** 未知の言語を評価するレビュー票と撤退基準を作れ。**調査課題:** 実際の言語仕様・runtime issue・CVEを一つ結び付けて説明せよ。

**知らないとする誤判断:** 個別機能の知識を、保証の構成を説明できることと同一視する。**次の学習:** 離散数学で論理、OSで実行資源、オートマトンで言語クラス、並行分散で順序保証を深める。

---

## 総合演習

1. **式DSL:** 文法、型規則、操作的意味論、error、評価戦略、compiler pipelineを一貫して設計する。
2. **plugin runtime:** memory ownership、FFI、sandbox、versioning、observabilityを含む実行基盤ADRを書く。
3. **障害分析:** 非同期handlerが古いclosureを捕捉し、例外を握りつぶし、GC rootから保持された事例を、名前・効果・並行性・memoryの四層で分析する。
4. **言語選定:** C/Java/Python/JavaScript/Go/Rustから二つを候補にし、代表workloadとfailure injectionを含む検証計画を作る。

## 参考文献への道標

- 各言語の公式language specification。解説記事より先に保証文言を読む。
- [The Java Language Specification, Java SE 26](https://docs.oracle.com/en/java/javase/26/docs/specs/jls/index.html)――CBVという一般分類と、Javaが別途定める左から右のoperand/argument評価順を区別する。
- [The Rust Reference: Type coercions](https://doc.rust-lang.org/reference/type-coercions.html)――subtyping、coercion、unsizingを同じ語でまとめない。
- Benjamin C. Pierce, *Types and Programming Languages*。
- Robert Harper, *Practical Foundations for Programming Languages*。
- Andrew W. Appel, *Modern Compiler Implementation*。

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **構文・意味・観測の三層** 直感的には、同じ見た目の構文でも言語が約束する意味と処理系で観測される挙動は別物である。正式には、構文を意味領域へ写す規則と、プログラムの観測同値性を定め、最適化や実装差がその同値性を保つかを考える。実務では、言語仕様、compiler/runtimeの選択、benchmark結果を分離し、「何が保証で何が偶然か」を判断する。
2. **型は可能なプログラムを制限する論理である** 直感的には、型は値のラベルではなく、許される操作と到達できない失敗を表す。正式には、typing judgmentと型保存・進行などの性質を通じて、静的または動的検査がどの不変条件をどの境界まで保証するかを見る。実務では、domain model、API、generics、FFIの境界を設計し、型で排除する誤りとruntime検証すべき外部入力を分ける。
3. **評価順序と効果の相互作用** 直感的には、式の値だけでなく「いつ、何回、どの順で何が起きるか」がプログラムの意味になる。正式には、評価戦略、effect、例外、非決定性、並行性を状態遷移として追い、reorderingが許される観測範囲を定める。実務では、遅延評価、`async`、callback、最適化、transaction境界で、順序依存と二重実行を見抜く。
4. **名前は環境・場所・寿命へ解決される** 直感的には、変数名そのものが値なのではなく、scopeとbindingが環境またはstorage上の対象を選ぶ。正式には、lexical environment、closure、alias、ownership、lifetimeを区別し、到達可能性と更新可能性を追跡する。実務では、古いclosure、共有可変状態、use-after-free、GCによる保持、module境界の不具合を同じモデルで診断する。
5. **抽象化境界は表現を隠し、局所的な保証を合成可能にする** 直感的には、利用側が実装の全状態を知らなくても、公開された契約だけで正しく推論できることが大規模programを成立させる。正式には、module、abstract data type、parametricity、representation invariantを用い、内部表現を変えても観測可能な振る舞いが保存されるかを見る。実務では、API、module、FFIの境界ごとに仮定と保証を接続し、別実装への置換、独立したtest、段階的migrationが可能かを判断する。

### 専門家の意見が根本的に分かれる3つの論点

1. **強い静的型付けを中心に置くか、動的検査と漸進的制約を中心に置くか**
   - **立場A――可能な誤りをcompile時に広く排除する。** 最も強い主張は、大規模変更で全経路を人間が追えなくても、machine-checkableな不変条件が局所変更の影響を全体へ伝え、長期保守と安全なrefactoringを可能にするというものだ。
   - **立場B――runtimeの値と利用実態から制約を成長させる。** 最も強い主張は、要件探索中や異質なデータ境界では静的modelが現実より先に固定され、誤った抽象化の費用を高めるため、動的検査、test、漸進的typingの方が知識の変化へ忠実だというものだ。
   - 判断は、変更規模、domainの安定性、失敗費用、latency要件、tooling、team構成、外部dataの比率、段階的migrationの可否で変わる。
2. **追跡型の自動memory管理を中心に置くか、所有権に基づく決定的なresource管理を中心に置くか**
   - **立場A――GCなどに到達可能性の追跡と回収を任せる。** 最も強い主張は、aliasやcycleを含む一般的なobject graphの寿命を各programmerへ管理させること自体が主要な欠陥源であり、collectorの費用を払っても安全性、表現力、開発速度の総利益が大きいというものだ。
   - **立場B――ownership、lifetime、scope終了時の解放を型またはprogram構造へ組み込む。** 最も強い主張は、memory以外の有限resource、予測可能な停止時間、局所的な解放時点は到達可能性だけでは契約できず、所有権を明示すれば手動解放に依存せず安全性と制御を両立できるというものだ。
   - 判断は、pause/footprint制約、object graphの複雑さ、resourceの種類、FFI、real-time性、検証能力、開発期間で変わる。
3. **効果を型と純粋性で隔離するか、直接的な命令的表現を認めるか**
   - **立場A――pure coreと明示的effectを言語設計の中心に置く。** 最も強い主張は、参照透過性とeffectの型付けにより、局所推論、並列化、test、retryの安全性を構造的に得られ、隠れた順序依存を減らせるというものだ。
   - **立場B――効果を通常の計算として直接記述する。** 最も強い主張は、実システムはI/O、状態、例外、並行性そのものであり、それらを高度な抽象へ持ち上げると制御flow、性能、debug時の因果が読みにくくなり、抽象の誤用という別の複雑さを生むというものだ。
   - 判断は、domainに占める効果の割合、再試行や並列化の必要性、抽象化を支える型機能、性能予測、teamの習熟度、debugging環境で変わる。

### 深い理解と暗記を見分ける10の質問

1. source上で同じ値を返す二つの式が、例外、logging、並行実行を加えると同値でなくなる例を作り、どの観測を意味に含めるべきか説明せよ。
2. 型検査を通る認可処理が越権を許した。型安全性が保証したこととしなかったことを分離し、domain invariantをどの境界へ置き直すか示せ。
3. lexical scopeを採る言語でcallbackが古い設定値を読む障害を、名前、環境、場所、値、寿命の五つを使って説明し、単なる再代入以外の設計修正を提案せよ。
4. call-by-valueから遅延評価へ一部を書き換えると、性能と例外発生時点が逆方向に変化する事例を構成せよ。共有の有無と保持される環境も分析せよ。
5. GC言語でmemory使用量が増え続ける。collectorの欠陥と断定せず、到達可能だが不要なobject、native resource、allocator、cacheを識別する調査を設計せよ。
6. 動的型のprototypeを静的型のproduction codeへ移す判断について、静的型が増やす保証と、誤ったmodelを固定する危険を同時に評価するpilotを設計せよ。
7. compiler最適化でsourceの読み書き順が変わってもよい条件を、single-thread、data race、I/O effectの三事例で比較し、必要なmemory/effect modelを述べよ。
8. 制約のないparametric polymorphismを使う関数が型変数の値へ行える操作が限られることから、実装についてどのfree theoremを導けるか。reflectionや型caseがその推論を壊す例と、型class相当の制約を明示したときに導ける命題がどう変わるかを区別せよ。
9. FFIを介してmemory-safeな言語からnative libraryを呼ぶとき、各層の保証がどこで切れるか。ownership、例外、thread、ABI、入力検証を含む境界契約を書け。
10. 新言語の短いbenchmarkが既存言語より速かったとしても採用を決められない理由を、仕様・処理系・library・workload・運用・撤退費用に分解し、反証可能な評価計画を示せ。
