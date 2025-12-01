# Akamai システム設計

## 1. システム概要

### 目的と主要機能

Akamaiは、エンタープライズ向けのCDN（Content Delivery Network）プラットフォームです。大規模なWebサイトやアプリケーション向けにコンテンツ配信とセキュリティサービスを提供します。

**主要機能**:
- CDN（コンテンツ配信）
- DDoS保護
- WAF（Web Application Firewall）
- 動画配信
- ライブストリーミング
- モバイル最適化
- エッジコンピューティング

### ユーザースケール

- **アクティブドメイン数**: 約500万ドメイン
- **1日のリクエスト数**: 約3兆リクエスト
- **1秒あたりのリクエスト数**: 約3,500万リクエスト/秒（ピーク時）
- **エッジサーバー数**: 約400,000（世界中）

### 主要なユースケース

1. **コンテンツ配信**: ユーザーにコンテンツを高速配信
2. **動画配信**: 動画コンテンツの配信
3. **ライブストリーミング**: ライブイベントのストリーミング
4. **DDoS保護**: DDoS攻撃から保護
5. **エッジコンピューティング**: エッジでのコンピューティング

## 2. 機能要件

### コア機能

1. **CDN**
   - 静的コンテンツのキャッシング
   - 動的コンテンツの最適化
   - 画像最適化

2. **動画配信**
   - 動画のストリーミング
   - アダプティブビットレート
   - DRM保護

3. **ライブストリーミング**
   - ライブイベントのストリーミング
   - 低レイテンシストリーミング
   - マルチビットレート

4. **DDoS保護**
   - レイヤー3/4 DDoS保護
   - レイヤー7 DDoS保護
   - 自動緩和

5. **エッジコンピューティング**
   - エッジでのJavaScript実行
   - エッジでのAPI処理
   - エッジでのデータ処理

### 非機能要件

- **可用性**: 99.99%以上（SLA）
- **パフォーマンス**:
  - コンテンツ配信: < 50ms
  - 動画配信: < 100ms
  - ライブストリーミング: < 5秒
- **スケーラビリティ**: 自動スケーリング
- **セキュリティ**: 強固なセキュリティとコンプライアンス

### 優先順位付け

1. **P0（必須）**: CDN、動画配信、DDoS保護、WAF
2. **P1（重要）**: ライブストリーミング、エッジコンピューティング、モバイル最適化
3. **P2（望ましい）**: 高度な分析機能、カスタムルール

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (Web Browser, Mobile Apps, Video Players)
└──────┬──────┘
       │ HTTPS
       │
┌──────▼─────────────────────────────────────┐
│         Edge Server (Closest to User)        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Cache   │  │   WAF    │  │  DDoS    │ │
│  │  Layer   │  │  Filter  │  │ Protection│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │             │             │         │
│  ┌────▼─────────────▼─────────────▼─────┐  │
│  │      Edge Computing                  │  │
│  │      (JavaScript Execution)         │  │
│  └────┬──────────────────────────────────┘  │
└───────┼─────────────────────────────────────┘
        │
        │ Cache Miss / Origin Request
        │
┌───────▼─────────────────────────────────────┐
│         Origin Server                        │
│         (Customer's Server)                  │
└─────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Edge Server**: ユーザーに最も近いエッジサーバー
2. **Cache Layer**: コンテンツのキャッシング
3. **WAF Filter**: Webアプリケーションファイアウォール
4. **DDoS Protection**: DDoS攻撃の保護
5. **Edge Computing**: エッジでのコンピューティング
6. **Origin Server**: 顧客のオリジンサーバー

### データフロー

#### 動画配信のフロー

```
1. Client → Edge Server (Closest to User)
2. Edge Server:
   a. Cache Layerで動画を確認
   b. キャッシュがあればストリーミング開始
   c. キャッシュがなければOrigin Serverから取得
   d. 動画をキャッシュしてストリーミング
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
    video_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_id (account_id),
    INDEX idx_domain_name (domain_name)
) ENGINE=InnoDB;
```

#### Video_Assets テーブル

```sql
CREATE TABLE video_assets (
    asset_id BIGINT PRIMARY KEY,
    domain_id BIGINT NOT NULL,
    asset_name VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    duration INT,
    bitrate INT,
    status ENUM('processing', 'ready', 'failed') DEFAULT 'processing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(domain_id),
    INDEX idx_domain_id (domain_id),
    INDEX idx_status (status)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: ドメイン設定、動画アセットの永続化

### スキーマ設計の考慮事項

1. **パーティショニング**: `domains`テーブルは`account_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: アクセスログは時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 動画アップロード

```
POST /api/v1/videos
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "file": <video_file>,
  "domain_id": 1234567890
}

Response (200 OK):
{
  "asset_id": "asset_1234567890",
  "status": "processing",
  "estimated_time": 300
}
```

### 認証・認可

- **認証**: API Token、OAuth 2.0
- **認可**: API Tokenベースのアクセス制御
- **レート制限**: 
  - API呼び出し: 1,000回/分
  - 動画アップロード: 10回/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### エッジサーバー

- **地理的分散**: 世界中に約400,000のエッジサーバーを配置
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
2. **動画エンコーディング**: 動画のエンコーディング時間
3. **ライブストリーミング**: ライブストリーミングのレイテンシ

### CDNの活用

- **エッジキャッシング**: ユーザーに近いエッジサーバーでキャッシング
- **地理的分散**: 世界中にエッジサーバーを配置

### 動画配信最適化

1. **アダプティブビットレート**: ネットワーク状況に応じてビットレートを調整
2. **事前エンコーディング**: 動画を事前にエンコーディング
3. **チャンク配信**: 動画をチャンクに分割して配信

### ライブストリーミング最適化

1. **低レイテンシプロトコル**: WebRTC、LL-HLSを使用
2. **エッジでの処理**: エッジサーバーでストリーミング処理
3. **マルチビットレート**: 複数のビットレートを同時配信

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **アクティブドメイン数**: 500万ドメイン
- **1日のリクエスト数**: 3兆リクエスト

#### サーバーコスト

**エッジサーバー**:
- サーバー数: 約400,000（世界中）
- 1サーバーあたりのコスト: 約$5,000/月
- 合計: 約 **$2,000,000,000/月**

**データベース**:
- PostgreSQL: 約100台（マスター + レプリカ）
- コスト: $0.76/時間 × 100台 × 730時間 = **$55,480/月**

**ネットワーク**:
- データ転送: 50 PB/月
- コスト: $0.01/GB × 50,000,000 GB = **$500,000/月**

**合計**: 約 **$2,000,555,480/月**（約24,006,665,760ドル/年）

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
   - 動画: DRM保護

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
- **動画開始**: < 100ms

### プログレッシブローディング

1. **動画の遅延読み込み**: 動画の遅延読み込み
2. **アダプティブビットレート**: ネットワーク状況に応じてビットレートを調整

## 12. 実装例

### エッジサーバー（疑似コード）

```python
class EdgeServer:
    def __init__(self, cache, waf_filter, ddos_protection, video_service, origin_client):
        self.cache = cache
        self.waf_filter = waf_filter
        self.ddos_protection = ddos_protection
        self.video_service = video_service
        self.origin_client = origin_client
    
    async def handle_request(self, request):
        # DDoS保護
        if await self.ddos_protection.is_attack(request):
            return Response(status_code=429, body="Rate limited")
        
        # WAFフィルタ
        if await self.waf_filter.is_blocked(request):
            return Response(status_code=403, body="Blocked by WAF")
        
        # 動画リクエストの場合
        if self.is_video_request(request):
            return await self.video_service.stream_video(request)
        
        # 通常のコンテンツリクエスト
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

- **1日のリクエスト数**: 3兆リクエスト
- **1時間あたり**: 3兆 / 24 = 約1,250億リクエスト
- **1秒あたり**: 1,250億 / 3600 = 約3,472万リクエスト/秒
- **ピーク時（2倍）**: 約6,944万リクエスト/秒

### キャッシュヒット率

- **キャッシュヒット率**: 約95%
- **オリジンサーバーへのリクエスト**: 3兆 × 5% = 1,500億リクエスト/日

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **エッジキャッシング**: ユーザーに近いエッジサーバーでキャッシング
2. **動画最適化**: アダプティブビットレートと事前エンコーディング
3. **DDoS保護**: 多層防御でDDoS攻撃から保護
4. **モニタリング**: 包括的なモニタリングとアラート
5. **セキュリティ**: 強固なセキュリティとコンプライアンス

### よくある落とし穴

1. **動画エンコーディングのレイテンシ**:
   - 問題: 動画のエンコーディングが遅い
   - 解決策: 事前エンコーディングと並列処理

2. **ライブストリーミングのレイテンシ**:
   - 問題: ライブストリーミングのレイテンシが高い
   - 解決策: 低レイテンシプロトコルとエッジでの処理

## 15. 関連システム

### 類似システムへのリンク

- [Cloudflare](cloudflare_design.md) - CDNプラットフォーム
- [AWS CloudFront](aws_cloudfront_design.md) - CDNプラットフォーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [AWS CloudFront](aws_cloudfront_design.md)でCDNプラットフォームの設計を学ぶ

