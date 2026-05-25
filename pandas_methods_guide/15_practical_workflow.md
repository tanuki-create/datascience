# 15. 実務ワークフロー例

ここでは、画像にある主要メソッドを組み合わせた実務寄りの流れを示します。

## 目的

CSVで受け取った売上明細を読み込み、欠損を確認し、店舗別に集計し、月次推移を作り、結果を出力します。

## 全体の流れ

- 基本の考え方: 実務では「読み込み」「確認」「型変換」「欠損処理」「派生列作成」「集計」「時系列処理」「出力」の順に進めると、データ事故を発見しやすくなります。
- 基本構文:

```python
df = pd.read_csv("input.csv")
df = df.assign(new_col=...)
summary = df.groupby("key").agg(...)
summary.to_csv("output.csv", index=False)
```

- 主な引数/指定:
  - 読み込み時は `encoding`, `parse_dates`, `dtype` を必要に応じて指定します。
  - 集計時は `groupby()` のキー列と `agg()` の集計列・集計関数を明確にします。
  - 出力時は `index=False` を指定し、不要なインデックス列の混入を防ぎます。
- 戻り値: 各工程は基本的に新しい `DataFrame` や `Series` を返します。代入しながら処理を進めると、どの段階のデータか追いやすくなります。
- よくある注意点:
  - 読み込み直後の型や欠損を確認せずに集計へ進むと、数値が文字列扱いになったまま計算されるなどの事故が起きます。
  - 欠損をすべて削除すると、分析対象が大きく偏る場合があります。列ごとに削除・補完・保留を判断します。
  - 出力前に `shape` と主要指標の合計を確認し、中間処理で行が意図せず増減していないか見ます。
- 関連メソッド: `read_csv()`, `head()`, `info()`, `isna()`, `dropna()`, `fillna()`, `assign()`, `groupby()`, `agg()`, `resample()`, `rolling()`, `to_csv()`, `to_excel()`

## コード例

```python
import pandas as pd

# 1. 読み込み
df = pd.read_csv("sales.csv")

# 2. 確認
print(df.head())
print(df.shape)
print(df.dtypes)
df.info()

# 3. 型変換
df["date"] = pd.to_datetime(df["date"])

# 4. 欠損確認と補完
print(df.isna().sum())
df = df.dropna(subset=["date", "store", "price"])
df["quantity"] = df["quantity"].fillna(0)

# 5. 派生列
df = df.assign(amount=df["quantity"] * df["price"])

# 6. 店舗別集計
store_summary = (
    df.groupby("store")
    .agg(
        total_amount=("amount", "sum"),
        avg_price=("price", "mean"),
        row_count=("amount", "count"),
    )
    .reset_index()
    .sort_values("total_amount", ascending=False)
)

# 7. 月次集計
monthly = (
    df.set_index("date")
    .resample("ME")["amount"]
    .sum()
    .reset_index(name="monthly_amount")
)

# 8. 移動平均
monthly["rolling_3m"] = monthly["monthly_amount"].rolling(window=3).mean()

# 9. 出力
store_summary.to_csv("store_summary.csv", index=False)
try:
    monthly.to_excel("monthly_summary.xlsx", index=False)
except ModuleNotFoundError as exc:
    if exc.name != "openpyxl":
        raise
    monthly.to_csv("monthly_summary.csv", index=False)
```

## 各ステップの要点

### 1. 読み込み

- 基本構文:

```python
df = pd.read_csv("sales.csv", encoding="utf-8")
```

- 主な引数/指定: `encoding` で文字コード、`parse_dates` で日付列、`dtype` で列型、`usecols` で読み込む列を指定します。
- 戻り値: CSVの内容を持つ `DataFrame` です。
- よくある注意点: 日本語CSVは環境によって文字化けするため、`utf-8`, `utf-8-sig`, `cp932` を確認します。ID列は先頭ゼロ保持のため文字列型で読む場合があります。
- 関連メソッド: `read_excel()`, `read_json()`, `to_csv()`

### 2. 確認

- 基本構文:

```python
df.head()
df.shape
df.dtypes
df.info()
```

- 主な引数/指定: `head(n)` で表示行数、`info(show_counts=True)` で非欠損数の表示を調整できます。
- 戻り値: `head()` は先頭行の `DataFrame`、`shape` は `(行数, 列数)` のタプル、`dtypes` は列ごとの型、`info()` は概要を表示して通常 `None` を返します。
- よくある注意点: `info()` は表示系メソッドなので、結果を変数に入れて加工する用途には向きません。確認結果をもとに型変換や欠損処理の方針を決めます。
- 関連メソッド: `tail()`, `describe()`, `columns`, `isna()`

### 3. 型変換

- 基本構文:

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
```

- 主な引数/指定: `errors="coerce"` は変換できない値を欠損にします。`format` を指定すると日付解釈を固定できます。
- 戻り値: 変換後の `Series` です。列へ代入して `DataFrame` に反映します。
- よくある注意点: 日付や数値の変換に失敗した値は欠損になるため、変換後に `isna().sum()` で増加分を確認します。
- 関連メソッド: `astype()`, `to_datetime()`, `to_numeric()`, `dtypes`

### 4. 欠損処理

- 基本構文:

```python
df.isna().sum()
df = df.dropna(subset=["date", "store", "price"])
df["quantity"] = df["quantity"].fillna(0)
```

- 主な引数/指定: `dropna(subset=...)` で重要列だけを削除判定に使い、`fillna(value)` で補完値を指定します。
- 戻り値: `isna()` は真偽値の表、`sum()` は欠損数、`dropna()` と `fillna()` は処理後の `DataFrame` または `Series` を返します。
- よくある注意点: 目的変数や金額列の欠損をゼロ補完すると、実績がないのか不明なのかを混同する場合があります。補完理由をコメントや別列で残すと安全です。
- 関連メソッド: `notna()`, `interpolate()`, `duplicated()`, `describe()`

### 5. 派生列

- 基本構文:

```python
df = df.assign(amount=df["quantity"] * df["price"])
```

- 主な引数/指定: `assign(列名=式)` の形で、既存列を使った新しい列を追加します。ラムダ式を使うと同じ `assign()` 内の列を参照できます。
- 戻り値: 新しい列を追加した `DataFrame` です。
- よくある注意点: 既存列と同じ名前を指定すると上書きされます。金額計算では数量・単価の型と欠損処理が済んでいるか確認します。
- 関連メソッド: `eval()`, `rename()`, `drop()`, `astype()`

### 6. 店舗別集計

- 基本構文:

```python
summary = (
    df.groupby("store")
    .agg(total_amount=("amount", "sum"), avg_price=("price", "mean"))
    .reset_index()
)
```

- 主な引数/指定: `groupby("store")` で集計単位、`agg(新列名=(対象列, 集計関数))` で指標名と計算内容を指定します。
- 戻り値: グループごとの集計結果を持つ `DataFrame` です。`reset_index()` によりキー列が通常列に戻ります。
- よくある注意点: `count()` は非欠損件数、`size()` は欠損を含む行数です。どちらを使うかで件数の意味が変わります。
- 関連メソッド: `groupby()`, `agg()`, `transform()`, `sort_values()`

### 7. 月次集計

- 基本構文:

```python
monthly = df.set_index("date").resample("ME")["amount"].sum()
```

- 主な引数/指定: `set_index("date")` で日時列をインデックスにし、`resample("ME")` で月末区切りの月次集計を指定します。
- 戻り値: 月ごとの集計値を持つ `Series` または `DataFrame` です。
- よくある注意点: `resample()` は日時型インデックスが必要です。月初区切りや月末区切りなど、頻度文字列の意味をレポート要件と合わせます。
- 関連メソッド: `set_index()`, `sort_index()`, `resample()`, `reset_index()`

### 8. 移動平均

- 基本構文:

```python
monthly["rolling_3m"] = monthly["monthly_amount"].rolling(window=3).mean()
```

- 主な引数/指定: `window` で窓幅、`min_periods` で計算に必要な最小件数を指定します。
- 戻り値: 元の行数と同じ長さの `Series` です。
- よくある注意点: 最初の `window - 1` 行は既定で欠損になります。初期月にも値を出したい場合は `min_periods=1` を検討します。
- 関連メソッド: `rolling()`, `expanding()`, `shift()`, `plot()`

### 9. 出力

- 基本構文:

```python
store_summary.to_csv("store_summary.csv", index=False)
monthly.to_excel("monthly_summary.xlsx", index=False)
```

- 主な引数/指定: `index=False` で余分なインデックス列を出さず、`encoding` や `sheet_name` で共有先に合わせた形式にします。
- 戻り値: ファイルへ出力する場合は通常 `None` です。
- よくある注意点: 出力前に行数、列名、主要指標の合計を確認します。Excel出力には `openpyxl` などのライターが必要な場合があります。
- 関連メソッド: `to_csv()`, `to_excel()`, `ExcelWriter`, `read_csv()`

## 実務上のインパクト

- 読み込み直後に `head()`、`shape`、`dtypes`、`info()` を見ることで、データ事故を早期に発見できます。
- `to_datetime()` を早めに行うことで、月次集計や期間抽出の誤りを防げます。
- `dropna()` と `fillna()` を使い分けることで、削除すべき欠損と補完すべき欠損を明確にできます。
- `assign()`、`groupby()`、`agg()`、`reset_index()` を組み合わせると、明細データをレポート用の表に変換できます。
- `resample()` と `rolling()` により、時系列の粒度変換とトレンド把握ができます。
- `to_csv()`、`to_excel()` により、分析結果を共有・再利用できます。
