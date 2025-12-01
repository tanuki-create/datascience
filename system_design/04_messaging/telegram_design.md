# Telegram システム設計

## 1. システム概要

### 目的と主要機能

Telegramは、エンドツーエンド暗号化を備えたセキュアなメッセージングアプリです。高速、セキュア、プライバシー重視のメッセージングプラットフォームを提供します。

**主要機能**:
- 1対1メッセージング（Secret Chats）
- グループチャット（最大200,000メンバー）
- チャンネル（無制限の購読者）
- ボット（Bot API）
- ファイル共有（最大2GB）
- 音声・ビデオ通話
- 音声メッセージ

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約7億人
- **日間アクティブユーザー（DAU）**: 約5億人
- **1日のメッセージ数**: 約150億メッセージ
- **1秒あたりのメッセージ数**: 約20,000メッセージ/秒（ピーク時）

### 主要なユースケース

1. **メッセージ送信**: ユーザーがメッセージを送信
2. **Secret Chats**: エンドツーエンド暗号化されたチャット
3. **グループチャット**: 大規模グループでのチャット
4. **チャンネル**: ブロードキャストチャンネル
5. **ボット**: 自動化されたボットとの対話

## 2. 機能要件

### コア機能

1. **メッセージング**
   - テキストメッセージ
   - 画像・動画メッセージ
   - 音声メッセージ
   - ファイル送信（最大2GB）

2. **エンドツーエンド暗号化**
   - Secret Chats（MTProtoプロトコル）
   - メッセージの暗号化
   - 鍵の交換

3. **グループチャット**
   - 最大200,000メンバー
   - グループ管理機能
   - メッセージの配信

4. **チャンネル**
   - 無制限の購読者
   - ブロードキャスト機能

5. **ボット**
   - Bot API
   - 自動応答機能

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: メッセージは最終的に一貫性を保つ
- **パフォーマンス**:
  - メッセージ送信: < 100ms
  - メッセージ配信: < 500ms
  - ファイルアップロード: < 30秒（開始）
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: メッセージは永続的に保存（Secret Chatsは除く）

### 優先順位付け

1. **P0（必須）**: メッセージング、Secret Chats、グループチャット
2. **P1（重要）**: チャンネル、ボット、ファイル共有
3. **P2（望ましい）**: 音声・ビデオ通話

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps, Web, Desktop)
└──────┬──────┘
       │ MTProto/HTTPS
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
│  │ Message  │  │  Group   │  │  Channel │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Encryption Service             │         │
│  │      Bot Service                    │         │
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
2. **API Gateway**: リクエストのルーティングと認証（MTProtoプロトコル）
3. **Application Servers**:
   - **Message Service**: メッセージの処理
   - **Group Service**: グループチャットの管理
   - **Channel Service**: チャンネルの管理
   - **Encryption Service**: エンドツーエンド暗号化の処理
   - **Bot Service**: ボットの管理
4. **Database**: メッセージ、ユーザー、グループの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（メッセージ配信など）
7. **Object Storage**: ファイルの保存
8. **CDN**: ファイルの配信

### データフロー

#### メッセージ送信のフロー（Secret Chat）

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Message Service
3. Message Service:
   a. Encryption Serviceでメッセージを暗号化
   b. データベースに保存（暗号化済み）
   c. Message Queueに送信
   d. 受信者の接続を確認
4. Message Service:
   a. Message Queueからメッセージを受信
   b. 受信者がオンラインの場合、即座に配信
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
    channel_id BIGINT,
    chat_type ENUM('secret', 'normal', 'group', 'channel') NOT NULL,
    message_type ENUM('text', 'image', 'video', 'audio', 'file') NOT NULL,
    content TEXT,
    encrypted_content BLOB,
    media_url VARCHAR(500),
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    INDEX idx_sender_receiver_created (sender_id, receiver_id, created_at DESC),
    INDEX idx_group_created (group_id, created_at DESC),
    INDEX idx_channel_created (channel_id, created_at DESC)
) ENGINE=InnoDB;
```

#### Secret_Chats テーブル

```sql
CREATE TABLE secret_chats (
    chat_id BIGINT PRIMARY KEY,
    user_id_1 BIGINT NOT NULL,
    user_id_2 BIGINT NOT NULL,
    encryption_key BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id_1) REFERENCES users(user_id),
    FOREIGN KEY (user_id_2) REFERENCES users(user_id),
    INDEX idx_user_pair (user_id_1, user_id_2)
) ENGINE=InnoDB;
```

#### Channels テーブル

```sql
CREATE TABLE channels (
    channel_id BIGINT PRIMARY KEY,
    creator_id BIGINT NOT NULL,
    channel_name VARCHAR(200) NOT NULL,
    description TEXT,
    subscriber_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(user_id),
    INDEX idx_creator_id (creator_id)
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
4. **暗号化**: Secret Chatsのメッセージは暗号化して保存

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
  "chat_type": "secret",
  "message_type": "text",
  "content": "Hello, Telegram!"
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

- **認証**: MTProtoプロトコル、Phone Number認証
- **認可**: ユーザーは自分のメッセージのみアクセス可能
- **レート制限**: 
  - メッセージ送信: 30メッセージ/秒
  - メッセージ取得: 30リクエスト/秒

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
- **地理的分散**: 複数のリージョンにデプロイ（Telegramは地理的に分散）
- **CDN**: ファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ユーザー情報、グループ情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メッセージ配信**: MTProtoプロトコルの最適化
2. **ファイル転送**: 大きなファイルサイズ
3. **暗号化処理**: エンドツーエンド暗号化のオーバーヘッド

### CDNの活用

- **ファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### メッセージ配信最適化

1. **MTProtoプロトコル**: 高速なプロトコル
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

- **月間アクティブユーザー**: 7億人
- **日間アクティブユーザー**: 5億人
- **1日のメッセージ数**: 150億メッセージ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,500台（リージョン間で分散）
- コスト: $0.192/時間 × 1,500台 × 730時間 = **$210,240/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.76/時間 × 80台 × 730時間 = **$44,384/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 150台
- コスト: $0.175/時間 × 150台 × 730時間 = **$19,162.50/月**

**ストレージ（S3）**:
- メッセージストレージ: 5 PB
- コスト: $0.023/GB/月 × 5,000,000 GB = **$115,000/月**

**ネットワーク**:
- データ転送: 5 PB/月
- コスト: $0.09/GB × 5,000,000 GB = **$450,000/月**

**合計**: 約 **$838,786.50/月**（約10,065,438ドル/年）

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
   - MTProto接続のヘルスチェック

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
   - MTProtoプロトコル
   - Phone Number認証
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のメッセージのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: MTProtoプロトコル（暗号化済み）
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - Secret Chats: エンドツーエンド暗号化

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

2. **ファイルの遅延読み込み**:
   - ビューポートに入るまでファイルを読み込まない
   - サムネイルを先に表示

## 12. 実装例

### メッセージサービス（疑似コード）

```python
class MessageService:
    def __init__(self, db, cache, message_queue, encryption_service):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.encryption_service = encryption_service
    
    async def send_message(self, sender_id: int, receiver_id: int, chat_type: str, message_type: str, content: str):
        # Secret Chatの場合、暗号化
        if chat_type == 'secret':
            encrypted_content = await self.encryption_service.encrypt(
                user_id_1=sender_id,
                user_id_2=receiver_id,
                content=content
            )
        else:
            encrypted_content = None
        
        # メッセージを保存
        message_id = await self.db.insert_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            chat_type=chat_type,
            message_type=message_type,
            content=content if chat_type != 'secret' else None,
            encrypted_content=encrypted_content
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="messages",
            message={
                "message_id": message_id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "chat_type": chat_type,
                "message_type": message_type,
                "content": content if chat_type != 'secret' else None,
                "encrypted_content": encrypted_content
            },
            partition_key=receiver_id
        )
        
        return {
            "message_id": message_id,
            "status": "sent"
        }
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
3. **MTProtoプロトコル**: 高速なプロトコルを使用
4. **エンドツーエンド暗号化**: Secret Chatsでエンドツーエンド暗号化
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **暗号化のオーバーヘッド**:
   - 問題: エンドツーエンド暗号化が遅い
   - 解決策: 効率的な暗号化アルゴリズムの使用

2. **メッセージ配信のスケーラビリティ**:
   - 問題: 大規模グループでのメッセージ配信が困難
   - 解決策: メッセージキューとバッチ処理

## 15. 関連システム

### 類似システムへのリンク

- [WhatsApp](whatsapp_design.md) - メッセージングアプリ
- [WeChat](wechat_design.md) - メッセージングアプリ
- [Slack](slack_design.md) - ビジネス向けメッセージング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Slack](slack_design.md)でビジネス向けメッセージングプラットフォームの設計を学ぶ

