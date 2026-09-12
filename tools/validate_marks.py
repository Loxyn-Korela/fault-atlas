#!/usr/bin/env python3
"""Validate a file of marks, one JSON object per line (NDJSON), against schema/mark.schema.json.

  python3 tools/validate_marks.py marks/example.jsonl [more.jsonl …]

Exit code 1 on any failure. Standard library only; uses jsonschema when it is installed and a
built-in check of the same rules when it is not, so a contributor never needs to install anything
to find out whether their file is acceptable.

Line-oriented on purpose: a mark file for a corpus of 39 million documents holds up to 117 million
marks, which is 1.5 GB gzipped at 13 bytes a line. Read one line, validate it, forget it — the
validator never holds more than one mark in memory, whatever the file weighs.
"""
import gzip, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "mark.schema.json").read_text())
DAMAGES = set(SCHEMA["properties"]["body"]["properties"]["damage"]["enum"])
FORM_RE = re.compile(SCHEMA["properties"]["body"]["properties"]["form"]["pattern"])
CONTEXT = SCHEMA["properties"]["@context"]["const"]


def check(m):
    """The rules of the schema, said once in Python so no dependency is needed to hear them."""
    e = []
    if m.get("@context") != CONTEXT: e.append(f"@context must be {CONTEXT}")
    if m.get("type") != "Annotation": e.append("type must be Annotation")
    b, t = m.get("body"), m.get("target")
    if not isinstance(b, dict): return e + ["body is required and must be an object"]
    if not isinstance(t, dict): return e + ["target is required and must be an object"]
    if not FORM_RE.match(str(b.get("form", ""))):
        e.append("body.form must be the URL of a Fault Atlas form")
    c = b.get("confidence")
    if not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1:
        e.append("body.confidence must be a number in [0, 1]: how sure the observer is that the "
                 "fault is present here, and nothing else")
    if "damage" in b and b["damage"] not in DAMAGES:
        e.append(f"body.damage {b['damage']!r} is not one of the seven, plus CORPUS_PARAMETER")
    if not t.get("source"): e.append("target.source is required")
    s = t.get("selector")
    if s is not None:
        if s.get("type") == "TextPositionSelector":
            a, z = s.get("start"), s.get("end")
            if not isinstance(a, int) or not isinstance(z, int):
                e.append("a TextPositionSelector needs integer start and end")
            elif z < a:
                e.append(f"selector ends before it starts: {a} -> {z}")
        elif s.get("type") == "TextQuoteSelector":
            if not s.get("exact"): e.append("a TextQuoteSelector needs its exact text")
        else:
            e.append("selector.type must be TextPositionSelector or TextQuoteSelector")
    # A house rule no schema can state: a fault of a registry is marked against the base, once,
    # and a slice of a base has no position in a text.
    if "extent" in t and s is not None:
        e.append("a target with an extent is a base, not a document: it cannot carry a selector")
    return e


try:
    import jsonschema
    _v = jsonschema.Draft202012Validator(SCHEMA)
    validate = lambda m: [x.message for x in _v.iter_errors(m)] + check(m)
except ImportError:
    validate = check


def lines(p):
    op = gzip.open if p.suffix == ".gz" else open
    with op(p, "rt", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            if line.strip():
                yield i, line


def main(paths):
    total = bad = 0
    for p in map(Path, paths):
        for i, line in lines(p):
            total += 1
            try:
                m = json.loads(line)
            except json.JSONDecodeError as exc:
                bad += 1; print(f"✗ {p.name}:{i} not JSON — {exc}"); continue
            errs = validate(m)
            if errs:
                bad += 1; print(f"✗ {p.name}:{i}"); [print("   ", x) for x in errs]
    print(f"{total - bad}/{total} marks valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or [ROOT / "marks" / "example.jsonl"]))
