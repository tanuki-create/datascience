# 主成分分析（PCA）

## 概要

主成分分析（Principal Component Analysis, PCA）は、高次元データの次元削減と可視化のための強力な手法です。データの分散を最大化する方向を見つけ、重要な情報を保持しながら次元を削減します。

## 1. PCAの基本概念

### 1.1 主成分とは

**定義**：
- データの分散を最大化する方向
- 元の特徴量の線形結合
- 互いに直交する

**数学的表現**：
```
PC1 = w₁₁x₁ + w₁₂x₂ + ... + w₁ₙxₙ
PC2 = w₂₁x₁ + w₂₂x₂ + ... + w₂ₙxₙ
```

### 1.2 固有値と固有ベクトル

**共分散行列**：
```
C = (1/n) X^T X
```

**固有値分解**：
```
C = P Λ P^T
```
- P: 固有ベクトル行列
- Λ: 固有値行列

## 2. PCAの手順

### 2.1 データの前処理

1. **平均化**：各特徴量の平均を0にする
2. **標準化**：各特徴量の分散を1にする（オプション）

### 2.2 主成分の計算

1. **共分散行列の計算**
2. **固有値・固有ベクトルの計算**
3. **固有値の降順ソート**
4. **主成分の選択**

### 2.3 次元削減

**寄与率**：
```
Contribution Ratio = λᵢ / Σλⱼ
```

**累積寄与率**：
```
Cumulative Ratio = Σᵢ₌₁ᵏ λᵢ / Σⱼ₌₁ᵈ λⱼ
```

## 3. PCAの実装

### 3.1 手動実装

```python
def pca_manual(X):
    # 1. データの標準化
    X_centered = X - np.mean(X, axis=0)
    
    # 2. 共分散行列の計算
    cov_matrix = np.cov(X_centered.T)
    
    # 3. 固有値・固有ベクトルの計算
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # 4. 固有値の降順ソート
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvalues, eigenvectors
```

### 3.2 scikit-learnでの実装

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# データの標準化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCAの適用
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 寄与率の取得
explained_variance_ratio = pca.explained_variance_ratio_
```

## 4. PCAの解釈

### 4.1 寄与率の解釈

**寄与率**：
- 各主成分が全体の分散に占める割合
- 高い寄与率 = 重要な情報

**累積寄与率**：
- 最初のk個の主成分で説明される分散の割合
- 次元削減の指標

### 4.2 主成分の意味

**第1主成分**：
- 最大の分散を持つ方向
- データの主要な変動

**第2主成分**：
- 第1主成分と直交する方向
- 第2に大きな分散を持つ方向

## 5. PCAの応用

### 5.1 次元削減

**目的**：
- 計算コストの削減
- 可視化の改善
- ノイズの除去

**手順**：
1. 寄与率の確認
2. 主成分数の決定
3. データの変換

### 5.2 可視化

**2D可視化**：
- 第1・第2主成分でプロット
- データの構造の理解

**3D可視化**：
- 第1・第2・第3主成分でプロット
- より詳細な分析

### 5.3 特徴量エンジニアリング

**新特徴量**：
- 主成分を新しい特徴量として使用
- 元の特徴量の線形結合

## 6. PCAの制限と注意点

### 6.1 制限

**線形変換**：
- 非線形関係は捉えられない
- カーネルPCAが必要な場合がある

**解釈性**：
- 主成分の意味が不明確
- 元の特徴量との関係が複雑

### 6.2 注意点

**データの前処理**：
- 標準化の重要性
- 外れ値の影響

**主成分数の選択**：
- 寄与率の基準
- ドメイン知識の活用

## 7. 実装の詳細

### 7.1 完全な実装例

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# データの読み込み
iris = load_iris()
X, y = iris.data, iris.target

# データの標準化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCAの適用
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# 寄与率の可視化
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(range(1, 5), pca.explained_variance_ratio_)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Explained Variance Ratio by Component')

plt.subplot(1, 2, 2)
plt.plot(range(1, 5), np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('Cumulative Explained Variance Ratio')

plt.tight_layout()
plt.show()
```

### 7.2 主成分の可視化

```python
# 2D可視化
plt.figure(figsize=(10, 8))
colors = ['red', 'green', 'blue']
for i, color in enumerate(colors):
    plt.scatter(X_pca[y == i, 0], X_pca[y == i, 1], 
               c=color, label=iris.target_names[i], alpha=0.7)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA of Iris Dataset')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 8. 高度な話題

### 8.1 カーネルPCA

**非線形PCA**：
- カーネル関数を使用
- 非線形関係の捉え方

### 8.2 インクリメンタルPCA

**大規模データ**：
- メモリ効率的な実装
- オンライン学習

### 8.3 スパースPCA

**特徴選択**：
- スパース性の制約
- 解釈性の向上

## 9. 実務での活用

### 9.1 データ分析

**探索的データ分析**：
- 高次元データの可視化
- データの構造理解

**前処理**：
- 次元削減による計算効率化
- ノイズ除去

### 9.2 機械学習

**特徴量エンジニアリング**：
- 新しい特徴量の作成
- 次元の呪いの回避

**可視化**：
- モデルの解釈
- 結果の説明

## 10. まとめ

PCAは高次元データの理解と処理において重要な手法です。

**重要なポイント**：
- 分散最大化による次元削減
- 寄与率による主成分の選択
- 可視化と解釈の重要性
- 前処理の重要性

**実務での活用**：
- 探索的データ分析
- 特徴量エンジニアリング
- 可視化と解釈

## 関連トピック

- [特徴量スケーリング](../02_feature_scaling/02_feature_scaling.md)
- [クラスタリング](../13_clustering/13_clustering.md)
- [分類評価指標](../10_classification_metrics/10_classification_metrics.md)
