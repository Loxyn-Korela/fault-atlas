"""Fault Atlas probe — catalogue line 100 (form-100).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-100.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(100, "effectif écrit en toutes lettres")
def d100(x):
    return sorted(set(re.findall(
        r'(?i)\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty)[\s-]?'
        r'(?:\w+\s)?(?:patients?|subjects?|participants?|cases?|animals?|samples?)\b', _txt(x))))[:5]
