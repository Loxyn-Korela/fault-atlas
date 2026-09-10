"""Fault Atlas probe — catalogue line 81 (form-081): equipment and supplier entities.
The observation of 2026-08-08 says: 57/272 articles carry in the body at least one parenthesised
supplier mention of the form "(… Ltd/Inc/GmbH/Corp/B.V./AG …)".
    python3 tools/run_probe.py probes/2026-09-recovered/line-081.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r'(?s)<body\b.*?</body>', x); return m.group(0) if m else x
SUP = re.compile(r'\(([^()]{0,80}?\b(?:Ltd|Inc|GmbH|Corp|B\.V\.|AG|Co\.|LLC)\b[^()]{0,80}?)\)')

@sonde(81, "a supplier named in parentheses beside a piece of equipment")
def d81(x):
    h = SUP.findall(re.sub(r'<[^>]+>', ' ', _body(x)))
    return [f"{len(h)} supplier mentions, e.g. ({h[0].strip()})"] if h else []
