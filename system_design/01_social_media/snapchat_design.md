# Snapchat システム設計

## 1. システム概要

### 目的と主要機能

Snapchatは、エフェメラルメッセージング（一時的なメッセージ）を特徴とするソーシャルメディアプラットフォームです。スナップ（写真・動画）を送信し、一定時間後に自動的に削除されます。

**主要機能**:
- スナップ送信（写真・動画）
- ストーリー（24時間有効）
- チャット（1対1、グループ）
- フィルター・レンズ（AR機能）
- Discover（コンテンツ発見）
- Snap Map（位置情報共有）
- Memories（保存されたスナップ）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約4億人
- **日間アクティブユーザー（DAU）**: 約2.5億人
- **1日のスナップ送信数**: 約50億スナップ
- **1日のストーリー視聴**: 約30億回
- **1秒あたりのスナップ送信**: 約60,000スナップ/秒（ピーク時）

### 主要なユースケース

1. **スナップ送信**: ユーザーがスナップを送信
2. **ストーリー投稿**: ユーザーがストーリーに投稿
3. **チャット**: ユーザーがチャットでメッセージを送信
4. **フィルター・レンズ**: ユーザーがARフィルター・レンズを使用
5. **Discover**: ユーザーがDiscoverコンテンツを閲覧

## 2. 機能要件

### コア機能

1. **スナップ送信**
   - 写真・動画の送信
   - タイマー設定（1-10秒）
   - 自動削除

2. **ストーリー**
   - 24時間有効なストーリー
   - ストーリーの視聴
   - ストーリーの自動削除

3. **チャット**
   - 1対1チャット
   - グループチャット
   - メッセージの自動削除

4. **フィルター・レンズ**
   - ARフィルター
   - レンズ（ARエフェクト）
   - リアルタイム処理

5. **Memories**
   - スナップの保存
   - 保存されたスナップの管理

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: スナップは最終的に一貫性を保つ
- **パフォーマンス**:
  - スナップ送信: < 2秒
  - スナップ受信: < 1秒
  - ストーリー読み込み: < 500ms
  - ARフィルター処理: < 100ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: Memoriesは永続的に保存、スナップは一時的

### 優先順位付け

1. **P0（必須）**: スナップ送信、ストーリー、チャット
2. **P1（重要）**: フィルター・レンズ、Memories、Discover
3. **P2（望ましい）**: Snap Map、高度なAR機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Mobile Apps)
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
│  │ Snap     │  │ Story    │  │ Chat     │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  │          │  │          │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      AR Service (Filters/Lenses)      │         │
│  │      Media Service                   │         │
│  │      Deletion Service                │         │
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
│         (Temporary Snap Storage)                  │
│         (Memories Storage)                        │
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Snap Service**: スナップの送受信
   - **Story Service**: ストーリーの管理
   - **Chat Service**: チャットの管理
   - **AR Service**: フィルター・レンズの処理
   - **Media Service**: メディアファイルの管理
   - **Deletion Service**: スナップの自動削除
4. **Database**: スナップメタデータ、ストーリー、チャットの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（スナップ配信、削除など）
7. **Object Storage**: スナップファイルの一時保存、Memoriesの永続保存
8. **CDN**: メディアファイルの配信

### データフロー

#### スナップ送信のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Snap Service
3. Snap Service:
   a. スナップファイルをObject Storageに保存（一時的）
   b. スナップメタデータをデータベースに保存
   c. タイマーを設定（Deletion Service）
   d. 受信者に通知（WebSocketまたはプッシュ通知）
   e. 受信者が開封後、タイマーが開始
   f. タイマー終了後、自動削除
```

## 4. データモデル設計

### 主要なエンティティ

#### Snaps テーブル

```sql
CREATE TABLE snaps (
    snap_id BIGINT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    recipient_id BIGINT,
    group_id BIGINT,
    media_url VARCHAR(500) NOT NULL,
    media_type ENUM('photo', 'video') NOT NULL,
    duration INT NOT NULL, -- 秒
    timer_seconds INT NOT NULL, -- 1-10秒
    status ENUM('sent', 'opened', 'expired', 'deleted') DEFAULT 'sent',
    opened_at TIMESTAMP NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id),
    FOREIGN KEY (group_id) REFERENCES groups(group_id),
    INDEX idx_recipient_id_status (recipient_id, status),
    INDEX idx_expires_at (expires_at),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Stories テーブル

```sql
CREATE TABLE stories (
    story_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    media_url VARCHAR(500) NOT NULL,
    media_type ENUM('photo', 'video') NOT NULL,
    view_count INT DEFAULT 0,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_expires_at (user_id, expires_at),
    INDEX idx_expires_at (expires_at)
) ENGINE=InnoDB;
```

#### Story_Views テーブル

```sql
CREATE TABLE story_views (
    view_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    story_id BIGINT NOT NULL,
    viewer_id BIGINT NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (story_id) REFERENCES stories(story_id),
    FOREIGN KEY (viewer_id) REFERENCES users(user_id),
    UNIQUE KEY unique_story_viewer (story_id, viewer_id),
    INDEX idx_story_id (story_id),
    INDEX idx_viewer_id (viewer_id)
) ENGINE=InnoDB;
```

#### Memories テーブル

```sql
CREATE TABLE memories (
    memory_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    snap_id BIGINT,
    media_url VARCHAR(500) NOT NULL,
    media_type ENUM('photo', 'video') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: スナップメタデータ、ストーリー、チャットの永続化
- **Redis**:
  - 理由: リアルタイムデータ、オンラインステータス、タイマー管理
  - 用途: オンラインステータス、セッション情報、タイマー

### スキーマ設計の考慮事項

1. **パーティショニング**: `snaps`テーブルは`recipient_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: スナップ、ストーリーは時系列で保存
4. **自動削除**: タイマー終了後、自動的に削除

## 5. API設計

### 主要なAPIエンドポイント

#### スナップ送信

```
POST /api/v1/snaps
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "recipient_id": 987654321,
  "media": <file>,
  "media_type": "photo",
  "timer_seconds": 5
}

Response (201 Created):
{
  "snap_id": 1234567890,
  "status": "sent",
  "expires_at": "2024-01-15T10:30:05Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### スナップ開封

```
POST /api/v1/snaps/{snap_id}/open
Authorization: Bearer <token>

Response (200 OK):
{
  "snap_id": 1234567890,
  "media_url": "https://cdn.snapchat.com/...",
  "timer_seconds": 5,
  "opened_at": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Snapchat Account統合
- **認可**: ユーザーは自分のスナップのみアクセス可能
- **レート制限**: 
  - スナップ送信: 1,000回/分
  - ストーリー投稿: 100回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### スナップのシャーディング

**シャーディング戦略**: Recipient IDベースのシャーディング

```
Shard 1: recipient_id % 16 == 0
Shard 2: recipient_id % 16 == 1
...
Shard 16: recipient_id % 16 == 15
```

**シャーディングキー**: `recipient_id`
- スナップは`recipient_id`でシャーディング

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
   - 用途: オンラインステータス、セッション情報、スナップメタデータ
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: メディアファイル（一時的）
   - TTL: 24時間

## 7. レイテンシ最適化

### ボトルネックの特定

1. **スナップ配信**: 大量のスナップの配信
2. **AR処理**: リアルタイムAR処理
3. **メディアファイル配信**: 大きなファイルサイズ

### スナップ配信最適化

1. **WebSocket**: リアルタイムスナップ配信
2. **メッセージキュー**: 非同期スナップ配信
3. **プッシュ通知**: オフライン時の通知

### AR処理最適化

1. **エッジコンピューティング**: ユーザーに近いエッジでAR処理
2. **GPU最適化**: GPU最適化サーバーを使用
3. **キャッシング**: ARフィルター・レンズをキャッシュ

### CDNの活用

- **メディアファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **スナップ配信**:
   ```
   Topic: snap-delivery
   Partition Key: recipient_id
   ```

2. **スナップ削除**:
   ```
   Topic: snap-deletion
   Partition Key: snap_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 4億人
- **日間アクティブユーザー**: 2.5億人
- **1日のスナップ送信数**: 50億スナップ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,500台（リージョン間で分散）
- コスト: $0.192/時間 × 1,500台 × 730時間 = **$210,240/月**

**AR処理サーバー**:
- EC2インスタンス: g4dn.xlarge (4 vCPU, 16 GB RAM, GPU)
- インスタンス数: 500台（動的スケーリング）
- コスト: $0.526/時間 × 500台 × 730時間 = **$191,990/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 150台（マスター + レプリカ）
- コスト: $0.76/時間 × 150台 × 730時間 = **$83,220/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 250台
- コスト: $0.175/時間 × 250台 × 730時間 = **$31,937/月**

**ストレージ（S3）**:
- 一時スナップストレージ: 100 PB（回転）
- Memoriesストレージ: 50 PB
- コスト: $0.023/GB/月 × 150,000,000 GB = **$3,450,000/月**

**ネットワーク**:
- データ転送: 150 PB/月
- コスト: $0.09/GB × 150,000,000 GB = **$13,500,000/月**

**合計**: 約 **$17,467,387/月**（約209,608,644ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減
6. **自動削除**: スナップの自動削除でストレージコストを削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - AR処理サーバーのヘルスチェック

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

2. **Memoriesバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Snapchat Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のスナップのみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - S3: サーバーサイド暗号化

### プライバシー保護

1. **エフェメラルメッセージング**: スナップは自動的に削除
2. **スクリーンショット検出**: スクリーンショットの検出と通知
3. **データ最小化**: 必要最小限のデータのみ保存

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
- **スナップ送信**: < 2秒
- **スナップ受信**: < 1秒
- **ストーリー読み込み**: < 500ms
- **ARフィルター処理**: < 100ms

### プログレッシブローディング

1. **ストーリーの遅延読み込み**:
   - 最初の5件を先に表示
   - 残りのストーリーはスワイプ時に読み込み

2. **チャット履歴の遅延読み込み**:
   - 最初の50件を先に表示
   - 残りのメッセージはスクロール時に読み込み

## 12. 実装例

### スナップサービス（疑似コード）

```python
class SnapService:
    def __init__(self, db, cache, storage, message_queue, deletion_service):
        self.db = db
        self.cache = cache
        self.storage = storage
        self.message_queue = message_queue
        self.deletion_service = deletion_service
    
    async def send_snap(self, sender_id: int, recipient_id: int, 
                       media_file: bytes, timer_seconds: int):
        # メディアファイルをストレージに保存（一時的）
        media_url = await self.storage.upload_temporary(
            file=media_file,
            ttl=timer_seconds + 60  # タイマー + バッファ
        )
        
        # スナップメタデータを保存
        snap_id = await self.db.insert_snap(
            sender_id=sender_id,
            recipient_id=recipient_id,
            media_url=media_url,
            timer_seconds=timer_seconds,
            expires_at=datetime.now() + timedelta(seconds=timer_seconds + 60)
        )
        
        # 受信者がオンラインか確認
        is_online = await self.cache.get(f"user:{recipient_id}:online")
        
        if is_online:
            # WebSocketで即座に通知
            await self.websocket_manager.send_notification(
                user_id=recipient_id,
                notification={
                    "type": "snap_received",
                    "snap_id": snap_id,
                    "sender_id": sender_id
                }
            )
        else:
            # プッシュ通知を送信
            await self.push_notification_service.send(
                user_id=recipient_id,
                message="新しいスナップが届きました"
            )
        
        return {
            "snap_id": snap_id,
            "status": "sent",
            "expires_at": datetime.now() + timedelta(seconds=timer_seconds + 60)
        }
    
    async def open_snap(self, user_id: int, snap_id: int):
        # スナップを取得
        snap = await self.db.get_snap(snap_id=snap_id)
        
        if snap["recipient_id"] != user_id:
            raise UnauthorizedError("Not authorized to open this snap")
        
        if snap["status"] == "expired":
            raise SnapExpiredError("Snap has expired")
        
        # 開封時刻を記録
        await self.db.update_snap(
            snap_id=snap_id,
            status="opened",
            opened_at=datetime.now()
        )
        
        # タイマーを開始（Deletion Service）
        await self.deletion_service.schedule_deletion(
            snap_id=snap_id,
            delay_seconds=snap["timer_seconds"]
        )
        
        return {
            "snap_id": snap_id,
            "media_url": snap["media_url"],
            "timer_seconds": snap["timer_seconds"]
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のスナップ読み込み**: 100億回
- **1時間あたり**: 100億 / 24 = 約4.17億回
- **1秒あたり**: 4.17億 / 3600 = 約115,833回/秒
- **ピーク時（3倍）**: 約347,499回/秒

#### 書き込みトラフィック

- **1日のスナップ送信数**: 50億スナップ
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

### ストレージ見積もり

#### 一時スナップストレージ

- **1スナップあたりの平均サイズ**: 2 MB
- **1日のスナップ数**: 50億スナップ
- **1日のストレージ**: 50億 × 2 MB = 10 PB
- **平均保持期間**: 10秒
- **同時保持ストレージ**: 10 PB × (10秒 / 86400秒) = 約1.16 TB

#### Memoriesストレージ

- **1メモリーあたりの平均サイズ**: 3 MB
- **1ユーザーあたりの平均メモリー数**: 100
- **ユーザー数**: 4億人
- **合計ストレージ**: 4億 × 100 × 3 MB = 120 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **エフェメラルメッセージング**: スナップの自動削除
2. **マイクロサービス**: 機能ごとにサービスを分割
3. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
4. **WebSocket**: リアルタイムスナップ配信
5. **AR処理**: エッジコンピューティングでAR処理
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **スナップ配信のスケーラビリティ**:
   - 問題: 大量のスナップの配信が遅い
   - 解決策: WebSocketとメッセージキューを併用

2. **AR処理のレイテンシ**:
   - 問題: AR処理のレイテンシが高い
   - 解決策: エッジコンピューティングとGPU最適化

3. **ストレージコスト**:
   - 問題: 一時スナップのストレージコストが高い
   - 解決策: 自動削除と効率的なストレージ管理

## 15. 関連システム

### 類似システムへのリンク

- [Instagram](instagram_design.md) - 写真共有プラットフォーム
- [TikTok](tiktok_design.md) - ショート動画プラットフォーム
- [WhatsApp](whatsapp_design.md) - メッセージングシステム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Message Queues](../17_common_patterns/message_queues.md) - メッセージキュー

---

**次のステップ**: [Pinterest](pinterest_design.md)で画像共有プラットフォームの設計を学ぶ

