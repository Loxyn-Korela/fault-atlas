"""Fault Atlas probe — catalogue line 92 (form-092).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-092.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _corps(x):
    m = re.search(r'<body\b[^>]*>(.*?)</body>', x, re.S)
    return m.group(1) if m else ''

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(92, "lettrine — capitale isolée collée au mot suivant")
def d92(x):
    t = re.sub(r'\s+', ' ', _txt(_corps(x)))
    return sorted(set(re.findall(r'(?<![A-Za-z])([A-Z]) ([A-Z]{3,})\b', t)))[:5]
