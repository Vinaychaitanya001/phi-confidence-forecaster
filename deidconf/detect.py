"""Run the existing detectors (repo regex rules + OpenMed FastClinical-82M, as published) on a MedDeID split and
cache everything the confidence layer will need. No training. Fusion / post-processing are NOT applied here: they
are cheap and are run offline in evaluation so that several configurations can be compared from one model pass.

    python -m deidconf.detect --split cal            (resumable; ~4 s per note on CPU)

Per note it stores
  results/detect/<split>/entities.jsonl   {"note_id", "regex": [Entity...], "model": [Entity...], "seconds": ...}
  results/detect/<split>/probs/<note_id>.npz   P: (n_words, n_tags) float16 full softmax per word (first sub-token),
                                               spans: (n_words, 2) char offsets of each word
  results/detect/<split>/meta.json        model tags, label map, adapted configuration

Configuration adapted to MedDeID's annotation guideline (settings only, see PLAN.md 2):
  regex.age_min = 0            every age is PHI (the repo's HIPAA default keeps only >= 90)
  postprocess.min_model_score = None   keep every model span; the 0.5 cut-off is evaluated offline as a baseline
  postprocess.strip_person_titles = False   MedDeID keeps "Dr" inside caregiver names
  postprocess.drop_state_names = False      anything smaller than a country is PHI in MedDeID
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np

from deidconf import PROJECT_ROOT
from deidconf.data import read_jsonl

REPO = PROJECT_ROOT / "Deidentification"


def adapted_configs():
    from deid.config import load_labels, load_yaml
    det = load_yaml(REPO / "configs/detection.yaml")
    det.setdefault("regex", {})["age_min"] = 0
    det["regex"]["rule_sets"] = ["meddeid"]                     # MedDeID-specific regex rules
    det["regex"]["disabled_rules"] = sorted(set(det["regex"].get("disabled_rules") or []) | {"organization", "name_field"})
    # the repo's generic "<words> Hospital/Laboratory/Clinic" rule fires on section headings ("NHS LABORATORY REPORT")
    fus = det.setdefault("fusion", {})
    fus["regex_trusted_categories"] = sorted(set(fus.get("regex_trusted_categories") or []) | {"PROFESSION"})
    fus["propagate_repeats"] = True                              # other exact occurrences of a detected name are PHI too
    pp = det.setdefault("postprocess", {})
    pp["min_model_score"] = None
    pp["strip_person_titles"] = False
    pp["drop_state_names"] = False
    pp["age_strip_old"] = True                                   # "42-year-old" -> "42-year" (guideline)
    pp["drop_impossible_dates"] = True                           # "31/04/2025" is a listed hard negative
    models = load_yaml(REPO / "configs/models.yaml")
    labels = load_labels(REPO / "configs/labels.yaml")
    return det, models, labels


def baseline_configs():
    """The repo's shipped rules and settings, only adapted to the MedDeID guideline (the 'as shipped' baseline that
    was scored on cal before any MedDeID rule existed): all ages, titles kept, states kept, no model-score cut."""
    from deid.config import load_labels, load_yaml
    det = load_yaml(REPO / "configs/detection.yaml")
    det.setdefault("regex", {})["age_min"] = 0
    pp = det.setdefault("postprocess", {})
    pp["min_model_score"] = None
    pp["strip_person_titles"] = False
    pp["drop_state_names"] = False
    models = load_yaml(REPO / "configs/models.yaml")
    labels = load_labels(REPO / "configs/labels.yaml")
    return det, models, labels


def score_words_full(det, text: str):
    """Same word scoring as HFTokenClassifier.score_words, but returns the FULL probability matrix.
    Returns (spans [(start,end)], P (n_words, n_tags) float32) in original-text offsets, or None."""
    from deid.detectors.hf_detector import text_words
    from deid.preprocessing.normalize import normalize
    if not text or not text.strip():
        return None
    nt = normalize(text) if det.normalize_text else None
    work = nt.text if nt else text
    enc = det.tokenizer(work, add_special_tokens=False, return_offsets_mapping=True,
                        return_attention_mask=False, return_token_type_ids=False, verbose=False)
    ids, offsets = enc["input_ids"], enc["offset_mapping"]
    if not ids:
        return None
    probs = det._token_probs(ids)
    if det.word_unit == "text":
        tw = text_words(work)
        word_ids = det.text_word_ids(offsets, tw, work)
    else:
        word_ids = enc.word_ids()
    first_tok: dict[int, int] = {}
    last_tok: dict[int, int] = {}
    for t, w in enumerate(word_ids):
        if w is None:
            continue
        first_tok.setdefault(w, t)
        last_tok[w] = t
    words = sorted(first_tok)
    spans = [tw[w] for w in words] if det.word_unit == "text" else \
        [(offsets[first_tok[w]][0], offsets[last_tok[w]][1]) for w in words]
    if nt is not None and not nt.is_identity_mapping:
        spans = [nt.to_original(a, b) for a, b in spans]
    P = probs[[first_tok[w] for w in words]] if words else np.zeros((0, len(det.tags)), np.float32)
    return [tuple(map(int, s)) for s in spans], P.astype(np.float32)


def model_entities_from_P(det, text: str, spans, P):
    """Decode entities from a full probability matrix with the repo's own decision rule and post-processing."""
    from deid.detectors.hf_detector import WordScores, entities_from_word_scores
    if len(P) == 0:
        return []
    am = P.argmax(1)
    rows = np.arange(len(P))
    if det.o_index is not None:
        p_o = P[:, det.o_index]
        Q = P.copy()
        Q[:, det.o_index] = -1.0
        nb = Q.argmax(1)
    else:
        p_o, nb = np.zeros(len(P)), am
    ws = WordScores(spans=list(spans), p_o=p_o.tolist(), am=am.tolist(), am_p=P[rows, am].tolist(),
                    nb=nb.tolist(), nb_p=P[rows, nb].tolist())
    params = det.decode_params()
    params["normalize_text"] = False  # spans are already in original offsets
    return entities_from_word_scores(text, ws, **params)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="cal", choices=["cal", "test", "train"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--out", default="results/detect")
    a = ap.parse_args(argv)

    from deid.detectors.hf_detector import build_detector
    from deid.detectors.regex_detector import RegexDetector

    det_cfg, models_cfg, labels_cfg = adapted_configs()
    out = PROJECT_ROOT / a.out / a.split
    (out / "probs").mkdir(parents=True, exist_ok=True)
    notes = read_jsonl(PROJECT_ROOT / f"data/meddeid/{a.split}.jsonl")
    if a.limit:
        notes = notes[:a.limit]

    done = set()
    ent_path = out / "entities.jsonl"
    if ent_path.exists():
        done = {json.loads(l)["note_id"] for l in open(ent_path, encoding="utf-8") if l.strip()}
    todo = [n for n in notes if n["note_id"] not in done]
    print(f"{a.split}: {len(notes)} notes, {len(done)} already done, {len(todo)} to run", flush=True)
    if not todo:
        return 0

    regex = RegexDetector.from_config(det_cfg)
    model = build_detector(models_cfg["selected"], models_cfg, labels_cfg, det_cfg, deployment=False,
                           threads=a.threads)
    (out / "meta.json").write_text(json.dumps({
        "model": model.describe(), "tags": model.tags, "label_map": model.label_map, "o_index": model.o_index,
        "decode_params": {k: v for k, v in model.decode_params().items() if k not in ("tags", "label_map")},
        "detection_cfg": det_cfg, "regex_rules": [r.name for r in regex.rules]}, indent=1, default=str),
        encoding="utf-8")

    t_start = time.perf_counter()
    with open(ent_path, "a", encoding="utf-8") as f:
        for i, n in enumerate(todo, 1):
            text = n["text"]
            t0 = time.perf_counter()
            r_ents = regex.detect(text)
            t1 = time.perf_counter()
            sw = score_words_full(model, text)
            if sw is None:
                spans, P, m_ents = [], np.zeros((0, len(model.tags)), np.float32), []
            else:
                spans, P = sw
                m_ents = model_entities_from_P(model, text, spans, P)
            t2 = time.perf_counter()
            np.savez_compressed(out / "probs" / f"{n['note_id']}.npz", P=P.astype(np.float16),
                                spans=np.asarray(spans, dtype=np.int32).reshape(-1, 2))
            f.write(json.dumps({"note_id": n["note_id"], "regex": [e.to_dict() for e in r_ents],
                                "model": [e.to_dict() for e in m_ents],
                                "seconds": {"regex": round(t1 - t0, 4), "model": round(t2 - t1, 4)}}) + "\n")
            f.flush()
            if i % 25 == 0 or i == len(todo):
                el = time.perf_counter() - t_start
                print(f"  {i}/{len(todo)}  {el / i:.2f} s/note  eta {(len(todo) - i) * el / i / 60:.0f} min", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
