"""Fault Atlas probe — catalogue line 121 (form-121).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-121.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 121 · FORMAT D'ACCÈS : quelle forme du document tient-on réellement ?
@sonde(121, "format d'accès au document (XML intégral / front seul / PDF)")
def d121(x):
    if x.lstrip().startswith('%PDF'):                     return ['PDF']
    if '<body' in x and '<sec' in x:                      return ['XML JATS intégral (body + sections)']
    if '<body' in x:                                      return ['XML JATS · body sans sections']
    if '<article' in x:                                   return ['XML JATS · front seul']
    return ['format non reconnu']
