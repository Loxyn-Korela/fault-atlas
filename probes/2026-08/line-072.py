"""Fault Atlas probe — catalogue line 72 (form-072).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-072.py <dir with the 272 .xml>
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

@sonde(72, "même valeur dite dans le texte ET dans un tableau")
def d72(x):
    """⚠️ RESSERRÉE DEUX FOIS le 08/08. Tous les nombres → « 10 », « 12 », « 13 » :
    du hasard. Décimales seules (107/272) → « 0.3 » tombait sur une borne d'IC ici
    et un temps de trajet là. Seuil retenu : ≥ 3 chiffres significatifs → 95/272,
    cas inspectés à la main, redondances réelles."""
    tw = re.findall(r'(?s)<table-wrap\b.*?</table-wrap>', x)
    if not tw: return []
    cell = set()
    for t in tw:
        cell |= {v for v in re.findall(r'<td[^>]*>\s*(?:<p[^>]*>\s*)?(\d+[.,]\d+)', t)
                 if len(re.sub(r'\D', '', v)) >= 3}
    if not cell: return []
    corps = re.sub(r'(?s)<table-wrap\b.*?</table-wrap>', ' ', x)
    m = CORPS(corps)
    if not m: return []
    txt = _txt(m.group(0))
    dans = sorted({c for c in cell if re.search(r'(?<![\d.,])' + re.escape(c) + r'(?![\d.,])', txt)})
    return [f"{len(dans)} valeurs communes : {dans[:5]}"] if dans else []
