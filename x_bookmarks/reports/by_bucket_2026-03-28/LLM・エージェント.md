# バケットレポート: LLM・エージェント

対象: [`_merged_bookmarks.tsv`](../_merged_bookmarks.tsv) 全行をキーワードルールで分類。**104 件**がこのバケットに該当（1行が複数バケットに載ることはありません: 先にマッチしたタグのみ）。

## 今あらためて見るべきポイント（抜粋）

長さ・情報密度が高い行と、公式/製品/研究らしきキーワードを優先して列挙。**一次ソースで更新**してから判断してください。

1. **要点**: Cline @cline 3月26日 Introducing Cline Kanban: A standalone app for CLI-agnostic multi-agent orchestration. Claude and Codex compatible. npm i -g cline Tasks run in worktrees, click to review diffs, & l
2. **要点**: Google Research @GoogleResearch 3月25日 GIF Introducing TurboQuant: Our new compression algorithm that reduces LLM key-value cache memory by at least 6x and delivers up to 8x speedup, all with zero accu
3. **要点**: Google Research @GoogleResearch 3月25日 Introducing TurboQuant: Our new compression algorithm that reduces LLM key-value cache memory by at least 6x and delivers up to 8x speedup, all with zero accuracy
4. **要点**: Google for Developers @googledevs 3月26日 Provide coding agents with the Gemini API developer skill. The skill provides agents with the latest SDK knowledge: API feature sets Current models and SDKs Sam
5. Brady Long @thisguyknowsai 17時間 BREAKING: A self-taught developer from Brazil just cracked the context window problem that's been plaguing RAG systems for 2 years. No PhD. No research lab affiliation.
6. Cline @cline 3月26日 Introducing Cline Kanban: A standalone app for CLI-agnostic multi-agent orchestration. Claude and Codex compatible. npm i -g cline Tasks run in worktrees, click to review diffs, & l
7. Google Research @GoogleResearch 3月25日 GIF Introducing TurboQuant: Our new compression algorithm that reduces LLM key-value cache memory by at least 6x and delivers up to 8x speedup, all with zero accu
8. Google Research @GoogleResearch 3月25日 Introducing TurboQuant: Our new compression algorithm that reduces LLM key-value cache memory by at least 6x and delivers up to 8x speedup, all with zero accuracy
9. Google for Developers @googledevs 3月26日 Provide coding agents with the Gemini API developer skill. The skill provides agents with the latest SDK knowledge: API feature sets Current models and SDKs Sam
10. **要点**: はやっち @ AI Business Lab @HayattiQ 3月14日 Claude code でエンジニア終わった論だが、あれから更に俯瞰してみてみると 1. 今までエンジニアがやってたコーディングは本当に無くなった。コーダーは終了 2. 機能開発のスピードは爆速になったが、今までより速く大量の施策を打たなければならなくなった。企画や仕様まで出来る上級SE的仕事が爆増
11. はやっち @ AI Business Lab @HayattiQ 3月14日 Claude code でエンジニア終わった論だが、あれから更に俯瞰してみてみると 1. 今までエンジニアがやってたコーディングは本当に無くなった。コーダーは終了 2. 機能開発のスピードは爆速になったが、今までより速く大量の施策を打たなければならなくなった。企画や仕様まで出来る上級SE的仕事が爆増
12. **要点**: 「**Cline**（@cline）紹介ポストの引用。**Cline Kanban**」に関するメモ: CLI 非依存のマルチエージェント用スタンドアロンアプリ。Claude / Codex 互換、`npm i -g cline`、ワークツリー・差分レビュー等（文中切れ）。

## GitHub リポジトリ（行から抽出）

- [https://github.com/FoundationVision/VAR](https://github.com/FoundationVision/VAR)
- [https://github.com/obra/superpowers](https://github.com/obra/superpowers)

（2 件。表記ゆれで重複・薄い言及が混じる場合があります。）

## 示唆・読み方

**推論コストとコンテキスト**が中心。TurboQuant 系（KV 圧縮・量子化）は自前・端末運用の単価に直結するため、公式ブログと実装の追従をセットで。RAG / Mythos 等のバズ系は「再現・一次ソース」を確認してから設計に載せるのが安全。Embedding・ドメイン特化ベクトルは検索品質のレバーなので、HF 記事と社内データの距離感をセットで見直す価値あり。

---

- 全文500件カタログ: [`bookmarks_500_2026-03-28.md`](../bookmarks_500_2026-03-28.md)
- 全体分析: [`analysis_500_2026-03-28.md`](../analysis_500_2026-03-28.md)
