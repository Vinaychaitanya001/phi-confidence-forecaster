"""deidconf: confidence-aware clinical de-identification on the MedDeID English synthetic corpus.

Detector: the existing OpenMed FastClinical-82M model from the `Deidentification` repo, used exactly as published
(no training), plus that repo's regex rules extended with a MedDeID rule set
(`Deidentification/src/deid/detectors/meddeid_rules.py`). Everything about confidence lives here.

Modules (in pipeline order)
  data        corpus reader, 14 labels, deterministic train / cal / test split
  prepare     build the split (run once)
  detect      run rules + model on a split; cache spans and the full per-word probability matrix
  mcdropout   N stochastic passes with dropout on (paper 1 uncertainty)
  evaluate    fusion / post-processing offline, detector metrics (MedDeID's character-level metrics, per label,
              hard negatives), several system variants from one model pass
  errors      error analysis used to write rules (on `train` only)
  features    per predicted span: paper 1 + paper 2 + our features, three targets
  confidence  baselines, GBDT / decision-tree forecasters, ablations, ECE / Brier / AUROC / review curves;
              --save to persist, --apply for the single final run on `test`
  nearmiss    our addition: candidates the detector did not predict, missed-PHI forecaster, note-level leak risk
  robustness  hard negatives after confidence, cost per note, shift experiments
  report      one Markdown results document per split
  pipeline    end-to-end: new note -> spans with confidences, possible misses, note risk, de-identified text
  annotate    readable per-note view of a scored split (saved outputs only)
  before_after  the detector alone vs with the forecasters (drop low-confidence spans, add missed-PHI candidates)
  figures     the result figures in results/figures/
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
