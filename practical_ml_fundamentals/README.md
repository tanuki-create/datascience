# 実践ML基礎 / Practical ML Fundamentals ガイド

このディレクトリは、機械学習の基礎を「現場でどう機能するか」から学ぶための日本語テキストです。古典的な回帰・分類から、深層学習、Transformer、Diffusion、評価、失敗解析、MLOps までを、数式だけでなくデータ・実装・運用の判断につなげて整理します。

参照元の PDF は私的利用の学習用リファレンスとして扱い、本ガイドの本文、例、演習、判断軸はオリジナルに作成します。PDF の翻訳や章ごとの要約ではありません。

## このディレクトリの位置づけ

- [pandas_methods_guide/](../pandas_methods_guide/) でデータ操作を学んだ後、実際にモデルを作る段階の橋渡し。
- [ml_research_practice/](../ml_research_practice/) の検証・R&D マインドセットへ進む前に、ML の基本部品を現場語彙で理解する場所。
- [object_detection/](../object_detection/) や [vector_search_cs_foundations/](../vector_search_cs_foundations/) のような専門領域に入る前の共通基礎。
- [system_design/16_ml_ai_systems/](../system_design/16_ml_ai_systems/) の推論・運用設計を読むための前提。

## ドキュメント構成

0. [00_core_message.md](./00_core_message.md)
   - ML を「データから意思決定ルールを作る仕事」として捉える
   - 現場でモデルより先に決めるべきこと

1. [01_problem_framing.md](./01_problem_framing.md)
   - 問題設定、目的変数、業務指標、使わない判断
   - PoC が失敗する典型パターン

2. [02_data_probability_uncertainty.md](./02_data_probability_uncertainty.md)
   - 確率、分布、サンプリング、不確実性
   - 数字を信じすぎないためのデータ観察

3. [03_regression_and_classification.md](./03_regression_and_classification.md)
   - 線形回帰、ロジスティック回帰、分類の基本
   - ベースラインの作り方

4. [04_loss_optimization_sgd.md](./04_loss_optimization_sgd.md)
   - 損失関数、勾配、SGD、学習曲線
   - 学習が不安定なときの疑う順

5. [05_generalization_regularization_validation.md](./05_generalization_regularization_validation.md)
   - 汎化、過学習、正則化、検証設計
   - validation を信じてよい条件

6. [06_classical_models_in_practice.md](./06_classical_models_in_practice.md)
   - kNN、Naive Bayes、木、SVM、Boosting
   - モデル選定を制約条件から説明する

7. [07_feature_engineering_and_pipelines.md](./07_feature_engineering_and_pipelines.md)
   - 前処理、特徴量、sklearn pipeline、train/serve skew
   - 手元実験から再利用可能な処理へ移す

8. [08_bayesian_em_latent_variables.md](./08_bayesian_em_latent_variables.md)
   - Bayesian、EM、GMM、潜在変数
   - 不確実性を出力に持たせる考え方

9. [09_dimensionality_reduction_representation.md](./09_dimensionality_reduction_representation.md)
   - PCA、埋め込み、表現学習
   - 圧縮・可視化・ノイズ除去の使い分け

10. [10_neural_networks_deep_learning.md](./10_neural_networks_deep_learning.md)
    - NN、CNN、RNN、転移学習、学習ループ
    - 深層学習を導入する判断基準

11. [11_transformers_self_supervised_llm.md](./11_transformers_self_supervised_llm.md)
    - Transformer、自己教師あり、LLM、RAG
    - 生成モデルを評価可能な部品として扱う

12. [12_generative_and_diffusion_models.md](./12_generative_and_diffusion_models.md)
    - VAE、GAN、Diffusion、条件付き生成
    - 品質、速度、制御性、安全性のトレードオフ

13. [13_evaluation_error_analysis_mlops.md](./13_evaluation_error_analysis_mlops.md)
    - 評価、失敗解析、監視、再学習、MLOps
    - 本番後に劣化したときの調査順

14. [14_capstone_project.md](./14_capstone_project.md)
    - end-to-end の実践課題
    - 問題設定からモデルカード、監視計画まで

15. [15_quick_reference.md](./15_quick_reference.md)
    - 現場判断の早見表
    - よくある症状と最初に疑う場所

補助: [sources.md](./sources.md)

## 読み方

- 初学者: `00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 07 -> 13`
- 実務投入前: `01 -> 03 -> 04 -> 05 -> 06 -> 07 -> 13 -> 14`
- 深層学習以降を急ぐ人: `00 -> 04 -> 05 -> 09 -> 10 -> 11 -> 12 -> 13`
- レビュー担当: `01 -> 02 -> 05 -> 13 -> 15`

## 実行できるサンプル

以下はリポジトリルート（`/Users/hiromitsu/datascience-1`）から実行します。

```bash
python practical_ml_fundamentals/examples/classification_baseline.py
python practical_ml_fundamentals/examples/regression_baseline.py
python practical_ml_fundamentals/examples/sklearn_pipeline_workflow.py
python practical_ml_fundamentals/examples/model_selection_cv.py
python practical_ml_fundamentals/examples/error_analysis_template.py
```

サンプルは小さな CSV と scikit-learn の基本機能だけで動くようにしています。大規模学習、GPU、外部 API、クラウド設定はこのディレクトリの範囲外です。

## 共通方針

- まずベースラインを作る。
- 評価指標は業務上の損失から選ぶ。
- validation の数字だけでなく、失敗例を必ず見る。
- 学習時と推論時の前処理を分けない。
- モデル変更より先に、データ・ラベル・分割・指標の欠陥を疑う。
