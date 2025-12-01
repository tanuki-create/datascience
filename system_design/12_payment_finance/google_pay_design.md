# Google Pay システム設計

## 1. システム概要

### 目的と主要機能

Google Payは、Googleが提供するモバイル決済システムです。Androidデバイス、Web、iOSでNFC、指紋認証、トークン化を使用して安全な決済を提供します。

**主要機能**:
- NFC決済（店舗での決済）
- アプリ内決済
- Web決済
- トークン化（カード情報の保護）
- 指紋認証・顔認証
- Google Pay Send（P2P送金）
- Google Pay Balance（残高管理）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約4億人
- **日間アクティブユーザー（DAU）**: 約1.5億人
- **1日の取引数**: 約4,000万件
- **1日の取引額**: 約15億ドル
- **1秒あたりの取引数**: 約500件/秒（ピーク時）
- **年間取引額**: 約5,475億ドル

### 主要なユースケース

1. **店舗決済**: NFCを使用した店舗での決済
2. **アプリ内決済**: アプリ内での決済
3. **Web決済**: Webサイトでの決済
4. **Google Pay Send**: P2P送金
5. **定期課金**: サブスクリプション決済

## 2. 機能要件

### コア機能

1. **決済処理**
   - NFC決済（店舗）
   - アプリ内決済
   - Web決済
   - トークン化決済

2. **認証**
   - 指紋認証
   - 顔認証
   - パスコード認証

3. **カード管理**
   - カードの追加・削除
   - カード情報のトークン化
   - カード情報の暗号化保存

4. **Google Pay Send**
   - P2P送金
   - 残高管理
   - 取引履歴

5. **Google Pay Balance**
   - 残高管理
   - チャージ・引き出し
   - 取引履歴

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
2. **P1（重要）**: Google Pay Send、カード管理、Google Pay Balance
3. **P2（望ましい）**: 高度な分析・レポート、不正検出

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Android, iOS, Web)
└──────┬──────┘
       │ HTTPS / NFC
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer (Google Cloud LB)     │
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
│  │ Payment  │  │ Token    │  │ Google   │        │
│  │ Service  │  │ Service  │  │ Pay Send │        │
│  │          │  │          │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Authentication Service          │         │
│  │      Card Management Service         │         │
│  │      Balance Service                │         │
│  │      Fraud Detection Service        │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┐
        │                 │                  │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│   Database   │  │   Cache       │  │  Message     │
│   (Sharded)  │  │   (Redis)     │  │  Queue       │
│              │  │               │  │  (Pub/Sub)   │
└───────┬──────┘  └───────────────┘  └──────────────┘
        │
        │
┌───────▼──────────────────────────────────────────┐
│         Payment Gateway (External)                │
│         Tokenization Service (HSM)               │
│         Bank API (Google Pay Send)                │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Payment Service**: 決済処理
   - **Token Service**: トークン化処理
   - **Google Pay Send Service**: Google Pay Sendの管理
   - **Authentication Service**: 指紋認証・顔認証
   - **Card Management Service**: カード管理
   - **Balance Service**: Google Pay Balanceの管理
   - **Fraud Detection Service**: 不正検出
4. **Database**: 決済、カード情報、Google Pay Sendの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（決済、不正検出など）
7. **Payment Gateway**: 外部決済ゲートウェイ（カードネットワーク）
8. **Tokenization Service**: HSM（Hardware Security Module）を使用したトークン化
9. **Bank API**: 銀行API（Google Pay Send用）

### データフロー

#### NFC決済処理のフロー

```
1. Client (Android) → NFC → Payment Terminal
2. Payment Terminal → Load Balancer → API Gateway
3. API Gateway → Payment Service
4. Payment Service:
   a. 指紋認証・顔認証を要求
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

#### Google_Pay_Send_Transactions テーブル

```sql
CREATE TABLE google_pay_send_transactions (
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

#### User_Balances テーブル

```sql
CREATE TABLE user_balances (
    user_id BIGINT PRIMARY KEY,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'USD',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_balance (balance)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（Cloud SQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 決済、カード情報、Google Pay Sendの永続化
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

- **認証**: OAuth 2.0 / JWT、Google Account統合
- **認可**: ユーザーは自分の決済情報のみアクセス可能
- **生体認証**: 指紋認証・顔認証
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

- **Load Balancer**: Google Cloud Load Balancer
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
3. **認証**: 指紋認証・顔認証

### 決済処理最適化

1. **非同期処理**: 決済処理を非同期で処理
2. **キャッシング**: 頻繁にアクセスされるデータをキャッシュ
3. **接続プール**: Payment Gatewayへの接続をプール

### トークン化最適化

1. **HSMクラスター**: 複数のHSMを使用
2. **トークンキャッシュ**: トークンをキャッシュ
3. **バッチ処理**: 複数のトークンをバッチで処理

### 非同期処理

#### メッセージキュー（Pub/Sub）

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

- **月間アクティブユーザー**: 4億人
- **日間アクティブユーザー**: 1.5億人
- **1日の取引数**: 4,000万件

#### サーバーコスト（GCP）

**アプリケーションサーバー**:
- Compute Engine: n1-standard-4 (4 vCPU, 15 GB RAM)
- インスタンス数: 1,200台（リージョン間で分散）
- コスト: $0.19/時間 × 1,200台 × 730時間 = **$166,440/月**

**データベース**:
- Cloud SQL: db-n1-standard-8 (8 vCPU, 30 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.75/時間 × 80台 × 730時間 = **$43,800/月**

**キャッシュ（Memorystore）**:
- Redis Standard Tier: 26 GB RAM
- インスタンス数: 150台
- コスト: $0.17/時間 × 150台 × 730時間 = **$18,615/月**

**HSM（Cloud HSM）**:
- Cloud HSMインスタンス: 40台
- コスト: $1.25/時間 × 40台 × 730時間 = **$36,500/月**

**ネットワーク**:
- データ転送: 8 PB/月
- コスト: $0.12/GB × 8,000,000 GB = **$960,000/月**

**合計**: 約 **$1,225,355/月**（約14,704,260ドル/年）

### コスト削減戦略

1. **コミットメント割引**: 1年契約で最大57%削減
2. **プリエンプティブルインスタンス**: 非クリティカルなワークロードで最大80%削減
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
   - Google Account統合
   - 指紋認証・顔認証

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の決済情報のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ
   - HSM: ハードウェア暗号化

### トークン化

1. **カード情報の保護**: カード情報はトークンとして保存
2. **HSM**: ハードウェアセキュリティモジュールを使用
3. **PCI DSS準拠**: PCI DSS準拠の実装

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - ユーザーベースのレート制限

2. **CDN**: Google Cloud Armor
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

- **1日の決済履歴アクセス**: 8億回
- **1時間あたり**: 8億 / 24 = 約3,333万回
- **1秒あたり**: 3,333万 / 3600 = 約9,259回/秒
- **ピーク時（3倍）**: 約27,777回/秒

#### 書き込みトラフィック

- **1日の決済数**: 4,000万件
- **1時間あたり**: 4,000万 / 24 = 約167万回
- **1秒あたり**: 167万 / 3600 = 約464回/秒
- **ピーク時（3倍）**: 約1,392回/秒

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **トークン化**: カード情報はトークンとして保存
2. **生体認証**: 指紋認証・顔認証を使用
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
- [Apple Pay](apple_pay_design.md) - モバイル決済システム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Rate Limiting](../17_common_patterns/rate_limiting.md) - レート制限

---

**次のステップ**: [LINE](../04_messaging/line_design.md)でメッセージングシステムの設計を学ぶ

