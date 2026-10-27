# Security Review

See `docs/THREAT_MODEL.md` and `docs/SECURITY_ARCHITECTURE.md`. Highest-priority issue is missing authentication/authorization. Until resolved, bind to loopback only. SQL is parameterized, subprocess uses an argument array (no shell), output errors are generic to clients, and collector reads aggregate metrics rather than process command lines.
