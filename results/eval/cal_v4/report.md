# Existing detector on MedDeID `cal_v4` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **98.2%** [97.9%–98.6%] | 0.09% [0.07%–0.11%] | 93.3% / 94.3% / 93.8% | 5813 | 72 | 0.43 |
| rules+model(all) | **98.9%** [98.6%–99.2%] | 0.11% [0.09%–0.13%] | 92.3% / 94.9% / 93.6% | 5910 | 100 | 0.43 |
| rules-only | **93.5%** [92.8%–94.2%] | 0.06% [0.04%–0.07%] | 97.0% / 90.9% / 93.9% | 5390 | 16 | 0.43 |
| model-only | **83.6%** [82.7%–84.6%] | 0.04% [0.02%–0.05%] | 72.8% / 69.1% / 70.9% | 5458 | 57 | 0.43 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 1110 | 98.7% | 1.0% | 0.3% | 99.6% | 98.6% |
| Name:Caregiver | 646 | 96.0% | 2.2% | 1.9% | 95.2% | 89.5% |
| Name:Other | 448 | 90.2% | 6.0% | 3.8% | 93.1% | 87.5% |
| Address_Location:Patient | 363 | 100.0% | 0.0% | 0.0% | 100.0% | 95.9% |
| Address_Location:Caregiver | 50 | 94.0% | 0.0% | 6.0% | 80.0% | 80.0% |
| Address_Location:Other | 79 | 92.4% | 1.3% | 6.3% | 88.6% | 83.5% |
| Organization:Healthcare | 435 | 89.0% | 10.1% | 0.9% | 96.8% | 80.9% |
| Organization:Other | 98 | 88.8% | 10.2% | 1.0% | 92.9% | 85.7% |
| ID:Patient | 921 | 98.3% | 1.5% | 0.2% | 99.8% | 98.2% |
| ID:Caregiver | 167 | 89.8% | 0.0% | 10.2% | 88.0% | 88.0% |
| Date | 523 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 470 | 98.7% | 1.1% | 0.2% | 99.6% | 98.5% |
| Contactdetails | 317 | 100.0% | 0.0% | 0.0% | 98.7% | 98.7% |
| Profession | 123 | 97.6% | 0.0% | 2.4% | 97.6% | 97.6% |
| **all** | 5750 | 96.6% | | 1.2% | 97.6% | 94.3% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 4079 | 100.0% | 99.9% | 98.1% | 1 |
| model | 549 | 89.8% | 69.2% | 56.1% | 56 |
| rules | 1185 | 98.7% | 98.4% | 93.9% | 15 |
| Address_Location | 504 | 99.8% | 94.0% | 90.1% | 1 |
| Age_Birthdate | 478 | 97.9% | 97.9% | 96.9% | 10 |
| Contactdetails | 317 | 100.0% | 98.7% | 98.7% | 0 |
| Date | 526 | 99.6% | 99.4% | 99.4% | 2 |
| ID | 1070 | 100.0% | 100.0% | 98.2% | 0 |
| Name | 2175 | 98.8% | 98.3% | 94.9% | 27 |
| Organization | 537 | 96.6% | 95.9% | 81.2% | 18 |
| Other | 86 | 83.7% | 0.0% | 0.0% | 14 |
| Profession | 120 | 100.0% | 100.0% | 100.0% | 0 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 500 | 98.4% | 0.10% |
| en-US | 500 | 98.0% | 0.09% |
| clinic_note | 168 | 98.6% | 0.04% |
| discharge_summary | 168 | 98.9% | 0.09% |
| emergency_note | 166 | 97.2% | 0.11% |
| laboratory_report | 166 | 99.6% | 0.14% |
| nursing_note | 166 | 98.0% | 0.07% |
| referral_letter | 166 | 97.2% | 0.10% |

## 5. Hard negatives wrongly redacted (rules+model)

| Hard-negative type | n | Redacted | Rate | Redacted as |
|---|---|---|---|---|
| duration | 177 | 0 | 0.0% |  |
| relative_time | 164 | 0 | 0.0% |  |
| medication | 129 | 0 | 0.0% |  |
| vital_sign | 77 | 0 | 0.0% |  |
| measurement | 73 | 0 | 0.0% |  |
| pain_score | 70 | 0 | 0.0% |  |
| time | 53 | 0 | 0.0% |  |
| eponym | 50 | 0 | 0.0% |  |
| caregiver_role | 47 | 1 | 2.1% | Organization:1 |
| gestational_age | 36 | 7 | 19.4% | Age_Birthdate:7 |
| gene_variant | 25 | 1 | 4.0% | Other:1 |
| clinical_scale | 22 | 0 | 0.0% |  |
| terminology_code | 22 | 6 | 27.3% | Other:6 |
| impossible_date | 18 | 0 | 0.0% |  |
| ambiguous_month_word | 16 | 0 | 0.0% |  |
| laboratory_code | 16 | 0 | 0.0% |  |
| device_model | 5 | 0 | 0.0% |  |
| **all** | 1000 | 15 | 1.5% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
