"""Fault Atlas probe — catalogue line 84 (form-084).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-084.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(84, "cellules non atomiques")
def d84(x):
    c = re.findall(r'<td[^>]*>([^<]{2,40})</td>', x)
    nn = [v for v in c if re.match(r'^\s*[\d.,]+\s*[(±]\s*[\d.,]', v) or ' / ' in v]
    return nn[:5]
