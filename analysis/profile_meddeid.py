"""Profile the MedDeID English synthetic corpus. Usage: python -I profile_meddeid.py <train.jsonl> <development.jsonl>"""
import json
import statistics as st
import sys
from collections import Counter, defaultdict


def load(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def q(xs):
    xs = sorted(xs)
    return dict(min=xs[0], p25=xs[len(xs) // 4], median=xs[len(xs) // 2], p75=xs[3 * len(xs) // 4],
                max=xs[-1], mean=round(st.mean(xs), 1))


train, dev = load(sys.argv[1]), load(sys.argv[2])
print("records: train.jsonl", len(train), "| source/development.jsonl", len(dev))
print("train fields:", Counter(k for r in train for k in r))
print("dev fields:", Counter(k for r in dev for k in r))

# --- are the two files the same corpus?
same_ids = [r["document_id"] for r in train] == [r["document_id"] for r in dev]
same_text = all(a["text"] == b["text"] for a, b in zip(train, dev))
same_spans = all(a["spans"] == b["spans"] for a, b in zip(train, dev))
same_meta = all(json.loads(a["metadata_json"]) == b["metadata"] for a, b in zip(train, dev))
print(f"train == development? ids {same_ids}, text {same_text}, spans {same_spans}, metadata {same_meta}")
print("annotated flag:", Counter(r.get("annotated") for r in train))
print("unique document_ids:", len({r['document_id'] for r in train}), "| unique texts:", len({r['text'] for r in train}))

meta = [json.loads(r["metadata_json"]) for r in train]
print("\nmetadata top-level keys:", Counter(k for m in meta for k in m).most_common())
for key in ["lang", "document_type", "generation_method", "renderer", "model", "synthetic"]:
    print(f"  {key}:", Counter(str(m.get(key)) for m in meta).most_common())
print("  style_profile.name:", Counter((m.get("style_profile") or {}).get("name") for m in meta).most_common())
print("  doc_type x lang:", Counter((m.get("document_type"), m.get("lang")) for m in meta).most_common())
hn = Counter(t.get("category") for m in meta for t in (m.get("hard_negative_targets") or []))
print("  hard_negative_targets categories:", hn.most_common())
ex = defaultdict(list)
for m in meta:
    for t in m.get("hard_negative_targets") or []:
        if len(ex[t.get("category")]) < 3:
            ex[t.get("category")].append(t.get("value"))
print("  hard-negative examples:", dict(ex))
years = Counter((m.get("document_creation_date") or "????")[:3] + "0s" for m in meta)
print("  document_creation_date decades:", sorted(years.items()))
# keys that look pediatric-related
ped = Counter()
for m in meta:
    for k, v in m.items():
        if "pediatric" in k.lower() or "age_band" in k.lower():
            ped[(k, json.dumps(v)[:60])] += 1
print("  pediatric-related keys:", ped.most_common(12))

# --- text stats
chars = [len(r["text"]) for r in train]
words = [len(r["text"].split()) for r in train]
print("\ntext chars:", q(chars))
print("text words:", q(words))
for lang in ["en-GB", "en-US"]:
    w = [len(r["text"].split()) for r, m in zip(train, meta) if m.get("lang") == lang]
    print(f"  words {lang}:", q(w))
print("total words:", sum(words))

# --- spans
labels = Counter()
by_lang = defaultdict(Counter)
per_doc, span_len, slots, confirmed = [], defaultdict(list), Counter(), Counter()
bad_off, mismatch, overlaps, unsorted, empty_docs = 0, 0, 0, 0, 0
for r, m in zip(train, meta):
    t, sp = r["text"], r["spans"]
    per_doc.append(len(sp))
    if not sp:
        empty_docs += 1
    if [(s["begin"], s["end"]) for s in sp] != sorted((s["begin"], s["end"]) for s in sp):
        unsorted += 1
    ordered = sorted(sp, key=lambda s: (s["begin"], s["end"]))
    for a, b in zip(ordered, ordered[1:]):
        if b["begin"] < a["end"]:
            overlaps += 1
    for s in sp:
        labels[s["label"]] += 1
        by_lang[m.get("lang")][s["label"]] += 1
        span_len[s["label"]].append(len(s["text"].split()))
        slots[s.get("source_slot")] += 1
        confirmed[s.get("confirmed")] += 1
        if not (0 <= s["begin"] < s["end"] <= len(t)):
            bad_off += 1
        elif t[s["begin"]:s["end"]] != s["text"]:
            mismatch += 1
print("\nspans total:", sum(labels.values()), "| per doc:", q(per_doc), "| docs with 0 spans:", empty_docs)
print("integrity: bad offsets", bad_off, "| text mismatches", mismatch, "| overlapping pairs", overlaps,
      "| docs with unsorted spans", unsorted)
print("confirmed flag:", confirmed)
print("span field keys:", Counter(k for r in train for s in r["spans"] for k in s))
print("\nlabel counts (all | en-GB | en-US | median words | max words):")
for lab, n in labels.most_common():
    print(f"  {lab:28s} {n:6d} {by_lang['en-GB'][lab]:6d} {by_lang['en-US'][lab]:6d}"
          f"   {st.median(span_len[lab]):4} {max(span_len[lab]):4}")
docs_with = Counter(lab for r in train for lab in {s['label'] for s in r['spans']})
print("documents containing each label:", docs_with.most_common())
print("\nsource_slot (top 40):", slots.most_common(40))

# required targets vs spans
missing_req = 0
total_req = 0
for r, m in zip(train, meta):
    got = {(s["text"], s["label"]) for s in r["spans"]}
    for tgt in m.get("required_pii_targets") or []:
        total_req += 1
        if (tgt.get("value"), tgt.get("label")) not in got:
            missing_req += 1
print(f"required_pii_targets: {total_req}, not found verbatim among spans: {missing_req}")

# examples per label
exs = defaultdict(list)
for r in train:
    for s in r["spans"]:
        if len(exs[s["label"]]) < 8 and s["text"] not in exs[s["label"]]:
            exs[s["label"]].append(s["text"])
print("\nexamples per label:")
for lab in sorted(exs):
    print(f"  {lab}: {exs[lab]}")

# Contactdetails / Age_Birthdate / ID sub-kinds by slot
for lab in ["Contactdetails", "Age_Birthdate", "ID:Patient", "ID:Caregiver", "Date"]:
    c = Counter(s.get("source_slot") for r in train for s in r["spans"] if s["label"] == lab)
    print(f"slots for {lab}:", c.most_common(12))
