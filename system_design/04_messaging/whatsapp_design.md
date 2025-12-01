# WhatsApp システム設計

## 1. システム概要

### 目的と主要機能

WhatsAppは、エンドツーエンド暗号化を備えたメッセージングプラットフォームです。

**主要機能**:
- 1対1メッセージング
- グループチャット
- メディア共有（画像、動画、音声）
- 音声通話・ビデオ通話
- ステータス（ストーリー）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約20億人
- **日間アクティブユーザー（DAU）**: 約10億人
- **1日のメッセージ数**: 約1,000億メッセージ
- **1秒あたりのメッセージ**: 約1,200,000メッセージ/秒（ピーク時）

### 主要なユースケース

1. **メッセージ送信**: ユーザーがメッセージを送信
2. **メッセージ受信**: ユーザーがメッセージを受信
3. **グループチャット**: 複数ユーザーでのチャット
4. **メディア共有**: 画像・動画・音声の共有

## 2. 機能要件

### コア機能

1. **メッセージング**
   - テキストメッセージ
   - メディアメッセージ
   - メッセージの配信確認

2. **エンドツーエンド暗号化**
   - メッセージの暗号化
   - 鍵の管理

3. **オフライン対応**
   - オフライン時のメッセージキューイング
   - オンライン復帰時の同期

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - メッセージ送信: < 100ms
  - メッセージ配信: < 1秒
- **セキュリティ**: エンドツーエンド暗号化

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps)
└──────┬──────┘
       │ HTTPS / WebSocket
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                       │
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
│  │ Message  │  │ Media    │  │ Group    │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      User Service                    │         │
│  └────┬──────────────────────────────────┘         │
└───────┼───────────────────────────────────────────┘
        │
        ├─────────────────┬──────────────────┬──────────┐
        │                 │                  │          │
┌───────▼──────┐  ┌───────▼──────┐  ┌───────▼──────┐  │
│   Database   │  │   Cache       │  │  Message     │  │
│   (Sharded)  │  │   (Redis)     │  │  Queue       │  │
└──────────────┘  └───────────────┘  └──────────────┘  │
        │
┌───────▼───────────────────────────────────┐
│         Object Storage (S3)                │
│         (Media files)                      │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Message Service**: メッセージの送受信
2. **Media Service**: メディアファイルの管理
3. **Group Service**: グループチャットの管理
4. **Message Queue**: メッセージの非同期配信

## 4. データモデル設計

### 主要なエンティティ

#### Messages テーブル

```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    recipient_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    message_type ENUM('text', 'image', 'video', 'audio') NOT NULL,
    media_url VARCHAR(500),
    encrypted_content BLOB,
    status ENUM('sent', 'delivered', 'read') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id),
    INDEX idx_recipient_id_created_at (recipient_id, created_at DESC),
    INDEX idx_sender_id (sender_id)
) ENGINE=InnoDB;
```

#### Groups テーブル

```sql
CREATE TABLE groups (
    group_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
) ENGINE=InnoDB;
```

#### Group_Members テーブル

```sql
CREATE TABLE group_members (
    group_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    role ENUM('admin', 'member') DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;
```

## 5. API設計

### メッセージ送信

```
POST /api/v1/messages
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "recipient_id": 987654321,
  "content": "Hello!",
  "message_type": "text"
}

Response (201 Created):
{
  "message_id": 1234567890,
  "status": "sent",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## 6. スケーラビリティ設計

### メッセージのシャーディング

- **シャーディングキー**: `recipient_id`
- **シャーディング戦略**: `recipient_id % 16`

### メッセージキュー

- **Kafka**: メッセージの非同期配信
- **パーティション**: `recipient_id`でパーティション

## 7. レイテンシ最適化

### メッセージ配信の最適化

- **WebSocket**: リアルタイムメッセージ配信
- **プッシュ通知**: オフライン時の通知
- **メッセージキュー**: 非同期配信でスループット向上

## 8. コスト最適化

### インフラコストの見積もり

- **サーバー**: 約 **$2,000,000/月**
- **データベース**: 約 **$500,000/月**
- **ストレージ**: 約 **$1,000,000/月**（メディアファイル）
- **合計**: 約 **$3,500,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにデプロイ
- **メッセージの永続化**: メッセージをデータベースに保存

## 10. セキュリティ

### エンドツーエンド暗号化

- **Signal Protocol**: エンドツーエンド暗号化プロトコル
- **鍵交換**: 鍵の安全な交換
- **前進秘匿性**: 過去のメッセージの保護

## 11. UX最適化

### パフォーマンス指標

- **メッセージ送信**: < 100ms
- **メッセージ配信**: < 1秒
- **メディアアップロード**: バックグラウンド処理

## 12. 実装例

### メッセージサービス（疑似コード）

```python
class MessageService:
    def __init__(self, db, message_queue, encryption_service):
        self.db = db
        self.message_queue = message_queue
        self.encryption_service = encryption_service
    
    async def send_message(self, sender_id: int, recipient_id: int, content: str):
        # メッセージを暗号化
        encrypted_content = await self.encryption_service.encrypt(
            content,
            recipient_id
        )
        
        # データベースに保存
        message_id = await self.db.create_message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
            encrypted_content=encrypted_content,
            status="sent"
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="message-delivery",
            partition_key=recipient_id,
            message={
                "message_id": message_id,
                "recipient_id": recipient_id,
                "encrypted_content": encrypted_content
            }
        )
        
        return {
            "message_id": message_id,
            "status": "sent"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日のメッセージ数**: 1,000億メッセージ
- **1秒あたり**: 約1,200,000メッセージ/秒（平均）
- **ピーク時**: 約3,600,000メッセージ/秒

### ストレージ見積もり

- **1メッセージあたりのサイズ**: 約500バイト
- **1日のメッセージストレージ**: 1,000億 × 500バイト = 500 GB
- **1年のメッセージストレージ**: 約182.5 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **エンドツーエンド暗号化**: Signal Protocolを使用
2. **メッセージキュー**: 非同期配信でスループット向上
3. **オフライン対応**: オフライン時のメッセージキューイング

## 15. 関連システム

### 類似システムへのリンク

- [Telegram](telegram_design.md) - セキュアメッセージング
- [Slack](slack_design.md) - ビジネス向けメッセージング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Instagram](instagram_design.md)で写真共有プラットフォームの設計を学ぶ

