"""MedDeID English synthetic corpus: reader, label set and deterministic splits.

Source: https://huggingface.co/datasets/stighellemans/meddeid-english-synthetic-corpus (CC BY 4.0).
The publisher ships one `train` split of 6,700 documents and asks users to make their own partition.

Internal record (JSONL, one note per line):
    {"note_id", "text", "spans": [{"start","end","label","slot"}], "doc_type", "lang", "style",
     "patient_age", "hard_negatives": [{"start","end","category"}]}
Offsets are absolute, half-open, in Unicode code points: identical to Python string indexing.
"""
from __future__ import annotations

import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

LABELS = [
    "Name:Patient", "Name:Caregiver", "Name:Other",
    "Address_Location:Patient", "Address_Location:Caregiver", "Address_Location:Other",
    "Organization:Healthcare", "Organization:Other",
    "ID:Patient", "ID:Caregiver",
    "Date", "Age_Birthdate", "Contactdetails", "Profession",
]
CATEGORY = {l: l.split(":")[0] for l in LABELS}          # Name:Patient -> Name (8 top-level categories)
CATEGORIES = sorted(set(CATEGORY.values()))


def read_corpus(path: str | Path) -> list[dict[str, Any]]:
    """Read the published data/train.jsonl and convert every record; fail loudly on any inconsistency."""
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            meta = r["metadata"] if "metadata" in r else json.loads(r["metadata_json"])
            text = r["text"]
            spans = []
            for s in r["spans"]:
                if not (0 <= s["begin"] < s["end"] <= len(text)) or text[s["begin"]:s["end"]] != s["text"]:
                    raise ValueError(f"{r['document_id']}: span offsets do not match text")
                if s["label"] not in LABELS:
                    raise ValueError(f"{r['document_id']}: unknown label {s['label']}")
                spans.append({"start": s["begin"], "end": s["end"], "label": s["label"], "slot": s.get("source_slot")})
            spans.sort(key=lambda x: (x["start"], x["end"]))
            for a, b in zip(spans, spans[1:]):
                if b["start"] < a["end"]:
                    raise ValueError(f"{r['document_id']}: overlapping spans")
            hard = []
            for t in meta.get("hard_negative_targets") or []:
                v = t.get("value")
                p = text.find(v) if v else -1
                if p >= 0:
                    hard.append({"start": p, "end": p + len(v), "category": t.get("category")})
            out.append({
                "note_id": r["document_id"], "text": text, "spans": spans,
                "doc_type": meta.get("document_type"), "lang": meta.get("lang"),
                "style": (meta.get("style_profile") or {}).get("name"),
                "patient_age": meta.get("patient_age"), "hard_negatives": hard,
            })
    return out


def assign_splits(notes: Iterable[dict[str, Any]], fractions: dict[str, float], seed: int) -> dict[str, str]:
    """Deterministic stratified split. Within every (lang, doc_type) stratum the note ids are shuffled with a
    seed derived from (seed, stratum) and cut by cumulative fractions, in insertion order. {note_id: split}."""
    if abs(sum(fractions.values()) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1")
    strata: dict[tuple, list[str]] = defaultdict(list)
    for n in notes:
        strata[(n["lang"], n["doc_type"])].append(n["note_id"])
    names = list(fractions)
    assignment: dict[str, str] = {}
    for key in sorted(strata):
        ids = sorted(strata[key])
        h = int(hashlib.sha256(f"{seed}|{key}".encode()).hexdigest(), 16) % (2 ** 32)
        random.Random(h).shuffle(ids)
        n, start, acc = len(ids), 0, 0.0
        for i, name in enumerate(names):
            acc += fractions[name]
            end = n if i == len(names) - 1 else int(round(acc * n))
            for nid in ids[start:end]:
                assignment[nid] = name
            start = end
    return assignment


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def split_summary(notes: list[dict[str, Any]], assignment: dict[str, str]) -> dict[str, Any]:
    """Counts only (never text) per split."""
    per: dict[str, Any] = {}
    for n in notes:
        d = per.setdefault(assignment[n["note_id"]], {"notes": 0, "spans": 0, "labels": Counter(),
                                                       "hard_negatives": Counter(), "lang": Counter(),
                                                       "doc_type": Counter(), "style": Counter()})
        d["notes"] += 1
        d["spans"] += len(n["spans"])
        d["labels"].update(x["label"] for x in n["spans"])
        d["hard_negatives"].update(x["category"] for x in n["hard_negatives"])
        d["lang"][n["lang"]] += 1
        d["doc_type"][n["doc_type"]] += 1
        d["style"][n["style"]] += 1
    return {k: {kk: (dict(vv) if isinstance(vv, Counter) else vv) for kk, vv in v.items()} for k, v in per.items()}
