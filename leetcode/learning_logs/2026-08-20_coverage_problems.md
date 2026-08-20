# 2026年8月20日：カバレッジ問題文セット

## 対象

- Day: 4
- 主テーマ: 配列・シミュレーション・分割・Prefix／Two Pointers
- 問題数: 41問
- 深掘り3問: `3069`、`915`、`410`。このセットには含めない。
- 状態: `presented`

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約と公式リンクで整理する。

## Easy：9問

### 27. Remove Element

配列から指定値を取り除き、残った要素数を返す。配列の先頭部分を結果として扱う。

[LeetCode公式ページ](https://leetcode.com/problems/remove-element/)

### 88. Merge Sorted Array

2つのソート済み配列を、追加配列なしで1つの配列へ統合する。

[LeetCode公式ページ](https://leetcode.com/problems/merge-sorted-array/)

### 118. Pascal's Triangle

二項係数に相当するパスカルの三角形を、指定行数まで生成する。

[LeetCode公式ページ](https://leetcode.com/problems/pascals-triangle/)

### 119. Pascal's Triangle II

パスカルの三角形の指定行だけを、追加空間を抑えて生成する。

[LeetCode公式ページ](https://leetcode.com/problems/pascals-triangle-ii/)

### 283. Move Zeroes

配列内の0を末尾へ移動し、非ゼロ要素の相対順序を維持する。

[LeetCode公式ページ](https://leetcode.com/problems/move-zeroes/)

### 605. Can Place Flowers

隣接して植えられない花壇に、指定数の花を追加で植えられるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/can-place-flowers/)

### 724. Find Pivot Index

左側の合計と右側の合計が等しくなるインデックスを求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-pivot-index/)

### 747. Largest Number At Least Twice of Others

配列の最大値が、それ以外のすべての値の少なくとも2倍か判定する。

[LeetCode公式ページ](https://leetcode.com/problems/largest-number-at-least-twice-of-others/)

### 896. Monotonic Array

配列が単調非減少または単調非増加になっているか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/monotonic-array/)

## Medium：22問

### 11. Container With Most Water

2本の柱を選び、その間に入る水の最大面積を求める。

[LeetCode公式ページ](https://leetcode.com/problems/container-with-most-water/)

### 16. 3Sum Closest

3つの要素の合計が目標値に最も近くなる組を求める。

[LeetCode公式ページ](https://leetcode.com/problems/3sum-closest/)

### 31. Next Permutation

数列を辞書順で次に大きい順列へ、追加配列なしで変換する。

[LeetCode公式ページ](https://leetcode.com/problems/next-permutation/)

### 48. Rotate Image

正方行列を時計回りに90度回転させる。

[LeetCode公式ページ](https://leetcode.com/problems/rotate-image/)

### 90. Subsets II

重複要素を含む配列から、重複しない全部分集合を生成する。

[LeetCode公式ページ](https://leetcode.com/problems/subsets-ii/)

### 153. Find Minimum in Rotated Sorted Array

回転されたソート済み配列から最小値を二分探索で求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

### 162. Find Peak Element

隣接要素より大きいピーク要素のインデックスを求める。

[LeetCode公式ページ](https://leetcode.com/problems/find-peak-element/)

### 189. Rotate Array

配列を右へ`k`個回転させる。

[LeetCode公式ページ](https://leetcode.com/problems/rotate-array/)

### 274. H-Index

論文の引用数から、引用数が少なくとも`h`回ある論文が`h`本以上となる最大の`h`を求める。

[LeetCode公式ページ](https://leetcode.com/problems/h-index/)

### 436. Find Right Interval

各区間について、開始位置が自区間の終端以上となる最小の区間を探す。

[LeetCode公式ページ](https://leetcode.com/problems/find-right-interval/)

### 540. Single Element in a Sorted Array

他の要素がすべて2回ずつ現れるソート済み配列から、1回だけ現れる値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/single-element-in-a-sorted-array/)

### 581. Shortest Unsorted Continuous Subarray

その区間をソートすれば全体がソートされる最短の連続区間を求める。

[LeetCode公式ページ](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/)

### 646. Maximum Length of Pair Chain

`a < b`の組をつなげ、最長のペアチェーンを作る。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-length-of-pair-chain/)

### 670. Maximum Swap

数字の2桁を最大1回交換し、作れる最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-swap/)

### 769. Max Chunks To Make Sorted

分割して個別にソートし、連結すると全体がソート済みになる最大チャンク数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/max-chunks-to-make-sorted/)

### 775. Global and Local Inversions

局所反転の数と全体反転の数が一致するか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/global-and-local-inversions/)

### 945. Minimum Increment to Make Array Unique

配列の重複をなくすために必要な最小増加回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-increment-to-make-array-unique/)

### 1014. Best Sightseeing Pair

2地点の価値と距離による減点の合計を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/best-sightseeing-pair/)

### 1052. Grumpy Bookstore Owner

店主の不機嫌を一定時間だけ抑え、満足する顧客数を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/grumpy-bookstore-owner/)

### 1094. Car Pooling

乗客の乗降区間から、車の定員を超えないか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/car-pooling/)

### 1423. Maximum Points You Can Obtain from Cards

配列の左右から合計`k`枚のカードを取り、得点を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/)

### 1574. Shortest Subarray to be Removed to Make Array Sorted

連続区間を1つ削除して配列を非減少にする、その最短区間を求める。

[LeetCode公式ページ](https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/)

## Hard：10問

### 84. Largest Rectangle in Histogram

棒グラフから、作れる最大長方形の面積を求める。

[LeetCode公式ページ](https://leetcode.com/problems/largest-rectangle-in-histogram/)

### 85. Maximal Rectangle

二値行列から、1だけで構成される最大長方形の面積を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximal-rectangle/)

### 123. Best Time to Buy and Sell Stock III

株の売買を最大2回行ったときの最大利益を求める。

[LeetCode公式ページ](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

### 188. Best Time to Buy and Sell Stock IV

株の売買を最大`k`回行ったときの最大利益を求める。

[LeetCode公式ページ](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

### 295. Find Median from Data Stream

数値が順次追加されるデータストリームから、現在の中央値を取得する。

[LeetCode公式ページ](https://leetcode.com/problems/find-median-from-data-stream/)

### 214. Shortest Palindrome

文字列の先頭へ最小限の文字を追加し、回文にする。

[LeetCode公式ページ](https://leetcode.com/problems/shortest-palindrome/)

### 354. Russian Doll Envelopes

幅・高さがともに大きい封筒へ入れられる最長の入れ子列を求める。

[LeetCode公式ページ](https://leetcode.com/problems/russian-doll-envelopes/)

### 23. Merge k Sorted Lists

`k`個のソート済み連結リストを、1つのソート済みリストへ統合する。

[LeetCode公式ページ](https://leetcode.com/problems/merge-k-sorted-lists/)

### 862. Shortest Subarray with Sum at Least K

合計が`k`以上になる最短の連続部分配列を求める。

[LeetCode公式ページ](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)

### 1851. Minimum Interval to Include Each Query

各クエリ値を含む区間のうち、長さが最小のものを求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-interval-to-include-each-query/)
