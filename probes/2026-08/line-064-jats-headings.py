"""Fault Atlas probe — catalogue line 64 (form-064), absence check on the 272 JATS files.
Question: does the dated convention (title in full capitals) survive in recent
Europe PMC articles? Three counts per document:
  A. the article title itself carries no lower-case letter
  B. at least one section heading (<title>) of four characters or more is in full capitals
  C. at least one word of four letters or more in the article title is in full capitals

Run:
    python3 tools/run_probe.py probes/2026-08/line-064-jats-headings.py <dir with the 272 .xml>

Result (re-run 2026-09-09): A = 0/272 — the convention is absent from the modern corpus.
The record's excerpt also quotes 70/272 for B and 30/272 for C, measured 2026-08-08
with a rule that was not preserved; this probe gives 36 and 36. Both figures are
kept, the discrepancy is stated, not hidden. A carrier here is a document with A.
"""
import re

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def _txt(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip()

def counts(x):
    m = re.search(r'(?s)<article-title[^>]*>(.*?)</article-title>', x)
    t = _txt(m.group(1)) if m else ''
    a = bool(t) and not re.search(r'[a-z]', t)
    heads = [_txt(h) for h in re.findall(r'(?s)<title[^>]*>(.*?)</title>', x)]
    b = [h for h in heads if len(h) >= 4 and re.search(r'[A-Z]', h) and not re.search(r'[a-z]', h)]
    c = [w for w in re.findall(r'[A-Za-z]{4,}', t) if w.isupper()]
    return a, b, c

@sonde(64, "article title in full capitals (dated convention)")
def d64(x):
    a, b, c = counts(x)
    return [f"title in full capitals"] if a else []
