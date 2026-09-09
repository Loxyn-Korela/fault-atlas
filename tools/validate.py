#!/usr/bin/env python3
"""Validate every form record against schema/form.schema.json, plus the house rules that a schema cannot say.
Exit code 1 on any failure. No dependency beyond the standard library (falls back to a built-in checker if jsonschema is absent)."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT/"schema"/"form.schema.json").read_text())
FORMS = sorted((ROOT/"forms").glob("*.json"))

def check_builtin(obj, sch, path="$"):
    errs = []
    t = sch.get("type")
    if t and not isinstance(obj, {"object":dict,"array":list,"string":str,"integer":int,"boolean":bool}[t]) or (t=="integer" and isinstance(obj,bool)):
        return [f"{path}: expected {t}"]
    if "enum" in sch and obj not in sch["enum"]: errs.append(f"{path}: {obj!r} not in {sch['enum']}")
    if "pattern" in sch and isinstance(obj,str) and not re.search(sch["pattern"], obj): errs.append(f"{path}: {obj!r} does not match {sch['pattern']}")
    if "minLength" in sch and isinstance(obj,str) and len(obj) < sch["minLength"]: errs.append(f"{path}: too short")
    if "minimum" in sch and isinstance(obj,int) and obj < sch["minimum"]: errs.append(f"{path}: below minimum")
    if "minItems" in sch and isinstance(obj,list) and len(obj) < sch["minItems"]: errs.append(f"{path}: needs at least {sch['minItems']} item(s)")
    if isinstance(obj, dict):
        for r in sch.get("required", []):
            if r not in obj: errs.append(f"{path}: missing required '{r}'")
        props = sch.get("properties", {})
        if sch.get("additionalProperties") is False:
            for k in obj:
                if k not in props: errs.append(f"{path}: unknown field '{k}'")
        for k, v in obj.items():
            if k in props: errs += check_builtin(v, props[k], f"{path}.{k}")
    if isinstance(obj, list) and "items" in sch:
        for i, v in enumerate(obj): errs += check_builtin(v, sch["items"], f"{path}[{i}]")
    return errs

def house_rules(rec):
    errs = []
    if rec["status"] == "validated":
        if not rec["seen"]: errs.append("validated form without any observation (seen is empty)")
        if rec["specimens"]["cases"] and not rec["specimens"]["counter_examples"]: errs.append("cases without a counter-example cannot be tested")
        if not rec.get("observer_agreement"): errs.append("validated form must state observer agreement")
    if rec["damage"] == "CORPUS_PARAMETER" and rec["repair"]["reachable_by_deletion"] != "no": errs.append("a corpus parameter is not repairable")
    for s in rec["seen"]:
        if not s["excerpt"].strip(): errs.append("empty excerpt")
    return errs

try:
    import jsonschema
    validate = lambda rec: [e.message for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(rec)]
except ImportError:
    validate = lambda rec: check_builtin(rec, SCHEMA)

bad = 0
ids = set()
for f in FORMS:
    rec = json.loads(f.read_text())
    errs = validate(rec) + house_rules(rec)
    if rec["id"] in ids: errs.append("duplicate id")
    ids.add(rec["id"])
    if not f.name.startswith(rec["id"]): errs.append(f"file name must start with {rec['id']}")
    if errs:
        bad += 1
        print(f"✗ {f.name}"); [print("   ", e) for e in errs]
print(f"{len(FORMS)-bad}/{len(FORMS)} forms valid")
sys.exit(1 if bad else 0)
