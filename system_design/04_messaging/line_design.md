# LINE システム設計

## 1. システム概要

### 目的と主要機能

LINEは、日本・アジアで人気のメッセージングアプリです。メッセージング、スタンプ、タイムライン、ゲーム、決済などの機能を提供します。

**主要機能**:
- 1対1メッセージング
- グループチャット
- スタンプ（絵文字）
- タイムライン（ソーシャルフィード）
- 音声通話・ビデオ通話
- LINE Pay（決済）
- LINE Games（ゲーム）
- LINE Official Account（企業アカウント）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約2億人
- **日間アクティブユーザー（DAU）**: 約1億人
- **1日のメッセージ数**: 約200億メッセージ
- **1秒あたりのメッセージ**: 約250,000メッセージ/秒（ピーク時）
- **1日のスタンプ送信数**: 約50億個

### 主要なユースケース

1. **メッセージ送信**: ユーザーがメッセージを送信
2. **スタンプ送信**: ユーザーがスタンプを送信
3. **タイムライン投稿**: ユーザーがタイムラインに投稿
4. **LINE Pay決済**: ユーザーがLINE Payで決済
5. **ゲームプレイ**: ユーザーがLINE Gamesをプレイ

## 2. 機能要件

### コア機能

1. **メッセージング**
   - テキストメッセージ
   - スタンプメッセージ
   - メディアメッセージ（画像、動画、音声）
   - メッセージの配信確認

2. **スタンプ**
   - スタンプの購入・管理
   - スタンプの送信
   - スタンプショップ

3. **タイムライン**
   - タイムライン投稿
   - いいね・コメント
   - タイムライン表示

4. **LINE Pay**
   - 決済処理
   - 残高管理
   - 送金機能

5. **LINE Games**
   - ゲーム配信
   - ゲーム内課金
   - ゲームランキング

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: メッセージは最終的に一貫性を保つ
- **パフォーマンス**:
  - メッセージ送信: < 100ms
  - メッセージ配信: < 1秒
  - タイムライン読み込み: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: メッセージは永続的に保存

### 優先順位付け

1. **P0（必須）**: メッセージング、スタンプ、タイムライン
2. **P1（重要）**: LINE Pay、LINE Games、音声・ビデオ通話
3. **P2（望ましい）**: 高度な分析・レポート、AI機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps, Web)
└──────┬──────┘
       │ HTTPS / WebSocket
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
│  │ Message  │  │ Stamp    │  │ Timeline │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  │          │  │          │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      LINE Pay Service                │         │
│  │      LINE Games Service             │         │
│  │      Media Service                  │         │
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
│         (Media files, Stamps)                     │
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Message Service**: メッセージの送受信
   - **Stamp Service**: スタンプの管理・配信
   - **Timeline Service**: タイムラインの管理
   - **LINE Pay Service**: 決済処理
   - **LINE Games Service**: ゲーム配信
   - **Media Service**: メディアファイルの管理
4. **Database**: メッセージ、スタンプ、タイムラインの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（メッセージ配信など）
7. **Object Storage**: メディアファイル、スタンプの保存
8. **CDN**: メディアファイル、スタンプの配信

### データフロー

#### メッセージ送信のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Message Service
3. Message Service:
   a. メッセージをデータベースに保存
   b. メッセージをメッセージキューに送信
   c. 受信者がオンラインの場合、WebSocketで即座に配信
   d. 受信者がオフラインの場合、プッシュ通知を送信
```

## 4. データモデル設計

### 主要なエンティティ

#### Messages テーブル

```sql
CREATE TABLE messages (
    message_id BIGINT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    recipient_id BIGINT,
    group_id BIGINT,
    content TEXT,
    message_type ENUM('text', 'stamp', 'image', 'video', 'audio') NOT NULL,
    stamp_id BIGINT,
    media_url VARCHAR(500),
    status ENUM('sent', 'delivered', 'read') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    INDEX idx_recipient_id_created_at (recipient_id, created_at DESC),
    INDEX idx_group_id_created_at (group_id, created_at DESC),
    INDEX idx_sender_id (sender_id)
) ENGINE=InnoDB;
```

#### Stamps テーブル

```sql
CREATE TABLE stamps (
    stamp_id BIGINT PRIMARY KEY,
    stamp_set_id BIGINT NOT NULL,
    stamp_name VARCHAR(200) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    price DECIMAL(10, 2) DEFAULT 0.00,
    is_free BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stamp_set_id) REFERENCES stamp_sets(stamp_set_id),
    INDEX idx_stamp_set_id (stamp_set_id),
    INDEX idx_is_free (is_free)
) ENGINE=InnoDB;
```

#### User_Stamps テーブル

```sql
CREATE TABLE user_stamps (
    user_id BIGINT NOT NULL,
    stamp_id BIGINT NOT NULL,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, stamp_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (stamp_id) REFERENCES stamps(stamp_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

#### Timeline_Posts テーブル

```sql
CREATE TABLE timeline_posts (
    post_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    content TEXT,
    image_url VARCHAR(500),
    video_url VARCHAR(500),
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: メッセージ、スタンプ、タイムラインの永続化
- **Redis**:
  - 理由: リアルタイムデータ、オンラインステータス
  - 用途: オンラインステータス、セッション情報

### スキーマ設計の考慮事項

1. **パーティショニング**: `messages`テーブルは`recipient_id`または`group_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: メッセージ、タイムラインは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### メッセージ送信

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

#### スタンプ送信

```
POST /api/v1/messages
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "recipient_id": 987654321,
  "stamp_id": 12345,
  "message_type": "stamp"
}

Response (201 Created):
{
  "message_id": 1234567890,
  "status": "sent",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、LINE Account統合
- **認可**: ユーザーは自分のメッセージのみアクセス可能
- **レート制限**: 
  - メッセージ送信: 1,000回/分
  - スタンプ送信: 500回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### メッセージのシャーディング

**シャーディング戦略**: Recipient IDまたはGroup IDベースのシャーディング

```
Shard 1: recipient_id % 16 == 0
Shard 2: recipient_id % 16 == 1
...
Shard 16: recipient_id % 16 == 15
```

**シャーディングキー**: `recipient_id`または`group_id`
- 1対1メッセージは`recipient_id`でシャーディング
- グループメッセージは`group_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: メディアファイル、スタンプをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: オンラインステータス、セッション情報、スタンプ情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: メディアファイル、スタンプ画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メッセージ配信**: 大量のメッセージの配信
2. **タイムライン読み込み**: タイムラインの生成
3. **メディアファイル配信**: 大きなファイルサイズ

### メッセージ配信最適化

1. **WebSocket**: リアルタイムメッセージ配信
2. **メッセージキュー**: 非同期メッセージ配信
3. **プッシュ通知**: オフライン時の通知

### タイムライン最適化

1. **キャッシング**: タイムラインをキャッシュ
2. **遅延読み込み**: タイムラインを段階的に読み込み
3. **事前計算**: タイムラインを事前に計算

### CDNの活用

- **メディアファイル**: CloudflareまたはAWS CloudFront
- **スタンプ画像**: CDNで配信
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **メッセージ配信**:
   ```
   Topic: message-delivery
   Partition Key: recipient_id
   ```

2. **タイムライン更新**:
   ```
   Topic: timeline-update
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 2億人
- **日間アクティブユーザー**: 1億人
- **1日のメッセージ数**: 200億メッセージ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 2,000台（リージョン間で分散）
- コスト: $0.192/時間 × 2,000台 × 730時間 = **$280,320/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 200台（マスター + レプリカ）
- コスト: $0.76/時間 × 200台 × 730時間 = **$110,960/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 300台
- コスト: $0.175/時間 × 300台 × 730時間 = **$38,325/月**

**ストレージ（S3）**:
- メディアファイルストレージ: 500 PB
- コスト: $0.023/GB/月 × 500,000,000 GB = **$11,500,000/月**

**ネットワーク**:
- データ転送: 200 PB/月
- コスト: $0.09/GB × 200,000,000 GB = **$18,000,000/月**

**合計**: 約 **$29,929,605/月**（約359,155,260ドル/年）

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
   - データベースのヘルスチェック

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

2. **メディアファイルバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - LINE Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のメッセージのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - S3: サーバーサイド暗号化

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
- **メッセージ配信**: < 1秒
- **タイムライン読み込み**: < 500ms

### プログレッシブローディング

1. **メッセージ履歴の遅延読み込み**:
   - 最初の50件を先に表示
   - 残りのメッセージはスクロール時に読み込み

2. **タイムラインの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りの投稿はスクロール時に読み込み

## 12. 実装例

### メッセージサービス（疑似コード）

```python
class MessageService:
    def __init__(self, db, cache, message_queue, websocket_manager):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.websocket_manager = websocket_manager
    
    async def send_message(self, sender_id: int, recipient_id: int, 
                          content: str, message_type: str):
        # メッセージを保存
        message_id = await self.db.insert_message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content,
            message_type=message_type,
            status="sent"
        )
        
        # 受信者がオンラインか確認
        is_online = await self.cache.get(f"user:{recipient_id}:online")
        
        if is_online:
            # WebSocketで即座に配信
            await self.websocket_manager.send_message(
                user_id=recipient_id,
                message={
                    "message_id": message_id,
                    "sender_id": sender_id,
                    "content": content,
                    "message_type": message_type
                }
            )
        else:
            # メッセージキューに送信（非同期配信）
            await self.message_queue.publish(
                topic="message-delivery",
                message={
                    "message_id": message_id,
                    "recipient_id": recipient_id,
                    "content": content
                },
                partition_key=recipient_id
            )
        
        return {
            "message_id": message_id,
            "status": "sent",
            "created_at": datetime.now()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のメッセージ読み込み**: 500億回
- **1時間あたり**: 500億 / 24 = 約20.8億回
- **1秒あたり**: 20.8億 / 3600 = 約578,000回/秒
- **ピーク時（3倍）**: 約1,734,000回/秒

#### 書き込みトラフィック

- **1日のメッセージ数**: 200億メッセージ
- **1時間あたり**: 200億 / 24 = 約8.3億回
- **1秒あたり**: 8.3億 / 3600 = 約231,000回/秒
- **ピーク時（3倍）**: 約693,000回/秒

### ストレージ見積もり

#### メッセージストレージ

- **1メッセージあたりの平均サイズ**: 100 bytes
- **1日のメッセージ数**: 200億メッセージ
- **1日のストレージ**: 200億 × 100 bytes = 200 GB
- **1年のストレージ**: 200 GB × 365 = 73 TB

#### メディアファイルストレージ

- **1メディアファイルあたりの平均サイズ**: 5 MB
- **1日のメディアファイル数**: 5億ファイル
- **1日のストレージ**: 5億 × 5 MB = 2.5 PB
- **1年のストレージ**: 2.5 PB × 365 = 912.5 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **WebSocket**: リアルタイムメッセージ配信
4. **メッセージキュー**: 非同期メッセージ配信
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **メッセージ配信のスケーラビリティ**:
   - 問題: 大量のメッセージの配信が遅い
   - 解決策: WebSocketとメッセージキューを併用

2. **タイムラインのスケーラビリティ**:
   - 問題: タイムラインの生成が遅い
   - 解決策: キャッシングと事前計算

## 15. 関連システム

### 類似システムへのリンク

- [WhatsApp](whatsapp_design.md) - メッセージングシステム
- [WeChat](wechat_design.md) - スーパーアプリ
- [Telegram](telegram_design.md) - セキュアメッセージング
- [Slack](slack_design.md) - ビジネスコミュニケーション

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Snapchat](../01_social_media/snapchat_design.md)でソーシャルメディアシステムの設計を学ぶ

