# Medium システム設計

## 1. システム概要

### 目的と主要機能

Mediumは、長文コンテンツの公開・共有プラットフォームです。執筆者と読者を結び、高品質な記事を提供します。

**主要機能**:
- 記事の公開・編集
- 記事の閲覧
- フォロー機能
- おすすめ記事
- コメント機能
- ハイライト・ブックマーク
- タグ・トピック

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1億人
- **日間アクティブユーザー（DAU）**: 約3,000万人
- **1日の記事閲覧数**: 約5,000万回
- **1日の記事投稿数**: 約10万記事
- **1秒あたりのリクエスト数**: 約8,000リクエスト/秒（ピーク時）
- **記事総数**: 約5,000万記事

### 主要なユースケース

1. **記事投稿**: 執筆者が記事を投稿
2. **記事閲覧**: 読者が記事を閲覧
3. **フォロー**: ユーザーが執筆者をフォロー
4. **おすすめ記事**: ユーザーに記事を推薦
5. **コメント**: ユーザーが記事にコメント

## 2. 機能要件

### コア機能

1. **記事管理**
   - 記事の作成・編集・削除
   - マークダウンエディタ
   - 画像・動画の埋め込み

2. **記事閲覧**
   - 記事の表示
   - 読み取り時間の推定
   - 関連記事の推薦

3. **フォロー機能**
   - 執筆者のフォロー
   - フォローフィード

4. **おすすめ記事**
   - パーソナライズされた記事推薦
   - トピックベースの推薦

5. **コメント機能**
   - 記事へのコメント
   - コメントへの返信

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 記事は強い一貫性、コメントは最終的に一貫性を保つ
- **パフォーマンス**:
  - 記事表示: < 2秒
  - 記事検索: < 1秒
  - おすすめ記事生成: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 記事は永続的に保存

### 優先順位付け

1. **P0（必須）**: 記事投稿・閲覧、検索、フォロー機能
2. **P1（重要）**: おすすめ記事、コメント機能
3. **P2（望ましい）**: ハイライト・ブックマーク、高度な検索

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
│  │ Article  │  │  Feed    │  │  Search  │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Recommendation Service          │         │
│  │      Comment Service                 │         │
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
│         Object Storage (S3)                       │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Article Service**: 記事の管理
   - **Feed Service**: フィードの生成
   - **Search Service**: 記事検索の処理
   - **Recommendation Service**: おすすめ記事の生成
   - **Comment Service**: コメントの管理
4. **Database**: 記事、ユーザー、コメントの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（おすすめ記事生成など）
7. **Search Index**: 記事検索インデックス
8. **Object Storage**: 画像の保存
9. **CDN**: 画像の配信

### データフロー

#### 記事投稿のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Article Service
3. Article Service:
   a. 記事をデータベースに保存
   b. Message Queueに検索インデックス更新を依頼
   c. フォロワーに通知を送信（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Articles テーブル

```sql
CREATE TABLE articles (
    article_id BIGINT PRIMARY KEY,
    author_id BIGINT NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    reading_time INT,
    view_count BIGINT DEFAULT 0,
    clap_count BIGINT DEFAULT 0,
    status ENUM('draft', 'published') DEFAULT 'draft',
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(user_id),
    INDEX idx_author_id (author_id),
    INDEX idx_published_at (published_at DESC),
    INDEX idx_status (status),
    FULLTEXT INDEX idx_title_content (title, content)
) ENGINE=InnoDB;
```

#### Follows テーブル

```sql
CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    following_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (following_id) REFERENCES users(user_id),
    INDEX idx_follower_id (follower_id),
    INDEX idx_following_id (following_id)
) ENGINE=InnoDB;
```

#### Comments テーブル

```sql
CREATE TABLE comments (
    comment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    article_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    parent_comment_id BIGINT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(article_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id),
    INDEX idx_article_id (article_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 記事、ユーザー、コメントの永続化
- **Elasticsearch**:
  - 理由: 全文検索、記事検索
  - 用途: 検索インデックス
- **Object Storage（S3）**:
  - 理由: 画像ストレージ
  - 用途: 画像の保存

### スキーマ設計の考慮事項

1. **パーティショニング**: `articles`テーブルは`author_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 記事は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 記事投稿

```
POST /api/v1/articles
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Article Title",
  "content": "Article content...",
  "tags": ["technology", "programming"]
}

Response (200 OK):
{
  "article_id": 1234567890,
  "title": "Article Title",
  "status": "published",
  "published_at": "2024-01-15T10:30:00Z"
}
```

#### 記事検索

```
GET /api/v1/articles/search?q=programming&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "articles": [
    {
      "article_id": 1234567890,
      "title": "Article Title",
      "author": "Author Name",
      "excerpt": "Article excerpt...",
      "reading_time": 5
    }
  ],
  "total_results": 1000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の記事のみ編集可能
- **レート制限**: 
  - 記事投稿: 10記事/日
  - 記事検索: 100リクエスト/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Author IDベースのシャーディング

```
Shard 1: author_id % 8 == 0
Shard 2: author_id % 8 == 1
...
Shard 8: author_id % 8 == 7
```

**シャーディングキー**: `author_id`
- 記事は`author_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 画像をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 記事メタデータ、フィード、人気記事
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **記事検索**: Elasticsearchクエリの最適化
2. **フィード生成**: フォローフィードの生成
3. **おすすめ記事**: 機械学習モデルの推論

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### フィード生成最適化

1. **事前計算**: フィードを事前計算してキャッシュ
2. **キャッシング**: 人気フィードをキャッシュ
3. **並列処理**: 複数のフィードを並列で生成

### 非同期処理

#### メッセージキュー（Kafka）

1. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: article_id
   ```

2. **おすすめ記事生成**:
   ```
   Topic: recommendation-generation
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1億人
- **日間アクティブユーザー**: 3,000万人
- **1日の記事閲覧数**: 5,000万回
- **1日の記事投稿数**: 10万記事

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 400台（リージョン間で分散）
- コスト: $0.192/時間 × 400台 × 730時間 = **$56,064/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台（マスター + レプリカ）
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ（S3）**:
- 画像ストレージ: 10 PB
- コスト: $0.023/GB/月 × 10,000,000 GB = **$230,000/月**

**ネットワーク**:
- データ転送: 2 PB/月
- コスト: $0.09/GB × 2,000,000 GB = **$180,000/月**

**合計**: 約 **$501,469/月**（約6,017,628ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - データベースの接続チェック

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

2. **記事バックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の記事のみ編集可能

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
- **記事表示**: < 2秒
- **記事検索**: < 1秒

### プログレッシブローディング

1. **記事の遅延読み込み**:
   - 記事の本文を遅延読み込み
   - サムネイルを先に表示

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - サムネイルを先に表示

## 12. 実装例

### 記事サービス（疑似コード）

```python
class ArticleService:
    def __init__(self, db, cache, search_service, message_queue):
        self.db = db
        self.cache = cache
        self.search_service = search_service
        self.message_queue = message_queue
    
    async def publish_article(self, author_id: int, title: str, content: str, tags: list):
        # 読み取り時間を推定
        reading_time = self.estimate_reading_time(content)
        
        # 記事をデータベースに保存
        article_id = await self.db.insert_article(
            author_id=author_id,
            title=title,
            content=content,
            reading_time=reading_time,
            status='published',
            published_at=datetime.now()
        )
        
        # 検索インデックス更新を依頼（非同期）
        await self.message_queue.publish(
            topic="search-index-update",
            message={
                "article_id": article_id,
                "title": title,
                "content": content,
                "tags": tags
            },
            partition_key=article_id
        )
        
        # フォロワーに通知を送信（非同期）
        await self.message_queue.publish(
            topic="article-notifications",
            message={
                "article_id": article_id,
                "author_id": author_id
            },
            partition_key=author_id
        )
        
        return {
            "article_id": article_id,
            "status": "published",
            "reading_time": reading_time
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の記事閲覧数**: 5,000万回
- **1時間あたり**: 5,000万 / 24 = 約208万回
- **1秒あたり**: 208万 / 3600 = 約578回/秒
- **ピーク時（3倍）**: 約1,734回/秒

#### 書き込みトラフィック

- **1日の記事投稿数**: 10万記事
- **1時間あたり**: 10万 / 24 = 約4,167記事
- **1秒あたり**: 4,167 / 3600 = 約1.16記事/秒
- **ピーク時（3倍）**: 約3.48記事/秒

### ストレージ見積もり

#### 記事ストレージ

- **1記事あたりの平均サイズ**: 約50 KB
- **記事総数**: 5,000万記事
- **合計ストレージ**: 5,000万 × 50 KB = 2.5 TB
- **1年のストレージ**: 2.5 TB + (10万記事/日 × 50 KB × 365日) = 約4.325 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **全文検索**: Elasticsearchで全文検索を実装
4. **キャッシング**: 人気記事を積極的にキャッシュ
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **フィード生成のスケーラビリティ**:
   - 問題: フォローフィードの生成が遅い
   - 解決策: 事前計算とキャッシング

2. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Reddit](reddit_design.md) - ソーシャルニュースプラットフォーム
- [Quora](quora_design.md) - Q&Aプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Quora](quora_design.md)でQ&Aプラットフォームの設計を学ぶ

