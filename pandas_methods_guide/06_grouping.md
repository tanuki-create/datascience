# 06. グルーピング

グルーピングは「カテゴリごとに分けて計算する」ための機能です。店舗別、商品別、月別、ユーザー別など、実務分析の中心になります。

## `groupby()`

- 基本の説明: 指定した列やインデックスでデータをグループに分けます。
- 基本構文: `df.groupby(by)[target].集計関数()`, `df.groupby(by).agg(...)`
- 主な引数/指定:
  - `by`: グループ化に使う列名、列名リスト、関数、`Series` などを指定します。
  - `as_index`: `False` にするとグループキーをインデックスではなく列として残します。
  - `dropna`: `False` にするとグループキーの欠損値も1つのグループとして扱います。
  - `sort`: グループキーで並べ替えるかを指定します。元の出現順を重視する場合は `False` を検討します。
- 実用での使用場面: 店舗別売上、商品別数量、ユーザー別利用回数などを集計します。
- 使用例:

```python
store_summary = sales.groupby("store")["quantity"].sum()
```

- 戻り値: `groupby()` 単体では `DataFrameGroupBy` または `SeriesGroupBy` オブジェクトを返します。`sum()` や `agg()` などを呼んで初めて集計結果になります。
- よくある注意点:
  - `groupby()` しただけでは計算は完了していません。必ず集計・変換・抽出のメソッドを続けます。
  - デフォルトではグループキーがインデックスになりやすいため、通常の列として扱いたい場合は `as_index=False` や `reset_index()` を使います。
  - 欠損キーはデフォルトでグループから除外されます。欠損もカテゴリとして数えたい場合は `dropna=False` を明示します。
- 関連メソッド: `agg()`, `transform()`, `filter()`, `pivot_table()`, `resample()`
- インパクト: 明細データを意思決定に使える集計値へ変換できます。

## `agg()`

- 基本の説明: 複数の集計関数をまとめて適用します。
- 基本構文: `df.groupby(keys).agg(new_col=(source_col, func))`
- 主な引数/指定:
  - 文字列関数: `"sum"`, `"mean"`, `"count"`, `"nunique"` などを指定します。
  - リスト指定: `{"quantity": ["sum", "mean"]}` のように複数集計できます。
  - 名前付き集計: `total=("amount", "sum")` のように出力列名を明示できます。
  - 独自関数: `lambda` や関数名を指定できますが、速度と可読性に注意します。
- 実用での使用場面: 店舗別に合計、平均、件数を同時に出すレポートで使います。
- 使用例:

```python
summary = sales.groupby("store").agg(
    total_quantity=("quantity", "sum"),
    avg_price=("price", "mean"),
    rows=("product", "count"),
)
```

- 戻り値: 集計後の `DataFrame` または `Series`。複数関数をリスト指定すると列が階層構造になることがあります。
- よくある注意点:
  - `count` は欠損を除いた件数、`size` は欠損を含む行数です。件数定義を取り違えないようにします。
  - 複数集計で `MultiIndex` 列になると後続処理が扱いにくいため、名前付き集計が実務では便利です。
  - 独自関数は便利ですが、標準集計より遅くなりやすいです。
- 関連メソッド: `groupby()`, `sum()`, `mean()`, `size()`, `describe()`
- インパクト: 複数指標を1回の処理で作れるため、レポート作成が安定します。

## `apply()`

- 基本の説明: 各グループや行・列に任意の関数を適用します。
- 基本構文: `df.groupby(keys).apply(func)`, `df.apply(func, axis=...)`
- 主な引数/指定:
  - `func`: 各グループ、行、列に適用する関数を指定します。
  - `axis`: 通常の `DataFrame.apply()` では `0` が列方向、`1` が行方向です。
  - `args`, `kwargs`: 関数へ追加引数を渡すときに使います。
- 実用での使用場面: 標準メソッドだけでは書きにくい独自計算を行います。
- 使用例:

```python
def top_product(group):
    amounts = group["quantity"] * group["price"]
    return group.loc[amounts.idxmax(), "product"]

top_by_store = sales.dropna(subset=["quantity"]).groupby("store").apply(top_product)
```

- 戻り値: 関数の戻り値に応じて `Series`、`DataFrame`、スカラーの組み合わせになります。
- よくある注意点:
  - `apply()` は柔軟ですが、pandasのベクトル化処理より遅くなりがちです。
  - 関数が返す形がグループごとに揃っていないと、扱いにくい結果になります。
  - 集計なら `agg()`、元行数を保つ計算なら `transform()`、行単位の単純な条件ならベクトル演算を先に検討します。
- 関連メソッド: `agg()`, `transform()`, `map()`, `pipe()`, `filter()`
- インパクト: 柔軟性は高いですが、処理速度は遅くなりがちです。まず `agg()` や `transform()` で書けないか検討します。

## `transform()`

- 基本の説明: グループ単位で計算し、元データと同じ行数の結果を返します。
- 基本構文: `df.groupby(keys)[col].transform(func)`
- 主な引数/指定:
  - `func`: `"sum"`, `"mean"`, `"rank"` などの文字列関数、または関数を指定します。
  - 対象列: 通常は `groupby(keys)[col]` のように列を絞ってから使います。
  - 複数列: `DataFrameGroupBy.transform()` で複数列に同じ変換を適用できます。
- 実用での使用場面: 店舗内平均との差、店舗内シェア、グループ内順位など、明細行に集計結果を戻すときに使います。
- 使用例:

```python
df = sales.assign(amount=sales["quantity"] * sales["price"])
df["store_total"] = df.groupby("store")["amount"].transform("sum")
df["share_in_store"] = df["amount"] / df["store_total"]
```

- 戻り値: 元データと同じ長さの `Series` または同じ形にそろった `DataFrame`。
- よくある注意点:
  - 各グループで返す値は、スカラーまたはグループと同じ長さにできる値である必要があります。
  - 集計結果だけが欲しい場合は `agg()` の方が自然です。
  - 元行に戻して使う処理なので、代入先のインデックス整合性を確認します。
- 関連メソッド: `agg()`, `rank()`, `cumcount()`, `cumsum()`, `ngroup()`
- インパクト: 集計値と明細を自然に同居させられます。特徴量作成で特に重要です。

## `filter()`

- 基本の説明: グループ単位の条件で、残すグループを選びます。
- 基本構文: `df.groupby(keys).filter(lambda g: 条件)`
- 主な引数/指定:
  - `func`: 各グループを受け取り、残すなら `True`、除外するなら `False` を返す関数を指定します。
  - `dropna`: 条件を満たさないグループを欠損行として残すか、削除するかを指定します。
- 実用での使用場面: 注文数が一定以上ある店舗だけ、平均売上が高いカテゴリだけを残します。
- 使用例:

```python
active_stores = sales.groupby("store").filter(lambda g: g["quantity"].count() >= 2)
```

- 戻り値: 条件を満たしたグループの元行を残した `DataFrame`。
- よくある注意点:
  - `filter()` は集計表ではなく、条件を満たすグループに属する元の明細行を返します。
  - 行単位の条件抽出には `loc[]`、集計結果の絞り込みには `agg()` 後の条件指定を使う方が明確です。
  - グループごとに関数を実行するため、大規模データでは集計してからキーで絞る方が速い場合があります。
- 関連メソッド: `groupby()`, `agg()`, `transform()`, `loc[]`, `query()`
- インパクト: 行単位ではなくグループ単位でデータを絞れるため、分析対象の品質を揃えられます。
