"""Error analysis for rule development: what the detector misses, what it wrongly redacts, where boundaries differ.

    python -m deidconf.errors --split train --system rules+model [--label Profession] [--limit 40]

Reads results/eval/<split>/<system>.predictions.jsonl and the gold split, prints grouped examples with context, and
writes results/eval/<split>/<system>.errors.md. Use on `train` (rule development) or `cal` (measurement); never on
`test` before the end.
"""
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict

from deidconf import PROJECT_ROOT
from deidconf.data import CATEGORY, LABELS, read_jsonl


def ctx(text: str, s: int, e: int, w: int = 35) -> str:
    left = text[max(0, s - w):s].replace("\n", "⏎")
    mid = text[s:e].replace("\n", "⏎")
    right = text[e:e + w].replace("\n", "⏎")
    return f"{left}⟦{mid}⟧{right}"


def shape(s: str) -> str:
    """Rough surface pattern of a string: letters -> a/A, digits -> 9, keep punctuation; runs collapsed."""
    t = re.sub(r"[A-Z]+", "A", s)
    t = re.sub(r"[a-z]+", "a", t)
    t = re.sub(r"[0-9]+", "9", t)
    return t[:40]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="train")
    ap.add_argument("--system", default="rules+model")
    ap.add_argument("--label", default=None, help="restrict missed/partial listing to one MedDeID label")
    ap.add_argument("--limit", type=int, default=30, help="examples per group")
    a = ap.parse_args(argv)
    data_split = a.split.split("_")[0]          # results folder may carry a tag, e.g. train_rules_v1
    notes = {n["note_id"]: n for n in read_jsonl(PROJECT_ROOT / f"data/meddeid/{data_split}.jsonl")}
    preds = read_jsonl(PROJECT_ROOT / f"results/eval/{a.split}/{a.system}.predictions.jsonl")

    missed = defaultdict(list)       # label -> [(shape, ctx)]
    partial = defaultdict(list)      # label -> [(gold ctx, pred text)]
    wrong_cat = defaultdict(list)    # (gold label, pred category) -> ctx
    false_alarm = defaultdict(list)  # (pred category, source kind) -> ctx
    hard_hit = defaultdict(list)
    miss_shapes = defaultdict(Counter)
    prev_word = defaultdict(Counter)

    for p in preds:
        n = notes[p["note_id"]]
        text, gold, spans = n["text"], n["spans"], p["spans"]
        for g in gold:
            ov = [s for s in spans if s["start"] < g["end"] and g["start"] < s["end"]]
            gtxt = text[g["start"]:g["end"]]
            if not ov:
                missed[g["label"]].append(ctx(text, g["start"], g["end"]))
                miss_shapes[g["label"]][shape(gtxt)] += 1
                pw = re.findall(r"(\S+)\s*[:\-]?\s*$", text[max(0, g["start"] - 25):g["start"]])
                prev_word[g["label"]][pw[0].lower() if pw else "<none>"] += 1
                continue
            full = all(any(s["start"] <= i < s["end"] for s in ov) for i in range(g["start"], g["end"]))
            exact = any(s["start"] == g["start"] and s["end"] == g["end"] for s in ov)
            if not full or not exact:
                partial[g["label"]].append((ctx(text, g["start"], g["end"]),
                                            " | ".join(f"{text[s['start']:s['end']]!r}:{s['category']}" for s in ov)))
            if not any(s["category"] == CATEGORY[g["label"]] for s in ov):
                wrong_cat[(g["label"], ",".join(sorted({s["category"] for s in ov})))].append(ctx(text, g["start"], g["end"]))
        for s in spans:
            ov = [g for g in gold if s["start"] < g["end"] and g["start"] < s["end"]]
            if not ov:
                kind = "rules" if s["source"] == "regex" else ("both" if "regex" in s["source"] else "model")
                false_alarm[(s["category"], kind, s.get("rule") or s.get("label"))].append(ctx(text, s["start"], s["end"]))
        for h in n.get("hard_negatives", []):
            if any(s["start"] < h["end"] and h["start"] < s["end"] for s in spans):
                hard_hit[h["category"]].append(ctx(text, h["start"], h["end"]))

    L = [f"# Error analysis: `{a.system}` on `{a.split}`", ""]
    L += ["## Missed gold spans (no overlap with any prediction)", ""]
    for lab in LABELS:
        if a.label and lab != a.label:
            continue
        ex = missed.get(lab, [])
        if not ex:
            continue
        L += [f"### {lab}: {len(ex)} missed", "",
              "shapes: " + ", ".join(f"`{s}`×{c}" for s, c in miss_shapes[lab].most_common(8)),
              "preceded by: " + ", ".join(f"`{w}`×{c}" for w, c in prev_word[lab].most_common(8)), ""]
        L += [f"- {e}" for e in ex[:a.limit]] + [""]
    L += ["## Found but wrong boundaries (partial or inexact)", ""]
    for lab in LABELS:
        if a.label and lab != a.label:
            continue
        ex = partial.get(lab, [])
        if ex:
            L += [f"### {lab}: {len(ex)}", ""] + [f"- {g}  →  {p}" for g, p in ex[:a.limit]] + [""]
    L += ["## Found but wrong category", ""]
    for (lab, cat), ex in sorted(wrong_cat.items(), key=lambda kv: -len(kv[1])):
        L += [f"### gold {lab} → predicted {cat}: {len(ex)}", ""] + [f"- {e}" for e in ex[:a.limit]] + [""]
    L += ["## False alarms (prediction overlaps no gold span)", ""]
    for (cat, kind, lab), ex in sorted(false_alarm.items(), key=lambda kv: -len(kv[1])):
        L += [f"### {cat} by {kind} (rule/label {lab}): {len(ex)}", ""] + [f"- {e}" for e in ex[:a.limit]] + [""]
    L += ["## Hard negatives redacted", ""]
    for cat, ex in sorted(hard_hit.items(), key=lambda kv: -len(kv[1])):
        L += [f"### {cat}: {len(ex)}", ""] + [f"- {e}" for e in ex[:a.limit]] + [""]
    out = PROJECT_ROOT / f"results/eval/{a.split}/{a.system}.errors.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"missed: {sum(len(v) for v in missed.values())}  partial/inexact: {sum(len(v) for v in partial.values())}  "
          f"wrong category: {sum(len(v) for v in wrong_cat.values())}  false alarms: {sum(len(v) for v in false_alarm.values())}")
    print(f"written {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
