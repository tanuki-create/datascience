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
└── 13_mathematical/                   # 数学的アルゴリズム
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
   - 3Sum

3. **[スライディングウィンドウ](03_sliding_window/README.md)** - 連続する部分列の問題に最適
   - Longest Substring Without Repeating Characters
   - Minimum Window Substring

### Phase 2: データ構造

4. **[スタック・キュー](04_stack_queue/README.md)** - LIFO/FIFOの特性を活かす
5. **[二分探索](05_binary_search/README.md)** - ソート済み配列での高速検索

### Phase 3: 高度なアルゴリズム

6. **[動的計画法](07_dynamic_programming/README.md)** - 最適化問題の強力な手法
7. **[貪欲法](08_greedy/README.md)** - 局所最適解を積み重ねる
8. **[木の探索](09_tree_traversal/README.md)** - DFS/BFSの理解

### Phase 4: 専門テクニック

9. **[グラフアルゴリズム](10_graph_algorithms/README.md)** - ネットワーク構造の処理
10. **[文字列処理](11_string_manipulation/README.md)** - 高度な文字列マッチング
11. **[ビット操作](12_bit_manipulation/README.md)** - メモリ効率的な処理
12. **[数学的アルゴリズム](13_mathematical/README.md)** - 数論と組み合わせ論

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

---

**注意**: このシリーズはロジックの理解を重視しています。実装の詳細が必要な場合は、[leetcode](../leetcode/)ディレクトリ内の各問題の`solution.py`を参照してください。

