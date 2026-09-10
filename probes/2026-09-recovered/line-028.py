"""Fault Atlas probe — line 28 (form-028): one person in two roles.
August: 39/272 have an AUTHOR of the article who is also an author of a cited reference.
    python3 tools/run_probe.py probes/2026-09-recovered/line-028.py <dir with the 272 .xml>
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

@sonde(28, "an author of the article is also an author of one of its references")
def d28(x):
    front = x.split("</front>")[0]
    back = x[x.find("<back"):] if "<back" in x else ""
    au = {_txt(s).strip().lower() for s in re.findall(r"<surname[^>]*>(.*?)</surname>", front) if len(_txt(s).strip()) > 2}
    rf = {_txt(s).strip().lower() for s in re.findall(r"<surname[^>]*>(.*?)</surname>", back)}
    both = sorted(au & rf)
    return [f"{len(both)} surnames both signing and cited, e.g. {both[0]}"] if both else []
