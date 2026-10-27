# Security Policy

## Supported scope

This is an educational, local-first portfolio project. Security reports are welcome as issues or private maintainer contact when a repository maintainer has been configured.

## Current deployment warnings

- Authentication and authorization are not implemented. Do not expose the API to untrusted networks.
- Use loopback binding for local demos. Place an authenticated reverse proxy in front before any shared deployment.
- The collector reads host `/proc`; it does not read process command lines or environments.
- Dependencies should be updated and scanned before deployment.
- Do not place secrets in issue reports, logs, or `.env` files committed to version control.

## Reporting

Provide affected version, impact, minimal reproduction, and any suggested mitigation. Avoid sharing real credentials or sensitive host data.
