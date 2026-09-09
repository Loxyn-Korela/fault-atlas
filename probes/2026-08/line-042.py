"""Fault Atlas probe — catalogue line 42 (form-042).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-042.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 42 — nom abîmé par le scan (OCR) ────────────────────────────────────────
# ⚠️ CORRIGÉE le 08/08 : la 1re version écrivait `<(?:…|institution)[^>]*>`, qui
#    attrapait AUSSI <institution-id> — et rendait « chiffre dans le nom » sur des
#    URL ROR (https://ror.org/02z1vqm45). 22/272 étaient donc 0 vrai positif.
#    Elle rendait aussi « lettre détachée » sur le « e » conjonctif portugais.
@sonde(42, "nom d'auteur abîmé par le scan (OCR)")
def d42(x):
    noms = re.findall(r'<(surname|given-names)(?:\s[^>]*)?>([^<]{2,60})<', x)
    ab = []
    for balise, n in noms:
        if '�' in n or 'ï¿½' in n or re.search(r'Ã[©¨¢«¤ -¿]', n):
            ab.append(f"mojibake:{balise}:{n}")
        elif re.search(r'[A-Za-zÀ-ÿ][01]|[01][A-Za-zÀ-ÿ]', n):
            ab.append(f"chiffre-dans-le-nom:{balise}:{n}")
        elif re.search(r'(?<=[a-zà-ÿ]) [a-zà-ÿ](?![a-zà-ÿ])', n):
            ab.append(f"lettre-detachee:{balise}:{n}")
    return sorted(set(ab))[:6]
