# Discord システム設計

## 1. システム概要

### 目的と主要機能

Discordは、ゲーマーやコミュニティ向けのボイス・テキストチャットプラットフォームです。サーバー、チャンネル、ボイスチャット、スクリーン共有などの機能を提供します。

**主要機能**:
- サーバー（コミュニティ）管理
- テキストチャンネル
- ボイスチャンネル
- ビデオチャット
- スクリーン共有
- ファイル共有
- ボット（Bot API）
- リアクション（絵文字）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5億人
- **日間アクティブユーザー（DAU）**: 約1.5億人
- **1日のメッセージ数**: 約150億メッセージ
- **1秒あたりのメッセージ数**: 約20,000メッセージ/秒（ピーク時）
- **同時ボイスチャットユーザー**: 約1,000万人（ピーク時）

### 主要なユースケース

1. **テキストチャット**: サーバーやチャンネルでのメッセージ送信
2. **ボイスチャット**: リアルタイム音声通話
3. **ビデオチャット**: リアルタイムビデオ通話
4. **スクリーン共有**: 画面の共有
5. **ファイル共有**: ファイルのアップロード・共有

## 2. 機能要件

### コア機能

1. **メッセージング**
   - テキストメッセージ
   - 画像・動画メッセージ
   - ファイル送信
   - リアクション（絵文字）

2. **ボイス・ビデオチャット**
   - リアルタイム音声通話
   - リアルタイムビデオ通話
   - スクリーン共有
   - 低レイテンシ通信

3. **サーバー管理**
   - サーバーの作成・管理
   - チャンネルの作成・管理
   - ロール・権限管理

4. **ボット**
   - Bot API
   - 自動応答機能
   - カスタムコマンド

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: メッセージは最終的に一貫性を保つ
- **パフォーマンス**:
  - メッセージ送信: < 100ms
  - メッセージ配信: < 500ms
  - ボイスチャット開始: < 2秒
  - ボイスチャットレイテンシ: < 100ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: メッセージとファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: テキストチャット、ボイスチャット、サーバー管理
2. **P1（重要）**: ビデオチャット、ファイル共有、ボット
3. **P2（望ましい）**: スクリーン共有、高度な権限管理

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Desktop, Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS/WebSocket/WebRTC
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
│  │ Message  │  │  Voice   │  │  Server  │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      WebSocket Manager               │         │
│  │      WebRTC Manager                  │         │
│  │      Bot Service                     │         │
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
│         Media Servers (WebRTC)                    │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Message Service**: メッセージの処理
   - **Voice Service**: ボイスチャットの管理
   - **Server Service**: サーバーの管理
   - **WebSocket Manager**: WebSocket接続の管理
   - **WebRTC Manager**: WebRTC接続の管理
   - **Bot Service**: ボットの管理
4. **Database**: メッセージ、ユーザー、サーバーの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（メッセージ配信など）
7. **Object Storage**: ファイルの保存
8. **CDN**: ファイルの配信
9. **Media Servers**: WebRTC用のメディアサーバー

### データフロー

#### メッセージ送信のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Message Service
3. Message Service:
   a. メッセージを検証
   b. データベースに保存
   c. Message Queueに送信
   d. チャンネルメンバーを取得
4. WebSocket Manager:
   a. Message Queueからメッセージを受信
   b. チャンネルメンバーにWebSocket経由で配信
```

#### ボイスチャット開始のフロー

```
1. Client → API Gateway → Voice Service
2. Voice Service:
   a. WebRTC接続を確立
   b. Media Serverを割り当て
   c. 他の参加者に通知
3. WebRTC Manager:
   a. メディアストリームを管理
   b. 低レイテンシで配信
```

## 4. データモデル設計

### 主要なエンティティ

#### Servers テーブル

```sql
CREATE TABLE servers (
    server_id BIGINT PRIMARY KEY,
    server_name VARCHAR(200) NOT NULL,
    owner_id BIGINT NOT NULL,
    icon_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    INDEX idx_owner_id (owner_id)
) ENGINE=InnoDB;
```

#### Channels テーブル

```sql
CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    server_id BIGINT NOT NULL,
    channel_name VARCHAR(200) NOT NULL,
    channel_type ENUM('text', 'voice', 'video') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (server_id) REFERENCES servers(server_id),
    INDEX idx_server_id (server_id),
    INDEX idx_channel_type (channel_type)
) ENGINE=InnoDB;
```

#### Messages テーブル

```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    channel_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    message_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_channel_created (channel_id, created_at DESC),
    FULLTEXT INDEX idx_message_text (message_text)
) ENGINE=InnoDB;
```

#### Server_Members テーブル

```sql
CREATE TABLE server_members (
    server_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role_id BIGINT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (server_id, user_id),
    FOREIGN KEY (server_id) REFERENCES servers(server_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: メッセージ、ユーザー、サーバーの永続化
- **NoSQL（Cassandra）**:
  - 理由: メッセージの書き込み負荷が高い、水平スケーリングが必要
  - 用途: メッセージの保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `messages`テーブルは`server_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: メッセージは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### メッセージ送信

```
POST /api/v1/channels/{channel_id}/messages
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "content": "Hello, Discord!"
}

Response (200 OK):
{
  "message_id": 1234567890,
  "channel_id": 987654321,
  "user_id": 111222333,
  "content": "Hello, Discord!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### ボイスチャット参加

```
POST /api/v1/channels/{channel_id}/voice/join
Authorization: Bearer <token>

Response (200 OK):
{
  "voice_token": "abc123",
  "endpoint": "wss://voice.discord.com",
  "session_id": "xyz789"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは参加しているサーバーのメッセージのみアクセス可能
- **レート制限**: 
  - メッセージ送信: 5メッセージ/5秒
  - ボイスチャット参加: 10回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Server IDベースのシャーディング

```
Shard 1: server_id % 8 == 0
Shard 2: server_id % 8 == 1
...
Shard 8: server_id % 8 == 7
```

**シャーディングキー**: `server_id`
- メッセージは`server_id`でシャーディング
- チャンネルは`server_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **Media Servers**: WebRTC用のメディアサーバーを追加

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
   - 用途: ユーザー情報、サーバー情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メッセージ配信**: チャンネルメンバーへの配信
2. **ボイスチャット**: WebRTC接続のレイテンシ
3. **ファイル転送**: 大きなファイルサイズ

### CDNの活用

- **ファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ボイスチャット最適化

1. **WebRTC**: 低レイテンシのリアルタイム通信
2. **Media Servers**: 地理的に分散したメディアサーバー
3. **適応的ビットレート**: ネットワーク状況に応じてビットレートを調整

### 非同期処理

#### メッセージキュー（Kafka）

1. **メッセージ配信**:
   ```
   Topic: messages
   Partition Key: channel_id
   ```

2. **ボイスチャット通知**:
   ```
   Topic: voice-events
   Partition Key: channel_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 5億人
- **日間アクティブユーザー**: 1.5億人
- **1日のメッセージ数**: 150億メッセージ
- **同時ボイスチャットユーザー**: 1,000万人（ピーク時）

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**Media Servers（WebRTC）**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 500台
- コスト: $0.34/時間 × 500台 × 730時間 = **$124,100/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 60台（マスター + レプリカ）
- コスト: $0.76/時間 × 60台 × 730時間 = **$33,288/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**ストレージ（S3）**:
- ファイルストレージ: 5 PB
- コスト: $0.023/GB/月 × 5,000,000 GB = **$115,000/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.09/GB × 10,000,000 GB = **$900,000/月**

**合計**: 約 **$1,325,323/月**（約15,903,876ドル/年）

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
   - Media Serversのヘルスチェック

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
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - サーバーベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3、WebRTC（DTLS）
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
- **メッセージ送信**: < 100ms
- **メッセージ配信**: < 500ms
- **ボイスチャットレイテンシ**: < 100ms

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
    def __init__(self, db, cache, message_queue, websocket_manager):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.websocket_manager = websocket_manager
    
    async def send_message(self, channel_id: int, user_id: int, content: str):
        # メッセージを保存
        message_id = await self.db.insert_message(
            channel_id=channel_id,
            user_id=user_id,
            message_text=content
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="messages",
            message={
                "message_id": message_id,
                "channel_id": channel_id,
                "user_id": user_id,
                "content": content
            },
            partition_key=channel_id
        )
        
        return {
            "message_id": message_id,
            "status": "sent"
        }
    
    async def handle_message_delivery(self, message):
        # チャンネルメンバーを取得
        members = await self.db.get_channel_members(message["channel_id"])
        
        # WebSocket経由でメンバーに配信
        for member in members:
            await self.websocket_manager.send_to_user(
                user_id=member["user_id"],
                data=message
            )
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のメッセージ取得**: 50億回
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

#### 書き込みトラフィック

- **1日のメッセージ数**: 150億メッセージ
- **1時間あたり**: 150億 / 24 = 約6.25億メッセージ
- **1秒あたり**: 6.25億 / 3600 = 約173,611メッセージ/秒
- **ピーク時（3倍）**: 約520,833メッセージ/秒

### ストレージ見積もり

#### メッセージストレージ

- **1メッセージあたりのサイズ**: 約500バイト（テキストメッセージ）
- **1日のメッセージ数**: 150億メッセージ
- **1日のストレージ**: 150億 × 500バイト = 75 GB
- **1年のストレージ**: 75 GB × 365 = 約27.375 TB
- **5年のストレージ**: 約136.875 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **WebSocket**: リアルタイム通信にWebSocketを使用
4. **WebRTC**: 低レイテンシのボイスチャットにWebRTCを使用
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **ボイスチャットのレイテンシ**:
   - 問題: WebRTC接続のレイテンシが高い
   - 解決策: 地理的に分散したMedia Servers

2. **メッセージ配信のスケーラビリティ**:
   - 問題: 大規模チャンネルでのメッセージ配信が困難
   - 解決策: メッセージキューとバッチ処理

## 15. 関連システム

### 類似システムへのリンク

- [Slack](slack_design.md) - ビジネス向けメッセージング
- [Telegram](telegram_design.md) - メッセージングアプリ
- [Zoom](../15_realtime_systems/zoom_design.md) - ビデオ会議

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Bing](../05_search_engines/bing_design.md)で検索エンジンの設計を学ぶ

