# Largest Rectangle in Histogram - ロジック解説

## 問題概要

ヒストグラムの高さの配列が与えられたとき、最大の矩形の面積を返す。

**例**:
```
Input: heights = [2,1,5,6,2,3]
Output: 10
説明: 高さ5と6の矩形で面積10
```

## ロジックの核心

### なぜモノトニックスタックが有効か？

**全探索（O(n²)）**:
- 全ての可能な矩形を試す
- 時間計算量: O(n²) - 非効率

**モノトニックスタックを使う理由**:
- **単調性の保持**: スタックで単調増加を保持
- **時間計算量**: O(n) - 各要素を1回ずつ処理
- **空間計算量**: O(n) - スタック

### アルゴリズムのステップ

```
function largestRectangleArea(heights):
    stack = []
    max_area = 0
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    while stack:
        height = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)
    
    return max_area
```

## 現実世界での応用

### 1. 画像処理
- **シナリオ**: 画像処理で、最大の矩形領域を検出
- **実装**: モノトニックスタックで最大矩形を検出
- **メリット**: 効率的な画像処理

### 2. データ分析
- **シナリオ**: データ分析で、最大のデータ領域を検出
- **実装**: モノトニックスタックで最大領域を検出
- **メリット**: 効率的なデータ分析

## 注意点と落とし穴

### 1. モノトニックスタック
- **問題**: スタックで単調増加を保持する必要がある
- **解決策**: 減少する要素が来たら、スタックから要素を削除
- **注意**: スタックの管理が重要

## 関連問題

- [Daily Temperatures](./daily_temperatures_logic.md) - モノトニックスタック
- [Trapping Rain Water](./trapping_rain_water_logic.md) - 水のトラップ

---

**次のステップ**: [Trapping Rain Water](./trapping_rain_water_logic.md)で水のトラップを学ぶ

