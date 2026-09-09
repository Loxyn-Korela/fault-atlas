"""Fault Atlas probe — catalogue line 83 (form-083).
Question: does a table carry its own definitions in its foot (<table-wrap-foot> with "XX = ..." or "XX: ...")?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-083.py <dir with the 272 .xml>
Result (re-run 2026-09-09): 180/272 carry a table, 128/272 a table foot, 47/272 define acronyms in a table foot. Same figures as the excerpt. A carrier here is a document whose table foot defines its acronyms.
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

@sonde(83, "the table carries its definitions in its foot")
def d83(x):
    pieds = re.findall(r'(?s)<table-wrap-foot\b.*?</table-wrap-foot>', x)
    out = []
    for p in pieds:
        m = re.search(r'\b[A-Z]{2,6}\b\s*[=:]', txt(p))
        if m:
            out.append(txt(p)[max(0, m.start()-10):m.start()+60].strip())
    return out[:5]
