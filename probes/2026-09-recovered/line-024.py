"""Fault Atlas probe — catalogue line 24 (form-024): acronyms and abbreviations.
The observation of 2026-08-08 says: 224/272 articles carry at least one gloss "Full name (ACRONYM)",
2,104 glosses in all. This probe re-runs that count on the same corpus.
    python3 tools/run_probe.py probes/2026-09-recovered/line-024.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r'(?s)<body\b.*?</body>', x); return m.group(0) if m else x

@sonde(24, "a full name glossed by its acronym in parentheses")
def d24(x):
    t = re.sub(r'<[^>]+>', ' ', _body(x))
    g = re.findall(r'\b([A-Z][A-Za-z\-]+(?:\s+[a-z\-]+){0,4}\s+[A-Za-z\-]+)\s*\(([A-Z]{2,6})\)', t)
    g = [(full, ac) for full, ac in g if ac[0] in {w[0] for w in full.split()}]
    return [f"{len(g)} glosses, e.g. {full.strip()} ({ac})" for full, ac in g[:1]] if g else []
