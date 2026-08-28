# AZ-900初心者向け用語集

AZ-900対策教材の本文を読むときに参照する用語集です。Azureのサービスや契約条件は変更されることがあるため、実際の構成や試験前の確認では各公式URLも参照してください。

## 配置と障害範囲

### リージョン（Region）

Azureのサービスやリソースを配置する地理的な地域です。リージョンごとに利用できるサービス、ゾーン対応、料金、データ所在地などが異なるため、作成前に確認します。

公式：[Azure リージョン](https://learn.microsoft.com/ja-jp/azure/virtual-machines/regions)

### 可用性ゾーン（Availability Zone）

リージョン内にある、電源・冷却・ネットワークなどが物理的に分離された場所です。対応サービスを複数の可用性ゾーンに配置して初めて、単一ゾーンの障害に対する耐障害性を高められ、1つのゾーンを選ぶだけで高可用性になるわけではありません。

リージョン全体の障害には、複数リージョンやバックアップなど別の対策が必要です。

公式：[Azure Availability Zonesとは](https://learn.microsoft.com/ja-jp/azure/reliability/availability-zones-overview)

## ストレージの冗長性

### LRS（Locally Redundant Storage）

1つのリージョン内にある単一の物理的な場所で、データを複数コピー保持する方式です。データセンターやゾーン全体の障害、リージョン全体の障害への耐性を提供する方式ではありません。

公式：[データの冗長性 - Azure Storage](https://learn.microsoft.com/ja-jp/azure/storage/common/storage-redundancy)

### ZRS（Zone-Redundant Storage）

対応リージョンでは、1つのリージョン内の複数の可用性ゾーンにデータを同期コピーする方式です。リージョン内のゾーンやデータセンターの障害に備えられますが、リージョン全体の障害には備えられません。

公式：[データの冗長性 - Azure Storage](https://learn.microsoft.com/ja-jp/azure/storage/common/storage-redundancy)

### GRS（Geo-Redundant Storage）

プライマリリージョン内で複製したデータを、セカンダリリージョンへ非同期にコピーする方式です。リージョン全体の障害に備えられますが、非同期コピーのため障害時点の最新データがセカンダリにない場合があり、通常はセカンダリリージョンを読み取りに使えず、書き込みを継続するにはフェールオーバーが必要です。

公式：[データの冗長性 - Azure Storage](https://learn.microsoft.com/ja-jp/azure/storage/common/storage-redundancy)

## クラウドサービスの種類

### IaaS（Infrastructure as a Service）

仮想マシン、ディスク、ネットワークなどの基盤を借りる形態です。Microsoftが物理設備を管理し、利用者は主にOS、ミドルウェア、アプリケーション、データを管理します。

公式：[クラウド サービスの種類について説明する](https://learn.microsoft.com/ja-jp/training/modules/describe-cloud-service-types/)

### PaaS（Platform as a Service）

アプリケーションを動かす基盤をサービスとして利用する形態です。基盤側の物理設備やOSなどは原則としてMicrosoftが管理し、利用者はアプリケーション、データ、設定などを管理します。

公式：[クラウドでの共同責任](https://learn.microsoft.com/ja-jp/azure/security/fundamentals/shared-responsibility)

### SaaS（Software as a Service）

完成したアプリケーションをサービスとして利用する形態です。利用者は通常、基盤を管理せず、アカウント、アクセス権、設定、データなどを管理します。

公式：[クラウド サービスの種類について説明する](https://learn.microsoft.com/ja-jp/training/modules/describe-cloud-service-types/)

## IDとアクセス制御

### 認証（Authentication／AuthN）

利用者、デバイス、アプリケーションなどの主体が、主張しているIDであることを確認することです。パスワード、多要素認証、証明書などは認証に使われる手段です。

公式：[認証と承認](https://learn.microsoft.com/ja-jp/entra/identity-platform/authentication-vs-authorization)

### 認可（Authorization／AuthZ）

認証された主体に対して、どのリソースにどの操作まで許可するかを決めることです。認証に成功しても、すべてのリソースや操作が許可されるわけではありません。

公式：[認証と承認](https://learn.microsoft.com/ja-jp/entra/identity-platform/authentication-vs-authorization)

### Azure RBAC（ロールベースのアクセス制御）

Azureリソースへの操作権限を、ロールとしてユーザー、グループ、サービスプリンシパル、マネージドIDなどに割り当てる認可の仕組みです。管理グループ、サブスクリプション、リソースグループ、リソースなどのスコープで適用し、アプリケーション内部の権限管理とは別に考えます。

公式：[Azure ロールベースのアクセス制御（Azure RBAC）とは](https://learn.microsoft.com/ja-jp/azure/role-based-access-control/overview)

### Azure Policy

リソースの状態や操作要求を組織のルールと照合し、準拠状況を評価・制御する仕組みです。効果の種類により監査、拒否、変更、関連リソースの展開など動作が異なり、既存リソースの違反が常に自動修正されるわけではありません。

公式：[Azure Policy の概要](https://learn.microsoft.com/ja-jp/azure/governance/policy/overview)

### リソースロック（Resource lock）

Azureのサブスクリプション、リソースグループ、リソースに対する削除や変更を、管理操作の範囲で防ぐ仕組みです。CanNotDeleteは削除を、ReadOnlyは更新と削除を防ぎますが、データそのものを保護するバックアップではありません。

公式：[インフラストラクチャを保護するためにAzureリソースをロックする](https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/management/lock-resources)

## サービス水準と管理

### SLA（Service Level Agreement／サービス レベル アグリーメント）

Microsoftが特定のサービスについて、定められた条件のもとで可用性などの提供水準を約束する契約です。SLAの数値は利用者のアプリケーション全体の稼働率を保証するものではないため、対象サービス、前提条件、除外事項、サービスクレジットなどを確認します。

公式：[サービス レベル アグリーメント（SLA）を読み取る方法](https://learn.microsoft.com/ja-jp/azure/reliability/concept-service-level-agreements)

### Azure Advisor

Azureの利用状況を分析し、コスト、性能、信頼性、セキュリティなどの改善提案を示すサービスです。提案を表示する機能であり、リソースを自動的に監視・変更する仕組みそのものではありません。

公式：[Azure Advisor の概要](https://learn.microsoft.com/ja-jp/azure/advisor/advisor-overview)

### Azure Service Health

Azureの障害、計画メンテナンス、正常性に関するアドバイザリなど、自分のサブスクリプションやリソースに影響し得るAzure側の情報を確認するサービスです。アプリケーションのリクエスト数や例外などを測る監視機能ではありません。

公式：[Azure Service Health とは](https://learn.microsoft.com/ja-jp/azure/service-health/overview)

### Resource Health

個別のAzureリソースについて、現在および過去の可用性状態を確認するサービスです。Azureサービス全体の障害情報を扱うService Healthとは異なります。

公式：[Azure Resource Health の概要](https://learn.microsoft.com/ja-jp/azure/service-health/resource-health-overview)

### Azure Monitor

Azureやハイブリッド環境のリソース、アプリケーションからメトリック、ログ、トレース、イベントなどを収集・分析し、問題への対応に利用する監視基盤です。Advisorの改善提案やService HealthのAzure側の障害情報とは役割が異なります。

公式：[Azure Monitor の概要](https://learn.microsoft.com/ja-jp/azure/azure-monitor/fundamentals/overview)

## 使い分けの要点

- リージョンは地理的な配置地域、可用性ゾーンはリージョン内の物理的に分離された場所です。
- 可用性ゾーンは、対応サービスを複数ゾーンへ配置して初めて単一ゾーン障害への耐障害性に結び付きます。
- LRS、ZRS、GRSは、主に「どこへ、どのようにコピーするか」の違いです。冗長化はバックアップやアプリケーションのフェールオーバー設計を自動的に代替しません。
- 認証は「誰（何）か」、認可は「何ができるか」、RBACはAzureリソースの認可、Policyは組織ルールへの準拠、ロックは誤削除・誤変更の防止です。
- Advisorは改善提案、Service HealthはAzure側の影響情報、Monitorはリソースやアプリケーションの観測です。
