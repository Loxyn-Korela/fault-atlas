"""Fault Atlas probe — catalogue line 36 (form-036).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-036.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 36 · dates relatives ───────────────────────────────────────────────────
REL = (r'(?i)\b((?:the\s+)?(?:previous|preceding|following|next|last|past|coming)\s+'
       r'(?:year|month|week|decade|quarter|season|fiscal year|study period)s?'
       r'|(?:one|two|three|four|five|\d{1,2})\s+(?:years?|months?|weeks?|decades?)\s+(?:ago|earlier|later|before|after)'
       r'|(?:l\'|la\s+)?(?:année|annee)\s+(?:précédente|precedente|dernière|derniere|suivante)'
       r'|to\s?day|as of (?:today|writing)|at present|nowadays)\b')

def _txt(x):
    x = re.sub(r'(?s)<(front|back|ref-list)\b.*?</\1>', ' ', x)
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(36, "date relative (à résoudre contre la date du document)")
def d36(x):
    return sorted(set(m.strip() for m in re.findall(REL, _txt(x))))[:6]
