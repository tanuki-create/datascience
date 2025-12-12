# Python画像処理 完全ガイド

Pythonを使用した画像処理の基本から応用まで、理論と実装を段階的に学習できる包括的な教材です。

## 📚 教材の構成

### 1. 基礎編 (01_basics/)
画像処理の基本操作とNumPy配列としての画像の扱い方を学びます。

- **理論**: [画像処理の基礎](01_basics/01_image_processing_basics.md)
- **実装**:
  - [画像の読み込み・表示・保存](01_basics/notebooks/image_io.ipynb)
  - [NumPy配列としての画像操作](01_basics/notebooks/numpy_image_operations.ipynb)
  - [画像の基本情報と統計](01_basics/notebooks/image_statistics.ipynb)

**学習内容**:
- PIL/Pillow、OpenCV、matplotlibでの画像読み込み
- 画像の表示と保存
- NumPy配列としての画像データ構造
- ピクセル値へのアクセスと操作
- 画像の基本統計（平均、分散、ヒストグラム）

### 2. 色空間変換編 (02_color_spaces/)
様々な色空間への変換とその応用を学びます。

- **理論**: [色空間変換](02_color_spaces/02_color_spaces.md)
- **実装**:
  - [RGB、HSV、LAB変換](02_color_spaces/notebooks/color_space_conversion.ipynb)
  - [グレースケール変換](02_color_spaces/notebooks/grayscale_conversion.ipynb)
  - [色空間を使った画像処理](02_color_spaces/notebooks/color_space_applications.ipynb)

**学習内容**:
- RGB、HSV、LAB、YUV色空間
- グレースケール変換の各種手法
- 色空間変換の実用例（肌色検出、背景除去など）

### 3. フィルタリング編 (03_filtering/)
画像の平滑化、シャープ化、エッジ検出などのフィルタ処理を学びます。

- **理論**: [画像フィルタリング](03_filtering/03_filtering.md)
- **実装**:
  - [平滑化フィルタ（平均、ガウシアン、メディアン）](03_filtering/notebooks/smoothing_filters.ipynb)
  - [シャープ化フィルタ](03_filtering/notebooks/sharpen_filters.ipynb)
  - [エッジ検出（Sobel、Canny、Laplacian）](03_filtering/notebooks/edge_detection.ipynb)
  - [カスタムフィルタの作成](03_filtering/notebooks/custom_filters.ipynb)

**学習内容**:
- 畳み込み演算の原理
- 各種フィルタの特性と使い分け
- ノイズ除去への応用
- エッジ検出アルゴリズムの比較

### 4. 幾何変換編 (04_geometric_transforms/)
画像の回転、リサイズ、アフィン変換などの幾何変換を学びます。

- **理論**: [幾何変換](04_geometric_transforms/04_geometric_transforms.md)
- **実装**:
  - [リサイズとクロップ](04_geometric_transforms/notebooks/resize_crop.ipynb)
  - [回転と反転](04_geometric_transforms/notebooks/rotation_flip.ipynb)
  - [アフィン変換と射影変換](04_geometric_transforms/notebooks/affine_projective.ipynb)
  - [透視変換の実用例](04_geometric_transforms/notebooks/perspective_transform_applications.ipynb)

**学習内容**:
- 線形変換と非線形変換
- 補間手法（最近傍、双線形、双三次）
- 画像の歪み補正
- 実用例（文書スキャン、パノラマ合成など）

### 5. 閾値処理編 (05_thresholding/)
画像の二値化と閾値処理の各種手法を学びます。

- **理論**: [閾値処理](05_thresholding/05_thresholding.md)
- **実装**:
  - [単純閾値処理](05_thresholding/notebooks/simple_thresholding.ipynb)
  - [適応的閾値処理](05_thresholding/notebooks/adaptive_thresholding.ipynb)
  - [Otsu法による自動閾値決定](05_thresholding/notebooks/otsu_thresholding.ipynb)
  - [実用例（文書画像の二値化）](05_thresholding/notebooks/document_binarization.ipynb)

**学習内容**:
- グローバル閾値とローカル閾値
- ヒストグラム解析による閾値決定
- 実用例（OCR前処理、背景除去など）

### 6. モルフォロジー演算編 (06_morphology/)
モルフォロジー演算による画像の形状処理を学びます。

- **理論**: [モルフォロジー演算](06_morphology/06_morphology.md)
- **実装**:
  - [基本演算（エロージョン、ディレーション）](06_morphology/notebooks/basic_morphology.ipynb)
  - [複合演算（オープニング、クロージング）](06_morphology/notebooks/opening_closing.ipynb)
  - [実用例（ノイズ除去、形状抽出）](06_morphology/notebooks/morphology_applications.ipynb)

**学習内容**:
- 構造化要素の設計
- モルフォロジー演算の組み合わせ
- 実用例（文字認識、細胞画像解析など）

### 7. 特徴検出編 (07_feature_detection/)
コーナー検出、特徴点検出、特徴記述子を学びます。

- **理論**: [特徴検出](07_feature_detection/07_feature_detection.md)
- **実装**:
  - [コーナー検出（Harris、Shi-Tomasi）](07_feature_detection/notebooks/corner_detection.ipynb)
  - [特徴点検出（SIFT、ORB、AKAZE）](07_feature_detection/notebooks/feature_points.ipynb)
  - [特徴マッチング](07_feature_detection/notebooks/feature_matching.ipynb)
  - [実用例（画像マッチング、物体追跡）](07_feature_detection/notebooks/feature_matching_applications.ipynb)

**学習内容**:
- 特徴点検出アルゴリズムの比較
- 特徴記述子の生成とマッチング
- 実用例（画像検索、パノラマ合成など）

### 8. 画像セグメンテーション編 (08_segmentation/)
画像の領域分割手法を学びます。

- **理論**: [画像セグメンテーション](08_segmentation/08_segmentation.md)
- **実装**:
  - [閾値ベースセグメンテーション](08_segmentation/notebooks/threshold_segmentation.ipynb)
  - [領域成長法](08_segmentation/notebooks/region_growing.ipynb)
  - [Watershedアルゴリズム](08_segmentation/notebooks/watershed.ipynb)
  - [K-meansクラスタリングによるセグメンテーション](08_segmentation/notebooks/kmeans_segmentation.ipynb)
  - [実用例（物体抽出、背景分離）](08_segmentation/notebooks/segmentation_applications.ipynb)

**学習内容**:
- セグメンテーション手法の比較
- 実用例（医療画像解析、物体検出など）

### 9. 画像復元編 (09_image_restoration/)
ノイズ除去と画像復元手法を学びます。

- **理論**: [画像復元](09_image_restoration/09_image_restoration.md)
- **実装**:
  - [ノイズ除去（ガウシアン、ソルト&ペッパー）](09_image_restoration/notebooks/noise_removal.ipynb)
  - [非局所平均法（Non-local Means）](09_image_restoration/notebooks/non_local_means.ipynb)
  - [画像のぼけ除去](09_image_restoration/notebooks/deblurring.ipynb)
  - [実用例（古い写真の復元）](09_image_restoration/notebooks/photo_restoration.ipynb)

**学習内容**:
- 各種ノイズモデル
- 復元アルゴリズムの比較
- 実用例（古い写真の修復、医療画像の改善など）

### 10. 実用例編 (10_applications/)
実践的な画像処理アプリケーションを学びます。

- **理論**: [実用例のまとめ](10_applications/10_applications.md)
- **実装**:
  - [顔検出と認識](10_applications/notebooks/face_detection.ipynb)
  - [OCR（文字認識）](10_applications/notebooks/ocr.ipynb)
  - [画像分類の前処理](10_applications/notebooks/image_classification_preprocessing.ipynb)
  - [画像の品質向上（コントラスト調整、色補正）](10_applications/notebooks/image_enhancement.ipynb)
  - [物体検出の前処理](10_applications/notebooks/object_detection_preprocessing.ipynb)

**学習内容**:
- 実務でよく使われる画像処理パイプライン
- 機械学習との統合
- パフォーマンス最適化

### 11. 総まとめ (11_summary/)
画像処理のベストプラクティスと実践ガイドです。

- **総括**: [総まとめ](11_summary/11_comprehensive_summary.md)

**学習内容**:
- 画像処理のベストプラクティス
- 実践的なワークフロー
- よくある問題と解決策
- 次のステップ（深層学習への応用など）

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
- 実用例編を活用して実務に応用

## 💻 環境構築

### 必要なライブラリ

```bash
pip install numpy opencv-python pillow matplotlib scikit-image scipy jupyter
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
| 2. 色空間変換 | 20分 | 60分 | 1.3時間 |
| 3. フィルタリング | 45分 | 120分 | 2.75時間 |
| 4. 幾何変換 | 30分 | 90分 | 2時間 |
| 5. 閾値処理 | 25分 | 75分 | 1.75時間 |
| 6. モルフォロジー演算 | 20分 | 60分 | 1.3時間 |
| 7. 特徴検出 | 40分 | 120分 | 2.7時間 |
| 8. 画像セグメンテーション | 35分 | 105分 | 2.3時間 |
| 9. 画像復元 | 30分 | 90分 | 2時間 |
| 10. 実用例 | 45分 | 150分 | 3.25時間 |
| 11. 総まとめ | 30分 | - | 30分 |
| **合計** | **6.5時間** | **10.6時間** | **17.1時間** |

## 🎓 学習目標

### 基礎レベル
- [ ] 画像の読み込み、表示、保存ができる
- [ ] NumPy配列として画像を操作できる
- [ ] 基本的な色空間変換ができる
- [ ] 基本的なフィルタリングができる

### 中級レベル
- [ ] エッジ検出と特徴点検出を実装できる
- [ ] 画像セグメンテーションを実装できる
- [ ] 適切な前処理パイプラインを構築できる
- [ ] 実用例を理解し応用できる

### 上級レベル
- [ ] 画像復元アルゴリズムを実装できる
- [ ] 複雑な画像処理パイプラインを設計できる
- [ ] 機械学習との統合ができる
- [ ] パフォーマンス最適化ができる

## 🔍 実践的な応用例

各ノートブックには以下のような実践例が含まれています：

- **顔検出**: OpenCVを使った顔検出と認識
- **OCR**: 文書画像からの文字抽出
- **画像分類前処理**: 機械学習モデル用の画像前処理
- **画像品質向上**: コントラスト調整、色補正
- **物体検出前処理**: 物体検出モデル用の前処理

## 📝 演習問題

各ノートブックには演習問題が含まれています：
- 基礎的な実装問題
- 応用的な分析問題
- 実データでの検証問題

## 🚀 次のステップ

画像処理を習得した後は：
1. **深層学習**: CNNを使った画像分類
2. **物体検出**: YOLO、R-CNNなどの物体検出モデル
3. **画像生成**: GAN、VAEなどの生成モデル
4. **画像セグメンテーション**: U-Net、DeepLabなどのセマンティックセグメンテーション

## 📚 参考資料

### 書籍
- 「ディジタル画像処理」原島博
- 「OpenCVによる画像処理入門」北山洋幸
- 「Computer Vision: Algorithms and Applications」Richard Szeliski

### オンラインリソース
- OpenCV公式ドキュメント
- scikit-image公式ドキュメント
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

**最終更新**: 2025年1月

**Happy Learning! 📸🎉**

