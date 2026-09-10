#!/usr/bin/env python3
"""Fault Atlas probe — form-186: the official register asserts a relation that the
act's text never states (implicit repeal by expiry and replacement).

Two checks, both reproducible, no model:
  1. the register: Cellar says A repeals B  (SPARQL on the public endpoint)
  2. the text: the number of B never appears in the text of A on EUR-Lex; the text
     says instead that the earlier regime expires on a date and that A replaces it.

    python3 probes/2026-09/form-186-registry-relation-not-in-text.py 31999R0718 31995R2819

Result 2026-09-10 (found by a human auditor of the truth, fact f-477411 of audit-200):
  register: repeals = yes ; text of A (FR): "2819/95" 0 occurrence, "1995/2819" 0 occurrence ;
  the text says "le règlement (CEE) no 1101/89 … prend fin le 28 avril 1999".
"""
import sys, re, json, html, urllib.request, urllib.parse

UA = {"User-Agent": "Mozilla/5.0 (fault-atlas probe)"}


def register_says(a, b):
    q = f"""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
ASK {{ ?x cdm:resource_legal_id_celex "{a}"^^<http://www.w3.org/2001/XMLSchema#string> ; cdm:resource_legal_repeals_resource_legal ?y .
       ?y cdm:resource_legal_id_celex "{b}"^^<http://www.w3.org/2001/XMLSchema#string> . }}"""
    url = "https://publications.europa.eu/webapi/rdf/sparql?" + urllib.parse.urlencode({"query": q})
    r = urllib.request.Request(url, headers={"Accept": "application/sparql-results+json", **UA})
    return json.load(urllib.request.urlopen(r, timeout=120))["boolean"]


def text_of(celex, lang="FR"):
    h = urllib.request.urlopen(urllib.request.Request(f"https://eur-lex.europa.eu/legal-content/{lang}/TXT/?uri=CELEX:{celex}", headers=UA), timeout=120).read().decode("utf-8", "replace")
    body = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))


def keys(celex):
    m = re.match(r"^\d(\d{4})[A-Z]{1,2}(\d{3,4})", celex); year, num = m.group(1), int(m.group(2))
    return [f"{num}/{year}", f"{year}/{num}", f"{num}/{year[2:]}", f"{year[2:]}/{num}"]


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    print("register says A repeals B:", register_says(a, b))
    t = text_of(a)
    for k in keys(b):
        print(f"text of A, occurrences of {k!r}:", len(re.findall(r"(?<!\d)" + re.escape(k) + r"(?!\d)", t)))
    m = re.search(r"[^.]{0,160}prend fin[^.]{0,160}", t)
    print("what the text says instead:", m.group(0).strip() if m else "(not found)")
