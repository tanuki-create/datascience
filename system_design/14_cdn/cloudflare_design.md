# Cloudflare システム設計

## 1. システム概要

### 目的と主要機能

Cloudflareは、CDN（Content Delivery Network）とセキュリティサービスを提供するプラットフォームです。Webサイトのパフォーマンス向上とセキュリティ保護を提供します。

**主要機能**:
- CDN（コンテンツ配信）
- DDoS保護
- WAF（Web Application Firewall）
- SSL/TLS証明書
- DNSサービス
- ボット管理
- レート制限

### ユーザースケール

- **アクティブドメイン数**: 約2,000万ドメイン
- **1日のリクエスト数**: 約1兆リクエスト
- **1秒あたりのリクエスト数**: 約1,200万リクエスト/秒（ピーク時）
- **エッジサーバー数**: 約300（世界中）

### 主要なユースケース

1. **コンテンツ配信**: ユーザーにコンテンツを高速配信
2. **DDoS保護**: DDoS攻撃から保護
3. **WAF**: Webアプリケーションの保護
4. **SSL/TLS**: 暗号化通信の提供
5. **DNS**: DNSクエリの高速解決

## 2. 機能要件

### コア機能

1. **CDN**
   - 静的コンテンツのキャッシング
   - 動的コンテンツの最適化
   - 画像最適化

2. **DDoS保護**
   - レイヤー3/4 DDoS保護
   - レイヤー7 DDoS保護
   - 自動緩和

3. **WAF**
   - SQLインジェクション保護
   - XSS保護
   - CSRF保護

4. **SSL/TLS**
   - 無料SSL証明書
   - TLS 1.3サポート
   - 自動証明書更新

5. **DNS**
   - 高速DNS解決
   - DNSSECサポート
   - グローバルDNS

### 非機能要件

- **可用性**: 99.99%以上（SLA）
- **パフォーマンス**:
  - DNS解決: < 10ms
  - コンテンツ配信: < 50ms
  - SSL/TLSハンドシェイク: < 100ms
- **スケーラビリティ**: 自動スケーリング
- **セキュリティ**: 強固なセキュリティとコンプライアンス

### 優先順位付け

1. **P0（必須）**: CDN、DDoS保護、WAF、SSL/TLS
2. **P1（重要）**: DNS、ボット管理、レート制限
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
│         Edge Server (Closest to User)        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Cache   │  │   WAF    │  │  DDoS    │ │
│  │  Layer   │  │  Filter  │  │ Protection│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
└───────┼──────────────┼──────────────┼───────┘
        │             │             │
        │ Cache Miss  │ Blocked     │ Allowed
        │             │             │
┌───────▼─────────────▼─────────────▼───────┐
│         Origin Server                      │
│         (Customer's Server)                │
└───────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Edge Server**: ユーザーに最も近いエッジサーバー
2. **Cache Layer**: コンテンツのキャッシング
3. **WAF Filter**: Webアプリケーションファイアウォール
4. **DDoS Protection**: DDoS攻撃の保護
5. **Origin Server**: 顧客のオリジンサーバー

### データフロー

#### コンテンツ配信のフロー

```
1. Client → Edge Server (Closest to User)
2. Edge Server:
   a. Cache Layerでコンテンツを確認
   b. キャッシュがあれば返す
   c. キャッシュがなければOrigin Serverから取得
   d. コンテンツをキャッシュして返す
```

## 4. データモデル設計

### 主要なエンティティ

#### Domains テーブル

```sql
CREATE TABLE domains (
    domain_id BIGINT PRIMARY KEY,
    account_id BIGINT NOT NULL,
    domain_name VARCHAR(255) NOT NULL,
    status ENUM('active', 'pending', 'paused') DEFAULT 'pending',
    ssl_enabled BOOLEAN DEFAULT TRUE,
    waf_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_id (account_id),
    INDEX idx_domain_name (domain_name)
) ENGINE=InnoDB;
```

#### Cache_Rules テーブル

```sql
CREATE TABLE cache_rules (
    rule_id BIGINT PRIMARY KEY,
    domain_id BIGINT NOT NULL,
    path_pattern VARCHAR(500) NOT NULL,
    cache_ttl INT NOT NULL,
    cache_level ENUM('bypass', 'standard', 'aggressive') DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(domain_id),
    INDEX idx_domain_id (domain_id)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ドメイン設定、キャッシュルールの永続化

### スキーマ設計の考慮事項

1. **パーティショニング**: `domains`テーブルは`account_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: アクセスログは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### キャッシュパージ

```
POST /api/v1/zones/{zone_id}/purge_cache
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "files": ["https://example.com/image.jpg"]
}

Response (200 OK):
{
  "id": "purge_1234567890",
  "status": "success"
}
```

### 認証・認可

- **認証**: API Token、OAuth 2.0
- **認可**: API Tokenベースのアクセス制御
- **レート制限**: 
  - API呼び出し: 1,200回/分
  - キャッシュパージ: 30回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### エッジサーバー

- **地理的分散**: 世界中に約300のエッジサーバーを配置
- **自動スケーリング**: トラフィックに応じて自動スケール
- **ロードバランシング**: Anycast DNSで最適なエッジサーバーにルーティング

#### データベースシャーディング

**シャーディング戦略**: Account IDベースのシャーディング

```
Shard 1: account_id % 8 == 0
Shard 2: account_id % 8 == 1
...
Shard 8: account_id % 8 == 7
```

**シャーディングキー**: `account_id`
- ドメイン設定は`account_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisで水平スケーリング

### 負荷分散

- **Anycast DNS**: 最適なエッジサーバーにルーティング
- **地理的分散**: 複数のリージョンにデプロイ

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（エッジサーバー内）**: 
   - 用途: 頻繁にアクセスされるコンテンツ
   - TTL: 1時間-24時間

2. **L2 Cache（共有キャッシュ）**:
   - 用途: 複数のエッジサーバー間で共有
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **オリジンサーバーへのアクセス**: オリジンサーバーが遠い場合
2. **SSL/TLSハンドシェイク**: 初回接続時のハンドシェイク
3. **DNS解決**: DNSクエリの解決時間

### CDNの活用

- **エッジキャッシング**: ユーザーに近いエッジサーバーでキャッシング
- **地理的分散**: 世界中にエッジサーバーを配置

### SSL/TLS最適化

1. **TLS 1.3**: 最新のTLSプロトコルを使用
2. **OCSP Stapling**: OCSP応答をキャッシュ
3. **Session Resumption**: セッション再開をサポート

### DNS最適化

1. **Anycast DNS**: 最適なDNSサーバーにルーティング
2. **DNSキャッシング**: DNS応答をキャッシュ
3. **DNSSEC**: DNSセキュリティ拡張

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **アクティブドメイン数**: 2,000万ドメイン
- **1日のリクエスト数**: 1兆リクエスト

#### サーバーコスト

**エッジサーバー**:
- サーバー数: 約300（世界中）
- 1サーバーあたりのコスト: 約$10,000/月
- 合計: 約 **$3,000,000/月**

**データベース**:
- PostgreSQL: 約50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.01/GB × 10,000,000 GB = **$100,000/月**

**合計**: 約 **$3,127,740/月**（約37,532,880ドル/年）

### コスト削減戦略

1. **効率的なキャッシング**: キャッシュヒット率を向上
2. **データ圧縮**: データ転送量を削減
3. **エッジサーバーの最適化**: リソース使用率を向上

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のエッジサーバーにデプロイ
   - データベースのマルチAZ配置

2. **ヘルスチェック**:
   - エッジサーバーのヘルスチェック
   - オリジンサーバーのヘルスチェック

3. **自動フェイルオーバー**:
   - エッジサーバー障害時の自動フェイルオーバー
   - オリジンサーバー障害時のフォールバック

### 冗長化戦略

#### エッジサーバー冗長化

- **地理的分散**: 世界中にエッジサーバーを配置
- **自動フェイルオーバー**: エッジサーバー障害時の自動フェイルオーバー

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
   - API Token
   - OAuth 2.0

2. **認可**:
   - API Tokenベースのアクセス制御
   - リソースベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたストレージ

### DDoS対策

1. **レイヤー3/4保護**: ネットワーク層のDDoS保護
2. **レイヤー7保護**: アプリケーション層のDDoS保護
3. **自動緩和**: DDoS攻撃の自動検出と緩和

### WAF

1. **SQLインジェクション保護**: SQLインジェクション攻撃のブロック
2. **XSS保護**: クロスサイトスクリプティング攻撃のブロック
3. **CSRF保護**: クロスサイトリクエストフォージェリ攻撃のブロック

## 11. UX最適化

### パフォーマンス指標

#### Web Vitals

- **TTFB（Time to First Byte）**: < 50ms
- **FCP（First Contentful Paint）**: < 1秒
- **LCP（Largest Contentful Paint）**: < 2秒
- **DNS解決**: < 10ms

### プログレッシブローディング

1. **画像最適化**: 画像の自動最適化
2. **遅延読み込み**: 画像の遅延読み込み

## 12. 実装例

### エッジサーバー（疑似コード）

```python
class EdgeServer:
    def __init__(self, cache, waf_filter, ddos_protection, origin_client):
        self.cache = cache
        self.waf_filter = waf_filter
        self.ddos_protection = ddos_protection
        self.origin_client = origin_client
    
    async def handle_request(self, request):
        # DDoS保護
        if await self.ddos_protection.is_attack(request):
            return Response(status_code=429, body="Rate limited")
        
        # WAFフィルタ
        if await self.waf_filter.is_blocked(request):
            return Response(status_code=403, body="Blocked by WAF")
        
        # キャッシュを確認
        cache_key = self.get_cache_key(request)
        cached_response = await self.cache.get(cache_key)
        
        if cached_response:
            return cached_response
        
        # オリジンサーバーから取得
        origin_response = await self.origin_client.fetch(request)
        
        # キャッシュ可能な場合はキャッシュ
        if self.is_cacheable(origin_response):
            await self.cache.set(cache_key, origin_response, ttl=3600)
        
        return origin_response
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のリクエスト数**: 1兆リクエスト
- **1時間あたり**: 1兆 / 24 = 約416億リクエスト
- **1秒あたり**: 416億 / 3600 = 約1,156万リクエスト/秒
- **ピーク時（2倍）**: 約2,312万リクエスト/秒

### キャッシュヒット率

- **キャッシュヒット率**: 約90%
- **オリジンサーバーへのリクエスト**: 1兆 × 10% = 1,000億リクエスト/日

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **エッジキャッシング**: ユーザーに近いエッジサーバーでキャッシング
2. **DDoS保護**: 多層防御でDDoS攻撃から保護
3. **WAF**: Webアプリケーションの保護
4. **モニタリング**: 包括的なモニタリングとアラート
5. **セキュリティ**: 強固なセキュリティとコンプライアンス

### よくある落とし穴

1. **キャッシュの無効化**:
   - 問題: キャッシュが適切に無効化されない
   - 解決策: キャッシュキーの適切な設計と無効化戦略

2. **オリジンサーバーの負荷**:
   - 問題: オリジンサーバーへの負荷が高い
   - 解決策: キャッシュヒット率の向上とレート制限

## 15. 関連システム

### 類似システムへのリンク

- [Akamai](akamai_design.md) - CDNプラットフォーム
- [AWS CloudFront](aws_cloudfront_design.md) - CDNプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Akamai](akamai_design.md)でCDNプラットフォームの設計を学ぶ

