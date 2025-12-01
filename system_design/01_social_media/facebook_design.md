# Facebook システム設計

## 1. システム概要

### 目的と主要機能

Facebookは、ユーザーがコンテンツを共有し、コミュニケーションを取るソーシャルネットワークプラットフォームです。

**主要機能**:
- ニュースフィード
- 友達リクエストと承認
- グループとページ
- イベント
- メッセンジャー
- ライブストリーミング

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約30億人
- **日間アクティブユーザー（DAU）**: 約20億人
- **1日の投稿数**: 約50億投稿
- **1日のニュースフィード読み込み**: 約200億回

## 2. 機能要件

### コア機能

1. **ニュースフィード**
   - アルゴリズムベースのフィード
   - リアルタイム更新

2. **ソーシャルグラフ**
   - 友達関係の管理
   - グラフトラバーサル

3. **コンテンツ共有**
   - テキスト、画像、動画の共有
   - リアクション（いいね、コメント、シェア）

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
News Feed Service → Graph Database → Cache
Social Graph Service → Neo4j / Custom Graph DB
Content Service → Database → Object Storage → CDN
```

## 4. データモデル設計

### Posts テーブル

```sql
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC)
) ENGINE=InnoDB;
```

### Friends テーブル

```sql
CREATE TABLE friends (
    user1_id BIGINT NOT NULL,
    user2_id BIGINT NOT NULL,
    status ENUM('pending', 'accepted') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user1_id, user2_id),
    INDEX idx_user1_id (user1_id),
    INDEX idx_user2_id (user2_id)
) ENGINE=InnoDB;
```

## 5. API設計

### ニュースフィード取得

```
GET /api/v1/feed?limit=20&cursor=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "posts": [...],
  "next_cursor": "1234567891"
}
```

## 6. スケーラビリティ設計

### グラフデータベース

- **Neo4j**: ソーシャルグラフの管理
- **カスタムグラフDB**: 大規模グラフの処理

### ニュースフィード生成

- **事前計算**: ニュースフィードを事前計算してキャッシュ
- **リアルタイム更新**: 新しい投稿でリアルタイム更新

## 7. レイテンシ最適化

### ニュースフィードの最適化

- **キャッシング**: ニュースフィードを積極的にキャッシュ
- **CDN**: 静的コンテンツをCDNで配信

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$10,000,000/月**
- **データベース**: 約 **$5,000,000/月**
- **ストレージ**: 約 **$3,000,000/月**
- **CDN**: 約 **$8,000,000/月**
- **合計**: 約 **$26,000,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにデプロイ
- **データベースレプリケーション**: 読み取りレプリカを配置

## 10. セキュリティ

### セキュリティ対策

- **認証**: OAuth 2.0 / JWT
- **プライバシー設定**: 投稿の公開範囲設定

## 11. UX最適化

### パフォーマンス指標

- **ニュースフィード読み込み**: < 1秒
- **投稿作成**: < 500ms

## 12. 実装例

### ニュースフィードサービス（疑似コード）

```python
class NewsFeedService:
    def __init__(self, graph_db, cache):
        self.graph_db = graph_db
        self.cache = cache
    
    async def get_feed(self, user_id: int, limit: int = 20):
        # キャッシュから取得を試みる
        cache_key = f"feed:{user_id}"
        cached_feed = await self.cache.get(cache_key)
        
        if cached_feed:
            return cached_feed
        
        # 友達を取得
        friends = await self.graph_db.get_friends(user_id)
        
        # 友達の投稿を取得
        posts = await self.db.get_posts_by_users(
            user_ids=[f["user_id"] for f in friends],
            limit=limit
        )
        
        # アルゴリズムでランキング
        ranked_posts = await self.rank_posts(posts, user_id)
        
        # キャッシュに保存
        await self.cache.set(cache_key, ranked_posts, ttl=300)
        
        return ranked_posts
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日のニュースフィード読み込み**: 200億回
- **1秒あたり**: 約23万回/秒（平均）
- **ピーク時**: 約70万回/秒

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **グラフデータベース**: ソーシャルグラフの効率的な管理
2. **事前計算**: ニュースフィードを事前計算
3. **キャッシング**: 積極的なキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Twitter](twitter_design.md) - マイクロブログプラットフォーム
- [Instagram](instagram_design.md) - 写真共有プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Airbnb](airbnb_design.md)でマーケットプレイスの設計を学ぶ

