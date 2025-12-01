# AWS システム設計

## 1. システム概要

### 目的と主要機能

AWS（Amazon Web Services）は、コンピューティング、ストレージ、ネットワークなどのクラウドインフラサービスを提供するプラットフォームです。

**主要機能**:
- 仮想マシン（EC2）
- オブジェクトストレージ（S3）
- データベース（RDS、DynamoDB）
- コンテナオーケストレーション（ECS、EKS）
- サーバーレス（Lambda）
- CDN（CloudFront）

### ユーザースケール

- **アクティブアカウント数**: 約100万アカウント
- **1日のリクエスト数**: 約数兆リクエスト
- **総ストレージ**: 約数エクサバイト
- **データセンター数**: 約200（世界中）

## 2. 機能要件

### コア機能

1. **コンピューティング**
   - 仮想マシンの起動と管理
   - オートスケーリング

2. **ストレージ**
   - オブジェクトストレージ
   - ブロックストレージ
   - ファイルストレージ

3. **ネットワーク**
   - VPC（Virtual Private Cloud）
   - ロードバランサー
   - CDN

4. **データベース**
   - リレーショナルデータベース
   - NoSQLデータベース
   - データベースの自動バックアップ

### 非機能要件

- **可用性**: 99.99%以上（SLA）
- **パフォーマンス**:
  - API応答: < 100ms
  - 仮想マシン起動: < 1分
- **スケーラビリティ**: 自動スケーリング
- **セキュリティ**: 強固なセキュリティとコンプライアンス

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (AWS Console, CLI, SDK)
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
│  EC2        │   │  S3          │   │  RDS        │
│  Service    │   │  Service     │   │  Service    │
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
2. **EC2 Service**: 仮想マシンの管理
3. **S3 Service**: オブジェクトストレージの管理
4. **RDS Service**: リレーショナルデータベースの管理
5. **Resource Management**: 物理リソースの管理

## 4. データモデル設計

### Instances テーブル

```sql
CREATE TABLE instances (
    instance_id VARCHAR(50) PRIMARY KEY,
    account_id BIGINT NOT NULL,
    instance_type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'running', 'stopped', 'terminated') NOT NULL,
    availability_zone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_account_id (account_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### S3_Objects テーブル

```sql
CREATE TABLE s3_objects (
    object_key VARCHAR(2000) PRIMARY KEY,
    bucket_name VARCHAR(255) NOT NULL,
    account_id BIGINT NOT NULL,
    file_size BIGINT NOT NULL,
    content_type VARCHAR(100),
    storage_class VARCHAR(50) DEFAULT 'STANDARD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_bucket_name (bucket_name),
    INDEX idx_account_id (account_id)
) ENGINE=InnoDB;
```

## 5. API設計

### EC2インスタンス起動

```
POST /api/v1/ec2/instances
Authorization: AWS4-HMAC-SHA256 <credentials>
Content-Type: application/json

Request Body:
{
  "instance_type": "t3.micro",
  "image_id": "ami-12345678",
  "key_name": "my-key",
  "security_groups": ["sg-12345678"]
}

Response (200 OK):
{
  "instance_id": "i-1234567890abcdef0",
  "status": "pending"
}
```

### S3オブジェクトアップロード

```
PUT /api/v1/s3/{bucket_name}/{object_key}
Authorization: AWS4-HMAC-SHA256 <credentials>
Content-Type: application/octet-stream

Request Body: <file content>

Response (200 OK):
{
  "etag": "\"abc123...\"",
  "location": "https://s3.amazonaws.com/bucket/key"
}
```

## 6. スケーラビリティ設計

### マルチテナンシー

- **リソース分離**: 各アカウントのリソースを分離
- **仮想化**: ハイパーバイザーで仮想化
- **オーバーサブスクリプション**: リソースの効率的な利用

### 自動スケーリング

- **オートスケーリンググループ**: 需要に応じて自動スケール
- **スケーリングポリシー**: CPU、メモリ、ネットワークに基づくスケーリング

## 7. レイテンシ最適化

### API応答の最適化

- **キャッシング**: API応答をキャッシュ
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: CloudFrontで静的コンテンツを配信

## 8. コスト最適化

### インフラコストの見積もり

- **データセンター**: 約 **$1,000,000,000/年**（建設・運用）
- **サーバー**: 約 **$10,000,000,000/年**（数百万台）
- **ネットワーク**: 約 **$2,000,000,000/年**
- **合計**: 約 **$13,000,000,000/年**

### コストモデル

- **従量課金**: 使用した分だけ課金
- **リザーブドインスタンス**: 1年契約で最大72%割引
- **Spotインスタンス**: 最大90%割引

## 9. 可用性・信頼性

### 障害対策

- **マルチAZ**: 複数のアベイラビリティゾーンにデプロイ
- **マルチリージョン**: 複数のリージョンにデプロイ
- **SLA**: 99.99%の可用性を保証

### 冗長化

- **データベース**: マルチAZ配置
- **ストレージ**: 複数のデータセンターにレプリケート
- **ネットワーク**: 複数のパスで冗長化

## 10. セキュリティ

### セキュリティ対策

- **IAM**: アイデンティティとアクセス管理
- **VPC**: 仮想プライベートクラウド
- **暗号化**: 転送中と保存時の暗号化
- **コンプライアンス**: SOC 2、ISO 27001、PCI DSS

## 11. UX最適化

### パフォーマンス指標

- **API応答**: < 100ms
- **仮想マシン起動**: < 1分
- **コンソール読み込み**: < 2秒

## 12. 実装例

### EC2サービス（疑似コード）

```python
class EC2Service:
    def __init__(self, hypervisor_manager, db):
        self.hypervisor_manager = hypervisor_manager
        self.db = db
    
    async def launch_instance(self, account_id: int, instance_type: str, image_id: str):
        # 利用可能なホストを選択
        host = await self.hypervisor_manager.select_host(instance_type)
        
        # 仮想マシンを起動
        instance_id = await self.hypervisor_manager.launch_vm(
            host=host,
            instance_type=instance_type,
            image_id=image_id
        )
        
        # データベースに記録
        await self.db.create_instance(
            instance_id=instance_id,
            account_id=account_id,
            instance_type=instance_type,
            status="pending"
        )
        
        return {
            "instance_id": instance_id,
            "status": "pending"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日のAPIリクエスト**: 約数兆回
- **1秒あたり**: 約数千万回/秒

### ストレージ見積もり

- **総ストレージ**: 約数エクサバイト
- **S3オブジェクト数**: 約数兆オブジェクト

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マルチテナンシー**: リソースの効率的な分離
2. **自動スケーリング**: 需要に応じた自動スケール
3. **セキュリティ**: 強固なセキュリティとコンプライアンス

## 15. 関連システム

### 類似システムへのリンク

- [Azure](azure_design.md) - Microsoft Azure
- [GCP](gcp_design.md) - Google Cloud Platform

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [共通パターン](../17_common_patterns/README.md)でシステム設計の共通パターンを学ぶ

