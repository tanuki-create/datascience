# Load Balancing パターン

## 1. 概要

ロードバランシングは、複数のサーバー間でトラフィックを分散させる技術です。可用性、スケーラビリティ、パフォーマンスの向上を実現します。

## 2. 主要なロードバランシングアルゴリズム

### 2.1 Round Robin

**説明**: リクエストを順番に各サーバーに割り当てます。

**メリット**:
- 実装が簡単
- 均等な負荷分散

**デメリット**:
- サーバーの性能差を考慮しない
- セッションの保持が困難

**使用例**:
- ステートレスなアプリケーション
- サーバーの性能が均一な場合

### 2.2 Least Connections

**説明**: 現在の接続数が最も少ないサーバーにリクエストを割り当てます。

**メリット**:
- サーバーの負荷を考慮
- 長時間接続に適している

**デメリット**:
- 接続数の追跡が必要
- 実装が複雑

**使用例**:
- 長時間接続が必要なアプリケーション
- データベース接続プール

### 2.3 Weighted Round Robin

**説明**: サーバーに重みを設定し、重みに応じてリクエストを割り当てます。

**メリット**:
- サーバーの性能差を考慮
- 柔軟な負荷分散

**デメリット**:
- 重みの設定が必要
- 動的な調整が困難

**使用例**:
- サーバーの性能が異なる場合
- 段階的なスケーリング

### 2.4 IP Hash

**説明**: クライアントのIPアドレスに基づいてサーバーを選択します。

**メリット**:
- セッションの保持が容易
- キャッシュの効率化

**デメリット**:
- IPアドレスの分散が不均一になる可能性
- サーバーの追加・削除時に問題が発生

**使用例**:
- セッションが必要なアプリケーション
- キャッシュの効率化が必要な場合

## 3. ロードバランサーの種類

### 3.1 Layer 4 (L4) Load Balancer

**説明**: TCP/UDPレベルでロードバランシングを行います。

**特徴**:
- 高速
- シンプル
- アプリケーション層の情報を参照しない

**使用例**:
- 高スループットが必要な場合
- シンプルな負荷分散

### 3.2 Layer 7 (L7) Load Balancer

**説明**: HTTP/HTTPSレベルでロードバランシングを行います。

**特徴**:
- アプリケーション層の情報を参照可能
- コンテンツベースのルーティング
- SSL終端

**使用例**:
- コンテンツベースのルーティングが必要な場合
- SSL終端が必要な場合

## 4. 実装例

### 4.1 NGINX設定例

```nginx
upstream backend {
    least_conn;
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 4.2 HAProxy設定例

```haproxy
global
    daemon

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http-in
    bind *:80
    default_backend servers

backend servers
    balance roundrobin
    server server1 192.168.1.10:8080 check
    server server2 192.168.1.11:8080 check
    server server3 192.168.1.12:8080 check
```

## 5. ベストプラクティス

1. **ヘルスチェック**: 定期的にサーバーのヘルスチェックを実施
2. **セッション保持**: セッションが必要な場合はSticky Sessionを使用
3. **冗長化**: ロードバランサー自体も冗長化
4. **モニタリング**: ロードバランサーのメトリクスを監視
5. **SSL終端**: SSL終端をロードバランサーで実施してバックエンドの負荷を軽減

## 6. よくある落とし穴

1. **セッションの喪失**: ステートレス設計を推奨
2. **ヘルスチェックの設定**: 適切なヘルスチェック設定が必要
3. **ロードバランサーの単一障害点**: ロードバランサーの冗長化が必要

## 7. 関連パターン

- [Caching Strategies](caching_strategies.md) - キャッシング戦略
- [Database Sharding](database_sharding.md) - データベースシャーディング

---

**次のステップ**: [Caching Strategies](caching_strategies.md)でキャッシング戦略を学ぶ

