# Epic Games システム設計

## 1. システム概要

### 目的と主要機能

Epic Gamesは、Epic Games StoreとUnreal Engineを提供するゲームプラットフォームです。ゲームの購入、ダウンロード、マルチプレイヤー機能を提供します。

**主要機能**:
- ゲームの購入・ダウンロード
- Epic Games Store
- Fortnite（バトルロイヤルゲーム）
- Unreal Engine（ゲームエンジン）
- フレンド機能
- マルチプレイヤー機能
- クロスプラットフォームプレイ

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約6億人（Fortnite含む）
- **日間アクティブユーザー（DAU）**: 約2.5億人
- **1日の同時接続ユーザー**: 約1,000万人（ピーク時）
- **1日のゲームダウンロード数**: 約500万回
- **1秒あたりのリクエスト数**: 約30,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ゲーム購入**: ユーザーがゲームを購入
2. **ゲームダウンロード**: ユーザーがゲームをダウンロード
3. **マルチプレイヤー**: ユーザーがマルチプレイヤーゲームをプレイ
4. **フレンド機能**: ユーザーがフレンドを追加・管理
5. **クロスプラットフォーム**: 異なるプラットフォーム間でのプレイ

## 2. 機能要件

### コア機能

1. **ゲーム配信**
   - ゲームの購入・ダウンロード
   - ゲームの更新・パッチ配信
   - ゲームライブラリ管理

2. **マルチプレイヤー**
   - リアルタイムマルチプレイヤーゲーム
   - ゲームサーバーの管理
   - マッチメイキング

3. **フレンド機能**
   - フレンドの追加・削除
   - オンラインステータス表示
   - パーティー機能

4. **クロスプラットフォーム**
   - PC、コンソール、モバイル間でのプレイ
   - アカウント統合

5. **決済処理**
   - クレジットカード決済
   - V-Bucks（仮想通貨）

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ゲームライブラリは強い一貫性、マルチプレイヤーは最終的に一貫性を保つ
- **パフォーマンス**:
  - ゲームダウンロード開始: < 5秒
  - マッチメイキング: < 10秒
  - ゲームサーバー接続: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ゲームファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: ゲーム購入・ダウンロード、マルチプレイヤー、マッチメイキング
2. **P1（重要）**: フレンド機能、クロスプラットフォーム、決済処理
3. **P2（望ましい）**: 高度なマルチプレイヤー機能、統計・リーダーボード

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (PC, Console, Mobile)
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
│  │ Game     │  │ Match    │  │ Friend  │        │
│  │ Service  │  │ Making   │  │ Service │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Game Server Manager             │         │
│  │      Payment Service                 │         │
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
   - **Game Service**: ゲームの管理・配信
   - **Match Making Service**: マッチメイキングの処理
   - **Friend Service**: フレンド機能の管理
   - **Game Server Manager**: ゲームサーバーの管理
   - **Payment Service**: 決済処理
4. **Database**: ゲームライブラリ、ユーザー、マッチ情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（マッチメイキングなど）
7. **Object Storage**: ゲームファイルの保存
8. **Game Servers**: マルチプレイヤーゲーム用の専用サーバー
9. **CDN**: ゲームファイルの配信

### データフロー

#### マッチメイキングのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Match Making Service
3. Match Making Service:
   a. ユーザーのスキルレベルを取得
   b. 適切なマッチを検索
   c. マッチが見つかったらGame Server Managerに通知
   d. Game Server Managerがゲームサーバーを割り当て
   e. ユーザーにゲームサーバー情報を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Games テーブル

```sql
CREATE TABLE games (
    game_id BIGINT PRIMARY KEY,
    game_name VARCHAR(500) NOT NULL,
    developer_id BIGINT NOT NULL,
    publisher_id BIGINT NOT NULL,
    release_date DATE,
    price DECIMAL(10, 2) NOT NULL,
    file_size BIGINT NOT NULL,
    download_url VARCHAR(500) NOT NULL,
    is_multiplayer BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_developer_id (developer_id),
    INDEX idx_is_multiplayer (is_multiplayer),
    FULLTEXT INDEX idx_game_name (game_name)
) ENGINE=InnoDB;
```

#### Matches テーブル

```sql
CREATE TABLE matches (
    match_id BIGINT PRIMARY KEY,
    game_id BIGINT NOT NULL,
    game_server_id BIGINT NOT NULL,
    status ENUM('waiting', 'in_progress', 'completed', 'cancelled') DEFAULT 'waiting',
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    INDEX idx_game_id_status (game_id, status),
    INDEX idx_game_server_id (game_server_id)
) ENGINE=InnoDB;
```

#### Match_Players テーブル

```sql
CREATE TABLE match_players (
    match_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    team_id INT,
    score INT DEFAULT 0,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (match_id, user_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ゲームライブラリ、ユーザー、マッチ情報の永続化
- **Redis**:
  - 理由: リアルタイムデータ、マッチメイキングキュー
  - 用途: マッチメイキングキュー、オンラインステータス

### スキーマ設計の考慮事項

1. **パーティショニング**: `matches`テーブルは`game_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: マッチは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### マッチメイキング

```
POST /api/v1/matches/join
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "game_id": 1234567890,
  "game_mode": "battle_royale"
}

Response (200 OK):
{
  "match_id": 9876543210,
  "game_server_url": "wss://game.epicgames.com/match/9876543210",
  "status": "matched"
}
```

#### ゲームサーバー接続

```
GET /api/v1/matches/{match_id}/connect
Authorization: Bearer <token>

Response (200 OK):
{
  "game_server_url": "wss://game.epicgames.com/match/9876543210",
  "session_token": "abc123"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Epic Account統合
- **認可**: ユーザーは購入したゲームのみプレイ可能
- **レート制限**: 
  - マッチメイキング: 10回/分
  - ゲームダウンロード: 無制限

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

**シャーディング戦略**: Game IDベースのシャーディング

```
Shard 1: game_id % 4 == 0
Shard 2: game_id % 4 == 1
Shard 3: game_id % 4 == 2
Shard 4: game_id % 4 == 3
```

**シャーディングキー**: `game_id`
- マッチは`game_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ゲームファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ゲームメタデータ、マッチメイキングキュー、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ゲームファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **マッチメイキング**: 適切なマッチの検索
2. **ゲームサーバー接続**: 低レイテンシが必要
3. **ゲームダウンロード**: 大きなファイルサイズ

### CDNの活用

- **ゲームファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### マッチメイキング最適化

1. **スキルベースマッチング**: ユーザーのスキルレベルに基づいたマッチング
2. **地理的マッチング**: ユーザーの地理的位置に基づいたマッチング
3. **事前計算**: マッチ候補を事前計算

### 非同期処理

#### メッセージキュー（Kafka）

1. **マッチメイキング**:
   ```
   Topic: match-making-requests
   Partition Key: game_id
   ```

2. **ゲームサーバー管理**:
   ```
   Topic: game-server-management
   Partition Key: game_server_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 6億人
- **日間アクティブユーザー**: 2.5億人
- **1日の同時接続ユーザー**: 1,000万人（ピーク時）

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**ゲームサーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 5,000台（動的スケーリング）
- コスト: $0.34/時間 × 5,000台 × 730時間 = **$1,241,000/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**ストレージ（S3）**:
- ゲームファイルストレージ: 100 PB
- コスト: $0.023/GB/月 × 100,000,000 GB = **$2,300,000/月**

**ネットワーク**:
- データ転送: 50 PB/月
- コスト: $0.09/GB × 50,000,000 GB = **$4,500,000/月**

**合計**: 約 **$8,221,675/月**（約98,660,100ドル/年）

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

2. **ゲームファイルバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Epic Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは購入したゲームのみアクセス可能

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
- **マッチメイキング**: < 10秒
- **ゲームサーバー接続**: < 2秒

### プログレッシブローディング

1. **ゲームライブラリの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのゲームはスクロール時に読み込み

2. **マッチメイキング進捗表示**:
   - リアルタイムでマッチメイキング進捗を表示

## 12. 実装例

### マッチメイキングサービス（疑似コード）

```python
class MatchMakingService:
    def __init__(self, db, cache, game_server_manager):
        self.db = db
        self.cache = cache
        self.game_server_manager = game_server_manager
    
    async def join_match(self, user_id: int, game_id: int, game_mode: str):
        # ユーザーのスキルレベルを取得
        user_skill = await self.db.get_user_skill(user_id=user_id, game_id=game_id)
        
        # マッチメイキングキューに追加
        await self.cache.lpush(
            f"match_queue:{game_id}:{game_mode}",
            json.dumps({
                "user_id": user_id,
                "skill_level": user_skill,
                "timestamp": time.time()
            })
        )
        
        # 適切なマッチを検索
        match = await self.find_match(game_id=game_id, game_mode=game_mode, user_skill=user_skill)
        
        if match:
            # ゲームサーバーを割り当て
            game_server = await self.game_server_manager.allocate_server(
                game_id=game_id,
                match_id=match["match_id"]
            )
            
            return {
                "match_id": match["match_id"],
                "game_server_url": game_server["url"],
                "status": "matched"
            }
        else:
            return {
                "status": "waiting",
                "estimated_wait_time": 30
            }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のゲームライブラリアクセス**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日のマッチ作成数**: 500万マッチ
- **1時間あたり**: 500万 / 24 = 約20.8万マッチ
- **1秒あたり**: 20.8万 / 3600 = 約58マッチ/秒
- **ピーク時（3倍）**: 約174マッチ/秒

### ストレージ見積もり

#### ゲームファイルストレージ

- **1ゲームあたりの平均サイズ**: 15 GB
- **ゲームライブラリ**: 1,000タイトル
- **合計ストレージ**: 1,000 × 15 GB = 15 TB
- **複数バージョン**: 15 TB × 2バージョン = 30 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **ゲームサーバー**: マルチプレイヤーゲーム用の専用サーバー
4. **マッチメイキング**: スキルベースと地理的マッチング
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **マッチメイキングのレイテンシ**:
   - 問題: マッチメイキングが遅い
   - 解決策: スキルベースマッチングと事前計算

2. **ゲームサーバーのスケーラビリティ**:
   - 問題: ゲームサーバーのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

## 15. 関連システム

### 類似システムへのリンク

- [Steam](steam_design.md) - ゲーム配信プラットフォーム
- [PlayStation Network](playstation_network_design.md) - コンソールゲームプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Realtime Systems](../15_realtime_systems/zoom_design.md) - リアルタイムシステム

---

**次のステップ**: [PlayStation Network](playstation_network_design.md)でコンソールゲームプラットフォームの設計を学ぶ

