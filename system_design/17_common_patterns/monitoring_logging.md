# Monitoring & Logging パターン

## 1. 概要

モニタリングとログは、システムの状態を監視し、問題を特定・解決するための技術です。

## 2. モニタリングの種類

### 2.1 メトリクスモニタリング

**説明**: システムのメトリクスを収集・監視します。

**メトリクスの種類**:
- CPU使用率
- メモリ使用率
- リクエストレート
- エラーレート
- レイテンシ

**使用例**:
- システムの健全性監視
- パフォーマンス監視

### 2.2 ログモニタリング

**説明**: アプリケーションのログを収集・分析します。

**ログの種類**:
- アプリケーションログ
- アクセスログ
- エラーログ
- 監査ログ

**使用例**:
- 問題の特定
- デバッグ
- 監査

### 2.3 トレーシング

**説明**: リクエストのトレースを収集・分析します。

**特徴**:
- 分散システムでのトレーシング
- パフォーマンス分析

**使用例**:
- マイクロサービス
- 分散システム

## 3. モニタリングツール

### 3.1 Prometheus

**説明**: メトリクス収集・監視システムです。

**特徴**:
- 時系列データベース
- クエリ言語（PromQL）
- アラート機能

**使用例**:
- メトリクス監視
- アラート

### 3.2 Grafana

**説明**: メトリクスの可視化ツールです。

**特徴**:
- ダッシュボード
- 複数のデータソース
- アラート機能

**使用例**:
- メトリクスの可視化
- ダッシュボード

### 3.3 ELK Stack

**説明**: Elasticsearch、Logstash、Kibanaのスタックです。

**特徴**:
- ログの収集・分析
- 可視化
- 検索機能

**使用例**:
- ログ分析
- ログ検索

### 3.4 Jaeger

**説明**: 分散トレーシングシステムです。

**特徴**:
- 分散トレーシング
- パフォーマンス分析

**使用例**:
- マイクロサービス
- 分散システム

## 4. ログの構造化

### 4.1 構造化ログ

**説明**: JSON形式などの構造化されたログを使用します。

**メリット**:
- 解析が容易
- 検索が容易
- 自動化が可能

**使用例**:
- 本番環境
- 大規模システム

### 4.2 ログレベル

**説明**: ログの重要度に応じてレベルを設定します。

**レベル**:
- DEBUG: デバッグ情報
- INFO: 一般的な情報
- WARN: 警告
- ERROR: エラー
- FATAL: 致命的なエラー

## 5. アラート

### 5.1 アラートの種類

**説明**: システムの状態に応じてアラートを送信します。

**アラートの種類**:
- メトリクスベース
- ログベース
- ヘルスチェックベース

### 5.2 アラートの設定

**説明**: 適切な閾値を設定してアラートを送信します。

**考慮事項**:
- 閾値の設定
- アラートの頻度
- 通知先の設定

## 6. 実装例

### 6.1 ログ記録

```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_request(user_id: int, endpoint: str, status_code: int, latency_ms: int):
    """リクエストをログに記録"""
    log_data = {
        "user_id": user_id,
        "endpoint": endpoint,
        "status_code": status_code,
        "latency_ms": latency_ms
    }
    logging.info(json.dumps(log_data))
```

### 6.2 メトリクス収集

```python
from prometheus_client import Counter, Histogram

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')

def handle_request():
    """リクエストを処理してメトリクスを記録"""
    with request_latency.time():
        # リクエスト処理
        request_count.inc()
```

## 7. ベストプラクティス

1. **構造化ログ**: 構造化されたログを使用
2. **ログレベル**: 適切なログレベルを使用
3. **メトリクスの選択**: 重要なメトリクスを選択
4. **アラートの設定**: 適切なアラートを設定
5. **ダッシュボード**: 重要なメトリクスのダッシュボードを作成

## 8. よくある落とし穴

1. **ログの過剰**: 過剰なログがパフォーマンスに影響
2. **アラートの過剰**: 過剰なアラートが無視される
3. **メトリクスの選択**: 重要なメトリクスを見逃す

## 9. 関連パターン

- [Load Balancing](load_balancing.md) - 負荷分散
- [Caching Strategies](caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Scaling Challenges](../18_case_studies/scaling_challenges.md)でスケーリングの課題を学ぶ

