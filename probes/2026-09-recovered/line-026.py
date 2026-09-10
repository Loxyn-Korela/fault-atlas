"""Fault Atlas probe — line 26 (form-026): strict homonyms.
August, corpus-wide: 1,215 surnames of 9,160 are borne by at least two different given names.
Per document, this probe returns the surnames shared by two different authors of the same article.
    python3 tools/run_probe.py probes/2026-09-recovered/line-026.py <dir with the 272 .xml>
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
import collections

@sonde(26, "two different people sharing a surname inside one document")
def d26(x):
    pairs = re.findall(r"(?s)<surname[^>]*>(.*?)</surname>\s*<given-names[^>]*>(.*?)</given-names>", x)
    by = collections.defaultdict(set)
    for s, g in pairs:
        by[_txt(s).strip()].add(_txt(g).strip())
    dup = {s: gs for s, gs in by.items() if len(gs) > 1 and s}
    return [f"{len(dup)} shared surnames, e.g. {s} borne by {sorted(gs)}" for s, gs in list(dup.items())[:1]]
