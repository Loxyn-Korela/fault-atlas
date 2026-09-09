"""Fault Atlas probe — catalogue line 97 (form-097).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-097.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 97 · RÉGIMES DE PDF : il faut un flux PDF. Y en a-t-il un seul ?
@sonde(97, "régime de PDF (natif / OCR posé / image pure)")
def d97(x):
    return ['flux PDF présent'] if x.lstrip().startswith('%PDF') else []
