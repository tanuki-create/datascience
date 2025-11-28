# Maximum Depth of Binary Tree - ロジック解説

## 問題概要

二分木の最大深度（根から最も遠い葉ノードまでの距離）を求める。

**例**:
```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

## ロジックの核心

### DFS（再帰的アプローチ）

**考え方**:
- 木の最大深度 = 1 + max(左部分木の最大深度, 右部分木の最大深度)
- ベースケース: ノードがnullの場合は0を返す

### アルゴリズムのステップ

```
function maxDepth(root):
    if root is null:
        return 0
    
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    return 1 + max(left_depth, right_depth)
```

## 具体例でのトレース

```
        3
       / \
      9   20
          / \
         15  7

maxDepth(3):
  left = maxDepth(9) = 1
  right = maxDepth(20) = 2
  return 1 + max(1, 2) = 3
```

## 現実世界での応用

### 1. ファイルシステム
- **シナリオ**: ディレクトリ構造の最大深度を計算
- **実装**: 同様のDFSで深さを計算

### 2. 組織構造
- **シナリオ**: 組織の階層構造の最大深度を計算
- **実装**: 木構造として表現してDFSで計算

## 注意点と落とし穴

1. **nullチェック**: ノードがnullの場合の処理が重要
2. **再帰の深さ**: 深い木の場合、スタックオーバーフローに注意
3. **反復的実装**: スタックを使った反復的実装も可能

## 関連問題

- Minimum Depth of Binary Tree
- Balanced Binary Tree
- Diameter of Binary Tree

---

**次のステップ**: [Level Order Traversal](./level_order_traversal_logic.md)でBFSを学ぶ

