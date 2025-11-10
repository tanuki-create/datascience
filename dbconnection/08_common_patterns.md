# 共通パターンとベストプラクティス

## 概要

このガイドは、すべてのアプリケーションタイプに適用可能なデータベース接続の共通パターンとベストプラクティスを提供します。コネクションプーリング、リトライ、トランザクション管理、データマイグレーション、監視など、実践的なパターンを網羅しています。

## コネクションプーリングパターン

### 基本的なコネクションプール

```python
# PostgreSQL用のコネクションプール
import asyncpg
from contextlib import asynccontextmanager

class ConnectionPool:
    def __init__(self):
        self.pool = None
    
    async def initialize(self, **config):
        """コネクションプールを初期化"""
        self.pool = await asyncpg.create_pool(
            host=config.get('host', 'localhost'),
            database=config.get('database'),
            user=config.get('user'),
            password=config.get('password'),
            min_size=config.get('min_size', 5),
            max_size=config.get('max_size', 20),
            max_queries=config.get('max_queries', 50000),
            max_inactive_connection_lifetime=config.get('max_inactive_lifetime', 300),
            command_timeout=config.get('command_timeout', 30)
        )
    
    @asynccontextmanager
    async def acquire(self):
        """コネクションを取得（コンテキストマネージャー）"""
        async with self.pool.acquire() as conn:
            yield conn
    
    async def execute(self, query: str, *args):
        """クエリを実行"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        """クエリを実行して結果を取得"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def close(self):
        """プールを閉じる"""
        await self.pool.close()
```

### 接続プールの監視

```python
# 接続プールの状態を監視
class PoolMonitor:
    def __init__(self, pool):
        self.pool = pool
    
    async def get_pool_stats(self):
        """プールの統計情報を取得"""
        return {
            'size': self.pool.get_size(),
            'idle_size': self.pool.get_idle_size(),
            'min_size': self.pool.get_min_size(),
            'max_size': self.pool.get_max_size(),
            'free_size': self.pool.get_max_size() - self.pool.get_size()
        }
    
    async def check_health(self):
        """プールの健全性をチェック"""
        stats = await self.get_pool_stats()
        
        # 警告条件をチェック
        warnings = []
        if stats['free_size'] < 2:
            warnings.append("Low available connections")
        if stats['idle_size'] == 0:
            warnings.append("No idle connections")
        
        return {
            'healthy': len(warnings) == 0,
            'warnings': warnings,
            'stats': stats
        }
```

### 接続プールの動的調整

```python
# 負荷に応じて接続プールサイズを動的に調整
class AdaptivePool:
    def __init__(self, pool):
        self.pool = pool
        self.adjustment_interval = 60  # 60秒ごとに調整
    
    async def adjust_pool_size(self, target_size: int):
        """プールサイズを調整"""
        current_size = self.pool.get_size()
        
        if target_size > current_size:
            # プールサイズを増やす
            await self.pool.resize(target_size)
        elif target_size < current_size:
            # プールサイズを減らす（既存接続は自然に閉じられる）
            await self.pool.resize(target_size)
    
    async def monitor_and_adjust(self):
        """監視して自動調整"""
        while True:
            stats = await self.get_pool_stats()
            active_connections = stats['size'] - stats['idle_size']
            
            # アクティブ接続数に基づいて最適サイズを計算
            optimal_size = max(
                stats['min_size'],
                min(stats['max_size'], active_connections * 2 + 5)
            )
            
            if optimal_size != stats['size']:
                await self.adjust_pool_size(optimal_size)
            
            await asyncio.sleep(self.adjustment_interval)
```

## リトライパターン

### 指数バックオフリトライ

```python
# 指数バックオフを使ったリトライパターン
import asyncio
import random
from typing import Callable, TypeVar, Optional

T = TypeVar('T')

class RetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def execute_with_retry(
        self,
        func: Callable[[], T],
        retryable_exceptions: tuple = (Exception,)
    ) -> T:
        """リトライ可能な関数を実行"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await func() if asyncio.iscoroutinefunction(func) else func()
            except retryable_exceptions as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    # 指数バックオフ + ジッター
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    await asyncio.sleep(delay)
                else:
                    raise
        
        raise last_exception

# 使用例
async def database_query_with_retry(pool, query: str, *args):
    """リトライ付きデータベースクエリ"""
    retry_handler = RetryHandler(max_retries=3, base_delay=1.0)
    
    async def execute_query():
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    return await retry_handler.execute_with_retry(
        execute_query,
        retryable_exceptions=(asyncpg.PostgresConnectionError,)
    )
```

### サーキットブレーカーパターン

```python
# サーキットブレーカーパターン
from enum import Enum
import time

class CircuitState(Enum):
    CLOSED = "closed"  # 正常動作
    OPEN = "open"      # 障害発生、リクエストを拒否
    HALF_OPEN = "half_open"  # 回復試行中

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func: Callable) -> T:
        """サーキットブレーカー経由で関数を呼び出し"""
        if self.state == CircuitState.OPEN:
            # 回復タイムアウトをチェック
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func() if asyncio.iscoroutinefunction(func) else func()
            
            # 成功した場合
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            
            return result
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
            
            raise

# 使用例
async def database_query_with_circuit_breaker(pool, query: str, *args):
    """サーキットブレーカー付きデータベースクエリ"""
    circuit_breaker = CircuitBreaker(
        failure_threshold=5,
        recovery_timeout=60
    )
    
    async def execute_query():
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    return await circuit_breaker.call(execute_query)
```

## トランザクション管理

### トランザクションコンテキストマネージャー

```python
# トランザクション管理のコンテキストマネージャー
from contextlib import asynccontextmanager

class TransactionManager:
    def __init__(self, pool):
        self.pool = pool
    
    @asynccontextmanager
    async def transaction(self, isolation_level: str = "READ COMMITTED"):
        """トランザクションコンテキストマネージャー"""
        async with self.pool.acquire() as conn:
            async with conn.transaction(isolation=isolation_level):
                yield conn

# 使用例
async def transfer_funds(pool, from_account: int, to_account: int, amount: float):
    """資金を転送（トランザクション内で実行）"""
    tx_manager = TransactionManager(pool)
    
    async with tx_manager.transaction():
        # 送金元から引き落とし
        await conn.execute(
            "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
            amount, from_account
        )
        
        # 送金先に追加
        await conn.execute(
            "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
            amount, to_account
        )
        
        # トランザクションログを記録
        await conn.execute("""
            INSERT INTO transactions (from_account, to_account, amount, created_at)
            VALUES ($1, $2, $3, NOW())
        """, from_account, to_account, amount)
```

### 分散トランザクション（Sagaパターン）

```python
# Sagaパターンによる分散トランザクション管理
class SagaTransaction:
    def __init__(self):
        self.steps = []
        self.compensations = []
    
    def add_step(self, step_func: Callable, compensation_func: Callable):
        """ステップと補償処理を追加"""
        self.steps.append(step_func)
        self.compensations.append(compensation_func)
    
    async def execute(self):
        """Sagaトランザクションを実行"""
        executed_steps = []
        
        try:
            for step in self.steps:
                result = await step()
                executed_steps.append(step)
        except Exception as e:
            # 補償処理を実行（逆順）
            for step in reversed(executed_steps):
                idx = self.steps.index(step)
                await self.compensations[idx]()
            raise e

# 使用例
async def order_processing(order_id: int):
    """注文処理（Sagaパターン）"""
    saga = SagaTransaction()
    
    # ステップ1: 在庫を確保
    async def reserve_inventory():
        # 在庫確保処理
        pass
    
    async def release_inventory():
        # 在庫解放処理
        pass
    
    saga.add_step(reserve_inventory, release_inventory)
    
    # ステップ2: 支払いを処理
    async def process_payment():
        # 支払い処理
        pass
    
    async def refund_payment():
        # 返金処理
        pass
    
    saga.add_step(process_payment, refund_payment)
    
    # 実行
    await saga.execute()
```

## データマイグレーション戦略

### バージョン管理されたマイグレーション

```python
# データベースマイグレーション管理
import asyncpg
from pathlib import Path

class MigrationManager:
    def __init__(self, pool):
        self.pool = pool
        self.migrations_dir = Path("migrations")
    
    async def init_migration_table(self):
        """マイグレーション管理テーブルを作成"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
    
    async def get_applied_migrations(self):
        """適用済みマイグレーションを取得"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT version FROM schema_migrations ORDER BY version")
            return [row['version'] for row in rows]
    
    async def apply_migration(self, version: str, sql: str):
        """マイグレーションを適用"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # SQLを実行
                await conn.execute(sql)
                
                # マイグレーション履歴を記録
                await conn.execute("""
                    INSERT INTO schema_migrations (version, applied_at)
                    VALUES ($1, NOW())
                """, version)
    
    async def run_migrations(self):
        """すべてのマイグレーションを実行"""
        await self.init_migration_table()
        applied = await self.get_applied_migrations()
        
        # マイグレーションファイルを読み込む
        migration_files = sorted(self.migrations_dir.glob("*.sql"))
        
        for migration_file in migration_files:
            version = migration_file.stem
            
            if version not in applied:
                print(f"Applying migration: {version}")
                sql = migration_file.read_text()
                await self.apply_migration(version, sql)
```

### ロールバック可能なマイグレーション

```python
# ロールバック対応マイグレーション
class RollbackableMigration:
    def __init__(self, pool):
        self.pool = pool
    
    async def migrate(self, up_sql: str, down_sql: str, version: str):
        """マイグレーションを適用"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                try:
                    # アップマイグレーションを実行
                    await conn.execute(up_sql)
                    
                    # ダウンマイグレーションSQLを保存
                    await conn.execute("""
                        INSERT INTO migration_rollbacks (version, down_sql)
                        VALUES ($1, $2)
                    """, version, down_sql)
                except Exception as e:
                    # エラーが発生した場合、自動的にロールバック
                    raise e
    
    async def rollback(self, version: str):
        """マイグレーションをロールバック"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # ダウンマイグレーションSQLを取得
                row = await conn.fetchrow("""
                    SELECT down_sql FROM migration_rollbacks WHERE version = $1
                """, version)
                
                if row:
                    # ダウンマイグレーションを実行
                    await conn.execute(row['down_sql'])
                    
                    # 履歴を削除
                    await conn.execute("""
                        DELETE FROM migration_rollbacks WHERE version = $1
                    """, version)
```

## 監視とロギング

### クエリパフォーマンス監視

```python
# クエリパフォーマンスの監視
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class QueryMonitor:
    def __init__(self, slow_query_threshold: float = 1.0):
        self.slow_query_threshold = slow_query_threshold
        self.query_stats = []
    
    def monitor_query(self, query: str):
        """クエリを監視するデコレータ"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # スロークエリをログに記録
                    if execution_time > self.slow_query_threshold:
                        logger.warning(
                            f"Slow query detected: {query[:100]} "
                            f"(took {execution_time:.2f}s)"
                        )
                    
                    # 統計を記録
                    self.query_stats.append({
                        'query': query[:100],
                        'execution_time': execution_time,
                        'timestamp': time.time()
                    })
                    
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(
                        f"Query failed: {query[:100]} "
                        f"(took {execution_time:.2f}s): {e}"
                    )
                    raise
            return wrapper
        return decorator
    
    def get_slow_queries(self, limit: int = 10):
        """スロークエリを取得"""
        return sorted(
            self.query_stats,
            key=lambda x: x['execution_time'],
            reverse=True
        )[:limit]

# 使用例
monitor = QueryMonitor(slow_query_threshold=1.0)

@monitor.monitor_query("SELECT * FROM users WHERE id = $1")
async def get_user(pool, user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
```

### 接続プールのメトリクス収集

```python
# 接続プールのメトリクス収集
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge

class PoolMetrics:
    def __init__(self):
        # メトリクスを定義
        self.connection_requests = Counter(
            'db_connection_requests_total',
            'Total number of connection requests'
        )
        self.connection_errors = Counter(
            'db_connection_errors_total',
            'Total number of connection errors'
        )
        self.query_duration = Histogram(
            'db_query_duration_seconds',
            'Query execution duration',
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        self.active_connections = Gauge(
            'db_active_connections',
            'Number of active database connections'
        )
        self.pool_size = Gauge(
            'db_pool_size',
            'Current connection pool size'
        )
    
    def record_connection_request(self):
        """接続リクエストを記録"""
        self.connection_requests.inc()
    
    def record_connection_error(self):
        """接続エラーを記録"""
        self.connection_errors.inc()
    
    def record_query(self, duration: float):
        """クエリ実行時間を記録"""
        self.query_duration.observe(duration)
    
    def update_pool_metrics(self, pool):
        """プールメトリクスを更新"""
        self.active_connections.set(pool.get_size() - pool.get_idle_size())
        self.pool_size.set(pool.get_size())
```

## パフォーマンスチューニング

### クエリ最適化のベストプラクティス

```python
# クエリ最適化のヘルパー
class QueryOptimizer:
    @staticmethod
    def add_pagination(query: str, limit: int, offset: int) -> str:
        """ページネーションを追加"""
        return f"{query} LIMIT {limit} OFFSET {offset}"
    
    @staticmethod
    def add_index_hint(query: str, index_name: str) -> str:
        """インデックスヒントを追加（PostgreSQLでは使用不可、MySQLで使用可能）"""
        # PostgreSQLでは使用できないが、概念を示す
        return query  # 実際の実装はデータベースに依存
    
    @staticmethod
    def optimize_select(query: str, only_needed_columns: bool = True) -> str:
        """SELECTクエリを最適化"""
        if only_needed_columns and "SELECT *" in query.upper():
            # SELECT *を避ける（実際の実装ではより高度な解析が必要）
            pass
        return query

# 使用例
optimizer = QueryOptimizer()

# ページネーション付きクエリ
query = "SELECT id, name, email FROM users WHERE active = true"
paginated_query = optimizer.add_pagination(query, limit=20, offset=0)
```

### バッチ処理の最適化

```python
# バッチ処理の最適化
class BatchProcessor:
    def __init__(self, pool, batch_size: int = 1000):
        self.pool = pool
        self.batch_size = batch_size
    
    async def batch_insert(self, table: str, columns: list, data: list):
        """バッチ挿入を実行"""
        async with self.pool.acquire() as conn:
            # データをバッチに分割
            for i in range(0, len(data), self.batch_size):
                batch = data[i:i + self.batch_size]
                
                # バッチで挿入
                await conn.executemany(
                    f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['$' + str(j+1) for j in range(len(columns))])})",
                    batch
                )
    
    async def batch_update(self, table: str, update_query: str, data: list):
        """バッチ更新を実行"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for batch in self._chunk_data(data, self.batch_size):
                    await conn.executemany(update_query, batch)
    
    def _chunk_data(self, data: list, chunk_size: int):
        """データをチャンクに分割"""
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]
```

## エラーハンドリング

### 包括的なエラーハンドリング

```python
# データベースエラーの包括的なハンドリング
import asyncpg
from typing import Optional

class DatabaseErrorHandler:
    @staticmethod
    def handle_error(error: Exception) -> Optional[str]:
        """エラーを処理してユーザーフレンドリーなメッセージを返す"""
        if isinstance(error, asyncpg.PostgresConnectionError):
            return "データベースへの接続に失敗しました。しばらくしてから再試行してください。"
        elif isinstance(error, asyncpg.UniqueViolationError):
            return "このデータは既に存在します。"
        elif isinstance(error, asyncpg.ForeignKeyViolationError):
            return "参照されているデータが存在しないため、操作を完了できませんでした。"
        elif isinstance(error, asyncpg.CheckViolationError):
            return "データの制約条件を満たしていません。"
        elif isinstance(error, asyncpg.NotNullViolationError):
            return "必須項目が入力されていません。"
        else:
            # 予期しないエラー
            logger.error(f"Unexpected database error: {error}")
            return "データベースエラーが発生しました。管理者にお問い合わせください。"

# 使用例
async def safe_database_operation(pool, query: str, *args):
    """安全なデータベース操作"""
    try:
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)
    except Exception as e:
        user_message = DatabaseErrorHandler.handle_error(e)
        raise DatabaseError(user_message) from e
```

## 実装例

### 完全なデータベース接続マネージャー

```python
# 完全なデータベース接続マネージャーの実装例
import asyncio
import asyncpg
import logging
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None
        self.retry_handler = RetryHandler(max_retries=3)
        self.circuit_breaker = CircuitBreaker(failure_threshold=5)
        self.monitor = QueryMonitor(slow_query_threshold=1.0)
        self.metrics = PoolMetrics()
    
    async def initialize(self):
        """データベース接続プールを初期化"""
        self.pool = await asyncpg.create_pool(
            host=self.config['host'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
            min_size=self.config.get('min_size', 5),
            max_size=self.config.get('max_size', 20),
            command_timeout=self.config.get('command_timeout', 30)
        )
        logger.info("Database connection pool initialized")
    
    @asynccontextmanager
    async def get_connection(self):
        """コネクションを取得（コンテキストマネージャー）"""
        self.metrics.record_connection_request()
        try:
            async with self.pool.acquire() as conn:
                yield conn
        except Exception as e:
            self.metrics.record_connection_error()
            raise
    
    @asynccontextmanager
    async def transaction(self, isolation_level: str = "READ COMMITTED"):
        """トランザクションコンテキストマネージャー"""
        async with self.get_connection() as conn:
            async with conn.transaction(isolation=isolation_level):
                yield conn
    
    async def execute(self, query: str, *args):
        """クエリを実行（リトライ、サーキットブレーカー、監視付き）"""
        async def _execute():
            start_time = time.time()
            try:
                async with self.get_connection() as conn:
                    result = await conn.execute(query, *args)
                    duration = time.time() - start_time
                    self.monitor.query_stats.append({
                        'query': query[:100],
                        'execution_time': duration,
                        'timestamp': time.time()
                    })
                    self.metrics.record_query(duration)
                    return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Query execution failed: {query[:100]} (took {duration:.2f}s): {e}")
                raise
        
        return await self.circuit_breaker.call(
            lambda: self.retry_handler.execute_with_retry(_execute)
        )
    
    async def fetch(self, query: str, *args):
        """クエリを実行して結果を取得"""
        async def _fetch():
            start_time = time.time()
            try:
                async with self.get_connection() as conn:
                    result = await conn.fetch(query, *args)
                    duration = time.time() - start_time
                    self.monitor.query_stats.append({
                        'query': query[:100],
                        'execution_time': duration,
                        'timestamp': time.time()
                    })
                    self.metrics.record_query(duration)
                    return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Query fetch failed: {query[:100]} (took {duration:.2f}s): {e}")
                raise
        
        return await self.circuit_breaker.call(
            lambda: self.retry_handler.execute_with_retry(_fetch)
        )
    
    async def get_health(self):
        """データベースの健全性をチェック"""
        try:
            await self.execute("SELECT 1")
            return {'status': 'healthy', 'pool_stats': await self.get_pool_stats()}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    async def get_pool_stats(self):
        """プールの統計情報を取得"""
        if self.pool:
            return {
                'size': self.pool.get_size(),
                'idle_size': self.pool.get_idle_size(),
                'min_size': self.pool.get_min_size(),
                'max_size': self.pool.get_max_size()
            }
        return {}
    
    async def close(self):
        """プールを閉じる"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

# 使用例
async def main():
    config = {
        'host': 'localhost',
        'database': 'myapp',
        'user': 'postgres',
        'password': 'password',
        'min_size': 5,
        'max_size': 20
    }
    
    db = DatabaseManager(config)
    await db.initialize()
    
    try:
        # クエリを実行
        users = await db.fetch("SELECT * FROM users WHERE active = $1", True)
        print(f"Found {len(users)} active users")
        
        # トランザクション内で操作
        async with db.transaction() as conn:
            await conn.execute(
                "UPDATE users SET last_login = NOW() WHERE id = $1",
                1
            )
        
        # 健全性チェック
        health = await db.get_health()
        print(f"Database health: {health}")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## まとめ

共通パターンとベストプラクティスの重要なポイント：

### コネクションプーリング
- 適切なプールサイズの設定
- プールの監視と動的調整
- コンテキストマネージャーの活用

### リトライとサーキットブレーカー
- 指数バックオフリトライ
- サーキットブレーカーパターンによる障害の隔離
- 適切な例外処理

### トランザクション管理
- トランザクションコンテキストマネージャー
- 分散トランザクション（Sagaパターン）
- 適切な分離レベル

### データマイグレーション
- バージョン管理されたマイグレーション
- ロールバック可能なマイグレーション
- 安全なマイグレーション実行

### 監視とロギング
- クエリパフォーマンス監視
- 接続プールのメトリクス収集
- スロークエリの検出

### パフォーマンスチューニング
- クエリ最適化
- バッチ処理の最適化
- インデックスの適切な使用

### エラーハンドリング
- 包括的なエラーハンドリング
- ユーザーフレンドリーなエラーメッセージ
- 適切なロギング

これらのパターンとベストプラクティスを適用することで、堅牢でパフォーマンスの高いデータベース接続システムを構築できます。



