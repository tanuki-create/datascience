# PlayStation Network システム設計

## 1. システム概要

### 目的と主要機能

PlayStation Network（PSN）は、Sonyが提供するコンソールゲームプラットフォームです。PlayStationコンソール向けのゲーム配信、マルチプレイヤー機能を提供します。

**主要機能**:
- ゲームの購入・ダウンロード
- PlayStation Store
- マルチプレイヤー機能
- トロフィーシステム
- フレンド機能
- メッセージング
- PlayStation Plus（サブスクリプション）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.1億人
- **日間アクティブユーザー（DAU）**: 約5,000万人
- **1日の同時接続ユーザー**: 約2,000万人（ピーク時）
- **1日のゲームダウンロード数**: 約800万回
- **1秒あたりのリクエスト数**: 約15,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ゲーム購入**: ユーザーがゲームを購入
2. **ゲームダウンロード**: ユーザーがゲームをダウンロード
3. **マルチプレイヤー**: ユーザーがマルチプレイヤーゲームをプレイ
4. **トロフィー**: ユーザーがトロフィーを獲得
5. **フレンド機能**: ユーザーがフレンドを追加・管理

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

3. **トロフィーシステム**
   - トロフィーの獲得・表示
   - トロフィーの同期

4. **フレンド機能**
   - フレンドの追加・削除
   - オンラインステータス表示
   - パーティー機能

5. **PlayStation Plus**
   - サブスクリプション管理
   - 無料ゲームの配布

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
2. **P1（重要）**: トロフィーシステム、フレンド機能、PlayStation Plus
3. **P2（望ましい）**: 高度なマルチプレイヤー機能、統計・リーダーボード

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (PlayStation Console)
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
│  │ Game     │  │ Match    │  │ Trophy  │        │
│  │ Service  │  │ Making   │  │ Service │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Game Server Manager             │         │
│  │      Subscription Service           │         │
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
   - **Trophy Service**: トロフィーシステムの管理
   - **Game Server Manager**: ゲームサーバーの管理
   - **Subscription Service**: PlayStation Plusの管理
4. **Database**: ゲームライブラリ、ユーザー、トロフィーの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（トロフィー同期など）
7. **Object Storage**: ゲームファイルの保存
8. **Game Servers**: マルチプレイヤーゲーム用の専用サーバー
9. **CDN**: ゲームファイルの配信

### データフロー

#### トロフィー獲得のフロー

```
1. Client (PlayStation) → Load Balancer → API Gateway
2. API Gateway → Trophy Service
3. Trophy Service:
   a. トロフィー獲得をデータベースに保存
   - トロフィーを同期（非同期）
   - フレンドに通知を送信（非同期）
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_developer_id (developer_id),
    FULLTEXT INDEX idx_game_name (game_name)
) ENGINE=InnoDB;
```

#### Trophies テーブル

```sql
CREATE TABLE trophies (
    trophy_id BIGINT PRIMARY KEY,
    game_id BIGINT NOT NULL,
    trophy_name VARCHAR(200) NOT NULL,
    trophy_type ENUM('bronze', 'silver', 'gold', 'platinum') NOT NULL,
    description TEXT,
    rarity_percentage DECIMAL(5, 2),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    INDEX idx_game_id (game_id),
    INDEX idx_trophy_type (trophy_type)
) ENGINE=InnoDB;
```

#### User_Trophies テーブル

```sql
CREATE TABLE user_trophies (
    user_id BIGINT NOT NULL,
    trophy_id BIGINT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, trophy_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (trophy_id) REFERENCES trophies(trophy_id),
    INDEX idx_user_id (user_id),
    INDEX idx_trophy_id (trophy_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ゲームライブラリ、ユーザー、トロフィーの永続化
- **Redis**:
  - 理由: リアルタイムデータ、マッチメイキングキュー
  - 用途: マッチメイキングキュー、オンラインステータス

### スキーマ設計の考慮事項

1. **パーティショニング**: `user_trophies`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: トロフィー獲得は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### トロフィー獲得

```
POST /api/v1/trophies/{trophy_id}/earn
Authorization: Bearer <token>

Response (200 OK):
{
  "trophy_id": 1234567890,
  "trophy_name": "First Victory",
  "trophy_type": "gold",
  "earned_at": "2024-01-15T10:30:00Z"
}
```

#### トロフィー一覧取得

```
GET /api/v1/users/{user_id}/trophies?game_id=9876543210
Authorization: Bearer <token>

Response (200 OK):
{
  "trophies": [
    {
      "trophy_id": 1234567890,
      "trophy_name": "First Victory",
      "trophy_type": "gold",
      "earned_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_trophies": 50,
  "earned_trophies": 25
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、PlayStation Account統合
- **認可**: ユーザーは自分のトロフィーのみアクセス可能
- **レート制限**: 
  - トロフィー獲得: 100回/分
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

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- トロフィーは`user_id`でシャーディング

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
   - 用途: ゲームメタデータ、トロフィー情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ゲームファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **トロフィー同期**: 大量のトロフィーデータの同期
2. **ゲームサーバー接続**: 低レイテンシが必要
3. **ゲームダウンロード**: 大きなファイルサイズ

### CDNの活用

- **ゲームファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### トロフィー同期最適化

1. **バッチ同期**: 複数のトロフィーをバッチで同期
2. **キャッシング**: トロフィー情報をキャッシュ
3. **非同期処理**: トロフィー同期を非同期で処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **トロフィー同期**:
   ```
   Topic: trophy-sync
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

- **月間アクティブユーザー**: 1.1億人
- **日間アクティブユーザー**: 5,000万人
- **1日の同時接続ユーザー**: 2,000万人（ピーク時）

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 800台（リージョン間で分散）
- コスト: $0.192/時間 × 800台 × 730時間 = **$112,128/月**

**ゲームサーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 3,000台（動的スケーリング）
- コスト: $0.34/時間 × 3,000台 × 730時間 = **$744,600/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**ストレージ（S3）**:
- ゲームファイルストレージ: 150 PB
- コスト: $0.023/GB/月 × 150,000,000 GB = **$3,450,000/月**

**ネットワーク**:
- データ転送: 80 PB/月
- コスト: $0.09/GB × 80,000,000 GB = **$7,200,000/月**

**合計**: 約 **$12,139,140/月**（約145,669,680ドル/年）

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
   - PlayStation Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のトロフィーのみアクセス可能

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

2. **トロフィー一覧の遅延読み込み**:
   - 最初の50件を先に表示
   - 残りのトロフィーはスクロール時に読み込み

## 12. 実装例

### トロフィーサービス（疑似コード）

```python
class TrophyService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def earn_trophy(self, user_id: int, trophy_id: int):
        # トロフィーを獲得
        await self.db.insert_user_trophy(
            user_id=user_id,
            trophy_id=trophy_id
        )
        
        # トロフィー情報を取得
        trophy = await self.db.get_trophy(trophy_id=trophy_id)
        
        # トロフィー同期を非同期で処理
        await self.message_queue.publish(
            topic="trophy-sync",
            message={
                "user_id": user_id,
                "trophy_id": trophy_id,
                "trophy_type": trophy["trophy_type"]
            },
            partition_key=user_id
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"user:{user_id}:trophies")
        
        return {
            "trophy_id": trophy_id,
            "trophy_name": trophy["trophy_name"],
            "trophy_type": trophy["trophy_type"],
            "earned_at": datetime.now()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のゲームライブラリアクセス**: 8億回
- **1時間あたり**: 8億 / 24 = 約3,333万回
- **1秒あたり**: 3,333万 / 3600 = 約9,259回/秒
- **ピーク時（3倍）**: 約27,777回/秒

#### 書き込みトラフィック

- **1日のトロフィー獲得数**: 1億回
- **1時間あたり**: 1億 / 24 = 約416万回
- **1秒あたり**: 416万 / 3600 = 約1,156回/秒
- **ピーク時（3倍）**: 約3,468回/秒

### ストレージ見積もり

#### ゲームファイルストレージ

- **1ゲームあたりの平均サイズ**: 50 GB
- **ゲームライブラリ**: 5,000タイトル
- **合計ストレージ**: 5,000 × 50 GB = 250 TB
- **複数バージョン**: 250 TB × 2バージョン = 500 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **ゲームサーバー**: マルチプレイヤーゲーム用の専用サーバー
4. **トロフィーシステム**: リアルタイムトロフィー同期
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **トロフィー同期のスケーラビリティ**:
   - 問題: 大量のトロフィーデータの同期が遅い
   - 解決策: バッチ同期と非同期処理

2. **ゲームサーバーのスケーラビリティ**:
   - 問題: ゲームサーバーのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

## 15. 関連システム

### 類似システムへのリンク

- [Steam](steam_design.md) - PCゲームプラットフォーム
- [Epic Games](epic_games_design.md) - ゲーム配信プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Realtime Systems](../15_realtime_systems/zoom_design.md) - リアルタイムシステム

---

**次のステップ**: [Stripe](../12_payment_finance/stripe_design.md)で決済プラットフォームの設計を学ぶ

