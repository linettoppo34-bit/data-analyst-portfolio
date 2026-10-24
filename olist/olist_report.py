"""
E-commerce Delivery and Customer Reviews - Olist dataset
Runs olist_delivery_reviews.sql on the Olist CSV files and builds a one-page report.
Setup: put the 6 CSV files listed in the SQL file inside a folder called "data" (or set DATA_DIR).
Run:   python olist_report.py      (needs pandas and matplotlib)
Outputs: Olist_Report.pdf, Olist_Report.png, results/*.csv
"""
import os, sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

TEAL, RED, GREY, INK = "#0b7a63", "#c0392b", "#8a98a3", "#14202b"
DATA_DIR = os.environ.get("DATA_DIR", "data")

# ---- 1. Load CSVs into an in-memory SQLite database ----
con = sqlite3.connect(":memory:")
for t in ["olist_orders_dataset", "olist_order_reviews_dataset", "olist_order_items_dataset",
          "olist_products_dataset", "olist_customers_dataset", "product_category_name_translation"]:
    pd.read_csv(f"{DATA_DIR}/{t}.csv", encoding="utf-8-sig").to_sql(t, con, index=False)

# ---- 2. Run the SQL file; keep the result of every SELECT ----
sql = "\n".join(l for l in open("olist_delivery_reviews.sql").read().splitlines() if not l.strip().startswith("--"))
results = []
for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
    cur = con.execute(stmt)
    if stmt.upper().startswith("SELECT"):
        results.append(pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description]))
status, main, bands, cats, states = results
os.makedirs("results", exist_ok=True)
for name, d in zip(["1_status", "3_late_vs_ontime", "4_delay_bands", "5_categories", "6_states"], results):
    d.to_csv(f"results/{name}.csv", index=False)

total = int(main.orders.sum())
late = main.set_index("delivery_status")
late_pct = late.loc["Late", "orders"] / total * 100
s_on, s_late = late.loc["On time", "avg_review_score"], late.loc["Late", "avg_review_score"]
bad_on, bad_late = late.loc["On time", "pct_bad_reviews"], late.loc["Late", "pct_bad_reviews"]

# ---- 3. One-page report ----
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#c5d0d8", "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK})
fig = plt.figure(figsize=(14, 9.4), facecolor="white")
gs = GridSpec(5, 12, figure=fig, height_ratios=[0.55, 0.9, 3.0, 3.0, 1.5], hspace=0.65, wspace=1.4,
              left=0.17, right=0.97, top=0.97, bottom=0.04)
fig.text(0.02, 0.955, "E-commerce Delivery and Customer Reviews", fontsize=21, fontweight="bold", va="center")
fig.text(0.02, 0.922, f"Olist Brazilian E-commerce dataset ({total:,} delivered orders with a review) | Prepared by Linet Toppo",
         fontsize=10.5, color=GREY)

for i, (lab, val) in enumerate([("Delivered orders analysed", f"{total:,}"), ("Delivered late", f"{late_pct:.1f}%"),
                                ("Avg review: on time", f"{s_on:.2f} / 5"), ("Avg review: late", f"{s_late:.2f} / 5")]):
    a = fig.add_subplot(gs[1, i*3:(i+1)*3]); a.axis("off")
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, fc="#eef3f6", ec="none"))
    a.text(0.06, 0.66, lab, fontsize=10.5, color=GREY, transform=a.transAxes)
    a.text(0.06, 0.15, val, fontsize=21, fontweight="bold", color=RED if i == 3 else TEAL, transform=a.transAxes)

labels = ["On time", "1-3 days\nlate", "4-7 days\nlate", "8-14 days\nlate", "15+ days\nlate"]
a1 = fig.add_subplot(gs[2, 0:6])
a1.bar(labels, bands.avg_review_score, color=[TEAL] + [RED]*4)
a1.set_title("Average review score by delivery delay", loc="left", fontweight="bold"); a1.set_ylim(0, 5)
for x, (v, n) in enumerate(zip(bands.avg_review_score, bands.orders)):
    a1.text(x, v + 0.08, f"{v:.2f}", ha="center", fontweight="bold"); a1.text(x, 0.12, f"n={n:,}", ha="center", color="white", fontsize=8)

a2 = fig.add_subplot(gs[2, 6:])
a2.bar(["On time", "Late"], [bad_on, bad_late], color=[TEAL, RED], width=0.5)
a2.set_title("Orders with a 1 or 2 star review (%)", loc="left", fontweight="bold"); a2.set_ylim(0, 65)
for x, v in enumerate([bad_on, bad_late]): a2.text(x, v + 1.2, f"{v:.1f}%", ha="center", fontweight="bold")

c = cats[cats.category != "unknown"].sort_values("avg_score_when_late", ascending=False).tail(8)
a3 = fig.add_subplot(gs[3, 0:6])
a3.barh(c.category, c.avg_score_when_late, color=RED)
a3.set_title(f"Avg review of late orders, 8 lowest categories (on-time avg: {s_on:.2f})", loc="left", fontweight="bold", fontsize=9.5); a3.set_xlim(0, 4.3)
for y, (v, n) in enumerate(zip(c.avg_score_when_late, c.late_orders)): a3.text(v + 0.05, y, f"{v:.2f} (n={n})", va="center", fontsize=8.5)

st = states.sort_values("pct_late").tail(8)
a4 = fig.add_subplot(gs[3, 6:])
a4.barh(st.customer_state, st.pct_late, color=[RED if v > late_pct * 1.5 else TEAL for v in st.pct_late])
a4.axvline(late_pct, color=INK, ls="--", lw=1)
a4.set_title("States with the highest share of late orders (%)", loc="left", fontweight="bold"); a4.set_xlim(0, 24)
for y, (v, n) in enumerate(zip(st.pct_late, st.orders)): a4.text(v + 0.3, y, f"{v:.1f}% (n={n:,})", va="center", fontsize=8.5)

fig.text(0.02, 0.145, f"Key findings (dashed line = overall late rate; red states = 1.5x that rate or more)", fontweight="bold", va="top")
notes = [f"1. Late delivery cuts the average review from {s_on:.2f} to {s_late:.2f}. {bad_late:.0f}% of late orders got a 1 or 2 star review, against {bad_on:.0f}% of on-time orders.",
         f"2. The longer the delay, the worse the score: {bands.avg_review_score[1]:.2f} for 1-3 days late, {bands.avg_review_score[2]:.2f} for 4-7 days, and about {bands.avg_review_score[4]:.1f} for 8+ days.",
         f"3. Only {late_pct:.1f}% of orders were late, but it is uneven: MA ({states.set_index('customer_state').loc['MA','pct_late']:.1f}%) and CE ({states.set_index('customer_state').loc['CE','pct_late']:.1f}%) are far above average. Late orders score low in every category (about 2.3 to 2.5)."]
for i, s in enumerate(notes): fig.text(0.02, 0.115 - i*0.03, s, fontsize=10, va="top")
fig.savefig("Olist_Report.pdf"); fig.savefig("Olist_Report.png", dpi=110)
print(main.to_string()); print(f"late share {late_pct:.2f}%")
