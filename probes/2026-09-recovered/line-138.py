"""Fault Atlas probe — line 138 (form-138): a mnemonic superscript that is not a power.
August: 9/272 carry a non-arithmetic lettered superscript, such as CD16^dim beside CD16^hi.
    python3 tools/run_probe.py probes/2026-09-recovered/line-138.py <dir with the 272 .xml>
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

@sonde(138, "a lettered superscript that means a category, not a power")
def d138(x):
    h = re.findall(r"([A-Za-z0-9]{2,10})<sup>([A-Za-z]{2,6})</sup>", _body(x))
    h = [(a, b) for a, b in h if b.lower() not in {"th", "st", "nd", "rd", "a", "b", "c"}]
    return [f"{len(h)} lettered superscripts, e.g. {a}^{b}" for a, b in h[:1]] if h else []
