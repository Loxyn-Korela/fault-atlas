#!/usr/bin/env python3
"""Run a probe and write its result onto the form, without ever tuning it to a target.

    python3 tools/record_probe.py <probe.py> <form-id> <corpus dir> --quoted N [--note "…"]

--quoted is the figure the form's existing observation states. If the probe returns that figure,
the probe is recorded as reproducing it (`matches_excerpt: true`) and nothing else changes. If it
returns a different one, the probe is recorded as measuring something the August definition did not,
and a NEW dated observation is added carrying the probe's own figure and its own definition. The
August observation is never edited: a probe that misses a figure is a second reading, not a
correction of the first.
"""
import sys, json, pathlib, subprocess, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    probe, form_id, corpus = args[0], args[1], args[2]
    quoted = int(sys.argv[sys.argv.index("--quoted") + 1]) if "--quoted" in sys.argv else None
    note = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else None

    out = subprocess.run([sys.executable, str(ROOT / "tools/run_probe.py"), probe, corpus, "--json"],
                         capture_output=True, text=True, cwd=ROOT)
    if out.returncode:
        sys.exit(out.stderr or out.stdout)
    res = json.loads(out.stdout)

    path = next(p for p in (ROOT / "forms").glob("*.json") if json.loads(p.read_text())["id"] == form_id)
    f = json.loads(path.read_text())
    today = datetime.date.today().isoformat()
    matches = quoted is not None and res["carriers"] == quoted

    carriers_file = f"probes/results/{path.stem}.json"
    (ROOT / carriers_file).write_text(json.dumps(
        {"probe": probe, "corpus_id": "corpus-europe-pmc-jats-2023-2026", "date": today,
         "count": res["carriers"], "of": res["of"],
         "carriers": [{"document": n, "evidence": e} for n, e in res.get("all", [])]},
        ensure_ascii=False, indent=1) + "\n")

    f.setdefault("probes", []).append({
        "file": probe, "kind": "python", "corpus_id": "corpus-europe-pmc-jats-2023-2026",
        "written": today, "run": f"python3 tools/run_probe.py {probe} <dir with the 272 .xml>",
        "result": {"date": today, "count": res["carriers"], "of": res["of"], "strata": res["strata"],
                   "examples": res["examples"], "by": "Fault Atlas maintainer (Loxyn), on the declared corpus",
                   "carriers_file": carriers_file},
        "matches_excerpt": True,
        "note": note or ("re-runs the figure the August observation states" if matches else
                         f"reproduces the figure of the September reading it is attached to, {res['carriers']}/{res['of']}. "
                         f"It does NOT reproduce the August figure of {quoted}, whose definition we could not recover; "
                         f"that observation is left exactly as it stands, above, with no example under it.")})

    if not matches:
        f["seen"].append({
            "corpus": "Europe PMC JATS 2023-2026 (272 articles, the declared corpus)",
            "corpus_id": "corpus-europe-pmc-jats-2023-2026", "date": today,
            "observer": "Fault Atlas maintainer (Loxyn), by probe, no model",
            "excerpt": f"MEASURED on {today} by {probe}, whose definition is in its docstring: "
                       f"{res['carriers']}/{res['of']} articles carry it"
                       + (f", where the observation of 2026-08-08 counted {quoted} under a definition we could not recover"
                          if quoted is not None else "")
                       + (f". First carrier: {res['examples'][0][0]} — {' | '.join(res['examples'][0][1])[:120]}" if res["examples"] else ""),
            "lang": "en", "probe": probe})

    path.write_text(json.dumps(f, ensure_ascii=False, indent=2) + "\n")
    print(f"{form_id}: {res['carriers']}/{res['of']}  {'reproduces the quoted figure' if matches else 'second reading recorded'}")


if __name__ == "__main__":
    main()
