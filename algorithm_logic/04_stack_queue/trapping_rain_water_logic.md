# Trapping Rain Water - ロジック解説

## 問題概要

高さの配列が与えられたとき、トラップできる水の量を返す。

**例**:
```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

## ロジックの核心

### なぜ二ポインタが有効か？

**全探索（O(n²)）**:
- 全ての位置で水の量を計算
- 時間計算量: O(n²) - 非効率

**二ポインタを使う理由**:
- **左右からの走査**: 左右から走査して水の量を計算
- **時間計算量**: O(n) - 線形時間
- **空間計算量**: O(1) - 定数空間

### アルゴリズムのステップ

```
function trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

## 現実世界での応用

### 1. 水資源管理
- **シナリオ**: 水資源管理で、水の貯水量を計算
- **実装**: トラップできる水の量を計算
- **メリット**: 効率的な水資源管理

### 2. 地形分析
- **シナリオ**: 地形分析で、水の貯水量を計算
- **実装**: トラップできる水の量を計算
- **メリット**: 効率的な地形分析

## 注意点と落とし穴

### 1. 二ポインタの管理
- **問題**: 左右のポインタを正確に管理する必要がある
- **解決策**: 低い方のポインタを移動
- **注意**: ポインタの管理が重要

## 関連問題

- [Container With Most Water](../02_two_pointers/container_with_most_water_logic.md) - 水のコンテナ
- [Largest Rectangle in Histogram](./largest_rectangle_histogram_logic.md) - 最大矩形

---

**次のステップ**: [Next Greater Element](./next_greater_element_logic.md)で次の大きい要素を学ぶ

