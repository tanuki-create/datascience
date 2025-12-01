# Z-algorithm - ロジック解説

## 問題概要

Z-algorithmは、文字列`S`に対して、**各位置iから始まる部分文字列がSの接頭辞と最大で何文字一致するか**をO(n)で計算するアルゴリズムです。Z配列（Z-array）を構築し、パターンマッチングや文字列検索に使用されます。KMPアルゴリズムの代替として、より直感的な実装が可能です。

**例**:
```
文字列: "aabxaabxcaabxaabxay"
Z配列:  [X, 1, 0, 0, 4, 1, 0, 0, 0, 6, 1, 0, 0, 0, 4, 1, 0, 0, 0, 0]
         ↑
       Z[0]は未定義（通常は文字列の長さ）
```

## ロジックの核心

### なぜZ-algorithmが有効か？

**素朴なアプローチ（O(n²)）**:
- 各位置で接頭辞と比較
- 時間計算量: O(n²) - 非効率

**Z-algorithmを使う理由**:
- **Z-boxの活用**: 既に計算した情報を再利用
- **時間計算量**: O(n) - 線形時間
- **空間計算量**: O(n) - Z配列

### アルゴリズムのステップ

#### Z配列の構築

```
function buildZArray(s):
    n = len(s)
    z = [0] * n
    left = 0
    right = 0
    
    for i in range(1, n):
        if i > right:
            // Z-boxの外側
            left = right = i
            while right < n and s[right - left] == s[right]:
                right += 1
            z[i] = right - left
            right -= 1
        else:
            // Z-boxの内側
            k = i - left
            if z[k] < right - i + 1:
                // 既存のZ-box内で完結
                z[i] = z[k]
            else:
                // Z-boxを拡張
                left = i
                while right < n and s[right - left] == s[right]:
                    right += 1
                z[i] = right - left
                right -= 1
    
    return z
```

### 具体例でのトレース

#### 例: 文字列 "aabxaabxcaabxaabxay"

**ステップ1: i=1**
```
s = "aabxaabxcaabxaabxay"
i=1, left=0, right=0

i > right (1 > 0) → Z-boxの外側
left = right = 1
比較: s[0]='a' vs s[1]='a' → 一致
right = 2
比較: s[1]='a' vs s[2]='b' → 不一致
z[1] = 2 - 1 = 1
right = 1

Z配列: [X, 1, ...]
```

**ステップ2: i=2**
```
i=2, left=1, right=1

i > right (2 > 1) → Z-boxの外側
left = right = 2
比較: s[0]='a' vs s[2]='b' → 不一致
z[2] = 0
right = 2

Z配列: [X, 1, 0, ...]
```

**ステップ3: i=4**
```
i=4, left=2, right=2

i > right (4 > 2) → Z-boxの外側
left = right = 4
比較: s[0]='a' vs s[4]='a' → 一致
right = 5
比較: s[1]='a' vs s[5]='a' → 一致
right = 6
比較: s[2]='b' vs s[6]='b' → 一致
right = 7
比較: s[3]='x' vs s[7]='x' → 一致
right = 8
比較: s[4]='a' vs s[8]='c' → 不一致
z[4] = 8 - 4 = 4
right = 7

Z配列: [X, 1, 0, 0, 4, ...]
```

**ステップ4: i=5**
```
i=5, left=4, right=7

i <= right (5 <= 7) → Z-boxの内側
k = 5 - 4 = 1
z[1] = 1
right - i + 1 = 7 - 5 + 1 = 3
z[1] < 3 (1 < 3) → 既存のZ-box内で完結
z[5] = z[1] = 1

Z配列: [X, 1, 0, 0, 4, 1, ...]
```

**ステップ5: i=9**
```
i=9, left=4, right=7

i > right (9 > 7) → Z-boxの外側
left = right = 9
比較: s[0]='a' vs s[9]='a' → 一致
right = 10
比較: s[1]='a' vs s[10]='a' → 一致
right = 11
比較: s[2]='b' vs s[11]='b' → 一致
right = 12
比較: s[3]='x' vs s[12]='x' → 一致
right = 13
比較: s[4]='a' vs s[13]='a' → 一致
right = 14
比較: s[5]='a' vs s[14]='b' → 不一致
z[9] = 14 - 9 = 5
right = 13

Z配列: [X, 1, 0, 0, 4, 1, 0, 0, 0, 5, ...]
```

#### パターンマッチングへの応用

**問題**: テキスト内でパターンを検索

```
テキスト: "aabxaabxcaabxaabxay"
パターン: "aabx"

結合文字列: "aabx$" + "aabxaabxcaabxaabxay"
          = "aabx$aabxaabxcaabxaabxay"

Z配列を構築し、Z[i] == len(pattern)の位置を探す
```

## 現実世界での応用

### 1. パターンマッチング
- **シナリオ**: テキスト内でパターンを検索
- **実装**: Z-algorithmでパターンマッチング
- **メリット**: O(n+m)でパターンを検索

### 2. 文字列の周期検出
- **シナリオ**: 文字列の周期を検出
- **実装**: Z配列で周期を検出
- **メリット**: 効率的な周期検出

### 3. 最長回文部分文字列
- **シナリオ**: 文字列の最長回文部分文字列を検出
- **実装**: Z-algorithmとManacherアルゴリズムの組み合わせ
- **メリット**: 効率的な回文検出

### 4. 文字列圧縮
- **シナリオ**: 文字列の繰り返しパターンを検出
- **実装**: Z配列で繰り返しパターンを検出
- **メリット**: 効率的な文字列圧縮

### 5. DNA配列解析
- **シナリオ**: DNA配列の繰り返しパターンを検出
- **実装**: Z-algorithmでパターンを検出
- **メリット**: 効率的なDNA配列解析

### 6. テキストエディタの検索
- **シナリオ**: テキストエディタで高速な検索
- **実装**: Z-algorithmでパターンを検索
- **メリット**: 高速なテキスト検索

## 注意点と落とし穴

### 1. Z-boxの管理
- **問題**: Z-boxの範囲（left, right）を正確に管理
- **解決策**: leftとrightを適切に更新
- **実装**: Z-boxの境界を正確に追跡
- **注意**: 範囲を間違えると結果が間違う

### 2. Z-boxの内側の処理
- **問題**: Z-boxの内側では既存の情報を再利用
- **解決策**: `k = i - left`で対応する位置を計算
- **実装**: `z[i] = z[k]`で値をコピー
- **注意**: 範囲外の場合は拡張が必要

### 3. Z-boxの拡張
- **問題**: Z-boxを拡張する必要がある場合
- **解決策**: 右端から文字を比較して拡張
- **実装**: `while right < n and s[right - left] == s[right]`
- **注意**: 範囲外アクセスに注意

### 4. インデックスの計算
- **問題**: Z-box内の対応する位置の計算
- **解決策**: `k = i - left`で計算
- **実装**: 相対位置を計算
- **注意**: インデックスの計算を間違えると結果が間違う

### 5. パターンマッチングへの応用
- **問題**: パターンマッチングでは区切り文字が必要
- **解決策**: パターンとテキストの間に特殊文字を挿入
- **実装**: `combined = pattern + "$" + text`
- **注意**: 区切り文字はテキストやパターンに出現しない文字を使用

### 6. 時間計算量の理解
- **問題**: 各文字は最大2回しか比較されない
- **解決策**: Z-boxの活用で比較回数を削減
- **実装**: 既存の情報を再利用
- **注意**: 最悪時間計算量はO(n)

### 7. KMPとの比較
- **問題**: Z-algorithmとKMPのどちらを使うか
- **解決策**: 
  - Z-algorithm: より直感的、実装が簡単
  - KMP: より一般的、失敗関数の概念が明確
- **実装**: 問題の要件に応じて選択
- **注意**: 両方のアルゴリズムを理解することが重要

## 関連問題

- [KMP Algorithm](./kmp_algorithm_logic.md) - パターンマッチングの別アプローチ
- [Rabin-Karp](./rabin_karp_logic.md) - ローリングハッシュを使った検索
- [Manacher's Algorithm](./manacher_algorithm_logic.md) - 回文検出

---

**次のステップ**: [KMP Algorithm](./kmp_algorithm_logic.md)でパターンマッチングの別アプローチを学ぶ

