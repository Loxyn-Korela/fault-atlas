# Probes

A probe is the exact question asked of a corpus, kept verbatim so that anyone can ask it again.
It repairs nothing and decides nothing. It answers one thing: *is this fault here, and where?*

| directory | what | corpus | how to run |
|---|---|---|---|
| `2026-08/line-NNN.py` | one Python regex probe per catalogue line (form-NNN), extracted verbatim from the scripts of the August 2026 observation campaign (Loxyn) | the 272 Europe PMC JATS articles, `corpora/europe-pmc-jats-2023-2026-272.json` | `python3 tools/run_probe.py probes/2026-08/line-036.py <dir with the 272 .xml>` |
| `2026-08/line-064-arginine-titles.py` | corpus probe on the 3,642 PubMed abstracts of the origin observation of form-064 | `corpora/pubmed-arginine-pre1990-3642.json` | `python3 tools/run_probe.py … <corpus .md file>` |
| `2026-09/form-182-*.sparql`, `form-184-*.sparql` | SPARQL on the public Cellar endpoint | `corpora/observation-2026-09-eurlex.json` | `curl -G https://publications.europa.eu/webapi/rdf/sparql -H 'Accept: text/csv' --data-urlencode query@<file>` |
| `2026-09/form-185-format-by-era.sh` | three CELEX, three `Accept` headers | same | `sh probes/2026-09/form-185-format-by-era.sh` |
| `2026-09/form-183-dump-coverage.py` | stream inventory of the Publications Office dump (EU Login) | same | `python3 probes/2026-09/form-183-dump-coverage.py <dir with the three .zip>` |

Rules:

- **The file is the record.** Its header says the question, the command, the population and the answer it gave, dated. The form's `probes[]` entry repeats the figure and points to the file; the observation's `probe` field points to the same file.
- **A re-run is a new measurement, dated.** `tools/rerun_probes.py` writes it back into `probes[].result`; the excerpt keeps its own figure.
- **A probe is shown only when it finds the quoted figure again.** When the kept probe gives another figure than the note (`matches_excerpt: false`), the form says "to be shown" and nothing else; the probe waits here for a second reader to settle which rule the note used. No substitute probe with another figure is ever attached to a form.
- **Zero is a result.** A probe that finds no carrier on a corpus is attached under *measured absent in*, with the same file and the same date.
- **No model, no key, stdlib only** for the Python probes. The corpora themselves are not redistributed; their identifier lists are.

A probe that sounds on 100 % of a corpus is an alarm about the probe, not a discovery (line 140 and line 39 were corrected for that reason in August; the correction notes are kept in the files).
