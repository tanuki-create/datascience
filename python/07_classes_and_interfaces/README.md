# Chapter 7: Classes and Interfaces

クラスとインターフェースのベストプラクティスを学びます。

## 目次

1. [クラス属性のオーバーライドを避ける](#1-クラス属性のオーバーライドを避ける)
2. [インスタンス属性の初期化に__init__を使用する](#2-インスタンス属性の初期化に__init__を使用する)
3. [プロパティで単純な属性アクセスを置き換える](#3-プロパティで単純な属性アクセスを置き換える)
4. [プロパティでリファクタリングを容易にする](#4-プロパティでリファクタリングを容易にする)
5. [デスクリプタで再利用可能なプロパティロジックを作成する](#5-デスクリプタで再利用可能なプロパティロジックを作成する)
6. [__getattr__、__getattribute__、__setattr__の違いを理解する](#6-__getattr__、__getattribute__、__setattr__の違いを理解する)
7. [__slots__でメモリ使用量を削減する](#7-__slots__でメモリ使用量を削減する)
8. [__init_subclass__でサブクラスを検証する](#8-__init_subclass__でサブクラスを検証する)
9. [__set_name__でメタクラスを避ける](#9-__set_name__でメタクラスを避ける)
10. [__prepare__で名前空間を事前に準備する](#10-__prepare__で名前空間を事前に準備する)

---

## 1. クラス属性のオーバーライドを避ける

### 基本概念

クラス属性をオーバーライドすると、予期しない動作を引き起こす可能性があります。インスタンス属性を使用することで、より安全で予測可能なコードを書けます。

### 具体例

#### 例1: クラス属性のオーバーライドの問題

```python
# 悪い例（クラス属性のオーバーライド）
class CounterBad:
    """カウンタークラス（悪い例）"""
    count = 0  # クラス属性
    
    def __init__(self, name):
        self.name = name
    
    def increment(self):
        """カウントを増加"""
        self.count += 1  # クラス属性を変更
        return self.count

# 良い例（インスタンス属性の使用）
class CounterGood:
    """カウンタークラス（良い例）"""
    
    def __init__(self, name):
        self.name = name
        self.count = 0  # インスタンス属性
    
    def increment(self):
        """カウントを増加"""
        self.count += 1
        return self.count

# 使用例
print("=== クラス属性のオーバーライドの問題 ===")

# 悪い例
counter1_bad = CounterBad("Counter 1")
counter2_bad = CounterBad("Counter 2")

print(f"Counter 1: {counter1_bad.increment()}")  # 1
print(f"Counter 2: {counter2_bad.increment()}")  # 2 (予期しない結果)
print(f"Counter 1: {counter1_bad.increment()}")  # 3 (予期しない結果)

# 良い例
counter1_good = CounterGood("Counter 1")
counter2_good = CounterGood("Counter 2")

print(f"\nCounter 1: {counter1_good.increment()}")  # 1
print(f"Counter 2: {counter2_good.increment()}")  # 1 (正しい結果)
print(f"Counter 1: {counter1_good.increment()}")  # 2 (正しい結果)
```

#### 例2: 設定管理でのクラス属性の問題

```python
# 悪い例（クラス属性のオーバーライド）
class ConfigBad:
    """設定クラス（悪い例）"""
    debug = False
    log_level = 'INFO'
    
    def __init__(self, name):
        self.name = name
    
    def set_debug(self, debug):
        """デバッグモードを設定"""
        self.debug = debug  # クラス属性を変更
    
    def set_log_level(self, level):
        """ログレベルを設定"""
        self.log_level = level  # クラス属性を変更

# 良い例（インスタンス属性の使用）
class ConfigGood:
    """設定クラス（良い例）"""
    
    def __init__(self, name, debug=False, log_level='INFO'):
        self.name = name
        self.debug = debug  # インスタンス属性
        self.log_level = log_level  # インスタンス属性
    
    def set_debug(self, debug):
        """デバッグモードを設定"""
        self.debug = debug
    
    def set_log_level(self, level):
        """ログレベルを設定"""
        self.log_level = level

# 使用例
print("=== 設定管理でのクラス属性の問題 ===")

# 悪い例
config1_bad = ConfigBad("Config 1")
config2_bad = ConfigBad("Config 2")

config1_bad.set_debug(True)
config1_bad.set_log_level('DEBUG')

print(f"Config 1 debug: {config1_bad.debug}")  # True
print(f"Config 2 debug: {config2_bad.debug}")  # True (予期しない結果)
print(f"Config 1 log_level: {config1_bad.log_level}")  # DEBUG
print(f"Config 2 log_level: {config2_bad.log_level}")  # DEBUG (予期しない結果)

# 良い例
config1_good = ConfigGood("Config 1")
config2_good = ConfigGood("Config 2")

config1_good.set_debug(True)
config1_good.set_log_level('DEBUG')

print(f"\nConfig 1 debug: {config1_good.debug}")  # True
print(f"Config 2 debug: {config2_good.debug}")  # False (正しい結果)
print(f"Config 1 log_level: {config1_good.log_level}")  # DEBUG
print(f"Config 2 log_level: {config2_good.log_level}")  # INFO (正しい結果)
```

#### 例3: データベース接続でのクラス属性の問題

```python
# 悪い例（クラス属性のオーバーライド）
class DatabaseConnectionBad:
    """データベース接続クラス（悪い例）"""
    connection = None
    connected = False
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def connect(self):
        """データベースに接続"""
        self.connection = f"{self.host}:{self.port}"
        self.connected = True
    
    def disconnect(self):
        """データベースから切断"""
        self.connection = None
        self.connected = False

# 良い例（インスタンス属性の使用）
class DatabaseConnectionGood:
    """データベース接続クラス（良い例）"""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
        self.connected = False
    
    def connect(self):
        """データベースに接続"""
        self.connection = f"{self.host}:{self.port}"
        self.connected = True
    
    def disconnect(self):
        """データベースから切断"""
        self.connection = None
        self.connected = False

# 使用例
print("=== データベース接続でのクラス属性の問題 ===")

# 悪い例
db1_bad = DatabaseConnectionBad("localhost", 5432)
db2_bad = DatabaseConnectionBad("remote", 3306)

db1_bad.connect()
print(f"DB1 connected: {db1_bad.connected}")  # True
print(f"DB2 connected: {db2_bad.connected}")  # True (予期しない結果)

db1_bad.disconnect()
print(f"DB1 connected: {db1_bad.connected}")  # False
print(f"DB2 connected: {db2_bad.connected}")  # False (予期しない結果)

# 良い例
db1_good = DatabaseConnectionGood("localhost", 5432)
db2_good = DatabaseConnectionGood("remote", 3306)

db1_good.connect()
print(f"\nDB1 connected: {db1_good.connected}")  # True
print(f"DB2 connected: {db2_good.connected}")  # False (正しい結果)

db1_good.disconnect()
print(f"DB1 connected: {db1_good.connected}")  # False
print(f"DB2 connected: {db2_good.connected}")  # False (正しい結果)
```

### よくある間違い

1. **クラス属性のオーバーライド**: インスタンス属性として使用すべき属性をクラス属性として定義
2. **共有状態の無視**: クラス属性が共有されることを理解しない
3. **初期化の不備**: インスタンス属性の適切な初期化を行わない

### 応用例

```python
# ログ管理でのクラス属性の問題
class LoggerBad:
    """ログクラス（悪い例）"""
    log_level = 'INFO'
    log_file = None
    
    def __init__(self, name):
        self.name = name
    
    def set_log_level(self, level):
        """ログレベルを設定"""
        self.log_level = level
    
    def set_log_file(self, filename):
        """ログファイルを設定"""
        self.log_file = filename

class LoggerGood:
    """ログクラス（良い例）"""
    
    def __init__(self, name, log_level='INFO', log_file=None):
        self.name = name
        self.log_level = log_level
        self.log_file = log_file
    
    def set_log_level(self, level):
        """ログレベルを設定"""
        self.log_level = level
    
    def set_log_file(self, filename):
        """ログファイルを設定"""
        self.log_file = filename
    
    def log(self, message, level='INFO'):
        """ログを出力"""
        if level >= self.log_level:
            print(f"[{self.name}] {level}: {message}")

# 使用例
print("=== ログ管理でのクラス属性の問題 ===")

# 悪い例
logger1_bad = LoggerBad("Logger 1")
logger2_bad = LoggerBad("Logger 2")

logger1_bad.set_log_level('DEBUG')
logger1_bad.set_log_file('app.log')

print(f"Logger 1 level: {logger1_bad.log_level}")  # DEBUG
print(f"Logger 2 level: {logger2_bad.log_level}")  # DEBUG (予期しない結果)
print(f"Logger 1 file: {logger1_bad.log_file}")  # app.log
print(f"Logger 2 file: {logger2_bad.log_file}")  # app.log (予期しない結果)

# 良い例
logger1_good = LoggerGood("Logger 1")
logger2_good = LoggerGood("Logger 2")

logger1_good.set_log_level('DEBUG')
logger1_good.set_log_file('app.log')

print(f"\nLogger 1 level: {logger1_good.log_level}")  # DEBUG
print(f"Logger 2 level: {logger2_good.log_level}")  # INFO (正しい結果)
print(f"Logger 1 file: {logger1_good.log_file}")  # app.log
print(f"Logger 2 file: {logger2_good.log_file}")  # None (正しい結果)

# ログ出力
logger1_good.log("Test message", "DEBUG")
logger2_good.log("Test message", "DEBUG")
```

### ベストプラクティス

- インスタンス属性を使用する
- クラス属性は定数として使用する
- 共有状態を避ける
- 適切な初期化を行う

---

## 2. インスタンス属性の初期化に__init__を使用する

### 基本概念

`__init__`メソッドを使用してインスタンス属性を初期化することで、オブジェクトの状態を明確にし、予測可能な動作を保証できます。

### 具体例

#### 例1: 基本的な__init__の使用

```python
# 悪い例（__init__を使用しない）
class PersonBad:
    """人物クラス（悪い例）"""
    
    def set_name(self, name):
        """名前を設定"""
        self.name = name
    
    def set_age(self, age):
        """年齢を設定"""
        self.age = age
    
    def get_info(self):
        """情報を取得"""
        return f"{self.name} is {self.age} years old"

# 良い例（__init__を使用）
class PersonGood:
    """人物クラス（良い例）"""
    
    def __init__(self, name, age):
        """初期化"""
        self.name = name
        self.age = age
    
    def get_info(self):
        """情報を取得"""
        return f"{self.name} is {self.age} years old"

# 使用例
print("=== インスタンス属性の初期化 ===")

# 悪い例
person_bad = PersonBad()
person_bad.set_name("Alice")
person_bad.set_age(25)
print(f"悪い例: {person_bad.get_info()}")

# 良い例
person_good = PersonGood("Alice", 25)
print(f"良い例: {person_good.get_info()}")
```

#### 例2: 複雑な初期化

```python
# 複雑な初期化での__init__の使用
class BankAccount:
    """銀行口座クラス"""
    
    def __init__(self, account_number, owner_name, initial_balance=0):
        """初期化"""
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = initial_balance
        self.transactions = []
        self.is_active = True
    
    def deposit(self, amount):
        """入金"""
        if not self.is_active:
            raise ValueError("口座が無効です")
        if amount <= 0:
            raise ValueError("入金額は正の値である必要があります")
        
        self.balance += amount
        self.transactions.append(f"入金: +{amount}")
        return self.balance
    
    def withdraw(self, amount):
        """出金"""
        if not self.is_active:
            raise ValueError("口座が無効です")
        if amount <= 0:
            raise ValueError("出金額は正の値である必要があります")
        if amount > self.balance:
            raise ValueError("残高不足です")
        
        self.balance -= amount
        self.transactions.append(f"出金: -{amount}")
        return self.balance
    
    def get_balance(self):
        """残高を取得"""
        return self.balance
    
    def get_transactions(self):
        """取引履歴を取得"""
        return self.transactions.copy()

# 使用例
print("=== 銀行口座の初期化 ===")

# 口座を作成
account = BankAccount("123456789", "Alice", 1000)
print(f"口座番号: {account.account_number}")
print(f"所有者: {account.owner_name}")
print(f"初期残高: {account.get_balance()}")

# 入金
account.deposit(500)
print(f"入金後の残高: {account.get_balance()}")

# 出金
account.withdraw(200)
print(f"出金後の残高: {account.get_balance()}")

# 取引履歴
print(f"取引履歴: {account.get_transactions()}")
```

#### 例3: デフォルト値とバリデーション

```python
# デフォルト値とバリデーションでの__init__の使用
class Product:
    """商品クラス"""
    
    def __init__(self, name, price, category="未分類", description=""):
        """初期化"""
        if not name:
            raise ValueError("商品名は必須です")
        if price < 0:
            raise ValueError("価格は負の値にできません")
        
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.created_at = "2023-01-01"  # 実際の実装では現在時刻
        self.is_available = True
    
    def update_price(self, new_price):
        """価格を更新"""
        if new_price < 0:
            raise ValueError("価格は負の値にできません")
        self.price = new_price
    
    def update_category(self, new_category):
        """カテゴリを更新"""
        self.category = new_category
    
    def get_info(self):
        """商品情報を取得"""
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "description": self.description,
            "is_available": self.is_available
        }

# 使用例
print("=== 商品の初期化 ===")

# 商品を作成
product = Product("Laptop", 100000, "Electronics", "高性能ノートパソコン")
print(f"商品情報: {product.get_info()}")

# 価格を更新
product.update_price(95000)
print(f"価格更新後: {product.get_info()}")

# カテゴリを更新
product.update_category("Computer")
print(f"カテゴリ更新後: {product.get_info()}")

# エラーハンドリング
try:
    invalid_product = Product("", -100)
except ValueError as e:
    print(f"エラー: {e}")
```

### よくある間違い

1. **__init__の不使用**: インスタンス属性を適切に初期化しない
2. **バリデーションの不備**: 初期化時のバリデーションを行わない
3. **デフォルト値の不適切な設定**: 意味のないデフォルト値を設定する

### 応用例

```python
# 設定管理での__init__の使用
class AppConfig:
    """アプリケーション設定クラス"""
    
    def __init__(self, config_dict=None):
        """初期化"""
        config_dict = config_dict or {}
        
        # デフォルト値を設定
        self.debug = config_dict.get('debug', False)
        self.log_level = config_dict.get('log_level', 'INFO')
        self.database_url = config_dict.get('database_url', 'sqlite:///app.db')
        self.secret_key = config_dict.get('secret_key', 'default-secret')
        self.max_connections = config_dict.get('max_connections', 10)
        
        # バリデーション
        if not isinstance(self.debug, bool):
            raise ValueError("debugは真偽値である必要があります")
        if self.log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            raise ValueError("log_levelは有効な値である必要があります")
        if self.max_connections <= 0:
            raise ValueError("max_connectionsは正の値である必要があります")
    
    def update_config(self, updates):
        """設定を更新"""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"不明な設定キー: {key}")
    
    def get_config(self):
        """設定を取得"""
        return {
            'debug': self.debug,
            'log_level': self.log_level,
            'database_url': self.database_url,
            'secret_key': self.secret_key,
            'max_connections': self.max_connections
        }

# 使用例
print("=== アプリケーション設定の初期化 ===")

# デフォルト設定で作成
default_config = AppConfig()
print(f"デフォルト設定: {default_config.get_config()}")

# カスタム設定で作成
custom_config = AppConfig({
    'debug': True,
    'log_level': 'DEBUG',
    'database_url': 'postgresql://localhost/myapp',
    'max_connections': 20
})
print(f"カスタム設定: {custom_config.get_config()}")

# 設定を更新
custom_config.update_config({'log_level': 'WARNING'})
print(f"更新後の設定: {custom_config.get_config()}")

# エラーハンドリング
try:
    invalid_config = AppConfig({'debug': 'yes', 'log_level': 'INVALID'})
except ValueError as e:
    print(f"設定エラー: {e}")
```

### ベストプラクティス

- `__init__`でインスタンス属性を初期化する
- 適切なバリデーションを行う
- デフォルト値を適切に設定する
- エラーハンドリングを適切に行う

---

## まとめ

Chapter 7では、クラスとインターフェースのベストプラクティスを学びました：

1. **クラス属性のオーバーライド**: インスタンス属性を使用する
2. **__init__の使用**: インスタンス属性の適切な初期化
3. **プロパティ**: 単純な属性アクセスを置き換える
4. **プロパティ**: リファクタリングを容易にする
5. **デスクリプタ**: 再利用可能なプロパティロジックを作成する
6. **属性アクセス**: `__getattr__`、`__getattribute__`、`__setattr__`の違いを理解する
7. **__slots__**: メモリ使用量を削減する
8. **__init_subclass__**: サブクラスを検証する
9. **__set_name__**: メタクラスを避ける
10. **__prepare__**: 名前空間を事前に準備する

これらの原則を実践することで、効率的で保守性の高いクラスを設計できるようになります。
