# 特徴量スケーリング

## 目次
1. [特徴量スケーリングとは](#特徴量スケーリングとは)
2. [標準化](#標準化)
3. [正規化](#正規化)
4. [その他のスケーリング手法](#その他のスケーリング手法)
5. [スケーリングの必要性](#スケーリングの必要性)
6. [実装時の注意点](#実装時の注意点)
7. [まとめ](#まとめ)

## 特徴量スケーリングとは

### 定義
特徴量スケーリング（Feature Scaling）は、**異なるスケールを持つ特徴量を同じ範囲に変換する**前処理手法です。機械学習アルゴリズムの性能向上と安定化に重要な役割を果たします。

### なぜスケーリングが必要か

#### 1. アルゴリズムの特性
- **距離ベースのアルゴリズム**: k-NN、k-meansなど
- **勾配ベースのアルゴリズム**: 最急降下法、ニューラルネットワークなど
- **正則化**: Ridge、Lasso回帰など

#### 2. 数値的安定性
- **計算の安定性**: 大きな値による数値誤差の回避
- **収束の改善**: 最適化アルゴリズムの収束速度向上
- **正則化の効果**: 正則化項の適切な作用

### 具体例：住宅価格予測

**問題のあるデータ**:
| 面積(m²) | 築年数(年) | 価格(万円) |
|---------|-----------|-----------|
| 80      | 5         | 4000      |
| 120     | 10        | 6000      |
| 60      | 2         | 3000      |

**問題点**:
- 面積: 60-120の範囲
- 築年数: 2-10の範囲
- 価格: 3000-6000の範囲

面積の値が築年数より10倍大きいため、面積が価格に与える影響が過大評価される可能性があります。

## 標準化

### 基本概念
標準化（Standardization）は、**平均を0、標準偏差を1に変換する**手法です。

### 数学的表現

**Z-score標準化**:
```
z = (x - μ) / σ
```

ここで：
- `x`: 元の値
- `μ`: 平均値
- `σ`: 標準偏差
- `z`: 標準化後の値

### 標準化の特徴

#### 利点
1. **平均0、分散1**: 正規分布に近い形になる
2. **外れ値に頑健**: 極端な値の影響を軽減
3. **解釈しやすい**: 標準偏差の倍数として表現

#### 制約
1. **正規分布を仮定**: 非正規分布では効果が限定的
2. **外れ値の影響**: 極端な外れ値があると全体に影響
3. **データの分布**: 元の分布の形状は保持される

### 実装例

```python
from sklearn.preprocessing import StandardScaler

# 標準化の実行
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# パラメータの確認
print(f"平均: {scaler.mean_}")
print(f"標準偏差: {scaler.scale_}")
```

### 適用場面

**標準化が適している場合**:
- データが正規分布に近い
- 外れ値が少ない
- 線形回帰、ロジスティック回帰
- ニューラルネットワーク

## 正規化

### 基本概念
正規化（Normalization）は、**値を0から1の範囲に変換する**手法です。

### 数学的表現

**Min-Max正規化**:
```
x_norm = (x - x_min) / (x_max - x_min)
```

ここで：
- `x`: 元の値
- `x_min`: 最小値
- `x_max`: 最大値
- `x_norm`: 正規化後の値

### 正規化の特徴

#### 利点
1. **範囲が明確**: 0から1の固定範囲
2. **解釈しやすい**: パーセンテージとして理解可能
3. **外れ値の影響**: 最小値と最大値のみに依存

#### 制約
1. **外れ値に敏感**: 極端な値があると全体に影響
2. **分布の歪み**: 元の分布の形状が変わる
3. **新しいデータ**: 訓練時の範囲を超える値の処理

### 実装例

```python
from sklearn.preprocessing import MinMaxScaler

# 正規化の実行
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)

# パラメータの確認
print(f"最小値: {scaler.data_min_}")
print(f"最大値: {scaler.data_max_}")
```

### 適用場面

**正規化が適している場合**:
- データの範囲が明確
- 外れ値が少ない
- k-NN、k-means
- 画像処理（ピクセル値0-255）

## その他のスケーリング手法

### 1. Robust Scaling
**外れ値に頑健な標準化**:
```
x_robust = (x - median) / IQR
```

- `median`: 中央値
- `IQR`: 四分位範囲（Q3 - Q1）

### 2. Unit Vector Scaling
**ベクトルの長さを1に正規化**:
```
x_unit = x / ||x||
```

### 3. Log Transformation
**対数変換によるスケーリング**:
```
x_log = log(x + 1)
```

### 4. Box-Cox Transformation
**正規分布に近づける変換**:
```
x_boxcox = (x^λ - 1) / λ
```

## スケーリングの必要性

### アルゴリズム別の必要性

#### 必須（Required）
- **k-NN**: 距離計算に影響
- **k-means**: クラスタリングに影響
- **SVM**: マージンの計算に影響
- **最急降下法**: 収束速度に影響

#### 推奨（Recommended）
- **線形回帰**: 正則化の効果
- **ロジスティック回帰**: 収束の改善
- **ニューラルネットワーク**: 学習の安定化

#### 不要（Not Required）
- **決定木**: 分割基準に影響しない
- **ランダムフォレスト**: 決定木ベース
- **勾配ブースティング**: 決定木ベース

### 具体例：最急降下法での影響

**スケーリングなし**:
```
特徴量1: [1, 2, 3, 4, 5]
特徴量2: [1000, 2000, 3000, 4000, 5000]
```

特徴量2の勾配が特徴量1より1000倍大きくなり、収束が不安定になります。

**スケーリング後**:
```
特徴量1: [-1.41, -0.71, 0, 0.71, 1.41]
特徴量2: [-1.41, -0.71, 0, 0.71, 1.41]
```

両特徴量が同じスケールになり、安定した収束が期待できます。

## 実装時の注意点

### 1. データリークの回避

**間違った方法**:
```python
# 全データでスケーリング（データリーク）
scaler.fit(X_all)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**正しい方法**:
```python
# 訓練データのみでスケーリング
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 2. パイプラインの使用

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# パイプラインの作成
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

# 訓練と予測
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

### 3. 交差検証での注意

```python
from sklearn.model_selection import cross_val_score

# パイプラインを使用することで、各Foldで適切にスケーリング
scores = cross_val_score(pipeline, X, y, cv=5)
```

### 4. 新しいデータの処理

```python
# 新しいデータの予測
new_data = [[100, 5, 10]]  # 新しい住宅データ
new_data_scaled = scaler.transform(new_data)
prediction = model.predict(new_data_scaled)
```

## まとめ

### 特徴量スケーリングの重要性

1. **アルゴリズムの性能向上**: 特に距離ベースと勾配ベースのアルゴリズム
2. **数値的安定性**: 計算の安定性と収束の改善
3. **正則化の効果**: 適切な正則化の適用
4. **解釈性の向上**: 特徴量の重要度の公平な比較

### 手法の選択指針

| 手法 | 適用場面 | 利点 | 制約 |
|------|----------|------|------|
| 標準化 | 正規分布、外れ値少 | 解釈しやすい | 外れ値に敏感 |
| 正規化 | 範囲明確、外れ値少 | 範囲固定 | 外れ値に敏感 |
| Robust | 外れ値多 | 外れ値に頑健 | 計算複雑 |
| 対数変換 | 右裾分布 | 分布改善 | 0以下不可 |

### 実践的なポイント

1. **データの理解**: 分布と外れ値の確認
2. **アルゴリズムの特性**: スケーリングの必要性の判断
3. **パイプラインの活用**: データリークの回避
4. **交差検証**: 適切な評価手順の確保

### 次のステップ

- [標準化の実装](./notebooks/standardization.ipynb)
- [正規化の実装](./notebooks/normalization.ipynb)
- [統計的推論](../03_statistical_inference/03_statistical_inference.md)
- [モデル評価](../04_model_evaluation/04_model_evaluation.md)

---

**関連ノートブック**:
- [標準化の実装](./notebooks/standardization.ipynb)
- [正規化の実装](./notebooks/normalization.ipynb)
