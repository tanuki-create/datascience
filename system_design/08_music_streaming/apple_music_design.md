# Apple Music システム設計

## 1. システム概要

### 目的と主要機能

Apple Musicは、Appleが提供する音楽ストリーミングサービスです。7,500万曲以上の楽曲をストリーミング配信し、Appleデバイスと統合されています。

**主要機能**:
- 音楽ストリーミング
- プレイリスト作成・管理
- ラジオ機能（Beats 1）
- オフライン再生
- 歌詞表示
- 音楽検索
- レコメンデーション

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約8,800万人
- **日間アクティブユーザー（DAU）**: 約4,000万人
- **1日のストリーミング数**: 約10億回
- **1秒あたりのストリーミング数**: 約12,000回/秒（ピーク時）
- **楽曲ライブラリ**: 約7,500万曲

### 主要なユースケース

1. **音楽ストリーミング**: ユーザーが楽曲をストリーミング再生
2. **プレイリスト作成**: ユーザーがプレイリストを作成
3. **音楽検索**: ユーザーが楽曲を検索
4. **レコメンデーション**: ユーザーに楽曲を推薦
5. **オフライン再生**: ダウンロードした楽曲をオフラインで再生

## 2. 機能要件

### コア機能

1. **音楽ストリーミング**
   - 高品質オーディオストリーミング
   - 適応的ビットレート
   - 低レイテンシ再生

2. **プレイリスト管理**
   - プレイリストの作成・編集
   - プレイリストの共有
   - 自動プレイリスト生成

3. **検索機能**
   - 楽曲検索
   - アーティスト検索
   - アルバム検索

4. **レコメンデーション**
   - パーソナライズされたレコメンデーション
   - 機械学習ベースの推薦

5. **オフライン再生**
   - 楽曲のダウンロード
   - オフライン再生

### 非機能要件

- **可用性**: 99.9%以上（年間ダウンタイム < 8.76時間）
- **一貫性**: プレイリストは強い一貫性、ストリーミングは最終的に一貫性を保つ
- **パフォーマンス**:
  - ストリーミング開始: < 2秒
  - 音楽検索: < 1秒
  - レコメンデーション生成: < 3秒
- **スケーラビリティ**: 水平スケーリング可能
- **耐久性**: 楽曲は永続的に保存

### 優先順位付け

1. **P0（必須）**: 音楽ストリーミング、検索、プレイリスト管理
2. **P1（重要）**: レコメンデーション、オフライン再生
3. **P2（望ましい）**: ラジオ機能、高度なレコメンデーション

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐
│   Client    │ (iOS, macOS, Web)
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
│  │ Streaming│  │  Search  │  │ Playlist│        │
│  │ Service  │  │ Service  │  │ Service │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │                │
│  ┌────▼─────────────▼─────────────▼─────┐         │
│  │      Recommendation Service          │         │
│  │      Radio Service                   │         │
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
│         Object Storage (S3)                       │
│         Search Index (Elasticsearch)              │
│         CDN (CloudFront/Cloudflare)               │
│         Media Server (HLS/DASH)                   │
└──────────────────────────────────────────────────┘
```

### コンポーネントの説明

1. **Load Balancer**: トラフィックを複数のAPI Gatewayに分散
2. **API Gateway**: リクエストのルーティングと認証
3. **Application Servers**:
   - **Streaming Service**: 音楽ストリーミングの処理
   - **Search Service**: 音楽検索の処理
   - **Playlist Service**: プレイリスト管理の処理
   - **Recommendation Service**: レコメンデーションの処理
   - **Radio Service**: ラジオ機能の処理
4. **Database**: 楽曲メタデータ、プレイリスト、ユーザー情報の永続化
5. **Cache**: 頻繁にアクセスされるデータのキャッシング
6. **Message Queue**: 非同期処理（レコメンデーション生成など）
7. **Object Storage**: 楽曲ファイルの保存
8. **Search Index**: 音楽検索インデックス
9. **CDN**: 楽曲の配信
10. **Media Server**: HLS/DASHストリーミングサーバー

### データフロー

#### 音楽ストリーミングのフロー

```
1. Client → Load Balancer → API Gateway
2. API Gateway → Streaming Service
3. Streaming Service:
   a. 楽曲メタデータを取得
   b. CDNから楽曲をストリーミング
   c. 適応的ビットレートで配信
   d. 再生履歴を記録
```

## 4. データモデル設計

### 主要なエンティティ

#### Songs テーブル

```sql
CREATE TABLE songs (
    song_id BIGINT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    artist_id BIGINT NOT NULL,
    album_id BIGINT,
    duration INT NOT NULL,
    genre VARCHAR(100),
    release_date DATE,
    storage_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    INDEX idx_artist_id (artist_id),
    INDEX idx_album_id (album_id),
    FULLTEXT INDEX idx_title (title)
) ENGINE=InnoDB;
```

#### Playlists テーブル

```sql
CREATE TABLE playlists (
    playlist_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    playlist_name VARCHAR(200) NOT NULL,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
```

#### Playlist_Songs テーブル

```sql
CREATE TABLE playlist_songs (
    playlist_id BIGINT NOT NULL,
    song_id BIGINT NOT NULL,
    position INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id),
    INDEX idx_playlist_position (playlist_id, position)
) ENGINE=InnoDB;
```

### データベース選択の理由

- **RDBMS（MySQL/PostgreSQL）**: 
  - 理由: ACID特性が必要、複雑なクエリ（JOIN、集計）、トランザクション処理
  - 用途: 楽曲メタデータ、プレイリスト、ユーザー情報の永続化
- **Object Storage（S3）**:
  - 理由: 大規模ファイルストレージ、水平スケーリング
  - 用途: 楽曲ファイルの保存
- **Elasticsearch**:
  - 理由: 全文検索、音楽検索
  - 用途: 検索インデックス

### スキーマ設計の考慮事項

1. **パーティショニング**: `songs`テーブルは`artist_id`でシャーディング
2. **インデックス**: 頻繁にクエリされるカラムにインデックス
3. **時系列データ**: 再生履歴は時系列で保存

## 5. API設計

### 主要なAPIエンドポイント

#### 音楽ストリーミング

```
GET /api/v1/songs/{song_id}/stream
Authorization: Bearer <token>
Range: bytes=0-

Response (206 Partial Content):
[Audio Data Stream]
```

#### 音楽検索

```
GET /api/v1/search?q=hello&type=song&limit=20
Authorization: Bearer <token>

Response (200 OK):
{
  "songs": [
    {
      "song_id": 1234567890,
      "title": "Hello",
      "artist": "Adele",
      "duration": 295
    }
  ],
  "total_results": 1000
}
```

#### プレイリスト作成

```
POST /api/v1/playlists
Authorization: Bearer <token>
Content-Type: application/json

Request Body:
{
  "playlist_name": "My Favorites",
  "is_public": false
}

Response (200 OK):
{
  "playlist_id": 9876543210,
  "playlist_name": "My Favorites"
}
```

### 認証・認可

- **認証**: OAuth 2.0 / JWT、Apple ID統合
- **認可**: ユーザーは自分のプレイリストのみ編集可能
- **レート制限**: 
  - ストリーミング: 無制限
  - 検索: 100リクエスト/分

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### アプリケーションサーバー

- **ステートレス設計**: セッション情報をRedisに保存
- **ロードバランサー**: ラウンドロビンまたはLeast Connections
- **オートスケーリング**: CPU使用率に基づいて自動スケール

#### データベースシャーディング

**シャーディング戦略**: Artist IDベースのシャーディング

```
Shard 1: artist_id % 8 == 0
Shard 2: artist_id % 8 == 1
...
Shard 8: artist_id % 8 == 7
```

**シャーディングキー**: `artist_id`
- 楽曲は`artist_id`でシャーディング

### 垂直スケーリング戦略

- **データベース**: 読み取りレプリカを追加
- **キャッシュ**: Redisクラスターで水平スケーリング
- **検索**: Elasticsearchクラスターで水平スケーリング

### 負荷分散

- **Load Balancer**: NGINXまたはAWS ELB
- **地理的分散**: 複数のリージョンにデプロイ
- **CDN**: 楽曲をCDNで配信

### キャッシング戦略

#### キャッシュレイヤー

1. **L1 Cache（アプリケーション内）**: 
   - 用途: 頻繁にアクセスされる小さなデータ
   - TTL: 1-5分

2. **L2 Cache（Redis）**:
   - 用途: 楽曲メタデータ、プレイリスト、人気楽曲
   - TTL: 5-15分

3. **L3 Cache（CDN）**:
   - 用途: 楽曲ファイル
   - TTL: 24時間-7日

## 7. レイテンシ最適化

### ボトルネックの特定

1. **ストリーミング開始**: 楽曲ファイルの読み込み
2. **検索**: Elasticsearchクエリの最適化
3. **レコメンデーション**: 機械学習モデルの推論

### CDNの活用

- **楽曲**: CloudflareまたはAWS CloudFront
- **地理的分散**: ユーザーに近いCDNエッジから配信

### ストリーミング最適化

1. **適応的ビットレート**: ネットワーク状況に応じてビットレートを調整
2. **プリフェッチ**: 次の楽曲を事前に読み込み
3. **バッファリング**: 楽曲をバッファリングしてスムーズな再生

### 非同期処理

#### メッセージキュー（Kafka）

1. **再生履歴記録**:
   ```
   Topic: play-history
   Partition Key: user_id
   ```

2. **レコメンデーション生成**:
   ```
   Topic: recommendation-generation
   Partition Key: user_id
   ```

## 8. コスト最適化

### インフラコストの見積もり

#### 前提条件

- **月間アクティブユーザー**: 8,800万人
- **日間アクティブユーザー**: 4,000万人
- **1日のストリーミング数**: 10億回

#### サーバーコスト（AWS）

**アプリケーションサーバー**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 1,000台（リージョン間で分散）
- コスト: $0.192/時間 × 1,000台 × 730時間 = **$140,160/月**

**データベース**:
- RDS MySQL db.r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 50台（マスター + レプリカ）
- コスト: $0.76/時間 × 50台 × 730時間 = **$27,740/月**

**キャッシュ（ElastiCache）**:
- Redis cache.r5.xlarge (26 GB RAM)
- インスタンス数: 100台
- コスト: $0.175/時間 × 100台 × 730時間 = **$12,775/月**

**検索（Elasticsearch）**:
- Elasticsearch r5.2xlarge (8 vCPU, 64 GB RAM)
- インスタンス数: 20台
- コスト: $0.76/時間 × 20台 × 730時間 = **$11,096/月**

**ストレージ（S3）**:
- 楽曲ストレージ: 100 PB
- コスト: $0.023/GB/月 × 100,000,000 GB = **$2,300,000/月**

**ネットワーク**:
- データ転送: 50 PB/月
- コスト: $0.09/GB × 50,000,000 GB = **$4,500,000/月**

**合計**: 約 **$6,991,771/月**（約83,901,252ドル/年）

### コスト削減戦略

1. **リザーブドインスタンス**: 1年契約で最大72%削減
2. **Spotインスタンス**: 非クリティカルなワークロードで最大90%削減
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

2. **楽曲バックアップ**:
   - S3のマルチAZレプリケーション
   - クロスリージョンレプリケーション

## 10. セキュリティ

### 認証・認可

1. **認証**:
   - OAuth 2.0 / JWT
   - Apple ID統合

2. **認可**:
   - RBAC（Role-Based Access Control）
   - ユーザーは自分のプレイリストのみ編集可能

### データ暗号化

1. **転送中の暗号化**: TLS 1.3
2. **保存時の暗号化**: 
   - データベース: 暗号化されたEBSボリューム
   - S3: サーバーサイド暗号化

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
- **ストリーミング開始**: < 2秒
- **音楽検索**: < 1秒

### プログレッシブローディング

1. **楽曲の遅延読み込み**:
   - プレイリストの遅延読み込み
   - サムネイルを先に表示

2. **オフライン対応**:
   - オフライン時の基本機能の提供

## 12. 実装例

### ストリーミングサービス（疑似コード）

```python
class StreamingService:
    def __init__(self, db, cache, cdn, media_server):
        self.db = db
        self.cache = cache
        self.cdn = cdn
        self.media_server = media_server
    
    async def stream_song(self, song_id: int, user_id: int, range_header: str = None):
        # 楽曲メタデータを取得
        song = await self.db.get_song(song_id)
        
        if not song:
            raise NotFoundError("Song not found")
        
        # CDNから楽曲をストリーミング
        stream_url = await self.cdn.get_stream_url(
            song_id=song_id,
            quality="high"
        )
        
        # 再生履歴を記録（非同期）
        await self.record_play_history(
            user_id=user_id,
            song_id=song_id
        )
        
        # ストリーミングURLを返す
        return {
            "stream_url": stream_url,
            "song_title": song["title"],
            "artist": song["artist"],
            "duration": song["duration"]
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日のストリーミング数**: 10億回
- **1時間あたり**: 10億 / 24 = 約4,167万回
- **1秒あたり**: 4,167万 / 3600 = 約11,575回/秒
- **ピーク時（3倍）**: 約34,725回/秒

### ストレージ見積もり

#### 楽曲ストレージ

- **1楽曲あたりの平均サイズ**: 5 MB（高品質）
- **楽曲ライブラリ**: 7,500万曲
- **合計ストレージ**: 7,500万 × 5 MB = 375 TB
- **複数品質**: 375 TB × 3品質 = 1.125 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **マイクロサービス**: 機能ごとにサービスを分割
2. **イベント駆動**: 非同期処理でイベント駆動アーキテクチャ
3. **CDN活用**: 楽曲をCDN経由で配信
4. **適応的ビットレート**: ネットワーク状況に応じてビットレートを調整
5. **モニタリング**: 包括的なモニタリングとアラート

### よくある落とし穴

1. **ストリーミングのレイテンシ**:
   - 問題: ストリーミング開始が遅い
   - 解決策: CDNとプリフェッチ

2. **レコメンデーションのスケーラビリティ**:
   - 問題: 機械学習モデルの推論が遅い
   - 解決策: 事前計算とキャッシング

## 15. 関連システム

### 類似システムへのリンク

- [Spotify](spotify_design.md) - 音楽ストリーミング
- [Pandora](pandora_design.md) - 音楽ストリーミング

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略
- [CDN](../14_cdn/cloudflare_design.md) - CDN設計

---

**次のステップ**: [Pandora](pandora_design.md)でラジオスタイルの音楽ストリーミングシステムの設計を学ぶ

