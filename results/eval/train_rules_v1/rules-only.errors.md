# Error analysis: `rules-only` on `train_rules_v1`

## Missed gold spans (no overlap with any prediction)

### Name:Patient: 710 missed

shapes: `Aa`×208, `Aa Aa`×102, `Aa A.`×97, `a a`×88, `A A`×84, `A. Aa`×78, `Aa-Aa`×12, `Aa-Aa A.`×11
preceded by: `referring`×198, `of`×55, `patient,`×24, `dear`×15, `situation`×14, `illness:`×13, `for`×12, `history`×12

- Discharge summary for ⟦RENU BLACKWELL⟧⏎NHS number: 000 161 4780⏎⏎You were
- zaq, MRN 001416410⏎⏎I am referring ⟦Abdulrazaq⟧ from Royal Infirmary of Edinburgh 
- ical contributor to the symptoms.⏎⏎⟦Abdulrazaq⟧ describes persistent, difficult-to
- rge or become difficult to resist, ⟦Abdulrazaq⟧ should contact the GP surgery urge
- on  ⏎Contact detail: 07700 900208⏎⏎⟦SASKA SIMS⟧ remains admitted under the early p
- bourne Hospital⏎Occupation: Baker⏎⏎⟦Prabh⟧ was reviewed today with a three-we
-  detail: honie.hunt19@outlook.com⏎⏎⟦honie hunt⟧ was admitted under the early pregn
-  or GP appointment.⏎⏎At discharge, ⟦honie hunt⟧ was alert, haemodynamically stable
- Discharge summary for ⟦NOEMI MCMILLAN⟧⏎NHS number: 0003486606⏎⏎Encounter 
- ear Genetics Team,⏎⏎I am referring ⟦samar richards⟧ for assessment of a substantial fa

### Name:Caregiver: 1093 missed

shapes: `a a`×261, `A. Aa`×253, `Aa Aa`×233, `A A`×221, `A. A`×38, `Aa A`×22, `a-a a`×21, `A-A A`×15
preceded by: `sincerely,`×366, `by`×350, `by:`×96, `faithfully,`×73, `with`×37, `clinician:`×21, `signed,`×21, `regards,`×15

- clinic review.⏎⏎Yours faithfully,⏎⏎⟦J. Payne⟧⏎GMC number: 0987216⏎Referring clin
- an female patient  ⏎Clinical lead: ⟦Aryaz Khalid⟧⏎⏎Assessment⏎Alert and orientated, 
- nge character.⏎⏎Yours faithfully,⏎⏎⟦zeenah french⟧⏎General Practitioner
-  referral.⏎⏎Seen and documented by ⟦Nylah-Mae Sanderson⟧.
- be appreciated.⏎⏎Yours sincerely,⏎⏎⟦R. WATSON⟧
- ry 1989⏎⏎Validated and reported by ⟦sholah perkins⟧⏎Laboratory medicine clinician⏎Inte
- d in Braeswick.⏎⏎Yours sincerely,⏎⏎⟦SABIRAH AKRAM⟧⏎GMC: 0695920⏎Referring clinician
-  primary care.⏎⏎Yours faithfully,⏎⏎⟦H. Gill⟧⏎GP, ULSTER HOSPITAL
- 5450⏎Reviewed and plan agreed with ⟦V. Sidhu⟧, Crickhowell Medical Centre.
- ion is needed.⏎⏎Yours faithfully,⏎⏎⟦Yumi O'SHEA⟧⏎GP⏎Primary care service, RASHARKIN

### Name:Other: 1621 missed

shapes: `Aa`×338, `a a`×311, `A. Aa`×282, `Aa Aa`×267, `A A`×257, `A. A`×33, `Aa-Aa`×33, `Aa A`×31
preceded by: `spouse,`×124, `father,`×119, `mother,`×108, `sibling,`×85, `partner,`×84, `friend`×80, `child,`×78, `friend,`×74

- ⏎⏎With your consent, your relative ⟦A. Bryant⟧ in Poolewe was informed that you w
- ge or signs of systemic infection. ⟦BOJIDAR PRINCE⟧ updated by telephone regarding the
- l period not documented at triage. ⟦C. Daniel⟧, her relative, is available by tel
- ysuria or diarrhoea. Her relative, ⟦SIFN LANGLEY⟧, was updated by telephone with the
- ischarge contact arrangements with ⟦SIFN LANGLEY⟧ before discharge planning.
- , or cannot drink.⏎⏎Your relative, ⟦Syona Sanders⟧, who is based in LAURELVALE, was u
- ient, with collateral from brother ⟦Bissan Kane⟧.⏎⏎Presenting problem: 18-hour hist
- tial relevance to adult relatives. ⟦Jem Aston⟧, the patient’s adult sibling, is a
- observations deteriorate. Relative ⟦Teague⟧ updated by the patient and aware o
- eding.⏎⏎The patient’s adult child, ⟦Kyen Uddin⟧, was involved in discharge discuss

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
- end at bedside; patient resides at ⟦489 63rd St, Withee, WI 54498⟧.⏎⏎Background: Known systolic heart
- Home address and contact verified: ⟦833 28th St, Maidens, VA 23102⟧; (202) 555-0177.⏎⏎Escalation: Cove

### Address_Location:Caregiver: 84 missed

shapes: `Aa`×42, `A`×28, `Aa Aa`×12, `A A`×1, `A A A`×1
preceded by: `clinician`×13, `in`×9, `gp`×7, `gp,`×6, `from`×6, `clinician,`×4, `hospital`×3, `service,`×2

- umber: 0987216⏎Referring clinician⏎⟦BALLYHORNAN⟧
- m the referring clinician based in ⟦Braeswick⟧.⏎⏎Yours sincerely,⏎⏎SABIRAH AKRAM⏎
- mi O'SHEA⏎GP⏎Primary care service, ⟦RASHARKIN⟧
- lly,⏎⏎F. Sharpe⏎GP⏎Ulster Hospital⏎⟦ARMOY⟧⏎Professional identifier: 0996112
- .⏎⏎Yours sincerely,⏎⏎I. MCCANN⏎GP, ⟦ROSTREVOR⟧
- erring clinician: ARANDEEP HEALEY, ⟦Tongland⟧⏎Professional ID: 0175972
- eview.⏎⏎This referral is made from ⟦Bangor⟧. Please direct correspondence to m
- ion use. The referral is made from ⟦COLERAINE⟧.⏎⏎Yours sincerely,⏎⏎davis rowley
- ⏎Yours sincerely,⏎⏎Daryle Hoque⏎GP⏎⟦THE DIAMOND⟧
- ns.⏎⏎Yours sincerely,⏎⏎E. MORAN⏎GP⏎⟦Borgue⟧

### Address_Location:Other: 285 missed

shapes: `Aa`×174, `A`×64, `Aa Aa`×36, `Aa a Aa`×3, `A A`×2, `A'A A`×2, `Aa Aa Aa`×2, `Aa a' Aa`×1
preceded by: `in`×150, `from`×52, `locality`×26, `as`×22, `is`×8, `of`×7, `through`×3, `via`×1

- onsent, your relative A. Bryant in ⟦Poolewe⟧ was informed that you were leaving
- ve, Syona Sanders, who is based in ⟦LAURELVALE⟧, was updated with your agreement. 
- ng available through a relative in ⟦Fanagmore⟧.⏎⏎Discharging clinician: Dr Aureya
- AL. Cora-Mae Calvert, who lives in ⟦Clare⟧, has been updated about the discha
-  and treated. Sabriin Gordon, from ⟦Achfrish⟧, was recorded as her emergency con
- dmission; the family’s locality is ⟦BALLYMARTIN⟧.⏎⏎Assessment and investigations⏎On
- ted relative, erys imran, lives in ⟦DRUMBEG⟧ and was updated with the patient’s
- lative, Melchizedek Rowlands, from ⟦Whitefield⟧, was updated with consent. Dischar
- .⏎⏎The patient’s relative lives in ⟦Cessford⟧, and the discharge advice was disc
- ravel. A relative, XIANA HOWE from ⟦North Sandwick⟧, provided additional collateral hi

### Organization:Healthcare: 65 missed

shapes: `Aa Aa Aa`×17, `A A A`×12, `Aa Aa Aa Aa`×8, `Aa Aa a Aa`×3, `Aa - Aa Aa a Aa Aa`×3, `A A A A`×3, `Aa Aa`×3, `Aa Aa a Aa Aa`×2
preceded by: `at`×18, `with`×10, `through`×5, `from`×4, `facility:`×4, `to`×3, `clinician,`×3, `from:`×2

-  with the on-call surgical team at ⟦University Hospital Llandough⟧. They advised outpatient review pr
- mil RHODES, partner⏎Referred from: ⟦University Hospital of Wales⟧⏎Presenting complaint: Acute right 
- e on-call general surgical team at ⟦University Hospital of Wales⟧ for review and likely laparoscopic
-  is not evident on the report from ⟦University Hospital Llandough⟧.⏎⏎Clinical impression:⏎Acute pulmo
- itive; ultrasound arranged through ⟦Inpatient - University Hospital of North Durham⟧.⏎⏎ACTIONS⏎Cannula inserted. Intrav
-  with the on-call surgical team at ⟦University Hospital of Wales⟧, who advised admission for operati
-  with the on-call surgical team at ⟦University Hospital of North Durham⟧. Patient accepted for surgical ass
- scussed with acute medical team at ⟦University Hospital Llandough⟧; suitable for admission for IV ant
- lowering strategy.⏎⏎Discussed with ⟦UNIVERSITY HOSPITAL OF WALES⟧; outpatient review booked for 2024
- an: Discussed with miceal dyson at ⟦University Hospital Bristol and Weston Virtual Site⟧. Continue oral amoxicillin as pres

### Organization:Other: 47 missed

shapes: `Aa Aa Aa`×32, `Aa Aa Aa Aa`×8, `A Aa Aa`×5, `Aa-a Aa Aa`×1, `Aa Aa Aa Aa Aa`×1
preceded by: `at`×11, `with`×10, `through`×7, `support:`×2, `symptoms.`×1, `ask`×1, `via`×1, `attend`×1

- ain or new neurological symptoms.⏎⏎⟦Mountjoy Town Council⟧ has been informed that appointment
- nder some work-related pressure at ⟦South Knighton Voluntary Service⟧, with reduced sleep on several nig
- thma.⏎⏎Cora-Leigh works as Chef at ⟦Sheddocksley Secondary School⟧. The history has been provided joi
- ng attendance and participation at ⟦KESH Sports Club⟧. There has been no reported fainti
- pointments in the meantime and ask ⟦Gerlan Sports Club⟧ to support any temporary adjustmen
- is able to work as a Pharmacist at ⟦Aird-dhubh Secondary School⟧, although concentration is reduced
- ng concentration and attendance at ⟦Overbrae Voluntary Service⟧, where the patient’s occupation is
- 4 1AB⏎Family support currently via ⟦Port Gaverne Town Council⟧.⏎⏎Reason for review: neonatal jaun
-  output remains usual. They attend ⟦Meadowmill Cottages Public Library⟧ and have been less settled there t
- vant information being shared with ⟦Llanidan Voluntary Service⟧ where needed for practical support

### ID:Patient: 22 missed

shapes: `9`×15, `A9A9`×3, `9 9 9`×3, `9/9`×1
preceded by: `is`×14, `under`×3, `identifier:`×3, `to`×1, `reference`×1

- resent. The report/accession ID is ⟦26/351462⟧. If attacks become more frequent, 
- ory report/accession identifier is ⟦0553952501⟧. The initial inflammatory markers 
- by latika iqbal⏎Report filed under ⟦0916333040⟧
-  associated report/accession ID is ⟦08391420⟧. I will forward the imaging report
- mality. The report/accession ID is ⟦L20S66999⟧.⏎⏎Current treatment is paracetamol
- the report/accession identifier is ⟦0688999720⟧. Routine blood tests, including fu
- ted report/accession identifier is ⟦051336404⟧. Results show total bilirubin 248 
- rtment; the report/accession ID is ⟦01853482⟧. Results did not identify an acute
- ESR today; results to be linked to ⟦L21P48524⟧.⏎- Continue regular methotrexate a
- perforation. Result reviewed under ⟦08496234⟧.⏎⏎Impression: Acute uncomplicated 

### ID:Caregiver: 215 missed

shapes: `9`×215
preceded by: `identifier`×49, `md,`×14, `identifier:`×11, `as`×5, `reference`×2, `gp`×2, `reference:`×2, `clinician`×2

- tern.⏎⏎Yours faithfully,⏎⏎C. Short⏎⟦0640873⟧⏎For ROYAL INFIRMARY OF EDINBURGH
- ultant: Kebba Dyer, GMC identifier ⟦0449082⟧
-  Dr Kol Omar, MBBS, GMC identifier ⟦0146399⟧.
- t, Minal Callaghan, GMC identifier ⟦0088838⟧. No operative intervention was req
- rofessional identifier recorded as ⟦0198842⟧. Escalate immediately for worsenin
-  medical registrar, GMC identifier ⟦0498858⟧. Plan to continue IV antibiotics a
- ours faithfully,⏎⏎Titilope Goodman⏎⟦0452192⟧⏎Queen Elizabeth University Hospita
- onsultant physician (GMC reference ⟦0935269⟧). The emergency contact recorded i
- n: Mariana Simpson, GMC identifier ⟦0779694⟧
-  Professional identifier recorded: ⟦0871376⟧. Escalate promptly for fever, sudd

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
- y – Paediatrics⏎⏎Patient: Krithin, ⟦18 m/o⟧⏎Informant: father, A. Cox⏎⏎Reason 
- date: 2004-02-28⏎Clinical context: ⟦4 m/o⟧ infant with acute vomiting, watery

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
-  suspension.⏎⏎The patient works as ⟦Front Desk Receptionist⟧ for Altmar Community College. Thei
- y activities. The patient works as ⟦Plumber⟧ at Nashville Community College.⏎⏎L

## Found but wrong boundaries (partial or inexact)

### Name:Patient: 47

- A&E assessment⏎⏎Patient: ⟦KASIEMOBI JOHN⟧   MRN: 05555873⏎Adult, brought by   →  'KASIEMOBI JOHN   MRN':Name
- t⏎NHS number: 0002312485⏎⏎Patient: ⟦N. Winter⟧    MRN: 05636466⏎Contact: neevan.w  →  'N. Winter    MRN':Name
- NHS number: 000 893 2434⏎⏎Patient: ⟦Durell⟧    MRN: 04251011⏎Referred by Royal  →  'Durell    MRN':Name
- Patient: ⟦Kaide C.⟧   DOB: 6 Feb 1974⏎Nursing progress  →  'Kaide C.   DOB':Name
- Date: 2022-08-31⏎Patient: ⟦Nishvika W.⟧   MRN: 0287244⏎Brought by adult ch  →  'Nishvika W.   MRN':Name
- &E handover – priority 2⏎⏎Patient: ⟦milou blackburn⟧  DOB: 09/08/1973⏎MRN: 0983175⏎Addr  →  'milou blackburn  DOB':Name
- Medicine⏎Date: 30/09/2025⏎Patient: ⟦A. WOODWARD⟧    DOB: 1967-02-09⏎⏎Reviewed this   →  'A. WOODWARD    DOB':Name
- N – A&E handover, 08:15  ⏎Patient: ⟦B. Batchelor⟧   DOB: 04/09/1924  ⏎Address: 178 K  →  'B. Batchelor   DOB':Name
- Patient: ⟦truly day⟧⏎DOB: 18 Sep 1943⏎Contact: 07700 90  →  'truly':Name
- NHS number: 000 448 0504⏎⏎Patient: ⟦D'Andre S.⟧    MRN: 01288602⏎Emergency contact  →  "D'Andre S.    MRN":Name

### Name:Caregiver: 143

- nd discharge advice discussed with ⟦Dr Chahat Cook, MBBS⟧, Emergency Medicine clinician.  →  'with Dr Chahat Cook, MBBS':Name
-  discharge plan were reviewed with ⟦Dr Aureya Oakley, MBBS⟧.⏎⏎Follow-up and safety-netting⏎The  →  'with Dr Aureya Oakley, MBBS':Name
- rink.⏎⏎Reviewed and handed over by ⟦Dr Caileb Slade, MBBS⟧.  →  'by Dr Caileb Slade, MBBS':Name
- wered before discharge.⏎⏎Signed by ⟦Dr Yakoub Ratcliffe, MBBS⟧⏎Accident and emergency, Ealing Hos  →  'by Dr Yakoub Ratcliffe, MBBS':Name
- /2022⏎⏎Validated electronically by ⟦Dr Meriel Noor, MBBS⟧⏎Laboratory medicine consultant⏎Rep  →  'by Dr Meriel Noor, MBBS':Name
- few days.⏎⏎Discharge authorised by ⟦Dr Imogine Rahman, MBBS⟧, consultant physician, on behalf o  →  'by Dr Imogine Rahman, MBBS':Name
- ail.com⏎⏎Validated and reported by ⟦Dr Maani Ryan, MBBS⟧⏎Laboratory clinician⏎Report date:   →  'by Dr Maani Ryan, MBBS':Name
- -04-12.⏎⏎Validated and reported by ⟦Dr Ayeisha Li, MBBS⟧; GMC: 0229740  →  'by Dr Ayeisha Li, MBBS':Name
- 12/1988⏎⏎Validated and reported by ⟦Dr Ottis Wade, MBBS⟧.⏎This report should be interpreted  →  'by Dr Ottis Wade, MBBS':Name
- rioration.⏎⏎Seen and documented by ⟦Dr Nancy-Ann FOLEY, MBBS⟧, clinician.  →  'by Dr Nancy-Ann FOLEY, MBBS':Name

### Name:Other: 38

- rk with Belfast Voluntary Service. ⟦Dunya⟧, the patient’s sister, reports tha  →  'Belfast Voluntary Service. Dunya':Organization
- pital. Emergency contact/relative: ⟦A. Hughes⟧. Patient contact detail: odyn.phil  →  'A. Hughes. Patient contact':Name
- e male patient. Emergency contact: ⟦rejus webb⟧.⏎⏎Current assessment: Breathless o  →  'rejus webb.':Name
- aken.⏎⏎Relative/emergency contact: ⟦jahed wheeler⟧ updated by telephone; understands   →  'jahed wheeler updated':Name
- ain or syncope. Emergency contact: ⟦Priyaa⟧. Patient email: azmi.sullivan92@ou  →  'Priyaa. Patient email':Name
- e symptoms or chest pain reported. ⟦Shri Drew⟧, the patient’s sibling, provided c  →  'Drew':Name
- ion discussed with the patient and ⟦Shri Drew⟧; both confirmed understanding.  →  'Drew':Name
-  with viral croup. Legal guardian: ⟦TAJAUN READ⟧. Contact: alaa.bryant20@fastmail.c  →  'TAJAUN READ. Contact':Name
- ett41@proton.me⏎⏎Collateral: uncle ⟦VIOLET-GRACE FOSTER⟧, present with patient.⏎⏎Presenting  →  'uncle VIOLET-GRACE FOSTER':Name
-   MRN: 01288602⏎Emergency contact: ⟦A. O'Connell⟧    Contact: 07700 900314⏎⏎Presenti  →  "A. O'Connell    Contact":Name

### Address_Location:Patient: 106

- nes. Your recorded home address is ⟦169 Richardson Road, Insch, AB52 6AB⟧, and your contact detail is 07700   →  '169 Richardson Road, Insch, AB':Address_Location
- Patient’s home address recorded as ⟦13 Brewis Terrace, Birchburn, KA27 8AA⟧ for discharge planning.⏎⏎Escalatio  →  '13 Brewis Terrace, Birchburn, KA':Address_Location
- d as 07700 900318 and home address ⟦123 Morrison Lane, Alford, AB33 8AA⟧ before any discharge planning; the  →  '123 Morrison Lane, Alford, AB':Address_Location
- worsening breathlessness. Lives at ⟦166 LLys Illtern, Monmouth / Trefynwy, NP25 3AB⟧.⏎⏎Presenting problem⏎Progressive s  →  'NP25 3AB':Address_Location
- ation: Receptionist. Home address: ⟦119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA⟧. Preferred contact telephone: 0770  →  '119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA. Preferred contact telephone: 07700 900982.':Address_Location
- gby69@outlook.com and home address ⟦78 Glenspean Place, Bellshill, ML4 1AB⟧.⏎⏎Plan for next shift⏎Continue fou  →  '78 Glenspean Place, Bellshill, ML':Address_Location
- act. The patient’s home address is ⟦116 Raith Road, Inverness / Inbhir Nis, IV99 1AA⟧ and preferred email contact is jed  →  '116 Raith Road, Inverness':Address_Location | 'IV99 1AA':Address_Location
- nt: shabaan flanagan⏎Home address: ⟦4 DUNNAMAN PARK, ANNALONG⟧  Contact: 07700 900701⏎Relative pr  →  '4 DUNNAMAN PARK, ANNALONG  Contact: 07700 900701':Address_Location
- 2012. Home correspondence address: ⟦139 CARSONSTOWN ROAD, AGIVEY⟧. The associated result/accession i  →  '139 CARSONSTOWN ROAD, AGIVEY. The associated result/accession identifier is 0029301109.':Address_Location
- ndhu71@talktalk.net. Home address: ⟦133 Northroad, Bury, BL9 0AD⟧.⏎⏎Examination: Alert, distressed b  →  '133 Northroad, Bury, BL9 0AD.':Address_Location

### Address_Location:Caregiver: 123

- lster Hospital⏎Referring locality: ⟦BALLYHORNAN⟧⏎⏎Clinical question⏎Please assess t  →  'BALLYHORNAN\n\nClinical question\nPlease':Address_Location
- GMC-TEST-0340295⏎Service locality: ⟦FINTONA⟧⏎⏎Dear Mental Health Assessment Tea  →  'FINTONA\n\nDear Mental Health':Address_Location
- n: Daryle Hoque⏎Clinical locality: ⟦THE DIAMOND⟧⏎⏎Dear Respiratory Medicine Team,⏎⏎  →  'THE DIAMOND\n\nDear Respiratory':Address_Location
- AI WOODHOUSE, GP⏎Service locality: ⟦Clifton⟧⏎Professional identifier: GMC-TEST-  →  'Clifton\nProfessional identifier':Address_Location
- a Barratt, MBBS⏎Clinical locality: ⟦MONKSTOWN⟧⏎Employer: LAWRENCETOWN Sports Club  →  'MONKSTOWN\nEmployer':Address_Location
- UGHLIN, 0666462⏎Clinical locality: ⟦MAGHERAMASON⟧⏎⏎Dear Colleague,⏎⏎I would be grate  →  'MAGHERAMASON\n\nDear Colleague':Address_Location
- n: rahsaan rigby⏎Service locality: ⟦Croftown⟧⏎Professional identifier: 0680740⏎⏎  →  'Croftown\nProfessional identifier':Address_Location
-  BASHIR, 0948396⏎Service locality: ⟦STEWARTSTOWN⟧⏎⏎Clinical question⏎Please assess f  →  'STEWARTSTOWN\n\nClinical question\nPlease':Address_Location
- AXWELL⏎Referring service locality: ⟦FLURRYBRIDGE⟧⏎⏎Clinical question:⏎Please assess   →  'FLURRYBRIDGE\n\nClinical question':Address_Location
- ing clinician: K. McCabe⏎Locality: ⟦Badnellan⟧⏎Professional identifier: 0339738⏎⏎  →  'Badnellan\nProfessional identifier':Address_Location

### Address_Location:Other: 25

-  contact Jorden Rodgers (locality: ⟦Logie Coldstone⟧) updated during the admission with  →  'Logie Coldstone)':Address_Location
-  care. Emergency contact locality: ⟦Lower Largo⟧.⏎⏎Reason for admission:⏎Wheeze, in  →  'Lower Largo.':Address_Location
- story; emergency contact locality: ⟦Drumligair⟧.⏎⏎Key results⏎Admission blood test  →  'Drumligair.':Address_Location
- Family contact:⏎Spouse’s locality: ⟦Athelstaneford⟧⏎⏎Condition at discharge:⏎Clinicall  →  'Athelstaneford\n\nCondition at discharge':Address_Location
- ent and friend. Friend’s locality: ⟦Borrowstoun⟧.⏎⏎Discharging clinician: Remaya-Ro  →  'Borrowstoun.':Address_Location
-  with partner. Partner’s locality: ⟦Crossfields⟧.⏎⏎Follow-up / actions⏎GP review an  →  'Crossfields.':Address_Location
- pouse; emergency contact locality: ⟦Washington⟧.⏎⏎Discharging clinician: Trelynn C  →  'Washington.':Address_Location
- flat.⏎⏎Emergency contact locality: ⟦Harrison⟧⏎⏎Discharge summary signed by kaisl  →  'Harrison\n\nDischarge summary signed':Address_Location
-  home. Emergency contact locality: ⟦Boonton⟧.⏎⏎Discharge instructions:⏎Increase  →  'Boonton.':Address_Location
- liable⏎Emergency contact locality: ⟦Beachwood⟧⏎⏎Admission reason:⏎The patient, ag  →  'Beachwood\n\nAdmission reason':Address_Location

### Organization:Healthcare: 260

- 10⏎⏎I am referring Abdulrazaq from ⟦Royal Infirmary of Edinburgh⟧ for specialist assessment and advi  →  'Royal Infirmary':Organization
- ⏎Requesting service: Rheumatology, ⟦Skewen Medical Centre⟧⏎Specimen collection/report date: 2  →  'Rheumatology, Skewen Medical Centre':Organization
- tient: niyah-rae houghton⏎Seen at: ⟦Norfolk ICASH - Queen Elizabeth Hospital⟧⏎The patient, aged 86, was reviewed  →  'Queen Elizabeth Hospital':Organization
- ⏎Discharging service: Gynaecology, ⟦Ulster Hospital⟧⏎Report/accession ID: 0815228527⏎⏎R  →  'Gynaecology, Ulster Hospital':Organization
-  faithfully,⏎⏎C. Short⏎0640873⏎For ⟦ROYAL INFIRMARY OF EDINBURGH⟧  →  'For ROYAL INFIRMARY':Organization
- : 27 Jun 2023⏎Responsible service: ⟦Royal Infirmary of Edinburgh⟧⏎⏎Reason for admission⏎Admitted wit  →  'Royal Infirmary':Organization
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
- upation is Pharmacist, employed by ⟦Heathfield Further Education College⟧. They have been advised that a gen  →  'Heathfield Further Education College. They':Organization
- on⏎Patient occupation: employed by ⟦CALEDON Community Centre⟧⏎Emergency contact: REGAN ALEXANDER  →  'employed by CALEDON Community Centre':Profession

### ID:Patient: 86

- ine culture⏎⏎Patient: Sanayah⏎MRN: ⟦019 576 505⟧⏎Home address: 165 Hinchcliffe, Chi  →  '019':ID
-  21 C⏎⏎Patient: Zalayah ROPER⏎MRN: ⟦099 508 763⟧⏎Referring service: Queen Victoria   →  '099':ID
- ted result/accession identifier is ⟦0029301109⟧.⏎⏎Yours faithfully,⏎⏎Tam Hawkes  →  '139 CARSONSTOWN ROAD, AGIVEY. The associated result/accession identifier is 0029301109.':Address_Location
- ry⏎⏎Patient: Sienna-Louise V.⏎MRN: ⟦013 025 563⟧⏎Discharging service: General Medic  →  '013':ID
- port⏎⏎Patient: AMARISSA CURRY⏎MRN: ⟦078 409 289⟧⏎Requesting clinician: GP (name not  →  '078':ID
- ry Report⏎⏎Patient: N. Martin⏎MRN: ⟦037 575 719⟧⏎Specimen: EDTA whole blood⏎Collect  →  '037':ID
-  003 6944⏎⏎Patient: SON WILLS⏎MRN: ⟦077 910 470⟧⏎Address: 9 Shilton Close, Salisbur  →  '077':ID
- ment⏎⏎Patient: jonelle sandhu⏎MRN: ⟦030 359 538⟧⏎Home address: 137 Stryd-y-Capel, L  →  '030':ID
- spital⏎Patient: Denziel Joyce⏎MRN: ⟦033 594 430⟧⏎⏎Dear Colleague,⏎⏎I would be grate  →  '033':ID
-  EMERGENCY⏎⏎Patient: T. Howes⏎MRN: ⟦003 342 835⟧⏎Specimen collected: 4 July 2004⏎Pa  →  '003':ID

### ID:Caregiver: 7

- octor’s professional identifier is ⟦0991053⟧.⏎⏎Next shift: repeat observations   →  'is 0991053':ID
- ician’s professional identifier is ⟦0793020⟧; medical review to be requested pr  →  'is 0793020':ID
- octor’s professional identifier is ⟦0697542⟧.  →  'is 0697542':ID
- tion: Duty doctor reviewed; GMC ID ⟦0314778⟧. Repeat clinical review if unable   →  'GMC ID 0314778':ID
- r: 0001661664⏎⏎From: Jahdel Price, ⟦0355361⟧⏎Organisation: ROYAL INFIRMARY OF E  →  'Jahdel Price, 0355361':Organization
- ver. My professional identifier is ⟦086903137⟧.⏎⏎Thank you for evaluating this pa  →  'is 086903137':ID
- diology Service⏎From: kyper hobus, ⟦009424273⟧⏎Organization: CHENANGO MEMORIAL HO  →  'kyper hobus, 009424273':Organization

### Age_Birthdate: 13

- Patient: Aviva Byrne⏎Clinical age: ⟦7 wk old⟧⏎Parent present: A. COLLIER⏎⏎Reason  →  '7 wk':Age_Birthdate
- ing management.⏎⏎K-Ci is currently ⟦7 wk old⟧, brought by legal guardian A. Hutc  →  '7 wk':Age_Birthdate
- ⏎⏎Patient: Rumaithah⏎Clinical age: ⟦2 wk old⟧⏎Parent present: Iori⏎Referred from  →  '2 wk':Age_Birthdate
- 16⏎⏎Patient: N. Howe⏎Clinical age: ⟦7 wk old⟧ infant⏎Legal guardian: menisha mun  →  '7 wk':Age_Birthdate
- comfort. Patient: Kishaan P., aged ⟦27 years⟧. Home address: 9 Afon Llwyd Terrac  →  '27 year':Age_Birthdate
- ort⏎⏎Patient: Cyriah⏎Clinical age: ⟦2 wk old⟧⏎Legal guardian: Deshae⏎Contact: (2  →  '2 wk':Age_Birthdate
-  Cropp⏎MRN: 09984136⏎Clinical age: ⟦7 wk old⟧⏎History: Jaundice first noted duri  →  '7 wk':Age_Birthdate
-  666 84 3532⏎⏎Patient: M. Billiard⏎⟦2 wk old⟧⏎Home address: 76 Co Rd 4 Kh, Willa  →  '2 wk':Age_Birthdate
- Patient: alynah houg⏎Clinical age: ⟦18 m/o⟧⏎Report/accession ID: 07562786⏎Spec  →  '18':Age_Birthdate
- 32. Callback: (312) 555-0177. DOB: ⟦March 11th, 1979⟧.⏎⏎Background: No known recent trau  →  '376 Centre Ave, Northborough, MA 01532. Callback: (312) 555-0177. DOB: March 11th, 1979.':Address_Location

### Contactdetails: 20

-  0AA. Preferred contact telephone: ⟦07700 900982⟧.⏎⏎On examination, she appeared wel  →  '119 Ffordd Glasgoed, Hendy-Gwyn / Whitland, SA34 0AA. Preferred contact telephone: 07700 900982.':Address_Location
-  DUNNAMAN PARK, ANNALONG  Contact: ⟦07700 900701⟧⏎Relative present: sibling, PRAIRIE  →  '4 DUNNAMAN PARK, ANNALONG  Contact: 07700 900701':Address_Location
-  Scaur, DG5 4AA⏎Preferred contact: ⟦moses.o'donnell30@hotmail.com⟧⏎⏎Admission reason⏎Admitted under G  →  'donnell30@hotmail.com':Contactdetails
- orea, Minffordd, LL48 6AA⏎Contact: ⟦ryanne.o'leary74@gmail.com⟧⏎⏎Reason for review: Persistent dep  →  'leary74@gmail.com':Contactdetails
- , Saundersfoot, SA69 9AB  Contact: ⟦milou.blackburn31@hotmail.com⟧⏎⏎Situation: Acute left flank pain   →  '47 Parc Waen, Saundersfoot, SA69 9AB  Contact: milou.blackburn31@hotmail.com':Address_Location
- nt⏎MRN: 042862061⏎Patient contact: ⟦alexandra.o'connell63@virginmedia.com⟧⏎⏎A&E assessment⏎⏎Presenting compla  →  'connell63@virginmedia.com':Contactdetails
- umnock, KA18 1AA. Patient contact: ⟦alyssia.coles36@sky.com⟧.⏎⏎B: Orthopnoea on lying flat, bil  →  "23 Nun's Walk, Cumnock, KA18 1AA. Patient contact: alyssia.coles36@sky.com.":Address_Location
- 93 B⏎MRN: 0563741⏎Patient contact: ⟦anfa.o'donnell15@virginmedia.com⟧⏎Clinic: Cardiology outpatient revi  →  'donnell15@virginmedia.com':Contactdetails
- Clears, SA33 4AA. Patient contact: ⟦madeeha.o'hara12@gmail.com⟧. Clinical genetics department refe  →  'hara12@gmail.com':Contactdetails
- tardawe, SA8 3AB. Patient contact: ⟦shamen.salmon40@outlook.com⟧.⏎⏎ASSESSMENT⏎Alert, speaking norma  →  '38 Fourteenth Avenue, Pontardawe, SA8 3AB. Patient contact: shamen.salmon40@outlook.com.':Address_Location

## Found but wrong category

### gold Name:Caregiver → predicted Organization: 26

- nt: Fitz Raza⏎MRN: 048449794⏎From: ⟦A. Howe⟧, BELFAST CITY HOSPITAL⏎⏎Dear Clini
- on clinic / general medicine⏎From: ⟦Dr Nana-Ama Gilbert, MBBS⟧, DOLLINGSTOWN⏎Organisation: Royal 
- h headache/light-headedness⏎⏎From: ⟦Dr Chima JOHN, MBBS⟧, General Practitioner, MAYOBRIDGE⏎
- urance number: ZZ 79 25 90 D⏎From: ⟦Dr Amarleen Nixon, MBBS⟧, GP, BELFAST CITY HOSPITAL⏎Referri
- logy⏎NHS number: 0001661664⏎⏎From: ⟦Jahdel Price⟧, 0355361⏎Organisation: ROYAL INFIR
- docrinology  ⏎SSN: 983796065⏎From: ⟦MELENA MCMINIMY⟧, Heron⏎⏎Patient: Arav K.  ⏎DOB: De
- to Pediatric Otolaryngology⏎⏎From: ⟦elbert mattiuz⟧, Clinician, St Mary-Corwin Hospita
- Neurology / Headache Service⏎From: ⟦MAHDI KULCZYCKI⟧, P H S INDIAN HOSPITAL AT BROWNING
- ediatric Dermatology Service⏎From: ⟦kobichimdi hagopian⟧, Community Pediatrics⏎Referring or
- 21⏎To: Endocrinology Service⏎From: ⟦Cayne Pirog, MD⟧, Emergency Department, CHI Oakes H

### gold Address_Location:Caregiver → predicted Organization: 20

- e⏎From: Dr Nana-Ama Gilbert, MBBS, ⟦DOLLINGSTOWN⟧⏎Organisation: Royal Victoria Hospi
-  JOHN, MBBS, General Practitioner, ⟦MAYOBRIDGE⟧⏎Organisation: BELFAST CITY HOSPITA
-  service: Royal Victoria Hospital, ⟦WARINGSFORD⟧
- r⏎From: Altnagelvin Area Hospital, ⟦CAPPAGH⟧⏎Referring clinician: M. NEAL, 0088
- vice⏎⏎From: Belfast City Hospital, ⟦AGIVEY⟧⏎Patient: Efemena Mellor⏎Referring 
- I⏎From: Altnagelvin Area Hospital, ⟦BELLEEK⟧⏎Referring clinician: ellie-jae kay
- ervice: Altnagelvin Area Hospital, ⟦FORKHILL⟧
- : 983796065⏎From: MELENA MCMINIMY, ⟦Heron⟧⏎⏎Patient: Arav K.  ⏎DOB: December 
- TERN REGIONAL MEDICAL CENTER, INC, ⟦Eden⟧⏎⏎Dear Orthopedic Consultant,⏎⏎I am
-  HIRATA, Hunterdon Medical Center, ⟦Gloucester City⟧⏎Professional ID: 073373719⏎⏎Patien

### gold ID:Patient → predicted Contactdetails: 15

- he report/accession identifier was ⟦024700117⟧. Urine dip was unremarkable. Blood
- sion ID for the imaging episode is ⟦026966020⟧.⏎⏎Assessment⏎⏎The history is most 
-  admission report/accession ID was ⟦027918962⟧.⏎⏎ABERDEEN ROYAL INFIRMARY treated
- naemia. The report/accession ID is ⟦0317155794⟧. A short course of oral corticoste
- 0870⏎⏎Patient: KELSIE-MAE GUY⏎MRN: ⟦029 419 048⟧⏎Responsible team: General Medicine
- SITUATION⏎Joy W. (MRN ⟦020 989 045⟧) — ED assessment, acute abdominal 
- e Report⏎⏎Patient: J. Pearson⏎MRN: ⟦021 036 327⟧⏎Clinical context: 9-year-old Middl
- wood⏎NHS number: 000 739 6199⏎MRN: ⟦027 354 832⟧⏎Clinic: Cardiology, Upton Hospital
- MAGUIRE⏎DOB: 22 November 2008⏎MRN: ⟦027 628 943⟧⏎Requesting service: Cardiology⏎Spe
- 5 C⏎⏎Patient: kirandeep welch⏎MRN: ⟦020 278 017⟧⏎The patient, aged 18 months, was r

### gold ID:Caregiver → predicted Contactdetails: 14

-  verified in chart.⏎⏎Documented by ⟦029799272⟧.
- rging clinician: daphne angelozzi, ⟦021933126⟧⏎⏎Torrance Caffie was evaluated in 
-  visit.⏎⏎Signed,⏎daphne angelozzi, ⟦021933126⟧
- released by: Lilliann Muzzall, MD, ⟦029505871⟧⏎Final status: Final report
- eciated.⏎⏎Sincerely,⏎⏎kate fatemi, ⟦020841913⟧⏎Referring clinician⏎Berkeley Medic
- idated/reported by: M. Luczkowski, ⟦022204178⟧
- erring clinician: Kevyn Toppel, ID ⟦027987690⟧⏎⏎Dear Sleep Medicine Clinician,⏎⏎I
- boratory clinician: Holton Deluco, ⟦028489468⟧
- ⏎Discharging clinician identifier: ⟦020014144⟧
- .⏎⏎Validated by: Adalaine Dearmon, ⟦023841891⟧⏎Laboratory medicine.

### gold Contactdetails → predicted Address_Location: 12

-  0AA. Preferred contact telephone: ⟦07700 900982⟧.⏎⏎On examination, she appeared wel
-  DUNNAMAN PARK, ANNALONG  Contact: ⟦07700 900701⟧⏎Relative present: sibling, PRAIRIE
- , Saundersfoot, SA69 9AB  Contact: ⟦milou.blackburn31@hotmail.com⟧⏎⏎Situation: Acute left flank pain 
- umnock, KA18 1AA. Patient contact: ⟦alyssia.coles36@sky.com⟧.⏎⏎B: Orthopnoea on lying flat, bil
- tardawe, SA8 3AB. Patient contact: ⟦shamen.salmon40@outlook.com⟧.⏎⏎ASSESSMENT⏎Alert, speaking norma
- ncader, SA39 9AA  Patient contact: ⟦07700 900005⟧⏎⏎Presented with 5 days of persiste
- th Fwy, Encino, TX 78353. Contact: ⟦farid.fabella92@comcast.net⟧.⏎Disposition: Discharged ambulator
- egon, MI 49441. Preferred contact: ⟦(617) 555-0167⟧.⏎⏎Discharging clinician: damere br
-  Northborough, MA 01532. Callback: ⟦(312) 555-0177⟧. DOB: March 11th, 1979.⏎⏎Backgroun
- Hope, RI 02831. Preferred contact: ⟦roger.ponnusamy64@hotmail.com⟧. Last emesis shortly before arriva

### gold Organization:Healthcare → predicted Name: 8

- ion ID: 031756847  ⏎Care provider: ⟦UNIVERSITY HOSPITAL⟧⏎⏎Presenting problem  ⏎Dysuria, mar
- patient⏎Usual healthcare provider: ⟦ROYAL VICTORIA HOSPITAL⟧⏎Informant: patient and mother, P. 
- ted by DAMEON HARRINGTON⏎Provider: ⟦KINGSMEAD MEDICAL CENTRE⟧
- nnah Lamb (partner)⏎Under care of: ⟦ULSTER HOSPITAL⟧⏎⏎Reason for admission: acute pyelo
- eral medicine⏎Healthcare provider: ⟦ULSTER HOSPITAL⟧⏎⏎Respiratory: Increased SOB overni
- use, Z. Mann.⏎Attending clinician: ⟦The Royal Glamorgan Hospital⟧⏎⏎Arrival: 08:15⏎⏎Presenting compla
- enneff⏎Care setting: Pediatric ED, ⟦Hospital Upr, Dr Federico Trilla⟧⏎⏎Chief complaint: Wheeze, increase
- , or poor response. Follow up with ⟦Hospital Upr, Dr Federico Trilla⟧ primary care.

### gold ID:Patient → predicted Address_Location: 5

- ted result/accession identifier is ⟦0029301109⟧.⏎⏎Yours faithfully,⏎⏎Tam Hawkes
- SIXMILECROSS. Report/accession ID: ⟦043828057⟧.⏎⏎B: Established cardiac condition
- ur, IL 61875. Report/accession ID: ⟦20/890505⟧.
- gs, WY 82224. Report/accession ID: ⟦0415448937⟧.⏎⏎Current assessment: Awake, appro
- in, WV 25617. Report/accession ID: ⟦A26S36217⟧.⏎⏎BACKGROUND: Postoperative incisi

### gold Name:Other → predicted Organization: 2

- rk with Belfast Voluntary Service. ⟦Dunya⟧, the patient’s sister, reports tha
- ks at Belfast Sports Club. Sibling ⟦Kacie-Ann⟧ assists with appointments and repo

### gold ID:Caregiver → predicted Organization: 2

- r: 0001661664⏎⏎From: Jahdel Price, ⟦0355361⟧⏎Organisation: ROYAL INFIRMARY OF E
- diology Service⏎From: kyper hobus, ⟦009424273⟧⏎Organization: CHENANGO MEMORIAL HO

### gold Age_Birthdate → predicted Date: 2

- d. Your date of birth is listed as ⟦October 27th, 1973⟧.⏎⏎You have noticed painless enlarg
-  and light-headedness. Your DOB is ⟦1961-01-09⟧, and your MRN is 032715623. At the

### gold Address_Location:Other → predicted Name: 1

- dress/contact locality for mother: ⟦TEDD⟧⏎Discharging service: Royal Victori

### gold Organization:Other → predicted Profession: 1

- on⏎Patient occupation: employed by ⟦CALEDON Community Centre⟧⏎Emergency contact: REGAN ALEXANDER

### gold Organization:Healthcare → predicted Address_Location: 1

- ultural Equipment Mechanic⏎Seen at ⟦Salem Health West Valley⟧ by beto belsher.⏎⏎Chief concern: I

### gold Age_Birthdate → predicted Address_Location: 1

- 32. Callback: (312) 555-0177. DOB: ⟦March 11th, 1979⟧.⏎⏎Background: No known recent trau

### gold Address_Location:Caregiver → predicted Name: 1

- le through the referring office in ⟦Taylor⟧.⏎⏎Ezz Bossenbroek, MD

## False alarms (prediction overlaps no gold span)

### Organization by rules (repo label ORGANIZATION): 858

- ⟦NHS LABORATORY⟧ MEDICINE REPORT⏎⏎Patient: RUIEN MO
- ⟦NHS LABORATORY⟧ MEDICINE REPORT⏎⏎Patient: ATTA MAR
-  would therefore not exclude gout. ⟦Where diagnostic⟧ uncertainty persists, aspiration o
- 01152638⏎Clinical Microbiology and ⟦Biochemistry Laboratory⟧ Report⏎⏎Patient: Lana-Rae Hamid⏎Re
-  treating clinician’s assessment.⏎⏎⟦Additional laboratory⟧ findings⏎Serum creatinine: 89 µmol
- ⟦NHS Clinical Genetics Laboratory⟧ Report⏎⏎Patient: Miyana Hawkins⏎Ag
- esults were pending at discharge.⏎⏎⟦Treatment and hospital⟧ course⏎⏎Following review by the gy
- ⟦ACCIDENT AND EMERGENCY CLINIC⟧ NOTE⏎⏎Patient: radiance partridge⏎
- ⟦NHS LABORATORY⟧ REPORT⏎NHS number: 0007468530⏎⏎Pat
- Suitable for discharge with urgent ⟦TIA clinic⟧ assessment within 24–48 hours. GP 

### Name by rules (repo label PERSON): 776

- Re: ⟦Hereditary breast⟧ and ovarian cancer risk assessment
- 00 900609.⏎⏎Discharging clinician: ⟦consultant physician⟧⏎Professional identifier: 0019530
- n assessment⏎Requesting clinician: ⟦Not stated⟧⏎Specimen: Serum, venous blood⏎Clin
- RN: 06361696⏎Requesting clinician: ⟦GP⟧ (name not supplied)⏎Healthcare org
- h March 2026⏎Requesting clinician: ⟦not stated⟧⏎⏎Clinical details⏎Acute pyelonephr
-  support.⏎⏎Responsible consultant: ⟦stroke medicine consultant⟧⏎Professional identifier: 0088423
- ct: 07700 900701⏎Relative present: ⟦sibling⟧, PRAIRIE SHEPPARD⏎⏎Assessment⏎Pati
- od and urine⏎Requesting clinician: ⟦Not stated⟧⏎Clinical details: Vomiting and dia
- D: 065675597⏎Requesting clinician: ⟦Not stated⟧⏎Specimen: Venous blood and urine⏎⏎
- confirmed.⏎⏎Discharging clinician: ⟦GMC identifier⟧ 0225290

### Age_Birthdate by rules (repo label AGE): 77

- g orally twice daily to complete a ⟦14-day⟧ course.⏎• Metronidazole 400 mg ora
- g orally twice daily to complete a ⟦14-day⟧ course.⏎• Paracetamol 1 g orally u
- g orally twice daily to complete a ⟦7-day⟧ course in total. Paracetamol 1 g u
- g orally twice daily to complete a ⟦14-day⟧ course.⏎• Metronidazole 400 mg ora
- g orally twice daily to complete a ⟦14-day⟧ course.⏎• Ceftriaxone course compl
- cycline to complete the prescribed ⟦14-day⟧ course.⏎• Metronidazole to complet
- idazole to complete the prescribed ⟦14-day⟧ course; avoid alcohol during treat
- : LAB-00509358⏎⏎Seen in A&E with a ⟦6-day⟧ history of low back pain after lif
- Black female patient attended with ⟦3-day⟧ productive cough, fever and sharp 
- act: 07700 900567⏎⏎Admitted with a ⟦2-day⟧ history of right flank pain, dysur

### ID by rules (repo label ID): 56

- ing; report linked to accession ID ⟦above⟧.⏎⏎Working diagnosis and plan⏎Clini
- or ovarian surgery. They report no ⟦previous⟧ genetic counselling and have not r
- epancy in family history, sample id⟦entity⟧, or the reported familial variant 
- ated laboratory report/accession id⟦entifier⟧ is 0553952501. The initial inflamm
- r other indication for admission id⟦entified⟧.⏎⏎Plan⏎• Continue oral fluids, nut
- fever or dizziness. They report no ⟦recent⟧ change in prescribed medication an
- ntibiotics; the report/accession id⟦entifier⟧ was 024700117. Urine dip was unrem
- t stenosis. The report/accession id⟦entifier⟧ for the imaging episode is 0583993
- ere explained. Advised to report no⟦sebleeds⟧, blood in urine or stool, increasi
- ed to the above report/accession id⟦entifier⟧ for continuity of care. This advic

### Date by rules (repo label DATE): 35

- itic discomfort, pain reduced from ⟦5/10⟧ to 3/10 and respiratory effort set
- s and interpretation undertaken in ⟦2028⟧ using the current laboratory pipel
- sult.⏎⏎Response:⏎Pain reduced from ⟦7/10⟧ to 4/10 following paracetamol. Rig
- n as prescribed, pain reduced from ⟦6/10⟧ to 3/10. Oral amoxicillin administ
- ipheral oedema. Pain improved from ⟦7/10⟧ to 2/10 after sublingual glyceryl 
- ioning provided. Pain reduced from ⟦6/10⟧ to 4/10 after prescribed analgesia
- ith good effect. Pain reduced from ⟦5/10⟧ to 2/10 after medication. Warm flu
- pain, with reported reduction from ⟦6/10⟧ to 3/10 after review. Leg elevated
- eement.⏎⏎Response: Pain eased from ⟦8/10⟧ to 5/10 after morphine, able to re
- after treatment. Pain reduced from ⟦8/10⟧ to 5/10. Tolerated 250 mL oral flu

### Profession by rules (repo label PROFESSION): 18

- ce, Rhosgoch, LL66 0AA⏎Occupation: ⟦Retired⟧⏎History from patient and spouse. A
- nn22@gmail.com⏎Patient occupation: ⟦secondary-school pupil⟧⏎⏎Thank you for attending the paedi
- t: salima kent⏎Patient occupation: ⟦warehouse operative⟧⏎Employer: NEWFERRY Public Library⏎
- t at baseline. Patient occupation: ⟦office administrator⟧.⏎⏎Examination⏎Alert, speaking in f
-  ID: 057742621⏎Patient occupation: ⟦Not documented⟧⏎⏎Dear Specialist,⏎⏎I am referring 
- t: R. Battista⏎Patient occupation: ⟦Not documented⟧⏎Home address: 158 N Hastings Way, 
- l suhm, friend⏎Patient occupation: ⟦Not documented⟧⏎⏎Arrival/Chief complaint:⏎Pruritic
- al age: 65 y/o⏎Patient occupation: ⟦Not documented⟧⏎Relative involved: Sibling⏎⏎Admiss
- atient: Gadiel⏎Patient occupation: ⟦Warehouse associate⟧⏎Employer: Charlotte Amalie Senior 
- t: sujey kumke⏎Patient occupation: ⟦Student⟧⏎History source: Patient and aunt, 

### Contactdetails by rules (repo label PHONE): 11

- GFR: >90 mL/min/1.73 m²⏎Venous pH: ⟦7.37 (7.31⟧–7.41)⏎Bicarbonate: 24 mmol/L (22–2
- GFR: >90 mL/min/1.73 m²⏎Venous pH: ⟦7.38 (7.31⟧–7.41)⏎Bicarbonate: 23 mmol/L (22–2
- GFR: >90 mL/min/1.73 m²⏎Venous pH: ⟦7.37 (7.31⟧–7.41)⏎Bicarbonate: 24 mmol/L (22–2
- c gravity: 1.015 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Protein: Negative⏎Blood: Nega
- c gravity: 1.021 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Leukocyte esterase: Large (ne
- c gravity: 1.018 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Leukocyte esterase: 3+ (negat
- gravity: 1.032 (1.005–1.030) H⏎pH: ⟦5.5 (5.0⟧–8.0)⏎Protein: Trace (Negative)⏎Glu
- c gravity: 1.018 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Protein: 2+ (negative)⏎Blood:
- c gravity: 1.020 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Leukocyte esterase: 3+ (negat
- c gravity: 1.018 (1.005–1.030)⏎pH: ⟦6.0 (5.0⟧–8.0)⏎Leukocyte esterase: 3+ (negat

## Hard negatives redacted

### gestational_age: 4

- r syncope. Current gestational age ⟦9+4 weeks' gestation⟧. Taking doxylamine-pyridoxine with
- eremesis. Current gestational age: ⟦9+4 weeks' gestation⟧. Ongoing emesis with poor oral tol
- n and weight loss⏎Gestational age: ⟦9+4 weeks' gestation⟧⏎⏎Presentation⏎Persistent vomiting 
- eremesis. Current gestational age: ⟦9+4 weeks' gestation⟧.⏎⏎Assessment: Persistent vomiting 

### pain_score: 3

- hen. Your flank pain improved from ⟦5/10⟧ on arrival, and you remained witho
-  hospital. Your pain improved from ⟦5/10⟧ on arrival, and you were able to d
- ved. Pain gradually decreased from ⟦5/10⟧ on admission to a tolerable level 

### caregiver_role: 1

- bany jelliffe⏎Referring clinician: ⟦attending endocrinologist⟧⏎Author: Fidelia Riccomini⏎⏎Reason 

