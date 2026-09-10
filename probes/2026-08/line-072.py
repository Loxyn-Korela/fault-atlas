"""Fault Atlas probe — catalogue line 72 (form-072): the same value stated in the text AND in a table.

Recovered on 2026-09-10 from the internal probe workshop of 2026-08-08
(atelier-filtres/sondes-vague3.py, sonde 72), and re-run here on the declared corpus. The threshold
is the workshop's own, twice narrowed on 2026-08-08 and written down there: every number gives
"10", "12", "13", which is chance; decimals alone put an interval bound next to a travel time. A
value counts only with at least three significant digits, and the carriers were then read by hand.

A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-072.py <dir with the 272 .xml>
"""
import re

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

def _corps(x):
    return re.search(r'(?s)<body\b.*?</body>', x)


# ── 72 · redundancy between the running text and a table ───────────────────
@sonde(72, "the same value stated in the running text and in a table")
def d72(x):
    tw = re.findall(r'(?s)<table-wrap\b.*?</table-wrap>', x)
    if not tw:
        return []
    cell = set()
    for t in tw:
        cell |= {v for v in re.findall(r'<td[^>]*>\s*(?:<p[^>]*>\s*)?(\d+[.,]\d+)', t)
                 if len(re.sub(r'\D', '', v)) >= 3}
    if not cell:
        return []
    body = _corps(re.sub(r'(?s)<table-wrap\b.*?</table-wrap>', ' ', x))
    if not body:
        return []
    txt = _txt(body.group(0))
    shared = sorted({c for c in cell if re.search(r'(?<![\d.,])' + re.escape(c) + r'(?![\d.,])', txt)})
    return [f"{len(shared)} values in both: {shared[:5]}"] if shared else []
