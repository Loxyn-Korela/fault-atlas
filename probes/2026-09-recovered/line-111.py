"""Fault Atlas probe — catalogue line 111 (form-111): forest plot as image.
The observation of 2026-08-08 says: 36/272 articles mention a "forest plot" and 28/272 mention it
inside a figure caption — the pooled result is a graphical object there, not a sentence.
    python3 tools/run_probe.py probes/2026-09-recovered/line-111.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d

@sonde(111, "the pooled result of a meta-analysis lives in a figure, not in a sentence")
def d111(x):
    caps = re.findall(r'(?s)<caption\b.*?</caption>', x)
    inside = [c for c in caps if re.search(r'(?i)forest\s*plot', re.sub(r'<[^>]+>', ' ', c))]
    return [f"forest plot named in {len(inside)} figure caption(s)"] if inside else []
