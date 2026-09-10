"""Fault Atlas probe — form-187: a retraction notice carries the title of the article it withdraws.
Written 2026-09-10 from the August verdict on rare genres, and run on the retraction stratum of
the 272 Europe PMC articles.

Question: does the notice's own title repeat the title of the retracted article, so that an
extractor reading it produces exactly the fact being withdrawn? And does the notice record a
disagreement about its own conclusion?

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-187-retraction-carries-what-it-withdraws.py <dir with the 272 .xml>

Result (2026-09-10): of the 33 retraction notices in the corpus, 25 carry the withdrawn article's
title in their own title, and 9 record a disagreement ("do not agree with this retraction").
A carrier here is a notice whose title repeats the withdrawn one.
"""
import re

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip()

@sonde(187, "a retraction notice carries the title of the article it withdraws")
def d187(x):
    at = re.search(r'article-type="([^"]+)"', x)
    if not at or "retraction" not in at.group(1):
        return []
    m = re.search(r'(?s)<article-title[^>]*>(.*?)</article-title>', x)
    title = _txt(m.group(1)) if m else ""
    out = []
    if re.match(r'(?i)^(retraction|retracted|withdrawal)[:\s]', title) and len(title) > 40:
        out.append("the notice's title repeats the withdrawn title: " + title[:180])
    b = re.search(r'(?s)<body\b.*?</body>', x)
    if b and re.search(r'(?i)do(es)? not agree|disagree', _txt(b.group(0))):
        out.append("and it records a disagreement about its own conclusion")
    return out
