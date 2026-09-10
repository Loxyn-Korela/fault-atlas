"""Fault Atlas probe — catalogue line 31 (form-031): degree of assertion of a link.
The observation of 2026-08-08 says: 233/272 articles carry at least one non-assertion marker
(may, might, could, suggests, appears to, likely, has been proposed), 4,518 occurrences in all.
    python3 tools/run_probe.py probes/2026-09-recovered/line-031.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r'(?s)<body\b.*?</body>', x); return m.group(0) if m else x

MARK = re.compile(r'(?i)\b(may|might|could|suggests?|appears? to|likely|has been proposed)\b')

@sonde(31, "a link stated with a hedge rather than asserted")
def d31(x):
    hits = MARK.findall(re.sub(r'<[^>]+>', ' ', _body(x)))
    return [f"{len(hits)} hedges, e.g. {hits[0]}"] if hits else []
