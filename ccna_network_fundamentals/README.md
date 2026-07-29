# CCNAレベル 実務向けネットワーク解説書

資格暗記ではなく、設計・構築・障害対応に使える理解を目指す解説書です。

## 状態

**執筆完了**（目次、第1章〜第10章、合本、完了チェックリスト）。

要件充足の確認は [COMPLETE.md](COMPLETE.md)。

| 区分 | ファイル | おおよその規模 |
|------|----------|----------------|
| 章ファイル一式 | `00`〜`10` | 約6,800行 |
| 通読用合本 | [BOOK_FULL.md](BOOK_FULL.md) | 約6,900行 |
| 完了確認 | [COMPLETE.md](COMPLETE.md) | チェックリスト |

## 読み始め

1. [完了チェックリスト](COMPLETE.md)
2. [詳細目次・到達目標・通貫シナリオ](00_mokuji.md)
3. [第1章 ネットワークの全体像](01_network_overview.md) から順読、または [合本](BOOK_FULL.md)

## 章一覧

| 章 | 内容 | ファイル |
|----|------|----------|
| 目次 | 目的、読者、通貫シナリオ、到達目標 | [00_mokuji.md](00_mokuji.md) |
| 1 | ネットワークの全体像 | [01_network_overview.md](01_network_overview.md) |
| 2 | EthernetとLAN | [02_ethernet_lan.md](02_ethernet_lan.md) |
| 3 | IPアドレスとサブネット | [03_ip_subnet.md](03_ip_subnet.md) |
| 4 | TCP、UDPと主要プロトコル | [04_tcp_udp_protocols.md](04_tcp_udp_protocols.md) |
| 5 | VLANとスイッチング | [05_vlan_switching.md](05_vlan_switching.md) |
| 6 | ルーティング | [06_routing.md](06_routing.md) |
| 7 | 冗長化とループ防止 | [07_redundancy.md](07_redundancy.md) |
| 8 | NAT、ACL、ネットワークセキュリティ | [08_nat_acl_security.md](08_nat_acl_security.md) |
| 9 | 無線LAN | [09_wireless_lan.md](09_wireless_lan.md) |
| 10 | ネットワーク運用とトラブルシューティング | [10_operations_troubleshooting.md](10_operations_troubleshooting.md) |
| 合本 | 全章結合（通読用） | [BOOK_FULL.md](BOOK_FULL.md) |
| 完了確認 | 要件チェックリスト | [COMPLETE.md](COMPLETE.md) |

## 通貫シナリオ（要約）

- 本社＋支社の小規模企業
- 営業 / 開発 / 管理を VLAN 10 / 20 / 30 で分離
- DHCP、社内DNS、業務サーバー、インターネット接続
- 部署間を ACL で制限、機器を冗長化
- 第10章で障害切り分けを一連で扱う

## 各章の共通構成

1. 学習目標
2. 背景と基本概念
3. 通信の流れと構成例
4. Cisco設定、ホスト確認コマンド
5. 誤解、障害、切り分け、設計注意点
6. 要点まとめ、章末問題、演習
