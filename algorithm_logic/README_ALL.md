# Algorithm Logic Series - アルゴリズム・データ構造ロジック解説シリーズ

## 概要

このシリーズは、LeetCodeやAtCoderで頻出のアルゴリズムとデータ構造の**ロジック**に焦点を当てた解説集です。コードの実装詳細よりも、**なぜそのアプローチが有効なのか**、**どのように思考を進めるのか**を理解することを目的としています。

### このシリーズの特徴

- **ロジック重視**: コードは最小限に抑え、アルゴリズムの本質的な思考プロセスを解説
- **段階的学習**: Easy → Medium → Hard の順で難易度を上げながら学習
- **実践的**: 現実世界での応用例や実際の使用場面を豊富に紹介
- **視覚的説明**: 図や表を使って理解を促進
- **相互参照**: 関連するテクニックや問題へのリンクを充実

## ディレクトリ構造

```
algorithm_logic/
├── README.md                          # このファイル（シリーズ全体のインデックス）
├── 01_hash_table/                     # ハッシュテーブル
├── 02_two_pointers/                   # 二ポインタ
├── 03_sliding_window/                 # スライディングウィンドウ
├── 04_stack_queue/                    # スタック・キュー
├── 05_binary_search/                  # 二分探索
├── 06_sorting/                        # ソート
├── 07_dynamic_programming/            # 動的計画法
├── 08_greedy/                         # 貪欲法
├── 09_tree_traversal/                 # 木の探索
├── 10_graph_algorithms/               # グラフアルゴリズム
├── 11_string_manipulation/            # 文字列処理
├── 12_bit_manipulation/               # ビット操作
├── 13_mathematical/                  # 数学的アルゴリズム
├── 14_backtracking/                   # バックトラッキング（Phase 5）
├── 15_trie/                           # トライ木（Phase 5）
├── 16_union_find/                     # Union-Find（Phase 5）
├── 17_heap/                           # ヒープ（Phase 5）
├── 18_divide_conquer/                 # 分割統治法（Phase 6）
├── 19_prefix_sum/                     # 累積和（Phase 6）
├── 20_linked_list/                    # リンクリスト（Phase 6）
├── 21_intervals/                      # インターバル問題（Phase 6）
├── 22_advanced_string/                # 高度な文字列アルゴリズム（Phase 7）
├── 23_advanced_graph/                 # 高度なグラフアルゴリズム（Phase 7）
├── 24_advanced_math/                  # 高度な数学的アルゴリズム（Phase 7）
├── 25_segment_tree/                   # セグメント木（Phase 8）
├── 26_coordinate_compression/         # 座標圧縮（Phase 8）
├── 27_design/                         # 設計問題（Phase 8）
└── 28_pattern_recognition/            # 問題パターン識別ガイド（Phase 8）
```

## 学習の進め方

### Phase 1: 基礎テクニック（推奨開始点）

1. **[ハッシュテーブル](01_hash_table/README.md)** - 最も基本的で強力なデータ構造
   - Two Sum
   - Group Anagrams
   - Longest Substring

2. **[二ポインタ](02_two_pointers/README.md)** - 配列や文字列を効率的に処理
   - Valid Palindrome
   - Container With Most Water
   - [3Sum](02_two_pointers/3sum_logic.md)

3. **[スライディングウィンドウ](03_sliding_window/README.md)** - 連続する部分列の問題に最適
   - Longest Substring Without Repeating Characters
   - [Minimum Window Substring](03_sliding_window/minimum_window_substring_logic.md)

### Phase 2: データ構造

4. **[スタック・キュー](04_stack_queue/README.md)** - LIFO/FIFOの特性を活かす
5. **[二分探索](05_binary_search/README.md)** - ソート済み配列での高速検索
6. **[ソート](06_sorting/README.md)** - データの並び替え

### Phase 3: 高度なアルゴリズム

6. **[動的計画法](07_dynamic_programming/README.md)** - 最適化問題の強力な手法
   - [Interval DP](07_dynamic_programming/interval_dp_logic.md)
   - [Bit DP](07_dynamic_programming/bit_dp_logic.md)
7. **[貪欲法](08_greedy/README.md)** - 局所最適解を積み重ねる
8. **[木の探索](09_tree_traversal/README.md)** - DFS/BFSの理解
   - [Tree DP](09_tree_traversal/tree_dp_logic.md)
   - [Tree Diameter](09_tree_traversal/tree_diameter_logic.md)
   - [Centroid Decomposition](09_tree_traversal/centroid_decomposition_logic.md)
   - [Euler Tour](09_tree_traversal/euler_tour_logic.md)

### Phase 4: 専門テクニック

9. **[グラフアルゴリズム](10_graph_algorithms/README.md)** - ネットワーク構造の処理
   - [Number of Islands](10_graph_algorithms/number_of_islands_logic.md)
   - [Topological Sort](10_graph_algorithms/topological_sort_logic.md)
   - [Dijkstra Shortest Path](10_graph_algorithms/dijkstra_shortest_path_logic.md)
10. **[文字列処理](11_string_manipulation/README.md)** - 高度な文字列マッチング
   - [Longest Common Prefix](11_string_manipulation/longest_common_prefix_logic.md)
   - [Word Pattern](11_string_manipulation/word_pattern_logic.md)
   - [Valid Anagram](11_string_manipulation/valid_anagram_logic.md)
11. **[ビット操作](12_bit_manipulation/README.md)** - メモリ効率的な処理
12. **[数学的アルゴリズム](13_mathematical/README.md)** - 数論と組み合わせ論
   - [Power of Two](13_mathematical/power_of_two_logic.md)
   - [Factorial](13_mathematical/factorial_logic.md)
   - [Fibonacci](13_mathematical/fibonacci_logic.md)

### Phase 5: 重要なデータ構造とアルゴリズム

13. **[バックトラッキング](14_backtracking/README.md)** - 全ての解を探索
   - [Generate Parentheses](14_backtracking/generate_parentheses_logic.md)
   - [N-Queens](14_backtracking/n_queens_logic.md)
   - [Sudoku Solver](14_backtracking/sudoku_solver_logic.md)
14. **[トライ木](15_trie/README.md)** - 文字列集合の効率的な管理
   - [Implement Trie](15_trie/implement_trie_logic.md)
   - [Word Search II](15_trie/word_search_ii_logic.md)
15. **[Union-Find](16_union_find/README.md)** - 連結成分の管理
   - [Friend Circles](16_union_find/friend_circles_logic.md)
   - [Redundant Connection](16_union_find/redundant_connection_logic.md)
16. **[ヒープ](17_heap/README.md)** - 優先度付きキュー
   - [Kth Largest Element](17_heap/kth_largest_element_logic.md)
   - [Merge K Sorted Lists](17_heap/merge_k_sorted_lists_logic.md)

### Phase 6: 中級テクニック

17. **[分割統治法](18_divide_conquer/README.md)** - 問題を分割して解決
   - [Merge Sort](18_divide_conquer/merge_sort_logic.md)
   - [Quick Sort](18_divide_conquer/quick_sort_logic.md)
   - [Pow(x, n)](18_divide_conquer/pow_x_n_logic.md)
18. **[累積和](19_prefix_sum/README.md)** - 範囲クエリの効率化
   - [Range Sum Query](19_prefix_sum/range_sum_query_logic.md)
   - [Subarray Sum Equals K](19_prefix_sum/subarray_sum_equals_k_logic.md)
19. **[リンクリスト](20_linked_list/README.md)** - 動的なデータ構造
   - [Reverse Linked List](20_linked_list/reverse_linked_list_logic.md)
   - [Merge Two Sorted Lists](20_linked_list/merge_two_sorted_lists_logic.md)
20. **[インターバル問題](21_intervals/README.md)** - 範囲の処理
   - [Merge Intervals](21_intervals/merge_intervals_logic.md)
   - [Insert Interval](21_intervals/insert_interval_logic.md)

### Phase 7: 高度なアルゴリズム拡張

21. **[高度な文字列アルゴリズム](22_advanced_string/README.md)** - KMP、Rabin-Karp、Manacher
   - [KMP Algorithm](22_advanced_string/kmp_algorithm_logic.md)
   - [Rabin-Karp](22_advanced_string/rabin_karp_logic.md)
   - [Manacher's Algorithm](22_advanced_string/manacher_algorithm_logic.md)
   - [Z-algorithm](22_advanced_string/z_algorithm_logic.md)
22. **[高度なグラフアルゴリズム](23_advanced_graph/README.md)** - トポロジカルソート、最短経路、MST
   - [Topological Sort](23_advanced_graph/topological_sort_logic.md)
   - [Dijkstra Shortest Path](23_advanced_graph/dijkstra_shortest_path_logic.md)
   - [Kruskal MST](23_advanced_graph/kruskal_mst_logic.md)
   - [Strongly Connected Components (SCC)](23_advanced_graph/strongly_connected_components_logic.md)
   - [Bipartite Graph Detection](23_advanced_graph/bipartite_graph_logic.md)
23. **[高度な数学的アルゴリズム](24_advanced_math/README.md)** - GCD、素数、組み合わせ
   - [GCD/LCM](24_advanced_math/gcd_lcm_logic.md)
   - [Sieve of Eratosthenes](24_advanced_math/sieve_of_eratosthenes_logic.md)
   - [Combinatorics](24_advanced_math/combinatorics_logic.md)
   - [Extended Euclidean Algorithm](24_advanced_math/extended_euclidean_logic.md)

### Phase 8: 専門トピック

24. **[セグメント木](25_segment_tree/README.md)** - 範囲クエリと更新（AtCoder特有）
   - [Range Sum Query - Mutable](25_segment_tree/range_sum_query_segment_tree_logic.md)
   - [Range Minimum Query](25_segment_tree/range_minimum_query_logic.md)
   - [Fenwick Tree (Binary Indexed Tree)](25_segment_tree/fenwick_tree_logic.md)
   - [Lazy Segment Tree](25_segment_tree/lazy_segment_tree_logic.md)
25. **[座標圧縮](26_coordinate_compression/README.md)** - 大きな値を小さな整数にマッピング
   - [Coordinate Compression](26_coordinate_compression/coordinate_compression_logic.md)
26. **[設計問題](27_design/README.md)** - 実用的なシステム設計
   - [LRU Cache](27_design/lru_cache_logic.md)
   - [Design Twitter](27_design/design_twitter_logic.md)
   - [Design Hit Counter](27_design/design_hit_counter_logic.md)
27. **[問題パターン識別ガイド](28_pattern_recognition/README.md)** - 問題のパターンを識別
   - [Problem Pattern Guide](28_pattern_recognition/problem_pattern_guide.md)
   - [Technique Combination Guide](28_pattern_recognition/technique_combination_guide.md)
   - [Optimization Techniques](28_pattern_recognition/optimization_techniques.md)

## 各テクニックの構成

各テクニックフォルダには以下のファイルが含まれます：

- **README.md**: テクニックの概要、適用場面、計算量、現実世界での応用例
- **問題名_logic.md**: 個別問題のロジック解説
  - 問題概要
  - ロジックの核心（思考プロセス）
  - 具体例でのトレース
  - 現実世界での応用
  - 注意点と落とし穴
  - 関連問題へのリンク

## 使い方

1. **テクニックのREADMEを読む**: まずは各テクニックの概要を理解
2. **問題のロジック解説を読む**: 具体的な問題を通じて理解を深める
3. **自分で実装してみる**: ロジックを理解したら、実際にコードを書いてみる
4. **関連問題に挑戦**: 同じテクニックを使う他の問題で練習

## 関連リソース

- [LeetCode Problems Collection](../leetcode/README.md) - 問題集と実装例
- [Python Best Practices](../python/README.md) - Pythonicな書き方

## 更新履歴

- 2024: Phase 1（ハッシュテーブル、二ポインタ、スライディングウィンドウ）を追加
- 2024: Phase 2（スタック・キュー、二分探索）を追加
- 2024: Phase 3（動的計画法、貪欲法、木の探索）を追加
- 2024: Phase 4（グラフアルゴリズム、文字列処理、ビット操作、数学的アルゴリズム）を追加
- 2024: Phase 5（バックトラッキング、トライ木、Union-Find、ヒープ）を追加
- 2024: Phase 6（分割統治法、累積和、リンクリスト、インターバル問題）を追加
- 2024: Phase 7（高度な文字列、高度なグラフ、高度な数学的アルゴリズム）を追加
- 2024: Phase 8（セグメント木、座標圧縮、設計問題、問題パターン識別ガイド）を追加
- 2024: 既存セクションへの重要問題を追加（DP: 5問題、Tree: 4問題、Graph: 3問題、String: 4問題、Math: 4問題、Stack/Queue: 3問題）
- 2024: 追加トピックを追加（Fenwick Tree、Lazy Segment Tree、SCC、Z-algorithm、Extended Euclidean、Interval DP、Bit DP、Tree DP、Tree Diameter、Centroid Decomposition、Euler Tour、Bipartite Graph）

---

**注意**: このシリーズはロジックの理解を重視しています。実装の詳細が必要な場合は、[leetcode](../leetcode/)ディレクトリ内の各問題の`solution.py`を参照してください。


---

# 目次

- [ハッシュテーブル (Hash Table)](#ハッシュテーブル-hash-table)


---

# ハッシュテーブル (Hash Table)

## 概要

ハッシュテーブル（ハッシュマップ、辞書）は、キーと値のペアを効率的に保存・検索するデータ構造です。平均的に**O(1)**の時間計算量で要素の挿入、削除、検索が可能なため、アルゴリズム問題で最も頻繁に使用されるデータ構造の一つです。

## 基本概念

### ハッシュテーブルの仕組み

1. **ハッシュ関数**: キーを配列のインデックスに変換する関数
2. **バケット**: 実際にデータを格納する配列の要素
3. **衝突処理**: 異なるキーが同じインデックスにマッピングされた場合の処理方法

#### 視覚的イメージ

```
ハッシュテーブルの構造:

キー "apple"  →  hash("apple") = 3  →  [3] → "りんご"
キー "banana" →  hash("banana") = 1 →  [1] → "バナナ"
キー "cherry" →  hash("cherry") = 3 →  [3] → "さくらんぼ" (衝突)

配列インデックス:  0    1        2    3             4    5
                 ┌──┐ ┌──────┐ ┌──┐ ┌──────────┐ ┌──┐ ┌──┐
                 │  │ │banana│ │  │ │apple     │ │  │ │  │
                 │  │ │バナナ│ │  │ │りんご    │ │  │ │  │
                 └──┘ └──────┘ └──┘ └──────────┘ └──┘ └──┘
                                    │
                                    ▼
                                 ┌──────────┐
                                 │cherry    │ (チェイニング)
                                 │さくらんぼ│
                                 └──────────┘

衝突処理（チェイニング方式）:
同じインデックスに複数の要素を連結リストで保存
```

### 主な操作と計算量

| 操作 | 平均時間計算量 | 最悪時間計算量 | 空間計算量 |
|------|--------------|--------------|-----------|
| 検索 | O(1) | O(n) | O(n) |
| 挿入 | O(1) | O(n) | O(n) |
| 削除 | O(1) | O(n) | O(n) |

**注意**: 最悪時間計算量は衝突が頻繁に発生する場合（例：全てのキーが同じハッシュ値になる）にO(n)になりますが、実用的にはO(1)として扱えます。

## いつ使うべきか

ハッシュテーブルは以下のような場面で威力を発揮します：

### 1. 高速な検索が必要な場合
- 「この要素は存在するか？」をO(1)で確認
- 「このキーに対応する値は何か？」をO(1)で取得

### 2. 要素の出現回数をカウントする場合
- 文字列内の文字の出現頻度
- 配列内の要素の出現回数

### 3. 要素をグループ化する場合
- 同じ特性を持つ要素をまとめる
- アナグラムのグループ化

### 4. 補助データ構造として使用
- 他のアルゴリズムの補助として、中間結果を保存
- 訪問済みノードの記録（グラフ探索など）

## 現実世界での応用例

### 1. データベースのインデックス
- **例**: ユーザーIDからユーザー情報を高速に取得
- **実装**: データベースエンジンが内部的にハッシュテーブルを使用
- **メリット**: 大量のデータからもO(1)でアクセス可能

### 2. ブラウザのキャッシュ
- **例**: 訪問済みのWebページのURLを記録
- **実装**: URLをキー、ページ内容を値として保存
- **メリット**: 同じページへの再訪問を高速化

### 3. プログラミング言語の辞書型
- **例**: Pythonの`dict`、JavaScriptの`Map`、Javaの`HashMap`
- **実装**: 言語の標準ライブラリとして提供
- **メリット**: キーと値のペアを効率的に管理

### 4. コンパイラのシンボルテーブル
- **例**: 変数名から変数の情報（型、スコープなど）を取得
- **実装**: コンパイラが変数名をキーとして使用
- **メリット**: コード解析中に変数情報を高速に参照

### 5. セッション管理（Webアプリケーション）
- **例**: セッションIDからユーザーセッション情報を取得
- **実装**: セッションIDをキー、セッション情報を値として保存
- **メリット**: ユーザーの状態を効率的に管理

## 実装時の注意点

### 1. キーの型
- **可変オブジェクトは避ける**: リストや辞書をキーにすると、変更時にハッシュ値が変わり予期しない動作を引き起こす
- **推奨**: イミュータブルな型（文字列、数値、タプル）をキーに使用

### 2. 衝突の処理
- **チェイニング**: 同じインデックスに複数の要素を連結リストで保存
- **オープンアドレッシング**: 別の空きスロットを探す
- **実装の選択**: 言語の標準ライブラリが適切に処理してくれるため、通常は意識する必要がない

### 3. 空間計算量
- **メモリ使用量**: 要素数に比例してメモリを消費
- **リサイズ**: 要素数が増えると内部配列をリサイズする必要がある（通常は自動）
- **トレードオフ**: 時間計算量の改善と引き換えに空間計算量が増える

### 4. 順序の保持
- **Python 3.7+**: `dict`は挿入順序を保持
- **それ以前**: 順序が保証されない
- **注意**: 順序が重要な場合は`collections.OrderedDict`を使用

## 関連するLeetCode/AtCoder問題

### Easy
- [Two Sum](../leetcode/easy/001_two_sum/) - ハッシュテーブルの基本
- [Valid Anagram](../leetcode/easy/007_valid_anagram/) - 文字の出現回数カウント
- [Contains Duplicate](../leetcode/easy/) - 要素の存在確認

### Medium
- [Group Anagrams](./group_anagrams_logic.md) - グループ化の典型例
- [Longest Substring Without Repeating Characters](../03_sliding_window/longest_substring_no_repeat_logic.md) - スライディングウィンドウと組み合わせ
- [Find All Anagrams in String](../leetcode/easy/033_find_all_anagrams_in_string/) - パターンマッチング

### Hard
- [Minimum Window Substring](../03_sliding_window/) - 高度なスライディングウィンドウ
- [Substring with Concatenation of All Words](../leetcode/hard/) - 複雑な文字列マッチング

## 学習の進め方

1. **Two Sum**から始める: ハッシュテーブルの最も基本的な使い方を理解
2. **Group Anagrams**でグループ化を学ぶ: キーを工夫して要素を分類
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Two Sum のロジック解説](./two_sum_logic.md)
- [Group Anagrams のロジック解説](./group_anagrams_logic.md)
- [二ポインタテクニック](../02_two_pointers/README.md) - ハッシュテーブルと組み合わせて使用

---

**重要**: ハッシュテーブルは多くのアルゴリズムの基礎となるデータ構造です。まずはこのテクニックをしっかり理解することで、他の高度なアルゴリズムの理解も深まります。

- [二ポインタ (Two Pointers)](#二ポインタ-two-pointers)


---

# 二ポインタ (Two Pointers)

## 概要

二ポインタテクニックは、配列や文字列を効率的に処理するための強力な手法です。2つのポインタ（インデックス）を同時に使用して、配列を1回の走査で処理することで、時間計算量を大幅に改善できます。

## 基本概念

### 二ポインタのパターン

1. **対向ポインタ（Opposite Ends）**: 配列の両端から中央に向かって移動
   - 左ポインタ: 先頭から開始
   - 右ポインタ: 末尾から開始
   - 用途: ソート済み配列での検索、回文判定など

2. **同方向ポインタ（Same Direction）**: 両方のポインタが同じ方向に移動
   - スローポインタ: ゆっくり移動
   - ファストポインタ: 速く移動
   - 用途: リンクリストのサイクル検出、配列の重複削除など

3. **スライディングウィンドウ**: 二ポインタの特殊なケース
   - 連続する部分配列を効率的に処理
   - 詳細は[スライディングウィンドウ](../03_sliding_window/README.md)を参照

#### 視覚的イメージ

**1. 対向ポインタ（Opposite Ends）**
```
例: ソート済み配列 [1, 2, 3, 4, 5, 6] で合計が7になるペアを探す

初期状態:
  left                    right
   ↓                      ↓
  [1,  2,  3,  4,  5,  6]
   0   1   2   3   4   5

ステップ1: 1 + 6 = 7 → 見つかった！
  left                    right
   ↓                      ↓
  [1,  2,  3,  4,  5,  6]
   0   1   2   3   4   5

移動パターン:
  left →                    ← right
   [1,  2,  3,  4,  5,  6]
```

**2. 同方向ポインタ（Same Direction）**
```
例: リンクリストのサイクル検出（ウサギとカメ）

slow (1歩ずつ)    fast (2歩ずつ)
     ↓                  ↓
  [A] → [B] → [C] → [D] → [E] → [C] (サイクル)
         ↑                        │
         └────────────────────────┘

slowとfastが同じノードに到達 → サイクル検出！
```

**3. スライディングウィンドウ**
```
例: 固定サイズk=3のウィンドウ

初期:  [1, 2, 3, 4, 5, 6, 7]
       └───┘
       window

スライド1: [1, 2, 3, 4, 5, 6, 7]
              └───┘
              window

スライド2: [1, 2, 3, 4, 5, 6, 7]
                 └───┘
                 window
```

### 主な操作と計算量

| パターン | 時間計算量 | 空間計算量 | 適用場面 |
|---------|-----------|-----------|---------|
| 対向ポインタ | O(n) | O(1) | ソート済み配列、回文判定 |
| 同方向ポインタ | O(n) | O(1) | 重複削除、サイクル検出 |
| スライディングウィンドウ | O(n) | O(k) | 連続する部分配列 |

**特徴**: 通常はO(1)の追加空間のみで、O(n)の時間計算量を達成できます。

## いつ使うべきか

二ポインタテクニックは以下のような場面で威力を発揮します：

### 1. ソート済み配列での検索
- 「2つの要素の合計が目標値になる組み合わせを探す」
- 「3つの要素の合計が目標値になる組み合わせを探す」
- **利点**: ソート済みという性質を活かして効率的に検索

### 2. 回文判定
- 「文字列が回文かどうか判定」
- 「配列が対称かどうか判定」
- **利点**: 両端から中央に向かって比較することで効率的に判定

### 3. 配列の重複削除
- 「ソート済み配列から重複を削除」
- 「特定の条件を満たす要素を削除」
- **利点**: 1回の走査で処理可能

### 4. 領域の最大化
- 「2つの線で囲まれる最大の面積を求める」
- 「2つの要素の間の最大の差を求める」
- **利点**: 貪欲的なアプローチで最適解を効率的に発見

### 5. マージ操作
- 「2つのソート済み配列をマージ」
- 「2つのソート済みリストをマージ」
- **利点**: 各配列を1回ずつ走査するだけでマージ可能

## 現実世界での応用例

### 1. 検索エンジンのインデックス
- **例**: ソート済みの文書IDリストから、2つのクエリの共通部分を高速に検索
- **実装**: 2つのソート済みリストを二ポインタで走査して共通要素を発見
- **メリット**: 大量のデータからもO(n + m)で処理可能

### 2. データベースのJOIN操作
- **例**: 2つのソート済みテーブルを結合
- **実装**: 二ポインタで両方のテーブルを同時に走査
- **メリット**: インデックスを活用して効率的に結合

### 3. ゲーム開発（衝突検出）
- **例**: ソート済みのオブジェクトリストから、距離が近いオブジェクトのペアを検出
- **実装**: 二ポインタで効率的にペアを探索
- **メリット**: 全ペアをチェックする必要がなく、O(n²)からO(n)に改善

### 4. 金融取引システム
- **例**: ソート済みの価格リストから、目標価格になる2つの商品の組み合わせを探す
- **実装**: 二ポインタで効率的に検索
- **メリット**: リアルタイム取引で高速な検索が必要な場合に有効

### 5. 画像処理（エッジ検出）
- **例**: 画像の端から中央に向かってエッジを検出
- **実装**: 二ポインタで両端から同時に処理
- **メリット**: 対称的な処理を効率的に実行

## 実装時の注意点

### 1. ポインタの移動条件
- **問題**: いつ、どちらのポインタを動かすべきか判断が難しい
- **解決策**: 問題の性質に応じて明確なルールを設定
  - 対向ポインタ: 条件に応じて左または右を動かす
  - 同方向ポインタ: スローポインタは条件を満たすまで動かさない

### 2. 境界条件
- **問題**: 配列の範囲外アクセス
- **解決策**: ループ条件を`left < right`や`left <= right`で適切に設定
- **注意**: インデックスの範囲を常に確認

### 3. 重複要素の扱い
- **問題**: 同じ値が複数回出現する場合の処理
- **解決策**: 重複をスキップするロジックを追加
- **例**: `while left < right and nums[left] == nums[left+1]: left += 1`

### 4. ソートの必要性
- **問題**: 多くの二ポインタ問題はソート済み配列を前提とする
- **解決策**: 必要に応じて事前にソート（O(n log n)のコスト）
- **トレードオフ**: ソートのコストと二ポインタの効率性を比較

### 5. 時間計算量の理解
- **平均**: O(n) - 各要素を1回ずつ処理
- **最悪**: O(n) - 常に線形時間
- **空間**: O(1) - 追加の空間は定数

## 関連するLeetCode/AtCoder問題

### Easy
- [Valid Palindrome](./valid_palindrome_logic.md) - 回文判定の基本
- [Remove Duplicates from Sorted Array](../leetcode/easy/015_remove_duplicates_from_sorted_array/) - 重複削除
- [Merge Sorted Array](../leetcode/easy/017_merge_sorted_array/) - マージ操作

### Medium
- [Container With Most Water](./container_with_most_water_logic.md) - 領域の最大化
- [3Sum](../leetcode/medium/041_3sum/) - 3つの要素の組み合わせ
- [Trapping Rain Water](../leetcode/medium/) - 高度な二ポインタ

### Hard
- [Trapping Rain Water II](../leetcode/hard/) - 3次元への拡張
- [Longest Valid Parentheses](../leetcode/hard/) - 複雑な境界条件

## 学習の進め方

1. **Valid Palindrome**から始める: 最もシンプルな二ポインタの例
2. **Container With Most Water**で最適化を学ぶ: 貪欲的なアプローチとの組み合わせ
3. **3Sum**で複雑な条件を学ぶ: 重複の扱いと複数のポインタ

## 次のステップ

- [Valid Palindrome のロジック解説](./valid_palindrome_logic.md)
- [Container With Most Water のロジック解説](./container_with_most_water_logic.md)
- [スライディングウィンドウテクニック](../03_sliding_window/README.md) - 二ポインタの特殊なケース

---

**重要**: 二ポインタテクニックは、配列や文字列の問題で頻繁に使用されます。ソート済み配列での検索や、回文判定など、多くの問題でO(n²)からO(n)に改善できます。

- [スライディングウィンドウ (Sliding Window)](#スライディングウィンドウ-sliding-window)


---

# スライディングウィンドウ (Sliding Window)

## 概要

スライディングウィンドウは、配列や文字列の**連続する部分列（サブアレイ/サブストリング）**を効率的に処理するためのテクニックです。二ポインタの特殊なケースとして、固定サイズまたは可変サイズの「ウィンドウ」を配列上で滑らせるように移動させながら処理を行います。

## 基本概念

### スライディングウィンドウのパターン

1. **固定サイズウィンドウ**: ウィンドウのサイズが一定
   - 例: 長さkの部分配列の最大和を求める
   - 用途: 固定サイズのサブアレイの問題

2. **可変サイズウィンドウ**: ウィンドウのサイズが条件に応じて変化
   - 例: 条件を満たす最長の部分文字列を求める
   - 用途: 条件を満たす最長/最短のサブアレイの問題

#### 視覚的イメージ

**1. 固定サイズウィンドウ（k=3）**
```
配列: [1, 2, 3, 4, 5, 6, 7]
      └─────┘
      window (sum=6)

      [1, 2, 3, 4, 5, 6, 7]
         └─────┘
         window (sum=9) ← 前の和から 1を引き、4を足す

      [1, 2, 3, 4, 5, 6, 7]
            └─────┘
            window (sum=12)

left →                    ← right
```

**2. 可変サイズウィンドウ（重複のない最長部分文字列）**
```
文字列: "abcabcbb"
        left
         right
        └─┘
        "a" (長さ1)

        left
          right
        └──┘
        "ab" (長さ2)

        left
           right
        └───┘
        "abc" (長さ3) ← 最長

        left
            right
        └────┘
        "abca" → 重複！左を縮小

         left
            right
         └───┘
         "bca" (長さ3)
```

**3. ウィンドウの拡張と縮小**
```
条件を満たすまで拡張:
left →                    ← right
[1, 2, 3, 4, 5, 6, 7]
└───────────────┘
   window拡張

条件を満たさなくなったら縮小:
left →                    ← right
[1, 2, 3, 4, 5, 6, 7]
    └────────────┘
     window縮小
```

### 主な操作と計算量

| パターン | 時間計算量 | 空間計算量 | 適用場面 |
|---------|-----------|-----------|---------|
| 固定サイズ | O(n) | O(1) | 固定サイズのサブアレイ |
| 可変サイズ | O(n) | O(k) | 条件を満たす最長/最短のサブアレイ |

**特徴**: 通常はO(n)の時間計算量で、全ての部分列を効率的に処理できます。

## いつ使うべきか

スライディングウィンドウテクニックは以下のような場面で威力を発揮します：

### 1. 連続する部分列の問題
- 「重複のない最長の部分文字列を求める」
- 「条件を満たす最長の部分配列を求める」
- **利点**: 全ての部分列を列挙する必要がなく、効率的に処理

### 2. 固定サイズのサブアレイ
- 「長さkの部分配列の最大和を求める」
- 「長さkの部分配列の平均値を求める」
- **利点**: ウィンドウを1つずつスライドさせることで、重複計算を避けられる

### 3. 文字列マッチング
- 「文字列s内で文字列tの全ての文字を含む最小の部分文字列を求める」
- 「文字列s内で文字列tのアナグラムを全て見つける」
- **利点**: 部分文字列を効率的に探索

### 4. カウント問題
- 「最大k個の異なる文字を含む最長の部分文字列を求める」
- 「条件を満たす部分配列の数を数える」
- **利点**: ウィンドウ内の要素を効率的にカウント

### 5. 最適化問題
- 「条件を満たす最小/最大の部分配列を求める」
- 「条件を満たす部分配列の和の最大/最小を求める」
- **利点**: 貪欲的なアプローチで最適解を効率的に発見

## 現実世界での応用例

### 1. ネットワークトラフィック分析
- **例**: 一定時間内のネットワークトラフィックの最大値を監視
- **実装**: 固定サイズのスライディングウィンドウで、時間窓内のトラフィックを集計
- **メリット**: リアルタイムでトラフィックのピークを検出

### 2. ストリーミングデータの処理
- **例**: 動画ストリーミングで、一定時間内の平均ビットレートを計算
- **実装**: スライディングウィンドウで、最新のNフレームの平均を計算
- **メリット**: リアルタイムで品質を監視

### 3. 金融取引システム
- **例**: 株価データで、過去N日間の移動平均を計算
- **実装**: 固定サイズのスライディングウィンドウで、移動平均を効率的に計算
- **メリット**: リアルタイムでトレンドを分析

### 4. ログ分析システム
- **例**: サーバーログで、一定時間内のエラー発生回数を監視
- **実装**: スライディングウィンドウで、時間窓内のエラーをカウント
- **メリット**: 異常検出をリアルタイムで実行

### 5. 自然言語処理
- **例**: テキスト内で、重複のない最長の単語列を検出
- **実装**: 可変サイズのスライディングウィンドウで、重複を避けながら最長の部分列を探索
- **メリット**: テキストの構造を効率的に解析

## 実装時の注意点

### 1. ウィンドウの拡張と縮小
- **問題**: いつウィンドウを拡張し、いつ縮小するべきか？
- **解決策**: 問題の条件に応じて明確なルールを設定
  - 条件を満たすまで拡張
  - 条件を満たさなくなったら縮小

### 2. ハッシュテーブルとの組み合わせ
- **問題**: ウィンドウ内の要素を効率的に管理する必要がある
- **解決策**: ハッシュテーブルやセットを使用して、要素の存在やカウントを管理
- **例**: 文字の出現回数を`dict`で管理

### 3. 境界条件
- **問題**: ウィンドウが配列の範囲外に出ないようにする
- **解決策**: ループ条件を適切に設定（`right < len(array)`など）
- **注意**: ウィンドウのサイズが0になる場合も考慮

### 4. 重複の処理
- **問題**: ウィンドウ内に重複要素がある場合の処理
- **解決策**: ハッシュセットやカウントマップを使用して重複を管理
- **例**: 文字の出現回数をカウントして、重複を検出

### 5. 時間計算量の理解
- **平均**: O(n) - 各要素を1回ずつ処理
- **最悪**: O(n) - 常に線形時間
- **空間**: O(k) - ウィンドウ内の要素を保存（kはウィンドウの最大サイズ）

### 6. 固定サイズウィンドウの最適化
- **問題**: 固定サイズの場合、毎回和を再計算するのは非効率
- **解決策**: 最初の和を計算し、ウィンドウをスライドさせる際に、出る要素を引き、入る要素を足す
- **例**: `current_sum = current_sum - array[left] + array[right]`

## 関連するLeetCode/AtCoder問題

### Easy
- [Maximum Average Subarray I](../leetcode/easy/) - 固定サイズウィンドウの基本
- [Contains Duplicate II](../leetcode/easy/) - ウィンドウ内の重複検出

### Medium
- [Longest Substring Without Repeating Characters](./longest_substring_no_repeat_logic.md) - 可変サイズウィンドウの典型例
- [Minimum Window Substring](../leetcode/hard/) - より複雑な可変サイズウィンドウ
- [Longest Substring with At Most K Distinct Characters](../leetcode/medium/) - 条件付きウィンドウ

### Hard
- [Minimum Window Substring](../leetcode/hard/) - 高度なスライディングウィンドウ
- [Sliding Window Maximum](../leetcode/hard/) - モノトニックキューとの組み合わせ

## 学習の進め方

1. **Longest Substring Without Repeating Characters**から始める: 可変サイズウィンドウの最も基本的な例
2. **固定サイズウィンドウ**の問題で、ウィンドウのスライド方法を学ぶ
3. **より複雑な条件**の問題で、ハッシュテーブルとの組み合わせを学ぶ

## 次のステップ

- [Longest Substring Without Repeating Characters のロジック解説](./longest_substring_no_repeat_logic.md)
- [二ポインタテクニック](../02_two_pointers/README.md) - スライディングウィンドウの基礎
- [ハッシュテーブルテクニック](../01_hash_table/README.md) - よく組み合わせて使用

---

**重要**: スライディングウィンドウは、連続する部分列の問題で非常に強力なテクニックです。二ポインタとハッシュテーブルを組み合わせることで、O(n²)やO(n³)の問題をO(n)に改善できます。

- [スタック・キュー (Stack & Queue)](#スタック・キュー-stack--queue)


---

# スタック・キュー (Stack & Queue)

## 概要

スタックとキューは、データの**挿入順序**と**削除順序**が異なる2つの基本的なデータ構造です。それぞれ異なる特性を持ち、特定の問題に最適化されています。

### スタック（Stack）
- **LIFO（Last In First Out）**: 最後に入れた要素が最初に出る
- **操作**: `push`（追加）、`pop`（削除）、`peek`（先頭参照）
- **例**: 本の積み重ね、関数呼び出しのコールスタック

### キュー（Queue）
- **FIFO（First In First Out）**: 最初に入れた要素が最初に出る
- **操作**: `enqueue`（追加）、`dequeue`（削除）、`peek`（先頭参照）
- **例**: レジの待ち行列、タスクスケジューリング

## 基本概念

### スタックの特性

1. **後入れ先出し**: 最後に追加した要素が最初に取り出される
2. **一方向アクセス**: 先頭（トップ）からのみアクセス可能
3. **再帰的な構造**: 再帰的な問題を反復的に解くのに適している

### キューの特性

1. **先入れ先出し**: 最初に追加した要素が最初に取り出される
2. **双方向アクセス**: 先頭（front）と末尾（rear）からアクセス可能
3. **順序保持**: 要素の順序を保持しながら処理するのに適している

#### 視覚的イメージ

**スタック（LIFO - Last In First Out）**
```
push(1) → push(2) → push(3) → pop() → pop() → pop()
   │        │        │        │      │      │
   ▼        ▼        ▼        ▼      ▼      ▼
  ┌──┐    ┌──┐    ┌──┐    ┌──┐   ┌──┐   (空)
  │ 1│    │ 2│    │ 3│    │ 2│   │ 1│
  └──┘    │ 1│    │ 2│    │ 1│   └──┘
          └──┘    │ 1│    └──┘
                  └──┘
                  TOP

本の積み重ねのように、最後に積んだ本が最初に取り出される
```

**キュー（FIFO - First In First Out）**
```
enqueue(1) → enqueue(2) → enqueue(3) → dequeue() → dequeue()
    │           │            │            │           │
    ▼           ▼            ▼            ▼           ▼
  ┌──┐       ┌──┐ ┌──┐   ┌──┐ ┌──┐ ┌──┐  ┌──┐ ┌──┐  ┌──┐
  │ 1│       │ 1│ │ 2│   │ 1│ │ 2│ │ 3│  │ 2│ │ 3│  │ 3│
  └──┘       └──┘ └──┘   └──┘ └──┘ └──┘  └──┘ └──┘  └──┘
  front      front rear   front      rear  front rear front rear
             rear

レジの待ち行列のように、最初に並んだ人が最初にサービスを受ける
```

**括弧マッチング（スタックの使用例）**
```
文字列: "([{}])"
         ↑
         push '('

         ([{}])
          ↑
          push '['

         ([{}])
           ↑
           push '{'

         ([{}])
            ↑
            pop '}' → '{'とマッチ ✓

         ([{}])
           ↑
           pop ']' → '['とマッチ ✓

         ([{}])
          ↑
          pop ')' → '('とマッチ ✓
```

### 主な操作と計算量

| データ構造 | 操作 | 時間計算量 | 空間計算量 |
|-----------|------|-----------|-----------|
| スタック | push/pop | O(1) | O(n) |
| スタック | peek | O(1) | O(1) |
| キュー | enqueue/dequeue | O(1) | O(n) |
| キュー | peek | O(1) | O(1) |

## いつ使うべきか

### スタックを使う場面

1. **括弧のマッチング**: 開き括弧と閉じ括弧の対応を確認
2. **式の評価**: 逆ポーランド記法、中置記法の変換
3. **履歴管理**: 元に戻す（Undo）機能、ブラウザの戻る機能
4. **再帰の代替**: 深さ優先探索（DFS）を反復的に実装
5. **モノトニックスタック**: 次に大きい/小さい要素を探す

### キューを使う場面

1. **幅優先探索（BFS）**: グラフや木のレベル順探索
2. **タスクスケジューリング**: プロセスキュー、ジョブキュー
3. **キャッシュ管理**: LRUキャッシュの実装
4. **ストリーミング処理**: データストリームの順次処理
5. **スライディングウィンドウ**: 固定サイズのウィンドウを管理

## 現実世界での応用例

### スタックの応用

1. **コンパイラの構文解析**
   - **例**: プログラミング言語の構文チェック
   - **実装**: 括弧の対応をスタックで確認
   - **メリット**: ネストされた構造を効率的に処理

2. **ブラウザの戻る/進む機能**
   - **例**: ウェブブラウザの履歴管理
   - **実装**: 訪問したURLをスタックに保存
   - **メリット**: ユーザーの操作履歴を効率的に管理

3. **テキストエディタのUndo/Redo**
   - **例**: 編集操作の履歴管理
   - **実装**: 操作をスタックに保存し、Undoで取り出す
   - **メリット**: 操作の順序を逆順に実行可能

4. **関数呼び出しの管理**
   - **例**: プログラムの実行時のコールスタック
   - **実装**: 関数呼び出しをスタックで管理
   - **メリット**: 再帰的な関数呼び出しを効率的に処理

5. **式の評価（電卓アプリ）**
   - **例**: 数式の計算
   - **実装**: 逆ポーランド記法でスタックを使用
   - **メリット**: 括弧のない数式を効率的に評価

### キューの応用

1. **オペレーティングシステムのプロセススケジューリング**
   - **例**: CPUのタスクキュー
   - **実装**: 実行待ちのプロセスをキューで管理
   - **メリット**: 公平な順序でプロセスを実行

2. **メッセージキューシステム**
   - **例**: メッセージブローカー（RabbitMQ、Kafka）
   - **実装**: メッセージをキューに保存し、順次処理
   - **メリット**: 非同期処理と負荷分散を実現

3. **プリンタの印刷キュー**
   - **例**: 複数の印刷ジョブの管理
   - **実装**: 印刷ジョブをキューに保存
   - **メリット**: 先着順で印刷を実行

4. **幅優先探索（BFS）**
   - **例**: グラフの最短経路探索
   - **実装**: 探索するノードをキューで管理
   - **メリット**: レベル順に探索することで最短経路を保証

5. **リアルタイムデータ処理**
   - **例**: ストリーミングデータの処理
   - **実装**: データをキューに保存し、順次処理
   - **メリット**: データの順序を保持しながら処理

## 実装時の注意点

### スタックの注意点

1. **オーバーフロー/アンダーフロー**
   - **問題**: スタックが満杯の場合の`push`、空の場合の`pop`
   - **解決策**: 事前にサイズをチェック
   - **注意**: 動的配列を使えば自動的に拡張される

2. **メモリ管理**
   - **問題**: 大量の要素をスタックに保存するとメモリを消費
   - **解決策**: 必要に応じて要素を削除
   - **注意**: 再帰の深さが大きい場合、スタックオーバーフローに注意

3. **順序の理解**
   - **問題**: LIFOの特性を理解していないと予期しない動作
   - **解決策**: スタックの動作を視覚的に理解する
   - **例**: 本の積み重ねをイメージする

### キューの注意点

1. **循環キュー**
   - **問題**: 固定サイズのキューで、末尾に達した場合の処理
   - **解決策**: 循環キューを実装してメモリを効率的に使用
   - **メリット**: 先頭の要素が削除された後、そのスペースを再利用

2. **優先度付きキュー**
   - **問題**: 単純なFIFOではなく、優先度に基づいて処理したい場合
   - **解決策**: ヒープを使った優先度付きキューを使用
   - **例**: タスクスケジューリングで優先度の高いタスクを先に処理

3. **デキュー（両端キュー）**
   - **問題**: 先頭と末尾の両方から要素を追加・削除したい場合
   - **解決策**: `collections.deque`を使用
   - **メリット**: スタックとキューの両方の機能を提供

## 関連するLeetCode/AtCoder問題

### Easy
- [Valid Parentheses](./valid_parentheses_logic.md) - スタックの基本
- [Implement Queue using Stacks](../leetcode/easy/) - データ構造の変換
- [Implement Stack using Queues](../leetcode/easy/) - データ構造の変換

### Medium
- [Daily Temperatures](./daily_temperatures_logic.md) - モノトニックスタック
- [Next Greater Element](../leetcode/medium/) - モノトニックスタック
- [Decode String](../leetcode/medium/) - ネストされた構造の処理

### Hard
- [Trapping Rain Water](../leetcode/hard/) - スタックを使った高度な問題
- [Largest Rectangle in Histogram](../leetcode/hard/) - モノトニックスタック
- [Sliding Window Maximum](../leetcode/hard/) - デキューを使った問題

## 学習の進め方

1. **Valid Parentheses**から始める: スタックの最も基本的な使い方
2. **Daily Temperatures**でモノトニックスタックを学ぶ: より高度なスタックの応用
3. **BFS問題**でキューを学ぶ: グラフ探索でのキューの使用

## 次のステップ

- [Valid Parentheses のロジック解説](./valid_parentheses_logic.md)
- [Daily Temperatures のロジック解説](./daily_temperatures_logic.md)
- [二分探索テクニック](../05_binary_search/README.md) - 次のPhase 2のテクニック

---

**重要**: スタックとキューは、多くのアルゴリズムの基礎となるデータ構造です。特に、再帰的な問題を反復的に解く際や、順序を保持しながら処理する際に強力です。


- [二分探索 (Binary Search)](#二分探索-binary-search)


---

# 二分探索 (Binary Search)

## 概要

二分探索は、**ソート済み配列**から特定の要素を効率的に検索するアルゴリズムです。線形探索のO(n)に対して、O(log n)の時間計算量を達成できる強力な手法です。

## 基本概念

### 二分探索の原理

1. **分割統治**: 配列を半分に分割し、どちらの半分に目的の要素があるかを判断
2. **ソート済みの活用**: ソート済みという性質を利用して、不要な半分を排除
3. **対数的な時間**: 各ステップで探索範囲が半分になるため、O(log n)の時間計算量

#### 視覚的イメージ

**二分探索のプロセス（target=7を探す）**
```
ソート済み配列: [1, 3, 5, 7, 9, 11, 13, 15]
                0  1  2  3  4   5   6   7

ステップ1: left=0, right=7, mid=3
           [1, 3, 5, 7, 9, 11, 13, 15]
            ↑        ↑              ↑
          left      mid           right
            arr[mid]=7 == target → 見つかった！

もしtarget=9の場合:
ステップ1: left=0, right=7, mid=3
           [1, 3, 5, 7, 9, 11, 13, 15]
            ↑        ↑              ↑
          left      mid           right
            arr[mid]=7 < 9 → 右半分を探索

ステップ2: left=4, right=7, mid=5
           [1, 3, 5, 7, 9, 11, 13, 15]
                       ↑    ↑       ↑
                     left  mid    right
            arr[mid]=11 > 9 → 左半分を探索

ステップ3: left=4, right=4, mid=4
           [1, 3, 5, 7, 9, 11, 13, 15]
                       ↑
                    left=right=mid
            arr[mid]=9 == target → 見つかった！

探索範囲の縮小:
[1, 3, 5, 7, 9, 11, 13, 15]  ← 8要素
└───────────┘
[9, 11, 13, 15]              ← 4要素
└─────┘
[9]                          ← 1要素
```

**探索範囲の変化**
```
n要素 → n/2要素 → n/4要素 → ... → 1要素
O(log n)ステップで1要素に収束
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 前提条件 |
|------|-----------|-----------|---------|
| 要素の検索 | O(log n) | O(1) | ソート済み配列 |
| 挿入位置の検索 | O(log n) | O(1) | ソート済み配列 |
| 範囲の検索 | O(log n) | O(1) | ソート済み配列 |

**特徴**: ソート済み配列に対して、非常に効率的な検索が可能。

## いつ使うべきか

二分探索は以下のような場面で威力を発揮します：

### 1. ソート済み配列での検索
- 「配列内に特定の値が存在するか？」
- 「配列内で特定の値の位置は？」
- **利点**: O(log n)で高速に検索可能

### 2. 境界の探索
- 「条件を満たす最小/最大の値は？」
- 「条件を満たす要素の範囲は？」
- **利点**: 境界を効率的に特定

### 3. 最適化問題
- 「条件を満たす最大/最小の値は？」
- 「条件を満たす解の存在確認」
- **利点**: 解の空間を効率的に探索

### 4. 回転済み配列
- 「回転されたソート済み配列で要素を検索」
- 「回転点を見つける」
- **利点**: 回転を考慮しながら効率的に検索

## 現実世界での応用例

### 1. データベースのインデックス検索
- **例**: B-treeインデックスでの検索
- **実装**: データベースエンジンが内部的に二分探索を使用
- **メリット**: 大量のデータからもO(log n)でアクセス可能

### 2. 辞書アプリケーション
- **例**: 単語の検索機能
- **実装**: ソート済みの単語リストから二分探索で検索
- **メリット**: 大量の単語からも高速に検索

### 3. ゲーム開発（当たり判定）
- **例**: ソート済みのオブジェクトリストから、特定範囲内のオブジェクトを検索
- **実装**: 二分探索で範囲の境界を特定
- **メリット**: 空間分割の効率化

### 4. 金融取引システム
- **例**: ソート済みの価格リストから、特定の価格帯の取引を検索
- **実装**: 二分探索で価格範囲を効率的に特定
- **メリット**: リアルタイム取引で高速な検索が必要な場合に有効

### 5. コンパイラの最適化
- **例**: シンボルテーブルでの変数名の検索
- **実装**: ソート済みのシンボルテーブルから二分探索で検索
- **メリット**: コード解析中に変数情報を高速に参照

## 実装時の注意点

### 1. オーバーフローの回避
- **問題**: `mid = (left + right) // 2`で、`left + right`がオーバーフローする可能性
- **解決策**: `mid = left + (right - left) // 2`を使用
- **注意**: Pythonでは整数のオーバーフローはないが、他の言語では重要

### 2. ループの終了条件
- **問題**: `left < right`と`left <= right`のどちらを使うべきか？
- **解決策**: 問題に応じて選択
  - `left < right`: 要素が見つからない場合の処理が異なる
  - `left <= right`: 要素が見つかるまで続ける
- **注意**: 無限ループを避けるため、必ず`left`または`right`を更新

### 3. 境界の扱い
- **問題**: 要素が見つからない場合、どのインデックスを返すべきか？
- **解決策**: 問題の要件に応じて選択
  - 挿入位置: 要素が挿入されるべき位置を返す
  - 存在確認: `-1`や`None`を返す
- **注意**: 境界条件を明確に定義する

### 4. 重複要素の扱い
- **問題**: 同じ値が複数回出現する場合、どの要素を返すべきか？
- **解決策**: 問題の要件に応じて選択
  - 最初の出現: `left`を更新する条件を調整
  - 最後の出現: `right`を更新する条件を調整
- **注意**: 問題文をよく読んで要件を確認

### 5. 回転済み配列の処理
- **問題**: 配列が回転している場合、通常の二分探索が使えない
- **解決策**: 回転点を見つけて、適切な半分を選択
- **注意**: 回転点の検出も二分探索で可能

## 関連するLeetCode/AtCoder問題

### Easy
- [Binary Search](./binary_search_logic.md) - 二分探索の基本
- [Search Insert Position](../leetcode/easy/) - 挿入位置の検索
- [First Bad Version](../leetcode/easy/) - 境界の探索

### Medium
- [Search in Rotated Sorted Array](./search_rotated_array_logic.md) - 回転済み配列での検索
- [Find First and Last Position](../leetcode/medium/) - 範囲の検索
- [Search a 2D Matrix](../leetcode/medium/) - 2次元配列での検索

### Hard
- [Median of Two Sorted Arrays](../leetcode/hard/) - 2つのソート済み配列の中央値
- [Find Minimum in Rotated Sorted Array](../leetcode/hard/) - 回転済み配列の最小値
- [Split Array Largest Sum](../leetcode/hard/) - 最適化問題への応用

## 学習の進め方

1. **Binary Search**から始める: 二分探索の最も基本的な実装
2. **Search in Rotated Sorted Array**で回転を学ぶ: より複雑な条件での二分探索
3. **最適化問題**で応用を学ぶ: 二分探索を最適化問題に適用

## 次のステップ

- [Binary Search のロジック解説](./binary_search_logic.md)
- [Search in Rotated Sorted Array のロジック解説](./search_rotated_array_logic.md)
- [動的計画法テクニック](../07_dynamic_programming/README.md) - 次のPhase 3のテクニック

---

**重要**: 二分探索は、ソート済み配列での検索をO(log n)に改善する強力な手法です。条件を満たす解を探す最適化問題にも応用できます。


- [ソート (Sorting)](#ソート-sorting)


---

# ソート (Sorting)

## 概要

ソートは、データを特定の順序（昇順・降順）に並べ替える基本的な操作です。多くのアルゴリズムの前提条件として重要です。

## 基本概念

### 主要なソートアルゴリズム

1. **マージソート**: O(n log n)、安定、分割統治
2. **クイックソート**: O(n log n)平均、不安定、分割統治
3. **ヒープソート**: O(n log n)、不安定、ヒープ構造
4. **挿入ソート**: O(n²)、安定、小規模データに適す

## いつ使うべきか

- データを順序付ける必要がある場合
- 二分探索の前処理
- 重複の削除
- 範囲クエリの前処理

## 現実世界での応用例

### 1. データベース
- **例**: クエリ結果のソート
- **実装**: ORDER BY句でソート
- **メリット**: データを効率的に表示

### 2. 検索エンジン
- **例**: 検索結果のランキング
- **実装**: 関連度でソート
- **メリット**: ユーザーに最適な結果を表示

### 3. 金融取引
- **例**: 取引履歴の時系列ソート
- **実装**: タイムスタンプでソート
- **メリット**: 時系列データを効率的に処理

## 関連するLeetCode/AtCoder問題

### Easy
- [Merge Sorted Array](./merge_sorted_array_logic.md) - マージ操作
- [Sort Colors](../leetcode/easy/) - 特殊なソート

### Medium
- [Merge Intervals](../leetcode/medium/) - ソート後の処理

## 学習の進め方

1. **基本的なソートアルゴリズム**を理解
2. **マージ操作**でソート済み配列を結合
3. **特殊なソート**で応用を学ぶ

---

**次のステップ**: [Merge Sorted Array](./merge_sorted_array_logic.md)


- [動的計画法 (Dynamic Programming)](#動的計画法-dynamic-programming)


---

# 動的計画法 (Dynamic Programming)

## 概要

動的計画法（DP）は、**最適化問題**を効率的に解くための強力な手法です。大きな問題を小さな部分問題に分割し、部分問題の解を再利用することで、計算量を大幅に削減します。

## 基本概念

### 動的計画法の特徴

1. **部分問題の重複**: 同じ部分問題が複数回出現する
2. **最適部分構造**: 最適解が部分問題の最適解から構成される
3. **メモ化**: 計算済みの結果を保存して再利用

### アプローチの種類

1. **トップダウン（メモ化再帰）**: 再帰関数にメモ化を追加
2. **ボトムアップ（反復的DP）**: 小さな問題から順に解いていく

#### 視覚的イメージ

**1. フィボナッチ数列（DPの典型例）**
```
再帰（非効率）:          DPテーブル（効率的）:
fib(5)                   dp[0]=0
├─ fib(4)                dp[1]=1
│  ├─ fib(3)            dp[2]=1 (0+1)
│  │  ├─ fib(2)         dp[3]=2 (1+1)
│  │  │  ├─ fib(1)      dp[4]=3 (1+2)
│  │  │  └─ fib(0)      dp[5]=5 (2+3)
│  │  └─ fib(1)         ↑
│  └─ fib(2)            メモ化で重複計算を回避
└─ fib(3)  ← 重複計算！

ボトムアップアプローチ:
dp[0] → dp[1] → dp[2] → dp[3] → dp[4] → dp[5]
 0       1       1       2       3       5
```

**2. 2次元DP（グリッド上の経路）**
```
問題: (0,0)から(2,2)への経路数

グリッド:          DPテーブル:
┌───┬───┬───┐      ┌───┬───┬───┐
│ S │   │   │      │ 1 │ 1 │ 1 │
├───┼───┼───┤      ├───┼───┼───┤
│   │   │   │  →   │ 1 │ 2 │ 3 │
├───┼───┼───┤      ├───┼───┼───┤
│   │   │ G │      │ 1 │ 3 │ 6 │
└───┴───┴───┘      └───┴───┴───┘
S=Start, G=Goal    dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

**3. メモ化の効果**
```
再帰（メモ化なし）:      メモ化あり:
fib(5)                  fib(5)
├─ fib(4)              ├─ fib(4) [計算済み]
│  ├─ fib(3) [計算済み]│  └─ 3
│  └─ 2                └─ 5
└─ fib(3) [計算済み]
    └─ 2

計算回数: O(2^n)       計算回数: O(n)
```

### 主な操作と計算量

| アプローチ | 時間計算量 | 空間計算量 | 適用場面 |
|-----------|-----------|-----------|---------|
| メモ化再帰 | O(n) | O(n) | 直感的だが再帰のオーバーヘッド |
| 反復的DP | O(n) | O(n) | 効率的で推奨 |
| 空間最適化 | O(n) | O(1) | 一部の問題で可能 |

## いつ使うべきか

動的計画法は以下のような場面で威力を発揮します：

### 1. 最適化問題
- 「最大/最小の値を求める」
- 「最適な組み合わせを見つける」
- **利点**: 全探索を避けて効率的に最適解を見つける

### 2. カウント問題
- 「特定の条件を満たす組み合わせの数を数える」
- 「パターンの数を計算する」
- **利点**: 重複計算を避けて効率的にカウント

### 3. 判定問題
- 「特定の条件を満たす解が存在するか判定」
- 「目標を達成できるか判定」
- **利点**: 効率的に判定可能

### 4. 経路問題
- 「グリッド上の経路の数を数える」
- 「最短経路を見つける」
- **利点**: 重複する経路を効率的に処理

## 現実世界での応用例

### 1. 株式取引の最適化
- **例**: 複数の取引から最大利益を求める
- **実装**: DPで各時点での最適な戦略を計算
- **メリット**: 複雑な取引戦略を効率的に最適化

### 2. リソース配分の最適化
- **例**: 限られた予算で最大の価値を得る
- **実装**: ナップサック問題としてDPで解く
- **メリット**: 最適なリソース配分を効率的に計算

### 3. テキスト処理（編集距離）
- **例**: 2つの文字列の類似度を計算
- **実装**: DPで編集距離を計算
- **メリット**: スペルチェッカーや検索エンジンで使用

### 4. ゲーム開発（AI）
- **例**: ゲームAIの意思決定
- **実装**: DPで最適な手を計算
- **メリット**: 複雑なゲーム木を効率的に探索

### 5. ネットワーク最適化
- **例**: ネットワーク上の最短経路を計算
- **実装**: DPで経路を最適化
- **メリット**: ルーティングアルゴリズムで使用

## 実装時の注意点

### 1. 状態の定義
- **問題**: DPテーブルの次元と意味を正確に定義する必要がある
- **解決策**: 「dp[i]は何を表すか？」を明確にする
- **例**: `dp[i]` = i番目の要素までの最適解

### 2. 遷移式の導出
- **問題**: 状態間の遷移を正確に表現する必要がある
- **解決策**: 「現在の状態はどの状態から遷移できるか？」を考える
- **例**: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`

### 3. 初期値の設定
- **問題**: ベースケースを正確に設定する必要がある
- **解決策**: 最小の部分問題の解を設定
- **例**: `dp[0] = 0`, `dp[1] = 1`

### 4. 空間最適化
- **問題**: 全ての状態を保存するとメモリを消費
- **解決策**: 必要な状態のみを保存（例: 直前の2つの状態のみ）
- **メリット**: O(n)からO(1)に空間計算量を削減

## 関連するLeetCode/AtCoder問題

### Easy
- [Climbing Stairs](./climbing_stairs_logic.md) - DPの基本
- [House Robber](./house_robber_logic.md) - 1次元DP
- [Fibonacci Number](../leetcode/easy/) - DPの典型例

### Medium
- [Coin Change](../leetcode/medium/) - ナップサック型DP
- [Longest Increasing Subsequence](../leetcode/medium/) - LIS問題
- [Unique Paths](../leetcode/medium/) - 2次元DP

### Hard
- [Edit Distance](../leetcode/hard/) - 文字列DP
- [Regular Expression Matching](../leetcode/hard/) - 複雑なDP
- [Word Break II](../leetcode/hard/) - 高度なDP

## 学習の進め方

1. **Climbing Stairs**から始める: DPの最も基本的な例
2. **House Robber**で1次元DPを学ぶ: より複雑な状態遷移
3. **2次元DP**で応用を学ぶ: グリッド上の問題

## 次のステップ

- [Climbing Stairs のロジック解説](./climbing_stairs_logic.md)
- [House Robber のロジック解説](./house_robber_logic.md)
- [貪欲法テクニック](../08_greedy/README.md) - 次のPhase 3のテクニック

---

**重要**: 動的計画法は、最適化問題を効率的に解く強力な手法です。部分問題の重複を利用することで、指数時間から多項式時間に改善できます。


- [貪欲法 (Greedy Algorithm)](#貪欲法-greedy-algorithm)


---

# 貪欲法 (Greedy Algorithm)

## 概要

貪欲法は、**各ステップで局所最適解を選択**することで、全体の最適解を目指すアルゴリズムです。動的計画法と異なり、過去の選択を後から変更しません。

## 基本概念

### 貪欲法の特徴

1. **局所最適選択**: 各ステップで最適と思われる選択を行う
2. **不可逆性**: 一度選択したら後から変更しない
3. **効率性**: 通常はO(n log n)またはO(n)の時間計算量

### 貪欲法が有効な条件

1. **貪欲選択性質**: 局所最適解が全体最適解に含まれる
2. **最適部分構造**: 部分問題の最適解が全体最適解の一部になる

## いつ使うべきか

貪欲法は以下のような場面で威力を発揮します：

### 1. スケジューリング問題
- 「タスクを最適な順序で実行」
- 「リソースを効率的に配分」
- **利点**: シンプルで効率的

### 2. 最適化問題
- 「最大/最小の値を求める」
- 「条件を満たす最適な組み合わせを見つける」
- **利点**: DPよりシンプルで高速

### 3. 区間問題
- 「重複しない区間を最大数選択」
- 「区間を最小数でカバー」
- **利点**: ソート後に貪欲に選択

## 現実世界での応用例

### 1. 株式取引
- **例**: 最適な売買タイミングを決定
- **実装**: 各時点で最適な選択を貪欲に行う
- **メリット**: リアルタイムで意思決定可能

### 2. ネットワークルーティング
- **例**: 最短経路を選択
- **実装**: 各ノードで最適な次のホップを選択
- **メリット**: 効率的なパケット転送

### 3. データ圧縮（ハフマン符号）
- **例**: 最適な符号化を生成
- **実装**: 頻度の高い文字に短い符号を割り当て
- **メリット**: 効率的なデータ圧縮

## 関連するLeetCode/AtCoder問題

### Easy
- [Best Time to Buy and Sell Stock](./best_time_to_buy_sell_stock_logic.md) - 貪欲法の基本
- [Maximum Subarray](./maximum_subarray_logic.md) - Kadane's Algorithm

### Medium
- [Jump Game](../leetcode/medium/) - 貪欲的な選択
- [Non-overlapping Intervals](../leetcode/medium/) - 区間問題

## 学習の進め方

1. **Best Time to Buy and Sell Stock**から始める: 貪欲法の最も基本的な例
2. **Maximum Subarray**でKadane's Algorithmを学ぶ: より複雑な貪欲法
3. **区間問題**で応用を学ぶ: ソートと組み合わせた貪欲法

---

**次のステップ**: [Best Time to Buy and Sell Stock](./best_time_to_buy_sell_stock_logic.md)


- [木の探索 (Tree Traversal)](#木の探索-tree-traversal)


---

# 木の探索 (Tree Traversal)

## 概要

木構造のデータを効率的に探索するためのアルゴリズムです。**深さ優先探索（DFS）**と**幅優先探索（BFS）**が主要な手法です。

## 基本概念

### 深さ優先探索（DFS）

1. **Pre-order（前順）**: 根 → 左 → 右
2. **In-order（中順）**: 左 → 根 → 右
3. **Post-order（後順）**: 左 → 右 → 根

### 幅優先探索（BFS）

1. **Level-order（レベル順）**: レベルごとに左から右へ

#### 視覚的イメージ

**二分木の構造**
```
        1
       / \
      2   3
     / \ / \
    4  5 6  7
```

**DFS（深さ優先探索）の3つの順序**
```
Pre-order（前順）: 1 → 2 → 4 → 5 → 3 → 6 → 7
                 根 → 左 → 右

        1
       / \
      2   3
     / \ / \
    4  5 6  7
    ↑
    1を処理 → 左部分木 → 右部分木

In-order（中順）: 4 → 2 → 5 → 1 → 6 → 3 → 7
                左 → 根 → 右

        1
       / \
      2   3
     / \ / \
    4  5 6  7
        ↑
        左部分木 → 1を処理 → 右部分木

Post-order（後順）: 4 → 5 → 2 → 6 → 7 → 3 → 1
                   左 → 右 → 根

        1
       / \
      2   3
     / \ / \
    4  5 6  7
            ↑
            左部分木 → 右部分木 → 1を処理
```

**BFS（幅優先探索）**
```
Level-order（レベル順）: 1 → 2 → 3 → 4 → 5 → 6 → 7

レベル0:        1
               ↓
レベル1:      2   3
             ↓   ↓
レベル2:    4  5 6  7

キューを使用:
[1] → [2,3] → [3,4,5] → [4,5,6,7] → [5,6,7] → ...
```

**DFS vs BFS**
```
DFS（スタック使用）:        BFS（キュー使用）:
    1                          1
   / \                        / \
  2   3                      2   3
 / \ / \                    / \ / \
4  5 6  7                  4  5 6  7

探索順序:                  探索順序:
1 → 2 → 4 → 5 → 3 → 6 → 7  1 → 2 → 3 → 4 → 5 → 6 → 7
（深く探索）                （浅く探索）
```

### 主な操作と計算量

| 探索方法 | 時間計算量 | 空間計算量 | 適用場面 |
|---------|-----------|-----------|---------|
| DFS（再帰） | O(n) | O(h) | 深さが浅い場合 |
| DFS（反復） | O(n) | O(h) | スタック使用 |
| BFS | O(n) | O(w) | 幅が狭い場合 |

h: 木の高さ, w: 最大幅

## いつ使うべきか

### DFSを使う場面
- パスの探索
- 木の構造の確認
- 深い探索が必要な場合

### BFSを使う場面
- 最短経路の探索
- レベルごとの処理
- 浅い探索が必要な場合

## 関連するLeetCode/AtCoder問題

### Easy
- [Maximum Depth of Binary Tree](./maximum_depth_logic.md) - DFSの基本
- [Binary Tree Level Order Traversal](./level_order_traversal_logic.md) - BFSの基本

### Medium
- [Binary Tree Zigzag Level Order Traversal](../leetcode/easy/) - BFSの応用
- [Path Sum](../leetcode/easy/) - DFSの応用

## 学習の進め方

1. **Maximum Depth**から始める: DFSの最も基本的な例
2. **Level Order Traversal**でBFSを学ぶ: キューを使った探索
3. **より複雑な問題**で応用を学ぶ: 条件付き探索

---

**次のステップ**: [Maximum Depth](./maximum_depth_logic.md) | [Level Order Traversal](./level_order_traversal_logic.md)


- [グラフアルゴリズム (Graph Algorithms)](#グラフアルゴリズム-graph-algorithms)


---

# グラフアルゴリズム (Graph Algorithms)

## 概要

グラフは、ノード（頂点）とエッジ（辺）で構成されるデータ構造です。ネットワーク、ソーシャルネットワーク、地図など、多くの現実世界の問題をモデル化できます。

## 基本概念

### グラフの種類

1. **有向グラフ**: エッジに方向がある
2. **無向グラフ**: エッジに方向がない
3. **重み付きグラフ**: エッジに重みがある

### 主要なアルゴリズム

1. **BFS（幅優先探索）**: 最短経路を求める
2. **DFS（深さ優先探索）**: パスの探索、サイクルの検出
3. **トポロジカルソート**: 依存関係の解決
4. **最短経路**: Dijkstra、Bellman-Ford

#### 視覚的イメージ

**グラフの種類**
```
無向グラフ:         有向グラフ:         重み付きグラフ:
   A ─── B            A ──→ B            A ──3──→ B
   │     │            │     │            │        │
   │     │            │     ↓            │        │
   C ─── D            C ←── D            C ──5──→ D
```

**BFS（幅優先探索）**
```
グラフ:              探索順序:
   1                 レベル0: 1
  / \                レベル1: 2, 3
 2   3               レベル2: 4, 5, 6
/ \ / \              レベル3: 7
4 5 6  7

キュー: [1] → [2,3] → [3,4,5] → [4,5,6] → [5,6,7] → ...
```

**DFS（深さ優先探索）**
```
グラフ:              探索順序:
   1                 1 → 2 → 4 → 5 → 3 → 6 → 7
  / \               
 2   3              スタック: [1] → [1,2] → [1,2,4] → ...
/ \ / \              → [1,2] → [1] → [1,3] → [1,3,6] → ...
4 5 6  7
```

**トポロジカルソート（依存関係）**
```
依存関係グラフ:      トポロジカル順序:
  A ──→ B            A → C → B → D
  │     │            
  ↓     ↓            または
  C ──→ D            A → B → C → D

例: タスクAとCが完了してからBとDを実行
```

**最短経路（Dijkstra）**
```
グラフ（重み付き）:  最短経路: A → C → D (合計: 1+2=3)
    A ──1──→ B      
    │        │      Aから各ノードへの最短距離:
    │        │      A: 0
    2        │      B: 1
    │        │      C: 2
    ↓        │      D: 3
    C ──2──→ D
```

## いつ使うべきか

- ネットワーク構造の処理
- 依存関係の解決
- 最短経路の探索
- サイクルの検出

## 関連するLeetCode/AtCoder問題

### Medium
- [Number of Islands](../leetcode/medium/) - BFS/DFSの基本
- [Course Schedule](../leetcode/medium/) - トポロジカルソート

### Hard
- [Word Ladder](../leetcode/hard/) - BFSの応用
- [Critical Connections](../leetcode/hard/) - DFSの応用

## 学習の進め方

1. **BFS/DFSの基本**から始める
2. **トポロジカルソート**で依存関係を学ぶ
3. **最短経路アルゴリズム**で応用を学ぶ

---

**次のステップ**: [文字列処理テクニック](../11_string_manipulation/README.md)


- [文字列処理 (String Manipulation)](#文字列処理-string-manipulation)


---

# 文字列処理 (String Manipulation)

## 概要

文字列処理は、テキストデータを効率的に操作・検索するためのアルゴリズムです。パターンマッチング、文字列検索、圧縮などに応用されます。

## 基本概念

### 主要なアルゴリズム

1. **KMP（Knuth-Morris-Pratt）**: 効率的な文字列マッチング
2. **Trie（トライ木）**: 文字列の集合を効率的に管理
3. **Rabin-Karp**: ハッシュを使った文字列マッチング

## いつ使うべきか

- パターンマッチング
- 文字列検索
- プレフィックス/サフィックスの処理
- 文字列の圧縮

## 関連するLeetCode/AtCoder問題

### Medium
- [Implement Trie](../leetcode/medium/) - Trieの実装
- [Longest Palindromic Substring](../leetcode/medium/) - 文字列処理の応用

### Hard
- [Edit Distance](../leetcode/hard/) - 文字列の編集距離

## 学習の進め方

1. **基本的な文字列操作**から始める
2. **Trie**で文字列集合を学ぶ
3. **高度なマッチングアルゴリズム**で応用を学ぶ

---

**次のステップ**: [ビット操作テクニック](../12_bit_manipulation/README.md)


- [ビット操作 (Bit Manipulation)](#ビット操作-bit-manipulation)


---

# ビット操作 (Bit Manipulation)

## 概要

ビット操作は、整数をビットレベルで操作する技術です。メモリ効率的で高速な処理が可能です。

## 基本概念

### 主要な操作

1. **AND (&)**: 両方のビットが1の場合に1
2. **OR (|)**: どちらかのビットが1の場合に1
3. **XOR (^)**: ビットが異なる場合に1
4. **NOT (~)**: ビットを反転
5. **シフト (<<, >>)**: ビットを左/右にシフト

## いつ使うべきか

- フラグの管理
- 集合の表現
- メモリ効率が重要な場合
- 高速な計算が必要な場合

## 関連するLeetCode/AtCoder問題

### Easy
- [Single Number](./single_number_logic.md) - XORの基本
- [Power of Two](../leetcode/easy/) - ビット操作の基本

### Medium
- [Single Number II](../leetcode/medium/) - より複雑なビット操作

## 学習の進め方

1. **基本的なビット操作**から始める
2. **XORの性質**を理解する
3. **集合の表現**で応用を学ぶ

---

**次のステップ**: [Single Number](./single_number_logic.md)


- [数学的アルゴリズム (Mathematical Algorithms)](#数学的アルゴリズム-mathematical-algorithms)


---

# 数学的アルゴリズム (Mathematical Algorithms)

## 概要

数学的アルゴリズムは、数論、組み合わせ論、幾何学などの数学的概念を計算機で効率的に処理するためのアルゴリズムです。

## 基本概念

### 主要なアルゴリズム

1. **GCD（最大公約数）**: ユークリッドの互除法
2. **素数判定**: エラトステネスの篩
3. **組み合わせ**: 二項係数、順列
4. **モジュロ演算**: 大きな数の計算

## いつ使うべきか

- 数論の問題
- 組み合わせの問題
- 幾何学の問題
- 確率・統計の問題

## 関連するLeetCode/AtCoder問題

### Easy
- [Power of Two](../leetcode/easy/) - 2の累乗判定
- [Count Primes](../leetcode/easy/) - 素数のカウント

### Medium
- [Pow(x, n)](../leetcode/medium/) - 累乗の計算
- [Permutations](../leetcode/medium/) - 順列の生成

## 学習の進め方

1. **基本的な数学的操作**から始める
2. **GCD/LCM**で数論を学ぶ
3. **組み合わせ論**で応用を学ぶ

---

**まとめ**: アルゴリズム・データ構造ロジック解説シリーズの全てのPhaseが完成しました！


- [バックトラッキング (Backtracking)](#バックトラッキング-backtracking)


---

# バックトラッキング (Backtracking)

## 概要

バックトラッキングは、全ての可能な解を体系的に探索するアルゴリズム手法です。解が見つからない場合や、現在の選択が解に繋がらない場合に、**一つ前の状態に戻って別の選択を試す**という特徴があります。組み合わせ問題、順列問題、制約充足問題などで威力を発揮します。

## 基本概念

### バックトラッキングの仕組み

1. **選択**: 現在の状態から可能な選択肢を選ぶ
2. **再帰**: 選択した状態で次のステップに進む
3. **制約チェック**: 現在の選択が有効か確認
4. **バックトラック**: 無効な場合、または解が見つからない場合に一つ前の状態に戻る
5. **解の記録**: 有効な解を見つけたら記録

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 組み合わせ生成 | O(2^n) | O(n) | 全ての部分集合を生成 |
| 順列生成 | O(n!) | O(n) | 全ての順列を生成 |
| N-Queens | O(n!) | O(n) | 制約充足問題 |

**注意**: バックトラッキングは指数時間または階乗時間になることが多いですが、早期終了（pruning）により実際の実行時間は大幅に短縮される場合があります。

## いつ使うべきか

バックトラッキングは以下のような場面で威力を発揮します：

### 1. 組み合わせ・順列問題
- 全ての可能な組み合わせを生成する必要がある
- 「n個からk個を選ぶ」全ての組み合わせ
- 全ての順列を生成

### 2. 制約充足問題
- 複数の制約を同時に満たす解を探す
- N-Queens問題（クイーンが互いに攻撃しない配置）
- 数独ソルバー（行・列・ブロックの制約を満たす）

### 3. パス探索問題
- 迷路やグラフで全ての可能なパスを探索
- 条件を満たす全てのパスを見つける

### 4. 分割問題
- 文字列や配列を条件を満たすように分割
- パーティション問題

## 現実世界での応用例

### 1. スケジューリングシステム
- **例**: 会議室の予約システムで、制約を満たす全てのスケジュールを探索
- **実装**: 時間スロットを選択し、制約（会議室の容量、時間の重複など）をチェック
- **メリット**: 最適なスケジュールを見つける

### 2. ゲームAI（パズルゲーム）
- **例**: 数独、クロスワードパズル、N-Queensなどの自動解法
- **実装**: 可能な選択肢を試し、制約に違反したら戻る
- **メリット**: 複雑なパズルを自動的に解く

### 3. コンパイラの最適化
- **例**: レジスタ割り当て、命令スケジューリング
- **実装**: 可能な割り当てを試し、最適なものを選択
- **メリット**: コードの実行効率を向上

### 4. ネットワークルーティング
- **例**: 複数の経路から最適な経路を探索
- **実装**: 可能な経路を試し、制約（帯域幅、遅延など）を満たすものを選択
- **メリット**: 効率的なネットワーク経路を見つける

### 5. DNA配列解析
- **例**: 遺伝子配列の組み合わせを探索
- **実装**: 可能な配列を生成し、生物学的制約をチェック
- **メリット**: 遺伝子の機能を理解

### 6. パスワードクラッキング（セキュリティテスト）
- **例**: セキュリティテストで、可能なパスワードの組み合わせを試す
- **実装**: 文字の組み合わせを生成し、ハッシュと照合
- **メリット**: システムの脆弱性を発見

## 実装時の注意点

### 1. 状態の管理
- **問題**: 再帰呼び出しで状態を正確に管理する必要がある
- **解決策**: 状態を引数として渡す、またはグローバル変数を使用
- **推奨**: 引数として渡す方が、バックトラック時に自動的に状態が戻る

### 2. メモ化の活用
- **問題**: 同じ状態が複数回計算される可能性がある
- **解決策**: 計算済みの状態をメモ化して再利用
- **注意**: メモ化により時間計算量を大幅に改善できる場合がある

### 3. 早期終了（Pruning）
- **問題**: 全ての可能性を探索すると時間がかかりすぎる
- **解決策**: 制約を満たさない選択肢を早期に排除
- **実装**: 制約チェックを各ステップで行い、無効な場合は即座に戻る

### 4. 空間計算量
- **問題**: 再帰の深さが深い場合、スタックオーバーフローのリスク
- **解決策**: 反復的実装を使用、または再帰の深さを制限
- **注意**: Pythonのデフォルト再帰制限は1000程度

### 5. 解の重複
- **問題**: 同じ解が複数回生成される可能性がある
- **解決策**: 解をセットに保存する、または生成時に重複チェック
- **実装**: ソートしてから生成することで、重複を避けられる場合がある

## 関連するLeetCode/AtCoder問題

### Medium
- [Generate Parentheses](./generate_parentheses_logic.md) - バックトラッキングの基本
- [Combination Sum](./combination_sum_logic.md) - 組み合わせ問題
- [Permutations](../leetcode/medium/) - 順列生成

### Hard
- [N-Queens](./n_queens_logic.md) - 制約充足問題の典型例
- [Sudoku Solver](./sudoku_solver_logic.md) - 複雑な制約充足問題
- [Word Search II](../15_trie/word_search_ii_logic.md) - バックトラッキング + Trie

## 学習の進め方

1. **Generate Parentheses**から始める: バックトラッキングの最も基本的な例
2. **Combination Sum**で組み合わせ問題を学ぶ: 選択肢の生成と制約チェック
3. **N-Queens**で制約充足問題を学ぶ: 複数の制約を同時に満たす解の探索
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Generate Parentheses のロジック解説](./generate_parentheses_logic.md)
- [N-Queens のロジック解説](./n_queens_logic.md)
- [動的計画法テクニック](../07_dynamic_programming/README.md) - バックトラッキングと比較

---

**重要**: バックトラッキングは、全ての可能な解を探索する強力な手法ですが、時間計算量が大きくなる可能性があります。早期終了（pruning）とメモ化を適切に使用することで、実用的な実行時間に抑えることができます。


- [トライ木 (Trie)](#トライ木-trie)


---

# トライ木 (Trie)

## 概要

トライ木（Trie、Prefix Tree）は、文字列の集合を効率的に保存・検索するための木構造のデータ構造です。文字列の**共通プレフィックスを共有**することで、メモリを効率的に使用し、高速な検索を実現します。文字列検索、自動補完、IPルーティングなどで広く使用されています。

## 基本概念

### トライ木の構造

1. **ルートノード**: 空文字列を表す
2. **エッジ**: 各エッジは1つの文字を表す
3. **ノード**: 各ノードは文字列のプレフィックスを表す
4. **終端マーカー**: 単語の終わりを示すフラグ

#### 視覚的イメージ

**トライ木の構造（単語: "cat", "car", "dog", "do"）**
```
         (root)
        /  |  \
       c   d   ...
      /    |
     a     o
    / \    |
   t   r   g
   *   *   *
   │   │   │
  cat car dog
       │
       *
      do

* = 終端マーカー（単語の終わり）

共通プレフィックス "ca" を共有:
- "cat" と "car" は "ca" を共有
- "dog" と "do" は "do" を共有
```

**検索のプロセス**
```
"cat"を検索:
root → 'c' → 'a' → 't' → * (見つかった！)

"cap"を検索:
root → 'c' → 'a' → 'p' → 存在しない

プレフィックス "ca" で検索:
root → 'c' → 'a' → 子ノードを探索
→ "cat", "car" が見つかる
```

**メモリ効率**
```
通常の配列:         トライ木:
["cat", "car",      (root)
 "dog", "do"]       /  |  \
                    c  d  ...
各文字列を個別に   共通部分を共有
保存: 12文字        → メモリ節約
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 挿入 | O(m) | O(m) | mは文字列の長さ |
| 検索 | O(m) | O(1) | 文字列の存在確認 |
| プレフィックス検索 | O(m) | O(1) | 共通プレフィックスを持つ文字列を検索 |
| 削除 | O(m) | O(1) | 文字列の削除 |

**注意**: 時間計算量は文字列の長さに比例し、文字列の数には依存しません。これがトライ木の最大の利点です。

## いつ使うべきか

トライ木は以下のような場面で威力を発揮します：

### 1. 文字列の高速検索
- 大量の文字列から特定の文字列を高速に検索
- 文字列の存在確認をO(m)で実行

### 2. プレフィックス検索
- 共通プレフィックスを持つ文字列を全て検索
- 自動補完機能の実装

### 3. 文字列の集合管理
- 辞書や単語リストの管理
- スペルチェッカー

### 4. IPルーティング
- IPアドレスの最長プレフィックスマッチ
- ルーティングテーブルの管理

## 現実世界での応用例

### 1. 検索エンジンの自動補完
- **例**: Google検索で、入力中のクエリに対する候補を表示
- **実装**: トライ木に検索履歴を保存し、プレフィックス検索で候補を取得
- **メリット**: ユーザーの入力効率を向上

### 2. スペルチェッカー
- **例**: ワードプロセッサで、入力中の単語のスペルをチェック
- **実装**: 辞書をトライ木に保存し、単語の存在を確認
- **メリット**: リアルタイムでスペルエラーを検出

### 3. IPルーティング（最長プレフィックスマッチ）
- **例**: ルーターが、IPアドレスに基づいて最適な経路を選択
- **実装**: IPアドレスをトライ木に保存し、最長の一致するプレフィックスを検索
- **メリット**: 効率的なパケットルーティング

### 4. オートコンプリート機能
- **例**: IDEのコード補完機能
- **実装**: 関数名や変数名をトライ木に保存し、入力に基づいて候補を表示
- **メリット**: 開発効率を向上

### 5. 電話帳アプリケーション
- **例**: 電話番号や名前の検索
- **実装**: 連絡先をトライ木に保存し、名前のプレフィックスで検索
- **メリット**: 高速な連絡先検索

### 6. データベースのインデックス
- **例**: 全文検索エンジンで、キーワードの検索
- **実装**: 文書内の単語をトライ木に保存し、高速に検索
- **メリット**: 大量のデータから高速に検索

## 実装時の注意点

### 1. ノードの構造
- **問題**: 各ノードにどのような情報を保存するか
- **解決策**: 
  - 子ノードへのポインタ（配列または辞書）
  - 終端フラグ（単語の終わりを示す）
  - 必要に応じて、追加の情報（出現回数など）
- **実装**: `children = {}`（辞書）または`children = [None] * 26`（配列）

### 2. メモリ使用量
- **問題**: 文字セットが大きい場合、メモリを大量に消費する可能性
- **解決策**: 
  - 辞書を使う場合: 実際に使用される文字のみを保存
  - 配列を使う場合: 固定サイズだが、未使用の領域も確保
- **トレードオフ**: 時間効率 vs 空間効率

### 3. 削除操作の実装
- **問題**: ノードを削除する際、他の単語に影響を与えないようにする必要がある
- **解決策**: 
  - 終端フラグをfalseにする
  - 子ノードがなく、終端フラグもfalseの場合のみノードを削除
- **注意**: 再帰的に親ノードも削除する必要がある場合がある

### 4. プレフィックス検索の実装
- **問題**: 共通プレフィックスを持つ全ての文字列を効率的に取得
- **解決策**: DFS（深さ優先探索）で、プレフィックスノードから全ての子ノードを探索
- **実装**: 再帰的に全ての終端ノードを収集

### 5. 大文字小文字の扱い
- **問題**: 大文字小文字を区別するかどうか
- **解決策**: 問題の要件に応じて、小文字に統一するか、区別するか決定
- **実装**: 挿入・検索時に`.lower()`で統一

## 関連するLeetCode/AtCoder問題

### Medium
- [Implement Trie](./implement_trie_logic.md) - トライ木の基本実装
- [Word Search II](./word_search_ii_logic.md) - トライ木 + バックトラッキング
- [Longest Word in Dictionary](./longest_word_dictionary_logic.md) - トライ木の応用

### Hard
- [Concatenated Words](../leetcode/hard/) - トライ木を使った文字列連結
- [Maximum XOR of Two Numbers](../leetcode/hard/) - トライ木の応用（ビット操作）

## 学習の進め方

1. **Implement Trie**から始める: トライ木の最も基本的な実装
2. **Word Search II**でバックトラッキングと組み合わせ: 複雑な問題への応用
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Implement Trie のロジック解説](./implement_trie_logic.md)
- [Word Search II のロジック解説](./word_search_ii_logic.md)
- [バックトラッキングテクニック](../14_backtracking/README.md) - トライ木と組み合わせて使用

---

**重要**: トライ木は文字列検索に特化した強力なデータ構造です。特にプレフィックス検索が必要な場合、他のデータ構造よりも圧倒的に効率的です。


- [Union-Find (Disjoint Set)](#union-find-disjoint-set)


---

# Union-Find (Disjoint Set)

## 概要

Union-Find（Disjoint Set Union、DSU）は、要素の集合を効率的に管理するデータ構造です。**2つの要素が同じ集合に属するか**を高速に判定し、**2つの集合を統合**する操作をサポートします。グラフの連結成分の判定、最小全域木の構築、ネットワークの接続性チェックなどで広く使用されています。

## 基本概念

### Union-Findの操作

1. **Find**: 要素が属する集合の代表（ルート）を見つける
2. **Union**: 2つの集合を1つに統合する
3. **初期化**: 各要素を独立した集合として初期化

#### 視覚的イメージ

**初期状態（各要素が独立した集合）**
```
parent配列: [0, 1, 2, 3, 4]
            ↓  ↓  ↓  ↓  ↓
            0  1  2  3  4  (各要素が自分の親)

集合: {0} {1} {2} {3} {4}
```

**Union操作（0と1を統合）**
```
Union(0, 1):
  0 ← 1  (1の親を0に設定)

parent配列: [0, 0, 2, 3, 4]
            ↓  ↓  ↓  ↓  ↓
            0  0  2  3  4

集合: {0,1} {2} {3} {4}
```

**Union操作（0と2を統合）**
```
Union(0, 2):
  0 ← 2  (2の親を0に設定)

parent配列: [0, 0, 0, 3, 4]
            ↓  ↓  ↓  ↓  ↓
            0  0  0  3  4

集合: {0,1,2} {3} {4}
```

**経路圧縮（Path Compression）**
```
圧縮前:          圧縮後:
  0               0
 / \             /|\
1   2           1 2 3
 \
  3

Find(3)の際に、3を直接0に接続
```

**ランク統合（Union by Rank）**
```
小さい木を大きい木に統合:

rank[0]=2      rank[3]=1
  0               3
 / \             / \
1   2           4   5

Union(0,3): 小さい方(3)を大きい方(0)に統合
  0
 /|\
1 2 3
   / \
  4   5
```

### 主な操作と計算量

| 操作 | 時間計算量（経路圧縮 + ランク統合） | 空間計算量 | 適用場面 |
|------|--------------------------------|-----------|---------|
| Find | O(α(n)) | O(n) | 集合の代表を見つける |
| Union | O(α(n)) | O(n) | 2つの集合を統合 |
| 初期化 | O(n) | O(n) | n個の要素を初期化 |

**注意**: α(n)はアッカーマン関数の逆関数で、実用的には定数（5以下）として扱えます。

## いつ使うべきか

Union-Findは以下のような場面で威力を発揮します：

### 1. グラフの連結成分の判定
- 2つのノードが同じ連結成分に属するか判定
- 連結成分の数を数える

### 2. 最小全域木（MST）の構築
- Kruskalのアルゴリズムで、サイクルを検出

### 3. ネットワークの接続性チェック
- ネットワーク内のノードが接続されているか確認

### 4. 画像処理
- 画像内の連結領域を検出

### 5. ゲーム開発
- ゲーム内のオブジェクトのグループ化

## 現実世界での応用例

### 1. ソーシャルネットワーク分析
- **例**: Facebookで、2人のユーザーが同じコミュニティに属するか判定
- **実装**: ユーザーをノード、友達関係をエッジとして、Union-Findで管理
- **メリット**: 大規模なネットワークでも高速に処理

### 2. 画像処理（連結成分の検出）
- **例**: 画像内の物体を検出し、同じ物体に属するピクセルをグループ化
- **実装**: 隣接するピクセルをUnionして、連結領域を検出
- **メリット**: 物体の識別とカウント

### 3. ネットワークインフラの管理
- **例**: データセンターで、サーバー間の接続性をチェック
- **実装**: サーバーをノード、接続をエッジとして、Union-Findで管理
- **メリット**: ネットワークの障害検出

### 4. ゲーム開発（物理エンジン）
- **例**: 物理シミュレーションで、接触しているオブジェクトをグループ化
- **実装**: 接触しているオブジェクトをUnionして、衝突判定を効率化
- **メリット**: 物理計算の高速化

### 5. データベースのクエリ最適化
- **例**: データベースで、関連するレコードをグループ化
- **実装**: 関連するレコードをUnionして、クエリを効率化
- **メリット**: クエリの実行時間を短縮

### 6. 遺伝子解析
- **例**: DNA配列で、関連する遺伝子をグループ化
- **実装**: 関連する遺伝子をUnionして、遺伝子の機能を理解
- **メリット**: 遺伝子の分類と解析

## 実装時の注意点

### 1. 経路圧縮（Path Compression）
- **問題**: Find操作で、木の高さを削減して効率化
- **解決策**: 探索中に、全てのノードを直接ルートに接続
- **実装**: `parent[x] = find(parent[x])`で再帰的に圧縮
- **メリット**: 時間計算量をO(log n)からO(α(n))に改善

### 2. ランク統合（Union by Rank）
- **問題**: Union操作で、小さい木を大きい木に統合して効率化
- **解決策**: 各ノードのランク（高さ）を記録し、小さい方を大きい方に統合
- **実装**: `rank`配列を管理し、統合時に更新
- **メリット**: 木の高さを抑制し、時間計算量を改善

### 3. 初期化
- **問題**: 各要素を独立した集合として初期化する必要がある
- **解決策**: `parent[i] = i`と`rank[i] = 0`で初期化
- **実装**: コンストラクタで初期化
- **注意**: 初期化を忘れると、正しく動作しない

### 4. サイクルの検出
- **問題**: グラフにサイクルがあるか判定
- **解決策**: Union操作で、2つの要素が既に同じ集合に属する場合、サイクルが存在
- **実装**: `find(x) == find(y)`の場合、サイクルが存在
- **メリット**: 最小全域木の構築でサイクルを検出

### 5. 連結成分の数
- **問題**: グラフの連結成分の数を数える
- **解決策**: 各要素のルートを数え、ユニークなルートの数が連結成分の数
- **実装**: 全ての要素のルートをセットに保存し、サイズを返す
- **メリット**: グラフの構造を理解

## 関連するLeetCode/AtCoder問題

### Medium
- [Friend Circles](./friend_circles_logic.md) - Union-Findの基本
- [Redundant Connection](./redundant_connection_logic.md) - サイクルの検出
- [Number of Provinces](./number_of_provinces_logic.md) - 連結成分の数

### Hard
- [Accounts Merge](../leetcode/hard/) - Union-Findの応用
- [Remove Max Number of Edges](../leetcode/hard/) - 複雑なUnion-Find

## 学習の進め方

1. **Friend Circles**から始める: Union-Findの最も基本的な例
2. **Redundant Connection**でサイクル検出を学ぶ: 最小全域木への応用
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Friend Circles のロジック解説](./friend_circles_logic.md)
- [Redundant Connection のロジック解説](./redundant_connection_logic.md)
- [グラフアルゴリズムテクニック](../10_graph_algorithms/README.md) - Union-Findと組み合わせて使用

---

**重要**: Union-Findは、グラフの連結成分を効率的に管理する強力なデータ構造です。経路圧縮とランク統合を組み合わせることで、実用的には定数時間に近い性能を実現できます。


- [ヒープ (Heap / Priority Queue)](#ヒープ-heap---priority-queue)


---

# ヒープ (Heap / Priority Queue)

## 概要

ヒープ（優先度付きキュー）は、要素を優先度順に管理するデータ構造です。**最小値（または最大値）をO(1)で取得**し、**要素の挿入・削除をO(log n)で実行**できます。ダイクストラ法、トップK問題、マージソートなどで広く使用されています。

## 基本概念

### ヒープの種類

1. **最小ヒープ**: 親ノードが子ノードより小さい（または等しい）
2. **最大ヒープ**: 親ノードが子ノードより大きい（または等しい）

#### 視覚的イメージ

**最小ヒープの構造**
```
配列表現: [1, 3, 2, 5, 4]
インデックス: 0  1  2  3  4

木構造:
        1
       / \
      3   2
     / \
    5   4

親 < 子の関係:
- 1 < 3, 1 < 2
- 3 < 5, 3 < 4
```

**ヒープの挿入（push）**
```
挿入前:        挿入(0):        ヒープ化:
    1              1               0
   / \            / \             / \
  3   2    →     3   2     →    1   2
 / \            / \ /           / \
5   4          5  4 0          3   4
                              /
                             5

0を末尾に追加 → 親と比較して交換 → ヒープ条件を満たすまで上へ
```

**ヒープの削除（pop）**
```
削除前:        最小値(0)削除:   ヒープ化:
    0              5               1
   / \            / \             / \
  1   2    →     1   2     →    3   2
 / \            / \             / \
3   4          3   4           5   4

末尾(5)を根に移動 → 子と比較して交換 → ヒープ条件を満たすまで下へ
```

**配列での表現**
```
インデックス:  0  1  2  3  4  5
値:          [1, 3, 2, 5, 4]

親のインデックス = (i-1) // 2
左の子 = 2*i + 1
右の子 = 2*i + 2

例: インデックス1の親は0、子は3と4
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 挿入 | O(log n) | O(n) | 要素の追加 |
| 最小値取得 | O(1) | O(1) | 最小値の取得 |
| 最小値削除 | O(log n) | O(1) | 最小値の削除 |
| ヒープ構築 | O(n) | O(n) | 配列からヒープを構築 |

**注意**: Pythonの`heapq`モジュールは最小ヒープを実装しています。最大ヒープが必要な場合は、値を負にして使用します。

## いつ使うべきか

ヒープは以下のような場面で威力を発揮します：

### 1. トップK問題
- K個の最大（最小）要素を見つける
- 頻度の高い要素を取得

### 2. ダイクストラ法
- 最短経路問題で、未訪問ノードから最小コストのノードを選択

### 3. マージK個のソート済みリスト
- 複数のソート済みリストを1つにマージ

### 4. スケジューリング
- 優先度の高いタスクを優先的に処理

### 5. メディアン（中央値）の追跡
- ストリーミングデータから動的に中央値を計算

## 現実世界での応用例

### 1. タスクスケジューラー
- **例**: OSのプロセススケジューラーで、優先度の高いプロセスを優先的に実行
- **実装**: プロセスの優先度をヒープで管理
- **メリット**: 効率的なリソース管理

### 2. ネットワークルーティング
- **例**: ルーターが、パケットの優先度に基づいて転送順序を決定
- **実装**: パケットの優先度をヒープで管理
- **メリット**: 重要なパケットを優先的に処理

### 3. イベント駆動システム
- **例**: ゲームエンジンで、イベントを時間順に処理
- **実装**: イベントのタイムスタンプをヒープで管理
- **メリット**: 時系列順のイベント処理

### 4. データストリームの分析
- **例**: リアルタイムデータから、トップKの要素を追跡
- **実装**: データをヒープで管理し、K個の最大（最小）要素を保持
- **メリット**: メモリ効率的なデータ分析

### 5. 医療システム
- **例**: 病院の救急外来で、患者の緊急度に基づいて診察順序を決定
- **実装**: 患者の緊急度をヒープで管理
- **メリット**: 緊急患者を優先的に診察

### 6. 金融取引システム
- **例**: 株式取引で、注文の優先度に基づいて処理順序を決定
- **実装**: 注文の優先度をヒープで管理
- **メリット**: 重要な注文を優先的に処理

## 実装時の注意点

### 1. 最小ヒープと最大ヒープ
- **問題**: Pythonの`heapq`は最小ヒープのみをサポート
- **解決策**: 最大ヒープが必要な場合、値を負にして使用
- **実装**: `heapq.heappush(heap, -value)`で最大ヒープを実現
- **注意**: 値を取得する際に、再度負にする必要がある

### 2. カスタム比較関数
- **問題**: 複雑なオブジェクトをヒープで管理する場合、比較方法を定義する必要がある
- **解決策**: `__lt__`メソッドを実装、またはタプルを使用
- **実装**: `(priority, item)`のタプルを使用
- **注意**: タプルの最初の要素で比較される

### 3. ヒープのサイズ制限
- **問題**: トップK問題で、ヒープのサイズをKに制限する必要がある
- **解決策**: ヒープのサイズがKを超えた場合、最小値を削除
- **実装**: `if len(heap) > k: heapq.heappop(heap)`
- **メリット**: メモリ使用量を削減

### 4. ヒープの構築
- **問題**: 配列からヒープを構築する場合、効率的な方法がある
- **解決策**: `heapq.heapify()`を使用（O(n)時間）
- **実装**: `heapq.heapify(arr)`で配列をヒープに変換
- **注意**: 既存の配列を直接変更する

### 5. 空のヒープの処理
- **問題**: 空のヒープから要素を取得しようとするとエラーが発生
- **解決策**: ヒープが空かどうかをチェック
- **実装**: `if heap: value = heapq.heappop(heap)`
- **注意**: エラーハンドリングが重要

## 関連するLeetCode/AtCoder問題

### Medium
- [Kth Largest Element](./kth_largest_element_logic.md) - トップK問題の基本
- [Merge K Sorted Lists](./merge_k_sorted_lists_logic.md) - マージ問題
- [Top K Frequent Elements](./top_k_frequent_elements_logic.md) - 頻度問題

### Hard
- [Find Median from Data Stream](../leetcode/hard/) - メディアンの追跡
- [Sliding Window Maximum](../leetcode/hard/) - スライディングウィンドウ + ヒープ

## 学習の進め方

1. **Kth Largest Element**から始める: ヒープの最も基本的な使い方
2. **Merge K Sorted Lists**でマージ問題を学ぶ: 複数のリストの統合
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Kth Largest Element のロジック解説](./kth_largest_element_logic.md)
- [Merge K Sorted Lists のロジック解説](./merge_k_sorted_lists_logic.md)
- [動的計画法テクニック](../07_dynamic_programming/README.md) - ヒープと組み合わせて使用

---

**重要**: ヒープは、優先度に基づいた処理が必要な場合に強力なデータ構造です。特にトップK問題やダイクストラ法で頻繁に使用されます。


- [分割統治法 (Divide and Conquer)](#分割統治法-divide-and-conquer)


---

# 分割統治法 (Divide and Conquer)

## 概要

分割統治法は、問題を**より小さな部分問題に分割**し、それぞれを**再帰的に解決**して、結果を**統合**するアルゴリズム手法です。マージソート、クイックソート、バイナリサーチなど、多くの効率的なアルゴリズムの基礎となっています。

## 基本概念

### 分割統治法の3つのステップ

1. **分割（Divide）**: 問題をより小さな部分問題に分割
2. **統治（Conquer）**: 部分問題を再帰的に解決
3. **統合（Combine）**: 部分問題の解を統合して元の問題の解を構築

### 主な操作と計算量

| アルゴリズム | 時間計算量 | 空間計算量 | 適用場面 |
|------------|-----------|-----------|---------|
| マージソート | O(n log n) | O(n) | 安定ソートが必要な場合 |
| クイックソート | O(n log n)平均 | O(log n) | 一般的なソート |
| バイナリサーチ | O(log n) | O(1) | ソート済み配列の検索 |
| べき乗計算 | O(log n) | O(log n) | 大きな数のべき乗 |

**注意**: 分割統治法は再帰的な構造を持つため、再帰の深さに注意が必要です。

## いつ使うべきか

分割統治法は以下のような場面で威力を発揮します：

### 1. ソート問題
- マージソート、クイックソート
- 安定ソートが必要な場合

### 2. 検索問題
- ソート済み配列での検索
- バイナリサーチ

### 3. 数学的問題
- べき乗計算
- 最大部分配列問題

### 4. 幾何学的問題
- 最近点対問題
- 凸包問題

### 5. 文字列問題
- 最長共通部分列
- 文字列のマッチング

## 現実世界での応用例

### 1. マージソートの実装
- **例**: 大規模なデータセットのソート
- **実装**: 配列を2つに分割し、それぞれをソートしてマージ
- **メリット**: 安定ソートで、最悪時間計算量が保証される

### 2. クイックソートの実装
- **例**: 一般的なソート処理
- **実装**: ピボットを選択し、配列を分割して再帰的にソート
- **メリット**: 平均的に高速で、インプレースソート

### 3. バイナリサーチ
- **例**: ソート済みデータベースでの検索
- **実装**: 配列を2つに分割し、目的の値が含まれる方を選択
- **メリット**: 対数時間で検索可能

### 4. べき乗計算
- **例**: 暗号化アルゴリズムでの大きな数のべき乗
- **実装**: 指数を2つに分割し、再帰的に計算
- **メリット**: 線形時間から対数時間に改善

### 5. 画像処理
- **例**: 画像の圧縮や変換
- **実装**: 画像を領域に分割し、それぞれを処理
- **メリット**: 並列処理が可能

### 6. データベースのクエリ最適化
- **例**: 大規模なデータベースでのクエリ処理
- **実装**: データを分割し、それぞれを並列に処理
- **メリット**: クエリの実行時間を短縮

## 実装時の注意点

### 1. ベースケースの定義
- **問題**: 再帰が終了する条件を明確に定義する必要がある
- **解決策**: 問題が十分に小さい場合、直接解決
- **実装**: `if n <= 1: return`などのベースケース
- **注意**: ベースケースを忘れると、無限再帰が発生

### 2. 再帰の深さ
- **問題**: 深い再帰はスタックオーバーフローを引き起こす可能性がある
- **解決策**: 反復的実装を使用、または再帰の深さを制限
- **実装**: スタックを使った反復的実装
- **注意**: Pythonのデフォルト再帰制限は1000程度

### 3. 部分問題の独立性
- **問題**: 部分問題が独立している必要がある
- **解決策**: 部分問題間の依存関係を最小化
- **実装**: データを適切に分割
- **注意**: 依存関係がある場合、動的計画法を検討

### 4. 統合のコスト
- **問題**: 部分問題の解を統合するコストを考慮する必要がある
- **解決策**: 統合のコストが部分問題の解決コストより小さいことを確認
- **実装**: 統合のアルゴリズムを最適化
- **注意**: 統合のコストが大きい場合、分割統治法が非効率になる可能性がある

### 5. メモ化の活用
- **問題**: 同じ部分問題が複数回計算される可能性がある
- **解決策**: メモ化を使って、計算済みの結果を再利用
- **実装**: `@lru_cache`デコレータを使用
- **注意**: メモ化により時間計算量を改善できる場合がある

## 関連するLeetCode/AtCoder問題

### Medium
- [Merge Sort](./merge_sort_logic.md) - 分割統治法の基本
- [Quick Sort](./quick_sort_logic.md) - インプレースソート
- [Pow(x, n)](./pow_x_n_logic.md) - べき乗計算

### Hard
- [Maximum Subarray](../08_greedy/maximum_subarray_logic.md) - 分割統治法アプローチ
- [Count of Smaller Numbers After Self](../leetcode/hard/) - マージソートの応用

## 学習の進め方

1. **Merge Sort**から始める: 分割統治法の最も基本的な例
2. **Quick Sort**でインプレースソートを学ぶ: 実用的なソートアルゴリズム
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Merge Sort のロジック解説](./merge_sort_logic.md)
- [Quick Sort のロジック解説](./quick_sort_logic.md)
- [動的計画法テクニック](../07_dynamic_programming/README.md) - 分割統治法と比較

---

**重要**: 分割統治法は、多くの効率的なアルゴリズムの基礎です。問題を適切に分割し、部分問題を解決して統合する思考プロセスを理解することが重要です。


- [累積和 (Prefix Sum)](#累積和-prefix-sum)


---

# 累積和 (Prefix Sum)

## 概要

累積和（Prefix Sum）は、配列の各位置までの要素の合計を事前に計算しておくテクニックです。これにより、**任意の範囲の合計をO(1)で取得**できます。AtCoderで頻出のテクニックで、範囲クエリの問題で威力を発揮します。

## 基本概念

### 累積和の構築

1. **1次元累積和**: `prefix[i] = arr[0] + arr[1] + ... + arr[i-1]`
2. **2次元累積和**: 2次元配列の矩形領域の合計をO(1)で取得
3. **いもす法**: 範囲への加算を効率的に処理

#### 視覚的イメージ

**1次元累積和**
```
元の配列:    [2, 5, 3, 1, 4]
インデックス: 0  1  2  3  4

累積和配列:  [0, 2, 7, 10, 11, 15]
インデックス: 0  1  2   3   4   5
            ↑
            prefix[0] = 0（空の合計）

範囲[1,3]の合計:
prefix[4] - prefix[1] = 11 - 2 = 9
arr[1] + arr[2] + arr[3] = 5 + 3 + 1 = 9 ✓
```

**2次元累積和**
```
元の配列:        累積和配列:
[1, 2, 3]        [0,  0,  0,  0]
[4, 5, 6]   →    [0,  1,  3,  6]
[7, 8, 9]        [0,  5, 12, 21]
                 [0, 12, 27, 45]

矩形[1,1]から[2,2]の合計:
prefix[3][3] - prefix[1][3] - prefix[3][1] + prefix[1][1]
= 45 - 6 - 12 + 1 = 28
= 5 + 6 + 8 + 9 = 28 ✓
```

**いもす法（範囲加算）**
```
範囲[2,4]に+3を加算:

元の配列:    [0, 0, 0, 0, 0]
差分配列:    [0, 0, +3, 0, 0, -3]
            ↑        ↑        ↑
          開始位置  終了+1位置

累積和で復元: [0, 0, 3, 3, 3, 0]
            ↑        ↑
          範囲[2,4]に+3が適用
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 累積和の構築 | O(n) | O(n) | 1次元配列 |
| 範囲の合計取得 | O(1) | O(1) | 任意の範囲 |
| 2次元累積和の構築 | O(n×m) | O(n×m) | 2次元配列 |
| 矩形領域の合計取得 | O(1) | O(1) | 任意の矩形 |

**注意**: 累積和は範囲クエリが頻繁に行われる場合に特に有効です。

## いつ使うべきか

累積和は以下のような場面で威力を発揮します：

### 1. 範囲クエリ問題
- 配列の任意の範囲の合計を高速に取得
- 部分配列の合計を複数回計算する場合

### 2. AtCoderの問題
- 範囲の合計、平均、最大値などを求める問題
- いもす法を使った範囲への加算

### 3. データ分析
- 時系列データの累積和を計算
- 売上の累積、訪問者の累積など

### 4. 画像処理
- 画像の矩形領域の輝度の合計
- 2次元累積和を使用

### 5. ゲーム開発
- ゲーム内のスコアの累積
- 経験値の累積など

## 現実世界での応用例

### 1. データベースのクエリ最適化
- **例**: SQLのSUMクエリを高速化
- **実装**: 累積和を事前に計算して保存
- **メリット**: クエリの実行時間を短縮

### 2. 金融取引システム
- **例**: 株価の累積リターンを計算
- **実装**: 価格変動の累積和を計算
- **メリット**: リアルタイム計算が可能

### 3. ウェブアナリティクス
- **例**: ウェブサイトの訪問者の累積数を追跡
- **実装**: 日次の訪問者数の累積和を計算
- **メリット**: 効率的なデータ分析

### 4. 画像処理
- **例**: 画像の矩形領域の平均輝度を計算
- **実装**: 2次元累積和を使用
- **メリット**: 高速な画像処理

### 5. ゲーム開発
- **例**: ゲーム内のスコアの累積を表示
- **実装**: スコアの累積和を計算
- **メリット**: リアルタイム表示が可能

### 6. ログ分析
- **例**: サーバーログの特定期間のエラー数を集計
- **実装**: エラー数の累積和を計算
- **メリット**: 効率的なログ分析

## 実装時の注意点

### 1. インデックスの扱い
- **問題**: 累積和のインデックスが1-basedか0-basedかを明確にする
- **解決策**: `prefix[i]`が`arr[0..i-1]`の合計を表すように定義
- **実装**: `prefix[0] = 0`として開始
- **注意**: インデックスのずれに注意

### 2. 範囲の計算
- **問題**: 範囲[i, j]の合計を計算する際の式
- **解決策**: `prefix[j+1] - prefix[i]`で計算
- **実装**: 右端を含む場合は`j+1`を使用
- **注意**: 範囲の定義を明確にする

### 3. オーバーフローの注意
- **問題**: 大きな値の累積和でオーバーフローが発生する可能性
- **解決策**: 言語によっては大きな整数型を使用
- **実装**: Pythonでは自動的に大きな整数を扱える
- **注意**: 他の言語では注意が必要

### 4. 2次元累積和
- **問題**: 2次元配列の矩形領域の合計を計算
- **解決策**: 2次元累積和を構築
- **実装**: `prefix[i][j] = arr[i][j] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]`
- **注意**: 重複部分を引く必要がある

### 5. いもす法
- **問題**: 範囲への加算を効率的に処理
- **解決策**: 開始位置に+1、終了位置+1に-1を記録し、累積和を取る
- **実装**: `diff[start] += value; diff[end+1] -= value`
- **メリット**: 複数の範囲への加算をO(1)で処理

## 関連するLeetCode/AtCoder問題

### Medium
- [Range Sum Query](./range_sum_query_logic.md) - 累積和の基本
- [Subarray Sum Equals K](./subarray_sum_equals_k_logic.md) - ハッシュマップとの組み合わせ
- [Product of Array Except Self](./product_array_except_self_logic.md) - 累積積
- [2D Prefix Sum](./2d_prefix_sum_logic.md) - 2次元累積和

### Hard
- [Maximum Sum of 3 Non-Overlapping Subarrays](../leetcode/hard/) - 累積和の応用

## 学習の進め方

1. **Range Sum Query**から始める: 累積和の最も基本的な例
2. **Subarray Sum Equals K**でハッシュマップと組み合わせ: より複雑な問題
3. **2D Prefix Sum**で2次元累積和を学ぶ: 矩形領域のクエリ
4. **より複雑な問題**に挑戦: いもす法などの応用を学ぶ

## 次のステップ

- [Range Sum Query のロジック解説](./range_sum_query_logic.md)
- [Subarray Sum Equals K のロジック解説](./subarray_sum_equals_k_logic.md)
- [二分探索テクニック](../05_binary_search/README.md) - 累積和と組み合わせて使用

---

**重要**: 累積和は、範囲クエリが頻繁に行われる場合に強力なテクニックです。特にAtCoderでは頻出なので、しっかりと理解することが重要です。


- [リンクリスト (Linked List)](#リンクリスト-linked-list)


---

# リンクリスト (Linked List)

## 概要

リンクリストは、要素をノードとして連結したデータ構造です。各ノードは**データと次のノードへのポインタ**を持ちます。配列と異なり、**動的なサイズ変更**が可能で、**挿入・削除がO(1)で実行**できます。メモリ効率が良く、多くのアルゴリズムで使用されます。

## 基本概念

### リンクリストの種類

1. **単方向リンクリスト**: 各ノードが次のノードへのポインタのみを持つ
2. **双方向リンクリスト**: 各ノードが前後のノードへのポインタを持つ
3. **循環リンクリスト**: 最後のノードが最初のノードを指す

#### 視覚的イメージ

**単方向リンクリスト**
```
head → [1|→] → [2|→] → [3|→] → [4|→] → null
        ↑                ↑
      データ           ポインタ

各ノード: {data, next}
```

**双方向リンクリスト**
```
head → [←|1|→] ↔ [←|2|→] ↔ [←|3|→] ↔ [←|4|→] → null
        ↑         ↑         ↑
       prev     data      next

各ノード: {prev, data, next}
```

**循環リンクリスト**
```
head → [1|→] → [2|→] → [3|→] → [4|→]
        ↑                          │
        └──────────────────────────┘

最後のノードが最初のノードを指す
```

**挿入操作（先頭）**
```
挿入前:       挿入(0):        結果:
head → 1      head → 0        head → 0 → 1 → 2 → 3
        ↓            ↓                ↓
        2            1                2
        ↓            ↓                ↓
        3            2                3
                     ↓
                     3

O(1)で実行可能
```

**削除操作**
```
削除前:       削除(2):        結果:
head → 1      head → 1        head → 1 → 3
        ↓            ↓                ↓
        2            3                4
        ↓            ↓
        3            4
        ↓
        4

前のノードを探す必要があるためO(n)
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 挿入（先頭） | O(1) | O(1) | 先頭への挿入 |
| 挿入（末尾） | O(n) | O(1) | 末尾への挿入（末尾ポインタがあればO(1)） |
| 削除 | O(n) | O(1) | 要素の削除（前のノードを探す必要がある） |
| 検索 | O(n) | O(1) | 要素の検索 |
| 反転 | O(n) | O(1) | リンクリストの反転 |

**注意**: リンクリストはランダムアクセスができないため、特定の位置へのアクセスにはO(n)時間がかかります。

## いつ使うべきか

リンクリストは以下のような場面で威力を発揮します：

### 1. 動的なサイズ変更が必要な場合
- サイズが事前に分からないデータ構造
- 頻繁に挿入・削除が行われる場合

### 2. メモリ効率が重要な場合
- メモリが断片化している環境
- 大きなデータを扱う場合

### 3. スタック・キューの実装
- スタックやキューの内部実装
- LIFO/FIFOの操作

### 4. グラフの表現
- 隣接リストとしてグラフを表現
- スパースグラフに適している

### 5. 多項式の表現
- 多項式の項をノードとして表現
- 多項式の演算

## 現実世界での応用例

### 1. メモリ管理
- **例**: OSのメモリアロケーターで、空きメモリブロックを管理
- **実装**: 空きメモリブロックをリンクリストで管理
- **メリット**: 動的なメモリ割り当てが可能

### 2. ファイルシステム
- **例**: ファイルシステムで、ファイルのブロックを管理
- **実装**: ファイルのブロックをリンクリストで管理
- **メリット**: 断片化したファイルを効率的に管理

### 3. ブラウザの履歴
- **例**: ブラウザの戻る/進む機能
- **実装**: 訪問履歴を双方向リンクリストで管理
- **メリット**: 効率的な履歴管理

### 4. 音楽プレイヤー
- **例**: 音楽プレイヤーのプレイリスト
- **実装**: 曲をリンクリストで管理
- **メリット**: 効率的なプレイリスト管理

### 5. テキストエディタ
- **例**: テキストエディタの行の管理
- **実装**: 各行をリンクリストで管理
- **メリット**: 効率的なテキスト編集

### 6. キャッシュシステム
- **例**: LRUキャッシュの実装
- **実装**: アクセス順序を双方向リンクリストで管理
- **メリット**: 効率的なキャッシュ管理

## 実装時の注意点

### 1. ポインタの管理
- **問題**: ポインタを適切に更新しないと、リンクが切れる
- **解決策**: 操作の順序を慎重に設計
- **実装**: 一時変数を使用してポインタを保存
- **注意**: ポインタを失うと、メモリリークが発生

### 2. エッジケースの処理
- **問題**: 空のリスト、1つの要素のみ、先頭・末尾の処理
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if head is None:`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

### 3. ダミーノードの使用
- **問題**: 先頭・末尾の処理が複雑になる場合がある
- **解決策**: ダミーノードを使用して、エッジケースを簡潔に処理
- **実装**: `dummy = ListNode(0)`で開始
- **メリット**: コードが簡潔になる

### 4. サイクルの検出
- **問題**: リンクリストにサイクルがあるか判定
- **解決策**: フロイドの循環検出アルゴリズム（ウサギとカメ）
- **実装**: 2つのポインタを異なる速度で移動
- **メリット**: O(1)空間でサイクルを検出

### 5. 再帰の使用
- **問題**: リンクリストの問題で再帰が有効な場合がある
- **解決策**: 再帰を使って、コードを簡潔に
- **実装**: 再帰的にノードを処理
- **注意**: 深い再帰はスタックオーバーフローのリスク

### 6. 反復的実装
- **問題**: 再帰の代わりに反復的実装を使用
- **解決策**: ループを使ってノードを処理
- **実装**: `while current:`でループ
- **メリット**: スタックオーバーフローのリスクがない

## 関連するLeetCode/AtCoder問題

### Easy
- [Reverse Linked List](./reverse_linked_list_logic.md) - リンクリストの基本操作
- [Merge Two Sorted Lists](./merge_two_sorted_lists_logic.md) - マージ操作

### Medium
- [Detect Cycle](./detect_cycle_logic.md) - サイクルの検出
- [Remove Nth Node From End](./remove_nth_node_logic.md) - 2つのポインタ

### Hard
- [Merge K Sorted Lists](../17_heap/merge_k_sorted_lists_logic.md) - ヒープとの組み合わせ
- [Reverse Nodes in k-Group](../leetcode/hard/) - 複雑な反転操作

## 学習の進め方

1. **Reverse Linked List**から始める: リンクリストの最も基本的な操作
2. **Merge Two Sorted Lists**でマージ操作を学ぶ: 2つのリストの統合
3. **Detect Cycle**でサイクル検出を学ぶ: 2つのポインタテクニック
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Reverse Linked List のロジック解説](./reverse_linked_list_logic.md)
- [Merge Two Sorted Lists のロジック解説](./merge_two_sorted_lists_logic.md)
- [二ポインタテクニック](../02_two_pointers/README.md) - リンクリストと組み合わせて使用

---

**重要**: リンクリストは、動的なデータ構造として多くのアルゴリズムの基礎となります。ポインタの操作を正確に理解することが重要です。


- [インターバル問題 (Intervals)](#インターバル問題-intervals)


---

# インターバル問題 (Intervals)

## 概要

インターバル問題は、時間範囲、数値範囲、区間などの**インターバル（区間）を扱う問題**です。会議室の予約、イベントのスケジューリング、範囲のマージなど、多くの実用的な問題で使用されます。ソートと適切な処理順序が鍵となります。

## 基本概念

### インターバルの表現

1. **開始点と終了点**: `[start, end]`で表現
2. **包含関係**: インターバルAがインターバルBに含まれるか
3. **重複**: 2つのインターバルが重複しているか
4. **マージ**: 重複するインターバルを1つに統合

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| ソート | O(n log n) | O(1) | インターバルの整理 |
| マージ | O(n) | O(n) | 重複するインターバルの統合 |
| 挿入 | O(n) | O(n) | 新しいインターバルの挿入 |
| 重複チェック | O(n log n) | O(1) | 重複の検出 |

**注意**: インターバル問題では、通常最初にソートを行うことで、効率的に処理できます。

## いつ使うべきか

インターバル問題は以下のような場面で威力を発揮します：

### 1. スケジューリング問題
- 会議室の予約
- イベントのスケジューリング
- タスクの割り当て

### 2. 範囲のマージ
- 重複する範囲を統合
- 連続する範囲を結合

### 3. 範囲の挿入
- 新しい範囲を適切な位置に挿入
- 既存の範囲と統合

### 4. 範囲のクエリ
- 特定の範囲に含まれるインターバルを検索
- 範囲の重複をチェック

## 現実世界での応用例

### 1. 会議室予約システム
- **例**: 会議室の予約を管理し、重複を避ける
- **実装**: インターバルをソートし、重複をチェック
- **メリット**: 効率的な予約管理

### 2. カレンダーアプリケーション
- **例**: カレンダーで、イベントの重複をチェック
- **実装**: インターバルをソートし、重複を検出
- **メリット**: 効率的なイベント管理

### 3. ネットワークの帯域幅管理
- **例**: ネットワークで、帯域幅の使用時間を管理
- **実装**: インターバルをソートし、重複を統合
- **メリット**: 効率的な帯域幅管理

### 4. データベースのクエリ最適化
- **例**: データベースで、時間範囲のクエリを最適化
- **実装**: インターバルをソートし、効率的にクエリ
- **メリット**: クエリの実行時間を短縮

### 5. ゲーム開発
- **例**: ゲームで、イベントの時間範囲を管理
- **実装**: インターバルをソートし、重複を処理
- **メリット**: 効率的なイベント管理

### 6. 金融取引システム
- **例**: 金融取引で、取引時間の範囲を管理
- **実装**: インターバルをソートし、重複を統合
- **メリット**: 効率的な取引管理

## 実装時の注意点

### 1. ソートの重要性
- **問題**: インターバルをソートすることで、処理が簡単になる
- **解決策**: 開始点でソート（終了点でソートする場合もある）
- **実装**: `intervals.sort(key=lambda x: x[0])`
- **メリット**: 重複チェックやマージが効率的に

### 2. 重複の判定
- **問題**: 2つのインターバルが重複しているか判定
- **解決策**: `intervals[i].end >= intervals[j].start`で重複を判定
- **実装**: ソート後、隣接するインターバルのみをチェック
- **注意**: 重複の定義を明確にする必要がある

### 3. マージ操作
- **問題**: 重複するインターバルを1つに統合
- **解決策**: 開始点の最小値と終了点の最大値を取る
- **実装**: `[min(start1, start2), max(end1, end2)]`
- **注意**: マージの条件を正確に理解する必要がある

### 4. エッジケースの処理
- **問題**: 空のリスト、1つのインターバル、重複がない場合
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if not intervals: return []`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

### 5. 包含関係の判定
- **問題**: インターバルAがインターバルBに含まれるか判定
- **解決策**: `A.start >= B.start and A.end <= B.end`
- **実装**: 包含関係を正確に判定
- **注意**: 等号を含めるかどうかを明確にする

## 関連するLeetCode/AtCoder問題

### Medium
- [Merge Intervals](./merge_intervals_logic.md) - インターバルのマージ
- [Insert Interval](./insert_interval_logic.md) - インターバルの挿入
- [Non-overlapping Intervals](./non_overlapping_intervals_logic.md) - 重複の削除
- [Meeting Rooms](./meeting_rooms_logic.md) - 会議室の予約

### Hard
- [Meeting Rooms II](../leetcode/medium/) - 複数の会議室
- [Employee Free Time](../leetcode/hard/) - 空き時間の検出

## 学習の進め方

1. **Merge Intervals**から始める: インターバル問題の最も基本的な例
2. **Insert Interval**で挿入操作を学ぶ: 新しいインターバルの処理
3. **Non-overlapping Intervals**で重複削除を学ぶ: 貪欲法の応用
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Merge Intervals のロジック解説](./merge_intervals_logic.md)
- [Insert Interval のロジック解説](./insert_interval_logic.md)
- [ソートテクニック](../06_sorting/README.md) - インターバル問題と組み合わせて使用

---

**重要**: インターバル問題では、ソートが鍵となります。ソートすることで、重複チェックやマージが効率的に行えます。


- [高度な文字列アルゴリズム (Advanced String Algorithms)](#高度な文字列アルゴリズム-advanced-string-algorithms)


---

# 高度な文字列アルゴリズム (Advanced String Algorithms)

## 概要

高度な文字列アルゴリズムは、文字列の検索、マッチング、解析を効率的に行うためのアルゴリズムです。KMP、Rabin-Karp、Manacherなどのアルゴリズムは、文字列処理の性能を大幅に向上させます。テキストエディタ、検索エンジン、コンパイラなどで広く使用されています。

## 基本概念

### 主要なアルゴリズム

1. **KMP (Knuth-Morris-Pratt)**: パターンマッチングをO(n+m)で実行
2. **Rabin-Karp**: ローリングハッシュを使ったパターンマッチング
3. **Manacher's Algorithm**: 最長パリンドローム部分文字列をO(n)で検出

### 主な操作と計算量

| アルゴリズム | 時間計算量 | 空間計算量 | 適用場面 |
|------------|-----------|-----------|---------|
| KMP | O(n + m) | O(m) | パターンマッチング |
| Rabin-Karp | O(n + m)平均 | O(1) | 複数パターンの検索 |
| Manacher | O(n) | O(n) | パリンドローム検出 |

**注意**: これらのアルゴリズムは、単純な文字列検索より効率的です。

## いつ使うべきか

高度な文字列アルゴリズムは以下のような場面で威力を発揮します：

### 1. パターンマッチング
- テキスト内でパターンを検索
- 複数のパターンを同時に検索

### 2. パリンドローム検出
- 最長のパリンドローム部分文字列を検出
- パリンドロームの数をカウント

### 3. 文字列の解析
- コンパイラの構文解析
- 正規表現エンジン

### 4. テキスト検索
- 検索エンジンの実装
- テキストエディタの検索機能

## 現実世界での応用例

### 1. テキストエディタの検索機能
- **例**: Vim、VS Codeなどの検索機能
- **実装**: KMPアルゴリズムでパターンを検索
- **メリット**: 高速なテキスト検索

### 2. 検索エンジン
- **例**: Google検索エンジン
- **実装**: Rabin-Karpで複数のキーワードを検索
- **メリット**: 効率的なキーワード検索

### 3. コンパイラの構文解析
- **例**: プログラミング言語のコンパイラ
- **実装**: KMPでキーワードや演算子を検索
- **メリット**: 高速な構文解析

### 4. DNA配列解析
- **例**: バイオインフォマティクスでのDNA配列の検索
- **実装**: KMPやRabin-Karpでパターンを検索
- **メリット**: 効率的なDNA配列解析

### 5. ネットワークセキュリティ
- **例**: 侵入検知システムでのパターンマッチング
- **実装**: KMPで悪意のあるパターンを検出
- **メリット**: リアルタイムの脅威検出

### 6. データ圧縮
- **例**: データ圧縮アルゴリズムでの文字列マッチング
- **実装**: KMPで繰り返しパターンを検出
- **メリット**: 効率的なデータ圧縮

## 実装時の注意点

### 1. KMPアルゴリズム
- **問題**: 失敗関数（failure function）の構築が複雑
- **解決策**: パターンの最長の接頭辞と接尾辞を事前に計算
- **実装**: `lps`（Longest Proper Prefix）配列を構築
- **注意**: 失敗関数の構築が重要

### 2. Rabin-Karpアルゴリズム
- **問題**: ハッシュの衝突を処理する必要がある
- **解決策**: ハッシュが一致した場合、実際の文字列を比較
- **実装**: ローリングハッシュを使用
- **注意**: ハッシュの衝突に注意

### 3. Manacher's Algorithm
- **問題**: パリンドロームの中心と半径を追跡
- **解決策**: ミラーリングテクニックを使用
- **実装**: 既に計算したパリンドロームの情報を再利用
- **注意**: アルゴリズムの理解が重要

### 4. 時間計算量の理解
- **問題**: 各アルゴリズムの時間計算量を正確に理解する必要がある
- **解決策**: アルゴリズムの動作を詳しく理解
- **実装**: 時間計算量を考慮した実装
- **注意**: 最悪時間計算量と平均時間計算量の違い

## 関連するLeetCode/AtCoder問題

### Medium
- [KMP Algorithm](./kmp_algorithm_logic.md) - パターンマッチングの基本
- [Rabin-Karp](./rabin_karp_logic.md) - ローリングハッシュ
- [Manacher's Algorithm](./manacher_algorithm_logic.md) - パリンドローム検出

### Hard
- [Shortest Palindrome](../leetcode/hard/) - KMPの応用
- [Longest Palindromic Substring](../leetcode/medium/) - Manacherの応用

## 学習の進め方

1. **KMP Algorithm**から始める: パターンマッチングの基本
2. **Rabin-Karp**でローリングハッシュを学ぶ: 複数パターンの検索
3. **Manacher's Algorithm**でパリンドローム検出を学ぶ: 高度な文字列処理
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [KMP Algorithm のロジック解説](./kmp_algorithm_logic.md)
- [Rabin-Karp のロジック解説](./rabin_karp_logic.md)
- [文字列処理テクニック](../11_string_manipulation/README.md) - 基本の文字列処理

---

**重要**: 高度な文字列アルゴリズムは、大規模なテキスト処理で威力を発揮します。各アルゴリズムの動作原理を理解することが重要です。


- [高度なグラフアルゴリズム (Advanced Graph Algorithms)](#高度なグラフアルゴリズム-advanced-graph-algorithms)


---

# 高度なグラフアルゴリズム (Advanced Graph Algorithms)

## 概要

高度なグラフアルゴリズムは、グラフ構造を効率的に処理するためのアルゴリズムです。トポロジカルソート、最短経路アルゴリズム（Dijkstra、Bellman-Ford）、最小全域木（Kruskal、Prim）など、多くの実用的な問題で使用されます。ネットワークルーティング、スケジューリング、最適化問題などで広く応用されています。

## 基本概念

### 主要なアルゴリズム

1. **トポロジカルソート**: 有向非巡回グラフ（DAG）のノードを順序付け
2. **Dijkstra**: 非負の重みを持つグラフの最短経路
3. **Bellman-Ford**: 負の重みも扱える最短経路
4. **Kruskal**: 最小全域木（MST）の構築
5. **Prim**: 最小全域木（MST）の構築

### 主な操作と計算量

| アルゴリズム | 時間計算量 | 空間計算量 | 適用場面 |
|------------|-----------|-----------|---------|
| トポロジカルソート | O(V + E) | O(V) | DAGの順序付け |
| Dijkstra | O((V + E) log V) | O(V) | 非負重みの最短経路 |
| Bellman-Ford | O(V × E) | O(V) | 負重みの最短経路 |
| Kruskal | O(E log E) | O(V) | MSTの構築 |
| Prim | O((V + E) log V) | O(V) | MSTの構築 |

**注意**: Vは頂点数、Eは辺数です。

## いつ使うべきか

高度なグラフアルゴリズムは以下のような場面で威力を発揮します：

### 1. 依存関係の解決
- タスクの実行順序
- パッケージの依存関係
- コンパイル順序

### 2. 最短経路問題
- 地図アプリケーション
- ネットワークルーティング
- ゲームのパスファインディング

### 3. 最小全域木
- ネットワーク設計
- クラスタリング
- 画像処理

### 4. スケジューリング
- タスクのスケジューリング
- リソースの割り当て
- プロジェクト管理

## 現実世界での応用例

### 1. コンパイラの依存関係解決
- **例**: プログラミング言語のコンパイラで、モジュールのコンパイル順序を決定
- **実装**: トポロジカルソートで依存関係を解決
- **メリット**: 効率的なコンパイル

### 2. 地図アプリケーション
- **例**: Google Mapsで、最短経路を計算
- **実装**: Dijkstraアルゴリズムで最短経路を計算
- **メリット**: 効率的なルート検索

### 3. ネットワーク設計
- **例**: データセンターのネットワーク設計
- **実装**: 最小全域木で最適な接続を構築
- **メリット**: コスト効率的なネットワーク

### 4. パッケージマネージャー
- **例**: npm、pipなどのパッケージマネージャー
- **実装**: トポロジカルソートで依存関係を解決
- **メリット**: 効率的なパッケージインストール

### 5. ゲーム開発
- **例**: ゲームのAIで、最短経路を計算
- **実装**: A*アルゴリズム（Dijkstraの拡張）でパスファインディング
- **メリット**: 効率的なAIの移動

### 6. 物流システム
- **例**: 配送ルートの最適化
- **実装**: 最短経路アルゴリズムで最適なルートを計算
- **メリット**: コストの削減

## 実装時の注意点

### 1. グラフの表現
- **問題**: グラフをどのように表現するか（隣接リスト vs 隣接行列）
- **解決策**: 通常は隣接リストが効率的
- **実装**: `graph = defaultdict(list)`で表現
- **注意**: スパースグラフでは隣接リストが有利

### 2. 優先度付きキュー
- **問題**: DijkstraやPrimで優先度付きキューが必要
- **解決策**: `heapq`モジュールを使用
- **実装**: `heapq.heappush(heap, (distance, node))`
- **注意**: 距離を最初の要素にすることで、最小値が先頭に来る

### 3. 負の重みの扱い
- **問題**: 負の重みがある場合、Dijkstraは使用できない
- **解決策**: Bellman-Fordを使用
- **実装**: 負のサイクルを検出する必要がある
- **注意**: 負のサイクルがある場合、最短経路は存在しない

### 4. サイクルの検出
- **問題**: トポロジカルソートでサイクルを検出
- **解決策**: DFSでサイクルを検出
- **実装**: 訪問済み、処理中、完了の3つの状態を管理
- **注意**: サイクルがある場合、トポロジカルソートは不可能

## 関連するLeetCode/AtCoder問題

### Medium
- [Topological Sort](./topological_sort_logic.md) - 依存関係の解決
- [Course Schedule](./course_schedule_logic.md) - トポロジカルソートの応用
- [Dijkstra Shortest Path](./dijkstra_shortest_path_logic.md) - 最短経路

### Hard
- [Bellman-Ford](./bellman_ford_logic.md) - 負重みの最短経路
- [Kruskal MST](./kruskal_mst_logic.md) - 最小全域木

## 学習の進め方

1. **Topological Sort**から始める: 依存関係の解決の基本
2. **Dijkstra**で最短経路を学ぶ: 非負重みの最短経路
3. **Kruskal**で最小全域木を学ぶ: MSTの構築
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Topological Sort のロジック解説](./topological_sort_logic.md)
- [Dijkstra Shortest Path のロジック解説](./dijkstra_shortest_path_logic.md)
- [グラフアルゴリズムテクニック](../10_graph_algorithms/README.md) - 基本のグラフアルゴリズム

---

**重要**: 高度なグラフアルゴリズムは、多くの実用的な問題の基礎となります。各アルゴリズムの動作原理と適用場面を理解することが重要です。


- [高度な数学的アルゴリズム (Advanced Mathematical Algorithms)](#高度な数学的アルゴリズム-advanced-mathematical-algorithms)


---

# 高度な数学的アルゴリズム (Advanced Mathematical Algorithms)

## 概要

高度な数学的アルゴリズムは、数論、組み合わせ論、モジュラー演算などの数学的概念を効率的に処理するためのアルゴリズムです。GCD/LCM、素数判定、組み合わせ計算、モジュラー演算など、多くの実用的な問題で使用されます。暗号化、データ分析、最適化問題などで広く応用されています。

## 基本概念

### 主要なアルゴリズム

1. **GCD/LCM**: 最大公約数と最小公倍数の計算
2. **Sieve of Eratosthenes**: 素数の効率的な列挙
3. **Combinatorics**: 組み合わせと順列の計算
4. **Modular Arithmetic**: モジュラー演算（合同式）

### 主な操作と計算量

| アルゴリズム | 時間計算量 | 空間計算量 | 適用場面 |
|------------|-----------|-----------|---------|
| GCD (Euclidean) | O(log min(a,b)) | O(1) | 最大公約数の計算 |
| LCM | O(log min(a,b)) | O(1) | 最小公倍数の計算 |
| Sieve of Eratosthenes | O(n log log n) | O(n) | 素数の列挙 |
| Combination | O(k) | O(1) | 組み合わせの計算 |
| Modular Exponentiation | O(log n) | O(1) | べき乗の計算 |

**注意**: 数学的アルゴリズムは、多くの場合、効率的な実装が可能です。

## いつ使うべきか

高度な数学的アルゴリズムは以下のような場面で威力を発揮します：

### 1. 数論問題
- 最大公約数・最小公倍数の計算
- 素数の判定と列挙
- 約数の計算

### 2. 組み合わせ問題
- 組み合わせと順列の計算
- 二項係数の計算
- カタラン数の計算

### 3. モジュラー演算
- 大きな数のべき乗
- 逆元の計算
- 合同式の計算

### 4. 暗号化
- RSA暗号
- ハッシュ関数
- 乱数生成

## 現実世界での応用例

### 1. 暗号化システム
- **例**: RSA暗号で、大きな数のべき乗を計算
- **実装**: モジュラー演算とGCDを使用
- **メリット**: セキュアな暗号化

### 2. データ分析
- **例**: データ分析で、組み合わせの数を計算
- **実装**: 組み合わせ計算を使用
- **メリット**: 効率的なデータ分析

### 3. ゲーム開発
- **例**: ゲームで、確率や組み合わせを計算
- **実装**: 組み合わせ計算を使用
- **メリット**: 効率的なゲーム処理

### 4. 金融計算
- **例**: 金融計算で、複利や組み合わせを計算
- **実装**: モジュラー演算と組み合わせ計算を使用
- **メリット**: 効率的な金融計算

### 5. コンピュータグラフィックス
- **例**: グラフィックスで、幾何学的計算を行う
- **実装**: GCD/LCMを使用
- **メリット**: 効率的なグラフィックス処理

### 6. データベース
- **例**: データベースで、ハッシュ関数を実装
- **実装**: モジュラー演算を使用
- **メリット**: 効率的なハッシュ計算

## 実装時の注意点

### 1. オーバーフローの注意
- **問題**: 大きな数の計算でオーバーフローが発生する可能性
- **解決策**: モジュラー演算を使用、または大きな数型を使用
- **実装**: Pythonでは自動的に大きな整数を扱える
- **注意**: 他の言語では注意が必要

### 2. モジュラー演算の性質
- **問題**: モジュラー演算の性質を理解する必要がある
- **解決策**: 加算、減算、乗算は通常通り、除算は逆元を使用
- **実装**: `(a + b) % mod`, `(a * b) % mod`など
- **注意**: 除算は`pow(a, mod-2, mod)`で逆元を計算

### 3. 組み合わせ計算の効率化
- **問題**: 組み合わせ計算で、階乗が大きくなりすぎる可能性
- **解決策**: モジュラー演算を使用、または動的計画法で計算
- **実装**: `C(n,k) = fact[n] * inv_fact[k] * inv_fact[n-k] % mod`
- **注意**: 事前計算で階乗と逆元を計算

### 4. 素数判定の効率化
- **問題**: 大きな数の素数判定が非効率
- **解決策**: Sieve of Eratosthenesで事前に計算
- **実装**: エラトステネスの篩で素数を列挙
- **注意**: メモリ使用量に注意

## 関連するLeetCode/AtCoder問題

### Medium
- [GCD/LCM](./gcd_lcm_logic.md) - 最大公約数と最小公倍数
- [Sieve of Eratosthenes](./sieve_of_eratosthenes_logic.md) - 素数の列挙
- [Combinatorics](./combinatorics_logic.md) - 組み合わせと順列
- [Modular Arithmetic](./modular_arithmetic_logic.md) - モジュラー演算

### Hard
- [Count Primes](../leetcode/medium/) - 素数の数
- [Unique Paths](../leetcode/medium/) - 組み合わせの応用

## 学習の進め方

1. **GCD/LCM**から始める: 数学的アルゴリズムの基本
2. **Sieve of Eratosthenes**で素数を学ぶ: 効率的な素数判定
3. **Combinatorics**で組み合わせを学ぶ: 組み合わせと順列
4. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [GCD/LCM のロジック解説](./gcd_lcm_logic.md)
- [Sieve of Eratosthenes のロジック解説](./sieve_of_eratosthenes_logic.md)
- [数学的アルゴリズムテクニック](../13_mathematical/README.md) - 基本の数学的アルゴリズム

---

**重要**: 高度な数学的アルゴリズムは、多くの実用的な問題の基礎となります。各アルゴリズムの数学的背景を理解することが重要です。


- [セグメント木 (Segment Tree)](#セグメント木-segment-tree)


---

# セグメント木 (Segment Tree)

## 概要

セグメント木は、配列の範囲クエリ（合計、最小値、最大値など）を効率的に処理するデータ構造です。AtCoderで頻出のテクニックで、**範囲クエリと点更新をO(log n)で実行**できます。累積和と異なり、**要素の更新も効率的**に処理できます。

## 基本概念

### セグメント木の構造

1. **完全二分木**: 配列を完全二分木として表現
2. **葉ノード**: 各要素に対応
3. **内部ノード**: 子ノードの情報を統合（合計、最小値など）

#### 視覚的イメージ

**セグメント木の構造（配列: [1, 3, 5, 7]）**
```
配列インデックス: 0  1  2  3
値:            [1, 3, 5, 7]

セグメント木（合計）:
                [16]
               /    \
            [4]      [12]
           /   \     /   \
         [1]  [3]  [5]  [7]
         0    1    2    3

各ノードは範囲の合計を保持:
- [16]: 範囲[0,3]の合計 = 16
- [4]: 範囲[0,1]の合計 = 4
- [12]: 範囲[2,3]の合計 = 12
```

**範囲クエリ（[1,2]の合計）**
```
                [16]
               /    \
            [4]      [12]
           /   \     /   \
         [1]  [3]  [5]  [7]
         0    1    2    3
              ↑    ↑
           範囲[1,2] = 3 + 5 = 8

探索パス: ルート → 左子 → 右子 → 葉ノード
```

**点更新（インデックス1を4に更新）**
```
更新前:             更新後:
    [16]                [17]
   /    \              /    \
 [4]    [12]    →    [5]    [12]
/   \   /   \       /   \   /   \
1   3  5    7      1   4  5    7

影響を受けるノードのみ更新:
[3] → [4], [4] → [5], [16] → [17]
```

**配列表現**
```
インデックス: 0  1  2  3  4  5  6
値:         [16, 4, 12, 1, 3, 5, 7]
            ↑   ↑   ↑   ↑  ↑  ↑  ↑
           根  左  右  葉 葉 葉 葉

親 = (i-1) // 2
左の子 = 2*i + 1
右の子 = 2*i + 2
```

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 構築 | O(n) | O(n) | 初期化 |
| 範囲クエリ | O(log n) | O(1) | 範囲の合計/最小値/最大値 |
| 点更新 | O(log n) | O(1) | 要素の更新 |

**注意**: セグメント木は、範囲更新もO(log n)で処理できます（遅延評価を使用）。

## いつ使うべきか

セグメント木は以下のような場面で威力を発揮します：

### 1. 範囲クエリ + 更新
- 範囲の合計/最小値/最大値を取得し、要素を更新
- 累積和では更新がO(n)だが、セグメント木はO(log n)

### 2. AtCoderの問題
- 範囲クエリと更新が混在する問題
- 遅延評価セグメント木が必要な問題

### 3. データ構造の問題
- 動的な範囲クエリを処理する必要がある場合

## 現実世界での応用例

### 1. データベースのクエリ最適化
- **例**: データベースで、範囲クエリと更新を効率的に処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: クエリの実行時間を短縮

### 2. ゲーム開発
- **例**: ゲームで、スコアの範囲クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なゲーム処理

### 3. 金融取引システム
- **例**: 金融取引で、価格の範囲クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的な取引処理

### 4. ログ分析
- **例**: ログ分析で、時間範囲のクエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なログ分析

### 5. 画像処理
- **例**: 画像処理で、矩形領域のクエリと更新を処理
- **実装**: 2次元セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的な画像処理

### 6. ネットワーク監視
- **例**: ネットワーク監視で、トラフィックの範囲クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なネットワーク監視

## 実装時の注意点

### 1. 配列のサイズ
- **問題**: セグメント木の配列サイズは2のべき乗に調整
- **解決策**: `size = 2 ** (n-1).bit_length()`でサイズを決定
- **実装**: 完全二分木にするため、サイズを調整
- **注意**: サイズを間違えると、インデックスの計算が複雑になる

### 2. インデックスの計算
- **問題**: 親子関係のインデックスを正確に計算する必要がある
- **解決策**: 
  - 親: `(i - 1) // 2`
  - 左の子: `2 * i + 1`
  - 右の子: `2 * i + 2`
- **実装**: インデックスの計算を正確に実装
- **注意**: 0-basedか1-basedかを明確にする

### 3. 遅延評価
- **問題**: 範囲更新を効率的に処理する必要がある場合
- **解決策**: 遅延評価セグメント木を使用
- **実装**: 更新を遅延させ、必要になったときに適用
- **注意**: 実装が複雑になる

## 関連するLeetCode/AtCoder問題

### Medium
- [Range Sum Query - Mutable](./range_sum_query_segment_tree_logic.md) - セグメント木の基本
- [Range Minimum Query](./range_minimum_query_logic.md) - 最小値クエリ

### Hard
- [Range Sum Query 2D - Mutable](../leetcode/hard/) - 2次元セグメント木

## 学習の進め方

1. **Range Sum Query**から始める: セグメント木の最も基本的な例
2. **Range Minimum Query**で最小値クエリを学ぶ: 異なる演算の適用
3. **より複雑な問題**に挑戦: 遅延評価セグメント木などの応用を学ぶ

## 次のステップ

- [Range Sum Query - Mutable のロジック解説](./range_sum_query_segment_tree_logic.md)
- [Range Minimum Query のロジック解説](./range_minimum_query_logic.md)
- [累積和テクニック](../19_prefix_sum/README.md) - セグメント木と比較

---

**重要**: セグメント木は、AtCoderで頻出のテクニックです。範囲クエリと更新が混在する問題で強力です。


- [座標圧縮 (Coordinate Compression)](#座標圧縮-coordinate-compression)


---

# 座標圧縮 (Coordinate Compression)

## 概要

座標圧縮は、大きな値の座標を連続する小さな整数にマッピングするテクニックです。AtCoderで頻出のテクニックで、**値の範囲が大きいが、実際に使用される値が少ない場合**に威力を発揮します。セグメント木やFenwick Treeと組み合わせて使用されることが多いです。

## 基本概念

### 座標圧縮の手順

1. **値の収集**: 全てのユニークな値を収集
2. **ソート**: 値をソート
3. **マッピング**: 各値をインデックスにマッピング

### 主な操作と計算量

| 操作 | 時間計算量 | 空間計算量 | 適用場面 |
|------|-----------|-----------|---------|
| 圧縮 | O(n log n) | O(n) | 値のマッピング |
| 逆変換 | O(1) | O(1) | インデックスから値への変換 |

**注意**: 座標圧縮は、値の順序を保持しながら、値を小さな整数にマッピングします。

## いつ使うべきか

座標圧縮は以下のような場面で威力を発揮します：

### 1. 大きな値の範囲
- 値の範囲が10^9など大きいが、実際に使用される値が10^5程度
- セグメント木やFenwick Treeのサイズを削減

### 2. AtCoderの問題
- 座標の範囲が大きいが、実際の座標が少ない問題
- セグメント木と組み合わせて使用

### 3. 離散化が必要な問題
- 連続値を離散値に変換する必要がある問題

## 現実世界での応用例

### 1. データベースのインデックス
- **例**: データベースで、大きなIDを小さなインデックスにマッピング
- **実装**: 座標圧縮でIDをインデックスに変換
- **メリット**: インデックスのサイズを削減

### 2. 地理情報システム
- **例**: GISで、大きな座標を小さなインデックスにマッピング
- **実装**: 座標圧縮で座標をインデックスに変換
- **メリット**: メモリ効率的な処理

### 3. 画像処理
- **例**: 画像処理で、ピクセル座標を圧縮
- **実装**: 座標圧縮で座標をインデックスに変換
- **メリット**: 効率的な画像処理

### 4. ゲーム開発
- **例**: ゲームで、大きな座標を小さなインデックスにマッピング
- **実装**: 座標圧縮で座標をインデックスに変換
- **メリット**: 効率的なゲーム処理

### 5. データ分析
- **例**: データ分析で、大きな値を小さなインデックスにマッピング
- **実装**: 座標圧縮で値をインデックスに変換
- **メリット**: 効率的なデータ分析

### 6. ネットワーク分析
- **例**: ネットワーク分析で、大きなノードIDを小さなインデックスにマッピング
- **実装**: 座標圧縮でIDをインデックスに変換
- **メリット**: 効率的なネットワーク分析

## 実装時の注意点

### 1. 値の収集
- **問題**: 全てのユニークな値を収集する必要がある
- **解決策**: セットを使用してユニークな値を収集
- **実装**: `unique_values = sorted(set(values))`
- **注意**: ソートすることで、順序を保持

### 2. マッピングの作成
- **問題**: 値からインデックスへのマッピングを作成
- **解決策**: 辞書を使用してマッピングを作成
- **実装**: `compression = {val: idx for idx, val in enumerate(unique_values)}`
- **注意**: マッピングを正確に作成する必要がある

### 3. 逆変換
- **問題**: インデックスから値への逆変換が必要な場合
- **解決策**: 配列を使用して逆変換を実現
- **実装**: `decompression = unique_values`
- **注意**: 逆変換も効率的に実装可能

### 4. 時間計算量の理解
- **平均**: O(n log n) - ソートのコスト
- **最悪**: O(n log n) - 常に同じ時間計算量
- **空間**: O(n) - ユニークな値の配列とマッピング
- **注意**: ソートのコストが支配的

## 関連するLeetCode/AtCoder問題

### Medium
- [Coordinate Compression](./coordinate_compression_logic.md) - 座標圧縮の基本

### Hard
- [Count of Smaller Numbers After Self](../leetcode/hard/) - 座標圧縮 + セグメント木
- [Reverse Pairs](../leetcode/hard/) - 座標圧縮 + セグメント木

## 学習の進め方

1. **Coordinate Compression**から始める: 座標圧縮の最も基本的な例
2. **セグメント木と組み合わせ**: 座標圧縮 + セグメント木の問題に挑戦
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [Coordinate Compression のロジック解説](./coordinate_compression_logic.md)
- [セグメント木テクニック](../25_segment_tree/README.md) - 座標圧縮と組み合わせて使用
- [累積和テクニック](../19_prefix_sum/README.md) - 座標圧縮と組み合わせて使用

---

**重要**: 座標圧縮は、AtCoderで頻出のテクニックです。大きな値の範囲を小さな整数にマッピングすることで、セグメント木などのデータ構造を効率的に使用できます。


- [設計問題 (Design Problems)](#設計問題-design-problems)


---

# 設計問題 (Design Problems)

## 概要

設計問題は、特定の機能を持つデータ構造やシステムを設計する問題です。LRU Cache、Twitter、Hit Counterなどの実用的なシステムを設計します。**適切なデータ構造の選択**と**効率的な操作の実装**が鍵となります。

## 基本概念

### 設計問題の特徴

1. **複数の操作**: 複数の操作を効率的にサポートする必要がある
2. **データ構造の組み合わせ**: 複数のデータ構造を組み合わせて使用
3. **時間・空間のトレードオフ**: 時間効率と空間効率のバランスを取る

### 主な設計パターン

| 設計パターン | 時間計算量 | 空間計算量 | 適用場面 |
|------------|-----------|-----------|---------|
| LRU Cache | O(1) | O(capacity) | キャッシュシステム |
| Twitter | O(1)投稿, O(n)取得 | O(n) | ソーシャルメディア |
| Hit Counter | O(1) | O(300) | カウンターシステム |

**注意**: 設計問題では、各操作の時間計算量を最適化することが重要です。

## いつ使うべきか

設計問題は以下のような場面で威力を発揮します：

### 1. キャッシュシステム
- LRU Cache
- LFU Cache
- タイムベースキャッシュ

### 2. ソーシャルメディア
- Twitter
- Facebook
- Instagram

### 3. カウンターシステム
- Hit Counter
- Rate Limiter
- アクセスカウンター

### 4. データベース設計
- インデックスの設計
- クエリの最適化

## 現実世界での応用例

### 1. Webアプリケーション
- **例**: Webアプリケーションで、セッション管理やキャッシュを実装
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なWebアプリケーション

### 2. ソーシャルメディアプラットフォーム
- **例**: Twitter、Facebookなどのソーシャルメディア
- **実装**: タイムラインの管理、フォロー関係の管理
- **メリット**: 効率的なソーシャルメディア

### 3. ゲーム開発
- **例**: ゲームで、リーダーボードやスコア管理を実装
- **実装**: 適切なデータ構造で管理
- **メリット**: 効率的なゲーム処理

### 4. データベースシステム
- **例**: データベースで、インデックスやキャッシュを設計
- **実装**: 適切なデータ構造で管理
- **メリット**: 効率的なデータベース

### 5. ネットワークシステム
- **例**: ネットワークで、ルーティングテーブルやキャッシュを設計
- **実装**: 適切なデータ構造で管理
- **メリット**: 効率的なネットワーク

### 6. モバイルアプリケーション
- **例**: モバイルアプリで、オフラインキャッシュを実装
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なモバイルアプリ

## 実装時の注意点

### 1. データ構造の選択
- **問題**: どのデータ構造を選択するかが重要
- **解決策**: 各操作の時間計算量を考慮
- **実装**: ハッシュマップ、双方向リンクリスト、ヒープなどを組み合わせ
- **注意**: データ構造の組み合わせが重要

### 2. 時間計算量の最適化
- **問題**: 各操作を効率的に実装する必要がある
- **解決策**: O(1)またはO(log n)を目指す
- **実装**: 適切なデータ構造を使用
- **注意**: 時間計算量の最適化が重要

### 3. 空間計算量の考慮
- **問題**: メモリ使用量も考慮する必要がある
- **解決策**: 時間効率と空間効率のバランスを取る
- **実装**: 必要最小限のデータ構造を使用
- **注意**: 空間計算量も重要

### 4. エッジケースの処理
- **問題**: エッジケースを適切に処理する必要がある
- **解決策**: 各操作でエッジケースをチェック
- **実装**: 空の状態、容量制限、無効な入力などの処理
- **注意**: エッジケースの処理が重要

## 関連するLeetCode/AtCoder問題

### Medium
- [LRU Cache](./lru_cache_logic.md) - キャッシュシステムの基本
- [Design Twitter](./design_twitter_logic.md) - ソーシャルメディアの設計
- [Design Hit Counter](./design_hit_counter_logic.md) - カウンターシステム

### Hard
- [LFU Cache](../leetcode/hard/) - より複雑なキャッシュシステム
- [Design Search Autocomplete System](../leetcode/hard/) - 自動補完システム

## 学習の進め方

1. **LRU Cache**から始める: 設計問題の最も基本的な例
2. **Design Twitter**で複雑な設計を学ぶ: 複数の操作の組み合わせ
3. **より複雑な問題**に挑戦: 他のテクニックと組み合わせた使用法を学ぶ

## 次のステップ

- [LRU Cache のロジック解説](./lru_cache_logic.md)
- [Design Twitter のロジック解説](./design_twitter_logic.md)
- [データ構造テクニック](../01_hash_table/README.md) - 基本のデータ構造

---

**重要**: 設計問題では、適切なデータ構造の選択と効率的な操作の実装が重要です。各操作の時間計算量を最適化することを心がけましょう。


- [問題パターン識別ガイド (Problem Pattern Recognition Guide)](#問題パターン識別ガイド-problem-pattern-recognition-guide)


---

# 問題パターン識別ガイド (Problem Pattern Recognition Guide)

## 概要

問題パターン識別ガイドは、LeetCodeやAtCoderの問題を効率的に解くための**問題パターンの識別方法**を解説します。問題を見たときに、どのアルゴリズムやデータ構造を使うべきかを素早く判断できるようになることが目標です。

## 基本概念

### パターン識別の重要性

1. **時間の節約**: 適切なアプローチを素早く選択
2. **効率的な解決**: 最適なアルゴリズムを選択
3. **学習の効率化**: パターンを理解することで、類似問題を素早く解決

### 主要な識別ポイント

| 識別ポイント | パターン | 適用アルゴリズム |
|------------|---------|----------------|
| 範囲クエリ | 範囲の合計/最小値/最大値 | 累積和、セグメント木 |
| 最短経路 | グラフの最短経路 | Dijkstra、BFS |
| 組み合わせ | 全ての組み合わせを生成 | バックトラッキング |
| 最適化問題 | 最適な選択を求める | 動的計画法、貪欲法 |

## 問題パターンの分類

### 1. 配列・文字列問題
- **特徴**: 配列や文字列の操作
- **パターン**: 検索、ソート、マッチング
- **アルゴリズム**: 二ポインタ、スライディングウィンドウ、ハッシュテーブル

### 2. グラフ問題
- **特徴**: ノードとエッジの関係
- **パターン**: 探索、最短経路、サイクル検出
- **アルゴリズム**: DFS、BFS、Dijkstra、Union-Find

### 3. 木問題
- **特徴**: 階層構造
- **パターン**: 探索、パス、構築
- **アルゴリズム**: DFS、BFS、再帰

### 4. 動的計画法問題
- **特徴**: 最適化問題、重複する部分問題
- **パターン**: 最適な選択、組み合わせ
- **アルゴリズム**: メモ化、ボトムアップDP

### 5. 貪欲法問題
- **特徴**: 局所最適選択が全体最適解
- **パターン**: スケジューリング、選択問題
- **アルゴリズム**: 貪欲法

## 現実世界での応用例

### 1. 競技プログラミング
- **シナリオ**: LeetCodeやAtCoderで、問題を素早く識別
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的な問題解決

### 2. 技術面接
- **シナリオ**: 技術面接で、問題のアプローチを素早く決定
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的な面接準備

### 3. アルゴリズム学習
- **シナリオ**: アルゴリズム学習で、問題のパターンを理解
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的な学習

### 4. コードレビュー
- **シナリオ**: コードレビューで、適切なアルゴリズムを提案
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的なコードレビュー

### 5. システム設計
- **シナリオ**: システム設計で、適切なデータ構造を選択
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的なシステム設計

### 6. 問題解決
- **シナリオ**: 実務で、問題のアプローチを決定
- **実装**: パターン識別ガイドで問題を分類
- **メリット**: 効率的な問題解決

## 学習の進め方

1. **Problem Pattern Guide**から始める: 問題パターンの基本分類
2. **Technique Combination Guide**で組み合わせを学ぶ: 複数のテクニックの組み合わせ
3. **Optimization Techniques**で最適化を学ぶ: アルゴリズムの最適化

## 次のステップ

- [Problem Pattern Guide の解説](./problem_pattern_guide.md)
- [Technique Combination Guide の解説](./technique_combination_guide.md)
- [Optimization Techniques の解説](./optimization_techniques.md)

---

**重要**: 問題パターン識別は、効率的な問題解決の鍵です。問題を見たときに、どのアルゴリズムを使うべきかを素早く判断できるようになりましょう。


