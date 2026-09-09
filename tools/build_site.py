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
import datetime
BUILT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

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
def corpus_short(text):
    t = text.lower()
    for key, label in [("eur-lex","EUR-Lex / Cellar"),("cellar","EUR-Lex / Cellar"),("openalex","OpenAlex"),("openaire","OpenAIRE"),("wikidata","Wikidata"),("faers","FDA FAERS"),
                       ("pubtator","PubTator3"),("mesh","MeSH history"),("author keyword","PubMed author keywords"),("mots-clés","PubMed author keywords"),("baseline","PubMed baseline 2026-08-18"),
                       ("funding","PubMed funding table"),("authors table","PubMed authors table"),
                       ("jats","Europe PMC (272 JATS articles)"),("europe pmc","Europe PMC (272 JATS articles)"),
                       ("migraine","biomedical PDFs 1957-1987"),("pdfs 1957","biomedical PDFs 1957-1987"),("outside biomedicine","arXiv / PLOS / HAL 2021-2026"),
                       ("pubmed abstracts","PubMed abstracts pre-1990"),("arginine","PubMed abstracts pre-1990"),("p6","synthetic tier P6 (VERDAL)"),("palier","synthetic tier P6 (VERDAL)")]:
        if key in t: return label
    return text[:40]
def corpora_of(f): 
    seen = []
    for s in f["seen"]:
        c = corpus_short(s["corpus"]); seen.append(c) if c not in seen else None
    return seen

E = html.escape

def layout(title, body, depth=0, desc=""):
    p = "../"*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc or 'Observed fault forms in knowledge graphs built from documents, with provenance, damage and the truth that judges them.')}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:ital,opsz,wght,SOFT@1,9..144,300,0&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}style.css"></head><body>
<header class="top"><a class="brand" href="{p}index.html"><img src="{p}favicon.svg" alt="" width="22" height="22"> Fault Atlas <span class="by">by Loxyn</span></a>
<nav><a href="{p}index.html#forms">Forms</a><a href="{p}corpora.html">Corpora</a><a href="{p}probes.html">Probes</a><a href="{p}index.html#about">About</a><a href="{DATA}">Data &amp; API</a><a href="{REPO}">GitHub</a><a href="https://doi.org/{DOI}">DOI</a></nav></header>
<main>{body}</main>
<footer><p><strong>Fault Atlas</strong> v{E(VERSION)} · built {BUILT} · Loxyn SAS, Lyon · Gracia S., Bagnol-Lebon C., Comtet Y. · records CC BY-SA 4.0, tools Apache 2.0 · <a href="https://doi.org/{DOI}">doi:{DOI}</a> · <a href="{REPO}">source</a> · <a href="mailto:contact@loxyn.ai">contact@loxyn.ai</a></p>
<p class="muted">Every record is still <code>migrated_unreviewed</code>: classified by one reader, awaiting a second. The JSON file is the record of truth; this site is a view rebuilt at each release.</p></footer>
</body></html>"""

# ── index ──
counts = Counter(f["damage"] for f in forms)
GRAPH_LAYERS = {"⑥","⑦","⑧","⑨"}
def is_graph_layer(layer):
    L = set(re.findall(r"[①-⑬]", layer)); return bool(L & GRAPH_LAYERS) and not (L - GRAPH_LAYERS - {"⑩"})
gcounts = Counter(f["damage"] for f in forms if is_graph_layer(f["layer"]))
cards = "".join(f"""<a class="card" href="#forms" data-damage="{k}" style="--c:{v[2]}"><span class="n">{counts.get(k,0)}<small> · {gcounts.get(k,0)} in graph layers</small></span><span class="t">{E(v[0])}</span><span class="d">{E(v[1])}</span></a>""" for k,v in DAMAGE.items())
rows = "".join(f"""<tr data-damage="{f['damage']}" data-class="{f['class']}" data-layer="{E(f['layer'])}" data-src="{E(" ".join(corpora_of(f)).lower())}" data-text="{E((f['name']+' '+f.get('name_fr','')+' '+' '.join(corpora_of(f))).lower())}">
<td><a href="forms/{f['id']}.html">{E(f['name'])}</a><br><span class="fr">{E(f.get('name_fr',''))}</span></td>
<td><span class="pill" style="--c:{DAMAGE[f['damage']][2]}">{E(DAMAGE[f['damage']][0])}</span></td>
<td>{E(CLASS[f['class']])}</td><td>{E(f['layer'])}</td><td class="src">{E(" · ".join(corpora_of(f)) or "—")}</td><td>{E(REACH[f['repair']['reachable_by_deletion']])}</td></tr>""" for f in forms)
index = f"""
<section class="hero"><p class="eyebrow">A library of observed fault forms in knowledge graphs built from documents</p>
<h1>Every fault has a form. Every form does one of seven things to the graph.</h1>
<p class="lead">{len(forms)} forms observed on real corpora, each with its provenance, the damage it causes, whether code can cancel it, whether a deletion-only repair can restore the truth, and which kind of truth can judge it. A repair that holds on one form of a damage may fail on another form of the same damage: this is the test matrix that says which.</p>
<p class="cta"><a class="btn" href="#forms">Browse the forms</a> <a class="btn ghost" href="{DATA}">Query the data</a> <a class="btn ghost" href="propose.html">Propose a form</a></p></section>
<section class="grid" id="damages">{cards}</section>
<section id="forms"><div class="bar"><input id="q" type="search" placeholder="Search a form…" aria-label="Search">
<select id="fd"><option value="">All damages</option>{''.join(f'<option value="{k}">{E(v[0])}</option>' for k,v in DAMAGE.items())}</select>
<select id="fc"><option value="">All classes</option>{''.join(f'<option value="{k}">{E(v)}</option>' for k,v in CLASS.items())}</select>
<select id="fl"><option value="">All layers</option>{''.join(f'<option value="{E(l)}">{E(l)}</option>' for l in sorted({f["layer"] for f in forms}))}</select>
<span id="count" class="muted"></span></div>
<div class="tablewrap"><table id="t"><thead><tr><th>Form</th><th>Damage</th><th>Class</th><th>Layer</th><th>Seen on</th><th>Deletion repairs it (classified)</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="about" class="about"><h2>What a record says</h2>
<div class="cols"><div><h3>Seven damages</h3><p>What a fault does to the graph: merge, split, spurious edge, missing, wrong value, wrong label, anachronism. The 113 difficulties observed in August 2026, however different they look, each produce one of these. Verified line by line.</p></div>
<div><h3>Two counts, always together</h3><p>Each damage card shows two numbers: all forms, and forms whose layer is a graph layer — resolution, schema, coherence, structure — where the phenomenon is itself a graph damage rather than a reading failure felt downstream. Deletion-only repair fully addresses one damage, the spurious edge; the identity damages, merge and split, it never touches.</p></div>
<div><h3>Layers</h3><p>Where the form bites: the pixel, the reading, the utterance, the extraction, the anchoring, the resolution, the schema, the coherence, the structure. A layout fault is a reading failure whose downstream effect on the graph is a missing fact: the damage says what happens to the graph, the layer says where it starts. Filter by layer to separate the two.</p></div>
<div><h3>Four classes</h3><p>Whether deterministic code cancels the form before it enters the graph, can abstain on it, cannot see it from inside, or whether it needs meaning. Half of what was observed is cancelled by code once; the other half is the real benchmark.</p></div>
<div><h3>Provenance, not opinion</h3><p>A form enters with a verbatim excerpt from a named corpus, a date, an observer. Cases come with counter-examples. A refuted form stays, marked refuted. Nothing is deleted.</p></div>
<div><h3>Why it matters</h3><p>Graph repair is evaluated against constraints the graph must satisfy, not against what is true. The atlas is half of an answer key: the map of forms by damage, with the kind of truth that can judge each. The other half, the truth itself, is built on it.</p></div></div>
<p>Met a form on your corpus? <a href="propose.html">Propose it</a> with its excerpt, corpus and date — no code, no account. Or, if you prefer, open an issue or a pull request on GitHub. A second reader reviews; a contested form stays recorded as contested; nothing enters unreviewed. Cite: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). <em>Fault Atlas.</em> Loxyn SAS, Lyon. Zenodo. <a href="https://doi.org/{DOI}">doi:{DOI}</a>.</p></section>
<script>
const q=document.getElementById('q'),fd=document.getElementById('fd'),fc=document.getElementById('fc'),fl=document.getElementById('fl'),rows=[...document.querySelectorAll('#t tbody tr')],c=document.getElementById('count');
function apply(){{const s=q.value.toLowerCase(),d=fd.value,k=fc.value,l=fl.value;let n=0;for(const r of rows){{const ok=(!d||r.dataset.damage===d)&&(!k||r.dataset.class===k)&&(!l||r.dataset.layer===l)&&(!s||r.dataset.text.includes(s));r.hidden=!ok;if(ok)n++;}}c.textContent=n+' of '+rows.length;}}
[q,fd,fc,fl].forEach(e=>e.addEventListener('input',apply));document.querySelectorAll('.card').forEach(a=>a.addEventListener('click',()=>{{fd.value=a.dataset.damage;apply();}}));apply();
</script>"""
CORPUS_NAMES = {json.loads(cf.read_text())["id"]: json.loads(cf.read_text())["name"] for cf in (ROOT/"corpora").glob("*.json")}
(SITE/"index.html").write_text(layout("Fault Atlas", index))

# ── form pages ──
for f in forms:
    d = DAMAGE[f["damage"]]
    src_name = next(x.name for x in (ROOT/"forms").glob(f"{f['id']}-*.json"))
    (SITE/"forms"/f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=2)+"\n")
    probes_by_file = {pr["file"]: pr for pr in f.get("probes", [])}
    def doc_link(doc, corpus_id):
        """A clickable link to the very document, per corpus."""
        import re as _re
        m = _re.search(r'(PMC\d+)', doc)
        if corpus_id == "corpus-europe-pmc-jats-2023-2026" and m:
            return f'<a href="https://europepmc.org/article/PMC/{m.group(1)}">{E(m.group(1))}</a> <a class="xml" href="https://www.ebi.ac.uk/europepmc/webservices/rest/{m.group(1)}/fullTextXML" title="the JATS XML the probe read">xml</a>'
        m = _re.search(r'PMID (\d+)', doc)
        if m:
            return f'<a href="https://pubmed.ncbi.nlm.nih.gov/{m.group(1)}/">PMID {m.group(1)}</a>'
        if doc.startswith("http://publications.europa.eu/resource/cellar/"):
            return f'<a href="{E(doc)}">{E(doc.rsplit("/",1)[-1])}</a>'
        if _re.fullmatch(r'[0-9]\d{4}[A-Z]{1,2}\d{4}(\(\d\d\))?(R\(\d\d\))?', doc):
            return f'<a href="https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:{E(doc)}">CELEX {E(doc)}</a>'
        return E(doc)
    def probe_block(file):
        pr = probes_by_file.get(file)
        if not pr: return ""
        r = pr.get("result", {})
        head = f"{r.get('count')}/{r.get('of')} documents" if r.get("of") is not None else f"{r.get('count')} results"
        code = (ROOT/pr["file"]).read_text(encoding="utf-8") if (ROOT/pr["file"]).is_file() else ""
        carriers = []
        if r.get("carriers_file") and (ROOT/r["carriers_file"]).is_file():
            carriers = [(c["document"], c.get("evidence", [])) for c in json.loads((ROOT/r["carriers_file"]).read_text())["carriers"]]
        elif r.get("examples"):
            carriers = [(n, e) for n, e in r["examples"]]
        def li(n, e):
            ev = (" — <span class='ev'>" + E(" | ".join(map(str, e)))[:260] + "</span>") if e else ""
            return f"<li>{doc_link(n, pr['corpus_id'])}{ev}</li>"
        first, rest = carriers[:12], carriers[12:]
        docs = ""
        if carriers:
            docs = f"<h4>See the trap in the documents (what a graph would fall on; whether a graph does fall is what a bench measures)</h4><ol class='docs'>" + "".join(li(n, e) for n, e in first) + "</ol>"
            if rest:
                docs += f"<details><summary>the other {len(rest)} documents</summary><ol class='docs' start='13'>" + "".join(li(n, e) for n, e in rest) + "</ol></details>"
            if r.get("carriers_file"):
                docs += f"<p class='meta'>Full list with evidence: <a href='{REPO}/blob/main/{E(r['carriers_file'])}'>{E(r['carriers_file'].split('/')[-1])}</a></p>"
        elif r.get("count") == 0:
            docs = "<p class='meta'>No document carries it in this corpus: the probe ran on every document and found nothing. That is the measurement.</p>"
        strata = (" · by stratum: " + ", ".join(f"{E(k)} {v}" for k, v in r["strata"].items())) if r.get("strata") else ""
        verdict = "the re-run figure is the excerpt's figure" if pr.get("matches_excerpt") else "the re-run figure differs from the excerpt's figure — both kept"
        return f"""<div class="probe"><p class="probe-head"><strong>How to find it again: {E(head)}</strong> · {E(pr['kind'])} probe, run {E(r.get('date','?'))} · {E(verdict)}</p>
{docs}
{('<p class="note">'+E(pr['note'])+'</p>') if pr.get('note') else ''}
<details class="code"><summary>The exact probe (code) · <code>{E(pr['file'].split('/')[-1])}</code>{strata}</summary>
<p class="meta">Run: <code>{E(pr.get('run',''))}</code> · <a href="{REPO}/blob/main/{E(pr['file'])}">{E(pr['file'])}</a> · the population searched (the denominator): <a href="../corpora/{E(pr['corpus_id'])}.html">{E(CORPUS_NAMES.get(pr['corpus_id'], pr['corpus_id']).split(' — ')[0])}</a>{(' · written '+E(pr['written'])) if pr.get('written') else ''}{(' · '+E(r['by'])) if r.get('by') else ''}</p>
<pre><code>{E(code)}</code></pre></details></div>"""
    seen = "".join(f"""<article class="obs"><p class="meta"><strong>{E(corpus_short(s['corpus']))}</strong> · {E(s['corpus'])} · {E(s['date'])}{(' · '+E(s['observer'])) if s.get('observer') else ''}{(' · '+E(s['organisation'])) if s.get('organisation') else ''}</p>
<p>{E(s.get('excerpt_en', s['excerpt']))}</p>{('<details><summary>Original note ('+E(s.get('lang','fr'))+')</summary><p class="fr">'+E(s['excerpt'])+'</p></details>') if s.get('excerpt_en') and s.get('excerpt_en')!=s['excerpt'] else ''}{probe_block(s.get('probe')) if s.get('probe') else ('<p class="noprobe">Cannot be shown yet: this figure was counted in August 2026 by code that was not saved, so no document can be pointed at. A probe is still to write for it. (The population searched is described on the <a href="../corpora/'+E(s['corpus_id'])+'.html">corpus page</a>; that page holds no fault.)</p>' if s.get('corpus_id') else '')}</article>""" for s in f["seen"]) or "<p class='muted'>No observation yet: this form is a hypothesis, not an observation.</p>"
    cases = f["specimens"]["cases"]; cex = f["specimens"]["counter_examples"]
    spec = (f"<p>{len(cases)} case(s), {len(cex)} counter-example(s).</p>" if cases or cex else "<p class='muted'>Specimens not yet transcribed into this record.</p>")
    hist = "".join(f"<li><span class='meta'>{E(h['date'])}</span> {E(h['event'])}{(' — '+E(h['by'])) if h.get('by') else ''}</li>" for h in f["history"])
    prev = f["prevention"]; rep = f["repair"]
    body = f"""<p class="crumb"><a href="../index.html">Fault Atlas</a> › {E(f['id'])}</p>
<h1>{E(f['name'])}</h1><p class="fr big">{E(f.get('name_fr',''))}</p><p class="found">Found by <strong>{E(f.get("origin",{}).get("organisation","—"))}</strong>{(" — "+E(f["origin"]["campaign"])) if f.get("origin",{}).get("campaign") else ""}{(" · first seen "+E(f["seen"][0]["date"])) if f["seen"] else ""}</p><p class="found">Seen on: <strong>{E(" · ".join(corpora_of(f)) or "no observation yet")}</strong></p>
<div class="badges"><span class="pill" style="--c:{d[2]}">{E(d[0])}</span><span class="pill grey">from: {E(f.get("origin",{}).get("organisation","—"))}</span><span class="pill grey">{E(CLASS[f['class']])}</span><span class="pill grey">layer: {E(f['layer'])}</span><span class="pill grey">injection: {E(f.get('injection','—'))}</span><span class="pill warn">{E(f['status'].replace('_',' '))}</span></div>
<div class="facts"><div><h3>Damage in the graph</h3><p><strong>{E(d[0])}</strong> — {E(d[1])}.</p></div>
<div><h3>Can code cancel it?</h3><p>{'Yes' if prev['cancellable_by_code'] else 'No'}{('. Refusal clause: '+E(prev['refusal_clause'])) if prev.get('refusal_clause') else ''}{('. '+E(prev['note'])) if prev.get('note') else ''}.</p></div>
<div><h3>Can a deletion-only repair restore the truth? <span class="opt">classified, not measured</span></h3><p><strong>{E(REACH[rep['reachable_by_deletion']])}</strong>{(' — '+E(rep['note'])) if rep.get('note') else ''}.</p></div>
<div><h3>Which truth can judge it</h3><p>{', '.join(E(JUDGE[j]) for j in f['judgeable_by']) or '<span class="muted">none known yet</span>'}.</p></div></div>
{('<div class="note">Measured absent in: '+E('; '.join(f['observed_absent_in']))+' — an absence is a result, not a gap.'+''.join(probe_block(pr['file']) for pr in f.get('probes', []) if pr['file'] not in {x.get('probe') for x in f['seen']})+'</div>') if f.get('observed_absent_in') else ''.join(probe_block(pr['file']) for pr in f.get('probes', []) if pr['file'] not in {x.get('probe') for x in f['seen']})}
<h2>Where it was seen</h2>{seen}
<h2>Specimens</h2>{spec}
<h2>History</h2><ul class="hist">{hist}</ul>
<p class="muted">Record: <a href="../atlas.json">atlas.json</a> · <a href="{REPO}/blob/main/forms/{E(src_name)}">source file on GitHub</a> · <a href="{E(f['id'])}.json">this record as JSON</a> · <a href="{DATA}/forms/{E(f['id'])}">row in the data explorer</a></p>"""
    (SITE/"forms"/f"{f['id']}.html").write_text(layout(f"{f['name']} — Fault Atlas", body, depth=1, desc=f"{f['name']}: {d[0].lower()} — {d[1]}."))


# ── probes page ──
prow = ""
for f in forms:
    for pr in f.get("probes", []):
        r = pr.get("result", {})
        head = f"{r.get('count')}/{r.get('of')}" if r.get("of") is not None else f"{r.get('count')} rows"
        prow += f"""<tr><td><a href="forms/{E(f['id'])}.html">{E(f['id'])}</a></td><td>{E(f['name'])}</td><td>{E(pr['kind'])}</td><td><a href="{REPO}/blob/main/{E(pr['file'])}">{E(pr['file'].split('/')[-1])}</a></td><td><a href="corpora/{E(pr['corpus_id'])}.html">{E(CORPUS_NAMES.get(pr['corpus_id'], pr['corpus_id']).split(' — ')[0][:48])}</a></td><td>{E(head)}</td><td>{E(r.get('date',''))}</td><td>{'yes' if pr.get('matches_excerpt') else 'no'}</td></tr>"""
nprobes = sum(len(f.get("probes", [])) for f in forms)
(SITE/"probes.html").write_text(layout("Probes — Fault Atlas", f"""<p class="crumb"><a href="index.html">Fault Atlas</a> › probes</p><h1>Exact probes</h1>
<p class="lead">{nprobes} probes on {sum(1 for f in forms if f.get('probes'))} forms. A probe is the exact question asked of a corpus, kept verbatim: a Python regex on one document, a SPARQL query on a public endpoint, a shell request with its headers. It repairs nothing and decides nothing; it answers "is this fault here, and where?". Anyone can run it again: <code>python3 tools/run_probe.py &lt;probe&gt; &lt;corpus&gt;</code>. The last column says whether the re-run figure is the one quoted in the observation; when it is not, both figures are kept and the difference is stated on the form.</p>
<div class="tablewrap"><table><thead><tr><th>Form</th><th>Name</th><th>Kind</th><th>Probe</th><th>Corpus</th><th>Result</th><th>Run on</th><th>Matches excerpt</th></tr></thead><tbody>{prow}</tbody></table></div>"""))

# ── propose page ──
dmg_cards = "".join(f"""<label class="dcard" style="--c:{v[2]}"><input type="radio" name="damage" value="{k}" required><span class="dt">{E(v[0])}</span><span class="dd">{E(v[1])}</span></label>""" for k,v in DAMAGE.items() if k!="CORPUS_PARAMETER") + """<label class="dcard" style="--c:#57534e"><input type="radio" name="damage" value="UNKNOWN"><span class="dt">I don't know</span><span class="dd">the reviewer will classify it</span></label>"""
propose_body = f"""<p class="crumb"><a href="index.html">Fault Atlas</a> › propose</p>
<h1>Propose a fault form</h1>
<p class="lead">You met a fault on a corpus that a graph would get wrong. Tell us what it is and show us the proof. A second reader reviews it, you get an answer by e-mail, and your name stays in the form's history.</p>
<div id="sent" class="note ok" hidden>Thank you. Your proposal is received and will be reviewed. You will get an answer at the address you gave.</div>
<div id="err" class="note" hidden></div>
<form class="propose" method="post" action="/propose">
<input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">

<fieldset><legend><span class="step">1</span> The fault</legend>
<div class="field"><label for="f-name">Give it a short name</label><input id="f-name" name="name" required maxlength="120" placeholder="Acronym reused for two different institutions"><p class="help">In English, like a title. The reviewer may rename it.</p></div>
<div class="field"><span class="lbl">What does it do to a graph?</span><div class="dgrid">{dmg_cards}</div></div>
<div class="field"><label for="f-why">Why is it a fault?</label><textarea id="f-why" name="why" required rows="3" maxlength="3000" placeholder="What a construction or repair system gets wrong on it, in a few sentences."></textarea></div>
</fieldset>

<fieldset><legend><span class="step">2</span> The proof</legend>
<div class="row"><div class="field"><label for="f-corpus">Corpus</label><input id="f-corpus" name="corpus" required maxlength="200" placeholder="EUR-Lex, Cellar snapshot 2026-09-01"><p class="help">Name it so that someone else can open it: source, version or date.</p></div>
<div class="field"><label for="f-doc">Document identifier <span class="opt">optional</span></label><input id="f-doc" name="document" maxlength="200" placeholder="CELEX number, PMC id, DOI…" style="--w:420px"></div></div>
<div class="row"><div class="field"><label for="f-date">When did you see it?</label><input id="f-date" name="date" type="date" required style="--w:200px"></div>
<div class="field"><label for="f-existing">Closest existing form <span class="opt">optional</span></label><input id="f-existing" name="existing" maxlength="40" placeholder="form-024" style="--w:240px"><p class="help">If you found one in the <a href="index.html#forms">list</a>.</p></div></div>
<div class="field"><label for="f-excerpt">Verbatim excerpt</label><textarea id="f-excerpt" name="excerpt" required rows="5" maxlength="4000" placeholder="Paste the text exactly as it appears, in its own language."></textarea><p class="help">This is the proof. Without it, a proposal is a hypothesis, not an observation.</p></div>
</fieldset>

<fieldset><legend><span class="step">3</span> You</legend>
<div class="row"><div class="field"><label for="f-who">Name and affiliation <span class="opt">optional</span></label><input id="f-who" name="who" maxlength="200" placeholder="Jane Doe, LIRIS"></div>
<div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" required maxlength="200" placeholder="you@lab.org"><p class="help">Only to answer you. Not published.</p></div></div>
<label class="check"><input type="checkbox" name="rule_public" value="yes" required><span>The excerpt comes from a public corpus, not from a client document, and contains no personal data.</span></label>
<label class="check"><input type="checkbox" name="rule_review" value="yes" required><span>I understand that a second reader reviews, that a contested form stays recorded as contested, and that my name stays in the form's history.</span></label>
</fieldset>

<p class="actions"><button class="btn" type="submit">Send the proposal</button> <span class="muted">or <a href="{REPO}/issues/new?template=propose-form.yml">open an issue on GitHub</a></span></p>
</form>
<script>const u=new URL(location.href);if(u.searchParams.get('sent')){{document.getElementById('sent').hidden=false;document.querySelector('form').hidden=true;}}
const e=u.searchParams.get('err');if(e){{const b=document.getElementById('err');b.hidden=false;b.textContent=e==='rate'?'Too many proposals from this address in one hour. Try again later.':e==='missing'?'Some required fields are missing or invalid: '+(u.searchParams.get('fields')||''):'The proposal could not be sent. Please try again or use GitHub.';}}</script>"""
(SITE/"propose.html").write_text(layout("Propose a fault form — Fault Atlas", propose_body))

# ── corpora: one page per corpus, plus an index ──
(SITE/"corpora").mkdir(exist_ok=True)
corp_index = ""
for cf in sorted((ROOT/"corpora").glob("*.json")):
    c = json.loads(cf.read_text())
    cid = c["id"]
    # forms on this corpus: with a probe / without
    with_probe, without = [], []
    for f in forms:
        pf = {pr["file"]: pr for pr in f.get("probes", []) if pr["corpus_id"] == cid}
        obs = [x for x in f["seen"] if x.get("corpus_id") == cid]
        absent = any(pr for pr in pf.values() if pr["file"] not in {x.get("probe") for x in f["seen"]})
        if any(x.get("probe") in pf for x in obs) or absent:
            for pr in pf.values():
                r = pr.get("result", {})
                with_probe.append((f, pr, f"{r.get('count')}/{r.get('of')}" if r.get("of") is not None else f"{r.get('count')} rows"))
        elif obs:
            without.append(f)
    body_c = f"<p class=\"crumb\"><a href=\"../index.html\">Fault Atlas</a> › <a href=\"../corpora.html\">corpora</a> › {E(cid)}</p><h1>{E(c['name'])}</h1>"
    body_c += "<p class=\"lead\">This page says <strong>which documents</strong> the corpus holds and <strong>how they were chosen</strong>. It does not find any fault: the exact probe that finds a fault sits on each form, listed at the bottom of this page.</p>"
    if c.get("source"): body_c += f"<p><strong>Source:</strong> {E(c['source'])}</p>"
    if c.get("harvested"): body_c += f"<p><strong>Harvested:</strong> {E(c['harvested'])}</p>"
    if c.get("selection"): body_c += f"<p><strong>How the documents were chosen:</strong> {E(c['selection'])}</p>"
    if c.get("queries"): body_c += "<h2>Selection queries</h2><p class=\"muted\">These queries chose the articles on Europe PMC, one per stratum. They are not the queries that find the faults.</p><ul>" + "".join(f"<li><code>{E(k)}</code>: <code>{E(v)}</code></li>" for k,v in c["queries"].items()) + "</ul>"
    if c.get("by_stratum"): body_c += "<p><strong>By stratum:</strong> " + ", ".join(f"{E(k)} {v}" for k,v in c["by_stratum"].items()) + f" — {c.get('count','')} articles</p>"
    if c.get("by_decade"): body_c += "<p><strong>By decade:</strong> " + ", ".join(f"{E(k)}s {v}" for k,v in c["by_decade"].items()) + f" — {c.get('count','')} records, {c.get('without_abstract','')} without abstract</p>"
    if c.get("note"): body_c += f"<p>{E(c['note'])}</p>"
    if c.get("populations"): body_c += "<h2>Populations</h2><ul>" + "".join(f"<li>{E(pp['name'])}{(' — '+E(pp['note'])) if pp.get('note') else ''}</li>" for pp in c["populations"]) + "</ul>"
    if c.get("how_to_reproduce"): body_c += f"<h2>How to get the same documents</h2><p>{E(c['how_to_reproduce'])}</p>"
    if c.get("articles"): body_c += f"<details><summary>The {len(c['articles'])} identifiers</summary><p class=\"ids\">" + " ".join(E(a.get('pmcid') or a.get('pmid') or '') for a in c['articles']) + "</p></details>"
    if c.get("observer_agreement"): body_c += f"<p><strong>Observer agreement:</strong> {E(json.dumps(c['observer_agreement'], ensure_ascii=False))}</p>"
    if c.get("lesson"): body_c += f"<p><em>{E(c['lesson'])}</em></p>"
    if with_probe:
        body_c += f"<h2>Forms found on this corpus, with the exact probe that finds them ({len(with_probe)})</h2><div class=\"tablewrap\"><table><thead><tr><th>Form</th><th>Name</th><th>Probe</th><th>Result</th></tr></thead><tbody>" + "".join(f"<tr><td><a href=\"../forms/{E(f['id'])}.html\">{E(f['id'])}</a></td><td>{E(f['name'])}</td><td><a href=\"{REPO}/blob/main/{E(pr['file'])}\">{E(pr['file'].split('/')[-1])}</a></td><td>{E(res)}</td></tr>" for f, pr, res in with_probe) + "</tbody></table></div>"
    if without:
        body_c += f"<h2>Forms measured on this corpus without a kept probe ({len(without)})</h2><p class=\"muted\">The figure in their observation was counted in August 2026 by code that was not saved. The corpus is reproducible; the count is not yet. Each is a probe still to write.</p><p>" + " · ".join(f"<a href=\"../forms/{E(f['id'])}.html\">{E(f['id'])}</a>" for f in without) + "</p>"
    body_c += f"<p class=\"muted\">Record: <a href=\"{REPO}/blob/main/corpora/{E(cf.name)}\">{E(cf.name)}</a></p>"
    (SITE/"corpora"/f"{cid}.html").write_text(layout(f"{c['name'].split(' — ')[0]} — Fault Atlas", body_c, depth=1))
    n_obs = sum(1 for f in forms for x in f["seen"] if x.get("corpus_id") == cid)
    corp_index += f"<section class=\"corpus\"><h2><a href=\"corpora/{E(cid)}.html\">{E(c['name'])}</a></h2><p>{E(c.get('selection', c.get('note', ''))[:260])}{'…' if len(c.get('selection', c.get('note', '')))>260 else ''}</p><p class=\"meta\">{n_obs} observation(s) · {len(with_probe)} exact probe(s){(' · '+str(len(without))+' figure(s) without a kept probe') if without else ''}{(' · harvested '+E(c['harvested'])) if c.get('harvested') else ''}</p></section>"
(SITE/"corpora.html").write_text(layout("Corpora — Fault Atlas", f"<p class=\"crumb\"><a href=\"index.html\">Fault Atlas</a> › corpora</p><h1>Observed corpora</h1><p class=\"lead\">One page per corpus: which documents it holds, how they were chosen, how to get them again. A corpus page never finds a fault; the exact probe that does sits on each form.</p>{corp_index}"))

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
.card .n{display:block;font-size:36px;font-weight:600;line-height:1;letter-spacing:-.03em;font-family:var(--mono)}.card .n small{display:block;font-size:12px;font-weight:500;color:var(--muted);font-family:var(--sans);letter-spacing:0;margin-top:4px}.card .t{display:block;font-weight:600;margin-top:8px}.card .d{display:block;font-size:13px;color:var(--muted);margin-top:4px;line-height:1.45}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 12px}input,select,textarea{font:inherit;font-size:15px;padding:10px 12px;border:1px solid var(--line-strong);border-radius:8px;background:#fff;color:var(--fg)}.bar input{flex:1;min-width:220px}input:focus,select:focus{outline:2px solid var(--acc-soft);border-color:var(--acc)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}table{border-collapse:collapse;width:100%;min-width:780px}th,td{text-align:left;padding:11px 14px;border-top:1px solid var(--line);vertical-align:top}th{border-top:0;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;background:var(--bg-elev)}td.num{text-align:right;font-family:var(--mono);font-size:14px}td.src{font-size:13px;color:var(--luxe)}
.pill{display:inline-block;white-space:nowrap;padding:2px 10px;border-radius:999px;font-size:12.5px;font-weight:600;color:#fff;background:var(--c);letter-spacing:.01em}.pill.grey{background:var(--surface);color:var(--fg);font-weight:500}.pill.warn{background:#fff3c4;color:#6b4c00;font-weight:500}
.fr{color:var(--muted);font-size:13px;font-family:var(--serif);font-style:italic}.fr.big{font-size:17px;margin-top:-10px}.muted{color:var(--muted)}
.about{margin-top:56px;border-top:1px solid var(--line);padding-top:32px}.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}.cols p{margin:0;color:var(--luxe);font-size:15px}
.crumb{color:var(--muted);font-size:14px;font-family:var(--mono)}.found{margin:-4px 0 14px;font-size:15px;color:var(--luxe)}.badges{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 22px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;background:var(--bg-elev);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:26px}.facts p{margin:0;font-size:15px}
.note{background:#fff7ed;color:#7c2d12;border:1px solid #fed7aa;border-radius:8px;padding:10px 14px;margin-bottom:22px;font-size:15px}
.obs{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:10px 0}.obs p{margin:0}.meta{color:var(--muted);font-size:13px;margin:0 0 8px;font-family:var(--mono)}details{margin-top:8px}details summary{cursor:pointer;color:var(--muted);font-size:14px}details .fr{display:block;margin-top:8px;font-size:14px}
.probe{margin-top:12px;border-top:1px dashed var(--line);padding-top:10px}.probe .probe-head{margin:0 0 6px;font-size:14px}.probe h4{margin:10px 0 4px;font-size:14px}.probe ol.docs{margin:0 0 6px 22px;padding:0;font-size:13.5px;line-height:1.5}.probe ol.docs li{margin:2px 0}.probe .ev{color:var(--muted)}.probe a.xml{font-family:var(--mono);font-size:11px;color:var(--muted);margin-left:2px}.probe details.code{margin-top:8px}.probe details.code summary{color:var(--muted);font-size:13.5px}.probe pre{margin:10px 0 0;padding:12px 14px;background:var(--bg-elev);border:1px solid var(--line);border-radius:8px;overflow-x:auto;font-size:12.5px;line-height:1.45;max-height:520px}.probe .note{margin:8px 0}.noprobe{margin-top:10px!important;border-top:1px dashed var(--line);padding-top:8px;font-size:13.5px;color:var(--muted)}
.corpus{border-top:1px solid var(--line);padding:18px 0}.corpus h2{scroll-margin-top:80px}.ids{font-family:var(--mono);font-size:12px;line-height:1.7;word-break:break-all}
.hist{padding-left:18px}.hist li{margin:5px 0;font-size:15px}code{background:var(--surface);padding:1px 6px;border-radius:4px;font-size:88%;font-family:var(--mono)}
.propose{max-width:700px}.propose fieldset{border:1px solid var(--line);border-radius:12px;padding:28px 28px 16px;margin:22px 0 30px;background:#fff}.propose legend{padding:0 10px;font-weight:600;font-size:17px;letter-spacing:-.01em;display:flex;align-items:center;gap:10px}
.step{display:inline-flex;width:26px;height:26px;border-radius:50%;background:var(--acc);color:#fff;font-size:13px;align-items:center;justify-content:center;font-family:var(--mono)}
.field{margin:0 0 22px}.field label,.field .lbl{display:block;font-weight:600;font-size:14px;margin-bottom:6px}.opt{font-weight:400;color:var(--muted);font-size:13px;margin-left:4px}
.field input,.field select,.field textarea{display:block;width:100%;max-width:var(--w,100%)}.field input[type=date]{max-width:200px}.field input#f-existing{max-width:240px}.field input#f-doc,.field input#f-who{max-width:420px}.field textarea{resize:vertical;line-height:1.5}.help{margin:7px 0 0;font-size:13px;color:var(--muted);line-height:1.5}
.row{display:block}
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:12px;margin-top:4px}.dcard{position:relative;display:block;border:1px solid var(--line-strong);border-left:4px solid var(--c);border-radius:10px;padding:13px 15px 13px 16px;cursor:pointer;background:#fff;transition:border-color .15s,box-shadow .15s}.dcard:hover{border-color:var(--c)}.dcard input{position:absolute;opacity:0;width:0;height:0}.dcard:has(input:checked){border-color:var(--c);box-shadow:0 0 0 3px var(--acc-soft);background:var(--bg-elev)}.dcard .dt{display:block;font-weight:600;font-size:14px}.dcard .dd{display:block;font-size:13px;color:var(--muted);margin-top:3px;line-height:1.45}
.check{display:flex;gap:12px;align-items:flex-start;margin:0;padding:14px 16px;font-size:14px;line-height:1.55;cursor:pointer;background:var(--bg-elev);border:1px solid var(--line);border-radius:9px}.check+.check{margin-top:10px}.check:hover{border-color:var(--line-strong)}.check input{width:18px;height:18px;margin:2px 0 0;flex:0 0 auto}
.actions{margin-top:26px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}.actions .btn{padding:13px 26px;font-size:15px}.hp{position:absolute;left:-9999px}.note.ok{background:#ecfdf5;color:#065f46;border-color:#a7f3d0}
footer{border-top:1px solid var(--line);padding:24px 5vw 40px;font-size:14px;color:var(--muted);background:var(--bg-elev)}footer p{max-width:1120px;margin:6px auto}
""")
print(f"site: {len(forms)} form pages + index, v{VERSION}")
