"""Fault Atlas probe — catalogue line 117 (form-117).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-117.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

@sonde(117, "article rétracté (marqué dans le document)")
def d117(x):
    return sorted(set(re.findall(
        r'(?i)<article-title[^>]*>([^<]{0,90}retract[^<]{0,60})</article-title>'
        r'|(?i)>(\s*retracted:?[^<]{0,60})<', x)[0] if False else
        [m for m in re.findall(r'(?i)(retraction of|this article has been retracted|<related-article[^>]*retracted[^>]*>)', x)]))[:3]
