# eBay システム設計

## 1. システム概要

### 目的と主要機能

eBayは、個人や企業が商品を出品し、他のユーザーが入札または即決購入できるオークション・Eコマースプラットフォームです。

**主要機能**:
- 商品の出品
- オークション入札
- 即決購入（Buy It Now）
- 商品検索
- 決済処理
- レビュー・評価システム

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.8億人
- **日間アクティブユーザー（DAU）**: 約6,000万人
- **1日の商品出品数**: 約500万商品
- **1日の取引数**: 約1,000万取引
- **1秒あたりのリクエスト数**: 約30,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **商品出品**: 売り手が商品を出品
2. **商品検索**: 買い手が商品を検索
3. **入札**: 買い手がオークションに入札
4. **即決購入**: 買い手が即決価格で購入
5. **決済**: 取引の決済処理

## 2. 機能要件

### コア機能

1. **商品管理**
   - 商品の出品
   - 商品情報の編集
   - 商品の削除

2. **オークション**
   - 入札機能
   - 自動入札（Proxy Bidding）
   - オークション終了処理

3. **検索**
   - 商品検索
   - カテゴリ検索
   - フィルタリング

4. **決済**
   - 決済処理
   - 支払い方法の管理

5. **レビュー・評価**
   - 取引後のレビュー
   - 売り手・買い手の評価

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 入札は強い一貫性が必要、商品情報は最終的に一貫性を保つ
- **パフォーマンス**:
  - 商品検索: < 1秒
  - 入札処理: < 200ms
  - 商品出品: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 取引データは永続的に保存

### 優先順位付け

1. **P0（必須）**: 商品出品、商品検索、入札、決済
2. **P1（重要）**: レビュー、評価、通知
3. **P2（望ましい）**: 推薦、パーソナライゼーション

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
│  │ Listing  │  │  Search  │  │  Bidding │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Payment Service                 │         │
│  │      Notification Service             │         │
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
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Listing Service**: 商品の出品と管理
   - **Search Service**: 商品検索
   - **Bidding Service**: 入札処理
   - **Payment Service**: 決済処理
   - **Notification Service**: 通知送信
4. **Database**: 商品、取引、ユーザーの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（通知、オークション終了処理など）
7. **Search Index**: 商品検索インデックス
8. **CDN**: 静的コンテンツ（画像、CSS、JS）をCDNで配信

### データフロー

#### 商品出品のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Listing Service
3. Listing Service:
   a. 商品情報をデータベースに保存
   b. 検索インデックスを更新
   c. Cacheに商品情報を保存
   d. Message Queueに通知イベントを送信
```

#### 入札のフロー

```
1. Client → API Gateway → Bidding Service
2. Bidding Service:
   a. 入札情報を検証（現在の最高入札額より高いか）
   b. データベースにトランザクションで保存
   c. Cacheを更新
   d. Message Queueに通知イベントを送信
3. Notification Service（非同期）:
   a. 他の入札者に通知を送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Listings テーブル

```sql
CREATE TABLE listings (
    listing_id BIGINT PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id BIGINT NOT NULL,
    starting_price DECIMAL(10, 2) NOT NULL,
    buy_it_now_price DECIMAL(10, 2),
    current_bid DECIMAL(10, 2),
    bid_count INT DEFAULT 0,
    status ENUM('active', 'ended', 'sold') DEFAULT 'active',
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_category_id (category_id),
    INDEX idx_status_end_time (status, end_time),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Bids テーブル

```sql
CREATE TABLE bids (
    bid_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    listing_id BIGINT NOT NULL,
    bidder_id BIGINT NOT NULL,
    bid_amount DECIMAL(10, 2) NOT NULL,
    is_proxy_bid BOOLEAN DEFAULT FALSE,
    max_proxy_bid DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id),
    FOREIGN KEY (bidder_id) REFERENCES users(user_id),
    INDEX idx_listing_id_created_at (listing_id, created_at DESC),
    INDEX idx_bidder_id (bidder_id)
) ENGINE=InnoDB;
```

#### Transactions テーブル

```sql
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    listing_id BIGINT NOT NULL,
    buyer_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (seller_id) REFERENCES users(user_id),
    INDEX idx_buyer_id (buyer_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 商品、入札、取引の永続化
- **Elasticsearch**:
  - 理由: 全文検索、商品検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `listings`テーブルは`category_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **トランザクション**: 入札処理はトランザクションで処理

## 5. API設計

### 主要なAPIエンドポイント

#### 商品出品

```
POST /api/v1/listings
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Product Title",
  "description": "Product Description",
  "category_id": 123,
  "starting_price": 10.00,
  "buy_it_now_price": 50.00,
  "end_time": "2024-01-20T10:00:00Z"
}

Response (201 Created):
{
  "listing_id": 1234567890,
  "status": "active"
}
```

#### 入札

```
POST /api/v1/listings/{listing_id}/bids
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "bid_amount": 15.00,
  "is_proxy_bid": false,
  "max_proxy_bid": 20.00
}

Response (200 OK):
{
  "bid_id": 1234567891,
  "status": "accepted",
  "current_bid": 15.00
}
```

#### 商品検索

```
GET /api/v1/search?q=laptop&category=electronics&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "listings": [...],
  "total_results": 1000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の商品のみ編集可能
- **レート制限**: 
  - 商品出品: 100商品/日
  - 入札: 100入札/分
  - 検索: 100リクエスト/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Category IDベースのシャーディング

```
Shard 1: category_id % 4 == 0
Shard 2: category_id % 4 == 1
Shard 3: category_id % 4 == 2
Shard 4: category_id % 4 == 3
```

**シャーディングキー**: `category_id`
- 商品は`category_id`でシャーディング
- 入札は`listing_id`でシャーディング

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
   - 用途: 商品情報、入札情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 静的コンテンツ、商品画像
   - TTL: 1時間-1日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **商品検索**: Elasticsearchクエリの最適化
2. **入札処理**: トランザクション処理の最適化
3. **オークション終了処理**: バッチ処理の最適化

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: 商品情報をエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### データベースクエリ最適化

1. **インデックス最適化**: 
   - `(category_id, status, end_time)`の複合インデックス
   - `(listing_id, created_at)`の複合インデックス

2. **クエリ最適化**:
   - JOINの代わりにアプリケーションレベルのJOIN
   - LIMIT句で結果数を制限
   - ページネーションでカーソルベースのページング

3. **読み取りレプリカ**:
   - 読み取り専用クエリはレプリカにルーティング
   - 書き込みはマスターデータベースに

### 非同期処理

#### メッセージキュー（Kafka）

1. **オークション終了イベント**:
   ```
   Topic: auction-ended
   Partition Key: listing_id
   ```

2. **通知送信**:
   - 入札、オークション終了の通知を非同期で送信

3. **検索インデックス更新**:
   - 商品出品・更新時に非同期で検索インデックスを更新

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1.8億人
- **日間アクティブユーザー**: 6,000万人
- **1日の商品出品数**: 500万商品
- **1日の取引数**: 1,000万取引

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 800台（リージョン間で分散）
- コスト: $0.192/時間 × 800台 × 730時間 = **$112,128/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**ストレージ**:
- EBS: 200 TB
- コスト: $0.10/GB/月 × 200,000 GB = **$20,000/月**

**ネットワーク**:
- データ転送: 1 PB/月
- コスト: $0.09/GB × 1,000,000 GB = **$90,000/月**

**合計**: 約 **$276,732/月**（約3,320,784ドル/年）

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
   - ユーザーは自分の商品のみ編集可能

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

### 入札サービス（疑似コード）

```python
class BiddingService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def place_bid(self, listing_id: int, bidder_id: int, bid_amount: float, max_proxy_bid: float = None):
        # トランザクション開始
        async with self.db.transaction():
            # 現在の最高入札額を取得
            listing = await self.db.get_listing(listing_id)
            
            # 入札額を検証
            if bid_amount <= listing["current_bid"]:
                raise ValueError("Bid amount must be higher than current bid")
            
            # 入札を保存
            bid_id = await self.db.insert_bid(
                listing_id=listing_id,
                bidder_id=bidder_id,
                bid_amount=bid_amount,
                max_proxy_bid=max_proxy_bid
            )
            
            # 商品情報を更新
            await self.db.update_listing(
                listing_id=listing_id,
                current_bid=bid_amount,
                bid_count=listing["bid_count"] + 1
            )
            
            # キャッシュを更新
            await self.cache.set(
                f"listing:{listing_id}",
                {...listing, "current_bid": bid_amount},
                ttl=300
            )
        
        # 通知イベントを送信
        await self.message_queue.publish(
            topic="bid-placed",
            message={
                "bid_id": bid_id,
                "listing_id": listing_id,
                "bidder_id": bidder_id,
                "bid_amount": bid_amount
            }
        )
        
        return {
            "bid_id": bid_id,
            "status": "accepted",
            "current_bid": bid_amount
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の商品検索**: 10億回
- **1時間あたり**: 10億 / 24 = 約4.17億回
- **1秒あたり**: 4.17億 / 3600 = 約115,833回/秒
- **ピーク時（3倍）**: 約347,499回/秒

#### 書き込みトラフィック

- **1日の商品出品数**: 500万商品
- **1時間あたり**: 500万 / 24 = 約208,333商品
- **1秒あたり**: 208,333 / 3600 = 約58商品/秒

### ストレージ見積もり

#### 商品ストレージ

- **1商品あたりのサイズ**: 約2 KB（メタデータ含む）
- **1日の商品出品数**: 500万商品
- **1日のストレージ**: 500万 × 2 KB = 10 GB
- **1年のストレージ**: 10 GB × 365 = 約3.65 TB
- **5年のストレージ**: 約18.25 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **トランザクション**: 入札処理はトランザクションで処理
4. **キャッシュファースト**: 可能な限りキャッシュを活用
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **入札の競合状態**:
   - 問題: 同時入札で競合が発生
   - 解決策: トランザクションと楽観的ロック

2. **オークション終了処理**:
   - 問題: オークション終了処理が遅い
   - 解決策: バッチ処理と非同期処理

## 15. 関連システム

### 類似システムへのリンク

- [Amazon](amazon_design.md) - Eコマースプラットフォーム
- [Shopify](shopify_design.md) - Eコマースプラットフォーム
- [Alibaba](alibaba_design.md) - Eコマースプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Shopify](shopify_design.md)でEコマースプラットフォームの設計を学ぶ

