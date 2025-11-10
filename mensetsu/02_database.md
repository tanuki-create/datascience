# データベース - 面接対策ガイド

## 1. 素のSQLを操れるか

### 1.1 基本的なSQL操作

#### SELECT文の高度な使い方

**複雑なJOIN**
```sql
-- 3テーブル以上のJOIN
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    c.email,
    p.product_name,
    oi.quantity,
    oi.price,
    (oi.quantity * oi.price) AS line_total
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC, o.order_id;
```

**LEFT JOIN vs INNER JOIN の使い分け**
```sql
-- INNER JOIN: 両方のテーブルに存在するレコードのみ
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- LEFT JOIN: 左側のテーブルの全レコード（注文がない顧客も含む）
SELECT c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;

-- 注文がない顧客のみを取得
SELECT c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**サブクエリの活用**
```sql
-- 相関サブクエリ: 各顧客の最新注文を取得
SELECT 
    c.customer_id,
    c.customer_name,
    (
        SELECT o.order_date
        FROM orders o
        WHERE o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        LIMIT 1
    ) AS last_order_date
FROM customers c;

-- EXISTS句: 注文がある顧客のみ
SELECT c.customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.customer_id
    AND o.order_date >= '2024-01-01'
);

-- IN句: 特定の商品を含む注文
SELECT o.order_id, o.order_date
FROM orders o
WHERE o.order_id IN (
    SELECT DISTINCT order_id
    FROM order_items
    WHERE product_id IN (1, 2, 3)
);
```

### 1.2 集約関数とGROUP BY

**複雑な集約処理**
```sql
-- 月別売上集計（前年同月比も計算）
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(oi.quantity * oi.price) AS total_sales,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    COUNT(o.order_id) AS order_count,
    AVG(oi.quantity * oi.price) AS avg_order_value
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month DESC;

-- HAVING句: 集約結果でフィルタリング
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.price) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(oi.quantity * oi.price) > 10000  -- 1万円以上購入した顧客
ORDER BY total_spent DESC;
```

**ウィンドウ関数（Window Functions）**
```sql
-- ROW_NUMBER: 各顧客の注文に連番を付与
SELECT 
    customer_id,
    order_id,
    order_date,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id 
        ORDER BY order_date DESC
    ) AS order_rank
FROM orders;

-- RANK vs DENSE_RANK
SELECT 
    product_id,
    product_name,
    price,
    RANK() OVER (ORDER BY price DESC) AS rank_with_gaps,
    DENSE_RANK() OVER (ORDER BY price DESC) AS rank_without_gaps
FROM products;

-- LAG/LEAD: 前後のレコードと比較
SELECT 
    order_date,
    daily_sales,
    LAG(daily_sales, 1) OVER (ORDER BY order_date) AS previous_day_sales,
    daily_sales - LAG(daily_sales, 1) OVER (ORDER BY order_date) AS day_over_day_change
FROM (
    SELECT 
        DATE(order_date) AS order_date,
        SUM(quantity * price) AS daily_sales
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY DATE(order_date)
) daily_summary;

-- 累積合計
SELECT 
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_sales
FROM (
    SELECT 
        DATE(order_date) AS order_date,
        SUM(quantity * price) AS daily_sales
    FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY DATE(order_date)
) daily_summary;
```

### 1.3 CASE文と条件分岐

```sql
-- 複雑な条件分岐
SELECT 
    customer_id,
    customer_name,
    total_spent,
    CASE
        WHEN total_spent >= 50000 THEN 'VIP'
        WHEN total_spent >= 20000 THEN 'Gold'
        WHEN total_spent >= 10000 THEN 'Silver'
        ELSE 'Regular'
    END AS customer_tier,
    CASE
        WHEN customer_tier = 'VIP' THEN total_spent * 0.1
        WHEN customer_tier = 'Gold' THEN total_spent * 0.05
        WHEN customer_tier = 'Silver' THEN total_spent * 0.02
        ELSE 0
    END AS reward_points
FROM (
    SELECT 
        c.customer_id,
        c.customer_name,
        COALESCE(SUM(oi.quantity * oi.price), 0) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY c.customer_id, c.customer_name
) customer_summary;
```

### 1.4 複雑な要件への対応例

**例1: リピート購入率の計算**
```sql
-- 2回以上購入した顧客の割合
SELECT 
    COUNT(DISTINCT CASE WHEN order_count >= 2 THEN customer_id END) * 100.0 / 
    COUNT(DISTINCT customer_id) AS repeat_purchase_rate
FROM (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) customer_orders;
```

**例2: コホート分析**
```sql
-- 初回購入月別のコホート分析
WITH first_purchase AS (
    SELECT 
        customer_id,
        DATE_FORMAT(MIN(order_date), '%Y-%m') AS cohort_month
    FROM orders
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT 
        fp.customer_id,
        fp.cohort_month,
        DATE_FORMAT(o.order_date, '%Y-%m') AS activity_month,
        TIMESTAMPDIFF(MONTH, 
            STR_TO_DATE(CONCAT(fp.cohort_month, '-01'), '%Y-%m-%d'),
            STR_TO_DATE(CONCAT(DATE_FORMAT(o.order_date, '%Y-%m'), '-01'), '%Y-%m-%d')
        ) AS period_number
    FROM first_purchase fp
    INNER JOIN orders o ON fp.customer_id = o.customer_id
    GROUP BY fp.customer_id, fp.cohort_month, activity_month
)
SELECT 
    cohort_month,
    period_number,
    COUNT(DISTINCT customer_id) AS active_customers
FROM monthly_activity
GROUP BY cohort_month, period_number
ORDER BY cohort_month, period_number;
```

**例3: 階層データの処理（再帰CTE）**
```sql
-- 組織階層の取得（PostgreSQL/MySQL 8.0+）
WITH RECURSIVE org_hierarchy AS (
    -- 基底ケース: トップレベルの組織
    SELECT 
        org_id,
        org_name,
        parent_org_id,
        0 AS level,
        CAST(org_name AS CHAR(1000)) AS path
    FROM organizations
    WHERE parent_org_id IS NULL
    
    UNION ALL
    
    -- 再帰ケース: 子組織を追加
    SELECT 
        o.org_id,
        o.org_name,
        o.parent_org_id,
        oh.level + 1,
        CONCAT(oh.path, ' > ', o.org_name)
    FROM organizations o
    INNER JOIN org_hierarchy oh ON o.parent_org_id = oh.org_id
)
SELECT * FROM org_hierarchy ORDER BY path;
```

## 2. チューニングできるか

### 2.1 インデックスの理解

#### インデックスの種類

**B-Treeインデックス（最も一般的）**
```sql
-- 単一カラムインデックス
CREATE INDEX idx_customer_email ON customers(email);

-- 複合インデックス（複数カラム）
CREATE INDEX idx_order_customer_date ON orders(customer_id, order_date);

-- 複合インデックスの順序が重要
-- 良い例: customer_id, order_date の順
-- 悪い例: order_date, customer_id の順（customer_id単独での検索に使えない）
```

**ユニークインデックス**
```sql
CREATE UNIQUE INDEX idx_customer_email_unique ON customers(email);
```

**部分インデックス（Partial Index）**
```sql
-- アクティブな注文のみにインデックスを作成
CREATE INDEX idx_active_orders ON orders(order_date)
WHERE status = 'active';
```

**カバリングインデックス（Covering Index）**
```sql
-- クエリで必要な全カラムを含むインデックス
-- SELECT customer_id, email, name を実行する場合
CREATE INDEX idx_customer_covering ON customers(customer_id, email, name);
-- インデックスだけでクエリが完結（テーブルアクセス不要）
```

#### インデックスの効果的な使い方

**EXPLAINで実行計画を確認**
```sql
-- クエリの実行計画を確認
EXPLAIN SELECT * FROM orders 
WHERE customer_id = 123 AND order_date >= '2024-01-01';

-- 出力例:
-- id | select_type | table  | type  | possible_keys              | key                        | rows | Extra
-- 1  | SIMPLE      | orders | ref   | idx_order_customer_date    | idx_order_customer_date    | 50   | Using where
```

**インデックスが使われないケース**

1. **関数を適用したカラム**
```sql
-- 悪い例: インデックスが使われない
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024;

-- 良い例: インデックスが使われる
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

2. **LIKE '%...' パターン**
```sql
-- 悪い例: インデックスが使われない
SELECT * FROM customers 
WHERE email LIKE '%@example.com';

-- 良い例: 前方一致ならインデックスが使われる
SELECT * FROM customers 
WHERE email LIKE 'user%@example.com';
```

3. **NULL値の比較**
```sql
-- 悪い例
SELECT * FROM orders WHERE status = NULL;

-- 良い例
SELECT * FROM orders WHERE status IS NULL;
```

### 2.2 クエリの最適化

#### N+1問題の解決

**問題のあるコード（アプリケーション側）**
```python
# N+1問題: 各注文ごとに顧客情報を取得
orders = Order.objects.all()
for order in orders:
    print(order.customer.name)  # 各ループでDBクエリが実行される
```

**解決策1: JOINを使用**
```sql
-- 1回のクエリで全データを取得
SELECT 
    o.order_id,
    o.order_date,
    c.customer_name,
    c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```

**解決策2: IN句を使用（アプリケーション側）**
```python
# 事前に必要なIDを取得
order_ids = [order.id for order in orders]
customers = Customer.objects.filter(order__id__in=order_ids)
# メモリ上で結合
```

#### サブクエリの最適化

**相関サブクエリをJOINに変換**
```sql
-- 悪い例: 相関サブクエリ（各行でサブクエリが実行される）
SELECT 
    c.customer_id,
    c.customer_name,
    (
        SELECT COUNT(*)
        FROM orders o
        WHERE o.customer_id = c.customer_id
    ) AS order_count
FROM customers c;

-- 良い例: JOIN + GROUP BY（1回のスキャンで完了）
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

#### LIMITとOFFSETの最適化

**OFFSETのパフォーマンス問題**
```sql
-- 悪い例: OFFSETが大きいと遅い
SELECT * FROM orders 
ORDER BY order_date DESC 
LIMIT 20 OFFSET 10000;  -- 最初の10000件をスキップする必要がある

-- 良い例: カーソルベースのページネーション
SELECT * FROM orders 
WHERE order_id < :last_seen_id
ORDER BY order_date DESC 
LIMIT 20;
```

### 2.3 パーティショニング

**範囲パーティショニング（Range Partitioning）**
```sql
-- 注文テーブルを月単位でパーティション分割
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10, 2)
) PARTITION BY RANGE (YEAR(order_date) * 100 + MONTH(order_date)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    -- ...
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- 特定の月のデータのみをスキャン
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
-- → p202401パーティションのみをスキャン
```

**ハッシュパーティショニング**
```sql
-- 顧客IDでハッシュパーティション
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE
) PARTITION BY HASH(customer_id) PARTITIONS 4;
```

## 3. SQLの実装能力 - 複雑な要件への対応

### 3.1 複雑なビジネスロジックの実装

**例1: 在庫管理システム**
```sql
-- 在庫の引当処理（楽観的ロック）
UPDATE inventory
SET 
    available_quantity = available_quantity - :requested_quantity,
    reserved_quantity = reserved_quantity + :requested_quantity,
    version = version + 1
WHERE 
    product_id = :product_id
    AND available_quantity >= :requested_quantity
    AND version = :current_version;  -- 楽観的ロック

-- 更新された行数で成功/失敗を判定
-- affected_rows = 1 → 成功
-- affected_rows = 0 → 失敗（在庫不足または競合）
```

**例2: ランキング機能**
```sql
-- 商品の売上ランキング（カテゴリ別）
SELECT 
    p.product_id,
    p.product_name,
    p.category_id,
    SUM(oi.quantity * oi.price) AS total_sales,
    RANK() OVER (
        PARTITION BY p.category_id 
        ORDER BY SUM(oi.quantity * oi.price) DESC
    ) AS category_rank
FROM products p
INNER JOIN order_items oi ON p.product_id = oi.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY p.product_id, p.product_name, p.category_id
HAVING category_rank <= 10;  -- カテゴリごとのトップ10
```

**例3: 複雑な集計（ピボットテーブル風）**
```sql
-- 月別・カテゴリ別の売上集計
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(CASE WHEN p.category_id = 1 THEN oi.quantity * oi.price ELSE 0 END) AS category1_sales,
    SUM(CASE WHEN p.category_id = 2 THEN oi.quantity * oi.price ELSE 0 END) AS category2_sales,
    SUM(CASE WHEN p.category_id = 3 THEN oi.quantity * oi.price ELSE 0 END) AS category3_sales,
    SUM(oi.quantity * oi.price) AS total_sales
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month DESC;
```

### 3.2 トランザクション管理

**ACID特性の理解**

```sql
-- トランザクションの例: 注文処理
START TRANSACTION;

-- 1. 在庫チェックと更新
UPDATE inventory 
SET available_quantity = available_quantity - :quantity
WHERE product_id = :product_id 
AND available_quantity >= :quantity;

-- 2. 注文作成
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES (:customer_id, NOW(), :total_amount);

SET @order_id = LAST_INSERT_ID();

-- 3. 注文明細作成
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES (@order_id, :product_id, :quantity, :price);

-- 4. 決済処理
INSERT INTO payments (order_id, amount, payment_method)
VALUES (@order_id, :total_amount, :payment_method);

-- すべて成功した場合のみコミット
COMMIT;

-- エラーが発生した場合はロールバック
-- ROLLBACK;
```

**デッドロックの回避**

```sql
-- デッドロックを避けるため、常に同じ順序でロックを取得
-- 例: 常に customer_id の昇順でロック

-- トランザクション1
START TRANSACTION;
SELECT * FROM customers WHERE customer_id IN (1, 2) ORDER BY customer_id FOR UPDATE;
-- 処理...

-- トランザクション2（同じ順序でロック）
START TRANSACTION;
SELECT * FROM customers WHERE customer_id IN (2, 1) ORDER BY customer_id FOR UPDATE;
-- 処理...
```

### 3.3 データ整合性の保証

**制約の活用**
```sql
-- 外部キー制約
ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
ON DELETE RESTRICT  -- 顧客が存在する注文は削除不可
ON UPDATE CASCADE;  -- 顧客IDが変更されたら連動して更新

-- チェック制約
ALTER TABLE orders
ADD CONSTRAINT chk_order_amount
CHECK (total_amount > 0);

-- ユニーク制約
ALTER TABLE customers
ADD CONSTRAINT uk_customer_email
UNIQUE (email);
```

**トリガーの使用例**
```sql
-- 注文作成時に在庫を自動更新
DELIMITER //
CREATE TRIGGER trg_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE inventory
    SET available_quantity = available_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END//
DELIMITER ;
```

## 4. パフォーマンス改善

### 4.1 クエリパフォーマンスの分析

**スロークエリログの活用**
```sql
-- MySQL: スロークエリログを有効化
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- 1秒以上かかるクエリを記録

-- スロークエリの確認
SELECT * FROM mysql.slow_log 
ORDER BY start_time DESC 
LIMIT 10;
```

**EXPLAIN ANALYZE（PostgreSQL）**
```sql
-- 実際の実行時間も含めて分析
EXPLAIN ANALYZE
SELECT * FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= '2024-01-01';
```

### 4.2 インデックス戦略

**複合インデックスの設計原則**

1. **カーディナリティの高いカラムを先に**
```sql
-- 良い例: customer_id（高カーディナリティ）を先に
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- 悪い例: order_date（低カーディナリティ）を先に
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id);
```

2. **WHERE句で使われるカラムを優先**
```sql
-- このクエリに対して
SELECT * FROM orders 
WHERE customer_id = 123 
AND status = 'completed'
ORDER BY order_date DESC;

-- 最適なインデックス
CREATE INDEX idx_orders_customer_status_date 
ON orders(customer_id, status, order_date DESC);
```

3. **カバリングインデックスの活用**
```sql
-- SELECT句の全カラムを含むインデックス
CREATE INDEX idx_orders_covering 
ON orders(customer_id, order_date, total_amount, status);
-- テーブルアクセス不要でクエリが完結
```

### 4.3 データベース設計の最適化

**正規化と非正規化のバランス**

**正規化のメリット**
- データの重複を排除
- 更新の一貫性を保証
- ストレージ効率が良い

**非正規化のメリット**
- クエリパフォーマンスの向上
- JOINの削減

**実践例: 読み取り専用カラムの非正規化**
```sql
-- 注文テーブルに顧客名を非正規化（読み取り専用）
ALTER TABLE orders
ADD COLUMN customer_name VARCHAR(100);

-- 注文作成時に顧客名をコピー
INSERT INTO orders (customer_id, customer_name, order_date, total_amount)
SELECT 
    :customer_id,
    c.customer_name,  -- 非正規化
    NOW(),
    :total_amount
FROM customers c
WHERE c.customer_id = :customer_id;

-- クエリが高速化（JOIN不要）
SELECT order_id, customer_name, order_date, total_amount
FROM orders
WHERE order_date >= '2024-01-01';
```

### 4.4 キャッシュ戦略

**クエリ結果のキャッシュ**
```sql
-- MySQL: クエリキャッシュ（MySQL 8.0以前）
SET GLOBAL query_cache_size = 67108864;  -- 64MB

-- アプリケーション側でのキャッシュ
-- Redis等を使用して頻繁にアクセスされるデータをキャッシュ
```

**マテリアライズドビュー（物化ビュー）**
```sql
-- PostgreSQL: マテリアライズドビュー
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    SUM(total_amount) AS total_sales,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- 定期的にリフレッシュ
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- 高速な集計クエリ
SELECT * FROM monthly_sales_summary 
WHERE month >= '2024-01-01';
```

### 4.5 接続プールとリソース管理

**接続プールの設定**
```python
# Python (SQLAlchemy) での接続プール設定
from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://user:password@localhost/db',
    pool_size=10,           # プールサイズ
    max_overflow=20,        # 最大オーバーフロー
    pool_timeout=30,        # 接続取得のタイムアウト
    pool_recycle=3600,      # 1時間で接続を再生成
    pool_pre_ping=True      # 接続の有効性をチェック
)
```

**長時間実行クエリの対策**
```sql
-- クエリタイムアウトの設定
SET SESSION max_execution_time = 30000;  -- 30秒

-- バッチ処理での分割
-- 大量データを一度に処理せず、小さなバッチに分割
SELECT * FROM orders 
WHERE order_date >= '2024-01-01'
LIMIT 1000 OFFSET 0;

-- 次のバッチ
SELECT * FROM orders 
WHERE order_date >= '2024-01-01'
LIMIT 1000 OFFSET 1000;
```

## 5. 実践的な最適化例

### 5.1 パフォーマンス改善の実例

**Before: 遅いクエリ**
```sql
-- 実行時間: 5秒
SELECT 
    c.customer_id,
    c.customer_name,
    (
        SELECT COUNT(*)
        FROM orders o
        WHERE o.customer_id = c.customer_id
    ) AS order_count,
    (
        SELECT SUM(total_amount)
        FROM orders o
        WHERE o.customer_id = c.customer_id
    ) AS total_spent
FROM customers c
WHERE c.created_at >= '2024-01-01';
```

**After: 最適化されたクエリ**
```sql
-- 実行時間: 0.2秒（25倍高速化）

-- 1. インデックス追加
CREATE INDEX idx_orders_customer_created 
ON orders(customer_id, created_at);

CREATE INDEX idx_customers_created 
ON customers(created_at);

-- 2. JOIN + GROUP BY に変更
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE c.created_at >= '2024-01-01'
GROUP BY c.customer_id, c.customer_name;
```

### 5.2 モニタリングと分析

**パフォーマンスメトリクスの監視**

1. **クエリ実行時間**
2. **スロークエリの数**
3. **インデックス使用率**
4. **テーブルスキャンの発生率**
5. **デッドロックの発生数**
6. **接続プールの使用率**

**定期的な分析クエリ**
```sql
-- 使用されていないインデックスの検出
SELECT 
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    s.INDEX_NAME,
    s.CARDINALITY
FROM information_schema.TABLES t
INNER JOIN information_schema.STATISTICS s 
    ON t.TABLE_SCHEMA = s.TABLE_SCHEMA 
    AND t.TABLE_NAME = s.TABLE_NAME
LEFT JOIN information_schema.INDEX_STATISTICS i
    ON s.TABLE_SCHEMA = i.TABLE_SCHEMA
    AND s.TABLE_NAME = i.TABLE_NAME
    AND s.INDEX_NAME = i.INDEX_NAME
WHERE i.INDEX_NAME IS NULL  -- 使用されていない
AND t.TABLE_SCHEMA = 'your_database';
```

## 6. まとめ

### SQL実装能力のポイント

1. **基本的なSQL操作**
   - 複雑なJOIN
   - サブクエリとウィンドウ関数
   - 集約関数の活用

2. **パフォーマンス最適化**
   - 適切なインデックスの設計
   - クエリの最適化
   - 実行計画の理解

3. **複雑な要件への対応**
   - ビジネスロジックのSQL実装
   - トランザクション管理
   - データ整合性の保証

### 面接で説明できる実践例

- 「ECサイトの注文履歴画面で、N+1問題によりページ読み込みに5秒かかっていました。JOINを使用して1回のクエリに集約した結果、0.3秒に短縮しました。」

- 「月次レポートの生成に10分かかっていたため、マテリアライズドビューを導入し、事前集計を行うようにしました。これにより、レポート生成時間を10秒に短縮しました。」

- 「複合インデックスの順序を見直し、カバリングインデックスを活用することで、商品一覧画面のクエリを50%高速化しました。」

