#!/usr/bin/env python3
"""One-shot migration of the 2026-08-09 catalogue (korela.db, 139 lines) into Fault Atlas form records.
Run once; afterwards the JSON files are the source of truth and this script is history.
Classification by damage and injection was done line by line on 2026-09-09 (see docs/VERIFICATION-2026-09-09.md)."""
import json, re, sqlite3, sys, unicodedata
from pathlib import Path

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()/"Coffre-local/Korela For Science/korela.db"
OUT = Path(__file__).resolve().parent.parent/"forms"
OUT.mkdir(exist_ok=True)

# damage, injection — per line, judgment of 2026-09-09
C = {
12:("CORPUS_PARAMETER","PARAMETER"),13:("CORPUS_PARAMETER","PARAMETER"),14:("WRONG_LABEL","DESIGN"),15:("WRONG_LABEL","CONSTRAINT"),16:("CORPUS_PARAMETER","DUPLICATE"),
17:("MISSING","FORMAT"),18:("MISSING","FORMAT"),19:("SPURIOUS_EDGE","INSERT"),20:("SPURIOUS_EDGE","FORMAT"),21:("SPLIT","RENAME"),22:("MERGE","RENAME"),
23:("SPLIT","NOISE"),24:("MERGE","RENAME"),25:("MERGE","ALTER"),26:("MERGE","RENAME"),27:("SPLIT","RENAME"),28:("MERGE","DESIGN"),
29:("SPLIT","RENAME"),30:("MISSING","MOVE"),31:("SPURIOUS_EDGE","ALTER"),32:("ANACHRONISM","ALTER"),33:("WRONG_LABEL","RENAME"),34:("WRONG_LABEL","INSERT"),
35:("WRONG_VALUE","ALTER"),36:("WRONG_VALUE","ALTER"),37:("CORPUS_PARAMETER","INSERT"),38:("SPURIOUS_EDGE","DUPLICATE"),39:("ANACHRONISM","DUPLICATE"),40:("MISSING","DELETE"),
41:("MISSING","DELETE"),42:("SPLIT","NOISE"),43:("SPURIOUS_EDGE","FORMAT"),44:("SPLIT","TRANSLATE"),45:("MISSING","IMAGE"),46:("CORPUS_PARAMETER","PARAMETER"),
62:("MISSING","DELETE"),63:("MISSING","MOVE"),64:("SPLIT","FORMAT"),65:("CORPUS_PARAMETER","PARAMETER"),66:("MISSING","FORMAT"),67:("SPLIT","TRANSLATE"),
68:("MISSING","IMAGE"),69:("MERGE","DUPLICATE"),70:("SPURIOUS_EDGE","MOVE"),71:("WRONG_VALUE","ALTER"),72:("CORPUS_PARAMETER","DUPLICATE"),73:("WRONG_VALUE","ALTER"),
74:("SPURIOUS_EDGE","INSERT"),75:("MISSING","FORMAT"),76:("MERGE","RENAME"),77:("WRONG_VALUE","ALTER"),78:("MISSING","FORMAT"),79:("MERGE","NOISE"),
80:("WRONG_VALUE","ALTER"),81:("WRONG_LABEL","INSERT"),82:("MISSING","IMAGE"),83:("MISSING","MOVE"),84:("WRONG_VALUE","ALTER"),85:("WRONG_VALUE","ALTER"),86:("SPLIT","RENAME"),
87:("WRONG_VALUE","ALTER"),88:("MERGE","RENAME"),89:("SPURIOUS_EDGE","FORMAT"),90:("MISSING","MOVE"),91:("ANACHRONISM","ALTER"),92:("MISSING","NOISE"),
93:("SPURIOUS_EDGE","INSERT"),94:("SPURIOUS_EDGE","INSERT"),95:("WRONG_LABEL","ALTER"),96:("SPLIT","RENAME"),97:("MISSING","IMAGE"),100:("WRONG_VALUE","ALTER"),
101:("MISSING","MOVE"),102:("MISSING","FORMAT"),103:("WRONG_LABEL","ALTER"),104:("MISSING","FORMAT"),105:("WRONG_VALUE","ALTER"),106:("MISSING","NOISE"),
107:("MERGE","INSERT"),108:("SPLIT","ALTER"),109:("MISSING","FORMAT"),110:("WRONG_LABEL","INSERT"),111:("WRONG_VALUE","IMAGE"),112:("WRONG_VALUE","IMAGE"),
113:("MISSING","DELETE"),114:("SPURIOUS_EDGE","INSERT"),115:("SPURIOUS_EDGE","INSERT"),116:("SPURIOUS_EDGE","INSERT"),117:("ANACHRONISM","ALTER"),118:("SPLIT","NOISE"),
119:("WRONG_LABEL","IMAGE"),120:("SPLIT","RENAME"),121:("CORPUS_PARAMETER","PARAMETER"),122:("MISSING","FORMAT"),123:("SPURIOUS_EDGE","ALTER"),124:("WRONG_VALUE","FORMAT"),
125:("MISSING","MOVE"),126:("MISSING","FORMAT"),127:("MISSING","MOVE"),128:("SPLIT","FORMAT"),129:("SPURIOUS_EDGE","INSERT"),130:("MISSING","FORMAT"),
131:("MISSING","FORMAT"),132:("MISSING","FORMAT"),133:("MISSING","FORMAT"),134:("SPURIOUS_EDGE","INSERT"),135:("WRONG_VALUE","TRANSLATE"),136:("SPURIOUS_EDGE","FORMAT"),
137:("WRONG_VALUE","ALTER"),138:("WRONG_VALUE","ALTER"),139:("MISSING","FORMAT"),140:("ANACHRONISM","ALTER"),141:("MISSING","DUPLICATE"),
}
EN = {
12:"Corpus volume",13:"Distribution of relation types",14:"Entity typing",15:"Schema constraints",16:"Fact redundancy across documents",
17:"Diversity of document templates",18:"Variable length and chunking",19:"Salience and distractors",20:"Layout furniture (headers, footers)",21:"Multiple spellings of one entity",
22:"Pronominal references",23:"Typos and OCR confusions",24:"Acronyms and abbreviations",25:"Registry identifiers",26:"Strict homonyms",
27:"Name-to-address bridge",28:"One person in two roles",29:"Entities that change identity",30:"Facts spread across documents",31:"Degree of assertion of a link",
32:"Link status: never, or expired",33:"Confusable relation types",34:"Hard negatives for typing",35:"Undated contradiction",36:"Relative dates",
37:"Density: documents of no interest",38:"Exact and near duplicates",39:"Successive versions of a document",40:"Cited documents absent from the corpus",41:"Truncated or unreadable documents",
42:"Names damaged by scanning",43:"Tables with multi-level headers",44:"Several languages in one corpus",45:"Genuinely scanned pages",46:"Incremental ingestion",
62:"Document reduced to its title",63:"The title carries the fact",64:"Period typographic conventions",65:"Temporal span of the corpus",66:"Multi-column layout",
67:"Bilingual document",68:"The fact is in the figure",69:"Several documents in one file",70:"Bibliographic references",71:"Multiple dates on one document",
72:"Redundancy between text and table",73:"Values with quantified uncertainty",74:"Content quoted from elsewhere",75:"Multiple citation conventions",76:"Anonymised entities",
77:"Local and ambiguous date formats",78:"Structured abstract in numbered points",79:"Scientific notation inside names",80:"Relative quantified relations",81:"Equipment and supplier entities",
82:"Landscape-oriented table",83:"The table carries its own definitions",84:"Non-atomic cells",85:"Non-standard decimal separator",86:"One compound, several names",
87:"Mixed units and conventions",88:"Collective entity",89:"Complex attributions and affiliations",90:"Text-to-figure reference by label",91:"Dense relative chronology",
92:"Drop cap",93:"Content added by digitisation",94:"Editorial metadata",95:"The study type qualifies all its facts",96:"Methods as entities with a genealogy",
97:"The three PDF regimes (native, OCR layer, pure image)",100:"Sample size written in words",101:"Sample size is computed, not stated",102:"Furniture language differs from body language",103:"Significance marker with two meanings",
104:"No apparatus at all",105:"Abbreviation dot inside a unit",106:"Signature mark of a gathering",107:"Several DOIs per document",108:"Partial ORCID",
109:"Structured abstract",110:"Pre-registration identifier",111:"Forest plot as image",112:"Ordinal scale by colour",113:"Supplementary material cited and absent",
114:"Author declarations",115:"Licence on page 1",116:"Open peer-review furniture",117:"Crossmark badge (retraction status)",118:"Unicode traps in native PDF",
119:"Coloured hyperlinks carrying a type",120:"Running head with dotted initials",121:"Access format of the document (PDF, HTML, XML)",122:"Numbered display equation",123:"Bare-number reference with ambiguous target",
124:"Quantifier in a column right of the equation",125:"Numbered theorem whose body is the claim",126:"Pseudo-code with double numbering",127:"Structured object presented as a figure",128:"Acronym defined by typography alone",
129:"Repository cover page prepended to the article",130:"Two conflicting paginations",131:"Display mathematics inside the abstract",132:"Clickable zone differs from semantic unit",133:"HTML fragments the text",
134:"Page 1 is not representative",135:"Translated verbatim",136:"Columns of different natures",137:"Three kinds of number in one string",138:"Mnemonic superscript that is not a power",
139:"Citation with internal locator",140:"Editorial status printed in the document",141:"Multiple abstracts from different registries",
}
REACH = {"SPURIOUS_EDGE":"yes","ANACHRONISM":"yes","WRONG_LABEL":"partial","MERGE":"no","SPLIT":"no","MISSING":"no","WRONG_VALUE":"no","CORPUS_PARAMETER":"no"}
REACH_NOTE = {"yes":"the faulty edge can be deleted","partial":"an extra label can be deleted, a missing one cannot be added","no":"deletion cannot restore this; judgment of 2026-09-09, to be measured"}
JUDGE = {"MERGE":["construction","registry","curated","closed_world"],"SPLIT":["construction","registry","curated","closed_world"],
         "SPURIOUS_EDGE":["construction","curated","closed_world"],"MISSING":["construction","curated","closed_world"],
         "WRONG_VALUE":["construction","registry","dated_future","closed_world"],"WRONG_LABEL":["construction","curated"],
         "ANACHRONISM":["construction","registry","dated_future","closed_world"],"CORPUS_PARAMETER":[]}

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")[:48]

def klass(annulable, partiel, dest):
    if annulable == "V": return "DEFEATED"
    if annulable == "VX": return "DEFEATED_IF_XML"
    if partiel == "PA": return "REFUSABLE"
    if partiel == "PR": return "SILENT_FALSE"
    if annulable == "I": return "IRREDUCIBLE"
    return "UNCLASSIFIED"

con = sqlite3.connect(DB)
rows = con.execute("""select p.ligne,p.nom,p.couche,p.gravite,p.mode_echec,p.mecanisme,p.annulable,p.partiel,s.destination,s.motif
  from parametre p left join selection s on s.ligne=p.ligne and s.domaine='science' order by p.ligne""").fetchall()
filt = {r[0]: r for r in con.execute("select ligne,fichier,dossier,nature,vu,cas,contre_exemples,vert from filtre")}
diff = {r[0]: r for r in con.execute("select ligne,fichier,vu,touche,marques from difficulte")}

out_of_scope, n = [], 0
for ligne,nom,couche,grav,mode,meca,annul,partiel,dest,motif in rows:
    if dest == "HORS":
        out_of_scope.append({"legacy_line":ligne,"name_fr":nom,"reason":"instrument, metric or discovery property — not a fault form"}); continue
    damage, inj = C[ligne]
    seen = []
    for src in (filt.get(ligne), diff.get(ligne)):
        if src and src[2 if src is filt.get(ligne) else 2]:
            pass
    if ligne in filt and filt[ligne][4]:
        seen.append({"corpus":"observation 2026-08 (Europe PMC JATS 2023-2026 and PubMed abstracts)","date":"2026-08-08","observer":"house observer (LLM agent), see report","excerpt":filt[ligne][4],"lang":"fr"})
    if ligne in diff and diff[ligne][2] and (ligne not in filt or diff[ligne][2] != filt[ligne][4]):
        seen.append({"corpus":"observation 2026-08 (272 Europe PMC JATS articles)","date":"2026-08-08","observer":"house observer (LLM agent), see report","excerpt":diff[ligne][2],"lang":"fr"})
    rec = {
      "id": f"form-{ligne:03d}", "version": 1, "legacy_line": ligne,
      "name": EN[ligne], "name_fr": nom,
      "damage": damage, "class": klass(annul, partiel, dest), "layer": couche or "",
      "injection": inj, "legacy_severity": (grav or "").split()[-1] if grav else "", "legacy_mechanism": meca or "",
      "status": "migrated_unreviewed",
      "seen": seen,
      "specimens": {"cases": [], "counter_examples": []},
      "prevention": {"cancellable_by_code": annul in ("V","VX") or partiel == "PA",
                     **({"refusal_clause": "handle, or abstain and declare — never guess"} if partiel == "PA" else {}),
                     **({"note": "cancelled only when the source is structured (XML/HTML); not on composed PDF"} if annul == "VX" else {})},
      "repair": {"reachable_by_deletion": REACH[damage], "note": REACH_NOTE[REACH[damage]]},
      "judgeable_by": JUDGE[damage],
      "history": [{"date":"2026-08-09","event":f"catalogue line {ligne} — {dest}: {motif or ''}".strip(),"by":"Korela For Science"},
                  {"date":"2026-09-09","event":f"migrated; classified damage={damage} injection={inj} (judgment, unreviewed by a second reader)","by":"Fault Atlas migration"}],
    }
    if dest == "ACCEPTE": rec["observed_absent_in"] = ["Europe PMC JATS 2023-2026 (272 articles, measured 2026-08-08)"]
    if ligne in filt:
        rec["history"].append({"date":"2026-08-08","event":f"house filter exists with {filt[ligne][5]} cases and {filt[ligne][6]} counter-examples (bench green={bool(filt[ligne][7])}); specimens to be transcribed into this record","by":"Korela For Science"})
    (OUT/f"form-{ligne:03d}-{slug(EN[ligne])}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2)+"\n")
    n += 1
(Path(__file__).resolve().parent.parent/"docs"/"out-of-scope-2026-08.json").write_text(json.dumps(out_of_scope, ensure_ascii=False, indent=2)+"\n")
print(f"{n} forms written, {len(out_of_scope)} out of scope")
