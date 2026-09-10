"""Fault Atlas probe — line 14 (form-014): entity typing.
August: 63/272 place a tagged <institution> next to a NAMED study or cohort, two entities of
different kinds side by side.
    python3 tools/run_probe.py probes/2026-09-recovered/line-014.py <dir with the 272 .xml>
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
STUDY = re.compile(r"\b((?:[A-Z][A-Za-z\-]+ ){1,4}(?:Study|Cohort|Trial|Survey|Registry))\b")

@sonde(14, "a tagged institution standing beside a named study or cohort")
def d14(x):
    if not re.search(r"<institution\b", x): return []
    h = STUDY.findall(_txt(_body(x)))
    return [f"institution tagged, and {len(h)} named studies in the body, e.g. {h[0]}"] if h else []
