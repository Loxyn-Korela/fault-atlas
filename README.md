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
| `seen` | where it was observed: corpus, document, date, observer, verbatim excerpt |
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

| damage | all layers | graph layers only¹ |
|---|---|---|
| MISSING | 47 | 11 |
| WRONG_VALUE | 25 | 13 |
| SPURIOUS_EDGE | 19 | 3 |
| SPLIT | 22 | 17 |
| MERGE | 14 | 12 |
| WRONG_LABEL | 14 | 9 |
| ANACHRONISM | 8 | 6 |
| CORPUS_PARAMETER | 8 | 4 |
| **total** | **157** | **75** |

¹ Graph layers: resolution, schema, coherence, structure — where the phenomenon is itself a graph damage. The other layers (pixel, reading, utterance, extraction, anchoring) are reading failures whose effect reaches the graph downstream. The two counts are always given together. Deletion-only repair fully addresses one damage (spurious edge: 3 forms in graph layers); the identity damages (merge, split: 29) it never touches. All of this is classified by judgment, not measured, until a bench measures it.

The 272 Europe PMC articles of the August observation are listed by PMC identifier, with the harvest queries, in `corpora/europe-pmc-jats-2023-2026-272.json`: anyone can re-download them. Every August form has `status: migrated_unreviewed` and every September form `status: proposed`. A second reader validates or contests each one before it becomes `validated`. Where a September form overlaps an August one, the `related` field says so; the novel/variant decision is the reader's, not the machine's.

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
datasette fault-atlas.sqlite --immutable fault-atlas.sqlite --metadata datasette-metadata.json   # browse locally
```

## Review

A second reader records a decision with `tools/review.py` (validated, variant, contested, refuted), dated and signed, in the form's history. See `REVIEWING.md`.

## Contribute

Met a form on your corpus? [Propose it](https://github.com/Loxyn-Korela/fault-atlas/issues/new?template=propose-form.yml) with its excerpt, corpus and date — no code needed. Or scaffold the record with `tools/new_form.py` and send it by pull request (see `CONTRIBUTING.md`). A second reader reviews. Disagreement is recorded, not erased. Nothing enters unreviewed.

## Citation and licence

Records and documentation: CC BY-SA 4.0. Tools: Apache 2.0. See `CITATION.cff`.

**One way to say the count**: 157 forms — 113 migrated from the August catalogue (`migrated_unreviewed`), 40 proposed by a second observer in September and 4 measured on EUR-Lex (`proposed`); 75 of them in graph layers. Validated: 0, until the second reader's decisions are recorded.

Cite as: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). *Fault Atlas: observed fault forms in knowledge graphs built from documents.* Loxyn SAS, Lyon. Zenodo. https://doi.org/10.5281/zenodo.22674547 — this concept DOI always resolves to the latest version; each release has its own DOI on Zenodo.

## Team

Loxyn SAS, Lyon — Sébastien Gracia (technical direction, author of the instrument), Coralie Bagnol-Lebon (evaluation doctrine: closed question, cited proof, deferred mechanical verdict), Yoline Comtet (presidency). Co-authorship agreed by the three co-founders on 2026-09-09. Contact: contact@loxyn.ai.
