# 07. 前処理、特徴量、Pipeline

## 現場の問い

ML の事故は、モデル本体より前処理で起きることが多いです。学習時と推論時で処理が違う、validation の外で前処理を fit する、カテゴリの未知値に落ちる、といった問題は本番で頻出します。

## 直感

特徴量は、モデルに渡す観測の形です。良い特徴量は、業務上の構造をモデルが使いやすい形にします。Pipeline は、その変換を一つの再現可能な手順として固定します。

## 最小限の数式

前処理込みのモデルは、次の合成関数です。

```text
y_hat = model(transform(raw_input))
```

`transform` が学習時と推論時で変わると、同じモデルでも別物になります。

## 実装で見るべきログ・指標

- 前処理をどこで fit しているか。
- unknown category の扱い。
- 欠損補完のルール。
- 学習・推論で同じコードを通っているか。
- 特徴量の数、疎密、値域。
- pipeline artifact とモデル artifact の対応。

## よくある失敗

- scaler や encoder を全データで fit してから分割する。
- notebook 上の前処理を本番コードに手で移植してずれる。
- 欠損補完値を意味なく 0 にする。
- カテゴリ増加で推論が落ちる。
- 特徴量を増やしすぎ、運用で取得不能になる。

## 実務メモ

scikit-learn の `Pipeline` と `ColumnTransformer` は、前処理とモデルを一体化するための基本道具です。実験時点から pipeline 化しておくと、cross validation や本番化でリークを減らせます。

特徴量は多ければよいわけではありません。取得コスト、鮮度、欠損、説明性、削除時の影響まで含めて評価します。

## 演習

1. [examples/sklearn_pipeline_workflow.py](./examples/sklearn_pipeline_workflow.py) を実行し、数値・カテゴリ前処理がどこで定義されているか確認する。
2. unknown category が来たときに落ちない設定を探す。
3. train と serve で処理がずれる例を 2 つ書く。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 3, 6, 8 の parametric modeling and optimization。
- scikit-learn: Pipeline, ColumnTransformer, preprocessing。
