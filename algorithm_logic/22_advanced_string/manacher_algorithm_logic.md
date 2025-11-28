# Manacher's Algorithm - ロジック解説

## 問題概要

文字列`s`が与えられたとき、最長のパリンドローム部分文字列の長さを返す。

**制約**:
- `1 <= s.length <= 1000`

**例**:
```
Input: s = "babad"
Output: 3
説明: "bab"または"aba"が最長のパリンドローム
```

## ロジックの核心

### なぜManacherが有効か？

**全探索（O(n³)）**:
- 全ての部分文字列をチェック
- 時間計算量: O(n³) - 非効率

**Manacherを使う理由**:
- **ミラーリング**: 既に計算したパリンドロームの情報を再利用
- **時間計算量**: O(n) - 線形時間
- **空間計算量**: O(n) - パリンドロームの半径を保存

### 思考プロセス

1. **文字列の変換**: 偶数長のパリンドロームも扱えるように、文字の間に特殊文字を挿入
2. **中心の探索**: 各位置を中心としてパリンドロームを拡張
3. **ミラーリング**: 既に計算したパリンドロームの情報を再利用

### アルゴリズムのステップ

```
function longestPalindrome(s):
    // 文字列を変換: "abc" -> "#a#b#c#"
    transformed = "#" + "#".join(s) + "#"
    n = len(transformed)
    radius = [0] * n
    
    center = 0
    right = 0
    max_len = 0
    
    for i in range(n):
        // ミラーリング: 既に計算したパリンドロームの情報を再利用
        if i < right:
            mirror = 2 * center - i
            radius[i] = min(right - i, radius[mirror])
        
        // パリンドロームを拡張
        left_bound = i - radius[i] - 1
        right_bound = i + radius[i] + 1
        
        while left_bound >= 0 and right_bound < n and transformed[left_bound] == transformed[right_bound]:
            radius[i] += 1
            left_bound -= 1
            right_bound += 1
        
        // 右端を更新
        if i + radius[i] > right:
            center = i
            right = i + radius[i]
        
        max_len = max(max_len, radius[i])
    
    return max_len
```

## 具体例でのトレース

### 例: `s = "babad"`

```
変換後: "#b#a#b#a#d#"

i=0: center=0, right=0
  radius[0] = 0

i=1: center=0, right=0
  radius[1] = 0
  拡張: "#" == "#" → radius[1] = 1
  center=1, right=2

i=2: center=1, right=2
  mirror = 2*1-2 = 0, radius[0]=0
  radius[2] = min(2-2, 0) = 0
  拡張: "b" == "b" → radius[2] = 1
  center=2, right=3

i=3: center=2, right=3
  mirror = 2*2-3 = 1, radius[1]=1
  radius[3] = min(3-3, 1) = 0
  拡張: "a" == "a" → radius[3] = 1
  center=3, right=4

i=4: center=3, right=4
  mirror = 2*3-4 = 2, radius[2]=1
  radius[4] = min(4-4, 1) = 0
  拡張: "b" == "b" → radius[4] = 1
  center=4, right=5

結果: max_len = 3
```

## 現実世界での応用

### 1. テキスト処理
- **シナリオ**: テキストエディタで、パリンドロームを検出
- **実装**: Manacherアルゴリズムで効率的に検出
- **メリット**: 高速なテキスト処理

### 2. DNA配列解析
- **シナリオ**: バイオインフォマティクスで、パリンドローム配列を検出
- **実装**: Manacherアルゴリズムで効率的に検出
- **メリット**: 効率的なDNA配列解析

### 3. データ圧縮
- **シナリオ**: データ圧縮アルゴリズムで、パリンドロームパターンを検出
- **実装**: Manacherアルゴリズムで効率的に検出
- **メリット**: 効率的なデータ圧縮

### 4. 文字列の解析
- **シナリオ**: コンパイラで、文字列リテラルの解析
- **実装**: Manacherアルゴリズムで効率的に解析
- **メリット**: 高速な文字列解析

### 5. ゲーム開発
- **シナリオ**: ゲームで、パリンドロームパターンを検出
- **実装**: Manacherアルゴリズムで効率的に検出
- **メリット**: 効率的なゲーム処理

### 6. セキュリティ
- **シナリオ**: セキュリティで、パリンドロームパターンを検出
- **実装**: Manacherアルゴリズムで効率的に検出
- **メリット**: 効率的なセキュリティ分析

## 注意点と落とし穴

### 1. 文字列の変換
- **問題**: 偶数長のパリンドロームも扱えるように、文字の間に特殊文字を挿入
- **解決策**: `"#" + "#".join(s) + "#"`で変換
- **実装**: 特殊文字を挿入することで、偶数長も扱える
- **注意**: 変換後の文字列の長さは2n+1になる

### 2. ミラーリングの理解
- **問題**: 既に計算したパリンドロームの情報を再利用
- **解決策**: `mirror = 2 * center - i`でミラー位置を計算
- **実装**: `radius[i] = min(right - i, radius[mirror])`で再利用
- **注意**: ミラーリングの理解が重要

### 3. パリンドロームの拡張
- **問題**: パリンドロームを左右に拡張
- **解決策**: `while`ループで拡張
- **実装**: 左右の文字が一致する限り拡張
- **注意**: 境界チェックが重要

### 4. 時間計算量の理解
- **平均**: O(n) - 各文字を1回ずつ処理
- **最悪**: O(n) - 常に線形時間
- **空間**: O(n) - 半径の配列
- **メリット**: O(n²)からO(n)に改善

### 5. 中心と右端の更新
- **問題**: パリンドロームの中心と右端を適切に更新
- **解決策**: `if i + radius[i] > right:`で更新
- **実装**: 右端が拡張された場合、中心と右端を更新
- **注意**: 更新を忘れると、ミラーリングが正しく動作しない

### 6. 最長パリンドロームの追跡
- **問題**: 最長のパリンドロームの長さを追跡
- **解決策**: `max_len = max(max_len, radius[i])`で更新
- **実装**: 各位置で最大値を更新
- **注意**: 変換後の文字列では、実際の長さは`radius[i]`になる

### 7. 実際のパリンドロームの取得
- **問題**: 最長のパリンドロームの文字列を取得する必要がある場合
- **解決策**: 最長の位置を記録し、変換後の文字列から抽出
- **実装**: `max_pos`を記録し、`transformed[max_pos-radius[max_pos]:max_pos+radius[max_pos]+1]`から抽出
- **注意**: 特殊文字を除いて、実際の文字列を取得

### 8. エッジケースの処理
- **問題**: 空の文字列、1文字、全て同じ文字の場合
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if not s: return ""`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

## 関連問題

- [Longest Palindromic Substring](../leetcode/medium/) - 最長パリンドローム部分文字列
- [Palindromic Substrings](../leetcode/medium/) - パリンドロームの数
- [Shortest Palindrome](../leetcode/hard/) - KMPの応用
- [Valid Palindrome](../02_two_pointers/valid_palindrome_logic.md) - パリンドロームの検証

---

**次のステップ**: [Advanced Graphテクニック](../23_advanced_graph/README.md)で高度なグラフアルゴリズムを学ぶ

