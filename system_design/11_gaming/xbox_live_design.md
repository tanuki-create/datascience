# Xbox Live システム設計

## 1. システム概要

### 目的と主要機能

Xbox Liveは、Microsoftが提供するコンソールゲームプラットフォームです。Xboxコンソール向けのゲーム配信、マルチプレイヤー機能、Xbox Game Passを提供します。

**主要機能**:
- ゲームの購入・ダウンロード
- Microsoft Store
- マルチプレイヤー機能
- 実績システム（Achievements）
- フレンド機能
- メッセージング
- Xbox Game Pass（サブスクリプション）
- Xbox Cloud Gaming（クラウドゲーミング）

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.2億人
- **日間アクティブユーザー（DAU）**: 約6,000万人
- **1日の同時接続ユーザー**: 約2,500万人（ピーク時）
- **1日のゲームダウンロード数**: 約1,000万回
- **1秒あたりのリクエスト数**: 約18,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ゲーム購入**: ユーザーがゲームを購入
2. **ゲームダウンロード**: ユーザーがゲームをダウンロード
3. **マルチプレイヤー**: ユーザーがマルチプレイヤーゲームをプレイ
4. **実績獲得**: ユーザーが実績を獲得
5. **フレンド機能**: ユーザーがフレンドを追加・管理
6. **Xbox Game Pass**: ユーザーがサブスクリプションでゲームをプレイ
7. **Xbox Cloud Gaming**: ユーザーがクラウドでゲームをストリーミング

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

3. **実績システム**
   - 実績の獲得・表示
   - 実績の同期
   - Gamerscore（ゲーマースコア）

4. **フレンド機能**
   - フレンドの追加・削除
   - オンラインステータス表示
   - パーティー機能

5. **Xbox Game Pass**
   - サブスクリプション管理
   - 無料ゲームの配布
   - 新作ゲームの早期アクセス

6. **Xbox Cloud Gaming**
   - クラウドゲーミングストリーミング
   - 低レイテンシゲーミング
   - 複数デバイス対応

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ゲームライブラリは強い一貫性、マルチプレイヤーは最終的に一貫性を保つ
- **パフォーマンス**:
  - ゲームダウンロード開始: < 5秒
  - マッチメイキング: < 10秒
  - ゲームサーバー接続: < 2秒
  - クラウドゲーミングレイテンシ: < 50ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ゲームファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: ゲーム購入・ダウンロード、マルチプレイヤー、マッチメイキング
2. **P1（重要）**: 実績システム、フレンド機能、Xbox Game Pass
3. **P2（望ましい）**: Xbox Cloud Gaming、高度なマルチプレイヤー機能、統計・リーダーボード

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Xbox Console, PC, Mobile)
└──────┬──────┘
       │ HTTPS / WebSocket
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer (Azure Load Balancer) │
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
│  │ Game     │  │ Match    │  │Achievement│        │
│  │ Service  │  │ Making   │  │ Service  │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Game Server Manager             │         │
│  │      Subscription Service           │         │
│  │      Cloud Gaming Service           │         │
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
│         Object Storage (Azure Blob Storage)       │
│         Game Servers (Azure Virtual Machines)    │
│         Cloud Gaming Servers (Azure)             │
│         CDN (Azure CDN)                          │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Game Service**: ゲームの管理・配信
   - **Match Making Service**: マッチメイキングの処理
   - **Achievement Service**: 実績システムの管理
   - **Game Server Manager**: ゲームサーバーの管理
   - **Subscription Service**: Xbox Game Passの管理
   - **Cloud Gaming Service**: Xbox Cloud Gamingのストリーミング
4. **Database**: ゲームライブラリ、ユーザー、実績の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（実績同期など）
7. **Object Storage**: ゲームファイルの保存
8. **Game Servers**: マルチプレイヤーゲーム用の専用サーバー
9. **Cloud Gaming Servers**: Xbox Cloud Gaming用のストリーミングサーバー
10. **CDN**: ゲームファイルの配信

### データフロー

#### 実績獲得のフロー

```
1. Client (Xbox) → Load Balancer → API Gateway
2. API Gateway → Achievement Service
3. Achievement Service:
   a. 実績獲得をデータベースに保存
   b. Gamerscoreを更新
   c. 実績を同期（非同期）
   d. フレンドに通知を送信（非同期）
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
    game_pass_available BOOLEAN DEFAULT FALSE,
    cloud_gaming_available BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_developer_id (developer_id),
    INDEX idx_game_pass_available (game_pass_available),
    FULLTEXT INDEX idx_game_name (game_name)
) ENGINE=InnoDB;
```

#### Achievements テーブル

```sql
CREATE TABLE achievements (
    achievement_id BIGINT PRIMARY KEY,
    game_id BIGINT NOT NULL,
    achievement_name VARCHAR(200) NOT NULL,
    gamerscore INT NOT NULL,
    description TEXT,
    rarity_percentage DECIMAL(5, 2),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    INDEX idx_game_id (game_id),
    INDEX idx_gamerscore (gamerscore)
) ENGINE=InnoDB;
```

#### User_Achievements テーブル

```sql
CREATE TABLE user_achievements (
    user_id BIGINT NOT NULL,
    achievement_id BIGINT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id),
    INDEX idx_user_id (user_id),
    INDEX idx_achievement_id (achievement_id)
) ENGINE=InnoDB;
```

#### Users テーブル

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    gamertag VARCHAR(15) UNIQUE NOT NULL,
    gamerscore INT DEFAULT 0,
    xbox_game_pass_subscriber BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_gamertag (gamertag),
    INDEX idx_gamerscore (gamerscore)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（Azure SQL Database）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ゲームライブラリ、ユーザー、実績の永続化
- **Redis**:
  - 理由: リアルタイムデータ、マッチメイキングキュー
  - 用途: マッチメイキングキュー、オンラインステータス

### スキーマ設計の考慮事項

1. **パーティショニング**: `user_achievements`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 実績獲得は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 実績獲得

```
POST /api/v1/achievements/{achievement_id}/earn
Authorization: Bearer <token>

Response (200 OK):
{
  "achievement_id": 1234567890,
  "achievement_name": "First Victory",
  "gamerscore": 50,
  "earned_at": "2024-01-15T10:30:00Z",
  "total_gamerscore": 1250
}
```

#### 実績一覧取得

```
GET /api/v1/users/{user_id}/achievements?game_id=9876543210
Authorization: Bearer <token>

Response (200 OK):
{
  "achievements": [
    {
      "achievement_id": 1234567890,
      "achievement_name": "First Victory",
      "gamerscore": 50,
      "earned_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_achievements": 100,
  "earned_achievements": 50,
  "total_gamerscore": 2500
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Microsoft Account統合
- **認可**: ユーザーは自分の実績のみアクセス可能
- **レート制限**: 
  - 実績獲得: 100回/分
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

#### クラウドゲーミングサーバー

- **Azure Virtual Machines**: Xbox Cloud Gaming用のVM
- **GPU最適化**: GPU最適化VMを使用
- **低レイテンシ**: ユーザーに近いリージョンに配置

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- 実績は`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: Azure Load Balancer
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ゲームファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ゲームメタデータ、実績情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ゲームファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **実績同期**: 大量の実績データの同期
2. **ゲームサーバー接続**: 低レイテンシが必要
3. **ゲームダウンロード**: 大きなファイルサイズ
4. **クラウドゲーミング**: 超低レイテンシが必要

### CDNの活用

- **ゲームファイル**: Azure CDN
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 実績同期最適化

1. **バッチ同期**: 複数の実績をバッチで同期
2. **キャッシング**: 実績情報をキャッシュ
3. **非同期処理**: 実績同期を非同期で処理

### クラウドゲーミング最適化

1. **低レイテンシネットワーク**: Azureの低レイテンシネットワークを使用
2. **GPU最適化**: GPU最適化VMを使用
3. **地理的分散**: ユーザーに近いリージョンに配置

### 非同期処理

#### メッセージキュー（Kafka）

1. **実績同期**:
   ```
   Topic: achievement-sync
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

- **月間アクティブユーザー**: 1.2億人
- **日間アクティブユーザー**: 6,000万人
- **1日の同時接続ユーザー**: 2,500万人（ピーク時）

#### サーバーコスト（Azure）

**アプリケーションサーバー**:
- Azure Virtual Machines: Standard_D4s_v3 (4 vCPU, 16 GB RAM)
- インスタンス数: 900台（リージョン間で分散）
- コスト: $0.192/時間 × 900台 × 730時間 = **$126,144/月**

**ゲームサーバー**:
- Azure Virtual Machines: Standard_D8s_v3 (8 vCPU, 32 GB RAM)
- インスタンス数: 3,500台（動的スケーリング）
- コスト: $0.384/時間 × 3,500台 × 730時間 = **$981,120/月**

**クラウドゲーミングサーバー**:
- Azure Virtual Machines: Standard_NC6s_v3 (6 vCPU, 112 GB RAM, GPU)
- インスタンス数: 5,000台（動的スケーリング）
- コスト: $3.06/時間 × 5,000台 × 730時間 = **$11,169,000/月**

**データベース**:
- Azure SQL Database: Business Critical, Gen5, 8 vCores
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $2.04/時間 × 50台 × 730時間 = **$74,460/月**

**キャッシュ（Azure Cache for Redis）**:
- Premium P1 (6 GB RAM)
- インスタンス数: 100台
- コスト: $0.20/時間 × 100台 × 730時間 = **$14,600/月**

**ストレージ（Azure Blob Storage）**:
- ゲームファイルストレージ: 180 PB
- コスト: $0.018/GB/月 × 180,000,000 GB = **$3,240,000/月**

**ネットワーク**:
- データ転送: 100 PB/月
- コスト: $0.087/GB × 100,000,000 GB = **$8,700,000/月**

**合計**: 約 **$24,305,324/月**（約291,663,888ドル/年）

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
   - クラウドゲーミングサーバーのヘルスチェック

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
   - Azure Blob StorageのマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Microsoft Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分の実績のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ
   - Azure Blob Storage: サーバーサイド暗号化

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - ユーザーベースのレート制限

2. **CDN**: Azure DDoS Protection
3. **WAF**: Azure Application Gateway WAFで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **マッチメイキング**: < 10秒
- **ゲームサーバー接続**: < 2秒
- **クラウドゲーミングレイテンシ**: < 50ms

### プログレッシブローディング

1. **ゲームライブラリの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのゲームはスクロール時に読み込み

2. **実績一覧の遅延読み込み**:
   - 最初の50件を先に表示
   - 残りの実績はスクロール時に読み込み

## 12. 実装例

### 実績サービス（疑似コード）

```python
class AchievementService:
    def __init__(self, db, cache, message_queue):
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def earn_achievement(self, user_id: int, achievement_id: int):
        # 実績を獲得
        await self.db.insert_user_achievement(
            user_id=user_id,
            achievement_id=achievement_id
        )
        
        # 実績情報を取得
        achievement = await self.db.get_achievement(achievement_id=achievement_id)
        
        # Gamerscoreを更新
        await self.db.update_user_gamerscore(
            user_id=user_id,
            gamerscore_delta=achievement["gamerscore"]
        )
        
        # 実績同期を非同期で処理
        await self.message_queue.publish(
            topic="achievement-sync",
            message={
                "user_id": user_id,
                "achievement_id": achievement_id,
                "gamerscore": achievement["gamerscore"]
            },
            partition_key=user_id
        )
        
        # キャッシュを無効化
        await self.cache.delete(f"user:{user_id}:achievements")
        await self.cache.delete(f"user:{user_id}:gamerscore")
        
        return {
            "achievement_id": achievement_id,
            "achievement_name": achievement["achievement_name"],
            "gamerscore": achievement["gamerscore"],
            "earned_at": datetime.now()
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

- **1日の実績獲得数**: 1.2億回
- **1時間あたり**: 1.2億 / 24 = 約500万回
- **1秒あたり**: 500万 / 3600 = 約1,389回/秒
- **ピーク時（3倍）**: 約4,167回/秒

### ストレージ見積もり

#### ゲームファイルストレージ

- **1ゲームあたりの平均サイズ**: 60 GB
- **ゲームライブラリ**: 6,000タイトル
- **合計ストレージ**: 6,000 × 60 GB = 360 TB
- **複数バージョン**: 360 TB × 2バージョン = 720 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **ゲームサーバー**: マルチプレイヤーゲーム用の専用サーバー
4. **実績システム**: リアルタイム実績同期
5. **クラウドゲーミング**: 超低レイテンシネットワーク
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **実績同期のスケーラビリティ**:
   - 問題: 大量の実績データの同期が遅い
   - 解決策: バッチ同期と非同期処理

2. **ゲームサーバーのスケーラビリティ**:
   - 問題: ゲームサーバーのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

3. **クラウドゲーミングのレイテンシ**:
   - 問題: クラウドゲーミングのレイテンシが高い
   - 解決策: 低レイテンシネットワークとGPU最適化VM

## 15. 関連システム

### 類似システムへのリンク

- [Steam](steam_design.md) - PCゲームプラットフォーム
- [Epic Games](epic_games_design.md) - ゲーム配信プラットフォーム
- [PlayStation Network](playstation_network_design.md) - コンソールゲームプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Realtime Systems](../15_realtime_systems/zoom_design.md) - リアルタイムシステム

---

**次のステップ**: [Nintendo Switch Online](nintendo_switch_online_design.md)でコンソールゲームプラットフォームの設計を学ぶ

