# Changelog

## 0.1.0 — 2026-09-09
- Schema `form.schema.json` (record of truth: damage, class, seen, specimens, prevention, repair, judgeable_by, history).
- 113 forms migrated from the internal catalogue of 2026-08-09 (`korela.db`), all `migrated_unreviewed`; 26 lines set out of scope.
- Classification by damage and injection done line by line on 2026-09-09 (`docs/VERIFICATION-2026-09-09.md`); judgment, not measurement.
- Validator with house rules; proves itself on seven planted faults.
- SQLite view builder for Datasette.

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
