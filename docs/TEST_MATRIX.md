# Test Matrix

| ID | Requirement | Procedure | Expected outcome | Actual outcome |
|---|---|---|---|---|
| C-001 | Parse valid fixture procfs files | `make test-c` | JSON includes protocol version and fixture metrics | PASS |
| C-002 | Missing procfs input fails safely | `collector/tests/test_collector.sh` | Nonzero exit; diagnostic on stderr | PASS |
| C-003 | Real host `/proc` can be read | `./build/sysatlas-collector` on Linux | Valid JSON with required metric groups | PASS |
| C-004 | Sanitizer build and fixture tests | `make sanitize` | Build and fixture tests complete | PASS |
| API-001 | Liveness endpoint | `GET /health/live` | 200 and `status=ok` | PASS |
| API-002 | Readiness endpoint | `GET /health/ready` | 200 when SQLite works | PASS |
| API-003 | Alert threshold validation | POST threshold >100 | 422 validation response | PASS |
| API-004 | Duplicate rule rejected | POST same name twice | Second request returns 409 | PASS |
| API-005 | Collection persistence round trip | `POST /api/v1/collect`, then latest snapshot | Snapshot saved and retrievable | PASS |
| OPS-001 | Docker hardening | `docker compose up --build` | Image builds and health check passes | UNVERIFIED; Docker unavailable |
| CI-001 | Hosted workflow | Inspect actual hosted run | Actual checks visible in CI | UNVERIFIED; no run observed |
