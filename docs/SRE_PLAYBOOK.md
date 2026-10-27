# SRE Playbook

## Health checks

- `GET /health/live`: process liveness.
- `GET /health/ready`: SQLite connectivity.
- `GET /api/v1/diagnostics`: latest snapshot timestamp and collector configuration.

## Triage

1. Check liveness and readiness.
2. Inspect application logs for `collector_failed`, SQLite errors, or malformed protocol output.
3. Run the collector manually and confirm stdout is valid JSON.
4. Verify database path permissions and free disk space.
5. Preserve the database before attempting recovery.

## Reliability targets (proposed, not measured)

Candidate indicators are successful collection rate, snapshot freshness, API availability, and p95 API latency. No SLO compliance is claimed until instrumentation, an observation window, and a reproducible load test exist.
