"""Fault Atlas probe — catalogue line 116 (form-116): open peer-review furniture.
The observation of 2026-08-08 says: 5/272 articles carry named open peer-review furniture
(peer review file, reviewer report, editor's evaluation, eLife assessment).
    python3 tools/run_probe.py probes/2026-09-recovered/line-116.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
FURN = re.compile(r"(?i)(peer[- ]review file|reviewer report|editor'?s evaluation|eLife assessment)")

@sonde(116, "a signed editorial judgment carried inside the article")
def d116(x):
    h = FURN.findall(re.sub(r'<[^>]+>', ' ', x))
    return [f"{len(h)} pieces of review furniture, e.g. {h[0]}"] if h else []
