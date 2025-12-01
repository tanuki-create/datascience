# LinkedIn システム設計

## 1. システム概要

### 目的と主要機能

LinkedInは、プロフェッショナル向けのソーシャルネットワーキングプラットフォームです。ユーザーがプロフィールを作成し、他のプロフェッショナルとつながり、求人情報を検索・応募し、コンテンツを共有できます。

**主要機能**:
- プロフェッショナルプロフィールの作成・管理
- ネットワーク構築（接続、フォロー）
- フィード（ニュースフィード）の表示
- 求人検索・応募
- メッセージング（InMail）
- コンテンツ投稿（記事、投稿）
- グループ参加
- 学習コース（LinkedIn Learning）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約9.3億人
- **日間アクティブユーザー（DAU）**: 約3.1億人
- **1日の投稿数**: 約1億投稿
- **1秒あたりのリクエスト数**: 約50,000リクエスト/秒（ピーク時）
- **1日のフィード読み込み**: 約50億回

### 主要なユースケース

1. **プロフィール作成**: ユーザーがプロフェッショナルプロフィールを作成
2. **ネットワーク構築**: 他のユーザーと接続
3. **フィード閲覧**: 接続しているユーザーの投稿を表示
4. **求人検索**: キーワード、場所、業種で求人を検索
5. **メッセージング**: 他のユーザーにメッセージを送信

## 2. 機能要件

### コア機能

1. **ユーザー管理**
   - ユーザー登録・ログイン
   - プロフィール管理（職歴、学歴、スキル）
   - プロフィール検索

2. **ネットワーキング**
   - 接続リクエストの送信・承認
   - フォロー/アンフォロー
   - 接続の推奨

3. **フィード**
   - ニュースフィードの表示
   - 投稿の作成（テキスト、画像、記事）
   - いいね、コメント、シェア

4. **求人**
   - 求人検索
   - 求人応募
   - 求人保存

5. **メッセージング**
   - 1対1メッセージング
   - InMail（接続していないユーザーへのメッセージ）

### 非機能要件

- **可用性**: 99.95%以上（年間ダウンタイム < 4.38時間）
- **一貫性**: プロフィールは強い一貫性、フィードは最終的に一貫性を保つ
- **パフォーマンス**:
  - プロフィール読み込み: < 300ms
  - フィード読み込み: < 500ms
  - 求人検索: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: プロフィール、投稿、メッセージは永続的に保存

### 優先順位付け

1. **P0（必須）**: プロフィール作成、ネットワーク構築、フィード表示
2. **P1（重要）**: 求人検索、メッセージング、投稿
3. **P2（望ましい）**: グループ、学習コース、分析

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
│  │ Profile  │  │  Feed    │  │  Job     │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Network Service                │         │
│  │      Messaging Service              │         │
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
   - **Profile Service**: プロフィールの管理と検索
   - **Feed Service**: ニュースフィードの生成
   - **Job Service**: 求人の検索と管理
   - **Network Service**: 接続関係の管理
   - **Messaging Service**: メッセージング機能
4. **Database**: プロフィール、投稿、接続関係の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（フィード更新など）

### データフロー

#### プロフィール作成のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Profile Service
3. Profile Service:
   a. データベースにプロフィールを保存
   b. 検索インデックスを更新
   c. Cacheにプロフィールを保存
```

#### フィード読み込みのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Feed Service
3. Feed Service:
   a. Cacheからフィードを取得（キャッシュヒット時）
   b. キャッシュミス時: 接続しているユーザーの投稿を取得
   c. ランキングアルゴリズムでソート
   d. Cacheに保存
4. Feed Service → Client
```

## 4. データモデル設計

### 主要なエンティティ

#### Users テーブル

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    headline VARCHAR(200),
    location VARCHAR(100),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_location (location),
    INDEX idx_industry (industry)
) ENGINE=InnoDB;
```

#### Connections テーブル

```sql
CREATE TABLE connections (
    user_id_1 BIGINT NOT NULL,
    user_id_2 BIGINT NOT NULL,
    status ENUM('pending', 'accepted', 'blocked') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id_1, user_id_2),
    FOREIGN KEY (user_id_1) REFERENCES users(user_id),
    FOREIGN KEY (user_id_2) REFERENCES users(user_id),
    INDEX idx_user_id_1 (user_id_1),
    INDEX idx_user_id_2 (user_id_2),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Posts テーブル

```sql
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    post_type ENUM('text', 'image', 'article') DEFAULT 'text',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_content (content)
) ENGINE=InnoDB;
```

#### Jobs テーブル

```sql
CREATE TABLE jobs (
    job_id BIGINT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    location VARCHAR(100),
    job_type ENUM('full-time', 'part-time', 'contract', 'internship'),
    salary_min DECIMAL(10, 2),
    salary_max DECIMAL(10, 2),
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    INDEX idx_location (location),
    INDEX idx_job_type (job_type),
    INDEX idx_posted_at (posted_at DESC),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: プロフィール、接続関係、投稿の永続化
- **Elasticsearch**:
  - 理由: 全文検索、求人検索、プロフィール検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `posts`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **正規化**: データの整合性を保つため3NFまで正規化
4. **デノーマライゼーション**: パフォーマンスが必要な場合は適度にデノーマライズ

## 5. API設計

### 主要なAPIエンドポイント

#### プロフィール取得

```
GET /api/v1/users/{user_id}/profile
Authorization: Bearer <token>

Response (200 OK):
{
  "user_id": 1234567890,
  "first_name": "John",
  "last_name": "Doe",
  "headline": "Software Engineer at Tech Corp",
  "location": "San Francisco, CA",
  "industry": "Technology",
  "experience": [...],
  "education": [...],
  "skills": [...]
}
```

#### フィード取得

```
GET /api/v1/feed?limit=20&cursor=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "posts": [
    {
      "post_id": 1234567891,
      "user_id": 987654321,
      "content": "Excited to announce...",
      "created_at": "2024-01-15T10:30:00Z",
      "likes_count": 100,
      "comments_count": 20
    }
  ],
  "next_cursor": "1234567891"
}
```

#### 求人検索

```
GET /api/v1/jobs/search?q=software+engineer&location=san+francisco&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "jobs": [...],
  "total_results": 1000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のプロフィールのみ編集可能
- **レート制限**: 
  - プロフィール更新: 10回/時間
  - フィード読み込み: 30リクエスト/分
  - 求人検索: 100リクエスト/分

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
- プロフィールは`user_id`でシャーディング
- 投稿は`user_id`でシャーディング
- 接続関係は`user_id_1`と`user_id_2`の両方でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 静的コンテンツ（画像、CSS、JS）をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: フィード、プロフィール
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 静的コンテンツ、メディアファイル
   - TTL: 1時間-1日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **データベースクエリ**: JOINと集計が遅い
2. **フィード生成**: 複数の接続先から投稿を取得
3. **検索**: Elasticsearchクエリの最適化

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: フィードをエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

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

1. **投稿作成イベント**:
   ```
   Topic: post-created
   Partition Key: user_id
   ```

2. **フィード更新**:
   - 非同期で接続しているユーザーのフィードを更新
   - バッチ処理で効率化

3. **通知送信**:
   - 接続リクエスト、メッセージ、いいねの通知を非同期で送信

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 9.3億人
- **日間アクティブユーザー**: 3.1億人
- **1日の投稿数**: 1億投稿
- **1日のフィード読み込み**: 50億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ**:
- EBS: 500 TB
- コスト: $0.10/GB/月 × 500,000 GB = **$50,000/月**

**ネットワーク**:
- データ転送: 2 PB/月
- コスト: $0.09/GB × 2,000,000 GB = **$180,000/月**

**合計**: 約 **$416,223/月**（約4,994,676ドル/年）

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

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 1時間
   - RPO（Recovery Point Objective）: 15分

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のリソースのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - パスワード: bcryptでハッシュ化

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
- **FID（First Input Delay）**: < 100ms
- **CLS（Cumulative Layout Shift）**: < 0.1

### プログレッシブローディング

1. **無限スクロール**: 
   - ページネーションの代わりに無限スクロール
   - ビューポートに近づいたら次のページを読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - プレースホルダーを表示

## 12. 実装例

### プロフィールサービス（疑似コード）

```python
class ProfileService:
    def __init__(self, db, cache, search_index):
        self.db = db
        self.cache = cache
        self.search_index = search_index
    
    async def get_profile(self, user_id: int):
        # キャッシュから取得を試みる
        cache_key = f"profile:{user_id}"
        cached_profile = await self.cache.get(cache_key)
        
        if cached_profile:
            return cached_profile
        
        # データベースから取得
        profile = await self.db.get_user_profile(user_id)
        
        # キャッシュに保存
        await self.cache.set(cache_key, profile, ttl=900)
        
        return profile
```

### フィードサービス（疑似コード）

```python
class FeedService:
    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
    
    async def get_feed(self, user_id: int, limit: int = 20, cursor: str = None):
        # キャッシュから取得を試みる
        cache_key = f"feed:{user_id}:{cursor or 'latest'}"
        cached_feed = await self.cache.get(cache_key)
        
        if cached_feed:
            return cached_feed
        
        # 接続しているユーザーを取得
        connections = await self.db.get_connections(user_id)
        connected_user_ids = [c["user_id_2"] for c in connections]
        
        # 接続しているユーザーの投稿を取得
        posts = await self.db.get_posts_by_users(
            user_ids=connected_user_ids,
            limit=limit,
            cursor=cursor
        )
        
        # ランキングアルゴリズムでソート
        ranked_posts = self.rank_posts(posts, user_id)
        
        # キャッシュに保存
        await self.cache.set(cache_key, ranked_posts, ttl=300)
        
        return ranked_posts
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のフィード読み込み**: 50億回
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

#### 書き込みトラフィック

- **1日の投稿数**: 1億投稿
- **1時間あたり**: 1億 / 24 = 約416万投稿
- **1秒あたり**: 416万 / 3600 = 約1,156投稿/秒
- **ピーク時（3倍）**: 約3,468投稿/秒

### ストレージ見積もり

#### 投稿ストレージ

- **1投稿あたりのサイズ**: 約1 KB（メタデータ含む）
- **1日の投稿数**: 1億投稿
- **1日のストレージ**: 1億 × 1 KB = 100 GB
- **1年のストレージ**: 100 GB × 365 = 約36.5 TB
- **5年のストレージ**: 約182.5 TB

### 帯域幅見積もり

#### 読み取り帯域幅

- **1フィードあたりのサイズ**: 平均100 KB（20投稿）
- **1秒あたりの読み取り**: 173,334回/秒（ピーク時）
- **読み取り帯域幅**: 173,334 × 100 KB = 17.3 GB/秒 = 約138 Gbps

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

2. **フィード生成の複雑さ**:
   - 問題: リアルタイムでフィードを生成すると遅い
   - 解決策: 事前計算とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Twitter](twitter_design.md) - マイクロブログプラットフォーム
- [Facebook](facebook_design.md) - ソーシャルネットワーク
- [Instagram](instagram_design.md) - メディア中心のソーシャルメディア

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [TikTok](tiktok_design.md)で動画中心のソーシャルメディアの設計を学ぶ

