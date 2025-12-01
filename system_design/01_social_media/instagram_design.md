# Instagram システム設計

## 1. システム概要

### 目的と主要機能

Instagramは、ユーザーが写真と動画を共有するソーシャルメディアプラットフォームです。

**主要機能**:
- 写真・動画の投稿
- フィードの表示
- ストーリー（24時間有効）
- ダイレクトメッセージ
- 探索（Discover）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約20億人
- **日間アクティブユーザー（DAU）**: 約10億人
- **1日の投稿数**: 約5億投稿
- **1日のストーリー視聴**: 約5億回

## 2. 機能要件

### コア機能

1. **メディアアップロード**
   - 写真・動画のアップロード
   - フィルター適用
   - 複数の解像度へのエンコード

2. **フィード**
   - フォローしているユーザーの投稿を表示
   - アルゴリズムベースのフィード

3. **ストーリー**
   - 24時間有効なストーリー
   - ストーリーの視聴

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
Media Upload Service → Object Storage → CDN
Feed Service → Database → Cache
Story Service → Time-series DB
```

## 4. データモデル設計

### Posts テーブル

```sql
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    media_url VARCHAR(500) NOT NULL,
    caption TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC)
) ENGINE=InnoDB;
```

## 5. API設計

### 投稿作成

```
POST /api/v1/posts
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "media": <file>,
  "caption": "My photo"
}

Response (201 Created):
{
  "post_id": 1234567890,
  "media_url": "https://cdn.instagram.com/..."
}
```

## 6. スケーラビリティ設計

### メディアストレージ

- **Object Storage**: S3/GCSでメディアファイルを保存
- **CDN**: CloudFrontでグローバル配信
- **複数解像度**: サムネイル、標準、高解像度

## 7. レイテンシ最適化

### CDNの活用

- **エッジキャッシング**: メディアファイルをCDNでキャッシュ
- **地理的分散**: ユーザーに近いCDNエッジから配信

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$1,500,000/月**
- **ストレージ**: 約 **$2,000,000/月**（メディアファイル）
- **CDN**: 約 **$5,000,000/月**
- **合計**: 約 **$8,500,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにデプロイ
- **メディアのレプリケーション**: 複数リージョンにレプリケート

## 10. セキュリティ

### セキュリティ対策

- **認証**: OAuth 2.0 / JWT
- **メディアアクセス制御**: 公開/非公開設定

## 11. UX最適化

### パフォーマンス指標

- **メディアアップロード**: バックグラウンド処理
- **フィード読み込み**: < 1秒
- **ストーリー視聴**: < 500ms

## 12. 実装例

### メディアアップロードサービス（疑似コード）

```python
class MediaUploadService:
    def __init__(self, storage, db, encoding_service):
        self.storage = storage
        self.db = db
        self.encoding_service = encoding_service
    
    async def upload_media(self, user_id: int, media_file: bytes, caption: str):
        # メディアファイルをストレージにアップロード
        media_url = await self.storage.upload(media_file)
        
        # エンコーディングジョブをキューに追加
        await self.encoding_service.encode_media(media_url)
        
        # 投稿をデータベースに保存
        post_id = await self.db.create_post(
            user_id=user_id,
            media_url=media_url,
            caption=caption
        )
        
        return {"post_id": post_id, "media_url": media_url}
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の投稿数**: 5億投稿
- **1投稿あたりのメディアサイズ**: 平均5 MB
- **1日のメディアアップロード**: 5億 × 5 MB = 2.5 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **CDNファースト**: メディア配信はCDN経由
2. **非同期処理**: エンコーディングは非同期で処理
3. **キャッシング**: フィードを積極的にキャッシュ

## 15. 関連システム

### 類似システムへのリンク

- [Twitter](twitter_design.md) - マイクロブログプラットフォーム
- [Facebook](facebook_design.md) - ソーシャルネットワーク

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Facebook](facebook_design.md)でより複雑なソーシャルネットワークの設計を学ぶ

