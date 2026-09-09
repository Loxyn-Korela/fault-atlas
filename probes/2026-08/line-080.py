"""Fault Atlas probe — catalogue line 80 (form-080).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-080.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(80, "relations quantifiées relatives")
def d80(x):
    return sorted(set(re.findall(
        r'(?i)\b(\d+[\.,]?\d*[- ]?fold|\d+[\.,]?\d*\s*times (?:higher|lower|greater)|increased by \d+)', _txt(x))))[:5]
