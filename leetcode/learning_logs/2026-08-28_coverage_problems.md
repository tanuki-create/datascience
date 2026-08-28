# 2026年8月28日：カバレッジ問題文セット

## 対象

- Day: 12
- 主テーマ: Binary Search on Answer
- 問題数: 41問
- 内訳: Easy 9問、Medium 22問、Hard 10問
- 深掘り3問: `1608`、`875`、`3734`。このセットには含めない。
- 状態: `presented`

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約、入力・出力、制約の要点、タグ、公式リンクで整理する。全問について、2026年8月28日時点のLeetCode公式メタデータで公開状態と難易度を確認した。

## Easy：9問

### 888. Fair Candy Swap — Easy

AliceとBobが持つキャンディの箱のサイズから、1箱ずつ交換して両者の総量を同じにできる交換を返す。箱数は各最大`10^4`、サイズは最大`10^5`で、必ず有効解がある。

タグ: Array、Hash Table、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/fair-candy-swap/)

### 1346. Check If N and Its Double Exist — Easy

整数配列に、ある値`N`とその2倍`2N`が異なる添字で存在するか判定する。配列長は`2..500`、要素は`-10^3..10^3`。

タグ: Array、Hash Table、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/check-if-n-and-its-double-exist/)

### 1385. Find the Distance Value Between Two Arrays — Easy

2つの配列について、もう一方のどの要素とも距離`d`以下にならない要素の個数を返す。各配列長は最大`500`、値は`-1000..1000`、`d`は`0..100`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/)

### 2089. Find Target Indices After Sorting Array — Easy

配列を昇順に並べた後、値が`target`になるすべての添字を返す。配列長は最大`100`、要素と`target`は`1..100`。

タグ: Array、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/find-target-indices-after-sorting-array/)

### 2529. Maximum Count of Positive Integer and Negative Integer — Easy

昇順の整数配列に含まれる正数の個数と負数の個数のうち大きい方を返す。配列長は最大`2000`、要素は`-2000..2000`。

タグ: Array、Binary Search、Counting

[LeetCode公式ページ](https://leetcode.com/problems/maximum-count-of-positive-integer-and-negative-integer/)

### 2540. Minimum Common Value — Easy

2つの昇順配列に共通して現れる最小の値を返し、共通値がなければ`-1`を返す。各配列長は最大`10^5`、値は`1..10^9`。

タグ: Array、Hash Table、Two Pointers、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/minimum-common-value/)

### 2824. Count Pairs Whose Sum is Less than Target — Easy

異なる添字のペアで、要素の和が`target`未満になる組数を返す。配列長は`1..50`、値と`target`は`-50..50`。

タグ: Array、Two Pointers、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/count-pairs-whose-sum-is-less-than-target/)

### 860. Lemonade Change — Easy

レモネードを5ドルで販売し、各客の支払いに対して正しい釣り銭を最後まで渡せるか判定する。客数は最大`10^5`、支払いは`5`、`10`、`20`のいずれか。

タグ: Array、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/lemonade-change/)

### 1480. Running Sum of 1d Array — Easy

整数配列の各位置について、先頭からその位置までの累積和を返す。配列長は最大`1000`、要素は`-10^6..10^6`。

タグ: Array、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/running-sum-of-1d-array/)

## Medium：22問

### 167. Two Sum II - Input Array Is Sorted — Medium

昇順配列から、和が`target`になる2要素の添字を返す。配列長は`2..3 * 10^4`で、解はちょうど1つ存在する。

タグ: Array、Two Pointers、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

### 240. Search a 2D Matrix II — Medium

各行・各列が昇順の行列から`target`の存在を判定する。行列の各辺は最大`300`、値と`target`は`-10^9..10^9`。

タグ: Array、Binary Search、Divide and Conquer、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/search-a-2d-matrix-ii/)

### 633. Sum of Square Numbers — Medium

非負整数`c`が、2つの整数の平方和として表せるか判定する。`0 <= c <= 2^31 - 1`。

タグ: Math、Two Pointers、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/sum-of-square-numbers/)

### 1011. Capacity To Ship Packages Within D Days — Medium

重さの順序を保った荷物を`days`日以内に運ぶための船の最小積載量を返す。荷物数は最大`5 * 10^4`、各重量は最大`500`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

### 1201. Ugly Number III — Medium

`a`、`b`、`c`の少なくとも1つで割り切れる正整数のうち、`n`番目の値を返す。各入力は最大`10^9`、答えは`2 * 10^9`以下。

タグ: Math、Binary Search、Combinatorics、Number Theory、Least Common Multiple、Euclidean Algorithm、Greatest Common Divisor、Inclusion-Exclusion Principle

[LeetCode公式ページ](https://leetcode.com/problems/ugly-number-iii/)

### 1482. Minimum Number of Days to Make m Bouquets — Medium

各花の開花日から、隣接する`k`本を使う花束を`m`個作れる最小の日数を返す。不可能なら`-1`。配列長は最大`10^5`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)

### 1552. Magnetic Force Between Two Balls — Medium

異なる位置にあるバスケットへ`m`個のボールを置き、最小距離を最大化した値を返す。位置数は最大`10^5`、座標は最大`10^9`。

タグ: Array、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/magnetic-force-between-two-balls/)

### 1760. Minimum Limit of Balls in a Bag — Medium

袋を分割して、各袋のボール数の最大値を最小化する。分割回数は`10^9`以下、袋数は最大`10^5`、初期個数は最大`10^9`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/)

### 1870. Minimum Speed to Arrive on Time — Medium

列車を乗り継いで制限時間以内に到着するための最小速度を返し、不可能なら`-1`を返す。区間数は最大`10^5`、距離は最大`10^5`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/)

### 1898. Maximum Number of Removable Characters — Medium

指定位置の文字を削除しても`p`が`s`の部分列であり続けるように、削除できる最大回数を返す。`s`の長さは最大`10^5`。

タグ: Array、Two Pointers、String、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/maximum-number-of-removable-characters/)

### 1901. Find a Peak Element II — Medium

隣接セルと異なる整数行列から、上下左右の隣接値より大きいピークセルの位置を1つ返す。行・列数は各最大`500`。

タグ: Array、Binary Search、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/find-a-peak-element-ii/)

### 2055. Plates Between Candles — Medium

ろうそくと皿からなる文字列について、指定区間内で両端をろうそくに囲まれた皿の数を各問い合わせに返す。文字列長・問い合わせ数は各最大`10^5`。

タグ: Array、String、Binary Search、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/plates-between-candles/)

### 2064. Minimized Maximum of Products Distributed to Any Store — Medium

各種類の商品を店舗へ分配し、各店舗の商品数の最大値を最小化する。店舗数・種類数は最大`10^5`、各数量は最大`10^5`。

タグ: Array、Binary Search、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/)

### 2070. Most Beautiful Item for Each Query — Medium

商品ごとの価格と美しさに対し、各予算以下で購入できる商品の最大美しさを返す。商品数・問い合わせ数は各最大`10^5`、価格と美しさは最大`10^9`。

タグ: Array、Binary Search、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/most-beautiful-item-for-each-query/)

### 2187. Minimum Time to Complete Trips — Medium

各バスの所要時間と必要な総便数から、全便を完了する最小時間を返す。バス数は最大`10^5`、所要時間と総便数は最大`10^7`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/minimum-time-to-complete-trips/)

### 2226. Maximum Candies Allocated to K Children — Medium

複数の箱のキャンディを分割し、`k`人へ同数ずつ配れる最大個数を返す。箱数は最大`10^5`、各箱は最大`10^7`、`k`は最大`10^12`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/)

### 2439. Minimize Maximum of Array — Medium

隣接要素間で1ずつ移動できる配列について、操作後の最大値として可能な最小値を返す。配列長は最大`10^5`、要素は最大`10^9`。

タグ: Array、Binary Search、Dynamic Programming、Greedy、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/minimize-maximum-of-array/)

### 2517. Maximum Tastiness of Candy Basket — Medium

価格配列から`k`個を選び、選択要素間の最小価格差を最大化した値を返す。価格数は最大`10^5`、価格は最大`10^9`。

タグ: Array、Binary Search、Greedy、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/maximum-tastiness-of-candy-basket/)

### 2560. House Robber IV — Medium

隣接家を同時に選ばずに少なくとも`k`軒を選ぶとき、選択した家の金額の最大値を最小化する。配列長は最大`10^5`、金額は最大`10^9`。

タグ: Array、Binary Search、Dynamic Programming、Greedy

[LeetCode公式ページ](https://leetcode.com/problems/house-robber-iv/)

### 2616. Minimize the Maximum Difference of Pairs — Medium

配列から`p`組の非共有ペアを選び、各ペアの差の最大値を最小化する。配列長は最大`10^5`、値は最大`10^9`。

タグ: Array、Binary Search、Dynamic Programming、Greedy、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/)

### 2812. Find the Safest Path in a Grid — Medium

盗賊の位置を含む正方形グリッドで、通過セルと盗賊との距離の最小値を最大化する経路の安全度を返す。辺の長さは最大`400`。

タグ: Array、Binary Search、Breadth-First Search、Union-Find、Heap (Priority Queue)、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/find-the-safest-path-in-a-grid/)

### 2861. Maximum Number of Alloys — Medium

複数の合金組成と在庫・単価・予算から、1種類の組成を選んで作れる合金数の最大値を返す。元素数・組成数は最大`100`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/maximum-number-of-alloys/)

## Hard：10問

### 2040. Kth Smallest Product of Two Sorted Arrays — Hard

2つの昇順配列から1要素ずつ選んだ全積のうち、`k`番目に小さい値を返す。各配列長は最大`5 * 10^4`、要素は`-10^5..10^5`。

タグ: Array、Binary Search

[LeetCode公式ページ](https://leetcode.com/problems/kth-smallest-product-of-two-sorted-arrays/)

### 2141. Maximum Running Time of N Computers — Hard

複数のバッテリーを使って`n`台のコンピューターを同時稼働できる最大時間を返す。`n`は最大`10^5`、バッテリー数も最大`10^5`、容量は最大`10^9`。

タグ: Array、Binary Search、Greedy、Sorting

[LeetCode公式ページ](https://leetcode.com/problems/maximum-running-time-of-n-computers/)

### 2528. Maximize the Minimum Powered City — Hard

発電所の追加配置を`k`回まで行い、各都市の供給電力の最小値を最大化する。都市数は最大`10^5`、追加数は最大`10^9`。

タグ: Array、Binary Search、Greedy、Queue、Sliding Window、Prefix Sum

[LeetCode公式ページ](https://leetcode.com/problems/maximize-the-minimum-powered-city/)

### 3134. Find the Median of the Uniqueness Array — Hard

すべての部分配列について異なる値の個数を並べた配列の中央値を求める。入力配列の長さと値は最大`10^5`。

タグ: Array、Hash Table、Binary Search、Sliding Window

[LeetCode公式ページ](https://leetcode.com/problems/find-the-median-of-the-uniqueness-array/)

### 732. My Calendar III — Hard

時間区間の予約を順に追加し、各追加後に同時開催される予約数の最大値を返す。時刻は`0..10^9`、予約追加は最大`400`回。

タグ: Binary Search、Design、Segment Tree、Prefix Sum、Ordered Set

[LeetCode公式ページ](https://leetcode.com/problems/my-calendar-iii/)

### 1970. Last Day Where You Can Still Cross — Hard

日ごとに水没するセルが増える行列で、上端から下端へ渡れる最後の日を返す。行列のセル数は最大`2 * 10^4`で、各セルは一度だけ水没する。

タグ: Array、Binary Search、Depth-First Search、Breadth-First Search、Union-Find、Matrix

[LeetCode公式ページ](https://leetcode.com/problems/last-day-where-you-can-still-cross/)

### 778. Swim in Rising Water — Hard

高さが異なる正方形グリッドで、水位が上がる中、左上から右下へ到達できる最小時刻を返す。辺の長さは最大`50`で、高さは一意。

タグ: Array、Binary Search、Depth-First Search、Breadth-First Search、Union-Find、Minimax、Heap (Priority Queue)、Matrix、Dijkstra's Algorithm

[LeetCode公式ページ](https://leetcode.com/problems/swim-in-rising-water/)

### 878. Nth Magical Number — Hard

`a`または`b`で割り切れる正整数を小さい順に並べたとき、`n`番目の値を`10^9+7`で割った余りを返す。`n <= 10^9`、`a,b <= 4 * 10^4`。

タグ: Math、Binary Search、Least Common Multiple、Inclusion-Exclusion Principle

[LeetCode公式ページ](https://leetcode.com/problems/nth-magical-number/)

### 887. Super Egg Drop — Hard

`k`個の卵と`n`階建ての建物で、卵が割れる階の境界を特定するための最小試行回数を返す。`k <= 100`、`n <= 10^4`。

タグ: Math、Binary Search、Dynamic Programming

[LeetCode公式ページ](https://leetcode.com/problems/super-egg-drop/)

### 1044. Longest Duplicate Substring — Hard

文字列内に2回以上現れる重複部分文字列のうち最長のものを返し、なければ空文字列を返す。文字列長は`2..3 * 10^4`で、小文字英字のみ。

タグ: String、Binary Search、Sliding Window、Rolling Hash、Suffix Array、Hash Function、Suffix Automaton、Suffix Tree、Z Algorithm、Boyer–Moore String-Search Algorithm

[LeetCode公式ページ](https://leetcode.com/problems/longest-duplicate-substring/)
