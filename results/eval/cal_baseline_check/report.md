# Existing detector on MedDeID `cal_baseline_check` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **91.4%** [90.8%–92.0%] | 0.31% [0.26%–0.35%] | 73.2% / 74.4% / 73.8% | 5845 | 242 | 0.41 |
| rules+model(all) | **94.1%** [93.6%–94.6%] | 0.33% [0.28%–0.37%] | 72.9% / 77.8% / 75.2% | 6134 | 270 | 0.41 |
| rules-only | **68.8%** [67.7%–70.1%] | 0.24% [0.19%–0.28%] | 76.4% / 53.5% / 63.0% | 4025 | 173 | 0.41 |
| model-only | **83.4%** [82.4%–84.3%] | 0.07% [0.06%–0.09%] | 70.5% / 66.8% / 68.6% | 5447 | 71 | 0.41 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 1110 | 88.0% | 7.7% | 4.2% | 93.6% | 86.0% |
| Name:Caregiver | 646 | 60.1% | 28.3% | 11.6% | 79.9% | 52.0% |
| Name:Other | 448 | 78.8% | 9.6% | 11.6% | 83.0% | 74.3% |
| Address_Location:Patient | 363 | 100.0% | 0.0% | 0.0% | 100.0% | 96.4% |
| Address_Location:Caregiver | 50 | 92.0% | 0.0% | 8.0% | 76.0% | 74.0% |
| Address_Location:Other | 79 | 91.1% | 1.3% | 7.6% | 86.1% | 81.0% |
| Organization:Healthcare | 435 | 80.9% | 17.9% | 1.1% | 96.6% | 79.8% |
| Organization:Other | 98 | 89.8% | 9.2% | 1.0% | 94.9% | 86.7% |
| ID:Patient | 921 | 97.5% | 1.5% | 1.0% | 88.7% | 87.1% |
| ID:Caregiver | 167 | 66.5% | 0.0% | 33.5% | 64.7% | 64.7% |
| Date | 523 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 470 | 53.4% | 46.4% | 0.2% | 73.8% | 4.0% |
| Contactdetails | 317 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Profession | 123 | 3.3% | 0.0% | 96.7% | 0.0% | 0.0% |
| **all** | 5750 | 82.5% | | 6.5% | 87.3% | 74.4% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 3325 | 99.9% | 96.2% | 81.4% | 2 |
| model | 1820 | 96.2% | 76.9% | 65.1% | 69 |
| rules | 700 | 75.6% | 62.1% | 54.9% | 171 |
| Address_Location | 517 | 99.8% | 90.9% | 87.2% | 1 |
| Age_Birthdate | 357 | 97.2% | 97.2% | 5.3% | 10 |
| Contactdetails | 415 | 100.0% | 76.4% | 76.4% | 0 |
| Date | 664 | 97.1% | 78.8% | 78.8% | 19 |
| ID | 929 | 100.0% | 100.0% | 98.0% | 0 |
| Name | 1970 | 98.7% | 97.9% | 82.4% | 25 |
| Organization | 698 | 75.2% | 74.2% | 61.9% | 173 |
| Other | 295 | 95.3% | 0.0% | 0.0% | 14 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 500 | 91.3% | 0.24% |
| en-US | 500 | 91.5% | 0.38% |
| clinic_note | 168 | 86.3% | 0.43% |
| discharge_summary | 168 | 93.5% | 0.14% |
| emergency_note | 166 | 93.3% | 0.11% |
| laboratory_report | 166 | 93.9% | 1.03% |
| nursing_note | 166 | 93.0% | 0.10% |
| referral_letter | 166 | 89.0% | 0.14% |

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
| caregiver_role | 47 | 0 | 0.0% |  |
| gestational_age | 36 | 7 | 19.4% | Age_Birthdate:7 |
| gene_variant | 25 | 1 | 4.0% | Other:1 |
| clinical_scale | 22 | 0 | 0.0% |  |
| terminology_code | 22 | 6 | 27.3% | Other:6 |
| impossible_date | 18 | 17 | 94.4% | Date:17 |
| ambiguous_month_word | 16 | 0 | 0.0% |  |
| laboratory_code | 16 | 0 | 0.0% |  |
| device_model | 5 | 0 | 0.0% |  |
| **all** | 1000 | 31 | 3.1% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
