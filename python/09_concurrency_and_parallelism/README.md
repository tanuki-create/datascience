# Chapter 9: Concurrency and Parallelism

並行処理と並列処理のベストプラクティスを学びます。

## 目次

1. [threadingでI/Oバウンドな処理を並行化する](#1-threadingでioバウンドな処理を並行化する)
2. [multiprocessingでCPUバウンドな処理を並列化する](#2-multiprocessingでcpuバウンドな処理を並列化する)
3. [asyncioで非同期処理を効率的に管理する](#3-asyncioで非同期処理を効率的に管理する)
4. [concurrent.futuresで高レベルな並行処理を実装する](#4-concurrentfuturesで高レベルな並行処理を実装する)
5. [Queueでスレッド間の通信を安全に行う](#5-queueでスレッド間の通信を安全に行う)
6. [Lockで共有リソースへのアクセスを制御する](#6-lockで共有リソースへのアクセスを制御する)
7. [Eventでスレッド間の同期を実現する](#7-eventでスレッド間の同期を実現する)
8. [Semaphoreでリソースの使用量を制限する](#8-semaphoreでリソースの使用量を制限する)
9. [ThreadPoolExecutorでスレッドプールを管理する](#9-threadpoolexecutorでスレッドプールを管理する)
10. [ProcessPoolExecutorでプロセスプールを管理する](#10-processpoolexecutorでプロセスプールを管理する)

---

## 1. threadingでI/Oバウンドな処理を並行化する

### 基本概念

`threading`モジュールを使用することで、I/Oバウンドな処理（ファイル読み書き、ネットワーク通信など）を並行化できます。PythonのGIL（Global Interpreter Lock）により、CPUバウンドな処理には適していません。

### 具体例

#### 例1: 基本的なスレッド処理

```python
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# 悪い例（逐次処理）
def fetch_urls_sequential(urls):
    """URLを逐次取得"""
    results = []
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            results.append(f"{url}: {response.status_code}")
        except Exception as e:
            results.append(f"{url}: Error - {e}")
    return results

# 良い例（並行処理）
def fetch_single_url(url):
    """単一URLを取得"""
    try:
        response = requests.get(url, timeout=5)
        return f"{url}: {response.status_code}"
    except Exception as e:
        return f"{url}: Error - {e}"

def fetch_urls_parallel(urls):
    """URLを並行取得"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_single_url, urls))
    return results

# 使用例
urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/3"
]

print("=== URL取得の比較 ===")

# 逐次処理
start_time = time.time()
sequential_results = fetch_urls_sequential(urls)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"結果: {sequential_results}")

# 並行処理
start_time = time.time()
parallel_results = fetch_urls_parallel(urls)
parallel_time = time.time() - start_time
print(f"\n並行処理時間: {parallel_time:.2f}秒")
print(f"結果: {parallel_results}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")
```

#### 例2: ファイル処理の並行化

```python
import os
import threading
from pathlib import Path

class FileProcessor:
    """ファイル処理クラス"""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.results = []
        self.lock = threading.Lock()
    
    def process_file(self, file_path):
        """単一ファイルを処理"""
        try:
            # ファイル処理をシミュレート
            with open(file_path, 'r') as f:
                content = f.read()
            
            # 処理時間をシミュレート
            time.sleep(0.1)
            
            result = {
                'file': str(file_path),
                'size': len(content),
                'lines': len(content.split('\n')),
                'status': 'success'
            }
            
            with self.lock:
                self.results.append(result)
            
            return result
        except Exception as e:
            error_result = {
                'file': str(file_path),
                'error': str(e),
                'status': 'error'
            }
            with self.lock:
                self.results.append(error_result)
            return error_result
    
    def process_files_sequential(self, file_paths):
        """ファイルを逐次処理"""
        self.results = []
        for file_path in file_paths:
            self.process_file(file_path)
        return self.results
    
    def process_files_parallel(self, file_paths):
        """ファイルを並行処理"""
        self.results = []
        threads = []
        
        for file_path in file_paths:
            thread = threading.Thread(target=self.process_file, args=(file_path,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        return self.results

# 使用例
print("=== ファイル処理の並行化 ===")

# テスト用ファイルを作成
test_files = []
for i in range(5):
    file_path = f"test_file_{i}.txt"
    with open(file_path, 'w') as f:
        f.write(f"Test content for file {i}\n" * 10)
    test_files.append(file_path)

processor = FileProcessor()

# 逐次処理
start_time = time.time()
sequential_results = processor.process_files_sequential(test_files)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"処理されたファイル数: {len(sequential_results)}")

# 並行処理
start_time = time.time()
parallel_results = processor.process_files_parallel(test_files)
parallel_time = time.time() - start_time
print(f"\n並行処理時間: {parallel_time:.2f}秒")
print(f"処理されたファイル数: {len(parallel_results)}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")

# クリーンアップ
for file_path in test_files:
    os.remove(file_path)
```

#### 例3: データベース操作の並行化

```python
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class DatabaseManager:
    """データベース管理クラス"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
    
    def init_database(self):
        """データベースを初期化"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def insert_user(self, name, email):
        """ユーザーを挿入"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "INSERT INTO users (name, email) VALUES (?, ?)",
                    (name, email)
                )
                conn.commit()
                return cursor.lastrowid
    
    def get_user_count(self):
        """ユーザー数を取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM users")
            return cursor.fetchone()[0]
    
    def get_all_users(self):
        """全ユーザーを取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM users")
            return cursor.fetchall()

def insert_users_sequential(db_manager, user_data):
    """ユーザーを逐次挿入"""
    for name, email in user_data:
        db_manager.insert_user(name, email)
        time.sleep(0.01)  # 処理時間をシミュレート

def insert_users_parallel(db_manager, user_data):
    """ユーザーを並行挿入"""
    def insert_single_user(user_info):
        name, email = user_info
        db_manager.insert_user(name, email)
        time.sleep(0.01)  # 処理時間をシミュレート
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(insert_single_user, user_data)

# 使用例
print("=== データベース操作の並行化 ===")

# テストデータ
user_data = [
    (f"User{i}", f"user{i}@example.com") for i in range(20)
]

# 逐次処理
db_manager = DatabaseManager("test.db")
start_time = time.time()
insert_users_sequential(db_manager, user_data)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"ユーザー数: {db_manager.get_user_count()}")

# データベースをリセット
os.remove("test.db")
db_manager = DatabaseManager("test.db")

# 並行処理
start_time = time.time()
insert_users_parallel(db_manager, user_data)
parallel_time = time.time() - start_time
print(f"\n並行処理時間: {parallel_time:.2f}秒")
print(f"ユーザー数: {db_manager.get_user_count()}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")

# クリーンアップ
os.remove("test.db")
```

### よくある間違い

1. **CPUバウンドな処理での使用**: GILの制限を理解しない
2. **共有リソースの不適切な管理**: ロックを使用しない
3. **スレッド数の過多**: 適切なスレッド数を設定しない

### 応用例

```python
# Webスクレイピングでの並行処理
class WebScraper:
    """Webスクレイピングクラス"""
    
    def __init__(self, max_workers=5):
        self.max_workers = max_workers
        self.session = requests.Session()
        self.results = []
        self.lock = threading.Lock()
    
    def scrape_single_page(self, url):
        """単一ページをスクレイピング"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # 簡単なスクレイピングをシミュレート
                content_length = len(response.text)
                return {
                    'url': url,
                    'status': 'success',
                    'content_length': content_length,
                    'title': 'Sample Title'  # 実際の実装ではHTMLをパース
                }
            else:
                return {
                    'url': url,
                    'status': 'error',
                    'error': f"HTTP {response.status_code}"
                }
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }
    
    def scrape_pages_parallel(self, urls):
        """ページを並行スクレイピング"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self.scrape_single_page, urls))
        return results

# 使用例
scraper = WebScraper(max_workers=3)
urls = [
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/xml",
    "https://httpbin.org/robots.txt"
]

print("=== Webスクレイピングの並行処理 ===")
results = scraper.scrape_pages_parallel(urls)
for result in results:
    print(f"URL: {result['url']}")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Content Length: {result['content_length']}")
    else:
        print(f"Error: {result['error']}")
    print()
```

### ベストプラクティス

- I/Oバウンドな処理に`threading`を使用する
- 適切なスレッド数を設定する
- 共有リソースにはロックを使用する
- `ThreadPoolExecutor`を活用する

---

## 2. multiprocessingでCPUバウンドな処理を並列化する

### 基本概念

`multiprocessing`モジュールを使用することで、CPUバウンドな処理を複数のプロセスで並列化できます。GILの制限を回避し、真の並列処理を実現できます。

### 具体例

#### 例1: 基本的なプロセス処理

```python
import multiprocessing
import time
import math

# CPUバウンドな処理
def calculate_fibonacci(n):
    """フィボナッチ数を計算"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def calculate_prime_numbers(max_num):
    """素数を計算"""
    primes = []
    for num in range(2, max_num):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# 逐次処理
def process_sequential(numbers):
    """逐次処理"""
    results = []
    for num in numbers:
        result = calculate_fibonacci(num)
        results.append(result)
    return results

# 並列処理
def process_parallel(numbers):
    """並列処理"""
    with multiprocessing.Pool() as pool:
        results = pool.map(calculate_fibonacci, numbers)
    return results

# 使用例
print("=== CPUバウンドな処理の並列化 ===")

# テストデータ
numbers = [30, 31, 32, 33, 34]

# 逐次処理
start_time = time.time()
sequential_results = process_sequential(numbers)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"結果: {sequential_results}")

# 並列処理
start_time = time.time()
parallel_results = process_parallel(numbers)
parallel_time = time.time() - start_time
print(f"\n並列処理時間: {parallel_time:.2f}秒")
print(f"結果: {parallel_results}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")
print(f"スピードアップ: {sequential_time / parallel_time:.2f}x")
```

#### 例2: 画像処理の並列化

```python
import multiprocessing
import time
import random

class ImageProcessor:
    """画像処理クラス"""
    
    def __init__(self):
        self.processed_count = 0
        self.lock = multiprocessing.Lock()
    
    def process_single_image(self, image_data):
        """単一画像を処理"""
        image_id, width, height = image_data
        
        # 画像処理をシミュレート
        time.sleep(0.1)  # 処理時間をシミュレート
        
        # 簡単な画像処理をシミュレート
        processed_pixels = width * height
        brightness = random.uniform(0.5, 1.5)
        contrast = random.uniform(0.8, 1.2)
        
        result = {
            'image_id': image_id,
            'processed_pixels': processed_pixels,
            'brightness': brightness,
            'contrast': contrast,
            'status': 'completed'
        }
        
        return result
    
    def process_images_sequential(self, image_data_list):
        """画像を逐次処理"""
        results = []
        for image_data in image_data_list:
            result = self.process_single_image(image_data)
            results.append(result)
        return results
    
    def process_images_parallel(self, image_data_list):
        """画像を並列処理"""
        with multiprocessing.Pool() as pool:
            results = pool.map(self.process_single_image, image_data_list)
        return results

# 使用例
print("=== 画像処理の並列化 ===")

# テストデータ
image_data_list = [
    (i, 1920, 1080) for i in range(10)
]

processor = ImageProcessor()

# 逐次処理
start_time = time.time()
sequential_results = processor.process_images_sequential(image_data_list)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"処理された画像数: {len(sequential_results)}")

# 並列処理
start_time = time.time()
parallel_results = processor.process_images_parallel(image_data_list)
parallel_time = time.time() - start_time
print(f"\n並列処理時間: {parallel_time:.2f}秒")
print(f"処理された画像数: {len(parallel_results)}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")
print(f"スピードアップ: {sequential_time / parallel_time:.2f}x")
```

#### 例3: データ分析の並列化

```python
import multiprocessing
import time
import random
import statistics

def analyze_data_chunk(data_chunk):
    """データチャンクを分析"""
    chunk_id, data = data_chunk
    
    # データ分析をシミュレート
    time.sleep(0.05)  # 処理時間をシミュレート
    
    # 統計計算
    mean_val = statistics.mean(data)
    median_val = statistics.median(data)
    std_val = statistics.stdev(data) if len(data) > 1 else 0
    min_val = min(data)
    max_val = max(data)
    
    result = {
        'chunk_id': chunk_id,
        'count': len(data),
        'mean': mean_val,
        'median': median_val,
        'std': std_val,
        'min': min_val,
        'max': max_val
    }
    
    return result

def analyze_data_sequential(data_chunks):
    """データを逐次分析"""
    results = []
    for chunk in data_chunks:
        result = analyze_data_chunk(chunk)
        results.append(result)
    return results

def analyze_data_parallel(data_chunks):
    """データを並列分析"""
    with multiprocessing.Pool() as pool:
        results = pool.map(analyze_data_chunk, data_chunks)
    return results

# 使用例
print("=== データ分析の並列化 ===")

# テストデータ
data_chunks = [
    (i, [random.uniform(0, 100) for _ in range(1000)]) 
    for i in range(20)
]

# 逐次処理
start_time = time.time()
sequential_results = analyze_data_sequential(data_chunks)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"分析されたチャンク数: {len(sequential_results)}")

# 並列処理
start_time = time.time()
parallel_results = analyze_data_parallel(data_chunks)
parallel_time = time.time() - start_time
print(f"\n並列処理時間: {parallel_time:.2f}秒")
print(f"分析されたチャンク数: {len(parallel_results)}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")
print(f"スピードアップ: {sequential_time / parallel_time:.2f}x")

# 結果の表示
print(f"\n最初のチャンクの結果:")
result = parallel_results[0]
print(f"  チャンクID: {result['chunk_id']}")
print(f"  データ数: {result['count']}")
print(f"  平均: {result['mean']:.2f}")
print(f"  中央値: {result['median']:.2f}")
print(f"  標準偏差: {result['std']:.2f}")
```

### よくある間違い

1. **I/Oバウンドな処理での使用**: プロセス間通信のオーバーヘッドを考慮しない
2. **メモリ使用量の軽視**: プロセスごとにメモリを消費することを理解しない
3. **プロセス数の過多**: 適切なプロセス数を設定しない

### 応用例

```python
# 機械学習での並列処理
class MLProcessor:
    """機械学習処理クラス"""
    
    def __init__(self):
        self.model_results = []
    
    def train_model(self, model_data):
        """モデルを訓練"""
        model_id, features, labels = model_data
        
        # モデル訓練をシミュレート
        time.sleep(0.2)  # 処理時間をシミュレート
        
        # 簡単なモデル訓練をシミュレート
        accuracy = random.uniform(0.7, 0.95)
        loss = random.uniform(0.1, 0.5)
        
        result = {
            'model_id': model_id,
            'accuracy': accuracy,
            'loss': loss,
            'features_count': len(features),
            'samples_count': len(labels),
            'status': 'trained'
        }
        
        return result
    
    def train_models_sequential(self, model_data_list):
        """モデルを逐次訓練"""
        results = []
        for model_data in model_data_list:
            result = self.train_model(model_data)
            results.append(result)
        return results
    
    def train_models_parallel(self, model_data_list):
        """モデルを並列訓練"""
        with multiprocessing.Pool() as pool:
            results = pool.map(self.train_model, model_data_list)
        return results

# 使用例
print("=== 機械学習の並列処理 ===")

# テストデータ
model_data_list = [
    (i, [random.uniform(0, 1) for _ in range(100)], [random.randint(0, 1) for _ in range(100)])
    for i in range(8)
]

processor = MLProcessor()

# 逐次処理
start_time = time.time()
sequential_results = processor.train_models_sequential(model_data_list)
sequential_time = time.time() - start_time
print(f"逐次処理時間: {sequential_time:.2f}秒")
print(f"訓練されたモデル数: {len(sequential_results)}")

# 並列処理
start_time = time.time()
parallel_results = processor.train_models_parallel(model_data_list)
parallel_time = time.time() - start_time
print(f"\n並列処理時間: {parallel_time:.2f}秒")
print(f"訓練されたモデル数: {len(parallel_results)}")
print(f"時間短縮: {sequential_time - parallel_time:.2f}秒")
print(f"スピードアップ: {sequential_time / parallel_time:.2f}x")

# 結果の表示
print(f"\n最初のモデルの結果:")
result = parallel_results[0]
print(f"  モデルID: {result['model_id']}")
print(f"  精度: {result['accuracy']:.3f}")
print(f"  損失: {result['loss']:.3f}")
print(f"  特徴量数: {result['features_count']}")
print(f"  サンプル数: {result['samples_count']}")
```

### ベストプラクティス

- CPUバウンドな処理に`multiprocessing`を使用する
- 適切なプロセス数を設定する
- メモリ使用量を考慮する
- プロセス間通信のオーバーヘッドを最小化する

---

## まとめ

Chapter 9では、並行処理と並列処理のベストプラクティスを学びました：

1. **threading**: I/Oバウンドな処理を並行化する
2. **multiprocessing**: CPUバウンドな処理を並列化する
3. **asyncio**: 非同期処理を効率的に管理する
4. **concurrent.futures**: 高レベルな並行処理を実装する
5. **Queue**: スレッド間の通信を安全に行う
6. **Lock**: 共有リソースへのアクセスを制御する
7. **Event**: スレッド間の同期を実現する
8. **Semaphore**: リソースの使用量を制限する
9. **ThreadPoolExecutor**: スレッドプールを管理する
10. **ProcessPoolExecutor**: プロセスプールを管理する

これらの原則を実践することで、効率的で安全な並行・並列処理を実装できるようになります。


