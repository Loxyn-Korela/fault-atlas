"""WITHDRAWN 2026-09-11 — form-108 is NOT universal, and this file records why.

A truncated ORCID cannot be told from a DOI suffix on the character stream alone. Run here, the
probe returned 4 of 272 and three of them were bibliography DOIs: 10.4085/1062-6050-0041.23,
10.1590/2317-6431-2021-2621pt, 10.1186/1687-6180-2012-86. The digits are identical in shape; what
separates them is knowing that one sits in an author block and the other in a reference list.
So this form needs the role of the passage, not just its characters. Kept as a negative result.

Fault Atlas probe — UNIVERSAL: it reads the character stream only.
It strips every tag before looking, so it runs on JATS, on a PubMed abstract, on OCR text from a
PDF, on an e-mail. If it needs a tag to see the fault, it does not belong in this folder.
    python3 tools/run_probe.py <this file> <dir of documents>
"""
import re, unicodedata
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _plain(x):
    """the document as characters, with no markup at all"""
    x = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", x)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))

@sonde(108, "an ORCID that is truncated: four groups expected, fewer or shorter found")
def d108(x):
    # the first version matched the PREFIX of every well-formed ORCID and returned 74/272 of pure
    # noise. A truncated ORCID is only a truncated ORCID when it is not part of a complete one.
    t = _plain(x)
    spans = [m.span() for m in re.finditer(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dXx]\b", t)]
    out = []
    for m in re.finditer(r"\b\d{4}-\d{4}-\d{4}(?:-\d{1,3})?\b", t):
        if any(a <= m.start() and m.end() <= b for a, b in spans):
            continue
        out.append(m.group(0))
    return [f"{len(out)} truncated ORCID-shaped strings, e.g. {out[0]}"] if out else []
