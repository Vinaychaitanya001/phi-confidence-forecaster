"""Before / after table: the detector alone versus the detector with the four forecasters, from saved outputs only.

    python -m deidconf.before_after --split test --tag _v5

Reads results/annotated/<split><tag>.jsonl (written by ``deidconf.annotate``) and the saved forecaster metrics, and
writes results/before_after/<split><tag>/summary.json and report.md. Nothing is refitted.

Two uses of the forecasters are measured separately and together:
  drop  remove the least-confident predicted spans (is-PHI forecaster). The number removed is the largest that loses
        at most 0.1 % of the true spans; it is chosen with the answer key, so it shows what the score makes
        possible, not a fixed threshold. The tool itself sends low-confidence spans to review instead.
  add   add the candidates the missed-PHI forecaster scores at p >= 0.5 (threshold fixed on `cal`).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from deidconf.confidence import precision_at_recall_loss
from deidconf.data import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
ADD_AT = 0.5


def _mask(n: int, spans: list[dict]) -> np.ndarray:
    m = np.zeros(n, bool)
    for s in spans:
        m[s["start"]:s["end"]] = True
    return m


def system_metrics(notes: list[dict], kept: dict[str, list[dict]], added: dict[str, list[dict]]) -> dict:
    """Character PHI recall, non-PII redaction, gold spans with uncovered letters/digits, false alarms."""
    phi = phi_cov = non = non_red = missed = fa = 0
    for n in notes:
        text, gold = n["text"], n["gold_spans"]
        preds = kept[n["note_id"]] + added.get(n["note_id"], [])
        gm, pm = _mask(len(text), gold), _mask(len(text), preds)
        phi += int(gm.sum()); phi_cov += int((gm & pm).sum())
        non += int((~gm).sum()); non_red += int((~gm & pm).sum())
        alnum = np.fromiter((ch.isalnum() for ch in text), bool, len(text))
        missed += sum(1 for g in gold if (alnum[g["start"]:g["end"]] & ~pm[g["start"]:g["end"]]).any())
        fa += sum(1 for p in kept[n["note_id"]]
                  if not any(p["start"] < g["end"] and g["start"] < p["end"] for g in gold))
    return {"phi_recall": phi_cov / phi, "nonphi_redaction": non_red / non, "missed_gold_spans": missed,
            "false_alarms": fa}


def summarise(notes: list[dict]) -> dict:
    spans = [(n["note_id"], i, p) for n in notes for i, p in enumerate(n["predicted_spans"])]
    conf = np.array([p["conf_is_phi"] for _, _, p in spans])
    y = np.array([0 if p["verdict"] == "false alarm" else 1 for _, _, p in spans])
    prec = precision_at_recall_loss(conf, y)
    drop = {(nid, i) for nid, i, _ in [spans[j] for j in np.argsort(conf, kind="stable")[:prec["spans_dropped"]]]}

    every = {n["note_id"]: list(n["predicted_spans"]) for n in notes}
    kept = {n["note_id"]: [p for i, p in enumerate(n["predicted_spans"]) if (n["note_id"], i) not in drop]
            for n in notes}
    add = {n["note_id"]: [c for c in n["candidate_misses"] if c["p_missed"] >= ADD_AT] for n in notes}
    n_add = sum(len(v) for v in add.values())
    n_add_real = sum(c["is_real_miss"] for v in add.values() for c in v)
    return {
        "notes": len(notes), "spans": len(spans), "not_phi_spans": int((y == 0).sum()),
        "drop": {**prec, "spans_kept": len(spans) - prec["spans_dropped"]},
        "add": {"threshold": ADD_AT, "added": n_add, "real_misses": n_add_real},
        "before": system_metrics(notes, every, {}),
        "after_drop": system_metrics(notes, kept, {}),
        "after_add": system_metrics(notes, every, add),
        "after_drop_and_add": system_metrics(notes, kept, add),
    }


def report(s: dict, conf: dict, near: dict, split: str, tag: str) -> str:
    b, d, a, both = s["before"], s["after_drop"], s["after_add"], s["after_drop_and_add"]
    pct = lambda x, k=1: f"{100 * x:.{k}f} %"
    ece = " / ".join(f"{conf[t]['raw_softmax']['ece']:.3f}" for t in ("y_is_phi", "y_cat_ok", "y_exact"))
    ece_f = " / ".join(f"{conf[t]['gbdt:all']['ece']:.4f}" for t in ("y_is_phi", "y_cat_ok", "y_exact"))
    phi = conf["y_is_phi"]
    L = [f"# Before and after the forecasters: `{split}{tag}`", "",
         f"{s['notes']} notes, {s['spans']} predicted spans ({s['not_phi_spans']} not PHI). Same rules and model in "
         "both columns; nothing is refitted.", "",
         "| Group | Measure | Before (detector alone) | After (with the forecasters) |", "|---|---|---|---|",
         f"| Confidence | ECE: is PHI / category / exact | {ece} | {ece_f} |",
         f"| | AUROC for ranking wrong spans (is PHI) | {phi['raw_softmax']['auroc_error']:.3f} | "
         f"{phi['gbdt:all']['auroc_error']:.3f} |",
         f"| | Not-PHI spans among the 10 % least confident | {pct(phi['raw_softmax']['capture@10%'], 0)} | "
         f"{pct(phi['gbdt:all']['capture@10%'], 0)} |",
         f"| Drop | Precision (spans that are PHI) | {pct(s['drop']['precision_before'], 2)} | "
         f"{pct(s['drop']['precision_after'], 2)} ({s['drop']['spans_dropped']} least-confident spans dropped, "
         f"{s['drop']['true_spans_lost']} true spans lost) |",
         f"| | False alarms (spans touching no PHI) | {b['false_alarms']} | {d['false_alarms']} |",
         f"| Add (p ≥ {s['add']['threshold']}) | PHI recall (characters) | {pct(b['phi_recall'], 2)} | "
         f"{pct(a['phi_recall'], 2)} |",
         f"| | Gold spans with uncovered letters or digits | {b['missed_gold_spans']} | {a['missed_gold_spans']} |",
         f"| | Non-PII redaction | {pct(b['nonphi_redaction'], 3)} | {pct(a['nonphi_redaction'], 3)} |",
         f"| | Additions that are real missed PHI | – | {s['add']['real_misses']} of {s['add']['added']} |",
         f"| Note risk | Missed spans in the riskiest 10 % of notes | – | "
         f"{pct(near['note_level']['missed_spans_in_top10%notes'], 0)} |", "",
         f"Drop and add together: PHI recall {pct(both['phi_recall'], 2)}, {both['missed_gold_spans']} gold spans with "
         f"uncovered letters or digits, {both['false_alarms']} false alarms.", "",
         "The drop count is the largest that loses at most 0.1 % of the true spans, chosen with the answer key: it "
         "shows what the score makes possible, not a fixed threshold. The deliverable pipeline sends spans below "
         "0.9 to review instead of dropping them. The add threshold (0.5) was fixed on `cal`."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="test")
    ap.add_argument("--tag", default="_v5")
    a = ap.parse_args(argv)
    notes = read_jsonl(ROOT / f"results/annotated/{a.split}{a.tag}.jsonl")
    s = summarise(notes)
    conf = {t: json.loads((ROOT / f"results/confidence/{a.split}{a.tag}.rules+model.{t}/metrics.json")
                          .read_text(encoding="utf-8"))["metrics"] for t in ("y_is_phi", "y_cat_ok", "y_exact")}
    near = json.loads((ROOT / f"results/nearmiss/{a.split}{a.tag}/metrics.json").read_text(encoding="utf-8"))
    out = ROOT / "results/before_after" / f"{a.split}{a.tag}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    (out / "report.md").write_text(report(s, conf, near, a.split, a.tag), encoding="utf-8")
    print(f"wrote {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
