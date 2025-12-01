# Idempotency パターン

## 1. 概要

Idempotency（べき等性）は、同じ操作を複数回実行しても結果が同じになる性質です。

## 2. Idempotencyの重要性

### 2.1 ネットワークエラー

**説明**: ネットワークエラーによる重複リクエストを処理します。

**問題**:
- リクエストが重複して送信される
- 同じ操作が複数回実行される

**解決策**:
- べき等性を保証
- 重複リクエストを検出

### 2.2 リトライ

**説明**: リトライによる重複リクエストを処理します。

**問題**:
- リトライで同じ操作が複数回実行される
- 副作用が重複する

**解決策**:
- べき等性を保証
- リトライキーを使用

## 3. Idempotencyの実装

### 3.1 Idempotency Key

**説明**: リクエストに一意のキーを付与します。

**実装**:
```python
import uuid
import hashlib
from datetime import datetime, timedelta

class IdempotencyService:
    def __init__(self, cache):
        self.cache = cache
    
    async def execute_with_idempotency(self, idempotency_key: str,
                                       func: Callable, *args, **kwargs):
        """べき等性を保証して実行"""
        # 既存の結果を確認
        cached_result = await self.cache.get(
            f"idempotency:{idempotency_key}"
        )
        
        if cached_result:
            return cached_result
        
        # 実行中フラグを設定
        await self.cache.setex(
            f"idempotency:{idempotency_key}:processing",
            60,  # タイムアウト: 60秒
            "1"
        )
        
        try:
            # 操作を実行
            result = await func(*args, **kwargs)
            
            # 結果をキャッシュ
            await self.cache.setex(
                f"idempotency:{idempotency_key}",
                3600,  # TTL: 1時間
                json.dumps(result)
            )
            
            return result
        finally:
            # 実行中フラグを削除
            await self.cache.delete(
                f"idempotency:{idempotency_key}:processing"
            )
```

### 3.2 データベースベースの実装

```python
class IdempotencyStore:
    def __init__(self, db):
        self.db = db
    
    async def execute_with_idempotency(self, idempotency_key: str,
                                      func: Callable, *args, **kwargs):
        """べき等性を保証して実行"""
        # 既存の結果を確認
        existing = await self.db.get_idempotency_record(idempotency_key)
        
        if existing:
            if existing["status"] == "completed":
                return json.loads(existing["result"])
            elif existing["status"] == "processing":
                # 処理中の場合は待機またはエラー
                raise IdempotencyProcessingError()
        
        # レコードを作成
        await self.db.insert_idempotency_record(
            idempotency_key=idempotency_key,
            status="processing"
        )
        
        try:
            # 操作を実行
            result = await func(*args, **kwargs)
            
            # 結果を保存
            await self.db.update_idempotency_record(
                idempotency_key=idempotency_key,
                status="completed",
                result=json.dumps(result)
            )
            
            return result
        except Exception as e:
            # エラーを記録
            await self.db.update_idempotency_record(
                idempotency_key=idempotency_key,
                status="failed",
                error=str(e)
            )
            raise
```

## 4. ベストプラクティス

1. **一意のキー**: 一意のIdempotency Keyを生成
2. **適切なTTL**: 結果のTTLを適切に設定
3. **エラーハンドリング**: エラーを適切に処理
4. **ロック**: 同時実行を防ぐロックを実装
5. **モニタリング**: べき等性の使用状況を監視

## 5. よくある落とし穴

1. **キーの生成**: Idempotency Keyの生成が不適切
2. **TTLの設定**: TTLが適切でないと、古い結果が返される
3. **同時実行**: 同時実行による問題

## 6. 関連パターン

- [Retry Pattern](retry_pattern.md) - リトライパターン
- [Message Queues](message_queues.md) - メッセージキュー

---

**次のステップ**: [Data Replication](data_replication.md)でデータレプリケーションパターンを学ぶ

