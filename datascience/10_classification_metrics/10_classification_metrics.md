# 分類評価指標

## 概要

分類問題におけるモデルの性能を評価するための様々な指標について学習します。単純な精度から、混同行列、Precision、Recall、F1-score、Specificityまで、実務で重要な評価指標を網羅的に解説します。

## 1. 基本的な評価指標

### 1.1 精度（Accuracy）

**定義**：
```
Accuracy = (正解数) / (全サンプル数) = (TP + TN) / (TP + TN + FP + FN)
```

**特徴**：
- 最も直感的な指標
- 0から1の範囲
- 1に近いほど良い

**制限**：
- クラス不均衡データでは適切でない場合がある
- すべてのクラスを等しく扱う

### 1.2 混同行列（Confusion Matrix）

**2×2混同行列**：
```
                予測
            0       1
実際  0    TN      FP
     1    FN      TP
```

**要素の説明**：
- **TP（True Positive）**：正しく正例と予測
- **TN（True Negative）**：正しく負例と予測
- **FP（False Positive）**：間違って正例と予測（Type I Error）
- **FN（False Negative）**：間違って負例と予測（Type II Error）

### 1.3 混同行列の解釈

**医療診断の例**：
- TP：病気の人を正しく病気と診断
- TN：健康な人を正しく健康と診断
- FP：健康な人を病気と誤診断（偽陽性）
- FN：病気の人を健康と誤診断（偽陰性）

## 2. 主要な評価指標

### 2.1 Precision（適合率）

**定義**：
```
Precision = TP / (TP + FP)
```

**意味**：
- 正例と予測したもののうち、実際に正例だった割合
- 「予測の精度」

**実務での意味**：
- スパム判定：スパムと判定したメールのうち、実際にスパムだった割合
- 推薦システム：推薦した商品のうち、実際に購入された割合

### 2.2 Recall（再現率）

**定義**：
```
Recall = TP / (TP + FN)
```

**意味**：
- 実際の正例のうち、正しく正例と予測できた割合
- 「見逃しの少なさ」

**実務での意味**：
- 医療診断：病気の人を正しく病気と診断できた割合
- 不正検知：不正取引を正しく検知できた割合

### 2.3 Specificity（特異度）

**定義**：
```
Specificity = TN / (TN + FP)
```

**意味**：
- 実際の負例のうち、正しく負例と予測できた割合
- 「偽陽性の少なさ」

### 2.4 F1-score

**定義**：
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

**意味**：
- PrecisionとRecallの調和平均
- バランスの取れた指標

**特徴**：
- 0から1の範囲
- 1に近いほど良い
- PrecisionとRecallの両方を考慮

## 3. 多クラス分類の評価指標

### 3.1 Macro平均

**定義**：
```
Macro-Precision = (1/K) Σ[k=1 to K] Precision_k
Macro-Recall = (1/K) Σ[k=1 to K] Recall_k
Macro-F1 = (1/K) Σ[k=1 to K] F1_k
```

**特徴**：
- 各クラスを等しく扱う
- 少数クラスの影響を受けやすい

### 3.2 Micro平均

**定義**：
```
Micro-Precision = Micro-Recall = Micro-F1 = Accuracy
```

**特徴**：
- 全体的な性能を反映
- 多数クラスの影響を受けやすい

### 3.3 Weighted平均

**定義**：
```
Weighted-Precision = Σ[k=1 to K] (n_k / N) × Precision_k
```

**特徴**：
- クラスのサンプル数に比例して重み付け
- 実用的な指標

## 4. 実務での指標選択

### 4.1 医療診断

**重要な指標**：
- **Recall**：病気の見逃しを避ける
- **Specificity**：健康な人の誤診を避ける

**トレードオフ**：
- Recallを上げると、Specificityが下がる
- 適切な閾値の選択が重要

### 4.2 スパム判定

**重要な指標**：
- **Precision**：重要なメールの誤判定を避ける
- **Recall**：スパムメールの見逃しを避ける

### 4.3 推薦システム

**重要な指標**：
- **Precision**：推薦の精度
- **Recall**：商品の網羅性

## 5. 閾値の調整

### 5.1 決定閾値の影響

**閾値を下げる**：
- Recall ↑、Precision ↓
- より多くの正例を検出
- 偽陽性が増加

**閾値を上げる**：
- Precision ↑、Recall ↓
- より確実な正例のみ検出
- 偽陰性が増加

### 5.2 最適な閾値の選択

**方法**：
1. **F1-score最大化**：バランス重視
2. **Precision-Recall曲線**：トレードオフの可視化
3. **ビジネス要件**：コストとベネフィットの考慮

## 6. クラス不均衡への対処

### 6.1 問題点

**不均衡データでの問題**：
- Accuracyが不適切
- 多数クラスに偏った評価
- 少数クラスの性能が見えない

### 6.2 対処法

**評価指標の選択**：
- Precision、Recall、F1-score
- ROC-AUC
- Precision-Recall曲線

**データの調整**：
- サンプリング手法
- コスト感度学習
- アンサンブル手法

## 7. 実装の詳細

### 7.1 scikit-learnでの実装

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

# 基本的な指標
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# 多クラス分類
precision_macro = precision_score(y_true, y_pred, average='macro')
recall_macro = recall_score(y_true, y_pred, average='macro')
f1_macro = f1_score(y_true, y_pred, average='macro')
```

### 7.2 混同行列の可視化

```python
import matplotlib.pyplot as plt
import seaborn as sns

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()
```

## 8. よくある落とし穴

### 8.1 指標の誤解釈

**よくある間違い**：
- Accuracyが高ければ良いモデル
- 単一の指標でモデルを評価
- クラス不均衡を考慮しない

### 8.2 適切な指標の選択

**考慮すべき要因**：
- ビジネス要件
- データの特性
- コストとベネフィット
- 解釈可能性

## 9. 高度な評価手法

### 9.1 クロスバリデーション

**目的**：
- モデルの汎化性能の評価
- 過学習の検出
- 安定した性能指標の取得

### 9.2 統計的有意性検定

**目的**：
- モデル間の性能差の検証
- 偶然による差の排除
- 信頼性の高い結論

### 9.3 学習曲線

**目的**：
- データ量と性能の関係
- 過学習の検出
- 必要なデータ量の推定

## 10. まとめ

分類評価指標は、モデルの性能を多角的に評価するための重要なツールです。

**重要なポイント**：
- 単一の指標に依存しない
- ビジネス要件に応じた指標選択
- クラス不均衡への配慮
- 適切な閾値の設定

**実務での活用**：
- モデル選択の基準
- ハイパーパラメータの調整
- ビジネス判断の支援

## 関連トピック

- [ROC/AUC](../11_roc_auc/11_roc_auc.md)
- [多クラス分類](../09_multiclass_classification/09_multiclass_classification.md)
- [ロジスティック回帰](../08_logistic_regression/08_logistic_regression.md)
