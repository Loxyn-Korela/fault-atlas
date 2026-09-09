"""Fault Atlas probe — catalogue line 41 (form-041).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-041.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 41 · DOCUMENT TRONQUÉ : le texte intégral n'est pas là
# ⚠️ 1re version RETIRÉE : « <body> de moins de 300 mots » sonnait 29 fois, TOUTES
#    dans la strate `retract`. Un avis de rétractation COURT n'est pas un document
#    tronqué — c'est un genre bref. Une sonde concentrée à 100 % sur une strate est
#    une alarme de méthode. Restent ici les seules marques de troncature RÉELLES :
#    corps absent, renvoi interne dont la cible manque, bloc déclaré indisponible.
@sonde(41, "document tronqué (corps absent, cible interne manquante, bloc indisponible)")
def d41(x):
    marques = []
    if '<body' not in x:
        marques.append('AUCUN <body> — front-matter seul')
    ids = set(re.findall(r'\bid="([^"]+)"', x))
    rids = set()
    for r in re.findall(r'<xref[^>]*\brid="([^"]+)"', x):
        rids.update(r.split())
    pendants = sorted(rids - ids)
    if pendants:
        marques.append(f'renvoi interne SANS cible : {pendants[:3]}')
    if re.search(r'(?s)<table-wrap\b(?:(?!</table-wrap>).)*</table-wrap>', x):
        sans = [t for t in re.findall(r'(?s)<table-wrap\b.*?</table-wrap>', x) if '<table' not in t]
        if sans: marques.append('tableau livré sans contenu textuel')
    if re.search(r'(?i)\[(?:text|figure|image|table)s? (?:omitted|not available|unavailable)\]', x):
        marques.append('bloc déclaré manquant')
    return marques
