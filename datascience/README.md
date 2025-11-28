# 線形回帰 完全ガイド


機械学習の基礎である線形回帰を、理論から実装まで段階的に学習できる包括的な教材です。
１２３

## 📚 教材の構成

### 1. 基礎編 (01_basics/)
線形回帰の基本理論と最適化手法を学びます。

- **理論**: [線形回帰の基礎](01_basics/01_linear_regression_basics.md)
- **実装**:
  - [最急降下法の実装](01_basics/notebooks/gradient_descent_implementation.ipynb)
  - [正規方程式の実装](01_basics/notebooks/normal_equation_implementation.ipynb)
  - [基本的な線形回帰](01_basics/notebooks/linear_regression_basic.ipynb)

**学習内容**:
- 線形回帰とは何か
- 最小二乗法の原理
- 最急降下法の段階的実装
- 正規方程式による解析解
- 実践的な応用例

### 2. 特徴量スケーリング編 (02_feature_scaling/)
データの前処理として重要なスケーリング手法を学びます。

- **理論**: [特徴量スケーリング](02_feature_scaling/02_feature_scaling.md)
- **実装**:
  - [標準化の実装](02_feature_scaling/notebooks/standardization.ipynb)
  - [正規化の実装](02_feature_scaling/notebooks/normalization.ipynb)

**学習内容**:
- 標準化 (Standardization)
- 正規化 (Normalization)
- スケーリング手法の使い分け
- データリークの回避

### 3. 統計的推論編 (03_statistical_inference/)
回帰係数の統計的検定と解釈を学びます。

- **理論**: [統計的推論](03_statistical_inference/03_statistical_inference.md)
- **実装**:
  - [係数のt検定](03_statistical_inference/notebooks/coefficient_t_test.ipynb)
  - [ダミー変数](03_statistical_inference/notebooks/dummy_variables.ipynb)

**学習内容**:
- 係数の仮説検定 (t検定)
- モデル全体の検定 (F検定)
- one-hotエンコーディング
- ダミー変数トラップ

### 4. モデル評価編 (04_model_evaluation/)
モデルの汎化性能を評価する手法を学びます。

- **理論**: [モデル評価](04_model_evaluation/04_model_evaluation.md)
- **実装**:
  - [Hold-out法](04_model_evaluation/notebooks/holdout_validation.ipynb)
  - [LOOCV](04_model_evaluation/notebooks/loocv_implementation.ipynb)
  - [k-Fold CV](04_model_evaluation/notebooks/kfold_cv_implementation.ipynb)
  - [Pipeline](04_model_evaluation/notebooks/pipeline_cv_scaling.ipynb)

**学習内容**:
- 汎化性能と過学習
- Hold-out法
- 交差検証 (LOOCV, k-Fold)
- Bias-Variance Tradeoff

### 5. 評価指標編 (05_metrics/)
回帰モデルの性能を測る指標を学びます。

- **理論**: [評価指標](05_metrics/05_evaluation_metrics.md)
- **実装**:
  - [回帰評価指標](05_metrics/notebooks/regression_metrics.ipynb)

**学習内容**:
- MSE, RMSE, MAE
- R² (決定係数)
- 調整済みR²
- 指標の使い分け

### 6. 非線形回帰編 (06_nonlinear_regression/)
線形回帰を拡張した非線形モデルを学びます。

- **理論**: [非線形回帰](06_nonlinear_regression/06_nonlinear_regression.md)
- **実装**:
  - [多項式特徴量](06_nonlinear_regression/notebooks/polynomial_features.ipynb)
  - [多項式回帰](06_nonlinear_regression/notebooks/polynomial_regression.ipynb)
  - [kNN回帰](06_nonlinear_regression/notebooks/knn_regression.ipynb)
  - [様々なkの比較](06_nonlinear_regression/notebooks/knn_various_k.ipynb)

**学習内容**:
- 多項式特徴量の生成
- 多項式回帰の実装
- k近傍法 (kNN) 回帰
- 線形 vs 非線形の比較

### 7. 総まとめ (07_summary/)
線形回帰のベストプラクティスと実践ガイドです。

- **総括**: [総まとめ](07_summary/07_comprehensive_summary.md)

**学習内容**:
- ベストプラクティス
- 実践的なワークフロー
- よくある問題と解決策
- 次のステップ

## 🎯 学習の進め方

### 初学者向け
1. **基礎編**から順番に学習
2. 理論のMDファイルを読む
3. 対応するJupyterノートブックで実装
4. 演習問題に取り組む

### 中級者向け
- 興味のあるトピックから学習可能
- 各セクションは独立して学習できます
- 実装の詳細を重点的に学習

### 実務者向け
- **総まとめ**からベストプラクティスを確認
- 必要に応じて各トピックを参照
- パイプラインの実装例を活用

## 💻 環境構築

### 必要なライブラリ

```bash
pip install numpy pandas matplotlib seaborn scikit-learn scipy jupyter
```

または

```bash
pip install -r requirements.txt
```

### Jupyter Notebookの起動

```bash
jupyter notebook
```

## 📖 各章の所要時間目安

| 章 | 理論 | 実装 | 合計 |
|----|------|------|------|
| 1. 基礎編 | 30分 | 90分 | 2時間 |
| 2. 特徴量スケーリング | 15分 | 30分 | 45分 |
| 3. 統計的推論 | 30分 | 60分 | 1.5時間 |
| 4. モデル評価 | 45分 | 90分 | 2.25時間 |
| 5. 評価指標 | 20分 | 30分 | 50分 |
| 6. 非線形回帰 | 25分 | 75分 | 1.75時間 |
| 7. 総まとめ | 30分 | - | 30分 |
| **合計** | **3.25時間** | **6.25時間** | **9.5時間** |

## 🎓 学習目標

### 基礎レベル
- [ ] 線形回帰の基本概念を理解する
- [ ] 最小二乗法の原理を説明できる
- [ ] scikit-learnで線形回帰を実装できる

### 中級レベル
- [ ] 最急降下法を実装できる
- [ ] 正規方程式を導出できる
- [ ] 交差検証を適切に使用できる
- [ ] 評価指標を適切に選択できる

### 上級レベル
- [ ] アルゴリズムの数学的背景を理解する
- [ ] パイプラインで完全な機械学習フローを構築できる
- [ ] ビジネス課題に対して適切なモデルを選択・実装できる

## 🔍 実践的な応用例

各ノートブックには以下のような実践例が含まれています：

- **住宅価格予測**: 面積、築年数、立地から価格を予測
- **売上予測**: 広告費、価格、競合から売上を予測
- **顧客満足度分析**: サービス品質から満足度を予測

## 📝 演習問題

各ノートブックには演習問題が含まれています：
- 基礎的な実装問題
- 応用的な分析問題
- 実データでの検証問題

## 🚀 次のステップ

線形回帰を習得した後は：
1. **ロジスティック回帰**: 分類問題への応用
2. **正則化**: Ridge、Lasso回帰
3. **一般化線形モデル**: GLM
4. **ニューラルネットワーク**: ディープラーニング

## 📚 参考資料

### 書籍
- 「統計的学習の基礎」Trevor Hastie他
- 「パターン認識と機械学習」Christopher M. Bishop
- 「Machine Learning」Andrew Ng (Coursera)

### オンラインリソース
- scikit-learn公式ドキュメント
- Kaggle Learn
- Towards Data Science

## 🤝 貢献

このプロジェクトへの貢献を歓迎します：
- バグ報告
- 新しい演習問題の提案
- 翻訳の改善
- 追加の実装例

## 📄 ライセンス

このプロジェクトは教育目的で作成されました。自由に学習・改変・共有してください。

## 📧 お問い合わせ

質問や提案がありましたら、お気軽にお問い合わせください。

---

**最終更新**: 2025年10月

**Happy Learning! 📊🎉**
