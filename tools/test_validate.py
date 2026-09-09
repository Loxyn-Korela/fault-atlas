#!/usr/bin/env python3
"""The validator proves itself by failing: plant known faults in a copy of a record and check each one is caught."""
import json, subprocess, sys, shutil, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
src = sorted((ROOT/"forms").glob("form-085-*.json"))[0]
base = json.loads(src.read_text())
faults = {
  "missing required field": lambda r: r.pop("damage"),
  "unknown damage": lambda r: r.update(damage="BROKEN"),
  "unknown top-level field": lambda r: r.update(secret_mechanism="..."),
  "empty excerpt": lambda r: r["seen"].append({"corpus":"x","date":"2026-01-01","excerpt":"  "}),
  "validated without observation": lambda r: (r.update(status="validated"), r.update(seen=[])),
  "cases without counter-example, validated": lambda r: (r.update(status="validated", observer_agreement="2/2"), r["specimens"].update(cases=[{"input":1,"expected":2}], counter_examples=[])),
  "bad id pattern": lambda r: r.update(id="form-85"),
  "probe file that does not exist": lambda r: r.update(probes=[{"file":"probes/2026-08/line-999.py","kind":"python","corpus_id":"corpus-europe-pmc-jats-2023-2026"}]),
  "observation citing an unlisted probe": lambda r: r["seen"][0].update(probe="probes/2026-08/line-036.py"),
  "probe on an unknown corpus": lambda r: r.update(probes=[{"file":"probes/2026-08/line-085.py","kind":"python","corpus_id":"corpus-nowhere"}]),
}
caught = 0
with tempfile.TemporaryDirectory() as d:
    tmp = Path(d); shutil.copytree(ROOT/"schema", tmp/"schema"); (tmp/"forms").mkdir(); (tmp/"tools").mkdir()
    shutil.copy(ROOT/"tools"/"validate.py", tmp/"tools"/"validate.py")
    shutil.copytree(ROOT/"corpora", tmp/"corpora"); shutil.copytree(ROOT/"probes", tmp/"probes")
    for name, mutate in faults.items():
        r = json.loads(json.dumps(base)); mutate(r)
        for f in (tmp/"forms").glob("*"): f.unlink()
        (tmp/"forms"/src.name).write_text(json.dumps(r))
        rc = subprocess.run([sys.executable, str(tmp/"tools"/"validate.py")], capture_output=True).returncode
        print(("caught  " if rc else "MISSED  ") + name); caught += bool(rc)
print(f"{caught}/{len(faults)} planted faults caught")
sys.exit(0 if caught == len(faults) else 1)
