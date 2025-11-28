# Dijkstra Shortest Path (Graph) - ロジック解説

## 問題概要

重み付き有向グラフと開始ノードが与えられたとき、開始ノードから全てのノードへの最短経路の距離を返す。

**制約**:
- `1 <= n <= 100`
- 全ての重みは非負

**例**:
```
Input: n = 4, edges = [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]], start = 0
Output: [0,1,3,4]
```

## ロジックの核心

### なぜDijkstraが有効か？

**全探索（O(2^n)）**:
- 全ての可能な経路を試す
- 時間計算量: O(2^n) - 非効率

**Dijkstraを使う理由**:
- **貪欲法**: 最短距離が確定したノードから順に処理
- **優先度付きキュー**: 最短距離のノードを効率的に取得
- **時間計算量**: O((V + E) log V) - 効率的

### 思考プロセス

1. **距離の初期化**: 開始ノードの距離を0、他を無限大に設定
2. **優先度付きキュー**: (距離, ノード)のペアをキューに追加
3. **最短距離の確定**: キューから最短距離のノードを取得
4. **隣接ノードの更新**: 隣接ノードの距離を更新

### アルゴリズムのステップ

```
function dijkstra(n, edges, start):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    
    dist = [float('inf')] * n
    dist[start] = 0
    
    heap = [(0, start)]
    visited = set()
    
    while heap:
        d, node = heapq.heappop(heap)
        
        if node in visited:
            continue
        
        visited.add(node)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_dist = d + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))
    
    return dist
```

## 現実世界での応用

### 1. 地図アプリケーション
- **シナリオ**: Google Mapsで、最短経路を計算
- **実装**: Dijkstraアルゴリズムで最短経路を計算
- **メリット**: 効率的なルート検索

### 2. ネットワークルーティング
- **シナリオ**: ルーターが、パケットの最適な経路を選択
- **実装**: Dijkstraアルゴリズムで最短経路を計算
- **メリット**: 効率的なパケットルーティング

### 3. ゲーム開発
- **シナリオ**: ゲームのAIで、最短経路を計算
- **実装**: A*アルゴリズム（Dijkstraの拡張）でパスファインディング
- **メリット**: 効率的なAIの移動

### 4. 物流システム
- **シナリオ**: 配送ルートの最適化
- **実装**: Dijkstraアルゴリズムで最適なルートを計算
- **メリット**: コストの削減

### 5. ソーシャルネットワーク
- **シナリオ**: ソーシャルネットワークで、最短の接続経路を計算
- **実装**: Dijkstraアルゴリズムで最短経路を計算
- **メリット**: 効率的なネットワーク分析

### 6. 電力網の管理
- **シナリオ**: 電力網で、電力の最適な経路を計算
- **実装**: Dijkstraアルゴリズムで最短経路を計算
- **メリット**: 効率的な電力管理

## 注意点と落とし穴

### 1. 非負の重みの前提
- **問題**: Dijkstraは非負の重みのみを扱える
- **解決策**: 負の重みがある場合、Bellman-Fordを使用
- **実装**: 重みが負でないことを確認
- **注意**: 負の重みがある場合、Dijkstraは正しく動作しない

### 2. 優先度付きキュー
- **問題**: 最短距離のノードを効率的に取得する必要がある
- **解決策**: `heapq`モジュールを使用
- **実装**: `heapq.heappush(heap, (distance, node))`
- **注意**: 距離を最初の要素にすることで、最小値が先頭に来る

### 3. 訪問済みノードの管理
- **問題**: 同じノードを複数回処理しないようにする必要がある
- **解決策**: `visited`セットで管理
- **実装**: `if node in visited: continue`でスキップ
- **注意**: 訪問済みチェックを忘れると、無限ループが発生する可能性

### 4. 距離の更新
- **問題**: より短い経路が見つかった場合、距離を更新する必要がある
- **解決策**: `if new_dist < dist[neighbor]:`で更新
- **実装**: 距離を更新し、キューに追加
- **注意**: 更新を忘れると、最短経路を見逃す

### 5. 時間計算量の理解
- **平均**: O((V + E) log V) - 優先度付きキューの操作
- **最悪**: O((V + E) log V) - 常に同じ時間計算量
- **空間**: O(V) - 距離配列、キュー、訪問済みセット
- **注意**: 優先度付きキューの操作が支配的

## 関連問題

- [Bellman-Ford](../23_advanced_graph/bellman_ford_logic.md) - 負重みの最短経路
- [Topological Sort](./topological_sort_logic.md) - 依存関係の解決
- [Number of Islands](./number_of_islands_logic.md) - グラフ探索

---

**次のステップ**: [Course Schedule](../23_advanced_graph/course_schedule_logic.md)でトポロジカルソートの応用を学ぶ

