# TypeScript OpenAPI クライアント使用例

このディレクトリには、OpenAPI仕様書から生成されたTypeScriptクライアントの使用例が含まれています。

## セットアップ

```bash
# クライアント生成
python ../../tools/generate-client.py \
  --spec ../../specifications/dimension-detection-api.yaml \
  --lang typescript \
  --output ./client

# 依存関係のインストール
cd client
npm install
npm run build
```

## 使用例

### 1. 基本的なAPI呼び出し

```typescript
import { Configuration, AnalysisApi, AnalysisResult } from './client';

// 設定
const configuration = new Configuration({
  basePath: 'https://api.example.com/v1',
  accessToken: 'your-access-token'
});

// APIクライアントの作成
const apiInstance = new AnalysisApi(configuration);

// ファイルアップロード
const fileInput = document.getElementById('fileInput') as HTMLInputElement;
const file = fileInput.files?.[0];

if (file) {
  try {
    // 解析実行
    const result: AnalysisResult = await apiInstance.analyzeFloorplan(
      file,
      '{"detection_threshold": 0.8}'
    );
    
    console.log(`解析成功: ${result.message}`);
    console.log(`検出された寸法線数: ${result.metadata?.detectedLines}`);
    
    // 結果の処理
    Object.entries(result.data?.segmentsByLine || {}).forEach(([lineId, segments]) => {
      console.log(`寸法線 ${lineId}:`);
      segments.forEach(segment => {
        console.log(`  座標: (${segment.q1.x}, ${segment.q1.y}) -> (${segment.q2.x}, ${segment.q2.y})`);
        console.log(`  長さ: ${segment.lineLength}`);
      });
    });
    
  } catch (error) {
    console.error('エラー:', error);
  }
}
```

### 2. エラーハンドリング

```typescript
import { ApiException } from './client';

try {
  const result = await apiInstance.analyzeFloorplan(file);
} catch (error) {
  if (error instanceof ApiException) {
    switch (error.status) {
      case 400:
        console.error('リクエストエラー:', error.body);
        break;
      case 401:
        console.error('認証エラー: トークンを確認してください');
        break;
      case 429:
        console.error('レート制限: しばらく待ってから再試行してください');
        break;
      default:
        console.error(`APIエラー (${error.status}):`, error.body);
    }
  } else {
    console.error('予期しないエラー:', error);
  }
}
```

### 3. React コンポーネントでの使用

```typescript
import React, { useState, useCallback } from 'react';
import { AnalysisApi, Configuration, AnalysisResult } from './client';

interface AnalysisComponentProps {
  apiKey: string;
}

const AnalysisComponent: React.FC<AnalysisComponentProps> = ({ apiKey }) => {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const configuration = new Configuration({
    basePath: 'https://api.example.com/v1',
    accessToken: apiKey
  });

  const apiInstance = new AnalysisApi(configuration);

  const handleFileUpload = useCallback(async (file: File) => {
    setLoading(true);
    setError(null);
    
    try {
      const analysisResult = await apiInstance.analyzeFloorplan(
        file,
        '{"detection_threshold": 0.8}'
      );
      setResult(analysisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [apiInstance]);

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFileUpload(file);
        }}
        disabled={loading}
      />
      
      {loading && <p>解析中...</p>}
      
      {error && <p style={{ color: 'red' }}>エラー: {error}</p>}
      
      {result && (
        <div>
          <h3>解析結果</h3>
          <p>検出された寸法線数: {result.metadata?.detectedLines}</p>
          <p>処理時間: {result.metadata?.processingTimeMs}ms</p>
          
          <div>
            <h4>寸法線詳細</h4>
            {Object.entries(result.data?.segmentsByLine || {}).map(([lineId, segments]) => (
              <div key={lineId}>
                <h5>寸法線 {lineId}</h5>
                {segments.map((segment, index) => (
                  <div key={index}>
                    <p>座標: ({segment.q1.x}, {segment.q1.y}) → ({segment.q2.x}, {segment.q2.y})</p>
                    <p>長さ: {segment.lineLength}</p>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisComponent;
```

### 4. Node.js での使用

```typescript
import fs from 'fs';
import { AnalysisApi, Configuration } from './client';

async function analyzeFloorplan(filePath: string): Promise<void> {
  const configuration = new Configuration({
    basePath: 'https://api.example.com/v1',
    accessToken: process.env.API_TOKEN
  });

  const apiInstance = new AnalysisApi(configuration);

  try {
    // ファイル読み込み
    const fileBuffer = fs.readFileSync(filePath);
    const file = new File([fileBuffer], 'floorplan.png', { type: 'image/png' });

    // 解析実行
    const result = await apiInstance.analyzeFloorplan(file);
    
    console.log('解析成功:', result.message);
    console.log('検出された寸法線数:', result.metadata?.detectedLines);
    
    // 結果をJSONファイルに保存
    fs.writeFileSync(
      'analysis_result.json',
      JSON.stringify(result, null, 2)
    );
    
  } catch (error) {
    console.error('解析エラー:', error);
  }
}

// 使用例
analyzeFloorplan('./floorplan.png');
```

### 5. バッチ処理

```typescript
import fs from 'fs';
import path from 'path';
import { AnalysisApi, Configuration, AnalysisResult } from './client';

interface BatchResult {
  file: string;
  result?: AnalysisResult;
  error?: string;
  success: boolean;
}

async function batchAnalyze(directoryPath: string): Promise<BatchResult[]> {
  const configuration = new Configuration({
    basePath: 'https://api.example.com/v1',
    accessToken: process.env.API_TOKEN
  });

  const apiInstance = new AnalysisApi(configuration);
  const results: BatchResult[] = [];

  const files = fs.readdirSync(directoryPath)
    .filter(file => /\.(png|jpg|jpeg)$/i.test(file));

  for (const file of files) {
    console.log(`解析中: ${file}`);
    
    try {
      const filePath = path.join(directoryPath, file);
      const fileBuffer = fs.readFileSync(filePath);
      const fileObj = new File([fileBuffer], file, { type: 'image/png' });

      const result = await apiInstance.analyzeFloorplan(fileObj);
      
      results.push({
        file,
        result,
        success: true
      });
      
    } catch (error) {
      results.push({
        file,
        error: error instanceof Error ? error.message : 'Unknown error',
        success: false
      });
    }
  }

  return results;
}

// 使用例
batchAnalyze('./images').then(results => {
  results.forEach(result => {
    if (result.success) {
      console.log(`✅ ${result.file}: ${result.result?.metadata?.detectedLines} 本の寸法線を検出`);
    } else {
      console.log(`❌ ${result.file}: ${result.error}`);
    }
  });
});
```

## テスト

```typescript
import { AnalysisApi, Configuration } from './client';

describe('DimensionDetectionAPI', () => {
  let apiInstance: AnalysisApi;

  beforeEach(() => {
    const configuration = new Configuration({
      basePath: 'http://localhost:8000/v1'
    });
    apiInstance = new AnalysisApi(configuration);
  });

  test('health check should return healthy status', async () => {
    const response = await apiInstance.healthCheck();
    expect(response.status).toBe('healthy');
  });

  test('analyze with valid file should return result', async () => {
    // テスト用のファイルを準備
    const file = new File(['test'], 'test.png', { type: 'image/png' });
    
    const result = await apiInstance.analyzeFloorplan(file);
    expect(result.success).toBe(true);
    expect(result.data).toBeDefined();
  });
});
```

## 設定オプション

```typescript
// カスタム設定
const configuration = new Configuration({
  basePath: 'https://api.example.com/v1',
  accessToken: 'your-token',
  username: 'your-username',  // Basic認証の場合
  password: 'your-password',
  apiKey: {
    'BearerAuth': 'your-token'
  },
  baseOptions: {
    timeout: 30000,  // 30秒のタイムアウト
    headers: {
      'User-Agent': 'MyApp/1.0'
    }
  }
});

// プロキシ設定
configuration.proxy = 'http://proxy.example.com:8080';

// SSL設定
configuration.sslCaCert = '/path/to/ca-cert.pem';
configuration.certFile = '/path/to/client-cert.pem';
configuration.keyFile = '/path/to/client-key.pem';
```
