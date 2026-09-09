"""Fault Atlas probe — catalogue line 44 (form-044).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-044.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(44, "même contenu en DEUX langues dans le même document")
def d44(x):
    tt = re.findall(r'<trans-title[^>]*>', x)
    ta = re.findall(r'<trans-abstract[^>]*>', x)
    return ([f"trans-title ×{len(tt)}"] if tt else []) + ([f"trans-abstract ×{len(ta)}"] if ta else [])
