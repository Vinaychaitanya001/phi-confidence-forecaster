# Existing detector on MedDeID `train_rules_v4` split

Detector: repo regex rules + OpenMed FastClinical-82M as published (no training). Settings adapted to the MedDeID guideline (all ages, no clock times, titles kept, states kept). Fusion/post-processing applied offline.

## 1. Headline (character level, MedDeID's own metrics)

| System | PHI recall [95% CI] | Non-PII redaction [95% CI] | Strict cat. P / R / F1 | Pred spans | False alarms | s/note |
|---|---|---|---|---|---|---|
| rules-only | **93.9%** [93.5%–94.2%] | 0.05% [0.04%–0.06%] | 97.1% / 91.3% / 94.1% | 25418 | 77 | 0.03 |

## 2. Gold spans per MedDeID label (system: rules+model)

| Label | n | Fully covered | Partly | Missed | Category correct | Exact |
|---|---|---|---|---|---|---|
| Name:Patient | 5251 | 95.5% | 0.1% | 4.4% | 95.6% | 95.5% |
| Name:Caregiver | 3031 | 87.7% | 0.0% | 12.2% | 87.0% | 83.3% |
| Name:Other | 2041 | 72.6% | 0.1% | 27.2% | 72.7% | 72.4% |
| Address_Location:Patient | 1694 | 97.4% | 1.8% | 0.8% | 99.2% | 93.0% |
| Address_Location:Caregiver | 231 | 80.1% | 0.4% | 19.5% | 71.4% | 71.0% |
| Address_Location:Other | 311 | 58.8% | 0.3% | 40.8% | 58.2% | 52.4% |
| Organization:Healthcare | 2065 | 89.3% | 7.1% | 3.6% | 96.0% | 84.8% |
| Organization:Other | 512 | 87.1% | 0.0% | 12.9% | 86.5% | 84.6% |
| ID:Patient | 4401 | 97.9% | 1.8% | 0.3% | 99.4% | 97.5% |
| ID:Caregiver | 944 | 85.6% | 0.0% | 14.4% | 84.0% | 83.9% |
| Date | 2400 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% |
| Age_Birthdate | 2015 | 98.6% | 0.6% | 0.8% | 99.1% | 98.4% |
| Contactdetails | 1478 | 99.5% | 0.5% | 0.0% | 99.2% | 98.6% |
| Profession | 667 | 98.5% | 0.0% | 1.5% | 98.5% | 98.5% |
| **all** | 27041 | 92.8% | | 6.1% | 93.5% | 91.3% |

## 3. Predicted spans (system: rules+model)

| Group | n | Overlaps PHI | Right category | Exact | False alarms |
|---|---|---|---|---|---|
| model | 543 | 99.8% | 99.8% | 99.8% | 1 |
| rules | 24875 | 99.7% | 99.5% | 97.1% | 76 |
| Address_Location | 2041 | 100.0% | 99.6% | 93.2% | 1 |
| Age_Birthdate | 2000 | 99.8% | 99.8% | 99.2% | 4 |
| Contactdetails | 1490 | 100.0% | 98.4% | 97.9% | 0 |
| Date | 2403 | 100.0% | 99.9% | 99.9% | 1 |
| ID | 5167 | 100.0% | 100.0% | 98.4% | 0 |
| Name | 9196 | 99.5% | 99.4% | 98.1% | 47 |
| Organization | 2457 | 99.3% | 98.7% | 88.9% | 18 |
| Profession | 664 | 99.1% | 98.9% | 98.9% | 6 |

## 4. By locale and document type (rules+model, character level)

| Group | Notes | PHI recall | Non-PII redaction |
|---|---|---|---|
| en-GB | 2346 | 95.0% | 0.05% |
| en-US | 2346 | 92.7% | 0.05% |
| clinic_note | 782 | 96.6% | 0.03% |
| discharge_summary | 782 | 94.1% | 0.07% |
| emergency_note | 782 | 92.1% | 0.06% |
| laboratory_report | 782 | 98.0% | 0.05% |
| nursing_note | 782 | 92.7% | 0.05% |
| referral_letter | 782 | 90.2% | 0.05% |

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
