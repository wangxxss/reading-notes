# SQL CTE (Common Table Expression) 教程

## 1. 什么是 CTE

CTE（Common Table Expression，公用表表达式）是 SQL 中用 `WITH` 关键字定义的**临时命名结果集**。它只在当前语句的作用域内有效，执行完毕后自动销毁。

可以把 CTE 理解为"SQL 语句内部的临时视图"——它不会持久化到数据库中，但能让复杂查询变得清晰、可读、可维护。

### 支持情况

| 数据库 | 非递归 CTE | 递归 CTE |
|--------|-----------|---------|
| Oracle | 9i（2001 年）起支持 | 11gR2（2009 年）起支持 |
| MySQL | 8.0（2018 年）起支持 | 8.0（2018 年）起支持 |
| PostgreSQL | 8.4（2009 年）起支持 | 8.4（2009 年）起支持 |
| SQL Server | 2005 起支持 | 2005 起支持 |

---

## 2. 为什么用 CTE——优缺点与适用场景

### 2.1 CTE 的优点

**1. 可读性强，逻辑分层清晰**

CTE 允许把一条复杂 SQL 拆成多个命名步骤，从上到下阅读就像读伪代码。对比嵌套三四层的子查询，维护成本大幅降低。

```sql
-- 嵌套子查询：由内向外读，层层剥开才能理解
SELECT * FROM (
    SELECT * FROM (
        SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id
    ) t1 WHERE total > 50000
) t2 WHERE dept_id IN (SELECT dept_id FROM active_depts);

-- CTE：从上到下读，每一步都有名字
WITH dept_salary AS (
    SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id
),
high_salary_dept AS (
    SELECT * FROM dept_salary WHERE total > 50000
)
SELECT * FROM high_salary_dept
WHERE dept_id IN (SELECT dept_id FROM active_depts);
```

**2. 消除重复——同一结果集复用多次**

如果一个子查询在 SQL 中出现了两次以上，用 CTE 定义一次、引用多次，既避免了复制粘贴，也保证了逻辑一致性。

```sql
WITH monthly_sales AS (
    SELECT product_id, sale_month, SUM(amount) AS total
    FROM sales GROUP BY product_id, sale_month
)
-- 同一个 CTE 被 JOIN 了两次
SELECT curr.product_id, curr.total AS this_month, prev.total AS last_month
FROM monthly_sales curr
LEFT JOIN monthly_sales prev
    ON curr.product_id = prev.product_id
    AND curr.sale_month = prev.sale_month + 1;
```

**3. 支持递归——处理树形/层级数据的标准方案**

递归 CTE 是 SQL 标准中唯一的递归查询语法，跨数据库通用（Oracle 的 `CONNECT BY` 是私有扩展）。

**4. 易于调试和修改**

每个 CTE 都可以单独拿出来执行验证结果，修改某一步不影响其他步骤。

### 2.2 CTE 的缺点

**1. 不一定有性能优势**

CTE 本质上是语法糖。非递归 CTE 在大多数数据库中默认被**内联展开**为子查询，执行计划和手写子查询完全一样——它提升的是可读性，不是性能。

**2. 可能阻碍优化器**

在某些数据库（如 PostgreSQL 11 及之前版本）中，CTE 默认被物化，导致优化器无法将外层的过滤条件下推到 CTE 内部，反而比子查询更慢。

```sql
-- PostgreSQL 11-：CTE 被物化，100 万行全部算完后才过滤
WITH all_orders AS (
    SELECT * FROM orders  -- 扫描全表
)
SELECT * FROM all_orders WHERE order_id = 12345;

-- 等价子查询：优化器直接走索引
SELECT * FROM (SELECT * FROM orders) t WHERE order_id = 12345;
```

**3. 只在当前语句内有效**

CTE 无法跨语句复用。如果多条 SQL 都需要同一个中间结果，应该用临时表或视图，而不是在每条 SQL 里重复定义 CTE。

**4. 递归 CTE 有失控风险**

如果终止条件写错或数据存在循环引用，递归 CTE 会无限执行，直到超时或内存耗尽。

### 2.3 什么时候推荐使用 CTE

| 场景 | 原因 |
|------|------|
| SQL 嵌套超过 2 层子查询 | CTE 拆分后可读性显著提升 |
| 同一子查询在 SQL 中出现 2 次以上 | CTE 定义一次，引用多次，避免重复 |
| 需要遍历树形/层级数据 | 递归 CTE 是跨库标准方案 |
| 复杂报表、多步聚合计算 | 每步一个 CTE，逻辑清晰便于维护 |
| 调试复杂 SQL | 可以逐个 CTE 单独执行验证 |

### 2.4 什么时候不推荐使用 CTE

| 场景 | 更好的替代方案 |
|------|--------------|
| 简单查询，一层子查询就能搞定 | 直接写子查询，没必要加 `WITH` |
| 多条 SQL 需要共享同一个中间结果 | 用临时表（`CREATE GLOBAL TEMPORARY TABLE`）或视图 |
| CTE 内数据量巨大且只取少量行 | 确认优化器是否内联；若被物化导致全量计算，改用子查询或加 Hint |
| 对性能要求极高的热点 SQL | 先看执行计划，CTE 和子查询哪个更优就用哪个，不要盲目选择 |
| Oracle 项目中的层级查询 | 优先用 `CONNECT BY`，语法更简洁、Oracle 优化更成熟 |

### 2.5 一句话总结

> CTE 是为**可读性和可维护性**而生的，不是为性能而生的。当你的 SQL 变得"难以阅读"或"子查询重复"时，就是引入 CTE 的时机；当查询本身很简单，或者性能是第一优先级时，不需要强行使用。

---

## 3. 基本语法

```sql
WITH cte_name [(column1, column2, ...)] AS (
    -- CTE 查询体
    SELECT ...
)
-- 主查询，引用 CTE
SELECT * FROM cte_name;
```

**要点：**
- `WITH` 关键字开头
- `cte_name` 是你给这个临时结果集起的名字
- 列名列表可选，省略时自动继承内部 SELECT 的列名
- CTE 定义完成后，紧跟的**第一条** SELECT/INSERT/UPDATE/DELETE 语句可以引用它

---

## 4. 非递归 CTE

### 4.1 基础用法——替代子查询

**不用 CTE（嵌套子查询）：**

```sql
SELECT dept_id, total_salary
FROM (
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
) dept_stats
WHERE total_salary > 100000;
```

**使用 CTE（逻辑更清晰）：**

```sql
WITH dept_stats AS (
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
)
SELECT dept_id, total_salary
FROM dept_stats
WHERE total_salary > 100000;
```

### 4.2 多个 CTE 链式定义

多个 CTE 之间用逗号分隔，后面的 CTE 可以引用前面的 CTE：

```sql
WITH
-- 第一步：统计每个部门的工资总额
dept_salary AS (
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
),
-- 第二步：计算公司平均部门工资
avg_salary AS (
    SELECT AVG(total_salary) AS company_avg
    FROM dept_salary
)
-- 第三步：找出高于平均值的部门
SELECT d.dept_id, d.total_salary, a.company_avg
FROM dept_salary d
CROSS JOIN avg_salary a
WHERE d.total_salary > a.company_avg;
```

### 4.3 CTE 复用——同一个 CTE 引用多次

```sql
WITH monthly_sales AS (
    SELECT product_id, 
           EXTRACT(MONTH FROM sale_date) AS sale_month,
           SUM(amount) AS total_amount
    FROM sales
    WHERE sale_date >= DATE '2025-01-01'
    GROUP BY product_id, EXTRACT(MONTH FROM sale_date)
)
-- 当月 vs 上月 对比
SELECT curr.product_id,
       curr.total_amount AS current_month,
       prev.total_amount AS previous_month,
       curr.total_amount - NVL(prev.total_amount, 0) AS diff
FROM monthly_sales curr
LEFT JOIN monthly_sales prev
    ON curr.product_id = prev.product_id
    AND curr.sale_month = prev.sale_month + 1
WHERE curr.sale_month = 3;
```

> 如果不用 CTE，上面的查询需要写两次相同的子查询，既冗余又容易出错。

---

## 5. 递归 CTE

递归 CTE 用于处理**树形/层级结构**数据，例如组织架构、分类目录、BOM 物料清单等。

### 5.1 语法结构

```sql
WITH RECURSIVE cte_name AS (
    -- 锚点查询（Anchor）：定义起始行
    SELECT ...
    
    UNION ALL
    
    -- 递归查询（Recursive）：引用自身，逐层展开
    SELECT ...
    FROM table_name t
    JOIN cte_name c ON t.parent_col = c.id_col
)
SELECT * FROM cte_name;
```

> **Oracle 语法差异：** Oracle 不需要写 `RECURSIVE` 关键字，直接 `WITH cte_name AS (...)` 即可。

**执行流程：**
1. 执行锚点查询，得到初始结果集
2. 用上一轮的结果作为输入，执行递归查询，得到新一轮的行
3. 重复步骤 2，直到递归查询不再返回新行
4. 将所有轮次的结果 UNION ALL 合并，作为最终结果

### 5.2 示例：组织架构树遍历

假设有如下 `departments` 表：

| dept_id | dept_name | parent_id |
|---------|-----------|-----------|
| 1 | 总公司 | NULL |
| 2 | 华东区 | 1 |
| 3 | 华北区 | 1 |
| 4 | 上海分公司 | 2 |
| 5 | 南京分公司 | 2 |
| 6 | 北京分公司 | 3 |

**标准 SQL 递归 CTE 写法：**

```sql
WITH RECURSIVE dept_tree AS (
    -- 锚点：从根节点（总公司）开始
    SELECT dept_id, dept_name, parent_id, 1 AS lvl,
           dept_name AS full_path
    FROM departments
    WHERE parent_id IS NULL

    UNION ALL

    -- 递归：逐层加入子节点
    SELECT d.dept_id, d.dept_name, d.parent_id, t.lvl + 1,
           t.full_path || '/' || d.dept_name
    FROM departments d
    JOIN dept_tree t ON d.parent_id = t.dept_id
)
SELECT LPAD(' ', 2 * (lvl - 1)) || dept_name AS tree_display,
       lvl,
       full_path
FROM dept_tree
ORDER BY full_path;
```

**输出：**

```
TREE_DISPLAY          LVL  FULL_PATH
总公司                 1    总公司
  华东区               2    总公司/华东区
    上海分公司          3    总公司/华东区/上海分公司
    南京分公司          3    总公司/华东区/南京分公司
  华北区               2    总公司/华北区
    北京分公司          3    总公司/华北区/北京分公司
```

**等价的 Oracle CONNECT BY 写法：**

```sql
SELECT LPAD(' ', 2 * (LEVEL - 1)) || dept_name AS tree_display,
       LEVEL AS lvl,
       SYS_CONNECT_BY_PATH(dept_name, '/') AS full_path
FROM departments
START WITH parent_id IS NULL
CONNECT BY PRIOR dept_id = parent_id
ORDER SIBLINGS BY dept_name;
```

### 5.3 示例：自底向上查询

从某个节点出发，向上查找所有祖先：

```sql
WITH RECURSIVE ancestors AS (
    -- 锚点：从"上海分公司"开始
    SELECT dept_id, dept_name, parent_id, 1 AS lvl
    FROM departments
    WHERE dept_id = 4

    UNION ALL

    -- 递归：向上找父节点
    SELECT d.dept_id, d.dept_name, d.parent_id, a.lvl + 1
    FROM departments d
    JOIN ancestors a ON d.dept_id = a.parent_id
)
SELECT * FROM ancestors;
```

**输出：**

```
DEPT_ID  DEPT_NAME     PARENT_ID  LVL
4        上海分公司     2          1
2        华东区         1          2
1        总公司         NULL       3
```

### 5.4 示例：生成数字序列

递归 CTE 的一个常见技巧——生成连续数字：

```sql
WITH RECURSIVE nums AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 100
)
SELECT n FROM nums;
-- 生成 1 到 100
```

Oracle 中更简洁的写法：

```sql
SELECT LEVEL AS n FROM dual CONNECT BY LEVEL <= 100;
```

---

## 6. CTE 与 DML 配合使用

CTE 不仅能用在 SELECT 中，也能配合 INSERT、UPDATE、DELETE 使用。

### 6.1 CTE + INSERT

```sql
WITH new_records AS (
    SELECT emp_id, salary * 1.1 AS new_salary
    FROM employees
    WHERE dept_id = 10
)
INSERT INTO salary_history (emp_id, salary, effective_date)
SELECT emp_id, new_salary, SYSDATE FROM new_records;
```

### 6.2 CTE + UPDATE（Oracle）

```sql
WITH high_performers AS (
    SELECT emp_id
    FROM performance_reviews
    WHERE score >= 95
)
UPDATE employees
SET bonus = 5000
WHERE emp_id IN (SELECT emp_id FROM high_performers);
```

### 6.3 CTE + DELETE

```sql
WITH duplicates AS (
    SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY id) AS rn
    FROM users
)
DELETE FROM users
WHERE id IN (SELECT id FROM duplicates WHERE rn > 1);
```

---

## 7. 性能注意事项

### 7.1 CTE 是否会被物化

**什么是物化（Materialize）？**

数据库执行 CTE 时有两种策略：

- **内联展开（Inline）**：把 CTE 的定义"复制粘贴"到每个引用处，和写子查询没有区别。不产生额外的临时存储，优化器可以把 CTE 和外层查询统一优化。
- **物化（Materialize）**：先把 CTE 的查询结果**实际执行一次**，存到一个内存临时表中，后续每次引用 CTE 时直接从这个临时表读取，不再重复计算。

简单类比：内联展开就像"每次都重新算一遍"，物化就像"先算好存起来，后面直接查结果"。

**什么时候物化更好？** CTE 被引用多次、且内部计算量大时，物化可以避免重复执行。

**什么时候内联更好？** CTE 只被引用一次、或者内联后优化器能做更好的整体优化（如谓词下推、索引利用）时。

**各数据库的行为：**

- **Oracle**：优化器自动选择物化或内联，也可以通过 Hint 手动控制：
  ```sql
  WITH /*+ MATERIALIZE */ cte AS (...) SELECT ...;
  WITH /*+ INLINE */      cte AS (...) SELECT ...;
  ```
- **MySQL**：8.0 中非递归 CTE 通常被内联展开，递归 CTE 会创建临时表。
- **PostgreSQL**：12+ 版本默认内联展开非递归 CTE（之前版本总是物化）。

### 7.2 递归 CTE 防止无限循环

如果数据中存在循环引用（如 A → B → C → A），递归 CTE 会无限执行。

**Oracle 方案：**
```sql
-- 使用 NOCYCLE 关键字
SELECT * FROM departments
START WITH dept_id = 1
CONNECT BY NOCYCLE PRIOR dept_id = parent_id;
```

**标准 SQL 方案：** 在递归部分加入深度限制或路径去重：
```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, 1 AS depth, CAST(id AS VARCHAR(1000)) AS path
    FROM nodes WHERE parent_id IS NULL

    UNION ALL

    SELECT n.id, n.parent_id, t.depth + 1,
           t.path || ',' || CAST(n.id AS VARCHAR(1000))
    FROM nodes n
    JOIN tree t ON n.parent_id = t.id
    WHERE t.depth < 20                          -- 深度限制
      AND t.path NOT LIKE '%' || n.id || '%'    -- 路径去重防循环
)
SELECT * FROM tree;
```

### 7.3 使用建议

| 场景 | 建议 |
|------|------|
| 简单子查询替代 | 直接用 CTE，可读性更好 |
| 同一子查询引用多次 | 用 CTE 避免重复计算 |
| 树形层级遍历 | Oracle 优先 CONNECT BY，跨库用递归 CTE |
| 超大数据集递归 | 注意递归深度和性能，必要时改用程序处理 |
| CTE 嵌套过多（>5 层） | 考虑拆分为多条 SQL 或使用临时表 |

---

## 8. 快速对照表

| 特性 | CTE 语法 | Oracle CONNECT BY |
|------|---------|-------------------|
| 定义根节点 | 锚点查询 | `START WITH` |
| 定义递归关系 | `JOIN cte ON ...` | `CONNECT BY PRIOR` |
| 当前层级 | 需手动计算 `lvl + 1` | `LEVEL` 伪列 |
| 完整路径 | 需手动拼接 | `SYS_CONNECT_BY_PATH()` |
| 根节点列值 | 需手动传递 | `CONNECT_BY_ROOT` |
| 是否叶子节点 | 需额外判断 | `CONNECT_BY_ISLEAF` |
| 防循环 | 手动路径检测 | `NOCYCLE` |
| 同级排序 | `ORDER BY` 自行控制 | `ORDER SIBLINGS BY` |
| 可移植性 | 跨数据库通用 | 仅 Oracle |

---

## 9. 总结

- **非递归 CTE** 是子查询的上位替代，让 SQL 更易读、可复用
- **递归 CTE** 是处理树形数据的标准 SQL 方案，跨数据库通用
- Oracle 项目中，层级查询优先使用 `CONNECT BY`（语法更简洁，性能更优），跨库场景用递归 CTE
- 写递归 CTE 时务必注意终止条件，防止无限递归
