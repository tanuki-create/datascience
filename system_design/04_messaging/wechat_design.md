# WeChat システム設計

## 1. システム概要

### 目的と主要機能

WeChatは、中国で最も人気のあるメッセージングアプリです。テキストメッセージ、音声メッセージ、ビデオ通話、モーメンツ（友達の動き）、決済、ミニプログラムなどの機能を統合したプラットフォームです。

**主要機能**:
- 1対1メッセージング
- グループチャット
- 音声・ビデオ通話
- モーメンツ（友達の動き）
- WeChat Pay（決済）
- ミニプログラム
- 公式アカウント

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約13億人
- **日間アクティブユーザー（DAU）**: 約10億人
- **1日のメッセージ数**: 約450億メッセージ
- **1秒あたりのメッセージ数**: 約50,000メッセージ/秒（ピーク時）

### 主要なユースケース

1. **メッセージ送信**: ユーザーがメッセージを送信
2. **グループチャット**: 複数ユーザーでのチャット
3. **音声・ビデオ通話**: リアルタイム通話
4. **モーメンツ**: 友達の動きを共有
5. **決済**: WeChat Payでの決済

## 2. 機能要件

### コア機能

1. **メッセージング**
   - テキストメッセージ
   - 画像・動画メッセージ
   - 音声メッセージ
   - ファイル送信

2. **リアルタイム通信**
   - WebSocket経由のリアルタイムメッセージ配信
   - 音声・ビデオ通話（WebRTC）

3. **グループチャット**
   - グループの作成・管理
   - グループメッセージの配信

4. **モーメンツ**
   - 写真・動画の投稿
   - 友達のモーメンツ閲覧

5. **決済**
   - WeChat Pay統合

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: メッセージは最終的に一貫性を保つ
- **パフォーマンス**:
  - メッセージ送信: < 100ms
  - メッセージ配信: < 500ms
  - 音声・ビデオ通話開始: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: メッセージは永続的に保存

### 優先順位付け

1. **P0（必須）**: メッセージング、グループチャット、リアルタイム通信
2. **P1（重要）**: モーメンツ、決済
3. **P2（望ましい）**: ミニプログラム、公式アカウント

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps)
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
│  │ Message  │  │  Group   │  │  Call    │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      WebSocket Manager               │         │
│  │      Moments Service                 │         │
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
│         Object Storage (S3)                       │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Message Service**: メッセージの処理
   - **Group Service**: グループチャットの管理
   - **Call Service**: 音声・ビデオ通話の管理
   - **WebSocket Manager**: WebSocket接続の管理
   - **Moments Service**: モーメンツの管理
4. **Database**: メッセージ、ユーザー、グループの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（メッセージ配信など）
7. **Object Storage**: メディアファイルの保存
8. **CDN**: メディアファイルの配信

### データフロー

#### メッセージ送信のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Message Service
3. Message Service:
   a. メッセージを検証
   b. データベースに保存
   c. Message Queueに送信
   d. 受信者のWebSocket接続を確認
4. WebSocket Manager:
   a. Message Queueからメッセージを受信
   b. 受信者がオンラインの場合、WebSocket経由で即座に配信
   c. 受信者がオフラインの場合、プッシュ通知を送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Messages テーブル

```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT,
    group_id BIGINT,
    message_type ENUM('text', 'image', 'video', 'audio', 'file') NOT NULL,
    content TEXT,
    media_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    INDEX idx_sender_receiver_created (sender_id, receiver_id, created_at DESC),
    INDEX idx_group_created (group_id, created_at DESC)
) ENGINE=InnoDB;
```

#### Groups テーブル

```sql
CREATE TABLE groups (
    group_id BIGINT PRIMARY KEY,
    group_name VARCHAR(200),
    owner_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    INDEX idx_owner_id (owner_id)
) ENGINE=InnoDB;
```

#### Group_Members テーブル

```sql
CREATE TABLE group_members (
    group_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role ENUM('owner', 'admin', 'member') DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: メッセージ、ユーザー、グループの永続化
- **NoSQL（Cassandra）**:
  - 理由: メッセージの書き込み負荷が高い、水平スケーリングが必要
  - 用途: メッセージの保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `messages`テーブルは`sender_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: メッセージは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### メッセージ送信

```
POST /api/v1/messages
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "receiver_id": 987654321,
  "message_type": "text",
  "content": "Hello, WeChat!"
}

Response (200 OK):
{
  "message_id": 1234567890,
  "status": "sent",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### メッセージ取得

```
GET /api/v1/messages?receiver_id=987654321&limit=20&cursor=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "messages": [...],
  "next_cursor": "1234567891"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のメッセージのみアクセス可能
- **レート制限**: 
  - メッセージ送信: 100メッセージ/分
  - メッセージ取得: 30リクエスト/分

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
- メッセージは`sender_id`でシャーディング
- グループは`owner_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: メディアファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ユーザー情報、グループ情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: メディアファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メッセージ配信**: WebSocket接続の管理
2. **メディアファイル**: 大きなファイルサイズ
3. **グループメッセージ**: 複数ユーザーへの配信

### CDNの活用

- **メディアファイル**: CloudflareまたはAWS CloudFront
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
   Partition Key: receiver_id
   ```

2. **プッシュ通知**:
   - オフラインユーザーへのプッシュ通知を非同期で送信

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 13億人
- **日間アクティブユーザー**: 10億人
- **1日のメッセージ数**: 450億メッセージ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 3,000台（リージョン間で分散）
- コスト: $0.192/時間 × 3,000台 × 730時間 = **$420,480/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 150台（マスター + レプリカ）
- コスト: $0.76/時間 × 150台 × 730時間 = **$83,220/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 300台
- コスト: $0.175/時間 × 300台 × 730時間 = **$38,325/月**

**ストレージ（S3）**:
- メッセージストレージ: 10 PB
- コスト: $0.023/GB/月 × 10,000,000 GB = **$230,000/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.09/GB × 10,000,000 GB = **$900,000/月**

**合計**: 約 **$1,672,025/月**（約20,064,300ドル/年）

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

2. **メッセージバックアップ**:
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
   - ユーザーは自分のメッセージのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - メッセージ: エンドツーエンド暗号化（オプション）

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
- **メッセージ送信**: < 100ms
- **メッセージ配信**: < 500ms

### プログレッシブローディング

1. **メッセージの遅延読み込み**:
   - 最新のメッセージを先に読み込み
   - 過去のメッセージはスクロール時に読み込み

2. **メディアファイルの遅延読み込み**:
   - ビューポートに入るまでメディアを読み込まない
   - サムネイルを先に表示

## 12. 実装例

### メッセージサービス（疑似コード）

```python
class MessageService:
    def __init__(self, db, cache, message_queue, websocket_manager):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.websocket_manager = websocket_manager
    
    async def send_message(self, sender_id: int, receiver_id: int, message_type: str, content: str):
        # メッセージを保存
        message_id = await self.db.insert_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="messages",
            message={
                "message_id": message_id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message_type": message_type,
                "content": content
            },
            partition_key=receiver_id
        )
        
        return {
            "message_id": message_id,
            "status": "sent"
        }
    
    async def handle_message_delivery(self, message):
        # 受信者のオンラインステータスを確認
        is_online = await self.cache.get(f"user:{message['receiver_id']}:online")
        
        if is_online:
            # WebSocket経由で即座に配信
            await self.websocket_manager.send_to_user(
                user_id=message['receiver_id'],
                data=message
            )
        else:
            # プッシュ通知を送信
            await self.send_push_notification(
                user_id=message['receiver_id'],
                message=message
            )
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のメッセージ取得**: 100億回
- **1時間あたり**: 100億 / 24 = 約4.17億回
- **1秒あたり**: 4.17億 / 3600 = 約115,833回/秒
- **ピーク時（3倍）**: 約347,499回/秒

#### 書き込みトラフィック

- **1日のメッセージ数**: 450億メッセージ
- **1時間あたり**: 450億 / 24 = 約18.75億メッセージ
- **1秒あたり**: 18.75億 / 3600 = 約520,833メッセージ/秒
- **ピーク時（3倍）**: 約1,562,499メッセージ/秒

### ストレージ見積もり

#### メッセージストレージ

- **1メッセージあたりのサイズ**: 約500バイト（テキストメッセージ）
- **1日のメッセージ数**: 450億メッセージ
- **1日のストレージ**: 450億 × 500バイト = 225 GB
- **1年のストレージ**: 225 GB × 365 = 約82.125 TB
- **5年のストレージ**: 約410.625 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **WebSocket**: リアルタイム通信にWebSocketを使用
4. **キャッシュファースト**: 可能な限りキャッシュを活用
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **WebSocket接続の管理**:
   - 問題: 大量のWebSocket接続の管理が困難
   - 解決策: 接続プールと適切な負荷分散

2. **メッセージ配信のスケーラビリティ**:
   - 問題: 大規模グループでのメッセージ配信が困難
   - 解決策: メッセージキューとバッチ処理

## 15. 関連システム

### 類似システムへのリンク

- [WhatsApp](whatsapp_design.md) - メッセージングアプリ
- [Telegram](telegram_design.md) - メッセージングアプリ
- [Slack](slack_design.md) - ビジネス向けメッセージング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Telegram](telegram_design.md)でセキュアなメッセージングアプリの設計を学ぶ

