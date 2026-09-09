"""Fault Atlas probe — catalogue line 66 (form-066).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-066.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 66 · MULTI-COLONNES : reste-t-il la moindre information de mise en page ?
@sonde(66, "mise en page multi-colonnes (info de colonnes HORS tableau)")
def d66(x):
    y = re.sub(r'(?s)<table-wrap\b.*?</table-wrap>', ' ', x)
    y = re.sub(r'(?s)<table\b.*?</table>', ' ', y)
    return sorted(set(re.findall(
        r'<(?:column|multicol|layout|column-break)\b[^>]*>'
        r'|\b(?:two|three|multi)[- ]columns?\b'
        r'|column-count\s*[:=]'
        r'|\bcolumn[- ]?(?:layout|order|width)\b', y, re.I)))[:4]
