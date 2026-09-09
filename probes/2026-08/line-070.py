"""Fault Atlas probe — catalogue line 70 (form-070).
Question: does the document carry a final reference block, and citation calls in its body?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-070.py <dir with the 272 .xml>
Result (re-run 2026-09-09): 251/272 carry a final <ref> block (10,912 references, median 36, max 450); 247/272 carry <xref ref-type="bibr"> calls (17,210); 13/272 carry an author-year citation in the running text. Same figures as the excerpt. A carrier here is a document with a reference block.
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

CIT_LIGNE = re.compile(r'\((?:[A-Z][A-Za-z\'’-]+(?: et al\.?| and [A-Z][A-Za-z-]+)?,? '
                       r'(?:19|20)\d\d[a-z]?)\)')

@sonde(70, "bibliographic references: final block, xref calls, inline author-year")
def d70(x):
    nref = len(re.findall(r'<ref\b', x))
    nxref = len(re.findall(r'<xref[^>]*ref-type="bibr"', x))
    ninline = len(CIT_LIGNE.findall(txt(corps(x) or x)))
    if not nref:
        return []
    return [f"ref x{nref}", f"xref bibr x{nxref}"] + ([f"inline author-year x{ninline}"] if ninline else [])
