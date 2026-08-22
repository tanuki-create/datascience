# 2026年8月22日：カバレッジ問題文セット

## 対象

- Day: 6
- 主テーマ: Sliding Window
- 問題数: 41問
- 深掘り3問: `643`、`209`、`3116`。このセットには含めない。
- 状態: `presented`

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約と公式リンクで整理する。

## Easy：9問

### 594. Longest Harmonious Subsequence

最大値と最小値の差がちょうど1になる部分列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-harmonious-subsequence/)

### 1652. Defuse the Bomb

循環配列の各要素を、`k > 0`なら直後、`k < 0`なら直前の要素の合計へ置き換え、`k = 0`なら0にする。

[LeetCode公式ページ](https://leetcode.com/problems/defuse-the-bomb/)

### 1876. Substrings of Size Three with Distinct Characters

3文字がすべて異なる長さ3の部分文字列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/substrings-of-size-three-with-distinct-characters/)

### 1984. Minimum Difference Between Highest and Lowest of K Scores

得点配列から`k`個を選び、最大値と最小値の差を最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/)

### 2269. Find the K-Beauty of a Number

整数の10進表記から長さ`k`の部分文字列を取り出し、元の整数を割り切る非ゼロ値の個数を数える。

[LeetCode公式ページ](https://leetcode.com/problems/find-the-k-beauty-of-a-number/)

### 2379. Minimum Recolors to Get K Consecutive Black Blocks

長さ`k`の黒いブロックを連続させるために、白から黒へ塗り替える最小個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/)

### 2760. Longest Even Odd Subarray With Threshold

偶数から始まり、偶奇が交互で、全要素がしきい値以下となる最長部分配列を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-even-odd-subarray-with-threshold/)

### 3206. Alternating Groups I

円環状に並ぶ色について、中央のタイルが両隣と異なる長さ3のグループ数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/alternating-groups-i/)

### 3258. Count Substrings That Satisfy K-Constraint I

0の個数または1の個数が`k`以下となる二値部分文字列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/count-substrings-that-satisfy-k-constraint-i/)

## Medium：22問

### 187. Repeated DNA Sequences

DNA文字列内で複数回現れる長さ10の塩基配列をすべて求める。

[LeetCode公式ページ](https://leetcode.com/problems/repeated-dna-sequences/)

### 395. Longest Substring with At Least K Repeating Characters

含まれる各文字が少なくとも`k`回現れる部分文字列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/)

### 424. Longest Repeating Character Replacement

最大`k`文字を置換し、同じ文字だけで構成できる部分文字列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-repeating-character-replacement/)

### 567. Permutation in String

一方の文字列の順列が、もう一方の文字列に部分文字列として含まれるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/permutation-in-string/)

### 713. Subarray Product Less Than K

要素の積が`k`未満となる連続部分配列の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/subarray-product-less-than-k/)

### 904. Fruit Into Baskets

高々2種類の値だけを含む連続部分配列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/fruit-into-baskets/)

### 1004. Max Consecutive Ones III

最大`k`個の0を1へ反転したとき、連続する1の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/max-consecutive-ones-iii/)

### 1156. Swap For Longest Repeated Character Substring

最大1回の文字交換後に得られる、同一文字が連続する部分文字列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/swap-for-longest-repeated-character-substring/)

### 1208. Get Equal Substrings Within Budget

対応する文字の変更コスト合計を予算内に収め、等しくできる部分文字列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/get-equal-substrings-within-budget/)

### 1234. Replace the Substring for Balanced String

部分文字列を1つ置換し、`Q`、`W`、`E`、`R`を同数にするための最短置換長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/replace-the-substring-for-balanced-string/)

### 1297. Maximum Number of Occurrences of a Substring

異なる文字数と長さの条件を満たす部分文字列について、最大出現回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-number-of-occurrences-of-a-substring/)

### 1343. Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

平均値がしきい値以上となる長さ`k`の連続部分配列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

### 1358. Number of Substrings Containing All Three Characters

`a`、`b`、`c`をすべて1文字以上含む部分文字列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/)

### 1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

最大値と最小値の差が`limit`以下となる連続部分配列の最長長を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

### 1456. Maximum Number of Vowels in a Substring of Given Length

長さ`k`の部分文字列に含まれる母音数の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/)

### 1493. Longest Subarray of 1's After Deleting One Element

要素をちょうど1つ削除した後に残る、1だけの最長連続区間を求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/)

### 1658. Minimum Operations to Reduce X to Zero

配列の左端または右端から要素を取り除き、合計を`x`にする最小操作回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/)

### 1695. Maximum Erasure Value

重複要素のない連続部分配列について、要素合計の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-erasure-value/)

### 1838. Frequency of the Most Frequent Element

合計`k`回以内の要素増加後に実現できる、同一値の最大出現回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/frequency-of-the-most-frequent-element/)

### 2024. Maximize the Confusion of an Exam

最大`k`個の解答を反転し、同じ解答が連続する最長区間を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/)

### 2461. Maximum Sum of Distinct Subarrays With Length K

要素がすべて異なる長さ`k`の連続部分配列について、合計の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/)

### 2537. Count the Number of Good Subarrays

値が等しいインデックスの組を少なくとも`k`個含む連続部分配列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/count-the-number-of-good-subarrays/)

## Hard：10問

### 220. Contains Duplicate III

インデックス差と値の差がそれぞれ指定上限以内となる要素ペアが存在するか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/contains-duplicate-iii/)

### 480. Sliding Window Median

配列上を移動する長さ`k`の各ウィンドウについて、中央値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/sliding-window-median/)

### 632. Smallest Range Covering Elements from K Lists

`k`個のソート済みリストそれぞれから少なくとも1要素を含む、最小の数値範囲を求める。

[LeetCode公式ページ](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)

### 689. Maximum Sum of 3 Non-Overlapping Subarrays

重ならない長さ`k`の部分配列を3つ選び、合計を最大化する開始位置を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/)

### 1425. Constrained Subsequence Sum

選択する隣接インデックス間の距離を`k`以下に制限し、空でない部分列の最大合計を求める。

[LeetCode公式ページ](https://leetcode.com/problems/constrained-subsequence-sum/)

### 1499. Max Value of Equation

`x`座標の差が`k`以下となる2点を選び、指定された式の最大値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/max-value-of-equation/)

### 1703. Minimum Adjacent Swaps for K Consecutive Ones

二値配列内の`k`個の1を連続させるために必要な、隣接交換の最小回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-adjacent-swaps-for-k-consecutive-ones/)

### 2009. Minimum Number of Operations to Make Array Continuous

配列を、重複がなく最大値と最小値の差が要素数より1小さい状態へ変える最小操作回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-number-of-operations-to-make-array-continuous/)

### 2302. Count Subarrays With Score Less Than K

要素合計と長さの積で定義されるスコアが`k`未満の連続部分配列を数える。

[LeetCode公式ページ](https://leetcode.com/problems/count-subarrays-with-score-less-than-k/)

### 2398. Maximum Number of Robots Within Budget

連続するロボットを同時稼働させる費用が予算内となる、最大台数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/maximum-number-of-robots-within-budget/)
