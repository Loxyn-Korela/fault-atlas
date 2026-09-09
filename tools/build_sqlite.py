#!/usr/bin/env python3
"""Compile the form records into fault-atlas.sqlite for browsing with Datasette. The JSON files remain the source of truth; this file is a view.
Serve with:  datasette fault-atlas.sqlite --immutable fault-atlas.sqlite --metadata datasette-metadata.json"""
import json, sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
out = ROOT/"fault-atlas.sqlite"
if out.exists(): out.unlink()
db = sqlite3.connect(out)
db.executescript("""
create table forms(id text primary key, name text, damage text, class text, injection text, layer text, status text,
  cancellable_by_code int, reachable_by_deletion text, judgeable_by text, observations int, observed_absent_in text,
  name_fr text, legacy_line int, version int, record json);
create table observations(id integer primary key, form_id text references forms(id), form_name text, corpus text, document text, date text, observer text, excerpt_en text, excerpt_original text, lang text);
create table history(id integer primary key, form_id text references forms(id), form_name text, date text, event text, by text);
""")
for f in sorted((ROOT/"forms").glob("*.json")):
    r = json.loads(f.read_text())
    db.execute("insert into forms values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (r["id"], r["name"], r["damage"], r["class"], r.get("injection"), r["layer"], r["status"],
        int(r["prevention"]["cancellable_by_code"]), r["repair"]["reachable_by_deletion"], ", ".join(r["judgeable_by"]), len(r["seen"]), ", ".join(r.get("observed_absent_in", [])),
        r.get("name_fr"), r.get("legacy_line"), r["version"], json.dumps(r, ensure_ascii=False)))
    for s in r["seen"]:
        db.execute("insert into observations(form_id,form_name,corpus,document,date,observer,excerpt_en,excerpt_original,lang) values(?,?,?,?,?,?,?,?,?)",
                   (r["id"], r["name"], s["corpus"], s.get("document"), s["date"], s.get("observer"), s.get("excerpt_en", s["excerpt"]), s["excerpt"], s.get("lang")))
    for h in r["history"]:
        db.execute("insert into history(form_id,form_name,date,event,by) values(?,?,?,?,?)", (r["id"], r["name"], h["date"], h["event"], h.get("by")))
db.commit()
n = db.execute("select count(*) from forms").fetchone()[0]
print(f"{n} forms → {out.name}")
for row in db.execute("select damage, count(*) from forms group by damage order by 2 desc"): print("  ", *row)
