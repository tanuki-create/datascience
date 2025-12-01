# Nintendo Switch Online システム設計

## 1. システム概要

### 目的と主要機能

Nintendo Switch Onlineは、任天堂が提供するコンソールゲームプラットフォームです。Nintendo Switchコンソール向けのオンラインゲームプレイ、クラシックゲーム配信、クラウドセーブを提供します。

**主要機能**:
- オンラインゲームプレイ
- Nintendo Switch Online アプリ
- クラシックゲーム配信（NES/SNES/N64/Game Boy）
- クラウドセーブ
- 特別オファー
- バーチャルコンソール

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3,800万人
- **日間アクティブユーザー（DAU）**: 約1,500万人
- **1日の同時接続ユーザー**: 約800万人（ピーク時）
- **1日のオンラインゲームセッション数**: 約500万セッション
- **1秒あたりのリクエスト数**: 約8,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **オンラインゲームプレイ**: ユーザーがオンラインでマルチプレイヤーゲームをプレイ
2. **クラシックゲーム配信**: ユーザーがクラシックゲームをダウンロード・プレイ
3. **クラウドセーブ**: ユーザーがセーブデータをクラウドに保存
4. **フレンド機能**: ユーザーがフレンドを追加・管理
5. **特別オファー**: ユーザーが特別オファーを利用

## 2. 機能要件

### コア機能

1. **オンラインゲームプレイ**
   - マルチプレイヤーゲーム
   - ゲームサーバーの管理
   - マッチメイキング

2. **クラシックゲーム配信**
   - NES/SNES/N64/Game Boyゲームの配信
   - ゲームのダウンロード・ストリーミング
   - ゲームライブラリ管理

3. **クラウドセーブ**
   - セーブデータのクラウド保存
   - セーブデータの同期
   - セーブデータの復元

4. **フレンド機能**
   - フレンドの追加・削除
   - オンラインステータス表示
   - パーティー機能

5. **Nintendo Switch Online アプリ**
   - スマートフォンアプリとの連携
   - ボイスチャット
   - ゲーム内情報の表示

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: セーブデータは強い一貫性、オンラインゲームは最終的に一貫性を保つ
- **パフォーマンス**:
  - オンラインゲーム接続: < 3秒
  - マッチメイキング: < 15秒
  - クラウドセーブ同期: < 2秒
  - クラシックゲームダウンロード開始: < 5秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: セーブデータは永続的に保存

### 優先順位付け

1. **P0（必須）**: オンラインゲームプレイ、クラウドセーブ、マッチメイキング
2. **P1（重要）**: クラシックゲーム配信、フレンド機能、Nintendo Switch Online アプリ
3. **P2（望ましい）**: 特別オファー、バーチャルコンソール拡張

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Nintendo Switch Console, Mobile App)
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
│  │ Online   │  │ Classic  │  │ Cloud    │        │
│  │ Gaming   │  │ Game     │  │ Save     │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Game Server Manager             │         │
│  │      Match Making Service           │         │
│  │      Friend Service                  │         │
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
│         Game Servers (Dedicated Servers)         │
│         CDN (CloudFront/Cloudflare)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Online Gaming Service**: オンラインゲームプレイの管理
   - **Classic Game Service**: クラシックゲームの配信
   - **Cloud Save Service**: クラウドセーブの管理
   - **Game Server Manager**: ゲームサーバーの管理
   - **Match Making Service**: マッチメイキングの処理
   - **Friend Service**: フレンド機能の管理
4. **Database**: セーブデータ、ユーザー、フレンドの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（セーブデータ同期など）
7. **Object Storage**: クラシックゲームファイルの保存
8. **Game Servers**: マルチプレイヤーゲーム用の専用サーバー
9. **CDN**: クラシックゲームファイルの配信

### データフロー

#### クラウドセーブ同期のフロー

```
1. Client (Nintendo Switch) → Load Balancer → API Gateway
2. API Gateway → Cloud Save Service
3. Cloud Save Service:
   a. セーブデータをデータベースに保存
   b. セーブデータを同期（非同期）
   c. 他のデバイスに通知を送信（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Classic_Games テーブル

```sql
CREATE TABLE classic_games (
    game_id BIGINT PRIMARY KEY,
    game_name VARCHAR(500) NOT NULL,
    console_type ENUM('NES', 'SNES', 'N64', 'GameBoy') NOT NULL,
    release_date DATE,
    file_size BIGINT NOT NULL,
    download_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_console_type (console_type),
    FULLTEXT INDEX idx_game_name (game_name)
) ENGINE=InnoDB;
```

#### User_Save_Data テーブル

```sql
CREATE TABLE user_save_data (
    save_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    game_id BIGINT NOT NULL,
    save_data BLOB NOT NULL,
    save_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    INDEX idx_user_id (user_id),
    INDEX idx_game_id (game_id),
    INDEX idx_save_timestamp (save_timestamp)
) ENGINE=InnoDB;
```

#### User_Classic_Games テーブル

```sql
CREATE TABLE user_classic_games (
    user_id BIGINT NOT NULL,
    game_id BIGINT NOT NULL,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, game_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (game_id) REFERENCES classic_games(game_id),
    INDEX idx_user_id (user_id),
    INDEX idx_game_id (game_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: セーブデータ、ユーザー、フレンドの永続化
- **Redis**:
  - 理由: リアルタイムデータ、マッチメイキングキュー
  - 用途: マッチメイキングキュー、オンラインステータス

### スキーマ設計の考慮事項

1. **パーティショニング**: `user_save_data`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: セーブデータは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### クラウドセーブ保存

```
POST /api/v1/save-data
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "game_id": 1234567890,
  "save_data": "<base64_encoded_data>"
}

Response (200 OK):
{
  "save_id": 9876543210,
  "game_id": 1234567890,
  "save_timestamp": "2024-01-15T10:30:00Z"
}
```

#### クラウドセーブ取得

```
GET /api/v1/save-data?game_id=1234567890
Authorization: Bearer <token>

Response (200 OK):
{
  "save_id": 9876543210,
  "game_id": 1234567890,
  "save_data": "<base64_encoded_data>",
  "save_timestamp": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Nintendo Account統合
- **認可**: ユーザーは自分のセーブデータのみアクセス可能
- **レート制限**: 
  - クラウドセーブ保存: 100回/分
  - クラシックゲームダウンロード: 無制限

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### ゲームサーバー

- **専用サーバー**: マルチプレイヤーゲーム用の専用サーバー
- **動的スケーリング**: 需要に応じてゲームサーバーを起動・停止
- **地理的分散**: 複数のリージョンにゲームサーバーを配置

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- セーブデータは`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: クラシックゲームファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ゲームメタデータ、セーブデータ、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: クラシックゲームファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **セーブデータ同期**: 大量のセーブデータの同期
2. **ゲームサーバー接続**: 低レイテンシが必要
3. **クラシックゲームダウンロード**: ファイルサイズは小さいが、多数のダウンロード

### CDNの活用

- **クラシックゲームファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### セーブデータ同期最適化

1. **差分同期**: 変更された部分のみを同期
2. **キャッシング**: セーブデータをキャッシュ
3. **非同期処理**: セーブデータ同期を非同期で処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **セーブデータ同期**:
   ```
   Topic: save-data-sync
   Partition Key: user_id
   ```

2. **ゲームサーバー管理**:
   ```
   Topic: game-server-management
   Partition Key: game_server_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3,800万人
- **日間アクティブユーザー**: 1,500万人
- **1日の同時接続ユーザー**: 800万人（ピーク時）

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.large (2 vCPU, 8 GB RAM)
- インスタンス数: 300台（リージョン間で分散）
- コスト: $0.096/時間 × 300台 × 730時間 = **$21,024/月**

**ゲームサーバー**:
- EC2インスタンス: c5.xlarge (4 vCPU, 8 GB RAM)
- インスタンス数: 1,200台（動的スケーリング）
- コスト: $0.17/時間 × 1,200台 × 730時間 = **$148,920/月**

**データベース**:
- RDS MySQL db.r5.xlarge (4 vCPU, 32 GB RAM)
- インスタンス数: 20台（マスター + レプリカ）
- コスト: $0.38/時間 × 20台 × 730時間 = **$5,548/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.large (13 GB RAM)
- インスタンス数: 30台
- コスト: $0.087/時間 × 30台 × 730時間 = **$1,905/月**

**ストレージ（S3）**:
- クラシックゲームファイルストレージ: 50 TB
- コスト: $0.023/GB/月 × 50,000 GB = **$1,150/月**

**ネットワーク**:
- データ転送: 20 PB/月
- コスト: $0.09/GB × 20,000,000 GB = **$1,800,000/月**

**合計**: 約 **$1,977,547/月**（約23,730,564ドル/年）

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
   - ゲームサーバーのヘルスチェック

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

2. **セーブデータバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Nintendo Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のセーブデータのみアクセス可能

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
- **マッチメイキング**: < 15秒
- **ゲームサーバー接続**: < 3秒
- **クラウドセーブ同期**: < 2秒

### プログレッシブローディング

1. **クラシックゲームライブラリの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのゲームはスクロール時に読み込み

2. **セーブデータ一覧の遅延読み込み**:
   - 最初の10件を先に表示
   - 残りのセーブデータはスクロール時に読み込み

## 12. 実装例

### クラウドセーブサービス（疑似コード）

```python
class CloudSaveService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def save_game_data(self, user_id: int, game_id: int, save_data: bytes):
        # セーブデータを保存
        save_id = await self.db.insert_save_data(
            user_id=user_id,
            game_id=game_id,
            save_data=save_data
        )
        
        # セーブデータ同期を非同期で処理
        await self.message_queue.publish(
            topic="save-data-sync",
            message={
                "user_id": user_id,
                "game_id": game_id,
                "save_id": save_id
            },
            partition_key=user_id
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"user:{user_id}:game:{game_id}:save")
        
        return {
            "save_id": save_id,
            "game_id": game_id,
            "save_timestamp": datetime.now()
        }
    
    async def load_game_data(self, user_id: int, game_id: int):
        # キャッシュを確認
        cache_key = f"user:{user_id}:game:{game_id}:save"
        cached_save = await self.cache.get(cache_key)
        
        if cached_save:
            return cached_save
        
        # データベースから取得
        save_data = await self.db.get_latest_save_data(
            user_id=user_id,
            game_id=game_id
        )
        
        # キャッシュに保存
        await self.cache.setex(
            cache_key,
            300,  # TTL: 5分
            save_data
        )
        
        return save_data
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のクラシックゲームライブラリアクセス**: 2億回
- **1時間あたり**: 2億 / 24 = 約833万回
- **1秒あたり**: 833万 / 3600 = 約2,315回/秒
- **ピーク時（3倍）**: 約6,945回/秒

#### 書き込みトラフィック

- **1日のセーブデータ保存数**: 5,000万回
- **1時間あたり**: 5,000万 / 24 = 約208万回
- **1秒あたり**: 208万 / 3600 = 約578回/秒
- **ピーク時（3倍）**: 約1,734回/秒

### ストレージ見積もり

#### クラシックゲームファイルストレージ

- **1ゲームあたりの平均サイズ**: 5 MB
- **クラシックゲームライブラリ**: 10,000タイトル
- **合計ストレージ**: 10,000 × 5 MB = 50 GB

#### セーブデータストレージ

- **1セーブデータあたりの平均サイズ**: 1 MB
- **1ユーザーあたりの平均セーブデータ数**: 20
- **ユーザー数**: 3,800万人
- **合計ストレージ**: 3,800万 × 20 × 1 MB = 760 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **ゲームサーバー**: マルチプレイヤーゲーム用の専用サーバー
4. **クラウドセーブ**: リアルタイムセーブデータ同期
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **セーブデータ同期のスケーラビリティ**:
   - 問題: 大量のセーブデータの同期が遅い
   - 解決策: 差分同期と非同期処理

2. **ゲームサーバーのスケーラビリティ**:
   - 問題: ゲームサーバーのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

## 15. 関連システム

### 類似システムへのリンク

- [Steam](steam_design.md) - PCゲームプラットフォーム
- [Epic Games](epic_games_design.md) - ゲーム配信プラットフォーム
- [PlayStation Network](playstation_network_design.md) - コンソールゲームプラットフォーム
- [Xbox Live](xbox_live_design.md) - コンソールゲームプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Realtime Systems](../15_realtime_systems/zoom_design.md) - リアルタイムシステム

---

**次のステップ**: [Apple Pay](../12_payment_finance/apple_pay_design.md)でモバイル決済システムの設計を学ぶ

