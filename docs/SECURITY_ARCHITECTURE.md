# Security Architecture

The app uses Pydantic request validation, SQL parameter binding, a fixed collector executable path, subprocess timeout, generic internal error responses, foreign-key constraints, and a Compose profile with a non-root user, dropped capabilities, read-only root filesystem, and loopback port binding.

Important missing control: application authentication/authorization. This means the service is not safe for untrusted networks. HTTPS, rate limiting, dependency scanning, token/session lifecycle, and production secret management remain deployment prerequisites, not implemented features.
