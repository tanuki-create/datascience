# Chapter 10: Robustness

堅牢性のベストプラクティスを学びます。

## 目次

1. [例外処理でエラーを適切にハンドリングする](#1-例外処理でエラーを適切にハンドリングする)
2. [ログ記録で問題を追跡する](#2-ログ記録で問題を追跡する)
3. [バリデーションで入力データを検証する](#3-バリデーションで入力データを検証する)
4. [設定管理で環境に応じた動作を実現する](#4-設定管理で環境に応じた動作を実現する)
5. [リトライ機構で一時的な障害に対応する](#5-リトライ機構で一時的な障害に対応する)
6. [タイムアウトで無限待機を防ぐ](#6-タイムアウトで無限待機を防ぐ)
7. [サーキットブレーカーで障害の伝播を防ぐ](#7-サーキットブレーカーで障害の伝播を防ぐ)
8. [ヘルスチェックでシステムの状態を監視する](#8-ヘルスチェックでシステムの状態を監視する)
9. [グレースフルシャットダウンで安全に終了する](#9-グレースフルシャットダウンで安全に終了する)
10. [監視とアラートで問題を早期発見する](#10-監視とアラートで問題を早期発見する)

---

## 1. 例外処理でエラーを適切にハンドリングする

### 基本概念

適切な例外処理により、プログラムの堅牢性を向上させ、予期しないエラーから回復できます。具体的な例外をキャッチし、適切な処理を行うことが重要です。

### 具体例

#### 例1: 基本的な例外処理

```python
import logging
import time
from typing import Optional

# 悪い例（例外を無視）
def divide_numbers_bad(a, b):
    """数値を割り算（例外を無視）"""
    return a / b

# 良い例（適切な例外処理）
def divide_numbers_good(a, b):
    """数値を割り算（適切な例外処理）"""
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        logging.error(f"ゼロ除算エラー: {a} / {b}")
        return None
    except TypeError as e:
        logging.error(f"型エラー: {e}")
        return None
    except Exception as e:
        logging.error(f"予期しないエラー: {e}")
        return None

# 使用例
print("=== 基本的な例外処理 ===")
print(f"正常な計算: {divide_numbers_good(10, 2)}")
print(f"ゼロ除算: {divide_numbers_good(10, 0)}")
print(f"型エラー: {divide_numbers_good(10, 'a')}")

# ファイル操作での例外処理
def read_file_safely(filename: str) -> Optional[str]:
    """ファイルを安全に読み込み"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        logging.error(f"ファイルが見つかりません: {filename}")
        return None
    except PermissionError:
        logging.error(f"ファイルの読み込み権限がありません: {filename}")
        return None
    except UnicodeDecodeError:
        logging.error(f"ファイルの文字エンコーディングエラー: {filename}")
        return None
    except Exception as e:
        logging.error(f"ファイル読み込みエラー: {e}")
        return None

# 使用例
content = read_file_safely("nonexistent.txt")
if content is not None:
    print(f"ファイル内容: {content}")
else:
    print("ファイルの読み込みに失敗しました")
```

#### 例2: データベース操作での例外処理

```python
import sqlite3
import logging
from contextlib import contextmanager

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースを初期化"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"データベース初期化エラー: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """データベース接続を取得"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except sqlite3.Error as e:
            logging.error(f"データベース接続エラー: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def insert_user(self, name: str, email: str) -> bool:
        """ユーザーを挿入"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                conn.commit()
                logging.info(f"ユーザーを挿入しました: {name}")
                return True
        except sqlite3.IntegrityError as e:
            logging.error(f"ユニーク制約エラー: {e}")
            return False
        except sqlite3.Error as e:
            logging.error(f"データベースエラー: {e}")
            return False
        except Exception as e:
            logging.error(f"予期しないエラー: {e}")
            return False
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        """メールアドレスでユーザーを取得"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM users WHERE email = ?",
                    (email,)
                )
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'created_at': row[3]
                    }
                return None
        except sqlite3.Error as e:
            logging.error(f"データベースエラー: {e}")
            return None
        except Exception as e:
            logging.error(f"予期しないエラー: {e}")
            return None

# 使用例
print("\n=== データベース操作での例外処理 ===")
db_manager = DatabaseManager("test.db")

# ユーザーを挿入
success = db_manager.insert_user("Alice", "alice@example.com")
print(f"ユーザー挿入: {'成功' if success else '失敗'}")

# 重複したメールアドレス
success = db_manager.insert_user("Bob", "alice@example.com")
print(f"重複ユーザー挿入: {'成功' if success else '失敗'}")

# ユーザーを取得
user = db_manager.get_user_by_email("alice@example.com")
if user:
    print(f"ユーザー情報: {user}")
else:
    print("ユーザーが見つかりません")
```

#### 例3: API操作での例外処理

```python
import requests
import time
from typing import Optional, Dict, Any

class APIClient:
    """APIクライアントクラス"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """APIリクエストを実行"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logging.error(f"APIタイムアウト: {url}")
            return None
        except requests.exceptions.ConnectionError:
            logging.error(f"API接続エラー: {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTPエラー: {e.response.status_code} - {url}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"リクエストエラー: {e}")
            return None
        except ValueError as e:
            logging.error(f"JSON解析エラー: {e}")
            return None
        except Exception as e:
            logging.error(f"予期しないエラー: {e}")
            return None
    
    def get_user(self, user_id: int) -> Optional[Dict[Any, Any]]:
        """ユーザーを取得"""
        return self.make_request('GET', f'users/{user_id}')
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[Any, Any]]:
        """ユーザーを作成"""
        return self.make_request('POST', 'users', json=user_data)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[Any, Any]]:
        """ユーザーを更新"""
        return self.make_request('PUT', f'users/{user_id}', json=user_data)

# 使用例
print("\n=== API操作での例外処理 ===")
api_client = APIClient("https://httpbin.org")

# 正常なリクエスト
response = api_client.get_user(1)
if response:
    print(f"ユーザー取得成功: {response}")
else:
    print("ユーザー取得失敗")

# 存在しないエンドポイント
response = api_client.make_request('GET', 'nonexistent')
if response:
    print(f"リクエスト成功: {response}")
else:
    print("リクエスト失敗")
```

### よくある間違い

1. **例外の無視**: 例外をキャッチしても何もしない
2. **過度な例外処理**: すべての例外を一括でキャッチする
3. **ログの不適切な記録**: エラーの詳細を記録しない

### 応用例

```python
# 設定管理での例外処理
class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """設定を読み込み"""
        try:
            import json
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logging.info(f"設定を読み込みました: {self.config_file}")
        except FileNotFoundError:
            logging.warning(f"設定ファイルが見つかりません: {self.config_file}")
            self.config = self.get_default_config()
        except json.JSONDecodeError as e:
            logging.error(f"設定ファイルのJSON解析エラー: {e}")
            self.config = self.get_default_config()
        except Exception as e:
            logging.error(f"設定読み込みエラー: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """デフォルト設定を取得"""
        return {
            'debug': False,
            'log_level': 'INFO',
            'database_url': 'sqlite:///app.db',
            'max_connections': 10
        }
    
    def get(self, key: str, default=None):
        """設定値を取得"""
        try:
            return self.config[key]
        except KeyError:
            logging.warning(f"設定キーが見つかりません: {key}")
            return default
        except Exception as e:
            logging.error(f"設定取得エラー: {e}")
            return default

# 使用例
config_manager = ConfigManager("config.json")
debug_mode = config_manager.get('debug', False)
log_level = config_manager.get('log_level', 'INFO')
print(f"デバッグモード: {debug_mode}")
print(f"ログレベル: {log_level}")
```

### ベストプラクティス

- 具体的な例外をキャッチする
- 適切なログ記録を行う
- エラーの詳細を記録する
- デフォルト値やフォールバック処理を提供する

---

## 2. ログ記録で問題を追跡する

### 基本概念

適切なログ記録により、問題の原因を特定し、システムの動作を監視できます。ログレベルを適切に設定し、構造化されたログを記録することが重要です。

### 具体例

#### 例1: 基本的なログ設定

```python
import logging
import sys
from datetime import datetime

# ログ設定
def setup_logging(log_level=logging.INFO, log_file=None):
    """ログ設定を初期化"""
    # ログフォーマット
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ルートロガーを設定
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 既存のハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # ファイルハンドラー（指定された場合）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger

# 使用例
logger = setup_logging(log_level=logging.DEBUG, log_file="app.log")

logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.critical("致命的エラーメッセージ")
```

#### 例2: 構造化ログ記録

```python
import json
import logging
from typing import Dict, Any

class StructuredLogger:
    """構造化ログ記録クラス"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_event(self, level: str, message: str, **kwargs):
        """構造化ログを記録"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            **kwargs
        }
        
        if level.upper() == 'DEBUG':
            self.logger.debug(json.dumps(log_data, ensure_ascii=False))
        elif level.upper() == 'INFO':
            self.logger.info(json.dumps(log_data, ensure_ascii=False))
        elif level.upper() == 'WARNING':
            self.logger.warning(json.dumps(log_data, ensure_ascii=False))
        elif level.upper() == 'ERROR':
            self.logger.error(json.dumps(log_data, ensure_ascii=False))
        elif level.upper() == 'CRITICAL':
            self.logger.critical(json.dumps(log_data, ensure_ascii=False))
    
    def log_user_action(self, user_id: str, action: str, **kwargs):
        """ユーザーアクションを記録"""
        self.log_event('INFO', f"User action: {action}", 
                      user_id=user_id, action=action, **kwargs)
    
    def log_api_request(self, method: str, url: str, status_code: int, 
                       response_time: float, **kwargs):
        """APIリクエストを記録"""
        self.log_event('INFO', f"API request: {method} {url}", 
                      method=method, url=url, status_code=status_code, 
                      response_time=response_time, **kwargs)
    
    def log_error(self, error: Exception, context: str = "", **kwargs):
        """エラーを記録"""
        self.log_event('ERROR', f"Error in {context}: {str(error)}", 
                      error_type=type(error).__name__, 
                      error_message=str(error), context=context, **kwargs)

# 使用例
print("=== 構造化ログ記録 ===")
structured_logger = StructuredLogger("app")

# ユーザーアクションを記録
structured_logger.log_user_action("user123", "login", ip_address="192.168.1.1")

# APIリクエストを記録
structured_logger.log_api_request("GET", "/api/users", 200, 0.15, user_id="user123")

# エラーを記録
try:
    result = 1 / 0
except ZeroDivisionError as e:
    structured_logger.log_error(e, "calculation", operation="division")
```

#### 例3: アプリケーションログ管理

```python
class ApplicationLogger:
    """アプリケーションログ管理クラス"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.logger = logging.getLogger(app_name)
        self.setup_logging()
    
    def setup_logging(self):
        """ログ設定を初期化"""
        # ログフォーマット
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # ファイルハンドラー
        file_handler = logging.FileHandler(f"{self.app_name}.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # エラーファイルハンドラー
        error_handler = logging.FileHandler(f"{self.app_name}_error.log", encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def log_startup(self, version: str, config: Dict[str, Any]):
        """アプリケーション起動を記録"""
        self.logger.info(f"Application started", version=version, config=config)
    
    def log_shutdown(self, reason: str = "normal"):
        """アプリケーション終了を記録"""
        self.logger.info(f"Application shutdown", reason=reason)
    
    def log_database_operation(self, operation: str, table: str, 
                              success: bool, duration: float):
        """データベース操作を記録"""
        level = 'INFO' if success else 'ERROR'
        self.logger.log(getattr(logging, level), 
                       f"Database operation: {operation}", 
                       operation=operation, table=table, 
                       success=success, duration=duration)
    
    def log_performance(self, operation: str, duration: float, 
                      memory_usage: float = None):
        """パフォーマンスを記録"""
        self.logger.info(f"Performance: {operation}", 
                        operation=operation, duration=duration, 
                        memory_usage=memory_usage)

# 使用例
print("\n=== アプリケーションログ管理 ===")
app_logger = ApplicationLogger("myapp")

# アプリケーション起動
app_logger.log_startup("1.0.0", {"debug": True, "database": "sqlite"})

# データベース操作
app_logger.log_database_operation("INSERT", "users", True, 0.05)
app_logger.log_database_operation("UPDATE", "users", False, 0.1)

# パフォーマンス
app_logger.log_performance("data_processing", 2.5, 1024.5)

# アプリケーション終了
app_logger.log_shutdown("user_request")
```

### よくある間違い

1. **ログレベルの不適切な設定**: 本番環境でDEBUGレベルを使用
2. **ログの過多**: 必要以上に多くのログを記録
3. **構造化の不備**: ログの解析が困難

### 応用例

```python
# 監視システムでのログ活用
class MonitoringLogger:
    """監視システムログクラス"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.setup_logging()
    
    def setup_logging(self):
        """ログ設定を初期化"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 監視用ファイルハンドラー
        monitor_handler = logging.FileHandler(f"{self.service_name}_monitor.log", encoding='utf-8')
        monitor_handler.setFormatter(formatter)
        self.logger.addHandler(monitor_handler)
    
    def log_health_check(self, status: str, response_time: float, **kwargs):
        """ヘルスチェックを記録"""
        self.logger.info(f"Health check: {status}", 
                        status=status, response_time=response_time, **kwargs)
    
    def log_metric(self, metric_name: str, value: float, unit: str = ""):
        """メトリクスを記録"""
        self.logger.info(f"Metric: {metric_name}", 
                        metric_name=metric_name, value=value, unit=unit)
    
    def log_alert(self, alert_type: str, message: str, severity: str = "warning"):
        """アラートを記録"""
        self.logger.warning(f"Alert: {alert_type}", 
                           alert_type=alert_type, message=message, severity=severity)

# 使用例
monitor_logger = MonitoringLogger("web_service")

# ヘルスチェック
monitor_logger.log_health_check("healthy", 0.05, endpoint="/health")

# メトリクス
monitor_logger.log_metric("cpu_usage", 75.5, "percent")
monitor_logger.log_metric("memory_usage", 1024.5, "MB")

# アラート
monitor_logger.log_alert("high_cpu", "CPU usage is above 90%", "critical")
```

### ベストプラクティス

- 適切なログレベルを設定する
- 構造化されたログを記録する
- ログの回転とアーカイブを設定する
- 本番環境では適切なログレベルを使用する

---

## まとめ

Chapter 10では、堅牢性のベストプラクティスを学びました：

1. **例外処理**: エラーを適切にハンドリングする
2. **ログ記録**: 問題を追跡する
3. **バリデーション**: 入力データを検証する
4. **設定管理**: 環境に応じた動作を実現する
5. **リトライ機構**: 一時的な障害に対応する
6. **タイムアウト**: 無限待機を防ぐ
7. **サーキットブレーカー**: 障害の伝播を防ぐ
8. **ヘルスチェック**: システムの状態を監視する
9. **グレースフルシャットダウン**: 安全に終了する
10. **監視とアラート**: 問題を早期発見する

これらの原則を実践することで、堅牢で信頼性の高いシステムを構築できるようになります。


