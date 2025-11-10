# 大規模Webアプリケーション向けデータベース接続ベストプラクティス

## 概要

このガイドは、エンタープライズや大規模サービス向けのデータベース接続とデータ管理のベストプラクティスを提供します。グローバルスケール、高可用性、パフォーマンス最適化に焦点を当てています。

### ターゲットアプリケーション

- エンタープライズアプリケーション
- 大規模Webサービス（日次アクティブユーザー > 100,000人）
- グローバルに展開するサービス
- 高可用性が必須のサービス
- 複数のデータセンターに展開

## レイテンシ最適化

### マルチリージョン構成

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import geoip2.database

class MultiRegionDatabaseRouter:
    """マルチリージョン対応のデータベースルーター"""
    
    def __init__(self):
        # リージョンごとのエンジン
        self.engines = {
            'us-east-1': create_engine('postgresql://...@us-east-1.rds.amazonaws.com/db'),
            'us-west-2': create_engine('postgresql://...@us-west-2.rds.amazonaws.com/db'),
            'eu-west-1': create_engine('postgresql://...@eu-west-1.rds.amazonaws.com/db'),
            'ap-northeast-1': create_engine('postgresql://...@ap-northeast-1.rds.amazonaws.com/db'),
        }
        
        # マスター（書き込み用）
        self.master_engine = self.engines['us-east-1']
        
        # リージョン検出
        self.geoip_reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
    
    def get_user_region(self, ip_address):
        """ユーザーのリージョンを取得"""
        try:
            response = self.geoip_reader.city(ip_address)
            country = response.country.iso_code
            
            # 国コードからリージョンをマッピング
            region_map = {
                'US': 'us-east-1',
                'GB': 'eu-west-1',
                'DE': 'eu-west-1',
                'FR': 'eu-west-1',
                'JP': 'ap-northeast-1',
            }
            return region_map.get(country, 'us-east-1')
        except:
            return 'us-east-1'  # デフォルト
    
    def get_read_session(self, user_ip=None):
        """読み取りセッションを取得（最寄りのリージョン）"""
        if user_ip:
            region = self.get_user_region(user_ip)
            engine = self.engines.get(region, self.master_engine)
        else:
            engine = self.master_engine
        
        Session = sessionmaker(bind=engine)
        return Session()
    
    def get_write_session(self):
        """書き込みセッション（マスター）"""
        Session = sessionmaker(bind=self.master_engine)
        return Session()
```

### CDN統合とエッジキャッシング

```python
# CloudFront / Cloudflare Workers でのエッジキャッシング
# データベースクエリ結果をCDNでキャッシュ

import hashlib
import json

def get_cached_data_from_cdn(cache_key, cdn_url):
    """CDNからキャッシュされたデータを取得"""
    import requests
    
    url = f"{cdn_url}/cache/{cache_key}"
    response = requests.get(url, headers={
        'Cache-Control': 'max-age=300'
    })
    
    if response.status_code == 200:
        return json.loads(response.text)
    return None

def set_cached_data_to_cdn(cache_key, data, cdn_url):
    """CDNにデータをキャッシュ"""
    import requests
    
    url = f"{cdn_url}/cache/{cache_key}"
    requests.put(url, json=data, headers={
        'Cache-Control': 'public, max-age=300'
    })
```

### 高度なキャッシュ戦略

```python
from redis.cluster import RedisCluster
import json

class DistributedCache:
    """分散キャッシュシステム"""
    
    def __init__(self):
        # Redis Cluster構成
        startup_nodes = [
            {"host": "redis-node-1", "port": "6379"},
            {"host": "redis-node-2", "port": "6379"},
            {"host": "redis-node-3", "port": "6379"},
        ]
        self.client = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True,
            skip_full_coverage_check=True
        )
    
    def get(self, key):
        """値を取得"""
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None
    
    def set(self, key, value, ttl=300):
        """値を設定"""
        try:
            self.client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def invalidate_pattern(self, pattern):
        """パターンに一致するキーを無効化"""
        try:
            keys = []
            for node in self.client.get_nodes():
                keys.extend(node.keys(pattern))
            
            if keys:
                self.client.delete(*keys)
        except Exception as e:
            print(f"Cache invalidation error: {e}")

# マルチレイヤーキャッシュ
class MultiLayerCache:
    """L1: ローカル、L2: Redis、L3: CDN"""
    
    def __init__(self):
        self.local_cache = {}  # L1: アプリケーションメモリ
        self.redis_cache = DistributedCache()  # L2: Redis Cluster
        self.cdn_url = "https://cdn.example.com"  # L3: CDN
    
    def get(self, key):
        # L1から取得
        if key in self.local_cache:
            return self.local_cache[key]
        
        # L2から取得
        value = self.redis_cache.get(key)
        if value:
            self.local_cache[key] = value
            return value
        
        # L3から取得（CDN）
        value = get_cached_data_from_cdn(key, self.cdn_url)
        if value:
            self.redis_cache.set(key, value, ttl=300)
            self.local_cache[key] = value
            return value
        
        return None
    
    def set(self, key, value, ttl=300):
        # すべてのレイヤーに保存
        self.local_cache[key] = value
        self.redis_cache.set(key, value, ttl=ttl)
        set_cached_data_to_cdn(key, value, self.cdn_url)
```

## 経済的最適化

### リザーブドインスタンスとオートスケーリング

```python
# AWS RDS リザーブドインスタンスの使用
# 1年契約で30-40%のコスト削減

# オートスケーリング設定（CloudFormation例）
"""
Resources:
  DBInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceClass: db.r5.xlarge
      Engine: postgres
      MasterUsername: admin
      MasterUserPassword: !Ref MasterPassword
      AllocatedStorage: 100
      StorageType: gp3
      BackupRetentionPeriod: 7
      MultiAZ: true
      AutoMinorVersionUpgrade: true
      
  DBScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyType: TargetTrackingScaling
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 70.0
        PredefinedMetricSpecification:
          PredefinedMetricType: RDSReaderAverageCPUUtilization
      ScalableDimension: rds:cluster:ReadReplicaCount
      ServiceNamespace: rds
"""

# コスト最適化のためのクエリ分析
from sqlalchemy import event, text
import time

class QueryAnalyzer:
    """高コストなクエリを特定"""
    
    def __init__(self):
        self.slow_queries = []
    
    def analyze_query(self, statement, parameters, duration):
        """クエリを分析"""
        if duration > 1.0:  # 1秒以上のクエリ
            self.slow_queries.append({
                'statement': statement,
                'duration': duration,
                'timestamp': time.time()
            })
    
    def get_costly_queries(self):
        """高コストなクエリを返す"""
        return sorted(
            self.slow_queries,
            key=lambda x: x['duration'],
            reverse=True
        )[:10]

# イベントリスナーの設定
analyzer = QueryAnalyzer()

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    duration = time.time() - context._query_start_time
    analyzer.analyze_query(statement, parameters, duration)
```

### ストレージ最適化

```python
# データアーカイブ戦略
from datetime import datetime, timedelta

class DataArchiver:
    """古いデータをアーカイブ"""
    
    def __init__(self, archive_threshold_days=90):
        self.archive_threshold = timedelta(days=archive_threshold_days)
    
    def archive_old_data(self, table_name, date_column='created_at'):
        """古いデータをアーカイブテーブルに移動"""
        cutoff_date = datetime.utcnow() - self.archive_threshold
        
        # アーカイブテーブルに移動
        query = f"""
            INSERT INTO {table_name}_archive
            SELECT * FROM {table_name}
            WHERE {date_column} < %s
        """
        
        # 元のテーブルから削除
        delete_query = f"""
            DELETE FROM {table_name}
            WHERE {date_column} < %s
        """
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (cutoff_date,))
            cursor.execute(delete_query, (cutoff_date,))
            conn.commit()

# 圧縮とパーティショニング
# PostgreSQLのテーブルパーティショニング
"""
-- 日付によるパーティショニング
CREATE TABLE events (
    id SERIAL,
    event_date DATE NOT NULL,
    data JSONB
) PARTITION BY RANGE (event_date);

-- 月ごとのパーティション
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02 PARTITION OF events
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
"""
```

## セキュリティ

### 多層防御

```python
# 1. ネットワーク層のセキュリティ
# VPC、セキュリティグループ、ネットワークACL

# 2. アプリケーション層のセキュリティ
from cryptography.fernet import Fernet
import os

class DataEncryption:
    """データ暗号化"""
    
    def __init__(self):
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        """データを暗号化"""
        return self.cipher.encrypt(data)
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """データを復号化"""
        return self.cipher.decrypt(encrypted_data)

# 3. データベース層のセキュリティ
# Transparent Data Encryption (TDE)
# PostgreSQLの例
"""
-- 暗号化された接続の強制
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';
"""

# 4. 監査とコンプライアンス
class AuditLogger:
    """包括的な監査ログ"""
    
    def __init__(self):
        self.audit_table = 'audit_logs'
    
    def log_access(self, user_id, resource, action, ip_address):
        """アクセスをログ"""
        query = """
            INSERT INTO audit_logs 
            (user_id, resource, action, ip_address, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, resource, action, ip_address))
            conn.commit()
    
    def log_data_access(self, user_id, table_name, record_id, action):
        """データアクセスをログ（GDPR対応）"""
        query = """
            INSERT INTO data_access_logs
            (user_id, table_name, record_id, action, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, table_name, record_id, action))
            conn.commit()
```

### セキュリティ監視

```python
# 異常検知システム
class SecurityMonitor:
    """セキュリティ監視"""
    
    def __init__(self):
        self.suspicious_patterns = []
    
    def detect_sql_injection_attempt(self, query):
        """SQLインジェクション試行を検出"""
        suspicious_keywords = [
            "'; DROP",
            "UNION SELECT",
            "OR 1=1",
            "--",
            "/*"
        ]
        
        for keyword in suspicious_keywords:
            if keyword.lower() in query.lower():
                self.log_security_event('sql_injection_attempt', query)
                return True
        return False
    
    def detect_brute_force(self, user_id, failed_attempts):
        """ブルートフォース攻撃を検出"""
        if failed_attempts > 5:
            self.log_security_event('brute_force_attempt', user_id)
            # アカウントを一時的にロック
            self.lock_account(user_id, duration_minutes=30)
    
    def log_security_event(self, event_type, details):
        """セキュリティイベントをログ"""
        query = """
            INSERT INTO security_events
            (event_type, details, timestamp, severity)
            VALUES (%s, %s, NOW(), %s)
        """
        severity = 'high' if event_type in ['sql_injection_attempt', 'brute_force_attempt'] else 'medium'
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (event_type, str(details), severity))
            conn.commit()
        
        # アラートを送信
        self.send_alert(event_type, details)
```

## UX最適化

### グローバルな低レイテンシ

```python
# エッジコンピューティングの活用
# Cloudflare Workers, AWS Lambda@Edge

# ユーザーの位置に基づく最適化
class LatencyOptimizer:
    """レイテンシ最適化"""
    
    def __init__(self):
        self.region_endpoints = {
            'us-east-1': 'https://api-us.example.com',
            'eu-west-1': 'https://api-eu.example.com',
            'ap-northeast-1': 'https://api-ap.example.com',
        }
    
    def get_optimal_endpoint(self, user_ip):
        """最適なエンドポイントを取得"""
        region = self.detect_region(user_ip)
        return self.region_endpoints.get(region, self.region_endpoints['us-east-1'])
    
    def detect_region(self, ip_address):
        """IPアドレスからリージョンを検出"""
        # GeoIPデータベースを使用
        # 実装は省略
        return 'us-east-1'
```

### 高可用性の実現

```python
# フェイルオーバーの実装
class HighAvailabilityManager:
    """高可用性管理"""
    
    def __init__(self):
        self.primary_db = create_engine('postgresql://...@primary/db')
        self.replica_dbs = [
            create_engine('postgresql://...@replica1/db'),
            create_engine('postgresql://...@replica2/db'),
        ]
        self.current_replica_index = 0
    
    def get_read_connection(self):
        """読み取り接続を取得（自動フェイルオーバー）"""
        for attempt in range(len(self.replica_dbs)):
            try:
                engine = self.replica_dbs[self.current_replica_index]
                conn = engine.connect()
                # 接続テスト
                conn.execute(text("SELECT 1"))
                return conn
            except Exception as e:
                print(f"Replica {self.current_replica_index} failed: {e}")
                self.current_replica_index = (self.current_replica_index + 1) % len(self.replica_dbs)
        
        # すべてのレプリカが失敗した場合、マスターを使用
        print("All replicas failed, using primary")
        return self.primary_db.connect()
    
    def health_check(self):
        """ヘルスチェック"""
        health_status = {
            'primary': self.check_connection(self.primary_db),
            'replicas': []
        }
        
        for i, replica in enumerate(self.replica_dbs):
            health_status['replicas'].append({
                'index': i,
                'healthy': self.check_connection(replica)
            })
        
        return health_status
    
    def check_connection(self, engine):
        """接続の健全性を確認"""
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except:
            return False
```

## データ保存戦略

### 分散データベースとシャーディング

```python
# シャーディングの実装
class ShardedDatabase:
    """シャーディングされたデータベース"""
    
    def __init__(self, num_shards=4):
        self.shards = []
        for i in range(num_shards):
            engine = create_engine(f'postgresql://...@shard{i}/db')
            self.shards.append(engine)
    
    def get_shard(self, shard_key):
        """シャードキーから適切なシャードを取得"""
        shard_index = hash(shard_key) % len(self.shards)
        return self.shards[shard_index]
    
    def get_user(self, user_id):
        """ユーザーを取得（シャーディング対応）"""
        shard = self.get_shard(user_id)
        Session = sessionmaker(bind=shard)
        session = Session()
        
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

# 水平シャーディングの例
"""
-- ユーザーテーブルをシャード1に
CREATE TABLE users_shard1 (
    CHECK (user_id % 4 = 0)
) INHERITS (users);

-- ユーザーテーブルをシャード2に
CREATE TABLE users_shard2 (
    CHECK (user_id % 4 = 1)
) INHERITS (users);
"""
```

### マルチモデルデータベース

```python
# 異なるデータモデルを組み合わせる
class MultiModelDataStore:
    """マルチモデルデータストア"""
    
    def __init__(self):
        # RDBMS: トランザクションデータ
        self.rdbms = create_engine('postgresql://...')
        
        # NoSQL: ドキュメントストア
        self.mongodb = MongoClient('mongodb://...')
        
        # グラフDB: 関係性データ
        self.neo4j = GraphDatabase.driver("bolt://localhost:7687")
        
        # 時系列DB: メトリクスデータ
        self.influxdb = InfluxDBClient('localhost', 8086, 'admin', 'password', 'metrics')
    
    def store_user(self, user_data):
        """ユーザーを保存（RDBMS）"""
        with self.rdbms.connect() as conn:
            conn.execute(
                text("INSERT INTO users (email, username) VALUES (:email, :username)"),
                user_data
            )
            conn.commit()
    
    def store_user_profile(self, user_id, profile_data):
        """ユーザープロフィールを保存（MongoDB）"""
        db = self.mongodb.myapp
        db.user_profiles.insert_one({
            'user_id': user_id,
            'profile': profile_data
        })
    
    def store_user_relationships(self, user_id, friend_ids):
        """ユーザー関係を保存（Neo4j）"""
        with self.neo4j.session() as session:
            for friend_id in friend_ids:
                session.run(
                    "MATCH (u1:User {id: $user_id}), (u2:User {id: $friend_id}) "
                    "CREATE (u1)-[:FRIENDS_WITH]->(u2)",
                    user_id=user_id, friend_id=friend_id
                )
    
    def store_metrics(self, metric_name, value, tags):
        """メトリクスを保存（InfluxDB）"""
        json_body = [{
            "measurement": metric_name,
            "tags": tags,
            "fields": {"value": value}
        }]
        self.influxdb.write_points(json_body)
```

### CQRSパターン

```python
# Command Query Responsibility Segregation
class CQRSHandler:
    """CQRSパターンの実装"""
    
    def __init__(self):
        # コマンド側（書き込み）
        self.command_db = create_engine('postgresql://...@command/db')
        
        # クエリ側（読み取り）
        self.query_db = create_engine('postgresql://...@query/db')
        
        # イベントストア
        self.event_store = []
    
    def handle_command(self, command):
        """コマンドを処理"""
        # 1. コマンドを検証
        self.validate_command(command)
        
        # 2. イベントを生成
        event = self.create_event(command)
        
        # 3. イベントを保存
        self.event_store.append(event)
        
        # 4. コマンドDBに書き込み
        with self.command_db.connect() as conn:
            self.execute_command(conn, command)
            conn.commit()
        
        # 5. クエリDBを更新（非同期）
        self.update_query_db(event)
    
    def handle_query(self, query):
        """クエリを処理（読み取り専用）"""
        with self.query_db.connect() as conn:
            return self.execute_query(conn, query)
```

## キャッシュ戦略

### マルチレイヤーキャッシュ

```python
# L1: ローカルメモリ、L2: Redis、L3: CDN、L4: データベース
class AdvancedCache:
    """高度なマルチレイヤーキャッシュ"""
    
    def __init__(self):
        self.l1_cache = {}  # アプリケーションメモリ
        self.l2_cache = DistributedCache()  # Redis Cluster
        self.l3_cache = CDNCache()  # CDN
        self.cache_stats = {
            'l1_hits': 0,
            'l2_hits': 0,
            'l3_hits': 0,
            'misses': 0
        }
    
    def get(self, key):
        """マルチレイヤーから取得"""
        # L1
        if key in self.l1_cache:
            self.cache_stats['l1_hits'] += 1
            return self.l1_cache[key]
        
        # L2
        value = self.l2_cache.get(key)
        if value:
            self.cache_stats['l2_hits'] += 1
            self.l1_cache[key] = value
            return value
        
        # L3
        value = self.l3_cache.get(key)
        if value:
            self.cache_stats['l3_hits'] += 1
            self.l2_cache.set(key, value)
            self.l1_cache[key] = value
            return value
        
        self.cache_stats['misses'] += 1
        return None
    
    def get_stats(self):
        """キャッシュ統計を取得"""
        total = sum(self.cache_stats.values())
        if total == 0:
            return {}
        
        return {
            'l1_hit_rate': self.cache_stats['l1_hits'] / total,
            'l2_hit_rate': self.cache_stats['l2_hits'] / total,
            'l3_hit_rate': self.cache_stats['l3_hits'] / total,
            'miss_rate': self.cache_stats['misses'] / total,
        }
```

### キャッシュ無効化戦略

```python
# イベント駆動のキャッシュ無効化
class CacheInvalidation:
    """キャッシュ無効化"""
    
    def __init__(self):
        self.cache = AdvancedCache()
        self.message_queue = MessageQueue()  # Kafka, RabbitMQなど
    
    def invalidate_on_update(self, entity_type, entity_id):
        """更新時にキャッシュを無効化"""
        patterns = [
            f"{entity_type}:{entity_id}",
            f"{entity_type}:{entity_id}:*",
            f"list:{entity_type}:*",  # リストキャッシュも無効化
        ]
        
        for pattern in patterns:
            self.cache.invalidate_pattern(pattern)
        
        # イベントを発行
        self.message_queue.publish('cache_invalidation', {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'patterns': patterns
        })
    
    def subscribe_to_invalidation_events(self):
        """無効化イベントを購読"""
        self.message_queue.subscribe('cache_invalidation', self.handle_invalidation)
    
    def handle_invalidation(self, event):
        """無効化イベントを処理"""
        for pattern in event['patterns']:
            self.cache.invalidate_pattern(pattern)
```

## オーケストレーション

### Kubernetesデプロイメント

```yaml
# kubernetes/postgresql-deployment.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
spec:
  serviceName: postgresql
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:15
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgresql-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgresql-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgresql-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
spec:
  clusterIP: None
  selector:
    app: postgresql
  ports:
  - port: 5432
```

### サービスメッシュ

```yaml
# Istio Service Mesh設定例
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: database-service
spec:
  hosts:
  - database
  http:
  - match:
    - headers:
        x-db-operation:
          exact: read
    route:
    - destination:
        host: database-replica
      weight: 100
  - route:
    - destination:
        host: database-master
      weight: 100
```

### CI/CDパイプライン

```python
# GitHub Actions / GitLab CI の例
# .github/workflows/deploy-db.yml
"""
name: Deploy Database

on:
  push:
    branches: [main]
    paths:
      - 'migrations/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run migrations
        run: |
          alembic upgrade head
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Run tests
        run: |
          pytest tests/
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
"""
```

## 実装例

### 完全な大規模アプリケーション構成

```python
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis.cluster import RedisCluster
import os

app = Flask(__name__)

# マルチリージョン対応
class AppConfig:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.primary_db = create_engine(
            f"postgresql://...@primary-{self.region}/db",
            pool_size=50,
            max_overflow=20
        )
        self.replica_dbs = [
            create_engine(f"postgresql://...@replica-{self.region}-{i}/db")
            for i in range(3)
        ]
        self.redis_cluster = RedisCluster(
            startup_nodes=[
                {"host": f"redis-{self.region}-{i}", "port": "6379"}
                for i in range(3)
            ]
        )

config = AppConfig()

# データベースルーター
db_router = MultiRegionDatabaseRouter()

# キャッシュ
cache = AdvancedCache()

@app.route('/users/<int:user_id>')
def get_user(user_id):
    # キャッシュから取得
    user = cache.get(f"user:{user_id}")
    if user:
        return jsonify(user)
    
    # データベースから取得
    with db_router.get_read_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user_dict = user.to_dict()
            cache.set(f"user:{user_id}", user_dict, ttl=600)
            return jsonify(user_dict)
    
    return jsonify({'error': 'User not found'}), 404
```

## まとめ

### 重要なポイント

1. **マルチリージョン構成**: グローバルな低レイテンシ
2. **高可用性**: マルチAZ、自動フェイルオーバー
3. **分散アーキテクチャ**: シャーディング、CQRS
4. **高度なキャッシュ**: マルチレイヤーキャッシュ戦略
5. **包括的な監視**: パフォーマンス、セキュリティ、コスト

### 次のステップ

- [共通パターンとベストプラクティス](./08_common_patterns.md) - より高度なパターン
- [セキュリティベストプラクティス](./09_security_best_practices.md) - セキュリティの強化

### 推奨ツールとサービス

- **データベース**: AWS RDS Multi-AZ, Google Cloud SQL HA, Azure Database
- **キャッシュ**: Redis Cluster, Memcached, CloudFront
- **オーケストレーション**: Kubernetes, Istio, Terraform
- **監視**: Datadog, New Relic, Prometheus + Grafana
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
- **メッセージキュー**: Kafka, RabbitMQ, AWS SQS

