# 企業向けカスタムAI — 運用・保守ドキュメント

企業に **カスタム開発で** 導入する AI ソリューション（生成AI・RAG・エージェント等を含む）について、**導入プロジェクト中**から **本番稼働後**までを対象に、運用・保守で「現場で差がつく前提」と「争点の整理」をまとめた資料集です。

## この資料の位置づけ

- **対象**: 顧客企業の IT／事業オーナー、ベンダー側の PM・アーキテクト・SRE、セキュリティ・法務など、導入〜契約〜引き渡し後まで関わるロール。
- **スコープ**: **カスタム開発が中心**（ベンダー標準SaaSだけ利用のケースとは責務境界が違う点を前提に書いています）。
- **狙い**: PoC と本番のギャップ、TCO、責務分界、AI 固有の「品質・コスト・安全」の継続管理を、**メンタルモデル**と**合意形成**まで含めて揃える。

## 用語（主要）

| 用語 | 概要 |
|------|------|
| **SLA** (Service Level Agreement) | サービス品質を契約で約束する文書。違反時の救済とセットで読む。 |
| **SLO** (Service Level Objective) | 内部目標。ユーザー体験とコストのバランスを設計する単位。 |
| **SLI** (Service Level Indicator) | SLO を測る指標（可用性、遅延、エラー率など）。 |
| **RTO** (Recovery Time Objective) | 障害からどれくらいで復旧すべきか（時間）。 |
| **RPO** (Recovery Point Objective) | どれくらい前のデータまで戻せればよいか（許容データ損失）。 |
| **DR** (Disaster Recovery) | 災害・大規模障害時の復旧設計・手順。 |

## 文書マップ

| ファイル | 内容 |
|----------|------|
| [01_mental_models_and_reality.md](./01_mental_models_and_reality.md) | 素人とプロで差がつく前提・本番の現実 |
| [02_delivery_and_contracts.md](./02_delivery_and_contracts.md) | 導入前〜中：契約、受入、サポート境界 |
| [03_architecture_for_operations.md](./03_architecture_for_operations.md) | 運用に効くアーキテクチャ・環境・境界 |
| [04_observability_sre_and_incidents.md](./04_observability_sre_and_incidents.md) | 監視・SRE・障害対応 |
| [05_ai_specific_ops.md](./05_ai_specific_ops.md) | AI 固有の運用（モデル・RAG・コスト・安全） |
| [06_change_release_and_data_governance.md](./06_change_release_and_data_governance.md) | 変更管理・リリース・データガバナンス |
| [07_professional_tensions.md](./07_professional_tensions.md) | プロ同士の争点と合意の進め方 |
| [08_maturity_roadmap.md](./08_maturity_roadmap.md) | 成熟度とチェックリスト |
| [09_pro_field_notes_2026.md](./09_pro_field_notes_2026.md) | **2026-04 時点**のプロ知見（**OWASP Agentic 2026 / MCP ガイド**、LLM Top 10 2025、NIST AI 600-1、EU AI Act Service Desk、Evals 等） |
| [10_operational_playbooks_and_governance_hooks.md](./10_operational_playbooks_and_governance_hooks.md) | **運用ひな形**（重大度、RACI、初動、定例、チケット分類、NIST/ISO 接続） |
| [11_staffing_and_capacity.md](./11_staffing_and_capacity.md) | **人員・稼働（FTE）目安**（経営・現場、フェーズ別・規模別） |

## いつ・誰が・どの順で読むか

**導入前（契約・提案）**

1. [01](./01_mental_models_and_reality.md) … 期待値とコスト感の共通言語を揃える。
2. [02](./02_delivery_and_contracts.md) … 何が「引き渡し」で、何が「運用」かを契約レベルで固定。
3. [07](./07_professional_tensions.md) … 早期に揉める論点を表にし、意思決定者を並べる。
4. [11](./11_staffing_and_capacity.md) … **社内・ベンダー**の必要人員と **FTE 目安**（予算・稟議・兼務の現実）。

**導入中（設計・実装・受入）**

1. [03](./03_architecture_for_operations.md) … 本番で回る構成・秘匿・デプロイ境界。
2. [04](./04_observability_sre_and_incidents.md) … 監視・Runbook・オンコールの「空箱」まで作る。
3. [05](./05_ai_specific_ops.md) … 評価・バージョン・RAG・コスト上限。
4. [06](./06_change_release_and_data_governance.md) … リリースとデータ取扱の門番。
5. [10](./10_operational_playbooks_and_governance_hooks.md) … 重大度・RACI・引き渡し後30日・定例アジェンダを **そのままコピー用**に。

**導入後（安定運用・改善）**

1. [04](./04_observability_sre_and_incidents.md) … インシデントから学習するサイクル。
2. [05](./05_ai_specific_ops.md) … ドリフト・プロバイダ変更・回帰評価。
3. [06](./06_change_release_and_data_governance.md) … 変更とコンプライアンスの継続監査。
4. [08](./08_maturity_roadmap.md) … 次の投資先の優先順位付け。
5. [09](./09_pro_field_notes_2026.md) … **最新のプロ現場知見**（セキュリティ対応表・エージェント・評価の落とし穴）を一冊に凝縮。
6. [10](./10_operational_playbooks_and_governance_hooks.md) … 障害初動・週次/月次運用・ガバナンス（NIST AI RMF / ISO 42001）との **対応表**。
7. [11](./11_staffing_and_capacity.md) … 定常・改善フェーズの **稼働を見直す**（四半期レビューに相性が良い）。

## 更新方針

- 法規・クラウド・モデルプロバイダの仕様は変わるため、**原理（責務・測り方・変更の扱い）** を核にし、数値 SLA の例は「契約時に各自で再検証する」前提とする。
- プロジェクト固有の Runbook・連絡網は本リポジトリの一般論をベースに、顧客・ベンダー内の **秘密情報** として別管理する。
- セキュリティ標準やプロバイダ仕様は更新が速いため、**四半期**に [09](./09_pro_field_notes_2026.md) 冒頭の **2026 追従リスト**（OWASP Agentic 2026・MCP ガイド・NIST AI 600-1・EU AI Act Service Desk）と OWASP GenAI 全体の差分を見直すことを推奨する。
