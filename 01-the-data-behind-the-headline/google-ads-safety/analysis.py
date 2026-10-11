"""
Ads removed per suspended account, from Google's public Ads Safety Reports.

The question: is Google enforcing more at the ad level and less at the account level?
The proxy: ads removed / advertiser accounts suspended, by year and by scope.

Usage:
    python analysis.py                      
    python analysis.py --data my_data.csv   

All figures come from Google's published reports.
"""

import argparse
import csv
from pathlib import Path


def load(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "year": int(r["year"]),
                "scope": r["scope"],
                "ads_removed": float(r["ads_removed"]),
                "accounts_suspended": float(r["accounts_suspended"]),
                "ads_restricted": float(r["ads_restricted"]) if r["ads_restricted"] else None,
                "verified": r["verified"].strip().upper() == "TRUE",
            })
    return rows


def add_residual_scope(rows):
    """Back out a 'non-scam' row wherever a year has both 'all' and 'scams'."""
    by_key = {(r["year"], r["scope"]): r for r in rows}
    extra = []
    for (year, scope), total in by_key.items():
        scam = by_key.get((year, "scams"))
        if scope == "all" and scam:
            extra.append({
                "year": year,
                "scope": "non-scam (derived)",
                "ads_removed": total["ads_removed"] - scam["ads_removed"],
                "accounts_suspended": total["accounts_suspended"] - scam["accounts_suspended"],
                "ads_restricted": None,
                "verified": total["verified"] and scam["verified"],
            })
    return rows + extra


def ratio(r):
    return r["ads_removed"] / r["accounts_suspended"]


def pct_change(new, old):
    return (new - old) / old * 100


def report(rows):
    print(f"{'year':<6}{'scope':<22}{'ads removed':>14}{'accts susp.':>14}{'ads/acct':>10}  verified")
    for r in sorted(rows, key=lambda r: (r["year"], r["scope"])):
        print(f"{r['year']:<6}{r['scope']:<22}{r['ads_removed']/1e9:>12.2f}B"
              f"{r['accounts_suspended']/1e6:>12.1f}M{ratio(r):>10.0f}  {r['verified']}")

    totals = sorted((r for r in rows if r["scope"] == "all"), key=lambda r: r["year"])
    for prev, cur in zip(totals, totals[1:]):
        print(f"\n{prev['year']} -> {cur['year']} (all scopes)")
        print(f"  ads removed        {pct_change(cur['ads_removed'], prev['ads_removed']):+.1f}%")
        print(f"  accounts suspended {pct_change(cur['accounts_suspended'], prev['accounts_suspended']):+.1f}%")
        print(f"  ads per account    {pct_change(ratio(cur), ratio(prev)):+.1f}%")
        if cur["ads_restricted"] and prev["ads_restricted"]:
            print(f"  ads restricted     {pct_change(cur['ads_restricted'], prev['ads_restricted']):+.1f}%")

    if not all(r["verified"] for r in rows):
        print("\nHeads up: some rows are unverified. Check them against the primary reports.")


def chart(rows, out="ads_enforcements.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed, skipping chart.")
        return
    rows = sorted(rows, key=lambda r: (r["year"], r["scope"]))
    labels = [f"{r['year']}\n{r['scope']}" for r in rows]
    values = [ratio(r) for r in rows]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(labels, values, color=["#9aa0a6" if r["scope"] == "scams" else "#1a73e8" for r in rows])
    ax.bar_label(bars, fmt="%.0f")
    ax.set_ylabel("Ads removed per suspended account")
    ax.set_title("Google Ads enforcement: ads removed per suspended account")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, "Source: Google Ads Safety Reports 2024, 2025. Ratio is a proxy; see README.",
             fontsize=8, color="#5f6368")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out, dpi=200)
    print(f"\nSaved {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", default=Path(__file__).parent / "data" / "ads_safety_report.csv")
    p.add_argument("--chart", default="ads_enforcements.png")
    args = p.parse_args()
    rows = add_residual_scope(load(args.data))
    report(rows)
    chart(rows, args.chart)
