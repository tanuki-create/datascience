# Range Minimum Query - ロジック解説

## 問題概要

配列`nums`が与えられたとき、範囲[i, j]の最小値を取得し、要素を更新するクエリを複数回処理する。

**制約**:
- `1 <= nums.length <= 10^5`
- クエリ数は最大10^5

**例**:
```
Input: nums = [1,3,2,5,4]
Query: query(0,2) → 1
Update: update(1,0) → nums = [1,0,2,5,4]
Query: query(0,2) → 0
```

## ロジックの核心

### なぜセグメント木が有効か？

**全探索（O(n)）**:
- 各クエリで範囲を走査して最小値を取得
- 時間計算量: O(n×q) - 非効率

**セグメント木を使う理由**:
- **範囲クエリ**: O(log n)で範囲の最小値を取得
- **点更新**: O(log n)で要素を更新
- **時間計算量**: O(q log n) - 大幅に改善

### 思考プロセス

1. **セグメント木の構築**: 合計の代わりに最小値を保存
2. **範囲クエリ**: 範囲に含まれるセグメントの最小値を統合
3. **点更新**: 葉ノードから根まで更新を伝播

### アルゴリズムのステップ

```
class SegmentTree:
    def __init__(self, nums):
        n = len(nums)
        self.n = n
        self.size = 2 ** (n-1).bit_length()
        self.tree = [float('inf')] * (2 * self.size)
        
        // 葉ノードに値を設定
        for i in range(n):
            self.tree[self.size + i] = nums[i]
        
        // 内部ノードを構築
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[2*i], self.tree[2*i+1])
    
    def update(self, index, val):
        index += self.size
        self.tree[index] = val
        
        // 親ノードを更新
        while index > 1:
            index //= 2
            self.tree[index] = min(self.tree[2*index], self.tree[2*index+1])
    
    def query(self, left, right):
        left += self.size
        right += self.size
        result = float('inf')
        
        while left <= right:
            if left % 2 == 1:
                result = min(result, self.tree[left])
                left += 1
            if right % 2 == 0:
                result = min(result, self.tree[right])
                right -= 1
            left //= 2
            right //= 2
        
        return result
```

## 具体例でのトレース

### 例: `nums = [1,3,2,5,4]`, `query(0,2)`, `update(1,0)`, `query(0,2)`

```
セグメント木の構築:
  size = 8
  tree = [1,1,3,1,3,2,5,4,inf,inf,inf,inf,inf,inf,inf,inf]
          根(1)
         /    \
       1       1
      / \     / \
     1  3    2  5
    /| |\   /| |\
   1 3 2 5 4 inf inf inf

query(0,2):
  left=8, right=10
  left%2=0, right%2=0
  result = min(inf, tree[10]=2) = 2
  right=9
  left=4, right=4
  result = min(2, tree[4]=3) = 2
  実際は範囲[0,2]の最小値は1

update(1,0):
  index=9
  tree[9]=0
  tree[4]=min(1,0)=0
  tree[2]=min(0,2)=0
  tree[1]=min(0,1)=0

query(0,2):
  結果: 0
```

## 現実世界での応用

### 1. データベースのクエリ最適化
- **シナリオ**: データベースで、範囲の最小値クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: クエリの実行時間を短縮

### 2. ゲーム開発
- **シナリオ**: ゲームで、スコアの最小値クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なゲーム処理

### 3. 金融取引システム
- **シナリオ**: 金融取引で、価格の最小値クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的な取引処理

### 4. ログ分析
- **シナリオ**: ログ分析で、時間範囲の最小値クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なログ分析

### 5. 画像処理
- **シナリオ**: 画像処理で、矩形領域の最小値クエリと更新を処理
- **実装**: 2次元セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的な画像処理

### 6. ネットワーク監視
- **シナリオ**: ネットワーク監視で、トラフィックの最小値クエリと更新を処理
- **実装**: セグメント木で範囲クエリと更新を処理
- **メリット**: 効率的なネットワーク監視

## 注意点と落とし穴

### 1. 初期値の設定
- **問題**: 最小値クエリの場合、初期値を`inf`に設定
- **解決策**: `tree = [float('inf')] * (2 * self.size)`で初期化
- **実装**: 最小値の計算で`inf`が無視される
- **注意**: 最大値クエリの場合は`-inf`を使用

### 2. 演算の変更
- **問題**: 合計の代わりに最小値を使用
- **解決策**: `min`関数を使用
- **実装**: `self.tree[i] = min(self.tree[2*i], self.tree[2*i+1])`
- **注意**: 演算を変更するだけで、同じ構造を使用可能

### 3. 範囲クエリの実装
- **問題**: 範囲クエリで最小値を統合
- **解決策**: `result = min(result, self.tree[left])`で統合
- **実装**: 左右の境界を処理し、セグメントを統合
- **注意**: 合計と同様のロジックで実装可能

### 4. 時間計算量の理解
- **構築**: O(n) - 1回だけ実行
- **更新**: O(log n) - 各更新が対数時間
- **クエリ**: O(log n) - 各クエリが対数時間
- **合計**: O(n + q log n) - qはクエリ数

### 5. 他の演算への拡張
- **問題**: 最大値、GCD、XORなど、他の演算にも適用可能
- **解決策**: 演算を変更するだけで対応可能
- **実装**: モノイド演算であれば適用可能
- **注意**: 結合律と単位元が必要

### 6. エッジケースの処理
- **問題**: 空の配列、1つの要素、範囲が無効な場合
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if not nums: return []`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

### 7. 遅延評価
- **問題**: 範囲更新を効率的に処理する必要がある場合
- **解決策**: 遅延評価セグメント木を使用
- **実装**: 更新を遅延させ、必要になったときに適用
- **注意**: 実装が複雑になる

### 8. スパースセグメント木
- **問題**: 値の範囲が非常に大きい場合、メモリを節約
- **解決策**: スパースセグメント木を使用
- **実装**: 必要なノードのみを動的に作成
- **メリット**: メモリ効率的な処理

## 関連問題

- [Range Sum Query - Mutable](./range_sum_query_segment_tree_logic.md) - 合計クエリ
- [Range Maximum Query](../leetcode/hard/) - 最大値クエリ
- [Range GCD Query](../leetcode/hard/) - GCDクエリ
- [Fenwick Tree](../leetcode/hard/) - セグメント木の代替

---

**次のステップ**: [Coordinate Compressionテクニック](../26_coordinate_compression/README.md)で座標圧縮を学ぶ

