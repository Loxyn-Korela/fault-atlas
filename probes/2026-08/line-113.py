"""Fault Atlas probe — catalogue line 113 (form-113).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-113.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

ATTACHE = re.compile(r'<(?:inline-)?supplementary-material\b|<media\b[^>]*xlink:href=')

# ── 113 · MATÉRIEL SUPPLÉMENTAIRE CITÉ, mais AUCUN fichier attaché
# ⚠️ 1re version CORRIGÉE deux fois. (a) elle ne comptait comme « attaché » que
#    xlink:href porté par <supplementary-material> — or le fichier pend souvent d'un
#    <media> imbriqué : 115/272 faux porteurs. (b) « supplementary material » nu, dans
#    la formule de disponibilité des données, n'est PAS la citation d'un objet : on
#    exige désormais un objet NOMMÉ (« Supplementary Fig. S1 », « S1 Table »).
CITE_SUP = re.compile(
    r'\b(?:[Ss]upplementary|[Ss]upplemental|[Ss]upporting)\s+'
    r'(?:[Tt]able|[Ff]igure|[Ff]ig\.?|[Ff]ile|[Dd]ataset|[Dd]ata|[Mm]aterial|'
    r'[Ii]nformation|[Mm]ovie|[Vv]ideo|[Aa]ppendix|[Nn]ote|[Mm]ethod)s?\s*(?:S\s?\d+|\d+)\b'
    r'|\bS\d+\s+(?:Table|Fig(?:ure)?|File|Appendix|Text|Data|Movie|Video)\b'
    r'|\b(?:Table|Fig(?:ure)?)\s*S\d+\b')

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(113, "objet supplémentaire NOMMÉ, cité, sans aucun fichier attaché")
def d113(x):
    cites = sorted({re.sub(r'\s+', ' ', m.group(0)).strip() for m in CITE_SUP.finditer(_txt(x))})
    return cites[:5] if cites and not ATTACHE.search(x) else []
