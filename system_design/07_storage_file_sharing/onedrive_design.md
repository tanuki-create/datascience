# OneDrive システム設計

## 1. システム概要

### 目的と主要機能

OneDriveは、Microsoftが提供するクラウドストレージサービスです。ファイルの保存、共有、同期、Office統合機能を提供します。

**主要機能**:
- ファイルのアップロード・ダウンロード
- ファイルの共有（リンク共有、ユーザー共有）
- リアルタイム同期
- Office統合（Word、Excel、PowerPoint）
- ファイル検索
- バージョン管理

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約5億人
- **日間アクティブユーザー（DAU）**: 約2億人
- **1日のファイルアップロード数**: 約5億ファイル
- **1日のファイルダウンロード数**: 約20億回
- **1秒あたりのリクエスト数**: 約15,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **ファイルアップロード**: ユーザーがファイルをアップロード
2. **ファイル共有**: ユーザーがファイルを共有
3. **リアルタイム同期**: 複数デバイス間での同期
4. **Office統合**: Officeファイルのオンライン編集
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

4. **Office統合**
   - Word、Excel、PowerPointのオンライン編集
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
2. **P1（重要）**: Office統合、検索、バージョン管理
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
│  │ File     │  │  Share   │  │  Sync   │        │
│  │ Service  │  │ Service  │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Office Service                 │         │
│  │      Search Service                 │         │
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
│         Object Storage (Azure Blob Storage)      │
│         Search Index (Azure Cognitive Search)    │
│         CDN (Azure CDN)                         │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **File Service**: ファイルの管理
   - **Share Service**: ファイル共有の管理
   - **Sync Service**: 同期機能の管理
   - **Office Service**: Office統合機能の管理
   - **Search Service**: 検索機能の管理
4. **Database**: ファイルメタデータ、共有情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（同期、検索インデックス更新など）
7. **Object Storage**: ファイルの保存（Azure Blob Storage）
8. **Search Index**: ファイル検索インデックス（Azure Cognitive Search）
9. **CDN**: ファイルの配信（Azure CDN）

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
    is_office_file BOOLEAN DEFAULT FALSE,
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

### データベース選択の理由

- **RDBMS（SQL Server/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ファイルメタデータ、共有情報の永続化
- **Object Storage（Azure Blob Storage）**:
  - 理由: 大規模ファイルストレージ、水平スケーリング
  - 用途: ファイルの保存
- **Azure Cognitive Search**:
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
  "name": "document.docx"
}

Response (200 OK):
{
  "file_id": 1234567890,
  "file_name": "document.docx",
  "file_size": 1024000,
  "storage_url": "https://storage.azure.com/..."
}
```

#### Officeファイル編集

```
GET /api/v1/files/{file_id}/edit
Authorization: Bearer <token>

Response (200 OK):
{
  "edit_url": "https://office.live.com/...",
  "session_id": "abc123"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Microsoft Account統合
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
Shard 1: user_id % 4 == 0
Shard 2: user_id % 4 == 1
Shard 3: user_id % 4 == 2
Shard 4: user_id % 4 == 3
```

**シャーディングキー**: `user_id`
- ファイルは`user_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Azure Cognitive Searchで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAzure Load Balancer
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: ファイルをAzure CDNで配信

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
3. **Office統合**: リアルタイム共同編集のレイテンシ

### CDNの活用

- **ファイル**: Azure CDN
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

- **月間アクティブユーザー**: 5億人
- **日間アクティブユーザー**: 2億人
- **1日のファイルアップロード数**: 5億ファイル

#### サーバーコスト（Azure）

**アプリケーションサーバー**:
- Azure VM: Standard_D4s_v3 (4 vCPU, 16 GB RAM)
- インスタンス数: 800台（リージョン間で分散）
- コスト: $0.192/時間 × 800台 × 730時間 = **$112,128/月**

**データベース**:
- Azure SQL Database: Business Critical (8 vCPU, 64 GB RAM)
- インスタンス数: 40台（マスター + レプリカ）
- コスト: $0.76/時間 × 40台 × 730時間 = **$22,192/月**

**キャッシュ（Azure Cache for Redis）**:
- Redis Premium P1 (26 GB RAM)
- インスタンス数: 80台
- コスト: $0.175/時間 × 80台 × 730時間 = **$10,220/月**

**ストレージ（Azure Blob Storage）**:
- ファイルストレージ: 25 PB
- コスト: $0.018/GB/月 × 25,000,000 GB = **$450,000/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.05/GB × 10,000,000 GB = **$500,000/月**

**合計**: 約 **$1,094,540/月**（約13,134,480ドル/年）

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
   - Azure Blob StorageのマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Microsoft Account統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ファイルベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ
   - Azure Blob Storage: サーバーサイド暗号化

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - ユーザーベースのレート制限

2. **CDN**: Azure CDN
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
            container="onedrive-files",
            blob_name=f"{user_id}/{uuid.uuid4()}/{file_name}",
            file=file_data
        )
        
        # Officeファイルかどうかを判定
        is_office_file = self.is_office_file(file_name)
        
        # ファイルメタデータをデータベースに保存
        file_id = await self.db.insert_file(
            user_id=user_id,
            file_name=file_name,
            file_size=len(file_data),
            storage_url=storage_url,
            parent_folder_id=parent_folder_id,
            is_office_file=is_office_file
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
            "storage_url": storage_url,
            "is_office_file": is_office_file
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のファイルダウンロード**: 20億回
- **1時間あたり**: 20億 / 24 = 約8,333万回
- **1秒あたり**: 8,333万 / 3600 = 約23,148回/秒
- **ピーク時（3倍）**: 約69,444回/秒

#### 書き込みトラフィック

- **1日のファイルアップロード数**: 5億ファイル
- **1時間あたり**: 5億 / 24 = 約2,083万ファイル
- **1秒あたり**: 2,083万 / 3600 = 約5,787ファイル/秒
- **ピーク時（3倍）**: 約17,361ファイル/秒

### ストレージ見積もり

#### ファイルストレージ

- **1ファイルあたりの平均サイズ**: 5 MB
- **1日のファイルアップロード数**: 5億ファイル
- **1日のストレージ**: 5億 × 5 MB = 2.5 PB
- **1年のストレージ**: 2.5 PB × 365 = 約912.5 PB
- **5年のストレージ**: 約4,562.5 PB

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

2. **Office統合のレイテンシ**:
   - 問題: Officeファイルのリアルタイム共同編集が遅い
   - 解決策: WebSocketと最適化されたアルゴリズム

## 15. 関連システム

### 類似システムへのリンク

- [Google Drive](google_drive_design.md) - ファイルストレージ
- [Dropbox](dropbox_design.md) - ファイルストレージ
- [iCloud](icloud_design.md) - ファイルストレージ

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [iCloud](icloud_design.md)でAppleのファイルストレージシステムの設計を学ぶ

