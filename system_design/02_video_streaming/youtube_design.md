# YouTube システム設計

## 1. システム概要

### 目的と主要機能

YouTubeは、ユーザーが動画をアップロード、視聴、共有できる動画共有プラットフォームです。

**主要機能**:
- 動画のアップロード
- 動画のストリーミング視聴
- 動画の検索と発見
- コメント、いいね、チャンネル登録
- ライブストリーミング
- レコメンデーション

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約20億人
- **日間アクティブユーザー（DAU）**: 約10億人
- **1時間あたりのアップロード**: 約500時間分の動画
- **1日の視聴時間**: 約10億時間
- **1秒あたりの視聴開始**: 約30,000回/秒（ピーク時）

### 主要なユースケース

1. **動画アップロード**: ユーザーが動画をアップロード
2. **動画視聴**: ユーザーが動画をストリーミング視聴
3. **動画検索**: キーワードで動画を検索
4. **レコメンデーション**: ユーザーに適した動画を推薦

## 2. 機能要件

### コア機能

1. **動画アップロード**
   - 動画ファイルのアップロード
   - 複数の解像度とビットレートへのエンコード
   - サムネイル生成

2. **動画ストリーミング**
   - アダプティブビットレートストリーミング
   - 複数の解像度（144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p）
   - 低レイテンシストリーミング

3. **検索と発見**
   - 動画の全文検索
   - レコメンデーションアルゴリズム
   - トレンド動画

4. **エンゲージメント**
   - コメント、いいね、チャンネル登録
   - プレイリスト作成

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 動画アップロード: バックグラウンド処理（非同期）
  - 動画視聴開始: < 2秒
  - 検索: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **ストレージ**: 膨大な動画ファイルの保存

### 優先順位付け

1. **P0（必須）**: 動画アップロード、動画視聴、検索
2. **P1（重要）**: レコメンデーション、コメント、いいね
3. **P2（望ましい）**: ライブストリーミング、4K動画

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS
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
│  │ Upload   │  │ Streaming│  │ Search   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Video Metadata Service           │         │
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
│              Video Processing Pipeline                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Encoding │  │ Thumbnail│  │ Metadata │            │
│  │ Service  │  │ Service  │  │ Extract  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼──────────────┼──────────────┼──────────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼──────┐
│         Object Storage (S3/GCS)            │
│         (Raw videos, Encoded videos)      │
└───────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────┐
│              CDN (Edge Servers)            │
│         (Video delivery worldwide)        │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Upload Service**: 動画アップロードの受け付け
   - **Streaming Service**: 動画ストリーミングの配信
   - **Search Service**: 動画の検索
   - **Video Metadata Service**: 動画メタデータの管理
4. **Video Processing Pipeline**:
   - **Encoding Service**: 動画のエンコード
   - **Thumbnail Service**: サムネイル生成
   - **Metadata Extract**: 動画メタデータの抽出
5. **Object Storage**: 動画ファイルの保存（S3/GCS）
6. **CDN**: 動画のグローバル配信

### データフロー

#### 動画アップロードのフロー

```
1. Client → Load Balancer → API Gateway → Upload Service
2. Upload Service:
   a. 動画ファイルをObject Storageにアップロード
   b. メタデータをデータベースに保存
   c. Message Queueにエンコードジョブを送信
3. Encoding Service（非同期）:
   a. Message Queueからジョブを受信
   b. 複数の解像度とビットレートにエンコード
   c. エンコード済み動画をObject Storageに保存
   d. メタデータを更新
4. Thumbnail Service（非同期）:
   a. サムネイルを生成
   b. Object Storageに保存
```

#### 動画視聴のフロー

```
1. Client → Load Balancer → API Gateway → Streaming Service
2. Streaming Service:
   a. 動画メタデータをデータベースから取得
   b. CDN URLを生成
   c. クライアントにストリーミングURLを返す
3. Client → CDN:
   a. CDNから動画をストリーミング受信
   b. アダプティブビットレートストリーミング
```

## 4. データモデル設計

### 主要なエンティティ

#### Videos テーブル

```sql
CREATE TABLE videos (
    video_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration INT NOT NULL, -- seconds
    status ENUM('uploading', 'processing', 'ready', 'failed') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    view_count BIGINT DEFAULT 0,
    like_count INT DEFAULT 0,
    dislike_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Video_Encodings テーブル

```sql
CREATE TABLE video_encodings (
    encoding_id BIGINT PRIMARY KEY,
    video_id BIGINT NOT NULL,
    resolution VARCHAR(10) NOT NULL, -- '144p', '240p', '360p', etc.
    bitrate INT NOT NULL, -- kbps
    file_size BIGINT NOT NULL, -- bytes
    storage_url VARCHAR(500) NOT NULL,
    codec VARCHAR(20) NOT NULL, -- 'h264', 'vp9', 'av1'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    INDEX idx_video_id (video_id),
    INDEX idx_resolution (resolution)
) ENGINE=InnoDB;
```

#### Users テーブル

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    channel_name VARCHAR(100),
    channel_description TEXT,
    subscriber_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB;
```

#### Comments テーブル

```sql
CREATE TABLE comments (
    comment_id BIGINT PRIMARY KEY,
    video_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    parent_comment_id BIGINT, -- for nested comments
    like_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(video_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(comment_id),
    INDEX idx_video_id (video_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: メタデータの管理、複雑なクエリ、トランザクション処理
  - 用途: 動画メタデータ、ユーザー、コメント
- **NoSQL（Cassandra）**:
  - 理由: 動画視聴履歴の書き込み負荷が高い
  - 用途: 視聴履歴、レコメンデーション用データ
- **Object Storage（S3/GCS）**:
  - 理由: 大容量ファイルの保存、コスト効率
  - 用途: 動画ファイルの保存

## 5. API設計

### 主要なAPIエンドポイント

#### 動画アップロード開始

```
POST /api/v1/videos/upload
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "My Video",
  "description": "Video description",
  "file_size": 104857600, -- 100 MB
  "content_type": "video/mp4"
}

Response (201 Created):
{
  "video_id": 1234567890,
  "upload_url": "https://storage.googleapis.com/upload/...",
  "upload_token": "abc123..."
}
```

#### 動画アップロード完了

```
POST /api/v1/videos/{video_id}/upload/complete
Authorization: Bearer <token>

Response (200 OK):
{
  "video_id": 1234567890,
  "status": "processing"
}
```

#### 動画ストリーミング

```
GET /api/v1/videos/{video_id}/stream
Authorization: Bearer <token>

Response (200 OK):
{
  "video_id": 1234567890,
  "title": "My Video",
  "streaming_urls": {
    "144p": "https://cdn.youtube.com/video/1234567890/144p.m3u8",
    "240p": "https://cdn.youtube.com/video/1234567890/240p.m3u8",
    "360p": "https://cdn.youtube.com/video/1234567890/360p.m3u8",
    "480p": "https://cdn.youtube.com/video/1234567890/480p.m3u8",
    "720p": "https://cdn.youtube.com/video/1234567890/720p.m3u8",
    "1080p": "https://cdn.youtube.com/video/1234567890/1080p.m3u8"
  },
  "thumbnail_url": "https://cdn.youtube.com/thumbnails/1234567890.jpg"
}
```

#### 動画検索

```
GET /api/v1/search?q=hello&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "videos": [
    {
      "video_id": 1234567890,
      "title": "Hello World",
      "thumbnail_url": "...",
      "view_count": 1000000,
      "duration": 300
    }
  ],
  "total_results": 1000
}
```

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Video IDベースのシャーディング

```
Shard 1: video_id % 8 == 0
Shard 2: video_id % 8 == 1
...
Shard 8: video_id % 8 == 7
```

**シャーディングキー**: `video_id`
- 動画メタデータは`video_id`でシャーディング
- コメントは`video_id`でシャーディング

### 動画ストレージの分散

- **Object Storage**: 複数のリージョンに分散
- **CDN**: 世界中のエッジサーバーでキャッシュ
- **レプリケーション**: 人気動画は複数のリージョンにレプリケート

### エンコーディングのスケーリング

- **ワーカープール**: エンコーディングワーカーを水平スケーリング
- **キュー管理**: メッセージキューでジョブを管理
- **優先度**: 人気動画や有料動画を優先エンコード

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 動画メタデータ、人気動画リスト
   - TTL: 5-15分

2. **L2 Cache（Redis）**:
   - 用途: 動画メタデータ、検索結果
   - TTL: 15-30分

3. **L3 Cache（CDN）**:
   - 用途: 動画ファイル、サムネイル
   - TTL: 24時間-7日（動画の種類による）

## 7. レイテンシ最適化

### ボトルネックの特定

1. **動画エンコーディング**: 時間がかかる処理
2. **動画配信**: 大容量ファイルの転送
3. **検索**: 大規模なインデックス検索

### CDNの活用

- **動画配信**: CloudflareまたはAWS CloudFront
- **エッジキャッシング**: 人気動画をエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### アダプティブビットレートストリーミング

- **HLS（HTTP Live Streaming）**: Appleのストリーミングプロトコル
- **DASH（Dynamic Adaptive Streaming over HTTP）**: オープンスタンダード
- **品質の自動調整**: ネットワーク状況に応じて品質を調整

### 動画エンコーディングの最適化

1. **並列エンコーディング**: 複数の解像度を並列でエンコード
2. **GPUアクセラレーション**: GPUでエンコーディングを高速化
3. **事前エンコーディング**: アップロード時に全ての解像度をエンコード

### 検索の最適化

1. **インデックス最適化**: Elasticsearchで全文検索
2. **キャッシング**: 人気検索クエリをキャッシュ
3. **ファセット検索**: フィルタリングで結果を絞り込み

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 20億人
- **1時間あたりのアップロード**: 500時間分の動画
- **1日の視聴時間**: 10億時間
- **平均動画サイズ**: 100 MB（1080p、10分）
- **平均エンコード時間**: 動画時間の2倍

#### ストレージコスト

**動画ストレージ**:
- **1時間あたりのアップロード**: 500時間分
- **1時間あたりのストレージ**: 500時間 × 100 MB/10分 × 6 = 30 GB/時間
- **1日のストレージ**: 30 GB × 24 = 720 GB/日
- **1年のストレージ**: 720 GB × 365 = 262.8 TB/年
- **5年のストレージ**: 約1.314 PB

**エンコード済み動画**:
- **解像度数**: 8種類（144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p）
- **平均サイズ**: 解像度ごとに異なる（144p: 5 MB, 1080p: 100 MB）
- **合計ストレージ**: 約10 PB（5年分）

**ストレージコスト（GCS）**:
- **標準ストレージ**: $0.020/GB/月
- **ニアラインストレージ**: $0.010/GB/月（30日以上アクセスされない動画）
- **合計ストレージコスト**: 約 **$200,000/月**（10 PB）

#### エンコーディングコスト

**エンコーディングワーカー**:
- **1時間あたりのエンコード時間**: 500時間 × 2 = 1,000時間
- **必要なワーカー数**: 1,000時間 / 1時間 = 1,000ワーカー
- **EC2インスタンス**: c5.2xlarge (8 vCPU, 16 GB RAM)
- **コスト**: $0.34/時間 × 1,000台 × 730時間 = **$248,200/月**

#### CDNコスト

**動画配信**:
- **1日の視聴時間**: 10億時間
- **平均ビットレート**: 2 Mbps
- **1日のデータ転送**: 10億時間 × 2 Mbps = 2,000,000 Gbps時間
- **1日のデータ転送（GB）**: 約900,000 TB = 900 PB
- **CDNコスト（Cloudflare）**: $0.01/GB
- **1日のCDNコスト**: 900 PB × $0.01/GB = **$9,000,000/日** = **$270,000,000/月**

**注**: 実際にはCDNキャッシュにより、オリジンへのリクエストは大幅に削減されます。

#### 合計コスト（概算）

- **ストレージ**: $200,000/月
- **エンコーディング**: $248,200/月
- **CDN**: $270,000,000/月（キャッシュヒット率を考慮すると大幅に削減）
- **その他（データベース、アプリケーションサーバーなど）**: $500,000/月
- **合計**: 約 **$270,948,200/月**（CDNキャッシュヒット率80%を考慮すると約 **$54,948,200/月**）

### コスト削減戦略

1. **CDNキャッシュ**: キャッシュヒット率を80%以上に
2. **ストレージ階層化**: 
   - ホットストレージ: 最近アップロードされた動画
   - コールドストレージ: 古い動画（30日以上アクセスなし）
3. **エンコーディング最適化**: 
   - GPUアクセラレーションで高速化
   - 不要な解像度のエンコードをスキップ
4. **動画圧縮**: より効率的なコーデック（AV1）を使用

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - 動画ファイルの複数リージョンへのレプリケーション

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - CDNエッジサーバーのヘルスチェック

3. **フォールバック**:
   - CDN障害時はオリジンサーバーから配信
   - エンコーディング失敗時のリトライ

### 動画ファイルの冗長化

- **マルチリージョンレプリケーション**: 人気動画は複数リージョンにレプリケート
- **エラーの訂正**: レプリケーションによるデータの整合性

### バックアップ・復旧戦略

1. **メタデータバックアップ**:
   - 日次フルバックアップ
   - ポイントインタイムリカバリ

2. **動画ファイルバックアップ**:
   - Object Storageの自動バックアップ
   - 複数リージョンへのレプリケーション

3. **災害復旧**:
   - RTO: 4時間
   - RPO: 1時間

## 10. セキュリティ

### 認証・認可

1. **認証**: OAuth 2.0 / JWT
2. **認可**: ユーザーは自分の動画のみ削除可能
3. **動画アクセス制御**: 
   - 公開動画: 誰でも視聴可能
   - 非公開動画: リンクを知っている人のみ
   - 限定公開動画: 指定したユーザーのみ

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: Object Storageの暗号化
3. **動画DRM**: 有料動画のDRM保護

### DDoS対策

1. **レート制限**: IPアドレスベースのレート制限
2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewall

## 11. UX最適化

### パフォーマンス指標

- **動画視聴開始時間**: < 2秒
- **バッファリング**: 最小限に
- **検索**: < 500ms

### プログレッシブローディング

1. **サムネイルの先行読み込み**: リスト表示時にサムネイルを先行読み込み
2. **動画の遅延読み込み**: ビューポートに入るまで動画を読み込まない
3. **品質の自動調整**: ネットワーク状況に応じて品質を調整

### オフライン対応

1. **オフライン視聴**: 動画のダウンロードとオフライン視聴
2. **オフラインアップロード**: オフライン時の動画アップロードキューイング

## 12. 実装例

### 動画アップロードサービス（疑似コード）

```python
class VideoUploadService:
    def __init__(self, storage, db, message_queue):
        self.storage = storage
        self.db = db
        self.message_queue = message_queue
    
    async def initiate_upload(self, user_id: int, metadata: dict):
        # 動画メタデータをデータベースに保存
        video_id = await self.db.create_video(
            user_id=user_id,
            title=metadata["title"],
            description=metadata.get("description", ""),
            status="uploading"
        )
        
        # アップロードURLを生成
        upload_url = await self.storage.generate_upload_url(
            video_id=video_id,
            file_size=metadata["file_size"]
        )
        
        return {
            "video_id": video_id,
            "upload_url": upload_url
        }
    
    async def complete_upload(self, video_id: int):
        # 動画ファイルの存在確認
        if not await self.storage.file_exists(f"videos/{video_id}/original.mp4"):
            raise ValueError("Video file not found")
        
        # 動画メタデータを取得
        video = await self.db.get_video(video_id)
        
        # エンコーディングジョブをキューに追加
        await self.message_queue.publish(
            topic="video-encoding",
            message={
                "video_id": video_id,
                "storage_path": f"videos/{video_id}/original.mp4"
            }
        )
        
        # ステータスを更新
        await self.db.update_video_status(video_id, "processing")
```

### 動画ストリーミングサービス（疑似コード）

```python
class VideoStreamingService:
    def __init__(self, db, cdn):
        self.db = db
        self.cdn = cdn
    
    async def get_streaming_urls(self, video_id: int, user_id: int = None):
        # 動画メタデータを取得
        video = await self.db.get_video(video_id)
        
        if video["status"] != "ready":
            raise ValueError("Video is not ready")
        
        # エンコード情報を取得
        encodings = await self.db.get_video_encodings(video_id)
        
        # ストリーミングURLを生成
        streaming_urls = {}
        for encoding in encodings:
            streaming_urls[encoding["resolution"]] = self.cdn.generate_streaming_url(
                video_id=video_id,
                resolution=encoding["resolution"],
                codec=encoding["codec"]
            )
        
        # 視聴履歴を記録（非同期）
        await self.record_view(video_id, user_id)
        
        return {
            "video_id": video_id,
            "title": video["title"],
            "streaming_urls": streaming_urls,
            "thumbnail_url": self.cdn.get_thumbnail_url(video_id)
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 動画アップロード

- **1時間あたりのアップロード**: 500時間分の動画
- **平均動画サイズ**: 100 MB（1080p、10分）
- **1時間あたりのアップロードサイズ**: 500時間 × 100 MB/10分 × 6 = 30 GB/時間
- **1秒あたりのアップロード**: 30 GB / 3600 = 約8.3 MB/秒

#### 動画視聴

- **1日の視聴時間**: 10億時間
- **平均ビットレート**: 2 Mbps
- **1日のデータ転送**: 10億時間 × 2 Mbps = 2,000,000 Gbps時間
- **1日のデータ転送（GB）**: 約900,000 TB = 900 PB
- **1秒あたりのデータ転送**: 900 PB / 86400 = 約10.4 TB/秒

### ストレージ見積もり

#### 動画ストレージ（5年間）

- **1日のアップロード**: 720 GB
- **5年間のアップロード**: 720 GB × 365 × 5 = 1.314 PB
- **エンコード済み動画**: 1.314 PB × 8解像度 = 10.512 PB
- **合計ストレージ**: 約 **11.826 PB**

### エンコーディングリソース

- **1時間あたりのエンコード時間**: 500時間 × 2 = 1,000時間
- **必要なワーカー数**: 1,000ワーカー（同時実行）
- **EC2インスタンス**: c5.2xlarge (8 vCPU)
- **合計vCPU**: 1,000 × 8 = 8,000 vCPU

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **非同期処理**: エンコーディングは非同期で処理
2. **CDN活用**: 動画配信はCDN経由
3. **ストレージ階層化**: ホット/コールドストレージを使い分け
4. **アダプティブストリーミング**: ネットワーク状況に応じた品質調整

### よくある落とし穴

1. **エンコーディングのボトルネック**:
   - 問題: エンコーディングが遅い
   - 解決策: GPUアクセラレーション、並列処理

2. **ストレージコスト**:
   - 問題: ストレージコストが高い
   - 解決策: ストレージ階層化、古い動画のアーカイブ

3. **CDNコスト**:
   - 問題: CDNコストが高い
   - 解決策: キャッシュヒット率の向上、エッジキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Netflix](netflix_design.md) - オンデマンドストリーミングサービス
- [Twitch](twitch_design.md) - ライブストリーミングプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Netflix](netflix_design.md)でオンデマンドストリーミングの設計を学ぶ

