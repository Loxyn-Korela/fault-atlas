"""Fault Atlas probe — catalogue line 88 (form-088).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-088.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(88, "entité collective")
def d88(x):
    """⚠️ RESSERRÉE le 08/08 : la 1re version captait « Neural Network » et
    « control group » — des termes techniques, pas des collectifs d'auteurs.
    On exige maintenant que le collectif figure comme AUTEUR ou soit cité comme tel."""
    dans_contrib = re.findall(r'<collab[^>]*>([^<]{4,80})</collab>', x)
    nomme = re.findall(
        r'\b((?:[A-Z][A-Za-z]{2,}\s){1,3}(?:Consortium|Collaboration|Study Group|Investigators|Trial Group|Working Group))\b',
        _txt(x))
    exclus = re.compile(r'(?i)neural|control|treatment|placebo|experimental|intervention')
    return sorted(set(v.strip() for v in dans_contrib + nomme if not exclus.search(v)))[:4]
