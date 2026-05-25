# 00. メソッド索引

画像に出ている全項目の索引です。重複している項目は、主に説明している章を示しています。

| 項目 | 種別 | 主な章 | 補足 |
|---|---|---|---|
| `Series()` | コンストラクタ | [データ構造](./01_data_structures.md) | 1次元データ |
| `DataFrame()` | コンストラクタ | [データ構造](./01_data_structures.md) | 2次元表データ |
| `read_csv()` | 関数 | [データ生成・読み込み](./02_data_loading_creation.md) | CSV読み込み |
| `read_excel()` | 関数 | [データ生成・読み込み](./02_data_loading_creation.md) | Excel読み込み |
| `read_json()` | 関数 | [データ生成・読み込み](./02_data_loading_creation.md) | JSON読み込み |
| `dict` | Python標準型 | [データ生成・読み込み](./02_data_loading_creation.md) | pandasメソッドではない |
| `head()` | メソッド | [データ確認](./03_data_inspection.md) | 先頭確認 |
| `tail()` | メソッド | [データ確認](./03_data_inspection.md) | 末尾確認 |
| `info()` | メソッド | [データ確認](./03_data_inspection.md) | 型・欠損・メモリ確認 |
| `describe()` | メソッド | [データ確認](./03_data_inspection.md) | 要約統計 |
| `shape` | 属性 | [データ確認](./03_data_inspection.md) | 行数・列数 |
| `columns` | 属性 | [データ確認](./03_data_inspection.md) | 列名一覧 |
| `dtypes` | 属性 | [データ確認](./03_data_inspection.md) | 列ごとの型 |
| `loc[]` | インデクサ | [データ選択](./04_data_selection.md) | ラベル指定 |
| `iloc[]` | インデクサ | [データ選択](./04_data_selection.md) | 位置指定 |
| `at[]` | インデクサ | [データ選択](./04_data_selection.md) | 単一セル・ラベル指定 |
| `iat[]` | インデクサ | [データ選択](./04_data_selection.md) | 単一セル・位置指定 |
| `filter()` | メソッド | [データ選択](./04_data_selection.md), [グルーピング](./06_grouping.md) | DataFrameとGroupByで意味が違う |
| `assign()` | メソッド | [データ操作](./05_data_operations.md) | 派生列作成 |
| `drop()` | メソッド | [データ操作](./05_data_operations.md) | 行・列削除 |
| `rename()` | メソッド | [データ操作](./05_data_operations.md) | 列名・行名変更 |
| `replace()` | メソッド | [データ操作](./05_data_operations.md) | 値の置換 |
| `sort_values()` | メソッド | [インデックス・順序操作](./10_index_sorting.md) | 値で並べ替え |
| `sort_index()` | メソッド | [インデックス・順序操作](./10_index_sorting.md) | インデックスで並べ替え |
| `reset_index()` | メソッド | [インデックス・順序操作](./10_index_sorting.md) | インデックスを列へ戻す |
| `melt()` | メソッド | [データ操作](./05_data_operations.md) | 横持ちから縦持ち |
| `groupby()` | メソッド | [グルーピング](./06_grouping.md) | グループ化 |
| `agg()` | メソッド | [グルーピング](./06_grouping.md) | 複数集計 |
| `apply()` | メソッド | [グルーピング](./06_grouping.md) | 任意関数適用 |
| `transform()` | メソッド | [グルーピング](./06_grouping.md) | 元行数へ戻す集計 |
| `dropna()` | メソッド | [データ整形・欠損処理](./07_data_cleaning.md) | 欠損削除 |
| `fillna()` | メソッド | [データ整形・欠損処理](./07_data_cleaning.md) | 欠損補完 |
| `isna()` | メソッド | [データ整形・欠損処理](./07_data_cleaning.md) | 欠損判定 |
| `interpolate()` | メソッド | [データ整形・欠損処理](./07_data_cleaning.md) | 補間 |
| `duplicated()` | メソッド | [データ整形・欠損処理](./07_data_cleaning.md) | 重複判定 |
| `to_datetime()` | 関数 | [時系列処理](./08_time_series.md) | 日時型変換 |
| `date_range()` | 関数 | [時系列処理](./08_time_series.md) | 日時範囲作成 |
| `resample()` | メソッド | [時系列処理](./08_time_series.md) | 時間粒度変換 |
| `shift()` | メソッド | [時系列処理](./08_time_series.md) | 前後シフト |
| `rolling()` | メソッド | [Window関数](./12_window_functions.md) | 移動窓 |
| `expanding()` | メソッド | [Window関数](./12_window_functions.md) | 累積窓 |
| `mean()` | メソッド | [統計量](./09_statistics.md) | 平均 |
| `median()` | メソッド | [統計量](./09_statistics.md) | 中央値 |
| `mode()` | メソッド | [統計量](./09_statistics.md) | 最頻値 |
| `std()` | メソッド | [統計量](./09_statistics.md) | 標準偏差 |
| `var()` | メソッド | [統計量](./09_statistics.md) | 分散 |
| `min()` | メソッド | [統計量](./09_statistics.md) | 最小値 |
| `max()` | メソッド | [統計量](./09_statistics.md) | 最大値 |
| `count()` | メソッド | [統計量](./09_statistics.md) | 非欠損件数 |
| `set_index()` | メソッド | [インデックス・順序操作](./10_index_sorting.md) | 列をインデックスへ |
| `merge()` | 関数/メソッド | [データ結合](./11_joining_combining.md) | キー結合 |
| `join()` | メソッド | [データ結合](./11_joining_combining.md) | インデックス結合 |
| `concat()` | 関数 | [データ結合](./11_joining_combining.md) | 縦横連結 |
| `append()` | 旧メソッド | [データ結合](./11_joining_combining.md) | pandas 2.0以降では削除 |
| `plot()` | メソッド | [可視化](./13_visualization.md) | 汎用プロット |
| `hist()` | メソッド | [可視化](./13_visualization.md) | ヒストグラム |
| `boxplot()` | メソッド | [可視化](./13_visualization.md) | 箱ひげ図 |
| `scatter_matrix()` | 関数 | [可視化](./13_visualization.md) | `pandas.plotting` 由来 |
| `to_csv()` | メソッド | [出力](./14_export.md) | CSV出力 |
| `to_excel()` | メソッド | [出力](./14_export.md) | Excel出力 |
