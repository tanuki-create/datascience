# 16. 全項目クイックリファレンス

画像にある全項目を、目的、基本構文、実務インパクトで横断的に確認する表です。詳しい説明は各章を参照してください。

| 項目 | 目的 | 基本構文 | 実務インパクト |
|---|---|---|---|
| `Series()` | 1列のラベル付きデータを作る | `pd.Series([1, 2, 3])` | 列単位の計算・欠損処理・時系列処理の基礎になる |
| `DataFrame()` | 表データを作る | `pd.DataFrame({"a": [1, 2]})` | 分析、結合、集計、可視化の中心オブジェクトになる |
| `read_csv()` | CSVを読み込む | `pd.read_csv("file.csv")` | 外部データを分析可能な表に変換する |
| `read_excel()` | Excelを読み込む | `pd.read_excel("file.xlsx")` | 現場の表計算ファイルを自動処理に載せる |
| `read_json()` | JSONを読み込む | `pd.read_json("file.json")` | APIやログのデータを表形式にする |
| `dict` | DataFrame作成元にする | `pd.DataFrame({"a": [1]})` | サンプルデータやマッピングを簡単に作れる |
| `head()` | 先頭を確認する | `df.head()` | 読み込みミス、列ずれ、値の形式を早期に見つける |
| `tail()` | 末尾を確認する | `df.tail()` | 最新データや末尾の異常を確認する |
| `info()` | 型・欠損・メモリを確認する | `df.info()` | 前処理方針を決める初期診断になる |
| `describe()` | 要約統計を出す | `df.describe()` | 外れ値、スケール、分布の概観を掴む |
| `shape` | 行数・列数を返す | `df.shape` | 結合や抽出前後の件数異常を検知する |
| `columns` | 列名を返す | `df.columns` | 列名の表記揺れや不足を確認する |
| `dtypes` | 列ごとの型を返す | `df.dtypes` | 日付・数値・文字列の誤認識を見つける |
| `loc[]` | ラベルで選択する | `df.loc[df["a"] > 0, ["a"]]` | 条件抽出と列選択を明確に書ける |
| `iloc[]` | 位置で選択する | `df.iloc[:5, :2]` | 列名不明の初期確認や位置指定に使える |
| `at[]` | ラベルで単一セルを扱う | `df.at[0, "a"]` | ピンポイントの確認・更新を明示できる |
| `iat[]` | 位置で単一セルを扱う | `df.iat[0, 0]` | 位置が決まったセルを高速に扱える |
| `filter()` | ラベル名で抽出する | `df.filter(regex="sales")` | 多数の列から命名規則で必要列を選べる |
| `assign()` | 派生列を作る | `df.assign(total=df["a"] * 2)` | 元データを壊さず前処理を再現しやすくする |
| `drop()` | 行・列を削除する | `df.drop(columns=["a"])` | 不要な情報を落として処理対象を明確にする |
| `rename()` | 行名・列名を変更する | `df.rename(columns={"old": "new"})` | 列名を標準化して後工程を安定させる |
| `replace()` | 値を置換する | `df.replace({"N/A": pd.NA})` | 表記揺れや欠損表現を統一する |
| `sort_values()` | 値で並べ替える | `df.sort_values("sales")` | ランキング、異常値確認、レポート整形に効く |
| `sort_index()` | インデックスで並べ替える | `df.sort_index()` | 時系列やID順の前提を整える |
| `reset_index()` | インデックスを列へ戻す | `df.reset_index()` | 集計結果を通常の表として扱える |
| `melt()` | 横持ちを縦持ちにする | `df.melt(id_vars="id")` | 可視化・集計・機械学習で扱いやすい粒度にする |
| `groupby()` | グループに分ける | `df.groupby("store")` | 店舗別・商品別などの集計の起点になる |
| `agg()` | 複数集計する | `df.groupby("store").agg(total=("sales", "sum"))` | レポート指標をまとめて作れる |
| `apply()` | 任意関数を適用する | `df.groupby("store").apply(func)` | 複雑な独自処理を書けるが速度には注意が必要 |
| `transform()` | 元行数に戻る集計をする | `df.groupby("store")["sales"].transform("sum")` | 明細行にグループ指標を付与できる |
| `GroupBy.filter()` | グループ単位で残す | `df.groupby("store").filter(lambda g: len(g) > 1)` | 分析対象グループの品質を揃えられる |
| `dropna()` | 欠損を削除する | `df.dropna(subset=["date"])` | 計算不能な行を除外し、エラーや誤集計を防ぐ |
| `fillna()` | 欠損を補完する | `df.fillna({"qty": 0})` | 欠損を残せない処理へ進める |
| `isna()` | 欠損を判定する | `df.isna().sum()` | 欠損の量と場所を把握できる |
| `interpolate()` | 欠損を補間する | `s.interpolate()` | 連続値や時系列の自然な欠損補完に使える |
| `duplicated()` | 重複を判定する | `df.duplicated(subset=["id"])` | 二重計上や重複レコードを検知する |
| `to_datetime()` | 日時型に変換する | `pd.to_datetime(df["date"])` | 期間抽出、時系列集計、日付ソートを正しくする |
| `date_range()` | 日時範囲を作る | `pd.date_range("2026-01-01", periods=7)` | カレンダー作成や欠損日補完に使える |
| `resample()` | 時間粒度を変える | `df.set_index("date").resample("ME").sum()` | 日次から月次などKPI粒度を変換できる |
| `shift()` | 値を前後にずらす | `s.shift(1)` | 前日比、前月比、ラグ特徴量を作れる |
| `rolling()` | 移動窓を作る | `s.rolling(7).mean()` | 移動平均や移動標準偏差で傾向を見る |
| `expanding()` | 累積窓を作る | `s.expanding().mean()` | 累積平均や開始以来の推移を見られる |
| `mean()` | 平均を出す | `df["x"].mean()` | 代表値を素早く確認する |
| `median()` | 中央値を出す | `df["x"].median()` | 外れ値に強い代表値を得る |
| `mode()` | 最頻値を出す | `df["x"].mode()` | よく出るカテゴリや値を把握する |
| `std()` | 標準偏差を出す | `df["x"].std()` | ばらつきや安定性を把握する |
| `var()` | 分散を出す | `df["x"].var()` | ばらつきの理論的評価に使う |
| `min()` | 最小値を出す | `df["x"].min()` | 下限や異常値を確認する |
| `max()` | 最大値を出す | `df["x"].max()` | 上限や突出値を確認する |
| `count()` | 非欠損件数を数える | `df["x"].count()` | 有効データ数を確認する |
| `set_index()` | 列をインデックスにする | `df.set_index("date")` | 時系列処理やラベル抽出の前提を作る |
| `merge()` | キーで結合する | `left.merge(right, on="id", how="left")` | 明細にマスタや属性を付与できる |
| `join()` | インデックスで結合する | `left.join(right)` | 同じインデックスを持つ表を簡潔に結合する |
| `concat()` | 縦横に連結する | `pd.concat([df1, df2])` | 分割ファイルや特徴量をまとめる |
| `append()` | 旧式の行追加 | `pd.concat([df, new_rows])` | 古いコードを現行pandasへ移行する判断材料になる |
| `plot()` | グラフを描く | `df.plot()` | 集計結果の傾向をすぐ確認できる |
| `hist()` | ヒストグラムを描く | `df["x"].hist()` | 分布、偏り、外れ値を確認できる |
| `boxplot()` | 箱ひげ図を描く | `df.boxplot(column="x", by="group")` | グループ間のばらつきや外れ値を比較できる |
| `scatter_matrix()` | 散布図行列を描く | `scatter_matrix(df)` | 数値列同士の関係をまとめて探索できる |
| `to_csv()` | CSVへ保存する | `df.to_csv("out.csv", index=False)` | 他システム連携や軽量な共有に使える |
| `to_excel()` | Excelへ保存する | `df.to_excel("out.xlsx", index=False)` | 非エンジニアへの共有やレビューに使いやすい |

## 全体で特に重要な注意点

- `append()` は現行pandasでは使わず、`pd.concat()` に置き換えます。
- `shape`、`columns`、`dtypes` は `()` を付けない属性です。
- `loc[]` はラベル、`iloc[]` は位置で選択します。
- `filter()` は値の条件抽出ではなく、主にラベル名での抽出です。値の条件抽出は `loc[]` を使います。
- `groupby().apply()` は便利ですが遅くなりやすいため、まず `agg()` や `transform()` で書けるか確認します。
- `merge()` の前後では `shape` を確認します。キー重複で行数が増える事故がよくあります。
- `to_excel()` は `openpyxl` などのExcelライターが必要になる場合があります。
