# LRU Cache - ロジック解説

## 問題概要

LRU (Least Recently Used) Cacheを実装する。`get(key)`と`put(key, value)`をO(1)時間で実行する。

**制約**:
- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`
- `0 <= value <= 10^5`

**例**:
```
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1) → 1
cache.put(3, 3) → 2が削除される（LRU）
cache.get(2) → -1（削除済み）
```

## ロジックの核心

### なぜ双方向リンクリスト + ハッシュマップが有効か？

**配列（O(n)）**:
- 各操作で配列を走査してLRUを探す
- 時間計算量: O(n) - 非効率

**双方向リンクリスト + ハッシュマップを使う理由**:
- **O(1)アクセス**: ハッシュマップでO(1)でノードにアクセス
- **O(1)削除・挿入**: 双方向リンクリストでO(1)で削除・挿入
- **時間計算量**: O(1) - 各操作が定数時間

### 思考プロセス

1. **ハッシュマップ**: キーからノードへのO(1)アクセス
2. **双方向リンクリスト**: アクセス順序を管理（先頭がMRU、末尾がLRU）
3. **操作**: 
   - get: ノードを先頭に移動
   - put: 既存なら更新して先頭に移動、新規なら先頭に追加し、容量超過時は末尾を削除

### アルゴリズムのステップ

```
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  // キーからノードへのマッピング
        self.head = Node(0, 0)  // ダミーヘッド
        self.tail = Node(0, 0)  // ダミーテール
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.value
    
    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                self._remove_tail()
            
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
    
    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)
    
    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _remove_tail(self):
        lru = self.tail.prev
        self._remove_node(lru)
        del self.cache[lru.key]
```

## 具体例でのトレース

### 例: `capacity = 2`, `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`, `get(2)`

```
初期状態:
  head <-> tail
  cache = {}

put(1,1):
  head <-> (1,1) <-> tail
  cache = {1: node1}

put(2,2):
  head <-> (2,2) <-> (1,1) <-> tail
  cache = {1: node1, 2: node2}

get(1):
  head <-> (1,1) <-> (2,2) <-> tail
  cache = {1: node1, 2: node2}
  結果: 1

put(3,3):
  head <-> (3,3) <-> (1,1) <-> tail
  cache = {1: node1, 3: node3}
  (2,2)が削除される

get(2):
  結果: -1（削除済み）
```

## 現実世界での応用

### 1. Webアプリケーション
- **シナリオ**: Webアプリケーションで、セッション管理やキャッシュを実装
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なWebアプリケーション

### 2. データベースシステム
- **シナリオ**: データベースで、クエリ結果をキャッシュ
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なデータベース

### 3. オペレーティングシステム
- **シナリオ**: OSで、ページキャッシュを管理
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なメモリ管理

### 4. ブラウザ
- **シナリオ**: ブラウザで、ページキャッシュを管理
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なブラウザ

### 5. CDN
- **シナリオ**: CDNで、コンテンツをキャッシュ
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なコンテンツ配信

### 6. モバイルアプリケーション
- **シナリオ**: モバイルアプリで、オフラインキャッシュを実装
- **実装**: LRU Cacheでキャッシュを管理
- **メリット**: 効率的なモバイルアプリ

## 注意点と落とし穴

### 1. 双方向リンクリストの実装
- **問題**: 双方向リンクリストを正確に実装する必要がある
- **解決策**: ダミーヘッドとダミーテールを使用
- **実装**: `head`と`tail`でエッジケースを簡潔に処理
- **注意**: ポインタの更新を正確に行う必要がある

### 2. ハッシュマップとの同期
- **問題**: ハッシュマップとリンクリストを同期させる必要がある
- **解決策**: ノードを削除する際、ハッシュマップからも削除
- **実装**: `del self.cache[lru.key]`で削除
- **注意**: 同期を忘れると、メモリリークが発生

### 3. 時間計算量の理解
- **get**: O(1) - ハッシュマップでアクセス、リンクリストで移動
- **put**: O(1) - ハッシュマップでアクセス、リンクリストで追加・削除
- **空間**: O(capacity) - ハッシュマップとリンクリスト
- **メリット**: 各操作が定数時間

### 4. 容量制限の処理
- **問題**: 容量を超えた場合、LRUを削除する必要がある
- **解決策**: 末尾のノード（LRU）を削除
- **実装**: `_remove_tail()`で削除
- **注意**: 容量チェックを忘れると、メモリリークが発生

### 5. ノードの移動
- **問題**: アクセスしたノードを先頭に移動する必要がある
- **解決策**: ノードを削除してから先頭に追加
- **実装**: `_move_to_head()`で移動
- **注意**: 移動を忘れると、LRUの判定が正しく動作しない

### 6. エッジケースの処理
- **問題**: 空のキャッシュ、容量1、既存のキーの更新
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if len(self.cache) >= self.capacity:`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

### 7. ノードクラスの定義
- **問題**: ノードクラスを定義する必要がある
- **解決策**: `key`, `value`, `prev`, `next`を持つノードクラス
- **実装**: `class Node:`で定義
- **注意**: ノードクラスの定義が重要

### 8. スレッドセーフティ
- **問題**: マルチスレッド環境での使用を考慮する必要がある場合
- **解決策**: ロックを使用してスレッドセーフにする
- **実装**: `threading.Lock()`を使用
- **注意**: この問題ではスレッドセーフティは不要

## 関連問題

- [LFU Cache](../leetcode/hard/) - より複雑なキャッシュシステム
- [Design Twitter](./design_twitter_logic.md) - 複雑な設計問題
- [Design Hit Counter](./design_hit_counter_logic.md) - カウンターシステム
- [All O`one Data Structure](../leetcode/hard/) - 複雑な設計問題

---

**次のステップ**: [Design Twitter](./design_twitter_logic.md)で複雑な設計問題を学ぶ

