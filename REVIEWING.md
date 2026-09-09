# Reviewing a form (second reader)

A form becomes `validated` only after a second reader, independent of the observer, has read it. The reader does not edit the record's content; the reader records a decision, dated and signed, in the form's history.

```
python3 tools/review.py form-026 --by "Your name" --decision validated --agreement "2/2" --comment "…"
python3 tools/review.py form-150 --by "Your name" --decision variant --of form-021 --comment "same phenomenon, other corpus"
python3 tools/review.py form-164 --by "Your name" --decision contested --comment "no measurement located"
python3 tools/validate.py
```

Decisions: **validated** (the observation and its classification hold), **variant** (a form of an existing one; the record stays, linked), **contested** (the reader disagrees; both readings stay), **refuted** (measured absent or wrong; the record stays, marked refuted). Nothing is ever deleted.

Reading order suggested by the second reader on 2026-09-09: MISSING and MERGE first — the two damages a deletion-only repair can never touch.
