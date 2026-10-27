# Project Summary — SysAtlas Omega

SysAtlas Omega is a local-first Linux observability and reliability portfolio project. It combines a C collector for aggregate `/proc` metrics with a Python FastAPI control plane, SQLite history, and basic memory-pressure incident evaluation.

## Demonstrable engineering topics

- Native compilation with strict warnings.
- Parsing kernel metrics and emitting versioned JSON.
- API input validation and consistent failure responses.
- Transactional persistence and schema constraints.
- Subprocess timeouts and protocol validation.
- Tests, CI configuration, container hardening, and architecture decision records.

## Limitations to disclose

Authentication, background scheduling, strict nested protocol validation, migration history extraction, retention, and production telemetry are incomplete. Do not describe the system as production-ready.
