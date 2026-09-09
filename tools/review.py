#!/usr/bin/env python3
"""Second reader's tool. Records a review decision in a form's history and status; never deletes anything.

  python3 tools/review.py form-026 --by "Coralie Bagnol-Lebon" --decision validated  [--comment "…"] [--agreement "2/2"]
  python3 tools/review.py form-026 --by "…" --decision contested --comment "variant of form-024: …"
  python3 tools/review.py form-026 --by "…" --decision refuted   --comment "measured absent on …"
  python3 tools/review.py form-150 --by "…" --decision variant --of form-021 --comment "…"   (keeps the record, links it, marks contested)
"""
import argparse, json
from datetime import date
from pathlib import Path
FORMS = Path(__file__).resolve().parent.parent/"forms"
ap = argparse.ArgumentParser(); ap.add_argument("form"); ap.add_argument("--by", required=True); ap.add_argument("--decision", required=True, choices=["validated","contested","refuted","variant"])
ap.add_argument("--comment", default=""); ap.add_argument("--agreement"); ap.add_argument("--of"); ap.add_argument("--date", default=date.today().isoformat())
a = ap.parse_args()
m = list(FORMS.glob(f"{a.form}-*.json")); assert len(m) == 1, m
r = json.loads(m[0].read_text())
if a.decision == "validated":
    if not r["seen"]: raise SystemExit("cannot validate a form without observation")
    r["status"] = "validated"
elif a.decision == "refuted": r["status"] = "refuted"
else: r["status"] = "proposed" if r["status"] == "proposed" else r["status"]  # contested/variant: stays as is, the disagreement is recorded
if a.agreement: r["observer_agreement"] = a.agreement
if a.decision == "variant" and a.of:
    r.setdefault("related", []); a.of not in r["related"] and r["related"].append(a.of)
r["version"] += 1
r["history"].append({"date": a.date, "event": f"second reader: {a.decision}" + (f" of {a.of}" if a.of else "") + (f" — {a.comment}" if a.comment else ""), "by": a.by})
m[0].write_text(json.dumps(r, ensure_ascii=False, indent=2)+"\n")
print(f"{r['id']} → {r['status']} (version {r['version']}) ; run tools/validate.py")
