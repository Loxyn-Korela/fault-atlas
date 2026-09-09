"""Fault Atlas probe — catalogue line 131 (form-131).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-131.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _resume(x):
    m = re.search(r'<abstract\b[^>]*>(.*?)</abstract>', x, re.S)
    return m.group(1) if m else ''

@sonde(131, "mathématiques en display DANS le résumé")
def d131(x):
    a = _resume(x)
    d = re.findall(r'<disp-formula\b[^>]*>(.*?)</disp-formula>', a, re.S)
    if not d: return []
    tex = re.findall(r'<tex-math[^>]*>(.*?)</tex-math>', d[0], re.S)
    return [f"disp-formula×{len(d)} | {(tex[0] if tex else re.sub(r'<[^>]+>','',d[0]))[:60]}"]
