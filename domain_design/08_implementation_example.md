# 08. 実装例 - ソーシャルメディアの簡易実装

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- これまで学んだ概念の統合
- ソーシャルメディアの簡易実装例
- 設計判断の説明
- 完全なコード例（簡易的だが動作する）

## 実装の全体像

この章では、これまで学んだDDDの概念を統合して、ソーシャルメディアアプリケーションの簡易実装を作成します。

### 実装する機能

1. **ユーザー管理**: ユーザーの作成、取得
2. **投稿管理**: 投稿の作成、取得、削除
3. **フォロー関係**: ユーザーのフォロー、フォロー解除
4. **いいね機能**: 投稿へのいいね、いいね解除
5. **コメント機能**: 投稿へのコメント追加
6. **タイムライン**: ホームタイムラインの生成

### アーキテクチャ

```
┌─────────────────────────────────────┐
│   Application Layer                │
│   (PostApplicationService, etc.)   │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Domain Layer                      │
│   (Post, User, TimelineService)     │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Infrastructure Layer              │
│   (PostRepository, UserRepository)  │
└─────────────────────────────────────┘
```

## 値オブジェクト

### Email

```python
class Email:
    """メールアドレス（値オブジェクト）"""
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self._value = value
    
    def _is_valid(self, value):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, value) is not None
    
    @property
    def value(self):
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)
    
    def __str__(self):
        return self._value
```

### PostContent

```python
class PostContent:
    """投稿内容（値オブジェクト）"""
    def __init__(self, value):
        if not value or len(value) == 0:
            raise ValueError("Post content cannot be empty")
        if len(value) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @property
    def length(self):
        return len(self._value)
    
    def __eq__(self, other):
        if not isinstance(other, PostContent):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)
    
    def __str__(self):
        return self._value
```

## エンティティ

### User

```python
from datetime import datetime

class User:
    """ユーザー（エンティティ）"""
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = Email(email)
        self._following = set()  # フォローしているユーザーのID
        self.created_at = datetime.now()
    
    def follow(self, user_id):
        """ユーザーをフォロー"""
        if self.user_id == user_id:
            raise ValueError("Cannot follow yourself")
        self._following.add(user_id)
    
    def unfollow(self, user_id):
        """フォローを解除"""
        self._following.discard(user_id)
    
    def get_following(self):
        """フォローしているユーザーのIDを取得"""
        return list(self._following)
    
    def is_following(self, user_id):
        """フォローしているかチェック"""
        return user_id in self._following
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id
    
    def __hash__(self):
        return hash(self.user_id)
```

### Like

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
    
    def __hash__(self):
        return hash(self.user_id)
```

### Comment

```python
class Comment:
    """コメント（エンティティ）"""
    def __init__(self, comment_id, post_id, author_id, content):
        self.comment_id = comment_id
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.created_at = datetime.now()
    
    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return self.comment_id == other.comment_id
    
    def __hash__(self):
        return hash(self.comment_id)
```

### Post（集約ルート）

```python
class Post:
    """投稿（集約ルート）"""
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = PostContent(content)
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
        return list(self._comments)
    
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
        return list(self._likes)
```

## リポジトリ

### PostRepository

```python
from abc import ABC, abstractmethod

class PostRepository(ABC):
    """投稿リポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, post):
        """投稿を保存"""
        pass
    
    @abstractmethod
    def find_by_id(self, post_id):
        """IDで投稿を取得"""
        pass
    
    @abstractmethod
    def find_by_author_id(self, author_id):
        """作成者IDで投稿を取得"""
        pass
    
    @abstractmethod
    def delete(self, post_id):
        """投稿を削除"""
        pass

class InMemoryPostRepository(PostRepository):
    """メモリ上の投稿リポジトリ（テスト用）"""
    
    def __init__(self):
        self._posts = {}  # {post_id: post}
    
    def save(self, post):
        """投稿を保存"""
        self._posts[post.post_id] = post
    
    def find_by_id(self, post_id):
        """IDで投稿を取得"""
        return self._posts.get(post_id)
    
    def find_by_author_id(self, author_id):
        """作成者IDで投稿を取得"""
        return [post for post in self._posts.values() if post.author_id == author_id]
    
    def delete(self, post_id):
        """投稿を削除"""
        if post_id in self._posts:
            del self._posts[post_id]
```

### UserRepository

```python
class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, user):
        """ユーザーを保存"""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id):
        """IDでユーザーを取得"""
        pass
    
    @abstractmethod
    def find_by_email(self, email):
        """メールアドレスでユーザーを取得"""
        pass

class InMemoryUserRepository(UserRepository):
    """メモリ上のユーザーリポジトリ（テスト用）"""
    
    def __init__(self):
        self._users = {}  # {user_id: user}
        self._users_by_email = {}  # {email: user}
    
    def save(self, user):
        """ユーザーを保存"""
        self._users[user.user_id] = user
        self._users_by_email[user.email.value] = user
    
    def find_by_id(self, user_id):
        """IDでユーザーを取得"""
        return self._users.get(user_id)
    
    def find_by_email(self, email):
        """メールアドレスでユーザーを取得"""
        if isinstance(email, Email):
            email = email.value
        return self._users_by_email.get(email)
```

## ドメインサービス

### TimelineService

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

## アプリケーションサービス

### PostApplicationService

```python
import uuid

class PostApplicationService:
    """投稿アプリケーションサービス"""
    
    def __init__(self, post_repository, user_repository):
        self.post_repository = post_repository
        self.user_repository = user_repository
    
    def create_post(self, author_id, content):
        """投稿を作成"""
        # ユーザーを取得
        user = self.user_repository.find_by_id(author_id)
        if not user:
            raise ValueError("User not found")
        
        # 投稿を作成
        post = Post(
            post_id=str(uuid.uuid4()),
            author_id=author_id,
            content=content
        )
        
        # 投稿を保存
        self.post_repository.save(post)
        
        return post
    
    def get_post(self, post_id):
        """投稿を取得"""
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        return post
    
    def delete_post(self, post_id, user_id):
        """投稿を削除"""
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        # 権限チェック: 作成者のみ削除可能
        if post.author_id != user_id:
            raise ValueError("Only the author can delete the post")
        
        self.post_repository.delete(post_id)
    
    def add_comment(self, post_id, author_id, content):
        """コメントを追加"""
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        comment = Comment(
            comment_id=str(uuid.uuid4()),
            post_id=post_id,
            author_id=author_id,
            content=content
        )
        
        post.add_comment(comment)
        self.post_repository.save(post)
        
        return comment
    
    def add_like(self, post_id, user_id):
        """いいねを追加"""
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        post.add_like(user_id)
        self.post_repository.save(post)
    
    def remove_like(self, post_id, user_id):
        """いいねを削除"""
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise ValueError("Post not found")
        
        post.remove_like(user_id)
        self.post_repository.save(post)
```

### UserApplicationService

```python
class UserApplicationService:
    """ユーザーアプリケーションサービス"""
    
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def create_user(self, name, email):
        """ユーザーを作成"""
        # メールアドレスの重複チェック
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")
        
        user = User(
            user_id=str(uuid.uuid4()),
            name=name,
            email=email
        )
        
        self.user_repository.save(user)
        
        return user
    
    def get_user(self, user_id):
        """ユーザーを取得"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    def follow_user(self, follower_id, followee_id):
        """ユーザーをフォロー"""
        follower = self.user_repository.find_by_id(follower_id)
        if not follower:
            raise ValueError("Follower not found")
        
        followee = self.user_repository.find_by_id(followee_id)
        if not followee:
            raise ValueError("Followee not found")
        
        follower.follow(followee_id)
        self.user_repository.save(follower)
    
    def unfollow_user(self, follower_id, followee_id):
        """フォローを解除"""
        follower = self.user_repository.find_by_id(follower_id)
        if not follower:
            raise ValueError("Follower not found")
        
        follower.unfollow(followee_id)
        self.user_repository.save(follower)
```

### TimelineApplicationService

```python
class TimelineApplicationService:
    """タイムラインアプリケーションサービス"""
    
    def __init__(self, user_repository, post_repository):
        self.user_repository = user_repository
        self.post_repository = post_repository
        self.timeline_service = TimelineService(post_repository)
    
    def get_home_timeline(self, user_id):
        """ホームタイムラインを取得"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        timeline = self.timeline_service.generate_home_timeline(user)
        
        return timeline
    
    def get_user_timeline(self, user_id):
        """ユーザータイムラインを取得"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        timeline = self.timeline_service.generate_user_timeline(user)
        
        return timeline
```

## 使用例

### 基本的な使用例

```python
# リポジトリの初期化
user_repository = InMemoryUserRepository()
post_repository = InMemoryPostRepository()

# アプリケーションサービスの初期化
user_service = UserApplicationService(user_repository)
post_service = PostApplicationService(post_repository, user_repository)
timeline_service = TimelineApplicationService(user_repository, post_repository)

# ユーザーを作成
user1 = user_service.create_user("Alice", "alice@example.com")
user2 = user_service.create_user("Bob", "bob@example.com")

# ユーザーをフォロー
user_service.follow_user(user1.user_id, user2.user_id)

# 投稿を作成
post1 = post_service.create_post(user2.user_id, "Hello, world!")
post2 = post_service.create_post(user2.user_id, "This is my second post")

# いいねを追加
post_service.add_like(post1.post_id, user1.user_id)

# コメントを追加
comment = post_service.add_comment(post1.post_id, user1.user_id, "Nice post!")

# ホームタイムラインを取得
timeline = timeline_service.get_home_timeline(user1.user_id)

# タイムラインを表示
for post in timeline:
    print(f"{post.author_id}: {post.content.value}")
    print(f"  Likes: {post.get_like_count()}")
    print(f"  Comments: {len(post.get_comments())}")
    print()
```

## 設計判断の説明

### 判断1: Postを集約ルートにする

**理由**: Postは、CommentとLikeの整合性を保つ必要があるため、集約ルートとして設計しました。

### 判断2: UserとPostを別の集約にする

**理由**: UserとPostは異なる整合性の境界を持つため、別の集約として設計しました。User集約はフォロー関係を管理し、Post集約は投稿とそのコメント・いいねを管理します。

### 判断3: TimelineServiceをドメインサービスにする

**理由**: タイムライン生成は、User集約とPost集約にまたがるロジックのため、ドメインサービスとして実装しました。

### 判断4: 集約間の参照はIDで行う

**理由**: Post集約は、User集約のUserオブジェクトを直接参照せず、author_id（User ID）のみを保持します。これにより、集約間の結合を弱め、変更の影響を最小限に抑えます。

## まとめ

この実装例では、以下のDDDの概念を統合しました：

- **値オブジェクト**: Email、PostContent、Like
- **エンティティ**: User、Post、Comment
- **集約**: Post集約（Post + Comment + Like）
- **リポジトリ**: PostRepository、UserRepository
- **ドメインサービス**: TimelineService
- **アプリケーションサービス**: PostApplicationService、UserApplicationService、TimelineApplicationService

これらの概念を統合することで、保守性が高く、テストしやすい、ビジネスロジックが明確なコードを実現できました。

## 考えてみよう

1. この実装例で、どの部分がDDDのどの概念に対応していますか？
2. この実装例を改善できる箇所はありますか？
3. 実際のプロジェクトで、この実装例をどのように適用できますか？

次の章では、**ベストプラクティス**について詳しく学びます。

