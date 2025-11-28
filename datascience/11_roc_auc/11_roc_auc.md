# ROC曲線とAUC

## 概要

ROC曲線（Receiver Operating Characteristic curve）とAUC（Area Under the Curve）は、分類モデルの性能を評価するための強力なツールです。特にクラス不均衡データや、閾値の選択が重要な場合に有用です。

## 1. ROC曲線の基本概念

### 1.1 ROC曲線とは

**定義**：
- 横軸：偽陽性率（FPR: False Positive Rate）
- 縦軸：真陽性率（TPR: True Positive Rate = Recall）
- 異なる閾値でのTPRとFPRをプロット

**計算式**：
```
TPR = TP / (TP + FN) = Recall
FPR = FP / (FP + TN) = 1 - Specificity
```

### 1.2 ROC曲線の解釈

**理想的なモデル**：
- 左上の角（0, 1）に近い
- TPRが高く、FPRが低い
- 完全な分類器

**ランダムモデル**：
- 対角線上（y = x）
- TPR = FPR
- 予測力がない

## 2. AUC（Area Under the Curve）

### 2.1 AUCの定義

**意味**：
- ROC曲線の下の面積
- 0から1の範囲
- 1に近いほど良いモデル

**解釈**：
```
AUC = 1.0: 完全な分類器
AUC = 0.9-1.0: 優れた分類器
AUC = 0.8-0.9: 良い分類器
AUC = 0.7-0.8: まあまあの分類器
AUC = 0.6-0.7: 悪い分類器
AUC = 0.5: ランダムな分類器
AUC < 0.5: 予測が逆
```

### 2.2 AUCの利点

**利点**：
1. 閾値に依存しない
2. クラス不均衡に対して頑健
3. モデル間の比較が容易
4. 確率的解釈が可能

**確率的解釈**：
- ランダムに選んだ正例と負例のペアで
- 正例のスコアが負例より高い確率

## 3. ROC曲線とPrecision-Recall曲線の比較

### 3.1 使い分け

**ROC曲線が適している場合**：
- バランスの取れたデータ
- 負例が重要な場合
- 一般的なモデル評価

**Precision-Recall曲線が適している場合**：
- クラス不均衡データ
- 正例が重要な場合
- 医療診断、不正検知など

### 3.2 特徴の比較

| 特徴 | ROC曲線 | PR曲線 |
|------|---------|--------|
| 横軸 | FPR | Recall |
| 縦軸 | TPR | Precision |
| クラス不均衡 | 影響を受けにくい | 影響を受けやすい |
| 解釈 | 全体的な性能 | 正例の性能 |

## 4. 多クラス分類でのROC/AUC

### 4.1 One-vs-Rest（OvR）

**方法**：
- 各クラスを「そのクラス vs その他」として扱う
- クラスごとにROC曲線を描画
- クラスごとにAUCを計算

### 4.2 One-vs-One（OvO）

**方法**：
- 全てのクラスペアでROC曲線を描画
- より詳細な分析が可能
- 計算コストが高い

### 4.3 Macro/Micro平均

**Macro平均**：
- 各クラスのAUCの平均
- 各クラスを等しく扱う

**Micro平均**：
- 全クラスのTP、FP、TN、FNを集計
- 全体的な性能

## 5. 実装の詳細

### 5.1 scikit-learnでの実装

```python
from sklearn.metrics import roc_curve, auc, roc_auc_score

# ROC曲線の計算
fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)

# AUCの計算
auc_score = auc(fpr, tpr)
# または
auc_score = roc_auc_score(y_true, y_pred_proba)

# 可視化
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc_score:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

### 5.2 多クラス分類での実装

```python
from sklearn.metrics import roc_auc_score

# One-vs-Rest
auc_ovr = roc_auc_score(y_true, y_pred_proba, multi_class='ovr')

# One-vs-One
auc_ovo = roc_auc_score(y_true, y_pred_proba, multi_class='ovo')
```

## 6. 実務での活用

### 6.1 閾値の選択

**方法**：
1. ROC曲線上の点を選択
2. ビジネス要件に応じて調整
3. コストと利益を考慮

**Youden's Index**：
```
J = TPR - FPR
```
- Jを最大化する閾値を選択

### 6.2 モデルの比較

**方法**：
1. 複数モデルのROC曲線を同時プロット
2. AUCで定量的に比較
3. 信頼区間の計算

## 7. よくある落とし穴

### 7.1 AUCの過信

**注意点**：
- AUCが高くても実務で使えない場合がある
- 特定の閾値での性能も確認
- ビジネス要件を考慮

### 7.2 クラス不均衡の影響

**問題**：
- 極端な不均衡では誤解を招く
- Precision-Recall曲線も確認
- 適切な評価指標の選択

### 7.3 過学習の検出

**方法**：
- 訓練データとテストデータのROC曲線を比較
- AUCの差を確認
- クロスバリデーションの活用

## 8. まとめ

ROC曲線とAUCは、分類モデルの性能評価における標準的なツールです。

**重要なポイント**：
- ROC曲線は閾値に依存しない評価
- AUCは0から1の範囲で解釈が容易
- クラス不均衡に対して頑健
- モデル比較が容易

**実務での活用**：
- モデル選択の基準
- 閾値の最適化
- ビジネス判断の支援

## 関連トピック

- [分類評価指標](../10_classification_metrics/10_classification_metrics.md)
- [ロジスティック回帰](../08_logistic_regression/08_logistic_regression.md)
- [多クラス分類](../09_multiclass_classification/09_multiclass_classification.md)
