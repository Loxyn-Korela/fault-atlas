"""Fault Atlas probe — catalogue line 21 (form-021).
Extracted verbatim from the August 2026 observation campaign (Loxyn SAS, Lyon).
A probe answers one question on one JATS XML file: "is this fault here, and where?"
It repairs nothing and decides nothing. Returns a list of excerpts, empty if absent.

Run on the reproducible corpus (see corpora/europe-pmc-jats-2023-2026-272.json):
    python3 tools/run_probe.py probes/2026-08/line-021.py <dir with the 272 .xml>
"""
import re, collections, unicodedata

SONDES = {}
def sonde(ligne, nom):
    def deco(f): SONDES[ligne] = (nom, f); return f
    return deco

# ── 21 · GRAPHIES MULTIPLES : « Forme Longue (ACRO) », puis « ACRO » tout seul
# ⚠️ 1re version CORRIGÉE : elle rendait « By extracting tumor volume (TV) » — les
#    initiales étaient cherchées EN SOUS-CHAÎNE, donc l'empan de la forme longue
#    débordait. On exige maintenant une correspondance EXACTE, et on prend le plus
#    court segment qui la donne. Hors correspondance exacte : refus, pas de devinette.
GLOSE = re.compile(r"((?:[\wÀ-ÿ'’\-]+ ){1,8})\(([A-Z][A-Za-z0-9]{1,6})\)")

def _corps(x):
    m = re.search(r'(?s)<body\b.*?</body>', x)
    return m.group(0) if m else ''

def _forme_longue(avant, acro):
    lettres = ''.join(c for c in acro if c.isalpha()).lower()
    mots = [m for m in avant.split() if m]
    for depart in range(len(mots) - 1, -1, -1):       # du plus COURT au plus long
        seg = mots[depart:]
        ini = ''.join(p[0] for w in seg for p in w.split('-') if p).lower()
        if ini == lettres:
            return ' '.join(seg)
    return None

def _txt(x):
    return re.sub(r'<[^>]+>', ' ', x)

@sonde(21, "graphies multiples d'une entité (forme longue + acronyme réutilisé)")
def d21(x):
    t = _txt(_corps(x)) or _txt(x)
    out = []
    for avant, acro in GLOSE.findall(t):
        longue = _forme_longue(avant, acro)
        if not longue or len(acro) < 2:
            continue
        # l'acronyme doit être RÉUTILISÉ seul : sinon ce n'est pas une 2e graphie
        if len(re.findall(r'\b%s\b' % re.escape(acro), t)) >= 2:
            out.append(f"{longue} ({acro})")
    return sorted(set(out))[:5]
