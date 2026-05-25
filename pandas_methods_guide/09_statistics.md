# 09. 統計量

統計量は、データの中心、ばらつき、範囲、件数を把握するための基本です。単純ですが、品質確認と意思決定の出発点になります。

## `mean()`

- 基本の説明: 平均値を計算します。
- 基本構文: `series.mean(skipna=True)`、`df.mean(axis=0, numeric_only=False)`
- 主な引数/指定:
  - `skipna`: `True` の場合、欠損値を除外して計算します。
  - `axis`: DataFrameで列ごとに計算するか、行ごとに計算するかを指定します。
  - `numeric_only`: 数値列だけを対象にするかを指定します。
- 戻り値: Seriesではスカラー、DataFrameでは列または行ごとのSeriesを返します。
- 実用での使用場面: 平均売上、平均単価、平均処理時間を確認します。
- 使用例:

```python
avg_price = sales["price"].mean()
avg_by_store = sales.groupby("store")["price"].mean()
```

- インパクト: 代表値を素早く把握できます。外れ値に引っ張られやすい点に注意します。
- よくある注意点:
  - 外れ値が大きい列では、平均だけで判断せず `median()` や分位点も確認します。
  - 欠損はデフォルトで除外されます。欠損を0として扱う業務定義なら、事前に `fillna(0)` します。
  - カテゴリ列を含むDataFrameでは、対象列を明示すると意図しない集計を避けられます。
- 関連メソッド: `median()`、`describe()`、`groupby().mean()`、`rolling().mean()`

## `median()`

- 基本の説明: 中央値を計算します。
- 基本構文: `series.median(skipna=True)`、`df.median(axis=0, numeric_only=False)`
- 主な引数/指定:
  - `skipna`: 欠損値を除外するかを指定します。
  - `axis`: DataFrameで集計方向を指定します。
  - `numeric_only`: 数値列だけを対象にするかを指定します。
- 戻り値: Seriesではスカラー、DataFrameではSeriesを返します。
- 実用での使用場面: 所得、注文金額、処理時間など外れ値が大きいデータで使います。
- 使用例:

```python
median_price = sales["price"].median()
median_by_category = sales.groupby("category")["price"].median()
```

- インパクト: 外れ値に強い代表値を得られます。現場感に近い「普通の値」を見るときに有効です。
- よくある注意点:
  - 偶数件の場合は中央2値の平均になります。
  - 分布の偏りが大きい場合、平均と中央値の差を見ると偏りを把握しやすくなります。
  - カテゴリごとの典型値を見る場合は `groupby()` と組み合わせます。
- 関連メソッド: `mean()`、`quantile()`、`describe()`、`groupby().median()`

## `mode()`

- 基本の説明: 最頻値を返します。
- 基本構文: `series.mode(dropna=True)`、`df.mode(axis=0, dropna=True)`
- 主な引数/指定:
  - `dropna`: 欠損値を最頻値の候補から除外するかを指定します。
  - `axis`: DataFrameで列方向・行方向のどちらに計算するかを指定します。
- 戻り値: Seriesを返します。最頻値が複数ある場合は複数行になります。
- 実用での使用場面: よく売れるカテゴリ、最頻出ステータス、代表的な地域を確認します。
- 使用例:

```python
most_common_store = sales["store"].mode()
first_mode = sales["store"].mode().iloc[0]
```

- インパクト: カテゴリデータの偏りを把握できます。複数の最頻値が返ることがあります。
- よくある注意点:
  - 戻り値は常にSeriesとして扱うのが安全です。単一値が必要なら `.iloc[0]` などで取り出します。
  - 同率1位が複数ある場合、どれを代表値にするかは業務ルールで決めます。
  - 欠損の多さ自体を確認したい場合は、`dropna=False` も検討します。
- 関連メソッド: `value_counts()`、`idxmax()`、`groupby().agg()`、`describe()`

## `std()`

- 基本の説明: 標準偏差を計算します。
- 基本構文: `series.std(skipna=True, ddof=1)`、`df.std(axis=0, skipna=True, ddof=1)`
- 主な引数/指定:
  - `skipna`: 欠損値を除外するかを指定します。
  - `ddof`: 自由度の補正です。pandasのデフォルトは `1` で、標本標準偏差です。
  - `axis`: DataFrameで集計方向を指定します。
- 戻り値: Seriesではスカラー、DataFrameではSeriesを返します。
- 実用での使用場面: 売上や処理時間のばらつき、品質指標の安定性を確認します。
- 使用例:

```python
price_std = sales["price"].std()
price_std_population = sales["price"].std(ddof=0)
```

- インパクト: 平均だけでは見えない不安定さを把握できます。異常検知や品質管理で重要です。
- よくある注意点:
  - NumPyの `std()` はデフォルト `ddof=0`、pandasは `ddof=1` です。比較時に差が出ます。
  - 単位は元データと同じなので、ばらつきを説明しやすい指標です。
  - 外れ値の影響を受けるため、箱ひげ図や分位点と併用します。
- 関連メソッド: `var()`、`sem()`、`rolling().std()`、`describe()`

## `var()`

- 基本の説明: 分散を計算します。標準偏差の二乗に相当します。
- 基本構文: `series.var(skipna=True, ddof=1)`、`df.var(axis=0, skipna=True, ddof=1)`
- 主な引数/指定:
  - `skipna`: 欠損値を除外するかを指定します。
  - `ddof`: 自由度の補正です。標本分散では `1`、母分散では `0` を使います。
  - `axis`: DataFrameで集計方向を指定します。
- 戻り値: Seriesではスカラー、DataFrameではSeriesを返します。
- 実用での使用場面: 統計モデル、分散分析、ばらつきの理論的評価で使います。
- 使用例:

```python
price_var = sales["price"].var()
price_var_population = sales["price"].var(ddof=0)
```

- インパクト: ばらつきの大きさを数値化できます。単位が二乗になるため、説明では `std()` の方が直感的なことが多いです。
- よくある注意点:
  - 標準偏差と同じく、pandasのデフォルトは標本分散です。
  - 単位が二乗になるため、業務説明ではそのまま使いにくい場合があります。
  - ばらつきの比較では平均値の規模差も考慮します。
- 関連メソッド: `std()`、`cov()`、`corr()`、`rolling().var()`

## `min()`

- 基本の説明: 最小値を返します。
- 基本構文: `series.min(skipna=True)`、`df.min(axis=0, skipna=True)`
- 主な引数/指定:
  - `skipna`: 欠損値を除外するかを指定します。
  - `axis`: DataFrameで列ごと・行ごとのどちらに計算するかを指定します。
  - `numeric_only`: DataFrameで数値列だけを対象にするかを指定できます。
- 戻り値: Seriesではスカラー、DataFrameではSeriesを返します。日時列では最古日時、文字列では辞書順の最小値になります。
- 実用での使用場面: 最低売上、最短処理時間、最古日付を確認します。
- 使用例:

```python
min_price = sales["price"].min()
oldest_date = sales["date"].min()
```

- インパクト: 範囲チェックや異常値確認に役立ちます。
- よくある注意点:
  - 欠損はデフォルトで無視されます。全て欠損の列では結果も欠損になります。
  - 最小値の行を知りたい場合は `idxmin()` と組み合わせます。
  - 文字列列にも使えますが、意味のある大小かを確認します。
- 関連メソッド: `max()`、`idxmin()`、`nsmallest()`、`describe()`

## `max()`

- 基本の説明: 最大値を返します。
- 基本構文: `series.max(skipna=True)`、`df.max(axis=0, skipna=True)`
- 主な引数/指定:
  - `skipna`: 欠損値を除外するかを指定します。
  - `axis`: DataFrameで集計方向を指定します。
  - `numeric_only`: DataFrameで数値列だけを対象にするかを指定できます。
- 戻り値: Seriesではスカラー、DataFrameではSeriesを返します。日時列では最新日時、文字列では辞書順の最大値になります。
- 実用での使用場面: 最高売上、最大注文数、最新日付を確認します。
- 使用例:

```python
max_price = sales["price"].max()
latest_date = sales["date"].max()
```

- インパクト: 上限値や突出値を確認できます。桁違いの入力ミス発見にも使えます。
- よくある注意点:
  - 最大値の行を知りたい場合は `idxmax()` を使います。
  - 上限値が業務ルールを超えている場合は、入力ミス・単位違い・重複を疑います。
  - 文字列の最大値は辞書順であり、業務上の優先順位とは限りません。
- 関連メソッド: `min()`、`idxmax()`、`nlargest()`、`describe()`

## `count()`

- 基本の説明: 欠損値を除いた件数を数えます。
- 基本構文: `series.count()`、`df.count(axis=0)`
- 主な引数/指定:
  - `axis`: DataFrameで列ごと・行ごとのどちらに数えるかを指定します。
  - グループ別件数では `groupby(...).count()` を使います。
- 戻り値: Seriesでは整数、DataFrameでは列または行ごとのSeriesを返します。
- 実用での使用場面: 有効データ数、列ごとの欠損状況、グループ別件数を確認します。
- 使用例:

```python
valid_quantity_count = sales["quantity"].count()
count_by_store = sales.groupby("store")["quantity"].count()
non_null_by_column = sales.count()
```

- インパクト: 欠損を除いた実データ数を把握できます。全行数を見る `len()` や `shape[0]` とは意味が違います。
- よくある注意点:
  - `count()` は欠損を数えません。全行数は `len(df)` または `df.shape[0]` で確認します。
  - グループ別の行数を数えるだけなら、欠損の影響を受けにくい `groupby().size()` も有効です。
  - 欠損数を見たい場合は `isna().sum()` を使います。
- 関連メソッド: `size()`、`value_counts()`、`isna().sum()`、`nunique()`
