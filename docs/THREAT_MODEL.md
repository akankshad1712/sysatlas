# Threat Model

## Assets

Collected host-level resource metrics, database integrity, API availability, and operational logs.

## Trust boundaries

- HTTP clients to FastAPI: currently no authentication; this is the primary risk boundary.
- API process to collector subprocess: bounded runtime and fixed executable path, but collector output still requires strict schema validation.
- API process to SQLite: local file permissions and transactions protect integrity; host filesystem access remains in scope.

## Abuse cases

| Abuse case | Current mitigation | Residual risk |
|---|---|---|
| Untrusted user creates alert rules | Request validation and database constraints | No authentication; network exposure is unsafe |
| Client floods collection endpoint | Per-call subprocess timeout | No rate limiting or global concurrency queue |
| Collector emits invalid output | JSON parse and top-level protocol checks | Nested fields are not fully validated |
| Database lock contention | SQLite busy timeout and short transactions | Sustained write load can still fail |
| Sensitive data leaked in logs | Collector avoids process command lines/environments; generic API error body | Access logs include paths and application logs need deployment review |

## Deployment boundary

Keep bound to loopback. Do not expose publicly until authentication, authorization, rate limiting, dependency scanning, and deployment review are implemented and tested.
