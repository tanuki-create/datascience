# 画像処理の基礎

画像処理の基本概念と、Pythonで画像を扱うための基礎知識を学びます。

## 目次

1. [画像とは何か](#画像とは何か)
2. [画像のデータ構造](#画像のデータ構造)
3. [画像の読み込み](#画像の読み込み)
4. [画像の表示](#画像の表示)
5. [画像の保存](#画像の保存)
6. [NumPy配列としての画像](#numpy配列としての画像)
7. [ピクセル操作](#ピクセル操作)
8. [画像の基本統計](#画像の基本統計)

---

## 画像とは何か

### デジタル画像の定義

デジタル画像は、**画素（ピクセル）**の集合として表現されます。各ピクセルは位置情報（x, y座標）と色情報（RGB値など）を持ちます。

### 画像の種類

1. **グレースケール画像**: 各ピクセルが1つの値（0-255）を持つ
2. **カラー画像**: 各ピクセルが3つの値（R, G, B）を持つ
3. **RGBA画像**: 透明度（Alpha）チャンネルを含むカラー画像

### 画像の解像度

- **解像度**: 画像の幅×高さ（例: 1920×1080）
- **アスペクト比**: 幅と高さの比率
- **DPI/PPI**: ドット/ピクセル密度（印刷や表示品質に関連）

---

## 画像のデータ構造

### NumPy配列としての画像

Pythonでは、画像は**NumPy配列**として表現されます：

```python
# グレースケール画像: shape = (height, width)
# カラー画像: shape = (height, width, channels)
# RGBA画像: shape = (height, width, 4)
```

### データ型

- **uint8**: 0-255の整数値（最も一般的）
- **uint16**: 0-65535の整数値（高精度画像）
- **float32/float64**: 0.0-1.0の浮動小数点数（正規化された画像）

### メモリサイズ

画像のメモリサイズは以下の式で計算できます：

```
メモリサイズ = height × width × channels × bytes_per_pixel
```

例: 1920×1080のRGB画像（uint8）
```
1920 × 1080 × 3 × 1 = 6,220,800 bytes ≈ 6 MB
```

---

## 画像の読み込み

### PIL/Pillow

```python
from PIL import Image

# 画像の読み込み
img = Image.open('image.jpg')

# 画像情報の取得
print(f"サイズ: {img.size}")  # (width, height)
print(f"モード: {img.mode}")  # RGB, L (グレースケール), RGBA
```

### OpenCV

```python
import cv2

# カラー画像の読み込み（BGR形式）
img = cv2.imread('image.jpg', cv2.IMREAD_COLOR)

# グレースケール画像の読み込み
img_gray = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
```

**注意**: OpenCVはBGR形式で画像を読み込むため、matplotlibで表示する際はRGBに変換が必要です。

### matplotlib

```python
import matplotlib.image as mpimg

# 画像の読み込み（RGB形式）
img = mpimg.imread('image.jpg')
```

---

## 画像の表示

### matplotlib

```python
import matplotlib.pyplot as plt

# 画像の表示
plt.imshow(img)
plt.axis('off')  # 軸を非表示
plt.show()
```

### OpenCV

```python
import cv2

# 画像の表示
cv2.imshow('Image', img)
cv2.waitKey(0)  # キー入力待ち
cv2.destroyAllWindows()
```

### PIL/Pillow

```python
from PIL import Image

# 画像の表示
img.show()
```

---

## 画像の保存

### PIL/Pillow

```python
from PIL import Image

# 画像の保存
img.save('output.jpg', quality=95)

# フォーマット指定
img.save('output.png', format='PNG')
```

### OpenCV

```python
import cv2

# 画像の保存
cv2.imwrite('output.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 95])
```

### matplotlib

```python
import matplotlib.pyplot as plt

plt.imshow(img)
plt.axis('off')
plt.savefig('output.png', bbox_inches='tight', dpi=300)
```

---

## NumPy配列としての画像

### 配列への変換

```python
import numpy as np
from PIL import Image

# PIL画像をNumPy配列に変換
img_array = np.array(img)

# 形状の確認
print(f"形状: {img_array.shape}")
print(f"データ型: {img_array.dtype}")
print(f"最小値: {img_array.min()}, 最大値: {img_array.max()}")
```

### 配列から画像への変換

```python
from PIL import Image

# NumPy配列からPIL画像へ
img = Image.fromarray(img_array)
```

---

## ピクセル操作

### ピクセル値へのアクセス

```python
# グレースケール画像
pixel_value = img[y, x]

# カラー画像
r, g, b = img[y, x]

# 特定のチャンネル
red_channel = img[:, :, 0]
```

### ピクセル値の変更

```python
# 単一ピクセルの変更
img[y, x] = 255

# 領域の変更
img[100:200, 100:200] = [255, 0, 0]  # 赤色で塗りつぶし

# 条件に基づく変更
img[img > 128] = 255
```

### 画像のコピー

```python
# 浅いコピー（参照）
img_copy = img

# 深いコピー（推奨）
img_copy = img.copy()
# または
img_copy = np.copy(img)
```

---

## 画像の基本統計

### 基本統計量

```python
import numpy as np

# 平均値
mean_value = np.mean(img)

# 標準偏差
std_value = np.std(img)

# 最小値・最大値
min_value = np.min(img)
max_value = np.max(img)

# 中央値
median_value = np.median(img)
```

### ヒストグラム

ヒストグラムは画像の輝度分布を表します：

```python
import matplotlib.pyplot as plt

# グレースケール画像のヒストグラム
hist, bins = np.histogram(img.flatten(), bins=256, range=(0, 256))

plt.hist(img.flatten(), bins=256, range=(0, 256))
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Image Histogram')
plt.show()
```

### チャンネル別統計

```python
# カラー画像の各チャンネル統計
for i, channel_name in enumerate(['Red', 'Green', 'Blue']):
    channel = img[:, :, i]
    print(f"{channel_name} Channel:")
    print(f"  平均: {np.mean(channel):.2f}")
    print(f"  標準偏差: {np.std(channel):.2f}")
    print(f"  最小値: {np.min(channel)}")
    print(f"  最大値: {np.max(channel)}")
```

---

## よくある操作

### 画像のリサイズ

```python
from PIL import Image

# リサイズ
img_resized = img.resize((new_width, new_height))

# アスペクト比を保ったリサイズ
img.thumbnail((max_width, max_height))
```

### 画像の回転

```python
# 90度回転
img_rotated = img.rotate(90)

# 任意の角度で回転
img_rotated = img.rotate(45, expand=True)
```

### 画像のクロップ

```python
# 領域の切り出し
img_cropped = img.crop((left, top, right, bottom))

# NumPy配列でのクロップ
img_cropped = img[y1:y2, x1:x2]
```

---

## ベストプラクティス

1. **メモリ管理**: 大きな画像を扱う際は、必要に応じてリサイズを検討
2. **データ型の統一**: 処理中はデータ型を統一（通常はuint8）
3. **コピーの使用**: 元の画像を保持したい場合は必ずコピーを作成
4. **エラーハンドリング**: 画像ファイルの存在確認と例外処理を実装
5. **パフォーマンス**: NumPyのベクトル化演算を活用

---

## 次のステップ

基礎編を習得したら、次は以下を学習します：

1. **色空間変換**: RGB以外の色空間への変換
2. **フィルタリング**: 画像の平滑化やエッジ検出
3. **幾何変換**: 回転、リサイズ、アフィン変換

---

**参考資料**:
- PIL/Pillow公式ドキュメント: https://pillow.readthedocs.io/
- OpenCV公式ドキュメント: https://docs.opencv.org/
- NumPy公式ドキュメント: https://numpy.org/doc/

