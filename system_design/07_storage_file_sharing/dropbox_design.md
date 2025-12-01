# Dropbox システム設計

## 1. システム概要

### 目的と主要機能

Dropboxは、ユーザーがファイルをアップロード、保存、共有するクラウドストレージサービスです。

**主要機能**:
- ファイルのアップロードとダウンロード
- ファイルの同期（複数デバイス間）
- ファイルの共有
- バージョン管理
- オフラインアクセス

### ユーザースケール

- **月間アクティブユーザー（MAU）**: 約7億人
- **日間アクティブユーザー（DAU）**: 約3億人
- **1日のファイルアップロード**: 約10億ファイル
- **総ストレージ**: 約500 PB

## 2. 機能要件

### コア機能

1. **ファイルアップロード**
   - 大容量ファイルのアップロード
   - チャンクアップロード

2. **ファイル同期**
   - 複数デバイス間での同期
   - リアルタイム同期

3. **ファイル共有**
   - リンク共有
   - フォルダ共有

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
Client → Load Balancer → API Gateway → Application Servers
  ↓
File Upload Service → Object Storage (S3)
File Sync Service → Database → Message Queue
File Share Service → Database
```

## 4. データモデル設計

### Files テーブル

```sql
CREATE TABLE files (
    file_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_path VARCHAR(2000) NOT NULL,
    file_size BIGINT NOT NULL,
    file_hash VARCHAR(64),
    storage_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_id_path (user_id, file_path),
    INDEX idx_file_hash (file_hash)
) ENGINE=InnoDB;
```

## 5. API設計

### ファイルアップロード

```
POST /api/v1/files/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

Request Body:
{
  "file": <file>,
  "path": "/Documents/file.pdf"
}

Response (201 Created):
{
  "file_id": 1234567890,
  "file_path": "/Documents/file.pdf",
  "file_size": 1048576
}
```

## 6. スケーラビリティ設計

### ファイルストレージ

- **Object Storage**: S3/GCSでファイルを保存
- **重複排除**: 同じファイルは1回だけ保存
- **チャンクアップロード**: 大容量ファイルをチャンクに分割

## 7. レイテンシ最適化

### ファイル同期の最適化

- **差分同期**: 変更された部分のみ同期
- **キャッシング**: 最近アクセスしたファイルをキャッシュ

## 8. コスト最適化

### インフラコストの見積もり

- **ストレージ**: 500 PB × $0.023/GB/月 = 約 **$11,500,000/月**
- **サーバー**: 約 **$2,000,000/月**
- **データ転送**: 約 **$1,000,000/月**
- **合計**: 約 **$14,500,000/月**

## 9. 可用性・信頼性

### 障害対策

- **マルチリージョン**: 複数のリージョンにファイルをレプリケート
- **バックアップ**: 定期的なバックアップ

## 10. セキュリティ

### セキュリティ対策

- **暗号化**: 転送中と保存時の暗号化
- **アクセス制御**: ファイルのアクセス権限管理

## 11. UX最適化

### パフォーマンス指標

- **ファイルアップロード**: バックグラウンド処理
- **ファイル同期**: < 5秒の遅延
- **ファイルダウンロード**: CDN経由で高速化

## 12. 実装例

### ファイル同期サービス（疑似コード）

```python
class FileSyncService:
    def __init__(self, db, storage, message_queue):
        self.db = db
        self.storage = storage
        self.message_queue = message_queue
    
    async def sync_file(self, user_id: int, device_id: str, file_path: str):
        # ファイルのメタデータを取得
        file_meta = await self.db.get_file(user_id, file_path)
        
        # デバイスの最終同期時刻を確認
        last_sync = await self.db.get_last_sync(user_id, device_id, file_path)
        
        if file_meta["updated_at"] > last_sync:
            # ファイルを同期
            file_content = await self.storage.download(file_meta["storage_url"])
            
            # 同期イベントを送信
            await self.message_queue.publish(
                topic="file-sync",
                message={
                    "user_id": user_id,
                    "device_id": device_id,
                    "file_path": file_path,
                    "file_content": file_content
                }
            )
```

## 13. 数値例と計算

### トラフィック見積もり

- **1日のファイルアップロード**: 10億ファイル
- **平均ファイルサイズ**: 5 MB
- **1日のアップロードサイズ**: 10億 × 5 MB = 5 PB

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **重複排除**: 同じファイルは1回だけ保存
2. **チャンクアップロード**: 大容量ファイルをチャンクに分割
3. **差分同期**: 変更された部分のみ同期

## 15. 関連システム

### 類似システムへのリンク

- [Google Drive](google_drive_design.md) - クラウドストレージサービス
- [OneDrive](onedrive_design.md) - Microsoftのクラウドストレージ

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散
- [Caching Strategies](../17_common_patterns/caching_strategies.md) - キャッシング戦略

---

**次のステップ**: [Spotify](spotify_design.md)で音楽ストリーミングの設計を学ぶ

