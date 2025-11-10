# セキュリティベストプラクティス

## 概要

このガイドは、データベース接続におけるセキュリティのベストプラクティスを提供します。認証・認可、接続暗号化、SQLインジェクション対策、データ暗号化、監査、コンプライアンスなど、包括的なセキュリティ考慮事項をカバーしています。

## 認証と認可

### 強力なパスワードポリシー

```python
# パスワード強度の検証
import re
import hashlib
import secrets

class PasswordPolicy:
    def __init__(self):
        self.min_length = 12
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special = True
    
    def validate_password(self, password: str) -> tuple[bool, str]:
        """パスワードを検証"""
        if len(password) < self.min_length:
            return False, f"パスワードは{self.min_length}文字以上である必要があります"
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            return False, "パスワードには大文字が含まれている必要があります"
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            return False, "パスワードには小文字が含まれている必要があります"
        
        if self.require_digits and not re.search(r'\d', password):
            return False, "パスワードには数字が含まれている必要があります"
        
        if self.require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "パスワードには特殊文字が含まれている必要があります"
        
        return True, "パスワードは有効です"
    
    def hash_password(self, password: str, salt: bytes = None) -> tuple[str, bytes]:
        """パスワードをハッシュ化"""
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # PBKDF2を使用してパスワードをハッシュ化
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return key.hex(), salt
    
    def verify_password(self, password: str, hashed: str, salt: bytes) -> bool:
        """パスワードを検証"""
        key, _ = self.hash_password(password, salt)
        return key == hashed
```

### 多要素認証（MFA）

```python
# 多要素認証の実装
import pyotp
import qrcode
from io import BytesIO
import base64

class MultiFactorAuth:
    def __init__(self):
        self.totp = pyotp.TOTP
    
    def generate_secret(self) -> str:
        """TOTPシークレットを生成"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, user_email: str, secret: str) -> str:
        """QRコードを生成"""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name='MyApp'
        )
        
        img = qrcode.make(totp_uri)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.read()).decode()
    
    def verify_token(self, secret: str, token: str) -> bool:
        """TOTPトークンを検証"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)
    
    async def enable_mfa(self, user_id: int, secret: str):
        """MFAを有効化"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE users 
                SET mfa_secret = $1, mfa_enabled = true
                WHERE id = $2
            """, secret, user_id)
    
    async def authenticate_with_mfa(self, user_id: int, password: str, token: str) -> bool:
        """MFA付きで認証"""
        # パスワードを検証
        async with self.db_pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT password_hash, password_salt, mfa_secret, mfa_enabled FROM users WHERE id = $1",
                user_id
            )
            
            if not user:
                return False
            
            # パスワード検証
            policy = PasswordPolicy()
            if not policy.verify_password(password, user['password_hash'], user['password_salt']):
                return False
            
            # MFAが有効な場合、トークンを検証
            if user['mfa_enabled']:
                if not self.verify_token(user['mfa_secret'], token):
                    return False
            
            return True
```

### ロールベースアクセス制御（RBAC）

```python
# ロールベースアクセス制御の実装
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"
    ANALYST = "analyst"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class RBACManager:
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
            Role.USER: [Permission.READ, Permission.WRITE],
            Role.VIEWER: [Permission.READ],
            Role.ANALYST: [Permission.READ, Permission.WRITE]
        }
    
    def has_permission(self, role: Role, permission: Permission) -> bool:
        """権限をチェック"""
        return permission in self.role_permissions.get(role, [])
    
    async def check_database_access(self, user_id: int, action: str, resource: str) -> bool:
        """データベースアクセスをチェック"""
        async with self.db_pool.acquire() as conn:
            user = await conn.fetchrow(
                "SELECT role FROM users WHERE id = $1",
                user_id
            )
            
            if not user:
                return False
            
            role = Role(user['role'])
            permission = Permission(action)
            
            return self.has_permission(role, permission)
    
    async def execute_with_permission_check(self, user_id: int, query: str, *args):
        """権限チェック付きでクエリを実行"""
        # クエリタイプを判定（簡易版）
        if query.strip().upper().startswith('SELECT'):
            action = 'read'
        elif query.strip().upper().startswith(('INSERT', 'UPDATE')):
            action = 'write'
        elif query.strip().upper().startswith('DELETE'):
            action = 'delete'
        else:
            action = 'admin'
        
        if not await self.check_database_access(user_id, action, 'database'):
            raise PermissionError("Access denied")
        
        async with self.db_pool.acquire() as conn:
            return await conn.execute(query, *args)
```

### 行レベルセキュリティ（RLS）

```python
# PostgreSQLの行レベルセキュリティの実装
class RowLevelSecurity:
    async def setup_rls(self):
        """行レベルセキュリティをセットアップ"""
        async with self.db_pool.acquire() as conn:
            # RLSを有効化
            await conn.execute("""
                ALTER TABLE user_data ENABLE ROW LEVEL SECURITY;
                
                -- ポリシー: ユーザーは自分のデータのみアクセス可能
                CREATE POLICY user_data_policy ON user_data
                    FOR ALL
                    TO authenticated_user
                    USING (user_id = current_setting('app.user_id')::int);
            """)
    
    async def set_user_context(self, conn, user_id: int):
        """ユーザーコンテキストを設定"""
        await conn.execute(f"SET app.user_id = {user_id}")
    
    async def get_user_data(self, user_id: int):
        """ユーザーデータを取得（RLSが自動的に適用される）"""
        async with self.db_pool.acquire() as conn:
            await self.set_user_context(conn, user_id)
            return await conn.fetch("SELECT * FROM user_data")
```

## 接続暗号化

### TLS/SSL接続

```python
# TLS/SSL接続の設定
import ssl

class SecureConnection:
    def __init__(self):
        self.ssl_context = ssl.create_default_context()
        # 証明書の検証を有効化
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    async def create_secure_pool(self, config: dict):
        """セキュアな接続プールを作成"""
        return await asyncpg.create_pool(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            ssl=self.ssl_context,
            # 接続文字列でSSLを強制
            command_timeout=30
        )
    
    def create_ssl_context_with_cert(self, cert_file: str, key_file: str):
        """カスタム証明書でSSLコンテキストを作成"""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(cert_file, key_file)
        return context
```

### 接続文字列の安全な管理

```python
# 接続文字列の安全な管理
import os
from cryptography.fernet import Fernet

class SecureConfigManager:
    def __init__(self, encryption_key: bytes = None):
        if encryption_key is None:
            # 環境変数から取得
            key = os.getenv('CONFIG_ENCRYPTION_KEY')
            if key:
                self.cipher = Fernet(key.encode())
            else:
                raise ValueError("Encryption key not found")
        else:
            self.cipher = Fernet(encryption_key)
    
    def encrypt_connection_string(self, connection_string: str) -> str:
        """接続文字列を暗号化"""
        encrypted = self.cipher.encrypt(connection_string.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_connection_string(self, encrypted_string: str) -> str:
        """接続文字列を復号化"""
        decrypted = self.cipher.decrypt(base64.b64decode(encrypted_string))
        return decrypted.decode()
    
    def get_connection_config_from_env(self) -> dict:
        """環境変数から接続設定を取得（推奨方法）"""
        return {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),  # シークレットマネージャーから取得推奨
            'port': int(os.getenv('DB_PORT', 5432))
        }
```

## SQLインジェクション対策

### パラメータ化クエリ

```python
# SQLインジェクション対策：パラメータ化クエリ
class SafeQueryExecutor:
    def __init__(self, pool):
        self.pool = pool
    
    # 悪い例：SQLインジェクションの脆弱性
    async def unsafe_query(self, user_id: str):
        """危険：SQLインジェクションの脆弱性がある"""
        # 絶対にこの方法は使わない
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)
    
    # 良い例：パラメータ化クエリ
    async def safe_query(self, user_id: str):
        """安全：パラメータ化クエリを使用"""
        query = "SELECT * FROM users WHERE id = $1"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, user_id)
    
    async def safe_query_multiple_params(self, user_id: str, status: str):
        """複数パラメータの安全なクエリ"""
        query = "SELECT * FROM users WHERE id = $1 AND status = $2"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, user_id, status)
    
    async def safe_like_query(self, search_term: str):
        """LIKEクエリの安全な実装"""
        # パラメータ化クエリでLIKEも安全
        query = "SELECT * FROM users WHERE name LIKE $1"
        search_pattern = f"%{search_term}%"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, search_pattern)
```

### 入力検証とサニタイゼーション

```python
# 入力検証とサニタイゼーション
import re
from typing import Any

class InputValidator:
    @staticmethod
    def validate_user_id(user_id: Any) -> bool:
        """ユーザーIDを検証"""
        if not isinstance(user_id, (int, str)):
            return False
        
        # 整数のみ許可
        if isinstance(user_id, str):
            return user_id.isdigit()
        
        return isinstance(user_id, int) and user_id > 0
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """メールアドレスを検証"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 255) -> str:
        """文字列をサニタイズ"""
        # 制御文字を削除
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
        # 長さを制限
        return sanitized[:max_length]
    
    @staticmethod
    def validate_sql_identifier(identifier: str) -> bool:
        """SQL識別子を検証（テーブル名、カラム名など）"""
        # 英数字とアンダースコアのみ許可
        pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, identifier))

# 使用例
class SafeQueryBuilder:
    def __init__(self, validator: InputValidator):
        self.validator = validator
    
    async def build_safe_query(self, table: str, column: str, value: Any):
        """安全なクエリを構築"""
        # テーブル名とカラム名を検証
        if not self.validator.validate_sql_identifier(table):
            raise ValueError(f"Invalid table name: {table}")
        if not self.validator.validate_sql_identifier(column):
            raise ValueError(f"Invalid column name: {column}")
        
        # パラメータ化クエリを使用
        query = f"SELECT * FROM {table} WHERE {column} = $1"
        return query, value
```

## データ暗号化

### 保存時の暗号化

```python
# データベース保存時の暗号化
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class DataEncryption:
    def __init__(self, password: str, salt: bytes = None):
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
        self.salt = salt
    
    def encrypt_field(self, data: str) -> str:
        """フィールドを暗号化"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_field(self, encrypted_data: str) -> str:
        """フィールドを復号化"""
        decrypted = self.cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted.decode()
    
    async def store_encrypted_data(self, user_id: int, sensitive_data: dict):
        """暗号化されたデータを保存"""
        encrypted = {
            'email': self.encrypt_field(sensitive_data['email']),
            'phone': self.encrypt_field(sensitive_data['phone']),
            'ssn': self.encrypt_field(sensitive_data['ssn'])
        }
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO encrypted_user_data (user_id, encrypted_data, salt)
                VALUES ($1, $2, $3)
            """, user_id, json.dumps(encrypted), base64.b64encode(self.salt).decode())
    
    async def retrieve_encrypted_data(self, user_id: int) -> dict:
        """暗号化されたデータを取得して復号化"""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT encrypted_data, salt FROM encrypted_user_data WHERE user_id = $1
            """, user_id)
            
            if not row:
                return None
            
            # 同じパスワードとソルトで復号化キーを再生成
            # （実際の実装では、パスワードを安全に管理する必要がある）
            encrypted_data = json.loads(row['encrypted_data'])
            salt = base64.b64decode(row['salt'])
            
            # 復号化（パスワードは安全に管理された場所から取得）
            password = self.get_encryption_password()  # 実装が必要
            decryption = DataEncryption(password, salt)
            
            return {
                'email': decryption.decrypt_field(encrypted_data['email']),
                'phone': decryption.decrypt_field(encrypted_data['phone']),
                'ssn': decryption.decrypt_field(encrypted_data['ssn'])
            }
```

### 転送時の暗号化

```python
# 転送時の暗号化（TLS/SSL）
class SecureDataTransfer:
    def __init__(self):
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = True
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED
    
    async def create_secure_connection(self, host: str, port: int):
        """セキュアな接続を作成"""
        reader, writer = await asyncio.open_connection(
            host, port, ssl=self.ssl_context
        )
        return reader, writer
    
    async def send_encrypted_data(self, connection, data: dict):
        """暗号化されたデータを送信"""
        encrypted = json.dumps(data).encode()
        connection.write(encrypted)
        await connection.drain()
```

## 監査とロギング

### 監査ログの実装

```python
# データベース操作の監査ログ
class AuditLogger:
    def __init__(self, pool):
        self.pool = pool
    
    async def log_database_operation(
        self,
        user_id: int,
        operation: str,
        table: str,
        record_id: int,
        old_values: dict = None,
        new_values: dict = None
    ):
        """データベース操作を監査ログに記録"""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO audit_logs (
                    user_id, operation, table_name, record_id,
                    old_values, new_values, created_at, ip_address
                ) VALUES ($1, $2, $3, $4, $5, $6, NOW(), $7)
            """, user_id, operation, table, record_id,
                json.dumps(old_values) if old_values else None,
                json.dumps(new_values) if new_values else None,
                self.get_client_ip()
            )
    
    async def setup_audit_triggers(self):
        """監査トリガーをセットアップ"""
        async with self.db_pool.acquire() as conn:
            # トリガー関数を作成
            await conn.execute("""
                CREATE OR REPLACE FUNCTION audit_trigger_func()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        INSERT INTO audit_logs (
                            table_name, operation, record_id, new_values, created_at
                        ) VALUES (
                            TG_TABLE_NAME, 'INSERT', NEW.id, row_to_json(NEW), NOW()
                        );
                        RETURN NEW;
                    ELSIF TG_OP = 'UPDATE' THEN
                        INSERT INTO audit_logs (
                            table_name, operation, record_id, old_values, new_values, created_at
                        ) VALUES (
                            TG_TABLE_NAME, 'UPDATE', NEW.id,
                            row_to_json(OLD), row_to_json(NEW), NOW()
                        );
                        RETURN NEW;
                    ELSIF TG_OP = 'DELETE' THEN
                        INSERT INTO audit_logs (
                            table_name, operation, record_id, old_values, created_at
                        ) VALUES (
                            TG_TABLE_NAME, 'DELETE', OLD.id, row_to_json(OLD), NOW()
                        );
                        RETURN OLD;
                    END IF;
                END;
                $$ LANGUAGE plpgsql;
                
                -- トリガーを作成
                CREATE TRIGGER user_data_audit_trigger
                AFTER INSERT OR UPDATE OR DELETE ON user_data
                FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
            """)
    
    def get_client_ip(self) -> str:
        """クライアントIPアドレスを取得（実装が必要）"""
        # 実際の実装では、リクエストコンテキストから取得
        return "127.0.0.1"
```

### セキュリティイベントのロギング

```python
# セキュリティイベントのロギング
import logging

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.WARNING)
        
        # セキュリティログ用のハンドラー
        handler = logging.FileHandler('security.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_failed_login(self, username: str, ip_address: str):
        """失敗したログイン試行をログに記録"""
        self.logger.warning(
            f"Failed login attempt - Username: {username}, IP: {ip_address}"
        )
    
    def log_sql_injection_attempt(self, query: str, ip_address: str):
        """SQLインジェクション試行をログに記録"""
        self.logger.critical(
            f"SQL injection attempt detected - Query: {query[:100]}, IP: {ip_address}"
        )
    
    def log_unauthorized_access(self, user_id: int, resource: str, ip_address: str):
        """不正アクセスをログに記録"""
        self.logger.warning(
            f"Unauthorized access attempt - User: {user_id}, Resource: {resource}, IP: {ip_address}"
        )
    
    def log_data_breach_attempt(self, user_id: int, table: str, ip_address: str):
        """データ侵害試行をログに記録"""
        self.logger.critical(
            f"Data breach attempt - User: {user_id}, Table: {table}, IP: {ip_address}"
        )
```

## コンプライアンス

### GDPR準拠

```python
# GDPR準拠の実装
class GDPRCompliance:
    def __init__(self, pool):
        self.pool = pool
    
    async def request_user_data(self, user_id: int) -> dict:
        """ユーザーデータの開示リクエスト（GDPR Article 15）"""
        async with self.pool.acquire() as conn:
            user_data = await conn.fetchrow("""
                SELECT * FROM users WHERE id = $1
            """, user_id)
            
            user_activity = await conn.fetch("""
                SELECT * FROM user_activity WHERE user_id = $1
            """, user_id)
            
            return {
                'user_data': dict(user_data) if user_data else None,
                'activity': [dict(row) for row in user_activity]
            }
    
    async def delete_user_data(self, user_id: int):
        """ユーザーデータの削除リクエスト（GDPR Article 17）"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 関連データをすべて削除
                await conn.execute("DELETE FROM user_activity WHERE user_id = $1", user_id)
                await conn.execute("DELETE FROM user_preferences WHERE user_id = $1", user_id)
                await conn.execute("DELETE FROM users WHERE id = $1", user_id)
                
                # 削除をログに記録
                await conn.execute("""
                    INSERT INTO gdpr_deletion_log (user_id, deleted_at)
                    VALUES ($1, NOW())
                """, user_id)
    
    async def export_user_data(self, user_id: int) -> str:
        """ユーザーデータのエクスポート（GDPR Article 20）"""
        data = await self.request_user_data(user_id)
        return json.dumps(data, indent=2, ensure_ascii=False)
```

### PCI DSS準拠

```python
# PCI DSS準拠の実装（クレジットカード情報の保護）
class PCIDSSCompliance:
    def __init__(self):
        self.encryption = DataEncryption(os.getenv('PCI_ENCRYPTION_KEY'))
    
    async def store_card_token(self, user_id: int, card_token: str):
        """カードトークンを保存（実際のカード番号は保存しない）"""
        # カード情報は決済プロバイダーに保存し、トークンのみを保存
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO payment_tokens (user_id, token, created_at)
                VALUES ($1, $2, NOW())
            """, user_id, card_token)
    
    async def mask_card_number(self, card_number: str) -> str:
        """カード番号をマスキング（表示用）"""
        if len(card_number) < 4:
            return "****"
        return "****-****-****-" + card_number[-4:]
    
    async def log_card_access(self, user_id: int, action: str):
        """カード情報へのアクセスをログに記録"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO pci_access_log (user_id, action, accessed_at, ip_address)
                VALUES ($1, $2, NOW(), $3)
            """, user_id, action, self.get_client_ip())
```

## 実装例

### 完全なセキュアデータベース接続マネージャー

```python
# 完全なセキュアデータベース接続マネージャーの実装例
import asyncio
import asyncpg
import ssl
import os
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class SecureDatabaseManager:
    def __init__(self, config: dict):
        self.config = config
        self.pool = None
        self.validator = InputValidator()
        self.audit_logger = None
        self.security_logger = SecurityLogger()
    
    async def initialize(self):
        """セキュアなデータベース接続プールを初期化"""
        # SSLコンテキストを作成
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        
        # 接続プールを作成
        self.pool = await asyncpg.create_pool(
            host=self.config['host'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
            ssl=ssl_context,
            min_size=5,
            max_size=20,
            command_timeout=30
        )
        
        # 監査ログを初期化
        self.audit_logger = AuditLogger(self.pool)
        await self.audit_logger.setup_audit_triggers()
        
        logger.info("Secure database connection pool initialized")
    
    @asynccontextmanager
    async def get_connection(self, user_id: int = None):
        """セキュアなコネクションを取得"""
        async with self.pool.acquire() as conn:
            # 行レベルセキュリティのコンテキストを設定
            if user_id:
                await conn.execute(f"SET app.user_id = {user_id}")
            yield conn
    
    async def execute_safe_query(
        self,
        user_id: int,
        query: str,
        *args,
        table: str = None,
        operation: str = None
    ):
        """安全なクエリを実行"""
        # 入力検証
        if not self.validator.validate_user_id(user_id):
            self.security_logger.log_unauthorized_access(
                user_id, 'database', self.get_client_ip()
            )
            raise ValueError("Invalid user ID")
        
        # SQLインジェクション検出（簡易版）
        if self.detect_sql_injection(query):
            self.security_logger.log_sql_injection_attempt(
                query, self.get_client_ip()
            )
            raise ValueError("Potential SQL injection detected")
        
        try:
            async with self.get_connection(user_id) as conn:
                result = await conn.execute(query, *args)
                
                # 監査ログを記録
                if table and operation:
                    await self.audit_logger.log_database_operation(
                        user_id, operation, table, None
                    )
                
                return result
        except Exception as e:
            logger.error(f"Database error: {e}")
            raise
    
    def detect_sql_injection(self, query: str) -> bool:
        """SQLインジェクションの可能性を検出（簡易版）"""
        dangerous_patterns = [
            '; DROP',
            '; DELETE',
            '; UPDATE',
            'UNION SELECT',
            'OR 1=1',
            '--',
            '/*',
            'xp_',
            'EXEC(',
            'EXECUTE('
        ]
        
        query_upper = query.upper()
        for pattern in dangerous_patterns:
            if pattern in query_upper:
                return True
        
        return False
    
    def get_client_ip(self) -> str:
        """クライアントIPアドレスを取得"""
        # 実際の実装では、リクエストコンテキストから取得
        return "127.0.0.1"
    
    async def close(self):
        """プールを閉じる"""
        if self.pool:
            await self.pool.close()
            logger.info("Secure database connection pool closed")

# 使用例
async def main():
    config = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    
    db = SecureDatabaseManager(config)
    await db.initialize()
    
    try:
        # 安全なクエリを実行
        result = await db.execute_safe_query(
            user_id=1,
            query="SELECT * FROM users WHERE id = $1",
            1,
            table='users',
            operation='SELECT'
        )
        print(f"Query executed successfully")
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## まとめ

セキュリティベストプラクティスの重要なポイント：

### 認証と認可
- 強力なパスワードポリシー
- 多要素認証（MFA）
- ロールベースアクセス制御（RBAC）
- 行レベルセキュリティ（RLS）

### 接続暗号化
- TLS/SSL接続の強制
- 接続文字列の安全な管理
- 環境変数やシークレットマネージャーの使用

### SQLインジェクション対策
- パラメータ化クエリの使用
- 入力検証とサニタイゼーション
- SQL識別子の検証

### データ暗号化
- 保存時の暗号化（機密データ）
- 転送時の暗号化（TLS/SSL）
- 適切な鍵管理

### 監査とロギング
- データベース操作の監査ログ
- セキュリティイベントのロギング
- 監査トリガーの実装

### コンプライアンス
- GDPR準拠（データ開示、削除、エクスポート）
- PCI DSS準拠（クレジットカード情報の保護）
- 業界固有のコンプライアンス要件への対応

セキュリティは多層防御のアプローチで実装する必要があります。単一の対策に依存せず、認証、認可、暗号化、監査、コンプライアンスを組み合わせることで、堅牢なセキュリティ体制を構築できます。


