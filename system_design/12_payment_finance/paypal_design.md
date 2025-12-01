# PayPal システム設計

## 1. システム概要

### 目的と主要機能

PayPalは、オンライン決済を可能にする決済サービスプラットフォームです。

**主要機能**:
- アカウント作成と管理
- 送金と受金
- クレジットカード決済
- 請求書の発行
- 取引履歴

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約4億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日の取引数**: 約4,000万件
- **1日の取引額**: 約10億ドル

## 2. 機能要件

### コア機能

1. **決済処理**
   - クレジットカード決済
   - PayPal残高からの決済
   - 送金と受金

2. **アカウント管理**
   - アカウント作成
   - 残高管理
   - 取引履歴

3. **セキュリティ**
   - 不正検出
   - 2要素認証
   - 監査ログ

### 非機能要件

- **可用性**: 99.99%以上（金融システム）
- **パフォーマンス**:
  - 決済処理: < 2秒
  - 残高確認: < 100ms
- **一貫性**: 強い一貫性（ACID）
- **セキュリティ**: PCI DSS準拠

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
Payment Service → Database (ACID) → Payment Gateway
Account Service → Database → Cache
Fraud Detection Service → ML Service → Database
```

## 4. データモデル設計

### Accounts テーブル

```sql
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    status ENUM('active', 'suspended', 'closed') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;
```

### Transactions テーブル

```sql
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    from_account_id BIGINT,
    to_account_id BIGINT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    transaction_type ENUM('payment', 'transfer', 'refund') NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (to_account_id) REFERENCES accounts(account_id),
    INDEX idx_from_account_id (from_account_id),
    INDEX idx_to_account_id (to_account_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

## 5. API設計

### 決済処理

```
POST /api/v1/payments
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "to_account_id": 987654321,
  "amount": 100.00,
  "currency": "USD",
  "payment_method": "paypal_balance"
}

Response (201 Created):
{
  "transaction_id": 1234567890,
  "status": "completed",
  "amount": 100.00
}
```

## 6. スケーラビリティ設計

### データベースシャーディング

- **シャーディングキー**: `account_id`
- **シャーディング戦略**: `account_id % 32`

### トランザクション処理

- **分散トランザクション**: 2フェーズコミット
- **補償トランザクション**: 失敗時のロールバック

## 7. レイテンシ最適化

### 決済処理の最適化

- **非同期処理**: 不正検出を非同期で処理
- **キャッシング**: アカウント情報をキャッシュ

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$2,000,000/月**
- **データベース**: 約 **$1,000,000/月**（高可用性）
- **セキュリティ**: 約 **$500,000/月**
- **合計**: 約 **$3,500,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにデプロイ
- **データベースレプリケーション**: 同期レプリケーション
- **バックアップ**: 日次フルバックアップ

## 10. セキュリティ

### セキュリティ対策

- **PCI DSS準拠**: クレジットカード情報の安全な処理
- **トークン化**: クレジットカード情報をトークン化
- **不正検出**: 機械学習による不正検出
- **監査ログ**: 全ての取引を記録

## 11. UX最適化

### パフォーマンス指標

- **決済処理**: < 2秒
- **残高確認**: < 100ms
- **取引履歴**: < 500ms

## 12. 実装例

### 決済サービス（疑似コード）

```python
class PaymentService:
    def __init__(self, db, payment_gateway, fraud_detection):
        self.db = db
        self.payment_gateway = payment_gateway
        self.fraud_detection = fraud_detection
    
    async def process_payment(self, from_account_id: int, to_account_id: int, amount: decimal.Decimal):
        # トランザクション開始
        async with self.db.transaction():
            # 残高を確認
            from_account = await self.db.get_account(from_account_id)
            if from_account["balance"] < amount:
                raise ValueError("Insufficient balance")
            
            # 不正検出（非同期）
            fraud_score = await self.fraud_detection.check(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount
            )
            
            if fraud_score > 0.8:
                raise ValueError("Fraud detected")
            
            # 残高を更新
            await self.db.update_balance(from_account_id, -amount)
            await self.db.update_balance(to_account_id, amount)
            
            # 取引を記録
            transaction_id = await self.db.create_transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                status="completed"
            )
            
            return {
                "transaction_id": transaction_id,
                "status": "completed"
            }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の取引数**: 4,000万件
- **1秒あたり**: 約463件/秒（平均）
- **ピーク時**: 約1,400件/秒

### ストレージ見積もり

- **1取引あたりのサイズ**: 約1 KB
- **1日の取引ストレージ**: 4,000万 × 1 KB = 40 GB
- **1年の取引ストレージ**: 約14.6 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **ACID特性**: トランザクションの一貫性を保証
2. **不正検出**: 機械学習による不正検出
3. **監査ログ**: 全ての取引を記録

## 15. 関連システム

### 類似システムへのリンク

- [Stripe](stripe_design.md) - 決済APIプラットフォーム
- [Venmo](venmo_design.md) - P2P決済サービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [AWS](aws_design.md)でクラウドインフラの設計を学ぶ

