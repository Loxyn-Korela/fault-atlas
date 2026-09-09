"""Fault Atlas probe — catalogue line 89 (form-089).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-089.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(89, "attributions et affiliations complexes")
def d89(x):
    a = re.findall(r'<aff\b', x); c = re.findall(r'<contrib\b', x)
    return [f"{len(c)} auteurs · {len(a)} affiliations"] if len(a) > 3 and len(c) > 3 else []
