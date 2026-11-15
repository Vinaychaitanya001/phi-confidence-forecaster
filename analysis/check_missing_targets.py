"""Why are some required_pii_targets not among the labelled spans? And where are the hard negatives?
Usage: python -I check_missing_targets.py <train.jsonl>"""
import json
import re
import sys
from collections import Counter, defaultdict

rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]

# ---- 1. required targets missing from spans
kinds = Counter()
by_slot = Counter()
examples = defaultdict(list)
n_unlabelled_verbatim = 0
docs_affected = set()
for r in rows:
    m = json.loads(r["metadata_json"])
    text = r["text"]
    spans = r["spans"]
    got = {(s["text"], s["label"]) for s in spans}
    got_text = {s["text"] for s in spans}
    covered = [False] * len(text)
    for s in spans:
        for i in range(s["begin"], s["end"]):
            covered[i] = True
    for tgt in m.get("required_pii_targets") or []:
        v, lab, slot = tgt.get("value"), tgt.get("label"), tgt.get("slot")
        if (v, lab) in got:
            continue
        docs_affected.add(r["document_id"])
        by_slot[slot] += 1
        if v in got_text:
            kind = "same text, different label"
        elif v not in text:
            # does it appear with different case?
            if v.lower() in text.lower():
                kind = "in text with different case"
            else:
                kind = "NOT in text at all (reworded/omitted by generator)"
        else:
            # verbatim in text but not a span: is that position covered by some other span?
            pos = text.find(v)
            inside = all(covered[pos:pos + len(v)])
            partial = any(covered[pos:pos + len(v)])
            if inside:
                kind = "verbatim, inside a larger labelled span"
            elif partial:
                kind = "verbatim, partly covered by a span"
            else:
                kind = "verbatim in text, NOT labelled  <-- possible label gap"
                n_unlabelled_verbatim += 1
        kinds[kind] += 1
        if len(examples[kind]) < 6:
            ctx = ""
            if v in text:
                p = text.find(v)
                ctx = text[max(0, p - 40):p + len(v) + 40].replace("\n", "\\n")
            examples[kind].append((r["document_id"], slot, lab, v, ctx))

print("=== required_pii_targets not found as (text,label) span ===")
print("documents affected:", len(docs_affected))
for k, n in kinds.most_common():
    print(f"\n[{n}] {k}")
    for ex in examples[k]:
        print("   ", ex)
print("\nby slot:", by_slot.most_common(15))

# ---- 2. hard negatives: are they in the text, and are they ever (wrongly) inside a labelled span?
hn_total = Counter()
hn_in_text = Counter()
hn_overlap_span = Counter()
hn_ex = defaultdict(list)
for r in rows:
    m = json.loads(r["metadata_json"])
    text = r["text"]
    spans = r["spans"]
    for t in m.get("hard_negative_targets") or []:
        cat, v = t.get("category"), t.get("value")
        hn_total[cat] += 1
        p = text.find(v) if v else -1
        if p < 0:
            continue
        hn_in_text[cat] += 1
        if any(s["begin"] < p + len(v) and p < s["end"] for s in spans):
            hn_overlap_span[cat] += 1
            if len(hn_ex[cat]) < 3:
                hn_ex[cat].append((r["document_id"], v, text[max(0, p - 30):p + len(v) + 30].replace("\n", "\\n")))
print("\n=== hard negatives ===")
print(f"{'category':22s} {'total':>6s} {'found verbatim':>15s} {'overlaps a PHI span':>20s}")
for cat, n in hn_total.most_common():
    print(f"{cat:22s} {n:6d} {hn_in_text[cat]:15d} {hn_overlap_span[cat]:20d}")
for cat, exs in hn_ex.items():
    print(" overlap examples", cat, exs)

# ---- 3. how often does a labelled name string reappear unlabelled in the same note? (consistency feature check)
reappear = Counter()
for r in rows:
    text = r["text"]
    spans = r["spans"]
    covered = [False] * len(text)
    for s in spans:
        for i in range(s["begin"], s["end"]):
            covered[i] = True
    for s in spans:
        if not s["label"].startswith("Name:") or len(s["text"]) < 4:
            continue
        for mt in re.finditer(r"(?<!\w)" + re.escape(s["text"]) + r"(?!\w)", text):
            if not any(covered[mt.start():mt.end()]):
                reappear[s["label"]] += 1
print("\n=== labelled name string reappears UNLABELLED elsewhere in the same note ===")
print(reappear.most_common())
