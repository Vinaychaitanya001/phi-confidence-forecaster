# Missed-PHI candidates and note-level risk: `cal_v5`

838 candidates (tau=0.02) in 1000 notes; 94 contain missed PHI. Gold spans with uncovered characters: 110; 93 of them have a candidate (85% candidate coverage).

| Forecaster | AUROC | AUPRC | missed found @5% | @10% | @20% of candidates | add p≥0.5: added / true / precision |
|---|---|---|---|---|---|---|
| raw_mass | 0.889 | 0.464 | 27% | 53% | 73% | 131 / 63 / 48% |
| p1 | 0.915 | 0.735 | 43% | 62% | 80% | 69 / 54 / 78% |
| p1+p2 | 0.939 | 0.835 | 43% | 71% | 89% | 76 / 62 / 82% |
| all | 0.977 | 0.912 | 44% | 79% | 97% | 86 / 75 / 87% |

## Note-level leak risk  P(≥1 miss) = 1 − Π(1 − p_i)

- notes with at least one missed gold span: 98 of 1000
- AUROC of P(≥1 miss): **0.947** (baseline: number of candidates 0.771)
- ECE of P(≥1 miss): 0.0252
- reviewing the riskiest 5 / 10 / 20 % of notes finds 52% / 81% / 89% of all missed PHI spans

## Missed gold spans WITHOUT any candidate (the coverage gap)

### Organization:Healthcare: 7 (max PHI mass: median 0.890, ≥0.005 in 100%)

- ogy⏎⏎Patient: Scarlett H.⏎Seen at: ⟦NMP - CARE OF THE ELDERLY ROYAL SHREWSBURY HOSPITAL⟧⏎Reviewing clinician: C. Newton⏎Pre  (max PHI mass 0.900)
- ate medication. Review arranged at ⟦NMP - CARE OF THE ELDERLY ROYAL SHREWSBURY HOSPITAL⟧ on 5th January 2027; swab results   (max PHI mass 0.890)
-  and hematology evaluation through ⟦Memorial Hospital, the⟧.⏎2. Genetic risk assessment. Curre  (max PHI mass 0.820)
-  optimization. Transfer of care to ⟦PIONEER MEMORIAL HOSPITAL - CAH⟧. Escalate immediately for hypotens  (max PHI mass 0.961)
- EMI changes reported.⏎⏎Background: ⟦SAINT THOMAS HOSPITAL FOR SPINAL SURGERY⟧ involved in current evaluation. As  (max PHI mass 0.053)
- trexate, folic acid, and naproxen. ⟦UPMC COLE⟧ rheumatology records requested for  (max PHI mass 0.006)
- n.⏎⏎Follow-up with primary care at ⟦University of Illinois Hospital and Clinics⟧ on 02/10/2025.⏎⏎Disposition: Disch  (max PHI mass 0.922)

### Name:Other: 3 (max PHI mass: median 0.011, ≥0.005 in 67%)

- act, no visible discharge. Partner ⟦farina maguire⟧ present.⏎⏎Obs: T 37.8°C, HR 96, BP  (max PHI mass 0.011)
- ion. History obtained from mother, ⟦eyobel mcleod⟧. Ongoing loose stools; two vomits   (max PHI mass 0.011)
- d mild suprapubic discomfort. Aunt ⟦symphony prevallet⟧ at bedside; patient interviewed br  (max PHI mass 0.001)

### Name:Patient: 3 (max PHI mass: median 0.942, ≥0.005 in 100%)

- SITUATION: ED handoff—⟦celes nikolenko⟧, 74 y/o, evaluated for transient l  (max PHI mass 0.998)
- TUATION: Internal medicine handoff—⟦Aracelli B.⟧, DOB December 18th, 2005, MRN 0049  (max PHI mass 0.839)
- ardiology observation unit handoff—⟦Raghad B.⟧ with rheumatoid arthritis flare. R  (max PHI mass 0.942)

### Age_Birthdate: 2 (max PHI mass: median 0.790, ≥0.005 in 100%)

- aundice review⏎⏎Patient: Amaria P.⏎⟦2 wk old⟧; born at 39+2 weeks' gestation⏎⏎Hi  (max PHI mass 0.601)
- ral⏎⏎Patient: Vaylen⏎Clinical age: ⟦7 wk old⟧⏎Legal guardian: Priscella Vanhuss⏎  (max PHI mass 0.978)

### Profession: 2 (max PHI mass: median 0.002, ≥0.005 in 0%)

- tely.⏎⏎Zaiyaan Bainbridge works as ⟦Police officer⟧ for Blairdrummond Further Educatio  (max PHI mass 0.002)
- ontrolled.⏎⏎The patient works as a ⟦Hairdresser⟧ for Parkgate Housing Association.   (max PHI mass 0.002)

