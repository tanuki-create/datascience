# Retry Pattern パターン

## 1. 概要

Retry Pattern（リトライパターン）は、一時的な障害に対してリクエストを再試行するパターンです。

## 2. Retry Patternの戦略

### 2.1 Fixed Interval（固定間隔）

**説明**: 固定間隔でリトライします。

**特徴**:
- 実装が簡単
- 予測可能
- リソースの無駄

**使用例**:
- シンプルなリトライ
- 低頻度のリトライ

### 2.2 Exponential Backoff（指数バックオフ）

**説明**: リトライ間隔を指数関数的に増やします。

**特徴**:
- リソースの効率的な使用
- サーバーへの負荷を軽減
- 実装が複雑

**使用例**:
- 高頻度のリトライ
- サーバーへの負荷を軽減したい場合

### 2.3 Jitter（ジッター）

**説明**: リトライ間隔にランダムな要素を追加します。

**特徴**:
- スラッシングの防止
- より自然なリトライ
- 実装が複雑

**使用例**:
- 複数のクライアントが同時にリトライする場合
- スラッシングを防ぎたい場合

## 3. Retry Patternの実装

### 3.1 Exponential Backoff実装例

```python
import time
import random
from typing import Callable, Optional

class RetryPolicy:
    def __init__(self, max_retries: int = 3,
                 initial_delay: float = 1.0,
                 max_delay: float = 60.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
    
    def retry(self, func: Callable, *args, **kwargs):
        """リトライを実行"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    time.sleep(delay)
                else:
                    raise last_exception
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """リトライ間隔を計算"""
        delay = self.initial_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            # ジッターを追加（0-25%）
            jitter_amount = delay * 0.25 * random.random()
            delay += jitter_amount
        
        return delay
```

### 3.2 条件付きリトライ

```python
class ConditionalRetry:
    def __init__(self, retry_policy: RetryPolicy):
        self.retry_policy = retry_policy
    
    def retry(self, func: Callable, *args, **kwargs):
        """条件付きリトライを実行"""
        last_exception = None
        
        for attempt in range(self.retry_policy.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                # リトライ可能かチェック
                if not self._should_retry(e, attempt):
                    raise e
                
                if attempt < self.retry_policy.max_retries:
                    delay = self.retry_policy._calculate_delay(attempt)
                    time.sleep(delay)
                else:
                    raise last_exception
        
        raise last_exception
    
    def _should_retry(self, exception: Exception, attempt: int) -> bool:
        """リトライ可能かチェック"""
        # 一時的なエラーのみリトライ
        retryable_errors = [
            ConnectionError,
            TimeoutError,
            TemporaryError
        ]
        
        return isinstance(exception, tuple(retryable_errors))
```

## 4. ベストプラクティス

1. **適切なリトライ回数**: リトライ回数を適切に設定
2. **指数バックオフ**: 指数バックオフを使用
3. **ジッター**: ジッターを追加してスラッシングを防止
4. **条件付きリトライ**: リトライ可能なエラーのみリトライ
5. **タイムアウト**: 適切なタイムアウトを設定

## 5. よくある落とし穴

1. **無限リトライ**: 無限リトライによるリソースの浪費
2. **リトライ可能なエラー**: リトライ不可能なエラーもリトライ
3. **スラッシング**: 複数のクライアントが同時にリトライ

## 6. 関連パターン

- [Circuit Breaker](circuit_breaker.md) - サーキットブレーカー
- [Bulkhead Pattern](bulkhead_pattern.md) - バルクヘッドパターン

---

**次のステップ**: [Idempotency](idempotency.md)でべき等性パターンを学ぶ

