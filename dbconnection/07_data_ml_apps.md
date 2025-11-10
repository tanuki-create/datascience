# データ分析・機械学習アプリケーション向けデータベース接続ベストプラクティス

## 概要

このガイドは、データ分析、機械学習推論、レコメンデーションシステム、データウェアハウス、ETL/ELTパイプラインなど、データ集約的なアプリケーション向けのデータベース接続とデータ管理のベストプラクティスを提供します。大量データの効率的な処理、ストレージ最適化、計算リソース管理に焦点を当てています。

### ターゲットアプリケーション

- データ分析プラットフォーム
- 機械学習推論サービス
- レコメンデーションシステム
- データウェアハウス
- ETL/ELTパイプライン
- ビジネスインテリジェンス（BI）ツール
- 時系列分析システム
- 特徴量ストア

## レイテンシ最適化

### バッチ処理とストリーミング処理の使い分け

データ分析アプリケーションでは、バッチ処理とストリーミング処理を適切に使い分けることが重要です。

```python
# バッチ処理とストリーミング処理の実装例
import asyncio
from datetime import datetime, timedelta
import pandas as pd

class DataProcessingPipeline:
    def __init__(self):
        self.batch_size = 10000
        self.stream_buffer = []
    
    async def batch_process(self, start_date: datetime, end_date: datetime):
        """バッチ処理：大量データを効率的に処理"""
        async with self.db_pool.acquire() as conn:
            # チャンクごとにデータを取得
            offset = 0
            while True:
                # チャンクサイズでデータを取得
                rows = await conn.fetch("""
                    SELECT * FROM raw_data
                    WHERE created_at BETWEEN $1 AND $2
                    ORDER BY id
                    LIMIT $3 OFFSET $4
                """, start_date, end_date, self.batch_size, offset)
                
                if not rows:
                    break
                
                # データを処理
                df = pd.DataFrame([dict(row) for row in rows])
                await self.process_chunk(df)
                
                offset += self.batch_size
    
    async def stream_process(self, data_stream):
        """ストリーミング処理：リアルタイムデータを処理"""
        async for data_chunk in data_stream:
            self.stream_buffer.append(data_chunk)
            
            # バッファが一定サイズに達したら処理
            if len(self.stream_buffer) >= 1000:
                await self.process_stream_buffer()
                self.stream_buffer.clear()
    
    async def process_stream_buffer(self):
        """ストリームバッファを処理"""
        df = pd.DataFrame(self.stream_buffer)
        # 軽量な処理を実行
        processed = self.lightweight_transform(df)
        
        # 処理済みデータを保存
        await self.save_processed_data(processed)
```

### 読み取り専用レプリカの活用

分析クエリは読み取り専用レプリカから実行し、プライマリデータベースへの負荷を軽減します。

```python
# 読み取り専用レプリカの活用
class AnalyticsQueryExecutor:
    def __init__(self):
        # プライマリ（書き込み用）
        self.write_pool = None
        # レプリカ（読み取り用、複数）
        self.read_pools = []
        self.current_read_pool = 0
    
    async def execute_analytics_query(self, query: str, params: tuple = None):
        """分析クエリをレプリカで実行"""
        # ラウンドロビンでレプリカを選択
        pool = self.read_pools[self.current_read_pool]
        self.current_read_pool = (self.current_read_pool + 1) % len(self.read_pools)
        
        async with pool.acquire() as conn:
            return await conn.fetch(query, *params if params else ())
    
    async def execute_aggregation(self, table: str, group_by: str, metrics: list):
        """集計クエリを実行（レプリカから）"""
        query = f"""
            SELECT {group_by}, {', '.join(metrics)}
            FROM {table}
            GROUP BY {group_by}
        """
        return await self.execute_analytics_query(query)
```

### 接続プールの最適化

長時間実行される分析クエリに対応した接続プール設定。

```python
# 分析クエリ用の接続プール設定
import asyncpg

async def create_analytics_pool():
    """分析クエリ用の接続プール"""
    pool = await asyncpg.create_pool(
        host='localhost',
        database='analytics_db',
        user='analytics_user',
        password='password',
        min_size=5,
        max_size=20,  # 分析クエリは長時間実行されるため、接続数を制限
        max_queries=1000,
        max_inactive_connection_lifetime=1800,  # 30分
        command_timeout=3600,  # 1時間（長時間実行クエリに対応）
        server_settings={
            'application_name': 'analytics_app',
            'statement_timeout': '3600000',  # 1時間
            'work_mem': '256MB',  # 分析クエリ用にメモリを増やす
        }
    )
    return pool
```

## 経済的最適化

### データレイヤーの階層化

アクセス頻度に応じてデータを異なるストレージ層に配置し、コストを最適化します。

```python
# データレイヤーの階層化（ホット、ウォーム、コールド）
class TieredDataStorage:
    def __init__(self):
        # ホットデータ：PostgreSQL（最近のデータ、頻繁にアクセス）
        self.hot_storage = None
        
        # ウォームデータ：S3 + PostgreSQL（中程度のアクセス頻度）
        self.warm_storage_s3 = None
        
        # コールドデータ：S3 Glacier（アーカイブ、まれにアクセス）
        self.cold_storage = None
    
    async def get_data(self, data_id: str, date: datetime):
        """データレイヤーから適切にデータを取得"""
        days_old = (datetime.now() - date).days
        
        if days_old <= 30:
            # ホットデータ：PostgreSQLから取得
            async with self.hot_storage.acquire() as conn:
                return await conn.fetchrow(
                    "SELECT * FROM hot_data WHERE id = $1", data_id
                )
        elif days_old <= 365:
            # ウォームデータ：S3から取得
            return await self.get_from_s3(f"warm/{data_id}")
        else:
            # コールドデータ：Glacierから取得（非同期）
            return await self.get_from_glacier(f"cold/{data_id}")
    
    async def archive_old_data(self, days: int = 365):
        """古いデータをアーカイブ（コスト削減）"""
        # 365日以上前のデータをS3 Glacierに移動
        async with self.hot_storage.acquire() as conn:
            old_data = await conn.fetch("""
                SELECT * FROM hot_data
                WHERE created_at < NOW() - INTERVAL '%s days'
            """, days)
            
            # S3 Glacierにアップロード
            for row in old_data:
                await self.upload_to_glacier(row)
            
            # ホットストレージから削除
            await conn.execute("""
                DELETE FROM hot_data
                WHERE created_at < NOW() - INTERVAL '%s days'
            """, days)
```

### 列指向ストレージの活用

分析クエリでは列指向データベースが効率的です。

```python
# 列指向データベース（例：ClickHouse、Amazon Redshift）の活用
class ColumnarStorage:
    async def setup_columnar_table(self):
        """列指向テーブルをセットアップ"""
        async with self.pool.acquire() as conn:
            # ClickHouseの例
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_events (
                    event_date Date,
                    event_time DateTime,
                    user_id String,
                    event_type String,
                    properties String
                ) ENGINE = MergeTree()
                PARTITION BY toYYYYMM(event_date)
                ORDER BY (event_date, event_type, user_id)
            """)
    
    async def insert_events_batch(self, events: list):
        """イベントをバッチで挿入（列指向DBはバッチ挿入が効率的）"""
        async with self.pool.acquire() as conn:
            # バッチ挿入
            await conn.executemany("""
                INSERT INTO analytics_events 
                (event_date, event_time, user_id, event_type, properties)
                VALUES ($1, $2, $3, $4, $5)
            """, events)
    
    async def aggregate_by_date(self, start_date: date, end_date: date):
        """日付で集計（列指向DBは集計が高速）"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT 
                    event_date,
                    event_type,
                    count() as event_count,
                    uniq(user_id) as unique_users
                FROM analytics_events
                WHERE event_date BETWEEN $1 AND $2
                GROUP BY event_date, event_type
                ORDER BY event_date, event_type
            """, start_date, end_date)
```

### パーティショニング戦略

大規模データをパーティション分割して、クエリパフォーマンスとコストを最適化します。

```python
# パーティショニング戦略
class PartitionedDataStorage:
    async def setup_partitioned_table(self):
        """パーティション分割されたテーブルをセットアップ"""
        async with self.pool.acquire() as conn:
            # PostgreSQLのパーティショニング例
            await conn.execute("""
                -- 親テーブル
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id BIGSERIAL,
                    sensor_id TEXT NOT NULL,
                    value DOUBLE PRECISION,
                    created_at TIMESTAMPTZ NOT NULL,
                    PRIMARY KEY (id, created_at)
                ) PARTITION BY RANGE (created_at);
                
                -- 月次パーティションを作成
                CREATE TABLE sensor_data_2024_01 
                PARTITION OF sensor_data
                FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
                
                CREATE TABLE sensor_data_2024_02 
                PARTITION OF sensor_data
                FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
            """)
    
    async def query_partitioned_data(self, start_date: datetime, end_date: datetime):
        """パーティション分割されたデータをクエリ"""
        async with self.pool.acquire() as conn:
            # PostgreSQLは自動的に適切なパーティションを選択
            return await conn.fetch("""
                SELECT sensor_id, AVG(value) as avg_value
                FROM sensor_data
                WHERE created_at BETWEEN $1 AND $2
                GROUP BY sensor_id
            """, start_date, end_date)
    
    async def drop_old_partitions(self, months_to_keep: int = 12):
        """古いパーティションを削除（コスト削減）"""
        async with self.pool.acquire() as conn:
            # 12ヶ月より古いパーティションを削除
            await conn.execute("""
                DROP TABLE IF EXISTS sensor_data_old_partitions;
            """)
```

## セキュリティ

### データガバナンスとアクセス制御

分析データへのアクセスを適切に制御します。

```python
# ロールベースアクセス制御（RBAC）
class AnalyticsAccessControl:
    def __init__(self):
        self.roles = {
            'admin': ['read', 'write', 'delete'],
            'analyst': ['read'],
            'viewer': ['read_limited']
        }
    
    async def check_permission(self, user_role: str, action: str, resource: str) -> bool:
        """権限をチェック"""
        if user_role not in self.roles:
            return False
        
        permissions = self.roles[user_role]
        
        if action == 'read':
            return 'read' in permissions or 'read_limited' in permissions
        elif action == 'write':
            return 'write' in permissions
        elif action == 'delete':
            return 'delete' in permissions
        
        return False
    
    async def execute_analytics_query(self, user_role: str, query: str):
        """権限チェック付きで分析クエリを実行"""
        if not await self.check_permission(user_role, 'read', 'analytics_data'):
            raise PermissionError("Access denied")
        
        # ビューアーロールの場合は制限付きクエリ
        if user_role == 'viewer':
            query = self.apply_data_masking(query)
        
        return await self.db_pool.fetch(query)
    
    def apply_data_masking(self, query: str) -> str:
        """データマスキングを適用（PIIを保護）"""
        # メールアドレスや電話番号をマスキング
        # 実装例
        return query.replace('email', 'masked_email')
```

### データ暗号化

保存時と転送時のデータ暗号化を実装します。

```python
# データ暗号化の実装
from cryptography.fernet import Fernet
import base64

class EncryptedDataStorage:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)
    
    def encrypt_sensitive_field(self, data: str) -> str:
        """機密データを暗号化"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_sensitive_field(self, encrypted_data: str) -> str:
        """暗号化されたデータを復号化"""
        decrypted = self.cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted.decode()
    
    async def store_encrypted_data(self, user_id: str, sensitive_data: dict):
        """暗号化されたデータを保存"""
        encrypted = {
            k: self.encrypt_sensitive_field(v) if k in ['email', 'phone'] else v
            for k, v in sensitive_data.items()
        }
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO encrypted_user_data (user_id, data)
                VALUES ($1, $2)
            """, user_id, json.dumps(encrypted))
```

## UX最適化

### 非同期処理と進捗表示

長時間実行される分析処理を非同期で実行し、進捗を表示します。

```python
# 非同期処理と進捗追跡
import asyncio
from celery import Celery

celery_app = Celery('analytics_app', broker='redis://localhost:6379/0')

class AsyncAnalyticsProcessor:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
    
    @celery_app.task(bind=True)
    def process_large_dataset(self, task_id: str, query_params: dict):
        """大規模データセットを非同期で処理"""
        total_records = self.get_total_records(query_params)
        processed = 0
        
        for chunk in self.process_in_chunks(query_params):
            # チャンクを処理
            self.process_chunk(chunk)
            processed += len(chunk)
            
            # 進捗を更新
            progress = (processed / total_records) * 100
            self.redis.setex(
                f"task_progress:{task_id}",
                3600,
                json.dumps({
                    'progress': progress,
                    'processed': processed,
                    'total': total_records,
                    'status': 'processing'
                })
            )
        
        # 完了
        self.redis.setex(
            f"task_progress:{task_id}",
            3600,
            json.dumps({
                'progress': 100,
                'status': 'completed',
                'result_url': f"/results/{task_id}"
            })
        )
    
    async def get_progress(self, task_id: str) -> dict:
        """進捗を取得"""
        progress_data = self.redis.get(f"task_progress:{task_id}")
        if progress_data:
            return json.loads(progress_data)
        return {'status': 'not_found'}
```

### キャッシュされた分析結果

頻繁にアクセスされる分析結果をキャッシュします。

```python
# 分析結果のキャッシュ
class CachedAnalytics:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.cache_ttl = 3600  # 1時間
    
    async def get_cached_analytics(self, query_hash: str):
        """キャッシュされた分析結果を取得"""
        cached = self.redis.get(f"analytics:{query_hash}")
        if cached:
            return json.loads(cached)
        return None
    
    async def execute_and_cache(self, query: str, params: tuple = None):
        """クエリを実行し、結果をキャッシュ"""
        import hashlib
        query_hash = hashlib.md5(f"{query}{params}".encode()).hexdigest()
        
        # キャッシュをチェック
        cached = await self.get_cached_analytics(query_hash)
        if cached:
            return cached
        
        # クエリを実行
        async with self.db_pool.acquire() as conn:
            result = await conn.fetch(query, *params if params else ())
            data = [dict(row) for row in result]
        
        # キャッシュに保存
        self.redis.setex(
            f"analytics:{query_hash}",
            self.cache_ttl,
            json.dumps(data)
        )
        
        return data
```

## データ保存戦略

### データウェアハウス: Amazon Redshift / Snowflake

大規模な分析データにはデータウェアハウスが適しています。

```python
# Amazon Redshiftへの接続とクエリ
import psycopg2

class RedshiftAnalytics:
    def __init__(self):
        self.conn = psycopg2.connect(
            host='your-redshift-cluster.amazonaws.com',
            port=5439,
            database='analytics',
            user='analytics_user',
            password='password'
        )
    
    def execute_analytics_query(self, query: str):
        """分析クエリを実行"""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def load_data_from_s3(self, s3_path: str, table_name: str):
        """S3からデータをロード"""
        query = f"""
            COPY {table_name}
            FROM '{s3_path}'
            IAM_ROLE 'arn:aws:iam::account:role/RedshiftRole'
            CSV
            IGNOREHEADER 1
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
        self.conn.commit()
```

### 時系列データベース: InfluxDB / TimescaleDB

時系列データの分析には時系列データベースが最適です。

```python
# InfluxDBを使った時系列データ分析
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBAnalytics:
    def __init__(self):
        self.client = InfluxDBClient(
            url="http://localhost:8086",
            token="your-token",
            org="your-org"
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
    
    def write_time_series_data(self, measurement: str, tags: dict, fields: dict, time: datetime):
        """時系列データを書き込み"""
        point = Point(measurement).time(time)
        for key, value in tags.items():
            point.tag(key, value)
        for key, value in fields.items():
            point.field(key, value)
        
        self.write_api.write(bucket="analytics", record=point)
    
    def query_time_series(self, measurement: str, start_time: datetime, end_time: datetime):
        """時系列データをクエリ"""
        query = f'''
            from(bucket: "analytics")
            |> range(start: {start_time.isoformat()}, stop: {end_time.isoformat()})
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
        '''
        return self.query_api.query(org="your-org", query=query)
```

### 特徴量ストア: Feast / Tecton

機械学習モデル用の特徴量を管理します。

```python
# Feastを使った特徴量ストア
from feast import FeatureStore

class FeatureStoreManager:
    def __init__(self, repo_path: str):
        self.fs = FeatureStore(repo_path=repo_path)
    
    def get_online_features(self, entity_rows: list, features: list):
        """オンライン特徴量を取得（低レイテンシ）"""
        return self.fs.get_online_features(
            features=features,
            entity_rows=entity_rows
        ).to_dict()
    
    def get_historical_features(self, entity_df, features: list):
        """履歴特徴量を取得（トレーニング用）"""
        return self.fs.get_historical_features(
            features=features,
            entity_df=entity_df
        ).to_df()
```

### NoSQL: MongoDB / Cassandra

柔軟なスキーマが必要な分析データにはNoSQLが適しています。

```python
# MongoDBを使った分析データ管理
from pymongo import MongoClient
import pandas as pd

class MongoDBAnalytics:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['analytics_db']
    
    def store_analytics_event(self, event: dict):
        """分析イベントを保存"""
        self.db.events.insert_one(event)
    
    def aggregate_events(self, pipeline: list):
        """MongoDBの集計パイプラインを実行"""
        return list(self.db.events.aggregate(pipeline))
    
    def export_to_dataframe(self, collection: str, query: dict = None):
        """MongoDBのデータをPandas DataFrameにエクスポート"""
        cursor = self.db[collection].find(query) if query else self.db[collection].find()
        return pd.DataFrame(list(cursor))
```

## キャッシュ戦略

### 分析結果のキャッシュ

計算コストの高い分析結果をキャッシュします。

```python
# 分析結果の多層キャッシュ
class AnalyticsCache:
    def __init__(self):
        # L1: メモリキャッシュ（最速、小容量）
        self.memory_cache = {}
        
        # L2: Redis（高速、中容量）
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # L3: データベース（永続化、大容量）
        self.db_pool = None
    
    async def get_cached_result(self, query_hash: str):
        """キャッシュされた結果を取得"""
        # L1: メモリキャッシュ
        if query_hash in self.memory_cache:
            return self.memory_cache[query_hash]
        
        # L2: Redis
        cached = self.redis.get(f"analytics:{query_hash}")
        if cached:
            result = json.loads(cached)
            # メモリキャッシュにも保存
            self.memory_cache[query_hash] = result
            return result
        
        # L3: データベース
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT result FROM cached_analytics WHERE query_hash = $1",
                query_hash
            )
            if row:
                result = json.loads(row['result'])
                # 上位キャッシュにも保存
                self.memory_cache[query_hash] = result
                self.redis.setex(f"analytics:{query_hash}", 3600, json.dumps(result))
                return result
        
        return None
    
    async def cache_result(self, query_hash: str, result: dict, ttl: int = 3600):
        """結果をキャッシュ"""
        # すべてのレイヤーに保存
        self.memory_cache[query_hash] = result
        self.redis.setex(f"analytics:{query_hash}", ttl, json.dumps(result))
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO cached_analytics (query_hash, result, created_at)
                VALUES ($1, $2, NOW())
                ON CONFLICT (query_hash) DO UPDATE
                SET result = $2, created_at = NOW()
            """, query_hash, json.dumps(result))
```

## オーケストレーション

### ETL/ELTパイプラインのオーケストレーション

データパイプラインを効率的にオーケストレーションします。

```python
# Apache Airflowを使ったETLパイプライン
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract_data():
    """データ抽出"""
    # データソースからデータを抽出
    pass

def transform_data():
    """データ変換"""
    # データを変換
    pass

def load_data():
    """データロード"""
    # データウェアハウスにロード
    pass

# DAG定義
default_args = {
    'owner': 'analytics_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'analytics_etl_pipeline',
    default_args=default_args,
    description='Analytics ETL Pipeline',
    schedule_interval=timedelta(hours=1),
    catchup=False,
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
```

### 分散処理: Spark / Dask

大規模データの分散処理を実装します。

```python
# PySparkを使った分散処理
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

class SparkAnalytics:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("AnalyticsApp") \
            .config("spark.sql.warehouse.dir", "/tmp/warehouse") \
            .getOrCreate()
    
    def process_large_dataset(self, input_path: str, output_path: str):
        """大規模データセットを処理"""
        df = self.spark.read.parquet(input_path)
        
        # 集計処理
        result = df.groupBy("category") \
            .agg(
                avg("value").alias("avg_value"),
                count("*").alias("count")
            )
        
        # 結果を保存
        result.write.parquet(output_path)
    
    def join_large_datasets(self, df1_path: str, df2_path: str):
        """大規模データセットを結合"""
        df1 = self.spark.read.parquet(df1_path)
        df2 = self.spark.read.parquet(df2_path)
        
        return df1.join(df2, on="id", how="inner")
```

## 実装例

### 完全な分析パイプライン

```python
# 完全な分析パイプラインの実装例
import asyncio
import asyncpg
import pandas as pd
from datetime import datetime, timedelta

class CompleteAnalyticsPipeline:
    def __init__(self):
        self.db_pool = None
        self.redis = redis.Redis(host='localhost', port=6379)
    
    async def init_database(self):
        """データベースを初期化"""
        self.db_pool = await asyncpg.create_pool(
            host='localhost',
            database='analytics_db',
            user='analytics_user',
            password='password',
            min_size=5,
            max_size=20
        )
        
        # テーブルを作成
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS raw_events (
                    id SERIAL PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    properties JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                
                CREATE INDEX idx_raw_events_created ON raw_events(created_at);
                CREATE INDEX idx_raw_events_type ON raw_events(event_type);
                
                CREATE TABLE IF NOT EXISTS aggregated_metrics (
                    id SERIAL PRIMARY KEY,
                    metric_name TEXT NOT NULL,
                    metric_value DOUBLE PRECISION,
                    date DATE NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    UNIQUE(metric_name, date)
                );
            """)
    
    async def ingest_event(self, event_type: str, user_id: str, properties: dict):
        """イベントを取り込み"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO raw_events (event_type, user_id, properties)
                VALUES ($1, $2, $3)
            """, event_type, user_id, json.dumps(properties))
    
    async def aggregate_daily_metrics(self, target_date: date):
        """日次メトリクスを集計"""
        async with self.db_pool.acquire() as conn:
            # イベントタイプごとの集計
            metrics = await conn.fetch("""
                SELECT 
                    event_type,
                    COUNT(*) as event_count,
                    COUNT(DISTINCT user_id) as unique_users
                FROM raw_events
                WHERE DATE(created_at) = $1
                GROUP BY event_type
            """, target_date)
            
            # 集計結果を保存
            for metric in metrics:
                await conn.execute("""
                    INSERT INTO aggregated_metrics (metric_name, metric_value, date)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (metric_name, date) DO UPDATE
                    SET metric_value = $2
                """, f"{metric['event_type']}_count", metric['event_count'], target_date)
    
    async def get_analytics_dashboard(self, start_date: date, end_date: date):
        """分析ダッシュボード用のデータを取得"""
        async with self.db_pool.acquire() as conn:
            return await conn.fetch("""
                SELECT 
                    metric_name,
                    date,
                    metric_value
                FROM aggregated_metrics
                WHERE date BETWEEN $1 AND $2
                ORDER BY date, metric_name
            """, start_date, end_date)

# 使用例
async def main():
    pipeline = CompleteAnalyticsPipeline()
    await pipeline.init_database()
    
    # イベントを取り込み
    await pipeline.ingest_event('page_view', 'user123', {'page': '/home'})
    
    # 日次集計を実行
    await pipeline.aggregate_daily_metrics(datetime.now().date())
    
    # ダッシュボードデータを取得
    dashboard_data = await pipeline.get_analytics_dashboard(
        datetime.now().date() - timedelta(days=7),
        datetime.now().date()
    )
    
    print(dashboard_data)

if __name__ == "__main__":
    asyncio.run(main())
```

## まとめ

データ分析・機械学習アプリケーション向けのデータベース接続ベストプラクティスの重要なポイント：

### レイテンシ最適化
- バッチ処理とストリーミング処理の適切な使い分け
- 読み取り専用レプリカの活用
- 分析クエリ用の接続プール最適化

### 経済的最適化
- データレイヤーの階層化（ホット、ウォーム、コールド）
- 列指向ストレージの活用（ClickHouse、Redshift）
- パーティショニング戦略によるコスト削減

### セキュリティ
- ロールベースアクセス制御（RBAC）
- データ暗号化（保存時、転送時）
- データガバナンスとコンプライアンス

### UX最適化
- 非同期処理と進捗表示
- 分析結果のキャッシュ

### データ保存戦略
- **データウェアハウス**: Amazon Redshift、Snowflake（大規模分析）
- **時系列DB**: InfluxDB、TimescaleDB（時系列データ）
- **特徴量ストア**: Feast、Tecton（ML特徴量管理）
- **NoSQL**: MongoDB、Cassandra（柔軟なスキーマ）

### キャッシュ戦略
- 多層キャッシュ（メモリ → Redis → データベース）
- 分析結果のキャッシュ

### オーケストレーション
- ETL/ELTパイプライン（Apache Airflow）
- 分散処理（Spark、Dask）

データ分析・機械学習アプリケーションでは、大量データの効率的な処理とストレージコストの最適化が重要です。適切なデータベース選択、パーティショニング、キャッシュ戦略により、スケーラブルでコスト効率の良いシステムを構築できます。



