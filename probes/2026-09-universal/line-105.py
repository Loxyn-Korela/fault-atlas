"""Fault Atlas probe — UNIVERSAL: it reads the character stream only.
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

@sonde(105, "an abbreviation dot INSIDE a unit: c.c., m.g., m.l. — not a unit ending a sentence")
def d105(x):
    # the dot must sit BETWEEN the letters of the unit. "cm." at the end of a sentence is a full
    # stop and not this fault: the first version of this probe counted 21 of those and was wrong.
    t = _plain(x)
    h = re.findall(r"(?<![A-Za-z.])(?:c\.c|m\.g|m\.l|c\.m|k\.g|m\.m)\.(?![A-Za-z])", t)
    return [f"{len(h)} units with an internal dot, e.g. {h[0]}"] if h else []
