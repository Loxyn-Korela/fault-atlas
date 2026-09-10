# Fault Atlas

[![DOI](https://zenodo.org/badge/1362563154.svg)](https://doi.org/10.5281/zenodo.22674547)

**A catalogue of observed fault forms in knowledge graphs built from documents — each with its provenance, the damage it causes in the graph, and the kind of truth that can judge it.**

Maintained by [Loxyn](https://loxyn.ai) (Korela), Lyon, France. Contact: contact@loxyn.ai.

> Status: version 0.1.0, public since 2026-09-09. Migrated from an internal catalogue observed in August 2026; every form is still `migrated_unreviewed` until a second reader validates it.

## Why

Knowledge-graph construction and repair are evaluated against benchmarks whose ground truth is written by the people who score. When a repair algorithm counts deletions because "no ground truth is available", it verifies the graph against its own constraints.

The Fault Atlas is the other half of an answer key: **the map of the forms a fault can take**, observed on real corpora, classified by the damage they cause in the graph. A repair that holds on one form of a damage may fail on another form of the same damage. The atlas is the test matrix that says which.

## What a record says

One JSON file per form, self-contained (`schema/form.schema.json`):

| field | meaning |
|---|---|
| `origin` | the organisation and campaign that contributed the form; every observation also names its observer and organisation |
| `damage` | what it does to the graph — one of seven: `MERGE`, `SPLIT`, `SPURIOUS_EDGE`, `MISSING`, `WRONG_VALUE`, `WRONG_LABEL`, `ANACHRONISM` (or `CORPUS_PARAMETER` when it is not a damage) |
| `layer` | where the form bites in the stack (pixel, reading, utterance, extraction, anchoring, resolution, schema, coherence, structure); the damage says what happens to the graph, the layer says where it starts |
| `class` | whether deterministic code cancels it (`DEFEATED`, `DEFEATED_IF_XML`), can abstain on it (`REFUSABLE`), cannot see it from inside (`SILENT_FALSE`), or whether it needs meaning (`IRREDUCIBLE`) |
| `seen` | where it was observed: corpus, document, date, observer, verbatim excerpt — and, when it was kept, the exact `probe` that produced the figures |
| `probes` | the exact question asked of the corpus, verbatim and re-runnable: a Python regex on one document, a SPARQL query on a public endpoint, a shell request with its headers; with the dated re-run figure and whether it is the figure the excerpt quotes |
| `specimens` | fabricated test cases **and counter-examples** — what a remedy must not touch |
| `prevention` | whether it can be cancelled before entering the graph, and the refusal clause |
| `repair` | whether a deletion-only repair can restore the truth — **classified by judgment, not measured**, until a bench measures it |
| `judgeable_by` | which kind of truth can judge it: by construction, an official registry, a curated database, the dated future, a closed world |
| `injection` | how a controlled corpus can fabricate it — nine text operations, or `IMAGE` when vision is required |
| `history` | every event, dated; nothing is ever deleted |

The file is the truth. Software reads it; software never completes it from memory.

## Current content

157 forms from three observation campaigns:

- **August 2026** — 113 forms on business documents, old PubMed abstracts and 272 Europe PMC JATS articles, two independent observers (agreement on the novel/variant boundary: 54 %). 26 catalogue lines were instrument or metric properties, not fault forms: `docs/out-of-scope-2026-08.json`.
- **September 2026** — 40 forms reported by a second, independent observer from the construction of a 40-million-record PubMed substrate (PubTator3, MeSH history, author keywords) and from four other corpora: OpenAlex, OpenAIRE, Wikidata, FAERS. Each carries its measurement file and date.
- **September 2026, EUR-Lex** — 4 forms measured by the collection session on the official Cellar registry and data dump (`corpora/observation-2026-09-eurlex.json`).

| damage | all layers | reaches the graph¹ |
|---|---|---|
| MISSING | 48 | 29 |
| WRONG_VALUE | 25 | 22 |
| SPURIOUS_EDGE | 19 | 13 |
| SPLIT | 22 | 17 |
| MERGE | 14 | 14 |
| WRONG_LABEL | 14 | 14 |
| ANACHRONISM | 8 | 7 |
| CORPUS_PARAMETER | 8 | 7 |
| **total** | **158** | **123** |

¹ Second reader's rule (Coralie Bagnol-Lebon, 2026-09-10): a form sits upstream of the graph only if **every** one of its layers is pixel or reading — columns, drop caps, scanned pages; one layer beyond them and it reaches a repairer. **No damage count is ever cited without its layer.** Said to Bonifati: of the 62 identity forms (MISSING and MERGE), 43 reach the graph, not 62. All of this is classified by judgment, not measured, until a bench measures it.

The 272 Europe PMC articles of the August observation are listed by PMC identifier in `corpora/europe-pmc-jats-2023-2026-272.json`, with the selection queries, the sha256 of each file as read on 2026-08-08 and the licence found in it; a frozen copy of the 267 redistributable files is prepared for Zenodo. There is no corpus page and no probes page on the site: each form links the documents where the fault sits and, folded, the code that found them and the record behind them. Every August form has `status: migrated_unreviewed` and every September form `status: proposed`. A second reader validates or contests each one before it becomes `validated`. Where a September form overlaps an August one, the `related` field says so; the novel/variant decision is the reader's, not the machine's.

## Eras

A form has a period of validity, and a bench that ignores it measures the wrong thing. Measured on
2026-08-08, 45 PDFs of 1957-1987 against 15 of 2023-2026, 174 pages, 9 publishers:

| | forms |
|---|---|
| **ancient documents only** — the difficulty is gone from current publishing | 6 (drop cap, gathering signature, the dot inside a unit, scans, the three PDF regimes, content added by digitisation) |
| **both eras** — behaves the same in 1957 and in 2026 | 19, and three of them are *worse* now: the fact in the figure, multiple dates, editorial metadata |
| **born with the modern era** — no ancestor at all | 14 (several DOIs, partial ORCID, structured abstract, pre-registration, forest plot as image, colour scale, absent supplementary material, author declarations, licence on page 1, open peer-review furniture, Crossmark badge, Unicode traps in native PDF, coloured hyperlinks, dotted running head) |
| **not settled** — the sample was too small | 1 |
| not recorded yet | 118 |

*A corpus built on the old would measure robustness to OCR — a skill current science never calls
for. A corpus built only on the modern would never exercise the six that are dead.*

One classification was **refuted, twice, on the same day**: the non-standard decimal separator was
declared dead on the 15 modern PDFs, then found alive in a 2023 West African journal (a French
abstract writing 10,6 % where its own English summary writes 10.6 %) and in a 2026 systematic
review (-1,97 on one line, -1.97 on the next, in the same table). The lesson is on the form:
fifteen modern PDFs were not enough to declare a convention dead.

## Rules

1. A form enters with a verbatim excerpt from a named corpus, or it is a hypothesis, not an observation.
2. Cases without a counter-example cannot be tested; the validator refuses them for validated forms.
3. A refuted form stays in the atlas, marked refuted, with the measurement that refuted it. A form measured absent from a corpus is a result.
4. The atlas records the **effect** of a remedy, never its mechanism. No implementation of any filter, guard or repair is published here.
5. No client document, no personal data. Specimens are forms and excerpts from public corpora.
6. The number of forms is not a quantity: two competent readers disagree on the novel/variant boundary. What is objective is the list of phenomena with their proof.

## Use

```
python3 tools/validate.py        # every record against the schema and the house rules
python3 tools/test_validate.py   # the validator proves itself on seven planted faults
python3 tools/build_sqlite.py    # fault-atlas.sqlite, a view for Datasette
python3 tools/build_site.py      # site/ — the public site, static HTML generated from the records
python3 tools/test_probes.py     # every probe loads, declares one question, runs without crashing
python3 tools/run_probe.py probes/2026-08/line-036.py <dir with the 272 .xml>   # re-ask one question of one corpus
python3 tools/rerun_probes.py <dir with the 272 .xml>                          # re-run all document probes, write the dated results back
datasette fault-atlas.sqlite --immutable fault-atlas.sqlite --metadata datasette-metadata.json   # browse locally
```

## Probes: re-finding what was seen

An observation says what was found and where; a probe says how to find it again. `probes/2026-08/` holds the 66 regex probes written during the August 2026 campaign on the 272 Europe PMC articles, one file per catalogue line, extracted verbatim from the campaign's scripts; `probes/2026-09/` holds the SPARQL queries, the shell request and the dump inventory of the EUR-Lex forms. Each probe file carries its question, the command to run it and the answer it gave on the date it was run. Re-runs are dated measurements: when a re-run figure differs from the figure the excerpt quotes, both are kept and the difference is said on the form (`matches_excerpt: false`), never adjusted. See `probes/README.md`.

## Review

A form enters as `migrated_unreviewed` (August catalogue) or `proposed` (September observers), and a second reader validates, contests or refutes it, in writing, with `tools/review.py`. Nothing is deleted: a contested form stays, marked contested, with the disagreement in its history.

State on 2026-09-10, after the second reader (Coralie Bagnol-Lebon) read the 62 identity forms (MISSING and MERGE) in full:

| | |
|---|---|
| validated | 43 |
| contested | 5 (form-030, form-041, form-160, form-164, and form-165 as a variant of form-163) |
| classified and returned for decision | 12 (form-143, 144, 150, 156, 157, 158, 163, 167, 170, 171, 173, 176: their `class` was `UNCLASSIFIED`; the first reader filled it with a prevention clause, the second reader has not yet decided) |
| not yet reviewed | 103 |

Two decisions the second reader reversed on her own second pass, both on truncated excerpts: form-127 (its result *is* the absence: "the ABSENCE is the measure") and form-078 (kept distinct from form-109, its modern form, because the atlas must separate the traps of the past from those of the present).

## Contribute

Met a form on your corpus? [Propose it](https://github.com/Loxyn-Korela/fault-atlas/issues/new?template=propose-form.yml) with its excerpt, corpus and date — no code needed. Or scaffold the record with `tools/new_form.py` and send it by pull request (see `CONTRIBUTING.md`). A second reader reviews. Disagreement is recorded, not erased. Nothing enters unreviewed.

## Citation and licence

Records and documentation: CC BY-SA 4.0. Tools: Apache 2.0. See `CITATION.cff`.

**One way to say the count**: 158 forms — 113 migrated from the August catalogue, 40 proposed by a second observer in September, 4 measured on EUR-Lex, 1 found by the human audit of the truth; 123 of them reach the graph. Second reader's decisions on the 62 identity forms (MISSING, MERGE), 2026-09-10: **43 validated**, 5 contested, 12 classified and sent back for decision.

Cite as: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). *Fault Atlas: observed fault forms in knowledge graphs built from documents.* Loxyn SAS, Lyon. Zenodo. https://doi.org/10.5281/zenodo.22674547 — this concept DOI always resolves to the latest version; each release has its own DOI on Zenodo.

## Team

Loxyn SAS, Lyon — Sébastien Gracia (technical direction, author of the instrument), Coralie Bagnol-Lebon (evaluation doctrine: closed question, cited proof, deferred mechanical verdict), Yoline Comtet (presidency). Co-authorship agreed by the three co-founders on 2026-09-09. Contact: contact@loxyn.ai.
