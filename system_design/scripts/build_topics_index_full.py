#!/usr/bin/env python3
"""Expand system_design_topics_index_ja.md: 98 topics × 8 sections."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "system_design_topics_index_ja.md"

# Category → template functions return 8 strings: pro, role, diff, why, wout, hist, practice, ask


def sec_pro(title: str, cat: str) -> str:
    return {
        "nfr": f"「{title}」は非機能要件の中でも**数値化・契約化**されやすく、SLO/SLAやコスト試算の出発点になる。他指標と混同されないよう定義を揃える。",
        "arch": f"「{title}」はアーキテクチャ選択の**前提語彙**。メリットだけでなく運用コストまでセットで語れると信頼される。",
        "net": f"「{title}」はエッジ〜オリジン間の**遅延・可用性・セキュリティ**に直結。設定ミスが全トラフィックに効く。",
        "api": f"「{title}」はクライアントとの**契約**の中心。バージョン・互換・エラー設計まで含めて議論される。",
        "authz": f"「{title}」は**信頼境界**をどこに引くかの話。実装はライブラリ任せにせず脅威モデルとセット。",
        "dist": f"「{title}」は分散システムの**トレードオフ**を言語化する語。机上の定義と運用現実の差が論点になりやすい。",
        "data": f"「{title}」は**データの置き方・問い合わせ方**の根幹。スキールとコストの両方に効く。",
        "style": f"「{title}」は**結合度とデプロイ**のトレードオフを表す。チーム構造とも相関する。",
        "res": f"「{title}」は障害を**前提**にした設計。再送・遅延・部分的失敗とセットで効く。",
        "svc": f"「{title}」は動的環境で**誰がどこにいるか**を解決する層。Kubernetes 時代は標準装備に近い。",
        "deploy": f"「{title}」は**リスクを下げてリリース速度を上げる**ための技法。ロールバック戦略と一体。",
        "obs": f"「{title}」は**観測可能性**の部品。インシデント時に「推測」ではなく根拠で動くため。",
        "search": f"「{title}」は**問い合わせパターン特化**のストア／技法。汎用RDBだけでは辛い負荷を分担する。",
        "cache": f"「{title}」は**鮮度と速度**のトレードオフを露骨にする。ホットキーほど設計が効く。",
        "serde": f"「{title}」は**ワイヤ上の表現**とCPU/帯域のバランス。スキーマ進化とセットで論じる。",
        "rt": f"「{title}」は**双方向・低遅延**通信の選択肢。HTTP/1の限界を超える場面で検討される。",
        "pattern": f"「{title}」は**横断関心**を整理するパターン。導入コストとチーム学習コストが伴う。",
        "ds": f"「{title}」はストレージ／アルゴリズムの**実装の芯**。面接では特性と用途の対応が問われる。",
        "big": f"「{title}」は**データ量・処理遅延**が効く領域。バッチとストリームの使い分けが鍵。",
        "sec": f"「{title}」は**コンプライアンスと事故時影響**に直結。鍵のライフサイクルまで含めて設計する。",
        "lowrel": f"「{title}」は**ビットが壊れる**世界の話。大規模ストレージ・ネットワークでは前提。",
        "consensus": f"「{title}」は**複製と障害**の核心。複数ノードで「誰が正」を決める難問。",
    }[cat]


def sec_role(title: str, cat: str) -> str:
    return {
        "nfr": f"プロダクトの**SLA/SLO・リリース優先度・インフラ予算**を説明する指標として使われる。",
        "arch": f"**システム分割・チーム境界・技術スタック**の意思決定材料になる。",
        "net": f"**レイテンシ削減・可用性・オリジン保護**のために実装・設定される。",
        "api": f"**クライアント実装・ゲートウェイ・SDK**の前提として固定される。",
        "authz": f"**ログイン・APIアクセス・内部サービス間**の境界で実装される。",
        "dist": f"**レプリケーション・分断・障害時**の挙動を説明・合意するために使う。",
        "data": f"**クエリ性能・一貫性・運用**（バックアップ、マイグレーション）に効く。",
        "style": f"**デプロイ頻度・障害半径・データ共有**の設計に効く。",
        "res": f"**外部依存・ネットワーク**が不安定な環境でサービスを守る。",
        "svc": f"**動的IP・スケールアウト**環境でサービスを発見・ルーティングする。",
        "deploy": f"**本番リリースとロールバック**の手順とリスク低減に使う。",
        "obs": f"**インシデント対応・容量計画・回帰分析**のデータ源になる。",
        "search": f"**検索・推薦・監視データ**など負荷の高い読み取りを支える。",
        "cache": f"**DB・オリジン負荷**を下げ、ユーザー体験を安定させる。",
        "serde": f"**サービス境界・ストレージ**でデータを交換・保存する。",
        "rt": f"**チャット・協調編集・ライブ**など双方向UXを支える。",
        "pattern": f"**複雑ドメイン・大規模移行**で整理・段階導入に使う。",
        "ds": f"**DB・分散ストレージ・インメモリ**の実装と性能特性の根拠になる。",
        "big": f"**分析・ML・レポート**のためのデータ収集・変換を支える。",
        "sec": f"**秘密・権限・暗号**を統制し、漏洩影響を限定する。",
        "lowrel": f"**ディスク・ネットワーク**の信頼性を数理的に補う。",
        "consensus": f"**レプリケーション・メタデータ**の単一の真実を決める。",
    }[cat]


def sec_diff(title: str, cat: str) -> str:
    hints = {
        "nfr": "隣接指標（例: レイテンシとスループット、可用性と信頼性）との**定義の違い**を整理する。",
        "arch": "代替アーキテクチャ（例: モノリス vs マイクロ）との**境界と移行コスト**で比較する。",
        "net": "同層の別機構（例: CDN vs キャッシュ vs LB）と**責務の切り分け**で比較する。",
        "api": "REST / GraphQL / gRPC など**契約とクライアント**の違いで比較する。",
        "authz": "認証と認可、レート制限とスロットリングなど**近い言葉**と役割分担を明確にする。",
        "dist": "CAP・整合性レベル・レプリケーション方式など**トレードオフの軸**で比較する。",
        "data": "正規化・インデックス・デノーマルなど**読み書きの最適点**で対比する。",
        "style": "同期/非同期、キューとPub/Subなど**結合と信頼性**で比較する。",
        "res": "リトライ・タイムアウト・サーキットなど**失敗時の挙動**の組み合わせで比較する。",
        "svc": "DNS・サービスレジストリ・LB**の解決レイヤ**の違いで比較する。",
        "deploy": "ブルーグリーン・カナリ・フィーチャーフラグの**リスクと速度**で比較する。",
        "obs": "ログ・メトリクス・トレースの**用途とコスト**で使い分けを説明する。",
        "search": "RDB・全文・ベクトルなど**クエリ種別**に適したストアで比較する。",
        "cache": "無効化・ウォーミング・スタンピード対策など**鮮度戦略**で比較する。",
        "serde": "JSON・Protobuf・Avroなど**スキーマと互換**で比較する。",
        "rt": "WebSocket・WebRTC・通常HTTPの**接続モデル**で比較する。",
        "pattern": "CQRS・イベントソーシング・BFFなど**複雑さと得られる分離**で比較する。",
        "ds": "LSM・B木・確率構造など**読み書きパターン**で比較する。",
        "big": "バッチ・ストリーム・レイク・WHの**レイテンシと用途**で比較する。",
        "sec": "RBAC・ABAC・SSOなど**モデルと運用**で比較する。",
        "lowrel": "チェックサム・レプリケーション・ECの**検出と修復**の役割で比較する。",
        "consensus": "Raft・Paxos・リーダー選挙の**提供する保証**で比較する。",
    }
    return hints[cat]


def sec_why(title: str, cat: str) -> str:
    return f"**{title}**を議論・実装に落とさないと、要件と実装のギャップが埋まらず、**運用・インシデント・コスト**で後から効くから。"


def sec_wout(title: str, cat: str) -> str:
    return {
        "nfr": f"指標が曖昧なままだと**過剰投資 or 障害頻発**、SLO違反の責任分界が争点になる。",
        "arch": f"前提が共有されず**変更コストが爆増**、チーム間の結合が強すぎる。",
        "net": f"単一障害点・遅延・攻撃面が残り**ユーザー体験とセキュリティ**が一括で損なわれる。",
        "api": f"クライアントとサーバで**解釈違い**、バージョン地獄、サポート不能になる。",
        "authz": f"不正アクセス・権限昇格・**監査不能**につながる。",
        "dist": f"分断時・レプリカ遅延時に**「バグ」か「仕様」か**が判別できず、データ不整合が残る。",
        "data": f"遅いクエリ・不整合・**マイグレーション困難**が常態化する。",
        "style": f"デプロイ・デバッグ・**データの一貫性**が難しくなり、スケールと逆行する。",
        "res": f"小さな障害が**カスケード**し、復旧が長引く。",
        "svc": f"設定がハードコードされ**スケール・フェイルオーバ**が壊れる。",
        "deploy": f"リリースが怖くなり**変更頻度が落ち**、逆にバッチ変更で大事故が起きる。",
        "obs": f"原因不明の障害が続き**MTTR**が伸び、同じ障害を繰り返す。",
        "search": f"検索が遅い・不正確・**インフラコスト**が読めない。",
        "cache": f"DBやオリジンに**雪崩**、古いデータ表示、またはキャッシュ無意味。",
        "serde": f"互換破壊・**パフォーマンス劣化**・デバッグ困難になる。",
        "rt": f"ポーリング地獄・**レイテンシ**・接続枯渇が起きる。",
        "pattern": f"複雑さだけ増え**理解コスト**が勝つ、移行が止まる。",
        "ds": f"想定外の**読み書き性能**、ストレージ膨張、復旧困難。",
        "big": f"データが負債化し**分析・コンプライアンス**が回らない。",
        "sec": f"漏洩・**内部犯行**・鍵ローテ失敗で致命傷。",
        "lowrel": f"サイレント破損・**データ喪失**に気づくのが遅れる。",
        "consensus": f"スプリットブレイン・**二重書き込み**・データ破損のリスク。",
    }[cat]


def sec_hist(title: str, cat: str) -> str:
    return {
        "nfr": f"インターネット規模サービスとクラウドの普及で**数値SLO**が標準化。可用性〇〇%はベンダー契約でも定番化した。",
        "arch": f"SOA・クラウド・コンテナの波で**分割と統合**の語彙が更新され続けている。",
        "net": f"Web爆発期から **CDN/LB/DNS** がインフラの三種の神器として定着した。",
        "api": f"RESTの普及後、**モバイル・マイクロサービス**で GraphQL/gRPC が並ぶ選択肢に。",
        "authz": f"WebのOAuth/OIDC・ゼロトラストで**トークンとmTLS**が実務の主軸に。",
        "dist": f"**Brewer の CAP** 以降、NoSQL と分散DB で実務言語になった。",
        "data": f"関係モデルから**水平分割・専用ストア**へ用途別に最適化が進んだ。",
        "style": f"**DDD・マイクロサービス**でイベントとメッセージが設計の中心語になった。",
        "res": f"分散システムの失敗モード研究と **Netflix 等の実装**でパターンが教科書化した。",
        "svc": f"静的設定から **etcd/Consul/K8s** へ、サービス発見が自動化された。",
        "deploy": f"継続デリバリーと**カナリ・フィーチャーフラグ**がリリース工学の標準に。",
        "obs": f"**Dapper 以降の分散トレース**と Prometheus 系で三本柱が揃った。",
        "search": f"Web検索・Elasticsearch・**近年はベクトル**とRAGで再ブーム。",
        "cache": f"メモリ安価化と **Redis** によりアプリ層キャッシュが一般化。",
        "serde": f"JSON全盛の後、**スキーマ駆動（Protobuf/Avro）**が内部通信で主流に。",
        "rt": f"ブラウザAPIとして **WebSocket/WebRTC** が定着し、会議・協調系が標準化。",
        "pattern": f"**DDD・CQRS・イベントソーシング**がエンタープライズからクラウドネイティブへ。",
        "ds": f"ディスクとRAMのギャップから **LSM・B+木** がストレージエンジンの定番に。",
        "big": f"**Hadoop 以降のデータ基盤**から、クラウドマネージドとストリームへ。",
        "sec": f"漏洩事故と規制で **KMS・Vault・SSO** が必須インフラに。",
        "lowrel": f"オブジェクトストレージの大規模化で **EC** が標準技術に。",
        "consensus": f"**Raft の教育容易性**で実装が増え、分散システムの土台に。",
    }[cat]


def sec_practice(title: str, cat: str) -> str:
    return f"**SLO/メトリクス**で測り、**Runbook**に落とし、**レビュー**でトレードオフを文書化する。{title}単体ではなく**依存（DB・ネットワーク・他チーム）**とセットで設計する。"


def sec_ask(title: str, cat: str) -> str:
    return (
        f"このプロダクトで {title} の**数値目標**は何か（または定義できない理由は）。"
        f" 障害時・スケール時に**最初に見るメトリクス**は。"
        f" 代替案と比べて**捨てたもの**は何か。"
    )


CAT_FOR_NUM: dict[int, str] = {
    **{i: "nfr" for i in range(1, 7)},
    **{7: "arch", 8: "arch", 9: "data"},
    **{i: "net" for i in range(10, 15)},
    **{i: "api" for i in range(15, 19)},
    **{19: "authz", 20: "authz", 21: "authz"},
    **{i: "dist" for i in range(22, 29)},
    **{i: "data" for i in range(29, 33)},
    **{i: "style" for i in range(33, 39)},
    **{i: "res" for i in range(39, 45)},
    45: "svc",
    46: "svc",
    47: "res",
    48: "svc",
    **{i: "deploy" for i in range(49, 52)},
    **{i: "obs" for i in range(52, 59)},
    **{i: "search" for i in range(59, 65)},
    **{i: "cache" for i in range(65, 68)},
    **{i: "serde" for i in range(68, 71)},
    **{i: "rt" for i in range(71, 73)},
    **{i: "pattern" for i in range(73, 79)},
    **{i: "ds" for i in range(79, 84)},
    **{i: "big" for i in range(84, 91)},
    **{i: "sec" for i in range(91, 95)},
    **{i: "lowrel" for i in range(95, 97)},
    **{i: "consensus" for i in range(97, 99)},
}


def parse_topics(md: str) -> list[tuple[int, str, str]]:
    """Return list of (num, title, one_line_summary_for_一言).

    生成済みドキュメントでは *（一言）* 行のみを採用する。
    旧形式（### の直後に短い段落1つ）はその段落を採用する。
    """
    heading = re.compile(r"^### (\d+)\.\s+(.+)$", re.MULTILINE)
    matches = list(heading.finditer(md))
    out: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        num = int(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        block = md[start:end]
        one = re.search(r"^\s*\*（一言）\*\s*(.+)$", block, re.MULTILINE)
        if one:
            summary = one.group(1).strip()
        else:
            block_stripped = block.strip()
            if not block_stripped:
                summary = ""
            else:
                parts = re.split(r"\n\s*\n", block_stripped, maxsplit=1)
                summary = parts[0].strip().replace("\n", " ")
        out.append((num, title, summary))
    return sorted(out, key=lambda x: x[0])


def render_topic(num: int, title: str, summary: str) -> str:
    cat = CAT_FOR_NUM[num]
    lines = [
        f"### {num}. {title}",
        "",
        "- **現場のプロの解説**",
        f"  {sec_pro(title, cat)}",
        "",
        "- **実際のプロダクトでの役割**",
        f"  {sec_role(title, cat)}",
        "",
        "- **似た概念の違い**",
        f"  {sec_diff(title, cat)}",
        "",
        "- **なぜ本当に必要か**",
        f"  {sec_why(title, cat)}",
        "",
        "- **ないと何が困るか**",
        f"  {sec_wout(title, cat)}",
        "",
        "- **歴史・背景と広まり方**",
        f"  {sec_hist(title, cat)}",
        "",
        "- **プロの扱い方**",
        f"  {sec_practice(title, cat)}",
        "",
        "- **プロになるための質問**",
        f"  {sec_ask(title, cat)}",
        "",
        f"  *（一言）* {summary}",
        "",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    topics = parse_topics(text)
    if len(topics) != 98:
        raise SystemExit(f"Expected 98 topics, got {len(topics)}: {[t[0] for t in topics]}")

    idx = text.index("## 非機能要件と指標")
    tail_idx = text.index("## 既存パターン集へのショートカット")
    header = text[:idx]
    dup = (
        "深い横断対照は [現場プロ向け概念解説](pro_field_concepts_guide_ja.md) を参照してください。"
        "深い横断対照は [現場プロ向け概念解説](pro_field_concepts_guide_ja.md) を参照してください。"
    )
    if dup in header:
        header = header.replace(
            dup,
            "深い横断対照は [現場プロ向け概念解説](pro_field_concepts_guide_ja.md) を参照してください。",
        )
    intro_new = (
        "面接・設計レビュー用の一覧です。**各項目は次の8点**で統一しています："
        "\n\n1. **現場のプロの解説** 2. **実際のプロダクトでの役割** 3. **似た概念の違い** 4. **なぜ本当に必要か** 5. **ないと何が困るか**"
        "\n6. **歴史・背景と広まり方** 7. **プロの扱い方** 8. **プロになるための質問**（各項目末尾の *一言* に従来の短い定義を併記）。"
        "\n\n深い横断対照は [現場プロ向け概念解説](pro_field_concepts_guide_ja.md) を参照してください。"
    )
    intro_old = (
        "面接・設計レビュー・用語の引き直し用の一覧です。各項目は **一言定義** と、ある場合は **関連リソース**（同一リポジトリ内）へのリンクのみです。"
        "深い横断対照は [現場プロ向け概念解説](pro_field_concepts_guide_ja.md) を参照してください。"
    )
    if intro_old in header:
        header = header.replace(intro_old, intro_new)
    tail = text[tail_idx:]

    h2_order = [
        "## 非機能要件と指標",
        "## アーキテクチャ基礎",
        "## ネットワーク・エッジ",
        "## API",
        "## 認証・制御",
        "## 分散・可用性",
        "## データモデル・DB",
        "## スタイル・メッセージング",
        "## レジリエンス",
        "## サービス運用・ゲートウェイ",
        "## デプロイ・リリース",
        "## オブザーバビリティ",
        "## 検索・データストア応用",
        "## キャッシュ応用",
        "## 転送・表現",
        "## リアルタイム通信",
        "## パターン（CQRS 等）",
        "## データ構造・確率的",
        "## 大規模処理・データ基盤",
        "## セキュリティ・統制",
        "## 信頼性（低レベル）",
        "## 分散合意",
    ]
    ranges = [
        (1, 6),
        (7, 9),
        (10, 14),
        (15, 18),
        (19, 21),
        (22, 28),
        (29, 32),
        (33, 38),
        (39, 45),
        (46, 48),
        (49, 51),
        (52, 58),
        (59, 64),
        (65, 67),
        (68, 70),
        (71, 72),
        (73, 78),
        (79, 83),
        (84, 90),
        (91, 94),
        (95, 96),
        (97, 98),
    ]
    topic_dict = {n: (t, s) for n, t, s in topics}
    out_chunks: list[str] = []
    for h2, (lo, hi) in zip(h2_order, ranges):
        out_chunks.append(h2 + "\n\n")
        for n in range(lo, hi + 1):
            t, s = topic_dict[n]
            out_chunks.append(render_topic(n, t, s))
        out_chunks.append("---\n\n")
    body = "".join(out_chunks).rstrip() + "\n"

    new_text = header + body + "\n" + tail
    SRC.write_text(new_text, encoding="utf-8")
    print(f"Wrote {SRC} ({len(topic_dict)} topics)")


if __name__ == "__main__":
    main()
