# Rate Limiting パターン

## 1. 概要

レート制限は、APIやサービスの使用量を制限する技術です。DoS攻撃の防止、リソースの保護、公平な使用を実現します。

## 2. レート制限アルゴリズム

### 2.1 Fixed Window

**説明**: 固定時間ウィンドウ内でのリクエスト数を制限します。

**特徴**:
- 実装が簡単
- ウィンドウの境界でバーストが発生する可能性

**使用例**:
- シンプルなレート制限
- バーストが許容できる場合

### 2.2 Sliding Window

**説明**: スライディングウィンドウ内でのリクエスト数を制限します。

**特徴**:
- より正確な制限
- バーストが少ない

**使用例**:
- 正確なレート制限が必要な場合
- バーストを避けたい場合

### 2.3 Token Bucket

**説明**: トークンバケットアルゴリズムを使用します。

**特徴**:
- バーストを許可
- 平均レートを制御

**使用例**:
- バーストが必要な場合
- 平均レートを制御したい場合

### 2.4 Leaky Bucket

**説明**: リーキーバケットアルゴリズムを使用します。

**特徴**:
- 一定のレートで処理
- バーストを平滑化

**使用例**:
- 一定のレートが必要な場合
- バーストを平滑化したい場合

## 3. レート制限の実装

### 3.1 Redis使用例

```python
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def rate_limit(user_id: int, limit: int, window: int) -> bool:
    """レート制限をチェック"""
    key = f"rate_limit:{user_id}"
    current = redis_client.incr(key)
    
    if current == 1:
        redis_client.expire(key, window)
    
    return current <= limit
```

### 3.2 NGINX設定例

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

## 4. レート制限のレベル

### 4.1 IPアドレスベース

**説明**: IPアドレスに基づいてレート制限を実施します。

**メリット**:
- 実装が簡単
- 匿名ユーザーにも適用可能

**デメリット**:
- NAT環境で問題が発生
- 共有IPの問題

### 4.2 ユーザーベース

**説明**: ユーザーIDに基づいてレート制限を実施します。

**メリット**:
- 正確な制限
- ユーザーごとの制限

**デメリット**:
- 認証が必要
- 匿名ユーザーには適用不可

### 4.3 API Keyベース

**説明**: API Keyに基づいてレート制限を実施します。

**メリット**:
- 柔軟な制限
- プランごとの制限

**デメリット**:
- API Keyの管理が必要

## 5. ベストプラクティス

1. **適切な制限**: 適切なレート制限を設定
2. **エラーメッセージ**: 分かりやすいエラーメッセージを返す
3. **ヘッダー**: レート制限情報をヘッダーで返す
4. **段階的な制限**: 段階的な制限を実装
5. **ホワイトリスト**: 信頼できるIP/ユーザーをホワイトリストに追加

## 6. よくある落とし穴

1. **レート制限のバイパス**: レート制限をバイパスする方法が存在
2. **誤検知**: 正当なユーザーがブロックされる
3. **パフォーマンス**: レート制限の実装がパフォーマンスに影響

## 7. 関連パターン

- [Load Balancing](load_balancing.md) - 負荷分散
- [Caching Strategies](caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Monitoring & Logging](monitoring_logging.md)でモニタリングとログを学ぶ

