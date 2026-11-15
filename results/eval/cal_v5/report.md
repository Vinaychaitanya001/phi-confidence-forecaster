# Existing detector on MedDeID `cal_v5` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **98.5%** [98.2%–98.8%] | 0.09% [0.07%–0.11%] | 94.1% / 94.9% / 94.5% | 5800 | 72 | 0.43 |
| rules+model(all) | **99.1%** [98.8%–99.3%] | 0.11% [0.09%–0.13%] | 93.3% / 95.5% / 94.4% | 5887 | 100 | 0.43 |
| rules-only | **94.1%** [93.5%–94.8%] | 0.06% [0.04%–0.07%] | 97.6% / 91.6% / 94.5% | 5398 | 16 | 0.43 |
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
| Organization:Healthcare | 435 | 93.1% | 6.4% | 0.5% | 98.2% | 85.1% |
| Organization:Other | 98 | 88.8% | 10.2% | 1.0% | 92.9% | 85.7% |
| ID:Patient | 921 | 99.9% | 0.0% | 0.1% | 99.9% | 99.8% |
| ID:Caregiver | 167 | 89.8% | 0.0% | 10.2% | 88.0% | 88.0% |
| Date | 523 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 470 | 98.7% | 1.1% | 0.2% | 99.6% | 98.5% |
| Contactdetails | 317 | 100.0% | 0.0% | 0.0% | 98.7% | 98.7% |
| Profession | 123 | 97.6% | 0.0% | 2.4% | 97.6% | 97.6% |
| **all** | 5750 | 97.2% | | 1.1% | 97.7% | 94.9% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 4073 | 100.0% | 99.9% | 98.5% | 1 |
| model | 528 | 89.4% | 70.8% | 58.3% | 56 |
| rules | 1199 | 98.7% | 98.5% | 94.8% | 15 |
| Address_Location | 492 | 99.8% | 96.3% | 92.3% | 1 |
| Age_Birthdate | 478 | 97.9% | 97.9% | 96.9% | 10 |
| Contactdetails | 314 | 100.0% | 99.7% | 99.7% | 0 |
| Date | 526 | 99.6% | 99.4% | 99.4% | 2 |
| ID | 1067 | 100.0% | 100.0% | 99.9% | 0 |
| Name | 2174 | 98.8% | 98.4% | 94.9% | 27 |
| Organization | 543 | 96.7% | 95.9% | 83.6% | 18 |
| Other | 86 | 83.7% | 0.0% | 0.0% | 14 |
| Profession | 120 | 100.0% | 100.0% | 100.0% | 0 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 500 | 98.8% | 0.10% |
| en-US | 500 | 98.2% | 0.09% |
| clinic_note | 168 | 98.9% | 0.04% |
| discharge_summary | 168 | 99.0% | 0.09% |
| emergency_note | 166 | 98.1% | 0.11% |
| laboratory_report | 166 | 99.8% | 0.14% |
| nursing_note | 166 | 98.2% | 0.07% |
| referral_letter | 166 | 97.3% | 0.10% |

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
