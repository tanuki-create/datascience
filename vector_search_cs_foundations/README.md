# 実用的な検索・RAGシステムのためのCS基礎

このフォルダは、ベクトル検索、RAG、推薦、画像検索、類似検索、検索基盤、DB選定、インフラ設計に必要なコンピューターサイエンス基礎を、実務判断に使える形で章立てしたものです。

出発点は次の問題意識です。

> 実験用・小規模なら FAISS で cosine 距離を総当たりしてもよい。しかし実用的なシステムを作るには、IVF / PQ / HNSW などのインデックスを「ライブラリ機能」ではなく、計算量、メモリ、I/O、近似、分散処理、運用制約の問題として理解する必要がある。

## 章構成

1. [00_core_message.md](00_core_message.md)  
   ポストの核心。FAISS総当たり検索と本番システムの差分。

2. [01_cs_foundations.md](01_cs_foundations.md)  
   実用システムに必要なCS基礎。アルゴリズム、DB、OS、分散、セキュリティ、RAGOpsまで。

3. [02_ann_indexes_ivf_pq_hnsw.md](02_ann_indexes_ivf_pq_hnsw.md)  
   IVF / PQ / HNSW の深掘り。なぜ速いのか、何を犠牲にするのか、どう選ぶのか。

4. [03_database_selection.md](03_database_selection.md)  
   PostgreSQL + pgvector、FAISS、Milvus、Qdrant、Weaviate、Elasticsearch/OpenSearch、Redis Vector Search、自作検索基盤の選定。

5. [04_production_gap.md](04_production_gap.md)  
   小規模実験では問題にならないが、本番で効いてくる観点。

6. [05_decision_framework.md](05_decision_framework.md)  
   条件別の実用的な判断フレームワーク。

7. [06_learning_roadmap.md](06_learning_roadmap.md)  
   Level 1 から Level 4 までの学習ロードマップ。

8. [07_glossary.md](07_glossary.md)  
   各章で出てくる専門用語の注釈。

9. [08_architecture_diagrams.md](08_architecture_diagrams.md)  
   RAG、ベクトル検索、検索基盤の具体的な構成図レビュー素材。

10. [09_benchmark_template.md](09_benchmark_template.md)  
   RAG/ベクトルDB/検索基盤を比較するための指標、実験条件、表形式テンプレート、落とし穴、合格基準。

11. [10_design_review_checksheet.md](10_design_review_checksheet.md)  
   DB選定、ANN、フィルタ/権限、更新/削除、RAG品質、運用、セキュリティ、コストを確認する設計レビュー用チェックシート。

12. [11_rag_implementation_sample.md](11_rag_implementation_sample.md)  
   ingest / search / rerank / generate / evaluate の流れが分かるRAG最小実装サンプル。

13. [sources.md](sources.md)  
   参照した一次情報と関連資料。

## 使い方

設計レビューでは、まず `00_core_message.md` と `05_decision_framework.md` を読み、レビュー会では `10_design_review_checksheet.md` を使うのが効率的です。

学習目的では、`01_cs_foundations.md` から順に読み、`06_learning_roadmap.md` のミニプロジェクトを作ると理解が実装に落ちます。

実装レビューでは、`11_rag_implementation_sample.md` を参照して、ingest、search、rerank、generate、evaluateの責務分離を確認してください。

専門用語の意味を確認したい場合は、[07_glossary.md](07_glossary.md) を参照してください。
