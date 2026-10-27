# Interview Questions and Defensible Answers

**Why C for collection?** It demonstrates systems-level parsing and low-level resource discipline; the collector is intentionally narrow. The Python control plane keeps HTTP and persistence logic easier to test.

**Why SQLite?** It minimizes setup for a local portfolio demo. For multiple writers or high availability, measure contention and migrate to PostgreSQL with explicit migration/recovery tests.

**How is CPU utilization calculated?** It is not yet calculated. `/proc/stat` counters are cumulative; utilization requires two samples and a delta calculation, with handling for resets and zero deltas.

**What are the main security gaps?** Authentication and authorization are absent. The service must remain loopback-only until those controls and rate limiting are implemented.

**What reliability controls exist?** Collector timeout, nonzero exit handling, SQLite transactions, busy timeout, constraints, and health endpoints. Scheduler recovery and automated backup/restore remain gaps.

**What performance improvements were measured?** None. The project includes a benchmark plan but does not claim measured performance gains.

**What would you change for multiple instances?** Evaluate database contention and service availability requirements first; move to PostgreSQL only when justified, then add auth, TLS, backups, and operational monitoring.
