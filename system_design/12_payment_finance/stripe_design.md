# Stripe システム設計

## 1. システム概要

### 目的と主要機能

Stripeは、開発者向けの決済プラットフォームです。API経由でクレジットカード決済、サブスクリプション、送金などの機能を提供します。

**主要機能**:
- クレジットカード決済
- サブスクリプション管理
- 送金（Payout）
- 請求書（Invoice）
- 返金処理
- 不正検出
- マルチカレンシー

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約100万企業（API利用者）
- **1日の取引数**: 約1億件
- **1日の取引額**: 約10億ドル
- **1秒あたりの取引数**: 約1,200件/秒（ピーク時）
- **年間取引額**: 約3,650億ドル

### 主要なユースケース

1. **決済処理**: クレジットカード決済の処理
2. **サブスクリプション**: 定期課金の管理
3. **送金**: マーチャントへの送金
4. **返金処理**: 返金の処理
5. **不正検出**: 不正取引の検出

## 2. 機能要件

### コア機能

1. **決済処理**
   - クレジットカード決済
   - デビットカード決済
   - デジタルウォレット（Apple Pay、Google Pay）

2. **サブスクリプション管理**
   - 定期課金の作成・更新・キャンセル
   - 請求書の自動生成
   - 支払い失敗時の処理

3. **送金処理**
   - マーチャントへの送金
   - 複数の送金方法のサポート

4. **不正検出**
   - 機械学習ベースの不正検出
   - リアルタイム不正検出

5. **マルチカレンシー**
   - 複数の通貨のサポート
   - 為替レートの管理

### 非機能要件

- **可用性**: 99.99%以上（年間ダウンタイム < 52.56分）
- **一貫性**: 決済情報は強い一貫性が必要
- **パフォーマンス**:
  - 決済処理: < 2秒
  - 返金処理: < 5秒
  - 送金処理: < 1日
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 決済情報は永続的に保存
- **セキュリティ**: PCI DSS準拠

### 優先順位付け

1. **P0（必須）**: 決済処理、サブスクリプション管理、不正検出
2. **P1（重要）**: 送金処理、返金処理、マルチカレンシー
3. **P2（望ましい）**: 高度な不正検出、分析・レポート

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps, API Clients)
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
│  │ Payment  │  │ Subscription│ │ Payout  │        │
│  │ Service  │  │ Service   │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Fraud Detection Service         │         │
│  │      Refund Service                  │         │
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
│         ML Service (Fraud Detection)              │
│         Bank API (Payout)                         │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Payment Service**: 決済処理
   - **Subscription Service**: サブスクリプション管理
   - **Payout Service**: 送金処理
   - **Fraud Detection Service**: 不正検出
   - **Refund Service**: 返金処理
4. **Database**: 決済、サブスクリプション、送金の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（送金、不正検出など）
7. **Payment Gateway**: 外部決済ゲートウェイ（カードネットワーク）
8. **ML Service**: 機械学習ベースの不正検出
9. **Bank API**: 銀行API（送金用）

### データフロー

#### 決済処理のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Payment Service
3. Payment Service:
   a. 決済情報を検証
   b. Fraud Detection Serviceで不正検出
   c. Payment Gatewayに決済リクエストを送信
   d. 決済結果をデータベースに保存
   e. 決済結果を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Payments テーブル

```sql
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('pending', 'succeeded', 'failed', 'refunded') DEFAULT 'pending',
    payment_method_id BIGINT,
    payment_intent_id VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(payment_method_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Subscriptions テーブル

```sql
CREATE TABLE subscriptions (
    subscription_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    plan_id BIGINT NOT NULL,
    status ENUM('active', 'canceled', 'past_due', 'unpaid') DEFAULT 'active',
    current_period_start TIMESTAMP NOT NULL,
    current_period_end TIMESTAMP NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Payouts テーブル

```sql
CREATE TABLE payouts (
    payout_id BIGINT PRIMARY KEY,
    account_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('pending', 'paid', 'failed', 'canceled') DEFAULT 'pending',
    arrival_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_id (account_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 決済、サブスクリプション、送金の永続化
- **Redis**:
  - 理由: リアルタイムデータ、レート制限
  - 用途: レート制限、セッション管理

### スキーマ設計の考慮事項

1. **パーティショニング**: `payments`テーブルは`customer_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 決済は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 決済作成

```
POST /api/v1/payment_intents
Authorization: Bearer <secret_key>
Content-Type: application/json

Request Body:
{
  "amount": 2000,
  "currency": "usd",
  "payment_method": "pm_1234567890",
  "customer": "cus_1234567890"
}

Response (200 OK):
{
  "id": "pi_1234567890",
  "amount": 2000,
  "currency": "usd",
  "status": "succeeded",
  "client_secret": "pi_1234567890_secret_xyz"
}
```

#### サブスクリプション作成

```
POST /api/v1/subscriptions
Authorization: Bearer <secret_key>
Content-Type: application/json

Request Body:
{
  "customer": "cus_1234567890",
  "items": [
    {
      "price": "price_1234567890"
    }
  ]
}

Response (200 OK):
{
  "id": "sub_1234567890",
  "status": "active",
  "current_period_start": 1640995200,
  "current_period_end": 1643587200
}
```

### 認証・認可

- **認証**: API Key（Secret Key、Publishable Key）
- **認可**: API Keyベースのアクセス制御
- **レート制限**: 
  - 決済作成: 100回/秒
  - サブスクリプション作成: 10回/秒

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Customer IDベースのシャーディング

```
Shard 1: customer_id % 8 == 0
Shard 2: customer_id % 8 == 1
...
Shard 8: customer_id % 8 == 7
```

**シャーディングキー**: `customer_id`
- 決済は`customer_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 顧客情報、プラン情報、レート制限
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **外部決済ゲートウェイ**: カードネットワークへのAPI呼び出し
2. **不正検出**: 機械学習モデルの推論
3. **送金処理**: 銀行API呼び出し

### 決済処理最適化

1. **非同期処理**: 決済処理を非同期で実行
2. **バッチ処理**: 複数の決済をバッチで処理
3. **キャッシング**: 顧客情報をキャッシュ

### 非同期処理

#### メッセージキュー（Kafka）

1. **送金処理**:
   ```
   Topic: payout-processing
   Partition Key: account_id
   ```

2. **不正検出**:
   ```
   Topic: fraud-detection
   Partition Key: payment_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **1日の取引数**: 1億件
- **1日の取引額**: 10億ドル

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 500台（リージョン間で分散）
- コスト: $0.192/時間 × 500台 × 730時間 = **$70,080/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**ストレージ**:
- EBS: 50 TB
- コスト: $0.10/GB/月 × 50,000 GB = **$5,000/月**

**ネットワーク**:
- データ転送: 100 TB/月
- コスト: $0.09/GB × 100,000 GB = **$9,000/月**

**合計**: 約 **$119,485/月**（約1,433,820ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - データベースの接続チェック
   - 外部決済ゲートウェイのヘルスチェック

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
   - API Key（Secret Key、Publishable Key）
   - OAuth 2.0（Connectアカウント用）

2. **認可**:
   - API Keyベースのアクセス制御
   - スコープベースのアクセス制御

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
   - API Keyベースのレート制限
   - IPアドレスベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **決済処理**: < 2秒

### プログレッシブローディング

1. **決済フォームの遅延読み込み**:
   - 必要な時だけ決済フォームを読み込み

2. **エラーハンドリング**:
   - 分かりやすいエラーメッセージ

## 12. 実装例

### 決済サービス（疑似コード）

```python
class PaymentService:
    def __init__(self, db, cache, payment_gateway, fraud_detection_service):
        self.db = db
        self.cache = cache
        self.payment_gateway = payment_gateway
        self.fraud_detection_service = fraud_detection_service
    
    async def create_payment(self, customer_id: int, amount: float, currency: str, payment_method_id: int):
        # 不正検出
        fraud_score = await self.fraud_detection_service.detect_fraud(
            customer_id=customer_id,
            amount=amount,
            payment_method_id=payment_method_id
        )
        
        if fraud_score > 0.8:
            raise FraudDetectedError("Fraud detected")
        
        # 決済を作成
        payment_intent_id = await self.db.insert_payment(
            customer_id=customer_id,
            amount=amount,
            currency=currency,
            payment_method_id=payment_method_id,
            status='pending'
        )
        
        # 外部決済ゲートウェイに決済リクエストを送信
        payment_result = await self.payment_gateway.process_payment(
            payment_intent_id=payment_intent_id,
            amount=amount,
            currency=currency,
            payment_method_id=payment_method_id
        )
        
        # 決済結果を更新
        await self.db.update_payment(
            payment_intent_id=payment_intent_id,
            status='succeeded' if payment_result['status'] == 'success' else 'failed'
        )
        
        return {
            "id": payment_intent_id,
            "amount": amount,
            "currency": currency,
            "status": payment_result['status']
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の決済照会**: 5億回
- **1時間あたり**: 5億 / 24 = 約2,083万回
- **1秒あたり**: 2,083万 / 3600 = 約5,787回/秒
- **ピーク時（3倍）**: 約17,361回/秒

#### 書き込みトラフィック

- **1日の取引数**: 1億件
- **1時間あたり**: 1億 / 24 = 約416万件
- **1秒あたり**: 416万 / 3600 = 約1,156件/秒
- **ピーク時（3倍）**: 約3,468件/秒

### ストレージ見積もり

#### 決済ストレージ

- **1決済あたりのサイズ**: 約2 KB
- **1日の取引数**: 1億件
- **1日のストレージ**: 1億 × 2 KB = 200 GB
- **1年のストレージ**: 200 GB × 365 = 約73 TB
- **7年のストレージ**: 約511 TB（規制要件）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **PCI DSS準拠**: カード情報の非保存とトークン化
4. **不正検出**: 機械学習ベースの不正検出
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **決済の重複処理**:
   - 問題: 同じ決済が複数回処理される
   - 解決策: べき等性の実装とトランザクション

2. **外部決済ゲートウェイのレイテンシ**:
   - 問題: 外部API呼び出しが遅い
   - 解決策: タイムアウト設定とリトライロジック

## 15. 関連システム

### 類似システムへのリンク

- [PayPal](paypal_design.md) - 決済プラットフォーム
- [Venmo](venmo_design.md) - P2P決済プラットフォーム
- [Square](square_design.md) - 決済プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Venmo](venmo_design.md)でP2P決済プラットフォームの設計を学ぶ

