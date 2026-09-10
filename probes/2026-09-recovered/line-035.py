"""Fault Atlas probe — line 35 (form-035): the undated statement is the norm.
August, corpus-wide: 15,049 of the 16,411 body paragraphs (92 %) contain no year. Per document, this
probe returns the share of that document's body paragraphs that carry no four-digit year.
    python3 tools/run_probe.py probes/2026-09-recovered/line-035.py <dir with the 272 .xml>
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

@sonde(35, "most body paragraphs carry no year at all")
def d35(x):
    ps = re.findall(r"(?s)<p\b.*?</p>", _body(x))
    if not ps: return []
    sans = [p for p in ps if not re.search(r"\b(19|20)\d{2}\b", _txt(p))]
    return [f"{len(sans)}/{len(ps)} body paragraphs with no year"] if len(sans) > len(ps) // 2 else []
