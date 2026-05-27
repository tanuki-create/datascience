# Sources and Reference Map

このファイルは、実践ML基礎テキストの参照元と対応関係を管理するための台帳です。本文は PDF の翻訳や長文要約ではなく、オリジナルの実務教材として作成します。

## Primary Book Reference

- Sergios Theodoridis, *Machine Learning: From the Classics to Deep Networks, Transformers, and Diffusion Models*, Third Edition, Elsevier, 2026.
  - Local private reference: `../mlpdf/machine-learning-from-the-classics-to-deep-networks-transformers-and-diffusion-models-3.pdf`
  - 参照方針: 章立て、概念確認、学習範囲の確認に利用。本文の翻訳、図表、演習、長文引用は行わない。

## PDF対応表

| 本ガイド | 主な対応章 |
|---|---|
| 00 Core message | Ch.1 Introduction |
| 01 Problem framing | Ch.1, Ch.3 |
| 02 Data, probability, uncertainty | Ch.2 |
| 03 Regression and classification | Ch.3, Ch.6, Ch.7 |
| 04 Loss, optimization, SGD | Ch.5, Ch.8, Ch.18 |
| 05 Generalization and validation | Ch.3, Ch.8, Ch.18 |
| 06 Classical models | Ch.7, Ch.11 |
| 07 Feature engineering and pipelines | Ch.3, Ch.6, Ch.8 |
| 08 Bayesian, EM, latent variables | Ch.12, Ch.13 |
| 09 Dimensionality reduction | Ch.20 |
| 10 Neural networks and deep learning | Ch.18 |
| 11 Transformers and self-supervised learning | Ch.19 |
| 12 Generative and diffusion models | Ch.19 |
| 13 Evaluation and MLOps | Ch.3, Ch.5, Ch.7, Ch.18 |
| 14 Capstone | Cross-chapter synthesis |
| 15 Quick reference | Cross-chapter synthesis |

## Official Documentation

- scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- scikit-learn model evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn Pipeline: https://scikit-learn.org/stable/modules/compose.html
- pandas documentation: https://pandas.pydata.org/docs/
- PyTorch documentation: https://pytorch.org/docs/stable/index.html
- TensorFlow documentation: https://www.tensorflow.org/guide

## Foundational Papers and Concepts

- Vaswani et al., "Attention Is All You Need", 2017.
- Ho et al., "Denoising Diffusion Probabilistic Models", 2020.
- Kingma and Welling, "Auto-Encoding Variational Bayes", 2013.
- Goodfellow et al., "Generative Adversarial Nets", 2014.
- Breiman, "Random Forests", 2001.
- Cortes and Vapnik, "Support-vector networks", 1995.

## Adjacent Repo References

- [pandas_methods_guide/](../pandas_methods_guide/)
- [ml_research_practice/](../ml_research_practice/)
- [object_detection/](../object_detection/)
- [vector_search_cs_foundations/](../vector_search_cs_foundations/)
- [system_design/16_ml_ai_systems/](../system_design/16_ml_ai_systems/)

## Reuse Notes

- 利用目的は私的・非商用・ローカル学習用。
- 公開配布する場合は、引用、翻案、再配布の観点で再レビューする。
- PDF からの長文引用、図表、演習の流用は行わない。
