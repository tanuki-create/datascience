# Pandasの必須メソッド解説

このフォルダは、画像「Pandasの必須メソッド」を元に、pandasの主要メソッド・属性・インデクサを章立てで整理した教材です。各項目ごとに、基本の説明、実用での使用場面、使用例、インパクトをまとめています。

## 前提

- 想定バージョン: pandas 3.x 系を中心に説明
- `append()` は pandas 2.0 以降で削除済みのため、現行コードでは `concat()` を使う前提で説明
- 画像内の `data_range()` は `date_range()` の誤記として扱う
- `dict` は pandas メソッドではなく Python 標準のデータ構造として扱う
- `shape`、`columns`、`dtypes` はメソッドではなく属性として扱う
- `loc[]`、`iloc[]`、`at[]`、`iat[]` はメソッドではなくインデクサとして扱う
- `filter()` は `DataFrame.filter()` と `GroupBy.filter()` で意味が異なるため、該当章で分けて説明

## 章構成

0. [メソッド索引](./00_method_index.md)
1. [データ構造](./01_data_structures.md)
2. [データ生成・読み込み](./02_data_loading_creation.md)
3. [データ確認](./03_data_inspection.md)
4. [データ選択](./04_data_selection.md)
5. [データ操作](./05_data_operations.md)
6. [グルーピング](./06_grouping.md)
7. [データ整形・欠損処理](./07_data_cleaning.md)
8. [時系列処理](./08_time_series.md)
9. [統計量](./09_statistics.md)
10. [インデックス・順序操作](./10_index_sorting.md)
11. [データ結合](./11_joining_combining.md)
12. [Window関数](./12_window_functions.md)
13. [可視化](./13_visualization.md)
14. [出力](./14_export.md)
15. [実務ワークフロー例](./15_practical_workflow.md)
16. [全項目クイックリファレンス](./16_quick_reference.md)

## 各項目の読み方

各章では、できるだけ次の観点で説明します。

- 基本の説明: 何をする項目か
- 基本構文: 最小の書き方
- 実用での使用場面: 現場でいつ使うか
- 使用例: 動くコード例
- インパクト: 品質、速度、再現性、分析精度への影響
- 注意点: 初学者が誤りやすい点、pandasのバージョン差、戻り値の違い

## 学習順の目安

1. `Series()` と `DataFrame()` でpandasの表現を理解する
2. `read_csv()`、`head()`、`info()`、`dtypes` でデータを読む
3. `loc[]`、`assign()`、`dropna()`、`fillna()` で前処理する
4. `groupby()`、`agg()`、`merge()`、`concat()` で分析用データを作る
5. `to_datetime()`、`resample()`、`rolling()` で時系列を扱う
6. `plot()`、`to_csv()`、`to_excel()` で確認・共有する

## 実行できるサンプル

- サンプルCSV: [examples/sales.csv](./examples/sales.csv)
- ワークフローコード: [examples/practical_workflow.py](./examples/practical_workflow.py)

```bash
python pandas_methods_guide/examples/practical_workflow.py
```

## 共通サンプルデータ

各章の例では、必要に応じて次のような販売データを使います。

```python
import pandas as pd

sales = pd.DataFrame({
    "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
    "store": ["Tokyo", "Tokyo", "Osaka", "Osaka"],
    "product": ["A", "B", "A", "B"],
    "quantity": [10, 4, 7, None],
    "price": [1200, 2500, 1200, 2500],
})
```

## 公式リファレンス

- pandas API reference: https://pandas.pydata.org/docs/reference/
- DataFrame reference: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- pandas 3.0 release notes: https://pandas.pydata.org/docs/whatsnew/v3.0.0.html
- `append()` deprecation note: https://pandas.pydata.org/docs/whatsnew/v1.4.0.html#deprecated-dataframe-append-and-series-append
