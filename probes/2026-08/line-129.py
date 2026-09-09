"""Fault Atlas probe — catalogue line 129 (form-129).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-129.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(129, "couverture de dépôt ajoutée devant l'article")
def d129(x):
    """⚠️ CORRIGÉE le 08/08 après audit. La 1re version trouvait 53/272 en captant
    « distributed under the terms of the Creative Commons » — une mention de LICENCE,
    pas une page de garde. Sur les marqueurs réels d'un dépôt : 0/272."""
    return sorted(set(re.findall(
        r'(?i)(to cite this version|hal id\s*:|archive ouverte|submitted on \d{1,2} '
        r'[a-z]{3}|this is a pdf file of an unedited manuscript)', _txt(x))))[:4]
