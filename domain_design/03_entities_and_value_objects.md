# 03. エンティティと値オブジェクト - ドメインモデルの基本要素

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- エンティティの特徴（同一性を持つ）
- 値オブジェクトの特徴（値で識別）
- エンティティと値オブジェクトの違い
- いつエンティティを使い、いつ値オブジェクトを使うか
- 実装コード例

## エンティティと値オブジェクトの違い

DDDでは、ドメインモデルを構成する要素を**エンティティ**と**値オブジェクト**に分類します。

### エンティティ（Entity）

**エンティティ**は、**同一性（ID）を持つ**オブジェクトです。

- **特徴**: IDが同じなら、内容が変わっても同じオブジェクト
- **例**: `User`（ユーザーIDで識別）、`Post`（投稿IDで識別）

### 値オブジェクト（Value Object）

**値オブジェクト**は、**値で識別**されるオブジェクトです。

- **特徴**: 値が同じなら、同じオブジェクトとみなす
- **例**: `Email`（メールアドレスの値で識別）、`PostContent`（内容の値で識別）

## エンティティの詳細

### エンティティの特徴

1. **同一性を持つ**: IDで識別される
2. **可変**: 内容を変更できる
3. **ライフサイクル**: 作成、変更、削除される

### エンティティの例: User（ユーザー）

```python
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id  # 同一性（ID）
        self.name = name
        self.email = email
    
    def change_name(self, new_name):
        # エンティティは可変: 名前を変更できる
        self.name = new_name
    
    def change_email(self, new_email):
        # エンティティは可変: メールアドレスを変更できる
        self.email = new_email
    
    def __eq__(self, other):
        # 同一性で比較: IDが同じなら同じオブジェクト
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id
```

**重要なポイント**:
- `user_id`が同じなら、`name`や`email`が変わっても同じユーザー
- 例: ユーザーIDが`123`のユーザーが名前を「田中」から「佐藤」に変更しても、同じユーザー（ID: 123）

### エンティティの例: Post（投稿）

```python
class Post:
    def __init__(self, post_id, author, content):
        self.post_id = post_id  # 同一性（ID）
        self.author = author
        self.content = content
        self.created_at = datetime.now()
    
    def update_content(self, new_content):
        # エンティティは可変: 内容を変更できる
        self.content = new_content
    
    def __eq__(self, other):
        # 同一性で比較: IDが同じなら同じオブジェクト
        if not isinstance(other, Post):
            return False
        return self.post_id == other.post_id
```

**重要なポイント**:
- `post_id`が同じなら、`content`が変わっても同じ投稿
- 例: 投稿IDが`456`の投稿が内容を「今日はいい天気」から「今日は雨」に変更しても、同じ投稿（ID: 456）

## 値オブジェクトの詳細

### 値オブジェクトの特徴

1. **値で識別**: 値が同じなら同じオブジェクト
2. **不変**: 内容を変更できない（変更する場合は新しいオブジェクトを作成）
3. **交換可能**: 値が同じなら、どのインスタンスでも同じ

### 値オブジェクトの例: Email（メールアドレス）

```python
class Email:
    def __init__(self, value):
        # バリデーション
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self._value = value  # 不変: 直接変更できない
    
    def _is_valid(self, value):
        # メールアドレスの形式を検証
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, value) is not None
    
    @property
    def value(self):
        return self._value
    
    def __eq__(self, other):
        # 値で比較: 値が同じなら同じオブジェクト
        if not isinstance(other, Email):
            return False
        return self._value == other._value
    
    def __hash__(self):
        # ハッシュ値も値に基づく
        return hash(self._value)
    
    def __str__(self):
        return self._value
```

**重要なポイント**:
- 値が同じなら、どのインスタンスでも同じ
- 例: `Email("user@example.com")`と`Email("user@example.com")`は同じ
- 不変: 一度作成したら変更できない

### 値オブジェクトの例: PostContent（投稿内容）

```python
class PostContent:
    def __init__(self, value):
        # バリデーション
        if not value or len(value) == 0:
            raise ValueError("Post content cannot be empty")
        if len(value) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        self._value = value  # 不変: 直接変更できない
    
    @property
    def value(self):
        return self._value
    
    @property
    def length(self):
        return len(self._value)
    
    def __eq__(self, other):
        # 値で比較: 値が同じなら同じオブジェクト
        if not isinstance(other, PostContent):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)
    
    def __str__(self):
        return self._value
```

**重要なポイント**:
- 値が同じなら、どのインスタンスでも同じ
- 例: `PostContent("Hello")`と`PostContent("Hello")`は同じ
- 不変: 一度作成したら変更できない（変更する場合は新しいオブジェクトを作成）

### 値オブジェクトの例: LikeCount（いいね数）

```python
class LikeCount:
    def __init__(self, value):
        # バリデーション
        if value < 0:
            raise ValueError("Like count cannot be negative")
        self._value = value  # 不変: 直接変更できない
    
    @property
    def value(self):
        return self._value
    
    def increment(self):
        # 不変: 新しいオブジェクトを返す
        return LikeCount(self._value + 1)
    
    def decrement(self):
        # 不変: 新しいオブジェクトを返す（0未満にはならない）
        if self._value == 0:
            return self
        return LikeCount(self._value - 1)
    
    def __eq__(self, other):
        # 値で比較: 値が同じなら同じオブジェクト
        if not isinstance(other, LikeCount):
            return False
        return self._value == other._value
    
    def __hash__(self):
        return hash(self._value)
    
    def __str__(self):
        return str(self._value)
```

**重要なポイント**:
- 値が同じなら、どのインスタンスでも同じ
- 不変: `increment()`や`decrement()`は新しいオブジェクトを返す
- 例: `LikeCount(5).increment()`は`LikeCount(6)`を返す（元のオブジェクトは変更されない）

## エンティティと値オブジェクトの使い分け

### 判断基準

以下の質問に答えることで、エンティティか値オブジェクトかを判断できます：

1. **同一性が必要か？**: IDで識別する必要があるか？
2. **変更可能か？**: 内容を変更する必要があるか？
3. **交換可能か？**: 値が同じなら、どのインスタンスでも同じでよいか？

### 判断フローチャート

```
オブジェクトを設計する
    ↓
同一性（ID）が必要か？
    ↓ YES
    ↓
内容を変更する必要があるか？
    ↓ YES
    ↓
→ エンティティ

    ↓ NO
    ↓
→ 値オブジェクト（不変）
```

### 具体例での判断

#### 例1: User（ユーザー）

- **同一性が必要か？**: はい（ユーザーIDで識別）
- **変更可能か？**: はい（名前やメールアドレスを変更できる）
- **→ エンティティ**

#### 例2: Email（メールアドレス）

- **同一性が必要か？**: いいえ（値で識別）
- **変更可能か？**: いいえ（変更する場合は新しいオブジェクトを作成）
- **→ 値オブジェクト**

#### 例3: Post（投稿）

- **同一性が必要か？**: はい（投稿IDで識別）
- **変更可能か？**: はい（内容を変更できる）
- **→ エンティティ**

#### 例4: PostContent（投稿内容）

- **同一性が必要か？**: いいえ（値で識別）
- **変更可能か？**: いいえ（変更する場合は新しいオブジェクトを作成）
- **→ 値オブジェクト**

## エンティティと値オブジェクトの組み合わせ

エンティティは、値オブジェクトを含むことができます。

### 例: UserエンティティにEmail値オブジェクトを含める

```python
class Email:
    # 値オブジェクト（前の例と同じ）
    def __init__(self, value):
        if not self._is_valid(value):
            raise ValueError(f"Invalid email: {value}")
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self._value == other._value

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id  # エンティティの同一性
        self.name = name
        self.email = Email(email)  # 値オブジェクトを含む
    
    def change_email(self, new_email):
        # 新しいEmail値オブジェクトを作成
        self.email = Email(new_email)
```

**重要なポイント**:
- `User`はエンティティ（IDで識別）
- `Email`は値オブジェクト（値で識別）
- エンティティは値オブジェクトを含むことができる

### 例: PostエンティティにPostContent値オブジェクトを含める

```python
class PostContent:
    # 値オブジェクト（前の例と同じ）
    def __init__(self, value):
        if not value or len(value) == 0:
            raise ValueError("Post content cannot be empty")
        if len(value) > 1000:
            raise ValueError("Post content cannot exceed 1000 characters")
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    def __eq__(self, other):
        if not isinstance(other, PostContent):
            return False
        return self._value == other._value

class Post:
    def __init__(self, post_id, author, content):
        self.post_id = post_id  # エンティティの同一性
        self.author = author
        self.content = PostContent(content)  # 値オブジェクトを含む
    
    def update_content(self, new_content):
        # 新しいPostContent値オブジェクトを作成
        self.content = PostContent(new_content)
```

**重要なポイント**:
- `Post`はエンティティ（IDで識別）
- `PostContent`は値オブジェクト（値で識別）
- エンティティは値オブジェクトを含むことができる

## よくある間違い

### 間違い1: 値オブジェクトを可変にする

```python
# ❌ 悪い例: 値オブジェクトを可変にする
class Email:
    def __init__(self, value):
        self.value = value  # 直接変更可能
    
    def change(self, new_value):
        self.value = new_value  # 変更してしまう

# ✅ 良い例: 値オブジェクトを不変にする
class Email:
    def __init__(self, value):
        self._value = value  # プライベート
    
    @property
    def value(self):
        return self._value  # 読み取り専用
```

### 間違い2: エンティティを値で比較する

```python
# ❌ 悪い例: エンティティを値で比較する
class User:
    def __eq__(self, other):
        return self.name == other.name and self.email == other.email  # 値で比較

# ✅ 良い例: エンティティをIDで比較する
class User:
    def __eq__(self, other):
        return self.user_id == other.user_id  # IDで比較
```

### 間違い3: 値オブジェクトにIDを付ける

```python
# ❌ 悪い例: 値オブジェクトにIDを付ける
class Email:
    def __init__(self, email_id, value):
        self.email_id = email_id  # IDは不要
        self.value = value

# ✅ 良い例: 値オブジェクトは値で識別
class Email:
    def __init__(self, value):
        self._value = value  # IDは不要
```

## まとめ

- **エンティティ**は、同一性（ID）を持つオブジェクト
- **値オブジェクト**は、値で識別されるオブジェクト
- **エンティティ**は可変、**値オブジェクト**は不変
- **エンティティ**は値オブジェクトを含むことができる
- **判断基準**: 同一性が必要か、変更可能か、交換可能か

## 考えてみよう

1. あなたのプロジェクトで、エンティティと値オブジェクトを区別していますか？
2. 値オブジェクトを不変にしていますか？
3. エンティティをIDで比較していますか？

次の章では、**集約**について詳しく学びます。

