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

@sonde(103, "two significance markers defined with two different thresholds")
def d103(x):
    t = _plain(x)
    h = sorted(set(re.findall(r"(\*{1,3})\s*[Pp]\s*[<≤]\s*0?[.,]\d+", t)))
    return [f"{len(h)} distinct star markers with a threshold: {h}"] if len(h) > 1 else []
