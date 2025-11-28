# Count Primes - ロジック解説

## 問題概要

整数`n`が与えられたとき、n未満の素数の数を返す。

**制約**:
- `0 <= n <= 5 * 10^6`

**例**:
```
Input: n = 10
Output: 4
説明: 2, 3, 5, 7
```

## ロジックの核心

### なぜエラトステネスの篩が有効か？

**素朴なアプローチ（O(n√n)）**:
- 各数について素数判定
- 時間計算量: O(n√n) - 非効率

**エラトステネスの篩を使う理由**:
- **合成数の除去**: 各素数の倍数を順次除去
- **時間計算量**: O(n log log n) - ほぼ線形時間
- **空間計算量**: O(n) - ブール配列

### アルゴリズムのステップ

```
function countPrimes(n):
    if n < 2:
        return 0
    
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n, i):
                is_prime[j] = False
    
    return sum(is_prime)
```

## 現実世界での応用

### 1. 暗号化システム
- **シナリオ**: 暗号化システムで、大きな素数を生成
- **実装**: エラトステネスの篩で素数を列挙
- **メリット**: セキュアな暗号化

### 2. データ分析
- **シナリオ**: データ分析で、素数のパターンを分析
- **実装**: エラトステネスの篩で素数を列挙
- **メリット**: 効率的なデータ分析

## 注意点と落とし穴

### 1. √nまでの走査
- **問題**: なぜ√nまで走査すれば十分か？
- **解決策**: √nより大きい数の倍数は既に篩い落とされている
- **注意**: 効率化のポイント

## 関連問題

- [Sieve of Eratosthenes](../24_advanced_math/sieve_of_eratosthenes_logic.md) - 素数の列挙
- [GCD/LCM](../24_advanced_math/gcd_lcm_logic.md) - 最大公約数と最小公倍数

---

**次のステップ**: [Happy Number](./happy_number_logic.md)でハッピー数を学ぶ

