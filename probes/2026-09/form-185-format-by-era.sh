#!/bin/sh
# Fault Atlas probe — form-185: the text format Cellar serves depends on the act's age.
# Public REST resolution by CELEX, content negotiation on Accept. No key.
# Written 2026-09-09 from lot B (Alexandrie); re-run live 2026-09-09:
#   32026D1970 (2026): xhtml+xml 200, text/html 404
#   31985L0374 (1985): xhtml+xml 404, text/html 200
#   31968R5759 (1968): 404 in both, and in Formex — no text served at all
# A client that asks for one format only will call half the registry "without text".
for celex in 32026D1970 31985L0374 31968R5759; do
  for accept in "application/xhtml+xml" "text/html" "application/xml;type=fmx4"; do
    printf '%s | %-28s | ' "$celex" "$accept"
    curl -s -o /dev/null -L -w '%{http_code} %{content_type}\n' \
      -H "Accept: $accept" -H "Accept-Language: eng" \
      "http://publications.europa.eu/resource/celex/$celex"
  done
done
