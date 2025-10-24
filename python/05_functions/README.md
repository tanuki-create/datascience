# Chapter 5: Functions

関数のベストプラクティスを学びます。

## 目次

1. [関数の引数が変更される可能性があることを知る](#1-関数の引数が変更される可能性があることを知る)
2. [3つ以上の変数をアンパックする必要がある場合は専用の結果オブジェクトを返す](#2-3つ以上の変数をアンパックする必要がある場合は専用の結果オブジェクトを返す)
3. [Noneを返すよりも例外を発生させることを好む](#3-noneを返すよりも例外を発生させることを好む)
4. [クロージャが変数スコープとnonlocalとどのように相互作用するかを知る](#4-クロージャが変数スコープとnonlocalとどのように相互作用するかを知る)
5. [可変位置引数で視覚的ノイズを減らす](#5-可変位置引数で視覚的ノイズを減らす)
6. [キーワード引数でオプションの動作を提供する](#6-キーワード引数でオプションの動作を提供する)
7. [動的デフォルト引数を指定するためにNoneとdocstringを使用する](#7-動的デフォルト引数を指定するためにnoneとdocstringを使用する)
8. [キーワード専用と位置専用の引数で明確性を強制する](#8-キーワード専用と位置専用の引数で明確性を強制する)
9. [関数デコレータをfunctools.wrapsで定義する](#9-関数デコレータをfunctoolswrapsで定義する)
10. [グルー関数にlambda式よりもfunctools.partialを好む](#10-グルー関数にlambda式よりもfunctoolspartialを好む)

---

## 1. 関数の引数が変更される可能性があることを知る

### 基本概念

Pythonでは、関数に渡された引数（特に可変オブジェクト）は、関数内で変更される可能性があります。この動作を理解することで、予期しない副作用を防げます。

### 具体例

#### 例1: リストの変更

```python
# 危険な例（引数を変更）
def process_items_bad(items):
    """アイテムを処理（引数を変更）"""
    items.append('processed')  # 元のリストを変更
    return items

# 安全な例（コピーを作成）
def process_items_good(items):
    """アイテムを処理（コピーを作成）"""
    processed_items = items.copy()
    processed_items.append('processed')
    return processed_items

# 使用例
original_items = ['apple', 'banana', 'cherry']
print(f"元のリスト: {original_items}")

# 危険な例
result_bad = process_items_bad(original_items)
print(f"危険な例の結果: {result_bad}")
print(f"元のリスト（変更後）: {original_items}")  # 元のリストが変更されている

# 安全な例
original_items = ['apple', 'banana', 'cherry']  # リセット
result_good = process_items_good(original_items)
print(f"安全な例の結果: {result_good}")
print(f"元のリスト（変更後）: {original_items}")  # 元のリストは変更されていない
```

#### 例2: 辞書の変更

```python
# 危険な例（辞書を変更）
def update_user_bad(user_data):
    """ユーザーデータを更新（引数を変更）"""
    user_data['last_updated'] = '2023-01-01'  # 元の辞書を変更
    return user_data

# 安全な例（コピーを作成）
def update_user_good(user_data):
    """ユーザーデータを更新（コピーを作成）"""
    updated_data = user_data.copy()
    updated_data['last_updated'] = '2023-01-01'
    return updated_data

# 使用例
original_user = {'name': 'Alice', 'age': 25}
print(f"元のユーザー: {original_user}")

# 危険な例
result_bad = update_user_bad(original_user)
print(f"危険な例の結果: {result_bad}")
print(f"元のユーザー（変更後）: {original_user}")  # 元の辞書が変更されている

# 安全な例
original_user = {'name': 'Alice', 'age': 25}  # リセット
result_good = update_user_good(original_user)
print(f"安全な例の結果: {result_good}")
print(f"元のユーザー（変更後）: {original_user}")  # 元の辞書は変更されていない
```

#### 例3: クラスの属性変更

```python
# 危険な例（オブジェクトの属性を変更）
def update_person_bad(person):
    """人物データを更新（属性を変更）"""
    person.age += 1  # 元のオブジェクトを変更
    return person

# 安全な例（新しいオブジェクトを作成）
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def copy(self):
        return Person(self.name, self.age)
    
    def __str__(self):
        return f"{self.name} ({self.age}歳)"

def update_person_good(person):
    """人物データを更新（新しいオブジェクトを作成）"""
    updated_person = person.copy()
    updated_person.age += 1
    return updated_person

# 使用例
original_person = Person('Alice', 25)
print(f"元の人物: {original_person}")

# 危険な例
result_bad = update_person_bad(original_person)
print(f"危険な例の結果: {result_bad}")
print(f"元の人物（変更後）: {original_person}")  # 元のオブジェクトが変更されている

# 安全な例
original_person = Person('Alice', 25)  # リセット
result_good = update_person_good(original_person)
print(f"安全な例の結果: {result_good}")
print(f"元の人物（変更後）: {original_person}")  # 元のオブジェクトは変更されていない
```

### よくある間違い

1. **引数の変更**: 関数内で引数を直接変更する
2. **副作用の無視**: 関数の副作用を考慮しない
3. **コピーの不使用**: 必要な場合にコピーを作成しない

### 応用例

```python
# データベース操作での安全な処理
class DatabaseProcessor:
    """データベース処理クラス"""
    
    def process_records(self, records):
        """レコードを処理"""
        # 元のレコードを変更しないようにコピーを作成
        processed_records = []
        for record in records.copy():
            processed_record = self._process_single_record(record)
            processed_records.append(processed_record)
        return processed_records
    
    def _process_single_record(self, record):
        """単一レコードを処理"""
        # レコードのコピーを作成
        processed = record.copy()
        processed['processed_at'] = '2023-01-01 10:00:00'
        processed['status'] = 'processed'
        return processed

# 使用例
processor = DatabaseProcessor()
original_records = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'}
]

processed = processor.process_records(original_records)
print(f"元のレコード: {original_records}")
print(f"処理されたレコード: {processed}")

# 設定管理での安全な処理
class ConfigManager:
    """設定管理クラス"""
    
    def update_config(self, config, updates):
        """設定を更新"""
        # 元の設定を変更しないようにコピーを作成
        updated_config = config.copy()
        updated_config.update(updates)
        return updated_config
    
    def merge_configs(self, base_config, override_config):
        """設定をマージ"""
        # ベース設定を変更しないようにコピーを作成
        merged_config = base_config.copy()
        merged_config.update(override_config)
        return merged_config

# 使用例
config_manager = ConfigManager()
base_config = {'host': 'localhost', 'port': 5432}
updates = {'port': 3306, 'database': 'myapp'}

updated_config = config_manager.update_config(base_config, updates)
print(f"元の設定: {base_config}")
print(f"更新された設定: {updated_config}")
```

### ベストプラクティス

- 引数を変更する場合は明示的にドキュメント化する
- 必要な場合はコピーを作成する
- 副作用を避けるためにイミュータブルなオブジェクトを使用する
- 関数の動作を予測可能にする

---

## 2. 3つ以上の変数をアンパックする必要がある場合は専用の結果オブジェクトを返す

### 基本概念

関数が複数の値を返す場合、3つ以上の変数をアンパックするのは可読性を損ないます。専用の結果オブジェクトを作成することで、コードの意図を明確にできます。

### 具体例

#### 例1: 複数値の返却の問題

```python
# 悪い例（複数値の返却）
def get_user_stats_bad(user_id):
    """ユーザー統計を取得（複数値の返却）"""
    # 複数の値を返す
    return user_id, 'Alice', 25, 'alice@example.com', 'active', 100

# 良い例（専用の結果オブジェクト）
class UserStats:
    """ユーザー統計クラス"""
    def __init__(self, user_id, name, age, email, status, score):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.email = email
        self.status = status
        self.score = score
    
    def __str__(self):
        return f"UserStats(user_id={self.user_id}, name={self.name}, age={self.age})"

def get_user_stats_good(user_id):
    """ユーザー統計を取得（専用の結果オブジェクト）"""
    return UserStats(user_id, 'Alice', 25, 'alice@example.com', 'active', 100)

# 使用例
print("=== 悪い例（複数値の返却） ===")
user_id, name, age, email, status, score = get_user_stats_bad(1)
print(f"ユーザー: {name}, 年齢: {age}, ステータス: {status}")

print("\n=== 良い例（専用の結果オブジェクト） ===")
stats = get_user_stats_good(1)
print(f"ユーザー: {stats.name}, 年齢: {stats.age}, ステータス: {stats.status}")
print(f"完全な統計: {stats}")
```

#### 例2: データベース操作での結果オブジェクト

```python
# データベース操作での結果オブジェクト
class QueryResult:
    """クエリ結果クラス"""
    def __init__(self, success, data=None, error=None, execution_time=0):
        self.success = success
        self.data = data
        self.error = error
        self.execution_time = execution_time
    
    def is_successful(self):
        """成功したかどうか"""
        return self.success
    
    def get_data(self):
        """データを取得"""
        return self.data
    
    def get_error(self):
        """エラーを取得"""
        return self.error

class DatabaseQuery:
    """データベースクエリクラス"""
    
    def execute_query(self, query):
        """クエリを実行"""
        try:
            # 実際のクエリ実行をシミュレート
            data = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
            execution_time = 0.1
            return QueryResult(True, data, None, execution_time)
        except Exception as e:
            return QueryResult(False, None, str(e), 0)
    
    def get_user_by_id(self, user_id):
        """ユーザーIDでユーザーを取得"""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.execute_query(query)

# 使用例
db_query = DatabaseQuery()
result = db_query.get_user_by_id(1)

if result.is_successful():
    print(f"クエリ成功: {result.get_data()}")
    print(f"実行時間: {result.execution_time}秒")
else:
    print(f"クエリエラー: {result.get_error()}")
```

#### 例3: ファイル処理での結果オブジェクト

```python
# ファイル処理での結果オブジェクト
class FileProcessResult:
    """ファイル処理結果クラス"""
    def __init__(self, success, lines_processed=0, errors=None, file_size=0):
        self.success = success
        self.lines_processed = lines_processed
        self.errors = errors or []
        self.file_size = file_size
    
    def has_errors(self):
        """エラーがあるかどうか"""
        return len(self.errors) > 0
    
    def get_error_summary(self):
        """エラーサマリーを取得"""
        return f"エラー数: {len(self.errors)}"

class FileProcessor:
    """ファイル処理クラス"""
    
    def process_file(self, filename):
        """ファイルを処理"""
        try:
            # ファイル処理をシミュレート
            lines = ['Hello', 'World', 'Python']
            file_size = 100
            return FileProcessResult(True, len(lines), [], file_size)
        except Exception as e:
            return FileProcessResult(False, 0, [str(e)], 0)
    
    def process_multiple_files(self, filenames):
        """複数ファイルを処理"""
        results = []
        for filename in filenames:
            result = self.process_file(filename)
            results.append(result)
        return results

# 使用例
file_processor = FileProcessor()
result = file_processor.process_file('test.txt')

if result.success:
    print(f"ファイル処理成功: {result.lines_processed}行処理")
    print(f"ファイルサイズ: {result.file_size}バイト")
else:
    print(f"ファイル処理エラー: {result.get_error_summary()}")
```

### よくある間違い

1. **複数値の返却**: 3つ以上の値を返す
2. **結果オブジェクトの不使用**: 複雑な結果を適切に構造化しない
3. **可読性の軽視**: アンパックの可読性を考慮しない

### 応用例

```python
# API操作での結果オブジェクト
class APIResponse:
    """APIレスポンスクラス"""
    def __init__(self, status_code, data=None, error=None, headers=None):
        self.status_code = status_code
        self.data = data
        self.error = error
        self.headers = headers or {}
    
    def is_successful(self):
        """成功したかどうか"""
        return 200 <= self.status_code < 300
    
    def get_data(self):
        """データを取得"""
        return self.data
    
    def get_error(self):
        """エラーを取得"""
        return self.error

class APIClient:
    """APIクライアントクラス"""
    
    def get_user(self, user_id):
        """ユーザーを取得"""
        try:
            # API呼び出しをシミュレート
            data = {'id': user_id, 'name': 'Alice', 'email': 'alice@example.com'}
            return APIResponse(200, data, None, {'Content-Type': 'application/json'})
        except Exception as e:
            return APIResponse(500, None, str(e))
    
    def create_user(self, user_data):
        """ユーザーを作成"""
        try:
            # API呼び出しをシミュレート
            created_data = {**user_data, 'id': 123}
            return APIResponse(201, created_data, None)
        except Exception as e:
            return APIResponse(400, None, str(e))

# 使用例
api_client = APIClient()

# ユーザー取得
user_response = api_client.get_user(1)
if user_response.is_successful():
    print(f"ユーザー取得成功: {user_response.get_data()}")
else:
    print(f"ユーザー取得エラー: {user_response.get_error()}")

# ユーザー作成
new_user_data = {'name': 'Bob', 'email': 'bob@example.com'}
create_response = api_client.create_user(new_user_data)
if create_response.is_successful():
    print(f"ユーザー作成成功: {create_response.get_data()}")
else:
    print(f"ユーザー作成エラー: {create_response.get_error()}")
```

### ベストプラクティス

- 3つ以上の値を返す場合は専用の結果オブジェクトを作成する
- 結果オブジェクトには適切なメソッドを提供する
- エラーハンドリングを適切に行う
- コードの可読性を優先する

---

## 3. Noneを返すよりも例外を発生させることを好む

### 基本概念

関数が失敗した場合に`None`を返すよりも、適切な例外を発生させることで、エラーの原因を明確にし、呼び出し側でのエラーハンドリングを改善できます。

### 具体例

#### 例1: Noneを返す問題

```python
# 悪い例（Noneを返す）
def find_user_bad(user_id, users):
    """ユーザーを検索（Noneを返す）"""
    for user in users:
        if user['id'] == user_id:
            return user
    return None  # 見つからない場合

# 良い例（例外を発生させる）
def find_user_good(user_id, users):
    """ユーザーを検索（例外を発生させる）"""
    for user in users:
        if user['id'] == user_id:
            return user
    raise ValueError(f"ユーザーID {user_id} が見つかりません")

# 使用例
users = [
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
    {'id': 3, 'name': 'Charlie'}
]

print("=== 悪い例（Noneを返す） ===")
user = find_user_bad(1, users)
if user is not None:
    print(f"ユーザー: {user['name']}")
else:
    print("ユーザーが見つかりません")

# 存在しないユーザー
user = find_user_bad(999, users)
if user is not None:
    print(f"ユーザー: {user['name']}")
else:
    print("ユーザーが見つかりません")

print("\n=== 良い例（例外を発生させる） ===")
try:
    user = find_user_good(1, users)
    print(f"ユーザー: {user['name']}")
except ValueError as e:
    print(f"エラー: {e}")

# 存在しないユーザー
try:
    user = find_user_good(999, users)
    print(f"ユーザー: {user['name']}")
except ValueError as e:
    print(f"エラー: {e}")
```

#### 例2: データベース操作での例外処理

```python
# データベース操作での例外処理
class DatabaseError(Exception):
    """データベースエラークラス"""
    pass

class UserNotFoundError(DatabaseError):
    """ユーザーが見つからないエラー"""
    pass

class DatabaseConnectionError(DatabaseError):
    """データベース接続エラー"""
    pass

class UserRepository:
    """ユーザーリポジトリクラス"""
    
    def __init__(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ]
    
    def find_by_id(self, user_id):
        """IDでユーザーを検索"""
        for user in self.users:
            if user['id'] == user_id:
                return user
        raise UserNotFoundError(f"ユーザーID {user_id} が見つかりません")
    
    def find_by_email(self, email):
        """メールアドレスでユーザーを検索"""
        for user in self.users:
            if user['email'] == email:
                return user
        raise UserNotFoundError(f"メールアドレス {email} のユーザーが見つかりません")
    
    def save(self, user_data):
        """ユーザーを保存"""
        try:
            # 保存処理をシミュレート
            new_id = max(user['id'] for user in self.users) + 1
            user_data['id'] = new_id
            self.users.append(user_data)
            return user_data
        except Exception as e:
            raise DatabaseError(f"ユーザーの保存に失敗しました: {e}")

# 使用例
user_repo = UserRepository()

# 正常なケース
try:
    user = user_repo.find_by_id(1)
    print(f"ユーザー: {user['name']}")
except UserNotFoundError as e:
    print(f"ユーザーが見つかりません: {e}")

# 存在しないユーザー
try:
    user = user_repo.find_by_id(999)
    print(f"ユーザー: {user['name']}")
except UserNotFoundError as e:
    print(f"ユーザーが見つかりません: {e}")

# ユーザー保存
try:
    new_user = user_repo.save({'name': 'Charlie', 'email': 'charlie@example.com'})
    print(f"新しいユーザー: {new_user}")
except DatabaseError as e:
    print(f"保存エラー: {e}")
```

#### 例3: ファイル処理での例外処理

```python
# ファイル処理での例外処理
class FileProcessingError(Exception):
    """ファイル処理エラークラス"""
    pass

class FileNotFoundError(FileProcessingError):
    """ファイルが見つからないエラー"""
    pass

class FilePermissionError(FileProcessingError):
    """ファイル権限エラー"""
    pass

class FileProcessor:
    """ファイル処理クラス"""
    
    def read_file(self, filename):
        """ファイルを読み込み"""
        try:
            # ファイル読み込みをシミュレート
            if filename == 'nonexistent.txt':
                raise FileNotFoundError(f"ファイル {filename} が見つかりません")
            elif filename == 'protected.txt':
                raise FilePermissionError(f"ファイル {filename} へのアクセス権限がありません")
            else:
                return f"ファイル {filename} の内容"
        except FileNotFoundError:
            raise
        except FilePermissionError:
            raise
        except Exception as e:
            raise FileProcessingError(f"ファイル処理中にエラーが発生しました: {e}")
    
    def write_file(self, filename, content):
        """ファイルに書き込み"""
        try:
            # ファイル書き込みをシミュレート
            if filename == 'readonly.txt':
                raise FilePermissionError(f"ファイル {filename} は読み取り専用です")
            else:
                return f"ファイル {filename} に書き込み完了"
        except FilePermissionError:
            raise
        except Exception as e:
            raise FileProcessingError(f"ファイル書き込み中にエラーが発生しました: {e}")

# 使用例
file_processor = FileProcessor()

# 正常なファイル読み込み
try:
    content = file_processor.read_file('normal.txt')
    print(f"読み込み成功: {content}")
except FileProcessingError as e:
    print(f"ファイル処理エラー: {e}")

# 存在しないファイル
try:
    content = file_processor.read_file('nonexistent.txt')
    print(f"読み込み成功: {content}")
except FileNotFoundError as e:
    print(f"ファイルが見つかりません: {e}")

# 権限のないファイル
try:
    content = file_processor.read_file('protected.txt')
    print(f"読み込み成功: {content}")
except FilePermissionError as e:
    print(f"権限エラー: {e}")
```

### よくある間違い

1. **Noneの返却**: エラー時に`None`を返す
2. **例外の不使用**: 適切な例外を発生させない
3. **エラーハンドリングの不備**: 呼び出し側でのエラーハンドリングを考慮しない

### 応用例

```python
# API操作での例外処理
class APIError(Exception):
    """APIエラークラス"""
    pass

class APIResponseError(APIError):
    """APIレスポンスエラー"""
    pass

class APITimeoutError(APIError):
    """APIタイムアウトエラー"""
    pass

class APIClient:
    """APIクライアントクラス"""
    
    def get_user(self, user_id):
        """ユーザーを取得"""
        try:
            # API呼び出しをシミュレート
            if user_id == 999:
                raise APIResponseError(f"ユーザーID {user_id} は存在しません")
            elif user_id == 0:
                raise APITimeoutError("API呼び出しがタイムアウトしました")
            else:
                return {'id': user_id, 'name': 'Alice', 'email': 'alice@example.com'}
        except APIResponseError:
            raise
        except APITimeoutError:
            raise
        except Exception as e:
            raise APIError(f"API呼び出し中にエラーが発生しました: {e}")
    
    def create_user(self, user_data):
        """ユーザーを作成"""
        try:
            # API呼び出しをシミュレート
            if 'email' not in user_data:
                raise APIResponseError("メールアドレスが必須です")
            else:
                return {'id': 123, **user_data}
        except APIResponseError:
            raise
        except Exception as e:
            raise APIError(f"ユーザー作成中にエラーが発生しました: {e}")

# 使用例
api_client = APIClient()

# 正常なユーザー取得
try:
    user = api_client.get_user(1)
    print(f"ユーザー取得成功: {user}")
except APIError as e:
    print(f"APIエラー: {e}")

# 存在しないユーザー
try:
    user = api_client.get_user(999)
    print(f"ユーザー取得成功: {user}")
except APIResponseError as e:
    print(f"APIレスポンスエラー: {e}")

# タイムアウト
try:
    user = api_client.get_user(0)
    print(f"ユーザー取得成功: {user}")
except APITimeoutError as e:
    print(f"APIタイムアウトエラー: {e}")

# ユーザー作成
try:
    new_user = api_client.create_user({'name': 'Bob', 'email': 'bob@example.com'})
    print(f"ユーザー作成成功: {new_user}")
except APIResponseError as e:
    print(f"APIレスポンスエラー: {e}")
```

### ベストプラクティス

- エラー時は適切な例外を発生させる
- 例外の階層を適切に設計する
- 呼び出し側でのエラーハンドリングを考慮する
- エラーメッセージを明確にする

---

## まとめ

Chapter 5では、関数のベストプラクティスを学びました：

1. **引数の変更**: 関数の引数が変更される可能性を理解する
2. **結果オブジェクト**: 複数値の返却には専用の結果オブジェクトを使用する
3. **例外処理**: `None`を返すよりも適切な例外を発生させる
4. **クロージャ**: 変数スコープと`nonlocal`の相互作用を理解する
5. **可変引数**: 視覚的ノイズを減らすために可変位置引数を使用する
6. **キーワード引数**: オプションの動作を提供するためにキーワード引数を使用する
7. **動的デフォルト**: 動的デフォルト引数には`None`とdocstringを使用する
8. **引数の制限**: キーワード専用と位置専用の引数で明確性を強制する
9. **デコレータ**: 関数デコレータを`functools.wraps`で定義する
10. **部分適用**: グルー関数に`lambda`式よりも`functools.partial`を好む

これらの原則を実践することで、効率的で保守性の高い関数を書くことができるようになります。
