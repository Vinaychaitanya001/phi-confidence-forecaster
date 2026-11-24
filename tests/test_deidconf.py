"""Unit tests for deidconf: split determinism, MedDeID rules on crafted sentences, metrics, candidate generation."""
import numpy as np
import pytest

from deidconf.data import LABELS, assign_splits


# ----------------------------------------------------------------------------- split
def test_split_is_deterministic_and_stratified():
    notes = [{"note_id": f"n{i}", "lang": "en-GB" if i % 2 else "en-US", "doc_type": f"t{i % 3}"} for i in range(600)]
    a = assign_splits(notes, {"train": 0.7, "cal": 0.15, "test": 0.15}, seed=1)
    b = assign_splits(list(reversed(notes)), {"train": 0.7, "cal": 0.15, "test": 0.15}, seed=1)
    assert a == b
    counts = {k: sum(1 for v in a.values() if v == k) for k in ("train", "cal", "test")}
    assert counts["train"] == 420 and counts["cal"] == 90 and counts["test"] == 90
    gb = [n["note_id"] for n in notes if n["lang"] == "en-GB"]
    assert sum(1 for i in gb if a[i] == "test") == 45
    assert assign_splits(notes, {"train": 0.7, "cal": 0.15, "test": 0.15}, seed=2) != a


# ----------------------------------------------------------------------------- rules
@pytest.fixture(scope="module")
def regex():
    from deid.detectors.regex_detector import RegexDetector
    from deidconf.detect import adapted_configs
    return RegexDetector.from_config(adapted_configs()[0])


def found(regex, text):
    return {(text[e.start:e.end], e.label) for e in regex.detect(text)}


@pytest.mark.parametrize("text,expected", [
    ("NHS number: 000 161 4780\n", ("000 161 4780", "ID")),
    ("National Insurance number: ZZ 37 59 11 A\n", ("ZZ 37 59 11 A", "ID")),
    ("MRN: 0466356\n", ("0466356", "ID")),
    ("Report/Accession ID: LAB-08664712\n", ("LAB-08664712", "ID")),
    ("GMC identifier 0449082.", ("0449082", "ID")),
    ("Professional identifier: GMC-TEST-0340295\n", ("GMC-TEST-0340295", "ID")),
    ("Contact: 07700 900547\n", ("07700 900547", "PHONE")),
    ("Patient: Elis, a 42-year-old African American male patient", ("42-year", "AGE")),
    ("Clinical age: 65 y/o\n", ("65 y/o", "AGE")),
    ("The patient is 23 years old.", ("23 years", "AGE")),
    ("DOB: 12/05/1998\n", ("12/05/1998", "AGE")),
    ("Occupation: Taxi driver\nHome address: 1 Road", ("Taxi driver", "PROFESSION")),
    ("Discharging clinician: Dr Suheib Childs, MBBS\n", ("Dr Suheib Childs, MBBS", "PERSON")),
    ("Attending: Avyana Misso, MD\n", ("Avyana Misso, MD", "PERSON")),
    ("Patient: OKKES REILLY\nOccupation: Writer", ("OKKES REILLY", "PERSON")),
    ("Patient: honie hunt\nMRN: 0466356", ("honie hunt", "PERSON")),
    ("Yours sincerely,\n\nI. MCCANN\nGP, ROSTREVOR", ("I. MCCANN", "PERSON")),
    ("Yours sincerely,\n\nI. MCCANN\nGP, ROSTREVOR", ("ROSTREVOR", "LOCATION")),
    ("Validated and reported by sholah perkins\nLaboratory medicine clinician", ("sholah perkins", "PERSON")),
    ("With your consent, your relative A. Bryant in Poolewe was informed.", ("A. Bryant", "PERSON")),
    ("With your consent, your relative A. Bryant in Poolewe was informed.", ("Poolewe", "LOCATION")),
    ("Relative present: sibling, PRAIRIE SHEPPARD\n", ("PRAIRIE SHEPPARD", "PERSON")),
    ("Home address: 22 De Ferrers Drive, Aylesbury, HP19 0FA\n", ("22 De Ferrers Drive, Aylesbury, HP19 0FA", "LOCATION")),
    ("Employer: Brownroyd Hill Secondary School\n", ("Brownroyd Hill Secondary School", "ORGANIZATION")),
    ("You were admitted to Aberdeen Royal Infirmary with heart failure.", ("Aberdeen Royal Infirmary", "ORGANIZATION")),
    ("Service locality: Braeswick\n", ("Braeswick", "LOCATION")),
])
def test_meddeid_rules_find(regex, text, expected):
    assert expected in found(regex, text)


@pytest.mark.parametrize("text,bad", [
    ("Venous pH: 7.37 (7.31–7.41)", "7.37 (7.31"),
    ("Review on 31/04/2025 if needed.", "31/04/2025"),
    ("Pain reduced from 6/10 to 3/10 after analgesia.", "6/10"),
    ("Complete a 14-day course of antibiotics.", "14-day"),
    ("Term baby at 9+4 weeks' gestation.", "4 weeks"),
    ("Requesting clinician: Not stated\n", "Not stated"),
    ("Responsible consultant: General Medicine\n", "General"),
    ("Re: Hereditary breast and ovarian cancer risk assessment", "Hereditary breast"),
    ("Requesting service: Cardiology\n", "Cardiology"),
    ("Referring organisation: Ulster Hospital\n", "organisation"),
    ("Early benefit from CPAP, but adherence poor.", "CPAP"),
    ("There is a six-week history of pain.", "There"),
])
def test_meddeid_rules_do_not_fire(regex, text, bad):
    assert bad not in {t for t, _ in found(regex, text)}


# ----------------------------------------------------------------------------- metrics
def test_ece_perfect_and_worst():
    from deidconf.confidence import ece, review_capture
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    assert ece(y.astype(float), y) == 0.0
    assert ece(1 - y.astype(float), y) == pytest.approx(1.0)
    p = np.array([0.9, 0.95, 0.99, 0.8, 0.1, 0.2, 0.6, 0.7])
    cap = review_capture(p, y, budgets=(0.25, 0.5))
    assert cap["capture@25%"] == pytest.approx(0.5) and cap["capture@50%"] == pytest.approx(1.0)


# ----------------------------------------------------------------------------- candidates
def test_candidates_pick_uncovered_mass_and_repeats():
    from deidconf.features import TagGroups
    from deidconf.nearmiss import candidates_for_note
    meta = {"tags": [["O", None], ["B", "first_name"], ["I", "first_name"], ["B", "city"]], "o_index": 0}
    groups = TagGroups(meta, {"first_name": "PERSON", "city": "LOCATION"})
    text = "Seen Reilly today. Reilly lives in Poolewe now."
    words = [(0, 4), (5, 11), (12, 18), (19, 25), (26, 31), (32, 34), (35, 42), (43, 47)]
    P = np.zeros((len(words), 4), dtype=np.float32)
    P[:, 0] = 1.0
    P[1] = [0.1, 0.9, 0, 0]          # Reilly (predicted)
    P[3] = [0.6, 0.4, 0, 0]          # second Reilly: weak -> candidate by mass and by repeat
    P[6] = [0.9, 0, 0, 0.1]          # Poolewe: weak city mass -> candidate
    pred = [{"start": 5, "end": 11, "category": "Name", "source": "model", "label": "PERSON"}]
    cands = candidates_for_note({"text": text, "spans": []}, pred, P, np.array(words), groups, tau=0.05)
    got = {(text[c["start"]:c["end"]], c["category"]) for c in cands}
    assert ("Reilly", "Name") in got and ("Poolewe", "Address_Location") in got
    assert all(not (c["start"] < 11 and 5 < c["end"]) for c in cands)      # never inside a prediction


def test_labels_cover_all_categories():
    assert len(LABELS) == 14


# ----------------------------------------------------------------------------- before / after
def test_before_after_drop_and_add():
    from deidconf.before_after import summarise
    text = "Pt John Smith seen by Dr Ann Lee at Leeds."
    note = {"note_id": "n1", "text": text,
            "gold_spans": [{"start": 3, "end": 13}, {"start": 25, "end": 32}],
            "predicted_spans": [{"start": 3, "end": 13, "conf_is_phi": 0.99, "verdict": "correct"},
                                {"start": 14, "end": 18, "conf_is_phi": 0.10, "verdict": "false alarm"},
                                {"start": 25, "end": 28, "conf_is_phi": 0.95, "verdict": "boundary off"}],
            "candidate_misses": [{"start": 29, "end": 32, "p_missed": 0.8, "is_real_miss": 1},
                                 {"start": 36, "end": 41, "p_missed": 0.1, "is_real_miss": 0}]}
    s = summarise([note])
    assert s["drop"]["spans_dropped"] == 1 and s["drop"]["true_spans_lost"] == 0
    assert s["before"]["false_alarms"] == 1 and s["after_drop"]["false_alarms"] == 0
    assert s["before"]["missed_gold_spans"] == 1 and s["after_add"]["missed_gold_spans"] == 0
    assert s["add"] == {"threshold": 0.5, "added": 1, "real_misses": 1}
    assert s["before"]["phi_recall"] == pytest.approx(13 / 17) and s["after_add"]["phi_recall"] == pytest.approx(16 / 17)
