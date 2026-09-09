#!/usr/bin/env python3
"""Run one probe and print what it finds. No model, no network, stdlib only.

A probe answers one question on one document: "is this fault here, and where?"
It repairs nothing and decides nothing. It returns a list of excerpts, empty if
the fault is absent. This runner counts the carrier documents and shows examples.

    python3 tools/run_probe.py probes/2026-08/line-036.py <dir with the JATS .xml files>
    python3 tools/run_probe.py probes/2026-08/line-064-arginine-titles.py <corpus .md file>
    python3 tools/run_probe.py ... --json          # machine-readable result

Two kinds of Python probe:
  document probe  — the module registers one function in SONDES via @sonde(line, name);
                    the runner calls it on every *.xml of the directory.
  corpus probe    — the module sets CORPUS_PROBE = True and defines probe(text) -> list;
                    the runner calls it once on the whole file and counts the hits.

SPARQL (.sparql) and shell (.sh) probes are not run by this tool: their file is
the query itself, with the endpoint and the expected answer in its header.
"""
import sys, json, pathlib, collections, datetime


def load(probe_path):
    ns = {"__name__": "probe", "__file__": str(probe_path)}
    exec(compile(probe_path.read_text(encoding="utf-8"), str(probe_path), "exec"), ns)
    return ns


def run_document_probe(ns, corpus_dir):
    (line, (title, fn)), = ns["SONDES"].items()
    files = sorted(pathlib.Path(corpus_dir).glob("*.xml"))
    carriers = []
    for f in files:
        x = f.read_text(encoding="utf-8", errors="replace")
        try:
            e = fn(x)
        except Exception as ex:  # a probe that crashes is reported, not hidden
            e = [f"EXCEPTION {ex}"]
        if e:
            carriers.append((f.name, [str(v) for v in e]))
    strata = collections.Counter(n.split("-")[0] for n, _ in carriers)
    return {"line": line, "title": title, "of": len(files), "carriers": len(carriers),
            "strata": dict(strata.most_common()),
            "examples": [[n, e[:3]] for n, e in carriers[:3]]}


def run_corpus_probe(ns, corpus_file):
    text = pathlib.Path(corpus_file).read_text(encoding="utf-8", errors="replace")
    hits = ns["probe"](text)
    return {"line": ns.get("LINE"), "title": ns.get("TITLE", ""), "of": ns.get("population", lambda t: None)(text),
            "carriers": len(hits), "strata": {}, "examples": [[str(h), []] for h in hits[:3]]}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    probe_path, target = pathlib.Path(args[0]), args[1]
    if probe_path.suffix != ".py":
        sys.exit(f"{probe_path}: not a Python probe; open the file, the query and the endpoint are inside.")
    ns = load(probe_path)
    res = run_corpus_probe(ns, target) if ns.get("CORPUS_PROBE") else run_document_probe(ns, target)
    res["probe"] = str(probe_path)
    res["date"] = datetime.date.today().isoformat()
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    print(f"{res['probe']} — {res['title']}")
    print(f"  carriers: {res['carriers']}/{res['of']}   ({res['date']})")
    if res["strata"]:
        print("  by stratum: " + ", ".join(f"{k} {v}" for k, v in res["strata"].items()))
    for name, ex in res["examples"]:
        print(f"  {name}: {' | '.join(ex)[:160]}")


if __name__ == "__main__":
    main()
