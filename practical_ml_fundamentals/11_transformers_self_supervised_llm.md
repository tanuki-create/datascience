# 11. Transformer、自己教師あり、LLM

## 現場の問い

Transformer と LLM は強力ですが、魔法の部品ではありません。現場では、生成結果をどう検証するか、根拠をどう結びつけるか、コストとレイテンシをどう制御するかが中心になります。

## 直感

Self-attention は、系列内の各要素が他の要素を参照して表現を更新する仕組みです。自己教師あり学習は、ラベルなしデータから予測課題を作り、汎用表現を学びます。LLM は、この表現学習と大規模事前学習を使い、文脈に応じた生成を行います。

## 最小限の数式

attention の中心は、問い合わせ `Q`、鍵 `K`、値 `V` の重み付き和です。

```text
Attention(Q, K, V) = softmax(QK^T / sqrt(d)) V
```

実務では式そのものより、どの情報を参照できるか、参照できないかが重要です。

## 実装で見るべきログ・指標

- 入力トークン数、出力トークン数、レイテンシ、コスト。
- RAG の検索 recall と回答の根拠一致。
- hallucination の失敗例。
- prompt / model / retrieval index のバージョン。
- 安全フィルタ、人手確認、拒否条件。

## よくある失敗

- LLM の回答を正解としてログに戻し、誤りを増幅する。
- RAG を入れれば根拠付きになると思い、検索品質を評価しない。
- prompt を手で変更し、評価セットを回さない。
- fine-tuning と RAG と prompting の使い分けを決めない。
- 個人情報や機密情報の入力経路を設計しない。

## 実務メモ

LLM システムの評価は、自然文の「良さ」だけでは不十分です。業務では、根拠の正しさ、禁止事項の遵守、回答不能時の挙動、再現性、コスト、遅延を評価します。

RAG は検索システムと生成システムの合成です。回答が悪いときは、検索で必要文書が取れていないのか、取れているのに生成が誤ったのかを分けて調査します。

## 演習

1. 社内 FAQ bot の評価項目を 10 個作る。
2. RAG の失敗を retrieval failure と generation failure に分ける。
3. prompt を変更したときに必ず回す回帰テストを設計する。

## PDFまたは一次資料との対応

- Theodoridis: Chapter 19 Transformers, GPT, BERT, self-supervised learning。
- 関連: [rag/](../rag/), [vector_search_cs_foundations/](../vector_search_cs_foundations/)。
