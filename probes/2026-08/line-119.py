"""Fault Atlas probe — catalogue line 119 (form-119).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-119.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(119, "hyperlien dont la COULEUR porte le type")
def d119(x):
    """⚠️ CORRIGÉE le 08/08 après audit. La 1re version trouvait 24/272 — c'étaient
    des style="background-color:#ccc" sur des CELLULES, pas sur des liens. On
    n'interroge plus que les liens eux-mêmes : 0/272. En JATS le type est porté par
    ref-type / ext-link-type (24 158 et 18 156 occurrences), donc EXPLICITE. La
    couleur est un fait de RENDU (PDF, HTML), absent de la source."""
    return sorted(set(re.findall(r'<(?:ext-link|xref)[^>]*(?:style|color)="[^"]*"', x)))[:4]
