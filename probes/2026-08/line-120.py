"""Fault Atlas probe — catalogue line 120 (form-120).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-120.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(120, "running head / titre alternatif à initiales pointées")
def d120(x):
    alt = re.findall(r'<alt-title\b[^>]*>(.*?)</alt-title>', x, re.S)
    alt += re.findall(r'<subtitle\b[^>]*>(.*?)</subtitle>', x, re.S)
    out = []
    for a in alt:
        a = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', a)).strip()
        if re.search(r'\b[A-Z]\.\s?[A-Z]?\.?\s?[A-Z][a-zà-ÿ]+', a): out.append(a[:70])
    return out[:4]
