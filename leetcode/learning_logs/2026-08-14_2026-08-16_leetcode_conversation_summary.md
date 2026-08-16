# LeetCode学習ログ：2026年8月14日〜16日

このファイルは、2026年8月14日から16日までのLeetCode学習に関する会話を、問題・解法・学習テーマの順に整理したものです。

## 学習の進め方

- その日の3問を確認する。
- まず問題文、`substring`、`subsequence`、XORなどの用語を理解する。
- 次に解法とコードを確認する。
- 最後に、Pythonの記法と、コンピュータが状態をどのように更新するかまで分解する。
- 解法の中心だけでなく、計算量、データ構造、なぜその方法で正しいかも確認する。

## 2026年8月14日：文字列とスライディングウィンドウ

### 3090. Maximum Length Substring With Two Occurrences — Easy

[LeetCode公式ページ](https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/)

#### 問題の要点

文字列 `s` の中から、各文字が2回以下しか登場しない最長の連続部分文字列を探し、その長さを返す。

`at most two occurrences` は、各文字の出現回数が0回、1回、2回なら有効で、3回以上なら無効という意味。

説明文のコピー時に下線が失われると、元の文字列全体が有効な部分文字列のように見えることがある。

Example 1の有効な部分文字列は、`bcbbbcba` の末尾にある `bcba` である。

#### 解法

スライディングウィンドウを使う。

- `left` と `right` で現在の連続区間を表す。
- `count` で各文字の出現回数を管理する。
- 右端の文字を追加して、3回以上になったら左端を進める。
- 条件が回復した区間の長さで最大値を更新する。

```python
class Solution:
    def maximumLengthSubstring(self, s: str) -> int:
        count = [0] * 26
        left = 0
        answer = 0

        for right, ch in enumerate(s):
            current = ord(ch) - ord('a')
            count[current] += 1

            while count[current] > 2:
                left_char = ord(s[left]) - ord('a')
                count[left_char] -= 1
                left += 1

            answer = max(answer, right - left + 1)

        return answer
```

計算量は、時間 `O(n)`、追加空間 `O(1)`。

#### コードを読むときのポイント

- `enumerate(s)` は、インデックスと文字を同時に取り出す。
- `ord(ch) - ord('a')` は、英字を配列の添字に変換する。
- `right - left + 1` は、両端を含む区間の長さを表す。
- 文字列自体を切ったり削除したりせず、`left` と `right` の数値だけを動かす。

### 3. Longest Substring Without Repeating Characters — Medium

[LeetCode公式ページ](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

#### 問題の要点

同じ文字が重複しない最長の連続部分文字列の長さを求める。

`substring` は連続している必要がある。

`subsequence` のように文字を飛ばして選ぶことはできない。

#### 解法

スライディングウィンドウと、各文字の最後の出現位置を管理する辞書を使う。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        answer = 0

        for right, ch in enumerate(s):
            previous = last_seen.get(ch, -1)

            if previous >= left:
                left = previous + 1

            last_seen[ch] = right
            answer = max(answer, right - left + 1)

        return answer
```

重複した文字が現在の区間内にあるとき、左端をその文字の直後へ一気に移動する。

`left` が過去へ戻らないように、現在の区間内にある出現位置だけを使う。

計算量は、辞書操作の平均 `O(1)` を前提に、時間 `O(n)`、追加空間 `O(n)`。

### 76. Minimum Window Substring — Hard

[LeetCode公式ページ](https://leetcode.com/problems/minimum-window-substring/)

#### 問題の要点

文字列 `t` が必要とするすべての文字を、必要な個数も含めて持つ、`s` の最短の連続部分文字列を返す。

例えば `t = "AABC"` なら、`A` は2個、`B` は1個、`C` は1個必要。

必要な部分文字列が存在しなければ、空文字列 `""` を返す。

#### 解法

必要数を `need`、現在のウィンドウの数を `window` で管理する。

- 右端を進めて、必要な文字をすべて揃える。
- 条件を満たしたら、左端を進めて可能な限り短くする。
- 有効な区間の中で最短のものを記録する。

`3090` と `3` は「無効な間に縮める」のに対し、`76` は「有効な間に縮める」という違いがある。

```python
from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        window = {}
        required = len(need)
        have = 0

        left = 0
        best_length = float("inf")
        best_start = 0

        for right, ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1

            if ch in need and window[ch] == need[ch]:
                have += 1

            while have == required:
                current_length = right - left + 1

                if current_length < best_length:
                    best_length = current_length
                    best_start = left

                left_ch = s[left]
                window[left_ch] -= 1

                if left_ch in need and window[left_ch] < need[left_ch]:
                    have -= 1

                left += 1

        if best_length == float("inf"):
            return ""

        return s[best_start:best_start + best_length]
```

計算量は、時間 `O(m + n)`、追加空間 `O(k)`。

ここで `k` は、`s` と `t` に登場する異なる文字の種類数。

## 3問を一段下のレイヤーで整理

3問の共通部分は、文字列をコピーせず、区間をインデックスで表すこと。

```text
現在の区間 = s[left:right + 1]
```

実際に変更しているのは文字列ではなく、次の状態である。

- `left`: 区間の左端
- `right`: 区間の右端
- カウント配列または辞書
- これまでに見つけた最大値または最小値

`left` と `right` は左から右へしか進まないため、`while` があっても合計の移動回数は `O(n)` に抑えられる。

ヒープは、最小値や最大値を優先的に取り出すデータ構造である。

この3問で必要なのは文字の出現回数や最後の位置なので、配列・辞書・集合の方が適切であり、ヒープは使わない。

## 2026年8月15日：XORとビット演算

### 136. Single Number — Easy

[LeetCode公式ページ](https://leetcode.com/problems/single-number/)

#### 解法

配列のすべての要素をXORする。

```python
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        answer = 0

        for num in nums:
            answer ^= num

        return answer
```

XORには次の性質がある。

```text
x XOR x = 0
x XOR 0 = x
```

そのため、2回登場する要素は相殺され、1回だけ登場する要素が残る。

計算量は、時間 `O(n)`、追加空間 `O(1)`。

#### Pythonとコンピュータ処理

- `^` はビット単位のXORであり、累乗ではない。
- `^=` は `answer = answer ^ num` の省略記法。
- `2` は2進数では `010`、`1` は `001` として扱える。
- 同じビット同士のXORは0になる。
- `for num in nums` は、配列の要素を左から1つずつ取り出す。
- `return answer` は、関数を終了して答えを返す。

### 3702. Longest Subsequence With Non-Zero Bitwise XOR — Medium

[LeetCode公式ページ](https://leetcode.com/problems/longest-subsequence-with-non-zero-bitwise-xor/)

#### 解法

配列全体のXORと、非ゼロ要素の有無だけを調べる。

```python
class Solution:
    def longestSubsequence(self, nums: list[int]) -> int:
        total_xor = 0
        has_non_zero = False

        for num in nums:
            total_xor ^= num

            if num != 0:
                has_non_zero = True

        if total_xor != 0:
            return len(nums)

        if has_non_zero:
            return len(nums) - 1

        return 0
```

考え方は3ケース。

1. 配列全体のXORが非ゼロなら、全要素を選べるので `n`。
2. 全体のXORが0で、非ゼロ要素があれば、非ゼロ要素を1つ除いて `n - 1`。
3. すべての要素が0なら、どの部分列のXORも0なので `0`。

計算量は、時間 `O(n)`、追加空間 `O(1)`。

### 1707. Maximum XOR With an Element From Array — Hard

[LeetCode公式ページ](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)

#### 問題の制約

各クエリ `[x, m]` について、`nums[j] <= m` を満たす要素の中から、`x XOR nums[j]` が最大になるものを探す。

`nums` とクエリが最大10万個あるため、各クエリで全要素を調べる方法は `O(nq)` になり、遅すぎる。

#### 解法

オフライン処理と二進Trieを組み合わせる。

1. `nums` を昇順に並べる。
2. クエリを `m` の昇順に並べ、元のインデックスを保持する。
3. 現在の `m` 以下の `nums` だけを二進Trieに追加する。
4. XORの上位ビットから、反対のビットの枝を優先して選ぶ。
5. 結果を元のクエリ順に戻す。

```python
class Solution:
    def maximizeXor(
        self,
        nums: list[int],
        queries: list[list[int]]
    ) -> list[int]:
        MAX_BIT = 30

        nums.sort()

        ordered_queries = sorted(
            (m, x, index)
            for index, (x, m) in enumerate(queries)
        )

        # trie[node] = [0の子ノード, 1の子ノード]
        trie = [[-1, -1]]

        def insert(value: int) -> None:
            node = 0

            for bit in range(MAX_BIT, -1, -1):
                current_bit = (value >> bit) & 1

                if trie[node][current_bit] == -1:
                    trie[node][current_bit] = len(trie)
                    trie.append([-1, -1])

                node = trie[node][current_bit]

        def find_max_xor(value: int) -> int:
            node = 0
            result = 0

            for bit in range(MAX_BIT, -1, -1):
                current_bit = (value >> bit) & 1
                preferred_bit = 1 - current_bit

                if trie[node][preferred_bit] != -1:
                    result |= 1 << bit
                    node = trie[node][preferred_bit]
                else:
                    node = trie[node][current_bit]

            return result

        answer = [-1] * len(queries)
        nums_index = 0

        for limit, value, query_index in ordered_queries:
            while (
                nums_index < len(nums)
                and nums[nums_index] <= limit
            ):
                insert(nums[nums_index])
                nums_index += 1

            if nums_index > 0:
                answer[query_index] = find_max_xor(value)

        return answer
```

Trieの検索では、各ビットについて、`x` と反対のビットを選べるならXOR結果を1にできる。

上位ビットほど数値への影響が大きいため、上位ビットから貪欲に選択してよい。

計算量は、ビット数を `B = 31` とすると、

```text
時間: O(n log n + q log q + (n + q)B)
空間: O(nB + q)
```

`B` は定数なので、概ね時間 `O(n log n + q log q)`、空間 `O(n + q)`。

## 2026年8月16日：ゲーム理論

### 292. Nim Game — Easy

[LeetCode公式ページ](https://leetcode.com/problems/nim-game/)

#### 問題の要点

1回のターンで1〜3個の石を取り、最後の石を取った人が勝つ。

両者が最適に動く場合に、先手が勝てるかを判定する。

#### 解法

4の倍数の状態は負けで、それ以外は勝ち。

```python
class Solution:
    def canWinNim(self, n: int) -> bool:
        return n % 4 != 0
```

4個のとき、先手が1〜3個のどれを取っても、相手は残りの石をすべて取れる。

4の倍数でない場合は、最初に `n % 4` 個を取って、相手に4の倍数を渡せる。

相手が1個取れば自分は3個、相手が2個取れば自分は2個、相手が3個取れば自分は1個取ることで、2人の合計を常に4にできる。

計算量は、時間 `O(1)`、追加空間 `O(1)`。

### 2029. Stone Game IX — Medium

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-ix/)

石を交互に取り除き、取り除いた石の合計が3で割り切れる状態で石を取ったプレイヤーが負けるゲーム。

両者が最適に動いた場合に、Aliceが勝つかを判定する。

この問題は提示まで行っており、解法・コードはまだ整理していない。

主なテーマは、剰余、ゲーム理論、最適戦略、状態の圧縮。

### 1406. Stone Game III — Hard

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-iii/)

先頭から1〜3個の石を取り、取得した石の合計得点を競うゲーム。

最適に行動した場合に、Alice、Bob、Tieのどれになるかを返す。

この問題は提示まで行っており、解法・コードはまだ整理していない。

主なテーマは、動的計画法、ゲーム理論、最適な得点差。

## Pythonとコンピュータ処理の学習メモ

今回の学習では、問題を解くために必要なPython記法と、コンピュータがコードを実行する仕組みも確認した。

### 基本的なPython記法

```python
x = 0              # 代入
x == 0             # 比較
x += 1             # 代入の省略記法

if condition:      # 条件分岐
    ...

for value in values:  # 繰り返し
    ...

while condition:   # 条件が真の間の繰り返し
    ...

def function(x):   # 関数定義
    return x       # 値を返す
```

### よく使うデータ構造

- `list`: 順番に値を保持する。
- `dict`: キーと値を対応付ける。
- `set`: 重複を除いた値の集合を保持する。
- 固定長の配列: 文字やビットの個数を直接管理する。

### コンピュータ側の見方

- 整数は内部ではビット列として扱われる。
- `^` はビットごとのXORを行う。
- 文字列は動かさず、`left` と `right` の整数で論理的な区間を表せる。
- 辞書は、キーから対応する値を平均的に高速に探す。
- `O(n)` は入力を1回程度調べる処理、`O(1)` は入力サイズに依存しない処理を表す。
- `O(1)` 追加空間は、入力以外に使うメモリ量が一定という意味であり、メモリを全く使わないという意味ではない。

### ヒープについて

ヒープは、最小値・最大値・優先度の高い要素を取り出すためのデータ構造。

今回の問題では、文字の個数、最後の位置、XORのビット、ゲーム状態を扱うため、ヒープは中心的なデータ構造ではない。

1707ではヒープではなく、ビット列を上位ビットから探索する二進Trieを使う。

## 今後の学習候補

- 2029 `Stone Game IX` の剰余による状態整理。
- 1406 `Stone Game III` の動的計画法と得点差。
- 1707の二進Trieを、ビットを1つずつ追跡しながら手計算する。
- Pythonの `list`、`dict`、`set` の操作と計算量を小さなコードで確認する。
- `O(n)`、`O(n log n)`、`O(n^2)` の処理量を具体的な入力サイズで比較する。
