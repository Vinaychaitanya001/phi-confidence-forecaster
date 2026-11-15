# Annotated `test` notes (examples)

Legend: `[text | Category conf%]` is a predicted span with the forecaster's probability that it is PHI; `⚠ verdict` marks a span that is a false alarm, has the wrong category or off boundaries; `{{text | MISSED label}}` is gold PHI the detector did not predict. Synthetic notes (MedDeID, CC BY 4.0). Every note is in `test_v5.jsonl`.

## en-gb-synthetic-02061 (en-GB, emergency_note)

Note leak risk 1.000, expected misses 1.99; 5 spans predicted, 3 gold spans missed.

```text
SITUATION
A&E assessment, [27 March 2026 | Date 100%]. {{D. Young | MISSED Name:Patient}}, accompanied by adult child, with 18-hour history of central abdominal pain migrating to the right lower quadrant. Nausea and loss of appetite; no diarrhoea. Pain worse on movement.

BACKGROUND
Usual GP record reviewed. No previous abdominal surgery reported. Paracetamol taken at home with limited effect. No known drug allergy documented.

ASSESSMENT
Alert, uncomfortable but haemodynamically stable. BP 120/80 mmHg, pulse 96, temperature 37.8°C, SpO₂ 98% on air. Abdomen soft, focal RIF tenderness with guarding and positive percussion tenderness; no palpable mass. Chest clear, heart sounds normal.

Bloods: neutrophilia and raised CRP; renal function acceptable. Urinalysis negative for blood and nitrites. Pregnancy testing not clinically indicated. CT abdomen/pelvis: inflamed appendix with periappendiceal inflammatory change, no collection or perforation.

ACTION / PRIORITIES
Cannula inserted. IV fluids commenced, analgesia with paracetamol. Intravenous co-amoxiclav given following surgical discussion. Nil by mouth pending theatre review. General surgery referral accepted by [Epsom General Hospital | Organization 100%].

PLAN
Admit under surgery for laparoscopic appendicectomy assessment. Escalate for increasing pain, sepsis or haemodynamic change. Handover completed to {{A. Nicholson | MISSED Name:Caregiver}}, clinician at [Epsom General Hospital | Organization 100%]. Patient and adult child updated; questions answered. Contact details confirmed in EHR. Documented at [27 March 2026 | Date 100%] for [47 | Age_Birthdate 100% ⚠ boundary off] y/o.
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| '47' | Age_Birthdate | 1.00 / 1.00 / 0.87 | boundary off |

Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): 'D. Young' p=0.99 (real miss); 'A. Nicholson' p=0.99 (real miss)

## en-us-synthetic-01542 (en-US, nursing_note)

Note leak risk 1.000, expected misses 1.99; 5 spans predicted, 2 gold spans missed.

```text
Nursing Handover – Clinical Genetics
SSN: [666922287 | ID 100%]

Situation: [Emelie | Name 100%] with diabetic plantar foot ulcer, decreased protective sensation, and scant local drainage. Afebrile this shift; reports tenderness only with dressing removal.

Background: Followed by [Ochsner Stennis Memorial Hospital | Organization 100%]. Receiving amoxicillin-clavulanate and ordered wound care. Home address on file: [770 State Hwy 510, Summit, MS 39666 | Address_Location 100%]. Patient contact: [emelie.cobe69@gmail.com | Contactdetails 100%]. Adult child {{A. Manga | MISSED Name:Other}} involved in updates per patient request.

Assessment:
- 08:15 dressing found damp with serous drainage; no foul odor.
- Periwound skin mildly erythematous, margins intact. Pedal pulse palpable; foot warm.
- Ambulates short distances with off-loading shoe and standby assist. Reminded to avoid barefoot walking and prolonged weight-bearing.
- Intake adequate. No nausea reported.

Actions: Cleansed ulcer with normal saline, dried surrounding skin, applied ordered dressing, and reinforced off-loading precautions. Reviewed daily foot inspection and to report spreading redness, fever, increased drainage, or new pain. Tolerated care well; drainage decreased on reassessment.

Escalation/risk: Monitor closely for cellulitis, worsening infection, and falls related to sensory loss. Notify covering provider for fever, streaking, purulence, increasing erythema, neurovascular change, or inability to bear weight.

Next shift: Reassess wound and neurovascular status, document drainage/odor, administer antibiotic as scheduled, maintain fall precautions, and confirm follow-up plan with patient and {{A. Manga | MISSED Name:Other}}.
```

Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): 'A. Manga' p=0.99 (real miss); 'A. Manga' p=1.00 (real miss)

## en-us-synthetic-00202 (en-US, referral_letter)

Note leak risk 1.000, expected misses 1.99; 7 spans predicted, 2 gold spans missed.

```text
Vascular and Wound Care Consultation Referral

Patient: [Damazi S. | Name 100%]
Referring clinician: [evelene prade | Name 100%], {{034481817 | MISSED ID:Caregiver}}
Referring service locality: [Genoa | Address_Location 100%]

Dear Wound Care and Limb Preservation Team,

I am referring [Damazi S. | Name 100%] for evaluation and management of a diabetic foot ulcer, with particular concern for a neuropathic plantar wound with persistent local discharge. Please assess depth, infection severity, perfusion, and risk for progression, and advise whether advanced wound therapy, vascular testing, or surgical consultation is indicated.

The ulcer is located beneath the forefoot on the plantar surface and has been present despite regular outpatient wound care. The patient reports minimal pain but describes reduced sensation in both feet. Examination in the office showed a full-thickness plantar ulcer with a moist wound bed and scant serous-to-cloudy discharge. The surrounding skin was mildly macerated without crepitus or rapidly spreading erythema. There was no visible exposed bone or tendon. Dorsalis pedis and posterior tibial pulses were difficult to appreciate bilaterally; the feet were warm, although capillary refill appeared mildly delayed. Monofilament sensation was reduced at multiple plantar sites.

The patient has been receiving cleansing, nonadherent dressing changes, and off-loading counseling. Adherence to off-loading has been inconsistent because of difficulty avoiding weight-bearing during routine activities. Current treatment includes wound care and amoxicillin-clavulanate. The antibiotic was started for concern about localized wound infection after the appearance of increased drainage. There have been no reported fevers, rigors, vomiting, or acute change in mental status. The patient denies calf pain. Please reassess the need for continued antimicrobial therapy after examination and, if appropriate, obtain a deep tissue specimen rather than a superficial swab.

Recent diabetes monitoring remains suboptimal, with HbA1c 8.7%. I recommend coordination with primary care or endocrinology to improve glycemic control while the ulcer is healing. Plain radiographs of the foot would be reasonable if there is clinical concern for retained foreign material or osteomyelitis; advanced imaging should be guided by your examination and radiographic findings. An ankle-brachial index with toe pressures or another vascular assessment would also be helpful given the diminished pedal pulses.

The patient’s adult child, [zakira | Other 100% ⚠ wrong category] [aipperspach | Name 100% ⚠ boundary off], is aware of the referral and may assist with dressing changes and transportation. Until seen, the patient has been instructed to minimize weight-bearing on the affected foot, avoid soaking or walking barefoot, inspect both feet daily, and seek emergency evaluation for fever, rapidly increasing redness or swelling, foul drainage, black discoloration, or systemic illness.

Please provide recommendations regarding debridement, off-loading equipment, dressing selection, vascular workup, and follow-up interval. Thank you for evaluating this patient.

Sincerely,

[evelene prade | Name 100%]
Referring clinician
{{034481817 | MISSED ID:Caregiver}}
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'zakira' | Other | 1.00 / 0.01 / 0.00 | wrong category |
| 'aipperspach' | Name | 1.00 / 0.98 / 0.00 | boundary off |

Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): '034481817' p=0.99 (real miss); '034481817' p=0.99 (real miss)

## en-us-synthetic-00393 (en-US, emergency_note)

Note leak risk 1.000, expected misses 1.96; 5 spans predicted, 1 gold spans missed.

```text
Emergency Department Assessment

Patient: [miha bestard | Name 100%]
Report/accession ID: [038947802 | ID 100%]
Seen for 4 days of worsening dyspnea, orthopnea, bilateral ankle swelling, and reduced exercise tolerance. Spouse [Aidric | Name 100%] reports a 6-lb increase on home scale and increased need for pillows. No chest pain, fever, unilateral leg pain, or missed doses of furosemide or metoprolol succinate.

Vitals: BP 168/94, HR 96, RR 24, SpO2 91% room air, T 98.2°F.
Exam: Mild respiratory distress; bibasilar crackles to mid-lung fields. JVP elevated. Regular rhythm, no murmur. 2+ pitting edema to both shins. Calves nontender. Alert, speaking in short sentences.

Workup: ECG sinus rhythm with left bundle branch block, no acute ST elevation. Chest radiograph shows cardiomegaly, pulmonary vascular congestion, and small bilateral pleural effusions. Labs: WBC 8.7 K/uL, Hgb 12.9 g/dL, creatinine 1.4 mg/dL, potassium 4.2 mmol/L, high-sensitivity troponin 28 ng/L with repeat 27 ng/L. BNP 2,840 pg/mL. Viral respiratory panel negative.

Assessment: Acute on chronic decompensated heart failure with hypoxemia; no evidence of acute coronary syndrome or pneumonia. Discussed findings with cardiology at {{Hospital Menonita Humacao, Inc | MISSED Organization:Healthcare}}.

Treatment: Oxygen 2 L/min nasal cannula; furosemide 80 mg IV with 900 mL urine output in ED and improved work of breathing. Admission recommended for continued diuresis, telemetry, and medication optimization. Patient agrees. Accepted to telemetry; stable at handoff.

Follow-up: Cardiology review scheduled for [2022-06-02 | Date 100%].
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'Menonita Humacao' | Address_Location | 1.00 / 0.61 / 0.02 | wrong category |

Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): 'Hospital' p=0.97 (real miss); ', Inc' p=0.99 (real miss)

## en-gb-synthetic-03309 (en-GB, emergency_note)

Note leak risk 0.009, expected misses 0.01; 11 spans predicted, 2 gold spans missed.

```text
S: [dua-fatima | Other 100% ⚠ wrong category] [nunn | Name 100% ⚠ boundary off], DOB [4th December 1937 | Age_Birthdate 100%], assessed in A&E at [University Hospital Bristol | Organization 100% ⚠ boundary off] and [Weston | Address_Location 100% ⚠ wrong category] [Virtual Site | Organization 95% ⚠ boundary off] on [2026-10-26 | Date 100%]. Partner reports sudden spinning episodes when turning in bed or looking upwards, each lasting under a minute, with nausea and unsteadiness. No headache, hearing loss, chest pain or collapse.

B: Previous similar brief episodes; medication: prochlorperazine as required. No recent head injury reported.

A: Observations stable. Alert, communicating normally. Cranial nerves grossly intact, normal limb power and coordination. Gait mildly unsteady initially. No spontaneous nystagmus. Right Dix–Hallpike reproduces vertigo with fatigable torsional nystagmus. Capillary glucose normal. ECG sinus rhythm. Presentation consistent with benign paroxysmal positional vertigo; no features currently suggesting posterior circulation event.

Actions: Prochlorperazine given for nausea. Epley manoeuvre performed with improvement; mobilised safely afterwards. Encourage oral fluids and slow positional changes. Partner present and understands advice.

P: Suitable for discharge from general medicine/A&E. Continue prochlorperazine as required, avoid driving or hazardous activity until settled, and arrange GP review if persistent or recurrent. Return urgently for continuous vertigo, new diplopia, dysarthria, limb weakness, severe headache, inability to walk or repeated vomiting.

Handover completed 08:15 by [NORRIE SCOTT | Name 100%], [University Hospital Bristol | Organization 100% ⚠ boundary off] and [Weston | Address_Location 100% ⚠ wrong category] [Virtual Site | Organization 96% ⚠ boundary off].
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'dua-fatima' | Other | 1.00 / 0.00 / 0.00 | wrong category |
| 'nunn' | Name | 1.00 / 0.99 / 0.00 | boundary off |
| 'University Hospital Bristol' | Organization | 1.00 / 1.00 / 0.86 | boundary off |
| 'Weston' | Address_Location | 1.00 / 0.26 / 0.01 | wrong category |
| 'Virtual Site' | Organization | 0.95 / 0.90 / 0.01 | boundary off |
| 'University Hospital Bristol' | Organization | 1.00 / 1.00 / 0.75 | boundary off |
| 'Weston' | Address_Location | 1.00 / 0.26 / 0.01 | wrong category |
| 'Virtual Site' | Organization | 0.96 / 0.87 / 0.00 | boundary off |

## en-gb-synthetic-02929 (en-GB, clinic_note)

Note leak risk 0.975, expected misses 1.42; 9 spans predicted, 2 gold spans missed.

```text
General Medicine Specialist Clinic Report

Patient: [H. Baxter | Name 100%]
Occupation: [Journalist | Profession 100%]
Report/accession ID: [L20D35559 | ID 100%]
Referring service: [Chelsea & Westminster NHS | Organization 100% ⚠ boundary off] Fdn Trust - [Weymouth Street Hospital | Organization 100% ⚠ boundary off]

Clinical findings:
The patient reports a gradually enlarging, painless swelling in the left side of the neck, with further nodal enlargement noted over recent weeks. Associated drenching night sweats and unintentional weight loss. No infective symptoms reported. Eating and drinking adequately, although energy levels are reduced.

Examination demonstrates firm, non-tender cervical lymphadenopathy, with palpable supraclavicular nodes. No overlying skin change. Chest is clear to auscultation; heart sounds normal. Abdomen soft, with no definite hepatosplenomegaly on examination. Performance status remains good.

Investigations reviewed:
Cross-sectional imaging demonstrates extensive cervical and mediastinal lymphadenopathy, radiologically concerning for lymphoma. Blood tests show inflammatory marker elevation; full blood count does not demonstrate significant cytopenia. An image-guided core biopsy has been arranged, with histopathological classification awaited.

Impression:
Clinical and radiological picture is consistent with Hodgkin lymphoma. Tissue diagnosis remains required before definitive staging and treatment selection. The constitutional symptoms are concerning for active disease.

Plan:
Supportive care pending tissue diagnosis, including oral fluids, nutritional support and simple analgesia if required. Avoid corticosteroids unless clinically indicated, as these may affect biopsy interpretation. Expedite biopsy reporting and arrange PET-CT and echocardiography once histology is available. The patient has been advised to seek urgent assessment for rapidly increasing swelling, breathlessness, dysphagia or fever.

Report authored by [vedh | Other 100% ⚠ wrong category] [lea | Name 100% ⚠ boundary off]
General Medicine
[Chelsea & Westminster NHS Fdn | Organization 100% ⚠ boundary off] Trust - [Weymouth Street Hospital | Organization 100% ⚠ boundary off]
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'Chelsea & Westminster NHS' | Organization | 1.00 / 0.96 / 0.46 | boundary off |
| 'Weymouth Street Hospital' | Organization | 1.00 / 1.00 / 0.97 | boundary off |
| 'vedh' | Other | 1.00 / 0.00 / 0.00 | wrong category |
| 'lea' | Name | 1.00 / 0.94 / 0.00 | boundary off |
| 'Chelsea & Westminster NHS Fdn' | Organization | 1.00 / 0.95 / 0.26 | boundary off |
| 'Weymouth Street Hospital' | Organization | 1.00 / 1.00 / 0.92 | boundary off |

Possible misses (the pipeline adds those with p ≥ 0.5 as PHI and flags p ≥ 0.2 for review): 'Fdn Trust' p=0.95 (real miss); 'Trust' p=0.47 (real miss)

## en-gb-synthetic-00363 (en-GB, emergency_note)

Note leak risk 0.000, expected misses 0.00; 8 spans predicted, 0 gold spans missed.

```text
Presenting complaint
[Maho C. | Name 100%] attended the emergency department with 5 days of worsening breathlessness, now requiring three pillows at night. Reports bilateral ankle swelling and markedly reduced exercise tolerance. No chest pain, palpitations, fever or productive cough. Adult child, [cristina | Other 100% ⚠ wrong category] [molloy | Name 100% ⚠ boundary off], accompanied the patient and reports a 2 kg increase on home scales over the past week. Known heart failure; taking furosemide and bisoprolol, with no missed doses reported.

Assessment
Alert and speaking in short sentences. Glasgow Coma Scale 15. Respiratory rate 26/min, oxygen saturations 91% on air, pulse 96 bpm regular, BP 148/88 mmHg, temperature 36.7°C. Raised JVP, bilateral fine basal crackles and pitting oedema to the shins. Heart sounds dual without murmur. Abdomen soft and non-tender. No focal neurological deficit.

Investigations
ECG: sinus rhythm with no acute ischaemic change. Chest radiograph demonstrates pulmonary vascular congestion and small bilateral pleural effusions. Blood tests show raised NT-proBNP and mildly impaired renal function; potassium within reference range. High-sensitivity troponin not significantly changing on repeat sample. Viral respiratory screen negative.

Clinical impression and treatment
Findings are consistent with acute decompensated heart failure, without evidence of acute coronary syndrome or infection. Given oxygen by nasal cannula and intravenous furosemide, with 1.1 L urine output during observation and improved work of breathing. Fluid balance and renal profile to be monitored.

Disposition
Discussed with the medical registrar at [Cardiff Royal Infirmary | Organization 100%]. Admit to the acute medical unit for ongoing diuresis, daily weights and medication review. Cardiology follow-up arranged for [2025-01-29 | Date 100%]. Safety-net advice given to [cristina | Other 100% ⚠ wrong category] [molloy | Name 100% ⚠ boundary off]. 

Documented by [HARRY-JOHN DAVIS | Name 100%], emergency clinician.
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'cristina' | Other | 1.00 / 0.00 / 0.00 | wrong category |
| 'molloy' | Name | 1.00 / 1.00 / 0.00 | boundary off |
| 'cristina' | Other | 1.00 / 0.00 / 0.00 | wrong category |
| 'molloy' | Name | 1.00 / 0.91 / 0.01 | boundary off |

## en-gb-synthetic-01628 (en-GB, discharge_summary)

Note leak risk 0.000, expected misses 0.00; 11 spans predicted, 0 gold spans missed.

```text
Discharge summary – Paediatrics
NHS number: [000 053 3983 | ID 100%]

Patient: [musfirah dutton | Name 100%]
MRN: [0997142 | ID 100%]
Legal guardian: [adeleine hull | Name 100%]
Admitting service: [Ulster Hospital | Organization 100%]

Reason for admission
Brought to the emergency department following a first generalised convulsion in the context of fever. The episode lasted approximately two minutes, with bilateral stiffening and rhythmic jerking, followed by drowsiness. [adeleine | Other 100% ⚠ wrong category] [hull | Name 92% ⚠ boundary off] witnessed the event and reported fever for 3 days with reduced appetite, but no preceding head injury or known ingestion.

At presentation, [3 y/o | Age_Birthdate 69%] was febrile but cardiovascularly stable. Initial examination showed postictal drowsiness, improving during observation; no meningism, focal neurological deficit or respiratory distress. Capillary glucose was normal. No further seizure activity occurred.

Investigations and course
Blood tests were not felt necessary after senior paediatric review. Urinalysis was unremarkable. The child remained clinically well hydrated and returned to usual interaction and oral intake later that day. Fever settled with fluids, light clothing and paracetamol for comfort. No antibiotics or anticonvulsant treatment required. The presentation was considered consistent with a simple febrile seizure associated with a self-limiting viral illness. There were no features suggesting meningitis or a complex seizure.

Problem list
• First simple febrile seizure
• Acute febrile viral illness
• Recovered postictal drowsiness

Discharge condition and plan
Discharged home with [adeleine | Other 97% ⚠ wrong category] [hull | Name 100% ⚠ boundary off] after paediatric assessment. No regular discharge medicines. Continue antipyretic comfort measures if distressed or uncomfortable; avoid alternating preparations unless advised by the GP.

Seizure first-aid advice given: place on the side, protect from injury, do not restrain and do not put anything in the mouth. Call 999 if the seizure lasts five minutes or more, breathing is affected, recovery is not as expected, or another seizure occurs without recovery. GP review if fever persists or concerns arise. No routine paediatric follow-up arranged; referral to [Ulster Hospital | Organization 100%] if recurrent, prolonged or atypical events.
```

| span | category | conf PHI / category / exact | verdict |
|---|---|---|---|
| 'adeleine' | Other | 1.00 / 0.00 / 0.00 | wrong category |
| 'hull' | Name | 0.92 / 0.95 / 0.00 | boundary off |
| '3 y/o' | Age_Birthdate | 0.69 / 0.93 / 0.98 | correct |
| 'adeleine' | Other | 0.97 / 0.00 / 0.00 | wrong category |
| 'hull' | Name | 1.00 / 0.99 / 0.40 | boundary off |

## en-gb-synthetic-00033 (en-GB, emergency_note)

Note leak risk 0.000, expected misses 0.00; 6 spans predicted, 0 gold spans missed.

```text
Emergency Department Assessment
NHS number: [000 271 4834 | ID 100%]

Patient: [Ismaaeel MCGRATH | Name 100%]
DOB: [5 Apr 1934 | Age_Birthdate 100%]
Address: [129 Wychbury Close, Middlewich, CW10 0AA | Address_Location 100%]
Contact: [07700 900006 | Contactdetails 100%]

Presenting complaint
Three-day history of markedly reduced urine output with increasing tiredness and poor oral intake. Reports drinking very little because of nausea, without vomiting or diarrhoea. No dysuria, visible haematuria, flank pain, chest pain or breathlessness. No recent contrast exposure. Has taken usual medicines but has been eating and drinking poorly.

Background and medicines
Known hypertension and osteoarthritis. No documented chronic kidney disease in the available GP summary. Regular medicines reviewed; nephrotoxic and blood-pressure-lowering medicines to be withheld temporarily while renal function and hydration are reassessed. No known drug allergies recorded.

Examination
Alert and appropriately responsive, speaking in full sentences. Temperature 36.4°C, pulse 96 bpm regular, blood pressure 102/64 mmHg, respiratory rate 18/min, oxygen saturations 98% on air. Dry tongue and mildly reduced skin turgor. Heart sounds normal, chest clear bilaterally. Abdomen soft and non-tender, with no palpable bladder and no renal angle tenderness. No peripheral oedema. Urine passed only a small amount since arrival.

Investigations
Blood tests show urea 18.2 mmol/L, creatinine 186 µmol/L, estimated GFR reduced from the previous documented result, with mild hyperkalaemia at 5.5 mmol/L. Sodium 136 mmol/L, bicarbonate 21 mmol/L, venous lactate 1.4 mmol/L. Full blood count without significant anaemia or leukocytosis. Urinalysis: concentrated urine, trace protein, no blood or nitrites. ECG shows sinus rhythm with no acute T-wave or QRS changes.

Management and decision-making
Clinical picture is most consistent with acute kidney injury, probably related to volume depletion and poor intake. A 500 mL bolus of intravenous sodium chloride was given, followed by slower replacement with close monitoring because of the reduced renal function. Repeat observations remained stable. Bladder scan showed 74 mL after voiding; renal tract ultrasound requested to exclude obstruction.

The case was reviewed with the on-call medical registrar, who advised admission for continued intravenous fluids, strict fluid balance, repeat U&E and review of withheld medicines. The patient understands the rationale and agrees to admission.

Disposition
Admit to the acute medical unit. Nursing staff asked to record urine output and escalate oliguria, hypotension, breathlessness or worsening confusion. Repeat potassium and renal profile arranged for four hours after treatment.

Documented by: [MERCI CONWAY | Name 100%]
```

## en-gb-synthetic-00037 (en-GB, clinic_note)

Note leak risk 0.000, expected misses 0.00; 7 spans predicted, 0 gold spans missed.

```text
Endocrinology Outpatient Review

Patient: [Mallie | Name 100%]
Occupation: [Administrative assistant | Profession 100%]
Home address: [18 Teasdale Road, Fleet, GU52 0AB | Address_Location 100%]
Contact telephone: [07700 900509 | Contactdetails 100%]
Employer: [Moorend Public Library | Organization 100%]

Reason for review

Assessment of persistent symptoms in the context of established primary hypothyroidism treated with levothyroxine.

Clinical history

[Mallie | Name 100%] describes gradually worsening fatigue, particularly in the late afternoon, with reduced exercise tolerance but no exertional chest pain or breathlessness. They report increased sensitivity to cold and constipation for 3 days, although bowel frequency has generally been reduced over recent months. There has been no dysphagia, neck pain, change in voice or subjective thyroid swelling. Weight has increased by approximately 3 kg since the previous review. Appetite is unchanged.

Levothyroxine is currently taken every morning with water. On detailed questioning, breakfast is sometimes taken within 20 minutes of the dose, and a calcium-containing supplement is taken later in the morning. There are no other regular prescribed medicines. No recent A&E attendance or intercurrent infection was reported. Sleep is adequate, although the patient feels unrefreshed on waking. Mood is mildly low in relation to reduced energy, without suicidal thoughts or other features suggestive of a major depressive episode.

Examination

The patient was comfortable at rest and communicated appropriately. Pulse 62 beats per minute and regular; blood pressure 118/72 mmHg; temperature 36.4 °C. There was no tremor, lid lag or conjunctival injection. The thyroid was not enlarged or tender, with no palpable nodules or cervical lymphadenopathy. Heart sounds were normal, with no murmur. Chest examination was clear. There was dry skin over the forearms but no peripheral oedema. Neurological examination showed normal power and reflexes, with a mildly delayed relaxation phase at the ankles.

Investigations

Recent thyroid function testing showed TSH 8.6 mIU/L (reference range 0.4–4.0 mIU/L) and free T4 11.2 pmol/L (reference range 10–22 pmol/L). Full blood count was satisfactory, with haemoglobin 128 g/L. Ferritin was 42 micrograms/L, vitamin B12 318 ng/L and HbA1c 35 mmol/mol. Renal and liver profiles were unremarkable. These results are consistent with biochemical under-replacement rather than a new structural thyroid disorder.

Impression and plan

The symptoms and raised TSH most likely reflect suboptimal levothyroxine absorption or administration timing. Levothyroxine will be increased to 75 micrograms once daily. It should be taken with water on an empty stomach, ideally 30–60 minutes before breakfast; calcium supplements should be separated by at least 4 hours. No indication for thyroid imaging is identified today.

Repeat TSH and free T4 are requested in 8 weeks, with review arranged thereafter. Earlier clinical assessment is advised if palpitations, tremor, marked anxiety or chest pain develop. The patient understands the plan and will contact the clinic using [07700 900509 | Contactdetails 100%] if symptoms deteriorate or medication difficulties arise.
```

## en-gb-synthetic-00046 (en-GB, referral_letter)

Note leak risk 0.001, expected misses 0.00; 6 spans predicted, 0 gold spans missed.

```text
Dear Colleague,

Re: [Aarvika Millar | Name 100%]  
Patient identifier/MRN: [005317258 | ID 100%]

I would be grateful for an assessment by the appropriate mental health service regarding this patient’s generalised anxiety disorder, particularly the persistence of symptoms despite an adequate primary-care trial of sertraline and the most suitable next step in psychological treatment.

[Aarvika Millar | Name 100%] describes persistent, difficult-to-control worry across several areas of daily life, with associated poor sleep and marked muscle tension. They report spending prolonged periods anticipating adverse events and find it difficult to disengage from these thoughts. Sleep is currently fragmented, with prolonged sleep onset and early waking. There has also been intermittent nausea and reduced concentration, although appetite and weight are reported as stable. A recent exacerbation of anxiety has included palpitations for 3 days, without chest pain, syncope or exertional symptoms.

There is no reported history of mania, psychosis, illicit drug use or alcohol dependence. They deny thoughts of suicide or self-harm and have no current safeguarding concerns. On review in the surgery, they were appropriately dressed and engaged well, with mildly anxious affect but normal speech, coherent thought form and good insight. Observations were within the expected range. There was no tremor or focal neurological deficit. Recent blood tests, including full blood count, renal profile, liver function, thyroid function and ferritin, were unremarkable.

Sertraline was started at 50 mg once daily and increased to 100 mg once daily after review because of limited improvement. The patient reports taking it consistently for approximately eight weeks, without significant adverse effects. We have discussed sleep hygiene, reducing caffeine, paced breathing and graded activity. They have been signposted to NHS talking therapies and have begun using a brief cognitive behavioural therapy workbook, but symptoms continue to interfere with work and routine activities. They are not taking any other regular medicines.

Assessment

The presentation remains consistent with generalised anxiety disorder, with prominent insomnia and somatic tension. There is no evidence today of an acute psychiatric crisis, but the ongoing functional impact warrants specialist advice.

Requested action

Please assess whether a further medication adjustment, structured psychological intervention or combined approach would be appropriate. I would also welcome guidance on managing the sleep disturbance and on the recommended duration of sertraline treatment. The patient has been advised to seek urgent help through NHS 111 or the emergency department if suicidal thoughts, severe agitation or inability to keep safe develops.

Yours sincerely,

[taiba owen | Name 100%]  
GP  
Professional identifier: [GMC 0050249 | ID 100%]  
[QUEEN ELIZABETH UNIVERSITY HOSPITAL | Organization 100%]
```

## en-gb-synthetic-00082 (en-GB, referral_letter)

Note leak risk 0.002, expected misses 0.00; 7 spans predicted, 0 gold spans missed.

```text
Dear Endocrinology Team,
NHS number: [000 016 6791 | ID 100%]

Re: [Bran DONOVAN | Name 100%]

Clinical question
Please assess persistent biochemical and symptomatic hypothyroidism despite apparently appropriate levothyroxine treatment. I would value advice on dose adjustment, investigation of possible impaired absorption, and whether any further endocrine assessment is indicated.

History
[Bran DONOVAN | Name 100%] reports several months of troublesome fatigue, increased sensitivity to cold and constipation. There has been no neck swelling, dysphagia, hoarseness or tremor. They deny palpitations, diarrhoea and unintentional weight loss. Mood is somewhat low in the context of reduced energy, without thoughts of self-harm.

Treatment and adherence
Current medication is levothyroxine 75 micrograms once daily. The patient takes this on waking with water and generally waits before eating, although timing is less consistent at weekends. They do not take calcium, iron or over-the-counter thyroid supplements. There has been no recent change in prescribed medication. Adherence appears good, supported by their relative, [AIDAN GOODMAN | Name 100%].

Examination and results
At review, the patient was alert and clinically stable. Pulse was 68 bpm and regular; blood pressure was 124/76 mmHg. There was no palpable goitre or thyroid tenderness. No tremor, lid lag or peripheral oedema was observed. Weight has been broadly stable. Recent blood tests showed raised TSH with free T4 at the lower end of the reference range; full blood count, ferritin, vitamin B12, renal profile and liver tests were unremarkable. Coeliac serology has not yet been checked.

Management to date
I have reinforced administration of levothyroxine separately from food and mineral supplements. A repeat TSH and free T4 have been requested after a suitable interval, together with coeliac screening. No dose escalation has been made pending specialist advice.

Please advise whether further investigations, supervised dosing or a change in replacement strategy would be appropriate. The referral is submitted from [Fairhill | Address_Location 100%].

Yours sincerely,

[sorena nelson | Name 100%]
GP
GMC number: [GMC 0129331 | ID 100%]
```
