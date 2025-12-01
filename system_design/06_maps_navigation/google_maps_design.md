# Google Maps システム設計

## 1. システム概要

### 目的と主要機能

Google Mapsは、地図表示、ルート検索、リアルタイム交通情報、ストリートビューなどの機能を提供する地図・ナビゲーションサービスです。

**主要機能**:
- 地図表示
- ルート検索（車、徒歩、自転車、公共交通機関）
- リアルタイム交通情報
- ストリートビュー
- 場所検索
- レビュー・評価
- オフラインマップ

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約10億人
- **日間アクティブユーザー（DAU）**: 約5億人
- **1日の検索クエリ数**: 約10億クエリ
- **1秒あたりのリクエスト数**: 約20,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **地図表示**: ユーザーが地図を表示
2. **ルート検索**: 出発地から目的地までのルートを検索
3. **場所検索**: キーワードで場所を検索
4. **リアルタイム交通情報**: 交通渋滞情報の表示
5. **ナビゲーション**: リアルタイムナビゲーション

## 2. 機能要件

### コア機能

1. **地図表示**
   - タイルベースの地図表示
   - ズーム・パン機能
   - マーカー表示

2. **ルート検索**
   - 複数のルートオプション
   - リアルタイム交通情報を考慮
   - 複数の交通手段のサポート

3. **場所検索**
   - キーワード検索
   - カテゴリ検索
   - 近くの場所検索

4. **リアルタイム情報**
   - 交通渋滞情報
   - 事故情報
   - 工事情報

5. **ストリートビュー**
   - 360度の街並み表示
   - パノラマ画像

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 地図データは最終的に一貫性を保つ
- **パフォーマンス**:
  - 地図表示: < 1秒
  - ルート検索: < 2秒
  - 場所検索: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 地図データは永続的に保存

### 優先順位付け

1. **P0（必須）**: 地図表示、ルート検索、場所検索
2. **P1（重要）**: リアルタイム交通情報、ストリートビュー
3. **P2（望ましい）**: オフラインマップ、高度な検索機能

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
│  │ Map      │  │  Route   │  │  Place   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Traffic Service                │         │
│  │      Street View Service             │         │
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
│         Tile Server (Map Tiles)                   │
│         Search Index (Elasticsearch)              │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Map Service**: 地図タイルの配信
   - **Route Service**: ルート検索の処理
   - **Place Service**: 場所検索の処理
   - **Traffic Service**: リアルタイム交通情報の処理
   - **Street View Service**: ストリートビューの処理
4. **Database**: 場所情報、レビューの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（交通情報更新など）
7. **Tile Server**: 地図タイルの配信
8. **Search Index**: 場所検索インデックス
9. **CDN**: 地図タイル、ストリートビュー画像の配信

### データフロー

#### 地図表示のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Map Service
3. Map Service:
   a. 必要なタイルを特定（ズームレベル、座標）
   b. Cacheからタイルを取得（キャッシュヒット時）
   c. キャッシュミス時: Tile Serverから取得
   d. CDN経由でタイルを配信
```

#### ルート検索のフロー

```
1. Client → API Gateway → Route Service
2. Route Service:
   a. 出発地・目的地を取得
   b. ルートアルゴリズムでルートを計算
   c. Traffic Serviceからリアルタイム交通情報を取得
   d. 交通情報を考慮してルートを最適化
   e. 複数のルートオプションを返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Places テーブル

```sql
CREATE TABLE places (
    place_id BIGINT PRIMARY KEY,
    place_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT,
    phone_number VARCHAR(20),
    rating DECIMAL(3, 2),
    review_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_location (latitude, longitude),
    FULLTEXT INDEX idx_place_name (place_name)
) ENGINE=InnoDB;
```

#### Routes テーブル

```sql
CREATE TABLE routes (
    route_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    origin_lat DECIMAL(10, 8) NOT NULL,
    origin_lng DECIMAL(11, 8) NOT NULL,
    dest_lat DECIMAL(10, 8) NOT NULL,
    dest_lng DECIMAL(11, 8) NOT NULL,
    route_data JSON NOT NULL,
    duration INT,
    distance DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_origin (origin_lat, origin_lng),
    INDEX idx_dest (dest_lat, dest_lng)
) ENGINE=InnoDB;
```

#### Traffic_Data テーブル

```sql
CREATE TABLE traffic_data (
    traffic_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    road_segment_id BIGINT NOT NULL,
    speed INT NOT NULL,
    congestion_level ENUM('free', 'moderate', 'heavy', 'severe') NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_road_segment_recorded (road_segment_id, recorded_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 場所情報、ルート、交通データの永続化
- **Elasticsearch**:
  - 理由: 全文検索、場所検索
  - 用途: 場所検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `places`テーブルは地理的領域でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **空間インデックス**: 緯度・経度に空間インデックス

## 5. API設計

### 主要なAPIエンドポイント

#### 地図タイル取得

```
GET /api/v1/maps/tiles/{z}/{x}/{y}.png

Response (200 OK):
[PNG Image Data]
```

#### ルート検索

```
GET /api/v1/routes?origin=37.7749,-122.4194&destination=37.7849,-122.4094&mode=driving
Authorization: Bearer <token>

Response (200 OK):
{
  "routes": [
    {
      "distance": 5000,
      "duration": 600,
      "polyline": "encoded_polyline_string",
      "steps": [...]
    }
  ]
}
```

#### 場所検索

```
GET /api/v1/places/search?q=restaurant&location=37.7749,-122.4194&radius=1000
Authorization: Bearer <token>

Response (200 OK):
{
  "places": [
    {
      "place_id": 1234567890,
      "name": "Restaurant Name",
      "location": {
        "lat": 37.7749,
        "lng": -122.4194
      },
      "rating": 4.5
    }
  ]
}
```

### 認証・認可

- **認証**: API Key / OAuth 2.0
- **認可**: API Keyベースのアクセス制御
- **レート制限**: 
  - 地図タイル: 10,000リクエスト/日
  - ルート検索: 2,500リクエスト/日
  - 場所検索: 5,000リクエスト/日

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報を保存しない
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: 地理的領域ベースのシャーディング

```
Shard 1: latitude < -45 (南半球)
Shard 2: -45 <= latitude < 0 (南半球-赤道)
Shard 3: 0 <= latitude < 45 (北半球-赤道)
Shard 4: latitude >= 45 (北半球)
```

**シャーディングキー**: `latitude`
- 場所は地理的領域でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 地図タイル、ストリートビュー画像をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 地図タイル、ルート、場所情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 地図タイル、ストリートビュー画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **地図タイル配信**: 大量のタイルリクエスト
2. **ルート計算**: 複雑なルートアルゴリズム
3. **リアルタイム交通情報**: 頻繁な更新

### CDNの活用

- **地図タイル**: CloudflareまたはAWS CloudFront
- **ストリートビュー**: CDN経由で配信
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ルート計算最適化

1. **事前計算**: 人気ルートを事前計算
2. **キャッシング**: ルート結果をキャッシュ
3. **並列計算**: 複数のルートオプションを並列で計算

### 非同期処理

#### メッセージキュー（Kafka）

1. **交通情報更新**:
   ```
   Topic: traffic-updates
   Partition Key: road_segment_id
   ```

2. **地図タイル生成**:
   ```
   Topic: tile-generation
   Partition Key: tile_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 10億人
- **日間アクティブユーザー**: 5億人
- **1日の検索クエリ数**: 10億クエリ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,500台（リージョン間で分散）
- コスト: $0.192/時間 × 1,500台 × 730時間 = **$210,240/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.76/時間 × 80台 × 730時間 = **$44,384/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 150台
- コスト: $0.175/時間 × 150台 × 730時間 = **$19,162.50/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**ストレージ**:
- EBS: 200 TB
- コスト: $0.10/GB/月 × 200,000 GB = **$20,000/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.09/GB × 10,000,000 GB = **$900,000/月**

**合計**: 約 **$1,210,430.50/月**（約14,525,166ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **CDN活用**: データ転送コストを削減
5. **タイルキャッシング**: 地図タイルのキャッシングでコスト削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Tile Serverのヘルスチェック

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

2. **地図データバックアップ**:
   - 地図タイルのバックアップ
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - API Key
   - OAuth 2.0（オプション）

2. **認可**:
   - API Keyベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム

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
- **地図表示**: < 1秒
- **ルート検索**: < 2秒

### プログレッシブローディング

1. **地図タイルの遅延読み込み**:
   - ビューポート内のタイルを優先的に読み込み
   - 周辺のタイルは遅延読み込み

2. **オフラインマップ**:
   - 事前にダウンロードしたマップをオフラインで使用

## 12. 実装例

### ルートサービス（疑似コード）

```python
class RouteService:
    def __init__(self, db, cache, traffic_service):
        self.db = db
        self.cache = cache
        self.traffic_service = traffic_service
    
    async def find_route(self, origin_lat: float, origin_lng: float, 
                        dest_lat: float, dest_lng: float, mode: str = 'driving'):
        # キャッシュから取得を試みる
        cache_key = f"route:{origin_lat},{origin_lng}:{dest_lat},{dest_lng}:{mode}"
        cached_route = await self.cache.get(cache_key)
        
        if cached_route:
            return cached_route
        
        # ルートアルゴリズムでルートを計算
        routes = await self.calculate_routes(
            origin=(origin_lat, origin_lng),
            destination=(dest_lat, dest_lng),
            mode=mode
        )
        
        # リアルタイム交通情報を取得
        for route in routes:
            traffic_info = await self.traffic_service.get_traffic_info(route['path'])
            route['duration'] = self.adjust_duration(route['duration'], traffic_info)
        
        # 最適なルートを選択
        best_route = min(routes, key=lambda r: r['duration'])
        
        # キャッシュに保存
        await self.cache.set(cache_key, best_route, ttl=300)
        
        return best_route
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の地図タイルリクエスト**: 100億リクエスト
- **1時間あたり**: 100億 / 24 = 約4.17億リクエスト
- **1秒あたり**: 4.17億 / 3600 = 約115,833リクエスト/秒
- **ピーク時（3倍）**: 約347,499リクエスト/秒

#### 書き込みトラフィック

- **1日の交通情報更新**: 10億更新
- **1時間あたり**: 10億 / 24 = 約4,167万更新
- **1秒あたり**: 4,167万 / 3600 = 約11,575更新/秒

### ストレージ見積もり

#### 地図タイルストレージ

- **1タイルあたりのサイズ**: 約20 KB
- **タイル総数**: 約100億タイル（全ズームレベル）
- **合計ストレージ**: 100億 × 20 KB = 20 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **タイルキャッシング**: 地図タイルを積極的にキャッシュ
4. **CDN活用**: 地図タイルをCDN経由で配信
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **地図タイル配信のコスト**:
   - 問題: 大量のタイルリクエストでコストが高い
   - 解決策: CDNとキャッシング

2. **ルート計算のレイテンシ**:
   - 問題: 複雑なルート計算が遅い
   - 解決策: 事前計算とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Uber](uber_design.md) - ライドシェアリング
- [Lyft](lyft_design.md) - ライドシェアリング
- [Grab](grab_design.md) - ライドシェアリング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Lyft](lyft_design.md)でライドシェアリングプラットフォームの設計を学ぶ

