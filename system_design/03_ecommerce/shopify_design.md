# Shopify システム設計

## 1. システム概要

### 目的と主要機能

Shopifyは、企業がオンラインストアを構築・運営できるEコマースプラットフォームです。ストアの作成、商品管理、決済処理、在庫管理などの機能を提供します。

**主要機能**:
- オンラインストアの作成・カスタマイズ
- 商品管理
- 在庫管理
- 決済処理
- 注文管理
- 配送管理
- レポート・分析

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.5億人（ストアオーナー + 顧客）
- **日間アクティブユーザー（DAU）**: 約5,000万人
- **1日の取引数**: 約500万取引
- **1秒あたりのリクエスト数**: 約20,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ストア作成**: 企業がオンラインストアを作成
2. **商品管理**: ストアオーナーが商品を追加・編集
3. **注文処理**: 顧客が商品を注文
4. **決済処理**: 注文の決済処理
5. **在庫管理**: 在庫の更新・管理

## 2. 機能要件

### コア機能

1. **ストア管理**
   - ストアの作成・設定
   - テーマのカスタマイズ
   - ドメイン設定

2. **商品管理**
   - 商品の追加・編集・削除
   - 商品カテゴリ管理
   - 商品画像管理

3. **在庫管理**
   - 在庫数の追跡
   - 在庫アラート
   - 在庫履歴

4. **注文管理**
   - 注文の受付
   - 注文ステータスの管理
   - 注文履歴

5. **決済処理**
   - 複数の決済方法のサポート
   - 決済ゲートウェイとの統合

6. **配送管理**
   - 配送方法の設定
   - 配送料計算
   - 配送追跡

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 在庫は強い一貫性が必要、商品情報は最終的に一貫性を保つ
- **パフォーマンス**:
  - ストアページ読み込み: < 2秒
  - 商品検索: < 1秒
  - 注文処理: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 注文、在庫データは永続的に保存

### 優先順位付け

1. **P0（必須）**: ストア作成、商品管理、注文処理、決済
2. **P1（重要）**: 在庫管理、配送管理、レポート
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
│  │ Store    │  │ Product  │  │ Order    │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Inventory Service               │         │
│  │      Payment Service                 │         │
│  │      Shipping Service                │         │
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
   - **Store Service**: ストアの管理
   - **Product Service**: 商品の管理
   - **Order Service**: 注文の処理
   - **Inventory Service**: 在庫の管理
   - **Payment Service**: 決済処理
   - **Shipping Service**: 配送管理
4. **Database**: ストア、商品、注文、在庫の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（在庫更新、通知など）
7. **Search Index**: 商品検索インデックス
8. **CDN**: 静的コンテンツ（画像、CSS、JS）をCDNで配信

### データフロー

#### 注文処理のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Order Service
3. Order Service:
   a. 在庫を確認（Inventory Service）
   b. 在庫を予約
   c. 注文を作成
   d. Payment Serviceに決済リクエスト
   e. 決済成功後、在庫を更新
   f. Message Queueに通知イベントを送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Stores テーブル

```sql
CREATE TABLE stores (
    store_id BIGINT PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    store_name VARCHAR(200) NOT NULL,
    domain VARCHAR(200) UNIQUE,
    theme_id BIGINT,
    status ENUM('active', 'suspended', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    INDEX idx_owner_id (owner_id),
    INDEX idx_domain (domain)
) ENGINE=InnoDB;
```

#### Products テーブル

```sql
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    compare_at_price DECIMAL(10, 2),
    sku VARCHAR(100),
    status ENUM('active', 'draft', 'archived') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    INDEX idx_store_id (store_id),
    INDEX idx_status (status),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Inventory テーブル

```sql
CREATE TABLE inventory (
    inventory_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    variant_id BIGINT,
    quantity INT NOT NULL DEFAULT 0,
    reserved_quantity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_product_id (product_id),
    INDEX idx_variant_id (variant_id)
) ENGINE=InnoDB;
```

#### Orders テーブル

```sql
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    store_id BIGINT NOT NULL,
    customer_id BIGINT,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (customer_id) REFERENCES users(user_id),
    INDEX idx_store_id_created_at (store_id, created_at DESC),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ストア、商品、注文、在庫の永続化
- **Elasticsearch**:
  - 理由: 全文検索、商品検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `products`テーブルは`store_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **トランザクション**: 在庫更新はトランザクションで処理

## 5. API設計

### 主要なAPIエンドポイント

#### 商品追加

```
POST /api/v1/stores/{store_id}/products
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Product Title",
  "description": "Product Description",
  "price": 29.99,
  "sku": "SKU-123",
  "quantity": 100
}

Response (201 Created):
{
  "product_id": 1234567890,
  "status": "active"
}
```

#### 注文作成

```
POST /api/v1/stores/{store_id}/orders
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
  "payment_method": "credit_card"
}

Response (201 Created):
{
  "order_id": 9876543210,
  "status": "pending",
  "total_amount": 59.98
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ストアオーナーは自分のストアのみ管理可能
- **レート制限**: 
  - 商品追加: 1,000商品/日
  - 注文処理: 10,000注文/日

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Store IDベースのシャーディング

```
Shard 1: store_id % 4 == 0
Shard 2: store_id % 4 == 1
Shard 3: store_id % 4 == 2
Shard 4: store_id % 4 == 3
```

**シャーディングキー**: `store_id`
- 商品は`store_id`でシャーディング
- 注文は`store_id`でシャーディング

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

1. **在庫更新**: トランザクション処理の最適化
2. **商品検索**: Elasticsearchクエリの最適化
3. **決済処理**: 外部決済ゲートウェイとの通信

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: 商品情報をエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### データベースクエリ最適化

1. **インデックス最適化**: 
   - `(store_id, status)`の複合インデックス
   - `(product_id, variant_id)`の複合インデックス

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

2. **注文通知**:
   - 注文作成、ステータス変更の通知を非同期で送信

3. **検索インデックス更新**:
   - 商品追加・更新時に非同期で検索インデックスを更新

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1.5億人
- **日間アクティブユーザー**: 5,000万人
- **1日の取引数**: 500万取引

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 600台（リージョン間で分散）
- コスト: $0.192/時間 × 600台 × 730時間 = **$84,096/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ**:
- EBS: 150 TB
- コスト: $0.10/GB/月 × 150,000 GB = **$15,000/月**

**ネットワーク**:
- データ転送: 800 TB/月
- コスト: $0.09/GB × 800,000 GB = **$72,000/月**

**合計**: 約 **$212,049/月**（約2,544,588ドル/年）

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
   - ストアオーナーは自分のストアのみ管理可能

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

### 在庫サービス（疑似コード）

```python
class InventoryService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def reserve_inventory(self, product_id: int, quantity: int):
        # トランザクション開始
        async with self.db.transaction():
            # 在庫を取得
            inventory = await self.db.get_inventory(product_id)
            
            # 在庫を確認
            available_quantity = inventory["quantity"] - inventory["reserved_quantity"]
            if available_quantity < quantity:
                raise ValueError("Insufficient inventory")
            
            # 在庫を予約
            await self.db.update_inventory(
                product_id=product_id,
                reserved_quantity=inventory["reserved_quantity"] + quantity
            )
            
            # キャッシュを更新
            await self.cache.set(
                f"inventory:{product_id}",
                {...inventory, "reserved_quantity": inventory["reserved_quantity"] + quantity},
                ttl=300
            )
        
        return {
            "product_id": product_id,
            "reserved_quantity": quantity
        }
    
    async def confirm_inventory(self, product_id: int, quantity: int):
        # トランザクション開始
        async with self.db.transaction():
            # 在庫を更新
            await self.db.update_inventory(
                product_id=product_id,
                quantity=inventory["quantity"] - quantity,
                reserved_quantity=inventory["reserved_quantity"] - quantity
            )
        
        # 在庫更新イベントを送信
        await self.message_queue.publish(
            topic="inventory-updated",
            message={
                "product_id": product_id,
                "quantity": inventory["quantity"] - quantity
            }
        )
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のストアページビュー**: 20億回
- **1時間あたり**: 20億 / 24 = 約8.33億回
- **1秒あたり**: 8.33億 / 3600 = 約231,389回/秒
- **ピーク時（3倍）**: 約694,167回/秒

#### 書き込みトラフィック

- **1日の取引数**: 500万取引
- **1時間あたり**: 500万 / 24 = 約208,333取引
- **1秒あたり**: 208,333 / 3600 = 約58取引/秒

### ストレージ見積もり

#### 商品ストレージ

- **1商品あたりのサイズ**: 約3 KB（メタデータ含む）
- **商品総数**: 1億商品
- **合計ストレージ**: 1億 × 3 KB = 300 GB
- **5年のストレージ**: 約1.5 TB（新規追加を考慮）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **トランザクション**: 在庫更新はトランザクションで処理
4. **キャッシュファースト**: 可能な限りキャッシュを活用
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **在庫の競合状態**:
   - 問題: 同時注文で在庫の競合が発生
   - 解決策: トランザクションと楽観的ロック

2. **決済処理の失敗**:
   - 問題: 決済失敗時の在庫ロールバック
   - 解決策: サーガパターンまたは補償トランザクション

## 15. 関連システム

### 類似システムへのリンク

- [Amazon](amazon_design.md) - Eコマースプラットフォーム
- [eBay](ebay_design.md) - オークション・Eコマースプラットフォーム
- [Alibaba](alibaba_design.md) - Eコマースプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Alibaba](alibaba_design.md)で大規模Eコマースプラットフォームの設計を学ぶ

