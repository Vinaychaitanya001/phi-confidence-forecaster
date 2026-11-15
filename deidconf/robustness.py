"""Step 7a: robustness views of the confidence layer.

    python -m deidconf.robustness --split cal --eval-tag _v4

(a) Hard negatives: for every hard-negative span the detector redacted, the confidence it received; share that a
    review threshold would flag. (b) Cost per note: regex, single model pass, MC dropout.
(c) Locale / document-type shift is produced by `deidconf.confidence --shift ...` and summarised here if present.
Writes results/robustness/<split><tag>/report.md.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

import numpy as np
import pandas as pd

from deidconf import PROJECT_ROOT
from deidconf.data import read_jsonl


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--eval-tag", default="_v4")
    ap.add_argument("--run", default=None, help="confidence run folder (default <split><tag>.rules+model.y_is_phi)")
    ap.add_argument("--review-below", type=float, default=0.9)
    a = ap.parse_args(argv)
    run = a.run or f"{a.split}{a.eval_tag}.rules+model.y_is_phi"
    notes = {n["note_id"]: n for n in read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")}
    oof = pd.read_csv(PROJECT_ROOT / f"results/confidence/{run}/oof_predictions.csv")
    out = PROJECT_ROOT / "results/robustness" / f"{a.split}{a.eval_tag}"
    out.mkdir(parents=True, exist_ok=True)

    # (a) hard negatives
    by_note = defaultdict(list)
    for r in oof.to_dict("records"):
        by_note[r["note_id"]].append(r)
    hn = defaultdict(lambda: {"n": 0, "redacted": 0, "conf": [], "flagged": 0})
    for nid, n in notes.items():
        for h in n.get("hard_negatives", []):
            d = hn[h["category"]]
            d["n"] += 1
            hits = [r for r in by_note.get(nid, []) if r["start"] < h["end"] and h["start"] < r["end"]]
            if hits:
                d["redacted"] += 1
                c = min(r["p_gbdt:all"] for r in hits)
                d["conf"].append(c)
                d["flagged"] += int(c < a.review_below)
    rows = []
    for cat, d in sorted(hn.items(), key=lambda kv: -kv[1]["n"]):
        rows.append({"type": cat, "n": d["n"], "redacted": d["redacted"],
                     "mean_confidence": float(np.mean(d["conf"])) if d["conf"] else None,
                     "flagged_for_review": d["flagged"]})
    tot = {"n": sum(r["n"] for r in rows), "redacted": sum(r["redacted"] for r in rows),
           "flagged": sum(r["flagged_for_review"] for r in rows)}

    # (b) cost
    det = read_jsonl(PROJECT_ROOT / f"results/detect/{a.split}/entities.jsonl")
    cost = {"regex_s": float(np.mean([d["seconds"]["regex"] for d in det])),
            "model_s": float(np.mean([d["seconds"]["model"] for d in det]))}
    mc_meta = PROJECT_ROOT / f"results/mcdropout/{a.split}/meta.json"
    mc_log = PROJECT_ROOT / f"results/logs/mcdropout_{a.split}.log"
    if mc_meta.exists() and mc_log.exists():
        import re
        m = re.findall(r"([\d.]+) s/note", mc_log.read_text())
        if m:
            cost["mc_dropout_s"] = float(m[-1])
            cost["mc_passes"] = json.loads(mc_meta.read_text())["passes"]

    # (c) shift results, if the confidence run stored them
    shift = {}
    for name in sorted((PROJECT_ROOT / "results/confidence").glob(f"{a.split}{a.eval_tag}*")):
        mj = name / "metrics.json"
        if mj.exists():
            s = json.loads(mj.read_text()).get("shift") or {}
            if s:
                shift[name.name] = s

    L = [f"# Robustness: `{a.split}{a.eval_tag}`", "",
         "## Hard negatives (text that looks like PHI but is not) after the confidence layer", "",
         f"Review threshold: confidence < {a.review_below} is flagged.", "",
         "| Type | n | redacted by detector | mean confidence of those | flagged for review |", "|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['type']} | {r['n']} | {r['redacted']} | {('%.3f' % r['mean_confidence']) if r['mean_confidence'] is not None else '–'} | {r['flagged_for_review']} |")
    L.append(f"| **all** | {tot['n']} | {tot['redacted']} | | {tot['flagged']} |")
    L += ["", "## Cost per note (CPU, 8 threads)", "",
          f"- regex rules: {1000 * cost['regex_s']:.0f} ms", f"- model, single pass: {cost['model_s']:.2f} s"]
    if "mc_dropout_s" in cost:
        L.append(f"- MC dropout, {cost['mc_passes']} passes: {cost['mc_dropout_s']:.2f} s ({cost['mc_dropout_s'] / cost['model_s']:.1f}x)")
    if shift:
        L += ["", "## Shift experiments (forecaster trained on one group, scored on another)", ""]
        for run_name, s in shift.items():
            L += [f"### {run_name}: train {s['_setup']['train']} → test {s['_setup']['test']}", "",
                  "| Model | ECE | AUROC(error) | errors caught @10% |", "|---|---|---|---|"]
            for k, m in s.items():
                if not k.startswith("_"):
                    L.append(f"| {k} | {m['ece']:.4f} | {m['auroc_error']:.3f} | {100 * m['capture@10%']:.0f}% |")
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps({"hard_negatives": rows, "total": tot, "cost": cost, "shift": shift}, indent=1),
                                      encoding="utf-8")
    print(f"hard negatives: {tot} | cost: {cost}")
    print(f"written {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
