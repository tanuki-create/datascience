# Booking.com システム設計

## 1. システム概要

### 目的と主要機能

Booking.comは、ホテル、アパートメント、その他の宿泊施設の予約プラットフォームです。世界中の宿泊施設を検索・予約できます。

**主要機能**:
- 宿泊施設検索
- 予約管理
- レビュー・評価
- 決済処理
- キャンセル管理
- 地図表示
- フィルター・ソート

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1億人
- **日間アクティブユーザー（DAU）**: 約3,000万人
- **1日の予約数**: 約150万件
- **1日の検索クエリ数**: 約5,000万クエリ
- **1秒あたりのリクエスト数**: 約10,000リクエスト/秒（ピーク時）
- **宿泊施設数**: 約2,800万件

### 主要なユースケース

1. **宿泊施設検索**: ユーザーが宿泊施設を検索
2. **予約作成**: ユーザーが予約を作成
3. **予約確認**: ユーザーが予約を確認
4. **レビュー投稿**: ユーザーがレビューを投稿
5. **キャンセル**: ユーザーが予約をキャンセル

## 2. 機能要件

### コア機能

1. **宿泊施設検索**
   - 場所・日付・人数での検索
   - フィルター・ソート機能
   - 地図表示

2. **予約管理**
   - 予約の作成・確認・キャンセル
   - 予約履歴の管理
   - 予約確認メール送信

3. **レビュー・評価**
   - レビューの投稿・閲覧
   - 評価の集計・表示

4. **決済処理**
   - クレジットカード決済
   - 複数の決済方法のサポート

5. **在庫管理**
   - 宿泊施設の在庫管理
   - リアルタイム在庫更新

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 予約情報は強い一貫性が必要
- **パフォーマンス**:
  - 検索結果表示: < 2秒
  - 予約作成: < 5秒
  - 在庫確認: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 予約情報は永続的に保存

### 優先順位付け

1. **P0（必須）**: 宿泊施設検索、予約作成、在庫管理
2. **P1（重要）**: 決済処理、レビュー・評価
3. **P2（望ましい）**: キャンセル管理、高度なフィルター

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
│  │ Search   │  │ Booking  │  │ Inventory│        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Payment Service                 │         │
│  │      Review Service                  │         │
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
│         Geospatial Database (PostGIS)            │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Search Service**: 宿泊施設検索の処理
   - **Booking Service**: 予約管理の処理
   - **Inventory Service**: 在庫管理の処理
   - **Payment Service**: 決済処理
   - **Review Service**: レビュー・評価の処理
4. **Database**: 宿泊施設、予約、ユーザー情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（予約確認メール送信など）
7. **Search Index**: 宿泊施設検索インデックス
8. **Geospatial Database**: 地図検索用の空間データベース
9. **CDN**: 画像の配信

### データフロー

#### 予約作成のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Booking Service
3. Booking Service:
   a. Inventory Serviceで在庫を確認
   b. 在庫があれば予約を作成
   c. Payment Serviceで決済処理
   d. 予約確認メールを送信（非同期）
   e. Inventory Serviceで在庫を更新
```

## 4. データモデル設計

### 主要なエンティティ

#### Properties テーブル

```sql
CREATE TABLE properties (
    property_id BIGINT PRIMARY KEY,
    property_name VARCHAR(500) NOT NULL,
    property_type ENUM('hotel', 'apartment', 'hostel', 'resort') NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(200) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    rating DECIMAL(3, 2),
    review_count INT DEFAULT 0,
    price_per_night DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city_country (city, country),
    INDEX idx_property_type (property_type),
    SPATIAL INDEX idx_location (latitude, longitude),
    FULLTEXT INDEX idx_property_name (property_name)
) ENGINE=InnoDB;
```

#### Bookings テーブル

```sql
CREATE TABLE bookings (
    booking_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    property_id BIGINT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    INDEX idx_user_id (user_id),
    INDEX idx_property_id (property_id),
    INDEX idx_check_in_date (check_in_date),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Inventory テーブル

```sql
CREATE TABLE inventory (
    property_id BIGINT NOT NULL,
    date DATE NOT NULL,
    available_rooms INT NOT NULL DEFAULT 0,
    booked_rooms INT NOT NULL DEFAULT 0,
    PRIMARY KEY (property_id, date),
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    INDEX idx_date (date)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 宿泊施設、予約、在庫の永続化
- **PostGIS**:
  - 理由: 空間クエリ、地図検索
  - 用途: 地理的検索
- **Elasticsearch**:
  - 理由: 全文検索、宿泊施設検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `bookings`テーブルは`property_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 在庫は日付ごとに管理

## 5. API設計

### 主要なAPIエンドポイント

#### 宿泊施設検索

```
GET /api/v1/properties/search?location=Paris&check_in=2024-06-01&check_out=2024-06-05&guests=2
Authorization: Bearer <token>

Response (200 OK):
{
  "properties": [
    {
      "property_id": 1234567890,
      "property_name": "Hotel Example",
      "price_per_night": 150.00,
      "rating": 4.5,
      "review_count": 1234
    }
  ],
  "total_results": 1000
}
```

#### 予約作成

```
POST /api/v1/bookings
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "property_id": 1234567890,
  "check_in_date": "2024-06-01",
  "check_out_date": "2024-06-05",
  "number_of_guests": 2,
  "payment_method": "credit_card"
}

Response (200 OK):
{
  "booking_id": 9876543210,
  "status": "confirmed",
  "total_price": 600.00
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の予約のみアクセス可能
- **レート制限**: 
  - 検索: 100リクエスト/分
  - 予約作成: 10回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Property IDベースのシャーディング

```
Shard 1: property_id % 8 == 0
Shard 2: property_id % 8 == 1
...
Shard 8: property_id % 8 == 7
```

**シャーディングキー**: `property_id`
- 予約は`property_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

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
   - 用途: 宿泊施設メタデータ、在庫情報、人気検索結果
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **検索**: Elasticsearchクエリの最適化
2. **在庫確認**: リアルタイム在庫更新の処理
3. **決済処理**: 外部決済API呼び出しのレイテンシ

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 検索最適化

1. **キャッシング**: 人気検索クエリの結果をキャッシュ
2. **インデックス最適化**: Elasticsearchインデックスの最適化
3. **並列検索**: 複数の検索条件を並列で実行

### 非同期処理

#### メッセージキュー（Kafka）

1. **予約確認メール送信**:
   ```
   Topic: booking-confirmation-emails
   Partition Key: booking_id
   ```

2. **在庫更新**:
   ```
   Topic: inventory-updates
   Partition Key: property_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1億人
- **日間アクティブユーザー**: 3,000万人
- **1日の予約数**: 150万件
- **1日の検索クエリ数**: 5,000万クエリ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 500台（リージョン間で分散）
- コスト: $0.192/時間 × 500台 × 730時間 = **$70,080/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 25台
- コスト: $0.76/時間 × 25台 × 730時間 = **$13,870/月**

**ストレージ**:
- EBS: 100 TB
- コスト: $0.10/GB/月 × 100,000 GB = **$10,000/月**

**ネットワーク**:
- データ転送: 1 PB/月
- コスト: $0.09/GB × 1,000,000 GB = **$90,000/月**

**合計**: 約 **$216,362/月**（約2,596,344ドル/年）

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
   - ユーザーは自分の予約のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - 決済情報: PCI DSS準拠

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
- **検索結果表示**: < 2秒
- **予約作成**: < 5秒

### プログレッシブローディング

1. **検索結果の遅延読み込み**:
   - 最初の20件を先に表示
   - 残りの結果はスクロール時に読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - サムネイルを先に表示

## 12. 実装例

### 予約サービス（疑似コード）

```python
class BookingService:
    def __init__(self, db, cache, inventory_service, payment_service, message_queue):
        self.db = db
        self.cache = cache
        self.inventory_service = inventory_service
        self.payment_service = payment_service
        self.message_queue = message_queue
    
    async def create_booking(self, user_id: int, property_id: int, 
                            check_in_date: str, check_out_date: str, 
                            number_of_guests: int, payment_method: str):
        # 在庫を確認
        is_available = await self.inventory_service.check_availability(
            property_id=property_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests
        )
        
        if not is_available:
            raise AvailabilityError("Property not available")
        
        # 価格を計算
        total_price = await self.calculate_price(
            property_id=property_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests
        )
        
        # 予約を作成
        booking_id = await self.db.insert_booking(
            user_id=user_id,
            property_id=property_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests,
            total_price=total_price,
            status='pending'
        )
        
        # 決済処理
        payment_result = await self.payment_service.process_payment(
            booking_id=booking_id,
            amount=total_price,
            payment_method=payment_method
        )
        
        if payment_result['status'] == 'success':
            # 予約を確定
            await self.db.update_booking(
                booking_id=booking_id,
                status='confirmed',
                payment_status='paid'
            )
            
            # 在庫を更新
            await self.inventory_service.update_inventory(
                property_id=property_id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                number_of_guests=number_of_guests
            )
            
            # 予約確認メールを送信（非同期）
            await self.message_queue.publish(
                topic="booking-confirmation-emails",
                message={
                    "booking_id": booking_id,
                    "user_id": user_id
                },
                partition_key=booking_id
            )
        
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "total_price": total_price
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の検索クエリ数**: 5,000万クエリ
- **1時間あたり**: 5,000万 / 24 = 約208万クエリ
- **1秒あたり**: 208万 / 3600 = 約578クエリ/秒
- **ピーク時（3倍）**: 約1,734クエリ/秒

#### 書き込みトラフィック

- **1日の予約数**: 150万件
- **1時間あたり**: 150万 / 24 = 約6.25万件
- **1秒あたり**: 6.25万 / 3600 = 約17.36件/秒
- **ピーク時（3倍）**: 約52.08件/秒

### ストレージ見積もり

#### 予約ストレージ

- **1予約あたりのサイズ**: 約1 KB
- **1日の予約数**: 150万件
- **1日のストレージ**: 150万 × 1 KB = 1.5 GB
- **1年のストレージ**: 1.5 GB × 365 = 約547.5 GB
- **5年のストレージ**: 約2.7375 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **在庫管理**: リアルタイム在庫更新の実装
4. **トランザクション**: 予約作成時のトランザクション処理
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **在庫の競合**:
   - 問題: 同時予約で在庫の競合が発生
   - 解決策: 楽観的ロックとトランザクション

2. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Airbnb](airbnb_design.md) - 宿泊施設予約プラットフォーム
- [Expedia](expedia_design.md) - 旅行予約プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Expedia](expedia_design.md)で旅行予約プラットフォームの設計を学ぶ

