# 04. 損失関数、最適化、SGD

## 現場の問い

学習とは、モデルの間違いを数値化し、その数値を小さくするようにパラメータを更新することです。現場で重要なのは、どの損失を小さくしているのか、その損失が業務上の失敗を表しているのか、学習が安定しているのかです。

## 直感

損失関数はモデルに対する採点表です。平均二乗誤差は大きな誤差に強く罰を与えます。交差エントロピーは確率の自信過剰な間違いを強く罰します。

SGD は全データを一度に見ず、小さなバッチから近似的に良い方向へ進みます。ノイズはありますが、大規模データや深層学習ではこの揺れが現実的な計算方法になります。

## 最小限の数式

```text
loss = L(y, f(x; theta))
theta <- theta - learning_rate * gradient(loss)
```

`learning_rate` が大きすぎると発散し、小さすぎると進みません。勾配が不安定なときは、データスケール、初期値、バッチサイズ、損失、外れ値を疑います。

## 実装で見るべきログ・指標

- train loss と validation loss の推移。
- learning rate と batch size。
- 勾配爆発・勾配消失の兆候。
- NaN / inf の発生。
- seed を変えたときのばらつき。
- early stopping の発火タイミング。

## よくある失敗

- loss は下がっているが、業務指標は改善していない。
- learning rate を勘で変え、実験記録を残さない。
- validation loss が悪化しているのに長く学習する。
- 正規化不足で一部特徴量が勾配を支配する。
- class imbalance を無視し、損失が多数派クラスに寄る。

## 実務メモ

学習曲線は健康診断です。train も validation も悪いなら underfit、train だけ良く validation が悪いなら overfit、どちらも激しく揺れるなら最適化かデータの問題を疑います。

深層学習で詰まったときは、まず小さなデータに overfit できるかを確認します。小さなデータにも合わないなら、モデル容量より実装、ラベル、損失、前処理の問題である可能性が高いです。

## 演習

1. 学習率を大きくしすぎると何が起きるか、学習曲線で説明する。
2. 回帰で MSE と MAE のどちらを選ぶか、外れ値が多いケースで比較する。
3. 不均衡分類で class weight を使う前に確認すべきことを書く。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 5 Online learning and SGD、Chapter 8 Convex analytic path、Chapter 18 Backpropagation。
- scikit-learn: SGDClassifier / SGDRegressor documentation。
