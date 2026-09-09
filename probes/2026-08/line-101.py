"""Fault Atlas probe — catalogue line 101 (form-101).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-101.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

MOTS_SUJETS = r'(?:patients?|participants?|subjects?|cases?|women|men|children|individuals)'

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

# ── 101 — l'effectif ne se lit nulle part : a = b + c ───────────────────────
def effectifs(x):
    t = _txt(x)
    v = re.findall(rf'(?i)\b(\d{{1,5}})\s+(?:\w+\s+){{0,2}}{MOTS_SUJETS}\b', t)
    v += re.findall(rf'(?i){MOTS_SUJETS}\s*[\(:=]?\s*n\s*=\s*(\d{{1,5}})', t)
    return sorted({int(n) for n in v if 1 < int(n) < 100000})

@sonde(101, "effectif obtenu par addition (a = b + c), écrit nulle part")
def d101(x):
    v = effectifs(x)
    if len(v) < 3:
        return []
    t = [f"{a}={b}+{c}" for a in v for i, b in enumerate(v) for c in v[i + 1:]
         if b + c == a and b != a and c != a]
    return sorted(set(t))[:5]
