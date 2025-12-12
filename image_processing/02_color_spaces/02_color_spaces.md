# 色空間変換

様々な色空間への変換とその応用を学びます。

## 目次

1. [色空間とは](#色空間とは)
2. [RGB色空間](#rgb色空間)
3. [HSV色空間](#hsv色空間)
4. [LAB色空間](#lab色空間)
5. [YUV色空間](#yuv色空間)
6. [グレースケール変換](#グレースケール変換)
7. [色空間変換の実用例](#色空間変換の実用例)

---

## 色空間とは

### 色空間の定義

色空間（Color Space）は、色を数値で表現するための座標系です。異なる色空間は、異なる目的や用途に適しています。

### 主な色空間

1. **RGB**: 赤、緑、青の加法混色
2. **HSV**: 色相、彩度、明度
3. **LAB**: 知覚的に均一な色空間
4. **YUV**: 輝度と色差信号

---

## RGB色空間

### RGBの特徴

- **R (Red)**: 0-255の赤成分
- **G (Green)**: 0-255の緑成分
- **B (Blue)**: 0-255の青成分

### RGBの用途

- ディスプレイ表示
- 画像の基本表現
- デジタルカメラの標準形式

### RGBの制限

- 明度と色相が混在
- 知覚的に均一ではない
- 色調整が直感的でない

---

## HSV色空間

### HSVの特徴

- **H (Hue)**: 0-360度の色相
- **S (Saturation)**: 0-100%の彩度
- **V (Value)**: 0-100%の明度

### HSVの利点

- 色調整が直感的
- 明度と色相が分離
- 肌色検出などに適している

### HSVへの変換

```python
import cv2

# RGBからHSVへ
hsv = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)

# HSVからRGBへ
rgb = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
```

---

## LAB色空間

### LABの特徴

- **L (Lightness)**: 0-100の明度
- **A**: -128から+127の緑-赤軸
- **B**: -128から+127の青-黄軸

### LABの利点

- 知覚的に均一
- 色差計算に適している
- 画像処理アルゴリズムに適している

### LABへの変換

```python
import cv2

# RGBからLABへ
lab = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2LAB)

# LABからRGBへ
rgb = cv2.cvtColor(lab_img, cv2.COLOR_LAB2RGB)
```

---

## YUV色空間

### YUVの特徴

- **Y**: 輝度信号（0-255）
- **U**: 青-黄の色差信号
- **V**: 赤-緑の色差信号

### YUVの用途

- テレビ放送
- 動画圧縮（MPEG、H.264）
- 効率的な色情報圧縮

---

## グレースケール変換

### 変換手法

1. **平均法**: `(R + G + B) / 3`
2. **加重平均法**: `0.299*R + 0.587*G + 0.114*B`（ITU-R BT.601）
3. **最大値法**: `max(R, G, B)`
4. **最小値法**: `min(R, G, B)`
5. **輝度法**: YUVのY成分を使用

### 実装例

```python
from PIL import Image
import numpy as np

# 平均法
gray_avg = np.mean(img, axis=2).astype(np.uint8)

# 加重平均法
gray_weighted = (0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]).astype(np.uint8)

# PILでの変換
gray_pil = Image.fromarray(img).convert('L')
```

---

## 色空間変換の実用例

### 1. 肌色検出

HSV色空間を使用して肌色を検出：

```python
import cv2
import numpy as np

# HSVに変換
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# 肌色の範囲を定義
lower_skin = np.array([0, 20, 70])
upper_skin = np.array([20, 255, 255])

# マスクの作成
mask = cv2.inRange(hsv, lower_skin, upper_skin)
```

### 2. 背景除去

HSV色空間を使用して特定の色の背景を除去：

```python
# 緑色の背景を除去
lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

mask = cv2.inRange(hsv, lower_green, upper_green)
result = cv2.bitwise_and(img, img, mask=~mask)
```

### 3. 色補正

LAB色空間を使用して色補正：

```python
# LABに変換
lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

# Lチャンネル（明度）を調整
lab[:,:,0] = np.clip(lab[:,:,0] * 1.2, 0, 100)

# RGBに戻す
corrected = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
```

---

## ベストプラクティス

1. **用途に応じた選択**: 目的に応じて適切な色空間を選択
2. **変換の順序**: 複数回変換する場合は注意
3. **データ型**: 変換後のデータ型に注意（uint8、float32など）
4. **値の範囲**: 各色空間の値の範囲を理解する

---

## 次のステップ

色空間変換を習得したら、次は以下を学習します：

1. **フィルタリング**: 画像の平滑化やエッジ検出
2. **幾何変換**: 回転、リサイズ、アフィン変換
3. **閾値処理**: 画像の二値化

---

**参考資料**:
- OpenCV公式ドキュメント: https://docs.opencv.org/
- scikit-image公式ドキュメント: https://scikit-image.org/

