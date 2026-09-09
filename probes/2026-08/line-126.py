"""Fault Atlas probe — catalogue line 126 (form-126).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-126.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _corps(x):
    m = re.search(r'(?s)<body\b[^>]*>(.*?)</body>', x)
    return m.group(1) if m else ''

def _txt(x):
    x = re.sub(r'(?s)<(front|back|ref-list)\b.*?</\1>', ' ', x)
    return re.sub(r'<[^>]+>', ' ', x)

# ── 126 · pseudo-code à double numérotation ────────────────────────────────
@sonde(126, "bloc d'algorithme / pseudo-code numéroté")
def d126(x):
    t = _txt(_corps(x))
    algo = re.findall(r'(?i)\bAlgorithm\s+\d+\b', t)
    mots = re.findall(r'(?im)^\s*\d{1,2}:\s|\b(?:Require|Ensure|end for|end while|end procedure)\b', t)
    balise = re.findall(r'<(?:preformat|code)\b[^>]*>', x)
    if algo or (mots and balise):
        return [f"Algorithm N ×{len(algo)}", f"mots-clés pseudo-code ×{len(mots)}", f"<preformat|code> ×{len(balise)}"]
    return []
