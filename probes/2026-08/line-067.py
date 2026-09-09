"""Fault Atlas probe — catalogue line 67 (form-067).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-067.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 67 — document bilingue : la MÊME chose dite deux fois ───────────────────
@sonde(67, "document bilingue (traduction redondante déclarée)")
def d67(x):
    tr = re.findall(r'<trans-(abstract|title)\b[^>]*?xml:lang="([^"]+)"', x)
    if not tr:
        return []
    b = re.search(r'<article\b[^>]*xml:lang="([^"]+)"', x)
    return [f"{b.group(1) if b else '?'}→{lg} ({k})" for k, lg in tr][:6]
