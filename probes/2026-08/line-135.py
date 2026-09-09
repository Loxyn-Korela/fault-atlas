"""Fault Atlas probe — catalogue line 135 (form-135).
Question: does the document carry a block quotation (<disp-quote>), and a marker that it is a translation ("our translation", "translated by")?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-135.py <dir with the 272 .xml>
Result (re-run 2026-09-09): 11/272 carry a block quotation (102 blocks); 1/272 carries a translation marker (phys-PMC13234180, "our translation"). Same figures as the excerpt. A carrier here is a document with a block quotation or a translation marker (11 + 1 = 12).
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

TRAD = re.compile(r'(?i)\b(translated (?:by|from)|our translation|translation (?:by|from|of) the authors?|\(translation\))\b')

@sonde(135, "verbatim quotation, possibly translated")
def d135(x):
    n = len(re.findall(r'<disp-quote\b', x))
    m = TRAD.findall(txt(x))
    out = [f"disp-quote x{n}"] if n else []
    if m: out.append("translation marker: " + ", ".join(sorted(set(m))))
    return out
