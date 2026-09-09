"""Fault Atlas probe — catalogue line 39 (form-039).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-039.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

ETATS = {'retracted-article', 'retraction-forward', 'corrected-article',
         'correction-forward', 'final-edited-article', 'updated-article', 'preprint'}

@sonde(39, "versions successives du même document")
def d39(x):
    """⚠️ RESSERRÉE le 08/08 après audit (143/272 → 39/272). Deux fautes de la 1re
    version : <article-version>1</article-version> (120 documents) n'est PAS une
    succession, et <pub-history> est présent dans 272/272 — une sonde à 100 % est
    une alarme de méthode. On ne garde que les liens désignant un AUTRE ÉTAT DU MÊME
    TEXTE : « companion » et « commentary-article » sont d'autres documents."""
    r = sorted(set(re.findall(r'related-article-type="([^"]+)"', x)) & ETATS)
    v = sorted({f"version={s.strip()}" for s in re.findall(r'<article-version[^>]*>([^<]*)', x)
                if s.strip() and s.strip() != '1'})
    return (r + v)[:5]
