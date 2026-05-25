# 02. データ生成・読み込み

外部ファイルやPythonオブジェクトから `DataFrame` を作る章です。分析の品質は、読み込み時の型、欠損値、文字コード、日付解釈で大きく変わります。

## `read_csv()`

- 基本の説明: CSVファイルを `DataFrame` として読み込みます。
- 基本構文: `pd.read_csv(filepath_or_buffer, sep=",", header="infer", names=None, index_col=None, usecols=None, dtype=None, parse_dates=None, encoding=None)`
- 主な引数/指定:
  - `filepath_or_buffer`: CSVファイルのパス、URL、ファイルライクオブジェクトを指定します。
  - `sep`: 区切り文字を指定します。タブ区切りなら `sep="\t"` を使います。
  - `header`: 列名として使う行を指定します。列名行がない場合は `header=None` にします。
  - `names`: 列名を明示します。`header=None` と組み合わせることが多いです。
  - `index_col`: インデックスにする列を指定します。
  - `usecols`: 読み込む列を絞ります。大きなCSVではメモリ削減にも効きます。
  - `dtype`: 列ごとの型を指定します。IDや郵便番号のような値は文字列として読むことがあります。
  - `parse_dates`: 日付として解釈する列を指定します。
  - `encoding`: 文字コードを指定します。日本語CSVでは `utf-8`, `utf-8-sig`, `cp932` などを確認します。
- 戻り値: CSVの内容を持つ `pandas.DataFrame` を返します。
- 実用での使用場面: 売上ログ、広告レポート、システム出力、機械学習用データセットなど、最も頻繁に使う入力です。
- 使用例:

```python
import pandas as pd

df = pd.read_csv(
    "sales.csv",
    parse_dates=["date"],
    dtype={"store_id": "string"},
)

log = pd.read_csv(
    "access.log",
    sep="\t",
    names=["timestamp", "user_id", "path"],
    parse_dates=["timestamp"],
)
```

- よくある注意点:
  - 先頭のゼロを持つコード値を数値として読むと、ゼロが落ちます。`dtype={"code": "string"}` のように指定します。
  - Excel由来のCSVはBOM付きUTF-8やShift_JIS系の文字コードで保存されていることがあります。文字化け時は `encoding` を確認します。
  - 空文字、`NA`、`NULL` などは欠損値として解釈されることがあります。必要に応じて `keep_default_na` や `na_values` を調整します。
  - 巨大ファイルでは `usecols`、`dtype`、`chunksize` を使うと読み込み負荷を抑えられます。
- 関連メソッド: `to_csv()`, `read_table()`, `read_excel()`, `read_json()`, `DataFrame()`
- インパクト: `parse_dates` や `dtype` を明示すると、後工程の型変換ミスや集計ミスを減らせます。

## `read_excel()`

- 基本の説明: Excelファイルを `DataFrame` として読み込みます。
- 基本構文: `pd.read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None, dtype=None, parse_dates=False, engine=None)`
- 主な引数/指定:
  - `io`: Excelファイルのパス、URL、ファイルライクオブジェクトを指定します。
  - `sheet_name`: 読み込むシート名またはシート番号を指定します。複数指定や `None` で複数シートを読み込めます。
  - `header`: 列名として使う行を指定します。表の上にタイトル行があるExcelでは調整が必要です。
  - `usecols`: 読み込む列を列名、Excel列記号、範囲などで指定します。
  - `dtype`: 列ごとの型を指定します。
  - `parse_dates`: 日付として解釈する列を指定します。
  - `engine`: 読み込みエンジンを指定します。通常は自動判定で十分です。
- 戻り値: `sheet_name` が単一指定なら `DataFrame`、複数シート指定や `None` の場合はシート名をキーにした辞書を返します。
- 実用での使用場面: 部門から受け取る管理表、請求データ、手作業で更新されるマスタを取り込むときに使います。
- 使用例:

```python
import pandas as pd

df = pd.read_excel(
    "monthly_report.xlsx",
    sheet_name="sales",
    usecols=["date", "store", "sales"],
)

all_sheets = pd.read_excel("monthly_report.xlsx", sheet_name=None)
sales = all_sheets["sales"]
```

- よくある注意点:
  - Excelの見た目とデータ構造は一致しないことがあります。結合セル、注釈行、空白行、複数表が混在するシートに注意します。
  - `sheet_name=None` は全シートを読むため、ファイルが大きいと時間がかかります。
  - 日付やIDがExcel側で自動変換されている場合、読み込み後の型と値を必ず確認します。
  - `.xlsx` を読むには環境によって `openpyxl` などの追加ライブラリが必要です。
- 関連メソッド: `to_excel()`, `ExcelFile`, `read_csv()`, `read_html()`, `DataFrame()`
- インパクト: Excel前提の業務データを自動処理に載せられます。`sheet_name` や `usecols` を使うと不要な列を読み込まずに済みます。

## `read_json()`

- 基本の説明: JSON形式のデータを `DataFrame` として読み込みます。
- 基本構文: `pd.read_json(path_or_buf, orient=None, typ="frame", dtype=None, convert_dates=True, lines=False, encoding=None)`
- 主な引数/指定:
  - `path_or_buf`: JSONファイルのパス、URL、JSON文字列、ファイルライクオブジェクトを指定します。
  - `orient`: JSONの構造を指定します。`records`, `columns`, `index`, `split`, `table` などがあります。
  - `typ`: `frame` なら `DataFrame`、`series` なら `Series` として読み込みます。
  - `dtype`: 列ごとの型を指定します。
  - `convert_dates`: 日付らしい値を日時型へ変換するかを指定します。
  - `lines`: 1行1JSONのJSON Lines形式を読む場合に `True` にします。
  - `encoding`: 文字コードを指定します。
- 戻り値: 通常は `pandas.DataFrame` を返します。`typ="series"` の場合は `Series` を返します。
- 実用での使用場面: Web API、ログ、NoSQL由来のデータを表形式に変換するときに使います。
- 使用例:

```python
import pandas as pd

df = pd.read_json("events.json", lines=True)

records = pd.read_json("users.json", orient="records")
```

- よくある注意点:
  - JSON Lines形式は `lines=True` が必要です。通常のJSON配列とは読み方が異なります。
  - ネストしたJSONは、そのままでは列に辞書やリストが入ることがあります。平坦化したい場合は `json_normalize()` を使います。
  - APIレスポンスを直接読む場合、必要な配列部分だけを取り出してから `DataFrame` 化する方が扱いやすいことがあります。
  - `orient` が保存時と一致しないと、行列の向きや列名が想定とずれることがあります。
- 関連メソッド: `to_json()`, `json_normalize()`, `DataFrame()`, `read_csv()`
- インパクト: APIやログの半構造データを集計できる形に変換できます。ネストが深い場合は `json_normalize()` も検討します。

## `dict`

- 基本の説明: Python標準の辞書です。pandasメソッドではありませんが、`DataFrame` や `Series` の入力としてよく使います。
- 基本構文: `{"列名": [値1, 値2, ...]}` または `{"キー": 値}`
- 主な引数/指定:
  - キー: `DataFrame` 作成時は列名、`Series` 作成時はインデックスになりやすいです。
  - 値: リスト、スカラー、辞書、`Series` などを入れられます。
  - 辞書のリスト: `[{列名: 値, ...}, ...]` の形は、APIレスポンスやレコード形式のデータと相性が良いです。
- 戻り値: `dict` 自体はPythonの辞書です。`pd.DataFrame(data)` や `pd.Series(data)` に渡すとpandasオブジェクトが作られます。
- 実用での使用場面: 小さなサンプルデータ、設定値、APIレスポンス、マッピング表を作るときに使います。
- 使用例:

```python
import pandas as pd

data = {
    "store": ["Tokyo", "Osaka"],
    "sales": [120000, 98000],
}

df = pd.DataFrame(data)

mapping = {"Tokyo": "east", "Osaka": "west"}
df["area"] = df["store"].map(mapping)
```

- よくある注意点:
  - `DataFrame` に渡す列形式の辞書では、各リストの長さが同じである必要があります。
  - スカラー値だけの辞書を `DataFrame` にする場合は、`index` の指定が必要になることがあります。
  - レコード形式の辞書リストでは、存在しないキーが欠損値になります。APIデータではよく起きます。
  - マッピング用途では、キーの表記揺れがあると `map()` の結果が欠損値になります。
- 関連メソッド: `DataFrame()`, `Series()`, `from_dict()`, `from_records()`, `map()`, `json_normalize()`
- インパクト: テストデータや説明用データをすぐ作れます。列名と値の関係が明示されるため、コードの意図も読みやすくなります。
