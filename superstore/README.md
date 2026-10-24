# Retail Sales and Profit Analysis (Sample Superstore)

**Question:** Which categories, regions, and discount levels make money, and which lose it?

**Data:** Sample Superstore dataset (Kaggle), 9,994 order lines, 13 columns. This version has no order dates or order IDs, so the analysis covers products, regions, segments, and discounts, not time trends.

**Tools:** Python (pandas, matplotlib). Dashboard exported as PDF.

## Cleaning
- Checked for missing values: none.
- Removed 17 exact duplicate rows (9,994 to 9,977).

## Headline numbers
- Total sales: $2.30M. Total profit: $286K. Profit margin: 12.5%.

## Key findings
1. **Discounts above 20% lose money.** Order lines discounted more than 20% lost $135K in total, while lines at 20% or less earned $422K. Margin falls from 30% (no discount) to -15% (20-40% discount) and -77% (over 40%).
2. **Three sub-categories lose money overall:** Tables (-$18K), Bookcases (-$3K) and Supplies (-$1K).
3. **Furniture earns a 2.5% margin**, against about 17% for Office Supplies and Technology.
4. **Central is the weakest region** (7.9% margin vs 14.9% in the West). Texas, Ohio and Pennsylvania lose the most money.

## Recommendations
- Cap discounts at 20% and review the 932 lines discounted over 40%.
- Review pricing and discounting on Tables and Bookcases.
- Investigate why Central and Texas underperform.

## Limitations
- Correlation, not proof: heavy discounts may be used on products that already sell badly.
- No dates, so no trend or seasonality analysis.

## Files
- `superstore_analysis.py`: the full analysis (run it to reproduce the dashboard)
- `Superstore_Dashboard.pdf` / `.png`: one-page dashboard
- `SampleSuperstore.csv`: the data
