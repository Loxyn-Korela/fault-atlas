#!/usr/bin/env python3
"""Compile the form records into fault-atlas.sqlite for browsing with Datasette. The JSON files remain the source of truth; this file is a view."""
import json, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
out = ROOT/"fault-atlas.sqlite"
if out.exists(): out.unlink()
db = sqlite3.connect(out)
db.executescript("""
create table forms(id text primary key, version int, legacy_line int, name text, name_fr text, damage text, class text, layer text, injection text,
  status text, cancellable_by_code int, reachable_by_deletion text, judgeable_by text, n_observations int, observed_absent_in text, record json);
create table observations(form_id text, corpus text, document text, date text, observer text, excerpt text, lang text);
create table history(form_id text, date text, event text, by text);
""")
for f in sorted((ROOT/"forms").glob("*.json")):
    r = json.loads(f.read_text())
    db.execute("insert into forms values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (r["id"], r["version"], r.get("legacy_line"), r["name"], r.get("name_fr"), r["damage"], r["class"], r["layer"], r.get("injection"),
        r["status"], int(r["prevention"]["cancellable_by_code"]), r["repair"]["reachable_by_deletion"], ",".join(r["judgeable_by"]), len(r["seen"]), ",".join(r.get("observed_absent_in", [])), json.dumps(r, ensure_ascii=False)))
    for s in r["seen"]: db.execute("insert into observations values(?,?,?,?,?,?,?)", (r["id"], s["corpus"], s.get("document"), s["date"], s.get("observer"), s["excerpt"], s.get("lang")))
    for h in r["history"]: db.execute("insert into history values(?,?,?,?)", (r["id"], h["date"], h["event"], h.get("by")))
db.commit()
n = db.execute("select count(*) from forms").fetchone()[0]
print(f"{n} forms → {out.name}")
for row in db.execute("select damage, count(*) from forms group by damage order by 2 desc"): print("  ", *row)
