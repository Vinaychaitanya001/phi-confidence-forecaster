# Existing detector on MedDeID `train_rules_v2` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules-only | **92.7%** [92.4%–93.0%] | 0.34% [0.32%–0.36%] | 89.7% / 89.2% / 89.4% | 26902 | 1896 | 0.02 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 5251 | 94.3% | 0.1% | 5.5% | 94.1% | 93.9% |
| Name:Caregiver | 3031 | 80.8% | 0.0% | 19.2% | 79.9% | 73.4% |
| Name:Other | 2041 | 67.8% | 0.1% | 32.0% | 67.8% | 63.3% |
| Address_Location:Patient | 1694 | 97.4% | 1.8% | 0.8% | 99.2% | 93.0% |
| Address_Location:Caregiver | 231 | 82.3% | 0.4% | 17.3% | 74.0% | 73.6% |
| Address_Location:Other | 311 | 69.8% | 1.0% | 29.3% | 69.8% | 63.3% |
| Organization:Healthcare | 2065 | 87.4% | 8.2% | 4.4% | 93.8% | 83.0% |
| Organization:Other | 512 | 86.9% | 0.0% | 13.1% | 86.5% | 84.6% |
| ID:Patient | 4401 | 97.9% | 1.8% | 0.3% | 99.4% | 97.5% |
| ID:Caregiver | 944 | 85.6% | 0.0% | 14.4% | 84.0% | 83.9% |
| Date | 2400 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 2015 | 98.6% | 0.6% | 0.8% | 99.1% | 98.4% |
| Contactdetails | 1478 | 99.5% | 0.5% | 0.0% | 99.2% | 98.6% |
| Profession | 667 | 98.5% | 0.0% | 1.5% | 98.5% | 98.5% |
| **all** | 27041 | 91.4% | | 7.4% | 92.0% | 89.2% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| model | 772 | 71.2% | 71.2% | 71.2% | 222 |
| rules | 26130 | 93.6% | 93.2% | 90.2% | 1674 |
| Address_Location | 2192 | 97.1% | 94.7% | 88.6% | 64 |
| Age_Birthdate | 2000 | 99.8% | 99.8% | 99.2% | 4 |
| Contactdetails | 1490 | 100.0% | 98.4% | 97.9% | 0 |
| Date | 2403 | 100.0% | 99.9% | 99.9% | 1 |
| ID | 5167 | 100.0% | 100.0% | 98.4% | 0 |
| Name | 10473 | 83.7% | 83.5% | 80.7% | 1702 |
| Organization | 2513 | 95.3% | 94.7% | 85.4% | 119 |
| Profession | 664 | 99.1% | 98.9% | 98.9% | 6 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 2346 | 93.4% | 0.36% |
| en-US | 2346 | 92.0% | 0.32% |
| clinic_note | 782 | 96.1% | 0.20% |
| discharge_summary | 782 | 93.2% | 0.19% |
| emergency_note | 782 | 91.2% | 0.19% |
| laboratory_report | 782 | 95.6% | 0.19% |
| nursing_note | 782 | 92.2% | 0.41% |
| referral_letter | 782 | 88.4% | 0.83% |

## 5. Hard negatives wrongly redacted (rules+model)

| Hard-negative type | n | Redacted | Rate | Redacted as |
|---|---|---|---|---|
| duration | 888 | 0 | 0.0% |  |
| relative_time | 819 | 0 | 0.0% |  |
| medication | 586 | 0 | 0.0% |  |
| measurement | 343 | 0 | 0.0% |  |
| vital_sign | 332 | 0 | 0.0% |  |
| time | 327 | 0 | 0.0% |  |
| pain_score | 275 | 0 | 0.0% |  |
| caregiver_role | 198 | 1 | 0.5% | Name:1 |
| eponym | 191 | 0 | 0.0% |  |
| gestational_age | 140 | 4 | 2.9% | Age_Birthdate:4 |
| gene_variant | 128 | 0 | 0.0% |  |
| terminology_code | 124 | 1 | 0.8% | Name:1 |
| clinical_scale | 117 | 0 | 0.0% |  |
| laboratory_code | 80 | 0 | 0.0% |  |
| ambiguous_month_word | 62 | 0 | 0.0% |  |
| impossible_date | 51 | 0 | 0.0% |  |
| device_model | 31 | 0 | 0.0% |  |
| **all** | 4692 | 6 | 0.1% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
