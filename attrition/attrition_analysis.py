"""
Employee Attrition Analysis - IBM HR Analytics dataset
Question: Which groups of employees are most likely to leave, and what do they have in common?
Run: python attrition_analysis.py   (needs pandas and matplotlib)
Outputs: Attrition_Dashboard.pdf and Attrition_Dashboard.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

TEAL, RED, GREY, INK = "#0b7a63", "#c0392b", "#8a98a3", "#14202b"

# ---- 1. Load and check ----
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")
assert df.isna().sum().sum() == 0 and df.duplicated().sum() == 0
df["Left"] = (df["Attrition"] == "Yes").astype(int)   # 1 = left, 0 = stayed
overall = df["Left"].mean() * 100

# ---- 2. Attrition rate helper (rate = share of employees in the group who left) ----
def rate(col):
    g = df.groupby(col, observed=True)["Left"].agg(["size", "mean"])
    g["mean"] *= 100
    return g

df["Age band"] = pd.cut(df["Age"], [0, 25, 35, 45, 100], labels=["Under 25", "25-34", "35-44", "45+"], right=False)
df["Tenure band"] = pd.cut(df["YearsAtCompany"], [0, 2, 6, 11, 100], labels=["0-1 yrs", "2-5 yrs", "6-10 yrs", "11+ yrs"], right=False)
df["Income band"] = pd.cut(df["MonthlyIncome"], [0, 3000, 5000, 8000, 1e6], labels=["Under 3K", "3-5K", "5-8K", "8K+"], right=False)

role, ot = rate("JobRole").sort_values("mean"), rate("OverTime")
age, ten, inc = rate("Age band"), rate("Tenure band"), rate("Income band")
inc_left = df[df.Left == 1]["MonthlyIncome"].mean()
inc_stay = df[df.Left == 0]["MonthlyIncome"].mean()

# ---- 3. Dashboard ----
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c5d0d8", "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})
fig = plt.figure(figsize=(14, 9.4), facecolor="white")
gs = GridSpec(5, 12, figure=fig, height_ratios=[0.55, 0.9, 3.0, 3.0, 1.5], hspace=0.6, wspace=1.2,
              left=0.19, right=0.97, top=0.97, bottom=0.04)

t = fig.add_subplot(gs[0, :]); t.axis("off")
fig.text(0.02, 0.955, "Employee Attrition Analysis", fontsize=21, fontweight="bold", va="center")
fig.text(0.02, 0.922, "IBM HR Analytics sample dataset (1,470 employees) | Prepared by Linet Toppo", fontsize=10.5, color=GREY)

kpis = [("Employees", f"{len(df):,}"), ("Left the company", f"{df.Left.sum()}"),
        ("Attrition rate", f"{overall:.1f}%"),
        ("Avg income: left vs stayed", f"{inc_left:,.0f} vs {inc_stay:,.0f}")]
for i, (lab, val) in enumerate(kpis):
    a = fig.add_subplot(gs[1, i*3:(i+1)*3]); a.axis("off")
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, fc="#eef3f6", ec="none"))
    a.text(0.06, 0.66, lab, fontsize=10.5, color=GREY, transform=a.transAxes)
    a.text(0.06, 0.15, val, fontsize=21 if i < 3 else 17, fontweight="bold", color=TEAL, transform=a.transAxes)

def hbar(ax, g, title, xmax):
    cols = [RED if v >= overall * 1.5 else TEAL for v in g["mean"]]
    ax.barh(g.index.astype(str), g["mean"], color=cols)
    ax.axvline(overall, color=INK, lw=1, ls="--")
    ax.set_title(title, loc="left", fontweight="bold"); ax.set_xlim(0, xmax)
    for y, (v, n) in enumerate(zip(g["mean"], g["size"])):
        ax.text(v + 0.8, y, f"{v:.1f}% (n={n})", va="center", fontsize=8.5)

hbar(fig.add_subplot(gs[2:4, 0:4]), role, "Attrition rate by job role (%)", 62)
hbar(fig.add_subplot(gs[2, 4:8]), ot, "By overtime (%)", 50)
hbar(fig.add_subplot(gs[2, 8:]), ten, "By years at company (%)", 52)
hbar(fig.add_subplot(gs[3, 4:8]), age, "By age band (%)", 58)
hbar(fig.add_subplot(gs[3, 8:]), inc, "By monthly income band (%)", 46)

f = fig.add_subplot(gs[4, :]); f.axis("off")
fig.text(0.02, 0.145, "Key findings (dashed line = overall rate of 16.1%; red = 1.5x the overall rate or more)", fontweight="bold", va="top")
notes = [
 f"1. Overtime is the strongest signal: {ot.loc['Yes','mean']:.1f}% of employees working overtime left, against {ot.loc['No','mean']:.1f}% of those who do not.",
 f"2. New and young employees leave most: {ten.loc['0-1 yrs','mean']:.1f}% in their first year and {age.loc['Under 25','mean']:.1f}% of those under 25.",
 f"3. Low pay and some roles stand out: {inc.loc['Under 3K','mean']:.1f}% attrition under 3K monthly income; Sales Representatives {role.loc['Sales Representative','mean']:.1f}% (small group, n={role.loc['Sales Representative','size']}).",
]
for i, s in enumerate(notes): fig.text(0.02, 0.115 - i*0.03, s, fontsize=10, va="top")

fig.savefig("Attrition_Dashboard.pdf"); fig.savefig("Attrition_Dashboard.png", dpi=110)

# combined group used in the README
g = df[(df.OverTime == "Yes") & (df.Age < 35)]
print(f"overall {overall:.1f}%  overtime&under35: n={len(g)}, rate={g.Left.mean()*100:.1f}%")
print(f"income left {inc_left:,.0f} vs stayed {inc_stay:,.0f}")
