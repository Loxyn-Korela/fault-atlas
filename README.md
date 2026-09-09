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
| `damage` | what it does to the graph — one of seven: `MERGE`, `SPLIT`, `SPURIOUS_EDGE`, `MISSING`, `WRONG_VALUE`, `WRONG_LABEL`, `ANACHRONISM` (or `CORPUS_PARAMETER` when it is not a damage) |
| `class` | whether deterministic code cancels it (`DEFEATED`, `DEFEATED_IF_XML`), can abstain on it (`REFUSABLE`), cannot see it from inside (`SILENT_FALSE`), or whether it needs meaning (`IRREDUCIBLE`) |
| `seen` | where it was observed: corpus, document, date, observer, verbatim excerpt |
| `specimens` | fabricated test cases **and counter-examples** — what a remedy must not touch |
| `prevention` | whether it can be cancelled before entering the graph, and the refusal clause |
| `repair` | whether a deletion-only repair can restore the truth |
| `judgeable_by` | which kind of truth can judge it: by construction, an official registry, a curated database, the dated future, a closed world |
| `injection` | how a controlled corpus can fabricate it — nine text operations, or `IMAGE` when vision is required |
| `history` | every event, dated; nothing is ever deleted |

The file is the truth. Software reads it; software never completes it from memory.

## Current content

113 forms from the August 2026 observation campaign (81 real documents, then 272 Europe PMC JATS articles, two independent observers — agreement on the novel/variant boundary: 54 %). 26 catalogue lines were instrument or metric properties, not fault forms: `docs/out-of-scope-2026-08.json`.

| damage | forms |
|---|---|
| MISSING | 33 |
| WRONG_VALUE | 17 |
| SPURIOUS_EDGE | 17 |
| SPLIT | 14 |
| MERGE | 10 |
| WRONG_LABEL | 9 |
| ANACHRONISM | 5 |
| CORPUS_PARAMETER | 8 |

Every form has `status: migrated_unreviewed`. A second reader validates or contests each one before it becomes `validated`.

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
datasette fault-atlas.sqlite --immutable fault-atlas.sqlite --metadata datasette-metadata.json   # browse locally
```

## Contribute

Propose a form by pull request: one JSON file, the excerpt, the corpus, the date. A second reader reviews. Disagreement is recorded, not erased.

## Citation and licence

Records and documentation: CC BY-SA 4.0. Tools: Apache 2.0. See `CITATION.cff`.

Cite as: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). *Fault Atlas: observed fault forms in knowledge graphs built from documents.* Loxyn SAS, Lyon. Zenodo. https://doi.org/10.5281/zenodo.22674547 — this concept DOI always resolves to the latest version; each release has its own DOI on Zenodo.

## Team

Loxyn SAS, Lyon — Sébastien Gracia (technical direction, author of the instrument), Coralie Bagnol-Lebon (evaluation doctrine: closed question, cited proof, deferred mechanical verdict), Yoline Comtet (presidency). Co-authorship agreed by the three co-founders on 2026-09-09. Contact: contact@loxyn.ai.
