"""Fault Atlas probe — catalogue line 94 (form-094): editorial metadata.
The observation of 2026-08-08 says: 89/272 articles carry a tagged <kwd> keyword block.
    python3 tools/run_probe.py probes/2026-09-recovered/line-094.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d

@sonde(94, "editorial metadata carried as tagged keywords")
def d94(x):
    k = re.findall(r'<kwd\b[^>]*>(.*?)</kwd>', x, re.S)
    return [f"{len(k)} tagged keywords, e.g. {re.sub(r'<[^>]+>', '', k[0]).strip()[:40]}"] if k else []
