"""Fault Atlas probe — catalogue line 14 (form-014), written 2026-09-09.
Question, taken literally from the observation's excerpt: does a sentence of the
body hold BOTH a tagged <institution> organisation AND a named study or cohort
("the Fremantle Diabetes Study", "the Brazilian Longitudinal Study") — two
confusable types side by side? And does the apposition that settles it
(", a multicenter …") appear?

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-014.py <dir with the 272 .xml>

Result (2026-09-09): 2/272 documents carry the two types in ONE sentence
(essai-PMC13280184, moderne-PMC13282721, both in a funding statement); 0/272 carry
the settling apposition. The excerpt quotes 63/272 and 9/272, counted in August by
code that was not saved. Looser rules do not recover 63 either: a tagged
<institution> plus a named study anywhere in the body gives 30, anywhere in the
file (references included) gives 59. The August rule is lost; the literal one is
published, with its own figure. A carrier here is a document with a same-sentence pair.
"""
import re

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

def txt(x):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip()

STUDY = re.compile(r'\b[Tt]he ((?:[A-Z][\w-]+ ){1,6}(?:Study|Cohort|Trial|Survey|Registry|Consortium|Project|Program|Programme))\b')
APPO = re.compile(r'(?:Study|Cohort|Trial|Survey|Registry)\b, (?:a|an) (?:[a-z-]+[ ,]){0,4}(?:multicent(?:er|re)|prospective|retrospective|population-based|cohort|randomi[sz]ed|longitudinal|national|cross-sectional)', re.I)

@sonde(14, "organisation and named study in the same sentence (confusable types)")
def d14(x):
    inst = {txt(i) for i in re.findall(r'(?s)<institution\b[^>]*>(.*?)</institution>', x)} - {''}
    body = re.search(r'(?s)<body\b.*?</body>', x)
    t = txt(body.group(0)) if body else ''
    out = []
    for sent in re.split(r'(?<=[.!?])\s+', t):
        m = STUDY.search(sent)
        if m and any(i in sent for i in inst):
            org = next(i for i in inst if i in sent)
            out.append(f"organisation «{org}» + study «{m.group(1)}» — {sent[:140]}")
    if out and APPO.search(t):
        out.append("settling apposition present: " + APPO.search(t).group(0))
    return out[:4]
