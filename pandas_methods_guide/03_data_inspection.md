# 03. データ確認

データ確認は、分析前の健康診断です。行数、列名、型、欠損、分布を最初に見ることで、後工程の手戻りを減らします。

## `head()`

- 基本の説明: 先頭数行を表示します。デフォルトは5行です。
- 基本構文: `df.head(n=5)` / `series.head(n=5)`
- 主な引数/指定:
  - `n`: 表示する行数を指定します。負の値を指定すると末尾から指定行数を除いた結果になります。
- 戻り値: 元データと同じ型の `DataFrame` または `Series` を返します。
- 実用での使用場面: 読み込み直後に列名、値の形式、日付やカテゴリの見た目を確認します。
- 使用例:

```python
print(sales.head())
print(sales.head(10))
preview = sales.head(3)
```

- よくある注意点:
  - 先頭だけでは全体の偏りや末尾の異常を見落とします。`tail()`、`sample()`、`describe()` も併用します。
  - 表示は省略されることがあります。列数が多い場合は `columns` や `info()` で構造も確認します。
  - `head()` は元データを変更しません。確認用の戻り値です。
- 関連メソッド: `tail()`, `sample()`, `info()`, `describe()`
- インパクト: データの全体感を素早く掴み、読み込みミスや列ずれを早期に見つけられます。

## `tail()`

- 基本の説明: 末尾数行を表示します。デフォルトは5行です。
- 基本構文: `df.tail(n=5)` / `series.tail(n=5)`
- 主な引数/指定:
  - `n`: 表示する行数を指定します。負の値を指定すると先頭から指定行数を除いた結果になります。
- 戻り値: 元データと同じ型の `DataFrame` または `Series` を返します。
- 実用での使用場面: ログや時系列データで最新行を確認します。
- 使用例:

```python
print(sales.tail())
print(sales.tail(10))
```

- よくある注意点:
  - データが時系列順に並んでいるとは限りません。最新行を確認したい場合は、必要に応じて日付列で並べ替えます。
  - 末尾に集計行や注釈行が混ざるCSV/Excelでは、`tail()` で読み込み不要行を発見できます。
  - `tail()` も元データを変更しません。
- 関連メソッド: `head()`, `sample()`, `sort_values()`, `info()`
- インパクト: 追加データの反映、日付範囲、末尾の異常値確認に役立ちます。

## `info()`

- 基本の説明: 行数、列数、欠損していない件数、データ型、メモリ使用量を表示します。
- 基本構文: `df.info(verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None)`
- 主な引数/指定:
  - `verbose`: 列情報を詳細表示するかを指定します。列数が多いと自動で省略されることがあります。
  - `buf`: 出力先を指定します。文字列として取得したい場合は `io.StringIO()` を使います。
  - `max_cols`: 詳細表示する列数の上限を指定します。
  - `memory_usage`: メモリ使用量の表示方法を指定します。`"deep"` で文字列列を含めて詳しく見積もれます。
  - `show_counts`: 非欠損件数を表示するかを指定します。
- 戻り値: 画面または指定先に情報を出力し、戻り値は通常 `None` です。
- 実用での使用場面: 読み込み直後の型確認、欠損列の把握、メモリ負荷の確認に使います。
- 使用例:

```python
sales.info()
sales.info(memory_usage="deep")
```

- よくある注意点:
  - `print(sales.info())` と書くと、情報の後に `None` が表示されます。通常は `sales.info()` だけで使います。
  - `object` 型は文字列だけでなく、混在型の可能性もあります。必要に応じて実データや `map(type)` で確認します。
  - 非欠損件数は欠損の有無を見る入口です。欠損率や欠損パターンは `isna()` と集計で追加確認します。
- 関連メソッド: `dtypes`, `isna()`, `memory_usage()`, `astype()`, `convert_dtypes()`
- インパクト: `object` や `string` になっている日付・数値列を見つけられます。型修正の優先順位を決めやすくなります。

## `describe()`

- 基本の説明: 数値列の件数、平均、標準偏差、最小値、四分位数、最大値などを出します。
- 基本構文: `df.describe(percentiles=None, include=None, exclude=None)` / `series.describe(percentiles=None)`
- 主な引数/指定:
  - `percentiles`: 表示する分位点をリストで指定します。例: `[0.01, 0.05, 0.5, 0.95, 0.99]`
  - `include`: 集計対象の型を指定します。`"all"` で全列、`"object"` で文字列系を含められます。
  - `exclude`: 集計から除外する型を指定します。
- 戻り値: 要約統計量を持つ `DataFrame` または `Series` を返します。
- 実用での使用場面: 外れ値、スケール感、分布の偏りを確認します。
- 使用例:

```python
print(sales.describe())
print(sales.describe(include="all"))
print(sales.describe(percentiles=[0.05, 0.5, 0.95]))
```

- よくある注意点:
  - デフォルトでは主に数値列だけが対象です。カテゴリ列や文字列列も見たい場合は `include` を指定します。
  - 平均と中央値が大きく離れている場合は、外れ値や偏りを疑います。
  - 欠損値は集計から除外されます。欠損の多さは `info()` や `isna().sum()` で別に確認します。
  - 標準偏差や四分位数だけでは分布の形までは分かりません。必要に応じてヒストグラムなども使います。
- 関連メソッド: `info()`, `value_counts()`, `mean()`, `median()`, `quantile()`, `isna()`
- インパクト: 分析前に異常値や桁違いの値を発見できます。前処理や可視化の方針決定に効きます。

## `shape`

- 基本の説明: `(行数, 列数)` を返す属性です。メソッドではないため `()` は付けません。
- 基本構文: `df.shape` / `series.shape`
- 主な引数/指定: 属性のため引数はありません。
- 戻り値: 次元ごとの要素数を表すタプルを返します。`DataFrame` では `(行数, 列数)`、`Series` では `(要素数,)` です。
- 実用での使用場面: フィルタや結合の前後でレコード数が想定通りか確認します。
- 使用例:

```python
rows, cols = sales.shape
print(rows, cols)

before_rows = sales.shape[0]
after_rows = sales.drop_duplicates().shape[0]
```

- よくある注意点:
  - `shape` は属性なので `sales.shape()` とは書きません。
  - 行数だけが必要なら `len(sales)` や `sales.shape[0]` を使います。
  - 列数だけを見ても、必要列の存在は保証できません。`columns` と組み合わせて確認します。
- 関連メソッド: `len()`, `size`, `columns`, `index`, `drop_duplicates()`
- インパクト: データ欠落、重複増殖、不自然な結合結果を数で検知できます。

## `columns`

- 基本の説明: 列名の一覧を返す属性です。
- 基本構文: `df.columns`
- 主な引数/指定: 属性のため引数はありません。列名の変更は `df.columns = [...]` または `rename()` を使います。
- 戻り値: 列ラベルを持つ `pandas.Index` を返します。
- 実用での使用場面: 列名の確認、列名変更前の把握、必要列の存在チェックに使います。
- 使用例:

```python
print(sales.columns)
print(list(sales.columns))

required = {"date", "store", "sales"}
missing = required - set(sales.columns)
```

- よくある注意点:
  - 戻り値は通常のリストではなく `Index` です。リストとして扱いたい場合は `list(sales.columns)` にします。
  - 列名の前後に空白が入っていると選択時にエラーになりやすいです。`sales.columns.str.strip()` で確認・補正できます。
  - 重複した列名を持つ `DataFrame` も作れてしまいます。必要に応じて `sales.columns.duplicated()` で確認します。
- 関連メソッド: `rename()`, `set_axis()`, `filter()`, `reindex()`, `Index`
- インパクト: スペースや表記揺れを見つけられます。自動処理で列名エラーを減らせます。

## `dtypes`

- 基本の説明: 各列のデータ型を返す属性です。
- 基本構文: `df.dtypes` / `series.dtype`
- 主な引数/指定: 属性のため引数はありません。`DataFrame` では列ごとの型一覧、`Series` では `dtype` を使います。
- 戻り値: `DataFrame.dtypes` は列名をインデックスにした `Series`、`Series.dtype` は単一のdtypeを返します。
- 実用での使用場面: 数値、文字列、日付が想定通り読み込まれているか確認します。
- 使用例:

```python
print(sales.dtypes)
print(sales["date"].dtype)
```

- よくある注意点:
  - `object` 型は文字列、数値と文字列の混在、Pythonオブジェクトなど複数の可能性があります。
  - 日付が `object` のままだと、時系列処理や日付比較が正しくできないことがあります。`to_datetime()` を検討します。
  - 整数列に欠損があると、nullable整数型や浮動小数型になることがあります。
  - 型変換は `astype()`、`to_numeric()`、`to_datetime()`、`convert_dtypes()` などを使い分けます。
- 関連メソッド: `info()`, `astype()`, `convert_dtypes()`, `to_numeric()`, `to_datetime()`, `select_dtypes()`
- インパクト: 型が不適切なまま集計すると、計算結果や並び順が誤ることがあります。早期確認の効果が大きい項目です。
