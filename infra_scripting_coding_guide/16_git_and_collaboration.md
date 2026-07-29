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
