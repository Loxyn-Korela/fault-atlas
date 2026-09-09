"""Fault Atlas probe — catalogue line 106 (form-106).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-106.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

CORPS = lambda x: re.search(r'(?s)<body\b.*?</body>', x)

@sonde(106, "signature de cahier (chiffre nu isolé, artefact d'imprimerie)")
def d106(x):
    """⚠️ CORRIGÉE le 08/08 après audit. La 1re version trouvait 1/272 — et
    l'inspection a montré que ces « chiffres nus » étaient des CELLULES DE TABLEAU
    (<td><p>4</p></td> dans nonEN-PMC13267755). On retire tableaux, listes et
    figures : il reste 0/272. La signature de cahier est un artefact d'IMPRIMERIE,
    elle n'atteint pas le XML."""
    m = CORPS(x)
    if not m: return []
    b = re.sub(r'(?s)<table-wrap\b.*?</table-wrap>', ' ', m.group(0))
    b = re.sub(r'(?s)<(?:list|fig|disp-formula)\b.*?</(?:list|fig|disp-formula)>', ' ', b)
    p = re.findall(r'<p[^>]*>\s*(\d{1,3})\s*</p>', b)
    return [f"paragraphe = chiffre nu : {p[:5]}"] if p else []
