"""Fault Atlas probe — catalogue line 110 (form-110).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-110.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(110, "registre d'essai")
def d110(x):
    return sorted(set(re.findall(r'\b(NCT\d{8}|ISRCTN\d{8}|EUCTR\d{4}-\d{6}-\d{2})\b', x)))[:4]
