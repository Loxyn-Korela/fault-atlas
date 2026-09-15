"""Fault Atlas probe — form-208: a claim attributed to another source, written as a fact.
Question: does the body of the article state, as a fact, something it attributes to someone else —
« X et al. reported that … », « it has been suggested that … », « according to … » — and, among
those, does the same article then contradict it (« however », « in contrast », « we found no … ») ?
The first is a reported claim; the second is the denial the generator's level 6 fabricates.
    python3 tools/run_probe.py probes/2026-09/form-208-reported-claim.py <dir with the 272 .xml>
Written 2026-09-15. No model, no network, stdlib only. Result on the day it was written: see the form.
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r"(?s)<body\b.*?</body>", x); return m.group(0) if m else ""
def _txt(x):
    x = re.sub(r"(?s)<xref[^>]*ref-type=\"bibr\"[^>]*>.*?</xref>", " [CIT] ", x)
    x = re.sub(r"(?s)<table-wrap\b.*?</table-wrap>|<fig\b.*?</fig>", " ", x)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))
ATTR = re.compile(r"(?i)(?:\bet al\.?|\[CIT\])[^.]{0,60}?\b(?:reported|showed|found|demonstrated|suggested|observed|concluded|proposed|claimed|described|noted|argued|hypothesi[sz]ed)\s+that\b[^.]{10,200}\.|"
                  r"(?i)\bit (?:has been|was) (?:reported|suggested|claimed|proposed|shown|argued|hypothesi[sz]ed) that\b[^.]{10,200}\.|"
                  r"(?i)\baccording to\b[^.]{3,60}\[CIT\][^.]{10,200}\.")
DENY = re.compile(r"(?i)^\s*(?:however|but|in contrast|contrary to|nevertheless|conversely)\b|(?i)\bwe (?:found|observed|detected) no\b|\bdid not (?:confirm|replicate|support|find)\b|\bnot (?:supported|confirmed|replicated) by\b")

@sonde(208, "a claim attributed to another source, written as a fact — and, when present, its denial in the same article")
def d208(x):
    t = _txt(_body(x))
    hits = []
    for m in ATTR.finditer(t):
        s = m.group(0).strip()
        nxt = t[m.end():m.end() + 220]
        tag = "denied: " if DENY.search(nxt) else ""
        hits.append(tag + s[:200])
    denied = [h for h in hits if h.startswith("denied: ")]
    return (denied[:2] + [h for h in hits if not h.startswith("denied: ")][:2]) if hits else []
