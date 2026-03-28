# Vision Language Model（VLM）を用いた物体検出 — bbox 正確性と実務判断（2025〜2026 近傍レポート）

この文書は、**Vision Language Model（VLM）／マルチモーダル LLM（MLLM）**を物体検出に使う流れのうち、特に **バウンディングボックス（bbox）の正確性（localization）** に焦点を当てた整理です。論文・公式・ブログ・コミュニティ情報を横断して要点を掛け合わせていますが、**数値は原典を必ず確認**してください（ベンチマーク条件やプロトコルが異なるため）。

> **位置づけ**: 本リポジトリの他ドキュメント（closed-set 検出、`mAP` 設計、[04_training_playbook.md](./04_training_playbook.md)）は「クラス固定・本番 mAP 最適化」が主役です。本文書は **open-vocabulary / grounding / 生成型座標** という隣接領域の **設計判断材料** を増やすための補遺です。

**調査メモの日付**: 2026-03-21 時点のウェブ検索・公式ページに基づく。Qwen 系は **月単位でモデル・推奨 `transformers` 版が更新**されるため、実装前に **Hugging Face モデルカードと Qwen 公式ブログ**を必ず再確認してください。

---

## 1. まず結論 — プロが 2025 年前後でよく言うこと

1. **「VLM をそのまま本番の唯一の検出器にする」は少数派**。多くの現場では、**専用 detector（YOLO / RF-DETR / Grounding DINO 系のファインチューン品）で mAP・latency を取り**、VLM は **説明・クエリ理解・ラフな候補・pseudo-label / QA** に寄せる **ハイブリッド** が安定しやすい、という割り切りが多い。  
2. **bbox の厳密さ**は、closed-set の SOTA 検出器に比べると、まだ **クエリの言い回し・解像度・キャリブレーション・幻覚**の影響を受けやすい、という認識が研究コミュニティ側でも共有されつつある（後述のサーベイ・幻覚系研究）。  
3. **fine-tuning は効くことが多い**が、典型トレードオフは「**ターゲット表現・ドメインには強くなるが、ゼロショット汎化や未見クエリの較正が崩れる**」であり、OWLv2 の OpenReview 付録でも cross-query calibration / fine-tune trade-off が注意されている。  
4. **「検出を生成モデル（座標トークン）に埋め込む」系**は 2025 後半に具体例が増え、**幾何に対する RL 報酬**などで box 品質を詰める動きが見える（`Rex-Omni` が代表例のひとつ）。

---

## 2. 「VLM を使った物体検出」という曖昧語の分解

実務の会話で混線しやすいので、次の **4 系統**に分けると設計がブレません。

| 系統 | ざっくり説明 | bbox が出る仕方 | bbox 精度の典型的な論点 |
|------|----------------|-----------------|-------------------------|
| **A. 言語条件付き検出器** | CLIP／BERT 等でテキストを条件として **DETR 系ヘッドが直接 box 回帰** | 連続値回帰（＋損失は L1 / GIoU 等） | **学習データと短语設計**に強く依存。FT でドメイン追従しやすい。代表: Grounding DINO 系、GLIP 系 |
| **B. 画像テキストエンコーダ型 OVD** | ViT + text tower で **region と語の類似度** | 提案格子や既知アーキテクチャ上のスコア | **クロステキスト間の confidence 較正**、長尾。代表: OWL-ViT / OWLv2 |
| **C. VLM（MLLM）が座標を“テキストとして”出す** | 画像トークン＋LLM が **数値トークン列で bbox を生成** | 離散トークン（量子化座標） | **幻覚・座標形式・反復デコードコスト**。RL・SFT で補正する研究が増える。代表: 一部 Qwen-VL 系の出力形式、Rex-Omni |
| **D. ツール呼び出し型** | MLLM が **外部 detector を呼ぶ**計画を立てる | 下位モジュール依存 | **パイプライン設計**が本質。単体 bbox の上限は下位 detector |

ユーザーが「VLM 検出」と言ったとき、**A/B（従来の OVD）なのか C（生成型）なのか D なのか**を先に揃えると、`mAP` 比較や **finetune 方針**が真水で決まります。

---

## 3. bbox 正確性で何が壊れやすいか（技術論点）

### 3.1 幻覚・過検出・スコア較正

- VLM は **言語側のバイアス**で「ありそうな物体」を語ることがあり、**画像根拠のない bbox** が付くことがある。対策系の研究として、**幻覚のトークン粒度検知**（CVPR 2025: [HalLoc](https://openaccess.thecvf.com/content/CVPR2025/html/Park_HalLoc_Token-level_Localization_of_Hallucinations_for_Vision_Language_Models_CVPR_2025_paper.html) / arXiv [2506.10286](https://arxiv.org/abs/2506.10286)）、**接地情報で幻覚を減らす**（例: [GroundSight](https://arxiv.org/abs/2509.25669)）などがある。  
- OWLv2 の議論では、**クエリを跨いだ confidence の解釈**が難しい、**fine-tune すると未見クエリ側が落ちる** といった trade-off が整理されている（OpenReview 付録 [例](https://openreview.net/attachment?id=mQPNcBWjGc&name=supplementary_material)）。

### 3.2 解像度・アスペクト比・小物体

- **可変解像度・時空間の位置エンコーディング**を強化する VLM（例: Qwen2-VL 系の動的解像度・M-RoPE、**Qwen3-VL** の interleaved-MRoPE / **DeepStack**［多層 ViT 特徴の統合］や動画向けテキスト時刻アラインメント）は、**細かい接地・動画内の時系列**で有利になりやすい一方、**実装・`qwen_vl_utils` / `transformers` の版・プロンプト**に強く依存する（コミュニティ報告: [InternVL GitHub issue #1103](https://github.com/OpenGVLab/InternVL/issues/1103) のようなアスペクト比感受性は **全 MLLM で起きうる** — **再現時は自前で検証**）。

### 3.3 プロンプト依存

- 「`red car in the background`」のような **指示の粒度**で box が変わる。InternVL  docs / issues では **推奨プロンプト形式**が議論される。本番では **テンプレ固定・言い換えアンサンブル・LLM でクエリ正規化**などが現場対処になりやすい。

---

## 4. 主要モデル・研究ライン（2025 前後で名前がよく出るもの）

以下は **網羅ではなく「方角図」**です。自社ドメインでは **自前 val で箱の IoU 分布**を必ず取ってください。

### 4.1 Grounding DINO / MM-Grounding-DINO / DINO-X（言語条件付き DETR 系）

- **Grounding DINO**: オープンボキャブラリー検出の実務的デファクトのひとつ。**fine-tuning** の解説は LearnOpenCV（[Fine-Tuning Grounding DINO](https://learnopencv.com/fine-tuning-grounding-dino/)）、NVIDIA TAO（[Grounding DINO fine-tuning](https://docs.nvidia.com/tao/tao-toolkit/text/cv_finetuning/pytorch/object_detection/grounding_dino.html)）など。  
- **MM-Grounding-DINO**: Grounding DINO の改良系。Hugging Face モデルカードやコレクション（[MM Grounding DINO](https://huggingface.co/docs/transformers/en/model_doc/mm-grounding-dino)）で **COCO / LVIS などの報告数値**が参照される — **原典 Table で確認**。arXiv [2401.02361](https://arxiv.org/abs/2401.02361)。  
- **DINO-X**: 「オープンワールド検出と理解」を掲げる統合モデル。**Grounding-100M 規模の事前学習**などが売り。論文 [2411.14347](https://arxiv.org/abs/2411.14347)、API / コミュニティリソース [DINO-X-API](https://github.com/IDEA-Research/DINO-X-API)。

**bbox 精度の含意**: **連続 box 回帰**なので、従来の detector と同じく **IoU 損失・データ分布・解像度**でコントロールしやすい。FT の経験則も比較的溜まっている。

### 4.2 OWL-ViT / OWLv2（エンコーダ型 OVD）

- **スケール学習**で rare クラスが伸びた、という報告がサーベイ・ブログで繰り返し引用される（例: NeurIPS 2023 [Scaling Open-Vocabulary Object Detection](https://proceedings.neurips.cc/paper_files/paper/2023/hash/e6d58fc68c0f3c36ae6e0e64478a69c0-Abstract-Conference.html)）。技術ブログ [OWLv2 overview (Ikomia)](https://www.ikomia.ai/blog/owlv2-open-vocabulary-object-detection)。  
- Hugging Face [OWLv2 ドキュメント](https://huggingface.co/docs/transformers/model_doc/owlv2)。

**bbox 精度の含意**: **クエリ間較正**と **FT 汎化 trade-off** に注意。本番で閾値を決めるときは **クエリごと**に様子を見る運用が安全。

### 4.3 Florence-2（軽量 VLM、タスク記法で検出もこなす）

- Microsoft の **コンパクトな vision-language 基盤**。Roboflow のブログ（[Florence-2 概要](https://blog.roboflow.com/florence-2/)、[物体検出向け FT](https://blog.roboflow.com/fine-tune-florence-2-object-detection/)）がわかりやすい。  
- ドメイン適応の例として、**非構造化環境での FT** ＋ LoRA 等を扱う論文 [2503.04918](https://arxiv.org/abs/2503.04918)（Papers with Code: [ページ](https://paperswithcode.com/paper/fine-tuning-florence2-for-enhanced-object)）。

**bbox 精度の含意**: **小さめモデルで統一インターフェース**はエンジニアリングに有利。一方、**極小物体・高密度シーン**は従来 detector と **数値比較必須**。

### 4.4 Qwen2-VL / Qwen2.5-VL / **Qwen3-VL** / **Qwen3.5**（Qwen 系 MLLM の世代整理）

Qwen チーム（Alibaba Cloud）のマルチモーダルラインは、**物体検出というより「視覚接地・座標や JSON を含む構造化出力・キャプション・動画理解」**まで含む **汎用 MLLM** として使われることが多い。**bbox を直接 `mAP` で最適化したヘッドを持つ Grounding DINO 型ではない**ため、同じ「検出」と言っても §2 の **系統 C（生成型座標）**に寄りやすい。

| 世代 | 一次情報（例） | ざっくり位置づけ |
|------|----------------|------------------|
| **Qwen2-VL** | [2409.12191](https://arxiv.org/abs/2409.12191) | 任意解像度周りの強化などで広く使われた前世代 |
| **Qwen2.5-VL** | 技術報告 [2502.13923](https://arxiv.org/abs/2502.13923)、HF [Qwen2.5-VL-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct) | 2025 年前半の主力。**FT 手順・ブログが最多** |
| **Qwen3-VL** | 技術報告 [2511.21631](https://arxiv.org/abs/2511.21631)、リポジトリ [QwenLM/Qwen3-VL](https://github.com/QwenLM/Qwen3-VL)、HF 例 [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct)、`transformers` [Qwen3 VL](https://huggingface.co/docs/transformers/model_doc/qwen3_vl) | **ネイティブ 256K トークン**前後の長いインタリーブ（テキスト・画像・動画）、**Dense（2B/4B/8B/32B）と MoE（30B-A3B / 235B-A22B）**。論文要旨では **interleaved-MRoPE**、**DeepStack**（多層 ViT）、動画の **text-based time alignment** を主なアーキ更新として明示 |
| **Qwen3.5** | リポジトリ [QwenLM/Qwen3.5](https://github.com/QwenLM/Qwen3.5)、HF 例 [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)、紹介記事 *Qwen3.5: Towards Native Multimodal Agents*（モデルカード引用: [qwen.ai/blog](https://qwen.ai/blog?id=qwen3.5)、**2026-02**） | **「ネイティブ・マルチモーダル・エージェント」**を打ち出した世代。HF の利用例では **画像・動画**入力と **超長文コンテキスト**（設定次第で **1M トークン級**の議論あり）、vLLM / SGLang / `transformers serve` 等がモデルカードに記載。**MoE＋小型 Dense** の複数サイズが公開される運用 |

**bbox 精度の含意（共通）**:

- **強み**: 自然言語クエリでの **ゼロショット接地**、**複数物体・関係性・動画フレーム**を含む指示。Qwen3-VL は長コンテキスト・動画で **「どの瞬間のどこか」** に寄せたい用途と相性が良い（要は **ベンチと業務仮説の一致**）。  
- **弱み・注意**: 出力は **テキスト上の座標列・JSON** になりがち。**厳密 mAP** では (1) **形式パース**、(2) **画像座標系と正規化**、(3) **NMS / 重複出力** を自前パイプラインで揃えないと closed-set SOTA detector と**比較不可能**。  
- **実務の割り切り**: PyImageSearch の [Qwen 2.5 による detection / grounding](https://pyimagesearch.com/2025/06/09/object-detection-and-visual-grounding-with-qwen-2-5)（2025-06）のように **チュートリアルは豊富**だが、**本番は val の IoU 分布とレイテンシ**で勝負。

### 4.5 InternVL3 系（オープンソース MLLM、接地を含む多機能）

- InternVL3 紹介 [2504.10479](https://arxiv.org/abs/2504.10479)、公式 readthedocs [internvl3.0](https://internvl.readthedocs.io/en/latest/internvl3.0/introduction.html)。  
- 実運用者の **接地まわりのプロンプト・制約議論**は GitHub [Issue #1103](https://github.com/OpenGVLab/InternVL/issues/1103) などに集約されがち — **一次情報として有用**。

### 4.6 GLIP（言語画像事前学習の古典／現場ではまだ参照される）

- 公式実装 [microsoft/GLIP](https://github.com/microsoft/GLIP)。MMDetection 上の FT 議論は Issue などに蓄積（例: [open-mmlab/mmdetection#11014](https://github.com/open-mmlab/mmdetection/issues/11014)）。

### 4.7 T-Rex2（テキスト＋ビジュアルプロンプト）

- ECCV 2024: [2403.14610](https://arxiv.org/abs/2403.14610)、IDEA [GitHub T-Rex](https://github.com/IDEA-Research/T-Rex)、紹介ブログ [Medium IDEA CV](https://medium.com/@ideacvr2024/exploring-the-t-rex2-family-part-1-t-rex2-an-object-detection-model-using-text-visual-prompts-e48c16172706)。

**bbox 精度の含意**: **ラベルが言語化しづらい物体**はビジュアルプロンプトが効く一方、**本番監視**では「誰がプロンプトを供給するか」が運用設計。

### 4.8 Rex-Omni（座標をトークン化する MLLM、幾何 RL）

- **IDEA-Research** [Rex-Omni GitHub](https://github.com/IDEA-Research/Rex-Omni)、プロジェクトページ [rex-omni.github.io](https://rex-omni.github.io/)、論文 [2510.12798](https://arxiv.org/abs/2510.12798)（HTML: [2510.12798v1](https://arxiv.org/html/2510.12798v1)）。  
- 典型的な主張: **検出・OCR・GUI grounding 等を next prediction に統一**し、**幾何意識の RL** で重複や box 品質を改善、など — 原論文の Ablation を参照。

**bbox 精度の含意**: **フレームワークの魅力は「統一インターフェース」**。実務では **レイテンシ・並列性・失敗モード（座標桁・順序）**をプロファイルすること。

### 4.9 合意・マルチモデル推論（精度安定化の別枠）

- **複数 LLM／VLM の合意**で box を統合するサーベイが 2025 年に増えている（例: MDPI [Multiple Large AI Models’ Consensus for Object Detection](https://www.mdpi.com/2076-3417/15/24/12961)、Preprints [202511.0879](https://www.preprints.org/manuscript/202511.0879/v1)）。  
- **コストと遅延は増える**が、**高品質 pseudo-label 生成**や **監査用途**では検討枠に入る。

---

## 5. Fine-tuning（ファインチューニング）— 精度向上の見込みと落とし穴

### 5.1 期待してよいこと（経験則）

| 状況 | FT の効きやすさ | 代表的な手法 |
|------|------------------|--------------|
| ドメイン差が大きい（衛星、医療、図面、赤外） | **高** — baseline を大きく上げることが多い | フル FT / LoRA / 部分層解凍；データは COCO 形式が通りやすい |
| クラス名がニッチ・属語が多い | **高** — 言語条件・class embedding が追従 | phrase / caption と box のペア学習 |
| ゼロショットで「見つける」はできるが **位置がズレる** | **中〜高** — 回帰ヘッドがデータに慣れる | longer schedule + 強めの幾何損失；小物体は解像度も上げる |
| 本番は **latency と mAP の両立** | **要別モデル** — VLM 単体より **蒸留・専用 detector** が現実解になりやすい | 教師: 強い VLM / Grounding DINO、生徒: YOLO系・RF-DETR 等 |

### 5.2 警戒すべきこと

1. **未見クエリ・未見クラス**への汎化落ち（OWLv2 の fine-tune trade-offの系譜）。  
2. **学習データのラベルノイズ** — FT はノイズにもフィットする。  
3. **評価プロトコルの取り違え** — open-vocabulary mAP と closed-set mAP を混ぜない。  
4. **生成型モデル**は **座標フォーマット逸脱**（トークン化・桁）による **後処理エラー**。

### 5.3 実装リソース（コミュニティ／ベンダー）

- LearnOpenCV: [Fine-Tuning Grounding DINO](https://learnopencv.com/fine-tuning-grounding-dino/)  
- NVIDIA TAO: [Grounding DINO](https://docs.nvidia.com/tao/tao-toolkit/text/cv_finetuning/pytorch/object_detection/grounding_dino.html)  
- Roboflow: [Fine-tune Florence-2 for Object Detection](https://blog.roboflow.com/fine-tune-florence-2-object-detection/)  
- GitHub フォーク群（例: `GroundingDINO_Fix`、`Groundingdino-Finetuning`） — **ライセンス・メンテ状況を確認**して採用

### 5.4 Qwen2.5-VL / **Qwen3-VL** / **Qwen3.5** の追加学習（継続学習・ドメイン適応）の可能性

**結論から**: **座標付きの SFT（教師あり微調整）や LoRA は、ドメイン語彙・プロンプト形式・出力 JSON の安定化に効く**一方、**ゼロショット汎化の維持・幻覚ゼロ**までは期待しにくい。検出専用ヘッドが無いため、**「mAP が何ポイント上がる」はデータと評価プロトコルに強く依存**し、論文・ブログの転記だけでは再現保証がない。

#### 5.4.1 期待できること（追加学習でやりがちなこと）

| 目的 | 追加学習の効きやすさ | メモ |
|------|----------------------|------|
| **自社ドメインの呼び方**（部品コード、現場スラング）で **同じ物体を安定して指す** | 高 | instruction + 画像 + **期待する bbox / polygon 文字列** を JSONL で大量に揃える |
| **出力スキーマ固定**（例: 常に `{"bbox_2d": [x1,y1,x2,y2]}`） | 高 | 形式エラー削減 = 後処理が楽になり **実効 mAP が上がる**ことは多い |
| **動画・マルチ画像**での **時間指定・フレーム参照**の安定化 | 中〜高（世代依存） | Qwen3-VL / 3.5 は長文・動画入力が売り。**ラベルにタイムスタンプやフレーム番号**を含めると効く可能性 |
| **極小物体の bbox が常にズレる**を、専用データで詰める | 中 | **画像解像度・タイル分割・プロンプトで「原画像基準で答えよ」**と明示。それでも足りなければ **Grounding DINO 側の FT**と役割分担した方が早いことが多い |

#### 5.4.2 手法の選択（実務でよく使うレンジ）

- **LoRA / QLoRA（PEFT）**: メモリ効率が良い。**vision encoder を凍結し、言語側アテンション・MLP にだけ LoRA**という運用例がコミュニティに多い（過学習しにくい一方、**幾何だけ大きく変えたい**ときは足りないことも）。  
- **フルパラメータ FT**: データが十分・GPU が潤沢な組向け。Qwen3-VL の **30B-A3B MoE** 等は **8×H100 級**の話が Issue に出やすい。  
- **RL / GRPO（座標や IoU を報酬に）**: Rex-Omni など **検出をトークン予測に落とした系**では論文化されている。Qwen 公式で一般公開されているかは **モデル世代ごとに要確認** — 研究再現とプロダクションは別。

#### 5.4.3 公式・準公式に近いトレーニングスタック（2025〜2026）

- **Hugging Face `transformers`**: Qwen3-VL は **`Qwen3VLForConditionalGeneration`** と **`AutoProcessor`** でロードする例がモデルカードに記載。**`transformers` の互換版**（モデルカードが要求する **main / 4.57+** 等）は毎回確認。  
- **ms-swift（ModelScope）**: [Qwen3-VL Best Practices](https://swift.readthedocs.io/en/latest/BestPractices/Qwen3-VL-Best-Practice.html) に **依存パッケージ版・動画デコーダ（`torchcodec` 推奨等）・学習コマンド**がまとまっている。 **Qwen3-VL の FT 議論**は [Issue #6207](https://github.com/modelscope/ms-swift/issues/6207) などに具体設定が出る。  
- **LLaMA-Factory**: Qwen3-VL-30B-A3B の FT が遅い・設定がシビア、といった **実戦スレ**（例: [hiyouga/LLaMA-Factory#9303](https://github.com/hiyouga/LLaMA-Factory/issues/9303)）がある。  
- **Qwen2.5-VL 向けブログ・コミュニティ**: Roboflow [Fine-Tune Qwen2.5-VL with a Custom Dataset](https://blog.roboflow.com/fine-tune-qwen-2-5/)、F22 Labs [Fine-tuning Qwen2.5 VL](https://f22labs.com/blogs/complete-guide-to-fine-tuning-qwen2-5-vl-model)、コミュニティ実装（例: [donvink/Qwen2.5-VL-Finetune](https://github.com/donvink/qwen2.5-vl-finetune)）。

#### 5.4.4 Qwen3.5 固有の注意（2026 時点の整理）

- HF モデルカードでは **画像・動画入力**と **Thinking モード**、**vLLM / SGLang** 起動例、**超長コンテキスト用 RoPE オーバーライド**まで一括で説明されている（例: [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B)）。  
- **追加学習の手順は Qwen3-VL と流用できる部分と、チャットテンプレート・特殊トークンだけ変わる部分**が混ざる。**「3.5 用に更新された swift / LLaMA-Factory のドキュメント」**を優先し、古い Qwen2.5 手順のコピペは非推奨。  
- **エージェント・ツール呼び出し**とセットで使う設計（モデルカード内の Qwen-Agent 例）では、**bbox は「モデルが直接描く」のではなく「コードや外部 detector が返す」**という **§2 の系統 D** になりやすい — **役割設計を先に固定**すること。

---

## 6. サーベイ論文・広い地図（2025）

| 資料 | 概要 | リンク |
|------|------|--------|
| **Object Detection with Multimodal Large Vision-Language Models: An In-depth Review** | LVLMs が検出に与える影響を体系的に整理。Information Fusion 掲載扱い／arXiv [2508.19294](https://arxiv.org/abs/2508.19294) | 大枠の引用に便利 |
| **Vision Language Models: A Survey of 26K Papers (CVPR, ICLR, NeurIPS 2023–2025)** | 文献規模の広い VLM サーベイ [2510.09586](https://arxiv.org/abs/2510.09586) | 「どこが盛り上がっているか」の俯瞰 |
| **Multiple LLM Consensus for Object Detection — A Survey** | 合意推論の整理（例: [Preprints 202511.0879](https://www.preprints.org/manuscript/202511.0879/v1)、[MDPI Applied Sciences](https://www.mdpi.com/2076-3417/15/24/12961)） | インフラ負荷と精度の trade-off 理解 |

---

## 7. 「実際のプロ」思考（スタートアップ〜エンプラでよくある割り切り）

以下は **規範ではなく頻出パターン**の要約です。

1. **KPI が mAP か latencies か**  
   - **厳密数値＋SLO** が最優先なら、まず **専用 detector + 十分なラベル**。VLM は補助。  
   - **クラスが増え続け、ラベルコストが支配的**なら、**OVD / grounding を前工程**にして、最終的に **student を小型 detector に蒸留**。

2. **VLM を “ラベラー” にする**  
   - [05_applications_and_case_studies.md](./05_applications_and_case_studies.md) の流儀どおり、**高精度ラフラベル → human review** が現実的。合意推論・HalLoc 系の文脈は **ラベル品質管理**に接続できる。

3. **Roboflow 型の「ファインチューン前提アーキテクチャ」**  
   - [RF-DETR](https://github.com/roboflow/rf-detr) は **純 VLM ではない**が、「**ベンダーが 2025 頃に推す線**」として **closed-set の fine-tune 最適化**を強く打ち出している（blog: [Train and Deploy RF-DETR](https://blog.roboflow.com/train-deploy-rf-detr)）。  
   - **「開放語彙でプロトタイプ、固定語彙で本番」**の二段ロケットと併せて読むと現実的。

4. **ベンチマークカードに踊らない**  
   - COCO / LVIS の数字は **プロトコル依存**。ドメイン外では **必ず社内 val**。tiny object では **slice / multi-scale** が VLM より効くことも多い（[07](./07_architectural_drawing_symbol_detection.md)、[04](./04_training_playbook.md) と接続）。

---

## 8. 実務チェックリスト（bbox 品質）

- [ ] 系統 A/B/C/D のどれで勝負しているか、チームで言葉を統一したか  
- [ ] **同一画像に対する IoU 分布**（クラス別）を Baseline detector と比較したか  
- [ ] **プロンプト複数**で bbox がどれだけ動くか（感度分析）  
- [ ] FT 後に **未見クエリ**をスポットチェックしたか（OWLv2 系の trade-off）  
- [ ] 生成型なら **座標トークン→パース→clip** のユニットテスト  
- [ ] 本番は **NMS / WBF / 閾値**をどうするか（OVD でも後処理は効く）  
- [ ] **幻覚率**を別メトリクスで見るか（HalLoc / GroundSight 系の発想）

---

## 9. 参考文献・リンク集（随時更新用）

### サーベイ・総説

- Sapkota & Karkee, *Object Detection with Multimodal Large Vision-Language Models: An In-depth Review*, arXiv [2508.19294](https://arxiv.org/abs/2508.19294)  
- *Vision Language Models: A Survey of 26K Papers*, arXiv [2510.09586](https://arxiv.org/abs/2510.09586)

### 幻覚・接地・品質

- Park et al., *HalLoc*, CVPR 2025 Open Access [ページ](https://openaccess.thecvf.com/content/CVPR2025/html/Park_HalLoc_Token-level_Localization_of_Hallucinations_for_Vision_Language_Models_CVPR_2025_paper.html), arXiv [2506.10286](https://arxiv.org/abs/2506.10286)  
- *GroundSight*（接地と de-hallucination）, arXiv [2509.25669](https://arxiv.org/abs/2509.25669)

### モデル・手法（一次）

- Grounding DINO（原著・派生実装多数）— FT: [LearnOpenCV](https://learnopencv.com/fine-tuning-grounding-dino/), [TAO](https://docs.nvidia.com/tao/tao-toolkit/text/cv_finetuning/pytorch/object_detection/grounding_dino.html)  
- MM-Grounding-DINO, arXiv [2401.02361](https://arxiv.org/abs/2401.02361), HF [docs](https://huggingface.co/docs/transformers/en/model_doc/mm-grounding-dino)  
- DINO-X, arXiv [2411.14347](https://arxiv.org/abs/2411.14347), [GitHub API](https://github.com/IDEA-Research/DINO-X-API)  
- OWLv2 / Scaling OVD, NeurIPS [2023 paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/e6d58fc68c0f3c36ae6e0e64478a69c0-Abstract-Conference.html), [HF OWLv2](https://huggingface.co/docs/transformers/model_doc/owlv2)  
- Florence-2, Roboflow [blog](https://blog.roboflow.com/florence-2/), FT [blog](https://blog.roboflow.com/fine-tune-florence-2-object-detection/), arXiv FT 例 [2503.04918](https://arxiv.org/abs/2503.04918)  
- Qwen2.5-VL, arXiv [2502.13923](https://arxiv.org/abs/2502.13923)  
- Qwen3-VL, arXiv [2511.21631](https://arxiv.org/abs/2511.21631), [GitHub](https://github.com/QwenLM/Qwen3-VL), HF [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct), `transformers` [model_doc/qwen3_vl](https://huggingface.co/docs/transformers/model_doc/qwen3_vl)  
- Qwen3.5, [GitHub QwenLM/Qwen3.5](https://github.com/QwenLM/Qwen3.5), HF [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B), 紹介 *Towards Native Multimodal Agents*（モデルカード引用: [qwen.ai/blog](https://qwen.ai/blog?id=qwen3.5)）  
- ms-swift Qwen3-VL: [Best Practices](https://swift.readthedocs.io/en/latest/BestPractices/Qwen3-VL-Best-Practice.html), [Issue #6207](https://github.com/modelscope/ms-swift/issues/6207)  
- LLaMA-Factory: [Issue #9303](https://github.com/hiyouga/LLaMA-Factory/issues/9303)（Qwen3-VL-30B-A3B）  
- Roboflow: [Fine-Tune Qwen2.5-VL](https://blog.roboflow.com/fine-tune-qwen-2-5/)  
- InternVL3, arXiv [2504.10479](https://arxiv.org/abs/2504.10479), [docs](https://internvl.readthedocs.io/en/latest/internvl3.0/introduction.html)  
- GLIP, [microsoft/GLIP](https://github.com/microsoft/GLIP)  
- T-Rex2, arXiv [2403.14610](https://arxiv.org/abs/2403.14610), [GitHub](https://github.com/IDEA-Research/T-Rex)  
- Rex-Omni, arXiv [2510.12798](https://arxiv.org/abs/2510.12798), [GitHub](https://github.com/IDEA-Research/Rex-Omni), [サイト](https://rex-omni.github.io/)

### 実務・ベンダー・コミュニティ

- RF-DETR, [GitHub roboflow/rf-detr](https://github.com/roboflow/rf-detr), [学習ドキュメント](https://roboflow.github.io/rf-detr/learn/train/)  
- PyImageSearch, Qwen grounding 記事（2025）: [リンク](https://pyimagesearch.com/2025/06/09/object-detection-and-visual-grounding-with-qwen-2-5)

---

## 10. 本ドキュメントの限界

- **商用 API・非公開モデル**（各クラウドの最新版）の挙動は載せきれない。**NDA 下の比較表**が最強。  
- arXiv は **未査読**が混じる。採択論文・ジャーナル最終版を優先すること。  
- 数値ベンチマークは **省略**が多い — 必要なら論文 Table と **同一条件再現**で追う。

---

*次の更新候補: Rex-Omni / DINO-X 系の **長期再現実験**、**合意推論のコストモデル**、**cvpr/iccv 2026** のオーラル採択が出揃った段階での差し替え。*
