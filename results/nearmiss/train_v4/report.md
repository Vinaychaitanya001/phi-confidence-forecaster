# Missed-PHI candidates and note-level risk: `train_v4`

3932 candidates (tau=0.02) in 4692 notes; 460 contain missed PHI. Gold spans with uncovered characters: 525; 455 of them have a candidate (87% candidate coverage).

| Forecaster | AUROC | AUPRC | missed found @5% | @10% | @20% of candidates | add p≥0.5: added / true / precision |
|---|---|---|---|---|---|---|
| raw_mass | 0.890 | 0.529 | 32% | 53% | 75% | 607 / 310 / 51% |
| p1 | 0.913 | 0.772 | 43% | 64% | 81% | 297 / 259 / 87% |
| p1+p2 | 0.968 | 0.889 | 43% | 74% | 91% | 368 / 329 / 89% |
| all | 0.993 | 0.967 | 43% | 82% | 98% | 431 / 404 / 94% |

## Note-level leak risk  P(≥1 miss) = 1 − Π(1 − p_i)

- notes with at least one missed gold span: 479 of 4692
- AUROC of P(≥1 miss): **0.936** (baseline: number of candidates 0.766)
- ECE of P(≥1 miss): 0.0203
- reviewing the riskiest 5 / 10 / 20 % of notes finds 51% / 84% / 90% of all missed PHI spans

## Missed gold spans WITHOUT any candidate (the coverage gap)

### Organization:Healthcare: 22 (max PHI mass: median 0.992, ≥0.005 in 100%)

- ER⏎Reporting laboratory clinician, ⟦William Harvey Hospital - Occupational Health⟧⏎Report date: 27/06/2018  (max PHI mass 0.948)
- d. Discussed with surgical team at ⟦Royal Victoria Hospital - Diabetes & Endocrinology⟧; no indication for immediate opera  (max PHI mass 0.995)
-  by JOOLS DEAN, Clinical Genetics, ⟦Haslemere Hospital Minor Injuries Unit⟧.  (max PHI mass 0.992)
- t fever or reduced oral intake. GP/⟦Royal Papworth Hospital - Off Site⟧ review booked for 2026-03-06.⏎⏎Sig  (max PHI mass 0.765)
- lood sample to be arranged through ⟦WEAVER LODGE INDEPENDENT HOSPITAL - EPACT⟧ once familial result confirmed.⏎-   (max PHI mass 0.992)
-  borbala nash⏎Laboratory clinician⏎⟦Llandudno General Hospital Site⟧  (max PHI mass 0.993)
- A&E assessment – ⟦Sexual Health Services - Royal Preston Hospital⟧⏎⏎Date: 31 December 2026⏎Patient: E  (max PHI mass 0.972)
- nical genetics referral noted from ⟦Royal Victoria Hospital - Health Care of the Elderly⟧; no acute genetics issue identifie  (max PHI mass 0.950)
- Referring healthcare organisation: ⟦North Manchester General Hospital - Urgent Treatment Centre⟧⏎⏎Presenting problem:⏎Two-day histo  (max PHI mass 0.978)
-  Case discussed with cardiology at ⟦MAYO CLINIC HEALTH SYSTEM-NORTHLAND⟧; no indication for emergent STEMI   (max PHI mass 0.988)
- Up and Instructions⏎Follow up with ⟦NORTHWEST MEDICAL CENTER-SPRINGDALE⟧ hematology/primary care team for o  (max PHI mass 0.928)
- che Service⏎From: MAHDI KULCZYCKI, ⟦P H S INDIAN HOSPITAL AT BROWNING - BLACKFEET⟧⏎Patient: Declan S.⏎Report/accessio  (max PHI mass 0.963)

### Age_Birthdate: 18 (max PHI mass: median 0.913, ≥0.005 in 100%)

- Patient: Aviva Byrne⏎Clinical age: ⟦7 wk old⟧⏎Parent present: A. COLLIER⏎⏎Reason  (max PHI mass 0.987)
- ing management.⏎⏎K-Ci is currently ⟦7 wk old⟧, brought by legal guardian A. Hutc  (max PHI mass 0.940)
- ent: DEACON-JAMES DAVISON⏎Current: ⟦day 3 of life⟧⏎MRN: MRN-04391902⏎Father: MAYARA K  (max PHI mass 0.005)
- ⏎⏎Patient: Rumaithah⏎Clinical age: ⟦2 wk old⟧⏎Parent present: Iori⏎Referred from  (max PHI mass 0.952)
- 16⏎⏎Patient: N. Howe⏎Clinical age: ⟦7 wk old⟧ infant⏎Legal guardian: menisha mun  (max PHI mass 0.979)
- comfort. Patient: Kishaan P., aged ⟦27 years⟧. Home address: 9 Afon Llwyd Terrac  (max PHI mass 0.999)
- al Unit⏎⏎Patient: raysha blackburn⏎⟦day 3 of life⟧; mother Daniele WEBBER present and  (max PHI mass 0.009)
-  number: KN605915D⏎⏎Re: Dustin P., ⟦day 3 of life⟧⏎⏎I would be grateful for your urge  (max PHI mass 0.010)
- than-jay tomlinson⏎Clinical stage: ⟦4 m/o⟧⏎Specimen: capillary blood, bilirub  (max PHI mass 0.015)
- ort⏎⏎Patient: Cyriah⏎Clinical age: ⟦2 wk old⟧⏎Legal guardian: Deshae⏎Contact: (2  (max PHI mass 0.954)
-  Cropp⏎MRN: 09984136⏎Clinical age: ⟦7 wk old⟧⏎History: Jaundice first noted duri  (max PHI mass 0.963)
-  666 84 3532⏎⏎Patient: M. Billiard⏎⟦2 wk old⟧⏎Home address: 76 Co Rd 4 Kh, Willa  (max PHI mass 0.886)

### Name:Other: 10 (max PHI mass: median 0.007, ≥0.005 in 60%)

- isposition⏎Safe for discharge with ⟦A. Said⟧ aware of the plan. Advised to avoi  (max PHI mass 0.854)
- tion status on ward round. Partner ⟦ecaterina wells⟧ updated with patient’s consent.⏎⏎F  (max PHI mass 0.001)
- : patient; collateral from sibling ⟦lyes carey⟧⏎⏎Presenting complaint:⏎Two-day his  (max PHI mass 0.006)
- ds77@outlook.com⏎Relative/contact: ⟦IVA HEATH⟧ (adult child)⏎Service: ROYAL VICTO  (max PHI mass 0.004)
- noted on dressing removal. Partner ⟦ettore fellows⟧ present and updated.⏎⏎Observations  (max PHI mass 0.007)
- ry effort and oral intake. Sibling ⟦cybil gale⟧ updated by patient’s permission.⏎⏎  (max PHI mass 0.002)
- trointestinal illness. Her sister, ⟦bowman schwagerl⟧, has noticed that hand swelling is  (max PHI mass 0.020)
-  and reported weight loss. Friend, ⟦noriah delamerced⟧, at bedside; history corroborated.  (max PHI mass 0.995)
- ⏎MRN: 042116/91⏎Historian: Mother, ⟦orren barbot⟧⏎⏎CC: Eczema flare with nighttime i  (max PHI mass 0.009)
- atoid arthritis flare. Adult child ⟦nayelis dibley⟧ at bedside; history confirmed.⏎⏎As  (max PHI mass 0.002)

### Profession: 9 (max PHI mass: median 0.002, ≥0.005 in 11%)

- cated asthma.⏎⏎Cora-Leigh works as ⟦Chef⟧ at Sheddocksley Secondary School.   (max PHI mass 0.002)
- ctivities and is able to work as a ⟦Pharmacist⟧ at Aird-dhubh Secondary School, al  (max PHI mass 0.002)
- atient’s occupation is recorded as ⟦Postal worker⟧. There has also been increased rea  (max PHI mass 0.002)
- ems.⏎⏎The patient is employed as a ⟦Librarian⟧ by Cornaigbeg Community Centre. Th  (max PHI mass 0.002)
- t yet available.⏎⏎The patient is a ⟦Builder⟧ and lives at 142 Greenwood Avenue,  (max PHI mass 0.015)
- cancer.⏎⏎The patient occupation is ⟦Pharmacist⟧, employed by Heathfield Further Ed  (max PHI mass 0.002)
-  emergency. The patient works as a ⟦Plumber⟧ at Skinnet Town Council.⏎⏎Current   (max PHI mass 0.003)
-  suspension.⏎⏎The patient works as ⟦Front Desk Receptionist⟧ for Altmar Community College. Thei  (max PHI mass 0.002)
- y activities. The patient works as ⟦Plumber⟧ at Nashville Community College.⏎⏎L  (max PHI mass 0.002)

### Name:Patient: 8 (max PHI mass: median 0.999, ≥0.005 in 88%)

- note – Clinical Genetics⏎⏎Patient: ⟦Re⟧; 72 y/o⏎Reason for review: Episode  (max PHI mass 0.009)
- UATION: Pulmonary medicine handoff—⟦Raychel⟧ with diabetic plantar foot ulcer a  (max PHI mass 0.001)
- SITUATION: ED handoff—⟦Stiles Homier⟧, MRN MRN-02875882, with right lowe  (max PHI mass 0.999)
- ON: Clinical Genetics unit handoff—⟦devlyn meteer⟧, the patient, age 74 years, review  (max PHI mass 0.999)
- UATION: Pulmonary medicine handoff—⟦H. Briddle⟧ admitted with non-ST-elevation myo  (max PHI mass 0.999)
- S: Cardiology floor handoff—⟦Tao Fabry⟧, DOB 03/01/1972, home address 84 N  (max PHI mass 1.000)
- SITUATION: Cardiology unit handoff—⟦Elizah S.⟧ admitted with acute pyelonephritis  (max PHI mass 0.970)
- SITUATION⏎ED handover—⟦H. Gilbride⟧, DOB July 9th, 1972, from home at   (max PHI mass 1.000)

### Name:Caregiver: 2 (max PHI mass: median 0.003, ≥0.005 in 0%)

- ory failure.⏎⏎Plan: Discussed with ⟦miceal dyson⟧ at University Hospital Bristol and  (max PHI mass 0.005)
- . Case discussed with ED attending ⟦zumra seiuli⟧ at Hamilton Memorial Hospital. Giv  (max PHI mass 0.001)

### Organization:Other: 1 (max PHI mass: median 0.991, ≥0.005 in 100%)

- nder some work-related pressure at ⟦South Knighton Voluntary Service⟧, with reduced sleep on several nig  (max PHI mass 0.991)

