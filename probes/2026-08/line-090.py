"""Fault Atlas probe — catalogue line 90 (form-090).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-090.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(90, "renvoi texte ↔ figure par étiquette")
def d90(x):
    return sorted(set(re.findall(r'<xref[^>]*ref-type="fig"[^>]*>([^<]{1,14})</xref>', x)))[:5]
