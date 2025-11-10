# サーバーサイド開発 - 面接対策ガイド

## 1. 良いコードを書くための知見

### 1.1 コードの可読性

#### 命名規則の徹底
- **意図が明確な変数名・関数名**
  - 悪い例: `data`, `process()`, `temp`
  - 良い例: `userProfile`, `calculateMonthlyRevenue()`, `expirationDate`
  
- **ドメイン用語の使用**
  - ビジネスロジックを理解していることを示す
  - 例: `Order`, `Payment`, `Invoice` など、ドメインエキスパートが使う用語

- **一貫性の維持**
  - プロジェクト全体で同じ命名規則を適用
  - 例: データベーステーブルは複数形、モデルクラスは単数形

#### 関数・メソッドの設計原則

**単一責任の原則（SRP）**
```python
# 悪い例: 複数の責任を持つ関数
def process_order(order):
    # 在庫チェック
    # 価格計算
    # 決済処理
    # メール送信
    # ログ記録
    pass

# 良い例: 責任を分離
def check_inventory(order):
    """在庫をチェックする"""
    pass

def calculate_total_price(order):
    """合計金額を計算する"""
    pass

def process_payment(order, amount):
    """決済を処理する"""
    pass

def send_confirmation_email(order):
    """確認メールを送信する"""
    pass
```

**関数のサイズ**
- 1つの関数は20-30行以内を目安
- 長くなりそうな場合は、複数の関数に分割

**引数の数**
- 3つ以下を目安（それ以上はオブジェクトでまとめる）
```python
# 悪い例
def create_user(name, email, age, address, phone, role):
    pass

# 良い例
def create_user(user_data: UserData):
    pass
```

#### コメントの書き方

**良いコメント**
- **なぜ**そのコードが存在するかを説明
- 複雑なビジネスロジックの意図を説明
- 将来の開発者への警告や注意事項

```python
# 悪い例: 何をしているかはコードから明らか
# ユーザーIDを取得する
user_id = user.id

# 良い例: なぜその処理が必要かを説明
# セッションタイムアウトを防ぐため、アクティビティを記録
# （30分以内のアクティビティがあればセッションを延長）
record_user_activity(user_id)
```

**悪いコメント**
- コードの動作をそのまま説明するだけのコメント
- 古くなってコードと乖離したコメント

### 1.2 テストしやすいコードの工夫

#### 依存性の注入（Dependency Injection）

```python
# 悪い例: 依存関係がハードコードされている
class OrderService:
    def __init__(self):
        self.payment_gateway = PaymentGateway()  # テストが困難
        self.email_service = EmailService()
    
    def process_order(self, order):
        result = self.payment_gateway.charge(order.amount)
        self.email_service.send_confirmation(order)

# 良い例: 依存関係を注入できる
class OrderService:
    def __init__(self, payment_gateway, email_service):
        self.payment_gateway = payment_gateway
        self.email_service = email_service
    
    def process_order(self, order):
        result = self.payment_gateway.charge(order.amount)
        self.email_service.send_confirmation(order)

# テスト時
def test_process_order():
    mock_payment = MockPaymentGateway()
    mock_email = MockEmailService()
    service = OrderService(mock_payment, mock_email)
    # テスト実行
```

#### 純粋関数の活用

**副作用の分離**
```python
# 悪い例: データベースアクセスと計算が混在
def calculate_discount(user_id, amount):
    user = User.get(user_id)  # DBアクセス
    if user.is_premium:
        return amount * 0.1
    return 0

# 良い例: 純粋関数と副作用を分離
def calculate_discount(user_type, amount):
    """純粋関数: 同じ入力に対して常に同じ出力"""
    if user_type == 'premium':
        return amount * 0.1
    return 0

def apply_discount_to_order(order_id):
    """副作用（DBアクセス）を含む関数"""
    order = Order.get(order_id)
    user = User.get(order.user_id)
    discount = calculate_discount(user.type, order.amount)
    order.apply_discount(discount)
    order.save()
```

#### モック可能な設計

```python
# 外部API呼び出しを抽象化
class WeatherService:
    def get_temperature(self, city: str) -> float:
        raise NotImplementedError

class OpenWeatherMapService(WeatherService):
    def get_temperature(self, city: str) -> float:
        # 実際のAPI呼び出し
        response = requests.get(f"https://api.openweathermap.org/...")
        return response.json()['temp']

# テスト用のモック
class MockWeatherService(WeatherService):
    def get_temperature(self, city: str) -> float:
        return 25.0  # 固定値を返す
```

### 1.3 エラーハンドリング

#### 適切な例外処理

```python
# 悪い例: 例外を握りつぶす
def process_payment(amount):
    try:
        charge(amount)
    except:
        pass  # エラーが隠される

# 良い例: 適切な例外処理
def process_payment(amount):
    try:
        charge(amount)
    except PaymentGatewayError as e:
        logger.error(f"Payment failed: {e}", extra={"amount": amount})
        raise PaymentProcessingError("決済処理に失敗しました") from e
    except InsufficientFundsError:
        raise PaymentProcessingError("残高が不足しています")
```

#### 早期リターン

```python
# 悪い例: ネストが深い
def validate_order(order):
    if order:
        if order.items:
            if order.total > 0:
                if order.user:
                    return True
    return False

# 良い例: 早期リターンで可読性向上
def validate_order(order):
    if not order:
        return False
    if not order.items:
        return False
    if order.total <= 0:
        return False
    if not order.user:
        return False
    return True
```

## 2. 良いプログラム・設計のために普段から気をつけていること

### 2.1 設計段階での考慮事項

#### 変更に強い設計

**オープン・クローズドの原則（OCP）**
- 拡張に対して開いており、修正に対して閉じている

```python
# 悪い例: 新しい決済方法を追加するたびに既存コードを修正
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == 'credit_card':
            # クレジットカード処理
        elif payment_type == 'paypal':
            # PayPal処理
        elif payment_type == 'bank_transfer':  # 追加時に既存コードを変更
            # 銀行振込処理

# 良い例: 拡張可能な設計
class PaymentProcessor:
    def __init__(self):
        self.strategies = {}
    
    def register_strategy(self, payment_type, strategy):
        self.strategies[payment_type] = strategy
    
    def process(self, payment_type, amount):
        strategy = self.strategies.get(payment_type)
        if not strategy:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return strategy.process(amount)

# 新しい決済方法を追加する際は、既存コードを変更せずに新しいクラスを追加
class BankTransferStrategy:
    def process(self, amount):
        # 銀行振込処理
        pass
```

#### 依存関係逆転の原則（DIP）

```python
# 悪い例: 具象クラスに依存
class UserService:
    def __init__(self):
        self.repository = MySQLUserRepository()  # 具象クラスに依存

# 良い例: 抽象に依存
class UserService:
    def __init__(self, repository: UserRepository):  # インターフェースに依存
        self.repository = repository

# インターフェース定義
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        pass

# 実装
class MySQLUserRepository(UserRepository):
    def find_by_id(self, user_id: int) -> User:
        # MySQL実装
        pass

class PostgreSQLUserRepository(UserRepository):
    def find_by_id(self, user_id: int) -> User:
        # PostgreSQL実装
        pass
```

### 2.2 コードレビューの観点

#### レビュー時にチェックする項目

1. **可読性**
   - 変数名・関数名が意図を明確に表しているか
   - コメントが適切か（不要なコメントはないか）

2. **保守性**
   - 重複コードがないか（DRY原則）
   - 関数が適切なサイズか
   - 責任が適切に分離されているか

3. **テスト可能性**
   - モック可能な設計か
   - テストが書きやすい構造か

4. **パフォーマンス**
   - 不要なループやクエリがないか
   - N+1問題がないか

5. **セキュリティ**
   - SQLインジェクション対策
   - XSS対策
   - 認証・認可の実装

### 2.3 リファクタリングの習慣

#### 定期的なリファクタリング

**コードの臭い（Code Smell）の識別**
- 長い関数（Long Method）
- 大きなクラス（Large Class）
- 重複コード（Duplicated Code）
- 長いパラメータリスト（Long Parameter List）
- データの塊（Data Clumps）

**リファクタリングのタイミング**
- 機能追加の前後
- バグ修正の際に、根本原因を解決するため
- コードレビューで指摘された時
- 定期的な技術的負債の返済

**安全なリファクタリング手順**
1. テストを書く（既存の動作を保証）
2. 小さなステップで変更
3. 各ステップでテストを実行
4. コミット（ロールバック可能に）

## 3. アーキテクチャの知見

### 3.1 リファクタリングの経験

#### レガシーコードの改善例

**問題のあるコードの例**
```python
# レガシーコード: すべてが1つのファイルに
# app.py (2000行)
class App:
    def handle_request(self, request):
        # 認証チェック
        # バリデーション
        # ビジネスロジック
        # データベースアクセス
        # レスポンス生成
        pass
```

**リファクタリング後の構造**
```
app/
├── domain/
│   ├── models/
│   │   ├── user.py
│   │   └── order.py
│   └── services/
│       ├── user_service.py
│       └── order_service.py
├── infrastructure/
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── order_repository.py
│   └── external/
│       ├── payment_gateway.py
│       └── email_service.py
├── application/
│   ├── use_cases/
│   │   ├── create_user.py
│   │   └── process_order.py
│   └── dto/
│       ├── user_dto.py
│       └── order_dto.py
└── presentation/
    ├── controllers/
    │   ├── user_controller.py
    │   └── order_controller.py
    └── middleware/
        ├── auth.py
        └── validation.py
```

#### 段階的なリファクタリング戦略

1. **機能追加の機会を活用**
   - 新機能を追加する際に、関連する既存コードもリファクタリング

2. **Boy Scout Rule（ボーイスカウトの規則）**
   - 「来た時よりも綺麗にして去る」
   - 触ったコードは必ず少しでも改善する

3. **Strangler Fig Pattern（絞め殺しのイチジクパターン）**
   - 新しいアーキテクチャで新機能を実装
   - 既存機能を段階的に移行

### 3.2 クリーンアーキテクチャ

#### レイヤー構造

```
┌─────────────────────────────────────┐
│         Presentation Layer         │  ← Controllers, Routes
├─────────────────────────────────────┤
│        Application Layer            │  ← Use Cases, DTOs
├─────────────────────────────────────┤
│          Domain Layer                │  ← Entities, Business Logic
├─────────────────────────────────────┤
│      Infrastructure Layer            │  ← DB, External APIs
└─────────────────────────────────────┘
```

#### 依存関係の方向

**依存関係逆転の原則**
- 外側のレイヤーは内側のレイヤーに依存
- 内側のレイヤーは外側のレイヤーに依存しない
- インターフェースを通じて依存関係を逆転

```python
# Domain Layer (内側) - ビジネスロジック
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def is_premium(self) -> bool:
        # ビジネスロジック
        return self.subscription_type == 'premium'

# Application Layer - ユースケース
class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_data: CreateUserDTO) -> User:
        user = User(
            user_id=None,  # 新規作成
            name=user_data.name,
            email=user_data.email
        )
        return self.user_repository.save(user)

# Infrastructure Layer (外側) - 実装
class MySQLUserRepository(UserRepository):
    def save(self, user: User) -> User:
        # データベースへの保存
        pass
```

#### 実践例: ユーザー登録機能

```python
# Domain Layer
class User:
    def __init__(self, user_id: int, email: str, password_hash: str):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # ビジネスルール: メールアドレスの検証
        return "@" in email and "." in email.split("@")[1]

# Application Layer
class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.email_service = email_service
    
    def execute(self, email: str, password: str) -> User:
        # 既存ユーザーチェック
        if self.user_repository.find_by_email(email):
            raise UserAlreadyExistsError()
        
        # パスワードハッシュ化
        password_hash = self.password_hasher.hash(password)
        
        # ユーザー作成
        user = User(
            user_id=None,
            email=email,
            password_hash=password_hash
        )
        
        saved_user = self.user_repository.save(user)
        
        # 確認メール送信
        self.email_service.send_verification_email(saved_user.email)
        
        return saved_user

# Presentation Layer
class UserController:
    def __init__(self, register_user_use_case: RegisterUserUseCase):
        self.register_user_use_case = register_user_use_case
    
    def register(self, request):
        try:
            user = self.register_user_use_case.execute(
                email=request.json['email'],
                password=request.json['password']
            )
            return {"user_id": user.user_id, "email": user.email}, 201
        except UserAlreadyExistsError:
            return {"error": "User already exists"}, 409
        except ValueError as e:
            return {"error": str(e)}, 400
```

### 3.3 ドメイン駆動設計（DDD）

#### ドメインモデル

**エンティティ vs 値オブジェクト**

```python
# エンティティ: 識別子を持つ
class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id  # 識別子
        self.name = name
    
    def __eq__(self, other):
        return self.user_id == other.user_id

# 値オブジェクト: 識別子を持たない、値で等価性を判断
class Money:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency
    
    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency
    
    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

#### 集約（Aggregate）

```python
# 集約ルート: Order
class Order:
    def __init__(self, order_id: int, customer_id: int):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
    
    def add_item(self, product_id: int, quantity: int, price: float):
        """集約の整合性を保つ"""
        if self.status != OrderStatus.PENDING:
            raise InvalidOperationError("Cannot modify confirmed order")
        
        item = OrderItem(product_id, quantity, price)
        self.items.append(item)
    
    def confirm(self):
        """ビジネスルール: 注文を確定"""
        if not self.items:
            raise InvalidOperationError("Cannot confirm empty order")
        if self.status != OrderStatus.PENDING:
            raise InvalidOperationError("Order already confirmed")
        
        self.status = OrderStatus.CONFIRMED
        # ドメインイベントの発行
        DomainEventPublisher.publish(OrderConfirmedEvent(self.order_id))

# 集約の内部エンティティ
class OrderItem:
    def __init__(self, product_id: int, quantity: int, price: float):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def total(self) -> float:
        return self.quantity * self.price
```

#### ドメインサービス

```python
# ドメインサービス: 1つのエンティティに属さないビジネスロジック
class TransferService:
    def transfer(
        self,
        from_account: Account,
        to_account: Account,
        amount: Money
    ):
        """アカウント間の送金ロジック"""
        if from_account.balance < amount:
            raise InsufficientFundsError()
        
        if from_account.currency != to_account.currency:
            # 通貨変換が必要な場合
            converted_amount = self.currency_converter.convert(
                amount, to_account.currency
            )
            from_account.withdraw(amount)
            to_account.deposit(converted_amount)
        else:
            from_account.withdraw(amount)
            to_account.deposit(amount)
```

#### リポジトリパターン

```python
# リポジトリインターフェース（Domain Layer）
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: int) -> Order:
        pass
    
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass
    
    @abstractmethod
    def find_by_customer_id(self, customer_id: int) -> List[Order]:
        pass

# リポジトリ実装（Infrastructure Layer）
class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session
    
    def find_by_id(self, order_id: int) -> Order:
        order_orm = self.session.query(OrderORM).filter_by(id=order_id).first()
        if not order_orm:
            return None
        return self._to_domain(order_orm)
    
    def save(self, order: Order) -> Order:
        order_orm = self._to_orm(order)
        self.session.add(order_orm)
        self.session.commit()
        return self._to_domain(order_orm)
    
    def _to_domain(self, orm: OrderORM) -> Order:
        # ORMからドメインモデルへ変換
        pass
    
    def _to_orm(self, domain: Order) -> OrderORM:
        # ドメインモデルからORMへ変換
        pass
```

### 3.4 コードの可読性・保守性を高める実践

#### 設計パターンの活用

**ファクトリーパターン**
```python
class UserFactory:
    @staticmethod
    def create_customer(name: str, email: str) -> User:
        return User(
            user_type=UserType.CUSTOMER,
            name=name,
            email=email
        )
    
    @staticmethod
    def create_admin(name: str, email: str) -> User:
        return User(
            user_type=UserType.ADMIN,
            name=name,
            email=email,
            permissions=AdminPermissions.all()
        )
```

**ストラテジーパターン**
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        pass

class RegularPricingStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price

class PremiumPricingStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.9  # 10%割引

class VIPPricingStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.8  # 20%割引
```

#### 設定の外部化

```python
# 悪い例: 設定がコードに埋め込まれている
class EmailService:
    def send(self, to: str, subject: str, body: str):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        username = "app@example.com"
        password = "hardcoded_password"

# 良い例: 設定を外部化
class EmailService:
    def __init__(self, config: EmailConfig):
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.username = config.username
        self.password = config.password
```

## 4. 実践的な例: リファクタリング前後

### Before: モノリシックなコード

```python
# app.py (すべてが1つのファイル)
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/api/users', methods=['POST'])
def create_user():
    # バリデーション
    data = request.json
    if not data.get('email'):
        return jsonify({'error': 'Email required'}), 400
    
    # データベース接続
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='mydb'
    )
    cursor = conn.cursor()
    
    # 既存ユーザーチェック
    cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        return jsonify({'error': 'User exists'}), 409
    
    # パスワードハッシュ化
    import hashlib
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    # ユーザー作成
    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (data['email'], password_hash)
    )
    conn.commit()
    
    # メール送信
    import smtplib
    # ... メール送信コード ...
    
    return jsonify({'message': 'User created'}), 201
```

### After: クリーンアーキテクチャに基づいた設計

```python
# domain/models/user.py
class User:
    def __init__(self, user_id: int, email: str, password_hash: str):
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[1]

# domain/repositories/user_repository.py
class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass

# application/use_cases/create_user.py
class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.email_service = email_service
    
    def execute(self, email: str, password: str) -> User:
        if self.user_repository.find_by_email(email):
            raise UserAlreadyExistsError()
        
        password_hash = self.password_hasher.hash(password)
        user = User(user_id=None, email=email, password_hash=password_hash)
        saved_user = self.user_repository.save(user)
        self.email_service.send_verification_email(saved_user.email)
        return saved_user

# presentation/controllers/user_controller.py
class UserController:
    def __init__(self, create_user_use_case: CreateUserUseCase):
        self.create_user_use_case = create_user_use_case
    
    def create(self, request_data: dict):
        try:
            user = self.create_user_use_case.execute(
                email=request_data['email'],
                password=request_data['password']
            )
            return {"user_id": user.user_id, "email": user.email}, 201
        except UserAlreadyExistsError:
            return {"error": "User already exists"}, 409
        except ValueError as e:
            return {"error": str(e)}, 400

# infrastructure/repositories/mysql_user_repository.py
class MySQLUserRepository(UserRepository):
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def find_by_email(self, email: str) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if not row:
            return None
        return User(user_id=row[0], email=row[1], password_hash=row[2])
    
    def save(self, user: User) -> User:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (user.email, user.password_hash)
        )
        self.conn.commit()
        user.user_id = cursor.lastrowid
        return user
```

## 5. まとめ

### 良いコードを書くためのポイント

1. **可読性**
   - 明確な命名
   - 適切な関数サイズ
   - 意味のあるコメント

2. **テスト可能性**
   - 依存性の注入
   - 純粋関数の活用
   - モック可能な設計

3. **保守性**
   - 単一責任の原則
   - DRY原則（重複の排除）
   - 変更に強い設計

4. **アーキテクチャ**
   - レイヤー分離
   - 依存関係の管理
   - ドメインモデルの活用

### 面接で説明できる実践例

- 「以前のプロジェクトで、2000行のモノリシックなコードをクリーンアーキテクチャに基づいてリファクタリングしました。その結果、テストカバレッジが30%から85%に向上し、新機能の追加時間が50%短縮されました。」

- 「ドメイン駆動設計を適用し、ビジネスロジックをドメインレイヤーに集約しました。これにより、ビジネスルールの変更が1箇所で完結し、バグの発生率が40%減少しました。」

- 「依存性の注入を徹底することで、ユニットテストの作成が容易になり、CI/CDパイプラインでの自動テストが可能になりました。」

