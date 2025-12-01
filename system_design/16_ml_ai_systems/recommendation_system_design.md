# Recommendation System システム設計

## 1. システム概要

### 目的と主要機能

レコメンデーションシステムは、ユーザーの行動履歴や好みに基づいて、ユーザーに関連するコンテンツやアイテムを推薦するシステムです。

**主要機能**:
- コンテンツベースフィルタリング
- 協調フィルタリング
- ハイブリッドレコメンデーション
- リアルタイムレコメンデーション
- A/Bテスト
- パーソナライゼーション

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約10億人
- **1日の推薦リクエスト数**: 約100億回
- **1秒あたりの推薦リクエスト数**: 約120万リクエスト/秒（ピーク時）
- **推薦アイテム数**: 約1億アイテム

### 主要なユースケース

1. **コンテンツ推薦**: ユーザーに関連するコンテンツを推薦
2. **商品推薦**: ユーザーに関連する商品を推薦
3. **パーソナライゼーション**: ユーザーに合わせたパーソナライズ
4. **リアルタイム推薦**: リアルタイムでの推薦
5. **A/Bテスト**: 推薦アルゴリズムのA/Bテスト

## 2. 機能要件

### コア機能

1. **コンテンツベースフィルタリング**
   - アイテムの特徴量抽出
   - ユーザープロファイルの構築
   - 類似度計算

2. **協調フィルタリング**
   - ユーザーベース協調フィルタリング
   - アイテムベース協調フィルタリング
   - マトリックス分解

3. **ハイブリッドレコメンデーション**
   - 複数のアルゴリズムの組み合わせ
   - 重み付け
   - アンサンブル

4. **リアルタイムレコメンデーション**
   - リアルタイムでの推薦
   - ストリーミング処理
   - 低レイテンシ

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 推薦生成: < 100ms
  - リアルタイム推薦: < 50ms
- **スケーラビリティ**: 水平スケーリング可能
- **精度**: 高い推薦精度

### 優先順位付け

1. **P0（必須）**: 協調フィルタリング、コンテンツベースフィルタリング、リアルタイム推薦
2. **P1（重要）**: ハイブリッドレコメンデーション、A/Bテスト、パーソナライゼーション
3. **P2（望ましい）**: 高度な機械学習モデル、深層学習

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                      │
└──────┬──────────────────────────────────────┘
       │
┌──────▼─────────────────────────────────────▼──────┐
│              Recommendation Service                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Content  │  │Collaborative│ │ Real-time│        │
│  │ Based    │  │ Filtering │  │ Service │        │
│  │ Service  │  │ Service   │  │          │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Hybrid Service                   │         │
│  │      A/B Testing Service              │         │
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
│         ML Model Serving (TensorFlow Serving)    │
│         Feature Store                            │
│         Spark (Batch Processing)                 │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Recommendation Service**: 推薦リクエストの処理
2. **Content Based Service**: コンテンツベースフィルタリング
3. **Collaborative Filtering Service**: 協調フィルタリング
4. **Real-time Service**: リアルタイム推薦
5. **Hybrid Service**: ハイブリッドレコメンデーション
6. **A/B Testing Service**: A/Bテスト
7. **ML Model Serving**: 機械学習モデルの推論
8. **Feature Store**: 特徴量の保存・管理
9. **Spark**: バッチ処理

### データフロー

#### 推薦生成のフロー

```
1. Client → Load Balancer → Recommendation Service
2. Recommendation Service:
   a. ユーザープロファイルを取得
   b. Content Based Serviceで推薦を生成
   c. Collaborative Filtering Serviceで推薦を生成
   d. Hybrid Serviceで推薦を統合
   e. A/B Testing Serviceでアルゴリズムを選択
   f. 推薦結果を返す
```

## 4. データモデル設計

### 主要なエンティティ

#### User_Profiles テーブル

```sql
CREATE TABLE user_profiles (
    user_id BIGINT PRIMARY KEY,
    preferences JSON,
    feature_vector BLOB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_last_updated (last_updated)
) ENGINE=InnoDB;
```

#### User_Interactions テーブル

```sql
CREATE TABLE user_interactions (
    interaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    interaction_type ENUM('view', 'click', 'purchase', 'rating') NOT NULL,
    rating INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_timestamp (user_id, timestamp DESC),
    INDEX idx_item_id (item_id)
) ENGINE=InnoDB;
```

#### Recommendations テーブル

```sql
CREATE TABLE recommendations (
    recommendation_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    score DECIMAL(10, 6) NOT NULL,
    algorithm_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_score (user_id, score DESC),
    INDEX idx_item_id (item_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ユーザープロファイル、インタラクションの永続化
- **Redis**:
  - 理由: リアルタイムデータ、推薦結果のキャッシング
  - 用途: 推薦結果、ユーザープロファイルのキャッシング
- **Feature Store**:
  - 理由: 特徴量の保存・管理
  - 用途: 機械学習モデルの特徴量

### スキーマ設計の考慮事項

1. **パーティショニング**: `user_interactions`テーブルは`user_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: インタラクションは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 推薦取得

```
GET /api/v1/recommendations?user_id=1234567890&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "recommendations": [
    {
      "item_id": 9876543210,
      "score": 0.95,
      "algorithm": "collaborative_filtering"
    }
  ],
  "total_results": 100
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT
- **認可**: ユーザーは自分の推薦のみアクセス可能
- **レート制限**: 
  - 推薦取得: 100回/分
  - インタラクション送信: 1,000回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### ML Model Serving

- **TensorFlow Serving**: 機械学習モデルの推論
- **動的スケーリング**: 需要に応じてモデルサーバーを起動・停止
- **地理的分散**: 複数のリージョンにモデルサーバーを配置

#### データベースシャーディング

**シャーディング戦略**: User IDベースのシャーディング

```
Shard 1: user_id % 8 == 0
Shard 2: user_id % 8 == 1
...
Shard 8: user_id % 8 == 7
```

**シャーディングキー**: `user_id`
- ユーザープロファイルは`user_id`でシャーディング

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
   - 用途: 推薦結果、ユーザープロファイル
   - TTL: 5-15分

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ML Model推論**: 機械学習モデルの推論時間
2. **特徴量取得**: 特徴量の取得時間
3. **推薦生成**: 推薦アルゴリズムの実行時間

### ML Model推論最適化

1. **モデル最適化**: モデルの量子化と最適化
2. **バッチ推論**: 複数のリクエストをバッチで処理
3. **キャッシング**: 推論結果をキャッシュ

### 推薦生成最適化

1. **事前計算**: 推薦を事前計算してキャッシュ
2. **並列処理**: 複数のアルゴリズムを並列で実行
3. **キャッシング**: 推薦結果をキャッシュ

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 10億人
- **1日の推薦リクエスト数**: 100億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 800台
- コスト: $0.192/時間 × 800台 × 730時間 = **$112,128/月**

**ML Model Serving**:
- EC2インスタンス: g4dn.xlarge (4 vCPU, 16 GB RAM, GPU)
- インスタンス数: 200台
- コスト: $0.526/時間 × 200台 × 730時間 = **$76,796/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**Sparkクラスター**:
- EMRクラスター: 100ノード
- コスト: $0.27/時間 × 100ノード × 730時間 = **$19,710/月**

**合計**: 約 **$249,149/月**（約2,989,788ドル/年）

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
   - ML Model Servingのヘルスチェック

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
2. **認可**: ユーザーは自分の推薦のみアクセス可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム

### プライバシー

1. **データ匿名化**: ユーザーデータの匿名化
2. **差分プライバシー**: 差分プライバシーの実装
3. **GDPR準拠**: GDPR準拠のデータ処理

## 11. UX最適化

### パフォーマンス指標

- **推薦生成**: < 100ms
- **リアルタイム推薦**: < 50ms
- **推薦精度**: 高い推薦精度

## 12. 実装例

### 推薦サービス（疑似コード）

```python
class RecommendationService:
    def __init__(self, content_based_service, collaborative_service, 
                 hybrid_service, cache, ml_model_serving):
        self.content_based_service = content_based_service
        self.collaborative_service = collaborative_service
        self.hybrid_service = hybrid_service
        self.cache = cache
        self.ml_model_serving = ml_model_serving
    
    async def get_recommendations(self, user_id: int, limit: int = 20):
        # キャッシュを確認
        cache_key = f"recommendations:{user_id}"
        cached_recommendations = await self.cache.get(cache_key)
        
        if cached_recommendations:
            return cached_recommendations
        
        # ユーザープロファイルを取得
        user_profile = await self.get_user_profile(user_id)
        
        # 複数のアルゴリズムで推薦を生成（並列）
        content_based_recs = await self.content_based_service.get_recommendations(
            user_id=user_id,
            user_profile=user_profile,
            limit=limit
        )
        
        collaborative_recs = await self.collaborative_service.get_recommendations(
            user_id=user_id,
            limit=limit
        )
        
        # ML Modelで推薦を生成
        ml_recs = await self.ml_model_serving.predict(
            user_id=user_id,
            user_profile=user_profile
        )
        
        # ハイブリッドサービスで推薦を統合
        recommendations = await self.hybrid_service.combine_recommendations(
            content_based=content_based_recs,
            collaborative=collaborative_recs,
            ml=ml_recs,
            limit=limit
        )
        
        # キャッシュに保存
        await self.cache.set(cache_key, recommendations, ttl=300)
        
        return recommendations
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の推薦リクエスト数**: 100億回
- **1時間あたり**: 100億 / 24 = 約4,167億回
- **1秒あたり**: 4,167億 / 3600 = 約1,157万回/秒
- **ピーク時（2倍）**: 約2,314万回/秒

### ストレージ見積もり

#### インタラクションデータストレージ

- **1インタラクションあたりのサイズ**: 約500バイト
- **1日のインタラクション数**: 500億回
- **1日のストレージ**: 500億 × 500バイト = 25 TB
- **1年のストレージ**: 25 TB × 365 = 約9.125 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **ハイブリッドアプローチ**: 複数のアルゴリズムを組み合わせ
2. **リアルタイム処理**: リアルタイムでの推薦生成
3. **キャッシング**: 推薦結果を積極的にキャッシュ
4. **A/Bテスト**: アルゴリズムのA/Bテスト
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **コールドスタート問題**:
   - 問題: 新規ユーザーや新規アイテムへの推薦が困難
   - 解決策: コンテンツベースフィルタリングとデフォルト推薦

2. **スパース性問題**:
   - 問題: ユーザーとアイテムのマトリックスがスパース
   - 解決策: マトリックス分解と深層学習

## 15. 関連システム

### 類似システムへのリンク

- [ML Inference](ml_inference_design.md) - 機械学習推論システム
- [Chatbot](chatbot_design.md) - チャットボットシステム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [ML Inference](ml_inference_design.md)で機械学習推論システムの設計を学ぶ

