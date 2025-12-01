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
├── 13_mathematical/                   # 数学的アルゴリズム
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

