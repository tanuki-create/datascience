# CQRS パターン

## 1. 概要

CQRS（Command Query Responsibility Segregation）は、読み取り（Query）と書き込み（Command）の責任を分離するパターンです。

## 2. CQRSの概念

### 2.1 Command（コマンド）

**説明**: 状態を変更する操作です。

**特徴**:
- 副作用がある
- 戻り値がない（または最小限）
- 非同期処理が可能

### 2.2 Query（クエリ）

**説明**: 状態を読み取る操作です。

**特徴**:
- 副作用がない
- 戻り値がある
- 読み取り専用

## 3. CQRSのメリット

### 3.1 読み書きの最適化

**説明**: 読み取りと書き込みを独立して最適化できます。

**メリット**:
- 読み取り用の最適化されたデータモデル
- 書き込み用の最適化されたデータモデル
- 異なるデータベースの使用

### 3.2 スケーラビリティ

**説明**: 読み取りと書き込みを独立してスケールできます。

**メリット**:
- 読み取りの水平スケーリング
- 書き込みの最適化
- リソースの効率的な使用

### 3.3 複雑性の分離

**説明**: 読み取りと書き込みの複雑性を分離できます。

**メリット**:
- コードの簡潔性
- 保守性の向上
- テストの容易さ

## 4. CQRSの実装

### 4.1 Command Handler

```python
class CreateUserCommand:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

class CreateUserCommandHandler:
    def __init__(self, db, event_store):
        self.db = db
        self.event_store = event_store
    
    async def handle(self, command: CreateUserCommand):
        # バリデーション
        if await self.db.user_exists(command.username):
            raise UserAlreadyExistsError()
        
        # イベントを発行
        await self.event_store.append_event(
            aggregate_id=command.username,
            event_type="UserCreated",
            event_data={
                "username": command.username,
                "email": command.email
            },
            version=1
        )
```

### 4.2 Query Handler

```python
class GetUserQuery:
    def __init__(self, user_id: int):
        self.user_id = user_id

class GetUserQueryHandler:
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle(self, query: GetUserQuery) -> dict:
        # 読み取り専用データベースから取得
        user = await self.read_db.get_user(query.user_id)
        return user
```

### 4.3 読み取りモデルの更新

```python
class UserReadModelUpdater:
    def __init__(self, read_db):
        self.read_db = read_db
    
    async def handle_event(self, event: dict):
        """イベントを受信して読み取りモデルを更新"""
        event_type = event["event_type"]
        
        if event_type == "UserCreated":
            await self.read_db.insert_user(
                user_id=event["event_data"]["user_id"],
                username=event["event_data"]["username"],
                email=event["event_data"]["email"]
            )
        elif event_type == "UserUpdated":
            await self.read_db.update_user(
                user_id=event["event_data"]["user_id"],
                **event["event_data"]
            )
```

## 5. ベストプラクティス

1. **適切な分離**: 読み取りと書き込みを適切に分離
2. **イベント駆動**: イベント駆動で読み取りモデルを更新
3. **最終的一貫性**: 最終的一貫性を許容
4. **パフォーマンス**: 読み取りモデルを最適化
5. **複雑性の管理**: 複雑性を適切に管理

## 6. よくある落とし穴

1. **過度な複雑性**: CQRSの導入が過度に複雑になる
2. **最終的一貫性**: 最終的一貫性による問題
3. **イベントの順序**: イベントの順序の問題

## 7. 関連パターン

- [Event Sourcing](event_sourcing.md) - イベントソーシング
- [Message Queues](message_queues.md) - メッセージキュー

---

**次のステップ**: [Saga Pattern](saga_pattern.md)で分散トランザクション管理パターンを学ぶ

