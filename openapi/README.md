# 🧭 OpenAPI 仕様書・事例集

## 📋 概要

このディレクトリには、OpenAPI 3.x 仕様に基づいた **実践的なAPI設計事例集** が含まれています。
構造設計・スキーマ整備を重視する開発者向けに、主要な **10カテゴリ × 実例テンプレート＋設計解説** をまとめています。

## 📁 ファイル構成

```
openapi/
├── README.md                           # このファイル
├── specifications/                     # OpenAPI仕様書
│   ├── dimension-detection-api.yaml    # 寸法線検出API（メイン）
│   ├── simple-crud-api.yaml           # シンプルCRUD API
│   ├── geojson-api.yaml               # GeoJSON対応API
│   ├── graphql-gateway-api.yaml       # GraphQL Gateway向け
│   ├── ai-model-api.yaml              # AIモデル推論API
│   ├── webhook-api.yaml               # イベントWebhook
│   ├── file-upload-api.yaml           # ファイルアップロード
│   ├── measurement-api.yaml           # ユニット付きスキーマ
│   ├── versioning-api.yaml            # バージョニング対応
│   └── oauth2-api.yaml                # OAuth2認証付きAPI
├── examples/                          # 実装例・サンプル
│   ├── python/                        # Python実装例
│   ├── typescript/                    # TypeScript実装例
│   └── postman/                       # Postmanコレクション
└── tools/                             # 開発ツール・スクリプト
    ├── generate-client.py             # クライアント生成
    └── validate-spec.py               # 仕様検証
```

## 🚀 クイックスタート

### 1. 仕様書の確認
```bash
# メインの寸法線検出API仕様を確認
cat specifications/dimension-detection-api.yaml

# Swagger UIで可視化（ローカル）
npx swagger-ui-serve specifications/dimension-detection-api.yaml
```

### 2. クライアント生成
```bash
# Pythonクライアント生成
python tools/generate-client.py --spec specifications/dimension-detection-api.yaml --lang python

# TypeScriptクライアント生成
python tools/generate-client.py --spec specifications/dimension-detection-api.yaml --lang typescript
```

### 3. 仕様検証
```bash
# OpenAPI仕様の妥当性チェック
python tools/validate-spec.py specifications/dimension-detection-api.yaml
```

## 📚 カテゴリ別ガイド

### ① シンプルな CRUD API
- **対象**: 典型的なRESTベースアプリケーション
- **目的**: Entityの一覧・登録・更新・削除を自動生成できる最小構成
- **ファイル**: `specifications/simple-crud-api.yaml`

### ② 座標・図面データAPI（メイン）
- **対象**: 画像解析・CAD・測定アプリ
- **目的**: 構造化した点・線・寸法を返すAPI
- **ファイル**: `specifications/dimension-detection-api.yaml`

### ③ GeoJSON対応API
- **対象**: 地図、測位、地理空間情報
- **目的**: 世界標準フォーマット互換でAPI連携
- **ファイル**: `specifications/geojson-api.yaml`

### ④ GraphQL Gateway向け
- **対象**: GraphQL → REST ラップ構築
- **目的**: RESTエンドポイントの型をGraphQLに流用
- **ファイル**: `specifications/graphql-gateway-api.yaml`

### ⑤ AIモデルAPI (Inference)
- **対象**: LLM / VisionモデルのREST API
- **目的**: 推論入力・出力を明確に
- **ファイル**: `specifications/ai-model-api.yaml`

### ⑥ イベントWebhook
- **対象**: Slack, GitHub, Stripeのような外部通知
- **目的**: 双方向契約（送信側/受信側）を明示
- **ファイル**: `specifications/webhook-api.yaml`

### ⑦ ファイルアップロード／メディアAPI
- **対象**: 画像／音声／PDF解析など
- **目的**: multipart/form-data対応
- **ファイル**: `specifications/file-upload-api.yaml`

### ⑧ ユニット付きスキーマ（工学系）
- **対象**: 計測・解析・物理API
- **目的**: 値＋単位＋誤差を明確化
- **ファイル**: `specifications/measurement-api.yaml`

### ⑨ バージョニング／互換性
- **対象**: API進化を前提にした設計
- **目的**: 互換性確保＋新旧併存
- **ファイル**: `specifications/versioning-api.yaml`

### ⑩ OAuth2 + Bearer認証付きAPI
- **対象**: 公開APIや管理系
- **目的**: 認可フローを仕様に統合
- **ファイル**: `specifications/oauth2-api.yaml`

## 🛠️ 開発ツール

### Swagger UI
```bash
# ローカルでSwagger UIを起動
npx swagger-ui-serve specifications/dimension-detection-api.yaml
```

### Redoc
```bash
# Redocでドキュメント生成
npx redoc-cli build specifications/dimension-detection-api.yaml
```

### OpenAPI Generator
```bash
# 各種言語のクライアント生成
npx @openapitools/openapi-generator-cli generate \
  -i specifications/dimension-detection-api.yaml \
  -g python \
  -o examples/python/client
```

## 📖 ベストプラクティス

### スキーマ設計
- ✅ `components/schemas/` でモデル定義を分離再利用
- ✅ `additionalProperties` で動的キーに対応
- ✅ `enum` で地物種別を明確化
- ✅ 数値に意味を持たせるためにオブジェクト化

### API設計
- ✅ RESTfulなURL設計
- ✅ 適切なHTTPステータスコード
- ✅ エラーレスポンスの統一
- ✅ バージョニング戦略の明確化

### セキュリティ
- ✅ OAuth2認証スキームの明示
- ✅ スコープベースのアクセス制御
- ✅ APIキー管理の標準化

## 🔗 参考リンク

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger Editor](https://editor.swagger.io/)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Redoc](https://redoc.ly/)

## 📝 更新履歴

- 2024-10-XX: 初版作成
- 寸法線検出API仕様の詳細化
- 10カテゴリの事例集完成
