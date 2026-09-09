"""Fault Atlas probe — catalogue line 82 (form-082).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-082.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 82 — tableau en orientation paysage (propriété de mise en page) ─────────
@sonde(82, "tableau en orientation PAYSAGE")
def d82(x):
    o = re.findall(r'<(table-wrap|fig)\b[^>]*orientation="([^"]+)"', x)
    return [f"{b}:{v}" for b, v in o if v.lower() != 'portrait'][:6]
