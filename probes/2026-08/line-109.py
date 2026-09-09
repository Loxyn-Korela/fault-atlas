"""Fault Atlas probe — catalogue line 109 (form-109).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-109.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _resume(x):
    m = re.search(r'<abstract\b[^>]*>(.*?)</abstract>', x, re.S)
    return m.group(1) if m else ''

@sonde(109, "résumé structuré (rubriques nommées dans l'abstract)")
def d109(x):
    a = _resume(x)
    ti = [re.sub(r'<[^>]+>', '', t).strip()
          for t in re.findall(r'<sec\b[^>]*>\s*<title>(.*?)</title>', a, re.S)]
    ti = [t for t in ti if t]
    return ti[:6] if len(ti) >= 2 else []
