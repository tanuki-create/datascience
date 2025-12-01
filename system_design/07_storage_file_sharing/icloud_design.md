# iCloud システム設計

## 1. システム概要

### 目的と主要機能

iCloudは、Appleが提供するクラウドストレージサービスです。ファイルの保存、共有、同期、Appleデバイス統合機能を提供します。

**主要機能**:
- ファイルのアップロード・ダウンロード
- ファイルの共有（リンク共有、ユーザー共有）
- リアルタイム同期
- Appleデバイス統合（iPhone、iPad、Mac）
- 写真・動画のバックアップ
- ファイル検索

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約8.5億人
- **日間アクティブユーザー（DAU）**: 約4億人
- **1日のファイルアップロード数**: 約8億ファイル
- **1日のファイルダウンロード数**: 約30億回
- **1秒あたりのリクエスト数**: 約25,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ファイルアップロード**: ユーザーがファイルをアップロード
2. **写真・動画バックアップ**: 自動バックアップ
3. **リアルタイム同期**: 複数デバイス間での同期
4. **ファイル共有**: ユーザーがファイルを共有
5. **ファイル検索**: ファイルの検索

## 2. 機能要件

### コア機能

1. **ファイル管理**
   - ファイルのアップロード・ダウンロード
   - ファイルの削除・移動・コピー
   - フォルダ管理

2. **写真・動画バックアップ**
   - 自動バックアップ
   - 写真ライブラリの同期
   - 動画ライブラリの同期

3. **共有機能**
   - リンク共有
   - ユーザー共有
   - 権限管理（閲覧、編集、コメント）

4. **同期機能**
   - リアルタイム同期
   - オフライン同期
   - 競合解決

5. **検索機能**
   - ファイル名検索
   - 全文検索
   - メタデータ検索

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: ファイルメタデータは強い一貫性、ファイル内容は最終的に一貫性を保つ
- **パフォーマンス**:
  - ファイルアップロード: < 30秒（開始）
  - ファイルダウンロード: < 2秒（開始）
  - ファイル検索: < 1秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: ファイルは永続的に保存

### 優先順位付け

1. **P0（必須）**: ファイルアップロード・ダウンロード、写真・動画バックアップ、同期
2. **P1（重要）**: 共有、検索、バージョン管理
3. **P2（望ましい）**: 高度な検索、オフライン対応

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (iOS, macOS, Web)
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
│  │ File     │  │  Photo   │  │  Sync   │        │
│  │ Service  │  │ Service  │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Share Service                   │         │
│  │      Search Service                  │         │
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
│         Search Index (Elasticsearch)              │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **File Service**: ファイルの管理
   - **Photo Service**: 写真・動画のバックアップ管理
   - **Sync Service**: 同期機能の管理
   - **Share Service**: ファイル共有の管理
   - **Search Service**: 検索機能の管理
4. **Database**: ファイルメタデータ、共有情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（同期、検索インデックス更新など）
7. **Object Storage**: ファイルの保存（S3）
8. **Search Index**: ファイル検索インデックス
9. **CDN**: ファイルの配信

### データフロー

#### 写真バックアップのフロー

```
1. Client (iOS) → Load Balancer → API Gateway
2. API Gateway → Photo Service
3. Photo Service:
   a. 写真メタデータをデータベースに保存
   b. 写真をObject Storageにアップロード
   c. Message Queueに同期イベントを送信
   d. Search Serviceに検索インデックス更新を依頼
```

## 4. データモデル設計

### 主要なエンティティ

#### Files テーブル

```sql
CREATE TABLE files (
    file_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_size BIGINT,
    parent_folder_id BIGINT,
    storage_url VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100),
    is_photo BOOLEAN DEFAULT FALSE,
    is_video BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_folder_id) REFERENCES folders(folder_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_folder_id (parent_folder_id),
    INDEX idx_is_photo (is_photo),
    FULLTEXT INDEX idx_file_name (file_name)
) ENGINE=InnoDB;
```

#### Photos テーブル

```sql
CREATE TABLE photos (
    photo_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    file_id BIGINT NOT NULL,
    photo_date TIMESTAMP,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    camera_model VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    INDEX idx_user_id_date (user_id, photo_date DESC),
    INDEX idx_location (location_lat, location_lng)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ファイルメタデータ、共有情報の永続化
- **Object Storage（S3）**:
  - 理由: 大規模ファイルストレージ、水平スケーリング
  - 用途: ファイルの保存
- **Elasticsearch**:
  - 理由: 全文検索、ファイル検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `files`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **バージョン管理**: ファイルのバージョンを管理

## 5. API設計

### 主要なAPIエンドポイント

#### ファイルアップロード

```
POST /api/v1/files/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "file": <file_data>,
  "parent_folder_id": 123,
  "name": "photo.jpg"
}

Response (200 OK):
{
  "file_id": 1234567890,
  "file_name": "photo.jpg",
  "file_size": 1024000,
  "storage_url": "https://s3.amazonaws.com/..."
}
```

#### 写真バックアップ

```
POST /api/v1/photos/backup
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "photos": [
    {
      "file_data": <base64_encoded>,
      "photo_date": "2024-01-15T10:30:00Z",
      "location": {
        "lat": 37.7749,
        "lng": -122.4194
      }
    }
  ]
}

Response (200 OK):
{
  "backed_up_count": 10,
  "failed_count": 0
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Apple ID統合
- **認可**: ユーザーは自分のファイルまたは共有されたファイルのみアクセス可能
- **レート制限**: 
  - ファイルアップロード: 100ファイル/分
  - 写真バックアップ: 1,000写真/分

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
- ファイルは`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ファイルをCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: ファイルメタデータ、共有情報
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: ファイル、写真
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ファイルアップロード**: 大きなファイルサイズ
2. **写真バックアップ**: 大量の写真のアップロード
3. **検索**: Elasticsearchクエリの最適化

### CDNの活用

- **ファイル・写真**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ファイル転送最適化

1. **チャンクアップロード**: 大きなファイルをチャンクに分割
2. **並列アップロード**: 複数のチャンクを並列でアップロード
3. **レジューム機能**: アップロード中断時の再開
4. **写真最適化**: 写真の圧縮とサムネイル生成

### 非同期処理

#### メッセージキュー（Kafka）

1. **同期イベント**:
   ```
   Topic: sync-events
   Partition Key: user_id
   ```

2. **写真バックアップ**:
   ```
   Topic: photo-backup
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 8.5億人
- **日間アクティブユーザー**: 4億人
- **1日のファイルアップロード数**: 8億ファイル

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,200台（リージョン間で分散）
- コスト: $0.192/時間 × 1,200台 × 730時間 = **$168,192/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 60台（マスター + レプリカ）
- コスト: $0.76/時間 × 60台 × 730時間 = **$33,288/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 120台
- コスト: $0.175/時間 × 120台 × 730時間 = **$15,330/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 25台
- コスト: $0.76/時間 × 25台 × 730時間 = **$13,870/月**

**ストレージ（S3）**:
- ファイルストレージ: 40 PB
- コスト: $0.023/GB/月 × 40,000,000 GB = **$920,000/月**

**ネットワーク**:
- データ転送: 15 PB/月
- コスト: $0.09/GB × 15,000,000 GB = **$1,350,000/月**

**合計**: 約 **$2,500,680/月**（約30,008,160ドル/年）

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

2. **ファイルバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Apple ID統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ファイルベースのアクセス制御

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
- **ファイルアップロード**: < 30秒（開始）
- **ファイルダウンロード**: < 2秒（開始）

### プログレッシブローディング

1. **ファイルの遅延読み込み**:
   - ビューポートに入るまでファイルを読み込まない
   - サムネイルを先に表示

2. **写真の遅延読み込み**:
   - 写真ライブラリの遅延読み込み
   - サムネイルを先に表示

## 12. 実装例

### 写真サービス（疑似コード）

```python
class PhotoService:
    def __init__(self, db, cache, object_storage, message_queue, search_service):
        self.db = db
        self.cache = cache
        self.object_storage = object_storage
        self.message_queue = message_queue
        self.search_service = search_service
    
    async def backup_photos(self, user_id: int, photos: list):
        backed_up_count = 0
        failed_count = 0
        
        for photo_data in photos:
            try:
                # 写真をObject Storageにアップロード
                storage_url = await self.object_storage.upload_file(
                    bucket="icloud-photos",
                    key=f"{user_id}/{uuid.uuid4()}.jpg",
                    file=photo_data['file_data']
                )
                
                # ファイルメタデータをデータベースに保存
                file_id = await self.db.insert_file(
                    user_id=user_id,
                    file_name=f"photo_{uuid.uuid4()}.jpg",
                    file_size=len(photo_data['file_data']),
                    storage_url=storage_url,
                    is_photo=True
                )
                
                # 写真メタデータを保存
                await self.db.insert_photo(
                    photo_id=file_id,
                    user_id=user_id,
                    file_id=file_id,
                    photo_date=photo_data.get('photo_date'),
                    location_lat=photo_data.get('location', {}).get('lat'),
                    location_lng=photo_data.get('location', {}).get('lng')
                )
                
                # 同期イベントを送信
                await self.message_queue.publish(
                    topic="sync-events",
                    message={
                        "file_id": file_id,
                        "user_id": user_id,
                        "action": "photo_backup"
                    },
                    partition_key=user_id
                )
                
                backed_up_count += 1
            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to backup photo: {e}")
        
        return {
            "backed_up_count": backed_up_count,
            "failed_count": failed_count
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のファイルダウンロード**: 30億回
- **1時間あたり**: 30億 / 24 = 約1.25億回
- **1秒あたり**: 1.25億 / 3600 = 約34,722回/秒
- **ピーク時（3倍）**: 約104,166回/秒

#### 書き込みトラフィック

- **1日のファイルアップロード数**: 8億ファイル
- **1時間あたり**: 8億 / 24 = 約3,333万ファイル
- **1秒あたり**: 3,333万 / 3600 = 約9,259ファイル/秒
- **ピーク時（3倍）**: 約27,777ファイル/秒

### ストレージ見積もり

#### ファイルストレージ

- **1ファイルあたりの平均サイズ**: 5 MB
- **1日のファイルアップロード数**: 8億ファイル
- **1日のストレージ**: 8億 × 5 MB = 4 PB
- **1年のストレージ**: 4 PB × 365 = 約1,460 PB
- **5年のストレージ**: 約7,300 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **Object Storage**: 大規模ファイルストレージにObject Storageを使用
4. **チャンクアップロード**: 大きなファイルをチャンクに分割
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **写真バックアップのスケーラビリティ**:
   - 問題: 大量の写真のアップロードでボトルネック
   - 解決策: バッチ処理と非同期処理

2. **同期の競合**:
   - 問題: 複数デバイスでの同時編集で競合が発生
   - 解決策: バージョン管理と競合解決アルゴリズム

## 15. 関連システム

### 類似システムへのリンク

- [Google Drive](google_drive_design.md) - ファイルストレージ
- [OneDrive](onedrive_design.md) - ファイルストレージ
- [Dropbox](dropbox_design.md) - ファイルストレージ

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Apple Music](../08_music_streaming/apple_music_design.md)で音楽ストリーミングシステムの設計を学ぶ

