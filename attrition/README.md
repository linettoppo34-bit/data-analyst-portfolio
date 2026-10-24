# Employee Attrition Analysis (IBM HR Analytics)

**Question:** Which groups of employees are most likely to leave, and what do they have in common?

**Data:** IBM HR Analytics Employee Attrition & Performance (Kaggle), 1,470 employees, 35 columns. This is a sample dataset created by IBM data scientists, not real company records.

**Tools:** Python (pandas, matplotlib). Dashboard exported as PDF.

## Method
- Checked for missing values and duplicates: none.
- Created a `Left` column (1 if Attrition = Yes, else 0). The **attrition rate** of a group is the average of this column, which is the share of that group who left.
- Compared attrition rates by job role, overtime, age band, years at company, and monthly income band.
- Compared average income of employees who left and those who stayed.

## Headline numbers
- 237 of 1,470 employees left: an attrition rate of **16.1%**.
- Employees who left earned less on average (4,787 vs 6,833 per month).

## Key findings
1. **Overtime is the strongest signal.** 30.5% of employees working overtime left, against 10.4% of those who do not (about 3 times higher).
2. **New and young employees leave most.** 34.9% of employees in their first year and 39.2% of those under 25 left.
3. **Lower pay is linked to leaving.** Attrition was 28.6% for monthly income under 3K, against about 10% above 5K.
4. **Some roles stand out.** Sales Representatives (39.8%, n=83), Laboratory Technicians (23.9%) and Human Resources (23.1%, n=52) are above average. Sales Representatives and HR are small groups, so treat their rates as indicators, not firm results.
5. **The combination is stronger:** employees under 35 who work overtime had a 45.3% attrition rate (n=172).

## Recommendations
- Review overtime workloads, especially for employees under 35.
- Strengthen onboarding and check-ins during the first year.
- Review pay for the lowest income band and for Sales Representatives.

## Limitations
- These are associations, not proven causes. Overtime is linked to leaving, but the data cannot show that it causes it.
- Sample dataset with fictional data, so the results are for practice and are not real company findings.

## Files
- `attrition_analysis.py`: the full analysis (run it to reproduce the dashboard)
- `Attrition_Dashboard.pdf` / `.png`: one-page dashboard
- `WA_Fn-UseC_-HR-Employee-Attrition.csv`: the data
