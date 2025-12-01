# Slack システム設計

## 1. システム概要

### 目的と主要機能

Slackは、企業向けのチームコラボレーションプラットフォームです。チャンネルベースのメッセージング、ファイル共有、統合機能を提供します。

**主要機能**:
- チャンネルベースのメッセージング
- ダイレクトメッセージ（DM）
- ファイル共有
- スレッド機能
- アプリ統合（Bot、Webhook）
- 検索機能
- 音声・ビデオ通話

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3,300万人
- **日間アクティブユーザー（DAU）**: 約1,200万人
- **1日のメッセージ数**: 約10億メッセージ
- **1秒あたりのメッセージ数**: 約10,000メッセージ/秒（ピーク時）

### 主要なユースケース

1. **チャンネルメッセージ**: チームチャンネルでのメッセージ送信
2. **ダイレクトメッセージ**: 1対1のメッセージング
3. **ファイル共有**: ファイルのアップロード・共有
4. **検索**: 過去のメッセージやファイルの検索
5. **統合**: サードパーティアプリとの統合

## 2. 機能要件

### コア機能

1. **メッセージング**
   - チャンネルメッセージ
   - ダイレクトメッセージ
   - スレッド機能
   - リアクション（絵文字）

2. **ファイル管理**
   - ファイルのアップロード
   - ファイルの共有
   - ファイルの検索

3. **検索**
   - メッセージ検索
   - ファイル検索
   - 全文検索

4. **統合**
   - Bot API
   - Webhook
   - サードパーティアプリ統合

5. **通知**
   - リアルタイム通知
   - メンション通知
   - カスタム通知設定

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: メッセージは最終的に一貫性を保つ
- **パフォーマンス**:
  - メッセージ送信: < 200ms
  - メッセージ配信: < 500ms
  - 検索: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: メッセージとファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: チャンネルメッセージング、ダイレクトメッセージ、検索
2. **P1（重要）**: ファイル共有、統合、通知
3. **P2（望ましい）**: 音声・ビデオ通話、高度な検索

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps, Desktop)
└──────┬──────┘
       │ HTTPS/WebSocket
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
│  │ Message  │  │  File    │  │  Search  │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Channel Service                │         │
│  │      Integration Service            │         │
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
│         Object Storage (S3)                       │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Message Service**: メッセージの処理
   - **File Service**: ファイルの管理
   - **Search Service**: 検索機能
   - **Channel Service**: チャンネルの管理
   - **Integration Service**: 統合機能の管理
4. **Database**: メッセージ、ユーザー、チャンネルの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（メッセージ配信、検索インデックス更新など）
7. **Search Index**: メッセージとファイルの検索インデックス
8. **Object Storage**: ファイルの保存
9. **CDN**: ファイルの配信

### データフロー

#### チャンネルメッセージ送信のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Message Service
3. Message Service:
   a. メッセージを検証
   b. データベースに保存
   c. Message Queueに送信
   d. Search Serviceに検索インデックス更新を依頼
4. Message Service:
   a. Message Queueからメッセージを受信
   b. チャンネルメンバーに配信
   c. 通知サービスに通知を送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Workspaces テーブル

```sql
CREATE TABLE workspaces (
    workspace_id BIGINT PRIMARY KEY,
    workspace_name VARCHAR(200) NOT NULL,
    domain VARCHAR(200) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_domain (domain)
) ENGINE=InnoDB;
```

#### Channels テーブル

```sql
CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    workspace_id BIGINT NOT NULL,
    channel_name VARCHAR(200) NOT NULL,
    channel_type ENUM('public', 'private', 'dm') NOT NULL,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    INDEX idx_workspace_id (workspace_id),
    INDEX idx_channel_type (channel_type)
) ENGINE=InnoDB;
```

#### Messages テーブル

```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    channel_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    thread_ts BIGINT,
    message_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_channel_created (channel_id, created_at DESC),
    INDEX idx_thread_ts (thread_ts),
    FULLTEXT INDEX idx_message_text (message_text)
) ENGINE=InnoDB;
```

#### Files テーブル

```sql
CREATE TABLE files (
    file_id BIGINT PRIMARY KEY,
    workspace_id BIGINT NOT NULL,
    channel_id BIGINT,
    user_id BIGINT NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_size BIGINT,
    file_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_workspace_id (workspace_id),
    INDEX idx_channel_id (channel_id),
    FULLTEXT INDEX idx_file_name (file_name)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: メッセージ、ユーザー、チャンネルの永続化
- **Elasticsearch**:
  - 理由: 全文検索、メッセージ検索、ファイル検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `messages`テーブルは`workspace_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: メッセージは時系列で保存
4. **全文検索**: Elasticsearchで全文検索を実装

## 5. API設計

### 主要なAPIエンドポイント

#### メッセージ送信

```
POST /api/v1/channels/{channel_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "text": "Hello, Slack!",
  "thread_ts": null
}

Response (200 OK):
{
  "message_id": 1234567890,
  "channel_id": 987654321,
  "user_id": 111222333,
  "text": "Hello, Slack!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### メッセージ検索

```
GET /api/v1/search/messages?q=hello&workspace_id=123&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "messages": [...],
  "total_results": 1000
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のワークスペースのメッセージのみアクセス可能
- **レート制限**: 
  - メッセージ送信: 20メッセージ/分
  - 検索: 20リクエスト/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Workspace IDベースのシャーディング

```
Shard 1: workspace_id % 4 == 0
Shard 2: workspace_id % 4 == 1
Shard 3: workspace_id % 4 == 2
Shard 4: workspace_id % 4 == 3
```

**シャーディングキー**: `workspace_id`
- メッセージは`workspace_id`でシャーディング
- チャンネルは`workspace_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ユーザー情報、チャンネル情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メッセージ配信**: チャンネルメンバーへの配信
2. **検索**: Elasticsearchクエリの最適化
3. **ファイル転送**: 大きなファイルサイズ

### CDNの活用

- **ファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### メッセージ配信最適化

1. **WebSocket**: リアルタイム双方向通信
2. **メッセージキュー**: Kafkaでメッセージを配信
3. **バッチ処理**: 複数のメッセージをバッチで配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **メッセージ配信**:
   ```
   Topic: messages
   Partition Key: channel_id
   ```

2. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: workspace_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3,300万人
- **日間アクティブユーザー**: 1,200万人
- **1日のメッセージ数**: 10億メッセージ

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

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ（S3）**:
- ファイルストレージ: 2 PB
- コスト: $0.023/GB/月 × 2,000,000 GB = **$46,000/月**

**ネットワーク**:
- データ転送: 1 PB/月
- コスト: $0.09/GB × 1,000,000 GB = **$90,000/月**

**合計**: 約 **$240,207.50/月**（約2,882,490ドル/年）

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
   - WebSocket接続のヘルスチェック

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

2. **ファイルバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - SSO（Single Sign-On）サポート
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ワークスペースベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - ファイル: S3サーバーサイド暗号化

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
- **メッセージ送信**: < 200ms
- **メッセージ配信**: < 500ms
- **検索**: < 1秒

### プログレッシブローディング

1. **メッセージの遅延読み込み**:
   - 最新のメッセージを先に読み込み
   - 過去のメッセージはスクロール時に読み込み

2. **ファイルの遅延読み込み**:
   - ビューポートに入るまでファイルを読み込まない
   - サムネイルを先に表示

## 12. 実装例

### メッセージサービス（疑似コード）

```python
class MessageService:
    def __init__(self, db, cache, message_queue, search_service):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.search_service = search_service
    
    async def send_message(self, channel_id: int, user_id: int, text: str, thread_ts: int = None):
        # メッセージを保存
        message_id = await self.db.insert_message(
            channel_id=channel_id,
            user_id=user_id,
            text=text,
            thread_ts=thread_ts
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="messages",
            message={
                "message_id": message_id,
                "channel_id": channel_id,
                "user_id": user_id,
                "text": text,
                "thread_ts": thread_ts
            },
            partition_key=channel_id
        )
        
        # 検索インデックス更新を非同期で実行
        await self.search_service.update_index(
            message_id=message_id,
            text=text,
            channel_id=channel_id
        )
        
        return {
            "message_id": message_id,
            "status": "sent"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のメッセージ取得**: 20億回
- **1時間あたり**: 20億 / 24 = 約8,333万回
- **1秒あたり**: 8,333万 / 3600 = 約23,148回/秒
- **ピーク時（3倍）**: 約69,444回/秒

#### 書き込みトラフィック

- **1日のメッセージ数**: 10億メッセージ
- **1時間あたり**: 10億 / 24 = 約4,167万メッセージ
- **1秒あたり**: 4,167万 / 3600 = 約11,575メッセージ/秒
- **ピーク時（3倍）**: 約34,725メッセージ/秒

### ストレージ見積もり

#### メッセージストレージ

- **1メッセージあたりのサイズ**: 約1 KB（メタデータ含む）
- **1日のメッセージ数**: 10億メッセージ
- **1日のストレージ**: 10億 × 1 KB = 1 TB
- **1年のストレージ**: 1 TB × 365 = 約365 TB
- **5年のストレージ**: 約1.825 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **WebSocket**: リアルタイム通信にWebSocketを使用
4. **検索**: Elasticsearchで全文検索を実装
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **チャンネルメッセージ配信のスケーラビリティ**:
   - 問題: 大規模チャンネルでのメッセージ配信が困難
   - 解決策: メッセージキューとバッチ処理

2. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Discord](discord_design.md) - コミュニティ向けメッセージング
- [Telegram](telegram_design.md) - メッセージングアプリ
- [Microsoft Teams](../15_realtime_systems/zoom_design.md) - ビジネス向けコラボレーション

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Discord](discord_design.md)でコミュニティ向けメッセージングプラットフォームの設計を学ぶ

