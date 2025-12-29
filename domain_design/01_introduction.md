# 01. イントロダクション - Domain-Driven Designとは何か

## この章の学習目標

この章を読むことで、以下を理解できるようになります：

- DDDとは何か、なぜ重要か
- 従来のアプローチとの違い
- DDDの基本用語
- ソーシャルメディアでの問題提起を通じたDDDの必要性

## DDDとは何か

**Domain-Driven Design（ドメイン駆動設計）**は、Eric Evansが2003年に提唱した、複雑なビジネスロジックを持つソフトウェアを設計するためのアプローチです。

### 定義

> **Domain-Driven Design**は、ソフトウェアの設計を**ドメイン（ビジネスの領域）**と**ドメインモデル**を中心に据える設計手法です。

### 3つの核心原則

1. **ドメインが最も重要**: 技術的な詳細よりも、ビジネスの問題解決を優先する
2. **ドメインエキスパートと協働**: ビジネスの専門家と開発者が密接に協力する
3. **モデルがコードを駆動**: ドメインモデルが実装の指針となる

## なぜDDDが重要か

### 従来のアプローチの問題点

従来のアプローチでは、以下のような問題が発生しがちです：

#### 問題1: データ中心設計

```python
# ❌ 悪い例: データ構造だけを考える
class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

# ビジネスロジックが散在
def create_post(user_id, content):
    # 投稿作成のロジックがここに...
    pass

def like_post(user_id, post_id):
    # いいねのロジックが別の場所に...
    pass
```

**問題点**:
- ビジネスルールがコードのあちこちに散在
- データとロジックが分離されている
- ビジネスの意図がコードから読み取れない

#### 問題2: アノミー（用語の不統一）

```python
# 開発者Aのコード
def create_message(user_id, text):
    # "message"という用語を使用
    pass

# 開発者Bのコード
def add_post(user_id, content):
    # "post"という用語を使用（同じものを指している）
    pass

# 開発者Cのコード
def publish_article(user_id, body):
    # "article"という用語を使用（これも同じもの）
    pass
```

**問題点**:
- 同じ概念に対して異なる用語が使われる
- ドメインエキスパートと開発者の間で用語が一致しない
- コードレビューや会議で混乱が生じる

#### 問題3: 技術的な詳細がドメインロジックを汚染

```python
# ❌ 悪い例: データベースの詳細がドメインロジックに混在
def follow_user(follower_id, followee_id):
    # SQLの詳細が混在
    query = "INSERT INTO follows (follower_id, followee_id) VALUES (?, ?)"
    db.execute(query, follower_id, followee_id)
    
    # ビジネスルール: 自分自身をフォローできない
    if follower_id == followee_id:
        raise ValueError("Cannot follow yourself")
    
    # またSQL...
    query = "SELECT COUNT(*) FROM follows WHERE follower_id = ?"
    # ...
```

**問題点**:
- データベースの詳細がビジネスロジックに混在
- テストが困難（データベースが必要）
- ビジネスルールの変更が技術的な変更と混同される

### DDDによる解決

DDDは、これらの問題を以下のように解決します：

1. **ドメインモデルにビジネスロジックを集約**: データとロジックを一緒に配置
2. **ユビキタス言語の確立**: ドメインエキスパートと開発者が同じ言葉を使う
3. **技術的な詳細の分離**: ドメインロジックとインフラストラクチャを分離

## ソーシャルメディアでの問題提起

実際のソーシャルメディアアプリケーションを例に、DDDの必要性を理解しましょう。

### シナリオ: ソーシャルメディアアプリの開発

あなたは、新しいソーシャルメディアアプリを開発することになりました。以下の機能が必要です：

- ユーザーが投稿を作成できる
- ユーザーが他のユーザーをフォローできる
- フォローしているユーザーの投稿がタイムラインに表示される
- 投稿にいいねができる
- 投稿にコメントができる

### 従来のアプローチでの実装

```python
# データベーススキーマ（テーブル定義）
# users テーブル: id, name, email
# posts テーブル: id, user_id, content, created_at
# follows テーブル: follower_id, followee_id
# likes テーブル: user_id, post_id
# comments テーブル: id, post_id, user_id, content

# サービス層（ビジネスロジックが散在）
class PostService:
    def create_post(self, user_id, content):
        # バリデーション
        if not content or len(content) > 1000:
            raise ValueError("Invalid content")
        
        # データベースに保存
        post_id = db.execute(
            "INSERT INTO posts (user_id, content) VALUES (?, ?)",
            user_id, content
        )
        return post_id
    
    def like_post(self, user_id, post_id):
        # 重複チェック
        existing = db.execute(
            "SELECT * FROM likes WHERE user_id = ? AND post_id = ?",
            user_id, post_id
        )
        if existing:
            raise ValueError("Already liked")
        
        # いいねを保存
        db.execute(
            "INSERT INTO likes (user_id, post_id) VALUES (?, ?)",
            user_id, post_id
        )
        
        # いいね数を更新
        db.execute(
            "UPDATE posts SET like_count = like_count + 1 WHERE id = ?",
            post_id
        )

class FollowService:
    def follow_user(self, follower_id, followee_id):
        # 自分自身をフォローできない
        if follower_id == followee_id:
            raise ValueError("Cannot follow yourself")
        
        # 既にフォローしているかチェック
        existing = db.execute(
            "SELECT * FROM follows WHERE follower_id = ? AND followee_id = ?",
            follower_id, followee_id
        )
        if existing:
            raise ValueError("Already following")
        
        # フォロー関係を保存
        db.execute(
            "INSERT INTO follows (follower_id, followee_id) VALUES (?, ?)",
            follower_id, followee_id
        )

class TimelineService:
    def get_timeline(self, user_id):
        # フォローしているユーザーを取得
        following = db.execute(
            "SELECT followee_id FROM follows WHERE follower_id = ?",
            user_id
        )
        following_ids = [row['followee_id'] for row in following]
        
        # フォローしているユーザーの投稿を取得
        posts = db.execute(
            "SELECT * FROM posts WHERE user_id IN (?) ORDER BY created_at DESC LIMIT 20",
            following_ids
        )
        
        return posts
```

### このアプローチの問題点

1. **ビジネスルールが散在**: 「自分自身をフォローできない」というルールが`FollowService`に、「投稿の文字数制限」が`PostService`にある
2. **用語の不統一**: 「post」「message」「article」など、同じ概念に対して異なる用語が使われる可能性
3. **テストが困難**: データベースが必要で、単体テストが書きにくい
4. **変更が困難**: ビジネスルールを変更する際に、複数のサービスを修正する必要がある

### DDDアプローチでの改善（予告）

後の章で詳しく学びますが、DDDでは以下のように改善されます：

```python
# ドメインモデル（ビジネスロジックが集約）
class User:
    def follow(self, other_user):
        # ビジネスルール: 自分自身をフォローできない
        if self.id == other_user.id:
            raise ValueError("Cannot follow yourself")
        # フォロー関係を管理
        self._following.add(other_user.id)

class Post:
    def __init__(self, author, content):
        # ビジネスルール: 投稿内容の検証
        if not content or len(content) > 1000:
            raise ValueError("Invalid content")
        self.author = author
        self.content = content
        self._likes = set()
    
    def like(self, user):
        # ビジネスルール: 重複いいねを防ぐ
        if user.id in self._likes:
            raise ValueError("Already liked")
        self._likes.add(user.id)
```

**改善点**:
- ビジネスロジックがドメインモデルに集約されている
- データとロジックが一緒に配置されている
- ビジネスの意図がコードから読み取れる

## DDDの基本用語

この解説書で頻繁に登場する用語を理解しましょう。

### ドメイン（Domain）

**ドメイン**は、ビジネスの領域、問題領域を指します。

- **例**: ソーシャルメディア、eコマース、銀行システム
- **特徴**: ビジネスの専門知識が必要な領域

### モデル（Model）

**モデル**は、ドメインを抽象化した表現です。

- **例**: 「ユーザーが投稿を作成する」という現実を、`User`と`Post`というクラスで表現
- **特徴**: 現実の複雑さを簡略化し、重要な部分だけを表現

### ユビキタス言語（Ubiquitous Language）

**ユビキタス言語**は、ドメインエキスパートと開発者が共有する共通言語です。

- **例**: 「投稿」という用語を、コード、ドキュメント、会議で一貫して使用
- **特徴**: 同じ概念に対して常に同じ用語を使う

### エンティティ（Entity）

**エンティティ**は、同一性（ID）を持つオブジェクトです。

- **例**: `User`（ユーザーIDで識別）、`Post`（投稿IDで識別）
- **特徴**: IDが同じなら、内容が変わっても同じオブジェクト

### 値オブジェクト（Value Object）

**値オブジェクト**は、値で識別されるオブジェクトです。

- **例**: `Email`（メールアドレスの値で識別）、`PostContent`（内容の値で識別）
- **特徴**: 値が同じなら、同じオブジェクトとみなす

### 集約（Aggregate）

**集約**は、整合性の境界を持つオブジェクトのグループです。

- **例**: `Post`集約（`Post` + `Comment` + `Like`）
- **特徴**: 集約内の整合性を保証する

### リポジトリ（Repository）

**リポジトリ**は、集約の永続化を抽象化するオブジェクトです。

- **例**: `PostRepository`（投稿の保存・取得を抽象化）
- **特徴**: データベースの詳細を隠蔽

### ドメインサービス（Domain Service）

**ドメインサービス**は、エンティティや値オブジェクトに属さないドメインロジックです。

- **例**: `TimelineService`（タイムライン生成ロジック）
- **特徴**: 複数の集約にまたがるロジックを扱う

### 境界づけられたコンテキスト（Bounded Context）

**境界づけられたコンテキスト**は、モデルが有効な明確な境界です。

- **例**: 「ユーザー管理コンテキスト」と「投稿管理コンテキスト」
- **特徴**: 異なるコンテキストでは、同じ用語でも意味が異なる場合がある

## DDDの適用範囲

### DDDが有効な場合

- **複雑なビジネスロジック**がある
- **ドメインエキスパート**が存在する
- **長期的なプロジェクト**である
- **チーム開発**である

### DDDが不要な場合

- **単純なCRUDアプリケーション**（データの登録・更新・削除のみ）
- **技術的な問題のみ**を扱う（ビジネスロジックが少ない）
- **短期間のプロトタイプ**

**注意**: 小規模なプロジェクトでも、DDDの考え方（特にユビキタス言語、エンティティと値オブジェクトの区別）は有効です。

## この解説書の構成

この解説書は、以下の順序でDDDを学びます：

1. **ユビキタス言語**（02章）: ドメインエキスパートと開発者が同じ言葉で話せるように
2. **エンティティと値オブジェクト**（03章）: ドメインモデルの基本要素
3. **集約**（04章）: 整合性の境界を定義
4. **リポジトリ**（05章）: 永続化の抽象化
5. **ドメインサービス**（06章）: 集約に属さないロジック
6. **境界づけられたコンテキスト**（07章）: 大規模システムでの分割
7. **実装例**（08章）: これまで学んだ概念の統合
8. **ベストプラクティス**（09章）: 実践的な知見

## まとめ

- **DDD**は、複雑なビジネスロジックを持つソフトウェアを設計するためのアプローチ
- **ドメイン**を中心に据え、**ドメインエキスパート**と協働する
- **従来のアプローチ**では、ビジネスロジックが散在し、用語が不統一になりがち
- **DDD**では、ビジネスロジックをドメインモデルに集約し、ユビキタス言語を確立する

## 考えてみよう

1. あなたが開発している（または開発した）アプリケーションで、ビジネスロジックが散在している箇所はありますか？
2. ドメインエキスパートと開発者の間で、用語の不一致が発生した経験はありますか？
3. データベースの詳細がビジネスロジックに混在している箇所はありますか？

次の章では、**ユビキタス言語**について詳しく学びます。

