"""Step 2: score the existing detector on a MedDeID split, from the cached regex + model spans.

    python -m deidconf.evaluate --split cal

Fusion and post-processing are applied here (offline, cheap) in several configurations ("systems"), all from the
same model pass:
  rules+model          repo pipeline: model spans with score < 0.5 dropped, fusion, post-processing   (main)
  rules+model(all)     same but no 0.5 cut-off: every model span kept
  rules-only           regex detector alone
  model-only           model alone (0.5 cut-off)
Clock-time spans (TIME) are dropped in all systems: clock times are not PHI under the MedDeID guideline.

Metrics (PLAN.md step 2), all per system and some per locale / document type:
  * character level: PHI recall (gold PHI characters covered) and non-PII redaction (non-PHI characters redacted),
    MedDeID's own two numbers; document-bootstrap 95% CIs
  * gold span coverage per MedDeID label: fully / partly / not covered (label-agnostic) and category-correct
  * predicted spans: overlap precision, category precision; strict exact P/R/F1 at category level
  * hard negatives: share of each hard-negative type that was (wrongly) redacted
  * speed: seconds per note
Outputs results/eval/<split>/<system>.json, <system>.predictions.jsonl (final spans, for the confidence layer) and
results/eval/<split>/report.md.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from deidconf import PROJECT_ROOT
from deidconf.data import CATEGORIES, CATEGORY, LABELS, read_jsonl

# repo category -> MedDeID top-level category. TIME -> None: not PHI in MedDeID (dropped before scoring).
REPO_TO_MEDDEID = {"PERSON": "Name", "LOCATION": "Address_Location", "ORGANIZATION": "Organization", "ID": "ID",
                   "DATE": "Date", "AGE": "Age_Birthdate", "PHONE": "Contactdetails", "EMAIL": "Contactdetails",
                   "OTHER_PHI": "Other", "PROFESSION": "Profession", "TIME": None}

SYSTEMS = {
    "rules+model": dict(regex=True, model=True, min_score=0.5),
    "rules+model(all)": dict(regex=True, model=True, min_score=None),
    "rules-only": dict(regex=True, model=False, min_score=None),
    "model-only": dict(regex=False, model=True, min_score=0.5),
}


# ----------------------------------------------------------------------------- building final predictions
def final_spans(text: str, regex_ents: list[dict], model_ents: list[dict], cfg: dict, system: dict) -> list[dict]:
    from deid.fusion.span_merger import FusionConfig, fuse
    from deid.postprocess import min_model_score, postprocess_final
    from deid.schema import Entity
    sources = []
    if system["regex"]:
        sources.append([Entity.from_dict(e) for e in regex_ents])
    if system["model"]:
        m = [Entity.from_dict(e) for e in model_ents]
        if system["min_score"] is not None:
            m = min_model_score(m, system["min_score"])
        sources.append(m)
    ents = fuse(text, sources, FusionConfig.from_config(cfg))
    ents = postprocess_final(ents, text, cfg)
    out = []
    for e in ents:
        cat = REPO_TO_MEDDEID.get(e.label, "Other")
        if cat is None:
            continue
        out.append({"start": e.start, "end": e.end, "label": e.label, "category": cat, "source": e.source,
                    "score": e.score, "rule": e.fine_label})
    return out


# ----------------------------------------------------------------------------- scoring one note
def _mask(n: int, spans) -> np.ndarray:
    m = np.zeros(n, dtype=bool)
    for s in spans:
        m[s["start"]:s["end"]] = True
    return m


def score_note(note: dict, pred: list[dict]) -> dict[str, Any]:
    text, gold = note["text"], note["spans"]
    n = len(text)
    gm, pm = _mask(n, gold), _mask(n, pred)
    r: dict[str, Any] = {
        "phi_chars": int(gm.sum()), "phi_chars_covered": int((gm & pm).sum()),
        "nonphi_chars": int((~gm).sum()), "nonphi_chars_redacted": int((~gm & pm).sum()),
        "gold": [], "pred": [], "hard": [],
    }
    for g in gold:
        ov = [p for p in pred if p["start"] < g["end"] and g["start"] < p["end"]]
        covered = int(gm[g["start"]:g["end"]].sum() and (pm[g["start"]:g["end"]]).sum())
        full = bool(pm[g["start"]:g["end"]].all())
        cat_ok = any(p["category"] == CATEGORY[g["label"]] for p in ov)
        exact = any(p["start"] == g["start"] and p["end"] == g["end"] and p["category"] == CATEGORY[g["label"]]
                    for p in ov)
        r["gold"].append({"label": g["label"], "state": "full" if full else ("partial" if ov else "missed"),
                          "cat_ok": cat_ok, "exact": exact})
    for p in pred:
        ov = [g for g in gold if p["start"] < g["end"] and g["start"] < p["end"]]
        inside = pm[p["start"]:p["end"]] & gm[p["start"]:p["end"]]
        r["pred"].append({"category": p["category"], "source": p["source"], "score": p["score"],
                          "is_phi": bool(ov), "mostly_phi": bool(inside.mean() >= 0.5) if p["end"] > p["start"] else False,
                          "cat_ok": any(CATEGORY[g["label"]] == p["category"] for g in ov),
                          "exact": any(g["start"] == p["start"] and g["end"] == p["end"] and
                                       CATEGORY[g["label"]] == p["category"] for g in ov)})
    for h in note.get("hard_negatives", []):
        hit = [p for p in pred if p["start"] < h["end"] and h["start"] < p["end"]]
        r["hard"].append({"category": h["category"], "redacted": bool(hit),
                          "as": sorted({p["category"] for p in hit})})
    return r


# ----------------------------------------------------------------------------- aggregation
def _rate(a, b):
    return a / b if b else None


def _boot(num: np.ndarray, den: np.ndarray, n: int = 1000, seed: int = 7) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n, len(num)))
    vals = num[idx].sum(1) / np.maximum(den[idx].sum(1), 1)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def aggregate(notes: list[dict], per_note: list[dict], seconds: list[dict]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    pc = np.array([r["phi_chars"] for r in per_note]); pcc = np.array([r["phi_chars_covered"] for r in per_note])
    nc = np.array([r["nonphi_chars"] for r in per_note]); ncr = np.array([r["nonphi_chars_redacted"] for r in per_note])
    out["char"] = {"phi_recall": _rate(pcc.sum(), pc.sum()), "phi_recall_ci": _boot(pcc, pc),
                   "nonphi_redaction": _rate(ncr.sum(), nc.sum()), "nonphi_redaction_ci": _boot(ncr, nc)}
    # by locale / doc type
    for key in ("lang", "doc_type"):
        d: dict[str, Any] = {}
        groups = defaultdict(list)
        for n, r in zip(notes, per_note):
            groups[n[key]].append(r)
        for g, rs in sorted(groups.items()):
            d[g] = {"notes": len(rs),
                    "phi_recall": _rate(sum(r["phi_chars_covered"] for r in rs), sum(r["phi_chars"] for r in rs)),
                    "nonphi_redaction": _rate(sum(r["nonphi_chars_redacted"] for r in rs), sum(r["nonphi_chars"] for r in rs))}
        out[f"char_by_{key}"] = d
    # gold coverage per label
    lab: dict[str, Counter] = defaultdict(Counter)
    for r in per_note:
        for g in r["gold"]:
            c = lab[g["label"]]
            c["n"] += 1
            c[g["state"]] += 1
            c["cat_ok"] += g["cat_ok"]
            c["exact"] += g["exact"]
    out["gold_by_label"] = {l: {"n": c["n"], "full": _rate(c["full"], c["n"]), "partial": _rate(c["partial"], c["n"]),
                                "missed": _rate(c["missed"], c["n"]), "found_any": _rate(c["full"] + c["partial"], c["n"]),
                                "category_correct": _rate(c["cat_ok"], c["n"]), "exact": _rate(c["exact"], c["n"])}
                            for l, c in lab.items() if c["n"]}
    allg = Counter()
    for c in lab.values():
        allg.update(c)
    out["gold_all"] = {"n": allg["n"], "full": _rate(allg["full"], allg["n"]), "found_any": _rate(allg["full"] + allg["partial"], allg["n"]),
                       "missed": _rate(allg["missed"], allg["n"]), "category_correct": _rate(allg["cat_ok"], allg["n"]),
                       "exact": _rate(allg["exact"], allg["n"])}
    # predicted spans
    pr = Counter()
    by_src: dict[str, Counter] = defaultdict(Counter)
    by_cat: dict[str, Counter] = defaultdict(Counter)
    for r in per_note:
        for p in r["pred"]:
            for c in (pr, by_src[_src_kind(p["source"])], by_cat[p["category"]]):
                c["n"] += 1
                c["is_phi"] += p["is_phi"]
                c["cat_ok"] += p["cat_ok"]
                c["exact"] += p["exact"]
    def _p(c):
        return {"n": c["n"], "overlap_precision": _rate(c["is_phi"], c["n"]), "category_precision": _rate(c["cat_ok"], c["n"]),
                "exact_precision": _rate(c["exact"], c["n"]), "false_alarms": c["n"] - c["is_phi"]}
    out["pred_all"] = _p(pr)
    out["pred_by_source"] = {k: _p(c) for k, c in sorted(by_src.items())}
    out["pred_by_category"] = {k: _p(c) for k, c in sorted(by_cat.items())}
    # strict exact P/R/F1 at category level
    tp = pr["exact"]; fp = pr["n"] - tp; fn = allg["n"] - allg["exact"]
    P = _rate(tp, tp + fp); R = _rate(tp, tp + fn)
    out["strict_category"] = {"tp": tp, "fp": fp, "fn": fn, "precision": P, "recall": R,
                              "f1": (2 * P * R / (P + R)) if P and R else 0.0}
    # hard negatives
    hn: dict[str, Counter] = defaultdict(Counter)
    for r in per_note:
        for h in r["hard"]:
            hn[h["category"]]["n"] += 1
            hn[h["category"]]["redacted"] += h["redacted"]
            for a in h["as"]:
                hn[h["category"]][f"as:{a}"] += 1
    out["hard_negatives"] = {k: {"n": c["n"], "redacted": c["redacted"], "rate": _rate(c["redacted"], c["n"]),
                                 "as": {kk[3:]: v for kk, v in c.items() if kk.startswith("as:")}}
                             for k, c in sorted(hn.items(), key=lambda kv: -kv[1]["n"])}
    out["hard_negatives_all"] = {"n": sum(c["n"] for c in hn.values()), "redacted": sum(c["redacted"] for c in hn.values())}
    out["hard_negatives_all"]["rate"] = _rate(out["hard_negatives_all"]["redacted"], out["hard_negatives_all"]["n"])
    out["speed"] = {"notes": len(seconds), "mean_regex_s": float(np.mean([s["regex"] for s in seconds])),
                    "mean_model_s": float(np.mean([s["model"] for s in seconds]))}
    return out


def _src_kind(source: str) -> str:
    parts = set(source.split("|"))
    has_r = "regex" in parts
    has_m = any(p not in ("regex", "propagated", "fused") for p in parts)
    return "both" if has_r and has_m else ("rules" if has_r else "model")


# ----------------------------------------------------------------------------- report
def pct(x, d=1):
    return "–" if x is None else f"{100 * x:.{d}f}%"


def write_report(split: str, results: dict[str, dict], out: Path) -> None:
    L = [f"# Existing detector on MedDeID `{split}` split", "",
         "Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the "
         "MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.", "",
         "## 1. Headline (character level, MedDeID's own metrics)", "",
         "| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |",
         "|---|---|---|---|---|---|---|"]
    for name, r in results.items():
        c, s, p, sp = r["char"], r["strict_category"], r["pred_all"], r["speed"]
        L.append(f"| {name} | **{pct(c['phi_recall'])}** [{pct(c['phi_recall_ci'][0])}–{pct(c['phi_recall_ci'][1])}] | "
                 f"{pct(c['nonphi_redaction'], 2)} [{pct(c['nonphi_redaction_ci'][0], 2)}–{pct(c['nonphi_redaction_ci'][1], 2)}] | "
                 f"{pct(s['precision'])} / {pct(s['recall'])} / {pct(s['f1'])} | {p['n']} | {p['false_alarms']} | "
                 f"{sp['mean_regex_s'] + sp['mean_model_s']:.2f} |")
    main = results.get("rules+model") or next(iter(results.values()))
    L += ["", "## 2. Gold spans per MedDeID label (system: rules+model)", "",
          "| Label | n | Fully covered | Partly | Missed | Category correct | Exact |", "|---|---|---|---|---|---|---|"]
    for l in LABELS:
        g = main["gold_by_label"].get(l)
        if g:
            L.append(f"| {l} | {g['n']} | {pct(g['full'])} | {pct(g['partial'])} | {pct(g['missed'])} | "
                     f"{pct(g['category_correct'])} | {pct(g['exact'])} |")
    g = main["gold_all"]
    L.append(f"| **all** | {g['n']} | {pct(g['full'])} | | {pct(g['missed'])} | {pct(g['category_correct'])} | {pct(g['exact'])} |")
    L += ["", "## 3. Predicted spans (system: rules+model)", "",
          "| Group | n | Overlaps PHI | Right category | Exact | False alarms |", "|---|---|---|---|---|---|"]
    for k, p in list(main["pred_by_source"].items()) + list(main["pred_by_category"].items()):
        L.append(f"| {k} | {p['n']} | {pct(p['overlap_precision'])} | {pct(p['category_precision'])} | {pct(p['exact_precision'])} | {p['false_alarms']} |")
    L += ["", "## 4. By locale and document type (rules+model, character level)", "",
          "| Group | Notes | PHI recall | Non-PII redaction |", "|---|---|---|---|"]
    for key in ("char_by_lang", "char_by_doc_type"):
        for k, v in main[key].items():
            L.append(f"| {k} | {v['notes']} | {pct(v['phi_recall'])} | {pct(v['nonphi_redaction'], 2)} |")
    L += ["", "## 5. Hard negatives wrongly redacted (rules+model)", "",
          "| Hard-negative type | n | Redacted | Rate | Redacted as |", "|---|---|---|---|---|"]
    for k, v in main["hard_negatives"].items():
        L.append(f"| {k} | {v['n']} | {v['redacted']} | {pct(v['rate'])} | {', '.join(f'{a}:{n}' for a, n in sorted(v['as'].items()))} |")
    h = main["hard_negatives_all"]
    L.append(f"| **all** | {h['n']} | {h['redacted']} | {pct(h['rate'])} | |")
    L += ["", "Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and "
          "Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error "
          "material the confidence layer (steps 4–6) learns from."]
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------- live re-computation
def redecode_model(text: str, npz_path: Path, meta: dict, label_map: dict) -> list[dict]:
    """Decode model entities again from the cached full probability matrix, with a (possibly updated) label map."""
    from deid.detectors.hf_detector import WordScores, entities_from_word_scores
    z = np.load(npz_path)
    P = z["P"].astype(np.float32)
    spans = [tuple(map(int, s)) for s in z["spans"]]
    if len(P) == 0:
        return []
    o = meta["o_index"]
    am = P.argmax(1)
    rows = np.arange(len(P))
    if o is not None:
        p_o = P[:, o]
        Q = P.copy()
        Q[:, o] = -1.0
        nb = Q.argmax(1)
    else:
        p_o, nb = np.zeros(len(P)), am
    ws = WordScores(spans=spans, p_o=p_o.tolist(), am=am.tolist(), am_p=P[rows, am].tolist(), nb=nb.tolist(),
                    nb_p=P[rows, nb].tolist())
    dp = dict(meta["decode_params"])
    dp.update(tags=[tuple(t) for t in meta["tags"]], label_map=label_map, o_index=o, normalize_text=False)
    return [e.to_dict() for e in entities_from_word_scores(text, ws, **dp)]


# ----------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--detect", default="results/detect")
    ap.add_argument("--out", default="results/eval")
    ap.add_argument("--rules", default="cached", choices=["cached", "live", "baseline"],
                    help="live: run the current regex rules (incl. MedDeID rule set) instead of the cached spans; "
                         "baseline: run the original regex rules and NER model (no MedDeID rule set)")
    ap.add_argument("--model", default="cached", choices=["cached", "redecode"],
                    help="redecode: decode model spans again from cached probabilities with the current label map")
    ap.add_argument("--tag", default=None, help="output folder suffix (default: '_live' when rules/model are live)")
    a = ap.parse_args(argv)
    det_dir = PROJECT_ROOT / a.detect / a.split
    live = a.rules in ("live", "baseline") or a.model == "redecode"
    tag = a.tag if a.tag is not None else ("_live" if live else "")
    out = PROJECT_ROOT / a.out / f"{a.split}{tag}"
    out.mkdir(parents=True, exist_ok=True)
    notes = {n["note_id"]: n for n in read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")}

    from deidconf.detect import adapted_configs, baseline_configs
    live_cfg, models_cfg, labels_cfg = (baseline_configs if a.rules == "baseline" else adapted_configs)()
    systems = dict(SYSTEMS)
    if (det_dir / "entities.jsonl").exists():
        cached = read_jsonl(det_dir / "entities.jsonl")
        meta = json.loads((det_dir / "meta.json").read_text(encoding="utf-8"))
        cfg = live_cfg if live else meta["detection_cfg"]
        missing = set(notes) - {c["note_id"] for c in cached}
        if missing:
            print(f"warning: {len(missing)} notes have no cached detection yet; scoring {len(cached)}")
    else:
        if a.rules not in ("live", "baseline"):
            raise SystemExit(f"no cached detection in {det_dir}: use --rules live for a rules-only evaluation")
        print("no cached model output for this split: scoring rules-only")
        cached = [{"note_id": nid, "regex": [], "model": [], "seconds": {"regex": 0.0, "model": 0.0}} for nid in notes]
        meta, cfg = None, live_cfg
        systems = {"rules-only": SYSTEMS["rules-only"]}
    ordered = [notes[c["note_id"]] for c in cached]

    if a.rules in ("live", "baseline"):
        import time
        from deid.detectors.regex_detector import RegexDetector
        regex = RegexDetector.from_config(live_cfg)
        for c, n in zip(cached, ordered):
            t0 = time.perf_counter()
            c["regex"] = [e.to_dict() for e in regex.detect(n["text"])]
            c["seconds"]["regex"] = time.perf_counter() - t0
    if a.model == "redecode" and meta is not None:
        spec = next(m for m in models_cfg["shortlist"] if m["key"] == models_cfg["selected"])
        label_map = labels_cfg["models"][spec["label_schema"]]
        for c, n in zip(cached, ordered):
            c["model"] = redecode_model(n["text"], det_dir / "probs" / f"{n['note_id']}.npz", meta, label_map)

    results = {}
    for name, system in systems.items():
        per_note, preds = [], []
        for c, n in zip(cached, ordered):
            fs = final_spans(n["text"], c["regex"], c["model"], cfg, system)
            preds.append({"note_id": n["note_id"], "spans": fs})
            per_note.append(score_note(n, fs))
        agg = aggregate(ordered, per_note, [c["seconds"] for c in cached])
        results[name] = agg
        (out / f"{name}.json").write_text(json.dumps(agg, indent=1), encoding="utf-8")
        with open(out / f"{name}.predictions.jsonl", "w", encoding="utf-8") as f:
            for p in preds:
                f.write(json.dumps(p) + "\n")
        c = agg["char"]
        print(f"{name:18s} PHI recall {pct(c['phi_recall'])}  non-PII redaction {pct(c['nonphi_redaction'], 2)}  "
              f"strict F1 {pct(agg['strict_category']['f1'])}  false alarms {agg['pred_all']['false_alarms']}")
    write_report(f"{a.split}{tag}", results, out)
    print(f"report: {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
