"""Presentation figures from saved outputs only (no model is run, nothing is fitted).

    python -m deidconf.figures --split test --tag _v5      -> results/figures/*.png
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OURS, GREY = "#c0504d", "#1f6fb5", "#888888"


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(alpha=0.25)


def detector(split, tag, out):
    base = json.loads((ROOT / f"results/eval/{split}/rules+model.json").read_text())
    new = json.loads((ROOT / f"results/eval/{split}{tag}/rules+model.json").read_text())
    fig, (a, b) = plt.subplots(1, 2, figsize=(9, 4), gridspec_kw={"width_ratios": [2, 1]})
    names = ["PHI recall\n(characters)", "Strict category F1"]
    bv = [base["char"]["phi_recall"] * 100, base["strict_category"]["f1"] * 100]
    nv = [new["char"]["phi_recall"] * 100, new["strict_category"]["f1"] * 100]
    x = np.arange(2)
    r1 = a.bar(x - 0.19, bv, 0.38, color=RAW, label="Repo as shipped")
    r2 = a.bar(x + 0.19, nv, 0.38, color=OURS, label="With our 43 rules")
    for r in list(r1) + list(r2):
        a.text(r.get_x() + r.get_width() / 2, r.get_height() + 0.5, f"{r.get_height():.1f}%", ha="center", fontsize=10)
    a.set_xticks(x, names); a.set_ylim(50, 110); a.set_ylabel("%"); a.legend(loc="upper center", ncol=2, frameon=False); _style(a)
    fa = [base["pred_all"]["false_alarms"], new["pred_all"]["false_alarms"]]
    r = b.bar(["Repo as\nshipped", "With our\nrules"], fa, color=[RAW, OURS], width=0.55)
    for rr in r:
        b.text(rr.get_x() + rr.get_width() / 2, rr.get_height() + 4, f"{int(rr.get_height())}", ha="center", fontsize=10)
    b.set_title("False alarms", fontsize=11); _style(b)
    fig.suptitle(f"Detector on the held-out {split} split ({new.get('n_notes', 1008)} notes)", fontsize=12)
    fig.tight_layout(); fig.savefig(out / "fig1_detector.png", dpi=170); plt.close(fig)


def reliability(split, tag, out):
    d = pd.read_csv(ROOT / f"results/confidence/{split}{tag}.rules+model.y_is_phi/oof_predictions.csv")
    y = d["y_is_phi"].to_numpy()
    met = json.loads((ROOT / f"results/confidence/{split}{tag}.rules+model.y_is_phi/metrics.json").read_text())["metrics"]
    reported = {"p_raw_softmax": met["raw_softmax"]["ece"], "p_gbdt:all": met["gbdt:all"]["ece"]}
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
    for a, col, color, title in ((ax[0], "p_raw_softmax", RAW, "Before: the model's own probability"),
                                 (ax[1], "p_gbdt:all", OURS, "After: our forecaster")):
        p = np.nan_to_num(d[col].to_numpy(), nan=0.5)
        bins = np.minimum((p * 10).astype(int), 9)
        xs, ys, ns = [], [], []
        for k in range(10):
            m = bins == k
            if m.sum() >= 5:
                xs.append(p[m].mean()); ys.append(y[m].mean()); ns.append(m.sum())
        a.plot([0, 1], [0, 1], ":", color="black", lw=1, label="perfectly honest")
        a.scatter(xs, ys, s=[30 + 260 * n / max(ns) for n in ns], color=color, alpha=0.85, zorder=3)
        a.plot(xs, ys, color=color, lw=1.3)
        a.set_title(f"{title}\nECE {reported[col]:.3f} (lower is better)", fontsize=11)
        a.set_xlabel("confidence the system states"); a.set_ylabel("how often it was really right")
        a.set_xlim(-0.03, 1.03); a.set_ylim(-0.03, 1.05); _style(a); a.legend(loc="lower right", frameon=False, fontsize=8)
    fig.suptitle("Is this span PHI? Stated confidence versus reality on test (dot size = number of spans)", fontsize=12)
    fig.tight_layout(); fig.savefig(out / "fig2_calibration.png", dpi=170); plt.close(fig)


def review_budget(split, tag, out):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for a, (t, title) in zip(axes, (("y_is_phi", "Is it PHI?\n(false alarms)"), ("y_cat_ok", "Is the category right?"),
                                    ("y_exact", "Are the boundaries exact?"))):
        d = pd.read_csv(ROOT / f"results/confidence/{split}{tag}.rules+model.{t}/oof_predictions.csv")
        err = (d[t].to_numpy() == 0)
        n, e = len(d), int(err.sum())
        for col, color, lab in (("p_raw_softmax", RAW, "model's own probability"), ("p_gbdt:all", OURS, "our forecaster")):
            p = np.nan_to_num(d[col].to_numpy(), nan=0.5)
            o = np.argsort(p, kind="stable")
            found = np.cumsum(err[o]) / e
            a.plot(np.arange(1, n + 1) / n * 100, found * 100, color=color, lw=2, label=lab)
        a.plot([0, 100], [0, 100], ":", color=GREY, label="random order")
        a.set_xlim(0, 30); a.set_ylim(0, 102); a.set_xlabel("% of spans a person reviews (least confident first)")
        a.set_title(f"{title}  ({e} wrong of {n})", fontsize=10.5); _style(a)
    axes[0].set_ylabel("% of the wrong spans found"); axes[0].legend(frameon=False, fontsize=9, loc="lower right")
    fig.suptitle("Review budget on test: where should a person look first?", fontsize=12)
    fig.tight_layout(); fig.savefig(out / "fig3_review_budget.png", dpi=170); plt.close(fig)


def note_risk(split, tag, out):
    d = pd.read_csv(ROOT / f"results/nearmiss/{split}{tag}/note_risk.csv")
    tot = d["n_missed_gold"].sum()
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    n = len(d)
    for key, color, lab in (("p_any", OURS, "our note-level leak risk"), ("n_cands", RAW, "just count suspicious words")):
        o = d.assign(_k=d[key] + 1e-9 * np.random.RandomState(0).rand(n)).sort_values("_k", ascending=False)
        ax.plot(np.arange(1, n + 1) / n * 100, np.cumsum(o["n_missed_gold"]) / tot * 100, color=color, lw=2, label=lab)
    ax.plot([0, 100], [0, 100], ":", color=GREY, label="random order")
    ax.set_xlim(0, 40); ax.set_ylim(0, 102); ax.set_xlabel("% of notes a person reviews (riskiest first)")
    ax.set_ylabel("% of all missed PHI spans found"); ax.legend(frameon=False, loc="lower right"); _style(ax)
    ax.set_title(f"Where is the PHI the detector missed?  ({int(tot)} missed spans in {n} test notes)", fontsize=10.5)
    fig.tight_layout(); fig.savefig(out / "fig4_note_risk.png", dpi=170); plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test")
    ap.add_argument("--tag", default="_v5")
    a = ap.parse_args()
    out = ROOT / "results/figures"
    out.mkdir(exist_ok=True)
    detector(a.split, a.tag, out); reliability(a.split, a.tag, out); review_budget(a.split, a.tag, out); note_risk(a.split, a.tag, out)
    print("wrote", ", ".join(sorted(p.name for p in out.glob("fig*.png"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
