"""Fault Atlas probe — catalogue line 87 (form-087).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-087.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _corps(x):
    m = re.search(r'(?s)<body\b[^>]*>(.*?)</body>', x)
    return m.group(1) if m else ''

# ── 87 · unités et conventions mixtes ──────────────────────────────────────
FAMILLES = {
 'masse'  : r'\b\d+[\.,]?\d*\s*(?:µg|mcg|ug|mg|kg|ng|pg)\b',
 'volume' : r'\b\d+[\.,]?\d*\s*(?:mL|ml|µL|uL|cc|dL)\b',
 'molaire': r'\b\d+[\.,]?\d*\s*(?:mol|mmol|µmol|nmol|M|mM|µM|nM)\b',
 'pourcent': r'\d+[\.,]?\d*\s*%',
 'duree'  : r'\b\d+[\.,]?\d*\s*(?:s|min|h|hours?|minutes?|seconds?|days?|weeks?)\b',
 'temp'   : r'\b−?-?\d+[\.,]?\d*\s*°\s*C\b',
}

def _txt(x):
    x = re.sub(r'(?s)<(front|back|ref-list)\b.*?</\1>', ' ', x)
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(87, "unités mixtes : ≥3 familles de mesure dans le même corps")
def d87(x):
    t = _txt(_corps(x))
    trouv = {k: len(re.findall(p, t)) for k, p in FAMILLES.items()}
    pres = {k: v for k, v in trouv.items() if v >= 2}
    return [f"{k}×{v}" for k, v in sorted(pres.items(), key=lambda kv: -kv[1])] if len(pres) >= 3 else []
