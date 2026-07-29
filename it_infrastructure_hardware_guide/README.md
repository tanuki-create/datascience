# ITインフラエンジニアのためのハードウェア基礎・実務解説書

**執筆状態：完了（FINAL）**

要件充足の確認は [COMPLETE.md](COMPLETE.md)。

コンピューターハードウェアの構成要素と動作原理を、選定・冗長化・障害対応の実務に結びつけて学ぶ解説書です。

架空の中規模企業「北風商事」のオンプレミス構成を全章で共通利用します。

## 完成物

| 種別 | ファイル | 内容 |
|---|---|---|
| 完了確認 | [COMPLETE.md](COMPLETE.md) | 要件チェックリスト |
| 通読用一冊版 | [COMPLETE_BOOK.md](COMPLETE_BOOK.md) | 概要〜シナリオまで結合した完成稿 |
| 章分割版 | `00`〜`15` | 章ごとの編集・参照用 |
| 案内 | 本ファイル | 読み順と一覧 |

## 読み順

1. [COMPLETE.md](COMPLETE.md)（完了確認）
2. [00_overview.md](00_overview.md)（目次・到達目標・仮想構成）
3. 第1章から第14章を順に読む
4. [15_practical_scenarios.md](15_practical_scenarios.md) で統合演習

一括で読む場合は [COMPLETE_BOOK.md](COMPLETE_BOOK.md) を開く。

## 章一覧

| 章 | ファイル |
|---|---|
| 概要 | [00_overview.md](00_overview.md) |
| 第1章 全体像 | [01_computer_hardware_overview.md](01_computer_hardware_overview.md) |
| 第2章 CPU | [02_cpu.md](02_cpu.md) |
| 第3章 メモリ | [03_memory.md](03_memory.md) |
| 第4章 ストレージ | [04_storage_devices.md](04_storage_devices.md) |
| 第5章 RAID | [05_raid.md](05_raid.md) |
| 第6章 マザーボード | [06_motherboard_interfaces.md](06_motherboard_interfaces.md) |
| 第7章 NIC | [07_network_interface.md](07_network_interface.md) |
| 第8章 電源と冷却 | [08_power_cooling.md](08_power_cooling.md) |
| 第9章 ラックとファシリティ | [09_chassis_rack_datacenter.md](09_chassis_rack_datacenter.md) |
| 第10章 ファームウェアとBMC | [10_firmware_bmc.md](10_firmware_bmc.md) |
| 第11章 GPU | [11_gpu_accelerators.md](11_gpu_accelerators.md) |
| 第12章 周辺機器 | [12_peripherals.md](12_peripherals.md) |
| 第13章 選定とサイジング | [13_sizing_selection.md](13_sizing_selection.md) |
| 第14章 障害診断と保守 | [14_troubleshooting_maintenance.md](14_troubleshooting_maintenance.md) |
| 実務シナリオ | [15_practical_scenarios.md](15_practical_scenarios.md) |

## 必須構成の充足

- 第1章〜第14章：学習目標、役割、原理、指標、関係、選定、構成例、誤解、障害、注意点、章末問題、解答、実務演習
- 実務シナリオ：S1〜S7（性能・信頼性・保守性・停止リスク・コストのトレードオフ付き）
- 共通仮想構成：北風商事（hv / db / web / bk / mgmt）

## 注意

- 製品スペックや価格は世代・時期で変わります。数値例は理解用です
- 電気工事、消火、耐震などの施設作業は有資格者と手順に従ってください
- 本番作業は保守契約、変更管理、バックアップ確認を前提にしてください
