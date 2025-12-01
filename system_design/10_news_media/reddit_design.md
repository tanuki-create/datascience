# Reddit システム設計

## 1. システム概要

### 目的と主要機能

Redditは、ユーザーがコンテンツを投稿、閲覧、議論するソーシャルニュースアグリゲーションプラットフォームです。

**主要機能**:
- サブレディット（コミュニティ）での投稿
- 投票システム（アップボート・ダウンボート）
- コメントスレッド
- ランキングアルゴリズム
- 検索機能

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日の投稿数**: 約500万投稿
- **1日のコメント数**: 約5,000万コメント
- **サブレディット数**: 約10万

## 2. 機能要件

### コア機能

1. **投稿システム**
   - テキスト、リンク、画像の投稿
   - サブレディットへの投稿

2. **投票システム**
   - アップボート・ダウンボート
   - スコアの計算

3. **コメントスレッド**
   - ネストされたコメント構造
   - コメントの投票

4. **ランキング**
   - ホット、トップ、新着のランキング
   - 時間減衰アルゴリズム

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 投稿読み込み: < 1秒
  - 投票処理: < 100ms
- **スケーラビリティ**: 水平スケーリング可能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
Post Service → Database → Cache
Vote Service → Database → Cache → Message Queue
Comment Service → Database → Cache
Ranking Service → Database → Cache
```

## 4. データモデル設計

### Posts テーブル

```sql
CREATE TABLE posts (
    post_id BIGINT PRIMARY KEY,
    subreddit_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    post_type ENUM('text', 'link', 'image') NOT NULL,
    upvotes INT DEFAULT 0,
    downvotes INT DEFAULT 0,
    score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subreddit_id) REFERENCES subreddits(subreddit_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_subreddit_id_created_at (subreddit_id, created_at DESC),
    INDEX idx_score (score DESC)
) ENGINE=InnoDB;
```

### Votes テーブル

```sql
CREATE TABLE votes (
    vote_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    post_id BIGINT,
    comment_id BIGINT,
    vote_type ENUM('upvote', 'downvote') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
    UNIQUE KEY idx_user_post (user_id, post_id),
    UNIQUE KEY idx_user_comment (user_id, comment_id)
) ENGINE=InnoDB;
```

## 5. API設計

### 投稿取得

```
GET /api/v1/r/{subreddit}/hot?limit=25
Authorization: Bearer <token>

Response (200 OK):
{
  "posts": [
    {
      "post_id": 1234567890,
      "title": "Post Title",
      "score": 1000,
      "upvotes": 1200,
      "downvotes": 200
    }
  ]
}
```

### 投票

```
POST /api/v1/posts/{post_id}/vote
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "vote_type": "upvote"
}

Response (200 OK):
{
  "post_id": 1234567890,
  "new_score": 1001
}
```

## 6. スケーラビリティ設計

### 投票システムのスケーリング

- **非同期処理**: 投票を非同期で処理
- **バッチ更新**: スコアをバッチで更新
- **キャッシング**: スコアをキャッシュ

### ランキングのスケーリング

- **事前計算**: ランキングを事前計算してキャッシュ
- **時間減衰**: 時間に基づくスコアの減衰

## 7. レイテンシ最適化

### ランキングの最適化

- **キャッシング**: ホット、トップのランキングをキャッシュ
- **事前計算**: ランキングを事前計算

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$1,000,000/月**
- **データベース**: 約 **$500,000/月**
- **ストレージ**: 約 **$200,000/月**
- **合計**: 約 **$1,700,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチAZ**: 複数のアベイラビリティゾーンにデプロイ
- **データベースレプリケーション**: 読み取りレプリカを配置

## 10. セキュリティ

### セキュリティ対策

- **認証**: OAuth 2.0 / JWT
- **投票の重複防止**: 1ユーザー1投票

## 11. UX最適化

### パフォーマンス指標

- **投稿読み込み**: < 1秒
- **投票処理**: < 100ms
- **コメント読み込み**: < 500ms

## 12. 実装例

### 投票サービス（疑似コード）

```python
class VoteService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def vote(self, user_id: int, post_id: int, vote_type: str):
        # 既存の投票を確認
        existing_vote = await self.db.get_vote(user_id, post_id)
        
        if existing_vote:
            if existing_vote["vote_type"] == vote_type:
                # 同じ投票は取り消し
                await self.db.delete_vote(existing_vote["vote_id"])
                vote_change = -1 if vote_type == "upvote" else 1
            else:
                # 投票を変更
                await self.db.update_vote(existing_vote["vote_id"], vote_type)
                vote_change = 2 if vote_type == "upvote" else -2
        else:
            # 新しい投票
            await self.db.create_vote(user_id, post_id, vote_type)
            vote_change = 1 if vote_type == "upvote" else -1
        
        # スコア更新をキューに送信
        await self.message_queue.publish(
            topic="score-update",
            message={
                "post_id": post_id,
                "vote_change": vote_change
            }
        )
        
        return {"post_id": post_id, "vote_change": vote_change}
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の投票数**: 約10億回
- **1秒あたり**: 約11,574回/秒（平均）
- **ピーク時**: 約35,000回/秒

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **非同期処理**: 投票とスコア更新を非同期で処理
2. **キャッシング**: ランキングを積極的にキャッシュ
3. **時間減衰**: 時間に基づくスコアの減衰

## 15. 関連システム

### 類似システムへのリンク

- [Medium](medium_design.md) - ブログプラットフォーム
- [Quora](quora_design.md) - Q&Aプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [PayPal](paypal_design.md)で決済システムの設計を学ぶ

