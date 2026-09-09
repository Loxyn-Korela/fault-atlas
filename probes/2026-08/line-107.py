"""Fault Atlas probe — catalogue line 107 (form-107).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-107.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(107, "plusieurs DOI")
def d107(x):
    d = re.findall(r'<article-id[^>]*pub-id-type="doi"[^>]*>([^<]+)', x)
    return d if len(d) > 1 else []
