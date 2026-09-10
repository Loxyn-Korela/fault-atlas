"""Fault Atlas probe — line 137 (form-137): three kinds of number in one string.
August: 48/272 carry a tagged <sub> chemical index.
    python3 tools/run_probe.py probes/2026-09-recovered/line-137.py <dir with the 272 .xml>
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

@sonde(137, "a subscript digit that is a chemical index, not a quantity")
def d137(x):
    h = re.findall(r"([A-Z][a-z]?)<sub>(\d{1,2})</sub>", _body(x))
    return [f"{len(h)} subscript indices, e.g. {a}{b}" for a, b in h[:1]] if h else []
