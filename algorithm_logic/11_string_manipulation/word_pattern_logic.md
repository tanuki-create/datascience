# Word Pattern - ロジック解説

## 問題概要

パターン`pattern`と文字列`s`が与えられたとき、`s`が`pattern`に従っているか判定する。

**例**:
```
Input: pattern = "abba", s = "dog cat cat dog"
Output: true
```

## ロジックの核心

### なぜハッシュマップが有効か？

**全探索（非効率）**:
- 全ての可能なマッピングを試す
- 時間計算量: 指数時間 - 非効率

**ハッシュマップを使う理由**:
- **双方向マッピング**: パターン→単語と単語→パターンの両方を管理
- **時間計算量**: O(n) - 線形時間
- **空間計算量**: O(n) - ハッシュマップ

### アルゴリズムのステップ

```
function wordPattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    
    pattern_to_word = {}
    word_to_pattern = {}
    
    for i in range(len(pattern)):
        p, w = pattern[i], words[i]
        
        if p in pattern_to_word:
            if pattern_to_word[p] != w:
                return False
        else:
            pattern_to_word[p] = w
        
        if w in word_to_pattern:
            if word_to_pattern[w] != p:
                return False
        else:
            word_to_pattern[w] = p
    
    return True
```

## 現実世界での応用

### 1. テキストエディタのマクロ
- **シナリオ**: テキストエディタで、パターンに基づいてテキストを変換
- **実装**: パターンマッチングでテキストを変換
- **メリット**: 効率的なテキスト処理

### 2. 自然言語処理
- **シナリオ**: NLPで、文の構造をパターンで表現
- **実装**: パターンマッチングで文の構造を解析
- **メリット**: 効率的な自然言語処理

### 3. データ検証
- **シナリオ**: データ検証で、データが特定のパターンに従っているかチェック
- **実装**: パターンマッチングでデータを検証
- **メリット**: 効率的なデータ検証

## 注意点と落とし穴

### 1. 双方向マッピング
- **問題**: パターン→単語と単語→パターンの両方を管理する必要がある
- **解決策**: 2つのハッシュマップを使用
- **注意**: 片方向のみでは不十分

### 2. 長さの一致
- **問題**: パターンと単語の数が一致する必要がある
- **解決策**: 最初に長さをチェック
- **注意**: 長さが異なる場合はFalse

## 関連問題

- [Isomorphic Strings](../leetcode/easy/) - 同型文字列
- [Longest Common Prefix](./longest_common_prefix_logic.md) - 共通プレフィックス

---

**次のステップ**: [Valid Anagram](./valid_anagram_logic.md)でアナグラムを学ぶ

