# GitHub システム設計

## 1. システム概要

### 目的と主要機能

GitHubは、コードホスティング・バージョン管理プラットフォームです。Gitリポジトリのホスティング、コラボレーション、CI/CDなどの機能を提供します。

**主要機能**:
- Gitリポジトリのホスティング
- プルリクエスト（Pull Request）
- コードレビュー
- Issues（課題管理）
- GitHub Actions（CI/CD）
- GitHub Pages（静的サイトホスティング）
- コード検索
- セキュリティスキャン

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1億人
- **日間アクティブユーザー（DAU）**: 約5,000万人
- **リポジトリ数**: 約4億リポジトリ
- **1日のプッシュ数**: 約1億回
- **1日のプルリクエスト作成数**: 約500万回
- **1秒あたりのリクエスト数**: 約10,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **コードプッシュ**: 開発者がコードをプッシュ
2. **プルリクエスト**: 開発者がプルリクエストを作成
3. **コードレビュー**: 開発者がコードをレビュー
4. **CI/CD**: GitHub ActionsでCI/CDを実行
5. **コード検索**: 開発者がコードを検索

## 2. 機能要件

### コア機能

1. **Gitリポジトリ管理**
   - リポジトリの作成・削除
   - Git操作（push、pull、clone）
   - ブランチ管理
   - タグ管理

2. **プルリクエスト**
   - プルリクエストの作成・マージ
   - コードレビュー
   - コメント・ディスカッション

3. **Issues**
   - Issueの作成・管理
   - ラベル・マイルストーン
   - プロジェクト管理

4. **GitHub Actions**
   - CI/CDパイプライン
   - ワークフロー実行
   - ジョブ管理

5. **コード検索**
   - 全文検索
   - コードナビゲーション
   - シンボル検索

### 非機能要件

- **可用性**: 99.95%以上（年間ダウンタイム < 4.38時間）
- **一貫性**: Git操作は強い一貫性が必要
- **パフォーマンス**:
  - Git操作: < 5秒
  - コード検索: < 1秒
  - プルリクエスト作成: < 2秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: コードは永続的に保存

### 優先順位付け

1. **P0（必須）**: Gitリポジトリ管理、プルリクエスト、コードレビュー
2. **P1（重要）**: GitHub Actions、コード検索、Issues
3. **P2（望ましい）**: 高度な分析・レポート、セキュリティスキャン

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Git Client, API Clients)
└──────┬──────┘
       │ HTTPS / Git Protocol
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
│  │ Git      │  │ Pull     │  │ Code     │        │
│  │ Service  │  │ Request  │  │ Search   │        │
│  │          │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      GitHub Actions Service          │         │
│  │      Issue Service                  │         │
│  │      Notification Service           │         │
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
│         Git Storage (Distributed File System)     │
│         Object Storage (S3)                        │
│         (Large files, artifacts)                  │
│         Search Index (Elasticsearch)              │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Git Service**: Git操作の処理
   - **Pull Request Service**: プルリクエストの管理
   - **Code Search Service**: コード検索
   - **GitHub Actions Service**: CI/CDパイプラインの実行
   - **Issue Service**: Issueの管理
   - **Notification Service**: 通知の送信
4. **Database**: リポジトリメタデータ、プルリクエスト、Issueの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（通知、CI/CD実行など）
7. **Git Storage**: Gitリポジトリの保存（分散ファイルシステム）
8. **Object Storage**: 大きなファイル、アーティファクトの保存
9. **Search Index**: Elasticsearchを使用したコード検索インデックス

### データフロー

#### Git Pushのフロー

```
1. Client (Git) → Load Balancer → API Gateway
2. API Gateway → Git Service
3. Git Service:
   a. Git操作を検証
   b. Git Storageに保存
   c. リポジトリメタデータを更新
   d. Webhookをトリガー（非同期）
   e. GitHub Actionsをトリガー（非同期）
   f. 検索インデックスを更新（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Repositories テーブル

```sql
CREATE TABLE repositories (
    repo_id BIGINT PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    repo_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    is_fork BOOLEAN DEFAULT FALSE,
    parent_repo_id BIGINT,
    default_branch VARCHAR(255) DEFAULT 'main',
    star_count INT DEFAULT 0,
    fork_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_repo_id) REFERENCES repositories(repo_id),
    UNIQUE KEY unique_owner_repo (owner_id, repo_name),
    INDEX idx_owner_id (owner_id),
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_repo_name_description (repo_name, description)
) ENGINE=InnoDB;
```

#### Pull_Requests テーブル

```sql
CREATE TABLE pull_requests (
    pr_id BIGINT PRIMARY KEY,
    repo_id BIGINT NOT NULL,
    number INT NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    author_id BIGINT NOT NULL,
    head_branch VARCHAR(255) NOT NULL,
    base_branch VARCHAR(255) NOT NULL,
    status ENUM('open', 'closed', 'merged') DEFAULT 'open',
    merge_commit_sha VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES repositories(repo_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id),
    UNIQUE KEY unique_repo_number (repo_id, number),
    INDEX idx_repo_id_status (repo_id, status),
    INDEX idx_author_id (author_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### Issues テーブル

```sql
CREATE TABLE issues (
    issue_id BIGINT PRIMARY KEY,
    repo_id BIGINT NOT NULL,
    number INT NOT NULL,
    title VARCHAR(500) NOT NULL,
    body TEXT,
    author_id BIGINT NOT NULL,
    status ENUM('open', 'closed') DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES repositories(repo_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id),
    UNIQUE KEY unique_repo_number (repo_id, number),
    INDEX idx_repo_id_status (repo_id, status),
    INDEX idx_author_id (author_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: リポジトリメタデータ、プルリクエスト、Issueの永続化
- **Elasticsearch**:
  - 理由: 全文検索、コード検索
  - 用途: コード検索インデックス
- **Redis**:
  - 理由: リアルタイムデータ、セッション情報
  - 用途: セッション情報、キャッシュ

### スキーマ設計の考慮事項

1. **パーティショニング**: `repositories`テーブルは`owner_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: プルリクエスト、Issueは時系列で保存
4. **全文検索**: Elasticsearchを使用したコード検索

## 5. API設計

### 主要なAPIエンドポイント

#### リポジトリ作成

```
POST /api/v1/repos
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "name": "my-repo",
  "description": "My repository",
  "private": false
}

Response (201 Created):
{
  "id": 1234567890,
  "name": "my-repo",
  "full_name": "username/my-repo",
  "private": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### プルリクエスト作成

```
POST /api/v1/repos/{owner}/{repo}/pulls
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Fix bug",
  "head": "feature-branch",
  "base": "main",
  "body": "This PR fixes a bug"
}

Response (201 Created):
{
  "id": 9876543210,
  "number": 123,
  "title": "Fix bug",
  "status": "open",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Personal Access Token
- **認可**: リポジトリのアクセス権限に基づく認可
- **レート制限**: 
  - APIリクエスト: 5,000回/時間（認証済み）
  - Git操作: 無制限

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### Git Storage

- **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
- **地理的分散**: 複数のリージョンにGit Storageを配置
- **レプリケーション**: Gitリポジトリを複数のリージョンにレプリケート

#### データベースシャーディング

**シャーディング戦略**: Owner IDベースのシャーディング

```
Shard 1: owner_id % 16 == 0
Shard 2: owner_id % 16 == 1
...
Shard 16: owner_id % 16 == 15
```

**シャーディングキー**: `owner_id`
- リポジトリは`owner_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索インデックス**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **Git Protocol**: Git操作専用のロードバランサー

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: リポジトリメタデータ、プルリクエスト情報、セッション情報
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **Git操作**: 大きなリポジトリの操作
2. **コード検索**: 大量のコードの検索
3. **CI/CD実行**: GitHub Actionsの実行

### Git操作最適化

1. **分散ファイルシステム**: 高速なGit Storage
2. **キャッシング**: 頻繁にアクセスされるリポジトリをキャッシュ
3. **圧縮**: Gitオブジェクトの圧縮

### コード検索最適化

1. **Elasticsearch**: 全文検索インデックス
2. **事前インデックス**: コードを事前にインデックス
3. **キャッシング**: 検索結果をキャッシュ

### CI/CD最適化

1. **並列実行**: 複数のジョブを並列実行
2. **キャッシング**: ビルドアーティファクトをキャッシュ
3. **分散実行**: 複数のランナーで分散実行

### 非同期処理

#### メッセージキュー（Kafka）

1. **通知送信**:
   ```
   Topic: notifications
   Partition Key: user_id
   ```

2. **GitHub Actions実行**:
   ```
   Topic: github-actions
   Partition Key: repo_id
   ```

3. **検索インデックス更新**:
   ```
   Topic: search-index-update
   Partition Key: repo_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1億人
- **日間アクティブユーザー**: 5,000万人
- **リポジトリ数**: 4億リポジトリ
- **1日のプッシュ数**: 1億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.2xlarge (8 vCPU, 32 GB RAM)
- インスタンス数: 3,000台（リージョン間で分散）
- コスト: $0.384/時間 × 3,000台 × 730時間 = **$840,960/月**

**Git Storageサーバー**:
- EC2インスタンス: i3.2xlarge (8 vCPU, 61 GB RAM, NVMe SSD)
- インスタンス数: 5,000台
- コスト: $0.624/時間 × 5,000台 × 730時間 = **$2,277,600/月**

**データベース**:
- RDS MySQL db.r5.4xlarge (16 vCPU, 128 GB RAM)
- インスタンス数: 500台（マスター + レプリカ）
- コスト: $1.52/時間 × 500台 × 730時間 = **$554,800/月**

**検索インデックス（Elasticsearch）**:
- Elasticsearch r5.4xlarge (16 vCPU, 128 GB RAM)
- インスタンス数: 300台
- コスト: $1.52/時間 × 300台 × 730時間 = **$332,880/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 500台
- コスト: $0.175/時間 × 500台 × 730時間 = **$63,875/月**

**ストレージ（S3）**:
- Gitリポジトリストレージ: 500 PB
- コスト: $0.023/GB/月 × 500,000,000 GB = **$11,500,000/月**

**ネットワーク**:
- データ転送: 200 PB/月
- コスト: $0.09/GB × 200,000,000 GB = **$18,000,000/月**

**合計**: 約 **$33,570,115/月**（約402,841,380ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減
6. **Gitオブジェクトの最適化**: Gitオブジェクトの圧縮と最適化

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置
   - Git Storageのレプリケーション

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Git Storageのヘルスチェック

3. **サーキットブレーカー**:
   - 障害が発生したサービスへのリクエストを遮断
   - フォールバック処理を実装

### 冗長化戦略

#### データベース冗長化

- **マスター-レプリカ構成**: 1つのマスター、複数のレプリカ
- **自動フェイルオーバー**: マスター障害時にレプリカを昇格
- **マルチリージョン**: 地理的に分散したレプリカ

#### Git Storage冗長化

- **レプリケーション**: Gitリポジトリを複数のリージョンにレプリケート
- **バックアップ**: 定期的なバックアップ

### バックアップ・復旧戦略

1. **データベースバックアップ**:
   - 日次フルバックアップ
   - 継続的なバックアップ（ポイントインタイムリカバリ）
   - バックアップの保存期間: 30日

2. **Git Storageバックアップ**:
   - 定期的なバックアップ
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Personal Access Token
   - SSH鍵認証（Git操作）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - リポジトリレベルのアクセス制御

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
- **Git操作**: < 5秒
- **コード検索**: < 1秒
- **プルリクエスト作成**: < 2秒

### プログレッシブローディング

1. **リポジトリ一覧の遅延読み込み**:
   - 最初の30件を先に表示
   - 残りのリポジトリはスクロール時に読み込み

2. **コードファイルの遅延読み込み**:
   - 大きなファイルは段階的に読み込み

## 12. 実装例

### Gitサービス（疑似コード）

```python
class GitService:
    def __init__(self, git_storage, db, cache, message_queue):
        self.git_storage = git_storage
        self.db = db
        self.cache = cache
        self.message_queue = message_queue
    
    async def push(self, repo_id: int, ref: str, objects: list):
        # Gitオブジェクトを保存
        await self.git_storage.store_objects(
            repo_id=repo_id,
            ref=ref,
            objects=objects
        )
        
        # リポジトリメタデータを更新
        await self.db.update_repository(
            repo_id=repo_id,
            updated_at=datetime.now()
        )
        
        # Webhookをトリガー（非同期）
        await self.message_queue.publish(
            topic="webhooks",
            message={
                "repo_id": repo_id,
                "event": "push",
                "ref": ref
            },
            partition_key=repo_id
        )
        
        # GitHub Actionsをトリガー（非同期）
        await self.message_queue.publish(
            topic="github-actions",
            message={
                "repo_id": repo_id,
                "event": "push",
                "ref": ref
            },
            partition_key=repo_id
        )
        
        # 検索インデックスを更新（非同期）
        await self.message_queue.publish(
            topic="search-index-update",
            message={
                "repo_id": repo_id,
                "ref": ref
            },
            partition_key=repo_id
        )
        
        return {"status": "success"}
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のリポジトリアクセス**: 50億回
- **1時間あたり**: 50億 / 24 = 約2.08億回
- **1秒あたり**: 2.08億 / 3600 = 約57,778回/秒
- **ピーク時（3倍）**: 約173,334回/秒

#### 書き込みトラフィック

- **1日のプッシュ数**: 1億回
- **1時間あたり**: 1億 / 24 = 約416万回
- **1秒あたり**: 416万 / 3600 = 約1,156回/秒
- **ピーク時（3倍）**: 約3,468回/秒

### ストレージ見積もり

#### Gitリポジトリストレージ

- **1リポジトリあたりの平均サイズ**: 100 MB
- **リポジトリ数**: 4億リポジトリ
- **合計ストレージ**: 4億 × 100 MB = 40 PB
- **履歴を含む**: 40 PB × 2 = 80 PB
- **レプリケーション**: 80 PB × 3 = 240 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
2. **マイクロサービス**: 機能ごとにサービスを分割
3. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
4. **検索インデックス**: Elasticsearchを使用したコード検索
5. **CI/CD**: GitHub ActionsでCI/CDを実行
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **Git操作のスケーラビリティ**:
   - 問題: 大きなリポジトリの操作が遅い
   - 解決策: 分散ファイルシステムとキャッシング

2. **コード検索のスケーラビリティ**:
   - 問題: 大量のコードの検索が遅い
   - 解決策: Elasticsearchと事前インデックス

3. **ストレージコスト**:
   - 問題: Gitリポジトリのストレージコストが高い
   - 解決策: Gitオブジェクトの圧縮と最適化

## 15. 関連システム

### 類似システムへのリンク

- [GitLab](gitlab_design.md) - DevOpsプラットフォーム
- [Bitbucket](bitbucket_design.md) - コードホスティングプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [GitLab](gitlab_design.md)でDevOpsプラットフォームの設計を学ぶ

