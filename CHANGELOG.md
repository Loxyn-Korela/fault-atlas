# Changelog

## 0.1.0 — 2026-09-09
- Schema `form.schema.json` (record of truth: damage, class, seen, specimens, prevention, repair, judgeable_by, history).
- 113 forms migrated from the internal catalogue of 2026-08-09 (`korela.db`), all `migrated_unreviewed`; 26 lines set out of scope.
- Classification by damage and injection done line by line on 2026-09-09 (`docs/VERIFICATION-2026-09-09.md`); judgment, not measurement.
- Validator with house rules; proves itself on seven planted faults.
- SQLite view builder for Datasette.

## 0.3.0 — 2026-09-09
- The exact probe on each observation (third reader's request: "which corpus and which exact query finds the problem, not something general"). `probes/2026-08/`: the 66 regex probes of the August campaign, one file per catalogue line, extracted verbatim and re-run on the same 272 files today; `probes/2026-09/`: the two SPARQL queries, the shell request and the dump inventory of the EUR-Lex forms, all re-run live today and reproducing the collector's figures. Schema: `probes[]` on the form, `probe` on the observation.
- Re-run figures published as measured: 38 of 66 August probes give exactly the figure quoted in the excerpt; 28 do not (finer hand-run counts whose code was not kept) and say so on the form. Zero counts attached under "measured absent in" (17 forms).
- form-064 corrected: its origin observation is restored on its own corpus, the 3,642 PubMed abstracts on arginine before 1990, now published by PMID (`corpora/pubmed-arginine-pre1990-3642.json`) with a probe (234 titles in full capitals; the August note said 184 with a rule not kept). The 272-file check stays as a second, absence observation.
- form-182 and form-184 widened by live queries on the whole Cellar graph: the empty CELEX URI is the object of 8,164 triples under 14 predicates; the sentinel date 1003-03-03 sits on 351 works, 80 with a CELEX.
- Tools: `run_probe.py`, `rerun_probes.py`, `test_probes.py`; validator checks that every cited probe exists, sits in the form's list and names a known corpus (three more planted faults, 10/10 caught).
- Site: "Exact probe" block under each observation with the code, the command, the re-run figure and whether it matches; `probes.html`; Datasette table `probes`; build date in the footer.

## 0.2.3 — 2026-09-09
- Four forms measured on EUR-Lex / Cellar by the collection session (form-182 to form-185) and the collection's corpus record with its pre-registered bets.
- Two counts, always together: all layers and graph layers only, on the home cards and in the README.
- The corpus is visible up front: 'Seen on' under each title, a 'Seen on' column in the list, the corpus name first on each observation; observation links name the reproducible list they point to; three wrongly linked observations unlinked.

## 0.2.2 — 2026-09-09
- Second reader's first pass (Coralie Bagnol-Lebon): eight MISSING/MERGE forms had no excerpt — their August observations (wave-1 PDFs, non-biomedical wave) transcribed from the annexes and the journal; three remain without measurement (form-030, form-041, form-164), for the reader to mark contested.
- Wording: `repair.reachable_by_deletion` is a classification by judgment, not a measurement — said on every record, on every page and in the README.
- Each record also served as JSON on the site (`forms/<id>.json`); exact source-file link on GitHub.
- Layer filter on the list; 'Layers' explained: the damage says what happens to the graph, the layer says where it starts.
- One way to say the count: 153 = 113 migrated + 40 proposed; validated 0.

## 0.2.1 — 2026-09-09
- Reproducibility: the 272 Europe PMC articles of the August observation published by PMC identifier with the harvest queries (`corpora/…-272.json`, page `corpora.html`); observations made on them link to it.
- `origin` on every form (organisation, campaign, contact); 'Found by' line on each page.
- Second reader's tool `tools/review.py` and `REVIEWING.md`; ANACHRONISM set to 'partial' after the second reader's remark.
- Datasette: organisation column and facet.

## 0.2.0 — 2026-09-09
- 40 forms reported by a second, independent observer (the Voûte Claude) from the PubMed substrate (PubTator3, MeSH history, author keywords) and from OpenAlex, OpenAIRE, Wikidata and FAERS: form-142 to form-181, status `proposed`, each with its measurement and date. Form-164 is a hypothesis without observation (measurement not located).
- `corpora/observation-2026-09-voute.json`: the populations, what the observer could not verify, what surprised him.
- Damage counts updated in the README (153 forms).

## 0.1.2 — 2026-09-09
- Public site generated from the records (`tools/build_site.py` → `site/`): home with the seven damages, filterable list, one page per form with observations (English, original on demand), specimens, history. Loxyn visual identity (Inter, Fraunces, JetBrains Mono, accent #0969da).
- Datasette kept for data and API under `/data`.

## 0.1.1 — 2026-09-09
- Every observation note carries an English translation (`excerpt_en`); the original French note stays the record.
- Layer labels and history events in English.
- Internal script names removed from observation notes.
- Datasette view: `observations` and `history` now carry the form name and a foreign key to `forms`; `datasette-metadata.json` added (label column, facets, descriptions).
