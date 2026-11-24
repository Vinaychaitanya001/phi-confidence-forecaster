"""Assemble the result JSONs of one split into a single Markdown results document.

    python -m deidconf.report --split cal --eval-tag _v4 --baseline-tag "" --out results/RESULTS_cal.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from deidconf import PROJECT_ROOT
from deidconf.data import LABELS


def pct(x, d=1):
    return "–" if x is None else f"{100 * x:.{d}f}%"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--eval-tag", default="_v4")
    ap.add_argument("--baseline-tag", default="")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    R = PROJECT_ROOT / "results"
    ev = load(R / f"eval/{a.split}{a.eval_tag}/rules+model.json")
    ev_rules = load(R / f"eval/{a.split}{a.eval_tag}/rules-only.json")
    ev_model = load(R / f"eval/{a.split}{a.eval_tag}/model-only.json")
    base = load(R / f"eval/{a.split}{a.baseline_tag}/rules+model.json") if a.baseline_tag is not None else None
    conf = {t: load(R / f"confidence/{a.split}{a.eval_tag}.rules+model.{t}/metrics.json") for t in ("y_is_phi", "y_cat_ok", "y_exact")}
    nm = load(R / f"nearmiss/{a.split}{a.eval_tag}/metrics.json")
    rb = load(R / f"robustness/{a.split}{a.eval_tag}/summary.json")
    L = [f"# Results on the MedDeID `{a.split}` split ({ev['speed']['notes'] if ev else '?'} notes)", ""]

    # ---- detector
    L += ["## 1. Detector", "",
          "| System | PHI recall (chars) [95% CI] | Non-PII redaction | Strict category P / R / F1 | False alarms | Hard negatives redacted |",
          "|---|---|---|---|---|---|"]
    rows = []
    if base:
        rows.append(("Baseline: regex + NER model", base))
    if ev_rules:
        rows.append(("MedDeID rules only", ev_rules))
    if ev_model:
        rows.append(("Model only", ev_model))
    if ev:
        rows.append(("**Improved: MedDeID rules + model**", ev))
    for name, r in rows:
        c, s = r["char"], r["strict_category"]
        L.append(f"| {name} | {pct(c['phi_recall'])} [{pct(c['phi_recall_ci'][0])}–{pct(c['phi_recall_ci'][1])}] | "
                 f"{pct(c['nonphi_redaction'], 2)} | {pct(s['precision'])} / {pct(s['recall'])} / {pct(s['f1'])} | "
                 f"{r['pred_all']['false_alarms']} | {r['hard_negatives_all']['redacted']} / {r['hard_negatives_all']['n']} |")
    if ev:
        L += ["", "Per MedDeID label (improved detector):", "",
              "| Label | n | Found (any overlap) | Category correct | Exact |", "|---|---|---|---|---|"]
        for l in LABELS:
            g = ev["gold_by_label"].get(l)
            if g:
                L.append(f"| {l} | {g['n']} | {pct(g['found_any'])} | {pct(g['category_correct'])} | {pct(g['exact'])} |")
        g = ev["gold_all"]
        L.append(f"| **all** | {g['n']} | {pct(g['found_any'])} | {pct(g['category_correct'])} | {pct(g['exact'])} |")
        L += ["", "By locale: " + ", ".join(f"{k} recall {pct(v['phi_recall'])}" for k, v in ev["char_by_lang"].items()) + ". "
              "By document type: " + ", ".join(f"{k} {pct(v['phi_recall'])}" for k, v in ev["char_by_doc_type"].items()) + "."]

    # ---- confidence
    L += ["", "## 2. Confidence of predicted spans (out-of-fold by note)", ""]
    for t, title in (("y_is_phi", "Is the span PHI at all?"), ("y_cat_ok", "…and is the category right?"), ("y_exact", "…and are the boundaries exact?")):
        m = conf.get(t)
        if not m:
            continue
        L += [f"### {title} (`{t}`): {m['n_spans']} spans, {m['n_errors']} errors", "",
              "| Model | ECE ↓ | Brier ↓ | AUROC(error) ↑ | errors caught @5% / 10% / 20% review | precision before → after (≤0.1% recall loss) |",
              "|---|---|---|---|---|---|"]
        for name in ("raw_softmax", "raw_score", "temperature", "platt", "calibrated_mean", "gbdt:p1", "gbdt:p1+mc",
                     "gbdt:p1+p2", "gbdt:our", "gbdt:p1+p2+our", "gbdt:all", "tree:p1", "tree:all"):
            mm = m["metrics"].get(name)
            if not mm:
                continue
            ci = f" [{mm['ece_ci'][0]:.3f}–{mm['ece_ci'][1]:.3f}]" if mm.get("ece_ci") else ""
            L.append(f"| {name} | {mm['ece']:.4f}{ci} | {mm['brier']:.4f} | {mm['auroc_error']:.3f} | "
                     f"{100 * mm['capture@5%']:.0f}% / {100 * mm['capture@10%']:.0f}% / {100 * mm['capture@20%']:.0f}% | "
                     f"{pct(mm['precision_before'], 2)} → {pct(mm['precision_after'], 2)} |")
        if m.get("shift"):
            s = m["shift"]
            L += ["", f"Shift test, forecaster trained on {s['_setup']['train']} and scored on {s['_setup']['test']}: " +
                  "; ".join(f"{k} ECE {v['ece']:.4f}, AUROC {v['auroc_error']:.3f}" for k, v in s.items() if not k.startswith("_")) + "."]
        L += [""]
    m = conf.get("y_is_phi")
    if m and m.get("permutation_importance_top"):
        L += ["Most useful features (permutation importance, `gbdt:all`, is-PHI): " +
              ", ".join(f"`{n}`" for n, _ in m["permutation_importance_top"][:8]) + ".", ""]
    if m:
        L += [f"![reliability](confidence/{a.split}{a.eval_tag}.rules+model.y_is_phi/reliability.png)", ""]

    # ---- near misses
    if nm:
        L += ["## 3. Missed PHI: near-miss candidates and note-level leak risk (our addition)", "",
              f"- {nm['n_candidates']} candidates (τ = {nm['tau']}); {nm['n_positive']} contain missed PHI.",
              f"- Gold spans left (partly) uncovered by the detector: {nm['gold_missed_spans']}; "
              f"{nm['gold_missed_with_candidate']} of them have a candidate ({pct(nm['gold_missed_with_candidate'] / max(1, nm['gold_missed_spans']), 0)} coverage).", "",
              "| Forecaster | AUROC | AUPRC | missed found in top 5% / 10% / 20% of candidates | add p ≥ 0.5: added / truly missed / precision |",
              "|---|---|---|---|---|"]
        for name, mm in nm["span_level"].items():
            a5 = mm["add@0.5"]
            L.append(f"| {name} | {mm['auroc']:.3f} | {mm['auprc']:.3f} | {100 * mm['missed_found@5%cands']:.0f}% / "
                     f"{100 * mm['missed_found@10%cands']:.0f}% / {100 * mm['missed_found@20%cands']:.0f}% | "
                     f"{a5['added']} / {a5['true_missed']} / {pct(a5['precision'], 0) if a5['precision'] is not None else '–'} |")
        n = nm["note_level"]
        L += ["", f"Note level: {n['notes_with_miss']} of {n['notes']} notes contain a missed span. "
              f"P(≥1 miss) = 1 − Π(1 − pᵢ): AUROC **{n['auroc_p_any']:.3f}** (baseline, candidate count: {n['auroc_baseline_ncands']:.3f}), "
              f"ECE {n['ece_p_any']:.3f}. Reviewing the riskiest 5 / 10 / 20% of notes finds "
              f"{pct(n['missed_spans_in_top5%notes'], 0)} / {pct(n['missed_spans_in_top10%notes'], 0)} / {pct(n['missed_spans_in_top20%notes'], 0)} of all missed spans.", ""]

    # ---- robustness
    if rb:
        t = rb["total"]
        L += ["## 4. Hard negatives and cost", "",
              f"- Hard negatives (look like PHI, are not): {t['redacted']} of {t['n']} redacted by the detector; "
              f"the confidence layer flags {t['flagged']} of those {t['redacted']} for review."]
        c = rb["cost"]
        L.append(f"- Cost per note on CPU: rules {1000 * c['regex_s']:.0f} ms, model {c['model_s']:.2f} s" +
                 (f", MC dropout ({c['mc_passes']} passes) {c['mc_dropout_s']:.1f} s" if "mc_dropout_s" in c else "") + ".")
    text = "\n".join(L) + "\n"
    out = Path(a.out) if a.out else R / f"RESULTS_{a.split}{a.eval_tag}.md"
    out.write_text(text, encoding="utf-8")
    print(f"written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
