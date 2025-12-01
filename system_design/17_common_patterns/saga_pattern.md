# Saga Pattern パターン

## 1. 概要

Saga Patternは、分散システムで複数のサービスにまたがるトランザクションを管理するパターンです。各サービスがローカルトランザクションを実行し、失敗時には補償トランザクションを実行します。

## 2. Saga Patternの種類

### 2.1 Choreography（コレオグラフィー）

**説明**: 各サービスがイベントを発行し、他のサービスがイベントを監視します。

**特徴**:
- 中央制御がない
- 疎結合
- 実装が複雑

**使用例**:
- イベント駆動アーキテクチャ
- マイクロサービス

### 2.2 Orchestration（オーケストレーション）

**説明**: 中央のオーケストレーターが各サービスを呼び出します。

**特徴**:
- 中央制御がある
- 密結合
- 実装が簡単

**使用例**:
- ワークフロー管理
- ビジネスプロセス

## 3. Saga Patternの実装

### 3.1 Choreography実装例

```python
class OrderService:
    def __init__(self, db, message_queue):
        self.db = db
        self.message_queue = message_queue
    
    async def create_order(self, order_data: dict):
        # オーダーを作成
        order_id = await self.db.insert_order(order_data)
        
        # イベントを発行
        await self.message_queue.publish(
            topic="order-created",
            message={
                "order_id": order_id,
                "user_id": order_data["user_id"],
                "amount": order_data["amount"]
            }
        )
        
        return order_id
    
    async def compensate_order(self, order_id: int):
        # 補償トランザクション: オーダーをキャンセル
        await self.db.cancel_order(order_id)
        
        await self.message_queue.publish(
            topic="order-cancelled",
            message={"order_id": order_id}
        )

class PaymentService:
    def __init__(self, db, message_queue):
        self.db = db
        self.message_queue = message_queue
    
    async def handle_order_created(self, event: dict):
        try:
            # 支払いを処理
            payment_id = await self.db.process_payment(
                user_id=event["user_id"],
                amount=event["amount"]
            )
            
            await self.message_queue.publish(
                topic="payment-processed",
                message={
                    "order_id": event["order_id"],
                    "payment_id": payment_id
                }
            )
        except PaymentFailedError:
            # 補償トランザクションをトリガー
            await self.message_queue.publish(
                topic="payment-failed",
                message={"order_id": event["order_id"]}
            )
```

### 3.2 Orchestration実装例

```python
class OrderOrchestrator:
    def __init__(self, order_service, payment_service, inventory_service):
        self.order_service = order_service
        self.payment_service = payment_service
        self.inventory_service = inventory_service
    
    async def create_order(self, order_data: dict):
        steps = []
        
        try:
            # ステップ1: 在庫を確保
            inventory_reservation = await self.inventory_service.reserve(
                product_id=order_data["product_id"],
                quantity=order_data["quantity"]
            )
            steps.append(("inventory", inventory_reservation))
            
            # ステップ2: 支払いを処理
            payment = await self.payment_service.process_payment(
                user_id=order_data["user_id"],
                amount=order_data["amount"]
            )
            steps.append(("payment", payment))
            
            # ステップ3: オーダーを作成
            order_id = await self.order_service.create_order(order_data)
            steps.append(("order", order_id))
            
            return order_id
        
        except Exception as e:
            # 補償トランザクションを実行
            await self.compensate(steps)
            raise
    
    async def compensate(self, steps: list):
        """補償トランザクションを実行"""
        # 逆順で補償
        for step_type, step_data in reversed(steps):
            if step_type == "inventory":
                await self.inventory_service.release(step_data)
            elif step_type == "payment":
                await self.payment_service.refund(step_data)
            elif step_type == "order":
                await self.order_service.cancel_order(step_data)
```

## 4. ベストプラクティス

1. **補償トランザクション**: 適切な補償トランザクションを実装
2. **べき等性**: 補償トランザクションをべき等にする
3. **タイムアウト**: 適切なタイムアウトを設定
4. **モニタリング**: Sagaの実行を監視
5. **ログ記録**: Sagaの実行をログに記録

## 5. よくある落とし穴

1. **補償トランザクション**: 補償トランザクションの実装が不適切
2. **べき等性**: 補償トランザクションがべき等でない
3. **順序**: イベントの順序の問題

## 6. 関連パターン

- [Event Sourcing](event_sourcing.md) - イベントソーシング
- [CQRS](cqrs.md) - コマンドクエリ責任分離
- [Message Queues](message_queues.md) - メッセージキュー

---

**次のステップ**: [Bulkhead Pattern](bulkhead_pattern.md)でリソース分離パターンを学ぶ

