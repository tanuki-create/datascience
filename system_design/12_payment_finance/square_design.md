# Square システム設計

## 1. システム概要

### 目的と主要機能

Squareは、小売店向けの決済プラットフォームです。POSシステム、オンライン決済、ビジネス管理ツールを提供します。

**主要機能**:
- POS決済
- オンライン決済
- 請求書発行
- 在庫管理
- 顧客管理
- レポート・分析
- Square Capital（融資）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約400万企業
- **日間アクティブユーザー（DAU）**: 約200万企業
- **1日の取引数**: 約5,000万件
- **1日の取引額**: 約20億ドル
- **1秒あたりの取引数**: 約580件/秒（ピーク時）

### 主要なユースケース

1. **POS決済**: 小売店での決済処理
2. **オンライン決済**: オンラインストアでの決済処理
3. **請求書発行**: ビジネス向けの請求書発行
4. **在庫管理**: 在庫の管理・追跡
5. **レポート・分析**: 売上レポート・分析

## 2. 機能要件

### コア機能

1. **POS決済**
   - クレジットカード決済
   - デビットカード決済
   - タッチ決済（NFC）
   - レシート発行

2. **オンライン決済**
   - オンラインストアでの決済
   - 決済リンク
   - サブスクリプション

3. **請求書発行**
   - 請求書の作成・送信
   - 請求書の支払い追跡

4. **在庫管理**
   - 在庫の追跡
   - 在庫アラート
   - 在庫レポート

5. **顧客管理**
   - 顧客情報の管理
   - 顧客履歴
   - 顧客分析

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 決済情報は強い一貫性が必要
- **パフォーマンス**:
  - POS決済: < 3秒
  - オンライン決済: < 2秒
  - 在庫更新: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 決済情報は永続的に保存
- **セキュリティ**: PCI DSS準拠

### 優先順位付け

1. **P0（必須）**: POS決済、オンライン決済、在庫管理
2. **P1（重要）**: 請求書発行、顧客管理、レポート・分析
3. **P2（望ましい）**: Square Capital、高度な分析機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (POS Terminal, Web, Mobile Apps)
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
│  │ POS      │  │ Online   │  │ Inventory│        │
│  │ Payment  │  │ Payment  │  │ Service │        │
│  │ Service  │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Invoice Service                 │         │
│  │      Customer Service                │         │
│  │      Reporting Service               │         │
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
│         Payment Gateway (External)                │
│         Card Reader API                           │
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **POS Payment Service**: POS決済の処理
   - **Online Payment Service**: オンライン決済の処理
   - **Inventory Service**: 在庫管理
   - **Invoice Service**: 請求書発行
   - **Customer Service**: 顧客管理
   - **Reporting Service**: レポート・分析
4. **Database**: 決済、在庫、顧客の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（レポート生成など）
7. **Payment Gateway**: 外部決済ゲートウェイ（カードネットワーク）
8. **Card Reader API**: カードリーダーAPI
9. **CDN**: 画像の配信

### データフロー

#### POS決済のフロー

```
1. Client (POS Terminal) → Load Balancer → API Gateway
2. API Gateway → POS Payment Service
3. POS Payment Service:
   a. カード情報を読み取り
   b. Payment Gatewayに決済リクエストを送信
   c. 決済結果をデータベースに保存
   d. Inventory Serviceで在庫を更新
   e. Customer Serviceで顧客履歴を更新
   f. レシートを発行
```

## 4. データモデル設計

### 主要なエンティティ

#### Transactions テーブル

```sql
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    merchant_id BIGINT NOT NULL,
    customer_id BIGINT,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method ENUM('card', 'cash', 'digital_wallet') NOT NULL,
    transaction_type ENUM('sale', 'refund', 'void') DEFAULT 'sale',
    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Inventory テーブル

```sql
CREATE TABLE inventory (
    item_id BIGINT PRIMARY KEY,
    merchant_id BIGINT NOT NULL,
    item_name VARCHAR(500) NOT NULL,
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    low_stock_threshold INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_low_stock (merchant_id, quantity)
) ENGINE=InnoDB;
```

#### Customers テーブル

```sql
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    merchant_id BIGINT NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    name VARCHAR(200),
    total_spent DECIMAL(15, 2) DEFAULT 0.00,
    visit_count INT DEFAULT 0,
    last_visit TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_email (email)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 決済、在庫、顧客の永続化
- **Redis**:
  - 理由: リアルタイムデータ、在庫管理
  - 用途: 在庫情報、セッション管理

### スキーマ設計の考慮事項

1. **パーティショニング**: `transactions`テーブルは`merchant_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 取引は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### POS決済

```
POST /api/v1/transactions
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "amount": 50.00,
  "payment_method": "card",
  "items": [
    {
      "item_id": 1234567890,
      "quantity": 2
    }
  ]
}

Response (200 OK):
{
  "id": "transaction_1234567890",
  "status": "completed",
  "amount": 50.00,
  "receipt_url": "https://square.com/receipt/..."
}
```

#### 在庫更新

```
PUT /api/v1/inventory/{item_id}
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "quantity": 100
}

Response (200 OK):
{
  "item_id": 1234567890,
  "quantity": 100,
  "status": "updated"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: マーチャントは自分の取引のみアクセス可能
- **レート制限**: 
  - POS決済: 100回/分
  - 在庫更新: 50回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Merchant IDベースのシャーディング

```
Shard 1: merchant_id % 8 == 0
Shard 2: merchant_id % 8 == 1
...
Shard 8: merchant_id % 8 == 7
```

**シャーディングキー**: `merchant_id`
- 取引は`merchant_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

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
   - 用途: 在庫情報、顧客情報、マーチャント情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **外部決済ゲートウェイ**: カードネットワークへのAPI呼び出し
2. **在庫更新**: リアルタイム在庫更新の処理
3. **レポート生成**: 大量データの集計

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 在庫更新最適化

1. **キャッシング**: 在庫情報をキャッシュ
2. **バッチ更新**: 複数の在庫更新をバッチで処理
3. **非同期処理**: 在庫更新を非同期で処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **レポート生成**:
   ```
   Topic: report-generation
   Partition Key: merchant_id
   ```

2. **在庫アラート**:
   ```
   Topic: inventory-alerts
   Partition Key: merchant_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 400万企業
- **日間アクティブユーザー**: 200万企業
- **1日の取引数**: 5,000万件

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 600台（リージョン間で分散）
- コスト: $0.192/時間 × 600台 × 730時間 = **$84,096/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**ストレージ**:
- EBS: 100 TB
- コスト: $0.10/GB/月 × 100,000 GB = **$10,000/月**

**ネットワーク**:
- データ転送: 200 TB/月
- コスト: $0.09/GB × 200,000 GB = **$18,000/月**

**合計**: 約 **$150,056/月**（約1,800,672ドル/年）

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
   - バックアップの保存期間: 7年（規制要件）

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 1時間
   - RPO（Recovery Point Objective）: 0（ゼロデータロス）

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - マーチャントは自分の取引のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - カード情報: PCI DSS準拠（トークン化）

### PCI DSS準拠

1. **カード情報の非保存**: カード情報は保存せず、トークン化
2. **セキュアな通信**: TLS 1.3で暗号化
3. **アクセス制御**: 厳格なアクセス制御

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - マーチャントベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **POS決済**: < 3秒
- **在庫更新**: < 1秒

### プログレッシブローディング

1. **レポートの遅延読み込み**:
   - レポートを非同期で生成
   - 進捗を表示

2. **エラーハンドリング**:
   - 分かりやすいエラーメッセージ

## 12. 実装例

### POS決済サービス（疑似コード）

```python
class POSPaymentService:
    def __init__(self, db, cache, payment_gateway, inventory_service, customer_service):
        self.db = db
        self.cache = cache
        self.payment_gateway = payment_gateway
        self.inventory_service = inventory_service
        self.customer_service = customer_service
    
    async def process_payment(self, merchant_id: int, amount: float, 
                            payment_method: str, items: list, customer_id: int = None):
        # 在庫を確認
        for item in items:
            available = await self.inventory_service.check_stock(
                item_id=item["item_id"],
                quantity=item["quantity"]
            )
            if not available:
                raise InsufficientStockError(f"Insufficient stock for item {item['item_id']}")
        
        # 外部決済ゲートウェイに決済リクエストを送信
        payment_result = await self.payment_gateway.process_payment(
            amount=amount,
            payment_method=payment_method
        )
        
        if payment_result['status'] == 'success':
            # トランザクションで決済を処理
            async with self.db.transaction():
                # 決済を作成
                transaction_id = await self.db.insert_transaction(
                    merchant_id=merchant_id,
                    customer_id=customer_id,
                    amount=amount,
                    payment_method=payment_method,
                    status='completed'
                )
                
                # 在庫を更新
                for item in items:
                    await self.inventory_service.update_stock(
                        item_id=item["item_id"],
                        quantity_change=-item["quantity"]
                    )
                
                # 顧客履歴を更新
                if customer_id:
                    await self.customer_service.update_customer_history(
                        customer_id=customer_id,
                        amount=amount
                    )
        
        return {
            "id": transaction_id,
            "status": "completed",
            "amount": amount,
            "receipt_url": f"https://square.com/receipt/{transaction_id}"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の在庫照会**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の取引数**: 5,000万件
- **1時間あたり**: 5,000万 / 24 = 約208万件
- **1秒あたり**: 208万 / 3600 = 約578件/秒
- **ピーク時（3倍）**: 約1,734件/秒

### ストレージ見積もり

#### 取引ストレージ

- **1取引あたりのサイズ**: 約2 KB
- **1日の取引数**: 5,000万件
- **1日のストレージ**: 5,000万 × 2 KB = 100 GB
- **1年のストレージ**: 100 GB × 365 = 約36.5 TB
- **7年のストレージ**: 約255.5 TB（規制要件）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **PCI DSS準拠**: カード情報の非保存とトークン化
4. **在庫管理**: リアルタイム在庫更新の実装
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **在庫の競合**:
   - 問題: 同時決済で在庫の競合が発生
   - 解決策: 楽観的ロックとトランザクション

2. **外部決済ゲートウェイのレイテンシ**:
   - 問題: 外部API呼び出しが遅い
   - 解決策: タイムアウト設定とリトライロジック

## 15. 関連システム

### 類似システムへのリンク

- [PayPal](paypal_design.md) - 決済プラットフォーム
- [Stripe](stripe_design.md) - 決済プラットフォーム
- [Venmo](venmo_design.md) - P2P決済プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Azure](../13_cloud_services/azure_design.md)でクラウドサービスの設計を学ぶ

