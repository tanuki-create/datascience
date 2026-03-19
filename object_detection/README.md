# 画像検知 / Object Detection ガイド

このディレクトリは、画像検知モデルの基礎から実務導入までを、複数の解説ファイルに分けて体系化した学習ガイドです。

本ガイドでは、依頼文中の `Deimv2` は文脈上 `DINOv2` を指すものとして扱い、YOLO 系、DETR / DINO 系、DINOv2 のような自己教師あり事前学習バックボーン活用まで含めて整理しています。

## 最新アップデート方針

このガイドは、2026-03-18 時点で確認できる一次情報に合わせて、次の観点を強化しています。

- 学術動向:
  - DINO による end-to-end DETR の実用化
  - RT-DETRv2 による real-time DETR の改善
  - YOLOv10 による NMS-free real-time 検出の整理
  - Grounding DINO / YOLO-World による open-vocabulary detection
  - DINOv2 による視覚 foundation backbone の実務転用
- コミュニティ実践知:
  - Ultralytics の pretrained-first な学習導線
  - MMDetection の config ベース実験管理と auto-scale LR
  - RT-DETR 公式実装での custom data、deployment、small object sliced inference の実践知

重要なのは、研究の最新をそのまま本番に入れることではありません。研究の進展を踏まえつつ、どこが本番で使える知見で、どこが探索段階かを分けて扱うことです。

## ドキュメント構成

1. [01_foundations.md](./01_foundations.md)
   - 物体検出とは何か
   - 分類、セグメンテーションとの差
   - 代表モデル系統、評価指標、失敗パターン
   - 学習パイプラインの全体像
   - 2024-2026 の研究潮流が基礎設計に何を変えたか

2. [02_terms_and_metrics.md](./02_terms_and_metrics.md)
   - bbox、IoU、NMS、mAP などの頻出用語
   - 学習やデバッグでの実践的な読み替え
   - 指標の見方と落とし穴
   - open-vocabulary や NMS-free 系で増えた新語彙

3. [03_model_families_and_mechanisms.md](./03_model_families_and_mechanisms.md)
   - R-CNN 系、SSD / RetinaNet、YOLO 系
   - DETR 系、DINO 系
   - DINOv2 のような自己教師ありバックボーンをどう使うか
   - RT-DETRv2、YOLOv10、Grounding DINO、YOLO-World の位置づけ

4. [04_training_playbook.md](./04_training_playbook.md)
   - データ収集、アノテーション品質、分割設計
   - 学習率、batch size、image size、augmentation
   - 小物体対策、長尾対策、実験管理、推論最適化
   - YOLO 系と DINOv2 活用時の具体的な学習設定の考え方
   - open-vocabulary を使ったデータ立ち上げ、RT-DETRv2 系の bag-of-freebies 実践

5. [05_applications_and_case_studies.md](./05_applications_and_case_studies.md)
   - 産業別の応用例
   - PoC から本番展開までの進め方
   - ROI、human-in-the-loop、データフライホイール
   - 現場で起きる故障モードと運用上の罠
   - promptable detector や foundation model をどう現場に落とすか

6. [06_professional_curriculum.md](./06_professional_curriculum.md)
   - プロフェッショナル育成のための学習ロードマップ
   - 到達目標、演習課題、レビュー観点
   - キャップストーン設計と評価ルーブリック

7. [07_architectural_drawing_symbol_detection.md](./07_architectural_drawing_symbol_detection.md)
   - 建築図面・設備図の細かい記号検出
   - tile / sliced inference 中心の実務設計
   - OCR、vector parsing、rule engine を含む本番パイプライン

8. [08_end_to_end_training_workflow.md](./08_end_to_end_training_workflow.md)
   - データ作成から学習、評価、運用までの実務手順
   - 実際に便利なツールと使い分け
   - プロの視点での細かい効率化と運用の勘所

9. [09_kaggle_leonardo_airborne_gold_strategy.md](./09_kaggle_leonardo_airborne_gold_strategy.md)
   - Kaggle Leonardo（機載・可視＋IR・VOC mAP@0.5・Code Competition）向けゴールド級攻略
   - Leaderboard と Efficiency Prize の二正面設計、CV・学習・推論・提出バグ防止

## このガイドの特徴

- 研究論文の紹介ではなく、現場で使える判断軸に寄せている
- 各ファイルに「5つの中核的なメンタルモデル」を入れている
- 各ファイルに、専門家の間で割れる論点と双方の最強主張を入れている
- モデルだけでなく、データ、評価、運用、ROI まで一貫して扱っている
- 学習者が読むだけで終わらないよう、演習、チェックリスト、レビュー観点を入れている
- 2024-2026 の主要論文と公式実装の差分が見えるようにしている
- 「SOTA だから採用」ではなく、「制約条件に対して何が有効か」で選ぶ訓練を重視している

## 対象読者

- 画像検知を基礎から実務レベルまで体系的に学びたいデータサイエンティスト
- 画像系の案件に入る前に、設計判断の型を身につけたい機械学習エンジニア
- PoC 止まりではなく、導入から運用まで責任を持てる人材を育てたいリードやマネージャ

## 育成目標

このガイド全体の到達目標は、次の 5 つです。

1. 問題設定をモデル選定の前に切れること
2. データセット、ラベル、評価設計の欠陥を早期に見抜けること
3. YOLO 系、DETR 系、DINOv2 系の選定理由を説明できること
4. 学習失敗を数値と画像の両方から診断できること
5. 本番導入で必要な ROI、監視、再学習、責任分界まで設計できること

## 読み方

- 初学者: `01` -> `02` -> `03` -> `04` -> `05`
- 実装者: `03` と `04` を先に読み、必要に応じて `02` を辞書として使う
- 導入担当者: `01` で前提をそろえた後、`05` を中心に読む
- 育成担当者: `06` を先に読み、演習とレビューの進め方を決めてから全体を使う

## 推奨カリキュラム

### Phase 1: 基礎理解

- `01` で問題設定を理解する
- `02` で用語と指標を言語化できるようにする
- 成果物: 用語説明メモ、mAP と業務指標の違いを説明する短いレポート

### Phase 2: モデル理解

- `03` でモデル系統ごとの差分を整理する
- モデル選定理由を、精度ではなく制約条件から説明する
- 成果物: 3種類のユースケースに対するモデル選定メモ

### Phase 3: 学習実務

- `04` を使い、ベースライン構築、実験管理、エラー解析を回す
- 少なくとも 1 つの公開データセットか社内データで再現実験を行う
- 成果物: 実験台帳、失敗例の可視化、再学習計画

### Phase 4: 事業実装

- `05` で PoC から本番までの設計を学ぶ
- ROI、human-in-the-loop、監視体制、例外処理を設計する
- 成果物: 導入提案書、運用監視の設計図、障害時対応フロー

### Phase 5: プロフェッショナル化

- `06` を使い、キャップストーン課題とレビューを行う
- 技術だけでなく、説明責任、意思決定、他部署連携まで含めて訓練する
- 成果物: 最終レポート、経営向け要約、技術レビュー記録

## 重要な前提

画像検知は、モデル選定だけで成果が決まる分野ではありません。実務では、次の順で差が出ます。

1. 問題設定とラベル定義
2. データ分布とアノテーション品質
3. 学習設定と失敗解析
4. 推論最適化と運用導線

したがって、このディレクトリ全体も「モデル一覧」ではなく、「設計判断の地図」として使う前提で作っています。

## どう評価するか

学習者を評価するときは、単に用語を暗記しているかではなく、次を見ます。

- なぜそのデータ分割が危険かを説明できるか
- どのエラーが支配的かを、画像付きで説明できるか
- モデルを変える前に、データやラベルの欠陥を疑えるか
- 本番運用で何を監視し、何を再学習対象にするかを設計できるか
- 精度改善が事業価値に変わる条件を説明できるか

## 主要な一次情報

- DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection
- DINOv2: Learning Robust Visual Features without Supervision
- RT-DETRv2: Improved Baseline with Bag-of-Freebies for Real-Time Detection Transformer
- YOLOv10: Real-Time End-to-End Object Detection
- Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection
- YOLO-World: Real-Time Open-Vocabulary Object Detection
- Ultralytics YOLO Docs
- MMDetection Docs
- RT-DETR Official Repository
