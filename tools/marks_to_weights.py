#!/usr/bin/env python3
"""Turn marks into one number per fact — the step between an atlas and a repairer.

  python3 tools/marks_to_weights.py <facts.jsonl> <marks.jsonl…> > facts-weighted.jsonl

A fact is a line {"s":…, "p":…, "o":…, "doc":…, "span":[a,b]}. A mark is a line of the format in
schema/mark.schema.json. Out comes the same fact with two fields added:

  conf    an integer weight, what a repairer reads (pgrepair: --custom-weight conf)
  marks   the forms that produced it, so the number stays explicable

This is a REFERENCE implementation. It does the simplest defensible thing and says where the
judgement sits, because the judgement is the whole of it and it is not universal: how much an
ambiguous decimal should cost a numeric fact is a question about your corpus and your use, not
about the atlas.

── the three decisions, stated ──────────────────────────────────────────────────────────────

1. WHICH MARKS BEAR ON A FACT. A mark on the fact's document, and either carrying no selector —
   most do not, the fault is a property of the whole document — or carrying one that overlaps the
   fact's own span. A mark on a corpus bears on every fact drawn from that corpus.

2. HOW TRUST FALLS. Each bearing mark multiplies trust by (1 - confidence x impact), where impact
   comes from the form's consequence: a fault that contaminates an identity costs a fact more than
   one that merely hides something else. Marks compound, so two weak marks are worse than one.
   This is the arbitrary part. It is one line, it is named `IMPACT`, and it is meant to be changed.

3. THE SCALE. Every weight, on nodes and edges alike, is multiplied by SCALE. Multiplying all of
   them changes no ordering and no optimum — it only buys resolution, so that trust can vary in
   200 steps instead of 2. An unmarked edge keeps exactly the weight pgrepair would have computed
   for it, times SCALE: an unmarked graph therefore behaves exactly as it does today. A fully
   distrusted fact floors at 1 and never at 0, because a weight of 0 is free to delete, and a
   repairer handed a free edge deletes it before anything else.
"""
import json, sys
from pathlib import Path

EDGE_WEIGHT = 2      # pgrepair/constants.py
SCALE = 100
FLOOR = 1

# What a damage does to a fact drawn from where it was seen. Derived from the atlas consequence
# classes: G1 contaminates an identity, G2 answers wrongly in silence, G3 hides, G4 stops upstream.
IMPACT = {
    "MERGE": 0.9, "SPLIT": 0.9,            # G1 — the identity is wrong, everything hanging on it inherits
    "WRONG_VALUE": 0.8, "WRONG_LABEL": 0.8,  # G2 — the fact is false and nothing signals it
    "SPURIOUS_EDGE": 0.8, "ANACHRONISM": 0.6,
    "MISSING": 0.3,                        # G3 — it hides something else; the fact at hand may be sound
    "CORPUS_PARAMETER": 0.0,               # not a fault: a property of the corpus
}


def bears_on(mark, fact):
    """Decision 1."""
    t = mark["target"]
    if t["source"] not in (fact.get("doc"), fact.get("corpus")):
        return False
    sel = t.get("selector")
    if sel is None:
        return True                          # a property of the whole document
    span = fact.get("span")
    if not span:
        return True                          # we cannot place the fact: the mark is kept, not dropped
    if sel.get("type") == "TextPositionSelector":
        return not (span[1] < sel["start"] or span[0] > sel["end"])
    return sel.get("exact", "") in (fact.get("text") or "")


def weigh(fact, marks):
    """Decisions 2 and 3. Returns (weight, the forms that moved it)."""
    trust, used = 1.0, []
    for m in marks:
        if not bears_on(m, fact):
            continue
        b = m["body"]
        impact = IMPACT.get(b.get("damage", ""), 0.5)
        trust *= 1.0 - b["confidence"] * impact
        used.append(b["form"].rsplit("/", 1)[-1].removesuffix(".html"))
    return max(FLOOR, round(EDGE_WEIGHT * SCALE * trust)), sorted(set(used))


def load(paths):
    out = []
    for p in paths:
        for line in Path(p).read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    marks = load(argv[1:])
    n = 0
    for line in Path(argv[0]).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        fact = json.loads(line)
        fact["conf"], fact["marks"] = weigh(fact, marks)
        print(json.dumps(fact, ensure_ascii=False))
        n += 1
    print(f"{n} facts weighed against {len(marks)} marks", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
