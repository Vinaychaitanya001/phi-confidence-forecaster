# Existing detector on MedDeID `test` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **91.1%** [90.5%–91.7%] | 0.30% [0.25%–0.34%] | 73.3% / 74.2% / 73.8% | 5863 | 244 | 0.35 |
| rules+model(all) | **93.7%** [93.2%–94.2%] | 0.32% [0.28%–0.36%] | 73.0% / 77.6% / 75.2% | 6148 | 272 | 0.35 |
| rules-only | **69.6%** [68.5%–70.7%] | 0.23% [0.19%–0.27%] | 76.7% / 54.4% / 63.7% | 4107 | 176 | 0.35 |
| model-only | **83.3%** [82.4%–84.2%] | 0.07% [0.06%–0.08%] | 71.1% / 67.0% / 69.0% | 5461 | 69 | 0.35 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 1125 | 89.7% | 7.0% | 3.3% | 94.8% | 88.1% |
| Name:Caregiver | 636 | 55.2% | 30.8% | 14.0% | 77.2% | 47.3% |
| Name:Other | 442 | 77.4% | 9.3% | 13.3% | 81.0% | 72.9% |
| Address_Location:Patient | 373 | 100.0% | 0.0% | 0.0% | 100.0% | 96.8% |
| Address_Location:Caregiver | 47 | 89.4% | 0.0% | 10.6% | 78.7% | 76.6% |
| Address_Location:Other | 60 | 86.7% | 0.0% | 13.3% | 76.7% | 71.7% |
| Organization:Healthcare | 452 | 84.3% | 15.3% | 0.4% | 98.5% | 83.2% |
| Organization:Other | 105 | 89.5% | 8.6% | 1.9% | 91.4% | 84.8% |
| ID:Patient | 919 | 96.6% | 2.4% | 1.0% | 87.8% | 85.3% |
| ID:Caregiver | 187 | 70.6% | 0.0% | 29.4% | 63.6% | 63.6% |
| Date | 518 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 444 | 49.3% | 49.8% | 0.9% | 75.2% | 2.5% |
| Contactdetails | 347 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Profession | 135 | 4.4% | 0.0% | 95.6% | 0.0% | 0.0% |
| **all** | 5790 | 82.1% | | 6.9% | 87.0% | 74.2% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 3425 | 100.0% | 96.8% | 82.3% | 1 |
| model | 1756 | 96.1% | 76.0% | 63.8% | 68 |
| rules | 682 | 74.3% | 59.2% | 52.5% | 175 |
| Address_Location | 501 | 99.8% | 91.0% | 87.8% | 1 |
| Age_Birthdate | 335 | 99.7% | 99.7% | 3.3% | 1 |
| Contactdetails | 451 | 100.0% | 76.9% | 76.9% | 0 |
| Date | 646 | 96.6% | 80.2% | 80.2% | 22 |
| ID | 935 | 100.0% | 100.0% | 96.6% | 0 |
| Name | 1962 | 98.3% | 97.7% | 82.3% | 33 |
| Organization | 735 | 77.0% | 74.8% | 63.3% | 169 |
| Other | 298 | 94.0% | 0.0% | 0.0% | 18 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 504 | 90.6% | 0.26% |
| en-US | 504 | 91.5% | 0.33% |
| clinic_note | 168 | 86.8% | 0.44% |
| discharge_summary | 168 | 93.7% | 0.13% |
| emergency_note | 168 | 92.8% | 0.13% |
| laboratory_report | 168 | 92.7% | 0.95% |
| nursing_note | 168 | 93.9% | 0.09% |
| referral_letter | 168 | 86.9% | 0.14% |

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
| impossible_date | 22 | 21 | 95.5% | Date:21 |
| ambiguous_month_word | 17 | 0 | 0.0% |  |
| laboratory_code | 11 | 0 | 0.0% |  |
| device_model | 6 | 0 | 0.0% |  |
| **all** | 1008 | 32 | 3.2% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
