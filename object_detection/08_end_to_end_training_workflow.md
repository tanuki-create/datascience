# 物体検出モデル学習の実務ワークフロー

この文書は、物体検出モデルを実際に現場で学習させるときの手順を、データ作成から運用監視まで一気通貫で整理したガイドです。目的は「とりあえず学習を回すこと」ではなく、再現可能で、改善可能で、運用できる検出器を作ることです。

## まず結論

実務では、次の順序で進めると失敗しにくいです。

1. 問題定義
2. 生データ収集
3. ラベル設計
4. アノテーション
5. データ検査と分割
6. データ版管理
7. ベースライン学習
8. エラー解析
9. 改善サイクル
10. export / deploy
11. 監視と再学習

プロの現場で差が出るのは、モデルより前の `4-6` と、モデルより後の `9-11` です。

## 推奨ツールスタック

### 小規模チームの現実解

- アノテーション:
  - `CVAT` または `Label Studio`
- データ版管理:
  - `DVC`
- 学習:
  - `Ultralytics YOLO`
- 可視化 / エラー解析:
  - `FiftyOne`
- 実験管理:
  - `MLflow` または `Weights & Biases`
- 小物体対策:
  - `SAHI`
- augmentation:
  - `Albumentations`

### 中規模以上のチーム

- アノテーション:
  - `CVAT`
- ストレージ:
  - S3 / GCS / MinIO
- データ版管理:
  - `DVC`
- 学習:
  - `MMDetection` と `Ultralytics` を併用
- 可視化 / review:
  - `FiftyOne`
- 実験管理:
  - `MLflow` もしくは `Weights & Biases`
- 小物体・大画像:
  - `SAHI`

## 2026年時点の最新手法と工夫ポイント

2026年時点で実務に効く「新しさ」は、単に新しいモデル名を追うことではありません。特に重要なのは、次の 6 つです。

### 1. NMS-free / end-to-end detector が実用域に入った

2026年時点では、`YOLO26` のような NMS-free な real-time detector と、`RF-DETR` や `RT-DETR` 系の real-time transformer detector が、比較対象として普通に入ってきます。

- 使いどころ:
  - GPU 推論
  - cloud / server inference
  - NMS の重複整理で loss が大きい案件
- 実務上の注意:
  - 学習精度だけでなく export 後 latency を比較する
  - 既存 post-process と運用監視が流用できるか確認する
  - edge では依然として YOLO 系の成熟度が強い

現場の感覚では、「2026年は YOLO 一択ではなくなった」が正確です。ただし「常に transformer が勝つ」でもありません。GPU/cloud なら RF-DETR 系、edge や既存運用との親和性なら YOLO 系が依然強いです。

### 2. foundation model を学習前工程に入れるのが標準化した

`Grounding DINO` のような open-vocabulary detector や、promptable segmentation 系は、本番主系よりも `auto-label / pre-label / tail discovery` の道具として価値が高いです。

- 強い使い方:
  1. 少量手ラベル
  2. foundation model で pre-label
  3. 人手修正
  4. closed-set detector に distill / fine-tune
- 工夫ポイント:
  - prompt を ontology に固定する
  - pre-label のノイズ率を class ごとに測る
  - foundation model の誤りを reviewer guide に反映する

2026年のプロの運用では、「foundation model で全部解く」より「foundation model でデータ作成を速める」が主流です。

### 3. OBB が特殊用途ではなくなってきた

`Albumentations` でも OBB が公式に整理され、`Ultralytics` でも OBB task が普通に扱われるようになりました。航空画像、建築図面、回転記号、斜め撮像では OBB を最初から検討する価値があります。

- OBB を使うべき条件:
  - 細長い対象が多い
  - 回転が意味を持つ
  - HBB だと背景を取り込みすぎる
- 工夫ポイント:
  - annotation コストと gain を先に比較する
  - augmentation は OBB 対応で統一する
  - evaluation も OBB 前提に合わせる

### 4. object detection の改善は architecture より data engine で差が出る

2026年の強いチームは、モデル更新より `data engine` を整えています。

- 実際にやること:
  - hard negative mining
  - disagreement sampling
  - uncertainty sampling
  - production drift sampling
  - reviewer feedback の再学習反映

特に `FiftyOne` のような可視化ツールと、`DVC` の experiment queue を組み合わせると、改善サイクルを継続しやすいです。

### 5. compression は最後ではなく設計初期に入る

2026年は、edge を意識するなら quantization と distillation を最後の作業にしない方がよいです。

- 現実的な順序:
  1. deployment target を決める
  2. 使える precision を決める
  3. その制約で baseline を選ぶ
  4. 量子化後の劣化が大きければ distillation を検討する

工夫ポイント:

- teacher-student の蒸留を class imbalance の強いクラスに意識的に効かせる
- post-training quantization だけで足りないなら QAT / distillation へ進む
- export 前後で AP だけでなく class-wise recall を比較する

### 6. 学習系統を 1 本に固定しすぎない

2026年の実務では、次の 3 層構成がかなり強いです。

1. foundation model / promptable model:
   - pre-label と data bootstrap
2. production detector:
   - YOLO26 / YOLO11 / RF-DETR / RT-DETR 系
3. deployment optimizer:
   - ONNX / TensorRT / OpenVINO / quantized runtime

1 つのモデルで全部やろうとするより、役割ごとに分けた方が保守しやすくなります。

## 2026年の実務で効く細かな工夫

### 工夫 1: 最初から benchmark を 2 系統で取る

- object-level:
  - mAP
  - recall
  - precision
- system-level:
  - end-to-end latency
  - image/page あたり誤検知数
  - human correction rate

2026年は model API の速度より `pipeline latency` の方が意思決定に効きます。

### 工夫 2: pre-label を前提に reviewer workflow を設計する

- reviewer は全件見るのではなく、次を見る:
  - low confidence
  - class confusion
  - prompt ambiguity
  - rare class

これを最初から回すと annotation cost が大きく下がります。

### 工夫 3: experiment queue を使って探索を詰める

`DVC exp run --queue` と `dvc queue start` を使うと、同じコードベースで data version を固定したまま条件比較がしやすいです。

比較すべき優先順は次です。

1. resolution
2. split
3. threshold
4. augmentation
5. slicing
6. model family

### 工夫 4: RF-DETR 系では gradient checkpointing と logger を最初から入れる

RF-DETR の公式 docs でも、`gradient checkpointing`、`early stopping`、`TensorBoard / W&B / ClearML / MLflow` 連携が前提になっています。transformer 系はメモリと再現性の両方がボトルネックになりやすいので、最初から運用に入れるべきです。

### 工夫 5: YOLO26 系では edge 最適化まで含めて判断する

Ultralytics docs では `YOLO26` を end-to-end NMS-free inference と edge optimization を特徴として打ち出しています。つまり、2026年の YOLO 系は「学習で高精度」より「edge deployment ready」まで含めて評価するのが筋です。

### 工夫 6: OBB と slicing を建築図面・航空で最初から比較する

対象が小さく回転するなら、2026年は HBB 固定で始める理由が弱くなっています。

- 比較すべき組み合わせ:
  - HBB + full image
  - HBB + slicing
  - OBB + slicing

これを最初に比較する方が、あとで detector を何度も変えるより速いです。

## Step 1: 問題定義

最初に決めるべきなのはモデルではありません。

- 何を検知するのか
- 何を検知しないのか
- 誤検知と見逃しのどちらが高コストか
- 推論対象は静止画か動画か
- レイテンシ要件は何 ms か
- 最終出力は alert か、候補提示か、全自動処理か

### プロの視点

- 仕様書には必ず `non-target` を書く
- クラスの粒度は、業務フローで必要な粒度に合わせる
- 初期から `page/image level KPI` と `object level KPI` を分けて考える

## Step 2: 生データ収集

収集段階で失敗すると、後でどれだけ学習しても伸びません。

### やること

- 本番に近い条件でデータを集める
- hard negative を意識して集める
- 昼夜、季節、照明、解像度、カメラ違いを含める
- 例外ケースをわざと入れる

### 保存の実務

- raw は immutable に保存する
- 後処理済みデータは別ディレクトリにする
- 画像とメタデータを分離しない
- `source`, `camera_id`, `timestamp`, `site`, `version` を残す

### プロの視点

- 収集時点で `train 用` と `test 用` を混ぜない
- 同一動画や burst 撮影はリーク源になるので識別子を残す
- データが少ないときほど、代表性より failure mode の多様性を優先する

## Step 3: ラベル設計

アノテーション前に ontology を固定します。

### 決めること

- クラス一覧
- 属性
  - `occluded`
  - `truncated`
  - `difficult`
  - `source`
- bbox の描き方
  - visible only
  - full extent
- 重なりの扱い
- 小さすぎる対象の扱い

### プロの視点

- 初期の class は細かく切りすぎない
- 迷うクラスは coarse class で始める
- `annotate if visible > x%` のような基準を文章で固定する
- guide なしでラベルすると、あとで学習が壊れる

## Step 4: アノテーション

### おすすめツール

- `CVAT`
  - タスク管理、dataset export/import、automatic annotation が使いやすい
- `Label Studio`
  - 柔軟な labeling config と semi-automatic labeling に向く

### 実際の流れ

1. 100-300 枚で pilot annotation
2. ラベルガイドを修正
3. annotator training
4. 本格アノテーション
5. reviewer が spot check

### 効率化

- 既存モデルで pre-label
- class-wise shortkeys を使う
- frequent mistakes を annotator に毎週共有する
- 難例だけ senior reviewer に回す

### プロの視点

- 最初から全量をラベルしない
- pilot で guide を固めてから量産する
- annotator agreement を取る
- review サンプルをクラス別に固定比率で抜く

## Step 5: データ検査と分割

### 検査項目

- 空ラベル画像の比率
- クラス頻度
- size 分布
- aspect ratio 分布
- camera/site ごとの偏り
- ラベル欠損
- bbox の異常
  - 0 area
  - image outside
  - class mismatch

### 分割の原則

- `train/val/test` をランダムで切らない
- site / camera / video / day をまたがせない
- 同一現場の近接フレームは同一 split に置く

### おすすめツール

- `FiftyOne`
  - データ可視化、検出評価、mistake analysis に強い

### プロの視点

- split は固定して version 管理する
- `test` は最後まで触らない
- `val` を tuning 用、`test` を報告用に分ける

## Step 6: データ版管理

データが変わったのに run 名だけ変えて学習を続ける運用は破綻します。

### おすすめツール

- `DVC`
  - data versioning
  - pipeline 定義
  - stage 再現

### 管理すべきもの

- raw data version
- labeled data version
- split file
- class map
- training config
- evaluation script

### 推奨構成

```text
object_detection_project/
  data/
    raw/
    interim/
    processed/
  annotations/
    v001/
    v002/
  splits/
    split_v001.json
  configs/
    baseline_yolo.yaml
    baseline_mmdet.py
  experiments/
  models/
  reports/
```

### プロの視点

- `dataset version` と `label version` を分ける
- Git でコード、DVC でデータを管理する
- 実験結果に必ず data version を紐づける

## Step 7: ベースライン学習

最初のベースラインは、最強モデルではなく、再現しやすいモデルを使います。

### まず使うとよいもの

- `Ultralytics YOLO`
  - 早く baseline を作る
  - custom dataset の学習導線が短い
- `MMDetection`
  - 研究・比較・高度な config 管理
  - model zoo が豊富

### 典型的な進め方

1. pretrained model を使う
2. 標準解像度から始める
3. class-wise metrics を取る
4. error analysis を見る

### 例: YOLO 系

- `imgsz=640` か `960` から開始
- `epochs=100` 前後で baseline
- pretrained weights を使う
- batch は GPU に合わせる

### 例: MMDetection

- model zoo の安定 config をそのまま再現
- `auto_scale_lr` を batch size に合わせて確認
- config を commit する

### プロの視点

- 最初から augmentation を盛りすぎない
- small object なら解像度と slicing を先に比較する
- model change より label / split / data coverage を先に疑う

## Step 8: augmentation

### おすすめツール

- `Albumentations`
  - bbox 同期がしやすい
  - object detection / OBB に対応

### 基本方針

- 幾何変換
  - flip, scale, translate
- 見た目変換
  - blur, noise, jpeg compression, color jitter
- task-specific
  - copy-paste
  - mosaic

### プロの視点

- 記号や回転意味があるタスクでは回転 augmentation を安易に入れない
- `min_area`, `min_visibility` を設定して invalid bbox を防ぐ
- augment の前後で bbox の破綻を可視化する

## Step 9: 小物体・大画像対策

### おすすめツール

- `SAHI`
  - sliced inference / sliced prediction

### 有効なケース

- 建築図面
- 監視
- 航空画像
- 高解像度製造検査

### プロの視点

- model を変える前に slicing を比較する
- tile size と overlap を sweep する
- merge 後の duplicate error を別評価する

## Step 10: 実験管理

### おすすめツール

- `MLflow`
  - OSS で堅い
  - runs, params, metrics, artifacts を管理しやすい
- `Weights & Biases`
  - dashboard が強い
  - チーム比較がやりやすい

### 必ず記録するもの

- model name
- code commit hash
- data version
- split version
- hyperparameters
- metrics
- confusion examples
- checkpoint

### プロの視点

- 「良かった run」だけでなく、失敗 run も残す
- run 名に class や site を詰め込みすぎない
- tags と config を使う

## Step 11: エラー解析

精度を伸ばす最短経路です。

### おすすめツール

- `FiftyOne`
  - `evaluate_detections()`
  - 失敗例の可視化
  - subset analysis

### 見るべき失敗

- false positive
- false negative
- localization error
- class confusion
- small object only
- site / camera 別悪化

### プロの視点

- `mAP` の前に失敗画像を見る
- class ごとに `top 50` の bad case を固定 review する
- 改善策は必ず `data`, `label`, `model`, `threshold` のどれに効くかを分ける

## Step 12: semi-automatic labeling と active learning

現場では、全件手作業 annotation は非効率です。

### 効率化パターン

- CVAT の automatic annotation
- Label Studio の ML backend / OpenMMLab integration
- 既存 detector で pre-label
- uncertainty の高いサンプルだけ再ラベル

### 実務で強い流れ

1. 少量を手でラベル
2. baseline を学習
3. pre-label を生成
4. annotator が修正
5. hard cases だけ追加収集

### プロの視点

- pre-label は楽になるが、誤りのバイアスも注入する
- review 指標を固定して、pre-label 依存の誤りを監視する

## Step 13: export / deploy

### やること

- exporter を固定する
- ONNX / TensorRT / OpenVINO を比較する
- CPU と GPU の両方で latency を測る
- threshold を class-wise に調整する

### プロの視点

- 学習機の FPS と本番 FPS は違う
- batch inference と single inference を分けて測る
- NMS / post-process の時間を別に測る

## Step 14: 監視と再学習

### 監視項目

- class-wise detection count drift
- confidence drift
- false positive report rate
- human correction rate
- site / camera 別悪化

### 再学習トリガー

- 新規 site 追加
- class distribution change
- hardware / camera change
- label ontology change

### プロの視点

- 本番データを定期サンプリングして再ラベルする
- model release ごとに canary を作る
- rollback 手順を先に作る

## 実務で特に便利なツールの使い分け

### CVAT

- 大量アノテーション
- タスク分割
- export/import
- automatic annotation

### Label Studio

- 柔軟な labeling UI
- semi-automatic labeling
- custom workflow

### FiftyOne

- dataset inspection
- duplicate / outlier / mistake review
- detector failure の可視化

### DVC

- data versioning
- pipeline 再現
- チームでの共有

### MLflow / W&B

- experiments 管理
- run 比較
- artifact 管理

### Ultralytics

- baseline を素早く作る
- export まで短い

### MMDetection

- 比較実験
- config 管理
- model family を広く試す

### Albumentations

- bbox 同期 augmentation
- visibility / clipping 管理

### SAHI

- small object recall の底上げ
- large image inference

## プロがやる細かい効率化

- annotation task は class 単位ではなく scene 単位で分ける
- annotator 向けに bad example 集を作る
- dataset.yaml や class map を PR review 対象にする
- split ファイルを手編集しない
- run ごとに `top FP`, `top FN` を artifact 化する
- best model だけでなく `best per class threshold` を保存する
- export 済みモデルに対しても regression test を回す
- production issue は screenshot ではなく原画像で回収する

## 最小構成のおすすめ

とりあえず現場で回る最小構成は、次です。

1. `CVAT`
2. `DVC`
3. `Ultralytics YOLO`
4. `FiftyOne`
5. `MLflow`

これで

- ラベル
- データ版
- ベースライン
- エラー解析
- 実験管理

が一通り回せます。

## よくある失敗

- dataset version を残さない
- split を毎回変える
- test を tuning に使う
- mAP だけ見て deployment する
- pre-label の誤りを review しない
- site / camera 別評価をしない
- export 後の速度を測らない

## この分野の専門家がみな共有している、5つの中核的なメンタルモデル

1. 学習はコードではなく、データと運用も含めたシステムである
2. ベースラインは速く、改善は慎重に行うべきである
3. データ版管理なしの実験は、再現不能で価値が低い
4. エラー解析は評価の付属物ではなく、改善の本体である
5. デプロイと監視まで含めて初めて学習手順が完成する

## この分野の専門家たちが根本的に意見を異にしている点

### 1. まず YOLO 系で速く回すか、最初から柔軟な研究基盤へ行くか

立場A: まず YOLO 系で速く baseline を作るべき。改善ループが最も速いことが最大の強みです。

立場B: 最初から MMDetection のような柔軟基盤で進めるべき。比較実験と長期保守がしやすいことが最大の強みです。

### 2. 実験管理は SaaS を使うか、OSS で閉じるか

立場A: W&B のような SaaS を使うべき。可視化と共同作業の速度が最大の強みです。

立場B: MLflow を中心に OSS で閉じるべき。制御性と情報管理が最大の強みです。

### 3. pre-label を積極活用するか、手ラベル中心で行くか

立場A: pre-label を使うべき。立ち上がり速度と annotation 工数削減が最大の強みです。

立場B: 初期は手ラベル中心で行くべき。バイアス混入を避けやすいことが最大の強みです。

## 演習課題

1. 自分の案件で、`最小構成` と `中規模構成` のどちらを採るか理由付きで書く
2. train/val/test の split 基準を、camera / site / day 単位で設計する
3. baseline 学習後に見るべき failure 50 件の review 手順を書く
4. pre-label を使うときの品質管理ルールを 5 つ決める

## セルフチェック

- 自分の run に data version を必ず紐づけられているか
- 学習前に annotation guide が文章化されているか
- `best checkpoint` だけでなく `best threshold` を保存しているか
- export 後の本番想定 latency を測っているか
