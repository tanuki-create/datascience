# Airbnb システム設計

## 1. システム概要

### 目的と主要機能

Airbnbは、宿泊施設の予約を可能にするマーケットプレイスプラットフォームです。

**主要機能**:
- 宿泊施設の検索とフィルタリング
- 予約システム
- 決済処理
- レビューと評価
- メッセージング

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.5億人
- **日間アクティブユーザー（DAU）**: 約5,000万人
- **1日の予約数**: 約200万件
- **宿泊施設数**: 約700万件

## 2. 機能要件

### コア機能

1. **検索とフィルタリング**
   - 場所、日付、価格での検索
   - 複数のフィルター条件

2. **予約システム**
   - リアルタイム在庫管理
   - 予約の競合制御

3. **決済処理**
   - 安全な決済トランザクション
   - ホストへの支払い

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
Search Service → Elasticsearch → Cache
Booking Service → Database → Message Queue
Payment Service → Payment Gateway
```

## 4. データモデル設計

### Listings テーブル

```sql
CREATE TABLE listings (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location_latitude DECIMAL(10, 8),
    location_longitude DECIMAL(11, 8),
    price_per_night DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(user_id),
    SPATIAL INDEX idx_location (location_latitude, location_longitude),
    INDEX idx_price (price_per_night)
) ENGINE=InnoDB;
```

### Bookings テーブル

```sql
CREATE TABLE bookings (
    booking_id BIGINT PRIMARY KEY,
    listing_id BIGINT NOT NULL,
    guest_id BIGINT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES listings(listing_id),
    FOREIGN KEY (guest_id) REFERENCES users(user_id),
    INDEX idx_listing_id (listing_id),
    INDEX idx_guest_id (guest_id),
    INDEX idx_dates (check_in_date, check_out_date)
) ENGINE=InnoDB;
```

## 5. API設計

### 宿泊施設検索

```
GET /api/v1/listings/search?location=San+Francisco&check_in=2024-01-20&check_out=2024-01-25&guests=2
Authorization: Bearer <token>

Response (200 OK):
{
  "listings": [
    {
      "listing_id": 1234567890,
      "title": "Cozy Apartment",
      "price_per_night": 150.00,
      "rating": 4.8
    }
  ],
  "total_results": 1000
}
```

### 予約作成

```
POST /api/v1/bookings
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "listing_id": 1234567890,
  "check_in_date": "2024-01-20",
  "check_out_date": "2024-01-25",
  "guests": 2
}

Response (201 Created):
{
  "booking_id": 9876543210,
  "status": "confirmed",
  "total_amount": 750.00
}
```

## 6. スケーラビリティ設計

### 検索のスケーリング

- **Elasticsearch**: 全文検索と地理空間検索
- **キャッシング**: 人気検索クエリをキャッシュ

### 在庫管理の競合制御

- **分散ロック**: Redisで分散ロック
- **楽観的ロック**: バージョン番号を使用

## 7. レイテンシ最適化

### 検索の最適化

- **Elasticsearch**: 高速な全文検索
- **キャッシング**: 検索結果をキャッシュ

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$500,000/月**
- **データベース**: 約 **$200,000/月**
- **Elasticsearch**: 約 **$100,000/月**
- **合計**: 約 **$800,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチAZ**: 複数のアベイラビリティゾーンにデプロイ
- **データベースレプリケーション**: 読み取りレプリカを配置

## 10. セキュリティ

### セキュリティ対策

- **認証**: OAuth 2.0 / JWT
- **決済セキュリティ**: PCI DSS準拠

## 11. UX最適化

### パフォーマンス指標

- **検索**: < 500ms
- **予約作成**: < 2秒

## 12. 実装例

### 予約サービス（疑似コード）

```python
class BookingService:
    def __init__(self, db, redis_lock, payment_service):
        self.db = db
        self.redis_lock = redis_lock
        self.payment_service = payment_service
    
    async def create_booking(self, listing_id: int, guest_id: int, check_in: date, check_out: date):
        # 分散ロックを取得
        lock_key = f"booking_lock:{listing_id}:{check_in}:{check_out}"
        async with self.redis_lock.acquire(lock_key, timeout=5):
            # 在庫を確認
            if not await self.is_available(listing_id, check_in, check_out):
                raise ValueError("Listing not available")
            
            # 予約を作成
            booking_id = await self.db.create_booking(
                listing_id=listing_id,
                guest_id=guest_id,
                check_in_date=check_in,
                check_out_date=check_out
            )
            
            # 決済処理
            await self.payment_service.process_payment(booking_id)
            
            return {"booking_id": booking_id, "status": "confirmed"}
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の検索リクエスト**: 約5,000万回
- **1日の予約数**: 200万件
- **1秒あたりの検索**: 約579回/秒（平均）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **在庫管理**: 分散ロックで競合制御
2. **検索**: Elasticsearchで高速検索
3. **決済**: 安全な決済処理

## 15. 関連システム

### 類似システムへのリンク

- [Booking.com](booking_design.md) - ホテル予約プラットフォーム
- [Expedia](expedia_design.md) - 旅行予約プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Dropbox](dropbox_design.md)でファイルストレージの設計を学ぶ

