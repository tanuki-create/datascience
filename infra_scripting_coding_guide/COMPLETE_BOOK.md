# インフラエンジニアのためのスクリプト言語・コーディング実践解説書（合本）

**状態: 全て完了（FINAL）**

本ファイルは、分冊（README、第1章〜第16章、付録A〜C）を読み順に結合した完成本である。
編集・差分管理は分冊側を正とする。
サンプルコードの実行可能ファイルは `samples/` 配下、テストは `tests/` 配下を参照する。

---



<!-- SOURCE: README.md -->

# インフラエンジニアのためのスクリプト言語・コーディング実践解説書

**状態: 全て完了（FINAL）**

| 読み方 | ファイル |
|--------|----------|
| 一冊で通読 | [COMPLETE_BOOK.md](COMPLETE_BOOK.md) |
| 完了確認 | [COMPLETE.md](COMPLETE.md) |
| 目次・環境・opsctl仕様 | 本ファイル |

本書は、Python 3、Bash、PowerShell 7を使い、運用作業を自動化するスクリプトを、要件整理から安全な実装、テスト、共同開発まで一貫して書くための解説書である。

動くだけのコードではなく、入力検証、エラー処理、ログ、終了コード、dry-run、再実行性、秘密情報の分離を備えたコードを書ける状態を到達点とする。

## 想定読者

- プログラミング経験が少ないインフラエンジニア
- 手作業の運用を自動化したい人
- 他人が保守できるスクリプトを書きたい人
- Python、Bash、PowerShellの使い分けに迷っている人

## 対象言語と前提

| 言語 | 前提バージョン | 主な実行環境 |
|------|----------------|--------------|
| Python | 3.11以上を推奨（3.9以上で動作する例を中心） | Linux、macOS、Windows |
| Bash | Bash 4.x以上（一部はBash 3.xでも可） | Linux、macOS。WindowsではWSLやGit Bash |
| PowerShell | PowerShell 7.4以上を中心 | Windows、Linux、macOS。必要に応じてWindows PowerShell 5.1との差異を注記 |

サンプルコードは学習用である。本番環境へ投入する前に、対象システムでの検証、権限の最小化、変更管理手順の確認を行うこと。

破壊的操作（削除、上書き、再起動、権限変更）を含む例には警告を付ける。dry-runを省略せず、確認なしで本番へ適用しない。

## 本書の読み方

第1章から第2章で、スクリプトの基本と問題分解の作法を固める。

第3章から第9章で、三言語の文法と実務パターン（データ、制御、関数、ファイル、プロセス、エラー、ログ）を比較しながら積む。

第10章から第14章で、セキュリティ、API、CLI設計、テスト、保守性を扱う。

第15章で運用題材を実装し、第16章でGitと共同開発に接続する。

各章は次の要素を含む。

1. 学習目標
2. 基本概念
3. 最小構成のコード
4. 実務向けに改善したコード
5. 悪いコードの例と問題点
6. 改善後のコード
7. セキュリティ上の注意点
8. テスト方法
9. 章末問題と解答
10. 実装演習

---

## 詳細目次

### 導入（本ファイル）

- 目的と想定読者
- 対象言語と前提
- 各章の到達目標
- 開発環境の準備
- 言語選択の指針
- 全体を通すサンプルツール `opsctl` の仕様
- ディレクトリ構成

### 第1章 スクリプトとプログラミングの基本

ファイル: [01_script_and_programming_basics.md](01_script_and_programming_basics.md)

- スクリプトとは何か
- コンパイル言語との違い、インタープリター、ソースコード
- 標準入力、標準出力、標準エラー、終了コード
- 環境変数、コマンドライン引数
- 手作業を自動化する際の考え方
- 自動化すべき作業とすべきでない作業

### 第2章 問題分解とアルゴリズム

ファイル: [02_problem_decomposition_and_algorithms.md](02_problem_decomposition_and_algorithms.md)

- 入力、処理、出力と要件整理
- 処理の分割、疑似コード、フローチャート
- 条件分岐、反復、状態、関数、再利用
- 計算量の基礎、エッジケース、失敗時の挙動

### 第3章 データ型とデータ構造

ファイル: [03_data_types_and_structures.md](03_data_types_and_structures.md)

- 文字列、整数、小数、真偽値
- 配列とリスト、辞書とハッシュテーブル、null相当値
- 型変換、文字コード、日付と時刻
- JSON、CSV、YAMLの概要（三言語比較）

### 第4章 制御構文

ファイル: [04_control_flow.md](04_control_flow.md)

- if、switch/case、for、while、break、continue
- 条件式、比較演算子、論理演算子
- ネストを深くしない方法、早期リターン、異常系を先に処理する方法

### 第5章 関数とモジュール

ファイル: [05_functions_and_modules.md](05_functions_and_modules.md)

- 関数の目的、引数、戻り値、スコープ、副作用、純粋関数
- モジュール化、名前空間、責務の分離、分割判断
- Pythonモジュール、Bash関数、PowerShell関数とモジュール

### 第6章 ファイル操作

ファイル: [06_file_operations.md](06_file_operations.md)

- テキストとバイナリ、読み書き追記、ディレクトリ、検索、権限
- 一時ファイル、ファイルロック、大容量ファイル
- 文字コード、改行コード、安全な更新、バックアップ後の変更

### 第7章 コマンド実行とプロセス制御

ファイル: [07_command_and_process.md](07_command_and_process.md)

- 外部コマンド実行、引数の安全な受け渡し
- stdout/stderr取得、終了コード、タイムアウト、並列実行
- シェルインジェクション対策
- Python subprocess、Bashのパイプとリダイレクト、PowerShellパイプライン

### 第8章 エラー処理

ファイル: [08_error_handling.md](08_error_handling.md)

- エラーの種類、例外、終了コード
- try/except/finally、trap、try/catch/finally
- リトライ、指数バックオフ、タイムアウト
- 握りつぶし禁止、部分成功、ロールバック、利用者向けと調査用エラー

### 第9章 ログ

ファイル: [09_logging.md](09_logging.md)

- printとログの違い、ログレベル、タイムスタンプ、実行ID
- 構造化ログ、JSONログ、ローテーション
- 秘密情報のマスキング、調査可能なログ、過剰ログの抑制

### 第10章 入力値検証とセキュリティ

ファイル: [10_validation_and_security.md](10_validation_and_security.md)

- 型、必須、範囲、パス検証
- コマンドインジェクション、パストラバーサル、権限、秘密情報
- 環境変数、シークレット管理、TLS検証、安全でない一時ファイル
- 最小権限、監査ログ

### 第11章 APIとネットワーク処理

ファイル: [11_api_and_network.md](11_api_and_network.md)

- HTTP、REST、メソッド、ステータスコード、JSON、認証
- タイムアウト、リトライ、ページネーション、レート制限、TLS
- Python、PowerShell、curl（Bash）による呼び出し例

### 第12章 設定ファイルとCLIツール

ファイル: [12_config_and_cli.md](12_config_and_cli.md)

- 設定とコードの分離、JSON/YAML/TOML/環境変数
- 引数、ヘルプ、サブコマンド、デフォルト、優先順位
- 終了コード、dry-run、verbose、quiet、実行結果サマリー

### 第13章 テストと品質管理

ファイル: [13_testing_and_quality.md](13_testing_and_quality.md)

- ユニット、結合、正常系、異常系、境界値、モック、テストデータ
- pytest、Pester、Bashのテスト
- 静的解析、型ヒント、lint、フォーマッター、コードレビュー、CI

### 第14章 保守しやすいコード

ファイル: [14_maintainable_code.md](14_maintainable_code.md)

- 命名、関数の長さ、責務、重複排除、コメント、ドキュメント
- マジックナンバー、設定値、依存関係、バージョン固定
- 後方互換性、非推奨、リファクタリング、技術的負債

### 第15章 インフラ自動化の実践

ファイル: [15_infrastructure_automation_practice.md](15_infrastructure_automation_practice.md)

次の題材を、言語適性を踏まえて実装する。

1. 複数サーバーへの疎通確認
2. ディスク使用率監視
3. ログファイル検索
4. 古いファイルの整理
5. ユーザーアカウント棚卸し
6. サービス稼働確認
7. 設定ファイルの一括変更
8. APIから情報を取得してCSVに出力
9. バックアップ処理
10. 証明書期限確認
11. 定期レポート生成

各実装は要件、入出力、処理フロー、エラー処理、ログ、設定、dry-run、再実行性、テスト、実行例、運用上の注意点を含む。

### 第16章 Gitと共同開発

ファイル: [16_git_and_collaboration.md](16_git_and_collaboration.md)

- バージョン管理、リポジトリ、commit、branch、merge、pull request
- コンフリクト、.gitignore、秘密情報の除外
- コードレビュー、リリースタグ、ロールバック、README、CHANGELOG

### 付録

- [A_language_selection.md](A_language_selection.md): 言語選択の詳細比較
- [B_exit_codes.md](B_exit_codes.md): 終了コードの推奨表
- [C_checklist.md](C_checklist.md): 本番投入前チェックリスト

---

## 各章の到達目標

| 章 | 到達目標 |
|----|----------|
| 1 | 標準入出力、終了コード、環境変数、引数を使い、手作業を入出力に分解できる |
| 2 | 要件を疑似コードと処理単位に落とし、エッジケースと失敗時挙動を先に書ける |
| 3 | 三言語で基本型とJSON/CSVを扱い、型と文字コードの差を説明できる |
| 4 | 浅い制御構造で正常系と異常系を分離し、早期リターンで読める分岐を書ける |
| 5 | 副作用を意識して関数を分割し、モジュールとして再利用できる |
| 6 | 文字コードと改行を踏まえ、バックアップと原子的更新でファイルを安全に更新できる |
| 7 | シェルインジェクションを避け、終了コードとタイムアウト付きで外部コマンドを呼べる |
| 8 | 例外と終了コードを使い分け、リトライとロールバック方針を決められる |
| 9 | 実行ID付きの構造化ログを出し、秘密情報をマスクできる |
| 10 | 入力検証とパス検証を行い、秘密情報をコード外で扱える |
| 11 | 認証付きHTTP呼び出しをタイムアウトとリトライ付きで実装できる |
| 12 | dry-runと設定優先順位を持つCLIを設計できる |
| 13 | 正常系・異常系・境界値のテストを書き、静的解析をCIに載せられる |
| 14 | 命名と責務分離で、変更しやすいスクリプトをレビューできる |
| 15 | 運用題材を言語適性に応じて実装し、再実行可能に運用できる |
| 16 | 秘密情報を除外したGit運用と、レビュー可能な変更単位で共同開発できる |

---

## 開発環境

### 共通

- Git 2.40以上
- テキストエディタ（Visual Studio Code、Cursorなど）
- ターミナル（Linux/macOSの標準端末、Windows Terminal）

### Python

```bash
python3 --version   # 3.11以上を推奨
python3 -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

本書リポジトリ内の `infra_scripting_coding_guide/.venv` は `.gitignore` 対象である。サンプル実行時はこの仮想環境の Python を使う。

推奨パッケージ（本書の例で使用）:

```text
pytest>=8.0
ruff>=0.6
mypy>=1.10
PyYAML>=6.0
requests>=2.32
httpx>=0.27
```

### Bash

```bash
bash --version   # 4.x以上を推奨
shellcheck --version   # 静的解析用。未導入なら OS のパッケージで導入
```

macOSの `/bin/bash` は古い場合がある。Homebrewの `bash` を使うか、Linux/WSLで検証する。

### PowerShell

```powershell
pwsh --version   # 7.4以上を推奨
```

Windows PowerShell 5.1との差が重要な箇所は本文で注記する。本書の主対象は PowerShell 7（`pwsh`）である。

Pester（テスト）:

```powershell
Install-Module -Name Pester -MinimumVersion 5.5 -Scope CurrentUser -Force
```

### OS差異への注意

| 項目 | Linux / macOS | Windows |
|------|---------------|---------|
| パス区切り | `/` | `\`（PowerShellでは `/` も多くの場面で可） |
| 改行 | LF | CRLFが多い。Gitの `core.autocrlf` に注意 |
| 実行権限 | `chmod +x` | 実行ポリシー（`Get-ExecutionPolicy`） |
| シェル | Bashが標準に近い | PowerShellが標準。BashはWSL等 |
| ルート相当 | root / sudo | Administrator / UAC |

---

## 言語選択の指針

優劣ではなく用途適性で選ぶ。詳細は付録Aに譲り、ここでは判断軸だけ示す。

| 観点 | Bash | PowerShell | Python |
|------|------|------------|--------|
| 対象OS | Linux/macOS中心 | Windows中心、7ならクロス | クロスプラットフォーム |
| 処理の複雑さ | 短い糊付け向き | オブジェクトパイプライン向き | 中〜大規模ロジック向き |
| 外部コマンド連携 | 強い | Windows管理との連携が強い | subprocessで可能だが厚め |
| データ加工 | テキスト向き、複雑な構造は弱い | オブジェクトとCSV/JSONが扱いやすい | 強い |
| API操作 | curlで可能 | `Invoke-RestMethod` が便利 | ライブラリが豊富でテストしやすい |
| 可搬性 | シェル差に注意 | 7なら広い。5.1はWindows限定 | 高い |
| テスト容易性 | 工夫が必要 | Pesterで可能 | pytestが成熟 |
| 保守性 | 長大化すると落ちやすい | モジュール化で伸ばせる | モジュールと型で伸ばしやすい |
| 実行環境準備 | ほぼ標準装備 | Windowsは標準、他は導入 | ランタイムとvenvが必要 |
| チームスキル | インフラ層で共通しやすい | Windows運用チーム向き | 開発経験があると速い |

選定の目安:

1. 1ファイル数十行以内のLinuxコマンド糊付け → Bash
2. Windowsのサービス、レジストリ、AD、イベントログ → PowerShell
3. JSON加工、API連携、複雑な分岐、テスト必須 → Python
4. 迷ったら、保守期間とテスト要否で決める。短期使い捨てならBash/PowerShell、半年以上触るならPythonを優先検討する

---

## 全体を通すサンプルツール: `opsctl`

本書では、章が進むにつれて機能を足していく共通ツール **opsctl**（Operations Control）を使う。

`opsctl` は、ホスト一覧と設定ファイルを入力に、疎通確認、ディスク監視、ログ検索、証明書期限確認などの運用タスクを実行するCLIである。同じ仕様を Python 実装を主とし、Bash / PowerShell では得意なサブセットを実装する。

### 目的

- 章ごとの断片例を、一つの運用ツールとして接続する
- dry-run、設定優先順位、終了コード、構造化ログの共通作法を固定する
- 第15章の題材を、サブコマンドとして実装する

### 全体仕様

```text
opsctl <subcommand> [options]

共通オプション:
  --config PATH       設定ファイル（既定: ./config/opsctl.yaml）
  --dry-run           変更を行わず予定だけ表示
  --verbose           DEBUGログを出す
  --quiet             WARNING以上のみ出す
  --timeout SECONDS   外部呼び出しの既定タイムアウト（既定: 30）
  --hosts-file PATH   対象ホスト一覧（1行1ホスト）
```

### 設定ファイル例

```yaml
# config/opsctl.yaml
defaults:
  timeout_seconds: 30
  disk_warn_percent: 80
  disk_crit_percent: 90
  log_level: INFO
  backup_retention_days: 14

logging:
  format: json
  include_run_id: true

paths:
  work_dir: ./work
  report_dir: ./reports
  backup_dir: ./backups

api:
  base_url: "https://api.example.invalid"
  # 認証情報はファイルに書かない。環境変数 OPSCTL_API_TOKEN を使う
```

### ホスト一覧例

```text
# config/hosts.txt
web01.example.invalid
web02.example.invalid
db01.example.invalid
```

### サブコマンド一覧

| サブコマンド | 概要 | 主実装言語 | 補助実装 |
|--------------|------|------------|----------|
| `ping-check` | 複数ホストへの疎通確認 | Python | Bash |
| `disk-check` | ディスク使用率監視 | Bash / PowerShell | Python |
| `log-search` | ログファイル検索 | Python | Bash |
| `cleanup-old` | 古いファイル整理 | Python | PowerShell |
| `user-audit` | ユーザーアカウント棚卸し | PowerShell | Bash |
| `service-check` | サービス稼働確認 | Bash / PowerShell | Python |
| `config-patch` | 設定ファイル一括変更 | Python | — |
| `api-export` | API取得→CSV出力 | Python | PowerShell |
| `backup` | バックアップ | Bash / Python | PowerShell |
| `cert-check` | 証明書期限確認 | Python | Bash |
| `report` | 定期レポート生成 | Python | — |

### 終了コード規約（opsctl共通）

| コード | 意味 |
|--------|------|
| 0 | 成功（警告なし） |
| 1 | 使い方誤り、設定誤りなどの利用者エラー |
| 2 | 実行時エラー（一部失敗を含む） |
| 3 | 閾値超過など、監視上の CRITICAL |
| 4 | タイムアウト |
| 130 | ユーザーによる中断（Ctrl+C） |

部分成功は「全体成功」にしない。失敗ホスト一覧を標準エラーまたはレポートに残し、終了コード 2 または 3 を返す。

### ログ規約

- 各実行に UUID 形式の `run_id` を付与する
- 既定は JSON 1行1イベント
- フィールド例: `ts`, `level`, `run_id`, `event`, `host`, `message`
- パスワード、トークン、Authorizationヘッダーはマスクする

### 再実行性

- 同じ入力で再実行しても、破壊的操作は冪等またはスキップ可能にする
- バックアップやレポートはタイムスタンプ付きパスへ書き、上書き事故を避ける
- dry-run では書き込み、削除、再起動、外部への変更APIを呼ばない

### 実装ディレクトリ（本書リポジトリ内）

```text
infra_scripting_coding_guide/
  README.md
  01_....md ... 16_....md
  A_language_selection.md
  B_exit_codes.md
  C_checklist.md
  requirements.txt
  config/
    opsctl.yaml
    hosts.txt
  samples/
    python/
    bash/
    powershell/
    shared/
  tests/
```

---

## 執筆進捗

| ファイル | 状態 |
|----------|------|
| README.md（本ファイル） | 完成 |
| 01〜16（本編） | 完成 |
| A / B / C（付録） | 完成 |
| COMPLETE.md | 完成（FINAL） |
| COMPLETE_BOOK.md | 完成（合本） |

各章のサンプルコードは `samples/` 配下に完全な形で置く。テストは `tests/` を参照する。


---


<!-- SOURCE: 01_script_and_programming_basics.md -->

# 第1章 スクリプトとプログラミングの基本

## 学習目標

この章を終えると、次ができるようになる。

- スクリプトとコンパイル言語の違いを、実行の流れで説明できる
- 標準入力、標準出力、標準エラー、終了コードを使い分けられる
- 環境変数とコマンドライン引数で、設定と秘密情報をコードから分離できる
- 手作業を「入力・処理・出力・失敗時挙動」に分解し、自動化の可否を判断できる

前提:

- Python 3.11以上、Bash 4以上、PowerShell 7.4以上のいずれかが使えること
- ターミナルでカレントディレクトリを変更できること

---

## 基本概念

本章で扱う中心概念は次のとおりである。

- **スクリプト**: インタープリターがソースを読みながら実行するプログラム
- **標準入出力**: stdin / stdout / stderr の役割分担
- **終了コード**: プロセスの成否を整数で返す契約
- **環境変数と引数**: 実行環境の設定と、その実行だけの選択の分離

詳細は以降の節で順に展開する。

---

## 1.1 スクリプトとは何か

**スクリプト**とは、インタープリターがソースコードを読みながら逐次実行するプログラムである。

インフラ運用では、次のような作業をファイルに書いて繰り返せる形にしたものがスクリプトと呼ばれる。

- 複数サーバーへの疎通確認
- ログの検索と集計
- 設定ファイルのバックアップと差し替え
- APIから情報を取得してCSVに落とす

スクリプトの価値は、タイピングの省略だけではない。手順を文章ではなく実行可能な形で固定し、同じ条件なら同じ結果を再現できる点にある。

手作業の手順書が「だいたい同じ」で終わるのに対し、スクリプトは入力が同じなら出力も揃う。揃わないときは、環境差かバグとして調査対象になる。

---

## 1.2 コンパイル言語との違い

**コンパイル言語**では、ソースコードをコンパイラが機械語や中間表現に変換してから実行する。CやGo、Rustが典型である。

**インタープリター言語**では、実行のたびにインタープリターがソースを解釈する。Python、Bash、PowerShellがこれに近い。[^1]

実務上の差は次のとおりである。

| 観点 | スクリプト寄り（Python / Bash / PowerShell） | コンパイル寄り（Go / Rust など） |
|------|-----------------------------------------------|----------------------------------|
| 変更から実行まで | 編集してすぐ実行できる | ビルドが必要 |
| 配布 | ランタイムが必要 | 単一バイナリにしやすい |
| 型や安全性 | 言語と運用で補う | コンパイル時検査が強いことが多い |
| 運用現場での採用 | 既存コマンドとの糊付けに強い | 長期稼働の常駐ツール向き |

インフラ自動化では、既存のOSコマンド、設定ファイル、APIを短期間でつなぐことが多い。そのためスクリプトが選ばれやすい。一方、常駐エージェントや高負荷な収集基盤ではコンパイル言語が選ばれることもある。本書は前者を対象とする。

[^1]: PowerShellは実行前にパースとコンパイル段階を持つ。本書では「ソースを直接実行できる」点をスクリプトとして扱う。

---

## 1.3 インタープリターとソースコード

**ソースコード**は、人が読み書きするプログラムの原文である。

**インタープリター**は、ソースコードを読み、文を解釈して実行するプログラムである。

三言語の起動例:

```bash
python3 hello.py
bash hello.sh
pwsh hello.ps1
```

シバン（shebang）を付けると、Unix系ではファイルを直接実行できる。

```bash
#!/usr/bin/env python3
print("hello")
```

```bash
#!/usr/bin/env bash
echo "hello"
```

```bash
#!/usr/bin/env pwsh
Write-Output "hello"
```

実行権限が必要である。

```bash
chmod +x hello.py
./hello.py
```

Windowsではシバンは使わないことが多い。`python`、`pwsh` を明示して呼び出す。

PowerShellの実行ポリシーが RemoteSigned などの制限だと、ダウンロードしたスクリプトがブロックされる。方針は組織のセキュリティポリシーに従う。学習用ローカルファイルでは、署名なしローカルスクリプトが許可されているかを確認する。

```powershell
Get-ExecutionPolicy -List
```

---

## 1.4 標準入力、標準出力、標準エラー

プロセスは起動時に、少なくとも三つの入出力チャネルを持つ。

- **標準入力（stdin）**: 入力の受け口。番号は 0
- **標準出力（stdout）**: 正常な結果の出し口。番号は 1
- **標準エラー（stderr）**: 診断情報やエラーの出し口。番号は 2

運用スクリプトでは、次の分担が扱いやすい。

- stdout: 機械が次に使う結果（CSV、JSON、ホスト名一覧）
- stderr: 人や監視が読む進捗とエラー

結果とログを同じストリームに混ぜると、パイプの下流が壊れる。

### 最小構成のコード

Python:

```python
#!/usr/bin/env python3
import sys

name = sys.stdin.readline().strip()
if not name:
    print("name is required", file=sys.stderr)
    sys.exit(1)

print(f"hello, {name}")
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

read -r name
if [[ -z "${name}" ]]; then
  echo "name is required" >&2
  exit 1
fi

echo "hello, ${name}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

$name = [Console]::In.ReadLine()
if ([string]::IsNullOrWhiteSpace($name)) {
    [Console]::Error.WriteLine('name is required')
    exit 1
}

Write-Output "hello, $name"
```

実行例（Bash）:

```bash
printf 'ops\n' | bash samples/bash/01_hello_stdin.sh
# stdout: hello, ops
```

エラー例:

```bash
printf '\n' | bash samples/bash/01_hello_stdin.sh
# stderr: name is required
# exit code: 1
```

### リダイレクト

```bash
# stdout をファイルへ
./tool.sh > result.txt

# stderr をファイルへ
./tool.sh 2> error.txt

# 両方
./tool.sh > all.txt 2>&1

# stdin をファイルから
./tool.sh < hosts.txt
```

PowerShell:

```powershell
./tool.ps1 > result.txt
./tool.ps1 2> error.txt
Get-Content hosts.txt | ./tool.ps1
```

---

## 1.5 終了コード

**終了コード**（exit status）は、プロセスが終了したときにOSへ返す整数である。

慣例:

- `0`: 成功
- 非0: 失敗

シェルでは直前のコマンドの終了コードが `$?`（Bash）または `$LASTEXITCODE`（PowerShell）に入る。

```bash
true
echo $?    # 0

false
echo $?    # 1
```

```powershell
pwsh -NoProfile -Command 'exit 3'
echo $LASTEXITCODE
```

監視やCIは終了コードで成否を判定する。メッセージだけ出して終了コード0のままにするのは、失敗の隠蔽である。

本書の `opsctl` では次を使う（README参照）。

| コード | 意味 |
|--------|------|
| 0 | 成功 |
| 1 | 使い方・設定の誤り |
| 2 | 実行時エラー（部分失敗を含む） |
| 3 | 監視上の CRITICAL |
| 4 | タイムアウト |
| 130 | Ctrl+C |

### 悪いコード

```python
#!/usr/bin/env python3
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
print(text.upper())
# ファイルが無くても例外で落ちるが、呼び出し側向けの終了コード設計がない
# 引数不足も IndexError のまま
```

問題点:

- 引数不足が利用者向けメッセージにならない
- 例外がトレースバックのまま終わり、終了コードが言語既定に依存する
- stderr / stdout の役割が不明

### 改善後のコード

```python
#!/usr/bin/env python3
"""Read a text file and print its uppercased contents."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("upperfile")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uppercase a text file")
    parser.add_argument("path", type=Path, help="input text file")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="enable debug logging",
    )
    return parser.parse_args(argv)


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    if not path.is_file():
        raise ValueError(f"not a regular file: {path}")
    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(args.verbose)

    try:
        text = read_text_file(args.path)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME

    sys.stdout.write(text.upper())
    if text and not text.endswith("\n"):
        sys.stdout.write("\n")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

実行例:

```bash
echo 'abc' > /tmp/a.txt
python3 samples/python/01_upperfile.py /tmp/a.txt
# ABC

python3 samples/python/01_upperfile.py /tmp/missing.txt
echo $?
# stderr に error、終了コード 2
```

---

## 1.6 環境変数

**環境変数**は、プロセスに渡されるキーと値の組である。子プロセスにも継承される。

用途の分離:

- コード: 手順とロジック
- 引数: その実行だけの選択
- 環境変数: 実行環境ごとの設定や秘密情報の受け渡し口

秘密情報（APIトークン、パスワード）をソースに直書きしない。環境変数、シークレットマネージャ、CIの秘密変数から渡す。

### 読み取り例

Python:

```python
#!/usr/bin/env python3
import os
import sys

token = os.environ.get("OPSCTL_API_TOKEN")
if not token:
    print("OPSCTL_API_TOKEN is required", file=sys.stderr)
    sys.exit(1)

print("token is set", file=sys.stderr)
print(len(token))  # 値そのものは出さない
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPSCTL_API_TOKEN:-}" ]]; then
  echo "OPSCTL_API_TOKEN is required" >&2
  exit 1
fi

echo "token is set" >&2
echo "${#OPSCTL_API_TOKEN}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($env:OPSCTL_API_TOKEN)) {
    [Console]::Error.WriteLine('OPSCTL_API_TOKEN is required')
    exit 1
}

[Console]::Error.WriteLine('token is set')
Write-Output $env:OPSCTL_API_TOKEN.Length
```

設定例:

```bash
export OPSCTL_API_TOKEN='replace-me'
python3 samples/python/01_check_token.py
```

```powershell
$env:OPSCTL_API_TOKEN = 'replace-me'
pwsh samples/powershell/01_check_token.ps1
```

ログや標準出力にトークン本体を出さない。長さや「設定済み」だけを出す。

---

## 1.7 コマンドライン引数

**コマンドライン引数**は、起動時にプロセスへ渡すパラメータである。

```bash
python3 tool.py --hosts-file hosts.txt --timeout 10
```

`sys.argv`、Bashの `$1`、PowerShellの `param()` ブロックで受け取る。

実務では次を最初から決める。

- 必須引数と任意引数
- デフォルト値
- ヘルプ（`--help`）
- 不正値のときの終了コード

### 最小構成（三言語）

Python（argparse）:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Echo hosts file path")
    parser.add_argument("--hosts-file", required=True)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.timeout <= 0:
        print("--timeout must be positive", file=sys.stderr)
        return 1
    print(f"{args.hosts_file},{args.timeout}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

hosts_file=""
timeout=30

usage() {
  cat <<'EOF' >&2
Usage: 01_parse_args.sh --hosts-file PATH [--timeout SECONDS]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hosts-file)
      hosts_file="${2:-}"
      shift 2
      ;;
    --timeout)
      timeout="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${hosts_file}" ]]; then
  echo "--hosts-file is required" >&2
  usage
  exit 1
fi

if ! [[ "${timeout}" =~ ^[1-9][0-9]*$ ]]; then
  echo "--timeout must be a positive integer" >&2
  exit 1
fi

echo "${hosts_file},${timeout}"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile,

    [int]$Timeout = 30
)

$ErrorActionPreference = 'Stop'

if ($Timeout -le 0) {
    [Console]::Error.WriteLine('--Timeout must be positive')
    exit 1
}

Write-Output "$HostsFile,$Timeout"
exit 0
```

---

## 1.8 手作業を自動化する際の考え方

自動化は、手順書のタイピング置換ではない。次の順で分解する。

1. **目的**: 何が達成されれば終わりか
2. **入力**: ファイル、引数、環境変数、API、人の確認
3. **出力**: ファイル、標準出力、終了コード、チケット更新
4. **成功条件**: 終了コード0の意味
5. **失敗時**: どこまで戻すか、誰に何を残すか
6. **再実行**: 二度実行しても安全か
7. **権限**: 最小権限で足りるか

例: 「毎朝、各Webサーバーのディスク使用率を見て、90%超なら知らせる」

| 項目 | 内容 |
|------|------|
| 入力 | ホスト一覧、SSH認証、閾値、通知先 |
| 処理 | 各ホストで使用率取得、閾値比較 |
| 出力 | レポート、通知、終了コード |
| 失敗 | 一部ホスト不通でも残りは調べる。不通は一覧化 |
| 再実行 | 読み取りだけなら何度でも可 |
| やってはいけないこと | 閾値超過で即削除や即拡張を自動実行する（要変更管理） |

疑似コードに落とす。

```text
load hosts
for host in hosts:
  try:
    usage = get_disk_usage(host, timeout=30)
    if usage >= critical:
      record critical
    elif usage >= warn:
      record warn
  catch:
    record unreachable
write report
if any critical or unreachable:
  exit non-zero
else:
  exit 0
```

第2章で、この分解をアルゴリズムとして深める。

---

## 1.9 自動化すべき作業とすべきでない作業

### 自動化しやすい作業

- 手順が固定で、判断が規則に落とせる
- 頻度が高く、手作業ミスの損害が大きい
- 結果を終了コードやレポートで機械判定できる
- 失敗時に安全側へ倒せる（読み取り、dry-run、バックアップ付き）

例: 疎通確認、証明書期限の一覧化、ログの定型検索、バックアップ取得。

### 自動化を急がない作業

- 一回限りで、再現条件が残らない
- 判断が政治的・契約的で、コードに落とせない
- 失敗時の影響が大きく、承認なしで進めてはならない
- 対象が不定で、探索的調査が本体である

例: 初回の障害原因仮説の立案、大規模本番の手動フェイルオーバー判断、権限の永久付与。

破壊的操作を自動化する場合の最低条件:

1. dry-runがある
2. バックアップまたはロールバック手順がある
3. 実行前確認（対話または変更チケットID）がある
4. 監査ログが残る
5. 権限が最小である

> **警告**: 削除、上書き、再起動、ファイアウォール変更を、確認なしのcronだけで回さない。まず報告だけを自動化し、変更は承認後に別コマンドで実行する構成が安全である。

---

## 1.10 実務向けの小さな統合例

手作業「ホスト名を1行ずつ読み、空行とコメントを除いて件数を出す」を、三言語で実装する。

入力ファイル例 `config/hosts.txt`:

```text
# web tier
web01.example.invalid
web02.example.invalid

# db tier
db01.example.invalid
```

### Python

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("count_hosts")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Count non-empty host lines")
    parser.add_argument("hosts_file", type=Path)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")

    hosts: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {line_no}: contains whitespace")
        hosts.append(line)
    return hosts


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME

    logger.info("loaded %s hosts", len(hosts))
    print(len(hosts))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

### Bash

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 HOSTS_FILE" >&2
  exit 1
fi

hosts_file="$1"
if [[ ! -f "${hosts_file}" ]]; then
  echo "hosts file not found: ${hosts_file}" >&2
  exit 2
fi

count=0
line_no=0
while IFS= read -r raw || [[ -n "${raw}" ]]; do
  line_no=$((line_no + 1))
  # trim
  line="$(printf '%s' "${raw}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [[ -z "${line}" ]] && continue
  [[ "${line}" == \#* ]] && continue
  if [[ "${line}" =~ [[:space:]] ]]; then
    echo "invalid host at line ${line_no}: contains whitespace" >&2
    exit 2
  fi
  count=$((count + 1))
done < "${hosts_file}"

echo "loaded ${count} hosts" >&2
echo "${count}"
```

### PowerShell

```powershell
#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [string]$HostsFile
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $HostsFile -PathType Leaf)) {
    [Console]::Error.WriteLine("hosts file not found: $HostsFile")
    exit 2
}

$hosts = @()
$lineNo = 0
foreach ($raw in Get-Content -LiteralPath $HostsFile) {
    $lineNo++
    $line = $raw.Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line.StartsWith('#')) { continue }
    if ($line -match '\s') {
        [Console]::Error.WriteLine("invalid host at line ${lineNo}: contains whitespace")
        exit 2
    }
    $hosts += $line
}

[Console]::Error.WriteLine("loaded $($hosts.Count) hosts")
Write-Output $hosts.Count
exit 0
```

実行例:

```bash
python3 samples/python/01_count_hosts.py config/hosts.txt
# stderr: INFO loaded 3 hosts
# stdout: 3
```

---

## 1.11 セキュリティ上の注意点

- パスワード、トークン、秘密鍵をソース、ログ、コミットに含めない
- 引数に秘密情報を渡すと `ps` で見える場合がある。可能なら環境変数やファイル権限付きシークレットを使う
- 利用者入力をそのままシェルに連結しない（第7章、第10章）
- 終了コード0で失敗を隠さない
- 学習用ドメイン例には `example.invalid` など、実在しにくい名前を使う

---

## 1.12 テスト方法

第1章では「終了コード」と「stdout/stderrの分離」を手動でも機械でも確認する。

Python（pytestの骨格）:

```python
# tests/test_01_count_hosts.py
from pathlib import Path

from samples.python.count_hosts import load_hosts, main


def test_load_hosts_skips_comments(tmp_path: Path) -> None:
    path = tmp_path / "hosts.txt"
    path.write_text("# c\na.example.invalid\n\nb.example.invalid\n", encoding="utf-8")
    assert load_hosts(path) == ["a.example.invalid", "b.example.invalid"]


def test_main_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.txt"
    assert main([str(missing)]) == 2
```

Bash:

```bash
bash samples/bash/01_count_hosts.sh config/hosts.txt
test "$(bash samples/bash/01_count_hosts.sh config/hosts.txt 2>/dev/null)" -eq 3
```

PowerShell:

```powershell
$result = pwsh -File samples/powershell/01_count_hosts.ps1 -HostsFile config/hosts.txt
if ($result -ne 3) { throw "unexpected count: $result" }
```

---

## 章末問題

### 問題1

次の手作業を、入力・処理・出力・失敗時・再実行性に分解せよ。

「設定ファイル `app.conf` を編集する前に、同ディレクトリへ日時付きコピーを取り、編集後に `nginx -t` 相当の構文チェックを行う。」

### 問題2

stdoutに進捗メッセージ、結果JSONの両方を出しているスクリプトの問題点を述べ、修正方針を書け。

### 問題3

環境変数 `BACKUP_ROOT` が未設定のとき、デフォルトで `/` 以下を削除対象にしてしまう設計の危険を説明し、安全側のデフォルトを提案せよ。

### 問題4

終了コードが常に0で、失敗はメール本文にだけ書く監視連携の欠点を述べよ。

### 問題5

次のBash断片の問題点を指摘し、改善案を書け。

```bash
hosts=$1
for h in $(cat $hosts); do
  ping -c 1 $h
done
```

---

## 解答と解説

### 問題1

| 項目 | 例 |
|------|-----|
| 入力 | `app.conf` のパス、バックアップ先、チェックコマンド、dry-run可否 |
| 処理 | バックアップ作成 →（非dry-runなら）編集適用 → 構文チェック |
| 出力 | バックアップパス、チェック結果、終了コード |
| 失敗時 | チェック失敗なら編集を戻すか、サービス再読込をしない |
| 再実行 | バックアップ名に時刻を含め、上書きしない |

### 問題2

パイプやリダイレクトで結果だけを渡せない。進捗はstderr、結果はstdoutへ分離する。

### 問題3

未設定時にルート近傍を触ると、誤削除の被害が全域に広がる。未設定は即終了（終了コード1）にし、削除対象は明示引数のみとする。

### 問題4

監視やCIが失敗を検知できない。アラートがメール依存になり、遅延や見逃しが起きる。終了コードとログの両方を使う。

### 問題5

- `cat` と単語分割で、空白やグロブが壊れる
- 変数が引用符なし
- ping失敗でもループが続き、全体の終了コードが最後の結果に依存する
- タイムアウトがない

改善方針: `while read` で1行ずつ、引用符、失敗集計、`ping -W` などのタイムアウト、最後に集計終了コード。

---

## 実装演習

### 演習A: echoツールの三言語実装

要件:

- 引数 `--message` を必須とする
- `--times N`（既定1）で繰り返す
- Nが正の整数でなければ終了コード1
- 進捗はstderr、本文はstdout
- 使用方法を `--help` で出せる（Python/PowerShellは標準機能、Bashは自前）

提出物: 三言語のスクリプト、実行例、失敗例。

### 演習B: 手作業の分解シート

自分が週1回以上やっている手作業を一つ選び、次の表を埋める。

- 目的
- 入力
- 出力
- 成功条件
- 失敗時
- 再実行性
- 自動化する / しない の判断と理由

### 演習C: opsctl設定の読み取り準備

`config/opsctl.yaml` と `config/hosts.txt` を用意し、ホスト件数を数えるスクリプト（本章のcount_hosts）で検証する。次章以降でこの入力を共有する。

---

## 次章予告

第2章では、本章の分解を疑似コード、フローチャート、状態、計算量、エッジケースまで落とし、実装前に失敗時挙動を決める手順を扱う。


---


<!-- SOURCE: 02_problem_decomposition_and_algorithms.md -->

# 第2章 問題分解とアルゴリズム

## 学習目標

この章を終えると、次ができるようになる。

- 運用課題を入力・処理・出力に分解し、要件として書き出せる
- 疑似コードと簡単なフローで、実装前に手順を固定できる
- 条件分岐、反復、状態、関数を使って処理を分割できる
- エッジケースと失敗時挙動を、正常系より先に決められる
- 計算量の感覚で、ホスト数やファイルサイズに耐える設計を選べる

前提: 第1章の標準入出力、終了コード、引数、環境変数を理解していること。

---

## 基本概念

**問題分解**は、運用課題を入力・処理・出力・失敗時・再実行性へ分割し、実装可能な単位に落とすことである。

**アルゴリズム**は、その単位を、条件分岐と反復と状態更新の手順として表したものである。

コードを書く前に、疑似コードまたはフローで失敗経路を先に固定する。

---

## 2.1 入力、処理、出力

あらゆる自動化は、次の三段に落とせる。

1. **入力**: いま手元にある事実と設定
2. **処理**: 入力を変換・判定・副作用付き操作する手順
3. **出力**: 残すべき結果（ファイル、終了コード、通知）

例: 「証明書の期限が30日以内のホストを報告する」

| 段 | 具体例 |
|----|--------|
| 入力 | ホスト一覧、接続方法、閾値日数、現在日時 |
| 処理 | 各ホストの証明書を取得し、残日数を計算し、閾値と比較 |
| 出力 | CSVレポート、標準エラーの要約、終了コード |

入力が曖昧なまま実装に入ると、境界（閾値ちょうど、取得失敗、時計ずれ）で毎回議論が起きる。先に入出力を表に書く。

---

## 2.2 要件の整理

要件は「やりたいこと」の感想ではない。検証可能な文にする。

悪い要件:

> ディスクがいっぱいになったらなんとかする。

良い要件:

1. 対象は `config/hosts.txt` のホストとする
2. ルートファイルシステムの使用率が警告80%、重大90%とする
3. 重大が1台でもあれば終了コード3、取得失敗のみなら終了コード2とする
4. 結果は `reports/disk-YYYYMMDD-HHMMSS.csv` に書く
5. 既定は観察のみとし、削除や拡張は行わない

要件を次の観点で点検する。

- **完了条件**: いつ終わりか
- **対象範囲**: 何を含み、何を含まないか
- **非機能**: タイムアウト、同時実行数、権限
- **失敗時**: 部分失敗を成功と呼ぶか
- **再実行**: 二度目で何が起きるか
- **監査**: 誰がいつ何をしたか残るか

---

## 2.3 処理の分割

大きな処理を、一度に理解できる単位へ割る。

分割の目安:

- 一つの関数が一つの理由で変わる
- 名前を読んで入出力が想像できる
- テストで単独に假の入力を渡せる

ディスク監視の分割例:

```text
load_config()
load_hosts()
for host in hosts:
  usage = fetch_disk_usage(host)   # 外部I/O
  level = classify(usage, thresholds)  # 純粋な判定
  append_result(results, host, usage, level)
write_report(results)
exit_code = summarize(results)
```

`classify` はネットワークに依存しない。単体テストしやすい。

`fetch_disk_usage` は失敗しやすい。タイムアウトと例外方針をここに閉じ込める。

---

## 2.4 疑似コード

**疑似コード**は、特定言語の文法に縛られず手順を書くための表記である。実装前の設計メモとして使う。

```text
function check_disks(hosts_file, warn, crit, timeout):
  hosts = load_hosts(hosts_file)
  results = empty list
  for host in hosts:
    try:
      usage = get_usage(host, timeout)
      if usage >= crit:
        status = CRITICAL
      else if usage >= warn:
        status = WARNING
      else:
        status = OK
      append(results, host, usage, status)
    catch Timeout:
      append(results, host, null, TIMEOUT)
    catch Error as e:
      append(results, host, null, ERROR(e))
  write_csv(results)
  if any status is CRITICAL:
    return 3
  if any status is TIMEOUT or ERROR:
    return 2
  if any status is WARNING:
    return 0   # 警告はログに残し、監視重要度は運用方針で決める
  return 0
```

疑似コードの段階で、WARNINGを終了コード0にするか非0にするかを決める。実装後に変えると、監視の閾値定義が壊れる。

---

## 2.5 フローチャート

分岐と反復が多い処理は、図にすると抜け漏れが見える。

本書では Mermaid で表す。

```mermaid
flowchart TD
  A[開始] --> B[設定とホスト一覧を読む]
  B --> C{未処理ホストがある?}
  C -->|はい| D[使用率を取得]
  D --> E{成功?}
  E -->|いいえ| F[ERROR/TIMEOUTを記録]
  F --> C
  E -->|はい| G{使用率 >= crit?}
  G -->|はい| H[CRITICALを記録]
  H --> C
  G -->|いいえ| I{使用率 >= warn?}
  I -->|はい| J[WARNINGを記録]
  J --> C
  I -->|いいえ| K[OKを記録]
  K --> C
  C -->|いいえ| L[レポート出力]
  L --> M[終了コードを決定]
  M --> N[終了]
```

図は詳細実装の代替ではない。異常系の箱が欠けていないかを見るために使う。

---

## 2.6 条件分岐

**条件分岐**は、述語（真偽）に応じて経路を分けることである。

三言語の最小例（閾値判定）:

Python:

```python
def classify(usage: float, warn: float, crit: float) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"
```

Bash:

```bash
classify() {
  local usage="$1" warn="$2" crit="$3"
  if (( $(echo "${usage} >= ${crit}" | bc -l) )); then
    echo CRITICAL
  elif (( $(echo "${usage} >= ${warn}" | bc -l) )); then
    echo WARNING
  else
    echo OK
  fi
}
```

小数比較はBash単体では弱い。整数パーセントに丸めるか、Python/PowerShellへ寄せる判断が実務では多い。

PowerShell:

```powershell
function Classify {
    param([double]$Usage, [double]$Warn, [double]$Crit)
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}
```

分岐を深くしない。異常を先に返す方法は第4章で扱う。

---

## 2.7 反復処理

**反復**は、同じ手順を要素ごとに繰り返すことである。

ホスト一覧、ログ行、ページネーションのページが典型である。

注意点:

1. 無限ループの抜け条件を明示する
2. 1件失敗で全体を止めるか、集計して続けるかを先に決める
3. 並列化するなら、同時実行数とタイムアウトを制限する

### 悪いコード（1件失敗で黙って継続、終了コード常に0）

```python
def check_all(hosts):
    for host in hosts:
        try:
            print(get_usage(host))
        except Exception:
            pass
    return 0
```

問題点:

- 失敗が消える
- 呼び出し側が成功と誤解する
- どのホストが失敗したか残らない

### 改善後

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HostResult:
    host: str
    usage: float | None
    status: str
    error: str | None = None


def check_all(hosts: list[str], warn: float, crit: float, fetch) -> tuple[list[HostResult], int]:
    results: list[HostResult] = []
    for host in hosts:
        try:
            usage = fetch(host)
            status = classify(usage, warn, crit)
            results.append(HostResult(host, usage, status))
        except TimeoutError as exc:
            results.append(HostResult(host, None, "TIMEOUT", str(exc))
            )
        except OSError as exc:
            results.append(HostResult(host, None, "ERROR", str(exc)))

    if any(r.status == "CRITICAL" for r in results):
        return results, 3
    if any(r.status in {"TIMEOUT", "ERROR"} for r in results):
        return results, 2
    return results, 0


def classify(usage: float, warn: float, crit: float) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"
```

---

## 2.8 状態

**状態**は、処理の途中結果として保持している情報である。

スクリプトでよく出る状態:

- 累積カウンタ（成功数、失敗数）
- いま開いているファイルハンドル
- dry-runかどうか
- 既にバックアップ済みか

状態が多いほど、再実行時の挙動が読みにくい。可能なら、状態を「入力ファイルと引数から再現できる値」に寄せる。

例: 「削除済みファイル一覧」をメモリだけに持つのではなく、`work/cleanup-runid.done` に追記する。再実行時に済みをスキップできる。

```text
for file in candidates:
  if file in done_set:
    skip
  else if dry_run:
    log would_delete
  else:
    delete file
    append file to done_set file
```

これが再実行性の基本形である。

---

## 2.9 関数と再利用

関数にする判断:

- 同じコードが二箇所以上に現れそう
- 名前を付けた方が、読者が段落を飛ばせる
- 単体でテストしたい

再利用の単位:

| 単位 | 例 |
|------|-----|
| 関数 | `load_hosts`, `classify` |
| モジュール | ホスト読み込み、ログ初期化 |
| コマンド | `opsctl disk-check` |

まだ一度しか使わない処理でも、入出力が明確なら関数にしてよい。長さの削減より、読解単位の分割が目的である。

---

## 2.10 計算量の基礎

インフラスクリプトでも、入力サイズで実行時間が変わる。

目安:

- ホスト数 N に比例してSSHする → おおよそ O(N)
- 各ホストでファイル M 個を見る → O(N×M)
- 二重ループで全ホスト同士を比較 → O(N²) になりやすい

感覚の使い方:

1. N=10で1秒なら、N=1000で単純比例なら100秒
2. 直列SSHが遅いなら、同時実行数を制限した並列を検討する
3. 巨大ログを全部 `read()` でメモリに載せない（第6章）

厳密な漸近評価より、「入力が10倍になったとき何が壊れるか」を先に書く。

---

## 2.11 エッジケース

**エッジケース**は、境界や例外的な入力で起きる事態である。

ディスク監視の例:

| ケース | 期待挙動 |
|--------|----------|
| ホスト一覧が空 | 終了コード1（設定誤り） |
| 使用率ちょうど80.0 | WARNING（`>=` と決めたなら） |
| 使用率100 | CRITICAL |
| ホスト名に空白 | 読み込み時点で拒否 |
| 1台だけタイムアウト | 記録し、他は継続。終了コード2 |
| 時計が大きくずれている | 証明書用途では別問題。本章ではディスクでは影響小 |
| dry-run | 取得は行うか、行わないかを仕様で固定 |

境界値はテストに必ず入れる（第13章）。

---

## 2.12 失敗時の挙動

失敗時設計は、正常系より先に決める。

決める項目:

1. **検出**: 何をもって失敗とするか（終了コード、例外、NULL）
2. **記録**: どこに何を残すか（stderr、ログ、レポート列）
3. **継続**: 次の要素を続けるか、中断するか
4. **復帰**: ロールバックするか、人手に渡すか
5. **終了コード**: 監視がどう解釈するか

### 実務向けサンプル: ホスト疎通の設計から実装

要件:

- 入力: ホスト一覧、1ホストあたりのタイムアウト秒
- 処理: 各ホストへ ICMP 相当の疎通（環境により `ping`）
- 出力: CSV（host,ok,detail）、終了コード
- 失敗: 不通でも継続。1台でも不通なら終了コード2
- dry-run: 実際のpingはせず、実行予定だけをstderrへ出す

> **注意**: ICMPが制限された環境では失敗が増える。本番ではTCPポート確認など別手法を選ぶ。以下は学習用である。

Python実装（実行可能）:

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import platform
import subprocess
import sys
import time
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_TIMEOUT = 4

logger = logging.getLogger("ping_check")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ping hosts from a list file")
    parser.add_argument("--hosts-file", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(ch.isspace() for ch in line):
            raise ValueError(f"invalid host at line {line_no}")
        hosts.append(line)
    if not hosts:
        raise ValueError("hosts file is empty")
    return hosts


def ping_host(host: str, timeout: int) -> tuple[bool, str]:
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), host]

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "ping process timeout"
    except FileNotFoundError:
        return False, "ping command not found"

    if completed.returncode == 0:
        return True, "ok"
    detail = (completed.stderr or completed.stdout or "ping failed").strip().splitlines()
    return False, detail[0] if detail else "ping failed"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if args.timeout <= 0:
        logger.error("--timeout must be positive")
        return EXIT_USAGE

    try:
        hosts = load_hosts(args.hosts_file)
    except (OSError, ValueError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    args.report.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    failures = 0

    for host in hosts:
        if args.dry_run:
            logger.info("dry-run: would ping %s timeout=%s", host, args.timeout)
            rows.append({"host": host, "ok": "dry-run", "detail": "skipped"})
            continue

        started = time.monotonic()
        ok, detail = ping_host(host, args.timeout)
        elapsed_ms = int((time.monotonic() - started) * 1000)
        logger.info("host=%s ok=%s elapsed_ms=%s detail=%s", host, ok, elapsed_ms, detail)
        rows.append({"host": host, "ok": "true" if ok else "false", "detail": detail})
        if not ok:
            failures += 1

    with args.report.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "ok", "detail"])
        writer.writeheader()
        writer.writerows(rows)

    if args.dry_run:
        return EXIT_OK
    return EXIT_OK if failures == 0 else EXIT_RUNTIME


if __name__ == "__main__":
    sys.exit(main())
```

実行例:

```bash
python3 samples/python/02_ping_check.py \
  --hosts-file config/hosts.txt \
  --report reports/ping-dry.csv \
  --dry-run --verbose
```

```bash
python3 samples/python/02_ping_check.py \
  --hosts-file config/hosts.txt \
  --timeout 2 \
  --report reports/ping.csv
echo $?
```

想定失敗例:

- ホストファイルなし → 終了コード1
- 実在しないホストのみ → 終了コード2、CSVに false
- `ping` が無いコンテナ → detail に command not found

Bash版の骨子（疎通確認はBashが得意な糊付け）:

```bash
#!/usr/bin/env bash
set -euo pipefail

hosts_file=""
timeout=3
report=""
dry_run=0

usage() {
  echo "Usage: $0 --hosts-file PATH --report PATH [--timeout N] [--dry-run]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hosts-file) hosts_file="${2:-}"; shift 2 ;;
    --report) report="${2:-}"; shift 2 ;;
    --timeout) timeout="${2:-}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "${hosts_file}" && -n "${report}" ]] || { usage; exit 1; }
[[ -f "${hosts_file}" ]] || { echo "missing hosts file" >&2; exit 1; }
mkdir -p "$(dirname "${report}")"
echo "host,ok,detail" > "${report}"

failures=0
while IFS= read -r raw || [[ -n "${raw}" ]]; do
  line="${raw#"${raw%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "${line}" || "${line}" == \#* ]] && continue
  if [[ "${dry_run}" -eq 1 ]]; then
    echo "dry-run: would ping ${line}" >&2
    echo "${line},dry-run,skipped" >> "${report}"
    continue
  fi
  if ping -c 1 -W "${timeout}" "${line}" >/dev/null 2>&1; then
    echo "${line},true,ok" >> "${report}"
  else
    echo "${line},false,ping failed" >> "${report}"
    failures=$((failures + 1))
  fi
done < "${hosts_file}"

if [[ "${dry_run}" -eq 1 ]]; then
  exit 0
fi
[[ "${failures}" -eq 0 ]]
```

macOSの `ping -W` は単位がミリ秒の場合がある。OS差は第7章と第15章で明示する。上記BashはLinux想定とし、macOSでは Python版を優先する。

---

## 2.13 セキュリティ上の注意点

- ホスト名をシェルに未引用で渡さない
- 利用者供給のホスト一覧を、そのまま `eval` や `Invoke-Expression` に渡さない
- dry-runでも、認証情報をログに出さない
- レポートにIPやホスト名は出てよいが、認証トークンは出さない

---

## 2.14 テスト方法

純粋関数 `classify` からテストする。

```python
import pytest

from samples.python.ping_lib import classify  # 分割後の想定


@pytest.mark.parametrize(
    ("usage", "expected"),
    [
        (79.9, "OK"),
        (80.0, "WARNING"),
        (90.0, "CRITICAL"),
        (100.0, "CRITICAL"),
    ],
)
def test_classify(usage: float, expected: str) -> None:
    assert classify(usage, warn=80.0, crit=90.0) == expected
```

I/Oはモックする。

```python
def test_check_all_partial_failure():
    def fetch(host: str) -> float:
        if host == "bad":
            raise TimeoutError("timeout")
        return 10.0

    results, code = check_all(["good", "bad"], 80, 90, fetch)
    assert code == 2
    assert results[1].status == "TIMEOUT"
```

---

## 章末問題

### 問題1

「古いログを消す」作業について、要件を検証可能な文で5つ書け。dry-runと再実行性を含めること。

### 問題2

次の疑似コードの欠陥を指摘せよ。

```text
for host in hosts:
  restart_service(host)
print("done")
exit 0
```

### 問題3

ホスト100台へ直列で、1台30秒タイムアウトのAPIを叩く最悪時間を見積もれ。緩和策を二つ書け。

### 問題4

空のホスト一覧を成功（終了コード0）にする運用と、設定誤り（終了コード1）にする運用の、それぞれの向き先を述べよ。

### 問題5

状態をファイルに残す再実行設計と、毎回フルスキャンする設計の長所短所を比較せよ。

---

## 解答と解説

### 問題1（例）

1. 対象は `/var/log/myapp/` 配下の `*.log` のみ
2. 最終更新が30日超のファイルを候補とする
3. `--dry-run` では削除せず候補をstdoutへCSV出力する
4. 本番実行では削除前にパスを `work/cleanup.log` へ追記する
5. 既に追記済みのパスはスキップする（再実行安全）

### 問題2

- 失敗しても終了コード0
- dry-runも確認もない破壊的操作
- 部分失敗の記録がない
- タイムアウトがない

### 問題3

最悪 100×30秒 = 3000秒。緩和: 同時実行数制限付き並列、タイムアウト短縮、キャッシュ、失敗の早期打ち切り方針。

### 問題4

成功扱いは「対象ゼロが正常な日もある」定期ジョブ向き。誤り扱いは「一覧必須」な手動/設定必須ジョブ向き。`opsctl` では空一覧を終了コード1とする。

### 問題5

状態ファイル方式は再実行が速いが状態破損に弱い。フルスキャンは実装が単純で遅い。削除系は状態追記、照会系はフルスキャンが無難なことが多い。

---

## 実装演習

### 演習A

証明書残日数判定の純粋関数を疑似コードで書き、境界（0日、30日、31日）の期待値表を作れ。

### 演習B

第1章の `count_hosts` を拡張し、重複ホストを検出して終了コード2にする。重複一覧はstderrへ出す。

### 演習C

`02_ping_check.py` を実行し、dry-runと本番相当（ラボネットワーク）のレポート差を観察せよ。本番ネットワークへの無計画な大量pingは行わないこと。

---

## 次章予告

第3章では、三言語のデータ型とJSON/CSV/YAMLを比較し、型と文字コードの差で起きる運用事故を防ぐ。


---


<!-- SOURCE: 03_data_types_and_structures.md -->

# 第3章 データ型とデータ構造

## 学習目標

この章を終えると、次ができるようになる。

- Python、Bash、PowerShellの基本型の違いを説明できる
- 文字列、数値、真偽、配列、辞書、null相当を用途に応じて選べる
- 文字コードと改行を意識してテキストを扱える
- JSON / CSV を読み書きし、YAMLの位置づけを説明できる

前提: 第1章〜第2章の入出力と問題分解。

サンプルコードは学習用である。本番の文字コードやロケールは対象システムで確認すること。

---

## 3.1 基本概念

**データ型**は、値がどのような種類かを示す分類である。

**データ構造**は、複数の値をどう束ねるかを示す形である。

スクリプトでは、OSコマンドやファイルが返す「文字列」を、必要なら数値や構造化データへ変換する。変換を省略すると、`"10"` と `10` の比較ミスや、CSVの列ずれが起きる。

---

## 3.2 文字列

| 言語 | 型の呼び方 | 主な特徴 |
|------|------------|----------|
| Python | `str` | Unicode文字列。スライスやメソッドが豊富 |
| Bash | 文字列が基本 | 型宣言がほぼ無い。引用符が安全の要 |
| PowerShell | `System.String` | .NET文字列。単一/二重引用符で展開が異なる |

Python:

```python
host = "web01.example.invalid"
assert host.startswith("web")
assert host.split(".")[0] == "web01"
```

Bash:

```bash
host="web01.example.invalid"
prefix="${host%%.*}"
echo "${prefix}"   # web01
# 必ず引用する
echo "${host}"
```

PowerShell:

```powershell
$hostName = 'web01.example.invalid'
$hostName.Split('.')[0]   # web01
```

PowerShellの二重引用符は変数展開する。意図しない展開を避けるなら単一引用符を使う。

---

## 3.3 整数と小数

| 言語 | 整数 | 小数 |
|------|------|------|
| Python | `int`（桁数制限が実質ゆるい） | `float`（IEEE754）、正確さが要るなら `decimal` |
| Bash | 算術展開 `$(( ))` は整数 | 小数は `bc` や外部へ委譲することが多い |
| PowerShell | `[int]`, `[long]` など | `[double]`, `[decimal]` |

Python:

```python
used = 85
total = 100
percent = used / total * 100
assert percent == 85.0
```

Bash（整数パーセント）:

```bash
used=85
total=100
percent=$(( used * 100 / total ))
echo "${percent}"
```

PowerShell:

```powershell
[double]$used = 85
[double]$total = 100
$percent = $used / $total * 100
```

ディスク使用率のような閾値判定は、最初から整数パーセントに揃えると三言語で比較が安定する。

---

## 3.4 真偽値

| 言語 | 真 / 偽 | 注意 |
|------|---------|------|
| Python | `True` / `False` | 空文字、空リスト、0は偽と評価される |
| Bash | コマンドの終了コード0が成功 | 文字列 `true` はただの文字列 |
| PowerShell | `$true` / `$false` | 多くの値が真偽に変換されうる |

Bashで真偽を変数に持つなら、`0`/`1` か `yes`/`no` を決め、文字列比較する。

```bash
dry_run=1
if [[ "${dry_run}" -eq 1 ]]; then
  echo "dry-run" >&2
fi
```

---

## 3.5 配列、リスト

| 言語 | 代表 | 特徴 |
|------|------|------|
| Python | `list` | 可変、異型要素可。順序あり |
| Bash | 配列 `arr=(a b)` | 単語分割と引用が難しい |
| PowerShell | `Object[]` / `List` | パイプラインと相性が良い |

Python:

```python
hosts = ["web01.example.invalid", "web02.example.invalid"]
hosts.append("db01.example.invalid")
```

Bash:

```bash
hosts=("web01.example.invalid" "web02.example.invalid")
hosts+=("db01.example.invalid")
for host in "${hosts[@]}"; do
  echo "${host}"
done
```

PowerShell:

```powershell
$hosts = @('web01.example.invalid', 'web02.example.invalid')
$hosts += 'db01.example.invalid'
```

Bashで `for host in $(cat file)` は使わない。第1章の `while read` を使う。

---

## 3.6 辞書、ハッシュテーブル

| 言語 | 代表 | 用途 |
|------|------|------|
| Python | `dict` | 設定、集計、JSONとの相互変換 |
| Bash | 連想配列 `declare -A`（Bash 4+） | 簡易マップ。複雑ならPythonへ |
| PowerShell | `hashtable` `@{ }` | 設定とJSON変換 |

Python:

```python
thresholds = {"warn": 80, "crit": 90}
assert thresholds["warn"] == 80
```

Bash 4+:

```bash
declare -A thresholds=([warn]=80 [crit]=90)
echo "${thresholds[warn]}"
```

PowerShell:

```powershell
$thresholds = @{ warn = 80; crit = 90 }
$thresholds['warn']
```

macOSの古いBash 3.xでは連想配列が使えない。可搬性が要るならPythonかPowerShell 7へ寄せる。

---

## 3.7 null相当値

| 言語 | 無いことを表す値 | 判定 |
|------|------------------|------|
| Python | `None` | `is None` |
| Bash | 空文字、未設定変数 | `${var:-}`, `[[ -z ]]`。`set -u` 下では未設定参照がエラー |
| PowerShell | `$null` | `$null -eq $value` |

取得失敗を `0` と表現しない。使用率0%と取得失敗が区別できなくなる。

```python
usage: float | None
if usage is None:
    status = "ERROR"
```

---

## 3.8 型変換

明示変換を基本にする。

Python:

```python
percent = int(float("85.7"))  # 85
```

Bash:

```bash
n="42"
expr=$(( n + 1 ))
```

PowerShell:

```powershell
[int]'42' + 1
[double]'85.7'
```

悪い例（暗黙依存）:

```python
# "90" >= 80 は Python 3 では TypeError
# 古い感覚や他言語の癖で書いてしまう
```

改善:

```python
if int(value) >= 80:
    ...
```

---

## 3.9 文字コード

**文字コード**は、文字をバイト列へ対応づける規則である。現代の既定は UTF-8 が多い。

事故例:

- WindowsのCP932（Shift_JIS系）のログを、UTF-8前提で読む
- 赤シートが `���` になる
- ある1行だけ壊れてCSV全体が読えない

方針:

1. 入出力の encoding を明示する（Pythonは `encoding="utf-8"`）
2. 既存ログのコードページを調べてから読む
3. 新規成果物はUTF-8（必要ならBOM付きを相手に合わせる）

Python:

```python
text = path.read_text(encoding="utf-8")
path.write_text(text, encoding="utf-8", newline="\n")
```

PowerShell 7:

```powershell
Get-Content -LiteralPath $path -Encoding utf8
Set-Content -LiteralPath $path -Value $text -Encoding utf8
```

Windows PowerShell 5.1の `Set-Content` 既定はUTF-8と限らない。本書は PowerShell 7 を主とし、5.1では `-Encoding` を明示する。

---

## 3.10 日付と時刻

運用では「いつ」が監査と期限判定の中心になる。

推奨:

- 内部計算はUTCまたはモノトニック時計
- 表示はISO 8601（例: `2026-07-30T04:09:00+09:00`）
- タイムゾーンを省略した文字列をサーバ間で共有しない

Python:

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
print(now.isoformat())
```

Bash（GNU date）:

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

macOSの `date` はGNUとフラグが違う。可搬な日付処理はPythonが安全である。

PowerShell:

```powershell
[DateTimeOffset]::UtcNow.ToString('o')
```

証明書期限などは第15章で扱う。

---

## 3.11 JSON

**JSON**は、オブジェクトと配列をテキストで表す共通形式である。API連携の標準に近い。

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("root must be an object")
    return data


def main() -> int:
    path = Path(sys.argv[1])
    try:
        data = load_json(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 2
    print(data.get("defaults", {}).get("timeout_seconds"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

PowerShell:

```powershell
$data = Get-Content -LiteralPath .\config\sample.json -Raw | ConvertFrom-Json
$data.defaults.timeout_seconds
```

Bashは `jq` を使う。

```bash
jq -r '.defaults.timeout_seconds' config/sample.json
```

`jq` が無い環境では Python に寄せる。

---

## 3.12 CSV

**CSV**は表形式のテキストである。报表や棚卸しに向く。

注意:

- カンマや改行を含むフィールドは引用符が必要
- 自前の `split(",")` は壊れる
- 言語標準のCSVライブラリを使う

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "status", "detail"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    out = Path(sys.argv[1])
    rows = [
        {"host": "web01.example.invalid", "status": "OK", "detail": "85"},
        {"host": "web02.example.invalid", "status": "CRITICAL", "detail": "95"},
    ]
    write_report(out, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

PowerShell:

```powershell
$rows = @(
  [pscustomobject]@{ host = 'web01.example.invalid'; status = 'OK'; detail = '85' }
  [pscustomobject]@{ host = 'web02.example.invalid'; status = 'CRITICAL'; detail = '95' }
)
$rows | Export-Csv -LiteralPath .\reports\disk.csv -NoTypeInformation -Encoding utf8
```

---

## 3.13 YAMLの概要

**YAML**は設定ファイルでよく使う、インデント基調の形式である。

長所: 人が読みやすい。コメントが書ける。

短所: 暗黙型変換やアンカーなど、罠がある。`YES`/`NO` が真偽になる歴史的問題など、実装依存に注意する。

Python（PyYAML）:

```python
import yaml
from pathlib import Path

data = yaml.safe_load(Path("config/opsctl.yaml").read_text(encoding="utf-8"))
timeout = data["defaults"]["timeout_seconds"]
```

`yaml.load` ではなく **`safe_load`** を使う。任意コード実行のリスクを避けるためである。

PowerShellでは `powershell-yaml` モジュールや、設定をJSONに寄せる選択がある。本書の `opsctl` 設定はYAMLとし、読み込みはPythonを主とする。

BashでYAMLを本格処理しない。`yq` がある場合のみ補助的に使う。

---

## 3.14 最小構成から実務へ

### 悪いコード

```bash
# 自前CSV、文字コード無視、型なし
echo $host,$usage >> report.csv
```

問題点:

- フィールドにカンマがあると列が壊れる
- 文字コードと改行が環境依存
- ヘッダー欠落や追記競合

### 改善後（Pythonで安全にCSV）

`samples/python/03_write_status_csv.py` を参照。

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

logger = logging.getLogger("write_status_csv")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write status CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--status", required=True, choices=["OK", "WARNING", "CRITICAL", "ERROR"])
    parser.add_argument("--detail", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(message)s")

    if any(ch.isspace() for ch in args.host):
        logger.error("host must not contain whitespace")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.output.exists()
    with args.output.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "status", "detail"])
        if write_header:
            writer.writeheader()
        writer.writerow(
            {"host": args.host, "status": args.status, "detail": args.detail}
        )

    logger.info("appended row to %s", args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

並列追記ではファイルロックが必要になる（第6章）。単一プロセス追記に限定する。

---

## 3.15 セキュリティ上の注意点

- YAMLの危険なタグや `!!python/object` を有効にしない（`safe_load`）
- 利用者入力をJSONに埋め込むとき、文字列連結ではなくライブラリのシリアライズを使う
- CSVインジェクション（セル先頭の `=` など）が表計算ソフトで問題になる場合がある。外部公開レポートではサニタイズ方針を決める

---

## 3.16 テスト方法

```python
import json
from pathlib import Path


def test_json_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "a.json"
    path.write_text(json.dumps({"defaults": {"timeout_seconds": 30}}), encoding="utf-8")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["defaults"]["timeout_seconds"] == 30
```

文字コードテストでは、意図的に不正UTF-8を渡し、例外または置換方針を固定する。

---

## 章末問題

### 問題1

Bashで小数のディスク使用率を直接比較するのが難しい理由と、代替を二つ述べよ。

### 問題2

`None` / 空文字 / `0` を混同すると起きる運用事故を一つ具体的に書け。

### 問題3

次のCSV行を自前splitするとどう壊れるか説明せよ。

```text
web01,"disk full, needs cleanup",CRITICAL
```

### 問題4

PowerShell 5.1と7でファイル書き込みの文字コードに差が出る理由を述べよ。

### 問題5

設定にYAMLを選ぶ理由と、JSONを選ぶ理由をそれぞれ一つずつ書け。

---

## 解答と解説

### 問題1

`$(( ))` が整数だから。代替: 整数パーセントに丸める、`bc`、Python/PowerShellへ処理を移す。

### 問題2

ディスク取得失敗を0%と記録し、正常と誤認してアラートが出ない。

### 問題3

カンマが列区切りとフィールド内の両方に現れ、列数がずれる。

### 問題4

既定エンコーディングの歴史的差がある。`-Encoding` を明示し、可能ならPowerShell 7に揃える。

### 問題5

YAML: コメントと人が読む設定向き。JSON: 型が単純でツール共通、コメント不要な機械生成向き。

---

## 実装演習

### 演習A

`config/opsctl.yaml` を読み、`defaults.timeout_seconds` をstdoutへ出すPythonスクリプトを書け。失敗時は終了コード2。

### 演習B

ホストと使用率の組を受け取り、CSVを書くPowerShellスクリプトを書け。UTF-8を明示すること。

### 演習C

不正なUTF-8バイトを含むファイルを用意し、Pythonで `errors="strict"` と `errors="replace"` の差を観察せよ。運用ではどちらを選ぶか理由を書け。

---

## 次章予告

第4章では、条件分岐と反復を読みやすく保つ技法（早期リターン、異常系先行）を三言語で扱う。


---


<!-- SOURCE: 04_control_flow.md -->

# 第4章 制御構文

## 学習目標

- if / switch(case) / for / while / break / continue を三言語で使える
- 比較演算子と論理演算子の言語差を説明できる
- ネストを浅くし、早期リターンと異常系先行で読める分岐を書ける

---

## 4.1 基本概念

**制御構文**は、実行の流れを分岐・反復させる構文である。

運用スクリプトでは、正常系より異常系の分岐が多い。深くなる前に、関数の入口で不正を弾く。

---

## 4.2 最小構成のコード

閾値判定だけの最小例である。入力検証と終了コードはまだ薄い。

Python:

```python
#!/usr/bin/env python3
import sys

usage = float(sys.argv[1])
if usage >= 90:
    print("CRITICAL")
elif usage >= 80:
    print("WARNING")
else:
    print("OK")
```

Bash:

```bash
#!/usr/bin/env bash
usage="$1"
if (( usage >= 90 )); then
  echo CRITICAL
elif (( usage >= 80 )); then
  echo WARNING
else
  echo OK
fi
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
param([int]$Usage)
if ($Usage -ge 90) { 'CRITICAL' }
elseif ($Usage -ge 80) { 'WARNING' }
else { 'OK' }
```

問題点（この最小構成）:

- 引数不足や非数値が未処理
- 終了コードが常に0に近い
- ログがない
- warn/crit を変更できない

実務向けの改善は 4.9 節と `samples/` を参照する。

---

## 4.3 if

Python:

```python
if usage >= crit:
    status = "CRITICAL"
elif usage >= warn:
    status = "WARNING"
else:
    status = "OK"
```

Bash:

```bash
if [[ "${usage}" -ge "${crit}" ]]; then
  status=CRITICAL
elif [[ "${usage}" -ge "${warn}" ]]; then
  status=WARNING
else
  status=OK
fi
```

PowerShell:

```powershell
if ($Usage -ge $Crit) {
    $status = 'CRITICAL'
}
elseif ($Usage -ge $Warn) {
    $status = 'WARNING'
}
else {
    $status = 'OK'
}
```

Bashの `[[ ]]` を使う。古い `[ ]` より安全で機能が多い。

---

## 4.4 switch / case

Bashの `case`:

```bash
case "${status}" in
  OK) echo 0 ;;
  WARNING) echo 0 ;;
  CRITICAL) echo 3 ;;
  *) echo 2 ;;
esac
```

PowerShellの `switch`:

```powershell
switch ($status) {
    'OK' { 0 }
    'WARNING' { 0 }
    'CRITICAL' { 3 }
    default { 2 }
}
```

Pythonは 3.10以降で `match` がある。単純な対応表なら辞書でもよい。

```python
EXIT_BY_STATUS = {"OK": 0, "WARNING": 0, "CRITICAL": 3}
code = EXIT_BY_STATUS.get(status, 2)
```

---

## 4.5 for / while / break / continue

Python:

```python
for host in hosts:
    if host in skip:
        continue
    if hard_fail(host):
        break
```

Bash:

```bash
for host in "${hosts[@]}"; do
  [[ -n "${skip[${host}]+x}" ]] && continue
  ping -c1 "${host}" || break
done
```

PowerShell:

```powershell
foreach ($host in $hosts) {
    if ($skip -contains $host) { continue }
    if (-not (Test-Connection -ComputerName $host -Count 1 -Quiet)) { break }
}
```

`while` は条件が先に立つ反復である。ファイル読み込みの `while read` が代表例である。

無限ループには必ず打ち切り条件（回数上限、タイムアウト、フラグ）を入れる。

---

## 4.6 条件式、比較、論理演算

| 意味 | Python | Bash `[[ ]]` | PowerShell |
|------|--------|--------------|------------|
| 等しい | `==` | `=` または `==` | `-eq` |
| 異なる | `!=` | `!=` | `-ne` |
| 数値比較 | `<` `>` など | `-lt` `-gt` など | `-lt` `-gt` |
| 論理積 | `and` | `&&` | `-and` |
| 論理和 | `or` | `\|\|` | `-or` |
| 否定 | `not` | `!` | `-not` |

PowerShellで `==` を使うと別意味になる場面がある。比較演算子は `-eq` 系を使う。

文字列と数値の比較を混ぜない。先に型を揃える（第3章）。

---

## 4.7 ネストを深くしない方法

深いネストの徴候:

- 右端にコードが寄っていく
- `else` の対応が目で追えない
- 同じ条件を二重に書いている

対策:

1. 異常を先に `return` / `exit`
2. 判定を関数に切り出す
3. ガード節で階層を減らす
4. 複雑なら表駆動（辞書やcase）にする

---

## 4.8 早期リターンと異常系先行

### 悪いコード

```python
def deploy(config, dry_run: bool) -> int:
    if config is not None:
        if config.get("target"):
            if validate(config):
                if dry_run:
                    print("would deploy")
                    return 0
                else:
                    run_deploy(config)
                    return 0
            else:
                print("invalid")
                return 1
        else:
            print("no target")
            return 1
    else:
        print("no config")
        return 1
```

問題点: 正常系がネストの最深部に埋もれる。失敗経路が散る。

### 改善後

```python
def deploy(config: dict | None, dry_run: bool) -> int:
    if config is None:
        print("no config", file=sys.stderr)
        return 1
    if not config.get("target"):
        print("no target", file=sys.stderr)
        return 1
    if not validate(config):
        print("invalid", file=sys.stderr)
        return 1
    if dry_run:
        print("would deploy", file=sys.stderr)
        return 0
    run_deploy(config)
    return 0
```

Bashでも同じ発想で早期 `exit` する。

```bash
[[ -n "${config_file}" ]] || { echo "no config" >&2; exit 1; }
[[ -f "${config_file}" ]] || { echo "missing file" >&2; exit 1; }
```

PowerShell:

```powershell
function Invoke-Deploy {
    param($Config, [switch]$DryRun)
    if ($null -eq $Config) {
        [Console]::Error.WriteLine('no config')
        return 1
    }
    if (-not $Config.target) {
        [Console]::Error.WriteLine('no target')
        return 1
    }
    if ($DryRun) {
        [Console]::Error.WriteLine('would deploy')
        return 0
    }
    # run deploy
    return 0
}
```

---

## 4.9 実務向けに改善したコード

全文は次を参照する。

- `samples/python/04_classify_usage.py`
- `samples/bash/04_classify_usage.sh`
- `samples/powershell/04_classify_usage.ps1`

改善点:

- 引数の型と範囲を検証する
- warn <= crit を強制する
- CRITICAL は終了コード3、設定誤りは1
- 進捗・エラーは stderr、判定結果は stdout

実行例:

```bash
python3 samples/python/04_classify_usage.py --usage 95
# CRITICAL ; exit 3

python3 samples/python/04_classify_usage.py --usage 85
# WARNING ; exit 0

python3 samples/python/04_classify_usage.py --usage 10 --warn 90 --crit 80
# stderr: warn must be <= crit ; exit 1

bash samples/bash/04_classify_usage.sh --usage 95
pwsh samples/powershell/04_classify_usage.ps1 -Usage 95
```

---

## 4.10 セキュリティ上の注意点

- 利用者入力を条件式に埋め込む前に型と範囲を検証する
- Bashで `eval` による動的分岐を作らない
- PowerShellで `Invoke-Expression` による動的分岐を作らない

---

## 4.11 テスト方法

境界値を表で固定する。実装は `samples/python/04_classify_usage.py` の `classify` を対象にする。

```python
import pytest
from importlib.machinery import SourceFileLoader

mod = SourceFileLoader(
    "classify_usage",
    "samples/python/04_classify_usage.py",
).load_module()


@pytest.mark.parametrize(
    ("usage", "expected"),
    [(79.9, "OK"), (80.0, "WARNING"), (90.0, "CRITICAL")],
)
def test_boundaries(usage, expected):
    assert mod.classify(usage, 80, 90) == expected


def test_warn_gt_crit():
    with pytest.raises(ValueError):
        mod.classify(10, warn=90, crit=80)
```

`tests/test_classify_usage.py` も参照する。

---

## 章末問題

1. ネスト4段の if を、早期リターンで書き直せ（題材は任意でよい）。
2. PowerShellで文字列比較に `==` を使ったときのリスクを調べて書け。
3. `continue` と `break` の違いを、ホスト疎通ループの例で説明せよ。
4. WARNINGを終了コード0にする方針の利点と欠点を述べよ。
5. Bashの `[[ a = b ]]` と `[[ a == b ]]` について、チーム内の統一方針を一つ提案せよ。

## 解答と解説

1. 異常条件を先に return し、最後に正常処理を置く。
2. 代入や意図しない型変換と読み違えやすい。`-eq` を使う。
3. `continue` は次ホストへ。`break` はループ全体を終了。
4. 利点: 監視のCRITICALと分離できる。欠点: WARNING放置が成功扱いになる。レポート必須。
5. 可読性のため `==` に統一する、など。どちらか一方に固定する。

## 実装演習

- `04_classify_usage.py` と同等の判定をBash（整数）とPowerShellで実装する。
- 異常系テストを3本以上書く。

## 次章予告

第5章では関数とモジュールで責務を分け、副作用と純粋関数を意識した再利用を扱う。


---


<!-- SOURCE: 05_functions_and_modules.md -->

# 第5章 関数とモジュール

## 学習目標

この章を終えると、次ができるようになる。

- 関数の目的、引数、戻り値、スコープ、副作用を三言語で説明できる
- 純粋関数と副作用のある関数を見分け、境界を意識して分割できる
- モジュール化と名前空間の役割を説明し、責務ごとにファイルを分けられる
- 「関数に切り出すべきか」を具体的な判断基準で決められる
- Pythonモジュール、Bash関数、PowerShell関数とモジュールの書き方を実装できる

前提: 第1章〜第4章の入出力、終了コード、データ型、制御構文。

---

## 5.1 基本概念

**関数**は、入力を受け取り、決まった処理を行い、結果を返すコードのまとまりである。
名前を付けることで、呼び出し側は内部の実装を読まなくても、その関数が何をするか推測できる。
同じ処理を複数箇所に書く代わりに関数を一つ用意すれば、修正箇所も一つで済む。

**引数**は、関数の呼び出し時に渡す入力である。
**戻り値**は、関数が呼び出し元へ返す結果である。
戻り値を持たない関数もあるが、その場合は副作用（後述）が処理の本体になる。

**モジュール**は、関数や変数をひとまとめにして、他のコードから再利用できるようにした単位である。
Pythonの `.py` ファイル、PowerShellの `.psm1` ファイルが典型例である。
Bashには言語標準のモジュール機構が無く、ファイルを `source` することで代用する。

関数とモジュールは、どちらも「境界を作る」ための道具である。
境界がはっきりしていれば、変更の影響範囲を予測でき、テストも単独で書ける。
境界が曖昧なコードは、一箇所の修正が予期しない場所へ波及する。

---

## 5.2 引数と戻り値

三言語とも、引数には位置引数と名前付き引数がある。

Python:

```python
def classify(usage: float, warn: float = 80.0, crit: float = 90.0) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


result_a = classify(95.0)
result_b = classify(usage=95.0, warn=70.0, crit=85.0)
```

Bash:

```bash
classify() {
  local usage="$1"
  local warn="${2:-80}"
  local crit="${3:-90}"
  if (( usage >= crit )); then
    echo CRITICAL
  elif (( usage >= warn )); then
    echo WARNING
  else
    echo OK
  fi
}

result_a="$(classify 95)"
result_b="$(classify 95 70 85)"
```

Bashの関数は、戻り値として整数の終了コード（`return`）しか返せない。
文字列を返したいときは、標準出力へ `echo` し、呼び出し側でコマンド置換（`$( )`）を使う。
この違いを忘れると、`return "OK"` のような書き方をしてしまい、意図しない終了コードになる。

PowerShell:

```powershell
function Get-UsageStatus {
    param(
        [double]$Usage,
        [double]$Warn = 80,
        [double]$Crit = 90
    )
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}

$resultA = Get-UsageStatus -Usage 95
$resultB = Get-UsageStatus -Usage 95 -Warn 70 -Crit 85
```

PowerShellの関数は、`return` した値だけでなく、パイプラインへ出力した値もすべて戻り値として扱う。
関数内で `Write-Output` や素の式を書くと、呼び出し元には配列として渡ることがある。
デバッグ用の出力を関数内に残すと、戻り値が汚れる原因になる。

```powershell
function Get-UsageStatusBad {
    param([double]$Usage)
    Write-Output "debug: usage=$Usage"
    if ($Usage -ge 90) { return 'CRITICAL' }
    return 'OK'
}

# $status には "debug: usage=95" と "CRITICAL" の配列が入ってしまう
$status = Get-UsageStatusBad -Usage 95
```

デバッグ表示は `Write-Verbose` や `[Console]::Error.WriteLine()` を使い、標準出力（パイプライン）を汚さない。

---

## 5.3 スコープ

**スコープ**は、変数や関数の名前が有効な範囲である。

Python:

```python
warn_default = 80.0


def classify(usage: float) -> str:
    local_note = "temporary"  # この関数の中だけで有効
    if usage >= warn_default:  # 関数の外の変数を読める
        return "WARNING"
    return "OK"


print(local_note)  # NameError: local_note は関数の外から見えない
```

Bashの関数は、既定では変数を共有する。
`local` を付けない限り、関数内の代入がグローバルへ漏れる。

```bash
warn_default=80

classify() {
  local usage="$1"
  # local を付けないと呼び出し元のスコープを汚染する
  note="temporary"
  if (( usage >= warn_default )); then
    echo WARNING
  else
    echo OK
  fi
}

classify 95
echo "${note}"  # local を忘れると呼び出し元に "temporary" が漏れる
```

PowerShellのスコープはやや独特である。
関数内で変数を読むことはできるが、代入は既定で関数ローカルのスコープに作られる。

```powershell
$warnDefault = 80

function Get-UsageStatus2 {
    param([double]$Usage)
    $note = 'temporary'  # 関数ローカル
    if ($Usage -ge $warnDefault) { return 'WARNING' }
    return 'OK'
}

Get-UsageStatus2 -Usage 95 | Out-Null
# $note は呼び出し元には存在しない
```

三言語に共通する方針は、関数の外の変数を暗黙に書き換えないことである。
必要な値は引数として渡し、結果は戻り値として返す。
Bashで `local` を書き忘れないことは、レビューで必ず確認する項目にする。

---

## 5.4 副作用と純粋関数

**副作用**は、関数が戻り値を返す以外に、外部の状態を変更することである。
ファイル書き込み、ネットワーク呼び出し、グローバル変数の変更、標準出力への表示はすべて副作用である。

**純粋関数**は、同じ引数に対して常に同じ結果を返し、副作用を持たない関数である。
純粋関数は、外部環境やタイミングに依存しないため、単体テストが書きやすい。

判定と入出力を一つの関数に混ぜると、テストのたびにファイルやネットワークを用意する必要が出る。

### 悪いコード

```python
from __future__ import annotations

import sys
from pathlib import Path


def check_and_report(usage: float, warn: float, crit: float, report_path: Path) -> int:
    if usage >= crit:
        status = "CRITICAL"
    elif usage >= warn:
        status = "WARNING"
    else:
        status = "OK"

    # 判定とファイル書き込みが同じ関数に混在している
    with report_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{usage},{status}\n")

    if status == "CRITICAL":
        return 3
    return 0
```

問題点:

- `classify` 相当の判定だけを単体テストしたくても、ファイルI/Oが必ず走る
- テストのたびに一時ファイルの後始末が必要になる
- 判定ロジックを他のコマンドから再利用しづらい

### 改善後

```python
from __future__ import annotations

from pathlib import Path


def classify(usage: float, warn: float, crit: float) -> str:
    """純粋関数。I/Oを一切行わない。"""
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


def status_to_exit(status: str) -> int:
    """純粋関数。"""
    return 3 if status == "CRITICAL" else 0


def append_report(report_path: Path, usage: float, status: str) -> None:
    """副作用を持つ関数。ファイルへ追記する。"""
    with report_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{usage},{status}\n")


def check_and_report(usage: float, warn: float, crit: float, report_path: Path) -> int:
    """純粋関数と副作用のある関数を組み合わせる薄い層。"""
    status = classify(usage, warn, crit)
    append_report(report_path, usage, status)
    return status_to_exit(status)
```

`classify` と `status_to_exit` は、引数だけから結果が決まる。
モックもファイルも要らず、値を入れて結果を比べるだけでテストできる。
`append_report` は副作用を持つが、役割が一つに絞られているため、書き込み形式を変えるときもここだけを直せばよい。

Bashでも同じ発想で分ける。

```bash
classify() {
  local usage="$1" warn="$2" crit="$3"
  if (( usage >= crit )); then
    echo CRITICAL
  elif (( usage >= warn )); then
    echo WARNING
  else
    echo OK
  fi
}

append_report() {
  local report_path="$1" usage="$2" status="$3"
  echo "${usage},${status}" >> "${report_path}"
}
```

PowerShellでも同様である。

```powershell
function Get-UsageStatus3 {
    param([double]$Usage, [double]$Warn, [double]$Crit)
    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}

function Add-ReportLine {
    param([string]$ReportPath, [double]$Usage, [string]$Status)
    Add-Content -LiteralPath $ReportPath -Value "$Usage,$Status" -Encoding utf8
}
```

判定を純粋関数に、I/Oを別の関数に分けておくと、単体テストの範囲を判定側だけに絞れる。
I/O側は結合テストや実行例で確認する方針にできる（第13章）。

---

## 5.5 モジュール化と名前空間

**名前空間**は、同じ名前の関数や変数が衝突しないように分けるための区画である。

Pythonでは、ファイル（モジュール）やパッケージが名前空間になる。

```python
# hostlib.py
def load_hosts(path):
    ...

# main.py
import hostlib

hosts = hostlib.load_hosts("config/hosts.txt")
```

`import hostlib` としておけば、`hostlib.load_hosts` と他のモジュールの `load_hosts` が衝突しない。
`from hostlib import *` は名前空間を潰してしまうため、運用スクリプトでは避ける。

Bashには名前空間が無い。
関数名がすべて一つのフラットな空間に置かれるため、`source` した複数のファイルで同名関数を定義すると、後から読み込んだ方で上書きされる。

```bash
source lib/hostlib.sh
source lib/disklib.sh
# 両方に classify() があると、後から source した方が有効になる
```

対策として、関数名にプレフィックスを付ける運用が現実的である。

```bash
hostlib::load_hosts() { ... }
disklib::classify() { ... }
```

PowerShellのモジュール（`.psm1`）は、既定でエクスポートした関数だけを呼び出し元の名前空間に見せる。

```powershell
# HostLib.psm1
function Get-Hosts {
    param([string]$Path)
    Get-Content -LiteralPath $Path | Where-Object { $_ -and -not $_.StartsWith('#') }
}

Export-ModuleMember -Function Get-Hosts
```

```powershell
Import-Module ./HostLib.psm1
Get-Hosts -Path config/hosts.txt
```

`Export-ModuleMember` を書かないと、モジュール内のすべての関数が公開される。
内部だけで使う補助関数は、意図してエクスポートから外す。

---

## 5.6 責務分離と分割の判断基準

**責務**は、そのコードが担う一つの役割である。

一つの関数やモジュールに複数の責務が混ざると、片方の都合の変更がもう片方を壊す。

分割すべきかどうかを、次の基準で判断する。

1. 同じ処理が二箇所以上に現れている、または現れそうである
2. 名前を付けたほうが、呼び出し側のコードが読みやすくなる
3. 単体でテストしたい処理である
4. 外部I/O（ファイル、ネットワーク、外部コマンド）と、判定や計算が混在している
5. 一つの関数の行数が、画面をスクロールしないと読めない長さになっている
6. 関数名に「and」が要る（例: `load_and_validate_and_report`）

6番目の兆候が出たら、関数を分ける具体的な合図である。
`load_and_validate_and_report` は、`load`、`validate`、`report` の三つに分けられる。

過剰分割にも注意する。
一度しか呼ばれず、内容が数行で、単体テストの必要も薄い処理まで無理に切り出すと、呼び出しをたどるだけで時間を取られる。
分割の目的は行数の削減ではなく、読解とテストの単位を明確にすることである。

---

## 5.7 Pythonのモジュール

Pythonでは、ファイルがそのままモジュールになる。

```text
project/
  opsctl/
    __init__.py
    hostlib.py
    disklib.py
  main.py
```

```python
# opsctl/hostlib.py
from __future__ import annotations

from pathlib import Path


def load_hosts(path: Path) -> list[str]:
    if not path.is_file():
        raise FileNotFoundError(f"hosts file not found: {path}")
    hosts: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        hosts.append(line)
    return hosts
```

```python
# main.py
from __future__ import annotations

import sys
from pathlib import Path

from opsctl.hostlib import load_hosts


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    hosts = load_hosts(Path(args[0]))
    print(len(hosts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`__init__.py` を置くと `opsctl` がパッケージとして扱われ、`from opsctl.hostlib import load_hosts` のように階層を持ったモジュール構成にできる。
テストからも同じ書き方で `import` できるため、第13章のテストと相性がよい。

相対importと絶対importが混在すると、実行方法（`python main.py` か `python -m opsctl.main` か）によって壊れることがある。
運用スクリプトでは絶対import（`from opsctl.hostlib import ...`）を基本にし、実行はパッケージのルートから行う。

---

## 5.8 Bashの関数

Bashの関数定義は二通りの書き方があるが、意味は同じである。

```bash
function greet {
  echo "hello, $1"
}

greet2() {
  echo "hello, $1"
}
```

本書では `name() { ... }` の形式に統一する。
`function` キーワードは省略しても動くため、記述を減らせる。

関数を別ファイルへ分け、`source` で読み込むと、Bashなりのモジュール化ができる。

```bash
# lib/hostlib.sh
hostlib::load_hosts() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "hosts file not found: ${path}" >&2
    return 1
  fi
  grep -v '^\s*#' "${path}" | grep -v '^\s*$'
}
```

```bash
#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/hostlib.sh"

hosts="$(hostlib::load_hosts config/hosts.txt)"
echo "${hosts}" | wc -l
```

`source` するパスは、実行時のカレントディレクトリに依存させない。
`BASH_SOURCE[0]` からスクリプト自身の場所を求め、そこからの相対パスで `lib/` を指す。

Bashの関数は、`local` を付けた変数以外はすべてグローバルになる。
第4章までの規約と同様、関数の先頭で受け取る引数を `local` 変数に写してから使うと、事故が減る。

---

## 5.9 PowerShellの関数とモジュール

PowerShellの関数は、`param()` ブロックで型付きの引数を受け取れる。

```powershell
function Get-DiskStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [double]$Usage,

        [double]$Warn = 80,
        [double]$Crit = 90
    )

    if ($Usage -ge $Crit) { return 'CRITICAL' }
    if ($Usage -ge $Warn) { return 'WARNING' }
    return 'OK'
}
```

`[CmdletBinding()]` を付けると、`-Verbose` や `-ErrorAction` など共通パラメータが自動的に使えるようになる。
関数名は動詞-名詞の形式（`Get-DiskStatus` など）にするのがPowerShellの慣例であり、`Get-Verb` で承認済みの動詞一覧を確認できる。

モジュール化には `.psm1` ファイルを使う。

```powershell
# modules/HostLib.psm1
function Get-HostList {
    [CmdletBinding()]
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "hosts file not found: $Path"
    }
    Get-Content -LiteralPath $Path |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ -and -not $_.StartsWith('#') }
}

Export-ModuleMember -Function Get-HostList
```

```powershell
Import-Module (Join-Path $PSScriptRoot 'modules/HostLib.psm1') -Force

$hosts = Get-HostList -Path 'config/hosts.txt'
Write-Output $hosts.Count
```

`$PSScriptRoot` は、実行中のスクリプトファイルが置かれているディレクトリを指す組み込み変数である。
これを基準にモジュールを読み込むと、カレントディレクトリに依存しない。

`Import-Module` に `-Force` を付けると、開発中にモジュールを編集したあとの再読み込みが確実になる。
本番運用では、意図しないバージョンでの上書きを避けるため、モジュールのバージョン管理も検討する。

---

## 5.10 実務向けサンプル: ディスク監視ロジックの関数分割

要件は第2章、第4章のディスク監視と同じ判定を使う。
ここでは、責務ごとに関数を分けたPython実装を示す。

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_CRITICAL = 3

logger = logging.getLogger("disk_report")


@dataclass
class HostUsage:
    host: str
    usage_percent: float


def load_usages(path: Path) -> list[HostUsage]:
    """副作用: ファイル読み込み。"""
    if not path.is_file():
        raise FileNotFoundError(f"usage file not found: {path}")
    usages: list[HostUsage] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            usages.append(HostUsage(host=row["host"], usage_percent=float(row["usage_percent"])))
    return usages


def classify(usage_percent: float, warn: float, crit: float) -> str:
    """純粋関数。"""
    if usage_percent >= crit:
        return "CRITICAL"
    if usage_percent >= warn:
        return "WARNING"
    return "OK"


def summarize_exit_code(statuses: list[str]) -> int:
    """純粋関数。"""
    if "CRITICAL" in statuses:
        return EXIT_CRITICAL
    return EXIT_OK


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    """副作用: ファイル書き込み。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["host", "usage_percent", "status"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify disk usage and write a report")
    parser.add_argument("--input", type=Path, required=True, help="host,usage_percent CSV")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warn", type=float, default=80.0)
    parser.add_argument("--crit", type=float, default=90.0)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stderr,
    )

    if args.warn > args.crit:
        logger.error("--warn must be <= --crit")
        return EXIT_USAGE

    try:
        usages = load_usages(args.input)
    except (OSError, ValueError, KeyError) as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    rows: list[dict[str, str]] = []
    statuses: list[str] = []
    for item in usages:
        status = classify(item.usage_percent, args.warn, args.crit)
        statuses.append(status)
        rows.append(
            {
                "host": item.host,
                "usage_percent": str(item.usage_percent),
                "status": status,
            }
        )

    write_report(args.output, rows)
    logger.info("wrote %s rows to %s", len(rows), args.output)
    return summarize_exit_code(statuses)


if __name__ == "__main__":
    sys.exit(main())
```

`load_usages` と `write_report` はI/Oを持つ関数、`classify` と `summarize_exit_code` は純粋関数として明確に分かれている。
`main` は、それらを順番に呼び出す薄い調整役に徹している。

完全な実行可能ファイルは `samples/python/05_disk_report.py` に置く。
対応するBash版は `samples/bash/05_disk_report.sh`、PowerShell版は `samples/powershell/05_disk_report.ps1` を参照する。

---

## 5.11 セキュリティ上の注意点

- 関数の引数に秘密情報（トークン、パスワード）を渡すときは、ログ関数や例外メッセージにそのまま埋め込まない
- Bashで `source` するファイルパスを利用者入力から組み立てない。任意のファイルを読み込ませる経路になる
- PowerShellの `Import-Module` にも同様の注意が要る。信頼できないパスからモジュールを読み込まない
- 副作用を持つ関数（削除、上書き、外部API呼び出し）は名前や配置を分け、レビューで見つけやすくする
- モジュール分割によって「どこかで検証しているはず」という思い込みが生まれやすい。入力検証の責務がどの関数にあるかをコメントや設計で明示する

---

## 5.12 テスト方法

純粋関数はテストしやすい。

```python
import pytest

from samples.python.disk_report import classify, summarize_exit_code


@pytest.mark.parametrize(
    ("usage", "expected"),
    [(79.9, "OK"), (80.0, "WARNING"), (90.0, "CRITICAL")],
)
def test_classify(usage: float, expected: str) -> None:
    assert classify(usage, warn=80.0, crit=90.0) == expected


def test_summarize_exit_code_critical() -> None:
    assert summarize_exit_code(["OK", "CRITICAL", "WARNING"]) == 3


def test_summarize_exit_code_ok() -> None:
    assert summarize_exit_code(["OK", "WARNING"]) == 0
```

副作用を持つ関数は、一時ディレクトリを使って結合的にテストする。

```python
from pathlib import Path

from samples.python.disk_report import load_usages, write_report


def test_load_and_write_roundtrip(tmp_path: Path) -> None:
    src = tmp_path / "in.csv"
    src.write_text("host,usage_percent\nweb01.example.invalid,95\n", encoding="utf-8")

    usages = load_usages(src)
    assert usages[0].host == "web01.example.invalid"

    out = tmp_path / "out.csv"
    write_report(out, [{"host": "web01.example.invalid", "usage_percent": "95", "status": "CRITICAL"}])
    assert out.exists()
```

Bashの関数は、`source` してから直接呼び出してテストできる。

```bash
source samples/bash/05_disk_report.sh

result="$(classify 95 80 90)"
[[ "${result}" == "CRITICAL" ]] || { echo "test failed: ${result}" >&2; exit 1; }
echo "ok"
```

PowerShellでは、関数定義部分だけをドットソース（`. path`）で読み込み、Pesterでテストする。

```powershell
BeforeAll {
    . (Join-Path $PSScriptRoot '../samples/powershell/05_disk_report.ps1') -TestMode
}

Describe 'Get-DiskStatus' {
    It 'returns CRITICAL at threshold' {
        Get-DiskStatus -Usage 90 -Warn 80 -Crit 90 | Should -Be 'CRITICAL'
    }
}
```

`-TestMode` は、スクリプト本体（`main`相当の実行部）を止め、関数定義だけを読み込むための独自スイッチである。
テストから読み込まれるスクリプトには、この種の「実行を止める入口」を用意しておくと、ドットソースでも安全に関数だけを取り出せる。

---

## 章末問題

1. 「純粋関数」と「副作用のある関数」を、それぞれ運用スクリプトの具体例で一つずつ挙げよ。
2. Bashの関数で `local` を付け忘れたときに起きる事故を、変数名の衝突を例に説明せよ。
3. PowerShellの関数内で `Write-Output` をデバッグ目的に残してしまうと何が起きるか説明せよ。
4. 「関数名に `and` が要る」状態を解消する分割案を、任意の処理を例に書け。
5. Pythonのモジュールを `from module import *` で読み込むことの問題点を二つ挙げよ。

## 解答と解説

1. 純粋関数の例: 使用率としきい値からステータス文字列を返す判定関数。副作用のある関数の例: レポートファイルへ追記する関数。
2. 呼び出し元や他の関数が同名の変数を使っていた場合、意図せず値が上書きされる。原因の特定に時間がかかる。
3. 関数の戻り値に、デバッグ用の出力とパイプラインの本来の戻り値が混ざって配列になる。呼び出し元のロジックが壊れる。
4. 例: `load_and_validate_and_report(path)` を `load(path)`、`validate(data)`、`report(data)` の三関数に分ける。
5. どの名前がどのモジュール由来か分からなくなる。同名の関数や変数が衝突しても気づきにくい。

---

## 実装演習

1. `05_disk_report.py` の `load_usages` と `write_report` を、モックを使わずに一時ディレクトリでテストするコードを書け。
2. Bashで `lib/hostlib.sh` を作り、`hostlib::load_hosts` を別スクリプトから `source` して呼び出せ。
3. PowerShellで `HostLib.psm1` を作り、`Export-ModuleMember` で公開する関数と、公開しない補助関数を最低一つずつ用意せよ。
4. 自分が最近書いたスクリプトから、10行を超える関数を一つ選び、責務ごとに二つ以上へ分割せよ。

---

## 次章予告

第6章では、ファイルの読み書きと安全な更新を扱う。
文字コードと改行を意識したテキスト処理、バックアップしてから変更する手順、ロックを使った競合回避を三言語で実装する。


---


<!-- SOURCE: 06_file_operations.md -->

# 第6章 ファイル操作

## 学習目標

この章を終えると、次ができるようになる。

- テキストとバイナリの違いを理解し、目的に応じたモードでファイルを開ける
- 読み込み、書き込み、追記、ディレクトリ操作、検索を三言語で実装できる
- 一時ファイルとロックを使い、競合を避けたファイル操作を書ける
- 大容量ファイルをメモリに全展開せず処理できる
- 文字コードと改行を意識し、バックアップと原子的な置き換えで安全に更新できる

前提: 第3章の文字コード、第5章の関数分割。

サンプルコードは学習用である。本番のパスやアクセス権限は対象システムで確認すること。

---

## 6.1 基本概念

**テキストファイル**は、文字として解釈できるバイト列を持つファイルである。
**バイナリファイル**は、文字としての解釈を前提としないバイト列を持つファイルである。
画像、証明書、圧縮ファイルはバイナリとして扱う。

テキストとして開くべきファイルをバイナリモードで扱うと、改行の変換が起きずOS間で表示が崩れる。
逆にバイナリファイルをテキストモードで開くと、文字コード変換によってバイト列が壊れる。

Python:

```python
# テキスト
with open("config.yaml", encoding="utf-8") as fh:
    text = fh.read()

# バイナリ
with open("server.crt", "rb") as fh:
    raw = fh.read()
```

Bashは基本的にすべてをバイト列やテキスト行として扱う。
バイナリを厳密に扱う操作（ハッシュ計算、切り出し）は `dd`、`od`、`sha256sum` などの外部コマンドに委ねることが多い。

PowerShell:

```powershell
# テキスト
$text = Get-Content -LiteralPath 'config.yaml' -Raw -Encoding utf8

# バイナリ
$bytes = [System.IO.File]::ReadAllBytes('server.crt')
```

---

## 6.2 読み書き追記

**追記**は、既存の内容を残したまま末尾へ書き加える操作である。

Python:

```python
from pathlib import Path

path = Path("work/events.log")
path.parent.mkdir(parents=True, exist_ok=True)

# 上書き
path.write_text("first\n", encoding="utf-8")

# 追記
with path.open("a", encoding="utf-8") as fh:
    fh.write("second\n")

# 読み込み
lines = path.read_text(encoding="utf-8").splitlines()
```

Bash:

```bash
mkdir -p work
echo "first" > work/events.log     # 上書き
echo "second" >> work/events.log   # 追記
mapfile -t lines < work/events.log
```

PowerShell:

```powershell
New-Item -ItemType Directory -Path 'work' -Force | Out-Null

'first' | Set-Content -LiteralPath 'work/events.log' -Encoding utf8   # 上書き
'second' | Add-Content -LiteralPath 'work/events.log' -Encoding utf8  # 追記

$lines = Get-Content -LiteralPath 'work/events.log'
```

複数プロセスが同じファイルへ同時に追記すると、行の途中で書き込みが混ざることがある。
単一プロセスからの追記に限定するか、6.7節のロックを使う。

---

## 6.3 ディレクトリ操作

Python:

```python
from pathlib import Path

work_dir = Path("work/2026-07-30")
work_dir.mkdir(parents=True, exist_ok=True)

for entry in work_dir.iterdir():
    print(entry.name, entry.is_dir())

work_dir.rmdir()  # 空でなければ失敗する
```

Bash:

```bash
mkdir -p work/2026-07-30
ls -la work/2026-07-30
rmdir work/2026-07-30   # 空でなければ失敗する
```

PowerShell:

```powershell
New-Item -ItemType Directory -Path 'work/2026-07-30' -Force | Out-Null
Get-ChildItem -LiteralPath 'work/2026-07-30'
Remove-Item -LiteralPath 'work/2026-07-30'   # 空でなければ失敗する
```

再帰的な削除（`rm -rf` 相当）は破壊的操作である。

> **警告**: `Path.rmdir()` は空ディレクトリしか消せないが、Pythonの `shutil.rmtree`、PowerShellの `Remove-Item -Recurse`、Bashの `rm -rf` は中身ごと削除する。利用者入力をそのままパスに使わない。対象パスが想定ディレクトリ配下にあることを検証してから呼び出す。

```python
import shutil
from pathlib import Path

base = Path("work").resolve()
target = Path("work/2026-07-30").resolve()

if base not in target.parents and target != base:
    raise ValueError(f"refusing to delete outside of work dir: {target}")

shutil.rmtree(target)
```

---

## 6.4 検索

Python:

```python
from pathlib import Path

root = Path("/var/log/myapp")
for path in root.rglob("*.log"):
    if path.stat().st_size > 0:
        print(path)
```

Bash:

```bash
find /var/log/myapp -type f -name '*.log' -size +0c
```

PowerShell:

```powershell
Get-ChildItem -LiteralPath '/var/log/myapp' -Filter '*.log' -Recurse -File |
    Where-Object { $_.Length -gt 0 }
```

`find` や `Get-ChildItem` の結果をそのまま `rm` や `Remove-Item` に流し込む前に、件数と一覧を確認する運用にする。
第15章の「古いファイルの整理」で、検索と削除を安全に組み合わせる設計を扱う。

---

## 6.5 権限

Python:

```python
import os
import stat
from pathlib import Path

path = Path("work/secret.tmp")
path.write_text("data", encoding="utf-8")
os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)  # 所有者のみ読み書き（0600相当）

mode = path.stat().st_mode
print(oct(stat.S_IMODE(mode)))
```

Bash:

```bash
touch work/secret.tmp
chmod 600 work/secret.tmp
stat -c '%a' work/secret.tmp 2>/dev/null || stat -f '%Lp' work/secret.tmp
```

PowerShell（Windowsのアクセス制御はUnixパーミッションと構造が異なる）:

```powershell
New-Item -ItemType File -Path 'work/secret.tmp' -Force | Out-Null

# Windows: ACLで所有者のみアクセス許可にする例
$acl = Get-Acl -LiteralPath 'work/secret.tmp'
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $env:USERNAME, 'FullControl', 'Allow')
$acl.SetAccessRule($rule)
Set-Acl -LiteralPath 'work/secret.tmp' -AclObject $acl
```

Linux/macOSとWindowsでは権限モデルが異なる。
Unix系はパーミッションビット（所有者/グループ/その他）、Windowsはアクセス制御リスト（ACL）が基本になる。
秘密情報を含むファイルは、作成直後に権限を絞ることを既定の手順にする。

---

## 6.6 一時ファイル

**一時ファイル**は、処理の途中経過を保持するための、短命なファイルである。

自前でファイル名を組み立てると、他プロセスと衝突したり、推測されやすい名前になったりする。
言語標準の一時ファイル機能を使う。

Python:

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, dir="work") as tmp:
    tmp.write("draft content\n")
    tmp_path = Path(tmp.name)

# 検証やコピーが終わってから削除する
tmp_path.unlink()
```

Bash:

```bash
tmp_file="$(mktemp work/tmp.XXXXXX)"
trap 'rm -f "${tmp_file}"' EXIT

echo "draft content" > "${tmp_file}"
# 処理...
```

PowerShell:

```powershell
$tmpFile = [System.IO.Path]::Combine('work', [System.IO.Path]::GetRandomFileName())
try {
    'draft content' | Set-Content -LiteralPath $tmpFile -Encoding utf8
    # 処理...
}
finally {
    Remove-Item -LiteralPath $tmpFile -ErrorAction SilentlyContinue
}
```

一時ファイルは、作成した関数やスクリプトが責任を持って削除する。
Bashの `trap ... EXIT`、Pythonの `try/finally`、PowerShellの `finally` を使い、途中で例外が起きても後始末する（第8章で詳しく扱う）。

---

## 6.7 ファイルロック

**ファイルロック**は、複数プロセスが同じファイルへ同時にアクセスするのを防ぐ仕組みである。

Bashでは `flock` が代表的である。

```bash
#!/usr/bin/env bash
set -euo pipefail

lock_file="work/report.lock"
mkdir -p work

exec 9> "${lock_file}"
if ! flock -n 9; then
  echo "another process holds the lock" >&2
  exit 2
fi

echo "critical section" >> work/report.csv
# ファイルディスクリプタ9が閉じると自動的に解放される
```

Pythonでは、標準ライブラリだけではOS間で統一的なロックAPIが無い。
Unix系では `fcntl.flock`、Windowsでは別のAPIが必要になる。
運用スクリプトでは、対象OSを絞るか、`filelock` のような外部ライブラリを使う判断をする。

```python
import fcntl
from pathlib import Path

lock_path = Path("work/report.lock")
lock_path.parent.mkdir(parents=True, exist_ok=True)

with lock_path.open("w") as lock_fh:
    fcntl.flock(lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    # クリティカルセクション
    with open("work/report.csv", "a", encoding="utf-8") as report_fh:
        report_fh.write("row\n")
    # withブロックを抜けるとファイルが閉じ、ロックも解放される
```

PowerShellでは、ファイルを排他モードで開くこと自体がロックとして働く。

```powershell
$reportPath = 'work/report.csv'
$stream = [System.IO.File]::Open(
    $reportPath,
    [System.IO.FileMode]::Append,
    [System.IO.FileAccess]::Write,
    [System.IO.FileShare]::None)
try {
    $writer = New-Object System.IO.StreamWriter($stream)
    $writer.WriteLine('row')
    $writer.Flush()
}
finally {
    $stream.Dispose()
}
```

ロックはタイムアウト無しで待ち続けると、障害時にプロセスが詰まる原因になる。
`flock -n`（即座に失敗）や、待ち時間の上限を決めておく。

---

## 6.8 大容量ファイル

数百MBを超えるログを `read()` で一括読み込みすると、メモリを圧迫し、処理開始まで時間がかかる。

Python（1行ずつストリーム処理）:

```python
from pathlib import Path

path = Path("/var/log/myapp/access.log")
error_count = 0
with path.open(encoding="utf-8", errors="replace") as fh:
    for line in fh:
        if "ERROR" in line:
            error_count += 1
print(error_count)
```

Bash:

```bash
grep -c 'ERROR' /var/log/myapp/access.log
```

PowerShell（`Get-Content` は既定で行単位のパイプラインになる。ただし内部実装によっては速度差が出るため、巨大ファイルでは `-ReadCount` や `.NET` のストリームAPIを検討する）:

```powershell
$errorCount = 0
Get-Content -LiteralPath '/var/log/myapp/access.log' -ReadCount 1000 | ForEach-Object {
    $errorCount += ($_ | Select-String -Pattern 'ERROR').Count
}
$errorCount
```

大容量ファイルを扱う設計では、次を先に決める。

1. 全件を保持する必要があるか、集計値だけでよいか
2. 1回のスキャンで済むか、複数回読む必要があるか
3. 途中経過を報告するか（長時間ジョブでの進捗ログ）

---

## 6.9 文字コードと改行

第3章で触れたとおり、文字コードは明示する。
ファイル操作ではさらに、**改行コード**（LF、CRLF）の扱いが重要になる。

| 環境 | 既定の改行 |
|------|------------|
| Linux / macOS | LF (`\n`) |
| Windows | CRLF (`\r\n`) |

Python:

```python
from pathlib import Path

# 読み込み時に自動でLFへ正規化される（universal newlines、既定で有効）
text = Path("config.yaml").read_text(encoding="utf-8")

# 書き込み時の改行を明示する
Path("config.yaml").write_text(text, encoding="utf-8", newline="\n")
```

Bashのテキスト処理は、CRLFが混ざっていると行末に `\r` が残り、比較や正規表現が失敗する原因になる。

```bash
# CRLFをLFへ変換する
sed -i 's/\r$//' config.yaml
```

PowerShell 7の `Set-Content` は既定でOSに応じた改行を使う。
クロスプラットフォームで固定したい場合は、書き込む文字列の改行を明示的に統一する。

```powershell
$normalized = (Get-Content -LiteralPath 'config.yaml' -Raw) -replace "`r`n", "`n"
[System.IO.File]::WriteAllText('config.yaml', $normalized, [System.Text.Encoding]::UTF8)
```

Gitの `core.autocrlf` 設定次第で、コミットとチェックアウトの間に改行が変換される場合がある。
チーム全員が同じ設定を使うよう、`.gitattributes` で改行を固定する運用が安全である。

---

## 6.10 安全な更新: バックアップしてから変更、原子的な置き換え

設定ファイルの更新は、次の二つの事故を避ける設計にする。

1. 書き込み途中でプロセスが落ち、ファイルが壊れたまま残る
2. 変更を戻したいのに、変更前の内容が残っていない

対策は二つある。

- **バックアップ**: 変更前に、日時付きの別名でコピーを残す
- **原子的な置き換え**: 直接上書きせず、一時ファイルに書いてから、OSのリネーム操作で本番ファイルへ差し替える

同一ファイルシステム内でのリネーム（Pythonの `os.replace`、Bashの `mv`、PowerShellの `Move-Item`）は、多くのOSで単一の操作として扱われる。
書き込み途中の中間状態が外部から見えない。

### 悪いコード

```python
from pathlib import Path

def update_config_bad(path: Path, new_content: str) -> None:
    # 直接上書き。書き込み中に失敗すると内容が欠損する。
    # バックアップも無い。
    path.write_text(new_content, encoding="utf-8")
```

問題点:

- 書き込み中にディスク満杯やプロセス強制終了が起きると、ファイルが壊れたまま残る
- 変更前の内容を取り戻す手段が無い
- 変更後の構文チェックをしていない

### 改善後

```python
from __future__ import annotations

import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def backup_path(path: Path, backup_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir / f"{path.name}.{timestamp}.bak"


def update_config(
    path: Path,
    new_content: str,
    backup_dir: Path,
    validate=None,
) -> Path:
    """バックアップを取り、一時ファイル経由で原子的に置き換える。

    validate が渡されれば、書き込み前に新内容を検証する。
    """
    if validate is not None:
        validate(new_content)

    backup = backup_path(path, backup_dir)
    if path.exists():
        shutil.copy2(path, backup)

    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new_content)
        os.replace(tmp_path, path)  # 同一ファイルシステム内で原子的
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    return backup
```

`tempfile.mkstemp` を更新対象と同じディレクトリに作ることが重要である。
別ドライブや別ファイルシステムに作ると、`os.replace` が単純なリネームにならず、コピーと削除に分解されて原子性が失われる場合がある。

Bashでも同じ手順を踏む。

```bash
#!/usr/bin/env bash
set -euo pipefail

update_config() {
  local path="$1" new_content_file="$2" backup_dir="$3"
  local timestamp
  timestamp="$(date -u +%Y%m%dT%H%M%SZ)"

  mkdir -p "${backup_dir}"
  if [[ -f "${path}" ]]; then
    cp -p "${path}" "${backup_dir}/$(basename "${path}").${timestamp}.bak"
  fi

  local tmp_file
  tmp_file="$(mktemp "$(dirname "${path}")/.$(basename "${path}").XXXXXX")"
  trap 'rm -f "${tmp_file}"' RETURN

  cp "${new_content_file}" "${tmp_file}"
  mv "${tmp_file}" "${path}"   # 同一ファイルシステム内でのmvは原子的
  trap - RETURN
}
```

PowerShellでも同様である。

```powershell
function Update-Config {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$NewContent,
        [Parameter(Mandatory = $true)][string]$BackupDir
    )

    $timestamp = [DateTimeOffset]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

    if (Test-Path -LiteralPath $Path) {
        $name = Split-Path -Leaf $Path
        Copy-Item -LiteralPath $Path -Destination (Join-Path $BackupDir "$name.$timestamp.bak")
    }

    $dir = Split-Path -Parent $Path
    $tmpPath = Join-Path $dir ("." + [System.IO.Path]::GetFileName($Path) + "." + [System.IO.Path]::GetRandomFileName())

    try {
        [System.IO.File]::WriteAllText($tmpPath, $NewContent, [System.Text.Encoding]::UTF8)
        Move-Item -LiteralPath $tmpPath -Destination $Path -Force
    }
    catch {
        Remove-Item -LiteralPath $tmpPath -ErrorAction SilentlyContinue
        throw
    }
}
```

完全な実行可能ファイルは `samples/python/06_safe_config_update.py`、`samples/bash/06_safe_config_update.sh`、`samples/powershell/06_safe_config_update.ps1` に置く。

---

## 6.11 セキュリティ上の注意点

- バックアップにも秘密情報が含まれる場合がある。バックアップ先の権限を本体と同等以上に絞る
- 一時ファイルを予測可能な名前や `/tmp` 直下の固定名で作らない。`mktemp` や `tempfile` を使う
- 一時ファイルにも、最終ファイルと同じ権限を設定してからリネームする。既定権限のまま作成すると、一瞬でも緩い権限で内容が露出する
- 検索結果をそのまま削除や上書きに使う前に、対象パスが想定ディレクトリの配下にあるか検証する（パストラバーサル対策の詳細は第10章）
- ロック取得の失敗を握りつぶさない。取得できなければ処理を止め、原因を記録する

> **警告**: この章のコード例は学習用である。本番の設定ファイルを直接対象に実行する前に、バックアップ先の空き容量、権限、対象システムでの動作確認を行うこと。

---

## 6.12 テスト方法

一時ディレクトリを使い、実ファイルシステムに対して検証する。

```python
from pathlib import Path

from samples.python.safe_config_update import update_config


def test_update_config_creates_backup(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    target.write_text("old\n", encoding="utf-8")
    backup_dir = tmp_path / "backups"

    backup = update_config(target, "new\n", backup_dir)

    assert target.read_text(encoding="utf-8") == "new\n"
    assert backup.read_text(encoding="utf-8") == "old\n"


def test_update_config_first_time_no_backup(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    backup_dir = tmp_path / "backups"

    update_config(target, "new\n", backup_dir)

    assert target.read_text(encoding="utf-8") == "new\n"
    assert list(backup_dir.glob("*.bak")) == []


def test_update_config_validation_failure_keeps_original(tmp_path: Path) -> None:
    target = tmp_path / "app.conf"
    target.write_text("old\n", encoding="utf-8")
    backup_dir = tmp_path / "backups"

    def validate(content: str) -> None:
        if "bad" in content:
            raise ValueError("invalid content")

    try:
        update_config(target, "bad\n", backup_dir, validate=validate)
    except ValueError:
        pass

    assert target.read_text(encoding="utf-8") == "old\n"
```

途中で例外を起こす検証（`validate`）を組み込み、更新前のファイルが変わらないことを確認する点が、この章のテストの要になる。

Bash:

```bash
tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

echo "old" > "${tmp_dir}/app.conf"
echo "new" > "${tmp_dir}/new_content.txt"

source samples/bash/06_safe_config_update.sh
update_config "${tmp_dir}/app.conf" "${tmp_dir}/new_content.txt" "${tmp_dir}/backups"

[[ "$(cat "${tmp_dir}/app.conf")" == "new" ]] || { echo "content mismatch" >&2; exit 1; }
ls "${tmp_dir}/backups"/*.bak >/dev/null 2>&1 || { echo "backup missing" >&2; exit 1; }
echo "ok"
```

---

## 章末問題

1. 一時ファイルを対象ファイルと別のファイルシステムに作ると、原子的な置き換えが崩れる理由を説明せよ。
2. `find` の結果をそのまま `rm -rf $(find ...)` に渡す設計の危険を、ファイル名に空白がある場合を例に説明せよ。
3. `flock -n` を使わず、無制限に待つ実装にした場合、障害発生時にどのような問題が起きるか述べよ。
4. WindowsとLinux/macOSで改行コードが異なることが、テキスト処理スクリプトに与える具体的な影響を一つ挙げよ。
5. バックアップ先ディレクトリの権限を本体より緩くしてはいけない理由を述べよ。

## 解答と解説

1. 別ファイルシステムへのリネームは、OSによってコピーと削除に分解されることがあり、その間にファイルが存在しない、または不完全な状態が生じうる。
2. 空白を含むファイル名が単語分割され、意図しないパスや複数の引数に分裂して削除される。`find -print0` と `xargs -0`、または `-exec` を使う。
3. ロック保持プロセスが異常終了しないままハングすると、待機側が永久に処理を進められず、監視やcronジョブが詰まる。
4. 行末に `\r` が残り、正規表現の `$` 一致や文字列完全一致が失敗する。
5. バックアップにも秘密情報や機微な設定が含まれる場合があり、権限が緩いと本体より先に漏えい経路になる。

---

## 実装演習

1. `06_safe_config_update.py` に、直近5世代を超えるバックアップを削除する機能を追加せよ。削除前に一覧をログへ出すこと。
2. Bash版の `update_config` に、書き込み後に任意の検証コマンド（例: `jq empty` でJSON構文チェック）を実行し、失敗時はバックアップから復元する処理を追加せよ。
3. PowerShell版で、`-WhatIf` 相当のドライラン機能（実際には書き込まず、バックアップ先と一時ファイル名だけを表示する）を追加せよ。

---

## 次章予告

第7章では、外部コマンドの安全な実行を扱う。
引数の渡し方、標準出力と標準エラーの分離、終了コード、タイムアウト、並列実行、シェルインジェクション対策を三言語で実装する。


---


<!-- SOURCE: 07_command_and_process.md -->

# 第7章 コマンド実行とプロセス制御

## 学習目標

この章を終えると、次ができるようになる。

- 外部コマンドの引数を安全に渡し、シェルインジェクションを避けられる
- 標準出力と標準エラーを分離して取得し、終了コードで成否を判定できる
- タイムアウトと並列実行数の制限を付けて外部コマンドを呼べる
- コマンドが存在しない場合を検出し、利用者向けに分かりやすく報告できる
- Python subprocess、Bashのパイプとリダイレクト、PowerShellパイプラインを使い分けられる

前提: 第1章の終了コード、第5章の関数分割、第6章のファイル操作。

サンプルコードは学習用である。本番で実行するコマンドと権限は、対象システムで事前に確認すること。

---

## 7.1 基本概念

**外部コマンド実行**は、スクリプトが自分自身とは別のプロセスを起動し、その結果を利用することである。

インフラ運用スクリプトは、OS標準コマンド（`ping`、`systemctl`、`ssh`）や、他社製CLIツールを呼び出すことが多い。
すべてを自前で再実装するのではなく、既にあるコマンドと組み合わせる発想が土台になる。

外部コマンドを呼ぶたびに、次を意識する。

1. 引数はどう安全に渡すか
2. 標準出力・標準エラーをどう受け取るか
3. 終了コードをどう判定するか
4. いつまで待つか（タイムアウト）
5. コマンドが無い場合にどう振る舞うか

---

## 7.2 安全な引数渡し

**シェル文字列連結**は、コマンドと引数を一つの文字列として組み立て、シェルに解釈させる方式である。
**リスト渡し**（配列渡し）は、コマンド名と各引数を別々の要素として渡し、シェルの解釈を経由しない方式である。

リスト渡しでは、引数の中に空白や特殊文字が含まれても、それが一つの値として扱われる。
シェル文字列連結では、値の中身次第でコマンドの構造そのものが変わってしまう。

### 悪いコード

```python
import subprocess

hostname = "web01.example.invalid; rm -rf /tmp/work"
subprocess.run(f"ping -c 1 {hostname}", shell=True)  # 危険
```

`hostname` に `;` 以降のコマンドが混ざっていると、`ping` の後に別コマンドとして実行されてしまう。
利用者入力や設定ファイルから取得した値を、そのままシェル文字列へ埋め込むと同じ危険がある。

### 改善後

```python
import subprocess

hostname = "web01.example.invalid; rm -rf /tmp/work"
result = subprocess.run(
    ["ping", "-c", "1", hostname],
    capture_output=True,
    text=True,
    check=False,
)
# hostname 全体が1つの引数として ping に渡る。シェルは介在しない。
```

`shell=True` を使わない限り、`;` や `$( )` はシェルのメタ文字として解釈されない。
`hostname` はそのまま `ping` コマンドの一つの引数として渡り、意図しないコマンド実行は起きない。

Bashでは、変数展開の際に必ず引用符で囲む。

```bash
hostname='web01.example.invalid; rm -rf /tmp/work'

# 悪い例: 引用符なし。単語分割とグロブ展開が起きる
ping -c 1 $hostname

# 改善: 必ず引用符で囲む
ping -c 1 "${hostname}"
```

引用符で囲んでも、`hostname` の値そのものが `ping` の引数として渡るだけであり、シェルコマンドとして再解釈はされない。
ただし、値を `eval` や `bash -c "..."` に渡す設計は、引用符の有無に関わらず危険である（7.8節）。

PowerShell:

```powershell
$hostName = 'web01.example.invalid; Remove-Item C:\work -Recurse'

# 外部コマンド呼び出しでは、引数は配列として渡す
& ping -n 1 $hostName

# Invoke-Expression には絶対に文字列連結を渡さない
# Invoke-Expression "ping -n 1 $hostName"  # 危険。書いてはいけない
```

`&`（呼び出し演算子）で外部コマンドを実行すると、以降の引数はそれぞれ独立した値として渡る。
`Invoke-Expression` は文字列をPowerShellのコードとして評価するため、`eval` と同種の危険を持つ。

---

## 7.3 stdout/stderrの取得

Python:

```python
import subprocess

result = subprocess.run(
    ["df", "-h", "/"],
    capture_output=True,
    text=True,
    check=False,
)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("returncode:", result.returncode)
```

`capture_output=True` は `stdout=subprocess.PIPE, stderr=subprocess.PIPE` の短縮形である。
`text=True` を付けると、結果がバイト列ではなく文字列として得られる。

Bash:

```bash
# stdoutとstderrを別々の変数に取る
stdout="$(df -h / 2>/tmp/df_stderr.$$)"
stderr="$(cat /tmp/df_stderr.$$)"
rm -f "/tmp/df_stderr.$$"
exit_code=$?

echo "stdout: ${stdout}"
echo "stderr: ${stderr}"
```

Bashでコマンド置換 `$( )` を使うと標準出力だけが取れる。
標準エラーも変数に取りたい場合は、一時ファイルへリダイレクトするか、`{stdout,stderr}` を両方使うプロセス置換を使う。

```bash
# プロセス置換を使う方法（Bash 4以降）
exec 3>&1
stdout="$(df -h / 2>&2 1>&3)"
exec 3>&-
```

複雑になりやすいので、両方を厳密に分離したい場合は一時ファイル方式のほうが読みやすいことが多い。

PowerShell:

```powershell
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = 'df'
$psi.ArgumentList.Add('-h')
$psi.ArgumentList.Add('/')
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.UseShellExecute = $false

$process = [System.Diagnostics.Process]::Start($psi)
$stdout = $process.StandardOutput.ReadToEnd()
$stderr = $process.StandardError.ReadToEnd()
$process.WaitForExit()

Write-Output "stdout: $stdout"
Write-Output "stderr: $stderr"
Write-Output "exit code: $($process.ExitCode)"
```

`& command 2>&1` のような単純な呼び出しでも動くが、標準出力と標準エラーが混ざってしまう。
両方を分離して扱いたい場合は `System.Diagnostics.Process` を直接使うほうが確実である。

---

## 7.4 終了コード

各言語で、直前に実行した外部コマンドの終了コードを取得する方法が異なる。

| 言語 | 取得方法 |
|------|----------|
| Python | `subprocess.run(...).returncode` |
| Bash | `$?`（直前のコマンド）、`${PIPESTATUS[@]}`（パイプの各段階） |
| PowerShell | `$LASTEXITCODE`（ネイティブコマンド）、`$?`（成功/失敗の真偽） |

Bashのパイプでは、最後のコマンドの終了コードだけが `$?` に入る。
途中のコマンドが失敗しても、最後が成功すれば `$?` は0になる。

```bash
false | true
echo "$?"          # 0 になる（最後の true の結果）
echo "${PIPESTATUS[@]}"   # 1 0 （各段階の結果）
```

パイプの途中の失敗を検知したい場合は `set -o pipefail` を有効にする（第1章から本書で使っている `set -euo pipefail` に含まれる）。

```bash
set -euo pipefail
false | true
# pipefail により、パイプ全体が失敗として扱われスクリプトが止まる
```

PowerShellのネイティブコマンド呼び出しは、成功しても `$LASTEXITCODE` が更新されないことがある点に注意する。
呼び出し直後に必ず確認する。

```powershell
& ping -n 1 'web01.example.invalid' | Out-Null
if ($LASTEXITCODE -ne 0) {
    [Console]::Error.WriteLine("ping failed with exit code $LASTEXITCODE")
}
```

---

## 7.5 タイムアウト

タイムアウトの無い外部コマンド呼び出しは、応答しないホストやハングしたプロセスに引きずられ、スクリプト全体を止める。

Python:

```python
import subprocess

try:
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "web01.example.invalid", "uptime"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
except subprocess.TimeoutExpired:
    print("command timed out")
```

`timeout` を超えるとプロセスは強制終了され、`TimeoutExpired` 例外が発生する。

Bash:

```bash
if ! timeout 10 ssh -o BatchMode=yes web01.example.invalid uptime; then
  echo "command failed or timed out" >&2
fi
```

`timeout` コマンドの終了コード124は、タイムアウトによる強制終了を意味する。

```bash
timeout 10 sleep 30
echo "$?"   # 124
```

macOS標準の `/usr/bin` には `timeout` が入っていない。
Homebrewの `coreutils`（`brew install coreutils`）を入れると `gtimeout` として使えるが、常に入っているとは限らない。
`timeout` が無い環境向けに、バックグラウンド実行と `kill` で代替する移植性の高い実装を用意しておくと安全である。

```bash
# timeout コマンドが無い環境向けの代替実装
# 戻り値は GNU timeout に合わせ、打ち切り時は124を返す
portable_timeout() {
  local secs="$1"
  shift
  "$@" &
  local cmd_pid=$!

  (
    sleep "${secs}"
    kill -0 "${cmd_pid}" 2>/dev/null && kill -TERM "${cmd_pid}" 2>/dev/null
  ) &
  local watcher_pid=$!

  local rc
  wait "${cmd_pid}"
  rc=$?

  # watcherがまだ生きていればコマンドはタイムアウト前に終わっている
  if kill -0 "${watcher_pid}" 2>/dev/null; then
    kill "${watcher_pid}" 2>/dev/null
    wait "${watcher_pid}" 2>/dev/null || true
    return "${rc}"
  fi
  return 124
}
```

PowerShell（`.NET` のプロセスAPIでタイムアウトを実装する）:

```powershell
$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = 'ssh'
foreach ($a in @('-o', 'BatchMode=yes', 'web01.example.invalid', 'uptime')) {
    $psi.ArgumentList.Add($a)
}
$psi.UseShellExecute = $false

$process = [System.Diagnostics.Process]::Start($psi)
if (-not $process.WaitForExit(10000)) {
    $process.Kill()
    [Console]::Error.WriteLine('command timed out')
}
```

`Start-Process -Wait` にはタイムアウト引数が無いため、`WaitForExit(milliseconds)` を使う方法が確実である。

---

## 7.6 並列実行

多数のホストへ直列で処理を行うと、1台あたり数秒の遅延でも合計時間が大きくなる。
同時実行数を制限した並列化で短縮できる。

Python（`concurrent.futures`）:

```python
from __future__ import annotations

import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping_host(host: str, timeout: int) -> tuple[str, bool]:
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), host],
        capture_output=True,
        timeout=timeout + 2,
        check=False,
    )
    return host, result.returncode == 0


def ping_all(hosts: list[str], timeout: int, max_workers: int = 8) -> dict[str, bool]:
    results: dict[str, bool] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(ping_host, host, timeout): host for host in hosts}
        for future in as_completed(futures):
            host, ok = future.result()
            results[host] = ok
    return results
```

`max_workers` で同時実行数を絞る。
無制限に並列化すると、対象ホスト側やネットワーク帯域を圧迫する場合がある。

Bash（`xargs -P` で並列化する）:

```bash
cat config/hosts.txt | grep -v '^#' | grep -v '^\s*$' | \
  xargs -P 8 -I{} timeout 3 ping -c 1 {} >/tmp/ping_out.$$ 2>&1
```

`xargs -P N` は、1行につき1コマンドを起動し、同時実行数をNに制限する。
結果の集計や終了コードの合成は別途必要になる（`xargs` 自体は各コマンドの終了コードを合成しない）。

PowerShell 7（`ForEach-Object -Parallel`）:

```powershell
$hosts = Get-Content -LiteralPath 'config/hosts.txt' | Where-Object { $_ -and -not $_.StartsWith('#') }

$results = $hosts | ForEach-Object -Parallel {
    $h = $_
    $ok = Test-Connection -ComputerName $h -Count 1 -Quiet -TimeoutSeconds 3
    [pscustomobject]@{ Host = $h; Ok = $ok }
} -ThrottleLimit 8

$results
```

`-ThrottleLimit` が同時実行数の上限である。
`ForEach-Object -Parallel` はPowerShell 7以降の機能であり、Windows PowerShell 5.1には無い。

---

## 7.7 子プロセスと後始末

タイムアウトで親プロセスが待つのをやめても、子プロセス（および孫プロセス）が生き残ることがある。
特にシェル経由で起動した場合、シェルプロセスだけが終了し、その配下のコマンドが残るケースがある。

Python:

```python
import subprocess

process = subprocess.Popen(
    ["long_running_tool", "--arg", "value"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
try:
    stdout, stderr = process.communicate(timeout=30)
except subprocess.TimeoutExpired:
    process.kill()
    stdout, stderr = process.communicate()
    raise
```

`process.kill()` は直接の子プロセスを止める。
子プロセスがさらに孫プロセスを起動している構成では、プロセスグループごと止める必要がある場合がある（`os.killpg` など、OS依存の対応が要る）。

Bashでは、`trap` でスクリプト終了時に子プロセスを確実に片付ける。

```bash
#!/usr/bin/env bash
set -euo pipefail

long_running_tool --arg value &
child_pid=$!

cleanup() {
  kill "${child_pid}" 2>/dev/null || true
}
trap cleanup EXIT

wait "${child_pid}"
```

PowerShellでは、`finally` で確実に `Stop-Process` する。

```powershell
$process = Start-Process -FilePath 'long_running_tool' -ArgumentList '--arg', 'value' -PassThru
try {
    if (-not $process.WaitForExit(30000)) {
        throw 'timed out'
    }
}
finally {
    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
    }
}
```

---

## 7.8 シェルインジェクション対策

**シェルインジェクション**は、利用者が制御できる入力がシェルコマンドの一部として解釈され、意図しない処理を実行させられる脆弱性である。

対策の優先順位:

1. 可能な限りシェルを経由しない（Pythonの `shell=False`、PowerShellの `&` 呼び出し演算子）
2. どうしてもシェル文字列を組み立てる必要がある場合、言語のクォート関数を使う（`shlex.quote` など）
3. 利用者入力は、コマンドではなく引数の値としてのみ渡す
4. 許可された値の集合（ホスト名の形式、既知のサブコマンド名）で検証してから使う

```python
import shlex

hostname = "web01.example.invalid"
quoted = shlex.quote(hostname)
# それでも shell=True 自体を避けるのが最善である
```

`shlex.quote` はBash向けのクォートである。
PowerShellやWindowsのコマンド解釈規則は異なるため、そのまま流用できない。
最も安全なのは、どの言語でも「シェル文字列を組み立てない」ことである。

---

## 7.9 コマンド不存在の検出

対象環境にコマンドが無い場合、分かりにくいエラーで落ちるより、明示的に検出して報告するほうが運用しやすい。

Python:

```python
import shutil
import subprocess

def run_if_available(cmd: str, args: list[str]) -> subprocess.CompletedProcess[str] | None:
    if shutil.which(cmd) is None:
        return None
    return subprocess.run([cmd, *args], capture_output=True, text=True, check=False)
```

`shutil.which` はPATH上にコマンドがあるかを確認する。
呼び出す前に確認すれば、`FileNotFoundError` を捕まえる代わりに、事前分岐で処理できる。

Bash:

```bash
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required but not installed" >&2
  exit 1
fi
```

`command -v` はBash組み込みであり、`which` の外部コマンドに依存しない分、環境差が少ない。

PowerShell:

```powershell
if (-not (Get-Command -Name 'jq' -ErrorAction SilentlyContinue)) {
    [Console]::Error.WriteLine('jq is required but not installed')
    exit 1
}
```

---

## 7.10 実務向けサンプル: 汎用コマンドランナー

要件:

- 任意の外部コマンドを、引数リストとタイムアウト付きで実行する
- 標準出力と標準エラーを分離して返す
- コマンドが存在しない、タイムアウトした、非0で終了した、をそれぞれ区別できる終了コードにする

### 悪いコード

```python
import subprocess

def run_bad(cmd_string: str) -> str:
    # shell=True + 文字列連結。タイムアウトも無い。
    return subprocess.check_output(cmd_string, shell=True, text=True)
```

問題点:

- `cmd_string` に利用者由来の値が混ざるとシェルインジェクションになる
- タイムアウトが無く、応答しないコマンドで無限に待つ
- 標準エラーと終了コードの扱いが呼び出し側に委ねられていない
- コマンド不存在時の挙動が `CalledProcessError` 任せで分かりにくい

### 改善後

完全な実行可能ファイルは `samples/python/07_run_command.py`、`samples/bash/07_run_command.sh`、`samples/powershell/07_run_command.ps1` に置く。
骨子は次のとおりである。

```python
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass

EXIT_OK = 0
EXIT_COMMAND_NOT_FOUND = 1
EXIT_NONZERO = 2
EXIT_TIMEOUT = 4


@dataclass
class CommandResult:
    stdout: str
    stderr: str
    returncode: int
    exit_code: int


def run_command(args: list[str], timeout: int) -> CommandResult:
    if not args:
        raise ValueError("args must not be empty")
    if shutil.which(args[0]) is None:
        return CommandResult(stdout="", stderr=f"command not found: {args[0]}", returncode=-1, exit_code=EXIT_COMMAND_NOT_FOUND)

    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CommandResult(stdout="", stderr=f"timed out after {timeout}s", returncode=-1, exit_code=EXIT_TIMEOUT)

    exit_code = EXIT_OK if completed.returncode == 0 else EXIT_NONZERO
    return CommandResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
        exit_code=exit_code,
    )
```

`run_command` は引数をリストで受け取り、`shell=True` を一切使わない。
呼び出し元は `exit_code` を見るだけで、コマンド不存在・非0終了・タイムアウトを区別できる。

---

## 7.11 セキュリティ上の注意点

- `shell=True`、`Invoke-Expression`、Bashの `eval` に利用者入力を渡さない
- 引数に秘密情報を渡すと、`ps` や `Get-Process` のコマンドライン表示で見える場合がある。環境変数や標準入力経由の方が安全なことが多い
- 外部コマンドの標準出力をそのまま別のコマンドへ渡す前に、想定した形式かを検証する
- タイムアウトを必ず設定する。特に外部ネットワーク越しのコマンドは、対象側の障害が自スクリプトの障害に伝播しやすい
- 並列実行数を無制限にしない。対象システムへの意図しない高負荷を避ける

> **警告**: 本章のコマンド不存在検出やタイムアウトの例は学習用の簡略構成である。本番の並列実行数やタイムアウト値は、対象システムの許容量に応じて個別に検討すること。

---

## 7.12 テスト方法

外部コマンドをテストするときは、実コマンドに依存しない部分と依存する部分を分ける。

```python
from samples.python.run_command import run_command


def test_command_not_found() -> None:
    result = run_command(["definitely-not-a-real-command-xyz"], timeout=5)
    assert result.exit_code == 1


def test_nonzero_exit() -> None:
    result = run_command(["false"], timeout=5)
    assert result.exit_code == 2


def test_success() -> None:
    result = run_command(["echo", "hello"], timeout=5)
    assert result.exit_code == 0
    assert "hello" in result.stdout


def test_timeout() -> None:
    result = run_command(["sleep", "5"], timeout=1)
    assert result.exit_code == 4
```

`echo`、`false`、`sleep` はほぼ全環境に存在するため、実コマンドへの依存を許容してテストを書く。
移植性が必要な場合は、`sys.executable` でPython自身を子プロセスとして起動し、テスト専用の疑似コマンドとして使う方法もある。

Bash:

```bash
source samples/bash/07_run_command.sh
# サンプルは set -euo pipefail を含むため、source した側にも
# errexit が伝播する。個々の呼び出しの終了コードを判定したいテスト
# コードでは、いったん set +e で無効化する。
set +e

run_command 5 definitely-not-a-real-command-xyz
[[ "$?" -eq 1 ]] || { echo "fail: not found" >&2; exit 1; }

run_command 5 false
[[ "$?" -eq 2 ]] || { echo "fail: nonzero" >&2; exit 1; }

run_command 5 echo hello
[[ "$?" -eq 0 ]] || { echo "fail: success" >&2; exit 1; }

echo ok
```

---

## 章末問題

1. `subprocess.run(f"ping {host}", shell=True)` と `subprocess.run(["ping", host])` の違いを、シェルインジェクションの観点で説明せよ。
2. `set -o pipefail` を付けない場合、パイプの途中で失敗したコマンドがどのように無視されるか例を挙げよ。
3. `ForEach-Object -Parallel` の `-ThrottleLimit` を大きくしすぎたときに起きうる問題を述べよ。
4. `shutil.which` や `command -v` で事前にコマンドの有無を確認する利点を、例外処理だけに頼る場合と比較して述べよ。
5. `process.kill()` を呼んでも子プロセスの孫プロセスが残ることがある理由を説明せよ。

## 解答と解説

1. `shell=True` はシェルに文字列を渡して解釈させるため、`host` にメタ文字が含まれると別コマンドとして実行されうる。リスト渡しはシェルを経由せず、値がそのまま1引数になる。
2. 途中のコマンドが失敗しても、パイプ全体の終了コードは最後のコマンドの結果になり、失敗が握りつぶされる。
3. 対象ホストやAPIへの同時接続数が増えすぎ、相手側のリソースを圧迫したり、レート制限に引っかかったりする。
4. 事前確認は、失敗の原因が「コマンド不存在」であることを明示的に分岐でき、例外の種類を都度判定する必要が無い。エラーメッセージも利用者向けに整えやすい。
5. `kill()` は直接の子プロセスにしかシグナルを送らない。孫プロセスは別のプロセスグループやセッションに属している場合があり、明示的にプロセスツリーごと止める処理が必要になる。

---

## 実装演習

1. `07_run_command.py` に、標準出力を1万行を超えたら打ち切るオプションを追加せよ。理由と挙動をログに残すこと。
2. Bash版の `run_command` を使い、`config/hosts.txt` の各ホストへ `ping` をタイムアウト付きで並列実行し、結果をCSVへ集計するスクリプトを書け。
3. PowerShell版で、`Start-Process` ベースの実装と `System.Diagnostics.Process` ベースの実装を両方書き、標準出力・標準エラーの扱いの違いを確認せよ。

---

## 次章予告

第8章では、エラー処理を体系的に扱う。
例外と終了コードの使い分け、リトライと指数バックオフ、部分成功とロールバック、利用者向けメッセージと調査用ログの分離を三言語で実装する。


---


<!-- SOURCE: 08_error_handling.md -->

# 第8章 エラー処理

## 学習目標

この章を終えると、次ができるようになる。

- エラーの種類を分類し、例外と終了コードを適切に使い分けられる
- Pythonのtry/except/finally、Bashのtrap、PowerShellのtry/catch/finallyを実装できる
- 指数バックオフ付きリトライと、リトライしてはいけない場合を区別できる
- 部分成功とロールバックの方針を、実装前に決められる
- 利用者向けメッセージと、調査用の詳細ログを分けて出力できる

前提: 第1章の終了コード、第7章の外部コマンド実行。

サンプルコードは学習用である。本番のリトライ回数や待機時間は、対象システムの許容量に応じて調整すること。

---

## 8.1 基本概念

**エラー**は、処理が期待どおりに完了しなかった状態である。

エラーは、性質によって扱いを変える。

| 種類 | 例 | 対応の方向性 |
|------|-----|--------------|
| 利用者エラー | 引数不正、設定ファイルの構文誤り | 実行前に検証し、即座に分かりやすく報告する |
| 一時的なエラー | ネットワーク断、APIのレート制限 | リトライで回復する可能性がある |
| 恒久的なエラー | 認証失敗、権限不足 | リトライしても直らない。即座に報告する |
| 想定外のエラー | バグ、未処理の例外 | 調査用の詳細を残し、安全側に倒して停止する |

**例外**は、プログラムの通常の流れを中断し、呼び出し元へエラー情報を伝える仕組みである。
Python、PowerShellには例外機構がある。
Bashには例外が無く、終了コードと `trap` で代用する。

エラー処理の設計は、正常系の実装より先に決める。
第2章で述べたとおり、失敗時の挙動を後回しにすると、実装が進むほど直しにくくなる。

---

## 8.2 Pythonのtry/except/finally

```python
from __future__ import annotations

import logging

logger = logging.getLogger("example")


def read_threshold(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError(f"invalid threshold: {text!r}") from exc
    if not (0 <= value <= 100):
        raise ValueError(f"threshold out of range: {value}")
    return value


def load_and_report(text: str) -> int:
    try:
        threshold = read_threshold(text)
    except ValueError as exc:
        logger.error("%s", exc)
        return 1
    finally:
        logger.debug("load_and_report finished for input=%r", text)

    print(threshold)
    return 0
```

`except ValueError as exc` は、`ValueError` という具体的な型だけを捕まえる。
`except Exception` のような広い捕捉は、意図しないバグまで飲み込んでしまう。

`raise ... from exc` は、元の例外を保持したまま新しい例外に読み替える。
トレースバックに両方の情報が残るため、調査がしやすい。

`finally` ブロックは、例外が発生してもしなくても必ず実行される。
リソースの解放やログ出力に使う。

複数の例外型をまとめて捕まえることもできる。

```python
try:
    risky_operation()
except (OSError, ValueError) as exc:
    logger.error("%s", exc)
```

---

## 8.3 Bashのtrap

Bashには例外機構が無いため、**終了コード**と `trap` を組み合わせてエラー処理を行う。

```bash
#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  local exit_code=$?
  echo "cleanup: exit_code=${exit_code}" >&2
  rm -f /tmp/work.$$
}
trap cleanup EXIT

on_error() {
  local line_no=$1
  echo "error occurred at line ${line_no}" >&2
}
trap 'on_error ${LINENO}' ERR

echo "start" > /tmp/work.$$
false   # ここで ERR トラップが発火し、その後 set -e により終了する
echo "unreachable"
```

`trap ... EXIT` は、スクリプトがどのような理由で終了しても実行される。
正常終了、`exit` によるエラー終了、シグナルによる中断のいずれでも呼ばれるため、後始末処理を書く場所として適している。

`trap ... ERR` は、`set -e` が有効な状態でコマンドが失敗したときに呼ばれる。
`if` の条件式や `&&`/`||` の一部として実行されたコマンドの失敗では呼ばれない点に注意する。

```bash
trap 'echo "ERR at line ${LINENO}" >&2' ERR
set -e

false  # ERRトラップが発火する
if false; then :; fi  # 条件式なのでERRトラップは発火しない
```

シグナルごとのトラップも設定できる。

```bash
trap 'echo "interrupted" >&2; exit 130' INT
trap 'echo "terminated" >&2; exit 143' TERM
```

`INT`（Ctrl+C相当）を受けたら終了コード130、`TERM` を受けたら143を返す慣例は、第1章の終了コード表とも整合する。

---

## 8.4 PowerShellのtry/catch/finally

```powershell
$ErrorActionPreference = 'Stop'

function Read-Threshold {
    param([string]$Text)
    try {
        $value = [double]$Text
    }
    catch {
        throw "invalid threshold: $Text"
    }
    if ($value -lt 0 -or $value -gt 100) {
        throw "threshold out of range: $value"
    }
    return $value
}

function Invoke-LoadAndReport {
    param([string]$Text)
    try {
        $threshold = Read-Threshold -Text $Text
    }
    catch {
        [Console]::Error.WriteLine($_.Exception.Message)
        return 1
    }
    finally {
        Write-Verbose "Invoke-LoadAndReport finished for input=$Text"
    }

    Write-Output $threshold
    return 0
}
```

PowerShellの `try/catch` は、`$ErrorActionPreference = 'Stop'` を設定していないと、非終了エラー（non-terminating error）を捕まえられない場合がある。
本書のPowerShellサンプルは、スクリプトの先頭で必ず `$ErrorActionPreference = 'Stop'` を設定する方針にしている。

特定の例外型だけを捕まえたい場合は、`catch` に型を指定する。

```powershell
try {
    Invoke-RestMethod -Uri 'https://api.example.invalid/status' -TimeoutSec 5
}
catch [System.Net.WebException] {
    [Console]::Error.WriteLine("network error: $($_.Exception.Message)")
}
catch {
    [Console]::Error.WriteLine("unexpected error: $($_.Exception.Message)")
    throw
}
```

最後の `catch` で想定外の例外を再度 `throw` している点に注意する。
すべてのエラーを握りつぶさず、想定していないものは上位へ伝える。

---

## 8.5 終了コードとの対応関係

例外や `trap` で捕まえたエラーは、最終的にプロセスの終了コードへ変換する。

本書の `opsctl` 規約（README参照）を、三言語で一貫させる。

Python:

```python
import sys

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3
EXIT_TIMEOUT = 4


def main() -> int:
    try:
        ...
    except ValueError:
        return EXIT_USAGE
    except TimeoutError:
        return EXIT_TIMEOUT
    except Exception:
        logging.exception("unexpected error")
        return EXIT_RUNTIME
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

`except Exception` を使うのは、この「最上位で捕まえてログを残し、終了コードへ変換する」一箇所に限定する。
途中の関数で `except Exception` を多用すると、原因の特定が難しくなる。

Bash、PowerShellでも、関数内部の判定と、最終的な `exit` / `return` コードの変換は別の場所に置く。

---

## 8.6 リトライと指数バックオフ

**リトライ**は、一時的な失敗に対して、同じ処理をもう一度試みることである。
**指数バックオフ**は、リトライのたびに待機時間を指数的に伸ばす方式である。

すべての失敗をリトライしてよいわけではない。

| 失敗の種類 | リトライすべきか |
|------------|------------------|
| ネットワークタイムアウト | する |
| 5xx系のサーバーエラー | する（回数上限付き） |
| 429（レート制限） | する（`Retry-After` があれば従う） |
| 4xx系（認証失敗、権限不足、不正リクエスト） | しない |
| 入力値そのものが不正 | しない |

恒久的なエラーをリトライし続けると、無駄な待機時間が積み重なり、対象システムへの負荷にもなる。

Python:

```python
from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger("retry")


class RetryableError(Exception):
    """リトライしてよい失敗を表す。"""


class PermanentError(Exception):
    """リトライしても直らない失敗を表す。"""


def retry_with_backoff(
    func: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
) -> T:
    attempt = 0
    while True:
        attempt += 1
        try:
            return func()
        except PermanentError:
            raise
        except RetryableError as exc:
            if attempt >= max_attempts:
                raise
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jitter = random.uniform(0, delay * 0.1)
            sleep_for = delay + jitter
            logger.warning(
                "attempt %s/%s failed: %s; retrying in %.2fs",
                attempt,
                max_attempts,
                exc,
                sleep_for,
            )
            time.sleep(sleep_for)
```

`PermanentError` はそのまま再送出し、リトライループに入らない。
`RetryableError` だけが待機とリトライの対象になる。

**ジッター**（ランダムな揺らぎ）を待機時間に加えることで、複数のクライアントが同時に同じタイミングで再試行し、対象システムへ負荷が集中する事態（サンダリングハード）を緩和する。

Bash:

```bash
retry_with_backoff() {
  local max_attempts="$1"
  local base_delay="$2"
  shift 2

  local attempt=1
  local rc
  while true; do
    # rcの捕捉はelse節に置く。elseが無い「if false; then ...; fi」は
    # それ自体の終了コードが0になり、"$@"の本当の終了コードが消えてしまう。
    if "$@"; then
      return 0
    else
      rc=$?
    fi
    if [[ "${attempt}" -ge "${max_attempts}" ]]; then
      echo "giving up after ${attempt} attempts" >&2
      return "${rc}"
    fi
    local delay=$(( base_delay * (2 ** (attempt - 1)) ))
    echo "attempt ${attempt}/${max_attempts} failed; retrying in ${delay}s" >&2
    sleep "${delay}"
    attempt=$(( attempt + 1 ))
  done
}
```

Bashでは、恒久的なエラーと一時的なエラーの区別を、終了コードの値で判定する設計が現実的である（例: 特定の終了コードだけをリトライ対象にする）。

PowerShell:

```powershell
function Invoke-WithRetry {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Action,
        [int]$MaxAttempts = 5,
        [double]$BaseDelaySeconds = 0.5
    )

    $attempt = 0
    while ($true) {
        $attempt++
        try {
            return & $Action
        }
        catch [PermanentErrorException] {
            throw
        }
        catch {
            if ($attempt -ge $MaxAttempts) {
                throw
            }
            $delay = $BaseDelaySeconds * [Math]::Pow(2, $attempt - 1)
            [Console]::Error.WriteLine("attempt $attempt/$MaxAttempts failed: $($_.Exception.Message); retrying in ${delay}s")
            Start-Sleep -Seconds $delay
        }
    }
}
```

`PermanentErrorException` は、恒久的なエラー用に定義したカスタム例外クラスを想定している。
PowerShellでカスタム例外を作る場合は、`.NET` の `Exception` を継承したクラスをC#やPowerShellクラス構文で定義する。

---

## 8.7 握りつぶし禁止

**握りつぶし**は、エラーを検知したにもかかわらず、記録も再送出もせずに処理を継続することである。

### 悪いコード

```python
def check_all_bad(hosts: list[str]) -> int:
    for host in hosts:
        try:
            check_host(host)
        except Exception:
            pass  # 握りつぶし
    return 0  # 常に成功扱い
```

問題点:

- どのホストが失敗したか記録されない
- 呼び出し側は常に成功したと誤認する
- 想定外のバグ（`TypeError` など）まで同じ `except Exception: pass` で消えてしまう

### 改善後

```python
from dataclasses import dataclass


@dataclass
class CheckFailure:
    host: str
    error: str


def check_all(hosts: list[str]) -> tuple[list[CheckFailure], int]:
    failures: list[CheckFailure] = []
    for host in hosts:
        try:
            check_host(host)
        except (TimeoutError, ConnectionError) as exc:
            failures.append(CheckFailure(host=host, error=str(exc)))

    if failures:
        for failure in failures:
            logger.error("check failed: host=%s error=%s", failure.host, failure.error)
        return failures, 2
    return failures, 0
```

捕まえる例外の型を明示し、失敗を一覧として記録し、終了コードへ反映する。
`Exception` という広い型で握りつぶす代わりに、想定される例外だけを扱い、それ以外は伝播させる。

---

## 8.8 部分成功

**部分成功**は、複数の対象のうち一部だけが成功し、残りが失敗した状態である。

部分成功を「全体成功」として報告すると、失敗した対象が放置される。
第2章、第7章で扱った複数ホスト処理と同様、次を実装前に決める。

1. 1件でも失敗したら、全体をどの終了コードにするか
2. 失敗した対象の一覧を、どこに残すか（レポート、stderr、両方）
3. 一部成功した分の結果を、そのまま使ってよいか、取り消すべきか

```python
from dataclasses import dataclass


@dataclass
class ApplyResult:
    host: str
    ok: bool
    error: str | None = None


def apply_to_all(hosts: list[str], apply) -> tuple[list[ApplyResult], int]:
    results: list[ApplyResult] = []
    for host in hosts:
        try:
            apply(host)
            results.append(ApplyResult(host=host, ok=True))
        except Exception as exc:  # 個々の対象の失敗はここで吸収し、記録する
            results.append(ApplyResult(host=host, ok=False, error=str(exc)))

    failed = [r for r in results if not r.ok]
    exit_code = 2 if failed else 0
    return results, exit_code
```

ここでの `except Exception` は、ループの外側まで伝播させず、対象ごとの結果として記録する意図的な設計である。
8.7節の「握りつぶし」と違い、失敗を `results` に残し、`exit_code` にも反映している点が異なる。

---

## 8.9 ロールバック

**ロールバック**は、失敗した変更を、変更前の状態へ戻す操作である。

すべての操作をロールバック可能にするのは難しい。
設計時に、対象操作を次のように分類する。

| 分類 | 例 | ロールバック方針 |
|------|-----|-------------------|
| 冪等な操作 | 設定ファイルの上書き（バックアップあり） | 第6章のバックアップから復元 |
| 追記のみの操作 | ログ追記、レポート出力 | 通常はロールバック不要 |
| 外部への副作用 | API経由のリソース作成、メール送信 | 打ち消し操作（削除API、取消通知）を用意するか、事前承認制にする |
| 取り消し不能な操作 | 物理的な破棄、通知済みの重要アラート | 実行前の確認を必須にし、失敗時は人手対応に切り替える |

第6章の `update_config` を使った、設定変更のロールバック例:

```python
from pathlib import Path

from samples.python.safe_config_update import update_config


def apply_config_with_rollback(
    target: Path,
    new_content: str,
    backup_dir: Path,
    post_check,
) -> None:
    backup = update_config(target, new_content, backup_dir)
    try:
        post_check(target)
    except Exception:
        if backup is not None:
            target.write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
            logger.error("post_check failed; rolled back to %s", backup)
        raise
```

`post_check` は、変更後の設定を検証する関数を想定している（例: 設定の構文チェック、対象サービスへの反映確認）。
検証に失敗したら、バックアップの内容を書き戻し、例外を再送出して呼び出し元に失敗を伝える。

---

## 8.10 利用者向けエラーと調査用エラー

**利用者向けメッセージ**は、実行した人がすぐに理解し、次の行動を取れる短い説明である。
**調査用ログ**は、原因調査に必要な詳細情報（スタックトレース、内部状態、リクエストID）である。

両者を同じ場所に出すと、利用者向けの画面がノイズだらけになるか、調査に必要な情報が欠落するかのどちらかになりやすい。

```python
import logging
import sys
import uuid

logger = logging.getLogger("opsctl")


def main() -> int:
    run_id = str(uuid.uuid4())
    try:
        do_work()
    except ValueError as exc:
        # 利用者向け: 短く、対応方法が分かる
        print(f"設定が不正です。--config の内容を確認してください (run_id={run_id})", file=sys.stderr)
        # 調査用: 詳細と原因
        logger.error("validation failed run_id=%s detail=%s", run_id, exc, exc_info=True)
        return 1
    return 0
```

`run_id` を両方に含めておくと、利用者からの問い合わせと調査用ログを突き合わせられる。
第9章のログ設計で、この `run_id` を構造化ログの必須フィールドとして扱う。

---

## 8.11 実務向けサンプル: リトライ付きヘルスチェック

要件:

- 対象ホストへヘルスチェック相当のコマンドを実行する
- 一時的な失敗は指数バックオフでリトライする
- 恒久的な失敗（コマンド不存在、設定不正）は即座に打ち切る
- 利用者向けメッセージと調査用ログを分離する
- 部分成功を許容し、失敗ホストの一覧を残す

完全な実行可能ファイルは `samples/python/08_retry_backoff.py`、`samples/bash/08_retry_backoff.sh`、`samples/powershell/08_retry_backoff.ps1` に置く。
Python版の骨子:

```python
from __future__ import annotations

import logging
import random
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

logger = logging.getLogger("retry_backoff")


class PermanentError(Exception):
    pass


class RetryableError(Exception):
    pass


@dataclass
class HealthResult:
    host: str
    ok: bool
    attempts: int
    detail: str


def check_once(host: str, command: str, timeout: int) -> None:
    if shutil.which(command) is None:
        raise PermanentError(f"command not found: {command}")
    try:
        completed = subprocess.run(
            [command, "-c", "1", "-W", str(timeout), host],
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RetryableError(f"process timeout: {exc}") from exc

    if completed.returncode != 0:
        raise RetryableError(f"{command} failed: {(completed.stderr or completed.stdout).strip()}")


def check_with_retry(
    host: str,
    command: str,
    timeout: int,
    max_attempts: int,
    base_delay: float,
) -> HealthResult:
    attempt = 0
    while True:
        attempt += 1
        try:
            check_once(host, command, timeout)
            return HealthResult(host=host, ok=True, attempts=attempt, detail="ok")
        except PermanentError as exc:
            return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
        except RetryableError as exc:
            if attempt >= max_attempts:
                return HealthResult(host=host, ok=False, attempts=attempt, detail=str(exc))
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, delay * 0.1)
            logger.debug("host=%s attempt=%s retry in %.2fs: %s", host, attempt, delay + jitter, exc)
            time.sleep(delay + jitter)
```

`PermanentError` はリトライせずに即座に結果へ反映する。
`RetryableError` は上限回数まで指数バックオフで再試行し、上限に達したら失敗として記録する。

---

## 8.12 セキュリティ上の注意点

- 例外メッセージやスタックトレースに、秘密情報（トークン、パスワード、内部パス）を含めない
- 利用者向けメッセージには詳細を出しすぎない。攻撃者にシステム構成のヒントを与える場合がある
- リトライ処理が、認証エラーのような恒久的な失敗を繰り返すと、対象システムのアカウントロックを誘発することがある。恒久的なエラーは即座に打ち切る
- ロールバック処理自体も失敗しうる。ロールバックの失敗は、握りつぶさず別経路で強く警告する
- `trap` や `catch` の中で新たに例外を起こす処理（ログ出力先への書き込み失敗など）を入れる場合、無限ループにならないよう注意する

> **警告**: 本章のロールバック例は学習用の簡略構成である。本番環境でのロールバックは、対象システムの整合性制約（外部連携、キャッシュ、依存サービス）を踏まえて個別に設計すること。

---

## 8.13 テスト方法

リトライロジックは、失敗回数を制御できるダミー関数でテストする。

```python
import pytest

from samples.python.retry_backoff import PermanentError, RetryableError, retry_with_backoff


def test_retry_succeeds_after_failures(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = {"count": 0}

    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] < 3:
            raise RetryableError("temporary")
        return "ok"

    assert retry_with_backoff(flaky, max_attempts=5, base_delay=0.01) == "ok"
    assert calls["count"] == 3


def test_permanent_error_not_retried(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = {"count": 0}

    def always_permanent() -> None:
        calls["count"] += 1
        raise PermanentError("bad credentials")

    with pytest.raises(PermanentError):
        retry_with_backoff(always_permanent, max_attempts=5, base_delay=0.01)
    assert calls["count"] == 1


def test_gives_up_after_max_attempts(monkeypatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _: None)

    def always_retryable() -> None:
        raise RetryableError("still failing")

    with pytest.raises(RetryableError):
        retry_with_backoff(always_retryable, max_attempts=3, base_delay=0.01)
```

`time.sleep` をモックすることで、指数バックオフのテストが実時間を待たずに実行できる。
`calls["count"]` のように呼び出し回数を数え、リトライ回数と打ち切り条件を検証する。

Bash:

```bash
source samples/bash/08_retry_backoff.sh
set +e

attempt_count=0
flaky() {
  attempt_count=$(( attempt_count + 1 ))
  [[ "${attempt_count}" -ge 3 ]]
}

retry_with_backoff 5 0 flaky
[[ "$?" -eq 0 ]] || { echo "fail: should eventually succeed" >&2; exit 1; }
[[ "${attempt_count}" -eq 3 ]] || { echo "fail: unexpected attempt count ${attempt_count}" >&2; exit 1; }
echo ok
```

---

## 章末問題

1. リトライしてよい失敗と、リトライしてはいけない失敗を、HTTPステータスコードを例に3つずつ挙げよ。
2. `except Exception: pass` がなぜ危険か、想定外のバグを例に説明せよ。
3. Bashの `trap ... ERR` が発火しない条件を、`if` の条件式を例に説明せよ。
4. 部分成功を全体成功として報告した場合、監視やアラートにどのような悪影響が出るか述べよ。
5. 利用者向けメッセージに詳細なスタックトレースを含めるべきでない理由を、セキュリティの観点で述べよ。

## 解答と解説

1. リトライしてよい: 429、502、503。リトライしてはいけない: 400、401、403。
2. 意図した例外だけでなく、`TypeError` や `AttributeError` のようなコードのバグまで握りつぶし、発見が遅れる。
3. `if false; then :; fi` のように、条件式として評価されたコマンドの失敗は、`set -e` による終了もERRトラップも発火しない設計になっている。
4. 失敗が可視化されず、対応が遅れる。監視が「全体成功」を根拠にアラートを出さず、実際には一部の対象が壊れたまま放置される。
5. スタックトレースには内部のファイルパス、使用ライブラリ、時には設定値が含まれ、攻撃者に有用な情報を与える可能性がある。

---

## 実装演習

1. `08_retry_backoff.py` に、`Retry-After` ヘッダー相当の値を受け取り、指数バックオフより優先して待機時間を決める機能を追加せよ。
2. Bash版の `retry_with_backoff` に、特定の終了コード（例: 124のタイムアウト）だけをリトライ対象にし、それ以外は即座に打ち切る分岐を追加せよ。
3. PowerShell版で、`PermanentErrorException` に相当するカスタム例外クラスを定義し、リトライ対象外として扱うテストを書け。

---

## 次章予告

第9章では、ログを扱う。
printとログの違い、ログレベル、構造化ログ、実行ID、秘密情報のマスキングを三言語で実装する。


---


<!-- SOURCE: 09_logging.md -->

# 第9章 ログ

## 学習目標

- printとログの違いを説明し、ログレベルを用途で使い分けられる
- タイムスタンプと実行ID付きの構造化ログを三言語で出力できる
- JSONログを設計し、ローテーションと出力先を運用に合わせて設定できる
- 秘密情報とPIIをログからマスキングし、過剰ログを抑制できる

前提: 第1章（標準出力・標準エラー・終了コード）、第3章（JSON）。

サンプルコードは学習用である。
本番のログ基盤（集約先、保持期間、アクセス権）は対象システムの方針に従って別途設計すること。

---

## 9.1 基本概念

**ログ**は、実行中の出来事を時系列で記録した情報である。

`print` は、開発中の一時的な確認に向く。
呼び出すたびに標準出力へ無条件で書き、レベルや出力先を後から制御できない。

**ロギング**は、レベル、出力先、フォーマットを実行時に切り替えられる仕組みである。
Pythonの `logging` モジュール、PowerShellの `Write-Verbose`/`Write-Information`、Bashの自作関数がこれにあたる。

運用スクリプトでprintだけを使うと、次の問題が起きる。

- 調査に必要なログと進捗表示が同じ形式で混在する
- 本番で静かにしたくても、コード中の `print` を探して消す以外に方法がない
- 出力にタイムスタンプや実行元の情報が付かない

---

## 9.2 ログレベル

**ログレベル**は、メッセージの重大度を段階で表す分類である。

| レベル | 用途 | 例 |
|--------|------|-----|
| DEBUG | 開発時の詳細な追跡情報 | 個々のリクエストの中身、変数の値 |
| INFO | 正常な進行の記録 | ホストの処理開始、処理件数 |
| WARNING | 異常ではないが注意が要る事象 | リトライ発生、非推奨設定の使用 |
| ERROR | 個別処理の失敗 | 1ホストへの接続失敗 |
| CRITICAL | 続行不能な致命的事象、または監視上のCRITICAL | 全ホスト不通、設定ファイル破損 |

`opsctl` の `--verbose`/`--quiet` は、レベルの下限を切り替える。

| オプション | 出力される最低レベル |
|------------|----------------------|
| （既定） | INFO |
| `--verbose` | DEBUG |
| `--quiet` | WARNING |

`--verbose` と `--quiet` は同時指定を許可しない。
両方が指定された場合は、引数解析の時点で終了コード1にする（第1章のusageエラーと同じ扱い）。

---

## 9.3 タイムスタンプと実行ID

**実行ID**（`run_id`）は、1回の実行を一意に識別する値である。
UUIDを使うと、他システムとの衝突をほぼ避けられる。

実行IDが無いと、同時に動いた複数のプロセスのログが交ざったとき、どの行がどの実行に属すか追えなくなる。

タイムスタンプは第3章の方針に従い、UTCまたはタイムゾーン付きISO 8601で記録する。

Python:

```python
import uuid
from datetime import datetime, timezone

run_id = str(uuid.uuid4())
timestamp = datetime.now(timezone.utc).isoformat()
```

Bash:

```bash
run_id="$(uuidgen 2>/dev/null || python3 -c 'import uuid; print(uuid.uuid4())')"
timestamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
```

PowerShell:

```powershell
$runId = [guid]::NewGuid().ToString()
$timestamp = [DateTimeOffset]::UtcNow.ToString('o')
```

実行IDは、開始時に一度だけ生成し、その実行の全ログ行へ付与する。
サブプロセスへ引き継ぐ場合は、環境変数（例: `OPSCTL_RUN_ID`）で渡す。

---

## 9.4 最小構成のログ

Python:

```python
#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys

logger = logging.getLogger("minimal_demo")


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    logger.info("starting")
    logger.warning("disk usage high: %s%%", 85)
    logger.info("finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash（タイムスタンプ付き関数）:

```bash
#!/usr/bin/env bash
set -euo pipefail

log() {
  local level="$1"
  shift
  printf '%s %s %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "${level}" "$*" >&2
}

log INFO "starting"
log WARNING "disk usage high: 85%"
log INFO "finished"
```

PowerShell:

```powershell
#!/usr/bin/env pwsh
function Write-Log {
    param(
        [Parameter(Mandatory = $true)][string]$Level,
        [Parameter(Mandatory = $true)][string]$Message
    )
    $ts = [DateTimeOffset]::UtcNow.ToString('o')
    [Console]::Error.WriteLine("$ts $Level $Message")
}

Write-Log -Level INFO -Message 'starting'
Write-Log -Level WARNING -Message 'disk usage high: 85%'
Write-Log -Level INFO -Message 'finished'
```

三言語とも、ログは標準エラーへ出す。
標準出力は、第1章の方針どおり機械可読な結果専用にする。

---

## 9.5 構造化ログとJSONログ

**構造化ログ**は、メッセージを自由文ではなく、決まったフィールドの組として記録する方式である。

**JSONログ**は、構造化ログを1行1JSONオブジェクトで書く形式である。
`grep`、`jq`、ログ集約基盤のいずれでも扱いやすい。

`opsctl` の設定（README参照）は、JSONログと実行ID付与を既定にしている。

```yaml
logging:
  format: json
  include_run_id: true
```

推奨フィールド:

| フィールド | 内容 |
|------------|------|
| `ts` | ISO 8601形式のタイムスタンプ |
| `level` | ログレベル |
| `run_id` | 実行ID |
| `event` | ロガー名やイベント種別 |
| `host` | 対象ホスト（該当する場合） |
| `message` | 人が読む本文 |

Python（`logging.Formatter` を継承した最小実装）:

```python
import json
import logging


class JsonFormatter(logging.Formatter):
    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "run_id": self.run_id,
            "event": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)
```

Bash（`jq -n` で1行のJSONを組み立てる）:

```bash
log_json() {
  local level="$1"
  local message="$2"
  jq -n -c \
    --arg ts "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --arg level "$level" \
    --arg run_id "${RUN_ID:-unknown}" \
    --arg message "$message" \
    '{ts: $ts, level: $level, run_id: $run_id, event: "opsctl", message: $message}' >&2
}

log_json INFO "starting"
```

PowerShell（`ConvertTo-Json` で1行にする）:

```powershell
function Write-JsonLog {
    param(
        [string]$Level,
        [string]$Message,
        [string]$RunId
    )
    [pscustomobject]@{
        ts      = [DateTimeOffset]::UtcNow.ToString('o')
        level   = $Level
        run_id  = $RunId
        event   = 'opsctl'
        message = $Message
    } | ConvertTo-Json -Compress | ForEach-Object { [Console]::Error.WriteLine($_) }
}

Write-JsonLog -Level 'INFO' -Message 'starting' -RunId ([guid]::NewGuid().ToString())
```

---

## 9.6 実務向け改善: opsctl共通ロガー

`samples/python/09_json_logger.py` に、実行ID付与、JSONフォーマット、ファイル出力、秘密情報マスキングをまとめたヘルパーを置く。

```python
#!/usr/bin/env python3
"""opsctl向けの共通JSONロギングヘルパー。

logger, run_id = configure_json_logging("opsctl.ping_check", verbose=args.verbose)
のように、各サブコマンドの先頭で呼び出す想定である。
"""
from __future__ import annotations

import json
import logging
import re
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path

_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?i)(authorization\s*:\s*)(.+)"),
    re.compile(r"(?i)\b(token=)([^&\s]+)"),
    re.compile(r"(?i)\b(password=)([^&\s]+)"),
    re.compile(r"(?i)\b(api[_-]?key=)([^&\s]+)"),
]


def mask_secrets(message: str) -> str:
    """既知の秘密情報パターンを ``***`` へ置き換える。

    完全な検出は保証できない。ログ出力前に、そもそも秘密情報を
    メッセージへ含めない設計を優先する。
    """
    masked = message
    for pattern in _SECRET_PATTERNS:
        masked = pattern.sub(lambda m: f"{m.group(1)}***", masked)
    return masked


class JsonFormatter(logging.Formatter):
    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def format(self, record: logging.LogRecord) -> str:
        message = mask_secrets(record.getMessage())
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "run_id": self.run_id,
            "event": record.name,
            "message": message,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_json_logging(
    logger_name: str,
    *,
    verbose: bool = False,
    quiet: bool = False,
    log_file: Path | None = None,
) -> tuple[logging.Logger, str]:
    if verbose and quiet:
        raise ValueError("verbose and quiet are mutually exclusive")

    run_id = str(uuid.uuid4())
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()  # 二重呼び出しで行が重複するのを防ぐ
    logger.propagate = False

    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger.setLevel(level)

    formatter = JsonFormatter(run_id)

    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, run_id


def main() -> int:
    logger, run_id = configure_json_logging(
        "opsctl.demo", verbose=True, log_file=Path("work/logs/demo.log")
    )
    logger.info("run started")
    logger.debug("connecting host=web01.example.invalid")
    logger.warning("Authorization: Bearer sk-do-not-log-this-value")
    logger.error("host unreachable host=web02.example.invalid")
    logger.info("run finished run_id=%s", run_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

`mask_secrets` は、レンダリング後の完成メッセージに対して呼ぶ。
`record.msg`（`%s` などを含むテンプレート文字列）へ先に適用すると、引数側に埋め込まれた秘密情報を見逃す。

実行例:

```bash
python3 samples/python/09_json_logger.py
# stderr（抜粋、実際は1行1JSON）:
# {"ts": "...", "level": "WARNING", "run_id": "...", "event": "opsctl.demo", "message": "Authorization: ***"}
```

---

## 9.7 ログローテーション

**ログローテーション**は、ログファイルを一定の条件で切り替え、古いものを退避または削除する運用である。
無制限にログを追記し続けると、ディスクを圧迫する。

Python（サイズ基準、9.6の `RotatingFileHandler` と同じ仕組み）:

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "work/logs/opsctl.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
```

時間基準でローテーションしたい場合は `TimedRotatingFileHandler` を使う。

```python
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler(
    "work/logs/opsctl.log",
    when="midnight",
    backupCount=14,
    encoding="utf-8",
)
```

Linuxでは、アプリケーション側に実装せず `logrotate` へ委ねる選択もある。

```text
# /etc/logrotate.d/opsctl
/var/log/opsctl/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
    copytruncate
}
```

`copytruncate` は、ログを書き続けるプロセスがファイルディスクリプタを再オープンしない場合に使う。
プロセス側でSIGHUPを受けて再オープンできるなら、`copytruncate` を外し、`postrotate` でシグナル送信する方が欠損が少ない。

Windowsでは `logrotate` 相当の標準ツールがない。
`TimedRotatingFileHandler` などアプリケーション側での実装か、イベントログへの記録を検討する。

---

## 9.8 悪い例と問題点

### 悪いコード

```python
#!/usr/bin/env python3
import subprocess
import sys

token = sys.argv[1]
host = sys.argv[2]

print(f"calling api with token={token}")
result = subprocess.run(
    f"curl -H 'Authorization: Bearer {token}' https://api.example.invalid/v1/hosts/{host}",
    shell=True,
    capture_output=True,
    text=True,
)
print(result.stdout)
print(result.stderr)
if result.returncode != 0:
    print("failed")
```

問題点:

- トークンをそのまま標準出力へ出しており、ターミナル履歴やCI実行ログに残る
- `print` だけでレベルが無く、本番で静かにする手段がない
- タイムスタンプと実行IDが無く、複数実行のログが混ざると追跡できない
- 失敗時のメッセージが `"failed"` のみで、原因調査に必要な情報が残らない
- `shell=True` と文字列連結でコマンドを組み立てている（第10章で扱うコマンドインジェクションの温床）

### 改善後

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(0, str((__file__.rsplit("/", 2)[0])))  # samples/python を解決するための最小限の調整
from json_logger import configure_json_logging  # noqa: E402  (09_json_logger.py を想定)

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2


def main(argv: list[str]) -> int:
    logger, run_id = configure_json_logging("opsctl.api_call")

    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        logger.error("OPSCTL_API_TOKEN is required")
        return EXIT_USAGE
    if len(argv) < 1:
        logger.error("usage: api_call.py HOST")
        return EXIT_USAGE
    host = argv[0]

    logger.info("calling api host=%s run_id=%s", host, run_id)
    result = subprocess.run(
        ["curl", "-sS", "-H", f"Authorization: Bearer {token}",
         f"https://api.example.invalid/v1/hosts/{host}"],
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
    )
    if result.returncode != 0:
        logger.error("api call failed host=%s returncode=%s", host, result.returncode)
        return EXIT_RUNTIME

    logger.info("api call succeeded host=%s", host)
    print(result.stdout)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

改善後は、トークンをログへ出さず、レベルと実行IDを持ち、`shell=True` を使わずリスト引数で `curl` を呼ぶ。
`import` パスの調整はサンプル間の依存を示す簡略表現であり、実務では `samples/python` をパッケージとして整え、通常の `import` で解決する（第5章）。

---

## 9.9 過剰ログの抑制

大量のホストや繰り返し処理をすべてINFOで記録すると、ログ量が増え、重要な行が埋もれる。

対策:

1. ループ内の個別成功はDEBUGにし、INFOは集計行（開始・終了・件数）に絞る
2. 同一エラーが連続する場合は、件数をまとめて1行で報告する
3. ポーリングや定期チェックの「変化なし」を毎回記録しない。状態が変わった時だけ記録する
4. `logging.basicConfig` や `configure_json_logging` を1実行につき1回だけ呼ぶ。複数回呼ぶとハンドラが重複し、同じ行が複数回出力される

```python
failures = 0
for host in hosts:
    ok, detail = check(host)
    if ok:
        logger.debug("host=%s ok", host)
    else:
        failures += 1
        logger.error("host=%s failed detail=%s", host, detail)

logger.info("summary total=%s failures=%s", len(hosts), failures)
```

---

## 9.10 PII/秘密のマスキング

**マスキング**は、ログに残すべきでない値を、判読できない代替表現に置き換える処理である。

対象になりやすい値:

- APIトークン、パスワード、秘密鍵
- `Authorization` ヘッダー全体
- 個人を特定できる情報（メールアドレス、電話番号、氏名などのPII）
- クエリ文字列に含まれるトークン（`?token=...`）

> **警告**: リクエスト・レスポンスの本文をそのままログに出す実装は、意図せず秘密情報やPIIを記録する。
> デバッグ目的でも、本文全体のダンプは既定で無効にし、必要な項目だけを選んで記録する。

9.6の `mask_secrets` は正規表現によるマスキングであり、想定外の形式は見逃す。
確実性を上げるには、次を組み合わせる。

- ログに渡す前の時点で、秘密情報を持つオブジェクトから除外する（マスキングに頼らない設計）
- URLを記録するときはクエリ文字列を除去するか、既知のキーだけを除去する
- ログ集約基盤側でも、既知パターンの再マスキングやアクセス制御を設定する

---

## 9.11 調査可能なログ

**調査可能なログ**は、障害発生後に「いつ・どこで・何が起きたか」を、ログだけから再構成できるログである。

満たすべき条件:

- 実行ID、タイムスタンプ、対象ホスト、処理名、結果を含む
- エラー時は、原因になった例外の型とメッセージを含む（スタックトレース全体はDEBUGでもよい）
- 成功と失敗を同じフィールド構成で記録し、集計しやすくする
- 時刻はUTC、または常に同じタイムゾーン表記で統一する

```python
logger.error(
    "disk check failed host=%s error_type=%s error=%s",
    host,
    type(exc).__name__,
    exc,
)
```

---

## 9.12 セキュリティ上の注意点

- トークン、パスワード、秘密鍵をログへ書かない。9.10のマスキングは補助であり、根本対策は「そもそも記録しない設計」である
- リクエスト全文やレスポンス全文の無条件ログを避ける
- ログファイルの権限を絞る（例: `chmod 640`）。誰でも読めるパーミッションにしない
- ログ集約先への転送経路はTLSを使う（第11章）
- 監査目的のログ（誰が何を実行したか）は、デバッグログと分離し、改ざん検知や保持期間の要件を満たす場所へ送る（第10章の監査ログ）

---

## 9.13 テスト方法

Python（`caplog` でログ出力を検証する）:

```python
import logging

from samples.python.json_logger import mask_secrets


def test_mask_secrets_authorization_header() -> None:
    masked = mask_secrets("Authorization: Bearer sk-abcdef123456")
    assert "sk-abcdef123456" not in masked
    assert masked.startswith("Authorization: ")


def test_logger_emits_info(caplog) -> None:
    logger = logging.getLogger("test_logger_demo")
    logger.setLevel(logging.INFO)
    with caplog.at_level(logging.INFO):
        logger.info("host=%s ok", "web01.example.invalid")
    assert "web01.example.invalid" in caplog.text
```

Bash（出力形式の検証）:

```bash
output="$(bash -c 'source samples/bash/09_log_helpers.sh; log INFO "hello"' 2>&1)"
[[ "${output}" == *"INFO hello"* ]]
```

PowerShell（Pesterの骨格）:

```powershell
Describe 'Write-Log' {
    It 'writes level and message to stderr' {
        $err = & pwsh -NoProfile -Command {
            . ./samples/powershell/09_log_helpers.ps1
            Write-Log -Level 'INFO' -Message 'hello'
        } 2>&1
        $err | Should -Match 'INFO hello'
    }
}
```

---

## 章末問題

### 問題1

`print` とロギングモジュールの違いを、レベル・出力先・切り替え可能性の三点で説明せよ。

### 問題2

`Authorization: Bearer xxxx` をログに残した場合の具体的な被害を一つ挙げ、防止策を二つ述べよ。

### 問題3

`logging.basicConfig` を1実行の中で複数回呼ぶと何が起きるか説明し、防止方法を書け。

### 問題4

ポーリング型の監視スクリプトで、毎回のチェックをすべてINFOで出すと何が問題になるか述べ、改善方針を書け。

### 問題5

ログローテーションを実装しない場合に起きる運用上の問題を一つ挙げよ。

---

## 解答と解説

### 問題1

`print` はレベルが無く常に標準出力へ出る。
ロギングは、レベルで出力可否を制御し、出力先（標準エラー、ファイル、外部基盤）を実行時に切り替えられる。

### 問題2

被害例: 漏えいしたトークンで第三者がAPIを呼び、想定外の操作や情報取得をされる。
防止策: ログへ出す前にマスキングする、そもそもトークンを引数やログの対象文字列に含めない設計にする。

### 問題3

呼ぶたびにハンドラが追加され、同じログ行が複数回出力される。
防止方法: 設定関数の先頭で既存ハンドラをクリアするか、設定済みかどうかをフラグで管理して二重設定を防ぐ。

### 問題4

ログ量が増え、異常発生時の行が埋もれる。
改善方針: 個別の正常結果はDEBUGにし、INFOは開始・終了・集計に絞る。
状態変化時のみ記録する方式も有効である。

### 問題5

ディスクを圧迫し、最悪の場合はディスク枯渇で他の処理まで失敗する。
古いログの保持期間も管理できなくなる。

---

## 実装演習

### 演習A

`samples/python/09_json_logger.py` の `configure_json_logging` を使い、3台のホスト名を受け取って疎通確認の体裁（ダミーでよい）をログに残すスクリプトを書け。
DEBUGとINFOの使い分けを明示すること。

### 演習B

`mask_secrets` に、クエリ文字列 `?token=...` を検出して置換するパターンを追加し、テストを書け。

### 演習C

Bashで `log_json` 関数を作り、`RUN_ID` 環境変数を実行開始時に一度だけ生成して全ログ行へ付与するスクリプトを書け。

---

## 次章予告

第10章では、入力値検証とセキュリティを扱う。
型・範囲・パスの検証、コマンドインジェクションとパストラバーサルの対策、秘密情報の扱いを実装する。


---


<!-- SOURCE: 10_validation_and_security.md -->

# 第10章 入力値検証とセキュリティ

## 学習目標

- 型・必須・範囲・パスの検証を三言語で実装できる
- コマンドインジェクションとパストラバーサルの成立条件と対策を説明できる
- 秘密情報を環境変数とシークレット管理で扱い、コードに書かない設計にできる
- TLS検証、一時ファイル、最小権限、監査ログの基本方針を実装できる

前提: 第1章（環境変数）、第7章（コマンド実行）、第9章（ログ）。

サンプルコードは学習用である。
本番投入前には、対象システムでの侵入テストや脆弱性診断に相当する確認、権限設計のレビューを別途行うこと。

---

## 10.1 基本概念

**入力値検証**は、外部から受け取った値が、想定する型・範囲・形式に収まっているかを確認する処理である。

運用スクリプトへの入力は、コマンドライン引数、設定ファイル、環境変数、API応答、他プロセスの出力など多岐にわたる。
これらはすべて「信頼できない入力」として扱い、使う前に検証する。

検証を省略すると、誤操作や悪意ある入力が、意図しないコマンド実行やファイルアクセスに直結する。

---

## 10.2 最小構成の検証: 型・必須・範囲

第4章の `classify_usage` を例に、必須・範囲の検証を確認する。

```python
def classify(usage: float, warn: float, crit: float) -> str:
    if usage < 0 or usage > 100:
        raise ValueError("usage must be between 0 and 100")
    if warn < 0 or crit < 0 or warn > 100 or crit > 100:
        raise ValueError("thresholds must be between 0 and 100")
    if warn > crit:
        raise ValueError("warn must be <= crit")
    ...
```

辞書形式の設定値を検証する場合は、必須キーの欠落と型不一致を分けて報告すると、利用者が直しやすい。

```python
def validate_target_config(config: dict) -> None:
    required = ["host", "port"]
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError(f"missing required keys: {missing}")
    if not isinstance(config["port"], int):
        raise TypeError("port must be an integer")
    if not (1 <= config["port"] <= 65535):
        raise ValueError("port must be between 1 and 65535")
```

Bash（整数と範囲）:

```bash
validate_port() {
  local port="$1"
  if ! [[ "${port}" =~ ^[0-9]+$ ]]; then
    echo "port must be numeric: ${port}" >&2
    return 1
  fi
  if (( port < 1 || port > 65535 )); then
    echo "port out of range: ${port}" >&2
    return 1
  fi
}
```

PowerShell:

```powershell
function Assert-ValidPort {
    param([Parameter(Mandatory = $true)][int]$Port)
    if ($Port -lt 1 -or $Port -gt 65535) {
        throw "port out of range: $Port"
    }
}
```

---

## 10.3 パス検証とパストラバーサル対策

**パストラバーサル**は、`../` などを含む入力によって、想定した範囲外のファイルへアクセスさせる攻撃である。

### 悪いコード

```python
from pathlib import Path

def read_report(base_dir: str, filename: str) -> str:
    path = Path(base_dir) / filename
    return path.read_text(encoding="utf-8")

# filename = "../../../../etc/passwd" を渡すと base_dir の外を読んでしまう
```

### 改善後

```python
from pathlib import Path


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    """base_dir 配下に解決できないパスは拒否する。"""
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def read_report(base_dir: Path, filename: str) -> str:
    path = safe_resolve_path(base_dir, filename)
    return path.read_text(encoding="utf-8")
```

`resolve()` はシンボリックリンクを解決したうえで絶対パスにする。
`base_dir` 配下に見えるシンボリックリンクが外部を指している場合、この検証だけでは不十分になる場合がある。
公開範囲が広い用途では、シンボリックリンクの追跡自体を禁止する、あるいは対象ディレクトリの書き込み権限を管理者以外に与えない、といった追加の防御を検討する。

Bash（`realpath` で解決してから前方一致を確認する）:

```bash
safe_resolve_path() {
  local base_dir="$1"
  local relative_path="$2"
  local base_resolved candidate

  base_resolved="$(realpath -e "${base_dir}")" || return 1
  candidate="$(realpath -m "${base_resolved}/${relative_path}")"

  case "${candidate}" in
    "${base_resolved}"/*|"${base_resolved}")
      printf '%s\n' "${candidate}"
      ;;
    *)
      echo "path escapes base directory: ${relative_path}" >&2
      return 1
      ;;
  esac
}
```

PowerShell:

```powershell
function Get-SafeResolvedPath {
    param(
        [Parameter(Mandatory = $true)][string]$BaseDir,
        [Parameter(Mandatory = $true)][string]$RelativePath
    )
    $baseResolved = (Resolve-Path -LiteralPath $BaseDir).Path
    $candidate = [System.IO.Path]::GetFullPath((Join-Path $baseResolved $RelativePath))
    if (-not ($candidate -eq $baseResolved -or $candidate.StartsWith($baseResolved + [System.IO.Path]::DirectorySeparatorChar))) {
        throw "path escapes base directory: $RelativePath"
    }
    return $candidate
}
```

---

## 10.4 コマンドインジェクション対策

**コマンドインジェクション**は、外部入力を通じて、意図しないコマンドをシェルに実行させる攻撃である。

### 悪いコード

```python
import subprocess

def ping(host: str) -> str:
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return result.stdout

# host = "web01.example.invalid; rm -rf /tmp/work" のような入力で
# セミコロン以降が別コマンドとして実行される
```

### 改善後

```python
import re
import subprocess

HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def ping(host: str, timeout: int = 3) -> str:
    validate_hostname(host)
    result = subprocess.run(
        ["ping", "-c", "1", "-W", str(timeout), host],
        capture_output=True,
        text=True,
        timeout=timeout + 2,
        shell=False,
    )
    return result.stdout
```

対策の骨子は二つある。

1. `shell=True` を使わず、コマンドと引数をリストで渡す（第7章）
2. リストで渡す場合でも、値そのものが想定形式であることを検証する（コマンド名やオプションのすり替えを防ぐ）

Bashでは、`eval` と、引用符を欠いた変数展開が主な原因になる。

```bash
# 悪い例: evalで動的にコマンドを組み立てる
eval "ping -c 1 ${host}"

# 改善: 配列と引用符で引数を分離する
cmd=(ping -c 1 -- "${host}")
"${cmd[@]}"
```

PowerShellでは `Invoke-Expression` が同種のリスクを持つ。

```powershell
# 悪い例
Invoke-Expression "ping -n 1 $HostName"

# 改善: 呼び出し演算子と配列引数
$pingArgs = @('-n', '1', $HostName)
& ping @pingArgs
```

---

## 10.5 権限と最小権限

**最小権限の原則**は、処理の実行に必要な最小限の権限だけを与える考え方である。

実務上の指針:

- スクリプト全体をroot/Administratorで実行せず、必要な一操作だけを昇格する（`sudo` を特定コマンドに限定する、Windowsではタスクの実行アカウントを分ける）
- 秘密情報を含むファイルはパーミッションを絞る（`chmod 600`）
- サービスアカウントには、対象リソースへの読み書きなど、必要な操作のみを許可する
- 一時的な昇格は、目的と期間を監査ログに残す

```bash
chmod 600 /etc/opsctl/secrets.env
chown opsctl:opsctl /etc/opsctl/secrets.env
```

---

## 10.6 秘密情報と環境変数

秘密情報（APIトークン、パスワード、秘密鍵）は、次の場所に置かない。

- ソースコード中のリテラル
- Gitリポジトリにコミットする設定ファイル
- コマンドライン引数（`ps` や プロセス一覧で他ユーザーに見える場合がある）

環境変数、または後述のシークレット管理サービスから実行時に読み込む。

```python
import os
import sys

token = os.environ.get("OPSCTL_API_TOKEN")
if not token:
    print("OPSCTL_API_TOKEN is required", file=sys.stderr)
    sys.exit(1)
```

> **警告**: 秘密情報を `--token xxxx` のような引数で渡す設計は、`ps aux` や監査ログに値が残る場合がある。
> 環境変数か、値を含まないファイルパス渡し（ファイル自体の権限で保護する）を優先する。

---

## 10.7 シークレット管理

**シークレット管理**は、秘密情報の保存・配布・失効を一元的に扱う仕組みである。

方針:

- 秘密情報をリポジトリへコミットしない（`.gitignore` に環境変数ファイルを含める。第16章）
- 本番の秘密情報はHashiCorp Vault、AWS Secrets Manager、Azure Key Vaultのような専用サービス、またはCIの秘密変数機能で管理する
- 定期的にローテーション（値の更新と旧値の失効）する
- 漏えいが疑われたら、即座に失効し、影響範囲を監査ログから確認する

学習用の値は、必ず無効なダミー（`replace-me` など）にする。

```bash
export OPSCTL_API_TOKEN='replace-me'
```

---

## 10.8 TLS検証

**TLS検証**は、通信先の証明書が信頼できる認証局によって発行され、想定したホスト名と一致するかを確認する処理である。
検証を無効化すると、通信内容の盗聴や改ざん（中間者攻撃）を検出できなくなる。

> **警告**: `requests` の `verify=False`、curlの `-k`/`--insecure`、PowerShellの `-SkipCertificateCheck` は、TLS証明書検証を無効化する。
> 自己署名証明書の検証環境であっても、検証を無効化するのではなく、その環境のCA証明書をシステムまたはライブラリの信頼ストアへ登録する方法を優先する。

```python
import requests

# 悪い例
requests.get("https://api.example.invalid/v1/hosts", verify=False)

# 改善: 既定の検証を有効のままにし、社内CAが必要なら証明書バンドルを指定する
requests.get(
    "https://api.example.invalid/v1/hosts",
    verify="/etc/ssl/certs/internal-ca-bundle.pem",
)
```

第11章で、TLSを含むAPI呼び出しの全体像を扱う。

---

## 10.9 安全でない一時ファイル

予測可能な名前の一時ファイル（`/tmp/report.txt` など）は、他プロセスによる先読み・上書き・シンボリックリンク攻撃の対象になりうる。

Python:

```python
import tempfile
from pathlib import Path


def write_temp_report(content: str) -> Path:
    fd, name = tempfile.mkstemp(prefix="opsctl_", suffix=".txt")
    path = Path(name)
    try:
        with path.open("w", encoding="utf-8") as fh:
            fh.write(content)
    finally:
        import os

        os.close(fd)
    path.chmod(0o600)
    return path
```

`tempfile.mkstemp` は、他プロセスと衝突しないランダムな名前で、所有者のみアクセス可能なファイルを作る。

Bash:

```bash
tmp_file="$(mktemp /tmp/opsctl.XXXXXX)"
trap 'rm -f "${tmp_file}"' EXIT
```

PowerShell:

```powershell
$tmpFile = New-TemporaryFile
try {
    Set-Content -LiteralPath $tmpFile -Value 'report body' -Encoding utf8
}
finally {
    Remove-Item -LiteralPath $tmpFile -ErrorAction SilentlyContinue
}
```

---

## 10.10 監査ログ

**監査ログ**は、誰が・いつ・何を実行したかを、後から検証できる形で残す記録である。
デバッグ用のログと目的が異なるため、分離して扱う。

満たすべき条件:

- 実行者（サービスアカウント名、ログイン名）を含む
- 実行した操作、対象、結果（成功/失敗）を含む
- 改ざんされにくい保存先に送る（追記専用ストレージ、集約基盤）
- 保持期間をコンプライアンス要件に合わせて設定する

```python
audit_logger.info(
    "operation=%s actor=%s target=%s result=%s run_id=%s",
    "config-patch",
    os.environ.get("USER", "unknown"),
    target_host,
    "success",
    run_id,
)
```

破壊的操作（削除、設定変更、権限変更）を実行するサブコマンドは、監査ログを必須とし、dry-runでない実行のみ記録する。

---

## 10.11 悪い例と問題点（統合）

```python
#!/usr/bin/env python3
import subprocess
import sys

base_dir = "/var/opsctl/configs"


def patch_config(filename: str, host: str) -> None:
    path = base_dir + "/" + filename          # パス検証なし
    subprocess.run(f"scp {path} {host}:/etc/app.conf", shell=True)  # shell=True + 文字列連結
    print(f"patched {host}")                  # 成否を確認せず成功と表示


if __name__ == "__main__":
    patch_config(sys.argv[1], sys.argv[2])
```

問題点:

- `filename` にパストラバーサル文字列を渡すと `base_dir` 外のファイルを送信できる
- `host` や `filename` に `;` や `` ` `` を含めるとコマンドインジェクションが成立する
- `subprocess.run` の戻り値を確認しておらず、失敗しても成功と表示する
- 秘密情報や監査ログが無く、誰がいつ何を変更したか後から追えない

---

## 10.12 改善後のコード

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2

BASE_DIR = Path("/var/opsctl/configs")
HOSTNAME_RE = re.compile(
    r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,62})(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,62}))*$"
)

logger = logging.getLogger("config_patch")
audit_logger = logging.getLogger("config_patch.audit")


def safe_resolve_path(base_dir: Path, relative_path: str) -> Path:
    base_resolved = base_dir.resolve(strict=True)
    candidate = (base_resolved / relative_path).resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"path escapes base directory: {relative_path}")
    return candidate


def validate_hostname(host: str) -> str:
    if not HOSTNAME_RE.match(host):
        raise ValueError(f"invalid hostname: {host!r}")
    return host


def patch_config(filename: str, host: str, *, dry_run: bool) -> int:
    try:
        source = safe_resolve_path(BASE_DIR, filename)
        validate_hostname(host)
    except (OSError, ValueError) as exc:
        logger.error("validation failed: %s", exc)
        return EXIT_USAGE

    if not source.is_file():
        logger.error("config file not found: %s", source)
        return EXIT_USAGE

    if dry_run:
        logger.info("dry-run: would copy %s to %s:/etc/app.conf", source, host)
        return EXIT_OK

    result = subprocess.run(
        ["scp", str(source), f"{host}:/etc/app.conf"],
        capture_output=True,
        text=True,
        timeout=30,
        shell=False,
        check=False,
    )
    actor = os.environ.get("USER", "unknown")
    if result.returncode != 0:
        logger.error("scp failed host=%s stderr=%s", host, result.stderr.strip())
        audit_logger.info(
            "operation=config-patch actor=%s target=%s result=failure", actor, host
        )
        return EXIT_RUNTIME

    logger.info("patched host=%s", host)
    audit_logger.info(
        "operation=config-patch actor=%s target=%s result=success", actor, host
    )
    return EXIT_OK


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy a config file to a target host")
    parser.add_argument("--filename", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    return patch_config(args.filename, args.host, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

改善点は、パス検証、ホスト名検証、`shell=True` の排除、戻り値確認、dry-run、監査ログの六つである。

---

## 10.13 テスト方法

```python
import pytest
from pathlib import Path

from samples.python.safe_path_and_exec import safe_resolve_path, validate_hostname


def test_safe_resolve_path_rejects_traversal(tmp_path: Path) -> None:
    base = tmp_path / "configs"
    base.mkdir()
    with pytest.raises(ValueError):
        safe_resolve_path(base, "../../etc/passwd")


def test_safe_resolve_path_allows_nested_file(tmp_path: Path) -> None:
    base = tmp_path / "configs"
    (base / "sub").mkdir(parents=True)
    resolved = safe_resolve_path(base, "sub/app.conf")
    assert resolved == (base / "sub" / "app.conf").resolve()


@pytest.mark.parametrize("host", ["web01.example.invalid", "db-1.example.invalid"])
def test_validate_hostname_accepts_valid(host: str) -> None:
    assert validate_hostname(host) == host


@pytest.mark.parametrize("host", ["web01; rm -rf /", "$(whoami)", "web01 && id"])
def test_validate_hostname_rejects_injection(host: str) -> None:
    with pytest.raises(ValueError):
        validate_hostname(host)
```

---

## 章末問題

### 問題1

パストラバーサルが成立する条件を、入力例を挙げて説明せよ。

### 問題2

`subprocess.run(cmd, shell=True)` に文字列連結でホスト名を渡す設計の危険を述べ、安全な書き換えを示せ。

### 問題3

APIトークンをコマンドライン引数で渡してはいけない理由を、`ps` コマンドの挙動に触れて説明せよ。

### 問題4

TLS証明書検証を無効化することで防げなくなる攻撃を一つ挙げよ。

### 問題5

監査ログとデバッグログを分離すべき理由を二つ述べよ。

---

## 解答と解説

### 問題1

`../` を含む入力で、`base_dir` の外にあるファイルへパスが解決されると成立する。
例: `filename="../../etc/passwd"`。

### 問題2

ホスト名にシェルのメタ文字（`;`、`` ` ``、`$()`）を含めると、別コマンドとして実行される。
改善: `shell=True` をやめ、リスト引数で渡し、ホスト名を正規表現で検証する。

### 問題3

`ps aux` や `/proc/<pid>/cmdline` から、同一ホスト上の他ユーザーが起動時の引数を閲覧できる場合がある。
環境変数やファイル権限で保護した受け渡しに切り替える。

### 問題4

中間者攻撃（通信の盗聴・改ざん）を検出できなくなる。

### 問題5

監査ログは改ざん耐性と長期保持が求められ、デバッグログは詳細度と揮発性が高い。
目的と保持要件が異なるため、混在させると必要な情報の抽出とアクセス制御が難しくなる。

---

## 実装演習

### 演習A

`safe_resolve_path` を使い、指定ディレクトリ配下のファイル一覧を安全に列挙するPythonスクリプトを書け。
`../` を含む入力で終了コード1になることを確認せよ。

### 演習B

Bashで `validate_hostname` 相当の関数を実装し、ホスト名にセミコロンを含む入力を拒否するテストを書け。

### 演習C

`10_safe_path_and_exec.py` の監査ログ出力を、9章のJSONロガーへ差し替え、`operation`/`actor`/`target`/`result` フィールドを持つJSON行として出力せよ。

---

## 次章予告

第11章では、APIとネットワーク処理を扱う。
HTTPメソッドとステータスコード、認証、タイムアウトとリトライ、ページネーション、レート制限、TLSを含むAPI呼び出しを三言語で実装する。


---


<!-- SOURCE: 11_api_and_network.md -->

# 第11章 APIとネットワーク処理

## 学習目標

- HTTPの主要メソッドとステータスコードの分類を説明できる
- APIキーとOAuthの概要を理解し、認証付きHTTP呼び出しを実装できる
- タイムアウト、リトライ、ページネーション、レート制限を備えたAPI連携を三言語で書ける
- TLSを有効にしたまま、秘密情報を安全に扱うAPIクライアントを設計できる

前提: 第9章（ログ）、第10章（入力検証、TLS検証、秘密情報）。

サンプルコードは学習用である。
本番のAPIへ接続する前に、対象APIの利用規約、レート制限、認証方式を提供元のドキュメントで確認すること。
本章のAPIホストはすべて `example.invalid` を使う実在しないドメインであり、実行してもネットワーク応答は返らない。

---

## 11.1 基本概念

**HTTP**は、クライアントとサーバーがリクエストとレスポンスをやり取りする通信プロトコルである。

**REST**は、リソースをURLで表し、HTTPメソッドで操作するAPI設計の様式である。
`opsctl` の `api-export` サブコマンドは、REST形式のAPIからホスト情報を取得する想定である。

---

## 11.2 メソッドとステータスコード

| メソッド | 意味 | 冪等性 |
|----------|------|--------|
| `GET` | リソースの取得 | 冪等 |
| `POST` | リソースの新規作成、または処理の実行 | 非冪等 |
| `PUT` | リソースの全体置き換え | 冪等 |
| `PATCH` | リソースの部分更新 | 実装依存（非冪等が多い） |
| `DELETE` | リソースの削除 | 冪等（削除済みへの再実行は成功扱いが多い） |

| ステータス範囲 | 分類 | 代表例 |
|----------------|------|--------|
| 2xx | 成功 | `200 OK`、`201 Created`、`204 No Content` |
| 3xx | リダイレクト | `301 Moved Permanently` |
| 4xx | クライアントエラー | `400 Bad Request`、`401 Unauthorized`、`403 Forbidden`、`404 Not Found`、`429 Too Many Requests` |
| 5xx | サーバーエラー | `500 Internal Server Error`、`503 Service Unavailable` |

`opsctl` のAPI呼び出しでは、4xxを利用者・設定エラー（終了コード1）、5xxと通信断をリトライ対象の実行時エラー（終了コード2、上限超過はタイムアウトで終了コード4）に分類する。

---

## 11.3 JSON入出力の基本

APIのリクエスト本文とレスポンス本文は、JSONで表すことが多い（第3章）。

```python
import json

payload = {"host": "web01.example.invalid", "status": "OK"}
body = json.dumps(payload)
parsed = json.loads(body)
```

---

## 11.4 認証: APIキーとOAuthの概要

**APIキー**は、リクエストに添付する固定の文字列で、送信者を識別・認可する方式である。
`Authorization` ヘッダーやクエリパラメータで送ることが多い。

```text
Authorization: Bearer <token>
```

**OAuth**は、利用者の認可を得たうえで、有効期限付きのアクセストークンを発行する仕組みである。
代表的な流れの一つに、サーバー間連携で使う **クライアントクレデンシャルズフロー**がある。

1. クライアントIDとクライアントシークレットを使い、認可サーバーへトークンを要求する
2. 認可サーバーが、有効期限付きのアクセストークンを返す
3. アクセストークンを `Authorization: Bearer <token>` としてAPIへ送る
4. 期限切れ前に再取得する

本書では、`opsctl` の認証をAPIキー方式（環境変数 `OPSCTL_API_TOKEN`）に統一し、OAuthは概要にとどめる。
OAuthを採用するAPIへ接続する場合は、トークン取得処理を独立した関数にまとめ、有効期限とリフレッシュを管理する。

---

## 11.5 最小構成のAPI呼び出し

Python（`requests`）:

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import requests


def main() -> int:
    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        print("OPSCTL_API_TOKEN is required", file=sys.stderr)
        return 1

    response = requests.get(
        "https://api.example.invalid/v1/hosts",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    response.raise_for_status()
    print(response.json())
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

PowerShell（`Invoke-RestMethod`）:

```powershell
#!/usr/bin/env pwsh
$ErrorActionPreference = 'Stop'

$token = $env:OPSCTL_API_TOKEN
if ([string]::IsNullOrWhiteSpace($token)) {
    [Console]::Error.WriteLine('OPSCTL_API_TOKEN is required')
    exit 1
}

$headers = @{ Authorization = "Bearer $token" }
$result = Invoke-RestMethod -Uri 'https://api.example.invalid/v1/hosts' -Headers $headers -TimeoutSec 10
$result | ConvertTo-Json -Depth 5
```

Bash（curl）:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPSCTL_API_TOKEN:-}" ]]; then
  echo "OPSCTL_API_TOKEN is required" >&2
  exit 1
fi

curl --silent --show-error --fail \
  --max-time 10 \
  -H "Authorization: Bearer ${OPSCTL_API_TOKEN}" \
  "https://api.example.invalid/v1/hosts"
```

三例とも、タイムアウトを明示し、トークンを環境変数から読み、URLとトークンをログへそのまま出さない。

---

## 11.6 タイムアウトとリトライ

タイムアウトを指定しない呼び出しは、相手の応答が無いとき無期限に待ち続ける。
すべてのHTTP呼び出しにタイムアウトを設定する。

**指数バックオフ**は、リトライ間隔を試行のたびに指数関数的に伸ばす方式である。
輻輳している相手へ間隔を空けずに再送すると、状況を悪化させる。

```python
import time

import requests


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    timeout: float,
    max_retries: int,
) -> requests.Response:
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise
            backoff = min(2 ** attempt, 30)
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                return response
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2 ** attempt, 30)
            time.sleep(backoff)
            continue

        return response
```

リトライしてよいのは、通信断・タイムアウト・429・5xxに限る。
400番台の大半（`400`、`401`、`403`、`404`）は入力や認証の誤りであり、再送しても結果は変わらない。

---

## 11.7 ページネーション

**ページネーション**は、大量の結果を複数回のリクエストへ分割して取得する方式である。

カーソル方式の例:

```python
def iter_records(session, base_url, *, timeout, max_retries, page_size=100):
    cursor = None
    while True:
        params = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session, f"{base_url}/v1/hosts", timeout=timeout, max_retries=max_retries
        )
        payload = response.json()
        yield from payload.get("items", [])
        cursor = payload.get("next_cursor")
        if not cursor:
            return
```

オフセット方式のAPIでは、`offset` と `limit` を毎回進め、返却件数が `limit` 未満になった時点で終了する。
どちらの方式でも、上限件数や最大ページ数を設け、想定外に無限ループしないようにする。

---

## 11.8 レート制限対応

**レート制限**は、一定時間内に許可するリクエスト数をサーバー側が制限する仕組みである。
超過すると `429 Too Many Requests` が返り、`Retry-After` ヘッダーで再試行までの待機時間を示すAPIが多い。

```python
if response.status_code == 429:
    retry_after = response.headers.get("Retry-After")
    wait_seconds = float(retry_after) if retry_after else 10.0
    time.sleep(wait_seconds)
```

高頻度に呼ぶ処理では、事前にリクエスト間隔を空ける（クライアント側スロットリング）ことで、429の発生自体を減らせる。

---

## 11.9 TLS

APIホストは `https://` を使い、証明書検証を有効のまま呼び出す（第10章参照）。

```python
# 検証を無効化しない
requests.get("https://api.example.invalid/v1/hosts", timeout=10)

# 社内CAが必要な場合は証明書バンドルを指定する
requests.get(
    "https://api.example.invalid/v1/hosts",
    timeout=10,
    verify="/etc/ssl/certs/internal-ca-bundle.pem",
)
```

---

## 11.10 実務向け改善: opsctl api-exportサブコマンド

`samples/python/11_api_export.py` に、タイムアウト、リトライ、ページネーション、CSV出力をまとめたクライアントを置く。

```python
#!/usr/bin/env python3
"""ページ分割APIからホスト情報を取得し、CSVへ書き出す。

APIホストは example.invalid（実在しないドメイン）を既定にしている。
実際のAPIへ向ける場合は --base-url で上書きし、対象APIの利用規約と
レート制限を事前に確認すること。
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterator

import requests

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_TIMEOUT = 4

logger = logging.getLogger("api_export")

DEFAULT_BASE_URL = "https://api.example.invalid"
TOKEN_ENV_VAR = "OPSCTL_API_TOKEN"


class ApiError(RuntimeError):
    pass


def build_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    return session


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict[str, Any] | None,
    timeout: float,
    max_retries: int,
) -> requests.Response:
    attempt = 0
    while True:
        attempt += 1
        try:
            response = session.get(url, params=params, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout) as exc:
            if attempt > max_retries:
                raise ApiError(f"request failed after {attempt} attempts: {exc}") from exc
            backoff = min(2 ** attempt, 30)
            logger.warning(
                "request error (attempt %s/%s): %s; retrying in %ss",
                attempt, max_retries, exc, backoff,
            )
            time.sleep(backoff)
            continue

        if response.status_code == 429 or response.status_code >= 500:
            if attempt > max_retries:
                raise ApiError(
                    f"request failed with status {response.status_code} after {attempt} attempts"
                )
            retry_after = response.headers.get("Retry-After")
            backoff = float(retry_after) if retry_after else min(2 ** attempt, 30)
            logger.warning(
                "status=%s (attempt %s/%s); retrying in %ss",
                response.status_code, attempt, max_retries, backoff,
            )
            time.sleep(backoff)
            continue

        return response


def iter_records(
    session: requests.Session,
    base_url: str,
    *,
    timeout: float,
    max_retries: int,
    page_size: int = 100,
) -> Iterator[dict[str, Any]]:
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"limit": page_size}
        if cursor:
            params["cursor"] = cursor
        response = get_with_retry(
            session,
            f"{base_url}/v1/hosts",
            params=params,
            timeout=timeout,
            max_retries=max_retries,
        )
        if response.status_code != 200:
            raise ApiError(f"unexpected status {response.status_code}: {response.text[:200]}")
        payload = response.json()
        for record in payload.get("items", []):
            yield record
        cursor = payload.get("next_cursor")
        if not cursor:
            return


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["host", "status", "last_seen"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({key: record.get(key, "") for key in fieldnames})


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export host records from an API to CSV")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )

    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        logger.error("%s is required", TOKEN_ENV_VAR)
        return EXIT_USAGE

    if args.dry_run:
        logger.info("dry-run: would GET %s/v1/hosts and write %s", args.base_url, args.output)
        return EXIT_OK

    session = build_session(token)
    try:
        records = list(
            iter_records(
                session, args.base_url, timeout=args.timeout, max_retries=args.max_retries
            )
        )
    except ApiError as exc:
        logger.error("%s", exc)
        return EXIT_RUNTIME
    except requests.Timeout:
        logger.error("request timed out")
        return EXIT_TIMEOUT

    write_csv(args.output, records)
    logger.info("wrote %s records to %s", len(records), args.output)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

`--dry-run` を指定しても、`OPSCTL_API_TOKEN` の存在は確認する。
設定不備を早期に検知するためであり、実際のリクエストは送らない。

---

## 11.11 悪い例と問題点

```python
#!/usr/bin/env python3
import requests

def get_hosts(token, host_filter):
    url = f"https://api.example.invalid/v1/hosts?token={token}&filter={host_filter}"
    response = requests.get(url, verify=False)
    return response.json()
```

問題点:

- トークンをクエリ文字列に埋め込んでおり、アクセスログやブラウザ履歴に残る
- `verify=False` でTLS証明書検証を無効化している
- タイムアウトが無く、応答が無いと無期限に待つ
- ステータスコードを確認せず、失敗時も `response.json()` を呼んで例外の原因が分かりにくい
- リトライが無く、一時的な通信断で処理全体が落ちる

## 11.12 改善後のコード

```python
#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

import requests


def get_hosts(token: str, host_filter: str, *, timeout: float = 10.0) -> dict:
    response = requests.get(
        "https://api.example.invalid/v1/hosts",
        headers={"Authorization": f"Bearer {token}"},
        params={"filter": host_filter},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    token = os.environ.get("OPSCTL_API_TOKEN")
    if not token:
        print("OPSCTL_API_TOKEN is required", file=sys.stderr)
        return 1
    try:
        data = get_hosts(token, host_filter="web")
    except requests.HTTPError as exc:
        print(f"api error: {exc}", file=sys.stderr)
        return 2
    except requests.Timeout:
        print("request timed out", file=sys.stderr)
        return 4
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

改善点は、トークンをヘッダーへ移したこと、TLS検証を有効のままにしたこと、タイムアウトの明示、`raise_for_status` によるエラー分岐である。
リトライは11.6・11.10の `get_with_retry` を組み込むことで追加する。

---

## 11.13 セキュリティ上の注意点

- 秘密情報をURLのクエリ文字列に含めない。アクセスログやプロキシのログに残る
- TLS証明書検証を無効化しない（第10章）
- レスポンス本文をそのままログへ出さない。個人情報や内部識別子を含む場合がある（第9章）
- 想定外のフィールドを含むJSON応答をそのまま外部コマンドや別APIへ転送しない。必要なフィールドだけを取り出す
- APIキーやトークンには、必要な操作のみを許可する権限（読み取り専用など）を割り当てる

---

## 11.14 テスト方法

外部APIへ実際に接続せず、HTTP層をモックしてテストする。

```python
import pytest
import requests

from samples.python.api_export import ApiError, get_with_retry


class FakeResponse:
    def __init__(self, status_code: int, payload: dict, headers: dict | None = None) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}
        self.text = str(payload)

    def json(self) -> dict:
        return self._payload


class FakeSession:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self._responses = responses
        self.calls = 0

    def get(self, url, params=None, timeout=None):
        response = self._responses[self.calls]
        self.calls += 1
        return response


def test_get_with_retry_succeeds_after_500(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    session = FakeSession(
        [FakeResponse(500, {}), FakeResponse(200, {"items": []})]
    )
    response = get_with_retry(
        session, "https://api.example.invalid/v1/hosts", params=None, timeout=1, max_retries=3
    )
    assert response.status_code == 200
    assert session.calls == 2


def test_get_with_retry_raises_after_exhausting_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("time.sleep", lambda _seconds: None)
    session = FakeSession([FakeResponse(500, {}), FakeResponse(500, {})])
    with pytest.raises(ApiError):
        get_with_retry(
            session, "https://api.example.invalid/v1/hosts", params=None, timeout=1, max_retries=1
        )
```

PowerShellでは、`Invoke-RestMethod` をラップした関数を作り、Pesterの `Mock` で差し替える。

```powershell
Describe 'Get-WithRetry' {
    It 'retries on 500 and succeeds' {
        Mock Invoke-RestMethod { throw 'simulated 500' } -ParameterFilter { $script:CallCount -eq 0 }
        # 実運用のテストでは、モックの呼び出し回数に応じて戻り値を変える実装にする
    }
}
```

---

## 章末問題

### 問題1

`GET` と `POST` の冪等性の違いを、リトライしてよいかどうかの観点から説明せよ。

### 問題2

`429 Too Many Requests` を受け取ったとき、即座に同じ間隔でリトライすることの問題点を述べよ。

### 問題3

APIキーをクエリ文字列に含める設計の危険を、ログの観点から説明せよ。

### 問題4

カーソル方式のページネーションで、`next_cursor` の終了条件を確認しない実装が起こしうる問題を述べよ。

### 問題5

タイムアウトを設定しないHTTP呼び出しが、監視スクリプト全体に与える影響を述べよ。

---

## 解答と解説

### 問題1

`GET` は冪等なので安全にリトライできる。
`POST` は新規作成など副作用を伴うことが多く、無条件のリトライは二重作成を招く。
冪等性キーの付与など、追加の設計が要る。

### 問題2

サーバー側の輻輳を悪化させ、429が続く悪循環になる。
指数バックオフや `Retry-After` の尊重で間隔を空ける。

### 問題3

クエリ文字列はアクセスログやプロキシログに平文で残ることが多く、ログを読める人にトークンが漏れる。
ヘッダーでの送信に切り替える。

### 問題4

終了条件を誤ると無限ループになり、同じページを取得し続けるか、メモリを消費し続ける。
上限ページ数や最大件数を設ける。

### 問題5

相手の応答が無いとき、スクリプト全体が無期限に停止し、後続のホストやサブコマンドの処理が進まなくなる。
監視自体が機能しなくなる。

---

## 実装演習

### 演習A

`11_api_export.py` の `get_with_retry` に、最大待機時間の上限（例: 60秒）を設けるオプションを追加せよ。

### 演習B

Bashでcurlを使い、`429` を受け取った場合に `Retry-After` ヘッダーを読み取って待機するリトライ処理を実装せよ。

### 演習C

PowerShellで `Invoke-RestMethod` をラップし、タイムアウトとリトライを備えたページネーション取得関数を実装せよ。

---

## 次章予告

第12章では、設定ファイルとCLIツールを扱う。
設定とコードの分離、優先順位、サブコマンド設計を通じて、`opsctl` のCLI全体を組み立てる。


---


<!-- SOURCE: 12_config_and_cli.md -->

# 第12章 設定ファイルとCLIツール

## 学習目標

- 設定とコードを分離し、JSON/YAML/TOML/環境変数の使い分けを説明できる
- 引数、ヘルプ、サブコマンド、デフォルト値、優先順位を備えたCLIを設計できる
- 終了コード、dry-run、verbose、quietの一貫した扱いを実装できる
- 実行結果サマリーを出力し、`opsctl` のCLI設計へ接続できる

前提: 第1章（引数、終了コード）、第9章（ログ）、第10章（秘密情報）。

サンプルコードは学習用である。
本番のCLIでは、対象組織の運用ルール（承認フロー、変更管理番号の必須化など）に合わせて拡張すること。

---

## 12.1 基本概念

**設定とコードの分離**は、実行のたびに変わりうる値（閾値、対象ホスト、出力先）をコード本体から切り離し、外部ファイルや引数で与える設計である。

分離しないと、環境ごとにソースコードを書き換える運用になり、変更履歴とコードの変更履歴が混ざる。

`opsctl` は、コード（サブコマンドの実装）と設定（`config/opsctl.yaml`）を分離し、実行のたびに引数と環境変数で上書きできる構成にする。

---

## 12.2 設定形式の比較

| 形式 | 長所 | 短所 | 向く用途 |
|------|------|------|----------|
| JSON | 言語間で扱いやすい。パーサーが標準的 | コメントが書けない | API連携、機械生成の設定 |
| YAML | 人が読み書きしやすい。コメント可 | インデント依存、暗黙型変換の罠がある（第3章） | 人が編集する運用設定 |
| TOML | 型が明確。セクション構造が読みやすい | Bash/PowerShellでの標準サポートが薄い | Python中心のツール設定（`pyproject.toml`など） |
| 環境変数 | 秘密情報や実行環境ごとの値に向く | 構造化データには不向き。一覧性が低い | 秘密情報、実行環境の切り替えフラグ |

`opsctl` は、階層的な既定値をYAML、秘密情報を環境変数、単発の上書きをCLI引数に割り当てる。

---

## 12.3 優先順位

複数の設定源がある場合、値が競合したときの優先順位を先に決める。
`opsctl` は次の順で解決する（上ほど優先度が高い）。

1. コマンドライン引数
2. 環境変数
3. 設定ファイル（`config/opsctl.yaml`）
4. コード内蔵のデフォルト値

```python
def resolve_timeout(cli_value: int | None, config: dict) -> int:
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get("OPSCTL_TIMEOUT_SECONDS")
    if env_value:
        return int(env_value)
    configured = config.get("defaults", {}).get("timeout_seconds")
    if configured is not None:
        return int(configured)
    return DEFAULT_TIMEOUT_SECONDS
```

優先順位を決めていないと、「設定ファイルを直したのに反映されない」という調査に時間を取られる。
CLIのヘルプや `--verbose` ログに、実際に採用した値の出所を残すと調査が速くなる。

---

## 12.4 最小構成のCLI

Python（`argparse`）:

```python
#!/usr/bin/env python3
import argparse
import sys


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal CLI example")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    print(f"timeout={args.timeout} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Bash（`getopts` は長いオプションを扱いにくいため、第1章と同じ手書きパーサーを使う）:

```bash
#!/usr/bin/env bash
set -euo pipefail

timeout=30
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timeout) timeout="${2:-}"; shift 2 ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help)
      echo "Usage: $0 [--timeout SECONDS] [--dry-run]" >&2
      exit 0
      ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

echo "timeout=${timeout} dry_run=${dry_run}"
```

PowerShell（`param()` は標準でヘルプと型検証を持つ）:

```powershell
#!/usr/bin/env pwsh
param(
    [int]$Timeout = 30,
    [switch]$DryRun
)

Write-Output "timeout=$Timeout dry_run=$($DryRun.IsPresent)"
```

---

## 12.5 サブコマンド設計

**サブコマンド**は、1つのCLIの中に複数の操作を持たせ、`ツール名 サブコマンド名 [オプション]` の形で呼び出す構成である。

Python（`argparse` のサブパーサー）:

```python
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opsctl")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    ping_parser = subparsers.add_parser("ping-check", help="check connectivity to hosts")
    ping_parser.add_argument("--hosts-file", type=Path, default=None)

    subparsers.add_parser("disk-check", help="check disk usage thresholds")
    return parser
```

サブコマンドごとに固有のオプションを持たせつつ、`--config`、`--dry-run`、`--verbose`、`--quiet` のような共通オプションは親パーサーに置く。

---

## 12.6 ヘルプとデフォルト値の提示

利用者が `--help` を見ただけで既定値を判断できるように、ヘルプ文字列へデフォルト値を含める。

```python
parser.add_argument(
    "--timeout",
    type=int,
    default=30,
    help="request timeout in seconds (default: 30)",
)
```

Bashでは、`usage()` 関数に既定値を明記する。

```bash
usage() {
  cat <<'EOF' >&2
Usage: opsctl.sh ping-check [--timeout SECONDS] [--dry-run]
  --timeout SECONDS   default: 30
  --dry-run           show planned actions without making changes
EOF
}
```

---

## 12.7 dry-run、verbose、quietの実装

三つの共通オプションは、`opsctl` の全サブコマンドで意味を統一する。

| オプション | 効果 |
|------------|------|
| `--dry-run` | 変更を伴う操作を実行せず、実行予定だけをログとサマリーに出す |
| `--verbose` | DEBUGレベルまでログを出す（第9章） |
| `--quiet` | WARNING以上のみ出す |

```python
if args.verbose and args.quiet:
    parser.error("--verbose and --quiet are mutually exclusive")
```

`--dry-run` は、読み取り専用の処理では実質的に通常実行と同じ結果になってよい。
書き込み・削除・外部への変更APIを呼ぶ処理では、必ず実行前に分岐させる。

```python
if args.dry_run:
    logger.info("dry-run: would delete %s", target_path)
else:
    target_path.unlink()
```

---

## 12.8 終了コードと実行結果サマリー

`opsctl` 共通の終了コード（README参照）を、CLIスケルトンでも一貫して使う。

| コード | 意味 |
|--------|------|
| 0 | 成功（警告なし） |
| 1 | 使い方誤り、設定誤り |
| 2 | 実行時エラー（一部失敗を含む） |
| 3 | 閾値超過などのCRITICAL |
| 4 | タイムアウト |
| 130 | ユーザーによる中断 |

**実行結果サマリー**は、対象件数・成功件数・警告件数・失敗件数を1行にまとめた出力である。
終了コードだけでは「何件中何件失敗したか」が分からないため、ログの最後に必ず出す。

```python
@dataclass
class RunSummary:
    subcommand: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    failed: int = 0

    def exit_code(self) -> int:
        if self.critical:
            return EXIT_CRITICAL
        if self.failed:
            return EXIT_RUNTIME
        return EXIT_OK

    def render(self) -> str:
        return (
            f"summary subcommand={self.subcommand} total={self.total} "
            f"ok={self.ok} warning={self.warning} critical={self.critical} failed={self.failed}"
        )
```

---

## 12.9 実務向け改善: opsctl CLIスケルトン

`samples/python/12_opsctl_cli.py` に、設定読み込み、優先順位解決、サブコマンド、dry-run、サマリー出力をまとめたスケルトンを置く。

```python
#!/usr/bin/env python3
"""opsctlのCLIスケルトン: 設定優先順位、サブコマンド、dry-run、サマリー出力。

ping-check と disk-check は説明用の簡略実装であり、実際の疎通確認や
ディスク使用率取得は第15章で実装する。
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3
EXIT_TIMEOUT = 4

logger = logging.getLogger("opsctl")

DEFAULT_CONFIG_PATH = Path("config/opsctl.yaml")
DEFAULT_TIMEOUT_SECONDS = 30


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML is required to read config files (pip install PyYAML)")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping: {path}")
    return data


def resolve_timeout(cli_value: int | None, config: dict[str, Any]) -> int:
    """CLI引数 > 環境変数 > 設定ファイル > デフォルトの順で解決する。"""
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get("OPSCTL_TIMEOUT_SECONDS")
    if env_value:
        return int(env_value)
    configured = config.get("defaults", {}).get("timeout_seconds")
    if configured is not None:
        return int(configured)
    return DEFAULT_TIMEOUT_SECONDS


@dataclass
class RunSummary:
    subcommand: str
    total: int = 0
    ok: int = 0
    warning: int = 0
    critical: int = 0
    failed: int = 0

    def exit_code(self) -> int:
        if self.critical:
            return EXIT_CRITICAL
        if self.failed:
            return EXIT_RUNTIME
        return EXIT_OK

    def render(self) -> str:
        return (
            f"summary subcommand={self.subcommand} total={self.total} "
            f"ok={self.ok} warning={self.warning} critical={self.critical} failed={self.failed}"
        )


def configure_logging(*, verbose: bool, quiet: bool) -> None:
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)


def run_ping_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    timeout = resolve_timeout(args.timeout, config)
    hosts_file = args.hosts_file or Path(config.get("paths", {}).get("hosts_file", "config/hosts.txt"))
    summary = RunSummary(subcommand="ping-check")

    if not hosts_file.is_file():
        logger.error("hosts file not found: %s", hosts_file)
        summary.failed = 1
        return summary

    hosts = [
        line.strip()
        for line in hosts_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    summary.total = len(hosts)

    for host in hosts:
        if args.dry_run:
            logger.info("dry-run: would ping host=%s timeout=%s", host, timeout)
        else:
            logger.info("checked host=%s timeout=%s", host, timeout)
        summary.ok += 1

    return summary


def run_disk_check(args: argparse.Namespace, config: dict[str, Any]) -> RunSummary:
    warn_percent = config.get("defaults", {}).get("disk_warn_percent", 80)
    crit_percent = config.get("defaults", {}).get("disk_crit_percent", 90)
    summary = RunSummary(subcommand="disk-check")
    summary.total = 1

    if args.dry_run:
        logger.info("dry-run: would check disk usage warn=%s crit=%s", warn_percent, crit_percent)
    else:
        logger.info("disk usage checked warn=%s crit=%s", warn_percent, crit_percent)
    summary.ok = 1
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opsctl", description="Operations control CLI (teaching skeleton)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--dry-run", action="store_true", help="show planned actions without making changes")
    parser.add_argument("--verbose", action="store_true", help="enable DEBUG logging")
    parser.add_argument("--quiet", action="store_true", help="only show WARNING and above")
    parser.add_argument("--timeout", type=int, default=None, help="override timeout in seconds")

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    ping_parser = subparsers.add_parser("ping-check", help="check connectivity to hosts")
    ping_parser.add_argument("--hosts-file", type=Path, default=None)

    subparsers.add_parser("disk-check", help="check disk usage thresholds")

    return parser


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet are mutually exclusive")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    configure_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        config = load_config(args.config)
    except (OSError, ValueError, RuntimeError) as exc:
        logger.error("failed to load config %s: %s", args.config, exc)
        return EXIT_USAGE

    if args.subcommand == "ping-check":
        summary = run_ping_check(args, config)
    elif args.subcommand == "disk-check":
        summary = run_disk_check(args, config)
    else:  # pragma: no cover
        logger.error("unknown subcommand: %s", args.subcommand)
        return EXIT_USAGE

    print(summary.render(), file=sys.stderr)
    if not args.quiet:
        print(json.dumps(summary.__dict__))
    return summary.exit_code()


if __name__ == "__main__":
    sys.exit(main())
```

実行例:

```bash
python3 samples/python/12_opsctl_cli.py --config config/opsctl.yaml --dry-run ping-check --hosts-file config/hosts.txt
# stderr: ... summary subcommand=ping-check total=3 ok=3 warning=0 critical=0 failed=0
# stdout: {"subcommand": "ping-check", "total": 3, "ok": 3, "warning": 0, "critical": 0, "failed": 0}
# exit code: 0

python3 samples/python/12_opsctl_cli.py disk-check --config config/does_not_exist.yaml
# config/does_not_exist.yaml が無い場合は空設定として扱われ、デフォルト値で実行する
```

---

## 12.10 悪い例と問題点

```python
#!/usr/bin/env python3
import sys

# 設定値がコードに直書きされている
TIMEOUT = 30
HOSTS = ["web01.example.invalid", "web02.example.invalid"]

action = sys.argv[1] if len(sys.argv) > 1 else "ping"

if action == "ping":
    for h in HOSTS:
        print(f"pinging {h} with timeout {TIMEOUT}")
elif action == "disk":
    print("checking disk")
else:
    print("unknown action")
    # 終了コードを返さず、そのまま正常終了してしまう
```

問題点:

- ホスト一覧と閾値がコードに直書きされ、環境ごとにソースを書き換える運用になる
- サブコマンドが `if/elif` の連鎖で、ヘルプや型検証、必須引数チェックが無い
- 不明な操作でもメッセージを出すだけで終了コード0のまま終わり、CIや監視が失敗を検知できない
- `--dry-run`、`--verbose`、`--quiet` に相当する仕組みが無い

---

## 12.11 改善後のコード

12.9の `12_opsctl_cli.py` が改善後にあたる。
設定分離、`argparse` によるサブコマンドとヘルプ、優先順位解決、dry-run、終了コードとサマリーのすべてを満たす。

Bashで同等の骨格を作る場合は、サブコマンドをcase文で分岐し、共通オプションを親スクリプトで解析してから個別関数へ渡す。

```bash
#!/usr/bin/env bash
set -euo pipefail

dry_run=0
verbose=0
quiet=0
subcommand="${1:-}"
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) dry_run=1; shift ;;
    --verbose) verbose=1; shift ;;
    --quiet) quiet=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

case "${subcommand}" in
  ping-check)
    echo "dry_run=${dry_run} verbose=${verbose} quiet=${quiet}: running ping-check" >&2
    ;;
  disk-check)
    echo "dry_run=${dry_run} verbose=${verbose} quiet=${quiet}: running disk-check" >&2
    ;;
  "")
    echo "subcommand is required" >&2
    exit 1
    ;;
  *)
    echo "unknown subcommand: ${subcommand}" >&2
    exit 1
    ;;
esac
```

---

## 12.12 セキュリティ上の注意点

- 設定ファイルに秘密情報を書かない。`config/opsctl.yaml` のコメントにあるとおり、トークンは環境変数から読む（第10章）
- 設定ファイルのパーミッションを絞る。他ユーザーに読み取り可能な設定ファイルへ、将来誰かが誤って秘密情報を書き足すリスクを減らす
- `--verbose` で解決済みの設定値をログに出す際、秘密情報に該当するキーは値をマスキングする（第9章）
- YAML読み込みは `yaml.safe_load` を使う（第3章）。任意コード実行につながる `yaml.load` を使わない

---

## 12.13 テスト方法

```python
import pytest
from pathlib import Path

from samples.python.opsctl_cli import main, resolve_timeout


def test_resolve_timeout_prefers_cli_value() -> None:
    assert resolve_timeout(15, {"defaults": {"timeout_seconds": 30}}) == 15


def test_resolve_timeout_falls_back_to_config() -> None:
    assert resolve_timeout(None, {"defaults": {"timeout_seconds": 45}}) == 45


def test_resolve_timeout_env_overrides_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPSCTL_TIMEOUT_SECONDS", "20")
    assert resolve_timeout(None, {"defaults": {"timeout_seconds": 45}}) == 20


def test_main_ping_check_dry_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    hosts_file = tmp_path / "hosts.txt"
    hosts_file.write_text("a.example.invalid\nb.example.invalid\n", encoding="utf-8")
    exit_code = main(
        ["--dry-run", "--quiet", "ping-check", "--hosts-file", str(hosts_file)]
    )
    assert exit_code == 0


def test_main_rejects_verbose_and_quiet_together() -> None:
    with pytest.raises(SystemExit):
        main(["--verbose", "--quiet", "disk-check"])
```

---

## 章末問題

### 問題1

設定とコードを分離すべき理由を、環境差分の管理という観点から説明せよ。

### 問題2

`opsctl` の設定優先順位（CLI引数 > 環境変数 > 設定ファイル > デフォルト）を採用する利点を一つ述べよ。

### 問題3

`--dry-run` を、読み取り専用の処理と書き込みを伴う処理で同じように実装してよいか、理由とともに述べよ。

### 問題4

終了コードだけでなく実行結果サマリーを出力すべき理由を述べよ。

### 問題5

`--verbose` と `--quiet` を同時に指定できてしまう設計の問題点を述べよ。

---

## 解答と解説

### 問題1

環境ごとにコードを書き換えると、コードの変更履歴に環境固有の差分が混ざり、レビューとロールバックが難しくなる。
設定を分離すれば、コードは環境に依存せず一つに保てる。

### 問題2

その場限りの調整（CLI引数）を最優先にしつつ、通常運用は設定ファイルで管理でき、秘密情報や環境固有値は環境変数で分離できる。
優先順位が明確だと、値の出所を追跡しやすい。

### 問題3

読み取り専用の処理では通常実行と同じ結果でよい場合が多い。
書き込み・削除・外部への変更APIを伴う処理では、必ず分岐し、実際の変更を止める実装が必要である。

### 問題4

終了コードは成否の大枠しか示さない。
対象件数・成功件数・失敗件数が分からないと、部分的な失敗の規模を把握できない。

### 問題5

出力レベルの意図が矛盾し、どちらが優先されるか実装依存になる。
利用者の意図を確認できないため、引数解析の時点でエラーにするべきである。

---

## 実装演習

### 演習A

`12_opsctl_cli.py` に `log-search` サブコマンドを追加せよ。
オプションは `--pattern`（必須）と `--log-dir`（既定値は設定ファイルの `paths.report_dir`）とする。

### 演習B

Bashで、`--config` オプションからYAMLファイルのパスを受け取り、`yq` があれば使い、無ければ「PyYAMLで代替する」旨をエラーメッセージに含めて終了コード1にするスクリプトを書け。

### 演習C

`resolve_timeout` と同じ優先順位の考え方で、`disk_warn_percent` を解決する関数を実装し、CLI引数・環境変数・設定ファイル・デフォルトそれぞれのテストを書け。

---

## 次章予告

第13章では、テストと品質管理を扱う。
ユニットテストと結合テスト、境界値、モック、静的解析、CIへの組み込みを通じて、ここまでのサンプルを検証可能にする。


---


<!-- SOURCE: 13_testing_and_quality.md -->

# 第13章 テストと品質管理

## 学習目標

- テストの目的を説明し、ユニットテストと結合テストを使い分けられる
- 正常系・異常系・境界値の観点で、テストケースを漏れなく設計できる
- モックを使い、外部依存（ネットワーク、外部コマンド、時間）を切り離してテストできる
- pytest、Pester、Bashそれぞれでテストを書き、実行できる
- 型ヒント、lint、フォーマッターを使い、実行前に問題を検出できる
- コードレビューの観点を説明し、CIにテストと静的解析を組み込める

前提: 第1章（終了コード）、第7章（外部コマンド実行）、第8章（例外処理）、第12章（CLI設計）。

サンプルコードは学習用である。
本番のCIパイプラインやカバレッジ目標は、対象チームの品質基準に合わせて調整すること。

---

## 13.1 基本概念

**テスト**は、コードが期待どおりに動くことを、実行して確認する作業である。

インフラ運用スクリプトは、次の理由で特にテストの価値が高い。

- 対象が本番サーバーやネットワーク機器であり、誤動作の影響が大きい
- 削除、上書き、再起動のような破壊的操作を含むことが多く、手動確認だけでは危険が残る
- 定期実行や自動化の一部に組み込まれ、人が毎回結果を見るとは限らない
- 一度書いたら長く使われがちで、書いた本人以外が後から手を入れる

テストが無いコードを変更すると、次のいずれかになりやすい。

1. 変更のたびに手動で全パターンを再確認する（時間がかかり、確認漏れが起きる）
2. 確認を省略して変更を入れる（退行、いわゆるデグレを見逃す）

自動テストは、この二択を避け、変更のたびに機械的に同じ確認を再実行する手段である。

テストには、大きく分けて次の目的がある。

| 目的 | 説明 |
|------|------|
| 正しさの確認 | 実装した処理が仕様どおりに動くことを確認する |
| 退行の防止 | 既存の挙動を壊していないことを、変更のたびに確認する |
| 仕様の明文化 | テストコード自体が「この関数はこう動くべき」という仕様書になる |
| 設計の検証 | テストしにくいコードは、責務が混ざっているサインであることが多い（第5章、第14章） |
| 安心して変更する土台 | リファクタリング（第14章）を、挙動を変えずに進められる根拠になる |

---

## 13.2 ユニットテストと結合テスト

**ユニットテスト**は、関数やクラスなど、コードの最小単位を対象に、他の部分から切り離して検証するテストである。

**結合テスト**は、複数の部品を組み合わせた状態で、部品間の連携を含めて検証するテストである。

| 観点 | ユニットテスト | 結合テスト |
|------|-----------------|-------------|
| 対象範囲 | 1つの関数・クラス | 複数の関数・モジュール・外部システムとの連携 |
| 実行速度 | 速い（ミリ秒単位） | 遅くなりやすい（I/Oを含むため） |
| 外部依存 | モックで切り離すことが多い | 一部、または全部を実物に近い形で使う |
| 見つけやすい不具合 | ロジックの誤り、境界値の誤り | インターフェースの不一致、設定ミス、環境差異 |
| 失敗時の特定しやすさ | 高い（対象が狭い） | 低くなりやすい（原因箇所の絞り込みが必要） |

`opsctl` の `disk-check` 相当の機能を例にすると、次のように対応する。

| テスト対象 | 分類 |
|------------|------|
| `classify_disk_usage`（閾値判定だけ） | ユニットテスト |
| `parse_df_output`（テキスト解析だけ） | ユニットテスト |
| `fetch_disk_report`（外部コマンド呼び出し + パース） | 結合テスト（外部コマンドはモックすることが多い） |
| CLI全体（引数解析 + 収集 + 分類 + 出力） | 結合テスト |

両方が必要である。
ユニットテストだけでは、部品同士の繋ぎ込みの誤りを見逃す。
結合テストだけでは、実行が遅く、失敗時にどの部品が原因か特定しにくい。
一般に、ユニットテストを土台に多く持ち、結合テストで主要な経路を絞って確認する構成にする。

---

## 13.3 正常系・異常系・境界値

テストケースを考えるときは、次の3つの観点で漏れを確認する。

| 観点 | 意味 | 例（ディスク使用率の分類） |
|------|------|------------------------------|
| 正常系 | 想定どおりの入力で、期待どおりの結果になることを確認する | 使用率50%で`ok`になる |
| 異常系 | 不正な入力やエラー状態で、適切にエラー処理されることを確認する | 使用率が101%のとき例外を送出する |
| 境界値 | 判定が切り替わる値のちょうど上下を確認する | 使用率が閾値と同じ80%のとき`warning`になるか |

**境界値**を狙ったテストは特に重要である。
「80%を超えたら警告」なのか「80%以上で警告」なのかは、実装によって揺れやすく、
`>` と `>=` の取り違え（いわゆるoff-by-oneエラー）は典型的なバグの温床である。

境界値のテストは、次の3点をセットで確認するとよい。

1. 閾値のすぐ下（例: 79%） → 変化する前の状態
2. 閾値ちょうど（例: 80%） → 仕様上どちらに転ぶかを明確にする値
3. 閾値のすぐ上（例: 81%） → 変化した後の状態

さらに、値の取りうる範囲の両端（最小値、最大値、0、空文字列、空リストなど）も境界値の一種である。

| 種類 | 例 |
|------|-----|
| 数値の下限・上限 | 0%、100%、負の値 |
| 文字列の空 | 空文字列、空白のみの文字列 |
| コレクションの空・単数・複数 | 空リスト、要素1件、要素多数 |
| 個数の限界 | 上限ちょうどの件数、上限+1件 |

---

## 13.4 テストデータとフィクスチャ

**テストデータ**は、テストの入力として使う、あらかじめ用意した値である。

**フィクスチャ**は、テストの実行前に用意し、実行後に片付ける、テストに必要な準備一式（データ、リソース、モック）を指す。
pytestでは `@pytest.fixture` で定義した関数や、`tmp_path`・`capsys`・`monkeypatch` のような組み込みフィクスチャを使う。

テストデータを選ぶときの方針:

- 本物のホスト名やIPアドレスを使わない。第1章以降のサンプルと同様に `example.invalid` のような予約ドメインを使う
- ランダムなテストデータは再現性を損なう。失敗したときに同じ入力で再実行できることを優先し、固定値を使う
- 境界値・異常系を明示的にカバーする値を用意する。「たまたま通った」ではなく「この値を狙って確認した」と分かる名前や配置にする
- 大きすぎるテストデータは避ける。読む人が意図を追えるサイズに留める

```python
# 固定のテストデータ（df -P 相当の出力）。
# ホスト名やパスは実在しない値（.invalid）を使う。
SAMPLE_DF_OUTPUT = """Filesystem     1024-blocks     Used Available Capacity Mounted on
/dev/sda1         51475068 42787876   6045808      88% /
/dev/sda2        104845292 34567890  65432100      35% /var
/dev/sda3         20971520 19951616    524288      98% /data
"""
```

pytestの組み込みフィクスチャのうち、運用スクリプトのテストで頻繁に使うものを挙げる。

| フィクスチャ | 用途 |
|--------------|------|
| `tmp_path` | テスト専用の一時ディレクトリを提供する。実ファイルへの副作用を避ける |
| `capsys` | 標準出力・標準エラーをキャプチャする。CLIの出力検証に使う |
| `monkeypatch` | 環境変数、属性、関数を一時的に差し替える。テスト終了時に自動で元に戻る |
| `caplog` | ログ出力をキャプチャする。第9章のログ検証に使う |

`tmp_path` を使うと、テストごとに独立したディレクトリが払い出されるため、
複数のテストが同じ固定パス（例: `/tmp/report.txt`）を取り合って干渉する事故を防げる。

---

## 13.5 モック

**モック**は、テスト対象が依存する外部の部品を、制御可能な偽物に置き換える技法である。

モックを使う代表的な対象:

| 対象 | 理由 |
|------|------|
| ネットワーク呼び出し（`requests`、`Invoke-RestMethod`など） | 実際のAPIを毎回叩くと遅く、不安定で、相手側への負荷にもなる |
| 外部コマンド実行（`subprocess.run`、`ssh`など） | 対象ホストが無くてもロジックを検証したい |
| 時間（`time.sleep`、現在時刻） | 待機時間や日付依存の分岐を、実時間を待たずに検証したい（第8章のリトライテスト） |
| ファイルシステム | 実ファイルを汚さずに、様々な入力パターンを試したい（`tmp_path`で代替できる場合はそちらを優先する） |

Pythonでは、`unittest.mock` と、pytestの `monkeypatch` フィクスチャの両方が使える。
`monkeypatch` は、テスト終了時に自動で元の状態へ戻すため、後始末を書き忘れるリスクが低く、本書では基本的にこちらを使う。

```python
import subprocess

import pytest


def run_uptime() -> str:
    completed = subprocess.run(["uptime"], capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def test_run_uptime_returns_stdout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, returncode=0, stdout="up 3 days\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert run_uptime() == "up 3 days"
```

モックを使う際の注意点:

- **モックしすぎない**。全部をモックすると、テストは通っても実際の結合部分の不具合を見逃す。外部I/Oの境界線だけをモックし、自前のロジックは実物のまま通す
- **モック対象のインターフェースを正しく再現する**。実物と異なる形の偽物を作ると、テストは通るのに本番で壊れる「偽陽性」が起きる
- **依存性注入で置き換えられる場合は、それを優先する**。13.15節で示すように、外部依存を引数として受け取る設計にしておくと、モジュールの内部をパッチ（monkeypatch）せずにテストできる

---

## 13.6 pytestの基本

**pytest**は、Pythonの標準的なテストフレームワークである。
`assert` 文だけでテストを書け、実行結果を分かりやすく表示する。

規約:

- テストファイル名は `test_*.py` または `*_test.py`
- テスト関数名は `test_` で始める
- 各テストは `assert` で期待値を検証する。専用のアサーションメソッドは不要

```python
def add(a: int, b: int) -> int:
    return a + b


def test_add_returns_sum_of_two_numbers() -> None:
    assert add(2, 3) == 5


def test_add_handles_negative_numbers() -> None:
    assert add(-1, 1) == 0
```

実行:

```bash
pytest                       # カレントディレクトリ以下のテストをすべて実行
pytest tests/test_foo.py     # 特定のファイルだけ実行
pytest -k "boundary"         # 名前に"boundary"を含むテストだけ実行
pytest -v                    # テストごとの結果を詳細表示
pytest -x                    # 最初の失敗で打ち切る
pytest --maxfail=3           # 3件失敗したら打ち切る
```

**パラメトライズ**（`@pytest.mark.parametrize`）を使うと、同じ検証ロジックを複数の入力値に対して繰り返せる。
境界値テスト（13.3節）と特に相性がよい。

```python
import pytest


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (79, "ok"),
        (80, "warning"),
        (89, "warning"),
        (90, "critical"),
    ],
)
def test_classify_boundaries(value: int, expected: str) -> None:
    assert classify_disk_usage(value, warn_percent=80, crit_percent=90) == expected
```

異常系は `pytest.raises` で、送出される例外の型（と必要ならメッセージ）を検証する。

```python
import pytest


def test_classify_rejects_inverted_thresholds() -> None:
    with pytest.raises(InvalidThresholdError):
        classify_disk_usage(85, warn_percent=90, crit_percent=80)
```

設定は `pyproject.toml` に置ける。

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
```

---

## 13.7 最小構成のコード

テスト対象とテストの最小構成を示す。

```python
"""minimal_example.py: テスト対象の最小関数。"""
from __future__ import annotations


def is_valid_percent(value: float) -> bool:
    """0以上100以下ならTrueを返す。"""
    return 0 <= value <= 100
```

```python
"""test_minimal_example.py: 最小構成のテスト。"""
from minimal_example import is_valid_percent


def test_is_valid_percent_true_for_normal_value() -> None:
    assert is_valid_percent(50) is True


def test_is_valid_percent_false_for_negative_value() -> None:
    assert is_valid_percent(-1) is False


def test_is_valid_percent_true_at_lower_bound() -> None:
    assert is_valid_percent(0) is True


def test_is_valid_percent_true_at_upper_bound() -> None:
    assert is_valid_percent(100) is True
```

`pytest` をこのディレクトリで実行すると、4件のテストがすべて成功する。
関数を1つ、テストを4つ（正常系1、異常系1、境界値2）というバランスが、最小構成として分かりやすい。

---

## 13.8 型ヒントと静的解析

**型ヒント**は、変数や関数の引数・戻り値が、どの型を想定しているかをコードに明示する記法である。
Python自体は実行時に型ヒントを強制しないが、`mypy` のような**静的解析**ツールで、実行前に型の矛盾を検出できる。

```python
def classify_disk_usage(used_percent: float, warn_percent: float, crit_percent: float) -> str:
    ...
```

型ヒントが無いと、次のような誤りが実行するまで分からない。

```python
def bad_example(value):
    return value.strip()  # 呼び出し側が数値を渡すと、実行時まで気づけない
```

型ヒントを付けても、静的解析を実行しなければ検出できない。
mypyを実行する。

```bash
mypy --strict samples/python/13_disk_classifier.py
```

実行結果の例:

```text
Success: no issues found in 1 source file
```

`--strict` は、型ヒントの省略や `Any` への暗黙の依存を厳しく検出するモードである。
新規コードでは `--strict` から始め、既存コードへ段階的に導入する場合は緩いモードから始めて徐々に厳しくする。

設定は `pyproject.toml` にまとめられる。

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_ignores = true
```

型ヒントの効果:

- 呼び出し側の引数の型誤りを、実行前に検出できる
- IDEの補完とリファクタリング支援が効きやすくなる
- 関数のシグネチャ自体が、簡潔なドキュメントになる（第14章のドキュメントの節でも扱う）

---

## 13.9 lintとフォーマッター

**lint（静的解析）**は、コードを実行せずに、構文誤り・未使用変数・危険なパターンなどを検出する仕組みである。
**フォーマッター**は、インデントや空白、改行位置などのスタイルを、ツールで自動的に統一する仕組みである。

| 言語 | lint | フォーマッター |
|------|------|-----------------|
| Python | ruff（旧: flake8 + pylint相当） | ruff format（black相当） |
| Bash | shellcheck | shfmt |
| PowerShell | PSScriptAnalyzer | PowerShellの組み込み整形 |

Python（ruff）:

```bash
ruff check samples/python/13_disk_classifier.py
```

実行結果の例:

```text
All checks passed!
```

フォーマットを揃える:

```bash
ruff format samples/python/13_disk_classifier.py
```

Bash（shellcheck）:

```bash
shellcheck samples/bash/13_classify_disk.sh
```

shellcheckは、クォート漏れ（第7章のシェルインジェクションにも関わる）、未使用変数、
`[ ]` と `[[ ]]` の違いによる罠などを検出する。

PowerShell（PSScriptAnalyzer）:

```powershell
Install-Module -Name PSScriptAnalyzer -Scope CurrentUser -Force
Invoke-ScriptAnalyzer -Path samples/powershell/13_classify_disk.ps1
```

lintとフォーマッターを使う利点:

- レビューで「スペースが1つ多い」のようなスタイルの指摘をせずに済み、レビュー時間をロジックに集中できる
- 危険なパターン（未クォートの変数展開、broad except、`eval` の使用など）を、実行前に機械的に検出できる
- チーム内でスタイルの好みによる議論を減らせる（フォーマッターの設定がルールそのものになる）

> **警告**: lintとフォーマッターは、コードの意図や仕様の正しさまでは保証しない。
> 「lintが通った」は「正しく動く」の代わりにならない。テストと組み合わせて使う。

---

## 13.10 Bashのテスト

Bashには、pytestやPesterに相当する標準的なテストフレームワークが無い。
本書では、次の方針で手書きのテストを書く。

1. テスト対象のスクリプトを `source` して、関数だけを読み込む
2. `set -euo pipefail` の効果でテストスクリプト自体が途中終了しないよう、失敗を想定する箇所は `set +e` / `set -e` で切り替える
3. 期待値と実際の値を比較し、一致しなければメッセージを出して失敗を記録する
4. 最後に失敗件数を集計し、1件でもあれば終了コード1で終わる

```bash
#!/usr/bin/env bash
set -euo pipefail

source ./samples/bash/13_classify_disk.sh

failures=0

assert_eq() {
  local expected="$1"
  local actual="$2"
  local message="$3"
  if [[ "${expected}" != "${actual}" ]]; then
    echo "FAIL: ${message}: expected=${expected} actual=${actual}" >&2
    failures=$(( failures + 1 ))
  else
    echo "ok: ${message}"
  fi
}

assert_eq "ok" "$(classify_disk_usage 50 80 90)" "50% is ok"
assert_eq "warning" "$(classify_disk_usage 80 80 90)" "80% (=warn) is warning"
assert_eq "critical" "$(classify_disk_usage 90 80 90)" "90% (=crit) is critical"

if [[ "${failures}" -gt 0 ]]; then
  echo "FAILED: ${failures} assertion(s) failed" >&2
  exit 1
fi
echo "all assertions passed"
```

`source` されたときに `main` が自動実行されないよう、対象スクリプト側で次のガードを入れておく。

```bash
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

これが無いと、`source` した瞬間に本処理が実行され、テストのための読み込みのつもりが実際に処理を走らせてしまう。

より本格的なBashテストが必要な場合は、`bats-core`（Bash Automated Testing System）のような外部フレームワークの導入も選択肢になる。
本書では、追加のインストールを前提にしない手書き方式を基本とする。

---

## 13.11 Pesterの基本

**Pester**は、PowerShell用のテストフレームワークである。
`Describe`/`It`/`Should` を使い、pytestに近い書き味でテストを書ける。

導入（README参照）:

```powershell
Install-Module -Name Pester -MinimumVersion 5.5 -Scope CurrentUser -Force
```

基本構造:

```powershell
Describe 'Get-DiskStatus' {
    It 'returns ok for usage below warn threshold' {
        Get-DiskStatus -UsedPercent 50 -WarnPercent 80 -CritPercent 90 | Should -Be 'ok'
    }

    It 'throws when warn threshold exceeds crit threshold' {
        { Get-DiskStatus -UsedPercent 85 -WarnPercent 90 -CritPercent 80 } | Should -Throw
    }
}
```

`BeforeAll` でテスト対象をドットソースし、`Mock` で関数を差し替える。

```powershell
BeforeAll {
    . "$PSScriptRoot/../samples/powershell/13_classify_disk.ps1"
}

Describe 'Invoke-Main' {
    It 'returns exit code 3 when a mocked disk is critical' {
        Mock Get-LocalDiskUsage {
            @([pscustomobject]@{ MountPoint = 'C:'; UsedPercent = 95 })
        }
        Invoke-Main -WarnPercent 80 -CritPercent 90 | Should -Be 3
    }
}
```

`Mock` は、`Describe`/`It` のスコープ内で、指定した名前のコマンドやカスタム関数の呼び出しを横取りする。
実機のディスク構成に依存せず、`Get-LocalDiskUsage` が返す値を自由に設定してテストできる。

実行:

```powershell
Invoke-Pester ./tests/13_classify_disk.Tests.ps1 -Output Detailed
```

---

## 13.12 コードレビュー

**コードレビュー**は、変更を取り込む前に、書いた本人以外が内容を確認するプロセスである。

チェックすべき観点は、これまでの章の内容と対応している。

| 観点 | 確認内容 | 関連章 |
|------|----------|--------|
| 正しさ | 仕様どおりに動くか、テストで裏付けられているか | 本章 |
| 入力検証 | 型・範囲・パスの検証が漏れていないか | 第10章 |
| エラー処理 | 例外の握りつぶしが無いか、部分成功の扱いが明確か | 第8章 |
| セキュリティ | 秘密情報の直書きや、コマンドインジェクションの余地が無いか | 第10章 |
| ログ | 秘密情報のマスキング、過剰ログの抑制ができているか | 第9章 |
| dry-run | 破壊的操作にdry-runが効くか | 第12章 |
| 可読性・保守性 | 命名、関数の長さ、重複が適切か | 第14章 |

レビューを機能させるための実務上のコツ:

- **変更を小さく保つ**。1回のレビュー対象が大きいと、見落としが増え、レビューする側の負担も大きくなる（第16章）
- **指摘をブロッキングか任意か分ける**。「マストで直してほしい」と「気になったが必須ではない」を区別すると、議論が長引きにくい
- **機械的に検出できることは、lintとCIに任せる**。人間のレビューは、仕様の妥当性や設計判断のような、機械では判断しづらい観点に集中する
- **なぜその実装にしたかを、PRの説明やコミットメッセージに書く**。レビューする側が意図を推測する手間を減らす

---

## 13.13 CIへの組み込み

**CI（継続的インテグレーション）**は、コードの変更を取り込むたびに、テストや静的解析を自動実行する仕組みである。

CIに載せる基本的なステップ:

1. 依存関係のインストール
2. lint（ruff、shellcheck、PSScriptAnalyzer）
3. 型チェック（mypy）
4. テスト（pytest、Bashのテストスクリプト、Pester）
5. すべて成功したときだけマージ可能にする

GitHub Actionsの例:

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r infra_scripting_coding_guide/requirements.txt
      - run: ruff check infra_scripting_coding_guide
      - run: mypy --strict infra_scripting_coding_guide/samples/python
      - run: pytest infra_scripting_coding_guide/tests -v

  bash:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get update && sudo apt-get install -y shellcheck
      - run: shellcheck infra_scripting_coding_guide/samples/bash/*.sh
      - run: bash infra_scripting_coding_guide/tests/test_13_classify_disk.sh

  powershell:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - shell: pwsh
        run: |
          Install-Module -Name Pester -MinimumVersion 5.5 -Force -SkipPublisherCheck
          Invoke-Pester ./infra_scripting_coding_guide/tests -CI
```

CI設計のポイント:

- **言語ごとにジョブを分ける**。1つのジョブに詰め込むと、どの言語の問題で落ちたか分かりにくくなる
- **PowerShellはWindowsランナーで動かす**。`Win32_LogicalDisk` のようなWindows固有APIに依存するコードは、Linux上のpwshでは動かない
- **失敗したらマージをブロックする**。ブランチ保護ルールで、CIが green のPRだけをマージ可能にする
- **実行時間が伸びてきたら、変更されたファイルに関連するテストだけ先に流す等、段階的な最適化を検討する**。ただし本書の規模では、全件実行で十分に速い

> **警告**: CIのSecrets（APIトークンなど）は、ワークフローのログに出さない。
> `set -x` のようなコマンド全体を表示するデバッグオプションを有効にしたまま秘密情報を扱う処理を実行すると、
> CIの実行ログに秘密情報が残ってしまう（第9章、第10章）。

---

## 13.14 実務向け改善: opsctlのディスク分類とテストスイート

`disk-check` 相当の機能を、テストしやすい形に分割した実装を示す。
完全なファイルは `samples/python/13_disk_classifier.py` に置く。

```python
#!/usr/bin/env python3
"""ディスク使用率を分類する opsctl の補助モジュール。

第13章のテスト例（ユニット、境界値、モック、結合）で対象にするコードである。
`df -P` 相当のテキストをパースし、閾値に基づいて ok/warning/critical に分類する。
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, asdict
from typing import TextIO

logger = logging.getLogger("opsctl.disk_classifier")

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_RUNTIME = 2
EXIT_CRITICAL = 3


class InvalidThresholdError(ValueError):
    """warn/crit の閾値関係が不正なときに送出する。"""


@dataclass
class DiskUsage:
    mount_point: str
    used_percent: float


@dataclass
class ClassifiedUsage:
    mount_point: str
    used_percent: float
    status: str


def classify_disk_usage(used_percent: float, warn_percent: float, crit_percent: float) -> str:
    """使用率を ``ok``/``warning``/``critical`` に分類する。

    境界値は「以上」で次の段階に上がる。
    つまり ``used_percent == warn_percent`` は ``warning`` になり、
    ``used_percent == crit_percent`` は ``critical`` になる。
    """
    if warn_percent > crit_percent:
        raise InvalidThresholdError(
            f"warn_percent ({warn_percent}) must be <= crit_percent ({crit_percent})"
        )
    if used_percent < 0 or used_percent > 100:
        raise ValueError(f"used_percent out of range: {used_percent}")

    if used_percent >= crit_percent:
        return "critical"
    if used_percent >= warn_percent:
        return "warning"
    return "ok"


def parse_df_output(text: str) -> list[DiskUsage]:
    """``df -P`` 相当のテキストをパースする。

    先頭行はヘッダーとして無視する。
    列数が不足する行や使用率が数値でない行は、警告ログを出して読み飛ばす。
    """
    results: list[DiskUsage] = []
    lines = text.strip("\n").splitlines()
    if not lines:
        return results

    for line in lines[1:]:
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) < 6:
            logger.warning("skipping malformed df line: %r", line)
            continue
        percent_field = fields[4].rstrip("%")
        try:
            used_percent = float(percent_field)
        except ValueError:
            logger.warning("skipping non-numeric percent field: %r", line)
            continue
        mount_point = fields[5]
        results.append(DiskUsage(mount_point=mount_point, used_percent=used_percent))
    return results


def fetch_disk_report(host: str, timeout: int = 10) -> list[DiskUsage]:
    """対象ホストで ``ssh host df -P`` を実行し、結果をパースする。

    外部プロセス呼び出しを ``parse_df_output`` から分離してあるため、
    テストでは ``subprocess.run`` だけをモックすれば、実際の ``ssh`` 接続なしに
    このパースロジックまで通した結合テストができる。
    """
    completed = subprocess.run(
        ["ssh", host, "df", "-P"],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"df on {host} failed: {completed.stderr.strip()}")
    return parse_df_output(completed.stdout)


def classify_all(
    usages: list[DiskUsage], warn_percent: float, crit_percent: float
) -> tuple[list[ClassifiedUsage], str]:
    """複数のディスク使用率をまとめて分類し、最悪ステータスも返す。"""
    results: list[ClassifiedUsage] = []
    worst = "ok"
    severity = {"ok": 0, "warning": 1, "critical": 2}

    for usage in usages:
        status = classify_disk_usage(usage.used_percent, warn_percent, crit_percent)
        results.append(
            ClassifiedUsage(mount_point=usage.mount_point, used_percent=usage.used_percent, status=status)
        )
        if severity[status] > severity[worst]:
            worst = status

    return results, worst


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="disk_classifier", description="Classify disk usage from df -P output"
    )
    parser.add_argument("--host", help="remote host to query via ssh")
    parser.add_argument(
        "--input-file",
        type=argparse.FileType("r", encoding="utf-8"),
        help="local df -P output, mainly for testing without ssh",
    )
    parser.add_argument("--warn-percent", type=float, default=80.0)
    parser.add_argument("--crit-percent", type=float, default=90.0)
    parser.add_argument("--timeout", type=int, default=10)
    return parser


def _read_usages(args: argparse.Namespace) -> list[DiskUsage]:
    if args.input_file is not None:
        input_file: TextIO = args.input_file
        try:
            return parse_df_output(input_file.read())
        finally:
            input_file.close()
    return fetch_disk_report(args.host, timeout=args.timeout)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", stream=sys.stderr)
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if not args.host and args.input_file is None:
        parser.error("either --host or --input-file is required")

    try:
        usages = _read_usages(args)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        logger.error("failed to collect disk usage: %s", exc)
        return EXIT_RUNTIME

    try:
        results, worst = classify_all(usages, args.warn_percent, args.crit_percent)
    except InvalidThresholdError as exc:
        logger.error("%s", exc)
        return EXIT_USAGE

    print(json.dumps({"results": [asdict(r) for r in results], "worst": worst}, ensure_ascii=False))

    if worst == "critical":
        return EXIT_CRITICAL
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
```

設計上のポイント:

- `parse_df_output` は純粋関数（入力だけから出力が決まり、副作用が無い）にしてあり、ユニットテストが書きやすい
- `fetch_disk_report` は外部コマンド呼び出しを持つが、`subprocess.run` だけをモックすれば、実際の `ssh` 接続なしにパースまで通した結合テストができる
- `main` は `--input-file` を持ち、`--host` を経由した実際のネットワーク接続なしにCLI全体を結合テストできる
- 例外の型（`InvalidThresholdError`、`RuntimeError`、`subprocess.TimeoutExpired`）を使い分け、テストで `pytest.raises` により区別して検証できる

実行例:

```bash
printf 'Filesystem 1024-blocks Used Available Capacity Mounted-on\n/dev/sda1 100 88 12 88%% /\n' \
  | python3 samples/python/13_disk_classifier.py --input-file /dev/stdin
# stdout: {"results": [{"mount_point": "/", "used_percent": 88.0, "status": "warning"}], "worst": "warning"}
# exit code: 0
```

---

## 13.15 悪い例と問題点

テストコード自体にも、良し悪しがある。
次は、動くが問題のあるテストの例である。

```python
import time

import requests


def test_disk_check():
    # 実際のAPIを呼んでいる。ネットワークが無い、または相手側が落ちていると失敗する
    response = requests.get("https://api.example.invalid/v1/disks", timeout=5)
    time.sleep(2)  # サーバー処理待ちのための固定スリープ。遅く、待ち時間が本当に十分かも不明
    data = response.json()
    assert data  # 何を検証しているのか名前からも中身からも分からない

    # 別の関心事（ファイル書き込み）を同じテストに詰め込んでいる
    with open("/tmp/disk_report.txt", "w") as f:
        f.write(str(data))
    assert True  # 実質何も検証していない
```

問題点:

- 実際のネットワークとAPIに依存しており、CI環境やオフライン環境では常に失敗する（不安定、いわゆるflaky test）
- `time.sleep(2)` は、実際に2秒で十分か根拠が無く、テスト全体を遅くする（第8章のリトライテストと同様、モックで置き換えるべき箇所）
- `assert data` は「データが何か入っていればよい」というだけで、期待する値を検証していない
- ファイル書き込みという別の関心事を同じテストに混ぜており、失敗したときにAPI呼び出しとファイル書き込みのどちらが原因か切り分けにくい
- `/tmp/disk_report.txt` という固定パスを使っており、並列実行時に他のテストと衝突する可能性がある
- `assert True` は常に成功し、テストとして意味を持たない

---

## 13.16 改善後のコード

13.15の問題点を1つずつ解消し、関心事ごとにテストを分割する。

```python
import json
from pathlib import Path


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def json(self) -> dict:
        return self._payload


def fetch_disk_report_via_api(session, base_url: str, timeout: int = 5) -> dict:
    """APIから取得したJSONをそのまま返す。セッションを引数で受け取ることで、
    テストでは requests.get 自体をモックせず、偽のセッションを渡すだけで済む。
    """
    response = session.get(f"{base_url}/v1/disks", timeout=timeout)
    return response.json()


def test_fetch_disk_report_via_api_returns_parsed_json() -> None:
    class FakeSession:
        def get(self, url: str, timeout: int) -> FakeResponse:
            assert url == "https://api.example.invalid/v1/disks"
            assert timeout == 5
            return FakeResponse({"disks": [{"mount": "/", "used_percent": 42}]})

    result = fetch_disk_report_via_api(FakeSession(), "https://api.example.invalid")

    assert result == {"disks": [{"mount": "/", "used_percent": 42}]}


def test_disk_report_is_written_to_a_temp_file(tmp_path: Path) -> None:
    report_path = tmp_path / "disk_report.json"
    payload = {"disks": [{"mount": "/", "used_percent": 42}]}

    report_path.write_text(json.dumps(payload), encoding="utf-8")

    assert json.loads(report_path.read_text(encoding="utf-8")) == payload
```

改善点:

- 実際のネットワーク呼び出しをせず、`FakeSession` という依存性注入で置き換えている。`monkeypatch` で `requests.get` 自体をパッチする方法もあるが、
  関数がセッションを引数で受け取る設計にしておくと、モックがさらに単純になる
- `time.sleep` を廃止した。非同期処理の完了待ちが本当に必要な場合は、固定スリープではなくポーリングとタイムアウト上限を組み合わせる（第8章のリトライ設計を参照）
- API呼び出しの検証とファイル書き込みの検証を、別々のテスト関数に分離した。どちらかが失敗したとき、テスト名から原因箇所がすぐ分かる
- `tmp_path` を使い、固定パスへの依存と、テスト間の衝突を無くした
- `assert result == {...}` のように、期待する値を具体的に書いている

Bashで同種の問題を避ける改善例（`13_classify_disk.sh` からの抜粋、ソースするだけでは処理が走らないガード）:

```bash
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

このガードが無いBashスクリプトを `source` すると、テストのつもりが本処理まで実行してしまい、
13.15の「意図しない副作用を含むテスト」と同じ問題を引き起こす。

---

## 13.17 セキュリティ上の注意点

- テストコードにも本物の秘密情報を書かない。APIトークンやパスワードのテストデータは、明らかにダミーと分かる値（例: `dummy-token-for-test`）を使う
- モックを使い、テストが実際の本番システムへ誤って書き込み・削除を行わないようにする。特に「モックし忘れた1箇所」が本番へ到達する事故に注意する
- CIのログに、テスト失敗時のスタックトレースが秘密情報を含まないか確認する（第9章のマスキングと同じ考え方）
- 依存パッケージ（pytest、ruff、mypyなど）は、信頼できる配布元から、バージョンを固定して導入する（第14章の依存関係管理を参照）
- CIのSecretsをテストコードやログに出力しない。`print(os.environ)` のような全環境変数のダンプは、CI上では特に危険である

> **警告**: 結合テストやE2Eテストで実際の外部システムに接続する構成を取る場合、
> テスト専用の環境（本番から隔離されたステージング環境など）を用意する。
> 本番のAPIやデータベースに対して、テストのたびに書き込み・削除を行う構成にしない。

---

## 13.18 テスト方法

本章のテスト基盤自体を検証する方法を示す。
完全なテストファイルは `tests/test_13_disk_classifier.py`、`tests/test_13_classify_disk.sh`、`tests/13_classify_disk.Tests.ps1` に置く（抜粋を示す）。

Python（境界値、異常系、モック、CLI結合の代表例）:

```python
import subprocess

import pytest

from conftest import load_sample_module

disk_classifier = load_sample_module("13_disk_classifier.py")


@pytest.mark.parametrize(
    ("used_percent", "expected"),
    [
        (79.9, "ok"),
        (80.0, "warning"),
        (90.0, "critical"),
        (100.0, "critical"),
    ],
)
def test_classify_disk_usage_boundaries(used_percent: float, expected: str) -> None:
    assert disk_classifier.classify_disk_usage(used_percent, warn_percent=80.0, crit_percent=90.0) == expected


def test_classify_disk_usage_rejects_inverted_thresholds() -> None:
    with pytest.raises(disk_classifier.InvalidThresholdError):
        disk_classifier.classify_disk_usage(85.0, warn_percent=90.0, crit_percent=80.0)


def test_fetch_disk_report_mocks_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            cmd,
            returncode=0,
            stdout="Filesystem 1024-blocks Used Available Capacity Mounted-on\n"
            "/dev/sda1 100 88 12 88% /\n",
            stderr="",
        )

    monkeypatch.setattr(disk_classifier.subprocess, "run", fake_run)

    usages = disk_classifier.fetch_disk_report("web01.example.invalid")
    assert usages[0].mount_point == "/"


def test_main_with_input_file_reports_critical(tmp_path, capsys) -> None:
    input_file = tmp_path / "df.txt"
    input_file.write_text(
        "Filesystem 1024-blocks Used Available Capacity Mounted-on\n"
        "/dev/sda1 100 95 5 95% /\n",
        encoding="utf-8",
    )
    exit_code = disk_classifier.main(["--input-file", str(input_file)])
    assert exit_code == disk_classifier.EXIT_CRITICAL
```

`load_sample_module` は `tests/conftest.py` で定義した補助関数である。
`samples/python` 配下のファイルは `13_disk_classifier.py` のように数字で始まる名前であり、
`import 13_disk_classifier` という文は書けない（数字始まりの識別子は文法違反になる）。
`importlib.util` でファイルパスから直接読み込むことで、番号付きファイルのまま実行可能なテストにしている。
実務では、`samples/python` を番号無しのパッケージとして整理し、通常の `import` を使う構成を推奨する（第5章、第12章）。

実行結果の例:

```bash
cd infra_scripting_coding_guide
pytest tests/ -v
# ... 41 passed
```

Bash（抜粋）:

```bash
source samples/bash/13_classify_disk.sh

assert_eq() {
  [[ "$1" == "$2" ]] || { echo "FAIL: $3: expected=$1 actual=$2" >&2; exit 1; }
  echo "ok: $3"
}

assert_eq "warning" "$(classify_disk_usage 80 80 90)" "80%(=warn) is warning"
assert_eq "critical" "$(classify_disk_usage 90 80 90)" "90%(=crit) is critical"
```

PowerShell（Pester、抜粋）:

```powershell
BeforeAll {
    . "$PSScriptRoot/../samples/powershell/13_classify_disk.ps1"
}

Describe 'Get-DiskStatus' {
    It 'returns warning exactly at warn threshold' {
        Get-DiskStatus -UsedPercent 80 -WarnPercent 80 -CritPercent 90 | Should -Be 'warning'
    }

    It 'throws when used percent is out of range' {
        { Get-DiskStatus -UsedPercent 150 -WarnPercent 80 -CritPercent 90 } | Should -Throw
    }
}
```

---

## 章末問題

### 問題1

ユニットテストと結合テストの違いを、対象範囲と実行速度の観点で説明せよ。

### 問題2

`used_percent >= warn_percent` という条件の境界値テストとして、どのような値を選ぶべきか、3点挙げよ。

### 問題3

モックを使いすぎると、どのような問題が起きるか説明せよ。

### 問題4

`time.sleep(2)` を使ったテストの問題点を挙げ、代替方法を1つ述べよ。

### 問題5

lintとテストは、それぞれ何を検出できて何を検出できないか説明せよ。

---

## 解答と解説

### 問題1

ユニットテストは1つの関数やクラスを対象にし、外部依存をモックで切り離すため実行が速い。
結合テストは複数の部品や外部システムとの連携を対象にするため、I/Oを含み実行が遅くなりやすい。

### 問題2

閾値のすぐ下（例: 79%）、閾値ちょうど（例: 80%）、閾値のすぐ上（例: 81%）の3点を選ぶ。
これにより、`>` と `>=` の取り違えのような off-by-one エラーを検出できる。

### 問題3

依存部品の実際の挙動が検証されなくなり、モックした境界の外側で起きる不具合（インターフェースの不一致、実際のAPIレスポンス形式の変化など）を見逃す。
テストは通るが本番で壊れる「偽陽性」が起きやすくなる。

### 問題4

実際に必要な待機時間が分からず、環境によって足りない、または無駄に長くなる。
テスト全体も遅くなる。
代替方法: 完了をポーリングで確認しタイムアウト上限を設ける、または対象のI/Oをモックして待機自体を無くす。

### 問題5

lintは、構文誤り、未使用変数、危険なパターン（クォート漏れ、broad exceptなど）を実行前に検出できるが、
ロジックが仕様どおりかまでは判定できない。
テストは、実際にコードを実行し、期待する結果になるかを検証できるが、テストケースとして書かれていない入力やパスは検出できない。
両方を組み合わせて初めて、実行前の問題と実行時の問題の両方をカバーできる。

---

## 実装演習

### 演習A

`13_disk_classifier.py` の `classify_all` に、`warn_percent` と `crit_percent` が等しい場合（閾値が1段階しかない）の挙動を確認するテストを追加せよ。
境界値としてどう扱うべきか、コメントで理由も書くこと。

### 演習B

`13_classify_disk.sh` に、`--warn-percent` と `--crit-percent` を省略したときのデフォルト値（80、90）が使われることを確認するテストを、`tests/test_13_classify_disk.sh` に追加せよ。

### 演習C

`13_classify_disk.ps1` の `Get-LocalDiskUsage` をモックし、複数のディスクのうち1つだけが `critical` の場合に、`Invoke-Main` の標準出力（JSON）に全ディスクの結果が含まれることを検証するPesterテストを書け。

---

## 次章予告

第14章では、保守しやすいコードを扱う。
命名、関数の長さ、責務分離、マジックナンバーの排除、依存関係の管理、リファクタリングと技術的負債への向き合い方を、
これまでの章のサンプルを題材に実装する。


---


<!-- SOURCE: 14_maintainable_code.md -->

# 第14章 保守しやすいコード

## 学習目標

この章を終えると、次ができるようになる。

- 命名、関数の長さ、責務分離の観点から、変更しやすいコードとしにくいコードを見分けられる
- 重複したロジックを見つけ、共通化して保守箇所を一つにできる
- マジックナンバーを設定値や名前付き定数に置き換えられる
- 依存関係のバージョンを固定する理由と、固定しすぎることの副作用を説明できる
- 後方互換性を保ちながら機能を非推奨化し、安全にリファクタリングを進められる

前提: 第5章（関数とモジュール、責務分離）、第12章（設定とコードの分離）、第13章（テスト）。

サンプルコードは学習用である。
本番コードのリファクタリングは、必ずテストで現状の挙動を固定してから着手すること。
テストが無い状態での大規模な書き換えは、意図しない挙動変化を検出できないまま本番へ出る危険がある。

---

## 14.1 基本概念

**保守性**は、コードを書いた本人以外が、時間が経ってからでも安全に読み、変更できる度合いである。

保守性は、動いているかどうかとは別の軸である。
正しく動くコードでも、半年後に見て意図が分からなければ、変更のたびに調査コストがかかり、誤った変更を入れるリスクが上がる。

保守性を左右する要素は、突き詰めると「読み手が正しく推測できるか」に集約される。

- 名前から処理内容を推測できるか
- 関数やモジュールの範囲から責務を推測できるか
- 値の意味をコードの外（設定、定数名）から推測できるか
- 依存するライブラリのバージョンが、実行のたびに変わらず推測できるか

推測できない箇所が増えるほど、変更前に読むコード量が増え、変更後の確認範囲も広がる。

---

## 14.2 命名

**命名**は、変数・関数・モジュールに、その役割を表す名前を付けることである。

良い名前は、コメントを読まなくても処理内容を推測させる。
悪い名前は、実装を読まないと何のための値か分からない。

| 悪い例 | 改善後 | 理由 |
|--------|--------|------|
| `d` | `disk_usage_percent` | 単位と意味が分かる |
| `chk()` | `check_disk_usage()` | 何を確認する処理か分かる |
| `flag` | `is_dry_run` | 真偽値であることと意味が分かる |
| `data` | `host_usage_rows` | 何のデータかが分かる |
| `tmp` | `retry_delay_seconds` | 一時変数でも、意味と単位を示せる |
| `process()` | `classify_disk_usage()` | 汎用的すぎる名前を避ける |

三言語ごとの命名規約は次のとおりである。
規約が違っても、目的（意味の推測しやすさ）は共通している。

| 言語 | 変数・関数 | 慣例 |
|------|------------|------|
| Python | `snake_case` | PEP 8。クラスは `PascalCase` |
| Bash | `snake_case`、関数はモジュール名で名前空間化（第5章の `hostlib::load_hosts`） | Bashには言語標準の命名規約が無いが、`snake_case` が広く使われる |
| PowerShell | 関数は`動詞-名詞`の`PascalCase`（`Get-DiskStatus`） | `Get-Verb` で承認済み動詞を確認できる |

真偽値の変数・関数は、`is_`、`has_`、`should_` のような接頭辞を付けると、値の意味が読み取りやすくなる。

```python
# 悪い例: 真偽値なのか処理なのか名前から分からない
def dry_run(args) -> bool:
    ...

# 改善後
def is_dry_run(args: argparse.Namespace) -> bool:
    ...
```

省略形は、チーム全体で意味が通じる場合に限定する。
`cfg`（config）や `msg`（message）のような広く定着した省略形は問題にならないが、個人的な省略（`husg` のような造語）は避ける。

---

## 14.3 関数の長さと責務

第5章で分割の判断基準を扱った。
ここでは、既に大きくなってしまった関数を見つけ、直す観点を扱う。

関数が大きくなりすぎているサインは次のとおりである。

- 1画面でスクロールしないと全体を読めない（目安として40〜60行を超える）
- 関数の中に、明確に段落分けできる処理のまとまりが複数ある（読み込み、検証、判定、書き込みなど）
- 変更するとき、関数名が示す責務と関係ない部分まで読む必要がある
- テストを書こうとすると、無関係な前提条件まで用意しないと呼び出せない

```python
# 悪い例: 1つの関数に「引数解析」「検証」「読み込み」「判定」「書き込み」「通知」が全部入っている
def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--warn", type=float, default=80)
    parser.add_argument("--crit", type=float, default=90)
    args = parser.parse_args(argv)

    if args.warn > args.crit:
        print("invalid thresholds", file=sys.stderr)
        return 1

    rows = []
    with open(args.input, encoding="utf-8") as fh:
        for line in fh:
            host, usage = line.strip().split(",")
            rows.append((host, float(usage)))

    results = []
    for host, usage in rows:
        if usage >= args.crit:
            status = "CRITICAL"
        elif usage >= args.warn:
            status = "WARNING"
        else:
            status = "OK"
        results.append((host, usage, status))
        if status == "CRITICAL":
            requests.post("https://hooks.example.invalid/notify", json={"host": host})

    with open("report.csv", "w", encoding="utf-8") as fh:
        for host, usage, status in results:
            fh.write(f"{host},{usage},{status}\n")

    return 0
```

この関数は、引数解析・検証・入力読み込み・判定・通知・出力という6つの責務を持つ。
`classify` 相当の判定だけをテストしたくても、ファイル読み込みとHTTP呼び出しが必ず実行される。

責務ごとに分けると、次のようになる。

```python
def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--warn", type=float, default=80)
    parser.add_argument("--crit", type=float, default=90)
    return parser.parse_args(argv)


def validate_thresholds(warn: float, crit: float) -> None:
    if warn > crit:
        raise ValueError("--warn must be <= --crit")


def load_usage_rows(path: Path) -> list[tuple[str, float]]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            host, usage = line.strip().split(",")
            rows.append((host, float(usage)))
    return rows


def classify(usage: float, warn: float, crit: float) -> str:
    if usage >= crit:
        return "CRITICAL"
    if usage >= warn:
        return "WARNING"
    return "OK"


def notify_critical(host: str, *, notifier: Callable[[str], None]) -> None:
    notifier(host)


def write_report(path: Path, results: list[tuple[str, float, str]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for host, usage, status in results:
            fh.write(f"{host},{usage},{status}\n")
```

分割後は、`classify` を単体でテストでき、`validate_thresholds` の異常系も個別に確認できる。
`main` は、これらを呼び出す薄い調整役になる（第5章の考え方と同じ）。

---

## 14.4 重複排除

**重複**は、同じ、または本質的に同じロジックが、複数箇所に存在する状態である。

重複の何が問題かというと、修正漏れである。
バグ修正や仕様変更のとき、コピーされた箇所の一つを直し忘れると、直した箇所と直していない箇所で挙動が食い違う。

```python
# 悪い例: 3つのサービス確認関数が、タイムアウト値以外ほぼ同じ処理をコピーしている
def check_web(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "5", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0


def check_db(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "10", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0


def check_cache(host: str) -> bool:
    result = subprocess.run(["curl", "-sf", "--max-time", "3", f"http://{host}/health"], capture_output=True)
    return result.returncode == 0
```

タイムアウト値の意味（なぜwebは5秒でdbは10秒か）もコード中に残らず、`--max-time` の書式を変えたくなったとき3箇所を直す必要がある。

共通処理を1つの関数にまとめ、違いだけを引数にする。

```python
def check_service(host: str, *, timeout_seconds: int) -> bool:
    result = subprocess.run(
        ["curl", "-sf", "--max-time", str(timeout_seconds), f"http://{host}/health"],
        capture_output=True,
        timeout=timeout_seconds + 2,
    )
    return result.returncode == 0
```

重複排除は、似ているコードを闇雲に一つへ統合することではない。
「たまたま似ているが、将来別々に変化する可能性が高い処理」を無理に共通化すると、片方の変更がもう片方に影響し、条件分岐だらけの関数になる。
共通化するかどうかは、変更される理由が同じかどうかで判断する。

---

## 14.5 マジックナンバーと設定値

**マジックナンバー**は、コード中に直接書かれた、意味の説明が無い数値や文字列リテラルである。

```python
# 悪い例
if usage >= 90:
    return "CRITICAL"
if usage >= 80:
    return "WARNING"

time.sleep(0.5 * (2 ** attempt))  # 0.5 の意味がコードから読み取れない
```

`90`、`80`、`0.5` が何を意味するか、コードを読むだけでは分からない。
同じ値が別の場所に散らばっていると、一方だけ変更して不整合を起こしやすい。

名前付き定数にすると、意味と変更箇所が一つになる。

```python
DEFAULT_WARN_PERCENT = 80.0
DEFAULT_CRIT_PERCENT = 90.0
RETRY_BASE_DELAY_SECONDS = 0.5

if usage >= DEFAULT_CRIT_PERCENT:
    return "CRITICAL"
if usage >= DEFAULT_WARN_PERCENT:
    return "WARNING"

time.sleep(RETRY_BASE_DELAY_SECONDS * (2 ** attempt))
```

さらに、実行環境ごとに変わりうる値（第12章の「設定とコードの分離」）は、定数のままコードに置かず、設定ファイルや環境変数から解決する。

```python
warn_percent = resolve_threshold(cli_value=args.warn, config=config, key="disk_warn_percent", default=DEFAULT_WARN_PERCENT)
```

定数化すべきものと、設定化すべきものは区別する。

- 変更されないが意味を明示したい値（HTTPステータスコードの200など） → 名前付き定数
- 環境やチームによって変わりうる値（しきい値、タイムアウト、対象ホスト） → 設定ファイルや環境変数

---

## 14.6 コメントとドキュメント

**コメント**は、コードだけでは伝わらない意図や制約を補足する文章である。

コメントを書くべき場面と、書くべきでない場面がある。

```python
# 悪い例: コードをそのまま日本語に翻訳しただけ
i = i + 1  # iに1を足す

# 良い例: なぜそうするのか、コードだけでは分からない理由を書く
attempt += 1  # 初回リクエストも1回に数える(ログの attempt=1 がAPI呼び出し1回目と一致するように)
```

書くべきコメントの例:

- なぜその実装を選んだか（別の実装をあえて避けた理由）
- 一見不要に見えるが、外部要因のために必要な処理（特定OSのバグ回避など）
- TODOやFIXME（担当者や期限、関連チケット番号を添える）

```python
# WORKAROUND: macOSのbash 3.2では配列の空展開が異なる挙動をするため、
# 明示的に長さチェックを入れている。Bash 4以降では不要。
if [[ ${#hosts[@]} -gt 0 ]]; then
```

**ドキュメント**は、コードの外、またはdocstring・コメントブロックとして、使い方や設計方針をまとめたものである。
関数単位の使い方はdocstringに、モジュール全体の設計方針や運用手順はREADMEやこの種の解説書に書く。

```python
def resolve_timeout(cli_value: int | None, config: dict[str, Any]) -> int:
    """CLI引数 > 環境変数 > 設定ファイル > デフォルトの順で解決する。

    Args:
        cli_value: --timeout で指定された値。未指定なら None。
        config: 読み込み済みの設定辞書。

    Returns:
        解決済みのタイムアウト秒数。
    """
```

コメントとドキュメントは、コードの変更に追従しないと嘘の情報源になる。
コードレビューでロジックを変更したときは、関連するコメントとdocstringも同時に見直す。

---

## 14.7 依存関係とバージョン固定

**依存関係**は、自分のコードが動くために必要な、外部のライブラリやツールである。

**バージョン固定**は、依存関係のバージョンを明示的に指定し、実行のたびに異なるバージョンが入らないようにすることである。

```text
# requirements.txt: 悪い例
requests
pyyaml
```

バージョンを指定しないと、`pip install` を実行するタイミングによって異なるバージョンが入る。
ライブラリ側の破壊的変更（メジャーバージョンアップでの仕様変更）が、何もコードを変えていないのに突然ビルドを壊す原因になる。

```text
# requirements.txt: 改善後
requests==2.32.3
PyYAML==6.0.2
```

`==` による完全固定は再現性が最も高いが、セキュリティ修正を含む更新にも自分で追従する必要がある。
運用方針として、次のいずれかを選ぶ。

| 方針 | 書き方 | 向く場面 |
|------|--------|----------|
| 完全固定 | `requests==2.32.3` | 本番環境、再現性を最優先する場合 |
| 下限指定 | `requests>=2.32` | ライブラリ、互換範囲が分かっている場合 |
| 範囲指定 | `requests>=2.32,<3.0` | メジャーバージョンの破壊的変更だけ避けたい場合 |

Pythonでは `pip freeze > requirements-lock.txt` のようなロックファイル、またはPoetryやuvといったツールで依存関係全体（間接的な依存も含む）を固定できる。
PowerShellの `Install-Module` も `-RequiredVersion` でバージョンを固定できる。

```powershell
Install-Module -Name Pester -RequiredVersion 5.5.0 -Scope CurrentUser -Force
```

Bashは、外部コマンド（`curl`、`jq` など）のバージョンをOSのパッケージマネージャーに委ねることが多い。
バージョン差異が問題になる場合は、スクリプト内でバージョンを確認し、要件を満たさなければ早期にエラーにする。

```bash
if ! jq --version | grep -qE 'jq-1\.[6-9]'; then
  echo "jq 1.6 or later is required" >&2
  exit 1
fi
```

> **警告**: 古いバージョンに固定したまま長期間放置すると、既知の脆弱性が修正されないまま使われ続ける。
> バージョン固定は「勝手に変わらないこと」を保証する仕組みであり、「更新しなくてよい」という意味ではない。定期的な棚卸しと更新を運用に組み込む。

---

## 14.8 後方互換性と非推奨化

**後方互換性**は、新しいバージョンのコードが、古い呼び出し方や設定でも動き続ける性質である。

**非推奨化**は、古いインターフェースを即座に削除せず、警告を出しながら一定期間残す進め方である。

CLIのオプション名を変更する例で考える。

```python
# 悪い例: 予告なく --host を削除し、--target-host に変更する
parser.add_argument("--target-host", required=True)
# 既存の運用スクリプトが --host を渡していると、いきなり動かなくなる
```

既存の呼び出し元（他チームのスクリプト、cron、CIジョブ）が突然壊れると、影響範囲の調査に時間を取られる。
非推奨化を挟むと、移行期間を確保できる。

```python
import warnings

parser.add_argument("--target-host", default=None)
parser.add_argument("--host", default=None, help=argparse.SUPPRESS)  # 非推奨。ヘルプには出さない

args = parser.parse_args(argv)

if args.host is not None and args.target_host is None:
    warnings.warn(
        "--host is deprecated and will be removed in a future release; use --target-host instead",
        DeprecationWarning,
        stacklevel=2,
    )
    args.target_host = args.host

if args.target_host is None:
    parser.error("--target-host is required")
```

関数名を変更する場合も同様に、古い名前をラッパーとして残す。

```python
def check_service(host: str, *, timeout_seconds: int) -> bool:
    """新しい統一実装(14.4参照)。"""
    ...


def check_web(host: str) -> bool:
    """非推奨。check_service を使うこと。

    次のメジャーリリースで削除予定。
    """
    warnings.warn(
        "check_web is deprecated; use check_service(host, timeout_seconds=5) instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, timeout_seconds=5)
```

非推奨化の運用は、次の順序で進める。

1. 新しいインターフェースを追加し、既存のインターフェースはそのまま残す
2. 古いインターフェースを呼ぶと警告が出るようにする
3. 移行期間（リリースノートで告知した期間）を設ける
4. 移行が完了したことを確認してから、古いインターフェースを削除する

削除を急ぐと、把握していなかった利用箇所を壊す。
猶予を置きすぎると、非推奨のコードが増え続け、保守負担が下がらない。
どちらもチームの運用規模に応じて期間を決める。

---

## 14.9 リファクタリングの進め方

**リファクタリング**は、外部から見た挙動を変えずに、内部の実装を改善する作業である。

挙動を変えないことが前提のため、リファクタリング前にテストが無いと、変えていないつもりの挙動が変わったことに気づけない。

安全な進め方:

1. 対象コードに対するテストが無ければ、現状の挙動をそのまま固定するテスト（**特性化テスト**）を先に書く
2. 一度に一つの変更だけを行う（命名変更だけ、関数分割だけ、というように分ける）
3. 各変更のあとにテストを実行し、失敗しないことを確認してからコミットする
4. 大きな変更は、小さくレビュー可能な単位に分けてコミットする（第16章）

```python
# リファクタリング前の挙動を固定する特性化テスト
def test_legacy_run_behavior_before_refactor(tmp_path):
    input_path = tmp_path / "usage.csv"
    input_path.write_text("web01.example.invalid,95\n", encoding="utf-8")
    exit_code = run(["--input", str(input_path)])
    assert exit_code == 0
    # このテストは「正しい仕様」ではなく「今の挙動」を記録する。
    # リファクタリング後も同じ結果になることを確認してから、
    # 必要ならテストの期待値自体を仕様として見直す。
```

リファクタリングと機能追加は、同じコミットで混ぜない。
挙動が変わったとき、原因がリファクタリングによるものか機能追加によるものか切り分けられなくなる。

---

## 14.10 技術的負債

**技術的負債**は、その場をしのぐ実装や先送りにした設計判断が積み重なり、将来の変更コストを増やしている状態である。

負債という比喩が示すとおり、放置すると「利息」が発生する。
場当たり的な修正がさらに場当たり的な修正を呼び、変更のたびに影響範囲の調査が難しくなる。

技術的負債が生まれる典型的な状況:

- 締め切りに追われ、テストや検証を後回しにしたまま本番投入した
- 一時的なつもりだった回避策（14.6の`WORKAROUND`コメントのようなもの）が、恒久的な実装として残り続けた
- 依存関係を長期間更新せず、更新作業自体が大掛かりになってしまった
- ドキュメントが実装から乖離し、正しい情報がコードを読まないと分からない

技術的負債は、ゼロにすることを目指す性質のものではない。
締め切りに間に合わせるために意図的に負債を選ぶ判断もありうる。
重要なのは、負債を可視化し、あとで返済する計画を持つことである。

実務での扱い方:

- `TODO`/`FIXME`コメントに、内容だけでなく担当や関連チケット番号を添える
- 課題管理システムに負債専用のラベルを付け、棚卸しの対象にする
- 新機能の開発と並行して、負債返済の時間を定期的に確保する（スプリントの一定割合を割り当てるなど）
- 「動いているから触らない」判断と、「危険だから早期に返済する」判断を、影響範囲とリスクで区別する（セキュリティに関わる負債は優先度を上げる）

---

## 14.11 実務向け改善: サービス確認モジュールのリファクタリング

`samples/python/14_health_checks.py` に、14.3〜14.8の考え方をまとめて適用したモジュールを置く。
重複していた3つの確認関数を1つに統合し、マジックナンバーを定数化し、既存の関数名は非推奨警告付きで残す。

```python
#!/usr/bin/env python3
"""サービスのヘルスチェックを行う共通モジュール。

旧来は check_web/check_db/check_cache が個別に重複した実装を持っていた。
本モジュールでは check_service に統合し、旧関数は後方互換のための
非推奨ラッパーとして残す(第14章 14.4, 14.8参照)。
"""
from __future__ import annotations

import logging
import subprocess
import warnings
from dataclasses import dataclass

# サービスごとの既定タイムアウト(秒)。
# web: フロントは応答性が重要なため短め。
# db: 接続確立に時間がかかることがあるため長め。
# cache: 応答が速いことが前提のミドルウェアのため最短。
DEFAULT_TIMEOUT_SECONDS: dict[str, int] = {
    "web": 5,
    "db": 10,
    "cache": 3,
}
FALLBACK_TIMEOUT_SECONDS = 5
CURL_EXTRA_TIMEOUT_MARGIN_SECONDS = 2

logger = logging.getLogger("health_checks")


@dataclass
class HealthCheckResult:
    host: str
    service: str
    ok: bool
    timeout_seconds: int


def check_service(host: str, service: str, *, timeout_seconds: int | None = None) -> HealthCheckResult:
    """統合されたヘルスチェック関数。

    timeout_seconds を省略すると、service名に応じた既定値
    (DEFAULT_TIMEOUT_SECONDS)を使う。未知のservice名は
    FALLBACK_TIMEOUT_SECONDS を使う。
    """
    resolved_timeout = timeout_seconds if timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS.get(
        service, FALLBACK_TIMEOUT_SECONDS
    )
    result = subprocess.run(
        ["curl", "-sf", "--max-time", str(resolved_timeout), f"http://{host}/health"],
        capture_output=True,
        timeout=resolved_timeout + CURL_EXTRA_TIMEOUT_MARGIN_SECONDS,
        check=False,
    )
    return HealthCheckResult(host=host, service=service, ok=result.returncode == 0, timeout_seconds=resolved_timeout)


def check_web(host: str) -> bool:
    """非推奨。check_service(host, "web") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_web is deprecated; use check_service(host, "web") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "web").ok


def check_db(host: str) -> bool:
    """非推奨。check_service(host, "db") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_db is deprecated; use check_service(host, "db") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "db").ok


def check_cache(host: str) -> bool:
    """非推奨。check_service(host, "cache") を使うこと。次のメジャーリリースで削除予定。"""
    warnings.warn(
        'check_cache is deprecated; use check_service(host, "cache") instead',
        DeprecationWarning,
        stacklevel=2,
    )
    return check_service(host, "cache").ok
```

`check_service` は、タイムアウトの意味をコメントで明示し、値そのものは辞書（設定に近い形）にまとめている。
旧関数は挙動を変えずに残し、呼び出し元には警告だけを出す。
呼び出し元の移行が完了した時点で、旧関数と`DEFAULT_TIMEOUT_SECONDS`の`web`/`db`/`cache`固定値依存を削除する判断ができる。

---

## 14.12 悪い例と問題点

```python
#!/usr/bin/env python3
import subprocess


def chk1(h):
    r = subprocess.run(["curl", "-sf", "--max-time", "5", f"http://{h}/health"], capture_output=True)
    return r.returncode == 0


def chk2(h):
    # chk1とほぼ同じ処理をコピーしている。タイムアウト値だけ違う
    r = subprocess.run(["curl", "-sf", "--max-time", "10", f"http://{h}/health"], capture_output=True)
    return r.returncode == 0


def process(hosts):
    results = []
    for h in hosts:
        ok = chk1(h)  # なぜchk1が呼ばれるのか、名前から推測できない
        results.append((h, ok))
        if not ok:
            # 0.5, 3 の意味が不明なマジックナンバー
            import time
            time.sleep(0.5)
            ok = chk1(h)
            if not ok:
                time.sleep(3)
    return results
```

問題点:

- `chk1`、`chk2`、`process` という名前から処理内容を推測できない
- `chk1` と `chk2` がタイムアウト値以外ほぼ同じ処理を重複させている
- `0.5`、`3` の意味が説明されておらず、リトライ間隔の設計意図が失われている
- `process` 関数の中に、確認・リトライ・待機という複数の責務が混在している
- `import time` が関数の中にあり、依存関係がファイル冒頭から見えない
- バージョン固定や後方互換性への配慮が無く、`chk1`/`chk2`の呼び出し元を洗い出さないと安全に変更できない

---

## 14.13 改善後のコード

14.11の `check_service` と、名前付き定数、非推奨ラッパーの組み合わせが改善後にあたる。
呼び出し側は次のように書き換わる。

```python
from samples.python.health_checks import check_service

RETRY_DELAY_SECONDS = 0.5
MAX_RETRIES = 2


def check_with_simple_retry(host: str, service: str) -> bool:
    """1回失敗したら固定間隔で再試行する簡易版(第8章のリトライとは別に、
    ヘルスチェックの表面的な揺らぎだけを吸収する用途)。
    """
    for attempt in range(MAX_RETRIES + 1):
        result = check_service(host, service)
        if result.ok:
            return True
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)
    return False
```

`check_service`、`RETRY_DELAY_SECONDS`、`MAX_RETRIES` という名前だけで、処理の見通しが立つ。
リトライの間隔や回数を変えたくなったときも、変更箇所は定数の1箇所で済む。

---

## 14.14 セキュリティ上の注意点

- 依存関係のバージョンを固定したまま更新を止めると、既知の脆弱性が残り続ける。定期的な依存関係の棚卸しを運用に組み込む（14.7）
- 非推奨化の期間中、古いインターフェースにも新しいインターフェースと同じ入力検証を適用する。移行期間中だけ検証が緩い経路が残ると、そこが攻撃対象になる
- リファクタリングで認証・認可・入力検証のコードを触るときは、通常のリファクタリング以上に慎重にテストを増やす。挙動を変えないつもりの変更が、意図せずチェックを弱める場合がある
- `TODO`/`FIXME`コメントに、修正されていない既知の危険（検証未実装など）を書く場合、その情報が公開リポジトリや配布物に含まれてよいかを確認する。攻撃者へのヒントになりうる

---

## 14.15 テスト方法

重複排除やリファクタリングでは、変更前後で挙動が変わっていないことをテストで確認する。

```python
import pytest

from samples.python.health_checks import DEFAULT_TIMEOUT_SECONDS, check_service


@pytest.mark.parametrize(
    ("service", "expected_timeout"),
    [("web", 5), ("db", 10), ("cache", 3), ("unknown-service", 5)],
)
def test_check_service_resolves_timeout_by_service(service, expected_timeout, monkeypatch):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["timeout"] = kwargs.get("timeout")

        class _Result:
            returncode = 0

        return _Result()

    monkeypatch.setattr("samples.python.health_checks.subprocess.run", fake_run)
    result = check_service("web01.example.invalid", service)

    assert result.timeout_seconds == expected_timeout
    assert "--max-time" in captured["cmd"]
    assert str(expected_timeout) in captured["cmd"]


def test_deprecated_check_web_still_works_but_warns(monkeypatch):
    from samples.python.health_checks import check_web

    monkeypatch.setattr(
        "samples.python.health_checks.subprocess.run",
        lambda *a, **k: type("R", (), {"returncode": 0})(),
    )
    with pytest.warns(DeprecationWarning):
        assert check_web("web01.example.invalid") is True
```

`test_deprecated_check_web_still_works_but_warns` は、後方互換性のテストの典型例である。
「警告が出ること」と「結果が変わらないこと」の両方を確認する。
どちらか一方だけでは、非推奨化の意図（動き続けるが移行を促す）を検証したことにならない。

---

## 章末問題

### 問題1

`chk1`、`process` のような名前が保守性を下げる理由を、レビューする側の視点で説明せよ。

### 問題2

似た処理を重複させたまま残すべき場合があるとすれば、どのような条件のときか説明せよ。

### 問題3

マジックナンバーと設定値の違いを、「値が変わる理由」の観点から説明せよ。

### 問題4

依存関係を`==`で完全固定した場合に生じるリスクを一つ挙げ、対策を述べよ。

### 問題5

リファクタリング前にテストが無い場合、まず何をすべきか、その理由とともに述べよ。

---

## 解答と解説

### 問題1

名前から処理内容を推測できないと、レビューする側は実装を最初から最後まで読まないと妥当性を判断できない。
名前が適切なら、実装の細部を読む前に「意図どおりか」の見当がつき、レビューの負担が下がる。

### 問題2

将来、変更される理由が異なる可能性が高い場合である。
現時点でロジックが似ていても、片方だけ仕様変更が入る見込みが高いなら、無理に共通化すると条件分岐だらけの関数になり、かえって保守性が下がる。

### 問題3

マジックナンバーは、意味を明示していないだけで、値自体はコードの一部として固定でよい場合が多い（名前付き定数で解決する）。
設定値は、実行環境やチームの方針によって変わりうる値であり、コードの外（設定ファイル、環境変数）に置くべきものである。

### 問題4

リスク: 既知の脆弱性を修正した新バージョンが出ても、固定したままだと自動的には取り込まれない。
対策: 完全固定を維持しつつ、定期的な棚卸し(依存関係の脆弱性スキャン、更新確認)を運用に組み込む。

### 問題5

現状の挙動をそのまま固定する特性化テストを先に書く。
テストが無い状態でリファクタリングすると、変えていないつもりの挙動変化を検出する手段が無く、リファクタリングそのものが新たなバグの原因になりうる。

---

## 実装演習

### 演習A

`samples/python/14_health_checks.py` に `check_queue`（サービス名`"queue"`、既定タイムアウト15秒）を追加せよ。
`DEFAULT_TIMEOUT_SECONDS`辞書へ値を追加するだけで済む設計になっていることを確認せよ。

### 演習B

14.12の悪いコードから、責務ごとに関数を分割し、`chk1`/`chk2`/`process`に代わる名前を提案して書き換えよ。
書き換え後、14.15のテストパターンを参考に、正常系・異常系のテストを最低2つ追加せよ。

### 演習C

架空のCLIオプション`--legacy-mode`が非推奨だと仮定し、14.8の非推奨化の手順（新旧併存、警告、移行期間、削除）を、実際のコード変更案として4段階（4つのコミット相当）に分けて書け。
各段階でどのテストが必要かも述べること。

---

## 次章予告

第15章では、ここまでの知識を使い、疎通確認、ディスク監視、ログ検索、証明書期限確認など11個の運用題材を実装する。
言語適性（付録A）に応じて主実装言語を選び、テスト（第13章）と保守性（本章）を備えた形で仕上げる。


---


<!-- SOURCE: 15_infrastructure_automation_practice.md -->

# 第15章 インフラ自動化の実践

## 学習目標

この章を終えると、次ができるようになる。

- 運用題材を要件・入出力・失敗時・dry-run・再実行性まで落として実装できる
- Python / Bash / PowerShell の適性に応じて主実装言語を選べる
- `opsctl` の終了コード、設定ファイル、ログ規約に沿ったサブコマンドを運用できる
- 破壊的操作を、確認とロールバックを前提に扱える

前提:

- 第1章〜第14章の内容
- `config/opsctl.yaml` と `config/hosts.txt` がリポジトリ直下にあること
- 作業ディレクトリは `infra_scripting_coding_guide/` を想定する

> **警告**: 本章の削除、設定上書き、バックアップ整理、サービス再起動系の例は学習用である。対象パスは `./work`、`./backups`、`/tmp/opsctl-lab` などに限定している。本番パスへ向けて `--execute` を付けないこと。

サンプルは本番環境でそのまま安全とは限らない。投入前に付録Cのチェックリストを通すこと。

---

## 基本概念

**インフラ自動化スクリプト**は、手作業の運用手順を、入力・処理・出力・失敗時挙動・再実行性まで固定した実行可能手続きである。

本章では、前章までの部品を組み合わせ、言語適性に応じて題材を実装する。各題材は「動くデモ」ではなく、dry-run、終了コード、監査可能なログを備えた運用単位として扱う。

### 悪いコードの型（共通）

```bash
# 確認なし、ログなし、終了コードなし、パス検証なし
find /var/log -mtime +30 -delete
```

問題点:

- dry-runがない
- 対象範囲が広い
- 失敗しても気づきにくい
- 再実行や監査ができない

### 改善後の型（共通）

1. 対象パスを allowlist で制限する
2. 既定は報告のみ（`--execute` で実作業）
3. 実施前後をCSVまたはログに残す
4. 部分失敗は非0終了コードにする

具体例は 15.4（古いファイル整理）の `samples/python/15_cleanup_old.py` を参照する。

---

## 15.0 章の進め方と共通規約

各節は次の項目で揃える。

1. 要件
2. 入力
3. 出力
4. 処理フロー
5. エラー処理
6. ログ
7. 設定ファイル
8. dry-run
9. 再実行性
10. テスト
11. 実行例
12. 運用上の注意点

共通終了コード（README / 付録B）:

| コード | 意味 |
|--------|------|
| 0 | 成功（警告方針は各コマンドで定義） |
| 1 | 使い方・設定誤り |
| 2 | 実行時エラー（部分失敗を含む） |
| 3 | 監視上の CRITICAL |
| 4 | タイムアウト |
| 130 | Ctrl+C |

統合入口（任意）:

```bash
python3 samples/python/15_opsctl_dispatch.py --help
```

各サブコマンドは独立スクリプトとしても動く。学習時は独立実行を先に確認する。

ラボ用ディレクトリの準備:

```bash
mkdir -p work/logs work/tmp work/quarantine work/reports backups reports /tmp/opsctl-lab
printf 'ERROR connection refused\nINFO started\n' > work/logs/app.log
printf 'old\n' > work/tmp/stale.tmp
touch -d '40 days ago' work/tmp/stale.tmp 2>/dev/null || touch -t 202601010000 work/tmp/stale.tmp
```

---

## 15.1 複数サーバーへの疎通確認

主言語: Python（並列と集計が楽）。補助: Bash。

実装: `samples/python/15_ping_check.py`、`samples/bash/15_ping_check.sh`、基礎版 `samples/python/02_ping_check.py`

### 要件

1. `config/hosts.txt` のホストへ疎通確認する
2. 1ホストあたりのタイムアウトと全体デッドラインを持つ
3. 重要ホスト不通は CRITICAL（終了コード3）として扱う
4. 結果をCSVへ残す
5. dry-runでは ping を送らず予定だけ出す

### 入力

- `--hosts-file` または設定の `ping_check.hosts_file`
- `--timeout`、`--max-workers`、`--deadline-seconds`
- `ping_check.critical_hosts`

### 出力

- CSV: `host,ok,detail,elapsed_ms,critical`
- stderr: 構造化に近いテキストログ
- 終了コード: 全成功0、部分失敗2、重要ホスト失敗3

### 処理フロー

```text
load config and hosts
if dry-run:
  log each planned ping; write dry-run rows; exit 0
ping hosts with limited workers under deadline
classify failures; mark critical hosts
write CSV
return exit code
```

### エラー処理

- ホスト一覧空 / 不正行 → 終了コード1
- `ping` コマンド不存在 → そのホストを ERROR、全体は2
- 全体デッドライン超過 → 未完了を TIMEOUT 扱い、必要なら4または2

### ログ

`INFO host=... ok=... elapsed_ms=...` を stderr へ出す。

### 設定ファイル

```yaml
ping_check:
  hosts_file: ./config/hosts.txt
  timeout_seconds: 3
  max_workers: 8
  deadline_seconds: 60
  critical_hosts:
    - db01.example.invalid
```

### dry-run

実際の ICMP を送らない。レポートには `ok=dry-run` を書く。

### 再実行性

読み取りのみ。何度実行しても副作用はない。

### テスト

- 空ファイルで終了コード1
- dry-runで外部コマンド未呼び出し
- critical ホスト不通で終了コード3

### 実行例

```bash
python3 samples/python/15_ping_check.py --dry-run --report reports/ping-dry.csv --verbose

python3 samples/python/15_ping_check.py \
  --hosts-file config/hosts.txt \
  --timeout 2 \
  --report reports/ping.csv
echo $?
```

Bash補助:

```bash
bash samples/bash/15_ping_check.sh --hosts-file config/hosts.txt --report reports/ping-bash.csv --dry-run
```

### 運用上の注意点

- ICMPが塞がれた網では失敗が増える。TCPポート確認へ切り替える判断が必要
- 大量ホストへの無計画な並列pingは監視やセキュリティ機器に検知されることがある
- macOSとLinuxで `ping -W` の単位が違う。可搬性が要るならPython版を主にする

---

## 15.2 ディスク使用率監視

主言語: Bash / PowerShell（OSの容量情報取得が素直）。補助: Pythonの判定関数（第4章、第13章）。

実装: `samples/bash/15_disk_check.sh`、`samples/powershell/15_disk_check.ps1`

### 要件

1. 指定パスの使用率を取得する
2. warn / crit 閾値で分類する
3. CRITICALが1つでもあれば終了コード3
4. 取得失敗は継続し、終了コード2
5. dry-runではレポート書き込みとアラートコマンドを行わない

### 入力

- `--paths`（複数可、既定 `/`）
- `--warn`、`--crit`
- `--report`、`--alert-command`（信頼できる固定コマンドのみ）

### 出力

- CSV: `path,percent,status,detail`
- 終了コード 0 / 2 / 3

### 処理フロー

```text
validate thresholds
for path in paths:
  get usage via df / Get-PSDrive
  classify
  append row
if not dry-run: write report; maybe run alert command
compute exit code
```

### エラー処理

- 閾値の型・大小不正 → 1
- パスが存在しない / df失敗 → その行 ERROR、全体2
- alertコマンド失敗 → 2（監視通知失敗も失敗）

### ログ

`run_id` 付きで stderr へ INFO/ERROR。

### 設定ファイル

```yaml
defaults:
  disk_warn_percent: 80
  disk_crit_percent: 90
```

### dry-run

閾値判定までは行う。ファイル書き込みと `--alert-command` はスキップ。

### 再実行性

読み取り中心。レポートはタイムスタンプ付きパスを推奨。

### テスト

```bash
bash samples/bash/15_disk_check.sh --paths / --warn 80 --crit 90 --dry-run --verbose
```

境界値は第4章の `classify` を単体テストする。

### 実行例

```bash
bash samples/bash/15_disk_check.sh \
  --paths / --paths /var \
  --warn 80 --crit 90 \
  --report reports/disk.csv
```

```powershell
pwsh samples/powershell/15_disk_check.ps1 -Paths C:\ -Warn 80 -Crit 90 -DryRun
```

### 運用上の注意点

- `/` だけ見てデータパーティションを見落とさない
- `--alert-command` に利用者入力を連結しない（コマンドインジェクション）
- inode不足は使用率と別問題。必要なら別チェックを足す

---

## 15.3 ログファイル検索

主言語: Python（正規表現、大きなファイルのストリーム処理）。

実装: `samples/python/15_log_search.py`

### 要件

1. 複数ディレクトリ配下のログを正規表現で検索する
2. ファイル全体をメモリに載せない
3. バイナリや権限エラーは警告してスキップする
4. マッチ上限とファイル上限を持つ
5. dry-runでは対象ファイル一覧だけ出す

### 入力

- `--pattern`（必須）
- `--target-dir`、`--glob`（既定 `*.log`）
- `--max-files`、`--max-matches`
- 設定 `log_search`

### 出力

- CSV: `path,line_no,line`
- マッチ0でも検索成功なら終了コード0
- 対象ディレクトリ不正は1、読み取り多発失敗は2

### 処理フロー

```text
compile regex
enumerate files under target dirs with glob, up to max-files
if dry-run: list files; exit
for each file, stream lines; collect matches up to max-matches
write report
```

### エラー処理

- 不正正規表現 → 1
- ファイル上限超過 → 警告し打ち切り（仕様としてINFO）
- 個別ファイルの UnicodeDecodeError → 置換またはスキップをログ

### ログ

検索開始、スキップ理由、マッチ件数を INFO/WARNING で残す。

### 設定ファイル

```yaml
log_search:
  target_dirs:
    - ./work/logs
  max_files: 200
  max_matches: 5000
```

### dry-run

パターン適用前に、走査対象ファイルを列挙する。

### 再実行性

読み取りのみ。

### テスト

小さなログを `work/logs` に置き、既知行がマッチすることを確認する。

### 実行例

```bash
python3 samples/python/15_log_search.py \
  --pattern 'ERROR' \
  --target-dir work/logs \
  --report reports/log-search.csv \
  --verbose

python3 samples/python/15_log_search.py \
  --pattern 'ERROR' \
  --target-dir work/logs \
  --dry-run
```

### 運用上の注意点

- 本番ログに個人情報が含まれる場合、レポート保管場所と権限を制限する
- 巨大ディレクトリでは `--max-files` を先に絞る
- 文字コード不明ログは別エンコーディング指定が必要になることがある

---

## 15.4 古いファイルの整理

主言語: Python。

実装: `samples/python/15_cleanup_old.py`

> **警告**: `--action delete --execute` は復元できない削除を行う。既定は dry-run（報告のみ）である。まず `--action quarantine` で隔離運用する。

### 要件

1. 指定日数より古いファイルを候補にする
2. 対象ルートはラボ用パスに限定する（`./work`、`./backups`、`/tmp/opsctl-lab`）
3. 既定は実行せず報告のみ。`--execute` で実作業
4. 削除より隔離を推奨する
5. 実施結果をCSVに残す

### 入力

- `--target-dir`、`--max-age-days`、`--extension`
- `--action quarantine|delete`
- `--quarantine-dir`、`--report`、`--execute`

### 出力

- CSV: `path,action,status,detail`
- 終了コード: 設定誤り1、部分失敗2、成功0

### 処理フロー

```text
validate roots are inside lab allowlist
list candidates by mtime and extension
if not --execute: write planned actions; exit 0
for each candidate:
  quarantine (move) or delete
  append audit row
```

### エラー処理

- allowlist外のパス → 1（拒否）
- 移動/削除失敗 → その行 ERROR、全体2
- 隔離先が対象配下で循環する場合 → 1

### ログ

計画件数、実施件数、拒否パスを残す。

### 設定ファイル

```yaml
cleanup:
  target_dirs:
    - ./work/tmp
  max_age_days: 30
  extensions:
    - ".tmp"
    - ".log"
  quarantine_dir: ./work/quarantine
```

### dry-run

フラグ名は「実行しないのが既定」。`--execute` が無い限り変更しない。

### 再実行性

隔離済みファイルは対象から消える。削除は冪等に近いが、監査CSVは追記または時刻付き新規にする。

### テスト

```bash
python3 samples/python/15_cleanup_old.py --target-dir work/tmp --max-age-days 30 --verbose
# 変更なし

python3 samples/python/15_cleanup_old.py \
  --target-dir /etc --execute
# 拒否され終了コード1であること
```

### 実行例

```bash
python3 samples/python/15_cleanup_old.py \
  --target-dir work/tmp \
  --max-age-days 30 \
  --action quarantine \
  --report reports/cleanup.csv

python3 samples/python/15_cleanup_old.py \
  --target-dir work/tmp \
  --action quarantine \
  --execute \
  --report reports/cleanup-exec.csv
```

### 運用上の注意点

- バックアップ保持と掃除の保持日数を矛盾させない
- cron化する場合も最初の数週間は quarantine のみ
- NFSや共有ディスクでは mtime の解釈差に注意

---

## 15.5 ユーザーアカウント棚卸し

主言語: PowerShell（Windowsローカルユーザー）。補助: Bash（Linuxの passwd 系）。

実装: `samples/powershell/15_user_audit.ps1`、`samples/bash/15_user_audit.sh`

### 要件

1. 有効アカウントを一覧化する
2. パスワード期限なし、長期未ログイン、許可外シェルなどを検出する
3. アカウント変更は行わない（読み取り専用）
4. リスク検出時は終了コード3（方針で2でもよい。実装に従う）

### 入力

- 非アクティブ日数閾値
- 除外アカウント
- Linuxなら `uid_min`、`allowed_shells`

### 出力

- CSV: アカウント名、状態、findings
- dry-runでは列挙予定のみ

### 処理フロー

```text
enumerate accounts
filter excluded / system accounts
evaluate findings
write report
exit non-zero if findings exceed policy
```

### エラー処理

- コマンド非対応OS → 1（案内メッセージ）
- 列挙権限不足 → 2

### ログ

監査対象件数と、検出した finding を INFO/WARNING で残す。パスワード自体は出さない。

### 設定ファイル

```yaml
user_audit:
  uid_min: 1000
  allowed_shells:
    - /bin/bash
    - /usr/sbin/nologin
    - /bin/false
  inactive_days_warn: 90
```

### dry-run

アカウントへの問い合わせをせず、対象名の列挙方針だけを出すか、読み取りのみでレポートを書かない実装にする。各スクリプトのヘルプに従う。

### 再実行性

読み取りのみ。

### テスト

除外リストに入れたアカウントが findings に出ないこと。

### 実行例

```powershell
pwsh samples/powershell/15_user_audit.ps1 -DryRun
pwsh samples/powershell/15_user_audit.ps1 -InactiveDaysWarn 90 -ReportPath work/reports/user_audit.csv
```

```bash
bash samples/bash/15_user_audit.sh --dry-run
bash samples/bash/15_user_audit.sh --report reports/user-audit.csv
```

### 運用上の注意点

- ドメインアカウントは別API（Get-ADUserなど）が必要
- 棚卸し結果は権限情報を含む。レポートのACLを制限する
- 自動無効化までは本章の範囲外。変更は承認後の別手順にする

---

## 15.6 サービス稼働確認

主言語: Bash（systemd）、PowerShell（Windowsサービス）。

実装: `samples/bash/15_service_check.sh`、`samples/powershell/15_service_check.ps1`

### 要件

1. 指定サービスの稼働状態を確認する
2. 停止を検出したら終了コード3（または2。実装の定義に従う）
3. 再起動オプションがある場合は明示フラグでのみ実行する
4. dry-runでは再起動しない

> **警告**: `--restart-on-failure` はサービスに影響する。本番では変更管理なしで定期実行しない。

### 入力

- `--service`（複数）
- init系（systemd/sysv）または Windows サービス名
- `--restart-on-failure`、`--report`、`--dry-run`

### 出力

- CSV: `service,status,detail`
- 終了コード

### 処理フロー

```text
for service:
  query status
  if inactive and restart requested and not dry-run:
    restart and re-query
  record result
write report
```

### エラー処理

- 未知サービス → ERROR行、全体2または3
- 権限不足 → 2
- 再起動失敗 → 3

### ログ

照会結果と、再起動を行ったかどうかを残す。

### 設定ファイル

```yaml
service_check:
  services:
    - sshd
    - cron
```

### dry-run

状態取得は可。再起動は不可。

### 再実行性

確認のみなら安全。再起動付きは「停止時のみ起動」にすると冪等に近づく。

### テスト

存在しないサービス名で ERROR になること。dry-runで restart が呼ばれないこと。

### 実行例

```bash
bash samples/bash/15_service_check.sh --service sshd --dry-run --verbose
bash samples/bash/15_service_check.sh --service sshd --service cron --report reports/services.csv
```

```powershell
pwsh samples/powershell/15_service_check.ps1 -Service Spooler -DryRun
```

### 運用上の注意点

- コンテナや systemd user サービスでは単位名が異なる
- クラスタ管理下のサービスをスクリプトで単独再起動しない
- 起動直後の一時的な inactive を CRITICAL にしないための猶予が必要な場合がある

---

## 15.7 設定ファイルの一括変更

主言語: Python。

実装: `samples/python/15_config_bulk_edit.py`、`samples/python/15_config_patch.py`

> **警告**: 一括置換は影響範囲が広い。必ず差分を確認し、バックアップを取り、変更管理の承認後に `--execute` する。

### 要件

1. 複数ファイルへパターン置換を適用する
2. 書き込み前にタイムスタンプ付きバックアップを取る
3. 既定は dry-run（差分表示のみ）
4. 対象はラボ用ルートに限定する
5. 結果CSVを残す

### 入力

- 対象ディレクトリ、ファイルglob
- 置換ルール（CLIまたはYAMLルールファイル）
- `--execute`

### 出力

- unified diff（dry-run）
- バックアップディレクトリ
- CSV: `path,changed,status`

### 処理フロー

```text
validate roots
load rules
for each file:
  render new content
  if unchanged: skip
  if not execute: show diff
  else: backup; atomic write
```

### エラー処理

- ルール不正 → 1
- バックアップ失敗 → 中断（2）。中途半端な適用を避ける
- 個別書き込み失敗 → 2、適用済み一覧をレポート

### ログ

変更予定数、適用数、バックアップ先を出す。

### 設定ファイル

ルール例は `samples/shared/config_patch_rules.example.yaml` を参照。

### dry-run

書き込みもバックアップも行わない実装（`15_config_patch.py`）と、方針をヘルプで明示する。

### 再実行性

既に置換済みなら差分ゼロでスキップできるルールにする。

### テスト

一時ディレクトリにサンプル設定を置き、dry-run差分 → execute → 再実行で差分ゼロを確認する。

### 実行例

```bash
python3 samples/python/15_config_bulk_edit.py --help
python3 samples/python/15_config_patch.py --help
```

ラボで試す場合も、先にコピーを `work/` 配下へ置いてから対象にする。

### 運用上の注意点

- テンプレート管理（Ansible等）があるなら、そちらの正本を先に直す
- バイナリや証明書ファイルを置換対象に含めない
- ロールバックはバックアップからの復元手順を先に書いてから実行する

---

## 15.8 APIから情報を取得してCSVに出力

主言語: Python。補助: PowerShell。

実装: `samples/python/15_api_to_csv.py`、`samples/python/15_api_export.py`、`samples/powershell/11_api_export.ps1`

### 要件

1. 認証付きHTTP GETでページネーションを辿る
2. タイムアウト、リトライ、429尊重を行う
3. 結果をCSVへ書く
4. トークンは `OPSCTL_API_TOKEN` から読む
5. 既定ベースURLは `https://api.example.invalid`（到達しない）

### 入力

- `--base-url`、`--endpoint`、`--config`
- 環境変数 `OPSCTL_API_TOKEN`
- `--timeout`、`--report`、`--dry-run`

### 出力

- CSV（設定の fields）
- 終了コード 0/1/2/4

### 処理フロー

```text
load config; require token unless dry-run
if dry-run: print planned requests; exit 0
for page in pages:
  GET with timeout and retry
  yield rows
write CSV
```

### エラー処理

- トークン未設定 → 1
- 4xx（401/403等）→ 2（リトライしない）
- 5xx/429 → リトライ後に失敗なら2または4
- JSON不正 → 2

### ログ

URLにトークンを出さない。`Authorization` はマスクする（第9章、第11章）。

### 設定ファイル

```yaml
api:
  base_url: "https://api.example.invalid"
api_to_csv:
  endpoint: /v1/incidents
  fields:
    - incident_id
    - severity
    - host
    - opened_at
```

### dry-run

ネットワーク接続せず、組み立てたURLとページ方針だけを出す。

### 再実行性

同じAPIを再取得する。出力は時刻付きファイルにして上書きしない。

### テスト

`responses` や手書きモックでページ2枚と429を擬似する（第11章、第13章）。

### 実行例

```bash
python3 samples/python/15_api_to_csv.py --dry-run --verbose --output reports/incidents.csv

export OPSCTL_API_TOKEN='replace-me'
python3 samples/python/15_api_to_csv.py \
  --base-url "https://api.example.invalid" \
  --output reports/incidents.csv
# example.invalid は名前解決に失敗するのが正常な学習結果
```

### 運用上の注意点

- 利用規約とレート制限を確認する
- トークンをシェル履歴に残さない（`export` の運用ルールを決める）
- ページサイズを大きくしすぎるとメモリと相手負荷が増える

---

## 15.9 バックアップ処理

主言語: Bash（tarが強い） / Python（検証と整理）。

実装: `samples/bash/15_backup.sh`、`samples/python/15_backup.py`

> **警告**: 保持期間を超えたバックアップ削除は破壊的である。`--prune` や削除処理は dry-runで対象確認してから行う。

### 要件

1. ソースディレクトリをタイムスタンプ付きアーカイブにする
2. バックアップ先は `./backups` など明示パス
3. 保持日数を超えた古い世代を整理できる
4. dry-runでは作成も削除もしない
5. 可能ならチェックサムを記録する

### 入力

- `--source`（複数可）
- `--backup-dir`、`--retention-days`
- `--prune`、`--dry-run`

### 出力

- `backups/backup-YYYYMMDDTHHMMSS.tar.gz` など
- マニフェスト（任意）
- 終了コード

### 処理フロー

```text
validate sources exist
if dry-run: show archive name and prune candidates; exit
create archive atomically (temp then rename)
write checksum
if prune: delete older than retention
```

### エラー処理

- ソース無し → 1
- ディスク満杯 → 2、不完全ファイルを残さない
- 削除失敗 → 2（新規バックアップ成功と分けて報告）

### ログ

アーカイブパス、サイズ、削除した世代を残す。

### 設定ファイル

```yaml
backup:
  source_dirs:
    - ./config
  retention_days: 14
paths:
  backup_dir: ./backups
```

### dry-run

作成予定名と prune 候補だけ表示する。

### 再実行性

毎回新しいタイムスタンプファイルを作る。pruneは保持政策に対して収束する。

### テスト

小さな `config/` をソースに dry-run → 実行 → ファイル存在確認。

### 実行例

```bash
bash samples/bash/15_backup.sh --source config --backup-dir backups --dry-run
bash samples/bash/15_backup.sh --source config --backup-dir backups --retention-days 14

python3 samples/python/15_backup.py --dry-run --verbose
```

### 運用上の注意点

- バックアップ成功とリストア成功は別である。定期的に復元試験する
- 秘密鍵や `.env` を同じtarに入れるなら権限と保管先を分ける
- リモートコピーは本章の次段（rclone等）として別要件にする

---

## 15.10 証明書期限確認

主言語: Python。

実装: `samples/python/15_cert_check.py`

### 要件

1. ホスト:ポートへTLS接続し、証明書の残日数を計算する
2. warn / crit 日数で分類する
3. ローカルPEM（`--cert-file`）でも検証できる
4. 1件でも crit なら終了コード3
5. dry-runでは接続せず対象一覧を出す

### 入力

- `--host host:port`（複数）
- `--cert-file`
- `--warn-days`、`--crit-days`、`--timeout`
- 設定 `cert_check`

### 出力

- CSV: `target,not_after,days_left,status,detail`
- 終了コード 0/1/2/3

### 処理フロー

```text
load targets
if dry-run: list targets; exit 0
for target:
  fetch cert (TLS or PEM)
  compute days_left
  classify
write report
```

### エラー処理

- 接続失敗 → ERROR行、全体2（全件ERRORなら2）
- 証明書解析失敗 → 2
- crit 到達 → 3

### ログ

ホスト、残日数、status を出す。秘密鍵は扱わない。

### 設定ファイル

```yaml
cert_check:
  targets:
    - host: web01.example.invalid
      port: 443
  warn_days: 30
  crit_days: 7
```

### dry-run

TLS接続しない。

### 再実行性

読み取りのみ。

### テスト

自己署名PEMを `--cert-file` で渡し、残日数計算を固定時計で検証する（第14章の `14_cert_report.py` も参照）。

### 実行例

```bash
python3 samples/python/15_cert_check.py --dry-run --verbose

# ラボのPEMがある場合
python3 samples/python/15_cert_check.py \
  --cert-file /tmp/opsctl-lab/example.pem \
  --warn-days 30 --crit-days 7 \
  --report reports/certs.csv
```

### 運用上の注意点

- SNIが必要なサイトでは server_hostname を正しく渡す
- 中間証明書不足はブラウザと結果が違うことがある
- 自動更新（ACME）環境では、本チェックは監視であり発行そのものではない

---

## 15.11 定期レポート生成

主言語: Python。

実装: `samples/python/15_report.py`

### 要件

1. ping / disk / cert などのCSV結果を集約する
2. セクションごとに件数と最悪ステータスを要約する
3. Markdownまたはテキストレポートを `reports/` へ書く
4. dry-runでは集約結果をstderrに出しファイルを書かない
5. メール送信は本文では「宛先設定のみ」とし、送信は別途承認付きにする

### 入力

- `--report-dir`（入力CSV置き場）
- `--section`（複数）
- `--output`
- 設定 `report.sections`

### 出力

- サマリーレポートファイル
- 終了コード: 集約成功0、入力欠落は方針により0（欠落をWARNING）または2

### 処理フロー

```text
discover latest CSVs per section
aggregate counts
render report
if dry-run: print; else write output
```

### エラー処理

- 未知セクション → 1
- CSV破損 → そのセクション ERROR、全体2

### ログ

読んだファイルパスと集計件数を残す。

### 設定ファイル

```yaml
report:
  sections:
    - ping
    - disk
    - cert
  recipients:
    - ops-team@example.invalid
```

### dry-run

ファイルを書かない。

### 再実行性

出力は時刻付きファイル名にすると安全。

### テスト

fixture CSVを `work/reports` に置き、要約行が期待どおりか検証する。

### 実行例

```bash
python3 samples/python/15_report.py --dry-run --verbose
python3 samples/python/15_report.py \
  --report-dir reports \
  --output reports/summary.md
```

### 運用上の注意点

- 定期実行は「各チェック成功後にレポート」の依存順を決める
- 受信者リストをコードに直書きしない
- 要約だけ送ると詳細調査ができない。CSV保管期間を別に決める

---

## 15.12 題材と言語適性の整理

| 題材 | 主言語 | 理由 |
|------|--------|------|
| 疎通確認 | Python | 並列、集計、テスト |
| ディスク監視 | Bash / PowerShell | OSコマンドが近い |
| ログ検索 | Python | 正規表現とストリーム |
| 古いファイル整理 | Python | パス検証と安全策 |
| ユーザー棚卸し | PowerShell（Win）/ Bash（Linux） | 管理APIが近い |
| サービス確認 | Bash / PowerShell | サービス管理が近い |
| 設定一括変更 | Python | 差分、テスト、原子的更新 |
| API→CSV | Python | HTTPライブラリとテスト |
| バックアップ | Bash / Python | tarと検証の役割分担 |
| 証明書期限 | Python | TLSと日付計算 |
| レポート | Python | 複数形式の集約 |

---

## 15.13 セキュリティ上の注意点（章共通）

- 秘密情報を設定ファイルとレポートに書かない
- 破壊的操作は allowlist、dry-run既定、監査CSVを揃える
- アラート用シェルコマンドに外部入力を連結しない
- レポートにパスワードやトークンが混入していないか定期点検する

---

## 15.14 テスト方法（章共通）

1. 各スクリプトの `--help` が落ちないこと
2. dry-runが副作用ゼロであること
3. 不正入力で終了コード1であること
4. ラボパス外への変更が拒否されること（cleanup / config-patch）
5. pytest / シェルテストで純粋関数と集計を固定すること（`tests/`）

例:

```bash
cd infra_scripting_coding_guide
python3 -m pytest tests/ -q
bash samples/bash/15_disk_check.sh --paths / --dry-run
python3 samples/python/15_cleanup_old.py --target-dir work/tmp
```

---

## 章末問題

1. 疎通確認で「重要ホスト」をCRITICALにする要件を、終了コード表に落として書け。
2. cleanup を既定 dry-run にする理由を、運用事故のシナリオで説明せよ。
3. ディスク監視の `--alert-command` が危険になりうる入力例を一つ書け。
4. API取得で 401 をリトライすべきでない理由を述べよ。
5. バックアップの「取得成功」と「リストア成功」を分ける監視項目を提案せよ。

## 解答と解説

1. 重要ホスト不通 → 3。それ以外の不通のみ → 2。全成功 → 0。
2. cronや引数ミスで本番ディレクトリを消す事故を、報告モードで止められる。
3. `'; rm -rf /` を連結される、または利用者入力をそのまま `sh -c` に渡す。
4. 認証失敗は再試行で治らない。ロックや監査ノイズを増やす。
5. 取得ジョブの終了コード、アーカイブサイズ下限、月次リストア試験の成功記録。

## 実装演習

### 演習A

`15_ping_check.py` に「連続失敗がN回でCRITICAL」を足す設計だけ書け（実装は任意）。状態ファイルの置き場と再実行性も述べる。

### 演習B

`work/logs` に日本語を含むログを置き、`15_log_search.py` で検索せよ。文字コード問題が起きたら方針を記録する。

### 演習C

`15_opsctl_dispatch.py` 経由で `disk-check` と `cert-check` の dry-run を連続実行し、終了コードの伝播を確認せよ。

---

## 次章予告

第16章では、これらのスクリプトを秘密情報なしでGit管理し、レビューとリリース、ロールバック可能な共同開発へつなぐ。


---


<!-- SOURCE: 16_git_and_collaboration.md -->

# 第16章 Gitと共同開発

## 学習目標

この章を終えると、次ができるようになる。

- リポジトリ、commit、branch、merge、pull requestの役割を、`opsctl` の開発フローに沿って説明できる
- コンフリクトの発生条件を理解し、安全に解消できる
- `.gitignore` を設計し、秘密情報や生成物をリポジトリに含めない運用ができる
- 秘密情報を誤ってコミットした場合に、履歴からの除去とローテーションを実施できる
- コードレビューの観点を持ち、レビューを通過しやすい変更単位を作れる
- リリースタグとCHANGELOGを運用し、必要に応じてロールバックできる
- READMEとCHANGELOGを、利用者と開発者それぞれの目的に沿って書き分けられる

前提: 第1章（終了コード）、第9章（ログ）、第10章（秘密情報の扱い）、第12章（CLI設計）。
Git本体の詳細なコマンドリファレンスは扱わない。ここでは、運用スクリプトを複数人・複数環境で安全に育てるための最小限の型を扱う。

サンプルコードと運用フローは学習用である。
実際のチームでは、社内の変更管理規程、ブランチ保護ルール、レビュー必須人数などの組織的な取り決めに従うこと。

---

## 基本概念

本章の中心概念は次のとおりである。

- **バージョン管理**: 変更履歴を記録し、任意時点を再現できるようにする仕組み
- **ブランチとマージ**: 並行作業を分離し、後で統合する単位
- **pull request**: 変更の提案、レビュー、履歴上の議論の場
- **リリースとロールバック**: 動いている版を固定し、必要なら戻す運用

詳細は以降の節で、`opsctl` を題材に具体化する。

---

## 16.1 バージョン管理とは

**バージョン管理**は、ファイルの変更履歴を時系列で記録し、任意の時点の状態を再現・比較・復元できるようにする仕組みである。

運用スクリプトにバージョン管理が要るのは、単なる保険ではない。

- 誰が、いつ、なぜその変更を入れたかを追跡できる（障害調査、監査対応）
- 変更前の状態にいつでも戻せる（第8章のロールバックの、コード自体への適用）
- 複数人が同時に同じスクリプトへ手を入れても、変更を統合できる
- 本番に適用したコードのバージョンと、手元の変更を区別できる

バージョン管理をしない運用（`opsctl_v2_final_fix.py` のようなファイル名での多重保存）は、どれが本番稼働中の版か分からなくなり、障害時の切り戻しが著しく遅れる。

**Git**は、分散型バージョン管理システムである。
中央サーバーが一時的に落ちても、各自の手元に履歴の複製（クローン）があるため、作業を止めずに済む。
本章では、Gitを前提に、`opsctl` リポジトリの運用を具体例として進める。

---

## 16.2 リポジトリの基本

**リポジトリ（repository）**は、ファイルとその変更履歴一式を保持する単位である。

`opsctl` リポジトリの初期化から最初のコミットまで:

```bash
mkdir opsctl && cd opsctl
git init
git config user.name "Ops Taro"
git config user.email "ops-taro@example.invalid"

mkdir -p samples/python samples/bash samples/powershell config
echo "config/opsctl.yaml" > .gitignore   # 後で16.6節のとおり書き直す

git add .
git commit -m "chore: initialize opsctl repository"
```

よく使う基本コマンドと役割を、`opsctl` の作業に沿って整理する。

| コマンド | 役割 |
|----------|------|
| `git status` | 変更・未追跡ファイルの一覧を確認する |
| `git diff` | 作業ツリーとステージ済みの差分を確認する |
| `git add <path>` | 変更をステージング（次のcommitに含める）する |
| `git commit -m "<message>"` | ステージ済みの変更を1つの履歴として記録する |
| `git log --oneline` | commit履歴を要約して確認する |
| `git remote -v` | 連携しているリモートリポジトリを確認する |
| `git push` | ローカルのcommitをリモートへ反映する |
| `git pull` | リモートの変更をローカルへ取り込む |
| `git clone <url>` | リモートリポジトリを手元に複製する |

**作業ツリー（working tree）**、**ステージングエリア（index）**、**リポジトリ（履歴）**の3層構造を意識すると、`add` と `commit` の違いが分かりやすい。

```text
作業ツリー          git add          ステージングエリア        git commit          履歴
(編集中のファイル)  ------------->  (次にcommitする内容)  -------------->  (確定した1つの記録)
```

`git add` は「次のcommitに何を含めるか」を選ぶ操作であり、ファイルを保存する操作ではない。
編集後に `git add` を忘れると、意図した変更がcommitに含まれない。

---

## 16.3 commit: 変更を記録する単位

**commit**は、リポジトリの状態変化を1つにまとめた記録である。
各commitには、作成者、日時、変更内容、直前のcommitへの参照、そしてメッセージが含まれる。

### 良いcommitの単位

1つのcommitは、1つの論理的な変更を表す。

- 良い例: 「`ping-check` サブコマンドにタイムアウト引数を追加する」だけを1つのcommitにする
- 悪い例: タイムアウト引数の追加、無関係なログフォーマットの変更、別バグの修正を1つのcommitにまとめる

コミット単位が大きすぎると、後から特定の変更だけを取り消す（`git revert`）ことが難しくなる。
第8章で述べた「部分成功をひとまとめに報告しない」考え方と同じで、変更もまとめすぎると原因の切り分けができなくなる。

### コミットメッセージの型

`opsctl` リポジトリでは、次の型を採用する。

```text
<種別>: <要約（命令形、50字程度まで）>

<本文（任意。変更理由、影響範囲、関連チケット番号）>
```

種別の例:

| 種別 | 用途 |
|------|------|
| `feat` | 新機能の追加 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `refactor` | 挙動を変えないコード整理 |
| `test` | テストの追加・修正 |
| `chore` | ビルド設定、依存関係更新など |

```bash
git commit -m "feat: add --timeout option to ping-check subcommand" \
  -m "Resolves intermittent hangs on unreachable hosts (see issue #42)."
```

要約を命令形（「追加する」ではなく「追加せよ」に近い簡潔形、英語なら "add" であり "added"/"adds" ではない）で書く慣習は、Gitコミュニティで広く使われる。
チームで統一されていれば、日本語の「〜を追加」のような体言止めでもよい。
重要なのは、リポジトリ内で表記を統一することである。

### 差分の確認とステージングの取り消し

```bash
git diff                 # 未ステージの変更
git diff --staged        # ステージ済みの変更
git restore --staged <path>   # ステージングだけを取り消す（作業ツリーの変更は残る）
git restore <path>            # 作業ツリーの変更を直前のcommit状態に戻す（破壊的）
```

`git restore <path>`（引数なしの作業ツリー復元）は、保存していない編集を失う操作である。
実行前に `git diff` で内容を確認する。

---

## 16.4 branch: 変更を分離して進める

**branch（ブランチ）**は、commitの履歴を分岐させ、他の作業に影響を与えずに変更を進めるための仕組みである。

`opsctl` リポジトリでは、次の運用を採用する。

| ブランチ | 役割 |
|----------|------|
| `main` | 常に動作する状態を保つ。直接コミットせず、pull request経由でのみ変更する |
| `feature/<内容>` | 新機能の開発（例: `feature/log-search-subcommand`） |
| `fix/<内容>` | バグ修正（例: `fix/disk-check-off-by-one`） |
| `release/<バージョン>` | リリース準備用（必要な場合のみ。小規模チームでは省略可） |

```bash
git switch -c feature/log-search-subcommand   # 作成して切り替え（git checkout -b と等価）
# ... 実装とcommit ...
git push -u origin feature/log-search-subcommand
```

ブランチ名には、内容が分かる短い説明を入れる。
`feature/fix2`、`temp` のような名前は、後から見て目的が分からなくなる。

### mainブランチを直接汚さない理由

`main` へ直接コミットする運用では、動作未確認のコードが本番相当のブランチに混ざり、他の開発者の作業にも影響する。
`opsctl` リポジトリでは、GitHub/GitLabのブランチ保護ルールで `main` への直接pushを禁止し、pull request経由のマージのみを許可する。

---

## 16.5 merge: 変更を統合する

**merge（マージ）**は、あるブランチの変更を、別のブランチへ取り込む操作である。

```bash
git switch main
git pull origin main
git merge feature/log-search-subcommand
```

マージには大きく2つの方式がある。

| 方式 | 動作 | 向く場面 |
|------|------|----------|
| fast-forward | `main` に新しいcommitが無ければ、ポインタを進めるだけで統合する | 分岐後に `main` が更新されていない場合 |
| 3-way merge | 分岐点、両ブランチの最新を比較し、マージcommitを作る | 両方のブランチで変更が進んでいた場合 |

`opsctl` リポジトリでは、pull requestのマージ方式として「Squash and merge」（1つのブランチの複数commitを1つにまとめてmainへ載せる）を既定にし、`main` の履歴を機能単位で追いやすくしている。
履歴の詳細な経緯を残したいリリース作業では「Merge commit」を使う場合もあるが、チームで方針を統一する。

### rebase（参考）

**rebase**は、ブランチの分岐元を別のcommitに付け替え、履歴を直線的に整理する操作である。

```bash
git switch feature/log-search-subcommand
git rebase main
```

rebaseは履歴を書き換えるため、**すでに他人と共有（push済み）したブランチには使わない**のが原則である。
共有済みのブランチをrebaseしてforce pushすると、他の開発者のローカル履歴と食い違い、混乱を招く。
個人の作業ブランチをpushする前に整理する用途に限定する。

---

## 16.6 コンフリクト

**コンフリクト（conflict）**は、同じファイルの同じ箇所を異なるブランチで変更しており、Gitが自動統合できない状態である。

### 発生例

`opsctl` の設定スキーマに、2人が同時に別の項目を追加した場合を考える。

```yaml
# ブランチA (feature/add-backup-retention) での変更
defaults:
  timeout_seconds: 30
  backup_retention_days: 14
```

```yaml
# ブランチB (feature/add-log-level) での変更
defaults:
  timeout_seconds: 30
  log_level: INFO
```

同じ行の近くを別々に変更した場合、`git merge` や `git pull` はコンフリクトとして報告する。

```bash
$ git merge feature/add-log-level
Auto-merging config/opsctl.yaml
CONFLICT (content): Merge conflict in config/opsctl.yaml
Automatic merge failed; fix conflicts and then commit the result.
```

コンフリクトが起きたファイルには、次のようなマーカーが挿入される。

```text
defaults:
  timeout_seconds: 30
<<<<<<< HEAD
  backup_retention_days: 14
=======
  log_level: INFO
>>>>>>> feature/add-log-level
```

- `<<<<<<< HEAD` から `=======` まで: 現在のブランチ側の内容
- `=======` から `>>>>>>> feature/add-log-level` まで: 取り込もうとしたブランチ側の内容

### 解消手順

1. マーカーを含むファイルを開き、両方の変更内容を確認する
2. 意図した最終形に手で編集する（片方を採用する、両方を残す、書き直すのいずれか）
3. マーカー（`<<<<<<<`、`=======`、`>>>>>>>`）をすべて削除する
4. 編集後の内容が正しいか確認する（`opsctl` ならYAMLとして構文が有効かをチェックする）
5. `git add` でステージングし、`git commit` で解消を確定する

```yaml
defaults:
  timeout_seconds: 30
  backup_retention_days: 14
  log_level: INFO
```

```bash
git add config/opsctl.yaml
git commit -m "fix: resolve merge conflict by keeping both new config keys"
```

### コンフリクトを減らす習慣

- 長期間ブランチを分岐させたままにせず、こまめに `main` を取り込む（`git pull origin main` または `git rebase main`）
- 1つのcommit・pull requestを小さく保ち、同じファイルの広範囲を触る変更を避ける
- 設定ファイルやCHANGELOGのような「みんなが追記する」ファイルは、追記位置の慣例（アルファベット順、日付降順など）をチームで決めておく

コンフリクト解消中に判断に迷う場合、`git merge --abort`（マージ開始前の状態に戻す）で一度中断し、変更した本人に確認してから再度取り組む方が安全である。

---

## 16.7 pull request（プルリクエスト）

**pull request（PR、GitLabではmerge request）**は、あるブランチの変更を別のブランチ（通常は `main`）へ取り込む提案を行い、レビューと議論を経てから統合する仕組みである。

`opsctl` リポジトリのPRフロー:

```bash
git switch -c fix/disk-check-off-by-one
# ... 修正とcommit ...
git push -u origin fix/disk-check-off-by-one
```

```text
1. GitHub/GitLab上でPRを作成する
2. タイトルと本文に、変更内容・理由・確認方法を書く
3. CI（lint、テスト）が自動実行される
4. レビュアーが差分を確認し、コメントまたは承認を行う
5. 指摘があれば追加commitで対応し、再度レビューを受ける
6. 承認とCI成功を条件に、mainへマージする
```

### PR本文のテンプレート例

`.github/pull_request_template.md` として `opsctl` リポジトリに置く。

```markdown
## 変更内容

<!-- 何を変更したか、簡潔に -->

## 変更理由

<!-- なぜこの変更が必要か。関連issue番号があれば記載 -->

## 確認方法

<!-- レビュアーが再現できる手順、実行例、テスト結果 -->

## 影響範囲

- [ ] 破壊的操作（削除、上書き、再起動）を含む
- [ ] 設定ファイルのスキーマ変更を含む
- [ ] 既存のCLIオプションの挙動変更を含む

## チェックリスト

- [ ] テストを追加・更新した
- [ ] `--dry-run` の挙動を確認した
- [ ] 秘密情報を含んでいないことを確認した
- [ ] CHANGELOGを更新した
```

PRを小さく保つ（目安として、差分数百行以内）と、レビュアーが文脈を保ったまま確認でき、指摘から修正までのサイクルが速くなる。
第15章相当の大きな機能追加は、サブコマンド単位や処理段階単位でPRを分割する。

---

## 16.8 .gitignore

**`.gitignore`**は、Gitの追跡対象から除外するファイル・ディレクトリのパターンを定義するファイルである。

`opsctl` リポジトリの `.gitignore` 例:

```text
# Python
__pycache__/
*.pyc
.venv/
*.egg-info/

# テスト・カバレッジ
.pytest_cache/
.coverage
htmlcov/

# 秘密情報・ローカル専用設定
.env
*.env
secrets.yaml
config/opsctl.local.yaml

# 実行時生成物
work/
reports/
backups/
*.log

# OS・エディタ
.DS_Store
Thumbs.db
.vscode/
.idea/
```

分類の考え方:

| 分類 | 例 | 理由 |
|------|-----|------|
| 言語のビルド・キャッシュ生成物 | `__pycache__/`、`.pytest_cache/` | 誰の環境でも再生成できる。差分ノイズになる |
| 個人のローカル設定 | `.vscode/`、`config/opsctl.local.yaml` | チーム全体に強制すべきでない |
| 実行時生成物 | `work/`、`reports/`、`*.log` | 実行のたびに変わり、履歴管理する価値が薄い |
| 秘密情報 | `.env`、`secrets.yaml` | 次節のとおり、原則としてリポジトリに含めてはならない |

`.gitignore` に追加しても、**すでに追跡（コミット）済みのファイルは自動的に除外されない**。
追跡から外す場合は次を実行する。

```bash
git rm --cached config/opsctl.local.yaml
git commit -m "chore: stop tracking local config override"
```

`git status` で意図しないファイルがステージされていないかを、commit前に必ず確認する習慣をつける。

---

## 16.9 秘密情報をコミットしない

第10章で述べたとおり、APIトークン、パスワード、秘密鍵、証明書の秘密鍵部分はコードに直書きしない。
本節では、Gitリポジトリという観点から、同じ原則をどう運用に落とすかを扱う。

### 予防策

1. `.env` や `secrets.yaml` のような秘密情報専用ファイルは、必ず `.gitignore` に含める
2. `config/opsctl.yaml` のようなリポジトリに含める設定ファイルには、値そのものではなく「環境変数 `OPSCTL_API_TOKEN` を使う」という参照だけを書く（README、10.6節参照）
3. サンプル・テンプレート用の設定ファイルは、`config/opsctl.yaml.example` のように分離し、実値を含む `config/opsctl.yaml` は各自の環境でのみ作成する
4. コミット前フックで秘密情報らしき文字列を検知する（次項）

```bash
# .env.example はコミットする（実値は含めない）
cat > .env.example <<'EOF'
OPSCTL_API_TOKEN=replace-me
EOF

git add .env.example
git commit -m "docs: add .env.example for required environment variables"
```

### pre-commitフックによる検知

`pre-commit`（フレームワーク）と `detect-secrets` を組み合わせ、コミット前に秘密情報らしき文字列を検査する。

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

```bash
pip install pre-commit detect-secrets
pre-commit install
detect-secrets scan > .secrets.baseline
```

導入後は `git commit` のたびに自動でスキャンが走り、疑わしい文字列が新たに追加されるとcommitが失敗する。
CIでも同じチェックを実行し、フックを未導入のローカル環境からのpushも防ぐ。

### 誤ってコミットしてしまった場合の対応

秘密情報を含むcommitをpushしてしまった場合、**「あとから履歴を消したから安全」にはならない**。
リモートにpushされた時点で、他者が既に取得している可能性がある。対応は次の順で進める。

1. **直ちに該当の秘密情報を無効化・再発行（ローテーション）する**（最優先。履歴の修正より先に行う）
2. 影響範囲を確認する（そのトークンでアクセス可能なリソース、権限範囲）
3. 該当commitを含むブランチが共有リモートにpushされているかを確認する
4. 必要に応じて、履歴からファイルを除去する
5. チームへ共有し、各自のローカルリポジトリを再取得（`git fetch` + 強制的な参照更新）するよう周知する

履歴からの除去には `git filter-repo`（Gitプロジェクト推奨のツール。`git filter-branch` は非推奨）や BFG Repo-Cleaner を使う。

```bash
# 例: config/opsctl.yaml を全履歴から除去する（実行前にリポジトリのバックアップを取る）
git filter-repo --path config/opsctl.yaml --invert-paths
```

> **警告**: 履歴の書き換えは破壊的操作であり、共有リポジトリでは全員の協力が必要になる。
> 単独で `git filter-repo` や `git push --force` を実行する前に、チームへ周知し、影響範囲（他ブランチ、フォーク、CIのキャッシュ）を洗い出すこと。
> 何よりも優先すべきは、履歴の掃除ではなく、漏えいした秘密情報そのものの失効である。

---

## 16.10 コードレビュー

**コードレビュー**は、変更をマージする前に、他者が差分を確認し、品質・安全性・保守性を検証する工程である。

### レビュー観点（`opsctl` の例）

| 観点 | 確認内容 |
|------|----------|
| 正当性 | 要件どおりに動くか。エッジケース（第2章）を考慮しているか |
| エラー処理 | 例外の握りつぶしがないか（第8章）。終了コードが規約と整合するか |
| セキュリティ | 秘密情報の直書きがないか。コマンドインジェクション・パストラバーサル対策があるか（第10章） |
| dry-run | 破壊的操作にdry-runの分岐があるか（第12章） |
| ログ | 調査に必要な情報が出ているか。秘密情報がマスクされているか（第9章） |
| テスト | 正常系・異常系・境界値のテストが追加されているか（第13章） |
| 可読性・保守性 | 命名、関数の長さ、重複、コメントの妥当性（第14章） |
| 影響範囲 | 既存のCLI引数や設定スキーマとの互換性を壊していないか |

### レビューコメントの書き方

指摘は「何が問題か」だけでなく「なぜ問題か」「どう直すと良いか」まで含めると、対応が速くなる。

```text
悪い例: ここダメです。

良い例: この`subprocess.run(..., shell=True)`はホスト名をそのまま連結しており、
コマンドインジェクションの余地があります（第10章参照）。
リスト引数 + ホスト名の正規表現検証に変更してください。
```

必須の指摘（マージをブロックする）と、任意の提案（対応してもしなくてもよい）を区別する接頭辞をチームで決めておくと、著者が優先順位を判断しやすい。

```text
[must] 秘密情報がログに平文で出力されています。マスク処理を追加してください。
[nit]  変数名を`h`ではなく`host`にすると読みやすいと思います。
```

### 承認基準

`opsctl` リポジトリでは、次をマージの必須条件とする。

- 少なくとも1名（本番影響のある変更は2名）の承認
- CIの全チェック（lint、型検査、テスト）が成功していること
- レビューでの `[must]` 指摘がすべて解消されていること

レビュアー自身が実装者になっている変更を自己承認しない、というルールも、規模の大小によらず有効である。

---

## 16.11 リリースタグとバージョニング

**タグ（tag）**は、特定のcommitに恒久的な名前を付ける仕組みである。
リリースの区切りに使うと、「今動いているのはどの版か」を明確にできる。

`opsctl` は**セマンティックバージョニング（SemVer）**を採用する。

```text
v<メジャー>.<マイナー>.<パッチ>

例: v1.4.2
```

| 桁 | 上げるタイミング |
|----|------------------|
| メジャー | 既存のCLI引数・設定スキーマ・終了コードの意味を破壊的に変更したとき |
| マイナー | 後方互換を保ったまま、サブコマンドやオプションを追加したとき |
| パッチ | 後方互換を保ったバグ修正のみのとき |

```bash
git switch main
git pull origin main
git tag -a v1.4.2 -m "release: v1.4.2 - fix disk-check off-by-one error"
git push origin v1.4.2
```

`-a`（annotated tag）は、作成者・日時・メッセージを持つタグを作る。
軽量タグ（`-a` なし）と違い、リリースの記録として履歴に残す用途にはannotatedタグを使う。

タグを打つ前に、次を確認する。

- 対象commitが `main` 上にあり、CIが成功していること
- CHANGELOGにバージョンの項目が追加されていること
- 破壊的変更がある場合、メジャーバージョンを上げ、移行手順をCHANGELOGとREADMEに明記していること

---

## 16.12 ロールバック

**ロールバック**（第8章の実行時ロールバックと対になる、コード自体のロールバック）は、問題のある変更を取り消し、直前の安定した状態へ戻す操作である。

状況に応じて手段を使い分ける。

| 状況 | 手段 |
|------|------|
| マージ直後、まだ誰も派生作業をしていない | `git revert <commit>` で打ち消しcommitを作る |
| リリース済みバージョンに重大な不具合が見つかった | 直前の安定タグへデプロイを切り戻し、`main` 上でも `git revert` する |
| ローカル作業中の直前commitを取り消したい（未push） | `git reset --soft HEAD~1`（変更内容は保持） |
| 履歴ごと破棄してよい未push作業 | `git reset --hard HEAD~1`（破壊的。共有ブランチでは使わない） |

### git revertを使う理由

`git reset --hard` で過去に戻すと、共有ブランチの履歴が変わり、他の開発者のローカル履歴と食い違う。
`opsctl` リポジトリでは、**すでにpush・マージ済みの変更を取り消すときは、履歴を書き換えず `git revert` で「打ち消すcommit」を追加する**方針を取る。

```bash
git log --oneline
# a1b2c3d fix: adjust disk-check threshold rounding
# 9f8e7d6 feat: add disk-check subcommand

git revert a1b2c3d
```

`git revert` は、対象commitの変更を打ち消す新しいcommitを作る。
履歴自体は残るため、「いつ・なぜ取り消したか」も後から追跡できる。

### リリースタグからの切り戻し

本番環境へのデプロイ自体は本書の範囲外だが、Gitの観点では次のように対応する。

```bash
# v1.4.1 が安定版、v1.4.2 に問題があった場合
git switch main
git revert v1.4.1..v1.4.2   # v1.4.2で入った変更をまとめて打ち消す（コンフリクトに注意）
git tag -a v1.4.3 -m "release: v1.4.3 - revert v1.4.2 due to disk-check regression"
git push origin main v1.4.3
```

複数commitにまたがるrevertはコンフリクトを起こしやすい。
範囲が広い場合は、無理に自動化せず、diffを手動で確認しながら対応する。

---

## 16.13 READMEとCHANGELOG

### README

**README**は、リポジトリを初めて開いた人が、目的・使い方・前提条件を最短で理解するための文書である。

`opsctl` の `README.md` に含める最低限の項目:

```markdown
# opsctl

運用タスク（疎通確認、ディスク監視、ログ検索など）を実行するCLIツール。

## 前提

- Python 3.11以上
- `pip install -r requirements.txt`

## セットアップ

​```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 各自のトークンを設定する
​```

## 使い方

​```bash
python3 opsctl.py --config config/opsctl.yaml ping-check --hosts-file config/hosts.txt
​```

## 開発者向け

- テスト: `pytest`
- lint: `ruff check .`
- コミット規約、ブランチ運用、レビュー基準は `CONTRIBUTING.md` を参照
```

READMEは「使う人」向けであり、実装の詳細な設計判断までは書かない。
設計判断や開発フローは、`CONTRIBUTING.md` のような別ファイルに分離すると、両方の読者にとって読みやすくなる。

### CHANGELOG

**CHANGELOG**は、バージョンごとの変更内容を、利用者が読める形で記録した文書である。
commitログと違い、利用者にとって意味のある単位（機能追加、修正、破壊的変更）で整理する。

[Keep a Changelog](https://keepachangelog.com/) 形式を採用した `opsctl` の `CHANGELOG.md` 例:

```markdown
# Changelog

## [Unreleased]

### Added

- `log-search` サブコマンドを追加

## [1.4.2] - 2026-07-15

### Fixed

- `disk-check` の閾値判定における端数処理の誤りを修正（issue #58）

## [1.4.0] - 2026-06-02

### Added

- `--quiet` オプションを追加し、WARNING以上のみ出力できるようにした

### Changed

- ログのデフォルト形式をJSON構造化ログに変更

## [1.0.0] - 2026-04-01

### Added

- 初回リリース。`ping-check`、`disk-check`、`log-search` サブコマンドを提供
```

`[Unreleased]` セクションに、マージのたびに変更点を追記し、リリースタグを打つタイミングでバージョン番号と日付に置き換える運用にすると、リリース作業のたびに履歴を掘り返す手間がなくなる。
CHANGELOGの更新を、16.7節のPRテンプレートのチェック項目に含めているのはこのためである。

---

## 16.14 opsctlリポジトリ運用の全体像

ここまでの要素を、`opsctl` リポジトリの1つの変更が生まれてからリリースされるまでの流れとして接続する。

```text
1. issueで要望・不具合を記録する（例: #58 disk-checkの端数処理が誤っている）
2. feature/または fix/ ブランチを作成する
   git switch -c fix/disk-check-rounding
3. 実装し、小さく意味のあるcommitに分ける
4. ローカルでテストとlintを通す
   pytest && ruff check .
5. .envや秘密情報を含んでいないことを確認する
   git status && git diff --staged
6. pushしてPRを作成する
   git push -u origin fix/disk-check-rounding
7. CIが自動実行される。lint、テスト、detect-secretsのチェックが走る
8. レビュアーが確認し、[must]指摘があれば追加commitで対応する
9. 承認とCI成功を確認し、Squash and mergeでmainへ統合する
10. CHANGELOGのUnreleasedに変更点が反映されていることを確認する
11. リリースのタイミングで、CHANGELOGのバージョンを確定し、タグを打つ
    git tag -a v1.4.2 -m "release: v1.4.2 - fix disk-check off-by-one error"
    git push origin v1.4.2
12. 問題が見つかった場合、git revertで打ち消し、必要ならv1.4.3として再リリースする
```

この流れの中で、Gitそのものの操作は道具に過ぎない。
本質は、「変更を小さく保つ」「秘密情報を分離する」「失敗を検知できる状態でマージする」「戻せる状態を保つ」という、第1章から通して扱ってきた原則の、共同開発版である。

---

## 16.15 悪い例と問題点

### 悪い運用

```bash
# 直接mainで作業し、意味の分からないメッセージでcommitする
git switch main
vi opsctl.py
git add .
git commit -m "fix"
git push origin main

# 設定ファイルに実際のトークンを書いたままコミットしてしまう
git add config/opsctl.yaml   # api_token: "sk-abcdef123456" を含む
git commit -m "update config"
git push origin main
```

問題点:

- `main` に直接作業しており、レビューもCIも経由していない
- コミットメッセージ「fix」から、何をどう直したのか後から分からない
- `git add .` で意図しないファイルまでまとめてステージングし、差分の見直しをしていない
- 秘密情報を含む設定ファイルをそのままpushし、リモートリポジトリに漏えいした状態になっている
- 誰もレビューしていないため、コマンドインジェクションのような問題が本番に混入するリスクに気づけない

### 改善後

- `fix/<内容>` ブランチを切り、意味のある単位でcommitする
- コミットメッセージは16.3節の型に従う
- `config/opsctl.yaml` は `.gitignore` に含め、実値の代わりに `config/opsctl.yaml.example` を用意する
- PRを作成し、CIとレビューを経てからマージする
- 万一秘密情報を含めてpushしてしまった場合は、16.9節の手順（ローテーション最優先）に従う

---

## 16.16 セキュリティ上の注意点

- 秘密情報は `.gitignore` と環境変数管理で分離する。誤コミット時は履歴の掃除より先にローテーションする（16.9節）
- `git push --force` はブランチ保護がない限り基本的に使わない。共有ブランチへのforce pushは、他者の変更を消失させる恐れがある
- Personal Access Token やSSH鍵は、リポジトリ内ではなく、各自のローカル環境やCIのシークレットストアで管理する
- PRやissueのやり取りに、本番のホスト名・IPアドレス・実際の認証情報を貼り付けない。学習・共有用のログは、第9章のマスキング処理を通したものを使う
- 外部からのpull requestを受け入れる公開リポジトリでは、CIがシークレットへアクセスできる設定（`pull_request_target` など）を安易に有効化しない。悪意あるコードによるシークレット窃取を防ぐ
- ブランチ保護ルール（レビュー必須、CI必須、force push禁止）を `main` に設定する

---

## 16.17 テスト方法

Gitの運用そのものを自動テストすることは少ないが、**運用ルールをCIで機械的に強制する**ことはできる。

### コミットメッセージ規約のチェック（例: commitlint相当の考え方）

```bash
#!/usr/bin/env bash
# .githooks/commit-msg 相当の簡易チェック
set -euo pipefail

msg_file="$1"
first_line="$(head -n 1 "${msg_file}")"

if ! [[ "${first_line}" =~ ^(feat|fix|docs|refactor|test|chore):\ .+ ]]; then
  echo "commit message must start with feat/fix/docs/refactor/test/chore: <summary>" >&2
  echo "got: ${first_line}" >&2
  exit 1
fi
```

```bash
git config core.hooksPath .githooks
chmod +x .githooks/commit-msg
```

### CIでの必須チェック例（GitHub Actions）

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest
      - name: detect-secrets scan
        run: |
          pip install detect-secrets
          detect-secrets scan --baseline .secrets.baseline
```

PRごとにこのワークフローが実行され、lint・テスト・秘密情報スキャンのいずれかが失敗すればマージをブロックできるよう、リポジトリ設定でこのCIをブランチ保護の必須チェックに登録する。

### コンフリクトマーカーの残留チェック

コンフリクト解消時にマーカーを消し忘れたままコミットする事故は珍しくない。
CIまたはpre-commitフックで検知する。

```bash
if grep -RIn '^<<<<<<< \|^=======$\|^>>>>>>> ' --include='*.py' --include='*.sh' --include='*.ps1' --include='*.yaml' --include='*.md' .; then
  echo "unresolved merge conflict markers found" >&2
  exit 1
fi
```

---

## 章末問題

### 問題1

`git add` と `git commit` の役割の違いを、作業ツリー・ステージングエリア・履歴の3層構造を使って説明せよ。

### 問題2

`opsctl` リポジトリで `main` ブランチへの直接pushを禁止し、pull request経由のマージのみを許可する理由を2つ述べよ。

### 問題3

`config/opsctl.yaml` に実際のAPIトークンを書いてコミット・pushしてしまった。取るべき対応を、優先順位を付けて3つ以上述べよ。

### 問題4

共有済み（push済み）のブランチに対して `git rebase` や `git push --force` を避けるべき理由を説明せよ。

### 問題5

CHANGELOGを、commitログとは別に維持する意義を、読者（利用者と開発者）の違いに触れて述べよ。

### 問題6

セマンティックバージョニングにおいて、既存の終了コードの意味を変更するリリースは、メジャー・マイナー・パッチのどれを上げるべきか、理由とともに答えよ。

---

## 解答と解説

### 問題1

作業ツリーは編集中のファイルの実体である。
`git add` は、作業ツリーの変更のうち次のcommitに含めたい範囲を、ステージングエリアへ選び取る操作である。
`git commit` は、ステージングエリアの内容を1つの記録として履歴に確定する操作である。
`add` の時点ではまだ履歴に残らず、`commit` して初めて変更が記録される。

### 問題2

第一に、レビューを経ずにマージされる変更を防ぎ、コードレビューで検出できるはずの不具合やセキュリティ上の問題が本番へ混入するリスクを減らせる。
第二に、CIによる自動テストとlintを必須化でき、動作未確認のコードが `main` に混ざることを防げる。

### 問題3

1. 最優先で、漏えいしたAPIトークンを無効化し、新しいトークンを再発行する（ローテーション）
2. そのトークンでアクセス可能だったリソースへの不正利用の痕跡がないか確認する
3. `git filter-repo` などで該当ファイルを履歴から除去し、チームへ周知したうえで各自のローカルリポジトリを再取得してもらう
4. 再発防止として、`.gitignore` の見直しと `detect-secrets` によるpre-commitフックを導入する

### 問題4

rebaseやforce pushは、共有済みの履歴を書き換える。
他の開発者はすでに書き換え前の履歴をローカルに持っているため、書き換え後の履歴と食い違い、次回のpull/mergeで予期しないコンフリクトや重複commitが発生する。
共有前の個人作業ブランチに限定して使うべきである。

### 問題5

commitログは開発の経緯を時系列で細かく記録するが、些末な修正や中間状態のcommitも含まれ、利用者にとってはノイズが多い。
CHANGELOGは、利用者が「このバージョンで何が変わったか」を機能単位で把握するために整理された文書であり、開発者向けの詳細な経緯とは異なる読者と目的を持つ。

### 問題6

メジャーバージョンを上げるべきである。
終了コードは、CIや監視システムが機械的に読み取って判断に使う契約の一部であり、意味を変えると既存の呼び出し元が誤動作する可能性がある。
これは後方互換性を壊す変更にあたり、SemVerの定義上メジャーバージョンの対象になる。

---

## 実装演習

### 演習A: ブランチ運用の実践

`opsctl` を想定したローカルリポジトリを作成し、次を実施せよ。

1. `main` に初期commitを作る
2. `feature/add-report-subcommand` ブランチを作り、ダミーのサブコマンド定義を追加してcommitする
3. `fix/typo-in-readme` ブランチを別途作り、READMEの誤字を直してcommitする
4. 両方を `main` へマージし、`git log --graph --oneline --all` で履歴の分岐と統合を確認する

### 演習B: コンフリクトの発生と解消

2つのブランチで、`config/opsctl.yaml` の `defaults` セクションに別々のキーを追加し、意図的にコンフリクトを発生させよ。
マーカーを確認したうえで、両方の変更を残す形で解消し、解消内容が分かるコミットメッセージを付けてcommitせよ。

### 演習C: 秘密情報の誤コミット対応の演習

ダミーの秘密情報（例: `DUMMY_TOKEN=not-a-real-secret-12345`）を含むファイルを意図的にコミットし、次を実施せよ。

1. `.gitignore` に追加し、`git rm --cached` で追跡を外す
2. `git filter-repo`（学習用の使い捨てリポジトリで実行すること）で該当ファイルを履歴から除去する
3. 除去前後で `git log -p -- <ファイル名>` の出力を比較し、履歴から消えたことを確認する

> 演習B・Cは、本物の秘密情報や共有リポジトリでは絶対に試さないこと。学習用に新規作成した使い捨てローカルリポジトリでのみ実施する。

### 演習D: PRテンプレートとCIの整備

16.7節のPRテンプレートと、16.17節のCI設定例を、実際のGitHubリポジトリ（学習用の個人リポジトリでよい）に追加せよ。
わざと `ruff check .` に失敗するコードを含むPRを作成し、CIが失敗してマージがブロックされることを確認せよ。

---

## 本章のまとめと本書全体の接続

第16章までで、要件分解（第2章）から実装（第3章〜第7章）、安全性と品質（第8章〜第14章）、実践（第15章）、そして共同開発（本章）までの一連の流れが揃った。

`opsctl` は個人のスクリプトから、複数人でレビューし、CIで検証し、バージョンを追跡しながら育てるソフトウェアへと接続される。
付録A・B・Cでは、ここまでの内容を実務で参照しやすい形（言語選択の比較表、終了コードの推奨表、本番投入前チェックリスト）にまとめる。


---


<!-- SOURCE: A_language_selection.md -->

# 付録A 言語選択の指針

本書は、Bash、PowerShell、Pythonのどれが優れているかを決めるものではない。
三言語は前提とする実行環境も設計思想も異なり、同じ問題に対しても向き不向きがある。

この付録では、README冒頭で示した比較表を、判断軸ごとに詳細化する。
目的は「優劣の判定」ではなく「この案件ではどの軸が効くか」を先に洗い出し、そのうえで言語を選べるようにすることである。

---

## A.1 判断の進め方

いきなり言語を決めるのではなく、次の順で考える。

1. 対象OSを確認する(A.2)。選べる言語の範囲がここでほぼ決まる
2. 処理の複雑さと保守期間を見積もる(A.3、A.9)。使い捨てか、半年以上保守するかで重みが変わる
3. 外部コマンドとデータ加工のどちらが処理の中心かを確認する(A.4、A.5)
4. API連携やテストの要否を確認する(A.6、A.7)
5. 実行環境の準備コストとチームのスキルを確認する(A.9、A.10)

複数の軸が矛盾する場合(例: 対象OSはLinuxだがロジックが複雑)は、保守期間が長い案件ほど、複雑さとテスト容易性の軸を優先する。
数日で役目を終える使い捨てスクリプトは、対象OSと外部コマンド連携の軸を優先してよい。

---

## A.2 対象OS

実行するホストのOSは、選択肢を絞る最初の軸である。

- Linux/macOSが対象で、既にシェルでの運用が定着している現場では、Bashが最も摩擦が少ない。標準で入っており、追加の実行環境準備が要らない
- Windows Serverやオンプレミスの Active Directory、Windowsのサービス・レジストリ・イベントログを扱うなら、PowerShellが最も直接的にアクセスできる。`Get-ADUser`や`Get-Service`のような専用コマンドレットが用意されている
- Linux/macOS/Windowsを横断して同じロジックを動かす必要があるなら、Pythonが最も一貫している。PowerShell 7もクロスプラットフォームだが、Windows管理系コマンドレットの多くはWindows限定である

BashをWindowsで動かす場合はWSLやGit Bashを介するため、対象ホストそのものがWindowsであっても、管理端末側がLinux/macOSであれば選択肢に入る。
対象ホストと実行端末が異なる場合は、両方のOSを踏まえて判断する。

---

## A.3 処理の複雑さ

処理の複雑さは、条件分岐の数、状態管理の必要性、エラー処理の細かさで測る。

数行から数十行程度で、既存コマンドの組み合わせで完結する処理は、Bash・PowerShellどちらでも書きやすい。
分岐が増え、状態を持つオブジェクトや複雑なデータ構造(第3章)を扱い始めると、Bashは可読性が急速に落ちる。
Bashには構造体や辞書のネストを扱う標準的な手段が薄く、複雑なロジックを書こうとするほど、文字列操作でごまかす箇所が増える。

PowerShellはオブジェクトパイプラインを持つため、Bashよりは複雑な処理に耐えるが、それでも大規模な分岐やアルゴリズムの実装は、専用の言語機能(クラス、型システム、豊富な標準ライブラリ)を持つPythonの方が書きやすい。

目安として、条件分岐が三重以上にネストする、状態を持つデータ構造を複数扱う、といった兆候が出たら、Bash/PowerShellからPythonへの切り替えを検討する。

---

## A.4 外部コマンドとの連携

**外部コマンド連携**は、OS付属のコマンドや別ツールを呼び出し、その出力を処理する度合いである。

Bashは、パイプ(`|`)とリダイレクトを言語機能として持ち、外部コマンドの糊付けに最も向く。
`grep`、`awk`、`sed`のようなテキスト処理コマンドと組み合わせる用途では、他の二言語より短く書ける場合が多い。

PowerShellは、Windows管理コマンドレット(`Get-Service`、`Get-EventLog`など)との連携が強い。
外部の`.exe`を呼ぶこともできるが、標準出力は文字列として扱われ、Bashほど軽快ではない。

Pythonは`subprocess`モジュールで外部コマンドを呼べるが、第7章で見たとおり、記述量はBashより多くなる。
その代わり、コマンドの戻り値・標準出力・標準エラー・タイムアウトを構造化して扱えるため、外部コマンドの結果を条件分岐に細かく使う処理では、かえって見通しが良くなることがある。

---

## A.5 データ加工

**データ加工**は、取得した値を変換・集計・整形する処理である。

テキスト行の抽出やフィルタリングのような単純な加工は、Bashのパイプラインが簡潔である。
JSON/CSVのようにネストした構造や、複数キーでの結合・集計が必要になると、Bashは途端に不利になる。
`jq`を併用すればJSONを扱えるが、複雑なロジックを`jq`のフィルタ言語だけで組むのは可読性を損ないやすい。

PowerShellはオブジェクトとして扱うため、`ConvertFrom-Json`や`Import-Csv`と`Where-Object`/`Select-Object`の組み合わせで、構造化データの加工がしやすい。

Pythonは、標準ライブラリ(`json`、`csv`)とデータ構造(リスト、辞書、第3章)の組み合わせで、最も複雑な加工に耐える。
複数ソースの突き合わせ(第13章の`load_and_aggregate`のような処理)は、Pythonが最も書きやすい。

---

## A.6 API操作

HTTP/RESTでの外部API連携(第11章)は、認証、リトライ、ページネーション、エラーハンドリングの組み合わせになりやすい。

Bashでは`curl`でAPIを呼べるが、レスポンスのJSONを加工するには`jq`が必要になり、リトライやページネーションのロジックをシェルスクリプトで書くと複雑になりやすい。

PowerShellの`Invoke-RestMethod`は、JSONレスポンスを自動的にオブジェクトへ変換してくれるため、Bashより簡潔に書ける。

Pythonは`requests`や`httpx`のような成熟したライブラリがあり、認証・リトライ・タイムアウトの実装パターンが豊富である。
複数エンドポイントを扱う、レート制限に対応する、といった要件が増えるほどPythonが有利になる。

---

## A.7 可搬性

**可搬性**は、同じスクリプトが異なる環境でも同じように動く度合いである。

Bashは、ディストリビューションやバージョンによって`bash`のバージョンが異なり(第1章の脚注、macOSの古い`/bin/bash`など)、書き方によっては動かない環境が出る。
POSIX準拠を意識して書けば`sh`との互換性も上がるが、機能を絞ることになる。

PowerShellは、Windows PowerShell 5.1とPowerShell 7で差異があり、7を対象にすればクロスプラットフォームだが、5.1しか無い古いWindows Serverでは一部の構文が使えない。

Pythonは、バージョン差(3.9と3.11など)はあるものの、OS差そのものの影響は比較的小さい。
`pathlib`のようにOS差を吸収する標準ライブラリがあり、同じコードをLinux/macOS/Windowsで動かしやすい。

---

## A.8 テスト容易性

第13章で扱ったとおり、テストのしやすさは言語ごとのエコシステム成熟度に差がある。

Pythonはpytestが成熟しており、モック・パラメータ化・カバレッジ計測まで一通り揃っている。
PowerShellはPesterがあり、`Describe`/`It`/`Mock`でPythonに近い水準のテストが書ける。
Bashは標準のテストフレームワークが無く、手書きのアサーション関数か、Batsのような外部ツールの導入が必要になる(13.9)。

半年以上保守する、複数人で変更するといった前提がある案件では、テストのしやすさを軽視しないほうがよい。
テストが書きにくい言語で複雑なロジックを書くと、第13章で述べた「変更を安全に行える状態」を維持しにくくなる。

---

## A.9 保守性と実行環境準備

**保守性**は第14章で扱ったとおり、読み手が正しく推測できる度合いである。
言語そのものより設計や命名の影響が大きいが、言語機能の差も無視できない。

Bashは、行数が増えるほど責務分離が難しくなりやすい(名前空間が無い、第5章)。
PowerShellはモジュール(`.psm1`)で伸ばせるが、Windows運用チーム外への展開はやや限定的である。
Pythonはモジュールとパッケージ、型ヒント(第13章)を組み合わせることで、大きくなっても保守しやすい構造を保ちやすい。

**実行環境準備**は、スクリプトを動かすために必要な追加のセットアップである。

Bashは多くのLinux/macOS環境に標準で入っており、追加準備がほぼ要らない。
PowerShellはWindowsに標準で入っているが、Linux/macOSでは`pwsh`を別途導入する必要がある。
Pythonは、インタープリター本体に加え、仮想環境(`venv`)とライブラリのインストールが必要になる。
使い捨てのワンライナーであれば、この準備コストの差が選定に効いてくる。

---

## A.10 チームスキル

最終的な判断は、書いた本人だけでなく、将来それを保守する人のスキルセットにも依存する。

- インフラ層のメンバーが中心で、Linuxコマンドに慣れているチームは、Bashへの心理的な障壁が低い
- Windows運用が中心のチームは、PowerShellの方が採用・定着しやすい
- ソフトウェア開発の経験者が多いチームは、Pythonの型ヒント・パッケージ管理・テストフレームワークを使いこなしやすい

スキルが無い言語を「技術的に最適だから」という理由だけで選ぶと、保守段階で書ける人が限られ、属人化のリスクが上がる。
新しい言語を採用する場合は、チーム内の教育コストも選定理由に含める。

---

## A.11 まとめの目安表

判断軸を一つの表にまとめると、次のようになる(README冒頭の表と同一の要約)。

| 観点 | Bash | PowerShell | Python |
|------|------|------------|--------|
| 対象OS | Linux/macOS中心 | Windows中心、7ならクロス | クロスプラットフォーム |
| 処理の複雑さ | 短い糊付け向き | オブジェクトパイプライン向き | 中〜大規模ロジック向き |
| 外部コマンド連携 | 強い | Windows管理との連携が強い | subprocessで可能だが厚め |
| データ加工 | テキスト向き、複雑な構造は弱い | オブジェクトとCSV/JSONが扱いやすい | 強い |
| API操作 | curlで可能 | `Invoke-RestMethod`が便利 | ライブラリが豊富でテストしやすい |
| 可搬性 | シェル差に注意 | 7なら広い。5.1はWindows限定 | 高い |
| テスト容易性 | 工夫が必要(Bats等) | Pesterで可能 | pytestが成熟 |
| 保守性 | 長大化すると落ちやすい | モジュール化で伸ばせる | モジュールと型で伸ばしやすい |
| 実行環境準備 | ほぼ標準装備 | Windowsは標準、他は導入 | ランタイムとvenvが必要 |
| チームスキル | インフラ層で共通しやすい | Windows運用チーム向き | 開発経験があると速い |

---

## A.12 ケース別の判断例

判断軸を組み合わせた具体例を三つ挙げる。

**ケース1: Linuxサーバー群のログを毎晩grepして件数を集計し、Slackへ通知する**

対象OSはLinux、処理はテキスト抽出と件数集計のみで複雑さは低く、外部コマンド(`grep`、`curl`)中心である。
Bashが最も少ないコード量で完結し、実行環境準備も不要である。
通知先APIとのやり取りが増え、リトライやエラー分類が必要になった時点でPythonへの切り替えを検討する。

**ケース2: Active DirectoryのユーザーアカウントとM365ライセンスの棚卸しを、月次でCSV出力する**

対象OSはWindows、扱う対象がAD/M365という時点でPowerShellの専用コマンドレットが決定的に有利である。
データ加工(複数ソースの突き合わせ)はオブジェクトパイプラインで完結し、PowerShellを選ぶ。

**ケース3: 複数クラウドのAPIから使用量を取得し、しきい値判定してダッシュボード用にDBへ書き込む。半年以上運用しチームで保守する**

API連携が中心で、ロジックも複雑、かつ長期保守とチーム開発が前提である。
テスト容易性(pytest)、依存関係管理、型ヒントによる保守性のいずれもPythonが有利であり、Pythonを選ぶ。

---

## A.13 まとめ

言語選択で最も避けるべきなのは、「好きだから」「慣れているから」だけを理由に、対象OSや保守期間を考慮せず決めることである。
逆に、判断軸をすべて完璧に検討してから着手する必要もない。
対象OSと保守期間の二軸さえ最初に固定すれば、残りの判断はおおむね自然に絞られる。

複数言語を組み合わせる設計(README記載の`opsctl`のように、主実装と補助実装を分ける)も現実的な選択肢である。
一つの言語に固執せず、サブコマンドごとに最適な言語を選ぶ運用は、大きなツール群では珍しくない。


---


<!-- SOURCE: B_exit_codes.md -->

# 付録B 終了コード規約

**終了コード**は、プロセスが終了するときにOSへ返す小さな整数値であり、呼び出し元(シェル、他のプロセス、CI)が成否を判定するために使う。

README、第1章、第12章で示した`opsctl`共通の終了コード規約を、この付録でまとめて詳細化する。
サブコマンドを追加するときも、この規約から逸脱しないことを原則とする。

---

## B.1 opsctl終了コード規約

| コード | 名称 | 意味 | 想定する対応 |
|--------|------|------|----------------|
| 0 | `EXIT_OK` | 成功(警告なし) | 特に対応不要 |
| 1 | `EXIT_USAGE` | 利用者エラー(引数不正、設定ファイル誤り、必須値の欠落) | コマンドラインや設定ファイルを直して再実行する |
| 2 | `EXIT_RUNTIME` | 実行時エラー(一部失敗を含む) | ログを確認し、対象や環境を調査する |
| 3 | `EXIT_CRITICAL` | 閾値超過などの監視上のCRITICAL | 監視・アラートとして扱い、対応者を呼び出す |
| 4 | `EXIT_TIMEOUT` | タイムアウト | ネットワークや対象システムの応答性を確認する |
| 130 | (シェル慣例、`EXIT_SIGINT`) | ユーザーによる中断(Ctrl+C、`SIGINT`) | 意図した中断であれば対応不要 |

この6値は、全サブコマンド共通の意味を持つ。
サブコマンドごとに異なる意味を割り当てない。
「この値が返ってきたら、サブコマンドが何であれこの意味である」という一貫性が、監視システムやCIでの判定ロジックを単純に保つ。

### なぜ6値に絞るか

終了コードを増やしすぎると、呼び出し側(監視システム、CI、他のスクリプト)がすべての値を把握する必要が生じ、かえって扱いにくくなる。
サブコマンド固有の詳細情報(どのホストが失敗したか、何件中何件成功したか)は、終了コードではなく、第9章のログや第12章の実行結果サマリー(JSON)に持たせる。

終了コードは「次に何をすべきか」という大分類の判定に使い、詳細は構造化された出力から読み取る、という役割分担にする。

---

## B.2 コード129以降と130の由来

**130**という値は、慣例的にUnix系シェルで使われる。
プロセスがシグナルで終了した場合、多くのシェルは終了コードを`128 + シグナル番号`として報告する。
`SIGINT`(Ctrl+Cによる割り込み)はシグナル番号2のため、`128 + 2 = 130`になる。

```bash
sleep 100
# Ctrl+Cを押す
echo $?
# => 130
```

`opsctl`が130を明示的に返す実装をしていなくても、Ctrl+Cで中断されたプロセスの終了コードはシェルの慣例に従って130になることが多い。
Pythonでは、`KeyboardInterrupt`を捕捉しなければ、インタープリターが終了コード130相当(実際は`SIGINT`によるプロセス終了)で終わる。
意図的に130を返したい場合は、明示的に捕捉して`sys.exit(130)`とする。

```python
import sys

def main(argv: list[str] | None = None) -> int:
    try:
        return run(argv)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
```

新しいサブコマンドを追加する際、5〜129、131〜255の未使用範囲に独自の意味を割り当てたくなることがあるが、`opsctl`では行わない。
詳細な原因分類は終了コードではなく構造化ログとサマリー出力に任せる方針(B.1)を優先する。

---

## B.3 Pythonでの終了コードの扱い

Pythonでは`sys.exit(code)`で終了コードを指定する。

```python
import sys

def main(argv: list[str] | None = None) -> int:
    ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

注意点:

- `sys.exit()`(引数無し)は終了コード0と等価である
- `sys.exit("message")`のように文字列を渡すと、その文字列が標準エラーへ出力され、終了コードは1になる
- 終了コードは実際には0〜255の範囲に切り詰められる(OSのプロセス終了コードが1バイトのため)。256以上の値を返すと、`code % 256`相当の値になる
- 例外を捕捉せずにプログラムが終了すると、Pythonは終了コード1でプロセスを終える。第8章の方針どおり、想定される例外は`main`の中で捕捉し、意図した終了コードへ変換する

```python
# 悪い例: 想定外の終了コードになる
import sys
sys.exit(300)  # 実際には 300 % 256 = 44 になる環境がある

# 改善: 規約の範囲(0-255、opsctlでは0,1,2,3,4,130)に収める
sys.exit(4)
```

---

## B.4 Bashでの終了コードの扱い

Bashでは`exit`文で終了コードを指定し、直前に実行したコマンドの終了コードは`$?`で参照できる。

```bash
#!/usr/bin/env bash
set -euo pipefail

EXIT_OK=0
EXIT_USAGE=1
EXIT_RUNTIME=2

check_hosts() {
  ...
}

check_hosts || exit "${EXIT_RUNTIME}"
exit "${EXIT_OK}"
```

注意点:

- Bashの終了コードも0〜255に切り詰められる。負の値を渡すと`256 + n`相当になる場合がある(例: `exit -1`は多くの環境で255になる)
- `set -e`は、コマンドが非0の終了コードを返すとスクリプトを即座に終了させる。第8章のとおり、意図的に失敗を許容したいコマンドには`|| true`や`if`文での明示的な分岐を使う
- パイプライン(`cmd1 | cmd2`)の終了コードは、既定では最後のコマンド(`cmd2`)の終了コードになる。`cmd1`の失敗を検知したい場合は`set -o pipefail`を有効にする(第7章)
- 関数の`return`は0〜255の整数のみを返せる(第5章)。文字列を返したい場合は標準出力を使う

```bash
set -o pipefail
grep "ERROR" app.log | wc -l
# pipefail が無いと、grepが0件で終了コード1を返しても、
# wc -l が成功していれば全体の終了コードは0になってしまう
```

---

## B.5 PowerShellでの終了コードの扱い

PowerShellには、コマンドやスクリプトの成否を示す複数の仕組みがあり、Bash/Pythonより注意が必要である。

| 仕組み | 意味 |
|--------|------|
| `exit <n>` | スクリプトまたはセッション全体を、指定した終了コードで終わらせる |
| `$LASTEXITCODE` | 直前に実行した**ネイティブコマンド**(`.exe`など)の終了コードを保持する変数 |
| `$?` | 直前の**コマンドレットまたはステートメント**が成功したかを示す真偽値 |
| `$ErrorActionPreference` | 非終端エラー(non-terminating error)発生時の既定動作を制御する |

```powershell
param(
    [int]$Timeout = 30
)

$EXIT_OK = 0
$EXIT_USAGE = 1
$EXIT_RUNTIME = 2

if ($Timeout -le 0) {
    Write-Error "Timeout must be positive"
    exit $EXIT_USAGE
}

& ping.exe -n 1 example.invalid | Out-Null
if ($LASTEXITCODE -ne 0) {
    exit $EXIT_RUNTIME
}

exit $EXIT_OK
```

注意点:

- `$LASTEXITCODE`はネイティブコマンド専用であり、PowerShellの関数や`cmdlet`の成否には使えない。コマンドレットの成否は`$?`か、try/catch(第8章)で判定する
- PowerShellの関数内で`exit`を呼ぶと、関数だけでなく呼び出し元のスクリプト全体、場合によってはシェルセッションごと終了することがある。関数内では`exit`を使わず、`return`と戻り値、または例外(`throw`)で失敗を伝え、スクリプトの最上位でだけ`exit`を呼ぶ
- Windows PowerShell 5.1と PowerShell 7で、未処理例外発生時の既定終了コードの挙動に差がある場合がある。本番運用では、`try/catch`で確実に捕捉し、終了コードを明示的に設定する(第8章)
- `cmd.exe`の`%ERRORLEVEL%`は、PowerShellの`$LASTEXITCODE`とおおむね対応するが、別の仕組みである。`cmd.exe`から呼ばれるバッチファイル経由の連携では、両者を混同しない

---

## B.6 呼び出し元での終了コードの扱い

**Bashでの連結**:

```bash
opsctl ping-check --hosts-file config/hosts.txt && echo "all reachable"
opsctl disk-check || echo "disk check reported a problem"
```

`&&`は直前のコマンドが終了コード0のときだけ実行され、`||`は非0のときだけ実行される。

**cronでの扱い**:

cronは、ジョブの終了コードが非0で、かつ標準出力または標準エラーに出力があった場合、その内容をメール送信する設定になっていることが多い。
終了コードだけを見て通知するcron監視ラッパーを使う場合は、`opsctl`の終了コード規約(B.1)に合わせて閾値を設定する。

**systemdでの扱い**:

systemdサービス/タイマーとして`opsctl`を実行する場合、`systemctl status`や`journalctl`で終了コードを確認できる。
`OnFailure=`ディレクティブと組み合わせると、非0終了時に別のユニット(通知処理など)を起動できる。

**CIでの扱い**:

第13章のCI例のとおり、GitHub Actionsなどの多くのCIサービスは、ステップの終了コードが非0であればジョブ全体を失敗として扱う。
`opsctl`をCIのステップとして呼ぶ場合、`EXIT_CRITICAL`(3)や`EXIT_RUNTIME`(2)をCI上の失敗として扱いたいのか、警告として握りつぶしたいのかを、呼び出し側のワークフロー定義で明示する。

```yaml
- name: Run disk check
  run: |
    opsctl disk-check --config config/opsctl.yaml
    # 終了コード3(CRITICAL)はCI失敗として扱いたいので、
    # ここでは終了コードをそのまま伝播させる(何もしない)
```

---

## B.7 サブコマンド追加時のチェックリスト

新しいサブコマンドを実装するときは、次を確認する。

- [ ] 成功時に`EXIT_OK`(0)を返しているか
- [ ] 引数不正・設定不正を`EXIT_USAGE`(1)に統一しているか
- [ ] 対象の一部または全部の処理失敗を`EXIT_RUNTIME`(2)に統一しているか
- [ ] 監視上のCRITICAL相当(しきい値超過など)を`EXIT_CRITICAL`(3)に統一しているか
- [ ] タイムアウトを`EXIT_TIMEOUT`(4)に統一しているか
- [ ] 独自の終了コードを新設していないか(詳細はログとサマリー出力に持たせる、B.1参照)
- [ ] `KeyboardInterrupt`/`SIGINT`時の挙動を確認したか(そのままにするか、130を明示するか)


---


<!-- SOURCE: C_checklist.md -->

# 付録C 本番投入前チェックリスト

このチェックリストは、本書で作成したスクリプトを本番環境へ投入する前に確認する項目をまとめたものである。
各章の「セキュリティ上の注意点」で個別に触れた内容を、投入直前の作業として一箇所に集約している。

> **警告**: このチェックリストを満たしても、対象システム固有のリスクをすべて排除できるわけではない。
> 本書のサンプルコードは学習用であり、実際の本番投入では、対象システムの構成、権限モデル、社内の変更管理プロセスに従った追加の確認が必要である。「チェックリストを通したから安全」と機械的に判断しない。

---

## C.1 要件と検証

- [ ] 処理対象(ホスト一覧、ファイル、APIエンドポイント)が、意図した範囲と一致しているか確認した
- [ ] 想定する入力だけでなく、空データ・大量データ・一部欠損データでも動作を確認した(第2章、第13章の境界値)
- [ ] ステージング環境、または本番同等の検証環境で実行し、結果を確認した
- [ ] 処理対象の件数が、想定と大きく異なる場合に警告または停止する仕組みがあるか確認した(例: 対象ホストが0件、または想定の10倍という異常値で気づけるか)

## C.2 dry-run

- [ ] 破壊的操作(削除、上書き、再起動、権限変更、外部への変更API呼び出し)を含む場合、`--dry-run`相当のオプションを実装した(第12章)
- [ ] `--dry-run`で実行し、ログに出力される「実行予定の操作」が意図どおりであることを確認した
- [ ] `--dry-run`が、読み取り専用処理と書き込みを伴う処理を正しく区別しているか確認した(読み取り専用処理まで止めていないか、書き込み処理を誤って実行していないか)
- [ ] 初回の本番実行は、可能な限り影響範囲を絞ったサブセット(一部ホストのみなど)から始める計画を立てた

## C.3 秘密情報

- [ ] APIトークン、パスワード、秘密鍵がソースコードにリテラルで書かれていないか確認した(第10章)
- [ ] 秘密情報がGitの履歴やコミット済みの設定ファイルに含まれていないか確認した(第16章の`.gitignore`)
- [ ] 秘密情報の受け渡しに、コマンドライン引数(`ps`で見える)を使っていないか確認した
- [ ] ログ出力に秘密情報がマスキングされずに出力されていないか、実際にログを目視で確認した(第9章)
- [ ] 秘密情報のローテーション手順と、漏えい時の失効手順を確認した(第10章)

## C.4 権限

- [ ] スクリプトの実行アカウントが、必要な操作に対して最小限の権限を持っているか確認した(第10章の最小権限の原則)
- [ ] root/Administratorでの実行が必須かどうかを再確認し、可能であれば権限を絞った専用アカウントに変更した
- [ ] 秘密情報や設定ファイルのファイルパーミッションを絞ったか確認した(`chmod 600`など)
- [ ] 一時的な権限昇格が必要な場合、昇格の範囲と期間が最小になっているか確認した

## C.5 ログと監視

- [ ] 実行の成功・失敗・部分成功が、ログと終了コード(付録B)の両方から判別できるか確認した
- [ ] 実行ID(`run_id`)が付与され、複数回の実行や並列実行のログを混同しないことを確認した(第9章)
- [ ] 監査が必要な操作(削除、設定変更、権限変更)について、監査ログが記録されることを確認した(第10章)
- [ ] 失敗時に、担当者へ通知が届く経路(監視システム、Slack通知、メールなど)が設定されているか確認した
- [ ] ログの保存先とローテーション設定(第9章)が、ディスクを圧迫しない設定になっているか確認した

## C.6 テストと静的解析

- [ ] 正常系・異常系・境界値のテストが書かれ、パスすることを確認した(第13章)
- [ ] lint(ruff、ShellCheck、PSScriptAnalyzerなど)を実行し、指摘事項に対応した(第13章)
- [ ] 型ヒントを付けたPythonコードで、mypyの指摘に対応した(第13章)
- [ ] CIでテストとlintが自動実行される設定になっているか確認した(第13章)
- [ ] コードレビューを受け、指摘事項に対応した(第13章)

## C.7 依存関係

- [ ] 依存ライブラリ・モジュールのバージョンが固定されているか確認した(第14章)
- [ ] 依存関係に既知の重大な脆弱性が無いか確認した(脆弱性スキャンツール、またはパッケージマネージャーの監査コマンド)
- [ ] 実行環境(Python/Bash/PowerShellのバージョン)が、対象サーバーで利用可能なバージョンと一致しているか確認した

## C.8 ロールバックと復旧

- [ ] 処理が失敗した場合、途中状態からの復旧手順(再実行、ロールバック)が用意されているか確認した(第8章)
- [ ] 設定ファイルや対象データを変更する処理は、変更前の状態をバックアップしてから実行しているか確認した(第6章)
- [ ] 再実行しても安全(冪等、または安全にスキップできる)かどうかを確認した(README「再実行性」)
- [ ] 部分成功時に、失敗した対象だけを再処理できる仕組み(失敗リストの出力など)があるか確認した

## C.9 変更管理とドキュメント

- [ ] 変更内容が、社内の変更管理プロセス(変更管理番号、承認フローなど)に従って記録されているか確認した
- [ ] 実行手順、ロールバック手順、問い合わせ先が、実行者以外にも分かるドキュメントとして残っているか確認した
- [ ] スクリプトの使い方(`--help`、README、本書該当章へのリンク)が最新の実装と一致しているか確認した(第14章のコメント/ドキュメント追従)
- [ ] 初回実行の予定日時と、影響を受ける可能性があるチームへの事前周知を行ったか確認した

---

## C.10 最終確認

上記すべてを確認したうえで、次の問いに答えられる状態を最終確認の基準とする。

1. このスクリプトが失敗したとき、誰が、どのログを見て、どう対処するか説明できるか
2. このスクリプトを誤って2回実行してしまった場合、何が起きるか説明できるか
3. このスクリプトが対象を取り違えた場合、影響範囲をどう把握し、どう復旧するか説明できるか

三つの問いに具体的に答えられない場合は、本番投入前に該当する章(第8章のエラー処理、README「再実行性」、第6章のバックアップ)へ戻り、設計を見直す。


---
