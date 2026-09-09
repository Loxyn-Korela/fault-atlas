"""Fault Atlas probe — catalogue line 114 (form-114).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-114.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 114 — déclarations SUR LES AUTEURS (et non sur le sujet) ────────────────
TITRES_114 = (r'(?i)>\s*((?:competing|conflicts? of|conflict of) interests?|'
              r'authors?.{0,3} contributions?|contributorship statement|'
              r'data availability(?: statement)?|credit authorship[^<]{0,30}|'
              r'declarations? of (?:competing )?interests?)\s*<')

@sonde(114, "déclarations sur les auteurs (COI, contributions, données)")
def d114(x):
    v = re.findall(r'<fn[^>]*fn-type="(COI-statement|financial-disclosure|con)"', x)
    v += re.findall(r'<role[^>]*vocab="credit"[^>]*>([^<]{2,40})<', x)
    v += re.findall(TITRES_114, x)
    return sorted(set(s.strip() for s in v))[:6]
