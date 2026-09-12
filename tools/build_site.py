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
 "switch": {"en": "\U0001F1EB\U0001F1F7", "fr": "\U0001F1EC\U0001F1E7"},
      "from": {"en": "from:", "fr": "de :"},
 "frozen_copy": {"en": "frozen copy of the files as read:", "fr": "copie gelée des fichiers tels que lus :"},
 "explorer_row": {"en": "row in the data explorer", "fr": "sa ligne dans l'explorateur de données"},
 "yes": {"en": "Yes", "fr": "Oui"},
 "no": {"en": "No", "fr": "Non"},
 "refusal": {"en": "Refusal clause:", "fr": "Clause de refus :"},
 "see_here": {"en": "See it here", "fr": "Voyez-la ici"},
 "how_found": {"en": "How it was found: the query, the corpus, the date", "fr": "Comment elle a été trouvée : la requête, le corpus, la date"},
 "run": {"en": "Run:", "fr": "Lancer :"},
 "written": {"en": "written", "fr": "écrite le"},
 "searched_in": {"en": "Searched in:", "fr": "Cherchée dans :"},
 "read_on": {"en": "read on", "fr": "lu le"},
 "by_stratum": {"en": "by stratum:", "fr": "par strate :"},
 "years_tail": {"en": "— the publication year of the carrier files themselves, not the year of the observation.",
                "fr": "— l'année de publication des fichiers porteurs eux-mêmes, pas l'année de l'observation."},
 "found_by": {"en": "Found by", "fr": "Trouvée par"},
 "first_seen": {"en": "first seen", "fr": "vue pour la première fois le"},
 "no_obs_short": {"en": "no observation yet", "fr": "aucune observation pour l'instant"},
 "no_obs": {"en": "No observation yet: this form is a hypothesis, not an observation.",
            "fr": "Aucune observation pour l'instant : cette forme est une hypothèse, pas une observation."},
 "no_example_note": {"en": "No reproducible example yet for this note.",
                     "fr": "Pas encore d'exemple reproductible pour cette note."},
 "sev_meta": {"en": "severity §, judged line by line in the internal catalogue of 2026-08-09. It is independent of how often the fault occurs: a rare fault that answers wrongly in silence is worse than a common one that leaves a hole.",
              "fr": "gravité §, jugée ligne par ligne dans le catalogue interne du 9 août 2026. Elle est indépendante de la fréquence : une faute rare qui répond faux en silence est pire qu'une faute courante qui laisse un trou."},
 "judged": {"en": "Judged", "fr": "Jugé"},
 "judged_how": {"en": "on 2026-09-09, from the damage class, not form by form.", "fr": "le 9 septembre 2026, depuis la classe de dégât, pas forme par forme."},
 "measured": {"en": "Measured", "fr": "Mesuré"},
 "disagree": {"en": "The measurement disagrees with the judgment.", "fr": "La mesure contredit le jugement."},
 "disagree_2": {"en": "This form was classified", "fr": "Cette forme était classée"},
 "classified": {"en": "classified, not measured", "fr": "classé, non mesuré"},
 "switch_title": {"en": "Lire en français", "fr": "Read in English"},
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
 "h_rel": {"en": "Related forms", "fr": "Formes liées"},
 "rel_out": {"en": "This form points to", "fr": "Cette fiche renvoie vers"},
 "rel_in": {"en": "Pointed to by", "fr": "Fiches qui renvoient vers elle"},
 "rel_why": {"en": "A link says the two forms were compared when this one entered; it does not say one replaces the other. The decision, when there is one, is in the history below.",
             "fr": "Un lien dit que les deux formes ont été comparées à l'entrée de celle-ci ; il ne dit pas que l'une remplace l'autre. La décision, quand il y en a une, est dans l'histoire ci-dessous."},
 "rel_oos": {"en": "not published: the August catalogue ruled this line an instrument or metric property, not a fault",
             "fr": "non publiée : le catalogue d'août a jugé cette ligne propriété d'instrument ou de métrique, pas une forme de faute"},
 "nav_forms": {"en": "Forms", "fr": "Formes"},
 "nav_about": {"en": "About", "fr": "À propos"},
 "nav_data": {"en": "Data &amp; API", "fr": "Données et API"},
 "foot_note": {"en": "The JSON file is the record of truth; this site is a view rebuilt at each release. %d forms of %d are validated by a second reader; the rest carries its status on its own page.",
               "fr": "Le fichier JSON fait foi ; ce site en est une vue, reconstruite à chaque version. %d formes sur %d sont validées par une seconde lectrice, les autres portent leur statut sur leur fiche."},
}

def t(k):
    return T[k][LANG]

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT/"site" if LANG == "en" else ROOT/"site"/"fr"; (SITE/"forms").mkdir(parents=True, exist_ok=True)
import shutil; FAV = ROOT/"tools"/"favicon.svg"
if FAV.exists(): shutil.copy(FAV, SITE/"favicon.svg")
# A JSON-LD context that is not served at the URL it declares is a broken promise: a reader that
# resolves it gets a 404 and the document stops being self-describing. Both languages carry it.
_NS = ROOT/"ns"
if _NS.is_dir():
    (SITE/"ns").mkdir(parents=True, exist_ok=True)
    for _f in _NS.glob("*"):
        if _f.is_file(): shutil.copy(_f, SITE/"ns"/_f.name)
_SCHEMA = ROOT/"schema"
if _SCHEMA.is_dir():
    (SITE/"schema").mkdir(parents=True, exist_ok=True)
    for _f in _SCHEMA.glob("*.json"):
        shutil.copy(_f, SITE/"schema"/_f.name)
DOI = "10.5281/zenodo.22674547"; REPO = "https://github.com/Loxyn-Korela/fault-atlas"; DATA = "/data/fault-atlas"
VERSION = re.search(r"^version: (.+)$", (ROOT/"CITATION.cff").read_text(), re.M).group(1)

# Catalogue lines examined in August and ruled out of scope. A `related` pointing at one of them is
# not a dead link: the number exists, the form does not, and the record says why.
OUT_OF_SCOPE = {"form-%03d" % x["legacy_line"]: x for x in json.loads((ROOT/"docs"/"out-of-scope-2026-08.json").read_text())}
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

forms = [json.loads(f.read_text()) for f in sorted((ROOT/"forms").glob("*.json"))]
VALIDATED = sum(1 for f in forms if f["status"] == "validated")
NAME_OF = {f["id"]: (f.get("name_fr") or f["name"]) if LANG == "fr" else f["name"] for f in forms}
BACKLINKS = defaultdict(list)
for _f in forms:
    for _r in _f.get("related") or []:
        BACKLINKS[_r].append(_f["id"])

def related_block(f):
    """The `related` field, both ways. 37 forms carry it and the site showed none of it."""
    out, back = f.get("related") or [], sorted(BACKLINKS.get(f["id"], []))
    if not out and not back:
        return ""
    def li(fid):
        if fid in NAME_OF:
            return f'<li><a href="{E(fid)}.html">{E(fid)}</a> — {E(NAME_OF[fid])}</li>'
        if fid in OUT_OF_SCOPE:
            o = OUT_OF_SCOPE[fid]
            return (f'<li><span class="muted">{E(fid)}</span> — {E(o["name_fr"])} '
                    f'<span class="muted">({E(t("rel_oos"))}, '
                    f'<a href="{REPO}/blob/main/docs/out-of-scope-2026-08.json">record</a>)</span></li>')
        return f'<li><span class="muted">{E(fid)} — unknown</span></li>'
    parts = []
    if out:  parts.append(f'<p class="meta">{E(t("rel_out"))}</p><ul class="docs">' + "".join(li(x) for x in out) + "</ul>")
    if back: parts.append(f'<p class="meta">{E(t("rel_in"))}</p><ul class="docs">' + "".join(li(x) for x in back) + "</ul>")
    return f'<h2>{E(t("h_rel"))}</h2>' + "".join(parts) + f'<p class="meta">{E(t("rel_why"))}</p>'

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
<nav><a href="{p}index.html#forms">{E(t("nav_forms"))}</a><a href="{p}index.html#about">{E(t("nav_about"))}</a><a href="{DATA}">{E(t("nav_data"))}</a><a href="{REPO}">GitHub</a><a href="https://doi.org/{DOI}">DOI</a><a class="lang" href="{SWITCH[depth]}" title="{E(t("switch_title"))}" aria-label="{E(t("switch_title"))}"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/></svg>{"FR" if LANG == "en" else "EN"}</a></nav></header>
<main>{body}</main>
<footer><p><strong>Fault Atlas</strong> v{E(VERSION)} · built {BUILT} · Loxyn SAS, Lyon · Gracia S., Bagnol-Lebon C., Comtet Y. · records CC BY-SA 4.0, tools Apache 2.0 · <a href="https://doi.org/{DOI}">doi:{DOI}</a> · <a href="{REPO}">source</a> · <a href="mailto:contact@loxyn.ai">contact@loxyn.ai</a></p>
<p class="muted">{E(t("foot_note") % (VALIDATED, len(forms)))}</p></footer>
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
cards = "".join(f"""<a class="card" href="#forms" data-damage="{k}" style="--c:{v[2]}"><span class="n">{counts.get(k,0)}<small> · {gcounts.get(k,0)}{E(t("reach"))}</small></span><span class="t">{E(v[0])}</span><span class="d">{E(v[1])}</span></a>""" for k,v in DAMAGE.items() if k != "CORPUS_PARAMETER")
_cp = DAMAGE["CORPUS_PARAMETER"]
aside = f"""<p class="aside"><a href="#forms" data-damage="CORPUS_PARAMETER">{counts.get("CORPUS_PARAMETER",0)} {E(_cp[0])}</a> — {E(_cp[1])}</p>"""
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
rows = "".join(f"""<tr data-damage="{f['damage']}" data-class="{f['class']}" data-layer="{E(f['layer'])}" data-reach="{'no' if upstream(f) else 'yes'}" data-mode="{f.get('failure_mode',{}).get('value','')}" data-sev="{E(f.get('legacy_severity',''))}" data-proof="{proof_of(f)[0]}" data-src="{E(" ".join(corpora_of(f)).lower())}" data-text="{E((f['name']+' '+f.get('name_fr','')+' '+' '.join(corpora_of(f))).lower())}">
<td><a href="forms/{f['id']}.html">{E(nom(f))}</a><br><span class="fr">{E(f['name'] if LANG=='fr' else f.get('name_fr',''))}</span></td>
<td><span class="pill" style="--c:{DAMAGE[f['damage']][2]}">{E(DAMAGE[f['damage']][0])}</span></td>
<td class="date">{E(last_date(f) or '—')}</td><td>{E(CLASS_SHORT[f['class']])}</td><td>{E(f['layer'])}</td><td class="src" title="{E(" · ".join(corpora_of(f)) or "—")}">{E(" · ".join(corpora_of(f)) or "—")}</td><td class="proof p-{proof_of(f)[0]}">{E(proof_of(f)[1])}</td></tr>""" for f in forms)

MODE_MEANS = {"en": {
  "PROP": "identity: one thing appears under several forms, or several things under one — the error lands on a node and propagates to everything hanging from it",
  "FAUX": "a false fact: a value, a type or a link the source never asserted",
  "MANQ": "a gap: the graph is incomplete where the reading did not reach, not wrong",
  "MES":  "a property of the corpus or of the measuring apparatus, not a fault of a document",
  "DEC":  "a use made downstream of the graph, not a fault in building it"},
 "fr": {
  "PROP": "l'identité : une chose sous plusieurs formes, ou plusieurs choses sous une seule — l'erreur se pose sur un nœud et se propage à tout ce qui y pend",
  "FAUX": "un fait faux : une valeur, un type ou un lien que la source n'a jamais affirmé",
  "MANQ": "un trou : le graphe est incomplet là où la lecture n'est pas allée, pas menteur",
  "MES":  "une propriété du corpus ou de l'appareil de mesure, pas une faute d'un document",
  "DEC":  "un usage fait en aval du graphe, pas une faute de sa construction"}}
MODE_SRC = {"en": "the internal catalogue of 2026-08-09: judged line by line, and it varies inside a damage class",
            "fr": "le catalogue interne du 9 août 2026 : jugé ligne par ligne, et il varie à l'intérieur d'un même dégât"}
MEASURED_V = {"en": {"yes":"yes","no":"no","partial":"partial","yes_at_a_cost":"yes, at a cost","depends_on_visibility":"only when a law can see it"},
              "fr": {"yes":"oui","no":"non","partial":"partiel","yes_at_a_cost":"oui, à un prix","depends_on_visibility":"seulement quand une loi la voit"}}
MEASURED_NOTE = {"en": {
  "ANACHRONISM":"0 of 5,276 reached, on three identical runs","WRONG_VALUE":"0 of 2,613 reached",
  "MERGE":"0 of 2,532 reached","MISSING":"0 of 423 reached",
  "SPLIT":"0 of 1,355 restored; 24 twins deleted and the 1,674 true facts they took were not restored",
  "WRONG_LABEL":"3,932 of 3,932 reached, and 12,591 true facts were lost with them: the repair deletes the nodes, not their labels",
  "SPURIOUS_EDGE":"360 of 360 when a law can see it, 6 of 361 when none can"},
 "fr": {
  "ANACHRONISM":"0 atteint sur 5 276, sur trois exécutions identiques","WRONG_VALUE":"0 atteint sur 2 613",
  "MERGE":"0 atteint sur 2 532","MISSING":"0 atteint sur 423",
  "SPLIT":"0 rétabli sur 1 355 : 24 jumeaux supprimés, et les 1 674 faits vrais qu'ils avaient emportés ne reviennent pas",
  "WRONG_LABEL":"3 932 atteints sur 3 932, et 12 591 faits vrais sont partis avec : la réparation supprime les nœuds, pas leurs étiquettes",
  "SPURIOUS_EDGE":"360 sur 360 quand une loi la voit, 6 sur 361 quand aucune ne la voit"}}
MEASURED_SRC = {"en": "measured 2026-09-10 by pgrepair on the frozen EUR-Lex truth, three identical runs. Per damage class, not per form.",
                "fr": "mesuré le 10 septembre 2026 par pgrepair sur la vérité EUR-Lex gelée, trois exécutions identiques. Par classe de dégât, pas par forme."}
YEARS_SRC = {"en": "the publication year of the carrier files themselves, read from each file",
             "fr": "l'année de publication des fichiers porteurs eux-mêmes, lue dans chaque fichier"}
PROP_STATUS = {"en": "First reading, proposed. A second reader confirms or contests, as for the 43 validated forms.",
               "fr": "Première lecture, proposée. Une seconde lectrice confirme ou conteste, comme pour les 43 formes validées."}

SCOPE_WHY = {"en": "a fault of a registry has no prevalence: it is a property of the base, so everything drawn from that base carries it. What can be stated is the slice it touches.",
             "fr": "une faute de registre n'a pas de prévalence : elle est une propriété de la base, donc tout ce qu'on en tire la porte. Ce qui peut se dire, c'est la tranche qu'elle touche."}
REPAIR_NOTE = {"en": {"no":"deletion cannot restore this","yes":"the faulty edge can be deleted","partial":"an extra label can be deleted, a missing one cannot be added"},
               "fr": {"no":"une suppression ne peut pas rétablir ceci","yes":"l'arête fautive peut être supprimée","partial":"une étiquette en trop peut être supprimée, une manquante ne peut pas être ajoutée"}}
REPAIR_SRC = {"en": "derived from the damage class by the migration of 2026-09-09, not judged form by form and not measured",
              "fr": "dérivé de la classe de dégât par la migration du 9 septembre 2026, ni jugé forme par forme ni mesuré"}
def prop_note(f):
    v = f["proposed_severity"]
    if v.get("adds_to_the_damage_class"):
        return ("the August catalogue judges most %s forms otherwise; this reading says %s and the reason is above" % (f["damage"], v["value"])
                if LANG == "en" else
                "le catalogue d'août juge la plupart des formes %s autrement ; cette lecture dit %s, et la raison est ci-dessus" % (f["damage"], v["value"]))
    return ("this reading agrees with how the August catalogue judges most %s forms, so it adds little" % f["damage"]
            if LANG == "en" else
            "cette lecture rejoint la façon dont le catalogue d'août juge la plupart des formes %s : elle n'ajoute donc pas grand-chose" % f["damage"])
TH = "".join(('<th data-sort="text" class="sorted-desc">' if i==2 else '<th data-sort="text">')+html.escape(h)+"</th>" for i,h in enumerate(t("th")))
from collections import Counter as _PC
proof_counts = _PC(proof_of(f)[0] for f in forms)
ABOUT_EN = f"""<section id="about" class="about"><h2>What a record says</h2>
<div class="cols"><div><h3>Seven damages</h3><p>What a fault does to the graph: merge, split, spurious edge, missing, wrong value, wrong label, anachronism. The 113 difficulties observed in August 2026, however different they look, each produce one of these. Verified line by line.</p></div>
<div><h3>Two counts, always together</h3><p>Each damage card shows two numbers: all forms, and forms that reach the graph. A form whose layer is pixel or reading — columns, drop caps, scanned pages — sits upstream and never reaches a repairer; every other layer does. No damage count is cited without its layer.</p></div>
<div><h3>Layers</h3><p>Where the form bites: the pixel, the reading, the utterance, the extraction, the anchoring, the resolution, the schema, the coherence, the structure. A layout fault is a reading failure whose downstream effect on the graph is a missing fact: the damage says what happens to the graph, the layer says where it starts.</p></div>
<div><h3>Four classes</h3><p>Whether deterministic code cancels the form before it enters the graph, can abstain on it, cannot see it from inside, or whether it needs meaning. Half of what was observed is cancelled by code once; the other half is the real benchmark.</p></div>
<div><h3>Provenance, not opinion</h3><p>A form enters with a verbatim excerpt from a named corpus, a date, an observer. Cases come with counter-examples. A refuted form stays, marked refuted. Nothing is deleted.</p></div>
<div><h3>Why it matters</h3><p>Graph repair is evaluated against constraints the graph must satisfy, not against what is true. The atlas is half of an answer key: the map of forms by damage, with the kind of truth that can judge each. The other half, the truth itself, is built on it.</p></div></div>
"""
ABOUT_FR = f"""<section id="about" class="about"><h2>Ce que dit une fiche</h2>
<div class="cols"><div><h3>Sept dégâts</h3><p>Ce qu'une faute fait au graphe : fusion, scission, arête fausse, manque, mauvaise valeur, mauvaise étiquette, anachronisme. Les 113 difficultés observées en août 2026, si différentes soient-elles, produisent chacune l'un de ces sept. Vérifié ligne par ligne.</p></div>
<div><h3>Deux comptes, toujours ensemble</h3><p>Chaque carte de dégât porte deux nombres : toutes les formes, et celles qui atteignent le graphe. Une forme dont la couche est le pixel ou la lecture — colonnes, lettrines, pages scannées — se tient en amont et n'arrive jamais jusqu'à un réparateur ; toutes les autres couches y arrivent. Aucun compte de dégât n'est cité sans sa couche.</p></div>
<div><h3>Couches</h3><p>Là où la forme mord : le pixel, la lecture, l'énoncé, l'extraction, l'ancrage, la résolution, le schéma, la cohérence, la structure. Une faute de mise en page est un échec de lecture dont l'effet en aval est un fait manquant : le dégât dit ce qui arrive au graphe, la couche dit où ça commence.</p></div>
<div><h3>Quatre classes</h3><p>Si du code déterministe annule la forme avant qu'elle n'entre dans le graphe, s'il peut s'abstenir, s'il ne peut pas la voir de l'intérieur, ou s'il faut du sens. La moitié de ce qui a été observé s'annule une fois par du code ; l'autre moitié est le vrai banc d'essai.</p></div>
<div><h3>Provenance, pas opinion</h3><p>Une forme entre avec un extrait verbatim d'un corpus nommé, une date, un observateur. Les cas viennent avec des contre-exemples. Une forme réfutée reste, marquée réfutée. Rien n'est supprimé.</p></div>
<div><h3>Pourquoi ça compte</h3><p>La réparation de graphes est évaluée contre des contraintes que le graphe doit satisfaire, pas contre ce qui est vrai. L'atlas est la moitié d'un corrigé : la carte des formes par dégât, avec la sorte de vérité qui peut juger chacune. L'autre moitié, la vérité elle-même, se construit dessus.</p></div></div>
"""
ABOUT = ABOUT_EN if LANG == "en" else ABOUT_FR
CEILING = {'en': '<section id="ceiling" class="ceiling"><h2>Why the atlas has to name the form, not just the damage</h2>\n<p class="lead">A repair that only deletes is bounded by what the graph itself can tell apart. Measured on a frozen EUR-Lex truth of 489,223 facts, three identical runs of one repairer, deletion only:</p>\n<div class="tablewrap"><table class="reach"><thead><tr><th>damage injected</th><th>injected</th><th>reached</th><th></th></tr></thead><tbody>\n<tr class="yes"><td>spurious edge <em>a law separates</em></td><td>360</td><td>360</td><td>reached</td></tr>\n<tr class="yes"><td>wrong label</td><td>3,932</td><td>3,932</td><td>reached, and it destroyed 12,591 true facts</td></tr>\n<tr><td>spurious edge no law separates</td><td>361</td><td>6</td><td>not reached</td></tr>\n<tr><td>anachronism</td><td>5,276</td><td>0</td><td>not reached</td></tr>\n<tr><td>wrong value</td><td>2,613</td><td>0</td><td>not reached</td></tr>\n<tr><td>merge</td><td>2,532</td><td>0</td><td>not reached</td></tr>\n<tr><td>split</td><td>1,355</td><td>0</td><td>not reached</td></tr>\n<tr><td>missing</td><td>423</td><td>0</td><td>not reached</td></tr>\n</tbody></table></div>\n<p>The two classes reached are exactly the two where the graph carries what separates the true from the false: a law for the edge, the identifier inside the node for the label. The six it does not reach are exactly the six where it does not. This is not a defect of one repairer. To mend a gap you must know what to add; to mend a wrong value, the right one; to undo a merge, which fact belongs to whom. None of that is in the graph, so no deletion-only repair reaches it and no better constraint language would.</p>\n<p class="meta">Measured 2026-09-10 with pgrepair (Spinrath &amp; Bonifati, PVLDB 19), SciPyWeightedILP, three runs, identical on all three. Injection sealed by seed; the record, the journal and the command are in <a href="https://github.com/Loxyn-Korela/corrige">Le Corrigé</a>. A damage class, not a form: two forms of the same damage and the same visibility get the same answer.</p></section>', 'fr': '<section id="ceiling" class="ceiling"><h2>Pourquoi l\'atlas doit nommer la forme, et pas seulement le dégât</h2>\n<p class="lead">Une réparation qui ne sait que supprimer est bornée par ce que le graphe lui-même sait distinguer. Mesuré sur une vérité EUR-Lex gelée de 489 223 faits, trois passes identiques d\'un réparateur, suppression seule :</p>\n<div class="tablewrap"><table class="reach"><thead><tr><th>dégât injecté</th><th>injectés</th><th>atteints</th><th></th></tr></thead><tbody>\n<tr class="yes"><td>arête fausse <em>qu\'une loi sépare</em></td><td>360</td><td>360</td><td>atteinte</td></tr>\n<tr class="yes"><td>mauvaise étiquette</td><td>3 932</td><td>3 932</td><td>atteinte, et 12 591 faits vrais détruits</td></tr>\n<tr><td>arête fausse qu\'aucune loi ne sépare</td><td>361</td><td>6</td><td>non atteinte</td></tr>\n<tr><td>anachronisme</td><td>5 276</td><td>0</td><td>non atteint</td></tr>\n<tr><td>mauvaise valeur</td><td>2 613</td><td>0</td><td>non atteinte</td></tr>\n<tr><td>fusion</td><td>2 532</td><td>0</td><td>non atteinte</td></tr>\n<tr><td>scission</td><td>1 355</td><td>0</td><td>non atteinte</td></tr>\n<tr><td>manque</td><td>423</td><td>0</td><td>non atteint</td></tr>\n</tbody></table></div>\n<p>Les deux classes atteintes sont exactement les deux où le graphe porte lui-même de quoi séparer le vrai du faux : une loi pour l\'arête, l\'identifiant contenu dans le nœud pour l\'étiquette. Les six autres sont exactement celles où il ne le porte pas. Ce n\'est pas le défaut d\'un réparateur. Pour réparer un manque il faut savoir quoi ajouter ; pour une valeur fausse, la bonne ; pour défaire une fusion, quel fait appartient à qui. Rien de tout cela n\'est dans le graphe : aucune réparation par suppression ne l\'atteint, et aucun meilleur langage de contraintes n\'y changerait rien.</p>\n<p class="meta">Mesuré le 10-09-2026 avec pgrepair (Spinrath et Bonifati, PVLDB 19), SciPyWeightedILP, trois passes, identiques aux trois. Injection scellée par graine ; la vérité, le journal et la commande sont dans <a href="https://github.com/Loxyn-Korela/corrige">Le Corrigé</a>. Par classe de dégât et non par forme : deux formes du même dégât et de même visibilité reçoivent la même réponse.</p></section>'}[LANG]
proof_counts_docs = proof_counts["docs"]; proof_counts_none = proof_counts["none"]
TH = "".join(('<th data-sort="text" class="sorted-desc">' if i==2 else '<th data-sort="text">')+html.escape(h)+"</th>" for i,h in enumerate(t("th")))
from collections import Counter as _PC
proof_counts = _PC(proof_of(f)[0] for f in forms)
proof_counts_docs = proof_counts["docs"]; proof_counts_none = proof_counts["none"]
index = f"""
<section class="hero"><p class="eyebrow">{E(t("eyebrow"))}</p>
<h1>{E(t("h1"))}</h1>
<p class="cta"><a class="btn" href="#forms">{E(t("browse"))}</a> <a class="btn ghost" href="{DATA}">{E(t("query"))}</a> <a class="btn ghost" href="propose.html">{E(t("propose"))}</a></p></section>
<section class="grid" id="damages">{cards}</section>
{aside}
<section id="forms"><div class="bar"><input id="q" type="search" placeholder="{E(t("search"))}" aria-label="{E(t("search"))}">
<select id="fd"><option value="">{E(t("all_damages"))}</option>{''.join(f'<option value="{k}">{E(v[0])}</option>' for k,v in DAMAGE.items())}</select>
<select id="fc"><option value="">{E(t("all_classes"))}</option>{''.join(f'<option value="{k}">{E(v)}</option>' for k,v in CLASS.items())}</select>
<select id="fs"><option value="">{E(t("any_cons"))}</option>{"".join(f'<option value="{k}">{E(v[0])}</option>' for k,v in SEVERITY.items())}<option value="__none__">{E(t("cons_none"))}</option></select>
<select id="fm"><option value="">{E(t("any_mode"))}</option>{"".join(f'<option value="{k}">{E(v)}</option>' for k,v in MODE_LABEL.items())}<option value="__none__">{E(t("mode_none"))}</option></select>
<select id="fl"><option value="">{E(t("all_layers"))}</option>{''.join(f'<option value="{E(l)}">{E(l)}</option>' for l in sorted({f["layer"] for f in forms}))}</select>
<label class="chk"><input type="checkbox" id="fp"> {E(t('only_ex'))} ({proof_counts['docs']})</label>
<span id="count" class="muted"></span></div>
<div class="tablewrap"><table id="t"><thead><tr>{TH}</tr></thead><tbody>{rows}</tbody></table></div></section>
{ABOUT}
{CEILING}
<p>Met a form on your corpus? <a href="propose.html">Propose it</a> with its excerpt, corpus and date — no code, no account. Or, if you prefer, open an issue or a pull request on GitHub. A second reader reviews; a contested form stays recorded as contested; nothing enters unreviewed. Cite: Gracia S., Bagnol-Lebon C., Comtet Y. (2026). <em>Fault Atlas.</em> Loxyn SAS, Lyon. Zenodo. <a href="https://doi.org/{DOI}">doi:{DOI}</a>.</p></section>
<script>
const q=document.getElementById('q'),fd=document.getElementById('fd'),fc=document.getElementById('fc'),fl=document.getElementById('fl'),fs=document.getElementById('fs'),fm=document.getElementById('fm'),fp=document.getElementById('fp'),rows=[...document.querySelectorAll('#t tbody tr')],c=document.getElementById('count');
function apply(){{const s=q.value.toLowerCase(),d=fd.value,k=fc.value,l=fl.value,mo=fm.value,sv=fs.value,pf=fp.checked;let n=0;for(const r of rows){{const ok=(!d||r.dataset.damage===d)&&(!k||r.dataset.class===k)&&(!l||r.dataset.layer===l)&&(!mo||(mo==='__none__'?!r.dataset.mode:r.dataset.mode===mo))&&(!sv||(sv==='__none__'?!r.dataset.sev:r.dataset.sev===sv))&&(!pf||r.dataset.proof==='docs')&&(!s||r.dataset.text.includes(s));r.hidden=!ok;if(ok)n++;}}c.textContent=n+' of '+rows.length;}}
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
[q,fd,fc,fs,fm,fl,fp].forEach(e=>e.addEventListener('input',apply));document.querySelectorAll('.card').forEach(a=>a.addEventListener('click',()=>{{fd.value=a.dataset.damage;apply();}}));apply();
</script>"""
CORPUS_NAMES = {json.loads(cf.read_text())["id"]: json.loads(cf.read_text())["name"] for cf in (ROOT/"corpora").glob("*.json")}
CORPUS_REC = {json.loads(cf.read_text())["id"]: json.loads(cf.read_text()) for cf in (ROOT/"corpora").glob("*.json")}
CORPUS_FILE = {json.loads(cf.read_text())["id"]: cf.name for cf in (ROOT/"corpora").glob("*.json")}
(SITE/"index.html").write_text(layout("Fault Atlas", index))

# The index filters were dead for every visitor because the listener array named `fe`, an element
# that does not exist: one ReferenceError, and no listener was ever attached. Nothing caught it,
# so the build now checks its own script against its own markup before writing anything else.
def check_index_script(page):
    ids = set(re.findall(r'id="([A-Za-z0-9_-]+)"', page))
    for blk in re.findall(r"<script>(.*?)</script>", page, re.S):
        if "apply" not in blk: continue
        for name in re.findall(r"getElementById\('([^']+)'\)", blk):
            if name not in ids:
                raise SystemExit(f"build: the index script reads #{name}, which the page does not contain")
        declared = set(re.findall(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=", blk))
        declared |= set(re.findall(r",\s*([A-Za-z_$][\w$]*)\s*=", blk))
        declared |= {"document", "window", "location", "URL", "Math"}
        for arr in re.findall(r"\[([a-zA-Z0-9_,$\s]+)\]\s*\.forEach\s*\(\s*[a-z]\s*=>\s*\1?[a-z]*\.addEventListener", blk) or \
                   re.findall(r"\[([a-zA-Z0-9_,$\s]+)\]\.forEach\(e=>e\.addEventListener", blk):
            for name in (x.strip() for x in arr.split(",")):
                if name and name not in declared:
                    raise SystemExit(f"build: the index script binds a listener on `{name}`, which is never declared")
check_index_script((SITE/"index.html").read_text())

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
        strata = ((" · "+t("by_stratum")+" ") + ", ".join(f"{E(k)} {v}" for k, v in r["strata"].items())) if r.get("strata") else ""
        return f"""<div class="probe"><p class="probe-head"><strong>{E(t("see_here"))}</strong></p>
{docs}
<details class="code" open><summary>{E(t("how_found"))}</summary>
<p class="meta">{E(t("run"))} <code>{E(pr.get('run',''))}</code> · <a href="{REPO}/blob/main/{E(pr['file'])}">{E(pr['file'])}</a>{(' · '+E(t('written'))+' '+E(pr['written'])) if pr.get('written') else ''}{(' · '+E(r['by'])) if r.get('by') else ''}</p>
<p class="meta">{E(t("searched_in"))} {E(CORPUS_NAMES.get(pr['corpus_id'], pr['corpus_id']).split(' — ')[0])}{(', '+E(t('read_on'))+' '+E(CORPUS_REC[pr['corpus_id']]['harvested'])) if CORPUS_REC.get(pr['corpus_id'],{}).get('harvested') else ''} · identifiers, sha256 as read and licences: <a href="{REPO}/blob/main/corpora/{E(CORPUS_FILE[pr['corpus_id']])}">record</a>{(' · '+E(t('frozen_copy'))+' <a href="'+E(CORPUS_REC[pr['corpus_id']]['frozen_copy']['url'])+'">doi:'+E(CORPUS_REC[pr['corpus_id']]['frozen_copy']['doi'])+'</a>') if CORPUS_REC.get(pr['corpus_id'],{}).get('frozen_copy',{}).get('doi') else ''}</p>
<pre><code>{E(code)}</code></pre></details></div>"""
    seen = "".join(f"""<article class="obs"><p class="meta"><strong>{E(corpus_short(s['corpus']))}</strong> · {E(s['corpus'])} · {E(s['date'])}{(' · '+E(s['observer'])) if s.get('observer') else ''}{(' · '+E(s['organisation'])) if s.get('organisation') else ''}</p>
<p>{E(s['excerpt'] if LANG=='fr' else s.get('excerpt_en', s['excerpt']))}</p>{('<details><summary>'+('English' if LANG=='fr' else 'Original note ('+E(s.get('lang','fr'))+')')+'</summary><p class="fr">'+E(s.get('excerpt_en','') if LANG=='fr' else s['excerpt'])+'</p></details>') if s.get('excerpt_en') and s.get('excerpt_en')!=s['excerpt'] else ''}{('<p class="noprobe">'+E(s['reserve'])+'</p>') if s.get('reserve') else ''}{probe_block(s.get('probe')) if s.get('probe') else ('<p class="noprobe">'+E(t('no_example_note'))+'</p>' if s.get('corpus_id') else '')}</article>""" for s in f["seen"]) or "<p class='muted'>"+html.escape(t('no_obs'))+"</p>"
    cases = f["specimens"]["cases"]; cex = f["specimens"]["counter_examples"]
    spec = (f"<p>{len(cases)} case(s), {len(cex)} counter-example(s).</p>" if cases or cex else "<p class='muted'>Specimens not yet transcribed into this record.</p>")
    hist = "".join(f"<li><span class='meta'>{E(h['date'])}</span> {E(h['event'])}{(' — '+E(h['by'])) if h.get('by') else ''}</li>" for h in f["history"])
    prev = f["prevention"]; rep = f["repair"]
    body = f"""<p class="crumb"><a href="../index.html">Fault Atlas</a> › {E(f['id'])}</p>
<h1>{E(nom(f))}</h1><p class="fr big">{E(f['name'] if LANG=='fr' else f.get('name_fr',''))}</p><p class="found">{E(t("found_by"))} <strong>{E(f.get("origin",{}).get("organisation","—"))}</strong>{(" — "+E(f["origin"]["campaign"])) if f.get("origin",{}).get("campaign") else ""}{(" · "+E(t("first_seen"))+" "+E(f["seen"][0]["date"])) if f["seen"] else ""}</p><p class="found">{E(t("seen_on"))}<strong>{E(" · ".join(corpora_of(f)) or t("no_obs_short"))}</strong></p>
<div class="badges">{('<span class="pill" style="--c:'+SEVERITY[f["legacy_severity"]][1]+'">'+E(SEVERITY[f["legacy_severity"]][0])+'</span>') if f.get("legacy_severity") in SEVERITY else ''}{('<span class="pill era">'+E({"ancient_only":"ancient documents only","both":"both eras","born_modern":"born with the modern","not_settled":"era not settled"}[f["era"]["value"]])+('  ·  worse now' if f["era"].get("aggravated_by_the_modern") else '')+'</span>') if f.get("era") else ''}<span class="pill" style="--c:{d[2]}">{E(d[0])}</span><span class="pill grey">{E(t("from"))} {E(f.get("origin",{}).get("organisation","—"))}</span><span class="pill grey">{E(CLASS[f['class']])}</span><span class="pill grey">layer: {E(f['layer'])}</span><span class="pill grey">injection: {E(f.get('injection','—'))}</span><span class="pill warn">{E(f['status'].replace('_',' '))}</span></div>
<div class="facts"><div><h3>{E(t("h_damage"))}</h3><p><strong>{E(d[0])}</strong> — {E(d[1])}.</p></div>
<div><h3>{E(t("h_cancel"))}</h3><p>{E(t('yes')) if prev['cancellable_by_code'] else E(t('no'))}{('. '+E(t('refusal'))+' '+E(prev.get('refusal_clause_fr') if LANG=='fr' else prev['refusal_clause'])) if prev.get('refusal_clause') else ''}{('. '+E(prev['note'])) if prev.get('note') else ''}.</p></div>
<div><h3>{E(t("h_restore"))}<span class="opt">{E(t("classified"))}</span></h3><p><strong>{E(REACH[rep['reachable_by_deletion']])}</strong> — {E(REPAIR_NOTE[LANG].get(rep['reachable_by_deletion'], ''))}{'; '+E(REPAIR_SRC[LANG]) if 'derived from the damage class' in (rep.get('note') or '') else ''}.</p></div>
<div><h3>{E(t("h_judge"))}</h3><p>{', '.join(E(JUDGE[j]) for j in f['judgeable_by']) or '<span class="muted">none known yet</span>'}.</p></div></div>
{('<p class="muted small">Searched and not found in: '+E('; '.join(f['observed_absent_in']))+'.</p>') if f.get('observed_absent_in') else ''}
{('<div class="facts"><div><h3>'+E(t("costs_prop"))+'</h3><p><strong>'+E(SEVERITY[f["proposed_severity"]["value"]][0])+'.</strong> '+E(f["proposed_severity"].get("reason_fr") if LANG=="fr" else f["proposed_severity"]["reason"])+'</p><p class="noprobe">'+E(prop_note(f))+'</p><p class="meta">First reading by '+E(f["proposed_severity"]["proposed_by"])+' on '+E(f["proposed_severity"]["date"])+'. '+E(PROP_STATUS[LANG])+'</p></div></div>') if f.get("proposed_severity") else ''}
{('<div class="facts"><div><h3>'+E(t("reaches"))+'</h3><p><strong>'+E(f["registry_scope"].get("extent_fr") if LANG=="fr" else f["registry_scope"]["extent"])+'</strong></p><p class="meta">'+E(SCOPE_WHY[LANG])+'</p></div></div>') if f.get("registry_scope") else ''}
{('<div class="facts"><div><h3>'+E(t("costs"))+'</h3><p><strong>'+E(SEVERITY[f["legacy_severity"]][0])+'.</strong> '+E(SEVERITY[f["legacy_severity"]][2])+'</p><p class="meta">'+E(t('sev_meta')).replace('§', E(f["legacy_severity"]))+'</p>') if f.get("legacy_severity") in SEVERITY else ''}
{('<div class="facts"><div><h3>'+E(t("seen_years"))+'</h3><p><strong>'+E(" · ".join(f"{y} ({n})" for y, n in sorted(f["document_years"]["counts"].items())))+'</strong> {E(t("years_tail"))}</p><p class="meta">'+E(YEARS_SRC[LANG])+'</p></div></div>') if f.get("document_years") else ''}
{('<div class="facts"><div><h3>'+E(t("repairs"))+'</h3><p><strong>'+E(t("judged"))+' '+E(REACH[f["repair"]["reachable_by_deletion"]])+'</strong> '+E(t("judged_how"))+' <strong>'+E(t("measured"))+' '+E(MEASURED_V[LANG][f["repair"]["measured"]["value"]])+'</strong>: '+E(MEASURED_NOTE[LANG].get(f["damage"],""))+'</p>'+('<p class="noprobe"><strong>'+E(t("disagree"))+'</strong> '+E(t("disagree_2"))+' '+E(f["repair"]["measured"]["disagrees_with_the_judgment"])+'.</p>' if f["repair"]["measured"].get("disagrees_with_the_judgment") else '')+'<p class="meta">'+E(MEASURED_SRC[LANG])+'</p></div></div>') if f.get("repair",{}).get("measured") else ''}
{('<div class="facts"><div><h3>'+E(t("fails"))+'</h3><p><strong>'+E(MODE_LABEL[f["failure_mode"]["value"]])+'</strong>. '+E(MODE_MEANS[LANG][f["failure_mode"]["value"]])+'</p><p class="meta">'+E(MODE_SRC[LANG])+'</p></div></div>') if f.get('failure_mode') else ''}
{('<div class="facts"><div><h3>'+E(t("applies"))+'</h3><p><strong>'+E({"ancient_only":"Documents of the old era only","both":"Both eras, 1957 and 2026 alike","born_modern":"Born with the modern era","not_settled":"Era not settled"}[f["era"]["value"]])+'</strong>'+(' — and worse now than it was' if f["era"].get("aggravated_by_the_modern") else '')+('. '+E(f["era"]["note"]) if f["era"].get("note") else '')+'</p><p class="meta">'+E(f["era"]["source"])+'</p></div></div>') if f.get('era') else ''}
<h2>{E(t("h_seen"))}</h2>{seen}
<h2>{E(t("h_spec"))}</h2>{spec}
{related_block(f)}
<h2>{E(t("h_hist"))}</h2><ul class="hist">{hist}</ul>
<p class="muted">Record: <a href="../atlas.json">atlas.json</a> · <a href="{REPO}/blob/main/forms/{E(src_name)}">source file on GitHub</a> · <a href="{E(f['id'])}.json">this record as JSON</a> · <a href="{DATA}/forms/{E(f['id'])}">{E(t("explorer_row"))}</a></p>"""
    (SITE/"forms"/f"{f['id']}.html").write_text(layout(f"{nom(f)} — Fault Atlas", body, depth=1, desc=f"{nom(f)} : {d[0].lower()} — {d[1]}." if LANG=="fr" else f"{nom(f)}: {d[0].lower()} — {d[1]}."))


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
.aside{margin:14px 0 0;font-size:14px;color:var(--muted)}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:0 0 12px}input,select,textarea{font:inherit;font-size:15px;padding:10px 12px;border:1px solid var(--line-strong);border-radius:8px;background:#fff;color:var(--fg)}.bar input{flex:1;min-width:220px}input:focus,select:focus{outline:2px solid var(--acc-soft);border-color:var(--acc)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff}table{border-collapse:collapse;width:100%;table-layout:fixed}#t th:nth-child(1),#t td:nth-child(1){width:32%}#t th:nth-child(2),#t td:nth-child(2){width:12%}#t th:nth-child(3),#t td:nth-child(3){width:9%}#t th:nth-child(4),#t td:nth-child(4){width:12%}#t th:nth-child(5),#t td:nth-child(5){width:11%}#t th:nth-child(6),#t td:nth-child(6){width:14%}#t th:nth-child(7),#t td:nth-child(7){width:10%}#t td{overflow-wrap:anywhere}th,td{text-align:left;padding:11px 14px;border-top:1px solid var(--line);vertical-align:top}th{border-top:0;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:600;background:var(--bg-elev)}td.num{text-align:right;font-family:var(--mono);font-size:14px}td.src{font-size:13px;color:var(--luxe)}td.date{font-family:var(--mono);font-size:12.5px;white-space:nowrap;color:var(--muted)}
#t th{cursor:pointer;user-select:none;position:relative}#t th:hover{color:var(--ink)}
#t th.sorted-asc::after{content:" ▲";font-size:9px}#t th.sorted-desc::after{content:" ▼";font-size:9px}
td.proof{font-size:13px}td.p-docs{color:#166534;font-weight:600}td.p-none{color:var(--muted)}label.chk{display:inline-flex;align-items:center;gap:6px;font-size:14px;color:var(--ink)}label.chk input{width:auto;min-width:0;flex:none}table.kv th{width:190px;text-transform:none;letter-spacing:0;font-size:14px;color:var(--ink);background:transparent;border-top:1px solid var(--line)}table.kv td code{font-size:12.5px;white-space:normal;word-break:break-all}td.mono{font-family:var(--mono);font-size:12px}
.pill{display:inline-block;white-space:nowrap;padding:2px 10px;border-radius:999px;font-size:12.5px;font-weight:600;color:#fff;background:var(--c);letter-spacing:.01em}.pill.grey{background:var(--surface);color:var(--fg);font-weight:500}.pill.era{background:#f5f3ff;color:#5b21b6;border:1px solid #ddd6fe}
.lang{display:inline-flex;align-items:center;gap:5px;font-weight:600;font-size:13px;letter-spacing:.04em}.lang svg{opacity:.7}
.pill.warn{background:#fff3c4;color:#6b4c00;font-weight:500}
.fr{color:var(--muted);font-size:13px;font-family:var(--serif);font-style:italic}.fr.big{font-size:17px;margin-top:-10px}.muted{color:var(--muted)}
.ceiling{margin-top:48px;border-top:1px solid var(--line);padding-top:32px}.ceiling .lead{color:var(--luxe);font-size:15.5px;max-width:68ch}.ceiling p{max-width:74ch;font-size:15px;color:var(--luxe)}.ceiling .tablewrap{margin:20px 0;max-width:820px}table.reach{table-layout:auto}table.reach td:nth-child(2),table.reach td:nth-child(3){text-align:right;font-family:var(--mono);font-size:14px;white-space:nowrap}table.reach td:nth-child(4){font-size:13px;color:var(--muted)}table.reach tr.yes td:nth-child(4){color:#3f6212;font-weight:600}table.reach tr.yes td:first-child{font-weight:600}table.reach em{color:var(--muted);font-style:normal}.about{margin-top:56px;border-top:1px solid var(--line);padding-top:32px}.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:24px}.cols p{margin:0;color:var(--luxe);font-size:15px}
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
print(f"site: {len(forms)} form pages + index, v{VERSION} [{LANG}]")

# The server rebuilds with the documented command, which knows nothing of --fr. So the plain run
# builds both languages: asking ops to change a command is a change that never happens.
if LANG == "en":
    import subprocess
    subprocess.run([sys.executable, __file__, "--fr"], check=True)
