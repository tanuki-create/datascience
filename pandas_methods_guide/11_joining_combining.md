# 11. データ結合

実務データは複数の表に分かれています。明細、マスタ、ログ、外部データを正しく結合できるかが分析品質を左右します。

## `merge()`

- 基本の説明: SQLのJOINのように、共通キーで2つの `DataFrame` を結合します。
- 実用での使用場面: 売上明細に店舗マスタ、商品マスタ、顧客属性を付与します。
- 基本構文:

```python
pd.merge(left, right, how="inner", on=None, left_on=None, right_on=None)
left.merge(right, how="inner", on=None)
```

- 主な引数/指定:
  - `left`, `right`: 結合する2つの `DataFrame` です。
  - `how`: `"inner"`, `"left"`, `"right"`, `"outer"`, `"cross"` から結合方法を指定します。
  - `on`: 両方の表に同じ名前で存在するキー列を指定します。
  - `left_on`, `right_on`: 左右でキー列名が違う場合に指定します。
  - `left_index`, `right_index`: インデックスをキーにする場合に `True` を指定します。
  - `suffixes`: 同名列が衝突したときに付ける接尾辞を指定します。
  - `validate`: `"one_to_one"` や `"many_to_one"` など、想定する結合関係を検証します。
- 使用例:

```python
stores = pd.DataFrame({
    "store": ["Tokyo", "Osaka"],
    "region": ["Kanto", "Kansai"],
})

enriched = sales.merge(stores, on="store", how="left")
```

- 戻り値: キーに基づいて列を結合した新しい `DataFrame` を返します。
- インパクト: 分析に必要な属性を付け足せます。キー重複があると行数が増殖するため、結合前後の `shape` 確認が重要です。
- よくある注意点:
  - 明細にマスタを付ける用途では、通常 `how="left"` を使い、明細行を落とさないようにします。
  - マスタ側キーが重複していると、1行の明細が複数行に増えます。`validate="many_to_one"` を使うと事故を早期検出できます。
  - キー列の型が左右で違うと結合できない、または期待より欠損が増えます。事前に `dtypes` とユニーク値を確認します。
  - 同名列がある場合は `_x`, `_y` が付くため、必要なら `suffixes=("_sales", "_master")` のように明示します。
- 関連メソッド: `join()`, `concat()`, `set_index()`, `reset_index()`, `duplicated()`

## `join()`

- 基本の説明: 主にインデックスを基準に結合します。
- 実用での使用場面: 同じ日付インデックスを持つ時系列データ、同じIDインデックスを持つ特徴量表を横に結合します。
- 基本構文:

```python
left.join(other, on=None, how="left", lsuffix="", rsuffix="", sort=False)
```

- 主な引数/指定:
  - `other`: 結合する `DataFrame`、`Series`、またはそれらのリストです。
  - `on`: 左側の列をキーにし、右側のインデックスへ結合する場合に指定します。
  - `how`: `"left"`, `"right"`, `"inner"`, `"outer"`, `"cross"` を指定します。
  - `lsuffix`, `rsuffix`: 同名列が衝突したときの接尾辞です。
  - `sort`: 結合キーで結果を並べ替えるかを指定します。
- 使用例:

```python
left = pd.DataFrame({"sales": [100, 120]}, index=["Tokyo", "Osaka"])
right = pd.DataFrame({"orders": [10, 8]}, index=["Tokyo", "Osaka"])

joined = left.join(right)
```

- 戻り値: インデックスまたは指定キーに基づいて横結合した `DataFrame` を返します。
- インパクト: インデックス設計が整っているデータ同士を簡潔に結合できます。
- よくある注意点:
  - `join()` は左結合が既定です。完全一致だけ欲しい場合は `how="inner"` を指定します。
  - 列キー同士の結合が中心なら、`merge()` の方が意図を明示しやすいです。
  - 右側のインデックスに重複があると行数が増える点は `merge()` と同じです。
  - 同名列がある場合、`lsuffix` と `rsuffix` を指定しないとエラーになることがあります。
- 関連メソッド: `merge()`, `set_index()`, `concat()`, `sort_index()`

## `concat()`

- 基本の説明: 複数の `DataFrame` や `Series` を縦または横に連結します。
- 実用での使用場面: 月別ファイルの縦結合、複数特徴量の横結合、分割処理後の再結合に使います。
- 基本構文:

```python
pd.concat(objs, axis=0, join="outer", ignore_index=False, keys=None)
```

- 主な引数/指定:
  - `objs`: 連結する `DataFrame` や `Series` のリストです。
  - `axis`: `0` は縦方向、`1` は横方向に連結します。
  - `join`: 連結軸以外のラベルを `"outer"` で和集合、`"inner"` で共通部分にします。
  - `ignore_index`: `True` なら元インデックスを捨てて連番に振り直します。
  - `keys`: 元データの識別ラベルを付け、階層インデックスにします。
- 使用例:

```python
january = pd.DataFrame({"month": ["Jan"], "sales": [100]})
february = pd.DataFrame({"month": ["Feb"], "sales": [120]})

combined = pd.concat([january, february], ignore_index=True)
```

- 戻り値: 指定方向に連結した `DataFrame` または `Series` を返します。
- インパクト: 分割されたデータを分析可能な1つの表にできます。現行pandasでは `append()` の代替としても使います。
- よくある注意点:
  - 縦結合では列名が一致していないと欠損列が増えます。月別ファイルの列揺れを事前に確認します。
  - `ignore_index=True` を付けないと、元データのインデックスが重複したまま残ることがあります。
  - 横結合ではインデックスで位置合わせされます。単純に行番号順で結合したい場合はインデックスを整えてから実行します。
  - ループ内で1行ずつ `concat()` すると遅くなります。リストに貯めて最後に一度だけ連結します。
- 関連メソッド: `merge()`, `join()`, `reset_index()`, `append()`

## `append()`

- 基本の説明: かつて行を追加するために使われたメソッドです。pandas 2.0以降では削除されています。
- 実用での使用場面: 新規コードでは使いません。古いコードを読むときに、`concat()` に置き換える対象として理解します。
- 基本構文:

```python
# pandas 1.x までの旧形式
df.append(other, ignore_index=False)

# pandas 2.0以降の置き換え
pd.concat([df, other], ignore_index=False)
```

- 主な引数/指定:
  - `other`: 追加する `DataFrame`、`Series`、辞書などでした。
  - `ignore_index`: `True` なら連結後に連番インデックスへ振り直します。
- 使用例:

```python
df = pd.DataFrame({"month": ["Jan"], "sales": [100]})
new_rows = pd.DataFrame({"month": ["Feb"], "sales": [120]})

# 古い書き方: pandas 2.0以降では使えません。
# df = df.append(new_rows, ignore_index=True)

# 現行の推奨
df = pd.concat([df, new_rows], ignore_index=True)
```

- 戻り値: pandas 1.x では行を追加した新しい `DataFrame` を返していました。元の `df` は直接変更されません。
- インパクト: `append()` を残すと現行環境でエラーになります。`concat()` へ移行することで、互換性と保守性が上がります。
- よくある注意点:
  - pandas 2.0以降では `AttributeError` になります。教材や新規コードでは `append()` を書かないようにします。
  - 旧コードの `df = df.append(row)` は、`rows` のリストを作って `pd.concat()` する設計に直すと高速です。
  - `append()` は破壊的変更ではなかったため、戻り値を代入しない旧コードは実質何も変わっていない可能性があります。
- 関連メソッド: `concat()`, `merge()`, `DataFrame()`
