#!/usr/bin/env python3
"""Generate the public site (static HTML) from the form records. No framework, no dependency.
Output: site/  — index.html, forms/<id>.html, atlas.json (all records), style.css.
The JSON files remain the source of truth; the site is a view rebuilt at each release."""
import json, html, re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT/"site"; (SITE/"forms").mkdir(parents=True, exist_ok=True)
import shutil; FAV = ROOT/"tools"/"favicon.svg"
if FAV.exists(): shutil.copy(FAV, SITE/"favicon.svg")
DOI = "10.5281/zenodo.22674547"; REPO = "https://github.com/Loxyn-Korela/fault-atlas"; DATA = "/data/fault-atlas"
VERSION = re.search(r"^version: (.+)$", (ROOT/"CITATION.cff").read_text(), re.M).group(1)

DAMAGE = {
 "MERGE": ("Merge", "two real things become one node", "#b3261e"),
 "SPLIT": ("Split", "one thing becomes several nodes", "#c2410c"),
 "SPURIOUS_EDGE": ("Spurious edge", "a relation the source never asserted", "#a16207"),
 "MISSING": ("Missing", "a node or relation the source asserts and the graph lacks", "#3f6212"),
 "WRONG_VALUE": ("Wrong value", "a property, number or date is wrong", "#0e7490"),
 "WRONG_LABEL": ("Wrong label", "an entity or relation type is wrong", "#4338ca"),
 "ANACHRONISM": ("Anachronism", "a fact outside its validity interval, or a superseded status kept", "#7e22ce"),
 "CORPUS_PARAMETER": ("Corpus parameter", "not a damage: a property of the corpus composition", "#57534e"),
}
CLASS = {"DEFEATED": "Cancelled by code", "DEFEATED_IF_XML": "Cancelled by code when the source is XML", "REFUSABLE": "Code can abstain on it",
         "SILENT_FALSE": "Silent false: code cannot see it from inside", "IRREDUCIBLE": "Irreducible: needs meaning", "UNCLASSIFIED": "Unclassified"}
REACH = {"yes": "yes", "no": "no", "partial": "partial", "unknown": "unknown"}
JUDGE = {"construction": "truth by construction", "registry": "an official registry", "curated": "a curated database", "dated_future": "the dated future", "closed_world": "a closed world"}

forms = [json.loads(f.read_text()) for f in sorted((ROOT/"forms").glob("*.json"))]
E = html.escape

def layout(title, body, depth=0, desc=""):
    p = "../"*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc or 'Observed fault forms in knowledge graphs built from documents, with provenance, damage and the truth that judges them.')}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:ital,opsz,wght,SOFT@1,9..144,300,0&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}style.css"></head><body>
<header class="top"><a class="brand" href="{p}index.html"><img src="{p}favicon.svg" alt="" width="22" height="22"> Fault Atlas <span class="by">by Loxyn</span></a>
<nav><a href="{p}index.html#forms">Forms</a><a href="{p}index.html#about">About</a><a href="{DATA}">Data &amp; API</a><a href="{REPO}">GitHub</a><a href="https://doi.org/{DOI}">DOI</a></nav></header>
<main>{body}</main>
<footer><p><strong>Fault Atlas</strong> v{E(VERSION)} · Loxyn SAS, Lyon · Gracia S., Bagnol-Lebon C., Comtet Y. · records CC BY-SA 4.0, tools Apache 2.0 · <a href="https://doi.org/{DOI}">doi:{DOI}</a> · <a href="{REPO}">source</a> · <a href="mailto:contact@loxyn.ai">contact@loxyn.ai</a></p>
<p class="muted">Every record is still <code>migrated_unreviewed</code>: classified by one reader, awaiting a second. The JSON file is the record of truth; this site is a view rebuilt at each release.</p></footer>
</body></html>"""

# ── index ──
counts = Counter(f["damage"] for f in forms)
cards = "".join(f"""<a class="card" href="#forms" data-damage="{k}" style="--c:{v[2]}"><span class="n">{counts.get(k,0)}</span><span class="t">{E(v[0])}</span><span class="d">{E(v[1])}</span></a>""" for k,v in DAMAGE.items())
rows = "".join(f"""<tr data-damage="{f['damage']}" data-class="{f['class']}" data-inj="{f.get('injection','')}" data-text="{E((f['name']+' '+f.get('name_fr','')).lower())}">
<td><a href="forms/{f['id']}.html">{E(f['name'])}</a><br><span class="fr">{E(f.get('name_fr',''))}</span></td>
<td><span class="pill" style="--c:{DAMAGE[f['damage']][2]}">{E(DAMAGE[f['damage']][0])}</span></td>
<td>{E(CLASS[f['class']])}</td><td>{E(f.get('injection',''))}</td><td class="num">{len(f['seen'])}</td><td>{E(REACH[f['repair']['reachable_by_deletion']])}</td></tr>""" for f in forms)
index = f"""
<section class="hero"><p class="eyebrow">A library of observed fault forms in knowledge graphs built from documents</p>
<h1>Every fault has a form. Every form does one of seven things to the graph.</h1>
<p class="lead">{len(forms)} forms observed on real corpora, each with its provenance, the damage it causes, whether code can cancel it, whether a deletion-only repair can restore the truth, and which kind of truth can judge it. A repair that holds on one form of a damage may fail on another form of the same damage: this is the test matrix that says which.</p>
<p class="cta"><a class="btn" href="#forms">Browse the forms</a> <a class="btn ghost" href="{DATA}">Query the data</a> <a class="btn ghost" href="{REPO}/issues/new?template=propose-form.yml">Propose a form</a></p></section>
<section class="grid" id="damages">{cards}</section>
<section id="forms"><div class="bar"><input id="q" type="search" placeholder="Search a form…" aria-label="Search">
<select id="fd"><option value="">All damages</option>{''.join(f'<option value="{k}">{E(v[0])}</option>' for k,v in DAMAGE.items())}</select>
<select id="fc"><option value="">All classes</option>{''.join(f'<option value="{k}">{E(v)}</option>' for k,v in CLASS.items())}</select>
<span id="count" class="muted"></span></div>
<div class="tablewrap"><table id="t"><thead><tr><th>Form</th><th>Damage</th><th>Class</th><th>Injection</th><th>Seen</th><th>Deletion repairs it</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="about" class="about"><h2>What a record says</h2>
<div class="cols"><div><h3>Seven damages</h3><p>What a fault does to the graph: merge, split, spurious edge, missing, wrong value, wrong label, anachronism. The 113 difficulties observed in August 2026, however different they look, each produce one of these. Verified line by line.</p></div>
<div><h3>Four classes</h3><p>Whether deterministic code cancels the form before it enters the graph, can abstain on it, cannot see it from inside, or whether it needs meaning. Half of what was observed is cancelled by code once; the other half is the real benchmark.</p></div>
<div><h3>Provenance, not opinion</h3><p>A form enters with a verbatim excerpt from a named corpus, a date, an observer. Cases come with counter-examples. A refuted form stays, marked refuted. Nothing is deleted.</p></div>
<div><h3>Why it matters</h3><p>Graph repair is evaluated against constraints the graph must satisfy, not against what is true. The atlas is half of an answer key: the map of forms by damage, with the kind of truth that can judge each. The other half, the truth itself, is built on it.</p></div></div>
<p>Met a form on your corpus? <a href="{REPO}/issues/new?template=propose-form.yml">Propose it</a> with its excerpt, corpus and date — no code needed — or send the JSON record by pull request. A second reader reviews; a contested form stays recorded as contested; nothing enters unreviewed. Cite: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). <em>Fault Atlas.</em> Loxyn SAS, Lyon. Zenodo. <a href="https://doi.org/{DOI}">doi:{DOI}</a>.</p></section>
<script>
const q=document.getElementById('q'),fd=document.getElementById('fd'),fc=document.getElementById('fc'),rows=[...document.querySelectorAll('#t tbody tr')],c=document.getElementById('count');
function apply(){{const s=q.value.toLowerCase(),d=fd.value,k=fc.value;let n=0;for(const r of rows){{const ok=(!d||r.dataset.damage===d)&&(!k||r.dataset.class===k)&&(!s||r.dataset.text.includes(s));r.hidden=!ok;if(ok)n++;}}c.textContent=n+' of '+rows.length;}}
[q,fd,fc].forEach(e=>e.addEventListener('input',apply));document.querySelectorAll('.card').forEach(a=>a.addEventListener('click',()=>{{fd.value=a.dataset.damage;apply();}}));apply();
</script>"""
(SITE/"index.html").write_text(layout("Fault Atlas", index))

# ── form pages ──
for f in forms:
    d = DAMAGE[f["damage"]]
    seen = "".join(f"""<article class="obs"><p class="meta">{E(s['corpus'])} · {E(s['date'])}{(' · '+E(s['observer'])) if s.get('observer') else ''}</p>
<p>{E(s.get('excerpt_en', s['excerpt']))}</p>{('<details><summary>Original note ('+E(s.get('lang','fr'))+')</summary><p class="fr">'+E(s['excerpt'])+'</p></details>') if s.get('excerpt_en') and s.get('excerpt_en')!=s['excerpt'] else ''}</article>""" for s in f["seen"]) or "<p class='muted'>No observation yet: this form is a hypothesis, not an observation.</p>"
    cases = f["specimens"]["cases"]; cex = f["specimens"]["counter_examples"]
    spec = (f"<p>{len(cases)} case(s), {len(cex)} counter-example(s).</p>" if cases or cex else "<p class='muted'>Specimens not yet transcribed into this record.</p>")
    hist = "".join(f"<li><span class='meta'>{E(h['date'])}</span> {E(h['event'])}{(' — '+E(h['by'])) if h.get('by') else ''}</li>" for h in f["history"])
    prev = f["prevention"]; rep = f["repair"]
    body = f"""<p class="crumb"><a href="../index.html">Fault Atlas</a> › {E(f['id'])}</p>
<h1>{E(f['name'])}</h1><p class="fr big">{E(f.get('name_fr',''))}</p>
<div class="badges"><span class="pill" style="--c:{d[2]}">{E(d[0])}</span><span class="pill grey">{E(CLASS[f['class']])}</span><span class="pill grey">layer: {E(f['layer'])}</span><span class="pill grey">injection: {E(f.get('injection','—'))}</span><span class="pill warn">{E(f['status'].replace('_',' '))}</span></div>
<div class="facts"><div><h3>Damage in the graph</h3><p><strong>{E(d[0])}</strong> — {E(d[1])}.</p></div>
<div><h3>Can code cancel it?</h3><p>{'Yes' if prev['cancellable_by_code'] else 'No'}{('. Refusal clause: '+E(prev['refusal_clause'])) if prev.get('refusal_clause') else ''}{('. '+E(prev['note'])) if prev.get('note') else ''}.</p></div>
<div><h3>Can a deletion-only repair restore the truth?</h3><p><strong>{E(REACH[rep['reachable_by_deletion']])}</strong>{(' — '+E(rep['note'])) if rep.get('note') else ''}.</p></div>
<div><h3>Which truth can judge it</h3><p>{', '.join(E(JUDGE[j]) for j in f['judgeable_by']) or '<span class="muted">none known yet</span>'}.</p></div></div>
{('<div class="note">Measured absent in: '+E('; '.join(f['observed_absent_in']))+' — an absence is a result, not a gap.</div>') if f.get('observed_absent_in') else ''}
<h2>Where it was seen</h2>{seen}
<h2>Specimens</h2>{spec}
<h2>History</h2><ul class="hist">{hist}</ul>
<p class="muted">Record: <a href="../atlas.json">atlas.json</a> · <a href="{REPO}/blob/main/forms/">source file on GitHub</a> · <a href="{DATA}/forms/{E(f['id'])}">row in the data explorer</a></p>"""
    (SITE/"forms"/f"{f['id']}.html").write_text(layout(f"{f['name']} — Fault Atlas", body, depth=1, desc=f"{f['name']}: {d[0].lower()} — {d[1]}."))

(SITE/"atlas.json").write_text(json.dumps({"version": VERSION, "doi": DOI, "forms": forms}, ensure_ascii=False))
(SITE/"style.css").write_text("""
:root{--bg:#ffffff;--bg-elev:#f7f7f9;--surface:#ececf0;--line:rgba(10,10,11,.08);--line-strong:rgba(10,10,11,.16);--fg:#0a0a0b;--muted:rgba(10,10,11,.62);--luxe:rgba(10,10,11,.7);
--acc:#0969da;--acc-deep:#0550ae;--acc-soft:rgba(9,105,218,.08);--green:#00e896;
--sans:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--serif:"Fraunces","Spectral",ui-serif,Georgia,serif;--mono:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--acc);text-decoration:none}a:hover{color:var(--acc-deep);text-decoration:underline}
.top{display:flex;justify-content:space-between;align-items:center;padding:16px 5vw;border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:2}
.brand{display:inline-flex;align-items:center;gap:10px;font-weight:600;letter-spacing:-.01em;color:var(--fg);font-size:17px}.brand img{border-radius:5px}.brand .by{font-weight:400;color:var(--muted);font-size:14px;margin-left:2px}
.top nav a{margin-left:22px;color:var(--fg);font-size:14px;font-weight:500}.top nav a:hover{color:var(--acc);text-decoration:none}
main{max-width:1120px;margin:0 auto;padding:28px 5vw 72px}
.hero{padding:48px 0 16px}
.eyebrow{font-family:var(--serif);font-style:italic;font-weight:300;font-size:.98rem;color:var(--luxe);letter-spacing:.02em;display:inline-flex;align-items:center;gap:12px;margin:0 0 18px}.eyebrow::before{content:"";width:28px;height:1px;background:var(--acc);opacity:.65}
h1{font-size:clamp(30px,4.6vw,50px);line-height:1.08;margin:0 0 18px;letter-spacing:-.025em;max-width:22ch;font-weight:600}
h2{font-size:26px;letter-spacing:-.02em;margin:38px 0 12px;font-weight:600}h3{margin:0 0 6px;font-size:15px;letter-spacing:-.01em;font-weight:600}
.lead{font-size:18px;max-width:72ch;color:var(--luxe)}.cta{margin:22px 0 0}
.btn{display:inline-block;padding:10px 18px;border-radius:8px;background:var(--acc);color:#fff;font-weight:600;margin:0 8px 8px 0;font-size:15px}.btn:hover{background:var(--acc-deep);color:#fff;text-decoration:none}.btn.ghost{background:transparent;color:var(--acc);border:1px solid var(--line-strong)}.btn.ghost:hover{background:var(--acc-soft)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:30px 0 40px}
.card{display:block;background:var(--bg-elev);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:10px;padding:16px 18px;color:var(--fg);transition:border-color .15s}.card:hover{text-decoration:none;border-color:var(--c);background:#fff}
.card .n{display:block;font-size:36px;font-weight:600;line-height:1;letter-spacing:-.03em;font-family:var(--mono)}.card .t{display:block;font-weight:600;margin-top:8px}.card .d{display:block;font-size:13px;color:var(--muted);margin-top:4px;line-height:1.45}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 12px}input,select{font:inherit;font-size:15px;padding:9px 12px;border:1px solid var(--line-strong);border-radius:8px;background:#fff;color:var(--fg)}input{flex:1;min-width:220px}input:focus,select:focus{outline:2px solid var(--acc-soft);border-color:var(--acc)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}table{border-collapse:collapse;width:100%;min-width:780px}th,td{text-align:left;padding:11px 14px;border-top:1px solid var(--line);vertical-align:top}th{border-top:0;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;background:var(--bg-elev)}td.num{text-align:right;font-family:var(--mono);font-size:14px}
.pill{display:inline-block;white-space:nowrap;padding:2px 10px;border-radius:999px;font-size:12.5px;font-weight:600;color:#fff;background:var(--c);letter-spacing:.01em}.pill.grey{background:var(--surface);color:var(--fg);font-weight:500}.pill.warn{background:#fff3c4;color:#6b4c00;font-weight:500}
.fr{color:var(--muted);font-size:13px;font-family:var(--serif);font-style:italic}.fr.big{font-size:17px;margin-top:-10px}.muted{color:var(--muted)}
.about{margin-top:56px;border-top:1px solid var(--line);padding-top:32px}.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}.cols p{margin:0;color:var(--luxe);font-size:15px}
.crumb{color:var(--muted);font-size:14px;font-family:var(--mono)}.badges{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 22px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;background:var(--bg-elev);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:26px}.facts p{margin:0;font-size:15px}
.note{background:#fff7ed;color:#7c2d12;border:1px solid #fed7aa;border-radius:8px;padding:10px 14px;margin-bottom:22px;font-size:15px}
.obs{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:10px 0}.obs p{margin:0}.meta{color:var(--muted);font-size:13px;margin:0 0 8px;font-family:var(--mono)}details{margin-top:8px}details summary{cursor:pointer;color:var(--muted);font-size:14px}details .fr{display:block;margin-top:8px;font-size:14px}
.hist{padding-left:18px}.hist li{margin:5px 0;font-size:15px}code{background:var(--surface);padding:1px 6px;border-radius:4px;font-size:88%;font-family:var(--mono)}
footer{border-top:1px solid var(--line);padding:24px 5vw 40px;font-size:14px;color:var(--muted);background:var(--bg-elev)}footer p{max-width:1120px;margin:6px auto}
""")
print(f"site: {len(forms)} form pages + index, v{VERSION}")
