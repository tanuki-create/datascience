# 09 — プロの現場知見スナップショット（2026-04-01 までに効いていること）

本章は、章 [01](./01_mental_models_and_reality.md)〜[08](./08_maturity_roadmap.md) の **補遺**として、2024〜2026 年にかけて現場で繰り返し意思決定に効いた **具体的な論点**をまとめたものです。個別ベンダーの仕様変更日は **公式の deprecation / changelog を常に優先**してください（ここでは原理とチェック項目中心）。

---

## 2026年春 — 公式側の動き（OWASP / NIST / EU）

**スナップショット日: 2026-04-01**。以降も **原版の改訂**を追うこと。

### OWASP GenAI Security Project（2026-03-17 前後のコミュニティ更新）

RSAC 2026（サンフランシスコ、**3/23–26**）に合わせ、**エージェント／MCP／レッドチーム調達**まわりの参照資料が一段揃った。カスタム開発の **受入れ・設計レビュー**では、少なくとも次をブックマークし、**四半期で版差分**を見るのがプロのデフォルトになりつつある。

| リソース | URL | 運用・保守での使い所 |
|----------|-----|----------------------|
| **Top 10 for Agentic Applications（2026）** | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | ツール・ループ・メモリを載せた構成の **脅威モデル**、リリースゲート |
| **Secure MCP Server Development（実務ガイド）** | https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/ | MCP 公開時の **ハードニング**、権限・認証のレビュー観点 |
| **AIBOM / SBOM Generator** | https://genai.owasp.org/resource/owasp-aibom-generator/ | LLM03（Supply Chain）対応の **部品表**生成・棚卸し |
| **Vendor Evaluation Criteria for AI Red Teaming v1.0** | https://genai.owasp.org/resource/owasp-vendor-evaluation-criteria-for-ai-red-teaming-providers-tooling-v1-0/ | 外部レッドチーム／自動スキャン **ベンダー比較**の RFP |
| **AI Security Solutions Landscape** | https://genai.owasp.org/ai-security-solutions-landscape/ | ライフサイクル横断の **ツールマッピング**（Q2 2026 更新版がリリース文脈に登場） |

コミュニティ会合の一例: [OWASP GenAI Security Summit 2026（3/25）](https://genai.owasp.org/event/rsac-conference-2026-owasp-ai-security-summit-safeguarding-genai-agents-autonomous-ai-risk-2026/)。一次の説明はプロジェクトの [ニュース／ブログ](https://genai.owasp.org/news/) を参照。

**LLM アプリ向け Top 10（2025 版）** との関係: 次節 §1 は **アプリ＋モデル呼び出し**中心。**Agentic 2026** は **自律・ツール連鎖・MCP** の論点が増えた版として **併用**する（どちらか一方で「十分」とは限らない）。

### NIST — Generative AI Profile（AI RMF 派生）

NIST は **2024-07-26**、AI RMF に沿った生成AI向けプロファイル **[NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1)**（*Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*）を公開している。本体フレームは [AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)。実装例・Playbook は [Trustworthy & Responsible AI Resource Center (AIRC)](https://airc.nist.gov/) を定期確認すると、米国連邦・大手企業の **評価・調達**文脈との言語整合が取りやすい。

### EU AI Act — 実装タイムラインは法務と追う

EU 域内の顧客・データ・展開がある場合、**適用フェーズは法改正の影響を受けうる**。技術側は「どの機能が high-risk / 透明性 / GPAI 義務の説明責任に触れるか」を **法務・DPO とチケットで固定**し、ログ・人間監督・表示・リスク管理の **製品要件**に落とす。公式の整理の出発点として欧州委員会の **[EU AI Act — implementation timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline)**（AI Act Service Desk）を参照。**本資料は法令解釈を代替しない**。

---

## 1. セキュリティ：OWASP Top 10 for LLM Applications（2025 版）と運用の対応表

OWASP GenAI Security Project が **2024-11-17** に公表した [Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) は、企業カスタム開発の **受入れ・監査・Runbook** の共通言語になっています。リスク ID と「運用で何をするか」を対応づけるとレビューが速いです。

| ID | リスク（概要） | 運用・保守でやること（プロ視点） |
|----|----------------|----------------------------------|
| **LLM01:2025** | [Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)（直接・間接・マルチモーダル含む） | ツール権限の最小化、**信頼境界の分離**（ユーザー生入力をツール引数に直結しない）、間接注入想定の **RAG パイプライン設計**、昇格操作は HITL 必須 |
| **LLM02:2025** | [Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/) | ログ・トレースの **マスキング方針**、学習利用 opt-in、**プロンプト/応答の保持期間**、レッドチームでの抽出試験 |
| **LLM03:2025** | [Supply Chain](https://genai.owasp.org/llmrisk/llm032025-supply-chain/) | **AIBOM / SBOM** 相当の部品表、埋め込みモデル・ランキャスト・SDK の **ハッシュ/版固定**、サブプロセッサ変更の通知プロセス（→ [06](./06_change_release_and_data_governance.md)） |
| **LLM04:2025** | [Data and Model Poisoning](https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/) | 取込ソースの **改ざん検知・監査証跡**、再インデックス前の **サンプル検証**、ファインチューンDataのゲート |
| **LLM05:2025** | [Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/) | LLM 出力を **そのまま SQL/シェル/HTTP** に流さない、スキーマ検証・ allowlist、クライアント側 XSS 等の古典対策とセット |
| **LLM06:2025** | [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) | 「できること」の一覧とデフォルトOFF、**多段エージェントの予算**（反復上限・時間上限・コスト上限）、危険ツールは **承認キュー** |
| **LLM07:2025** | [System Prompt Leakage](https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/) | システムプロンプトに **秘密を書かない**、漏えいを検知したときの **ローテーション手順**、クライアント配布物との境界 |
| **LLM08:2025** | [Vector and Embedding Weaknesses](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/) | **埋め込みモデル変更**時の再インデックス計画、近傍汚染・ACL 不整合の監視、距離閾値と「検索不能」の扱い |
| **LLM09:2025** | [Misinformation](https://genai.owasp.org/llmrisk/llm092025-misinformation/) | 引用必須ポリシー、人間向け **免責と表示**、業務クリティカル用途では **自動実行を切る**、評価セットでの **事実性**メトリクス |
| **LLM10:2025** | [Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) | トークン/リクエスト/並列の **ハード上限**、ループ検知、**異常検知アラート**、DDoS と滥用的内部利用の両方を想定 |

**素人との差**: チェックリストを「セキュリティ部門の品質保証」ではなく **リリースゲートと監視ダッシュボード**に埋め込むと、本番で回る。

関連リソース: [Governance Checklist](https://genai.owasp.org/resource/llm-applications-cybersecurity-and-governance-checklist-english/)、[Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)。**2026 年版のエージェント網羅**は冒頭の [Agentic Top 10（2026）](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) を追加で追う。

---

## 2. エージェント / ツール呼び出しの「現場で効く」設計論

2025〜2026 は **ツールと権限**がセキュリティ・運用の主戦場です（OWASP の LLM05/06/10 と重なる）。

- **人間と同じ権限を AI に渡さない**: サービスプリンシパル1本で「何でもできる」構成は、侵害時の **ブラスト半径**が広すぎる。
- **承認トークン / ステップアップ認証**: 「読む」「提案する」「実際に書く」の間に、ビジネスが許容する **HITL またはポリシーエンジン**を挟む。
- **冪等キーと重複実行**: リトライ・ワーカー二重起動で **二重計上・二重送信**が起きる。決済・メール・チケット操作は特に **idempotency-key** を標準装備。
- **ツール入力のバリデーション**: モデルは JSON を「それっぽく」出す。**スキーマ検証**（構造化出力 / strict JSON schema 等）で弾くのは前提。失敗時は **ユーザーに直させる**のではなく **自動リトライ回数を制限**しログに残す。
- **MCP・外部統合**: エンドポイント追加が速いほど、**誰がいつどのスコープを有効化したか**の監査がボトルネックになる。本番トグルは **二人承認**や環境別フラグで縛るのが定石。実装の観点は OWASP の [Guide for Secure MCP Server Development](https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/) をレビューチェックリストに組み込む。

---

## 3. API・モデル版の「漂流」とプロダクション運用

**素人**: 最新モデルに追従すれば品質は上がる。  
**現場**: **変更は常に回帰リスク**。以下は 2026 年時点のプロのデフォルトです。

1. **モデル ID のピン留め**（「最新の GPT-x」系の本体指定は避け、**明示 ID** を設定ファイルで固定）。
2. **Structured outputs / strict schema** を業務クリティカルフローに適用し、**パース失敗率**を SLI に入れる（→ [04](./04_observability_sre_and_incidents.md)）。
3. **プロバイダ横断**を狙うなら **アダプタ層**で「機能フラグ（reasoning 強・ツール・画像）」の差分を吸収し、BOM に **互換マトリクス**を添える。
4. **Deprecation**: 公式の Deprecations / Changelog / メール通知を **RSS・週次レビュー**に乗せる。契約では「○日通知なき破壊的変更」の扱いを明記（→ [02](./02_delivery_and_contracts.md)）。
5. **Assistants / 古い API 形態の移行**: ベンダーが推す新 API（例: 会話状態の持ち方の変更）に対し、**セッションストア・添付ファイルライフサイクル**を設計し直すマイグレーション工数を見積もる（「ラップするだけ」で済まないことが多い）。

---

## 4. RAG のプロ運用：2025〜2026 で強まった論点

- **長コンテキスト神話**: コンテキスト窓が伸びても **「全部読めば正しい」にはならない**。注意の枯渇・途中の矛盾・コスト。現場は **検索品質＋適切なチャンク＋要約段**のほうが効くことが多い。
- **ハイブリッド検索**: キーワード（BM25 等）＋ベクタの **重み付け**はドメイン依存。**ゼロヒット**と **ノイズ上位**の両方を SLI で見る。
- **ACL の最終障壁**: 検索層の ACL ミスは **コンプラインシデント**。同期遅延・テナント混入を **合成監視**（「このユーザーでは取れないドキュメントがヒットしない」）で補うチームが増えている。
- **埋め込み／チャンカーのバージョン**: 「再インデックス無しで埋め込みモデルだけ差し替え」は **検索空間が別物**になり得る。世代タグと **切替手順（二段インデックス）** が標準（→ [06](./06_change_release_and_data_governance.md)）。

---

## 5. 評価（Evals）の運用品質：プロだけがやる落とし穴対策

- **LLM-as-judge の盲信**: 判定用モデルも **ドリフト**し、プロンプトバイアスも乗る。**人間ラベル**との **校合（calibration）**と、ジャッジ自身の **バージョンピン**が必要。
- **ゴールデンセットの汚染**: 本番ログから拾いすぎると **テスト漏れがテストに入る**。定期的に **人間が追加する対抗例**を混ぜる。
- **オンライン指標とのギャップ**: オフラインで勝っても本番で負ける。**カナリア**と **実ユーザ行動**（再試行、コピー率、エスカレーション率）をセットで見る。
- **セーフティと品質の分離**: 「拒否が増えた」は **ポリシー変更**か **入力分布の変化**か。ダッシュボードを分ける。

---

## 6. コスト・性能：2026 年の現場感

- **Thinking / reasoning 系**: 遅延とコストが **尾部で暴れやすい**。**p99 と請求の相関**を週次で見るチームが生存しやすい。
- **キャッシュ**: ヒット率と **鮮度スロット**（TTL）を政策として決める。機密案件ではキャッシュ禁止ゾーンを分ける。
- **バッチ・非同期**: リアルタイムでなくてよい業務は **キュー＋バックプレッシャ** が請求と SLO を救う。

---

## 7. 組織：シャドウIT・BYOK・ガバナンス

- **シャドウAI**: 公式システムより **ブラウザ版Chat** が速いと現場が流れる。公式チャネルが **同等かそれ以上に速く安全**であること、データ区分の教育がないと止まらない。
- **BYOK**: キー持ち込みはデータレジデンシには効くが、**キーローテーション・失効・誤設定**の運用が顧客側に寄る。Runbook の **RACI** を明示（→ [03](./03_architecture_for_operations.md)）。

---

## 8. プロの争点（2025〜2026 で温度が上がりやすいテーマ）

[07](./07_professional_tensions.md) の補足として、現場で頻出した論点です。

| 争点 | 一度決めないと起きること |
|------|---------------------------|
| **自律性のレベル**（提案のみ vs 自動実行） | コンプラ・監査がシステムを止める / 逆に手が足りなくなる |
| **ログの粒度** | インシデントで二度手間 vs プライバシー監査で赤入れ |
| **単一プロバイダ依存** | 価格改定・レート制限で計画崩壊 vs マルチの複雑さ |
| **「正しい幻覚」**（一貫したが誤った説明） | KPIは悪くないが **事業リスク** — メトリクス設計が前提 |

---

## 9. 週次〜月次で回す「一流寄り」の習慣（短尺）

- **週次**: 主要 SLI、請求、ベンダー障害ステータス、未解決インシデント、評価セットの **差分**。
- **月次**: 脅威モデル差分、サブプロセッサ一覧、データ分類の例外、**ゲームデイ**または **復旧手順のドライラン**の予定。
- **四半期**: AIBOM 更新、ペネテ・レッドチーム（範囲明示）、DR/RPO の実測。

---

## 10. 参照・更新のしかた

- OWASP GenAI（総合）: https://genai.owasp.org/
- **LLM Top 10（2025）**: https://genai.owasp.org/llm-top-10/ — リスク個別は `genai.owasp.org/llmrisk/...`（2025 版 ID）
- **Agentic Top 10（2026）**: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- **NIST GenAI Profile**: https://doi.org/10.6028/NIST.AI.600-1
- **EU AI Act 実装タイムライン（欧州委員会）**: https://ai-act-service-desk.ec.europa.eu/en/ai-act/eu-ai-act-implementation-timeline

**本ドキュメントの鮮度**: 日付付きの事実（例: Top 10 for LLM 2025 の **2024-11-17** 公表、NIST AI 600-1 の **2024-07-26**、OWASP ブログ更新 **2026-03-17** 前後）は **当該公式ページ**に依拠。ベンダー固有情報は **導入時の公式ドキュメント**で差し替えること。

前後の章: [08 — 成熟度ロードマップ](./08_maturity_roadmap.md) · [10 — 運用Playbook・ガバナンス接続](./10_operational_playbooks_and_governance_hooks.md) · [README](./README.md)
