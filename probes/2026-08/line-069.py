"""Fault Atlas probe — catalogue line 69 (form-069).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-069.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 69 · plusieurs documents dans un fichier ───────────────────────────────
@sonde(69, "plusieurs documents dans un même fichier")
def d69(x):
    s = re.findall(r'<sub-article\b[^>]*>', x)
    r = re.findall(r'<response\b[^>]*>', x)
    if len(s) + len(r) == 0: return []
    ty = re.findall(r'<sub-article\b[^>]*article-type="([^"]+)"', x)
    return [f"sub-article ×{len(s)} response ×{len(r)}", "types=" + ",".join(sorted(set(ty))[:4])]
