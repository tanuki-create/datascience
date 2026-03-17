# 建築図面の細かい記号検出

この文書は、建築図面、設備図、施工図、配線図のような高解像度かつ高密度な図面に含まれる細かい記号を、物体検出としてどう扱うかを整理するための実務ガイドです。

通常の自然画像検出とは、前提が大きく異なります。建築図面では、対象が極端に小さい、背景が線分だらけ、クラス定義が規格と運用に依存する、ページ全体の解像度が高い、という特徴があります。したがって、ここでは「小物体検出」「ドキュメントAI」「図面理解」の交差点として考えます。

## まず押さえる前提

建築図面の記号検出は、単にドアや窓を見つける問題ではありません。実際には、次の 3 層に分かれます。

1. 記号を見つける
2. 記号の意味を決める
3. 記号同士や壁・寸法・文字との関係を解釈する

物体検出が直接解くのは主に 1 です。2 と 3 まで自動化したいなら、OCR、線分抽出、グラフ構築、ルールベース、場合によっては LLM/VLM を組み合わせる必要があります。

## 何を検知対象にするか

建築図面では、対象クラスを曖昧にするとすぐに破綻します。よくある対象は次の通りです。

- 建築:
  - ドア記号
  - 窓記号
  - 柱
  - 階段方向記号
  - 断面記号
  - 通り芯記号
- 設備:
  - コンセント
  - 照明
  - スイッチ
  - 給排水器具
  - ダクト、バルブ、配管記号
- 管理記号:
  - 寸法線端点
  - 注記引出線
  - 仕上げ記号
  - 部屋ラベル対応記号

現場では、「壁」「寸法線」「文字」のような巨大クラスを同じ detector に入れるより、細かい記号クラスと、それ以外の構造要素を別パイプラインに分けた方が安定しやすいです。

## なぜ難しいか

### 1. 記号が極端に小さい

図面全体では A1/A0 相当の高解像度でも、記号単体は数ピクセルから数十ピクセルしかないことがあります。通常の 640 や 1024 の単一入力へ縮小すると、記号情報がほぼ消えます。

### 2. 背景が「背景」ではない

自然画像と違い、壁線、寸法線、ハッチング、文字、グリッド線がすべて強いエッジです。つまり、背景そのものが hard negative です。

### 3. クラス間よりクラス内の揺れが大きい

同じコンセント記号でも、設計事務所、CAD テンプレート、図面年代、縮尺、印刷品質で形が揺れます。逆に、異なる記号が非常に似ていることもあります。

### 4. 回転と向きが効く

図面記号は 90 度回転や鏡像で意味が変わる場合があります。自然画像向けの単純な augmentation を入れると、意味が壊れることがあります。

### 5. PDF / ラスター / スキャンが混在する

ベクタ PDF なら線や文字レイヤーが残っている一方、古い紙図面のスキャンでは、ノイズ、かすれ、傾き補正、二値化の問題が支配的になります。入力形式の違いが性能に直結します。

## 2024-2026 の研究と実務が示していること

近年の construction diagram / floor plan symbol detection の研究では、YOLO 系と Faster R-CNN 系の両方が使われています。2024 年公開の construction diagrams 論文では、業務由来の高解像度図面で YOLO ベース法と Faster R-CNN ベース法の双方が有効である一方、クラス不均衡、向き、重なり、小ささが依然として支配課題であることが示されています。

また、floor plan symbol spotting 系の研究では、図面全体をそのまま縮小するより、tile ベースの切り出し戦略が重要であることが繰り返し示されています。これは現在のコミュニティ実践知とも一致しており、SAHI のような sliced inference が小物体 recall 改善の標準手段になっています。

実務では、この領域でいきなり open-vocabulary detector を本番主系にするより、

1. tile ベースの closed-set detector を作る
2. 必要なら open-vocabulary detector を候補生成や弱教師として使う
3. OCR / vector parsing / rule engine と結合する

という構成の方が再現性があります。

## 2025年の詳細調査

2025年は、この領域で「公開データセットの規模」と「図面を画像だけで見ない」という2点が大きく前進した年です。

### 1. ArchCAD-400K が示したもの

2025年3月28日に初版が arXiv に出た `ArchCAD-400K: A Large-Scale CAD drawings Dataset and New Baseline for Panoptic Symbol Spotting` は、この分野でかなり重要です。論文では、CAD の内部属性を使った annotation engine を提案し、`413,062 chunks` を `5,538 drawings` から構築したとされています。さらに、既存最大級データセットの 26 倍超の規模と、line-grained annotation、panoptic symbol spotting を前面に出しています。

実務的に重要なのは次の 4 点です。

- データ立ち上げ:
  - 手作業アノテーションだけではなく、CAD の内部属性を利用した半自動ラベリングが現実的になった
- 問題定義:
  - bbox 検出だけでなく、symbol spotting をより構造的に扱う方向が強くなった
- モデル設計:
  - raster 特徴と primitive / CAD 属性を融合する発想が出てきた
- 評価:
  - 単一の detector 精度だけでなく、panoptic 的に構造をどこまで保持できるかを見る流れが強まった

つまり、2025年以降は「図面を単なる画像に変換して detector を当てるだけ」では、研究的にも実務的にも一段弱い立場になっています。

### 2. 2025年11月10日の multi-modal parsing 論文が示したもの

`A Study on Methods for Parsing Architectural Multi-Modal Data and Extracting Modeling Parameters` は、2025年11月10日に公開され、DXF、テキスト、表をまたぐ multi-modal parsing を扱っています。ここで重要なのは、建築図面処理の主戦場が「記号単体の検出」から、「図面・テキスト・表をまたいで modeling parameters を抽出する」方向へ広がっていることです。

論文要旨では、次の構成が明示されています。

- vector element parsing と layer semantic analysis
- spatial topology relationship analysis
- text 側では domain dictionary + BiLSTM-CRF
- table 側では multi-scale sliding window

実務への含意はかなり強いです。

- 記号 detector 単体で完了する案件は限定的
- DXF / PDF / 表 / 注記を同時に扱えるパイプラインが必要
- 「door / window / electrical schedule」など、図面外の表情報が最終的な意味決定に効く
- 記号検出の評価指標だけでは、最終用途のモデリング精度を説明しきれない

特にこの論文では、door と window の認識 F1 が wall や column より低く、記号や開口部の処理が依然として難しいことが示されています。これは現場感とも一致しています。建築図面では、線分構造が明瞭な対象より、周辺文脈と一緒に意味が決まる対象の方が難しいのです。

### 3. 2025年時点で何が実務標準に近いか

2025年の研究を踏まえると、実務標準に近いのは次の形です。

1. まず vector 情報があるか確認する
2. raster 化する場合も高解像度を維持する
3. tile 学習 + tile 推論をベースラインにする
4. OCR / table parsing / layer semantics を別モジュールでつなぐ
5. 必要に応じて CAD 属性や primitive 特徴を追加する

逆に、2025年時点でもなお危険なのは、

- 単一縮小画像だけで記号を拾おうとする
- 記号検出だけで図面理解までできると考える
- DXF や PDF の内部情報を捨ててしまう

という進め方です。

## 2026年の詳細調査

2026年は、建築図面処理の研究がさらに「hybrid pipeline」へ寄っています。画像モデル単体より、`object detection + OCR + topology + rule-based reconstruction` の統合が強く押し出されています。

### 1. 2026年3月6日の hybrid vectorization 論文

`A Hybrid Deep Learning and Rule-Based Method for Architectural Drawing Vectorization and CAD Reconstruction` は、2026年3月6日に公開されました。この論文で重要なのは、scanned raster image を editable CAD へ戻すために、次の4モジュールを並べている点です。

1. axis grid and dimension detection
2. text recognition and scale recovery
3. architectural line topology reconstruction
4. CAD geometric rectification and reconstruction

これは、建築図面の細かい記号検出を本番で使うときの構成とほぼ同じです。つまり、最新の研究は「記号 detector を単独で強くする」より、「検出結果を topology と geometric constraints に接続する」方向へ寄っています。

### 2. 2026年研究が実務に与える示唆

この論文から読み取れる実務上の示唆は明確です。

- スキャン図面:
  - 画像前処理と topology rectification が特に重要
- 記号検出:
  - 単独タスクとしては必要だが、それだけでは CAD 再構築に足りない
- geometry consistency:
  - 最終成果物が CAD や BIM に入るなら、box の正しさより topology の整合性が重要
- rule-based post-processing:
  - 2026年でも依然として強い

要するに、2026年時点でも、建築図面領域では end-to-end 純画像モデルが rule system を完全に置き換えたわけではありません。むしろ、deep learning で semantic anchor を取り、最後は domain constraints で整える構成の方が現実的です。

### 3. 2026年時点の現実的な技術選択

2026年3月18日時点で、建築図面の細かい記号検出に対する現実的な選択肢は次のように整理できます。

- PDF / DXF がある:
  - vector parsing を優先
  - detector は補助
- スキャン図面が中心:
  - tile detector + OCR + geometry rectification を主系にする
- まず PoC を作る:
  - YOLO 系 + SAHI
- recall を詰める:
  - Faster R-CNN / FPN 系 + sliced inference
- 最終成果物が CAD / BIM:
  - rule engine と topology reconstruction を必須コンポーネントとして扱う

### 4. 2025年から2026年で何が変わったか

この1年で変わったのは、単純に detector 精度が上がったことではありません。

- 2025年:
  - 大規模公開データと panoptic symbol spotting が前進
  - multi-modal parsing が前景化
- 2026年:
  - reconstruction まで見据えた hybrid pipeline が強くなった
  - 検出結果を geometry / topology と結びつける流れがより明確になった

したがって、2026年時点のプロ向け設計では、建築図面記号検出を「小物体検出の一種」とだけ見てはいけません。正しくは、「小物体検出を入口とする図面構造復元問題」として扱うべきです。

## 2025-2026 調査から導く実務ガイド

### 2025-2026 の結論

- detector 単体の改善より、データ生成と multi-modal 統合が効く
- CAD 属性や vector 情報を捨てないパイプラインが強い
- tile / sliced inference は依然として最重要
- 本番で価値が出るのは、記号検出の先にある parameter extraction と reconstruction
- rule-based post-processing は古い技術ではなく、2026年でも現役

### 2026年時点で避けるべき設計

- 全ページ縮小のみで学習する
- detector だけで BIM / CAD 復元まで行けると考える
- PDF / DXF の内部レイヤを無視する
- 記号ごとの AP だけを見て採用判断する
- topology error を評価しない

### 2026年時点で優先すべき設計

- vector-first で考える
- 画像 detector は tile-first で考える
- OCR / tables / notes を別系統で取り込む
- post-rule と geometric rectification を最初から設計に入れる
- ページ指標と downstream 指標で評価する

## 推奨アーキテクチャ

### パターンA: タイル化 + YOLO 系

最も実務的な開始点です。

- 向く条件:
  - クラス数が中程度
  - エッジ推論や高速処理が必要
  - まずベースラインを早く作りたい
- 構成:
  - PDF / TIFF を高解像度でラスタライズ
  - オーバーラップ付きタイルへ分割
  - YOLO 系でタイルごとに検出
  - タイル間マージ
- 長所:
  - 実装が速い
  - 学習と推論の運用がしやすい
  - SAHI と相性が良い
- 短所:
  - 密接記号の重複統合が難しい
  - 向きや縮尺差が大きいと設定依存になりやすい

### パターンB: タイル化 + Faster R-CNN / FPN

細かい記号や似たクラスの分離を少し丁寧にやりたい場合の有力候補です。

- 向く条件:
  - recall と precision の両方を詰めたい
  - クラスの形状差が微妙
  - サーバ推論を許容できる
- 長所:
  - 小物体で安定することが多い
  - FPN による multi-scale 特徴が効きやすい
- 短所:
  - 実装と運用がやや重い
  - 大量ページ処理でコストが上がる

### パターンC: detector + OCR + vector parsing

本番では、この組み合わせが最も強いです。

- detector:
  - 細かい記号を拾う
- OCR:
  - 部屋名、寸法、注記、器具番号を読む
- vector parsing:
  - PDF の線分、レイヤー、文字座標を使う
- rule engine:
  - 記号と文字、記号と部屋、記号と系統線を対応づける

建築図面は、画像だけで完結させるより、図面特有の構造情報を活用した方が圧倒的に有利です。

## 入力前処理

### ベクタ PDF がある場合

- まず PDF の vector 情報を使えるか確認する
- 可能なら text layer と line layer を保持する
- raster 化する場合も、最低 300-600 dpi 程度を比較する
- ページ回転や余白トリミングを先に揃える

### スキャン図面の場合

- deskew
- 二値化または adaptive threshold
- ノイズ除去
- 線のかすれ補正
- 裁断位置の正規化

ここでは、前処理の差がモデル差より大きいことがあります。

## vector parsing で何がどこまで取れるか

建築図面の `vector parsing` は非常に強力ですが、万能ではありません。重要なのは、「図形 primitive を抽出すること」と「それが何の記号かを理解すること」は別問題だと理解することです。

### ファイル形式ごとの現実的な目安

#### DXF / DWG 由来データ

最も強いケースです。特に `BLOCK` と `INSERT` が整理されている図面では、記号検出器を使わずに候補抽出できる範囲がかなり広いです。

- 抽出しやすいもの:
  - 設備記号
  - 凡例記号
  - 通り芯記号
  - 断面記号
  - 柱芯記号
- 抽出可能性の目安:
  - `70-100%`
- 条件:
  - block 名や layer 名が残っている
  - 回転、スケール、属性が壊れていない

一方、記号が block 化されず、単なる線分群として置かれている図面では、自作ルールや graph grouping が必要になり、抽出可能性は `40-80%` 程度まで落ちます。

#### vector PDF

`PyMuPDF` や `pdfplumber` で線、曲線、矩形、文字は取れますが、PDF 上では「この path 群が 1 つの設備記号」という情報が失われていることが多いです。

- 抽出しやすいもの:
  - 丸囲み番号
  - 単純な断面記号
  - 単純な設備記号
  - 文字と近い注記記号
- 抽出可能性の目安:
  - `30-70%`
- 条件:
  - path がきれい
  - text layer が残っている
  - ラスタ化されていない

#### scan PDF / 画像図面

この場合、`vector parsing` はほぼ効きません。主役は detector と OCR です。

- 抽出可能性の目安:
  - `0-10%`
- 主戦場:
  - deskew
  - binarization
  - OCR
  - tile detection

### 記号タイプごとの実用的な見立て

#### vector parsing だけで取りやすい

- DXF block 化された設備記号
- 通り芯記号
- 柱芯
- 丸囲み注記
- 単純な断面・立面記号

#### rule を足せば取りやすい

- コンセント
- 照明
- スイッチ
- 寸法端点
- 簡単な配管記号

#### vector parsing 単独では厳しい

- 壁線と一体化したドアスイング
- 文字がないと意味が確定しない記号
- 類似形状が多い設備図記号
- 古いスキャン図面由来の擬似ベクタ

### 実務での解釈

vector parsing の価値は、「最終認識を全部やる」ことより、次の 3 つにあります。

1. 候補領域を絞る
2. detector の hard negative を減らす
3. OCR や rule engine の入力を構造化する

したがって、vector parsing は detector の代替というより、detector の前段と後段の両方を助ける基盤と考える方が正確です。

## vector parsing で使える技術とライブラリ

### DXF / CAD 系

#### ezdxf

DXF を扱うなら第一候補です。

- 取れるもの:
  - `LINE`
  - `ARC`
  - `CIRCLE`
  - `LWPOLYLINE`
  - `TEXT`
  - `MTEXT`
  - `INSERT`
  - `ATTRIB`
- 強い用途:
  - block 展開
  - layer ごとの抽出
  - 回転、スケール、属性付き記号の取得

実務上は、`INSERT` と `BLOCK` が残っているかを最初に確認するのが重要です。これが残っていれば、図面記号抽出の難易度は大きく下がります。

### PDF ベクタ系

#### PyMuPDF

vector PDF の実務第一候補です。

- 取れるもの:
  - drawing paths
  - line / bezier / rect
  - text 座標
  - page geometry
- 強い用途:
  - page 上の primitive 抽出
  - text layer と path の同時利用

#### pdfplumber

デバッグと座標確認に非常に便利です。

- 取れるもの:
  - `line`
  - `rect`
  - `curve`
  - `char`
  - `word`
- 強い用途:
  - PDF の中身を可視化して把握する
  - detector と OCR のズレ確認

### BIM / IFC 系

#### IfcOpenShell

図面だけでなく BIM 要素とつなぎたい場合に重要です。

- 取れるもの:
  - 壁、ドア、窓などの IFC エンティティ
  - 属性
  - 幾何と配置
- 強い用途:
  - BIM と図面記号を対応づける
  - downstream の CAD / BIM 更新へつなぐ

### 幾何処理

#### Shapely

抽出した primitive を幾何的に扱うための定番です。

- 使いどころ:
  - 交差判定
  - 包含判定
  - 距離計算
  - スナップ
  - 近傍ルール

#### networkx

線分や記号の接続関係を graph として扱うのに向いています。

- 使いどころ:
  - topology reconstruction
  - 系統線接続
  - wall graph / room graph 構築

### 表と注記

#### Camelot

図面本体ではなく、設備表、仕上表、凡例表の抽出に向きます。

図面理解の最終段では、記号そのものより、表や凡例が意味決定に効くことが多いため、表抽出を別モジュールとして持つ価値があります。

## 推奨スタック

### vector PDF 中心

- `PyMuPDF`
- `pdfplumber`
- `Shapely`
- 必要に応じて `Camelot`

### DXF 中心

- `ezdxf`
- `Shapely`
- `networkx`

### BIM / IFC と接続

- `IfcOpenShell`
- `Shapely`
- `networkx`

## 実務での使い分け

- `DXF` がある:
  - まず `ezdxf`
  - detector は補助
- `vector PDF` しかない:
  - `PyMuPDF` と `pdfplumber` で primitive と text を取り、rule + detector で補う
- `scan PDF` しかない:
  - vector parsing は主役ではない
  - detector + OCR + image preprocessing を優先する

## vector parsing を使うときの注意

- PDF では、見た目上 1 つの記号でも内部的には複数 path に分かれていることがある
- DXF では、`INSERT` の回転、縮尺、属性を展開しないと意味を取り違える
- `LWPOLYLINE` の bulge を無視すると曲線が壊れる
- 記号認識よりも前に、座標系と単位系の正規化が必要
- 文字と記号の関係は、最終的に距離だけでなくレイヤや topology でも見るべき

## アノテーション設計

図面記号では、bbox だけで十分なクラスと、bbox では曖昧すぎるクラスがあります。

### bbox で十分な例

- コンセント
- 照明
- 断面記号
- 柱芯記号

### bbox だと曖昧になりやすい例

- 寸法線とその端点
- 長い設備記号
- 壁に埋もれたドアスイング記号
- テキストと一体化した注記記号

この場合は、

- oriented bbox
- instance segmentation
- detection + post-rule

のどれかを検討します。

## クラス設計の実務原則

- 規格上の意味で分けるのか、業務上の処理で分けるのかを最初に決める
- 似すぎる記号は、最初はまとめて coarse class にする
- 文字情報がないと確定できない記号は、単独クラス化しない
- ページ縮尺で見え方が変わるなら、クラスより前処理で吸収できるか先に検討する

強い設計は、「モデルが区別できるか」ではなく、「業務がその粒度を本当に必要としているか」で決まります。

## 学習設定の実践知

### 画像サイズ

図面記号では、単純な全体縮小はほぼ不利です。まずは次の比較をします。

- 全体推論
- tile 学習 + tile 推論
- 全体学習 + sliced inference

多くの案件では、tile 学習 + tile 推論が最初の勝ち筋になります。

### タイル設計

- タイルサイズ:
  - 512, 768, 1024, 1280 などを比較
- オーバーラップ:
  - 記号が境界で切れないよう 10-25% 程度を検討
- マージ:
  - NMS / NMM / class-aware merge を比較

### augmentation

自然画像と同じ発想で強くかけると危険です。

- 有効:
  - 軽い平行移動
  - 軽いスケール変更
  - コントラスト変化
  - 印刷劣化、ノイズ、ブラー
- 要注意:
  - 無差別な 90 度回転
  - 左右反転
  - 過剰 crop
  - 過剰 mosaic

記号の意味が向き依存なら、回転 augmentation はクラス定義と整合させる必要があります。

### negative sampling

この領域では hard negative を意図的に増やす価値が高いです。

- 寸法線交点
- 文字の一部
- ハッチング交点
- 壁線の端部
- 類似設備記号

誤検知しやすい背景を集めるだけで、precision が大きく改善することがあります。

## 評価のしかた

一般的な mAP だけでは足りません。最低でも次を見ます。

- クラス別 recall
- 小サイズ記号だけの AP
- 似た記号ペアの confusion
- ページ単位の誤検知数
- 1 枚の図面を処理し終えるまでの時間

図面運用では、「1ページあたり誤検知 3 個以下」「主要クラス recall 95% 以上」のようなページ単位 KPI の方が意思決定に直結します。

## 実務パイプラインの推奨形

1. 入力を分類する
   - vector PDF / raster PDF / scan を分ける
2. 前処理を分ける
   - deskew、crop、binarization、dpi 統一
3. detector を回す
   - tile ベース中心
4. OCR / vector parsing を追加する
   - 記号と文字の対応づけ
5. post-rule を適用する
   - 壁の内側だけ有効、寸法線近傍だけ有効、など
6. 人手確認 UI へ流す
   - 低信頼や競合候補のみレビュー
7. 修正結果を再学習へ戻す

## どのモデルから始めるべきか

- まず速く PoC を作る:
  - YOLO 系 + tile + SAHI
- 小物体 recall を丁寧に詰める:
  - Faster R-CNN / FPN 系 + tile
- 本番で図面意味理解までやる:
  - detector + OCR + vector parsing + rule engine
- 未知記号探索やラベル立ち上げ:
  - Grounding DINO / YOLO-World を補助利用

DETR 系や open-vocabulary 系をいきなり主系にするより、図面固有のタイル設計と post-rule を詰めた方が早く価値が出ることが多いです。

## よくある失敗

- 図面全体を 640 に縮小して学習する
- クラスを細かく切りすぎてラベルが揺れる
- OCR や vector 情報を使わず、画像だけで全部解こうとする
- 小記号案件なのに sliced inference を比較しない
- recall ではなく mAP だけで採用判断する
- 1 記号単位の指標は良いのに、ページ全体で誤検知が多すぎて業務に乗らない

## この分野の専門家がみな共有している、5つの中核的なメンタルモデル

1. 建築図面の記号検出は、自然画像検出ではなく「小物体ドキュメント検出」である
2. 最初に効くのはモデル変更より、タイル設計と前処理である
3. detector 単体では図面理解は完結せず、OCR と構造ルールが必要になる
4. クラス定義の曖昧さは、モデル性能より先に業務を壊す
5. ページ単位の運用品質を見ないと、導入判断を誤る

## この分野の専門家たちが根本的に意見を異にしている点

### 1. 画像ベースで押し切るか、vector / OCR / rule を併用するか

立場A: end-to-end に画像モデルで寄せるべき。保守対象を減らせることが最大の強みです。

立場B: 図面は構造情報が強すぎるので、vector / OCR / rule を併用すべき。再現性と説明可能性が最大の強みです。

### 2. タイル中心で設計するか、全体文脈を重視するか

立場A: 細かい記号では tile が必須。小物体 recall を守れることが最大の強みです。

立場B: 全体文脈を失うと誤検知が増える。ページ全体の関係性を保てることが最大の強みです。

### 3. open-vocabulary detector を本番に入れるか、補助に留めるか

立場A: 長尾や未知記号が多いなら本番でも使う価値がある。柔軟性が最大の強みです。

立場B: 建築図面では責任分界と閾値設計が重要なので、補助利用に留めるべき。安定運用が最大の強みです。

## 演習課題

1. A1 図面の設備記号検出で、全体縮小と tile 推論のどちらを選ぶか理由付きで説明する
2. ドア記号、窓記号、コンセント記号を同一 detector に入れるときのクラス設計方針を書く
3. vector PDF がある案件で、画像だけで解くより有利になる情報を列挙する
4. ページ単位 KPI を 3 つ定義し、mAP との差を説明する

## セルフチェック

- なぜ sliced inference がこの領域で特に効くのか説明できるか
- 回転 augmentation が危険になる条件を説明できるか
- detector の後に OCR と rule engine を入れる理由を説明できるか
- 図面 1 枚あたりの誤検知数をなぜ管理すべきか説明できるか

## 読むべき一次情報

- Towards fully automated processing and analysis of construction diagrams: AI-powered symbol detection
- ArchCAD-400K: A Large-Scale CAD drawings Dataset and New Baseline for Panoptic Symbol Spotting
- A Study on Methods for Parsing Architectural Multi-Modal Data and Extracting Modeling Parameters
- A Hybrid Deep Learning and Rule-Based Method for Architectural Drawing Vectorization and CAD Reconstruction
- SAHI Documentation
- Grounding DINO
- YOLO-World
