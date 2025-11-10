# フロントエンドインターンシップ講義ガイド - 後半

## 目次（後半）

1. [標準化について](#1-標準化について)
2. [ビルドツールについて](#2-ビルドツールについて)
3. [Webフレームワークについて](#3-webフレームワークについて)
4. [心構え的な話](#4-心構え的な話)
5. [付録](#5-付録)

---

## 1. 標準化について

### 1.1 標準化団体と仕様

ブラウザで動く言語やAPIなどはそれぞれ以下のような仕様で標準化されています。

| 標準化団体 | 策定している仕様 |
|-----------|----------------|
| WHATWG | HTML Living Standard<br>DOM Living Standard<br>Fetch Living Standard |
| W3C | CSS Specifications<br>WCAG |
| TC39 | ECMAScript<br>Internationalization API |
| IETF | RFC xxx |

### 1.2 こうした仕様を知ることは重要

**APIの正しい振る舞いを定義しているのは仕様**
- 世の中に公開されている情報が数多くあるが...
- その情報の正しさを最終的に保証するための情報源が仕様

**ブラウザ間の差異への対応**
- 例えばJavaScriptやCSSなどの振る舞いがブラウザ間で異なる場合...
- その時に正しさを保証してくれるのは仕様である
- 実際、開発をしてると仕様とブラウザの差異に遭遇することもある

### 1.3 ECMAScriptについて

**JavaScriptの標準仕様**
- JavaScriptの標準仕様はECMAScriptと呼ばれる
- Ecma Internationalの中のTechnical Committee 39（TC39）という技術委員会により策定
- 現在の仕様はhttps://github.com/tc39/ecma262
- 常に最新版が公開され続けてる（Living Standard）
- 毎年6月頃にECMAScript 2024のようなタグが打たれる
- バージョン番号が付与したものも公開される

### 1.4 ECMAScriptのStage

ECMAScriptには自由に提案（proposal）を出せます。

**プロセスの流れ**
1. GitHub上でproposalが公開される
2. issue、PR、TC39のミーティングなどでの議論を経て、Stageが上がる
3. Stage 4になると仕様に取り込まれる

**Stageの詳細**

| ステージ | ステージの概要 |
|---------|--------------|
| 0 | アイデアの段階 |
| 1 | 機能提案の段階 |
| 2 | 機能の仕様書ドラフトを作成した状態 |
| 3 | 仕様がある程度固まってて、実装前にプロトタイプなどを作って実験する段階 |
| 4 | 仕様としては完成しており、ブラウザの実装やフィードバックを求める段階 |
| 5 | 仕様策定が完了し、2つ以上の実装が存在している状態 |

**注意点**
- Stage 3以前時点での実装などはその後の仕様変更などの可能性もあるので、ブラウザの開発者向けフラグを有効にしているときだけ使えたり、prefixを付けた名前でAPIが提供されることもある
- V8、SpiderMonkey、HermesといったJavaScriptエンジンなどに実装されてることが要求されてる

### 1.5 ECMAScriptの仕様と実装

**Stage 4になる前に実装される**
- 実装上の困難さ、使用上や仕様の問題などを確認するため
- その過程で仕様にフィードバックができたり、有用性を示せる

**PolyfillやBabelによるトランスパイル**
- Stage 4になる前に、polyfillやBabelによるトランスパイルがサポートされることも
- ブラウザに実装するより前に、ユーザに試してもらえる

### 1.6 ECMAScriptは全てがOpen

**誰でも参加できる**
- 誰でもプロポーザルを出せるし、読めるし、議論できる
- 興味のある提案があったら覗いたり、使ってみよう
- フィードバックすれば、JavaScriptをより良くできる

**ECMAScriptのプロポーザル**
- 多くの場合、その提案が「どのようなモチベーションがあるのか」、「どのような問題を解決するのか」、「どのようなユースケースがあるのか」などが記されている
- その有用性などを示すことも貢献に繋がります

### 1.7 JavaScript APIを策定する仕様

実は、JavaScriptの全てがECMAScriptで策定されてる訳では無いです。

| 仕様 | 策定している内容 |
|------|----------------|
| ECMAScript (TC39) | JavaScriptの構文や基本的なAPI |
| DOM Living Standard (WHATWG) | `document.querySelector`などのDOM API |
| Fetch Living Standard (WHATWG) | `fetch` API |
| Internationalization API (TC39) | `Intl.DateTimeFormat`などの国際化API |

### 1.8 ブラウザベンダとWHATWG仕様

**各ブラウザベンダの立場**
- GoogleはHTMLやDOMに関わるAPIの提案を数多く行ってる
- Chromeには取り込まれるが、AppleやMozillaの反対により、標準化されないことも

**仕様トラッカー**
- **Chrome Platform Status**: Chromeの仕様トラッカー
- **Mozilla Specification Positions**: Mozillaの立場を表明するウェブサイト
- **Standards Positions | Webkit**: Appleの立場を表明するウェブサイト

**Web Incubator Community Group**
- W3C内のWeb Incubator Community Groupで様々な提案が作成・議論されている

---

## 2. ビルドツールについて

### 2.1 ビルドツールとは

**なぜ必要か？**
- TypeScriptがそのまま実行されることは少ない
- 最適化などの様々な都合により、大抵はコードを変換してから実行する
- その変換に使われるツールを「ビルドツール」と呼ぶ

### 2.2 代表的なビルドツール

#### ① TypeScriptをJavaScriptに変換するツール

- `.ts` => `.js`へ変換するツール
- `.ts`はJavaScriptランタイムで直接実行できないので、変換が必要
- `tsc`, `swc`, `esbuild`など

#### ② 古いECMAScriptバージョンへ変換（downlevel）するツール

- 古いブラウザなどをサポートするために必要
- `tsc`, `babel`, `swc`, `esbuild`など

#### ③ JavaScriptファイルを結合するツール（bundler）

- ページアクセス直後のネットワークリクエストの数を減らすために必要
- `webpack`, `rollup`など
- CSSや画像ファイルなどもbundleできる

#### ④ JavaScriptファイルを圧縮するツール（minifier）

- ネットワーク転送量を減らすために必要
- `terser`など

### 2.3 統合的なビルドツール

**上記の機能をまとめて提供するツール**
- `next build/next dev`, `Vite`など
- 内部的には`swc`や`terser`などを使ってる
- 基本的には、これを使うと良い

### 2.4 統合的なビルドツールに備わってる機能

実は他にも色々な機能が備わってます。

#### Watchビルド
- ファイルの変更を監視して、変更があったら自動でリビルドする

#### 開発サーバー
- `localhost:3000`などで開発中のアプリケーションを配信してくれる

#### Hot Module Replacement (HMR)
- リビルド結果をブラウザに開いているページに、リロードなしで反映する

#### File-based routing
- ファイルの構成に基づいてルーティングすること
- Next.jsであれば`app/user/page.tsx`を作成すると`/user`にルーティングできるようになる仕組み

---

## 3. Webフレームワークについて

### 3.1 Webフレームワークとは

Webフレームワークと呼ばれるものもあります。

**代表例**
- Next.js
- Remix
- Nuxt.js
- Astro

**特徴**
- フロントエンド開発をすぐに始められるよう、色々組み込まれてる

### 3.2 Webフレームワークが組み込んでるもの

#### ビルドツールとその推奨設定
- いい感じの設定が組み込まれてて、ほぼ設定不要で使える

#### ルーティング
- ページ遷移時にソフトナビゲーションしたり、File-based routingをサポートしたり

#### サーバーサイドレンダリング（SSR）
- Node.jsサーバー上でコンポーネントをレンダーしてからHTMLを返す技術
- SEOや初回表示の高速化に寄与する

#### テストランナーの提供
- すぐにユニットテストやコンポーネントテストが書ける

### 3.3 どれを使えば良いか

作りたいものの要件に応じて適切なものを選びましょう。

| 要件 | 推奨ツール |
|------|-----------|
| React使ってSSRもしたい | Next.jsを使う |
| React使うけどSSRは不要で、SEOも気にしない | Vite + Reactを使う |
| Node.js向けライブラリを作りたい | `tsc`だけで十分<br>`.js`をネットワーク経由で取得しないので、bundler/minifierは不要 |

**重要な考え方**
- それぞれのツールの役割や目的を知っていれば、自ずと分かるはずです

---

## 4. 心構え的な話

### 4.1 フロントエンドの重要性

**ユーザーに直接触れる部分**
- フロントエンドは、直接ユーザが触れる部分
- ユーザからの評価に直結する

**良いUIを実装しよう**
- ユーザビリティやパフォーマンス改善をちゃんとやる
- ユーザのことを考える

### 4.2 アクセシビリティに気を使いましょう

**具体的な配慮点**
- キーボードで操作できたり
- 機械翻訳できたり
- 文字サイズを自由に変えたり

**障害者の方のため、だけではない**
- 健常者も文字サイズ変えたいことはある
- 皆のためにもなる

### 4.3 色々な職種の方と協力しよう

#### デザイナーと協力する
- デザイナーさんの力だけでは実現が難しいものを、エンジニアがサポートしたり
- アニメーションのPoC作ってみるとか

#### プランナーと協力する
- UIの実装をしているからこそ、ユーザビリティの改善点が見つかるはず
- エンジニア視点で新機能の提案してみるとか

**協力して、より良いものを作っていきましょう**

### 4.4 お疲れさまでした

**この講義で学んだこと**
- JavaScript/TypeScript/Reactについてざっと紹介しました
- これだけで完璧に理解した！とならないと思いますが...
- 開発に入るため・学ぶための足がかりになったはず

**フロントエンドの世界**
- JavaScriptやフロントエンドの世界は更に広がっています
- ブラウザを介して、ここまで多くのユーザの目に触れる分野は中々ありません
- 是非フロントエンドの世界を楽しんでください

---

## 5. 付録

本編に入り切らなかった踏み込んだ補足や解説について書いています。興味があれば読んでください的なコーナーです。

### 5.1 || と ?? の違い

**?? は比較的新しい構文**
- 昔のエンジンで動かなかった
- 古いJavaScriptコードでは、代わりに`||`が使われがち

**|| の挙動**
- 左辺がFalsy（偽とみなせるもの）なら右辺の値を返す
- Falsyな値の例: `false`/`null`/`undefined`/`NaN`/`0`/`''`（空文字）

**?? の挙動**
- 左辺が`undefined`または`null`の時に右辺の値を返す
- それ以外なら左辺の値を返す

**例**

```javascript
const price1 = 0 || 100; // 100 (0はFalsyなので)
const price2 = 0 ?? 100; // 0 (0はnull/undefinedではないので)
```

**推奨**
- 挙動が難しいので、`??`を使うのがオススメ

### 5.2 Arrow Functionに置き換え出来ないケース

以下のケースでは、Arrow Functionに置き換えできません：

1. **`function`を使ってコンストラクタ関数にしている（`new`している）**
2. **`arguments`を参照している**
3. **`this`を参照している**

このケースについて解説します。

### 5.3 Arrow Functionとthis

Arrow Functionと`function xxx(){...}`で`this`の扱いが異なります。このことによって単純な置き換えが不可な場合があります。

#### functionだと呼び出し元のオブジェクトがthisになる

```javascript
const person = {
  name: "chris",
  say: function () {
    setTimeout(function () {
      console.log(`I'm ${this.name}`)
    }, 100)
  },
}
person.say() // I'm (this.nameがundefined)
```

この場合は`window.setTimeout`（`window`は省略できる）からの呼び出しなので、`this`は`window`になります。

#### Arrow Functionだとスコープが外と同じになる

```javascript
const person = {
  name: "chris",
  say: function () {
    setTimeout(() => {
      console.log(`I'm ${this.name}`)
    }, 100)
  },
}
person.say() // I'm chris
```

Arrow Functionでは、外側のスコープの`this`を継承します。

### 5.4 useStateのstateを更新する際の注意

#### 新しい値を渡すときの落とし穴

```javascript
const [count, setCount] = useState(0)
const increase = () => setCount(count + 1)
```

としてしまうと、

```javascript
const incrementDouble = () => {
  increment()
  increment()
}
```

のようなものを作ったときに、`incrementDouble`を呼んでも1しか増えません。

#### 関数内の変数スコープとuseState

例えば、以下のようなコードがあった時:

```javascript
const Component = () => {
  const [count, setCount] = useState(0)
  const increment = () => setCount(count + 1)
  const incrementDouble = () => {
    increment()
    increment()
  }
}
```

これと同じ意味になる:

```javascript
const Component = () => {
  const [count, setCount] = useState(0)
  const incrementDouble = () => {
    setCount(count + 1) // count = 0 の時、`setCount(1)` になる
    setCount(count + 1) // count = 0 の時、`setCount(1)` になる
  }
}
```

**問題点**: 両方とも`count`の値が`0`の時点での値を使っているため、2回呼んでも1しか増えません。

#### setterに関数を渡すと良い

```javascript
setCount((prevCount) => prevCount + 1)
```

とすると、期待通りになります。

```javascript
const Component = () => {
  const [count, setCount] = useState(0)
  const increment = () => setCount((prevCount) => prevCount + 1)
  const incrementDouble = () => {
    increment() // count = 0 の時、`setCount(0 + 1)` になる
    increment() // count = 1 の時、`setCount(1 + 1)` になる
  }
}
```

**推奨**: 更新後のstateの値が更新前の値に依存している場合は、関数を渡す形式を使いましょう。

### 5.5 Hooksの依存配列の変更検知について

**依存配列の値が変わったかは`Object.is`で検証される**

```javascript
console.log(Object.is("foo", "foo")) // true
console.log(Object.is({ prop: "foo" }, { prop: "foo" })) // false
const objA = { prop: "foo" }
const objB = objA
console.log(Object.is(objA, objB)) // true
```

**重要なポイント**: 同じ内容のオブジェクトでも、参照が異なると変わったと認識されます。

### 5.6 依存配列にオブジェクトを入れるケースについて

```javascript
function Component() {
  const config = { theme: "sports" }
  useEffect(() => {
    loadConfig(config).then(() => {})
  }, [config])
}
```

のような場合にはレンダリングの度に、`config`が再生成される。よって、異なる値として認識されてしまい、毎回エフェクトが実行されてしまう。

**注意**: このような例の場合は依存に`[config.theme]`という風に値を書いてしまっても良いが、依存するオブジェクトについて知っている必要があるので難しい。

### 5.7 シンプルな回避策

**一番簡単な回避策はComponentの外で初期化すること**

```javascript
const config = { theme: "sports" }
function Component() {
  useEffect(() => {
    loadConfig(config).then(() => {})
  }, [config])
}
```

**一方で、Propsを利用してオブジェクトを生成してる場合は採用できない**

### 5.8 useMemoを使った回避策

`useMemo`はReactに組み込まれているHooksで、値のメモ化ができます。これで過度なエフェクトの再実行を防げます。

```javascript
function Component({ theme }) {
  const config = useMemo(() => ({ theme }), [theme])
  useEffect(() => {
    loadConfig(config).then(() => {})
  }, [config])
}
```

**メモ化**: パフォーマンス改善のために計算結果をキャッシュしたりすること

### 5.9 useCallbackで関数をメモ化する

**関数も実態はオブジェクト**
- コンポーネント内で関数宣言すると、毎回再生成されてしまう
- 値同様に関数をメモ化したい場合は`useCallback`を利用する

```javascript
const handler = useCallback((val) => alert(val), [])
useEffect(() => {
  Api.notification.subscribe(handler)
}, [handler])
```

### 5.10 React Component内でDOMにアクセスする

Reactに組み込まれている、参照を保持できる`ref`オブジェクトを作成する`useRef`を使います。

- `ref`オブジェクトは`current`プロパティに現在の値を持っている

```javascript
const textInput = useRef(null)
const submit = (e) => {
  e.preventDefault()
  if (textInput.current.value.length < 100)
    return alert("101文字以上が必要です")
  createPost({ body: textInput.current.value })
}
return (
  <form onSubmit={submit}>
    <input type="text" ref={textInput} />
  </form>
)
```

### 5.11 DOMへのアクセスを避ける方が良い

**DOMに直接アクセスすると、Reactの制御外のところで値が取得されたり変更されることに**

- ライブラリの都合などで本当に必要なときのみにしておくと良い

**推奨される方法**

```javascript
const [text, setText] = useState("")
const submit = (e) => {
  e.preventDefault()
  if (text < 100) return alert("101文字以上が必要です")
  createPost({ body: text })
}
return (
  <form onSubmit={submit}>
    <input type="text" onChange={(e) => setText(e.target.value)} />
  </form>
)
```

Reactの状態管理を使うことで、Reactの制御下で値を管理できます。

---

## まとめ（後半）

後半では、以下の内容を学習しました：

1. **標準化について**
   - ECMAScript、WHATWG、W3Cなどの標準化団体
   - Stageプロセス
   - 仕様の重要性

2. **ビルドツールについて**
   - TypeScriptの変換、bundling、minification
   - 統合的なビルドツール（Next.js、Viteなど）
   - Watchビルド、HMRなどの開発支援機能

3. **Webフレームワークについて**
   - Next.js、Remix、Nuxt.js、Astroなど
   - SSR、ルーティング、テストランナーなどの機能
   - 要件に応じた選択方法

4. **心構え的な話**
   - ユーザーを第一に考える
   - アクセシビリティへの配慮
   - 他職種との協力

5. **付録**
   - `||`と`??`の違い
   - Arrow Functionと`this`のスコープ
   - `useState`の更新時の注意点
   - Hooksの依存配列とメモ化
   - DOMへのアクセス方法

---

## 全体のまとめ

この講義ガイドでは、フロントエンド開発に必要な基礎知識から実践的な内容まで、段階的に学習できるよう構成しました。

**重要なポイント**

1. **基礎を固める**
   - JavaScript/TypeScriptの基礎をしっかり理解する
   - Reactの概念と使い方をマスターする

2. **背景を理解する**
   - 各技術が登場した背景を考える
   - 長く通用する知識を身につける

3. **実践する**
   - 実際にコードを書いてみる
   - エラーと向き合いながら学ぶ

4. **継続的に学ぶ**
   - 標準化の動向を追う
   - 新しい技術の背景を理解する

**次のステップ**

- 実際にプロジェクトを作ってみる
- 公式ドキュメントを読む
- コミュニティに参加する
- 他の開発者と交流する

フロントエンドの世界は広く、常に変化しています。しかし、基礎をしっかり固め、技術の背景を理解することで、変化に対応できるようになります。

是非フロントエンドの世界を楽しんでください！

