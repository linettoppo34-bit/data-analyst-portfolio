"""
Retail Sales and Profit Analysis - Sample Superstore
Question: Which categories, regions, and discount levels make money, and which lose it?
Run: python superstore_analysis.py   (needs pandas and matplotlib)
Outputs: Superstore_Dashboard.pdf and Superstore_Dashboard.png
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

TEAL, RED, GREY, INK = "#0b7a63", "#c0392b", "#8a98a3", "#14202b"

# ---- 1. Load and clean ----
df = pd.read_csv("SampleSuperstore.csv")
rows_raw = len(df)
df = df.drop_duplicates()          # 17 exact duplicate rows removed
rows = len(df)
assert df.isna().sum().sum() == 0  # no missing values in this file

# ---- 2. KPIs ----
sales, profit = df["Sales"].sum(), df["Profit"].sum()
margin = profit / sales

# ---- 3. Breakdowns ----
sub = df.groupby("Sub-Category")["Profit"].sum().sort_values()
region = df.groupby("Region").agg(S=("Sales", "sum"), P=("Profit", "sum"))
region["M"] = region.P / region.S * 100
region = region.sort_values("M")
bands = pd.cut(df["Discount"], [-0.01, 0, 0.2, 0.4, 1.0],
               labels=["No discount", "Up to 20%", "20-40%", "Over 40%"])
disc = df.groupby(bands, observed=True).agg(S=("Sales", "sum"), P=("Profit", "sum"), n=("Sales", "size"))
disc["M"] = disc.P / disc.S * 100
states = df.groupby("State")["Profit"].sum().sort_values().head(5)
over20 = df[df.Discount > 0.2]["Profit"].sum()
upto20 = df[df.Discount <= 0.2]["Profit"].sum()

# ---- 4. Dashboard ----
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c5d0d8", "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})
fig = plt.figure(figsize=(14, 8.8), facecolor="white")
gs = GridSpec(4, 12, figure=fig, height_ratios=[0.55, 0.9, 3.2, 3.2], hspace=0.55, wspace=1.2,
              left=0.10, right=0.97, top=0.97, bottom=0.05)

t = fig.add_subplot(gs[0, :]); t.axis("off")
t.text(0, 0.55, "Retail Sales and Profit Dashboard", fontsize=21, fontweight="bold", color=INK, va="center")
t.text(0, 0.02, "Sample Superstore dataset | Prepared by Linet Toppo", fontsize=10.5, color=GREY)

kpis = [("Total Sales", f"${sales/1e6:.2f}M"), ("Total Profit", f"${profit/1e3:,.0f}K"),
        ("Profit Margin", f"{margin*100:.1f}%"), ("Order lines", f"{rows:,}")]
for i, (lab, val) in enumerate(kpis):
    a = fig.add_subplot(gs[1, i*3:(i+1)*3]); a.axis("off")
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, fc="#eef3f6", ec="none"))
    a.text(0.06, 0.66, lab, fontsize=10.5, color=GREY, transform=a.transAxes)
    a.text(0.06, 0.15, val, fontsize=21, fontweight="bold", color=TEAL, transform=a.transAxes)

a1 = fig.add_subplot(gs[2:, 0:4])
a1.barh(sub.index, sub.values/1e3, color=[RED if v < 0 else TEAL for v in sub.values])
a1.axvline(0, color=INK, lw=0.8); a1.set_title("Profit by sub-category ($K)", loc="left", fontweight="bold")
for y, v in enumerate(sub.values/1e3):
    a1.text(v + (1 if v >= 0 else -1), y, f"{v:.0f}", va="center", ha="left" if v >= 0 else "right", fontsize=8.5)
a1.set_xlim(-30, 68)

a2 = fig.add_subplot(gs[2, 4:8])
a2.bar(disc.index.astype(str), disc.M, color=[TEAL if v > 0 else RED for v in disc.M])
a2.axhline(0, color=INK, lw=0.8); a2.set_title("Profit margin by discount level (%)", loc="left", fontweight="bold")
for x, v in enumerate(disc.M):
    a2.text(x, v + (1.5 if v >= 0 else -1.5), f"{v:.0f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=9)
a2.set_ylim(-95, 45); a2.tick_params(axis="x", labelsize=8.5)

a3 = fig.add_subplot(gs[3, 4:8])
a3.barh(states.index, states.values/1e3, color=RED)
a3.set_title("5 states with the biggest losses ($K)", loc="left", fontweight="bold")
for y, v in enumerate(states.values/1e3): a3.text(v - 0.5, y, f"{v:.1f}", va="center", ha="right", fontsize=8.5)
a3.set_xlim(-34, 0)

a4 = fig.add_subplot(gs[2, 8:])
a4.barh(region.index, region.M, color=TEAL)
a4.set_title("Profit margin by region (%)", loc="left", fontweight="bold")
for y, v in enumerate(region.M): a4.text(v + 0.3, y, f"{v:.1f}%", va="center", fontsize=9)
a4.set_xlim(0, 19)

a5 = fig.add_subplot(gs[3, 8:]); a5.axis("off")
a5.set_title("Key findings", loc="left", fontweight="bold")
find = [
 f"1. Discounts above 20% lose money: ${abs(over20)/1e3:,.0f}K\n    lost on those lines vs ${upto20/1e3:,.0f}K earned at 20% or less.",
 "2. Tables, Bookcases and Supplies are the only\n    sub-categories with a negative total profit.",
 f"3. Central has the lowest margin ({region.M.iloc[0]:.1f}%);\n    Furniture earns just 2.5% against 17% elsewhere.",
]
for i, s in enumerate(find): a5.text(0, 0.88 - i*0.3, s, fontsize=9.6, va="top", transform=a5.transAxes)

fig.savefig("Superstore_Dashboard.pdf"); fig.savefig("Superstore_Dashboard.png", dpi=110)

print(f"rows raw {rows_raw}, after dedupe {rows}")
print(f"sales {sales:,.0f} profit {profit:,.0f} margin {margin:.3%}")
print(disc.round(1)); print(f"over20 {over20:,.0f} upto20 {upto20:,.0f}")
