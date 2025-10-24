# Chapter 8: Metaclasses and Attributes

メタクラスと属性のベストプラクティスを学びます。

## 目次

1. [__new__でオブジェクトの構築を制御する](#1-__new__でオブジェクトの構築を制御する)
2. [__init_subclass__でサブクラスを検証する](#2-__init_subclass__でサブクラスを検証する)
3. [__set_name__でメタクラスを避ける](#3-__set_name__でメタクラスを避ける)
4. [__prepare__で名前空間を事前に準備する](#4-__prepare__で名前空間を事前に準備する)
5. [__getattr__、__getattribute__、__setattr__の違いを理解する](#5-__getattr__、__getattribute__、__setattr__の違いを理解する)
6. [__slots__でメモリ使用量を削減する](#6-__slots__でメモリ使用量を削減する)
7. [デスクリプタで再利用可能なプロパティロジックを作成する](#7-デスクリプタで再利用可能なプロパティロジックを作成する)
8. [プロパティで単純な属性アクセスを置き換える](#8-プロパティで単純な属性アクセスを置き換える)
9. [プロパティでリファクタリングを容易にする](#9-プロパティでリファクタリングを容易にする)
10. [メタクラスでクラスの動作を制御する](#10-メタクラスでクラスの動作を制御する)

---

## 1. __new__でオブジェクトの構築を制御する

### 基本概念

`__new__`メソッドは、オブジェクトのインスタンス化プロセスを制御できます。シングルトンパターンや不変オブジェクトの作成に役立ちます。

### 具体例

#### 例1: シングルトンパターン

```python
# シングルトンパターンの実装
class Singleton:
    """シングルトンクラス"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.value = 0
    
    def set_value(self, value):
        """値を設定"""
        self.value = value
    
    def get_value(self):
        """値を取得"""
        return self.value

# 使用例
print("=== シングルトンパターン ===")
singleton1 = Singleton()
singleton1.set_value(42)

singleton2 = Singleton()
print(f"Singleton 1: {singleton1.get_value()}")
print(f"Singleton 2: {singleton2.get_value()}")
print(f"同じインスタンス: {singleton1 is singleton2}")

# 設定クラスでのシングルトン
class Config:
    """設定クラス（シングルトン）"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.settings = {}
    
    def set_setting(self, key, value):
        """設定を追加"""
        self.settings[key] = value
    
    def get_setting(self, key, default=None):
        """設定を取得"""
        return self.settings.get(key, default)

# 使用例
config1 = Config()
config1.set_setting('debug', True)
config1.set_setting('log_level', 'INFO')

config2 = Config()
print(f"\n=== 設定クラス ===")
print(f"Config 1 debug: {config1.get_setting('debug')}")
print(f"Config 2 debug: {config2.get_setting('debug')}")
print(f"同じインスタンス: {config1 is config2}")
```

#### 例2: 不変オブジェクトの作成

```python
# 不変オブジェクトの作成
class ImmutablePoint:
    """不変な点クラス"""
    
    def __new__(cls, x, y):
        # 既存のインスタンスをチェック
        for instance in cls._instances:
            if instance.x == x and instance.y == y:
                return instance
        
        # 新しいインスタンスを作成
        instance = super().__new__(cls)
        instance._x = x
        instance._y = y
        cls._instances.add(instance)
        return instance
    
    def __init__(self, x, y):
        # 既に初期化済みの場合はスキップ
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __repr__(self):
        return f"ImmutablePoint({self.x}, {self.y})"
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return isinstance(other, ImmutablePoint) and self.x == other.x and self.y == other.y

# クラス変数を初期化
ImmutablePoint._instances = set()

# 使用例
print("=== 不変オブジェクト ===")
point1 = ImmutablePoint(1, 2)
point2 = ImmutablePoint(1, 2)
point3 = ImmutablePoint(3, 4)

print(f"Point 1: {point1}")
print(f"Point 2: {point2}")
print(f"Point 3: {point3}")
print(f"Point 1 is Point 2: {point1 is point2}")
print(f"Point 1 == Point 2: {point1 == point2}")
print(f"Point 1 is Point 3: {point1 is point3}")
```

#### 例3: オブジェクトプール

```python
# オブジェクトプールの実装
class ConnectionPool:
    """接続プールクラス"""
    
    def __new__(cls, max_connections=10):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, max_connections=10):
        if hasattr(self, 'initialized'):
            return
        
        self.initialized = True
        self.max_connections = max_connections
        self.connections = []
        self.available_connections = []
    
    def get_connection(self):
        """接続を取得"""
        if self.available_connections:
            return self.available_connections.pop()
        
        if len(self.connections) < self.max_connections:
            connection = f"Connection-{len(self.connections) + 1}"
            self.connections.append(connection)
            return connection
        
        raise RuntimeError("接続プールが満杯です")
    
    def return_connection(self, connection):
        """接続を返却"""
        if connection in self.connections:
            self.available_connections.append(connection)
    
    def get_stats(self):
        """統計を取得"""
        return {
            'total_connections': len(self.connections),
            'available_connections': len(self.available_connections),
            'max_connections': self.max_connections
        }

# 使用例
print("=== オブジェクトプール ===")
pool1 = ConnectionPool(5)
pool2 = ConnectionPool(5)

print(f"Pool 1 is Pool 2: {pool1 is pool2}")

# 接続を取得
conn1 = pool1.get_connection()
conn2 = pool1.get_connection()
print(f"接続1: {conn1}")
print(f"接続2: {conn2}")
print(f"統計: {pool1.get_stats()}")

# 接続を返却
pool1.return_connection(conn1)
print(f"返却後の統計: {pool1.get_stats()}")
```

### よくある間違い

1. **__init__との混同**: `__new__`と`__init__`の役割を理解しない
2. **不適切な使用**: シンプルなケースで`__new__`を過度に使用
3. **メモリリーク**: 適切なクリーンアップを行わない

### 応用例

```python
# データベース接続管理での__new__活用
class DatabaseConnection:
    """データベース接続クラス"""
    _instances = {}
    
    def __new__(cls, connection_string):
        if connection_string not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[connection_string] = instance
        return cls._instances[connection_string]
    
    def __init__(self, connection_string):
        if hasattr(self, 'connection_string'):
            return
        
        self.connection_string = connection_string
        self.is_connected = False
        self.connection_count = 0
    
    def connect(self):
        """接続"""
        if not self.is_connected:
            self.is_connected = True
            self.connection_count += 1
            print(f"データベースに接続: {self.connection_string}")
    
    def disconnect(self):
        """切断"""
        if self.is_connected:
            self.is_connected = False
            print(f"データベースから切断: {self.connection_string}")
    
    def get_stats(self):
        """統計を取得"""
        return {
            'connection_string': self.connection_string,
            'is_connected': self.is_connected,
            'connection_count': self.connection_count
        }

# 使用例
print("=== データベース接続管理 ===")
db1 = DatabaseConnection("postgresql://localhost:5432/db1")
db2 = DatabaseConnection("postgresql://localhost:5432/db1")
db3 = DatabaseConnection("postgresql://localhost:5432/db2")

print(f"DB1 is DB2: {db1 is db2}")
print(f"DB1 is DB3: {db1 is db3}")

db1.connect()
print(f"DB1統計: {db1.get_stats()}")
print(f"DB2統計: {db2.get_stats()}")

db1.disconnect()
print(f"切断後DB1統計: {db1.get_stats()}")
```

### ベストプラクティス

- `__new__`は適切なケースでのみ使用する
- シングルトンパターンやオブジェクトプールに活用する
- メモリ管理を適切に行う
- `__init__`との違いを理解する

---

## 2. __init_subclass__でサブクラスを検証する

### 基本概念

`__init_subclass__`メソッドを使用することで、サブクラスの作成時に検証や設定を行うことができます。メタクラスよりもシンプルで理解しやすい方法です。

### 具体例

#### 例1: サブクラスの検証

```python
# サブクラスの検証
class BaseModel:
    """ベースモデルクラス"""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # 必須メソッドの存在をチェック
        required_methods = ['validate', 'save']
        for method in required_methods:
            if not hasattr(cls, method):
                raise TypeError(f"{cls.__name__} must implement {method} method")
        
        # 必須属性の存在をチェック
        if not hasattr(cls, 'table_name'):
            raise TypeError(f"{cls.__name__} must define table_name attribute")
        
        print(f"サブクラス {cls.__name__} が正常に作成されました")

class User(BaseModel):
    """ユーザークラス"""
    table_name = 'users'
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def validate(self):
        """バリデーション"""
        if not self.name:
            raise ValueError("名前は必須です")
        if not self.email or '@' not in self.email:
            raise ValueError("有効なメールアドレスを入力してください")
        return True
    
    def save(self):
        """保存"""
        if self.validate():
            print(f"ユーザー {self.name} を保存しました")
            return True
        return False

# 使用例
print("=== サブクラスの検証 ===")
user = User("Alice", "alice@example.com")
user.save()

# エラーケース
try:
    class InvalidModel(BaseModel):
        pass
except TypeError as e:
    print(f"エラー: {e}")
```

#### 例2: 設定の自動適用

```python
# 設定の自動適用
class ConfigurableBase:
    """設定可能なベースクラス"""
    
    def __init_subclass__(cls, config=None, **kwargs):
        super().__init_subclass__(**kwargs)
        
        if config:
            # 設定をクラス属性に適用
            for key, value in config.items():
                setattr(cls, key, value)
        
        # デフォルト設定を適用
        if not hasattr(cls, 'debug'):
            cls.debug = False
        if not hasattr(cls, 'log_level'):
            cls.log_level = 'INFO'
        
        print(f"クラス {cls.__name__} に設定を適用しました")

class APIClient(ConfigurableBase, config={'timeout': 30, 'retries': 3}):
    """APIクライアントクラス"""
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_config(self):
        """設定を取得"""
        return {
            'timeout': self.timeout,
            'retries': self.retries,
            'debug': self.debug,
            'log_level': self.log_level
        }

class DatabaseClient(ConfigurableBase, config={'pool_size': 10, 'timeout': 60}):
    """データベースクライアントクラス"""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def get_config(self):
        """設定を取得"""
        return {
            'pool_size': self.pool_size,
            'timeout': self.timeout,
            'debug': self.debug,
            'log_level': self.log_level
        }

# 使用例
print("\n=== 設定の自動適用 ===")
api_client = APIClient("https://api.example.com")
print(f"API設定: {api_client.get_config()}")

db_client = DatabaseClient("postgresql://localhost:5432/mydb")
print(f"DB設定: {db_client.get_config()}")
```

#### 例3: プラグインシステム

```python
# プラグインシステム
class PluginBase:
    """プラグインベースクラス"""
    _plugins = {}
    
    def __init_subclass__(cls, plugin_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # プラグイン名を設定
        if plugin_name:
            cls.plugin_name = plugin_name
        else:
            cls.plugin_name = cls.__name__.lower()
        
        # プラグインを登録
        cls._plugins[cls.plugin_name] = cls
        
        # 必須メソッドの存在をチェック
        if not hasattr(cls, 'execute'):
            raise TypeError(f"Plugin {cls.plugin_name} must implement execute method")
        
        print(f"プラグイン {cls.plugin_name} を登録しました")
    
    @classmethod
    def get_plugin(cls, name):
        """プラグインを取得"""
        return cls._plugins.get(name)
    
    @classmethod
    def list_plugins(cls):
        """プラグイン一覧を取得"""
        return list(cls._plugins.keys())

class EmailPlugin(PluginBase, plugin_name='email'):
    """メールプラグイン"""
    
    def execute(self, data):
        """実行"""
        print(f"メール送信: {data}")

class SMSSPlugin(PluginBase, plugin_name='sms'):
    """SMSプラグイン"""
    
    def execute(self, data):
        """実行"""
        print(f"SMS送信: {data}")

class NotificationPlugin(PluginBase, plugin_name='notification'):
    """通知プラグイン"""
    
    def execute(self, data):
        """実行"""
        print(f"通知送信: {data}")

# 使用例
print("\n=== プラグインシステム ===")
print(f"登録されたプラグイン: {PluginBase.list_plugins()}")

# プラグインを取得して実行
email_plugin = PluginBase.get_plugin('email')
if email_plugin:
    email_plugin().execute("Hello World")

sms_plugin = PluginBase.get_plugin('sms')
if sms_plugin:
    sms_plugin().execute("Hello World")
```

### よくある間違い

1. **メタクラスとの混同**: `__init_subclass__`とメタクラスの違いを理解しない
2. **過度な検証**: 必要以上に複雑な検証を行う
3. **設定の不適切な適用**: 設定の適用方法を誤る

### 応用例

```python
# データベースモデルでの__init_subclass__活用
class DatabaseModel:
    """データベースモデルベースクラス"""
    
    def __init_subclass__(cls, table_name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # テーブル名を設定
        if table_name:
            cls.table_name = table_name
        else:
            cls.table_name = cls.__name__.lower()
        
        # 必須属性をチェック
        if not hasattr(cls, 'primary_key'):
            cls.primary_key = 'id'
        
        # インデックスを設定
        if not hasattr(cls, 'indexes'):
            cls.indexes = []
        
        print(f"データベースモデル {cls.__name__} を初期化しました")

class User(DatabaseModel, table_name='users'):
    """ユーザーモデル"""
    primary_key = 'user_id'
    indexes = ['email', 'created_at']
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = '2023-01-01'
    
    def save(self):
        """保存"""
        print(f"ユーザー {self.name} をテーブル {self.table_name} に保存")

class Product(DatabaseModel, table_name='products'):
    """商品モデル"""
    primary_key = 'product_id'
    indexes = ['category', 'price']
    
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category
    
    def save(self):
        """保存"""
        print(f"商品 {self.name} をテーブル {self.table_name} に保存")

# 使用例
print("=== データベースモデル ===")
user = User("Alice", "alice@example.com")
print(f"ユーザーテーブル: {user.table_name}")
print(f"プライマリキー: {user.primary_key}")
print(f"インデックス: {user.indexes}")
user.save()

product = Product("Laptop", 100000, "Electronics")
print(f"商品テーブル: {product.table_name}")
print(f"プライマリキー: {product.primary_key}")
print(f"インデックス: {product.indexes}")
product.save()
```

### ベストプラクティス

- `__init_subclass__`でサブクラスの検証を行う
- 設定の自動適用に活用する
- プラグインシステムの構築に使用する
- メタクラスよりもシンプルな解決策を優先する

---

## まとめ

Chapter 8では、メタクラスと属性のベストプラクティスを学びました：

1. **__new__**: オブジェクトの構築を制御する
2. **__init_subclass__**: サブクラスを検証する
3. **__set_name__**: メタクラスを避ける
4. **__prepare__**: 名前空間を事前に準備する
5. **属性アクセス**: `__getattr__`、`__getattribute__`、`__setattr__`の違いを理解する
6. **__slots__**: メモリ使用量を削減する
7. **デスクリプタ**: 再利用可能なプロパティロジックを作成する
8. **プロパティ**: 単純な属性アクセスを置き換える
9. **プロパティ**: リファクタリングを容易にする
10. **メタクラス**: クラスの動作を制御する

これらの原則を実践することで、高度で柔軟なクラス設計ができるようになります。

