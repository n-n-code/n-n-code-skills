# Sessions

Use this reference with `security-identity-access` for session, cookie, token,
refresh, logout, or revocation behavior. Use `security` for evidence, severity,
remediation, validation, and reporting.

Inspect the repository, deployment, framework, and identity provider before
applying these invariants. Verify version- or profile-dependent conclusions
against current official specifications and deployed official documentation.

Model the complete lifecycle:

```text
authentication event
  -> session issuance
  -> use and optional refresh or rotation
  -> expiry, logout, invalidation, or revocation
```

Check as applicable:

- A new authenticated session cannot inherit an attacker-chosen
  pre-authentication identifier or unrelated initiating context.
- Session secrets are unpredictable, protected in transport and client storage,
  and excluded from URLs, logs, analytics, and user-facing errors.
- Browser cookies use deployment-appropriate `Secure`, `HttpOnly`, `SameSite`,
  host, path, and lifetime scope. Cookie-authenticated state changes receive
  CSRF protection appropriate to the actual cross-site flow.
- Authentication, privilege elevation, impersonation, and other material
  context changes rotate or replace authority when retaining it would enable
  fixation or stale privilege.
- Idle and absolute lifetime, refresh behavior, concurrency, logout, and
  server-side invalidation have explicit semantics; client deletion alone does
  not revoke server authority.
- Account disablement, recovery, password or factor changes, membership or role
  changes, and suspected compromise have intentionally defined effects on
  sessions and refresh credentials.
- Refresh credentials remain bound as the deployed profile requires, including
  the intended client, authorization grant, resources, and authorization
  context. When rotation or sender constraining is used, handle replay, reuse,
  and partial rotation failure according to that profile; do not infer a flaw
  from reuse the profile permits.
- Sensitive actions use authoritative or sufficiently current account,
  assurance, grant or membership, and resource state for the product's stated
  revocation window.

Do not infer a vulnerability from stateless tokens, persistence, or a long
lifetime alone. Identify the event that requires invalidation, the resulting
stale-authority window, and whether the deployment explicitly accepts that
risk.
