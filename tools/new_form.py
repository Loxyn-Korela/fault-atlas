#!/usr/bin/env python3
"""Scaffold a new form record, or add an observation to an existing one.

  python3 tools/new_form.py new "Short English name" --damage MERGE --corpus "EUR-Lex, Cellar snapshot 2026-09" --date 2026-09-10 --excerpt "verbatim excerpt…" [--document id] [--observer name] [--lang fr]
  python3 tools/new_form.py seen form-026 --corpus "…" --date 2026-09-10 --excerpt "…" [--document id] [--observer name] [--lang en]

The record is written with status "proposed" and the fields still to fill marked TODO. Run tools/validate.py afterwards."""
import argparse, json, re, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FORMS = ROOT/"forms"
DAMAGES = ["MERGE","SPLIT","SPURIOUS_EDGE","MISSING","WRONG_VALUE","WRONG_LABEL","ANACHRONISM","CORPUS_PARAMETER"]

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")[:48]

def next_id():
    nums = [int(re.match(r"form-(\d{3})", f.name).group(1)) for f in FORMS.glob("form-*.json")]
    return f"form-{max(nums)+1:03d}"

def observation(a):
    o = {"corpus": a.corpus, "date": a.date, "excerpt": a.excerpt, "lang": a.lang}
    if getattr(a, "organisation", None): o["organisation"] = a.organisation
    if a.document: o["document"] = a.document
    if a.observer: o["observer"] = a.observer
    return o

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
for name in ("new", "seen"):
    p = sub.add_parser(name)
    p.add_argument("target", help="English name (new) or form id (seen)")
    if name == "new": p.add_argument("--damage", required=True, choices=DAMAGES)
    p.add_argument("--corpus", required=True); p.add_argument("--date", required=True); p.add_argument("--excerpt", required=True)
    p.add_argument("--document"); p.add_argument("--observer"); p.add_argument("--lang", default="en"); p.add_argument("--organisation", required=(name=="new"), help="contributing organisation")
a = ap.parse_args()

if a.cmd == "new":
    fid = next_id()
    rec = {
      "id": fid, "version": 1, "name": a.target, "origin": {"organisation": a.organisation}, "damage": a.damage, "class": "UNCLASSIFIED", "layer": "TODO",
      "injection": "ALTER", "status": "proposed",
      "seen": [observation(a)],
      "specimens": {"cases": [], "counter_examples": []},
      "prevention": {"cancellable_by_code": False, "note": "TODO: can deterministic code cancel this form? with what refusal clause?"},
      "repair": {"reachable_by_deletion": "unknown", "note": "TODO"},
      "judgeable_by": [],
      "history": [{"date": a.date, "event": f"proposed from {a.corpus}", "by": a.observer or "TODO"}],
    }
    path = FORMS/f"{fid}-{slug(a.target)}.json"
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=2)+"\n")
    print(f"written {path.name} — fill class, layer, injection, prevention, repair, judgeable_by ; then: python3 tools/validate.py")
else:
    matches = list(FORMS.glob(f"{a.target}-*.json"))
    if len(matches) != 1: raise SystemExit(f"no unique file for {a.target}: {matches}")
    rec = json.loads(matches[0].read_text())
    rec["seen"].append(observation(a))
    rec["version"] += 1
    rec["history"].append({"date": a.date, "event": f"observation added from {a.corpus}", "by": a.observer or "TODO"})
    matches[0].write_text(json.dumps(rec, ensure_ascii=False, indent=2)+"\n")
    print(f"observation added to {matches[0].name} (version {rec['version']}) ; then: python3 tools/validate.py")
