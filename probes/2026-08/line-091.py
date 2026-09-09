"""Fault Atlas probe — catalogue line 91 (form-091).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-091.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

CORPS = lambda x: re.search(r'(?s)<body\b.*?</body>', x)

REL = re.compile(r'(?i)\b('
    r'\d+\s*(?:min|minutes?|hours?|days?|weeks?|months?|years?)\s+(?:later|earlier|after|before|from)'
    r'|(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,3})\s+'
    r'(?:minutes?|hours?|days?|weeks?|months?|years?)\s+(?:later|earlier|previously|after|before)'
    r'|on day \d{1,2}|at (?:day|week|month) \d{1,2}'
    r'|the (?:next|following|previous) (?:day|week|month|year|morning|evening)'
    r'|(?:shortly|soon|immediately) (?:after|before)'
    r'|thereafter|subsequently|from the onset|since the onset|prior to (?:admission|onset)'
    r')\b')

def _txt(x):
    """texte brut d'un XML JATS, balises retirées"""
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(91, "chronologie RELATIVE dense (≥8 repères, presque pas de dates)")
def d91(x):
    m = CORPS(x)
    if not m: return []
    t = _txt(m.group(0))
    rel = REL.findall(t)
    abs_ = re.findall(r'\b(?:19|20)\d{2}\b|\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b', t)
    return [f"{len(rel)} repères relatifs / {len(abs_)} dates absolues : {sorted(set(rel))[:4]}"] \
        if len(rel) >= 8 and len(rel) > len(abs_) else []
