# ML Inference システム設計

## 1. システム概要

### 目的と主要機能

ML推論システムは、機械学習モデルを本番環境で推論するためのシステムです。低レイテンシ、高スループット、高可用性を提供します。

**主要機能**:
- モデル推論
- バッチ推論
- リアルタイム推論
- モデルバージョン管理
- A/Bテスト
- 特徴量管理

### ユーザースケール

- **1日の推論リクエスト数**: 約1,000億回
- **1秒あたりの推論リクエスト数**: 約1,200万リクエスト/秒（ピーク時）
- **デプロイ済みモデル数**: 約10,000モデル

### 主要なユースケース

1. **リアルタイム推論**: リアルタイムでの推論
2. **バッチ推論**: バッチでの推論
3. **モデルデプロイ**: モデルのデプロイと管理
4. **A/Bテスト**: モデルのA/Bテスト
5. **特徴量管理**: 特徴量の管理と提供

## 2. 機能要件

### コア機能

1. **モデル推論**
   - リアルタイム推論
   - バッチ推論
   - ストリーミング推論

2. **モデル管理**
   - モデルバージョン管理
   - モデルのデプロイ
   - モデルのロールバック

3. **特徴量管理**
   - 特徴量の保存・取得
   - 特徴量の変換
   - 特徴量のキャッシング

4. **A/Bテスト**
   - モデルのA/Bテスト
   - トラフィック分割
   - メトリクス収集

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - リアルタイム推論: < 50ms
  - バッチ推論: 高スループット
- **スケーラビリティ**: 水平スケーリング可能
- **精度**: 高い推論精度

### 優先順位付け

1. **P0（必須）**: モデル推論、モデル管理、特徴量管理
2. **P1（重要）**: A/Bテスト、モニタリング、ログ
3. **P2（望ましい）**: 高度な機能、自動スケーリング

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps, Services)
└──────┬──────┘
       │ HTTPS/gRPC
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                      │
└──────┬──────────────────────────────────────┘
       │
┌──────▼─────────────────────────────────────▼──────┐
│              Inference Service                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Request  │  │ Feature  │  │ Model    │        │
│  │ Router   │  │ Store    │  │ Serving  │        │
│  │          │  │          │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      A/B Testing Service             │         │
│  │      Monitoring Service              │         │
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
│         Model Serving (TensorFlow Serving)        │
│         Feature Store                            │
│         Batch Processing (Spark)                 │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Inference Service**: 推論リクエストの処理
2. **Request Router**: リクエストのルーティング
3. **Feature Store**: 特徴量の保存・取得
4. **Model Serving**: 機械学習モデルの推論
5. **A/B Testing Service**: A/Bテスト
6. **Monitoring Service**: モニタリング

### データフロー

#### 推論のフロー

```
1. Client → Load Balancer → Inference Service
2. Inference Service:
   a. Request Routerでモデルを選択
   b. Feature Storeから特徴量を取得
   c. Model Servingで推論を実行
   d. A/B Testing Serviceでトラフィックを分割
   e. 推論結果を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Models テーブル

```sql
CREATE TABLE models (
    model_id BIGINT PRIMARY KEY,
    model_name VARCHAR(200) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    model_path VARCHAR(500) NOT NULL,
    model_type ENUM('tensorflow', 'pytorch', 'onnx') NOT NULL,
    status ENUM('training', 'deployed', 'archived') DEFAULT 'training',
    accuracy DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model_name_version (model_name, model_version),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

#### Inference_Requests テーブル

```sql
CREATE TABLE inference_requests (
    request_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    model_id BIGINT NOT NULL,
    input_data JSON NOT NULL,
    output_data JSON,
    latency_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(model_id),
    INDEX idx_model_id_created_at (model_id, created_at DESC)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: モデル情報、推論リクエストの永続化
- **Redis**:
  - 理由: リアルタイムデータ、特徴量のキャッシング
  - 用途: 特徴量、推論結果のキャッシング
- **Feature Store**:
  - 理由: 特徴量の保存・管理
  - 用途: 機械学習モデルの特徴量

## 5. API設計

### 主要なAPIエンドポイント

#### 推論リクエスト

```
POST /api/v1/models/{model_id}/predict
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "features": {
    "feature1": 1.0,
    "feature2": 2.0
  }
}

Response (200 OK):
{
  "prediction": 0.95,
  "confidence": 0.98,
  "latency_ms": 25
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: API Keyベースのアクセス制御
- **レート制限**: 
  - 推論リクエスト: 1,000回/秒
  - バッチ推論: 100回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### Model Serving

- **TensorFlow Serving**: 機械学習モデルの推論
- **動的スケーリング**: 需要に応じてモデルサーバーを起動・停止
- **地理的分散**: 複数のリージョンにモデルサーバーを配置

#### データベースシャーディング

**シャーディング戦略**: Model IDベースのシャーディング

```
Shard 1: model_id % 8 == 0
Shard 2: model_id % 8 == 1
...
Shard 8: model_id % 8 == 7
```

**シャーディングキー**: `model_id`
- 推論リクエストは`model_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 特徴量、推論結果
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **モデル推論**: 機械学習モデルの推論時間
2. **特徴量取得**: 特徴量の取得時間
3. **ネットワーク**: クライアントとサーバー間の距離

### モデル推論最適化

1. **モデル最適化**: モデルの量子化と最適化
2. **バッチ推論**: 複数のリクエストをバッチで処理
3. **GPU使用**: GPUでの推論高速化
4. **キャッシング**: 推論結果をキャッシュ

### 特徴量取得最適化

1. **Feature Store**: 特徴量の高速取得
2. **キャッシング**: 特徴量をキャッシュ
3. **事前計算**: 特徴量を事前計算

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **1日の推論リクエスト数**: 1,000億回
- **デプロイ済みモデル数**: 10,000モデル

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**Model Serving (GPU)**:
- EC2インスタンス: g4dn.xlarge (4 vCPU, 16 GB RAM, GPU)
- インスタンス数: 500台
- コスト: $0.526/時間 × 500台 × 730時間 = **$191,990/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**合計**: 約 **$372,665/月**（約4,471,980ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **モデル最適化**: モデルの量子化と最適化でコスト削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Model Servingのヘルスチェック

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

2. **モデルバックアップ**:
   - モデルのバージョン管理
   - モデルのバックアップ

## 10. セキュリティ

### 認証・認可

1. **認証**: OAuth 2.0 / JWT
2. **認可**: API Keyベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - モデル: 暗号化されたストレージ

## 11. UX最適化

### パフォーマンス指標

- **リアルタイム推論**: < 50ms
- **バッチ推論**: 高スループット
- **推論精度**: 高い推論精度

## 12. 実装例

### 推論サービス（疑似コード）

```python
class InferenceService:
    def __init__(self, request_router, feature_store, model_serving, cache, ab_testing_service):
        self.request_router = request_router
        self.feature_store = feature_store
        self.model_serving = model_serving
        self.cache = cache
        self.ab_testing_service = ab_testing_service
    
    async def predict(self, model_id: int, input_data: dict):
        # A/Bテストでモデルバージョンを選択
        model_version = await self.ab_testing_service.select_model_version(
            model_id=model_id
        )
        
        # キャッシュを確認
        cache_key = self.get_cache_key(model_id, model_version, input_data)
        cached_result = await self.cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        # 特徴量を取得
        features = await self.feature_store.get_features(
            input_data=input_data
        )
        
        # モデル推論を実行
        start_time = time.time()
        prediction = await self.model_serving.predict(
            model_id=model_id,
            model_version=model_version,
            features=features
        )
        latency_ms = (time.time() - start_time) * 1000
        
        # 結果をキャッシュ
        result = {
            "prediction": prediction,
            "latency_ms": latency_ms
        }
        await self.cache.set(cache_key, result, ttl=300)
        
        return result
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の推論リクエスト数**: 1,000億回
- **1時間あたり**: 1,000億 / 24 = 約4,167億回
- **1秒あたり**: 4,167億 / 3600 = 約1,157万回/秒
- **ピーク時（2倍）**: 約2,314万回/秒

### ストレージ見積もり

#### モデルストレージ

- **1モデルあたりの平均サイズ**: 100 MB
- **デプロイ済みモデル数**: 10,000モデル
- **合計ストレージ**: 10,000 × 100 MB = 1 TB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **モデル最適化**: モデルの量子化と最適化
2. **バッチ推論**: 複数のリクエストをバッチで処理
3. **キャッシング**: 推論結果を積極的にキャッシュ
4. **A/Bテスト**: モデルのA/Bテスト
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **レイテンシ**:
   - 問題: 推論のレイテンシが高い
   - 解決策: モデル最適化とGPU使用

2. **スケーラビリティ**:
   - 問題: 推論サーバーのリソース不足
   - 解決策: 動的スケーリングとオートスケーリング

## 15. 関連システム

### 類似システムへのリンク

- [Recommendation System](recommendation_system_design.md) - レコメンデーションシステム
- [Chatbot](chatbot_design.md) - チャットボットシステム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Chatbot](chatbot_design.md)でチャットボットシステムの設計を学ぶ

