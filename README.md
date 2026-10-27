# SysAtlas Omega

**Engineering Linux observability, reliability, diagnostics, and operational intelligence.**

SysAtlas Omega is a local-first portfolio project for demonstrating systems programming, backend engineering, data persistence, API contracts, reliability practices, and evidence-based delivery. It is not a claim of production readiness or professional senior/staff/principal experience.

## Implemented in this repository

- **Native C collector:** reads CPU counters, memory totals/availability, uptime, and load averages from Linux `/proc`; emits protocol-versioned JSON to stdout and diagnostics to stderr.
- **FastAPI control plane:** liveness/readiness, collection trigger, snapshot queries, alert-rule creation/listing, incident listing, diagnostics, request IDs, and safe generic internal errors.
- **SQLite persistence:** version table, constrained tables, indexes, short-lived connections, transactions, snapshots, rules, incidents, and audit events.
- **Alert evaluation:** memory-used percentage rules, deduplicated active incidents, resolution when pressure clears.
- **Quality tooling:** strict-warning C build, fixture-based collector tests, Python API tests, optional ASan/UBSan, Docker, Compose hardening, and GitHub Actions CI.
- **Engineering artifacts:** architecture, threat model, SRE/incident guidance, ADRs, technical debt, test matrix, and interview/portfolio material.

## Quick start (Linux/macOS/WSL)

Requirements: Python 3.11+, GCC or compatible C compiler, and pip.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make test
make run
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. In another terminal, trigger a collection:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/collect
curl http://127.0.0.1:8000/api/v1/snapshots/latest
```

Create a memory pressure rule:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/alert-rules \
  -H 'Content-Type: application/json' \
  -d '{"name":"high-memory-pressure","threshold":85}'
```

On non-Linux systems, the API starts but the native collector cannot read the expected Linux `/proc` layout. Run the collector on Linux or WSL for real host metrics.

## Docker

```bash
docker compose up --build
curl http://127.0.0.1:8000/health/ready
```

The Compose file binds only to loopback, drops Linux capabilities, uses a read-only root filesystem, and stores the database in a named volume. Review deployment assumptions before exposing the service to a network.

## Configuration

Copy `.env.example` to `.env` if desired and export the values in your shell. Settings can also be set directly as environment variables. The app intentionally has no built-in user authentication yet; do not expose it to untrusted networks.

## Architecture

- `collector/`: small C data-plane executable; stdout is a machine-readable contract.
- `app/`: API routes, collector adapter, SQLite repository functions, alert evaluation, and configuration.
- `migrations/`: migration policy and documented schema history (the initial migration is currently applied by `app/db.py`).
- `tests/` and `collector/tests/`: API and collector fixture tests.
- `docs/engineering/`: focused engineering reviews and architecture decisions.
- `portfolio/`: interview and portfolio material that avoids unverified impact claims.

## Engineering integrity

Run `make test` and `make sanitize` locally. Results depend on the local environment; CI results should be verified from the actual workflow run. Benchmarks and production SLO compliance are not claimed. See `docs/QUALITY_REPORT.md` for the initial validation record and limitations.
