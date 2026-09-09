"""Fault Atlas probe — catalogue line 64 (form-064), origin observation.
Corpus: PubMed abstracts on arginine, published before 1990-01-01, harvested
2026-07-29 by efetch (3,642 records; see corpora/pubmed-arginine-pre1990-3642.json).
The corpus file is a Markdown list: one record per "## n. PMID x · year" heading,
the title in bold on the next line.

Question: how many titles are written in full capitals (a dated convention)?

Run:
    python3 tools/run_probe.py probes/2026-08/line-064-arginine-titles.py <corpus .md file>

Result: 234 of 3,642 titles carry no lower-case letter (232 of them from the 1960s).
The August 2026 note counted 184 with a rule that was not preserved; the figure
below is the one this probe gives, and it is the one to cite from now on.
"""
import re

CORPUS_PROBE = True
LINE = 64
TITLE = "title in full capitals (dated typographic convention)"

REC = re.compile(r'^## \d+\. PMID (\d+) · (\d{4})\n\*\*(.*?)\*\*', re.M)


def population(text):
    return len(REC.findall(text))


def probe(text):
    out = []
    for pmid, year, title in REC.findall(text):
        if re.search(r'[A-Z]', title) and not re.search(r'[a-z]', title):
            out.append(f"PMID {pmid} ({year}): {title}")
    return out
