"""Fault Atlas probe — line 29 (form-029): entities that change identity.
August: 6/272 carry an identity-change phrase in the body.
    python3 tools/run_probe.py probes/2026-09-recovered/line-029.py <dir with the 272 .xml>
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
CHG = re.compile(r"(?i)\b(formerly (?:known as|called)|renamed|previously known as|merged with|acquired by)\b")

@sonde(29, "one entity said to have changed identity")
def d29(x):
    h = CHG.findall(_txt(_body(x)))
    return [f"{len(h)} identity-change phrases, e.g. {h[0]}"] if h else []
