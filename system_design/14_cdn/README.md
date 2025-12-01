# CDNシステム設計

## 概要

CDN（Content Delivery Network）は、コンテンツをユーザーに近い場所にキャッシュし、高速な配信を実現するシステムです。

## 主要システム

- **[Cloudflare](cloudflare_design.md)** - CDNとセキュリティサービス
- **[Akamai](akamai_design.md)** - エンタープライズCDN
- **[AWS CloudFront](aws_cloudfront_design.md)** - AWSのCDNサービス

## 共通の設計課題

- **エッジキャッシング**: 世界中のエッジサーバーでのキャッシング
- **キャッシュ無効化**: コンテンツ更新時のキャッシュ無効化
- **DDoS対策**: 分散サービス拒否攻撃への対策
- **SSL/TLS終端**: エッジでのSSL/TLS処理
- **動的コンテンツ**: 動的コンテンツの最適化

## 学習の進め方

1. **Cloudflare**から始める: CDNの基本設計
2. **Akamai**でエンタープライズ機能を学ぶ: 大規模エンタープライズ向けCDN

