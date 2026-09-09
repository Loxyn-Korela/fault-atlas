"""Fault Atlas probe — catalogue line 77 (form-077).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-077.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 77 · DATE LOCALE AMBIGUË : jj-mm-aa dans le TEXTE, sans indication
# ⚠️ 1re version CORRIGÉE : « \d{2,4} » en 3e groupe attrapait « 7.5-20 % », « 5/10/20
#    years », « version 2.3.28 », « v1.6.20 » — 11 documents porteurs dont 7 de bruit.
#    On EXIGE une année à 4 chiffres et le MÊME séparateur deux fois. Prix payé, dit :
#    l'année à 2 chiffres (« 31-05-77 » du corpus 1977) n'est plus vue.
DATE_NUM = re.compile(r'(?<![\w/.\-])(\d{1,2})([-/.])(\d{1,2})\2((?:19|20)\d{2})(?![\d/.\-])')

def _corps(x):
    m = re.search(r'(?s)<body\b.*?</body>', x)
    return m.group(0) if m else ''

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(77, "date numérique ambiguë dans le corps du texte")
def d77(x):
    out = []
    for a, s, b, an in DATE_NUM.findall(_txt(_corps(x))):
        if 1 <= int(a) <= 12 and 1 <= int(b) <= 12:     # les DEUX lisibles comme mois
            out.append(f"{a}{s}{b}{s}{an}")
    return sorted(set(out))[:5]
