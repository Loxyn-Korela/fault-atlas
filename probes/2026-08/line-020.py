"""Fault Atlas probe — catalogue line 20 (form-020).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-020.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(20, "fait porté par la mise en page (ligne de tableau / liste de définitions)")
def d20(x):
    n_tr = len(re.findall(r'<tr\b', x))
    n_def = len(re.findall(r'<def-item\b', x))
    if n_tr + n_def == 0: return []
    ex = re.findall(r'<tr\b[^>]*>(.*?)</tr>', x, re.S)
    e = re.sub(r'\s+', ' ', _txt(ex[0]))[:60] if ex else ''
    return [f"tr×{n_tr} def-item×{n_def} | {e}"]
