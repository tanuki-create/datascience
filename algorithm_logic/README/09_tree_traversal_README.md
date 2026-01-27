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

