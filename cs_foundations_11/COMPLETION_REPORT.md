# CS基礎11分野 教科書セット完了報告

集計基準: 2026-08-27 JST。行数とbytesはUTF-8 Markdown本体に対する `wc -l -c` の実値である。

## 成果物

| # | ファイル | 構成 | 章数 | 行数 | bytes |
|---:|---|---:|---:|---:|---:|
| 1 | `books/01_algorithms.md` | 指定15章＋誤判断章＋専門家付録 | 16 | 985 | 61,545 |
| 2 | `books/02_discrete_math.md` | 指定15章＋誤判断章＋専門家付録 | 16 | 981 | 56,145 |
| 3 | `books/03_automata_computability.md` | 指定16章＋誤判断章＋専門家付録 | 17 | 1,045 | 66,062 |
| 4 | `books/04_programming_languages.md` | 指定20章＋誤判断章＋専門家付録 | 21 | 774 | 53,039 |
| 5 | `books/05_operating_systems.md` | 指定23章＋誤判断章＋専門家付録 | 24 | 651 | 51,656 |
| 6 | `books/06_concurrency_distributed.md` | 指定30章＋誤判断章＋専門家付録 | 31 | 1,065 | 83,004 |
| 7 | `books/07_database.md` | 指定28章＋誤判断章＋専門家付録 | 29 | 1,106 | 77,840 |
| 8 | `books/08_probability_statistics.md` | 指定28章＋誤判断章＋専門家付録 | 29 | 1,657 | 84,120 |
| 9 | `books/09_software_engineering.md` | 指定32章＋誤判断章＋専門家付録 | 33 | 1,879 | 99,248 |
| 10 | `books/10_hci.md` | 指定29章＋誤判断章＋専門家付録 | 30 | 1,014 | 80,082 |
| 11 | `books/11_security.md` | 指定39章＋誤判断章＋専門家付録 | 40 | 1,488 | 103,544 |
|  | **総計** | **指定275章＋誤判断11章＋専門家付録11本** | **286** | **12,645** | **816,285** |

## 要件達成状況

| 要件 | 状況 | 確認内容 |
|---|---|---|
| 指定章＋最終誤判断章 | 達成 | 11冊すべて章番号が1から連続し、最後の番号付き章は「この分野を知らないエンジニアが陥りやすい誤判断」。各最終章は20例以上を収録。 |
| 章末問題 | 達成 | 全286章に要点、誤解チェック、基礎問題、応用問題、設計問題、調査課題を配置。検査scriptは基礎section内5問以上、応用section内3問以上を個別確認する。 |
| 数章ごとの総合演習 | 達成 | 各冊に3〜6か所、単独章の知識だけでは解けない横断演習を配置。 |
| 正式定義・図・数式・code | 達成 | 適用可能な章で形式定義、ASCII図、数式、Python/C/Rust/SQLまたは疑似codeを使用。 |
| 一次資料・参考文献 | 達成 | 全冊に参考文献sectionと調査課題を配置。言語仕様、Linux kernel/man-pages、論文、RFC、W3C、NIST、DB公式文書等への導線を収録し、時点依存資料は2026-08-27時点で確認。 |
| 相互参照 | 達成 | 各章の次章接続に加え、`README.md` に11冊の履修順、領域横断図、横断障害分析表を収録。 |
| 専門家の思考を測る付録 | 達成 | 全11冊の真の書末に、分野固有の中核的メンタルモデル5件、両陣営をsteelmanした根本論争3件、暗記では答えられない質問10件を収録。執筆担当とは別の担当がクロスレビュー。 |
| 未完成marker | なし | 教科書本文に `TODO`、`TBD`、`PLACEHOLDER` なし。 |

## 検証記録

実行directoryは `cs_foundations_11` の親directory。

```bash
python3 cs_foundations_11/tools/verify_books.py
```

結果:

```text
OK: 11 books, 286 numbered chapters, required work sections and 5/3/10 expert appendices present
```

この検査はREADMEの11冊へのlocal link、file存在、章番号・章数、最終誤判断章、総合演習、章末必須label、基礎5問・応用3問、最終章20例、巻末付録の5/3/10項目と最終配置、未完成marker、本文長、code fence parityを確認する。

集計と追加検査:

```bash
wc -l -c cs_foundations_11/books/*.md
rg -c '^##.*第[0-9]+章' cs_foundations_11/books/*.md
rg -n '\b(TODO|TBD|PLACEHOLDER)\b' cs_foundations_11/books/*.md
# 各fileの ^``` 出現数を2で割り、余りを検査
```

結果は総計12,645行・816,285 bytes・286章・専門家付録11本、未完成marker 0件、code fenceの奇数file 0件である。

構造検査は内容の真偽を自動証明しない。そのため、分野別レビューでは評価戦略・型/効果/variance、page fault・scheduler・fsync・container、CAP/Raft/exactly-once、WCAG 2.2、統計的推論、DB隔離、security標準など高誤解領域を重点的に一次資料と照合した。
