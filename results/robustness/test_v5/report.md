# Robustness: `test_v5`

## Hard negatives (text that looks like PHI but is not) after the confidence layer

Review threshold: confidence < 0.9 is flagged.

| Type | n | redacted by detector | mean confidence of those | flagged for review |
|---|---|---|---|---|
| relative_time | 184 | 0 | – | 0 |
| duration | 176 | 0 | – | 0 |
| medication | 117 | 0 | – | 0 |
| time | 86 | 0 | – | 0 |
| vital_sign | 75 | 0 | – | 0 |
| measurement | 69 | 0 | – | 0 |
| pain_score | 56 | 0 | – | 0 |
| caregiver_role | 47 | 0 | – | 0 |
| eponym | 41 | 0 | – | 0 |
| clinical_scale | 26 | 0 | – | 0 |
| gestational_age | 26 | 0 | – | 0 |
| terminology_code | 25 | 6 | 0.144 | 6 |
| gene_variant | 24 | 5 | 0.444 | 3 |
| impossible_date | 22 | 0 | – | 0 |
| ambiguous_month_word | 17 | 0 | – | 0 |
| laboratory_code | 11 | 0 | – | 0 |
| device_model | 6 | 0 | – | 0 |
| **all** | 1008 | 11 | | 9 |

## Cost per note (CPU, 8 threads)

- regex rules: 17 ms
- model, single pass: 0.35 s
- MC dropout, 10 passes: 4.32 s (12.5x)
