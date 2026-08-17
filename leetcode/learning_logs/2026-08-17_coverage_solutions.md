# 2026年8月17日：カバレッジ解法セット

## 対象

- Day: 1
- 主テーマ: ゲーム理論・状態DP・区間DP
- 対象: カバレッジ41問
- 深掘り3問: `1025`、`877`、`1563`。別途詳細解説する。

以下は、各問題を短時間で一巡するための解法方針と計算量である。

## Easy：9問

| 問題 | 解法方針 | 計算量 |
|---|---|---|
| [70. Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | `dp[i] = dp[i-1] + dp[i-2]`のFibonacci型DP。 | `O(n)` / `O(1)` |
| [509. Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | 直前2値を保持して数列を反復計算する。 | `O(n)` / `O(1)` |
| [746. Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | 1段前・2段前からの最小コストを更新する。 | `O(n)` / `O(1)` |
| [1137. N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) | 直前3項をローリング更新する。 | `O(n)` / `O(1)` |
| [121. Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 最安購入価格と、その時点までの最大利益を保持する。 | `O(n)` / `O(1)` |
| [338. Counting Bits](https://leetcode.com/problems/counting-bits/) | `i`を右シフトした値と最下位ビットから個数を再利用する。 | `O(n)` / `O(n)` |
| [303. Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | Prefix Sumを作り、`prefix[r+1]-prefix[l]`で答える。 | 構築`O(n)`、問合せ`O(1)` |
| [455. Assign Cookies](https://leetcode.com/problems/assign-cookies/) | 欲求度とクッキーをソートし、小さい要求から貪欲に割り当てる。 | `O(n log n)` |
| [392. Is Subsequence](https://leetcode.com/problems/is-subsequence/) | 2ポインタで、必要な文字を順番に探す。 | `O(n)` / `O(1)` |

## Medium：22問

| 問題 | 解法方針 | 計算量 |
|---|---|---|
| [486. Predict the Winner](https://leetcode.com/problems/predict-the-winner/) | 区間ごとの「手番側−相手」の最大得点差をDPする。 | `O(n²)` / `O(n)`〜 |
| [1140. Stone Game II](https://leetcode.com/problems/stone-game-ii/) | `index`と取得上限`M`を状態にして、取る数を全探索する。 | `O(n³)` / `O(n²)` |
| [1690. Stone Game VII](https://leetcode.com/problems/stone-game-vii/) | Prefix Sumで残り区間の合計を求め、区間の得点差をDPする。 | `O(n²)` / `O(n²)` |
| [1686. Stone Game VI](https://leetcode.com/problems/stone-game-vi/) | `aliceValue + bobValue`の降順で並べ、手番ごとに取得する。 | `O(n log n)` / `O(n)` |
| [1908. Game of Nim](https://leetcode.com/problems/game-of-nim/) | 各山のXORを計算し、XORが0かどうかで勝敗を判定する。 | `O(n)` / `O(1)` |
| [464. Can I Win](https://leetcode.com/problems/can-i-win/) | 使用済み集合をビットマスクで表し、状態をメモ化する。 | `O(n·2ⁿ)` / `O(2ⁿ)` |
| [294. Flip Game II](https://leetcode.com/problems/flip-game-ii/) | 可能な反転を試し、相手を負け状態にできるかメモ化DFSで判定する。 | 指数時間 |
| [375. Guess Number Higher or Lower II](https://leetcode.com/problems/guess-number-higher-or-lower-ii/) | 各区間で最初に選ぶ値を試し、最悪コストの最小値を取る。 | `O(n³)` / `O(n²)` |
| [198. House Robber](https://leetcode.com/problems/house-robber/) | `取らない場合`と`2つ前から取る場合`の最大値を更新する。 | `O(n)` / `O(1)` |
| [213. House Robber II](https://leetcode.com/problems/house-robber-ii/) | 先頭を除く区間と末尾を除く区間を別々に解く。 | `O(n)` / `O(1)` |
| [337. House Robber III](https://leetcode.com/problems/house-robber-iii/) | 各ノードについて、親子を取らない場合の2状態を返す。 | `O(n)` / `O(h)` |
| [1043. Partition Array for Maximum Sum](https://leetcode.com/problems/partition-array-for-maximum-sum/) | 最後の区間長を1から`k`まで試し、区間最大値を掛ける。 | `O(nk)` / `O(n)` |
| [1039. Minimum Score Triangulation of Polygon](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/) | 区間の最後の三角形を作る頂点を全探索する。 | `O(n³)` / `O(n²)` |
| [1130. Minimum Cost Tree From Leaf Values](https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/) | 区間DPで左右の木を分割するか、単調スタックで近い大きい値を処理する。 | DP:`O(n³)`、Stack:`O(n)` |
| [1312. Minimum Insertion Steps to Make a String Palindrome](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/) | 区間の両端が同じかを見て、挿入数の最小値をDPする。 | `O(n²)` / `O(n²)` |
| [97. Interleaving String](https://leetcode.com/problems/interleaving-string/) | `s1`を何文字、`s2`を何文字使ったかを状態にする。 | `O(mn)` / `O(n)` |
| [139. Word Break](https://leetcode.com/problems/word-break/) | 各位置まで辞書単語で到達できるかをDPする。 | `O(n²)` / `O(n)` |
| [300. Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | `tails`に各長さの最小末尾を保持し、二分探索で更新する。 | `O(n log n)` / `O(n)` |
| [322. Coin Change](https://leetcode.com/problems/coin-change/) | 金額ごとの最小枚数を完全ナップサックDPで計算する。 | `O(n·amount)` / `O(amount)` |
| [518. Coin Change II](https://leetcode.com/problems/coin-change-ii/) | コインを外側のループに置き、重複しない組合せ数を数える。 | `O(n·amount)` / `O(amount)` |
| [416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 合計の半分を作れるかを0/1ナップサックで判定する。 | `O(n·sum)` / `O(sum)` |
| [494. Target Sum](https://leetcode.com/problems/target-sum/) | `+`側の合計を部分集合和へ変換して数える。 | `O(n·sum)` / `O(sum)` |

## Hard：10問

| 問題 | 解法方針 | 計算量 |
|---|---|---|
| [1510. Stone Game IV](https://leetcode.com/problems/stone-game-iv/) | 各平方数を取った後が負け状態かを1次元DPする。 | `O(n√n)` / `O(n)` |
| [1872. Stone Game VIII](https://leetcode.com/problems/stone-game-viii/) | Prefix Sumを作り、右端から得点差の最大値を更新する。 | `O(n)` / `O(n)` |
| [913. Cat and Mouse](https://leetcode.com/problems/cat-and-mouse/) | ゲーム状態の勝敗を、終端状態から逆向きに確定する。 | `O(n³)` / `O(n³)` |
| [1728. Cat and Mouse II](https://leetcode.com/problems/cat-and-mouse-ii/) | 位置・手番・残りターンを状態にして、メモ化探索する。 | 状態数×遷移数 |
| [312. Burst Balloons](https://leetcode.com/problems/burst-balloons/) | 最後に割る風船を固定し、左右区間のDPを組み合わせる。 | `O(n³)` / `O(n²)` |
| [546. Remove Boxes](https://leetcode.com/problems/remove-boxes/) | 右端と同色の連続個数を状態に持つ3次元DP。 | おおむね`O(n⁴)` / `O(n³)` |
| [664. Strange Printer](https://leetcode.com/problems/strange-printer/) | 同じ文字の端点を同じ印刷操作としてまとめる区間DP。 | `O(n³)` / `O(n²)` |
| [1000. Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/) | 区間DPに、K個へ分割できるかの剰余条件を加える。 | `O(n³)` / `O(n²)` |
| [1547. Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/) | 切断点をソートし、区間で最初に切る位置を試す。 | `O(m³)` / `O(m²)` |
| [1335. Minimum Difficulty of a Job Schedule](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/) | 日数と仕事の終端を状態にし、各日の最大難易度を更新する。 | `O(dn²)` / `O(dn)` |

## 学習状態

カバレッジ問題の解法方針を確認した後、各問題を次の状態に分類する。

```text
solved   : 自力でAccepted
editorial: 解説を見て実装
revisit  : 後日再挑戦
blocked  : Premium・環境などで進められない
```
