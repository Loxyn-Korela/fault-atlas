#!/usr/bin/env python3
"""Re-run every Python document probe declared in the forms on a corpus directory,
and write the dated result back into each form's `probes[].result`; the full list of
carrier documents with their evidence goes to probes/results/<probe>.json (`carriers_file`).

    python3 tools/rerun_probes.py <dir with the .xml files> [--corpus corpus-europe-pmc-jats-2023-2026] [--by "name"]

Only probes whose `corpus_id` matches --corpus and whose kind is `python` (document
probes, not corpus probes) are run. The previous result is replaced: a re-run is a
new dated measurement, and the excerpt keeps the original figure. `matches_excerpt`
is left as it was; it is a human judgment on the excerpt, not a test.
Prints one line per probe: form, old count, new count.
"""
import sys, json, pathlib, datetime, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from run_probe import load, run_document_probe

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    corpus_dir = args[0]
    corpus_id = "corpus-europe-pmc-jats-2023-2026"
    by = "Fault Atlas tools"
    for i, a in enumerate(sys.argv):
        if a == "--corpus": corpus_id = sys.argv[i + 1]
        if a == "--by": by = sys.argv[i + 1]
    today = datetime.date.today().isoformat()
    changed = 0
    for fp in sorted((ROOT / "forms").glob("form-*.json")):
        rec = json.loads(fp.read_text(encoding="utf-8"))
        touched = False
        for pr in rec.get("probes", []):
            if pr["kind"] != "python" or pr["corpus_id"] != corpus_id:
                continue
            ns = load(ROOT / pr["file"])
            if ns.get("CORPUS_PROBE"):
                continue
            res = run_document_probe(ns, corpus_dir)
            old = pr.get("result", {}).get("count")
            cf = pathlib.Path("probes/results") / (pathlib.Path(pr["file"]).stem + ".json")
            (ROOT / cf).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / cf).write_text(json.dumps({"probe": pr["file"], "corpus_id": corpus_id, "date": today, "count": res["carriers"], "of": res["of"],
                                               "carriers": [{"document": n, "evidence": e} for n, e in res["all"]]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            pr["result"] = {"date": today, "count": res["carriers"], "of": res["of"],
                            "strata": res["strata"], "examples": [[n, e[:2]] for n, e in res["all"][:12]], "by": by,
                            "carriers_file": str(cf)}
            print(f"{rec['id']}  {pr['file']}  {old} -> {res['carriers']}/{res['of']}")
            touched = True
        if touched:
            fp.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed += 1
    print(f"{changed} forms updated")


if __name__ == "__main__":
    main()
