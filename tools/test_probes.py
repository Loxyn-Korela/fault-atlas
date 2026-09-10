#!/usr/bin/env python3
"""Every Python probe loads, declares exactly one question, and runs on an empty
document (or empty corpus) without crashing. Non-Python probes must carry their
endpoint or command in their header. Exit 1 on the first failure."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from run_probe import load

bad = 0; n = 0
for f in sorted((ROOT / "probes").rglob("*")):
    if f.is_dir() or f.name == "README.md" or "results" in f.parts:
        continue
    n += 1
    text = f.read_text(encoding="utf-8")
    try:
        if f.suffix == ".py" and "CORPUS_PROBE" not in text and "def main(" not in text and "__main__" not in text:
            ns = load(f)
            assert len(ns["SONDES"]) == 1, f"{len(ns['SONDES'])} questions declared, expected 1"
            (line, (title, fn)), = ns["SONDES"].items()
            assert isinstance(fn(""), list), "probe must return a list"
            assert isinstance(fn("<article><body><p>x</p></body></article>"), list)
        elif f.suffix == ".py" and "CORPUS_PROBE" in text:
            ns = load(f)
            assert ns.get("CORPUS_PROBE") and callable(ns.get("probe")), "corpus probe needs probe(text)"
            assert isinstance(ns["probe"](""), list)
        elif f.suffix == ".py":
            compile(text, str(f), "exec")
            assert "Run:" in text, "header must say how to run it"
        elif f.suffix == ".sparql":
            assert "publications.europa.eu/webapi/rdf/sparql" in text, "header must name the endpoint"
            assert "SELECT" in text or "CONSTRUCT" in text
        elif f.suffix == ".sh":
            assert "curl" in text and "Accept" in text
        else:
            raise AssertionError("unknown probe type")
    except Exception as e:
        bad += 1; print(f"FAIL  {f.relative_to(ROOT)}: {e}")
print(f"{n - bad}/{n} probes load and answer")
sys.exit(1 if bad else 0)
