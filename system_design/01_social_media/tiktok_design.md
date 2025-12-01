# TikTok システム設計

## 1. システム概要

### 目的と主要機能

TikTokは、ユーザーが短い動画（15秒〜3分）をアップロード、編集、共有できる動画共有プラットフォームです。AIベースの推薦アルゴリズムでパーソナライズされた動画フィードを提供します。

**主要機能**:
- 動画のアップロード・編集
- 無限スクロールの動画フィード（For You Page）
- 動画のいいね、コメント、シェア
- ユーザーのフォロー
- ライブストリーミング
- 動画検索
- ハッシュタグトレンド

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約15億人
- **日間アクティブユーザー（DAU）**: 約10億人
- **1日の動画アップロード数**: 約1億動画
- **1日の動画視聴数**: 約1000億回
- **1秒あたりの動画リクエスト数**: 約100,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **動画アップロード**: ユーザーが動画をアップロード
2. **動画視聴**: For You Pageで動画を視聴
3. **動画検索**: キーワードやハッシュタグで動画を検索
4. **ライブストリーミング**: リアルタイムでライブ配信

## 2. 機能要件

### コア機能

1. **動画管理**
   - 動画のアップロード
   - 動画のエンコード・トランスコード
   - 動画のストレージ

2. **推薦システム**
   - AIベースの動画推薦
   - パーソナライズされたフィード生成

3. **動画配信**
   - CDN経由での動画配信
   - 適応的ビットレートストリーミング（ABR）

4. **インタラクション**
   - いいね、コメント、シェア
   - フォロー/アンフォロー

5. **ライブストリーミング**
   - リアルタイム配信
   - ライブコメント

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 動画メタデータは強い一貫性、いいね数は最終的に一貫性を保つ
- **パフォーマンス**:
  - 動画アップロード: < 30秒（アップロード開始）
  - 動画再生開始: < 2秒
  - フィード読み込み: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 動画とメタデータは永続的に保存

### 優先順位付け

1. **P0（必須）**: 動画アップロード、動画視聴、推薦フィード
2. **P1（重要）**: いいね、コメント、検索
3. **P2（望ましい）**: ライブストリーミング、ハッシュタグトレンド

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
│  │ Video    │  │  Feed    │  │  ML      │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Transcoding Service            │         │
│  │      Live Streaming Service         │         │
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
│         Object Storage (S3/GCS)                   │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Video Service**: 動画のアップロードとメタデータ管理
   - **Feed Service**: 動画フィードの生成
   - **ML Service**: 推薦アルゴリズムの実行
   - **Transcoding Service**: 動画のエンコード・トランスコード
   - **Live Streaming Service**: ライブストリーミング機能
4. **Database**: 動画メタデータ、ユーザー、インタラクションの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（トランスコード、推薦更新など）
7. **Object Storage**: 動画ファイルの保存
8. **CDN**: 動画の配信

### データフロー

#### 動画アップロードのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Video Service
3. Video Service:
   a. 動画ファイルをObject Storageにアップロード
   b. メタデータをデータベースに保存
   c. Message Queueにトランスコードジョブを送信
   d. Clientに成功レスポンスを返す
4. Transcoding Service（非同期）:
   a. Message Queueからジョブを受信
   b. 動画を複数の解像度・ビットレートにトランスコード
   c. トランスコード済み動画をObject Storageに保存
   d. CDNにキャッシュを無効化
```

#### 動画視聴のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Feed Service
3. Feed Service:
   a. ML Serviceから推薦動画リストを取得
   b. 動画メタデータをCacheから取得
   c. CDN URLを生成
4. Feed Service → Client（動画URLリスト）
5. Client → CDN（動画ファイルを直接取得）
```

## 4. データモデル設計

### 主要なエンティティ

#### Videos テーブル

```sql
CREATE TABLE videos (
    video_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200),
    description TEXT,
    video_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    duration INT NOT NULL,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    comment_count BIGINT DEFAULT 0,
    share_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_view_count (view_count DESC),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Video_Likes テーブル

```sql
CREATE TABLE video_likes (
    user_id BIGINT NOT NULL,
    video_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    INDEX idx_video_id (video_id)
) ENGINE=InnoDB;
```

#### Video_Views テーブル

```sql
CREATE TABLE video_views (
    view_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    video_id BIGINT NOT NULL,
    watch_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    INDEX idx_video_id_created_at (video_id, created_at DESC),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 動画メタデータ、ユーザー、インタラクションの永続化
- **NoSQL（Cassandra）**:
  - 理由: 動画視聴履歴の書き込み負荷が高い、水平スケーリングが必要
  - 用途: 視聴履歴の保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `videos`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **デノーマライゼーション**: いいね数、視聴数などをデノーマライズして保存

## 5. API設計

### 主要なAPIエンドポイント

#### 動画アップロード

```
POST /api/v1/videos/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "file": <video_file>,
  "title": "My Video",
  "description": "Description"
}

Response (202 Accepted):
{
  "video_id": 1234567890,
  "status": "processing",
  "upload_url": "https://cdn.example.com/videos/1234567890"
}
```

#### 動画フィード取得

```
GET /api/v1/feed?limit=10&cursor=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "videos": [
    {
      "video_id": 1234567891,
      "user_id": 987654321,
      "title": "Video Title",
      "video_url": "https://cdn.example.com/videos/1234567891.mp4",
      "thumbnail_url": "https://cdn.example.com/thumbnails/1234567891.jpg",
      "duration": 30,
      "view_count": 10000,
      "like_count": 500,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "next_cursor": "1234567891"
}
```

#### 動画いいね

```
POST /api/v1/videos/{video_id}/like
Authorization: Bearer <token>

Response (200 OK):
{
  "liked": true,
  "like_count": 501
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の動画のみ削除可能
- **レート制限**: 
  - 動画アップロード: 10動画/時間
  - フィード読み込み: 30リクエスト/分

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
- 動画は`user_id`でシャーディング
- いいね、コメントは`video_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **Object Storage**: 自動スケーリング

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

1. **動画トランスコード**: CPU集約的な処理
2. **動画配信**: 大きなファイルサイズ
3. **推薦アルゴリズム**: ML推論のレイテンシ

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

1. **動画アップロードイベント**:
   ```
   Topic: video-uploaded
   Partition Key: user_id
   ```

2. **トランスコードジョブ**:
   - 非同期で動画をトランスコード
   - 複数のワーカーで並列処理

3. **推薦更新**:
   - 動画視聴履歴を非同期で処理
   - 推薦モデルを更新

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 15億人
- **日間アクティブユーザー**: 10億人
- **1日の動画アップロード数**: 1億動画
- **1日の動画視聴数**: 1000億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 2,000台（リージョン間で分散）
- コスト: $0.192/時間 × 2,000台 × 730時間 = **$280,320/月**

**トランスコードサーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 500台
- コスト: $0.34/時間 × 500台 × 730時間 = **$124,100/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.76/時間 × 80台 × 730時間 = **$44,384/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 200台
- コスト: $0.175/時間 × 200台 × 730時間 = **$25,550/月**

**ストレージ（S3）**:
- 動画ストレージ: 100 PB
- コスト: $0.023/GB/月 × 100,000,000 GB = **$2,300,000/月**

**ネットワーク（CDN）**:
- データ転送: 50 PB/月
- コスト: $0.085/GB × 50,000,000 GB = **$4,250,000/月**

**合計**: 約 **$7,024,354/月**（約84,292,248ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: トランスコードジョブで最大90%削減
3. **動画圧縮**: ストレージコストを削減
4. **CDN活用**: データ転送コストを削減
5. **動画のライフサイクル管理**: 古い動画を低コストストレージに移動

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
   - ユーザーは自分の動画のみ削除可能

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

1. **無限スクロール**: 
   - ページネーションの代わりに無限スクロール
   - ビューポートに近づいたら次の動画を読み込み

2. **動画の遅延読み込み**:
   - ビューポートに入るまで動画を読み込まない
   - サムネイルを先に表示

3. **適応的ビットレートストリーミング（ABR）**:
   - ネットワーク状況に応じてビットレートを調整
   - スムーズな再生体験を提供

## 12. 実装例

### 動画アップロードサービス（疑似コード）

```python
class VideoService:
    def __init__(self, db, s3, message_queue):
        self.db = db
        self.s3 = s3
        self.message_queue = message_queue
    
    async def upload_video(self, user_id: int, video_file, metadata):
        # S3にアップロード
        video_url = await self.s3.upload_file(
            bucket="tiktok-videos",
            key=f"{user_id}/{uuid.uuid4()}.mp4",
            file=video_file
        )
        
        # データベースにメタデータを保存
        video_id = await self.db.insert_video(
            user_id=user_id,
            video_url=video_url,
            title=metadata["title"],
            description=metadata["description"]
        )
        
        # トランスコードジョブをキューに送信
        await self.message_queue.publish(
            topic="video-uploaded",
            message={
                "video_id": video_id,
                "video_url": video_url,
                "user_id": user_id
            }
        )
        
        return {
            "video_id": video_id,
            "status": "processing"
        }
```

### 動画フィードサービス（疑似コード）

```python
class FeedService:
    def __init__(self, db, cache, ml_service):
        self.db = db
        self.cache = cache
        self.ml_service = ml_service
    
    async def get_feed(self, user_id: int, limit: int = 10, cursor: str = None):
        # ML Serviceから推薦動画IDリストを取得
        recommended_video_ids = await self.ml_service.get_recommendations(
            user_id=user_id,
            limit=limit,
            cursor=cursor
        )
        
        # 動画メタデータを取得
        videos = []
        for video_id in recommended_video_ids:
            # キャッシュから取得を試みる
            cache_key = f"video:{video_id}"
            cached_video = await self.cache.get(cache_key)
            
            if cached_video:
                videos.append(cached_video)
            else:
                video = await self.db.get_video(video_id)
                await self.cache.set(cache_key, video, ttl=900)
                videos.append(video)
        
        return videos
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の動画視聴数**: 1000億回
- **1時間あたり**: 1000億 / 24 = 約41.67億回
- **1秒あたり**: 41.67億 / 3600 = 約115.75万回/秒
- **ピーク時（3倍）**: 約347.25万回/秒

#### 書き込みトラフィック

- **1日の動画アップロード数**: 1億動画
- **1時間あたり**: 1億 / 24 = 約416万動画
- **1秒あたり**: 416万 / 3600 = 約1,156動画/秒
- **ピーク時（3倍）**: 約3,468動画/秒

### ストレージ見積もり

#### 動画ストレージ

- **1動画あたりのサイズ**: 平均10 MB
- **1日の動画アップロード数**: 1億動画
- **1日のストレージ**: 1億 × 10 MB = 1 PB
- **1年のストレージ**: 1 PB × 365 = 約365 PB
- **5年のストレージ**: 約1,825 PB

### 帯域幅見積もり

#### 動画配信帯域幅

- **1動画あたりのサイズ**: 平均10 MB
- **1秒あたりの視聴**: 347.25万回/秒（ピーク時）
- **配信帯域幅**: 347.25万 × 10 MB = 34.725 TB/秒 = 約277.8 Tbps

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **CDNファースト**: 動画はCDN経由で配信
4. **適応的ビットレートストリーミング**: ネットワーク状況に応じてビットレートを調整
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **動画トランスコードのボトルネック**:
   - 問題: トランスコードが遅い
   - 解決策: 非同期処理と並列化

2. **動画配信のコスト**:
   - 問題: CDNコストが高い
   - 解決策: 動画圧縮、適応的ビットレートストリーミング

## 15. 関連システム

### 類似システムへのリンク

- [YouTube](youtube_design.md) - 動画共有プラットフォーム
- [Instagram](instagram_design.md) - メディア中心のソーシャルメディア
- [Netflix](netflix_design.md) - ストリーミングサービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Twitch](twitch_design.md)でライブストリーミングプラットフォームの設計を学ぶ

