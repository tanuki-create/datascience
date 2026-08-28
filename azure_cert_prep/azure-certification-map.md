# Azure資格の選び方（調査基準日：2026-08-27）

貼付された「Microsoft認定資格（Azure）早見表」を出発点に、2026-08-27時点のMicrosoft Learn公式ページで受験先を確認するためのマップへ整理したものです。

## 先に結論

クラウド未経験なら、最初の候補は **Microsoft Certified: Azure Fundamentals（試験AZ-900）** です。AZ-900はクラウド概念、Azureの主要サービス、管理・ガバナンスを広く学ぶ基礎試験で、AZ-104など特定の上位資格を先に取る必要はありません。ただし、AZ-900は上位資格の一律の必須条件ではなく、Microsoftが示す「一般的な出発点」です。

ただし、Microsoftの資格体系や試験コードは更新されます。試験を申し込む前に、必ず [Microsoft Learnの資格一覧](https://learn.microsoft.com/ja-jp/credentials/browse/) と対象資格ページを確認してください。

## 目的別の選択

| 目的 | 最初の候補 | 次の学習先の目安 | 判断の軸 |
|---|---|---|---|
| Azureとクラウドの全体像を知りたい | Microsoft Certified: Azure Fundamentals（AZ-900） | Azure Administrator Associate（AZ-104）など | まず共通語彙を作る |
| Azureを運用・管理したい | Azure Fundamentals（AZ-900） | Azure Administrator Associate（AZ-104） | VM、ネットワーク、ストレージ、ID、ガバナンスを実務寄りに深める |
| Azureネットワークを担当したい | Azure Fundamentals（AZ-900） | Azure Network Engineer Associate（AZ-700） | VNet、VPN、ExpressRoute、名前解決などを深める |
| Azureの設計・アーキテクチャを担当したい | Azure Fundamentals（AZ-900） | Azure Administrator Associate（AZ-104） → Azure Solutions Architect Expert（AZ-305） | AZ-104は学習順であるだけでなく、AZ-305の公式前提資格 |
| Azureデータ基盤を担当したい | Azure Data Fundamentals（DP-900） | Azure Database Administrator Associate（DP-300）、Cosmos DB Developer Specialty（DP-420）、Azure Databricks Data Engineer Associate（DP-750） | Azureの運用・データサービスのどこを担当するかで分岐 |
| Microsoft Fabricのデータ基盤を担当したい | データ基礎の学習 | Fabric Analytics Engineer Associate（DP-600）、Fabric Data Engineer Associate（DP-700） | DP-600／DP-700はAzure資格ではなくFabric資格 |
| AI・機械学習を担当したい | Azure AI Fundamentals（AI-901） | Azure AI Apps and Agents Developer Associate（AI-103）、Azure AI Cloud Developer Associate（AI-200）、Machine Learning Operations Engineer Associate（AI-300） | 旧試験コードの教材を固定的に使わない |
| セキュリティの基礎を知りたい | Security, Compliance, and Identity Fundamentals（SC-900） | Identity and Access Administrator Associate（SC-300）、Security Operations Analyst Associate（SC-200）など | AzureだけでなくMicrosoft 365を含むセキュリティ、コンプライアンス、IDの基礎 |

上表の「次の学習先」は学習順の目安であり、Microsoftが定める唯一のロードマップではありません。

## シリーズの見方

貼付記事では、Azureに関連する資格を AZ / AI / DP / SC の4シリーズとして整理しています。この分類は資格選択には便利ですが、Microsoft公式の「Azure資格」の定義として固定されたものではありません。

| 系列 | ざっくりした領域 | 初学者が最初に見る資格 |
|---|---|---|
| AZ | Azureのクラウド基盤、管理、ネットワーク、設計、DevOpsなど | AZ-900 |
| AI | Azure AI、AIアプリ、機械学習など | AI-901、AI-103、AI-200、AI-300 |
| DP | Azureデータ、SQL、Fabric、データエンジニアリングなど | AzureはDP-900、DP-300、DP-420、DP-750。FabricはDP-600、DP-700 |
| SC | セキュリティ、ID、情報保護、セキュリティ運用など | SC-900。Azureセキュリティの新しい後継候補はSC-500 |

## 2026年の移行情報

2026-08-27時点でMicrosoft公式の廃止一覧から確認できる主な情報は次のとおりです。廃止日や一覧は変更される可能性があります。

| 状態 | 試験コード | 資格名 | 廃止日 | 後継資格・試験 |
|---|---|---|---:|---|
| 廃止済み | DP-100 | Azure Data Scientist Associate | 2026-06-01 | Machine Learning Operations Engineer Associate（AI-300） |
| 廃止済み | AI-900 | Azure AI Fundamentals | 2026-06-30 | Azure AI Fundamentals（AI-901） |
| 廃止済み | AI-102 | Azure AI Engineer Associate | 2026-06-30 | Azure AI Apps and Agents Developer Associate（AI-103） |
| 廃止済み | AZ-204 | Azure Developer Associate | 2026-07-31 | Azure AI Cloud Developer Associate（AI-200） |
| 廃止予定 | AZ-500 | Azure Security Engineer Associate | 2026-08-31 | Cloud and AI Security Engineer Associate（SC-500） |
| 廃止予定 | AZ-800／AZ-801 | Windows Server Hybrid Administrator Associate | 2026-09-30 | Windows Server Administrator Associate（AZ-802） |

出典：[Exam and assessment lab retirement（Microsoft Learn）](https://learn.microsoft.com/en-us/credentials/support/retired-certification-exams)

DP-203（Azure Data Engineer Associate）は **2025-03-31に廃止済み**です。DP-700はMicrosoft Fabricの資格であり、DP-203と同一資格の直接後継とは扱わず、関連する現行のデータエンジニアリング選択肢として確認してください。([廃止表示](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-engineer/renew/)、[Fabric Data Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/))

### 現行候補の公式ページ

| 資格 | 試験コード | 公式ページ |
|---|---|---|
| Azure AI Fundamentals | AI-901 | [資格ページ](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/) |
| Azure AI Apps and Agents Developer Associate | AI-103 | [資格ページ](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/) |
| Azure AI Cloud Developer Associate | AI-200 | [資格ページ](https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-cloud-developer-associate/) |
| Machine Learning Operations Engineer Associate | AI-300 | [資格ページ](https://learn.microsoft.com/en-gb/credentials/certifications/operationalizing-machine-learning-and-generative-ai-solutions/) |

### 前提条件の確認

- **AZ-305**の公式前提資格は **Azure Administrator Associate（AZ-104）** です。AZ-900は一般的な出発点ですが、AZ-305の前提資格ではありません。([AZ-305資格ページ](https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/))
- DP-900はAzureデータ系資格の学習準備には使えますが、Azure Database Administrator Associateなどの前提資格ではありません。([DP-900資格ページ](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-fundamentals/))
- 上記以外の前提条件、試験の対応関係、後継資格の提供状態は変更される可能性があるため、受験前に必ず各資格ページと廃止一覧を確認してください。

### この記事を教材に使うときの注意

- 貼付記事の資格数・ロードマップは、記事作成者の整理と、その時点の情報を含みます。現在の受験可否や認定要件を保証するものではありません。
- 新しい試験コードや後継資格は、名称が似ていても試験範囲・認定要件が異なる場合があります。記事の表だけで受験先を決めないでください。
- 廃止が近い試験をこれから学び始める場合は、受験予約が可能か、後継資格が一般提供されているかを公式資格ページで確認してから教材を選びます。特にDP-203→DP-700は、資格の直接後継ではなく、Fabricへの領域移行を含むため要確認です。
- 廃止済み資格を取得済みの場合、廃止によって直ちに履歴から消えるわけではありませんが、廃止後は新規取得や更新ができません。([資格廃止ポリシー](https://learn.microsoft.com/en-us/credentials/support/credential-retirement))
- 本フォルダーの本編は、現行の [AZ-900学習ガイド](https://learn.microsoft.com/ja-jp/credentials/certifications/resources/study-guides/az-900) に合わせています。

## 受験先を決める3問

1. Azureを使う目的は、全体理解、運用、ネットワーク、データ、AI、セキュリティのどれか。
2. 3か月後に実務で触るサービスは何か。
3. 試験コードと学習ガイドが、Microsoft公式ページで現在も有効か。

この3問に答えられない場合は、まずAZ-900の学習を始め、2週間後に専門領域を再判定するのが合理的です。

## 公式リンク

- [Microsoft資格を確認する](https://learn.microsoft.com/ja-jp/credentials/browse/)
- [Microsoft認定: Azure Fundamentals](https://learn.microsoft.com/ja-jp/credentials/certifications/azure-fundamentals/)
- [試験AZ-900の学習ガイド](https://learn.microsoft.com/ja-jp/credentials/certifications/resources/study-guides/az-900)
- [Microsoft認定資格の廃止情報](https://learn.microsoft.com/ja-jp/credentials/support/credential-retirement)
