# Ops request — Fault Atlas (2026-09-09)

**What**: a read-only browsing site for a public dataset. No accounts, no writes, no database server.

1. DNS: `faultatlas.loxyn.ai` → the Scaleway host (Cloudflare, proxied, TLS).
2. One container: `datasette` serving `fault-atlas.sqlite` in read-only mode (`datasette serve fault-atlas.sqlite --immutable ... --host 0.0.0.0 --port 8001`), behind the existing reverse proxy.
3. The SQLite file is produced by `tools/build_sqlite.py` from the repository at each tagged release; deploy = copy the new file and restart the container. No secrets involved.
4. Nothing else. `answerkey.loxyn.ai` (the platform with accounts) is a later, separate request.

**Not before**: the repository is public and the two co-founders have agreed. Until then the container can run on a private hostname for review.


# Ops request 2 — public site + data explorer (2026-09-09, v0.1.2)

1. Build at each tagged release: `python3 tools/build_site.py` → `site/` (static HTML, ~1 MB) and `python3 tools/build_sqlite.py` → `fault-atlas.sqlite`.
2. `faultatlas.loxyn.ai/` serves `site/` as static files (Caddy `file_server`, cache a few minutes).
3. `faultatlas.loxyn.ai/data/*` reverse-proxies to Datasette, started as:
   `datasette fault-atlas.sqlite --immutable fault-atlas.sqlite --metadata datasette-metadata.json --setting base_url /data/ --cors`
   (`base_url /data/` is required so Datasette's own links work under the prefix). One SQLite file only; remove `fault-atlas_2`.
4. Keep `Access-Control-Allow-Origin: *` on `/data/` and on `/atlas.json`.
5. Remove `atlas-review.loxyn.ai`.
