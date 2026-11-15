# Missed-PHI candidates and note-level risk: `cal_v4`

855 candidates (tau=0.02) in 1000 notes; 111 contain missed PHI. Gold spans with uncovered characters: 194; 110 of them have a candidate (57% candidate coverage).

| Forecaster | AUROC | AUPRC | missed found @5% | @10% | @20% of candidates | add p≥0.5: added / true / precision |
|---|---|---|---|---|---|---|
| raw_mass | 0.882 | 0.491 | 23% | 50% | 70% | 140 / 72 / 51% |
| p1 | 0.900 | 0.730 | 38% | 55% | 75% | 70 / 58 / 83% |
| p1+p2 | 0.956 | 0.864 | 38% | 67% | 90% | 87 / 75 / 86% |
| all | 0.981 | 0.943 | 39% | 74% | 95% | 99 / 94 / 95% |

## Note-level leak risk  P(≥1 miss) = 1 − Π(1 − p_i)

- notes with at least one missed gold span: 166 of 1000
- AUROC of P(≥1 miss): **0.835** (baseline: number of candidates 0.705)
- ECE of P(≥1 miss): 0.0768
- reviewing the riskiest 5 / 10 / 20 % of notes finds 33% / 58% / 69% of all missed PHI spans
