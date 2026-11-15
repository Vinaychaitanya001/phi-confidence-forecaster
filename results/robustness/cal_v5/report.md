# Robustness: `cal_v5`

## Hard negatives (text that looks like PHI but is not) after the confidence layer

Review threshold: confidence < 0.9 is flagged.

| Type | n | redacted by detector | mean confidence of those | flagged for review |
|---|---|---|---|---|
| duration | 177 | 0 | – | 0 |
| relative_time | 164 | 0 | – | 0 |
| medication | 129 | 0 | – | 0 |
| vital_sign | 77 | 0 | – | 0 |
| measurement | 73 | 0 | – | 0 |
| pain_score | 70 | 0 | – | 0 |
| time | 53 | 0 | – | 0 |
| eponym | 50 | 0 | – | 0 |
| caregiver_role | 47 | 1 | 0.737 | 1 |
| gestational_age | 36 | 7 | 0.195 | 6 |
| gene_variant | 25 | 1 | 0.912 | 0 |
| clinical_scale | 22 | 0 | – | 0 |
| terminology_code | 22 | 6 | 0.166 | 6 |
| impossible_date | 18 | 0 | – | 0 |
| ambiguous_month_word | 16 | 0 | – | 0 |
| laboratory_code | 16 | 0 | – | 0 |
| device_model | 5 | 0 | – | 0 |
| **all** | 1000 | 15 | | 13 |

## Cost per note (CPU, 8 threads)

- regex rules: 9 ms
- model, single pass: 0.40 s
- MC dropout, 10 passes: 4.55 s (11.3x)

## Shift experiments (forecaster trained on one group, scored on another)

### cal_v5.rules+model.y_cat_ok: train lang=en-GB (2889 spans) → test lang=en-US (2911 spans)

| Model | ECE | AUROC(error) | errors caught @10% |
|---|---|---|---|
| gbdt:p1 | 0.0117 | 0.918 | 74% |
| gbdt:all | 0.0109 | 0.984 | 92% |
| raw_softmax | 0.1778 | 0.673 | 14% |
### cal_v5.rules+model.y_exact: train lang=en-GB (2889 spans) → test lang=en-US (2911 spans)

| Model | ECE | AUROC(error) | errors caught @10% |
|---|---|---|---|
| gbdt:p1 | 0.0154 | 0.927 | 73% |
| gbdt:all | 0.0137 | 0.990 | 96% |
| raw_softmax | 0.1541 | 0.719 | 19% |
### cal_v5.rules+model.y_is_phi: train lang=en-GB (2889 spans) → test lang=en-US (2911 spans)

| Model | ECE | AUROC(error) | errors caught @10% |
|---|---|---|---|
| gbdt:p1 | 0.0058 | 0.974 | 97% |
| gbdt:all | 0.0047 | 0.987 | 95% |
| raw_softmax | 0.1952 | 0.765 | 29% |
