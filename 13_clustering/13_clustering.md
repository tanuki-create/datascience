# クラスタリング

## 概要

クラスタリングは、データを類似したグループに分ける教師なし学習の手法です。データの構造を発見し、隠れたパターンを理解するために使用されます。

## 1. クラスタリングの基本概念

### 1.1 クラスタリングとは

**定義**：
- 類似したデータポイントをグループ化
- 教師なし学習の代表的手法
- データの構造発見

**目的**：
- データの理解
- パターンの発見
- セグメンテーション

### 1.2 距離の定義

**ユークリッド距離**：
```
d(x, y) = √(Σ(xᵢ - yᵢ)²)
```

**マンハッタン距離**：
```
d(x, y) = Σ|xᵢ - yᵢ|
```

**コサイン類似度**：
```
cos(θ) = (x·y) / (||x|| ||y||)
```

## 2. k-meansクラスタリング

### 2.1 アルゴリズム

**手順**：
1. k個のクラスタ中心をランダムに初期化
2. 各データポイントを最も近い中心に割り当て
3. 各クラスタの中心を再計算
4. 収束するまで2-3を繰り返し

**目的関数**：
```
J = Σᵢ₌₁ᵏ Σₓ∈Cᵢ ||x - μᵢ||²
```

### 2.2 実装

```python
def kmeans(X, k, max_iters=100):
    # 1. 初期化
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    
    for _ in range(max_iters):
        # 2. クラスタ割り当て
        distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
        
        # 3. 中心の更新
        new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(k)])
        
        # 4. 収束判定
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    
    return centroids, labels
```

### 2.3 パラメータの選択

**kの選択**：
- エルボー法
- シルエット分析
- ドメイン知識

**初期化**：
- ランダム初期化
- k-means++初期化

## 3. 階層クラスタリング

### 3.1 アプローチ

**凝集型（Agglomerative）**：
- ボトムアップ
- 各データポイントから開始
- 最も近いクラスタを結合

**分割型（Divisive）**：
- トップダウン
- 全データから開始
- クラスタを分割

### 3.2 リンケージ基準

**単連結（Single Linkage）**：
```
d(C₁, C₂) = min{d(x, y) | x ∈ C₁, y ∈ C₂}
```

**完全連結（Complete Linkage）**：
```
d(C₁, C₂) = max{d(x, y) | x ∈ C₁, y ∈ C₂}
```

**平均連結（Average Linkage）**：
```
d(C₁, C₂) = (1/|C₁||C₂|) Σ d(x, y)
```

### 3.3 デンドログラム

**可視化**：
- 階層構造の表現
- クラスタ数の決定
- 距離の解釈

## 4. クラスタリングの評価

### 4.1 内部評価指標

**シルエット係数**：
```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

**エルボー法**：
- クラスタ内平方和（WCSS）の変化
- 最適なkの選択

### 4.2 外部評価指標

**調整ランド指数**：
- 既知のラベルとの比較
- 0から1の範囲

**正規化相互情報**：
- 情報理論的指標
- ラベルの独立性を考慮

## 5. 実装の詳細

### 5.1 k-meansの実装

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# データの生成
X, y_true = make_blobs(n_samples=300, centers=4, random_state=42)

# k-meansの適用
kmeans = KMeans(n_clusters=4, random_state=42)
y_pred = kmeans.fit_predict(X)

# 結果の可視化
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=y_true, cmap='viridis')
plt.title('True Clusters')

plt.subplot(1, 2, 2)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
           c='red', marker='x', s=200)
plt.title('K-means Clusters')

plt.tight_layout()
plt.show()
```

### 5.2 階層クラスタリングの実装

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 階層クラスタリング
clustering = AgglomerativeClustering(n_clusters=4)
y_pred = clustering.fit_predict(X)

# デンドログラムの作成
linkage_matrix = linkage(X, method='ward')
plt.figure(figsize=(10, 6))
dendrogram(linkage_matrix, truncate_mode='level', p=5)
plt.title('Dendrogram')
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.show()
```

## 6. 高度なクラスタリング手法

### 6.1 DBSCAN

**密度ベースクラスタリング**：
- ノイズの検出
- 任意の形状のクラスタ
- パラメータ：eps, min_samples

### 6.2 ガウシアンミクスチャモデル

**確率的クラスタリング**：
- ソフトクラスタリング
- 確率的割り当て
- EMアルゴリズム

### 6.3 スペクトラルクラスタリング

**グラフベース**：
- 非凸形状のクラスタ
- 類似度行列の固有値分解

## 7. 実務での活用

### 7.1 顧客セグメンテーション

**マーケティング**：
- 顧客の行動パターン分析
- ターゲティング戦略
- パーソナライゼーション

### 7.2 画像セグメンテーション

**コンピュータビジョン**：
- 画像の領域分割
- 物体検出の前処理
- 医療画像解析

### 7.3 異常検知

**アノマリ検出**：
- 外れ値の検出
- 不正検知
- 品質管理

## 8. よくある落とし穴

### 8.1 パラメータの選択

**k-means**：
- kの選択が困難
- 初期化の影響
- 局所最適解

**階層クラスタリング**：
- 計算コストが高い
- メモリ使用量
- ノイズへの敏感さ

### 8.2 データの前処理

**スケーリング**：
- 特徴量のスケール統一
- 距離計算への影響

**外れ値**：
- クラスタリングへの影響
- ロバストな手法の選択

## 9. まとめ

クラスタリングは、データの構造を理解するための強力な手法です。

**重要なポイント**：
- 距離の定義と選択
- パラメータの適切な設定
- 評価指標の理解
- 実務での応用

**実務での活用**：
- 顧客セグメンテーション
- 異常検知
- データの理解

## 関連トピック

- [主成分分析](../12_pca/12_pca.md)
- [特徴量スケーリング](../02_feature_scaling/02_feature_scaling.md)
- [分類評価指標](../10_classification_metrics/10_classification_metrics.md)
