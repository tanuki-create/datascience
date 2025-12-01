# Venmo システム設計

## 1. システム概要

### 目的と主要機能

Venmoは、P2P（Peer-to-Peer）決済プラットフォームです。ユーザー間での送金を簡単に行えます。

**主要機能**:
- P2P送金
- 請求・分割払い
- ソーシャルフィード
- 銀行口座連携
- デビットカード発行
- ビジネス決済

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約8,000万人
- **日間アクティブユーザー（DAU）**: 約3,000万人
- **1日の取引数**: 約2,000万件
- **1日の取引額**: 約5億ドル
- **1秒あたりの取引数**: 約230件/秒（ピーク時）

### 主要なユースケース

1. **P2P送金**: ユーザー間での送金
2. **請求**: ユーザーが他のユーザーに請求
3. **分割払い**: 複数人での費用分割
4. **ソーシャルフィード**: 取引の公開表示
5. **銀行口座連携**: 銀行口座への送金・入金

## 2. 機能要件

### コア機能

1. **P2P送金**
   - ユーザー間での送金
   - 即時送金
   - 標準送金（1-3営業日）

2. **請求・分割払い**
   - 他のユーザーへの請求
   - 複数人での費用分割

3. **ソーシャルフィード**
   - 取引の公開表示
   - コメント・絵文字

4. **銀行口座連携**
   - 銀行口座への送金
   - 銀行口座からの入金

5. **デビットカード**
   - Venmoデビットカードの発行
   - カード決済

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 決済情報は強い一貫性が必要
- **パフォーマンス**:
  - P2P送金: < 2秒
  - 残高確認: < 100ms
  - ソーシャルフィード表示: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 決済情報は永続的に保存
- **セキュリティ**: PCI DSS準拠

### 優先順位付け

1. **P0（必須）**: P2P送金、請求・分割払い、銀行口座連携
2. **P1（重要）**: ソーシャルフィード、デビットカード、不正検出
3. **P2（望ましい）**: 高度なソーシャル機能、分析・レポート

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps, Web)
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
│  │ Payment  │  │  Social  │  │  Bank    │        │
│  │ Service  │  │  Feed    │  │  Service │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Account Service                 │         │
│  │      Fraud Detection Service         │         │
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
│         Bank API (ACH, Wire Transfer)            │
│         Card Network API                         │
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Payment Service**: P2P送金の処理
   - **Social Feed Service**: ソーシャルフィードの管理
   - **Bank Service**: 銀行口座連携の処理
   - **Account Service**: アカウント管理
   - **Fraud Detection Service**: 不正検出
4. **Database**: 決済、アカウント、ソーシャルフィードの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（銀行送金、通知など）
7. **Bank API**: 銀行API（ACH、Wire Transfer）
8. **Card Network API**: カードネットワークAPI
9. **CDN**: 画像の配信

### データフロー

#### P2P送金のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Payment Service
3. Payment Service:
   a. 送金元アカウントの残高を確認
   b. Fraud Detection Serviceで不正検出
   c. 送金をデータベースに保存
   d. 送金元アカウントの残高を減算
   e. 送金先アカウントの残高を加算
   f. ソーシャルフィードに投稿（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Accounts テーブル

```sql
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    status ENUM('active', 'suspended', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

#### Transactions テーブル

```sql
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    from_account_id BIGINT,
    to_account_id BIGINT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    note VARCHAR(200),
    visibility ENUM('public', 'friends', 'private') DEFAULT 'public',
    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (to_account_id) REFERENCES accounts(account_id),
    INDEX idx_from_account_id (from_account_id),
    INDEX idx_to_account_id (to_account_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Social_Feed テーブル

```sql
CREATE TABLE social_feed (
    feed_id BIGINT PRIMARY KEY,
    transaction_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    note VARCHAR(200),
    visibility ENUM('public', 'friends', 'private') DEFAULT 'public',
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 決済、アカウント、ソーシャルフィードの永続化
- **Redis**:
  - 理由: リアルタイムデータ、ソーシャルフィード
  - 用途: ソーシャルフィード、セッション管理

### スキーマ設計の考慮事項

1. **パーティショニング**: `transactions`テーブルは`from_account_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 取引は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### P2P送金

```
POST /api/v1/payments
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "amount": 50.00,
  "note": "Dinner",
  "target": {
    "user": "user_1234567890"
  },
  "visibility": "public"
}

Response (200 OK):
{
  "id": "payment_1234567890",
  "status": "completed",
  "amount": 50.00,
  "note": "Dinner",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### ソーシャルフィード取得

```
GET /api/v1/social_feed?limit=20&offset=0
Authorization: Bearer <token>

Response (200 OK):
{
  "feed": [
    {
      "id": "feed_1234567890",
      "user": "John Doe",
      "amount": 50.00,
      "note": "Dinner",
      "like_count": 5,
      "comment_count": 2,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "has_more": true
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の取引のみアクセス可能
- **レート制限**: 
  - P2P送金: 10回/分
  - ソーシャルフィード取得: 100回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Account IDベースのシャーディング

```
Shard 1: account_id % 8 == 0
Shard 2: account_id % 8 == 1
...
Shard 8: account_id % 8 == 7
```

**シャーディングキー**: `account_id`
- 取引は`account_id`でシャーディング

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
   - 用途: アカウント情報、ソーシャルフィード、残高
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **銀行API呼び出し**: 銀行口座連携のAPI呼び出し
2. **ソーシャルフィード**: 大量のフィードデータの取得
3. **不正検出**: 機械学習モデルの推論

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ソーシャルフィード最適化

1. **キャッシング**: 人気フィードをキャッシュ
2. **遅延読み込み**: フィードを遅延読み込み
3. **事前計算**: フィードを事前計算

### 非同期処理

#### メッセージキュー（Kafka）

1. **銀行送金**:
   ```
   Topic: bank-transfers
   Partition Key: account_id
   ```

2. **ソーシャルフィード更新**:
   ```
   Topic: social-feed-updates
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 8,000万人
- **日間アクティブユーザー**: 3,000万人
- **1日の取引数**: 2,000万件

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 400台（リージョン間で分散）
- コスト: $0.192/時間 × 400台 × 730時間 = **$56,064/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**ストレージ**:
- EBS: 30 TB
- コスト: $0.10/GB/月 × 30,000 GB = **$3,000/月**

**ネットワーク**:
- データ転送: 50 TB/月
- コスト: $0.09/GB × 50,000 GB = **$4,500/月**

**合計**: 約 **$93,421/月**（約1,121,052ドル/年）

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
   - ユーザーは自分の取引のみアクセス可能

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
   - ユーザーベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **P2P送金**: < 2秒
- **ソーシャルフィード表示**: < 1秒

### プログレッシブローディング

1. **ソーシャルフィードの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのフィードはスクロール時に読み込み

2. **エラーハンドリング**:
   - 分かりやすいエラーメッセージ

## 12. 実装例

### 決済サービス（疑似コード）

```python
class PaymentService:
    def __init__(self, db, cache, fraud_detection_service, message_queue):
        self.db = db
        self.cache = cache
        self.fraud_detection_service = fraud_detection_service
        self.message_queue = message_queue
    
    async def send_payment(self, from_account_id: int, to_account_id: int, 
                          amount: float, note: str, visibility: str):
        # 送金元アカウントの残高を確認
        from_account = await self.db.get_account(account_id=from_account_id)
        
        if from_account["balance"] < amount:
            raise InsufficientBalanceError("Insufficient balance")
        
        # 不正検出
        fraud_score = await self.fraud_detection_service.detect_fraud(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount
        )
        
        if fraud_score > 0.8:
            raise FraudDetectedError("Fraud detected")
        
        # トランザクションで送金を処理
        async with self.db.transaction():
            # 送金を作成
            transaction_id = await self.db.insert_transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                note=note,
                visibility=visibility,
                status='completed'
            )
            
            # 送金元アカウントの残高を減算
            await self.db.update_account_balance(
                account_id=from_account_id,
                balance_change=-amount
            )
            
            # 送金先アカウントの残高を加算
            await self.db.update_account_balance(
                account_id=to_account_id,
                balance_change=amount
            )
        
        # ソーシャルフィードに投稿（非同期）
        await self.message_queue.publish(
            topic="social-feed-updates",
            message={
                "transaction_id": transaction_id,
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "amount": amount,
                "note": note,
                "visibility": visibility
            },
            partition_key=from_account_id
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"account:{from_account_id}:balance")
        await self.cache.delete(f"account:{to_account_id}:balance")
        
        return {
            "id": transaction_id,
            "status": "completed",
            "amount": amount,
            "note": note
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のソーシャルフィードアクセス**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の取引数**: 2,000万件
- **1時間あたり**: 2,000万 / 24 = 約83.3万件
- **1秒あたり**: 83.3万 / 3600 = 約231件/秒
- **ピーク時（3倍）**: 約693件/秒

### ストレージ見積もり

#### 取引ストレージ

- **1取引あたりのサイズ**: 約1 KB
- **1日の取引数**: 2,000万件
- **1日のストレージ**: 2,000万 × 1 KB = 20 GB
- **1年のストレージ**: 20 GB × 365 = 約7.3 TB
- **7年のストレージ**: 約51.1 TB（規制要件）

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

2. **ソーシャルフィードのスケーラビリティ**:
   - 問題: 大量のフィードデータの取得が遅い
   - 解決策: キャッシングと遅延読み込み

## 15. 関連システム

### 類似システムへのリンク

- [PayPal](paypal_design.md) - 決済プラットフォーム
- [Stripe](stripe_design.md) - 決済プラットフォーム
- [Square](square_design.md) - 決済プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Square](square_design.md)で決済プラットフォームの設計を学ぶ

