# 12. Window関数

Window関数は「直近N件」や「開始から現在まで」の範囲を使って計算します。時系列、品質管理、異常検知、特徴量作成でよく使います。

## `rolling()`

- 基本の説明: 固定幅の移動窓を作ります。そこに `mean()`、`sum()`、`std()` などを続けて計算します。
- 基本構文: `series.rolling(window, min_periods=None, center=False).agg_func()`
- 主な引数/指定:
  - `window`: 窓の大きさ。行数なら `3`、時間幅なら `"7D"` のように指定します。
  - `min_periods`: 計算に必要な最小データ数です。`1` にすると窓が埋まる前から値を返します。
  - `center`: `True` にすると結果ラベルを窓の中央に置きます。
  - `on`: DataFrameで日時列を基準に時間幅の窓を使う場合に指定します。
  - `closed`: 時間幅の窓で、左右端を含めるかを指定します。
- 戻り値: `Rolling` オブジェクトを返します。`mean()`、`sum()`、`std()`、`min()`、`max()`、`agg()` などを続けて計算します。
- 実用での使用場面: 7日移動平均、直近3回の合計、移動標準偏差による異常検知に使います。
- 使用例:

```python
daily_sales = pd.Series(
    [100, 120, 90, 150, 130, 160, 170],
    index=pd.date_range("2026-01-01", periods=7),
)

rolling_mean = daily_sales.rolling(window=3).mean()
rolling_std = daily_sales.rolling(window=3).std()
rolling_sum_from_start = daily_sales.rolling(window=3, min_periods=1).sum()
```

- インパクト: ノイズをならしてトレンドを把握できます。`window` が大きいほど滑らかになりますが、変化への反応は遅くなります。
- よくある注意点:
  - デフォルトでは窓の件数がそろうまで `NaN` になります。初期値も出したい場合は `min_periods` を調整します。
  - 行数ベースの `window=7` と時間ベースの `window="7D"` は意味が違います。欠測日のある時系列では特に差が出ます。
  - グループごとの移動平均は、全体に `rolling()` せず `groupby(...).rolling()` を使います。
  - `center=True` は見た目のラベル位置を変えるため、予測特徴量では未来情報を混ぜないよう注意します。
- 関連メソッド: `expanding()`、`ewm()`、`resample()`、`shift()`、`agg()`

## `expanding()`

- 基本の説明: 先頭から現在行までの累積窓を作ります。
- 基本構文: `series.expanding(min_periods=1).agg_func()`
- 主な引数/指定:
  - `min_periods`: 計算に必要な最小データ数です。デフォルトは `1` です。
  - DataFrameでも使え、列ごとに累積集計できます。
- 戻り値: `Expanding` オブジェクトを返します。`mean()`、`sum()`、`min()`、`max()`、`std()`、`agg()` などを続けて計算します。
- 実用での使用場面: 累積平均、累積最大、学習曲線、開始以来のパフォーマンス推移を見ます。
- 使用例:

```python
daily_sales = pd.Series([100, 120, 90, 150])
cumulative_avg = daily_sales.expanding().mean()
cumulative_max = daily_sales.expanding().max()
```

- インパクト: 時点ごとの累積的な変化を把握できます。移動平均とは違い、過去データ全体の影響を持ち続けます。
- よくある注意点:
  - 過去全体を使うため、古いデータの影響が残り続けます。最近の変化を重視するなら `rolling()` や `ewm()` を検討します。
  - `cumsum()` や `cummax()` のような累積専用メソッドで足りる場合は、そちらの方が簡潔です。
  - グループ別に累積窓を作る場合は `groupby(...).expanding()` を使います。
- 関連メソッド: `rolling()`、`ewm()`、`cumsum()`、`cummax()`、`cummin()`
