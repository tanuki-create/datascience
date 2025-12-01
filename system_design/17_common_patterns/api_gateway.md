# API Gateway パターン

## 1. 概要

API Gatewayは、クライアントとバックエンドサービス間の統一エントリーポイントです。ルーティング、認証、レート制限、ログ記録などの機能を提供します。

## 2. API Gatewayの機能

### 2.1 ルーティング

**説明**: リクエストを適切なバックエンドサービスにルーティングします。

**機能**:
- パスベースルーティング
- ホストベースルーティング
- ロードバランシング

### 2.2 認証・認可

**説明**: リクエストの認証・認可を行います。

**機能**:
- OAuth 2.0 / JWT認証
- API Key認証
- ロールベースアクセス制御（RBAC）

### 2.3 レート制限

**説明**: APIの使用量を制限します。

**機能**:
- IPアドレスベースのレート制限
- ユーザーベースのレート制限
- API Keyベースのレート制限

### 2.4 ログ記録・モニタリング

**説明**: リクエストをログに記録し、モニタリングします。

**機能**:
- アクセスログ
- エラーログ
- メトリクス収集

### 2.5 リクエスト・レスポンス変換

**説明**: リクエスト・レスポンスを変換します。

**機能**:
- リクエストの変換
- レスポンスの変換
- プロトコル変換

## 3. API Gatewayの実装

### 3.1 NGINX使用例

```nginx
upstream api_backend {
    least_conn;
    server api1.example.com:8080;
    server api2.example.com:8080;
    server api3.example.com:8080;
}

server {
    listen 80;
    server_name api.example.com;
    
    # レート制限
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    
    location /api/v1/users {
        limit_req zone=api_limit burst=20 nodelay;
        
        # 認証
        auth_request /auth;
        
        # プロキシ
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location = /auth {
        internal;
        proxy_pass http://auth_service:8080/validate;
    }
}
```

### 3.2 Kong使用例

```lua
-- Kong API Gateway設定例
-- プラグイン: rate-limiting, authentication, logging
```

### 3.3 AWS API Gateway使用例

```yaml
# API Gateway設定例（Serverless Framework）
service: my-api

provider:
  name: aws
  runtime: python3.9

functions:
  users:
    handler: handler.users
    events:
      - http:
          path: /api/v1/users
          method: get
          authorizer: aws_iam
          throttling:
            burstLimit: 20
            rateLimit: 10
```

## 4. ベストプラクティス

1. **単一責任**: API Gatewayはルーティングと共通機能に集中
2. **認証の一元化**: 認証をAPI Gatewayで一元化
3. **レート制限**: 適切なレート制限を設定
4. **モニタリング**: 包括的なモニタリングを実装
5. **キャッシング**: 適切なキャッシングを実装

## 5. よくある落とし穴

1. **単一障害点**: API Gatewayが単一障害点になる
2. **レイテンシ**: API Gatewayがレイテンシを増加させる
3. **スケーラビリティ**: API Gatewayのスケーラビリティ

## 6. 関連パターン

- [Load Balancing](load_balancing.md) - 負荷分散
- [Rate Limiting](rate_limiting.md) - レート制限
- [Circuit Breaker](circuit_breaker.md) - サーキットブレーカー

---

**次のステップ**: [Service Mesh](service_mesh.md)でサービスメッシュパターンを学ぶ

