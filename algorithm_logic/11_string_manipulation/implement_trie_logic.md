# Implement Trie - ロジック解説

## 問題概要

Trie（トライ木）を実装する。`insert(word)`, `search(word)`, `startsWith(prefix)`を実装する。

**例**:
```
trie = Trie()
trie.insert("apple")
trie.search("apple") → true
trie.search("app") → false
trie.startsWith("app") → true
```

## ロジックの核心

### なぜTrieが有効か？

**ハッシュマップ（O(1)検索）**:
- 単語の検索はO(1)だが、プレフィックス検索が非効率
- 時間計算量: プレフィックス検索でO(n×m)

**Trieを使う理由**:
- **プレフィックス検索**: プレフィックス検索を効率的に処理
- **時間計算量**: O(m) - mは単語の長さ
- **空間計算量**: O(ALPHABET_SIZE × N × M) - Nは単語数、Mは平均長

### アルゴリズムのステップ

```
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

## 現実世界での応用

### 1. 検索エンジン
- **シナリオ**: 検索エンジンで、自動補完を実装
- **実装**: Trieでプレフィックス検索を実装
- **メリット**: 効率的な自動補完

### 2. スペルチェッカー
- **シナリオ**: スペルチェッカーで、単語の検索を実装
- **実装**: Trieで単語の検索を実装
- **メリット**: 効率的なスペルチェック

### 3. IPルーティング
- **シナリオ**: IPルーティングで、最長プレフィックスマッチを実装
- **実装**: Trieで最長プレフィックスマッチを実装
- **メリット**: 効率的なルーティング

## 注意点と落とし穴

### 1. ノードの構造
- **問題**: 各ノードで子ノードと終端フラグを管理
- **解決策**: `children`辞書と`is_end`フラグを使用
- **注意**: ノードの構造が重要

### 2. プレフィックスと完全一致
- **問題**: `search`と`startsWith`の違いを理解
- **解決策**: `search`は`is_end`をチェック、`startsWith`はチェックしない
- **注意**: 実装の違いが重要

## 関連問題

- [Word Search II](../15_trie/word_search_ii_logic.md) - Trieの応用
- [Longest Word in Dictionary](../15_trie/longest_word_dictionary_logic.md) - Trieの応用

---

**次のステップ**: [Mathテクニック](../13_mathematical/README.md)で数学的問題を学ぶ

