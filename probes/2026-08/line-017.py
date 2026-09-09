"""Fault Atlas probe — catalogue line 17 (form-017).
Narrowed 2026-09-09 after independent review: the August probe listed every document's template (272/272); the fault is the template NOT declared, 2 files, which is what this probe returns now.
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
@sonde(17, "document template not declared (article-type missing or 'other')")
def d17(x):
    a = re.findall(r'<article\b[^>]*article-type="([^"]+)"', x)
    if not a:
        return ["no article-type on <article>"]
    if "other" in a:
        return ['article-type="other": the template is not declared']
    return []
