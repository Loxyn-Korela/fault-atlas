"""Fault Atlas probe — catalogue line 93 (form-093).
Question: does the text carry a stamp added by a digitisation chain ("Downloaded from", "Electronic Library Service", "scanned by"...)?
Rewritten 2026-09-09 as a standalone probe from the August 2026 campaign script
(the original was an inline loop, one counter per line, same regexes).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-093.py <dir with the 272 .xml>
Result (re-run 2026-09-09): the regex matches 25/272 documents. The excerpt says 0/272 after reading the matches by hand: modern "Downloaded from" / "Published online by" are publisher lines, not digitisation stamps, and "scanned by the bare plate" (phys-PMC13257740) is a physics sentence. The probe gives the raw matches; the zero is a human reading of them. Both kept.
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

NUM = re.compile(r'(Electronic Library Service|Published online by|Downloaded from '
                 r'https?://|Provided by the [A-Z]|scanned by|This content downloaded)', re.I)

@sonde(93, "content added by the digitisation chain (raw regex matches)")
def d93(x):
    return sorted(set(NUM.findall(txt(x))))[:4]
