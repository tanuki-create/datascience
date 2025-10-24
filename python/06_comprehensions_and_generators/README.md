# Chapter 6: Comprehensions and Generators

リスト内包表記とジェネレータのベストプラクティスを学びます。

## 目次

1. [リスト内包表記でmapとfilterを置き換える](#1-リスト内包表記でmapとfilterを置き換える)
2. [大きな内包表記ではジェネレータ式を好む](#2-大きな内包表記ではジェネレータ式を好む)
3. [yield fromでジェネレータを組み合わせる](#3-yield-fromでジェネレータを組み合わせる)
4. [sendでジェネレータにデータを注入する](#4-sendでジェネレータにデータを注入する)
5. [throwでジェネレータに例外を注入する](#5-throwでジェネレータに例外を注入する)
6. [finallyでジェネレータのクリーンアップを保証する](#6-finallyでジェネレータのクリーンアップを保証する)
7. [itertoolsでイテレータを組み合わせる](#7-itertoolsでイテレータを組み合わせる)

---

## 1. リスト内包表記でmapとfilterを置き換える

### 基本概念

リスト内包表記は`map`と`filter`の組み合わせよりも読みやすく、効率的です。複雑な変換やフィルタリングを簡潔に表現できます。

### 具体例

#### 例1: 基本的な置き換え

```python
# 悪い例（mapとfilterを使用）
def process_numbers_bad(numbers):
    """数値を処理（mapとfilterを使用）"""
    # 偶数を2倍にする
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    doubled_numbers = list(map(lambda x: x * 2, even_numbers))
    return doubled_numbers

# 良い例（リスト内包表記を使用）
def process_numbers_good(numbers):
    """数値を処理（リスト内包表記を使用）"""
    # 偶数を2倍にする
    return [x * 2 for x in numbers if x % 2 == 0]

# 使用例
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("=== 数値処理 ===")
print(f"元の数値: {numbers}")
print(f"悪い例の結果: {process_numbers_bad(numbers)}")
print(f"良い例の結果: {process_numbers_good(numbers)}")

# 文字列処理
words = ['hello', 'world', 'python', 'programming', 'data', 'science']

# 悪い例（mapとfilterを使用）
def process_words_bad(words):
    """単語を処理（mapとfilterを使用）"""
    long_words = list(filter(lambda x: len(x) > 5, words))
    upper_words = list(map(lambda x: x.upper(), long_words))
    return upper_words

# 良い例（リスト内包表記を使用）
def process_words_good(words):
    """単語を処理（リスト内包表記を使用）"""
    return [word.upper() for word in words if len(word) > 5]

print("\n=== 単語処理 ===")
print(f"元の単語: {words}")
print(f"悪い例の結果: {process_words_bad(words)}")
print(f"良い例の結果: {process_words_good(words)}")
```

#### 例2: 複雑な変換

```python
# 複雑な変換でのリスト内包表記
def process_user_data(users):
    """ユーザーデータを処理"""
    # アクティブなユーザーのメールアドレスを大文字に変換
    return [
        user['email'].upper() 
        for user in users 
        if user.get('active', False) and 'email' in user
    ]

# 使用例
users = [
    {'name': 'Alice', 'email': 'alice@example.com', 'active': True},
    {'name': 'Bob', 'email': 'bob@example.com', 'active': False},
    {'name': 'Charlie', 'email': 'charlie@example.com', 'active': True},
    {'name': 'David', 'active': True},  # メールアドレスなし
    {'name': 'Eve', 'email': 'eve@example.com', 'active': True}
]

print("=== ユーザーデータ処理 ===")
print(f"元のユーザー: {users}")
processed_emails = process_user_data(users)
print(f"処理されたメールアドレス: {processed_emails}")

# ネストしたリスト内包表記
def flatten_and_process(matrix):
    """行列を平坦化して処理"""
    return [x * 2 for row in matrix for x in row if x > 0]

# 使用例
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(f"\n=== 行列処理 ===")
print(f"元の行列: {matrix}")
flattened = flatten_and_process(matrix)
print(f"平坦化・処理結果: {flattened}")
```

#### 例3: 条件付き変換

```python
# 条件付き変換でのリスト内包表記
def process_scores(scores):
    """スコアを処理"""
    # スコアに応じて等級を付ける
    return [
        'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D'
        for score in scores
        if score >= 0
    ]

# 使用例
scores = [95, 85, 75, 65, 55, 45, -10, 100]
print("=== スコア処理 ===")
print(f"元のスコア: {scores}")
grades = process_scores(scores)
print(f"等級: {grades}")

# 辞書内包表記
def create_user_dict(users):
    """ユーザー辞書を作成"""
    return {
        user['name']: user['email'] 
        for user in users 
        if 'email' in user
    }

# 使用例
user_dict = create_user_dict(users)
print(f"\n=== ユーザー辞書 ===")
print(f"ユーザー辞書: {user_dict}")

# セット内包表記
def get_unique_domains(emails):
    """一意なドメインを取得"""
    return {
        email.split('@')[1] 
        for email in emails 
        if '@' in email
    }

# 使用例
emails = [
    'alice@example.com',
    'bob@test.com',
    'charlie@example.com',
    'david@test.com',
    'invalid-email'
]
domains = get_unique_domains(emails)
print(f"\n=== ドメイン抽出 ===")
print(f"メールアドレス: {emails}")
print(f"一意なドメイン: {domains}")
```

### よくある間違い

1. **mapとfilterの使用**: リスト内包表記で置き換え可能な場合
2. **複雑な内包表記**: 読みにくくなるほど複雑な内包表記
3. **ネストの過度な使用**: 深すぎるネストした内包表記

### 応用例

```python
# データ処理でのリスト内包表記活用
class DataProcessor:
    """データ処理クラス"""
    
    def __init__(self):
        self.data = []
    
    def add_data(self, items):
        """データを追加"""
        self.data.extend(items)
    
    def filter_and_transform(self, condition_func, transform_func):
        """データをフィルタリングして変換"""
        return [
            transform_func(item) 
            for item in self.data 
            if condition_func(item)
        ]
    
    def group_by_category(self, category_func):
        """カテゴリ別にグループ化"""
        categories = {}
        for item in self.data:
            category = category_func(item)
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        return categories

# 使用例
processor = DataProcessor()
processor.add_data([
    {'name': 'Apple', 'price': 100, 'category': 'fruit'},
    {'name': 'Banana', 'price': 50, 'category': 'fruit'},
    {'name': 'Carrot', 'price': 30, 'category': 'vegetable'},
    {'name': 'Tomato', 'price': 80, 'category': 'vegetable'}
])

# 高価な商品をフィルタリングして価格を2倍にする
expensive_items = processor.filter_and_transform(
    lambda item: item['price'] > 60,
    lambda item: {**item, 'price': item['price'] * 2}
)
print("=== 高価な商品の価格2倍 ===")
for item in expensive_items:
    print(f"{item['name']}: {item['price']}円")

# カテゴリ別にグループ化
categories = processor.group_by_category(lambda item: item['category'])
print(f"\n=== カテゴリ別グループ化 ===")
for category, items in categories.items():
    print(f"{category}: {[item['name'] for item in items]}")
```

### ベストプラクティス

- リスト内包表記で`map`と`filter`を置き換える
- 複雑すぎる場合は通常のループを使用する
- ネストした内包表記は適度に使用する
- 可読性を優先する

---

## 2. 大きな内包表記ではジェネレータ式を好む

### 基本概念

大きなデータセットを処理する場合、リスト内包表記はメモリを大量に消費します。ジェネレータ式を使用することで、メモリ効率を改善できます。

### 具体例

#### 例1: メモリ効率の比較

```python
# 悪い例（リスト内包表記）
def process_large_data_bad(data):
    """大きなデータを処理（リスト内包表記）"""
    # メモリを大量に消費
    processed = [x * 2 for x in data if x > 0]
    return processed

# 良い例（ジェネレータ式）
def process_large_data_good(data):
    """大きなデータを処理（ジェネレータ式）"""
    # メモリ効率的
    return (x * 2 for x in data if x > 0)

# 使用例
import sys

# 大きなデータセットを作成
large_data = list(range(1000000))

print("=== メモリ使用量の比較 ===")

# リスト内包表記
processed_list = [x * 2 for x in large_data if x > 0]
print(f"リスト内包表記のメモリ使用量: {sys.getsizeof(processed_list)} bytes")

# ジェネレータ式
processed_gen = (x * 2 for x in large_data if x > 0)
print(f"ジェネレータ式のメモリ使用量: {sys.getsizeof(processed_gen)} bytes")

# ジェネレータ式の使用
print("\n=== ジェネレータ式の使用 ===")
gen = process_large_data_good(range(10))
for i, value in enumerate(gen):
    print(f"値: {value}")
    if i >= 4:  # 最初の5つのみ表示
        break
```

#### 例2: ファイル処理でのジェネレータ式

```python
# ファイル処理でのジェネレータ式
def process_file_lines(filename):
    """ファイルの行を処理"""
    with open(filename, 'r') as f:
        # ジェネレータ式でメモリ効率的に処理
        return (line.strip().upper() for line in f if line.strip())

def count_words_in_file(filename):
    """ファイル内の単語数をカウント"""
    with open(filename, 'r') as f:
        # ジェネレータ式で単語をカウント
        word_count = sum(
            len(line.split()) 
            for line in f 
            if line.strip()
        )
        return word_count

# 使用例（実際のファイルがない場合のシミュレート）
def simulate_file_processing():
    """ファイル処理をシミュレート"""
    lines = ['hello world', 'python programming', 'data science', 'machine learning']
    
    # ジェネレータ式で処理
    processed_lines = (line.upper() for line in lines if line.strip())
    
    print("=== ファイル処理シミュレート ===")
    for line in processed_lines:
        print(f"処理された行: {line}")
    
    # 単語数カウント
    word_count = sum(len(line.split()) for line in lines if line.strip())
    print(f"総単語数: {word_count}")

simulate_file_processing()
```

#### 例3: データベース操作でのジェネレータ式

```python
# データベース操作でのジェネレータ式
class DatabaseQuery:
    """データベースクエリクラス"""
    
    def __init__(self):
        # シミュレート用のデータ
        self.users = [
            {'id': i, 'name': f'User{i}', 'age': 20 + i, 'active': i % 2 == 0}
            for i in range(100000)
        ]
    
    def get_active_users(self):
        """アクティブなユーザーを取得"""
        # ジェネレータ式でメモリ効率的に処理
        return (
            user for user in self.users 
            if user['active']
        )
    
    def get_users_by_age_range(self, min_age, max_age):
        """年齢範囲でユーザーを取得"""
        return (
            user for user in self.users
            if min_age <= user['age'] <= max_age
        )
    
    def process_users(self, users):
        """ユーザーを処理"""
        # ジェネレータ式で処理
        return (
            {**user, 'processed': True, 'score': user['age'] * 2}
            for user in users
        )

# 使用例
db = DatabaseQuery()

print("=== データベース操作 ===")

# アクティブなユーザーを取得
active_users = db.get_active_users()
print("アクティブなユーザー（最初の5人）:")
for i, user in enumerate(active_users):
    print(f"  {user['name']} (年齢: {user['age']})")
    if i >= 4:
        break

# 年齢範囲でユーザーを取得
young_users = db.get_users_by_age_range(20, 30)
print("\n若いユーザー（最初の5人）:")
for i, user in enumerate(young_users):
    print(f"  {user['name']} (年齢: {user['age']})")
    if i >= 4:
        break

# ユーザーを処理
processed_users = db.process_users(active_users)
print("\n処理されたユーザー（最初の3人）:")
for i, user in enumerate(processed_users):
    print(f"  {user['name']} (スコア: {user['score']})")
    if i >= 2:
        break
```

### よくある間違い

1. **メモリ効率の軽視**: 大きなデータセットでリスト内包表記を使用
2. **ジェネレータの誤用**: 複数回のイテレーションが必要な場合
3. **パフォーマンスの軽視**: メモリとCPUのバランスを考慮しない

### 応用例

```python
# ストリーミング処理でのジェネレータ式
class StreamProcessor:
    """ストリーミング処理クラス"""
    
    def __init__(self):
        self.data_stream = []
    
    def add_data(self, data):
        """データを追加"""
        self.data_stream.append(data)
    
    def process_stream(self, filter_func, transform_func):
        """ストリームを処理"""
        return (
            transform_func(item) 
            for item in self.data_stream 
            if filter_func(item)
        )
    
    def aggregate_data(self, group_func, agg_func):
        """データを集約"""
        groups = {}
        for item in self.data_stream:
            key = group_func(item)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        
        # ジェネレータ式で集約
        return (
            {key: agg_func(items) for key, items in groups.items()}
        )

# 使用例
processor = StreamProcessor()

# データを追加
for i in range(1000):
    processor.add_data({
        'id': i,
        'value': i * 2,
        'category': 'A' if i % 2 == 0 else 'B',
        'timestamp': f'2023-01-01 {i % 24:02d}:00:00'
    })

# ストリームを処理
processed_stream = processor.process_stream(
    lambda item: item['value'] > 100,
    lambda item: {**item, 'processed': True}
)

print("=== ストリーミング処理 ===")
print("処理されたアイテム（最初の5件）:")
for i, item in enumerate(processed_stream):
    print(f"  ID: {item['id']}, 値: {item['value']}, カテゴリ: {item['category']}")
    if i >= 4:
        break

# データを集約
aggregated = processor.aggregate_data(
    lambda item: item['category'],
    lambda items: sum(item['value'] for item in items)
)
print(f"\n集約結果: {aggregated}")
```

### ベストプラクティス

- 大きなデータセットではジェネレータ式を使用する
- メモリ効率を考慮する
- 複数回のイテレーションが必要な場合はリストに変換する
- パフォーマンスを測定して最適化する

---

## まとめ

Chapter 6では、リスト内包表記とジェネレータのベストプラクティスを学びました：

1. **リスト内包表記**: `map`と`filter`を置き換える
2. **ジェネレータ式**: 大きな内包表記でメモリ効率を改善する
3. **yield from**: ジェネレータを組み合わせる
4. **send**: ジェネレータにデータを注入する
5. **throw**: ジェネレータに例外を注入する
6. **finally**: ジェネレータのクリーンアップを保証する
7. **itertools**: イテレータを組み合わせる

これらの原則を実践することで、効率的でメモリ効率の良いコードを書くことができるようになります。

