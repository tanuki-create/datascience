# 2026年8月27日：カバレッジ問題文セット

## 対象

- Day: 11
- 主テーマ: Binary Search・境界探索
- 問題数: 41問
- 内訳: Easy 9問、Medium 22問、Hard 10問
- 深掘り3問: `35`、`2904`、`154`。このセットには含めない。
- 状態: `presented`

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約、入力・出力、制約の要点、タグ、公式リンクで整理する。全問について、2026年8月27日時点のLeetCode公式メタデータで公開状態と難易度を確認した。

## Easy：9問

### 69. Sqrt(x) — Easy

非負整数`x`の平方根を小数点以下切り捨てで求める。入力は`0 <= x <= 2^31 - 1`、出力は整数。

タグ: Math、Binary Search、Newton's Method

[LeetCode公式ページ](https://leetcode.com/problems/sqrtx/)

### 278. First Bad Version — Easy

ある版以降がすべて不良になる`1..n`の版列で、API呼び出しにより最初の不良版を求める。`1 <= bad <= n <= 2^31 - 1`。

タグ: Binary Search、Interactive

[LeetCode公式ページ](https://leetcode.com/problems/first-bad-version/)

### 367. Valid Perfect Square — Easy

正整数`num`が整数の平方か判定する。入力は`1 <= num <= 2^31 - 1`、出力は真偽値で、組み込み平方根は使わない。

タグ: Math、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/valid-perfect-square/)

### 374. Guess Number Higher or Lower — Easy

`1..n`の中から選ばれた数を比較APIで当てる。`1 <= pick <= n <= 2^31 - 1`。

タグ: Binary Search、Interactive

[LeetCode公式ページ](https://leetcode.com/problems/guess-number-higher-or-lower/)

### 441. Arranging Coins — Easy

`n`枚のコインを1段目から段数分ずつ並べ、完成する段数を返す。入力は`1 <= n <= 2^31 - 1`。

タグ: Math、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/arranging-coins/)

### 704. Binary Search — Easy

昇順かつ要素が一意な配列から`target`の添字を求め、存在しなければ`-1`を返す。配列長は最大`10^4`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/binary-search/)

### 744. Find Smallest Letter Greater Than Target — Easy

昇順の文字配列から`target`より厳密に大きい最小文字を返し、なければ先頭へ循環する。配列長は`2..10^4`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/find-smallest-letter-greater-than-target/)

### 1351. Count Negative Numbers in a Sorted Matrix — Easy

各行・各列が非増加順の`m x n`行列に含まれる負数の個数を返す。`1 <= m,n <= 100`、要素は`-100..100`。

タグ: Array、Binary Search、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/)

### 1539. Kth Missing Positive Number — Easy

正の整数からなる狭義昇順配列で、現れない正整数のうち`k`番目を返す。配列長と`k`は最大`1000`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/kth-missing-positive-number/)

## Medium：22問

### 33. Search in Rotated Sorted Array — Medium

一意な要素を持つ昇順配列を回転した配列から`target`の添字を求め、なければ`-1`を返す。配列長は最大`5000`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/search-in-rotated-sorted-array/)

### 34. Find First and Last Position of Element in Sorted Array — Medium

非減少配列における`target`の最初と最後の位置を返し、存在しなければ`[-1,-1]`を返す。配列長は最大`10^5`、要求計算量は`O(log n)`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

### 74. Search a 2D Matrix — Medium

各行が昇順で、次の行の先頭が前の行の末尾より大きい行列から`target`を探す。`1 <= m,n <= 100`。

タグ: Array、Binary Search、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/search-a-2d-matrix/)

### 81. Search in Rotated Sorted Array II — Medium

重複を許す回転済み配列に`target`が存在するか判定する。配列長は最大`5000`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

### 532. K-diff Pairs in an Array — Medium

整数配列にある相異なる値のペアのうち、絶対差が`k`になるものの個数を返す。配列長は最大`10^4`、`0 <= k <= 10^7`。

タグ: Array、Hash Table、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/k-diff-pairs-in-an-array/)

### 275. H-Index II — Medium

昇順の引用数配列から、少なくとも`h`本が各`h`回以上引用された最大の`h`を求める。配列長は最大`10^5`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/h-index-ii/)

### 378. Kth Smallest Element in a Sorted Matrix — Medium

各行・各列が非減少順の`n x n`行列で`k`番目に小さい値を返す。`1 <= n <= 300`、`1 <= k <= n^2`。

タグ: Array、Binary Search、Sorting、Heap、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)

### 475. Heaters — Medium

家とヒーターの座標から、すべての家を覆うために必要な共通半径の最小値を求める。各配列長は最大`3 * 10^4`、座標は最大`10^9`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/heaters/)

### 528. Random Pick with Weight — Medium

正の重み配列に比例した確率で添字を返すデータ構造を実装する。配列長と呼び出し回数は最大`10^4`。

タグ: Array、Math、Binary Search、Prefix Sum、Randomized

[LeetCode公式ページ](https://leetcode.com/problems/random-pick-with-weight/)

### 611. Valid Triangle Number — Medium

非負整数配列から3要素を選び、三角形を作れる組の個数を返す。配列長は最大`1000`、要素は`0..1000`。

タグ: Array、Two Pointers、Binary Search、Greedy、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/valid-triangle-number/)

### 658. Find K Closest Elements — Medium

昇順配列から`x`に最も近い`k`要素を昇順で返す。`1 <= k <= arr.length <= 10^4`。

タグ: Array、Two Pointers、Binary Search、Sliding Window、Sorting、Heap

[LeetCode公式ページ](https://leetcode.com/problems/find-k-closest-elements/)

### 786. K-th Smallest Prime Fraction — Medium

`1`と相異なる素数からなる昇順配列で、`i < j`の分数`arr[i]/arr[j]`のうち`k`番目に小さいものを返す。配列長は最大`1000`。

タグ: Array、Two Pointers、Binary Search、Sorting、Heap

[LeetCode公式ページ](https://leetcode.com/problems/k-th-smallest-prime-fraction/)

### 825. Friends Of Appropriate Ages — Medium

年齢に基づく送信条件を満たす友達申請の有向ペア数を数える。人数は最大`2 * 10^4`、年齢は`1..120`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/friends-of-appropriate-ages/)

### 826. Most Profit Assigning Work — Medium

仕事ごとの難易度と利益、作業者ごとの能力から、一人一仕事以下で得られる総利益の最大値を返す。仕事数・作業者数は各最大`10^4`。

タグ: Array、Two Pointers、Binary Search、Greedy、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/most-profit-assigning-work/)

### 852. Peak Index in a Mountain Array — Medium

厳密に増加してから厳密に減少する山型配列の頂点添字を返す。配列長は`3..10^5`。

タグ: Array、Binary Search、Ternary Search

[LeetCode公式ページ](https://leetcode.com/problems/peak-index-in-a-mountain-array/)

### 911. Online Election — Medium

時刻順の投票列が与えられ、任意時刻`t`までの最多得票者を返す。投票数は最大`5000`、問い合わせは最大`10^4`回。

タグ: Array、Hash Table、Binary Search、Design

[LeetCode公式ページ](https://leetcode.com/problems/online-election/)

### 1146. Snapshot Array — Medium

値の設定、スナップショット取得、過去スナップショットの値取得を行う配列を設計する。長さと総操作数は最大`5 * 10^4`。

タグ: Array、Hash Table、Binary Search、Design、Persistent Data Structure

[LeetCode公式ページ](https://leetcode.com/problems/snapshot-array/)

### 1170. Compare Strings by Frequency of the Smallest Character — Medium

各問い合わせ文字列について、最小文字の出現回数がそれより大きい単語の数を返す。問い合わせ・単語数は各最大`2000`、文字列長は最大`10`。

タグ: Array、Hash Table、String、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/compare-strings-by-frequency-of-the-smallest-character/)

### 1300. Sum of Mutated Array Closest to Target — Medium

配列中で選んだ値より大きい要素をすべてその値へ置換し、合計を`target`へ最も近づける置換値を返す。同差なら小さい値を選ぶ。配列長は最大`10^4`。

タグ: Array、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/)

### 2080. Range Frequency Queries — Medium

固定配列について、区間`[left,right]`内の指定値の出現回数を返すデータ構造を設計する。配列長・問い合わせ数は最大`10^5`。

タグ: Array、Hash Table、Binary Search、Design、Segment Tree

[LeetCode公式ページ](https://leetcode.com/problems/range-frequency-queries/)

### 2300. Successful Pairs of Spells and Potions — Medium

各呪文について、積が`success`以上になる薬の個数を返す。両配列長は最大`10^5`、`success`は最大`10^10`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/)

### 2563. Count the Number of Fair Pairs — Medium

`i < j`かつ`lower <= nums[i] + nums[j] <= upper`を満たすペア数を返す。配列長は最大`10^5`、値と境界は`-10^9..10^9`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/count-the-number-of-fair-pairs/)

## Hard：10問

### 363. Max Sum of Rectangle No Larger Than K — Hard

整数行列の長方形部分領域から、合計が`k`以下で最大の値を求める。`1 <= m,n <= 100`、要素は`-100..100`。

タグ: Array、Binary Search、Matrix、Prefix Sum、Ordered Set

[LeetCode公式ページ](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/)

### 483. Smallest Good Base — Hard

文字列で与えられる`3..10^18`の整数`n`について、全桁が`1`になる最小の基数を返す。

タグ: Math、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/smallest-good-base/)

### 668. Kth Smallest Number in Multiplication Table — Hard

`m x n`の掛け算表に含まれる値のうち`k`番目に小さいものを返す。`m,n <= 3 * 10^4`、`1 <= k <= m*n`。

タグ: Math、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/)

### 719. Find K-th Smallest Pair Distance — Hard

整数配列の全ペアの絶対差から`k`番目に小さい距離を返す。配列長は`2..10^4`、値は`0..10^6`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)

### 793. Preimage Size of Factorial Zeroes Function — Hard

末尾のゼロ数が`k`になる階乗`x!`を持つ非負整数`x`の個数を返す。`0 <= k <= 10^9`。

タグ: Math、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/)

### 1095. Find in Mountain Array — Hard

API越しに参照する山型配列から`target`の最小添字を返し、なければ`-1`を返す。配列長は最大`10^4`で、API呼び出し回数に制限がある。

タグ: Array、Binary Search、Interactive、Ternary Search

[LeetCode公式ページ](https://leetcode.com/problems/find-in-mountain-array/)

### 1157. Online Majority Element In Subarray — Hard

指定された配列の区間で、`threshold`回以上現れる値を返すデータ構造を設計する。配列長は最大`2 * 10^4`、問い合わせは最大`10^4`回で、閾値は区間長の半分を超える。

タグ: Array、Binary Search、Design、Binary Indexed Tree、Segment Tree、Sqrt Decomposition、Boyer–Moore

[LeetCode公式ページ](https://leetcode.com/problems/online-majority-element-in-subarray/)

### 1187. Make Array Strictly Increasing — Hard

`arr1`の要素を`arr2`の要素へ置換し、`arr1`を狭義昇順にする最小操作数を返す。不可能なら`-1`。両配列長は最大`2000`、値は最大`10^9`。

タグ: Array、Binary Search、Dynamic Programming、Sorting、Longest Increasing Subsequence

[LeetCode公式ページ](https://leetcode.com/problems/make-array-strictly-increasing/)

### 1235. Maximum Profit in Job Scheduling — Hard

開始時刻・終了時刻・利益を持つ仕事から、重ならない仕事を選んだ最大利益を返す。仕事数は最大`5 * 10^4`、時刻は最大`10^9`。

タグ: Array、Binary Search、Dynamic Programming、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)

### 2251. Number of Flowers in Full Bloom — Hard

各花の開花区間と各人の到着時刻から、その時刻に咲いている花の数を返す。花・人は各最大`5 * 10^4`、時刻は最大`10^9`。

タグ: Array、Hash Table、Binary Search、Sorting、Prefix Sum、Ordered Set

[LeetCode公式ページ](https://leetcode.com/problems/number-of-flowers-in-full-bloom/)
