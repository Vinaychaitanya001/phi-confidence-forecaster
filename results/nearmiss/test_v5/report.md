# Missed-PHI candidates and note-level risk: `test_v5`

877 candidates (tau=0.02) in 1008 notes; 99 contain missed PHI. Gold spans with uncovered characters: 114; 98 of them have a candidate (86% candidate coverage).

| Forecaster | AUROC | AUPRC | missed found @5% | @10% | @20% of candidates | add p≥0.5: added / true / precision |
|---|---|---|---|---|---|---|
| raw_mass | 0.858 | 0.375 | 22% | 40% | 71% | 129 / 53 / 41% |
| all | 0.990 | 0.945 | 44% | 83% | 99% | 80 / 76 / 95% |

## Note-level leak risk  P(≥1 miss) = 1 − Π(1 − p_i)

- notes with at least one missed gold span: 98 of 1008
- AUROC of P(≥1 miss): **0.964** (baseline: number of candidates 0.770)
- ECE of P(≥1 miss): 0.0258
- reviewing the riskiest 5 / 10 / 20 % of notes finds 53% / 84% / 93% of all missed PHI spans

## Missed gold spans WITHOUT any candidate (the coverage gap)

### Age_Birthdate: 5 (max PHI mass: median 0.953, ≥0.005 in 100%)

- ziz46@btinternet.com⏎Clinical age: ⟦51 y/o⟧⏎⏎History:⏎Brief spinning episodes   (max PHI mass 0.998)
- R. Documented at 27 March 2026 for ⟦47 y/o⟧.  (max PHI mass 0.097)
- ⏎Patient: A. Lazette⏎Clinical age: ⟦2 wk old⟧⏎Report/accession ID: 03723254⏎Coll  (max PHI mass 0.953)
- atient: Raima Russin⏎Clinical age: ⟦7 wk old⟧⏎Admission date: Jan 12, 2023⏎Servi  (max PHI mass 0.991)
- 00 30 5901⏎⏎Patient: Madden Y.  |  ⟦10 m/o⟧⏎Mother at bedside: J. Jamele⏎Home   (max PHI mass 0.006)

### Organization:Healthcare: 5 (max PHI mass: median 0.992, ≥0.005 in 100%)

-  December 1937, assessed in A&E at ⟦University Hospital Bristol and Weston Virtual Site⟧ on 2026-10-26. Partner reports sud  (max PHI mass 0.992)
- r completed 08:15 by NORRIE SCOTT, ⟦University Hospital Bristol and Weston Virtual Site⟧.  (max PHI mass 0.978)
- s or respiratory effort increases. ⟦Southwell Medical, a Campus of Trmc⟧ is the treating healthcare organiz  (max PHI mass 0.997)
- tics area after urgent transfer to ⟦Westfields Hospital and Clinic⟧ ED; no genetic emergency identifie  (max PHI mass 0.617)
- T follow-up. Care coordinated with ⟦Avera Heart Hospital of South Dakota⟧. Return for persistent symptoms, s  (max PHI mass 0.999)

### Profession: 3 (max PHI mass: median 0.003, ≥0.005 in 0%)

- k Housing Association and works as ⟦bus driver⟧. There is no reported history of n  (max PHI mass 0.003)
-  diagnosis. The patient works as a ⟦Care worker⟧ at Os Community Centre and is conc  (max PHI mass 0.002)
- inconsistent. The patient works as ⟦bus driver⟧ at Graniteville Senior Center. A s  (max PHI mass 0.003)

### Name:Caregiver: 1 (max PHI mass: median 0.745, ≥0.005 in 100%)

- scalation: findings discussed with ⟦FENRIS SENIOR⟧. Continue current wound-care plan   (max PHI mass 0.745)

### Name:Other: 1 (max PHI mass: median 0.003, ≥0.005 in 0%)

- d for 15 Nov 2012. Relative/spouse ⟦claudine berry⟧ updated with patient consent.⏎⏎Pla  (max PHI mass 0.003)

### Name:Patient: 1 (max PHI mass: median 0.003, ≥0.005 in 0%)

- : Cardiology step-down handoff for ⟦fred scasny⟧. Admitted with acute kidney injury  (max PHI mass 0.003)

