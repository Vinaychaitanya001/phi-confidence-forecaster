"""Step 4: features and targets for every PREDICTED span (the confidence layer's training table).

    python -m deidconf.features --split cal --eval-tag _v4 --system rules+model

Inputs: final predictions results/eval/<split><tag>/<system>.predictions.jsonl, the cached word-probability matrix
results/detect/<split>/probs/<note>.npz, optional MC-dropout results/mcdropout/<split>/<note>.npz, and the gold split.
Output: results/features/<split><tag>.<system>.csv, one row per predicted span.

Feature groups (PLAN.md 4.3)
  p1_*   paper 1 (Jagannatha & Yu 2020): mean / min / geometric-mean probability of the predicted label over the
         span's words, P(O) statistics, span length, MC-dropout mean and standard deviation, pass agreement
  p2_*   paper 2 (Jiwani et al. 2026): Probability Density Map of the neighbourhood (10 probability bins x
         {same category, other entity, O}, Gaussian distance weights), entropy, top-1/top-2 ratio and gap,
         coefficient of variation, class counts at span / neighbour / note level
  our_*  rules-vs-model agreement, which rule family fired, repetition of the string in the note, letter case,
         digits, "Key: value" header context, position, locale
Targets
  y_is_phi  >= 50% of the span's characters lie inside gold PHI (drives redaction decisions)
  y_cat_ok  y_is_phi and the MedDeID top-level category matches
  y_exact   exact start, end and category match
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from deidconf import PROJECT_ROOT
from deidconf.data import CATEGORY, read_jsonl
from deidconf.evaluate import REPO_TO_MEDDEID

N_BINS = 10
NEIGH = 8            # words on each side used for the PDM / neighbour statistics
PDM_R = 3.0          # Gaussian decay rate of paper 2 (distance in words)

RULE_FAMILY = {
    "header": ("md_name_header", "md_name_header_nl", "md_name_header_inline", "md_org_header", "md_org_from_line",
               "md_org_for_line", "md_locality", "md_home_address", "md_profession", "md_age_header", "md_dob",
               "md_mrn", "md_accession", "md_professional_id", "md_nhs_number", "md_ni_number_ctx", "org_field",
               "address_line", "date_ctx_label", "pin_ctx", "ssn_ctx", "phone_ctx", "age_ctx", "location_field"),
    "narrative": ("md_name_by", "md_name_with", "md_name_under", "md_name_relation", "md_name_relation_after",
                  "md_name_referring", "md_name_subject", "md_name_signoff", "md_place_in_from",
                  "md_place_after_name_from", "md_place_signoff", "org_employer", "name_relation"),
    "format": ("md_ni_number", "md_ssn_spaced", "md_professional_id_prefixed", "md_signoff_id", "md_uk_mobile",
               "md_uk_landline", "md_uk_postcode", "md_age_hyphen", "md_age_hyphen_small", "md_age_yo",
               "md_age_unit_old", "md_name_credential", "md_name_title", "md_org_suffix", "email", "url", "ssn",
               "phone_us", "street_address", "address_zip"),
}


def rule_family(rule: str | None) -> str:
    if not rule:
        return "none"
    for fam, names in RULE_FAMILY.items():
        if rule in names:
            return fam
    if rule.startswith("date") or rule.startswith("time"):
        return "format"
    return "other"


def entropy(P: np.ndarray) -> np.ndarray:
    Q = np.clip(P, 1e-9, 1.0)
    return -(Q * np.log(Q)).sum(-1)


def case_pattern(s: str) -> str:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return "nolet"
    if all(c.isupper() for c in letters):
        return "upper"
    if all(c.islower() for c in letters):
        return "lower"
    words = re.findall(r"[A-Za-z][A-Za-z'’\-]*", s)
    if words and all(w[0].isupper() for w in words):
        return "title"
    return "mixed"


class TagGroups:
    """Column groups of the model's tag space: for each MedDeID category, the tag ids whose repo category maps to it."""

    def __init__(self, meta: dict, label_map: dict):
        tags = [tuple(t) for t in meta["tags"]]
        self.o = meta["o_index"]
        self.cat_cols: dict[str, list[int]] = {}
        self.entity_cols: list[int] = []
        for i, (prefix, typ) in enumerate(tags):
            if typ is None:
                continue
            repo = label_map.get(typ)
            cat = REPO_TO_MEDDEID.get(repo) if repo else None
            if repo is None or cat is None:
                continue            # dropped labels count as non-PHI mass
            self.cat_cols.setdefault(cat, []).append(i)
            self.entity_cols.append(i)

    def mass(self, P: np.ndarray, cat: str | None) -> np.ndarray:
        cols = self.cat_cols.get(cat, [])
        return P[:, cols].sum(1) if cols else np.zeros(len(P))

    def entity_mass(self, P: np.ndarray) -> np.ndarray:
        return P[:, self.entity_cols].sum(1) if self.entity_cols else np.zeros(len(P))


def word_index(spans: np.ndarray, start: int, end: int) -> np.ndarray:
    """Indices of words overlapping [start, end)."""
    if len(spans) == 0:
        return np.zeros(0, dtype=int)
    return np.where((spans[:, 0] < end) & (spans[:, 1] > start))[0]


def pdm(P: np.ndarray, groups: TagGroups, cat: str, span_idx: np.ndarray, n_words: int) -> dict[str, float]:
    """Paper 2's Probability Density Map: for neighbour words (not in the span), add the distance-weighted
    probability of {same category, other entity, O} into 10 bins by probability value."""
    out = {}
    if len(span_idx) == 0 or n_words == 0:
        for g in ("same", "other", "o"):
            for b in range(N_BINS):
                out[f"p2_pdm_{g}_b{b}"] = 0.0
        return out
    lo, hi = int(span_idx.min()), int(span_idx.max())
    idx = np.arange(max(0, lo - NEIGH), min(n_words, hi + NEIGH + 1))
    idx = idx[(idx < lo) | (idx > hi)]
    same = groups.mass(P[idx], cat)
    ent = groups.entity_mass(P[idx]) - same
    o = P[idx, groups.o] if groups.o is not None else 1 - groups.entity_mass(P[idx])
    dist = np.where(idx < lo, lo - idx, idx - hi).astype(float)
    w = np.exp(-(dist ** 2) / (2 * PDM_R ** 2))
    n = max(1, len(idx))
    for g, vals in (("same", same), ("other", ent), ("o", o)):
        bins = np.minimum((vals * N_BINS).astype(int), N_BINS - 1)
        acc = np.zeros(N_BINS)
        for b, v, ww in zip(bins, vals, w):
            acc[b] += ww * v / n
        for b in range(N_BINS):
            out[f"p2_pdm_{g}_b{b}"] = float(acc[b])
    return out


def span_features(note: dict, span: dict, P: np.ndarray, spans_w: np.ndarray, groups: TagGroups,
                  mc: dict | None, all_spans: list[dict], note_stats: dict) -> dict:
    text = note["text"]
    s, e, cat = span["start"], span["end"], span["category"]
    f: dict[str, float | str] = {}
    idx = word_index(spans_w, s, e)
    n_words = len(spans_w)
    surface = text[s:e]

    # ---- paper 1: probability of the predicted label over the span's words
    if len(idx):
        Pw = P[idx]
        p_cat = groups.mass(Pw, cat)
        p_o = Pw[:, groups.o] if groups.o is not None else 1 - groups.entity_mass(Pw)
        p_max = Pw.max(1)
        f["p1_p_cat_mean"] = float(p_cat.mean()); f["p1_p_cat_min"] = float(p_cat.min())
        f["p1_p_cat_geo"] = float(np.exp(np.log(np.clip(p_cat, 1e-9, 1)).mean()))
        f["p1_p_o_mean"] = float(p_o.mean()); f["p1_p_o_max"] = float(p_o.max())
        f["p1_p_max_mean"] = float(p_max.mean()); f["p1_p_max_min"] = float(p_max.min())
        f["p1_frac_words_argmax_cat"] = float(np.mean([groups.mass(Pw[i:i + 1], cat)[0] >= 0.5 for i in range(len(idx))]))
    else:
        for k in ("p1_p_cat_mean", "p1_p_cat_min", "p1_p_cat_geo", "p1_p_o_mean", "p1_p_o_max", "p1_p_max_mean",
                  "p1_p_max_min", "p1_frac_words_argmax_cat"):
            f[k] = float("nan")
    f["p1_len_words"] = int(len(idx)); f["p1_len_chars"] = e - s
    # MC dropout (paper 1 "Var")
    if mc is not None and len(idx) and len(mc["P_mean"]) == n_words:
        Pm, Ps, am = mc["P_mean"][idx], mc["P_std"][idx], mc["argmax"][:, idx]
        pc_mean = groups.mass(Pm, cat)
        f["p1_mc_p_cat_mean"] = float(pc_mean.mean()); f["p1_mc_p_cat_min"] = float(pc_mean.min())
        cols = groups.cat_cols.get(cat, [])
        std_cat = np.sqrt((Ps[:, cols] ** 2).sum(1)) if cols else np.zeros(len(idx))
        f["p1_mc_std_cat_mean"] = float(std_cat.mean()); f["p1_mc_std_cat_max"] = float(std_cat.max())
        f["p1_mc_std_max_label"] = float(Ps[np.arange(len(idx)), P[idx].argmax(1)].mean())
        single = P[idx].argmax(1)
        f["p1_mc_agree"] = float((am == single[None, :]).mean())
        f["p1_mc_o_mean"] = float(Pm[:, groups.o].mean()) if groups.o is not None else float("nan")
    else:
        for k in ("p1_mc_p_cat_mean", "p1_mc_p_cat_min", "p1_mc_std_cat_mean", "p1_mc_std_cat_max",
                  "p1_mc_std_max_label", "p1_mc_agree", "p1_mc_o_mean"):
            f[k] = float("nan")

    # ---- paper 2: statistics and PDM
    if len(idx):
        Pw = P[idx]
        srt = np.sort(Pw, axis=1)
        top1, top2 = srt[:, -1], srt[:, -2]
        f["p2_entropy_mean"] = float(entropy(Pw).mean()); f["p2_entropy_max"] = float(entropy(Pw).max())
        f["p2_top_ratio_mean"] = float((top1 / np.clip(top2, 1e-9, None)).mean())
        f["p2_top_ratio_min"] = float((top1 / np.clip(top2, 1e-9, None)).min())
        f["p2_top_gap_mean"] = float((top1 - top2).mean()); f["p2_top_gap_min"] = float((top1 - top2).min())
        f["p2_cv_pmax"] = float(top1.std() / max(top1.mean(), 1e-9))
        ent_mass = groups.entity_mass(Pw)
        f["p2_frac_words_entity"] = float((ent_mass >= 0.5).mean())
        # neighbours
        lo, hi = int(idx.min()), int(idx.max())
        nb = np.arange(max(0, lo - NEIGH), min(n_words, hi + NEIGH + 1))
        nb = nb[(nb < lo) | (nb > hi)]
        if len(nb):
            Pn = P[nb]
            f["p2_nb_p_o_mean"] = float(Pn[:, groups.o].mean()) if groups.o is not None else float("nan")
            f["p2_nb_p_same_mean"] = float(groups.mass(Pn, cat).mean())
            f["p2_nb_p_same_max"] = float(groups.mass(Pn, cat).max())
            f["p2_nb_entity_frac"] = float((groups.entity_mass(Pn) >= 0.5).mean())
            f["p2_nb_entropy_mean"] = float(entropy(Pn).mean())
            # immediately adjacent words
            f["p2_prev_p_same"] = float(groups.mass(P[lo - 1:lo], cat)[0]) if lo > 0 else 0.0
            f["p2_next_p_same"] = float(groups.mass(P[hi + 1:hi + 2], cat)[0]) if hi + 1 < n_words else 0.0
        else:
            for k in ("p2_nb_p_o_mean", "p2_nb_p_same_mean", "p2_nb_p_same_max", "p2_nb_entity_frac",
                      "p2_nb_entropy_mean", "p2_prev_p_same", "p2_next_p_same"):
                f[k] = float("nan")
        f.update(pdm(P, groups, cat, idx, n_words))
    else:
        for k in ("p2_entropy_mean", "p2_entropy_max", "p2_top_ratio_mean", "p2_top_ratio_min", "p2_top_gap_mean",
                  "p2_top_gap_min", "p2_cv_pmax", "p2_frac_words_entity", "p2_nb_p_o_mean", "p2_nb_p_same_mean",
                  "p2_nb_p_same_max", "p2_nb_entity_frac", "p2_nb_entropy_mean", "p2_prev_p_same", "p2_next_p_same"):
            f[k] = float("nan")
        f.update(pdm(P, groups, cat, idx, n_words))
    f["p2_note_entropy_mean"] = note_stats["entropy_mean"]
    f["p2_note_entity_frac"] = note_stats["entity_frac"]

    # ---- ours
    src = span["source"]
    parts = set(src.split("|"))
    has_r = "regex" in parts
    has_m = any(p not in ("regex", "propagated") for p in parts)
    f["our_src_rules"] = int(has_r); f["our_src_model"] = int(has_m); f["our_src_both"] = int(has_r and has_m)
    f["our_src_propagated"] = int("propagated" in parts)
    f["our_rule_family"] = rule_family(span.get("rule"))
    f["our_rule"] = span.get("rule") or "none"
    f["our_category"] = cat
    f["our_score"] = span.get("score") if span.get("score") is not None else float("nan")
    # repetition of the surface string in the note
    key = surface.strip().lower()
    occ = len(re.findall(r"(?<!\w)" + re.escape(surface.strip()) + r"(?!\w)", text, flags=re.IGNORECASE)) if len(key) >= 3 else 1
    same_pred = sum(1 for o in all_spans if o is not span and text[o["start"]:o["end"]].strip().lower() == key)
    f["our_repeat_count"] = occ
    f["our_repeat_predicted"] = same_pred
    f["our_repeat_unpredicted"] = max(0, occ - 1 - same_pred)
    f["our_case"] = case_pattern(surface)
    f["our_has_digit"] = int(any(c.isdigit() for c in surface))
    f["our_frac_alpha"] = sum(c.isalpha() for c in surface) / max(1, len(surface))
    f["our_n_tokens"] = len(surface.split())
    pre = text[max(0, s - 40):s]
    f["our_after_header"] = int(bool(re.search(r"[A-Za-z][A-Za-z /()'’\-]{1,40}:\s*$", pre)))
    f["our_line_start"] = int(s == 0 or text[s - 1] == "\n" or pre.rstrip(" \t").endswith("\n"))
    f["our_in_header_block"] = int(text[:s].count("\n\n") <= 1)       # first paragraph(s) of the note
    f["our_rel_pos"] = s / max(1, len(text))
    f["our_lang"] = note.get("lang") or "unk"
    f["our_note_n_spans"] = len(all_spans)
    f["our_note_n_same_cat"] = sum(1 for o in all_spans if o["category"] == cat)
    return f


def targets(note: dict, span: dict) -> dict:
    s, e, cat = span["start"], span["end"], span["category"]
    gold = note["spans"]
    ov = [g for g in gold if g["start"] < e and s < g["end"]]
    inside = 0
    for g in ov:
        inside += min(e, g["end"]) - max(s, g["start"])
    frac = inside / max(1, e - s)
    is_phi = frac >= 0.5
    return {"y_overlap_any": int(bool(ov)), "y_is_phi": int(is_phi),
            "y_cat_ok": int(is_phi and any(CATEGORY[g["label"]] == cat for g in ov)),
            "y_exact": int(any(g["start"] == s and g["end"] == e and CATEGORY[g["label"]] == cat for g in ov)),
            "y_gold_label": next((g["label"] for g in ov), "none"), "y_frac_inside": frac}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--eval-tag", default="_v4")
    ap.add_argument("--system", default="rules+model")
    ap.add_argument("--out", default="results/features")
    a = ap.parse_args(argv)
    import pandas as pd
    from deidconf.detect import adapted_configs

    notes = {n["note_id"]: n for n in read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")}
    preds = read_jsonl(PROJECT_ROOT / f"results/eval/{a.split}{a.eval_tag}/{a.system}.predictions.jsonl")
    det_dir = PROJECT_ROOT / "results/detect" / a.split
    meta = json.loads((det_dir / "meta.json").read_text(encoding="utf-8"))
    _, models_cfg, labels_cfg = adapted_configs()
    spec = next(m for m in models_cfg["shortlist"] if m["key"] == models_cfg["selected"])
    groups = TagGroups(meta, labels_cfg["models"][spec["label_schema"]])
    mc_dir = PROJECT_ROOT / "results/mcdropout" / a.split

    rows = []
    n_mc = 0
    for p in preds:
        n = notes[p["note_id"]]
        z = np.load(det_dir / "probs" / f"{n['note_id']}.npz")
        P, spans_w = z["P"].astype(np.float32), z["spans"]
        mc = None
        mcp = mc_dir / f"{n['note_id']}.npz"
        if mcp.exists():
            zm = np.load(mcp)
            mc = {"P_mean": zm["P_mean"].astype(np.float32), "P_std": zm["P_std"].astype(np.float32), "argmax": zm["argmax"]}
            n_mc += 1
        note_stats = {"entropy_mean": float(entropy(P).mean()) if len(P) else float("nan"),
                      "entity_frac": float((groups.entity_mass(P) >= 0.5).mean()) if len(P) else float("nan")}
        for sp in p["spans"]:
            row = {"note_id": n["note_id"], "start": sp["start"], "end": sp["end"], "category": sp["category"],
                   "source": sp["source"], "rule": sp.get("rule") or "", "doc_type": n.get("doc_type"), "lang": n.get("lang")}
            row.update(span_features(n, sp, P, spans_w, groups, mc, p["spans"], note_stats))
            row.update(targets(n, sp))
            rows.append(row)
    df = pd.DataFrame(rows)
    out = PROJECT_ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{a.split}{a.eval_tag}.{a.system}.csv"
    df.to_csv(path, index=False)
    print(f"{len(df)} spans from {len(preds)} notes ({n_mc} with MC dropout) -> {path}")
    print("targets:", {k: int(df[k].sum()) for k in ("y_overlap_any", "y_is_phi", "y_cat_ok", "y_exact")})
    print("errors (not PHI):", int((df.y_is_phi == 0).sum()), "| wrong category:", int(((df.y_is_phi == 1) & (df.y_cat_ok == 0)).sum()),
          "| inexact:", int(((df.y_cat_ok == 1) & (df.y_exact == 0)).sum()))
    print("by source:", df.groupby(["our_src_rules", "our_src_model"]).y_is_phi.agg(["count", "mean"]).round(3).to_dict())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
