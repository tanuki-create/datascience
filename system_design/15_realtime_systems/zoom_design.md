# Zoom システム設計

## 1. システム概要

### 目的と主要機能

Zoomは、ビデオ会議プラットフォームです。リアルタイムでのビデオ・音声通話、画面共有、チャット機能を提供します。

**主要機能**:
- ビデオ会議
- 音声通話
- 画面共有
- チャット
- 録画・録音
- バーチャル背景
- ブレイクアウトルーム

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3億人
- **日間アクティブユーザー（DAU）**: 約1億人
- **1日の会議数**: 約3,000万回
- **1日の会議参加者数**: 約10億人
- **1秒あたりの同時接続数**: 約500万接続/秒（ピーク時）

### 主要なユースケース

1. **ビデオ会議**: ユーザーがビデオ会議を開始・参加
2. **画面共有**: ユーザーが画面を共有
3. **録画**: ユーザーが会議を録画
4. **チャット**: ユーザーがチャットを送信
5. **ブレイクアウトルーム**: ユーザーがブレイクアウトルームに参加

## 2. 機能要件

### コア機能

1. **ビデオ会議**
   - ビデオストリーミング
   - 音声ストリーミング
   - 低レイテンシ通信

2. **画面共有**
   - 画面のキャプチャ
   - 画面のストリーミング
   - リモート制御

3. **録画・録音**
   - 会議の録画
   - 会議の録音
   - 録画の保存・共有

4. **チャット**
   - テキストチャット
   - ファイル共有
   - リアクション

5. **ブレイクアウトルーム**
   - ルームの作成
   - 参加者の割り当て
   - ルームの管理

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 会議情報は強い一貫性、チャットは最終的に一貫性を保つ
- **パフォーマンス**:
  - ビデオレイテンシ: < 150ms
  - 音声レイテンシ: < 100ms
  - 会議開始: < 5秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 録画は永続的に保存

### 優先順位付け

1. **P0（必須）**: ビデオ会議、音声通話、画面共有
2. **P1（重要）**: 録画・録音、チャット、ブレイクアウトルーム
3. **P2（望ましい）**: バーチャル背景、高度な機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Desktop, Mobile Apps)
└──────┬──────┘
       │ WebRTC / HTTPS
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
│  │ Meeting  │  │  Media   │  │  Chat    │        │
│  │ Service  │  │  Server  │  │ Service  │        │
│  │          │  │          │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Recording Service                │         │
│  │      Breakout Room Service           │         │
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
│         Media Servers (SFU/MCU)                    │
│         Object Storage (S3)                        │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Meeting Service**: 会議の管理
   - **Media Server**: メディアストリーミングの処理
   - **Chat Service**: チャットの管理
   - **Recording Service**: 録画・録音の処理
   - **Breakout Room Service**: ブレイクアウトルームの管理
4. **Database**: 会議、ユーザー、録画の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（録画処理など）
7. **Media Servers**: SFU（Selective Forwarding Unit）またはMCU（Multipoint Control Unit）
8. **Object Storage**: 録画の保存
9. **CDN**: 録画の配信

### データフロー

#### ビデオ会議のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Meeting Service
3. Meeting Service:
   a. 会議を作成または参加
   b. Media Serverに接続情報を取得
   c. ClientにMedia Server情報を返す
4. Client → Media Server (WebRTC)
5. Media Server:
   a. ビデオ・音声ストリームを受信
   b. 他の参加者にストリームを転送
```

## 4. データモデル設計

### 主要なエンティティ

#### Meetings テーブル

```sql
CREATE TABLE meetings (
    meeting_id BIGINT PRIMARY KEY,
    host_id BIGINT NOT NULL,
    meeting_topic VARCHAR(500),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status ENUM('scheduled', 'in_progress', 'ended') DEFAULT 'scheduled',
    max_participants INT DEFAULT 100,
    recording_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(user_id),
    INDEX idx_host_id (host_id),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB;
```

#### Meeting_Participants テーブル

```sql
CREATE TABLE meeting_participants (
    meeting_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at TIMESTAMP,
    video_enabled BOOLEAN DEFAULT TRUE,
    audio_enabled BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (meeting_id, user_id),
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

#### Recordings テーブル

```sql
CREATE TABLE recordings (
    recording_id BIGINT PRIMARY KEY,
    meeting_id BIGINT NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    duration INT NOT NULL,
    status ENUM('processing', 'completed', 'failed') DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id),
    INDEX idx_meeting_id (meeting_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 会議、ユーザー、録画の永続化
- **Redis**:
  - 理由: リアルタイムデータ、セッション管理
  - 用途: 会議セッション、チャットメッセージ

### スキーマ設計の考慮事項

1. **パーティショニング**: `meetings`テーブルは`host_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 会議は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 会議作成

```
POST /api/v1/meetings
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "topic": "Team Meeting",
  "start_time": "2024-01-15T10:00:00Z",
  "duration": 60,
  "recording_enabled": true
}

Response (200 OK):
{
  "id": "meeting_1234567890",
  "join_url": "https://zoom.us/j/1234567890",
  "start_time": "2024-01-15T10:00:00Z"
}
```

#### 会議参加

```
POST /api/v1/meetings/{meeting_id}/join
Authorization: Bearer <token>

Response (200 OK):
{
  "meeting_id": "meeting_1234567890",
  "media_server_url": "wss://media.zoom.us/meeting/1234567890",
  "session_token": "abc123"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の会議のみ管理可能
- **レート制限**: 
  - 会議作成: 100回/日
  - 会議参加: 無制限

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### Media Servers

- **SFU（Selective Forwarding Unit）**: 各参加者のストリームを選択的に転送
- **動的スケーリング**: 需要に応じてMedia Serverを起動・停止
- **地理的分散**: 複数のリージョンにMedia Serverを配置

#### データベースシャーディング

**シャーディング戦略**: Host IDベースのシャーディング

```
Shard 1: host_id % 8 == 0
Shard 2: host_id % 8 == 1
...
Shard 8: host_id % 8 == 7
```

**シャーディングキー**: `host_id`
- 会議は`host_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **Media Server負荷分散**: 最適なMedia Serverにルーティング

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 会議情報、参加者情報、チャットメッセージ
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **メディアストリーミング**: ビデオ・音声のストリーミング
2. **Media Server接続**: Media Serverへの接続時間
3. **録画処理**: 録画のエンコーディング・保存

### CDNの活用

- **録画配信**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### メディアストリーミング最適化

1. **SFUアーキテクチャ**: 各参加者のストリームを選択的に転送
2. **アダプティブビットレート**: ネットワーク状況に応じてビットレートを調整
3. **地理的分散**: ユーザーに近いMedia Serverに接続

### 非同期処理

#### メッセージキュー（Kafka）

1. **録画処理**:
   ```
   Topic: recording-processing
   Partition Key: meeting_id
   ```

2. **会議終了通知**:
   ```
   Topic: meeting-end-notifications
   Partition Key: meeting_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3億人
- **日間アクティブユーザー**: 1億人
- **1日の会議数**: 3,000万回
- **1日の会議参加者数**: 10億人

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**Media Servers**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 10,000台（動的スケーリング）
- コスト: $0.34/時間 × 10,000台 × 730時間 = **$2,482,000/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**ストレージ（S3）**:
- 録画ストレージ: 50 PB
- コスト: $0.023/GB/月 × 50,000,000 GB = **$1,150,000/月**

**ネットワーク**:
- データ転送: 200 PB/月
- コスト: $0.09/GB × 200,000,000 GB = **$18,000,000/月**

**合計**: 約 **$21,812,675/月**（約261,752,100ドル/年）

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
   - Media Serverのヘルスチェック

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

2. **録画バックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - 2要素認証（2FA）: TOTP

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の会議のみ管理可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3、SRTP（Secure Real-time Transport Protocol）
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - 録画: 暗号化されたS3ストレージ

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
- **ビデオレイテンシ**: < 150ms
- **音声レイテンシ**: < 100ms

### プログレッシブローディング

1. **会議一覧の遅延読み込み**:
   - 最初の20件を先に表示
   - 残りの会議はスクロール時に読み込み

2. **録画の遅延読み込み**:
   - 録画のサムネイルを先に表示
   - 録画はクリック時に読み込み

## 12. 実装例

### 会議サービス（疑似コード）

```python
class MeetingService:
    def __init__(self, db, cache, media_server_manager, message_queue):
        self.db = db
        self.cache = cache
        self.media_server_manager = media_server_manager
        self.message_queue = message_queue
    
    async def create_meeting(self, host_id: int, topic: str, start_time: datetime, duration: int):
        # 会議を作成
        meeting_id = await self.db.insert_meeting(
            host_id=host_id,
            topic=topic,
            start_time=start_time,
            duration=duration,
            status='scheduled'
        )
        
        # Media Serverを割り当て
        media_server = await self.media_server_manager.allocate_server(
            meeting_id=meeting_id,
            expected_participants=100
        )
        
        # 会議情報をキャッシュ
        await self.cache.set(
            f"meeting:{meeting_id}",
            {
                "meeting_id": meeting_id,
                "media_server_url": media_server["url"],
                "status": "scheduled"
            },
            ttl=3600
        )
        
        return {
            "id": meeting_id,
            "join_url": f"https://zoom.us/j/{meeting_id}",
            "start_time": start_time.isoformat()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の会議アクセス**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日の会議数**: 3,000万回
- **1時間あたり**: 3,000万 / 24 = 約125万回
- **1秒あたり**: 125万 / 3600 = 約347回/秒
- **ピーク時（3倍）**: 約1,041回/秒

### ストレージ見積もり

#### 録画ストレージ

- **1会議あたりの平均録画サイズ**: 500 MB
- **1日の会議数**: 3,000万回
- **録画率**: 10%
- **1日の録画数**: 3,000万 × 10% = 300万回
- **1日のストレージ**: 300万 × 500 MB = 1.5 PB
- **1年のストレージ**: 1.5 PB × 365 = 約547.5 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **SFUアーキテクチャ**: 各参加者のストリームを選択的に転送
3. **低レイテンシ**: ビデオ・音声の低レイテンシ通信
4. **モニタリング**: 包括的なモニタリングとアラート
5. **セキュリティ**: 強固なセキュリティとコンプライアンス

### よくある落とし穴

1. **Media Serverのスケーラビリティ**:
   - 問題: Media Serverのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

2. **レイテンシ**:
   - 問題: ビデオ・音声のレイテンシが高い
   - 解決策: SFUアーキテクチャと地理的分散

## 15. 関連システム

### 類似システムへのリンク

- [WebRTC](webrtc_design.md) - WebRTCプロトコル
- [Realtime Gaming](realtime_gaming_design.md) - リアルタイムゲーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [WebRTC](webrtc_design.md)でWebRTCプロトコルの設計を学ぶ

