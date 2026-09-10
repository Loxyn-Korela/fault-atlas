"""Fault Atlas probe — line 27 (form-027): a name-to-address bridge inside one affiliation tag.
August: 54/272 carry, in the SAME <aff>, the institution name AND its postal address.
    python3 tools/run_probe.py probes/2026-09-recovered/line-027.py <dir with the 272 .xml>
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

@sonde(27, "an affiliation tag carrying both an institution and a postal address")
def d27(x):
    hits = []
    for a in re.findall(r"(?s)<aff\b.*?</aff>", x):
        t = _txt(a)
        if re.search(r"(?i)\b(univ|hospital|institut|college|school|center|centre|department)\b", t) and \
           re.search(r"\b\d{4,6}\b", t):
            hits.append(re.sub(r"\s+", " ", t).strip()[:90])
    return [f"{len(hits)} affiliations, e.g. {hits[0]}"] if hits else []
