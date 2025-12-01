# Pinterest システム設計

## 1. システム概要

### 目的と主要機能

Pinterestは、ユーザーが画像をピン留めして共有するソーシャルメディアプラットフォームです。ボード、ピン、検索などの機能を提供します。

**主要機能**:
- ピン作成・保存
- ボード作成・管理
- 画像検索
- レコメンデーション
- フォロー機能
- ショッピング機能
- 動画ピン

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約4.5億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日のピン作成数**: 約2億ピン
- **1日の検索数**: 約20億回
- **1秒あたりの検索数**: 約23,000検索/秒（ピーク時）

### 主要なユースケース

1. **ピン作成**: ユーザーがピンを作成
2. **ボード管理**: ユーザーがボードを作成・管理
3. **画像検索**: ユーザーが画像を検索
4. **レコメンデーション**: ユーザーにピンを推薦
5. **ショッピング**: ユーザーが商品を購入

## 2. 機能要件

### コア機能

1. **ピン管理**
   - ピンの作成・保存
   - ピンの編集・削除
   - ピンの共有

2. **ボード管理**
   - ボードの作成・編集・削除
   - ボードへのピン追加
   - ボードの共有

3. **検索**
   - 画像検索
   - テキスト検索
   - 視覚的検索（画像で検索）

4. **レコメンデーション**
   - パーソナライズされたピン推薦
   - 関連ピンの推薦
   - トレンドピンの表示

5. **ショッピング**
   - 商品ピン
   - 購入リンク
   - 価格情報

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ピン、ボードは最終的に一貫性を保つ
- **パフォーマンス**:
  - ピン作成: < 2秒
  - 画像検索: < 1秒
  - レコメンデーション生成: < 500ms
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ピン、ボードは永続的に保存

### 優先順位付け

1. **P0（必須）**: ピン作成、ボード管理、画像検索
2. **P1（重要）**: レコメンデーション、フォロー機能、ショッピング
3. **P2（望ましい）**: 動画ピン、高度な検索機能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
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
│  │ Pin      │  │ Board    │  │ Search   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  │          │  │          │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Recommendation Service         │         │
│  │      Image Processing Service       │         │
│  │      Shopping Service              │         │
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
│         (Image files)                            │
│         CDN (CloudFront/Cloudflare)              │
│         Search Index (Elasticsearch)            │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Pin Service**: ピンの管理
   - **Board Service**: ボードの管理
   - **Search Service**: 検索処理
   - **Recommendation Service**: レコメンデーション生成
   - **Image Processing Service**: 画像処理（リサイズ、サムネイル生成）
   - **Shopping Service**: ショッピング機能
4. **Database**: ピン、ボード、ユーザーの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（画像処理、レコメンデーション生成など）
7. **Object Storage**: 画像ファイルの保存
8. **CDN**: 画像ファイルの配信
9. **Search Index**: Elasticsearchを使用した検索インデックス

### データフロー

#### ピン作成のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Pin Service
3. Pin Service:
   a. 画像をObject Storageにアップロード
   b. 画像処理を非同期で実行（リサイズ、サムネイル生成）
   c. ピンメタデータをデータベースに保存
   d. 検索インデックスを更新（非同期）
   e. レコメンデーションを更新（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Pins テーブル

```sql
CREATE TABLE pins (
    pin_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    board_id BIGINT,
    image_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    title VARCHAR(500),
    description TEXT,
    link_url VARCHAR(500),
    pin_type ENUM('image', 'video', 'product') DEFAULT 'image',
    like_count INT DEFAULT 0,
    repin_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (board_id) REFERENCES boards(board_id),
    INDEX idx_user_id_created_at (user_id, created_at DESC),
    INDEX idx_board_id_created_at (board_id, created_at DESC),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_title_description (title, description)
) ENGINE=InnoDB;
```

#### Boards テーブル

```sql
CREATE TABLE boards (
    board_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    board_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    pin_count INT DEFAULT 0,
    follower_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Pin_Likes テーブル

```sql
CREATE TABLE pin_likes (
    pin_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (pin_id, user_id),
    FOREIGN KEY (pin_id) REFERENCES pins(pin_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id),
    INDEX idx_pin_id (pin_id)
) ENGINE=InnoDB;
```

#### User_Follows テーブル

```sql
CREATE TABLE user_follows (
    follower_id BIGINT NOT NULL,
    followee_id BIGINT NOT NULL,
    followed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (followee_id) REFERENCES users(user_id),
    INDEX idx_follower_id (follower_id),
    INDEX idx_followee_id (followee_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ピン、ボード、ユーザーの永続化
- **Elasticsearch**:
  - 理由: 全文検索、画像検索、レコメンデーション
  - 用途: 検索インデックス、レコメンデーション
- **Redis**:
  - 理由: リアルタイムデータ、オンラインステータス
  - 用途: オンラインステータス、セッション情報、キャッシュ

### スキーマ設計の考慮事項

1. **パーティショニング**: `pins`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: ピン、ボードは時系列で保存
4. **全文検索**: Elasticsearchを使用した全文検索

## 5. API設計

### 主要なAPIエンドポイント

#### ピン作成

```
POST /api/v1/pins
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "board_id": 1234567890,
  "image": <file>,
  "title": "My Pin",
  "description": "Description",
  "link_url": "https://example.com"
}

Response (201 Created):
{
  "pin_id": 9876543210,
  "image_url": "https://cdn.pinterest.com/...",
  "thumbnail_url": "https://cdn.pinterest.com/...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 画像検索

```
GET /api/v1/search?q=recipe&type=image
Authorization: Bearer <token>

Response (200 OK):
{
  "pins": [
    {
      "pin_id": 1234567890,
      "image_url": "https://cdn.pinterest.com/...",
      "title": "Recipe",
      "like_count": 1000
    }
  ],
  "total": 10000,
  "page": 1,
  "per_page": 20
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Pinterest Account統合
- **認可**: ユーザーは自分のピン・ボードのみ編集可能
- **レート制限**: 
  - ピン作成: 100回/分
  - 検索: 1,000回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### ピンのシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 16 == 0
Shard 2: user_id % 16 == 1
...
Shard 16: user_id % 16 == 15
```

**シャーディングキー**: `user_id`
- ピンは`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索インデックス**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 画像ファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ピンメタデータ、ボード情報、オンラインステータス
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **画像検索**: 大量の画像の検索
2. **レコメンデーション生成**: リアルタイムレコメンデーション
3. **画像処理**: リサイズ、サムネイル生成

### 画像検索最適化

1. **Elasticsearch**: 全文検索インデックス
2. **画像特徴量**: 画像特徴量を事前に抽出
3. **キャッシング**: 検索結果をキャッシュ

### レコメンデーション最適化

1. **事前計算**: レコメンデーションを事前に計算
2. **キャッシング**: レコメンデーションをキャッシュ
3. **非同期処理**: レコメンデーション生成を非同期で処理

### 画像処理最適化

1. **非同期処理**: 画像処理を非同期で処理
2. **複数解像度**: 複数の解像度を事前に生成
3. **CDN**: 画像をCDNで配信

### CDNの活用

- **画像ファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **画像処理**:
   ```
   Topic: image-processing
   Partition Key: pin_id
   ```

2. **レコメンデーション生成**:
   ```
   Topic: recommendation-generation
   Partition Key: user_id
   ```

3. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: pin_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 4.5億人
- **日間アクティブユーザー**: 2億人
- **1日のピン作成数**: 2億ピン

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 2,500台（リージョン間で分散）
- コスト: $0.192/時間 × 2,500台 × 730時間 = **$350,400/月**

**画像処理サーバー**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（動的スケーリング）
- コスト: $0.34/時間 × 1,000台 × 730時間 = **$248,200/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 300台（マスター + レプリカ）
- コスト: $0.76/時間 × 300台 × 730時間 = **$166,440/月**

**検索インデックス（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 200台
- コスト: $0.76/時間 × 200台 × 730時間 = **$110,960/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 400台
- コスト: $0.175/時間 × 400台 × 730時間 = **$51,100/月**

**ストレージ（S3）**:
- 画像ファイルストレージ: 1,000 PB
- コスト: $0.023/GB/月 × 1,000,000,000 GB = **$23,000,000/月**

**ネットワーク**:
- データ転送: 500 PB/月
- コスト: $0.09/GB × 500,000,000 GB = **$45,000,000/月**

**合計**: 約 **$68,926,100/月**（約827,113,200ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減
6. **画像最適化**: 画像の圧縮と最適化

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - 検索インデックスのヘルスチェック

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

2. **画像ファイルバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Pinterest Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のピン・ボードのみ編集可能

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
- **ピン作成**: < 2秒
- **画像検索**: < 1秒
- **レコメンデーション生成**: < 500ms

### プログレッシブローディング

1. **ピン一覧の遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのピンはスクロール時に読み込み

2. **画像の遅延読み込み**:
   - サムネイルを先に表示
   - フルサイズ画像は必要時に読み込み

## 12. 実装例

### ピンサービス（疑似コード）

```python
class PinService:
    def __init__(self, db, cache, storage, image_processor, 
                 message_queue, search_index):
        self.db = db
        self.cache = cache
        self.storage = storage
        self.image_processor = image_processor
        self.message_queue = message_queue
        self.search_index = search_index
    
    async def create_pin(self, user_id: int, board_id: int, 
                        image_file: bytes, title: str, description: str):
        # 画像をストレージにアップロード
        image_url = await self.storage.upload(image_file)
        
        # ピンメタデータを保存
        pin_id = await self.db.insert_pin(
            user_id=user_id,
            board_id=board_id,
            image_url=image_url,
            title=title,
            description=description
        )
        
        # 画像処理を非同期で実行
        await self.message_queue.publish(
            topic="image-processing",
            message={
                "pin_id": pin_id,
                "image_url": image_url
            },
            partition_key=pin_id
        )
        
        # 検索インデックスを更新（非同期）
        await self.message_queue.publish(
            topic="search-index-update",
            message={
                "pin_id": pin_id,
                "title": title,
                "description": description
            },
            partition_key=pin_id
        )
        
        # レコメンデーションを更新（非同期）
        await self.message_queue.publish(
            topic="recommendation-generation",
            message={
                "user_id": user_id,
                "pin_id": pin_id
            },
            partition_key=user_id
        )
        
        return {
            "pin_id": pin_id,
            "image_url": image_url,
            "created_at": datetime.now()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のピン読み込み**: 100億回
- **1時間あたり**: 100億 / 24 = 約4.17億回
- **1秒あたり**: 4.17億 / 3600 = 約115,833回/秒
- **ピーク時（3倍）**: 約347,499回/秒

#### 書き込みトラフィック

- **1日のピン作成数**: 2億ピン
- **1時間あたり**: 2億 / 24 = 約833万回
- **1秒あたり**: 833万 / 3600 = 約2,315回/秒
- **ピーク時（3倍）**: 約6,945回/秒

### ストレージ見積もり

#### 画像ファイルストレージ

- **1ピンあたりの平均画像サイズ**: 500 KB
- **1日のピン作成数**: 2億ピン
- **1日のストレージ**: 2億 × 500 KB = 100 TB
- **1年のストレージ**: 100 TB × 365 = 36.5 PB
- **累積ストレージ**: 約1,000 PB（過去のピンを含む）

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **検索インデックス**: Elasticsearchを使用した検索
4. **画像最適化**: 画像の圧縮と最適化
5. **レコメンデーション**: 事前計算とキャッシング
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **画像検索のスケーラビリティ**:
   - 問題: 大量の画像の検索が遅い
   - 解決策: Elasticsearchと画像特徴量の事前抽出

2. **レコメンデーション生成のレイテンシ**:
   - 問題: レコメンデーション生成が遅い
   - 解決策: 事前計算とキャッシング

3. **ストレージコスト**:
   - 問題: 画像ファイルのストレージコストが高い
   - 解決策: 画像の圧縮と最適化、CDN活用

## 15. 関連システム

### 類似システムへのリンク

- [Instagram](instagram_design.md) - 写真共有プラットフォーム
- [Twitter](twitter_design.md) - ソーシャルメディア
- [Facebook](facebook_design.md) - ソーシャルネットワーク

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [GitHub](../19_developer_tools/github_design.md)で開発者ツールの設計を学ぶ

