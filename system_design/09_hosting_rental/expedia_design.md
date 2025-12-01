# Expedia システム設計

## 1. システム概要

### 目的と主要機能

Expediaは、ホテル、フライト、レンタカー、パッケージ旅行などの予約を統合した旅行予約プラットフォームです。

**主要機能**:
- ホテル検索・予約
- フライト検索・予約
- レンタカー検索・予約
- パッケージ旅行
- レビュー・評価
- 決済処理
- キャンセル管理

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約7,500万人
- **日間アクティブユーザー（DAU）**: 約2,000万人
- **1日の予約数**: 約100万件
- **1日の検索クエリ数**: 約3,000万クエリ
- **1秒あたりのリクエスト数**: 約7,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ホテル検索・予約**: ユーザーがホテルを検索・予約
2. **フライト検索・予約**: ユーザーがフライトを検索・予約
3. **パッケージ旅行**: ユーザーがパッケージ旅行を予約
4. **レビュー投稿**: ユーザーがレビューを投稿
5. **キャンセル**: ユーザーが予約をキャンセル

## 2. 機能要件

### コア機能

1. **ホテル検索・予約**
   - 場所・日付・人数での検索
   - フィルター・ソート機能
   - 予約管理

2. **フライト検索・予約**
   - 出発地・目的地・日付での検索
   - 複数の航空会社の統合
   - 予約管理

3. **レンタカー検索・予約**
   - 場所・日付での検索
   - 複数のレンタカー会社の統合
   - 予約管理

4. **パッケージ旅行**
   - ホテル・フライト・レンタカーの組み合わせ
   - 割引価格の提供

5. **決済処理**
   - クレジットカード決済
   - 複数の決済方法のサポート

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

1. **P0（必須）**: ホテル検索・予約、フライト検索・予約、在庫管理
2. **P1（重要）**: パッケージ旅行、決済処理、レビュー・評価
3. **P2（望ましい）**: レンタカー、キャンセル管理

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
│  │ Hotel    │  │  Flight  │  │  Package │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Booking Service                 │         │
│  │      Payment Service                 │         │
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
│         External APIs (Airlines, Hotels)          │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Hotel Service**: ホテル検索・予約の処理
   - **Flight Service**: フライト検索・予約の処理
   - **Package Service**: パッケージ旅行の処理
   - **Booking Service**: 予約管理の処理
   - **Payment Service**: 決済処理
4. **Database**: 予約、ユーザー情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（予約確認メール送信など）
7. **Search Index**: 検索インデックス
8. **External APIs**: 航空会社、ホテルチェーンのAPI統合
9. **CDN**: 画像の配信

### データフロー

#### パッケージ旅行予約のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Package Service
3. Package Service:
   a. Hotel Serviceでホテルを検索
   b. Flight Serviceでフライトを検索
   c. パッケージ価格を計算
   d. Booking Serviceで予約を作成
   e. Payment Serviceで決済処理
```

## 4. データモデル設計

### 主要なエンティティ

#### Hotels テーブル

```sql
CREATE TABLE hotels (
    hotel_id BIGINT PRIMARY KEY,
    hotel_name VARCHAR(500) NOT NULL,
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
    SPATIAL INDEX idx_location (latitude, longitude),
    FULLTEXT INDEX idx_hotel_name (hotel_name)
) ENGINE=InnoDB;
```

#### Flights テーブル

```sql
CREATE TABLE flights (
    flight_id BIGINT PRIMARY KEY,
    airline_code VARCHAR(10) NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    departure_airport VARCHAR(10) NOT NULL,
    arrival_airport VARCHAR(10) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available_seats INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_departure_arrival (departure_airport, arrival_airport),
    INDEX idx_departure_time (departure_time)
) ENGINE=InnoDB;
```

#### Bookings テーブル

```sql
CREATE TABLE bookings (
    booking_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    booking_type ENUM('hotel', 'flight', 'package') NOT NULL,
    hotel_id BIGINT,
    flight_id BIGINT,
    check_in_date DATE,
    check_out_date DATE,
    total_price DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 予約、ユーザー情報の永続化
- **Elasticsearch**:
  - 理由: 全文検索、検索インデックス
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `bookings`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 予約は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ホテル検索

```
GET /api/v1/hotels/search?location=Paris&check_in=2024-06-01&check_out=2024-06-05&guests=2
Authorization: Bearer <token>

Response (200 OK):
{
  "hotels": [
    {
      "hotel_id": 1234567890,
      "hotel_name": "Hotel Example",
      "price_per_night": 150.00,
      "rating": 4.5
    }
  ],
  "total_results": 1000
}
```

#### パッケージ旅行予約

```
POST /api/v1/packages/book
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "hotel_id": 1234567890,
  "flight_id": 9876543210,
  "check_in_date": "2024-06-01",
  "check_out_date": "2024-06-05",
  "number_of_guests": 2
}

Response (200 OK):
{
  "booking_id": 1112223333,
  "status": "confirmed",
  "total_price": 1200.00
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

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 4 == 0
Shard 2: user_id % 4 == 1
Shard 3: user_id % 4 == 2
Shard 4: user_id % 4 == 3
```

**シャーディングキー**: `user_id`
- 予約は`user_id`でシャーディング

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
   - 用途: ホテルメタデータ、フライト情報、人気検索結果
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **外部API呼び出し**: 航空会社・ホテルチェーンのAPI呼び出し
2. **検索**: Elasticsearchクエリの最適化
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

2. **外部API呼び出し**:
   ```
   Topic: external-api-calls
   Partition Key: provider_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 7,500万人
- **日間アクティブユーザー**: 2,000万人
- **1日の予約数**: 100万件
- **1日の検索クエリ数**: 3,000万クエリ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 400台（リージョン間で分散）
- コスト: $0.192/時間 × 400台 × 730時間 = **$56,064/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台（マスター + レプリカ）
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ**:
- EBS: 80 TB
- コスト: $0.10/GB/月 × 80,000 GB = **$8,000/月**

**ネットワーク**:
- データ転送: 800 TB/月
- コスト: $0.09/GB × 800,000 GB = **$72,000/月**

**合計**: 約 **$171,469/月**（約2,057,628ドル/年）

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
   - 外部APIのヘルスチェック

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

### パッケージサービス（疑似コード）

```python
class PackageService:
    def __init__(self, hotel_service, flight_service, booking_service, payment_service):
        self.hotel_service = hotel_service
        self.flight_service = flight_service
        self.booking_service = booking_service
        self.payment_service = payment_service
    
    async def create_package_booking(self, user_id: int, hotel_id: int, flight_id: int,
                                    check_in_date: str, check_out_date: str, 
                                    number_of_guests: int, payment_method: str):
        # ホテルとフライトの在庫を確認
        hotel_available = await self.hotel_service.check_availability(
            hotel_id=hotel_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests
        )
        
        flight_available = await self.flight_service.check_availability(
            flight_id=flight_id
        )
        
        if not hotel_available or not flight_available:
            raise AvailabilityError("Hotel or flight not available")
        
        # パッケージ価格を計算
        hotel_price = await self.hotel_service.get_price(
            hotel_id=hotel_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests
        )
        
        flight_price = await self.flight_service.get_price(flight_id=flight_id)
        
        # パッケージ割引を適用
        total_price = (hotel_price + flight_price) * 0.9  # 10%割引
        
        # 予約を作成
        booking_id = await self.booking_service.create_booking(
            user_id=user_id,
            booking_type='package',
            hotel_id=hotel_id,
            flight_id=flight_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )
        
        # 決済処理
        payment_result = await self.payment_service.process_payment(
            booking_id=booking_id,
            amount=total_price,
            payment_method=payment_method
        )
        
        if payment_result['status'] == 'success':
            await self.booking_service.confirm_booking(booking_id=booking_id)
        
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "total_price": total_price
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の検索クエリ数**: 3,000万クエリ
- **1時間あたり**: 3,000万 / 24 = 約125万クエリ
- **1秒あたり**: 125万 / 3600 = 約347クエリ/秒
- **ピーク時（3倍）**: 約1,041クエリ/秒

#### 書き込みトラフィック

- **1日の予約数**: 100万件
- **1時間あたり**: 100万 / 24 = 約4.17万件
- **1秒あたり**: 4.17万 / 3600 = 約11.58件/秒
- **ピーク時（3倍）**: 約34.74件/秒

### ストレージ見積もり

#### 予約ストレージ

- **1予約あたりのサイズ**: 約1 KB
- **1日の予約数**: 100万件
- **1日のストレージ**: 100万 × 1 KB = 1 GB
- **1年のストレージ**: 1 GB × 365 = 約365 GB
- **5年のストレージ**: 約1.825 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **外部API統合**: 航空会社・ホテルチェーンのAPI統合
4. **トランザクション**: 予約作成時のトランザクション処理
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **外部APIのレイテンシ**:
   - 問題: 外部API呼び出しが遅い
   - 解決策: キャッシングとタイムアウト設定

2. **在庫の競合**:
   - 問題: 同時予約で在庫の競合が発生
   - 解決策: 楽観的ロックとトランザクション

## 15. 関連システム

### 類似システムへのリンク

- [Airbnb](airbnb_design.md) - 宿泊施設予約プラットフォーム
- [Booking.com](booking_design.md) - 宿泊施設予約プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Medium](../10_news_media/medium_design.md)でニュース・メディアプラットフォームの設計を学ぶ

