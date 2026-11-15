"""Make the fixed train / calibration / test split of the MedDeID corpus (run once).

    python -m deidconf.prepare --src meddeid_english_synthetic/data/train.jsonl

Writes data/meddeid/{train,cal,test}.jsonl, split_assignment.json and split_report.json (counts only).
Deterministic (seed + per-stratum hashing), stratified by locale x document type.
Rules: all decisions use `cal`; `test` is scored once at the very end.
"""
from __future__ import annotations

import argparse
import json

from deidconf import PROJECT_ROOT
from deidconf.data import assign_splits, read_corpus, split_summary, write_jsonl

FRACTIONS = {"train": 0.70, "cal": 0.15, "test": 0.15}
SEED = 20261115


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="meddeid_english_synthetic/data/train.jsonl")
    ap.add_argument("--out", default="data/meddeid")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    out = PROJECT_ROOT / a.out
    if (out / "split_assignment.json").exists() and not a.force:
        print(f"split already exists in {out}; pass --force to recreate it")
        return 1
    notes = read_corpus(PROJECT_ROOT / a.src)
    assignment = assign_splits(notes, FRACTIONS, a.seed)
    for name in FRACTIONS:
        n = write_jsonl(out / f"{name}.jsonl", (r for r in notes if assignment[r["note_id"]] == name))
        print(f"{name}: {n} notes")
    (out / "split_assignment.json").write_text(json.dumps(assignment, indent=0, sort_keys=True), encoding="utf-8")
    report = {"source": a.src, "seed": a.seed, "fractions": FRACTIONS, "stratified_by": ["lang", "doc_type"],
              "splits": split_summary(notes, assignment)}
    (out / "split_report.json").write_text(json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
