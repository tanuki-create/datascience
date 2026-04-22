# 検知モデル学習 完全ガイド

この文書は、物体検出を中心に、検知モデルの学習を基礎から実務レベルまでまとめた完全ガイドです。特に、現場で最も差が出やすい **学習設定** を、個別項目ごとに深掘りします。

本ディレクトリの他文書との関係は次の通りです。

- 基礎概念は [01_foundations.md](./01_foundations.md)
- 用語と指標は [02_terms_and_metrics.md](./02_terms_and_metrics.md)
- モデル系統は [03_model_families_and_mechanisms.md](./03_model_families_and_mechanisms.md)
- 学習実務の標準形は [04_training_playbook.md](./04_training_playbook.md)
- エンドツーエンド運用は [08_end_to_end_training_workflow.md](./08_end_to_end_training_workflow.md)
- アノテーション標準は [11_annotation_guidelines_professional.md](./11_annotation_guidelines_professional.md)
- クラウド GPU の判断は [12_cloud_gpu_training_practice.md](./12_cloud_gpu_training_practice.md)

この文書の役割は、それらを横断しつつ、**学習設定を中心に一冊で参照できる状態にすること** です。

## 第1章. まず押さえる結論

検知モデルの性能は、実務では次の順で決まりやすいです。

1. 問題設定とクラス設計
2. ラベル品質
3. train / val / test 分割
4. 学習設定
5. 閾値設計と後処理
6. モデル変更

特に重要なのは、学習設定を個別に最適化するのではなく、**相互作用として見ること** です。

- `learning rate` は `batch size` とセットで見る
- `image size` は `small object recall` と `GPU memory` とセットで見る
- `augmentation` は `label quality` と `split` とセットで見る
- `optimizer` は `backbone` と `fine-tuning depth` とセットで見る
- `multichannel auxiliary data` は `fusion design` と `normalization` と `missing modality handling` とセットで見る
- `epoch` は固定値ではなく `validation curve` とセットで見る

この前提を外すと、設定を一つずつ触っても再現性が出ません。

## 第2章. 検知モデル学習の全体像

検知モデル学習は、分類よりも設計点が多いです。最低限でも次を決める必要があります。

1. 何を正例とするか
2. 何を負例とするか
3. bbox をどう描くか
4. train / val / test をどう切るか
5. 何の指標で比較するか
6. どの設定を固定し、どれを探索するか

標準的な流れは次です。

1. データ収集
2. クラス設計
3. アノテーション
4. QA
5. 分割
6. ベースライン学習
7. エラー解析
8. 設定調整
9. 閾値最適化
10. 本番検証
11. 監視と再学習

## 第3章. 基礎知識

### 3.1 検知とは何か

物体検出は、画像中の対象を見つけて、位置とクラスを同時に出す問題です。分類と違い、次の失敗が別々に起きます。

- 存在を見逃す
- 存在しないものを誤検知する
- クラスを取り違える
- 位置がずれる
- 一つの物体を複数回出す

そのため、分類モデルの感覚で `accuracy` だけ見ても役に立ちません。

### 3.2 実務で見るべき指標

- `mAP`
  - 研究比較では標準
  - 現場での運用コストは直接は表しにくい
- `precision`
  - 誤検知を減らしたいときに重要
- `recall`
  - 見逃しを減らしたいときに重要
- `PR-AUC`
  - クラス不均衡が強いときに有効
- `per-image false positives`
  - 現場の確認工数に直結する
- `class-wise recall`
  - 長尾クラスや安全重要クラスの確認に重要

### 3.3 実務で先に決めるべきこと

- 見逃しが高コストか、誤検知が高コストか
- 対象の最小サイズは何 px か
- 推論は edge か cloud か
- しきい値をクラスごとに分けるか
- 最終出力は自動処理か、人への候補提示か

これが曖昧だと、学習設定をいくら詰めても方向を外します。

## 第4章. データとラベルの設計

### 4.1 データの質が設定より先

学習設定は重要ですが、次の問題があると改善幅は限定的です。

- ラベル漏れ
- bbox のブレ
- クラス定義の揺れ
- train と val のリーク
- 本番分布と異なる検証データ

### 4.2 train / val / test 分割の原則

分割はランダムだけでは不十分です。次を優先します。

- 同一動画は跨がせない
- 同一設備、同一顧客、同一現場は分けて評価する
- 時系列変化があるなら時系列で後ろを test に置く
- rare class が各 split に最低限残るようにする

### 4.3 現場で効くデータ改善

- hard negative を集める
- 誤検知例を定期的に再投入する
- 本番の悪条件サンプルを val に混ぜる
- class merge / split を早めに見直す

### 4.4 Multichannel 補助画像データの設計

実務では `RGB` 以外に、次のような補助チャネルを持つ案件があります。

- `depth`
- `thermal / infrared`
- `NIR`
- `polarization`
- `edge map`
- `segmentation prior`
- `mask`
- `elevation / DSM`
- `event frame` や時系列差分

これらは単純に「4ch, 5ch にすれば強くなる」とは限りません。むしろ、次を先に固めないと性能が不安定になります。

- 物理的に同じ視点か
- 時刻同期しているか
- 解像度と画角が合っているか
- チャネルごとの欠損率はどうか
- 本番でも全チャネルが常に入るか
- 補助チャネルが本当に識別に効いているか

#### 補助チャネルが効く典型例

- `RGB + thermal`
  - 夜間監視
  - 逆光環境
  - 発熱体の検出
- `RGB + depth`
  - 前景と背景の分離
  - 物体の高さ差が重要
  - 類似色背景からの分離
- `RGB + NIR`
  - 植生、素材差、反射差の補助
- `RGB + edge / mask prior`
  - 図面、文書、工業部品

#### 効かない、あるいは危険な例

- センサ間で厳密に位置がずれている
- train では補助チャネルがあるが本番では欠損する
- 補助チャネルにだけラベルリークが乗っている
- 補助チャネルの dynamic range がバラバラ
- 少量データで高次元入力だけ増やしている

## 第5章. モデル選定の基本線

設定の前に、モデル系統の選び方を揃えます。

- YOLO 系
  - 立ち上がりが速い
  - 実装と export の成熟度が高い
  - エッジ案件で強い
- RT-DETR / RF-DETR 系
  - GPU / cloud 推論で有力
  - NMS-free や end-to-end の設計が魅力
  - メモリと学習運用の難度は少し上がる
- open-vocabulary 系
  - 本番主系よりも pre-label と tail discovery に向く

モデルは重要ですが、最初の 80% は設定とデータで決まることが多いです。

## 第6章. 学習設定の全体マップ

学習設定は、次の5層で考えると整理しやすいです。

### 6.1 最適化系

- optimizer
- learning rate
- lr scheduler
- warmup
- weight decay
- gradient clipping
- mixed precision
- EMA

### 6.2 データ供給系

- batch size
- effective batch size
- sampler
- class weighting
- dataloader workers
- mosaic / mixup / copy-paste などの augmentation

### 6.3 入出力表現系

- image size
- multi-scale training
- aspect ratio strategy
- anchor / matcher / assigner
- loss function
- loss weights

### 6.4 学習戦略系

- epochs / max steps
- early stopping
- freeze / unfreeze
- pretrained weights
- backbone lr multiplier
- checkpoint policy
- validation frequency

### 6.5 マルチチャネル / マルチモーダル系

- fusion timing
- channel-wise normalization
- modality dropout
- missing channel strategy
- sensor alignment
- modality-specific augmentation
- branch-wise learning rate
- fusion block freeze / unfreeze

これらの層は独立ではありません。例えば `image size` を上げると `batch size` が下がり、結果として `learning rate` の再設計が必要になります。

マルチチャネル案件では、さらに `fusion design` を変えるだけで最適 `learning rate`、`batch size`、`augmentation` が崩れます。

## 第7章. 学習設定の深掘り

### 7.1 Optimizer

#### 何を決める項目か

勾配を使って重みをどう更新するかを決めます。

#### 実務上の基本線

- `AdamW`
  - まず最初に選びやすい
  - Transformer 系、ViT 系、fine-tuning で扱いやすい
- `SGD + momentum`
  - CNN 系の古典的な強い選択肢
  - 大規模学習や最終調整で効くことがある
- `RMSprop` や特殊 optimizer
  - 標準化された再現レシピがあるときだけ検討

#### どう効くか

- `AdamW` は立ち上がりが速い
- `SGD` は収束まで時間がかかるが、最終的な汎化で強いことがある
- fine-tune 対象が浅いなら `AdamW` の扱いやすさが勝ちやすい

#### 典型トラブル

- 小規模データで `SGD` にして学習が進まない
- ViT バックボーンで `SGD` に寄せすぎて初期収束が遅い
- `AdamW` で過学習気味なのに `weight decay` を見直していない

#### 実務の目安

- YOLO 系の標準 recipe が強いならまずそれに従う
- Transformer 系や backbone 微調整では `AdamW` を優先
- optimizer を変えるのは、split と lr と image size が固まってから

### 7.2 Learning Rate

#### 何を決める項目か

1 step あたりでどれだけ強く重みを動かすかを決めます。

#### なぜ最重要か

多くの学習不良は、モデル選択ではなく learning rate のミスです。

- 高すぎる
  - loss が不安定
  - bbox が飛ぶ
  - validation が改善しない
- 低すぎる
  - 収束が遅い
  - backbone がほとんど更新されない
  - 途中で頭打ちに見える

#### 実務の目安

- `AdamW`: `1e-4` から `3e-4` を起点にしやすい
- `SGD`: `1e-2` 前後から入ることが多い
- backbone は head より 5 分の 1 から 10 分の 1 に落とすことが多い

#### LR を決める考え方

- pretrained backbone を壊したくないなら下げる
- batch size を上げたら LR も見直す
- image size を上げて effective batch が落ちたら過大 LR になりやすい
- 過学習ではなく未収束なのかを見誤らない

#### 症状から見る目安

- train loss も val も動かない:
  - 低すぎる可能性
- train は下がるが val が大きく揺れる:
  - 高すぎる可能性
- 前半だけ伸びて後半で停滞:
  - scheduler か warmup を見直す

### 7.3 LR Scheduler

#### 役割

学習中に learning rate をどう変化させるかを決めます。

#### よく使う選択肢

- `cosine decay`
  - 汎用的で扱いやすい
- `one-cycle`
  - 短期学習で効くことがある
- `step decay`
  - 古典的で説明しやすい
- `plateau`
  - 検証指標ベースだが検出では使いどころが限られる

#### 実務判断

- 迷うなら `warmup + cosine`
- 再現レシピが配布されているモデルはそのまま踏襲
- scheduler だけ変えて比較するときは total steps を固定

#### 失敗例

- epoch を増やしたのに scheduler の山が前倒しで意味を失う
- step decay のタイミングが早すぎて未収束になる

### 7.4 Warmup

#### 役割

学習初期だけ LR を低くして、突然大きく更新しないようにします。

#### 重要な理由

検出モデルは初期の不安定さが大きく、特に次で効きます。

- pretrained backbone の微調整
- large image size
- AMP 使用時
- Transformer 系

#### 目安

- 最初の数百 step から数 epoch
- 小規模データなら短め
- backbone を全部解凍して始めるなら長めが安全

#### 症状

- 学習開始直後に loss が暴れる
- first epoch の予測が極端
- gradient overflow が出やすい

これらがあるなら warmup を入れる価値があります。

### 7.5 Batch Size と Effective Batch Size

#### 何を決める項目か

1 回の更新で何枚の画像を見て勾配を計算するかを決めます。

#### 実務での考え方

- 大きい batch
  - 勾配が安定しやすい
  - GPU メモリを使う
  - 1 epoch あたりの update 回数は減る
- 小さい batch
  - ノイズが多い
  - memory 制約下では現実的
  - LR 調整を誤ると不安定

#### Effective Batch Size

分散学習や gradient accumulation を使うなら、実効 batch を見る必要があります。

`effective_batch_size = per_gpu_batch x num_gpus x accumulation_steps`

#### 現場での罠

- `batch size` を変えたのに LR を据え置く
- gradient accumulation を入れたのに scheduler steps を再計算していない
- batch normalization 系の挙動変化を無視する

#### 実務ルール

- まず GPU に無理なく載る範囲で最大近辺を試す
- 不安定なら batch を下げる前に LR を疑う
- batch を 2 倍にしたら LR も再調整する

### 7.6 Epochs / Max Steps

#### 役割

どこまで学習を続けるかを決めます。

#### 実務の原則

epoch は固定数字ではなく、**データサイズと validation curve** で決めます。

- データが少ない
  - epoch は多くなりがち
  - 過学習しやすい
- データが多い
  - step ベース管理の方が分かりやすい
  - 早めに傾向が見える

#### 典型パターン

- 少量 fine-tune:
  - 数十 epoch で十分なことが多い
- 大規模 scratch or long fine-tune:
  - max steps ベースで設計した方が比較しやすい

#### 失敗例

- dataset が小さいのに長く回しすぎる
- epoch 数を増やしても scheduler が先に終わっていて意味がない

### 7.7 Early Stopping

#### 役割

検証性能の改善が止まったら学習を打ち切ります。

#### 有効な場面

- 小規模データ
- hyperparameter 探索中
- cloud GPU コストを抑えたいとき

#### 注意点

- noisy な val では短すぎる patience が危険
- rare class の recall は遅れて改善することがある
- one metric だけで止めると、業務上重要なクラスを落とすことがある

### 7.8 Image Size

#### なぜ重要か

検出では入力解像度が直接、対象の見え方を変えます。特に小物体案件では支配的です。

#### 効き方

- 高解像度
  - small object recall が上がりやすい
  - 学習時間とメモリが増える
  - batch size が下がる
- 低解像度
  - 高速
  - 小物体と細部の境界が消えやすい

#### 実務判断

- 最小対象が極小なら、最初から高解像度を検討
- ただし full image 高解像度が重いなら slicing も比較
- 図面、航空、監視遠景は `image size` を最優先で見る

#### 症状

- 大物体は取れるのに小物体だけ落ちる
- bbox が粗くなりやすい
- 密集物体で merge しやすい

### 7.9 Multi-Scale Training

#### 役割

学習中に入力解像度を変え、サイズ変動への頑健性を上げます。

#### 効く場面

- カメラやソースごとに解像度差が大きい
- 本番でリサイズ条件が揺れる
- target size distribution が広い

#### 注意

- small object 案件では下振れ側の scale が強すぎると害になる
- val は固定条件で取り、train だけ multi-scale にする

### 7.10 Aspect Ratio Strategy

#### 何を決めるか

入力画像を正方形へリサイズするか、letterbox するか、tile するかを決めます。

#### 実務での論点

- 正方形固定
  - 実装が簡単
  - 歪みが出ることがある
- letterbox
  - 幾何歪みを抑えやすい
  - 余白パターンへの過学習に注意
- tile / slice
  - 小物体に強い
  - 結果統合の設計が必要

### 7.11 Augmentation

#### 役割

本番の多様性を学習時に擬似的に作ります。

#### 主要カテゴリ

- 幾何変換
  - flip, scale, crop, translate, rotate
- 見た目変換
  - blur, noise, jpeg, brightness, contrast, color jitter
- 合成
  - mosaic, mixup, copy-paste
- ドメイン模倣
  - motion blur, low light, fog, compression artifact

#### 実務原則

- 本番で起きる変化だけ入れる
- 小物体案件では aggressive crop を疑う
- 図面や文書では color jitter より解像感の維持が重要
- mix 系 augmentation は class imbalance 改善に効くこともあるが、bbox 解釈を壊すこともある

#### よくある誤り

- augment を盛りすぎて train すら難しくする
- rare class の見え方を破壊する
- val にも augment を入れて比較不能にする

### 7.12 Sampler と Class Balance

#### 役割

どの画像をどれだけの頻度で学習に出すかを決めます。

#### 手段

- oversampling
- weighted sampler
- class-aware sampling
- hard example mining

#### 実務で効く場面

- rare class が極端に少ない
- データソースによって分布差が大きい
- hard negative が一部画像群に偏る

#### 注意

- oversampling は過学習しやすい
- rare class を上げても false positive が増えることがある
- sampler の変更は loss や threshold と一緒に見る

### 7.13 Loss Function

#### 検出で一般に分かれる項目

- classification loss
- box regression loss
- objectness / confidence loss
- auxiliary loss

#### 代表例

- `BCE`
- `Focal Loss`
- `Varifocal Loss`
- `IoU / GIoU / DIoU / CIoU`
- `L1`

#### 実務判断

- 長尾や背景優勢なら `Focal` 系が候補
- localization を詰めたいなら IoU 系の設計を重視
- DINO / DETR 系は matching と auxiliary loss の理解が必要

#### よくある誤解

loss を変える前に、ラベル品質と split を見直すべき場面が多いです。loss 変更は効きますが、万能ではありません。

### 7.14 Loss Weights

#### 何を決めるか

分類、bbox、objectness など複数 loss の寄与度を決めます。

#### どう効くか

- box loss を強める
  - 位置は詰まりやすい
  - class 学習が弱くなることがある
- cls loss を強める
  - class confusion 改善に効くことがある
  - localization が犠牲になることもある

#### 現場での使い方

- デフォルト recipe が強いモデルでは安易に崩さない
- エラー解析で問題が明確なときだけ動かす
- one change at a time を徹底する

### 7.15 Matcher / Assigner / Anchor 設計

#### なぜ重要か

検出では、どの予測をどの正解に対応付けるかが学習の核です。

#### 典型要素

- IoU threshold
- top-k assignment
- Hungarian matching
- anchor size / ratio
- anchor-free point assignment

#### 実務上の論点

- 小物体が弱いなら anchor / feature map / assigner のどこがボトルネックかを見る
- DETR 系では Hungarian matching の不安定さを denoising や auxiliary loss で緩和する
- YOLO 系では anchor-free 化や task-aligned assigner の挙動を理解する

#### 触る優先順位

assigner は効きますが、初心者が最初に触る場所ではありません。まずは image size、split、label、lr を固めます。

### 7.16 Weight Decay

#### 役割

重みの過大化を抑え、過学習を緩和します。

#### 実務の目安

- `AdamW` で `1e-4` から `1e-2` を調整対象にすることが多い
- backbone と head で扱いを変えることもある

#### 症状

- train は良いのに val が伸びない
- 微調整なのに backbone を壊し気味

#### 注意

augmentation と label noise が大きいと、weight decay だけで解決しません。

### 7.17 Label Smoothing

#### 役割

分類ターゲットを少しだけ平滑化して、過信を抑えます。

#### 向く場面

- class 境界がやや曖昧
- 過信した confidence が多い

#### 注意

- class が厳密で bbox の位置も重要な案件では効かないこともある
- calibrate の問題を label smoothing だけで片付けない

### 7.18 EMA

#### 役割

学習中の重みの指数移動平均を保持し、推論時に安定した重みを使います。

#### 効きやすい場面

- noisy training
- 小規模 fine-tune
- val が少し揺れやすい設定

#### 実務判断

- 使えるなら基本は ON
- ただし resume や export の扱いは実装依存なので確認する

### 7.19 Gradient Clipping

#### 役割

極端に大きい勾配で学習が壊れるのを防ぎます。

#### 効く場面

- Transformer 系
- 高解像度学習
- mixed precision
- 全層 unfreeze の初期段階

#### 症状

- ときどき loss が跳ねる
- NaN が出る
- AMP overflow が頻発する

### 7.20 Mixed Precision

#### 役割

FP16 / BF16 を使って速度とメモリ効率を上げます。

#### 利点

- batch size を上げやすい
- 学習速度が上がる

#### 注意

- 実装によっては数値不安定が出る
- clipping や warmup と組み合わせて安定化する
- reproducibility は FP32 より落ちることがある

### 7.21 Freeze / Unfreeze

#### 役割

どこまでの層を更新するかを制御します。

#### 実務の基本線

- 小規模データ
  - まず head 中心
  - その後に浅く unfreeze
- 中規模以上でドメイン差が大きい
  - 上位層から段階的に解凍
- 十分なデータがあり本番分布差が大きい
  - 全体 fine-tune も候補

#### トラブル

- 最初から全解凍して pretrained 表現を壊す
- freeze しすぎて target domain に適応しない

### 7.22 Pretrained Weights

#### なぜ重要か

検出は scratch 学習の難度が高いので、事前学習の恩恵が大きいです。

#### 選び方

- COCO 系 pretrained
  - 汎用的
- domain-specific pretrained
  - 近いデータなら強い
- self-supervised backbone
  - ラベルが少ないときに有効なことがある

#### 実務判断

- まずは強い公開 pretrained から開始
- scratch は比較実験が必要なときだけ

### 7.23 Validation Frequency

#### 役割

どの頻度で検証するかを決めます。

#### 実務判断

- 小規模実験では頻繁に見る
- 大規模学習では数 epoch ごとでも良い
- class-wise metrics を常に残す

#### 注意

- val が重いからといって全く見ないのは危険
- threshold 固定と free threshold の両方で見ると理解が進む

### 7.24 Checkpoint Policy

#### 役割

何を保存し、どれを best とみなすかを決めます。

#### 実務で保存すべきもの

- best overall
- best recall-heavy
- latest
- optimizer state
- config と seed

#### 理由

本番要件によって最良モデルが変わるためです。`mAP best` が業務 best とは限りません。

### 7.25 Multichannel 補助画像データ

#### 何を指すか

`RGB` に加えて別チャネル、別センサ、別表現を入力に使う設計です。

- 同一テンソルに連結する `4ch / 5ch / 6ch...`
- `RGB` と `thermal` を別 branch で持つ two-stream
- `RGB` と時系列差分、edge map、prior mask を併用する補助入力

#### まず決めるべきこと

- 追加チャネルは本番でも安定取得できるか
- 位置合わせは十分か
- 補助チャネルは主情報か補助情報か
- 単一 `RGB` baseline を超える根拠があるか
- チャネル欠損時の fallback を持つか

#### 実務で強い考え方

最初から複雑な fusion に入るより、次の順で比較します。

1. `RGB` 単独 baseline
2. 入力連結の early fusion
3. branch 分離の late / mid fusion
4. modality dropout を入れた堅牢化

これで、補助チャネルが本当に効いているかを切り分けやすくなります。

### 7.26 Fusion Timing

#### Early Fusion

入力段階でチャネルを結合します。

例:

- `RGB + depth -> 4ch input`
- `RGB + thermal -> 4ch or 6ch input`

利点:

- 実装が簡単
- 推論コストが比較的小さい
- 小規模案件で立ち上がりが速い

弱点:

- pretrained `RGB` 重みをそのまま使いにくい
- modality ごとの性質差を吸収しにくい
- 位置ずれに弱い

#### Mid Fusion

各モダリティを別 branch である程度特徴抽出してから融合します。

利点:

- modality ごとの性質を残しやすい
- `RGB` pretrained backbone を流用しやすい
- 補助チャネルの寄与を解析しやすい

弱点:

- 実装とチューニングが重い
- branch 間の学習バランスが難しい

#### Late Fusion

各モダリティでほぼ独立に特徴や予測を作り、後段で統合します。

利点:

- 欠損チャネルに強くしやすい
- センサ単位の切り分けがしやすい

弱点:

- 推論コストが高い
- end-to-end 最適化の利点が薄れることがある

#### 現場の推奨順

- 補助チャネルが weak signal なら early fusion から
- 補助チャネルの統計が `RGB` と大きく違うなら mid fusion を優先
- 欠損やセンサ停止が現実に起きるなら late fusion も比較する

### 7.27 Channel-Wise Normalization

#### なぜ重要か

`RGB` と `depth`、`thermal`、`NIR` は値域と意味が違います。全チャネルを同じ平均・分散で正規化すると壊れます。

#### 実務ルール

- チャネルごとに平均・分散を持つ
- 物理量なら min-max より robust scaling を検討
- depth の欠損値と valid 値を区別する
- thermal はセンサ固有のレンジ差を確認する

#### 典型トラブル

- depth 欠損の `0` が本物の近距離と混ざる
- thermal のレンジが撮影条件で大きく変わる
- 正規化統計を train / val / test で混ぜて計算している

### 7.28 Pretrained Weight と入力チャネル拡張

#### 実務上の論点

多くの公開 backbone は `RGB 3ch` 前提です。補助チャネルを足すと最初の畳み込みや patch embedding の扱いを決める必要があります。

#### 典型手法

- 追加チャネルをランダム初期化する
- `RGB` 重みの平均や複製で初期化する
- `RGB` branch は pretrained、補助 branch は別初期化にする
- 補助 branch を浅く作って後段で融合する

#### 実務判断

- データが少ないなら `RGB pretrained` を壊さない設計を優先
- 補助チャネルが主役なら branch 分離を検討
- early fusion で 4ch にするなら first layer の初期化差分を必ず記録する

### 7.29 Modality Dropout と欠損耐性

#### なぜ必要か

本番では補助チャネルの欠損が起きます。

- thermal camera の停止
- depth の穴
- auxiliary preprocessor の失敗
- 同期遅延

#### 有効な手段

- channel dropout
- modality dropout
- missing mask の追加
- fallback to RGB-only の学習

#### 実務の原則

train で常に全チャネルを見せると、本番欠損時に壊れやすいです。欠損を想定した学習を入れます。

### 7.30 Modality-Specific Augmentation

#### 原則

全チャネルに同じ augmentation をそのまま掛ければよいわけではありません。

- 幾何変換
  - 基本は全チャネル同期
- photometric 変換
  - `RGB` と `thermal` を同一ルールで変えない
- noise 付与
  - センサごとのノイズモデルを分ける
- blur
  - motion blur は `RGB` だけ強く出ることもある

#### 危険な例

- depth に color jitter を掛ける
- thermal に `RGB` 用 hue shift を掛ける
- 位置ずれがあるのに幾何変換を別々に掛ける

### 7.31 Sensor Alignment と同期

#### なぜ重要か

補助チャネルの価値は、同じ対象を同じ位置で見ていることが前提です。

#### 確認すべきこと

- intrinsic / extrinsic calibration
- temporal sync
- spatial registration
- resampling による歪み
- ROI の切り出し基準

#### 実務で起きる失敗

- 学習時だけ alignment が良く、本番で崩れる
- bbox は `RGB` 基準なのに thermal が数 px ずれる
- 動体で frame sync がズレ、補助チャネルがノイズになる

### 7.32 Branch-Wise Learning Rate

#### 役割

`RGB pretrained branch` と `auxiliary branch` の更新量を分けます。

#### 実務の基本線

- `RGB pretrained branch` は低 LR
- 新規 `auxiliary branch` は高め LR
- fusion block は中間 LR

#### 理由

既存の `RGB` 表現を壊さず、補助チャネルだけを早く適応させるためです。

### 7.33 Multichannel 案件の評価

#### 必ず比較するもの

- `RGB-only`
- `aux-only`
- `RGB + aux`
- `RGB + aux` with missing modality

#### 見るべき指標

- overall mAP
- class-wise recall
- 難条件 subset の改善幅
- modality 欠損時の劣化率
- per-image false positives

#### 実務の判断軸

平均指標が少し良いだけでは足りません。次のどれかを満たしたいです。

- 夜間や逆光など難条件で明確に効く
- 安全重要クラスの recall が上がる
- 誤検知が減ってレビュー工数が下がる
- 欠損時にも RGB-only と同等以上を維持できる

## 第8章. 学習設定はどう組み合わせるか

### 8.1 まず固める順番

1. split
2. metric
3. pretrained model
4. image size
5. batch size
6. learning rate
7. augmentation
8. threshold と後処理

### 8.2 一度に変える項目数

原則は 1 回の実験で 1 つ、多くても 2 つです。特に次を同時に変えると解釈不能になりやすいです。

- image size と augmentation
- batch size と learning rate
- optimizer と scheduler
- sampler と loss

### 8.3 探索の優先順位

1. データ修正
2. image size
3. learning rate
4. augmentation
5. threshold
6. sampler
7. loss / assigner
8. model family

## 第9章. 典型レシピ

### 9.1 YOLO 系の堅いベースライン

- pretrained weights を使う
- `imgsz` は 640 か 960 から開始
- batch は GPU に載る範囲で最大近辺
- LR は既定 recipe を基準に、batch と image size に合わせて微調整
- val は class-wise recall を必ず確認
- 誤検知例を hard negative として再投入

### 9.2 RT-DETR / RF-DETR 系

- `AdamW` と `warmup + cosine` を基本線にする
- AMP と gradient clipping を前提で考える
- backbone と head の LR を分ける
- memory を見ながら batch と image size を決める
- export 後 latency まで比較する

### 9.3 小物体案件

- image size を最優先
- slicing も同時比較
- aggressive crop を避ける
- size-wise AP と recall を確認
- label 漏れがないか重点 QA

### 9.4 長尾クラス案件

- sampler と threshold を class 別に調整
- confusion matrix を class group で見る
- ontology の merge / split を見直す
- hard negative mining を継続する

## 第10章. エラー症状から逆引きする

### 10.1 train も val も伸びない

疑う順番は次です。

1. ラベル壊れ
2. split の異常
3. learning rate が低すぎる
4. augment が強すぎる
5. class 定義が曖昧

### 10.2 train は上がるが val が上がらない

主な候補は次です。

- 過学習
- val の分布差
- leakage の逆、つまり val が難しすぎる
- weight decay 不足
- augment 不足

### 10.3 小物体だけ落ちる

- image size 不足
- feature map 解像度不足
- label 漏れ
- slicing 不足
- NMS や threshold が厳しすぎる

### 10.4 誤検知が多い

- hard negative 不足
- threshold 低すぎ
- class granularity が粗すぎる
- augmentation により背景パターンを壊した

### 10.5 学習が不安定

- LR が高い
- warmup が短い
- batch が小さすぎる
- AMP と clipping の調整不足
- 全層 unfreeze が早すぎる

## 第11章. 現場レベルの工夫

### 11.1 Hard Negative Mining

最も効きやすい改善の一つです。

手順は単純です。

1. 本番または擬似本番で誤検知を集める
2. 代表的な誤検知パターンを束ねる
3. 正常画像として再投入する
4. クラス定義の曖昧さがあれば ontology も見直す

### 11.2 Threshold を class ごとに分ける

全クラス一律しきい値は便利ですが、実務では粗いことが多いです。

- 安全重要クラスは recall 寄り
- 多発ノイズクラスは precision 寄り
- rare class は少し緩めるが、review flow で吸収する

### 11.3 Production-like Validation Set を作る

きれいな検証データだけでは本番性能を見誤ります。次を意図的に含めます。

- 低照度
- ブレ
- 遮蔽
- 逆光
- 圧縮劣化
- 異なるカメラ

### 11.4 Human-in-the-Loop

完全自動にせず、人間の確認と再学習を前提にした方が強い案件は多いです。

- 低 confidence だけ確認対象にする
- 特定クラスだけ manual review に送る
- reviewer の訂正を再学習データに回す

### 11.5 Open-Vocabulary / Foundation Model の活用

現場での最も強い使い方は次です。

1. promptable detector で候補を広く拾う
2. 人手で修正する
3. closed-set detector を学習する
4. rare class 追加時だけ foundation model を補助に使う

### 11.6 Deployment-Aware Training

本番が edge なら、学習段階から次を固定します。

- 入力解像度
- batch 1 latency
- export 形式
- quantization 方針
- memory ceiling

最後に圧縮を足すより、最初から制約込みで学習した方が失敗しにくいです。

### 11.7 Multichannel 補助画像データの現場運用

補助チャネル案件では、学習時より運用時の事故が多いです。次を運用要件に入れます。

- センサごとのヘルスチェック
- 時刻同期の監視
- registration error の監視
- modality 欠損時の fallback
- `RGB-only` での最低保証精度

特に重要なのは、`RGB + aux` の精度だけでなく、`aux` 欠損時の degraded mode を先に設計することです。

## 第12章. 応用例

### 12.1 外観検査

重要点は次です。

- 小傷、欠け、汚れの最小サイズを定義する
- 照明差を train と val の両方で見る
- hard negative を多めに集める
- bbox より defect segmentation の方が良いかも比較する

### 12.2 監視映像

- 単フレーム性能だけでなく、時間方向の安定性を確認
- blur と low-light augment が効きやすい
- track 連携で誤検知を減らせることがある
- 動画リークを厳しく防ぐ

### 12.3 航空・ドローン

- 小物体対策が最優先
- slicing, OBB, high-resolution の比較を早めにやる
- negative area が広いので false positive 管理が重要

### 12.4 図面・文書・記号検出

- raster 化条件を固定する
- image size と tile 戦略の影響が大きい
- class granularity と OCR / rule engine の責任分界を決める

### 12.6 RGB + Thermal / Depth の代表パターン

#### 夜間監視の `RGB + thermal`

- daytime では `RGB` 優勢
- nighttime では thermal が効く
- したがって、時間帯 subset 別に評価する
- fusion は mid fusion の方が壊れにくいことが多い

#### 産業検査の `RGB + depth`

- 形状差、段差、盛り上がりの検出に効く
- depth 欠損と反射ノイズを QA する
- augmentation は geometry 同期を崩さない

#### 航空・リモートセンシングの `RGB + NIR / IR`

- 植生差、温度差、地表性質差に効く
- センサ別正規化を明示する
- registration ずれが数 px でも小物体では痛い

### 12.5 小売・物流

- class imbalance が強い
- 背景類似が多く誤検知しやすい
- SKU ごとにやり過ぎる前に class hierarchy を整理する

## 第13章. 実験テンプレート

### 13.1 最初のベースライン

- データ split を固定
- pretrained model を 1 つ選ぶ
- image size を 1 つ選ぶ
- 標準 augmentation で開始
- LR と batch を 1 組だけ試す
- best / latest checkpoint を保存
- val 画像を毎回レビューする

### 13.2 2 周目に動かす項目

- image size
- hard negative 追加
- LR 微調整
- threshold 最適化
- class-wise sampler

### 13.3 3 周目に動かす項目

- loss / assigner
- backbone fine-tuning depth
- multi-scale
- slicing
- model family 変更

## 第14章. 精度改善のプロの工夫

### 14.1 Error Bucket を先に作る

強いチームは、まず失敗を分類します。全体 `mAP` だけでは改善優先順位が見えません。

典型的な bucket は次です。

- false positive
- false negative
- class confusion
- localization error
- small object miss
- occlusion miss
- low-light failure
- modality missing failure

この分類を作ると、`learning rate` を触るべきか、`image size` を上げるべきか、`hard negative` を集めるべきかが見えます。

### 14.2 Slice 評価を標準化する

全体指標だけでなく、条件別に切って評価します。

- 夜間
- 雨、霧、逆光
- 小物体
- 遠距離
- 混雑
- 特定カメラ
- 特定拠点
- 補助チャネル欠損時

実務では、改善の価値は全体平均よりも **業務上きつい slice でどれだけ改善したか** で決まることが多いです。

### 14.3 Threshold を class-wise に最適化する

全クラス一律しきい値は簡単ですが、荒いです。

- 安全重要クラス
  - recall 寄りにする
- 多発ノイズクラス
  - precision 寄りにする
- rare class
  - 少し緩めて review flow で吸収する

学習を触らずに threshold だけで改善できることは多いので、後回しにしない方がよいです。

### 14.4 Hard Negative Mining を継続運用する

誤検知した正常画像を集めて再学習に回します。

特に効きやすいのは次です。

- 背景の模様誤検知
- 類似クラス誤検知
- 反射、影、照明変化
- thermal や depth のノイズ起因誤検知

一度だけではなく、**本番から継続回収する運用** にした方が効きます。

### 14.5 Label Cleaning を定期作業にする

精度が伸びない原因がラベルにあることは非常に多いです。

有効なやり方は次です。

- 高 loss サンプルを抽出する
- prediction と label の大きな不一致を抽出する
- rare class を重点レビューする
- bbox の過小、過大、漏れを分類して直す

loss の工夫より、label cleaning の方が効く場面は多いです。

### 14.6 Annotation Policy 自体を見直す

モデル改善ではなく、アノテーション規約の見直しが必要な場合があります。

- class を merge する
- class を split する
- `ignore` を設ける
- `uncertain` を設ける
- visible box と full box の定義を固定する

ラベル定義が曖昧なままだと、モデルは学習できても本番では安定しません。

### 14.7 Pseudo-Label を丁寧に使う

未ラベルデータに高信頼予測を付けて再学習します。

効く場面:

- 未ラベルデータは多い
- ラベル付けコストが高い
- baseline はある程度安定している

注意点:

- 低精度モデルで回すと誤りを増幅する
- high precision 側の threshold を使う
- rare class は人手確認を入れる

### 14.8 Curriculum と Hard Example Replay

最初はきれいなデータから入り、後半で難例を増やすと安定する案件があります。

また、難例を毎回一定割合で混ぜる `hard example replay` も有効です。

向く場面:

- ラベル品質に揺れがある
- マルチチャネルで学習が不安定
- small object と hard negative が混在する

### 14.9 TTA は限定的に使う

`flip` や `multi-scale` の test-time augmentation は、PoC やオフライン処理では有効です。

注意点:

- latency が増える
- production では cost と相談
- edge では現実的でないことが多い

### 14.10 Ensemble と WBF

単体モデルが頭打ちのときは有効です。

- 異なる seed の ensemble
- 異なる family の ensemble
- `Weighted Boxes Fusion`

ただし、運用コストは確実に増えます。まず単体モデルを詰めてから検討します。

### 14.11 Calibration を見る

confidence が信用できるかを確認します。

重要な理由:

- threshold 設計がしやすい
- human-in-the-loop が作りやすい
- class-wise policy が安定する

同じ `mAP` でも、confidence が過信気味なモデルは運用で扱いにくいです。

### 14.12 Distillation を使う

重い teacher を使って軽量 student を鍛えます。

向く場面:

- edge deployment
- INT8 や軽量化で精度が落ちやすい
- 本番モデルは軽くしたいが学習時は重いモデルを使える

### 14.13 Deployment 条件で評価する

学習時の FP32 指標だけで判断しません。次を比較します。

- ONNX export 後
- TensorRT 化後
- FP16 化後
- INT8 化後
- batch 1 latency

最後に export したら精度が落ちる、は珍しくありません。

### 14.14 Production Drift Monitoring を先に設計する

精度改善は学習時だけで終わりません。本番で drift を拾えるかが重要です。

見るべきもの:

- 入力分布
- class 頻度
- confidence 分布
- per-image false positives
- modality 欠損率
- 特定 camera / site の悪化

drift 監視があると、次に何を再学習すべきかが明確になります。

### 14.15 Context 情報を使う

単画像だけでなく、追加コンテキストが効くことがあります。

- camera id
- site id
- timestamp
- 前後フレーム
- tracker 情報
- センサ状態

ただし、リークと shortcut learning の危険があるので、train / val / test の分離は厳密に行います。

### 14.16 プロの改善順序

迷ったら次の順番が堅いです。

1. error bucket を作る
2. label cleaning をする
3. slice 評価を作る
4. threshold を最適化する
5. hard negative を追加する
6. `image size`、`augmentation`、`learning rate` を調整する
7. pseudo-label、TTA、ensemble、distillation を検討する

### 14.17 学習前にやるべきプロの確認

学習前の詰めが甘いと、後ろでいくら改善しても効率が悪いです。強いチームは次を先に固めます。

- `negative definition`
  - 何を非対象とするか
- `minimum object size`
  - 何 px 未満は検出対象外にするか
- `ignore policy`
  - 曖昧物体、見切れ、重遮蔽をどう扱うか
- `train / val / test contract`
  - split の責任境界を文書化する
- `annotation QA checklist`
  - bbox の過小、過大、漏れ、class ぶれ
- `production constraints`
  - edge、cloud、latency、memory、欠損 modality

この段階で仕様が曖昧なら、モデル比較に入るべきではありません。

### 14.18 学習後にやるべきプロの確認

学習が終わった後に見るべきものは `best mAP` だけではありません。

- class-wise AP / recall
- size-wise AP
- confusion matrix
- confidence distribution
- per-image false positives
- difficult slice の画像レビュー
- export 後の精度差
- threshold sweep 結果

強い運用では、`best checkpoint` を出して終わりではなく、**採用可否レビュー** を別に行います。

### 14.19 クラス分け戦略

クラス設計は、精度改善に直結します。モデルの都合ではなく、業務判断と視覚的分離可能性の両方から決めます。

#### class を split すべき場面

- 業務上の処理が分かれる
- 見た目の差が十分大きい
- 混同コストが高い
- 片方だけ recall を上げたい

#### class を merge すべき場面

- 見た目差がほとんどない
- ラベル数が少なすぎる
- confusion が慢性的に高い
- 業務上は同じ後処理でよい

#### hierarchical class の考え方

単一の flat class にせず、階層で考えると整理しやすいです。

- 上位:
  - `vehicle`
  - `person`
  - `defect`
- 下位:
  - `car`
  - `truck`
  - `forklift`

まず上位で安定させ、必要なら下位へ落とす方が実務では堅いです。

#### ignore / uncertain class の使いどころ

- ラベラー間で一致しにくい
- 視覚的に境界が曖昧
- 対象外だが背景としても扱いたくない

`ignore` を適切に置くと、学習ノイズを大きく減らせます。

#### long-tail class の整理

rare class を無理に独立させるより、次を検討します。

- 上位 class に一時統合する
- two-stage で詳細分類する
- detector と classifier を分離する
- foundation model を補助に使う

### 14.20 クラス分け戦略の実務フレーム

迷ったら、各 class 候補に対して次を表で整理します。

- visual separability
- annotation consistency
- business importance
- sample count
- false positive cost
- false negative cost
- deployment action

この表を作ると、`split / merge / ignore / hierarchy` の判断がかなり明確になります。

### 14.21 モデルアンサンブルの設計

`ensemble` は最後の奥の手ではありますが、適切に使うとかなり効きます。

#### 代表パターン

- 同一 architecture、異なる seed
- 同一 family、異なる image size
- 異なる family
  - YOLO 系 + DETR 系
- modality 別 detector の統合
  - `RGB-only` と `thermal-only`
- slice 特化 detector の統合
  - day model と night model

#### どのとき効きやすいか

- 単体モデルの error pattern が違う
- small object と large object で強みが分かれる
- false positive の種類がモデルごとに違う
- 異なる modality が難条件で補完し合う

#### 効かないとき

- どのモデルも同じところで失敗する
- 同一 recipe の複製で多様性がない
- 閾値と後処理が未調整

### 14.22 Ensemble の統合方法

#### NMS ベース統合

- 実装が簡単
- 推論後に扱いやすい
- 強い 1 モデルに引っ張られやすい

#### Weighted Boxes Fusion

- 複数モデルの bbox を平均化しやすい
- localization 改善に効くことがある
- モデル間 calibration が悪いと不安定

#### score averaging / rank averaging

- classification 的な統合がしやすい
- bbox の統合設計は別に必要

#### rule-based gating

- day / night
- camera id
- site id
- modality availability

運用条件が明確に分かれるなら、単純平均より gating の方が強いことがあります。

### 14.23 Ensemble の実務注意点

- export と serving が複雑になる
- latency と memory が増える
- confidence calibration を揃える必要がある
- 再学習時の管理コストが増える
- どのモデルが効いているか追跡しにくい

したがって、次の順で使うのが堅いです。

1. 単体モデルを十分詰める
2. threshold と post-process を調整する
3. error diversity を確認する
4. 小さい ensemble から試す

### 14.24 後処理も精度改善の一部として扱う

学習後の後処理で変わる精度はかなり大きいです。

- class-wise threshold
- NMS / Soft-NMS
- WBF
- tracker 連携
- temporal smoothing
- topology / rule filtering
- ROI filtering

図面、監視、製造のような案件では、**モデル単体精度より後処理込み精度** の方が重要です。

### 14.25 学習前後をつなぐ改善ループ

プロの現場では、改善は次のループで回します。

1. 学習前に ontology と split を固定する
2. baseline を 1 本作る
3. error bucket と slice 評価を作る
4. threshold と後処理を詰める
5. hard negative と relabel を回す
6. 必要なら class 再設計をする
7. それでも足りなければ ensemble や distillation に進む

この順番だと、複雑な施策を早く入れすぎずに済みます。

## 第15章. 設定項目別の実務チェックリスト

### 15.1 Learning Rate

- batch size 変更時に見直したか
- backbone と head を同じ LR にしていないか
- first epoch で不安定になっていないか

### 15.2 Batch Size

- effective batch を把握しているか
- accumulation 導入時に scheduler を再計算したか
- memory を使い切るだけの目的になっていないか

### 15.3 Image Size

- 最小対象サイズに対して十分か
- val を同条件で比較しているか
- slicing と比較したか

### 15.4 Augmentation

- 本番で起きる変動だけを入れているか
- rare class の意味を壊していないか
- val に混入していないか

### 15.5 Freeze / Unfreeze

- データ量に対して深すぎないか
- backbone を壊していないか
- domain gap に対して浅すぎないか

### 15.6 Loss / Assigner

- 触る前に label と split を疑ったか
- class confusion か localization error かを分けたか
- 変更理由を画像付きで説明できるか

## 第16章. 現場で共有したいメンタルモデル

1. 検知モデルの精度は、データと設定と閾値の合成結果である。
2. 学習率は単独変数ではなく、batch と scheduler と warmup の一部である。
3. image size は model size より効くことがある。特に小物体ではそうなりやすい。
4. open-vocabulary model は本番 detector というより data engine として強い。
5. エラー解析は数値だけでは足りず、必ず画像で見る必要がある。

## 第17章. 迷ったときの推奨順

迷ったら、次の順番で疑います。

1. ラベルは正しいか
2. split は正しいか
3. metric は業務に合っているか
4. image size は足りているか
5. LR は妥当か
6. augmentation は本番に寄っているか
7. threshold は最適化したか
8. それでも足りなければ model family を変える

## 第18章. 最後のまとめ

検知モデル学習で最も重要なのは、設定項目の名前を覚えることではありません。**どの設定が、どの症状に効き、何と相互作用するかを理解すること** です。

実務では、次の姿勢が最も強いです。

- 最初に強い baseline を作る
- 設定は少数ずつ動かす
- 画像付きで失敗を分類する
- hard negative と再学習ループを作る
- model change を最後に回す

この順番を守ると、検知モデルの学習はかなり安定します。
