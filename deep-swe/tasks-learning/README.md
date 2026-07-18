# DeepSWE 学習用 instruction 集

生成日時：2026-07-09 11:09:53 JST

このフォルダは、`tasks/` 配下の 113 件のベンチマーク課題から、学習の入口になる `instruction.md` だけを抜き出したものです。

元の `tasks/` にはテスト、Docker 環境、参照解答が含まれます。
このフォルダでは、課題ごとに問題文・初学者向け解説・解法ガイドを同じディレクトリにまとめています。解法ガイドは自力で考えた後に読んでください。

## instruction.md を見ればよいか

最初に見るファイルは `instruction.md` で合っています。

`instruction.md` は、ベンチマーク上でエージェントに渡される課題文です。
何を直すか、どの挙動を満たすか、公開 API をどう保つかが書かれています。

ただし、学習では `instruction.md` だけで完結させないほうがよいです。
実装前に `task.toml` で対象リポジトリ、言語、base commit を確認します。
行き詰まった後に `tests/test.patch` を読むと、課題文のどの条件が採点されるかを確認できます。
`solution/solution.patch` は参照解答なので、最初には読まず、最後に自分の設計と比較するために使います。

## 推奨する読み方

1. `<task-id>/instruction.md` を読む。
2. `<task-id>/beginner.ja.md` の「中心アイデア」で、設計上そろえる対象を確認する。
3. 原文の要求を「入力」「期待する出力」「守るべき既存仕様」「公開 API」に分ける。
4. 元の `tasks/<task-id>/task.toml` で対象リポジトリ、言語、base commit を確認する。
5. 実装方針を立ててから、必要に応じて `tasks/<task-id>/tests/test.patch` を読む。
6. 行き詰まった後、または自力実装後に `<task-id>/solution.ja.md` を読む。
7. 最後に `tasks/<task-id>/solution/solution.patch` を見て、設計差分を復習する。

## フォルダ構成

```text
tasks-learning/
  README.md
  index.md
  <task-id>/
    instruction.md
    beginner.ja.md
    solution.ja.md
```

## 言語別件数

| language | count |
| --- | ---: |
| go | 34 |
| javascript | 5 |
| python | 34 |
| rust | 5 |
| typescript | 35 |

## カテゴリ別件数

| category | count |
| --- | ---: |
| bugfix | 4 |
| enhancement | 3 |
| feature_request | 106 |

## 例：abs-module-cache-flags の読み方

この課題は ABS という言語処理系のモジュール読み込みを堅牢にする問題です。

初心者は、まず「同じファイルを別のパスで `require()` したときに、キャッシュが二重にならないようにする」と読み替えると入口が見えます。
次に、`ABS_MODULE_PATH`、循環 import、デバッグ出力、CLI フラグという周辺仕様を分けて読みます。
全部を一つの if 文で処理するのではなく、解決処理、キャッシュ管理、循環検出、CLI オプション解析を別の責務として見るのが自然です。

この種の課題では、`instruction.md` の箇条書きはほぼ受け入れ条件です。
実装を始める前に、各条件を「どの入力で」「どの観測結果なら成功か」に変換すると学習しやすくなります。
