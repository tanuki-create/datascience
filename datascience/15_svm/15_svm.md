# サポートベクターマシン（SVM）

## 概要

サポートベクターマシン（Support Vector Machine, SVM）は、マージンを最大化することで分類を行う強力な機械学習手法です。高次元データや非線形問題に対して優れた性能を発揮します。

## 1. SVMの基本概念

### 1.1 マージン最大化

**マージン**：
- 決定境界と最も近いデータポイント間の距離
- 最大化することで汎化性能を向上

**サポートベクター**：
- マージンに最も近いデータポイント
- 決定境界を定義する重要な点

### 1.2 数学的定式化

**目的関数**：
```
min (1/2)||w||² + CΣᵢ ξᵢ
```

**制約条件**：
```
yᵢ(wᵀxᵢ + b) ≥ 1 - ξᵢ
ξᵢ ≥ 0
```

## 2. ハードマージンとソフトマージン

### 2.1 ハードマージン

**完全分離可能**：
- 線形分離可能なデータ
- マージン内にデータポイントなし
- 制約：yᵢ(wᵀxᵢ + b) ≥ 1

### 2.2 ソフトマージン

**不完全分離**：
- ノイズや外れ値の存在
- スラック変数ξᵢの導入
- 制約：yᵢ(wᵀxᵢ + b) ≥ 1 - ξᵢ

**パラメータC**：
- 正則化パラメータ
- 誤分類の許容度
- マージンと誤分類のトレードオフ

## 3. カーネルトリック

### 3.1 非線形変換

**特徴空間**：
- 高次元空間への写像
- 非線形関係の捉え方
- 計算コストの課題

**カーネル関数**：
- 内積の直接計算
- 高次元空間での計算回避
- 効率的な非線形分類

### 3.2 主要なカーネル

**線形カーネル**：
```
K(x, x') = xᵀx'
```

**多項式カーネル**：
```
K(x, x') = (xᵀx' + c)ᵈ
```

**RBFカーネル（ガウシアン）**：
```
K(x, x') = exp(-γ||x - x'||²)
```

**シグモイドカーネル**：
```
K(x, x') = tanh(γxᵀx' + c)
```

## 4. SVMの実装

### 4.1 基本的な実装

```python
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# データの準備
X, y = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                          n_informative=2, n_clusters_per_class=1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVMの訓練
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm.fit(X_train, y_train)

# 予測と評価
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
```

### 4.2 パラメータの調整

**C（正則化パラメータ）**：
- 小さい値：大きなマージン、多くの誤分類
- 大きい値：小さなマージン、少ない誤分類

**gamma（RBFカーネル）**：
- 小さい値：滑らかな決定境界
- 大きい値：複雑な決定境界

## 5. 決定境界の可視化

### 5.1 2D可視化

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.svm import SVC

# データの生成
X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, 
                          n_informative=2, n_clusters_per_class=1, random_state=42)

# SVMの訓練
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X, y)

# 決定境界の可視化
def plot_decision_boundary(X, y, model, title):
    # メッシュグリッドの作成
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    
    # 予測
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # プロット
    plt.figure(figsize=(10, 8))
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.RdYlBu)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolors='black')
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

plot_decision_boundary(X, y, svm, 'SVM Decision Boundary')
```

### 5.2 サポートベクターの可視化

```python
# サポートベクターの取得
support_vectors = svm.support_vectors_
support_vector_indices = svm.support_

# 可視化
plt.figure(figsize=(10, 8))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, alpha=0.7)
plt.scatter(support_vectors[:, 0], support_vectors[:, 1], 
           s=100, facecolors='none', edgecolors='red', linewidth=2)
plt.title('Support Vectors')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
```

## 6. 多クラス分類

### 6.1 One-vs-Rest（OvR）

**手法**：
- 各クラス vs その他
- k個のバイナリ分類器
- 最も高いスコアのクラスを選択

### 6.2 One-vs-One（OvO）

**手法**：
- 全てのクラスペアで分類
- k(k-1)/2個のバイナリ分類器
- 投票による最終決定

### 6.3 実装例

```python
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 多クラスデータの準備
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 多クラスSVMの訓練
svm_multiclass = SVC(kernel='rbf', C=1.0, gamma='scale', decision_function_shape='ovr')
svm_multiclass.fit(X_train, y_train)

# 予測と評価
y_pred = svm_multiclass.predict(X_test)
print("Multi-class SVM Results:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

## 7. 回帰問題への応用

### 7.1 SVR（Support Vector Regression）

**目的関数**：
```
min (1/2)||w||² + CΣᵢ (ξᵢ + ξᵢ*)
```

**制約条件**：
```
yᵢ - (wᵀxᵢ + b) ≤ ε + ξᵢ
(wᵀxᵢ + b) - yᵢ ≤ ε + ξᵢ*
```

### 7.2 実装例

```python
from sklearn.svm import SVR
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 回帰データの準備
X, y = make_regression(n_samples=100, n_features=1, noise=0.1, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVRの訓練
svr = SVR(kernel='rbf', C=1.0, gamma='scale', epsilon=0.1)
svr.fit(X_train, y_train)

# 予測と評価
y_pred = svr.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"R²: {r2:.4f}")
```

## 8. 実務での活用

### 8.1 テキスト分類

**文書分類**：
- スパム検知
- 感情分析
- トピック分類

**特徴量**：
- TF-IDF
- 単語の出現頻度
- n-gram

### 8.2 画像分類

**画像認識**：
- 物体検出
- 顔認識
- 医療画像解析

**特徴量**：
- ピクセル値
- ヒストグラム
- テクスチャ特徴

### 8.3 異常検知

**外れ値検出**：
- 不正検知
- 品質管理
- システム監視

**One-class SVM**：
- 正常データのみで学習
- 異常パターンの検出

## 9. よくある落とし穴

### 9.1 パラメータの選択

**Cの選択**：
- 過小：アンダーフィッティング
- 過大：オーバーフィッティング
- 交差検証による調整

**gammaの選択**：
- 過小：滑らかすぎる境界
- 過大：複雑すぎる境界
- データの特性に応じた調整

### 9.2 計算コスト

**大規模データ**：
- 計算時間の増加
- メモリ使用量
- 近似手法の活用

**カーネル選択**：
- 線形カーネル：高速
- RBFカーネル：柔軟性
- 問題に応じた選択

## 10. まとめ

SVMは、マージン最大化による強力な分類手法です。

**重要なポイント**：
- マージン最大化の原理
- カーネルトリックの活用
- パラメータの適切な調整
- 実務での応用

**実務での活用**：
- 高次元データの分類
- 非線形問題の解決
- 異常検知
- テキスト・画像分類

## 関連トピック

- [分類評価指標](../10_classification_metrics/10_classification_metrics.md)
- [ロジスティック回帰](../08_logistic_regression/08_logistic_regression.md)
- [主成分分析](../12_pca/12_pca.md)
