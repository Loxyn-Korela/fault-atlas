"""Fault Atlas probe — catalogue line 115 (form-115).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-115.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _corps(x):
    m = re.search(r'(?s)<body\b[^>]*>(.*?)</body>', x)
    return m.group(1) if m else ''

# ── 115 · licence en page 1 ────────────────────────────────────────────────
LIC = (r'(?i)(creative commons|open access article|licensed under|'
       r'permits unrestricted use|http://creativecommons\.org|https://creativecommons\.org)')

def _txt(x):
    x = re.sub(r'(?s)<(front|back|ref-list)\b.*?</\1>', ' ', x)
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(115, "paragraphe de licence — dans <permissions> et/ou dans le corps")
def d115(x):
    perm = bool(re.search(r'<permissions\b', x))
    lic  = bool(re.search(r'<license\b', x))
    dans_corps = sorted(set(m.lower() for m in re.findall(LIC, _txt(_corps(x)))))[:3]
    if not (perm or lic or dans_corps): return []
    return [f"permissions={perm} license={lic}", f"dans le corps: {dans_corps or 'non'}"]
