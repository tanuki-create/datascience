# 物体検出モデルの系統と仕組み

この文書は、R-CNN系からYOLO、DETR、DINO系までを「何を入力し、何を予測し、どう学習し、どう推論するか」という観点で整理する。実務では、精度だけでなく、ラベルコスト、推論速度、運用のしやすさ、データ分布の変化への強さで選ぶべきである。

## まず押さえる全体像

物体検出は、画像内の各物体について「クラス」と「位置」を同時に出す問題である。分類より難しく、セグメンテーションよりラベルが軽いが、学習信号は不安定になりやすい。

検出器は大きく次の観点で分かれる。

- 候補領域を先に作るか
- 画像全体を一気に処理するか
- アンカーを前提にするか
- セット予測として一対一対応を学ぶか
- 事前学習バックボーンにどこまで依存するか

## すべての検出器を分解する共通フレーム

どのモデルも、実務では次の 5 部品に分けて理解すると整理しやすいです。

1. backbone: 画像を特徴へ変換する
2. neck: 複数スケールの特徴を混ぜる
3. head: クラス、bbox、objectness を出す
4. assignment: どの予測をどの正解に対応づけるか決める
5. post-processing: NMS や score threshold で結果を整理する

強い人は、モデル名で覚えるのではなく、「どの部品が何を楽にし、何を難しくするか」で覚えます。

## R-CNN系

R-CNN系は「候補領域を作り、その領域ごとに分類と回帰を行う」設計である。Fast/Faster R-CNN、Mask R-CNN に連なる。

- 特徴抽出: CNNバックボーンで画像全体の特徴マップを作る
- ヘッド: RPNで候補領域を提案し、RoI Align/RoI Poolingで各領域を切り出して分類・回帰する
- 損失: RPNのobjectnessとbbox回帰、検出ヘッドの分類とbbox回帰
- ラベル割当: IoUしきい値で正例・負例を決める。サンプル選択が重要
- 推論の流れ: 画像 -> 特徴抽出 -> 候補生成 -> RoI特徴抽出 -> 分類/回帰 -> NMS

長所は、精度を出しやすく、複雑なシーンでも安定しやすいこと。短所は、構成が重く、推論が遅くなりやすいこと。強い条件は、精度重視で、遅延が多少許されるサーバ推論である。

## SSD / RetinaNet

SSD系は、複数スケールの特徴マップ上でアンカーごとに直接予測する。RetinaNetは、それをFocal Lossで強化した代表例である。

- 特徴抽出: FPN系の多段特徴、または複数解像度の特徴マップ
- ヘッド: 各位置・各アンカーに対して分類とbbox回帰を並列に出す
- 損失: bbox回帰はSmooth L1やIoU系、分類はCEまたはFocal Loss
- ラベル割当: アンカーとGTのIoUで正負を決める。正例が少ないため設計が効く
- 推論の流れ: 特徴マップごとに大量の候補を出し、スコア閾値とNMSで絞る

長所は、構造が比較的単純で高速にしやすいこと。短所は、アンカー設計とラベル割当のチューニングが難しいこと。強い条件は、速度と精度のバランスが必要で、データ分布が比較的安定している場合である。

## YOLO系

YOLO系は、単一の検出ネットワークで画像全体を高速に処理する実務的な系譜である。実装差は大きいが、発想は「高スループットで十分高精度」を狙うことにある。

- 特徴抽出: CSP系、PAFPN系、軽量ViT系など実装に応じて多様
- ヘッド: 複数スケールで分類、objectness、bbox回帰を同時に出す
- 損失: bbox回帰にIoU系、分類にCE/BCE、objectnessにBCE系が多い
- ラベル割当: アンカーありなら対応アンカー、アンカーフリーなら中心・距離・タスク整合で割り当てる
- 推論の流れ: 画像 -> バックボーン/ネック -> 検出ヘッド -> しきい値処理 -> NMS

長所は、実装と運用が比較的わかりやすく、GPU上で高速に動くこと。短所は、極端に小さい物体や密集物体で設定依存が強くなること。強い条件は、リアルタイム性、エッジ推論、頻繁な再学習が必要な案件である。

## DETR系

DETR系は、検出を「セット予測」として扱い、NMSへの依存を減らした。Transformerでクエリごとに物体を出す。

- 特徴抽出: CNNまたはViTバックボーンで特徴を作る
- ヘッド: object queryが各物体候補を表し、各クエリがクラスとbboxを予測する
- 損失: Hungarian matchingで一対一対応を作り、分類とbbox回帰を最適化する
- ラベル割当: 明示的なmatchingが中心。アンカー設計より学習理論がきれい
- 推論の流れ: 特徴抽出 -> Transformer encoder/decoder -> クエリごとの予測 -> 必要なら軽い後処理

長所は、NMS依存が小さく、設計思想がシンプルなこと。短所は、学習が遅くなりやすく、データや最適化設定に敏感なこと。強い条件は、ラベル品質が高く、十分な学習計算資源がある場合である。

## DINO系

DINO系は、DETR系の学習を改善した流れとして理解するとよい。クエリ設計、matching、denoising学習などで収束を早め、精度を引き上げる。

- 特徴抽出: CNNまたはViTバックボーン
- ヘッド: object queryベースの予測
- 損失: DETR系のset lossをベースに、ノイズ付き入力からの復元学習を加える実装が多い
- ラベル割当: Hungarian matchingに加え、denoising queryで学習を安定化する
- 推論の流れ: DETRと同様だが、より実用的な精度と収束性を狙う

長所は、DETR系の弱点である収束速度を改善しやすいこと。短所は、依然として構成が複雑で、ハイパーパラメータの影響が大きいこと。強い条件は、Transformerベースの一貫した設計を活かしたい場合である。

## RT-DETR / RT-DETRv2

RT-DETR は「real-time でも DETR 系を成立させる」ことに焦点を当てた系列である。RT-DETRv2 ではさらに、柔軟性と実用性を意識した bag-of-freebies が入った。

- 特徴抽出: CNN バックボーンと効率化した encoder / decoder
- ヘッド: query ベースの end-to-end prediction
- 損失: set prediction を前提にした DETR 系損失
- ラベル割当: Hungarian matching ベース
- 推論の流れ: 特徴抽出 -> decoder query prediction -> 軽い後処理

RT-DETRv2 で重要なのは、「Transformer detector を real-time に近づけるために architecture だけでなく training recipe を積極的に最適化している」点です。論文では selective multi-scale feature extraction、discrete sampling operator、dynamic data augmentation、scale-adaptive hyperparameters が前面に出ています。

長所は、DETR 系の一貫した定式化を保ちながら real-time 帯へ寄せやすいこと。短所は、依然として dense detector より ecosystem の厚みで劣る場面があること。強い条件は、NMS を弱めたいが、DETR の重さは抑えたい場合です。

## DINOv2 のような事前学習バックボーン

DINOv2は検出器そのものではなく、強力な事前学習バックボーンとして見るべきである。実務では「検出ヘッドより前段の表現力」を引き上げる役割が大きい。

- 特徴抽出: ViT系の汎用表現が強く、少量ラベルでも転移しやすい
- ヘッド: 検出ヘッドは別途必要。FPN相当の多段出力が必要になることが多い
- 損失: バックボーンの自己教師あり損失ではなく、検出タスクの損失で微調整する
- ラベル割当: 検出器側の設計に従う。ViT特徴は高解像度の扱いが重要
- 推論の流れ: 画像 -> ViT特徴 -> 検出ヘッド -> 後処理

強みは、少データ領域、ドメインが少し違う画像、複雑な背景での表現再利用である。注意点は、解像度、メモリ、FPN接続、微調整の深さで性能が大きく変わることだ。

## Grounding DINO と open-vocabulary detector

Grounding DINO は、closed-set detector に言語を深く結合し、任意のカテゴリ名や referring expression で検出できる方向を強く押し進めたモデルです。

- 特徴抽出: 視覚特徴と言語特徴を並列で扱う
- ヘッド: language-guided query selection と cross-modality decoder
- 損失: detection と grounding をまたぐ形で学習
- ラベル割当: closed-set よりも language grounding 前提の設計になる
- 推論の流れ: 画像 + テキスト -> multimodal fusion -> query prediction

長所は、未知クラスや long-tail を prompt で扱えること。短所は、プロンプト依存性、閾値設計、hallucination 的な誤検知管理が難しいこと。強い条件は、探索、初期データ作成、属性条件付き検出です。

## YOLO-World と real-time open-vocabulary

YOLO-World は、YOLO 系の速度感を保ちつつ open-vocabulary detection を実装しようとする方向です。Grounding DINO よりも「現場で回したい」文脈に近いモデルとして読むと整理しやすいです。

- 特徴抽出: YOLO 系 backbone + text encoder
- ヘッド: region-text 類似度を用いた contrastive な head
- 損失: region-text contrastive loss
- 推論の流れ: 画像 + 語彙 -> detection + text-conditioned scoring

長所は、open-vocabulary でも速度を出しやすいこと。短所は、一般に closed-set fine-tune detector ほどの安定性は期待しにくいこと。強い条件は、 long-tail カタログ探索、商品探索、annotation bootstrap です。

## YOLOv10 と NMS-free YOLO の流れ

YOLOv10 は、dense detector でありながら NMS-free 推論へ本気で踏み込んだ点が大きいです。論文のキーワードは consistent dual assignments と、効率と精度を同時に最適化する holistic design です。

ここで重要なのは、「YOLO = NMS 前提」という従来理解が崩れ始めたことです。dense detector と end-to-end detector の境界は以前より曖昧になっています。

ただし、現場では NMS-free であることより、export、profiling、quantization、現行パイプラインとの互換性が勝つ場面も多いです。したがって、NMS-free は採用理由の 1 つであって、採用理由の全てではありません。

## 損失関数をどう考えるか

検出の損失は、少なくとも次の 3 系統に分かれます。

- 分類損失: 何の物体か
- 位置回帰損失: どこにあるか
- objectness / matching 損失: そもそも物体候補か

この 3 つのどこが支配的に壊れているかで、改善策は変わります。例えば、分類が弱いならクラス境界や hard negative を疑いますが、位置回帰が弱いならラベル品質、解像度、IoU 系損失を疑うべきです。

## モデル選定フレーム

案件でモデルを選ぶときは、次の表で考えると判断がぶれにくくなります。

| 条件 | 向きやすい系統 | 理由 |
|---|---|---|
| リアルタイム、エッジ制約 | YOLO 系 | 実装成熟度、速度、配備性が高い |
| リアルタイム、NMS 依存を減らしたい | RT-DETR / YOLOv10 系 | end-to-end 化と speed のバランスを狙える |
| 精度最優先、サーバ推論 | R-CNN 系 | 候補領域処理が難例に強い |
| 研究開発、設計の一貫性 | DETR / DINO 系 | set prediction と matching が明快 |
| 少量ラベル、転移重視 | DINOv2 系バックボーン | 事前学習表現を活かしやすい |
| 未知クラス探索、annotation bootstrap | Grounding DINO / YOLO-World | promptable detection が使える |
| 長尾、大規模データ、柔軟な検討 | RetinaNet や YOLO 系改良 | 実験の自由度と速度のバランスがよい |

## 2026時点の現実的な採用パターン

- 最終本番 detector:
  - 依然として closed-set fine-tuned detector が主役
- データ立ち上げ:
  - Grounding DINO や YOLO-World で候補 box を作り、人手で確認する
- 少量データ高難度案件:
  - DINOv2 などの強い backbone を検討する
- real-time かつ modern end-to-end:
  - RT-DETRv2 や YOLOv10 を比較対象に入れる

## 研究の最前線と本番の距離

研究最前線では、open-vocabulary、grounded detection、vision foundation model 統合が急速に進んでいます。ですが、本番では次の順で優先度が決まります。

1. 既存インフラに載るか
2. 再学習や監視の運用が回るか
3. export と profiling が安定するか
4. その上で AP や recall が十分か

この順序を逆にすると、モデル比較は派手でも導入で止まります。

## 論文を読むときの観点

モデル論文を読むときは、次の順で読むと本質を外しにくいです。

1. 何を簡単にしたのか
2. 何を複雑にしたのか
3. どの制約条件で勝っているのか
4. ベースラインとの差が、backbone、resolution、recipe の差ではないか
5. 自分の案件に移植するとき、何が再現困難か

## 系統別の選び方

- 精度優先で、多少遅くてもよい: R-CNN系
- バランス重視で、古典的な運用実績を重視: SSD / RetinaNet
- 速度と実運用のしやすさを重視: YOLO系
- アーキテクチャの整合性とNMS依存の低減を重視: DETR系
- DETRの学習安定性を高めたい: DINO系
- 少量ラベルで強い表現を使いたい: DINOv2などの事前学習バックボーン

## 実務でよく出る失敗パターン

- IoUしきい値やNMSしきい値を固定したまま、データセットが変わって崩れる
- 小物体が多いのに入力解像度を上げない
- ラベル品質の揺れをモデルの限界と誤認する
- クラス不均衡を無視して、精度だけ見てしまう
- 推論速度の要件を後から思い出して設計し直す

## この分野の専門家がみな共有している、5つの中核的なメンタルモデル

1. 物体検出は「分類」と「位置推定」の同時最適化であり、どちらか片方だけを良くしても意味がない。
2. モデルの差は、ヘッドだけでなく、特徴ピラミッド、ラベル割当、後処理まで含めたシステム差である。
3. データ品質はモデル差より大きいことが多く、検出では特にアノテーションの一貫性が性能を支配する。
4. 小物体、密集物体、遮蔽、長尾分布は「例外」ではなく、実運用ではむしろ本番である。
5. 精度は単一指標では決まらず、mAP、再現率、遅延、スループット、安定性を同時に見る必要がある。

## この分野の専門家たちが根本的に意見を異にしている点

1. アンカー方式 vs アンカーフリー方式
- アンカー支持の最強主張: 実装と学習の挙動が読みやすく、成熟したノウハウが多い。
- アンカーフリー支持の最強主張: 設計負債を減らし、タスク依存のアンカー調整から解放される。

2. CNN中心 vs ViT/Transformer中心
- CNN支持の最強主張: 局所性と計算効率が強く、検出では今でも現実的に強い。
- Transformer支持の最強主張: 長距離依存と表現の柔軟性で、スケール時の上限が高い。

3. NMS前提でよいか、NMSを減らすべきか
- NMS支持の最強主張: 単純で高速、既存運用との互換性が高い。
- NMS削減支持の最強主張: 重複抑制の手作業を減らし、学習と推論の一貫性を高められる。

## 演習課題

1. ある案件で YOLO 系ではなく Faster R-CNN を選ぶ理由を、精度以外の観点も含めて説明する
2. DETR 系で NMS が不要になる発想を、自分の言葉で説明する
3. DINOv2 をバックボーンに使うとき、なぜ neck と解像度設計が重要か説明する
4. backbone、neck、head、assignment、post-processing のどこを変えるべきか、典型的な失敗例ごとに整理する

## セルフチェック

- one-stage と DETR 系の差を、出力フォーマットではなく学習の定式化として説明できるか
- モデル差と学習レシピ差を分けて議論できるか
- 論文の SOTA を、そのまま自案件に入れてはいけない理由を説明できるか

## 読むべき一次情報

- DINO
- RT-DETRv2
- YOLOv10
- Grounding DINO
- YOLO-World
- DINOv2
