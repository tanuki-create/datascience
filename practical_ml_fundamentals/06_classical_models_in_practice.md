# 06. 古典的モデルを現場で使う

## 現場の問い

古典的モデルは今でも現場で強いです。特に表形式データ、少量データ、説明責任が必要な案件では、深層学習より早く、安く、安定して価値を出すことがあります。

## 直感

モデルは得意な仮定が違います。

| モデル | 得意な状況 | 注意点 |
|---|---|---|
| kNN | 類似事例が多い | 高次元・大規模で重い |
| Naive Bayes | テキストや疎な特徴 | 独立仮定が粗い |
| 決定木 | ルール説明 | 単体では過学習しやすい |
| Random Forest | 安定した表データ | 推論や説明がやや重い |
| Gradient Boosting | 表データの高精度 | validation への過適合に注意 |
| SVM | 中規模・境界が重要 | 大規模化と確率解釈に注意 |

## 最小限の数式

モデル選定は、単に `score` 最大化ではなく制約付き最適化です。

```text
choose model that maximizes utility
subject to latency, cost, explainability, data size, maintenance
```

## 実装で見るべきログ・指標

- ベースラインとの差。
- 推論時間とメモリ。
- 重要特徴量やルールの妥当性。
- seed / fold を変えた安定性。
- rare category や外れ値への挙動。

## よくある失敗

- 最新モデルを使う理由を精度以外で説明できない。
- Boosting の validation tuning をやりすぎる。
- feature importance を因果効果として読んでしまう。
- 木モデルなら前処理不要だと思い、欠損やカテゴリの意味を確認しない。
- 解釈可能性が必要な現場でブラックボックスを先に導入する。

## 実務メモ

表データでは、強い baseline として Gradient Boosting 系を試す価値があります。ただし、業務説明や運用保守が重い場合は、ロジスティック回帰や浅い木の方がよいこともあります。選定理由は「精度が高い」ではなく、「この制約下で十分な精度・速度・説明性を満たす」と書きます。

## 演習

1. 3 つの業務タスクに対し、最初に試すモデルと理由を書く。
2. feature importance を意思決定に使うときの注意点を説明する。
3. kNN が本番で扱いにくい理由を、推論時の計算量から説明する。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 7 Classification、Chapter 11 RKHS and kernels。
- scikit-learn: nearest neighbors, naive Bayes, trees, ensembles, SVM。
