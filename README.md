# phi-confidence-forecaster

Confidence-aware clinical de-identification on the MedDeID English synthetic corpus.

An existing de-identification system (regex rules + the OpenMed FastClinical-82M token classifier, used as
published, no training) is extended with a **confidence layer**: for every predicted PHI span it reports how likely
the span is PHI, how likely the category is right and how likely the boundaries are exact. It also estimates **what
the detector missed** (near-miss candidates and a note-level leak risk). Spans below a confidence threshold are
flagged for review instead of being trusted.

Method: a gradient-boosted *forecaster* on held-out predictions with MC-dropout, neighbourhood probability-density
and rule/context features, following
[Jagannatha & Yu, ACL 2020](https://aclanthology.org/2020.acl-main.188/) (calibration of structured predictors) and
Jiwani et al., 2026, arXiv 2603.00022 (noise reduction in BERT NER with probability density maps and decision trees).

## Results (held-out test split, 1,008 notes, single run)

| | Baseline (repo as shipped) | This work |
|---|---|---|
| PHI recall (chars) | 91.1 % | **98.5 %** |
| Strict category F1 | 73.8 % | **94.5 %** |
| False alarms | 244 | **60** |
| Span confidence ECE (is PHI) | 0.203 (raw softmax) | **0.003** |
| AUROC for "span is wrong" | 0.752 | **0.998** |
| Missed-PHI candidates, AUROC / precision at p >= 0.5 | n/a | 0.990 / 95 % |
| PHI recall with those candidates added | n/a | **99.5 %** (gold spans missed: 114 → 40) |

Full write-up: [REPORT.md](REPORT.md). Tables: `results/RESULTS_cal_v5.md`, `results/RESULTS_test_v5.md`, and the
before / after table for the forecasters in `results/before_after/test_v5/report.md`.
Synthetic notes only; results do not transfer to real clinical text without local validation.

## Layout

- `deidconf/` confidence layer: `detect`, `mcdropout`, `evaluate`, `features`, `confidence`, `nearmiss`, `robustness`, `report`, `pipeline`, plus `annotate`, `before_after`, `figures` for reading the results
- `Deidentification/` the base system with our changes (43 MedDeID regex rules in `src/deid/detectors/meddeid_rules.py`)
- `scripts/run_test.sh` the single final test run; `tests/` unit tests
- `demo/` a test note and the saved pipeline output; `results/figures/` result figures (`python -m deidconf.figures`)
- `results/` reports and the saved forecasters (large caches are not committed)
- `results/annotated/test_v5_examples.md` test notes with every predicted span, its confidence and verdict, and the missed PHI; `python -m deidconf.annotate` writes the full per-note file for all notes

## Reproduce

Get the corpus from https://huggingface.co/datasets/stighellemans/meddeid-english-synthetic-corpus (CC BY 4.0) into
`meddeid_english_synthetic/`, then:

```
pip install -e . -e Deidentification
python -m deidconf.prepare && python -m deidconf.detect --split cal
python -m deidconf.evaluate --split cal --rules live --model redecode --tag _v5
python -m deidconf.features --split cal --eval-tag _v5
python -m deidconf.confidence --features results/features/cal_v5.rules+model.csv --target y_is_phi --save
# runs 10 MC-dropout passes by default (about 4 s per note), the setting the saved forecasters were fitted with
python -m deidconf.pipeline --text "Patient: Okkes Reilly, seen by Dr Amelia Hart at St Mary's Hospital, Leeds."
python -m deidconf.annotate --split test --tag _v5       # per-note annotated view
python -m deidconf.before_after --split test --tag _v5   # before / after table (needs the annotated file)
python -m pytest                                         # 43 unit tests
```

The base system is a clone of https://github.com/narsing64/Deidentification with our modifications.
