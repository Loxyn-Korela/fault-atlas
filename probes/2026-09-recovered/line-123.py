"""Fault Atlas probe — line 123 (form-123): a bare-number reference with an ambiguous target.
August: 2,280 references of the form "(N)" over 140/272 articles, 94.8 % with no lead-in.
    python3 tools/run_probe.py probes/2026-09-recovered/line-123.py <dir with the 272 .xml>
"""
import re
SONDES = {}
def sonde(l, n):
    def d(f): SONDES[l] = (n, f); return f
    return d
def _body(x):
    m = re.search(r"(?s)<body\b.*?</body>", x); return m.group(0) if m else x
def _txt(x):
    return re.sub(r"<[^>]+>", " ", x)

@sonde(123, "a bare number in parentheses with nothing saying what it points at")
def d123(x):
    t = _txt(_body(x))
    bare = re.findall(r"(?<![A-Za-z.])\((\d{1,3})\)", t)
    led = re.findall(r"(?i)\b(?:Eq|Fig|Figure|Table|Ref|Equation)\.?\s*\((\d{1,3})\)", t)
    n = len(bare) - len(led)
    return [f"{n} bare (N) references with no lead-in"] if n > 0 else []
