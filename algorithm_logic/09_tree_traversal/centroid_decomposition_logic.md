# 重心分解 (Centroid Decomposition) - ロジック解説

## 問題概要

重心分解は、**木を重心（centroid）で再帰的に分割する**テクニックです。重心は、その頂点を削除したときに残る部分木のサイズが全てn/2以下になる頂点です。O(n log n)で木を分割し、多くのクエリ問題を効率的に解くことができます。

**例**:
```
木:
    1
   / \
  2   3
 / \
4   5

重心: 2 (削除すると部分木のサイズが[1, 1, 1]で全て2以下)
```

## ロジックの核心

### なぜ重心分解が有効か？

**全探索（O(n²)）**:
- 全ての頂点ペアで距離を計算
- 時間計算量: O(n²) - 非効率

**重心分解を使う理由**:
- **分割統治**: 木を再帰的に分割
- **時間計算量**: O(n log n) - 各レベルでO(n)、レベル数がO(log n)
- **空間計算量**: O(n) - 各ノードの情報を保存

### アルゴリズムのステップ

```
function centroidDecomposition(tree):
    n = len(tree)
    size = [0] * n
    removed = [False] * n
    
    // 1. 部分木のサイズを計算
    function getSize(node, parent):
        size[node] = 1
        for neighbor in tree[node]:
            if neighbor != parent and not removed[neighbor]:
                size[node] += getSize(neighbor, node)
        return size[node]
    
    // 2. 重心を見つける
    function findCentroid(node, parent, total_size):
        for neighbor in tree[node]:
            if neighbor != parent and not removed[neighbor]:
                if size[neighbor] > total_size // 2:
                    return findCentroid(neighbor, node, total_size)
        return node
    
    // 3. 重心分解を実行
    function decompose(node):
        getSize(node, -1)
        centroid = findCentroid(node, -1, size[node])
        removed[centroid] = True
        
        // 重心での処理
        process(centroid)
        
        // 各部分木を再帰的に処理
        for neighbor in tree[centroid]:
            if not removed[neighbor]:
                decompose(neighbor)
    
    decompose(0)
```

### 具体例でのトレース

#### 例: 重心分解の実行

**木**:
```
    1
   / \
  2   3
 / \
4   5
```

**ステップ1: 部分木のサイズを計算**
```
getSize(1, -1):
  子ノード: [2, 3]
  
  getSize(2, 1):
    子ノード: [4, 5]
    
    getSize(4, 2):
      葉ノード
      size[4] = 1
      return 1
    
    getSize(5, 2):
      葉ノード
      size[5] = 1
      return 1
    
    size[2] = 1 + 1 + 1 = 3
    return 3
  
  getSize(3, 1):
    葉ノード
    size[3] = 1
    return 1
  
  size[1] = 1 + 3 + 1 = 5
  return 5

サイズ配列: size = [5, 3, 1, 1, 1]
```

**ステップ2: 重心を見つける**
```
findCentroid(1, -1, 5):
  子ノード: [2, 3]
  
  ノード2: size[2] = 3 > 5/2 = 2.5 → 重心ではない
  ノード3: size[3] = 1 <= 2.5 → 重心の可能性
  
  findCentroid(2, 1, 5):
    子ノード: [4, 5]
    
    ノード4: size[4] = 1 <= 2.5
    ノード5: size[5] = 1 <= 2.5
    
    ノード2を削除した場合:
      部分木のサイズ: [1, 1, 1] (全て2以下)
      → ノード2が重心
    
    return 2

重心: 2
```

**ステップ3: 重心分解を実行**
```
decompose(1):
  getSize(1, -1) → size = [5, 3, 1, 1, 1]
  centroid = findCentroid(1, -1, 5) = 2
  removed[2] = True
  
  process(2): 重心2での処理
  
  各部分木を再帰的に処理:
    decompose(4): 部分木{4}
    decompose(5): 部分木{5}
    decompose(1): 部分木{1, 3}
```

## 現実世界での応用

### 1. 距離クエリ
- **シナリオ**: 2頂点間の距離を効率的に計算
- **実装**: 重心分解で距離を計算
- **メリット**: O(log n)で距離を計算

### 2. パスカウント
- **シナリオ**: 条件を満たすパスの数を数える
- **実装**: 重心分解でパスをカウント
- **メリット**: 効率的なパスカウント

### 3. 最近傍探索
- **シナリオ**: クエリ点に最も近い点を見つける
- **実装**: 重心分解で最近傍を探索
- **メリット**: 効率的な最近傍探索

### 4. 範囲クエリ
- **シナリオ**: 範囲内の頂点を効率的に検索
- **実装**: 重心分解で範囲クエリを処理
- **メリット**: 効率的な範囲クエリ

### 5. ネットワーク分析
- **シナリオ**: ネットワークの構造を分析
- **実装**: 重心分解でネットワークを分割
- **メリット**: 効率的なネットワーク分析

### 6. クラスタリング
- **シナリオ**: 木構造のデータをクラスタリング
- **実装**: 重心分解でクラスタを構築
- **メリット**: 効率的なクラスタリング

## 注意点と落とし穴

### 1. 重心の一意性
- **問題**: 重心は必ずしも一意ではない
- **解決策**: 任意の重心を選択
- **実装**: 最初に見つかった重心を使用
- **注意**: どの重心を選んでも結果は同じ

### 2. 部分木のサイズの計算
- **問題**: 削除されたノードを除外する必要がある
- **解決策**: `removed`配列で削除されたノードを記録
- **実装**: `if not removed[neighbor]:`でチェック
- **注意**: 削除されたノードを考慮しないと結果が間違う

### 3. 再帰の深さ
- **問題**: 再帰の深さがO(log n)
- **解決策**: 通常は問題ないが、スタックオーバーフローに注意
- **実装**: 必要に応じて反復的な実装を使用
- **注意**: 大きな木ではスタックオーバーフローに注意

### 4. 時間計算量の理解
- **問題**: 各レベルでO(n)、レベル数がO(log n)
- **解決策**: 合計でO(n log n)
- **実装**: 効率的な実装を心がける
- **注意**: 実装によってはO(n log² n)になる場合がある

### 5. メモリ使用量
- **問題**: O(n)のメモリが必要
- **解決策**: 必要に応じて最適化
- **実装**: 不要な情報を削除
- **注意**: メモリ制約がある場合は注意

### 6. 重心の検出
- **問題**: 重心の検出が重要
- **解決策**: 部分木のサイズを正確に計算
- **実装**: `size[neighbor] > total_size // 2`で判定
- **注意**: 判定を間違えると効率が悪くなる

### 7. 処理の順序
- **問題**: 重心での処理の順序が重要
- **解決策**: 重心での処理を先に行い、その後各部分木を処理
- **実装**: `process(centroid)`を先に実行
- **注意**: 順序を間違えると結果が間違う

## 関連問題

- [Tree Distance Queries](../leetcode/hard/) - 距離クエリ
- [Path Counting](../leetcode/hard/) - パスカウント
- [Nearest Neighbor Search](../leetcode/hard/) - 最近傍探索

---

**次のステップ**: [オイラーツアー](./euler_tour_logic.md)で木の線形化を学ぶ

