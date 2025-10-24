# Chapter 1: Pythonic Thinking

Pythonicなコードを書くための基本的な考え方とベストプラクティスを学びます。

## 目次

1. [Pythonのバージョンを把握する](#1-pythonのバージョンを把握する)
2. [PEP 8スタイルガイドに従う](#2-pep-8スタイルガイドに従う)
3. [Pythonがコンパイル時にエラーを検出することを期待しない](#3-pythonがコンパイル時にエラーを検出することを期待しない)
4. [複雑な式の代わりにヘルパー関数を書く](#4-複雑な式の代わりにヘルパー関数を書く)
5. [インデックスアクセスよりも多重代入アンパックを好む](#5-インデックスアクセスよりも多重代入アンパックを好む)
6. [単一要素のタプルには常に括弧を付ける](#6-単一要素のタプルには常に括弧を付ける)
7. [シンプルなインラインロジックには条件式を検討する](#7-シンプルなインラインロジックには条件式を検討する)
8. [代入式で繰り返しを防ぐ](#8-代入式で繰り返しを防ぐ)
9. [フロー制御での構造化にはmatchを検討する](#9-フロー制御での構造化にはmatchを検討する)

---

## 1. Pythonのバージョンを把握する

### 基本概念

Pythonのバージョンによって利用可能な機能や構文が異なります。プロジェクトの互換性を保つため、使用しているPythonのバージョンを明確に把握することが重要です。

### 具体例

#### 例1: バージョン確認の基本

```python
import sys
print(f"Python version: {sys.version}")
print(f"Version info: {sys.version_info}")

# 実行結果例:
# Python version: 3.11.0 (main, Oct 24 2022, 18:26:48) [Clang 14.0.0 (clang-1400.0.29.202)]
# Version info: sys.version_info(major=3, minor=11, micro=0, releaselevel='final', serial=0)
```

#### 例2: バージョン依存の機能使用

```python
import sys

# Python 3.8以降でのみ利用可能な機能
if sys.version_info >= (3, 8):
    from typing import Literal
    def process_status(status: Literal["active", "inactive"]) -> str:
        return f"Status: {status}"
else:
    # 古いバージョン用の代替実装
    def process_status(status: str) -> str:
        if status in ["active", "inactive"]:
            return f"Status: {status}"
        raise ValueError("Invalid status")
```

#### 例3: プロジェクトでのバージョン管理

```python
# requirements.txt での指定例
# Python>=3.8,<4.0

# setup.py での指定例
"""
from setuptools import setup

setup(
    name="my_package",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.20.0",
    ]
)
"""
```

### よくある間違い

1. **バージョン確認を怠る**: 新しい機能を使っているのに古いPythonで実行しようとする
2. **過度な後方互換性**: 古すぎるバージョンに合わせて機能を制限する
3. **バージョン文字列の誤解釈**: `sys.version` と `sys.version_info` の違いを理解していない

### 応用例

```python
# プロジェクトの最小要件チェック
def check_python_version():
    """プロジェクトの最小Python要件をチェック"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        raise RuntimeError(
            f"Python {required_version[0]}.{required_version[1]}+ required, "
            f"but {current_version[0]}.{current_version[1]} found"
        )
    print(f"✓ Python version {current_version[0]}.{current_version[1]} is compatible")

# 実行時チェック
check_python_version()
```

### ベストプラクティス

- プロジェクト開始時に最小Pythonバージョンを明確にする
- `sys.version_info` を使用してバージョン比較を行う
- CI/CDでバージョン互換性をテストする
- 依存関係管理ツール（pipenv, poetry等）を活用する

---

## 2. PEP 8スタイルガイドに従う

### 基本概念

PEP 8はPythonの公式スタイルガイドです。一貫したコーディングスタイルにより、コードの可読性と保守性が向上します。

### 具体例

#### 例1: インデントとスペース

```python
# 良い例
def calculate_total(items):
    """商品の合計金額を計算"""
    total = 0
    for item in items:
        if item.price > 0:
            total += item.price * item.quantity
    return total

# 悪い例
def calculate_total(items):
    total=0
    for item in items:
        if item.price>0:
            total+=item.price*item.quantity
    return total
```

#### 例2: 行の長さと改行

```python
# 良い例（80文字以内）
def process_user_data(user_id, user_name, user_email, user_phone, 
                      user_address, user_preferences):
    """ユーザーデータを処理"""
    return {
        'id': user_id,
        'name': user_name,
        'email': user_email,
        'phone': user_phone,
        'address': user_address,
        'preferences': user_preferences
    }

# 悪い例（長すぎる行）
def process_user_data(user_id, user_name, user_email, user_phone, user_address, user_preferences):
    return {'id': user_id, 'name': user_name, 'email': user_email, 'phone': user_phone, 'address': user_address, 'preferences': user_preferences}
```

#### 例3: インポート文の整理

```python
# 良い例
import os
import sys
from typing import Dict, List, Optional

from mypackage.utils import helper_function
from mypackage.models import User

# 悪い例
import os,sys
from typing import Dict,List,Optional
from mypackage.utils import helper_function
from mypackage.models import User
```

### よくある間違い

1. **インデントの混在**: スペースとタブを混在させる
2. **長すぎる行**: 80文字制限を無視する
3. **不適切な命名**: 変数名に大文字やアンダースコアを不適切に使用

### 応用例

```python
# 設定ファイルでのPEP 8適用例
class DatabaseConfig:
    """データベース設定クラス"""
    
    def __init__(self, host: str, port: int, database: str):
        self.host = host
        self.port = port
        self.database = database
        self.connection_string = f"postgresql://{host}:{port}/{database}"
    
    def get_connection_params(self) -> Dict[str, str]:
        """接続パラメータを取得"""
        return {
            'host': self.host,
            'port': str(self.port),
            'database': self.database
        }
```

### ベストプラクティス

- 自動フォーマッター（black, autopep8）を使用する
- リンター（flake8, pylint）でコード品質をチェックする
- チーム全体でスタイルガイドを統一する
- IDEの設定でPEP 8準拠を自動化する

---

## 3. Pythonがコンパイル時にエラーを検出することを期待しない

### 基本概念

Pythonは動的型付け言語のため、多くのエラーは実行時まで検出されません。コンパイル時にエラーを検出することを期待せず、適切なテストと型ヒントを活用することが重要です。

### 具体例

#### 例1: 型エラーの実行時検出

```python
# このコードは構文的には正しいが、実行時にエラーが発生
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

# 実行時エラー例
try:
    result = calculate_average("hello")  # TypeError: unsupported operand type(s)
except TypeError as e:
    print(f"実行時エラー: {e}")
```

#### 例2: 型ヒントによる改善

```python
from typing import List, Union

def calculate_average(numbers: List[Union[int, float]]) -> float:
    """数値のリストから平均値を計算"""
    if not numbers:
        raise ValueError("空のリストは処理できません")
    return sum(numbers) / len(numbers)

# 型チェッカー（mypy）で検出可能
# calculate_average("hello")  # mypy がエラーを検出
```

#### 例3: 実行時バリデーション

```python
def safe_divide(a: Union[int, float], b: Union[int, float]) -> float:
    """安全な除算を実行"""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("引数は数値である必要があります")
    
    if b == 0:
        raise ValueError("ゼロ除算はできません")
    
    return a / b

# 使用例
try:
    result = safe_divide(10, 2)
    print(f"結果: {result}")
except (TypeError, ValueError) as e:
    print(f"エラー: {e}")
```

### よくある間違い

1. **型チェックの怠慢**: 実行時まで型エラーに気づかない
2. **例外処理の不備**: 予期しない型の引数に対する処理が不十分
3. **動的型付けの過信**: 型の安全性を軽視する

### 応用例

```python
# データ処理での型安全性確保
from typing import Any, Dict, List

class DataProcessor:
    """型安全なデータ処理クラス"""
    
    def __init__(self):
        self.processed_count = 0
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """データを処理し、型安全性を確保"""
        if not isinstance(data, list):
            raise TypeError("データはリストである必要があります")
        
        processed = []
        for item in data:
            if not isinstance(item, dict):
                raise TypeError("各アイテムは辞書である必要があります")
            
            # 型安全な処理
            processed_item = self._validate_and_process(item)
            processed.append(processed_item)
            self.processed_count += 1
        
        return processed
    
    def _validate_and_process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """アイテムの検証と処理"""
        required_fields = ['id', 'name', 'value']
        for field in required_fields:
            if field not in item:
                raise ValueError(f"必須フィールド '{field}' が不足しています")
        
        return {
            'id': str(item['id']),
            'name': str(item['name']),
            'value': float(item['value']) if isinstance(item['value'], (int, float)) else 0.0
        }
```

### ベストプラクティス

- 型ヒントを積極的に使用する
- 静的型チェッカー（mypy）を導入する
- 単体テストで型エラーをカバーする
- 実行時バリデーションを適切に実装する

---

## 4. 複雑な式の代わりにヘルパー関数を書く

### 基本概念

複雑な式は可読性を損ない、デバッグが困難になります。複雑なロジックはヘルパー関数に分離することで、コードの理解と保守が容易になります。

### 具体例

#### 例1: 複雑な条件式の改善

```python
# 悪い例（複雑な式）
def is_valid_user(user):
    return (user is not None and 
            user.age >= 18 and 
            user.email is not None and 
            '@' in user.email and 
            user.email.count('@') == 1 and
            not user.email.startswith('@') and
            not user.email.endswith('@') and
            len(user.password) >= 8 and
            any(c.isupper() for c in user.password) and
            any(c.islower() for c in user.password) and
            any(c.isdigit() for c in user.password))

# 良い例（ヘルパー関数使用）
def is_valid_user(user):
    """ユーザーが有効かどうかを判定"""
    if not _is_user_authenticated(user):
        return False
    if not _is_adult_user(user):
        return False
    if not _is_valid_email(user.email):
        return False
    if not _is_strong_password(user.password):
        return False
    return True

def _is_user_authenticated(user):
    """ユーザーが認証されているか"""
    return user is not None

def _is_adult_user(user):
    """成人ユーザーかどうか"""
    return user.age >= 18

def _is_valid_email(email):
    """有効なメールアドレスかどうか"""
    if not email or '@' not in email:
        return False
    if email.count('@') != 1:
        return False
    if email.startswith('@') or email.endswith('@'):
        return False
    return True

def _is_strong_password(password):
    """強力なパスワードかどうか"""
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit
```

#### 例2: データ処理の複雑な式

```python
# 悪い例
def process_sales_data(sales_list):
    return [s for s in sales_list if s['amount'] > 1000 and s['date'].year >= 2023 and s['customer']['status'] == 'active' and s['product']['category'] in ['electronics', 'books'] and s['region'] in ['Tokyo', 'Osaka']]

# 良い例
def process_sales_data(sales_list):
    """売上データを処理"""
    return [sale for sale in sales_list if _is_high_value_sale(sale)]

def _is_high_value_sale(sale):
    """高額売上かどうかを判定"""
    return (_is_amount_sufficient(sale) and
            _is_recent_sale(sale) and
            _is_active_customer(sale) and
            _is_target_category(sale) and
            _is_target_region(sale))

def _is_amount_sufficient(sale):
    """金額が十分かどうか"""
    return sale['amount'] > 1000

def _is_recent_sale(sale):
    """最近の売上かどうか"""
    return sale['date'].year >= 2023

def _is_active_customer(sale):
    """アクティブな顧客かどうか"""
    return sale['customer']['status'] == 'active'

def _is_target_category(sale):
    """対象カテゴリかどうか"""
    return sale['product']['category'] in ['electronics', 'books']

def _is_target_region(sale):
    """対象地域かどうか"""
    return sale['region'] in ['Tokyo', 'Osaka']
```

#### 例3: 数学的計算の複雑な式

```python
# 悪い例
def calculate_compound_interest(principal, rate, time, n):
    return principal * (1 + rate / n) ** (n * time) - principal

# 良い例
def calculate_compound_interest(principal, rate, time, n):
    """複利計算"""
    if not _is_valid_parameters(principal, rate, time, n):
        raise ValueError("無効なパラメータです")
    
    compound_factor = _calculate_compound_factor(rate, time, n)
    return principal * compound_factor - principal

def _is_valid_parameters(principal, rate, time, n):
    """パラメータが有効かどうか"""
    return (principal > 0 and 
            rate >= 0 and 
            time > 0 and 
            n > 0)

def _calculate_compound_factor(rate, time, n):
    """複利係数を計算"""
    return (1 + rate / n) ** (n * time)
```

### よくある間違い

1. **一行に詰め込みすぎ**: 可読性を犠牲にして簡潔さを追求
2. **ヘルパー関数の過度な分割**: 単純すぎる処理を分割しすぎる
3. **命名の不適切さ**: ヘルパー関数の名前が意図を明確に表現していない

### 応用例

```python
# データ分析での複雑な計算
class DataAnalyzer:
    """データ分析クラス"""
    
    def analyze_customer_segments(self, customers):
        """顧客セグメントを分析"""
        segments = {}
        for customer in customers:
            segment = self._determine_customer_segment(customer)
            if segment not in segments:
                segments[segment] = []
            segments[segment].append(customer)
        return segments
    
    def _determine_customer_segment(self, customer):
        """顧客セグメントを決定"""
        if self._is_high_value_customer(customer):
            return "high_value"
        elif self._is_frequent_customer(customer):
            return "frequent"
        elif self._is_new_customer(customer):
            return "new"
        else:
            return "regular"
    
    def _is_high_value_customer(self, customer):
        """高価値顧客かどうか"""
        return (customer.total_spent > 10000 and
                customer.order_count > 5)
    
    def _is_frequent_customer(self, customer):
        """頻繁な顧客かどうか"""
        return (customer.order_count > 10 and
                customer.last_order_days_ago < 30)
    
    def _is_new_customer(self, customer):
        """新規顧客かどうか"""
        return customer.registration_days_ago < 90
```

### ベストプラクティス

- 複雑な条件は論理的に意味のある単位で分割する
- ヘルパー関数には明確で説明的な名前を付ける
- 単一責任の原則に従って関数を設計する
- テストしやすい単位で関数を分割する

---

## 5. インデックスアクセスよりも多重代入アンパックを好む

### 基本概念

Pythonの多重代入アンパックは、インデックスアクセスよりも読みやすく、エラーが起きにくい方法です。タプルやリストの要素を直接変数に代入できます。

### 具体例

#### 例1: 基本的なアンパック

```python
# 悪い例（インデックスアクセス）
coordinates = (10, 20)
x = coordinates[0]
y = coordinates[1]

# 良い例（アンパック）
coordinates = (10, 20)
x, y = coordinates

# さらに良い例（直接アンパック）
x, y = (10, 20)
```

#### 例2: 複数要素のアンパック

```python
# 悪い例
data = [1, 2, 3, 4, 5]
first = data[0]
second = data[1]
rest = data[2:]

# 良い例
data = [1, 2, 3, 4, 5]
first, second, *rest = data

print(f"最初: {first}, 2番目: {second}, 残り: {rest}")
# 出力: 最初: 1, 2番目: 2, 残り: [3, 4, 5]
```

#### 例3: 辞書の値のアンパック

```python
# 悪い例
user_info = {'name': 'Alice', 'age': 30, 'city': 'Tokyo'}
name = user_info['name']
age = user_info['age']
city = user_info['city']

# 良い例
user_info = {'name': 'Alice', 'age': 30, 'city': 'Tokyo'}
name, age, city = user_info['name'], user_info['age'], user_info['city']

# さらに良い例（辞書の値のみをアンパック）
name, age, city = user_info.values()
```

### よくある間違い

1. **インデックス範囲エラー**: 存在しないインデックスにアクセス
2. **順序の間違い**: インデックスの順序を間違える
3. **アンパックの要素数不一致**: 変数の数と要素の数が合わない

### 応用例

```python
# データベースクエリ結果の処理
def process_query_results(results):
    """クエリ結果を処理"""
    processed_data = []
    for row in results:
        # アンパックで各フィールドを取得
        id, name, email, created_at = row
        processed_data.append({
            'id': id,
            'name': name,
            'email': email,
            'created_at': created_at
        })
    return processed_data

# ファイル処理でのアンパック
def parse_csv_line(line):
    """CSV行を解析"""
    parts = line.strip().split(',')
    if len(parts) >= 3:
        name, age, city = parts[0], parts[1], parts[2]
        return {'name': name, 'age': int(age), 'city': city}
    return None

# 関数の戻り値のアンパック
def get_user_statistics(user_id):
    """ユーザー統計を取得"""
    # 複数の値を返す
    return total_orders, total_spent, last_login

# 使用例
user_id = 123
orders, spent, last_login = get_user_statistics(user_id)
print(f"注文数: {orders}, 支出: {spent}, 最終ログイン: {last_login}")
```

### ベストプラクティス

- インデックスアクセスよりもアンパックを優先する
- アンパックできない場合は適切なエラーハンドリングを実装する
- 変数名は意味のある名前にする
- アンパックの要素数が不明な場合は `*rest` を使用する

---

## 6. 単一要素のタプルには常に括弧を付ける

### 基本概念

Pythonでは、単一要素のタプルを作成する際に括弧を省略すると、タプルではなく単なる値として扱われてしまいます。明示的に括弧を付けることで意図を明確にします。

### 具体例

#### 例1: 基本的な単一要素タプル

```python
# 悪い例（括弧なし）
single_item = 42,  # カンマは必要だが、括弧なしは混乱を招く
print(type(single_item))  # <class 'tuple'>

# 良い例（括弧あり）
single_item = (42,)  # 明確で読みやすい
print(type(single_item))  # <class 'tuple'>

# 間違いやすい例
not_tuple = (42)  # これはタプルではない
print(type(not_tuple))  # <class 'int'>
```

#### 例2: 関数の戻り値としての単一要素タプル

```python
# 悪い例
def get_user_id():
    return 123,  # カンマだけでは意図が不明確

# 良い例
def get_user_id():
    return (123,)  # 明示的にタプルを返すことを示す

# 使用例
user_id, = get_user_id()  # アンパックで受け取る
print(f"User ID: {user_id}")
```

#### 例3: データ構造での単一要素タプル

```python
# 設定データでの使用例
class Config:
    """設定クラス"""
    
    def __init__(self):
        # 単一要素のタプルで設定を保持
        self.allowed_extensions = ('.txt',)  # 明示的にタプル
        self.database_ports = (5432,)  # 明示的にタプル
    
    def is_allowed_extension(self, filename):
        """許可された拡張子かどうか"""
        return filename.endswith(self.allowed_extensions)
```

### よくある間違い

1. **括弧の省略**: `(42)` と `(42,)` の違いを理解していない
2. **意図しない型**: タプルを期待しているのに値が返される
3. **アンパックエラー**: 単一要素タプルのアンパック方法を間違える

### 応用例

```python
# APIレスポンスの処理
class APIResponse:
    """APIレスポンスクラス"""
    
    def __init__(self, data):
        self.data = data
    
    def get_single_result(self):
        """単一の結果をタプルで返す"""
        if len(self.data) == 1:
            return (self.data[0],)  # 明示的にタプル
        elif len(self.data) > 1:
            return tuple(self.data)  # 複数要素のタプル
        else:
            return ()  # 空のタプル

# 使用例
response = APIResponse([42])
result, = response.get_single_result()  # アンパックで受け取り
print(f"結果: {result}")

# データベース操作での使用
def execute_single_query(query):
    """単一クエリを実行"""
    results = database.execute(query)
    if results:
        return (results[0],)  # 単一結果をタプルで返す
    return ()  # 空のタプル

# 使用例
result, = execute_single_query("SELECT name FROM users WHERE id = 1")
print(f"ユーザー名: {result}")
```

### ベストプラクティス

- 単一要素タプルには常に括弧とカンマを付ける
- 関数の戻り値でタプルを返す場合は明示的にする
- アンパック時は要素数を確認する
- 型ヒントでタプルを明示する

---

## 7. シンプルなインラインロジックには条件式を検討する

### 基本概念

Pythonの条件式（三項演算子）は、シンプルな条件分岐を一行で表現できます。複雑すぎない場合に使用することで、コードを簡潔にできます。

### 具体例

#### 例1: 基本的な条件式

```python
# 悪い例（冗長なif文）
def get_status(is_active):
    if is_active:
        return "active"
    else:
        return "inactive"

# 良い例（条件式）
def get_status(is_active):
    return "active" if is_active else "inactive"

# 使用例
status = get_status(True)
print(f"ステータス: {status}")  # 出力: ステータス: active
```

#### 例2: 数値計算での条件式

```python
# 悪い例
def calculate_discount(price, is_member):
    if is_member:
        return price * 0.9
    else:
        return price

# 良い例
def calculate_discount(price, is_member):
    return price * 0.9 if is_member else price

# 使用例
member_price = calculate_discount(1000, True)
regular_price = calculate_discount(1000, False)
print(f"会員価格: {member_price}, 通常価格: {regular_price}")
```

#### 例3: 文字列処理での条件式

```python
# 悪い例
def format_message(name, is_vip):
    if is_vip:
        return f"VIP {name}様、ようこそ！"
    else:
        return f"{name}さん、ようこそ！"

# 良い例
def format_message(name, is_vip):
    return f"VIP {name}様、ようこそ！" if is_vip else f"{name}さん、ようこそ！"

# 使用例
message1 = format_message("Alice", True)
message2 = format_message("Bob", False)
print(message1)  # 出力: VIP Alice様、ようこそ！
print(message2)  # 出力: Bobさん、ようこそ！
```

### よくある間違い

1. **過度な複雑化**: 条件式をネストしすぎて可読性を損なう
2. **副作用の混入**: 条件式内で副作用のある処理を行う
3. **適切でない使用**: 複雑なロジックに条件式を使用する

### 応用例

```python
# データ処理での条件式活用
class DataProcessor:
    """データ処理クラス"""
    
    def process_item(self, item, is_premium=False):
        """アイテムを処理"""
        # 条件式でデフォルト値を設定
        priority = "high" if is_premium else "normal"
        
        # 条件式で処理方法を決定
        processor = self._get_premium_processor if is_premium else self._get_standard_processor
        
        return {
            'item': item,
            'priority': priority,
            'processed_by': processor.__name__
        }
    
    def _get_premium_processor(self):
        return "premium_processor"
    
    def _get_standard_processor(self):
        return "standard_processor"

# 設定管理での条件式
class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, environment):
        self.environment = environment
    
    def get_database_url(self):
        """環境に応じたデータベースURLを取得"""
        return (
            "postgresql://prod:password@prod-db:5432/app" if self.environment == "production"
            else "postgresql://dev:password@dev-db:5432/app"
        )
    
    def get_log_level(self):
        """環境に応じたログレベルを取得"""
        return "ERROR" if self.environment == "production" else "DEBUG"
```

### ベストプラクティス

- シンプルな条件分岐にのみ使用する
- ネストは避け、複雑な場合は通常のif文を使用する
- 可読性を最優先に考える
- 条件式内では副作用のある処理を避ける

---

## 8. 代入式で繰り返しを防ぐ

### 基本概念

Python 3.8で導入された代入式（`:=`）を使用することで、式の中で変数に代入し、その値を再利用できます。これにより、重複した計算や処理を避けることができます。

### 具体例

#### 例1: 基本的な代入式

```python
# 悪い例（重複した処理）
def process_data(data):
    if len(data) > 10:
        return data[:10] + "..."
    return data

# 良い例（代入式使用）
def process_data(data):
    if (length := len(data)) > 10:
        return data[:10] + "..."
    return data

# さらに良い例
def process_data(data):
    return data[:10] + "..." if (length := len(data)) > 10 else data
```

#### 例2: 正規表現での代入式

```python
import re

# 悪い例（重複したマッチング）
def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    if match:
        return match.group()
    return None

# 良い例（代入式使用）
def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if match := re.search(email_pattern, text):
        return match.group()
    return None
```

#### 例3: ファイル処理での代入式

```python
# 悪い例（重複したファイル読み込み）
def process_large_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    if len(content) > 1000:
        return content[:1000] + "..."
    return content

# 良い例（代入式使用）
def process_large_file(filename):
    with open(filename, 'r') as f:
        if (content := f.read()) and len(content) > 1000:
            return content[:1000] + "..."
        return content
```

### よくある間違い

1. **過度な使用**: すべての場面で代入式を使用する
2. **可読性の低下**: 複雑すぎる代入式でコードが読みにくくなる
3. **スコープの誤解**: 代入式の変数のスコープを理解していない

### 応用例

```python
# データベースクエリでの代入式活用
class DatabaseManager:
    """データベース管理クラス"""
    
    def find_user_by_email(self, email):
        """メールアドレスでユーザーを検索"""
        query = "SELECT * FROM users WHERE email = %s"
        if result := self.execute_query(query, (email,)):
            return result[0] if result else None
        return None
    
    def get_user_statistics(self, user_id):
        """ユーザー統計を取得"""
        # 複数のクエリを効率的に実行
        if user := self.find_user_by_id(user_id):
            if orders := self.get_user_orders(user_id):
                return {
                    'user': user,
                    'order_count': len(orders),
                    'total_spent': sum(order['amount'] for order in orders)
                }
        return None

# 設定処理での代入式
class ConfigLoader:
    """設定ローダー"""
    
    def load_config(self, config_file):
        """設定ファイルを読み込み"""
        import json
        
        try:
            with open(config_file, 'r') as f:
                if config := json.load(f):
                    # 設定の検証
                    if (db_config := config.get('database')) and db_config.get('host'):
                        return config
                    else:
                        raise ValueError("データベース設定が不完全です")
        except FileNotFoundError:
            return self._get_default_config()
        except json.JSONDecodeError:
            raise ValueError("設定ファイルの形式が正しくありません")
```

### ベストプラクティス

- 重複した処理を避ける場合に使用する
- 可読性を損なわない範囲で使用する
- 複雑な条件式では通常のif文を使用する
- 代入式の変数名は意味のある名前にする

---

## 9. フロー制御での構造化にはmatchを検討する

### 基本概念

Python 3.10で導入された`match`文は、パターンマッチングによる構造化されたフロー制御を提供します。複雑な条件分岐をより読みやすく、保守しやすくできます。

### 具体例

#### 例1: 基本的なmatch文

```python
# 悪い例（複雑なif文）
def handle_status(status):
    if status == "success":
        return "処理が完了しました"
    elif status == "error":
        return "エラーが発生しました"
    elif status == "pending":
        return "処理中です"
    elif status == "cancelled":
        return "処理がキャンセルされました"
    else:
        return "不明なステータスです"

# 良い例（match文使用）
def handle_status(status):
    match status:
        case "success":
            return "処理が完了しました"
        case "error":
            return "エラーが発生しました"
        case "pending":
            return "処理中です"
        case "cancelled":
            return "処理がキャンセルされました"
        case _:
            return "不明なステータスです"
```

#### 例2: パターンマッチングでの構造化

```python
# データ構造の処理
def process_data(data):
    match data:
        case {"type": "user", "name": name, "age": age}:
            return f"ユーザー: {name} ({age}歳)"
        case {"type": "product", "name": name, "price": price}:
            return f"商品: {name} (¥{price:,})"
        case {"type": "order", "id": order_id, "items": items}:
            return f"注文 #{order_id}: {len(items)}点"
        case _:
            return "不明なデータタイプです"

# 使用例
user_data = {"type": "user", "name": "Alice", "age": 30}
product_data = {"type": "product", "name": "Laptop", "price": 100000}
order_data = {"type": "order", "id": 12345, "items": ["item1", "item2"]}

print(process_data(user_data))    # 出力: ユーザー: Alice (30歳)
print(process_data(product_data)) # 出力: 商品: Laptop (¥100,000)
print(process_data(order_data))  # 出力: 注文 #12345: 2点
```

#### 例3: 複雑な条件でのmatch文

```python
# HTTPステータスコードの処理
def handle_http_response(response):
    match response:
        case {"status": 200, "data": data}:
            return f"成功: {data}"
        case {"status": 404}:
            return "リソースが見つかりません"
        case {"status": 500, "error": error}:
            return f"サーバーエラー: {error}"
        case {"status": status} if 400 <= status < 500:
            return f"クライアントエラー: {status}"
        case {"status": status} if 500 <= status < 600:
            return f"サーバーエラー: {status}"
        case _:
            return "不明なレスポンスです"

# 使用例
responses = [
    {"status": 200, "data": "Hello World"},
    {"status": 404},
    {"status": 500, "error": "Database connection failed"},
    {"status": 400}
]

for response in responses:
    print(handle_http_response(response))
```

### よくある間違い

1. **過度な使用**: シンプルな条件分岐にmatch文を使用する
2. **パターンの複雑化**: パターンを複雑にしすぎて可読性を損なう
3. **Python 3.10未満での使用**: 古いバージョンでmatch文を使用する

### 応用例

```python
# API レスポンス処理でのmatch文活用
class APIHandler:
    """APIハンドラー"""
    
    def handle_response(self, response):
        """APIレスポンスを処理"""
        match response:
            case {"status": "success", "data": data, "pagination": pagination}:
                return self._handle_success_with_pagination(data, pagination)
            case {"status": "success", "data": data}:
                return self._handle_success(data)
            case {"status": "error", "message": message, "code": code}:
                return self._handle_error(message, code)
            case {"status": "error", "message": message}:
                return self._handle_error(message)
            case _:
                return self._handle_unknown_response(response)
    
    def _handle_success_with_pagination(self, data, pagination):
        """ページネーション付きの成功レスポンスを処理"""
        return {
            "data": data,
            "has_more": pagination.get("has_more", False),
            "next_page": pagination.get("next_page")
        }
    
    def _handle_success(self, data):
        """成功レスポンスを処理"""
        return {"data": data}
    
    def _handle_error(self, message, code=None):
        """エラーレスポンスを処理"""
        error_info = {"message": message}
        if code:
            error_info["code"] = code
        return error_info
    
    def _handle_unknown_response(self, response):
        """不明なレスポンスを処理"""
        return {"error": "Unknown response format", "response": response}
```

### ベストプラクティス

- 複雑な条件分岐にmatch文を使用する
- パターンは明確で理解しやすいものにする
- デフォルトケース（`case _:`）を必ず含める
- Python 3.10以降でのみ使用する

---

## まとめ

Chapter 1では、Pythonicなコードを書くための基本的な考え方を学びました：

1. **バージョン管理**: 使用しているPythonのバージョンを明確に把握する
2. **スタイルガイド**: PEP 8に従って一貫したコーディングスタイルを維持する
3. **型安全性**: 動的型付けの特性を理解し、適切な型ヒントとテストを活用する
4. **可読性**: 複雑な式はヘルパー関数に分割し、コードの理解を容易にする
5. **効率性**: アンパックや代入式を活用して、より簡潔で効率的なコードを書く
6. **構造化**: 適切な場面でmatch文を使用し、フロー制御を明確にする

これらの原則を実践することで、保守性が高く、読みやすく、効率的なPythonコードを書くことができるようになります。
