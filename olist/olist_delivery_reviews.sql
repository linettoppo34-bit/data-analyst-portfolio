-- =====================================================================
-- PROJECT: E-commerce Delivery and Customer Reviews (Olist dataset)
-- QUESTION: Do late deliveries lower review scores, and by how much?
-- TOOL: DB Browser for SQLite (free). Syntax below is for SQLite.
-- For MySQL, replace julianday(a) - julianday(b) with DATEDIFF(a, b).
--
-- SETUP: In DB Browser: File > Import > Table from CSV file.
-- Import these CSVs and keep the names shown (drop the "_dataset" if you like,
-- but then edit the table names below):
--   olist_orders_dataset, olist_order_reviews_dataset,
--   olist_order_items_dataset, olist_products_dataset,
--   product_category_name_translation, olist_customers_dataset
-- Tick "Column names in first line" and "Trim fields" when importing.
-- =====================================================================


-- STEP 1: Know your data. How many orders per status?
SELECT order_status, COUNT(*) AS orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY orders DESC;
-- Why: we only analyze 'delivered' orders, because only they have a delivery date.


-- STEP 2: Build a clean working table: one row per delivered order with its delay.
-- delay_days > 0 means the order arrived AFTER the promised date (late).
DROP TABLE IF EXISTS order_delivery;
CREATE TABLE order_delivery AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp,
    o.order_estimated_delivery_date,
    o.order_delivered_customer_date,
    ROUND(julianday(o.order_delivered_customer_date)
        - julianday(o.order_estimated_delivery_date), 1) AS delay_days,
    CASE
        WHEN julianday(o.order_delivered_customer_date)
           > julianday(o.order_estimated_delivery_date) THEN 'Late'
        ELSE 'On time'
    END AS delivery_status,
    r.review_score
FROM olist_orders_dataset o
JOIN (
    -- a few orders have more than one review, so we average them to get ONE row per order
    SELECT order_id, AVG(review_score) AS review_score
    FROM olist_order_reviews_dataset
    WHERE review_score IS NOT NULL
    GROUP BY order_id
) r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_delivered_customer_date <> '';


-- STEP 3: MAIN ANSWER. Average review score, late vs on time.
SELECT
    delivery_status,
    COUNT(*)                        AS orders,
    ROUND(AVG(review_score), 2)     AS avg_review_score,
    ROUND(100.0 * SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) / COUNT(*), 1)
                                    AS pct_bad_reviews   -- scores of 1 or 2
FROM order_delivery
GROUP BY delivery_status;
-- >>> This is your headline number for the portfolio and resume.


-- STEP 4: How does the damage grow with the length of the delay?
SELECT
    CASE
        WHEN delay_days <= 0  THEN '1. On time or early'
        WHEN delay_days <= 3  THEN '2. Late by 1-3 days'
        WHEN delay_days <= 7  THEN '3. Late by 4-7 days'
        WHEN delay_days <= 14 THEN '4. Late by 8-14 days'
        ELSE                       '5. Late by 15+ days'
    END AS delay_band,
    COUNT(*)                    AS orders,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM order_delivery
GROUP BY delay_band
ORDER BY delay_band;


-- STEP 5: Which product categories suffer most from late deliveries?
-- (Only categories with at least 100 late orders, so the numbers are reliable.)
SELECT
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
    COUNT(DISTINCT d.order_id)                       AS late_orders,
    ROUND(AVG(d.review_score), 2)                    AS avg_score_when_late
FROM order_delivery d
JOIN olist_order_items_dataset i ON i.order_id = d.order_id
JOIN olist_products_dataset p    ON p.product_id = i.product_id
LEFT JOIN product_category_name_translation t
       ON t.product_category_name = p.product_category_name
WHERE d.delivery_status = 'Late'
GROUP BY category
HAVING late_orders >= 100
ORDER BY avg_score_when_late ASC
LIMIT 10;


-- STEP 6: Which states have the highest share of late orders?
SELECT
    c.customer_state,
    COUNT(*) AS orders,
    ROUND(100.0 * SUM(CASE WHEN d.delivery_status = 'Late' THEN 1 ELSE 0 END) / COUNT(*), 1)
        AS pct_late
FROM order_delivery d
JOIN olist_customers_dataset c ON c.customer_id = d.customer_id
GROUP BY c.customer_state
HAVING orders >= 500
ORDER BY pct_late DESC
LIMIT 10;

-- =====================================================================
-- WHAT TO SEND CLAUDE: the output tables of Steps 3, 4, 5 and 6
-- (copy the grid from DB Browser or take a screenshot).
-- =====================================================================
