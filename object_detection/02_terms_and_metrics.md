# 物体検出の用語と評価指標

このファイルは、物体検出の学習や実務で頻出する用語を、なるべく実戦的な意味で整理した辞書です。理論の厳密さよりも、設計やデバッグでどう使うかを重視します。

## 用語辞典

### bbox

物体を囲う矩形領域です。通常は `x, y, w, h` または `x1, y1, x2, y2` で表します。アノテーションの揺れがそのまま学習上限になるので、最重要の基礎データです。

### IoU

Intersection over Union の略で、予測 bbox と正解 bbox の重なりの指標です。検出では、正解判定、NMS、評価の中心になります。

### confidence

モデルがその検出をどれだけ信じているかを表すスコアです。高い confidence が必ずしも正しいとは限らず、校正不良が起きます。

### precision / recall

precision は「当たった予測の割合」、recall は「見つけるべき対象をどれだけ拾えたか」です。前者は誤検出、後者は見逃しに敏感です。

### mAP

mean Average Precision の略で、クラスごとの AP を平均したものです。検出研究の標準指標ですが、運用目的と必ずしも一致しません。

### AP50 / AP75

IoU しきい値を 0.50 や 0.75 に固定した AP です。AP50 は「見つけたか」に寄り、AP75 は「位置が十分正確か」に寄ります。両者の差を見ると、見つける力と位置精度のどちらが弱いか見えます。

### TP / FP / FN

True Positive、False Positive、False Negative です。検出では、何が FP で何が FN かを画像で確認しないと、改善方針を誤りやすいです。

### PR curve

precision と recall の関係を閾値ごとに見た曲線です。単一の mAP より、運用上どの閾値帯が安定しているかを見るのに役立ちます。

### one-to-one matching

DETR 系で使われる考え方で、予測と正解を 1 対 1 で対応づけます。NMS に頼りにくい end-to-end 検出の中核です。dense detector の「大量候補から削る」発想と対比して理解するとよいです。

### NMS-free

後処理としての NMS を不要にする、または大きく弱める設計です。近年の YOLOv10 や DETR 系で重要なキーワードです。理論的には美しいですが、実務では export、latency、threshold 制御まで含めて評価します。

### NMS

Non-Maximum Suppression の略で、重複する検出候補から代表だけを残す処理です。密集シーンでは、強すぎる NMS が真の検出まで消すことがあります。

### anchor

候補 bbox のテンプレートです。YOLO 以前の系統で重要でしたが、現在も一部の検出器では使われます。サイズやアスペクト比の事前知識を埋め込みます。

### stride

特徴マップ上の 1 ピクセルが入力画像上で何ピクセル分に対応するかを表します。stride が大きいほど高速ですが、小物体に不利です。

### feature pyramid

異なる解像度の特徴を組み合わせる構造です。小物体と大物体を同時に扱うために重要です。FPN 系が代表です。

### label assignment

どの予測位置をどの正解に対応づけるかのルールです。検出性能の大半を左右することがあり、学習の“隠れた主役”です。

### dual assignment

近年の NMS-free YOLO で出てくる概念で、学習安定化や性能維持のために複数の assignment を併用する考え方です。dense supervision と end-to-end 推論の折衷を理解する鍵になります。

### positive / negative sample

学習時に正例として扱う予測と、負例として扱う予測です。検出は負例が圧倒的に多いため、どこまでを正例にするかで収束挙動が変わります。

### augmentation

データ拡張です。flip, crop, scale, mosaic, mixup などがあり、汎化改善に効きますが、やりすぎるとラベル分布を壊します。

### hard negative

見た目が紛らわしいが正解ではない負例です。誤検出の主要因であり、難しい背景を学習するために重要です。

### long-tail

一部クラスにデータが偏り、少数クラスが極端に少ない状態です。現実データではほぼ常態で、評価の偏りも生みます。

### occlusion

遮蔽のことです。対象の一部が隠れている状態で、小物体や密集シーンと組み合わさると難度が上がります。

### domain shift

学習時と運用時の分布が変わることです。カメラ、照明、季節、解像度、撮影角度の変化が典型例です。

### calibration

confidence が確率としてどれだけ信頼できるかを表す性質です。運用で閾値制御をするなら、精度そのものと同じくらい重要です。

### GIoU / DIoU / CIoU

bbox 回帰で使う IoU 系損失です。単なる座標差よりも、重なりと位置関係を直接扱えるため、検出では実務上よく使われます。どの損失が効くかは物体サイズや形状分布にも依存します。

### OOD

Out-of-Distribution の略で、学習時に見ていない分布の入力です。検出では、照明、カメラ、地域、季節、製品切り替えが OOD の典型原因です。

### TTA

Test Time Augmentation の略で、推論時に複数の変換画像で推論して結果を統合する手法です。精度改善はあり得ますが、遅延と複雑性が増えます。

### open-vocabulary detection

固定ラベル集合ではなく、テキストやクエリ語に応じて任意概念を検出する枠組みです。Grounding DINO や YOLO-World が代表です。運用では、最終推論器というより、データ探索や long-tail 発見に効きます。

### grounded detection

単なるカテゴリ名だけでなく、属性や指示表現まで含めて対象を検出することです。例えば「赤い箱」「右端のフォークリフト」のような指定が入ります。open-vocabulary detection より運用条件が複雑です。

### vision foundation model

広い視覚タスクへ転移可能な大規模事前学習モデルです。検出文脈では、DINOv2 のような backbone が代表例です。重要なのは、foundation model 自体が detector ではなく、検出器設計の前段を強くすることです。

### bag-of-freebies

推論コストを大きく増やさずに性能を改善する学習上の工夫群です。RT-DETRv2 文脈では dynamic augmentation や scale-adaptive hyperparameter がこれに当たります。

### sliced inference

高解像度画像をタイル状に分割して推論し、小物体 recall を上げる実践手法です。航空画像、監視、製造で特に重要です。小物体が多い案件では、モデル変更より先にこれを検討する価値があります。

### latency / throughput

latency は 1 回の推論にかかる時間、throughput は単位時間あたりの処理枚数です。リアルタイム用途では latency、バッチ処理では throughput が重要になります。

## 評価指標の見方

- IoU threshold を上げると、位置精度の厳しさが増す
- mAP は全体性能の比較に便利だが、誤検出の種類までは見えにくい
- precision と recall のトレードオフは、閾値で大きく変わる
- FPS だけでなく、バッチサイズ、入力解像度、CPU/GPU 依存も確認する

実務では、単一の数字で判断しない方がよいです。mAP が高くても、特定クラスの見逃しや過検出が致命的なら失敗です。

## 指標を読む順番

強い実務者は、数字を次の順に見ます。

1. クラス別 recall
2. クラス別 precision
3. AP50 と AP75 の差
4. 物体サイズ別 AP
5. confidence 分布と calibration
6. latency / throughput

この順番にすると、見逃し、誤検知、位置ずれ、速度制約を混同しにくくなります。

## ダッシュボードで必ず見るべきもの

- クラス別 AP / recall / precision
- size 別 AP
- confusion の多いクラス対
- FP の代表例画像
- FN の代表例画像
- confidence のヒストグラム
- 学習データと本番データの分布差

open-vocabulary や promptable detector を使う場合は、これに加えて次も見るべきです。

- プロンプト表現の揺れに対する頑健性
- 未知クラスでの hallucination 的過検出
- prompt 変更時の confidence 変動
- closed-set student へ蒸留した後の性能差

## この分野の専門家がみな共有している、5つの中核的なメンタルモデル

- bbox は出力形式ではなく、問題定義そのものである
- IoU と NMS は「どれを正解とみなすか」を決める運用ルールである
- confidence は未校正のまま使うと危険である
- 長尾分布と遮蔽は例外ではなく通常ケースである
- 速度指標は精度指標と独立ではなく、設計全体の制約条件である

## この分野の専門家たちが根本的に意見を異にしている点

### 1. anchor を使うべきか

立場A: anchor は有効な事前知識であり、サイズ分布をうまく離散化できる。特にデータが限られる場面で強い、というのが最も強い主張です。

立場B: anchor は設計自由度を増やすが、ラベル割当を複雑にする。anchor-free の方が単純で保守しやすい、というのが最も強い主張です。

### 2. 評価は mAP 中心でよいか、用途別指標を優先すべきか

立場A: mAP は比較可能性が高く、研究と実装の共通言語として優れている。ベンチマークの標準があることが最大の強みです。

立場B: 実運用の損失関数は別にあるので、クラス別 recall や誤検出率、遅延まで見なければ意味がない。意思決定に直結するのが最大の強みです。

### 3. confidence は確率として扱ってよいか

立場A: 閾値運用が目的なら、confidence をそのまま実用に乗せても十分役立つ。単純さと速さが最大の強みです。

立場B: そのままでは校正されていないことが多く、確率として解釈すると危険です。温度スケーリングなどを含めて扱うべき、というのが最も強い主張です。

## 実務での読み替え

- bbox が荒いなら、まずアノテーション規約を疑う
- 小物体が弱いなら、stride と image size を疑う
- 過検出が多いなら、confidence 閾値と calibration を疑う
- 密集で落ちるなら、NMS と label assignment を疑う
- 本番で崩れるなら、domain shift と augmentation の不足を疑う

## 学習とデバッグの要点

1. まず train / val の評価差を見る
2. 次にクラス別の precision / recall を見る
3. 最後に失敗例を hard negative と誤ラベルに分ける
4. その上で augmentation、解像度、閾値を調整する

用語を覚えるだけでは足りません。検出では、各用語がそのまま設計パラメータと失敗原因に直結します。

## 2024-2026 の実務で特に重要になった語彙

- NMS-free:
  - 理想形の名前ではなく、deployment 制約とセットで評価すべき概念
- open-vocabulary detection:
  - 「最終製品の detector」ではなく「annotation bootstrap の道具」として使う場面が増えている
- foundation backbone:
  - pretraining の強さを示す語であり、 detector 全体の完成度を保証する語ではない
- bag-of-freebies:
  - architecture の派手さより、再現性ある training recipe が大きく効くことを示す
- sliced inference:
  - 小物体案件では、モデル変更以上に効くことがある運用レベルの工夫

## 読むべき一次情報

- DINO
- RT-DETRv2
- YOLOv10
- Grounding DINO
- YOLO-World
- DINOv2

## 演習課題

1. AP50 は高いが AP75 が低い場合に疑うべきことを列挙する
2. recall は高いが precision が低いモデルを、どんな業務なら許容できるか説明する
3. calibration が悪い検出器を、そのまま閾値運用する危険性を説明する
4. OOD と hard negative を混同すると、なぜ改善が止まるのかを説明する

## セルフチェック

- IoU、AP、mAP の違いを、式ではなく意思決定の違いとして説明できるか
- latency と throughput のどちらを優先すべきか、案件別に答えられるか
- anchor、stride、feature pyramid が小物体検出にどう関係するか説明できるか
- PR curve から、どの閾値帯で運用すべきか議論できるか
