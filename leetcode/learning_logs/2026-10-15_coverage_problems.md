# 2026年10月15日：カバレッジ問題文セット

## 対象

- Day: 60
- 主テーマ: House Robber・State Machine DP
- 問題数: 41問
- 深掘り3問: `2913`、`309`、`552`。このセットには含めない。

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約、制約、タグ、公式リンクで整理する。

## Easy：9問

### 1217. Minimum Cost to Move Chips to The Same Position

チップを同じ位置へ集める。2マス移動は無料、1マス移動はコスト1として、必要な最小コストを求める。

- 制約: `1 <= position.length <= 100`、`1 <= position[i] <= 10^9`
- タグ: Array、Math、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position/)

### 1221. Split a String in Balanced Strings

`L`と`R`からなる文字列を、各部分の`L`と`R`の個数が等しくなるように分割し、得られる部分数を最大化する。

- 制約: `2 <= s.length <= 1000`、文字は`L`または`R`、入力全体はbalanced
- タグ: String、Greedy、Counting

[LeetCode公式ページ](https://leetcode.com/problems/split-a-string-in-balanced-strings/)

### 1342. Number of Steps to Reduce a Number to Zero

整数が偶数なら2で割り、奇数なら1を引く操作を0になるまで行い、操作回数を求める。

- 制約: `0 <= num <= 10^6`
- タグ: Math、Bit Manipulation

[LeetCode公式ページ](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/)

### 1413. Minimum Value to Get Positive Step by Step Sum

配列を左から足したすべての累積和が1以上になるために必要な、最小の正の初期値を求める。

- 制約: `1 <= nums.length <= 100`、`-100 <= nums[i] <= 100`
- タグ: Array、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum/)

### 1422. Maximum Score After Splitting a String

二進文字列を空でない左半分と右半分に分け、左側の0の数と右側の1の数の合計を最大化する。

- 制約: `2 <= s.length <= 500`、`s`は`0`と`1`のみ
- タグ: String、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/maximum-score-after-splitting-a-string/)

### 1588. Sum of All Odd Length Subarrays

配列に含まれるすべての奇数長の連続部分配列の合計値を求める。

- 制約: `1 <= arr.length <= 100`、`1 <= arr[i] <= 1000`
- タグ: Array、Math、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/sum-of-all-odd-length-subarrays/)

### 1646. Get Maximum in Generated Array

規則 `nums[2*i] = nums[i]`、`nums[2*i+1] = nums[i] + nums[i+1]` で配列を生成し、最大値を返す。

- 制約: `0 <= n <= 100`
- タグ: Array、Simulation

[LeetCode公式ページ](https://leetcode.com/problems/get-maximum-in-generated-array/)

### 1800. Maximum Ascending Subarray Sum

隣接要素が厳密に増加する連続部分配列のうち、要素合計が最大のものを求める。

- 制約: `1 <= nums.length <= 100`、`1 <= nums[i] <= 100`
- タグ: Array

[LeetCode公式ページ](https://leetcode.com/problems/maximum-ascending-subarray-sum/)

### 2016. Maximum Difference Between Increasing Elements

`i < j`かつ`nums[i] < nums[j]`を満たす組について`nums[j] - nums[i]`の最大値を求め、該当しなければ`-1`を返す。

- 制約: `2 <= nums.length <= 1000`、`1 <= nums[i] <= 10^9`
- タグ: Array

[LeetCode公式ページ](https://leetcode.com/problems/maximum-difference-between-increasing-elements/)

## Medium：22問

### 5. Longest Palindromic Substring

文字列から、連続する部分文字列のうち最長の回文を返す。

- 制約: `1 <= s.length <= 1000`、英数字のみ
- タグ: Two Pointers、String、Dynamic Programming、Manacher

[LeetCode公式ページ](https://leetcode.com/problems/longest-palindromic-substring/)

### 22. Generate Parentheses

`n`組の括弧から、正しく対応するすべての括弧列を生成する。

- 制約: `1 <= n <= 8`
- タグ: String、Dynamic Programming、Backtracking、Bracket Sequences

[LeetCode公式ページ](https://leetcode.com/problems/generate-parentheses/)

### 45. Jump Game II

各要素をその位置から最大で進める距離とみなし、配列の末尾へ到達する最小ジャンプ回数を求める。

- 制約: `1 <= nums.length <= 10^4`、`0 <= nums[i] <= 1000`、末尾へ到達可能
- タグ: Array、Dynamic Programming、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/jump-game-ii/)

### 53. Maximum Subarray

整数配列から、合計が最大となる空でない連続部分配列の合計を求める。

- 制約: `1 <= nums.length <= 10^5`、`-10^4 <= nums[i] <= 10^4`
- タグ: Array、Divide and Conquer、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/maximum-subarray/)

### 55. Jump Game

各要素を最大ジャンプ距離としたとき、先頭から末尾へ到達できるか判定する。

- 制約: `1 <= nums.length <= 10^4`、`0 <= nums[i] <= 10^5`
- タグ: Array、Dynamic Programming、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/jump-game/)

### 62. Unique Paths

`m x n`グリッドの左上から右下まで、右または下だけで進む経路数を求める。

- 制約: `1 <= m, n <= 100`
- タグ: Math、Dynamic Programming、Combinatorics

[LeetCode公式ページ](https://leetcode.com/problems/unique-paths/)

### 63. Unique Paths II

障害物を含むグリッドで、左上から右下まで右または下だけで進む経路数を求める。

- 制約: `1 <= m, n <= 100`、各セルは`0`または`1`
- タグ: Array、Dynamic Programming、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/unique-paths-ii/)

### 64. Minimum Path Sum

非負整数グリッドで、左上から右下まで右または下に進む経路の最小合計を求める。

- 制約: `1 <= m, n <= 200`、`0 <= grid[i][j] <= 200`
- タグ: Array、Dynamic Programming、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/minimum-path-sum/)

### 72. Edit Distance

2つの文字列を、挿入・削除・置換で互いに変換するための最小操作回数を求める。

- 制約: 各文字列長は`0..500`、小文字英字のみ
- タグ: String、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/edit-distance/)

### 91. Decode Ways

数字列を`1`〜`26`の文字へ復号する方法数を求める。0の扱いに注意する。

- 制約: `1 <= s.length <= 100`、数字のみ（先頭0を含み得る）
- タグ: String、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/decode-ways/)

### 96. Unique Binary Search Trees

値`1..n`を使って作れる構造の異なる二分探索木の数を求める。

- 制約: `1 <= n <= 19`
- タグ: Math、Dynamic Programming、Tree、Binary Search Tree、Binary Tree

[LeetCode公式ページ](https://leetcode.com/problems/unique-binary-search-trees/)

### 122. Best Time to Buy and Sell Stock II

株を何度でも売買できる条件で、合計利益を最大化する。

- 制約: `1 <= prices.length <= 3 * 10^4`、`0 <= prices[i] <= 10^4`
- タグ: Array、Dynamic Programming、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

### 221. Maximal Square

0と1からなる行列から、1だけで構成される最大の正方形の面積を求める。

- 制約: 行列の行・列は各`1..300`、各セルは`0`または`1`
- タグ: Array、Dynamic Programming、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/maximal-square/)

### 264. Ugly Number II

素因数が2・3・5だけの正整数を小さい順に並べ、`n`番目の値を求める。

- 制約: `1 <= n <= 1690`
- タグ: Hash Table、Math、Dynamic Programming、Heap (Priority Queue)

[LeetCode公式ページ](https://leetcode.com/problems/ugly-number-ii/)

### 279. Perfect Squares

正整数`n`を完全平方数の和で表すとき、必要な平方数の最小個数を求める。

- 制約: `1 <= n <= 10^4`
- タグ: Math、Dynamic Programming、Breadth-First Search、Knapsack Problem

[LeetCode公式ページ](https://leetcode.com/problems/perfect-squares/)

### 343. Integer Break

整数`n`を2個以上の正整数へ分割し、積を最大化する。

- 制約: `2 <= n <= 58`
- タグ: Math、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/integer-break/)

### 368. Largest Divisible Subset

集合内の任意の2要素について、一方が他方で割り切れる最大の部分集合を返す。

- 制約: `1 <= nums.length <= 1000`、`1 <= nums[i] <= 2 * 10^9`、値は一意
- タグ: Array、Math、Dynamic Programming、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/largest-divisible-subset/)

### 376. Wiggle Subsequence

隣接差の符号が正負交互になる部分列の最長長を求める。

- 制約: `1 <= nums.length <= 1000`、`0 <= nums[i] <= 1000`
- タグ: Array、Dynamic Programming、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/wiggle-subsequence/)

### 377. Combination Sum IV

重複のない正整数配列から、順序を区別して合計が`target`になる組み合わせ数を求める。

- 制約: `1 <= nums.length <= 200`、`1 <= nums[i], target <= 1000`、`nums`の値は一意
- タグ: Array、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/combination-sum-iv/)

### 397. Integer Replacement

整数`n`を1にするため、偶数は2で割り、奇数は1を加減する操作の最小回数を求める。

- 制約: `1 <= n <= 2^31 - 1`
- タグ: Dynamic Programming、Greedy、Bit Manipulation、Memoization

[LeetCode公式ページ](https://leetcode.com/problems/integer-replacement/)

### 474. Ones and Zeroes

0と1からなる文字列群から、0を最大`m`個、1を最大`n`個使って選べる文字列数を最大化する。

- 制約: `1 <= strs.length <= 600`、各長さ`1..100`、`1 <= m, n <= 100`
- タグ: Array、String、Dynamic Programming、Knapsack Problem、0-1 Knapsack

[LeetCode公式ページ](https://leetcode.com/problems/ones-and-zeroes/)

### 740. Delete and Earn

値`x`を選ぶと`x`点を得て、値`x-1`と`x+1`をすべて使えなくする操作で、得点を最大化する。

- 制約: `1 <= nums.length <= 2 * 10^4`、`1 <= nums[i] <= 10^4`
- タグ: Array、Hash Table、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/delete-and-earn/)

## Hard：10問

### 10. Regular Expression Matching

文字列全体を、`.`（任意の1文字）と`*`（直前要素の0回以上の繰り返し）を含むパターンで完全一致できるか判定する。

- 制約: `s.length, p.length`は各`1..20`、`s`は小文字英字、`p`は小文字英字・`.`・`*`
- タグ: String、Dynamic Programming、Recursion

[LeetCode公式ページ](https://leetcode.com/problems/regular-expression-matching/)

### 32. Longest Valid Parentheses

括弧文字列から、正しく対応する連続部分文字列の最長長を求める。

- 制約: `0 <= s.length <= 3 * 10^4`、文字は`(`または`)`
- タグ: String、Dynamic Programming、Stack、Bracket Sequences

[LeetCode公式ページ](https://leetcode.com/problems/longest-valid-parentheses/)

### 44. Wildcard Matching

文字列全体が、`?`（任意の1文字）と`*`（任意の文字列）を含むパターンに一致するか判定する。

- 制約: `s.length, p.length <= 2000`、`s`は小文字英字、`p`は小文字英字・`?`・`*`
- タグ: String、Dynamic Programming、Greedy、Recursion

[LeetCode公式ページ](https://leetcode.com/problems/wildcard-matching/)

### 87. Scramble String

文字列を再帰的に二分割して入れ替える操作で、一方から他方を作れるか判定する。

- 制約: 2つの長さは等しく`1..30`、小文字英字のみ
- タグ: String、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/scramble-string/)

### 115. Distinct Subsequences

文字列`s`から順序を保って文字を削除し、`t`を作る異なる部分列の数を求める。

- 制約: `s.length, t.length`は各`1..1000`、英字のみ
- タグ: String、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/distinct-subsequences/)

### 132. Palindrome Partitioning II

文字列を回文だけの部分文字列へ分割するために必要な最小カット数を求める。

- 制約: `1 <= s.length <= 2000`、小文字英字のみ
- タグ: String、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/palindrome-partitioning-ii/)

### 174. Dungeon Game

正負の体力変化がある盤面で、右または下へ進んで姫に到達するための初期体力の最小値を求める。

- 制約: 行・列は各`1..200`、`-1000 <= dungeon[i][j] <= 1000`
- タグ: Array、Dynamic Programming、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/dungeon-game/)

### 233. Number of Digit One

`1`から`n`までの整数を十進表記したとき、数字`1`が現れる総回数を求める。

- 制約: `0 <= n <= 10^9`
- タグ: Math、Dynamic Programming、Recursion

[LeetCode公式ページ](https://leetcode.com/problems/number-of-digit-one/)

### 329. Longest Increasing Path in a Matrix

行列内で上下左右へ移動し、値が厳密に増加する経路の最長長を求める。

- 制約: 行・列は各`1..200`、`0 <= matrix[i][j] <= 2^31 - 1`
- タグ: Array、Dynamic Programming、DFS、BFS、Graph、Topological Sort、Memoization、Matrix、DAG

[LeetCode公式ページ](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

### 403. Frog Jump

石の位置が与えられ、直前のジャンプ長を`k`とした次のジャンプが`k-1`、`k`、`k+1`のいずれかになるとき、最後の石へ到達できるか判定する。

- 制約: `2 <= stones.length <= 2000`、位置は`0..2^31-1`、昇順かつ厳密増加、先頭は0
- タグ: Array、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/frog-jump/)
