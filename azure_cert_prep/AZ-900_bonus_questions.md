# AZ-900 追加確認問題（公式カバレッジ補完）

本編の不足項目を補うためのオリジナル4択問題です。実在の試験問題の再現ではありません。各問の正解は1つです。

## 問題

### Q1｜Azure CLIとAzure PowerShell

Linux環境で作業する管理者が、Bashスクリプトに組み込みやすい構文でAzureリソースを管理したいとします。最も適したコマンドラインツールはどれですか。

A. Azure CLI

B. Azure PowerShell

C. Azure Cloud Shell

D. Azure portal

**正解：** A

**短い解説：** Azure CLIはBashに近い構文で利用しやすいコマンドラインツールです。Azure PowerShellはPowerShellのコマンドレットを使います。Cloud Shellは、これらのツールを実行できるブラウザー上の環境です。

**対応する公式項目：** Describe Azure Cloud Shell, Azure CLI, and Azure PowerShell

### Q2｜Azure Cloud Shell

自分のPCにAzure CLIやAzure PowerShellをインストールせず、ブラウザーから認証済みのシェルを開いてAzureを管理したいとします。最も適したものはどれですか。

A. Azure Resource Manager

B. Azure Arc

C. Azure Cloud Shell

D. Azure Advisor

**正解：** C

**短い解説：** Azure Cloud Shellはブラウザーから利用できる認証済みのシェル環境です。BashまたはPowerShellを選択でき、Azure CLIやAzure PowerShellが用意されています。

**対応する公式項目：** Describe Azure Cloud Shell, Azure CLI, and Azure PowerShell

### Q3｜ARMテンプレート

開発・テスト・本番で同じ構成のAzureリソースを繰り返しデプロイしたいとします。リソースと構成を宣言的に定義するJSONファイルとして最も適したものはどれですか。

A. Azure Policy

B. ARMテンプレート

C. Azure Monitorアラート

D. Azure RBACロール定義

**正解：** B

**短い解説：** ARMテンプレートはAzureリソースと構成をJSONで宣言的に定義し、再現性のあるデプロイに利用します。Azure Policyはルールの準拠を評価・適用する機能です。

**対応する公式項目：** Describe Azure Resource Manager (ARM) and ARM templates

### Q4｜Infrastructure as Code（IaC）

インフラ構成をアプリケーションコードと同じようにリポジトリで管理し、変更履歴をレビューして同じ環境を再現したいとします。この考え方はどれですか。

A. 多要素認証（MFA）

B. 垂直スケーリング

C. データレジデンシー

D. Infrastructure as Code（IaC）

**正解：** D

**短い解説：** IaCは、インフラの構成をコードとして管理し、レビュー、バージョン管理、再現可能なデプロイを行う考え方です。ARMテンプレートやBicepはAzureでIaCを実現する手段の例です。

**対応する公式項目：** Describe infrastructure as code (IaC)

### Q5｜Azure Arc

自社データセンターにあるWindows ServerをAzureへ移行せず、Azure portalからAzureリソースとして整理し、ポリシーを適用したいとします。最も適した仕組みはどれですか。

A. Azure Arc

B. Azure Data Box

C. Azure Virtual Machine Scale Sets

D. Azure ExpressRoute

**正解：** A

**短い解説：** Azure Arcを使うと、オンプレミスや他クラウド上の対応サーバーなどをAzureのリソースとして表現し、Azureから管理・統制できます。ArcはサーバーをAzureへ移行するサービスではありません。

**対応する公式項目：** Describe the purpose of Azure Arc

### Q6｜Microsoft Purview

複数のデータソースに存在するデータ資産を発見し、メタデータや分類情報を確認して、組織のデータガバナンスに役立てたいとします。最も適したサービスはどれですか。

A. Azure Policy

B. Azure Service Health

C. Microsoft Purview

D. Azure Load Balancer

**正解：** C

**短い解説：** Microsoft Purviewは、データ資産の発見、カタログ化、分類、ガバナンスなどに利用します。Azure PolicyはAzureリソースの構成や準拠を扱うため、データ資産のカタログ用途とは異なります。

**対応する公式項目：** Describe the purpose of Microsoft Purview in Azure

### Q7｜VMに必要なネットワークリソース

Azure仮想マシンを仮想ネットワークへ接続する際、VMに少なくとも1つ必要となるネットワークリソースはどれですか。

A. パブリックIPアドレス

B. ネットワークセキュリティグループ（NSG）

C. ロードバランサー

D. ネットワークインターフェイス（NIC）

**正解：** D

**短い解説：** NICはVMと仮想ネットワークを接続するためのリソースで、VMには少なくとも1つ必要です。パブリックIP、NSG、ロードバランサーは構成要件に応じて追加するリソースです。

**対応する公式項目：** Describe the resources required for virtual machines

### Q8｜Application Insights

Webアプリケーションのサーバーリクエスト、外部サービスなどの依存関係、例外を関連付けて調査したいとします。最も直接的なAzure Monitorの機能はどれですか。

A. Log Analytics

B. Application Insights

C. Azure Service Health

D. Azure Policy

**正解：** B

**短い解説：** Application Insightsは、アプリケーションのリクエスト、依存関係、例外、性能などのテレメトリを収集・分析する機能です。Application InsightsはAzure Monitorのアプリケーション監視機能に位置付けられます。

**対応する公式項目：** Describe Azure Monitor, including Log Analytics, Azure Monitor alerts, and Azure Monitor Application Insights

## 公式範囲との対応一覧

| 問題 | 補完した領域 | 対応する公式項目 |
|---:|---|---|
| Q1 | Azure CLI / Azure PowerShell | Describe Azure Cloud Shell, Azure CLI, and Azure PowerShell |
| Q2 | Azure Cloud Shell | Describe Azure Cloud Shell, Azure CLI, and Azure PowerShell |
| Q3 | ARMテンプレート | Describe Azure Resource Manager (ARM) and ARM templates |
| Q4 | IaC | Describe infrastructure as code (IaC) |
| Q5 | Azure Arc | Describe the purpose of Azure Arc |
| Q6 | Microsoft Purview | Describe the purpose of Microsoft Purview in Azure |
| Q7 | VMに必要なリソース | Describe the resources required for virtual machines |
| Q8 | Application Insights | Describe Azure Monitor, including Log Analytics, Azure Monitor alerts, and Azure Monitor Application Insights |

## 参照したMicrosoft公開情報

- [Study guide for Exam AZ-900: Microsoft Azure Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900)（Skills measured as of July 20, 2026）
- [Choose the right Azure command-line tool](https://learn.microsoft.com/en-us/cli/azure/choose-the-right-azure-command-line-tool)
- [What is Azure Cloud Shell?](https://learn.microsoft.com/en-us/azure/cloud-shell/overview)
- [Templates overview - Azure Resource Manager](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)
- [Azure Arc-enabled servers Overview](https://learn.microsoft.com/en-us/azure/azure-arc/servers/overview)
- [Learn about data governance with Microsoft Purview](https://learn.microsoft.com/en-us/azure/purview/overview)
- [Overview of virtual machines in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/overview)
- [Dependency tracking in Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/dependencies)
