# ADR-001: SQLite for the initial deployment

- Status: Accepted

## Context
The first goal is a reproducible single-machine portfolio project with low setup burden.

## Decision
Use SQLite with foreign keys, constraints, parameterized queries, short-lived connections, and transactions.

## Alternatives
PostgreSQL would offer stronger multi-client deployment characteristics but adds service setup and operational cost. An in-memory database would not preserve historical metrics.

## Consequences
Local demos are simple. Concurrent write throughput and shared deployment are limited. Revisit when measurements or availability requirements justify a server database.
