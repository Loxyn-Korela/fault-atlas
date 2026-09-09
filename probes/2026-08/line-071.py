"""Fault Atlas probe — catalogue line 71 (form-071).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-071.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(71, "dates multiples du document")
def d71(x):
    d = re.findall(r'<date date-type="([^"]+)"|<pub-date[^>]*pub-type="([^"]+)"', x)
    v = sorted({a or b for a, b in d})
    return v if len(v) > 1 else []
