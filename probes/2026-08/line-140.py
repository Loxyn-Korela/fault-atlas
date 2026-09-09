"""Fault Atlas probe — catalogue line 140 (form-140).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-140.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(140, "statut éditorial imprimé (preprint, non relu)")
def d140(x):
    """⚠️ CORRIGÉE le 08/08 : la 1re version captait « pmc-prop-preprint », une
    métadonnée PMC présente dans 272/272 articles. Une sonde à 100 % est une
    alarme de méthode, pas une découverte. On retire d'abord le bloc custom-meta."""
    corps = re.sub(r'(?s)<custom-meta-group.*?</custom-meta-group>', ' ', x)
    corps = re.sub(r'(?s)<processing-meta.*?</processing-meta>', ' ', corps)
    return sorted(set(re.findall(
        r'(?i)\b(this is a preprint|not (?:been )?peer[- ]reviewed|author manuscript|'
        r'accepted manuscript|posted as a preprint)\b', _txt(corps))))[:4]
