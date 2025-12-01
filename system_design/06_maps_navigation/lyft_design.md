# Lyft システム設計

## 1. システム概要

### 目的と主要機能

Lyftは、ドライバーとライダーをマッチングするライドシェアリングプラットフォームです。Uberと同様の機能を提供しますが、よりコミュニティ重視のアプローチを取っています。

**主要機能**:
- ライダーの位置情報追跡
- ドライバーの位置情報追跡
- リアルタイムマッチング
- ルート計算とナビゲーション
- 決済処理
- レーティングとレビュー
- 共有ライド（Lyft Line）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約2,000万人
- **日間アクティブユーザー（DAU）**: 約800万人
- **1日のライド数**: 約300万回
- **1秒あたりの位置更新**: 約20,000回/秒（ピーク時）
- **1秒あたりのマッチングリクエスト**: 約2,000回/秒（ピーク時）

### 主要なユースケース

1. **ライドリクエスト**: ライダーがライドをリクエスト
2. **ドライバーマッチング**: 最適なドライバーをマッチング
3. **リアルタイム追跡**: ライダーとドライバーの位置をリアルタイム追跡
4. **ルート計算**: 最適なルートを計算
5. **共有ライド**: 複数のライダーを同じライドにマッチング

## 2. 機能要件

### コア機能

1. **位置情報追跡**
   - GPS位置情報のリアルタイム更新
   - 位置情報の履歴保存

2. **マッチング**
   - ライダーとドライバーのマッチング
   - ETA（到着予定時間）の計算
   - 共有ライドのマッチング

3. **ルート計算**
   - 最短ルートの計算
   - リアルタイム交通情報の考慮

4. **決済**
   - ライド後の自動決済
   - レシートの生成

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ライド情報は強い一貫性が必要
- **パフォーマンス**:
  - 位置更新: < 5秒の遅延
  - マッチング: < 10秒
  - ルート計算: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **リアルタイム性**: 位置情報のリアルタイム更新

### 優先順位付け

1. **P0（必須）**: 位置追跡、マッチング、ルート計算
2. **P1（重要）**: 決済、レーティング、共有ライド
3. **P2（望ましい）**: 予約、高度なマッチング

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps)
└──────┬──────┘
       │ HTTPS / WebSocket
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
│  │ Location │  │ Matching │  │ Routing │        │
│  │ Service  │  │ Service  │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Trip Service                    │         │
│  │      Shared Ride Service             │         │
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
│         Geospatial Database (PostGIS)             │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Location Service**: 位置情報の追跡
   - **Matching Service**: ライダーとドライバーのマッチング
   - **Routing Service**: ルート計算
   - **Trip Service**: ライドの管理
   - **Shared Ride Service**: 共有ライドの管理
4. **Database**: ライド、ユーザー、位置情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（位置更新、マッチングなど）
7. **Geospatial Database**: 位置情報の空間クエリ
8. **CDN**: 静的コンテンツの配信

### データフロー

#### ライドリクエストのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Trip Service
3. Trip Service:
   a. ライドリクエストを作成
   b. Matching Serviceにマッチングリクエストを送信
4. Matching Service:
   a. 近くのドライバーを検索（Geospatial Database）
   b. ETAを計算
   c. 最適なドライバーを選択
   d. ドライバーに通知
```

## 4. データモデル設計

### 主要なエンティティ

#### Rides テーブル

```sql
CREATE TABLE rides (
    ride_id BIGINT PRIMARY KEY,
    rider_id BIGINT NOT NULL,
    driver_id BIGINT,
    pickup_lat DECIMAL(10, 8) NOT NULL,
    pickup_lng DECIMAL(11, 8) NOT NULL,
    dropoff_lat DECIMAL(10, 8) NOT NULL,
    dropoff_lng DECIMAL(11, 8) NOT NULL,
    status ENUM('requested', 'matched', 'in_progress', 'completed', 'cancelled') DEFAULT 'requested',
    fare DECIMAL(10, 2),
    distance DECIMAL(10, 2),
    duration INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rider_id) REFERENCES users(user_id),
    FOREIGN KEY (driver_id) REFERENCES users(user_id),
    INDEX idx_rider_id (rider_id),
    INDEX idx_driver_id (driver_id),
    INDEX idx_status (status),
    SPATIAL INDEX idx_pickup_location (pickup_lat, pickup_lng)
) ENGINE=InnoDB;
```

#### Driver_Locations テーブル

```sql
CREATE TABLE driver_locations (
    driver_id BIGINT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    status ENUM('available', 'busy', 'offline') DEFAULT 'available',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (driver_id),
    FOREIGN KEY (driver_id) REFERENCES users(user_id),
    SPATIAL INDEX idx_location (latitude, longitude)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL with PostGIS）**: 
  - 理由: 空間クエリが必要、ACID特性が必要、複雑なクエリ（JOIN、集計）
  - 用途: ライド、ユーザー、位置情報の永続化
- **Redis**:
  - 理由: リアルタイム位置情報のキャッシング
  - 用途: 位置情報のキャッシング

### スキーマ設計の考慮事項

1. **パーティショニング**: `rides`テーブルは地理的領域でシャーディング
2. **空間インデックス**: 緯度・経度に空間インデックス
3. **時系列データ**: 位置情報は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ライドリクエスト

```
POST /api/v1/rides/request
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "pickup_lat": 37.7749,
  "pickup_lng": -122.4194,
  "dropoff_lat": 37.7849,
  "dropoff_lng": -122.4094,
  "ride_type": "standard"
}

Response (200 OK):
{
  "ride_id": 1234567890,
  "status": "matched",
  "driver": {
    "driver_id": 987654321,
    "name": "John Doe",
    "eta": 5
  }
}
```

#### 位置更新

```
POST /api/v1/location/update
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "latitude": 37.7749,
  "longitude": -122.4194
}

Response (200 OK):
{
  "status": "updated"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のライドのみアクセス可能
- **レート制限**: 
  - 位置更新: 10回/秒
  - ライドリクエスト: 5回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: 地理的領域ベースのシャーディング

```
Shard 1: latitude < 37.5 (San Francisco South)
Shard 2: latitude >= 37.5 (San Francisco North)
Shard 3: longitude < -122.4 (East Bay)
Shard 4: longitude >= -122.4 (Peninsula)
```

**シャーディングキー**: `pickup_lat`, `pickup_lng`
- ライドは地理的領域でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 静的コンテンツをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 位置情報、ドライバー情報
   - TTL: 30秒-2分

3. **L3 Cache（CDN）**:
   - 用途: 静的コンテンツ
   - TTL: 1時間-1日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **位置情報更新**: リアルタイム更新の処理
2. **マッチング**: 空間クエリの最適化
3. **ルート計算**: 複雑なルートアルゴリズム

### CDNの活用

- **静的コンテンツ**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### マッチング最適化

1. **空間インデックス**: PostGISで空間クエリを最適化
2. **キャッシング**: ドライバー位置情報をキャッシュ
3. **並列検索**: 複数のドライバー候補を並列で検索

### 非同期処理

#### メッセージキュー（Kafka）

1. **位置更新**:
   ```
   Topic: location-updates
   Partition Key: user_id
   ```

2. **マッチング**:
   ```
   Topic: matching-requests
   Partition Key: ride_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 2,000万人
- **日間アクティブユーザー**: 800万人
- **1日のライド数**: 300万回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 200台（リージョン間で分散）
- コスト: $0.192/時間 × 200台 × 730時間 = **$28,032/月**

**データベース**:
- RDS PostgreSQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台（マスター + レプリカ）
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 30台
- コスト: $0.175/時間 × 30台 × 730時間 = **$3,832.50/月**

**ストレージ**:
- EBS: 50 TB
- コスト: $0.10/GB/月 × 50,000 GB = **$5,000/月**

**ネットワーク**:
- データ転送: 500 TB/月
- コスト: $0.09/GB × 500,000 GB = **$45,000/月**

**合計**: 約 **$92,960.50/月**（約1,115,526ドル/年）

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
   - ユーザーは自分のライドのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - 位置情報: 暗号化して保存

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
- **位置更新**: < 5秒の遅延
- **マッチング**: < 10秒

### プログレッシブローディング

1. **地図の遅延読み込み**:
   - ビューポート内の地図を優先的に読み込み
   - 周辺の地図は遅延読み込み

2. **オフライン対応**:
   - オフライン時の基本機能の提供

## 12. 実装例

### マッチングサービス（疑似コード）

```python
class MatchingService:
    def __init__(self, db, cache, geospatial_db):
        self.db = db
        self.cache = cache
        self.geospatial_db = geospatial_db
    
    async def find_driver(self, ride_id: int, pickup_lat: float, pickup_lng: float):
        # 近くの利用可能なドライバーを検索
        nearby_drivers = await self.geospatial_db.find_nearby_drivers(
            latitude=pickup_lat,
            longitude=pickup_lng,
            radius_km=5,
            status='available'
        )
        
        # ETAを計算
        drivers_with_eta = []
        for driver in nearby_drivers:
            eta = await self.calculate_eta(
                driver_location=(driver['latitude'], driver['longitude']),
                pickup_location=(pickup_lat, pickup_lng)
            )
            drivers_with_eta.append({
                **driver,
                'eta': eta
            })
        
        # 最適なドライバーを選択（ETAが最短）
        best_driver = min(drivers_with_eta, key=lambda d: d['eta'])
        
        # ライドをマッチング
        await self.db.update_ride(
            ride_id=ride_id,
            driver_id=best_driver['driver_id'],
            status='matched'
        )
        
        return best_driver
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の位置情報取得**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の位置更新**: 10億更新
- **1時間あたり**: 10億 / 24 = 約4,167万更新
- **1秒あたり**: 4,167万 / 3600 = 約11,575更新/秒
- **ピーク時（3倍）**: 約34,725更新/秒

### ストレージ見積もり

#### 位置情報ストレージ

- **1位置情報あたりのサイズ**: 約100バイト
- **1日の位置更新**: 10億更新
- **1日のストレージ**: 10億 × 100バイト = 100 GB
- **1年のストレージ**: 100 GB × 365 = 約36.5 TB
- **5年のストレージ**: 約182.5 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **空間データベース**: PostGISで空間クエリを最適化
4. **リアルタイム更新**: WebSocketでリアルタイム位置更新
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **位置情報更新のスケーラビリティ**:
   - 問題: 大量の位置更新でデータベースがボトルネック
   - 解決策: キャッシングと非同期処理

2. **マッチングのレイテンシ**:
   - 問題: 空間クエリが遅い
   - 解決策: 空間インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Uber](uber_design.md) - ライドシェアリングプラットフォーム
- [Grab](grab_design.md) - ライドシェアリングプラットフォーム
- [Google Maps](google_maps_design.md) - 地図・ナビゲーション

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Grab](grab_design.md)でアジア地域のライドシェアリングプラットフォームの設計を学ぶ

