# Hulu システム設計

## 1. システム概要

### 目的と主要機能

Huluは、ユーザーが映画やテレビ番組をオンデマンドで視聴できる動画ストリーミングサービスです。ライブテレビ配信も提供しています。

**主要機能**:
- 動画のオンデマンドストリーミング
- ライブテレビ配信
- パーソナライズされた推薦
- ウォッチリスト（視聴リスト）
- 視聴履歴
- 複数プロファイル対応

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約4,800万人
- **日間アクティブユーザー（DAU）**: 約2,000万人
- **1日の動画視聴数**: 約5億回
- **1秒あたりの動画リクエスト数**: 約20,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **動画視聴**: ユーザーが動画をストリーミング視聴
2. **ライブテレビ視聴**: ユーザーがライブテレビを視聴
3. **推薦**: パーソナライズされた動画推薦
4. **ウォッチリスト**: 視聴したい動画を保存

## 2. 機能要件

### コア機能

1. **動画ストリーミング**
   - 動画のオンデマンドストリーミング
   - 適応的ビットレートストリーミング（ABR）
   - 複数の解像度・ビットレート対応

2. **ライブテレビ**
   - ライブテレビチャンネルの配信
   - タイムシフト視聴（過去の番組を視聴）

3. **推薦システム**
   - パーソナライズされた動画推薦
   - 視聴履歴に基づく推薦

4. **ユーザー管理**
   - 複数プロファイル対応
   - 視聴履歴の保存
   - ウォッチリスト

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 視聴履歴は最終的に一貫性を保つ
- **パフォーマンス**:
  - 動画再生開始: < 2秒
  - 推薦取得: < 500ms
  - ライブテレビ視聴開始: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 動画とメタデータは永続的に保存

### 優先順位付け

1. **P0（必須）**: 動画ストリーミング、推薦、ユーザー管理
2. **P1（重要）**: ライブテレビ、ウォッチリスト
3. **P2（望ましい）**: タイムシフト視聴、複数プロファイル

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps, Smart TV)
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
│  │ Video    │  │  Live    │  │  ML      │        │
│  │ Service  │  │  TV      │  │ Service  │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      User Service                    │         │
│  │      Recommendation Service          │         │
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
│         CDN (CloudFront/Cloudflare)               │
│         Object Storage (S3)                      │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Video Service**: 動画の管理とストリーミング
   - **Live TV Service**: ライブテレビの配信
   - **ML Service**: 推薦アルゴリズムの実行
   - **User Service**: ユーザー管理とプロファイル
   - **Recommendation Service**: 推薦の生成
4. **Database**: 動画メタデータ、ユーザー、視聴履歴の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（視聴履歴の記録など）
7. **CDN**: 動画の配信
8. **Object Storage**: 動画ファイルの保存

### データフロー

#### 動画視聴のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Video Service
3. Video Service:
   a. 動画メタデータをCacheから取得
   b. CDN URLを生成
   c. 視聴履歴をMessage Queueに送信
4. Video Service → Client（動画URL）
5. Client → CDN（動画ファイルを直接取得）
```

#### 推薦取得のフロー

```
1. Client → API Gateway → Recommendation Service
2. Recommendation Service:
   a. ML Serviceから推薦動画IDリストを取得
   b. 動画メタデータをCacheから取得
   c. 推薦リストを返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Videos テーブル

```sql
CREATE TABLE videos (
    video_id BIGINT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    genre VARCHAR(100),
    release_date DATE,
    duration INT NOT NULL,
    rating VARCHAR(10),
    video_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_genre (genre),
    INDEX idx_release_date (release_date DESC),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Watch_History テーブル

```sql
CREATE TABLE watch_history (
    history_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    video_id BIGINT NOT NULL,
    watch_time INT DEFAULT 0,
    last_watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    INDEX idx_user_profile_last_watched (user_id, profile_id, last_watched_at DESC),
    INDEX idx_video_id (video_id)
) ENGINE=InnoDB;
```

#### Watchlist テーブル

```sql
CREATE TABLE watchlist (
    user_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    video_id BIGINT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, profile_id, video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    INDEX idx_user_profile_added (user_id, profile_id, added_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 動画メタデータ、ユーザー、視聴履歴の永続化
- **NoSQL（Cassandra）**:
  - 理由: 視聴履歴の書き込み負荷が高い、水平スケーリングが必要
  - 用途: 視聴履歴の保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `watch_history`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 視聴履歴は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 動画情報取得

```
GET /api/v1/videos/{video_id}
Authorization: Bearer <token>

Response (200 OK):
{
  "video_id": 1234567890,
  "title": "Movie Title",
  "description": "Description",
  "duration": 7200,
  "video_url": "https://cdn.hulu.com/videos/1234567890.m3u8",
  "thumbnail_url": "https://cdn.hulu.com/thumbnails/1234567890.jpg"
}
```

#### 推薦取得

```
GET /api/v1/recommendations?limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "videos": [
    {
      "video_id": 1234567891,
      "title": "Recommended Movie",
      "thumbnail_url": "https://cdn.hulu.com/thumbnails/1234567891.jpg"
    }
  ]
}
```

#### 視聴履歴記録

```
POST /api/v1/watch-history
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "video_id": 1234567890,
  "profile_id": 987654321,
  "watch_time": 300
}

Response (200 OK):
{
  "status": "recorded"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のプロファイルのみアクセス可能
- **レート制限**: 
  - 動画視聴: 無制限
  - 推薦取得: 30リクエスト/分

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
- 視聴履歴は`user_id`でシャーディング
- ウォッチリストは`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 動画ファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 動画メタデータ、推薦リスト
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 動画ファイル、サムネイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **動画配信**: 大きなファイルサイズ
2. **推薦アルゴリズム**: ML推論のレイテンシ
3. **視聴履歴の記録**: 書き込み負荷

### CDNの活用

- **動画配信**: CloudflareまたはAWS CloudFront
- **適応的ビットレートストリーミング（ABR）**: ネットワーク状況に応じてビットレートを調整
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 動画配信最適化

1. **事前エンコード**: 複数の解像度・ビットレートに事前エンコード
2. **プログレッシブダウンロード**: 動画の先頭部分を優先的に配信
3. **チャンク配信**: 動画を小さなチャンクに分割して配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **視聴履歴記録**:
   ```
   Topic: watch-history
   Partition Key: user_id
   ```

2. **推薦更新**:
   - 視聴履歴を非同期で処理
   - 推薦モデルを更新

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 4,800万人
- **日間アクティブユーザー**: 2,000万人
- **1日の動画視聴数**: 5億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 500台（リージョン間で分散）
- コスト: $0.192/時間 × 500台 × 730時間 = **$70,080/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台（マスター + レプリカ）
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 50台
- コスト: $0.175/時間 × 50台 × 730時間 = **$6,387.50/月**

**ストレージ（S3）**:
- 動画ストレージ: 20 PB
- コスト: $0.023/GB/月 × 20,000,000 GB = **$460,000/月**

**ネットワーク（CDN）**:
- データ転送: 10 PB/月
- コスト: $0.085/GB × 10,000,000 GB = **$850,000/月**

**合計**: 約 **$1,403,111.50/月**（約16,837,338ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **動画圧縮**: ストレージコストを削減
3. **CDN活用**: データ転送コストを削減
4. **動画のライフサイクル管理**: 古い動画を低コストストレージに移動

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

2. **動画バックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のプロファイルのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - Object Storage: S3サーバーサイド暗号化

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
- **動画再生開始**: < 2秒

### プログレッシブローディング

1. **適応的ビットレートストリーミング（ABR）**:
   - ネットワーク状況に応じてビットレートを調整
   - スムーズな再生体験を提供

2. **事前読み込み**:
   - 次の動画を事前に読み込み
   - シームレスな視聴体験

## 12. 実装例

### 動画サービス（疑似コード）

```python
class VideoService:
    def __init__(self, db, cache, cdn):
        self.db = db
        self.cache = cache
        self.cdn = cdn
    
    async def get_video(self, video_id: int):
        # キャッシュから取得を試みる
        cache_key = f"video:{video_id}"
        cached_video = await self.cache.get(cache_key)
        
        if cached_video:
            return cached_video
        
        # データベースから取得
        video = await self.db.get_video(video_id)
        
        # CDN URLを生成
        video["video_url"] = self.cdn.generate_url(video_id)
        
        # キャッシュに保存
        await self.cache.set(cache_key, video, ttl=900)
        
        return video
```

### 推薦サービス（疑似コード）

```python
class RecommendationService:
    def __init__(self, db, cache, ml_service):
        self.db = db
        self.cache = cache
        self.ml_service = ml_service
    
    async def get_recommendations(self, user_id: int, profile_id: int, limit: int = 20):
        # ML Serviceから推薦動画IDリストを取得
        recommended_video_ids = await self.ml_service.get_recommendations(
            user_id=user_id,
            profile_id=profile_id,
            limit=limit
        )
        
        # 動画メタデータを取得
        videos = []
        for video_id in recommended_video_ids:
            video = await self.db.get_video(video_id)
            videos.append(video)
        
        return videos
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の動画視聴数**: 5億回
- **1時間あたり**: 5億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

### ストレージ見積もり

#### 動画ストレージ

- **1動画あたりの平均サイズ**: 5 GB
- **動画ライブラリ**: 10,000タイトル
- **合計ストレージ**: 10,000 × 5 GB = 50 TB
- **複数解像度・ビットレート**: 50 TB × 5 = 250 TB
- **1年のストレージ**: 約250 TB（新規追加を考慮）

### 帯域幅見積もり

#### 動画配信帯域幅

- **1動画あたりの平均帯域幅**: 5 Mbps
- **同時視聴者数**: 100万人（ピーク時）
- **配信帯域幅**: 100万 × 5 Mbps = 5 Tbps

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **CDNファースト**: 動画はCDN経由で配信
4. **適応的ビットレートストリーミング**: ネットワーク状況に応じてビットレートを調整
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **動画配信のコスト**:
   - 問題: CDNコストが高い
   - 解決策: 動画圧縮、適応的ビットレートストリーミング

2. **推薦アルゴリズムのレイテンシ**:
   - 問題: ML推論が遅い
   - 解決策: キャッシング、事前計算

## 15. 関連システム

### 類似システムへのリンク

- [Netflix](netflix_design.md) - 動画ストリーミングサービス
- [YouTube](youtube_design.md) - 動画共有プラットフォーム
- [Spotify](spotify_design.md) - 音楽ストリーミングサービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [eBay](ebay_design.md)でEコマースプラットフォームの設計を学ぶ

