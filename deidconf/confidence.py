"""Step 5: confidence models for predicted spans: baselines, forecasters, ablations, calibration metrics.

    python -m deidconf.confidence --features results/features/cal_v5.rules+model.csv --target y_is_phi

Everything is estimated out-of-fold with GroupKFold by note (a span never scores itself), on the calibration split.
Models
  raw_softmax        p1_p_cat_mean used directly as the confidence (what the repo had)
  raw_score          the fused span score (rule spans = 1.0)
  temperature        one parameter T on logit(p) fitted by NLL                      (Guo et al. 2017; paper 2 baseline)
  platt              logistic regression on logit(p)                               (Platt 2000; paper 1 baseline)
  calibrated_mean    GBDT on the mean probability only                             (paper 1 baseline)
  gbdt:<set>         gradient-boosted trees on a feature set                       (paper 1 forecaster)
  tree:<set>         depth-limited decision tree on a feature set                  (paper 2, explainable)
Feature sets (ablation): p1 | p1+mc | p1+p2 | p1+p2+our | our | all(=p1+mc+p2+our)
Metrics: ECE (20 equal-width bins), Brier, NLL, AUROC for "span is an error", review-budget error capture at
5/10/20 % of spans, precision after dropping the least-confident spans at <= 0.1 % recall loss.
Outputs results/confidence/<run>/{metrics.json, report.md, oof_predictions.csv, reliability.png, tree.txt}.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from deidconf import PROJECT_ROOT

CATEGORICAL = ["our_rule_family", "our_rule", "our_category", "our_case", "our_lang"]
ID_COLS = {"note_id", "start", "end", "category", "source", "rule", "doc_type", "lang"}
TARGETS = {"y_overlap_any", "y_is_phi", "y_cat_ok", "y_exact", "y_gold_label", "y_frac_inside"}


def feature_sets(cols: list[str]) -> dict[str, list[str]]:
    p1 = [c for c in cols if c.startswith("p1_") and "_mc_" not in c]
    mc = [c for c in cols if c.startswith("p1_mc_")]
    p2 = [c for c in cols if c.startswith("p2_")]
    our = [c for c in cols if c.startswith("our_")]
    return {"p1": p1, "p1+mc": p1 + mc, "p1+p2": p1 + p2, "p1+p2+our": p1 + p2 + our, "our": our,
            "all": p1 + mc + p2 + our}


# ----------------------------------------------------------------------------- metrics
def ece(p: np.ndarray, y: np.ndarray, n_bins: int = 20) -> float:
    bins = np.minimum((p * n_bins).astype(int), n_bins - 1)
    tot = 0.0
    for b in range(n_bins):
        m = bins == b
        if m.any():
            tot += m.mean() * abs(y[m].mean() - p[m].mean())
    return float(tot)


def reliability(p: np.ndarray, y: np.ndarray, n_bins: int = 10):
    bins = np.minimum((p * n_bins).astype(int), n_bins - 1)
    rows = []
    for b in range(n_bins):
        m = bins == b
        rows.append({"bin": b, "n": int(m.sum()), "conf": float(p[m].mean()) if m.any() else None,
                     "acc": float(y[m].mean()) if m.any() else None})
    return rows


def review_capture(p: np.ndarray, y: np.ndarray, budgets=(0.05, 0.10, 0.20)) -> dict[str, float]:
    """Share of all errors (y == 0) contained in the lowest-confidence `budget` fraction of spans."""
    order = np.argsort(p)
    err = (y == 0)
    out = {}
    for b in budgets:
        k = max(1, int(round(b * len(p))))
        out[f"capture@{int(b * 100)}%"] = float(err[order[:k]].sum() / max(1, err.sum()))
    return out


def precision_at_recall_loss(p: np.ndarray, y: np.ndarray, max_loss: float = 0.001) -> dict[str, float]:
    """Drop spans from the least confident upwards while true-PHI spans lost stay <= max_loss of all true spans."""
    order = np.argsort(p)
    n_pos = int(y.sum())
    allowed = int(np.floor(max_loss * n_pos))
    lost = 0
    cut = 0
    for i, idx in enumerate(order):
        if y[idx] == 1:
            if lost + 1 > allowed:
                break
            lost += 1
        cut = i + 1
    keep = np.ones(len(p), dtype=bool)
    keep[order[:cut]] = False
    base_prec = float(y.mean())
    new_prec = float(y[keep].mean()) if keep.any() else float("nan")
    return {"precision_before": base_prec, "precision_after": new_prec, "spans_dropped": int(cut),
            "errors_removed": int((y[order[:cut]] == 0).sum()), "true_spans_lost": int(lost)}


def all_metrics(p: np.ndarray, y: np.ndarray) -> dict:
    from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
    p = np.clip(p, 1e-6, 1 - 1e-6)
    out = {"n": int(len(y)), "errors": int((y == 0).sum()), "ece": ece(p, y), "brier": float(brier_score_loss(y, p)),
           "nll": float(log_loss(y, p)), "auroc_error": float(roc_auc_score(1 - y, 1 - p)) if 0 < y.sum() < len(y) else float("nan"),
           "auprc_error": float(average_precision_score(1 - y, 1 - p)) if 0 < y.sum() < len(y) else float("nan")}
    out.update(review_capture(p, y))
    out.update(precision_at_recall_loss(p, y))
    return out


def bootstrap_ci(p: np.ndarray, y: np.ndarray, groups: np.ndarray, fn, n: int = 500, seed: int = 7):
    rng = np.random.default_rng(seed)
    uniq = np.unique(groups)
    idx_by = {g: np.where(groups == g)[0] for g in uniq}
    vals = []
    for _ in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by[g] for g in pick])
        try:
            vals.append(fn(p[idx], y[idx]))
        except ValueError:
            continue
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))] if vals else [float("nan")] * 2


# ----------------------------------------------------------------------------- models
def make_pipeline(kind: str, cols: list[str], seed: int):
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.tree import DecisionTreeClassifier
    cat = [c for c in cols if c in CATEGORICAL]
    num = [c for c in cols if c not in CATEGORICAL]
    if kind == "gbdt":
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=10), cat),
                                 ("num", "passthrough", num)], sparse_threshold=0)
        clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_depth=4, min_samples_leaf=20,
                                             l2_regularization=1.0, random_state=seed)
    elif kind == "tree":
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=10), cat),
                                 ("num", SimpleImputer(strategy="median"), num)], sparse_threshold=0)
        clf = DecisionTreeClassifier(max_depth=5, min_samples_leaf=30, class_weight=None, random_state=seed)
    else:
        raise ValueError(kind)
    return Pipeline([("pre", pre), ("clf", clf)])


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def fit_temperature(z: np.ndarray, y: np.ndarray) -> float:
    from scipy.optimize import minimize_scalar
    def nll(T):
        q = 1 / (1 + np.exp(-z / T))
        q = np.clip(q, 1e-6, 1 - 1e-6)
        return -np.mean(y * np.log(q) + (1 - y) * np.log(1 - q))
    return float(minimize_scalar(nll, bounds=(0.05, 20), method="bounded").x)


def oof_predict(df: pd.DataFrame, y: np.ndarray, groups: np.ndarray, model_name: str, cols: list[str],
                n_splits: int, seed: int) -> np.ndarray:
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    oof = np.full(len(df), np.nan)
    gkf = GroupKFold(n_splits=n_splits)
    raw = df["p1_p_cat_mean"].fillna(df["our_score"]).fillna(0.5).to_numpy()
    for tr, te in gkf.split(df, y, groups):
        if model_name == "temperature":
            T = fit_temperature(logit(raw[tr]), y[tr])
            oof[te] = 1 / (1 + np.exp(-logit(raw[te]) / T))
        elif model_name == "platt":
            lr = LogisticRegression(C=1.0, max_iter=1000).fit(logit(raw[tr]).reshape(-1, 1), y[tr])
            oof[te] = lr.predict_proba(logit(raw[te]).reshape(-1, 1))[:, 1]
        else:
            kind, _, _ = model_name.partition(":")
            pipe = make_pipeline(kind, cols, seed)
            pipe.fit(df.iloc[tr][cols], y[tr])
            oof[te] = pipe.predict_proba(df.iloc[te][cols])[:, 1]
    return oof


# ----------------------------------------------------------------------------- apply a saved forecaster (test split)
def apply_saved(a, df: pd.DataFrame, y: np.ndarray, groups: np.ndarray) -> int:
    import joblib
    saved = joblib.load(PROJECT_ROOT / a.apply)
    if saved["target"] != a.target:
        raise SystemExit(f"saved model predicts {saved['target']}, not {a.target}")
    for c in saved["features"]:
        if c not in df:
            df[c] = np.nan
    run = a.run or f"{Path(a.features).stem}.{a.target}.applied"
    out = PROJECT_ROOT / "results/confidence" / run
    out.mkdir(parents=True, exist_ok=True)
    preds = {"raw_softmax": df["p1_p_cat_mean"].fillna(df["our_score"]).fillna(0.5).to_numpy()}
    preds["raw_score"] = np.where(df["our_score"].isna(), preds["raw_softmax"], df["our_score"].to_numpy())
    preds["gbdt:all"] = saved["model"].predict_proba(df[saved["features"]])[:, 1]
    from sklearn.metrics import roc_auc_score
    metrics = {}
    for name, p in preds.items():
        p = np.nan_to_num(p, nan=0.5)
        m = all_metrics(p, y)
        if not a.no_ci:
            m["ece_ci"] = bootstrap_ci(p, y, groups, ece)
            m["auroc_error_ci"] = bootstrap_ci(p, y, groups, lambda pp, yy: roc_auc_score(1 - yy, 1 - pp))
        m["reliability"] = reliability(p, y)
        metrics[name] = m
        print(f"{name:12s} ECE {m['ece']:.4f}  Brier {m['brier']:.4f}  AUROC(err) {m['auroc_error']:.3f}  "
              f"capture@10% {m['capture@10%']:.2f}  prec {m['precision_before']:.3f}->{m['precision_after']:.3f}")
    pb = np.nan_to_num(preds["gbdt:all"], nan=0.5)
    by = {}
    for col in ("category", "our_rule_family", "lang", "doc_type"):
        by[col] = {}
        for k, g in df.groupby(col).groups.items():
            idx = np.asarray(list(g))
            if len(idx) >= 30 and 0 < y[idx].sum() < len(idx):
                by[col][str(k)] = {"n": int(len(idx)), "errors": int((y[idx] == 0).sum()), "ece": ece(pb[idx], y[idx]),
                                   "ece_raw": ece(np.nan_to_num(preds["raw_softmax"][idx], nan=0.5), y[idx])}
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    for name, style in (("raw_softmax", "o-"), ("gbdt:all", "D-")):
        rel = [r for r in metrics[name]["reliability"] if r["n"] >= 20]
        ax.plot([r["conf"] for r in rel], [r["acc"] for r in rel], style, label=f"{name} (ECE {metrics[name]['ece']:.3f})")
    ax.plot([0, 1], [0, 1], "k:", lw=1); ax.set_xlabel("confidence"); ax.set_ylabel("fraction correct")
    ax.set_title(f"Reliability on {Path(a.features).stem} ({a.target}), forecaster fitted on cal"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "reliability.png", dpi=140)
    pd.DataFrame({**{c: df[c] for c in ("note_id", "start", "end", "category", "source", "rule", a.target)},
                  **{f"p_{k}": v for k, v in preds.items()}}).to_csv(out / "oof_predictions.csv", index=False)
    summary = {"features": a.features, "target": a.target, "applied_model": a.apply, "n_spans": int(len(df)),
               "n_errors": int((y == 0).sum()), "has_mc_dropout": bool(df["p1_mc_agree"].notna().mean() > 0.5) if "p1_mc_agree" in df else False,
               "metrics": {k: {kk: vv for kk, vv in v.items() if kk != "reliability"} for k, v in metrics.items()},
               "by_group_gbdt_all": by, "permutation_importance_top": [], "shift": {}}
    (out / "metrics.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"written {out}")
    return 0


# ----------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--features", required=True)
    ap.add_argument("--target", default="y_is_phi", choices=["y_is_phi", "y_cat_ok", "y_exact", "y_overlap_any"])
    ap.add_argument("--run", default=None, help="output folder name under results/confidence")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--no-ci", action="store_true")
    ap.add_argument("--save", action="store_true", help="save gbdt:all fitted on all rows to <run>/model.joblib")
    ap.add_argument("--shift", default=None,
                    help="col=train_value>test_value, e.g. lang=en-GB>en-US: fit on one group, score the other")
    ap.add_argument("--apply", default=None,
                    help="path of a saved model.joblib: no fitting, score these features with it (final test run)")
    a = ap.parse_args(argv)
    df = pd.read_csv(PROJECT_ROOT / a.features)
    y = df[a.target].to_numpy().astype(int)
    groups = df["note_id"].to_numpy()
    if a.apply:
        return apply_saved(a, df, y, groups)
    feats = [c for c in df.columns if c not in ID_COLS and c not in TARGETS]
    sets = feature_sets(feats)
    has_mc = df["p1_mc_agree"].notna().mean() > 0.5 if "p1_mc_agree" in df else False
    if not has_mc:
        sets = {k: [c for c in v if "_mc_" not in c] for k, v in sets.items() if k not in ("p1+mc",)}
        sets.pop("all", None)
        sets["all"] = sets["p1+p2+our"]
    run = a.run or f"{Path(a.features).stem}.{a.target}"
    out = PROJECT_ROOT / "results/confidence" / run
    out.mkdir(parents=True, exist_ok=True)

    preds: dict[str, np.ndarray] = {}
    preds["raw_softmax"] = df["p1_p_cat_mean"].fillna(df["our_score"]).fillna(0.5).to_numpy()
    preds["raw_score"] = np.where(df["our_score"].isna(), preds["raw_softmax"], df["our_score"].to_numpy())
    preds["temperature"] = oof_predict(df, y, groups, "temperature", [], a.folds, a.seed)
    preds["platt"] = oof_predict(df, y, groups, "platt", [], a.folds, a.seed)
    preds["calibrated_mean"] = oof_predict(df, y, groups, "gbdt:mean", ["p1_p_cat_mean"], a.folds, a.seed)
    for name, cols in sets.items():
        preds[f"gbdt:{name}"] = oof_predict(df, y, groups, f"gbdt:{name}", cols, a.folds, a.seed)
    for name in ("p1", "all"):
        preds[f"tree:{name}"] = oof_predict(df, y, groups, f"tree:{name}", sets[name], a.folds, a.seed)

    metrics = {}
    for name, p in preds.items():
        p = np.nan_to_num(p, nan=0.5)
        m = all_metrics(p, y)
        if not a.no_ci and name in ("raw_softmax", "temperature", "gbdt:p1", "gbdt:all", "tree:all"):
            m["ece_ci"] = bootstrap_ci(p, y, groups, ece)
            from sklearn.metrics import roc_auc_score
            m["auroc_error_ci"] = bootstrap_ci(p, y, groups, lambda pp, yy: roc_auc_score(1 - yy, 1 - pp))
        m["reliability"] = reliability(p, y)
        metrics[name] = m
        print(f"{name:20s} ECE {m['ece']:.4f}  Brier {m['brier']:.4f}  AUROC(err) {m['auroc_error']:.3f}  "
              f"capture@10% {m['capture@10%']:.2f}  prec {m['precision_before']:.3f}->{m['precision_after']:.3f}")

    # per-group breakdown for the full model
    best = "gbdt:all"
    pb = np.nan_to_num(preds[best], nan=0.5)
    by = {}
    for col in ("category", "our_rule_family", "lang", "doc_type"):
        by[col] = {}
        for k, g in df.groupby(col).groups.items():
            idx = np.asarray(list(g))
            if len(idx) >= 30 and 0 < y[idx].sum() < len(idx):
                by[col][str(k)] = {"n": int(len(idx)), "errors": int((y[idx] == 0).sum()), "ece": ece(pb[idx], y[idx]),
                                   "ece_raw": ece(np.nan_to_num(preds['raw_softmax'][idx], nan=0.5), y[idx])}
    # decision tree export (explanations, paper 2)
    from sklearn.tree import export_text
    pipe = make_pipeline("tree", sets["all"], a.seed).fit(df[sets["all"]], y)
    names = list(pipe.named_steps["pre"].get_feature_names_out())
    tree = pipe.named_steps["clf"]
    txt = export_text(tree, feature_names=names, max_depth=5, decimals=3, show_weights=True)
    # show_weights prints [n_wrong, n_right] per leaf; add the leaf's confidence = share of correct spans
    txt = re.sub(r"weights: \[([\d.]+), ([\d.]+)\] class: \d",
                 lambda m: f"n={int(float(m.group(1)) + float(m.group(2)))}  confidence={float(m.group(2)) / max(1e-9, float(m.group(1)) + float(m.group(2))):.3f}",
                 txt)
    (out / "tree.txt").write_text(txt, encoding="utf-8")
    # permutation importance of the full GBDT (on OOF folds would be costly; single fit on all data, grouped shuffle)
    from sklearn.inspection import permutation_importance
    gb = make_pipeline("gbdt", sets["all"], a.seed).fit(df[sets["all"]], y)
    pi = permutation_importance(gb, df[sets["all"]], y, scoring="neg_log_loss", n_repeats=3, random_state=a.seed)
    imp = sorted(zip(sets["all"], pi.importances_mean), key=lambda t: -t[1])[:25]

    # plots
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    for name, style in (("raw_softmax", "o-"), ("temperature", "s-"), ("gbdt:p1", "^-"), ("gbdt:all", "D-"), ("tree:all", "v--")):
        rel = [r for r in metrics[name]["reliability"] if r["n"] >= 20]
        ax[0].plot([r["conf"] for r in rel], [r["acc"] for r in rel], style, label=f"{name} (ECE {metrics[name]['ece']:.3f})")
    ax[0].plot([0, 1], [0, 1], "k:", lw=1)
    ax[0].set_xlabel("confidence"); ax[0].set_ylabel("fraction correct"); ax[0].set_title(f"Reliability ({a.target})")
    ax[0].legend(fontsize=7)
    budgets = np.linspace(0.01, 0.5, 50)
    for name in ("raw_softmax", "gbdt:p1", "gbdt:all"):
        p = np.nan_to_num(preds[name], nan=0.5)
        order = np.argsort(p); err = (y == 0)
        ax[1].plot(budgets * 100, [err[order[:max(1, int(round(b * len(p))))]].sum() / max(1, err.sum()) for b in budgets], label=name)
    ax[1].plot(budgets * 100, budgets, "k:", lw=1, label="random")
    ax[1].set_xlabel("% of spans sent to review (least confident first)"); ax[1].set_ylabel("share of errors caught")
    ax[1].set_title("Review budget"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(out / "reliability.png", dpi=140)

    if a.save:
        import joblib
        joblib.dump({"target": a.target, "features": sets["all"], "categorical": CATEGORICAL, "model": gb,
                     "feature_sets": sets, "n_train": int(len(df))}, out / "model.joblib")
        print(f"saved {out / 'model.joblib'}")
    shift = {}
    if a.shift:
        col, _, rest = a.shift.partition("=")
        tr_v, _, te_v = rest.partition(">")
        tr = np.where(df[col].astype(str) == tr_v)[0]
        te = np.where(df[col].astype(str) == te_v)[0]
        for name, cols in (("gbdt:p1", sets["p1"]), ("gbdt:all", sets["all"])):
            pipe = make_pipeline("gbdt", cols, a.seed).fit(df.iloc[tr][cols], y[tr])
            p = pipe.predict_proba(df.iloc[te][cols])[:, 1]
            shift[name] = all_metrics(p, y[te])
        shift["raw_softmax"] = all_metrics(np.nan_to_num(preds["raw_softmax"][te], nan=0.5), y[te])
        shift["_setup"] = {"train": f"{col}={tr_v} ({len(tr)} spans)", "test": f"{col}={te_v} ({len(te)} spans)"}
        for k, m in shift.items():
            if not k.startswith("_"):
                print(f"shift {a.shift} {k:12s} ECE {m['ece']:.4f} AUROC(err) {m['auroc_error']:.3f} capture@10% {m['capture@10%']:.2f}")

    pd.DataFrame({**{c: df[c] for c in ("note_id", "start", "end", "category", "source", "rule", a.target)},
                  **{f"p_{k}": v for k, v in preds.items()}}).to_csv(out / "oof_predictions.csv", index=False)
    summary = {"features": a.features, "target": a.target, "n_spans": int(len(df)), "n_errors": int((y == 0).sum()),
               "folds": a.folds, "has_mc_dropout": bool(has_mc), "feature_sets": {k: len(v) for k, v in sets.items()},
               "metrics": {k: {kk: vv for kk, vv in v.items() if kk != "reliability"} for k, v in metrics.items()},
               "by_group_gbdt_all": by, "permutation_importance_top": [(n, float(v)) for n, v in imp],
               "shift": shift}
    (out / "metrics.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")

    L = [f"# Confidence models: `{Path(a.features).name}`, target `{a.target}`", "",
         f"{len(df)} predicted spans, {int((y == 0).sum())} errors ({100 * (y == 0).mean():.2f}%). "
         f"{a.folds}-fold GroupKFold by note. MC dropout features: {'yes' if has_mc else 'no'}.", "",
         "| Model | ECE ↓ | Brier ↓ | NLL ↓ | AUROC(error) ↑ | errors caught @5% | @10% | @20% | precision before → after (≤0.1% recall loss) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for name, m in metrics.items():
        ci = f" [{m['ece_ci'][0]:.3f}–{m['ece_ci'][1]:.3f}]" if "ece_ci" in m else ""
        L.append(f"| {name} | {m['ece']:.4f}{ci} | {m['brier']:.4f} | {m['nll']:.3f} | {m['auroc_error']:.3f} | "
                 f"{100 * m['capture@5%']:.0f}% | {100 * m['capture@10%']:.0f}% | {100 * m['capture@20%']:.0f}% | "
                 f"{100 * m['precision_before']:.2f}% → {100 * m['precision_after']:.2f}% (−{m['errors_removed']} errors, −{m['true_spans_lost']} PHI) |")
    L += ["", "## ECE by group (gbdt:all vs raw softmax)", "", "| Group | n | errors | ECE gbdt:all | ECE raw |", "|---|---|---|---|---|"]
    for col, d in by.items():
        for k, v in d.items():
            L.append(f"| {col}={k} | {v['n']} | {v['errors']} | {v['ece']:.4f} | {v['ece_raw']:.4f} |")
    L += ["", "## Most important features (permutation, gbdt:all)", ""] + [f"- `{n}`: {v:.4f}" for n, v in imp[:20]]
    L += ["", "![reliability](reliability.png)", "", "Decision tree (paper 2 style explanations): `tree.txt`."]
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
