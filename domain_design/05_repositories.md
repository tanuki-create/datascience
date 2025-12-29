# 05. リポジトリ - 永続化の抽象化

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- リポジトリパターンの目的（永続化の抽象化）
- PostRepository、UserRepositoryの例
- クエリとコマンドの分離
- 実装コード例

## リポジトリとは

**リポジトリ（Repository）**は、集約の永続化を抽象化するオブジェクトです。

### 定義

> **リポジトリ**は、集約の保存・取得を抽象化し、ドメインモデルから永続化の詳細を隠蔽します。

### なぜリポジトリが必要か

ドメインモデルは、データベースの詳細を知る必要がありません。リポジトリを使用することで、以下のメリットがあります：

1. **ドメインモデルの独立性**: ドメインモデルがデータベースの詳細に依存しない
2. **テストの容易さ**: メモリ上のリポジトリでテストできる
3. **永続化の変更が容易**: データベースを変更しても、ドメインモデルは変更不要

## リポジトリの基本

### リポジトリのインターフェース

リポジトリは、**インターフェース**として定義します。

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
```

### リポジトリの実装

リポジトリの実装は、データベースの詳細を含みます。

```python
class PostRepositoryImpl(PostRepository):
    """投稿リポジトリの実装（データベース）"""
    
    def __init__(self, db):
        self.db = db
    
    def save(self, post):
        """投稿を保存"""
        # データベースの詳細
        with self.db.transaction():
            # Postを保存
            self.db.execute(
                "INSERT INTO posts (id, author_id, content, created_at) VALUES (?, ?, ?, ?)",
                post.post_id, post.author_id, post.content.value, post.created_at
            )
            # Commentを保存
            for comment in post.get_comments():
                self.db.execute(
                    "INSERT INTO comments (id, post_id, author_id, content, created_at) VALUES (?, ?, ?, ?, ?)",
                    comment.comment_id, post.post_id, comment.author_id, comment.content, comment.created_at
                )
            # Likeを保存
            for like in post.get_likes():
                self.db.execute(
                    "INSERT INTO likes (post_id, user_id, created_at) VALUES (?, ?, ?)",
                    post.post_id, like.user_id, like.created_at
                )
    
    def find_by_id(self, post_id):
        """IDで投稿を取得"""
        # データベースの詳細
        post_row = self.db.execute(
            "SELECT * FROM posts WHERE id = ?",
            post_id
        ).fetchone()
        
        if not post_row:
            return None
        
        # Postオブジェクトを再構築
        post = Post(
            post_id=post_row['id'],
            author_id=post_row['author_id'],
            content=PostContent(post_row['content'])
        )
        
        # Commentを取得
        comment_rows = self.db.execute(
            "SELECT * FROM comments WHERE post_id = ?",
            post_id
        ).fetchall()
        for row in comment_rows:
            comment = Comment(
                comment_id=row['id'],
                author_id=row['author_id'],
                content=row['content']
            )
            post.add_comment(comment)
        
        # Likeを取得
        like_rows = self.db.execute(
            "SELECT * FROM likes WHERE post_id = ?",
            post_id
        ).fetchall()
        for row in like_rows:
            post.add_like(row['user_id'])
        
        return post
    
    def find_by_author_id(self, author_id):
        """作成者IDで投稿を取得"""
        post_rows = self.db.execute(
            "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC",
            author_id
        ).fetchall()
        
        posts = []
        for row in post_rows:
            post = self.find_by_id(row['id'])
            posts.append(post)
        
        return posts
    
    def delete(self, post_id):
        """投稿を削除"""
        with self.db.transaction():
            # Likeを削除
            self.db.execute("DELETE FROM likes WHERE post_id = ?", post_id)
            # Commentを削除
            self.db.execute("DELETE FROM comments WHERE post_id = ?", post_id)
            # Postを削除
            self.db.execute("DELETE FROM posts WHERE id = ?", post_id)
```

### メモリ上のリポジトリ（テスト用）

テストでは、メモリ上のリポジトリを使用します。

```python
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

## リポジトリの使用例

### ドメインモデルでの使用

```python
class PostService:
    """投稿サービス（アプリケーション層）"""
    
    def __init__(self, post_repository):
        self.post_repository = post_repository
    
    def create_post(self, author_id, content):
        """投稿を作成"""
        # ドメインモデルを作成
        post = Post(
            post_id=generate_id(),
            author_id=author_id,
            content=PostContent(content)
        )
        
        # リポジトリを通じて保存
        self.post_repository.save(post)
        
        return post
    
    def get_post(self, post_id):
        """投稿を取得"""
        # リポジトリを通じて取得
        return self.post_repository.find_by_id(post_id)
    
    def get_posts_by_author(self, author_id):
        """作成者の投稿を取得"""
        # リポジトリを通じて取得
        return self.post_repository.find_by_author_id(author_id)
    
    def delete_post(self, post_id):
        """投稿を削除"""
        # リポジトリを通じて削除
        self.post_repository.delete(post_id)
```

### テストでの使用

```python
def test_create_post():
    """投稿作成のテスト"""
    # メモリ上のリポジトリを使用
    post_repository = InMemoryPostRepository()
    post_service = PostService(post_repository)
    
    # 投稿を作成
    post = post_service.create_post(
        author_id="123",
        content="Hello, world!"
    )
    
    # 検証
    assert post is not None
    assert post.author_id == "123"
    assert post.content.value == "Hello, world!"
    
    # リポジトリから取得して検証
    retrieved_post = post_repository.find_by_id(post.post_id)
    assert retrieved_post is not None
    assert retrieved_post.post_id == post.post_id
```

## クエリとコマンドの分離

### コマンド（Command）

**コマンド**は、集約の状態を変更する操作です。

- **例**: `save()`, `delete()`
- **特徴**: 副作用がある（状態を変更する）

### クエリ（Query）

**クエリ**は、集約の状態を取得する操作です。

- **例**: `find_by_id()`, `find_by_author_id()`
- **特徴**: 副作用がない（状態を変更しない）

### 分離の例

```python
class PostRepository(ABC):
    """投稿リポジトリのインターフェース"""
    
    # コマンド（状態を変更）
    @abstractmethod
    def save(self, post):
        """投稿を保存"""
        pass
    
    @abstractmethod
    def delete(self, post_id):
        """投稿を削除"""
        pass
    
    # クエリ（状態を取得）
    @abstractmethod
    def find_by_id(self, post_id):
        """IDで投稿を取得"""
        pass
    
    @abstractmethod
    def find_by_author_id(self, author_id):
        """作成者IDで投稿を取得"""
        pass
```

## UserRepositoryの例

### インターフェース

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
    
    @abstractmethod
    def delete(self, user_id):
        """ユーザーを削除"""
        pass
```

### 実装

```python
class UserRepositoryImpl(UserRepository):
    """ユーザーリポジトリの実装（データベース）"""
    
    def __init__(self, db):
        self.db = db
    
    def save(self, user):
        """ユーザーを保存"""
        self.db.execute(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE name = ?, email = ?",
            user.user_id, user.name, user.email.value, user.name, user.email.value
        )
    
    def find_by_id(self, user_id):
        """IDでユーザーを取得"""
        row = self.db.execute(
            "SELECT * FROM users WHERE id = ?",
            user_id
        ).fetchone()
        
        if not row:
            return None
        
        return User(
            user_id=row['id'],
            name=row['name'],
            email=Email(row['email'])
        )
    
    def find_by_email(self, email):
        """メールアドレスでユーザーを取得"""
        row = self.db.execute(
            "SELECT * FROM users WHERE email = ?",
            email.value
        ).fetchone()
        
        if not row:
            return None
        
        return User(
            user_id=row['id'],
            name=row['name'],
            email=Email(row['email'])
        )
    
    def delete(self, user_id):
        """ユーザーを削除"""
        self.db.execute("DELETE FROM users WHERE id = ?", user_id)
```

## リポジトリの設計原則

### 原則1: 集約単位でリポジトリを作成

**理由**: リポジトリは集約の永続化を担当するため、集約単位で作成します。

```python
# ✅ 良い例: 集約単位でリポジトリを作成
class PostRepository(ABC):
    """Post集約のリポジトリ"""
    pass

class UserRepository(ABC):
    """User集約のリポジトリ"""
    pass

# ❌ 悪い例: 集約を跨いでリポジトリを作成
class SocialMediaRepository(ABC):
    """すべての集約を含むリポジトリ（避けるべき）"""
    pass
```

### 原則2: インターフェースと実装を分離

**理由**: テストの容易さと、永続化の変更が容易になるため。

```python
# ✅ 良い例: インターフェースと実装を分離
class PostRepository(ABC):
    """インターフェース"""
    pass

class PostRepositoryImpl(PostRepository):
    """実装（データベース）"""
    pass

class InMemoryPostRepository(PostRepository):
    """実装（メモリ、テスト用）"""
    pass
```

### 原則3: クエリとコマンドを分離

**理由**: クエリとコマンドの責任を明確にし、テストと保守を容易にするため。

```python
# ✅ 良い例: クエリとコマンドを分離
class PostRepository(ABC):
    # コマンド
    @abstractmethod
    def save(self, post):
        pass
    
    # クエリ
    @abstractmethod
    def find_by_id(self, post_id):
        pass
```

## よくある間違い

### 間違い1: リポジトリにビジネスロジックを含める

```python
# ❌ 悪い例: リポジトリにビジネスロジックを含める
class PostRepository:
    def save(self, post):
        # ビジネスロジック: 投稿の文字数制限
        if len(post.content) > 1000:
            raise ValueError("Post content too long")
        # データベースに保存
        self.db.save(post)

# ✅ 良い例: ビジネスロジックはドメインモデルに
class Post:
    def __init__(self, post_id, author_id, content):
        # ビジネスロジック: 投稿の文字数制限
        self.content = PostContent(content)  # PostContentが検証する

class PostRepository:
    def save(self, post):
        # データベースに保存（ビジネスロジックは含まない）
        self.db.save(post)
```

### 間違い2: リポジトリで集約を跨いでアクセス

```python
# ❌ 悪い例: リポジトリで集約を跨いでアクセス
class PostRepository:
    def find_with_author(self, post_id):
        # 問題: User集約にアクセスしている
        post = self.find_by_id(post_id)
        user = self.user_repository.find_by_id(post.author_id)
        post.author = user  # 集約間で直接参照
        return post

# ✅ 良い例: 集約間の参照はIDで行う
class PostRepository:
    def find_by_id(self, post_id):
        # 集約間の参照はIDで行う
        post = self.find_by_id(post_id)
        # post.author_id を使用（Userオブジェクトは含まない）
        return post
```

### 間違い3: リポジトリで複雑なクエリを実装

```python
# ❌ 悪い例: リポジトリで複雑なクエリを実装
class PostRepository:
    def find_popular_posts(self, min_likes, min_comments):
        # 問題: 複雑なクエリがリポジトリに含まれる
        return self.db.execute(
            """
            SELECT p.* FROM posts p
            LEFT JOIN likes l ON p.id = l.post_id
            LEFT JOIN comments c ON p.id = c.post_id
            GROUP BY p.id
            HAVING COUNT(DISTINCT l.user_id) >= ? AND COUNT(DISTINCT c.id) >= ?
            ORDER BY COUNT(DISTINCT l.user_id) DESC
            """,
            min_likes, min_comments
        ).fetchall()

# ✅ 良い例: 複雑なクエリはクエリサービスに分離
class PostQueryService:
    """投稿クエリサービス（読み取り専用）"""
    def find_popular_posts(self, min_likes, min_comments):
        # 複雑なクエリはクエリサービスに
        pass

class PostRepository:
    """投稿リポジトリ（集約の永続化のみ）"""
    def find_by_id(self, post_id):
        # シンプルなクエリのみ
        pass
```

## まとめ

- **リポジトリ**は、集約の永続化を抽象化するオブジェクト
- **インターフェースと実装を分離**: テストの容易さと、永続化の変更が容易になる
- **集約単位でリポジトリを作成**: リポジトリは集約の永続化を担当
- **クエリとコマンドを分離**: 責任を明確にし、テストと保守を容易にする
- **ビジネスロジックは含めない**: リポジトリは永続化のみを担当

## 考えてみよう

1. あなたのプロジェクトで、リポジトリパターンを使用していますか？
2. リポジトリにビジネスロジックが含まれている箇所はありますか？
3. テストでメモリ上のリポジトリを使用していますか？

次の章では、**ドメインサービス**について詳しく学びます。

