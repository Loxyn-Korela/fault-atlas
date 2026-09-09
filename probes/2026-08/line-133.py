"""Fault Atlas probe — catalogue line 133 (form-133).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-133.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

# ── 133 — le balisage fragmente ET DOUBLE le texte ──────────────────────────
# ⚠️ CORRIGÉE le 08/08 : la 1re version cherchait <annotation> TeX — 0 partout.
#    Le doublement réel de ce corpus passe par <alternatives> : la MÊME formule y
#    est écrite deux fois, une fois en <tex-math>, une fois en MathML (ou en image).
@sonde(133, "le balisage FRAGMENTE le symbole (MathML)")
def d133(x):
    """Ce que mesure la sonde : un symbole contigu à la lecture devient, une fois les
    balises retirées bêtement, plusieurs morceaux séparés par des espaces."""
    ex = []
    for b in re.findall(r'(?s)<(?:mml:)?math\b.{0,4000}?</(?:mml:)?math>', x):
        nu = re.sub(r'\s+', ' ', _txt(b)).strip()          # lecture naïve
        vrai = ''.join(re.findall(r'<(?:mml:)?m[ino]\b[^>]*>([^<]*)<', b))  # lecture assemblée
        if vrai and nu != vrai and len(nu.split()) > 1:
            ex.append(f"{len(b)}o : naïf {nu[:34]!r} ≠ assemblé {vrai[:34]!r}")
        if len(ex) >= 3:
            break
    return ex
