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

@sonde(125, "a numbered theorem whose body carries the claim")
def d125(x):
    t = _plain(x)
    h = re.findall(r"(?i)\b(Theorem|Lemma|Proposition|Corollary)\s+\d{1,2}\s*[.:]", t)
    return [f"{len(h)} numbered statements, e.g. {h[0]}"] if h else []
