"""Fault Atlas probe — catalogue line 17 (form-017).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-017.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 17 · diversité des gabarits ────────────────────────────────────────────
@sonde(17, "gabarit du document (article-type JATS)")
def d17(x):
    a = re.findall(r'<article\b[^>]*article-type="([^"]+)"', x)
    s = re.findall(r'<sub-article\b[^>]*article-type="([^"]+)"', x)
    return sorted(set(a + s))
