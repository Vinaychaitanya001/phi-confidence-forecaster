# Existing detector on MedDeID `test_v5` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **98.5%** [98.3%–98.9%] | 0.07% [0.06%–0.09%] | 94.1% / 94.9% / 94.5% | 5838 | 60 | 0.36 |
| rules+model(all) | **99.0%** [98.8%–99.3%] | 0.09% [0.07%–0.11%] | 93.6% / 95.5% / 94.5% | 5909 | 87 | 0.36 |
| rules-only | **94.1%** [93.5%–94.8%] | 0.04% [0.03%–0.06%] | 97.6% / 91.6% / 94.5% | 5436 | 9 | 0.36 |
| model-only | **83.4%** [82.5%–84.3%] | 0.03% [0.02%–0.04%] | 73.2% / 69.0% / 71.0% | 5457 | 51 | 0.36 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 1125 | 99.3% | 0.5% | 0.2% | 99.6% | 99.0% |
| Name:Caregiver | 636 | 93.9% | 3.3% | 2.8% | 94.0% | 87.7% |
| Name:Other | 442 | 89.6% | 6.3% | 4.1% | 92.5% | 87.1% |
| Address_Location:Patient | 373 | 100.0% | 0.0% | 0.0% | 100.0% | 95.2% |
| Address_Location:Caregiver | 47 | 97.9% | 0.0% | 2.1% | 87.2% | 87.2% |
| Address_Location:Other | 60 | 88.3% | 1.7% | 10.0% | 83.3% | 76.7% |
| Organization:Healthcare | 452 | 92.9% | 6.6% | 0.4% | 99.1% | 88.3% |
| Organization:Other | 105 | 90.5% | 7.6% | 1.9% | 92.4% | 85.7% |
| ID:Patient | 919 | 100.0% | 0.0% | 0.0% | 99.9% | 99.8% |
| ID:Caregiver | 187 | 94.1% | 0.0% | 5.9% | 90.4% | 90.4% |
| Date | 518 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 444 | 96.8% | 2.3% | 0.9% | 99.1% | 96.8% |
| Contactdetails | 347 | 100.0% | 0.0% | 0.0% | 98.6% | 98.6% |
| Profession | 135 | 97.8% | 0.0% | 2.2% | 97.8% | 97.8% |
| **all** | 5790 | 97.0% | | 1.2% | 97.7% | 94.9% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 4127 | 100.0% | 100.0% | 98.5% | 0 |
| model | 531 | 90.4% | 69.5% | 58.2% | 51 |
| rules | 1180 | 99.2% | 98.7% | 95.0% | 9 |
| Address_Location | 486 | 99.8% | 95.5% | 90.9% | 1 |
| Age_Birthdate | 441 | 99.8% | 99.8% | 97.5% | 1 |
| Contactdetails | 345 | 100.0% | 99.1% | 99.1% | 0 |
| Date | 519 | 99.8% | 99.8% | 99.8% | 1 |
| ID | 1087 | 100.0% | 100.0% | 99.9% | 0 |
| Name | 2160 | 98.8% | 98.5% | 95.2% | 26 |
| Organization | 573 | 97.7% | 96.0% | 85.3% | 13 |
| Other | 95 | 81.1% | 0.0% | 0.0% | 18 |
| Profession | 132 | 100.0% | 100.0% | 100.0% | 0 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 504 | 98.8% | 0.08% |
| en-US | 504 | 98.3% | 0.07% |
| clinic_note | 168 | 98.7% | 0.01% |
| discharge_summary | 168 | 98.7% | 0.09% |
| emergency_note | 168 | 98.3% | 0.09% |
| laboratory_report | 168 | 99.6% | 0.10% |
| nursing_note | 168 | 98.6% | 0.06% |
| referral_letter | 168 | 97.7% | 0.08% |

## 5. Hard negatives wrongly redacted (rules+model)

| Hard-negative type | n | Redacted | Rate | Redacted as |
|---|---|---|---|---|
| relative_time | 184 | 0 | 0.0% |  |
| duration | 176 | 0 | 0.0% |  |
| medication | 117 | 0 | 0.0% |  |
| time | 86 | 0 | 0.0% |  |
| vital_sign | 75 | 0 | 0.0% |  |
| measurement | 69 | 0 | 0.0% |  |
| pain_score | 56 | 0 | 0.0% |  |
| caregiver_role | 47 | 0 | 0.0% |  |
| eponym | 41 | 0 | 0.0% |  |
| clinical_scale | 26 | 0 | 0.0% |  |
| gestational_age | 26 | 0 | 0.0% |  |
| terminology_code | 25 | 6 | 24.0% | Other:6 |
| gene_variant | 24 | 5 | 20.8% | Other:5 |
| impossible_date | 22 | 0 | 0.0% |  |
| ambiguous_month_word | 17 | 0 | 0.0% |  |
| laboratory_code | 11 | 0 | 0.0% |  |
| device_model | 6 | 0 | 0.0% |  |
| **all** | 1008 | 11 | 1.1% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
