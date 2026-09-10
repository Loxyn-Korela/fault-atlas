"""Fault Atlas probe — line 34 (form-034): two neighbouring-type formulations for one funding fact.
August: 19/272 carry "funded by" AND "supported by" in the same article.
    python3 tools/run_probe.py probes/2026-09-recovered/line-034.py <dir with the 272 .xml>
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

@sonde(34, "two different verbs for the same funding relation, in one document")
def d34(x):
    t = _txt(x)
    a = re.search(r"(?i)\bfunded by\b", t)
    b = re.search(r"(?i)\bsupported by\b", t)
    return ["both 'funded by' and 'supported by' in the same article"] if a and b else []
