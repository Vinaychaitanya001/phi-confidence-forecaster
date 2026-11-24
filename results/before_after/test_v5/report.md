# Before and after the forecasters: `test_v5`

1008 notes, 5838 predicted spans (62 not PHI). Same rules and model in both columns; nothing is refitted.

| Group | Measure | Before (detector alone) | After (with the forecasters) |
|---|---|---|---|
| Confidence | ECE: is PHI / category / exact | 0.203 / 0.183 / 0.160 | 0.0028 / 0.0045 / 0.0053 |
| | AUROC for ranking wrong spans (is PHI) | 0.752 | 0.998 |
| | Not-PHI spans among the 10 % least confident | 19 % | 100 % |
| Drop | Precision (spans that are PHI) | 98.94 % | 99.72 % (51 least-confident spans dropped, 5 true spans lost) |
| | False alarms (spans touching no PHI) | 60 | 14 |
| Add (p ≥ 0.5) | PHI recall (characters) | 98.55 % | 99.49 % |
| | Gold spans with uncovered letters or digits | 114 | 40 |
| | Non-PII redaction | 0.071 % | 0.073 % |
| | Additions that are real missed PHI | – | 76 of 80 |
| Note risk | Missed spans in the riskiest 10 % of notes | – | 84 % |

Drop and add together: PHI recall 99.42 %, 45 gold spans with uncovered letters or digits, 14 false alarms.

The drop count is the largest that loses at most 0.1 % of the true spans, chosen with the answer key: it shows what the score makes possible, not a fixed threshold. The deliverable pipeline sends spans below 0.9 to review instead of dropping them. The add threshold (0.5) was fixed on `cal`.
