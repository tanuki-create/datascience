# Google Drive システム設計

## 1. システム概要

### 目的と主要機能

Google Driveは、Googleが提供するクラウドストレージサービスです。ファイルの保存、共有、同期、コラボレーション機能を提供します。

**主要機能**:
- ファイルのアップロード・ダウンロード
- ファイルの共有（リンク共有、ユーザー共有）
- リアルタイム同期
- コラボレーション（Google Docs、Sheets、Slides）
- ファイル検索
- バージョン管理

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約10億人
- **日間アクティブユーザー（DAU）**: 約5億人
- **1日のファイルアップロード数**: 約10億ファイル
- **1日のファイルダウンロード数**: 約50億回
- **1秒あたりのリクエスト数**: 約30,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ファイルアップロード**: ユーザーがファイルをアップロード
2. **ファイル共有**: ユーザーがファイルを共有
3. **リアルタイム同期**: 複数デバイス間での同期
4. **コラボレーション**: 複数ユーザーでの同時編集
5. **ファイル検索**: ファイルの検索

## 2. 機能要件

### コア機能

1. **ファイル管理**
   - ファイルのアップロード・ダウンロード
   - ファイルの削除・移動・コピー
   - フォルダ管理

2. **共有機能**
   - リンク共有
   - ユーザー共有
   - 権限管理（閲覧、編集、コメント）

3. **同期機能**
   - リアルタイム同期
   - オフライン同期
   - 競合解決

4. **コラボレーション**
   - Google Docs、Sheets、Slidesの同時編集
   - リアルタイム共同編集

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

1. **P0（必須）**: ファイルアップロード・ダウンロード、共有、同期
2. **P1（重要）**: コラボレーション、検索、バージョン管理
3. **P2（望ましい）**: 高度な検索、オフライン対応

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps, Desktop)
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
│  │ File     │  │  Share   │  │  Sync    │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Collaboration Service            │         │
│  │      Search Service                   │         │
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
│         Object Storage (GCS)                      │
│         Search Index (Elasticsearch)              │
│         CDN (CloudFront/Cloudflare)               │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **File Service**: ファイルの管理
   - **Share Service**: ファイル共有の管理
   - **Sync Service**: 同期機能の管理
   - **Collaboration Service**: コラボレーション機能の管理
   - **Search Service**: 検索機能の管理
4. **Database**: ファイルメタデータ、共有情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（同期、検索インデックス更新など）
7. **Object Storage**: ファイルの保存（Google Cloud Storage）
8. **Search Index**: ファイル検索インデックス
9. **CDN**: ファイルの配信

### データフロー

#### ファイルアップロードのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → File Service
3. File Service:
   a. ファイルメタデータをデータベースに保存
   b. ファイルをObject Storageにアップロード
   c. Message Queueに同期イベントを送信
   d. Search Serviceに検索インデックス更新を依頼
```

#### ファイル共有のフロー

```
1. Client → API Gateway → Share Service
2. Share Service:
   a. 共有設定をデータベースに保存
   b. 共有リンクを生成
   c. 共有相手に通知を送信
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_folder_id) REFERENCES folders(folder_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_folder_id (parent_folder_id),
    FULLTEXT INDEX idx_file_name (file_name)
) ENGINE=InnoDB;
```

#### Shares テーブル

```sql
CREATE TABLE shares (
    share_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_id BIGINT NOT NULL,
    owner_id BIGINT NOT NULL,
    shared_with_user_id BIGINT,
    share_type ENUM('user', 'link') NOT NULL,
    share_link VARCHAR(500),
    permission ENUM('view', 'comment', 'edit') DEFAULT 'view',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    FOREIGN KEY (shared_with_user_id) REFERENCES users(user_id),
    INDEX idx_file_id (file_id),
    INDEX idx_shared_with_user_id (shared_with_user_id)
) ENGINE=InnoDB;
```

#### File_Versions テーブル

```sql
CREATE TABLE file_versions (
    version_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_id BIGINT NOT NULL,
    version_number INT NOT NULL,
    storage_url VARCHAR(500) NOT NULL,
    file_size BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    INDEX idx_file_id_version (file_id, version_number DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ファイルメタデータ、共有情報の永続化
- **Object Storage（GCS）**:
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
  "name": "document.pdf"
}

Response (200 OK):
{
  "file_id": 1234567890,
  "file_name": "document.pdf",
  "file_size": 1024000,
  "storage_url": "https://storage.googleapis.com/..."
}
```

#### ファイル共有

```
POST /api/v1/files/{file_id}/share
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "share_type": "link",
  "permission": "view"
}

Response (200 OK):
{
  "share_id": 9876543210,
  "share_link": "https://drive.google.com/file/d/abc123"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分のファイルまたは共有されたファイルのみアクセス可能
- **レート制限**: 
  - ファイルアップロード: 100ファイル/分
  - ファイルダウンロード: 無制限

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
   - 用途: ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ファイルアップロード**: 大きなファイルサイズ
2. **ファイルダウンロード**: 大きなファイルサイズ
3. **検索**: Elasticsearchクエリの最適化

### CDNの活用

- **ファイル**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ファイル転送最適化

1. **チャンクアップロード**: 大きなファイルをチャンクに分割
2. **並列アップロード**: 複数のチャンクを並列でアップロード
3. **レジューム機能**: アップロード中断時の再開

### 非同期処理

#### メッセージキュー（Kafka）

1. **同期イベント**:
   ```
   Topic: sync-events
   Partition Key: user_id
   ```

2. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: file_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 10億人
- **日間アクティブユーザー**: 5億人
- **1日のファイルアップロード数**: 10億ファイル

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,500台（リージョン間で分散）
- コスト: $0.192/時間 × 1,500台 × 730時間 = **$210,240/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.76/時間 × 80台 × 730時間 = **$44,384/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 150台
- コスト: $0.175/時間 × 150台 × 730時間 = **$19,162.50/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 30台
- コスト: $0.76/時間 × 30台 × 730時間 = **$16,644/月**

**ストレージ（S3）**:
- ファイルストレージ: 50 PB
- コスト: $0.023/GB/月 × 50,000,000 GB = **$1,150,000/月**

**ネットワーク**:
- データ転送: 20 PB/月
- コスト: $0.09/GB × 20,000,000 GB = **$1,800,000/月**

**合計**: 約 **$3,240,430.50/月**（約38,885,166ドル/年）

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
   - Object StorageのマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Google Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ファイルベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - Object Storage: サーバーサイド暗号化

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

2. **オフライン対応**:
   - オフライン時の基本機能の提供

## 12. 実装例

### ファイルサービス（疑似コード）

```python
class FileService:
    def __init__(self, db, cache, object_storage, message_queue, search_service):
        self.db = db
        self.cache = cache
        self.object_storage = object_storage
        self.message_queue = message_queue
        self.search_service = search_service
    
    async def upload_file(self, user_id: int, file_data, file_name: str, parent_folder_id: int = None):
        # ファイルをObject Storageにアップロード
        storage_url = await self.object_storage.upload_file(
            bucket="google-drive-files",
            key=f"{user_id}/{uuid.uuid4()}/{file_name}",
            file=file_data
        )
        
        # ファイルメタデータをデータベースに保存
        file_id = await self.db.insert_file(
            user_id=user_id,
            file_name=file_name,
            file_size=len(file_data),
            storage_url=storage_url,
            parent_folder_id=parent_folder_id
        )
        
        # 同期イベントを送信
        await self.message_queue.publish(
            topic="sync-events",
            message={
                "file_id": file_id,
                "user_id": user_id,
                "action": "upload"
            },
            partition_key=user_id
        )
        
        # 検索インデックス更新を依頼
        await self.search_service.update_index(
            file_id=file_id,
            file_name=file_name,
            user_id=user_id
        )
        
        return {
            "file_id": file_id,
            "file_name": file_name,
            "storage_url": storage_url
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のファイルダウンロード**: 50億回
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

#### 書き込みトラフィック

- **1日のファイルアップロード数**: 10億ファイル
- **1時間あたり**: 10億 / 24 = 約4,167万ファイル
- **1秒あたり**: 4,167万 / 3600 = 約11,575ファイル/秒
- **ピーク時（3倍）**: 約34,725ファイル/秒

### ストレージ見積もり

#### ファイルストレージ

- **1ファイルあたりの平均サイズ**: 5 MB
- **1日のファイルアップロード数**: 10億ファイル
- **1日のストレージ**: 10億 × 5 MB = 5 PB
- **1年のストレージ**: 5 PB × 365 = 約1,825 PB
- **5年のストレージ**: 約9,125 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **Object Storage**: 大規模ファイルストレージにObject Storageを使用
4. **チャンクアップロード**: 大きなファイルをチャンクに分割
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **ファイルアップロードのタイムアウト**:
   - 問題: 大きなファイルのアップロードがタイムアウト
   - 解決策: チャンクアップロードとレジューム機能

2. **同期の競合**:
   - 問題: 複数デバイスでの同時編集で競合が発生
   - 解決策: バージョン管理と競合解決アルゴリズム

## 15. 関連システム

### 類似システムへのリンク

- [Dropbox](dropbox_design.md) - ファイルストレージ
- [OneDrive](onedrive_design.md) - ファイルストレージ
- [iCloud](icloud_design.md) - ファイルストレージ

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [OneDrive](onedrive_design.md)でMicrosoftのファイルストレージシステムの設計を学ぶ

