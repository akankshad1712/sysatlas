# Architecture Evolution

1. **Local instance:** one API process, C collector subprocess, SQLite file.
2. **Team deployment:** add authn/authz, TLS, throttling, retention, backups, and operational ownership.
3. **Multiple instances:** move persistence to PostgreSQL only if concurrent write and availability requirements justify it; use migrations and test rollback/recovery.
4. **Fleet monitoring:** assess agent identity, transport security, queueing, tenant isolation, cardinality, and retention from measured workloads. Avoid adding Kafka/Kubernetes/Redis until a concrete bottleneck or operational requirement warrants the cost.
