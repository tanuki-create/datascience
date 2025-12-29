# 06. ドメインサービス - 集約に属さないロジック

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- ドメインサービスとは（エンティティや値オブジェクトに属さないロジック）
- Timeline生成サービスの例
- ドメインサービス vs アプリケーションサービス
- 実装コード例

## ドメインサービスとは

**ドメインサービス（Domain Service）**は、エンティティや値オブジェクトに属さないドメインロジックです。

### 定義

> **ドメインサービス**は、複数の集約にまたがるロジックや、エンティティや値オブジェクトに属さないロジックを扱うサービスです。

### なぜドメインサービスが必要か

エンティティや値オブジェクトに属さないロジックが存在します。例えば：

1. **複数の集約にまたがるロジック**: タイムライン生成（Post集約とUser集約にまたがる）
2. **エンティティに属さないロジック**: ユニークなメールアドレスの検証（Userエンティティに属さない）
3. **値オブジェクトに属さないロジック**: 複雑な計算ロジック

## ドメインサービス vs エンティティ/値オブジェクト

### エンティティ/値オブジェクトに属するロジック

```python
class Post:
    """投稿（エンティティ）"""
    def add_like(self, user_id):
        """いいねを追加（Postエンティティに属するロジック）"""
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        like = Like(user_id)
        self._likes.append(like)
```

**特徴**: Postエンティティに属するロジック（Postの状態を変更する）

### ドメインサービスに属するロジック

```python
class TimelineService:
    """タイムラインサービス（ドメインサービス）"""
    def generate_timeline(self, user, post_repository):
        """タイムラインを生成（複数の集約にまたがるロジック）"""
        # User集約とPost集約にまたがるロジック
        following = user.get_following()
        posts = []
        for user_id in following:
            user_posts = post_repository.find_by_author_id(user_id)
            posts.extend(user_posts)
        return sorted(posts, key=lambda p: p.created_at, reverse=True)
```

**特徴**: 複数の集約にまたがるロジック（TimelineServiceに属する）

## Timeline生成サービスの例

### 問題: タイムライン生成はどこに属するか？

タイムライン生成は、以下の集約にまたがります：

- **User集約**: フォローしているユーザーを取得
- **Post集約**: フォローしているユーザーの投稿を取得

このロジックは、どちらの集約にも属しません。したがって、**ドメインサービス**として実装します。

### 実装例

```python
class TimelineService:
    """タイムラインサービス（ドメインサービス）"""
    
    def __init__(self, post_repository):
        self.post_repository = post_repository
    
    def generate_home_timeline(self, user):
        """ホームタイムラインを生成"""
        # User集約からフォローしているユーザーを取得
        following = user.get_following()
        
        # Post集約からフォローしているユーザーの投稿を取得
        posts = []
        for user_id in following:
            user_posts = self.post_repository.find_by_author_id(user_id)
            posts.extend(user_posts)
        
        # 時系列でソート
        sorted_posts = sorted(posts, key=lambda p: p.created_at, reverse=True)
        
        # 最新20件を返す
        return sorted_posts[:20]
    
    def generate_user_timeline(self, user):
        """ユーザータイムラインを生成（特定のユーザーの投稿）"""
        # Post集約からユーザーの投稿を取得
        posts = self.post_repository.find_by_author_id(user.user_id)
        
        # 時系列でソート
        sorted_posts = sorted(posts, key=lambda p: p.created_at, reverse=True)
        
        return sorted_posts
```

### 使用例

```python
# ドメインサービスの使用
post_repository = PostRepositoryImpl(db)
timeline_service = TimelineService(post_repository)

# ホームタイムラインを生成
user = user_repository.find_by_id("123")
timeline = timeline_service.generate_home_timeline(user)

# タイムラインを表示
for post in timeline:
    print(f"{post.author_id}: {post.content.value}")
```

## ドメインサービス vs アプリケーションサービス

### ドメインサービス

**ドメインサービス**は、ドメインロジックを扱います。

- **特徴**: ドメインロジックのみ（永続化の詳細は含まない）
- **例**: Timeline生成、ユニークなメールアドレスの検証

### アプリケーションサービス

**アプリケーションサービス**は、アプリケーションのユースケースを実装します。

- **特徴**: ドメインサービスやリポジトリを組み合わせて、ユースケースを実装
- **例**: 投稿作成、ユーザー登録

### 比較例

#### ドメインサービス

```python
class TimelineService:
    """タイムラインサービス（ドメインサービス）"""
    def generate_home_timeline(self, user, post_repository):
        """ホームタイムラインを生成（ドメインロジックのみ）"""
        following = user.get_following()
        posts = []
        for user_id in following:
            user_posts = post_repository.find_by_author_id(user_id)
            posts.extend(user_posts)
        return sorted(posts, key=lambda p: p.created_at, reverse=True)
```

**特徴**: ドメインロジックのみ（永続化の詳細は含まない）

#### アプリケーションサービス

```python
class PostApplicationService:
    """投稿アプリケーションサービス（アプリケーションサービス）"""
    def __init__(self, post_repository, user_repository):
        self.post_repository = post_repository
        self.user_repository = user_repository
    
    def create_post(self, user_id, content):
        """投稿を作成（ユースケース）"""
        # ユーザーを取得
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # 投稿を作成
        post = Post(
            post_id=generate_id(),
            author_id=user_id,
            content=PostContent(content)
        )
        
        # 投稿を保存
        self.post_repository.save(post)
        
        return post
    
    def get_home_timeline(self, user_id):
        """ホームタイムラインを取得（ユースケース）"""
        # ユーザーを取得
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # ドメインサービスを使用
        timeline_service = TimelineService(self.post_repository)
        timeline = timeline_service.generate_home_timeline(user)
        
        return timeline
```

**特徴**: ドメインサービスやリポジトリを組み合わせて、ユースケースを実装

## ドメインサービスの適用タイミング

### タイミング1: 複数の集約にまたがるロジック

```python
class FollowService:
    """フォローサービス（ドメインサービス）"""
    def follow_user(self, follower, followee):
        """ユーザーをフォロー（複数の集約にまたがる）"""
        # User集約: フォロワーを追加
        follower.add_following(followee.user_id)
        
        # User集約: フォロイーを追加
        followee.add_follower(follower.user_id)
        
        # ビジネスルール: 自分自身をフォローできない
        if follower.user_id == followee.user_id:
            raise ValueError("Cannot follow yourself")
```

**理由**: 複数のUser集約にまたがるロジックのため

### タイミング2: エンティティに属さないロジック

```python
class EmailUniquenessService:
    """メールアドレス一意性サービス（ドメインサービス）"""
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def is_email_unique(self, email):
        """メールアドレスが一意かチェック"""
        existing_user = self.user_repository.find_by_email(email)
        return existing_user is None
```

**理由**: Userエンティティに属さないロジック（リポジトリにアクセスする必要がある）のため

### タイミング3: 複雑な計算ロジック

```python
class PostRankingService:
    """投稿ランキングサービス（ドメインサービス）"""
    def calculate_score(self, post):
        """投稿のスコアを計算"""
        # 複雑な計算ロジック
        like_score = post.get_like_count() * 10
        comment_score = len(post.get_comments()) * 5
        time_score = self._calculate_time_score(post.created_at)
        return like_score + comment_score + time_score
    
    def _calculate_time_score(self, created_at):
        """時間スコアを計算"""
        # 複雑な計算ロジック
        hours_since_creation = (datetime.now() - created_at).total_seconds() / 3600
        return max(0, 100 - hours_since_creation)
```

**理由**: 複雑な計算ロジックのため（Postエンティティに属さない）

## よくある間違い

### 間違い1: エンティティに属するロジックをドメインサービスに

```python
# ❌ 悪い例: エンティティに属するロジックをドメインサービスに
class PostService:
    def add_like(self, post, user_id):
        # 問題: このロジックはPostエンティティに属する
        if post.has_liked(user_id):
            raise ValueError("User has already liked this post")
        post._likes.append(Like(user_id))

# ✅ 良い例: エンティティに属するロジックはエンティティに
class Post:
    def add_like(self, user_id):
        # このロジックはPostエンティティに属する
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        self._likes.append(Like(user_id))
```

### 間違い2: アプリケーションロジックをドメインサービスに

```python
# ❌ 悪い例: アプリケーションロジックをドメインサービスに
class PostService:
    def create_post(self, user_id, content):
        # 問題: これはアプリケーションサービスに属する
        user = self.user_repository.find_by_id(user_id)
        post = Post(post_id=generate_id(), author_id=user_id, content=content)
        self.post_repository.save(post)
        return post

# ✅ 良い例: アプリケーションロジックはアプリケーションサービスに
class PostApplicationService:
    def create_post(self, user_id, content):
        # これはアプリケーションサービスに属する
        user = self.user_repository.find_by_id(user_id)
        post = Post(post_id=generate_id(), author_id=user_id, content=content)
        self.post_repository.save(post)
        return post
```

### 間違い3: ドメインサービスに永続化の詳細を含める

```python
# ❌ 悪い例: ドメインサービスに永続化の詳細を含める
class TimelineService:
    def generate_home_timeline(self, user_id):
        # 問題: データベースの詳細が含まれている
        db.execute("SELECT * FROM posts WHERE author_id IN (SELECT followee_id FROM follows WHERE follower_id = ?)", user_id)
        # ...

# ✅ 良い例: ドメインサービスはリポジトリを使用
class TimelineService:
    def __init__(self, post_repository):
        self.post_repository = post_repository
    
    def generate_home_timeline(self, user):
        # リポジトリを使用（永続化の詳細は含まない）
        following = user.get_following()
        posts = []
        for user_id in following:
            user_posts = self.post_repository.find_by_author_id(user_id)
            posts.extend(user_posts)
        return sorted(posts, key=lambda p: p.created_at, reverse=True)
```

## まとめ

- **ドメインサービス**は、エンティティや値オブジェクトに属さないドメインロジック
- **複数の集約にまたがるロジック**は、ドメインサービスに実装
- **エンティティに属するロジック**は、エンティティに実装
- **アプリケーションロジック**は、アプリケーションサービスに実装
- **ドメインサービス**は、永続化の詳細を含めない（リポジトリを使用）

## 考えてみよう

1. あなたのプロジェクトで、ドメインサービスを使用していますか？
2. エンティティに属するロジックをドメインサービスに実装している箇所はありますか？
3. アプリケーションロジックをドメインサービスに実装している箇所はありますか？

次の章では、**境界づけられたコンテキスト**について詳しく学びます。

