# Existing detector on MedDeID `train_rules_v1` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules-only | **86.9%** [86.5%–87.3%] | 0.46% [0.44%–0.49%] | 89.0% / 81.1% / 84.9% | 24647 | 1831 | 0.01 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 5251 | 86.4% | 0.1% | 13.5% | 86.5% | 85.6% |
| Name:Caregiver | 3031 | 63.9% | 0.0% | 36.1% | 63.1% | 59.2% |
| Name:Other | 2041 | 20.4% | 0.1% | 79.4% | 20.5% | 18.7% |
| Address_Location:Patient | 1694 | 97.4% | 1.8% | 0.8% | 99.2% | 93.0% |
| Address_Location:Caregiver | 231 | 63.6% | 0.0% | 36.4% | 54.5% | 10.0% |
| Address_Location:Other | 311 | 8.4% | 0.0% | 91.6% | 8.0% | 0.0% |
| Organization:Healthcare | 2065 | 88.1% | 8.8% | 3.1% | 96.4% | 84.0% |
| Organization:Other | 512 | 90.8% | 0.0% | 9.2% | 90.6% | 88.7% |
| ID:Patient | 4401 | 97.7% | 1.8% | 0.5% | 99.0% | 97.2% |
| ID:Caregiver | 944 | 77.2% | 0.0% | 22.8% | 75.5% | 75.0% |
| Date | 2400 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 2015 | 98.6% | 0.6% | 0.8% | 99.1% | 98.5% |
| Contactdetails | 1478 | 99.5% | 0.5% | 0.0% | 99.2% | 98.6% |
| Profession | 667 | 98.5% | 0.0% | 1.5% | 98.5% | 98.5% |
| **all** | 27041 | 83.4% | | 15.5% | 84.1% | 81.1% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| rules | 24647 | 92.6% | 92.3% | 89.0% | 1831 |
| Address_Location | 1839 | 100.0% | 99.9% | 86.9% | 0 |
| Age_Birthdate | 2073 | 96.3% | 96.3% | 95.7% | 77 |
| Contactdetails | 1506 | 99.3% | 97.3% | 96.8% | 11 |
| Date | 2437 | 98.6% | 98.5% | 98.5% | 35 |
| ID | 5129 | 98.9% | 98.9% | 97.2% | 56 |
| Name | 7656 | 89.9% | 89.7% | 87.1% | 776 |
| Organization | 3331 | 74.2% | 73.8% | 65.7% | 858 |
| Profession | 676 | 97.3% | 97.2% | 97.2% | 18 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 2346 | 87.0% | 0.40% |
| en-US | 2346 | 86.9% | 0.52% |
| clinic_note | 782 | 93.8% | 0.46% |
| discharge_summary | 782 | 85.6% | 0.35% |
| emergency_note | 782 | 86.1% | 0.21% |
| laboratory_report | 782 | 94.7% | 1.30% |
| nursing_note | 782 | 87.3% | 0.26% |
| referral_letter | 782 | 75.2% | 0.29% |

## 5. Hard negatives wrongly redacted (rules+model)

| Hard-negative type | n | Redacted | Rate | Redacted as |
|---|---|---|---|---|
| duration | 888 | 0 | 0.0% |  |
| relative_time | 819 | 0 | 0.0% |  |
| medication | 586 | 0 | 0.0% |  |
| measurement | 343 | 0 | 0.0% |  |
| vital_sign | 332 | 0 | 0.0% |  |
| time | 327 | 0 | 0.0% |  |
| pain_score | 275 | 3 | 1.1% | Date:3 |
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
| **all** | 4692 | 8 | 0.2% | |

Notes: the model has no Profession label and one PERSON label, so Profession is only reachable by chance and Name:Patient / Caregiver / Other are scored at the Name category. Precision and recall here are the error material the confidence layer (steps 4–6) learns from.
