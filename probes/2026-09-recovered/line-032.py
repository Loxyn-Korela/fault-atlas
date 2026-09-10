"""Fault Atlas probe — line 32 (form-032): a link asserted then cancelled.
August: 39/272 carry a successive version or a retraction.
    python3 tools/run_probe.py probes/2026-09-recovered/line-032.py <dir with the 272 .xml>
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

@sonde(32, "the document announces a later version or a retraction of itself")
def d32(x):
    h = []
    if re.search(r"(?i)<article-title[^>]*>[^<]*\b(retract|withdrawn)", x): h.append("retraction in the title")
    v = re.findall(r"(?i)<article-version[^>]*>([^<]+)<", x)
    h += [f"version={s.strip()}" for s in v]
    if re.search(r"(?i)<related-article[^>]*related-article-type=\"(retracted-article|corrected-article)\"", x):
        h.append("related-article says retracted or corrected")
    return h[:4]
