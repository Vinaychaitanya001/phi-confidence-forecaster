# Status and open items

*Updated 2026-11-24. Data: MedDeID English synthetic corpus only. Plan: PLAN.md; write-up: REPORT.md.*

## Decisions

- **Detector:** the existing `Deidentification` system (regex rules + OpenMed FastClinical-82M, used exactly as
  published, no training). 43 MedDeID-specific regex rules were added and a few repo settings adapted to the
  MedDeID guideline; rules were written on `train` only.
- **The project is the confidence layer** on top of it, from the two papers, plus our missed-PHI side.
- **Split:** train 4,692 (rule development) / cal 1,000 (forecasters, thresholds, all decisions) / test 1,008 (scored once).

## Status: all steps done

| # | Step | Result on `test` (single run, nothing refitted) |
|---|---|---|
| 1–2 | Detector + evaluation | Baseline (regex + NER model): PHI recall 91.1 %, 244 false alarms, strict F1 73.8 %. **Improved: 98.5 %, 60 false alarms, strict F1 94.5 %**, non-PII redaction 0.07 % |
| 3 | Full probabilities + MC dropout | cached in `results/detect/`, `results/mcdropout/` (cal and test) |
| 4–5 | Span confidence (papers 1 + 2 + ours) | is-PHI: ECE 0.203 → **0.003**, AUROC(error) 0.752 → **0.998**, all 62 spans that are not PHI (including all 60 false alarms) among the 5 % least-confident spans. Category: ECE 0.0045, AUROC 0.997. Exact: ECE 0.005, AUROC 0.997 |
| 6 | Missed PHI (our addition) | 86 % of uncovered gold spans get a candidate; forecaster AUROC 0.990; adding at p ≥ 0.5 adds 80 candidates, 76 of them real missed PHI (95 % precision), PHI recall 98.5 % → 99.5 %, gold spans missed 114 → 40; note-level risk AUROC 0.964, riskiest 10 % of notes hold 84 % of misses |
| 7 | Robustness, cost, final run | UK→US shift (cal): ECE ≤ 0.014, AUROC ≥ 0.984. Hard negatives: 11/1008 redacted, 9 flagged. Cost: rules 17 ms, model 0.35 s, MC dropout 4.3 s per note |
| — | Deliverable | `python -m deidconf.pipeline --text "..."` / `--input notes.jsonl`: per span three confidences + action, possible misses + action, note-level risk, de-identified text. 43 unit tests pass; the repo's own suite: 257 passed, 3 skipped |

## Open items

1. Score the official 300-note MedDeID benchmark once (not done; our `test` split is from the 6,700-note corpus).
2. Fit and evaluate span and missed-PHI forecasters without the MC-dropout features. The pipeline runs 10 MC passes
   by default (4.3 s per note) because the saved forecasters need them; the single-pass mode is untested.
3. Validate on real clinical text before any use outside this synthetic corpus.
