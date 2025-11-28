# Next Greater Element - ロジック解説

## 問題概要

配列`nums1`と`nums2`が与えられたとき、`nums1`の各要素について、`nums2`での次の大きい要素を返す。

**例**:
```
Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
```

## ロジックの核心

### なぜモノトニックスタックが有効か？

**全探索（O(n×m)）**:
- 各要素について、次の大きい要素を線形探索
- 時間計算量: O(n×m) - 非効率

**モノトニックスタックを使う理由**:
- **単調性の保持**: スタックで単調減少を保持
- **時間計算量**: O(n + m) - 線形時間
- **空間計算量**: O(m) - スタックとハッシュマップ

### アルゴリズムのステップ

```
function nextGreaterElement(nums1, nums2):
    stack = []
    next_greater = {}
    
    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    
    return [next_greater.get(num, -1) for num in nums1]
```

## 現実世界での応用

### 1. データ分析
- **シナリオ**: データ分析で、次の大きい値を検索
- **実装**: モノトニックスタックで次の大きい値を検索
- **メリット**: 効率的なデータ分析

### 2. スケジューリング
- **シナリオ**: スケジューリングで、次の大きい値を検索
- **実装**: モノトニックスタックで次の大きい値を検索
- **メリット**: 効率的なスケジューリング

## 注意点と落とし穴

### 1. モノトニックスタック
- **問題**: スタックで単調減少を保持する必要がある
- **解決策**: 大きい要素が来たら、スタックから要素を削除
- **注意**: スタックの管理が重要

## 関連問題

- [Daily Temperatures](./daily_temperatures_logic.md) - モノトニックスタック
- [Largest Rectangle in Histogram](./largest_rectangle_histogram_logic.md) - 最大矩形

---

**次のステップ**: [メインREADME](../README.md)で全体を確認

