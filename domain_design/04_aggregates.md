# 04. 集約 - 整合性の境界

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- 集約の概念（整合性の境界）
- 集約ルートの役割
- 不変条件（Invariant）の定義
- Post集約の例（Post + Comments + Likes）
- 集約のサイズと設計原則

## 集約とは

**集約（Aggregate）**は、DDDの最も重要な概念の一つです。

### 定義

> **集約**は、**整合性の境界**を持つオブジェクトのグループです。集約内のオブジェクトは、集約ルートを通じてのみアクセスされます。

### なぜ集約が必要か

複雑なドメインモデルでは、多くのオブジェクトが関連しています。すべてのオブジェクト間で整合性を保つのは困難です。

**例**: 投稿（Post）には、コメント（Comment）やいいね（Like）が関連しています。投稿が削除されたら、コメントやいいねも削除される必要があります。この整合性を保つために、集約を使用します。

## 集約の構成要素

### 集約ルート（Aggregate Root）

**集約ルート**は、集約の外部からアクセスする唯一のエントリーポイントです。

- **役割**: 集約内の整合性を保証する
- **特徴**: 集約の外部からは、集約ルートを通じてのみアクセスする

### 集約内のオブジェクト

集約内のオブジェクトは、集約ルートを通じてのみアクセスされます。

- **特徴**: 集約の外部から直接アクセスできない
- **役割**: 集約ルートの整合性を保つために存在する

## Post集約の例

### 集約の設計

ソーシャルメディアの投稿（Post）を例に、集約を設計しましょう。

**集約ルート**: `Post`
**集約内のオブジェクト**: `Comment`、`Like`

### 実装例

```python
class Like:
    """いいね（値オブジェクト）"""
    def __init__(self, user_id):
        self.user_id = user_id
        self.created_at = datetime.now()
    
    def __eq__(self, other):
        if not isinstance(other, Like):
            return False
        return self.user_id == other.user_id

class Comment:
    """コメント（エンティティ）"""
    def __init__(self, comment_id, author, content):
        self.comment_id = comment_id
        self.author = author
        self.content = content
        self.created_at = datetime.now()
    
    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.comment_id == other.comment_id

class Post:
    """投稿（集約ルート）"""
    def __init__(self, post_id, author, content):
        self.post_id = post_id
        self.author = author
        self.content = content
        self.created_at = datetime.now()
        self._comments = []  # 集約内のオブジェクト
        self._likes = []     # 集約内のオブジェクト
    
    def add_comment(self, comment):
        """コメントを追加（集約ルートを通じてのみアクセス）"""
        # 不変条件: コメントは投稿に属する
        if comment.post_id != self.post_id:
            raise ValueError("Comment does not belong to this post")
        self._comments.append(comment)
    
    def remove_comment(self, comment_id):
        """コメントを削除（集約ルートを通じてのみアクセス）"""
        self._comments = [c for c in self._comments if c.comment_id != comment_id]
    
    def get_comments(self):
        """コメントを取得（読み取り専用のコピーを返す）"""
        return list(self._comments)  # コピーを返す（不変性を保つ）
    
    def add_like(self, user_id):
        """いいねを追加（集約ルートを通じてのみアクセス）"""
        # 不変条件: 同じユーザーは複数回いいねできない
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        like = Like(user_id)
        self._likes.append(like)
    
    def remove_like(self, user_id):
        """いいねを削除（集約ルートを通じてのみアクセス）"""
        self._likes = [l for l in self._likes if l.user_id != user_id]
    
    def has_liked(self, user_id):
        """いいね済みかチェック"""
        return any(l.user_id == user_id for l in self._likes)
    
    def get_like_count(self):
        """いいね数を取得"""
        return len(self._likes)
    
    def get_likes(self):
        """いいねを取得（読み取り専用のコピーを返す）"""
        return list(self._likes)  # コピーを返す（不変性を保つ）
```

### 集約の使用例

```python
# 集約の外部からは、集約ルート（Post）を通じてのみアクセス
post = Post(post_id="123", author=user, content="Hello, world!")

# ✅ 良い例: 集約ルートを通じてコメントを追加
comment = Comment(comment_id="456", author=user, content="Nice post!")
post.add_comment(comment)

# ✅ 良い例: 集約ルートを通じていいねを追加
post.add_like(user_id="789")

# ❌ 悪い例: 集約内のオブジェクトに直接アクセス
# post._comments.append(comment)  # これは避けるべき

# ✅ 良い例: 集約ルートを通じてコメントを取得
comments = post.get_comments()

# ✅ 良い例: 集約ルートを通じていいね数を取得
like_count = post.get_like_count()
```

## 不変条件（Invariant）

**不変条件（Invariant）**は、集約が常に満たすべき条件です。

### Post集約の不変条件

1. **コメントは投稿に属する**: コメントは、必ず特定の投稿に属する
2. **同じユーザーは複数回いいねできない**: 1つの投稿に対して、同じユーザーは1回だけいいねできる
3. **いいね数は正確**: いいね数は、実際のいいねの数と一致する

### 不変条件の実装

```python
class Post:
    def add_comment(self, comment):
        # 不変条件1: コメントは投稿に属する
        if comment.post_id != self.post_id:
            raise ValueError("Comment does not belong to this post")
        self._comments.append(comment)
    
    def add_like(self, user_id):
        # 不変条件2: 同じユーザーは複数回いいねできない
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        like = Like(user_id)
        self._likes.append(like)
        # 不変条件3: いいね数は正確（自動的に保証される）
    
    def remove_like(self, user_id):
        self._likes = [l for l in self._likes if l.user_id != user_id]
        # 不変条件3: いいね数は正確（自動的に保証される）
```

## 集約の設計原則

### 原則1: 集約は小さく保つ

**理由**: 集約が大きいと、整合性を保つのが困難になり、パフォーマンスも低下します。

#### 悪い例: 集約が大きすぎる

```python
# ❌ 悪い例: すべてを1つの集約に含める
class SocialMediaPlatform:
    """ソーシャルメディアプラットフォーム（集約ルート）"""
    def __init__(self):
        self._users = []      # すべてのユーザー
        self._posts = []      # すべての投稿
        self._comments = []   # すべてのコメント
        self._likes = []      # すべてのいいね
        # 問題: 集約が大きすぎる
```

#### 良い例: 集約を小さく保つ

```python
# ✅ 良い例: 各集約を小さく保つ
class Post:
    """投稿集約（小さい）"""
    def __init__(self, post_id, author, content):
        self.post_id = post_id
        self.author = author
        self.content = content
        self._comments = []  # この投稿のコメントのみ
        self._likes = []     # この投稿のいいねのみ

class User:
    """ユーザー集約（小さい）"""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self._following = []  # このユーザーがフォローしているユーザーのIDのみ
```

### 原則2: 集約間の参照はIDで行う

**理由**: 集約間で直接オブジェクトを参照すると、整合性の境界が曖昧になります。

#### 悪い例: 集約間で直接参照

```python
# ❌ 悪い例: 集約間で直接参照
class Post:
    def __init__(self, post_id, author, content):
        self.post_id = post_id
        self.author = author  # Userオブジェクトを直接参照
        self.content = content
        # 問題: 集約間の境界が曖昧
```

#### 良い例: 集約間の参照はIDで行う

```python
# ✅ 良い例: 集約間の参照はIDで行う
class Post:
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id  # UserのIDを参照
        self.content = content
        # 良い: 集約間の境界が明確
```

### 原則3: 集約の外部からは、集約ルートを通じてのみアクセス

**理由**: 集約内の整合性を保つため、集約ルートを通じてのみアクセスします。

#### 悪い例: 集約内のオブジェクトに直接アクセス

```python
# ❌ 悪い例: 集約内のオブジェクトに直接アクセス
post = Post(post_id="123", author_id="456", content="Hello")
post._comments.append(comment)  # 直接アクセス（避けるべき）
post._likes.append(like)        # 直接アクセス（避けるべき）
```

#### 良い例: 集約ルートを通じてアクセス

```python
# ✅ 良い例: 集約ルートを通じてアクセス
post = Post(post_id="123", author_id="456", content="Hello")
post.add_comment(comment)  # 集約ルートを通じてアクセス
post.add_like(user_id)     # 集約ルートを通じてアクセス
```

## 集約のサイズ

### 小さな集約の例

```python
class Post:
    """投稿集約（小さい）"""
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self._comments = []  # この投稿のコメントのみ
        self._likes = []     # この投稿のいいねのみ
```

**特徴**:
- 整合性を保ちやすい
- パフォーマンスが良い
- テストが容易

### 大きな集約の例（避けるべき）

```python
# ❌ 悪い例: 集約が大きすぎる
class User:
    """ユーザー集約（大きすぎる）"""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self._posts = []        # すべての投稿
        self._comments = []      # すべてのコメント
        self._likes = []        # すべてのいいね
        self._following = []    # フォローしているユーザー
        self._followers = []    # フォロワー
        # 問題: 集約が大きすぎる
```

**問題点**:
- 整合性を保ちにくい
- パフォーマンスが悪い
- テストが困難

## 集約の永続化

集約は、**トランザクション単位**で保存・取得されます。

### 保存

```python
# 集約全体を1つのトランザクションで保存
def save_post(post):
    # Post、Comment、Likeを1つのトランザクションで保存
    with transaction():
        db.save_post(post)
        for comment in post.get_comments():
            db.save_comment(comment)
        for like in post.get_likes():
            db.save_like(like)
```

### 取得

```python
# 集約全体を1つのトランザクションで取得
def get_post(post_id):
    # Post、Comment、Likeを1つのトランザクションで取得
    post = db.get_post(post_id)
    comments = db.get_comments_by_post_id(post_id)
    likes = db.get_likes_by_post_id(post_id)
    post._comments = comments
    post._likes = likes
    return post
```

## よくある間違い

### 間違い1: 集約が大きすぎる

```python
# ❌ 悪い例: すべてを1つの集約に含める
class SocialMediaPlatform:
    def __init__(self):
        self._users = []
        self._posts = []
        self._comments = []
        # 問題: 集約が大きすぎる

# ✅ 良い例: 集約を小さく保つ
class Post:
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self._comments = []  # この投稿のコメントのみ
```

### 間違い2: 集約間で直接参照

```python
# ❌ 悪い例: 集約間で直接参照
class Post:
    def __init__(self, post_id, author, content):
        self.author = author  # Userオブジェクトを直接参照

# ✅ 良い例: 集約間の参照はIDで行う
class Post:
    def __init__(self, post_id, author_id, content):
        self.author_id = author_id  # UserのIDを参照
```

### 間違い3: 集約内のオブジェクトに直接アクセス

```python
# ❌ 悪い例: 集約内のオブジェクトに直接アクセス
post._comments.append(comment)

# ✅ 良い例: 集約ルートを通じてアクセス
post.add_comment(comment)
```

## まとめ

- **集約**は、整合性の境界を持つオブジェクトのグループ
- **集約ルート**は、集約の外部からアクセスする唯一のエントリーポイント
- **不変条件**は、集約が常に満たすべき条件
- **集約は小さく保つ**: 整合性を保ちやすく、パフォーマンスも良い
- **集約間の参照はIDで行う**: 集約間の境界を明確にする
- **集約の外部からは、集約ルートを通じてのみアクセス**: 整合性を保つため

## 考えてみよう

1. あなたのプロジェクトで、集約を設計したことはありますか？
2. 集約が大きすぎる箇所はありますか？
3. 集約間で直接参照している箇所はありますか？

次の章では、**リポジトリ**について詳しく学びます。

