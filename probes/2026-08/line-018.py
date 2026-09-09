"""Fault Atlas probe — catalogue line 18 (form-018).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-018.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

CORPS = lambda x: re.search(r'(?s)<body\b.*?</body>', x)

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(18, "document trop long pour un seul morceau (2 000 car.)")
def d18(x):
    m = CORPS(x)
    if not m: return []
    t = re.sub(r'\s+', ' ', _txt(m.group(0))).strip()
    n = -(-len(t) // 2000)
    return [f"{len(t)} car. → {n} morceaux"] if n > 1 else []
