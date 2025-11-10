# マイクロサービスアーキテクチャ向けデータベース接続ベストプラクティス

## 概要

このガイドは、マイクロサービスベースのアプリケーション向けのデータベース接続とデータ管理のベストプラクティスを提供します。サービス間通信、データ分離、一貫性保証に焦点を当てています。

### ターゲットアプリケーション

- マイクロサービスアーキテクチャ
- 分散システム
- サービス指向アーキテクチャ（SOA）
- ドメイン駆動設計（DDD）
- イベント駆動アーキテクチャ

## レイテンシ最適化

### サービス間通信の最適化

```python
# サービス間の直接データベースアクセスを避ける
# API Gateway経由での通信

from flask import Flask
import requests
import time

class ServiceClient:
    """他のマイクロサービスへのクライアント"""
    
    def __init__(self, service_name, base_url):
        self.service_name = service_name
        self.base_url = base_url
        self.session = requests.Session()
        # 接続プールの設定
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def get(self, endpoint, timeout=5):
        """GETリクエスト"""
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Service {self.service_name} error: {e}")
            raise
    
    def post(self, endpoint, data, timeout=5):
        """POSTリクエスト"""
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Service {self.service_name} error: {e}")
            raise

# 使用例
user_service = ServiceClient("user-service", "http://user-service:8000")
order_service = ServiceClient("order-service", "http://order-service:8001")

# ユーザー情報を取得
user = user_service.get(f"/users/{user_id}")

# 注文を作成
order = order_service.post("/orders", {
    "user_id": user_id,
    "items": items
})
```

### データベース分離

```python
# Database per Service パターン
# 各サービスが独自のデータベースを持つ

# User Service
class UserService:
    def __init__(self):
        self.db = create_engine('postgresql://...@user-db/userdb')
        self.session_factory = sessionmaker(bind=self.db)
    
    def get_user(self, user_id):
        session = self.session_factory()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

# Order Service
class OrderService:
    def __init__(self):
        self.db = create_engine('postgresql://...@order-db/orderdb')
        self.session_factory = sessionmaker(bind=self.db)
    
    def create_order(self, user_id, items):
        session = self.session_factory()
        try:
            order = Order(user_id=user_id, items=items)
            session.add(order)
            session.commit()
            return order
        finally:
            session.close()
```

### 接続プールの最適化

```python
# サービスごとの接続プール設定
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

class ServiceDatabase:
    """サービス専用のデータベース接続"""
    
    def __init__(self, connection_string, service_name):
        self.service_name = service_name
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=10,  # サービスごとに適切なサイズ
            max_overflow=5,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
            connect_args={
                "application_name": service_name
            }
        )
    
    def get_session(self):
        """セッションを取得"""
        Session = sessionmaker(bind=self.engine)
        return Session()
```

## 経済的最適化

### サービスごとの最適なDB選択

```python
# サービスごとに最適なデータベースを選択

# User Service - PostgreSQL（リレーショナルデータ）
class UserServiceDB:
    def __init__(self):
        self.db = create_engine('postgresql://...@user-db/userdb')

# Product Service - MongoDB（柔軟なスキーマ）
class ProductServiceDB:
    def __init__(self):
        self.client = MongoClient('mongodb://product-db:27017/')
        self.db = self.client.productdb

# Cart Service - Redis（高速な読み書き）
class CartServiceDB:
    def __init__(self):
        self.redis = redis.Redis(host='cart-db', port=6379, db=0)

# Analytics Service - InfluxDB（時系列データ）
class AnalyticsServiceDB:
    def __init__(self):
        self.client = InfluxDBClient(
            host='analytics-db',
            port=8086,
            database='analytics'
        )
```

### リソース共有の最適化

```yaml
# Kubernetes Resource Limits
# サービスごとに適切なリソース制限を設定

apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  template:
    spec:
      containers:
      - name: user-service
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: DB_POOL_SIZE
          value: "10"  # リソースに応じたプールサイズ
```

## セキュリティ

### サービス間認証

```python
# mTLS (Mutual TLS) によるサービス間認証
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class SecureServiceClient:
    """セキュアなサービス間通信"""
    
    def __init__(self, service_name, base_url, cert_path, key_path, ca_path):
        self.service_name = service_name
        self.base_url = base_url
        
        # mTLS設定
        self.session = requests.Session()
        adapter = HTTPAdapter()
        
        # SSLコンテキストの設定
        context = create_urllib3_context()
        context.load_cert_chain(cert_path, key_path)
        context.load_verify_locations(ca_path)
        
        self.session.mount('https://', adapter)
        self.session.cert = (cert_path, key_path)
        self.session.verify = ca_path
    
    def get(self, endpoint):
        """セキュアなGETリクエスト"""
        response = self.session.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

# JWT トークンによる認証
import jwt
from datetime import datetime, timedelta

class ServiceAuth:
    """サービス間認証"""
    
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def generate_token(self, service_name, audience):
        """サービス間トークンを生成"""
        payload = {
            'service': service_name,
            'aud': audience,
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token, audience):
        """トークンを検証"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256'],
                audience=audience
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

# 使用例
auth = ServiceAuth("secret-key")
token = auth.generate_token("user-service", "order-service")

headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://order-service:8001/orders",
    headers=headers
)
```

### ネットワーク分離

```yaml
# Kubernetes NetworkPolicy
# サービス間の通信を制限

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: user-service-policy
spec:
  podSelector:
    matchLabels:
      app: user-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: user-db
    ports:
    - protocol: TCP
      port: 5432
```

## UX最適化

### 集約されたAPI

```python
# API Gateway パターン
# 複数のサービスを集約して単一のAPIを提供

from flask import Flask, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

class APIGateway:
    """API Gateway"""
    
    def __init__(self):
        self.services = {
            'user': 'http://user-service:8000',
            'order': 'http://order-service:8001',
            'product': 'http://product-service:8002',
        }
    
    async def fetch_user_order(self, user_id):
        """ユーザーと注文を並列で取得"""
        async with aiohttp.ClientSession() as session:
            # 並列でリクエスト
            user_task = session.get(f"{self.services['user']}/users/{user_id}")
            order_task = session.get(f"{self.services['order']}/users/{user_id}/orders")
            
            user_response, order_response = await asyncio.gather(
                user_task, order_task
            )
            
            user_data = await user_response.json()
            order_data = await order_response.json()
            
            return {
                'user': user_data,
                'orders': order_data
            }

gateway = APIGateway()

@app.route('/api/users/<int:user_id>/dashboard')
async def get_user_dashboard(user_id):
    """ユーザーダッシュボード（複数サービスからデータを集約）"""
    data = await gateway.fetch_user_order(user_id)
    return jsonify(data)
```

### 一貫性保証

```python
# Saga パターンによる分散トランザクション
class OrderSaga:
    """注文作成のSaga"""
    
    def __init__(self):
        self.user_service = ServiceClient("user-service", "http://user-service:8000")
        self.inventory_service = ServiceClient("inventory-service", "http://inventory-service:8002")
        self.payment_service = ServiceClient("payment-service", "http://payment-service:8003")
        self.order_service = ServiceClient("order-service", "http://order-service:8001")
    
    def create_order(self, user_id, items):
        """注文を作成（Sagaパターン）"""
        saga_steps = []
        
        try:
            # Step 1: 在庫を確保
            inventory_result = self.inventory_service.post(
                "/inventory/reserve",
                {"items": items}
            )
            saga_steps.append(('inventory', inventory_result['reservation_id']))
            
            # Step 2: 支払いを処理
            payment_result = self.payment_service.post(
                "/payments/charge",
                {"user_id": user_id, "amount": inventory_result['total']}
            )
            saga_steps.append(('payment', payment_result['payment_id']))
            
            # Step 3: 注文を作成
            order_result = self.order_service.post(
                "/orders",
                {
                    "user_id": user_id,
                    "items": items,
                    "payment_id": payment_result['payment_id']
                }
            )
            saga_steps.append(('order', order_result['order_id']))
            
            return order_result
            
        except Exception as e:
            # 補償トランザクション（ロールバック）
            self.compensate(saga_steps)
            raise e
    
    def compensate(self, saga_steps):
        """補償トランザクション"""
        # 逆順でロールバック
        for step_type, step_id in reversed(saga_steps):
            try:
                if step_type == 'order':
                    self.order_service.delete(f"/orders/{step_id}")
                elif step_type == 'payment':
                    self.payment_service.post(f"/payments/{step_id}/refund", {})
                elif step_type == 'inventory':
                    self.inventory_service.post(f"/inventory/{step_id}/release", {})
            except Exception as e:
                print(f"Compensation failed for {step_type}: {e}")
```

## データ保存戦略

### Database per Service パターン

```python
# 各サービスが独自のデータベースを持つ

# User Service Database
class UserDB:
    def __init__(self):
        self.engine = create_engine('postgresql://...@user-db/userdb')
    
    def create_user(self, email, username):
        session = self.get_session()
        try:
            user = User(email=email, username=username)
            session.add(user)
            session.commit()
            return user
        finally:
            session.close()

# Order Service Database
class OrderDB:
    def __init__(self):
        self.engine = create_engine('postgresql://...@order-db/orderdb')
    
    def create_order(self, user_id, items):
        session = self.get_session()
        try:
            order = Order(user_id=user_id, items=items)
            session.add(order)
            session.commit()
            return order
        finally:
            session.close()
```

### CQRSパターン

```python
# Command Query Responsibility Segregation

# Command Side (書き込み)
class OrderCommandService:
    def __init__(self):
        self.command_db = create_engine('postgresql://...@order-command-db/orderdb')
        self.event_bus = EventBus()
    
    def create_order(self, user_id, items):
        """注文を作成（コマンド）"""
        session = self.get_session()
        try:
            order = Order(user_id=user_id, items=items, status='pending')
            session.add(order)
            session.commit()
            
            # イベントを発行
            self.event_bus.publish('order.created', {
                'order_id': order.id,
                'user_id': user_id,
                'items': items
            })
            
            return order
        finally:
            session.close()

# Query Side (読み取り)
class OrderQueryService:
    def __init__(self):
        self.query_db = create_engine('postgresql://...@order-query-db/orderdb')
    
    def get_user_orders(self, user_id):
        """ユーザーの注文を取得（クエリ）"""
        session = self.get_session()
        try:
            return session.query(Order).filter_by(user_id=user_id).all()
        finally:
            session.close()
    
    def get_order_stats(self):
        """注文統計を取得（読み取り最適化されたビュー）"""
        session = self.get_session()
        try:
            return session.query(OrderStats).first()
        finally:
            session.close()
```

### イベントソーシング

```python
# イベントストア
class EventStore:
    def __init__(self):
        self.db = create_engine('postgresql://...@event-store/eventsdb')
    
    def append_event(self, aggregate_id, event_type, event_data):
        """イベントを追加"""
        session = self.get_session()
        try:
            event = Event(
                aggregate_id=aggregate_id,
                event_type=event_type,
                event_data=event_data,
                timestamp=datetime.utcnow()
            )
            session.add(event)
            session.commit()
            return event
        finally:
            session.close()
    
    def get_events(self, aggregate_id):
        """集約のイベントを取得"""
        session = self.get_session()
        try:
            return session.query(Event).filter_by(
                aggregate_id=aggregate_id
            ).order_by(Event.sequence_number).all()
        finally:
            session.close()

# イベントハンドラー
class OrderEventHandler:
    def __init__(self):
        self.event_store = EventStore()
        self.order_query_db = create_engine('postgresql://...@order-query-db/orderdb')
    
    def handle_order_created(self, event):
        """注文作成イベントを処理"""
        # クエリDBを更新
        session = self.get_session()
        try:
            order_view = OrderView(
                order_id=event['order_id'],
                user_id=event['user_id'],
                status='pending',
                created_at=datetime.utcnow()
            )
            session.add(order_view)
            session.commit()
        finally:
            session.close()
    
    def handle_order_updated(self, event):
        """注文更新イベントを処理"""
        session = self.get_session()
        try:
            order_view = session.query(OrderView).filter_by(
                order_id=event['order_id']
            ).first()
            if order_view:
                order_view.status = event['status']
                order_view.updated_at = datetime.utcnow()
                session.commit()
        finally:
            session.close()
```

## キャッシュ戦略

### 分散キャッシュ

```python
# Redis Cluster による分散キャッシュ
from redis.cluster import RedisCluster

class DistributedCache:
    def __init__(self):
        startup_nodes = [
            {"host": "redis-node-1", "port": "6379"},
            {"host": "redis-node-2", "port": "6379"},
            {"host": "redis-node-3", "port": "6379"},
        ]
        self.client = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=True
        )
    
    def get(self, key):
        return self.client.get(key)
    
    def set(self, key, value, ttl=300):
        self.client.setex(key, ttl, value)
    
    def invalidate_pattern(self, pattern):
        keys = []
        for node in self.client.get_nodes():
            keys.extend(node.keys(pattern))
        if keys:
            self.client.delete(*keys)

# サービスごとのキャッシュキー命名規則
class CacheKeyBuilder:
    @staticmethod
    def user_key(user_id):
        return f"user-service:user:{user_id}"
    
    @staticmethod
    def order_key(order_id):
        return f"order-service:order:{order_id}"
    
    @staticmethod
    def user_orders_key(user_id):
        return f"order-service:user:{user_id}:orders"
```

### イベント駆動のキャッシュ無効化

```python
# イベントバス経由でのキャッシュ無効化
class CacheInvalidationHandler:
    def __init__(self, cache, event_bus):
        self.cache = cache
        self.event_bus = event_bus
        self.event_bus.subscribe('user.updated', self.handle_user_updated)
        self.event_bus.subscribe('order.created', self.handle_order_created)
    
    def handle_user_updated(self, event):
        """ユーザー更新時にキャッシュを無効化"""
        user_id = event['user_id']
        self.cache.invalidate_pattern(f"user-service:user:{user_id}*")
    
    def handle_order_created(self, event):
        """注文作成時にユーザーの注文リストキャッシュを無効化"""
        user_id = event['user_id']
        self.cache.delete(f"order-service:user:{user_id}:orders")
```

## オーケストレーション

### サービスメッシュ

```yaml
# Istio Service Mesh 設定
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        x-db-operation:
          exact: read
    route:
    - destination:
        host: user-service
        subset: read-replica
      weight: 100
  - route:
    - destination:
        host: user-service
        subset: primary
      weight: 100
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  subsets:
  - name: primary
    labels:
      version: v1
      role: primary
  - name: read-replica
    labels:
      version: v1
      role: replica
```

### API Gateway

```python
# Kong / AWS API Gateway / Ambassador
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

class APIGateway:
    def __init__(self):
        self.services = {
            '/users': 'http://user-service:8000',
            '/orders': 'http://order-service:8001',
            '/products': 'http://product-service:8002',
        }
    
    def route_request(self, path, method, data=None):
        """リクエストを適切なサービスにルーティング"""
        # サービスを特定
        service_url = None
        for prefix, url in self.services.items():
            if path.startswith(prefix):
                service_url = url
                break
        
        if not service_url:
            return {'error': 'Service not found'}, 404
        
        # リクエストを転送
        url = f"{service_url}{path}"
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        return response.json(), response.status_code

gateway = APIGateway()

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """すべてのリクエストをプロキシ"""
    data = request.get_json() if request.is_json else None
    return gateway.route_request(f"/{path}", request.method, data)
```

### イベント駆動アーキテクチャ

```python
# Kafka / RabbitMQ / AWS EventBridge
from kafka import KafkaProducer, KafkaConsumer
import json

class EventBus:
    def __init__(self, bootstrap_servers=['kafka:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumers = {}
    
    def publish(self, topic, event):
        """イベントを発行"""
        self.producer.send(topic, event)
        self.producer.flush()
    
    def subscribe(self, topic, handler):
        """イベントを購読"""
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='microservices'
        )
        
        def consume():
            for message in consumer:
                handler(message.value)
        
        import threading
        thread = threading.Thread(target=consume, daemon=True)
        thread.start()
        self.consumers[topic] = consumer

# 使用例
event_bus = EventBus()

# イベントを発行
event_bus.publish('order.created', {
    'order_id': 123,
    'user_id': 456,
    'items': [...]
})

# イベントを購読
def handle_order_created(event):
    print(f"Order created: {event}")

event_bus.subscribe('order.created', handle_order_created)
```

## 実装例

### 完全なマイクロサービス構成

```python
# User Service の完全な実装例
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

app = Flask(__name__)

class UserService:
    def __init__(self):
        # データベース接続
        self.db = create_engine('postgresql://...@user-db/userdb')
        self.Session = sessionmaker(bind=self.db)
        
        # キャッシュ
        self.cache = redis.Redis(host='redis', port=6379, db=0)
        
        # イベントバス
        self.event_bus = EventBus()
        self.event_bus.subscribe('user.updated', self.handle_user_updated_event)
    
    def get_user(self, user_id):
        """ユーザーを取得"""
        # キャッシュから取得
        cache_key = f"user:{user_id}"
        cached = self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # データベースから取得
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user_dict = user.to_dict()
                # キャッシュに保存
                self.cache.setex(cache_key, 300, json.dumps(user_dict))
                return user_dict
            return None
        finally:
            session.close()
    
    def update_user(self, user_id, data):
        """ユーザーを更新"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user.update_from_dict(data)
                session.commit()
                
                # キャッシュを無効化
                self.cache.delete(f"user:{user_id}")
                
                # イベントを発行
                self.event_bus.publish('user.updated', {
                    'user_id': user_id,
                    'changes': data
                })
                
                return user.to_dict()
            return None
        finally:
            session.close()
    
    def handle_user_updated_event(self, event):
        """ユーザー更新イベントを処理（他のサービスからの通知）"""
        user_id = event['user_id']
        # ローカルキャッシュを無効化
        self.cache.delete(f"user:{user_id}")

user_service = UserService()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = user_service.update_user(user_id, data)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## まとめ

### 重要なポイント

1. **Database per Service**: 各サービスが独自のデータベースを持つ
2. **サービス間通信**: API経由で通信、直接DBアクセスを避ける
3. **イベント駆動**: イベントバスによる疎結合
4. **CQRS**: コマンドとクエリの分離
5. **分散トランザクション**: Sagaパターンによる一貫性保証

### 次のステップ

- [リアルタイムアプリケーション](./06_realtime_apps.md) - リアルタイム同期が必要な場合
- [共通パターンとベストプラクティス](./08_common_patterns.md) - より高度なパターン
- [セキュリティベストプラクティス](./09_security_best_practices.md) - セキュリティの強化

### 推奨ツールとサービス

- **サービスメッシュ**: Istio, Linkerd, Consul Connect
- **API Gateway**: Kong, AWS API Gateway, Ambassador
- **メッセージキュー**: Kafka, RabbitMQ, AWS SQS, NATS
- **サービスディスカバリ**: Consul, Eureka, Kubernetes Service
- **分散トレーシング**: Jaeger, Zipkin, AWS X-Ray
- **監視**: Prometheus, Grafana, Datadog

