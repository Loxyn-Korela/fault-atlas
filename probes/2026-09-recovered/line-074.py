"""Fault Atlas probe — catalogue line 74 (form-074): content quoted from elsewhere.
The observation of 2026-08-08 says: 13/272 articles carry an explicit reuse signal
("reproduced with permission", "adapted from", "reprinted from").
    python3 tools/run_probe.py probes/2026-09-recovered/line-074.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
SIG = re.compile(r'(?i)(reproduced with permission|adapted from|reprinted from)')

@sonde(74, "a block explicitly reused from another document")
def d74(x):
    h = SIG.findall(re.sub(r'<[^>]+>', ' ', x))
    return [f"{len(h)} reuse signals, e.g. {h[0]}"] if h else []
