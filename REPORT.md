# Confidence-Aware Clinical De-identification on the MedDeID Corpus

*Independent study, semester 3. Results on the test split are from a single run (`results/RESULTS_test_v5.md`).*

## 1. Problem

De-identification systems find protected health information (PHI) in clinical notes and replace it. They produce
a span and a label but not a usable statement of how much to trust each decision, and nothing at all about what
they may have missed. The instructor's request was to make the system "tell what the model is saying about the
result": a confidence score. Two papers framed the work:

- **Jagannatha & Yu (ACL 2020), *Calibrating Structured Output Predictors for NLP***: a second, small model (the
  *forecaster*) is trained on held-out data to predict whether each predicted entity is correct, from the model's
  probability averaged over MC-dropout passes, the spread of those passes (10th and 90th percentiles), the rank of
  the decoding and the span length; calibration is measured with
  expected calibration error (ECE) and the calibrated score is used to re-rank predictions.
- **Jiwani et al. (2026), *Noise reduction in BERT NER models for clinical entity extraction***: an explainable
  decision tree classifies each prediction as strong or weak from a *probability density map* (PDM) of the
  neighbouring tokens' probabilities and statistical features (entropy, top-1/top-2 ratio and gap, coefficient of
  variation), exploiting the "semantic pull" that real entities exert on their neighbours.

Both papers only score what the model predicted. In de-identification the dangerous error is the opposite one, the
PHI that was *not* predicted. Our main addition is confidence on that side: near-miss candidates, a missed-PHI
forecaster and a note-level leak risk.

## 2. Data

MedDeID English synthetic clinical corpus (Hellemans et al., 2026; CC BY 4.0;
https://huggingface.co/datasets/stighellemans/meddeid-english-synthetic-corpus): 6,700 synthetic documents
(3,350 en-GB, 3,350 en-US; six document types; median 215 words), 38,581 PHI spans in 14 labels, plus 6,700
labelled *hard negatives*, one per note (clock times, doses, pain scores, eponyms, terminology codes, impossible dates…).
Labels were verified exact (offsets, no overlaps). 1,448 generator age values are not labelled word for word, all by the
guideline: 696 "42-year-old" ages are labelled "42-year" and 752 "aged 57 years" ages are labelled "57 years".

Split, stratified by locale × document type with a fixed seed: **train 4,692** (rule development only; no model is
trained), **calibration 1,000** (forecaster training, thresholds, every decision), **test 1,008** (scored once).

## 3. System

### 3.1 Detector (not trained)
The existing `Deidentification` system: regex rules + the OpenMed FastClinical-82M token classifier, used exactly as
published. Configuration adapted to the MedDeID guideline: all ages count, clock times are not PHI, titles stay in
names, states are PHI, the model's *occupation* tags stay ignored as in the repo (they also fire on caregiver roles), `-old` is trimmed
from ages, impossible numeric dates and pain scores are not dates.

### 3.2 MedDeID rule set
43 regex rules written from the guideline and the surface forms of the **train** split only (four rounds of error
analysis): UK/US identifiers (NHS, NI, SSN, MRN, accession, GMC/professional IDs), UK phones and postcodes, ages
with units, dates of birth, professions after `Occupation:`, names after headers / sign-offs / "by" / relation words /
credentials and titles (kept inside the span), localities, home addresses and organisations (headers, UK suffixes,
`University Hospital X`, ` - Department` extensions). Rule spans keep their matched boundaries (`raw`), bypassing
the repo's HIPAA-oriented clean-up. The repo's generic organisation and `name_field` rules are switched off.

### 3.3 Fusion
The repo's fusion: overlapping spans with the same label are merged into their union. When labels conflict, rule
spans of a structured category (dates, times, phones, emails, IDs, ages, other PHI, and professions in our setting)
keep their boundaries and label; otherwise the highest-scoring span wins. Other exact occurrences of a detected name
in the same note are marked too.

### 3.4 Confidence of predicted spans
For every predicted span, three targets: *is PHI* (≥ 50 % of its characters inside gold PHI), *category right*, and
*exact*. Features (86 columns used by the forecasters): paper 1 (mean / min / geometric-mean probability of the predicted category over the
span's words, P(O), length, MC-dropout mean and standard deviation over 10 passes, pass agreement); paper 2 (PDM:
10 probability bins × {same category, other entity, O} over ±8 neighbouring words with Gaussian distance weights;
entropy, top-1/top-2 ratio and gap, coefficient of variation; neighbour and note-level statistics); ours
(rule / model / both, rule family and rule, repetition of the string in the note, letter case, digits, `Key: value`
header context, position, locale). Forecasters: gradient-boosted trees (paper 1) and a depth-5 decision tree
(paper 2, for explanations). Baselines: raw softmax, raw fused score, temperature scaling, Platt scaling, the
"calibrated mean" of paper 1. All estimates are out-of-fold with 5-fold GroupKFold by note on the calibration split;
the test split is scored once with forecasters fitted on calibration.

### 3.5 Missed PHI (our addition)
Candidates: (a) runs of words outside every predicted span whose PHI probability mass is ≥ τ = 0.02; (b) other
occurrences of a predicted string. Target: the candidate contains gold-PHI letters or digits that no prediction
covers. A GBDT forecaster scores candidates; candidates with p ≥ 0.5 are added as PHI (paper 1's re-scoring on the
recall side), p ≥ 0.2 are flagged. Note-level leak risk: P(≥ 1 miss) = 1 − Π(1 − pᵢ), expected misses = Σ pᵢ.

### 3.6 Deliverable
`python -m deidconf.pipeline` takes new notes and returns, per note, the spans with their three confidences and an
action (replace / replace + review), the possible misses with their probability and action (add / review), the
note-level risk, and the de-identified text produced by the repo's policy engine.

## 4. Evaluation protocol
Detector: MedDeID's own character-level PHI recall and non-PII redaction with document-bootstrap 95 % CIs; strict
category-level precision / recall / F1; per-label coverage; hard negatives redacted. Confidence: ECE (20 bins),
Brier, NLL, AUROC and AUPRC for "this span is wrong", share of errors caught when reviewing the 5 / 10 / 20 % least
confident spans, precision after dropping low-confidence spans at ≤ 0.1 % recall loss; ECE by category, rule
family, locale and document type; locale shift (forecaster fitted on en-GB, scored on en-US). Missed PHI: candidate
coverage of real misses, AUROC / AUPRC, precision of added candidates, note-level AUROC and review-budget curves.
Cost: seconds per note on CPU, single pass vs MC dropout.

## 5. Results

### 5.1 Calibration split (development numbers; full tables in `results/RESULTS_cal_v5.md`)

**Detector** (1,000 notes, 5,750 gold spans). Every decision about rules and settings was made on `train`; these
are the first numbers seen on `cal`.

| System | PHI recall (chars) [95 % CI] | Non-PII redaction | Strict category P / R / F1 | False alarms | Hard negatives redacted |
|---|---|---|---|---|---|
| Baseline: repo rules + model, as shipped | 91.4 % [90.8–92.0] | 0.31 % | 73.0 / 74.3 / 73.7 | 251 | 33 / 1000 |
| MedDeID rules only | 94.1 % [93.5–94.8] | 0.06 % | 97.6 / 91.6 / 94.5 | 16 | 2 / 1000 |
| Model only | 83.6 % [82.7–84.6] | 0.04 % | 72.8 / 69.1 / 70.9 | 57 | 14 / 1000 |
| **MedDeID rules + model** | **98.5 % [98.2–98.8]** | 0.09 % | 94.1 / 94.9 / **94.5** | 72 | 15 / 1000 |

Weakest labels: `ID:Caregiver` (89.8 % found; professional IDs without a prefix), `Address_Location:Caregiver`
(94.0 %), `Name:Other` (96.2 %). Dates, ages, contact details and patient IDs are at or near 100 %. Referral letters
are the hardest document type (97.3 %).

**Confidence of predicted spans** (5,800 spans, out-of-fold). ECE = expected calibration error, AUROC(error) =
how well the confidence ranks wrong spans below right ones, capture = share of wrong spans among the 10 % least
confident.

| Target (errors) | Model | ECE | Brier | AUROC(error) | errors caught @10 % review | precision before → after |
|---|---|---|---|---|---|---|
| is PHI (80) | raw softmax | 0.202 | 0.133 | 0.764 | 29 % | 98.62 → 98.62 |
| | temperature scaling | 0.326 | 0.157 | 0.762 | 29 % | 98.62 → 98.62 |
| | GBDT, paper-1 features | 0.005 | 0.007 | 0.985 | 99 % | 98.62 → 99.03 |
| | GBDT, paper 1 + MC dropout | 0.004 | 0.006 | 0.989 | 98 % | 98.62 → 99.30 |
| | GBDT, paper 1 + paper 2 | 0.005 | 0.006 | 0.988 | 99 % | 98.62 → 99.25 |
| | **GBDT, all features** | **0.003** [0.002–0.005] | **0.004** | **0.998** | 99 % | 98.62 → **99.67** |
| | decision tree, all (depth 5) | 0.005 | 0.009 | 0.947 | 91 % | 98.62 → 98.65 |
| category right (182) | raw softmax | 0.185 | 0.144 | 0.669 | 14 % | 96.86 → 96.86 |
| | GBDT, paper-1 features | 0.007 | 0.022 | 0.937 | 80 % | 96.86 → 97.23 |
| | GBDT, paper 1 + paper 2 | 0.009 | 0.015 | 0.955 | 85 % | 96.86 → 98.01 |
| | **GBDT, all features** | 0.006 | 0.008 | **0.989** | 98 % | 96.86 → **99.03** |
| | decision tree, all | 0.005 | 0.012 | 0.950 | 92 % | 96.86 → 98.39 |
| exact (343) | raw softmax | 0.163 | 0.149 | 0.713 | 15 % | 94.09 → 94.08 |
| | GBDT, paper-1 features | 0.006 | 0.027 | 0.947 | 79 % | 94.09 → 95.38 |
| | GBDT, paper 1 + paper 2 | 0.008 | 0.017 | 0.975 | 91 % | 94.09 → 97.25 |
| | **GBDT, all features** | 0.006 | 0.009 | **0.991** | 97 % | 94.09 → **98.27** |
| | decision tree, all | 0.006 | 0.020 | 0.946 | 85 % | 94.09 → 96.79 |

Locale shift (forecaster fitted on en-GB only, scored on en-US): is-PHI ECE 0.005 / AUROC 0.987; category
0.011 / 0.984; exact 0.014 / 0.990 (raw softmax: 0.195 / 0.765). Most useful features (permutation importance,
is-PHI): MC-dropout mean P(O), fused rule score, geometric-mean probability, rule id, previous word's probability of
the same category, letter fraction, span length, position in the note.

The depth-5 tree reads as rules a reviewer can check. Its first split is the fused score (0.908; rule spans score
1.0), then the MC-dropout mean P(O) of the span. A span with fused score ≤ 0.908, mean P(O) above 0.192 and maximum
word entropy ≤ 1.233 is right only 22 % of the time (41 spans); the largest leaf, fused score above 0.969 and mean
P(O) ≤ 0.398, holds 5,024 spans with confidence 1.000 to three decimals.

**Missed PHI.** 838 candidates in 1,000 notes, 94 containing missed PHI. 110 gold spans are left (partly)
uncovered by the detector; 93 of them (85 %) have a candidate.

| Candidate forecaster | AUROC | AUPRC | missed found in top 10 % / 20 % of candidates | add p ≥ 0.5: added / truly missed / precision |
|---|---|---|---|---|
| PHI mass only | 0.889 | 0.464 | 53 % / 73 % | 131 / 63 / 48 % |
| paper-1 features | 0.915 | 0.735 | 62 % / 80 % | 69 / 54 / 78 % |
| paper 1 + paper 2 | 0.939 | 0.835 | 71 % / 89 % | 76 / 62 / 82 % |
| **all** | **0.977** | **0.912** | 79 % / 97 % | 86 / 75 / **87 %** |

Adding the p ≥ 0.5 candidates adds 75 of the 94 candidates that contain missed PHI (80 %) at 87 % precision. Note-level leak risk:
98 of 1,000 notes contain a miss; P(≥ 1 miss) has AUROC 0.947 (candidate count alone: 0.771), ECE 0.025;
reviewing the riskiest 10 % of notes finds 81 % of all missed spans, 20 % finds 89 %.

**Hard negatives and cost.** 15 of the 1,000 labelled hard negatives were redacted; the confidence layer flags 13
of the 15 for review. Per note on CPU: rules 9 ms, model 0.40 s, MC dropout with 10 passes 4.5 s.

### 5.2 Test split (single run; full tables in `results/RESULTS_test_v5.md`)

Nothing was refitted: rules and settings from `train`, forecasters and thresholds from `cal`. The baseline row
re-runs the repo's shipped rules and settings on the same notes (code-level guards added during the project also
apply to it, worth ≈ 9 false alarms per 1,000 notes on `cal`).

**Detector** (1,008 notes, 5,790 gold spans).

| System | PHI recall (chars) [95 % CI] | Non-PII redaction | Strict category P / R / F1 | False alarms | Hard negatives redacted |
|---|---|---|---|---|---|
| Baseline: repo rules + model, as shipped | 91.1 % [90.5–91.7] | 0.30 % | 73.3 / 74.2 / 73.8 | 244 | 32 / 1008 |
| MedDeID rules only | 94.1 % [93.5–94.8] | 0.04 % | 97.6 / 91.6 / 94.5 | 9 | 0 / 1008 |
| Model only | 83.4 % [82.5–84.3] | 0.03 % | 73.2 / 69.0 / 71.0 | 51 | 11 / 1008 |
| **MedDeID rules + model** | **98.5 % [98.3–98.9]** | 0.07 % | 94.1 / 94.9 / **94.5** | 60 | 11 / 1008 |

Per label the picture matches `cal`: Dates 100 %, patient IDs 100 %, contact details 100 %, patient names 99.8 %;
the weak labels are `Address_Location:Other` (90.0 % found, 60 spans), `ID:Caregiver` (94.1 %), `Name:Other`
(95.9 %) and `Name:Caregiver` (97.2 %). Locale: en-GB 98.8 %, en-US 98.3 %. Document types: 97.7 % (referral
letters) to 99.6 % (laboratory reports).

**Confidence of predicted spans** (5,838 spans; forecasters fitted on `cal`, applied once).

| Target (errors) | Score | ECE [95 % CI] | Brier | AUROC(error) | errors caught @5 / 10 / 20 % review | precision before → after |
|---|---|---|---|---|---|---|
| is PHI (62) | raw softmax | 0.203 [0.195–0.212] | 0.132 | 0.752 | 16 / 19 / 26 % | 98.94 → 98.94 |
| | raw fused score | 0.008 [0.007–0.011] | 0.010 | 0.889 | 76 / 84 / 85 % | 98.94 → 98.99 |
| | **forecaster (GBDT, all features)** | **0.003** [0.002–0.005] | **0.003** | **0.998** | 100 / 100 / 100 % | 98.94 → **99.72** |
| category right (179) | raw softmax | 0.183 [0.175–0.192] | 0.143 | 0.673 | 9 / 10 / 16 % | 96.93 → 96.93 |
| | raw fused score | 0.018 [0.015–0.022] | 0.022 | 0.935 | 75 / 91 / 92 % | 96.93 → 97.01 |
| | **forecaster** | **0.0045** [0.003–0.007] | **0.006** | **0.997** | 98 / 99 / 100 % | 96.93 → **99.07** |
| exact (342) | raw softmax | 0.160 [0.151–0.170] | 0.148 | 0.714 | 6 / 14 / 29 % | 94.14 → 94.14 |
| | raw fused score | 0.045 [0.038–0.051] | 0.046 | 0.807 | 54 / 65 / 68 % | 94.14 → 94.27 |
| | **forecaster** | **0.005** [0.004–0.009] | **0.007** | **0.997** | 84 / 98 / 100 % | 94.14 → **98.97** |

Every one of the 62 non-PHI spans is among the 5 % least-confident spans, so a reviewer who looks at 292 of the
5,838 spans sees all of them. Dropping the 51 least-confident spans removes 46 of the 62 and 5 true spans, raising
precision from 98.94 % to 99.72 %. The 51 is the largest number that loses at most 0.1 % of the true spans and is
chosen with the answer key, so the "after" precision column shows what the score makes possible rather than a fixed
threshold; the deliverable sends spans below 0.9 to review instead of dropping them.

The raw softmax is miscalibrated mostly by being *under*-confident: rule-backed spans get a low model probability but
are almost always right (on test, the 356 spans it rates below 0.05 are right 97 % of the time, the 235 it rates at
0.45–0.50 are right 99.6 % of the time).

Calibration per category on the test split (is-PHI target; `Other` = the repo's OTHER_PHI label, which has no
MedDeID category and is where most of the remaining false alarms sit):

| Category | spans | errors | ECE raw softmax | ECE forecaster |
|---|---|---|---|---|
| ID, Contactdetails, Profession | 1,564 | 0 | – | – |
| Address_Location | 486 | 2 | 0.205 | 0.004 |
| Age_Birthdate | 441 | 1 | 0.538 | 0.002 |
| Date | 519 | 1 | 0.002 | 0.001 |
| Name | 2160 | 27 | 0.149 | 0.005 |
| Organization | 573 | 13 | 0.358 | 0.003 |
| Other | 95 | 18 | 0.098 | 0.035 |

Reliability diagram: `results/confidence/test_v5.rules+model.y_is_phi/reliability.png`.

**Missed PHI** (candidate forecaster and thresholds from `cal`).

| | `cal` | `test` |
|---|---|---|
| candidates / containing missed PHI | 838 / 94 | 877 / 99 |
| gold spans left uncovered by the detector / with a candidate | 110 / 93 (85 %) | 114 / 98 (86 %) |
| candidate AUROC / AUPRC (PHI mass only) | 0.889 / 0.464 | 0.858 / 0.375 |
| candidate AUROC / AUPRC (forecaster) | 0.977 / 0.912 | **0.990 / 0.945** |
| add at p ≥ 0.5: added / truly missed / precision | 86 / 75 / 87 % | 80 / 76 / **95 %** |
| candidates containing missed PHI that are added | 75 of 94 (80 %) | 76 of 99 (77 %) |
| notes with a miss; note-risk AUROC (candidate count) | 98; 0.947 (0.771) | 98; **0.964** (0.770) |
| note-risk ECE | 0.025 | 0.026 |
| missed spans in riskiest 5 / 10 / 20 % of notes | 52 / 81 / 89 % | 53 / 84 / 93 % |

**Before and after the forecasters** (`python -m deidconf.before_after`; full table in
`results/before_after/test_v5/report.md`). Same rules and model in both columns; nothing refitted.

| Use of the forecasters | Measure | Before | After |
|---|---|---|---|
| span confidence | ECE: is PHI / category / exact | 0.203 / 0.183 / 0.160 | 0.003 / 0.0045 / 0.005 |
| | AUROC for ranking wrong spans (is PHI) | 0.752 | 0.998 |
| | not-PHI spans among the 10 % least confident | 19 % | 100 % |
| drop the 51 least-confident spans | precision | 98.94 % | 99.72 % (5 true spans lost) |
| | false alarms (spans touching no PHI) | 60 | 14 |
| add candidates at p ≥ 0.5 | PHI recall (characters) | 98.5 % | 99.5 % |
| | gold spans with uncovered letters or digits | 114 | 40 |
| | non-PII redaction | 0.071 % | 0.073 % |
| | additions that are real missed PHI | – | 76 of 80 |
| note risk | missed spans in the riskiest 10 % of notes | – | 84 % |

With both drop and add: PHI recall 99.4 %, 45 gold spans with uncovered letters or digits, 14 false alarms. Adding
the candidates takes recall past the 99.0 % of the untrimmed union of rules and model, which has 87 false alarms.

**Hard negatives and cost.** 11 of 1,008 labelled hard negatives redacted; 9 of the 11 flagged for review by the
confidence layer. Per note on CPU: rules 17 ms, model 0.35 s, MC dropout with 10 passes 4.3 s.

## 6. Discussion

**What the detector changes bought.** The shipped repo reached 91 % character recall on MedDeID with 251 false
alarms per 1,000 notes; most of the gap was guideline mismatch (titles, states, all ages, `Occupation:`), UK
identifiers the HIPAA-oriented rules never saw, and generic organisation rules that fired on specialties. 43
guideline-specific rules written on `train` plus a handful of post-processing switches took recall to 98.5 % and
strict F1 from 74 % to 94.5 % on `cal`, with fewer false alarms and fewer hard negatives redacted. The rules alone are
precise (97.6 % strict precision) but miss 6 % of PHI; the model alone misses 16 %; their union is what works, and
the confidence layer is what makes the union safe.

**What paper 1 contributed.** The forecaster idea is the core of the span confidence: a small gradient-boosted model
on held-out predictions turns a softmax that is badly calibrated (ECE ≈ 0.20, mostly because rule-backed spans carry
a low model probability yet are right, and partly because some model errors get a high probability) into a
probability with ECE ≈ 0.005 and an
error-ranking AUROC of 0.985 from the paper's own features alone. Temperature and Platt scaling cannot do this: they
re-map one number, and a rule-backed span with model probability zero is still correct. The MC-dropout features
sharpened the is-PHI forecaster a little (AUROC 0.985 → 0.989, Brier 0.0072 → 0.0058) and nothing on the exact
target, at ten times the model cost (4.5 s vs 0.4 s per note); the tree nevertheless chose MC mean P(O) as its
second split, so the signal is real but mostly redundant with the single-pass probabilities and the neighbourhood
features. A span-only forecaster without the MC columns (paper 1 + paper 2 + ours) is almost as good on `cal`
(is-PHI ECE 0.0043 vs 0.0033, AUROC 0.996 vs 0.998), so MC dropout is not what makes the span scores work. The saved
forecasters used for every test number, including the missed-PHI forecaster, were fitted *with* the MC features, so the
deliverable pipeline runs the same 10 passes by default; its single-pass mode (`--mc-passes 0`) is ten times faster but
was not evaluated, and a check on one test note showed it failing to flag two missed names that the 10-pass pipeline
flags at p = 0.99. A no-MC missed-PHI forecaster would have to be fitted and evaluated before it could be recommended.

**What paper 2 contributed.** The PDM and entropy features matter most where the error is *not* "is this PHI" but
"is the boundary / category right": on the exact target they lift AUROC from 0.947 to 0.975 and the precision after
pruning from 95.4 % to 97.3 %. The paper's "semantic pull" shows up directly: the previous word's probability of the
same category and the first PDM bin are among the top features. The depth-5 tree, the paper's explainable
classifier, is a few points worse than the GBDT (AUROC 0.95 vs 0.99) but its leaves are statements a reviewer can
read ("model-only span, neighbourhood confident, mean P(O) above 0.19 → right 22 % of the time").

**What our features and our addition contributed.** Knowing *which rule* produced a span, whether the model agreed,
how often the string repeats in the note, and its case pattern is the single most useful group (AUROC 0.995 alone
on is-PHI); combined with the two papers' features it gives the final forecaster. The missed-PHI side has no
counterpart in either paper: 85 % of the spans the detector leaves uncovered are reachable as candidates, the
candidate forecaster adds 80 % of the candidates that contain missed PHI, at 87 % precision, when adding at p ≥ 0.5, and the note-level risk puts
81 % of all misses in the 10 % of notes it ranks riskiest. That is the number a reviewer with a fixed budget needs.

**Where it fails.** (i) The 14 % of misses with no candidate (16 of 114 on `test`): three professions the model does
flag (mass about 0.99) but on its occupation tags, which the repo's label map ignores because they also fire on
caregiver roles; ten spans the detector *partly* covers where the missing piece is an age unit ("y/o", "wk old";
mass 0.01–0.11) or a connecting word or tail of a hospital name ("and", "of", "Clinic"; 0.002–0.02); two
lower-case names with mass of about 0.005; and one name tail ("SENIOR", 0.51). No re-scoring can recover what is
never proposed. (ii) Categories with very few errors on `cal` (dates, ages) give the forecaster almost nothing to learn
from; their confidences are high and, on this corpus, right, but the CIs are wide. (iii) The forecaster's view of
rule errors is optimistic because the rules were tuned on the same corpus's train split. (iv) The locale shift test
(fit on en-GB, score on en-US) is reassuring (ECE ≤ 0.014, AUROC ≥ 0.984 on all three targets) but is a mild shift;
a different note-writing style would be a harder one.

**Test split.** The single test run reproduces the calibration numbers almost exactly (detector 98.5 % recall and
94.5 % strict F1 on both; is-PHI ECE 0.003 on both; near-miss AUROC 0.977 → 0.990, note-risk AUROC 0.947 →
0.964). Nothing was refitted, so these are the numbers to quote: the forecasters fitted on 1,000 calibration notes
transfer to unseen notes of the same corpus without loss. The one soft spot is the `Other` category (OTHER_PHI
spans, 95 on test, 18 of them wrong): the forecaster's ECE there is 0.035, ten times the overall value, because
`cal` had few examples of it.

## 7. Limitations
- Synthetic notes, written by a language model; results do not transfer to real clinical text without local
  validation (the corpus authors say the same).
- The rules were developed on this corpus's train split, so rule-only spans are nearly always right here; on notes
  from another hospital the confidence layer would see more rule errors than it saw in training.
- The detector cannot distinguish `Name:Patient` from `Name:Caregiver` / `Name:Other`; we score at MedDeID's eight
  top-level categories.
- Few errors on the calibration split for the strictest target (dozens, not thousands); confidence intervals are
  reported.
- Temperature scaling is reported as worse than the raw score because rule-only spans carry a model probability of
  zero for their category; a probability-only method cannot represent a rule.
- The saved forecasters need the 10 MC-dropout passes (about 4.3 s per note on CPU); a single-pass version was not
  evaluated.
- The "precision after dropping" numbers use a cut chosen with the answer key (at most 0.1 % of true spans lost);
  they show what the score allows, not a fixed operating threshold.
- The official 300-note MedDeID benchmark was not scored; all results are on our split of the 6,700-note corpus.

## 8. Reproduction
```
python -m deidconf.prepare                      # split (once)
python -m deidconf.detect --split cal           # model pass, cached
python -m deidconf.mcdropout --split cal        # 10 passes; the saved forecasters use these features
python -m deidconf.evaluate --split cal --rules baseline --model redecode --tag ""   # shipped repo
python -m deidconf.evaluate --split cal --rules live --model redecode --tag _v5
python -m deidconf.features --split cal --eval-tag _v5
python -m deidconf.confidence --features results/features/cal_v5.rules+model.csv --target y_is_phi --save
#   (repeat for --target y_cat_ok and y_exact)
python -m deidconf.nearmiss --split cal --eval-tag _v5 --save
python -m deidconf.robustness --split cal --eval-tag _v5
python -m deidconf.report --split cal --eval-tag _v5 --baseline-tag ""
MC=1 scripts/run_test.sh                        # the single test run, with MC dropout on test
python -m deidconf.annotate --split test --tag _v5      # per-note view
python -m deidconf.before_after --split test --tag _v5  # before / after table
python -m deidconf.figures --split test --tag _v5       # figures in results/figures/
python -m pytest                                # 43 unit tests
```
