# Existing detector on MedDeID `train_v4` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **98.5%** [98.3%–98.6%] | 0.08% [0.07%–0.09%] | 93.7% / 94.8% / 94.2% | 27338 | 298 | 0.67 |
| rules+model(all) | **99.1%** [98.9%–99.2%] | 0.10% [0.09%–0.11%] | 92.9% / 95.4% / 94.1% | 27747 | 443 | 0.67 |
| rules-only | **93.9%** [93.5%–94.2%] | 0.05% [0.04%–0.06%] | 97.1% / 91.3% / 94.1% | 25418 | 77 | 0.67 |
| model-only | **82.4%** [81.9%–82.8%] | 0.03% [0.03%–0.04%] | 73.1% / 68.3% / 70.6% | 25276 | 224 | 0.67 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 5251 | 99.0% | 0.6% | 0.3% | 99.5% | 98.7% |
| Name:Caregiver | 3031 | 95.9% | 2.6% | 1.5% | 95.2% | 89.2% |
| Name:Other | 2041 | 90.5% | 6.4% | 3.1% | 92.6% | 87.1% |
| Address_Location:Patient | 1694 | 99.5% | 0.5% | 0.0% | 100.0% | 95.0% |
| Address_Location:Caregiver | 231 | 96.5% | 0.9% | 2.6% | 85.7% | 84.4% |
| Address_Location:Other | 311 | 92.3% | 0.3% | 7.4% | 87.5% | 81.7% |
| Organization:Healthcare | 2065 | 91.6% | 7.8% | 0.6% | 97.8% | 87.0% |
| Organization:Other | 512 | 90.8% | 8.4% | 0.8% | 93.0% | 88.3% |
| ID:Patient | 4401 | 98.4% | 1.5% | 0.1% | 99.6% | 98.0% |
| ID:Caregiver | 944 | 91.6% | 0.0% | 8.4% | 88.5% | 88.3% |
| Date | 2400 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 2015 | 98.6% | 0.7% | 0.7% | 99.2% | 98.4% |
| Contactdetails | 1478 | 100.0% | 0.0% | 0.0% | 99.2% | 99.1% |
| Profession | 667 | 98.5% | 0.0% | 1.5% | 98.5% | 98.5% |
| **all** | 27041 | 97.0% | | 1.0% | 97.6% | 94.8% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 19095 | 100.0% | 100.0% | 98.3% | 2 |
| model | 2465 | 91.0% | 69.5% | 57.0% | 222 |
| rules | 5778 | 98.7% | 97.8% | 94.4% | 74 |
| Address_Location | 2331 | 99.2% | 93.2% | 88.3% | 19 |
| Age_Birthdate | 2018 | 99.0% | 99.0% | 98.3% | 20 |
| Contactdetails | 1497 | 100.0% | 97.9% | 97.9% | 0 |
| Date | 2409 | 99.7% | 99.6% | 99.6% | 7 |
| ID | 5249 | 100.0% | 100.0% | 98.1% | 2 |
| Name | 10128 | 99.0% | 98.7% | 95.4% | 104 |
| Organization | 2610 | 97.4% | 96.4% | 86.1% | 68 |
| Other | 432 | 83.3% | 0.0% | 0.0% | 72 |
| Profession | 664 | 99.1% | 98.9% | 98.9% | 6 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 2346 | 98.6% | 0.09% |
| en-US | 2346 | 98.4% | 0.08% |
| clinic_note | 782 | 98.9% | 0.05% |
| discharge_summary | 782 | 98.6% | 0.08% |
| emergency_note | 782 | 98.0% | 0.09% |
| laboratory_report | 782 | 99.3% | 0.10% |
| nursing_note | 782 | 98.6% | 0.06% |
| referral_letter | 782 | 97.6% | 0.10% |

## 5. Hard negatives wrongly redacted (rules+model)

| Hard-negative type | n | Redacted | Rate | Redacted as |
|---|---|---|---|---|
| duration | 888 | 0 | 0.0% |  |
| relative_time | 819 | 0 | 0.0% |  |
| medication | 586 | 0 | 0.0% |  |
| measurement | 343 | 1 | 0.3% | Age_Birthdate:1 |
| vital_sign | 332 | 0 | 0.0% |  |
| time | 327 | 0 | 0.0% |  |
| pain_score | 275 | 0 | 0.0% |  |
| caregiver_role | 198 | 1 | 0.5% | Name:1 |
| eponym | 191 | 0 | 0.0% |  |
| gestational_age | 140 | 14 | 10.0% | Age_Birthdate:14 |
| gene_variant | 128 | 20 | 15.6% | Other:20 |
| terminology_code | 124 | 30 | 24.2% | Other:30 |
| clinical_scale | 117 | 0 | 0.0% |  |
| laboratory_code | 80 | 1 | 1.2% | ID:1 |
| ambiguous_month_word | 62 | 0 | 0.0% |  |
| impossible_date | 51 | 0 | 0.0% |  |
| device_model | 31 | 0 | 0.0% |  |
| **all** | 4692 | 67 | 1.4% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
