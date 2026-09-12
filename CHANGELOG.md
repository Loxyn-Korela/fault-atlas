# Changelog

## 0.19.0 — 2026-09-12
- **A mark has a format now, and it is not ours.** A fault observed on a corpus is written as a W3C Web Annotation (Recommendation, 23 February 2017) whose body names an atlas form: `schema/mark.schema.json`, with `ns/context.jsonld` extending the standard vocabulary by exactly five terms — `form`, `damage`, `confidence`, `extent`, `probe`. Both are served at the URLs they declare, so a reader who resolves the context gets it rather than a 404, and a mark is self-describing to someone who has never heard of this atlas.
- **`confidence` says one thing and the schema refuses to let it say more**: how sure the observer is that the fault is present at this target. Not a severity — what a fault costs is a property of the form, not of the sighting. Not a repairer's weight either — a weight is computed from all three. Conflating them is the mistake the field exists to prevent, and it is written into the schema's own description.
- **One mark per line, NDJSON.** Measured on 100,000 real records: 396 bytes each raw, 13 gzipped, a factor of 31 because the context and the field names repeat. The worst case for a 39-million-document corpus — three located marks on every document, 117 million marks — is 1.5 GB gzipped. A single JSON array of the same records could not be read one line at a time nor appended to; one file per document would be 39 million files, which is the allocation-block disaster a 1 MB exFAT block makes of 50 GB of data.
- **A registry fault is marked once against the base**, with its extent, and never once per document drawn from it. The 43 forms that carry a `registry_scope` are exactly those. A house rule the validator enforces: a target with an extent is a base, so it cannot carry a position in a text.
- `tools/validate_marks.py` validates a file of marks, standard library only, holding one mark in memory whatever the file weighs. Verified against seven deliberately wrong marks — a home-made context, a form outside the atlas, a confidence of 1.7, a confidence written in words, an invented damage, a selector that ends before it starts, an extent carrying a selector: all seven refused, each with its own reason.
- `tools/marks_to_weights.py` is the step that did not exist: marks in, one integer per fact out, plus the list of forms that produced it so the number stays explicable. It is a reference implementation and says so — the one arbitrary line is named `IMPACT` and is meant to be replaced. Every weight is scaled by a constant, which changes no ordering and no optimum but buys resolution, and an unmarked fact keeps exactly the weight a repairer would have computed for it. A fully distrusted fact floors at 1, never 0: a weight of 0 is free to delete.

## 0.18.0 — 2026-09-12
- **The home page now says why the atlas names the form and not only the damage**, with the measurement that makes the case rather than an argument. Three identical runs of a deletion-only repairer on a frozen EUR-Lex truth of 489,223 facts reach two of the eight damage classes: spurious edges a law separates, 360 of 360, and wrong labels, 3,932 of 3,932 at a cost of 12,591 true facts. Anachronism 0 of 5,276, wrong value 0 of 2,613, merge 0 of 2,532, split 0 of 1,355, missing 0 of 423, and a spurious edge no law separates 6 of 361.
- The two reached are exactly the two where the graph itself carries what separates the true from the false — a law for the edge, the identifier inside the node for the label. The six it does not reach are exactly the six where it does not. The section says so, and says it is a boundary and not a defect of one repairer: to mend a gap you must know what to add, and that is not in the graph.
- In both languages, with the source, the date, the engine and the reserve that it is measured per damage class and not per form.

## 0.17.0 — 2026-09-12
- **Four forms from a cleaning journal, which is a different kind of source.** The journal kept while the PubMed substrate was built (17-20 August 2026) is a register of the faults met in the building, corrections included. Those faults do not survive into the finished corpus, so no probe on the clean result can find them — which is exactly why they were missing here. **form-191** two identifier families in one document-id field: a reader that accepts only `<id>(\d+)</id>` skips the 472,882 documents whose id is a PMCID, 1.14 %, and the loss is not random — those documents carry 86.8 annotations against 63, because being in PMC means being full text. **form-192** an identifier containing the separator used to split it: `10.1590/1984-0462/;2018;36;4;00019erratum`, which flipped 473 retraction verdicts of 1,429. **form-193** documents truncated in the source itself, discarded correctly and silently. **form-194** Crossref and OpenAlex both returning the same wrong author name, so that the second registry — the usual defence — confirms instead of contradicting.
- All four enter as `proposed`, with the journal's own figure quoted verbatim and no re-measurement claimed. None carries a probe: the corpora are not local.
- **The footer counted the forms by hand** and said 43 of 162 while the atlas held 166. It counts them itself now. This is the same failure that kept the version at v0.6.1 for six releases.
- README: the per-campaign counts are read from the records' `origin.campaign` rather than kept by hand, and they were already wrong by five.

## 0.16.1 — 2026-09-12
- **The search box and all five filters did nothing.** The index script bound its listeners over `[q,fd,fc,fl,fe,fp]`, and no element carries the id `fe`: the line threw a ReferenceError before a single listener was attached, which also killed the click-to-filter on the damage cards and the "N of 162" count. Two of the filters it did list, severity and failure mode, were never declared either and worked only by the accident that a browser exposes elements by id. Declared and bound properly. This was live for every visitor since the filters were added.
- **The links between forms existed in the data and nowhere on the site.** 37 forms carry a `related` field and not one of them was rendered. Each form page now shows both directions — the forms it points to, and the forms that point to it — so form-163 finally says that form-165 exists, which is the whole record of the second reader's variant call of 9 September. The wording says what a link is and is not: the two forms were compared when the newer one entered; the decision, when there is one, is in the history.
- One of those links pointed at `form-003`, which is not a form: catalogue line 3 was ruled an instrument property in August. It renders as what it is, with its reason and a link to the record, instead of a dead link.
- **Rule 7: a form number is permanent**, never reused, never renumbered. Written down because the numbering is not a counter — `form-042` is line 42 of the August catalogue — and because a catalogue's identifier is a citation handle, not a database key.

## 0.16.0 — 2026-09-11
- **The translation is finished.** The 46 refusal clauses, the failure-mode labels, the truths that can judge a form, the probe block down to "frozen copy of the files as read", the yes/no of "can code cancel it", the pills. A French page now reads as French.
- Two duplicate definitions inside the generator were silently winning over the bilingual ones: the truths that judge, and the whole "what a record says" section. Both removed, which is why those two blocks stayed English however many times they were translated.
- What stays English on a French page, and should: the corpus names, the file names and hashes, the probe source, the observation excerpts written in English, and the history of the form, which is an audit trail quoted as written. The English name sits under the French one, as the French sits under the English.

## 0.15.1 — 2026-09-11
- **The French pages had English titles.** Every form page took its `<title>` and its `<h1>` from the English name, so the tab, the heading and the description were English on all 162 French pages. Fixed, along with everything else the generator still said in English on both sides: "found by", "first seen", the severity note, the whole probe block, the no-observation line.
- The English name still appears under the French one, and the French under the English. That is deliberate: it is the same device as the excerpt, which shows the original and folds the translation away.

## 0.15.0 — 2026-09-11
- **Seven cards under a sentence that says seven.** The eighth, corpus parameter, is not a damage and said so in its own description; it now sits below the grid instead of inside it, where it made the headline wrong by one.
- **The language switch is a glyph and a code, not a flag.** A flag is a country, and a country is not a language.
- **The 162 forms all carry a French name.** The last 44 were added.
- **Real bilingual records, not a bilingual shell.** What was English-only in the records and is now in both: the reason under every proposed consequence (49), the extent of every registry fault (41). What left the records entirely, because it repeats from form to form and belongs in the generator: the failure-mode meanings, the measured repairability notes, the sources, the judged/measured line, the disagreement notice.
- Still English on both sides, and deliberately: the corpus identifiers, the file names and hashes, and the history of each form, which is an audit trail and is quoted as it was written. Still English by omission: the 46 refusal clauses.

## 0.14.0 — 2026-09-11
- **The two opening paragraphs are gone.** One explained how to sort a table and listed what a record contains; the other gave a review census the table itself carries, form by form. Neither told a reader anything the page was not already showing.
- **The era filter is gone too**, and with it the "era not measured" block that sat on 122 forms saying nothing. The year the document was published replaces it where it is known, read from the files themselves, and the measured era stays on the 40 forms where it says something a year cannot: that the fault is dead on current publishing.

## 0.13.3 — 2026-09-11
- **The caveat under the count is a census now, not an extrapolation.** It read "two readers on the same six articles agreed on 54 %", which generalises from six documents to 162 forms — the very move this atlas exists to catch. Replaced by what is actually known about all 162: 43 validated by a second reader, 73 migrated and not yet reviewed, 46 proposed. The 54 % stays where its sample size can be stated, in the README.

## 0.13.2 — 2026-09-11
- **Two paragraphs cut to one line each.** The opening explained how to sort a table and what a record contains, both of which the page shows. The second one taught a researcher what a sample is. Gone: the count and the example stand on their own, and the 54 % agreement is one clause instead of a lecture.
- A flag replaces the language name in the navigation, with the destination in its title for anyone reading with a screen reader.

## 0.13.1 — 2026-09-11
- **The French pages were built and never served.** `site/` is not in git: the server rebuilds it with the documented command, which knew nothing of `--fr`. The plain run now builds both languages, so no command has to change anywhere.
- The "what a record says" section is translated too. What stays English on both sides: the proposal page, and 44 forms with no French name, where the English one stands in and shows.

## 0.13.0 — 2026-09-11
- **The site is bilingual.** One generator, run twice: `python3 tools/build_site.py` writes the English site, `--fr` writes `site/fr/`. A link in the navigation switches between the two, from any page, at any depth.
- The records already held most of it: 118 forms carry a French name, and the French original of every observation was already stored beside its English translation. In French the original is shown first and the translation folds away; in English the reverse. On the 44 forms with no French name, the English one stands in.
- Translated in this pass: the damage and class labels, the four consequences, the failure modes, the filters, the table headers, the block titles on each form, and both opening paragraphs. The long "what a record says" section is still English on both sides.
- Why bilingual rather than one or the other: an English-only catalogue keeps the audience it needs, and a French-only one loses it. But an instrument its own authors cannot read comfortably loses its best reviewer, which is the whole point of a catalogue whose every line must be checkable.

## 0.12.0 — 2026-09-11
- **The 49 forms with no severity have a first reading, and it says how much it is worth.** Each carries a proposed consequence with its reason, marked proposed and dated, for a second reader to confirm or contest as for the 43 already validated. **Only 11 of the 49 add anything to what the damage class already implies**, and the other 38 say so on their own page rather than pass a lookup off as a judgment.
- **One disagreement with the August catalogue, stated rather than smoothed over.** August judges most splits *contaminates*; this reading judges most of them *hides*. The two are defensible and the field cannot mean both, so the divergence is printed and left for the second reader.
- **Registry faults gain the field they were missing: how far they reach.** A fault of a base has no prevalence — it is a property of the source, so everything drawn from it carries the fault. 41 forms now state the slice touched, read from their own observation: every record after 2023, 21,292 projects with no jurisdiction, 0 records out of 1,305,653, the whole base. Ranking a systemic outage beside an isolated accident was the thing to avoid.

## 0.11.0 — 2026-09-11
- **What the fault costs you, on every form that has it.** The severity judged line by line in the catalogue of 2026-08-09 was recovered on 2026-09-10 and sat unused. It is now on the page, written as a consequence rather than a code: *contaminates* (21), *answers wrongly in silence* (41), *hides* (39), *stops before the graph* (12). A filter on the index, a pill on each form, a facet of the public database.
- **Because prevalence is not importance.** Nine forms are rare and silent at once — a mnemonic superscript read as a power, 1 of 272; a local and ambiguous date format, 4 of 272. Those are the dangerous ones, and a page that shows only how often a fault occurs invites exactly the wrong reading.

## 0.10.0 — 2026-09-11
- **The year the document was published, read from the files, on 78 forms.** Not the year of the observation: the publication year of the very files where the form was seen, taken from each file's earliest `pub-date`. An era says which period a form belongs to; a year says where it was found, and it does not interpret.
- **And the corpus is a year of publishing, not four.** Its name says 2023-2026 because that is the selection query's window (`FIRST_PDATE 2023-01-01 to 2026-12-31`). The harvest of 2026-08-08 returned **2025 for nine files and 2026 for the other 263**. Every prevalence measured on this corpus is a figure about 2025-2026 publishing, and the corpus record now says so in place of letting its own name imply a four-year spread. The per-file index is `corpora/index/document-years-europe-pmc-272.json`.

## 0.9.0 — 2026-09-10
- **Repairability is measured, not looked up.** 154 forms now carry, beside the judgment of 2026-09-09, what a deletion-only repair actually reached for their damage class: pgrepair on the frozen EUR-Lex truth, three identical runs, journal sha256 in `measures/reachability-by-damage-2026-09-10.json` of the companion repository.
- **The measurement disagrees with the judgment on 28 forms, and the disagreement is the result.** The eight anachronism forms are judged *partial*; the bench reached 0 of 5,276. The twenty spurious-edge forms are judged a flat *yes*; the bench reached 360 of 360 when a law can see the edge and 6 of 361 when none can. Each of the 28 says so on its own page.
- Confirmed by measurement: merge 0 of 2,532, missing 0 of 423, split 0 of 1,355 restored, wrong value 0 of 2,613. Wrong label is reached in full, 3,932 of 3,932, and costs 12,591 true facts because the repair deletes the nodes rather than their labels.
- The judgment is never overwritten. Where the two differ, both are printed.
- Reserve, stated on every form: the measurement is per damage class, not per form. Two forms of the same damage and the same visibility get the same answer.

## 0.8.0 — 2026-09-10
- **Twenty-three forms gain a reproducible example, and the atlas goes from 47 to 70.** The corpus was never lost: the 272 JATS articles are on disk and 36 forms observed on them had simply never had a probe written. Twenty-two probes were written and run, in `probes/2026-09-recovered/`.
- **Two reproduce the August figure exactly** (form-094, 89 of 272 tagged keyword blocks; form-111, 28 of 272 forest plots named inside a figure caption) and are recorded against that observation.
- **Twenty carry a second reading.** Their probe returns a different figure from August's because its definition differs and we could not recover the original one. We did not tune a regex until it hit the target: each probe states its own definition in its docstring, a new dated observation carries its own figure, and the August observation is left exactly as it stands with no example under it. Both readings sit on the page, side by side.
- **Two confirm an absence**: form-078 and form-127, 0 of 272 by an exact probe, as August said. An absence is a measurement, not a missing example.
- `tools/record_probe.py` does the recording, so a probe can never be quietly credited with a figure it did not return.

## 0.7.1 — 2026-09-10
- **The index table no longer scrolls sideways.** The column "Deletion repairs it (classified)" is gone: it repeated the damage column exactly, one value per damage, which is what 0.7.0 established. Class labels are shortened in the table and stay in full on the form page, the corpus cell carries its full text as a tooltip, and the seven columns are laid out on a fixed grid that sums to the width of the page.

## 0.7.0 — 2026-09-10
- **A published sentence was false and is corrected.** 121 forms said their repairability was "classified by judgment on 2026-09-09, not measured". It was not judged form by form: the migration script wrote it from a lookup table on the damage class, `REACH[damage]`. Eight values copied 162 times. The field carried no information the damage did not already carry, and every form now says so.
- **The per-form judgment was never lost, only unused.** The internal catalogue of 2026-08-09 (`korela.db`, table `parametre`) is intact, and its `mode_echec` column is a second axis, judged line by line, that **varies inside a damage class** where repairability does not: the twenty spurious-edge forms span three failure modes, the merges span two. Recovered onto 113 forms as `failure_mode`: PROP identity and it propagates (21) · FAUX a false fact (41) · MANQ a gap (39) · MES a property of the corpus (12). The 49 forms added in September do not carry it yet, and the site says so.
- The mechanism column of that catalogue is deliberately **not** recovered: the atlas records the effect of a remedy, never its mechanism.
- Failure mode is a filter on the index, a line on each form page, and a facet of the public database.

## 0.6.3 — 2026-09-10
- **The count is a shelf, not a measurement**, and the site now says so where the count appears. Two readers, the same six articles, 2026-08-08, no contact: nine novelties and eleven, seven shared — 54 % agreement, and two phenomena both had seen were filed by one as a new form and by the other as a variant. The boundary between new and variant is not objective, so the number of forms is not a quantity; the list of phenomena with their proof is.
- **The era is not the only axis.** Four forms said "born with the modern era" where the measurement of the same day says biomedical before modern: on 14 articles of physics, mathematics, computer science, economics and linguistics, zero structured abstract, zero pre-registration, zero ethics declaration. Structured abstract, pre-registration identifier, forest plot as image and open peer-review furniture now carry that reserve, so a corpus built from them measures a form and not a discipline.

## 0.6.2 — 2026-09-10
- An era that was never measured is now **said** instead of left blank. The confrontation of 2026-08-08 examined forty-three catalogue lines; forty forms carry a measured era, and the other 122 now read *"Era not measured. Nothing here says it is alive today, and nothing says it is dead."* The index gains a filter for exactly those, so the gap can be worked through rather than guessed at.

## 0.6.1 — 2026-09-10
- Four forms the August verdicts on scripts and on rare genres had found and the atlas had never carried. They are faults, not fields, so they enter as forms: **form-187** a retraction notice carries the title of the article it withdraws (25 of the 33 notices in the corpus, and 9 record a disagreement about their own conclusion — probed, reproducible); **form-188** no word boundary in the writing system, with the irreversible case of a name transliterated into katakana; **form-189** case does not exist, a sensor disappears, and its Latin-script mirror where the signal lies instead of missing; **form-190** reading direction inverts the template, a page range 112-129 displayed 129-112.
- The last three carry a reserve: the documents of that wave were not kept by identifier, so they have no reproducible example.

## 0.6.0 — 2026-09-10
- **Eras.** The August campaigns had measured when each difficulty applies — 45 PDFs of 1957-1987 against 15 of 2023-2026 — and the atlas had never carried it. 40 forms now declare their era with the measurement that settled it: 6 in old documents only, 19 in both (3 of them worse now), 14 born with the modern era, 1 not settled. New `era` field, a filter on the list, a section on each form page.
- One classification refuted twice the same day is recorded as such: the non-standard decimal separator, declared dead on 15 modern PDFs, then found alive in a 2023 West African journal and a 2026 systematic review. Fifteen modern PDFs were not enough.

## 0.5.1 — 2026-09-10
- The list carries the date of the most recent observation, is sorted most recent first, and every column sorts on a click.

## 0.5.0 — 2026-09-10
- **First validated forms.** The second reader (Coralie Bagnol-Lebon) read the 62 identity forms (MISSING, MERGE) in full: 43 validated, 5 contested (030, 041, 160, 164, 165), 12 returned because their class was `UNCLASSIFIED`. Two of her own earlier calls reversed on the full text: form-127 and form-078 validated, form-078 linked to form-109 rather than folded into it.
- Her layer rule corrected mine: a form sits upstream of the graph only if **every** one of its layers is pixel or reading. form-068 ("① pixel + ⑤ anchoring") reaches the graph. Of the 62 identity forms, 43 reach the graph, not 42 as I had counted.
- The 12 returned forms now carry a class and a prevention clause, classified by the first reader and awaiting her decision: 167 and 170 DEFEATED (an empty column, records flagged by their own flags), 144 SILENT_FALSE (the bucket passes every legitimate filter), 176 IRREDUCIBLE (choosing between homographs needs the sense), the other 8 REFUSABLE.
- README: the damage table and the review state are generated from the records.

## 0.4.7 — 2026-09-10
- Second reader's rule applied (Coralie Bagnol-Lebon): the second count next to every damage is now "reaches the graph" = every layer beyond pixel and reading; MISSING and MERGE said to Bonifati as 42 of 62, not 62. No damage count is cited without its layer. README table generated from the records.
- form-030, form-041, form-164 marked contested by the second reader.
- Reserve field on observations: the 7 forms citing the 14 non-biomedical articles whose identifiers were not kept carry the reserve on the observation itself.
- form-186: second observation (legal basis by competence, Article 307 never cited); probe covers the three relations.

## 0.4.5 — 2026-09-10
- form-186, found by a human auditor of the EUR-Lex truth: the official register asserts "repeals" where the act's text states an expiry and a replacement, never the repeal. Three live checks in one probe (register says yes, text search finds nothing, text says "prend fin le 28 avril 1999"). First form born from the audit of the truth itself.

## 0.4.4 — 2026-09-09
- Independent review (a second model, reading form-017 as a researcher) found examples that did not show the fault. Seven probe-based observations withdrawn (042, 066, 092, 108, 115, 126, 134: the probe described the document or contradicted the August verdict). Probes 017 and 076 narrowed to return only true instances (template not declared: 2; anonymised labels: 8). One example per form, not three. No example on corpus-parameter forms. History sorted by date; unsupported "bench green" wording removed; corpus label without a count. 45 forms with a reproducible example, 112 without.

## 0.4.3 — 2026-09-09
- "How it was found" open by default on the form.

## 0.4.2 — 2026-09-09
- No count on the form. "12 of 272" reads as a frequency; a form only says: someone can get this wrong, see it here. The counts stay in the records and the result files, off the page.

## 0.4.1 — 2026-09-09
- A database of faults, not of files (third reader): each form shows at most three examples — a document you can open, the evidence found in it, in one parenthesis how many of the checked documents carry it — and, folded, how it was found. The full carrier lists stay in the repository, off the site. "Measured absent" is no longer presented as a proof. Two states on the list: example shown (54) / no example yet (103).

## 0.4.0 — 2026-09-09
- Proof column on the list and a one-click filter "only forms with documents shown": 54 forms show the documents where the fault sits, 11 are measured absent, 41 quote a figure still to be shown, 45 cite an observation without a listed corpus, 6 have no observation. The lead line says the same five counts.
- Frozen corpus published on Zenodo: doi:10.5281/zenodo.22680055.

## 0.3.9 — 2026-09-09
- Frozen copy of the 272-article corpus deposited on Zenodo (draft, doi:10.5281/zenodo.22680055): 267 files as read on 2026-08-08 plus the manifest. Each form's folded "how it was found" block links it.

## 0.3.8 — 2026-09-09
- No probes page either. The form is the only place: the fault, where it was seen, the documents it was found in (clickable), and, folded, how it was found (code, corpus, date). Wording on the form shortened to "Found in N/272 · checked <date>".

## 0.3.7 — 2026-09-09
- Probes page: four statuses instead of two — found again (43), measured today (12), absent (11), to be shown (12) — so that a zero or an observation written today from the probe is not called "shown".

## 0.3.6 — 2026-09-09
- No corpus page any more (third reader: "it only confuses; they will have the link from the fault's own page"). Each shown probe links every carrier document directly, and its folded block says where it was searched, the read date, and points to the record with identifiers, sha256 as read and licences.
- The 272-article record now carries the sha256 of each file as read on 2026-08-08 and the licence found inside the file (175 CC BY 4.0, 45 CC BY-NC-ND 4.0, 18 CC BY-NC 4.0, …); a frozen archive of the 267 files under a named Creative Commons licence is prepared for a Zenodo deposit (5 not redistributed: 2 under a publisher licence, 3 saying only "Creative Commons").

## 0.3.5 — 2026-09-09
- Rule set by the third reader, applied everywhere: a fault is described; its August measurement is cited as a dated claim; documents are shown only when a kept probe finds that very figure again; otherwise the form says "to be shown" and nothing else. No substitute probe with another figure, no "both kept". form-014's substitute probe (2/272 by a different rule) withdrawn. 66 probes shown, 12 waiting for a second reader, 30 August figures without a kept probe.

## 0.3.4 — 2026-09-09
- The corpus link is gone from the observation line: it read as "see the fault here" and it is only the denominator. It stays inside the folded code block, named as such ("the population searched"). The document list is titled "See the trap in the documents": what a graph would fall on; whether a graph does fall is what a bench measures, not what the Atlas shows.

## 0.3.3 — 2026-09-09
- "How to find it again" on each observation, third reader's demand ("we don't care about the corpus, we want the document where the fault is"): every probe now keeps the full list of carrier documents with the evidence found in each (`probes/results/<probe>.json`), and the form shows them first, each document clickable (Europe PMC article and the JATS XML the probe read; PubMed by PMID; Cellar URI or CELEX on EUR-Lex), the code last. 79 probes, 76 result files.
- Observations without a kept probe now say "cannot be shown yet" instead of pointing at the corpus.

## 0.3.2 — 2026-09-09
- form-014 (third reader: "I have a link but where do I see the fault with my own eyes?"): a probe written from the excerpt's own definition, taken literally (organisation and named study in one sentence), finds 2/272 and shows the two sentences. The August 63/272 cannot be recovered (looser rules give 30 or 59) and is flagged on the form. The literal, visible figure is the one to cite.

## 0.3.1 — 2026-09-09
- Third reader's confusion resolved: the corpus page and the probe are two different things, and the site now says so. One page per corpus (`corpora/<id>.html`): which documents, how they were chosen (the selection queries, labelled as such: they choose the articles, they do not find the faults), how to get them again, then the forms found on it with their exact probe, then the forms measured on it whose count has no kept probe. The old single anchored page is gone.
- Each observation on a corpus without a kept probe now says it: "No exact probe kept for this figure; the corpus is reproducible, the count is not yet." 31 such observations remain on the 272 articles, listed on the corpus page.
- Six more probes: lines 22, 70, 83, 93, 128 rewritten from the campaign's inline script, and 135 written today (11/272 block quotations, 1/272 translation marker, exactly the excerpt's figures). 22, 70, 83, 135 reproduce the quoted figures; 93 and 128 do not and say so.

## 0.3.0 — 2026-09-09
- The exact probe on each observation (third reader's request: "which corpus and which exact query finds the problem, not something general"). `probes/2026-08/`: the 66 regex probes of the August campaign, one file per catalogue line, extracted verbatim and re-run on the same 272 files today; `probes/2026-09/`: the two SPARQL queries, the shell request and the dump inventory of the EUR-Lex forms, all re-run live today and reproducing the collector's figures. Schema: `probes[]` on the form, `probe` on the observation.
- Re-run figures published as measured: 38 of 66 August probes give exactly the figure quoted in the excerpt; 28 do not (finer hand-run counts whose code was not kept) and say so on the form. Zero counts attached under "measured absent in" (9 forms).
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

## 0.1.0 — 2026-09-09
- Schema `form.schema.json` (record of truth: damage, class, seen, specimens, prevention, repair, judgeable_by, history).
- 113 forms migrated from the internal catalogue of 2026-08-09 (`korela.db`), all `migrated_unreviewed`; 26 lines set out of scope.
- Classification by damage and injection done line by line on 2026-09-09 (`docs/VERIFICATION-2026-09-09.md`); judgment, not measurement.
- Validator with house rules; proves itself on seven planted faults.
- SQLite view builder for Datasette.
