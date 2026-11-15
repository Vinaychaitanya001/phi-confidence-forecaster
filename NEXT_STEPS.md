# Next steps (short)

*Updated 2026-11-15, end of the build. Data: MedDeID English synthetic corpus only. Full detail: PLAN.md; write-up: REPORT.md.*

## Decisions

- **Detector:** the existing `Deidentification` system (regex rules + OpenMed FastClinical-82M, used exactly as
  published, no training). 43 MedDeID-specific regex rules were added and a few repo settings adapted to the
  MedDeID guideline; rules were written on `train` only.
- **The project is the confidence layer** on top of it, from the two papers, plus our missed-PHI side.
- **Split:** train 4,692 (rule development) / cal 1,000 (forecasters, thresholds, all decisions) / test 1,008 (scored once).

## Status: all steps done

| # | Step | Result on `test` (single run, nothing refitted) |
|---|---|---|
| 1–2 | Detector + evaluation | Baseline (repo as shipped): PHI recall 91.1 %, 244 false alarms, strict F1 73.8 %. **Improved: 98.5 %, 60 false alarms, strict F1 94.5 %**, non-PII redaction 0.07 % |
| 3 | Full probabilities + MC dropout | cached in `results/detect/`, `results/mcdropout/` (cal and test) |
| 4–5 | Span confidence (papers 1 + 2 + ours) | is-PHI: ECE 0.20 → **0.003**, AUROC(error) 0.75 → **0.998**, all 62 false alarms among the 5 % least-confident spans. Category: ECE 0.005, AUROC 0.997. Exact: ECE 0.005, AUROC 0.997 |
| 6 | Missed PHI (our addition) | 86 % of uncovered gold spans get a candidate; forecaster AUROC 0.990; adding p ≥ 0.5 recovers 77 % of them at 95 % precision; note-level risk AUROC 0.964, riskiest 10 % of notes hold 84 % of misses |
| 7 | Robustness, cost, final run | UK→US shift: ECE ≤ 0.014, AUROC ≥ 0.984. Hard negatives: 11/1008 redacted, 9 flagged. Cost: rules 17 ms, model 0.35 s, MC dropout 4.3 s per note |
| — | Deliverable | `python -m deidconf.pipeline --text "..."` / `--input notes.jsonl`: per span three confidences + action, possible misses + action, note-level risk, de-identified text. 42 unit tests + the repo's 260 pass |

## What is left (for you)

1. Read `REPORT.md`; the tables in §5.2 are the numbers to present.
2. Ask the professor whether to also score the official 300-note MedDeID benchmark once (not done; our `test` split is from the 6,700-note corpus).
3. Possible extension if she wants more: drop MC dropout from the deployed forecaster (gain is small, cost is 10×); score the real-text benchmark if she has one.
