# Combination Sum - ロジック解説

## 問題概要

重複する要素を含む配列`candidates`と整数`target`が与えられたとき、合計が`target`になる全てのユニークな組み合わせを返す。同じ数字を何度でも使用できる。

**制約**:
- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- `1 <= target <= 500`

**例**:
```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
説明: 
- 2+2+3 = 7
- 7 = 7
```

## ロジックの核心

### なぜバックトラッキングが有効か？

**全探索（非効率）**:
- 全ての可能な組み合わせを試す
- 時間計算量: O(2^n) - 各要素を選ぶ/選ばないの2択

**バックトラッキングを使う理由**:
- **制約を満たすものだけを生成**: 合計がtargetを超える組み合わせを生成しない
- **重複の回避**: ソートとインデックスの管理で重複を避ける
- **早期終了**: 合計がtargetを超えた場合は即座に戻る
- **時間計算量**: O(2^n)だが、早期終了により大幅に短縮

### 思考プロセス

1. **ソート**: 配列をソートして、重複を避けやすくする
2. **選択**: 現在のインデックス以降の要素を選択できる
3. **合計の管理**: 現在の合計を追跡し、targetと比較
4. **バックトラック**: 
   - 合計がtargetに達したら結果に追加
   - 合計がtargetを超えたら戻る
   - 次の要素を試す

### アルゴリズムのステップ

```
function combinationSum(candidates, target):
    result = []
    candidates.sort()  // ソートして重複を避ける
    
    function backtrack(combination, start, remaining):
        // ベースケース: 合計がtargetに達した
        if remaining == 0:
            result.append(combination[:])
            return
        
        // 現在のインデックス以降の要素を試す
        for i in range(start, len(candidates)):
            // 早期終了: 残りが負になったら終了
            if remaining < candidates[i]:
                break
            
            // 要素を追加
            combination.append(candidates[i])
            // 同じ要素を再度使用できるため、iから再帰
            backtrack(combination, i, remaining - candidates[i])
            // バックトラック: 要素を削除
            combination.pop()
    
    backtrack([], 0, target)
    return result
```

## 具体例でのトレース

### 例: `candidates = [2,3,6,7], target = 7`

```
ソート後: [2,3,6,7]

初期状態: combination = [], start = 0, remaining = 7

start=0: 2を試す
  combination = [2], remaining = 5
  start=0: 2を再度試す
    combination = [2,2], remaining = 3
    start=0: 2を再度試す
      combination = [2,2,2], remaining = 1
      start=0: 2を試す → remaining < 2 → break
      start=1: 3を試す → remaining < 3 → break
      ... 全て無効
    start=1: 3を試す
      combination = [2,2,3], remaining = 0 ✓ 結果に追加
    start=2: 6を試す → remaining < 6 → break
    start=3: 7を試す → remaining < 7 → break
  start=1: 3を試す
    combination = [2,3], remaining = 2
    start=1: 3を試す → remaining < 3 → break
    start=2: 6を試す → remaining < 6 → break
    start=3: 7を試す → remaining < 7 → break
  start=2: 6を試す → remaining < 6 → break
  start=3: 7を試す → remaining < 7 → break

start=1: 3を試す
  combination = [3], remaining = 4
  start=1: 3を再度試す
    combination = [3,3], remaining = 1
    start=1: 3を試す → remaining < 3 → break
    ... 全て無効
  start=2: 6を試す → remaining < 6 → break
  start=3: 7を試す → remaining < 7 → break

start=2: 6を試す → remaining < 6 → break

start=3: 7を試す
  combination = [7], remaining = 0 ✓ 結果に追加

結果: [[2,2,3],[7]]
```

### 可視化

```
探索木:

                    []
                   / | | \
                 2  3 6 7
                /  | | \
              2    3 6 7
             /  |  |
           2    3  6
          /
        2 (無効)
       /
     3 ✓ [2,2,3]
```

## 現実世界での応用

### 1. 金融取引の最適化
- **シナリオ**: 複数の金融商品の組み合わせで、目標金額を達成
- **実装**: 各商品を候補として、目標金額に達する組み合わせを探索
- **例**: 投資ポートフォリオの最適化
- **メリット**: 最適な投資戦略を見つける

### 2. 在庫管理
- **シナリオ**: 複数の商品の組み合わせで、目標数量を達成
- **実装**: 各商品を候補として、目標数量に達する組み合わせを探索
- **例**: 在庫の補充計画
- **メリット**: 効率的な在庫管理

### 3. リソース配分
- **シナリオ**: 複数のリソースの組み合わせで、目標値を達成
- **実装**: 各リソースを候補として、目標値に達する組み合わせを探索
- **例**: クラウドリソースの割り当て
- **メリット**: リソースの効率的な利用

### 4. パッケージング問題
- **シナリオ**: 複数のサイズのパッケージで、目標容量を達成
- **実装**: 各サイズを候補として、目標容量に達する組み合わせを探索
- **例**: 配送の最適化
- **メリット**: コストの削減

### 5. レシピの最適化
- **シナリオ**: 複数の食材の組み合わせで、目標栄養価を達成
- **実装**: 各食材を候補として、目標栄養価に達する組み合わせを探索
- **例**: 栄養バランスの取れた食事計画
- **メリット**: 健康的な食事の設計

### 6. プロジェクト管理
- **シナリオ**: 複数のタスクの組み合わせで、目標時間を達成
- **実装**: 各タスクを候補として、目標時間に達する組み合わせを探索
- **例**: プロジェクトのスケジュール最適化
- **メリット**: 効率的なプロジェクト管理

## 注意点と落とし穴

### 1. 重複の回避
- **問題**: 同じ組み合わせが複数回生成される可能性がある
- **解決策**: ソートして、現在のインデックス以降の要素のみを選択
- **実装**: `for i in range(start, len(candidates)):`で重複を避ける
- **注意**: インデックスを管理しないと、[2,3]と[3,2]が両方生成される

### 2. リストのコピー
- **問題**: 結果に追加する際、リストの参照を追加すると、後で変更される
- **解決策**: リストのコピーを作成して追加
- **実装**: `result.append(combination[:])`でコピーを作成
- **注意**: `result.append(combination)`だと、後でcombinationが変更されると結果も変わる

### 3. 早期終了の重要性
- **問題**: 合計がtargetを超えた場合、それ以降の要素も超えるため無駄
- **解決策**: ソート後、合計がtargetを超えたら即座にbreak
- **実装**: `if remaining < candidates[i]: break`
- **メリット**: 探索空間を大幅に削減

### 4. 時間計算量の理解
- **平均**: O(2^n) - 各要素を選ぶ/選ばないの2択
- **最悪**: O(2^n) - 常に指数時間
- **空間**: O(target) - 再帰の深さが最大target（最小要素が1の場合）
- **注意**: 実際には早期終了により、大幅に短縮される

### 5. メモ化の可能性
- **問題**: 同じremaining値が複数回計算される可能性がある
- **解決策**: メモ化を使って、同じremaining値の結果を再利用
- **実装**: `@lru_cache`でメモ化
- **注意**: この問題では、combinationが異なるため、メモ化は効果的でない場合がある

### 6. ソートの重要性
- **問題**: ソートしないと、早期終了が効率的に機能しない
- **解決策**: 最初に配列をソート
- **実装**: `candidates.sort()`
- **メリット**: 早期終了により、探索空間を削減

### 7. 同じ要素の再利用
- **問題**: 同じ要素を何度でも使用できる
- **解決策**: 再帰時に`i`から開始（`start=i`）
- **実装**: `backtrack(combination, i, remaining - candidates[i])`
- **注意**: `i+1`にすると、同じ要素を再度使用できない

### 8. バックトラック時の状態復元
- **問題**: バックトラック時に、combinationを正確に復元する必要がある
- **解決策**: 再帰呼び出しの後、追加した要素を削除
- **実装**: `combination.pop()`で元に戻す
- **注意**: リストを直接変更するため、正確な復元が重要

## 関連問題

- [Combination Sum II](../leetcode/medium/) - 各要素を1回だけ使用
- [Combination Sum III](../leetcode/medium/) - k個の数字でtargetを達成
- [Combination Sum IV](../leetcode/medium/) - 順序を考慮（DP問題）
- [Generate Parentheses](./generate_parentheses_logic.md) - バックトラッキングの基本

---

**次のステップ**: [Trieテクニック](../15_trie/README.md)で文字列検索を学ぶ

