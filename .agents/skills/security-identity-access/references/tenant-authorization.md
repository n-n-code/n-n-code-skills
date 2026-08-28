# Tenant Authorization

Use this reference with `security-identity-access` for membership, role,
organization switching, resource scope, or cross-tenant paths. Use `security`
for evidence, severity, remediation, validation, and reporting.

Express the sensitive decision in repository terms. A useful default is:

```text
allow =
  principal and applicable grant or membership state are authoritative or
  sufficiently current for the accepted revocation window
  and target action/resource is within server-authorized tenant/resource scope
  and applicable policy permits it
```

A requested tenant, active-organization cookie, route parameter, token claim,
or globally unique resource identifier may locate candidate state. It does not
prove authority.

Preserve the invariant across the complete operation:

- At entry, authenticate the actor and resolve effective tenant and applicable
  grant or membership from trusted server-side state.
- At data access, constrain reads, writes, aggregates, existence checks, fields,
  and related-object traversal to the authorized scope.
- At mutation, recheck sensitive authority close enough to the state change to
  prevent stale-role and time-of-check/time-of-use bypasses.
- At side-effect boundaries, carry explicit actor and tenant scope into jobs,
  queues, exports, object storage, caches, subscriptions, and service calls.
- At response, avoid cross-tenant disclosure through data, counts, identifiers,
  errors, timing where material, or cached results.

Centralized mandatory middleware, policy engines, tenant-scoped repositories,
or database controls can satisfy these rules. Do not demand duplicate endpoint
checks when the lower layer demonstrably cannot be bypassed.

For role, invitation, and membership changes, verify both the target grant and
the actor's delegation authority. Prevent self-promotion, grants beyond the
actor's authority, stale invitation acceptance, and unacceptable revocation
latency in sessions or authorization caches. Treat support users,
impersonation, service accounts, API keys, and background workers as explicit
principals with bounded tenant and action scope.

Use focused negative cases across same-tenant versus cross-tenant resources,
lower versus higher roles, active versus revoked membership, field-level
access, alternate entrypoints, and asynchronous side effects. A passing happy
path does not validate isolation.

Verify version-, framework-, and storage-specific conclusions against current
official documentation and the effective deployment. Do not infer a flaw from
client-carried tenant selection when every sensitive server path re-derives and
enforces the accepted scope.
