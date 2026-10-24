# E-commerce Delivery and Customer Reviews (Olist)

**Question:** Do late deliveries lower review scores, and by how much?

**Data:** Brazilian E-Commerce Public Dataset by Olist (Kaggle). Six tables were used: orders, order reviews, order items, products, customers, and the category name translation. The data is not included here because of its size; download it from Kaggle and put the six CSV files in a folder called `data`.

**Tools:** SQL (SQLite) for the analysis, Python (pandas, matplotlib) for the charts and PDF report.

## Method
1. Kept only orders with status `delivered` (96,478 of 99,441 orders), since only they have a delivery date.
2. Averaged the review scores of the few orders that had more than one review, so each order counts once. Result: 95,824 delivered orders with a review.
3. Defined a **late** order as one delivered after its estimated delivery date.
4. Compared review scores for late and on-time orders, by length of delay, by product category, and by customer state.

## Key findings
1. **Late delivery lowers review scores sharply.** Average review: **4.29 for on-time orders vs 2.57 for late orders** (out of 5). 54.0% of late orders received a 1 or 2 star review, against 9.2% of on-time orders.
2. **The longer the delay, the lower the score.** 3.75 for 1-3 days late, 2.30 for 4-7 days, 1.74 for 8-14 days, and 1.71 for 15+ days.
3. **8.0% of orders were late**, but unevenly: Maranhão (MA, 19.2%), Ceará (CE, 15.2%), Bahia (BA, 13.7%) and Rio de Janeiro (RJ, 13.3%) are well above average.
4. **Late orders score low in every category** (about 2.3 to 2.5 for the categories with the most late orders), so the problem is delivery, not product type.

## Recommendations
- Focus delivery improvements on the states with the highest late rates (MA, CE, BA, RJ).
- Warn customers early when an order will be late, since reviews drop sharply after just 4-7 days.
- Review the delivery date estimates, as many late orders come from promises that were not met.

## Limitations
- This shows an association; other factors (product quality, seller behaviour) may also affect scores, and unhappy customers may be more likely to leave reviews.
- Delivery dates are compared with the estimated date shown to the customer, not with how fast the delivery actually was.
- Orders without a review are not included.

## Files
- `olist_delivery_reviews.sql`: the SQL queries, step by step with comments
- `olist_report.py`: runs the SQL and builds the report
- `Olist_Report.pdf` / `.png`: one-page report
- `results/`: the output tables of each SQL step
