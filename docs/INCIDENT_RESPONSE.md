# Incident Response

1. **Detect:** health check failure, missing snapshots, repeated collector errors, or database failures.
2. **Triage:** record UTC time, request ID, endpoint, error category, and deployment version. Do not copy credentials or sensitive host data into reports.
3. **Contain:** stop external traffic; this project is intended for local-only use until authentication is added.
4. **Recover:** restore known-good database backup if needed; verify schema version and readiness before resuming.
5. **Validate:** collect a fresh snapshot, inspect the result, and verify alert state.
6. **Review:** document timeline, root cause, contributing factors, remediation, and follow-up owners.
