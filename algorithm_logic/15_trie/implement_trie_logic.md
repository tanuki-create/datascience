# Implement Trie - ロジック解説

## 問題概要

トライ木（Trie）を実装する。以下の操作をサポートする必要がある：
- `insert(word)`: 単語をトライ木に挿入
- `search(word)`: 単語が存在するか検索
- `startsWith(prefix)`: プレフィックスで始まる単語が存在するか検索

**制約**:
- `1 <= word.length, prefix.length <= 2000`
- `word`と`prefix`は小文字の英字のみ

**例**:
```
trie = Trie()
trie.insert("apple")
trie.search("apple")   # True
trie.search("app")     # False
trie.startsWith("app") # True
trie.insert("app")
trie.search("app")     # True
```

## ロジックの核心

### なぜトライ木が有効か？

**ハッシュテーブル（比較）**:
- 単語の検索: O(1)平均、O(n)最悪
- プレフィックス検索: O(n) - 全ての単語をチェックする必要がある

**トライ木を使う理由**:
- **プレフィックス検索が高速**: O(m) - mはプレフィックスの長さ
- **共通プレフィックスの共有**: メモリを効率的に使用
- **時間計算量**: 検索・挿入がO(m)で一定

### 思考プロセス

1. **ノードの設計**: 
   - 子ノードへのポインタ（辞書または配列）
   - 終端フラグ（単語の終わりを示す）

2. **挿入操作**:
   - 文字ごとにノードを辿る
   - ノードが存在しない場合は作成
   - 最後の文字で終端フラグを設定

3. **検索操作**:
   - 文字ごとにノードを辿る
   - 全ての文字が存在し、最後のノードが終端フラグを持つか確認

4. **プレフィックス検索**:
   - 文字ごとにノードを辿る
   - 全ての文字が存在すればTrue

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

## 具体例でのトレース

### 例: `insert("apple")`, `insert("app")`, `search("app")`

```
初期状態: root = TrieNode()

insert("apple"):
  root → 'a' → TrieNode
    → 'p' → TrieNode
      → 'p' → TrieNode
        → 'l' → TrieNode
          → 'e' → TrieNode (is_end=True)

insert("app"):
  root → 'a' → TrieNode (既存)
    → 'p' → TrieNode (既存)
      → 'p' → TrieNode (既存、is_end=Trueを設定)

search("app"):
  root → 'a' → TrieNode
    → 'p' → TrieNode
      → 'p' → TrieNode (is_end=True) ✓ True

search("ap"):
  root → 'a' → TrieNode
    → 'p' → TrieNode (is_end=False) ✗ False

startsWith("ap"):
  root → 'a' → TrieNode
    → 'p' → TrieNode ✓ True
```

### 可視化

```
トライ木の構造:

        root
         |
         a
         |
         p
        / \
       p   p
       |   |
       l   (is_end=True for "app")
       |
       e
       |
    (is_end=True for "apple")
```

## 現実世界での応用

### 1. 検索エンジンの自動補完
- **シナリオ**: ユーザーが入力中に、候補を表示
- **実装**: 検索履歴をトライ木に保存し、プレフィックス検索で候補を取得
- **例**: Google検索の自動補完機能
- **メリット**: ユーザーの入力効率を向上

### 2. IDEのコード補完
- **シナリオ**: プログラマーがコードを入力中に、関数名や変数名を補完
- **実装**: コードベースの識別子をトライ木に保存し、プレフィックス検索
- **例**: Visual Studio CodeのIntelliSense
- **メリット**: 開発効率を向上

### 3. 電話帳アプリケーション
- **シナリオ**: 連絡先の名前を検索
- **実装**: 連絡先をトライ木に保存し、名前のプレフィックスで検索
- **例**: iPhoneの連絡先検索
- **メリット**: 高速な連絡先検索

### 4. スペルチェッカー
- **シナリオ**: 入力中の単語のスペルをチェック
- **実装**: 辞書をトライ木に保存し、単語の存在を確認
- **例**: Microsoft Wordのスペルチェック
- **メリット**: リアルタイムでスペルエラーを検出

### 5. IPルーティング
- **シナリオ**: IPアドレスに基づいて最適な経路を選択
- **実装**: IPアドレスをトライ木に保存し、最長の一致するプレフィックスを検索
- **例**: ルーターのルーティングテーブル
- **メリット**: 効率的なパケットルーティング

### 6. データベースのインデックス
- **シナリオ**: 全文検索エンジンで、キーワードの検索
- **実装**: 文書内の単語をトライ木に保存し、高速に検索
- **例**: Elasticsearchのインデックス
- **メリット**: 大量のデータから高速に検索

## 注意点と落とし穴

### 1. ノードの初期化
- **問題**: 各ノードを正しく初期化する必要がある
- **解決策**: `__init__`で`children = {}`と`is_end = False`を設定
- **注意**: 終端フラグを忘れると、部分文字列も単語として認識される

### 2. 子ノードの存在チェック
- **問題**: ノードが存在しない場合の処理
- **解決策**: `if char not in node.children:`でチェック
- **注意**: 存在しないノードにアクセスするとエラーが発生

### 3. 終端フラグの設定
- **問題**: 単語の終わりを正確にマークする必要がある
- **解決策**: 最後の文字を処理した後、`node.is_end = True`を設定
- **注意**: 終端フラグを設定しないと、`search`が正しく動作しない

### 4. プレフィックス検索と完全一致検索の違い
- **問題**: `search`と`startsWith`の違いを理解する必要がある
- **解決策**: 
  - `search`: 終端フラグもチェック（完全一致）
  - `startsWith`: 終端フラグはチェックしない（プレフィックスのみ）
- **注意**: 混同すると、誤った結果が返される

### 5. メモリ使用量
- **問題**: 文字セットが大きい場合、メモリを大量に消費する可能性
- **解決策**: 
  - 辞書を使う場合: 実際に使用される文字のみを保存（推奨）
  - 配列を使う場合: 固定サイズだが、未使用の領域も確保
- **トレードオフ**: 時間効率 vs 空間効率

### 6. 削除操作の実装（拡張）
- **問題**: 単語を削除する際、他の単語に影響を与えないようにする必要がある
- **解決策**: 
  - 終端フラグをfalseにする
  - 子ノードがなく、終端フラグもfalseの場合のみノードを削除
- **注意**: 再帰的に親ノードも削除する必要がある場合がある

### 7. 大文字小文字の扱い
- **問題**: 大文字小文字を区別するかどうか
- **解決策**: 問題の要件に応じて、小文字に統一するか、区別するか決定
- **実装**: 挿入・検索時に`.lower()`で統一

### 8. 時間計算量の理解
- **平均**: O(m) - mは文字列の長さ
- **最悪**: O(m) - 常に線形時間
- **空間**: O(ALPHABET_SIZE × N × M) - Nは単語数、Mは平均長
- **注意**: 文字列の数には依存せず、文字列の長さにのみ依存

## 関連問題

- [Word Search II](./word_search_ii_logic.md) - トライ木 + バックトラッキング
- [Longest Word in Dictionary](./longest_word_dictionary_logic.md) - トライ木の応用
- [Add and Search Word](../leetcode/medium/) - ワイルドカード検索
- [Prefix and Suffix Search](../leetcode/hard/) - プレフィックスとサフィックスの検索

---

**次のステップ**: [Word Search II](./word_search_ii_logic.md)でバックトラッキングと組み合わせた使用法を学ぶ

