# Contributing a form

A form enters the atlas with a **verbatim excerpt from a named corpus, a date and an observer**. Without them it is a hypothesis, not an observation, and the validator refuses it once you try to validate it.

## You saw a known form on a new corpus

```
python3 tools/new_form.py seen form-026 --corpus "EUR-Lex, Cellar snapshot 2026-09" --date 2026-09-10 --observer "your name" --excerpt "the verbatim note or excerpt"
python3 tools/validate.py
```

## You saw a form the atlas does not have

```
python3 tools/new_form.py new "Short English name" --damage MERGE --corpus "…" --date 2026-09-10 --observer "your name" --excerpt "…"
python3 tools/validate.py
```

Then fill the `TODO` fields: `class` (can code cancel it? can it abstain? is it silent? does it need meaning?), `layer`, `injection` (how a controlled corpus could fabricate it), `prevention`, `repair` (can a deletion-only repair restore the truth?), `judgeable_by` (which kind of truth can judge it). Add cases **and counter-examples** if you have them.

## Then

Open a pull request with the one JSON file. A second reader reviews: validated, or contested (novel form, or variant of an existing one — the disagreement is recorded, never erased). A refuted form stays, marked refuted, with the measurement.

## What never goes in

- The implementation of any remedy, filter, guard or repair. The atlas records effects, never mechanisms.
- Client documents or personal data. Specimens are forms and excerpts from public corpora.
- A number of forms as a claim of completeness. Say "complete for the observed population, saturation reached at document N".
