---
name: security-identity-access
description: Companion overlay for the local `security` workflow skill when the task centers on authentication, sessions, identity recovery, or tenant-scoped access boundaries. Use with `security` for session handling, verification and reset flows, MFA, invitation logic, callback-origin trust, and organization or tenant boundary enforcement.
---

# Security Identity Access

Use this companion overlay with `security` when the task involves auth stacks,
session systems, identity flows, invitation models, or multi-tenant
organization boundaries.

## Focus areas

- session creation, storage, refresh, invalidation, and revocation behavior
- password reset, email verification, recovery, and callback URL trust
- MFA enablement, verification, backup-code storage, and trusted-device flows
- invitation, membership, role, active-organization, and tenant-scoping logic
- origin checks, CSRF defenses, trusted origins, and cross-domain auth flows

## Not For

- generic user-model changes where auth or tenant boundaries are not the main risk
- routine login or signup implementation work with no security review or hardening goal
- generic RBAC discussions detached from actual session, identity, or tenant behavior

## Workflow

1. Map the auth surface:
   session transport, cookies or tokens, reset and verification endpoints, MFA
   state, invitation paths, active-org or tenant context, and privileged roles.
2. Identify trust assumptions:
   which origins are trusted, which callbacks are accepted, who can invite,
   promote, switch orgs, revoke sessions, or recover accounts.
3. Review boundary failures:
   account takeover paths, authz gaps, tenant-boundary leaks, stale-session
   risks, missing session revocation, insecure reset flows, and MFA bypasses.
4. Check secure defaults:
   absolute callback URLs or strict origin validation, bounded invitation
   lifetime, email verification where appropriate, session revocation on
   password reset, org or membership limits, and encrypted or hashed MFA
   recovery material when supported.
5. Report by boundary:
   state the impacted identity or tenant boundary, required attacker capability,
   and whether the issue leads to takeover, privilege escalation, or
   cross-tenant access.

## Review rules

- require explicit authorization on role changes, tenant switches, invitation
  acceptance, and privileged member-management actions
- inspect whether active-organization or tenant context is server-enforced, not
  only client-selected
- prefer short-lived, single-use recovery artifacts and invalidate older
  sessions after password reset when the platform supports it
- verify callback and redirect handling with absolute URLs or trusted-origin
  checks; do not trust inferred origins in split frontend/backend deployments
- treat MFA backup codes, OTP storage, and trusted-device markers as sensitive
  credentials

## False-positive guards

- do not flag a client-selected org or tenant switch if the server re-derives
  and enforces tenant scope on every sensitive action
- do not flag every redirect or callback as unsafe when the code enforces a
  strict allowlist or trusted-origin validation
- do not treat session persistence itself as a flaw when rotation, revocation,
  and transport protections match the deployment model
