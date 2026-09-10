"""Fault Atlas probe — line 127 (form-127): a structured object presented as a figure.
August: ZERO <code> or <preformat> blocks across the 272 articles. The measurement is the ABSENCE.
    python3 tools/run_probe.py probes/2026-09-recovered/line-127.py <dir with the 272 .xml>
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

@sonde(127, "a structured object carried as a code or preformatted block")
def d127(x):
    h = re.findall(r"<(code|preformat)\b", x)
    return [f"{len(h)} code or preformat blocks"] if h else []
