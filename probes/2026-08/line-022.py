"""Fault Atlas probe — catalogue line 22 (form-022).
Question: does a sentence open on a bare pronoun (It / They / These / Those / This) whose referent must be resolved?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A carrier here is a document with a bare-pronoun sentence opening.
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-022.py <dir with the 272 .xml>
Result (re-run 2026-09-09): 212/272 documents open at least one sentence on a bare pronoun, 3,260 occurrences; 49/272 also carry an explicit lexical reprise ("the latter", "these authors"). Same figures as the excerpt.
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

REP_EN = re.compile(r'\b(the latter|the former|this group|these authors|the same '
                    r'(?:group|authors|patients?)|said (?:company|study))\b', re.I)
PRON_SUJ = re.compile(r'(?<=[.;] )(It|They|These|Those|This)\b')

@sonde(22, "pronominal reprise: a sentence opens on a bare pronoun")
def d22(x):
    t = txt(corps(x) or x)
    pro = PRON_SUJ.findall(t)
    rep = REP_EN.findall(t)
    if not pro:
        return []
    out = [f"pronoun-subject x{len(pro)}"]
    if rep: out.append("lexical reprise: " + " | ".join(sorted(set(rep))[:3]))
    return out
