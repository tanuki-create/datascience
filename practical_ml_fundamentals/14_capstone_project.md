# 14. Capstone: end-to-end MLプロジェクト

## 現場の問い

この章の目的は、個別知識をつなげて、実務で説明できる ML プロジェクトにすることです。モデル精度だけでなく、問題設定、データ、評価、失敗解析、運用計画までを成果物にします。

## 直感

完成物は notebook ではなく、意思決定に使える説明可能な一式です。再現できるコード、評価レポート、モデルカード、監視計画、採用しない判断まで含めます。

## 最小限の数式

capstone では、モデル指標を業務価値に変換します。

```text
value = avoided_loss - false_alarm_cost - operation_cost - maintenance_cost
```

この式は厳密な会計ではなく、意思決定の抜け漏れを減らすための枠です。

## 実装で見るべきログ・指標

- データ版、コード版、実験設定。
- ベースラインと候補モデルの比較。
- validation / test / slice metrics。
- error analysis の分類。
- 推論時間、必要メモリ、運用手順。
- リリース条件と中止条件。

## よくある失敗

- 精度表だけで、業務アクションがない。
- 一番良いモデルだけを報告し、比較過程を残さない。
- 失敗例を見せず、平均指標だけで説得する。
- 本番後の監視と再学習条件がない。
- 利用者が出力をどう扱うかを確認しない。

## 実務メモ

capstone のレビューでは、「なぜこのモデルか」より「なぜこの問題設定・分割・指標・運用でよいのか」を重視します。モデルは変更できますが、問題設定が間違うと全体がずれます。

## 演習

1. 次の成果物を作る。
   - problem brief
   - data card
   - baseline report
   - model comparison table
   - error taxonomy
   - model card
   - monitoring plan
2. 採用しなかったモデルと、その理由を書く。
3. 本番導入前に確認する go / no-go 条件を 10 個作る。

## PDFまたは一次資料との対応

- Theodoridis 全体の概念を、実務プロジェクトに接続する章。
- 関連: [ml_research_practice/research_validation_mindset_ja.md](../ml_research_practice/research_validation_mindset_ja.md)。
