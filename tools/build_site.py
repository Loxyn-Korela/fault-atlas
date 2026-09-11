#!/usr/bin/env python3
"""Generate the public site (static HTML) from the form records. No framework, no dependency.
Output: site/  — index.html, forms/<id>.html, atlas.json (all records), style.css.
The JSON files remain the source of truth; the site is a view rebuilt at each release."""
import json, html, re, sys
from pathlib import Path
from collections import Counter, defaultdict

# Two languages, one generator. Run it twice: once plain for English, once with --fr.
# The records already hold both: name_fr for the names, and the French original of every excerpt,
# which is the language the observations were written in.
LANG = "fr" if "--fr" in sys.argv else "en"
T = {
 "eyebrow": {"en": "A library of observed fault forms in knowledge graphs built from documents",
             "fr": "Une bibliothèque de formes de fautes observées dans les graphes construits depuis des documents"},
 "h1": {"en": "Every fault has a form. Every form does one of seven things to the graph.",
        "fr": "Toute faute a une forme. Toute forme fait au graphe l'une de sept choses."},
 "browse": {"en": "Browse the forms", "fr": "Parcourir les formes"},
 "query": {"en": "Query the data", "fr": "Interroger les données"},
 "propose": {"en": "Propose a form", "fr": "Proposer une forme"},
 "search": {"en": "Search a form…", "fr": "Chercher une forme…"},
 "all_damages": {"en": "All damages", "fr": "Tous les dégâts"},
 "all_classes": {"en": "All classes", "fr": "Toutes les classes"},
 "all_layers": {"en": "All layers", "fr": "Toutes les couches"},
 "any_cons": {"en": "Any consequence", "fr": "Toute conséquence"},
 "cons_none": {"en": "Consequence not judged", "fr": "Conséquence non jugée"},
 "any_mode": {"en": "Any failure mode", "fr": "Tout mode d'échec"},
 "mode_none": {"en": "Failure mode not recovered", "fr": "Mode d'échec non récupéré"},
 "any_era": {"en": "Any era", "fr": "Toute époque"},
 "era_none": {"en": "Era not measured", "fr": "Époque non mesurée"},
 "era_anc": {"en": "Ancient documents only", "fr": "Documents anciens seulement"},
 "era_both": {"en": "Both eras", "fr": "Les deux époques"},
 "era_mod": {"en": "Born with the modern", "fr": "Née avec le moderne"},
 "era_ns": {"en": "Era not settled", "fr": "Époque non tranchée"},
 "only_ex": {"en": "Only forms with an example", "fr": "Seulement les formes avec un exemple"},
 "th": {"en": ["Form","Damage","Date","Class","Layer","Corpus","Example"],
        "fr": ["Forme","Dégât","Date","Classe","Couche","Corpus","Exemple"]},
 "reach": {"en": " reach the graph", "fr": " atteignent le graphe"},
 "ex_yes": {"en": "example shown", "fr": "exemple montré"},
 "ex_no": {"en": "no example yet", "fr": "pas encore d'exemple"},
 "of": {"en": " of ", "fr": " sur "},
 "costs": {"en": "What it costs you", "fr": "Ce que ça vous coûte"},
 "costs_prop": {"en": "What it costs you — proposed, not judged in August",
                "fr": "Ce que ça vous coûte — proposé, non jugé en août"},
 "reaches": {"en": "How far it reaches in the base", "fr": "Jusqu'où ça porte dans la base"},
 "seen_years": {"en": "Seen in documents published", "fr": "Vue dans des documents publiés en"},
 "repairs": {"en": "Can a deletion repair it?", "fr": "Une suppression peut-elle la réparer ?"},
 "fails": {"en": "How it fails", "fr": "Comment elle échoue"},
 "applies": {"en": "When it applies", "fr": "Quand elle s'applique"},
 "switch": {"en": "Français", "fr": "English"},
 "sev": {"en": {"G1": ("Contaminates","The error lands on an entity, and every fact hanging from that entity inherits it. One wrong identity, and a whole neighbourhood of the graph answers wrongly."),
                "G2": ("Answers wrongly, in silence","A single false fact, local, and nothing signals it. You get an answer, it looks like every other answer, and it is wrong. This is the one a low prevalence must not excuse."),
                "G3": ("Hides","A hole. The graph is incomplete, not lying. What you are looking for is simply not there, and nothing tells you it should have been."),
                "G4": ("Stops before the graph","The fault never reaches the graph. It costs work upstream, not answers downstream.")},
         "fr": {"G1": ("Contamine","L'erreur se pose sur une entité, et tout fait qui y pend en hérite. Une identité fausse, et c'est tout un voisinage du graphe qui répond de travers."),
                "G2": ("Répond faux, en silence","Un seul fait faux, local, et rien ne le signale. Vous obtenez une réponse, elle ressemble à toutes les autres, et elle est fausse. C'est celle qu'une faible prévalence ne doit jamais excuser."),
                "G3": ("Cache","Un trou. Le graphe est incomplet, pas menteur. Ce que vous cherchez n'y est pas, et rien ne dit qu'il aurait dû y être."),
                "G4": ("S'arrête avant le graphe","La faute n'atteint jamais le graphe. Elle coûte du travail en amont, pas des réponses en aval.")}},
 "h_damage": {"en": "Damage in the graph", "fr": "Dégât dans le graphe"},
 "h_cancel": {"en": "Can code cancel it?", "fr": "Du code peut-il l'annuler ?"},
 "h_restore": {"en": "Can a deletion-only repair restore the truth?", "fr": "Une réparation par suppression seule rétablit-elle la vérité ?"},
 "h_judge": {"en": "Which truth can judge it", "fr": "Quelle vérité peut la juger"},
 "h_seen": {"en": "Where it was seen", "fr": "Où elle a été vue"},
 "h_spec": {"en": "Specimens", "fr": "Spécimens"},
 "h_hist": {"en": "History", "fr": "Historique"},
 "h_record": {"en": "What a record says", "fr": "Ce que dit une fiche"},
 "h_seven": {"en": "Seven damages", "fr": "Sept dégâts"},
 "h_counts": {"en": "Two counts, always together", "fr": "Deux comptes, toujours ensemble"},
 "h_layers": {"en": "Layers", "fr": "Couches"},
 "h_classes": {"en": "Four classes", "fr": "Quatre classes"},
 "h_prov": {"en": "Provenance, not opinion", "fr": "Provenance, pas opinion"},
 "h_why": {"en": "Why it matters", "fr": "Pourquoi ça compte"},
 "seen_on": {"en": "Seen on: ", "fr": "Vue sur : "},
 "nav_forms": {"en": "Forms", "fr": "Formes"},
 "nav_about": {"en": "About", "fr": "À propos"},
 "nav_data": {"en": "Data &amp; API", "fr": "Données et API"},
 "foot_note": {"en": "The JSON file is the record of truth; this site is a view rebuilt at each release. 43 forms of 162 are validated by a second reader; the rest carries its status on its own page.",
               "fr": "Le fichier JSON fait foi ; ce site en est une vue, reconstruite à chaque version. 43 formes sur 162 sont validées par une seconde lectrice, les autres portent leur statut sur leur fiche."},
}

def t(k):
    return T[k][LANG]

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT/"site" if LANG == "en" else ROOT/"site"/"fr"; (SITE/"forms").mkdir(parents=True, exist_ok=True)
import shutil; FAV = ROOT/"tools"/"favicon.svg"
if FAV.exists(): shutil.copy(FAV, SITE/"favicon.svg")
DOI = "10.5281/zenodo.22674547"; REPO = "https://github.com/Loxyn-Korela/fault-atlas"; DATA = "/data/fault-atlas"
VERSION = re.search(r"^version: (.+)$", (ROOT/"CITATION.cff").read_text(), re.M).group(1)
# The footer said v0.6.1 for six releases because this number lives in CITATION.cff and nobody
# bumped it. It cannot drift again: the build refuses when it disagrees with the changelog.
_LATEST = max(re.findall(r"^## (\d+\.\d+\.\d+)", (ROOT/"CHANGELOG.md").read_text(), re.M),
              key=lambda v: [int(x) for x in v.split(".")])
if VERSION != _LATEST:
    raise SystemExit(f"CITATION.cff says {VERSION}, CHANGELOG.md's newest entry is {_LATEST}. "
                     f"Bump CITATION.cff before building, or the site will publish a stale version.")
import datetime
BUILT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

DAMAGE_EN = {
 "MERGE": ("Merge", "two real things become one node"),
 "SPLIT": ("Split", "one thing becomes several nodes"),
 "SPURIOUS_EDGE": ("Spurious edge", "a relation the source never asserted"),
 "MISSING": ("Missing", "a node or relation the source asserts and the graph lacks"),
 "WRONG_VALUE": ("Wrong value", "a property, number or date is wrong"),
 "WRONG_LABEL": ("Wrong label", "an entity or relation type is wrong"),
 "ANACHRONISM": ("Anachronism", "a fact outside its validity interval, or a superseded status kept"),
 "CORPUS_PARAMETER": ("Corpus parameter", "not a damage: a property of the corpus composition"),
}
DAMAGE_FR = {
 "MERGE": ("Fusion", "deux choses réelles deviennent un seul nœud"),
 "SPLIT": ("Scission", "une chose devient plusieurs nœuds"),
 "SPURIOUS_EDGE": ("Arête fausse", "une relation que la source n'a jamais affirmée"),
 "MISSING": ("Manque", "un nœud ou une relation que la source affirme et que le graphe n'a pas"),
 "WRONG_VALUE": ("Mauvaise valeur", "une propriété, un nombre ou une date est faux"),
 "WRONG_LABEL": ("Mauvaise étiquette", "un type d'entité ou de relation est faux"),
 "ANACHRONISM": ("Anachronisme", "un fait hors de son intervalle de validité, ou un statut périmé conservé"),
 "CORPUS_PARAMETER": ("Paramètre de corpus", "pas un dégât : une propriété de la composition du corpus"),
}
DCOL = {"MERGE":"#b3261e","SPLIT":"#c2410c","SPURIOUS_EDGE":"#a16207","MISSING":"#3f6212",
        "WRONG_VALUE":"#0e7490","WRONG_LABEL":"#4338ca","ANACHRONISM":"#7e22ce","CORPUS_PARAMETER":"#57534e"}
DAMAGE = {k: (v[0], v[1], DCOL[k]) for k, v in (DAMAGE_EN if LANG == "en" else DAMAGE_FR).items()}

REACH = {"yes": "yes", "no": "no", "partial": "partial", "unknown": "unknown"} if LANG == "en" else {"yes": "oui", "no": "non", "partial": "partiel", "unknown": "inconnu"}
JUDGE = ({"construction": "truth by construction", "registry": "an official registry", "curated": "a curated database", "dated_future": "the dated future", "closed_world": "a closed world"} if LANG == "en" else
         {"construction": "une vérité par construction", "registry": "un registre officiel", "curated": "une base curatée", "dated_future": "le futur daté", "closed_world": "un monde fermé"})
MODE_LABEL = ({"PROP": "Identity, and it propagates", "FAUX": "A false fact", "MANQ": "A gap", "MES": "A corpus property"} if LANG == "en" else
              {"PROP": "L'identité, et ça se propage", "FAUX": "Un fait faux", "MANQ": "Un trou", "MES": "Une propriété du corpus"})
COLOUR = {"G1": "#9B2C2C", "G2": "#8A4B12", "G3": "#1F4E79", "G4": "#5B6670"}
SEVERITY = {k: (v[0], COLOUR[k], v[1]) for k, v in t("sev").items()}
CLASS = ({"DEFEATED": "Cancelled by code", "DEFEATED_IF_XML": "Cancelled by code when the source is XML", "REFUSABLE": "Code can abstain on it",
          "SILENT_FALSE": "Silent false: code cannot see it from inside", "IRREDUCIBLE": "Irreducible: needs meaning", "UNCLASSIFIED": "Unclassified"} if LANG == "en" else
         {"DEFEATED": "Annulée par du code", "DEFEATED_IF_XML": "Annulée par du code quand la source est en XML", "REFUSABLE": "Le code peut s'abstenir",
          "SILENT_FALSE": "Faux silencieux : le code ne peut pas la voir de l'intérieur", "IRREDUCIBLE": "Irréductible : demande du sens", "UNCLASSIFIED": "Non classée"})
CLASS_SHORT = ({"DEFEATED": "Cancelled by code", "DEFEATED_IF_XML": "Cancelled if XML", "REFUSABLE": "Can abstain",
                "SILENT_FALSE": "Silent false", "IRREDUCIBLE": "Irreducible", "UNCLASSIFIED": "Unclassified"} if LANG == "en" else
               {"DEFEATED": "Annulée par du code", "DEFEATED_IF_XML": "Annulée si XML", "REFUSABLE": "Peut s'abstenir",
                "SILENT_FALSE": "Faux silencieux", "IRREDUCIBLE": "Irréductible", "UNCLASSIFIED": "Non classée"})
JUDGE = {"construction": "truth by construction", "registry": "an official registry", "curated": "a curated database", "dated_future": "the dated future", "closed_world": "a closed world"}

forms = [json.loads(f.read_text()) for f in sorted((ROOT/"forms").glob("*.json"))]
def corpus_short(text):
    t = text.lower()
    for key, label in [("eur-lex","EUR-Lex / Cellar"),("cellar","EUR-Lex / Cellar"),("openalex","OpenAlex"),("openaire","OpenAIRE"),("wikidata","Wikidata"),("faers","FDA FAERS"),
                       ("pubtator","PubTator3"),("mesh","MeSH history"),("author keyword","PubMed author keywords"),("mots-clés","PubMed author keywords"),("baseline","PubMed baseline 2026-08-18"),
                       ("funding","PubMed funding table"),("authors table","PubMed authors table"),
                       ("jats","Europe PMC (JATS, 2023-2026)"),("europe pmc","Europe PMC (JATS, 2023-2026)"),
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

# where the other language lives, from a page at this depth
SWITCH = ({0: "fr/index.html", 1: "../fr/index.html"} if LANG == "en"
          else {0: "../index.html", 1: "../../index.html"})
def layout(title, body, depth=0, desc=""):
    p = "../"*depth
    return f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc or 'Observed fault forms in knowledge graphs built from documents, with provenance, damage and the truth that judges them.')}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:ital,opsz,wght,SOFT@1,9..144,300,0&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="{p}style.css"></head><body>
<header class="top"><a class="brand" href="{p}index.html"><img src="{p}favicon.svg" alt="" width="22" height="22"> Fault Atlas <span class="by">by Loxyn</span></a>
<nav><a href="{p}index.html#forms">{E(t("nav_forms"))}</a><a href="{p}index.html#about">{E(t("nav_about"))}</a><a href="{DATA}">{E(t("nav_data"))}</a><a href="{REPO}">GitHub</a><a href="https://doi.org/{DOI}">DOI</a><a class="lang" href="{SWITCH[depth]}">{E(t("switch"))}</a></nav></header>
<main>{body}</main>
<footer><p><strong>Fault Atlas</strong> v{E(VERSION)} · built {BUILT} · Loxyn SAS, Lyon · Gracia S., Bagnol-Lebon C., Comtet Y. · records CC BY-SA 4.0, tools Apache 2.0 · <a href="https://doi.org/{DOI}">doi:{DOI}</a> · <a href="{REPO}">source</a> · <a href="mailto:contact@loxyn.ai">contact@loxyn.ai</a></p>
<p class="muted">{E(t("foot_note"))}</p></footer>
</body></html>"""

# ── index ──
counts = Counter(f["damage"] for f in forms)
GRAPH_LAYERS = {"⑥","⑦","⑧","⑨"}
def upstream(f):
    """Second reader's rule (2026-09-10): a form sits upstream of the graph only if EVERY one of
    its layers is pixel or reading. One layer beyond them (anchoring, resolution, …) and it reaches
    a repairer. No damage count is cited without its layer."""
    L = set(re.findall(r"[①-⑬]", f["layer"]))
    return bool(L) and L <= {"①", "②"}
gcounts = Counter(f["damage"] for f in forms if not upstream(f))
cards = "".join(f"""<a class="card" href="#forms" data-damage="{k}" style="--c:{v[2]}"><span class="n">{counts.get(k,0)}<small> · {gcounts.get(k,0)}{E(t("reach"))}</small></span><span class="t">{E(v[0])}</span><span class="d">{E(v[1])}</span></a>""" for k,v in DAMAGE.items())
def nom(f):
    """the form's name in the page's language; the French name is missing on 44 forms, and then the English one stands in"""
    return (f.get("name_fr") or f["name"]) if LANG == "fr" else f["name"]
def last_date(f):
    """The most recent observation date; a form without observation sorts last."""
    d = sorted((x["date"] for x in f["seen"] if x.get("date")), reverse=True)
    return d[0] if d else ""


def proof_of(f):
    """example / none: does the form show at least one document where the fault sits?"""
    for pr in f.get("probes", []):
        if pr.get("matches_excerpt") and pr.get("result", {}).get("count", 0) > 0 and f["damage"] != "CORPUS_PARAMETER":
            return "docs", t("ex_yes")
    return "none", t("ex_no")
rows = "".join(f"""<tr data-damage="{f['damage']}" data-class="{f['class']}" data-layer="{E(f['layer'])}" data-reach="{'no' if upstream(f) else 'yes'}" data-era="{f.get('era',{}).get('value','')}" data-mode="{f.get('failure_mode',{}).get('value','')}" data-sev="{E(f.get('legacy_severity',''))}" data-proof="{proof_of(f)[0]}" data-src="{E(" ".join(corpora_of(f)).lower())}" data-text="{E((f['name']+' '+f.get('name_fr','')+' '+' '.join(corpora_of(f))).lower())}">
<td><a href="forms/{f['id']}.html">{E(nom(f))}</a><br><span class="fr">{E(f['name'] if LANG=='fr' else f.get('name_fr',''))}</span></td>
<td><span class="pill" style="--c:{DAMAGE[f['damage']][2]}">{E(DAMAGE[f['damage']][0])}</span></td>
<td class="date">{E(last_date(f) or '—')}</td><td>{E(CLASS_SHORT[f['class']])}</td><td>{E(f['layer'])}</td><td class="src" title="{E(" · ".join(corpora_of(f)) or "—")}">{E(" · ".join(corpora_of(f)) or "—")}</td><td class="proof p-{proof_of(f)[0]}">{E(proof_of(f)[1])}</td></tr>""" for f in forms)
TH = "".join(('<th data-sort="text" class="sorted-desc">' if i==2 else '<th data-sort="text">')+html.escape(h)+"</th>" for i,h in enumerate(t("th")))
from collections import Counter as _PC
proof_counts = _PC(proof_of(f)[0] for f in forms)
proof_counts_docs = proof_counts["docs"]; proof_counts_none = proof_counts["none"]
LEAD = ((f"{len(forms)} forms of fault observed on real corpora, most recent first — click any column to sort; "
         f"{proof_counts_docs} of them come with a reproducible example — a document you can open, the query that found it, "
         f"the frozen copy — and {proof_counts_none} do not yet. A form says what the fault does to the graph, whether code "
         f"can cancel it, whether a deletion-only repair can restore the truth, and which kind of truth can judge it.")
        if LANG == "en" else
        (f"{len(forms)} formes de fautes observées sur des corpus réels, la plus récente en tête — cliquez une colonne pour trier ; "
         f"{proof_counts_docs} portent un exemple reproductible, un document que vous pouvez ouvrir, la requête qui l'a trouvé et la copie gelée, "
         f"et {proof_counts_none} n'en ont pas encore. Une fiche dit ce que la faute fait au graphe, si du code peut l'annuler, "
         f"si une réparation par suppression seule rétablit la vérité, et quelle sorte de vérité peut la juger."))
SHELF = ("Read the count as a shelf, not as a measurement. Two readers given the same six articles on 2026-08-08, working "
         "without contact, found nine novelties and eleven, seven of them shared: 54&nbsp;% agreement, and two phenomena both "
         "had seen were filed by one as a new form and by the other as a variant of an existing one. The boundary between new "
         "and variant is not objective, so the number of forms is not a quantity. What is: the list of phenomena, each with its proof."
         if LANG == "en" else
         "Il faut lire ce nombre comme une étagère, non comme une mesure. Deux lectrices ayant reçu les six mêmes articles le "
         "8 août 2026, sans se concerter, ont trouvé neuf nouveautés et onze, dont sept communes : 54&nbsp;% d'accord, et deux "
         "phénomènes vus par les deux ont été classés par l'une comme une forme nouvelle et par l'autre comme la variante d'une "
         "forme existante. La frontière entre nouveau et variante n'est pas objective, donc le nombre de formes n'est pas une "
         "grandeur. Ce qui en est une : la liste des phénomènes, chacun avec sa preuve.")
index = f"""
<section class="hero"><p class="eyebrow">{E(t("eyebrow"))}</p>
<h1>{E(t("h1"))}</h1>
<p class="lead">{LEAD}</p>
<p class="lead small">{SHELF}</p>
<p class="cta"><a class="btn" href="#forms">{E(t("browse"))}</a> <a class="btn ghost" href="{DATA}">{E(t("query"))}</a> <a class="btn ghost" href="propose.html">{E(t("propose"))}</a></p></section>
<section class="grid" id="damages">{cards}</section>
<section id="forms"><div class="bar"><input id="q" type="search" placeholder="{E(t("search"))}" aria-label="{E(t("search"))}">
<select id="fd"><option value="">{E(t("all_damages"))}</option>{''.join(f'<option value="{k}">{E(v[0])}</option>' for k,v in DAMAGE.items())}</select>
<select id="fc"><option value="">{E(t("all_classes"))}</option>{''.join(f'<option value="{k}">{E(v)}</option>' for k,v in CLASS.items())}</select>
<select id="fs"><option value="">{E(t("any_cons"))}</option>{"".join(f'<option value="{k}">{E(v[0])}</option>' for k,v in SEVERITY.items())}<option value="__none__">{E(t("cons_none"))}</option></select>
<select id="fm"><option value="">{E(t("any_mode"))}</option>{"".join(f'<option value="{k}">{E(v)}</option>' for k,v in MODE_LABEL.items())}<option value="__none__">{E(t("mode_none"))}</option></select>
<select id="fe"><option value="">{E(t("any_era"))}</option><option value="ancient_only">{E(t("era_anc"))}</option><option value="both">{E(t("era_both"))}</option><option value="born_modern">{E(t("era_mod"))}</option><option value="not_settled">{E(t("era_ns"))}</option><option value="__none__">{E(t("era_none"))}</option></select>
<select id="fl"><option value="">{E(t("all_layers"))}</option>{''.join(f'<option value="{E(l)}">{E(l)}</option>' for l in sorted({f["layer"] for f in forms}))}</select>
<label class="chk"><input type="checkbox" id="fp"> {E(t('only_ex'))} ({proof_counts['docs']})</label>
<span id="count" class="muted"></span></div>
<div class="tablewrap"><table id="t"><thead><tr>{TH}</tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="about" class="about"><h2>{E(t("h_record"))}</h2>
<div class="cols"><div><h3>{E(t("h_seven"))}</h3><p>What a fault does to the graph: merge, split, spurious edge, missing, wrong value, wrong label, anachronism. The 113 difficulties observed in August 2026, however different they look, each produce one of these. Verified line by line.</p></div>
<div><h3>{E(t("h_counts"))}</h3><p>Each damage card shows two numbers: all forms, and forms that reach the graph. A form whose layer is pixel or reading — columns, drop caps, scanned pages — sits upstream and never reaches a repairer; every other layer does. No damage count is cited without its layer. Deletion-only repair fully addresses one damage, the spurious edge; the identity damages, merge and split, it never touches.</p></div>
<div><h3>{E(t("h_layers"))}</h3><p>Where the form bites: the pixel, the reading, the utterance, the extraction, the anchoring, the resolution, the schema, the coherence, the structure. A layout fault is a reading failure whose downstream effect on the graph is a missing fact: the damage says what happens to the graph, the layer says where it starts. Filter by layer to separate the two.</p></div>
<div><h3>{E(t("h_classes"))}</h3><p>Whether deterministic code cancels the form before it enters the graph, can abstain on it, cannot see it from inside, or whether it needs meaning. Half of what was observed is cancelled by code once; the other half is the real benchmark.</p></div>
<div><h3>{E(t("h_prov"))}</h3><p>A form enters with a verbatim excerpt from a named corpus, a date, an observer. Cases come with counter-examples. A refuted form stays, marked refuted. Nothing is deleted.</p></div>
<div><h3>{E(t("h_why"))}</h3><p>Graph repair is evaluated against constraints the graph must satisfy, not against what is true. The atlas is half of an answer key: the map of forms by damage, with the kind of truth that can judge each. The other half, the truth itself, is built on it.</p></div></div>
<p>Met a form on your corpus? <a href="propose.html">Propose it</a> with its excerpt, corpus and date — no code, no account. Or, if you prefer, open an issue or a pull request on GitHub. A second reader reviews; a contested form stays recorded as contested; nothing enters unreviewed. Cite: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). <em>Fault Atlas.</em> Loxyn SAS, Lyon. Zenodo. <a href="https://doi.org/{DOI}">doi:{DOI}</a>.</p></section>
<script>
const q=document.getElementById('q'),fd=document.getElementById('fd'),fc=document.getElementById('fc'),fl=document.getElementById('fl'),fe=document.getElementById('fe'),fp=document.getElementById('fp'),rows=[...document.querySelectorAll('#t tbody tr')],c=document.getElementById('count');
function apply(){{const s=q.value.toLowerCase(),d=fd.value,k=fc.value,l=fl.value,er=fe.value,mo=fm.value,sv=fs.value,pf=fp.checked;let n=0;for(const r of rows){{const ok=(!d||r.dataset.damage===d)&&(!k||r.dataset.class===k)&&(!l||r.dataset.layer===l)&&(!er||(er==='__none__'?!r.dataset.era:r.dataset.era===er))&&(!mo||(mo==='__none__'?!r.dataset.mode:r.dataset.mode===mo))&&(!sv||(sv==='__none__'?!r.dataset.sev:r.dataset.sev===sv))&&(!pf||r.dataset.proof==='docs')&&(!s||r.dataset.text.includes(s));r.hidden=!ok;if(ok)n++;}}c.textContent=n+' of '+rows.length;}}
const tb=document.querySelector('#t tbody'),ths=[...document.querySelectorAll('#t th')];
let sortCol=2,sortDir=-1;
function key(r,i){{const c=r.children[i];return (c.dataset.k||c.textContent).trim().toLowerCase();}}
function sortBy(i,dir){{
  const rs=[...tb.querySelectorAll('tr')];
  rs.sort((a,b)=>{{const x=key(a,i),y=key(b,i);
    if(x===y||x==='—'&&y==='—') return key(a,0).localeCompare(key(b,0));
    if(x==='—'||x==='') return 1; if(y==='—'||y==='') return -1;
    return x<y?-dir:dir;}});
  rs.forEach(r=>tb.appendChild(r));
  ths.forEach((t,j)=>{{t.classList.remove('sorted-asc','sorted-desc');if(j===i)t.classList.add(dir>0?'sorted-asc':'sorted-desc');}});
  sortCol=i;sortDir=dir;}}
ths.forEach((t,i)=>t.addEventListener('click',()=>sortBy(i,i===sortCol?-sortDir:(i===2?-1:1))));
sortBy(2,-1);
[q,fd,fc,fl,fe,fp].forEach(e=>e.addEventListener('input',apply));document.querySelectorAll('.card').forEach(a=>a.addEventListener('click',()=>{{fd.value=a.dataset.damage;apply();}}));apply();
</script>"""
CORPUS_NAMES = {json.loads(cf.read_text())["id"]: json.loads(cf.read_text())["name"] for cf in (ROOT/"corpora").glob("*.json")}
CORPUS_REC = {json.loads(cf.read_text())["id"]: json.loads(cf.read_text()) for cf in (ROOT/"corpora").glob("*.json")}
CORPUS_FILE = {json.loads(cf.read_text())["id"]: cf.name for cf in (ROOT/"corpora").glob("*.json")}
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
        if not pr or f["damage"] == "CORPUS_PARAMETER": return ""
        r = pr.get("result", {})
        if not pr.get("matches_excerpt"):
            return """<p class="noprobe">No reproducible example yet for this note.</p>"""
        head = f"{r.get('count')}/{r.get('of')} documents" if r.get("of") is not None else f"{r.get('count')} results"
        code = (ROOT/pr["file"]).read_text(encoding="utf-8") if (ROOT/pr["file"]).is_file() else ""
        carriers = []
        if r.get("carriers_file") and (ROOT/r["carriers_file"]).is_file():
            carriers = [(c["document"], c.get("evidence", [])) for c in json.loads((ROOT/r["carriers_file"]).read_text())["carriers"]]
        elif r.get("examples"):
            carriers = [(n, e) for n, e in r["examples"]]
        if not carriers:
            return ""
        def li(n, e):
            ev = (" — <span class='ev'>" + E(" | ".join(map(str, e)))[:260] + "</span>") if e else ""
            return f"<li>{doc_link(n, pr['corpus_id'])}{ev}</li>"
        docs = "<ul class='docs'>" + "".join(li(n, e) for n, e in carriers[:1]) + "</ul>"
        strata = (" · by stratum: " + ", ".join(f"{E(k)} {v}" for k, v in r["strata"].items())) if r.get("strata") else ""
        return f"""<div class="probe"><p class="probe-head"><strong>See it here</strong></p>
{docs}
<details class="code" open><summary>How it was found: the query, the corpus, the date</summary>
<p class="meta">Run: <code>{E(pr.get('run',''))}</code> · <a href="{REPO}/blob/main/{E(pr['file'])}">{E(pr['file'])}</a>{(' · written '+E(pr['written'])) if pr.get('written') else ''}{(' · '+E(r['by'])) if r.get('by') else ''}</p>
<p class="meta">Searched in: {E(CORPUS_NAMES.get(pr['corpus_id'], pr['corpus_id']).split(' — ')[0])}{(', read on '+E(CORPUS_REC[pr['corpus_id']]['harvested'])) if CORPUS_REC.get(pr['corpus_id'],{}).get('harvested') else ''} · identifiers, sha256 as read and licences: <a href="{REPO}/blob/main/corpora/{E(CORPUS_FILE[pr['corpus_id']])}">record</a>{(' · frozen copy of the files as read: <a href="'+E(CORPUS_REC[pr['corpus_id']]['frozen_copy']['url'])+'">doi:'+E(CORPUS_REC[pr['corpus_id']]['frozen_copy']['doi'])+'</a>') if CORPUS_REC.get(pr['corpus_id'],{}).get('frozen_copy',{}).get('doi') else ''}</p>
<pre><code>{E(code)}</code></pre></details></div>"""
    seen = "".join(f"""<article class="obs"><p class="meta"><strong>{E(corpus_short(s['corpus']))}</strong> · {E(s['corpus'])} · {E(s['date'])}{(' · '+E(s['observer'])) if s.get('observer') else ''}{(' · '+E(s['organisation'])) if s.get('organisation') else ''}</p>
<p>{E(s['excerpt'] if LANG=='fr' else s.get('excerpt_en', s['excerpt']))}</p>{('<details><summary>'+('English' if LANG=='fr' else 'Original note ('+E(s.get('lang','fr'))+')')+'</summary><p class="fr">'+E(s.get('excerpt_en','') if LANG=='fr' else s['excerpt'])+'</p></details>') if s.get('excerpt_en') and s.get('excerpt_en')!=s['excerpt'] else ''}{('<p class="noprobe">'+E(s['reserve'])+'</p>') if s.get('reserve') else ''}{probe_block(s.get('probe')) if s.get('probe') else ('<p class="noprobe">No reproducible example yet for this note.</p>' if s.get('corpus_id') else '')}</article>""" for s in f["seen"]) or "<p class='muted'>No observation yet: this form is a hypothesis, not an observation.</p>"
    cases = f["specimens"]["cases"]; cex = f["specimens"]["counter_examples"]
    spec = (f"<p>{len(cases)} case(s), {len(cex)} counter-example(s).</p>" if cases or cex else "<p class='muted'>Specimens not yet transcribed into this record.</p>")
    hist = "".join(f"<li><span class='meta'>{E(h['date'])}</span> {E(h['event'])}{(' — '+E(h['by'])) if h.get('by') else ''}</li>" for h in f["history"])
    prev = f["prevention"]; rep = f["repair"]
    body = f"""<p class="crumb"><a href="../index.html">Fault Atlas</a> › {E(f['id'])}</p>
<h1>{E(f['name'])}</h1><p class="fr big">{E(f.get('name_fr',''))}</p><p class="found">Found by <strong>{E(f.get("origin",{}).get("organisation","—"))}</strong>{(" — "+E(f["origin"]["campaign"])) if f.get("origin",{}).get("campaign") else ""}{(" · first seen "+E(f["seen"][0]["date"])) if f["seen"] else ""}</p><p class="found">{E(t("seen_on"))}<strong>{E(" · ".join(corpora_of(f)) or "no observation yet")}</strong></p>
<div class="badges">{('<span class="pill" style="--c:'+SEVERITY[f["legacy_severity"]][1]+'">'+E(SEVERITY[f["legacy_severity"]][0])+'</span>') if f.get("legacy_severity") in SEVERITY else ''}{('<span class="pill era">'+E({"ancient_only":"ancient documents only","both":"both eras","born_modern":"born with the modern","not_settled":"era not settled"}[f["era"]["value"]])+('  ·  worse now' if f["era"].get("aggravated_by_the_modern") else '')+'</span>') if f.get("era") else ''}<span class="pill" style="--c:{d[2]}">{E(d[0])}</span><span class="pill grey">from: {E(f.get("origin",{}).get("organisation","—"))}</span><span class="pill grey">{E(CLASS[f['class']])}</span><span class="pill grey">layer: {E(f['layer'])}</span><span class="pill grey">injection: {E(f.get('injection','—'))}</span><span class="pill warn">{E(f['status'].replace('_',' '))}</span></div>
<div class="facts"><div><h3>{E(t("h_damage"))}</h3><p><strong>{E(d[0])}</strong> — {E(d[1])}.</p></div>
<div><h3>{E(t("h_cancel"))}</h3><p>{'Yes' if prev['cancellable_by_code'] else 'No'}{('. Refusal clause: '+E(prev['refusal_clause'])) if prev.get('refusal_clause') else ''}{('. '+E(prev['note'])) if prev.get('note') else ''}.</p></div>
<div><h3>{E(t("h_restore"))}<span class="opt">classified, not measured</span></h3><p><strong>{E(REACH[rep['reachable_by_deletion']])}</strong>{(' — '+E(rep['note'])) if rep.get('note') else ''}.</p></div>
<div><h3>{E(t("h_judge"))}</h3><p>{', '.join(E(JUDGE[j]) for j in f['judgeable_by']) or '<span class="muted">none known yet</span>'}.</p></div></div>
{('<p class="muted small">Searched and not found in: '+E('; '.join(f['observed_absent_in']))+'.</p>') if f.get('observed_absent_in') else ''}
{('<div class="facts"><div><h3>'+E(t("costs_prop"))+'</h3><p><strong>'+E(SEVERITY[f["proposed_severity"]["value"]][0])+'.</strong> '+E(f["proposed_severity"]["reason"])+'</p><p class="noprobe">'+E(f["proposed_severity"]["note"])+'</p><p class="meta">First reading by '+E(f["proposed_severity"]["proposed_by"])+' on '+E(f["proposed_severity"]["date"])+'. '+E(f["proposed_severity"].get("status",""))+'</p></div></div>') if f.get("proposed_severity") else ''}
{('<div class="facts"><div><h3>'+E(t("reaches"))+'</h3><p><strong>'+E(f["registry_scope"]["extent"])+'</strong></p><p class="meta">'+E(f["registry_scope"].get("why_not_a_prevalence",""))+'</p></div></div>') if f.get("registry_scope") else ''}
{('<div class="facts"><div><h3>'+E(t("costs"))+'</h3><p><strong>'+E(SEVERITY[f["legacy_severity"]][0])+'.</strong> '+E(SEVERITY[f["legacy_severity"]][2])+'</p><p class="meta">severity '+E(f["legacy_severity"])+', judged line by line in the internal catalogue of 2026-08-09. It is independent of how often the fault occurs: a rare fault that answers wrongly in silence is worse than a common one that leaves a hole.</p></div></div>') if f.get("legacy_severity") in SEVERITY else ''}
{('<div class="facts"><div><h3>'+E(t("seen_years"))+'</h3><p><strong>'+E(" · ".join(f"{y} ({n})" for y, n in sorted(f["document_years"]["counts"].items())))+'</strong> — the publication year of the carrier files themselves, not the year of the observation.</p><p class="meta">'+E(f["document_years"]["source"])+'</p></div></div>') if f.get("document_years") else ''}
{('<div class="facts"><div><h3>'+E(t("repairs"))+'</h3><p><strong>Judged '+E(REACH[f["repair"]["reachable_by_deletion"]])+'</strong> on 2026-09-09, from the damage class, not form by form. <strong>Measured '+E({"yes":"yes","no":"no","partial":"partial","yes_at_a_cost":"yes, at a cost","depends_on_visibility":"only when a law can see it"}[f["repair"]["measured"]["value"]])+'</strong>: '+E(f["repair"]["measured"].get("note",""))+'</p>'+('<p class="noprobe"><strong>The measurement disagrees with the judgment.</strong> This form was classified '+E(f["repair"]["measured"]["disagrees_with_the_judgment"])+' and the bench says otherwise.</p>' if f["repair"]["measured"].get("disagrees_with_the_judgment") else '')+'<p class="meta">'+E(f["repair"]["measured"]["source"])+'</p></div></div>') if f.get("repair",{}).get("measured") else ''}
{('<div class="facts"><div><h3>'+E(t("fails"))+'</h3><p><strong>'+E({"PROP":"Identity, and it propagates","FAUX":"A false fact","MANQ":"A gap, not a wrong answer","MES":"A property of the corpus, not a fault of a document","DEC":"A use made downstream"}[f["failure_mode"]["value"]])+'</strong>. '+E(f["failure_mode"]["means"])+'</p><p class="meta">'+E(f["failure_mode"]["source"])+'</p></div></div>') if f.get('failure_mode') else ''}
{('<div class="facts"><div><h3>'+E(t("applies"))+'</h3><p><strong>'+E({"ancient_only":"Documents of the old era only","both":"Both eras, 1957 and 2026 alike","born_modern":"Born with the modern era","not_settled":"Era not settled"}[f["era"]["value"]])+'</strong>'+(' — and worse now than it was' if f["era"].get("aggravated_by_the_modern") else '')+('. '+E(f["era"]["note"]) if f["era"].get("note") else '')+'</p><p class="meta">'+E(f["era"]["source"])+'</p></div></div>') if f.get('era') else '<div class="facts"><div><h3>'+E(t("applies"))+'</h3><p><strong>Era not measured.</strong> This form was not among the forty-three catalogue lines confronted, old against modern, on 2026-08-08. Nothing here says it is alive today, and nothing says it is dead.</p></div></div>'}
<h2>{E(t("h_seen"))}</h2>{seen}
<h2>{E(t("h_spec"))}</h2>{spec}
<h2>{E(t("h_hist"))}</h2><ul class="hist">{hist}</ul>
<p class="muted">Record: <a href="../atlas.json">atlas.json</a> · <a href="{REPO}/blob/main/forms/{E(src_name)}">source file on GitHub</a> · <a href="{E(f['id'])}.json">this record as JSON</a> · <a href="{DATA}/forms/{E(f['id'])}">row in the data explorer</a></p>"""
    (SITE/"forms"/f"{f['id']}.html").write_text(layout(f"{f['name']} — Fault Atlas", body, depth=1, desc=f"{f['name']}: {d[0].lower()} — {d[1]}."))


# ── probes: no page. Each form shows its own documents and, folded, how they were found. ──
if (SITE/"probes.html").exists(): (SITE/"probes.html").unlink()

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

# ── corpora: no page. The records in corpora/ stay the data; each form links the documents itself. ──
import shutil as _sh
if (SITE/"corpora").exists(): _sh.rmtree(SITE/"corpora")
if (SITE/"corpora.html").exists(): (SITE/"corpora.html").unlink()

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
.lead{font-size:18px;max-width:72ch;color:var(--luxe)}.lead.small{font-size:15px;margin-top:14px;opacity:.85}.cta{margin:22px 0 0}
.btn{display:inline-block;padding:10px 18px;border-radius:8px;background:var(--acc);color:#fff;font-weight:600;margin:0 8px 8px 0;font-size:15px}.btn:hover{background:var(--acc-deep);color:#fff;text-decoration:none}.btn.ghost{background:transparent;color:var(--acc);border:1px solid var(--line-strong)}.btn.ghost:hover{background:var(--acc-soft)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:30px 0 40px}
.card{display:block;background:var(--bg-elev);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:10px;padding:16px 18px;color:var(--fg);transition:border-color .15s}.card:hover{text-decoration:none;border-color:var(--c);background:#fff}
.card .n{display:block;font-size:36px;font-weight:600;line-height:1;letter-spacing:-.03em;font-family:var(--mono)}.card .n small{display:block;font-size:12px;font-weight:500;color:var(--muted);font-family:var(--sans);letter-spacing:0;margin-top:4px}.card .t{display:block;font-weight:600;margin-top:8px}.card .d{display:block;font-size:13px;color:var(--muted);margin-top:4px;line-height:1.45}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 12px}input,select,textarea{font:inherit;font-size:15px;padding:10px 12px;border:1px solid var(--line-strong);border-radius:8px;background:#fff;color:var(--fg)}.bar input{flex:1;min-width:220px}input:focus,select:focus{outline:2px solid var(--acc-soft);border-color:var(--acc)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}table{border-collapse:collapse;width:100%;table-layout:fixed}#t th:nth-child(1),#t td:nth-child(1){width:32%}#t th:nth-child(2),#t td:nth-child(2){width:12%}#t th:nth-child(3),#t td:nth-child(3){width:9%}#t th:nth-child(4),#t td:nth-child(4){width:12%}#t th:nth-child(5),#t td:nth-child(5){width:11%}#t th:nth-child(6),#t td:nth-child(6){width:14%}#t th:nth-child(7),#t td:nth-child(7){width:10%}#t td{overflow-wrap:anywhere}th,td{text-align:left;padding:11px 14px;border-top:1px solid var(--line);vertical-align:top}th{border-top:0;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;background:var(--bg-elev)}td.num{text-align:right;font-family:var(--mono);font-size:14px}td.src{font-size:13px;color:var(--luxe)}td.date{font-family:var(--mono);font-size:12.5px;white-space:nowrap;color:var(--muted)}
#t th{cursor:pointer;user-select:none;position:relative}#t th:hover{color:var(--ink)}
#t th.sorted-asc::after{content:" ▲";font-size:9px}#t th.sorted-desc::after{content:" ▼";font-size:9px}
td.proof{font-size:13px}td.p-docs{color:#166534;font-weight:600}td.p-none{color:var(--muted)}label.chk{display:inline-flex;align-items:center;gap:6px;font-size:14px;color:var(--ink)}label.chk input{width:auto;min-width:0;flex:none}table.kv th{width:190px;text-transform:none;letter-spacing:0;font-size:14px;color:var(--ink);background:transparent;border-top:1px solid var(--line)}table.kv td code{font-size:12.5px;white-space:normal;word-break:break-all}td.mono{font-family:var(--mono);font-size:12px}
.pill{display:inline-block;white-space:nowrap;padding:2px 10px;border-radius:999px;font-size:12.5px;font-weight:600;color:#fff;background:var(--c);letter-spacing:.01em}.pill.grey{background:var(--surface);color:var(--fg);font-weight:500}.pill.era{background:#f5f3ff;color:#5b21b6;border:1px solid #ddd6fe}
.lang{font-weight:600}
.pill.warn{background:#fff3c4;color:#6b4c00;font-weight:500}
.fr{color:var(--muted);font-size:13px;font-family:var(--serif);font-style:italic}.fr.big{font-size:17px;margin-top:-10px}.muted{color:var(--muted)}
.about{margin-top:56px;border-top:1px solid var(--line);padding-top:32px}.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}.cols p{margin:0;color:var(--luxe);font-size:15px}
.crumb{color:var(--muted);font-size:14px;font-family:var(--mono)}.found{margin:-4px 0 14px;font-size:15px;color:var(--luxe)}.badges{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 22px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;background:var(--bg-elev);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin-bottom:26px}.facts p{margin:0;font-size:15px}
.note{background:#fff7ed;color:#7c2d12;border:1px solid #fed7aa;border-radius:8px;padding:10px 14px;margin-bottom:22px;font-size:15px}
.obs{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:10px 0}.obs p{margin:0}.meta{color:var(--muted);font-size:13px;margin:0 0 8px;font-family:var(--mono)}details{margin-top:8px}details summary{cursor:pointer;color:var(--muted);font-size:14px}details .fr{display:block;margin-top:8px;font-size:14px}
.probe{margin-top:12px;border-top:1px dashed var(--line);padding-top:10px}.probe .probe-head{margin:0 0 6px;font-size:14px}.probe h4{margin:10px 0 4px;font-size:14px}.probe ul.docs{margin:0 0 6px 0;padding:0;list-style:none;font-size:14px;line-height:1.5}.probe ul.docs li{margin:2px 0}.probe .ev{color:var(--muted)}.probe a.xml{font-family:var(--mono);font-size:11px;color:var(--muted);margin-left:2px}.probe details.code{margin-top:8px}.probe details.code summary{color:var(--muted);font-size:13.5px}.probe pre{margin:10px 0 0;padding:12px 14px;background:var(--bg-elev);border:1px solid var(--line);border-radius:8px;overflow-x:auto;font-size:12.5px;line-height:1.45;max-height:520px}.probe .note{margin:8px 0}.noprobe{margin-top:10px!important;border-top:1px dashed var(--line);padding-top:8px;font-size:13.5px;color:var(--muted)}
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
