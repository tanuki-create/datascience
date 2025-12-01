# Steam システム設計

## 1. システム概要

### 目的と主要機能

Steamは、Valveが提供するデジタルゲーム配信プラットフォームです。ゲームの購入、ダウンロード、インストール、更新、マルチプレイヤー機能を提供します。

**主要機能**:
- ゲームの購入・ダウンロード
- ゲームライブラリ管理
- フレンド機能
- チャット・ボイスチャット
- ゲームストリーミング
- ワークショップ（MOD配布）
- レビュー・評価

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1.3億人
- **日間アクティブユーザー（DAU）**: 約6,000万人
- **1日のゲームダウンロード数**: 約1,000万回
- **1日の同時接続ユーザー**: 約3,000万人（ピーク時）
- **1秒あたりのリクエスト数**: 約20,000リクエスト/秒（ピーク時）
- **ゲームライブラリ**: 約5万タイトル

### 主要なユースケース

1. **ゲーム購入**: ユーザーがゲームを購入
2. **ゲームダウンロード**: ユーザーがゲームをダウンロード
3. **フレンド機能**: ユーザーがフレンドを追加・管理
4. **ゲームストリーミング**: ユーザーがゲームをストリーミング
5. **ワークショップ**: ユーザーがMODをアップロード・ダウンロード

## 2. 機能要件

### コア機能

1. **ゲーム配信**
   - ゲームの購入・ダウンロード
   - ゲームの更新・パッチ配信
   - ゲームライブラリ管理

2. **フレンド機能**
   - フレンドの追加・削除
   - オンラインステータス表示
   - チャット・ボイスチャット

3. **ゲームストリーミング**
   - リモートプレイ
   - ゲームのストリーミング配信

4. **ワークショップ**
   - MODのアップロード・ダウンロード
   - コミュニティコンテンツの配布

5. **決済処理**
   - クレジットカード決済
   - Steamウォレット

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ゲームライブラリは強い一貫性、ダウンロードは最終的に一貫性を保つ
- **パフォーマンス**:
  - ゲームダウンロード開始: < 5秒
  - ゲームストリーミング開始: < 3秒
  - フレンドリスト表示: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ゲームファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: ゲーム購入・ダウンロード、フレンド機能、ゲームライブラリ
2. **P1（重要）**: ゲームストリーミング、ワークショップ、決済処理
3. **P2（望ましい）**: レビュー・評価、高度なストリーミング機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Steam Client, Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS
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
│  │ Game     │  │  Friend  │  │ Streaming│        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Workshop Service                │         │
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
│         Object Storage (S3)                        │
│         CDN (CloudFront/Cloudflare)               │
│         Game Distribution Servers                 │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Game Service**: ゲームの管理・配信
   - **Friend Service**: フレンド機能の管理
   - **Streaming Service**: ゲームストリーミングの処理
   - **Workshop Service**: ワークショップの管理
   - **Payment Service**: 決済処理
4. **Database**: ゲームライブラリ、ユーザー、フレンドの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（ダウンロード通知など）
7. **Object Storage**: ゲームファイルの保存
8. **CDN**: ゲームファイルの配信
9. **Game Distribution Servers**: ゲーム配信用の専用サーバー

### データフロー

#### ゲームダウンロードのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Game Service
3. Game Service:
   a. ユーザーの購入履歴を確認
   b. CDNからゲームファイルをダウンロード
   c. ダウンロード進捗を記録
   d. ダウンロード完了時に通知を送信
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
    INDEX idx_publisher_id (publisher_id),
    FULLTEXT INDEX idx_game_name (game_name)
) ENGINE=InnoDB;
```

#### User_Games テーブル

```sql
CREATE TABLE user_games (
    user_id BIGINT NOT NULL,
    game_id BIGINT NOT NULL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    play_time INT DEFAULT 0,
    last_played TIMESTAMP,
    PRIMARY KEY (user_id, game_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    INDEX idx_user_id (user_id),
    INDEX idx_game_id (game_id)
) ENGINE=InnoDB;
```

#### Friends テーブル

```sql
CREATE TABLE friends (
    user_id_1 BIGINT NOT NULL,
    user_id_2 BIGINT NOT NULL,
    status ENUM('pending', 'accepted', 'blocked') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id_1, user_id_2),
    FOREIGN KEY (user_id_1) REFERENCES users(user_id),
    FOREIGN KEY (user_id_2) REFERENCES users(user_id),
    INDEX idx_user_id_1 (user_id_1),
    INDEX idx_user_id_2 (user_id_2)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ゲームライブラリ、ユーザー、フレンドの永続化
- **Object Storage（S3）**:
  - 理由: 大規模ファイルストレージ、水平スケーリング
  - 用途: ゲームファイルの保存

### スキーマ設計の考慮事項

1. **パーティショニング**: `user_games`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: プレイ時間は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ゲーム購入

```
POST /api/v1/games/{game_id}/purchase
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "payment_method": "credit_card"
}

Response (200 OK):
{
  "purchase_id": 1234567890,
  "game_id": 9876543210,
  "status": "completed",
  "download_url": "https://cdn.steam.com/..."
}
```

#### ゲームダウンロード

```
GET /api/v1/games/{game_id}/download
Authorization: Bearer <token>
Range: bytes=0-

Response (206 Partial Content):
[Game File Data Stream]
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Steam Account統合
- **認可**: ユーザーは購入したゲームのみダウンロード可能
- **レート制限**: 
  - ゲームダウンロード: 無制限
  - フレンド追加: 100回/日

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
- ゲームライブラリは`user_id`でシャーディング

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
   - 用途: ゲームメタデータ、フレンドリスト、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ゲームファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ゲームダウンロード**: 大きなファイルサイズ
2. **ゲームストリーミング**: 低レイテンシが必要
3. **フレンドリスト**: 大量のフレンド情報

### CDNの活用

- **ゲームファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ゲームダウンロード最適化

1. **チャンクダウンロード**: 大きなファイルをチャンクに分割
2. **並列ダウンロード**: 複数のチャンクを並列でダウンロード
3. **レジューム機能**: ダウンロード中断時の再開

### 非同期処理

#### メッセージキュー（Kafka）

1. **ダウンロード通知**:
   ```
   Topic: download-notifications
   Partition Key: user_id
   ```

2. **ゲーム更新**:
   ```
   Topic: game-updates
   Partition Key: game_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1.3億人
- **日間アクティブユーザー**: 6,000万人
- **1日のゲームダウンロード数**: 1,000万回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 600台（リージョン間で分散）
- コスト: $0.192/時間 × 600台 × 730時間 = **$84,096/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**ストレージ（S3）**:
- ゲームファイルストレージ: 200 PB
- コスト: $0.023/GB/月 × 200,000,000 GB = **$4,600,000/月**

**ネットワーク**:
- データ転送: 100 PB/月
- コスト: $0.09/GB × 100,000,000 GB = **$9,000,000/月**

**合計**: 約 **$13,716,508/月**（約164,598,096ドル/年）

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
   - データベースの接続チェック

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
   - Steam Account統合

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
- **ゲームダウンロード開始**: < 5秒
- **ゲームストリーミング開始**: < 3秒

### プログレッシブローディング

1. **ゲームライブラリの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのゲームはスクロール時に読み込み

2. **ダウンロード進捗表示**:
   - リアルタイムでダウンロード進捗を表示

## 12. 実装例

### ゲームサービス（疑似コード）

```python
class GameService:
    def __init__(self, db, cache, cdn, message_queue):
        self.db = db
        self.cache = cache
        self.cdn = cdn
        self.message_queue = message_queue
    
    async def download_game(self, user_id: int, game_id: int):
        # ユーザーがゲームを購入しているか確認
        has_game = await self.db.check_user_game(user_id=user_id, game_id=game_id)
        
        if not has_game:
            raise PermissionError("User does not own this game")
        
        # ゲームメタデータを取得
        game = await self.db.get_game(game_id=game_id)
        
        # CDNからダウンロードURLを取得
        download_url = await self.cdn.get_download_url(
            game_id=game_id,
            user_id=user_id
        )
        
        # ダウンロード通知を送信（非同期）
        await self.message_queue.publish(
            topic="download-notifications",
            message={
                "user_id": user_id,
                "game_id": game_id,
                "download_url": download_url
            },
            partition_key=user_id
        )
        
        return {
            "game_id": game_id,
            "game_name": game["game_name"],
            "download_url": download_url,
            "file_size": game["file_size"]
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のゲームライブラリアクセス**: 5億回
- **1時間あたり**: 5億 / 24 = 約2,083万回
- **1秒あたり**: 2,083万 / 3600 = 約5,787回/秒
- **ピーク時（3倍）**: 約17,361回/秒

#### 書き込みトラフィック

- **1日のゲームダウンロード数**: 1,000万回
- **1時間あたり**: 1,000万 / 24 = 約41.7万回
- **1秒あたり**: 41.7万 / 3600 = 約116回/秒
- **ピーク時（3倍）**: 約348回/秒

### ストレージ見積もり

#### ゲームファイルストレージ

- **1ゲームあたりの平均サイズ**: 10 GB
- **ゲームライブラリ**: 5万タイトル
- **合計ストレージ**: 5万 × 10 GB = 500 TB
- **複数バージョン**: 500 TB × 2バージョン = 1 PB
- **5年のストレージ**: 約5 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **CDN活用**: ゲームファイルをCDN経由で配信
4. **チャンクダウンロード**: 大きなファイルをチャンクに分割
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **ゲームダウンロードのタイムアウト**:
   - 問題: 大きなファイルのダウンロードがタイムアウト
   - 解決策: チャンクダウンロードとレジューム機能

2. **ゲームストリーミングのレイテンシ**:
   - 問題: ゲームストリーミングのレイテンシが高い
   - 解決策: 地理的に分散したストリーミングサーバー

## 15. 関連システム

### 類似システムへのリンク

- [Epic Games](epic_games_design.md) - ゲーム配信プラットフォーム
- [PlayStation Network](playstation_network_design.md) - ゲーム配信プラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Epic Games](epic_games_design.md)でゲーム配信プラットフォームの設計を学ぶ

