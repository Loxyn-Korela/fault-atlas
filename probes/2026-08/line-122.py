"""Fault Atlas probe — catalogue line 122 (form-122).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-122.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 122 — équation numérotée en display, objet citable ──────────────────────
@sonde(122, "équation numérotée en display (objet citable)")
def d122(x):
    v = re.findall(r'(?s)<disp-formula\b.{0,6000}?</disp-formula>', x)
    lab = [m.group(1) for m in (re.search(r'<label>([^<]{1,12})</label>', b) for b in v) if m]
    return lab[:6]
