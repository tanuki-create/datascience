# 05. 汎化、正則化、検証

## 現場の問い

モデルは学習データに合うだけでは不十分です。現場で価値があるのは、まだ見ていないデータ、来月のデータ、別店舗のデータでも壊れないことです。

## 直感

過学習は、データの本質ではなく偶然のノイズまで覚える状態です。正則化は、モデルに「複雑になりすぎるな」と制約をかける方法です。検証データは、その制約が効いているかを見るための疑似本番です。

## 最小限の数式

```text
objective = training_loss + regularization_penalty
```

L2 正則化なら、大きすぎる重みに罰を与えます。

```text
penalty = lambda * sum(w_i^2)
```

`lambda` が大きいほど単純なモデルになりますが、大きすぎると underfit します。

## 実装で見るべきログ・指標

- train / validation / test の性能差。
- 分割方法が本番の使い方と一致しているか。
- seed や fold を変えたときのばらつき。
- セグメント別の性能。
- ハイパーパラメータ探索で validation に合わせすぎていないか。

## よくある失敗

- test set を何度も見て、実質 validation にしてしまう。
- 時系列データをランダム分割する。
- 同一ユーザーや同一物件が train と test に跨る。
- cross validation の前処理を fold 外で fit してリークする。
- validation の平均だけ見て、悪い slice を見逃す。

## 実務メモ

検証設計は、将来の利用条件のシミュレーションです。本番で未来を予測するなら時間で分けます。本番で新規ユーザーに当てるならユーザー単位で分けます。データをどう分けるかは、モデル選定以上に重要です。

## 演習

1. ランダム分割が危険な時系列タスクを 3 つ挙げる。
2. 同一ユーザーが train/test に跨ると何が起きるか説明する。
3. [examples/model_selection_cv.py](./examples/model_selection_cv.py) を実行し、CV の平均と標準偏差を読む。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 3 の estimation、Chapter 8 の regularization、Chapter 18 の regularizing networks。
- scikit-learn: cross-validation and model selection。
