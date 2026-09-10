"""Fault Atlas probe — line 63 (form-063): the title carries the fact.
August: 197/272 titles carry at least two capitalised tokens or acronyms, hence at least two
entities and a relation stated only in the title.
    python3 tools/run_probe.py probes/2026-09-recovered/line-063.py <dir with the 272 .xml>
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

@sonde(63, "the title alone carries two entities and the relation between them")
def d63(x):
    m = re.search(r"(?s)<article-title[^>]*>(.*?)</article-title>", x)
    if not m: return []
    t = _txt(m.group(1)).strip()
    toks = re.findall(r"\b([A-Z][A-Za-z\-]{2,}|[A-Z]{2,6})\b", t)
    toks = [w for w in toks if w.lower() not in {"the","and","for","with","from","this","that"}]
    return [f"{len(toks)} capitalised tokens in the title: {toks[:4]}"] if len(toks) >= 2 else []
