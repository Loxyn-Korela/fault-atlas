"""Fault Atlas probe — catalogue line 43 (form-043).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-043.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 43 · tableaux à en-têtes multiples ─────────────────────────────────────
@sonde(43, "tableau à en-têtes sur plusieurs niveaux")
def d43(x):
    span = len(re.findall(r'<th[^>]*(?:col|row)span="([2-9]|\d\d)"', x))
    lignes_th = len(re.findall(r'(?s)<thead\b.*?</thead>', x))
    multi = 0
    for th in re.findall(r'(?s)<thead\b.*?</thead>', x):
        if len(re.findall(r'<tr\b', th)) > 1: multi += 1
    if span or multi:
        return [f"th colspan/rowspan ×{span}", f"thead à >1 ligne ×{multi}/{lignes_th}"]
    return []
