# Python OpenAPI クライアント使用例

このディレクトリには、OpenAPI仕様書から生成されたPythonクライアントの使用例が含まれています。

## セットアップ

```bash
# クライアント生成
python ../../tools/generate-client.py \
  --spec ../../specifications/dimension-detection-api.yaml \
  --lang python \
  --output ./client

# 依存関係のインストール
cd client
pip install -r requirements.txt
```

## 使用例

### 1. 基本的なAPI呼び出し

```python
from openapi_client import ApiClient, Configuration
from openapi_client.api.analysis_api import AnalysisApi
from openapi_client.model.analysis_result import AnalysisResult

# 設定
configuration = Configuration(
    host="https://api.example.com/v1"
)
configuration.access_token = "your-access-token"

# APIクライアントの作成
with ApiClient(configuration) as api_client:
    api_instance = AnalysisApi(api_client)
    
    # ファイルアップロード
    with open("floorplan.png", "rb") as f:
        file_data = f.read()
    
    try:
        # 解析実行
        result = api_instance.analyze_floorplan(
            file=file_data,
            options='{"detection_threshold": 0.8}'
        )
        
        print(f"解析成功: {result.message}")
        print(f"検出された寸法線数: {result.metadata.detected_lines}")
        
        # 結果の処理
        for line_id, segments in result.data.segments_by_line.items():
            print(f"寸法線 {line_id}:")
            for segment in segments:
                print(f"  座標: ({segment.q1.x}, {segment.q1.y}) -> ({segment.q2.x}, {segment.q2.y})")
                print(f"  長さ: {segment.line_length}")
                
    except Exception as e:
        print(f"エラー: {e}")
```

### 2. エラーハンドリング

```python
from openapi_client.exceptions import ApiException

try:
    result = api_instance.analyze_floorplan(file=file_data)
except ApiException as e:
    if e.status == 400:
        print(f"リクエストエラー: {e.body}")
    elif e.status == 401:
        print("認証エラー: トークンを確認してください")
    elif e.status == 429:
        print("レート制限: しばらく待ってから再試行してください")
    else:
        print(f"APIエラー ({e.status}): {e.body}")
```

### 3. 非同期処理

```python
import asyncio
from openapi_client.api_async.analysis_api import AnalysisApi as AsyncAnalysisApi

async def analyze_async():
    configuration = Configuration(host="https://api.example.com/v1")
    configuration.access_token = "your-access-token"
    
    async with ApiClient(configuration) as api_client:
        api_instance = AsyncAnalysisApi(api_client)
        
        with open("floorplan.png", "rb") as f:
            file_data = f.read()
        
        try:
            result = await api_instance.analyze_floorplan(file=file_data)
            return result
        except Exception as e:
            print(f"エラー: {e}")
            return None

# 実行
result = asyncio.run(analyze_async())
```

### 4. バッチ処理

```python
import os
from pathlib import Path

def batch_analyze(directory_path: str):
    """ディレクトリ内の全画像を解析"""
    results = []
    
    for file_path in Path(directory_path).glob("*.png"):
        print(f"解析中: {file_path}")
        
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        try:
            result = api_instance.analyze_floorplan(file=file_data)
            results.append({
                'file': file_path.name,
                'result': result,
                'success': True
            })
        except Exception as e:
            results.append({
                'file': file_path.name,
                'error': str(e),
                'success': False
            })
    
    return results

# 使用例
results = batch_analyze("./images")
for result in results:
    if result['success']:
        print(f"✅ {result['file']}: {result['result'].metadata.detected_lines} 本の寸法線を検出")
    else:
        print(f"❌ {result['file']}: {result['error']}")
```

## テスト

```python
import unittest
from openapi_client import ApiClient, Configuration
from openapi_client.api.analysis_api import AnalysisApi

class TestDimensionDetectionAPI(unittest.TestCase):
    def setUp(self):
        self.configuration = Configuration(host="http://localhost:8000/v1")
        self.api_client = ApiClient(self.configuration)
        self.api_instance = AnalysisApi(self.api_client)
    
    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = self.api_instance.health_check()
        self.assertEqual(response.status, "healthy")
    
    def test_analyze_with_valid_file(self):
        """有効なファイルでの解析テスト"""
        # テスト用の画像ファイルを準備
        with open("test_floorplan.png", "rb") as f:
            file_data = f.read()
        
        result = self.api_instance.analyze_floorplan(file=file_data)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)

if __name__ == '__main__':
    unittest.main()
```

## 設定オプション

```python
# カスタム設定
configuration = Configuration(
    host="https://api.example.com/v1",
    api_key={"BearerAuth": "your-token"},
    api_key_prefix={"BearerAuth": "Bearer"},
    username="your-username",  # Basic認証の場合
    password="your-password",
    discard_unknown_keys=True,
    disabled_client_side_validations="all"
)

# プロキシ設定
configuration.proxy = "http://proxy.example.com:8080"

# SSL設定
configuration.ssl_ca_cert = "/path/to/ca-cert.pem"
configuration.cert_file = "/path/to/client-cert.pem"
configuration.key_file = "/path/to/client-key.pem"
```
