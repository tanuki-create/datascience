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
