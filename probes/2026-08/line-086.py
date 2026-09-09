"""Fault Atlas probe — catalogue line 86 (form-086).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-086.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(86, "un composé, plusieurs noms")
def d86(x):
    t = _txt(x)
    return sorted(set(re.findall(r'\b[A-Za-z][A-Za-z0-9-]{3,}\s*\((?:also known as|aka|CAS|[A-Z]{2,6}-?\d{2,6})\)', t)))[:4]
