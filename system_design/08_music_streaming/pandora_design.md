# Pandora システム設計

## 1. システム概要

### 目的と主要機能

Pandoraは、音楽ゲノムプロジェクトに基づくパーソナライズされたラジオサービスです。ユーザーの好みに基づいて楽曲を自動的に選択・再生します。

**主要機能**:
- パーソナライズされたラジオステーション
- 音楽ゲノムプロジェクト（楽曲の特徴分析）
- スキップ機能
- いいね・よくない機能
- プレイリスト作成
- オフライン再生

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5,500万人
- **日間アクティブユーザー（DAU）**: 約2,000万人
- **1日のストリーミング数**: 約5億回
- **1秒あたりのストリーミング数**: 約6,000回/秒（ピーク時）
- **楽曲ライブラリ**: 約3,000万曲

### 主要なユースケース

1. **ラジオステーション再生**: ユーザーがラジオステーションを再生
2. **楽曲スキップ**: ユーザーが楽曲をスキップ
3. **いいね・よくない**: ユーザーが楽曲を評価
4. **プレイリスト作成**: ユーザーがプレイリストを作成
5. **レコメンデーション**: ユーザーの好みに基づいた楽曲推薦

## 2. 機能要件

### コア機能

1. **パーソナライズされたラジオ**
   - 音楽ゲノムプロジェクトに基づく楽曲選択
   - ユーザーの好みに基づいた自動再生

2. **音楽ゲノムプロジェクト**
   - 楽曲の特徴分析（450以上の属性）
   - 楽曲の類似性計算

3. **ユーザー評価**
   - いいね・よくない機能
   - スキップ履歴の記録

4. **プレイリスト管理**
   - プレイリストの作成・編集
   - カスタムラジオステーション

5. **レコメンデーション**
   - ユーザーの好みに基づいた楽曲推薦
   - 新しいアーティストの発見

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: プレイリストは強い一貫性、ストリーミングは最終的に一貫性を保つ
- **パフォーマンス**:
  - ストリーミング開始: < 2秒
  - 楽曲推薦: < 1秒
  - スキップ処理: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 楽曲は永続的に保存

### 優先順位付け

1. **P0（必須）**: パーソナライズされたラジオ、音楽ゲノムプロジェクト、ユーザー評価
2. **P1（重要）**: プレイリスト管理、レコメンデーション
3. **P2（望ましい）**: オフライン再生、高度なレコメンデーション

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
│  │ Radio    │  │  Genome  │  │  Rating │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Recommendation Service          │         │
│  │      Playlist Service                │         │
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
│         Object Storage (S3)                       │
│         Music Genome Database                     │
│         CDN (CloudFront/Cloudflare)               │
│         Media Server (HLS/DASH)                   │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Radio Service**: ラジオステーションの処理
   - **Genome Service**: 音楽ゲノムプロジェクトの処理
   - **Rating Service**: ユーザー評価の処理
   - **Recommendation Service**: レコメンデーションの処理
   - **Playlist Service**: プレイリスト管理の処理
4. **Database**: 楽曲メタデータ、プレイリスト、ユーザー評価の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（レコメンデーション生成など）
7. **Object Storage**: 楽曲ファイルの保存
8. **Music Genome Database**: 音楽ゲノムプロジェクトのデータベース
9. **CDN**: 楽曲の配信
10. **Media Server**: HLS/DASHストリーミングサーバー

### データフロー

#### ラジオステーション再生のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Radio Service
3. Radio Service:
   a. ユーザーの好みを取得
   b. Genome Serviceから類似楽曲を取得
   c. Recommendation Serviceで楽曲を選択
   d. CDNから楽曲をストリーミング
```

## 4. データモデル設計

### 主要なエンティティ

#### Songs テーブル

```sql
CREATE TABLE songs (
    song_id BIGINT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    artist_id BIGINT NOT NULL,
    album_id BIGINT,
    duration INT NOT NULL,
    genre VARCHAR(100),
    release_date DATE,
    storage_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    INDEX idx_artist_id (artist_id),
    INDEX idx_album_id (album_id),
    FULLTEXT INDEX idx_title (title)
) ENGINE=InnoDB;
```

#### Music_Genome テーブル

```sql
CREATE TABLE music_genome (
    song_id BIGINT NOT NULL,
    attribute_id INT NOT NULL,
    value DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY (song_id, attribute_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    INDEX idx_attribute_value (attribute_id, value)
) ENGINE=InnoDB;
```

#### User_Ratings テーブル

```sql
CREATE TABLE user_ratings (
    user_id BIGINT NOT NULL,
    song_id BIGINT NOT NULL,
    rating ENUM('like', 'dislike', 'skip') NOT NULL,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    INDEX idx_user_rating (user_id, rating),
    INDEX idx_song_rating (song_id, rating)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 楽曲メタデータ、プレイリスト、ユーザー評価の永続化
- **Object Storage（S3）**:
  - 理由: 大規模ファイルストレージ、水平スケーリング
  - 用途: 楽曲ファイルの保存
- **Music Genome Database**:
  - 理由: 音楽ゲノムプロジェクトのデータベース
  - 用途: 楽曲の特徴分析データ

### スキーマ設計の考慮事項

1. **パーティショニング**: `songs`テーブルは`artist_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: ユーザー評価は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ラジオステーション再生

```
GET /api/v1/radio/stations/{station_id}/play
Authorization: Bearer <token>

Response (200 OK):
{
  "song": {
    "song_id": 1234567890,
    "title": "Song Title",
    "artist": "Artist Name",
    "stream_url": "https://cdn.pandora.com/..."
  },
  "next_song_id": 9876543210
}
```

#### 楽曲評価

```
POST /api/v1/songs/{song_id}/rate
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "rating": "like"
}

Response (200 OK):
{
  "status": "rated",
  "next_song_id": 9876543210
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のプレイリストのみ編集可能
- **レート制限**: 
  - ストリーミング: 無制限
  - 楽曲評価: 100回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Artist IDベースのシャーディング

```
Shard 1: artist_id % 4 == 0
Shard 2: artist_id % 4 == 1
Shard 3: artist_id % 4 == 2
Shard 4: artist_id % 4 == 3
```

**シャーディングキー**: `artist_id`
- 楽曲は`artist_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 楽曲をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 楽曲メタデータ、プレイリスト、人気楽曲
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 楽曲ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **楽曲推薦**: 音楽ゲノムプロジェクトの計算
2. **ストリーミング開始**: 楽曲ファイルの読み込み
3. **スキップ処理**: 次の楽曲の選択

### CDNの活用

- **楽曲**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 楽曲推薦最適化

1. **事前計算**: ユーザーの好みに基づいた楽曲リストを事前計算
2. **キャッシング**: 推薦結果をキャッシュ
3. **並列計算**: 複数の楽曲候補を並列で評価

### 非同期処理

#### メッセージキュー（Kafka）

1. **ユーザー評価記録**:
   ```
   Topic: user-ratings
   Partition Key: user_id
   ```

2. **レコメンデーション生成**:
   ```
   Topic: recommendation-generation
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 5,500万人
- **日間アクティブユーザー**: 2,000万人
- **1日のストリーミング数**: 5億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 600台（リージョン間で分散）
- コスト: $0.192/時間 × 600台 × 730時間 = **$84,096/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台（マスター + レプリカ）
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 60台
- コスト: $0.175/時間 × 60台 × 730時間 = **$7,665/月**

**ストレージ（S3）**:
- 楽曲ストレージ: 50 PB
- コスト: $0.023/GB/月 × 50,000,000 GB = **$1,150,000/月**

**ネットワーク**:
- データ転送: 25 PB/月
- コスト: $0.09/GB × 25,000,000 GB = **$2,250,000/月**

**合計**: 約 **$3,508,405/月**（約42,100,860ドル/年）

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

2. **楽曲バックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のプレイリストのみ編集可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - S3: サーバーサイド暗号化

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
- **ストリーミング開始**: < 2秒
- **スキップ処理**: < 500ms

### プログレッシブローディング

1. **楽曲の遅延読み込み**:
   - プレイリストの遅延読み込み
   - サムネイルを先に表示

2. **オフライン対応**:
   - オフライン時の基本機能の提供

## 12. 実装例

### ラジオサービス（疑似コード）

```python
class RadioService:
    def __init__(self, db, cache, genome_service, recommendation_service):
        self.db = db
        self.cache = cache
        self.genome_service = genome_service
        self.recommendation_service = recommendation_service
    
    async def play_station(self, station_id: int, user_id: int):
        # ユーザーの好みを取得
        user_preferences = await self.db.get_user_preferences(user_id)
        
        # キャッシュから次の楽曲を取得
        cache_key = f"station:{station_id}:user:{user_id}:next_song"
        next_song_id = await self.cache.get(cache_key)
        
        if not next_song_id:
            # 音楽ゲノムプロジェクトから類似楽曲を取得
            similar_songs = await self.genome_service.find_similar_songs(
                station_id=station_id,
                user_preferences=user_preferences
            )
            
            # レコメンデーションサービスで楽曲を選択
            next_song_id = await self.recommendation_service.select_song(
                user_id=user_id,
                candidate_songs=similar_songs
            )
            
            # キャッシュに保存
            await self.cache.set(cache_key, next_song_id, ttl=300)
        
        # 楽曲メタデータを取得
        song = await self.db.get_song(next_song_id)
        
        return {
            "song": song,
            "next_song_id": await self.get_next_song_id(station_id, user_id)
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のストリーミング数**: 5億回
- **1時間あたり**: 5億 / 24 = 約2,083万回
- **1秒あたり**: 2,083万 / 3600 = 約5,787回/秒
- **ピーク時（3倍）**: 約17,361回/秒

### ストレージ見積もり

#### 楽曲ストレージ

- **1楽曲あたりの平均サイズ**: 5 MB（高品質）
- **楽曲ライブラリ**: 3,000万曲
- **合計ストレージ**: 3,000万 × 5 MB = 150 TB
- **複数品質**: 150 TB × 3品質 = 450 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **音楽ゲノムプロジェクト**: 楽曲の特徴分析に基づく推薦
4. **CDN活用**: 楽曲をCDN経由で配信
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **楽曲推薦のレイテンシ**:
   - 問題: 音楽ゲノムプロジェクトの計算が遅い
   - 解決策: 事前計算とキャッシング

2. **スキップ処理のスケーラビリティ**:
   - 問題: スキップ時の次の楽曲選択が遅い
   - 解決策: 事前計算とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Spotify](spotify_design.md) - 音楽ストリーミング
- [Apple Music](apple_music_design.md) - 音楽ストリーミング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Booking.com](../09_hosting_rental/booking_design.md)でホスティング・レンタルプラットフォームの設計を学ぶ

