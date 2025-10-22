# 決定木

## 概要

決定木（Decision Tree）は、データの特徴量に基づいて決定を下すための木構造のモデルです。解釈しやすく、特徴量の重要度を理解できるため、実務で広く使用されています。

## 1. 決定木の基本概念

### 1.1 木構造の要素

**ノード（節点）**：
- 根ノード：最上位のノード
- 内部ノード：分割条件を持つノード
- 葉ノード：最終的な予測を行うノード

**エッジ（枝）**：
- ノード間の接続
- 分割条件の結果

### 1.2 決定木の種類

**分類木**：
- カテゴリを予測
- 離散値の出力
- クラス確率

**回帰木**：
- 連続値を予測
- 数値の出力
- 平均値

## 2. 分割基準

### 2.1 分類での分割基準

**ジニ不純度（Gini Impurity）**：
```
Gini = 1 - Σᵢ pᵢ²
```

**エントロピー（Entropy）**：
```
Entropy = -Σᵢ pᵢ log₂(pᵢ)
```

**情報利得（Information Gain）**：
```
IG = Entropy(parent) - Σᵢ (|Sᵢ|/|S|) × Entropy(Sᵢ)
```

### 2.2 回帰での分割基準

**平均二乗誤差（MSE）**：
```
MSE = (1/n) Σᵢ (yᵢ - ȳ)²
```

**平均絶対誤差（MAE）**：
```
MAE = (1/n) Σᵢ |yᵢ - ȳ|
```

## 3. 決定木の構築

### 3.1 アルゴリズム

**手順**：
1. 根ノードから開始
2. 最適な分割を見つける
3. 子ノードを作成
4. 各子ノードで再帰的に実行
5. 停止条件を満たすまで繰り返し

**停止条件**：
- 最大深度に到達
- 最小サンプル数
- 不純度の閾値

### 3.2 実装例

```python
def build_tree(X, y, max_depth=3, min_samples_split=2):
    # 停止条件のチェック
    if max_depth == 0 or len(X) < min_samples_split:
        return LeafNode(predict_class(y))
    
    # 最適な分割を見つける
    best_split = find_best_split(X, y)
    
    if best_split is None:
        return LeafNode(predict_class(y))
    
    # 子ノードを構築
    left_X, left_y, right_X, right_y = split_data(X, y, best_split)
    
    left_node = build_tree(left_X, left_y, max_depth-1, min_samples_split)
    right_node = build_tree(right_X, right_y, max_depth-1, min_samples_split)
    
    return InternalNode(best_split, left_node, right_node)
```

## 4. 特徴量の重要度

### 4.1 重要度の計算

**不純度減少**：
```
Importance = Σᵢ (pᵢ × Δimpurityᵢ)
```

**特徴量の使用頻度**：
- 分割に使用された回数
- 重み付き平均

### 4.2 解釈

**高い重要度**：
- 予測に重要な特徴量
- ビジネス洞察の獲得

**低い重要度**：
- 予測に不要な特徴量
- 特徴選択の指標

## 5. 過学習と対策

### 5.1 過学習の問題

**原因**：
- 深すぎる木
- 小さなデータセット
- ノイズの多いデータ

**症状**：
- 訓練データでの高い性能
- テストデータでの低い性能
- 複雑すぎるルール

### 5.2 剪定（Pruning）

**事前剪定（Pre-pruning）**：
- 最大深度の制限
- 最小サンプル数
- 不純度の閾値

**事後剪定（Post-pruning）**：
- 構築後の簡素化
- コスト複雑度パラメータ
- 交差検証による選択

## 6. 実装の詳細

### 6.1 scikit-learnでの実装

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# データの準備
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 決定木の訓練
tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(X_train, y_train)

# 予測と評価
y_pred = tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

### 6.2 木の可視化

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# 決定木の可視化
plt.figure(figsize=(12, 8))
plot_tree(tree, feature_names=iris.feature_names, 
          class_names=iris.target_names, filled=True)
plt.title('Decision Tree Visualization')
plt.show()

# 特徴量の重要度
feature_importance = tree.feature_importances_
plt.figure(figsize=(10, 6))
plt.barh(iris.feature_names, feature_importance)
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Decision Tree')
plt.show()
```

## 7. 高度な話題

### 7.1 アンサンブル手法

**ランダムフォレスト**：
- 複数の決定木の組み合わせ
- バギングによる多様性
- 過学習の抑制

**勾配ブースティング**：
- 逐次的な改善
- ブースティングによる性能向上
- 高度な最適化

### 7.2 連続値の処理

**分割点の選択**：
- 閾値の最適化
- 二分探索
- 効率的な計算

**離散化**：
- 連続値の離散化
- ビニング手法
- 適応的離散化

## 8. 実務での活用

### 8.1 ビジネスルールの抽出

**解釈性**：
- 人間が理解できるルール
- ビジネス判断の根拠
- 説明可能性

**意思決定支援**：
- ルールベースシステム
- エキスパートシステム
- 自動化の基盤

### 8.2 特徴量選択

**重要度分析**：
- 特徴量のランキング
- 不要な特徴量の特定
- 次元削減

**ドメイン知識**：
- 専門家の知識
- ビジネス理解
- 解釈の検証

## 9. よくある落とし穴

### 9.1 過学習の回避

**パラメータ調整**：
- max_depthの適切な設定
- min_samples_splitの調整
- 交差検証の活用

**正則化**：
- 剪定の重要性
- 複雑度の制御
- 汎化性能の向上

### 9.2 データの前処理

**欠損値**：
- 決定木での処理
- 欠損値の分割
- 前処理の重要性

**カテゴリ変数**：
- エンコーディング
- 順序の考慮
- 解釈性の保持

## 10. まとめ

決定木は、解釈しやすく実用的な機械学習手法です。

**重要なポイント**：
- 解釈性の高さ
- 特徴量の重要度
- 過学習への対策
- 実務での活用

**実務での活用**：
- ビジネスルールの抽出
- 特徴量選択
- 説明可能なAI

## 関連トピック

- [分類評価指標](../10_classification_metrics/10_classification_metrics.md)
- [ロジスティック回帰](../08_logistic_regression/08_logistic_regression.md)
- [特徴量スケーリング](../02_feature_scaling/02_feature_scaling.md)
