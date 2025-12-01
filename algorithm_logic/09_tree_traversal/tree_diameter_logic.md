# 木の直径 (Tree Diameter) - ロジック解説

## 問題概要

木の直径は、**木の任意の2頂点間の最短経路の最大長**です。2つのアプローチがあります：1) 任意の頂点から最も遠い頂点を見つけ、その頂点から最も遠い頂点までの距離を計算する方法、2) 各ノードで2つの最深の子ノードの距離の最大値を計算する方法（木DP）。O(n)で計算できます。

**例**:
```
木:
    1
   / \
  2   3
 / \
4   5

直径: 4 (4→2→1→3 または 5→2→1→3)
```

## ロジックの核心

### なぜ2回のDFSが有効か？

**全探索（O(n²)）**:
- 全ての頂点ペアで距離を計算
- 時間計算量: O(n²) - 非効率

**2回のDFSを使う理由**:
- **最遠点の性質**: 任意の頂点から最も遠い頂点は直径の端点の1つ
- **時間計算量**: O(n) - 2回のDFS
- **空間計算量**: O(n) - 再帰の深さ

### アルゴリズムのステップ

#### 方法1: 2回のDFS

```
function treeDiameter(tree):
    // 1回目のDFS: 任意の頂点から最も遠い頂点を見つける
    def dfs(node, parent, depth):
        max_depth = depth
        farthest_node = node
        
        for neighbor in tree[node]:
            if neighbor != parent:
                depth_result, farthest = dfs(neighbor, node, depth + 1)
                if depth_result > max_depth:
                    max_depth = depth_result
                    farthest_node = farthest
        
        return max_depth, farthest_node
    
    // 0から開始して最も遠い頂点を見つける
    _, farthest1 = dfs(0, -1, 0)
    
    // 2回目のDFS: 最も遠い頂点から最も遠い頂点までの距離
    diameter, _ = dfs(farthest1, -1, 0)
    
    return diameter
```

#### 方法2: 木DP

```
function treeDiameterDP(root):
    max_diameter = 0
    
    def dfs(node, parent):
        max_depth = 0
        depths = []
        
        for child in tree[node]:
            if child != parent:
                depth = dfs(child, node)
                depths.append(depth)
                max_depth = max(max_depth, depth)
        
        // 2つの最深の子ノードの距離
        if len(depths) >= 2:
            depths.sort(reverse=True)
            diameter_at_node = depths[0] + depths[1] + 2
            max_diameter = max(max_diameter, diameter_at_node)
        elif len(depths) == 1:
            diameter_at_node = depths[0] + 1
            max_diameter = max(max_diameter, diameter_at_node)
        
        return max_depth + 1
    
    dfs(root, -1)
    return max_diameter
```

### 具体例でのトレース

#### 例: 木の直径の計算

**木**:
```
    1
   / \
  2   3
 / \
4   5
```

**方法1: 2回のDFS**

**1回目のDFS（頂点1から開始）**:
```
DFS(1, -1, 0):
  子ノード: [2, 3]
  
  DFS(2, 1, 1):
    子ノード: [4, 5]
    
    DFS(4, 2, 2):
      葉ノード
      return (2, 4)
    
    DFS(5, 2, 2):
      葉ノード
      return (2, 5)
    
    max_depth = max(2, 2) = 2
    farthest_node = 4 (または5)
    return (2, 4)
  
  DFS(3, 1, 1):
    葉ノード
    return (1, 3)
  
  max_depth = max(2, 1) = 2
  farthest_node = 4
  return (2, 4)

最も遠い頂点: 4
```

**2回目のDFS（頂点4から開始）**:
```
DFS(4, -1, 0):
  子ノード: [2]
  
  DFS(2, 4, 1):
    子ノード: [1, 5]
    
    DFS(1, 2, 2):
      子ノード: [3]
      
      DFS(3, 1, 3):
        葉ノード
        return (3, 3)
      
      return (3, 3)
    
    DFS(5, 2, 2):
      葉ノード
      return (2, 5)
    
    max_depth = max(3, 2) = 3
    farthest_node = 3
    return (3, 3)
  
  max_depth = 3
  farthest_node = 3
  return (3, 3)

直径: 3 (4→2→1→3)
```

**方法2: 木DP**

```
DFS(1, -1):
  子ノード: [2, 3]
  
  DFS(2, 1):
    子ノード: [4, 5]
    
    DFS(4, 2):
      葉ノード
      return 0
    
    DFS(5, 2):
      葉ノード
      return 0
    
    depths = [0, 0]
    max_depth = max(0, 0) = 0
    diameter_at_2 = 0 + 0 + 2 = 2
    return 1
  
  DFS(3, 1):
    葉ノード
    return 0
  
  depths = [1, 0]
  max_depth = max(1, 0) = 1
  diameter_at_1 = 1 + 0 + 2 = 3
  return 2

直径: max(2, 3) = 3
```

## 現実世界での応用

### 1. ネットワーク設計
- **シナリオ**: ネットワークの最大遅延を計算
- **実装**: 木の直径で最大遅延を計算
- **メリット**: ネットワークの性能評価

### 2. 配送ルートの最適化
- **シナリオ**: 配送センター間の最大距離を計算
- **実装**: 木の直径で最大距離を計算
- **メリット**: 配送ルートの最適化

### 3. データ構造の分析
- **シナリオ**: 木構造のデータの最大深さを分析
- **実装**: 木の直径で最大深さを計算
- **メリット**: データ構造の理解

### 4. ゲーム開発
- **シナリオ**: ゲームマップの最大距離を計算
- **実装**: 木の直径で最大距離を計算
- **メリット**: ゲームマップの設計

### 5. 組織構造の分析
- **シナリオ**: 組織の階層構造の最大深さを分析
- **実装**: 木の直径で最大深さを計算
- **メリット**: 組織構造の理解

### 6. ファイルシステムの分析
- **シナリオ**: ファイルシステムの最大深さを分析
- **実装**: 木の直径で最大深さを計算
- **メリット**: ファイルシステムの最適化

## 注意点と落とし穴

### 1. 親ノードの記録
- **問題**: 無向木では親ノードに戻らないようにする
- **解決策**: `parent`パラメータを使用
- **実装**: `if neighbor != parent:`で親ノードをスキップ
- **注意**: 親ノードを記録しないと無限ループになる

### 2. 2回のDFSの順序
- **問題**: 1回目のDFSで見つけた頂点から2回目のDFSを開始
- **解決策**: 1回目の結果を保存して2回目に使用
- **実装**: `_, farthest1 = dfs(0, -1, 0)`
- **注意**: 順序を間違えると正しい結果が得られない

### 3. 木DPでの直径の計算
- **問題**: 各ノードで2つの最深の子ノードの距離を計算
- **解決策**: 深さをソートして上位2つを選択
- **実装**: `depths.sort(reverse=True)`でソート
- **注意**: 子ノードが1つ以下の場合の処理に注意

### 4. エッジの重み
- **問題**: エッジに重みがある場合の処理
- **解決策**: 深さに重みを加算
- **実装**: `depth + weight`で重みを考慮
- **注意**: 重みを考慮しないと結果が間違う

### 5. 空の木の処理
- **問題**: 空の木（頂点数0）の場合の処理
- **解決策**: 頂点数をチェック
- **実装**: `if n == 0: return 0`
- **注意**: エッジケースの処理が重要

### 6. 単一頂点の処理
- **問題**: 頂点数が1の場合の処理
- **解決策**: 直径は0
- **実装**: `if n == 1: return 0`
- **注意**: エッジケースの処理が重要

### 7. 2つの方法の選択
- **問題**: 2回のDFSと木DPのどちらを使うか
- **解決策**: 
  - 2回のDFS: より直感的、実装が簡単
  - 木DP: より汎用的、他の情報も計算可能
- **実装**: 問題の要件に応じて選択
- **注意**: 両方の方法を理解することが重要

## 関連問題

- [Diameter of Binary Tree](../leetcode/easy/) - 二分木の直径
- [Tree Diameter](../leetcode/medium/) - 一般の木の直径
- [Binary Tree Maximum Path Sum](./binary_tree_max_path_sum_logic.md) - パスの最大和

---

**次のステップ**: [重心分解](./centroid_decomposition_logic.md)で木の分割を学ぶ

