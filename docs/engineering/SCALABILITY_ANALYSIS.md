# Scalability Analysis

- **One local instance:** FastAPI + SQLite is simple and reproducible; current target.
- **One shared team deployment:** add authentication, authorization, TLS termination, rate limits, backups, and retention first.
- **Multiple API instances:** SQLite on a shared filesystem is not the default answer; evaluate PostgreSQL after measuring concurrent writes and availability requirements.
- **High-volume fleet monitoring:** introduce a queue or remote agent protocol only after collecting real throughput, latency, and cardinality data.

No scale or throughput claim is made without a repeatable benchmark.
