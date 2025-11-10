# 技術者面接コーディング試験問題集

## 目次

1. [フィボナッチ数列](#1-フィボナッチ数列)
2. [関数を返す関数（クロージャ）](#2-関数を返す関数クロージャ)
3. [Maximum Subarray（最大部分配列）](#3-maximum-subarray最大部分配列)
4. [Spiral Matrix（螺旋行列）](#4-spiral-matrix螺旋行列)
5. [N-Queens（Nクイーン問題）](#5-n-queensnクイーン問題)
6. [The Skyline Problem（都市の稜線）](#6-the-skyline-problem都市の稜線)

---

## 1. フィボナッチ数列

### 問題

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55 ... という数列（フィボナッチ数列）を100個目まで表示するプログラムを書いてください。

### 基礎知識

#### フィボナッチ数列とは

フィボナッチ数列は、各項が前2項の和となる数列です。

- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) (n ≥ 2)

#### 数列の特徴

- 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...
- 自然界の現象（花びらの数、螺旋の数など）にも現れる
- 黄金比（約1.618）に収束する

### 解法1: 変数を3つ使う方法（推奨）

**考え方**
- 現在の値、1つ前の値、2つ前の値を保持
- ループで順次計算

**実装**
```python
def fibonacci_loop(n):
    """フィボナッチ数列をn個まで表示"""
    if n <= 0:
        return
    
    # 最初の2項
    if n >= 1:
        print(0)
    if n >= 2:
        print(1)
    
    # 3項目以降
    prev_prev = 0  # 2つ前
    prev = 1      # 1つ前
    
    for i in range(2, n):
        current = prev_prev + prev
        print(current)
        
        # 次のループのために更新
        prev_prev = prev
        prev = current

# 100個目まで表示
fibonacci_loop(100)
```

**メリット**
- メモリ効率が良い（O(1)）
- 計算量が少ない（O(n)）
- 理解しやすい

### 解法2: リストを使う方法

**考え方**
- リストに順次追加していく
- リストの末尾2つの和を次の値とする

**実装**
```python
def fibonacci_list(n):
    """フィボナッチ数列をn個まで表示（リスト使用）"""
    if n <= 0:
        return []
    
    fib = []
    for i in range(n):
        if i == 0:
            fib.append(0)
        elif i == 1:
            fib.append(1)
        else:
            fib.append(fib[i-1] + fib[i-2])
        print(fib[i])
    
    return fib

# 100個目まで表示
fibonacci_list(100)
```

**より簡潔な実装**
```python
def fibonacci_list_simple(n):
    """フィボナッチ数列をn個まで表示（簡潔版）"""
    fib = [0, 1]
    
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    for num in fib[:n]:
        print(num)

fibonacci_list_simple(100)
```

**メリット**
- すべての値を保持できる
- 後で参照できる
- 理解しやすい

**デメリット**
- メモリ使用量が多い（O(n)）

### 解法3: 再帰（非推奨：遅い）

**考え方**
- 定義そのままを実装
- F(n) = F(n-1) + F(n-2)

**実装**
```python
def fibonacci_recursive(n):
    """フィボナッチ数列のn項目を返す（再帰）"""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# 100個目まで表示
for i in range(100):
    print(fibonacci_recursive(i))
```

**問題点**
- 計算量が指数関数的（O(2^n)）
- 100個目まで計算すると非常に遅い
- スタックオーバーフローの可能性

### 解法4: メモ化再帰（最適化）

**考え方**
- 再帰の計算結果をキャッシュ
- 一度計算した値は再利用

**実装**
```python
def fibonacci_memoized(n, memo={}):
    """フィボナッチ数列のn項目を返す（メモ化再帰）"""
    if n in memo:
        return memo[n]
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)
        return memo[n]

# 100個目まで表示
for i in range(100):
    print(fibonacci_memoized(i))
```

**メリット**
- 再帰の考え方を保ちつつ高速
- 計算量: O(n)

### 解法5: functools.lru_cacheを使う（Python標準）

**実装**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_cached(n):
    """フィボナッチ数列のn項目を返す（LRUキャッシュ）"""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_cached(n-1) + fibonacci_cached(n-2)

# 100個目まで表示
for i in range(100):
    print(fibonacci_cached(i))
```

### 推奨解答

面接では、**解法1（変数を3つ使う方法）**が推奨されます。

**理由**
- メモリ効率が良い
- 計算が高速
- コードがシンプル
- 理解しやすい

**完全な解答例**
```python
def fibonacci(n):
    """フィボナッチ数列をn個目まで表示"""
    if n <= 0:
        return
    
    # 最初の2項
    if n >= 1:
        print(0)
    if n >= 2:
        print(1)
    
    # 3項目以降を計算
    prev_prev = 0
    prev = 1
    
    for i in range(2, n):
        current = prev_prev + prev
        print(current)
        prev_prev = prev
        prev = current

# 実行
fibonacci(100)
```

### 面接でのポイント

1. **複数の解法を説明できる**: ループ、リスト、再帰など
2. **計算量を理解している**: O(n) vs O(2^n)
3. **メモリ効率を考慮できる**: O(1) vs O(n)
4. **エッジケースを考慮**: n=0, n=1の場合

---

## 2. 関数を返す関数（クロージャ）

### 問題

次のように動作する関数 `adder` を作ってください。

```python
>>> a = adder(10)
>>> a(3)
13
>>> a(8)
18
```

### 基礎知識

#### クロージャとは

クロージャは、外部スコープの変数を参照する内部関数です。

**基本的な例**
```python
def outer(x):
    def inner(y):
        return x + y
    return inner

func = outer(10)
print(func(3))  # 13
```

#### 関数もオブジェクト

Pythonでは、関数もオブジェクトです。

```python
def add(a, b):
    return a + b

# 関数を変数に代入
my_func = add
print(my_func(3, 5))  # 8

# 関数を返す
def get_adder():
    return add

adder_func = get_adder()
print(adder_func(3, 5))  # 8
```

### 解法1: 基本的なクロージャ

**実装**
```python
def adder(x):
    """xを加算する関数を返す"""
    def inner(y):
        return x + y
    return inner

# 使用例
a = adder(10)
print(a(3))  # 13
print(a(8))  # 18
```

**動作の説明**
1. `adder(10)` が呼ばれる
2. `inner` 関数が定義される（この時点で `x=10` を参照）
3. `inner` 関数が返される
4. `a(3)` が呼ばれると、`inner(3)` が実行され、`10 + 3 = 13` を返す

### 解法2: lambda式を使う

**実装**
```python
def adder(x):
    """xを加算する関数を返す（lambda版）"""
    return lambda y: x + y

# 使用例
a = adder(10)
print(a(3))  # 13
print(a(8))  # 18
```

**メリット**
- より簡潔
- 関数型プログラミングのスタイル

### 解法3: クラスで実装

**実装**
```python
class Adder:
    def __init__(self, x):
        self.x = x
    
    def __call__(self, y):
        return self.x + y

# 使用例
a = Adder(10)
print(a(3))  # 13
print(a(8))  # 18
```

**説明**
- `__call__` メソッドにより、インスタンスを関数のように呼び出せる

### 応用: 複数の値を保持するクロージャ

**実装**
```python
def adder(x):
    """xを加算する関数を返す（累積版）"""
    total = x
    
    def inner(y):
        nonlocal total
        total += y
        return total
    return inner

# 使用例
a = adder(10)
print(a(3))   # 13 (10 + 3)
print(a(8))   # 21 (13 + 8)
print(a(5))   # 26 (21 + 5)
```

**ポイント**
- `nonlocal` で外部変数を変更可能にする

### 推奨解答

面接では、**解法1（基本的なクロージャ）**が推奨されます。

**理由**
- 理解しやすい
- クロージャの概念を明確に示せる
- 応用が効く

**完全な解答例**
```python
def adder(x):
    """xを加算する関数を返す"""
    def inner(y):
        return x + y
    return inner

# 動作確認
a = adder(10)
assert a(3) == 13
assert a(8) == 18
```

### 面接でのポイント

1. **クロージャの概念を理解している**: 外部スコープの変数を参照
2. **関数がオブジェクトであることを理解**: 関数を返すことができる
3. **型を説明できる**: `adder` は `int -> (int -> int)` の型
4. **実用例を説明できる**: デコレータ、部分適用など

---

## 3. Maximum Subarray（最大部分配列）

### 問題

与えられた整数の配列 `nums` の中から、連続する一部（subarray）を取り出して合計した際に最大となる部分の合計値を取得しなさい。

**例**
```
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6

Explanation: The subarray [4,-1,2,1] has the largest sum 6.
```

### 基礎知識

#### 部分配列（Subarray）とは

配列の連続する要素の部分列です。

**例**: `[1, 2, 3, 4]` の部分配列
- `[1]`, `[2]`, `[3]`, `[4]`
- `[1, 2]`, `[2, 3]`, `[3, 4]`
- `[1, 2, 3]`, `[2, 3, 4]`
- `[1, 2, 3, 4]`

**注意**: `[1, 3]` は部分配列ではない（連続していない）

### 解法1: ブルートフォース（全探索）

**考え方**
- すべての部分配列を生成
- それぞれの合計を計算
- 最大値を返す

**実装**
```python
def max_subarray_bruteforce(nums):
    """最大部分配列の合計（ブルートフォース）"""
    if not nums:
        return 0
    
    max_sum = float('-inf')
    n = len(nums)
    
    # すべての部分配列を探索
    for i in range(n):
        for j in range(i, n):
            # 部分配列 nums[i:j+1] の合計
            current_sum = sum(nums[i:j+1])
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# テスト
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_bruteforce(nums))  # 6
```

**計算量**: O(n³)
- 外側のループ: O(n)
- 内側のループ: O(n)
- sum(): O(n)

### 解法2: ブルートフォース（最適化）

**考え方**
- 合計を累積的に計算
- sum()を呼ばない

**実装**
```python
def max_subarray_optimized(nums):
    """最大部分配列の合計（最適化版）"""
    if not nums:
        return 0
    
    max_sum = float('-inf')
    n = len(nums)
    
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += nums[j]  # 累積的に加算
            max_sum = max(max_sum, current_sum)
    
    return max_sum

# テスト
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_optimized(nums))  # 6
```

**計算量**: O(n²)

### 解法3: Kadane's Algorithm（動的計画法）

**考え方**
- 各位置で「ここまでの最大部分配列和」を保持
- 新しい要素を追加するか、新しい部分配列を始めるか

**アルゴリズム**
1. `current_sum`: 現在の部分配列の合計
2. `max_sum`: これまでの最大合計
3. 各要素について:
   - `current_sum = max(nums[i], current_sum + nums[i])`
   - `max_sum = max(max_sum, current_sum)`

**実装**
```python
def max_subarray_kadane(nums):
    """最大部分配列の合計（Kadane's Algorithm）"""
    if not nums:
        return 0
    
    current_sum = nums[0]
    max_sum = nums[0]
    
    for i in range(1, len(nums)):
        # 現在の要素を加えるか、新しい部分配列を始めるか
        current_sum = max(nums[i], current_sum + nums[i])
        # 最大値を更新
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# テスト
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_kadane(nums))  # 6
```

**計算量**: O(n)
**空間計算量**: O(1)

**動作の追跡**
```
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

i=0: current_sum=-2, max_sum=-2
i=1: current_sum=max(1, -2+1)=1, max_sum=max(-2,1)=1
i=2: current_sum=max(-3, 1-3)=-2, max_sum=max(1,-2)=1
i=3: current_sum=max(4, -2+4)=4, max_sum=max(1,4)=4
i=4: current_sum=max(-1, 4-1)=3, max_sum=max(4,3)=4
i=5: current_sum=max(2, 3+2)=5, max_sum=max(4,5)=5
i=6: current_sum=max(1, 5+1)=6, max_sum=max(5,6)=6
i=7: current_sum=max(-5, 6-5)=1, max_sum=max(6,1)=6
i=8: current_sum=max(4, 1+4)=5, max_sum=max(6,5)=6

結果: 6
```

### 解法4: itertoolsを使う（1行で書ける）

**実装**
```python
from itertools import combinations

def max_subarray_itertools(nums):
    """最大部分配列の合計（itertools使用）"""
    if not nums:
        return 0
    
    # すべての連続する部分配列を生成
    n = len(nums)
    max_sum = float('-inf')
    
    for i in range(n):
        for j in range(i+1, n+1):
            max_sum = max(max_sum, sum(nums[i:j]))
    
    return max_sum

# より簡潔に（ただし効率は悪い）
def max_subarray_oneliner(nums):
    """最大部分配列の合計（1行版）"""
    return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i+1, len(nums)+1)) if nums else 0
```

### 推奨解答

面接では、**解法3（Kadane's Algorithm）**が推奨されます。

**理由**
- 計算量が最適（O(n)）
- 空間計算量も最適（O(1)）
- 動的計画法の良い例

**完全な解答例**
```python
def max_subarray(nums):
    """最大部分配列の合計を返す"""
    if not nums:
        return 0
    
    current_sum = nums[0]
    max_sum = nums[0]
    
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# テスト
assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray([1]) == 1
assert max_subarray([5, 4, -1, 7, 8]) == 23
```

### 面接でのポイント

1. **複数の解法を説明できる**: ブルートフォース → 最適化 → Kadane's
2. **計算量を理解している**: O(n³) → O(n²) → O(n)
3. **動的計画法の考え方を説明できる**: 部分問題の最適解を利用
4. **エッジケースを考慮**: 空配列、すべて負の数など

---

## 4. Spiral Matrix（螺旋行列）

### 問題

二次元の表（行列）の各要素を、渦を巻くような順番で表示しなさい。

**例**
```
Input: matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

### 基礎知識

#### 螺旋の動き

外側から内側へ、時計回りに進む:
1. 右 → 2. 下 → 3. 左 → 4. 上 → 1. 右 → ...

### 解法1: 境界を管理する方法

**考え方**
- 4つの境界（top, bottom, left, right）を管理
- 各方向に進みながら境界を縮小

**実装**
```python
def spiral_order(matrix):
    """螺旋順で要素を返す"""
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 右へ
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        
        # 下へ
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # 左へ（まだ行が残っている場合）
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        
        # 上へ（まだ列が残っている場合）
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result

# テスト
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(spiral_order(matrix))  # [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**動作の追跡**
```
初期状態:
top=0, bottom=2, left=0, right=2

1. 右へ: [1, 2, 3] → top=1
2. 下へ: [6, 9] → right=1
3. 左へ: [8, 7] → bottom=1
4. 上へ: [4] → left=1

次のループ:
top=1, bottom=1, left=1, right=1

1. 右へ: [5] → top=2
終了（top > bottom）
```

### 解法2: 方向ベクトルを使う方法

**考え方**
- 方向ベクトル（右、下、左、上）を定義
- 壁に当たったら方向を変える

**実装**
```python
def spiral_order_direction(matrix):
    """螺旋順で要素を返す（方向ベクトル版）"""
    if not matrix or not matrix[0]:
        return []
    
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False] * cols for _ in range(rows)]
    result = []
    
    # 方向ベクトル: 右、下、左、上
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction_index = 0
    
    row, col = 0, 0
    
    for _ in range(rows * cols):
        result.append(matrix[row][col])
        visited[row][col] = True
        
        # 次の位置を計算
        next_row = row + directions[direction_index][0]
        next_col = col + directions[direction_index][1]
        
        # 境界チェックまたは訪問済みチェック
        if (next_row < 0 or next_row >= rows or 
            next_col < 0 or next_col >= cols or 
            visited[next_row][next_col]):
            # 方向を変える
            direction_index = (direction_index + 1) % 4
            next_row = row + directions[direction_index][0]
            next_col = col + directions[direction_index][1]
        
        row, col = next_row, next_col
    
    return result
```

### 解法3: 表を回転させる方法

**考え方**
- 最初の行を取得
- 残りの表を反時計回りに90度回転
- 繰り返す

**実装**
```python
def spiral_order_rotate(matrix):
    """螺旋順で要素を返す（回転版）"""
    result = []
    
    while matrix:
        # 最初の行を追加
        result.extend(matrix[0])
        
        # 残りの行を反時計回りに90度回転
        matrix = list(zip(*matrix[1:]))[::-1] if matrix[1:] else []
    
    return result

# テスト
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(spiral_order_rotate(matrix))  # [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**回転の説明**
```python
# 元の行列
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]

# 最初の行を取得: [1, 2, 3]
# 残りを転置: [[4, 7], [5, 8], [6, 9]]
# 反転: [[6, 9], [5, 8], [4, 7]]
# 再度転置: [[6, 5, 4], [9, 8, 7]]
```

### 推奨解答

面接では、**解法1（境界を管理する方法）**が推奨されます。

**理由**
- 直感的で理解しやすい
- 実装が明確
- エッジケースの処理が容易

**完全な解答例**
```python
def spiral_order(matrix):
    """螺旋順で要素を返す"""
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 右へ
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        
        # 下へ
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # 左へ
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
        
        # 上へ
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result
```

### 面接でのポイント

1. **境界条件を正確に処理**: top, bottom, left, rightの管理
2. **重複を避ける**: 条件チェック（`if top <= bottom`など）
3. **複数の解法を説明できる**: 境界管理、方向ベクトル、回転
4. **エッジケースを考慮**: 空行列、1行のみ、1列のみ

---

## 5. N-Queens（Nクイーン問題）

### 問題

N×Nのチェス盤に、N個のクイーンを配置してください。ただし、どの2つのクイーンも互いに攻撃できないように配置してください。

クイーンは、縦、横、斜めの8方向に移動できます。

**例（4-Queens）**
```
解の1つ:
. Q . .
. . . Q
Q . . .
. . Q .
```

### 基礎知識

#### バックトラッキングとは

バックトラッキングは、解を探索するアルゴリズムです。

1. 候補を試す
2. 制約を満たさない場合、戻る（バックトラック）
3. すべての解を見つけるまで繰り返す

#### クイーンの動き

- 縦方向: 同じ列に他のクイーンがあってはいけない
- 横方向: 同じ行に他のクイーンがあってはいけない
- 斜め方向: 対角線上に他のクイーンがあってはいけない

### 解法: バックトラッキング

**考え方**
1. 各行に1つずつクイーンを配置
2. 各列を試す
3. 制約を満たすかチェック
4. 満たす場合、次の行へ
5. 満たさない場合、次の列を試す
6. すべての行に配置できたら解を記録

**実装**
```python
def solve_n_queens(n):
    """N-Queens問題のすべての解を返す"""
    def is_safe(board, row, col):
        """(row, col)にクイーンを配置できるかチェック"""
        # 同じ列にクイーンがあるかチェック
        for i in range(row):
            if board[i] == col:
                return False
        
        # 左上の対角線をチェック
        for i in range(row):
            if board[i] == col - (row - i):
                return False
        
        # 右上の対角線をチェック
        for i in range(row):
            if board[i] == col + (row - i):
                return False
        
        return True
    
    def backtrack(board, row):
        """バックトラッキングで解を探索"""
        if row == n:
            # 解を見つけた
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                # バックトラック（元に戻す必要はないが、明示的に）
                board[row] = -1
    
    solutions = []
    board = [-1] * n  # board[i] = j は i行目j列目にクイーン
    backtrack(board, 0)
    return solutions

# 解を表示する関数
def print_solution(solution, n):
    """解を視覚的に表示"""
    for row in range(n):
        line = ['.'] * n
        line[solution[row]] = 'Q'
        print(' '.join(line))
    print()

# テスト
n = 4
solutions = solve_n_queens(n)
print(f"{n}-Queens問題の解の数: {len(solutions)}")
for sol in solutions:
    print_solution(sol, n)
```

**最適化版（対角線チェックの改善）**
```python
def solve_n_queens_optimized(n):
    """N-Queens問題のすべての解を返す（最適化版）"""
    def backtrack(board, row, cols, diag1, diag2):
        """バックトラッキング（最適化版）"""
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            # 対角線のインデックスを計算
            d1 = row - col  # 左上から右下の対角線
            d2 = row + col  # 右上から左下の対角線
            
            # 制約チェック
            if cols[col] or diag1[d1] or diag2[d2]:
                continue
            
            # クイーンを配置
            board[row] = col
            cols[col] = True
            diag1[d1] = True
            diag2[d2] = True
            
            # 次の行へ
            backtrack(board, row + 1, cols, diag1, diag2)
            
            # バックトラック
            cols[col] = False
            diag1[d1] = False
            diag2[d2] = False
    
    solutions = []
    board = [-1] * n
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)  # 対角線の数
    diag2 = [False] * (2 * n - 1)
    
    backtrack(board, 0, cols, diag1, diag2)
    return solutions
```

**itertools.permutationsを使う方法**
```python
from itertools import permutations

def solve_n_queens_permutations(n):
    """N-Queens問題の解を返す（permutations使用）"""
    solutions = []
    
    # 各行に1つずつクイーンを配置する全順列を試す
    for perm in permutations(range(n)):
        # 対角線の衝突をチェック
        diag1 = [perm[i] - i for i in range(n)]  # 左上から右下
        diag2 = [perm[i] + i for i in range(n)]  # 右上から左下
        
        # 重複があれば対角線上に衝突
        if len(diag1) == len(set(diag1)) and len(diag2) == len(set(diag2)):
            solutions.append(list(perm))
    
    return solutions
```

### 推奨解答

面接では、**バックトラッキングの基本版**が推奨されます。

**理由**
- アルゴリズムの理解を確認できる
- 実装が明確
- 最適化版への拡張が可能

**完全な解答例**
```python
def solve_n_queens(n):
    """N-Queens問題の解を返す"""
    def is_safe(board, row, col):
        """(row, col)にクイーンを配置できるかチェック"""
        for i in range(row):
            # 同じ列
            if board[i] == col:
                return False
            # 対角線
            if abs(board[i] - col) == abs(i - row):
                return False
        return True
    
    def backtrack(board, row):
        """バックトラッキングで解を探索"""
        if row == n:
            solutions.append(board[:])
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
    
    solutions = []
    board = [-1] * n
    backtrack(board, 0)
    return solutions
```

### 面接でのポイント

1. **バックトラッキングの概念を理解**: 試行錯誤と戻る操作
2. **制約チェックを正確に実装**: 列、対角線のチェック
3. **計算量を理解**: 最悪O(n!)
4. **最適化を説明できる**: 対角線チェックの改善、メモ化など

---

## 6. The Skyline Problem（都市の稜線）

### 問題

都市の稜線とは、遠くから見たときにその都市のすべての建物によって形成されるシルエットの輪郭です。すべての建物の位置と高さが与えられているとき、これらの建物によって形成された稜線をまとめて出力するプログラムを作成します。

各建物の座標情報は整数の三重項 `[Li, Ri, Hi]` で、`Li` と `Ri` はそれぞれ建物の左端と右端のx座標で、`Hi` はその高さです。

**例**
```
Input: buildings = [[2,9,10], [3,7,15], [5,12,12], [15,20,10], [19,24,8]]
Output: [[2,10], [3,15], [7,12], [12,0], [15,10], [20,8], [24,0]]
```

### 基礎知識

#### キーポイントとは

稜線を一意に定義する点のリストです。キーポイントは水平線分の左端です。

**特徴**
- 高さが変わる点
- 建物が終わる点（高さ0に戻る）

### 解法: イベントベースのアプローチ

**考え方**
1. 各建物の開始点と終了点をイベントとして扱う
2. x座標でソート
3. 各x座標での最大高さを追跡
4. 高さが変わったらキーポイントを追加

**実装**
```python
def get_skyline(buildings):
    """都市の稜線を返す"""
    if not buildings:
        return []
    
    # イベントを作成: (x, height, is_start)
    events = []
    for Li, Ri, Hi in buildings:
        events.append((Li, Hi, True))   # 開始
        events.append((Ri, Hi, False))  # 終了
    
    # x座標でソート（同じx座標では開始を優先）
    events.sort(key=lambda x: (x[0], -x[1] if x[2] else x[1]))
    
    # 現在の高さを管理（最大ヒープ）
    import heapq
    heights = [0]  # 高さ0を初期値として保持
    removed = {}   # 削除された高さを追跡
    
    result = []
    prev_height = 0
    
    for x, height, is_start in events:
        if is_start:
            # 建物の開始: 高さを追加
            heapq.heappush(heights, -height)  # 最大ヒープのため負の値
        else:
            # 建物の終了: 高さを削除（遅延削除）
            removed[height] = removed.get(height, 0) + 1
        
        # 有効な最大高さを取得
        while heights and removed.get(-heights[0], 0) > 0:
            h = -heapq.heappop(heights)
            removed[h] -= 1
            if removed[h] == 0:
                del removed[h]
        
        current_height = -heights[0] if heights else 0
        
        # 高さが変わったらキーポイントを追加
        if current_height != prev_height:
            result.append([x, current_height])
            prev_height = current_height
    
    return result

# テスト
buildings = [[2,9,10], [3,7,15], [5,12,12], [15,20,10], [19,24,8]]
print(get_skyline(buildings))
# [[2,10], [3,15], [7,12], [12,0], [15,10], [20,8], [24,0]]
```

**動作の追跡**
```
建物: [[2,9,10], [3,7,15], [5,12,12], [15,20,10], [19,24,8]]

イベント:
(2, 10, start)  → heights=[0,10], current=10, キーポイント追加 [2,10]
(3, 15, start)  → heights=[0,10,15], current=15, キーポイント追加 [3,15]
(5, 12, start)  → heights=[0,10,12,15], current=15, 変化なし
(7, 15, end)    → heights=[0,10,12], current=12, キーポイント追加 [7,12]
(9, 10, end)    → heights=[0,12], current=12, 変化なし
(12, 12, end)   → heights=[0], current=0, キーポイント追加 [12,0]
(15, 10, start) → heights=[0,10], current=10, キーポイント追加 [15,10]
(19, 8, start)  → heights=[0,8,10], current=10, 変化なし
(20, 10, end)   → heights=[0,8], current=8, キーポイント追加 [20,8]
(24, 8, end)    → heights=[0], current=0, キーポイント追加 [24,0]
```

### 解法2: 分割統治法

**考え方**
- 建物を2つに分割
- それぞれの稜線を計算
- 2つの稜線をマージ

**実装**
```python
def get_skyline_divide_conquer(buildings):
    """都市の稜線を返す（分割統治法）"""
    if not buildings:
        return []
    
    if len(buildings) == 1:
        Li, Ri, Hi = buildings[0]
        return [[Li, Hi], [Ri, 0]]
    
    mid = len(buildings) // 2
    left = get_skyline_divide_conquer(buildings[:mid])
    right = get_skyline_divide_conquer(buildings[mid:])
    
    return merge_skylines(left, right)

def merge_skylines(left, right):
    """2つの稜線をマージ"""
    result = []
    i, j = 0, 0
    h1, h2 = 0, 0
    
    while i < len(left) and j < len(right):
        x1, y1 = left[i]
        x2, y2 = right[j]
        
        if x1 < x2:
            h1 = y1
            x, h = x1, max(h1, h2)
            i += 1
        elif x1 > x2:
            h2 = y2
            x, h = x2, max(h1, h2)
            j += 1
        else:
            h1, h2 = y1, y2
            x, h = x1, max(h1, h2)
            i += 1
            j += 1
        
        if not result or result[-1][1] != h:
            result.append([x, h])
    
    while i < len(left):
        result.append(left[i])
        i += 1
    
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result
```

### 推奨解答

面接では、**解法1（イベントベースのアプローチ）**が推奨されます。

**理由**
- 直感的で理解しやすい
- 実装が明確
- 計算量が良い（O(n log n)）

**完全な解答例**
```python
def get_skyline(buildings):
    """都市の稜線を返す"""
    if not buildings:
        return []
    
    import heapq
    
    # イベントを作成
    events = []
    for Li, Ri, Hi in buildings:
        events.append((Li, Hi, True))
        events.append((Ri, Hi, False))
    
    # ソート: x座標で、同じx座標では開始を優先
    events.sort(key=lambda x: (x[0], -x[1] if x[2] else x[1]))
    
    heights = [0]
    removed = {}
    result = []
    prev_height = 0
    
    for x, height, is_start in events:
        if is_start:
            heapq.heappush(heights, -height)
        else:
            removed[height] = removed.get(height, 0) + 1
        
        # 有効な最大高さを取得
        while heights and removed.get(-heights[0], 0) > 0:
            h = -heapq.heappop(heights)
            removed[h] -= 1
            if removed[h] == 0:
                del removed[h]
        
        current_height = -heights[0] if heights else 0
        
        if current_height != prev_height:
            result.append([x, current_height])
            prev_height = current_height
    
    return result
```

### 面接でのポイント

1. **問題を正確に理解**: キーポイントの定義、重複の排除
2. **イベントベースのアプローチ**: 開始/終了イベントの処理
3. **データ構造の選択**: 最大ヒープ、遅延削除
4. **エッジケースを考慮**: 空の入力、重複するx座標、同じ高さの連続

---

## まとめ

### 問題の難易度と学習順序

1. **初級**: フィボナッチ数列、関数を返す関数
2. **中級**: Maximum Subarray
3. **上級**: Spiral Matrix, N-Queens
4. **最上級**: The Skyline Problem

### 面接での評価ポイント

1. **問題理解**: 要件を正確に理解できるか
2. **アルゴリズム設計**: 適切な解法を選択できるか
3. **実装能力**: コードを正確に書けるか
4. **最適化**: 計算量を考慮できるか
5. **エッジケース**: 境界条件を考慮できるか
6. **コミュニケーション**: 考え方を説明できるか

### 学習の進め方

1. **基本問題から**: フィボナッチ、クロージャ
2. **動的計画法**: Maximum Subarray
3. **バックトラッキング**: N-Queens
4. **複雑な問題**: Spiral Matrix, Skyline Problem
5. **実践**: LeetCodeなどで類似問題を解く

### よくある質問

**Q: 計算量を改善する方法は？**
- ブルートフォース → 動的計画法
- 再帰 → メモ化
- 全探索 → 貪欲法

**Q: エッジケースは？**
- 空の入力
- 1要素のみ
- すべて同じ値
- 負の数

**Q: テストケースは？**
- 正常系
- エッジケース
- 大きな入力

