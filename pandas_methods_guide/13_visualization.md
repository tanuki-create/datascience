# 13. 可視化

pandasの可視化は、探索的データ分析で素早く傾向を見るために使います。最終成果物のデザインより、確認速度に強みがあります。

## `plot()`

- 基本の説明: 折れ線、棒、散布図などを簡単に描画します。
- 実用での使用場面: 売上推移、カテゴリ比較、簡易レポートの確認に使います。
- 基本構文:

```python
df.plot(kind="line", x=None, y=None, title=None, figsize=None)
series.plot(kind="line", title=None)
```

- 主な引数/指定:
  - `kind`: `"line"`, `"bar"`, `"barh"`, `"hist"`, `"box"`, `"scatter"`, `"area"`, `"pie"` などを指定します。
  - `x`, `y`: `DataFrame` で横軸・縦軸に使う列を指定します。
  - `title`: グラフタイトルを指定します。
  - `figsize`: 図の大きさを `(幅, 高さ)` のタプルで指定します。
  - `grid`: 目盛り線を表示するかを指定します。
  - `ax`: 既存のMatplotlib軸に描画する場合に指定します。
- 使用例:

```python
daily = pd.Series([100, 120, 90], index=pd.date_range("2026-01-01", periods=3))
daily.plot(title="Daily sales")
```

- 戻り値: Matplotlibの `Axes` オブジェクトを返します。さらにラベル、凡例、保存処理を追加できます。
- インパクト: 集計結果をすぐ視覚確認できます。数表だけでは見えにくいトレンドや急変を発見できます。
- よくある注意点:
  - pandasの可視化は内部的にMatplotlibを使います。表示されない環境では `import matplotlib.pyplot as plt` 後に `plt.show()` が必要なことがあります。
  - `kind="scatter"` では `x` と `y` の指定が必須です。
  - カテゴリが多すぎる棒グラフは読みにくくなります。上位N件に絞る、横棒にするなどの工夫が必要です。
  - 最終報告用の細かい体裁調整は、Matplotlibやseabornへ移すと管理しやすくなります。
- 関連メソッド: `hist()`, `boxplot()`, `groupby()`, `resample()`, `value_counts()`

## `hist()`

- 基本の説明: ヒストグラムを描画します。
- 実用での使用場面: 売上、単価、年齢、処理時間などの分布を見るときに使います。
- 基本構文:

```python
df.hist(column=None, bins=10, by=None, figsize=None)
series.hist(bins=10)
```

- 主な引数/指定:
  - `column`: 描画する数値列を指定します。
  - `bins`: 階級の数を指定します。細かさの調整に使います。
  - `by`: グループ別にヒストグラムを分けて描きます。
  - `figsize`: 図の大きさを指定します。
  - `range`: 集計対象にする値の範囲を指定します。
- 使用例:

```python
sales["price"].hist(bins=10)
```

- 戻り値: `Series.hist()` はMatplotlibの `Axes`、`DataFrame.hist()` は `Axes` 配列を返します。
- インパクト: 偏り、山の数、外れ値の存在を確認できます。平均値だけでは見えない分布の形を掴めます。
- よくある注意点:
  - 欠損値は自動的に除外されます。欠損の多さ自体は別途 `isna().sum()` で確認します。
  - `bins` が少なすぎると分布が粗く、多すぎるとノイズが目立ちます。複数の値で試すのが実務的です。
  - 極端な外れ値があると主要な分布が潰れて見えます。必要に応じて範囲指定や外れ値確認を行います。
- 関連メソッド: `plot(kind="hist")`, `describe()`, `value_counts()`, `boxplot()`

## `boxplot()`

- 基本の説明: 箱ひげ図を描画します。
- 実用での使用場面: 店舗別、カテゴリ別の分布差や外れ値を比較します。
- 基本構文:

```python
df.boxplot(column=None, by=None, figsize=None, grid=True)
```

- 主な引数/指定:
  - `column`: 箱ひげ図にする数値列を指定します。
  - `by`: グループ別に分布を比較する列を指定します。
  - `figsize`: 図の大きさを指定します。
  - `grid`: 目盛り線の表示有無を指定します。
  - `rot`: 軸ラベルの回転角度を指定します。
- 使用例:

```python
sales.boxplot(column="price", by="store")
```

- 戻り値: Matplotlibの `Axes`、または複数列の場合は `Axes` 配列を返します。
- インパクト: グループ間のばらつきや外れ値を一目で比較できます。
- よくある注意点:
  - 箱ひげ図の外れ値は統計的な目安であり、必ずしも異常データとは限りません。業務ルールと照合します。
  - グループ数が多い場合はラベルが重なります。対象を絞る、`rot` を指定する、図を大きくするなどが必要です。
  - 平均値ではなく中央値と四分位範囲を見る図です。平均比較が必要なら別途集計します。
- 関連メソッド: `hist()`, `describe()`, `groupby()`, `plot(kind="box")`

## `scatter_matrix()`

- 基本の説明: 複数の数値列同士の散布図行列を描きます。`pandas.plotting.scatter_matrix` として使います。
- 実用での使用場面: 数値特徴量同士の関係、相関、クラスタの兆候を探索します。
- 基本構文:

```python
from pandas.plotting import scatter_matrix

scatter_matrix(frame, alpha=0.5, figsize=None, diagonal="hist")
```

- 主な引数/指定:
  - `frame`: 数値列を含む `DataFrame` を指定します。
  - `alpha`: 点の透明度を指定します。重なりが多い場合に有効です。
  - `figsize`: 図全体の大きさを指定します。
  - `diagonal`: 対角線上に表示する図を `"hist"` または `"kde"` で指定します。
  - `range_padding`: 各軸の表示範囲に余白を加えます。
- 使用例:

```python
from pandas.plotting import scatter_matrix

features = pd.DataFrame({
    "sales": [100, 120, 90, 150],
    "orders": [10, 12, 8, 15],
    "price": [1000, 1000, 1125, 1000],
})

scatter_matrix(features)
```

- 戻り値: Matplotlibの `Axes` 配列を返します。
- インパクト: 複数変数の関係を一括で見られます。機械学習前の特徴量理解に役立ちます。
- よくある注意点:
  - 列数が多いと図が急激に大きくなります。まず重要な数値列に絞ります。
  - 欠損値や文字列列が混ざると期待どおり描けない場合があります。`select_dtypes("number")` で数値列だけにするのが安全です。
  - 相関がありそうに見えても因果関係を示すものではありません。必要に応じて `corr()` や業務知識で確認します。
- 関連メソッド: `plot(kind="scatter")`, `corr()`, `select_dtypes()`, `hist()`
