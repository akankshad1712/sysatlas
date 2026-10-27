# Technical Debt and Known Limitations

- No authentication, authorization, or rate limiting.
- Collection is triggered manually over the API; no background scheduler or overlap/backpressure policy exists.
- CPU counters are collected, but CPU utilization deltas are not calculated.
- Alerting currently supports memory-used percentage and does not expose acknowledgement, rule update/disable, or notification delivery.
- Protocol validation checks top-level keys but does not validate every nested value with a strict schema.
- Initial schema is created by application code; migration files and migration rollback tests should be added before schema evolution.
- No retention cleanup, backup automation, or restore test is implemented.
- No measured benchmark, production SLO, coverage percentage, or deployment claim is made.
- Docker and hosted CI must be validated in an environment that supports them.
