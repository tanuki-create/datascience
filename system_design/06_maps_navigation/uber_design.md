# Uber システム設計

## 1. システム概要

### 目的と主要機能

Uberは、ドライバーとライダーをマッチングするライドシェアリングプラットフォームです。

**主要機能**:
- ライダーの位置情報追跡
- ドライバーの位置情報追跡
- リアルタイムマッチング
- ルート計算とナビゲーション
- 決済処理
- レーティングとレビュー

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.3億人
- **日間アクティブユーザー（DAU）**: 約5,000万人
- **1日のライド数**: 約2,000万回
- **1秒あたりの位置更新**: 約100,000回/秒（ピーク時）
- **1秒あたりのマッチングリクエスト**: 約10,000回/秒（ピーク時）

### 主要なユースケース

1. **ライドリクエスト**: ライダーがライドをリクエスト
2. **ドライバーマッチング**: 最適なドライバーをマッチング
3. **リアルタイム追跡**: ライダーとドライバーの位置をリアルタイム追跡
4. **ルート計算**: 最適なルートを計算

## 2. 機能要件

### コア機能

1. **位置情報追跡**
   - GPS位置情報のリアルタイム更新
   - 位置情報の履歴保存

2. **マッチング**
   - ライダーとドライバーのマッチング
   - ETA（到着予定時間）の計算

3. **ルート計算**
   - 最短ルートの計算
   - リアルタイム交通情報の考慮

4. **決済**
   - ライド後の自動決済
   - レシートの生成

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 位置更新: < 5秒の遅延
  - マッチング: < 10秒
  - ルート計算: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **リアルタイム性**: 位置情報のリアルタイム更新

### 優先順位付け

1. **P0（必須）**: 位置追跡、マッチング、ルート計算
2. **P1（重要）**: 決済、レーティング
3. **P2（望ましい）**: 予約、共有ライド

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps)
└──────┬──────┘
       │ HTTPS / WebSocket
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                       │
└──────┬──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
│  API Gateway│   │  API Gateway│   │  API Gateway│
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       ├─────────────────┴──────────────────┤
       │                                     │
┌──────▼─────────────────────────────────────▼──────┐
│              Application Servers                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Location │  │ Matching │  │ Routing │        │
│  │ Service  │  │ Service  │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Trip Service                    │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┬──────────┐
        │                 │                  │          │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐  │
│   Database   │  │   Cache       │  │  Message     │  │
│   (Sharded)  │  │   (Redis)     │  │  Queue       │  │
└──────────────┘  └───────────────┘  └──────────────┘  │
                                                     │
┌─────────────────────────────────────────────────────▼──┐
│              Location Tracking Service                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ WebSocket│  │ Geospatial│ │ Location │            │
│  │ Server   │  │ Index     │ │ History  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼──────────────┼──────────────┼──────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼──────┐
│         Geospatial Database                │
│         (Redis Geo / PostGIS)             │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Location Service**: 位置情報の管理
   - **Matching Service**: ライダーとドライバーのマッチング
   - **Routing Service**: ルート計算
   - **Trip Service**: ライドの管理
4. **Location Tracking Service**:
   - **WebSocket Server**: リアルタイム位置更新
   - **Geospatial Index**: 地理空間インデックス
   - **Location History**: 位置履歴の保存
5. **Geospatial Database**: 地理空間データの管理

### データフロー

#### ライドリクエストのフロー

```
1. Client → Load Balancer → API Gateway → Trip Service
2. Trip Service:
   a. ライダーの位置情報を取得
   b. Matching Serviceにマッチングリクエストを送信
3. Matching Service:
   a. 近くのドライバーを検索（Geospatial Index）
   b. ETAを計算
   c. 最適なドライバーを選択
   d. ドライバーに通知
4. ドライバーが承認:
   a. Trip Serviceがライドを開始
   b. リアルタイム位置追跡を開始
```

#### 位置更新のフロー

```
1. Client → WebSocket Server → Location Service
2. Location Service:
   a. 位置情報をGeospatial Databaseに更新
   b. アクティブなライドがある場合、相手に位置情報を送信
   c. Location Historyに保存
```

## 4. データモデル設計

### 主要なエンティティ

#### Users テーブル

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    user_type ENUM('rider', 'driver') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone_number (phone_number)
) ENGINE=InnoDB;
```

#### Drivers テーブル

```sql
CREATE TABLE drivers (
    driver_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    vehicle_id BIGINT NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('offline', 'available', 'on_trip') NOT NULL,
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_status (status),
    SPATIAL INDEX idx_location (current_latitude, current_longitude)
) ENGINE=InnoDB;
```

#### Trips テーブル

```sql
CREATE TABLE trips (
    trip_id BIGINT PRIMARY KEY,
    rider_id BIGINT NOT NULL,
    driver_id BIGINT NOT NULL,
    pickup_latitude DECIMAL(10, 8) NOT NULL,
    pickup_longitude DECIMAL(11, 8) NOT NULL,
    dropoff_latitude DECIMAL(10, 8),
    dropoff_longitude DECIMAL(11, 8),
    status ENUM('requested', 'matched', 'driver_arrived', 'in_progress', 'completed', 'cancelled') NOT NULL,
    fare_amount DECIMAL(10, 2),
    distance_km DECIMAL(10, 2),
    duration_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id) REFERENCES users(user_id),
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
    INDEX idx_rider_id (rider_id),
    INDEX idx_driver_id (driver_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Trip_Locations テーブル

```sql
CREATE TABLE trip_locations (
    location_id BIGINT PRIMARY KEY,
    trip_id BIGINT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id),
    INDEX idx_trip_id_timestamp (trip_id, timestamp)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL with PostGIS）**: 
  - 理由: 地理空間データの管理、複雑なクエリ、トランザクション処理
  - 用途: ユーザー、ドライバー、ライド情報
- **NoSQL（Redis Geo）**:
  - 理由: リアルタイム位置検索、低レイテンシ
  - 用途: アクティブなドライバーの位置情報
- **Time Series DB（InfluxDB）**:
  - 理由: 位置履歴の時系列データ
  - 用途: 位置履歴の保存

## 5. API設計

### 主要なAPIエンドポイント

#### ライドリクエスト

```
POST /api/v1/trips/request
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "pickup_latitude": 37.7749,
  "pickup_longitude": -122.4194,
  "dropoff_latitude": 37.7849,
  "dropoff_longitude": -122.4294
}

Response (201 Created):
{
  "trip_id": 1234567890,
  "status": "requested",
  "estimated_wait_time": 5, -- minutes
  "estimated_fare": 25.50
}
```

#### 位置更新

```
WebSocket: ws://api.uber.com/v1/location
Message:
{
  "latitude": 37.7749,
  "longitude": -122.4194,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### アクティブなライドの位置取得

```
GET /api/v1/trips/{trip_id}/location
Authorization: Bearer <token>

Response (200 OK):
{
  "trip_id": 1234567890,
  "driver_location": {
    "latitude": 37.7750,
    "longitude": -122.4195,
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "rider_location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "eta_minutes": 3
}
```

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **WebSocket接続**: 接続を複数のサーバーに分散（Sticky Session）

#### 地理空間データの分散

- **地理的シャーディング**: 地域ごとにデータを分散
- **Redis Geo**: アクティブなドライバーの位置情報を管理

### マッチングアルゴリズム

1. **近くのドライバー検索**:
   - Redis GeoのGEORADIUSで近くのドライバーを検索
   - 半径5km以内のドライバーを取得

2. **ETA計算**:
   - ルーティングサービスでETAを計算
   - 交通情報を考慮

3. **最適なドライバー選択**:
   - ETAが最短のドライバーを選択
   - ドライバーの評価も考慮

### キャッシング戦略

#### キャッシュレイヤー

1. **Redis Geo**: 
   - 用途: アクティブなドライバーの位置情報
   - TTL: リアルタイム更新

2. **Redis Cache**:
   - 用途: ライド情報、ユーザー情報
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **地理空間検索**: 近くのドライバー検索が遅い
2. **ルート計算**: リアルタイム交通情報の取得
3. **WebSocket接続**: 大量の同時接続

### 地理空間検索の最適化

1. **Redis Geo**: 
   - GEORADIUSで高速な近傍検索
   - O(log N + M)の時間計算量（Nはドライバー数、Mは結果数）

2. **事前計算**:
   - 人気エリアのドライバーリストを事前計算
   - キャッシュに保存

### ルート計算の最適化

1. **キャッシング**: 
   - よく使われるルートをキャッシュ
   - 交通情報は5分ごとに更新

2. **並列計算**:
   - 複数のドライバーへのETAを並列計算

### WebSocket接続の最適化

1. **接続プール**: 
   - WebSocket接続をプール管理
   - 接続の再利用

2. **メッセージバッチング**:
   - 複数の位置更新をバッチで送信
   - 1秒ごとにバッチ送信

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1.3億人
- **1日のライド数**: 2,000万回
- **1秒あたりの位置更新**: 100,000回/秒（ピーク時）

#### サーバーコスト

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**WebSocketサーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 500台
- コスト: $0.34/時間 × 500台 × 730時間 = **$124,100/月**

**データベース**:
- RDS PostgreSQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache Redis）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**合計**: 約 **$304,775/月**

### コスト削減戦略

1. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
2. **リザーブドインスタンス**: 1年契約で最大72%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - WebSocket接続の冗長化

2. **フォールバック**:
   - マッチング失敗時のリトライ
   - ルート計算失敗時の簡易ルート

### モニタリング・アラート

- **位置更新の遅延**: 5秒を超えた場合
- **マッチング成功率**: 95%を下回った場合
- **WebSocket接続数**: 80%を超えた場合

## 10. セキュリティ

### 認証・認可

1. **認証**: OAuth 2.0 / JWT
2. **位置情報のプライバシー**: 
   - ライド中のみ位置情報を共有
   - ライド終了後は位置情報を削除

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: データベースの暗号化

## 11. UX最適化

### パフォーマンス指標

- **マッチング時間**: < 10秒
- **位置更新の遅延**: < 5秒
- **ルート計算**: < 2秒

### リアルタイム更新

1. **WebSocket**: リアルタイム位置更新
2. **プッシュ通知**: マッチング成功時の通知

## 12. 実装例

### マッチングサービス（疑似コード）

```python
class MatchingService:
    def __init__(self, redis_geo, routing_service):
        self.redis_geo = redis_geo
        self.routing_service = routing_service
    
    async def find_nearby_drivers(self, latitude: float, longitude: float, radius_km: float = 5):
        # Redis Geoで近くのドライバーを検索
        drivers = await self.redis_geo.georadius(
            "drivers:available",
            longitude,
            latitude,
            radius_km,
            unit="km",
            withdist=True,
            count=10
        )
        
        return drivers
    
    async def match_driver(self, trip_id: int, pickup_lat: float, pickup_lon: float):
        # 近くのドライバーを検索
        nearby_drivers = await self.find_nearby_drivers(pickup_lat, pickup_lon)
        
        if not nearby_drivers:
            return None
        
        # 各ドライバーへのETAを計算
        driver_etas = []
        for driver_id, distance in nearby_drivers:
            driver_location = await self.redis_geo.geopos("drivers:available", driver_id)
            eta = await self.routing_service.calculate_eta(
                driver_location[0],
                driver_location[1],
                pickup_lat,
                pickup_lon
            )
            driver_etas.append((driver_id, eta, distance))
        
        # ETAが最短のドライバーを選択
        best_driver = min(driver_etas, key=lambda x: x[1])
        
        return {
            "driver_id": best_driver[0],
            "eta_minutes": best_driver[1],
            "distance_km": best_driver[2]
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 位置更新

- **1秒あたりの位置更新**: 100,000回/秒（ピーク時）
- **1日の位置更新**: 100,000 × 86400 = 8.64億回
- **1位置更新あたりのサイズ**: 約100バイト
- **1日のデータ転送**: 8.64億 × 100バイト = 86.4 GB

#### マッチングリクエスト

- **1日のライド数**: 2,000万回
- **1秒あたりのマッチングリクエスト**: 約231回/秒（平均）
- **ピーク時（5倍）**: 約1,155回/秒

### ストレージ見積もり

#### 位置履歴

- **1ライドあたりの位置記録**: 平均60回（5分間、5秒ごと）
- **1日の位置記録**: 2,000万 × 60 = 12億回
- **1位置記録あたりのサイズ**: 約50バイト
- **1日のストレージ**: 12億 × 50バイト = 60 GB
- **1年のストレージ**: 60 GB × 365 = 約21.9 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **リアルタイム処理**: WebSocketでリアルタイム更新
2. **地理空間インデックス**: Redis Geoで高速検索
3. **非同期処理**: マッチングとルート計算を非同期で処理

### よくある落とし穴

1. **位置更新の頻度**:
   - 問題: 更新頻度が高すぎるとコストが高い
   - 解決策: 5秒ごとに更新、移動中のみ更新

2. **マッチングの複雑さ**:
   - 問題: マッチングアルゴリズムが複雑
   - 解決策: シンプルなアルゴリズムから始める

## 15. 関連システム

### 類似システムへのリンク

- [Google Maps](google_maps_design.md) - 地図・ナビゲーションサービス
- [Lyft](lyft_design.md) - ライドシェアリングサービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Netflix](netflix_design.md)でオンデマンドストリーミングの設計を学ぶ

