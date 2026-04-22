# 世界トップ企業・一流現場の MLOps / ML 実務 事例集

このドキュメントは、**ML 実務における世界クラスの具体例と工夫**を、テーマ別に整理した事例集です。各社のエンジニアリングブログ・論文・公開講演（KDD、RecSys、MLSys、CVPR、NeurIPS、Strata 等）で広く紹介されている内容をベースにしています。

## このドキュメントの読み方

- **目的**: 自分たちの設計を相対化する。**どこが業界の標準で、どこから先は投資判断か**の感覚を持つ。
- **注意**:
  - 各社の内部構成は**継続的に進化**しており、ここに書かれた構造がそのまま今も動いているとは限らない。
  - 非公開の詳細は除き、**公開情報に基づくパターン**として扱う。重要な判断で引用する場合は、最新の一次情報で再確認すること。
  - 「トップ企業だからこれをやる」ではなく、**「自社の規模・制約に合うか」**で取捨選択する。丸呑みは最悪の学び方。

既存の縦串（[research_validation_mindset_ja.md](./research_validation_mindset_ja.md)、[mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md)）の**具体例**として読むのが最も効果的です。

### 各章の読み方（共通テンプレ）

各セクションを読む際は、次の 4 点をメモに書くと、後から自分たちのロードマップに落としやすくなります。

1. **教訓 1 行**: その事例から持ち帰る設計原則は何か。
2. **自社のミニ版**: 人数・データ規模・規制の制約下で、**明日からできる縮小版**は何か（例: Feature Store ではなく `features.py` の単一モジュール化）。
3. **前提条件**: その工夫が効くために、先に揃っていた組織・データ・トラフィックは何か。
4. **取らない判断**: 自社ではコスパが悪いと思う点（無理に真似しないことを明示）。

---

## 1. 社内 ML プラットフォーム（End-to-End）

ML ライフサイクルの全工程を内製プラットフォーム化した例です。共通して、**プラットフォーム側で標準化し、モデルチームは差分だけに集中**する設計です。

### Uber — Michelangelo

- 2015 年頃から内製、2017 年に公開。UberEats の配達時間予測、Driver-Rider マッチング、不正検知まで横断的に動かす。
- コンポーネント: データ取り込み、**Feature Store（Palette）**、トレーニング（Horovod を内製して公開）、モデル管理、オンライン / オフライン推論。
- 工夫: **同じ Feature を学習と推論で参照**する徹底。Feature Store を共通インフラに置くことで、train/serve skew を組織的に防いだ。
- 派生: Michelangelo PyML、Michelangelo Palette、Horovod（OSS）。

### Meta — FBLearner Flow / Looper

- FBLearner Flow は 2016 年公開。レシピ（ワークフロー）ベースの学習パイプライン。社内数千のモデルを同じ基盤で管理。
- Looper は**軽量 ML プラットフォーム**として、プロダクトチームが**モデルを意識せず ML を呼ぶ**ためのレイヤー。
- 工夫: **モデルを書かずに既存モデルを呼ぶ層**を作り、ML 専門家でないエンジニアにも ML を届けた。

### Airbnb — Bighead / Zipline / Chronon

- Bighead は end-to-end ML プラットフォーム、**Zipline（後継: Chronon）** が Feature Store / Feature Engineering 基盤。
- 工夫: 学習とオンライン推論で**同じ Feature 定義**をバックテストできる。「過去のある時点で、この Feature はいくつだったか」を正確に再現できる（point-in-time correctness）。
- 副産物: **Airflow は Airbnb が社内発で公開**した OSS。ETL とパイプラインの標準になった。

### Netflix — Metaflow / Keystone / Mantis

- **Metaflow（OSS）**: データサイエンティストが Python だけでパイプラインを書ける設計。AWS へのデプロイを透過的に。
- 工夫: **開発体験を最優先**。Jupyter での探索から本番まで同じコードで動く。ローカル実行とクラウド実行の切り替えが 1 行。
- Keystone はストリーミングデータ基盤、Mantis はリアルタイム処理基盤。

### LinkedIn — Pro-ML / Frame / Photon-ML

- Pro-ML は社内 ML プラットフォーム。Feed、People You May Know、広告、検索まで動かす。
- Frame は Feature プラットフォーム。Photon-ML は大規模な一般化線形モデル / GLMix のための OSS。
- 工夫: **ランキング基盤の多段構成**（candidate generation → scoring → ranking → re-ranking）をプラットフォーム標準に。

### Spotify — Luigi / Klio / Hendrix

- Luigi は OSS ワークフロー、Klio は音声・メディア ML パイプライン、Hendrix（旧）は ML プラットフォーム。
- 工夫: Discover Weekly など、**バッチ推薦を大量に配信する設計**に最適化。データ量に対する経済性を重視。

### Databricks / MLflow（OSS）

- MLflow: Tracking、Projects、Models、Registry。多くの企業が**自社プラットフォームの土台**に採用。
- 工夫: **言語・フレームワーク中立**の設計。最初に入れて困らない最大公約数。

### Google — TFX / Vertex AI / Kubeflow

- TFX: TensorFlow 向けの production ML パイプライン。**データ検証（TFDV）、スキーマ進化、モデル評価（TFMA）、インフラでの検証（Infra Validator）**まで標準化。
- Vertex AI（旧 AI Platform）: マネージド MLOps。Kubeflow Pipelines / Vertex Pipelines をベースに。
- 工夫: **スキーマと統計を成果物として扱う**（TFDV）。データ異常をパイプラインの一級市民に。

### プラットフォーム章から持ち帰る縮小版（社内 5〜20 名チーム向けの例）

| 大企業でやっていること | ミニ版の例 |
|-------------------------|------------|
| 社内 Michelangelo 全部乗せ | **学習ジョブ 1 本**を GitHub Actions or 単一ノート→スクリプト化 + アーティファクトを S3 に固定 prefix |
| Metaflow 級の DX | **Makefile + 同じ Docker イメージ**で train / eval / export を叩く。Jupyter は探索専用に分離 |
| TFX の TFDV 相当 | **Great Expectations / Pandera / 独自 JSON スキーマ**で、パイプライン入り口にゲートを 1 つ |
| フルレジストリ | **モデル名 + 日付 + git hash** の命名規則と、本番だけ読み取る S3 バケットを一本化 |

---

## 2. Feature Store の工夫

Feature Store は**理論より運用が難しい**コンポーネントです。公開事例で共通するパターン:

- **Uber Palette / Airbnb Zipline (Chronon)**: point-in-time correctness、オンライン/オフラインの統一、再利用ランキング（よく使われる Feature をダッシュボード化）。
- **Tecton（Uber Palette の共同創業者ら）**: マネージド Feature Store。Transform を SQL で書いて、学習と推論に同じ定義を供給。
- **Feast（OSS、Google/Gojek 発）**: 軽量 Feature Store。登録・取得のシンプルさで広く採用。
- **Twitter/X（旧称）**: Feature Service として社内共有化。タイムライン、広告、検索で同一定義を参照。

工夫の共通点:

- Feature の**オーナーとライフサイクル**を決める（誰が品質を担保するか）。
- **廃止**を機能に入れる（作るより消す方が難しい）。
- コスト/利用頻度のダッシュボード化。**使われていない Feature は計算を止める**。

### Feature Store を入れないときに最低限やること

1. **定義の単一ソース**: 特徴量計算を 1 モジュールに集約（[mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md) 4.2 Minimum）。
2. **オフライン用テーブル**の列名・型と、オンライン特徴 API のレスポンスを**同じ JSON Schema** で検証。
3. **学習時の「その時点で知ってよい情報」だけ**を特徴に含める（リーク設計レビュー）。
4. **オーナーと廃止** — Feature ごとに Slack チャネルか CODEOWNER を置き、半年触っていない列は deprecate。

---

## 3. 実験管理・A/B テストプラットフォーム

トップ企業が最もコストをかける領域の 1 つで、**年間数千〜数万の実験**を並走させる設計になっています。

### Netflix — Experimentation Platform

- 1 ユーザーが**同時に数十の実験**に参加。直交性を担保する多層割当（layering）。
- 指標体系: **主要指標、ガードレール、ノース・スター指標**を厳格に分離。長期継続指標（retention）を重視。
- 工夫: CUPED（事前データで分散を削り、検出力を上げる手法）の本番運用。実験期間を**劇的に短縮**。

### Microsoft — ExP

- Bing、Office、Azure、LinkedIn で横断利用。書籍『Trustworthy Online Controlled Experiments』（Kohavi 他）の元。
- 工夫: **「直感に反する結果こそ真実」**を制度化。サンプル比率ミスマッチ（SRM）検知、A/A テストの常時運用。

### Booking.com

- 社内で**常時 1000+ の実験**が並走。「データなしでは何も決めない」文化。
- 工夫: 実験の**失敗率が高い（効かない方が多い）**ことを明示的に文化にした。成功よりも「効かなかった」を早く知ることを評価。

### Airbnb — ERF (Experimentation Reporting Framework)

- カテゴリカル Treatment、ヘテロジニアス効果、時系列効果の扱いを標準化。
- 工夫: **ネットワーク効果 / interference** を積極的に扱う（ホストとゲストが相互に影響する事業特有の難しさ）。

### Uber — XP Platform / StatsEngine

- 1 プラットフォームでバンディット、シーケンシャル検定、Switchback（地理・時間での割当）を扱う。
- 工夫: Uber のような**強いネットワーク効果**を持つサービスで、通常の A/B では検出不能な現象を Switchback で扱う。

### Stitch Fix

- 実験より**因果推論**寄りのアプローチ（観察データからの反事実推定、uplift modeling）。
- 工夫: 実験が難しい業務（在庫、スタイリング）で、観察データの限界と可能性を現実的に使い分ける。

### 大規模実験文化の「輸入」で効くもの

全社で 1000 本の A/B は不要でも、次はそのまま取り入れやすいです。

- **主要指標・ガードレール・探索指標の分離**（Netflix 型。解釈が速くなる）
- **SRM（サンプル比率ミスマッチ）検知**（Microsoft ExP 系）。実装のバグを早期に殺せる
- **「効かない実験」を週報で晒す**（Booking.com 型）。心理的安全性が前提だが、学びの速度が上がる
- **CUPED** や類似の分散削減 — 実装コストは低く、実験期間短縮の効果が大きいことが多い

**小規模チームの注意**: 同時多発の実験は、**相互作用**で解釈不能になりやすい。同時本数に上限を設け、ログに「実験 arm ID」を必ず残す。

---

## 4. 推薦・ランキング

### YouTube — 2-stage Recommender（Covington et al., 2016）

- **Candidate Generation**（数百万→数百）+ **Ranking**（数百→数十）の 2 段構成が業界標準に。
- 工夫: **Example Age** を特徴量に入れる（新しさのバイアスをモデルに明示的に教える）。Impression Discounting。

### TikTok / ByteDance — Monolith

- **オンライン学習**を本格運用。埋め込みテーブルは**動的・コリジョンレス・衝突時のハッシュ設計**に特徴。
- 工夫: **分単位でのモデル更新**が「面白さ」の質に直結。モデル構造の工夫より、**反応の速さそのものが競争力**という発想。

### Pinterest — PinSage

- GraphSAGE を数十億ノードに拡張。ランダムウォークで近傍をサンプリングして学習。
- 工夫: グラフ ML を**プロダクションで**回すためのサンプリングと分散学習設計。推薦の多様性と新規性の指標設計。

### Meta — DLRM / HSTU

- DLRM（OSS、2019）: 広告・推薦の深層学習標準構造（dense + sparse）。
- HSTU（Hierarchical Sequential Transduction Units、2024）: Transformer で推薦を**生成型**に書き直し。
- 工夫: **推薦もスケーリング則が効く**ことを大規模実証。Generative Recommenders の潮流。

### Instagram / Facebook Feed

- 数千の候補から、**複数の目的（エンゲージメント、長期満足度、健全性）を同時最適化**する多目的ランキング。
- 工夫: **長期指標と短期指標のトレードオフ**を explicit に制御（例: クリック率を上げすぎない）。

### Spotify — Discover Weekly / Home

- 協調フィルタ + 音響特徴 + NLP の組み合わせ。週次バッチで配信。
- 工夫: **新規アーティストの exposure** を目的関数に組み込む（CFs だけだと人気アーティストに偏るため）。

### LinkedIn — Feed / PYMK / Jobs

- ランキングに**複数の目的関数**（応答確率、スパム、低品質抑制、多様性）。
- 工夫: 多目的のラグランジュ定式化と、**目的重みをダッシュボードで調整可能**にする運用設計。

### Netflix — Personalization

- **メタデータの大半を自社で作る**（人手タグ付け + ML）。同じ作品でも**ユーザーごとにサムネイル**を変える。
- 工夫: 「何を見せるか」だけでなく「**どう見せるか**（アートワーク、並び、説明）」まで個別化。

### Amazon — Item-to-Item Collaborative Filtering

- 古典（2003 論文）だが、今も多くの推薦の土台。**行列分解より先にアイテム類似度**で始めるのが実務で強い。

### DoorDash / Uber Eats — ETA・配送最適化

- 配達時間予測は**区間推定**（点推定ではなく分布）。
- 工夫: ETA の誤りは**事業 KPI に直結**（遅延通知、補償、離脱）。単なる MAE 最小化ではなく、**非対称コスト**で評価。

### 推薦の「型」を自サービスに適用するとき

大規模サービスほど **多段パイプライン**（候補生成 → スコアリング → 再ランキング）が標準です。トラフィックが小さい段階でも、**論理構造だけ**先に真似すると後で幸せになります。

- **候補の再現**: まず「何を候補に乗せるか」がバイアス源。ランダムや人気だけでは多様性が死ぬ。
- **遅延予算の分配**: 各段で何 ms まで使うかを固定。Netflix / Uber 系の「遅延予算」発想。
- **多目的**: クリックだけ最大化すると炎上しやすい。**長期満足や健全性**をガードレールに（Instagram / LinkedIn 型）。

---

## 5. 検索

### Google Search

- **Learning to Rank、BERT（2019 導入）、MUM、RankBrain、Neural Matching**と段階的に進化。
- 工夫: **Core ranking と人手評価（Quality Raters）**の二本立て。評価ガイドラインが公開されている（数百ページ）。

### Airbnb — Search Ranking（KDD 2018 Best Paper）

- リスティングとユーザーの埋め込みを学習。**予約という稀なシグナル**を予測する設計。
- 工夫: 既存のツリーモデルから深層学習に移行する際の「**失敗からの学び**」を論文で公開。素朴に DL を導入すると**悪化する**ことを正直に書いた稀な事例。

### Amazon — Product Search

- テキスト + 行動 + 在庫 + 配送速度の多要素ランキング。
- 工夫: **在庫と配送の制約**をランキングに織り込む（検索精度だけではなく、購入可能性を最適化）。

### eBay / Etsy

- 大規模なロングテール在庫。埋め込みベース検索と BM25 の**ハイブリッド**が実運用で強い。
- 工夫: **BM25 を捨てない**。DL 単独より、古典 IR とのハイブリッドが頑健。

### 検索の現場で繰り返し効く教訓

- **ハイブリッドがデフォルト**: 稀疏特徴・新規クエリでは BM25 が強く、セマンティック系は類義語・表記ゆれで強い。単一モデル信仰は危険（eBay / Etsy の教訓の一般化）。
- **オフライン指標とオンライン指標のギャップ**: クリックや滞在は介入と相関しがち。**人手評価セット**（Google の Rater）のミニ版を社内で持つと意思決定が楽になる。
- **Airbnb KDD 論文の教訓**: DL を足すと必ず良くなるとは限らない。**単純特徴 + 強いベースライン**の確認を省かない。

---

## 6. 広告・マーケットプレイス

### Meta Ads — Ads Ranking

- **DLRM**系を極限まで最適化。学習ハードウェアから設計。
- 工夫: オークション + ランキング + 予算ペーシング + 広告主入札 の**連立最適化**。ここがプロダクト価値の中心。

### Google Ads — Smart Bidding

- 入札を ML 化。強化学習と供給制約下の最適化。
- 工夫: **広告主向けに「効果量」を説明できる形**でモデルを出す。内部精度と外部説明のバランス。

### Criteo

- 業界有数の広告 CTR 予測。**Criteo 1TB dataset** が公開され、多くの研究の基礎に。
- 工夫: ハッシュトリック、特徴量工学、online/offline consistency が広告 ML の基本語彙に。

### 広告で学べる「実務の基本語彙」

自社が広告事業でなくても、次の概念は **スパム・不正・リスクスコア** に転用されます。

- **Calibration**（スコアと確率の一致）: 入札や閾値に直結
- **Delayed feedback**（転換が遅れてラベルが遅延）: 学習データの補正が必要
- **Exploration / exploitation**: 新広告主や新施策とのトレードオフ
- **極度の疎な特徴**: ハッシュトリック、**未知カテゴリ**への一般化

---

## 7. 生成 AI / LLM（2023-2026）

### OpenAI

- **GPT-4/4o/5 系列**: 大規模事前学習 → RLHF → ツール使用・エージェント化。
- 工夫: **InstructGPT の RLHF パイプライン**を実運用規模で標準化。Evals（OSS）で評価の再現性。System Card / Model Spec の公開。

### Anthropic

- **Constitutional AI / RLAIF**: 人手フィードバックを減らし、原則（Constitution）に基づく自己改善。
- 工夫: Interpretability（mechanistic interpretability）への本格投資。**Responsible Scaling Policy** で安全性の閾値をモデル能力に結びつける。

### Google DeepMind — Gemini

- **ネイティブマルチモーダル**（画像・音声・動画・テキストを最初から混ぜて学習）。
- 工夫: TPU スタック最適化。**Ultra-long context**（1M+ tokens）を実用域に。

### Meta — Llama 系

- **オープンウェイト**で公開し、業界標準のベースに。
- 工夫: **Research SuperCluster（RSC）** で大規模学習、Llama 3 / 4 でデータ品質と事後学習（SFT/DPO/RLHF）を軸に進化。

### Mistral / Cohere / xAI

- Mistral: Mixture-of-Experts（Mixtral）を早期に実用域に。
- Cohere: 企業特化、検索特化のモデル群。
- xAI: Grok。巨大 GPU クラスタ（Colossus）での訓練速度を競争力に。

### 運用側の工夫（共通パターン）

- **評価セットの自前構築**: 公開ベンチマークは汚染されやすいので、**社内ドメイン評価セット**を必ず持つ。
- **Prompt + モデル + ツール**の組をバージョン管理（「モデルだけ」では再現不能）。
- **LLM-as-Judge** と人手評価のハイブリッド。LLM 評価のバイアスを監視。
- **プロバイダ切替**を設計段階で可能に（プロバイダ固有機能にロックされない抽象化）。

### LLM 運用のチェックリスト（短く）

| 観点 | 世界的に繰り返されている対策 |
|------|------------------------------|
| 評価 | **社内ゴールデンセット** + カテゴリ別（安全・事実・スタイル） |
| 版管理 | モデル ID + プロンプト版 + few-shot 例 + ツール定義を **BOM 化** |
| 安全 | 入力フィルタ、出力フィルタ、ツール権限の最小化（[system_operation_maintenance/05_ai_specific_ops.md](../system_operation_maintenance/05_ai_specific_ops.md)） |
| コスト | **リクエストあたり上限**・異常検知・キャッシュ方針 |
| 回帰 | **リリース前の自動評価**（少数でもよいので必須） |

---

## 8. RAG / 検索拡張生成の実務

### Perplexity

- **リアルタイム Web 検索 + LLM + 引用必須**の UX を標準化。
- 工夫: 引用を**第一級の成果物**として扱う。Hallucination を UX で抑え込む設計。

### Notion AI / Slack AI / Microsoft Copilot

- エンタープライズ RAG。**権限（ACL）を検索段階で透過的に反映**するのが最大の実装課題。
- 工夫: **ユーザーごとに見える文書**しか回答の根拠にしないテナント分離。監査ログ、プロンプトインジェクション対策。

### GitHub Copilot / Cursor / Codeium

- **コード補完と対話**の両立。エディタ内でのレイテンシ制約（数百 ms 以内）。
- 工夫: **コンテキスト選択**（関連ファイルの抽出）がモデル品質より効く場面が多い。評価は**受入率**を長期指標に。

### エンタープライズ RAG で躓く順（現場メモ）

多くのプロジェクトで、次の順に壁が来ます。**対策もセットで**。

1. **権限**: 検索層で ACL を効かせないと、一度で事業終了級の事故になりうる（Notion / Copilot 系の発想）。
2. **チャンク設計**: 長すぎるとノイズ、短すぎると文脈欠落。**オーバーラップ**と見出し単位の経験則をドキュメント化。
3. **ヒットしない**: 用語正規化、別名辞書、クエリ書き換え（hybrid: BM25 + ベクトル）。
4. **幻覚**: 引用必須 UX（Perplexity 型）または「根拠なき場合は不明と答える」ポリシー。
5. **鮮度**: インデックス世代と再取り込み SLO。**古い規程を読む bug** は運用カテゴリ。

---

## 9. コンピュータビジョン・自動運転

### Tesla — Data Engine（Autopilot）

- Karpathy らが CVPR/ICML で公開した「**Data Engine**」フレームワーク。
- フロー: 希少・難例をフリート（車両群）から自動収集 → ラベル付け → 学習 → 再デプロイ → 再収集。
- 工夫: **モデルより、難例データを取りに行く仕組み**が競争力の中心。Shadow mode で新モデルを走らせるが介入はしない（ログだけ取る）。

### Waymo — Carcraft / Simulation

- シミュレーション走行が実走行を大きく上回る。
- 工夫: **希少事象の合成**（歩行者の飛び出し等）。実走行では出会えないケースを先回り。ChauffeurNet（模倣学習 + 摂動）。

### Cruise / Zoox / Wayve

- End-to-end ニューラルネットワーク運転（Wayve）vs モジュラー構成の比較が業界で継続。
- 工夫: **Foundation Model の走行への転用**（Wayve GAIA、Tesla FSD v12）。

### Meta / Google — Visual Foundation Models

- DINOv2（Meta）、SigLIP（Google）、SAM / SAM 2（Meta）が下流タスクの基盤に。
- 工夫: **ドメイン特化チームは、自社データで Foundation Model を fine-tune**する方が、スクラッチより速く・安く・強い。詳細: [object_detection/](../object_detection/)

### CV / 自動運転から一般データサイエンスへ戻す要点

- **Data Engine**: モデルより「**何を学習データにするか**」の仕組み（Tesla）。物体検出の [04_training_playbook.md](../object_detection/04_training_playbook.md) と接続。
- **Simulation**: 現実の希少事象はシミュレーションで増やす（Waymo）。社内向けなら**合成データ・GAN / 摂動**も同じ発想。
- **Foundation 活用**: [object_detection/](../object_detection/) 全体が、現場での転用の型。

---

## 10. 不正検知・リスク

### Stripe — Radar

- **数億件の決済データ**で学習。リアルタイムで数 ms でスコアリング。
- 工夫: **False Positive のコスト（顧客離脱）と False Negative のコスト（被害）**を明示的に非対称に扱う。閾値は加盟店ごとに最適化。

### PayPal / Square

- グラフ ML（アカウント間の関係）を実運用。adversarial な相手が **学習する**ので、モデルも**継続的に更新**。
- 工夫: 攻撃者の適応を**想定して**特徴量を設計（安定すぎる特徴は回避されやすい）。

### 銀行（JPM、Goldman 等）

- 規制の制約で**説明可能性（XAI）**を強く要求される。
- 工夫: ツリーモデル + SHAP + 人手レビューが主戦場。DL 化は**説明責任が果たせる領域**から。

### 敵対的ドメイン共通の教訓

不正・スパム・Bot は**適応する相手**です。静的なモデルは必ず古くなる。

- **特徴量の寿命**を短く見積もり、**連続的ラベル付け**と再学習のサイクルを前提にする（PayPal 型）。
- **グラフ特徴**は強力だが、プライバシー・説明・計算コストとトレードオフ。
- **非対称コスト**を数値化し、閾値を事業横断で固定（Stripe 型）。

---

## 11. データ品質・パイプライン

### Netflix — Data Mesh / Data Quality

- 自動データテスト、Auditor（データ品質アラート）、**WAP（Write-Audit-Publish）**パターン。
- 工夫: データが**本番テーブルに入る前に**品質検査を通す。壊れたデータが下流に流れない設計。

### Airbnb — Data Quality Initiative

- 2019 頃のデータ品質改善プロジェクト。**Midas（認証データセット制度）**でデータに「SLA」を付ける。
- 工夫: 誰でも作れるデータと、**信頼できるデータ**を組織的に区別。

### Monte Carlo / Great Expectations / Soda

- データオブザーバビリティの標準化。スキーマ・分布・鮮度の監視を SaaS / OSS で。

### データ品質は「ツールよりプロセス」

Netflix / Airbnb のような取り組みの核心は、ツール名ではなく次です。

- **本番テーブルに入る前のゲート**（WAP）
- **信頼できるデータセットにバッジを付ける**（Midas）
- **データオーナーと SLA** の明文化

10 名未満のチームでは、**「信頼テーブル」のホワイトリストを 1 枚決める**だけでも効果が出ます。

---

## 12. トレーニングインフラ・GPU 運用

### Meta — Research SuperCluster (RSC) / Grand Teton

- **Llama 系列の学習基盤**。16,000 GPU 超。RDMA / InfiniBand / 専用ストレージ。
- 工夫: **GPU 故障率が規模の敵**。Checkpointing の頻度、故障 GPU の切り離しと再投入を自動化。

### Microsoft / OpenAI — Azure AI Supercomputer

- GPT-4 系列の学習基盤。
- 工夫: **冷却・電力・ネットワーク**のハードウェア層からの共同設計。

### Google — TPU Pods

- v2 → v3 → v4 → v5p → Trillium と進化。
- 工夫: **学習ソフトウェアスタック（JAX、XLA、Pathways）**をハードと共設計。PyTorch 主流の中で独自路線を維持。

### NVIDIA — NeMo / Megatron-LM / TensorRT-LLM

- 学習から推論までの参照実装 OSS。ほぼ業界標準。
- 工夫: **ハードウェア + OSS 参照実装**で生態系を牽引。

### 共通の運用工夫

- **Spot / Preemptible**の活用とチェックポイント戦略。詳細: [object_detection/12_cloud_gpu_training_practice.md](../object_detection/12_cloud_gpu_training_practice.md)
- **分散学習のデバッグ**（NCCL エラー、stragglers、データローダボトルネック）が現場の主戦場。
- **Mixed Precision / FP8 / 量子化**は今や前提。

### 大規模学習の教訓を中小規模に縮小するとき

- **チェックポイント**: 規模が小さくても、**失敗の主因は人間とクラウドの両方**。時間間隔とストレージコストのバランスを Runbook に書く（[object_detection/12_cloud_gpu_training_practice.md](../object_detection/12_cloud_gpu_training_practice.md)）。
- **ストラグラ（遅いワーカー）**: 分散のときほど、`DataLoader`、I/O、不均衡データがボトルネックになりやすい。
- **再現性**: 大企業ほど Git + コンテナ + データスナップショットの三点セットが当たり前に。

---

## 13. 推論インフラ・サービング

### Netflix — Bulletproofing Personalization

- **フォールバック階層**を明示設計。個別化サービスが落ちても**古いパーソナライズ、地域人気、グローバル人気**と段階的に縮退。
- 工夫: **サービスとして落とさない**ことが、個別化精度より優先される場面を認める。

### Meta — AI Inference at Scale

- **カスタム推論アクセラレータ（MTIA）**を開発。PyTorch を推論最適化スタック（AITemplate など）経由で展開。
- 工夫: レコメンドの**埋め込みテーブルが TB 級**。メモリ階層設計が最優先。

### Uber / DoorDash / Airbnb — Online Inference

- 共通: **Feature Store + gRPC / Thrift サービス + Cache**。p99 レイテンシが事業 KPI 直結。
- 工夫: ランキングは多段で、各段で**遅延予算を明確に分配**する。

### vLLM / TGI / SGLang（OSS）

- LLM 推論の OSS。PagedAttention、Continuous Batching、Speculative Decoding。
- 工夫: **バッチング戦略**で GPU 利用率を劇的に上げる。自社運用する組織が採用。

### 推論側でコピーしやすいパターン

- **段階的フォールバック**（Netflix）: 推論失敗時に**粗いが必ず返る**結果へ。SLA の本質。
- **埋め込みテーブルのメモリ設計**（Meta）: レコメンド規模なら、まず**特徴の次元と量子化**から疑う。
- **レイテンシ予算**（Uber / DoorDash）: p99 をビジネス要件として固定し、各コンポーネントに割り当て。

---

## 14. モニタリング・可観測性（ML 固有）

### Uber / Airbnb / Netflix

- **Drift Detection** を Feature Store と統合。学習時の統計を「真実」として保存。
- 工夫: ドリフトアラートを**闇雲に鳴らさず**、業務 KPI が連動しているドリフトだけエスカレーションする二段構え。

### Fiddler / WhyLabs / Arize / Evidently

- ML オブザーバビリティの SaaS / OSS 群。特徴量分布、予測分布、バイアスを可視化。
- 工夫: **「ドリフトしたから再学習」ではなく、「KPI が壊れたから調査→再学習」**というルーティングを入れる。

### アラート疲れを避けるコツ

- **ページャーに乗せるのは「サービスが落ちる系」だけ**。ドリフトはチケットや週次レビューへ。
- **ダッシュボードは「変化の幅」**（前週比、ベースライン比）を既定表示に。
- モデル監視は [mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md) の BOM とセットで見る。

---

## 15. 組織・プロセスの工夫

技術以上に差が出るのが、組織設計です。

### Netflix — Full Cycle Developers

- データサイエンティストが**学習から本番運用まで**持つ。Ops チームに投げない。
- 前提: ツール（Metaflow 等）が**自己完結的に運用可能**なレベルに整備されている。

### Meta — Platform + Product の二層

- プラットフォームチームが共通インフラ、プロダクトチームがモデル。明確な責務分離。
- 工夫: プラットフォームは**プロダクトの成果で評価**される（内部顧客満足度、モデル立ち上げまでの時間）。

### Airbnb — ML Infrastructure as Product

- プラットフォームを**社内プロダクト**として扱う。ドキュメント、サポート、ロードマップ、四半期レビュー。

### Google — Launch / Iterate / Impact Review

- 打ち上げ前後のレビュー文化。**「何を学んだか」が主目的**で、成功だけが評価されない。

### Shopify / Spotify — Squad / Guild

- ドメイン別 Squad + 横断 Guild。ML 専門家が**各 Squad に散り**、Guild で標準化。

### 共通する組織パターン

- **モデルより、データと評価の所有権**を先に決める。
- **オンコール**の責任がチームごとに閉じている（プラットフォームはプラットフォームの SLA、プロダクトはプロダクトの SLA）。
- **失敗のレビュー**（post-mortem）が非難なしで回る。

---

## 16. 業界横断で共通する「工夫のパターン」

個別事例を俯瞰すると、優れた現場には共通のパターンがあります。

1. **プラットフォームで標準化、モデルで差別化**  
   学習基盤・推論基盤・Feature Store は全社共通。モデル自体の独自性は、その上に薄く乗せる。

2. **評価セットは自前で作る**  
   公開ベンチマークは参考。業務で本当に使う評価は、**社内で、ドメインに合わせて**、長期的に育てる。

3. **ガードレールを先に書く**  
   攻める指標と、壊してはいけない指標を**先に**分離。あとから書くと、自分で書いた基準を自分で通せなくなる。

4. **データの質に最も投資する**  
   モデル改善の 80% は、データ（収集・ラベル・版管理・監視）の改善が源泉。

5. **小さく出して、早く学ぶ**  
   Shadow / Canary / Ramp-up を標準にする。**全量展開で学ぶのは最もコストが高い**。

6. **ロールバックを文化にする**  
   戻すことを失敗と呼ばない。戻せることが前提の設計を、組織の評価軸にする。

7. **難例データ収集を仕組みにする**  
   Tesla の Data Engine、HITL ラベリング、ユーザーフィードバック。**難例こそが次の改善の燃料**。

8. **モデル/閾値/プロンプトの独立バージョン管理**  
   この 3 つは**異なる周期で動く**。一緒くたにすると、緊急時の対応速度が落ちる。

9. **プロバイダ / フレームワーク依存から距離を取る**  
   抽象化レイヤーで、ベンダー固有機能を**必要最小限**に閉じ込める。

10. **失敗をオープンにする**  
    Booking.com の「実験の多くは効かない」、Airbnb の「深層学習導入で失敗した」。これを公開する文化が、内部の学びを加速する。

### パターン一覧を「投資判断」に落とす例

| パターン | 先に投資が必要な基盤 | 効果が出やすい事業特性 |
|----------|----------------------|------------------------|
| プラットフォーム標準化 | 共通 CI、開発者体験 | モデル本数が多い |
| 自前評価セット | ラベル付けリソース | ドメイン特化・コンプライアンス強い |
| データ品質ゲート | データ契約・オーナー | 上流システムが多い |
| Shadow / Canary | デプロイ自動化・観測 | トラフィックが十分大きい |
| オンライン学習 | 低レイテンシ基盤 | フィードバックが早い（広告・推薦） |

---

## 17. 情報源（一次情報）

各社のエンジニアリングブログと主要カンファレンスが一次情報として最も信頼できます。**四半期に一度**くらいの頻度で巡回すると、業界の空気が分かります。

- ブログ: Uber Engineering、Meta Engineering、Airbnb Tech、Netflix Tech、Spotify Engineering、LinkedIn Engineering、Pinterest Engineering、DoorDash Engineering、Stripe Engineering、Shopify Engineering、Booking.com、Etsy Engineering、Google Research、DeepMind、Microsoft Research、NVIDIA Developer、Databricks
- カンファレンス: MLSys、KDD、RecSys、NeurIPS、ICML、CVPR、EMNLP、SIGIR、WWW、Strata、QCon、NeurIPS Datasets & Benchmarks、LLM in Production（各種）
- 書籍:
  - 『Designing Machine Learning Systems』（Chip Huyen）
  - 『Machine Learning Design Patterns』（Lakshmanan 他）
  - 『Trustworthy Online Controlled Experiments』（Kohavi、Tang、Xu）
  - 『Reliable Machine Learning』（Chen 他）
  - 『Building Machine Learning Powered Applications』（Emmanuel Ameisen）

---

## 18. このドキュメントの使い方

読んで「真似する」ためではなく、**自分たちを相対化する**ために使います。

- 自分たちの**現在地を 1 つ特定**する（例: Feature Store は無いが、point-in-time correctness は共通ライブラリで担保している）。
- 次に**投資すべき 1 領域を特定**する（例: 実験管理が弱い → まず実験管理から）。
- トップ企業の**真似ではなく、自社規模に合ったミニ版**を設計する（[mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md) の「最小一筆書き」を参照）。
- **年 1 回**このリストを見直し、業界の標準が動いたかを確認する。

### ワークシート: 自社への投影（コピペ用）

```text
【現在地】うちのチームは world_class_case_studies の「共通パターン」10 のうち、どれが最も弱いか:
  最弱: ___  理由: ___

【次の 1 投資】四半期で入れるリソース (__ 人週）で、上を改善する具体策:
  _________________________________

【真似しないこと】規模・規制・トラフィックの理由で、意図的に捨てる標準:
  _________________________________

【検証】投資後に見る主要指標 1 つとガードレール 2 つ:
  主要指標: ___  ガードレール: ___ / ___
```

---

## 関連ドキュメント

- 検証・R&D のマインドセット: [research_validation_mindset_ja.md](./research_validation_mindset_ja.md)
- MLOps の基本と現場レベルの考え方: [mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md)
- AI 固有の運用論点: [system_operation_maintenance/05_ai_specific_ops.md](../system_operation_maintenance/05_ai_specific_ops.md)
- ML システム設計: [system_design/16_ml_ai_systems/README.md](../system_design/16_ml_ai_systems/README.md)
- 推論システム設計: [system_design/16_ml_ai_systems/ml_inference_design.md](../system_design/16_ml_ai_systems/ml_inference_design.md)
- 物体検出の実務: [object_detection/](../object_detection/)
- クラウド GPU 学習の現場判断: [object_detection/12_cloud_gpu_training_practice.md](../object_detection/12_cloud_gpu_training_practice.md)
