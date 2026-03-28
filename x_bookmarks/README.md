さ# X ブックマーク棚卸し

## 取得日・ソース

- **取得日**: 2026-03-28
- **ビュー**: Cursor 内蔵ブラウザで `https://x.com/i/bookmarks` の **「すべてのブックマーク」**および **フォルダタブ**（LLM / 画像生成 / 研究 など。URL が `/i/bookmarks/<フォルダID>` に変わる）。
- **方法**: アクセシビリティスナップショット＋スクロール。長文は **「さらに表示」** を押すと link の `name` が伸びることがある（MCP の `browser_click` で ref 指定）。フォルダ専用の投稿は **タブ切替**で追加取得。追加分は `snapshot_dumps/extra_link_names.txt` に 1 行 1 断片で足せる。
- **フルテキスト**: スナップショットの **リンク accessible name** が上限に近い本文になることが多いが、**API の公式本文ではない**。完全な文字列は X のデータエクスポートまたは各ポストを個別に開くこと。
- **拡張取得（同日）**: スナップショットを複数回保存してマージ。UI 上は **3月中旬〜下旬**の本文が中心で、別フレームでは **2月24–25日**（NDL OCR 関連など）も確認。**2026年1月の日付文字列はこのマージ結果には現れず**、一覧のさらに下または公式アーカイブでの検証を推奨。

## ファイル

| ファイル | 内容 |
|----------|------|
| **`bookmarks_500_2026-03-28.md`** | **500 件カタログ**（フルテキスト＝取得できた範囲＋要点）← **現在のメイン成果** |
| **`analysis_500_2026-03-28.md`** | 上記 500 件の **キーワードバケット分析** |
| **`reports/by_bucket_2026-03-28/README.md`** | **バケット別レポート**（再訪の焦点・GitHub 抽出・示唆）。`_merged_bookmarks.tsv` を `build_bucket_reports.py` で分割出力 |
| `bookmarks_200_2026-03-28.md` | 200 件版（旧ビルド。再生成する場合は `--limit 200`） |
| `analysis_200_2026-03-28.md` | 200 件版の分析 |
| `bookmarks_2026-03-28.md` | 初回セッションの整理リスト（時刻・ハンドル・要約） |
| `bookmarks_extended_2026-03-28.md` | 拡張スクロール＋複数スナップショットマージの一覧（表形式・カテゴリ別） |
| `categories_summary.md` | **カテゴリ別まとめ**（インテント整理・傾向・次のステップ） |
| `scroll_50_session.md` | **ブックマーク欄を下に 50 回スクロール**した直後の 1 スナップショットの整理 |
| `bookmarks_key_points.md` | **各投稿の要点**（短文まとめ・カテゴリ別） |
| `analysis.md` | 初回のトピック分析メモ |
| `bookmarks_digest_with_points.md` | スナップショット和集合のダイジェスト（要約＋原文断片） |
| `_merged_bookmarks.tsv` | 複数ソースをマージした **重複除去済み 1 行 1 エントリ**（2026-03-28 時点で **520 行**前後、`--limit 500` でカタログ化） |
| `snapshot_dumps/extra_link_names.txt` | ブラウザで拾った **フォルダ別リンク断片**（`[FOLDER:…]` 行頭はマージ時に除去） |
| `_parsed_bookmarks.tsv` | `~/.cursor/browser-logs/snapshot-*.log` と `snapshot_dumps/*` から抽出した候補 |
| `parse_bookmark_snapshots.py` | 上記ログ → `_parsed_bookmarks.tsv` |
| `merge_bookmark_sources.py` | TSV ＋各 `.md` → `_merged_bookmarks.tsv` |
| `build_bookmarks_catalog_md.py` | `_merged_bookmarks.tsv` → `bookmarks_{N}_*` / `analysis_{N}_*`（例: `python3 build_bookmarks_catalog_md.py --limit 500 --date 2026-03-28`） |
| `build_bucket_reports.py` | `_merged_bookmarks.tsv` → `reports/by_bucket_2026-03-28/*.md`（バケット別の再訪リスト・GitHub・示唆） |
| `build_bookmarks_200_md.py` | 旧 200 件専用（非推奨・`build_bookmarks_catalog_md.py` に統合予定） |
| `extract_show_more_refs.py` | スナップショット YAML から「さらに表示」ボタンの ref 一覧を出力 |
| `snapshot_dumps/` | スナップショット YAML/log を置くと `parse_bookmark_snapshots.py` の入力になる |

## 限界（「直近すべて」について）

- X は仮想スクロールのため、**スクロールしないと DOM に載らない投稿**があります。ここに書いた件数は、当セッションでスクロールして露出した範囲のサンプルです。
- 完全一致のポスト URL（`status/...`）はスナップショットからは安定取得できなかったため、**アプリ内で再検索する際の手がかり**としてハンドル＋要約＋外部リンクを載せています。
- 公式の全件エクスポートが必要な場合は、X の「設定 → データのアーカイブをダウンロード」で取得できる `bookmarks` 系ファイルを併用すると完全性が高いです。

## 再生成（500 件カタログ）

```bash
cd x_bookmarks
python3 parse_bookmark_snapshots.py
python3 merge_bookmark_sources.py
python3 build_bookmarks_catalog_md.py --limit 500 --date 2026-03-28
python3 build_bucket_reports.py
```

マージ件数が 500 を下回る場合は、`snapshot_dumps/extra_link_names.txt` を追記するか、フォルダタブをブラウザで切り替えて YAML を `snapshot_dumps/` に保存してから再度 `parse` → `merge` を実行してください。
