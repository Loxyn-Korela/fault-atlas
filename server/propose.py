#!/usr/bin/env python3
"""Receives proposals from the site form (POST /propose), keeps a copy on disk, e-mails contact@loxyn.ai.
Standard library only. Run behind the reverse proxy on 127.0.0.1:8002. Nothing external.

  PROPOSE_INBOX=/var/lib/fault-atlas/inbox  PROPOSE_TO=contact@loxyn.ai  PROPOSE_FROM=atlas@loxyn.ai  SMTP_HOST=127.0.0.1  python3 server/propose.py
"""
import json, os, re, smtplib, time
from datetime import datetime, timezone
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

INBOX = os.environ.get("PROPOSE_INBOX", "./inbox"); TO = os.environ.get("PROPOSE_TO", "contact@loxyn.ai")
FROM = os.environ.get("PROPOSE_FROM", "atlas@loxyn.ai"); SMTP = os.environ.get("SMTP_HOST", "127.0.0.1")
SITE = os.environ.get("PROPOSE_SITE", "https://faultatlas.loxyn.ai")
REQUIRED = ["name", "damage", "corpus", "date", "excerpt", "why", "email", "rule_public", "rule_review"]
RATE = {}  # ip -> [timestamps]

def ok_rate(ip):
    now = time.time(); RATE[ip] = [t for t in RATE.get(ip, []) if now - t < 3600] + [now]
    return len(RATE[ip]) <= 5

class H(BaseHTTPRequestHandler):
    def _reply(self, code, location):
        self.send_response(code); self.send_header("Location", location); self.send_header("Content-Length", "0"); self.end_headers()

    def do_POST(self):
        if self.path != "/propose": return self._reply(303, f"{SITE}/propose.html?err=path")
        n = int(self.headers.get("Content-Length", 0))
        if n > 200_000: return self._reply(303, f"{SITE}/propose.html?err=size")
        form = {k: v[0].strip() for k, v in parse_qs(self.rfile.read(n).decode("utf-8", "replace")).items()}
        ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
        if form.get("website"):  # honeypot field, hidden from humans
            return self._reply(303, f"{SITE}/propose.html?sent=1")
        if not ok_rate(ip): return self._reply(303, f"{SITE}/propose.html?err=rate")
        missing = [k for k in REQUIRED if not form.get(k)]
        if missing or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", form["date"]) or "@" not in form["email"]:
            return self._reply(303, f"{SITE}/propose.html?err=missing&fields={','.join(missing)}")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        rec = {"received": stamp, "ip": ip, **{k: v for k, v in form.items() if k != "website"}}
        os.makedirs(INBOX, exist_ok=True)
        path = os.path.join(INBOX, f"{stamp}-{re.sub(r'[^a-z0-9]+', '-', form['name'].lower())[:40]}.json")
        with open(path, "w", encoding="utf-8") as f: json.dump(rec, f, ensure_ascii=False, indent=2)
        try:
            m = EmailMessage(); m["Subject"] = f"[Fault Atlas] proposal: {form['name']}"; m["From"] = FROM; m["To"] = TO; m["Reply-To"] = form["email"]
            m.set_content("A form was proposed on the site.\n\n" + "\n".join(f"{k}: {v}" for k, v in rec.items()) + f"\n\nCopy on disk: {path}")
            with smtplib.SMTP(SMTP, timeout=10) as s: s.send_message(m)
        except Exception as e:
            with open(os.path.join(INBOX, "mail-errors.log"), "a") as f: f.write(f"{stamp}\t{path}\t{e}\n")
        self._reply(303, f"{SITE}/propose.html?sent=1")

    def do_GET(self):
        body = b"ok" if self.path == "/health" else b"not found"
        self.send_response(200 if self.path == "/health" else 404); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a): pass

if __name__ == "__main__":
    print(f"propose handler on 127.0.0.1:8002 → inbox {INBOX}, mail to {TO}", flush=True)
    HTTPServer(("127.0.0.1", 8002), H).serve_forever()
