"""Fault Atlas probe — catalogue line 132 (form-132).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-132.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 132 · ZONE CLIQUABLE ≠ UNITÉ SÉMANTIQUE : l'année reste HORS du lien
# ⚠️ 1re version CORRIGÉE : elle cherchait « <xref>Nom</xref> (année) » — l'annexe
#    décrit ce sens-là (« le lien entoure Staiger and Stock et laisse (1997) dehors »).
#    Mesuré : 0/272. C'est le sens INVERSE qui existe en JATS — le lien n'entoure que
#    l'ANNÉE, et le nom d'auteur reste dehors. Même défaut, même conséquence sur
#    l'ancrage : la zone active n'est pas l'unité sémantique.
COUPEE = re.compile(r"([A-ZÀ-Þ][\w.'’\-]*(?:\s+(?:et\s+al\.?|and|&|[A-ZÀ-Þ][\w.'’\-]*)){0,4})"
                    r"\s*<xref[^>]*ref-type=\"bibr\"[^>]*>\s*\(?\s*((?:19|20)\d{2}[a-z]?)\s*\)?\s*</xref>")

@sonde(132, "zone cliquable qui coupe la citation (nom hors du <xref>)")
def d132(x):
    return [f"« {a.strip()} » DEHORS + <xref>{b}</xref>" for a, b in COUPEE.findall(x)][:5]
