# AZ-900向け安全優先・最小ハンズオン

作成日: 2026-08-27<br>
対象: AZ-900（Azure Fundamentals）学習者<br>
方針: Azureポータル中心、各ラボを専用Resource Group内で完結させ、終了時はResource Group単位で削除する。

## 対象外

Functions、Virtual Machines、Log Analyticsは、この3ラボには含めない。いずれもホスティングプラン、実行時間、ディスク、ログ取り込み・保持など、サブスクリプションや構成に依存する課金条件の確認が必要なためである。

## 共通ルール

- 既存リソースを入れず、ラボごとに専用Resource Groupを新規作成する。
- Resource Group名は `az900-safe-<lab>-<識別子>` とし、作成先リージョンは1つにそろえる。
- ストレージアカウント名とWeb App名はグローバル一意性が必要なため、短い識別子を付ける。
- 作成前に **Review + create** でSKU、冗長性、Pricing tier、追加機能を確認する。
- タグには個人情報・秘密情報を書かない。タグは平文のメタデータである。
- 終了時は、Resource Groupの **Locks** を確認し、ロックがあれば先に削除してからResource Groupを削除する。
- Resource Group削除後、**Resource groups** 一覧と **Cost Management > Cost analysis** で対象が残っていないことを確認する。コスト表示には反映遅延があるため、削除直後の表示だけで請求ゼロと判断しない。
- 共有Resource Group、共有VNet、既存のStorage AccountやApp Service Planは削除しない。

---

## Lab 1: Storage AccountとプライベートBlob

### 目的

Storage Account、Blobコンテナー、Blobの関係を確認し、オブジェクトストレージの基本操作と匿名公開を無効にした構成を体験する。

### 最小手順（Azureポータル）

1. **Resource groups > Create** で `az900-safe-storage-<識別子>` を作成する。
2. **Storage accounts > Create** で、次を選ぶ。
   - Performance: **Standard**
   - Redundancy: **Locally-redundant storage (LRS)**
   - Account kind: **StorageV2 / General-purpose v2**
   - Blob anonymous access: **Disabled**
3. **Data storage > Containers > Create** で `labdata` を作成し、アクセスレベルは **Private** にする。
4. 数KBの機密でないテキストファイルを1つだけアップロードし、ポータルからダウンロードする。
5. **Configuration** で匿名Blobアクセスが無効であることを確認する。公開Webサイト、公開コンテナー、Private Endpoint、Lifecycle Managementは今回作成しない。

### 確認ポイント

- Storage AccountはBlobなどのAzure Storageデータサービスを収容する名前空間である。
- コンテナーはBlobの論理的な入れ物であり、既定のアクセスレベルはPrivateである。
- アカウント側で匿名アクセスを許可しても、コンテナー側を公開設定にしなければ匿名読み取りにはならない。通常はアカウント側も無効にする。
- LRSは学習用の小さなデータに使う構成であり、可用性・災害対策の要件を満たす冗長性とは限らない。

### 具体的な削除対象

- `labdata` コンテナーとアップロードしたBlob
- Storage Account本体
- `az900-safe-storage-<識別子>` Resource Group
- もし誤って作成した場合: Lifecycle Managementルール、Private Endpoint、Private DNS Zone、Storage関連の別Resource Group

Storage Accountの削除はデータ削除を伴う。学習データに復元要件がないことを確認してから削除する。

### 課金注意

容量、トランザクション、データ転送、冗長性、アクセス層によって課金条件が変わる。数KBに限定し、Premium、GRS/ZRS系、Archive、大量ダウンロード、公開URLへの大量アクセスを使わない。Soft deleteやBlob versioningを有効にした場合は、保持データが追加容量として残らないか確認する。

### 公式URL

- [Azure Storage Accountを作成する](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create)
- [AzureポータルでBlobコンテナーを管理する](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal)
- [Blobの匿名読み取りアクセスを設定する](https://learn.microsoft.com/en-us/azure/storage/blobs/anonymous-read-access-configure)
- [Azure Blob Storageの価格](https://azure.microsoft.com/ja-jp/pricing/details/storage/blobs/)
- [Blob Soft Deleteの概要と課金](https://learn.microsoft.com/en-us/azure/storage/blobs/soft-delete-blob-overview)

---

## Lab 2: App Service Free（F1）でPaaSを確認する

### 目的

Web AppとApp Service Planの関係を確認し、VMを管理せずにWebアプリをホストするPaaSの特徴を理解する。Free（F1）を選択できない場合は作成せず、料金確認だけで終了する。

### 最小手順（Azureポータル）

1. **Resource groups > Create** で `az900-safe-appservice-<識別子>` を作成する。
2. **Create a resource > Web App** を開き、次を選ぶ。
   - Publish: **Code**
   - Operating System: **Linux**（選択できる場合）
   - Runtime stack: ポータルで選択可能な現行の学習用ランタイム
   - App Service Plan: 新規作成
   - Pricing plan: **Free F1**
3. Review画面で、有料のBasic/Standard/Premiumになっていないことを確認して作成する。
4. 作成後、Web Appの **Overview** にある既定URLを開き、応答を確認する。
5. **Scale up (App Service plan)** を開き、Freeと有料プランの機能・料金差を確認する。ただし有料プランへの変更は保存しない。
6. Application Insights、カスタムドメイン、証明書、デプロイスロット、バックアップ、VNet統合は追加しない。

### 確認ポイント

- App Service PlanがOS、リージョン、インスタンス数、サイズ、価格レベルを定義する。
- Free/Sharedは共有コンピューティングで、CPUクォータや機能制限があり、本番SLAを前提にしない。
- Free tierを除くApp Service Planは、利用するコンピュートに対して課金される。
- Free F1の表示・利用可否はOS、リージョン、サブスクリプションなどに依存する。

### 具体的な削除対象

- Web App本体
- Web Appと同じResource Groupに作成したApp Service Plan
- もし誤って作成した場合: Application Insights、Alert rule、Action Group、Deployment slot、証明書関連リソース、VNet統合用の追加リソース
- `az900-safe-appservice-<識別子>` Resource Group

Web Appだけ削除して終了せず、App Service Planが一覧に残っていないことを確認する。

### 課金注意

F1は公式料金ページ上の無料プランだが、無料枠・クォータ・利用可能リージョンを作成時点で確認する。Basic以上へ変更すると課金対象になる。Application Insights、バックアップ、証明書、カスタムドメインなどを追加すると別の料金条件が発生し得る。F1が表示されない場合に、代替として有料プランを作成しない。

### 公式URL

- [App Service Planの概要と価格レベル](https://learn.microsoft.com/ja-jp/azure/app-service/overview-hosting-plans)
- [App Serviceの価格（Linux）](https://azure.microsoft.com/ja-jp/pricing/details/app-service/linux/)
- [AzureポータルでNode.js Web Appを作成するQuickstart](https://learn.microsoft.com/en-us/azure/app-service/quickstart-nodejs)
- [Azure無料アカウントの条件](https://azure.microsoft.com/ja-jp/pricing/purchase-options/azure-account)

---

## Lab 3: VNet・タグ・Resource Lock

### 目的

専用Resource Group、タグ、Virtual Network、サブネット、Resource Lockを使い、Azure Resource Managerによる整理・保護の基本を確認する。VMなどの通信テスト用リソースは作成しない。

### 最小手順（Azureポータル）

1. **Resource groups > Create** で `az900-safe-network-<識別子>` を作成する。
2. Resource Groupに次のタグを付ける。
   - `Environment=Training`
   - `Owner=<自分の識別子>`
   - `Expires=<YYYY-MM-DD>`
3. **Virtual networks > Create** で、アドレス空間 `10.10.0.0/16`、サブネット `app-subnet` / `10.10.1.0/24` を作成する。
4. Resource Groupの **Locks > Add** で、ロックレベル **Delete** のロックを追加する。
5. RGの削除操作を開始し、ロックが削除を防ぐことを確認する。削除は完了しない。
6. ロックを削除し、Resource Groupを削除する。

### 確認ポイント

- タグは分類・検索・コスト分析のためのキーと値であり、RBACやPolicyの代替ではない。
- VNetはAzure内の論理ネットワーク、サブネットはVNetのアドレス空間の分割である。
- Deleteロックは変更を許可するが削除を防ぐ。Read-onlyロックは更新も防ぐ。
- ロックは親Resource Groupから子リソースへ継承されるため、削除前に確認・解除が必要である。

### 具体的な削除対象

- Resource GroupのDeleteロック（最初に削除）
- `app-subnet` サブネット
- VNet本体
- `az900-safe-network-<識別子>` Resource Group
- 今回は作成しないが、誤って作成した場合: VNet Peering、NAT Gateway、VPN Gateway、ExpressRoute、Azure Firewall、Bastion、Private Endpoint、Public IP、NSGなど

共有VNetを対象にせず、専用Resource GroupのVNetだけを削除する。

### 課金注意

Virtual Network単体は無料だが、Peering、NAT Gateway、VPN Gateway、ExpressRoute、Azure Firewall、Bastion、VMなどは別の課金条件を持つ。今回の目的ではVNetとサブネットだけに限定し、これらを作成しない。

### 公式URL

- [Virtual Networkを作成するQuickstart](https://learn.microsoft.com/en-us/azure/virtual-network/quickstart-create-virtual-network)
- [Virtual Networkを作成・変更・削除する](https://learn.microsoft.com/en-us/azure/virtual-network/manage-virtual-network)
- [Virtual Networkの価格](https://azure.microsoft.com/ja-jp/pricing/details/virtual-network/)
- [Azureポータルでタグを付ける](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources-portal)
- [Azureリソースをロックして保護する](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources)

---

## 終了チェックリスト

- [ ] Resource Group名を確認した
- [ ] Locksを確認し、あれば削除した
- [ ] サブスクリプション、Resource Group、各リソースに適用されたロックと継承を確認し、ラボ所有のロックを解除した
- [ ] App Service Planを削除する前に、他のWeb Appが共有していないことを確認した
- [ ] Storage Account / App Service Plan / VNetなどの主要リソースが専用RG内にあることを確認した
- [ ] 専用RGを削除した
- [ ] Resource groups一覧から消えたことを確認した
- [ ] サブスクリプションのリソース一覧でも残存リソースがないことを確認した
- [ ] Cost Managementで関連サービス・リソースが残っていないことを確認した
- [ ] 削除直後のCost Management表示だけで請求ゼロと断定していない
- [ ] 作成した有料プラン、監視、ネットワーク追加機能がないことを確認した

## 事実・判断・未確認点

### 事実

- Microsoft公式資料では、StorageV2のStandard構成、App ServiceのFree/Shared tier、VNet、タグ、Resource Lockのポータル操作が案内されている。
- App Service PlanのFree tierにはCPUクォータなどの制限がある。
- VNet単体は無料だが、追加のネットワークサービスには課金条件がある。
- Log Analytics、Functions、VMは本成果物の対象外である。

### 判断

- 課金対象リソースを増やさず、3ラボすべてを専用Resource Groupで追跡できる構成にした。
- StorageはStandard/LRS・数KB、App ServiceはF1、VNetはVNet/サブネットだけに限定した。
- 無料枠を選べない場合に有料プランへ進まないことを安全側の終了条件にした。

### 未確認点

- 利用者のサブスクリプション契約、通貨、無料クレジット残高、RBAC権限、利用可能リージョンは未確認である。
- F1、Storageの設定項目、各リージョンのSKU可否は実際のポータル表示を作成時点で確認する必要がある。
- 既存のテナントポリシーや請求契約によって、作成・削除・Cost Managementの表示が制限される可能性がある。
