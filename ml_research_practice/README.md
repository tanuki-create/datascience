# 機械学習の検証・R&D 実務ガイド

このディレクトリは、**プロダクト開発**（まず動くものを作り、UX とスケールを改善していく流れ）とは別軸で、**検証・研究開発**の仕事に必要な考え方をまとめるための場所です。

データサイエンスやモデル学習の個別ノウハウは、既に他のディレクトリで扱っています。ここは**その横に置く、縦串のマインドセット集**として使います。

## このディレクトリの位置づけ

- プロダクト開発: 動く → UX → スケール、という順で価値を積み上げる。要件が固まっていれば、実装力と運用力が差になる。
- 検証・R&D: 正解が定義しきれない状態で、**何を主張するか・何があれば覆るか・いつ止めるか**を自分で設計する必要がある。ここで効くのは、実装力よりも **問題設定、指標設計、不確実性の扱い** である。

アカデミックな訓練が薄い人ほど、この縦串の前提が曖昧になりやすく、結果として「頑張ったが何が進んだか説明できない」状態になりがちです。ここを埋めることがこのフォルダの目的です。

## ドキュメント構成

1. [research_validation_mindset_ja.md](./research_validation_mindset_ja.md)
   - 検証・R&D 向けのマインドセットとメンタルモデル
   - 仮説シート・実験カード・週次セルフレビューなど**そのまま使えるテンプレ**
   - 層別評価、オフラインとオンラインのズレ、打ち切り条件の具体化
   - 既存の実験・運用ドキュメントへの導線

2. [mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md)
   - MLOps の基本（DevOps との違い、不要なケース、成熟度、自己診断 10 問）
   - コアコンポーネント別の **Minimum / Full / よくある穴**、障害時の疑う順、PSI 目安
   - BOM 例、ロールアウト・キル条件、LLM 運用の足場
   - CI/CD・モニタリング・アンチパターン・成熟度チェックリスト

3. [world_class_case_studies_ja.md](./world_class_case_studies_ja.md)
   - 各章の読み方テンプレ（教訓・ミニ版・前提・取らない判断）
   - プラットフォーム / Feature Store / 実験 / 推薦 / 検索 / LLM / RAG など**章ごとの深掘り小節**
   - 共通パターンと投資判断表、自社投影ワークシート
   - 主要企業の公開事例をテーマ別に整理（一次情報で再確認前提）

## 他ディレクトリとの役割分担

このフォルダ（`ml_research_practice/`）は**縦串のマインドセット**を扱います。隣接ディレクトリとは次のように分担しています。

| ディレクトリ | 扱う範囲 | 本フォルダとの関係 |
|--------------|----------|--------------------|
| [system_operation_maintenance/](../system_operation_maintenance/) | **企業カスタム AI の運用・契約**（SLA、RACI、SRE、ガバナンス） | 本フォルダは「ML ライフサイクル標準化」、あちらは「組織・契約・SRE の運用」 |
| [system_design/16_ml_ai_systems/](../system_design/16_ml_ai_systems/) | ML システムの**設計**（推論、レコメンド、チャットボット） | 本フォルダから設計ガイドへ降りるための入口 |
| [object_detection/](../object_detection/) | **物体検出ドメイン固有**の実務（データ、学習、評価、導入） | 本フォルダの縦串を、物体検出ドメインに落とした具体例 |
| [dbconnection/07_data_ml_apps.md](../dbconnection/07_data_ml_apps.md) | データ分析・ML アプリの**データ基盤**側 | 本フォルダのデータ契約・特徴量論点の基盤層 |

## 関連ドキュメント（トピック別）

対象タスクに応じて、併読してください。

- 実験の作法・ベースライン・失敗解析: [object_detection/04_training_playbook.md](../object_detection/04_training_playbook.md)
- 指標の読み方と運用目的とのズレ: [object_detection/02_terms_and_metrics.md](../object_detection/02_terms_and_metrics.md)
- PoC から本番までの落とし所と ROI: [object_detection/05_applications_and_case_studies.md](../object_detection/05_applications_and_case_studies.md)
- AI 固有の運用・再現性・オンライン評価: [system_operation_maintenance/05_ai_specific_ops.md](../system_operation_maintenance/05_ai_specific_ops.md)
- 運用プレイブックとガバナンス雛形: [system_operation_maintenance/10_operational_playbooks_and_governance_hooks.md](../system_operation_maintenance/10_operational_playbooks_and_governance_hooks.md)
- ML システム全体の設計入口: [system_design/16_ml_ai_systems/README.md](../system_design/16_ml_ai_systems/README.md)
- 推論システム設計: [system_design/16_ml_ai_systems/ml_inference_design.md](../system_design/16_ml_ai_systems/ml_inference_design.md)
- クラウド GPU 学習の現場判断: [object_detection/12_cloud_gpu_training_practice.md](../object_detection/12_cloud_gpu_training_practice.md)

## 読み方

- プロダクト畑の人: まず [research_validation_mindset_ja.md](./research_validation_mindset_ja.md) の「開発モードの違い」と「メンタルモデル」だけ読む。そのうえで、自分の案件に関係する既存ドキュメントに降りる。
- 検証に本格的に入る前: 「改善数値の出し方」と「現実的な落とし所」を先に読み、評価設計と停止条件を決めてから実験に入る。
- 本番運用に関わる人: [mlops_fundamentals_ja.md](./mlops_fundamentals_ja.md) の「現場レベルの考え方」と「成熟度チェックリスト」を先に読み、今のチームの穴を特定する。
- 業界の相場感を掴みたい人: [world_class_case_studies_ja.md](./world_class_case_studies_ja.md) の「業界横断で共通する工夫のパターン」から入り、各社事例は辞書的に使う。
- レビューする立場: 「アカデミック訓練が薄いときの借りる厳密さ」と「MLOps アンチパターン」を評価軸として使い、チームの実験レポートや運用設計に何が足りないかを指摘する観点にする。
