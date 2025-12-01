# Netflix システム設計

## 1. システム概要

### 目的と主要機能

Netflixは、ユーザーがオンデマンドで動画コンテンツをストリーミング視聴できるサービスです。

**主要機能**:
- 動画コンテンツのストリーミング視聴
- レコメンデーション
- 複数プロファイルの管理
- オフライン視聴（ダウンロード）
- 4K/HDR動画の配信

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約2.3億人
- **日間アクティブユーザー（DAU）**: 約1.5億人
- **1日の視聴時間**: 約3.5億時間
- **1秒あたりのストリーミング開始**: 約50,000回/秒（ピーク時）
- **コンテンツライブラリ**: 約15,000タイトル

### 主要なユースケース

1. **動画視聴**: ユーザーが動画をストリーミング視聴
2. **レコメンデーション**: ユーザーに適したコンテンツを推薦
3. **検索**: タイトルでコンテンツを検索
4. **プロファイル管理**: 複数のプロファイルで視聴履歴を分離

## 2. 機能要件

### コア機能

1. **動画ストリーミング**
   - アダプティブビットレートストリーミング
   - 複数の解像度（480p, 720p, 1080p, 4K）
   - HDR動画の配信

2. **レコメンデーション**
   - パーソナライズされたレコメンデーション
   - 視聴履歴に基づく推薦

3. **コンテンツ管理**
   - コンテンツメタデータの管理
   - コンテンツの分類とタグ付け

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 動画視聴開始: < 2秒
  - レコメンデーション: < 500ms
- **スケーラビリティ**: 水平スケーリング可能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile, TV Apps)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         CDN (Edge Servers)                  │
│    (Video delivery worldwide)               │
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
│  │ Streaming│  │ Recommend│  │ Search   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      User Service                    │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┐
        │                 │                  │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐
│   Database   │  │   Cache       │  │  ML Service  │
│   (Sharded)  │  │   (Redis)     │  │  (Recommend) │
└──────────────┘  └───────────────┘  └──────────────┘
        │
┌───────▼───────────────────────────────────┐
│         Object Storage (S3)                │
│         (Encoded videos)                   │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **CDN**: 動画のグローバル配信
2. **Streaming Service**: 動画ストリーミングの管理
3. **Recommendation Service**: レコメンデーションの生成
4. **ML Service**: 機械学習モデルによるレコメンデーション
5. **Object Storage**: エンコード済み動画の保存

## 4. データモデル設計

### 主要なエンティティ

#### Content テーブル

```sql
CREATE TABLE content (
    content_id BIGINT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content_type ENUM('movie', 'tv_show', 'documentary') NOT NULL,
    release_date DATE,
    duration_minutes INT,
    rating VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content_type (content_type),
    INDEX idx_release_date (release_date),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### User_Profiles テーブル

```sql
CREATE TABLE user_profiles (
    profile_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    profile_name VARCHAR(50) NOT NULL,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

#### Watch_History テーブル

```sql
CREATE TABLE watch_history (
    history_id BIGINT PRIMARY KEY,
    profile_id BIGINT NOT NULL,
    content_id BIGINT NOT NULL,
    watch_time_seconds INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES user_profiles(profile_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    INDEX idx_profile_id (profile_id),
    INDEX idx_content_id (content_id)
) ENGINE=InnoDB;
```

## 5. API設計

### 主要なAPIエンドポイント

#### 動画ストリーミング

```
GET /api/v1/stream/{content_id}
Authorization: Bearer <token>

Response (200 OK):
{
  "content_id": 1234567890,
  "title": "Movie Title",
  "streaming_urls": {
    "480p": "https://cdn.netflix.com/video/1234567890/480p.m3u8",
    "720p": "https://cdn.netflix.com/video/1234567890/720p.m3u8",
    "1080p": "https://cdn.netflix.com/video/1234567890/1080p.m3u8",
    "4k": "https://cdn.netflix.com/video/1234567890/4k.m3u8"
  }
}
```

#### レコメンデーション

```
GET /api/v1/recommendations?profile_id=123&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "recommendations": [
    {
      "content_id": 1234567890,
      "title": "Recommended Movie",
      "match_score": 0.95
    }
  ]
}
```

## 6. スケーラビリティ設計

### CDN戦略

- **グローバルCDN**: 世界中のエッジサーバーで動画を配信
- **キャッシュヒット率**: 80%以上を目標
- **動的コンテンツ**: レコメンデーションはエッジで生成

### レコメンデーションのスケーリング

- **バッチ処理**: 日次でレコメンデーションを事前計算
- **リアルタイム更新**: 視聴履歴に基づいてリアルタイム更新
- **MLモデル**: 分散学習でモデルを訓練

## 7. レイテンシ最適化

### CDNの活用

- **エッジキャッシング**: 人気コンテンツをエッジでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

### レコメンデーションの最適化

- **事前計算**: レコメンデーションを事前計算してキャッシュ
- **キャッシング**: 人気プロファイルのレコメンデーションをキャッシュ

## 8. コスト最適化

### ストレージコスト

- **コンテンツストレージ**: 約500 PB（全コンテンツ）
- **ストレージコスト**: 約 **$10,000,000/月**（S3標準ストレージ）

### CDNコスト

- **1日のデータ転送**: 約350 PB
- **CDNコスト**: 約 **$3,500,000/日** = **$105,000,000/月**
- **キャッシュヒット率80%を考慮**: 約 **$21,000,000/月**

### コスト削減戦略

1. **CDNキャッシュ**: キャッシュヒット率を80%以上に
2. **ストレージ階層化**: 古いコンテンツをコールドストレージに移動
3. **動画圧縮**: より効率的なコーデック（AV1）を使用

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにコンテンツをレプリケート
- **CDN冗長化**: 複数のCDNプロバイダーを使用

## 10. セキュリティ

### DRM保護

- **動画DRM**: Widevine、PlayReady、FairPlay
- **ライセンスサーバー**: DRMライセンスの配信

## 11. UX最適化

### パフォーマンス指標

- **動画視聴開始**: < 2秒
- **バッファリング**: 最小限に
- **レコメンデーション**: < 500ms

## 12. 実装例

### ストリーミングサービス（疑似コード）

```python
class StreamingService:
    def __init__(self, cdn, db):
        self.cdn = cdn
        self.db = db
    
    async def get_streaming_urls(self, content_id: int, profile_id: int):
        # コンテンツメタデータを取得
        content = await self.db.get_content(content_id)
        
        # ストリーミングURLを生成
        streaming_urls = {}
        for resolution in ['480p', '720p', '1080p', '4k']:
            streaming_urls[resolution] = self.cdn.generate_streaming_url(
                content_id=content_id,
                resolution=resolution
            )
        
        return {
            "content_id": content_id,
            "title": content["title"],
            "streaming_urls": streaming_urls
        }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の視聴時間**: 3.5億時間
- **平均ビットレート**: 5 Mbps（HD）
- **1日のデータ転送**: 3.5億時間 × 5 Mbps = 1,750,000 Gbps時間
- **1日のデータ転送（GB）**: 約787,500 TB = 787.5 PB

### ストレージ見積もり

- **コンテンツライブラリ**: 15,000タイトル
- **平均タイトルサイズ**: 約33 TB（全解像度）
- **合計ストレージ**: 15,000 × 33 TB = 約495 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **CDNファースト**: 動画配信はCDN経由
2. **事前エンコード**: 全ての解像度を事前にエンコード
3. **レコメンデーション**: バッチ処理とリアルタイム処理の組み合わせ

## 15. 関連システム

### 類似システムへのリンク

- [YouTube](youtube_design.md) - 動画共有プラットフォーム
- [Twitch](twitch_design.md) - ライブストリーミング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Amazon](amazon_design.md)でEコマースプラットフォームの設計を学ぶ

