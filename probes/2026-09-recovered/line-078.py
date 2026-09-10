"""Fault Atlas probe — line 78 (form-078): structured abstract in numbered points.
August: 0/272 abstracts start with a point number and 0/272 carry three numbered points. The
measurement is the ABSENCE, on this corpus.
    python3 tools/run_probe.py probes/2026-09-recovered/line-078.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r"(?s)<body\b.*?</body>", x); return m.group(0) if m else x
def _txt(x):
    return re.sub(r"<[^>]+>", " ", x)

@sonde(78, "an abstract written as numbered points")
def d78(x):
    m = re.search(r"(?s)<abstract\b.*?</abstract>", x)
    if not m: return []
    t = _txt(m.group(0)).strip()
    if re.match(r"^\s*1[.)]\s", t) and re.search(r"\b2[.)]\s.*\b3[.)]\s", t, re.S):
        return ["abstract written as numbered points"]
    return []
