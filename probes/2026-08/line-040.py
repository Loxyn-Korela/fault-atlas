"""Fault Atlas probe — catalogue line 40 (form-040).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-040.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(40, "renvoi interne pendant (xref sans cible dans le document)")
def d40(x):
    ids = set(re.findall(r'\bid="([^"]+)"', x))
    pend = []
    for m in re.finditer(r'<xref\b([^>]*)>', x):
        at = m.group(1)
        r = re.search(r'rid="([^"]+)"', at)
        if not r: continue
        for cible in r.group(1).split():
            if cible not in ids: pend.append(cible)
    return sorted(set(pend))[:6]
