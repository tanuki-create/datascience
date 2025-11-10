# よく使われるCSS要素のリストとUX実現

## 目次

1. [レイアウト関連](#1-レイアウト関連)
2. [タイポグラフィ](#2-タイポグラフィ)
3. [カラー・背景](#3-カラー背景)
4. [スペーシング](#4-スペーシング)
5. [ボーダー・シャドウ](#5-ボーダーシャドウ)
6. [アニメーション・トランジション](#6-アニメーショントランジション)
7. [レスポンシブデザイン](#7-レスポンシブデザイン)
8. [インタラクティブ要素](#8-インタラクティブ要素)
9. [視覚的階層](#9-視覚的階層)
10. [アクセシビリティ](#10-アクセシビリティ)

---

## 1. レイアウト関連

### `display: flex`
**意味**: Flexboxレイアウトを有効化。要素を柔軟に配置できる。

**UX目的**:
- **均等配置**: カードやボタンを等間隔で配置し、視覚的なバランスを保つ
- **中央揃え**: コンテンツを画面中央に配置し、ユーザーの注意を集める
- **レスポンシブ対応**: 画面サイズに応じて自動的に要素を再配置
- **ナビゲーションバー**: メニュー項目を横並びに配置

**使用例**:
```css
.navbar {
    display: flex;
    justify-content: space-between;  /* 左右に配置 */
    align-items: center;              /* 垂直方向の中央揃え */
}
```

---

### `display: grid`
**意味**: CSS Gridレイアウトを有効化。2次元のグリッドシステム。

**UX目的**:
- **複雑なレイアウト**: ヘッダー、サイドバー、メインコンテンツ、フッターを明確に分離
- **カードレイアウト**: 商品一覧や記事一覧を整然と配置
- **画像ギャラリー**: 画像を規則的に配置し、視覚的な秩序を保つ
- **ダッシュボード**: 複数のウィジェットを効率的に配置

**使用例**:
```css
.dashboard {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "sidebar header"
        "sidebar main"
        "sidebar footer";
}
```

---

### `position: relative` / `position: absolute`
**意味**: 要素の位置を相対的/絶対的に指定。

**UX目的**:
- **オーバーレイ**: モーダルやドロップダウンメニューを表示
- **バッジ表示**: 通知数や新着マークを要素の右上に配置
- **ツールチップ**: ホバー時に説明文を表示
- **固定ヘッダー**: スクロールしても常に表示されるナビゲーション

**使用例**:
```css
.badge {
    position: relative;
}

.badge::after {
    content: "3";
    position: absolute;
    top: -8px;
    right: -8px;
    background: red;
    border-radius: 50%;
}
```

---

### `position: fixed` / `position: sticky`
**意味**: 要素を画面の特定位置に固定。

**UX目的**:
- **固定ヘッダー**: スクロールしても常にナビゲーションを表示し、操作性を向上
- **固定フッター**: 重要なアクションボタンを常に表示
- **戻るボタン**: 長いページで上部に戻るボタンを固定表示
- **スティッキー要素**: サイドバーの目次をスクロール位置に応じて固定

**使用例**:
```css
.header {
    position: sticky;
    top: 0;
    background: white;
    z-index: 100;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

---

### `z-index`
**意味**: 要素の重なり順を制御。

**UX目的**:
- **モーダル表示**: ダイアログを他の要素の上に表示
- **ドロップダウンメニュー**: メニューを他の要素の上に表示
- **ツールチップ**: 説明文をコンテンツの上に表示
- **通知バナー**: 重要な通知を最前面に表示

**使用例**:
```css
.modal {
    z-index: 1000;
}

.modal-backdrop {
    z-index: 999;
}
```

---

## 2. タイポグラフィ

### `font-size`
**意味**: フォントサイズを指定。

**UX目的**:
- **視覚的階層**: 見出し、本文、補足情報をサイズで区別
- **可読性向上**: 適切なサイズで読みやすさを確保
- **強調**: 重要な情報を大きく表示して注意を引く
- **レスポンシブ**: 画面サイズに応じて調整

**使用例**:
```css
h1 { font-size: 2.5rem; }  /* メインタイトル */
h2 { font-size: 2rem; }   /* セクションタイトル */
p { font-size: 1rem; }     /* 本文 */
small { font-size: 0.875rem; } /* 補足情報 */
```

---

### `font-weight`
**意味**: フォントの太さを指定。

**UX目的**:
- **強調**: 重要な単語やフレーズを太字で強調
- **階層構造**: 見出しと本文を視覚的に区別
- **アクセント**: 特定の要素に視覚的なアクセントを付与
- **可読性**: 適切な太さで読みやすさを向上

**使用例**:
```css
.heading { font-weight: 700; }  /* 太字の見出し */
.body { font-weight: 400; }     /* 通常の本文 */
.emphasis { font-weight: 600; }  /* 中程度の強調 */
```

---

### `line-height`
**意味**: 行の高さ（行間）を指定。

**UX目的**:
- **可読性向上**: 適切な行間で読みやすさを向上
- **視覚的余白**: テキストブロックに適切な余白を作成
- **長文の読みやすさ**: 記事やブログ記事で重要
- **アクセシビリティ**: 視覚障害者にも読みやすい

**使用例**:
```css
.article {
    line-height: 1.6;  /* 1.5-1.8が読みやすい */
}

.heading {
    line-height: 1.2;  /* 見出しは少し詰める */
}
```

---

### `text-align`
**意味**: テキストの配置を指定。

**UX目的**:
- **中央揃え**: タイトルや重要なメッセージを中央に配置
- **左揃え**: 本文を左揃えで読みやすく（日本語・英語）
- **右揃え**: 数値や日付を右揃えで整列
- **両端揃え**: 正式な文書で使用

**使用例**:
```css
.title { text-align: center; }
.article { text-align: left; }
.price { text-align: right; }
```

---

### `text-decoration`
**意味**: テキストの装飾（下線、取り消し線など）を指定。

**UX目的**:
- **リンク表示**: リンクを下線で識別可能にする
- **取り消し**: 削除された価格や無効な情報を示す
- **装飾**: 視覚的なアクセントを付与
- **ホバー効果**: インタラクティブ要素のフィードバック

**使用例**:
```css
a {
    text-decoration: underline;
}

a:hover {
    text-decoration: none;
}

.old-price {
    text-decoration: line-through;
}
```

---

### `text-overflow: ellipsis`
**意味**: テキストがはみ出す場合に「...」を表示。

**UX目的**:
- **レイアウト維持**: 長いテキストでレイアウトが崩れるのを防ぐ
- **一貫性**: カードレイアウトで高さを統一
- **情報のヒント**: テキストが省略されていることを示す
- **モバイル対応**: 限られたスペースで情報を表示

**使用例**:
```css
.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
```

---

## 3. カラー・背景

### `color`
**意味**: テキストの色を指定。

**UX目的**:
- **視認性**: 背景とのコントラストで読みやすさを確保
- **ブランド統一**: ブランドカラーで統一感を出す
- **状態表示**: エラー（赤）、成功（緑）、警告（黄）を色で表現
- **階層構造**: 重要度を色の濃淡で表現

**使用例**:
```css
.error { color: #dc3545; }    /* エラーメッセージ */
.success { color: #28a745; }  /* 成功メッセージ */
.muted { color: #6c757d; }     /* 補足情報 */
```

---

### `background-color`
**意味**: 背景色を指定。

**UX目的**:
- **視覚的区分**: セクションを色で区別
- **強調**: 重要な情報の背景を色付け
- **ブランド表現**: ブランドカラーで統一感を出す
- **アクセシビリティ**: 十分なコントラストを確保

**使用例**:
```css
.hero {
    background-color: #007bff;  /* ヒーローセクション */
}

.card {
    background-color: #ffffff;  /* カードの背景 */
}

.highlight {
    background-color: #fff3cd;  /* ハイライト表示 */
}
```

---

### `background-image`
**意味**: 背景画像を指定。

**UX目的**:
- **視覚的インパクト**: ヒーローセクションで印象的な背景
- **ブランド表現**: ロゴやブランドイメージを背景に配置
- **装飾**: パターンやテクスチャで視覚的な興味を引く
- **オーバーレイ**: テキストの可読性を保ちながら背景を表示

**使用例**:
```css
.hero {
    background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
                      url('hero-image.jpg');
    background-size: cover;
    background-position: center;
}
```

---

### `opacity`
**意味**: 要素の透明度を指定。

**UX目的**:
- **視覚的階層**: 重要でない要素を薄く表示
- **ホバー効果**: マウスオーバー時に不透明度を変更
- **オーバーレイ**: モーダルの背景を半透明にする
- **フェード効果**: アニメーションで使用

**使用例**:
```css
.button {
    opacity: 0.7;
}

.button:hover {
    opacity: 1;
}

.modal-backdrop {
    background: black;
    opacity: 0.5;
}
```

---

## 4. スペーシング

### `margin`
**意味**: 要素の外側の余白を指定。

**UX目的**:
- **要素間の分離**: カードやセクション間に適切な余白を作成
- **視覚的呼吸**: コンテンツに適切な余白で読みやすさを向上
- **グループ化**: 関連する要素を近くに、無関係な要素を離す
- **レスポンシブ**: 画面サイズに応じて調整

**使用例**:
```css
.card {
    margin-bottom: 20px;  /* カード間の余白 */
}

.section {
    margin: 40px 0;  /* セクション間の余白 */
}
```

---

### `padding`
**意味**: 要素の内側の余白を指定。

**UX目的**:
- **クリック領域**: ボタンやリンクのクリックしやすさを向上
- **コンテンツの余白**: テキストと境界線の間に適切な余白
- **視覚的余裕**: カードやコンテナ内に適切な余白
- **タッチターゲット**: モバイルでタップしやすいサイズを確保

**使用例**:
```css
.button {
    padding: 12px 24px;  /* 上下12px、左右24px */
}

.card {
    padding: 20px;  /* 全方向に20px */
}
```

---

### `gap` (Flexbox/Grid)
**意味**: Flexbox/Gridコンテナ内の要素間の余白。

**UX目的**:
- **一貫性**: グリッドやフレックスアイテム間の余白を統一
- **簡潔なコード**: marginを使わずに要素間の余白を設定
- **レスポンシブ**: 画面サイズに応じて調整が容易

**使用例**:
```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;  /* グリッドアイテム間の余白 */
}

.flex-container {
    display: flex;
    gap: 16px;  /* フレックスアイテム間の余白 */
}
```

---

## 5. ボーダー・シャドウ

### `border`
**意味**: 要素の境界線を指定。

**UX目的**:
- **視覚的区分**: カードやボタンの境界を明確に
- **フォーカス表示**: 入力フィールドのフォーカス状態を示す
- **装飾**: 視覚的なアクセントを付与
- **グループ化**: 関連する要素を視覚的にグループ化

**使用例**:
```css
.card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

.input:focus {
    border: 2px solid #007bff;
}
```

---

### `border-radius`
**意味**: 要素の角を丸くする。

**UX目的**:
- **モダンなデザイン**: 角丸で洗練された印象
- **親しみやすさ**: 丸みで親しみやすい印象
- **視覚的統一**: デザインシステムで統一感を出す
- **カードデザイン**: カードやボタンでよく使用

**使用例**:
```css
.button {
    border-radius: 8px;  /* 少し丸み */
}

.card {
    border-radius: 12px;  /* より丸み */
}

.avatar {
    border-radius: 50%;  /* 完全な円 */
}
```

---

### `box-shadow`
**意味**: 要素に影を付ける。

**UX目的**:
- **深度感**: 要素を浮き上がらせ、階層を表現
- **カードデザイン**: カードを背景から浮かせて表示
- **ホバー効果**: インタラクティブ要素のフィードバック
- **視覚的階層**: 重要な要素を強調

**使用例**:
```css
.card {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* 軽い影 */
}

.card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);  /* ホバー時により強い影 */
}

.modal {
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);  /* 強い影 */
}
```

---

### `outline`
**意味**: 要素の外側の輪郭線を指定（通常はフォーカス表示用）。

**UX目的**:
- **アクセシビリティ**: キーボード操作時のフォーカス表示
- **視認性**: フォーカスされた要素を明確に示す
- **WCAG準拠**: アクセシビリティガイドラインに準拠

**使用例**:
```css
.button:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

.button:focus:not(:focus-visible) {
    outline: none;  /* マウスクリック時は非表示 */
}
```

---

## 6. アニメーション・トランジション

### `transition`
**意味**: プロパティの変化をスムーズにアニメーション。

**UX目的**:
- **スムーズな変化**: ホバーやクリック時の状態変化を滑らかに
- **視覚的フィードバック**: ユーザーの操作に対する反応を示す
- **プロフェッショナルな印象**: 滑らかなアニメーションで品質感を向上
- **注意の誘導**: 変化する要素に注意を引く

**使用例**:
```css
.button {
    background-color: #007bff;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
}
```

---

### `transform`
**意味**: 要素を変形（移動、回転、拡大縮小など）。

**UX目的**:
- **ホバー効果**: ボタンやカードを浮き上がらせる
- **アニメーション**: スムーズな移動や回転アニメーション
- **パフォーマンス**: GPU加速で滑らかなアニメーション
- **視覚的フィードバック**: インタラクションの反応を示す

**使用例**:
```css
.card:hover {
    transform: translateY(-5px) scale(1.02);  /* 上に移動 + 拡大 */
}

.loading {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

---

### `animation`
**意味**: キーフレームアニメーションを定義。

**UX目的**:
- **ローディング表示**: 読み込み中の視覚的フィードバック
- **注意の誘導**: 重要な要素をアニメーションで強調
- **状態変化**: 成功やエラーの表示をアニメーション
- **エンゲージメント**: 動きでユーザーの興味を引く

**使用例**:
```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
```

---

## 7. レスポンシブデザイン

### `@media` クエリ
**意味**: 画面サイズやデバイス特性に応じてスタイルを変更。

**UX目的**:
- **マルチデバイス対応**: スマホ、タブレット、PCで最適な表示
- **読みやすさ**: 画面サイズに応じてフォントサイズを調整
- **操作性**: タッチデバイスで適切なボタンサイズを確保
- **レイアウト最適化**: 画面サイズに応じてレイアウトを変更

**使用例**:
```css
.container {
    padding: 10px;
}

@media (min-width: 768px) {
    .container {
        padding: 20px;
        max-width: 750px;
    }
}

@media (min-width: 1024px) {
    .container {
        padding: 30px;
        max-width: 1200px;
    }
}
```

---

### `width: 100%` / `max-width`
**意味**: 要素の幅を指定。

**UX目的**:
- **レスポンシブ**: 親要素に合わせて幅を調整
- **最大幅制限**: 大画面で読みやすさを保つ
- **フル幅要素**: ヒーローセクションなどで画面幅いっぱいに表示

**使用例**:
```css
.container {
    width: 100%;
    max-width: 1200px;  /* 最大幅を制限 */
    margin: 0 auto;     /* 中央揃え */
}

.hero {
    width: 100%;  /* 画面幅いっぱい */
}
```

---

### `min-height: 100vh`
**意味**: 要素の最小高さをビューポートの高さに設定。

**UX目的**:
- **フルスクリーン表示**: ヒーローセクションを画面いっぱいに表示
- **フッター固定**: コンテンツが少ない場合でもフッターを下部に配置
- **視覚的インパクト**: 大きなセクションで印象を強く

**使用例**:
```css
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

---

## 8. インタラクティブ要素

### `:hover`
**意味**: マウスオーバー時のスタイル。

**UX目的**:
- **インタラクティブ性**: クリック可能な要素を示す
- **視覚的フィードバック**: ユーザーの操作に対する反応
- **情報の提示**: ホバー時に追加情報を表示
- **エンゲージメント**: 動的な要素で興味を引く

**使用例**:
```css
.button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.card:hover {
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}
```

---

### `:focus`
**意味**: フォーカス時のスタイル（キーボード操作時）。

**UX目的**:
- **アクセシビリティ**: キーボード操作時の視認性を確保
- **操作の明確化**: 現在フォーカスされている要素を示す
- **WCAG準拠**: アクセシビリティガイドラインに準拠

**使用例**:
```css
.input:focus {
    outline: 2px solid #007bff;
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
}
```

---

### `:active`
**意味**: クリック/タップ中のスタイル。

**UX目的**:
- **操作の確認**: クリック/タップが認識されたことを示す
- **視覚的フィードバック**: 即座に反応があることを示す
- **操作感の向上**: ボタンを押した感覚を視覚的に表現

**使用例**:
```css
.button:active {
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

---

### `cursor: pointer`
**意味**: マウスカーソルをポインター（手の形）に変更。

**UX目的**:
- **クリック可能の明示**: クリック可能な要素であることを示す
- **直感的な操作**: ユーザーが操作可能な要素を識別しやすく
- **一貫性**: インタラクティブ要素で統一

**使用例**:
```css
.button,
a,
.clickable {
    cursor: pointer;
}
```

---

### `pointer-events: none`
**意味**: マウスイベントを無効化。

**UX目的**:
- **オーバーレイ**: モーダルの背景をクリック不可にする
- **装飾要素**: 装飾的な要素がクリックを妨げないように
- **ローディング状態**: 読み込み中に操作を無効化

**使用例**:
```css
.modal-backdrop {
    pointer-events: none;
}

.modal {
    pointer-events: auto;
}

.loading-overlay {
    pointer-events: none;
}
```

---

## 9. 視覚的階層

### `font-size` の階層
**意味**: フォントサイズで重要度を表現。

**UX目的**:
- **情報の優先順位**: 重要な情報を大きく、補足情報を小さく
- **スキャンしやすさ**: ユーザーが情報を素早く把握
- **視覚的秩序**: 統一されたサイズ体系で整理

**使用例**:
```css
h1 { font-size: 2.5rem; }  /* 最重要 */
h2 { font-size: 2rem; }    /* 重要 */
h3 { font-size: 1.5rem; }  /* 中程度 */
p { font-size: 1rem; }     /* 本文 */
small { font-size: 0.875rem; } /* 補足 */
```

---

### `color` の階層
**意味**: 色の濃淡で重要度を表現。

**UX目的**:
- **情報の優先順位**: 濃い色で重要、薄い色で補足
- **視認性**: 重要な情報を目立たせる
- **統一感**: 色の階層でデザインを統一

**使用例**:
```css
.primary-text { color: #212529; }  /* 最重要テキスト */
.secondary-text { color: #6c757d; } /* 補足テキスト */
.muted-text { color: #adb5bd; }     /* 控えめなテキスト */
```

---

### `font-weight` の階層
**意味**: フォントの太さで重要度を表現。

**UX目的**:
- **強調**: 重要な単語やフレーズを太字で強調
- **視覚的バランス**: 太さのバリエーションで視覚的興味を引く
- **スキャンしやすさ**: 太字で重要な情報を素早く識別

**使用例**:
```css
.bold { font-weight: 700; }      /* 強い強調 */
.semibold { font-weight: 600; }  /* 中程度の強調 */
.normal { font-weight: 400; }    /* 通常 */
.light { font-weight: 300; }     /* 軽い */
```

---

## 10. アクセシビリティ

### `aria-*` 属性（HTMLと組み合わせ）
**意味**: スクリーンリーダー向けの情報を提供。

**UX目的**:
- **アクセシビリティ**: 視覚障害者にも情報を提供
- **セマンティック**: 要素の意味を明確に
- **WCAG準拠**: アクセシビリティガイドラインに準拠

**使用例**:
```html
<button aria-label="メニューを開く">
    <span aria-hidden="true">☰</span>
</button>

<div role="alert" aria-live="polite">
    エラーメッセージ
</div>
```

---

### `:focus-visible`
**意味**: キーボード操作時のみフォーカス表示。

**UX目的**:
- **UX向上**: マウスクリック時はフォーカス表示を非表示
- **アクセシビリティ**: キーボード操作時は必ず表示
- **視覚的クリーンさ**: 不要なフォーカス表示を削減

**使用例**:
```css
.button:focus {
    outline: none;  /* デフォルトのアウトラインを削除 */
}

.button:focus-visible {
    outline: 2px solid #007bff;  /* キーボード操作時のみ表示 */
}
```

---

### `prefers-reduced-motion`
**意味**: ユーザーがアニメーションを減らす設定を検出。

**UX目的**:
- **アクセシビリティ**: 動きに敏感なユーザーへの配慮
- **ユーザー設定の尊重**: システム設定に従う
- **WCAG準拠**: アクセシビリティガイドラインに準拠

**使用例**:
```css
.animated {
    animation: fadeIn 0.5s;
}

@media (prefers-reduced-motion: reduce) {
    .animated {
        animation: none;
    }
}
```

---

## よく使われる組み合わせパターン

### カードデザイン
```css
.card {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}
```

**UX目的**: 
- 情報を視覚的にグループ化
- ホバーでインタラクティブ性を示す
- モダンで洗練された印象

---

### ボタンデザイン
```css
.button {
    display: inline-block;
    padding: 12px 24px;
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
    background-color: #0056b3;
    transform: translateY(-1px);
}

.button:active {
    transform: translateY(0);
}
```

**UX目的**:
- 明確なクリック可能な要素
- 視覚的フィードバック
- ブランドカラーで統一

---

### モーダルデザイン
```css
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 999;
}

.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ffffff;
    border-radius: 12px;
    padding: 24px;
    max-width: 500px;
    width: 90%;
    z-index: 1000;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
```

**UX目的**:
- 重要な情報や操作を強調
- 背景を暗くして注意を集める
- 中央配置で視認性を確保

---

### ローディング表示
```css
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

**UX目的**:
- 処理中であることを明確に示す
- ユーザーの待機時間を視覚的に表現
- プロフェッショナルな印象

---

## まとめ

### 主要なUX目的別カテゴリ

1. **視覚的階層**: `font-size`, `font-weight`, `color`, `opacity`
2. **レイアウト**: `display: flex`, `display: grid`, `position`
3. **スペーシング**: `margin`, `padding`, `gap`
4. **インタラクティブ性**: `:hover`, `:focus`, `transition`, `transform`
5. **視覚的装飾**: `border`, `border-radius`, `box-shadow`, `background`
6. **レスポンシブ**: `@media`, `width`, `max-width`
7. **アクセシビリティ**: `:focus-visible`, `prefers-reduced-motion`, `aria-*`

### 実践のポイント

- **一貫性**: デザインシステムで統一された値を使用
- **パフォーマンス**: `transform`と`opacity`を優先（GPU加速）
- **アクセシビリティ**: コントラスト比、フォーカス表示、キーボード操作を考慮
- **レスポンシブ**: モバイルファーストアプローチ
- **ユーザビリティ**: 明確な視覚的フィードバック、適切なクリック領域

