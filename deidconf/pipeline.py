"""End-to-end confidence-aware de-identification of new notes (the deliverable).

    python -m deidconf.pipeline --input notes.jsonl --out out.jsonl [--models results/models]
    python -m deidconf.pipeline --text "Patient: OKKES REILLY ..."

Per note: regex rules + OpenMed model -> fusion/post-processing -> per-span confidences (is PHI / category right /
exact) from the saved forecasters -> near-miss candidates and their missed-PHI probability -> note-level leak risk
-> actions -> de-identified text via the repo's policy engine.

Actions (thresholds are configuration, chosen on the calibration split):
  predicted span : confidence >= --review-below   -> "replace";  below -> "replace + review" (never deleted)
  near miss      : p_missed >= --add-at           -> "add as PHI" (replaced too); >= --flag-at -> "review"
Output JSON per note:
  {"note_id", "note_confidence", "expected_misses", "expected_false_alarms", "spans": [...], "possible_misses": [...],
   "deidentified_text"}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from deidconf import PROJECT_ROOT
from deidconf.data import read_jsonl
from deidconf.detect import adapted_configs, model_entities_from_P, score_words_full
from deidconf.evaluate import final_spans
from deidconf.features import TagGroups, entropy, span_features
from deidconf.nearmiss import cand_features, candidates_for_note

MODEL_FILES = {
    "is_phi": "results/confidence/cal_v5.rules+model.y_is_phi/model.joblib",
    "cat_ok": "results/confidence/cal_v5.rules+model.y_cat_ok/model.joblib",
    "exact": "results/confidence/cal_v5.rules+model.y_exact/model.joblib",
    "missed": "results/nearmiss/cal_v5/model.joblib",
}


class ConfidencePipeline:
    def __init__(self, model_files: dict[str, str] | None = None, threads: int = 4, review_below: float = 0.9,
                 add_at: float = 0.5, flag_at: float = 0.2, policy_key: bytes | None = None):
        import joblib
        from deid.config import load_yaml
        from deid.detectors.hf_detector import build_detector
        from deid.detectors.regex_detector import RegexDetector
        from deid.policies.transform import PolicyEngine
        self.cfg, models_cfg, labels_cfg = adapted_configs()
        self.regex = RegexDetector.from_config(self.cfg)
        self.model = build_detector(models_cfg["selected"], models_cfg, labels_cfg, self.cfg, deployment=False,
                                    threads=threads)
        meta = {"tags": self.model.tags, "o_index": self.model.o_index}
        spec = next(m for m in models_cfg["shortlist"] if m["key"] == models_cfg["selected"])
        self.groups = TagGroups(meta, labels_cfg["models"][spec["label_schema"]])
        self.forecasters = {k: joblib.load(PROJECT_ROOT / v) for k, v in (model_files or MODEL_FILES).items()
                            if (PROJECT_ROOT / v).exists()}
        missing = set((model_files or MODEL_FILES)) - set(self.forecasters)
        if missing:
            print(f"warning: no saved forecaster for {sorted(missing)}; those confidences will be absent", file=sys.stderr)
        self.policy = PolicyEngine(load_yaml(PROJECT_ROOT / "Deidentification/configs/deid_policy.yaml"), key=policy_key)
        self.review_below, self.add_at, self.flag_at = review_below, add_at, flag_at
        self.system = dict(regex=True, model=True, min_score=0.5)

    def _apply(self, name: str, rows: list[dict]) -> np.ndarray:
        fc = self.forecasters.get(name)
        if fc is None or not rows:
            return np.full(len(rows), np.nan)
        X = pd.DataFrame(rows)
        for c in fc["features"]:
            if c not in X:
                X[c] = np.nan
        return fc["model"].predict_proba(X[fc["features"]])[:, 1]

    def process(self, note_id: str, text: str, lang: str | None = None) -> dict:
        from deid.schema import Entity
        note = {"note_id": note_id, "text": text, "lang": lang or "unk", "spans": []}
        r_ents = [e.to_dict() for e in self.regex.detect(text)]
        sw = score_words_full(self.model, text)
        if sw is None:
            spans_w, P, m_ents = np.zeros((0, 2), int), np.zeros((0, len(self.model.tags)), np.float32), []
        else:
            spans_w, P = sw
            m_ents = [e.to_dict() for e in model_entities_from_P(self.model, text, spans_w, P)]
            spans_w = np.asarray(spans_w, dtype=int).reshape(-1, 2)
        spans = final_spans(text, r_ents, m_ents, self.cfg, self.system)
        note_stats = {"entropy_mean": float(entropy(P).mean()) if len(P) else float("nan"),
                      "entity_frac": float((self.groups.entity_mass(P) >= 0.5).mean()) if len(P) else float("nan")}
        feat_rows = [span_features(note, s, P, spans_w, self.groups, None, spans, note_stats) for s in spans]
        conf = {k: self._apply(k, feat_rows) for k in ("is_phi", "cat_ok", "exact")}
        out_spans = []
        for i, s in enumerate(spans):
            c = {k: (None if np.isnan(v[i]) else round(float(v[i]), 3)) for k, v in conf.items()}
            main = c["is_phi"] if c["is_phi"] is not None else 1.0
            out_spans.append({"start": s["start"], "end": s["end"], "text": text[s["start"]:s["end"]],
                              "category": s["category"], "label": s["label"], "source": s["source"], "rule": s.get("rule"),
                              "confidence": c, "action": "replace" if main >= self.review_below else "replace + review"})
        cands = candidates_for_note(note, spans, P, spans_w, self.groups,
                                    self.forecasters.get("missed", {}).get("tau", 0.02))
        c_rows = [cand_features(note, c, spans, P, spans_w, self.groups, None) for c in cands]
        p_missed = self._apply("missed", c_rows)
        misses = []
        added = []
        for c, p in zip(cands, p_missed):
            p = None if np.isnan(p) else float(p)
            if p is None or p < self.flag_at:
                continue
            action = "add as PHI" if p >= self.add_at else "review"
            misses.append({"start": c["start"], "end": c["end"], "text": text[c["start"]:c["end"]],
                           "category": c["category"], "source": c["source"], "p_missed": round(p, 3), "action": action})
            if action == "add as PHI":
                added.append(c)
        pm = np.nan_to_num(p_missed, nan=0.0)
        remaining = [p for p, c in zip(pm, cands) if c not in added]
        note_conf = float(np.prod([1 - min(1.0, p) for p in remaining])) if remaining else 1.0
        # de-identify: predicted spans + added near-misses through the repo's policy engine
        ents = [Entity(s["start"], s["end"], s["label"], source=s["source"], score=s.get("score")) for s in spans]
        cat_to_label = {"Name": "PERSON", "Address_Location": "LOCATION", "Organization": "ORGANIZATION", "ID": "ID",
                        "Date": "DATE", "Age_Birthdate": "AGE", "Contactdetails": "PHONE", "Profession": "PROFESSION",
                        "Other": "OTHER_PHI"}
        for c in added:
            ents.append(Entity(c["start"], c["end"], cat_to_label.get(c["category"], "OTHER_PHI"), source="nearmiss"))
        ents = sorted({(e.start, e.end): e for e in ents}.values(), key=lambda e: e.start)
        merged = []
        for e in ents:                      # drop overlaps (keep the earlier/longer one)
            if merged and e.start < merged[-1].end:
                continue
            merged.append(e)
        deid = self.policy.transform(text, merged, note_id, None).text
        return {"note_id": note_id, "note_confidence": round(note_conf, 3),
                "expected_misses": round(float(sum(remaining)), 2) if remaining else 0.0,
                "expected_false_alarms": round(float(np.nansum([1 - (s["confidence"]["is_phi"] or 1.0) for s in out_spans])), 2),
                "n_spans": len(out_spans), "n_review": sum(s["action"] != "replace" for s in out_spans),
                "spans": out_spans, "possible_misses": misses, "deidentified_text": deid}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", help="JSONL with note_id, text[, lang] (gold spans ignored)")
    ap.add_argument("--text", help="one note as a string")
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--review-below", type=float, default=0.9)
    ap.add_argument("--add-at", type=float, default=0.5)
    ap.add_argument("--flag-at", type=float, default=0.2)
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args(argv)
    pipe = ConfidencePipeline(threads=a.threads, review_below=a.review_below, add_at=a.add_at, flag_at=a.flag_at)
    if a.text:
        print(json.dumps(pipe.process("note-1", a.text), indent=1, ensure_ascii=False))
        return 0
    notes = read_jsonl(a.input)
    if a.limit:
        notes = notes[:a.limit]
    sink = open(a.out, "w", encoding="utf-8") if a.out else sys.stdout
    for n in notes:
        sink.write(json.dumps(pipe.process(n["note_id"], n["text"], n.get("lang")), ensure_ascii=False) + "\n")
    if a.out:
        sink.close()
        print(f"wrote {len(notes)} notes to {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
