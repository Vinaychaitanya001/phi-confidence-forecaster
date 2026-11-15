"""Regex rules for the MedDeID English synthetic corpus (UK + US clinical documents), activated with
`regex.rule_sets: [meddeid]`. Written from the MedDeID annotation guideline and the surface forms seen in the
TRAIN split only (never calibration or test). Rules marked raw=True bypass the generic person/age clean-up so that
titles, credentials and age units stay inside the span, as the guideline requires:
    "Dr Suheib Childs, MBBS" -> whole string is Name:Caregiver;  "42-year-old" -> "42-year";  "40 y/o" -> "40 y/o"
"""
from __future__ import annotations

import re

from deid.detectors.regex_detector import MONTH, Rule, _r

# ----------------------------------------------------------------------------- building blocks
_T = r"(?:Dr|Prof|Professor|Mr|Mrs|Ms|Miss|Mx|Sr|Sister|Nurse|Rev)\.?"
_CRED = (r"(?:MD|DO|MBBS|MBChB|MB\s?BCh|BM\s?BS|RN|RGN|RMN|NP|ANP|PA-C|PA|FRCP|MRCP|FRCS|MRCS|MRCGP|FRCGP|FRCA|"
         r"FRCEM|FRCOG|MRCOG|MRCPCH|FRCPCH|PhD|BSN|MSN|DNP|CNM|CNS|DPM|DDS|DMD)")
_TOK = r"(?:[A-Za-z]\.|[A-Za-z][A-Za-z'’\-]*[A-Za-z]|[A-Za-z])"   # name token: initial "J." or a word (no trailing period)
# words that can never be part of a name value
_STOP_WORDS = {
    "a", "an", "the", "is", "was", "who", "with", "and", "or", "has", "had", "presented", "presents", "attended",
    "attends", "reports", "reported", "seen", "admitted", "came", "arrived", "referred", "aged", "age", "male",
    "female", "man", "woman", "boy", "girl", "patient", "pt", "today", "on", "at", "in", "for", "to", "of", "from",
    "by", "dob", "mrn", "nhs", "ssn", "re", "please", "thank", "dear", "yours", "regards", "kind", "noted", "states",
    "denies", "complains", "year", "years", "y/o", "yo", "day", "days", "week", "weeks", "month", "months", "old",
    "not", "stated", "documented", "supplied", "recorded", "known", "none", "unknown", "n/a", "na", "nil", "tbc",
    "gp", "consultant", "physician", "registrar", "nurse", "doctor", "clinician", "surgeon", "specialist", "team",
    "staff", "medicine", "medical", "stroke", "cardiology", "respiratory", "general", "senior", "junior", "lead",
    "identifier", "gmc", "nmc", "number", "id", "reference", "sibling", "spouse", "partner", "parent", "mother",
    "father", "friend", "child", "son", "daughter", "relative", "carer", "guardian", "neighbour", "neighbor",
    "husband", "wife", "brother", "sister", "colleague", "sir", "madam", "genetics", "department", "service",
    "ward", "clinic", "hospital", "practice", "surgery", "unit", "name", "signed", "see", "above", "below",
    "same", "self", "as", "per", "via", "lives", "living", "based", "resides", "updated", "informed", "present",
    "available", "contacted", "telephone", "phone", "email", "contact", "details", "detail", "hereditary", "risk",
    "assessment", "review", "follow", "up", "summary", "letter", "report", "note", "discharge", "referral",
    "admission", "history", "examination", "plan", "impression", "diagnosis", "treatment", "it", "he", "she",
    "they", "we", "you", "i", "his", "her", "their", "our", "this", "that", "these", "those", "no", "yes",
    "examination", "bloods", "pain", "impression", "observations", "obs", "chest", "abdomen", "heart", "lungs",
    "urine", "ecg", "ct", "mri", "cxr", "xr", "family", "home", "medication", "medications", "advice", "diet",
    "weight", "height", "bp", "temperature", "oxygen", "fluid", "fluids", "blood", "renal", "liver", "hb", "crp",
    "wcc", "sodium", "potassium", "creatinine", "glucose", "inr", "troponin", "lactate", "sats", "saturations",
    "pulse", "hr", "rr", "gcs", "news", "news2", "mobility", "bowels", "bladder", "sleep", "appetite", "mood",
    "skin", "wound", "dressing", "cannula", "catheter", "iv", "oral", "analgesia", "antibiotics", "nil", "ng",
    "management", "progress", "outcome", "result", "results", "finding", "findings", "symptoms", "symptom",
    "condition", "status", "function", "output", "intake", "balance", "level", "levels", "rate", "pressure",
    "unnamed", "registered", "emergency", "paediatric", "pediatric", "adult", "locum", "respiratory", "medicine",
    "cardiology", "neurology", "surgery", "surgical", "clinical", "specialty", "speciality", "laboratory",
    "genetics", "pharmacy", "radiology", "pathology", "nursing", "anaesthetic", "anaesthetics", "triage", "ambulance",
    "paramedic", "paramedics", "police", "social", "services", "safeguarding", "pharmacist", "physiotherapist",
    "occupational", "dietitian", "midwife", "sonographer", "radiographer", "healthcare", "assistant", "porter",
}
_STOP = r"(?:" + "|".join(sorted((re.escape(w) for w in _STOP_WORDS), key=len, reverse=True)) + r")"
_NOSTOP = rf"(?!{_STOP}(?=[\s,;:)]|$))"                 # the next token is not a whole stop word ("A." is fine)
_NAME = (rf"(?:{_T}[ \t]+)?{_NOSTOP}(?:{_TOK})(?:[ \t]+{_NOSTOP}(?:{_TOK})){{0,3}}"
         rf"(?:,[ \t]*{_CRED}(?:,[ \t]*{_CRED})?)?")
_ROLE = (r"(?:relative|spouse|partner|husband|wife|father|mother|parent|sibling|brother|sister|son|daughter|child|"
         r"friend|neighbou?r|carer|guardian|grand(?:mother|father|parent|son|daughter)|aunt|uncle|cousin|niece|nephew|"
         r"next\s+of\s+kin|nok|emergency\s+contact|informant|interpreter|advocate|key\s+worker|foster\s+(?:parent|carer))")

_NAME_HEADERS = (
    r"patient(?:\s+name)?|pt\.?(?:\s+name)?|name|re|"
    r"validated(?:\s+(?:and|&)\s+(?:reported|authori[sz]ed|released|signed|verified))?\s+by|"
    r"referring\s+(?:clinician|doctor|physician|gp|practitioner|consultant|nurse|midwife)|signed(?:\s+by)?|"
    r"discharging\s+(?:clinician|doctor|physician|consultant|nurse)|clinician|"
    r"attending(?:\s+(?:physician|clinician|consultant))?|documented\s+by|documenting\s+(?:rn|nurse|clinician)|"
    r"reviewing\s+(?:doctor|clinician)|reported\s+by|authori[sz]ed\s+by|released\s+by|verified\s+by|"
    r"consultant|gp|responsible\s+(?:clinician|consultant)|supervising\s+(?:clinician|consultant)|"
    r"(?:primary|duty|named|treating|admitting|ward|lead|clinical|requesting|operating|ordering)\s+"
    r"(?:nurse|clinician|doctor|consultant|physician|lead|surgeon|midwife)|clinical\s+lead|lead\s+clinician|"
    r"nurse|physician|doctor|author|dictated\s+by|surgeon|anaesthetist|anesthesiologist|radiologist|pathologist|"
    r"pharmacist|physiotherapist|midwife|sonographer|operator|key\s+worker|case\s+manager|social\s+worker|"
    r"emergency\s+contact(?:\s*/\s*(?:friend|partner|sibling|spouse|parent|carer|relative|neighbou?r|child))?|"
    r"legal\s+guardian|guardian|parent(?:\s+(?:present|at\s+bedside))?|mother|father|next\s+of\s+kin|nok|"
    r"accompanied\s+by|relative(?:\s+present|\s+involved)?|carer|spouse|partner|husband|wife|son|daughter|sibling|"
    r"informant|collateral(?:\s+from)?|family\s+(?:contact|member)|correspondence(?:\s+to)?|"
    r"history\s+(?:from|source)|interpreter|advocate|escort|chaperone"
)
# after the header, an optional role word before the actual name: "Relative present: sibling, PRAIRIE SHEPPARD"
_ROLE_PREFIX = rf"(?:{_ROLE}[ \t]*[,(:\-][ \t]*)?"

_ORG_HEADERS = (
    r"(?:patient'?s?\s+)?employer|reporting\s+laborator(?:y|ies)|referring\s+organi[sz]ation|"
    r"healthcare\s+organi[sz]ation|requesting\s+service|discharging\s+service|treating\s+facility|"
    r"clinic|family\s+support\s+(?:contact|affiliation)|(?:employer\s*/\s*)?community\s+affiliation|school|"
    r"affiliation|(?:referring|requesting|treating|admitting|discharging|receiving)\s+(?:organi[sz]ation|facility|"
    r"hospital|practice|service|site|unit)|(?:gp\s+)?practice|facility|hospital|laboratory|organi[sz]ation|"
    r"support\s+affiliation|correspondence\s*/\s*support\s+affiliation|institution|(?:care\s+)?provider|trust|health\s+board|"
    r"location\s+of\s+care|place\s+of\s+care|site|responsible\s+service|referred\s+(?:from|to|by)|"
    r"(?:reporting|responsible|treating|discharging|admitting|referring)\s+organi[sz]ation|reporting\s+(?:lab|laboratory)"
)
_ORG_SUFFIX_UK = (r"(?:NHS\s+(?:Foundation\s+)?Trust|Foundation\s+Trust|Health\s+Board|Hospitals?(?:\s+Trust)?|"
                  r"Infirmary(?:\s+of\s+[A-Z][A-Za-z]+)?|University\s+Hospitals?(?:\s+of\s+[A-Z][A-Za-z]+|\s+[A-Z][A-Za-z]{3,})?|General\s+Hospital|"
                  r"Medical\s+Cent(?:re|er)|Health\s+Cent(?:re|er)|Medical\s+Practice|Group\s+Practice|"
                  r"Hospice|Medical\s+Group|Health\s+System|Children'?s\s+Hospital|"
                  r"Community\s+Hospital|Regional\s+Medical\s+Center|Memorial\s+Hospital|Medical\s+Center)")
_ORG_LEAD_STOP = {"gp", "the", "a", "an", "local", "our", "their", "his", "her", "your", "this", "that", "nearest",
                  "another", "other", "same", "previous", "referring", "receiving", "treating", "admitting", "at",
                  "to", "from", "in", "of", "and", "or", "via", "by", "with", "for", "on", "was", "is", "district",
                  "general", "community", "university", "royal", "regional", "memorial", "children's", "childrens",
                  "where", "additional", "treatment", "accident", "emergency", "nhs", "clinical", "acute", "main"}
_DATE_ANY = (rf"(?:\d{{1,2}}[/.\-]\d{{1,2}}[/.\-]\d{{2,4}}|\d{{4}}-\d{{2}}-\d{{2}}|"
             rf"\d{{1,2}}(?:st|nd|rd|th)?\s+{MONTH}\.?,?\s+\d{{4}}|{MONTH}\.?\s+\d{{1,2}}(?:st|nd|rd|th)?,?\s+\d{{4}})")
_PLACE = r"[A-Z][A-Za-z'’\-]+(?:[ \t](?:of|a'?|an|the|y|ar|na|de|le|la|du|des)[ \t])?(?:[ \t][A-Z][A-Za-z'’\-]+){0,2}"
_PLACE_STOP = {
    "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
    "december", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "a&e", "ed", "icu",
    "itu", "hdu", "ccu", "nicu", "picu", "theatre", "theatres", "recovery", "resus", "majors", "minors", "triage",
    "clinic", "hospital", "ward", "bed", "room", "pain", "situ", "place", "order", "addition", "keeping", "view",
    "line", "total", "particular", "response", "terms", "light", "context", "summary", "general", "practice",
    "hours", "minutes", "days", "weeks", "months", "years", "time", "future", "person", "writing", "full", "part",
    "remission", "sinus", "atrial", "the", "an", "a", "uk", "england", "scotland", "wales", "ireland",
    "northern", "united", "states", "usa", "us", "america", "britain", "europe", "primary", "secondary", "care",
    "community", "nhs", "gp", "surgery", "accordance", "accord", "conjunction", "discussion", "agreement",
    "consultation", "liaison", "collaboration", "parallel", "progress", "attendance", "custody", "labour",
    "labor", "shock", "distress", "crisis", "spasm", "failure", "arrest", "doubt", "mind", "brief", "short",
    "long", "due", "course", "turn", "fact", "case", "spite", "excess", "error", "charge", "touch", "tandem",
    "bulk", "advance", "front", "back", "range", "most", "all", "some", "both", "either", "other", "english",
    "welsh", "scottish", "irish", "british", "american", "spanish", "polish", "french", "urdu", "punjabi",
    "arabic", "bengali", "hindi", "gujarati", "mandarin", "cantonese", "somali", "portuguese", "romanian",
}


_SPECIALTY = {
    "rheumatology", "respiratory", "medicine", "cardiology", "clinical", "genetics", "general", "paediatrics",
    "pediatrics", "paediatric", "pediatric", "neurology", "oncology", "haematology", "hematology", "gastroenterology",
    "nephrology", "urology", "orthopaedics", "orthopedics", "dermatology", "endocrinology", "psychiatry", "geriatrics",
    "obstetrics", "gynaecology", "gynecology", "surgery", "surgical", "medical", "emergency", "anaesthetics",
    "anaesthesia", "anesthesia", "radiology", "pathology", "laboratory", "microbiology", "biochemistry", "immunology",
    "pharmacy", "physiotherapy", "ophthalmology", "ent", "stroke", "acute", "elderly", "care", "team", "department",
    "unit", "service", "ward", "molecular", "chemical", "virology", "diabetes", "palliative", "intensive", "critical",
    "trauma", "maternity", "neonatal", "dental", "oral", "maxillofacial", "vascular", "thoracic", "plastic", "breast",
    "colorectal", "hepatology", "infectious", "diseases", "sexual", "health", "mental", "community", "primary",
    "outpatients", "outpatient", "inpatient", "ambulatory", "day", "assessment", "frailty", "rapid", "response",
    "same", "ed", "a&e", "icu", "itu", "hdu", "nicu", "picu", "ccu", "theatre", "theatres", "recovery", "triage",
    "resus", "children's", "childrens", "children’s", "adult", "women's", "men's", "minor", "injuries", "injury",
    "walk-in", "centre", "center", "and", "of", "for", "the", "&", "nhs", "hospital", "clinic", "medicine,",
    "unnamed", "registered", "locum", "on-call", "duty", "named", "senior", "junior", "specialist", "consultant",
    "clinician", "nurse", "doctor", "physician", "registrar", "surgeon", "practitioner", "midwife", "therapist",
    "pharmacist", "staff", "officer", "worker", "manager", "lead", "fellow", "intern", "resident", "attending",
    "gp", "rn", "snomed", "ct", "loinc", "icd", "edta", "serum", "plasma", "urine", "blood", "sample", "specimen",
    "sodium", "potassium", "creatinine", "glucose", "haemoglobin", "hemoglobin", "crp", "wcc", "inr", "troponin",
    "lactate", "copd", "dvt", "pe", "mi", "tia", "cva", "uti", "aki", "ckd", "chf", "af", "htn", "dm", "cpap",
    "bipap", "niv", "oxygen", "air", "room", "home", "bed", "chair", "discharge", "admission", "transfer",
    "referral", "review", "follow-up", "follow", "up", "plan", "treatment", "therapy", "antibiotics", "fluids",
    "analgesia", "observations", "obs", "examination", "history", "impression", "diagnosis", "differential",
    "internal", "/", "(", ")", "ordering", "requesting", "hospitalist", "hospital", "medicine", "family",
    "geriatric", "psychiatric", "paediatrics,", "accident", "department,", "services", "social", "work",
    "dietetics", "nutrition", "speech", "language", "occupational", "podiatry", "orthotics", "audiology",
    "optometry", "neonatology", "perinatal", "antenatal", "postnatal", "fertility", "andrology", "sleep",
    "allergy", "burns", "spinal", "neurosurgery", "cardiothoracic", "transplant", "renal", "dialysis",
    "chemotherapy", "radiotherapy", "haemato-oncology", "clinical,", "nursing", "midwifery", "paramedic",
}
_ROLE_NEXT = re.compile(
    r"[ \t]+(?:clinician|consultant|nurse|doctor|team|department|medicine|physician|registrar|surgeon|practitioner|"
    r"specialist|midwife|therapist|pharmacist|staff|service|unit|ward|clinic|hospital|laboratory|officer|worker|"
    r"manager|lead|fellow|intern|resident|attending|child|children|clinician,|rn|gp)\b")


def _all_specialty(words: list[str]) -> bool:
    return bool(words) and all(w.lower().strip(",.;:()/") in _SPECIALTY or w in "/()-–" for w in words)


# ----------------------------------------------------------------------------- validators
_EMPTY = {"none", "n/a", "na", "nil", "unknown", "not known", "not recorded", "not documented", "not stated",
          "not supplied", "nk", "-", "tbc", "see below", "as above", "self", "same", "not applicable", "declined",
          "retired", "student", "unemployed", "pupil", "schoolchild", "homemaker", "housewife", "pensioner",
          "not applicable (child)", "child", "infant", "toddler", "baby", "n/k", "unk", "pending", "to follow"}


def _v_value(m: re.Match, _t: str) -> bool:
    return m.group(1).strip(" .").lower() not in _EMPTY


def _case_consistent(core: list[str]) -> bool:
    """Name tokens are all Title/UPPER case, or all lower case ("honie hunt"); 'Hereditary breast' is neither."""
    kinds = {("l" if t[0].islower() else "u") for t in core}
    return len(kinds) == 1


def _v_name(m: re.Match, text: str) -> bool:
    v = m.group(1).strip()
    toks = [t for t in re.split(r"[ \t]+", v) if t]
    if not toks or len(toks) > 5:
        return False
    core = [t.rstrip(",") for t in toks if not re.fullmatch(_T, t) and not re.fullmatch(_CRED + ",?", t.rstrip(","))]
    if not core:
        return False
    if any(t.rstrip(",.").lower() in _STOP_WORDS for t in core if not re.fullmatch(r"[A-Za-z]\.", t.rstrip(","))):
        return False
    if any(t.endswith(("'s", "’s")) for t in core):
        return False
    if any(not re.fullmatch(r"[A-Za-z][A-Za-z'’\-]*\.?,?", t) for t in toks):
        return False
    if not _case_consistent(core):
        return False
    # all-lower-case names only as 1-2 tokens (first [last]); longer lower-case runs are sentences
    if core[0][0].islower() and len(core) > 2:
        return False
    if _all_specialty(core):
        return False
    if _ROLE_NEXT.match(text, m.end(1)):           # "Unnamed respiratory medicine clinician", "adult child"
        return False
    return v.strip(" .").lower() not in _EMPTY


def _v_name_lc_strict(m: re.Match, text: str) -> bool:
    """Lower-case names only when the name ends the clause (sign-offs, 'reported by sholah perkins\\n')."""
    if not _v_name(m, text):
        return False
    v = m.group(1).strip()
    if v[0].islower():
        return bool(re.match(r"[ \t]*(?:\n|$)", text[m.end(1):]))
    return True


def _v_name_two(m: re.Match, text: str) -> bool:
    """Header on its own line followed by the name on the next line: require 2+ tokens or an initial."""
    if not _v_name(m, text):
        return False
    v = m.group(1).strip()
    return len(v.split()) >= 2 or bool(re.search(r"\b[A-Za-z]\.", v))


_PLACE_PREV_OK = {"relative", "relatives", "family", "home", "locally", "via", "based", "lives", "living", "resides",
                  "residing", "contacted", "reachable", "contactable", "staying", "located", "recorded", "as",
                  "travelled", "traveled", "travelling", "traveling", "visiting", "originally", "resident"}


def _v_place_after(m: re.Match, text: str) -> bool:
    if not _v_place(m, text):
        return False
    before = text[max(0, m.start() - 40):m.start(1)]
    words = re.findall(r"[A-Za-z'’\.\-]+", before)
    words = [w for w in words if w.lower() not in ("in", "from", "at", "via", "near")]
    if not words:
        return False
    prev = words[-1]
    return prev.lower() in _PLACE_PREV_OK or (prev[0].isupper() and prev.lower() not in _SPECIALTY)


def _v_name_cap(m: re.Match, text: str) -> bool:
    """Narrative name rules: first token must be capitalised (lower-case narrative names are left to the model)."""
    return _v_name(m, text) and m.group(1).lstrip()[0].isupper()


def _v_age(m: re.Match, text: str) -> bool:
    after = text[m.end(1):m.end(1) + 16]
    if re.search(r"(?i)^['’]?\s*gestation|^\s*gestational|^\s*post[- ]?partum|^\s*(?:course|history|supply)\b", after):
        return False
    prev = text[max(0, m.start(1) - 14):m.start(1)]
    if re.search(r"(?i)(?:\bfor|\bover|\bpast|\blast|\bsince|\bwithin|\bafter|\bevery|\bin\s+about|\bin|\bnext|"
                 r"\bx|\+\d*|\bcomplete\s+a|\ba\s+further)\s*$", prev):
        return False
    return True


def _v_org_suffix(m: re.Match, _t: str) -> bool:
    words = m.group(1).split()
    lead = list(words[:-1])
    while lead and lead[0].lower() in _ORG_LEAD_STOP:
        lead.pop(0)
    return bool(lead) and any(w[:1].isupper() and w.lower() not in _ORG_LEAD_STOP for w in lead)


def _v_org_ext(m: re.Match, text: str) -> bool:
    """Extended organisation names: the trailing words must not be a specialty/stop word or a sentence start."""
    v = m.group(1)
    words = v.split()
    if len(words) < 2:
        return False
    tail = words[-1].strip(",.;:").lower()
    if tail in _SPECIALTY and "-" not in v and tail not in ("hospital", "infirmary", "trust"):
        return False
    if tail in _ORG_LEAD_STOP or tail in _STOP_WORDS:
        return False
    nxt = text[m.end(1):m.end(1) + 2]
    return not re.match(r"[ \t][a-z]", nxt) or True


def _v_org_value(m: re.Match, text: str) -> bool:
    v = m.group(1).strip()
    if v.strip(" .").lower() in _EMPTY:
        return False
    words = v.split()
    if _all_specialty(words):
        return False
    # a proper name: at least one capitalised word that is not a generic lead word; not a sentence
    return 1 <= len(words) <= 9 and any(w[:1].isupper() and w.lower() not in _ORG_LEAD_STOP for w in words) \
        and not re.search(r"[.!?]\s+[a-z]", v)


def _v_place(m: re.Match, text: str) -> bool:
    v = m.group(1).strip()
    words = [w.lower() for w in v.split()]
    if not words or words[0] in _PLACE_STOP or v.lower() in _PLACE_STOP:
        return False
    if any(w in {"hospital", "infirmary", "trust", "clinic", "surgery", "practice", "centre", "center", "ward",
                 "department", "unit", "team", "service", "gp", "a&e", "dr", "mr", "mrs", "ms"} for w in words):
        return False
    if _all_specialty(v.split()) or any(w.strip(",.") in _SPECIALTY for w in words):
        return False
    if len(v.split()) == 1 and v.isupper() and len(v) <= 5:   # EDTA, DVT, COPD
        return False
    return not re.fullmatch(_T, v.split()[0])


def _v_digits(m: re.Match, _t: str) -> bool:
    return sum(ch.isdigit() for ch in m.group(1)) >= 4


# ----------------------------------------------------------------------------- rules
def build_meddeid_rules() -> list[Rule]:
    R: list[Rule] = []
    # ---- identifiers
    R.append(_r("md_nhs_number", "ID",
                r"(?i)\bNHS\s*(?:number|no\.?|num|#)?\s*[:\-]?\s*(\d{3}[ \-]?\d{3}[ \-]?\d{4})(?!\d)", group=1, priority=8))
    R.append(_r("md_ni_number_ctx", "ID",
                r"(?i)\bnational\s+insurance(?:\s+(?:number|no\.?|num))?\s*[:\-]?\s*([A-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]?)(?![A-Z0-9])",
                group=1, priority=8))
    R.append(_r("md_ni_number", "ID", r"\b([A-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D])\b", group=1, priority=12))
    R.append(_r("md_ssn_spaced", "ID", r"(?<![\d-])(\d{3}[ \-]\d{2}[ \-]\d{4})(?![\d-])", group=1, priority=11))
    R.append(_r("md_mrn", "ID",
                r"(?i)\b(?:MRN|medical\s+record\s+(?:number|no\.?)|patient\s+identifier(?:\s*[/(]\s*MRN\s*\)?)?|"
                r"MRN\s*/\s*patient\s+identifier|hospital\s+(?:number|no\.?)|patient\s+(?:number|no\.?|id))(?![A-Za-z])"
                r"\s*[:\-]?\s*(?=[A-Za-z0-9/\- ]*\d)([A-Z0-9](?:[A-Z0-9/\-]|[ ](?=\d)){3,})(?![A-Z0-9/\-])", group=1, priority=8))
    R.append(_r("md_accession", "ID",
                r"(?i)\b(?:report\s*/\s*accession\s+id(?:entifier)?|accession\s+(?:id(?:entifier)?|number|no\.?)|"
                r"report\s+(?:id(?:entifier)?|number|no\.?)|lab(?:oratory)?\s+(?:id|number|no\.?)|"
                r"specimen\s+(?:id|number|no\.?)|sample\s+(?:id|number|no\.?)|order\s+(?:id|number|no\.?)|"
                r"encounter\s+(?:id|number|no\.?)|visit\s+(?:id|number|no\.?)|case\s+(?:id|number|no\.?)|"
                r"admission\s+(?:id|number|no\.?))(?![A-Za-z])"
                r"\s*(?:[:\-]|\bis|\bwas|\bof|recorded(?:\s+as)?)?\s*(?=[A-Za-z0-9/\- ]*\d)([A-Z0-9](?:[A-Z0-9/\-]|[ ](?=\d)){3,})(?![A-Z0-9/\-])",
                group=1, priority=8))
    R.append(_r("md_professional_id", "ID",
                r"(?i)\b(?:professional\s+(?:identifier|id|registration(?:\s+(?:number|no\.?))?|number)|"
                r"GMC(?:\s+(?:number|no\.?|identifier|reference|registration|professional\s+identifier))?|NMC(?:\s+PIN)?|"
                r"HCPC|GPhC|GDC|NPI|licen[cs]e\s+(?:number|no\.?)|registration\s+(?:number|no\.?)|"
                r"identifier\s+for\s+(?:the\s+)?[a-z ]{3,30}?|"
                r"(?:rn|nurse|clinician|doctor|physician|consultant)\s+professional\s+(?:id|identifier))(?![A-Za-z])"
                r"\s*(?:[:\-]|\bis|\bwas|\bof|recorded(?:\s+as)?|\(|as)?\s*"
                r"((?:GMC|LIC|NMC|NPI|HCPC)?[\-\s]?(?:TEST[\-\s]?)?\d{5,11}|[A-Z]{2,4}[\-\s]?\d{5,10}|"
                r"[A-Z]{2,4}-[A-Z]{2,5}-\d{5,10})(?![A-Z0-9])", group=1, priority=8))
    R.append(_r("md_professional_id_prefixed", "ID",
                r"\b((?:GMC|LIC|NMC|NPI|HCPC)[\-\s]?(?:TEST[\-\s]?)?\d{6,10})(?![A-Z0-9])", group=1, priority=12))
    # sign-off block: a bare 7-9 digit registration number on its own line shortly after "Yours sincerely"
    R.append(_r("md_signoff_id", "ID",
                r"(?is)yours\s+(?:sincerely|faithfully|truly),?[^\n]*\n(?:[^\n]*\n){0,4}?[ \t]*(\d{7,9})[ \t]*(?=\n|$)",
                group=1, priority=14))
    # ---- contact
    R.append(_r("md_uk_mobile", "PHONE",
                r"(?<![\d+])((?:(?:\+|00)44\s?\(?0?\)?\s?7\d{3}|07\d{3})[ \-]?\d{3}[ \-]?\d{3})(?!\d)", group=1, priority=13))
    R.append(_r("md_uk_landline", "PHONE",
                r"(?<![\d+])((?:(?:\+|00)44\s?\(?0?\)?\s?|0)(?:1\d{2,3}|2\d|3\d{2}|8\d{2})[ \-]?\d{3,4}[ \-]?\d{3,4})(?!\d)",
                group=1, priority=17))
    # ---- age and date of birth
    R.append(_r("md_age_hyphen", "AGE", r"(?<![\d.+])(\d{1,3}\s?-\s?year)(?=\s?-\s?old\b|\b)",
                group=1, validator=_v_age, priority=20))
    R.append(_r("md_age_hyphen_small", "AGE", r"(?<![\d.+])(\d{1,3}\s?-\s?(?:month|week|day))(?=\s?-\s?old\b)",
                group=1, validator=_v_age, priority=20))
    R.append(_r("md_age_yo", "AGE", r"(?i)(?<![\d.+])(\d{1,3}\s?(?:y/o|yo|yrs?\s?old|y\.o\.))(?![A-Za-z])",
                group=1, validator=_v_age, priority=20))
    R.append(_r("md_age_unit_old", "AGE",
                r"(?i)(?<![\d.+])(\d{1,3}\s?(?:years?|yrs?|months?|mths?|weeks?|wks?|days?))(?=\s+old\b|\s?-\s?old\b)",
                group=1, validator=_v_age, priority=20))
    R.append(_r("md_age_header", "AGE",
                r"(?i)\b(?:clinical\s+age(?:\s+group)?|age(?:\s*/\s*sex)?|aged)\s*[:\-]?\s*(\d{1,3}(?:\.\d)?(?:\s?(?:years?|yrs?|y/o|yo|"
                r"months?|mths?|weeks?|wks?|days?))?)(?![\d.])", group=1, validator=_v_age, priority=19))
    R.append(_r("md_dob", "AGE",
                rf"(?i)\b(?:DOB|D\.O\.B\.?|date\s+of\s+birth|birth\s*date|born(?:\s+on)?)\s*[:\-]?\s*({_DATE_ANY})(?![\d/])",
                group=1, priority=9))
    # ---- profession
    R.append(_r("md_profession", "PROFESSION",
                r"(?i)\b(?:patient'?s?\s+)?occupation(?:\s*/\s*employment)?\s*[:\-]\s*"
                r"([A-Za-z][A-Za-z'’/&\- ]{1,60}?)\s*(?=[\n\r.;|,()\t]|\s{2,}|$)", group=1, validator=_v_value,
                priority=20))
    # ---- names: headers
    R.append(_r("md_name_header", "PERSON",
                rf"(?i:(?:^|(?<=[\n\t|;(]))[ \t]*(?:{_NAME_HEADERS})[ \t]*:[ \t]*\n?[ \t]*{_ROLE_PREFIX})({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name, priority=30, flags=re.MULTILINE))
    R.append(_r("md_name_header_nl", "PERSON",
                rf"(?i:(?:^|(?<=\n))[ \t]*(?:{_NAME_HEADERS})[ \t]*\n[ \t]*)({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name_two, priority=30, flags=re.MULTILINE))
    R.append(_r("md_name_header_inline", "PERSON",
                rf"(?i:\b(?:{_NAME_HEADERS})[ \t]*:[ \t]*{_ROLE_PREFIX})({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name, priority=32))
    # ---- names: credential / title
    R.append(_r("md_name_credential", "PERSON",
                rf"\b((?:{_T}\s+)?[A-Za-z][A-Za-z'’\-]+(?:\s+[A-Za-z][A-Za-z'’\-]*\.?){{1,3}},\s*{_CRED}(?:,\s*{_CRED})?)(?![A-Za-z])",
                group=1, priority=28))
    R.append(_r("md_name_title", "PERSON",
                rf"\b((?:Dr|Prof|Professor|Sister|Mr|Mrs|Ms|Miss)\.?\s+[A-Z][A-Za-z'’\-]+(?:\s+(?:[A-Z]\.|[A-Z][A-Za-z'’\-]+)){{0,2}})"
                rf"(?![A-Za-z])", group=1, priority=29))
    # ---- names: narrative triggers
    R.append(_r("md_name_signoff", "PERSON",
                rf"(?i:\b(?:yours\s+(?:sincerely|faithfully|truly)|kind(?:est)?\s+regards|best\s+wishes|with\s+thanks|"
                rf"many\s+thanks|regards|signed|electronically\s+signed(?:\s+by)?),?[ \t]*\n+[ \t]*)({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name, priority=27))
    R.append(_r("md_name_by", "PERSON",
                rf"(?i:\b(?:documented|validated|reported|reviewed|seen|authori[sz]ed|released|signed|assessed|examined|"
                rf"dictated|discussed|agreed|countersigned|verified|completed|entered|prepared|written|checked|"
                rf"accompanied|escorted|supported|clerked|performed|supervised|requested|ordered|approved|discharged|"
                rf"admitted|transferred|handed\s+over|taken\s+over)"
                rf"(?:\s+(?:and|&)\s+[a-z]+)?(?:\s+[a-z]+ly)?\s+by[ \t]*:?\s*{_ROLE_PREFIX}"
                rf"(?:(?:the|a|an)\s+)?(?:(?:on-call|duty|medical|surgical|senior|junior|treating|named|responsible|"
                rf"acute|emergency|paediatric|pediatric|consultant|specialist|registered|lead|locum|ward|clinical|"
                rf"nurse|staff|team|registrar|physician|doctor|clinician|nurse|midwife|gp|practitioner|assistant|"
                rf"associate|fellow|resident|intern|student)\s+){{0,4}})({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name_lc_strict, priority=31))
    R.append(_r("md_name_under", "PERSON",
                rf"(?i:\b(?:under(?:\s+the\s+care\s+of)?|care\s+of|c/o)\s+(?:the\s+)?(?:(?:on-call|duty|medical|surgical|"
                rf"acute|consultant|team|registrar|physician|doctor)\s+){{0,3}})({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name_cap, priority=34))
    R.append(_r("md_name_with", "PERSON",
                rf"(?i:\b(?:agreed|discussed|liaised|confirmed|spoke|spoken|reviewed|handed\s+over)\s+with\s+(?:the\s+)?"
                rf"(?:(?:on-call|duty|medical|surgical|senior|junior|acute|emergency|paediatric|pediatric|consultant|"
                rf"specialist|registrar|physician|doctor|clinician|nurse|midwife|gp|team|ward|named|treating)\s+){{0,4}})"
                rf"({_NAME})(?=[\s,.;:)(|]|$)", group=1, validator=_v_name_cap, priority=33))
    R.append(_r("md_name_relation", "PERSON",
                rf"(?i:\b(?:(?:his|her|their|the\s+patient'?s|patient'?s|your|my|a|an|the)\s+)?(?:adult\s+|elderly\s+|young\s+)?"
                rf"{_ROLE}(?:\s*\([^)\n]{{1,25}}\))?[ \t]*[,:\-]?[ \t]*)({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name_cap, priority=31))
    R.append(_r("md_name_relation_after", "PERSON",
                rf"({_NAME})(?i:,[ \t]*(?:who\s+is\s+)?(?:his|her|their|the\s+patient'?s|a|an|the|our)\s+(?:[a-z\-]+\s+){{0,3}}"
                rf"(?:{_ROLE}|clinician|consultant|doctor|nurse|registrar|physician|surgeon|gp|midwife|paramedic|pharmacist|"
                rf"physiotherapist|therapist)\b)",
                group=1, validator=_v_name, priority=31))
    R.append(_r("md_name_referring", "PERSON",
                rf"(?i:\b(?:I\s+am\s+(?:re-?)?referring|we\s+are\s+referring|thank\s+you\s+for\s+(?:seeing|reviewing|referring)|"
                rf"(?:summary|letter|report|note|record)\s+for|dear)\s+)({_NAME})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_name, priority=31))
    # sentence-initial patient name followed by a strong verb: "Kyra-Rose A. attended", "Nergiz is a 56-year-old"
    R.append(_r("md_name_subject", "PERSON",
                rf"(?:(?<=\n)|(?<=\n[ \t])|(?<=\.\s)|(?<=\.\s\s)|^)([A-Z][A-Za-z'’\-]+[ \t][A-Z]\.)"
                rf"(?=[ \t]+(?:is|was|remains|attended|attends|says|said|describes|described|presented|presents|reports|"
                rf"reported|denies|underwent|received|arrived|tolerated|continues|continued|remained|should|will|has|had|"
                rf"lives|came|returned|requires|required|agreed|declined|wishes|would|can|cannot|did|does|updated|"
                rf"was\s+seen|is\s+a|was\s+a)\b)", group=1, validator=_v_name_cap, priority=39, flags=re.MULTILINE))
    # ---- places
    R.append(_r("md_uk_postcode", "LOCATION", r"\b([A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2})\b", group=1, priority=30))
    R.append(_r("md_locality", "LOCATION",
                rf"(?i:\b(?:[a-z/' ]{{0,40}}?locality|service\s+location|locality)\s*(?:is|was|[:\-])\s*)({_PLACE})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_place, priority=30))
    R.append(_r("md_home_address", "LOCATION",
                r"(?i)\b(?:home\s+address(?:\s+on\s+file)?|usual\s+address|mailing\s+address|patient(?:'s)?\s+(?:home\s+)?address|"
                r"address|residence)\s*[:\-][ \t]*([0-9A-Za-z][^\n\t|;]{4,120}?)[ \t]*(?=[\n\t|;]|\s{3,}|$)",
                group=1, priority=25))
    R.append(_r("md_place_in_from", "LOCATION",
                rf"(?i:\b(?:lives|living|resides|residing|based|located|staying|is|are|was|were|comes|coming|came|travell?ed|"
                rf"made|calling|contactable|reachable|resident)\s+(?:in|from|at|near)\s+)({_PLACE})(?=[\s,.;:)(|]|$)",
                group=1, validator=_v_place, priority=33))
    R.append(_r("md_place_after_name_from", "LOCATION",
                rf"(?i:(?<=[A-Za-z.]),?[ \t]+(?:from|in|via|at|near)[ \t]+)({_PLACE})(?=[ \t]*[,.;)]|\s+(?:was|were|is|has|provided|attended|who|if|and|for|to|with)\b)",
                group=1, validator=_v_place_after, priority=38))
    R.append(_r("md_place_signoff", "LOCATION",
                rf"(?i:(?:\bGP|clinician|service|practice|hospital|infirmary|trust|surgery|centre|center|team|clinic)[ \t]*(?:,|\n)[ \t]*)({_PLACE})(?=[ \t]*(?:\n|$|,))",
                group=1, validator=_v_place, priority=34))
    # ---- organisations
    R.append(_r("md_org_header", "ORGANIZATION",
                rf"(?i:(?:^|(?<=[\n\t|;(]))[ \t]*(?:{_ORG_HEADERS})[ \t]*:[ \t]*)([A-Z0-9][^\n\t|;]{{2,90}}?)[ \t]*(?=[\n\t|;]|\s{{3,}}|$|\.\s*(?:\n|$))",
                group=1, validator=_v_org_value, priority=35, flags=re.MULTILINE))
    R.append(_r("md_org_from_line", "ORGANIZATION",
                r"(?im)^[ \t]*from[ \t]*:[ \t]*([A-Z0-9][^\n\t|;]{2,90}?)[ \t]*(?=[\n\t|;]|$)", group=1,
                validator=_v_org_value, priority=36))
    R.append(_r("md_org_suffix", "ORGANIZATION",
                rf"\b((?:(?:[A-Z][A-Za-z'’&\-]+|of|the|and|&)[ \t]+){{1,6}}(?i:{_ORG_SUFFIX_UK}))(?![A-Za-z])",
                group=1, validator=_v_org_suffix, priority=44))
    R.append(_r("md_org_named_generic", "ORGANIZATION",
                r"\b((?:University|Royal|General|Community|Memorial|Regional|District|County|Children'?s|St\.?|Saint)[ \t]+"
                r"(?:Hospitals?|Infirmary|Medical[ \t]+Cent(?:re|er))(?:[ \t]+of)?(?:[ \t]+[A-Z][A-Za-z'’\-]{2,}){1,2})(?![A-Za-z])",
                group=1, validator=_v_org_ext, priority=43))
    R.append(_r("md_org_suffix_ext", "ORGANIZATION",
                rf"\b((?:(?:[A-Z][A-Za-z'’&\-]+|of|the|and|&)[ \t]+){{1,6}}(?i:{_ORG_SUFFIX_UK})"
                rf"(?:[ \t]+-[ \t]+[A-Z][A-Za-z0-9&'’ ]{{3,45}}?|[ \t]+(?:Site|Campus|Annexe?|Wing)|(?:[ \t]+[A-Z]{{3,}}){{1,3}}|(?:[ \t]+[A-Z][a-z]{{3,}}){{1,2}}))"
                rf"(?=[\n,.;:)(]|[ \t]+(?:[a-z]|$)|$)", group=1, validator=_v_org_ext, priority=42))
    R.append(_r("md_org_for_line", "ORGANIZATION",
                r"(?m)^[ \t]*(?:For|On\s+behalf\s+of)[ \t]+([A-Z][^\n\t|;]{2,80}?)[ \t]*$", group=1,
                validator=_v_org_value, priority=37))
    raw = {"md_org_named_generic", "md_org_suffix_ext",
           "md_name_header", "md_name_header_nl", "md_name_header_inline", "md_name_credential", "md_name_title",
           "md_name_signoff", "md_name_by", "md_name_with", "md_name_under", "md_name_relation", "md_name_relation_after",
           "md_name_referring", "md_name_subject",
           "md_age_hyphen", "md_age_hyphen_small", "md_age_yo", "md_age_unit_old", "md_age_header",
           "md_org_header", "md_org_from_line", "md_org_suffix", "md_org_for_line"}
    return [Rule(r.name, r.label, r.pattern, r.group, r.validator, r.unit_guard, r.priority, r.optional, r.name in raw)
            for r in R]
