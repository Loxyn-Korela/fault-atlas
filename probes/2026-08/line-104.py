"""Fault Atlas probe — catalogue line 104 (form-104).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-104.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _corps(x):
    m = re.search(r'(?s)<body\b[^>]*>(.*?)</body>', x)
    return m.group(1) if m else ''

# ── 104 · absence totale d'appareil ────────────────────────────────────────
@sonde(104, "absence d'appareil : ni résumé, ni mots-clés, ni section nommée")
def d104(x):
    res = bool(re.search(r'<abstract\b', x))
    kwd = bool(re.search(r'<kwd\b', x))
    corps = _corps(x)
    titres = re.findall(r'<title>([^<]{2,60})</title>', corps)
    manque = [n for n, v in (('résumé', res), ('mots-clés', kwd), ('titre de section', bool(titres))) if not v]
    return [f"manque: {', '.join(manque)}"] if len(manque) == 3 and corps else []
