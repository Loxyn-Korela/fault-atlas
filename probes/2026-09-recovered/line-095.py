"""Fault Atlas probe — line 95 (form-095): the study type qualifies all its facts.
August: 90/272 abstracts explicitly name their design.
    python3 tools/run_probe.py probes/2026-09-recovered/line-095.py <dir with the 272 .xml>
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
DESIGN = re.compile(r"(?i)\b(randomi[sz]ed|double[- ]blind|placebo[- ]controlled|retrospective|prospective cohort|case[- ]control|cross[- ]sectional|meta[- ]analysis|systematic review)\b")

@sonde(95, "the abstract names the study design that qualifies every fact under it")
def d95(x):
    m = re.search(r"(?s)<abstract\b.*?</abstract>", x)
    if not m: return []
    h = DESIGN.findall(_txt(m.group(0)))
    return [f"design named in the abstract: {sorted(set(h))}"] if h else []
