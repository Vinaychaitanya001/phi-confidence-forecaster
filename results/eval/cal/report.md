# Existing detector on MedDeID `cal` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules+model | **91.4%** [90.8%–92.0%] | 0.31% [0.27%–0.36%] | 73.0% / 74.3% / 73.7% | 5853 | 251 | 0.41 |
| rules+model(all) | **94.1%** [93.6%–94.6%] | 0.33% [0.29%–0.37%] | 72.8% / 77.8% / 75.2% | 6143 | 279 | 0.41 |
| rules-only | **68.8%** [67.7%–70.1%] | 0.25% [0.21%–0.29%] | 76.0% / 53.5% / 62.8% | 4051 | 199 | 0.41 |
| model-only | **83.3%** [82.3%–84.3%] | 0.07% [0.06%–0.09%] | 70.5% / 66.8% / 68.6% | 5444 | 71 | 0.41 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 1110 | 87.9% | 7.7% | 4.3% | 93.5% | 85.9% |
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
| **all** | 5750 | 82.5% | | 6.5% | 87.3% | 74.3% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| both | 3340 | 99.4% | 95.7% | 81.0% | 19 |
| model | 1802 | 97.1% | 77.6% | 65.6% | 52 |
| rules | 711 | 74.7% | 61.5% | 54.1% | 180 |
| Address_Location | 517 | 99.8% | 90.9% | 87.2% | 1 |
| Age_Birthdate | 357 | 97.2% | 97.2% | 5.3% | 10 |
| Contactdetails | 418 | 99.3% | 75.8% | 75.8% | 3 |
| Date | 670 | 96.3% | 78.1% | 78.1% | 25 |
| ID | 929 | 100.0% | 100.0% | 98.0% | 0 |
| Name | 1969 | 98.7% | 97.9% | 82.4% | 25 |
| Organization | 698 | 75.2% | 74.2% | 61.9% | 173 |
| Other | 295 | 95.3% | 0.0% | 0.0% | 14 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 500 | 91.2% | 0.24% |
| en-US | 500 | 91.5% | 0.38% |
| clinic_note | 168 | 86.3% | 0.43% |
| discharge_summary | 168 | 93.5% | 0.14% |
| emergency_note | 166 | 93.2% | 0.12% |
| laboratory_report | 166 | 93.9% | 1.05% |
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
| pain_score | 70 | 1 | 1.4% | Date:1 |
| time | 53 | 0 | 0.0% |  |
| eponym | 50 | 0 | 0.0% |  |
| caregiver_role | 47 | 0 | 0.0% |  |
| gestational_age | 36 | 7 | 19.4% | Age_Birthdate:7 |
| gene_variant | 25 | 1 | 4.0% | Other:1 |
| clinical_scale | 22 | 0 | 0.0% |  |
| terminology_code | 22 | 6 | 27.3% | Other:6 |
| impossible_date | 18 | 18 | 100.0% | Date:18 |
| ambiguous_month_word | 16 | 0 | 0.0% |  |
| laboratory_code | 16 | 0 | 0.0% |  |
| device_model | 5 | 0 | 0.0% |  |
| **all** | 1000 | 33 | 3.3% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
