# Bing システム設計

## 1. システム概要

### 目的と主要機能

Bingは、Microsoftが提供する検索エンジンです。Web検索、画像検索、動画検索、ニュース検索などの機能を提供します。

**主要機能**:
- Web検索
- 画像検索
- 動画検索
- ニュース検索
- 地図検索
- 翻訳機能
- AI検索（ChatGPT統合）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約13億人
- **日間アクティブユーザー（DAU）**: 約5億人
- **1日の検索クエリ数**: 約50億クエリ
- **1秒あたりの検索クエリ数**: 約60,000クエリ/秒（ピーク時）

### 主要なユースケース

1. **Web検索**: ユーザーがWebページを検索
2. **画像検索**: ユーザーが画像を検索
3. **動画検索**: ユーザーが動画を検索
4. **ニュース検索**: ユーザーがニュースを検索
5. **AI検索**: ChatGPT統合による対話型検索

## 2. 機能要件

### コア機能

1. **検索機能**
   - Web検索
   - 画像検索
   - 動画検索
   - ニュース検索
   - 地図検索

2. **ランキング**
   - 検索結果のランキング
   - パーソナライズされた検索結果
   - 地域ベースの検索結果

3. **AI検索**
   - ChatGPT統合
   - 対話型検索
   - 自然言語処理

4. **広告**
   - 検索広告の表示
   - 広告のターゲティング

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 検索結果は最終的に一貫性を保つ
- **パフォーマンス**:
  - 検索結果表示: < 500ms
  - 画像検索: < 1秒
  - AI検索: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 検索インデックスは永続的に保存

### 優先順位付け

1. **P0（必須）**: Web検索、画像検索、ランキング
2. **P1（重要）**: 動画検索、ニュース検索、AI検索
3. **P2（望ましい）**: パーソナライゼーション、高度な検索機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer (NGINX/HAProxy)       │
└──────┬──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
│  API Gateway│   │  API Gateway│   │  API Gateway│
│  (Region 1) │   │  (Region 2) │   │  (Region 3) │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       ├─────────────────┴──────────────────┤
       │                                     │
┌──────▼─────────────────────────────────────▼──────┐
│              Application Servers                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Web      │  │  Image   │  │  Video   │        │
│  │ Search   │  │ Search   │  │ Search   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Ranking Service                 │         │
│  │      AI Search Service               │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┐
        │                 │                  │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│   Database   │  │   Cache       │  │  Message     │
│   (Sharded)  │  │   (Redis)     │  │  Queue       │
│              │  │               │  │  (Kafka)     │
└───────┬──────┘  └───────────────┘  └──────────────┘
        │
        │
┌───────▼──────────────────────────────────────────┐
│         Search Index (Elasticsearch)              │
│         Image Index                                │
│         Video Index                                │
│         CDN (CloudFront/Cloudflare)                │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Web Search Service**: Web検索の処理
   - **Image Search Service**: 画像検索の処理
   - **Video Search Service**: 動画検索の処理
   - **Ranking Service**: 検索結果のランキング
   - **AI Search Service**: AI検索の処理（ChatGPT統合）
4. **Database**: 検索履歴、ユーザー設定の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（検索インデックス更新など）
7. **Search Index**: Webページ、画像、動画の検索インデックス
8. **CDN**: 画像、動画の配信

### データフロー

#### Web検索のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Web Search Service
3. Web Search Service:
   a. クエリを解析・正規化
   b. Cacheから検索結果を取得（キャッシュヒット時）
   c. キャッシュミス時: Search Indexから検索
   d. Ranking Serviceでランキング
   e. 検索結果を返す
   f. Cacheに保存
```

## 4. データモデル設計

### 主要なエンティティ

#### Search_Queries テーブル

```sql
CREATE TABLE search_queries (
    query_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    query_text VARCHAR(500) NOT NULL,
    search_type ENUM('web', 'image', 'video', 'news') NOT NULL,
    result_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id_created (user_id, created_at DESC),
    INDEX idx_query_text (query_text),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Search_Results テーブル

```sql
CREATE TABLE search_results (
    result_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    query_id BIGINT NOT NULL,
    url VARCHAR(500) NOT NULL,
    title VARCHAR(200),
    snippet TEXT,
    rank_position INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES search_queries(query_id),
    INDEX idx_query_id_rank (query_id, rank_position)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 検索履歴、ユーザー設定の永続化
- **Elasticsearch**:
  - 理由: 全文検索、大規模な検索インデックス
  - 用途: Webページ、画像、動画の検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `search_queries`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 検索履歴は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### Web検索

```
GET /api/v1/search/web?q=hello+world&limit=10
Authorization: Bearer <token>

Response (200 OK):
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "snippet": "This is an example...",
      "rank": 1
    }
  ],
  "total_results": 1000000
}
```

#### 画像検索

```
GET /api/v1/search/image?q=cat&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "images": [
    {
      "url": "https://example.com/image.jpg",
      "thumbnail_url": "https://example.com/thumb.jpg",
      "title": "Cat Image"
    }
  ],
  "total_results": 50000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT（オプション）
- **認可**: パブリックAPI、認証不要
- **レート制限**: 
  - 検索: 100リクエスト/分（認証ユーザー）
  - 検索: 10リクエスト/分（未認証ユーザー）

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 4 == 0
Shard 2: user_id % 4 == 1
Shard 3: user_id % 4 == 2
Shard 4: user_id % 4 == 3
```

**シャーディングキー**: `user_id`
- 検索履歴は`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 画像、動画をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 検索結果、人気検索クエリ
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像、動画
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **検索インデックス**: Elasticsearchクエリの最適化
2. **ランキング**: ランキングアルゴリズムの最適化
3. **AI検索**: ChatGPT API呼び出しのレイテンシ

### CDNの活用

- **画像・動画**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 検索最適化

1. **キャッシング**: 人気検索クエリの結果をキャッシュ
2. **インデックス最適化**: Elasticsearchインデックスの最適化
3. **並列検索**: 複数の検索タイプを並列で実行

### 非同期処理

#### メッセージキュー（Kafka）

1. **検索インデックス更新**:
   ```
   Topic: index-update
   Partition Key: document_id
   ```

2. **検索履歴記録**:
   ```
   Topic: search-history
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 13億人
- **日間アクティブユーザー**: 5億人
- **1日の検索クエリ数**: 50億クエリ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 2,000台（リージョン間で分散）
- コスト: $0.192/時間 × 2,000台 × 730時間 = **$280,320/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 100台（マスター + レプリカ）
- コスト: $0.76/時間 × 100台 × 730時間 = **$55,480/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 200台
- コスト: $0.175/時間 × 200台 × 730時間 = **$25,550/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 100台
- コスト: $0.76/時間 × 100台 × 730時間 = **$55,480/月**

**ストレージ**:
- EBS: 500 TB
- コスト: $0.10/GB/月 × 500,000 GB = **$50,000/月**

**ネットワーク**:
- データ転送: 5 PB/月
- コスト: $0.09/GB × 5,000,000 GB = **$450,000/月**

**合計**: 約 **$916,830/月**（約11,001,960ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **キャッシング**: 検索結果のキャッシングでコスト削減
5. **CDN活用**: データ転送コストを削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Elasticsearchクラスターのヘルスチェック

3. **サーキットブレーカー**:
   - 障害が発生したサービスへのリクエストを遮断
   - フォールバック処理を実装

### 冗長化戦略

#### データベース冗長化

- **マスター-レプリカ構成**: 1つのマスター、複数のレプリカ
- **自動フェイルオーバー**: マスター障害時にレプリカを昇格
- **マルチリージョン**: 地理的に分散したレプリカ

### バックアップ・復旧戦略

1. **データベースバックアップ**:
   - 日次フルバックアップ
   - 継続的なバックアップ（ポイントインタイムリカバリ）
   - バックアップの保存期間: 30日

2. **検索インデックスバックアップ**:
   - Elasticsearchスナップショット
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT（オプション）
   - Microsoft Account統合

2. **認可**:
   - パブリックAPI、認証不要
   - 認証ユーザーには追加機能を提供

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - ユーザーベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **検索結果表示**: < 500ms
- **画像検索**: < 1秒

### プログレッシブローディング

1. **検索結果の遅延読み込み**:
   - 最初の10件を先に表示
   - 残りの結果はスクロール時に読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - サムネイルを先に表示

## 12. 実装例

### 検索サービス（疑似コード）

```python
class WebSearchService:
    def __init__(self, search_index, cache, ranking_service):
        self.search_index = search_index
        self.cache = cache
        self.ranking_service = ranking_service
    
    async def search(self, query: str, limit: int = 10):
        # キャッシュから取得を試みる
        cache_key = f"search:{query}:{limit}"
        cached_results = await self.cache.get(cache_key)
        
        if cached_results:
            return cached_results
        
        # 検索インデックスから検索
        raw_results = await self.search_index.search(
            query=query,
            limit=limit * 2  # ランキング用に多めに取得
        )
        
        # ランキング
        ranked_results = await self.ranking_service.rank(
            query=query,
            results=raw_results,
            limit=limit
        )
        
        # キャッシュに保存
        await self.cache.set(cache_key, ranked_results, ttl=300)
        
        return ranked_results
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の検索クエリ数**: 50億クエリ
- **1時間あたり**: 50億 / 24 = 約2.08億クエリ
- **1秒あたり**: 2.08億 / 3600 = 約57,778クエリ/秒
- **ピーク時（3倍）**: 約173,334クエリ/秒

### ストレージ見積もり

#### 検索インデックスストレージ

- **Webページ数**: 1兆ページ
- **1ページあたりのインデックスサイズ**: 約10 KB
- **合計インデックスサイズ**: 1兆 × 10 KB = 10 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **キャッシング**: 人気検索クエリの結果をキャッシュ
4. **検索インデックス**: Elasticsearchで全文検索を実装
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

2. **ランキングの複雑さ**:
   - 問題: ランキングアルゴリズムが遅い
   - 解決策: 事前計算とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Google検索](google_search_design.md) - 検索エンジン
- [DuckDuckGo](duckduckgo_design.md) - プライバシー重視の検索エンジン

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Search Index](../17_common_patterns/database_sharding.md) - 検索インデックス

---

**次のステップ**: [DuckDuckGo](duckduckgo_design.md)でプライバシー重視の検索エンジンの設計を学ぶ

