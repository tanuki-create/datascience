# Design Twitter - ロジック解説

## 問題概要

Twitterのようなシステムを設計する。`postTweet(userId, tweetId)`, `getNewsFeed(userId)`, `follow(followerId, followeeId)`, `unfollow(followerId, followeeId)`を実装する。

**制約**:
- `1 <= userId, tweetId <= 500`
- ニュースフィードは最新10件を返す

**例**:
```
twitter = Twitter()
twitter.postTweet(1, 5)
twitter.getNewsFeed(1) → [5]
twitter.follow(1, 2)
twitter.postTweet(2, 6)
twitter.getNewsFeed(1) → [6, 5]
```

## ロジックの核心

### なぜ複数のデータ構造が有効か？

**単一のデータ構造（非効率）**:
- 全てのツイートを1つのリストに保存
- ニュースフィード取得時に全てをソート
- 時間計算量: O(n log n) - 非効率

**複数のデータ構造を使う理由**:
- **ユーザーごとのツイート**: 各ユーザーのツイートをリストで管理
- **フォロー関係**: セットでフォロー関係を管理
- **時間計算量**: O(1)投稿、O(k log k)取得（kはフォロー数）

### 思考プロセス

1. **ツイートの管理**: 各ユーザーのツイートを時系列順に保存
2. **フォロー関係**: セットでフォロー関係を管理
3. **ニュースフィード**: フォロー中のユーザーのツイートをマージして最新10件を返す

### アルゴリズムのステップ

```
class Twitter:
    def __init__(self):
        self.tweets = defaultdict(list)  // ユーザーごとのツイート
        self.following = defaultdict(set)  // フォロー関係
        self.time = 0  // タイムスタンプ
    
    def postTweet(self, userId, tweetId):
        self.tweets[userId].append((self.time, tweetId))
        self.time -= 1  // 負の値で最新が大きくなる
    
    def getNewsFeed(self, userId):
        heap = []
        
        // 自分のツイートを追加
        if userId in self.tweets:
            tweets = self.tweets[userId]
            if tweets:
                heap.append((tweets[-1][0], userId, len(tweets) - 1))
        
        // フォロー中のユーザーのツイートを追加
        for followeeId in self.following[userId]:
            if followeeId in self.tweets:
                tweets = self.tweets[followeeId]
                if tweets:
                    heap.append((tweets[-1][0], followeeId, len(tweets) - 1))
        
        heapq.heapify(heap)
        result = []
        
        // 最新10件を取得
        while heap and len(result) < 10:
            time, uid, idx = heapq.heappop(heap)
            result.append(self.tweets[uid][idx][1])
            
            // 次のツイートを追加
            if idx > 0:
                heapq.heappush(heap, (self.tweets[uid][idx-1][0], uid, idx-1))
        
        return result
    
    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)
    
    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

## 具体例でのトレース

### 例: `postTweet(1,5)`, `getNewsFeed(1)`, `follow(1,2)`, `postTweet(2,6)`, `getNewsFeed(1)`

```
初期状態:
  tweets = {}
  following = {}
  time = 0

postTweet(1,5):
  tweets[1] = [(-1, 5)]
  time = -1

getNewsFeed(1):
  heap = [(-1, 1, 0)]
  result = [5]

follow(1,2):
  following[1] = {2}

postTweet(2,6):
  tweets[2] = [(-2, 6)]
  time = -2

getNewsFeed(1):
  heap = [(-1, 1, 0), (-2, 2, 0)]
  result = [6, 5]
```

## 現実世界での応用

### 1. ソーシャルメディアプラットフォーム
- **シナリオ**: Twitter、Facebookなどのソーシャルメディア
- **実装**: タイムラインの管理、フォロー関係の管理
- **メリット**: 効率的なソーシャルメディア

### 2. ニュースアグリゲーター
- **シナリオ**: ニュースアプリで、複数のソースからニュースを集約
- **実装**: フォロー関係でニュースソースを管理
- **メリット**: 効率的なニュース配信

### 3. RSSリーダー
- **シナリオ**: RSSリーダーで、複数のフィードを管理
- **実装**: フォロー関係でフィードを管理
- **メリット**: 効率的なフィード管理

### 4. ブログプラットフォーム
- **シナリオ**: ブログプラットフォームで、フォロー中のブロガーの記事を表示
- **実装**: フォロー関係でブロガーを管理
- **メリット**: 効率的なコンテンツ配信

### 5. フォーラムシステム
- **シナリオ**: フォーラムで、フォロー中のユーザーの投稿を表示
- **実装**: フォロー関係でユーザーを管理
- **メリット**: 効率的なフォーラム

### 6. イベント管理システム
- **シナリオ**: イベント管理で、フォロー中の組織のイベントを表示
- **実装**: フォロー関係で組織を管理
- **メリット**: 効率的なイベント管理

## 注意点と落とし穴

### 1. タイムスタンプの管理
- **問題**: ツイートの時系列順序を管理する必要がある
- **解決策**: グローバルなタイムスタンプを使用
- **実装**: `self.time`で管理し、負の値で最新が大きくなる
- **注意**: タイムスタンプの管理が重要

### 2. ヒープの使用
- **問題**: 複数のユーザーのツイートから最新10件を取得
- **解決策**: 優先度付きキュー（ヒープ）を使用
- **実装**: 各ユーザーの最新ツイートをヒープに追加
- **メリット**: O(k log k)で最新10件を取得

### 3. フォロー関係の管理
- **問題**: フォロー関係を効率的に管理する必要がある
- **解決策**: セットを使用してO(1)で追加・削除
- **実装**: `self.following[userId]`でセットを管理
- **注意**: 自分自身をフォローしないようにする必要がある場合がある

### 4. 時間計算量の理解
- **postTweet**: O(1) - リストへの追加
- **getNewsFeed**: O(k log k) - kはフォロー数、ヒープ操作
- **follow/unfollow**: O(1) - セット操作
- **空間**: O(n) - nはツイート数

### 5. ニュースフィードの取得
- **問題**: フォロー中のユーザーのツイートをマージして最新10件を取得
- **解決策**: 各ユーザーの最新ツイートをヒープに追加し、順次取得
- **実装**: ヒープから取得後、次のツイートを追加
- **注意**: 各ユーザーのツイートインデックスを管理する必要がある

### 6. エッジケースの処理
- **問題**: フォローしていない、ツイートがない、自分自身をフォロー
- **解決策**: 各操作でエッジケースをチェック
- **実装**: `if userId in self.tweets:`などのチェック
- **注意**: エッジケースを忘れると、エラーが発生

### 7. 自分自身のフォロー
- **問題**: 自分自身をフォローする必要があるか？
- **解決策**: 通常は自分のツイートもニュースフィードに含める
- **実装**: `getNewsFeed`で自分のツイートも追加
- **注意**: 問題の要件を確認する必要がある

### 8. ツイートの削除
- **問題**: ツイートを削除する機能が必要な場合
- **解決策**: ツイートIDからユーザーとインデックスを追跡
- **実装**: 追加のデータ構造でツイートの位置を管理
- **注意**: この問題では削除機能は不要

## 関連問題

- [LRU Cache](./lru_cache_logic.md) - キャッシュシステム
- [Design Hit Counter](./design_hit_counter_logic.md) - カウンターシステム
- [Design Instagram](../leetcode/hard/) - より複雑な設計問題
- [Design Facebook](../leetcode/hard/) - より複雑な設計問題

---

**次のステップ**: [Design Hit Counter](./design_hit_counter_logic.md)でカウンターシステムを学ぶ

