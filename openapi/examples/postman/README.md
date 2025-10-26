# Postman コレクション使用例

このディレクトリには、OpenAPI仕様書に対応したPostmanコレクションが含まれています。

## セットアップ

### 1. Postmanへのインポート

1. Postmanを開く
2. 「Import」ボタンをクリック
3. `dimension-detection-api.json` ファイルを選択
4. 「Import」をクリック

### 2. 環境変数の設定

コレクションをインポート後、以下の環境変数を設定してください：

- `base_url`: APIのベースURL（例: `https://api.example.com/v1`）
- `access_token`: 認証トークン

## 使用例

### 1. ヘルスチェック

```http
GET {{base_url}}/health
```

**期待されるレスポンス:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-14T10:30:00Z",
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

### 2. 寸法線解析

```http
POST {{base_url}}/analyze
Authorization: Bearer {{access_token}}
Content-Type: multipart/form-data

file: [画像ファイル]
options: {"detection_threshold": 0.8, "min_line_length": 50}
metadata: {"project": "Office Building A", "author": "John Doe"}
```

**期待されるレスポンス:**
```json
{
  "success": true,
  "message": "Analysis completed successfully",
  "data": {
    "segmentsByLine": {
      "1": [
        {
          "q1": {"x": 100, "y": 200, "unit": "px"},
          "q2": {"x": 300, "y": 200, "unit": "px"},
          "line_length": 200
        }
      ],
      "2": [
        {
          "q1": {"x": 150, "y": 250, "unit": "px"},
          "q2": {"x": 150, "y": 400, "unit": "px"},
          "line_length": 150
        }
      ]
    }
  },
  "metadata": {
    "processing_time_ms": 2340,
    "image_size": {"width": 1920, "height": 1080},
    "detected_lines": 2
  }
}
```

## テストスクリプト

### 1. レスポンス検証

```javascript
// ヘルスチェックのテスト
pm.test("Health check returns healthy status", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.status).to.eql("healthy");
});

// 解析結果のテスト
pm.test("Analysis returns success", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.success).to.be.true;
});

pm.test("Analysis returns data", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.data).to.be.an('object');
    pm.expect(responseJson.data.segmentsByLine).to.be.an('object');
});

pm.test("Analysis returns metadata", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.metadata).to.be.an('object');
    pm.expect(responseJson.metadata.processing_time_ms).to.be.a('number');
});
```

### 2. 環境変数の設定

```javascript
// レスポンスからトークンを取得して環境変数に設定
if (pm.response.code === 200) {
    const responseJson = pm.response.json();
    if (responseJson.access_token) {
        pm.environment.set("access_token", responseJson.access_token);
    }
}
```

### 3. リクエスト前の処理

```javascript
// ファイルサイズのチェック
const fileSize = pm.request.body.formdata.find(item => item.key === "file").src.length;
pm.test("File size is within limit", function () {
    pm.expect(fileSize).to.be.below(10 * 1024 * 1024); // 10MB
});
```

## コレクション実行

### 1. 全テストの実行

1. Postmanでコレクションを選択
2. 「Run」ボタンをクリック
3. 実行したいリクエストを選択
4. 「Run」をクリック

### 2. モニタリング

Postman Monitorを使用してAPIの定期監視を設定できます：

1. コレクションの「Monitor」タブをクリック
2. 監視設定を構成：
   - 実行頻度（例: 5分ごと）
   - 通知設定
   - 環境変数
3. 「Create Monitor」をクリック

## 環境設定

### 開発環境
```json
{
  "base_url": "http://localhost:8000/v1",
  "access_token": "dev-token-123"
}
```

### ステージング環境
```json
{
  "base_url": "https://staging-api.example.com/v1",
  "access_token": "staging-token-456"
}
```

### 本番環境
```json
{
  "base_url": "https://api.example.com/v1",
  "access_token": "prod-token-789"
}
```

## トラブルシューティング

### よくあるエラー

1. **401 Unauthorized**
   - トークンが正しく設定されているか確認
   - トークンの有効期限を確認

2. **400 Bad Request**
   - ファイル形式が対応しているか確認（PNG, JPEG, PDF）
   - ファイルサイズが制限内か確認（10MB以下）

3. **429 Too Many Requests**
   - レート制限に達している
   - しばらく待ってから再試行

### デバッグのヒント

1. **コンソールログの確認**
   ```javascript
   console.log("Response:", pm.response.json());
   console.log("Request:", pm.request);
   ```

2. **レスポンス時間の監視**
   ```javascript
   pm.test("Response time is acceptable", function () {
       pm.expect(pm.response.responseTime).to.be.below(5000); // 5秒以下
   });
   ```

3. **ステータスコードの確認**
   ```javascript
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```
