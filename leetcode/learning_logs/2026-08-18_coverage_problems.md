# 2026年8月18日：カバレッジ問題文セット

## 対象

- Day: 2
- 主テーマ: 配列・Hash Table・頻度・欠損値・Prefix Sum・Two Pointers
- 問題数: 41問
- 深掘り3問: `3471`、`347`、`41`。このセットには含めない。
- 状態: `presented`

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約と公式リンクで整理する。

## Easy：9問

### 1. Two Sum

配列の中から、合計が目標値になる2つの要素のインデックスを求める。

[LeetCode公式ページ](https://leetcode.com/problems/two-sum/)

### 217. Contains Duplicate

配列に同じ値が2回以上登場するか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/contains-duplicate/)

### 349. Intersection of Two Arrays

2つの配列に共通して登場する値を重複なしで返す。

[LeetCode公式ページ](https://leetcode.com/problems/intersection-of-two-arrays/)

### 350. Intersection of Two Arrays II

2つの配列に共通する値を、登場回数も考慮して返す。

[LeetCode公式ページ](https://leetcode.com/problems/intersection-of-two-arrays-ii/)

### 219. Contains Duplicate II

同じ値がインデックス差`k`以内に存在するか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/contains-duplicate-ii/)

### 268. Missing Number

`0`から`n`までの整数のうち、配列に存在しない値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/missing-number/)

### 448. Find All Numbers Disappeared in an Array

`1`から`n`までのうち、配列に登場しない値をすべて求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)

### 645. Set Mismatch

1つが重複し、1つが欠けている集合から、重複値と欠損値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/set-mismatch/)

### 414. Third Maximum Number

配列にある異なる値のうち、3番目に大きい値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/third-maximum-number/)

## Medium：22問

### 15. 3Sum

配列から3つの値を選び、合計が0になる重複なしの組を求める。

[LeetCode公式ページ](https://leetcode.com/problems/3sum/)

### 49. Group Anagrams

互いにアナグラムになる文字列を同じグループへまとめる。

[LeetCode公式ページ](https://leetcode.com/problems/group-anagrams/)

### 128. Longest Consecutive Sequence

配列の値から、連続する整数列の最長の長さを求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-consecutive-sequence/)

### 380. Insert Delete GetRandom O(1)

挿入・削除・ランダム取得を平均`O(1)`で行うデータ構造を設計する。

[LeetCode公式ページ](https://leetcode.com/problems/insert-delete-getrandom-o1/)

### 560. Subarray Sum Equals K

合計が`k`になる連続部分配列の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/subarray-sum-equals-k/)

### 525. Contiguous Array

0と1の個数が等しい最長の連続部分配列を求める。

[LeetCode公式ページ](https://leetcode.com/problems/contiguous-array/)

### 523. Continuous Subarray Sum

合計が`k`の倍数になる長さ2以上の連続部分配列が存在するか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/continuous-subarray-sum/)

### 974. Subarray Sums Divisible by K

合計が`k`で割り切れる連続部分配列の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/subarray-sums-divisible-by-k/)

### 930. Binary Subarrays With Sum

0と1からなる配列で、合計が目標値になる連続部分配列の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/binary-subarrays-with-sum/)

### 1248. Count Number of Nice Subarrays

奇数をちょうど`k`個含む連続部分配列の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/count-number-of-nice-subarrays/)

### 287. Find the Duplicate Number

`1`から`n`の値を含む配列から、重複している1つの値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-the-duplicate-number/)

### 442. Find All Duplicates in an Array

配列に2回登場する値をすべて求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-all-duplicates-in-an-array/)

### 75. Sort Colors

0、1、2だけからなる配列を、追加配列なしでソートする。

[LeetCode公式ページ](https://leetcode.com/problems/sort-colors/)

### 56. Merge Intervals

重なっている区間を統合し、互いに重ならない区間へ整理する。

[LeetCode公式ページ](https://leetcode.com/problems/merge-intervals/)

### 57. Insert Interval

ソート済みの区間列へ新しい区間を追加し、重複区間を統合する。

[LeetCode公式ページ](https://leetcode.com/problems/insert-interval/)

### 54. Spiral Matrix

行列の要素を、外側から螺旋順に読み取る。

[LeetCode公式ページ](https://leetcode.com/problems/spiral-matrix/)

### 73. Set Matrix Zeroes

行列中の0に対応する行と列をすべて0にする。

[LeetCode公式ページ](https://leetcode.com/problems/set-matrix-zeroes/)

### 289. Game of Life

近傍セルの個数に従って、次の状態の盤面を計算する。

[LeetCode公式ページ](https://leetcode.com/problems/game-of-life/)

### 200. Number of Islands

上下左右につながった陸地のグループ数を数える。

[LeetCode公式ページ](https://leetcode.com/problems/number-of-islands/)

### 238. Product of Array Except Self

各位置について、自分以外の全要素の積を除算なしで求める。

[LeetCode公式ページ](https://leetcode.com/problems/product-of-array-except-self/)

### 918. Maximum Sum Circular Subarray

円環状に接続された配列から、最大連続部分配列和を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-sum-circular-subarray/)

### 152. Maximum Product Subarray

連続部分配列の積の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-product-subarray/)

## Hard：10問

### 42. Trapping Rain Water

棒の高さから、雨水を蓄えられる総量を求める。

[LeetCode公式ページ](https://leetcode.com/problems/trapping-rain-water/)

### 149. Max Points on a Line

平面上の点から、同一直線上にある点の最大数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/max-points-on-a-line/)

### 239. Sliding Window Maximum

各固定長ウィンドウ内の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/sliding-window-maximum/)

### 315. Count of Smaller Numbers After Self

各要素の右側にある、より小さい値の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

### 327. Count of Range Sum

指定範囲に入る連続部分配列和の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/count-of-range-sum/)

### 493. Reverse Pairs

`i < j`かつ`nums[i] > 2 * nums[j]`となる組の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/reverse-pairs/)

### 4. Median of Two Sorted Arrays

2つのソート済み配列を統合せず、全体の中央値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/median-of-two-sorted-arrays/)

### 135. Candy

子どもの評価に従い、隣接条件を満たす最小の飴の総数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/candy/)

### 330. Patching Array

1から`n`までを作れるように、追加すべき最小個数の値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/patching-array/)

### 164. Maximum Gap

ソート後の隣接要素間の最大差を、比較ソートなしで求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-gap/)
