# Error analysis: `rules-only` on `train_rules_v4`

## Missed gold spans (no overlap with any prediction)

### Name:Patient: 231 missed

shapes: `Aa`×68, `Aa A.`×41, `Aa Aa`×28, `A. Aa`×25, `A A`×24, `a a`×22, `A. A`×7, `Aa-Aa`×5
preceded by: `situation:`×55, `patient:`×44, `patient,`×24, `situation`×14, `—`×9, `handoff—`×7, `<none>`×6, `s:`×5

- A&E assessment⏎⏎Patient: ⟦KASIEMOBI JOHN⟧   MRN: 05555873⏎Adult, brought by 
- symptoms⏎NHS number: 000 649 1434⏎⏎⟦Gena⟧ attended for review of ongoing ref
-  ongoing oliguria and poor intake. ⟦Nergiz⟧ is a 56-year-old Asian male patien
- complaint⏎NHS number: 000 105 1645⏎⟦Zylan⟧ attended A&E with dysuria, urinary
- SITUATION⏎⟦ALIVIAH BACON⟧, a 25-year-old African American ma
- t⏎NHS number: 0002312485⏎⏎Patient: ⟦N. Winter⟧    MRN: 05636466⏎Contact: neevan.w
- l⏎NHS number: 0009069241⏎⏎Patient: ⟦ADALIN PORTER⟧⏎Occupation: Mechanic⏎Employer: Vid
- l Insurance number: NT 83 37 91 C⏎⏎⟦Rhaenyra⟧ was admitted via the emergency dep

### Name:Caregiver: 371 missed

shapes: `a a`×150, `A. Aa`×73, `Aa Aa`×66, `A A`×58, `a-a a`×13, `A. A`×3, `Aa A`×3, `a a'a`×1
preceded by: `sincerely,`×187, `by`×88, `with`×16, `referrer:`×9, `by:`×6, `caregiver:`×6, `to`×4, `attending`×4

- een at Royal Alexandra Hospital by ⟦della-rae ayres⟧⏎⏎The patient attended A&E with low
- e not clearly improving. Signed by ⟦della-rae ayres⟧.
- dated and electronically signed by ⟦deehan tyler⟧, Consultant Chemical Pathologist⏎G
- tion and repeat renal blood tests. ⟦jaspreet o'connor⟧, the treating emergency medicine c
- ate fluids.⏎⏎Handover completed by ⟦laike draper⟧.
- ent: 24 March 2036.⏎⏎Documented by ⟦kiara-leigh slater⟧, emergency clinician.
- omic features.⏎⏎Report prepared by ⟦tasleema reeves⟧, consultant endocrinologist, Cheps
- th October 2021. Note completed by ⟦aife webb⟧.

### Name:Other: 556 missed

shapes: `a a`×271, `Aa`×65, `A. Aa`×61, `Aa Aa`×59, `A A`×55, `a-a a`×15, `A-A A`×6, `A. A`×6
preceded by: `friend`×32, `spouse,`×30, `present:`×26, `bedside:`×25, `and`×18, `sibling`×18, `father,`×16, `partner`×16

- ge or signs of systemic infection. ⟦BOJIDAR PRINCE⟧ updated by telephone regarding the
- l period not documented at triage. ⟦C. Daniel⟧, her relative, is available by tel
- tial relevance to adult relatives. ⟦Jem Aston⟧, the patient’s adult sibling, is a
- ematology team at ULSTER HOSPITAL. ⟦Cora-Mae Calvert⟧, who lives in Clare, has been upda
- inary infection reported. Relative ⟦T. O'LEARY⟧ accompanied the patient and confir
- ot describe excess alcohol intake. ⟦Kady⟧, a close relative, has been helpin
- rs have been assessed and treated. ⟦Sabriin Gordon⟧, from Achfrish, was recorded as he
- s ago; pregnancy is not suspected. ⟦N. Bryant⟧ accompanied her and provided addit

### Address_Location:Patient: 13 missed

shapes: `9 A A, A`×3, `9 9a Aa, Aa, A 9`×2, `9 Aa 9, Aa, A 9`×2, `9 A A A, A`×1, `9 A A, Aa`×1, `A Aa Aa, 9 Aa Aa 9, Aa Aa, A 9`×1, `9 Aa Aa 9, Aa, A 9`×1, `9 A 9a Aa Aa, Aa Aa, A 9`×1
preceded by: `as`×3, `at`×3, `address`×1, `odgers91@btinternet.com,`×1, `is`×1, `to`×1, `file:`×1, `verified:`×1

- ⏎⏎Re: KISA STEVENSON, home address ⟦140 TAVNAGHMORE ROAD, CLOGH⟧⏎⏎I would be grateful for your asse
- bhimanyu.rodgers91@btinternet.com, ⟦153 HAVANA WALK, EDERNEY⟧.⏎⏎RISKS/PLAN FOR NEXT SHIFT: High 
- greement. Home address recorded as ⟦45 LYNEDALE GRANGE, BUCKNA⟧. Report/accession ID: 07767311.⏎⏎I
- a.com and confirms home address as ⟦160 BEN EDEN PARK, KIRKISTOWN⟧. Review arranged with ROYAL VICTOR
- d nausea. Home address recorded as ⟦150 DIVIS DRIVE, Pomeroy⟧. Report/accession ID: 0667193979.⏎
-  patient’s home address on file is ⟦URB San Patricio, 428 Cll Mora 772, San Juan, PR 00901⟧.⏎⏎Results:⏎⏎Complete blood count⏎W
- itten instructions also be sent to ⟦644 State Rte 988, Hammond, LA 70403⟧ for home reference.
- 096313986⏎Patient address on file: ⟦581 E 5th South St, Dutch John, UT 84023⟧

### Address_Location:Caregiver: 45 missed

shapes: `Aa`×24, `A`×12, `Aa Aa`×7, `A A`×1, `A A A`×1
preceded by: `in`×5, `from`×3, `hospital`×2, `gp`×2, `pediatrics,`×2, `healey,`×1, `practitioner`×1, `0015304`×1

- lly,⏎⏎F. Sharpe⏎GP⏎Ulster Hospital⏎⟦ARMOY⟧⏎Professional identifier: 0996112
- erring clinician: ARANDEEP HEALEY, ⟦Tongland⟧⏎Professional ID: 0175972
- ⏎Yours sincerely,⏎⏎Daryle Hoque⏎GP⏎⟦THE DIAMOND⟧
- aiden worrall⏎General Practitioner⏎⟦LOUGHGALL⟧⏎Professional ID: 0435580
- ncerely,⏎⏎Misty Hubbard⏎GP⏎0015304⏎⟦Blackford⟧
- AGE, MBBS⏎Cardiology referral from ⟦Balhalgardy⟧⏎Professional identifier: 0919360
- ferring clinician: Rhianne CURTIS, ⟦BALLYGALLEY⟧⏎Organisation: BELFAST CITY HOSPITA
- l is from Royal Victoria Hospital, ⟦HILLSBOROUGH⟧. Please direct correspondence to t

### Address_Location:Other: 127 missed

shapes: `Aa`×80, `A`×26, `Aa Aa`×15, `Aa a Aa`×2, `Aa a' Aa`×1, `A'A A`×1, `A A A`×1, `Aa Aa Aa`×1
preceded by: `in`×30, `locality`×26, `from`×25, `as`×22, `of`×7, `through`×3, `dodds,`×1, `maryanna,`×1

- d through the locality recorded as ⟦Loch a' Ghainmhich⟧ if needed. Discharge advice was ex
-  Their sibling, TAYSHIA MOON, from ⟦OMAGH⟧, was updated during the admission 
- gency contact locality recorded as ⟦Ythanbank⟧.⏎⏎Condition at discharge⏎Pain subs
- er spouse, ella-ray flanagan, from ⟦Hardmuir⟧, provided collateral history and r
- gency contact locality recorded as ⟦Brabstermire⟧.⏎⏎Follow-up and safety-netting⏎Rev
- ⏎Spouse: minerva coleman, locality ⟦BERAGH⟧. Updated regarding discharge arran
- ce. Sibling’s locality recorded as ⟦Bellochantuy⟧.⏎⏎Condition at discharge: stable, 
- contact: Elsiemae Downes, locality ⟦CARRIGANS⟧.

### Organization:Healthcare: 74 missed

shapes: `Aa Aa Aa`×19, `A A A`×13, `Aa Aa Aa Aa`×8, `Aa Aa`×4, `Aa - Aa Aa a Aa Aa`×3, `A A A A`×3, `Aa Aa a Aa`×2, `Aa Aa a Aa Aa`×2
preceded by: `at`×19, `with`×12, `through`×8, `from`×4, `clinician,`×4, `facility:`×4, `by`×3, `at:`×3

-  with the on-call surgical team at ⟦University Hospital Llandough⟧. They advised outpatient review pr
- e on-call general surgical team at ⟦University Hospital of Wales⟧ for review and likely laparoscopic
-  is not evident on the report from ⟦University Hospital Llandough⟧.⏎⏎Clinical impression:⏎Acute pulmo
- itive; ultrasound arranged through ⟦Inpatient - University Hospital of North Durham⟧.⏎⏎ACTIONS⏎Cannula inserted. Intrav
-  with the on-call surgical team at ⟦University Hospital of Wales⟧, who advised admission for operati
-  with the on-call surgical team at ⟦University Hospital of North Durham⟧. Patient accepted for surgical ass
- scussed with acute medical team at ⟦University Hospital Llandough⟧; suitable for admission for IV ant
- lowering strategy.⏎⏎Discussed with ⟦UNIVERSITY HOSPITAL OF WALES⟧; outpatient review booked for 2024

### Organization:Other: 66 missed

shapes: `Aa Aa Aa`×41, `Aa Aa Aa Aa`×15, `A Aa Aa`×8, `Aa-a Aa Aa`×1, `Aa Aa Aa Aa Aa`×1
preceded by: `with`×17, `at`×14, `through`×9, `affiliation:`×4, `support:`×3, `informed`×1, `symptoms.`×1, `ask`×1

-  MCDONAGH. They have also informed ⟦MAGHABERRY Community Centre⟧ that fatigue may affect attendance
- orrespondence/support affiliation: ⟦Norwood Green Community Centre⟧⏎⏎Presenting complaint⏎Several mont
- ain or new neurological symptoms.⏎⏎⟦Mountjoy Town Council⟧ has been informed that appointment
- nder some work-related pressure at ⟦South Knighton Voluntary Service⟧, with reduced sleep on several nig
- ng attendance and participation at ⟦KESH Sports Club⟧. There has been no reported fainti
- pointments in the meantime and ask ⟦Gerlan Sports Club⟧ to support any temporary adjustmen
- is able to work as a Pharmacist at ⟦Aird-dhubh Secondary School⟧, although concentration is reduced
- ng concentration and attendance at ⟦Overbrae Voluntary Service⟧, where the patient’s occupation is

### ID:Patient: 12 missed

shapes: `9`×8, `9 9 9`×3, `A9A9`×1
preceded by: `is`×4, `under`×3, `identifier:`×3, `to`×1, `reference`×1

- by latika iqbal⏎Report filed under ⟦0916333040⟧
- ESR today; results to be linked to ⟦L21P48524⟧.⏎- Continue regular methotrexate a
- perforation. Result reviewed under ⟦08496234⟧.⏎⏎Impression: Acute uncomplicated 
- ANCASTER⏎MRN / patient identifier: ⟦008 614 794⟧⏎Specimen: EDTA whole blood⏎Request
-  M. WISE⏎MRN / patient identifier: ⟦095 836 537⟧⏎Patient contact: 07700 900637⏎Spec
- s satisfactory. Report filed under ⟦04258200⟧.⏎⏎Management to date:⏎Sleep hygien
- SI MARSH⏎MRN / patient identifier: ⟦060 276 287⟧⏎Collection date: 2004-12-14⏎Patien
- tive lesion.⏎⏎The patient’s MRN is ⟦094243030⟧. Please review the available imagi

### ID:Caregiver: 136 missed

shapes: `9`×136
preceded by: `md,`×14, `identifier:`×3, `identifier`×2, `clinician`×2, `medicine`×2, `laderer,`×2, `md`×2, `whittingham,`×2

-  Professional identifier recorded: ⟦0871376⟧. Escalate promptly for fever, sudd
- irectly at appointment.⏎⏎M. Oliver⏎⟦0335900⟧⏎Referring clinician, Queen Elizabe
- ring clinician: Khawar McLAUGHLIN, ⟦0666462⟧⏎Clinical locality: MAGHERAMASON⏎⏎D
- g clinician: AURORA-LOUISE BASHIR, ⟦0948396⟧⏎Service locality: STEWARTSTOWN⏎⏎Cl
- eeks.⏎⏎Signed⏎AURORA-LOUISE BASHIR⏎⟦0948396⟧
- sional ID for reviewing clinician: ⟦0590827⟧.⏎⏎Plan for next shift: Continue IV
- inician: Dr Halil Wilkinson, MBBS, ⟦0983710⟧⏎Service locality: AGIVEY⏎⏎Dear Hea
- rring clinician.⏎⏎ANAHITA BOURNE  ⏎⟦0978004⟧  ⏎For Royal Infirmary of Edinburgh

### Age_Birthdate: 16 missed

shapes: `9 a/a`×10, `a 9 a a`×6
preceded by: `context:`×4, `age:`×3, `a.`×1, `current:`×1, `field:`×1, `blackburn`×1, `p.,`×1, `stage:`×1

- ent: Abi-Mae Sanders⏎Clinical age: ⟦day 3 of life⟧⏎Legal guardian: Raiqa Nixon⏎Contac
- ubin report⏎⏎Patient: Lathaniel A.⏎⟦4 m/o⟧⏎MRN: H6692938⏎Specimen collected: 
- ent: DEACON-JAMES DAVISON⏎Current: ⟦day 3 of life⟧⏎MRN: MRN-04391902⏎Father: MAYARA K
- nsley-rae mcdonnell⏎DOB/age field: ⟦18 m/o⟧⏎Date: 1 Dec 2023⏎Named carer: moth
- al Unit⏎⏎Patient: raysha blackburn⏎⟦day 3 of life⟧; mother Daniele WEBBER present and
-  number: KN605915D⏎⏎Re: Dustin P., ⟦day 3 of life⟧⏎⏎I would be grateful for your urge
- ⏎⏎Patient: T. Morley⏎Clinical age: ⟦day 3 of life⟧⏎Father: Shanzey⏎Report/accession I
- than-jay tomlinson⏎Clinical stage: ⟦4 m/o⟧⏎Specimen: capillary blood, bilirub

### Profession: 10 missed

shapes: `Aa`×7, `Aa a`×2, `Aa Aa Aa`×1
preceded by: `as`×5, `a`×4, `is`×1

- yed by MAGHERAMASON Sports Club as ⟦Taxi driver⟧. Increasing time is required for r
- cated asthma.⏎⏎Cora-Leigh works as ⟦Chef⟧ at Sheddocksley Secondary School. 
- ctivities and is able to work as a ⟦Pharmacist⟧ at Aird-dhubh Secondary School, al
- atient’s occupation is recorded as ⟦Postal worker⟧. There has also been increased rea
- ems.⏎⏎The patient is employed as a ⟦Librarian⟧ by Cornaigbeg Community Centre. Th
- t yet available.⏎⏎The patient is a ⟦Builder⟧ and lives at 142 Greenwood Avenue,
- cancer.⏎⏎The patient occupation is ⟦Pharmacist⟧, employed by Heathfield Further Ed
-  emergency. The patient works as a ⟦Plumber⟧ at Skinnet Town Council.⏎⏎Current 

## Found but wrong boundaries (partial or inexact)

### Name:Patient: 3

- Discharge summary⏎⏎Patient: ⟦sahira senior⟧, 66-year-old Black female patient⏎  →  'sahira':Name
- NHS number: 000 003 6944⏎⏎Patient: ⟦SON WILLS⟧⏎MRN: 077 910 470⏎Address: 9 Shilto  →  'WILLS':Name
- Patient: ⟦truly day⟧⏎DOB: 18 Sep 1943⏎Contact: 07700 90  →  'truly':Name

### Name:Caregiver: 134

- nd discharge advice discussed with ⟦Dr Chahat Cook, MBBS⟧, Emergency Medicine clinician.  →  'with Dr Chahat Cook, MBBS':Name
-  discharge plan were reviewed with ⟦Dr Aureya Oakley, MBBS⟧.⏎⏎Follow-up and safety-netting⏎The  →  'with Dr Aureya Oakley, MBBS':Name
- rink.⏎⏎Reviewed and handed over by ⟦Dr Caileb Slade, MBBS⟧.  →  'by Dr Caileb Slade, MBBS':Name
- wered before discharge.⏎⏎Signed by ⟦Dr Yakoub Ratcliffe, MBBS⟧⏎Accident and emergency, Ealing Hos  →  'by Dr Yakoub Ratcliffe, MBBS':Name
- /2022⏎⏎Validated electronically by ⟦Dr Meriel Noor, MBBS⟧⏎Laboratory medicine consultant⏎Rep  →  'by Dr Meriel Noor, MBBS':Name
- few days.⏎⏎Discharge authorised by ⟦Dr Imogine Rahman, MBBS⟧, consultant physician, on behalf o  →  'by Dr Imogine Rahman, MBBS':Name
- ail.com⏎⏎Validated and reported by ⟦Dr Maani Ryan, MBBS⟧⏎Laboratory clinician⏎Report date:   →  'by Dr Maani Ryan, MBBS':Name
- -04-12.⏎⏎Validated and reported by ⟦Dr Ayeisha Li, MBBS⟧; GMC: 0229740  →  'by Dr Ayeisha Li, MBBS':Name

### Name:Other: 7

- rk with Belfast Voluntary Service. ⟦Dunya⟧, the patient’s sister, reports tha  →  'Belfast Voluntary Service. Dunya':Organization
- e symptoms or chest pain reported. ⟦Shri Drew⟧, the patient’s sibling, provided c  →  'Drew':Name
- ion discussed with the patient and ⟦Shri Drew⟧; both confirmed understanding.  →  'Drew':Name
-  female patient  ⏎Collateral: Aunt ⟦Bahadur GOUGH⟧ present; reports night-time cough   →  'Aunt Bahadur GOUGH':Name
- e and reported weight loss. Sister ⟦Iylah⟧ updated by telephone.⏎⏎Observation  →  'Sister Iylah':Name
- ks at Belfast Sports Club. Sibling ⟦Kacie-Ann⟧ assists with appointments and repo  →  'Belfast Sports Club. Sibling Kacie-Ann':Organization
-  07700 900066⏎Next of kin/partner: ⟦adison day⟧⏎⏎Presenting complaint: Sudden onse  →  'adison':Name

### Address_Location:Patient: 106

- nes. Your recorded home address is ⟦169 Richardson Road, Insch, AB52 6AB⟧, and your contact detail is 07700   →  '169 Richardson Road, Insch, AB':Address_Location
- Patient’s home address recorded as ⟦13 Brewis Terrace, Birchburn, KA27 8AA⟧ for discharge planning.⏎⏎Escalatio  →  '13 Brewis Terrace, Birchburn, KA':Address_Location
- d as 07700 900318 and home address ⟦123 Morrison Lane, Alford, AB33 8AA⟧ before any discharge planning; the  →  '123 Morrison Lane, Alford, AB':Address_Location
- worsening breathlessness. Lives at ⟦166 LLys Illtern, Monmouth / Trefynwy, NP25 3AB⟧.⏎⏎Presenting problem⏎Progressive s  →  'NP25 3AB':Address_Location
- ation: Receptionist. Home address: ⟦119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA⟧. Preferred contact telephone: 0770  →  '119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA. Preferred contact telephone: 07700 900982.':Address_Location
- gby69@outlook.com and home address ⟦78 Glenspean Place, Bellshill, ML4 1AB⟧.⏎⏎Plan for next shift⏎Continue fou  →  '78 Glenspean Place, Bellshill, ML':Address_Location
- act. The patient’s home address is ⟦116 Raith Road, Inverness / Inbhir Nis, IV99 1AA⟧ and preferred email contact is jed  →  '116 Raith Road, Inverness':Address_Location | 'IV99 1AA':Address_Location
- nt: shabaan flanagan⏎Home address: ⟦4 DUNNAMAN PARK, ANNALONG⟧  Contact: 07700 900701⏎Relative pr  →  '4 DUNNAMAN PARK, ANNALONG  Contact: 07700 900701':Address_Location

### Address_Location:Caregiver: 21

- e⏎From: Dr Nana-Ama Gilbert, MBBS, ⟦DOLLINGSTOWN⟧⏎Organisation: Royal Victoria Hospi  →  'Dr Nana-Ama Gilbert, MBBS, DOLLINGSTOWN':Organization
-  JOHN, MBBS, General Practitioner, ⟦MAYOBRIDGE⟧⏎Organisation: BELFAST CITY HOSPITA  →  'Dr Chima JOHN, MBBS, General Practitioner, MAYOBRIDGE':Organization
-  service: Royal Victoria Hospital, ⟦WARINGSFORD⟧  →  'Royal Victoria Hospital, WARINGSFORD':Organization
- r⏎From: Altnagelvin Area Hospital, ⟦CAPPAGH⟧⏎Referring clinician: M. NEAL, 0088  →  'Altnagelvin Area Hospital, CAPPAGH':Organization
-  identifier: GMC 0281764⏎Locality: ⟦Ceann a-muigh Chuil⟧⏎⏎Yours faithfully,⏎⏎Dr Cesar LAWRE  →  'Ceann':Address_Location
- vice⏎⏎From: Belfast City Hospital, ⟦AGIVEY⟧⏎Patient: Efemena Mellor⏎Referring   →  'Belfast City Hospital, AGIVEY':Organization
- I⏎From: Altnagelvin Area Hospital, ⟦BELLEEK⟧⏎Referring clinician: ellie-jae kay  →  'Altnagelvin Area Hospital, BELLEEK':Organization
- ervice: Altnagelvin Area Hospital, ⟦FORKHILL⟧  →  'Altnagelvin Area Hospital, FORKHILL':Organization

### Address_Location:Other: 18

-  contact Jorden Rodgers (locality: ⟦Logie Coldstone⟧) updated during the admission with  →  'Logie Coldstone)':Address_Location
- th father D. Edwards, who lives in ⟦Ayres of Selivoe⟧. He verbalised understanding and a  →  'Ayres':Address_Location
-  care. Emergency contact locality: ⟦Lower Largo⟧.⏎⏎Reason for admission:⏎Wheeze, in  →  'Lower Largo.':Address_Location
- story; emergency contact locality: ⟦Drumligair⟧.⏎⏎Key results⏎Admission blood test  →  'Drumligair.':Address_Location
- ent and friend. Friend’s locality: ⟦Borrowstoun⟧.⏎⏎Discharging clinician: Remaya-Ro  →  'Borrowstoun.':Address_Location
-  with partner. Partner’s locality: ⟦Crossfields⟧.⏎⏎Follow-up / actions⏎GP review an  →  'Crossfields.':Address_Location
- pouse; emergency contact locality: ⟦Washington⟧.⏎⏎Discharging clinician: Trelynn C  →  'Washington.':Address_Location
-  home. Emergency contact locality: ⟦Boonton⟧.⏎⏎Discharge instructions:⏎Increase  →  'Boonton.':Address_Location

### Organization:Healthcare: 233

- ⏎Requesting service: Rheumatology, ⟦Skewen Medical Centre⟧⏎Specimen collection/report date: 2  →  'Rheumatology, Skewen Medical Centre':Organization
- tient: niyah-rae houghton⏎Seen at: ⟦Norfolk ICASH - Queen Elizabeth Hospital⟧⏎The patient, aged 86, was reviewed  →  'Queen Elizabeth Hospital':Organization
- ⏎Discharging service: Gynaecology, ⟦Ulster Hospital⟧⏎Report/accession ID: 0815228527⏎⏎R  →  'Gynaecology, Ulster Hospital':Organization
-  faithfully,⏎⏎C. Short⏎0640873⏎For ⟦ROYAL INFIRMARY OF EDINBURGH⟧  →  'For ROYAL INFIRMARY OF EDINBURGH':Organization
- consultant physician, on behalf of ⟦Ulster Hospital⟧.  →  'of Ulster Hospital':Organization
- N SHARIF⏎MRN: MRN-09242879⏎Seen at ⟦WALTON HOSPITAL ACUTE BEDS⟧ by L. CURRY⏎⏎ADHEEN SHARIF was rev  →  'WALTON HOSPITAL':Organization
- de to the physiotherapy service at ⟦WALTON HOSPITAL ACUTE BEDS⟧ for graded exercise, lumbar streng  →  'WALTON HOSPITAL':Organization
- y Pregnancy and Acute Gynaecology, ⟦ROYAL VICTORIA HOSPITAL⟧⏎Report/accession ID: 0779293053⏎⏎R  →  'Early Pregnancy and Acute Gynaecology, ROYAL VICTORIA HOSPITAL':Organization

### Organization:Other: 11

-  sleep and attendance at work with ⟦Belfast Voluntary Service⟧. Dunya, the patient’s sister, repo  →  'Belfast Voluntary Service. Dunya':Organization
- taining concentration at work with ⟦SCARVA Secondary School⟧. There have been no reported episo  →  'SCARVA Secondary School. There':Organization
- be helpful.⏎⏎The patient works for ⟦CRAIGAVON Sports Club⟧. Their spouse, dija newell, report  →  'CRAIGAVON Sports Club. Their':Organization
- ocial/family:⏎Non-smoker. Works at ⟦Belfast Sports Club⟧. Sibling Kacie-Ann assists with ap  →  'Belfast Sports Club. Sibling Kacie-Ann':Organization
-  to manage alongside their work at ⟦GREYSTEEL Secondary School⟧. Their adult child, Nuraz, has not  →  'GREYSTEEL Secondary School. Their':Organization
- urrent illness.⏎⏎Social:⏎Works for ⟦Calderbank Further Education College⟧. Independent with self-care. Linar  →  'Calderbank Further Education College. Independent':Organization
-  counselling.⏎⏎Social:⏎Employed by ⟦Aberdesach Community Centre⟧. Partner supportive. No safeguardi  →  'Aberdesach Community Centre. Partner':Organization
- .⏎⏎The patient remains employed by ⟦DONAGHCLONEY Housing Association⟧. Their emergency contact is HARRIS  →  'DONAGHCLONEY Housing Association. Their':Organization

### ID:Patient: 86

- ine culture⏎⏎Patient: Sanayah⏎MRN: ⟦019 576 505⟧⏎Home address: 165 Hinchcliffe, Chi  →  '019':ID
-  21 C⏎⏎Patient: Zalayah ROPER⏎MRN: ⟦099 508 763⟧⏎Referring service: Queen Victoria   →  '099':ID
- ted result/accession identifier is ⟦0029301109⟧.⏎⏎Yours faithfully,⏎⏎Tam Hawkes  →  '139 CARSONSTOWN ROAD, AGIVEY. The associated result/accession identifier is 0029301109.':Address_Location
- ry⏎⏎Patient: Sienna-Louise V.⏎MRN: ⟦013 025 563⟧⏎Discharging service: General Medic  →  '013':ID
- port⏎⏎Patient: AMARISSA CURRY⏎MRN: ⟦078 409 289⟧⏎Requesting clinician: GP (name not  →  '078':ID
- ry Report⏎⏎Patient: N. Martin⏎MRN: ⟦037 575 719⟧⏎Specimen: EDTA whole blood⏎Collect  →  '037':ID
-  003 6944⏎⏎Patient: SON WILLS⏎MRN: ⟦077 910 470⟧⏎Address: 9 Shilton Close, Salisbur  →  '077':ID
- ment⏎⏎Patient: jonelle sandhu⏎MRN: ⟦030 359 538⟧⏎Home address: 137 Stryd-y-Capel, L  →  '030':ID

### ID:Caregiver: 2

- tion: Duty doctor reviewed; GMC ID ⟦0314778⟧. Repeat clinical review if unable   →  'GMC ID 0314778':ID
- r: 0001661664⏎⏎From: Jahdel Price, ⟦0355361⟧⏎Organisation: ROYAL INFIRMARY OF E  →  'Jahdel Price, 0355361':Organization

### Age_Birthdate: 14

-  ED handover⏎⏎Patient: R. Sweeney  ⟦16 y/o⟧⏎History from patient and father, R  →  '16':Age_Birthdate
- Patient: Aviva Byrne⏎Clinical age: ⟦7 wk old⟧⏎Parent present: A. COLLIER⏎⏎Reason  →  '7 wk':Age_Birthdate
- ing management.⏎⏎K-Ci is currently ⟦7 wk old⟧, brought by legal guardian A. Hutc  →  '7 wk':Age_Birthdate
- ⏎⏎Patient: Rumaithah⏎Clinical age: ⟦2 wk old⟧⏎Parent present: Iori⏎Referred from  →  '2 wk':Age_Birthdate
- 16⏎⏎Patient: N. Howe⏎Clinical age: ⟦7 wk old⟧ infant⏎Legal guardian: menisha mun  →  '7 wk':Age_Birthdate
- comfort. Patient: Kishaan P., aged ⟦27 years⟧. Home address: 9 Afon Llwyd Terrac  →  '27 year':Age_Birthdate
- ort⏎⏎Patient: Cyriah⏎Clinical age: ⟦2 wk old⟧⏎Legal guardian: Deshae⏎Contact: (2  →  '2 wk':Age_Birthdate
-  Cropp⏎MRN: 09984136⏎Clinical age: ⟦7 wk old⟧⏎History: Jaundice first noted duri  →  '7 wk':Age_Birthdate

### Contactdetails: 20

-  0AA. Preferred contact telephone: ⟦07700 900982⟧.⏎⏎On examination, she appeared wel  →  '119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA. Preferred contact telephone: 07700 900982.':Address_Location
-  DUNNAMAN PARK, ANNALONG  Contact: ⟦07700 900701⟧⏎Relative present: sibling, PRAIRIE  →  '4 DUNNAMAN PARK, ANNALONG  Contact: 07700 900701':Address_Location
-  Scaur, DG5 4AA⏎Preferred contact: ⟦moses.o'donnell30@hotmail.com⟧⏎⏎Admission reason⏎Admitted under G  →  'donnell30@hotmail.com':Contactdetails
- orea, Minffordd, LL48 6AA⏎Contact: ⟦ryanne.o'leary74@gmail.com⟧⏎⏎Reason for review: Persistent dep  →  'leary74@gmail.com':Contactdetails
- , Saundersfoot, SA69 9AB  Contact: ⟦milou.blackburn31@hotmail.com⟧⏎⏎Situation: Acute left flank pain   →  '47 Parc Waen, Saundersfoot, SA69 9AB  Contact: milou.blackburn31@hotmail.com':Address_Location
- nt⏎MRN: 042862061⏎Patient contact: ⟦alexandra.o'connell63@virginmedia.com⟧⏎⏎A&E assessment⏎⏎Presenting compla  →  'connell63@virginmedia.com':Contactdetails
- umnock, KA18 1AA. Patient contact: ⟦alyssia.coles36@sky.com⟧.⏎⏎B: Orthopnoea on lying flat, bil  →  "23 Nun's Walk, Cumnock, KA18 1AA. Patient contact: alyssia.coles36@sky.com.":Address_Location
- 93 B⏎MRN: 0563741⏎Patient contact: ⟦anfa.o'donnell15@virginmedia.com⟧⏎Clinic: Cardiology outpatient revi  →  'donnell15@virginmedia.com':Contactdetails

## Found but wrong category

### gold Name:Caregiver → predicted Organization: 24

- nt: Fitz Raza⏎MRN: 048449794⏎From: ⟦A. Howe⟧, BELFAST CITY HOSPITAL⏎⏎Dear Clini
- on clinic / general medicine⏎From: ⟦Dr Nana-Ama Gilbert, MBBS⟧, DOLLINGSTOWN⏎Organisation: Royal 
- h headache/light-headedness⏎⏎From: ⟦Dr Chima JOHN, MBBS⟧, General Practitioner, MAYOBRIDGE⏎
- urance number: ZZ 79 25 90 D⏎From: ⟦Dr Amarleen Nixon, MBBS⟧, GP, BELFAST CITY HOSPITAL⏎Referri
- logy⏎NHS number: 0001661664⏎⏎From: ⟦Jahdel Price⟧, 0355361⏎Organisation: ROYAL INFIR
- docrinology  ⏎SSN: 983796065⏎From: ⟦MELENA MCMINIMY⟧, Heron⏎⏎Patient: Arav K.  ⏎DOB: De
- to Pediatric Otolaryngology⏎⏎From: ⟦elbert mattiuz⟧, Clinician, St Mary-Corwin Hospita
- ediatric Dermatology Service⏎From: ⟦kobichimdi hagopian⟧, Community Pediatrics⏎Referring or

### gold Address_Location:Caregiver → predicted Organization: 20

- e⏎From: Dr Nana-Ama Gilbert, MBBS, ⟦DOLLINGSTOWN⟧⏎Organisation: Royal Victoria Hospi
-  JOHN, MBBS, General Practitioner, ⟦MAYOBRIDGE⟧⏎Organisation: BELFAST CITY HOSPITA
-  service: Royal Victoria Hospital, ⟦WARINGSFORD⟧
- r⏎From: Altnagelvin Area Hospital, ⟦CAPPAGH⟧⏎Referring clinician: M. NEAL, 0088
- vice⏎⏎From: Belfast City Hospital, ⟦AGIVEY⟧⏎Patient: Efemena Mellor⏎Referring 
- I⏎From: Altnagelvin Area Hospital, ⟦BELLEEK⟧⏎Referring clinician: ellie-jae kay
- ervice: Altnagelvin Area Hospital, ⟦FORKHILL⟧
- : 983796065⏎From: MELENA MCMINIMY, ⟦Heron⟧⏎⏎Patient: Arav K.  ⏎DOB: December 

### gold ID:Caregiver → predicted Contactdetails: 14

-  verified in chart.⏎⏎Documented by ⟦029799272⟧.
- rging clinician: daphne angelozzi, ⟦021933126⟧⏎⏎Torrance Caffie was evaluated in 
-  visit.⏎⏎Signed,⏎daphne angelozzi, ⟦021933126⟧
- released by: Lilliann Muzzall, MD, ⟦029505871⟧⏎Final status: Final report
- eciated.⏎⏎Sincerely,⏎⏎kate fatemi, ⟦020841913⟧⏎Referring clinician⏎Berkeley Medic
- idated/reported by: M. Luczkowski, ⟦022204178⟧
- erring clinician: Kevyn Toppel, ID ⟦027987690⟧⏎⏎Dear Sleep Medicine Clinician,⏎⏎I
- boratory clinician: Holton Deluco, ⟦028489468⟧

### gold Contactdetails → predicted Address_Location: 12

-  0AA. Preferred contact telephone: ⟦07700 900982⟧.⏎⏎On examination, she appeared wel
-  DUNNAMAN PARK, ANNALONG  Contact: ⟦07700 900701⟧⏎Relative present: sibling, PRAIRIE
- , Saundersfoot, SA69 9AB  Contact: ⟦milou.blackburn31@hotmail.com⟧⏎⏎Situation: Acute left flank pain 
- umnock, KA18 1AA. Patient contact: ⟦alyssia.coles36@sky.com⟧.⏎⏎B: Orthopnoea on lying flat, bil
- tardawe, SA8 3AB. Patient contact: ⟦shamen.salmon40@outlook.com⟧.⏎⏎ASSESSMENT⏎Alert, speaking norma
- ncader, SA39 9AA  Patient contact: ⟦07700 900005⟧⏎⏎Presented with 5 days of persiste
- th Fwy, Encino, TX 78353. Contact: ⟦farid.fabella92@comcast.net⟧.⏎Disposition: Discharged ambulator
- egon, MI 49441. Preferred contact: ⟦(617) 555-0167⟧.⏎⏎Discharging clinician: damere br

### gold ID:Patient → predicted Contactdetails: 10

- sion ID for the imaging episode is ⟦026966020⟧.⏎⏎Assessment⏎⏎The history is most 
- 0870⏎⏎Patient: KELSIE-MAE GUY⏎MRN: ⟦029 419 048⟧⏎Responsible team: General Medicine
- SITUATION⏎Joy W. (MRN ⟦020 989 045⟧) — ED assessment, acute abdominal 
- e Report⏎⏎Patient: J. Pearson⏎MRN: ⟦021 036 327⟧⏎Clinical context: 9-year-old Middl
- wood⏎NHS number: 000 739 6199⏎MRN: ⟦027 354 832⟧⏎Clinic: Cardiology, Upton Hospital
- MAGUIRE⏎DOB: 22 November 2008⏎MRN: ⟦027 628 943⟧⏎Requesting service: Cardiology⏎Spe
- 5 C⏎⏎Patient: kirandeep welch⏎MRN: ⟦020 278 017⟧⏎The patient, aged 18 months, was r
- 0-70-6281⏎⏎Patient: Kyrese E.⏎MRN: ⟦022 883 860⟧⏎Discharging facility: Meadville Me

### gold Organization:Healthcare → predicted Name: 7

-  limited. The case was reviewed by ⟦Aberdeen Royal Infirmary⟧ cardiology services.⏎⏎Discharge me
- ed by mother, Donnach. Reviewed by ⟦Aberdeen Royal Infirmary⟧ medical team.⏎⏎CURRENT CONCERNS: A
- t present: ZAN WANG⏎Admitted under ⟦Aberdeen Royal Infirmary⟧⏎Patient contact: peggy.beaumont41@
- and heart rate. Case reviewed with ⟦Abrazo Scottsdale Campus⟧.⏎⏎Disposition: Discharge home with
-  providing history. Admitted under ⟦Sidney Health Center⟧.⏎⏎Background: Vomiting and watery 
- enneff⏎Care setting: Pediatric ED, ⟦Hospital Upr, Dr Federico Trilla⟧⏎⏎Chief complaint: Wheeze, increase
- , or poor response. Follow up with ⟦Hospital Upr, Dr Federico Trilla⟧ primary care.

### gold ID:Patient → predicted Address_Location: 5

- ted result/accession identifier is ⟦0029301109⟧.⏎⏎Yours faithfully,⏎⏎Tam Hawkes
- SIXMILECROSS. Report/accession ID: ⟦043828057⟧.⏎⏎B: Established cardiac condition
- ur, IL 61875. Report/accession ID: ⟦20/890505⟧.
- gs, WY 82224. Report/accession ID: ⟦0415448937⟧.⏎⏎Current assessment: Awake, appro
- in, WV 25617. Report/accession ID: ⟦A26S36217⟧.⏎⏎BACKGROUND: Postoperative incisi

### gold Address_Location:Other → predicted Name: 3

- dress/contact locality for mother: ⟦TEDD⟧⏎Discharging service: Royal Victori
- Next of kin: RHUEBEN CAIN, spouse, ⟦DONAGH⟧⏎⏎Reason for admission⏎Persistent v
- ntact: LANNA SORANNO, adult child, ⟦Stewart⟧⏎⏎Reason for admission:⏎Reduced uri

### gold Name:Other → predicted Organization: 2

- rk with Belfast Voluntary Service. ⟦Dunya⟧, the patient’s sister, reports tha
- ks at Belfast Sports Club. Sibling ⟦Kacie-Ann⟧ assists with appointments and repo

### gold Organization:Other → predicted Address_Location: 2

- thma.⏎⏎Cora-Leigh works as Chef at ⟦Sheddocksley Secondary School⟧. The history has been provided joi
-  The patient works as a Plumber at ⟦Skinnet Town Council⟧.⏎⏎Current medication:⏎Amlodipine 1

### gold Age_Birthdate → predicted Date: 2

- d. Your date of birth is listed as ⟦October 27th, 1973⟧.⏎⏎You have noticed painless enlarg
-  and light-headedness. Your DOB is ⟦1961-01-09⟧, and your MRN is 032715623. At the

### gold Organization:Healthcare → predicted Address_Location: 2

- rd was reviewed with D. Kornick at ⟦MELROSEWAKEFIELD HEALTHCARE⟧.⏎⏎Assessment:⏎Asthma with increase
- ultural Equipment Mechanic⏎Seen at ⟦Salem Health West Valley⟧ by beto belsher.⏎⏎Chief concern: I

### gold ID:Caregiver → predicted Organization: 1

- r: 0001661664⏎⏎From: Jahdel Price, ⟦0355361⟧⏎Organisation: ROYAL INFIRMARY OF E

### gold Organization:Other → predicted Profession: 1

- on⏎Patient occupation: employed by ⟦CALEDON Community Centre⟧⏎Emergency contact: REGAN ALEXANDER

### gold Age_Birthdate → predicted Address_Location: 1

- 32. Callback: (312) 555-0177. DOB: ⟦March 11th, 1979⟧.⏎⏎Background: No known recent trau

### gold Address_Location:Caregiver → predicted Name: 1

- le through the referring office in ⟦Taylor⟧.⏎⏎Ezz Bossenbroek, MD

## False alarms (prediction overlaps no gold span)

### Name by rules (rule/label md_name_relation_after): 19

- mprove treatment consistency.⏎⏎At r⟦eview⟧, the child was bright and well. Th
- iew is planned for 2028-12-21. At t⟦hat appointment⟧, the clinician should confirm that
- n is suspected. Once this attack ha⟦s settled⟧, the GP can review whether urate-l
- plication.⏎⏎Over the past several m⟦onths⟧, their friend has noticed coughing
-  breathing difficulty.⏎⏎On review t⟦oday⟧, the child was alert but unsettled
-  has been present for 3 days.⏎⏎On e⟦xamination⟧, the child was comfortable and sys
- WTOWNABBEY Voluntary Service.⏎⏎At r⟦eview⟧, the child was alert and engaging.
- rted choking episode or fever. At r⟦eview⟧, the child was alert and able to s

### Organization by rules (rule/label md_org_suffix): 13

- available locally in RANDALSTOWN.⏎⏎⟦Assessment and hospital⟧ course⏎On arrival the patient was 
-  by mild to moderate dehydration.⏎⏎⟦Assessment and hospital⟧ course⏎⏎On arrival the patient was
- the respiratory medicine service.⏎⏎⟦Investigations and hospital⟧ course⏎⏎Urine pregnancy testing wa
- ol and no recent travel reported.⏎⏎⟦Assessment and hospital⟧ course⏎On arrival clinically dehyd
- er and assisted with the history.⏎⏎⟦Assessment and hospital⟧ course⏎⏎On arrival she appeared cl
- ntact and is based in PORTAFERRY.⏎⏎⟦Investigations and hospital⟧ course⏎Observations remained stabl
- he accompanying operative record.⏎⏎⟦Assessment and hospital⟧ course⏎Reviewed by the emergency s
- or a high temperature with rigors. ⟦Contact the hospital⟧ team promptly if the night sweats 

### Name by rules (rule/label md_name_header_inline): 10

- rtaken with consent and chaperone: ⟦mucopurulent⟧ discharge at cervical os, marked c
- nation with consent and chaperone: ⟦mucopurulent cervical⟧ discharge, cervical motion tendern
- nation with consent and chaperone: ⟦mucopurulent⟧ discharge, cervical motion tendern
- aid advice reinforced with father: ⟦place⟧ on side, protect from injury, do n
- 96-07-11.⏎⏎Advice given to mother: ⟦seek urgent⟧ assessment via NHS 111/A&E if unab
- ses. Blood tests requested via GP: ⟦FBC⟧, U&E, LFT, CRP and urate after fla
- nation with consent and chaperone: ⟦mucopurulent cervical⟧ discharge and cervical motion tend
- d. Reviewed with senior clinician: ⟦clinically stable⟧ for ambulatory treatment, no oxyge

### Name by rules (rule/label md_name_header): 10

- spital notes.⏎⏎Discharging doctor: ⟦professional⟧ identifier 0917697
- inical Genetics⏎Documenting nurse: ⟦bedside⟧ nursing entry⏎⏎Problem:⏎Admitted w
- eterioration.⏎⏎Discharging doctor: ⟦Professional⟧ identifier 0356920
- oyer: Hephzibah Senior Center⏎⏎Re: ⟦Consultation⟧ for persistent lumbar radiculopath
- ergency contact: BLASE CHMIEL⏎⏎Re: ⟦Consultation⟧ for persistent depressive symptoms
- al Medicine⏎Discharging clinician: ⟦Professional⟧ identifier LIC71888170⏎⏎Admission 
- tient: Mairead⏎MRN: 060302/93⏎⏎Re: ⟦Evaluation⟧ of symptomatic hypothyroidism and 
- morial Hospital⏎Emergency contact: ⟦listed⟧ in chart⏎⏎CC: Severe limb and back

### Name by rules (rule/label md_name_referring): 6

-  Parkinson disease. I am referring ⟦them⟧ for a specialist review of increas
- . Bainbridge⏎Weight: 28.6 kg⏎⏎Dear ⟦Dermatology Colleagues⟧,⏎⏎I would be grateful for your ass
- KILLOUGH Housing Association⏎⏎Dear ⟦Colleagues⟧,⏎⏎I am referring Qiao Charlton for
- ce-daily blood pressure record for ⟦one⟧ week and to bring this, together w
- he original family test report for ⟦comparison⟧ and review with the patient’s gene
- ort/accession ID: 0443604623⏎⏎Dear ⟦Rheumatology Colleagues⟧:⏎⏎I am referring this patient for 

### Profession by rules (rule/label md_profession): 6

- nn22@gmail.com⏎Patient occupation: ⟦secondary-school pupil⟧⏎⏎Thank you for attending the paedi
- t: salima kent⏎Patient occupation: ⟦warehouse operative⟧⏎Employer: NEWFERRY Public Library⏎
- t at baseline. Patient occupation: ⟦office administrator⟧.⏎⏎Examination⏎Alert, speaking in f
- atient: Gadiel⏎Patient occupation: ⟦Warehouse associate⟧⏎Employer: Charlotte Amalie Senior 
-  amirii kedley⏎Patient occupation: ⟦warehouse supervisor⟧⏎Employer: Chignik Lagoon Youth Ser
- ees with plan. Patient occupation: ⟦not applicable for young child⟧.⏎⏎Signed by: IVANIA WILFER

### Age_Birthdate by rules (rule/label md_age_header): 4

- r syncope. Current gestational age ⟦9⟧+4 weeks' gestation. Taking doxylam
- eremesis. Current gestational age: ⟦9⟧+4 weeks' gestation. Ongoing emesis
- n and weight loss⏎Gestational age: ⟦9⟧+4 weeks' gestation⏎⏎Presentation⏎P
- eremesis. Current gestational age: ⟦9⟧+4 weeks' gestation.⏎⏎Assessment: P

### Organization by rules (rule/label md_org_header): 4

- O⏎MRN: 00911967⏎Admitting service: ⟦Pulmonary Medicine⟧⏎Discharging clinician: Onika Eldri
- by: zakaryah milestone⏎Laboratory: ⟦Clinical Genetics Molecular Diagnostics⟧; report identifier retained in the
- ⏎MRN: 02684341⏎Requesting service: ⟦Pulmonary Medicine⟧⏎Reporting laboratory: TEXAS HEALTH
- tient: C. Oeder⏎Admitting service: ⟦Pulmonary Medicine⟧⏎Report/accession ID: 058309175⏎Hom

### Date by rules (rule/label year_ctx): 1

- s and interpretation undertaken in ⟦2028⟧ using the current laboratory pipel

### Name by rules (rule/label md_name_by): 1

-  team.⏎⏎Reviewed by on-call doctor⏎⟦Professional⟧ identifier: 0204872

### Address_Location by rules (rule/label md_place_signoff): 1

- TAR GEORGETOWN UNIVERSITY HOSPITAL⏎⟦Partner⟧, Kyria, included in discharge disc

### Name by model (rule/label repeat): 1

- ation.⏎⏎Signed,⏎Fidelia Riccomini, ⟦attending endocrinologist⟧

### Organization by rules (rule/label org_field): 1

- onroe⏎Patient occupation/employer: ⟦Warehouse⟧ associate, Elizabeth Public Librar

## Hard negatives redacted

### gestational_age: 4

- r syncope. Current gestational age ⟦9+4 weeks' gestation⟧. Taking doxylamine-pyridoxine with
- eremesis. Current gestational age: ⟦9+4 weeks' gestation⟧. Ongoing emesis with poor oral tol
- n and weight loss⏎Gestational age: ⟦9+4 weeks' gestation⟧⏎⏎Presentation⏎Persistent vomiting 
- eremesis. Current gestational age: ⟦9+4 weeks' gestation⟧.⏎⏎Assessment: Persistent vomiting 

### caregiver_role: 1

- bany jelliffe⏎Referring clinician: ⟦attending endocrinologist⟧⏎Author: Fidelia Riccomini⏎⏎Reason 

