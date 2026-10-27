# Contributing

1. Create a focused branch and describe the behavior being changed.
2. Add or update deterministic tests for success and failure paths.
3. Run `make test`; run `make sanitize` for collector changes where supported.
4. Keep stdout of the collector strictly machine-readable; diagnostics belong on stderr.
5. Avoid logging secrets or arbitrary high-cardinality values.
6. Document API or schema compatibility changes and add an ADR for consequential design changes.
7. Do not claim tests, scans, benchmarks, or hosted CI passed unless observed.
