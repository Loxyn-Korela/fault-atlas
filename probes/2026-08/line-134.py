"""Fault Atlas probe — catalogue line 134 (form-134).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-134.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 134 · page 1 non représentative ────────────────────────────────────────
@sonde(134, "notion de PAGE dans le XML (préalable à « page 1 non représentative »)")
def d134(x):
    p = re.findall(r'<(?:page|page-break|pb)\b[^>]*>', x)
    return [f"marqueurs de page ×{len(p)}"] if p else []
