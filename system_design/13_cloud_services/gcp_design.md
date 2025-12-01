# GCP システム設計

## 1. システム概要

### 目的と主要機能

GCP（Google Cloud Platform）は、Googleが提供するクラウドコンピューティングプラットフォームです。コンピューティング、ストレージ、ネットワーク、AI/MLなどのサービスを提供します。

**主要機能**:
- 仮想マシン（Compute Engine）
- オブジェクトストレージ（Cloud Storage）
- データベース（Cloud SQL、Firestore）
- コンテナオーケストレーション（Google Kubernetes Engine）
- サーバーレス（Cloud Functions）
- AI/MLサービス（Vertex AI）
- CDN（Cloud CDN）

### ユーザースケール

- **アクティブアカウント数**: 約60万アカウント
- **1日のリクエスト数**: 約数兆リクエスト
- **総ストレージ**: 約数エクサバイト
- **データセンター数**: 約100（世界中）

### 主要なユースケース

1. **仮想マシン**: ユーザーが仮想マシンを起動・管理
2. **ストレージ**: ユーザーがデータを保存・取得
3. **データベース**: ユーザーがデータベースを作成・管理
4. **AI/ML**: ユーザーが機械学習モデルをデプロイ
5. **コンテナ**: ユーザーがコンテナをデプロイ・管理

## 2. 機能要件

### コア機能

1. **コンピューティング**
   - 仮想マシンの起動と管理
   - オートスケーリング
   - コンテナオーケストレーション

2. **ストレージ**
   - オブジェクトストレージ
   - ブロックストレージ
   - ファイルストレージ

3. **ネットワーク**
   - Virtual Private Cloud（VPC）
   - ロードバランサー
   - CDN

4. **データベース**
   - リレーショナルデータベース
   - NoSQLデータベース
   - データベースの自動バックアップ

5. **AI/ML**
   - 機械学習モデルのトレーニング
   - モデルのデプロイ
   - 推論サービス

### 非機能要件

- **可用性**: 99.99%以上（SLA）
- **パフォーマンス**:
  - API応答: < 100ms
  - 仮想マシン起動: < 1分
- **スケーラビリティ**: 自動スケーリング
- **セキュリティ**: 強固なセキュリティとコンプライアンス

### 優先順位付け

1. **P0（必須）**: 仮想マシン、ストレージ、データベース、ネットワーク
2. **P1（重要）**: AI/ML、コンテナ、サーバーレス
3. **P2（望ましい）**: 高度な分析機能、統合サービス

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Google Cloud Console, CLI, SDK)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         API Gateway                         │
└──────┬──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
│  Compute    │   │  Cloud      │   │  Cloud SQL  │
│  Engine     │   │  Storage    │   │  Service    │
│  Service    │   │  Service    │   │             │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       ├─────────────────┴──────────────────┤
       │                                     │
┌──────▼─────────────────────────────────────▼──────┐
│              Resource Management                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Hypervisor│ │ Storage  │ │ Network  │        │
│  │ Manager  │ │ Manager   │ │ Manager  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼──────────────┼──────────────┼──────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼──────┐
│         Physical Infrastructure           │
│         (Servers, Storage, Network)       │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **API Gateway**: 全てのAPIリクエストのエントリーポイント
2. **Compute Engine Service**: 仮想マシンの管理
3. **Cloud Storage Service**: オブジェクトストレージの管理
4. **Cloud SQL Service**: リレーショナルデータベースの管理
5. **Resource Management**: 物理リソースの管理

### データフロー

#### 仮想マシン起動のフロー

```
1. Client → API Gateway
2. API Gateway → Compute Engine Service
3. Compute Engine Service:
   a. リソースの可用性を確認
   b. Hypervisor Managerに仮想マシン作成を依頼
   c. ネットワーク設定を適用
   d. 仮想マシン情報を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Virtual_Machines テーブル

```sql
CREATE TABLE virtual_machines (
    vm_id BIGINT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    vm_name VARCHAR(200) NOT NULL,
    machine_type VARCHAR(50) NOT NULL,
    os_type ENUM('linux', 'windows') NOT NULL,
    status ENUM('running', 'stopped', 'terminated') DEFAULT 'stopped',
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    INDEX idx_project_id (project_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Storage_Buckets テーブル

```sql
CREATE TABLE storage_buckets (
    bucket_id BIGINT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    bucket_name VARCHAR(200) NOT NULL,
    storage_class ENUM('standard', 'nearline', 'coldline', 'archive') DEFAULT 'standard',
    total_size BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    INDEX idx_project_id (project_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（Cloud SQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: リソース管理、プロジェクト情報の永続化

### スキーマ設計の考慮事項

1. **パーティショニング**: `virtual_machines`テーブルは`project_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: リソース使用量は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 仮想マシン起動

```
POST /api/v1/projects/{project_id}/instances
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "name": "my-instance",
  "machine_type": "n1-standard-1",
  "image": "projects/debian-cloud/global/images/debian-11"
}

Response (200 OK):
{
  "id": "instance_1234567890",
  "name": "my-instance",
  "status": "running",
  "ip_address": "10.0.0.1"
}
```

### 認証・認可

- **認証**: Google OAuth 2.0
- **認可**: IAM（Identity and Access Management）
- **レート制限**: 
  - 仮想マシン起動: 100回/分
  - ストレージアクセス: 1,000回/秒

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: Cloud Load Balancing
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Project IDベースのシャーディング

```
Shard 1: project_id % 8 == 0
Shard 2: project_id % 8 == 1
...
Shard 8: project_id % 8 == 7
```

**シャーディングキー**: `project_id`
- リソースは`project_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Cloud Memorystore（Redis）で水平スケーリング

### 負荷分散

- **Load Balancer**: Cloud Load Balancing
- **地理的分散**: 複数のリージョンにデプロイ

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Cloud Memorystore）**:
   - 用途: リソース情報、プロジェクト情報
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **仮想マシン起動**: 物理リソースの割り当て
2. **ストレージアクセス**: 大規模ストレージへのアクセス
3. **ネットワーク**: 地理的な距離

### CDNの活用

- **静的コンテンツ**: Cloud CDN
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 仮想マシン起動最適化

1. **事前プロビジョニング**: よく使われるイメージを事前プロビジョニング
2. **キャッシング**: 仮想マシン情報をキャッシュ
3. **並列処理**: 複数の仮想マシンを並列で起動

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **アクティブアカウント数**: 60万アカウント
- **1日の仮想マシン起動数**: 80万回

#### サーバーコスト（GCP）

**アプリケーションサーバー**:
- Compute Engine: n1-standard-4 (4 vCPU, 15 GB RAM)
- インスタンス数: 800台（リージョン間で分散）
- コスト: $0.19/時間 × 800台 × 730時間 = **$110,960/月**

**データベース**:
- Cloud SQL: db-n1-standard-8 (8 vCPU, 30 GB RAM)
- インスタンス数: 80台（マスター + レプリカ）
- コスト: $0.70/時間 × 80台 × 730時間 = **$40,880/月**

**ストレージ**:
- Cloud Storage: 8 PB
- コスト: $0.020/GB/月 × 8,000,000 GB = **$160,000/月**

**ネットワーク**:
- データ転送: 400 TB/月
- コスト: $0.05/GB × 400,000 GB = **$20,000/月**

**合計**: 約 **$331,840/月**（約3,982,080ドル/年）

### コスト削減戦略

1. **コミットメント割引**: 1年契約で最大70%削減
2. **プリエンプティブルインスタンス**: 非クリティカルなワークロードで最大80%削減
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

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 1時間
   - RPO（Recovery Point Objective）: 15分

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - Google OAuth 2.0
   - マルチファクター認証（MFA）

2. **認可**:
   - IAM（Identity and Access Management）
   - リソースベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ
   - ストレージ: Cloud Storage Encryption

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限
   - プロジェクトベースのレート制限

2. **Cloud Armor**: DDoS攻撃の保護
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **仮想マシン起動**: < 1分

### プログレッシブローディング

1. **リソース一覧の遅延読み込み**:
   - 最初の50件を先に表示
   - 残りのリソースはスクロール時に読み込み

2. **エラーハンドリング**:
   - 分かりやすいエラーメッセージ

## 12. 実装例

### 仮想マシンサービス（疑似コード）

```python
class ComputeEngineService:
    def __init__(self, db, cache, hypervisor_manager, network_manager):
        self.db = db
        self.cache = cache
        self.hypervisor_manager = hypervisor_manager
        self.network_manager = network_manager
    
    async def create_instance(self, project_id: int, name: str, 
                            machine_type: str, image: str):
        # リソースの可用性を確認
        available = await self.check_resource_availability(machine_type=machine_type)
        
        if not available:
            raise ResourceUnavailableError("Resource not available")
        
        # 仮想マシンを作成
        instance_id = await self.db.insert_instance(
            project_id=project_id,
            name=name,
            machine_type=machine_type,
            status='running'
        )
        
        # Hypervisor Managerに仮想マシン作成を依頼
        instance_info = await self.hypervisor_manager.create_vm(
            instance_id=instance_id,
            machine_type=machine_type,
            image=image
        )
        
        # ネットワーク設定を適用
        ip_address = await self.network_manager.assign_ip(
            instance_id=instance_id
        )
        
        # 仮想マシン情報を更新
        await self.db.update_instance(
            instance_id=instance_id,
            ip_address=ip_address
        )
        
        return {
            "id": instance_id,
            "name": name,
            "status": "running",
            "ip_address": ip_address
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のAPIリクエスト数**: 80億回
- **1時間あたり**: 80億 / 24 = 約3,333万回
- **1秒あたり**: 3,333万 / 3600 = 約9,259回/秒
- **ピーク時（3倍）**: 約27,777回/秒

#### 書き込みトラフィック

- **1日の仮想マシン起動数**: 80万回
- **1時間あたり**: 80万 / 24 = 約3.33万回
- **1秒あたり**: 3.33万 / 3600 = 約9.26回/秒
- **ピーク時（3倍）**: 約27.78回/秒

### ストレージ見積もり

#### ストレージ

- **総ストレージ**: 8 PB
- **1日のストレージ増加**: 80 TB
- **1年のストレージ**: 8 PB + (80 TB × 365) = 約37.2 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **リソース管理**: 効率的なリソース管理
4. **モニタリング**: 包括的なモニタリングとアラート
5. **セキュリティ**: 強固なセキュリティとコンプライアンス

### よくある落とし穴

1. **リソースの競合**:
   - 問題: 同時にリソースを要求して競合が発生
   - 解決策: リソースキューと優先順位付け

2. **仮想マシン起動のレイテンシ**:
   - 問題: 仮想マシン起動が遅い
   - 解決策: 事前プロビジョニングとキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [AWS](aws_design.md) - クラウドコンピューティングプラットフォーム
- [Azure](azure_design.md) - クラウドコンピューティングプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Database Sharding](../17_common_patterns/database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Cloudflare](../14_cdn/cloudflare_design.md)でCDNの設計を学ぶ

