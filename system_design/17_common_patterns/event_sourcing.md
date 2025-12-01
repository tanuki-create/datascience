# Event Sourcing パターン

## 1. 概要

Event Sourcing（イベントソーシング）は、状態の変更をイベントとして保存し、イベントを再生することで状態を再構築するパターンです。

## 2. Event Sourcingの概念

### 2.1 イベントストア

**説明**: イベントを永続的に保存するストレージです。

**特徴**:
- イベントの追加のみ（不変）
- 時系列で保存
- イベントの再生が可能

### 2.2 イベント再生

**説明**: イベントを再生して状態を再構築します。

**方法**:
- 全イベントを再生
- スナップショットから再生

### 2.3 スナップショット

**説明**: 状態のスナップショットを保存します。

**目的**:
- イベント再生の高速化
- ストレージの最適化

## 3. Event Sourcingのメリット

### 3.1 監査ログ

**説明**: すべての変更がイベントとして記録されます。

**メリット**:
- 完全な監査ログ
- 変更履歴の追跡
- コンプライアンス対応

### 3.2 タイムトラベル

**説明**: 過去の任意の時点の状態を再構築できます。

**メリット**:
- デバッグの容易さ
- 過去の状態の分析
- ロールバック

### 3.3 イベントリプレイ

**説明**: イベントを再生して新しいビューを生成できます。

**メリット**:
- 新しいビューの追加が容易
- データの再処理
- 分析の柔軟性

## 4. Event Sourcingの実装

### 4.1 イベントストア

```python
from datetime import datetime
from typing import List, Optional
import json

class EventStore:
    def __init__(self, db):
        self.db = db
    
    async def append_event(self, aggregate_id: str, event_type: str, 
                          event_data: dict, version: int):
        """イベントを追加"""
        event = {
            "aggregate_id": aggregate_id,
            "event_type": event_type,
            "event_data": json.dumps(event_data),
            "version": version,
            "timestamp": datetime.now()
        }
        await self.db.insert_event(event)
    
    async def get_events(self, aggregate_id: str, 
                        from_version: int = 0) -> List[dict]:
        """イベントを取得"""
        events = await self.db.get_events(
            aggregate_id=aggregate_id,
            from_version=from_version
        )
        return events
    
    async def replay_events(self, aggregate_id: str) -> dict:
        """イベントを再生して状態を再構築"""
        events = await self.get_events(aggregate_id)
        state = {}
        
        for event in events:
            state = self.apply_event(state, event)
        
        return state
    
    def apply_event(self, state: dict, event: dict) -> dict:
        """イベントを適用して状態を更新"""
        event_type = event["event_type"]
        event_data = json.loads(event["event_data"])
        
        if event_type == "UserCreated":
            state["user_id"] = event_data["user_id"]
            state["username"] = event_data["username"]
        elif event_type == "UserUpdated":
            state.update(event_data)
        
        return state
```

### 4.2 スナップショット

```python
class SnapshotStore:
    def __init__(self, db):
        self.db = db
    
    async def save_snapshot(self, aggregate_id: str, state: dict, 
                           version: int):
        """スナップショットを保存"""
        snapshot = {
            "aggregate_id": aggregate_id,
            "state": json.dumps(state),
            "version": version,
            "timestamp": datetime.now()
        }
        await self.db.insert_snapshot(snapshot)
    
    async def get_snapshot(self, aggregate_id: str) -> Optional[dict]:
        """スナップショットを取得"""
        snapshot = await self.db.get_latest_snapshot(aggregate_id)
        if snapshot:
            return {
                "state": json.loads(snapshot["state"]),
                "version": snapshot["version"]
            }
        return None
    
    async def replay_from_snapshot(self, aggregate_id: str) -> dict:
        """スナップショットからイベントを再生"""
        snapshot = await self.get_snapshot(aggregate_id)
        
        if snapshot:
            state = snapshot["state"]
            from_version = snapshot["version"] + 1
        else:
            state = {}
            from_version = 0
        
        # スナップショット以降のイベントを再生
        events = await self.event_store.get_events(
            aggregate_id=aggregate_id,
            from_version=from_version
        )
        
        for event in events:
            state = self.apply_event(state, event)
        
        return state
```

## 5. ベストプラクティス

1. **イベントの設計**: イベントを適切に設計
2. **スナップショット**: 適切なタイミングでスナップショットを保存
3. **イベントのバージョニング**: イベントのバージョニングを実装
4. **イベントのスキーマ**: イベントのスキーマを定義
5. **パフォーマンス**: イベント再生のパフォーマンスを最適化

## 6. よくある落とし穴

1. **イベントの設計**: イベントの設計が不適切
2. **パフォーマンス**: 大量のイベント再生が遅い
3. **スキーマの変更**: イベントスキーマの変更が困難

## 7. 関連パターン

- [CQRS](cqrs.md) - コマンドクエリ責任分離
- [Message Queues](message_queues.md) - メッセージキュー

---

**次のステップ**: [CQRS](cqrs.md)でコマンドクエリ責任分離パターンを学ぶ

