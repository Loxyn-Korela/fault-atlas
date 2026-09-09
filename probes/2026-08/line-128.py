"""Fault Atlas probe — catalogue line 128 (form-128).
Question: is an acronym used repeatedly without ever being introduced as "long form (ACRONYM)", or introduced only by bare apposition ("NADPH, an important antioxidant")?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A carrier here is a document with at least one never-glossed acronym.
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-128.py <dir with the 272 .xml>
Result (re-run 2026-09-09): 240/272 use at least one all-capitals acronym twice or more without a parenthetical gloss (4,259 orphan acronyms); 143/272 carry a bare apposition. The excerpt quotes 214/272 with a stricter rule (three uses or more, and a stop list of common words) that was not kept in code. Both kept.
"""
import re, collections

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def corps(x):
    m = re.search(r'(?s)<body\b.*?</body>', x)
    return m.group(0) if m else ''

def txt(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))

ACRO = re.compile(r'\b([A-Z][A-Za-z0-9]{1,5})\b')
APPO = re.compile(r'\b([A-Z][A-Za-z0-9]{1,5}), (?:an?|the) [a-z]')

@sonde(128, "acronym never glossed by (ACRONYM); bare apposition")
def d128(x):
    t = txt(corps(x) or x)
    glosed = set(re.findall(r'\(([A-Z][A-Za-z0-9]{1,5})\)', t))
    counts = collections.Counter(ACRO.findall(t))
    orphans = sorted(a for a, n in counts.items() if n >= 2 and a not in glosed and a.isupper() and len(a) >= 2)
    if not orphans:
        return []
    out = [f"never glossed: {', '.join(orphans[:6])}"]
    ap = APPO.findall(t)
    if ap: out.append("bare apposition: " + ", ".join(sorted(set(ap))[:4]))
    return out
