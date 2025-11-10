# フロントエンドインターンシップ講義ガイド - 前半

## 概要

このドキュメントは、2025年8月18日に実施されたフロントエンドインターンシップ講義の解説です。Webフロントエンド開発に必要な基礎知識から実践的な内容まで、段階的に学習できるよう構成されています。

**講義のゴール**
- フロントエンド開発で必須の知識を押さえる
- それぞれの技術が登場した背景を知る
- 長く通用する知識を身につける

---

## 目次（前半）

1. [はじめに](#1-はじめに)
2. [JavaScriptについて](#2-javascriptについて)
3. [TypeScriptについて](#3-typescriptについて)
4. [Reactについて](#4-reactについて)

---

## 1. はじめに

### 1.1 Webフロントエンドとは

「Webフロントエンド」と聞いて、何を思い浮かべますか？

フロントエンド開発は、ユーザーが直接触れる部分を実装する領域です。HTML、CSS、JavaScriptを中心に、モダンな開発ではReactやNext.jsなどのフレームワークも使用されます。

### 1.2 必要な知識の一例

フロントエンド開発に必要な知識は多岐にわたります：

**基礎知識**
- Webページ/ブラウザ/サーバの関係性・役割
- HTML/CSS/JavaScript（言語）

**フレームワーク・ライブラリ**
- React, Next.js（Viewライブラリ/フレームワーク）

**セキュリティ**
- XSS, CSP

**パフォーマンス**
- Web Vitals

**その他**
- アクセシビリティ
- bundler, linter, formatter, test runner（開発ツール）

### 1.3 フロントエンドへのよくある印象

#### 「覚えることが多い」

確かにそうかもしれませんが、フロントエンド以外の領域でも同じことが言えます。

- アクセシビリティ/言語ツールは、この領域特有かもしれませんが...
- 言語/ライブラリ/パフォーマンスの知識は、他の領域でも必要
- あんまり恐れる必要はない

#### 「技術の流れが早い」

確かにそうかもしれません。

- フロントエンドはユーザーに近くて、コーディング人口が多い領域
- そのため、頻繁に新技術が出てくる

**向き合い方を変えるべき**
- 流行を追うのも良いけど...その技術が登場した背景を考えよう
- ライブラリの使い方を覚えるのも良いけど...長く通用する知識も身につけよう

---

## 2. JavaScriptについて

### 2.1 変数宣言

JavaScriptでは、`let`と`const`を使って変数を宣言します。

```javascript
// 変数と宣言
let a = "a" // let は上書き可能
const b = "b" // 上書き不可能
a = "A" // OK
b = "B" // Cannot assign to "b" because it is a constant
```

**ベストプラクティス**
- 変数宣言は`const`をできるだけ使うと良い
- 変数の値が変わることを考慮しなくて済む

### 2.2 プリミティブ型 / オブジェクト

JavaScriptには、プリミティブ型とオブジェクトがあります。

```javascript
const id1 = "1234" // string
const id2 = '1234' // string
const name = null // null
const age = 2022 // number
const isAdmin = false // boolean

// object
const user = {
  id: "1234",
  username: null,
  age: 2022,
  isAdmin, // `isAdmin: isAdmin` の省略形
}

user.age // 2022
// 未定義プロパティだと undefined が返る
user.abc // undefined
```

### 2.3 関数 / 配列

```javascript
// 関数
function add(a, b) {
  return a + b
}
add(1, 2) // 3

// 配列
const array1 = [1, 2]
// 配列操作
array1[0] // 1
for (elm of array1) {
  console.log(elm)
}
array1.forEach((elm) => {
  console.log(elm)
})
array1.map((elm) => elm * 2) // [2, 4]
```

### 2.4 Arrow Function

Arrow Functionは、簡潔に関数を書くための構文です。

```javascript
const add = (a, b) => {
    return a + b
}

// 1行だけなら return などを省略可
const add = (a, b) => a + b

// 引数が 1 つのときは引数を囲う `()` も省略可
const hello = name => `Hello, ${name}`

// 返り値がオブジェクトのときは `()` で囲う必要がある
const getProps = () => ({ a: "foo", b: "bar" })
```

### 2.5 typeof演算子

値の実行時の型を返す演算子です。

```javascript
const str = "hello world"
console.log(typeof str) // 'string'
console.log(typeof 10) // 'number'
console.log(typeof { name: "jonh", age: 20 }) // 'object'
console.log(typeof undefined) // 'undefined'
console.log(typeof ["a"]) // 'object'
console.log(typeof null) // 'object' (注意: nullは'object'と表示される)
```

### 2.6 in演算子

値に特定のプロパティがあることを判定する演算子です。ブラウザが特定のAPIに対応しているかどうかを識別することにも使われます。

```javascript
const user = { name: "hatena", age: 20 }
if ("name" in user) {
  console.log("user has name property")
}

if ("fetch" in window) {
  console.log("This browser supports fetch API")
}
```

### 2.7 Promiseについて

Promiseは、非同期処理を抽象化したオブジェクトです。

**3つの状態**
- **Pending**: 初期状態。成功も失敗もしていない
- **Fulfilled**: 非同期処理が成功した
- **Rejected**: 非同期処理が失敗した

まずPendingになって、その後Fulfilled or Rejectedになります。

#### Promiseの生成方法

```javascript
function sleep(ms) {
  return new Promise((resolve, reject) => {
    if (typeof ms !== "number") {
      reject(new Error("ms must be a number"))
      return
    }
    setTimeout(() => {
      resolve(ms)
    }, ms)
  })
}
```

#### コールバックの登録

```javascript
sleep(1000)
  .then((ms) => console.log(`sleep: ${ms}ms`))
  .catch((e) => console.error(e))
```

- `then`メソッド: Fulfilledになった時に呼ばれるコールバックを登録
- `catch`メソッド: Rejectedになった時に呼ばれるコールバックを登録

#### fetchを使った例

```javascript
const promise = fetch("https://api.example.com/user/1") // ①
  .then((res) => /* ② */ res.json())
  .then((json) => /* ③ */ console.log(json.user))
  .catch((e) => /* ④ */ console.error(e))
console.log(promise) // ⑤

// ① => ⑤ => ② => ③ => ④ の順に実行されることに注意
// コールバック関数は非同期処理が完了後に実行される (遅延される)
```

### 2.8 async/await

非同期処理を簡潔に書くための構文です。`then`や`catch`を使わずに、同期的なコードっぽく書けます。

```javascript
const getUser = async (id) => {
  try {
    const res = await fetch(`https://api.example.com/user/${id}`)
    const json = await res.json()
    const user = json.user
    console.log(`${user.name}のidは${user.id}`)
    return user
  } catch (e) {
    console.error(e)
    throw new Error("error reason: *********")
  }
}
```

エラーハンドリングには`try {} catch (e) {}`を使用します。

**注意点**
- `async function`自体も暗黙的にPromiseを返す
- 関数の返り値に対して、`then`を呼び出せる

```javascript
getUser(1)
  .then(console.log) // {id: 1, name: 'hatena'}
  .catch(console.error)
```

### 2.9 ECMAScript Modules (ES Modules)

プログラムをモジュールという単位に分割する機能です。

**特徴**
- 1ファイル == 1モジュール
- スコープはモジュールごと
- 関数や変数などを`import`/`export`できる

#### named export, named import

```javascript
// lib.js
export const logLevel = {
  WARN: "warn",
  ERROR: "error",
};
export function log(message, level) {/* ... */}

// main.js
import { logLevel, log } from './lib.js'
```

#### default export

```javascript
// lib.js
export default function (message, level) {/* ... */}

// main.js
import awesome from "./lib"
```

- `export default`というキーワードでもexportできる
- 名前を付けずにエクスポートできる
- `export default`できるのは、1つのモジュールにつき1つだけ
- import時に任意の名前を設定できる

#### import/exportの細かい挙動

```javascript
// as でリネーム出来る
import { logType as LOGTYPE } from "./namedModule"

// * as で export されているもの全てをオブジェクトにまとめる
import * as Logger from "./namedModule"
Logger.hello() // 'hello'
```

**注意**: 必要なものだけを取り込むことで受けられる恩恵（webpackによるTreeShakingなど）も多いので、基本的には`* as`は避ける方がオススメです。

### 2.10 for...of

反復可能（iterable）なオブジェクトの要素を順番に取り出せます。

```javascript
const iterable = [10, 20, 30]
for (const value of iterable) {
  console.log(value)
}
```

配列、文字列、NodeList、Map、Setなどが反復可能です。

### 2.11 Nullish coalescing operator ??

```javascript
// a ?? b のようにして使う
// 左辺が undefined or null の時に右辺の値を返す
// それ以外なら左辺の値を返す
// デフォルト値に fallback させるのに便利

function greet(name) {
  return `Hello, ${name ?? "mizdra"}!`
}
```

### 2.12 Optional chaining ?.

プロパティアクセス（`a.b`）の亜種で、`a?.b`のように書きます。

```javascript
// a が null または undefined のときは undefined を返す
// それ以外のときは通常通りプロパティアクセスを行う

const userId1 = session.user?.id;
const userId2 = session.user ? session.user.id : undefined;

// 関数呼び出しとも組み合わせられる
const result = someObject?.someMethod?.(arg1, arg2);
```

### 2.13 Spread Syntax

`...`を使うと配列やオブジェクトを展開できます。

```javascript
const sum = (a, b, c, d) => a + b + c + d
const nums = [1, 2]
const copied = [...nums] // 中身を複製した配列を作れる
const moreNums = [...copied, 5] // [1, 2, 5]
sum(...nums, 10) // 13

const obj = { a: 10, b: "foo" }
const obj2 = { b: "bar", c: true }
// 2つ以上のobjectをmergeする。キーが重複している場合は後に書いた方で上書きされる
const merged = { ...obj, ...obj2 } // {a: 10, b: 'bar', c: true}

const getUserConfig = (received) => ({
  force: false,
  ...received, // デフォルト値を渡された値があれば上書きする
})
```

### 2.14 Rest Parameters

関数の引数も`...`で受け取ることで可変な長さの引数を受け取れます。

```javascript
// Spread Syntax と違って、1 つだけ且つ引数の末尾でしか使えない
const sum = (num1, num2, ...nums) =>
  num1 + num2 + nums.reduce((a, b) => a + b, 0)

const numbers = [1, 2, 3]
sum(3, ...numbers, 6) // 15
```

---

## 3. TypeScriptについて

### 3.1 TypeScriptとは

TypeScriptは、JavaScriptに静的型付けを導入した言語です。

**特徴**
- JavaScript + 型注釈
- コンパイラ（tsc）で型チェックを行う
- 現代では生のJavaScript書くより、TypeScriptで書くことが多い

```typescript
function hello(name: string): string {
  return `Hello, ${name}!`
}
const result = hello(1)
//                   ^
// Type Error: Argument of type '1' is not assignable to parameter of type 'string'.
```

### 3.2 なぜTypeScriptが必要か？

**型エラーを未然に防ぐため**
- 実行した時ではなく、コードを書いてる時に気付けるように

**コードを変更しやすくするため**
- Rename/補完
- コードジャンプ

**コードを読みやすくするため**
- 型がドキュメント代わりに

### 3.3 tsc: TypeScript compiler

TypeScript言語のためのコンパイラです。

**主な機能**
- 型チェックをする
- TypeScriptで書かれたコードをJavaScriptに変換する
- 変換といっても、型アノテーション等の削除くらい

### 3.4 変数宣言時の型アノテーション

```typescript
// JavaScriptの場合
const a = 'hello';

// TypeScriptの場合は変数名と=の間に:を置いて型アノテーションを書く
const a: string = 'hello';

// これくらいだったら推論されるので、普通は省略されます
```

### 3.5 代表的な表現

#### プリミティブ型

```typescript
const a: number = 10
const b: boolean = false
const c: string = "hello"
const d: "hello" = "hello" // リテラル型
const n: null = null
```

#### 配列

```typescript
const arr: string[] = ["hello", "world"]
const arr2: Array<number> = [1, 2, 3, 5, 8]
const arr3: [string, number] = ["year", 2021] // タプル(Tuple)型
```

#### オブジェクト

```typescript
const person: {
  name: string
  age: number
  address?: string // ? を付けるとオプショナルなキーになる
} = {
  name: "john",
  age: 21,
}
```

**注意**: `string | undefined`のような記述と同じと紹介されることもあるが、値が入っているかどうかでJavaScriptとして実行した際の振る舞いが変わることがある（`Object.keys()`など）ので、厳密には同じではないことに注意。

### 3.6 type

`type`を使うと型にエイリアスを付けられます。

```typescript
type Person = {
  name: string
  age: number
}
type Team = Person[]
```

### 3.7 Union Type（合併型）

複数の型のいずれかを満たす型です。

```typescript
type Color = "red" | "green" | "blue" | "yellow" | "purple"
const c: Color = "red"
const d: Color = "black" // Type Error
```

### 3.8 Narrowing（型の絞り込み）

緩い型をいくつかの型に絞り込んでから、絞り込まれたそれぞれに対して処理したいことがあります。

```typescript
function padLeft(padding: number | string, input: string): string {
  if (typeof padding === "number") {
    // このブロック内では `padding` は `number` 型
    return " ".repeat(padding) + input;
  } else if (typeof padding === "string") {
    // このブロック内では `padding` は `string` 型
    return padding + input;
  }
  throw new Error("unreachable");
}
```

一部のJavaScriptの演算子を使うと、型の絞り込み（Narrowing）ができます。

#### typeof演算子

```typescript
function padLeft(padding: number | string, input: string): string {
  if (typeof padding === "number") {
    // このブロック内では `padding` は `number` 型
  } else if (typeof padding === "string") {
    // このブロック内では `padding` は `string` 型
  }
}
```

#### in演算子

```typescript
type Fish = { name: string, swim: () => void }
type Bird = { name: string, fly: () => void }

const move = (x: Fish | Bird) => {
  if ("swim" in x) {
    // Fish 型に絞り込まれる
    return x.swim()
  }
  // ここでは Bird 型に絞り込まれる
  return x.fly()
}
```

#### Tagged Union Types

Union Typeの個々の型に、`kind`のようなプロパティを持たせるテクニックです。

```typescript
type Fish = {
  kind: "fish"
  // ...
}
type Bird = {
  kind: "bird"
  // ...
}

const move = (x: Fish | Bird) => {
  if (x.kind === "fish") {
    return x.swim()
  }
  return x.fly()
}
```

`in`による絞り込みより堅牢な書き方で、おすすめです。

### 3.9 asを用いた型アサーション（Type Assertion）

TypeScriptによって推論された型を上書きしたいときに使います。

**注意点**
- 型キャストではない（ランタイム上での振る舞いがなんら変わることはない）
- 多くの場合は害になるので、本当に必要な場合だけ利用する
- 例えば、古いJavaScriptのコードを移植するなど

```typescript
type Foo = {
  bar: number
  piyo: string
}

const foo1: Foo = { bar: 1, piyo: "2" } // OK
const foo2: Foo = {} // NG
const foo3: Foo = {} as Foo // OK
```

### 3.10 constアサーション

`as const`とすることで変数代入時などに変更不可能としてアサーションしてくれます。

```typescript
const a = [1, 2, 3] // aの型はnumber[]となる
const b = [1, 2, 3] as const // bの型はreadonly [1, 2, 3]となる
// readonly な配列には push や pop などの変更を加えるメソッドが存在しない

a.push(4) // OK
b.push(4) // NG

type Pallet = {
  color: Color
}

const setPallet = (p: Pallet) => {
  /* do something */
}

const pallet = {
  color: "red",
} // ここに as const を付けないと{ color: string }と推論されてエラーになる
setPallet(pallet)
```

### 3.11 不定な型を扱う方法

#### any

どんな値でも入れられる型です。

```typescript
let anything: any = {}
// anyには何でも代入できる
anything = () => {}
anything = null
anything.split(",") // anyの場合はメソッドもなんでも参照できる
```

- Rustの`unsafe`のようなもの
- 自由に書けるが、コンパイラは何も警告しない
- `as`同様に避けられる場合は避ける

#### unknown

`any`同様にどんな値でも入れられますが、`any`と違い、`unknown`はプロパティアクセスが型エラーになります。

```typescript
const val: unknown = { name: "foo" };
val.name // Type Error: Property 'name' does not exist on type 'unknown'.

// 型を絞り込んでからアクセスする必要がある
if (typeof val === "object" && 'name' in val) {
  console.log(val.name) // OK
}
```

- `unknown ≒ {} | null | undefined`

### 3.12 関数

```typescript
const f = (x: string): number => {
  return x.length
}

// 特にreturnをしない場合は返り値にvoidを指定する
const a: () => void = () => {
  console.log("a")
}

// オプショナルな引数はkeyに?を付ける
// 推論されるもので良いなら返り値の型は省略可
const b = (n?: number) => `${n}`

// Rest Parametersを受け取る場合はこういう感じ
const c = (...texts: string[]) => {
  return texts.join("|")
}
```

### 3.13 型引数（Generics）

関数の返り値の型に関する制約を外から与えて、関数内部で利用できます。

```typescript
const getJSON = <T>(url: string): Promise<T> => {
  // res.jsonはanyとならずに型引数で渡されたものと解釈される
  return fetch(url).then<T>((res) => res.json())
}

// ここでusersはUser[]になる
const users = await getJSON<User[]>("/api/users")
// ここでblogsはBlog[]になる
const blogs = await getJSON<Blog[]>("/api/blogs")
```

#### extendsを使う

`extends`を使うと指定した型/インターフェースを満たすように指定できます。

```typescript
const echo = <T extends string>(text: T): T => {
  return text
}

const a = echo("foo") // a の型は 'foo'
const str: string = "foo"
const b = echo(str) // b の型は 'string'
```

### 3.14 TypeScriptの書き方で困ったら？

- **公式ドキュメントのHandbookを読もう**
  - https://www.typescriptlang.org/docs/handbook/intro.html
- **Playgroundで試し書きしよう**
  - https://www.typescriptlang.org/play
- **難しい型の書き方はType Challengeに結構載ってる**
  - https://github.com/type-challenges/type-challenges

---

## 4. Reactについて

### 4.1 Reactとは

Reactは、ユーザインターフェースを構築するためのViewライブラリです。

**特徴**
- UIを関数で定義する
- 「仮想DOM」と呼ばれるオブジェクトを返す
- Reactがその仮想DOMを元に、実際のDOMを更新する
- JSXというHTML-likeな拡張構文を使う

### 4.2 仮想（Virtual）DOM

Reactの内部で持っている、実際のDOMの対になる構造体です。

**動作の流れ**
1. 状態の変更を検知すると...
2. 変更前後の仮想DOMの差分を計算し、その差分だけを実際のDOMに反映

### 4.3 Reactの何が嬉しい？

**DOMをどう更新するかを意識しなくて済む**
- 完成形の仮想DOMを返せば、Reactがいい感じに更新してくれる

**DOMの状態更新を簡潔に書ける**
- `id=...`を付けて、`getElementById`で要素を取ってきて...が不要に
- `value={newTodo}`と書くだけでOK

**マークアップとロジックを近くに置ける**
- 関連するものが近くにあることで、認知負荷が下がる（コロケーション）
- 1つの関数にまとまってるので、テストもしやすい

### 4.4 JSX

JavaScriptにHTMLっぽい記法を追加した拡張構文です。

```jsx
<h1 className="hello">My name is Clementine!</h1>
```

**注意点**
- HTMLの属性名ではなく、キャメルケースの命名規則を使用
- `class`は`className`と記述される（`class`がJavaScriptにおいて予約語であるため）
- `aria-*`や`data-*`属性は例外

### 4.5 関数コンポーネントとクラスコンポーネント

Reactではコンポーネントの書き方が2種類あります。

#### 関数コンポーネント

```jsx
const HelloMessage = ({ name }) => {
  return <div>Hello {name}</div>
}
```

#### クラスコンポーネント

```jsx
class HelloMessage extends React.Component {
  render() {
    return <div>Hello {this.props.name}</div>
  }
}
```

**使い分け**
- 基本的にはどちらも同じことができる
- 関数コンポーネントのほうがシンプルで、書きやすい
- 公式ドキュメントでも関数コンポーネントが推奨されている
- **関数コンポーネントを使おう**
- ただし、一部APIがクラスコンポーネントでしか使えない（Error Boundary関連のAPIなど）
- そういう時だけ、クラスコンポーネントを使うと良い

### 4.6 Function ComponentとTypeScript

色々な書き方があります。

```typescript
// React.FC<Props>を使うパターン
type Props = { name: string }
const Welcome: React.FC<Props> = ({ name }) => {
  return <h1>Welcome {name}</h1>
}

// 型推論に任せるパターン
function Welcome({ name }: { name: string }) {
  return <h1>Welcome {name}</h1>
}
```

**書き方の選択**
- arrow function or function宣言
- type aliasでPropsを定義する or inlineで書く
- `React.FC<Props>`を使う or 使わない（型推論に任せる）
- どう書くかは好みで良いと思う

**注意**: `React.FC<Props>`を使うと、React Componentとして不正な`undefined`を返すことをコンパイル時に防止できます。

### 4.7 PropsとState

React Componentには値を持つ方法が大きく2つあります。

- **Props**: 関数の引数として受け取る
- **State**: 内部状態を保持する

#### Propsを渡す/受け取る

```jsx
// 受け取る側は関数の第1引数でオブジェクトとして受け取る
type Props = { name: string }
const Welcome: React.FC<Props> = ({ name }) => {
  return <h1>Welcome {name}</h1>
}

// 渡す側(親側)は JSX の属性値の記法で渡す
<Welcome name="John" />
// <h1>Welcome John</h1>
```

### 4.8 Hooks

フックを使うことで、さまざまなReactの機能に「接続（hook into）」して使用することができます。

**Hooksの掟**
- 名前は`use`から始める
- トップレベルで呼ぶ
- `if`の中などで呼ばない
- early returnする前に必ず呼ぶ

これらは`eslint-plugin-react-hooks`で検出してくれるように出来ます。

**注意**: React 19+で導入された`use`は、例外的に条件分岐の中で呼び出せます。

### 4.9 useState

コンポーネントに状態を持たせるためのHookです。

```jsx
const Counter = () => {
  const [count, setCount] = useState(0)
  const increaseCount = () => setCount((prevCount) => prevCount + 1)
  return (
    <div>
      カウント: {count}
      <button onClick={increaseCount}>カウント</button>
    </div>
  )
}
```

**使い方**
- `useState(initial)`で初期値を渡す
- 返り値はタプル
- 1つ目が現在の値で、2つ目がsetter
- setterを呼ぶと内部状態が更新されたことがReactに通知される
- 仮想DOMの再生成、比較、レンダリングの更新が行われる

**型指定**
```typescript
const [count, setCount] = useState(0)
const [color, setColor] = useState<Color>("red")
```

#### useStateのsetterについて

```jsx
// 新しい値を渡す
const [color, setColor] = useState<Color>("red")
const change2Blue = () => setColor("blue")

// 直前の値を利用して新しい値を決定する
const [count, setCount] = useState(0)
const increaseCount = () => setCount((prevCount) => prevCount + 1)
```

**重要**: 更新後のstateの値が更新前の値に依存している場合は、関数を渡す形式を使いましょう。

### 4.10 useEffect

外部システムに接続し、同期させるためのHookです。

**使用例**
- APIからデータを取得する
- 生のDOM APIを使う
- アニメーションさせる
- Reactの外のシステムと接続したい時に使う

#### setIntervalでタイマーと同期する

```jsx
const Timer = () => {
  const [duration, setDuration] = useState(1000)
  useEffect(() => {
    setInterval(() => {
      console.log("tick")
    }, duration)
  }, [])
  return (
    <div>
      <input type="number" value={duration} onChange={(e) => setDuration(+e.target.value)} />
      <div>間隔: {duration}</div>
    </div>
  )
}
```

これでComponentのマウント時に`setInterval`が呼ばれ、指定した間隔で`tick`が出力されます。

#### useEffectと依存配列

- デフォルトでは、エフェクトはレンダー時に毎回実行される
- しかし、それが望ましくない場合もある
- `useEffect`の第2引数（依存配列）で、不必要な実行を防げる

```jsx
// マウント時にだけ副作用を実行
useEffect(任意の処理関数, [])

// val1 や val2 のいずれかが変更されたときにエフェクトを実行
useEffect(任意の処理関数, [val1, val2])
```

**例: カウンターのカウントが変わるたびに、サーバーにメトリクスを送る**

```jsx
const Counter = () => {
  const [name, setName] = useState("インターンに参加した回数")
  const [count, setCount] = useState(0)
  useEffect(() => {
    fetch(`/api/user-metrics?count=${count}`)
  }, [count])
  return (
    <>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
      <button onClick={() => setCount(c => c + 1)}>
        Increment
      </button>
      <div>{count}</div>
    </>
  )
}
```

`name`が変わっても、メトリクスは送られない。

#### 依存配列は自分で選ぶものではない

- 基本的には、エフェクトから参照されてる値を全て依存配列に入れる
- ESLint + `eslint-plugin-react-hooks`を使うと、入れ忘れてる値を警告してくれる
- この警告に従うのがセオリー

```jsx
useEffect(() => {
  fetch(`/api/user-metrics?count=${count}`)
}, [])
// ^^ React Hook useEffect has a missing dependency: 'count'.
//    Either include it or remove the dependency array.
```

**注意**: 全ての参照値を依存配列に入れるといっても、「この値が変わる度に実行されると困る」ケースもあります。その場合はエフェクトを分割するなどがセオリーとされています。

#### useEffectとクリーンアップ

エフェクトから関数を返せます。これをクリーンアップ関数と呼びます。

- 次のエフェクトが実行される前に呼ばれる
- これを利用すると副作用のクリーンアップが出来る

```jsx
useEffect(() => {
  const id = setInterval(() => {
    console.log("tick")
  }, duration);
  return () => {
    // clearInterval でタイマーを停止する関数
    clearInterval(id)
  }
}, [duration])
```

**注意**: 空配列を指定している場合などはアンマウント時にも実行されます。

### 4.11 独自フック（Custom Hook）

内部で他のHookを呼び出す関数で、`use`から名前が始まるもののことです。

**用途**
- 複数のHooksを組み合わせたり
- Componentの振る舞いを共通化して、1つの関数に切り出すときなどに利用する

```jsx
const useUserStatus = ({ userId }) => {
  const [status, setStatus] = useState(null)
  useEffect(() => {
    const handler = (user) => {
      setStatus(user.status)
    }
    Api.subscribe(userId, handler)
    return () => Api.unsubscribe(userId, handler)
  })
  return status
}

function SomeComponent({ userId }) {
  const status = useUserStatus({ userId })
  return <div>{status}</div>
}
```

**独自フックについてのTips**
- 独自フックに切り出すことで、その部分をテストできる
- 独自フックの中では`useMemo`、`useEffect`、`useCallback`を積極的に使う
- パフォーマンス最適化のためになる

---

## まとめ（前半）

前半では、以下の内容を学習しました：

1. **JavaScript基礎**
   - 変数宣言、型、関数、配列
   - Promise、async/await
   - ES Modules
   - 便利な演算子（`??`, `?.`, `...`など）

2. **TypeScript**
   - 型システムの基礎
   - 型の絞り込み（Narrowing）
   - Generics
   - 不定な型（`any`, `unknown`）

3. **React**
   - コンポーネントの書き方
   - PropsとState
   - Hooks（`useState`, `useEffect`）
   - 独自フック

次回（後半）では、標準化、ビルドツール、Webフレームワーク、心構え、付録について解説します。

