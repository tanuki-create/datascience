# Google検索 システム設計

## 1. システム概要

### 目的と主要機能

Google検索は、Web上の情報をインデックス化し、ユーザーのクエリに対して関連性の高い結果を返す検索エンジンです。

**主要機能**:
- Webページのクローリング
- インデックス作成
- 検索クエリの処理
- ランキングアルゴリズム
- パーソナライゼーション

### ユーザースケール

- **1日の検索クエリ数**: 約35億回
- **1秒あたりの検索クエリ**: 約40,000回/秒（平均）
- **ピーク時**: 約100,000回/秒
- **インデックス化されたページ数**: 約1,300億ページ
- **1日のクロール数**: 約数十億ページ

### 主要なユースケース

1. **Web検索**: ユーザーがキーワードで検索
2. **画像検索**: 画像で検索
3. **動画検索**: 動画で検索
4. **ニュース検索**: ニュースで検索

## 2. 機能要件

### コア機能

1. **Webクローリング**
   - 数十億ページのクローリング
   - クロール頻度の最適化

2. **インデックス作成**
   - 大規模なインデックスの構築
   - インデックスの更新

3. **検索処理**
   - 低レイテンシでの検索結果返却
   - 関連性の高い結果のランキング

4. **ランキングアルゴリズム**
   - PageRankアルゴリズム
   - 機械学習によるランキング

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - 検索結果返却: < 200ms
  - インデックス更新: リアルタイムに近い
- **スケーラビリティ**: 水平スケーリング可能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web, Mobile)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         Load Balancer                       │
└──────┬──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
│  API Gateway│   │  API Gateway│   │  API Gateway│
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                  │
       ├─────────────────┴──────────────────┤
       │                                     │
┌──────▼─────────────────────────────────────▼──────┐
│              Search Servers                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Query    │  │ Ranking  │  │ Result   │        │
│  │ Parser   │  │ Service  │  │ Formatter│        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼──────────────┼──────────────┼──────────────┘
        │             │             │
┌───────▼─────────────▼─────────────▼──────┐
│         Index Servers (Distributed)       │
│         (Inverted Index)                  │
└───────────────────────────────────────────┘
        │
┌───────▼───────────────────────────────────┐
│         Crawler Service                    │
│  ┌──────────┐  ┌──────────┐              │
│  │ URL      │  │ Content  │              │
│  │ Queue    │  │ Parser   │              │
│  └────┬─────┘  └────┬─────┘              │
└───────┼──────────────┼──────────────────────┘
        │             │
┌───────▼─────────────▼──────┐
│         Web Pages          │
└────────────────────────────┘
```

### コンポーネントの説明

1. **Query Parser**: 検索クエリの解析
2. **Ranking Service**: 検索結果のランキング
3. **Index Servers**: 分散インデックスサーバー
4. **Crawler Service**: Webページのクローリング

## 4. データモデル設計

### インデックス構造

#### Inverted Index

```
Term: "python"
Documents: [
  {doc_id: 1, frequency: 5, positions: [10, 25, 50, 100, 200]},
  {doc_id: 2, frequency: 3, positions: [15, 30, 45]},
  ...
]
```

#### Document Metadata

```sql
CREATE TABLE documents (
    doc_id BIGINT PRIMARY KEY,
    url VARCHAR(2048) UNIQUE NOT NULL,
    title VARCHAR(500),
    content_hash VARCHAR(64),
    page_rank DECIMAL(10, 8),
    last_crawled_at TIMESTAMP,
    INDEX idx_url (url(255)),
    INDEX idx_last_crawled (last_crawled_at)
) ENGINE=InnoDB;
```

## 5. API設計

### 検索API

```
GET /search?q=python+programming&limit=10
Authorization: Bearer <token>

Response (200 OK):
{
  "results": [
    {
      "title": "Python Programming",
      "url": "https://example.com/python",
      "snippet": "Learn Python programming...",
      "rank": 1
    }
  ],
  "total_results": 1000000,
  "search_time_ms": 150
}
```

## 6. スケーラビリティ設計

### インデックスの分散

- **シャーディング**: 用語（Term）でシャーディング
- **レプリケーション**: 各シャードを複数レプリケート

### クローラーのスケーリング

- **分散クローリング**: 複数のクローラーノードで並列クローリング
- **URLキュー**: 分散キューでURLを管理

## 7. レイテンシ最適化

### 検索の最適化

- **インデックスキャッシング**: 頻繁に検索される用語をキャッシュ
- **結果キャッシング**: 人気検索クエリの結果をキャッシュ
- **並列検索**: 複数のインデックスサーバーで並列検索

## 8. コスト最適化

### インフラコストの見積もり

- **インデックスサーバー**: 約 **$10,000,000/月**
- **クローラー**: 約 **$5,000,000/月**
- **ストレージ**: 約 **$50,000,000/月**（大規模インデックス）
- **合計**: 約 **$65,000,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにインデックスをレプリケート
- **冗長化**: 各コンポーネントを冗長化

## 10. セキュリティ

### セキュリティ対策

- **DDoS対策**: レート制限とCDN
- **ボット対策**: CAPTCHAとボット検出

## 11. UX最適化

### パフォーマンス指標

- **検索結果返却**: < 200ms
- **オートコンプリート**: < 100ms

## 12. 実装例

### 検索サービス（疑似コード）

```python
class SearchService:
    def __init__(self, index_servers, ranking_service):
        self.index_servers = index_servers
        self.ranking_service = ranking_service
    
    async def search(self, query: str, limit: int = 10):
        # クエリを解析
        terms = self.parse_query(query)
        
        # 各インデックスサーバーで並列検索
        results = await asyncio.gather(*[
            server.search(term) for term in terms
        ])
        
        # 結果をマージ
        merged_results = self.merge_results(results)
        
        # ランキング
        ranked_results = await self.ranking_service.rank(
            merged_results,
            query
        )
        
        return ranked_results[:limit]
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日の検索クエリ**: 35億回
- **1秒あたり**: 約40,000回/秒（平均）
- **ピーク時**: 約100,000回/秒

### ストレージ見積もり

- **インデックス化されたページ**: 1,300億ページ
- **1ページあたりのインデックスサイズ**: 約1 KB
- **合計インデックスサイズ**: 約1.3 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **分散インデックス**: 用語でシャーディング
2. **並列検索**: 複数のインデックスサーバーで並列検索
3. **キャッシング**: 人気検索クエリをキャッシュ

## 15. 関連システム

### 類似システムへのリンク

- [Bing](bing_design.md) - Microsoftの検索エンジン
- [DuckDuckGo](duckduckgo_design.md) - プライバシー重視の検索エンジン

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [WhatsApp](whatsapp_design.md)でメッセージングシステムの設計を学ぶ

