# Error analysis: `rules-only` on `train_rules_v3`

## Missed gold spans (no overlap with any prediction)

### Name:Patient: 333 missed

shapes: `A. Aa`×127, `Aa A.`×73, `Aa`×39, `Aa Aa`×20, `A A`×19, `A. A`×18, `a a`×16, `Aa-Aa A.`×6
preceded by: `patient:`×188, `patient,`×23, `re:`×15, `—`×9, `situation:`×8, `referring`×7, `handoff—`×7, `of`×5

- A&E assessment⏎⏎Patient: ⟦KASIEMOBI JOHN⟧   MRN: 05555873⏎Adult, brought by 
- ⏎NHS number: 000 731 2882⏎Patient: ⟦A. Fuller⟧⏎MRN: 0439384⏎Contact: ariella-may.
- GP consultation note⏎⏎⟦Kyra-Rose A.⟧ attended the surgery to review blo
- No recent intercurrent infection.⏎⏎⟦Kyra-Rose A.⟧ says that home blood pressure read
- ed to attend A&E.⏎⏎On examination, ⟦Kyra-Rose A.⟧ was comfortable and conversational
- r⏎NHS number: 0009087703⏎⏎Patient: ⟦A. Garrett⟧⏎Seen in A&E with a 36-hour history
- Patient: ⟦Sathvik A.⟧⏎Occupation: Office manager⏎Employe
- h Assessment Team,⏎⏎I am referring ⟦Sathvik A.⟧ for specialist assessment of a maj

### Name:Caregiver: 397 missed

shapes: `A. Aa`×145, `a a`×87, `Aa Aa`×72, `A A`×64, `A. A`×18, `Aa A`×3, `a-a a`×2, `a a'a`×1
preceded by: `sincerely,`×197, `by`×39, `by:`×23, `with`×20, `clinician:`×20, `referrer:`×9, `signed:`×6, `caregiver:`×6

- ecommendations.⏎⏎Yours sincerely,⏎⏎⟦I. MCCANN⟧⏎GP, ROSTREVOR
- n⏎Discussed with medical registrar ⟦E. LACEY⟧. Admit to acute medical unit for o
- ollow-up: 2024-08-18⏎Discharged by ⟦K. Baker⟧.
- view.⏎⏎Validated electronically by ⟦LAREN BAINBRIDGE⟧⏎Laboratory clinician
- n at WALTON HOSPITAL ACUTE BEDS by ⟦L. CURRY⟧⏎⏎ADHEEN SHARIF was reviewed today 
- he plan.⏎⏎Signed electronically by ⟦L. CURRY⟧
- tion and repeat renal blood tests. ⟦jaspreet o'connor⟧, the treating emergency medicine c
- ed to the acute medical team under ⟦M. HANCOCK⟧.

### Name:Other: 600 missed

shapes: `a a`×280, `A. Aa`×98, `Aa`×62, `Aa Aa`×54, `A A`×52, `a-a a`×15, `A. A`×15, `A-A A`×6
preceded by: `spouse,`×33, `friend`×33, `present:`×27, `bedside:`×25, `partner,`×23, `and`×21, `father,`×21, `child,`×19

- ⏎⏎With your consent, your relative ⟦A. Bryant⟧ in Poolewe was informed that you w
- l period not documented at triage. ⟦C. Daniel⟧, her relative, is available by tel
- tial relevance to adult relatives. ⟦Jem Aston⟧, the patient’s adult sibling, is a
- ematology team at ULSTER HOSPITAL. ⟦Cora-Mae Calvert⟧, who lives in Clare, has been upda
- rm discharge support with relative ⟦A. Gregory⟧. Patient’s address recorded as 19 
- inary infection reported. Relative ⟦T. O'LEARY⟧ accompanied the patient and confir
- ot describe excess alcohol intake. ⟦Kady⟧, a close relative, has been helpin
- rs have been assessed and treated. ⟦Sabriin Gordon⟧, from Achfrish, was recorded as he

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
preceded by: `in`×4, `from`×3, `hospital`×2, `gp`×2, `pediatrics,`×2, `healey,`×1, `practitioner`×1, `0015304`×1

- lly,⏎⏎F. Sharpe⏎GP⏎Ulster Hospital⏎⟦ARMOY⟧⏎Professional identifier: 0996112
- erring clinician: ARANDEEP HEALEY, ⟦Tongland⟧⏎Professional ID: 0175972
- ⏎Yours sincerely,⏎⏎Daryle Hoque⏎GP⏎⟦THE DIAMOND⟧
- aiden worrall⏎General Practitioner⏎⟦LOUGHGALL⟧⏎Professional ID: 0435580
- ncerely,⏎⏎Misty Hubbard⏎GP⏎0015304⏎⟦Blackford⟧
- AGE, MBBS⏎Cardiology referral from ⟦Balhalgardy⟧⏎Professional identifier: 0919360
- ferring clinician: Rhianne CURTIS, ⟦BALLYGALLEY⟧⏎Organisation: BELFAST CITY HOSPITA
- l is from Royal Victoria Hospital, ⟦HILLSBOROUGH⟧. Please direct correspondence to t

### Address_Location:Other: 162 missed

shapes: `Aa`×97, `A`×36, `Aa Aa`×21, `A'A A`×2, `Aa a Aa`×2, `Aa a' Aa`×1, `A A`×1, `A A A`×1
preceded by: `in`×47, `from`×42, `locality`×26, `as`×22, `of`×7, `through`×3, `via`×1, `dodds,`×1

- onsent, your relative A. Bryant in ⟦Poolewe⟧ was informed that you were leaving
- ng available through a relative in ⟦Fanagmore⟧.⏎⏎Discharging clinician: Dr Aureya
-  and treated. Sabriin Gordon, from ⟦Achfrish⟧, was recorded as her emergency con
- lative, Melchizedek Rowlands, from ⟦Whitefield⟧, was updated with consent. Dischar
- ill support the patient at home in ⟦ORRITOR⟧.⏎⏎Assessment and investigations⏎On
- d through the locality recorded as ⟦Loch a' Ghainmhich⟧ if needed. Discharge advice was ex
- y and remains available locally in ⟦RANDALSTOWN⟧.⏎⏎Assessment and hospital course⏎O
- l history and can be contacted via ⟦RAFFREY⟧ if required.⏎⏎Investigations⏎Urina

### Organization:Healthcare: 110 missed

shapes: `Aa Aa a Aa`×22, `Aa Aa Aa`×20, `A A A A`×16, `A A A`×13, `Aa Aa Aa Aa`×8, `Aa Aa`×4, `A A`×3, `Aa - Aa Aa a Aa Aa`×3
preceded by: `at`×25, `with`×15, `through`×9, `from`×6, `clinician,`×6, `service:`×4, `by`×4, `to`×4

- 10⏎⏎I am referring Abdulrazaq from ⟦Royal Infirmary of Edinburgh⟧ for specialist assessment and advi
-  with the on-call surgical team at ⟦University Hospital Llandough⟧. They advised outpatient review pr
- : 27 Jun 2023⏎Responsible service: ⟦Royal Infirmary of Edinburgh⟧⏎⏎Reason for admission⏎Admitted wit
- mil RHODES, partner⏎Referred from: ⟦University Hospital of Wales⟧⏎Presenting complaint: Acute right 
- ion ID: 031756847  ⏎Care provider: ⟦UNIVERSITY HOSPITAL⟧⏎⏎Presenting problem  ⏎Dysuria, mar
- e on-call general surgical team at ⟦University Hospital of Wales⟧ for review and likely laparoscopic
- pointment will be arranged through ⟦ROYAL INFIRMARY OF EDINBURGH⟧. If you develop new facial droopin
-  is not evident on the report from ⟦University Hospital Llandough⟧.⏎⏎Clinical impression:⏎Acute pulmo

### Organization:Other: 68 missed

shapes: `Aa Aa Aa`×43, `Aa Aa Aa Aa`×15, `A Aa Aa`×8, `Aa-a Aa Aa`×1, `Aa Aa Aa Aa Aa`×1
preceded by: `with`×17, `at`×16, `through`×9, `affiliation:`×4, `support:`×3, `informed`×1, `symptoms.`×1, `ask`×1

-  MCDONAGH. They have also informed ⟦MAGHABERRY Community Centre⟧ that fatigue may affect attendance
- orrespondence/support affiliation: ⟦Norwood Green Community Centre⟧⏎⏎Presenting complaint⏎Several mont
- ain or new neurological symptoms.⏎⏎⟦Mountjoy Town Council⟧ has been informed that appointment
- nder some work-related pressure at ⟦South Knighton Voluntary Service⟧, with reduced sleep on several nig
- thma.⏎⏎Cora-Leigh works as Chef at ⟦Sheddocksley Secondary School⟧. The history has been provided joi
- ng attendance and participation at ⟦KESH Sports Club⟧. There has been no reported fainti
- pointments in the meantime and ask ⟦Gerlan Sports Club⟧ to support any temporary adjustmen
- is able to work as a Pharmacist at ⟦Aird-dhubh Secondary School⟧, although concentration is reduced

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

### Name:Patient: 6

- Discharge summary⏎⏎Patient: ⟦sahira senior⟧, 66-year-old Black female patient⏎  →  'sahira':Name
- NHS number: 000 003 6944⏎⏎Patient: ⟦SON WILLS⟧⏎MRN: 077 910 470⏎Address: 9 Shilto  →  'WILLS':Name
- Patient: ⟦truly day⟧⏎DOB: 18 Sep 1943⏎Contact: 07700 90  →  'truly':Name
- ccession ID: 027553969⏎⏎I reviewed ⟦I. Dodds⟧ today with their uncle present. Th  →  'Dodds':Name
- g, with no fever.⏎⏎On examination, ⟦I. Dodds⟧ was alert and appropriately intera  →  'Dodds':Name
- Specialty Service:⏎⏎I am referring ⟦A. Coppley⟧ for assessment of essential hypert  →  'Coppley':Name

### Name:Caregiver: 134

- nd discharge advice discussed with ⟦Dr Chahat Cook, MBBS⟧, Emergency Medicine clinician.  →  'with Dr Chahat Cook, MBBS':Name
-  discharge plan were reviewed with ⟦Dr Aureya Oakley, MBBS⟧.⏎⏎Follow-up and safety-netting⏎The  →  'with Dr Aureya Oakley, MBBS':Name
- rink.⏎⏎Reviewed and handed over by ⟦Dr Caileb Slade, MBBS⟧.  →  'by Dr Caileb Slade, MBBS':Name
- wered before discharge.⏎⏎Signed by ⟦Dr Yakoub Ratcliffe, MBBS⟧⏎Accident and emergency, Ealing Hos  →  'by Dr Yakoub Ratcliffe, MBBS':Name
- /2022⏎⏎Validated electronically by ⟦Dr Meriel Noor, MBBS⟧⏎Laboratory medicine consultant⏎Rep  →  'by Dr Meriel Noor, MBBS':Name
- few days.⏎⏎Discharge authorised by ⟦Dr Imogine Rahman, MBBS⟧, consultant physician, on behalf o  →  'by Dr Imogine Rahman, MBBS':Name
- ail.com⏎⏎Validated and reported by ⟦Dr Maani Ryan, MBBS⟧⏎Laboratory clinician⏎Report date:   →  'by Dr Maani Ryan, MBBS':Name
- -04-12.⏎⏎Validated and reported by ⟦Dr Ayeisha Li, MBBS⟧; GMC: 0229740  →  'by Dr Ayeisha Li, MBBS':Name

### Name:Other: 13

- r chest pain develops. Patient and ⟦H. Perkins⟧ updated by telephone at the patien  →  'Perkins':Name
- rk with Belfast Voluntary Service. ⟦Dunya⟧, the patient’s sister, reports tha  →  'Belfast Voluntary Service. Dunya':Organization
- w and confirm operative plan. Aunt ⟦Wanessa⟧ updated and understands current pl  →  'Aunt Wanessa':Name
- e symptoms or chest pain reported. ⟦Shri Drew⟧, the patient’s sibling, provided c  →  'Drew':Name
- ion discussed with the patient and ⟦Shri Drew⟧; both confirmed understanding.  →  'Drew':Name
-  female patient  ⏎Collateral: Aunt ⟦Bahadur GOUGH⟧ present; reports night-time cough   →  'Aunt Bahadur GOUGH':Name
- tient has assented to referral and ⟦E. ELLIOTT⟧ is aware and supportive. Please re  →  'ELLIOTT':Name
- e and reported weight loss. Sister ⟦Iylah⟧ updated by telephone.⏎⏎Observation  →  'Sister Iylah':Name

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

### Organization:Healthcare: 231

- ⏎Requesting service: Rheumatology, ⟦Skewen Medical Centre⟧⏎Specimen collection/report date: 2  →  'Rheumatology, Skewen Medical Centre':Organization
- tient: niyah-rae houghton⏎Seen at: ⟦Norfolk ICASH - Queen Elizabeth Hospital⟧⏎The patient, aged 86, was reviewed  →  'Queen Elizabeth Hospital':Organization
- ⏎Discharging service: Gynaecology, ⟦Ulster Hospital⟧⏎Report/accession ID: 0815228527⏎⏎R  →  'Gynaecology, Ulster Hospital':Organization
- consultant physician, on behalf of ⟦Ulster Hospital⟧.  →  'of Ulster Hospital':Organization
- N SHARIF⏎MRN: MRN-09242879⏎Seen at ⟦WALTON HOSPITAL ACUTE BEDS⟧ by L. CURRY⏎⏎ADHEEN SHARIF was rev  →  'WALTON HOSPITAL':Organization
- de to the physiotherapy service at ⟦WALTON HOSPITAL ACUTE BEDS⟧ for graded exercise, lumbar streng  →  'WALTON HOSPITAL':Organization
- y Pregnancy and Acute Gynaecology, ⟦ROYAL VICTORIA HOSPITAL⟧⏎Report/accession ID: 0779293053⏎⏎R  →  'Early Pregnancy and Acute Gynaecology, ROYAL VICTORIA HOSPITAL':Organization
- g service: Accident and Emergency, ⟦QUEEN ELIZABETH UNIVERSITY HOSPITAL⟧⏎Report/accession ID: 24/630769⏎⏎Yo  →  'Accident and Emergency, QUEEN ELIZABETH UNIVERSITY HOSPITAL':Organization

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

### gold Address_Location:Caregiver → predicted Organization: 19

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

### gold Address_Location:Caregiver → predicted Name: 12

- umber: 0987216⏎Referring clinician⏎⟦BALLYHORNAN⟧
- ns.⏎⏎Yours sincerely,⏎⏎E. MORAN⏎GP⏎⟦Borgue⟧
- ⏎⏎Yours sincerely,⏎⏎E. HOLLOWAY⏎GP⏎⟦Dundonald⟧
- ⏎Yours faithfully,⏎⏎Kam BUCKLEY⏎GP⏎⟦Penston⟧⏎GMC: 0049811
-  BLACKWELL  ⏎Referring clinician  ⏎⟦Brucefield⟧
- o Wallis, MBBS⏎Referring clinician⏎⟦BENDOORAGH⟧
- ⏎⏎Yours faithfully,⏎⏎C. STANLEY⏎GP⏎⟦Greenfoot⟧
- rs sincerely,⏎⏎LUCIE-MAE TANNER⏎GP⏎⟦Killen⟧

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

### gold Organization:Healthcare → predicted Name: 8

-  limited. The case was reviewed by ⟦Aberdeen Royal Infirmary⟧ cardiology services.⏎⏎Discharge me
- ed by mother, Donnach. Reviewed by ⟦Aberdeen Royal Infirmary⟧ medical team.⏎⏎CURRENT CONCERNS: A
- ⏎MELONA CONNOR⏎Referring clinician⏎⟦Royal Infirmary of Edinburgh⟧
- nd bisoprolol therapy. Reviewed by ⟦Royal Infirmary of Edinburgh⟧ team today.⏎⏎O: Alert and orientat
- ifier: 0186151⏎Referring clinician⏎⟦Royal Infirmary of Edinburgh⟧
-  and chest radiograph requested by ⟦Royal Infirmary of Edinburgh⟧; awaiting results. No falls this s
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

### gold Age_Birthdate → predicted Date: 2

- d. Your date of birth is listed as ⟦October 27th, 1973⟧.⏎⏎You have noticed painless enlarg
-  and light-headedness. Your DOB is ⟦1961-01-09⟧, and your MRN is 032715623. At the

### gold ID:Caregiver → predicted Organization: 1

- r: 0001661664⏎⏎From: Jahdel Price, ⟦0355361⟧⏎Organisation: ROYAL INFIRMARY OF E

### gold Organization:Other → predicted Profession: 1

- on⏎Patient occupation: employed by ⟦CALEDON Community Centre⟧⏎Emergency contact: REGAN ALEXANDER

### gold Organization:Healthcare → predicted Address_Location: 1

- ultural Equipment Mechanic⏎Seen at ⟦Salem Health West Valley⟧ by beto belsher.⏎⏎Chief concern: I

### gold Age_Birthdate → predicted Address_Location: 1

- 32. Callback: (312) 555-0177. DOB: ⟦March 11th, 1979⟧.⏎⏎Background: No known recent trau

## False alarms (prediction overlaps no gold span)

### Name by rules (rule/label md_name_subject): 2058

- ue diagnosis and staging.⏎⏎History⏎⟦There⟧ is a six-week history of painless 
- pproximately 6 kg over two months. ⟦There⟧ has been no documented fever, prur
- ve sensation to the affected foot. ⟦Ulcer⟧ remains clean-based with a small a
- fers to lie in a quiet, dark room. ⟦There⟧ is no associated limb weakness, fa
- nd visual fields to confrontation. ⟦There⟧ was no facial asymmetry. Power, to
- l four limbs, and gait was steady. ⟦Fundoscopy⟧ was unremarkable bilaterally. Ther
- copy was unremarkable bilaterally. ⟦There⟧ was no scalp tenderness or neck ri
- l managing basic daily activities. ⟦There⟧ is no history of panic-related col

### Name by model (rule/label repeat): 204

- istent with migraine without aura. ⟦There⟧ are no current red-flag features o
- ing sleep disturbance and tension. ⟦There⟧ have been no troublesome adverse e
- d within approximately 30 seconds. ⟦There⟧ were no focal neurological finding
- e times daily, taken before meals. ⟦There⟧ have been no recent medication cha
- bility, without suicidal thoughts. ⟦There⟧ are no reported hallucinations, ma
- ng and exposure to household dust. ⟦There⟧ have been no emergency department 
- sistant⏎Ciprofloxacin: Susceptible⏎⟦Nitrofurantoin⟧: Susceptible for lower urinary tra
- ng until the course is complete.⏎• ⟦Paracetamol⟧ when required for pain, according 

### Name by rules (rule/label md_name_by): 35

- eral areas of life, accompanied by ⟦muscle tension⟧, irritability and poor sleep. They
- te the spray, or is accompanied by ⟦breathlessness⟧, collapse or sweating, call 999 an
- mic rearrangements are assessed by ⟦read-depth analysis⟧. This is a germline test and canno
- ith exertion, or is accompanied by ⟦fainting⟧, marked breathlessness, sweating, 
- tions have not been accompanied by ⟦collapse⟧. There is no clinical history to s
- ined; no new ST change reported by ⟦telemetry⟧. IV access patent. Aspirin, fondap
- auren-Rose   13 y/o⏎Accompanied by ⟦uncle⟧, Coragh⏎⏎Clinical question⏎Please 
- inical age: 14 y/o⏎Accompanied by: ⟦aunt⟧, K. BUCKLEY⏎⏎Dear Community Paedia

### Name by rules (rule/label md_name_header): 26

- e agreed plan.⏎⏎Emergency contact: ⟦relative’s⟧ details held in the hospital recor
- Warren⏎0586044⏎Referring clinician⏎⟦Accident⟧ and emergency department
- er – clinical genetics⏎⏎Situation: ⟦Post-operative⟧ wound infection under review. Incr
- th University Hospital⏎⏎Situation: ⟦Adolescent⟧ admitted with acute asthma exacerb
- esteg General Hospital⏎⏎Situation: ⟦Increasing⟧ pain around the operative wound wi
- ard handover – NSTEMI.⏎⏎Situation: ⟦Central⟧ chest pressure earlier with diapho
- lockwood41@outlook.com⏎⏎Situation: ⟦Postoperative⟧ wound with increasing erythema, pu
- SITUATION⏎⟦National Insurance⟧ number: NK656548B⏎A&E respiratory 

### Organization by rules (rule/label md_org_header): 24

- MRN: 080212442⏎Requesting service: ⟦Rheumatology / general medicine⟧⏎Reporting organisation: HOLYWELL C
-  blood in EDTA⏎Requesting service: ⟦Cardiology (ordering clinician unnamed)⟧⏎Clinical indication: Significant f
- ient: T. Leonen⏎Admitting service: ⟦Internal Medicine⟧⏎Discharging service: Hospital Medi
- ⏎MRN: 083108776⏎Admitting service: ⟦Internal Medicine⟧⏎Discharging service: Internal Medi
- rnal Medicine⏎Discharging service: ⟦Internal Medicine⟧⏎⏎yetzel eufemia was admitted for t
- la⏎MRN: 0998403⏎Admitting service: ⟦Internal Medicine⟧⏎Discharging organization: Communit
- a⏎MRN: 02805908⏎Admitting service: ⟦Internal Medicine⟧⏎Discharging organization: Turning 
- ⏎MRN: 030517193⏎Admitting service: ⟦Internal Medicine⟧⏎Discharging organization: DEACONES

### Organization by rules (rule/label md_org_suffix): 13

- available locally in RANDALSTOWN.⏎⏎⟦Assessment and hospital⟧ course⏎On arrival the patient was 
-  by mild to moderate dehydration.⏎⏎⟦Assessment and hospital⟧ course⏎⏎On arrival the patient was
- the respiratory medicine service.⏎⏎⟦Investigations and hospital⟧ course⏎⏎Urine pregnancy testing wa
- ol and no recent travel reported.⏎⏎⟦Assessment and hospital⟧ course⏎On arrival clinically dehyd
- er and assisted with the history.⏎⏎⟦Assessment and hospital⟧ course⏎⏎On arrival she appeared cl
- ntact and is based in PORTAFERRY.⏎⏎⟦Investigations and hospital⟧ course⏎Observations remained stabl
- he accompanying operative record.⏎⏎⟦Assessment and hospital⟧ course⏎Reviewed by the emergency s
- or a high temperature with rigors. ⟦Contact the hospital⟧ team promptly if the night sweats 

### Name by rules (rule/label md_name_referring): 10

-  Parkinson disease. I am referring ⟦them⟧ for a specialist review of increas
- Dear ⟦Parkinson’s Disease⟧ and Movement Disorders Team,⏎NHS n
- . Bainbridge⏎Weight: 28.6 kg⏎⏎Dear ⟦Dermatology Colleagues⟧,⏎⏎I would be grateful for your ass
- KILLOUGH Housing Association⏎⏎Dear ⟦Colleagues⟧,⏎⏎I am referring Qiao Charlton for
- : Anelis Lake⏎MRN: 027400387⏎⏎Dear ⟦Spinal⟧ or Musculoskeletal Service,⏎⏎I am 
- ce-daily blood pressure record for ⟦one⟧ week and to bring this, together w
- he original family test report for ⟦comparison⟧ and review with the patient’s gene
- 18502432⏎⏎Patient: Kyzier M.⏎⏎Dear ⟦Podiatry⟧ and Wound Care Team,⏎⏎I am referri

### Name by rules (rule/label md_name_header_inline): 10

- rtaken with consent and chaperone: ⟦mucopurulent⟧ discharge at cervical os, marked c
- nation with consent and chaperone: ⟦mucopurulent cervical⟧ discharge, cervical motion tendern
- nation with consent and chaperone: ⟦mucopurulent⟧ discharge, cervical motion tendern
- aid advice reinforced with father: ⟦place⟧ on side, protect from injury, do n
- 96-07-11.⏎⏎Advice given to mother: ⟦seek urgent⟧ assessment via NHS 111/A&E if unab
- ses. Blood tests requested via GP: ⟦FBC⟧, U&E, LFT, CRP and urate after fla
- nation with consent and chaperone: ⟦mucopurulent cervical⟧ discharge and cervical motion tend
- d. Reviewed with senior clinician: ⟦clinically stable⟧ for ambulatory treatment, no oxyge

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

### Date by rules (rule/label year_ctx): 1

- s and interpretation undertaken in ⟦2028⟧ using the current laboratory pipel

### Address_Location by rules (rule/label md_place_signoff): 1

- TAR GEORGETOWN UNIVERSITY HOSPITAL⏎⟦Partner⟧, Kyria, included in discharge disc

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

