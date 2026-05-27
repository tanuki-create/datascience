# 03. 線形回帰、分類、基礎モデル

## 現場の問い

最初に複雑なモデルを使うべきではありません。線形回帰やロジスティック回帰は、単純だから弱いのではなく、データと評価の問題を発見しやすい基準線です。

## 直感

線形モデルは、特徴量を重み付きで足し合わせます。重みが見えるので、どの特徴が予測に効いているかを確認しやすいです。分類では、その合計値を確率やクラスに変換します。

ベースラインの役割は、最高精度を出すことではありません。データ分割、特徴量、指標、ラベルが最低限まともかを早く確認することです。

## 最小限の数式

線形回帰:

```text
y_hat = w1*x1 + w2*x2 + ... + b
```

ロジスティック回帰:

```text
p = sigmoid(w*x + b)
sigmoid(z) = 1 / (1 + exp(-z))
```

`p` は正例らしさのスコアです。分類クラスは `p >= threshold` のように閾値で決めます。

## 実装で見るべきログ・指標

- ダミーベースラインとの差。
- 学習データと検証データの性能差。
- 係数の符号と大きさ。
- 閾値別の precision / recall。
- 誤分類例の上位パターン。

## よくある失敗

- accuracy だけで不均衡データを評価する。
- 標準化せずに係数の大小を比較する。
- 閾値 0.5 を固定し、業務コストを反映しない。
- 線形で解けない問題を、特徴量設計なしに線形モデルへ押し込む。
- 高精度の複雑モデルを使い、データリークに気づけなくなる。

## 実務メモ

最初のモデルは、説明可能で壊れにくいものがよいです。線形モデルや決定木で異常に高い精度が出たら、喜ぶ前にリークを疑います。逆に単純なモデルでまったく当たらない場合、複雑化の前に目的変数、分割、特徴量、ラベル品質を見直します。

## 演習

1. [examples/classification_baseline.py](./examples/classification_baseline.py) を実行し、閾値を変えたときの precision / recall を比較する。
2. [examples/regression_baseline.py](./examples/regression_baseline.py) の特徴量を 1 つ消し、MAE の変化を見る。
3. 自分の業務で、線形モデルが説明しやすい特徴量を 5 個挙げる。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 3 Learning in parametric modeling、Chapter 6 Least-squares family、Chapter 7 Classification。
- scikit-learn User Guide: linear models, model evaluation。
