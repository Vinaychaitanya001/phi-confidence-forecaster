# Project Plan: Confidence-Aware Clinical De-identification on MedDeID

*The plan as written before the build. What was built and measured is in `REPORT.md`; section 12 lists where the
build differs from this plan. Dataset: `meddeid_english_synthetic/`. Our code: `deidconf/`.*

---

## 1. What we build

A system that finds PHI (names, dates, IDs, addresses, …) in MedDeID clinical notes **and tells you how much to
trust each finding**, plus how likely each note still hides a missed PHI. The confidence part is the project; the
detector is not trained or changed.

This is what the instructor means by "tell what the model is saying about the result, something like a confidence
score".

---

## 2. The pieces

| Piece | What | Status |
|---|---|---|
| **Data** | MedDeID English synthetic corpus: 6,700 notes (3,350 UK, 3,350 US), 6 document types, 14 PHI labels, 38,581 labelled spans, plus 6,700 labelled *hard negatives* (one per note) (text that looks like PHI but is not). Labels verified clean. | Done |
| **Split** | `cal` 1,000 notes: build and tune the confidence model. `test` 1,008 notes: scored **once**, at the end. `train` 4,692 notes: spare; used only if the confidence model needs more errors to learn from. Stratified by locale × document type, fixed seed. | Done (`data/meddeid/`) |
| **Detector** | The existing `Deidentification` repo: its regex rules + **OpenMed FastClinical-82M** NER model (pinned revision) + fusion. **No training, no fine-tuning.** Configuration adapted to MedDeID's annotation guideline: all ages count (not only ≥ 90), clock times are not PHI, titles stay inside names. | Done |
| **Confidence layer** | Our own code in `deidconf/`, built from the two papers. | Done |

---

## 3. The two papers and what we take from them

| | Paper 1: Jagannatha & Yu, ACL 2020 | Paper 2: Jiwani et al., 2026 |
|---|---|---|
| Problem | Softmax confidence is badly calibrated | Softmax thresholding cannot separate true from false entities |
| Idea | Train a small second model (the **forecaster**) on held-out data to predict "is this span correct?" | Train a **decision tree** to label each prediction strong or weak |
| Features | MC-dropout **mean** probability, the **spread** of the MC passes (10th and 90th percentiles, called "Var"), **rank** in top-k decoding, span **length** | **PDM**: probabilities of neighbouring tokens, in 10 bins, weighted by distance; plus statistics (mean, max, entropy, coefficient of variation, top-1/top-2 ratio and gap) |
| Model | Gradient-boosted trees | Decision tree (explainable decision paths) |
| Evaluation | ECE, reliability plots, F1 after re-scoring, out-of-domain test | F1; % false positives removed vs % true positives lost |
| We take | forecaster, uncertainty features, ECE, re-scoring, shift test | PDM, statistics, decision paths, "remove noise but cap recall loss" |

---

## 4. The steps

| # | Step | What exactly | Output |
|---|---|---|---|
| 1 | **Run the detector on `cal`** | Rules + model + fusion with MedDeID-adapted settings. Save every predicted span with its source (rule / model / both) and raw score. | `results/cal_predictions.jsonl` |
| 2 | **Measure it** | Per MedDeID label: fully / partly / not covered. Strict and category-level P/R/F1. Character-level PHI recall and non-PII redaction (MedDeID's own metrics). False alarms per hard-negative type. Seconds per note. | baseline table |
| 3 | **Capture the model's full output** | Extend the adapter to keep the whole probability vector per word (not just the top label). Add MC-dropout mode: N passes with dropout on. Cache for `cal` and `test`. | `results/probs/` |
| 4 | **Features and labels for every predicted span** | Paper 1: mean / min probability, MC-dropout mean and variance, rank, length. Paper 2: PDM bins, statistics at token / word / phrase / neighbour / note level. Ours: rules and model agree?, same string elsewhere in the note?, letter case, digits, `Key: value` header context, which rule fired. Label: correct / wrong against gold (overlap for "is PHI"; category match; exact match). | feature table |
| 5 | **Train the confidence model** | On `cal`, cross-validation grouped by note. GBDT (accuracy) and decision tree (explanations). Baselines: raw softmax, softmax threshold, temperature scaling, Platt scaling. Ablation: add feature groups one at a time. Metrics: ECE (20 bins), Brier, reliability plots, AUROC, review-budget curves (reviewing the 5/10/20% least confident spans catches what share of errors). | calibrated confidence per span |
| 6 | **Our new part: missed PHI** | Near-miss candidates: words where some PHI label has probability ≥ τ but "O" won; spans in the second-best decoding; other occurrences of a string already predicted as PHI; rule matches a filter suppressed. Forecaster for "is this a missed PHI". Note-level leak risk = P(at least one miss in the note). Re-scoring: add high-confidence near-misses back as PHI. Low-confidence predicted spans go to **review**, not deletion. | note-level risk, recall gain |
| 7 | **Robustness and final run** | UK vs US notes; per document type; hard negatives before and after confidence; cost per note (single pass vs MC-dropout). Then run `test` once. Write the report, with decision-path examples (as in paper 2, Appendix C). | final results + report |

---

## 5. What is new compared with the papers

1. **Confidence for missed PHI and a per-note risk score.** Both papers only score what the model predicted; in
   de-identification the miss is the real danger.
2. **One confidence across rules + model.** Both papers calibrate a single neural model; rule outputs have no
   probability at all.
3. **The two papers' features compared side by side**, including CPU cost (MC-dropout is N× slower than PDM).

---

## 6. Expected numbers and known limits

- The detector was never trained on MedDeID, so expect roughly 75–90% recall and thousands of errors on `cal`.
  That is good for this project: the confidence layer has plenty to learn from, and it is paper 2's setting (noisy
  model + learned filter).
- The model cannot output `Profession` and cannot tell `Name:Patient` from `Name:Caregiver` / `Name:Other`. We
  score at MedDeID's 8 top-level categories and report those gaps openly.
- Results are on synthetic notes; they do not prove performance on real clinical text.

---

## 7. Output format (example; numbers are illustrative, not results)

```json
{
  "document_id": "en-gb-synthetic-00001",
  "note_confidence": 0.93,
  "expected_misses": 0.4,
  "spans": [
    {"text": "OKKES REILLY", "category": "Name", "source": "model+rule",
     "confidence": 0.99, "action": "replace"},
    {"text": "Brownroyd Hill Secondary School", "category": "Organization", "source": "model",
     "confidence": 0.62, "action": "replace + review",
     "why": ["high MC-dropout variance", "weak neighbour support (PDM)"]}
  ],
  "possible_misses": [
    {"text": "Writer", "p_missed": 0.71, "action": "review",
     "why": ["follows 'Occupation:' header", "model gave 0.3 to a PHI label"]}
  ]
}
```

---

## 8. Timeline

| Week | Steps |
|---|---|
| 1 | 1, 2 |
| 2 | 3 |
| 3 | 4 |
| 4 | 5 |
| 5 | 6 |
| 6 | 7 |

---

## 9. Open question for the professor

- May we use the official 300-note MedDeID benchmark once, at the very end?

---

## 10. Glossary

- **PHI:** protected health information; anything that can identify a person.
- **Span:** a piece of text given by start and end character positions.
- **Softmax:** turns model scores into probabilities that sum to 1. Transformers are **overconfident**: 0.99 even
  when wrong.
- **Calibration:** confidence matches reality: of all spans given 0.8, about 80% are correct.
- **ECE:** expected calibration error. Bin predictions by confidence, average |accuracy − confidence| over bins.
  Lower is better.
- **Reliability diagram:** accuracy vs confidence per bin; perfect = the diagonal.
- **Brier score:** mean (confidence − outcome)². Lower is better.
- **AUROC:** chance that a random correct span scores higher than a random wrong one. 0.5 random, 1.0 perfect.
- **MC dropout:** run the model N times with dropout on; disagreement between runs = model uncertainty.
- **Temperature / Platt scaling:** simple one-parameter / logistic fixes of softmax calibration (baselines).
- **Forecaster:** paper 1's name for the second model that predicts "is this span correct?".
- **Rank / top-k:** best label sequence = rank 1, next best = rank 2; spans only in rank 2 are plausible alternatives.
- **GBDT:** gradient-boosted decision trees; accurate on tabular features.
- **PDM:** probability density map (paper 2): neighbours' probabilities, binned and distance-weighted.
- **Semantic pull:** around a real entity, nearby words also carry some entity probability; around a false one,
  they are flat "O".
- **Hard negative:** looks like PHI, is not: `08:15`, `5/10`, `Parkinson disease`, `SNOMED CT 233604007`.
- **Near-miss:** text the system did not mark as PHI but that has signs of being PHI.
- **Leakage:** letting test data influence decisions; avoided by making all decisions on `cal`.

## 11. Reading order

1. Paper 1 (`2020.acl-main.188.pdf`): sections 2.3–2.6, Algorithm 1, Tables 3–4, section 4.
2. Paper 2 (`2603.00022v1.pdf`): sections 3–5, Algorithm 1, Appendix B, Appendix C.
3. Guo et al. 2017, *On Calibration of Modern Neural Networks* (ECE, temperature scaling).
4. Gal & Ghahramani 2016, *Dropout as a Bayesian Approximation* (MC dropout).
5. MedDeID dataset card and annotation guideline (`meddeid_english_synthetic/`).
6. `Deidentification/REPORT.md`: how the detector works.


## 12. Final status (updated 2026-11-24)

All seven steps are done; `test` was run once with `scripts/run_test.sh`. Headline (test, 1,008 notes):
detector PHI recall 91.1 % → 98.5 % (strict F1 73.8 % → 94.5 %, false alarms 244 → 60); span confidence ECE
0.203 → 0.003 with AUROC(error) 0.998 (all 62 non-PHI spans in the 5 % least-confident spans); missed-PHI forecaster
AUROC 0.990, 95 % precision on added candidates, PHI recall 98.5 % → 99.5 % with them added, note-level risk AUROC
0.964. Full write-up in `REPORT.md`, tables in `results/RESULTS_cal_v5.md`, `results/RESULTS_test_v5.md` and
`results/before_after/test_v5/report.md`.

Where the build differs from the plan above:
- 43 MedDeID regex rules were added and a few repo settings changed; they were written on `train`, which was
  therefore used for rule development rather than kept spare.
- Missed-PHI candidates are runs of uncovered words with PHI mass ≥ 0.02 and repeats of detected text; candidates
  from a second-best decoding or from suppressed rule matches were not built.
- Paper 1's rank feature is not used (the model has no top-k decoder); paper 2's top-1/top-2 gap and ratio are used.
- Paper 2's three PDM classes (B, I, O) are adapted to same category / other entity / not PHI.
