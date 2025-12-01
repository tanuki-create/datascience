# Alibaba システム設計

## 1. システム概要

### 目的と主要機能

Alibabaは、B2B（Business-to-Business）とB2C（Business-to-Consumer）のEコマースプラットフォームです。企業間取引、小売取引、決済、物流などの機能を統合したエコシステムを提供します。

**主要機能**:
- B2B取引プラットフォーム（Alibaba.com）
- B2C取引プラットフォーム（Tmall、Taobao）
- 決済システム（Alipay）
- 物流システム（Cainiao）
- クラウドサービス（Alibaba Cloud）
- 推薦システム

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約10億人
- **日間アクティブユーザー（DAU）**: 約5億人
- **1日の取引数**: 約1億取引
- **1日の取引額**: 約100億ドル
- **1秒あたりのリクエスト数**: 約100,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **商品検索**: ユーザーが商品を検索
2. **商品購入**: ユーザーが商品を購入
3. **決済処理**: Alipay経由での決済
4. **物流追跡**: 配送状況の追跡
5. **推薦**: パーソナライズされた商品推薦

## 2. 機能要件

### コア機能

1. **商品管理**
   - 商品の出品・管理
   - 商品カテゴリ管理
   - 商品検索

2. **取引管理**
   - 注文の作成・処理
   - 取引履歴の管理
   - 返品・返金処理

3. **決済処理**
   - Alipay統合
   - 複数の決済方法のサポート
   - 決済セキュリティ

4. **物流管理**
   - 配送方法の選択
   - 配送追跡
   - 倉庫管理

5. **推薦システム**
   - パーソナライズされた商品推薦
   - 視聴履歴に基づく推薦

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 在庫、決済は強い一貫性が必要、商品情報は最終的に一貫性を保つ
- **パフォーマンス**:
  - 商品検索: < 1秒
  - 注文処理: < 500ms
  - 決済処理: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 取引、決済データは永続的に保存

### 優先順位付け

1. **P0（必須）**: 商品検索、注文処理、決済処理
2. **P1（重要）**: 物流管理、推薦システム
3. **P2（望ましい）**: 分析、マーケティングツール

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
│  │ Product  │  │  Order    │  │ Payment  │        │
│  │ Service  │  │ Service   │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Logistics Service               │         │
│  │      Recommendation Service          │         │
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
│         CDN (CloudFront/Cloudflare)                │
│         Alipay Integration                        │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Product Service**: 商品の管理
   - **Order Service**: 注文の処理
   - **Payment Service**: 決済処理（Alipay統合）
   - **Logistics Service**: 物流管理
   - **Recommendation Service**: 推薦の生成
4. **Database**: 商品、注文、決済の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（在庫更新、通知など）
7. **Search Index**: 商品検索インデックス
8. **CDN**: 静的コンテンツ（画像、CSS、JS）をCDNで配信
9. **Alipay Integration**: 決済ゲートウェイとの統合

### データフロー

#### 注文処理のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Order Service
3. Order Service:
   a. 在庫を確認
   b. 在庫を予約
   c. 注文を作成
   d. Payment Serviceに決済リクエスト
   e. Alipayと通信して決済処理
   f. 決済成功後、在庫を更新
   g. Logistics Serviceに配送リクエスト
   h. Message Queueに通知イベントを送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Products テーブル

```sql
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id BIGINT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    status ENUM('active', 'inactive', 'sold_out') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_category_id (category_id),
    INDEX idx_status (status),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Orders テーブル

```sql
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    buyer_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    order_status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (seller_id) REFERENCES users(user_id),
    INDEX idx_buyer_id_created_at (buyer_id, created_at DESC),
    INDEX idx_seller_id_created_at (seller_id, created_at DESC),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB;
```

#### Payments テーブル

```sql
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    alipay_transaction_id VARCHAR(100),
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    INDEX idx_order_id (order_id),
    INDEX idx_status (status),
    INDEX idx_alipay_transaction_id (alipay_transaction_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 商品、注文、決済の永続化
- **Elasticsearch**:
  - 理由: 全文検索、商品検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `products`テーブルは`category_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **トランザクション**: 在庫更新、決済処理はトランザクションで処理

## 5. API設計

### 主要なAPIエンドポイント

#### 商品検索

```
GET /api/v1/products/search?q=laptop&category=electronics&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "products": [...],
  "total_results": 10000
}
```

#### 注文作成

```
POST /api/v1/orders
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "items": [
    {
      "product_id": 1234567890,
      "quantity": 2
    }
  ],
  "shipping_address": {...},
  "payment_method": "alipay"
}

Response (201 Created):
{
  "order_id": 9876543210,
  "status": "pending",
  "total_amount": 199.98,
  "payment_url": "https://alipay.com/pay/..."
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の注文のみアクセス可能
- **レート制限**: 
  - 商品検索: 100リクエスト/分
  - 注文処理: 10注文/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Category IDベースのシャーディング

```
Shard 1: category_id % 8 == 0
Shard 2: category_id % 8 == 1
...
Shard 8: category_id % 8 == 7
```

**シャーディングキー**: `category_id`
- 商品は`category_id`でシャーディング
- 注文は`buyer_id`でシャーディング

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
   - 用途: 商品情報、在庫情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 静的コンテンツ、商品画像
   - TTL: 1時間-1日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **商品検索**: Elasticsearchクエリの最適化
2. **決済処理**: Alipayとの通信レイテンシ
3. **在庫更新**: トランザクション処理の最適化

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: 商品情報をエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### データベースクエリ最適化

1. **インデックス最適化**: 
   - `(category_id, status)`の複合インデックス
   - `(buyer_id, created_at)`の複合インデックス

2. **クエリ最適化**:
   - JOINの代わりにアプリケーションレベルのJOIN
   - LIMIT句で結果数を制限
   - ページネーションでカーソルベースのページング

3. **読み取りレプリカ**:
   - 読み取り専用クエリはレプリカにルーティング
   - 書き込みはマスターデータベースに

### 非同期処理

#### メッセージキュー（Kafka）

1. **在庫更新イベント**:
   ```
   Topic: inventory-updated
   Partition Key: product_id
   ```

2. **決済通知**:
   ```
   Topic: payment-completed
   Partition Key: order_id
   ```

3. **検索インデックス更新**:
   - 商品追加・更新時に非同期で検索インデックスを更新

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 10億人
- **日間アクティブユーザー**: 5億人
- **1日の取引数**: 1億取引

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
- インスタンス数: 50台
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**ストレージ**:
- EBS: 500 TB
- コスト: $0.10/GB/月 × 500,000 GB = **$50,000/月**

**ネットワーク**:
- データ転送: 5 PB/月
- コスト: $0.09/GB × 5,000,000 GB = **$450,000/月**

**合計**: 約 **$879,090/月**（約10,549,080ドル/年）

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
   - ユーザーは自分の注文のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - 決済情報: PCI DSS準拠の暗号化

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

### 決済サービス（疑似コード）

```python
class PaymentService:
    def __init__(self, db, cache, alipay_client, message_queue):
        self.db = db
        self.cache = cache
        self.alipay_client = alipay_client
        self.message_queue = message_queue
    
    async def process_payment(self, order_id: int, amount: float, payment_method: str):
        # トランザクション開始
        async with self.db.transaction():
            # 決済レコードを作成
            payment_id = await self.db.insert_payment(
                order_id=order_id,
                amount=amount,
                payment_method=payment_method,
                status='pending'
            )
            
            # Alipayと通信して決済処理
            if payment_method == 'alipay':
                result = await self.alipay_client.create_payment(
                    order_id=order_id,
                    amount=amount
                )
                
                # 決済結果を更新
                await self.db.update_payment(
                    payment_id=payment_id,
                    alipay_transaction_id=result['transaction_id'],
                    status='completed' if result['success'] else 'failed'
                )
                
                # 注文ステータスを更新
                await self.db.update_order(
                    order_id=order_id,
                    payment_status='paid' if result['success'] else 'failed'
                )
        
        # 決済完了イベントを送信
        await self.message_queue.publish(
            topic="payment-completed",
            message={
                "payment_id": payment_id,
                "order_id": order_id,
                "status": "completed" if result['success'] else "failed"
            }
        )
        
        return {
            "payment_id": payment_id,
            "status": "completed" if result['success'] else "failed"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の商品検索**: 50億回
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

#### 書き込みトラフィック

- **1日の取引数**: 1億取引
- **1時間あたり**: 1億 / 24 = 約416万取引
- **1秒あたり**: 416万 / 3600 = 約1,156取引/秒
- **ピーク時（3倍）**: 約3,468取引/秒

### ストレージ見積もり

#### 商品ストレージ

- **1商品あたりのサイズ**: 約3 KB（メタデータ含む）
- **商品総数**: 10億商品
- **合計ストレージ**: 10億 × 3 KB = 3 TB
- **5年のストレージ**: 約15 TB（新規追加を考慮）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **トランザクション**: 在庫更新、決済処理はトランザクションで処理
4. **キャッシュファースト**: 可能な限りキャッシュを活用
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **決済処理の失敗**:
   - 問題: 決済失敗時の在庫ロールバック
   - 解決策: サーガパターンまたは補償トランザクション

2. **在庫の競合状態**:
   - 問題: 同時注文で在庫の競合が発生
   - 解決策: トランザクションと楽観的ロック

## 15. 関連システム

### 類似システムへのリンク

- [Amazon](amazon_design.md) - Eコマースプラットフォーム
- [eBay](ebay_design.md) - オークション・Eコマースプラットフォーム
- [Shopify](shopify_design.md) - Eコマースプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [WeChat](wechat_design.md)でメッセージングプラットフォームの設計を学ぶ

