# GitLab システム設計

## 1. システム概要

### 目的と主要機能

GitLabは、DevOpsプラットフォームです。Gitリポジトリのホスティング、CI/CD、コンテナレジストリ、モニタリングなどの機能を統合して提供します。

**主要機能**:
- Gitリポジトリのホスティング
- GitLab CI/CD（継続的インテグレーション・デプロイメント）
- コンテナレジストリ（Container Registry）
- パッケージレジストリ（Package Registry）
- モニタリング・可観測性
- セキュリティスキャン
- プロジェクト管理
- Wiki・ドキュメント

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約3,000万人
- **日間アクティブユーザー（DAU）**: 約1,500万人
- **リポジトリ数**: 約3,000万リポジトリ
- **1日のCI/CDジョブ実行数**: 約5,000万ジョブ
- **1日のプッシュ数**: 約3,000万回
- **1秒あたりのリクエスト数**: 約5,000リクエスト/秒（ピーク時）

### 主要なユースケース

1. **コードプッシュ**: 開発者がコードをプッシュ
2. **CI/CD実行**: GitLab CI/CDでパイプラインを実行
3. **コンテナビルド**: コンテナイメージをビルド・保存
4. **セキュリティスキャン**: コードのセキュリティスキャン
5. **モニタリング**: アプリケーションのモニタリング

## 2. 機能要件

### コア機能

1. **Gitリポジトリ管理**
   - リポジトリの作成・削除
   - Git操作（push、pull、clone）
   - ブランチ管理
   - タグ管理

2. **GitLab CI/CD**
   - CI/CDパイプラインの定義・実行
   - ジョブ管理
   - ランナー管理
   - アーティファクト管理

3. **コンテナレジストリ**
   - コンテナイメージの保存
   - イメージのプッシュ・プル
   - イメージのバージョン管理

4. **パッケージレジストリ**
   - パッケージの保存（npm、Maven、PyPIなど）
   - パッケージの配布

5. **モニタリング**
   - メトリクス収集
   - ログ集約
   - トレーシング

### 非機能要件

- **可用性**: 99.95%以上（年間ダウンタイム < 4.38時間）
- **一貫性**: Git操作は強い一貫性が必要
- **パフォーマンス**:
  - Git操作: < 5秒
  - CI/CDジョブ開始: < 10秒
  - コンテナイメージプッシュ: < 30秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: コード、アーティファクトは永続的に保存

### 優先順位付け

1. **P0（必須）**: Gitリポジトリ管理、GitLab CI/CD、コンテナレジストリ
2. **P1（重要）**: パッケージレジストリ、モニタリング、セキュリティスキャン
3. **P2（望ましい）**: 高度な分析・レポート、AI機能

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
│  │ Git      │  │ CI/CD     │  │ Container│        │
│  │ Service  │  │ Service   │  │ Registry │        │
│  │          │  │           │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Package Registry Service        │         │
│  │      Monitoring Service              │         │
│  │      Security Scan Service           │         │
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
│         (Artifacts, Container Images)              │
│         CI/CD Runners (Kubernetes)                │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Git Service**: Git操作の処理
   - **CI/CD Service**: CI/CDパイプラインの管理
   - **Container Registry Service**: コンテナレジストリの管理
   - **Package Registry Service**: パッケージレジストリの管理
   - **Monitoring Service**: モニタリングの管理
   - **Security Scan Service**: セキュリティスキャン
4. **Database**: リポジトリメタデータ、CI/CDパイプライン、ジョブの永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（CI/CD実行、通知など）
7. **Git Storage**: Gitリポジトリの保存（分散ファイルシステム）
8. **Object Storage**: アーティファクト、コンテナイメージの保存
9. **CI/CD Runners**: KubernetesクラスターでCI/CDジョブを実行

### データフロー

#### CI/CDパイプライン実行のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → CI/CD Service
3. CI/CD Service:
   a. パイプライン定義を取得
   b. ジョブをキューに追加
   c. CI/CD Runnerにジョブを割り当て
   d. ジョブ実行結果を保存
   e. 通知を送信（非同期）
```

## 4. データモデル設計

### 主要なエンティティ

#### Repositories テーブル

```sql
CREATE TABLE repositories (
    repo_id BIGINT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    repo_name VARCHAR(255) NOT NULL,
    description TEXT,
    is_private BOOLEAN DEFAULT FALSE,
    default_branch VARCHAR(255) DEFAULT 'main',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    INDEX idx_project_id (project_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### CI_Pipelines テーブル

```sql
CREATE TABLE ci_pipelines (
    pipeline_id BIGINT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    ref VARCHAR(255) NOT NULL,
    sha VARCHAR(40) NOT NULL,
    status ENUM('pending', 'running', 'success', 'failed', 'canceled') DEFAULT 'pending',
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    INDEX idx_project_id_status (project_id, status),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB;
```

#### CI_Jobs テーブル

```sql
CREATE TABLE ci_jobs (
    job_id BIGINT PRIMARY KEY,
    pipeline_id BIGINT NOT NULL,
    job_name VARCHAR(255) NOT NULL,
    status ENUM('pending', 'running', 'success', 'failed', 'canceled') DEFAULT 'pending',
    runner_id BIGINT,
    started_at TIMESTAMP NULL,
    finished_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pipeline_id) REFERENCES ci_pipelines(pipeline_id),
    INDEX idx_pipeline_id_status (pipeline_id, status),
    INDEX idx_runner_id (runner_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: リポジトリメタデータ、CI/CDパイプライン、ジョブの永続化
- **Redis**:
  - 理由: リアルタイムデータ、セッション情報、ジョブキュー
  - 用途: セッション情報、キャッシュ、ジョブキュー

### スキーマ設計の考慮事項

1. **パーティショニング**: `repositories`テーブルは`project_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: CI/CDパイプライン、ジョブは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### CI/CDパイプライン実行

```
POST /api/v4/projects/{project_id}/pipeline
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "ref": "main"
}

Response (201 Created):
{
  "id": 1234567890,
  "status": "pending",
  "ref": "main",
  "sha": "abc123...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### コンテナイメージプッシュ

```
POST /api/v4/projects/{project_id}/registry/repositories
Authorization: Bearer <token>

Response (201 Created):
{
  "id": 9876543210,
  "name": "my-image",
  "path": "project/my-image"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Personal Access Token
- **認可**: プロジェクトのアクセス権限に基づく認可
- **レート制限**: 
  - APIリクエスト: 2,000回/分（認証済み）
  - Git操作: 無制限

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### CI/CD Runners

- **Kubernetes**: KubernetesクラスターでCI/CDジョブを実行
- **動的スケーリング**: 需要に応じてランナーを起動・停止
- **地理的分散**: 複数のリージョンにランナーを配置

#### Git Storage

- **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
- **地理的分散**: 複数のリージョンにGit Storageを配置
- **レプリケーション**: Gitリポジトリを複数のリージョンにレプリケート

#### データベースシャーディング

**シャーディング戦略**: Project IDベースのシャーディング

```
Shard 1: project_id % 16 == 0
Shard 2: project_id % 16 == 1
...
Shard 16: project_id % 16 == 15
```

**シャーディングキー**: `project_id`
- リポジトリ、CI/CDパイプラインは`project_id`でシャーディング

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
   - 用途: リポジトリメタデータ、CI/CDパイプライン情報、セッション情報
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **Git操作**: 大きなリポジトリの操作
2. **CI/CD実行**: CI/CDジョブの実行
3. **コンテナイメージプッシュ**: 大きなイメージのプッシュ

### Git操作最適化

1. **分散ファイルシステム**: 高速なGit Storage
2. **キャッシング**: 頻繁にアクセスされるリポジトリをキャッシュ
3. **圧縮**: Gitオブジェクトの圧縮

### CI/CD最適化

1. **並列実行**: 複数のジョブを並列実行
2. **キャッシング**: ビルドアーティファクトをキャッシュ
3. **分散実行**: 複数のランナーで分散実行
4. **事前ビルド**: 頻繁に使用されるイメージを事前ビルド

### コンテナイメージ最適化

1. **レイヤーキャッシング**: イメージレイヤーをキャッシュ
2. **圧縮**: イメージの圧縮
3. **CDN**: イメージをCDNで配信

### 非同期処理

#### メッセージキュー（Kafka）

1. **CI/CDジョブ実行**:
   ```
   Topic: ci-cd-jobs
   Partition Key: project_id
   ```

2. **通知送信**:
   ```
   Topic: notifications
   Partition Key: user_id
   ```

3. **セキュリティスキャン**:
   ```
   Topic: security-scan
   Partition Key: project_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 3,000万人
- **日間アクティブユーザー**: 1,500万人
- **リポジトリ数**: 3,000万リポジトリ
- **1日のCI/CDジョブ実行数**: 5,000万ジョブ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.2xlarge (8 vCPU, 32 GB RAM)
- インスタンス数: 2,000台（リージョン間で分散）
- コスト: $0.384/時間 × 2,000台 × 730時間 = **$560,640/月**

**CI/CD Runners（Kubernetes）**:
- EKSノード: m5.xlarge (4 vCPU, 16 GB RAM)
- ノード数: 5,000台（動的スケーリング）
- コスト: $0.192/時間 × 5,000台 × 730時間 = **$700,800/月**

**Git Storageサーバー**:
- EC2インスタンス: i3.2xlarge (8 vCPU, 61 GB RAM, NVMe SSD)
- インスタンス数: 3,000台
- コスト: $0.624/時間 × 3,000台 × 730時間 = **$1,366,560/月**

**データベース**:
- RDS PostgreSQL db.r5.4xlarge (16 vCPU, 128 GB RAM)
- インスタンス数: 300台（マスター + レプリカ）
- コスト: $1.52/時間 × 300台 × 730時間 = **$332,880/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 300台
- コスト: $0.175/時間 × 300台 × 730時間 = **$38,325/月**

**ストレージ（S3）**:
- Gitリポジトリストレージ: 300 PB
- アーティファクトストレージ: 100 PB
- コンテナイメージストレージ: 50 PB
- 合計: 450 PB
- コスト: $0.023/GB/月 × 450,000,000 GB = **$10,350,000/月**

**ネットワーク**:
- データ転送: 150 PB/月
- コスト: $0.09/GB × 150,000,000 GB = **$13,500,000/月**

**合計**: 約 **$26,849,205/月**（約322,190,460ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **データ圧縮**: ストレージコストを削減
5. **CDN活用**: データ転送コストを削減
6. **CI/CD最適化**: ジョブの実行時間を短縮

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置
   - Git Storageのレプリケーション

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - CI/CD Runnersのヘルスチェック

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

3. **アーティファクトバックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Personal Access Token
   - SSH鍵認証（Git操作）

2. **認可**:
   - RBAC（Role-Based Access Control）
   - プロジェクトレベルのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - S3: サーバーサイド暗号化

### セキュリティスキャン

1. **コードスキャン**: 静的コード解析
2. **依存関係スキャン**: 依存関係の脆弱性スキャン
3. **コンテナスキャン**: コンテナイメージのスキャン

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
- **CI/CDジョブ開始**: < 10秒
- **コンテナイメージプッシュ**: < 30秒

### プログレッシブローディング

1. **リポジトリ一覧の遅延読み込み**:
   - 最初の30件を先に表示
   - 残りのリポジトリはスクロール時に読み込み

2. **CI/CDパイプラインの遅延読み込み**:
   - 最初の20件を先に表示
   - 残りのパイプラインはスクロール時に読み込み

## 12. 実装例

### CI/CDサービス（疑似コード）

```python
class CICDService:
    def __init__(self, db, cache, kubernetes_client, message_queue):
        self.db = db
        self.cache = cache
        self.kubernetes_client = kubernetes_client
        self.message_queue = message_queue
    
    async def create_pipeline(self, project_id: int, ref: str, sha: str):
        # パイプライン定義を取得
        pipeline_config = await self.db.get_pipeline_config(
            project_id=project_id,
            ref=ref
        )
        
        # パイプラインを作成
        pipeline_id = await self.db.insert_pipeline(
            project_id=project_id,
            ref=ref,
            sha=sha,
            status="pending"
        )
        
        # ジョブを作成
        for job_config in pipeline_config["jobs"]:
            job_id = await self.db.insert_job(
                pipeline_id=pipeline_id,
                job_name=job_config["name"],
                status="pending"
            )
            
            # ジョブをキューに追加
            await self.message_queue.publish(
                topic="ci-cd-jobs",
                message={
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "job_config": job_config
                },
                partition_key=project_id
            )
        
        return {
            "pipeline_id": pipeline_id,
            "status": "pending",
            "created_at": datetime.now()
        }
    
    async def execute_job(self, job_id: int, job_config: dict):
        # Kubernetes Podを作成してジョブを実行
        pod = await self.kubernetes_client.create_pod(
            name=f"job-{job_id}",
            image=job_config["image"],
            commands=job_config["script"]
        )
        
        # ジョブステータスを更新
        await self.db.update_job(
            job_id=job_id,
            status="running",
            runner_id=pod.id,
            started_at=datetime.now()
        )
        
        # ジョブの完了を待機（非同期）
        await self.wait_for_job_completion(job_id, pod.id)
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のリポジトリアクセス**: 20億回
- **1時間あたり**: 20億 / 24 = 約8,333万回
- **1秒あたり**: 8,333万 / 3600 = 約23,148回/秒
- **ピーク時（3倍）**: 約69,444回/秒

#### 書き込みトラフィック

- **1日のプッシュ数**: 3,000万回
- **1時間あたり**: 3,000万 / 24 = 約125万回
- **1秒あたり**: 125万 / 3600 = 約347回/秒
- **ピーク時（3倍）**: 約1,041回/秒

### ストレージ見積もり

#### Gitリポジトリストレージ

- **1リポジトリあたりの平均サイズ**: 50 MB
- **リポジトリ数**: 3,000万リポジトリ
- **合計ストレージ**: 3,000万 × 50 MB = 1.5 PB
- **履歴を含む**: 1.5 PB × 2 = 3 PB
- **レプリケーション**: 3 PB × 3 = 9 PB

#### アーティファクトストレージ

- **1ジョブあたりの平均アーティファクトサイズ**: 100 MB
- **1日のジョブ実行数**: 5,000万ジョブ
- **1日のストレージ**: 5,000万 × 100 MB = 5 PB
- **保持期間**: 30日
- **合計ストレージ**: 5 PB × 30 = 150 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **分散ファイルシステム**: Gitリポジトリを分散ファイルシステムに保存
2. **マイクロサービス**: 機能ごとにサービスを分割
3. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
4. **Kubernetes**: CI/CDジョブをKubernetesで実行
5. **CI/CD最適化**: 並列実行とキャッシング
6. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **CI/CD実行のスケーラビリティ**:
   - 問題: CI/CDジョブの実行が遅い
   - 解決策: Kubernetesと動的スケーリング

2. **ストレージコスト**:
   - 問題: アーティファクトのストレージコストが高い
   - 解決策: アーティファクトの自動削除と圧縮

3. **コンテナイメージのスケーラビリティ**:
   - 問題: コンテナイメージのプッシュ・プルが遅い
   - 解決策: CDNとレイヤーキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [GitHub](github_design.md) - コードホスティングプラットフォーム
- [Bitbucket](bitbucket_design.md) - コードホスティングプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Bitbucket](bitbucket_design.md)でコードホスティングプラットフォームの設計を学ぶ

