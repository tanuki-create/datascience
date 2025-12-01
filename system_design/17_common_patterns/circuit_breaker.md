# Circuit Breaker パターン

## 1. 概要

Circuit Breaker（サーキットブレーカー）は、障害が発生したサービスへのリクエストを遮断し、システム全体への影響を防ぐパターンです。

## 2. Circuit Breakerの状態

### 2.1 Closed（閉）

**説明**: 正常に動作している状態です。

**動作**:
- リクエストを通常通り処理
- エラー数をカウント
- エラー率が閾値を超えたらOpen状態に遷移

### 2.2 Open（開）

**説明**: 障害が発生している状態です。

**動作**:
- リクエストを即座に拒否
- フォールバック処理を実行
- タイムアウト後にHalf-Open状態に遷移

### 2.3 Half-Open（半開）

**説明**: 障害からの回復を試みている状態です。

**動作**:
- 限定的なリクエストを処理
- 成功したらClosed状態に遷移
- 失敗したらOpen状態に戻る

## 3. Circuit Breakerの実装

### 3.1 閾値の設定

**エラー率**: 一定時間内のエラー率が閾値を超えたらOpen状態に遷移

**例**:
- エラー率: 50%
- 時間ウィンドウ: 60秒
- 最小リクエスト数: 10

### 3.2 タイムアウト

**説明**: Open状態からHalf-Open状態への遷移時間

**例**:
- タイムアウト: 30秒

### 3.3 フォールバック処理

**説明**: Open状態時に実行する代替処理

**例**:
- キャッシュされたデータを返す
- デフォルト値を返す
- エラーメッセージを返す

## 4. 実装例

### 4.1 Python実装例

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Optional

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5,
                 timeout: int = 60,
                 expected_exception: type = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return False
        
        return (datetime.now() - self.last_failure_time).seconds >= self.timeout
```

### 4.2 Redis使用例

```python
import redis
import json
from datetime import datetime, timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class CircuitBreaker:
    def __init__(self, service_name: str, failure_threshold: int = 5,
                 timeout: int = 60):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
    
    def call(self, func: Callable, *args, **kwargs):
        state = self._get_state()
        
        if state == "open":
            if self._should_attempt_reset():
                self._set_state("half_open")
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _get_state(self) -> str:
        state = redis_client.get(f"circuit_breaker:{self.service_name}:state")
        return state.decode() if state else "closed"
    
    def _set_state(self, state: str):
        redis_client.set(f"circuit_breaker:{self.service_name}:state", state)
    
    def _on_success(self):
        redis_client.delete(f"circuit_breaker:{self.service_name}:failure_count")
        if self._get_state() == "half_open":
            self._set_state("closed")
    
    def _on_failure(self):
        failure_count = redis_client.incr(
            f"circuit_breaker:{self.service_name}:failure_count"
        )
        redis_client.setex(
            f"circuit_breaker:{self.service_name}:last_failure",
            3600,
            datetime.now().isoformat()
        )
        
        if failure_count >= self.failure_threshold:
            self._set_state("open")
    
    def _should_attempt_reset(self) -> bool:
        last_failure = redis_client.get(
            f"circuit_breaker:{self.service_name}:last_failure"
        )
        if not last_failure:
            return False
        
        last_failure_time = datetime.fromisoformat(last_failure.decode())
        return (datetime.now() - last_failure_time).seconds >= self.timeout
```

## 5. ベストプラクティス

1. **適切な閾値設定**: エラー率とタイムアウトを適切に設定
2. **フォールバック処理**: 適切なフォールバック処理を実装
3. **モニタリング**: Circuit Breakerの状態を監視
4. **ログ記録**: 状態遷移をログに記録
5. **段階的な回復**: Half-Open状態で段階的に回復を試みる

## 6. よくある落とし穴

1. **閾値の設定**: 閾値が適切でないと、正常なサービスも遮断される
2. **フォールバック処理**: フォールバック処理が不適切だと、ユーザー体験が低下
3. **状態の共有**: 複数のインスタンス間で状態を共有する必要がある

## 7. 関連パターン

- [Retry Pattern](retry_pattern.md) - リトライパターン
- [Bulkhead Pattern](bulkhead_pattern.md) - バルクヘッドパターン

---

**次のステップ**: [API Gateway](api_gateway.md)でAPIゲートウェイパターンを学ぶ

