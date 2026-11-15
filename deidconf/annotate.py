"""Readable per-note view of a scored split, built only from saved outputs (no model is re-run).

    python -m deidconf.annotate --split test --tag _v5

For every note: the text with each predicted span marked ``[text | category conf%]``, a verdict per span
(correct / wrong boundary / wrong category / false alarm), every gold span the detector missed, and the candidate
misses with the forecaster's probability. Writes results/annotated/<split><tag>.jsonl (all notes) and
<split><tag>_examples.md (a selection, with the text marked inline).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from deidconf.data import read_jsonl

ROOT = Path(__file__).resolve().parents[1]


def uncovered_alnum(text: str, gs: int, ge: int, preds: list[dict]) -> int:
    cov = np.zeros(len(text), bool)
    for p in preds:
        cov[p["start"]:p["end"]] = True
    return sum(1 for i in range(gs, ge) if text[i].isalnum() and not cov[i])


def verdict(r) -> str:
    if r["y_is_phi"] == 0:
        return "false alarm"
    if r["y_cat_ok"] == 0:
        return "wrong category"
    if r["y_exact"] == 0:
        return "boundary off"
    return "correct"


def build(split: str, tag: str) -> list[dict]:
    notes = read_jsonl(ROOT / f"data/meddeid/{split}.jsonl")
    pred = {p["note_id"]: p["spans"] for p in read_jsonl(ROOT / f"results/eval/{split}{tag}/rules+model.predictions.jsonl")}
    frames = []
    for t, col in (("y_is_phi", "is_phi"), ("y_cat_ok", "cat_ok"), ("y_exact", "exact")):
        d = pd.read_csv(ROOT / f"results/confidence/{split}{tag}.rules+model.{t}/oof_predictions.csv")
        frames.append(d[["note_id", "start", "end", t, "p_gbdt:all"]].rename(columns={"p_gbdt:all": f"p_{col}"}))
    m = frames[0].merge(frames[1], on=["note_id", "start", "end"]).merge(frames[2], on=["note_id", "start", "end"])
    byk = {(r.note_id, r.start, r.end): r for r in m.itertuples(index=False)}
    saved = joblib.load(ROOT / f"results/nearmiss/cal{tag}/model.joblib")
    cand = pd.read_csv(ROOT / f"results/nearmiss/{split}{tag}/candidates.csv")
    for c in saved["features"]:
        if c not in cand:
            cand[c] = np.nan
    cand["p_missed"] = saved["model"].predict_proba(cand[saved["features"]])[:, 1]
    cands = {k: g for k, g in cand.groupby("note_id")}
    risk = pd.read_csv(ROOT / f"results/nearmiss/{split}{tag}/note_risk.csv").set_index("note_id")

    out = []
    for n in notes:
        text, nid = n["text"], n["note_id"]
        spans = []
        for p in pred.get(nid, []):
            r = byk.get((nid, p["start"], p["end"]))
            if r is None:
                continue
            spans.append({"start": p["start"], "end": p["end"], "text": text[p["start"]:p["end"]], "category": p["category"],
                          "source": p["source"], "rule": p.get("rule"),
                          "conf_is_phi": round(r.p_is_phi, 4), "conf_category": round(r.p_cat_ok, 4),
                          "conf_exact": round(r.p_exact, 4),
                          "verdict": verdict({"y_is_phi": r.y_is_phi, "y_cat_ok": r.y_cat_ok, "y_exact": r.y_exact})})
        missed = []
        for g in n["spans"]:
            miss = uncovered_alnum(text, g["start"], g["end"], pred.get(nid, []))
            if miss:
                missed.append({"start": g["start"], "end": g["end"], "text": text[g["start"]:g["end"]], "gold_label": g["label"],
                               "uncovered_chars": miss})
        cl = []
        if nid in cands:
            for r in cands[nid].itertuples(index=False):
                cl.append({"start": int(r.start), "end": int(r.end), "text": text[int(r.start):int(r.end)],
                           "category": r.category, "p_missed": round(float(r.p_missed), 4), "is_real_miss": int(r.y_missed)})
        rk = risk.loc[nid]
        out.append({"note_id": nid, "lang": n["lang"], "doc_type": n["doc_type"], "text": text,
                    "note_leak_risk": round(float(rk["p_any"]), 4), "expected_misses": round(float(rk["expected_misses"]), 4),
                    "predicted_spans": spans,
                    "gold_spans": [{"start": g["start"], "end": g["end"], "text": text[g["start"]:g["end"]], "label": g["label"]}
                                   for g in n["spans"]],
                    "missed_gold_spans": missed, "candidate_misses": [c for c in cl if c["p_missed"] >= 0.05]})
    return out


def mark(note: dict) -> str:
    """Text with predicted spans as [text | Cat conf%], missed gold as {{text | MISSED label}}."""
    t = note["text"]
    ev = []
    for s in note["predicted_spans"]:
        tag = f"{s['category']} {s['conf_is_phi'] * 100:.0f}%"
        if s["verdict"] != "correct":
            tag += f" \u26a0 {s['verdict']}"
        ev.append((s["start"], s["end"], "[" + t[s["start"]:s["end"]] + " | " + tag + "]"))
    for s in note["missed_gold_spans"]:
        ev.append((s["start"], s["end"], "{{" + t[s["start"]:s["end"]] + " | MISSED " + s["gold_label"] + "}}"))
    ev.sort()
    pos, buf = 0, []
    for a, b, rep in ev:
        if a < pos:
            continue
        buf += [t[pos:a], rep]
        pos = b
    buf.append(t[pos:])
    return "".join(buf)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test")
    ap.add_argument("--tag", default="_v5")
    ap.add_argument("--examples", type=int, default=12)
    a = ap.parse_args()
    notes = build(a.split, a.tag)
    out = ROOT / "results/annotated"
    out.mkdir(exist_ok=True)
    with open(out / f"{a.split}{a.tag}.jsonl", "w", encoding="utf-8") as f:
        for n in notes:
            f.write(json.dumps(n, ensure_ascii=False) + "\n")
    # a selection: riskiest notes, notes with low-confidence spans, and a few clean ones
    by_risk = sorted(notes, key=lambda n: -n["note_leak_risk"])
    with_err = [n for n in notes if any(s["verdict"] != "correct" for s in n["predicted_spans"])]
    clean = [n for n in notes if n["note_leak_risk"] < 0.01 and all(s["verdict"] == "correct" for s in n["predicted_spans"])
             and not n["missed_gold_spans"]]
    pick, seen = [], set()
    for grp, k in ((by_risk[:4], 4), (sorted(with_err, key=lambda n: -sum(s["verdict"] != "correct" for s in n["predicted_spans"]))[:4], 4),
                   (clean[:4], 4)):
        for n in grp:
            if n["note_id"] not in seen and len(pick) < a.examples:
                seen.add(n["note_id"]); pick.append(n)
    L = [f"# Annotated `{a.split}` notes (examples)", "",
         "Legend: `[text | Category conf%]` is a predicted span with the forecaster's probability that it is PHI; "
         "`⚠ verdict` marks a span that is a false alarm, has the wrong category or off boundaries; "
         "`{{text | MISSED label}}` is gold PHI the detector did not predict. Synthetic notes (MedDeID, CC BY 4.0). "
         "Every note is in `" + f"{a.split}{a.tag}.jsonl`.", ""]
    for n in pick:
        L += [f"## {n['note_id']} ({n['lang']}, {n['doc_type']})", "",
              f"Note leak risk {n['note_leak_risk']:.3f}, expected misses {n['expected_misses']:.2f}; "
              f"{len(n['predicted_spans'])} spans predicted, {len(n['missed_gold_spans'])} gold spans missed.", "",
              "```text", mark(n), "```", ""]
        low = [s for s in n["predicted_spans"] if s["verdict"] != "correct" or s["conf_is_phi"] < 0.9]
        if low:
            L += ["| span | category | conf PHI / category / exact | verdict |", "|---|---|---|---|"]
            L += [f"| {s['text']!r} | {s['category']} | {s['conf_is_phi']:.2f} / {s['conf_category']:.2f} / {s['conf_exact']:.2f} | {s['verdict']} |" for s in low]
            L += [""]
        if n["candidate_misses"]:
            L += ["Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): " + "; ".join(
                f"{c['text']!r} p={c['p_missed']:.2f} ({'real miss' if c['is_real_miss'] else 'not PHI'})" for c in n["candidate_misses"][:6]), ""]
    (out / f"{a.split}{a.tag}_examples.md").write_text("\n".join(L), encoding="utf-8")
    nspan = sum(len(n["predicted_spans"]) for n in notes)
    print(f"{len(notes)} notes, {nspan} predicted spans -> {out}/{a.split}{a.tag}.jsonl and _examples.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
