"""Fault Atlas probe — catalogue line 85 (form-085).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-085.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(85, "séparateur décimal — LES DEUX dans le même document")
def d85(x):
    t = _txt(x)
    virg = re.findall(r'\b\d+,\d\b', t); pt = re.findall(r'\b\d+\.\d\b', t)
    return [f"virgule: {virg[:3]}", f"point: {pt[:3]}"] if virg and pt else []
