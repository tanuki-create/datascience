# フロントエンド - 面接対策ガイド

## 1. デザイン実現力

### 1.1 CSS基礎とレイアウト

#### Flexboxの活用

**基本的なFlexboxパターン**
```css
/* 中央揃え（水平・垂直） */
.container {
    display: flex;
    justify-content: center;  /* 水平方向 */
    align-items: center;      /* 垂直方向 */
    min-height: 100vh;
}

/* カードレイアウト（等間隔配置） */
.card-container {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.card {
    flex: 1 1 300px;  /* 最小幅300px、必要に応じて伸縮 */
    min-width: 0;     /* オーバーフロー防止 */
}

/* ヘッダー・フッター・メインコンテンツ */
.layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.header {
    flex-shrink: 0;  /* 縮小しない */
}

.main {
    flex: 1;  /* 残りのスペースを占有 */
}

.footer {
    flex-shrink: 0;
}
```

#### CSS Gridの活用

**複雑なレイアウト**
```css
/* グリッドレイアウト */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    grid-auto-rows: minmax(200px, auto);
}

/* 複雑なグリッドレイアウト（ヘッダー、サイドバー、メイン、フッター） */
.app-layout {
    display: grid;
    grid-template-areas:
        "header header header"
        "sidebar main main"
        "footer footer footer";
    grid-template-columns: 200px 1fr 1fr;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
}

.header {
    grid-area: header;
}

.sidebar {
    grid-area: sidebar;
}

.main {
    grid-area: main;
}

.footer {
    grid-area: footer;
}
```

#### レスポンシブデザイン

**メディアクエリの活用**
```css
/* モバイルファーストアプローチ */
.container {
    padding: 10px;
}

/* タブレット */
@media (min-width: 768px) {
    .container {
        padding: 20px;
        max-width: 750px;
        margin: 0 auto;
    }
}

/* デスクトップ */
@media (min-width: 1024px) {
    .container {
        padding: 30px;
        max-width: 1200px;
    }
}

/* 大画面 */
@media (min-width: 1440px) {
    .container {
        max-width: 1400px;
    }
}
```

**コンテナクエリ（Container Queries）**
```css
/* 親要素のサイズに応じてスタイルを変更 */
.card-container {
    container-type: inline-size;
}

.card {
    padding: 10px;
}

@container (min-width: 400px) {
    .card {
        padding: 20px;
        display: flex;
        gap: 15px;
    }
}
```

### 1.2 デザインシステムの実装

#### CSS変数（カスタムプロパティ）の活用

```css
:root {
    /* カラーパレット */
    --color-primary: #007bff;
    --color-primary-dark: #0056b3;
    --color-secondary: #6c757d;
    --color-success: #28a745;
    --color-danger: #dc3545;
    
    /* タイポグラフィ */
    --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-size-base: 16px;
    --font-size-lg: 18px;
    --font-size-sm: 14px;
    
    /* スペーシング */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    
    /* シャドウ */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    
    /* ボーダー */
    --border-radius-sm: 4px;
    --border-radius-md: 8px;
    --border-radius-lg: 12px;
}

/* ダークモード対応 */
@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: #4dabf7;
        --color-bg: #1a1a1a;
        --color-text: #ffffff;
    }
}

/* コンポーネントでの使用 */
.button {
    background-color: var(--color-primary);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-sm);
    font-size: var(--font-size-base);
}

.button:hover {
    background-color: var(--color-primary-dark);
}
```

#### BEM命名規則

```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }
.card__title { }
.card__description { }

/* Modifier */
.card--featured { }
.card--compact { }
.card__title--large { }

/* HTML構造 */
/*
<div class="card card--featured">
    <div class="card__header">
        <h2 class="card__title card__title--large">タイトル</h2>
    </div>
    <div class="card__body">
        <p class="card__description">説明文</p>
    </div>
    <div class="card__footer">
        <button class="card__button">アクション</button>
    </div>
</div>
*/
```

### 1.3 アニメーションとトランジション

**スムーズなトランジション**
```css
/* 基本的なトランジション */
.button {
    background-color: var(--color-primary);
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
    background-color: var(--color-primary-dark);
    transform: translateY(-2px);
}

.button:active {
    transform: translateY(0);
}

/* フェードインアニメーション */
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

/* スライドアニメーション */
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.slide-in {
    animation: slideIn 0.3s ease-out;
}
```

**パフォーマンスを考慮したアニメーション**
```css
/* GPU加速を活用 */
.animated-element {
    will-change: transform, opacity;
    transform: translateZ(0);  /* ハードウェア加速を強制 */
}

/* 60fpsを維持するため、transformとopacityのみを使用 */
/* 悪い例: left, top を変更（リフローが発生） */
.bad-animation {
    left: 0;
    transition: left 0.3s;
}

/* 良い例: transformを使用（コンポジションのみ） */
.good-animation {
    transform: translateX(0);
    transition: transform 0.3s;
}
```

### 1.4 CSSフレームワークの活用

#### Tailwind CSSの実践例

```html
<!-- ユーティリティファーストアプローチ -->
<div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">
            カードタイトル
        </h2>
        <p class="text-gray-600 mb-4">
            カードの説明文
        </p>
        <button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition-colors duration-200">
            アクション
        </button>
    </div>
</div>
```

**カスタムコンポーネントとの組み合わせ**
```javascript
// React + Tailwind
const Card = ({ title, description, children }) => {
    return (
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
                {title}
            </h2>
            <p className="text-gray-600 mb-4">
                {description}
            </p>
            {children}
        </div>
    );
};
```

#### Bootstrapの活用

```html
<!-- グリッドシステム -->
<div class="container">
    <div class="row">
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">カード1</h5>
                    <p class="card-text">内容</p>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">カード2</h5>
                    <p class="card-text">内容</p>
                </div>
            </div>
        </div>
    </div>
</div>
```

### 1.5 デザイン実現の実践例

**ピクセルパーフェクトな実装**

1. **デザインツールからの情報取得**
   - Figma/Adobe XDから正確なサイズ、色、スペーシングを取得
   - デザインシステムのトークンを確認

2. **ブラウザ開発者ツールの活用**
   - 要素のサイズ、マージン、パディングを正確に測定
   - カラーコードを正確に取得

3. **クロスブラウザ対応**
```css
/* ベンダープレフィックスの使用 */
.button {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    
    display: -webkit-flex;
    display: flex;
    
    -webkit-transform: translateX(0);
    transform: translateX(0);
}
```

## 2. 動的実装 - React/Next.js

### 2.1 Reactの特徴とベストプラクティス

#### コンポーネント設計

**関数コンポーネントとHooks**
```javascript
// 関数コンポーネント
import { useState, useEffect, useCallback, useMemo } from 'react';

const UserProfile = ({ userId }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // useEffect: 副作用の処理
    useEffect(() => {
        const fetchUser = async () => {
            try {
                setLoading(true);
                const response = await fetch(`/api/users/${userId}`);
                if (!response.ok) throw new Error('Failed to fetch');
                const data = await response.json();
                setUser(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [userId]);  // userIdが変更された時のみ再実行

    // useMemo: 計算結果のメモ化
    const fullName = useMemo(() => {
        if (!user) return '';
        return `${user.firstName} ${user.lastName}`;
    }, [user]);

    // useCallback: 関数のメモ化
    const handleUpdate = useCallback(async (updates) => {
        try {
            const response = await fetch(`/api/users/${userId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updates),
            });
            const data = await response.json();
            setUser(data);
        } catch (err) {
            setError(err.message);
        }
    }, [userId]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!user) return <div>User not found</div>;

    return (
        <div>
            <h1>{fullName}</h1>
            <p>{user.email}</p>
            <button onClick={() => handleUpdate({ name: 'New Name' })}>
                Update
            </button>
        </div>
    );
};
```

**カスタムHooksの作成**
```javascript
// useFetch: データ取得のロジックを再利用
const useFetch = (url) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                if (!response.ok) throw new Error('Failed to fetch');
                const data = await response.json();
                setData(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [url]);

    return { data, loading, error };
};

// 使用例
const UserList = () => {
    const { data: users, loading, error } = useFetch('/api/users');

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <ul>
            {users?.map(user => (
                <li key={user.id}>{user.name}</li>
            ))}
        </ul>
    );
};
```

#### 状態管理

**Context APIの活用**
```javascript
// UserContext.js
import { createContext, useContext, useState, useCallback } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);

    const login = useCallback(async (email, password) => {
        setLoading(true);
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            setUser(data.user);
            return data;
        } finally {
            setLoading(false);
        }
    }, []);

    const logout = useCallback(() => {
        setUser(null);
    }, []);

    return (
        <UserContext.Provider value={{ user, loading, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within UserProvider');
    }
    return context;
};

// 使用例
const LoginButton = () => {
    const { user, login, logout } = useUser();

    if (user) {
        return <button onClick={logout}>Logout</button>;
    }

    return <button onClick={() => login('user@example.com', 'password')}>Login</button>;
};
```

**Zustand/Reduxの選択基準**
```javascript
// Zustand: シンプルな状態管理
import { create } from 'zustand';

const useStore = create((set) => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
    decrement: () => set((state) => ({ count: state.count - 1 })),
}));

// 使用例
const Counter = () => {
    const { count, increment, decrement } = useStore();
    return (
        <div>
            <p>{count}</p>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    );
};
```

#### パフォーマンス最適化

**React.memoの活用**
```javascript
// 子コンポーネントのメモ化
const UserCard = React.memo(({ user, onUpdate }) => {
    return (
        <div>
            <h3>{user.name}</h3>
            <p>{user.email}</p>
            <button onClick={() => onUpdate(user.id)}>Update</button>
        </div>
    );
}, (prevProps, nextProps) => {
    // カスタム比較関数
    return prevProps.user.id === nextProps.user.id &&
           prevProps.user.name === nextProps.user.name &&
           prevProps.user.email === nextProps.user.email;
});

// 親コンポーネント
const UserList = ({ users }) => {
    const handleUpdate = useCallback((userId) => {
        // 更新処理
    }, []);

    return (
        <div>
            {users.map(user => (
                <UserCard 
                    key={user.id} 
                    user={user} 
                    onUpdate={handleUpdate}
                />
            ))}
        </div>
    );
};
```

**仮想化（Virtualization）**
```javascript
// react-window を使用したリストの仮想化
import { FixedSizeList } from 'react-window';

const VirtualizedList = ({ items }) => {
    const Row = ({ index, style }) => (
        <div style={style}>
            {items[index].name}
        </div>
    );

    return (
        <FixedSizeList
            height={600}
            itemCount={items.length}
            itemSize={50}
            width="100%"
        >
            {Row}
        </FixedSizeList>
    );
};
```

### 2.2 Next.jsの特徴と活用

#### ファイルベースルーティング

```
pages/
├── index.js          → /
├── about.js          → /about
├── blog/
│   ├── index.js      → /blog
│   └── [id].js       → /blog/:id
└── api/
    └── users/
        └── [id].js   → /api/users/:id
```

**動的ルーティング**
```javascript
// pages/blog/[id].js
import { useRouter } from 'next/router';
import { getPostById, getAllPostIds } from '../../lib/posts';

export default function Post({ post }) {
    const router = useRouter();

    if (router.isFallback) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{post.title}</h1>
            <p>{post.content}</p>
        </div>
    );
}

// 静的生成のためのパス取得
export async function getStaticPaths() {
    const paths = getAllPostIds();
    return {
        paths,
        fallback: true,  // または false, 'blocking'
    };
}

// 静的生成のためのデータ取得
export async function getStaticProps({ params }) {
    const post = await getPostById(params.id);
    return {
        props: { post },
        revalidate: 60,  // ISR: 60秒ごとに再生成
    };
}
```

#### データフェッチング戦略

**SSG (Static Site Generation)**
```javascript
// ビルド時に静的HTMLを生成
export async function getStaticProps() {
    const posts = await getAllPosts();
    return {
        props: { posts },
    };
}
```

**SSR (Server-Side Rendering)**
```javascript
// リクエストごとにサーバーでHTMLを生成
export async function getServerSideProps(context) {
    const { req, res } = context;
    const posts = await getPostsForUser(req.headers.cookie);
    return {
        props: { posts },
    };
}
```

**ISR (Incremental Static Regeneration)**
```javascript
// 静的生成 + 定期的な再生成
export async function getStaticProps() {
    const posts = await getAllPosts();
    return {
        props: { posts },
        revalidate: 3600,  // 1時間ごとに再生成
    };
}
```

#### API Routes

```javascript
// pages/api/users/[id].js
export default async function handler(req, res) {
    const { id } = req.query;

    if (req.method === 'GET') {
        const user = await getUserById(id);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        return res.status(200).json(user);
    }

    if (req.method === 'PUT') {
        const { name, email } = req.body;
        const updatedUser = await updateUser(id, { name, email });
        return res.status(200).json(updatedUser);
    }

    if (req.method === 'DELETE') {
        await deleteUser(id);
        return res.status(204).end();
    }

    res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
    return res.status(405).json({ error: 'Method not allowed' });
}
```

### 2.3 大規模開発における注意点

#### コード分割とバンドル最適化

**動的インポート**
```javascript
// コンポーネントの遅延読み込み
import dynamic from 'next/dynamic';

const HeavyComponent = dynamic(() => import('../components/HeavyComponent'), {
    loading: () => <p>Loading...</p>,
    ssr: false,  // サーバーサイドレンダリングを無効化
});

// 使用例
const Page = () => {
    return (
        <div>
            <h1>Page Content</h1>
            <HeavyComponent />
        </div>
    );
};
```

**バンドル分析**
```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
    // その他の設定
});
```

#### 型安全性（TypeScript）

```typescript
// types/user.ts
export interface User {
    id: number;
    name: string;
    email: string;
    role: 'admin' | 'user' | 'guest';
    createdAt: Date;
}

// components/UserCard.tsx
import { User } from '../types/user';

interface UserCardProps {
    user: User;
    onUpdate?: (user: User) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onUpdate }) => {
    return (
        <div>
            <h3>{user.name}</h3>
            <p>{user.email}</p>
            {onUpdate && (
                <button onClick={() => onUpdate(user)}>Update</button>
            )}
        </div>
    );
};
```

#### テスト戦略

**ユニットテスト（Jest + React Testing Library）**
```javascript
// __tests__/UserCard.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import UserCard from '../components/UserCard';

describe('UserCard', () => {
    const mockUser = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
    };

    it('renders user information', () => {
        render(<UserCard user={mockUser} />);
        expect(screen.getByText('John Doe')).toBeInTheDocument();
        expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });

    it('calls onUpdate when button is clicked', () => {
        const mockOnUpdate = jest.fn();
        render(<UserCard user={mockUser} onUpdate={mockOnUpdate} />);
        
        fireEvent.click(screen.getByText('Update'));
        expect(mockOnUpdate).toHaveBeenCalledWith(mockUser);
    });
});
```

**E2Eテスト（Playwright/Cypress）**
```javascript
// e2e/user-flow.spec.js
import { test, expect } from '@playwright/test';

test('user can login and view profile', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    
    await expect(page).toHaveURL('/profile');
    await expect(page.locator('h1')).toContainText('Profile');
});
```

#### パフォーマンス監視

**Web Vitalsの計測**
```javascript
// lib/analytics.js
export const reportWebVitals = (metric) => {
    // Google Analytics などに送信
    if (metric.label === 'web-vital') {
        gtag('event', metric.name, {
            value: Math.round(metric.value),
            event_label: metric.id,
            non_interaction: true,
        });
    }
};

// _app.js
import { reportWebVitals } from '../lib/analytics';

export function reportWebVitals(metric) {
    reportWebVitals(metric);
}
```

#### エラーハンドリング

**Error Boundary**
```javascript
// components/ErrorBoundary.js
import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // エラーログの送信
        console.error('Error caught by boundary:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div>
                    <h2>Something went wrong.</h2>
                    <button onClick={() => this.setState({ hasError: false })}>
                        Try again
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}
```

## 3. まとめ

### デザイン実現力のポイント

1. **CSS基礎**
   - Flexbox/Gridの適切な使用
   - レスポンシブデザイン
   - アニメーションとトランジション

2. **デザインシステム**
   - CSS変数の活用
   - 命名規則の統一
   - 再利用可能なコンポーネント

3. **フレームワーク活用**
   - Tailwind CSS / Bootstrap
   - デザインツールとの連携

### 動的実装のポイント

1. **React**
   - コンポーネント設計
   - Hooksの適切な使用
   - パフォーマンス最適化

2. **Next.js**
   - ルーティング戦略
   - データフェッチング
   - SSR/SSG/ISRの使い分け

3. **大規模開発**
   - コード分割
   - 型安全性
   - テスト戦略
   - パフォーマンス監視

### 面接で説明できる実践例

- 「デザイナーが作成したFigmaデザインを、CSS GridとFlexboxを組み合わせてピクセルパーフェクトに実装しました。レスポンシブ対応も含め、モバイル・タブレット・デスクトップの3ブレークポイントで動作確認を行いました。」

- 「Reactアプリケーションで、useMemoとuseCallbackを適切に使用することで、不要な再レンダリングを削減し、リスト表示のパフォーマンスを40%改善しました。」

- 「Next.jsのISRを活用して、ブログ記事の初回読み込み時間を3秒から0.5秒に短縮しました。また、動的インポートを使用してバンドルサイズを30%削減しました。」

