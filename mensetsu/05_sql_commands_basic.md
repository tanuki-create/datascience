# よく使われるSQLコマンド - 基本から丁寧に

## 目次

1. [SQLの基本概念](#1-sqlの基本概念)
2. [データの取得（SELECT）](#2-データの取得select)
3. [データの絞り込み（WHERE）](#3-データの絞り込みwhere)
4. [データの並び替え（ORDER BY）](#4-データの並び替えorder-by)
5. [データの集計（GROUP BY, 集約関数）](#5-データの集計group-by-集約関数)
6. [テーブルの結合（JOIN）](#6-テーブルの結合join)
7. [データの挿入（INSERT）](#7-データの挿入insert)
8. [データの更新（UPDATE）](#8-データの更新update)
9. [データの削除（DELETE）](#9-データの削除delete)
10. [テーブルの作成と管理（CREATE, ALTER, DROP）](#10-テーブルの作成と管理create-alter-drop)
11. [サブクエリ](#11-サブクエリ)
12. [よく使われる関数](#12-よく使われる関数)

---

## 1. SQLの基本概念

### SQLとは

**SQL（Structured Query Language）** は、リレーショナルデータベースを操作するための標準的な言語です。

### 主なSQLコマンドの分類

1. **DQL（Data Query Language）**: データの取得
   - `SELECT`

2. **DML（Data Manipulation Language）**: データの操作
   - `INSERT`, `UPDATE`, `DELETE`

3. **DDL（Data Definition Language）**: データベース構造の定義
   - `CREATE`, `ALTER`, `DROP`

4. **DCL（Data Control Language）**: アクセス制御
   - `GRANT`, `REVOKE`

### 基本的な構文のルール

- SQL文はセミコロン（`;`）で終わる
- 大文字・小文字は区別されない（ただし、可読性のため大文字を使うことが多い）
- 文字列はシングルクォート（`'`）で囲む
- コメントは `--` または `/* */` を使用

---

## 2. データの取得（SELECT）

### 2.1 基本的なSELECT文

**すべてのカラムを取得**
```sql
SELECT * FROM users;
```
- `*` は「すべてのカラム」を意味する
- `FROM users` は `users` テーブルからデータを取得

**特定のカラムを取得**
```sql
SELECT id, name, email FROM users;
```
- カラム名をカンマ区切りで指定
- 必要なカラムのみ取得することで、パフォーマンスが向上

**カラムに別名を付ける（AS）**
```sql
SELECT 
    id AS user_id,
    name AS user_name,
    email AS user_email
FROM users;
```
- `AS` キーワードでカラムに別名を付けることができる
- `AS` は省略可能（`id user_id` でも可）

### 2.2 重複を除外（DISTINCT）

**重複する値を除外**
```sql
SELECT DISTINCT country FROM users;
```
- 同じ値の行を1つにまとめる
- 例: ユーザーの出身国を重複なく取得

**複数カラムでの重複除外**
```sql
SELECT DISTINCT country, city FROM users;
```
- 複数カラムの組み合わせで重複を判定

### 2.3 取得件数の制限（LIMIT）

**最初のN件を取得**
```sql
SELECT * FROM users LIMIT 10;
```
- 最初の10件のみ取得
- 大量データがある場合に便利

**OFFSETと組み合わせる**
```sql
SELECT * FROM users LIMIT 10 OFFSET 20;
```
- `OFFSET 20` で20件スキップしてから、`LIMIT 10` で10件取得
- ページネーションで使用（2ページ目を取得）

**簡潔な書き方（MySQL）**
```sql
SELECT * FROM users LIMIT 20, 10;
```
- `LIMIT offset, count` の形式
- 上記と同じ意味（20件スキップ、10件取得）

---

## 3. データの絞り込み（WHERE）

### 3.1 基本的なWHERE句

**等価条件（=）**
```sql
SELECT * FROM users WHERE id = 1;
```
- `id` が `1` の行のみ取得

**不等号（<, >, <=, >=）**
```sql
SELECT * FROM products WHERE price > 1000;
SELECT * FROM products WHERE price >= 1000;
SELECT * FROM products WHERE price < 5000;
SELECT * FROM products WHERE price <= 5000;
```

**不等価（!= または <>）**
```sql
SELECT * FROM users WHERE status != 'inactive';
SELECT * FROM users WHERE status <> 'inactive';
```
- `!=` と `<>` は同じ意味

### 3.2 複数条件の組み合わせ

**AND（かつ）**
```sql
SELECT * FROM users 
WHERE age >= 18 AND country = 'Japan';
```
- 両方の条件を満たす行を取得

**OR（または）**
```sql
SELECT * FROM users 
WHERE country = 'Japan' OR country = 'USA';
```
- どちらかの条件を満たす行を取得

**NOT（否定）**
```sql
SELECT * FROM users 
WHERE NOT status = 'inactive';
```
- 条件を否定

**複雑な条件の組み合わせ**
```sql
SELECT * FROM users 
WHERE (age >= 18 AND country = 'Japan') 
   OR (age >= 21 AND country = 'USA');
```
- 括弧で条件をグループ化

### 3.3 範囲指定（BETWEEN）

**範囲で指定**
```sql
SELECT * FROM products 
WHERE price BETWEEN 1000 AND 5000;
```
- `price` が 1000 以上 5000 以下
- `WHERE price >= 1000 AND price <= 5000` と同じ意味

**日付の範囲指定**
```sql
SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
```

### 3.4 リスト指定（IN）

**指定した値のいずれかに一致**
```sql
SELECT * FROM users 
WHERE country IN ('Japan', 'USA', 'UK');
```
- `country` が 'Japan', 'USA', 'UK' のいずれか
- `WHERE country = 'Japan' OR country = 'USA' OR country = 'UK'` と同じ意味

**NOT IN（指定した値以外）**
```sql
SELECT * FROM users 
WHERE country NOT IN ('Japan', 'USA');
```

### 3.5 パターンマッチング（LIKE）

**前方一致**
```sql
SELECT * FROM users 
WHERE email LIKE 'user%@example.com';
```
- `%` は任意の文字列を表す
- `user` で始まり、`@example.com` で終わるメールアドレス

**後方一致**
```sql
SELECT * FROM products 
WHERE name LIKE '%商品';
```

**部分一致**
```sql
SELECT * FROM products 
WHERE name LIKE '%ノート%';
```
- 名前に「ノート」が含まれる商品

**1文字のマッチング（_）**
```sql
SELECT * FROM users 
WHERE name LIKE '山田_';
```
- `_` は任意の1文字を表す
- 「山田」で始まる3文字の名前

**エスケープ文字**
```sql
SELECT * FROM products 
WHERE name LIKE '%\_%' ESCAPE '\';
```
- `%` や `_` 自体を検索する場合

### 3.6 NULL値の検索

**NULL値の検索**
```sql
SELECT * FROM users WHERE email IS NULL;
SELECT * FROM users WHERE email IS NOT NULL;
```
- `=` や `!=` では NULL を検索できない
- `IS NULL` または `IS NOT NULL` を使用

---

## 4. データの並び替え（ORDER BY）

### 4.1 基本的な並び替え

**昇順（ASC）**
```sql
SELECT * FROM users ORDER BY name ASC;
SELECT * FROM users ORDER BY name;
```
- `ASC` は省略可能（デフォルトで昇順）
- アルファベット順、数値の小さい順

**降順（DESC）**
```sql
SELECT * FROM products ORDER BY price DESC;
```
- 数値の大きい順、日付の新しい順

### 4.2 複数カラムでの並び替え

**複数カラムで並び替え**
```sql
SELECT * FROM users 
ORDER BY country ASC, name ASC;
```
- まず `country` で並び替え、同じ値の場合は `name` で並び替え

**異なる順序の組み合わせ**
```sql
SELECT * FROM products 
ORDER BY category ASC, price DESC;
```
- `category` は昇順、`price` は降順

### 4.3 よくある使用例

**最新のデータを取得**
```sql
SELECT * FROM orders 
ORDER BY created_at DESC 
LIMIT 10;
```

**価格が安い順**
```sql
SELECT * FROM products 
WHERE category = 'Electronics' 
ORDER BY price ASC;
```

---

## 5. データの集計（GROUP BY, 集約関数）

### 5.1 集約関数の基本

**COUNT（件数を数える）**
```sql
SELECT COUNT(*) FROM users;
```
- 全行の数を取得

```sql
SELECT COUNT(*) FROM users WHERE country = 'Japan';
```
- 条件に一致する行の数を取得

```sql
SELECT COUNT(DISTINCT country) FROM users;
```
- 重複を除外してカウント

**SUM（合計）**
```sql
SELECT SUM(price) FROM order_items;
```
- `price` カラムの合計を計算

**AVG（平均）**
```sql
SELECT AVG(price) FROM products;
```
- `price` カラムの平均を計算

**MAX（最大値）**
```sql
SELECT MAX(price) FROM products;
```

**MIN（最小値）**
```sql
SELECT MIN(price) FROM products;
```

### 5.2 GROUP BY（グループ化）

**基本的なGROUP BY**
```sql
SELECT country, COUNT(*) AS user_count 
FROM users 
GROUP BY country;
```
- `country` ごとにグループ化して、各グループの件数を取得

**複数カラムでグループ化**
```sql
SELECT country, city, COUNT(*) AS user_count 
FROM users 
GROUP BY country, city;
```

**集約関数と組み合わせ**
```sql
SELECT 
    category,
    COUNT(*) AS product_count,
    AVG(price) AS avg_price,
    MAX(price) AS max_price,
    MIN(price) AS min_price
FROM products 
GROUP BY category;
```

### 5.3 HAVING（集約結果の絞り込み）

**WHEREとの違い**
- `WHERE`: グループ化の前に条件を適用
- `HAVING`: グループ化の後に条件を適用

**HAVINGの使用例**
```sql
SELECT 
    country,
    COUNT(*) AS user_count
FROM users 
GROUP BY country
HAVING COUNT(*) >= 10;
```
- ユーザー数が10人以上の国のみ取得

**WHEREとHAVINGの組み合わせ**
```sql
SELECT 
    category,
    AVG(price) AS avg_price
FROM products 
WHERE price > 100  -- グループ化前にフィルタ
GROUP BY category
HAVING AVG(price) > 1000;  -- グループ化後にフィルタ
```

### 5.4 よくある集計パターン

**日付ごとの集計**
```sql
SELECT 
    DATE(order_date) AS order_day,
    COUNT(*) AS order_count,
    SUM(total_amount) AS daily_sales
FROM orders 
GROUP BY DATE(order_date)
ORDER BY order_day DESC;
```

**月ごとの集計**
```sql
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_sales
FROM orders 
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;
```

---

## 6. テーブルの結合（JOIN）

### 6.1 内部結合（INNER JOIN）

**基本的なINNER JOIN**
```sql
SELECT 
    users.name,
    orders.order_date,
    orders.total_amount
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```
- 両方のテーブルに存在するデータのみ取得
- `users.id` と `orders.user_id` が一致する行を結合

**複数テーブルの結合**
```sql
SELECT 
    users.name,
    products.name AS product_name,
    order_items.quantity,
    order_items.price
FROM users
INNER JOIN orders ON users.id = orders.user_id
INNER JOIN order_items ON orders.id = order_items.order_id
INNER JOIN products ON order_items.product_id = products.id;
```

**WHERE句での結合（古い書き方）**
```sql
SELECT 
    users.name,
    orders.order_date
FROM users, orders
WHERE users.id = orders.user_id;
```
- 古い書き方だが、INNER JOINと同じ結果
- 可読性のため、明示的なJOIN構文を推奨

### 6.2 外部結合（LEFT JOIN, RIGHT JOIN）

**LEFT JOIN（左外部結合）**
```sql
SELECT 
    users.name,
    orders.order_date
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```
- 左側（`users`）の全データを取得
- 右側（`orders`）に一致するデータがない場合は NULL

**注文がないユーザーを取得**
```sql
SELECT 
    users.name
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
```

**RIGHT JOIN（右外部結合）**
```sql
SELECT 
    users.name,
    orders.order_date
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;
```
- 右側（`orders`）の全データを取得
- 左側（`users`）に一致するデータがない場合は NULL
- LEFT JOINで書き換え可能なため、使用頻度は低い

**FULL OUTER JOIN（完全外部結合）**
```sql
SELECT 
    users.name,
    orders.order_date
FROM users
FULL OUTER JOIN orders ON users.id = orders.user_id;
```
- 両方のテーブルの全データを取得
- MySQLでは非対応（UNIONで実現可能）

### 6.3 自己結合（SELF JOIN）

**同じテーブルを結合**
```sql
SELECT 
    e1.name AS employee_name,
    e2.name AS manager_name
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```
- 同じテーブルを異なるエイリアス（`e1`, `e2`）で結合
- 組織階層の表現などで使用

---

## 7. データの挿入（INSERT）

### 7.1 基本的なINSERT

**単一行の挿入**
```sql
INSERT INTO users (name, email, age) 
VALUES ('山田太郎', 'yamada@example.com', 30);
```
- カラム名を指定して値を挿入

**すべてのカラムに値を挿入**
```sql
INSERT INTO users 
VALUES (1, '山田太郎', 'yamada@example.com', 30);
```
- カラム名を省略（すべてのカラムに順番に値を指定）
- テーブル構造が変更されるとエラーになるため、非推奨

**複数行の挿入**
```sql
INSERT INTO users (name, email, age) 
VALUES 
    ('山田太郎', 'yamada@example.com', 30),
    ('佐藤花子', 'sato@example.com', 25),
    ('鈴木一郎', 'suzuki@example.com', 35);
```

### 7.2 SELECT結果の挿入

**SELECT結果を挿入**
```sql
INSERT INTO user_backup (name, email, age)
SELECT name, email, age 
FROM users 
WHERE created_at < '2020-01-01';
```
- 既存テーブルからデータをコピー

### 7.3 デフォルト値の使用

**デフォルト値を使用**
```sql
INSERT INTO users (name, email) 
VALUES ('山田太郎', 'yamada@example.com');
```
- `age` カラムにデフォルト値が設定されている場合、自動的に使用される

**明示的にデフォルト値を指定**
```sql
INSERT INTO users (name, email, age) 
VALUES ('山田太郎', 'yamada@example.com', DEFAULT);
```

---

## 8. データの更新（UPDATE）

### 8.1 基本的なUPDATE

**単一カラムの更新**
```sql
UPDATE users 
SET email = 'newemail@example.com' 
WHERE id = 1;
```
- **重要**: WHERE句を忘れないこと（全行が更新される危険性）

**複数カラムの更新**
```sql
UPDATE users 
SET 
    name = '山田花子',
    email = 'yamada@example.com',
    age = 31
WHERE id = 1;
```

### 8.2 条件に基づく更新

**条件に一致する複数行を更新**
```sql
UPDATE products 
SET price = price * 1.1 
WHERE category = 'Electronics';
```
- 電子製品の価格を10%値上げ

**複数条件での更新**
```sql
UPDATE users 
SET status = 'inactive' 
WHERE last_login_date < '2023-01-01' 
  AND status = 'active';
```

### 8.3 JOINを使った更新

**結合したテーブルを更新**
```sql
UPDATE orders o
INNER JOIN users u ON o.user_id = u.id
SET o.status = 'cancelled'
WHERE u.status = 'inactive';
```

### 8.4 よくある注意点

**WHERE句の確認**
```sql
-- 危険な例（全行が更新される）
UPDATE users SET status = 'inactive';

-- 安全な例
UPDATE users SET status = 'inactive' WHERE id = 1;
```

**トランザクションでの実行**
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
COMMIT;  -- 成功時
-- ROLLBACK;  -- 失敗時
```

---

## 9. データの削除（DELETE）

### 9.1 基本的なDELETE

**条件に一致する行を削除**
```sql
DELETE FROM users WHERE id = 1;
```
- **重要**: WHERE句を忘れないこと（全行が削除される危険性）

**複数条件での削除**
```sql
DELETE FROM orders 
WHERE status = 'cancelled' 
  AND created_at < '2020-01-01';
```

### 9.2 全データの削除

**全データを削除**
```sql
DELETE FROM users;
```
- テーブル構造は残る
- より高速な方法: `TRUNCATE TABLE users;`

**TRUNCATEとの違い**
```sql
TRUNCATE TABLE users;
```
- `DELETE` より高速
- ロールバックできない場合がある（DBMSによる）
- 外部キー制約がある場合は使用できない場合がある

### 9.3 JOINを使った削除

**結合したテーブルから削除**
```sql
DELETE o FROM orders o
INNER JOIN users u ON o.user_id = u.id
WHERE u.status = 'inactive';
```

### 9.4 よくある注意点

**WHERE句の確認**
```sql
-- 危険な例（全行が削除される）
DELETE FROM users;

-- 安全な例
DELETE FROM users WHERE id = 1;
```

**削除前の確認**
```sql
-- 削除前に確認
SELECT * FROM users WHERE id = 1;

-- 削除実行
DELETE FROM users WHERE id = 1;
```

---

## 10. テーブルの作成と管理（CREATE, ALTER, DROP）

### 10.1 テーブルの作成（CREATE TABLE）

**基本的なテーブル作成**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**データ型の例**
- `INT`: 整数
- `VARCHAR(n)`: 可変長文字列（最大n文字）
- `CHAR(n)`: 固定長文字列（n文字）
- `TEXT`: 長い文字列
- `DATE`: 日付
- `DATETIME`: 日時
- `TIMESTAMP`: タイムスタンプ
- `DECIMAL(p, s)`: 固定小数点（p: 精度, s: スケール）
- `BOOLEAN`: 真偽値

**制約の種類**
- `PRIMARY KEY`: 主キー（一意で非NULL）
- `UNIQUE`: 一意制約
- `NOT NULL`: NULL値を許可しない
- `DEFAULT`: デフォルト値
- `AUTO_INCREMENT`: 自動増分（MySQL）
- `FOREIGN KEY`: 外部キー

**外部キー制約の例**
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 10.2 テーブルの変更（ALTER TABLE）

**カラムの追加**
```sql
ALTER TABLE users 
ADD COLUMN phone VARCHAR(20);
```

**カラムの削除**
```sql
ALTER TABLE users 
DROP COLUMN phone;
```

**カラムの変更**
```sql
ALTER TABLE users 
MODIFY COLUMN email VARCHAR(200);
```

**カラム名の変更**
```sql
ALTER TABLE users 
CHANGE COLUMN old_name new_name VARCHAR(100);
```

**インデックスの追加**
```sql
ALTER TABLE users 
ADD INDEX idx_email (email);
```

**インデックスの削除**
```sql
ALTER TABLE users 
DROP INDEX idx_email;
```

### 10.3 テーブルの削除（DROP TABLE）

**テーブルの削除**
```sql
DROP TABLE users;
```
- **注意**: テーブルとデータが完全に削除される
- 外部キー制約がある場合は削除できない場合がある

**存在する場合のみ削除**
```sql
DROP TABLE IF EXISTS users;
```

---

## 11. サブクエリ

### 11.1 スカラーサブクエリ

**単一値を返すサブクエリ**
```sql
SELECT 
    name,
    (SELECT COUNT(*) FROM orders WHERE user_id = users.id) AS order_count
FROM users;
```
- サブクエリが1行1列の値を返す
- 各ユーザーの注文数を取得

### 11.2 相関サブクエリ

**外部クエリの値を参照**
```sql
SELECT 
    name,
    (SELECT MAX(order_date) 
     FROM orders 
     WHERE user_id = users.id) AS last_order_date
FROM users;
```
- サブクエリ内で外部クエリの `users.id` を参照

### 11.3 IN句でのサブクエリ

**IN句で使用**
```sql
SELECT * FROM users 
WHERE id IN (
    SELECT DISTINCT user_id 
    FROM orders 
    WHERE order_date >= '2024-01-01'
);
```
- 2024年以降に注文したユーザーを取得

**NOT IN句で使用**
```sql
SELECT * FROM users 
WHERE id NOT IN (
    SELECT DISTINCT user_id 
    FROM orders
);
```
- 注文がないユーザーを取得

### 11.4 EXISTS句でのサブクエリ

**EXISTS句で使用**
```sql
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.id 
      AND o.order_date >= '2024-01-01'
);
```
- 2024年以降に注文したユーザーを取得
- `IN` より高速な場合が多い

**NOT EXISTS句で使用**
```sql
SELECT * FROM users u
WHERE NOT EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.id
);
```
- 注文がないユーザーを取得

### 11.5 FROM句でのサブクエリ

**FROM句で使用（派生テーブル）**
```sql
SELECT 
    country,
    AVG(user_count) AS avg_users_per_city
FROM (
    SELECT 
        country,
        city,
        COUNT(*) AS user_count
    FROM users
    GROUP BY country, city
) city_stats
GROUP BY country;
```

---

## 12. よく使われる関数

### 12.1 文字列関数

**CONCAT（文字列の結合）**
```sql
SELECT CONCAT(first_name, ' ', last_name) AS full_name 
FROM users;
```

**SUBSTRING（部分文字列の取得）**
```sql
SELECT SUBSTRING(email, 1, 5) AS email_prefix 
FROM users;
```

**UPPER / LOWER（大文字・小文字変換）**
```sql
SELECT UPPER(name) AS name_upper 
FROM users;

SELECT LOWER(email) AS email_lower 
FROM users;
```

**TRIM（前後の空白を削除）**
```sql
SELECT TRIM(name) AS trimmed_name 
FROM users;
```

**LENGTH（文字列の長さ）**
```sql
SELECT name, LENGTH(name) AS name_length 
FROM users;
```

### 12.2 数値関数

**ROUND（四捨五入）**
```sql
SELECT ROUND(price, 2) AS rounded_price 
FROM products;
```

**CEIL / FLOOR（切り上げ・切り捨て）**
```sql
SELECT CEIL(price) AS ceil_price 
FROM products;

SELECT FLOOR(price) AS floor_price 
FROM products;
```

**ABS（絶対値）**
```sql
SELECT ABS(balance) AS abs_balance 
FROM accounts;
```

### 12.3 日付関数

**NOW / CURRENT_TIMESTAMP（現在の日時）**
```sql
SELECT NOW() AS current_datetime;
SELECT CURRENT_TIMESTAMP AS current_timestamp;
```

**DATE（日付部分を取得）**
```sql
SELECT DATE(created_at) AS created_date 
FROM orders;
```

**YEAR / MONTH / DAY（年・月・日を取得）**
```sql
SELECT 
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    DAY(order_date) AS order_day
FROM orders;
```

**DATE_FORMAT（日付のフォーマット）**
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m-%d') AS formatted_date 
FROM orders;

SELECT DATE_FORMAT(order_date, '%Y年%m月%d日') AS japanese_date 
FROM orders;
```

**DATE_ADD / DATE_SUB（日付の加算・減算）**
```sql
SELECT DATE_ADD(order_date, INTERVAL 7 DAY) AS delivery_date 
FROM orders;

SELECT DATE_SUB(NOW(), INTERVAL 1 MONTH) AS one_month_ago;
```

**DATEDIFF（日付の差）**
```sql
SELECT DATEDIFF(NOW(), created_at) AS days_since_created 
FROM users;
```

### 12.4 集約関数（再掲）

**COUNT, SUM, AVG, MAX, MIN**
```sql
SELECT 
    COUNT(*) AS total_users,
    AVG(age) AS avg_age,
    MAX(age) AS max_age,
    MIN(age) AS min_age
FROM users;
```

### 12.5 条件分岐関数

**CASE文**
```sql
SELECT 
    name,
    CASE
        WHEN age < 20 THEN '未成年'
        WHEN age < 65 THEN '成人'
        ELSE '高齢者'
    END AS age_category
FROM users;
```

**IF関数（MySQL）**
```sql
SELECT 
    name,
    IF(age >= 18, '成人', '未成年') AS age_category
FROM users;
```

**COALESCE（NULL値の置換）**
```sql
SELECT 
    name,
    COALESCE(email, 'メール未登録') AS email_display
FROM users;
```
- 最初の非NULL値を返す

**NULLIF（値の比較）**
```sql
SELECT NULLIF(price, 0) AS price_or_null 
FROM products;
```
- 2つの値が等しい場合、NULLを返す

---

## 実践的なクエリ例

### 例1: ユーザー一覧と注文数の取得
```sql
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(o.id) AS order_count,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email
ORDER BY total_spent DESC;
```

### 例2: 月別売上集計
```sql
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS monthly_sales,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;
```

### 例3: リピート購入率の計算
```sql
SELECT 
    COUNT(DISTINCT CASE WHEN order_count >= 2 THEN customer_id END) * 100.0 / 
    COUNT(DISTINCT customer_id) AS repeat_purchase_rate
FROM (
    SELECT 
        user_id AS customer_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
) customer_orders;
```

---

## まとめ

### SQLコマンドの優先順位

1. **基本操作**: SELECT, INSERT, UPDATE, DELETE
2. **絞り込み**: WHERE, ORDER BY, LIMIT
3. **集計**: GROUP BY, HAVING, 集約関数
4. **結合**: JOIN（INNER, LEFT）
5. **高度な機能**: サブクエリ, ウィンドウ関数

### よくある間違いと注意点

1. **WHERE句の忘れ**: UPDATE, DELETEで全行が対象になる
2. **NULLの比較**: `=` ではなく `IS NULL` を使用
3. **文字列の引用符**: 数値と文字列を区別
4. **インデックスの活用**: 頻繁に検索するカラムにインデックスを設定
5. **パフォーマンス**: 大量データでは LIMIT や適切な WHERE 句を使用

### 学習の進め方

1. 基本の SELECT, WHERE, ORDER BY をマスター
2. 集計関数と GROUP BY を理解
3. JOIN で複数テーブルを扱えるように
4. サブクエリで複雑な条件を実現
5. 実践的なクエリを書けるように

