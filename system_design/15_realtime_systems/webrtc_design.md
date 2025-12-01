# WebRTC システム設計

## 1. システム概要

### 目的と主要機能

WebRTC（Web Real-Time Communication）は、ブラウザ間でリアルタイム通信を可能にするオープンスタンダードプロトコルです。P2P通信とメディアサーバーを組み合わせたシステムを設計します。

**主要機能**:
- P2Pビデオ・音声通信
- データチャネル
- 画面共有
- ファイル転送
- SFU（Selective Forwarding Unit）
- TURN/STUNサーバー

### ユーザースケール

- **1日の接続数**: 約1億接続
- **1秒あたりの同時接続数**: 約100万接続/秒（ピーク時）
- **1日のデータ転送量**: 約10 PB

### 主要なユースケース

1. **P2P通信**: ブラウザ間での直接通信
2. **マルチパーティ通信**: SFUを介した複数参加者間の通信
3. **データ転送**: データチャネルを介したファイル転送
4. **画面共有**: 画面の共有とリモート制御

## 2. 機能要件

### コア機能

1. **シグナリング**
   - オファー/アンサーの交換
   - ICE候補の交換
   - セッション管理

2. **メディア通信**
   - ビデオストリーミング
   - 音声ストリーミング
   - アダプティブビットレート

3. **NAT越え**
   - STUNサーバー
   - TURNサーバー

4. **SFU**
   - メディアストリームの選択的転送
   - スケーラブルなマルチパーティ通信

### 非機能要件

- **可用性**: 99.9%以上
- **パフォーマンス**:
  - ビデオレイテンシ: < 150ms
  - 音声レイテンシ: < 100ms
- **スケーラビリティ**: 水平スケーリング可能

## 3. システムアーキテクチャ

### 高レベルアーキテクチャ

```
┌─────────────┐         ┌─────────────┐
│   Client 1  │◄───────►│   Client 2  │ (P2P)
└──────┬──────┘         └──────┬──────┘
       │                        │
       │                        │
┌──────▼────────────────────────▼──────┐
│         Signaling Server               │
│         (WebSocket/HTTP)              │
└──────┬────────────────────────────────┘
       │
       │
┌──────▼────────────────────────────────┐
│         STUN/TURN Servers              │
│         (NAT Traversal)                │
└────────────────────────────────────────┘

マルチパーティ通信の場合:
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼────────────────────────────────┐
│         SFU (Selective Forwarding Unit)│
│         (Media Server)                 │
└──────┬─────────────────────────────────┘
       │
       ├──────────┬──────────┬──────────┐
       │          │          │          │
┌──────▼──┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│ Client 1│  │Client 2│  │Client 3│  │Client 4│
└─────────┘  └────────┘  └────────┘  └────────┘
```

### コンポーネントの説明

1. **Signaling Server**: WebSocket/HTTPでシグナリングメッセージを交換
2. **STUN Server**: NAT越えのためのパブリックIP/ポートの検出
3. **TURN Server**: NAT越えができない場合のリレーサーバー
4. **SFU**: メディアストリームの選択的転送

### データフロー

#### P2P接続確立のフロー

```
1. Client 1 → Signaling Server: Offer送信
2. Signaling Server → Client 2: Offer転送
3. Client 2 → Signaling Server: Answer送信
4. Signaling Server → Client 1: Answer転送
5. Client 1/2 → STUN Server: ICE候補の取得
6. Client 1/2: 直接P2P接続確立
```

## 4. データモデル設計

### 主要なエンティティ

#### Sessions テーブル

```sql
CREATE TABLE sessions (
    session_id BIGINT PRIMARY KEY,
    user_id_1 BIGINT NOT NULL,
    user_id_2 BIGINT NOT NULL,
    session_type ENUM('p2p', 'sfu') DEFAULT 'p2p',
    status ENUM('connecting', 'connected', 'disconnected') DEFAULT 'connecting',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id_1) REFERENCES users(user_id),
    FOREIGN KEY (user_id_2) REFERENCES users(user_id),
    INDEX idx_user_id_1 (user_id_1),
    INDEX idx_user_id_2 (user_id_2)
) ENGINE=InnoDB;
```

## 5. API設計

### 主要なAPIエンドポイント

#### オファー送信

```
POST /api/v1/signaling/offer
WebSocket Connection

Message:
{
  "type": "offer",
  "sdp": "...",
  "session_id": "session_1234567890"
}
```

## 6. スケーラビリティ設計

### 水平スケーリング戦略

#### Signaling Server

- **ステートレス設計**: セッション情報をRedisに保存
- **WebSocket接続**: 各サーバーがWebSocket接続を管理
- **ロードバランサー**: セッションIDベースのルーティング

#### SFU

- **動的スケーリング**: 需要に応じてSFUを起動・停止
- **地理的分散**: 複数のリージョンにSFUを配置

## 7. レイテンシ最適化

### ボトルネックの特定

1. **NAT越え**: STUN/TURNサーバーへのアクセス
2. **メディアストリーミング**: ビデオ・音声のストリーミング
3. **シグナリング**: シグナリングメッセージの交換

### NAT越え最適化

1. **STUN最適化**: 複数のSTUNサーバーを配置
2. **TURN最適化**: 地理的に分散したTURNサーバー
3. **ICE最適化**: ICE候補の優先順位付け

## 8. コスト最適化

### インフラコストの見積もり

#### サーバーコスト（AWS）

**Signaling Server**:
- EC2インスタンス: m5.xlarge (4 vCPU, 16 GB RAM)
- インスタンス数: 200台
- コスト: $0.192/時間 × 200台 × 730時間 = **$28,032/月**

**TURN Server**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 500台
- コスト: $0.34/時間 × 500台 × 730時間 = **$124,100/月**

**SFU**:
- EC2インスタンス: c5.2xlarge (8 vCPU, 16 GB RAM)
- インスタンス数: 1,000台
- コスト: $0.34/時間 × 1,000台 × 730時間 = **$248,200/月**

**ネットワーク**:
- データ転送: 10 PB/月
- コスト: $0.09/GB × 10,000,000 GB = **$900,000/月**

**合計**: 約 **$1,300,332/月**（約15,603,984ドル/年）

## 9. 可用性・信頼性

### 障害対策

1. **冗長化**: 
   - 複数のSignaling Serverにデプロイ
   - 複数のTURN/SFUサーバーにデプロイ

2. **ヘルスチェック**:
   - Signaling Serverのヘルスチェック
   - TURN/SFUサーバーのヘルスチェック

## 10. セキュリティ

### 認証・認可

1. **認証**: OAuth 2.0 / JWT
2. **認可**: セッションベースのアクセス制御

### データ暗号化

1. **転送中の暗号化**: DTLS（Datagram Transport Layer Security）
2. **メディア暗号化**: SRTP（Secure Real-time Transport Protocol）

## 11. UX最適化

### パフォーマンス指標

- **ビデオレイテンシ**: < 150ms
- **音声レイテンシ**: < 100ms
- **接続確立時間**: < 3秒

## 12. 実装例

### Signaling Server（疑似コード）

```python
class SignalingServer:
    def __init__(self, redis, stun_servers, turn_servers):
        self.redis = redis
        self.stun_servers = stun_servers
        self.turn_servers = turn_servers
    
    async def handle_offer(self, session_id: str, offer: dict, user_id: int):
        # オファーを保存
        await self.redis.set(
            f"session:{session_id}:offer",
            json.dumps(offer),
            ex=300
        )
        
        # 相手にオファーを転送
        await self.send_to_peer(session_id, {
            "type": "offer",
            "sdp": offer["sdp"]
        })
        
        # STUN/TURNサーバー情報を返す
        return {
            "stun_servers": self.stun_servers,
            "turn_servers": self.turn_servers
        }
```

## 13. 数値例と計算

### トラフィック見積もり

#### 読み取りトラフィック

- **1日の接続数**: 1億接続
- **1時間あたり**: 1億 / 24 = 約416万接続
- **1秒あたり**: 416万 / 3600 = 約1,156接続/秒
- **ピーク時（3倍）**: 約3,468接続/秒

## 14. ベストプラクティス

### 設計のベストプラクティス

1. **P2P優先**: 可能な限りP2P通信を使用
2. **SFU活用**: マルチパーティ通信ではSFUを使用
3. **NAT越え**: STUN/TURNサーバーでNAT越えを実現
4. **低レイテンシ**: ビデオ・音声の低レイテンシ通信
5. **セキュリティ**: DTLS/SRTPで暗号化

## 15. 関連システム

### 類似システムへのリンク

- [Zoom](zoom_design.md) - ビデオ会議プラットフォーム
- [Realtime Gaming](realtime_gaming_design.md) - リアルタイムゲーム

### 共通パターンへのリンク

- [Load Balancing](../17_common_patterns/load_balancing.md) - 負荷分散

---

**次のステップ**: [Realtime Gaming](realtime_gaming_design.md)でリアルタイムゲームの設計を学ぶ

