"""Fault Atlas probe — catalogue line 79 (form-079).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-079.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(79, "notation scientifique dans les noms")
def d79(x):
    return sorted(set(re.findall(r'\b[A-Z][a-z]?(?:<sup>\d?[+-]</sup>|\d+[+-])', x)))[:5]
