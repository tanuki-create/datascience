# Quora システム設計

## 1. システム概要

### 目的と主要機能

Quoraは、ユーザーが質問を投稿し、他のユーザーが回答するQ&Aプラットフォームです。知識の共有とコミュニティ形成を促進します。

**主要機能**:
- 質問の投稿・編集
- 回答の投稿・編集
- 投票システム（アップボート・ダウンボート）
- フォロー機能
- トピック・タグ
- 検索機能
- レコメンデーション

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3億人
- **日間アクティブユーザー（DAU）**: 約1億人
- **1日の質問数**: 約50万質問
- **1日の回答数**: 約500万回答
- **1日の閲覧数**: 約10億回
- **1秒あたりのリクエスト数**: 約15,000リクエスト/秒（ピーク時）
- **質問総数**: 約4,000万質問

### 主要なユースケース

1. **質問投稿**: ユーザーが質問を投稿
2. **回答投稿**: ユーザーが質問に回答
3. **質問閲覧**: ユーザーが質問と回答を閲覧
4. **投票**: ユーザーが回答に投票
5. **フォロー**: ユーザーがトピックや質問をフォロー

## 2. 機能要件

### コア機能

1. **質問管理**
   - 質問の作成・編集・削除
   - 質問へのタグ付け
   - 質問の重複検出

2. **回答管理**
   - 回答の作成・編集・削除
   - 回答のフォーマット（マークダウン）
   - 回答の投票

3. **投票システム**
   - アップボート・ダウンボート
   - スコアの計算
   - 回答のランキング

4. **フォロー機能**
   - トピックのフォロー
   - 質問のフォロー
   - ユーザーのフォロー

5. **検索機能**
   - 質問検索
   - 回答検索
   - トピック検索

6. **レコメンデーション**
   - パーソナライズされた質問推薦
   - 関連質問の推薦

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 質問・回答は強い一貫性、投票は最終的に一貫性を保つ
- **パフォーマンス**:
  - 質問表示: < 2秒
  - 質問検索: < 1秒
  - 回答投稿: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 質問・回答は永続的に保存

### 優先順位付け

1. **P0（必須）**: 質問投稿・閲覧、回答投稿・閲覧、投票システム
2. **P1（重要）**: 検索、フォロー機能、レコメンデーション
3. **P2（望ましい）**: 重複検出、高度な検索

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
│  │ Question │  │  Answer  │  │  Vote    │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Search Service                  │         │
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
│         Search Index (Elasticsearch)              │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Question Service**: 質問の管理
   - **Answer Service**: 回答の管理
   - **Vote Service**: 投票の処理
   - **Search Service**: 検索機能の処理
   - **Recommendation Service**: レコメンデーションの処理
4. **Database**: 質問、回答、投票の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（検索インデックス更新など）
7. **Search Index**: 質問・回答検索インデックス
8. **CDN**: 画像の配信

### データフロー

#### 回答投稿のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Answer Service
3. Answer Service:
   a. 回答をデータベースに保存
   b. 質問の回答数を更新
   c. Message Queueに検索インデックス更新を依頼
   d. 質問フォロワーに通知を送信（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Questions テーブル

```sql
CREATE TABLE questions (
    question_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    view_count BIGINT DEFAULT 0,
    answer_count INT DEFAULT 0,
    follower_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_title_content (title, content)
) ENGINE=InnoDB;
```

#### Answers テーブル

```sql
CREATE TABLE answers (
    answer_id BIGINT PRIMARY KEY,
    question_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    upvote_count INT DEFAULT 0,
    downvote_count INT DEFAULT 0,
    score INT DEFAULT 0,
    is_accepted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_question_id_score (question_id, score DESC),
    INDEX idx_user_id (user_id),
    FULLTEXT INDEX idx_content (content)
) ENGINE=InnoDB;
```

#### Votes テーブル

```sql
CREATE TABLE votes (
    vote_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    answer_id BIGINT NOT NULL,
    vote_type ENUM('upvote', 'downvote') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_answer (user_id, answer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id),
    INDEX idx_answer_id (answer_id)
) ENGINE=InnoDB;
```

#### Question_Topics テーブル

```sql
CREATE TABLE question_topics (
    question_id BIGINT NOT NULL,
    topic_id BIGINT NOT NULL,
    PRIMARY KEY (question_id, topic_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id),
    INDEX idx_topic_id (topic_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 質問、回答、投票の永続化
- **Elasticsearch**:
  - 理由: 全文検索、質問・回答検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `questions`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 質問・回答は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 質問投稿

```
POST /api/v1/questions
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "How does machine learning work?",
  "content": "I want to understand the basics of machine learning.",
  "topics": ["machine-learning", "artificial-intelligence"]
}

Response (200 OK):
{
  "question_id": 1234567890,
  "title": "How does machine learning work?",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 回答投稿

```
POST /api/v1/questions/{question_id}/answers
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "content": "Machine learning is a subset of artificial intelligence..."
}

Response (200 OK):
{
  "answer_id": 9876543210,
  "question_id": 1234567890,
  "content": "Machine learning is a subset of artificial intelligence...",
  "created_at": "2024-01-15T10:35:00Z"
}
```

#### 投票

```
POST /api/v1/answers/{answer_id}/vote
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "vote_type": "upvote"
}

Response (200 OK):
{
  "answer_id": 9876543210,
  "upvote_count": 100,
  "downvote_count": 5,
  "score": 95
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の質問・回答のみ編集可能
- **レート制限**: 
  - 質問投稿: 10質問/日
  - 回答投稿: 50回答/日
  - 投票: 100回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- 質問は`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 画像をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 質問メタデータ、回答、人気質問
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **質問検索**: Elasticsearchクエリの最適化
2. **回答ランキング**: スコア計算の最適化
3. **レコメンデーション**: 機械学習モデルの推論

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 回答ランキング最適化

1. **事前計算**: 回答スコアを事前計算
2. **キャッシング**: 人気質問の回答をキャッシュ
3. **並列処理**: 複数の回答を並列で処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: question_id
   ```

2. **投票処理**:
   ```
   Topic: vote-updates
   Partition Key: answer_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3億人
- **日間アクティブユーザー**: 1億人
- **1日の質問数**: 50万質問
- **1日の回答数**: 500万回答
- **1日の閲覧数**: 10億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 800台（リージョン間で分散）
- コスト: $0.192/時間 × 800台 × 730時間 = **$112,128/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**ストレージ**:
- EBS: 200 TB
- コスト: $0.10/GB/月 × 200,000 GB = **$20,000/月**

**ネットワーク**:
- データ転送: 3 PB/月
- コスト: $0.09/GB × 3,000,000 GB = **$270,000/月**

**合計**: 約 **$459,287/月**（約5,511,444ドル/年）

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

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 1時間
   - RPO（Recovery Point Objective）: 15分

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - パスワードハッシュ: bcrypt（コストファクター12）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の質問・回答のみ編集可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム

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
- **質問表示**: < 2秒
- **質問検索**: < 1秒

### プログレッシブローディング

1. **回答の遅延読み込み**:
   - 最初の10件の回答を先に表示
   - 残りの回答はスクロール時に読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - サムネイルを先に表示

## 12. 実装例

### 投票サービス（疑似コード）

```python
class VoteService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def vote_answer(self, user_id: int, answer_id: int, vote_type: str):
        # 既存の投票を確認
        existing_vote = await self.db.get_vote(user_id=user_id, answer_id=answer_id)
        
        if existing_vote:
            if existing_vote['vote_type'] == vote_type:
                # 同じ投票の場合は削除
                await self.db.delete_vote(user_id=user_id, answer_id=answer_id)
                vote_change = -1 if vote_type == 'upvote' else 1
            else:
                # 異なる投票の場合は更新
                await self.db.update_vote(user_id=user_id, answer_id=answer_id, vote_type=vote_type)
                vote_change = 2 if vote_type == 'upvote' else -2
        else:
            # 新しい投票を作成
            await self.db.insert_vote(user_id=user_id, answer_id=answer_id, vote_type=vote_type)
            vote_change = 1 if vote_type == 'upvote' else -1
        
        # 回答のスコアを更新
        await self.db.update_answer_score(
            answer_id=answer_id,
            vote_change=vote_change
        )
        
        # 投票更新を非同期で処理
        await self.message_queue.publish(
            topic="vote-updates",
            message={
                "answer_id": answer_id,
                "vote_type": vote_type,
                "vote_change": vote_change
            },
            partition_key=answer_id
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"answer:{answer_id}")
        
        return {
            "answer_id": answer_id,
            "vote_type": vote_type,
            "status": "voted"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の閲覧数**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の回答数**: 500万回答
- **1時間あたり**: 500万 / 24 = 約20.8万回答
- **1秒あたり**: 20.8万 / 3600 = 約58回答/秒
- **ピーク時（3倍）**: 約174回答/秒

### ストレージ見積もり

#### 質問・回答ストレージ

- **1質問あたりの平均サイズ**: 約2 KB
- **1回答あたりの平均サイズ**: 約5 KB
- **質問総数**: 4,000万質問
- **回答総数**: 約40億回答
- **合計ストレージ**: (4,000万 × 2 KB) + (40億 × 5 KB) = 約20 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **全文検索**: Elasticsearchで全文検索を実装
4. **投票システム**: リアルタイム投票処理の実装
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **投票の競合**:
   - 問題: 同時投票でスコアの競合が発生
   - 解決策: 楽観的ロックとトランザクション

2. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Reddit](reddit_design.md) - ソーシャルニュースプラットフォーム
- [Medium](medium_design.md) - 長文コンテンツプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [共通パターン](../17_common_patterns/load_balancing.md)でシステム設計の共通パターンを学ぶ

