# 08. 時系列処理

時系列処理では、日付型への変換、期間の作成、周期別集計、前期比較、移動平均を扱います。

## `to_datetime()`

- 基本の説明: 文字列や数値を日時型に変換します。
- 基本構文: `pd.to_datetime(arg, errors="raise", format=None, dayfirst=False, utc=False)`
- 主な引数/指定:
  - `arg`: 変換したい文字列、リスト、Series、DataFrameなど。
  - `format`: 日付文字列の形式を明示します。例: `"%Y-%m-%d"`、`"%Y/%m/%d %H:%M:%S"`。
  - `errors`: 変換できない値の扱いです。`"raise"` は例外、`"coerce"` は `NaT`、`"ignore"` は元の値を返します。
  - `utc`: `True` にするとUTCのタイムゾーン付き日時に変換します。
- 戻り値: 入力に応じて `Timestamp`、`DatetimeIndex`、`Series` などを返します。変換できない日時は `NaT` になります。
- 実用での使用場面: CSVから読み込んだ日付列を、月別集計や期間フィルタに使える形へ変換します。
- 使用例:

```python
df = sales.copy()
df["date"] = pd.to_datetime(df["date"])
df["date_strict"] = pd.to_datetime(df["date_text"], format="%Y-%m-%d", errors="coerce")
```

- インパクト: 日付比較、月次集計、時系列可視化が正しく行えます。文字列のままだと並び順や抽出が誤ることがあります。
- よくある注意点:
  - `errors="coerce"` を使うと不正な値を処理しやすくなりますが、欠損に変わるため後で `isna()` で確認します。
  - `format` を指定すると高速かつ解釈ミスを減らせます。`01/02/2026` のような表記は月日と日月の解釈に注意します。
  - 日時列を作っただけでは `resample()` の基準になりません。必要に応じて `set_index()` します。
- 関連メソッド: `Series.dt`、`set_index()`、`date_range()`、`to_timedelta()`

## `date_range()`

- 基本の説明: 指定した開始日・終了日・頻度で日時の連続範囲を作ります。
- 基本構文: `pd.date_range(start=None, end=None, periods=None, freq=None, tz=None)`
- 主な引数/指定:
  - `start`: 開始日時。
  - `end`: 終了日時。
  - `periods`: 生成する件数。`start` と `periods`、または `end` と `periods` の組み合わせでも使えます。
  - `freq`: 頻度。`"D"` は日次、`"W"` は週次、`"MS"` は月初、`"ME"` は月末、`"h"` は時間単位です。
  - `tz`: タイムゾーンを指定します。例: `"Asia/Tokyo"`。
- 戻り値: `DatetimeIndex` を返します。
- 実用での使用場面: 欠けている日付を補完する、カレンダーマスタを作る、将来予測用の日付を作るときに使います。
- 使用例:

```python
calendar = pd.date_range(start="2026-01-01", end="2026-01-07", freq="D")
month_starts = pd.date_range(start="2026-01-01", periods=6, freq="MS")
```

- インパクト: 日付の抜け漏れを明示できます。時系列分析で「データがない日」と「値が0の日」を区別しやすくなります。
- よくある注意点:
  - `start`、`end`、`periods` のうち通常は2つ以上を指定します。
  - `freq` を省略すると日次になりますが、意図が伝わるよう明示する方が安全です。
  - 月次は月初と月末で指定が異なります。月初は `"MS"`、月末は `"ME"` を使います。
- 関連メソッド: `period_range()`、`timedelta_range()`、`reindex()`、`asfreq()`

## `resample()`

- 基本の説明: 日時インデックスを基準に、日次、月次、週次などの頻度で集計・変換します。
- 基本構文: `df.resample(rule).agg_func()`、`series.resample(rule).agg_func()`
- 主な引数/指定:
  - `rule`: 変換後の頻度。例: `"D"`、`"W"`、`"MS"`、`"ME"`、`"h"`。
  - `on`: DataFrameの日時列を、インデックスにせず基準列として使います。
  - `closed`: 区間のどちら側を含めるかを指定します。`"left"` または `"right"`。
  - `label`: 集計結果のラベルを区間の左端・右端のどちらにするかを指定します。
- 戻り値: `DatetimeIndexResampler` などのResamplerオブジェクトです。`sum()`、`mean()`、`agg()` などを続けて結果にします。
- 実用での使用場面: 日次売上を月次にする、分単位ログを時間単位にする、株価を週次にする場面で使います。
- 使用例:

```python
df = sales.dropna(subset=["quantity"]).copy()
df["date"] = pd.to_datetime(df["date"])
df["amount"] = df["quantity"] * df["price"]

daily = df.set_index("date").resample("D")["amount"].sum()
monthly = df.resample("MS", on="date").agg(
    amount=("amount", "sum"),
    orders=("order_id", "nunique"),
)
```

- インパクト: 粒度の違う時系列を比較しやすくなります。日付インデックスが必要な点に注意します。
- よくある注意点:
  - `resample()` は日時型のインデックス、または `on` で指定した日時列が必要です。
  - 欠けた期間は集計方法によって0や欠損に見えます。売上のように「取引なし=0」と扱う場合は `fillna(0)` などを検討します。
  - 月次・週次の区切りは業務定義とずれやすいため、`rule`、`closed`、`label` を明示します。
- 関連メソッド: `groupby()`、`Grouper()`、`asfreq()`、`rolling()`

## `shift()`

- 基本の説明: 値を前後にずらします。
- 基本構文: `series.shift(periods=1, freq=None, fill_value=None)`、`df.shift(periods=1, axis=0)`
- 主な引数/指定:
  - `periods`: ずらす行数。正の値は下方向、負の値は上方向にずらします。
  - `freq`: 日時インデックスそのものを指定頻度でずらします。値の位置だけをずらす通常の `shift()` とは挙動が異なります。
  - `fill_value`: ずらして空いた位置に入れる値を指定します。
  - `axis`: DataFrameで行方向・列方向のどちらにずらすかを指定します。
- 戻り値: 元と同じ型のSeriesまたはDataFrameを返します。空いた位置は通常 `NaN` または `NaT` になります。
- 実用での使用場面: 前日比、前月比、ラグ特徴量、前回購入との差分を作ります。
- 使用例:

```python
daily = pd.Series([100, 120, 90], index=pd.date_range("2026-01-01", periods=3))
growth = daily / daily.shift(1) - 1
previous_day = daily.shift(1)
next_day = daily.shift(-1)
```

- インパクト: 時系列の変化率や差分を簡単に作れます。予測モデルの特徴量作成でも重要です。
- よくある注意点:
  - 先頭や末尾に欠損が発生します。変化率を作った後は欠損行をどう扱うか決めます。
  - グループごとの前期比較では、全体に `shift()` せず `groupby(...).shift()` を使います。
  - `freq` を指定すると値の並びではなくインデックスの日時が動くため、前期値作成とは目的が違います。
- 関連メソッド: `diff()`、`pct_change()`、`groupby().shift()`、`lag`特徴量作成

## `rolling()`

- 基本の説明: 一定幅の移動窓を作り、その範囲で集計します。
- 基本構文: `series.rolling(window, min_periods=None, center=False).agg_func()`
- 主な引数/指定:
  - `window`: 窓の大きさ。行数の `3`、時間幅の `"7D"` などを指定できます。
  - `min_periods`: 計算に必要な最小データ数。初期行にも値を出したい場合に調整します。
  - `center`: `True` にすると窓の結果ラベルを中央に置きます。
  - `closed`: 時間幅の窓で、端点を含める範囲を指定します。
- 戻り値: `Rolling` オブジェクトです。`mean()`、`sum()`、`std()`、`agg()` などを続けて計算します。
- 実用での使用場面: 7日移動平均、直近3回平均、移動標準偏差でトレンドや異常を見ます。
- 使用例:

```python
daily = pd.Series([100, 120, 90, 150, 130])
moving_avg = daily.rolling(window=3).mean()
moving_sum = daily.rolling(window=3, min_periods=1).sum()
```

- インパクト: 短期的なノイズをならし、傾向を見やすくします。詳細は [Window関数](./12_window_functions.md) でも扱います。
- よくある注意点:
  - デフォルトでは `window` 分の件数がそろうまで結果は `NaN` になります。
  - 時間幅の窓を使う場合は日時インデックス、または `on` の日時列が必要です。
  - 移動平均は遅れて反応するため、急な変化や異常値の検知では窓幅の選び方が重要です。
- 関連メソッド: `expanding()`、`ewm()`、`resample()`、`mean()`、`std()`
