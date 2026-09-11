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

@sonde(23, "a letter/digit confusion inside a word: l/1, O/0, S/5")
def d23(x):
    t = _plain(x)
    h = re.findall(r"\b[A-Za-zÀ-ÿ]{2,}[01][A-Za-zÀ-ÿ]{2,}\b", t)
    h = [w for w in h if not re.search(r"(?i)^(h[01]|co[01]|p[01])", w)]
    return [f"{len(h)} words with a digit inside letters, e.g. {h[0]}"] if h else []
