# 01. 実用システムに必要なCS基礎

この章では、ベクトル検索、RAG、推薦、画像検索、類似検索、検索基盤、DB選定、インフラ設計に効くCS基礎を整理します。

各項目で見るべき観点は同じです。

- 何を理解すべきか
- なぜ実用システムで重要か
- ベクトル検索・RAG・検索基盤との関係
- 知らないと起きる失敗
- 学ぶべきキーワード

## アルゴリズムと計算量

### 何を理解すべきか

総当たり検索は、N件のd次元ベクトルに対して、おおむね `O(Nd)` の距離計算をします。Nやdが小さい間は問題になりませんが、Nが1000万、1億になると、1クエリごとに膨大なCPU命令とメモリアクセスが発生します。

### なぜ実用システムで重要か

本番では平均速度ではなく、同時アクセス時のp95 / p99が問題になります。検索1回が遅いだけでなく、CPUを占有して他リクエストも遅くなります。

### ベクトル検索・RAG・検索基盤との関係

FAISS Flat は exact の基準線として重要です。HNSW、IVF、PQ は `O(Nd)` の全件比較を避けるための近似戦略です。pgvector、Milvus、Qdrant、Weaviate、Elasticsearch/OpenSearch の選定でも、どの探索空間削減を採用するかが効きます。

### 知らないと起きる失敗

PoCで100万件未満だけ測って「これで本番も大丈夫」と判断し、1000万件でレイテンシとCPU費用が破綻します。

### 学ぶべきキーワード

Big-O、top-k、heap、branching factor、recall-latency tradeoff、approximation、candidate generation。

## データ構造

### 何を理解すべきか

検索性能はアルゴリズムだけでなく、データの置き方で決まります。配列、ヒープ、B-tree、LSM-tree、転置インデックス、グラフ、クラスタリスト、ビットマップ、Roaring bitmap などの構造が重要です。

### なぜ実用システムで重要か

CPUはメモリをランダムに読むより、連続領域を読む方が得意です。HNSWはグラフの隣接リスト、IVFはクラスタごとのリスト、PQは短いコード列というデータ構造で探索コストを変えます。

### ベクトル検索・RAG・検索基盤との関係

Elasticsearch/OpenSearch は転置インデックスとLuceneセグメントが強みです。Qdrantはpayload indexとHNSWを組み合わせます。pgvectorはPostgresの通常インデックス、partial index、partitioningとベクトルインデックスを組み合わせて考える必要があります。

### 知らないと起きる失敗

「HNSWを貼れば速い」と考え、tenant_idやACLのフィルタが後段になり、検索後に候補が消えてtop-kが返らなくなります。

### 学ぶべきキーワード

B-tree、LSM-tree、inverted index、bitmap index、graph index、adjacency list、posting list、segment、heap。

## 距離計算・類似度・線形代数

### 何を理解すべきか

cosine、inner product、L2 はランキングの意味が違います。cosine は角度、inner product は方向とノルム、L2 は幾何距離です。正規化済みベクトルなら、cosine と inner product と L2 は単調変換で近い関係になります。

### なぜ実用システムで重要か

埋め込みモデルが想定している距離関数とDB側の距離関数がズレると、検索品質が落ちます。正規化漏れは本番では静かな品質劣化になります。

### ベクトル検索・RAG・検索基盤との関係

FAISSでは、cosineを使う場合にベクトルを正規化して inner product として扱う考え方が一般的です。pgvectorも L2、inner product、cosine などをサポートします。

### 知らないと起きる失敗

登録時は正規化し、検索時は正規化しない。あるいはモデル更新後に旧ベクトルと新ベクトルを同じ空間で混ぜ、RAGの根拠文書が不安定になります。

### 学ぶべきキーワード

cosine similarity、dot product、L2、normalization、vector norm、metric space、curse of dimensionality。

## 近似最近傍探索、ANN

### 何を理解すべきか

ANNは、真の最近傍を必ず返す代わりに、十分近い候補を高速に返す技術です。評価は「速いか」だけでなく、recall@k、nDCG、MRR、p95/p99で見ます。

### なぜ実用システムで重要か

RAGではtop-kの中に正しいチャンクが入るかが回答品質を左右します。検索が速くても、必要な根拠が落ちるとLLMはもっともらしく誤答します。

### ベクトル検索・RAG・検索基盤との関係

FAISS、Milvus、Qdrant、Weaviate、pgvector、Elasticsearch/OpenSearch はANNの実装やチューニング方針が違います。recall-QPS のトレードオフを実データで測る必要があります。

### 知らないと起きる失敗

平均レイテンシだけ見てHNSWの `efSearch` を下げすぎ、検索品質が落ちたことをプロンプトの問題と誤認します。

### 学ぶべきキーワード

ANN、recall@k、efSearch、nprobe、reranking、candidate set、ground truth exact search。

## インデックス構造

### 何を理解すべきか

インデックスは「検索を速くする魔法」ではなく、事前計算した補助構造です。その代わりにメモリ、構築時間、更新コスト、近似誤差を払います。

### なぜ実用システムで重要か

本番では検索だけでなく、追加、削除、再構築、バージョン切り替えが発生します。インデックスが大きいほど、障害復旧と再構築が運用イベントになります。

### ベクトル検索・RAG・検索基盤との関係

pgvectorはHNSWとIVFFlatを持ちます。Milvusは多様なindexを持ち、QdrantはHNSW中心、WeaviateはHNSW/Flat/Dynamic、ElasticはHNSWや量子化を統合しています。

### 知らないと起きる失敗

インデックス再構築中に検索停止が必要になり、埋め込みモデル更新ができなくなります。

### 学ぶべきキーワード

HNSW、IVF、PQ、SQ、DiskANN、Flat、segment、reindex、blue-green index。

## データベース基礎

### 何を理解すべきか

DBは単なる保存場所ではなく、クエリ最適化、トランザクション、インデックス、バックアップ、権限、レプリケーションを提供します。

### なぜ実用システムで重要か

ベクトルDBだけでは、業務データの正本、JOIN、権限、監査、履歴管理が不足することがあります。一方、RDBだけでは大規模ANNに弱い場合があります。

### ベクトル検索・RAG・検索基盤との関係

pgvectorは「正本DBに近い場所で検索できる」のが強みです。専用ベクトルDBは検索を独立スケールさせるのが強みです。Elasticsearch/OpenSearchは検索・集計・全文検索が強いですが、RDBの代替ではありません。

### 知らないと起きる失敗

ベクトルDBを正本DBとして扱い、業務更新、監査、復旧、整合性要件で詰まります。

### 学ぶべきキーワード

query planner、index scan、sequential scan、JOIN、ACID、backup、PITR、replication。

## トランザクションと整合性

### 何を理解すべきか

強整合性、結果整合性、read-after-write、一貫したスナップショットの違いを理解する必要があります。

### なぜ実用システムで重要か

RAGでは文書更新後に古いチャンクが残る、削除した文書が検索に出る、権限変更が遅れて反映される、といった事故が起きます。

### ベクトル検索・RAG・検索基盤との関係

PostgreSQLはトランザクションと整合性が強いです。専用ベクトルDBや検索エンジンでは、更新反映、refresh、replica同期、indexing lag を個別に設計します。

### 知らないと起きる失敗

「削除APIが成功した」ことと「検索結果から確実に消えた」ことを同一視します。

### 学ぶべきキーワード

ACID、eventual consistency、read-after-write、WAL、snapshot isolation、refresh lag、idempotency。

## ストレージエンジン

### 何を理解すべきか

データがメモリ、SSD、オブジェクトストレージ、WAL、セグメント、LSM-treeのどこにあり、どう書かれ、どう読まれるかを理解します。

### なぜ実用システムで重要か

ベクトル検索はメモリ帯域とI/Oに強く依存します。HNSWはメモリ常駐で強い一方、巨大化するとメモリ費用が支配的です。

### ベクトル検索・RAG・検索基盤との関係

Milvusは大規模向けにストレージと計算の分離を意識します。Elasticsearch/OpenSearchはLuceneセグメント、Qdrantはセグメントとpayload index、Postgresはheap/index/VACUUMの制約を持ちます。

### 知らないと起きる失敗

メモリに乗っていたPoC結果をもとに本番設計し、実データではSSDアクセスが混ざってp99が悪化します。

### 学ぶべきキーワード

WAL、segment、compaction、mmap、page cache、SSD random read、write amplification、VACUUM。

## OS・メモリ階層・キャッシュ

### 何を理解すべきか

CPUレジスタ、L1/L2/L3キャッシュ、RAM、SSD、ネットワークストレージの速度差を理解します。

### なぜ実用システムで重要か

高次元ベクトル検索はCPU演算だけでなく、メモリから大量のfloatを読むコストが効きます。PQや量子化はメモリ帯域を減らすための技術でもあります。

### ベクトル検索・RAG・検索基盤との関係

HNSWはリンクをたどるためランダムアクセスが増えます。IVFは候補リストを局所化できます。PQはベクトル表現を短くし、キャッシュ効率を上げます。

### 知らないと起きる失敗

CPUコア数だけ増やしても、メモリ帯域が詰まりQPSが伸びません。

### 学ぶべきキーワード

CPU cache、page cache、NUMA、memory bandwidth、cache locality、mmap、prefetch。

## CPU/GPU・SIMD・並列計算

### 何を理解すべきか

距離計算はベクトル演算なのでSIMDやGPUで高速化できます。ただし、GPUはデータ転送、バッチサイズ、更新頻度が効きます。

### なぜ実用システムで重要か

バッチ検索や巨大インデックス構築ではGPUが効く場合がありますが、低QPS・小バッチ・頻繁更新ではCPUの方が扱いやすい場合もあります。

### ベクトル検索・RAG・検索基盤との関係

FAISSはGPU対応が強みです。Milvus系はGPU/大規模検索の選択肢を持ちます。RedisやElastic系はCPU/SIMD/量子化で高速化する方向もあります。

### 知らないと起きる失敗

GPUを入れたのに、PCIe転送や小バッチで効果が出ません。

### 学ぶべきキーワード

SIMD、AVX、NEON、CUDA、batching、memory coalescing、CPU-GPU transfer。

## ネットワーク

### 何を理解すべきか

分散検索では、クエリが複数ノードへ飛び、結果を集約します。ネットワーク往復、シリアライズ、TLS、ロードバランサがレイテンシに入ります。

### なぜ実用システムで重要か

単一ノードでは速くても、シャードが増えると最も遅いシャードが全体のp99を決めます。

### ベクトル検索・RAG・検索基盤との関係

専用ベクトルDBを別サービスにすると、アプリDB内検索よりネットワークコストが増えます。一方で検索負荷を独立スケールできます。

### 知らないと起きる失敗

ローカルFAISSの速度を、そのままリモートDB検索の速度と見なします。

### 学ぶべきキーワード

RPC、gRPC、REST、TLS、scatter-gather、load balancing、timeout、retry。

## 分散システム

### 何を理解すべきか

シャーディング、レプリケーション、リーダー選出、合意形成、部分障害、バックプレッシャーを理解します。

### なぜ実用システムで重要か

1億件規模では単一ノードに収まらず、分散検索になります。分散すると、速さだけでなく障害時の挙動が設計対象になります。

### ベクトル検索・RAG・検索基盤との関係

Qdrantは分散デプロイ、シャーディング、レプリケーションを持ちます。Milvusは分散・クラウドネイティブ構成が前提になりやすいです。Elasticsearch/OpenSearchはシャードとレプリカ設計が中核です。

### 知らないと起きる失敗

シャード数を増やせば無限に速くなると思い、scatter-gatherとtail latencyで逆に遅くなります。

### 学ぶべきキーワード

shard、replica、coordinator、consensus、Raft、quorum、partial failure、backpressure。

## スケーラビリティ

### 何を理解すべきか

スケールアップ、スケールアウト、水平分割、読み取りレプリカ、キャッシュ、非同期処理の使い分けを理解します。

### なぜ実用システムで重要か

検索件数、QPS、更新頻度、top-k、フィルタ条件、次元数が同時に増えると、どこか一つを増強しても足りません。

### ベクトル検索・RAG・検索基盤との関係

pgvectorは既存Postgresに載せやすいが、OLTP負荷と検索負荷が競合します。専用DBは検索を独立スケールしやすいが、同期と運用が増えます。

### 知らないと起きる失敗

DB CPUが詰まっているのにアプリサーバーだけ増やします。

### 学ぶべきキーワード

capacity planning、horizontal scaling、vertical scaling、hot shard、load shedding、autoscaling。

## 可用性・耐障害性

### 何を理解すべきか

障害は必ず起きます。ノード停止、インデックス破損、再構築失敗、レプリカ遅延、バックアップ不備を想定します。

### なぜ実用システムで重要か

RAG検索が落ちると、LLMは根拠なし回答をするか、サービス全体が止まります。縮退設計が必要です。

### ベクトル検索・RAG・検索基盤との関係

レプリカ、スナップショット、blue-green index、再構築手順、fallback検索が設計対象です。

### 知らないと起きる失敗

埋め込みモデル更新で全インデックスを再構築したら、戻せなくなります。

### 学ぶべきキーワード

HA、failover、backup/restore、snapshot、blue-green deployment、graceful degradation。

## レイテンシとスループット

### 何を理解すべきか

レイテンシは1リクエストの遅さ、スループットは単位時間に処理できる量です。両者はトレードオフします。

### なぜ実用システムで重要か

RAGでは検索、rerank、LLM生成が直列になりがちです。検索のp99が悪いと全体SLOが崩れます。

### ベクトル検索・RAG・検索基盤との関係

HNSWの `efSearch`、IVFの `nprobe`、top-k、フィルタ、rerank候補数が直接効きます。

### 知らないと起きる失敗

平均50msだけを見てリリースし、p99が2秒でユーザー体験が悪化します。

### 学ぶべきキーワード

p50、p95、p99、QPS、tail latency、timeout budget、SLO。

## キューイング理論

### 何を理解すべきか

利用率が高くなると、待ち時間は非線形に増えます。CPUやDBが80-90%に近づくと、少しの負荷増でp99が跳ねます。

### なぜ実用システムで重要か

検索は重い処理です。バーストや再インデックスと重なると、通常クエリが詰まります。

### ベクトル検索・RAG・検索基盤との関係

embedding生成、indexing、検索、rerankingを同じリソースで動かすと干渉します。キュー分離と優先度制御が必要です。

### 知らないと起きる失敗

バッチ取り込み中にオンライン検索が遅延し、障害扱いになります。

### 学ぶべきキーワード

Little's Law、utilization、queue depth、backpressure、rate limit、priority queue。

## キャッシュ戦略

### 何を理解すべきか

キャッシュは速くしますが、鮮度、権限、無効化が難しくなります。

### なぜ実用システムで重要か

RAGでは同じ質問、同じユーザー、同じ文書集合への検索が繰り返されます。一方、権限や文書更新があるため、キャッシュ漏洩が重大です。

### ベクトル検索・RAG・検索基盤との関係

Redis Vector Searchは低レイテンシな検索や短命なベクトル集合に向きます。検索結果キャッシュ、embedding cache、rerank cacheは別物です。

### 知らないと起きる失敗

tenant_idやACLをキーに含めず、別ユーザーの検索結果を返します。

### 学ぶべきキーワード

TTL、cache key、invalidation、negative cache、embedding cache、result cache。

## データモデリング

### 何を理解すべきか

RAGでは document、chunk、embedding、metadata、permission、version を分けて考えます。

### なぜ実用システムで重要か

検索品質はベクトルだけで決まりません。chunk粒度、タイトル、セクション、更新日時、権限、言語、source_uriが効きます。

### ベクトル検索・RAG・検索基盤との関係

pgvectorはRDBスキーマで管理しやすいです。Qdrant/Weaviate/Milvusはpayloadやcollection設計が重要です。Elasticsearch/OpenSearchはドキュメント構造とnested passage設計が効きます。

### 知らないと起きる失敗

chunk_idだけ保存し、元文書、バージョン、権限、削除状態を追えなくなります。

### 学ぶべきキーワード

document_id、chunk_id、tenant_id、ACL、content_hash、embedding_model_version、schema evolution。

## クラウドインフラ

### 何を理解すべきか

コンピュート、メモリ、SSD、ネットワーク、マネージドサービス、バックアップ、リージョン設計を理解します。

### なぜ実用システムで重要か

ベクトルDBはメモリ費用が大きくなりがちです。レプリカを増やすと可用性は上がりますが、コストも増えます。

### ベクトル検索・RAG・検索基盤との関係

小規模ならマネージドPostgres + pgvectorで十分な場合があります。大規模なら専用DBや検索エンジンを別クラスタに分けます。

### 知らないと起きる失敗

開発環境の小さなインスタンスで測り、productionではメモリ不足・IOPS不足・高額請求になります。

### 学ぶべきキーワード

instance sizing、IOPS、autoscaling、multi-AZ、managed service、egress cost、reserved capacity。

## 観測可能性、ログ、メトリクス、トレーシング

### 何を理解すべきか

CPUやメモリだけでなく、検索品質と検索失敗を観測します。

### なぜ実用システムで重要か

RAGの障害は500エラーだけではありません。「検索できるが悪い文書を返す」ことが品質障害です。

### ベクトル検索・RAG・検索基盤との関係

見るべきは、検索レイテンシ、top-k候補数、filter後候補数、empty result rate、recall regression、indexing lag、モデルバージョン別品質です。

### 知らないと起きる失敗

インフラは正常なのに、検索品質が落ちていることに気づけません。

### 学ぶべきキーワード

OpenTelemetry、trace、span、indexing lag、zero-result rate、recall drift、query log。

## セキュリティ

### 何を理解すべきか

検索結果は情報漏洩経路です。ベクトルも元文書の情報を含む派生データとして扱います。

### なぜ実用システムで重要か

RAGは「ユーザーが見る権限のない文書」を一部でもコンテキストに入れると事故になります。

### ベクトル検索・RAG・検索基盤との関係

ACLを検索前に適用できるか、少なくともANN探索中に安全に制約できるかが重要です。検索後フィルタだけではtop-k不足と漏洩リスクが残ります。

### 知らないと起きる失敗

検索後に権限フィルタをかける設計で、候補不足時に不適切なfallbackが走ります。

### 学ぶべきキーワード

tenant isolation、document-level ACL、encryption、audit log、PII、right to be forgotten。

## コスト設計

### 何を理解すべきか

コストは件数、次元数、float精度、インデックス、レプリカ、QPS、再構築頻度、rerank候補数で決まります。

### なぜ実用システムで重要か

1536次元float32は1ベクトル約6KBです。1億件なら生ベクトルだけで約614GB、ここにインデックス、メタデータ、レプリカが乗ります。

### ベクトル検索・RAG・検索基盤との関係

PQ、SQ、binary quantization、DiskANN系、Elasticの量子化、Qdrantの量子化などは、メモリ・I/O・精度の交換です。

### 知らないと起きる失敗

精度向上のために高次元モデルへ切り替えたら、メモリ費用と再構築時間が倍増します。

### 学ぶべきキーワード

TCO、memory footprint、replication factor、quantization、reindex cost、embedding cost。

## MLOps / LLMOps / RAGOps

### 何を理解すべきか

RAGでは、モデル、chunking、正規化、距離関数、index type、prompt、reranker、データ版をまとめて管理します。

### なぜ実用システムで重要か

どれか一つを変えるだけで検索品質が変わります。再現性がないと障害解析できません。

### ベクトル検索・RAG・検索基盤との関係

embedding_model_version、chunk_version、index_version、distance_metric、normalization_policyを記録します。

### 知らないと起きる失敗

モデルを更新したが旧ベクトルが残り、検索空間が混ざります。

### 学ぶべきキーワード

model registry、dataset versioning、index versioning、offline eval、online eval、rollback。

## 評価指標とベンチマーク設計

### 何を理解すべきか

検索品質は主観ではなく、評価クエリと正解ラベルで測ります。ANNはexact searchをground truthにしてrecall@kを測ります。

### なぜ実用システムで重要か

「速いが悪い検索」と「遅いが良い検索」のどちらを選ぶかは、評価なしには判断できません。

### ベクトル検索・RAG・検索基盤との関係

ANN-BenchmarksはrecallとQPSのトレードオフを見る考え方を示します。BEIRのようなIRベンチマークは検索品質評価の参考になります。

### 知らないと起きる失敗

デモで数問試しただけで採用し、本番クエリで失敗します。

### 学ぶべきキーワード

recall@k、precision@k、MRR、nDCG、hit rate、golden query set、A/B test。

