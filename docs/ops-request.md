# Ops request — Fault Atlas (2026-09-09)

**What**: a read-only browsing site for a public dataset. No accounts, no writes, no database server.

1. DNS: `faultatlas.loxyn.ai` → the Scaleway host (Cloudflare, proxied, TLS).
2. One container: `datasette` serving `fault-atlas.sqlite` in read-only mode (`datasette serve fault-atlas.sqlite --immutable ... --host 0.0.0.0 --port 8001`), behind the existing reverse proxy.
3. The SQLite file is produced by `tools/build_sqlite.py` from the repository at each tagged release; deploy = copy the new file and restart the container. No secrets involved.
4. Nothing else. `answerkey.loxyn.ai` (the platform with accounts) is a later, separate request.

**Not before**: the repository is public and the two co-founders have agreed. Until then the container can run on a private hostname for review.
