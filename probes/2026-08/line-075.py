"""Fault Atlas probe — catalogue line 75 (form-075).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-075.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(75, "conventions de citation multiples")
def d75(x):
    t = _txt(x)
    f = {'auteur-année': len(re.findall(r'\([A-Z][a-zà-ÿ]+(?: et al\.?)?,? \d{4}\)', t)),
         'numérique': len(re.findall(r'\[\d{1,3}(?:[,–-]\d{1,3})*\]', t)),
         'exposant': len(re.findall(r'<sup>\d{1,3}(?:[,–-]\d{1,3})*</sup>', x))}
    p = {k: v for k, v in f.items() if v > 2}
    return [f"{k}×{v}" for k, v in p.items()] if len(p) > 1 else []
