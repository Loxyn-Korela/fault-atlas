"""Fault Atlas probe — line 19 (form-019): salience and distractors.
August: of the 75 articles carrying keywords, 163 of 523 keywords appear at most ONCE in the body.
Per document, this probe returns the keywords that the body barely uses.
    python3 tools/run_probe.py probes/2026-09-recovered/line-019.py <dir with the 272 .xml>
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

@sonde(19, "a declared keyword the body barely uses, beside one it repeats")
def d19(x):
    kws = [_txt(k).strip() for k in re.findall(r"<kwd\b[^>]*>(.*?)</kwd>", x, re.S)]
    kws = [k for k in kws if 3 < len(k) < 60]
    if not kws: return []
    t = _txt(_body(x)).lower()
    rare = [k for k in kws if t.count(k.lower()) <= 1]
    return [f"{len(rare)}/{len(kws)} keywords appear at most once in the body, e.g. {rare[0]}"] if rare else []
