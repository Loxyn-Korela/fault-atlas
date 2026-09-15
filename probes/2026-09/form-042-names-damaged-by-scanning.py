"""Fault Atlas probe — form-042: names damaged by scanning.
Question: in the OCR layer of scanned PDFs, does a person's name come out with a digit or a wrong
letter inside it — « SKINH0J » for Skinhøj, « WIDER0E » for Widerøe, « MCNA1JGHTON » for McNaughton ?
Population: the 45 biomedical PDFs 1957-1987 of the migraine corpus (form-045: 8 native, 36 with an
OCR layer, 1 pure image). Needs `pdftotext` (poppler); no model, no network.
Run:  python3 probes/2026-09/form-042-names-damaged-by-scanning.py <dir with the 45 .pdf>
It prints every capitalised token carrying a digit between letters, with its document and context;
which of them are names is a reading, done once and written into the form. Written 2026-09-15.
"""
import re, sys, subprocess, pathlib, collections
NOT_NAMES = re.compile(r"(?i)journal|pco2|paco2|pacc2|wc2a|ked5o|june|neurology|medical|joints|kg|ml|mm|hg")
def texts(d):
    for p in sorted(pathlib.Path(d).glob("*.pdf")):
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True)
        yield p.name, r.stdout
def main(d):
    hits = collections.OrderedDict()
    for name, t in texts(d):
        for m in re.finditer(r"\b[A-Z][a-z]*[0-9][A-Za-z]{2,}\b|\b[A-Z][A-Z]+[0-9][A-Z]+\b", t):
            w = m.group(0)
            if NOT_NAMES.search(w): continue
            hits.setdefault(w, (name, re.sub(r"\s+", " ", t[max(0, m.start()-70):m.end()+50])))
    print(f"{len(hits)} candidate tokens in {d}")
    for w, (name, ctx) in hits.items(): print(f"  {w:16} | {name} | …{ctx}…")
if __name__ == "__main__": main(sys.argv[1])
