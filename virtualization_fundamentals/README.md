# 仮想化技術の基礎から実務設計まで

製品操作ではなく、仮想化に共通する原理から、小規模基盤の設計、運用、障害対応までを扱う解説書です。

## 状態

**執筆完了**（目次、第1章〜第15章、用語集、合本、完了チェックリスト）。

要件充足の確認は [COMPLETE.md](COMPLETE.md)。

| 区分 | ファイル | おおよその規模 |
|------|----------|----------------|
| 章ファイル一式 | `00`〜`15`、`99` | 約11,200行 |
| 通読用合本 | [BOOK_FULL.md](BOOK_FULL.md) | 約11,300行 |
| 完了確認 | [COMPLETE.md](COMPLETE.md) | チェックリスト |

## 読み始め

1. [完了チェックリスト](COMPLETE.md)（要件充足の確認）
2. [詳細目次・到達目標・ハンズオン・シナリオ前提](00_mokuji.md)
3. [第1章 仮想化の全体像](01_virtualization_overview.md) から順読、または [合本](BOOK_FULL.md)
4. 設計の結論を一気に見る場合は [用語集と確定設計サマリ](99_glossary_and_design_summary.md)

## 章一覧

| 章 | 内容 | ファイル |
|----|------|----------|
| 目次 | 目的、読者、ハンズオン、通貫シナリオ、到達目標 | [00_mokuji.md](00_mokuji.md) |
| 1 | 仮想化の全体像 | [01_virtualization_overview.md](01_virtualization_overview.md) |
| 2 | ハイパーバイザー | [02_hypervisor.md](02_hypervisor.md) |
| 3 | CPU仮想化 | [03_cpu_virtualization.md](03_cpu_virtualization.md) |
| 4 | メモリ仮想化 | [04_memory_virtualization.md](04_memory_virtualization.md) |
| 5 | ストレージ仮想化 | [05_storage_virtualization.md](05_storage_virtualization.md) |
| 6 | ネットワーク仮想化 | [06_network_virtualization.md](06_network_virtualization.md) |
| 7 | 仮想マシンのライフサイクル | [07_vm_lifecycle.md](07_vm_lifecycle.md) |
| 8 | 可用性とクラスタ | [08_availability_cluster.md](08_availability_cluster.md) |
| 9 | バックアップと災害対策 | [09_backup_dr.md](09_backup_dr.md) |
| 10 | 仮想化基盤のセキュリティ | [10_security.md](10_security.md) |
| 11 | コンテナとの比較 | [11_containers.md](11_containers.md) |
| 12 | クラウドとの関係 | [12_cloud.md](12_cloud.md) |
| 13 | サイジングとキャパシティ管理 | [13_sizing_capacity.md](13_sizing_capacity.md) |
| 14 | 仮想化基盤の設計 | [14_design.md](14_design.md) |
| 15 | 運用とトラブルシューティング | [15_operations_troubleshooting.md](15_operations_troubleshooting.md) |
| 付録 | 用語集と確定設計サマリ | [99_glossary_and_design_summary.md](99_glossary_and_design_summary.md) |
| 合本 | 全章結合（通読用） | [BOOK_FULL.md](BOOK_FULL.md) |
| 完了確認 | 要件チェックリスト | [COMPLETE.md](COMPLETE.md) |

## 通貫シナリオ（結論の要約）

- 業務VM 30台（重要8）、2年で約45台
- 推奨：物理ホスト **4台** クラスタ（N+1、成長と保守を考慮）
- 共有ストレージ：iSCSI（代替はNFS、分散ストレージ）
- ネットワーク：管理 / 業務 / ストレージ / マイグレーションをVLAN分離
- バックアップ：日次イメージ、遠隔へ週次、RPO 24時間、RTO 8時間（仮）

詳細な採用理由、不採用案、トレードオフ、SPOF、障害時挙動は第14章と付録を参照してください。

## 各章の共通構成

1. 学習目標
2. 背景と動作原理
3. 構成図（Mermaidまたはテキスト）
4. 製品非依存の共通概念と代表製品の実装例
5. 設計判断、性能、セキュリティ
6. 障害例と切り分け
7. 章末問題、解答、ハンズオン

## 注意

- 理論値（カタログ、計算上の上限）と実測値（監視値）を混同しない
- スナップショットはバックアップではない
- 仮想マシンとコンテナは分離モデルが異なる
- 設計は唯一解ではなく、制約下の選択として記録する
