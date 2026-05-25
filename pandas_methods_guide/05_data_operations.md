# 05. データ操作

列を追加する、削除する、名前を変える、並べ替える、縦横の形を変える章です。実務では「分析しやすい形に変換する」中心的な作業です。

## `assign()`

- 基本の説明: 新しい列を追加した `DataFrame` を返します。
- 基本構文: `df.assign(new_col=value, other_col=lambda x: ...)`
- 主な引数/指定:
  - `列名=値`: スカラー、`Series`、配列、計算式を指定できます。
  - `列名=lambda x: ...`: `x` には処理中の `DataFrame` が渡されます。直前に `assign()` 内で作った列も後続の式から参照できます。
- 実用での使用場面: 売上金額、利益率、フラグ、ランクなどの派生列を作ります。
- 使用例:

```python
result = sales.assign(
    amount=sales["quantity"] * sales["price"],
    is_tokyo=sales["store"].eq("Tokyo"),
)
```

- 戻り値: 新しい列を追加した `DataFrame`。元の `sales` は変更されません。
- よくある注意点:
  - 既存列と同じ名前を指定すると、その列は上書きされた結果になります。
  - `Series` を渡す場合はインデックスで対応付けされます。行順だけで合わせたい場合は長さやインデックスを確認します。
  - 複雑な処理を詰め込みすぎると読みにくくなるため、意味のある単位で分けます。
- 関連メソッド: `eval()`, `pipe()`, `insert()`, `concat()`
- インパクト: 元データを直接壊さずに列追加できます。メソッドチェーンと相性がよく、前処理の再現性が上がります。

## `drop()`

- 基本の説明: 指定した行または列を削除します。
- 基本構文: `df.drop(labels=None, axis=0)`, `df.drop(index=..., columns=...)`
- 主な引数/指定:
  - `index`: 削除する行インデックスを指定します。
  - `columns`: 削除する列名を指定します。
  - `axis`: `0` または `"index"` は行、`1` または `"columns"` は列を対象にします。
  - `errors`: `"raise"` なら存在しないラベルでエラー、`"ignore"` なら無視します。
- 実用での使用場面: 不要列、集計に使わない列、誤って入った行を除外します。
- 使用例:

```python
without_price = sales.drop(columns=["price"])
without_first_row = sales.drop(index=0)
```

- 戻り値: 指定した行または列を除いた `DataFrame` または `Series`。
- よくある注意点:
  - `drop()` はデフォルトでは元データを変更しません。結果を変数に代入して使います。
  - 行番号のつもりで `index=0` を指定しても、実際には「インデックスラベル0」を削除します。
  - 必須列を落とすと後工程の `groupby()` や `merge()` が失敗するため、削除対象は明示します。
- 関連メソッド: `dropna()`, `drop_duplicates()`, `filter()`, `pop()`
- インパクト: ノイズを減らして処理対象を明確にできます。誤って必要列を落とすと後工程が壊れるため、列名指定を明示します。

## `rename()`

- 基本の説明: 行名や列名を変更します。
- 基本構文: `df.rename(columns={old: new})`, `df.rename(index={old: new})`
- 主な引数/指定:
  - `columns`: 変更前列名と変更後列名の辞書を指定します。
  - `index`: 変更前インデックス名と変更後インデックス名の辞書を指定します。
  - `mapper`: `axis` と組み合わせて辞書や関数を指定できます。
  - `errors`: `"raise"` にすると、存在しないラベル指定を検出できます。
- 実用での使用場面: 日本語列名を英語に統一する、外部データの列名を社内標準に合わせるときに使います。
- 使用例:

```python
renamed = sales.rename(columns={
    "quantity": "qty",
    "price": "unit_price",
})
```

- 戻り値: ラベル名を変更した `DataFrame` または `Series`。
- よくある注意点:
  - 辞書に存在しない列名を書いても、デフォルトではエラーになりません。タイプミスを検出したい場合は `errors="raise"` を使います。
  - 列名全体を一括で差し替える場合は `df.columns = [...]` も使えますが、列数と順序の管理が必要です。
  - 後工程で参照する列名と必ず合わせます。
- 関連メソッド: `set_axis()`, `add_prefix()`, `add_suffix()`, `rename_axis()`
- インパクト: 列名の標準化により、結合・集計・自動処理が安定します。

## `replace()`

- 基本の説明: 値を別の値に置換します。
- 基本構文: `df.replace(to_replace, value=None)`, `df.replace({col: {old: new}})`
- 主な引数/指定:
  - `to_replace`: 置換前の値、リスト、辞書、正規表現を指定します。
  - `value`: 置換後の値を指定します。
  - `regex`: `True` にすると正規表現として解釈します。
  - 辞書指定: `{列名: {置換前: 置換後}}` の形にすると列ごとに置換ルールを分けられます。
- 実用での使用場面: 表記揺れ、コード値、欠損表現を統一します。
- 使用例:

```python
cleaned = sales.replace({
    "store": {"tokyo": "Tokyo", "TOKYO": "Tokyo"},
    "product": {"unknown": pd.NA},
})
```

- 戻り値: 値を置換した `DataFrame` または `Series`。
- よくある注意点:
  - `replace()` は通常の値置換、`fillna()` は欠損値補完、`str.replace()` は文字列内の部分置換に向いています。
  - 数値の `0`、文字列の `"0"`、空文字 `""` は別の値として扱われます。
  - `regex=True` は強力ですが、意図しない部分一致を置換することがあります。
- 関連メソッド: `fillna()`, `where()`, `mask()`, `Series.str.replace()`
- インパクト: 集計時に同じ意味の値が別カテゴリとして分裂するのを防げます。

## `sort_values()`

- 基本の説明: 列の値に基づいて並べ替えます。
- 基本構文: `df.sort_values(by, ascending=True)`
- 主な引数/指定:
  - `by`: 並べ替えに使う列名。複数列ならリストで指定します。
  - `ascending`: 昇順なら `True`、降順なら `False`。複数列ではリスト指定できます。
  - `na_position`: 欠損値を `"first"` または `"last"` に置きます。
  - `kind`: ソートアルゴリズムを指定します。安定ソートが必要な場面では `"mergesort"` や `"stable"` を検討します。
- 実用での使用場面: 売上が高い順、日付が新しい順、優先度順に並べます。
- 使用例:

```python
ranked = sales.assign(amount=sales["quantity"] * sales["price"]).sort_values(
    "amount",
    ascending=False,
)
```

- 戻り値: 指定した列の値で並べ替えた `DataFrame` または `Series`。
- よくある注意点:
  - 並べ替え後も元のインデックスは保持されます。連番に戻したい場合は `reset_index(drop=True)` を使います。
  - 文字列の数値は辞書順で並ぶため、必要なら数値型に変換してから並べます。
  - 欠損値の位置は `na_position` で明示するとレポートの見え方が安定します。
- 関連メソッド: `sort_index()`, `nlargest()`, `nsmallest()`, `rank()`
- インパクト: 上位・下位の把握、レポート作成、異常値確認がしやすくなります。

## `sort_index()`

- 基本の説明: インデックスの順序で並べ替えます。
- 基本構文: `df.sort_index(axis=0, ascending=True)`
- 主な引数/指定:
  - `axis`: `0` は行インデックス、`1` は列ラベルを並べ替えます。
  - `ascending`: 昇順・降順を指定します。
  - `level`: `MultiIndex` の特定階層だけを対象にします。
  - `na_position`: 欠損ラベルの位置を指定します。
- 実用での使用場面: 日付インデックスやIDインデックスを昇順に戻すときに使います。
- 使用例:

```python
by_date = sales.set_index("date").sort_index()
```

- 戻り値: インデックス順に並べ替えた `DataFrame` または `Series`。
- よくある注意点:
  - 日付らしい文字列のままだと文字列順になります。時系列では `to_datetime()` 後に並べます。
  - インデックスが重複していても並べ替え自体はできますが、後続の参照や結合が曖昧になることがあります。
  - 列順をアルファベット順にしたい場合は `axis=1` を使います。
- 関連メソッド: `sort_values()`, `set_index()`, `reset_index()`, `reindex()`
- インパクト: 時系列処理や比較処理の前提を整えます。インデックス順が乱れていると、差分や移動平均の解釈が難しくなります。

## `reset_index()`

- 基本の説明: インデックスを通常の列に戻し、連番インデックスにします。
- 基本構文: `df.reset_index(drop=False)`, `series.reset_index(name=...)`
- 主な引数/指定:
  - `drop`: `True` にすると元のインデックスを列に残さず捨てます。
  - `names`: インデックスを列に戻すときの列名を指定します。
  - `level`: `MultiIndex` の一部階層だけを戻します。
  - `name`: `Series.reset_index()` で値列の名前を指定します。
- 実用での使用場面: `groupby()` 後の結果を通常の表に戻す、日付インデックスを列として出力する場面で使います。
- 使用例:

```python
summary = (
    sales.groupby("store")["quantity"]
    .sum()
    .reset_index(name="total_quantity")
)
```

- 戻り値: 連番インデックスに戻した `DataFrame`。`Series` に対して使うと通常は `DataFrame` になります。
- よくある注意点:
  - `drop=False` のままだと元インデックスが列として増えます。不要なら `drop=True` を指定します。
  - 既存列名とインデックス名が衝突するとエラーになることがあります。
  - `groupby()` 結果を表にしたいだけなら、集計時に `as_index=False` を指定する方法もあります。
- 関連メソッド: `set_index()`, `rename_axis()`, `sort_index()`, `groupby()`
- インパクト: 集計結果をCSV出力や結合に使いやすい形にできます。

## `melt()`

- 基本の説明: 横持ちデータを縦持ちデータに変換します。
- 基本構文: `df.melt(id_vars=..., value_vars=..., var_name=..., value_name=...)`
- 主な引数/指定:
  - `id_vars`: 縦持ち化しても識別子として残す列を指定します。
  - `value_vars`: 縦に並べる対象列を指定します。省略すると `id_vars` 以外が対象です。
  - `var_name`: 元の列名を格納する列名を指定します。
  - `value_name`: 元の値を格納する列名を指定します。
  - `ignore_index`: `True` なら新しい連番インデックスにします。
- 実用での使用場面: 月別列、商品別列、指標別列を、分析や可視化しやすい縦長形式に変換します。
- 使用例:

```python
wide = pd.DataFrame({
    "store": ["Tokyo", "Osaka"],
    "sales_A": [120000, 90000],
    "sales_B": [80000, 70000],
})

long = wide.melt(
    id_vars="store",
    var_name="product",
    value_name="sales",
)
```

- 戻り値: 縦持ち形式に変換した `DataFrame`。
- よくある注意点:
  - `id_vars` の指定を誤ると、識別子にすべき列まで縦に展開されます。
  - `value_name` が既存列名と重なると混乱しやすいため、意味のある名前にします。
  - `melt()` 後は行数が増えるため、後続処理の件数や重み付けに注意します。
- 関連メソッド: `pivot()`, `pivot_table()`, `stack()`, `wide_to_long()`
- インパクト: 可視化、集計、機械学習前処理で扱いやすい「1行1観測」の形に整えられます。
