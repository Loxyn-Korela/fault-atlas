"""Fault Atlas probe — line 96 (form-096): methods as entities with a genealogy.
August: 6/272 name a method by its author, 3/272 in the canonical form.
    python3 tools/run_probe.py probes/2026-09-recovered/line-096.py <dir with the 272 .xml>
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
METH = re.compile(r"(?i)\b(?:method|technique|criteria|procedure)\s+(?:of|according to)\s+([A-Z][A-Za-z\-]+)")

@sonde(96, "a method named after the person it descends from")
def d96(x):
    h = METH.findall(_txt(_body(x)))
    return [f"{len(h)} methods named after a person, e.g. {h[0]}"] if h else []
