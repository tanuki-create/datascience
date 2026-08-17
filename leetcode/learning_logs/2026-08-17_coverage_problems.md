# 2026年8月17日：カバレッジ問題文セット

## 対象

- Day: 1
- 主テーマ: ゲーム理論・状態DP・区間DP
- 問題数: 41問
- 深掘り3問: `1025`、`877`、`1563`。このセットには含めない。

問題文は著作権上、公式本文の全文転載ではなく、短い日本語要約と公式リンクで整理する。

## Easy：9問

### 70. Climbing Stairs

階段を1段または2段ずつ上るとき、最上段へ到達する方法数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/climbing-stairs/)

### 509. Fibonacci Number

Fibonacci数列の`n`番目の値を求める。

[LeetCode公式ページ](https://leetcode.com/problems/fibonacci-number/)

### 746. Min Cost Climbing Stairs

1段または2段ずつ進み、階段を上り切るための最小コストを求める。

[LeetCode公式ページ](https://leetcode.com/problems/min-cost-climbing-stairs/)

### 1137. N-th Tribonacci Number

直前3項の合計で定義されるTribonacci数列の`n`番目を求める。

[LeetCode公式ページ](https://leetcode.com/problems/n-th-tribonacci-number/)

### 121. Best Time to Buy and Sell Stock

株価の配列から、1回の売買で得られる最大利益を求める。

[LeetCode公式ページ](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

### 338. Counting Bits

`0`から`n`までの各整数について、2進表現に含まれる1の個数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/counting-bits/)

### 303. Range Sum Query - Immutable

固定配列に対する複数の区間和の問い合わせに答える。

[LeetCode公式ページ](https://leetcode.com/problems/range-sum-query-immutable/)

### 455. Assign Cookies

子どもの欲求度とクッキーの大きさを対応付け、満足できる子どもの人数を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/assign-cookies/)

### 392. Is Subsequence

文字列`t`が、文字列`s`から順番を保って文字を選んだ部分列か判定する。

[LeetCode公式ページ](https://leetcode.com/problems/is-subsequence/)

## Medium：22問

### 486. Predict the Winner

配列の両端から数を取り、両者が最適に動いたときに先手の得点が相手以上になるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/predict-the-winner/)

### 1140. Stone Game II

先頭から取れる石の最大数が手番ごとに変化するゲームで、Aliceの最大得点を求める。

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-ii/)

### 1690. Stone Game VII

両端から石を取り、残った区間の合計を得点にするゲームの最終得点差を求める。

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-vii/)

### 1686. Stone Game VI

各石にAlice用とBob用の価値があり、交互に石を取ったときの勝者を判定する。

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-vi/)

### 1908. Game of Nim

複数の石の山から任意個を取り、最後に手を打つプレイヤーを競うゲームの勝敗を判定する。

[LeetCode公式ページ](https://leetcode.com/problems/game-of-nim/)

### 464. Can I Win

未使用の整数を交互に選び、累積値を目標以上にできるプレイヤーが勝つゲームを判定する。

[LeetCode公式ページ](https://leetcode.com/problems/can-i-win/)

### 294. Flip Game II

文字列中の`++`を`--`へ反転する手を交互に行い、先手が勝てるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/flip-game-ii/)

### 375. Guess Number Higher or Lower II

数字を選んで外した場合のコストが発生するゲームで、最悪ケースのコストを最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/guess-number-higher-or-lower-ii/)

### 198. House Robber

隣接する家を同時に選ばず、盗める金額を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/house-robber/)

### 213. House Robber II

家が円環状に並ぶ場合に、隣接する家を同時に選ばず盗める金額を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/house-robber-ii/)

### 337. House Robber III

家が二分木状に並び、親子関係にある家を同時に選ばず盗める金額を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/house-robber-iii/)

### 1043. Partition Array for Maximum Sum

配列を長さ制限付きの区間へ分割し、各区間の最大値と長さの積の合計を最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/partition-array-for-maximum-sum/)

### 1039. Minimum Score Triangulation of Polygon

多角形を三角形へ分割したときのスコアを最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/)

### 1130. Minimum Cost Tree From Leaf Values

葉の値を保った二分木を作り、非葉ノードの積の合計を最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/)

### 1312. Minimum Insertion Steps to Make a String Palindrome

文字列を回文にするために必要な最小挿入回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)

### 97. Interleaving String

2つの文字列から順番を保って文字を取り出し、目標文字列を作れるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/interleaving-string/)

### 139. Word Break

辞書にある単語を連結して、入力文字列を作れるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/word-break/)

### 300. Longest Increasing Subsequence

配列から選べる最長の狭義単調増加部分列の長さを求める。

[LeetCode公式ページ](https://leetcode.com/problems/longest-increasing-subsequence/)

### 322. Coin Change

指定されたコインを使って金額を作るための最小枚数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/coin-change/)

### 518. Coin Change II

指定されたコインの組み合わせで金額を作る方法数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/coin-change-ii/)

### 416. Partition Equal Subset Sum

配列を合計が等しい2つの集合へ分割できるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/partition-equal-subset-sum/)

### 494. Target Sum

各要素に`+`または`-`を付け、目標値を作る方法数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/target-sum/)

## Hard：10問

### 1510. Stone Game IV

1回に平方数個の石を取るゲームで、両者が最適に動いたときの勝敗を判定する。

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-iv/)

### 1872. Stone Game VIII

石列をまとめる操作を行い、Aliceが得られる最大の得点差を求める。

[LeetCode公式ページ](https://leetcode.com/problems/stone-game-viii/)

### 913. Cat and Mouse

グラフ上でMouseとCatが交互に移動し、Mouseの勝利・Catの勝利・引き分けを判定する。

[LeetCode公式ページ](https://leetcode.com/problems/cat-and-mouse/)

### 1728. Cat and Mouse II

グリッド上でMouseとCatが移動し、制限ターン内にMouseが逃げ切れるか判定する。

[LeetCode公式ページ](https://leetcode.com/problems/cat-and-mouse-ii/)

### 312. Burst Balloons

風船を割る順番を選び、得られるコインを最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/burst-balloons/)

### 546. Remove Boxes

同色の連続した箱を消し、得られるスコアを最大化する。

[LeetCode公式ページ](https://leetcode.com/problems/remove-boxes/)

### 664. Strange Printer

1回の印刷で同じ文字を連続範囲に印刷し、目標文字列を作る最小印刷回数を求める。

[LeetCode公式ページ](https://leetcode.com/problems/strange-printer/)

### 1000. Minimum Cost to Merge Stones

隣接するK個の石の山を統合し、すべてを統合する最小コストを求める。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-cost-to-merge-stones/)

### 1547. Minimum Cost to Cut a Stick

指定された位置で棒を切る順番を選び、切断コストを最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/)

### 1335. Minimum Difficulty of a Job Schedule

順序を保った仕事をD日へ分け、各日の最大難易度の合計を最小化する。

[LeetCode公式ページ](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/)
