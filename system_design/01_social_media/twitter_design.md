# Twitter システム設計

## 1. システム概要

### 目的と主要機能

Twitterは、ユーザーが短いメッセージ（ツイート）を投稿し、他のユーザーをフォローしてタイムラインを閲覧できるマイクロブログプラットフォームです。

**主要機能**:
- ツイートの投稿（最大280文字）
- ユーザーのフォロー/アンフォロー
- タイムラインの表示（ホームタイムライン、ユーザータイムライン）
- リツイート、いいね、リプライ
- トレンドトピックの表示
- 検索機能

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3.3億人
- **日間アクティブユーザー（DAU）**: 約1.4億人
- **1日のツイート数**: 約5億ツイート
- **1秒あたりのツイート数**: 約6,000ツイート/秒（ピーク時）
- **1日のタイムライン読み込み**: 約150億回

### 主要なユースケース

1. **ツイート投稿**: ユーザーがツイートを投稿
2. **タイムライン閲覧**: フォローしているユーザーのツイートを時系列で表示
3. **検索**: キーワードでツイートを検索
4. **トレンド表示**: 人気のトピックを表示

## 2. 機能要件

### コア機能

1. **ユーザー管理**
   - ユーザー登録・ログイン
   - プロフィール管理
   - フォロー/アンフォロー

2. **ツイート機能**
   - ツイート投稿
   - リツイート
   - いいね
   - リプライ

3. **タイムライン**
   - ホームタイムライン（フォローしているユーザーのツイート）
   - ユーザータイムライン（特定ユーザーのツイート）

4. **検索**
   - リアルタイム検索
   - トレンドトピック

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: タイムラインは最終的に一貫性を保つ（Eventual Consistency）
- **パフォーマンス**:
  - ツイート投稿: < 200ms
  - タイムライン読み込み: < 500ms
  - 検索: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ツイートは永続的に保存

### 優先順位付け

1. **P0（必須）**: ツイート投稿、タイムライン表示、ユーザー認証
2. **P1（重要）**: 検索、リツイート、いいね
3. **P2（望ましい）**: トレンド、通知、メディア添付

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
│  │ Tweet    │  │ Timeline │  │ Search   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      User Service                    │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┐
        │                 │                  │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│   Database   │  │   Cache       │  │  Message     │
│   (Sharded)  │  │   (Redis)     │  │  Queue       │
│              │  │               │  │  (Kafka)     │
└──────────────┘  └───────────────┘  └──────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Tweet Service**: ツイートの投稿と取得
   - **Timeline Service**: タイムラインの生成
   - **Search Service**: ツイートの検索
   - **User Service**: ユーザー管理とフォロー関係
4. **Database**: ツイート、ユーザー、フォロー関係の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（タイムライン更新など）

### データフロー

#### ツイート投稿のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Tweet Service
3. Tweet Service:
   a. データベースにツイートを保存
   b. Message Queueにイベントを送信
   c. Cacheに最新ツイートを保存
4. Timeline Service（非同期）:
   a. Message Queueからイベントを受信
   b. フォロワーのタイムラインを更新
```

#### タイムライン読み込みのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Timeline Service
3. Timeline Service:
   a. Cacheからタイムラインを取得（キャッシュヒット時）
   b. キャッシュミス時: データベースから取得してキャッシュに保存
4. Timeline Service → Client
```

## 4. データモデル設計

### 主要なエンティティ

#### Users テーブル

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(50),
    bio TEXT,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB;
```

#### Tweets テーブル

```sql
CREATE TABLE tweets (
    tweet_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content VARCHAR(280) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reply_to_tweet_id BIGINT,
    retweet_of_tweet_id BIGINT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (reply_to_tweet_id) REFERENCES tweets(tweet_id),
    FOREIGN KEY (retweet_of_tweet_id) REFERENCES tweets(tweet_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_content (content)
) ENGINE=InnoDB;
```

#### Follows テーブル

```sql
CREATE TABLE follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (followee_id) REFERENCES users(user_id),
    INDEX idx_followee_id (followee_id),
    INDEX idx_follower_id (follower_id)
) ENGINE=InnoDB;
```

#### Likes テーブル

```sql
CREATE TABLE likes (
    user_id BIGINT NOT NULL,
    tweet_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, tweet_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id),
    INDEX idx_tweet_id (tweet_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ユーザー、ツイート、フォロー関係の永続化
- **NoSQL（Cassandra）**:
  - 理由: タイムラインの書き込み負荷が高い、水平スケーリングが必要
  - 用途: タイムラインの保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `tweets`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **正規化**: データの整合性を保つため3NFまで正規化
4. **デノーマライゼーション**: パフォーマンスが必要な場合は適度にデノーマライズ

## 5. API設計

### 主要なAPIエンドポイント

#### ツイート投稿

```
POST /api/v1/tweets
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "content": "Hello, Twitter!",
  "reply_to_tweet_id": null
}

Response (201 Created):
{
  "tweet_id": 1234567890,
  "user_id": 987654321,
  "content": "Hello, Twitter!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### タイムライン取得

```
GET /api/v1/timeline/home?limit=20&since_id=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "tweets": [
    {
      "tweet_id": 1234567891,
      "user_id": 987654322,
      "username": "user2",
      "display_name": "User 2",
      "content": "Another tweet",
      "created_at": "2024-01-15T10:29:00Z",
      "likes_count": 10,
      "retweets_count": 5
    }
  ],
  "next_cursor": "1234567891"
}
```

#### ユーザータイムライン取得

```
GET /api/v1/users/{user_id}/tweets?limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "tweets": [...]
}
```

#### 検索

```
GET /api/v1/search?q=hello&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "tweets": [...],
  "total_results": 1000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のツイートのみ削除可能
- **レート制限**: 
  - ツイート投稿: 300ツイート/3時間
  - タイムライン読み込み: 15リクエスト/15分

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
- ツイートは`user_id`でシャーディング
- タイムラインは`follower_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 静的コンテンツ（画像、CSS、JS）をCDNで配信

### データベースシャーディングの詳細

#### シャーディングの課題と解決策

1. **課題**: フォロー関係のクエリが複雑
   - **解決策**: フォロー関係を専用のサービスで管理

2. **課題**: タイムライン生成が複雑
   - **解決策**: タイムラインを事前計算してキャッシュ

3. **課題**: シャード間のJOINが困難
   - **解決策**: アプリケーションレベルでJOINを実装

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: タイムライン、ユーザープロフィール
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 静的コンテンツ、メディアファイル
   - TTL: 1時間-1日

#### キャッシュ戦略

- **Write-Through**: 書き込み時にキャッシュも更新
- **Write-Behind**: 非同期でキャッシュを更新
- **Cache-Aside**: アプリケーションがキャッシュを管理

## 7. レイテンシ最適化

### ボトルネックの特定

1. **データベースクエリ**: JOINと集計が遅い
2. **タイムライン生成**: 複数のフォロー先からツイートを取得
3. **ネットワークレイテンシ**: 地理的に遠いサーバーへのアクセス

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: タイムラインをエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### キャッシング戦略の詳細

#### タイムラインキャッシング

```
Cache Key: timeline:{user_id}:{page}
TTL: 5分
更新: 新しいツイート投稿時にキャッシュを無効化
```

#### ユーザープロフィールキャッシング

```
Cache Key: user:{user_id}
TTL: 15分
更新: プロフィール更新時にキャッシュを無効化
```

### データベースクエリ最適化

1. **インデックス最適化**: 
   - `(user_id, created_at)`の複合インデックス
   - `created_at`の降順インデックス

2. **クエリ最適化**:
   - JOINの代わりにアプリケーションレベルのJOIN
   - LIMIT句で結果数を制限
   - ページネーションでカーソルベースのページング

3. **読み取りレプリカ**:
   - 読み取り専用クエリはレプリカにルーティング
   - 書き込みはマスターデータベースに

### 非同期処理

#### メッセージキュー（Kafka）

1. **ツイート投稿イベント**:
   ```
   Topic: tweet-created
   Partition Key: user_id
   ```

2. **タイムライン更新**:
   - 非同期でフォロワーのタイムラインを更新
   - バッチ処理で効率化

3. **通知送信**:
   - リプライ、いいね、リツイートの通知を非同期で送信

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3.3億人
- **日間アクティブユーザー**: 1.4億人
- **1日のツイート数**: 5億ツイート
- **1日のタイムライン読み込み**: 150億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 500台（リージョン間で分散）
- コスト: $0.192/時間 × 500台 × 730時間 = **$70,080/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台（マスター + レプリカ）
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 50台
- コスト: $0.175/時間 × 50台 × 730時間 = **$6,387.50/月**

**ストレージ**:
- EBS: 100 TB
- コスト: $0.10/GB/月 × 100,000 GB = **$10,000/月**

**ネットワーク**:
- データ転送: 500 TB/月
- コスト: $0.09/GB × 500,000 GB = **$45,000/月**

**合計**: 約 **$142,563/月**（約1,710,756ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減

### リソース使用量の最適化

1. **キャッシュヒット率**: 80%以上を目標
2. **データベース接続プール**: 適切なサイズに設定
3. **クエリ最適化**: スロークエリの削減
4. **不要なデータの削除**: 古いツイートのアーカイブ

### クラウドプロバイダーの選択

- **AWS**: 最も成熟したサービス、高い可用性
- **Azure**: エンタープライズ統合が強い
- **GCP**: データ分析と機械学習が強い

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

#### アプリケーション冗長化

- **複数のアベイラビリティゾーン**: 各リージョンで3つのAZに分散
- **ロードバランサー**: ヘルスチェックで異常なインスタンスを除外

### バックアップ・復旧戦略

1. **データベースバックアップ**:
   - 日次フルバックアップ
   - 継続的なバックアップ（ポイントインタイムリカバリ）
   - バックアップの保存期間: 30日

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 1時間
   - RPO（Recovery Point Objective）: 15分

3. **バックアップのテスト**: 月次で復旧テストを実施

### モニタリング・アラート

#### モニタリング指標

1. **アプリケーション**:
   - リクエストレート
   - エラーレート
   - レイテンシ（p50, p95, p99）

2. **データベース**:
   - 接続数
   - クエリパフォーマンス
   - レプリケーションラグ

3. **インフラ**:
   - CPU使用率
   - メモリ使用率
   - ディスクI/O

#### アラート設定

- **エラーレート**: 1%を超えた場合
- **レイテンシ**: p95が1秒を超えた場合
- **データベース接続**: 80%を超えた場合
- **ディスク使用率**: 85%を超えた場合

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のリソースのみアクセス可能

3. **セッション管理**:
   - セッショントークンの有効期限: 24時間
   - リフレッシュトークン: 30日

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - パスワード: bcryptでハッシュ化

3. **機密情報**: 
   - 環境変数で管理
   - AWS Secrets ManagerまたはHashiCorp Vault

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - ユーザーベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

### セキュリティベストプラクティス

1. **入力検証**: 全てのユーザー入力を検証
2. **SQLインジェクション対策**: プリペアドステートメント
3. **XSS対策**: 出力のエスケープ
4. **CSRF対策**: CSRFトークン
5. **セキュリティ監査**: 定期的なセキュリティ監査

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **FID（First Input Delay）**: < 100ms
- **CLS（Cumulative Layout Shift）**: < 0.1

### オフライン対応

1. **Service Worker**: 
   - オフライン時にキャッシュからコンテンツを提供
   - オンライン復帰時に同期

2. **オフラインキューイング**:
   - オフライン時のツイート投稿をキューに保存
   - オンライン復帰時に送信

### プログレッシブローディング

1. **無限スクロール**: 
   - ページネーションの代わりに無限スクロール
   - ビューポートに近づいたら次のページを読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - プレースホルダーを表示

3. **スケルトンスクリーン**:
   - コンテンツ読み込み中にスケルトンスクリーンを表示

### エラーハンドリング

1. **エラーメッセージ**: 
   - ユーザーフレンドリーなエラーメッセージ
   - 技術的な詳細は隠す

2. **リトライ**: 
   - 一時的なエラーは自動リトライ
   - 指数バックオフでリトライ間隔を調整

3. **フォールバック**:
   - サービスが利用できない場合のフォールバック処理

## 12. 実装例

### ツイート投稿サービス（疑似コード）

```python
class TweetService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def create_tweet(self, user_id: int, content: str):
        # バリデーション
        if len(content) > 280:
            raise ValueError("Tweet exceeds 280 characters")
        
        # データベースに保存
        tweet_id = await self.db.insert_tweet(
            user_id=user_id,
            content=content,
            created_at=datetime.utcnow()
        )
        
        # キャッシュに保存（最新ツイート）
        await self.cache.set(
            f"user:{user_id}:latest_tweet",
            tweet_id,
            ttl=300
        )
        
        # メッセージキューにイベントを送信
        await self.message_queue.publish(
            topic="tweet-created",
            message={
                "tweet_id": tweet_id,
                "user_id": user_id,
                "content": content,
                "created_at": datetime.utcnow().isoformat()
            }
        )
        
        return {
            "tweet_id": tweet_id,
            "user_id": user_id,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }
```

### タイムラインサービス（疑似コード）

```python
class TimelineService:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    async def get_home_timeline(self, user_id: int, limit: int = 20, cursor: str = None):
        # キャッシュから取得を試みる
        cache_key = f"timeline:{user_id}:{cursor or 'latest'}"
        cached_timeline = await self.cache.get(cache_key)
        
        if cached_timeline:
            return cached_timeline
        
        # フォローしているユーザーを取得
        followees = await self.db.get_followees(user_id)
        
        # フォローしているユーザーのツイートを取得
        tweets = await self.db.get_tweets_by_users(
            user_ids=[f["followee_id"] for f in followees],
            limit=limit,
            cursor=cursor
        )
        
        # ユーザー情報を取得して結合
        timeline = []
        for tweet in tweets:
            user = await self.db.get_user(tweet["user_id"])
            timeline.append({
                **tweet,
                "username": user["username"],
                "display_name": user["display_name"],
                "avatar_url": user["avatar_url"]
            })
        
        # キャッシュに保存
        await self.cache.set(cache_key, timeline, ttl=300)
        
        return timeline
```

### 設定例（Docker Compose）

```yaml
version: '3.8'

services:
  api:
    image: twitter-api:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/twitter
      - REDIS_URL=redis://redis:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - db
      - redis
      - kafka
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=twitter
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
    depends_on:
      - zookeeper
  
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181

volumes:
  postgres_data:
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のタイムライン読み込み**: 150億回
- **1時間あたり**: 150億 / 24 = 6.25億回
- **1秒あたり**: 6.25億 / 3600 = 約17.4万回/秒
- **ピーク時（3倍）**: 約52万回/秒

#### 書き込みトラフィック

- **1日のツイート数**: 5億ツイート
- **1時間あたり**: 5億 / 24 = 約2,083万ツイート
- **1秒あたり**: 2,083万 / 3600 = 約5,786ツイート/秒
- **ピーク時（3倍）**: 約17,358ツイート/秒

### ストレージ見積もり

#### ツイートストレージ

- **1ツイートあたりのサイズ**: 約500バイト（メタデータ含む）
- **1日のツイート数**: 5億ツイート
- **1日のストレージ**: 5億 × 500バイト = 250 GB
- **1年のストレージ**: 250 GB × 365 = 約91.25 TB
- **5年のストレージ**: 約456.25 TB

#### メディアストレージ

- **メディア付きツイートの割合**: 30%
- **1メディアあたりのサイズ**: 平均2 MB
- **1日のメディアストレージ**: 5億 × 0.3 × 2 MB = 300 TB
- **1年のメディアストレージ**: 300 TB × 365 = 約109,500 TB（約109.5 PB）

### 帯域幅見積もり

#### 読み取り帯域幅

- **1タイムラインあたりのサイズ**: 平均50 KB（20ツイート）
- **1秒あたりの読み取り**: 52万回/秒（ピーク時）
- **読み取り帯域幅**: 52万 × 50 KB = 26 GB/秒 = 約208 Gbps

#### 書き込み帯域幅

- **1ツイートあたりのサイズ**: 平均500バイト
- **1秒あたりの書き込み**: 17,358ツイート/秒（ピーク時）
- **書き込み帯域幅**: 17,358 × 500バイト = 約8.7 MB/秒 = 約70 Mbps

### コスト見積もり（詳細）

#### ストレージコスト

- **ツイートストレージ**: 456.25 TB × $0.023/GB/月 = **$10,493.75/月**
- **メディアストレージ**: 109.5 PB × $0.023/GB/月 = **$2,518,500/月**
- **合計ストレージコスト**: 約 **$2,528,994/月**

#### 帯域幅コスト

- **読み取り帯域幅**: 208 Gbps × $0.09/GB = **$18.72/秒** = **$48,384/月**
- **書き込み帯域幅**: 70 Mbps × $0.09/GB = **$0.0063/秒** = **$16.3/月**
- **合計帯域幅コスト**: 約 **$48,400/月**

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **キャッシュファースト**: 可能な限りキャッシュを活用
4. **段階的ロールアウト**: カナリアリリースで段階的に展開
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **N+1問題**: 
   - 問題: ループ内でクエリを実行
   - 解決策: バッチ読み込みまたはJOIN

2. **キャッシュ無効化のタイミング**:
   - 問題: キャッシュが古いデータを返す
   - 解決策: 書き込み時にキャッシュを無効化

3. **データベース接続のリーク**:
   - 問題: 接続が適切にクローズされない
   - 解決策: 接続プールと適切なリソース管理

4. **タイムライン生成の複雑さ**:
   - 問題: リアルタイムでタイムラインを生成すると遅い
   - 解決策: 事前計算とキャッシング

### パフォーマンスチューニング

1. **データベースクエリの最適化**:
   - EXPLAINでクエリプランを確認
   - インデックスの追加
   - 不要なJOINの削除

2. **キャッシュ戦略の最適化**:
   - キャッシュヒット率の監視
   - TTLの調整
   - キャッシュキーの最適化

3. **非同期処理の活用**:
   - 重い処理は非同期で実行
   - メッセージキューでデカップリング

## 15. 関連システム

### 類似システムへのリンク

- [Facebook](facebook_design.md) - より複雑なソーシャルネットワーク
- [Instagram](instagram_design.md) - メディア中心のソーシャルメディア
- [LinkedIn](linkedin_design.md) - プロフェッショナルネットワーク

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー
- [Rate Limiting](../17_common_patterns/rate_limiting.md) - レート制限

---

**次のステップ**: [Facebook](facebook_design.md)でより複雑なソーシャルネットワークの設計を学ぶ

