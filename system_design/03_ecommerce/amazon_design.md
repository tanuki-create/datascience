# Amazon (Eコマース) システム設計

## 1. システム概要

### 目的と主要機能

Amazonは、商品の販売と購入を可能にする総合Eコマースプラットフォームです。

**主要機能**:
- 商品カタログの閲覧と検索
- 商品の購入と決済
- 在庫管理
- レコメンデーション
- レビューと評価
- 配送管理

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日の注文数**: 約1,000万件
- **商品数**: 約3億5,000万点
- **1秒あたりの検索リクエスト**: 約50,000回/秒（ピーク時）

### 主要なユースケース

1. **商品検索**: ユーザーが商品を検索
2. **商品購入**: ユーザーが商品を購入
3. **在庫確認**: リアルタイム在庫の確認
4. **レコメンデーション**: パーソナライズされた商品推薦

## 2. 機能要件

### コア機能

1. **商品カタログ**
   - 数百万商品の管理
   - 商品の検索とフィルタリング
   - 商品詳細ページ

2. **在庫管理**
   - リアルタイム在庫更新
   - 在庫の競合制御

3. **決済処理**
   - 安全な決済トランザクション
   - 複数の決済方法

4. **レコメンデーション**
   - パーソナライズされた商品推薦
   - 関連商品の表示

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 商品検索: < 500ms
  - 商品ページ読み込み: < 1秒
  - 決済処理: < 2秒
- **一貫性**: 在庫情報は強い一貫性が必要

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                       │
└──────┬──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
│  API Gateway│   │  API Gateway│   │  API Gateway│
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       ├─────────────────┴──────────────────┤
       │                                     │
┌──────▼─────────────────────────────────────▼──────┐
│              Application Servers                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Catalog │  │ Inventory│  │ Payment │        │
│  │ Service │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Order Service                   │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┬──────────┐
        │                 │                  │          │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐  │
│   Database   │  │   Cache       │  │  Search      │  │
│   (Sharded)  │  │   (Redis)     │  │  Engine      │  │
│              │  │               │  │  (Elastic)   │  │
└──────────────┘  └───────────────┘  └──────────────┘  │
```

### コンポーネントの説明

1. **Catalog Service**: 商品カタログの管理
2. **Inventory Service**: 在庫管理
3. **Payment Service**: 決済処理
4. **Order Service**: 注文管理
5. **Search Engine**: 商品検索（Elasticsearch）

## 4. データモデル設計

### 主要なエンティティ

#### Products テーブル

```sql
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
    INDEX idx_category_id (category_id),
    INDEX idx_seller_id (seller_id),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Inventory テーブル

```sql
CREATE TABLE inventory (
    inventory_id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    reserved_quantity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_product_id (product_id)
) ENGINE=InnoDB;
```

#### Orders テーブル

```sql
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

## 5. API設計

### 主要なAPIエンドポイント

#### 商品検索

```
GET /api/v1/products/search?q=laptop&limit=20&page=1
Authorization: Bearer <token>

Response (200 OK):
{
  "products": [
    {
      "product_id": 1234567890,
      "title": "Laptop Computer",
      "price": 999.99,
      "rating": 4.5,
      "review_count": 1234
    }
  ],
  "total_results": 10000,
  "page": 1,
  "limit": 20
}
```

#### 商品購入

```
POST /api/v1/orders
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "items": [
    {
      "product_id": 1234567890,
      "quantity": 1
    }
  ],
  "shipping_address": {...},
  "payment_method": "credit_card"
}

Response (201 Created):
{
  "order_id": 9876543210,
  "status": "confirmed",
  "total_amount": 999.99
}
```

## 6. スケーラビリティ設計

### データベースシャーディング

**シャーディング戦略**: Product IDベースのシャーディング

```
Shard 1: product_id % 16 == 0
Shard 2: product_id % 16 == 1
...
Shard 16: product_id % 16 == 15
```

### 在庫管理の競合制御

- **楽観的ロック**: バージョン番号を使用
- **悲観的ロック**: 在庫予約時にロック
- **分散ロック**: Redisで分散ロックを実装

## 7. レイテンシ最適化

### 検索の最適化

- **Elasticsearch**: 全文検索エンジン
- **キャッシング**: 人気検索クエリをキャッシュ
- **ファセット検索**: フィルタリングで結果を絞り込み

### 商品ページの最適化

- **CDN**: 静的コンテンツ（画像）をCDNで配信
- **キャッシング**: 商品詳細ページをキャッシュ
- **非同期読み込み**: レビューや関連商品を非同期で読み込み

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$500,000/月**
- **データベース**: 約 **$200,000/月**
- **ストレージ**: 約 **$100,000/月**
- **CDN**: 約 **$50,000/月**
- **合計**: 約 **$850,000/月**

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **オートスケーリング**: 需要に応じてインスタンス数を調整
3. **キャッシング**: キャッシュヒット率を80%以上に

## 9. 可用性・信頼性

### 障害対策

- **マルチAZ**: 複数のアベイラビリティゾーンにデプロイ
- **データベースレプリケーション**: 読み取りレプリカを配置

## 10. セキュリティ

### 決済セキュリティ

- **PCI DSS準拠**: クレジットカード情報の安全な処理
- **トークン化**: クレジットカード情報をトークン化
- **暗号化**: TLS 1.3で転送中の暗号化

## 11. UX最適化

### パフォーマンス指標

- **商品検索**: < 500ms
- **商品ページ読み込み**: < 1秒
- **決済処理**: < 2秒

## 12. 実装例

### 在庫管理サービス（疑似コード）

```python
class InventoryService:
    def __init__(self, db, redis_lock):
        self.db = db
        self.redis_lock = redis_lock
    
    async def reserve_inventory(self, product_id: int, quantity: int):
        # 分散ロックを取得
        lock_key = f"inventory_lock:{product_id}"
        async with self.redis_lock.acquire(lock_key, timeout=5):
            # 在庫を確認
            inventory = await self.db.get_inventory(product_id)
            
            if inventory["available_quantity"] < quantity:
                raise ValueError("Insufficient inventory")
            
            # 在庫を予約
            await self.db.reserve_inventory(
                product_id=product_id,
                quantity=quantity
            )
            
            return {
                "product_id": product_id,
                "reserved_quantity": quantity
            }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の検索リクエスト**: 約4.32億回
- **1秒あたりの検索リクエスト**: 約5,000回/秒（平均）
- **ピーク時（10倍）**: 約50,000回/秒

### ストレージ見積もり

- **商品数**: 3.5億点
- **1商品あたりのメタデータサイズ**: 約5 KB
- **合計ストレージ**: 3.5億 × 5 KB = 約1.75 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **在庫管理**: 楽観的ロックと悲観的ロックの組み合わせ
2. **検索**: Elasticsearchで高速検索
3. **キャッシング**: 商品詳細ページを積極的にキャッシュ

## 15. 関連システム

### 類似システムへのリンク

- [eBay](ebay_design.md) - オークション・マーケットプレイス
- [Shopify](shopify_design.md) - Eコマースプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Google検索](google_search_design.md)で検索エンジンの設計を学ぶ

