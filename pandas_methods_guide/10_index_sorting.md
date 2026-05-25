# 10. インデックス・順序操作

インデックスはpandasの行ラベルです。結合、時系列、抽出、整列の基準になるため、分析の土台として重要です。

## `set_index()`

- 基本の説明: 指定した列をインデックスにします。
- 実用での使用場面: 日付を時系列インデックスにする、IDを行ラベルにする、複合キーで管理する場面で使います。
- 基本構文:

```python
df.set_index(keys, drop=True, append=False, inplace=False, verify_integrity=False)
```

- 主な引数/指定:
  - `keys`: インデックスにする列名。複数列ならリストで指定します。
  - `drop`: `True` の場合、インデックス化した列を通常列から削除します。
  - `append`: 既存インデックスに追加して階層インデックスを作るかを指定します。
  - `inplace`: `True` なら元の `DataFrame` を直接変更します。
  - `verify_integrity`: `True` なら重複インデックスがないか検証します。
- 使用例:

```python
indexed = sales.set_index("date")
multi_indexed = sales.set_index(["store", "product"])
```

- 戻り値: 通常はインデックスを変更した新しい `DataFrame` を返します。`inplace=True` の場合は `None` です。
- インパクト: ラベル指定の抽出、時系列処理、結合がしやすくなります。
- よくある注意点:
  - インデックスは一意でなくても設定できます。結合や抽出で意図しない複数行が返る場合があるため、IDとして使う列は重複確認が必要です。
  - 日付列を時系列インデックスにする場合は、先に `pd.to_datetime()` で日時型へ変換します。
  - `inplace=True` は処理の流れが追いにくくなるため、教材や分析ノートでは代入して使う方が安全です。
- 関連メソッド: `reset_index()`, `sort_index()`, `loc[]`, `merge()`, `join()`

## `reset_index()`

- 基本の説明: インデックスを列に戻します。
- 実用での使用場面: 集計後の結果を通常の表に戻す、CSV出力前にインデックスを列として保存する場面で使います。
- 基本構文:

```python
df.reset_index(drop=False, inplace=False, names=None)
```

- 主な引数/指定:
  - `drop`: `True` の場合、インデックスを列として残さず破棄します。
  - `inplace`: `True` なら元の `DataFrame` を直接変更します。
  - `names`: 戻したインデックス列の列名を指定します。
- 使用例:

```python
summary = sales.groupby("store")["price"].mean().reset_index(name="avg_price")
```

- 戻り値: インデックスを通常列へ戻した `DataFrame` を返します。`Series.reset_index(name=...)` では値列の名前も指定できます。
- インパクト: 集計結果を他のデータと結合しやすくなります。
- よくある注意点:
  - `groupby()` 後の結果はインデックスにキーが入ることが多いため、出力や結合前に `reset_index()` が必要になる場合があります。
  - 元のインデックスが不要な連番なら `drop=True` を指定しないと、`index` という列が余分に増えます。
  - `MultiIndex` をリセットすると複数の列に戻ります。必要な階層だけ戻したい場合は `level` を指定します。
- 関連メソッド: `set_index()`, `groupby()`, `agg()`, `to_csv()`, `to_excel()`

## `sort_index()`

- 基本の説明: インデックスの順番で並べ替えます。
- 実用での使用場面: 日付順、ID順、階層インデックス順に整理します。
- 基本構文:

```python
df.sort_index(axis=0, ascending=True, inplace=False, level=None)
```

- 主な引数/指定:
  - `axis`: `0` は行インデックス、`1` は列名の並べ替えです。
  - `ascending`: 昇順か降順かを指定します。
  - `level`: `MultiIndex` のどの階層で並べるかを指定します。
  - `inplace`: `True` なら元の `DataFrame` を直接変更します。
- 使用例:

```python
ordered = sales.set_index("date").sort_index()
```

- 戻り値: インデックス順に並べ替えた `DataFrame` または `Series` を返します。
- インパクト: 時系列や比較処理で前後関係を明確にできます。
- よくある注意点:
  - 時系列処理ではインデックスが昇順に並んでいないと、差分・移動平均・期間抽出の結果を誤解しやすくなります。
  - 文字列の日付インデックスは辞書順で並びます。日付として扱うなら日時型にしてから並べます。
  - 値の大小で並べたい場合は `sort_values()` を使います。
- 関連メソッド: `set_index()`, `sort_values()`, `resample()`, `rolling()`

## `sort_values()`

- 基本の説明: 列の値に基づいて並べ替えます。
- 実用での使用場面: 売上順、日付順、スコア順、優先度順に表示します。
- 基本構文:

```python
df.sort_values(by, ascending=True, na_position="last", inplace=False)
```

- 主な引数/指定:
  - `by`: 並べ替えに使う列名。複数列ならリストで指定します。
  - `ascending`: 昇順か降順かを指定します。複数列ではリストで列ごとに指定できます。
  - `na_position`: 欠損値を `"first"` と `"last"` のどちらに置くかを指定します。
  - `inplace`: `True` なら元の `DataFrame` を直接変更します。
- 使用例:

```python
ordered = sales.sort_values(["store", "price"], ascending=[True, False])
```

- 戻り値: 指定列の値で並べ替えた `DataFrame` または `Series` を返します。
- インパクト: ランキング、異常値確認、レポート作成の見やすさが上がります。
- よくある注意点:
  - 数値列が文字列型になっていると、`"100"` より `"20"` が後に来るような辞書順の並びになります。必要に応じて型変換します。
  - 並べ替え後も元のインデックスは保持されます。連番に戻したい場合は `.reset_index(drop=True)` を続けます。
  - 複数列で並べる場合、先に指定した列から優先して並びます。
- 関連メソッド: `sort_index()`, `reset_index()`, `rank()`, `nlargest()`, `nsmallest()`
