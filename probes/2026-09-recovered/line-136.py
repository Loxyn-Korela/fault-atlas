"""Fault Atlas probe — line 136 (form-136): columns of different natures.
August: 124/272 carry a Funding / Competing interests / Acknowledgements block INSIDE <body>,
hence in the reading flow rather than in the end apparatus.
    python3 tools/run_probe.py probes/2026-09-recovered/line-136.py <dir with the 272 .xml>
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
ADMIN = re.compile(r"(?i)<title[^>]*>\s*(funding|competing interests?|conflicts? of interest|acknowledge?ments?|data availability)\s*</title>")

@sonde(136, "an administrative block sitting inside the body, in the reading flow")
def d136(x):
    h = ADMIN.findall(_body(x))
    return [f"{len(h)} administrative sections inside <body>, e.g. {h[0]}"] if h else []
