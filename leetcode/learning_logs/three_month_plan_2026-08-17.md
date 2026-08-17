# LeetCode 3か月全問一巡計画

## 目的

2026年8月17日から11月16日までの92日間で、LeetCodeの問題セットを一巡する。

問題セットの取得時点の総数は4,028問で、難易度別の内訳は次の通り。

| 難易度 | 問題数 |
|---|---:|
| Easy | 960 |
| Medium | 2,103 |
| Hard | 965 |
| 合計 | 4,028 |

問題数は新規追加や公開状態の変更で変動するため、実行開始時に公式Problemsetを再確認する。

## 1日の処理量

92日で4,028問を一巡するには、1日平均で約43.8問が必要になる。

配分は次の通り。

```text
72日間: 44問
20日間: 43問
合計: 4,028問
```

難易度別には、毎日おおむね次の量を処理する。

```text
Easy: 10〜11問
Medium: 22〜23問
Hard: 10〜11問
```

## 毎日の学習単位

### 深く学ぶ3問

その日の主テーマから、次の3問を選ぶ。

```text
Easy 1問
Medium 1問
Hard 1問
```

この3問については、問題文、例題、解法、コード、計算量、正しさ、一個下のレイヤーまで確認する。

### カバレッジ問題

残りの40〜41問は、同じ主テーマまたは隣接テーマから選ぶ。

カバレッジ問題は、次の情報を確認した時点で一巡済みとする。

- 問題の目的と入力・出力
- 制約
- 解法の方針
- コードを実行できる、または解説を読んで再現できる
- 計算量
- 後で復習するかどうか

問題文は著作権上、公式ページの全文を転載せず、短い日本語要約、入力・出力の要点、制約、公式リンクを表示する。

## 「今日の問題」運用

ユーザーが「今日の問題」と送ったら、Asia/Tokyoの当日を基準に次を行う。

1. この計画から当日のDayと主テーマを決める。
2. 実行ログから、すでに完了または提示済みの問題を除外する。
3. 深く学ぶEasy／Medium／Hardを1問ずつ提示する。
4. カバレッジ目標数の問題を、短い問題文要約付きで提示する。
5. 公式LeetCodeリンクを付ける。
6. 解法・答え・詳細解説は、ユーザーが求めるまで表示しない。

カバレッジ問題は、深く学ぶ3問と重複させない。

主テーマが狭く、同じタグだけで目標数を集められない場合は、隣接するパターンを明示して補う。

例として、Binary Searchの日には、通常の二分探索、境界探索、回転配列、答えの二分探索を同じテーマ群として扱う。

## 92日間の主テーマ

主テーマは毎日切り替える。

同じ大分類が再登場する場合も、基本、応用、最適化、設計などのサブテーマを変える。

### Day 1〜23

| Day | 主テーマ |
|---:|---|
| 1 | ゲーム理論基礎・勝ち状態と負け状態 |
| 2 | 配列の走査・最大値・最小値・累積処理 |
| 3 | Hash Table・頻度カウント |
| 4 | Set・重複除去・存在確認 |
| 5 | Two Pointers |
| 6 | Sliding Window |
| 7 | Prefix Sum |
| 8 | Difference Array・区間更新 |
| 9 | Sorting・比較関数・カスタムソート |
| 10 | Binary Search・完全一致探索 |
| 11 | Binary Search・境界探索 |
| 12 | Binary Search on Answer |
| 13 | Greedy・局所的な最適選択 |
| 14 | Interval・区間の統合 |
| 15 | Stack・括弧・後入れ先出し |
| 16 | Monotonic Stack |
| 17 | Queue・Deque |
| 18 | Heap・Priority Queue |
| 19 | Linked List・基本操作 |
| 20 | Linked List・反転・Fast／Slow Pointer |
| 21 | String Parsing・文字列の読み取り |
| 22 | Anagram・文字頻度 |
| 23 | Palindrome・回文・対称性 |

### Day 24〜46

| Day | 主テーマ |
|---:|---|
| 24 | Simulation・状態を順番に更新する問題 |
| 25 | Bit Manipulation・ビットシフト・AND・OR |
| 26 | XOR・ビットマスク |
| 27 | 数学・約数・剰余 |
| 28 | GCD・LCM・ユークリッドの互除法 |
| 29 | 素数・エラトステネスの篩・素因数分解 |
| 30 | Matrix・行列の走査 |
| 31 | Grid Simulation・盤面シミュレーション |
| 32 | Backtracking・部分集合 |
| 33 | Backtracking・組み合わせ |
| 34 | Backtracking・順列 |
| 35 | Backtracking・制約と枝刈り |
| 36 | Recursion・Divide and Conquer |
| 37 | Binary Tree・前順・中順・後順走査 |
| 38 | Binary Search Tree |
| 39 | Tree Path・深さ・高さ・直径 |
| 40 | Lowest Common Ancestor・祖先探索 |
| 41 | Tree Construction・復元・シリアライズ |
| 42 | Tree DP |
| 43 | Trie・Prefix Tree |
| 44 | Union-Find・Disjoint Set Union |
| 45 | Graph Representation・隣接リスト・隣接行列 |
| 46 | Graph BFS・DFS・連結成分 |

### Day 47〜69

| Day | 主テーマ |
|---:|---|
| 47 | Topological Sort・依存関係 |
| 48 | Bipartite Graph・二部グラフ・彩色 |
| 49 | Unweighted Shortest Path |
| 50 | Grid BFS・迷路・島 |
| 51 | Dijkstra・非負重み最短経路 |
| 52 | 0-1 BFS・重み0と1のグラフ |
| 53 | Bellman-Ford・Floyd-Warshall |
| 54 | Minimum Spanning Tree |
| 55 | Bridge・Articulation Point・SCC |
| 56 | DAG・Graph DP |
| 57 | Graph State Compression・ビットマスク |
| 58 | Network Flow・Matching |
| 59 | 1D Dynamic Programming |
| 60 | House Robber・State Machine DP |
| 61 | Knapsack・ナップサック |
| 62 | Subset DP・Partition DP |
| 63 | LIS・Longest Increasing Subsequence |
| 64 | LCS・String DP・Edit Distance |
| 65 | Grid DP |
| 66 | Interval DP |
| 67 | Range DP・Partition DP |
| 68 | Digit DP |
| 69 | Game Theory・Minimax・ゲームDP |

### Day 70〜92

| Day | 主テーマ |
|---:|---|
| 70 | Advanced Tree DP |
| 71 | Stock・Trading DP |
| 72 | Bitmask DP |
| 73 | Probability・Expected Value DP |
| 74 | Monotonic Queue Optimization |
| 75 | Divide and Conquer Optimization |
| 76 | Combinatorics・組み合わせ数学 |
| 77 | Number Theory・高度な剰余計算 |
| 78 | Geometry・幾何 |
| 79 | Sweep Line |
| 80 | Coordinate Compression |
| 81 | Fenwick Tree・Binary Indexed Tree |
| 82 | Segment Tree・Range Query |
| 83 | Sparse Table・静的区間クエリ |
| 84 | Advanced Heap・Median・Data Stream |
| 85 | Advanced Trie・XOR Trie |
| 86 | Design・LRU Cache・LFU Cache |
| 87 | Design・Iterator・Data Stream |
| 88 | SQL・SELECT・GROUP BY・集計 |
| 89 | SQL・JOIN・Subquery |
| 90 | SQL・Window Function・Date・String |
| 91 | Shell・Concurrency・Database周辺 |
| 92 | 未着手・未解決・Hard・Premiumの最終監査 |

## 完了状態

各問題は、次の状態で記録する。

| 状態 | 意味 |
|---|---|
| `planned` | 今日の候補として割り当て済み |
| `attempted` | 自力で考えたが、まだ提出・確認中 |
| `solved` | 自力でAcceptedまで到達 |
| `editorial` | 解説を確認して実装できた |
| `revisit` | 復習が必要 |
| `blocked` | 問題文・Premium権限・環境などで進められない |

3か月の一巡条件は、`solved` または `editorial` にすること。

すべてを自力で解くことは、3か月後の2周目の目標とする。
