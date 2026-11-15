"""Step 6 (our addition): near-miss candidates, the missed-PHI forecaster and the note-level leak risk.

    python -m deidconf.nearmiss --split cal --eval-tag _v4 --system rules+model

Both papers only score what the detector predicted. Here we also score what it did NOT predict:
  candidates  (a) runs of words outside every predicted span whose total PHI probability mass >= tau
                  (the model "considered" them: second-best readings, weak activations)
              (b) other occurrences, in the same note, of a string that was predicted as PHI elsewhere
                  (names are repeated; an inconsistent tag is suspicious)
  target      y_missed = the candidate contains gold-PHI characters that no predicted span covers
  features    the same families as for predicted spans (model probability, uncertainty, PDM neighbourhood,
              context), plus candidate source and distance to the nearest predicted span
  forecaster  GBDT, out-of-fold by note; baseline = raw PHI mass
  note risk   P(at least one miss in the note) = 1 - prod(1 - p_i); expected misses = sum p_i
  re-scoring  candidates with p >= theta are added as PHI (paper 1's re-scoring idea applied to recall)
Outputs results/nearmiss/<split><tag>/{candidates.csv, metrics.json, report.md, note_risk.csv}.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict

import numpy as np
import pandas as pd

from deidconf import PROJECT_ROOT
from deidconf.data import read_jsonl
from deidconf.features import NEIGH, TagGroups, case_pattern, entropy, pdm, word_index

TAU = 0.02
MIN_LEN = 2


def covered_mask(n: int, spans) -> np.ndarray:
    m = np.zeros(n, dtype=bool)
    for s in spans:
        m[s["start"]:s["end"]] = True
    return m


def candidates_for_note(note: dict, pred: list[dict], P: np.ndarray, spans_w: np.ndarray, groups: TagGroups,
                        tau: float) -> list[dict]:
    text = note["text"]
    cov = covered_mask(len(text), pred)
    cands: list[dict] = []
    if len(P):
        ent = groups.entity_mass(P)
        word_cov = np.array([cov[a:b].any() for a, b in spans_w])
        hot = (ent >= tau) & ~word_cov
        # (a) merge consecutive hot words (gap of at most one non-hot, uncovered word)
        i = 0
        while i < len(hot):
            if not hot[i]:
                i += 1
                continue
            j = i
            while j + 1 < len(hot) and (hot[j + 1] or (j + 2 < len(hot) and hot[j + 2] and not word_cov[j + 1])):
                j += 1
            s, e = int(spans_w[i][0]), int(spans_w[j][1])
            if e - s >= MIN_LEN and re.search(r"[^\W_]", text[s:e]):
                cat_mass = {c: float(groups.mass(P[i:j + 1], c).sum()) for c in groups.cat_cols}
                best = max(cat_mass, key=cat_mass.get) if cat_mass else "Other"
                cands.append({"start": s, "end": e, "category": best, "source": "prob", "wi": i, "wj": j})
            i = j + 1
    # (b) repeats of predicted strings
    for p in pred:
        surf = text[p["start"]:p["end"]].strip()
        if len(surf) < 3 or not re.search(r"[A-Za-z]", surf) or surf.lower() in ("the", "and"):
            continue
        for m in re.finditer(r"(?<!\w)" + re.escape(surf) + r"(?!\w)", text, flags=re.IGNORECASE):
            if cov[m.start():m.end()].any():
                continue
            idx = word_index(spans_w, m.start(), m.end())
            cands.append({"start": m.start(), "end": m.end(), "category": p["category"], "source": "repeat",
                          "wi": int(idx.min()) if len(idx) else -1, "wj": int(idx.max()) if len(idx) else -1})
    # merge overlapping candidates
    cands.sort(key=lambda c: (c["start"], c["end"]))
    merged: list[dict] = []
    for c in cands:
        if merged and c["start"] < merged[-1]["end"]:
            m = merged[-1]
            m["end"] = max(m["end"], c["end"])
            m["source"] = "+".join(sorted(set(m["source"].split("+")) | {c["source"]}))
            m["wj"] = max(m["wj"], c["wj"])
            if m["wi"] < 0:
                m["wi"] = c["wi"]
        else:
            merged.append(dict(c))
    return merged


def cand_features(note: dict, c: dict, pred: list[dict], P: np.ndarray, spans_w: np.ndarray, groups: TagGroups,
                  mc: dict | None) -> dict:
    text = note["text"]
    s, e, cat = c["start"], c["end"], c["category"]
    f: dict = {}
    idx = word_index(spans_w, s, e)
    n_words = len(spans_w)
    surface = text[s:e]
    if len(idx):
        Pw = P[idx]
        ent = groups.entity_mass(Pw)
        f["p1_ent_mean"] = float(ent.mean()); f["p1_ent_max"] = float(ent.max()); f["p1_ent_sum"] = float(ent.sum())
        f["p1_p_cat_mean"] = float(groups.mass(Pw, cat).mean()); f["p1_p_cat_max"] = float(groups.mass(Pw, cat).max())
        po = Pw[:, groups.o] if groups.o is not None else 1 - ent
        f["p1_p_o_min"] = float(po.min()); f["p1_p_o_mean"] = float(po.mean())
        srt = np.sort(Pw, axis=1)
        f["p2_entropy_mean"] = float(entropy(Pw).mean()); f["p2_entropy_max"] = float(entropy(Pw).max())
        f["p2_top_gap_min"] = float((srt[:, -1] - srt[:, -2]).min())
        f["p2_top_ratio_min"] = float((srt[:, -1] / np.clip(srt[:, -2], 1e-9, None)).min())
        lo, hi = int(idx.min()), int(idx.max())
        nb = np.arange(max(0, lo - NEIGH), min(n_words, hi + NEIGH + 1))
        nb = nb[(nb < lo) | (nb > hi)]
        if len(nb):
            f["p2_nb_entity_frac"] = float((groups.entity_mass(P[nb]) >= 0.5).mean())
            f["p2_nb_p_same_mean"] = float(groups.mass(P[nb], cat).mean())
            f["p2_nb_entropy_mean"] = float(entropy(P[nb]).mean())
        else:
            f["p2_nb_entity_frac"] = f["p2_nb_p_same_mean"] = f["p2_nb_entropy_mean"] = float("nan")
        f.update(pdm(P, groups, cat, idx, n_words))
        if mc is not None and len(mc["P_mean"]) == n_words:
            Pm, Ps, am = mc["P_mean"][idx], mc["P_std"][idx], mc["argmax"][:, idx]
            f["p1_mc_ent_mean"] = float(groups.entity_mass(Pm).mean())
            f["p1_mc_ent_max"] = float(groups.entity_mass(Pm).max())
            f["p1_mc_std_o"] = float(Ps[:, groups.o].mean()) if groups.o is not None else float("nan")
            f["p1_mc_frac_pass_entity"] = float((am != groups.o).mean()) if groups.o is not None else float("nan")
        else:
            for k in ("p1_mc_ent_mean", "p1_mc_ent_max", "p1_mc_std_o", "p1_mc_frac_pass_entity"):
                f[k] = float("nan")
    else:
        for k in ("p1_ent_mean", "p1_ent_max", "p1_ent_sum", "p1_p_cat_mean", "p1_p_cat_max", "p1_p_o_min", "p1_p_o_mean",
                  "p2_entropy_mean", "p2_entropy_max", "p2_top_gap_min", "p2_top_ratio_min", "p2_nb_entity_frac",
                  "p2_nb_p_same_mean", "p2_nb_entropy_mean", "p1_mc_ent_mean", "p1_mc_ent_max", "p1_mc_std_o",
                  "p1_mc_frac_pass_entity"):
            f[k] = float("nan")
        f.update(pdm(P, groups, cat, idx, n_words))
    f["our_src_prob"] = int("prob" in c["source"]); f["our_src_repeat"] = int("repeat" in c["source"])
    f["our_category"] = cat
    f["our_len_chars"] = e - s; f["our_n_tokens"] = len(surface.split()); f["our_len_words"] = int(len(idx))
    f["our_case"] = case_pattern(surface)
    f["our_has_digit"] = int(any(ch.isdigit() for ch in surface))
    f["our_frac_alpha"] = sum(ch.isalpha() for ch in surface) / max(1, len(surface))
    pre = text[max(0, s - 40):s]
    f["our_after_header"] = int(bool(re.search(r"[A-Za-z][A-Za-z /()'’\-]{1,40}:\s*$", pre)))
    f["our_line_start"] = int(s == 0 or text[s - 1] == "\n")
    f["our_sentence_start"] = int(bool(re.search(r"(?:^|[.!?]\s+)$", pre)))
    f["our_rel_pos"] = s / max(1, len(text))
    f["our_in_header_block"] = int(text[:s].count("\n\n") <= 1)
    key = surface.strip().lower()
    f["our_repeat_predicted"] = sum(1 for p in pred if text[p["start"]:p["end"]].strip().lower() == key)
    f["our_repeat_total"] = len(re.findall(r"(?<!\w)" + re.escape(surface.strip()) + r"(?!\w)", text, flags=re.IGNORECASE)) if len(key) >= 3 else 1
    # nearest predicted span
    dists = [min(abs(p["start"] - e), abs(s - p["end"])) for p in pred]
    j = int(np.argmin(dists)) if dists else -1
    f["our_dist_nearest_pred"] = int(dists[j]) if dists else 10_000
    f["our_nearest_pred_same_cat"] = int(pred[j]["category"] == cat) if dists else 0
    f["our_note_n_pred"] = len(pred)
    f["our_lang"] = note.get("lang") or "unk"
    # a capitalised word not at sentence start (name-like) / looks like an id / looks like a date
    f["our_titlecase_mid"] = int(bool(re.match(r"[A-Z][a-z]", surface)) and not f["our_sentence_start"])
    f["our_idlike"] = int(bool(re.fullmatch(r"[A-Z0-9][A-Z0-9 /\-]{4,}", surface)) and any(ch.isdigit() for ch in surface))
    return f


def target(note: dict, c: dict, cov: np.ndarray) -> dict:
    s, e = c["start"], c["end"]
    gold = note["spans"]
    missed_chars = 0
    lab = "none"
    for g in gold:
        a, b = max(s, g["start"]), min(e, g["end"])
        if a < b:
            k = int((~cov[a:b]).sum())
            if k:
                missed_chars += k
                lab = g["label"]
    return {"y_missed": int(missed_chars > 0), "y_missed_chars": missed_chars, "y_gold_label": lab}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="cal")
    ap.add_argument("--eval-tag", default="_v4")
    ap.add_argument("--system", default="rules+model")
    ap.add_argument("--tau", type=float, default=TAU)
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--save", action="store_true", help="save the 'all' forecaster fitted on every candidate")
    ap.add_argument("--apply", default=None, help="saved model.joblib: score candidates with it, no fitting (test run)")
    a = ap.parse_args(argv)
    from deidconf.confidence import CATEGORICAL, ece, make_pipeline
    from deidconf.detect import adapted_configs
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.model_selection import GroupKFold

    notes = {n["note_id"]: n for n in read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")}
    preds = read_jsonl(PROJECT_ROOT / f"results/eval/{a.split}{a.eval_tag}/{a.system}.predictions.jsonl")
    det_dir = PROJECT_ROOT / "results/detect" / a.split
    meta = json.loads((det_dir / "meta.json").read_text(encoding="utf-8"))
    _, models_cfg, labels_cfg = adapted_configs()
    spec = next(m for m in models_cfg["shortlist"] if m["key"] == models_cfg["selected"])
    groups = TagGroups(meta, labels_cfg["models"][spec["label_schema"]])
    mc_dir = PROJECT_ROOT / "results/mcdropout" / a.split
    out = PROJECT_ROOT / "results/nearmiss" / f"{a.split}{a.eval_tag}"
    out.mkdir(parents=True, exist_ok=True)

    rows, note_rows = [], []
    gold_missed_total = gold_missed_with_cand = 0
    uncovered_examples: dict[str, list[str]] = defaultdict(list)
    uncovered_counts: dict[str, int] = defaultdict(int)
    uncovered_mass: dict[str, list[float]] = defaultdict(list)
    for p in preds:
        n = notes[p["note_id"]]
        text = n["text"]
        z = np.load(det_dir / "probs" / f"{n['note_id']}.npz")
        P, spans_w = z["P"].astype(np.float32), z["spans"]
        mc = None
        if (mc_dir / f"{n['note_id']}.npz").exists():
            zm = np.load(mc_dir / f"{n['note_id']}.npz")
            mc = {"P_mean": zm["P_mean"].astype(np.float32), "P_std": zm["P_std"].astype(np.float32), "argmax": zm["argmax"]}
        cov_raw = covered_mask(len(text), p["spans"])
        cands = candidates_for_note(n, p["spans"], P, spans_w, groups, a.tau)
        # a miss = an uncovered LETTER or DIGIT of a gold span; a space between two predicted pieces is not a leak
        alnum = np.fromiter((ch.isalnum() for ch in text), dtype=bool, count=len(text))
        cov = cov_raw | ~alnum
        missed_gold = [g for g in n["spans"] if (~cov[g["start"]:g["end"]]).any()]
        gold_missed_total += len(missed_gold)
        for g in missed_gold:
            has = any(c["start"] < g["end"] and g["start"] < c["end"]
                      and (~cov[max(c["start"], g["start"]):min(c["end"], g["end"])]).any() for c in cands)
            if has:
                gold_missed_with_cand += 1
            else:
                uncovered_counts[g["label"]] += 1
                widx = word_index(spans_w, g["start"], g["end"])
                mass = float(groups.entity_mass(P[widx]).max()) if len(widx) and len(P) else 0.0
                uncovered_mass[g["label"]].append(mass)
                if len(uncovered_examples[g["label"]]) < 12:
                    a0, b0 = g["start"], g["end"]
                    uncovered_examples[g["label"]].append(
                        f"{text[max(0, a0 - 35):a0]}⟦{text[a0:b0]}⟧{text[b0:b0 + 35]}".replace("\n", "⏎") + f"  (max PHI mass {mass:.3f})")
        note_rows.append({"note_id": n["note_id"], "n_cands": len(cands), "n_pred": len(p["spans"]),
                          "n_missed_gold": len(missed_gold), "missed_chars": int(sum((~cov[g["start"]:g["end"]]).sum() for g in n["spans"])),
                          "lang": n.get("lang"), "doc_type": n.get("doc_type")})
        for c in cands:
            row = {"note_id": n["note_id"], "start": c["start"], "end": c["end"], "category": c["category"],
                   "source": c["source"], "text_len": c["end"] - c["start"]}
            row.update(cand_features(n, c, p["spans"], P, spans_w, groups, mc))
            row.update(target(n, c, cov))
            rows.append(row)
    df = pd.DataFrame(rows)
    notes_df = pd.DataFrame(note_rows)
    df.to_csv(out / "candidates.csv", index=False)
    y = df["y_missed"].to_numpy().astype(int)
    print(f"{len(df)} candidates in {len(preds)} notes; {int(y.sum())} contain missed PHI "
          f"({100 * y.mean():.1f}%). Missed gold spans: {gold_missed_total}, with a candidate: {gold_missed_with_cand} "
          f"({100 * gold_missed_with_cand / max(1, gold_missed_total):.0f}%)")
    print("candidates by source:", df.source.value_counts().to_dict(), "| positives by source:",
          df[df.y_missed == 1].source.value_counts().to_dict())

    # ---- forecaster, out-of-fold by note
    feats = [c for c in df.columns if c.startswith(("p1_", "p2_", "our_"))]
    has_mc = df["p1_mc_ent_mean"].notna().mean() > 0.5
    if not has_mc:
        feats = [c for c in feats if "_mc_" not in c]
    sets = {"raw_mass": None, "p1": [c for c in feats if c.startswith("p1_")],
            "p1+p2": [c for c in feats if c.startswith(("p1_", "p2_"))], "all": feats}
    groups_arr = df["note_id"].to_numpy()
    gkf = GroupKFold(n_splits=a.folds)
    oof: dict[str, np.ndarray] = {}
    if a.apply:
        import joblib
        saved = joblib.load(PROJECT_ROOT / a.apply)
        for c in saved["features"]:
            if c not in df:
                df[c] = np.nan
        oof["raw_mass"] = df["p1_ent_max"].fillna(0).to_numpy()
        oof["all"] = saved["model"].predict_proba(df[saved["features"]])[:, 1]
        sets = {"raw_mass": None, "all": saved["features"]}
        print(f"applied {a.apply} (fitted on {saved['n_train']} candidates)")
    for name, cols in sets.items():
        if name in oof:
            continue
        if cols is None:
            oof[name] = df["p1_ent_max"].fillna(0).to_numpy()
            continue
        o = np.full(len(df), np.nan)
        for tr, te in gkf.split(df, y, groups_arr):
            pipe = make_pipeline("gbdt", cols, a.seed).fit(df.iloc[tr][cols], y[tr])
            o[te] = pipe.predict_proba(df.iloc[te][cols])[:, 1]
        oof[name] = o
    metrics = {}
    for name, p in oof.items():
        p = np.nan_to_num(p, nan=0.0)
        order = np.argsort(-p)
        m = {"auroc": float(roc_auc_score(y, p)) if 0 < y.sum() < len(y) else float("nan"),
             "auprc": float(average_precision_score(y, p)), "ece": ece(np.clip(p, 0, 1), y) if cols is not None else None}
        for b in (0.05, 0.10, 0.20):
            k = max(1, int(round(b * len(p))))
            m[f"missed_found@{int(b * 100)}%cands"] = float(y[order[:k]].sum() / max(1, y.sum()))
        # re-scoring: add candidates with p >= theta; report precision of added, gain in missed spans found
        for theta in (0.5, 0.3, 0.2):
            add = p >= theta
            m[f"add@{theta}"] = {"added": int(add.sum()), "true_missed": int(y[add].sum()),
                                 "precision": float(y[add].mean()) if add.any() else None,
                                 "missed_gold_recovered_frac": float(y[add].sum() / max(1, y.sum()))}
        metrics[name] = m
        print(f"{name:10s} AUROC {m['auroc']:.3f} AUPRC {m['auprc']:.3f} found@10% {m['missed_found@10%cands']:.2f} "
              f"add@0.5: {m['add@0.5']}")

    if a.save:
        import joblib
        full = make_pipeline("gbdt", sets["all"], a.seed).fit(df[sets["all"]], y)
        joblib.dump({"features": sets["all"], "model": full, "tau": a.tau, "n_train": int(len(df))}, out / "model.joblib")
        print(f"saved {out / 'model.joblib'}")

    # ---- note-level leak risk
    p_all = np.nan_to_num(oof["all"], nan=0.0)
    df["p_missed"] = p_all
    agg = df.groupby("note_id").p_missed.agg(expected_misses="sum", p_any=lambda s: 1 - np.prod(1 - np.clip(s, 0, 1)),
                                             max_p="max").reset_index()
    nd = notes_df.merge(agg, on="note_id", how="left").fillna({"expected_misses": 0.0, "p_any": 0.0, "max_p": 0.0})
    nd["has_miss"] = (nd.n_missed_gold > 0).astype(int)
    nd.to_csv(out / "note_risk.csv", index=False)
    note_m = {"notes": int(len(nd)), "notes_with_miss": int(nd.has_miss.sum()),
              "auroc_p_any": float(roc_auc_score(nd.has_miss, nd.p_any)) if 0 < nd.has_miss.sum() < len(nd) else float("nan"),
              "auroc_baseline_ncands": float(roc_auc_score(nd.has_miss, nd.n_cands)) if 0 < nd.has_miss.sum() < len(nd) else float("nan"),
              "ece_p_any": ece(nd.p_any.to_numpy(), nd.has_miss.to_numpy())}
    order = np.argsort(-nd.p_any.to_numpy())
    tot_missed = nd.n_missed_gold.sum()
    for b in (0.05, 0.10, 0.20):
        k = max(1, int(round(b * len(nd))))
        note_m[f"missed_spans_in_top{int(b * 100)}%notes"] = float(nd.n_missed_gold.to_numpy()[order[:k]].sum() / max(1, tot_missed))
    print("note level:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in note_m.items()})

    summary = {"split": a.split, "tag": a.eval_tag, "tau": a.tau, "n_candidates": int(len(df)), "n_positive": int(y.sum()),
               "gold_missed_spans": gold_missed_total, "gold_missed_with_candidate": gold_missed_with_cand,
               "has_mc_dropout": bool(has_mc), "span_level": metrics, "note_level": note_m}
    (out / "metrics.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    L = [f"# Missed-PHI candidates and note-level risk: `{a.split}{a.eval_tag}`", "",
         f"{len(df)} candidates (tau={a.tau}) in {len(preds)} notes; {int(y.sum())} contain missed PHI. "
         f"Gold spans with uncovered characters: {gold_missed_total}; {gold_missed_with_cand} of them have a candidate "
         f"({100 * gold_missed_with_cand / max(1, gold_missed_total):.0f}% candidate coverage).", "",
         "| Forecaster | AUROC | AUPRC | missed found @5% | @10% | @20% of candidates | add p≥0.5: added / true / precision |",
         "|---|---|---|---|---|---|---|"]
    for name, m in metrics.items():
        a5 = m["add@0.5"]
        L.append(f"| {name} | {m['auroc']:.3f} | {m['auprc']:.3f} | {100 * m['missed_found@5%cands']:.0f}% | "
                 f"{100 * m['missed_found@10%cands']:.0f}% | {100 * m['missed_found@20%cands']:.0f}% | "
                 f"{a5['added']} / {a5['true_missed']} / {('%.0f%%' % (100 * a5['precision'])) if a5['precision'] is not None else '–'} |")
    L += ["", "## Note-level leak risk  P(≥1 miss) = 1 − Π(1 − p_i)", "",
          f"- notes with at least one missed gold span: {note_m['notes_with_miss']} of {note_m['notes']}",
          f"- AUROC of P(≥1 miss): **{note_m['auroc_p_any']:.3f}** (baseline: number of candidates {note_m['auroc_baseline_ncands']:.3f})",
          f"- ECE of P(≥1 miss): {note_m['ece_p_any']:.4f}",
          f"- reviewing the riskiest 5 / 10 / 20 % of notes finds {100 * note_m['missed_spans_in_top5%notes']:.0f}% / "
          f"{100 * note_m['missed_spans_in_top10%notes']:.0f}% / {100 * note_m['missed_spans_in_top20%notes']:.0f}% of all missed PHI spans"]
    L += ["", "## Missed gold spans WITHOUT any candidate (the coverage gap)", ""]
    for lab, cnt in sorted(uncovered_counts.items(), key=lambda kv: -kv[1]):
        ms = uncovered_mass[lab]
        L += [f"### {lab}: {cnt} (max PHI mass: median {np.median(ms):.3f}, ≥0.005 in {100 * np.mean(np.array(ms) >= 0.005):.0f}%)", ""]
        L += [f"- {e}" for e in uncovered_examples[lab]] + [""]
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
