# Topological Sort (Graph) - ロジック解説

## 問題概要

有向非巡回グラフ（DAG）のノードが与えられたとき、トポロジカルソート（依存関係を満たす順序）を返す。

**制約**:
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`

**例**:
```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,1,2,3] or [0,2,1,3]
```

## ロジックの核心

### なぜBFS/DFSが有効か？

**全探索（非効率）**:
- 全ての可能な順序を試す
- 時間計算量: O(n!) - 非効率

**BFS/DFSを使う理由**:
- **依存関係の追跡**: 各ノードの依存関係を追跡
- **時間計算量**: O(V + E) - 線形時間
- **空間計算量**: O(V) - 訪問状態の管理

### 思考プロセス

1. **グラフの構築**: 依存関係からグラフを構築
2. **入次数の計算**: 各ノードの入次数（依存数）を計算
3. **BFS/DFS**: 入次数が0のノードから開始し、順次処理

### アルゴリズムのステップ

```
function topologicalSort(numCourses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = deque()
    for i in range(numCourses):
        if indegree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == numCourses else []
```

## 現実世界での応用

### 1. コンパイラの依存関係解決
- **シナリオ**: プログラミング言語のコンパイラで、モジュールのコンパイル順序を決定
- **実装**: トポロジカルソートで依存関係を解決
- **メリット**: 効率的なコンパイル

### 2. パッケージマネージャー
- **シナリオ**: npm、pipなどのパッケージマネージャーで、依存関係を解決
- **実装**: トポロジカルソートで依存関係を解決
- **メリット**: 効率的なパッケージインストール

### 3. タスクスケジューリング
- **シナリオ**: タスクの実行順序を決定
- **実装**: トポロジカルソートでタスクの順序を決定
- **メリット**: 効率的なタスク実行

### 4. プロジェクト管理
- **シナリオ**: プロジェクトのタスクの実行順序を決定
- **実装**: トポロジカルソートでタスクの順序を決定
- **メリット**: 効率的なプロジェクト管理

### 5. ビルドシステム
- **シナリオ**: Make、CMakeなどのビルドシステムで、ターゲットのビルド順序を決定
- **実装**: トポロジカルソートでビルド順序を決定
- **メリット**: 効率的なビルド

### 6. データベースのクエリ最適化
- **シナリオ**: データベースで、テーブルの結合順序を決定
- **実装**: トポロジカルソートで結合順序を決定
- **メリット**: クエリの実行時間を短縮

## 注意点と落とし穴

### 1. サイクルの検出
- **問題**: サイクルがある場合、トポロジカルソートは不可能
- **解決策**: 結果のサイズがノード数と等しいか確認
- **実装**: `return result if len(result) == numCourses else []`
- **注意**: サイクルがある場合、空のリストを返す

### 2. 入次数の管理
- **問題**: 各ノードの入次数を正確に管理する必要がある
- **解決策**: グラフ構築時に入次数を計算
- **実装**: `indegree[course] += 1`で管理
- **注意**: 入次数の計算を忘れると、正しく動作しない

### 3. BFS vs DFS
- **問題**: BFSとDFSのどちらを使うべきか？
- **解決策**: 
  - BFS（Kahn's Algorithm）: 実装が簡単、キューを使用
  - DFS: 再帰的実装、スタックを使用
- **選択**: 通常はBFSが推奨される

### 4. 時間計算量の理解
- **平均**: O(V + E) - 各ノードと辺を1回ずつ処理
- **最悪**: O(V + E) - 常に線形時間
- **空間**: O(V) - グラフ、入次数、キュー
- **メリット**: 効率的なアルゴリズム

### 5. 複数の解
- **問題**: トポロジカルソートは複数の解を持つ可能性がある
- **解決策**: 問題の要件に応じて、特定の順序を選択
- **実装**: 通常は任意の有効な順序を返す
- **注意**: 問題の要件を確認する必要がある

## 関連問題

- [Course Schedule](../23_advanced_graph/course_schedule_logic.md) - トポロジカルソートの応用
- [Number of Islands](./number_of_islands_logic.md) - グラフ探索
- [Dijkstra Shortest Path](../23_advanced_graph/dijkstra_shortest_path_logic.md) - 最短経路

---

**次のステップ**: [Dijkstra Shortest Path](../23_advanced_graph/dijkstra_shortest_path_logic.md)で最短経路を学ぶ

