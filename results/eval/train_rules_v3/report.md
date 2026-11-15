# Existing detector on MedDeID `train_rules_v3` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules-only | **93.1%** [92.8%–93.5%] | 0.28% [0.26%–0.29%] | 88.9% / 90.4% / 89.6% | 27491 | 2393 | 0.02 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 5251 | 93.5% | 0.1% | 6.3% | 93.7% | 93.5% |
| Name:Caregiver | 3031 | 86.9% | 0.0% | 13.1% | 86.1% | 82.5% |
| Name:Other | 2041 | 70.2% | 0.4% | 29.4% | 70.5% | 70.0% |
| Address_Location:Patient | 1694 | 97.4% | 1.8% | 0.8% | 99.2% | 93.0% |
| Address_Location:Caregiver | 231 | 80.1% | 0.4% | 19.5% | 67.1% | 66.7% |
| Address_Location:Other | 311 | 47.6% | 0.3% | 52.1% | 46.9% | 41.2% |
| Organization:Healthcare | 2065 | 87.1% | 7.6% | 5.3% | 94.2% | 83.4% |
| Organization:Other | 512 | 86.7% | 0.0% | 13.3% | 86.5% | 84.6% |
| ID:Patient | 4401 | 97.9% | 1.8% | 0.3% | 99.4% | 97.5% |
| ID:Caregiver | 944 | 85.6% | 0.0% | 14.4% | 84.0% | 83.9% |
| Date | 2400 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 2015 | 98.6% | 0.6% | 0.8% | 99.1% | 98.4% |
| Contactdetails | 1478 | 99.5% | 0.5% | 0.0% | 99.2% | 98.6% |
| Profession | 667 | 98.5% | 0.0% | 1.5% | 98.5% | 98.5% |
| **all** | 27041 | 91.8% | | 7.0% | 92.5% | 90.4% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| model | 575 | 64.5% | 64.5% | 64.2% | 204 |
| rules | 26916 | 91.9% | 91.6% | 89.4% | 2189 |
| Address_Location | 1993 | 99.9% | 99.7% | 93.2% | 1 |
| Age_Birthdate | 2000 | 99.8% | 99.8% | 99.2% | 4 |
| Contactdetails | 1490 | 100.0% | 98.4% | 97.9% | 0 |
| Date | 2403 | 100.0% | 99.9% | 99.9% | 1 |
| ID | 5167 | 100.0% | 100.0% | 98.4% | 0 |
| Name | 11333 | 79.3% | 79.1% | 78.0% | 2343 |
| Organization | 2441 | 98.4% | 97.9% | 88.3% | 38 |
| Profession | 664 | 99.1% | 98.9% | 98.9% | 6 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 2346 | 94.0% | 0.31% |
| en-US | 2346 | 92.3% | 0.25% |
| clinic_note | 782 | 96.1% | 0.25% |
| discharge_summary | 782 | 92.4% | 0.34% |
| emergency_note | 782 | 92.0% | 0.16% |
| laboratory_report | 782 | 97.5% | 0.18% |
| nursing_note | 782 | 92.7% | 0.14% |
| referral_letter | 782 | 88.8% | 0.56% |

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
| terminology_code | 124 | 0 | 0.0% |  |
| clinical_scale | 117 | 0 | 0.0% |  |
| laboratory_code | 80 | 0 | 0.0% |  |
| ambiguous_month_word | 62 | 0 | 0.0% |  |
| impossible_date | 51 | 0 | 0.0% |  |
| device_model | 31 | 0 | 0.0% |  |
| **all** | 4692 | 5 | 0.1% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
