# 14. 出力

分析結果は、共有・再利用できる形で出力して価値になります。CSVやExcelは実務で特によく使う出力形式です。

## `to_csv()`

- 基本の説明: `DataFrame` をCSVファイルとして保存します。
- 実用での使用場面: 集計結果の共有、他システムへの連携、処理済みデータの保存に使います。
- 基本構文:

```python
df.to_csv(path_or_buf, index=True, encoding=None, sep=",", columns=None)
```

- 主な引数/指定:
  - `path_or_buf`: 保存先のファイルパス、またはファイル風オブジェクトです。
  - `index`: インデックスを出力するかを指定します。通常の表では `False` がよく使われます。
  - `encoding`: 文字コードを指定します。Excelで開く前提なら `"utf-8-sig"` が便利な場合があります。
  - `sep`: 区切り文字を指定します。TSVなら `"\t"` を指定します。
  - `columns`: 出力する列を絞る場合に指定します。
  - `header`: 列名行を出力するか、または別名の列名リストを指定します。
  - `mode`: `"w"` は上書き、`"a"` は追記です。
- 使用例:

```python
summary = sales.groupby("store")["quantity"].sum().reset_index()
summary.to_csv("store_summary.csv", index=False, encoding="utf-8")
```

- 戻り値: ファイルへ保存した場合は `None` です。`path_or_buf=None` の場合はCSV文字列を返します。
- インパクト: 軽量で汎用的な形式としてデータを渡せます。`index=False` を付けないと不要なインデックス列が出ることがあります。
- よくある注意点:
  - 日本語をExcelで開くと文字化けする場合があります。その場合は `encoding="utf-8-sig"` を試します。
  - `index=True` のまま出力すると、読み戻したときに `Unnamed: 0` のような不要列が出ることがあります。
  - カンマや改行を含む文字列は引用符付きで出力されます。連携先システムのCSV仕様と合わせます。
  - 追記出力ではヘッダーが重複しやすいため、`mode="a"` と `header=False` の組み合わせに注意します。
- 関連メソッド: `read_csv()`, `to_excel()`, `reset_index()`, `to_json()`, `to_parquet()`

## `to_excel()`

- 基本の説明: `DataFrame` をExcelファイルとして保存します。
- 実用での使用場面: 部門共有、報告書、手作業レビュー用のファイル作成に使います。
- 基本構文:

```python
df.to_excel(excel_writer, sheet_name="Sheet1", index=True, columns=None)
```

- 主な引数/指定:
  - `excel_writer`: 保存先パス、または `pd.ExcelWriter` オブジェクトです。
  - `sheet_name`: 出力するシート名を指定します。
  - `index`: インデックスを出力するかを指定します。
  - `columns`: 出力する列を絞る場合に指定します。
  - `startrow`, `startcol`: 書き込み開始位置を指定します。
  - `freeze_panes`: 固定表示する行・列の位置を指定します。
  - `engine`: `"openpyxl"` や `"xlsxwriter"` などのライターを指定します。
- 使用例:

```python
summary = sales.groupby("store")["quantity"].sum().reset_index()
summary.to_excel("store_summary.xlsx", index=False, sheet_name="summary")
```

- 戻り値: `None` です。指定したExcelファイルへ書き込みます。
- インパクト: 非エンジニアにも扱いやすい形で結果を共有できます。複数シート出力には `pd.ExcelWriter` を使います。
- 注意点: `.xlsx` 出力には環境によって `openpyxl` などのExcelライターが必要です。実行環境にない場合はインストールするか、CSV出力に切り替えます。
- よくある注意点:
  - Excelの1シートには行数・列数の上限があります。大規模データの保存にはCSVやParquetも検討します。
  - 複数シートに出力する場合は `with pd.ExcelWriter(...) as writer:` の中で複数回 `to_excel()` を呼びます。
  - 既存ファイルを上書きするため、手作業で編集されたファイルに出す場合は保存先名を分けます。
  - 日付や数値の表示形式はExcel側の見え方に依存します。体裁まで必要なら `xlsxwriter` などで書式設定します。
- 関連メソッド: `read_excel()`, `to_csv()`, `ExcelWriter`, `Styler.to_excel()`
