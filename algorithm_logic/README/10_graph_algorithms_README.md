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

