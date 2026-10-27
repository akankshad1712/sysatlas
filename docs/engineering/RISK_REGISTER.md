# Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Unauthenticated API exposed beyond loopback | High if misconfigured | High | Loopback binding; implement auth before shared use |
| Malformed collector output breaks persistence | Medium | Medium | Strict schema validation and malformed-output tests |
| SQLite contention under concurrent writes | Medium at higher load | Medium | Measure; bounded transactions; consider PostgreSQL only with evidence |
| Database loss/corruption | Low to medium | High | Document backup/restore; automate and test before production |
| Stale data mistaken for current data | Medium | Medium | Show collection timestamps; add explicit stale status in API |
