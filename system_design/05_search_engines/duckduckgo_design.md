# DuckDuckGo システム設計

## 1. システム概要

### 目的と主要機能

DuckDuckGoは、プライバシー重視の検索エンジンです。ユーザーの検索履歴を追跡せず、パーソナライズされていない検索結果を提供します。

**主要機能**:
- Web検索
- 画像検索
- 動画検索
- ニュース検索
- インスタントアンサー（Instant Answer）
- プライバシー保護
- トラッキング防止

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約1億人
- **日間アクティブユーザー（DAU）**: 約3,000万人
- **1日の検索クエリ数**: 約1億クエリ
- **1秒あたりの検索クエリ数**: 約1,200クエリ/秒（ピーク時）

### 主要なユースケース

1. **Web検索**: ユーザーがWebページを検索
2. **プライバシー保護**: 検索履歴を追跡しない
3. **インスタントアンサー**: クエリに対する即座の回答
4. **画像検索**: ユーザーが画像を検索
5. **動画検索**: ユーザーが動画を検索

## 2. 機能要件

### コア機能

1. **検索機能**
   - Web検索
   - 画像検索
   - 動画検索
   - ニュース検索

2. **プライバシー保護**
   - 検索履歴の非追跡
   - トラッキング防止
   - 匿名検索

3. **インスタントアンサー**
   - クエリに対する即座の回答
   - 構造化データの表示

4. **ランキング**
   - パーソナライズされていない検索結果
   - 関連性の高い結果のランキング

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: 検索結果は最終的に一貫性を保つ
- **パフォーマンス**:
  - 検索結果表示: < 500ms
  - インスタントアンサー: < 200ms
- **スケーラビリティ**: 水平スケーリング可能
- **プライバシー**: ユーザーデータを追跡しない

### 優先順位付け

1. **P0（必須）**: Web検索、プライバシー保護、ランキング
2. **P1（重要）**: 画像検索、動画検索、インスタントアンサー
3. **P2（望ましい）**: 高度な検索機能、多言語対応

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile Apps)
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
│  │ Web      │  │  Image   │  │ Instant  │        │
│  │ Search   │  │ Search   │  │ Answer   │        │
│  │ Service  │  │ Service  │  │ Service  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Ranking Service                 │         │
│  │      Privacy Service                 │         │
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
│         Search Index (Elasticsearch)              │
│         Image Index                                │
│         CDN (CloudFront/Cloudflare)                │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティング（認証なし）
3. **Application Servers**:
   - **Web Search Service**: Web検索の処理
   - **Image Search Service**: 画像検索の処理
   - **Instant Answer Service**: インスタントアンサーの処理
   - **Ranking Service**: 検索結果のランキング（パーソナライズなし）
   - **Privacy Service**: プライバシー保護の処理
4. **Database**: インスタントアンサーのデータの永続化（検索履歴は保存しない）
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（検索インデックス更新など）
7. **Search Index**: Webページ、画像の検索インデックス
8. **CDN**: 画像の配信

### データフロー

#### Web検索のフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Web Search Service
3. Web Search Service:
   a. クエリを解析・正規化
   b. Privacy Serviceでプライバシーチェック
   c. Cacheから検索結果を取得（キャッシュヒット時）
   d. キャッシュミス時: Search Indexから検索
   e. Ranking Serviceでランキング（パーソナライズなし）
   f. 検索結果を返す
   g. Cacheに保存（検索履歴は保存しない）
```

## 4. データモデル設計

### 主要なエンティティ

#### Instant_Answers テーブル

```sql
CREATE TABLE instant_answers (
    answer_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    query_pattern VARCHAR(500) NOT NULL,
    answer_type ENUM('definition', 'calculation', 'conversion', 'fact') NOT NULL,
    answer_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_query_pattern (query_pattern),
    FULLTEXT INDEX idx_query_pattern_fulltext (query_pattern)
) ENGINE=InnoDB;
```

**注意**: 検索履歴はプライバシー保護のため保存しない

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: インスタントアンサーのデータの永続化
- **Elasticsearch**:
  - 理由: 全文検索、大規模な検索インデックス
  - 用途: Webページ、画像の検索インデックス

### スキーマ設計の考慮事項

1. **プライバシー**: 検索履歴は保存しない
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **匿名化**: ユーザー識別情報は保存しない

## 5. API設計

### 主要なAPIエンドポイント

#### Web検索

```
GET /api/v1/search?q=hello+world&limit=10

Response (200 OK):
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "snippet": "This is an example...",
      "rank": 1
    }
  ],
  "total_results": 1000000,
  "instant_answer": {
    "type": "definition",
    "answer": "Hello world is a common phrase..."
  }
}
```

**注意**: 認証不要、ユーザー識別情報は送信しない

### 認証・認可

- **認証**: なし（パブリックAPI）
- **認可**: なし
- **レート制限**: 
  - 検索: 100リクエスト/分（IPアドレスベース）

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報を保存しない
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 画像をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 検索結果、インスタントアンサー
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 画像
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **検索インデックス**: Elasticsearchクエリの最適化
2. **ランキング**: ランキングアルゴリズムの最適化
3. **インスタントアンサー**: 即座の回答の生成

### CDNの活用

- **画像**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### 検索最適化

1. **キャッシング**: 人気検索クエリの結果をキャッシュ
2. **インデックス最適化**: Elasticsearchインデックスの最適化
3. **並列検索**: 複数の検索タイプを並列で実行

### 非同期処理

#### メッセージキュー（Kafka）

1. **検索インデックス更新**:
   ```
   Topic: index-update
   Partition Key: document_id
   ```

**注意**: 検索履歴は記録しない

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 1億人
- **日間アクティブユーザー**: 3,000万人
- **1日の検索クエリ数**: 1億クエリ

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 200台（リージョン間で分散）
- コスト: $0.192/時間 × 200台 × 730時間 = **$28,032/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 10台（マスター + レプリカ）
- コスト: $0.76/時間 × 10台 × 730時間 = **$5,548/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 20台
- コスト: $0.175/時間 × 20台 × 730時間 = **$2,555/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ**:
- EBS: 50 TB
- コスト: $0.10/GB/月 × 50,000 GB = **$5,000/月**

**ネットワーク**:
- データ転送: 500 TB/月
- コスト: $0.09/GB × 500,000 GB = **$45,000/月**

**合計**: 約 **$97,231/月**（約1,166,772ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
3. **オートスケーリング**: 需要に応じてインスタンス数を調整
4. **キャッシング**: 検索結果のキャッシングでコスト削減
5. **CDN活用**: データ転送コストを削減

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のアベイラビリティゾーンにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - アプリケーションサーバーのヘルスチェック
   - Elasticsearchクラスターのヘルスチェック

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

2. **検索インデックスバックアップ**:
   - Elasticsearchスナップショット
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**: なし（パブリックAPI）
2. **認可**: なし

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム

### プライバシー保護

1. **検索履歴の非追跡**: 検索履歴を保存しない
2. **トラッキング防止**: ユーザーの追跡を防止
3. **匿名化**: ユーザー識別情報を保存しない

### DDoS対策

1. **レート制限**: 
   - IPアドレスベースのレート制限

2. **CDN**: CloudflareまたはAWS Shield
3. **WAF**: Web Application Firewallで悪意のあるリクエストをブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 200ms
- **FCP（First Contentful Paint）**: < 1.8秒
- **LCP（Largest Contentful Paint）**: < 2.5秒
- **検索結果表示**: < 500ms
- **インスタントアンサー**: < 200ms

### プログレッシブローディング

1. **検索結果の遅延読み込み**:
   - 最初の10件を先に表示
   - 残りの結果はスクロール時に読み込み

2. **画像の遅延読み込み**:
   - ビューポートに入るまで画像を読み込まない
   - サムネイルを先に表示

## 12. 実装例

### 検索サービス（疑似コード）

```python
class WebSearchService:
    def __init__(self, search_index, cache, ranking_service, privacy_service):
        self.search_index = search_index
        self.cache = cache
        self.ranking_service = ranking_service
        self.privacy_service = privacy_service
    
    async def search(self, query: str, limit: int = 10):
        # プライバシーチェック（検索履歴は保存しない）
        self.privacy_service.ensure_no_tracking()
        
        # キャッシュから取得を試みる
        cache_key = f"search:{query}:{limit}"
        cached_results = await self.cache.get(cache_key)
        
        if cached_results:
            return cached_results
        
        # 検索インデックスから検索
        raw_results = await self.search_index.search(
            query=query,
            limit=limit * 2  # ランキング用に多めに取得
        )
        
        # ランキング（パーソナライズなし）
        ranked_results = await self.ranking_service.rank(
            query=query,
            results=raw_results,
            limit=limit,
            personalize=False  # パーソナライズなし
        )
        
        # キャッシュに保存（検索履歴は保存しない）
        await self.cache.set(cache_key, ranked_results, ttl=300)
        
        return ranked_results
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の検索クエリ数**: 1億クエリ
- **1時間あたり**: 1億 / 24 = 約416万クエリ
- **1秒あたり**: 416万 / 3600 = 約1,156クエリ/秒
- **ピーク時（3倍）**: 約3,468クエリ/秒

### ストレージ見積もり

#### 検索インデックスストレージ

- **Webページ数**: 100億ページ
- **1ページあたりのインデックスサイズ**: 約10 KB
- **合計インデックスサイズ**: 100億 × 10 KB = 1 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **プライバシー保護**: 検索履歴を保存しない
4. **キャッシング**: 人気検索クエリの結果をキャッシュ
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **プライバシー保護の実装**:
   - 問題: 意図せずユーザーを追跡してしまう
   - 解決策: 検索履歴を保存しない、ユーザー識別情報を使用しない

2. **検索のレイテンシ**:
   - 問題: Elasticsearchクエリが遅い
   - 解決策: インデックスの最適化とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Google検索](google_search_design.md) - 検索エンジン
- [Bing](bing_design.md) - 検索エンジン

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [Search Index](../17_common_patterns/database_sharding.md) - 検索インデックス

---

**次のステップ**: [Google Maps](../06_maps_navigation/google_maps_design.md)でマップ・ナビゲーションシステムの設計を学ぶ

