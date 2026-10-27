# ADR-002: Native C collector with Python control plane

- Status: Accepted

## Context
The project needs a focused systems-programming component and a maintainable API/control plane.

## Decision
Use C for `/proc` parsing and protocol output; use Python/FastAPI for HTTP, persistence, and alert policy.

## Alternatives
Python-only would reduce build complexity but remove the native systems component. A more complex multi-service design is unjustified at local scale.

## Consequences
The subprocess boundary isolates parser crashes but requires a strict protocol, timeout, and error handling. Add more components only when supported by evidence.
