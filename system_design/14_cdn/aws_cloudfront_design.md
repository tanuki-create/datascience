# AWS CloudFront システム設計

## 1. システム概要

### 目的と主要機能

AWS CloudFrontは、Amazon Web Servicesが提供するCDN（Content Delivery Network）サービスです。AWSサービスと統合されたコンテンツ配信とセキュリティサービスを提供します。

**主要機能**:
- CDN（コンテンツ配信）
- DDoS保護（AWS Shield統合）
- WAF（Web Application Firewall統合）
- SSL/TLS証明書（AWS Certificate Manager統合）
- Lambda@Edge（エッジでのLambda実行）
- 動画配信
- リアルタイムログ

### ユーザースケール

- **アクティブディストリビューション数**: 約100万ディストリビューション
- **1日のリクエスト数**: 約5,000億リクエスト
- **1秒あたりのリクエスト数**: 約600万リクエスト/秒（ピーク時）
- **エッジロケーション数**: 約450（世界中）

### 主要なユースケース

1. **コンテンツ配信**: S3、EC2、ELBからのコンテンツ配信
2. **動画配信**: 動画コンテンツの配信
3. **API配信**: APIの高速配信
4. **DDoS保護**: AWS Shield統合によるDDoS保護
5. **エッジコンピューティング**: Lambda@Edgeでのエッジ処理

## 2. 機能要件

### コア機能

1. **CDN**
   - 静的コンテンツのキャッシング
   - 動的コンテンツの最適化
   - 画像最適化

2. **AWS統合**
   - S3統合
   - EC2統合
   - ELB統合
   - API Gateway統合

3. **Lambda@Edge**
   - エッジでのLambda実行
   - リクエスト/レスポンスのカスタマイズ
   - A/Bテスト

4. **DDoS保護**
   - AWS Shield Standard（無料）
   - AWS Shield Advanced（有料）

5. **WAF統合**
   - AWS WAF統合
   - カスタムルール

### 非機能要件

- **可用性**: 99.99%以上（SLA）
- **パフォーマンス**:
  - コンテンツ配信: < 50ms
  - Lambda@Edge実行: < 100ms
- **スケーラビリティ**: 自動スケーリング
- **セキュリティ**: 強固なセキュリティとコンプライアンス

### 優先順位付け

1. **P0（必須）**: CDN、AWS統合、DDoS保護
2. **P1（重要）**: Lambda@Edge、WAF統合、動画配信
3. **P2（望ましい）**: 高度な分析機能、カスタムルール

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web Browser, Mobile Apps)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         CloudFront Edge Location            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Cache   │  │ Lambda@ │  │  AWS     │ │
│  │  Layer   │  │ Edge     │  │ Shield   │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
└───────┼──────────────┼──────────────┼───────┘
        │             │             │
        │ Cache Miss  │ Blocked     │ Allowed
        │             │             │
┌───────▼─────────────▼─────────────▼───────┐
│         Origin (S3, EC2, ELB, API Gateway) │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **CloudFront Edge Location**: ユーザーに最も近いエッジロケーション
2. **Cache Layer**: コンテンツのキャッシング
3. **Lambda@Edge**: エッジでのLambda実行
4. **AWS Shield**: DDoS保護
5. **Origin**: S3、EC2、ELB、API Gatewayなどのオリジン

### データフロー

#### コンテンツ配信のフロー

```
1. Client → CloudFront Edge Location (Closest to User)
2. CloudFront Edge Location:
   a. Lambda@Edgeでリクエストを処理（オプション）
   b. Cache Layerでコンテンツを確認
   c. キャッシュがあれば返す
   d. キャッシュがなければOriginから取得
   e. Lambda@Edgeでレスポンスを処理（オプション）
   f. コンテンツをキャッシュして返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Distributions テーブル

```sql
CREATE TABLE distributions (
    distribution_id VARCHAR(50) PRIMARY KEY,
    account_id BIGINT NOT NULL,
    domain_name VARCHAR(255) NOT NULL,
    origin_type ENUM('s3', 'ec2', 'elb', 'api_gateway') NOT NULL,
    origin_domain VARCHAR(255) NOT NULL,
    status ENUM('deployed', 'in_progress', 'disabled') DEFAULT 'in_progress',
    ssl_enabled BOOLEAN DEFAULT TRUE,
    waf_enabled BOOLEAN DEFAULT FALSE,
    lambda_edge_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_id (account_id),
    INDEX idx_domain_name (domain_name)
) ENGINE=InnoDB;
```

#### Cache_Behaviors テーブル

```sql
CREATE TABLE cache_behaviors (
    behavior_id BIGINT PRIMARY KEY,
    distribution_id VARCHAR(50) NOT NULL,
    path_pattern VARCHAR(500) NOT NULL,
    cache_ttl INT NOT NULL,
    cache_policy_id VARCHAR(50),
    origin_request_policy_id VARCHAR(50),
    lambda_function_arn VARCHAR(500),
    FOREIGN KEY (distribution_id) REFERENCES distributions(distribution_id),
    INDEX idx_distribution_id (distribution_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（RDS PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ディストリビューション設定、キャッシュ動作の永続化

### スキーマ設計の考慮事項

1. **パーティショニング**: `distributions`テーブルは`account_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: アクセスログは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### ディストリビューション作成

```
POST /api/v1/distributions
Authorization: AWS4-HMAC-SHA256 <signature>
Content-Type: application/json

Request Body:
{
  "origin_domain": "example.s3.amazonaws.com",
  "origin_type": "s3",
  "default_cache_behavior": {
    "cache_policy_id": "658327ea-f89d-4fab-a63d-7e88639e58f6",
    "viewer_protocol_policy": "redirect-to-https"
  }
}

Response (200 OK):
{
  "id": "E1234567890ABC",
  "domain_name": "d1234567890abc.cloudfront.net",
  "status": "in_progress"
}
```

### 認証・認可

- **認証**: AWS Signature Version 4
- **認可**: IAM（Identity and Access Management）
- **レート制限**: 
  - API呼び出し: 1,200回/分
  - キャッシュパージ: 30回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### エッジロケーション

- **地理的分散**: 世界中に約450のエッジロケーションを配置
- **自動スケーリング**: トラフィックに応じて自動スケール
- **ロードバランシング**: Route 53で最適なエッジロケーションにルーティング

#### データベースシャーディング

**シャーディング戦略**: Account IDベースのシャーディング

```
Shard 1: account_id % 8 == 0
Shard 2: account_id % 8 == 1
...
Shard 8: account_id % 8 == 7
```

**シャーディングキー**: `account_id`
- ディストリビューション設定は`account_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: ElastiCache（Redis）で水平スケーリング

### 負荷分散

- **Route 53**: 最適なエッジロケーションにルーティング
- **地理的分散**: 複数のリージョンにデプロイ

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（エッジロケーション内）**: 
   - 用途: 頻繁にアクセスされるコンテンツ
   - TTL: 1時間-24時間

2. **L2 Cache（リージョンキャッシュ）**:
   - 用途: 複数のエッジロケーション間で共有
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **オリジンへのアクセス**: オリジンが遠い場合
2. **Lambda@Edge実行**: Lambda@Edgeの実行時間
3. **SSL/TLSハンドシェイク**: 初回接続時のハンドシェイク

### CDNの活用

- **エッジキャッシング**: ユーザーに近いエッジロケーションでキャッシング
- **地理的分散**: 世界中にエッジロケーションを配置

### Lambda@Edge最適化

1. **軽量な関数**: Lambda@Edge関数を軽量化
2. **キャッシング**: Lambda@Edgeの結果をキャッシュ
3. **並列処理**: 複数のLambda@Edgeを並列で実行

### SSL/TLS最適化

1. **TLS 1.3**: 最新のTLSプロトコルを使用
2. **OCSP Stapling**: OCSP応答をキャッシュ
3. **Session Resumption**: セッション再開をサポート

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **アクティブディストリビューション数**: 100万ディストリビューション
- **1日のリクエスト数**: 5,000億リクエスト

#### サーバーコスト（AWS）

**エッジロケーション**:
- エッジロケーション数: 約450（世界中）
- 1エッジロケーションあたりのコスト: 約$50,000/月
- 合計: 約 **$22,500,000/月**

**データベース**:
- RDS PostgreSQL: 約50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**ネットワーク**:
- データ転送: 20 PB/月
- コスト: $0.085/GB × 20,000,000 GB = **$1,700,000/月**

**合計**: 約 **$24,227,740/月**（約290,732,880ドル/年）

### コスト削減戦略

1. **効率的なキャッシング**: キャッシュヒット率を向上
2. **データ圧縮**: データ転送量を削減
3. **エッジロケーションの最適化**: リソース使用率を向上

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のエッジロケーションにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - エッジロケーションのヘルスチェック
   - オリジンのヘルスチェック

3. **自動フェイルオーバー**:
   - エッジロケーション障害時の自動フェイルオーバー
   - オリジン障害時のフォールバック

### 冗長化戦略

#### エッジロケーション冗長化

- **地理的分散**: 世界中にエッジロケーションを配置
- **自動フェイルオーバー**: エッジロケーション障害時の自動フェイルオーバー

### バックアップ・復旧戦略

1. **データベースバックアップ**:
   - 日次フルバックアップ
   - 継続的なバックアップ（ポイントインタイムリカバリ）
   - バックアップの保存期間: 30日

2. **災害復旧**:
   - RTO（Recovery Time Objective）: 5分
   - RPO（Recovery Point Objective）: 1分

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - AWS Signature Version 4
   - IAM（Identity and Access Management）

2. **認可**:
   - IAMベースのアクセス制御
   - リソースベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ
   - S3: サーバーサイド暗号化

### DDoS対策

1. **AWS Shield Standard**: 基本的なDDoS保護（無料）
2. **AWS Shield Advanced**: 高度なDDoS保護（有料）
3. **自動緩和**: DDoS攻撃の自動検出と緩和

### WAF統合

1. **AWS WAF**: Webアプリケーションファイアウォール統合
2. **カスタムルール**: カスタムWAFルールの作成
3. **マネージドルール**: AWS提供のマネージドルール

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 50ms
- **FCP（First Contentful Paint）**: < 1秒
- **LCP（Largest Contentful Paint）**: < 2秒

### プログレッシブローディング

1. **画像最適化**: 画像の自動最適化
2. **遅延読み込み**: 画像の遅延読み込み

## 12. 実装例

### CloudFrontディストリビューション（疑似コード）

```python
class CloudFrontService:
    def __init__(self, db, cache, lambda_edge_service, origin_client):
        self.db = db
        self.cache = cache
        self.lambda_edge_service = lambda_edge_service
        self.origin_client = origin_client
    
    async def create_distribution(self, account_id: int, origin_domain: str, origin_type: str):
        # ディストリビューションを作成
        distribution_id = await self.db.insert_distribution(
            account_id=account_id,
            origin_domain=origin_domain,
            origin_type=origin_type,
            status='in_progress'
        )
        
        # CloudFront APIでディストリビューションを作成
        cloudfront_response = await self.cloudfront_api.create_distribution(
            origin_domain=origin_domain,
            origin_type=origin_type
        )
        
        # ディストリビューション情報を更新
        await self.db.update_distribution(
            distribution_id=distribution_id,
            cloudfront_id=cloudfront_response['id'],
            domain_name=cloudfront_response['domain_name'],
            status='deployed'
        )
        
        return {
            "id": distribution_id,
            "cloudfront_id": cloudfront_response['id'],
            "domain_name": cloudfront_response['domain_name'],
            "status": "deployed"
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のリクエスト数**: 5,000億リクエスト
- **1時間あたり**: 5,000億 / 24 = 約208億リクエスト
- **1秒あたり**: 208億 / 3600 = 約578万リクエスト/秒
- **ピーク時（2倍）**: 約1,156万リクエスト/秒

### キャッシュヒット率

- **キャッシュヒット率**: 約90%
- **オリジンへのリクエスト**: 5,000億 × 10% = 500億リクエスト/日

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **エッジキャッシング**: ユーザーに近いエッジロケーションでキャッシング
2. **AWS統合**: S3、EC2、ELB、API Gatewayとの統合
3. **Lambda@Edge**: エッジでの処理でレイテンシを削減
4. **モニタリング**: CloudWatchでの包括的なモニタリング
5. **セキュリティ**: AWS ShieldとWAFによる保護

### よくある落とし穴

1. **キャッシュの無効化**:
   - 問題: キャッシュが適切に無効化されない
   - 解決策: キャッシュキーの適切な設計と無効化戦略

2. **Lambda@Edgeのレイテンシ**:
   - 問題: Lambda@Edgeの実行時間が長い
   - 解決策: Lambda@Edge関数の軽量化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Cloudflare](cloudflare_design.md) - CDNプラットフォーム
- [Akamai](akamai_design.md) - CDNプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Zoom](../15_realtime_systems/zoom_design.md)でリアルタイムシステムの設計を学ぶ

