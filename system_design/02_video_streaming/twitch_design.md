# Twitch システム設計

## 1. システム概要

### 目的と主要機能

Twitchは、ユーザーがリアルタイムでライブストリーミング配信を行い、視聴者がコメントやチャットでインタラクションできるライブストリーミングプラットフォームです。

**主要機能**:
- ライブストリーミング配信
- ライブストリーミング視聴
- チャット機能
- フォロー/サブスクリプション
- クリップ作成
- VOD（Video On Demand）再生
- エモート（絵文字）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3億人
- **日間アクティブユーザー（DAU）**: 約1.5億人
- **同時視聴者数**: 約300万人（ピーク時）
- **1日のライブストリーム数**: 約500万ストリーム
- **1日のチャットメッセージ数**: 約10億メッセージ

### 主要なユースケース

1. **ライブストリーミング配信**: ストリーマーがライブ配信を開始
2. **ライブストリーミング視聴**: 視聴者がライブストリームを視聴
3. **チャット**: 視聴者がチャットでコメント
4. **VOD再生**: 過去の配信を再生

## 2. 機能要件

### コア機能

1. **ライブストリーミング**
   - RTMP/WebRTC経由でのストリーム受信
   - 動画のエンコード・トランスコード
   - 適応的ビットレートストリーミング（ABR）
   - 低レイテンシストリーミング

2. **チャット**
   - リアルタイムチャット
   - エモート（絵文字）
   - モデレーション機能

3. **VOD**
   - 過去の配信の保存
   - VODの再生

4. **フォロー/サブスクリプション**
   - ストリーマーのフォロー
   - サブスクリプション（有料）

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: チャットは最終的に一貫性を保つ
- **パフォーマンス**:
  - ストリーム開始: < 5秒
  - ストリーム視聴開始: < 3秒
  - チャット送信: < 100ms
  - ストリームレイテンシ: < 3秒（低レイテンシモード）
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: VODは永続的に保存

### 優先順位付け

1. **P0（必須）**: ライブストリーミング配信・視聴、チャット
2. **P1（重要）**: VOD、フォロー/サブスクリプション
3. **P2（望ましい）**: クリップ、エモート

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
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
│  │ Stream   │  │  Chat    │  │  VOD     │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Ingest Service                 │         │
│  │      Transcoding Service            │         │
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
│         Ingest Servers (RTMP/WebRTC)             │
│         CDN (CloudFront/Cloudflare)             │
│         Object Storage (S3)                      │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Stream Service**: ストリームの管理と配信
   - **Chat Service**: チャット機能
   - **VOD Service**: VODの管理と再生
   - **Ingest Service**: ストリーマーからのストリーム受信
   - **Transcoding Service**: 動画のエンコード・トランスコード
4. **Database**: ストリームメタデータ、チャット、VODの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（トランスコード、チャット配信など）
7. **Ingest Servers**: RTMP/WebRTC経由でストリームを受信
8. **CDN**: ストリームの配信
9. **Object Storage**: VODの保存

### データフロー

#### ライブストリーミング配信のフロー

```
1. Streamer → Ingest Server (RTMP/WebRTC)
2. Ingest Server:
   a. ストリームを受信
   b. ストリームメタデータをデータベースに保存
   c. Transcoding Serviceにストリームを転送
3. Transcoding Service:
   a. ストリームを複数の解像度・ビットレートにトランスコード
   b. CDNに配信
4. CDN → Viewers（ストリーム配信）
```

#### チャット送信のフロー

```
1. Viewer → API Gateway → Chat Service
2. Chat Service:
   a. メッセージを検証・モデレーション
   b. データベースに保存
   c. Message Queueに送信
3. Chat Service（複数のインスタンス）:
   a. Message Queueからメッセージを受信
   b. WebSocket経由で視聴者に配信
```

## 4. データモデル設計

### 主要なエンティティ

#### Streams テーブル

```sql
CREATE TABLE streams (
    stream_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200),
    game_id BIGINT,
    viewer_count INT DEFAULT 0,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status ENUM('live', 'ended') DEFAULT 'live',
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_status_started_at (status, started_at DESC),
    INDEX idx_game_id (game_id)
) ENGINE=InnoDB;
```

#### Chat_Messages テーブル

```sql
CREATE TABLE chat_messages (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    stream_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stream_id) REFERENCES streams(stream_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_stream_id_created_at (stream_id, created_at DESC)
) ENGINE=InnoDB;
```

#### VODs テーブル

```sql
CREATE TABLE vods (
    vod_id BIGINT PRIMARY KEY,
    stream_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    title VARCHAR(200),
    video_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    duration INT NOT NULL,
    view_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stream_id) REFERENCES streams(stream_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ストリームメタデータ、チャット、VODの永続化
- **NoSQL（Cassandra）**:
  - 理由: チャットメッセージの書き込み負荷が高い、水平スケーリングが必要
  - 用途: チャットメッセージの保存（オプション）

### スキーマ設計の考慮事項

1. **パーティショニング**: `chat_messages`テーブルは`stream_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: チャットメッセージは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ストリーム開始

```
POST /api/v1/streams/start
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "My Stream",
  "game_id": 123
}

Response (200 OK):
{
  "stream_id": 1234567890,
  "ingest_url": "rtmp://ingest.twitch.tv/app/stream_key",
  "stream_key": "live_1234567890_abcdef"
}
```

#### ライブストリーム取得

```
GET /api/v1/streams/{stream_id}
Authorization: Bearer <token>

Response (200 OK):
{
  "stream_id": 1234567890,
  "user_id": 987654321,
  "title": "My Stream",
  "viewer_count": 1000,
  "status": "live",
  "stream_url": "https://cdn.twitch.tv/streams/1234567890.m3u8"
}
```

#### チャット送信

```
POST /api/v1/streams/{stream_id}/chat
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "message": "Hello, chat!"
}

Response (200 OK):
{
  "message_id": 1234567891,
  "message": "Hello, chat!",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のストリームのみ管理可能
- **レート制限**: 
  - チャット送信: 20メッセージ/30秒
  - ストリーム開始: 1ストリーム/ユーザー

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Stream IDベースのシャーディング

```
Shard 1: stream_id % 4 == 0
Shard 2: stream_id % 4 == 1
Shard 3: stream_id % 4 == 2
Shard 4: stream_id % 4 == 3
```

**シャーディングキー**: `stream_id`
- チャットメッセージは`stream_id`でシャーディング
- VODは`stream_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **Ingest Servers**: ストリーム数に応じてスケール

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ストリームをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ストリームメタデータ、チャット履歴
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ストリームセグメント、VOD
   - TTL: リアルタイム（ストリーム）、24時間（VOD）

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ストリームトランスコード**: CPU集約的な処理
2. **チャット配信**: リアルタイム性が重要
3. **ストリーム配信**: ネットワークレイテンシ

### CDNの活用

- **ストリーム配信**: CloudflareまたはAWS CloudFront
- **適応的ビットレートストリーミング（ABR）**: ネットワーク状況に応じてビットレートを調整
- **低レイテンシストリーミング**: WebRTCまたは低レイテンシHLS

### チャット配信最適化

1. **WebSocket**: リアルタイム双方向通信
2. **メッセージキュー**: Kafkaでチャットメッセージを配信
3. **バッチ処理**: 複数のメッセージをバッチで配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **チャットメッセージ**:
   ```
   Topic: chat-messages
   Partition Key: stream_id
   ```

2. **ストリーム終了イベント**:
   ```
   Topic: stream-ended
   Partition Key: stream_id
   ```

3. **VOD生成**:
   - ストリーム終了時に非同期でVODを生成
   - トランスコードしてObject Storageに保存

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3億人
- **日間アクティブユーザー**: 1.5億人
- **同時視聴者数**: 300万人（ピーク時）
- **1日のライブストリーム数**: 500万ストリーム
- **1日のチャットメッセージ数**: 10億メッセージ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**トランスコードサーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 1,000台
- コスト: $0.34/時間 × 1,000台 × 730時間 = **$248,200/月**

**Ingest Servers**:
- EC2インスタンス: m5.2xlarge (8 vCPU, 32 GB RAM)
- インスタンス数: 200台
- コスト: $0.384/時間 × 200台 × 730時間 = **$56,064/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 60台（マスター + レプリカ）
- コスト: $0.76/時間 × 60台 × 730時間 = **$33,288/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 150台
- コスト: $0.175/時間 × 150台 × 730時間 = **$19,162.50/月**

**ストレージ（S3）**:
- VODストレージ: 50 PB
- コスト: $0.023/GB/月 × 50,000,000 GB = **$1,150,000/月**

**ネットワーク（CDN）**:
- データ転送: 20 PB/月
- コスト: $0.085/GB × 20,000,000 GB = **$1,700,000/月**

**合計**: 約 **$3,436,874.50/月**（約41,242,494ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: トランスコードジョブで最大90%削減
3. **動画圧縮**: ストレージコストを削減
4. **CDN活用**: データ転送コストを削減
5. **VODのライフサイクル管理**: 古いVODを低コストストレージに移動

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Ingest Serversのヘルスチェック

3. **サーキットブレーカー**:
   - 障害が発生したサービスへのリクエストを遮断
   - フォールバック処理を実装

### 冗長化戦略

#### データベース冗長化

- **マスター-レプリカ構成**: 1つのマスター、複数のレプリカ
- **自動フェイルオーバー**: マスター障害時にレプリカを昇格
- **マルチリージョン**: 地理的に分散したレプリカ

#### Ingest Servers冗長化

- **複数のIngest Servers**: 地理的に分散
- **自動フェイルオーバー**: 障害時に別のIngest Serverに切り替え

### バックアップ・復旧戦略

1. **データベースバックアップ**:
   - 日次フルバックアップ
   - 継続的なバックアップ（ポイントインタイムリカバリ）
   - バックアップの保存期間: 30日

2. **VODバックアップ**:
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
   - ユーザーは自分のストリームのみ管理可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - Object Storage: S3サーバーサイド暗号化

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
- **ストリーム視聴開始**: < 3秒
- **チャット送信**: < 100ms

### プログレッシブローディング

1. **適応的ビットレートストリーミング（ABR）**:
   - ネットワーク状況に応じてビットレートを調整
   - スムーズな再生体験を提供

2. **低レイテンシストリーミング**:
   - WebRTCまたは低レイテンシHLS
   - リアルタイム性を重視

## 12. 実装例

### ストリームサービス（疑似コード）

```python
class StreamService:
    def __init__(self, db, cache, ingest_service):
        self.db = db
        self.cache = cache
        self.ingest_service = ingest_service
    
    async def start_stream(self, user_id: int, title: str, game_id: int):
        # ストリームメタデータをデータベースに保存
        stream_id = await self.db.insert_stream(
            user_id=user_id,
            title=title,
            game_id=game_id,
            status='live'
        )
        
        # Ingest URLとStream Keyを生成
        ingest_url, stream_key = self.ingest_service.generate_ingest_info(stream_id)
        
        return {
            "stream_id": stream_id,
            "ingest_url": ingest_url,
            "stream_key": stream_key
        }
```

### チャットサービス（疑似コード）

```python
class ChatService:
    def __init__(self, db, cache, message_queue, websocket_manager):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
        self.websocket_manager = websocket_manager
    
    async def send_message(self, stream_id: int, user_id: int, message: str):
        # メッセージを検証・モデレーション
        if not self.moderate_message(message):
            raise ValueError("Message violates community guidelines")
        
        # データベースに保存
        message_id = await self.db.insert_chat_message(
            stream_id=stream_id,
            user_id=user_id,
            message=message
        )
        
        # メッセージキューに送信
        await self.message_queue.publish(
            topic="chat-messages",
            message={
                "message_id": message_id,
                "stream_id": stream_id,
                "user_id": user_id,
                "message": message
            },
            partition_key=stream_id
        )
        
        return {
            "message_id": message_id,
            "message": message
        }
    
    async def handle_chat_message(self, message):
        # WebSocket経由で視聴者に配信
        await self.websocket_manager.broadcast_to_stream(
            stream_id=message["stream_id"],
            data=message
        )
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **同時視聴者数**: 300万人（ピーク時）
- **1ストリームあたりの帯域幅**: 平均5 Mbps
- **合計帯域幅**: 300万 × 5 Mbps = 15 Tbps

#### 書き込みトラフィック

- **1日のライブストリーム数**: 500万ストリーム
- **1時間あたり**: 500万 / 24 = 約208,333ストリーム
- **1秒あたり**: 208,333 / 3600 = 約58ストリーム/秒

#### チャットトラフィック

- **1日のチャットメッセージ数**: 10億メッセージ
- **1時間あたり**: 10億 / 24 = 約4,167万メッセージ
- **1秒あたり**: 4,167万 / 3600 = 約11,575メッセージ/秒

### ストレージ見積もり

#### VODストレージ

- **1ストリームあたりの平均時間**: 2時間
- **1ストリームあたりのサイズ**: 平均5 GB
- **1日のVODストレージ**: 500万 × 5 GB = 25 PB
- **1年のストレージ**: 25 PB × 365 = 約9,125 PB

### 帯域幅見積もり

#### ストリーム配信帯域幅

- **同時視聴者数**: 300万人（ピーク時）
- **1ストリームあたりの帯域幅**: 平均5 Mbps
- **配信帯域幅**: 300万 × 5 Mbps = 15 Tbps

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **CDNファースト**: ストリームはCDN経由で配信
4. **適応的ビットレートストリーミング**: ネットワーク状況に応じてビットレートを調整
5. **低レイテンシ**: WebRTCまたは低レイテンシHLS

### よくある落とし穴

1. **ストリームトランスコードのボトルネック**:
   - 問題: トランスコードが遅い
   - 解決策: 非同期処理と並列化

2. **チャット配信のスケーラビリティ**:
   - 問題: 大規模ストリームでのチャット配信が困難
   - 解決策: メッセージキューとWebSocketの組み合わせ

## 15. 関連システム

### 類似システムへのリンク

- [YouTube](youtube_design.md) - 動画共有プラットフォーム
- [TikTok](tiktok_design.md) - 動画共有プラットフォーム
- [Netflix](netflix_design.md) - ストリーミングサービス

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Hulu](hulu_design.md)で動画ストリーミングサービスの設計を学ぶ

