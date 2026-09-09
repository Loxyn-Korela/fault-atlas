"""Fault Atlas probe — catalogue line 76 (form-076).
Narrowed 2026-09-09 after independent review: the August regex also matched counts ("28 subjects"); only the capitalised label + ordinal that names an anonymised person is kept.
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-076.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(76, "anonymised entities (Patient 1, Case 2, Subject 3)")
def d76(x):
    # singular label + small ordinal, capitalised as a name: "Patient 1", "Case 2"; not "28 subjects" nor "patients 18"
    return sorted(set(re.findall(r'\b(?:Patient|Case|Subject|Participant)\s+(?:No\.?\s*)?\d{1,2}\b', _txt(x))))[:6]
