# Spotify システム設計

## 1. システム概要

### 目的と主要機能

Spotifyは、ユーザーが音楽をストリーミングで聴く音楽ストリーミングサービスです。

**主要機能**:
- 音楽のストリーミング視聴
- プレイリストの作成と管理
- レコメンデーション
- オフライン再生
- ソーシャル機能

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5億人
- **日間アクティブユーザー（DAU）**: 約2.5億人
- **1日のストリーミング時間**: 約5億時間
- **楽曲数**: 約1億曲

## 2. 機能要件

### コア機能

1. **音楽ストリーミング**
   - オーディオストリーミング
   - 複数のビットレート

2. **レコメンデーション**
   - パーソナライズされたプレイリスト
   - Discover Weekly

3. **オフライン再生**
   - ダウンロードとオフライン再生

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
Streaming Service → CDN → Object Storage
Recommendation Service → ML Service → Database
Playlist Service → Database → Cache
```

## 4. データモデル設計

### Songs テーブル

```sql
CREATE TABLE songs (
    song_id BIGINT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id BIGINT NOT NULL,
    album_id BIGINT,
    duration_seconds INT NOT NULL,
    audio_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    INDEX idx_artist_id (artist_id),
    FULLTEXT INDEX idx_title (title)
) ENGINE=InnoDB;
```

### Playlists テーブル

```sql
CREATE TABLE playlists (
    playlist_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

## 5. API設計

### 音楽ストリーミング

```
GET /api/v1/songs/{song_id}/stream
Authorization: Bearer <token>

Response (200 OK):
{
  "song_id": 1234567890,
  "title": "Song Title",
  "streaming_url": "https://cdn.spotify.com/audio/1234567890.m3u8"
}
```

## 6. スケーラビリティ設計

### 音楽ストレージ

- **Object Storage**: S3/GCSでオーディオファイルを保存
- **CDN**: CloudFrontでグローバル配信
- **複数ビットレート**: 96kbps, 160kbps, 320kbps

## 7. レイテンシ最適化

### CDNの活用

- **エッジキャッシング**: 人気楽曲をCDNでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

## 8. コスト最適化

### インフラコストの見積もり

- **ストレージ**: 約 **$2,000,000/月**（1億曲）
- **CDN**: 約 **$10,000,000/月**
- **サーバー**: 約 **$1,000,000/月**
- **合計**: 約 **$13,000,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにデプロイ
- **CDN冗長化**: 複数のCDNプロバイダーを使用

## 10. セキュリティ

### DRM保護

- **オーディオDRM**: 有料プランの楽曲をDRM保護
- **ライセンスサーバー**: DRMライセンスの配信

## 11. UX最適化

### パフォーマンス指標

- **ストリーミング開始**: < 2秒
- **レコメンデーション**: < 500ms

## 12. 実装例

### ストリーミングサービス（疑似コード）

```python
class StreamingService:
    def __init__(self, cdn, db):
        self.cdn = cdn
        self.db = db
    
    async def get_streaming_url(self, song_id: int, user_id: int):
        # 楽曲メタデータを取得
        song = await self.db.get_song(song_id)
        
        # ストリーミングURLを生成
        streaming_url = self.cdn.generate_streaming_url(
            song_id=song_id,
            bitrate="320kbps"
        )
        
        # 再生履歴を記録（非同期）
        await self.record_play(song_id, user_id)
        
        return {
            "song_id": song_id,
            "title": song["title"],
            "streaming_url": streaming_url
        }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日のストリーミング時間**: 5億時間
- **平均ビットレート**: 160 kbps
- **1日のデータ転送**: 5億時間 × 160 kbps = 80,000,000 Gbps時間
- **1日のデータ転送（GB）**: 約36,000 TB = 36 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **CDNファースト**: オーディオ配信はCDN経由
2. **レコメンデーション**: 機械学習によるパーソナライゼーション
3. **オフライン再生**: ダウンロードとオフライン再生

## 15. 関連システム

### 類似システムへのリンク

- [Apple Music](apple_music_design.md) - Appleの音楽ストリーミング
- [Pandora](pandora_design.md) - 音楽レコメンデーションサービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Reddit](reddit_design.md)でコンテンツアグリゲーションの設計を学ぶ

