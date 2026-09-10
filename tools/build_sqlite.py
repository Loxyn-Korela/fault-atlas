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
create table forms(id text primary key, name text, damage text, class text, injection text, layer text, status text, organisation text, campaign text,
  cancellable_by_code int, reachable_by_deletion text, judgeable_by text, observations int, observed_absent_in text,
  name_fr text, legacy_line int, version int, era text, era_worse_now int, era_note text, era_measured text, failure_mode text, record json);
create table observations(id integer primary key, form_id text references forms(id), form_name text, corpus text, corpus_id text, document text, date text, observer text, excerpt_en text, excerpt_original text, lang text, probe text);
create table probes(id integer primary key, form_id text references forms(id), form_name text, file text, kind text, corpus_id text, written text, run text, result_count int, result_of int, result_date text, matches_excerpt int, note text, code text);
create table history(id integer primary key, form_id text references forms(id), form_name text, date text, event text, by text);
""")
for f in sorted((ROOT/"forms").glob("*.json")):
    r = json.loads(f.read_text())
    e = r.get("era") or {}
    db.execute("insert into forms values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (r["id"], r["name"], r["damage"], r["class"], r.get("injection"), r["layer"], r["status"], r.get("origin",{}).get("organisation"), r.get("origin",{}).get("campaign"),
        int(r["prevention"]["cancellable_by_code"]), r["repair"]["reachable_by_deletion"], ", ".join(r["judgeable_by"]), len(r["seen"]), ", ".join(r.get("observed_absent_in", [])),
        r.get("name_fr"), r.get("legacy_line"), r["version"],
        e.get("value", "not_measured"), int(bool(e.get("aggravated_by_the_modern"))), e.get("note"), e.get("measured"),
        (r.get("failure_mode") or {}).get("value", "not_recovered"),
        json.dumps(r, ensure_ascii=False)))
    for s in r["seen"]:
        db.execute("insert into observations(form_id,form_name,corpus,corpus_id,document,date,observer,excerpt_en,excerpt_original,lang,probe) values(?,?,?,?,?,?,?,?,?,?,?)",
                   (r["id"], r["name"], s["corpus"], s.get("corpus_id"), s.get("document"), s["date"], s.get("observer"), s.get("excerpt_en", s["excerpt"]), s["excerpt"], s.get("lang"), s.get("probe")))
    for pr in r.get("probes", []):
        res = pr.get("result", {}); pf = ROOT/pr["file"]
        db.execute("insert into probes(form_id,form_name,file,kind,corpus_id,written,run,result_count,result_of,result_date,matches_excerpt,note,code) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (r["id"], r["name"], pr["file"], pr["kind"], pr["corpus_id"], pr.get("written"), pr.get("run"), res.get("count"), res.get("of"), res.get("date"),
                    None if pr.get("matches_excerpt") is None else int(pr["matches_excerpt"]), pr.get("note"), pf.read_text(encoding="utf-8") if pf.is_file() else None))
    for h in r["history"]:
        db.execute("insert into history(form_id,form_name,date,event,by) values(?,?,?,?,?)", (r["id"], r["name"], h["date"], h["event"], h.get("by")))
db.commit()
n = db.execute("select count(*) from forms").fetchone()[0]
print(f"{n} forms → {out.name}")
for row in db.execute("select damage, count(*) from forms group by damage order by 2 desc"): print("  ", *row)
print("eras:")
for row in db.execute("select era, count(*) from forms group by era order by 2 desc"): print("  ", *row)
