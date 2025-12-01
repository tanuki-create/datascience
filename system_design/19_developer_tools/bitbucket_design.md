# Bitbucket システム設計

## 1. システム概要

### 目的と主要機能

Bitbucketは、Atlassianが提供するコードホスティング・バージョン管理プラットフォームです。Gitリポジトリのホスティング、CI/CD、Atlassian製品との統合を提供します。

**主要機能**:
- Gitリポジトリのホスティング
- プルリクエスト（Pull Request）
- Bitbucket Pipelines（CI/CD）
- Jira統合
- Confluence統合
- コードレビュー
- セキュリティスキャン

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1,000万人
- **日間アクティブユーザー（DAU）**: 約500万人
- **リポジトリ数**: 約1,000万リポジトリ
- **1日のプッシュ数**: 約1,000万回
- **1日のプルリクエスト作成数**: 約100万回
- **1秒あたりのリクエスト数**: 約3,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **コードプッシュ**: 開発者がコードをプッシュ
2. **プルリクエスト**: 開発者がプルリクエストを作成
3. **CI/CD実行**: Bitbucket PipelinesでCI/CDを実行
4. **Jira統合**: Jiraと連携して課題管理
5. **コードレビュー**: 開発者がコードをレビュー

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

3. **Bitbucket Pipelines**
   - CI/CDパイプラインの定義・実行
   - ジョブ管理
   - アーティファクト管理

4. **Jira統合**
   - Jira課題との連携
   - コミットとJira課題の関連付け
   - 自動的な課題更新

5. **Confluence統合**
   - ドキュメントとの連携
   - リポジトリ情報の表示

### 非機能要件

- **可用性**: 99.95%以上（年間ダウンタイム < 4.38時間）
- **一貫性**: Git操作は強い一貫性が必要
- **パフォーマンス**:
  - Git操作: < 5秒
  - プルリクエスト作成: < 2秒
  - CI/CDジョブ開始: < 10秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: コードは永続的に保存

### 優先順位付け

1. **P0（必須）**: Gitリポジトリ管理、プルリクエスト、コードレビュー
2. **P1（重要）**: Bitbucket Pipelines、Jira統合、Confluence統合
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
│  │ Git      │  │ Pull     │  │ Pipeline │        │
│  │ Service  │  │ Request  │  │ Service  │        │
│  │          │  │ Service  │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Jira Integration Service        │         │
│  │      Confluence Integration Service  │         │
│  │      Notification Service            │         │
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
│         (Artifacts)                               │
│         Pipeline Runners (Docker/Kubernetes)      │
│         Jira API                                  │
│         Confluence API                            │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Git Service**: Git操作の処理
   - **Pull Request Service**: プルリクエストの管理
   - **Pipeline Service**: CI/CDパイプラインの管理
   - **Jira Integration Service**: Jiraとの統合
   - **Confluence Integration Service**: Confluenceとの統合
   - **Notification Service**: 通知の送信
4. **Database**: リポジトリメタデータ、プルリクエスト、パイプラインの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（通知、CI/CD実行など）
7. **Git Storage**: Gitリポジトリの保存（分散ファイルシステム）
8. **Object Storage**: アーティファクトの保存
9. **Pipeline Runners**: Docker/KubernetesでCI/CDジョブを実行
10. **Jira API**: Jiraとの統合用API
11. **Confluence API**: Confluenceとの統合用API

### データフロー

#### プルリクエスト作成のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Pull Request Service
3. Pull Request Service:
   a. プルリクエストを作成
   b. Jira課題を関連付け（非同期）
   c. 通知を送信（非同期）
   d. CI/CDパイプラインをトリガー（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Repositories テーブル

```sql
CREATE TABLE repositories (
    repo_id BIGINT PRIMARY KEY,
    workspace_id BIGINT NOT NULL,
    repo_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    default_branch VARCHAR(255) DEFAULT 'main',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    UNIQUE KEY unique_workspace_repo (workspace_id, repo_name),
    INDEX idx_workspace_id (workspace_id),
    INDEX idx_created_at (created_at DESC)
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
    jira_issue_key VARCHAR(50),
    merge_commit_sha VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES repositories(repo_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id),
    UNIQUE KEY unique_repo_number (repo_id, number),
    INDEX idx_repo_id_status (repo_id, status),
    INDEX idx_jira_issue_key (jira_issue_key)
) ENGINE=InnoDB;
```

#### Pipelines テーブル

```sql
CREATE TABLE pipelines (
    pipeline_id BIGINT PRIMARY KEY,
    repo_id BIGINT NOT NULL,
    commit_sha VARCHAR(40) NOT NULL,
    branch VARCHAR(255) NOT NULL,
    status ENUM('pending', 'running', 'success', 'failed', 'canceled') DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repo_id) REFERENCES repositories(repo_id),
    INDEX idx_repo_id_status (repo_id, status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: リポジトリメタデータ、プルリクエスト、パイプラインの永続化
- **Redis**:
  - 理由: リアルタイムデータ、セッション情報
  - 用途: セッション情報、キャッシュ

### スキーマ設計の考慮事項

1. **パーティショニング**: `repositories`テーブルは`workspace_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: プルリクエスト、パイプラインは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### プルリクエスト作成

```
POST /api/2.0/repositories/{workspace}/{repo_slug}/pullrequests
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "title": "Fix bug",
  "source": {
    "branch": {
      "name": "feature-branch"
    }
  },
  "destination": {
    "branch": {
      "name": "main"
    }
  },
  "description": "This PR fixes a bug",
  "jira_issue_key": "PROJ-123"
}

Response (201 Created):
{
  "id": 1234567890,
  "title": "Fix bug",
  "state": "OPEN",
  "jira_issue_key": "PROJ-123",
  "created_on": "2024-01-15T10:30:00Z"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、App Password
- **認可**: ワークスペース・リポジトリのアクセス権限に基づく認可
- **レート制限**: 
  - APIリクエスト: 1,000回/時間（認証済み）
  - Git操作: 無制限

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### Pipeline Runners

- **Docker/Kubernetes**: Docker/KubernetesでCI/CDジョブを実行
- **動的スケーリング**: 需要に応じてランナーを起動・停止
- **地理的分散**: 複数のリージョンにランナーを配置

#### Git Storage

- **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
- **地理的分散**: 複数のリージョンにGit Storageを配置
- **レプリケーション**: Gitリポジトリを複数のリージョンにレプリケート

#### データベースシャーディング

**シャーディング戦略**: Workspace IDベースのシャーディング

```
Shard 1: workspace_id % 16 == 0
Shard 2: workspace_id % 16 == 1
...
Shard 16: workspace_id % 16 == 15
```

**シャーディングキー**: `workspace_id`
- リポジトリ、プルリクエストは`workspace_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

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
2. **CI/CD実行**: CI/CDジョブの実行
3. **Jira統合**: Jira APIへのリクエスト

### Git操作最適化

1. **分散ファイルシステム**: 高速なGit Storage
2. **キャッシング**: 頻繁にアクセスされるリポジトリをキャッシュ
3. **圧縮**: Gitオブジェクトの圧縮

### CI/CD最適化

1. **並列実行**: 複数のジョブを並列実行
2. **キャッシング**: ビルドアーティファクトをキャッシュ
3. **分散実行**: 複数のランナーで分散実行

### Jira統合最適化

1. **バッチ処理**: 複数のJira APIリクエストをバッチで処理
2. **キャッシング**: Jiraデータをキャッシュ
3. **非同期処理**: Jira統合を非同期で処理

### 非同期処理

#### メッセージキュー（Kafka）

1. **通知送信**:
   ```
   Topic: notifications
   Partition Key: user_id
   ```

2. **CI/CDジョブ実行**:
   ```
   Topic: pipeline-jobs
   Partition Key: repo_id
   ```

3. **Jira統合**:
   ```
   Topic: jira-integration
   Partition Key: workspace_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1,000万人
- **日間アクティブユーザー**: 500万人
- **リポジトリ数**: 1,000万リポジトリ
- **1日のプッシュ数**: 1,000万回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**Pipeline Runners（Kubernetes）**:
- EKSノード: m5.large (2 vCPU, 8 GB RAM)
- ノード数: 2,000台（動的スケーリング）
- コスト: $0.096/時間 × 2,000台 × 730時間 = **$140,160/月**

**Git Storageサーバー**:
- EC2インスタンス: i3.xlarge (4 vCPU, 30.5 GB RAM, NVMe SSD)
- インスタンス数: 1,500台
- コスト: $0.312/時間 × 1,500台 × 730時間 = **$341,640/月**

**データベース**:
- RDS PostgreSQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 150台（マスター + レプリカ）
- コスト: $0.76/時間 × 150台 × 730時間 = **$83,220/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.large (13 GB RAM)
- インスタンス数: 150台
- コスト: $0.087/時間 × 150台 × 730時間 = **$9,526/月**

**ストレージ（S3）**:
- Gitリポジトリストレージ: 100 PB
- アーティファクトストレージ: 20 PB
- 合計: 120 PB
- コスト: $0.023/GB/月 × 120,000,000 GB = **$2,760,000/月**

**ネットワーク**:
- データ転送: 50 PB/月
- コスト: $0.09/GB × 50,000,000 GB = **$4,500,000/月**

**合計**: 約 **$7,974,706/月**（約95,696,472ドル/年）

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
   - Git Storageのレプリケーション

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Pipeline Runnersのヘルスチェック

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

2. **Git Storageバックアップ**:
   - 定期的なバックアップ
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - App Password
   - SSH鍵認証（Git操作）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ワークスペース・リポジトリレベルのアクセス制御

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
- **プルリクエスト作成**: < 2秒
- **CI/CDジョブ開始**: < 10秒

### プログレッシブローディング

1. **リポジトリ一覧の遅延読み込み**:
   - 最初の30件を先に表示
   - 残りのリポジトリはスクロール時に読み込み

2. **プルリクエスト一覧の遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのプルリクエストはスクロール時に読み込み

## 12. 実装例

### プルリクエストサービス（疑似コード）

```python
class PullRequestService:
    def __init__(self, db, cache, jira_client, message_queue):
        self.db = db
        self.cache = cache
        self.jira_client = jira_client
        self.message_queue = message_queue
    
    async def create_pull_request(self, repo_id: int, title: str, 
                                 head_branch: str, base_branch: str,
                                 jira_issue_key: str = None):
        # プルリクエストを作成
        pr_id = await self.db.insert_pull_request(
            repo_id=repo_id,
            title=title,
            head_branch=head_branch,
            base_branch=base_branch,
            status="open",
            jira_issue_key=jira_issue_key
        )
        
        # Jira課題を関連付け（非同期）
        if jira_issue_key:
            await self.message_queue.publish(
                topic="jira-integration",
                message={
                    "pr_id": pr_id,
                    "jira_issue_key": jira_issue_key,
                    "action": "link_pr"
                },
                partition_key=repo_id
            )
        
        # 通知を送信（非同期）
        await self.message_queue.publish(
            topic="notifications",
            message={
                "type": "pull_request_created",
                "pr_id": pr_id,
                "repo_id": repo_id
            },
            partition_key=repo_id
        )
        
        # CI/CDパイプラインをトリガー（非同期）
        await self.message_queue.publish(
            topic="pipeline-jobs",
            message={
                "repo_id": repo_id,
                "branch": head_branch,
                "trigger": "pull_request"
            },
            partition_key=repo_id
        )
        
        return {
            "pr_id": pr_id,
            "status": "open",
            "created_at": datetime.now()
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のリポジトリアクセス**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

#### 書き込みトラフィック

- **1日のプッシュ数**: 1,000万回
- **1時間あたり**: 1,000万 / 24 = 約416万回
- **1秒あたり**: 416万 / 3600 = 約1,156回/秒
- **ピーク時（3倍）**: 約3,468回/秒

### ストレージ見積もり

#### Gitリポジトリストレージ

- **1リポジトリあたりの平均サイズ**: 50 MB
- **リポジトリ数**: 1,000万リポジトリ
- **合計ストレージ**: 1,000万 × 50 MB = 500 TB
- **履歴を含む**: 500 TB × 2 = 1 PB
- **レプリケーション**: 1 PB × 3 = 3 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
2. **マイクロサービス**: 機能ごとにサービスを分割
3. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
4. **Atlassian統合**: Jira、Confluenceとの統合
5. **CI/CD最適化**: 並列実行とキャッシング
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **Git操作のスケーラビリティ**:
   - 問題: 大きなリポジトリの操作が遅い
   - 解決策: 分散ファイルシステムとキャッシング

2. **Jira統合のレイテンシ**:
   - 問題: Jira APIへのリクエストが遅い
   - 解決策: バッチ処理とキャッシング

3. **CI/CD実行のスケーラビリティ**:
   - 問題: CI/CDジョブの実行が遅い
   - 解決策: Kubernetesと動的スケーリング

## 15. 関連システム

### 類似システムへのリンク

- [GitHub](github_design.md) - コードホスティングプラットフォーム
- [GitLab](gitlab_design.md) - DevOpsプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Circuit Breaker](../17_common_patterns/circuit_breaker.md)で障害対策パターンを学ぶ

