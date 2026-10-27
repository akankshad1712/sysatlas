# Reliability Review

Current protections: collector timeout, fixed executable invocation without a shell, SQLite busy timeout, transaction rollback, database constraints, health endpoints, and nonzero collector failures.

Gaps: no scheduler lifecycle, no global collection concurrency bound, no retries/backoff policy, no retention, no backup automation, and no end-to-end failure-injection suite. Retries should be added only with bounded attempts and idempotent persistence semantics.
