# 金融・決済システム設計

## 概要

金融・決済プラットフォームは、安全な決済処理と金融サービスを提供するシステムです。

## 主要システム

- **[PayPal](paypal_design.md)** - オンライン決済サービス
- **[Stripe](stripe_design.md)** - 決済APIプラットフォーム
- **[Venmo](venmo_design.md)** - P2P決済サービス
- **[Square](square_design.md)** - 決済処理プラットフォーム
- **[Apple Pay](apple_pay_design.md)** - Appleモバイル決済システム
- **[Google Pay](google_pay_design.md)** - Googleモバイル決済システム

## 共通の設計課題

- **決済処理**: 安全な決済トランザクション処理
- **不正検出**: 詐欺や不正取引の検出
- **コンプライアンス**: 金融規制への準拠
- **高可用性**: 99.99%以上の可用性
- **監査ログ**: 全ての取引の記録と追跡

## 学習の進め方

1. **PayPal**から始める: 決済システムの基本設計
2. **Stripe**でAPIプラットフォームを学ぶ: 開発者向け決済API

