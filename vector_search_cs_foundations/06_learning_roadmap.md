# 06. 学習ロードマップ

検索・RAG・推薦・データ基盤系の学習は、いきなり大規模分散検索を目指すより、4段階で積み上げると実務レビューに耐えやすくなります。

## Level 1: 小規模実験ができる

### 学ぶべき知識

全文検索の基本として、inverted index、tokenization、normalization、BM25を学びます。

ベクトル検索の基本として、embedding、cosine similarity、inner product、L2、nearest neighbor search、chunkingを学びます。

検索評価の基本として、precision@k、recall@k、MRR、nDCG、hit rate、評価クエリセットの作り方を学びます。

RAGの基本として、retrieval、reranking、context construction、grounding、hallucinationを学びます。

### 作るべきミニプロジェクト

小さな文書検索アプリを作ります。Markdown、PDF、FAQなどを取り込み、キーワード検索とベクトル検索を両方実装します。

10から100件程度の社内ドキュメント風データでRAGプロトタイプを作り、chunk size、overlap、top-k、distance metricを変えて検索結果を比較します。

20から50件の評価クエリを作り、正解文書を手でラベル付けし、検索方式ごとにスコアを比較します。

### 読むべき技術領域

情報検索の基礎、embeddingの基礎、RAGパターン、テキスト前処理、検索評価指標。

### 到達基準

BM25とベクトル検索の違いを説明できること。検索できた気がする、ではなく評価クエリで品質を比較できること。文書が取れない、取れたが順位が低い、文脈が長すぎる、回答生成で誤る、という失敗分類ができること。

## Level 2: 技術選定の理由を説明できる

### 学ぶべき知識

検索エンジンとベクトルDBの選定軸を学びます。PostgreSQL + pgvector、FAISS、Qdrant、Weaviate、Milvus、Elasticsearch/OpenSearch、Redis Vector Searchを比較します。

ANNアルゴリズムとして、HNSW、IVF、PQを学びます。

ハイブリッド検索として、lexical search、semantic search、score fusion、rerankingを学びます。

データモデリングとして、document、chunk、metadata、tenant、permission、embedding_model_versionを設計します。

### 作るべきミニプロジェクト

同じデータをpgvector、Qdrant、OpenSearchなどに入れ、latency、recall、フィルタ性能、更新反映、運用負荷を比較する検索APIを作ります。

BM25 + vector search + metadata filter + reranker を持つハイブリッド検索APIを作ります。

user / group / tenant 単位で検索結果を制限する権限制御付き検索を作り、フィルタ漏れのテストを書きます。

### 読むべき技術領域

検索エンジンのアーキテクチャ、ベクトルDBの内部構造、スコア正規化、マルチテナント設計、認可と検索フィルタリング、データパイプライン設計。

### 到達基準

「なぜこのDB・検索基盤を選ぶのか」を、データ量、QPS、更新頻度、SLA、コスト、チーム運用能力から説明できること。PoC結果から本番採用可否を判断できること。

## Level 3: 本番運用を見据えた設計ができる

### 学ぶべき知識

信頼性設計として、replication、sharding、backup/restore、failover、graceful degradationを学びます。

インデックス運用として、blue-green index、zero-downtime reindex、partial update、delete propagationを学びます。

監視として、latency、error rate、indexing lag、recall drift、empty result rate、costを学びます。

セキュリティとして、tenant isolation、document-level ACL、audit log、PII handlingを学びます。

品質運用として、query log analysis、human evaluation、regression test、feedback loopを学びます。

### 作るべきミニプロジェクト

本番想定検索サービスを作ります。ingestion pipeline、search API、reranker、monitoring dashboard、admin reindex commandを持たせます。

shadow indexを作り、検証後にalias切り替えし、rollback可能なインデックス再構築基盤を作ります。

zero-result query、low-confidence query、click-through、user feedback、regression query setを記録する検索品質モニタリングを作ります。

### 読むべき技術領域

SRE基礎、分散システムの障害設計、データパイプライン運用、Observability、セキュアなマルチテナント設計、MLOps / LLMOps / RAGOps。

### 到達基準

本番検索システムのSLOを定義できること。インデックス更新・再構築・ロールバックを設計できること。検索品質の劣化を検知できること。障害時に何を止め、何を継続するか判断できること。

## Level 4: 独自の検索基盤・大規模分散システムを設計できる

### 学ぶべき知識

分散検索アーキテクチャとして、shard、replica、coordinator、scatter-gather、query routingを学びます。

大規模インデックス設計として、segment、compaction、merge policy、tiered storage、hot/warm/coldを学びます。

大規模ベクトル検索として、ANN index partitioning、quantization、memory layout、GPU/CPU trade-offを学びます。

分散システム基礎として、consensus、consistency、backpressure、rate limiting、queueingを学びます。

ランキング基盤として、feature store、learning to rank、online/offline evaluation、A/B testingを学びます。

### 作るべきミニプロジェクト

複数shardに文書を分散し、coordinatorが検索を集約し、replica障害時に縮退する簡易分散検索エンジンを作ります。

segment merge、compaction、delete marker、rebuild costを可視化する大規模インデックスシミュレータを作ります。

API、indexing pipeline、shard strategy、failure mode、capacity model、migration planを含む検索プラットフォーム設計書を書きます。

### 読むべき技術領域

Lucene内部構造、Elasticsearch/OpenSearch/Vespaの分散設計、大規模ANN検索、分散DB、分散ログ、ストリーム処理、キャパシティプランニング、レコメンド・ランキングシステム。

### 到達基準

shard数、replica数、routing戦略を要件から決められること。latency、recall、freshness、costのトレードオフを説明できること。既製品を使うべきか、独自基盤を作るべきか判断できること。

## 共通チェックリスト

要件では、検索対象データ、現在と将来のデータ量、更新頻度、鮮度要件、QPS、p95/p99、マルチテナント、権限制御を確認します。

品質では、評価クエリセット、正解ラベル、失敗パターン分類、zero-result query、reranker効果、検索品質の回帰テストを確認します。

運用では、無停止reindex、rollback、delete反映、権限変更反映、indexing lag、backup/restore、障害時縮退を確認します。

セキュリティでは、document-level ACL、tenant isolation、query logの機密情報、PII、audit logを確認します。

コストでは、embedding生成コスト、vector indexのメモリ、reindex時の一時コスト、cache戦略、過剰なrerankingを確認します。

