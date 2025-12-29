# 09. ベストプラクティス - 実践的な知見とよくある落とし穴

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- よくある間違いとその回避方法
- 集約を小さく保つ重要性
- ドメインロジックをアプリケーション層に漏らさない
- テストの書き方（ドメインモデルのテスト）
- リファクタリングの指針

## よくある間違いとその回避方法

### 間違い1: 集約が大きすぎる

#### 問題

```python
# ❌ 悪い例: 集約が大きすぎる
class User:
    """ユーザー集約（大きすぎる）"""
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._posts = []        # すべての投稿
        self._comments = []      # すべてのコメント
        self._likes = []         # すべてのいいね
        self._following = []    # フォローしているユーザー
        self._followers = []    # フォロワー
        # 問題: 集約が大きすぎる
```

**問題点**:
- 整合性を保ちにくい
- パフォーマンスが悪い
- テストが困難

#### 解決方法

```python
# ✅ 良い例: 集約を小さく保つ
class User:
    """ユーザー集約（小さい）"""
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._following = []  # フォローしているユーザーのIDのみ

class Post:
    """投稿集約（小さい）"""
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self._comments = []  # この投稿のコメントのみ
        self._likes = []     # この投稿のいいねのみ
```

**改善点**:
- 集約を小さく保つ
- 各集約が明確な責任を持つ
- 整合性を保ちやすい

### 間違い2: ドメインロジックをアプリケーション層に漏らす

#### 問題

```python
# ❌ 悪い例: ドメインロジックをアプリケーション層に漏らす
class PostApplicationService:
    def create_post(self, user_id, content):
        # 問題: ビジネスロジックがアプリケーション層にある
        if not content or len(content) == 0:
            raise ValueError("Post content cannot be empty")
        if len(content) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        
        post = Post(post_id=generate_id(), author_id=user_id, content=content)
        self.post_repository.save(post)
        return post
```

**問題点**:
- ビジネスロジックがアプリケーション層に散在
- ドメインモデルが貧血症（Anemic Domain Model）になる
- ビジネスルールの変更が困難

#### 解決方法

```python
# ✅ 良い例: ドメインロジックをドメインモデルに配置
class PostContent:
    """投稿内容（値オブジェクト）"""
    def __init__(self, value):
        # ビジネスロジックを値オブジェクトに配置
        if not value or len(value) == 0:
            raise ValueError("Post content cannot be empty")
        if len(value) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        self._value = value

class PostApplicationService:
    def create_post(self, user_id, content):
        # ドメインロジックはドメインモデルに委譲
        post = Post(
            post_id=generate_id(),
            author_id=user_id,
            content=PostContent(content)  # PostContentが検証する
        )
        self.post_repository.save(post)
        return post
```

**改善点**:
- ビジネスロジックをドメインモデルに配置
- ドメインモデルが豊富（Rich Domain Model）になる
- ビジネスルールの変更が容易

### 間違い3: 集約間で直接オブジェクトを参照

#### 問題

```python
# ❌ 悪い例: 集約間で直接オブジェクトを参照
class Post:
    def __init__(self, post_id, author, content):
        self.author = author  # Userオブジェクトを直接参照
        # 問題: 集約間の結合が強い
```

**問題点**:
- 集約間の結合が強い
- 変更の影響が広範囲に及ぶ
- 整合性の境界が曖昧

#### 解決方法

```python
# ✅ 良い例: 集約間の参照はIDで行う
class Post:
    def __init__(self, post_id, author_id, content):
        self.author_id = author_id  # UserのIDを参照
        # 良い: 集約間の結合が弱い
```

**改善点**:
- 集約間の結合が弱い
- 変更の影響が限定的
- 整合性の境界が明確

### 間違い4: 値オブジェクトを可変にする

#### 問題

```python
# ❌ 悪い例: 値オブジェクトを可変にする
class Email:
    def __init__(self, value):
        self.value = value  # 直接変更可能
    
    def change(self, new_value):
        self.value = new_value  # 変更してしまう
```

**問題点**:
- 値オブジェクトの不変性が保証されない
- 予期しない変更が発生する可能性がある

#### 解決方法

```python
# ✅ 良い例: 値オブジェクトを不変にする
class Email:
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self._value = value  # プライベート
    
    @property
    def value(self):
        return self._value  # 読み取り専用
```

**改善点**:
- 値オブジェクトの不変性が保証される
- 予期しない変更が発生しない

### 間違い5: リポジトリにビジネスロジックを含める

#### 問題

```python
# ❌ 悪い例: リポジトリにビジネスロジックを含める
class PostRepository:
    def save(self, post):
        # 問題: ビジネスロジックがリポジトリにある
        if len(post.content) > 1000:
            raise ValueError("Post content too long")
        self.db.save(post)
```

**問題点**:
- リポジトリの責任が曖昧
- ビジネスロジックが散在

#### 解決方法

```python
# ✅ 良い例: ビジネスロジックはドメインモデルに
class PostContent:
    def __init__(self, value):
        # ビジネスロジックを値オブジェクトに配置
        if len(value) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        self._value = value

class PostRepository:
    def save(self, post):
        # リポジトリは永続化のみを担当
        self.db.save(post)
```

**改善点**:
- リポジトリの責任が明確
- ビジネスロジックがドメインモデルに集約

## 集約を小さく保つ重要性

### なぜ集約を小さく保つべきか

1. **整合性を保ちやすい**: 小さな集約は、整合性を保ちやすい
2. **パフォーマンスが良い**: 小さな集約は、読み込み・保存が高速
3. **テストが容易**: 小さな集約は、テストが書きやすい
4. **変更が容易**: 小さな集約は、変更の影響が限定的

### 集約のサイズの判断基準

以下の質問に答えることで、集約のサイズを判断できます：

1. **整合性の境界は明確か？**: 集約内のオブジェクトが、明確な整合性の境界を持っているか？
2. **トランザクションの単位は適切か？**: 集約全体を1つのトランザクションで保存・取得できるか？
3. **パフォーマンスは許容範囲内か？**: 集約の読み込み・保存が許容範囲内か？

### 集約を小さく保つ方法

1. **関連オブジェクトを別の集約にする**: 関連が弱いオブジェクトは、別の集約にする
2. **集約間の参照はIDで行う**: 集約間で直接オブジェクトを参照しない
3. **不変条件を最小限に**: 不変条件を最小限に保つ

## ドメインロジックをアプリケーション層に漏らさない

### 貧血症ドメインモデル（Anemic Domain Model）

**貧血症ドメインモデル**は、データとロジックが分離されたドメインモデルです。

```python
# ❌ 悪い例: 貧血症ドメインモデル
class Post:
    """投稿（データのみ）"""
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        # 問題: ロジックがない

class PostService:
    """投稿サービス（ロジックがここにある）"""
    def add_like(self, post, user_id):
        # 問題: ビジネスロジックがサービス層にある
        if user_id in post.likes:
            raise ValueError("User has already liked this post")
        post.likes.append(user_id)
```

**問題点**:
- ビジネスロジックがサービス層に散在
- ドメインモデルがデータの入れ物になる
- ビジネスルールの変更が困難

### 豊富なドメインモデル（Rich Domain Model）

**豊富なドメインモデル**は、データとロジックが一緒に配置されたドメインモデルです。

```python
# ✅ 良い例: 豊富なドメインモデル
class Post:
    """投稿（データとロジック）"""
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id
        self.content = PostContent(content)
        self._likes = []
    
    def add_like(self, user_id):
        # 良い: ビジネスロジックがドメインモデルにある
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        self._likes.append(Like(user_id))
    
    def has_liked(self, user_id):
        return any(l.user_id == user_id for l in self._likes)
```

**改善点**:
- ビジネスロジックがドメインモデルに集約
- ドメインモデルがビジネスの意図を表現
- ビジネスルールの変更が容易

## テストの書き方（ドメインモデルのテスト）

### ドメインモデルのテスト

ドメインモデルのテストは、**データベースや外部依存なし**で実行できる必要があります。

```python
def test_post_add_like():
    """投稿へのいいね追加のテスト"""
    # ドメインモデルのテスト（データベース不要）
    post = Post(
        post_id="123",
        author_id="456",
        content="Hello, world!"
    )
    
    # いいねを追加
    post.add_like("789")
    
    # 検証
    assert post.has_liked("789")
    assert post.get_like_count() == 1

def test_post_add_like_duplicate():
    """重複いいねのテスト"""
    post = Post(
        post_id="123",
        author_id="456",
        content="Hello, world!"
    )
    
    # いいねを追加
    post.add_like("789")
    
    # 重複いいねはエラー
    with pytest.raises(ValueError, match="User has already liked this post"):
        post.add_like("789")
```

### リポジトリのテスト

リポジトリのテストは、**メモリ上のリポジトリ**を使用します。

```python
def test_post_repository_save_and_find():
    """投稿リポジトリの保存と取得のテスト"""
    # メモリ上のリポジトリを使用（データベース不要）
    repository = InMemoryPostRepository()
    
    # 投稿を作成
    post = Post(
        post_id="123",
        author_id="456",
        content="Hello, world!"
    )
    
    # 保存
    repository.save(post)
    
    # 取得
    retrieved_post = repository.find_by_id("123")
    
    # 検証
    assert retrieved_post is not None
    assert retrieved_post.post_id == "123"
    assert retrieved_post.content.value == "Hello, world!"
```

### ドメインサービスのテスト

ドメインサービスのテストは、**メモリ上のリポジトリ**を使用します。

```python
def test_timeline_service_generate_home_timeline():
    """タイムラインサービスのホームタイムライン生成のテスト"""
    # メモリ上のリポジトリを使用
    post_repository = InMemoryPostRepository()
    timeline_service = TimelineService(post_repository)
    
    # ユーザーを作成
    user = User(user_id="123", name="Alice", email="alice@example.com")
    user.follow("456")
    
    # 投稿を作成
    post1 = Post(post_id="789", author_id="456", content="Post 1")
    post2 = Post(post_id="790", author_id="456", content="Post 2")
    post_repository.save(post1)
    post_repository.save(post2)
    
    # タイムラインを生成
    timeline = timeline_service.generate_home_timeline(user)
    
    # 検証
    assert len(timeline) == 2
    assert timeline[0].post_id == "790"  # 新しい投稿が先
    assert timeline[1].post_id == "789"
```

## リファクタリングの指針

### リファクタリングのタイミング

1. **ビジネスロジックがアプリケーション層に漏れている**: ドメインモデルに移動
2. **集約が大きすぎる**: 小さな集約に分割
3. **集約間で直接オブジェクトを参照している**: ID参照に変更
4. **値オブジェクトが可変になっている**: 不変にする

### リファクタリングの手順

1. **現状を理解する**: 現在のコードの問題点を特定
2. **目標を設定する**: リファクタリング後の目標を設定
3. **小さく変更する**: 大きな変更を避け、小さな変更を繰り返す
4. **テストを書く**: リファクタリング前後でテストを実行
5. **検証する**: リファクタリング後の動作を検証

### リファクタリングの例

#### 例1: ビジネスロジックをドメインモデルに移動

```python
# リファクタリング前
class PostApplicationService:
    def add_like(self, post, user_id):
        if user_id in post.likes:
            raise ValueError("User has already liked this post")
        post.likes.append(user_id)

# リファクタリング後
class Post:
    def add_like(self, user_id):
        if self.has_liked(user_id):
            raise ValueError("User has already liked this post")
        self._likes.append(Like(user_id))
```

#### 例2: 集約を小さく分割

```python
# リファクタリング前
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self._posts = []  # すべての投稿

# リファクタリング後
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        # 投稿は別の集約に

class Post:
    def __init__(self, post_id, author_id, content):
        self.post_id = post_id
        self.author_id = author_id  # UserのIDを参照
        self.content = content
```

## まとめ

- **集約を小さく保つ**: 整合性を保ちやすく、パフォーマンスも良い
- **ドメインロジックをドメインモデルに配置**: 貧血症ドメインモデルを避ける
- **集約間の参照はIDで行う**: 結合を弱め、変更の影響を最小限に
- **値オブジェクトを不変にする**: 予期しない変更を防ぐ
- **リポジトリにビジネスロジックを含めない**: リポジトリは永続化のみを担当
- **テストを書く**: ドメインモデル、リポジトリ、ドメインサービスのテストを書く
- **リファクタリングを継続する**: 小さな変更を繰り返し、コードを改善する

## 考えてみよう

1. あなたのプロジェクトで、集約が大きすぎる箇所はありますか？
2. ドメインロジックがアプリケーション層に漏れている箇所はありますか？
3. 値オブジェクトが可変になっている箇所はありますか？
4. ドメインモデルのテストを書いていますか？

---

**おめでとうございます！** この解説書を最後まで読了しました。DDDの核心概念を理解し、実践的な設計ができるようになったはずです。

実際のプロジェクトで、これらの概念を適用してみてください。最初は完璧でなくても構いません。小さな変更を繰り返し、継続的に改善していくことが重要です。

