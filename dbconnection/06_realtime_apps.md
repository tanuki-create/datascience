# リアルタイムアプリケーション向けデータベース接続ベストプラクティス

## 概要

このガイドは、チャットアプリケーション、オンラインゲーム、ライブストリーミング、コラボレーションツールなど、リアルタイム性が重要なアプリケーション向けのデータベース接続とデータ管理のベストプラクティスを提供します。低レイテンシと即座のデータ同期を実現するための戦略に焦点を当てています。

### ターゲットアプリケーション

- チャット・メッセージングアプリ
- オンラインゲーム（マルチプレイヤー）
- ライブストリーミングプラットフォーム
- コラボレーションツール（リアルタイム編集）
- リアルタイムダッシュボード
- IoTデバイス管理システム
- リアルタイム通知システム

## レイテンシ最適化

### WebSocketとデータベース接続の統合

リアルタイムアプリケーションでは、WebSocket接続とデータベース接続を効率的に統合する必要があります。

```python
# WebSocketサーバーとデータベース接続の統合例
import asyncio
import websockets
import asyncpg
from typing import Set

class RealtimeServer:
    def __init__(self):
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.db_pool = None
    
    async def init_db_pool(self):
        """データベース接続プールを初期化"""
        self.db_pool = await asyncpg.create_pool(
            host='localhost',
            database='realtime_app',
            user='postgres',
            password='password',
            min_size=10,
            max_size=50,
            command_timeout=5  # 短いタイムアウトでレイテンシを削減
        )
    
    async def handle_message(self, websocket, message):
        """メッセージを処理し、データベースに保存"""
        try:
            # データベースに非同期で保存
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO messages (user_id, content, created_at) VALUES ($1, $2, NOW())",
                    message['user_id'], message['content']
                )
            
            # すべてのクライアントにブロードキャスト
            await self.broadcast(message)
        except Exception as e:
            print(f"Error: {e}")
    
    async def broadcast(self, message):
        """すべての接続クライアントにメッセージを送信"""
        if self.clients:
            await asyncio.gather(
                *[client.send(str(message)) for client in self.clients],
                return_exceptions=True
            )
```

### インメモリデータベースの活用

頻繁にアクセスされるデータはインメモリデータベースに保持し、レイテンシを最小化します。

```python
# Redisをキャッシュとリアルタイムデータストアとして使用
import redis
import json
import asyncio

class RealtimeDataStore:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )
    
    async def get_user_status(self, user_id: str) -> dict:
        """ユーザーステータスを取得（インメモリから）"""
        status = self.redis_client.get(f"user:status:{user_id}")
        if status:
            return json.loads(status)
        
        # キャッシュミスの場合、PostgreSQLから取得
        # ... PostgreSQLクエリ ...
        return None
    
    async def update_user_status(self, user_id: str, status: dict):
        """ユーザーステータスを更新（インメモリと永続化）"""
        # Redisに即座に保存（低レイテンシ）
        self.redis_client.setex(
            f"user:status:{user_id}",
            3600,  # 1時間のTTL
            json.dumps(status)
        )
        
        # 非同期でPostgreSQLにも保存（永続化）
        # ... バックグラウンドタスクで実行 ...
    
    async def publish_event(self, channel: str, event: dict):
        """リアルタイムイベントを発行"""
        self.redis_client.publish(channel, json.dumps(event))
```

### 接続プールの最適化

リアルタイムアプリケーションでは、接続プールを適切に設定してレイテンシを削減します。

```python
# 非同期接続プールの最適化設定
import asyncpg

async def create_optimized_pool():
    """レイテンシ最適化された接続プール"""
    pool = await asyncpg.create_pool(
        host='localhost',
        database='realtime_app',
        user='postgres',
        password='password',
        min_size=20,  # 最小接続数を増やす
        max_size=100,  # 最大接続数
        max_queries=50000,  # 接続の再利用回数
        max_inactive_connection_lifetime=300,  # 5分で非アクティブ接続を閉じる
        command_timeout=3,  # 3秒でタイムアウト
        server_settings={
            'application_name': 'realtime_app',
            'tcp_keepalives_idle': '30',
            'tcp_keepalives_interval': '10',
            'tcp_keepalives_count': '3'
        }
    )
    return pool
```

## 経済的最適化

### ハイブリッドストレージ戦略

コストを抑えつつパフォーマンスを維持するため、インメモリDBと永続化DBを組み合わせます。

```python
# コスト効率の良いハイブリッドストレージ
class HybridStorage:
    def __init__(self):
        # Redis: ホットデータ（最近アクセスされたデータ）
        self.redis = redis.Redis(host='localhost', port=6379)
        
        # PostgreSQL: コールドデータ（履歴データ）
        self.postgres_pool = None
    
    async def get_message(self, message_id: str):
        """メッセージを取得（ホットデータから優先）"""
        # まずRedisから取得を試みる
        cached = self.redis.get(f"message:{message_id}")
        if cached:
            return json.loads(cached)
        
        # Redisにない場合、PostgreSQLから取得
        async with self.postgres_pool.acquire() as conn:
            message = await conn.fetchrow(
                "SELECT * FROM messages WHERE id = $1", message_id
            )
            
            # 取得したデータをRedisにキャッシュ（30分）
            if message:
                self.redis.setex(
                    f"message:{message_id}",
                    1800,
                    json.dumps(dict(message))
                )
            
            return dict(message) if message else None
    
    async def archive_old_messages(self, days: int = 30):
        """古いメッセージをアーカイブ（コスト削減）"""
        # 30日以上前のメッセージをアーカイブテーブルに移動
        async with self.postgres_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO messages_archive
                SELECT * FROM messages
                WHERE created_at < NOW() - INTERVAL '%s days'
            """, days)
            
            await conn.execute("""
                DELETE FROM messages
                WHERE created_at < NOW() - INTERVAL '%s days'
            """, days)
```

### ストリーミングデータの効率的な保存

リアルタイムデータを効率的に保存し、ストレージコストを削減します。

```python
# 時系列データの効率的な保存（TimescaleDB使用）
import asyncpg

class TimeSeriesStorage:
    async def init_hypertable(self):
        """TimescaleDBのハイパーテーブルを初期化"""
        async with self.pool.acquire() as conn:
            # ハイパーテーブルを作成（自動パーティショニング）
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    time TIMESTAMPTZ NOT NULL,
                    sensor_id TEXT NOT NULL,
                    value DOUBLE PRECISION,
                    PRIMARY KEY (time, sensor_id)
                );
                
                SELECT create_hypertable('sensor_data', 'time',
                    chunk_time_interval => INTERVAL '1 day');
            """)
    
    async def insert_sensor_data(self, sensor_id: str, value: float):
        """センサーデータを効率的に保存"""
        async with self.pool.acquire() as conn:
            # バッチ挿入で効率化
            await conn.execute("""
                INSERT INTO sensor_data (time, sensor_id, value)
                VALUES (NOW(), $1, $2)
            """, sensor_id, value)
    
    async def get_recent_data(self, sensor_id: str, hours: int = 1):
        """最近のデータを取得（自動的に最新チャンクから）"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT time, value
                FROM sensor_data
                WHERE sensor_id = $1
                AND time > NOW() - INTERVAL '%s hours'
                ORDER BY time DESC
            """, sensor_id, hours)
```

### 接続数の最適化

必要最小限の接続数で運用し、コストを削減します。

```python
# 接続数の動的調整
class AdaptiveConnectionPool:
    def __init__(self):
        self.base_min = 10
        self.base_max = 50
        self.current_load = 0
    
    async def adjust_pool_size(self, current_connections: int, active_queries: int):
        """負荷に応じて接続プールサイズを調整"""
        # アクティブなクエリ数に基づいて最適なサイズを計算
        optimal_size = max(
            self.base_min,
            min(self.base_max, active_queries * 2)
        )
        
        if optimal_size != current_connections:
            # プールサイズを調整
            await self.resize_pool(optimal_size)
    
    async def resize_pool(self, new_size: int):
        """プールサイズを変更"""
        # 実装: 接続プールのサイズを動的に変更
        pass
```

## セキュリティ

### リアルタイム接続の認証

WebSocket接続とデータベース接続の両方で適切な認証を実装します。

```python
# WebSocket接続の認証とデータベースアクセス制御
import jwt
import websockets
from datetime import datetime, timedelta

class AuthenticatedRealtimeServer:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.db_pool = None
    
    async def authenticate_websocket(self, websocket, path):
        """WebSocket接続を認証"""
        # クエリパラメータからトークンを取得
        token = self.extract_token_from_path(path)
        
        if not token:
            await websocket.close(code=4001, reason="Authentication required")
            return False
        
        try:
            # JWTトークンを検証
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            websocket.user_id = payload['user_id']
            websocket.role = payload.get('role', 'user')
            return True
        except jwt.InvalidTokenError:
            await websocket.close(code=4003, reason="Invalid token")
            return False
    
    async def handle_database_query(self, websocket, query_type: str, params: dict):
        """認証されたユーザーのデータベースクエリを処理"""
        # ロールベースアクセス制御
        if not self.has_permission(websocket.role, query_type):
            await websocket.send(json.dumps({
                "error": "Permission denied"
            }))
            return
        
        # ユーザーIDをパラメータに追加（行レベルセキュリティ）
        params['user_id'] = websocket.user_id
        
        async with self.db_pool.acquire() as conn:
            # 行レベルセキュリティが有効なクエリを実行
            result = await conn.fetch(
                "SELECT * FROM messages WHERE user_id = $1 AND ...",
                params['user_id']
            )
            
            await websocket.send(json.dumps({
                "data": [dict(row) for row in result]
            }))
```

### メッセージの暗号化

リアルタイムで送信されるメッセージを暗号化します。

```python
# エンドツーエンド暗号化の実装
from cryptography.fernet import Fernet
import base64

class EncryptedMessaging:
    def __init__(self):
        # 各ユーザーごとに異なるキーを生成（実際の実装では安全に管理）
        self.user_keys = {}
    
    def encrypt_message(self, user_id: str, message: str) -> str:
        """メッセージを暗号化"""
        if user_id not in self.user_keys:
            self.user_keys[user_id] = Fernet.generate_key()
        
        fernet = Fernet(self.user_keys[user_id])
        encrypted = fernet.encrypt(message.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_message(self, user_id: str, encrypted_message: str) -> str:
        """メッセージを復号化"""
        fernet = Fernet(self.user_keys[user_id])
        decrypted = fernet.decrypt(base64.b64decode(encrypted_message))
        return decrypted.decode()
    
    async def store_encrypted_message(self, sender_id: str, receiver_id: str, message: str):
        """暗号化されたメッセージをデータベースに保存"""
        encrypted = self.encrypt_message(receiver_id, message)
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO encrypted_messages (sender_id, receiver_id, encrypted_content, created_at)
                VALUES ($1, $2, $3, NOW())
            """, sender_id, receiver_id, encrypted)
```

### レート制限

リアルタイム接続に対するレート制限を実装します。

```python
# Redisを使ったレート制限
import time

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def check_rate_limit(self, user_id: str, action: str, max_requests: int, window: int) -> bool:
        """レート制限をチェック"""
        key = f"ratelimit:{user_id}:{action}"
        current = self.redis.incr(key)
        
        if current == 1:
            # 初回リクエストの場合、TTLを設定
            self.redis.expire(key, window)
        
        if current > max_requests:
            return False
        
        return True
    
    async def handle_realtime_message(self, user_id: str, message: dict):
        """レート制限を考慮したメッセージ処理"""
        # 1分間に最大60メッセージ
        if not await self.check_rate_limit(user_id, "send_message", 60, 60):
            raise Exception("Rate limit exceeded")
        
        # メッセージを処理
        # ...
```

## UX最適化

### オフライン対応と同期

ネットワークが不安定な場合でも、UXを損なわないようにします。

```python
# オフライン対応と自動同期
class OfflineSync:
    def __init__(self):
        self.local_queue = []  # ローカルキュー
        self.sync_in_progress = False
    
    async def send_message_offline_safe(self, message: dict):
        """オフラインでも動作するメッセージ送信"""
        try:
            # まずローカルに保存
            self.local_queue.append({
                'message': message,
                'timestamp': time.time(),
                'synced': False
            })
            
            # サーバーに送信を試みる
            await self.send_to_server(message)
            
            # 成功したらマーク
            self.local_queue[-1]['synced'] = True
        except Exception as e:
            # 失敗した場合、後で再試行
            print(f"Failed to send, will retry: {e}")
            await self.schedule_retry()
    
    async def sync_pending_messages(self):
        """保留中のメッセージを同期"""
        if self.sync_in_progress:
            return
        
        self.sync_in_progress = True
        try:
            unsynced = [m for m in self.local_queue if not m['synced']]
            for msg in unsynced:
                try:
                    await self.send_to_server(msg['message'])
                    msg['synced'] = True
                except Exception as e:
                    print(f"Retry failed: {e}")
        finally:
            self.sync_in_progress = False
```

### 読み取り最適化

リアルタイムデータの読み取りを最適化します。

```python
# 読み取り専用レプリカの活用
class OptimizedReader:
    def __init__(self):
        # 書き込み用プライマリ
        self.write_pool = None
        # 読み取り用レプリカ
        self.read_pool = None
    
    async def get_realtime_data(self, query: str, params: tuple):
        """読み取り専用レプリカからデータを取得"""
        # 読み取りはレプリカから（レイテンシ削減）
        async with self.read_pool.acquire() as conn:
            return await conn.fetch(query, *params)
    
    async def write_realtime_data(self, query: str, params: tuple):
        """書き込みはプライマリに"""
        async with self.write_pool.acquire() as conn:
            return await conn.execute(query, *params)
```

### バッチ処理とストリーミングのバランス

リアルタイム性と効率性のバランスを取ります。

```python
# バッチ処理とストリーミングのハイブリッド
class HybridProcessing:
    def __init__(self):
        self.batch_buffer = []
        self.batch_size = 100
        self.batch_interval = 1.0  # 1秒
    
    async def process_realtime_event(self, event: dict):
        """リアルタイムイベントを処理"""
        # 即座に処理が必要なイベント
        if event.get('priority') == 'high':
            await self.process_immediately(event)
        else:
            # 通常のイベントはバッチ処理
            self.batch_buffer.append(event)
            
            if len(self.batch_buffer) >= self.batch_size:
                await self.process_batch()
    
    async def process_batch(self):
        """バッチを処理"""
        if not self.batch_buffer:
            return
        
        batch = self.batch_buffer.copy()
        self.batch_buffer.clear()
        
        # バッチでデータベースに挿入
        async with self.db_pool.acquire() as conn:
            await conn.executemany(
                "INSERT INTO events (type, data, created_at) VALUES ($1, $2, NOW())",
                [(e['type'], json.dumps(e['data'])) for e in batch]
            )
```

## データ保存戦略

### RDBMS: PostgreSQL + TimescaleDB

時系列データやリアルタイムデータに適したRDBMS戦略。

```python
# TimescaleDBを使った時系列データ管理
class TimeSeriesDB:
    async def setup_hypertable(self):
        """ハイパーテーブルをセットアップ"""
        async with self.pool.acquire() as conn:
            # チャットメッセージ用のハイパーテーブル
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    time TIMESTAMPTZ NOT NULL,
                    room_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    PRIMARY KEY (time, room_id, user_id)
                );
                
                SELECT create_hypertable('chat_messages', 'time',
                    chunk_time_interval => INTERVAL '1 hour');
            """)
    
    async def get_recent_messages(self, room_id: str, limit: int = 100):
        """最近のメッセージを取得"""
        async with self.pool.acquire() as conn:
            return await conn.fetch("""
                SELECT time, user_id, message
                FROM chat_messages
                WHERE room_id = $1
                ORDER BY time DESC
                LIMIT $2
            """, room_id, limit)
```

### NoSQL: MongoDB

柔軟なスキーマが必要なリアルタイムデータに適したNoSQL戦略。

```python
# MongoDBを使ったリアルタイムデータ管理
from pymongo import MongoClient
from pymongo.collection import Collection

class MongoDBRealtime:
    def __init__(self):
        self.client = MongoClient(
            'mongodb://localhost:27017/',
            maxPoolSize=50,
            minPoolSize=10,
            connectTimeoutMS=2000,
            socketTimeoutMS=2000
        )
        self.db = self.client['realtime_app']
    
    async def store_game_state(self, game_id: str, state: dict):
        """ゲーム状態を保存（柔軟なスキーマ）"""
        self.db.game_states.update_one(
            {'game_id': game_id},
            {
                '$set': {
                    'state': state,
                    'updated_at': datetime.utcnow()
                }
            },
            upsert=True
        )
    
    async def get_active_games(self):
        """アクティブなゲームを取得"""
        return list(self.db.game_states.find(
            {'updated_at': {'$gte': datetime.utcnow() - timedelta(minutes=5)}}
        ))
```

### インメモリDB: Redis

超低レイテンシが必要なデータに適したインメモリDB戦略。

```python
# Redisを使った超低レイテンシデータ管理
class RedisRealtime:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1
        )
    
    async def update_presence(self, user_id: str, status: str):
        """ユーザーのオンライン状態を更新"""
        self.redis.setex(
            f"presence:{user_id}",
            60,  # 60秒のTTL
            status
        )
    
    async def get_online_users(self, room_id: str) -> list:
        """オンラインユーザーリストを取得"""
        pattern = f"presence:*"
        keys = self.redis.keys(pattern)
        return [key.split(':')[1] for key in keys if self.redis.get(key) == 'online']
```

## キャッシュ戦略

### 多層キャッシュ

レイテンシを最小化するための多層キャッシュ戦略。

```python
# 多層キャッシュの実装
class MultiLayerCache:
    def __init__(self):
        # L1: アプリケーションメモリ（最速）
        self.memory_cache = {}
        
        # L2: Redis（高速）
        self.redis = redis.Redis(host='localhost', port=6379)
        
        # L3: データベース（永続化）
        self.db_pool = None
    
    async def get_data(self, key: str):
        """多層キャッシュからデータを取得"""
        # L1: メモリキャッシュをチェック
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # L2: Redisをチェック
        cached = self.redis.get(key)
        if cached:
            data = json.loads(cached)
            # メモリキャッシュにも保存
            self.memory_cache[key] = data
            return data
        
        # L3: データベースから取得
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchrow("SELECT * FROM data WHERE key = $1", key)
            if result:
                data = dict(result)
                # 両方のキャッシュに保存
                self.memory_cache[key] = data
                self.redis.setex(key, 3600, json.dumps(data))
                return data
        
        return None
```

### Pub/Subパターン

リアルタイムイベントの配信にPub/Subを使用。

```python
# Redis Pub/Subを使ったリアルタイムイベント配信
class PubSubRealtime:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.pubsub = self.redis.pubsub()
    
    async def publish_event(self, channel: str, event: dict):
        """イベントを発行"""
        self.redis.publish(channel, json.dumps(event))
    
    async def subscribe_channel(self, channel: str, callback):
        """チャンネルを購読"""
        self.pubsub.subscribe(channel)
        
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                await callback(event)
```

## オーケストレーション

### WebSocketサーバーのスケーリング

複数のWebSocketサーバーインスタンスを協調させます。

```python
# 複数インスタンス間でのメッセージ配信
class ScalableWebSocketServer:
    def __init__(self):
        self.instance_id = str(uuid.uuid4())
        self.redis = redis.Redis(host='localhost', port=6379)
        self.local_clients = set()
    
    async def broadcast_to_all_instances(self, message: dict):
        """すべてのインスタンスにメッセージをブロードキャスト"""
        # Redis Pub/Subで他のインスタンスに通知
        self.redis.publish(
            'websocket:broadcast',
            json.dumps({
                'instance_id': self.instance_id,
                'message': message
            })
        )
    
    async def handle_cross_instance_message(self, message: dict):
        """他のインスタンスからのメッセージを処理"""
        if message['instance_id'] != self.instance_id:
            # ローカルのクライアントに配信
            await self.broadcast_to_local_clients(message['message'])
```

### メッセージキューとの統合

非同期処理をメッセージキューで管理します。

```python
# Celeryを使った非同期処理
from celery import Celery

celery_app = Celery('realtime_app', broker='redis://localhost:6379/0')

@celery_app.task
def process_realtime_event(event_data: dict):
    """リアルタイムイベントを非同期で処理"""
    # データベースに保存
    # 通知を送信
    # 分析処理
    pass

# WebSocketハンドラーから使用
async def handle_websocket_message(websocket, message: dict):
    # 即座にクライアントに返信
    await websocket.send(json.dumps({"status": "received"}))
    
    # 重い処理は非同期で実行
    process_realtime_event.delay(message)
```

## 実装例

### 完全なリアルタイムチャットアプリケーション

```python
# 完全なリアルタイムチャットアプリケーションの実装例
import asyncio
import websockets
import asyncpg
import redis
import json
from datetime import datetime

class RealtimeChatApp:
    def __init__(self):
        self.db_pool = None
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.clients = {}  # {room_id: {websocket: user_id}}
    
    async def init_database(self):
        """データベースを初期化"""
        self.db_pool = await asyncpg.create_pool(
            host='localhost',
            database='chat_app',
            user='postgres',
            password='password',
            min_size=10,
            max_size=50
        )
        
        # テーブルを作成
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    room_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                
                CREATE INDEX idx_messages_room_created ON messages(room_id, created_at DESC);
            """)
    
    async def handle_client(self, websocket, path):
        """クライアント接続を処理"""
        # 認証とルーム参加
        room_id, user_id = await self.authenticate_and_join(websocket, path)
        
        if not room_id or not user_id:
            await websocket.close()
            return
        
        try:
            # 既存のメッセージを送信
            await self.send_recent_messages(websocket, room_id)
            
            # メッセージを受信
            async for message in websocket:
                await self.handle_message(websocket, room_id, user_id, message)
        finally:
            await self.leave_room(websocket, room_id)
    
    async def handle_message(self, websocket, room_id: str, user_id: str, message: str):
        """メッセージを処理"""
        try:
            data = json.loads(message)
            content = data.get('content', '')
            
            # データベースに保存
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO messages (room_id, user_id, content)
                    VALUES ($1, $2, $3)
                """, room_id, user_id, content)
            
            # すべてのクライアントにブロードキャスト
            await self.broadcast_to_room(room_id, {
                'type': 'message',
                'user_id': user_id,
                'content': content,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        """ルーム内のすべてのクライアントにメッセージを送信"""
        if room_id in self.clients:
            disconnected = []
            for client, _ in self.clients[room_id].items():
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
            
            # 切断されたクライアントを削除
            for client in disconnected:
                del self.clients[room_id][client]

# サーバー起動
async def main():
    app = RealtimeChatApp()
    await app.init_database()
    
    async with websockets.serve(app.handle_client, "localhost", 8765):
        await asyncio.Future()  # 永続的に実行

if __name__ == "__main__":
    asyncio.run(main())
```

## まとめ

リアルタイムアプリケーション向けのデータベース接続ベストプラクティスの重要なポイント：

### レイテンシ最適化
- WebSocketとデータベース接続の効率的な統合
- インメモリデータベース（Redis）の活用
- 接続プールの最適化（適切なサイズとタイムアウト設定）

### 経済的最適化
- ハイブリッドストレージ戦略（ホットデータはRedis、コールドデータはPostgreSQL）
- 時系列データベース（TimescaleDB）の活用
- 接続数の動的調整

### セキュリティ
- WebSocket接続の認証（JWT）
- メッセージのエンドツーエンド暗号化
- レート制限の実装

### UX最適化
- オフライン対応と自動同期
- 読み取り専用レプリカの活用
- バッチ処理とストリーミングのバランス

### データ保存戦略
- **RDBMS**: PostgreSQL + TimescaleDB（時系列データ）
- **NoSQL**: MongoDB（柔軟なスキーマ）
- **インメモリDB**: Redis（超低レイテンシ）

### キャッシュ戦略
- 多層キャッシュ（メモリ → Redis → データベース）
- Pub/Subパターンによるリアルタイムイベント配信

### オーケストレーション
- 複数WebSocketサーバーインスタンスの協調
- メッセージキュー（Celery）との統合

リアルタイムアプリケーションでは、レイテンシの最小化が最優先事項です。適切なデータベース選択、キャッシュ戦略、接続管理により、優れたユーザー体験を提供できます。



