# Chapter 4: Dictionaries

辞書のベストプラクティスを学びます。

## 目次

1. [辞書の挿入順序に依存する際は注意する](#1-辞書の挿入順序に依存する際は注意する)
2. [欠落した辞書キーを処理するためにgetを使用する](#2-欠落した辞書キーを処理するためにgetを使用する)
3. [内部状態の欠落アイテムを処理するためにdefaultdictを好む](#3-内部状態の欠落アイテムを処理するためにdefaultdictを好む)
4. [__missing__でキー依存のデフォルト値を構築する方法を知る](#4-__missing__でキー依存のデフォルト値を構築する方法を知る)
5. [辞書、リスト、タプルを深くネストする代わりにクラスを構成する](#5-辞書、リスト、タプルを深くネストする代わりにクラスを構成する)

---

## 1. 辞書の挿入順序に依存する際は注意する

### 基本概念

Python 3.7以降では、辞書は挿入順序を保持しますが、この機能に依存するコードは注意深く設計する必要があります。古いバージョンとの互換性や、パフォーマンスを考慮する必要があります。

### 具体例

#### 例1: 挿入順序の基本的な使用

```python
# Python 3.7+ での挿入順序保持
def process_ordered_data():
    """挿入順序を保持したデータ処理"""
    data = {}
    data['first'] = 1
    data['second'] = 2
    data['third'] = 3
    
    # 挿入順序でイテレート
    for key, value in data.items():
        print(f"{key}: {value}")
    
    return data

# 使用例
result = process_ordered_data()
print(f"辞書の順序: {list(result.keys())}")

# 順序が重要な処理
def process_ordered_config(config_dict):
    """設定を順序付きで処理"""
    processed_config = {}
    for key, value in config_dict.items():
        if isinstance(value, str):
            processed_config[key] = value.upper()
        else:
            processed_config[key] = value
    return processed_config

# 使用例
config = {
    'database_host': 'localhost',
    'database_port': 5432,
    'database_name': 'myapp',
    'debug_mode': True
}

processed = process_ordered_config(config)
print(f"処理された設定: {processed}")
```

#### 例2: 順序依存の処理

```python
# 順序が重要なデータ処理
class OrderedDataProcessor:
    """順序付きデータ処理クラス"""
    
    def __init__(self):
        self.steps = {}
        self.execution_order = []
    
    def add_step(self, name, func):
        """ステップを追加"""
        self.steps[name] = func
        self.execution_order.append(name)
    
    def execute_steps(self):
        """ステップを順序付きで実行"""
        results = {}
        for step_name in self.execution_order:
            if step_name in self.steps:
                print(f"実行中: {step_name}")
                results[step_name] = self.steps[step_name]()
        return results

# 使用例
processor = OrderedDataProcessor()

# ステップを順序付きで追加
processor.add_step('validate', lambda: "データ検証完了")
processor.add_step('transform', lambda: "データ変換完了")
processor.add_step('save', lambda: "データ保存完了")

results = processor.execute_steps()
print(f"実行結果: {results}")
```

#### 例3: 順序依存の注意点

```python
# 順序依存の注意点
def demonstrate_order_dependency():
    """順序依存の注意点をデモンストレーション"""
    
    # 順序が重要な処理
    def process_user_data(users):
        """ユーザーデータを処理"""
        processed_users = {}
        for user_id, user_data in users.items():
            # 順序が重要な処理
            if 'name' in user_data and 'email' in user_data:
                processed_users[user_id] = {
                    'name': user_data['name'],
                    'email': user_data['email'],
                    'processed_at': '2023-01-01 10:00:00'
                }
        return processed_users
    
    # 順序付きユーザーデータ
    users = {
        'user1': {'name': 'Alice', 'email': 'alice@example.com'},
        'user2': {'name': 'Bob', 'email': 'bob@example.com'},
        'user3': {'name': 'Charlie', 'email': 'charlie@example.com'}
    }
    
    processed = process_user_data(users)
    print(f"処理されたユーザー: {processed}")
    
    # 順序が重要な場合の注意点
    print("\n注意点:")
    print("1. Python 3.7未満では順序が保証されない")
    print("2. 辞書の操作（削除、更新）で順序が変わる可能性")
    print("3. パフォーマンスを考慮する必要がある")

demonstrate_order_dependency()
```

### よくある間違い

1. **古いバージョンでの順序依存**: Python 3.7未満での順序保証の誤解
2. **辞書操作での順序変更**: 削除や更新で順序が変わることの無視
3. **パフォーマンスの軽視**: 大量データでの順序保持のコストを考慮しない

### 応用例

```python
# 設定管理での順序依存
class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self):
        self.config = {}
        self.load_order = []
    
    def set_config(self, key, value):
        """設定を設定"""
        self.config[key] = value
        if key not in self.load_order:
            self.load_order.append(key)
    
    def get_config_chain(self):
        """設定の読み込み順序を取得"""
        return [(key, self.config[key]) for key in self.load_order]
    
    def validate_config(self):
        """設定を検証"""
        for key in self.load_order:
            if key in self.config:
                if not self._is_valid_value(self.config[key]):
                    raise ValueError(f"無効な設定値: {key}")
        return True
    
    def _is_valid_value(self, value):
        """値が有効かどうか"""
        return value is not None and value != ""

# 使用例
config_manager = ConfigManager()

# 設定を順序付きで追加
config_manager.set_config('database_host', 'localhost')
config_manager.set_config('database_port', 5432)
config_manager.set_config('database_name', 'myapp')

# 設定の順序を確認
config_chain = config_manager.get_config_chain()
print("設定の読み込み順序:")
for key, value in config_chain:
    print(f"  {key}: {value}")

# 設定の検証
try:
    config_manager.validate_config()
    print("設定が有効です")
except ValueError as e:
    print(f"設定エラー: {e}")
```

### ベストプラクティス

- 順序依存の処理は明示的にドキュメント化する
- 古いバージョンとの互換性を考慮する
- 辞書操作で順序が変わることを理解する
- パフォーマンスが重要な場合は代替手段を検討する

---

## 2. 欠落した辞書キーを処理するためにgetを使用する

### 基本概念

辞書のキーにアクセスする際、キーが存在しない場合は`KeyError`が発生します。`get`メソッドを使用することで、安全にキーにアクセスできます。

### 具体例

#### 例1: 基本的なget使用

```python
# 悪い例（KeyErrorの可能性）
def get_user_info_bad(user_data):
    """ユーザー情報を取得（KeyErrorの可能性）"""
    name = user_data['name']  # KeyErrorの可能性
    age = user_data['age']    # KeyErrorの可能性
    return f"{name} is {age} years old"

# 良い例（get使用）
def get_user_info_good(user_data):
    """ユーザー情報を取得（get使用）"""
    name = user_data.get('name', 'Unknown')
    age = user_data.get('age', 0)
    return f"{name} is {age} years old"

# 使用例
user_data = {'name': 'Alice', 'age': 25}
print(get_user_info_good(user_data))

# 欠落したキーがある場合
incomplete_data = {'name': 'Bob'}
print(get_user_info_good(incomplete_data))
```

#### 例2: デフォルト値の設定

```python
# デフォルト値の設定
def process_config(config):
    """設定を処理"""
    # デフォルト値を設定
    host = config.get('host', 'localhost')
    port = config.get('port', 8080)
    debug = config.get('debug', False)
    timeout = config.get('timeout', 30)
    
    return {
        'host': host,
        'port': port,
        'debug': debug,
        'timeout': timeout
    }

# 使用例
config = {'host': 'example.com', 'debug': True}
processed_config = process_config(config)
print(f"処理された設定: {processed_config}")

# 空の設定の場合
empty_config = {}
processed_empty = process_config(empty_config)
print(f"空の設定の処理結果: {processed_empty}")
```

#### 例3: ネストした辞書でのget使用

```python
# ネストした辞書でのget使用
def get_nested_value(data, keys, default=None):
    """ネストした辞書から値を取得"""
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        else:
            return default
    return current

# 使用例
nested_data = {
    'user': {
        'profile': {
            'name': 'Alice',
            'age': 25
        },
        'settings': {
            'theme': 'dark'
        }
    }
}

# ネストした値の取得
name = get_nested_value(nested_data, ['user', 'profile', 'name'])
age = get_nested_value(nested_data, ['user', 'profile', 'age'])
theme = get_nested_value(nested_data, ['user', 'settings', 'theme'])

print(f"名前: {name}")
print(f"年齢: {age}")
print(f"テーマ: {theme}")

# 存在しないキーの場合
missing = get_nested_value(nested_data, ['user', 'profile', 'email'], 'N/A')
print(f"メール: {missing}")
```

### よくある間違い

1. **KeyErrorの無視**: キーの存在を確認せずにアクセス
2. **デフォルト値の不適切な設定**: 意味のないデフォルト値の設定
3. **ネストした辞書での不適切な処理**: 深いネストでの安全でないアクセス

### 応用例

```python
# データベース操作でのget使用
class DatabaseConfig:
    """データベース設定クラス"""
    
    def __init__(self, config_dict):
        self.config = config_dict
    
    def get_connection_string(self):
        """接続文字列を取得"""
        host = self.config.get('host', 'localhost')
        port = self.config.get('port', 5432)
        database = self.config.get('database', 'myapp')
        username = self.config.get('username', 'postgres')
        password = self.config.get('password', '')
        
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    def get_pool_settings(self):
        """プール設定を取得"""
        return {
            'min_connections': self.config.get('min_connections', 1),
            'max_connections': self.config.get('max_connections', 10),
            'timeout': self.config.get('timeout', 30)
        }
    
    def validate_config(self):
        """設定を検証"""
        required_keys = ['host', 'database']
        missing_keys = [key for key in required_keys if key not in self.config]
        
        if missing_keys:
            raise ValueError(f"必須設定が不足: {missing_keys}")
        
        return True

# 使用例
db_config = DatabaseConfig({
    'host': 'localhost',
    'database': 'myapp',
    'username': 'postgres'
})

print(f"接続文字列: {db_config.get_connection_string()}")
print(f"プール設定: {db_config.get_pool_settings()}")

try:
    db_config.validate_config()
    print("設定が有効です")
except ValueError as e:
    print(f"設定エラー: {e}")

# APIレスポンス処理でのget使用
class APIResponseProcessor:
    """APIレスポンス処理クラス"""
    
    def process_response(self, response):
        """レスポンスを処理"""
        if not isinstance(response, dict):
            return {'error': 'Invalid response format'}
        
        # 安全にデータを取得
        status = response.get('status', 'unknown')
        data = response.get('data', {})
        message = response.get('message', '')
        error = response.get('error', None)
        
        return {
            'status': status,
            'data': data,
            'message': message,
            'error': error,
            'success': status == 'success'
        }

# 使用例
api_processor = APIResponseProcessor()

# 正常なレスポンス
success_response = {
    'status': 'success',
    'data': {'user_id': 123, 'name': 'Alice'},
    'message': 'User created successfully'
}

# エラーレスポンス
error_response = {
    'status': 'error',
    'error': 'Validation failed'
}

# 不完全なレスポンス
incomplete_response = {
    'status': 'success'
}

print("正常なレスポンス:")
print(api_processor.process_response(success_response))

print("\nエラーレスポンス:")
print(api_processor.process_response(error_response))

print("\n不完全なレスポンス:")
print(api_processor.process_response(incomplete_response))
```

### ベストプラクティス

- キーの存在が不明な場合は`get`を使用する
- 適切なデフォルト値を設定する
- ネストした辞書では安全なアクセス方法を実装する
- エラーハンドリングを適切に行う

---

## 3. 内部状態の欠落アイテムを処理するためにdefaultdictを好む

### 基本概念

`defaultdict`を使用することで、存在しないキーにアクセスした際に自動的にデフォルト値を設定できます。これにより、コードが簡潔になり、エラーを防げます。

### 具体例

#### 例1: 基本的なdefaultdict使用

```python
from collections import defaultdict

# 悪い例（通常の辞書）
def count_items_bad(items):
    """アイテムをカウント（通常の辞書）"""
    counts = {}
    for item in items:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts

# 良い例（defaultdict使用）
def count_items_good(items):
    """アイテムをカウント（defaultdict使用）"""
    counts = defaultdict(int)
    for item in items:
        counts[item] += 1
    return counts

# 使用例
items = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
counts = count_items_good(items)
print(f"アイテムのカウント: {dict(counts)}")
```

#### 例2: リストをデフォルト値とするdefaultdict

```python
# リストをデフォルト値とするdefaultdict
def group_items_by_category(items):
    """アイテムをカテゴリでグループ化"""
    groups = defaultdict(list)
    for item, category in items:
        groups[category].append(item)
    return groups

# 使用例
items_with_categories = [
    ('apple', 'fruit'),
    ('banana', 'fruit'),
    ('carrot', 'vegetable'),
    ('tomato', 'vegetable'),
    ('orange', 'fruit')
]

grouped = group_items_by_category(items_with_categories)
print("カテゴリ別グループ化:")
for category, items in grouped.items():
    print(f"  {category}: {items}")
```

#### 例3: セットをデフォルト値とするdefaultdict

```python
# セットをデフォルト値とするdefaultdict
def find_common_items(data):
    """共通アイテムを見つける"""
    item_sets = defaultdict(set)
    for group, items in data.items():
        for item in items:
            item_sets[item].add(group)
    
    # 複数のグループに属するアイテムを見つける
    common_items = {item: groups for item, groups in item_sets.items() if len(groups) > 1}
    return common_items

# 使用例
data = {
    'group1': ['apple', 'banana', 'cherry'],
    'group2': ['banana', 'cherry', 'date'],
    'group3': ['cherry', 'date', 'elderberry']
}

common = find_common_items(data)
print("共通アイテム:")
for item, groups in common.items():
    print(f"  {item}: {groups}")
```

### よくある間違い

1. **defaultdictの不使用**: 複雑な条件分岐で通常の辞書を使用
2. **不適切なデフォルト値**: 目的に合わないデフォルト値の設定
3. **メモリ効率の軽視**: 大量データでのメモリ使用量を考慮しない

### 応用例

```python
# データベース操作でのdefaultdict活用
class DatabaseProcessor:
    """データベース処理クラス"""
    
    def __init__(self):
        self.queries = defaultdict(list)
        self.query_counts = defaultdict(int)
        self.query_times = defaultdict(list)
    
    def log_query(self, query_type, query, execution_time):
        """クエリをログに記録"""
        self.queries[query_type].append(query)
        self.query_counts[query_type] += 1
        self.query_times[query_type].append(execution_time)
    
    def get_query_statistics(self):
        """クエリ統計を取得"""
        stats = {}
        for query_type in self.queries:
            times = self.query_times[query_type]
            stats[query_type] = {
                'count': self.query_counts[query_type],
                'avg_time': sum(times) / len(times) if times else 0,
                'max_time': max(times) if times else 0,
                'min_time': min(times) if times else 0
            }
        return stats
    
    def get_slow_queries(self, threshold=1.0):
        """遅いクエリを取得"""
        slow_queries = defaultdict(list)
        for query_type, times in self.query_times.items():
            for i, time in enumerate(times):
                if time > threshold:
                    slow_queries[query_type].append({
                        'query': self.queries[query_type][i],
                        'time': time
                    })
        return slow_queries

# 使用例
processor = DatabaseProcessor()

# クエリをログに記録
processor.log_query('SELECT', 'SELECT * FROM users', 0.5)
processor.log_query('INSERT', 'INSERT INTO users VALUES (...)', 0.8)
processor.log_query('SELECT', 'SELECT * FROM orders', 1.2)
processor.log_query('UPDATE', 'UPDATE users SET name = ...', 0.3)

# 統計を取得
stats = processor.get_query_statistics()
print("クエリ統計:")
for query_type, stat in stats.items():
    print(f"  {query_type}: {stat}")

# 遅いクエリを取得
slow_queries = processor.get_slow_queries(0.7)
print("\n遅いクエリ:")
for query_type, queries in slow_queries.items():
    print(f"  {query_type}: {len(queries)}件")

# ファイル処理でのdefaultdict活用
class FileProcessor:
    """ファイル処理クラス"""
    
    def __init__(self):
        self.file_stats = defaultdict(lambda: {'lines': 0, 'size': 0, 'extensions': set()})
        self.line_counts = defaultdict(int)
    
    def process_file(self, filename, content):
        """ファイルを処理"""
        lines = content.split('\n')
        extension = filename.split('.')[-1] if '.' in filename else 'no_extension'
        
        # ファイル統計を更新
        self.file_stats[filename]['lines'] = len(lines)
        self.file_stats[filename]['size'] = len(content)
        self.file_stats[filename]['extensions'].add(extension)
        
        # 行数をカウント
        for line in lines:
            if line.strip():
                self.line_counts[line.strip()] += 1
    
    def get_file_summary(self):
        """ファイルサマリーを取得"""
        total_files = len(self.file_stats)
        total_lines = sum(stats['lines'] for stats in self.file_stats.values())
        total_size = sum(stats['size'] for stats in self.file_stats.values())
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'total_size': total_size,
            'avg_lines_per_file': total_lines / total_files if total_files > 0 else 0
        }
    
    def get_duplicate_lines(self):
        """重複行を取得"""
        return {line: count for line, count in self.line_counts.items() if count > 1}

# 使用例
file_processor = FileProcessor()

# ファイルを処理
file_processor.process_file('file1.txt', 'Hello\nWorld\nHello\nPython')
file_processor.process_file('file2.txt', 'World\nPython\nData\nScience')

# サマリーを取得
summary = file_processor.get_file_summary()
print(f"ファイルサマリー: {summary}")

# 重複行を取得
duplicates = file_processor.get_duplicate_lines()
print(f"重複行: {duplicates}")
```

### ベストプラクティス

- 内部状態の管理には`defaultdict`を使用する
- 適切なデフォルト値を選択する
- メモリ効率を考慮する
- 複雑なデータ構造には適切なデフォルト値を設定する

---

## 4. __missing__でキー依存のデフォルト値を構築する方法を知る

### 基本概念

`__missing__`メソッドを実装することで、存在しないキーにアクセスした際の動作をカスタマイズできます。これにより、キーに依存したデフォルト値を動的に生成できます。

### 具体例

#### 例1: 基本的な__missing__実装

```python
class DynamicDict(dict):
    """動的なデフォルト値を提供する辞書"""
    
    def __missing__(self, key):
        """存在しないキーにアクセスした際の処理"""
        if isinstance(key, str):
            # 文字列キーの場合は大文字に変換
            return key.upper()
        elif isinstance(key, int):
            # 整数キーの場合は2倍
            return key * 2
        else:
            # その他の場合は文字列表現
            return str(key)

# 使用例
dynamic_dict = DynamicDict()
print(f"文字列キー: {dynamic_dict['hello']}")  # HELLO
print(f"整数キー: {dynamic_dict[5]}")          # 10
print(f"その他: {dynamic_dict[3.14]}")         # 3.14
```

#### 例2: キー依存のデフォルト値

```python
class ConfigDict(dict):
    """設定辞書クラス"""
    
    def __missing__(self, key):
        """存在しないキーにアクセスした際の処理"""
        if key.startswith('database_'):
            # データベース関連の設定
            return self._get_database_default(key)
        elif key.startswith('api_'):
            # API関連の設定
            return self._get_api_default(key)
        else:
            # その他の設定
            return self._get_general_default(key)
    
    def _get_database_default(self, key):
        """データベース設定のデフォルト値"""
        defaults = {
            'database_host': 'localhost',
            'database_port': 5432,
            'database_name': 'myapp',
            'database_user': 'postgres',
            'database_password': ''
        }
        return defaults.get(key, None)
    
    def _get_api_default(self, key):
        """API設定のデフォルト値"""
        defaults = {
            'api_timeout': 30,
            'api_retries': 3,
            'api_base_url': 'https://api.example.com'
        }
        return defaults.get(key, None)
    
    def _get_general_default(self, key):
        """一般的な設定のデフォルト値"""
        return None

# 使用例
config = ConfigDict({
    'database_host': 'prod-db.example.com',
    'api_timeout': 60
})

print(f"データベースホスト: {config['database_host']}")  # 設定値
print(f"データベースポート: {config['database_port']}")  # デフォルト値
print(f"APIタイムアウト: {config['api_timeout']}")      # 設定値
print(f"APIリトライ: {config['api_retries']}")          # デフォルト値
```

#### 例3: 複雑なデフォルト値生成

```python
class SmartDict(dict):
    """スマートなデフォルト値を提供する辞書"""
    
    def __missing__(self, key):
        """存在しないキーにアクセスした際の処理"""
        if isinstance(key, str):
            # 文字列キーの場合
            if key.endswith('_list'):
                # リスト型のデフォルト値
                return []
            elif key.endswith('_dict'):
                # 辞書型のデフォルト値
                return {}
            elif key.endswith('_count'):
                # カウント型のデフォルト値
                return 0
            elif key.endswith('_enabled'):
                # 有効/無効型のデフォルト値
                return False
            else:
                # その他の文字列キー
                return f"default_{key}"
        elif isinstance(key, int):
            # 整数キーの場合
            return key * 10
        else:
            # その他のキー
            return f"unknown_{type(key).__name__}"

# 使用例
smart_dict = SmartDict()
print(f"リスト型: {smart_dict['items_list']}")      # []
print(f"辞書型: {smart_dict['config_dict']}")      # {}
print(f"カウント型: {smart_dict['user_count']}")   # 0
print(f"有効/無効型: {smart_dict['debug_enabled']}") # False
print(f"その他: {smart_dict['custom_key']}")       # default_custom_key
print(f"整数: {smart_dict[5]}")                     # 50
```

### よくある間違い

1. **__missing__の誤用**: 不適切なデフォルト値の生成
2. **無限再帰**: `__missing__`内で同じキーにアクセス
3. **パフォーマンスの軽視**: 複雑な処理でのパフォーマンス低下

### 応用例

```python
# データベース操作での__missing__活用
class DatabaseConfigDict(dict):
    """データベース設定辞書クラス"""
    
    def __missing__(self, key):
        """存在しないキーにアクセスした際の処理"""
        if key == 'connection_string':
            # 接続文字列を動的に生成
            host = self.get('host', 'localhost')
            port = self.get('port', 5432)
            database = self.get('database', 'myapp')
            username = self.get('username', 'postgres')
            password = self.get('password', '')
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
        
        elif key == 'pool_settings':
            # プール設定を動的に生成
            return {
                'min_connections': self.get('min_connections', 1),
                'max_connections': self.get('max_connections', 10),
                'timeout': self.get('timeout', 30)
            }
        
        elif key == 'retry_settings':
            # リトライ設定を動的に生成
            return {
                'max_retries': self.get('max_retries', 3),
                'retry_delay': self.get('retry_delay', 1),
                'backoff_factor': self.get('backoff_factor', 2)
            }
        
        else:
            # その他のキー
            return None

# 使用例
db_config = DatabaseConfigDict({
    'host': 'localhost',
    'database': 'myapp',
    'username': 'postgres',
    'max_connections': 20
})

print(f"接続文字列: {db_config['connection_string']}")
print(f"プール設定: {db_config['pool_settings']}")
print(f"リトライ設定: {db_config['retry_settings']}")

# API設定での__missing__活用
class APIConfigDict(dict):
    """API設定辞書クラス"""
    
    def __missing__(self, key):
        """存在しないキーにアクセスした際の処理"""
        if key == 'headers':
            # ヘッダーを動的に生成
            return {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.get('token', '')}",
                'User-Agent': f"API-Client/{self.get('version', '1.0')}"
            }
        
        elif key == 'timeout_settings':
            # タイムアウト設定を動的に生成
            return {
                'connect_timeout': self.get('connect_timeout', 10),
                'read_timeout': self.get('read_timeout', 30),
                'total_timeout': self.get('total_timeout', 60)
            }
        
        elif key == 'retry_policy':
            # リトライポリシーを動的に生成
            return {
                'max_retries': self.get('max_retries', 3),
                'retry_delay': self.get('retry_delay', 1),
                'backoff_factor': self.get('backoff_factor', 2),
                'retry_on': self.get('retry_on', [500, 502, 503, 504])
            }
        
        else:
            return None

# 使用例
api_config = APIConfigDict({
    'token': 'abc123',
    'version': '2.0',
    'connect_timeout': 15,
    'max_retries': 5
})

print(f"ヘッダー: {api_config['headers']}")
print(f"タイムアウト設定: {api_config['timeout_settings']}")
print(f"リトライポリシー: {api_config['retry_policy']}")
```

### ベストプラクティス

- `__missing__`は適切なデフォルト値の生成に使用する
- 無限再帰を避ける
- パフォーマンスを考慮する
- 複雑なロジックは別メソッドに分離する

---

## 5. 辞書、リスト、タプルを深くネストする代わりにクラスを構成する

### 基本概念

深くネストしたデータ構造は理解が困難で、保守性が低くなります。代わりにクラスを使用することで、データの構造を明確にし、操作を簡潔にできます。

### 具体例

#### 例1: ネストした辞書の問題

```python
# 悪い例（深くネストした辞書）
def create_user_data_bad():
    """ユーザーデータを作成（ネストした辞書）"""
    return {
        'user': {
            'id': 1,
            'name': 'Alice',
            'profile': {
                'age': 25,
                'email': 'alice@example.com',
                'address': {
                    'street': '123 Main St',
                    'city': 'Tokyo',
                    'country': 'Japan'
                }
            },
            'settings': {
                'theme': 'dark',
                'notifications': {
                    'email': True,
                    'push': False
                }
            }
        }
    }

# 良い例（クラスを使用）
class Address:
    """住所クラス"""
    def __init__(self, street, city, country):
        self.street = street
        self.city = city
        self.country = country
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class Notifications:
    """通知設定クラス"""
    def __init__(self, email=True, push=False):
        self.email = email
        self.push = push

class Settings:
    """設定クラス"""
    def __init__(self, theme='light', notifications=None):
        self.theme = theme
        self.notifications = notifications or Notifications()

class Profile:
    """プロフィールクラス"""
    def __init__(self, age, email, address):
        self.age = age
        self.email = email
        self.address = address

class User:
    """ユーザークラス"""
    def __init__(self, user_id, name, profile, settings):
        self.id = user_id
        self.name = name
        self.profile = profile
        self.settings = settings
    
    def get_full_address(self):
        """完全な住所を取得"""
        return str(self.profile.address)
    
    def is_notification_enabled(self, type_name):
        """通知が有効かどうか"""
        return getattr(self.settings.notifications, type_name, False)

# 使用例
address = Address('123 Main St', 'Tokyo', 'Japan')
notifications = Notifications(email=True, push=False)
settings = Settings(theme='dark', notifications=notifications)
profile = Profile(25, 'alice@example.com', address)
user = User(1, 'Alice', profile, settings)

print(f"ユーザー: {user.name}")
print(f"住所: {user.get_full_address()}")
print(f"メール通知: {user.is_notification_enabled('email')}")
```

#### 例2: データベース操作でのクラス活用

```python
# データベース操作でのクラス活用
class DatabaseConnection:
    """データベース接続クラス"""
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
    
    def get_connection_string(self):
        """接続文字列を取得"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_pool_settings(self):
        """プール設定を取得"""
        return {
            'min_connections': 1,
            'max_connections': 10,
            'timeout': 30
        }

class DatabaseConfig:
    """データベース設定クラス"""
    def __init__(self, connection, pool_settings=None):
        self.connection = connection
        self.pool_settings = pool_settings or {}
    
    def validate(self):
        """設定を検証"""
        if not self.connection.host:
            raise ValueError("ホストが設定されていません")
        if not self.connection.database:
            raise ValueError("データベース名が設定されていません")
        return True

# 使用例
connection = DatabaseConnection('localhost', 5432, 'myapp', 'postgres', 'password')
config = DatabaseConfig(connection)

try:
    config.validate()
    print(f"接続文字列: {connection.get_connection_string()}")
    print(f"プール設定: {connection.get_pool_settings()}")
except ValueError as e:
    print(f"設定エラー: {e}")
```

#### 例3: API設定でのクラス活用

```python
# API設定でのクラス活用
class APITimeout:
    """APIタイムアウト設定クラス"""
    def __init__(self, connect=10, read=30, total=60):
        self.connect = connect
        self.read = read
        self.total = total

class APIRetry:
    """APIリトライ設定クラス"""
    def __init__(self, max_retries=3, delay=1, backoff_factor=2):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff_factor = backoff_factor

class APIConfig:
    """API設定クラス"""
    def __init__(self, base_url, timeout=None, retry=None, headers=None):
        self.base_url = base_url
        self.timeout = timeout or APITimeout()
        self.retry = retry or APIRetry()
        self.headers = headers or {}
    
    def get_full_url(self, endpoint):
        """完全なURLを取得"""
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    
    def get_headers(self):
        """ヘッダーを取得"""
        return {
            'Content-Type': 'application/json',
            **self.headers
        }

# 使用例
timeout = APITimeout(connect=15, read=45, total=90)
retry = APIRetry(max_retries=5, delay=2, backoff_factor=3)
api_config = APIConfig(
    base_url='https://api.example.com',
    timeout=timeout,
    retry=retry,
    headers={'Authorization': 'Bearer token123'}
)

print(f"完全なURL: {api_config.get_full_url('/users')}")
print(f"ヘッダー: {api_config.get_headers()}")
print(f"タイムアウト設定: {api_config.timeout.__dict__}")
print(f"リトライ設定: {api_config.retry.__dict__}")
```

### よくある間違い

1. **深いネストの継続**: 複雑なデータ構造を辞書で管理
2. **クラス設計の不備**: 適切な責任分離を行わない
3. **可読性の軽視**: データ構造の意図を明確にしない

### 応用例

```python
# 設定管理でのクラス活用
class LogConfig:
    """ログ設定クラス"""
    def __init__(self, level='INFO', format_string=None, handlers=None):
        self.level = level
        self.format_string = format_string or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.handlers = handlers or []
    
    def add_handler(self, handler_type, **kwargs):
        """ハンドラーを追加"""
        handler = {
            'type': handler_type,
            'config': kwargs
        }
        self.handlers.append(handler)
    
    def get_config(self):
        """設定を取得"""
        return {
            'level': self.level,
            'format': self.format_string,
            'handlers': self.handlers
        }

class AppConfig:
    """アプリケーション設定クラス"""
    def __init__(self, database=None, api=None, logging=None):
        self.database = database
        self.api = api
        self.logging = logging or LogConfig()
    
    def validate(self):
        """設定を検証"""
        errors = []
        
        if not self.database:
            errors.append("データベース設定が不足しています")
        
        if not self.api:
            errors.append("API設定が不足しています")
        
        if errors:
            raise ValueError(f"設定エラー: {', '.join(errors)}")
        
        return True

# 使用例
log_config = LogConfig(level='DEBUG')
log_config.add_handler('file', filename='app.log', max_bytes=10485760, backup_count=5)
log_config.add_handler('console')

app_config = AppConfig(
    database=connection,
    api=api_config,
    logging=log_config
)

try:
    app_config.validate()
    print("アプリケーション設定が有効です")
    print(f"ログ設定: {log_config.get_config()}")
except ValueError as e:
    print(f"設定エラー: {e}")
```

### ベストプラクティス

- 深いネストを避けてクラスを使用する
- 適切な責任分離を行う
- データの構造を明確にする
- 操作を簡潔にする

---

## まとめ

Chapter 4では、辞書のベストプラクティスを学びました：

1. **挿入順序の注意**: 辞書の挿入順序に依存する際は注意する
2. **getメソッドの活用**: 欠落したキーを安全に処理する
3. **defaultdictの活用**: 内部状態の欠落アイテムを効率的に処理する
4. **__missing__の活用**: キー依存のデフォルト値を動的に生成する
5. **クラス構成**: 深いネストを避けてクラスでデータ構造を明確にする

これらの原則を実践することで、効率的で保守性の高い辞書操作ができるようになります。

