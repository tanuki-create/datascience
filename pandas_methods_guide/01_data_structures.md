# 01. データ構造

pandasの中心は `Series` と `DataFrame` です。`Series` は1列のラベル付きデータ、`DataFrame` は行と列を持つ表データです。

## `Series()`

- 基本の説明: 1次元のラベル付き配列です。値の集合にインデックスが付いたものと考えると理解しやすいです。
- 基本構文: `pd.Series(data=None, index=None, dtype=None, name=None)`
- 主な引数/指定:
  - `data`: リスト、辞書、NumPy配列、スカラー値などを指定します。
  - `index`: 各値に対応するラベルを指定します。省略すると `0` 始まりの整数インデックスになります。
  - `dtype`: 値の型を明示します。数値、文字列、カテゴリ、日時などを意図通り扱いたいときに重要です。
  - `name`: `Series` 自体の名前です。`DataFrame` に変換したときの列名にもなります。
- 戻り値: `pandas.Series` オブジェクトを返します。
- 実用での使用場面: 1列だけの売上、スコア、カテゴリ、時系列値を扱うときに使います。`DataFrame` の1列を取り出した結果も多くの場合 `Series` です。
- 使用例:

```python
import pandas as pd

sales_amount = pd.Series([1200, 2500, 1800], index=["A", "B", "C"], name="sales")
print(sales_amount)
print(sales_amount.mean())

status = pd.Series({"A": "active", "B": "paused"})
print(status.loc["A"])
```

- よくある注意点:
  - 辞書から作る場合、辞書のキーがインデックスになります。別途 `index` を指定すると、その順序に合わせて値が並び、不足するキーは欠損値になります。
  - 整数ラベルの `Series` では、ラベル指定と位置指定を混同しやすいです。ラベルは `loc[]`、位置は `iloc[]` を使うと意図が明確です。
  - 欠損値を含む整数列は、従来のNumPy整数型ではなく浮動小数やpandasのnullable整数型になることがあります。
- 関連メソッド: `DataFrame()`, `to_frame()`, `astype()`, `rename()`, `reset_index()`, `loc[]`, `iloc[]`
- インパクト: 列単位の計算、欠損チェック、集計が簡潔になります。pandasの多くの処理は `Series` を理解すると一気に読みやすくなります。

## `DataFrame()`

- 基本の説明: 2次元の表データです。列ごとに異なる型を持てるため、ExcelやSQLテーブルに近い感覚で扱えます。
- 基本構文: `pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)`
- 主な引数/指定:
  - `data`: 辞書、リストのリスト、辞書のリスト、NumPy配列、別の `DataFrame` などを指定します。
  - `index`: 行ラベルを指定します。省略すると `0` 始まりの整数インデックスになります。
  - `columns`: 列名と列順を指定します。存在しない列名を指定すると、その列は欠損値になります。
  - `dtype`: 全体に適用する型を指定します。列ごとに型を分けたい場合は作成後に `astype()` などを使います。
  - `copy`: 入力データをコピーするかどうかを指定します。通常は明示しなくて問題ありません。
- 戻り値: `pandas.DataFrame` オブジェクトを返します。
- 実用での使用場面: CSV、Excel、データベース、APIレスポンスなどを分析可能な表に変換するときに使います。
- 使用例:

```python
import pandas as pd

df = pd.DataFrame({
    "store": ["Tokyo", "Osaka"],
    "sales": [120000, 98000],
    "orders": [80, 64],
})

df["unit_price"] = df["sales"] / df["orders"]
print(df)

records = [
    {"store": "Tokyo", "sales": 120000},
    {"store": "Osaka", "sales": 98000},
]
df_from_records = pd.DataFrame(records, columns=["store", "sales"])
```

- よくある注意点:
  - 辞書で作る場合、各列の長さは揃っている必要があります。長さが違うとエラーになります。
  - 辞書のリストで作る場合、レコードごとに存在しないキーは欠損値になります。
  - `columns` を指定すると列順を固定できますが、入力にない列を指定すると空の列ができるため、タイプミスに注意します。
  - 表示上は同じ値に見えても、列の型が `object` になっていると数値計算や日時処理で期待通り動かないことがあります。
- 関連メソッド: `Series()`, `read_csv()`, `read_excel()`, `from_records()`, `from_dict()`, `astype()`, `copy()`
- インパクト: 複数列を組み合わせた加工、集計、結合、可視化の土台になります。分析パイプラインの中心オブジェクトです。
