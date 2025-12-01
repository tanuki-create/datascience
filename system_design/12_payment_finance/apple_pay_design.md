# Apple Pay システム設計

## 1. システム概要

### 目的と主要機能

Apple Payは、Appleが提供するモバイル決済システムです。iPhone、iPad、Apple Watch、MacでNFC、Touch ID/Face ID、トークン化を使用して安全な決済を提供します。

**主要機能**:
- NFC決済（店舗での決済）
- アプリ内決済
- Web決済
- トークン化（カード情報の保護）
- Touch ID/Face ID認証
- Apple Cash（P2P送金）
- Apple Card統合

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日の取引数**: 約5,000万件
- **1日の取引額**: 約20億ドル
- **1秒あたりの取引数**: 約600件/秒（ピーク時）
- **年間取引額**: 約7,300億ドル

### 主要なユースケース

1. **店舗決済**: NFCを使用した店舗での決済
2. **アプリ内決済**: アプリ内での決済
3. **Web決済**: Webサイトでの決済
4. **Apple Cash**: P2P送金
5. **定期課金**: サブスクリプション決済

## 2. 機能要件

### コア機能

1. **決済処理**
   - NFC決済（店舗）
   - アプリ内決済
   - Web決済
   - トークン化決済

2. **認証**
   - Touch ID認証
   - Face ID認証
   - パスコード認証

3. **カード管理**
   - カードの追加・削除
   - カード情報のトークン化
   - カード情報の暗号化保存

4. **Apple Cash**
   - P2P送金
   - 残高管理
   - 取引履歴

5. **Apple Card統合**
   - Apple Cardの管理
   - キャッシュバック計算
   - 支払い履歴

### 非機能要件

- **可用性**: 99.99%以上（年間ダウンタイム < 52.56分）
- **一貫性**: 決済情報は強い一貫性が必要
- **パフォーマンス**:
  - NFC決済処理: < 1秒
  - アプリ内決済処理: < 2秒
  - Web決済処理: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 決済情報は永続的に保存
- **セキュリティ**: PCI DSS準拠、トークン化、生体認証

### 優先順位付け

1. **P0（必須）**: 決済処理、認証、トークン化
2. **P1（重要）**: Apple Cash、カード管理、Apple Card統合
3. **P2（望ましい）**: 高度な分析・レポート、不正検出

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (iPhone, iPad, Apple Watch, Mac)
└──────┬──────┘
       │ HTTPS / NFC
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
│  │ Payment  │  │ Token    │  │ Apple    │        │
│  │ Service  │  │ Service  │  │ Cash     │        │
│  │          │  │          │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Authentication Service          │         │
│  │      Card Management Service         │         │
│  │      Fraud Detection Service        │         │
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
│         Tokenization Service (HSM)                 │
│         Bank API (Apple Cash)                     │
│         Apple Card API                            │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Payment Service**: 決済処理
   - **Token Service**: トークン化処理
   - **Apple Cash Service**: Apple Cashの管理
   - **Authentication Service**: Touch ID/Face ID認証
   - **Card Management Service**: カード管理
   - **Fraud Detection Service**: 不正検出
4. **Database**: 決済、カード情報、Apple Cashの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（決済、不正検出など）
7. **Payment Gateway**: 外部決済ゲートウェイ（カードネットワーク）
8. **Tokenization Service**: HSM（Hardware Security Module）を使用したトークン化
9. **Bank API**: 銀行API（Apple Cash用）
10. **Apple Card API**: Apple Card統合用API

### データフロー

#### NFC決済処理のフロー

```
1. Client (iPhone) → NFC → Payment Terminal
2. Payment Terminal → Load Balancer → API Gateway
3. API Gateway → Payment Service
4. Payment Service:
   a. Touch ID/Face ID認証を要求
   b. 認証成功後、トークンを取得
   c. Token Serviceでトークンを検証
   d. Payment Gatewayに決済リクエストを送信
   e. 決済結果をデータベースに保存
   f. 決済結果を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Payments テーブル

```sql
CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('pending', 'succeeded', 'failed', 'refunded') DEFAULT 'pending',
    payment_token VARCHAR(200) NOT NULL,
    payment_method ENUM('nfc', 'app', 'web') NOT NULL,
    merchant_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Payment_Tokens テーブル

```sql
CREATE TABLE payment_tokens (
    token_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    device_token VARCHAR(200) NOT NULL,
    card_token VARCHAR(200) NOT NULL,
    card_last4 VARCHAR(4) NOT NULL,
    card_brand VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_device_token (device_token),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB;
```

#### Apple_Cash_Transactions テーブル

```sql
CREATE TABLE apple_cash_transactions (
    transaction_id BIGINT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 決済、カード情報、Apple Cashの永続化
- **Redis**:
  - 理由: リアルタイムデータ、認証トークン
  - 用途: 認証トークン、セッション情報

### スキーマ設計の考慮事項

1. **パーティショニング**: `payments`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 決済は時系列で保存
4. **トークン化**: カード情報はトークンとして保存（実際のカード情報は保存しない）

## 5. API設計

### 主要なAPIエンドポイント

#### 決済処理

```
POST /api/v1/payments
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "amount": 100.00,
  "currency": "USD",
  "payment_token": "<device_token>",
  "payment_method": "nfc",
  "merchant_id": 1234567890
}

Response (200 OK):
{
  "payment_id": 9876543210,
  "status": "succeeded",
  "amount": 100.00,
  "currency": "USD",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### トークン生成

```
POST /api/v1/tokens
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "card_number": "4111111111111111",
  "expiry_date": "12/25",
  "cvv": "123"
}

Response (200 OK):
{
  "token_id": 1234567890,
  "device_token": "<device_token>",
  "card_last4": "1111",
  "card_brand": "Visa"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Apple ID統合
- **認可**: ユーザーは自分の決済情報のみアクセス可能
- **生体認証**: Touch ID/Face ID認証
- **レート制限**: 
  - 決済処理: 100回/分
  - トークン生成: 10回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- 決済は`user_id`でシャーディング

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
   - 用途: 認証トークン、セッション情報、カード情報
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **決済処理**: Payment Gatewayへのリクエスト
2. **トークン化**: HSMへのアクセス
3. **認証**: Touch ID/Face ID認証

### 決済処理最適化

1. **非同期処理**: 決済処理を非同期で処理
2. **キャッシング**: 頻繁にアクセスされるデータをキャッシュ
3. **接続プール**: Payment Gatewayへの接続をプール

### トークン化最適化

1. **HSMクラスター**: 複数のHSMを使用
2. **トークンキャッシュ**: トークンをキャッシュ
3. **バッチ処理**: 複数のトークンをバッチで処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **決済処理**:
   ```
   Topic: payment-processing
   Partition Key: user_id
   ```

2. **不正検出**:
   ```
   Topic: fraud-detection
   Partition Key: payment_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 5億人
- **日間アクティブユーザー**: 2億人
- **1日の取引数**: 5,000万件

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,500台（リージョン間で分散）
- コスト: $0.192/時間 × 1,500台 × 730時間 = **$210,240/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 100台（マスター + レプリカ）
- コスト: $0.76/時間 × 100台 × 730時間 = **$55,480/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 200台
- コスト: $0.175/時間 × 200台 × 730時間 = **$25,550/月**

**HSM（AWS CloudHSM）**:
- CloudHSMインスタンス: 50台
- コスト: $1.25/時間 × 50台 × 730時間 = **$45,625/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.09/GB × 10,000,000 GB = **$900,000/月**

**合計**: 約 **$1,236,895/月**（約14,842,740ドル/年）

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
   - HSMの冗長化

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Payment Gatewayのヘルスチェック

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

2. **トークン化データバックアップ**:
   - HSMのバックアップ
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Apple ID統合
   - Touch ID/Face ID認証

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の決済情報のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - HSM: ハードウェア暗号化

### トークン化

1. **カード情報の保護**: カード情報はトークンとして保存
2. **HSM**: ハードウェアセキュリティモジュールを使用
3. **PCI DSS準拠**: PCI DSS準拠の実装

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
- **NFC決済処理**: < 1秒
- **アプリ内決済処理**: < 2秒

### プログレッシブローディング

1. **決済履歴の遅延読み込み**:
   - 最初の20件を先に表示
   - 残りの決済はスクロール時に読み込み

2. **カード一覧の遅延読み込み**:
   - 最初の5件を先に表示
   - 残りのカードは必要時に読み込み

## 12. 実装例

### 決済サービス（疑似コード）

```python
class PaymentService:
    def __init__(self, db, cache, token_service, payment_gateway):
        self.db = db
        self.cache = cache
        self.token_service = token_service
        self.payment_gateway = payment_gateway
    
    async def process_payment(self, user_id: int, amount: float, 
                            payment_token: str, payment_method: str):
        # トークンを検証
        token_info = await self.token_service.verify_token(payment_token)
        
        if not token_info:
            raise InvalidTokenError("Invalid payment token")
        
        # 決済を処理
        payment_result = await self.payment_gateway.charge(
            amount=amount,
            token=token_info["card_token"],
            currency="USD"
        )
        
        # 決済結果を保存
        payment_id = await self.db.insert_payment(
            user_id=user_id,
            amount=amount,
            status=payment_result["status"],
            payment_token=payment_token,
            payment_method=payment_method
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"user:{user_id}:payments")
        
        return {
            "payment_id": payment_id,
            "status": payment_result["status"],
            "amount": amount,
            "created_at": datetime.now()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の決済履歴アクセス**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の決済数**: 5,000万件
- **1時間あたり**: 5,000万 / 24 = 約208万回
- **1秒あたり**: 208万 / 3600 = 約578回/秒
- **ピーク時（3倍）**: 約1,734回/秒

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **トークン化**: カード情報はトークンとして保存
2. **生体認証**: Touch ID/Face ID認証を使用
3. **HSM**: ハードウェアセキュリティモジュールを使用
4. **PCI DSS準拠**: PCI DSS準拠の実装
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **トークン化の実装**:
   - 問題: トークン化の実装が不適切
   - 解決策: HSMを使用したトークン化

2. **決済処理のスケーラビリティ**:
   - 問題: 決済処理のボトルネック
   - 解決策: 非同期処理とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [PayPal](paypal_design.md) - 決済システム
- [Stripe](stripe_design.md) - 決済APIプラットフォーム
- [Venmo](venmo_design.md) - P2P決済アプリ
- [Google Pay](google_pay_design.md) - モバイル決済システム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Rate Limiting](../17_common_patterns/rate_limiting.md) - レート制限

---

**次のステップ**: [Google Pay](google_pay_design.md)でモバイル決済システムの設計を学ぶ

