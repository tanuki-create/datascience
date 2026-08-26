# 確率・統計――不確実性を扱うエンジニアの基礎

## はじめに

統計は「数字から確信を作る技術」ではなく、観測生成過程、ばらつき、選択、測定誤差を明示して、どこまで言えるかを制御する技術である。本書では確率変数を大文字 \(X\)、実現値を小文字 \(x\)、標本数を \(n\) と書く。コードは Python と標準的な数値ライブラリを想定するが、必ずモデルの仮定を先に述べる。

---

## 第1章　なぜエンジニアに確率が必要なのか

### この章を学ぶ理由／現場の問題

レイテンシ、障害、ユーザー行動、ベンチマークは同条件でも変動する。単一の平均や直近値で判断すると、偶然・選択バイアス・構造変化を原因と誤認する。

### 中心概念と正式な定義

不確実性には、反復で変わる偶然変動（aleatory）と、モデル・測定・知識不足（epistemic）がある。統計的推論は、観測 \(D\) を確率モデル \(P_\theta\) が生成したと仮定し、未知量 \(\theta\) または将来観測を推論する。母集団は関心対象全体、標本は観測された部分、estimand は知りたい量である。

### 直感 → 図解 → 数式 → 例 → 実装

```text
real process -> sampling/measurement -> data -> model -> decision
                   bias                 uncertainty      loss
```

意思決定 \(a\) は推定値だけでなく損失 \(L(a,\theta)\) を用い、期待損失 \(E[L(a,\theta)]\) を比較する。障害率が同じ推定値でも、誤警報と見逃しの費用でアラート閾値は変わる。

```python
def choose(actions, scenarios, prob, loss):
    return min(actions, key=lambda a: sum(prob[s] * loss(a, s) for s in scenarios))
```

### よくある誤解／実務接続

- データ量が多くても偏った観測は偏ったまま。
- ランダムは「原因がない」ではなくモデル上の不確実性表現。
- 精密な小数は正確さを保証しない。
- SRE、容量計画、実験、ML、品質管理は同じ推論骨格を持つ。

### 要点

1. 観測値と生成過程を分ける。 2. 母集団・標本・estimand を明示する。 3. 変動と知識不足を区別する。 4. 推論には仮定がある。 5. 判断には損失も必要。

### 誤解チェック（5問）

1. 標本数が大きければ代表性は自動的に得られるか。 2. 平均が同じなら分布も同じか。 3. ランダムとは無原因か。 4. 推定値は真値か。 5. 最も確率が高い行動が常に最適か。

### 基礎問題（5問）

1. API 障害調査の母集団を定義せよ。 2. estimand を三つ挙げよ。 3. 偶然変動と測定誤差を分けよ。 4. 欠測の生成理由を列挙せよ。 5. 誤警報と見逃しの損失表を作れ。

### 応用問題（3問）／設計問題／調査課題

1. 成功リクエストだけの latency 分析を批判せよ。 2. 大規模だが偏った標本を例示せよ。 3. 不確実性を含むリリース判断を書け。 **設計:** SLA 違反予測の観測生成図を設計せよ。 **調査:** 社内ダッシュボード一つの estimand を確認せよ。

### 知らないとする誤判断／次章への接続

ノイズを改善効果と読み、直近の一点でロールバックする。次章では不確実性を集合と測度で形式化する。

---

## 第2章　確率の基本

### この章を学ぶ理由／現場の問題

「0.1%障害」の分母、事象、期間が曖昧なら数値は比較できない。確率空間は、起こり得る結果と関心ある事象を固定する。

### 中心概念と正式な定義

確率空間は \((\Omega,\mathcal F,P)\)。標本空間 \(\Omega\)、事象の \(\sigma\)-加法族 \(\mathcal F\)、確率測度 \(P\) は \(P(\Omega)=1\)、\(P(A)\ge0\)、互いに素な \(A_i\) について \(P(\cup_i A_i)=\sum_iP(A_i)\) を満たす。補集合は \(P(A^c)=1-P(A)\)、和は \(P(A\cup B)=P(A)+P(B)-P(A\cap B)\)。

### 直感 → 図解 → 数式 → 例 → 実装

```text
Ω: all requests
[ A: timeout ] overlaps [ B: HTTP 5xx ]
```

1000件中 timeout 20、5xx 30、両方10なら経験確率は \(P(A\cup B)=(20+30-10)/1000=.04\)。

```python
def union_rate(a, b, both, n):
    return (a + b - both) / n
```

頻度は確率の推定であり、同一物ではない。

### よくある誤解／実務接続

- 互いに素と独立は別。互いに素な非零事象は独立でない。
- 分母をリクエスト、ユーザー、日で混ぜない。
- `1 - small_probability` の浮動小数精度にも注意する。
- 可用性の合成、リスク和、キャッシュヒットに集合則が現れる。

### 要点

1. 事象は結果集合。 2. 確率は測度。 3. 全事象の確率は1。 4. 重複は包除で引く。 5. 分母・期間・単位を固定する。

### 誤解チェック（5問）

1. 排反なら独立か。 2. \(P(A\cup B)=P(A)+P(B)\) は常に成り立つか。 3. 観測頻度=真の確率か。 4. 確率は負になり得るか。 5. 事象と結果は同じか。

### 基礎問題（5問）

1. サイコロの空間を定義せよ。 2. 補集合確率を計算せよ。 3. 二障害の和事象を計算せよ。 4. 排反事象を例示せよ。 5. 分母違いの rate を修正せよ。

### 応用問題（3問）／設計問題／調査課題

1. 少なくとも一台失敗の確率を補集合で求めよ。 2. inclusion-exclusion を三事象へ拡張せよ。 3. request と user probability を比較せよ。 **設計:** エラー率イベントの仕様を作れ。 **調査:** メトリクス一つの分母と欠測処理を確認せよ。

### 知らないとする誤判断／次章への接続

重なるエラー種別を足して障害率を過大評価する。次章では情報を得た後に確率を更新する。

---

## 第3章　条件付き確率

### この章を学ぶ理由／現場の問題

全体平均は、地域・端末・バージョンによる条件差を隠す。観測条件を明示しなければ Simpson のパラドックスを招く。

### 中心概念と正式な定義

\(P(B)>0\) のとき \(P(A\mid B)=P(A\cap B)/P(B)\)。積の法則は \(P(A\cap B)=P(A\mid B)P(B)\)。A,B が独立とは \(P(A\cap B)=P(A)P(B)\)、同値に正確な条件下で \(P(A\mid B)=P(A)\)。全確率は分割 \(B_i\) に対し \(P(A)=\sum_iP(A\mid B_i)P(B_i)\)。

### 直感 → 図解 → 数式 → 例 → 実装

```text
all requests Ω -> restrict to mobile B -> timeout slice A∩B
```

mobile 400件中 timeout 20なら \(P(A\mid B)=.05\)。desktop 600件中6なら .01。全体 .026 だけでは差を隠す。

```python
def conditional(rows, event, condition):
    subset = [r for r in rows if condition(r)]
    return sum(event(r) for r in subset) / len(subset)
```

### よくある誤解／実務接続

- \(P(A|B)\) と \(P(B|A)\) は通常異なる。
- 条件を細分化しすぎると標本が疎になる。
- 観測した変数で条件付けること自体が collider bias を生む場合がある。
- feature flag、地域障害、セグメント分析に直結する。

### 要点

1. 条件付き確率は標本空間の制限。 2. 積の法則で同時確率を分解。 3. 独立は確率分解の性質。 4. 全確率で層を合成。 5. 条件選択にもバイアスがある。

### 誤解チェック（5問）

1. \(P(A|B)=P(B|A)\) か。 2. 排反は独立か。 3. 全体率だけで層別率を推測できるか。 4. 条件を増やせば常に良いか。 5. 相関なしは独立か。

### 基礎問題（5問）

1. 表から条件付き率を求めよ。 2. 積の法則で同時率を求めよ。 3. 独立性を検査せよ。 4. 全確率で全体率を復元せよ。 5. Simpson 例を構成せよ。

### 応用問題（3問）／設計問題／調査課題

1. version と region の交互作用を分析せよ。 2. collider 条件付けの例を描け。 3. 欠測条件下の率を批判せよ。 **設計:** 障害率ダッシュボードの層別軸を設計せよ。 **調査:** 実データで全体と層別の方向が異なる例を探せ。

### 知らないとする誤判断／次章への接続

障害中に集まった成功ログだけを条件にし、失敗率が下がったと判断する。次章では条件を逆向きに更新する Bayes 則を学ぶ。

---

## 第4章　Bayes の定理

### この章を学ぶ理由／現場の問題

検査の感度が高くても、基礎率が低ければ陽性の大半が偽陽性になり得る。アラート、異常検知、セキュリティ診断には逆確率が必要である。

### 中心概念と正式な定義

\(P(B)>0\) で \(P(A\mid B)=P(B\mid A)P(A)/P(B)\)。分割 \(A_i\) なら \(P(A_i\mid B)=P(B\mid A_i)P(A_i)/\sum_jP(B\mid A_j)P(A_j)\)。\(P(A)\) は事前、\(P(B|A)\) は尤度、\(P(A|B)\) は事後、分母は evidence。

### 直感 → 図解 → 数式 → 例 → 実装

障害事前率0.1%、検知感度99%、偽陽性率1%なら、陽性後の障害確率は \(.99*.001/(.99*.001+.01*.999)\approx9.0\%\)。

```text
1,000,000 runs: 1,000 incidents -> 990 true alerts
                999,000 normal -> 9,990 false alerts
```

```python
def posterior(prior, sensitivity, false_positive):
    return sensitivity*prior / (sensitivity*prior + false_positive*(1-prior))
```

### よくある誤解／実務接続

- \(P(alert|incident)\) を \(P(incident|alert)\) と読まない。
- 尤度はパラメータの確率分布ではない。
- 事前は恣意でよいのではなく、根拠と感度分析が必要。
- alert routing、fraud score、障害診断の優先順位に使う。

### 要点

1. Bayes は条件付き確率の向きを反転。 2. 基礎率が事後を支配する。 3. 感度と偽陽性率を両方使う。 4. 分母は全原因からの evidence。 5. 事前の感度分析が必要。

### 誤解チェック（5問）

1. 99%精度なら陽性の99%が真か。 2. prior=posterior か。 3. 偽陽性率と陽性的中率は同じか。 4. 尤度は合計1か。 5. 事前を隠してよいか。

### 基礎問題（5問）

1. 数値例を再計算せよ。 2. confusion matrix を作れ。 3. 事前率を10倍にせよ。 4. 尤度比を計算せよ。 5. 全確率で分母を導け。

### 応用問題（3問）／設計問題／調査課題

1. 二段アラート更新を計算せよ。 2. 独立でない evidence の二重計上を説明せよ。 3. 事前感度分析を可視化せよ。 **設計:** オンコール向け診断ランキングを設計せよ。 **調査:** 使用中検知器の base rate と precision を調べよ。

### 知らないとする誤判断／次章への接続

感度99%を「アラートの99%が真」と読み、調査資源を浪費する。次章では結果を数値へ写す確率変数を定義する。

---

## 第5章　確率変数

### この章を学ぶ理由／現場の問題

同じ実験から成功、件数、時間など複数の量を取り出す。観測結果と、それを数へ写す変数を区別しないと分布を誤る。

### 中心概念と正式な定義

確率変数 \(X:\Omega\to\mathbb R\) は可測関数。累積分布関数 \(F_X(x)=P(X\le x)\)。離散型は確率質量関数 \(p_X(x)=P(X=x)\)、連続型は密度 \(f_X\) が \(P(a<X\le b)=\int_a^bf_X(x)dx\) を満たす。確率変数の関数 \(Y=g(X)\) も新たな確率変数。

### 直感 → 図解 → 数式 → 例 → 実装

```text
request outcome ω -> X(ω)=latency_ms
                  -> Y(ω)=1{latency > 500}
```

連続変数では \(P(X=x)=0\) でも密度 \(f(x)\) は正になり得る。CDF は離散・連続の両方で使える。

```python
latency = [measure() for _ in range(1000)]
slow = [int(x > 500) for x in latency]
```

### よくある誤解／実務接続

- 確率変数は変動する物理変数そのものではなく結果上の関数。
- 密度の値は確率ではなく1を超えることもある。
- 離散と連続を同じ `P(X=x)` で扱わない。
- histogram の bin は観測・可視化選択であり分布そのものではない。

### 要点

1. 確率変数は結果を数へ写す。 2. CDF は \(P(X≤x)\)。 3. 離散は PMF。 4. 連続は区間積分。 5. 指示変数が件数解析を簡単にする。

### 誤解チェック（5問）

1. 連続変数で点確率は正か。 2. 密度は確率か。 3. CDF は減少し得るか。 4. 同じ Ω に複数変数を定義できるか。 5. histogram=PMF か。

### 基礎問題（5問）

1. request 結果に三変数を定義せよ。 2. Bernoulli PMF を書け。 3. CDF から区間確率を求めよ。 4. 指示変数で失敗件数を書け。 5. 変換 \(Y=2X\) を考えよ。

### 応用問題（3問）／設計問題／調査課題

1. 打切り latency の変数を定義せよ。 2. 混合離散連続分布を例示せよ。 3. 単調変換後の分位点を導け。 **設計:** benchmark outcome schema を設計せよ。 **調査:** 監視 SDK の histogram 境界を確認せよ。

### 知らないとする誤判断／次章への接続

timeout を最大 latency 値と同一視し、分布の尾を歪める。次章では分布の重心である期待値を扱う。

---

## 第6章　期待値

### この章を学ぶ理由／現場の問題

平均コスト、期待損失、平均負荷は長期判断の基準だが、典型値や保証値ではない。線形性を使うと依存した複雑な件数も簡単に扱える。

### 中心概念と正式な定義

離散型は \(E[X]=\sum_xxp(x)\)、連続型は \(E[X]=\int xf(x)dx\)（絶対可積分等を仮定）。線形性 \(E[aX+bY+c]=aE[X]+bE[Y]+c\) は独立性を要しない。LOTUS: \(E[g(X)]=\sum_xg(x)p(x)\) または積分。

### 直感 → 図解 → 数式 → 例 → 実装

100円損失が0.99、100000円損失が0.01なら期待損失は1099円だが、どちらの実現値でもない。

```text
probability mass --weighted balance point--> E[X]
```

```python
def expected(values, probabilities):
    return sum(x*p for x, p in zip(values, probabilities))
```

指示変数 \(I_i\) で失敗総数 \(N=\sum I_i\)、\(E[N]=\sum P(I_i=1)\)。

### よくある誤解／実務接続

- 期待値は最頻値でも中央値でもない。
- 期待値が有限に存在しない分布もある。
- `E[g(X)] = g(E[X])` は一般に誤り（Jensen）。
- capacity の平均だけでは burst や tail を吸収できない。

### 要点

1. 期待値は確率加重平均。 2. 実現可能値とは限らない。 3. 線形性は依存していても成立。 4. 非線形変換と交換できない。 5. 判断には分散・尾・損失も必要。

### 誤解チェック（5問）

1. 期待値は必ず観測可能か。 2. 線形性に独立性は必要か。 3. 平均 latency で p99 を推定できるか。 4. E[1/X]=1/E[X] か。 5. 期待値は常に有限か。

### 基礎問題（5問）

1. サイコロ期待値を求めよ。 2. Bernoulli の期待値を求めよ。 3. 指示変数で成功件数を求めよ。 4. 料金プランの期待費用を比較せよ。 5. 非線形反例を作れ。

### 応用問題（3問）／設計問題／調査課題

1. キャッシュ miss コストの期待値を作れ。 2. Jensen 不等式の実務例を示せ。 3. 重い尾で sample mean をシミュレートせよ。 **設計:** 期待損失によるリリース基準を設計せよ。 **調査:** クラウド料金見積りの平均仮定を調べよ。

### 知らないとする誤判断／次章への接続

平均負荷だけで必要容量を決め、burst で飽和する。次章では平均からの散らばりを測る。

---

## 第7章　分散

### この章を学ぶ理由／現場の問題

平均が同じ二システムでも安定性は異なる。分散、標準偏差、共分散は散らばりと共同変動を定量化する。

### 中心概念と正式な定義

\(Var(X)=E[(X-\mu)^2]=E[X^2]-\mu^2\)、\(SD(X)=\sqrt{Var(X)}\)。\(Cov(X,Y)=E[(X-E[X])(Y-E[Y])]\)。\(Var(aX+b)=a^2Var(X)\)、\(Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)\)。独立なら共分散0だが逆は一般に成り立たない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
same mean 10:  9,10,11  (small spread)
               0,10,20  (large spread)
```

標本分散 \(s^2=\sum_i(x_i-\bar x)^2/(n-1)\) は iid 標本で母分散の不偏推定量。

```python
def sample_variance(xs):
    m = sum(xs)/len(xs)
    return sum((x-m)**2 for x in xs)/(len(xs)-1)
```

### よくある誤解／実務接続

- 分散は元単位の二乗、標準偏差が元単位。
- 標準偏差は尾確率を分布仮定なしに一意に決めない。
- n と n-1 の選択は対象（記述か推定）で決まる。
- jitter、需要変動、replica 相関を容量設計へ反映する。

### 要点

1. 分散は二乗偏差期待値。 2. SD は元単位。 3. 和の分散に共分散が入る。 4. 独立⇒無相関、逆は一般に偽。 5. 標本分散の分母は目的で選ぶ。

### 誤解チェック（5問）

1. 分散とSDの単位は同じか。 2. 無相関なら独立か。 3. 分散は負か。 4. 独立和のSDは単純加算か。 5. n-1 は常に使うか。

### 基礎問題（5問）

1. 3値の分散を求めよ。 2. 線形変換後の分散を求めよ。 3. 共分散付き和を計算せよ。 4. 二標本の平均・SDを比較せよ。 5. 不偏分散を実装せよ。

### 応用問題（3問）／設計問題／調査課題

1. replica 障害の相関が冗長性へ与える影響を論ぜよ。 2. heavy-tail でSDの不安定性を試せ。 3. online variance を導け。 **設計:** latency の中心・散布・尾を報告せよ。 **調査:** 利用ライブラリの variance `ddof` を確認せよ。

### 知らないとする誤判断／次章への接続

平均と標準偏差だけでどんな分布も正規と見なし、tail risk を落とす。次章では代表的分布をモデルとして選ぶ。

---

## 第8章　確率分布

### この章を学ぶ理由／現場の問題

分布名はデータに貼るラベルではなく、生成過程への仮定である。support とパラメータが現象に合わなければ推論全体が壊れる。

### 中心概念と正式な定義

分布は確率変数が誘導する測度。parameterized family \(\{P_\theta:\theta\in\Theta\}\) からモデルを選ぶ。joint \(p(x,y)\)、marginal \(p_X(x)=\sum_yp(x,y)\)、conditional \(p(x|y)\) を区別する。quantile \(q_p=\inf\{x:F(x)\ge p\}\)。

### 直感 → 図解 → 数式 → 例 → 実装

```text
Bernoulli: one yes/no
Binomial : successes in fixed n
Poisson  : counts in exposure
Normal   : additive central variation
Exponential: waiting time under constant hazard
```

経験 CDF \(\hat F_n(x)=n^{-1}\sum_i1\{X_i\le x\}\) は分布形を仮定せず推定する。

```python
def ecdf(xs, x): return sum(v <= x for v in xs)/len(xs)
```

### よくある誤解／実務接続

- histogram の形だけで分布を断定しない。
- parameter fit が良くても独立性や定常性は保証されない。
- p99 は「99%の平均」ではない。
- SLO、queue、retry 数のモデル選択に生成機構を使う。

### 要点

1. 分布は生成仮定。 2. support を確認。 3. joint/marginal/conditional を区別。 4. quantile は CDF の逆。 5. empirical distribution は仮定の少ない基準。

### 誤解チェック（5問）

1. 同じ平均分散なら同じ分布か。 2. p99 は上位1%の平均か。 3. fit は因果機構を証明するか。 4. 離散 count に正規を必ず使えるか。 5. marginal から joint は一意か。

### 基礎問題（5問）

1. 五現象に候補分布を割り当てよ。 2. CDF から中央値を求めよ。 3. joint から marginal を求めよ。 4. support 違反を探せ。 5. ECDF を実装せよ。

### 応用問題（3問）／設計問題／調査課題

1. zero-inflated count を説明せよ。 2. mixture と単一分布を比較せよ。 3. Q-Q plot の読み方を述べよ。 **設計:** retry count のモデル診断を設計せよ。 **調査:** 実 latency に合う分布の候補と限界を調べよ。

### 知らないとする誤判断／次章への接続

平均と分散を合わせただけで正規モデルを採用する。次章では固定試行数の成功件数を扱う二項分布を学ぶ。

---

## 第9章　二項分布

### この章を学ぶ理由／現場の問題

固定件数の独立試行で成功数を数えるモデルはテスト成功率や conversion の基礎。ただしユーザー内相関や変動する確率は仮定違反になる。

### 中心概念と正式な定義

\(X\sim Binomial(n,p)\) は独立で同一成功確率 p の Bernoulli 試行 n 回の成功数。\(P(X=k)={n\choose k}p^k(1-p)^{n-k}\)、\(E[X]=np\)、\(Var(X)=np(1-p)\)。Bernoulli 指示変数の和として導ける。

### 直感 → 図解 → 数式 → 例 → 実装

```text
n fixed trials: F S F S ... -> count S
```

100 request、p=.02 の失敗が0件である確率は \(.98^{100}\approx.133\)。0件観測は p=0 の証明ではない。

```python
from math import comb
def binom_pmf(k,n,p): return comb(n,k)*p**k*(1-p)**(n-k)
```

### よくある誤解／実務接続

- 固定 n、同じ p、独立という三仮定を確認する。
- 一ユーザーの反復行動を独立 request と数えると有効標本数を過大評価。
- without replacement は超幾何分布が自然。
- proportion \(\hat p=X/n\) の標準誤差は概ね \(\sqrt{p(1-p)/n}\)。

### 要点

1. 二項は Bernoulli 和。 2. n 固定。 3. p 共通。 4. 試行独立。 5. 0 success は p=0 を意味しない。

### 誤解チェック（5問）

1. 時間窓内件数は常に二項か。 2. p が日ごとに違ってよいか。 3. 0失敗は無故障証明か。 4. 同一ユーザー反復は独立か。 5. 分散=npか。

### 基礎問題（5問）

1. PMF を計算せよ。 2. 平均分散を求めよ。 3. 0件確率を求めよ。 4. Bernoulli 和で示せ。 5. 仮定違反を三つ挙げよ。

### 応用問題（3問）／設計問題／調査課題

1. beta-binomial が過分散を扱う理由を述べよ。 2. cluster sampling の影響をシミュレートせよ。 3. rare event の Poisson 近似を試せ。 **設計:** release error rate の標本単位を設計せよ。 **調査:** 自社イベントの重複ユーザー率を確認せよ。

### 知らないとする誤判断／次章への接続

100万 request を100万独立標本と数え、ユーザー/時間クラスタを無視する。次章は一定 exposure 内の稀な件数モデルへ進む。

---

## 第10章　Poisson 分布

### この章を学ぶ理由／現場の問題

一定時間・面積・リクエスト量あたりの稀なイベント件数をモデル化する。ただし burst、自己励起、日周期があれば定率仮定は破れる。

### 中心概念と正式な定義

\(X\sim Poisson(\lambda)\) は \(P(X=k)=e^{-\lambda}\lambda^k/k!\)、\(E[X]=Var(X)=\lambda\)。Poisson process は独立増分と定常増分を持ち、長さ t の区間件数が \(Poisson(\rho t)\)。二項で \(n\to\infty,p\to0,np\to\lambda\) の極限でも得る。

### 直感 → 図解 → 数式 → 例 → 実装

```text
time: | *    *  **       * |  count events in exposure T
```

1時間平均2件なら0件確率 \(e^{-2}\)、5時間件数は定率なら平均10。

```python
import random, math
def poisson_zero(rate, exposure): return math.exp(-rate*exposure)
```

rate の分母 exposure を必ず保存する。

### よくある誤解／実務接続

- 平均=分散は診断点。variance≫mean は過分散。
- 単位時間を変えると \(\lambda\) も変わる。
- Poisson は同時 burst や障害伝播を表しにくい。
- incident、arrival、rare error の基準モデルとして使い、残差で仮定を疑う。

### 要点

1. Poisson は exposure 内件数。 2. λ は期待件数。 3. 平均と分散が等しい。 4. rate と exposure を分ける。 5. 独立・定率仮定を診断する。

### 誤解チェック（5問）

1. λ は必ず1時間単位か。 2. count があれば Poisson か。 3. burst でも独立増分か。 4. 平均と分散が大きく違ってよいか。 5. rate 比較で exposure は不要か。

### 基礎問題（5問）

1. 0件/1件確率を求めよ。 2. exposure を倍にせよ。 3. 二率を比較せよ。 4. 平均分散で適合を診断せよ。 5. 二項近似を計算せよ。

### 応用問題（3問）／設計問題／調査課題

1. negative binomial で過分散を扱え。 2. 非一様 Poisson を説明せよ。 3. incident clustering を可視化せよ。 **設計:** error count dashboard に exposure を組み込め。 **調査:** 週次季節性の有無を実データで確認せよ。

### 知らないとする誤判断／次章への接続

障害 burst を独立 Poisson とみなし、同時多発リスクを過小評価する。次章では加法的変動の近似として正規分布を学ぶ。

---

## 総合演習A（第1〜10章）

1. 二つのリージョンの error count を、分母、条件付き率、基礎率、独立性、過分散の観点でレビューせよ。
2. 「アラート感度99%」から調査優先順位を設計し、事前率を0.01%〜10%で感度分析せよ。
3. request、user、session の三標本単位で conversion 標準誤差がどう変わるかシミュレートせよ。
4. 任意の本番メトリクスについて \(\Omega\)、確率変数、分布候補、support、欠測、意思決定損失を一枚にまとめよ。

---

## 第11章　正規分布

### この章を学ぶ理由／現場の問題

正規分布は加法的な小変動や標本平均の近似に頻出するが、latency、収入、障害件数へ機械的に当てると負値や尾の過小評価を生む。

### 中心概念と正式な定義

\(X\sim N(\mu,\sigma^2)\) の密度は \(f(x)=(\sigma\sqrt{2\pi})^{-1}\exp(-(x-\mu)^2/(2\sigma^2))\)。標準化 \(Z=(X-\mu)/\sigma\sim N(0,1)\)。正規変数の線形結合は共同正規等の条件下で正規。密度は左右対称で平均=中央値=最頻値。

### 直感 → 図解 → 数式 → 例 → 実装

```text
density
  ^          .-''-.
  |       .-' μ    '-.
  +--------------------> x
          μ-σ  μ  μ+σ
```

約68%,95%,99.7%が \(\mu\pm1,2,3\sigma\) 内。これは正規仮定下の近似で普遍則ではない。

```python
z = [(x - mean) / sd for x in observations]
```

### よくある誤解／実務接続

- bell shape に見えるだけで正規とは限らない。
- 3σ rule を heavy-tail に適用しない。
- 個々の観測が非正規でも平均が近似正規になることと混同しない。
- 測定誤差、工程変動、標本平均の推論で仮定を診断して使う。

### 要点

1. 正規は μ,σ² で決まる。 2. 全実数が support。 3. z-score は単位を標準化。 4. 対称・薄い尾を仮定。 5. データ正規性と推定量正規性を分ける。

### 誤解チェック（5問）

1. latency は必ず正規か。 2. ±2σ に必ず95%か。 3. 正規分布は負値を許すか。 4. z=2 は上位2%か。 5. 標本平均が正規なら原データも正規か。

### 基礎問題（5問）

1. z-score を計算せよ。 2. 区間確率を標準化せよ。 3. μ,σ の変化を描け。 4. 負値確率を検査せよ。 5. 正規仮定不適合を例示せよ。

### 応用問題（3問）／設計問題／調査課題

1. log-normal と normal を比較せよ。 2. Q-Q plot を解釈せよ。 3. robust z-score を提案せよ。 **設計:** anomaly threshold を分布仮定付きで設計せよ。 **調査:** 本番 latency の正規性を診断せよ。

### 知らないとする誤判断／次章への接続

平均±3SD 外を即異常とし、heavy-tail の正常変動を大量通知する。次章では平均が確率的に真値へ近づく法則を学ぶ。

---

## 第12章　大数の法則

### この章を学ぶ理由／現場の問題

試行を増やすと平均は安定するが、どんなデータ収集でも真実に近づくわけではない。独立性、同分布性、有限期待値などの条件が本体である。

### 中心概念と正式な定義

iid で \(E|X_i|<\infty\)、\(\bar X_n=n^{-1}\sum_iX_i\) とする。弱大数は任意の \(\epsilon>0\) に対し \(P(|\bar X_n-\mu|>\epsilon)\to0\)。強大数は \(\bar X_n\to\mu\) almost surely。収束は有限 n で一致する保証ではない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
running mean: /\/\_/\__---→ μ
n increases: typical deviation shrinks, bias does not
```

```python
import random
s = 0
for n in range(1, 100001):
    s += random.random()
    if n in {10,100,1000,10000}: print(n, s/n)
```

母集団選択が偏っていれば \(\bar X_n\) は偏った分布の期待値へ精密に収束する。

### よくある誤解／実務接続

- gambler's fallacy のように短期の反動を保証しない。
- 大標本はバイアスを消さない。
- 自己相関が強い時の有効標本数は n より小さい。
- monitoring の長期率、load test の反復平均に適用条件を確認する。

### 要点

1. 標本平均の収束法則。 2. 有限標本保証ではない。 3. 代表的条件は iid と有限期待値。 4. variance でなく bias は残る。 5. 依存は有効標本数を下げる。

### 誤解チェック（5問）

1. 連敗後は勝ちやすいか。 2. n増加で選択バイアスは消えるか。 3. 強大数は毎列で収束か。 4. heavy-tail でも常に同条件か。 5. ログ重複は情報量を増やすか。

### 基礎問題（5問）

1. coin の running mean を模擬せよ。 2. 弱収束を言葉で述べよ。 3. biased sampler を作れ。 4. 自己相関系列を比較せよ。 5. 条件を列挙せよ。

### 応用問題（3問）／設計問題／調査課題

1. Cauchy 標本平均を模擬せよ。 2. cluster データの収束を論ぜよ。 3. ergodicity との関係を調べよ。 **設計:** benchmark の独立反復単位を設計せよ。 **調査:** 日次メトリクスの自己相関を測れ。

### 知らないとする誤判断／次章への接続

大量の偏った telemetry を「ビッグデータだから正しい」と断定する。次章では平均の誤差分布を与える中心極限定理へ進む。

---

## 第13章　中心極限定理

### この章を学ぶ理由／現場の問題

信頼区間や検定で正規近似が現れる理由を理解し、原データが正規だからではなく、標本平均の標準化極限だと区別する。

### 中心概念と正式な定義

iid、平均 \(\mu\)、有限で正の分散 \(\sigma^2\) のとき \(\sqrt n(\bar X_n-\mu)/\sigma\xrightarrow{d}N(0,1)\)。したがって大きな n で \(\bar X_n\approx N(\mu,\sigma^2/n)\)。Lindeberg 等の条件で非同分布へ一般化できるが、強い依存・無限分散では失敗し得る。

### 直感 → 図解 → 数式 → 例 → 実装

```text
skewed X samples -> averages of m items -> increasingly bell-shaped
```

```python
import random
means = [sum(random.expovariate(1) for _ in range(30))/30
         for _ in range(10000)]
```

標準誤差 \(SE(\bar X)=\sigma/\sqrt n\)。誤差を半分にするには概ね4倍の独立標本が要る。

### よくある誤解／実務接続

- CLT は原データを正規にしない。
- n=30 の万能ルールはない。歪度・尾・依存で収束速度が違う。
- 標本数と有効標本数を混同しない。
- ratio、percentile、最大値には単純な平均 CLT をそのまま使わない。

### 要点

1. CLT は標準化した平均の分布収束。 2. SEは1/√n。 3. 原分布の正規性とは別。 4. 有限分散等の条件がある。 5. 依存・heavy-tail は要注意。

### 誤解チェック（5問）

1. n=30なら必ず正規近似か。 2. 原データは正規になるか。 3. nを2倍でSE半分か。 4. p99 に平均CLTを直接使えるか。 5. 重複観測はnを増やすか。

### 基礎問題（5問）

1. SEを計算せよ。 2. nを4倍にせよ。 3. 指数分布平均を模擬せよ。 4. 標準化式を書け。 5. 条件違反を列挙せよ。

### 応用問題（3問）／設計問題／調査課題

1. Berry--Esseen の意味を調べよ。 2. block bootstrap と依存を論ぜよ。 3. 無限分散例を模擬せよ。 **設計:** mean latency CI の適用判断を設計せよ。 **調査:** 本番データの effective sample size を推定せよ。

### 知らないとする誤判断／次章への接続

観測行数だけを n とし、ユーザー内相関を無視して極端に狭い区間を出す。次章では標本をどう得るかを扱う。

---

## 第14章　標本抽出

### この章を学ぶ理由／現場の問題

推論の質は式より sampling design に支配される。生存者だけ、計測成功だけ、任意期間だけを集めたデータは母集団を代表しない。

### 中心概念と正式な定義

単純無作為抽出は母集団要素の各 n 部分集合が等確率。層化抽出は層内抽出し重みで合成、cluster sampling は群を抽出。包含確率 \(\pi_i=P(i\in s)\) が不均等なら逆確率重み \(1/\pi_i\) を考える。sampling frame、coverage error、nonresponse、selection bias を区別する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
target population -> frame -> selected sample -> observed sample
                  coverage     selection       nonresponse
```

```python
import random
sample = random.sample(population, n)  # frameが正しい場合だけSRS
```

production log は多くの場合確率標本でなく、欠測機構も運用状態に依存する。

### よくある誤解／実務接続

- `random()` を使っただけで母集団から無作為抽出とは限らない。
- 大きな convenience sample は偏りを精密化する。
- 日を跨ぐデータは独立とは限らない。
- telemetry sampling rate と重みを記録する。

### 要点

1. target/frame/observed を分ける。 2. 無作為化は既知の抽出確率を作る。 3. 層化は精度と代表性を改善し得る。 4. cluster は相関を生む。 5. 欠測理由を保存する。

### 誤解チェック（5問）

1. 先着1000件は無作為か。 2. nが大きければ coverage error は消えるか。 3. cluster 内は独立か。 4. sampling rate 不明でも補正できるか。 5. 本番ログは母集団そのものか。

### 基礎問題（5問）

1. target population を定義せよ。 2. frame gap を列挙せよ。 3. 層化案を作れ。 4. 重み付き平均を計算せよ。 5. 欠測理由を分類せよ。

### 応用問題（3問）／設計問題／調査課題

1. reservoir sampling を説明せよ。 2. informative missingness を例示せよ。 3. design effect を計算せよ。 **設計:** 多地域 telemetry sampling を設計せよ。 **調査:** 現行ログのdrop条件を確認せよ。

### 知らないとする誤判断／次章への接続

OOM で消えたログを「障害なし」と数え、可用性を過大評価する。次章では標本から母数を推定する。

---

## 第15章　推定

### この章を学ぶ理由／現場の問題

単一の推定値だけでなく、estimand、推定量、bias、variance を分けると、モデル選択とデータ量のトレードオフを議論できる。

### 中心概念と正式な定義

推定量 \(\hat\theta=T(X_1,\dots,X_n)\) は確率変数、推定値は観測後の数。不偏性 \(E[\hat\theta]=\theta\)、一致性 \(\hat\theta\xrightarrow p\theta\)。MSE \(E[(\hat\theta-\theta)^2]=Var(\hat\theta)+Bias(\hat\theta)^2\)。尤度 \(L(\theta;x)=p_\theta(x)\)、MLE はこれを最大化する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
many samples -> distribution of estimator
                 center=bias, spread=variance
```

Bernoulli の MLE は \(\hat p=\sum x_i/n\)。少し bias を許す shrinkage が MSE を下げる場合もある。

```python
def bernoulli_mle(xs): return sum(xs)/len(xs)
```

### よくある誤解／実務接続

- 不偏だから最良とは限らない。
- 一致性は小標本精度を保証しない。
- MLE はパラメータ化・モデル仮定に依存。
- model drift 下で全履歴を使うと variance は減っても bias が増える。

### 要点

1. estimandを先に定義。 2. estimatorとestimateを分ける。 3. bias-variance-MSEで評価。 4. MLEは尤度最大化。 5. 定常性破れも推定誤差。

### 誤解チェック（5問）

1. 推定値は確率変数か。 2. 不偏=最小MSEか。 3. 一致=有限nで正確か。 4. 尤度はθ上で確率分布か。 5. 古いデータは常に有益か。

### 基礎問題（5問）

1. Bernoulli MLEを導け。 2. biasを計算せよ。 3. MSE分解を示せ。 4. median estimatorを説明せよ。 5. estimand mismatchを例示せよ。

### 応用問題（3問）／設計問題／調査課題

1. shrinkage の利点をシミュレートせよ。 2. robust estimator を比較せよ。 3. censored data のMLEを考えよ。 **設計:** deploy後error rate推定窓を設計せよ。 **調査:** 利用ダッシュボードの集計量定義を確認せよ。

### 知らないとする誤判断／次章への接続

点推定の小数点以下を確実性と誤認する。次章では反復標本での被覆を保証する信頼区間を学ぶ。

---

## 第16章　信頼区間

### この章を学ぶ理由／現場の問題

推定の精度を範囲で示す。ただし頻度論的95%区間は、得られた区間に真値が95%確率で入るという直接の事後確率ではない。

### 中心概念と正式な定義

区間手続き \(C(X)\) が \(P_\theta(\theta\in C(X))\ge1-\alpha\) を全θで満たすとき \((1-\alpha)\) 信頼区間。正規近似平均は \(\bar x\pm z_{1-\alpha/2}s/\sqrt n\)（条件に注意）。未知分散・正規標本なら t 区間を使う。bootstrap は再標本化で推定量分布を近似するが、抽出設計を救済しない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
repeat study:  ----|θ|---  --|θ|--  -----  --|θ|---
                   most generated intervals cover θ
```

```python
def approx_ci(mean, sd, n, z=1.96):
    half = z*sd/(n**0.5)
    return mean-half, mean+half
```

### よくある誤解／実務接続

- 観測後、固定θと固定区間について頻度論的確率は0/1。
- 95%の観測値が区間内という意味ではない。
- optional stopping、選択後区間、cluster 無視で被覆が崩れる。
- effect の実務閾値と区間を比較する。

### 要点

1. 信頼度は手続きの長期被覆。 2. 標準誤差が幅を決める。 3. 仮定違反で被覆は崩れる。 4. 狭さと正しさは別。 5. 実務閾値との関係を読む。

### 誤解チェック（5問）

1. 真値が95%確率で区間内か。 2. 観測の95%が入るか。 3. n増加で幅は概ねどうなるか。 4. 偏りがあっても狭ければ良いか。 5. bootstrapで選択biasは消えるか。

### 基礎問題（5問）

1. 95%区間を計算せよ。 2. nを4倍にせよ。 3. tとzを区別せよ。 4. 被覆simulationを書け。 5. 実務閾値と比較せよ。

### 応用問題（3問）／設計問題／調査課題

1. proportion CIのWald法の問題を調べよ。 2. cluster-robust SEを説明せよ。 3. bootstrap percentile法を検証せよ。 **設計:** SLO error-rate interval表示を設計せよ。 **調査:** 社内レポートの区間算出法を確認せよ。

### 知らないとする誤判断／次章への接続

区間が0を含むことを「効果がない証明」と読む。次章では仮説とデータの不整合を判定する検定を扱う。

---

## 第17章　仮説検定

### この章を学ぶ理由／現場の問題

観測差が帰無仮説下でどれほど意外かを定量化する。検定は「差が存在する確率」や意思決定全体を単独で与えない。

### 中心概念と正式な定義

帰無仮説 \(H_0\)、対立 \(H_1\)、検定統計量 T、棄却域 R を定める。size は \(\sup_{\theta\in H_0}P_\theta(T\in R)\le\alpha\)。第一種誤りは真のH0を棄却、第二種誤りは偽のH0を棄却しない。power \(1-\beta(\theta)=P_\theta(reject)\)。設計、方向、αはデータを見る前に決める。

### 直感 → 図解 → 数式 → 例 → 実装

```text
truth H0  --reject--> type I error
truth H1  --retain--> type II error
```

```python
def z_test(mean, null, se):
    z = (mean-null)/se
    return z
```

棄却しないことは H0 の受容・同等性証明ではない。同等性には equivalence margin と TOST 等を設計する。

### よくある誤解／実務接続

- αは今回の誤判定確率そのものではない。
- power不足の非有意は情報が少ない。
- データ後の片側化、指標選択はsizeを壊す。
- release gate では効果、損失、guardrailと組み合わせる。

### 要点

1. H0下の反証手続き。 2. αは長期type I制御。 3. powerは具体的対立で定まる。 4. 非棄却≠H0証明。 5. 分析計画を事前固定する。

### 誤解チェック（5問）

1. 非有意は同じ証明か。 2. α=.05ならH0が真の確率5%か。 3. powerは常に80%か。 4. データ後に仮説を変えてよいか。 5. 大nで微小差も有意か。

### 基礎問題（5問）

1. H0/H1を書け。 2. 二誤りを表にせよ。 3. z統計量を計算せよ。 4. 片側/両側を選べ。 5. powerへ影響する量を挙げよ。

### 応用問題（3問）／設計問題／調査課題

1. equivalence testを設計せよ。 2. sequential peekingのα増加を模擬せよ。 3. randomization testを実装せよ。 **設計:** 非劣性リリース基準を設計せよ。 **調査:** チームの検定前分析計画を監査せよ。

### 知らないとする誤判断／次章への接続

非有意を「旧版と完全に同じ」と読み、低powerの退行を出荷する。次章では最も誤読される p 値を分離する。

---

## 第18章　p 値

### この章を学ぶ理由／現場の問題

p値は自動意思決定スコアとして乱用される。定義を条件付き確率として正確に読み、効果量・区間・事前計画と併用する。

### 中心概念と正式な定義

観測統計量 \(t_{obs}\) に対し、p値は **H0 とモデル仮定の下で** 少なくとも同程度に極端な統計量を得る確率。片側なら \(p=P_{H_0}(T\ge t_{obs})\)、両側の「極端」の定義は検定による。p値は \(P(H_0|data)\) でも、再現確率でも、効果の大きさでもない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
H0 reference distribution: ----| observed t ---- tail area = p
```

100万標本なら0.01%差でも小pになり得る。逆に小標本の重要差は大pになり得る。

```python
# permutation under H0
p = (1 + sum(abs(t) >= abs(t_obs) for t in permuted_stats)) / (B + 1)
```

### よくある誤解／実務接続

- p=.03 はH0が3%の確率で正しい意味ではない。
- 1-p は対立仮説の確率ではない。
- p=.049 と .051 に科学的断崖はない。
- optional stopping、指標漁り、外れ値除外後の再計算を開示する。

### 要点

1. H0下のtail probability。 2. 仮説の事後確率でない。 3. 効果量でない。 4. sample sizeに依存。 5. 分析選択全体で校正される。

### 誤解チェック（5問）

1. p=.01ならH0が1%か。 2. p=.2なら差なし証明か。 3. 小pなら大効果か。 4. pは再現確率か。 5. .049と.051は質的に別か。

### 基礎問題（5問）

1. p値定義を書け。 2. 片側/両側を比較せよ。 3. nとpの関係を模擬せよ。 4. 誤読を五つ修正せよ。 5. permutation p値を計算せよ。

### 応用問題（3問）／設計問題／調査課題

1. p-curve乱用を説明せよ。 2. optional stoppingを模擬せよ。 3. model misspecificationの影響を論ぜよ。 **設計:** 実験レポートをeffect/CI/power中心に設計せよ。 **調査:** ASA p-value statementを一次資料で読め。

### 知らないとする誤判断／次章への接続

p<.05だけを理由に、ユーザーが気づけない微小差へ数か月投資する。次章では差の規模を測る。

---

## 第19章　効果量

### この章を学ぶ理由／現場の問題

統計的有意性と実務的有意性を分ける。絶対差、相対差、標準化差は異なる問いに答えるため、基準率と費用を併記する。

### 中心概念と正式な定義

平均差 \(\Delta=\mu_1-\mu_0\)、比率差 \(p_1-p_0\)、risk ratio \(p_1/p_0\)、odds ratio \([p_1/(1-p_1)]/[p_0/(1-p_0)]\)。標準化平均差 Cohen's \(d=(\bar x_1-\bar x_0)/s_{pooled}\)。NNT は条件により \(1/|p_1-p_0|\)。estimand と unit を必ず示す。

### 直感 → 図解 → 数式 → 例 → 実装

conversion 1%→1.1% は絶対 +0.1pt、相対 +10%。どちらも正しいが意思決定への印象が違う。

```text
baseline 1.0% | treatment 1.1%
absolute +0.1 percentage point; relative +10%
```

```python
absolute = p1-p0
relative = p1/p0-1
```

### よくある誤解／実務接続

- percent と percentage point を混同しない。
- Cohen の慣例閾値を領域価値の代わりにしない。
- ratio はbaselineが小さいと誇張されやすい。
- 最小実務重要差（MDE/SESOI）を実験前に決める。

### 要点

1. 効果量は差の規模。 2. 絶対・相対を併記。 3. unit/estimandを明示。 4. 区間と共に報告。 5. 実務閾値は領域から決める。

### 誤解チェック（5問）

1. +10%は+10ptか。 2. 小pなら大dか。 3. OR=RRか。 4. 標準化すれば費用判断できるか。 5. baselineなしで相対差を読めるか。

### 基礎問題（5問）

1. 絶対/相対差を計算せよ。 2. RR/ORを比較せよ。 3. dを計算せよ。 4. NNTを求めよ。 5. 実務閾値を定義せよ。

### 応用問題（3問）／設計問題／調査課題

1. skewed latencyの効果量を提案せよ。 2. heterogeneous effectを層別せよ。 3. cost-benefitへ変換せよ。 **設計:** A/B結果カードを設計せよ。 **調査:** 過去レポートの相対差誇張を監査せよ。

### 知らないとする誤判断／次章への接続

相対50%改善だけを示し、0.002%→0.003%の絶対差と費用を隠す。次章では共変動と原因を分ける。

---

## 第20章　相関と因果

### この章を学ぶ理由／現場の問題

deploy と障害、機能利用と継続率が共変動しても、交絡・逆因果・選択があり得る。介入判断には因果 estimand が要る。

### 中心概念と正式な定義

Pearson相関 \(\rho=Cov(X,Y)/(\sigma_X\sigma_Y)\) は線形関連、Spearman は順位単調関連。潜在結果で個体効果は \(Y_i(1)-Y_i(0)\)、平均処置効果 ATE=\(E[Y(1)-Y(0)]\)。同一個体の二潜在結果は同時観測できない（因果推論の基本問題）。DAG で共通原因、mediator、collider を表し、識別仮定を明示する。

### 直感 → 図解 → 数式 → 例 → 実装

```text
complexity -> uses_tool
complexity -> failure       (confounding)
uses_tool  ?-> failure
```

```python
# correlation describes; random assignment can identify under assumptions
r = covariance(x,y)/(std(x)*std(y))
```

ランダム割付は処置と潜在結果の独立を設計で近似し、平均差を因果差へ結びつける。

### よくある誤解／実務接続

- 相関0でも非線形依存はあり得る。
- 高相関でも共通時系列トレンドだけかもしれない。
- 予測精度は介入効果を保証しない。
- collider で条件付けると偽相関を作る。

### 要点

1. 相関は関連の尺度。 2. 因果は介入反実仮想。 3. 交絡を識別する。 4. ランダム化が強い設計。 5. DAG と仮定を先に書く。

### 誤解チェック（5問）

1. r=0なら独立か。 2. 高rならXを変えればYが変わるか。 3. 予測モデルは因果モデルか。 4. 時系列trendは相関を作るか。 5. 全変数で調整すればよいか。

### 基礎問題（5問）

1. Pearson rを計算せよ。 2. 非線形無相関例を作れ。 3. DAGを描け。 4. confounder/colliderを分けよ。 5. ATEを定義せよ。

### 応用問題（3問）／設計問題／調査課題

1. deployとincidentの因果設計を作れ。 2. difference-in-differences仮定を述べよ。 3. mediationを区別せよ。 **設計:** feature adoption効果の識別戦略を設計せよ。 **調査:** 過去の相関主張をDAGで再評価せよ。

### 知らないとする誤判断／次章への接続

上級ユーザーほど使う機能を「継続率を上げる原因」とし全員へ強制する。次章では条件付き平均をモデル化する回帰へ進む。

---

## 総合演習B（第11〜20章）

1. 平均 latency が5ms改善し p=.001 の実験を、分布、tail、標本単位、CI、効果量、実務閾値からレビューせよ。
2. 観測データで「監視ツール導入企業は障害が多い」理由をDAGで三通り示し、識別に必要なデータまたは実験を提案せよ。
3. biased sampling でも極めて狭い95%区間が得られる simulation を作り、被覆と精度を区別せよ。
4. sequential dashboard で毎時間 p 値を確認する運用のtype I errorを模擬し、停止規則を再設計せよ。

---

## 第21章　回帰

### この章を学ぶ理由／現場の問題

複数要因と結果の条件付き関係を数量化する。ただし回帰係数はモデル、変数尺度、調整集合に条件づけられ、因果効果とは限らない。

### 中心概念と正式な定義

線形回帰は \(E[Y|X=x]=\beta_0+x^T\beta\)、観測モデル \(Y=X\beta+\varepsilon\)。OLS は \(\hat\beta=\arg\min_b\|y-Xb\|^2\)。full rank なら \((X^TX)^{-1}X^Ty\)。推論には誤差の独立性・平均0・分散構造等を区別して仮定する。ロジスティック回帰は \(logit P(Y=1|x)=\beta_0+x^T\beta\)。

### 直感 → 図解 → 数式 → 例 → 実装

```text
Y
|  * *     residual = observed - fitted
| *---*---- fitted conditional mean
+------------ X
```

```python
import numpy as np
beta = np.linalg.lstsq(X, y, rcond=None)[0]
residual = y - X @ beta
```

残差図で非線形、heteroskedasticity、時系列依存、影響点を診断する。

### よくある誤解／実務接続

- 高 \(R^2\) は因果・外部妥当性・正しさを保証しない。
- 係数は他の投入変数を固定した条件付き関連。
- extrapolation は観測範囲外で危険。
- 多重共線性は予測可能でも係数解釈を不安定にする。

### 要点

1. 回帰は条件付き平均モデル。 2. OLSは二乗誤差最小化。 3. 係数解釈は尺度と調整変数依存。 4. 残差診断が必要。 5. 予測と因果を分ける。

### 誤解チェック（5問）

1. 係数は常に因果効果か。 2. 高R²なら将来も正確か。 3. 線形は特徴量に線形という意味か。 4. 外挿は内挿と同じか。 5. 残差の平均0だけで十分か。

### 基礎問題（5問）

1. 単回帰係数を計算せよ。 2. dummy変数を解釈せよ。 3. 交互作用項を書け。 4. 残差図を読め。 5. logit係数をoddsへ変換せよ。

### 応用問題（3問）／設計問題／調査課題

1. robust SEを比較せよ。 2. regularizationのbias-varianceを論ぜよ。 3. 時系列cross-validationを設計せよ。 **設計:** capacity予測回帰のfeatureと検証を設計せよ。 **調査:** production modelの外挿範囲を監査せよ。

### 知らないとする誤判断／次章への接続

係数が有意なメトリクスを「原因」として最適化し、Goodhart化する。次章で介入をランダム化するA/Bテストを扱う。

---

## 第22章　A/B テスト

### この章を学ぶ理由／現場の問題

機能の因果効果を識別する強い方法だが、割付単位、干渉、sample ratio mismatch、計測欠落、停止規則で容易に壊れる。

### 中心概念と正式な定義

unit i を \(Z_i\in\{0,1\}\) に無作為割付し、潜在結果 \(Y_i(1),Y_i(0)\) を考える。SUTVA（処置の一貫性とunit間干渉なし）等の下で平均差はATEを不偏推定する。ITT は割付に基づく効果。MDE、α、power、variance、割付比から事前標本数を決める。

### 直感 → 図解 → 数式 → 例 → 実装

```text
eligible units --randomize--> A -> outcome
                            \-> B -> outcome
check SRM, exposure, missingness before effect
```

```python
def deterministic_arm(user_id):
    return hash_to_unit_interval(user_id) < 0.5
```

割付後のexposureだけで絞るとpost-treatment biasを生み得る。

### よくある誤解／実務接続

- request単位割付でuser体験が混ざる。
- 「有意になるまで待つ」は通常の固定標本検定を無効化。
- primary metricだけでなくguardrailと品質診断を事前定義。
- novelty、network effect、carryoverで短期ATEと長期効果が違う。

### 要点

1. 無作為化が交絡を平均化。 2. unitとestimandを揃える。 3. ITTを基本にする。 4. SRM/欠測を先に診断。 5. 停止規則・指標を事前登録。

### 誤解チェック（5問）

1. A/Bなら必ず因果か。 2. exposure済みだけで比較してよいか。 3. 毎日p値を見て止めてよいか。 4. user間干渉は無関係か。 5. 非有意なら同等か。

### 基礎問題（5問）

1. unitを選べ。 2. ATE/ITTを定義せよ。 3. SRMを検査せよ。 4. MDEを設定せよ。 5. guardrailを三つ挙げよ。

### 応用問題（3問）／設計問題／調査課題

1. cluster randomizationを設計せよ。 2. CUPEDの直感を説明せよ。 3. sequential testを固定標本と比較せよ。 **設計:** search ranking実験計画を事前登録せよ。 **調査:** 既存flagの割付安定性を確認せよ。

### 知らないとする誤判断／次章への接続

20指標のどれか一つが有意なら勝ちと宣言する。次章では多数の機会による偽陽性を制御する。

---

## 第23章　多重検定

### この章を学ぶ理由／現場の問題

指標、セグメント、期間、variantを増やすほど偶然の小pが見つかる。選択を含めた「検定族」を定義しなければαは意味を失う。

### 中心概念と正式な定義

m個の真のH0を各αで検定すると、独立なら少なくとも一偽陽性の確率は \(1-(1-\alpha)^m\)。FWERは一つ以上のtype I error、FDRは棄却中のfalse discovery割合の期待。Bonferroniは各 \(\alpha/m\) でFWER≤α。Benjamini--Hochbergは順序p値 \(p_{(k)}\le kq/m\) まで棄却し条件下でFDRを制御。

### 直感 → 図解 → 数式 → 例 → 実装

20独立検定を各5%なら少なくとも一偽陽性は約64%。

```text
many shots at noise -> at least one impressive result
```

```python
def bonferroni(pvalues, alpha=.05):
    return [p <= alpha/len(pvalues) for p in pvalues]
```

### よくある誤解／実務接続

- correction不要な「primary一つ」と探索的分析を事前分離する。
- FDR 5%は各発見が95%真という意味ではない。
- 相関検定で方法の仮定が変わる。
- dashboard上で任意segmentを掘る行為も多重性を生む。

### 要点

1. multiplicityは分析機会全体から生じる。 2. FWERとFDRは別目標。 3. Bonferroniは単純で保守的。 4. BHは発見集合を制御。 5. confirmatory/exploratoryを分ける。

### 誤解チェック（5問）

1. 20検定のどれかがp<.05なら全体5%か。 2. FDR=各仮説の誤り確率か。 3. segment探索は多重性か。 4. Bonferroniは依存下で無効か。 5. 事前primary一つも補正必須か。

### 基礎問題（5問）

1. FWERを計算せよ。 2. Bonferroni閾値を出せ。 3. BH手順を適用せよ。 4. 検定族を定義せよ。 5. 探索ラベルを付けよ。

### 応用問題（3問）／設計問題／調査課題

1. hierarchical testingを提案せよ。 2. dependent p-values下のFDRを調べよ。 3. selective inferenceを説明せよ。 **設計:** 50metric実験のgateを設計せよ。 **調査:** 過去実験の未報告segment数を監査せよ。

### 知らないとする誤判断／次章への接続

探索で偶然勝ったsegmentを再現確認せず全展開する。次章では事前と尤度から不確実性を直接更新するBayesian thinkingを学ぶ。

---

## 第24章　Bayesian thinking

### この章を学ぶ理由／現場の問題

未知パラメータについて確率を述べ、過去知識を更新し、意思決定損失へ接続する一貫した枠組みを得る。ただしpriorとモデル診断を隠してはならない。

### 中心概念と正式な定義

事前 \(p(\theta)\)、尤度 \(p(y|\theta)\)、事後 \(p(\theta|y)=p(y|\theta)p(\theta)/p(y)\)。posterior predictive は \(p(\tilde y|y)=\int p(\tilde y|\theta)p(\theta|y)d\theta\)。Beta(a,b)-Bernoulli では成功s、失敗f後 \(Beta(a+s,b+f)\)。credible interval は事後確率質量を含む区間。

### 直感 → 図解 → 数式 → 例 → 実装

```text
prior × likelihood -> posterior -> predictive/decision
```

```python
def beta_update(a, b, successes, failures):
    return a + successes, b + failures
```

posterior predictive checkでモデルから再現データを生成し、観測の尾・zero・clusterを再現できるか診断する。

### よくある誤解／実務接続

- Bayesianは主観なら何でもよいという意味ではない。
- noninformative priorもparameterization依存。
- credible 95%とfrequentist CI 95%は意味が違う。
- optional stoppingへの扱いもsampling/decision設計を無視してよいわけではない。

### 要点

1. 未知量へ分布を置く。 2. Bayes則で更新。 3. predictiveで将来を扱う。 4. prior感度を示す。 5. 意思決定はposteriorとlossを結ぶ。

### 誤解チェック（5問）

1. priorは自由に結論を作ってよいか。 2. credible=confidenceか。 3. posteriorだけでモデル適合は保証されるか。 4. flat priorは常に中立か。 5. Bayesianなら多重性は無関係か。

### 基礎問題（5問）

1. Beta posteriorを計算せよ。 2. posterior meanを求めよ。 3. predictiveを説明せよ。 4. prior感度を比較せよ。 5. credible intervalを解釈せよ。

### 応用問題（3問）／設計問題／調査課題

1. hierarchical partial poolingを説明せよ。 2. posterior predictive checkを書け。 3. ROPEによる同等性を論ぜよ。 **設計:** 低頻度incident rateのBayesian監視を設計せよ。 **調査:** 使用ライブラリのMCMC診断を一次資料で確認せよ。

### 知らないとする誤判断／次章への接続

データが少ないのにpriorを省略した体裁で極端なrateをランキングする。次章ではSREメトリクスへ統計を接続する。

---

## 第25章　SRE への応用：latency・percentile・SLA・error rate

### この章を学ぶ理由／現場の問題

平均可用性や平均latencyはユーザー体験の尾と時間局所性を隠す。SLOは統計量だけでなく、対象イベントと意思決定窓の仕様である。

### 中心概念と正式な定義

SLI は測定量、SLO は目標、SLA は通常契約上の結果を伴う約束。可用性SLIを good events / valid events とする。error budget は許容bad割合×窓内events。p99は経験CDFの0.99 quantile。分散システムの経路max・retry・queueingでtailが増幅する。複数時系列観測はiidでない。

### 直感 → 図解 → 数式 → 例 → 実装

```text
request path: service A -> fanout max(B1...Bk) -> C
one slow branch can dominate tail
```

```python
def sli(events):
    valid = [e for e in events if e.in_scope]
    return sum(e.good for e in valid)/len(valid)
```

分位点を平均して全体p99にはできない。集約には分布情報または mergeable sketch が必要。

### よくある誤解／実務接続

- p99の平均は全体p99でない。
- SLA/SLO/SLIを同義にしない。
- client retry は見かけの成功率と負荷を同時に変える。
- burn rate alertは複数窓で速度と持続を捉える。

### 要点

1. SLIの分子分母を仕様化。 2. percentileはtail位置。 3. quantileは単純平均不能。 4. error budgetはリスク配分。 5. 時系列依存・欠測を扱う。

### 誤解チェック（5問）

1. p99日次平均=月次p99か。 2. SLA=SLOか。 3. server成功=ユーザー成功か。 4. retryを独立試行とみなせるか。 5. 99.9%なら全時間均等か。

### 基礎問題（5問）

1. SLIを定義せよ。 2. budgetを計算せよ。 3. p99をデータから求めよ。 4. retry込みgood eventを決めよ。 5. burn rateを計算せよ。

### 応用問題（3問）／設計問題／調査課題

1. quantile sketch誤差を論ぜよ。 2. coordinated omissionを説明せよ。 3. fanout tailを模擬せよ。 **設計:** user-journey SLOを設計せよ。 **調査:** 現行SLIのexcluded eventsを監査せよ。

### 知らないとする誤判断／次章への接続

各hostのp99を平均して全体SLO達成を宣言する。次章では測定環境自体が結果へ影響するbenchmarkを設計する。

---

## 第26章　Performance Benchmark

### この章を学ぶ理由／現場の問題

benchmark差はコードだけでなくwarmup、CPU周波数、GC、I/O cache、負荷生成器、実行順に左右される。再現可能な比較実験として設計する。

### 中心概念と正式な定義

測定モデルを \(Y=\mu+\tau_{implementation}+\beta_{environment}+\varepsilon\) と考える。繰返しは同一process内iterationと独立runを区別。paired designは同条件block内差 \(D_i=Y_{Bi}-Y_{Ai}\) を解析し環境分散を減らす。throughput/latencyは負荷、concurrency、open/closed loopの関数。

### 直感 → 図解 → 数式 → 例 → 実装

```text
randomized blocks:
machine/day 1: A B B A
machine/day 2: B A A B -> analyze paired differences
```

```python
import random
order = ["A", "B"] * 20
random.shuffle(order)
results = [run_isolated(v) for v in order]
```

warmupは都合の悪い値の恣意的削除でなく、事前規則または定常性診断で扱う。

### よくある誤解／実務接続

- iteration数を独立標本数と数えない。
- microbenchmark改善はsystem throughput改善を保証しない。
- 最大性能と指定負荷での性能は別estimand。
- coordinated omission、dead-code elimination、timer resolutionを検査する。

### 要点

1. benchmarkは実験。 2. estimandとworkloadを固定。 3. 独立runを識別。 4. randomize/block/pairで環境差を制御。 5. 生データと環境を保存。

### 誤解チェック（5問）

1. 1process内100万回はn=100万か。 2. 平均だけで比較できるか。 3. warmupは必ず先頭10回か。 4. micro=macroか。 5. benchmark machineだけで外部妥当か。

### 基礎問題（5問）

1. estimandを書け。 2. noise源を列挙せよ。 3. randomized orderを作れ。 4. paired差を計算せよ。 5. CIを報告せよ。

### 応用問題（3問）／設計問題／調査課題

1. autocorrelationを診断せよ。 2. open/closed loadを比較せよ。 3. benchmark harness overheadを推定せよ。 **設計:** DB driver比較実験を設計せよ。 **調査:** 利用benchmark toolのwarmup/GC制御を確認せよ。

### 知らないとする誤判断／次章への接続

同じprocessの反復を独立標本とし、0.1%差へ極端に狭いCIを付ける。次章では統計推論と機械学習の境界を整理する。

---

## 第27章　Machine Learning への入口

### この章を学ぶ理由／現場の問題

MLは観測データから未知例へ一般化する統計的問題である。学習誤差、検証誤差、データ漏洩、分布変化を区別しないとproductionで崩れる。

### 中心概念と正式な定義

仮説 \(f\in\mathcal F\)、損失 \(\ell(f(X),Y)\)、risk \(R(f)=E_{(X,Y)\sim P}[\ell]\)。empirical risk \(\hat R_n=n^{-1}\sum_i\ell(f(x_i),y_i)\) を最小化する。generalization gapは \(R-\hat R\)。supervised/unsupervised、regression/classificationを問いで分ける。train/validation/test は選択に使う情報境界。

### 直感 → 図解 → 数式 → 例 → 実装

```text
historical population -> train -> choose on validation -> one final test
future population may drift
```

```python
train, valid, test = time_aware_split(data)
model.fit(train.X, train.y)
model = choose(models, key=lambda m: m.loss(valid))
report(model.loss(test))
```

### よくある誤解／実務接続

- test setを何度も見ればvalidation化する。
- 高accuracyは基礎率不均衡で無意味になり得る。
- calibrationとrankingを分ける。
- feature leakage、label delay、feedback loop、driftをproduction契約へ含める。

### 要点

1. 目的は未知分布へのrisk。 2. empirical riskは近似。 3. 情報境界でsplit。 4. metricは損失と基礎率に合わせる。 5. driftと監視を含めて設計。

### 誤解チェック（5問）

1. train accuracyでgeneralizationを測れるか。 2. testを毎週見てよいか。 3. 99%accuracyは常に良いか。 4. correlation featureは介入可能か。 5. static datasetでproduction driftを除けるか。

### 基礎問題（5問）

1. riskを定義せよ。 2. splitの役割を書け。 3. confusion matrixを作れ。 4. precision/recallを計算せよ。 5. leakageを例示せよ。

### 応用問題（3問）／設計問題／調査課題

1. time splitをrandom splitと比較せよ。 2. calibration curveを作れ。 3. fairness metricの母集団依存を論ぜよ。 **設計:** incident classifierのoffline/online評価を設計せよ。 **調査:** production featureのavailability時刻を監査せよ。

### 知らないとする誤判断／次章への接続

test setをモデル選択に使い続け、最終スコアを未知データ性能と報告する。次章では複数の誤りが重なるケースを診断する。

---

## 第28章　統計的誤判断のケーススタディ

### この章を学ぶ理由／現場の問題

実際の失敗は一つの公式誤りでなく、選択、停止、欠測、指標、因果解釈が連鎖する。再現可能な事故分析として切り分ける。

### 中心概念と正式な定義

ケース：新cacheは平均latencyを8%改善し p=.02 と報告された。しかし (1)成功requestのみ、(2)20 endpointから最良を選択、(3)毎時peeking、(4)host内反復を独立n、(5)p99悪化を未報告。estimand mismatch、selection bias、multiplicity、optional stopping、pseudoreplication、metric trade-off が同時にある。

### 直感 → 図解 → 数式 → 例 → 実装

```text
raw trials -> exclude failures -> search endpoints -> stop when p<.05
           -> narrow naive CI -> announce 8% mean win
```

再分析は割付unitでcluster、全valid requestをITTで数え、primary metricとguardrail、事前期間を使う。

```python
analysis = aggregate_by_randomization_unit(raw, include_failures=True)
report(primary(analysis), guardrails(analysis), all_exclusions=True)
```

### よくある誤解／実務接続

- 一つだけ補正しても全pipelineの選択性は残る。
- 生データ保存だけでは分析計画の後付けを防げない。
- 再解析で非有意でも旧結果が「逆に真」とは言えない。
- blameless reviewで意思決定構造を修正する。

### 要点

1. 生成過程から監査。 2. estimand mismatchを最優先。 3. 選択機会を列挙。 4. unit/依存を修正。 5. 全指標と欠測を報告。

### 誤解チェック（5問）

1. p値補正だけで成功ログbiasは消えるか。 2. 平均改善でtail悪化は無視できるか。 3. host内反復は独立か。 4. 事後primary選択は正当か。 5. 再解析非有意は悪化証明か。

### 基礎問題（5問）

1. 誤りを六つ分類せよ。 2. 正しいunitを選べ。 3. ITTデータを再構成せよ。 4. 検定族を定義せよ。 5. guardrailを追加せよ。

### 応用問題（3問）／設計問題／調査課題

1. 事故のDAGを描け。 2. corrected CIを設計せよ。 3. decision lossで再評価せよ。 **設計:** 実験レビューchecklistとanalysis contractを作れ。 **調査:** 過去レポート一件を再現可能性の観点で監査せよ。

### 知らないとする誤判断／次章への接続

「統計ツールの出力だから客観的」と分析pipelineの裁量を隠す。最終章で典型誤判断を対策と原因の組で総点検する。

---

## 総合演習C（第21〜28章）

1. 三variant、30metric、毎日peekingする実験を、割付、estimand、FWER/FDR、停止規則、guardrail、因果仮定まで再設計せよ。
2. production modelのaccuracyが98%から99%へ上がった提案を、base rate、calibration、loss、drift、test reuse、online impactから審査せよ。
3. 二実装のbenchmarkを独立machine/day blockで再設計し、生データschemaと再現手順を作れ。

---

## 第29章　この分野を知らないエンジニアが陥りやすい誤判断

### この章を学ぶ理由／現場の問題

誤判断は公式不足より、生成過程を飛ばして数値を意思決定へ直結することで起きる。以下をレビュー時のcause-oriented checklistとして使う。

### 中心概念と正式な定義

誤判断を、標本選択 \(S\)、観測 \(D\)、モデル \(M\)、推論 \(I\)、決定損失 \(L\) のどこで起きたか分類する。妥当な結論は \(P(D\mid M,design)\) だけでなく、estimand、識別仮定、sampling、分析選択、外部妥当性に条件づく。

### 直感 → 図解 → 数式 → 例 → 実装

```text
population -> selected/observed data -> model -> estimate -> action
               bias/cluster          assumptions    loss
```

```python
review = {"estimand": None, "unit": None, "missingness": None,
          "multiplicity": None, "uncertainty": None, "decision_loss": None}
```

### Countermeasures：誤判断22例

1. **対策: 母集団・標本枠・観測標本を分ける（想定原因: ログが母集団そのものだと思う）。** 欠測とsampling rateを保存する。
2. **対策: request/user/sessionのどれがunitか事前固定する（想定原因: 行数を独立標本数と数える）。** cluster-robust推論を使う。
3. **対策: 分子・分母・期間をmetric contractに書く（想定原因: rateは名前だけで比較できると思う）。** 分母変化を別指標にする。
4. **対策: 条件付き確率の向きを数式で確認する（想定原因: 感度を陽性的中率と読む）。** base rateを必ず表示する。
5. **対策: 平均とpercentile、散布、timeout率を併記する（想定原因: 平均が典型体験を代表すると思う）。** tailをguardrailにする。
6. **対策: 生成機構から分布を選び残差診断する（想定原因: bell shapeを標準仮定とする）。** heavy-tail/zero inflationを候補にする。
7. **対策: p値をH0下のtail probabilityと表示する（想定原因: H0が真の確率と読む）。** 効果量と区間を主表示にする。
8. **対策: 非棄却時はpowerと同等性marginを確認する（想定原因: p>.05を差なし証明と読む）。** 必要ならequivalence testを使う。
9. **対策: 絶対差・相対差・baselineを一組で報告する（想定原因: 相対改善だけで価値を誇張する）。** percentage pointを明記する。
10. **対策: primary metricと停止規則を事前登録する（想定原因: 有意になるまで見るのも同じ検定と思う）。** sequential設計なら専用境界を使う。
11. **対策: 検定族を列挙しFWER/FDRを選ぶ（想定原因: 各p値が個別に5%なら全体も5%と思う）。** 探索結果は再現実験へ回す。
12. **対策: 無作為割付、exposure、analysis populationを分ける（想定原因: exposure済みだけの比較が公平と思う）。** ITTを基本にする。
13. **対策: SRM・欠測・instrumentationを効果より先に検査する（想定原因: A/Bツールが割付と計測を自動保証する）。** データ品質失敗なら実験を無効化する。
14. **対策: DAGでconfounder・mediator・colliderを区別する（想定原因: 観測した全変数を調整すれば因果になる）。** 調整集合に根拠を残す。
15. **対策: 予測riskと介入効果を別のestimandにする（想定原因: 高精度featureを変えれば結果も変わると思う）。** 因果検証を別設計する。
16. **対策: benchmarkの独立run、randomize、blockを設計する（想定原因: loop iterationを独立反復と数える）。** 環境と生値を保存する。
17. **対策: p99集約にはraw分布かmergeable sketchを使う（想定原因: percentileを平均できると思う）。** 集約誤差を文書化する。
18. **対策: retry、timeout、censoringを観測生成過程へ入れる（想定原因: 欠測を成功または最大値で代用できると思う）。** 生存解析等も検討する。
19. **対策: test setを一回限りの境界として管理する（想定原因: 再利用しても未知データ評価のままだと思う）。** 新しいholdoutを用意する。
20. **対策: posterior/CIの意味と仮定をUIに書く（想定原因: 95%という数字は手法を越えて同じ意味と思う）。** prior感度とcoverageを区別する。
21. **対策: n増加前にbias・drift・依存を診断する（想定原因: 大数の法則が全誤差を消すと思う）。** 有効標本数を推定する。
22. **対策: 推定結果を意思決定損失と実務閾値へ接続する（想定原因: 最小p値の案が最良判断と思う）。** 誤警報・見逃し・実装費を比較する。

### よくある誤解／実務接続

- checklistは思考の代替でなく、仮定を表面化する道具。
- 精緻なモデルでも測定・選択設計を救えない。
- 「統計的に正しい」と「ユーザーに価値がある」を分ける。
- experiment review、SLO review、ML model card、benchmark reportへ同じ項目を埋め込む。

### 要点

1. 生成過程を先に描く。 2. estimandとunitを固定。 3. biasとvarianceを分ける。 4. 選択機会を開示。 5. effect・uncertainty・lossで判断。

### 誤解チェック（5問）

1. 大標本ならbiasは消えるか。 2. p<.05なら実務価値があるか。 3. A/Bなら計測欠測を無視できるか。 4. 高相関なら因果か。 5. percentileを単純平均できるか。

### 基礎問題（5問）

1. 分析のestimandを一文で書け。 2. 独立unitを特定せよ。 3. 欠測経路を描け。 4. 絶対/相対効果を計算せよ。 5. 区間を正しく解釈せよ。

### 応用問題（3問）／設計問題／調査課題

1. optional stoppingとmultiple metricsが重なる実験を再設計せよ。 2. clusterとdriftを含むCIを提案せよ。 3. predictionをcausal decisionへ誤用した例を修正せよ。 **設計:** 組織共通のstatistical analysis contractを設計せよ。 **調査:** 過去三判断をこの22項目で監査せよ。

### 知らないとする誤判断／次章への接続

数字の桁数とツールの権威を確実性と取り違える。本書の次は、実データで「仮定→simulation→診断→決定」を反復し、分析契約をコードとレビューへ定着させる。

## 参考文献

- Larry Wasserman, *All of Statistics*, Springer, 2004.
- George Casella, Roger L. Berger, *Statistical Inference*, 2nd ed., Duxbury, 2001.
- Judea Pearl, Madelyn Glymour, Nicholas Jewell, *Causal Inference in Statistics: A Primer*, Wiley, 2016.
- [American Statistical Association Statement on p-Values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf)
- [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/)
- [Google SRE Workbook: Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [SciPy statistical functions documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)

---

## 付録　専門家の思考を測る

### 専門家が共有する5つの中核的メンタルモデル

1. **データは生成過程の痕跡である。** 数字だけを見ても、誰が母集団に入り、何が観測され、何が欠測し、どの操作で記録されたかは分からない。専門家は分析手法を選ぶ前に `population → selection → measurement → recorded data` を描き、設計が許す推論の範囲を決める。
2. **確率は結合分布を条件で切ったものである。** 独立性、交絡、選択bias、Bayes更新はすべて「何に条件づけた分布か」という同じ問いで読める。式を見るときも `P(Y|X)` の条件集合を増減したときに結論がどう変わるかを考える。
3. **データ・推定量・推定対象を分離する。** 観測値、そこから計算する規則、知りたい母数やestimandは別物である。専門家は一つの推定値を答えとせず、反復したときのbias、variance、coverage、識別可能性を問う。
4. **不確実性には減らせるものと減らせないものがある。** 標本を増やせばsampling varianceは減るが、系統bias、測定誤差、model misspecification、母集団の変化は自動では消えない。MSEを論じる場面では `MSE = variance + bias²`（加えて予測では既約noise）という分解を使い、それ以外の場面でもsampling variability、systematic bias、model/design failureを区別して、追加データと設計変更のどちらが必要かを判断する。
5. **推論の終点は行動と損失である。** 統計的有意性は意思決定規則ではない。効果の大きさ、不確実性、偽陽性・偽陰性の非対称な損失、介入可能性を合わせ、「観測した関連」から「何をすると何が変わるか」へ進めるかを検査する。

### 専門家の意見が根本的に分かれる3つの論点

1. **確率は長期頻度か、知識の不確実性か。**
   - **頻度主義の最も強い主張:** 手続きの誤り率を、未知母数への主観的分布に頼らず反復可能な設計で校正できる。規制・臨床試験・品質管理のように、誰が分析しても同じcoverageやtype I errorを要求する場面で強い。
   - **Bayes主義の最も強い主張:** 意思決定者が本当に必要とするのは、観測後の仮説・母数・将来事象に対する不確実性である。事前情報と階層構造を明示的に統合し、小標本や逐次判断でも一貫した確率計算を行える。
   - **判断を分ける制約:** 反復手続きの公的保証が中心か、個別案件の意思決定が中心か。妥当なpriorを共有できるか、感度分析とcalibrationを検証できるかで選択が変わる。
2. **正しいmodelで効率を得るか、仮定を弱めて頑健性を得るか。**
   - **parametric/model-based側の最も強い主張:** 生成機構を十分に表すmodelは、少ないデータから精度の高い推定と外挿を可能にし、構造についての科学的知識も表現できる。仮定を避けることは情報を捨てることでもある。
   - **robust/design-based側の最も強い主張:** 現実のmodelは必ず誤指定され、精密な結論ほど壊れやすい。randomization、再標本化、sandwich推定、部分識別など、弱い仮定でも保証が残る方法を優先すべきである。
   - **判断を分ける制約:** 外挿の必要性、sample size、生成機構の安定性、誤指定時の損失、診断可能性。専門家は両方を実行し、結論が仮定に敏感かを見ることも多い。
3. **因果推論は設計を中心に置くか、構造modelを中心に置くか。**
   - **randomization/design-first側の最も強い主張:** 因果効果は比較可能な反実仮想を作る割付設計から最も信頼して識別できる。複雑な観測modelより、無作為化・自然実験・明示的estimandを優先すべきである。
   - **structural/graphical側の最も強い主張:** 実験不能な問題でも、DAGや構造方程式で因果仮定を可視化すれば、調整すべき変数、してはいけない調整、transportabilityを論理的に導ける。設計だけでは扱えない介入系列やmechanismも表現できる。
   - **判断を分ける制約:** 介入可能性、倫理、spillover、時間変化、domain knowledgeの質。両陣営とも識別仮定なしに観測データから因果が出るとは考えない。

### 深い理解と暗記を見分ける10の質問

1. 100万requestを分析してp値が極小になった。なぜ「十分な標本」とは限らないのか。独立単位、選択、effect sizeの三方向から説明できるか。
2. 障害率が1%から0.5%へ改善したが、同時に計測対象requestの定義が変わった。どのestimandを復元し、何を追加収集すれば比較可能になるか。
3. 検定が非有意だった結果について「差がない」と結論するには、通常の仮説検定以外にどの設計と量が必要か。
4. 平均latencyは改善しp99は悪化した。単一の代表値へ潰さず、利用者影響とcapacityをどう判断するか。
5. 全体ではA案が優れるが、全segment内ではB案が優れる。どの集計が正しいかを決めるため、生成過程と因果graphをどう調べるか。
6. A/B testで離脱した利用者のeventが記録されない。単なる欠測として補完する前に、どのbiasとestimandの変化を疑うか。
7. 高精度の障害予測modelがrelease後に役立たない。base rate、calibration、decision threshold、concept driftをどう切り分けるか。
8. 観測研究で強い相関が得られた。因果効果を識別するために必要な仮定を列挙し、そのうちdataだけでは検証できないものを説明できるか。
9. Bayesian credible intervalと頻度主義confidence intervalが似た数値になった。解釈と保証はなぜ同じとは限らず、どのsimulationで差を検査できるか。
10. 二つの施策の期待利益が同じだが、一方は小さな損失が頻発し、他方は極稀に壊滅的損失を出す。平均だけで選ばず、どのloss functionと不確実性を意思決定へ入れるか。
