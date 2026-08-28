# Recovery, Invitations, And Factor Lifecycle

Use this reference with `security-identity-access` for verification, recovery,
invitations, enrollment, replacement, backup-code, MFA, or trusted-device
flows. Use `security` for evidence, severity, remediation, validation, and
reporting.

Treat verification links, reset tokens, recovery codes, invitation tokens, and
factor-binding codes as purpose-bound capabilities. Model trusted-device
credentials as scoped persistent credentials with explicit expiry and
revocation semantics rather than assuming they are single-use.

```text
accepted capability =
  expected purpose and intended subject
  and applicable initiating transaction, tenant, and client binding
  and unexpired and, when one-time, unused
```

- Generate capabilities with a cryptographically appropriate random source and
  sufficient unpredictability; bind, expire, and rate-limit them, and consume
  one-time capabilities atomically. Define what reissuance does to older copies.
- Keep capability values out of logs, referrers, analytics, support tooling, and
  unintended recipients. Avoid account enumeration while ensuring attempt
  controls do not create a trivial lockout denial of service.
- Construct recovery destinations from trusted server-side configuration or a
  strict canonical allowlist. An absolute URL or request `Host` value is not a
  trust decision.
- Make recovery preserve the intended authentication strength, notify the
  legitimate user through an independent channel when appropriate, and define
  its effect on existing sessions and authenticators.
- Bind invitations to the intended tenant, permitted role, state, and verified
  recipient rule. Recheck inviter authority and tenant policy at acceptance;
  issuance-time authority may be stale.
- Treat ordinary factor enrollment, replacement, removal, and trusted-device
  changes as privileged transitions. Require recent or step-up authentication
  appropriate to impact and preserve a safe path when removing the last usable
  authenticator.
- When ordinary authenticators are unavailable, require the documented recovery
  proof and compensating controls instead of impossible reauthentication. Bound
  the recovery session, prevent it from silently weakening stronger factors,
  and apply appropriate delay, notification, audit, and session invalidation.

Protect stored material according to verifier semantics:

| Material | Protection invariant |
|---|---|
| password | Store a maintained one-way password verifier; never recover plaintext |
| backup or recovery code | Store an independent one-way verifier; make it single-use and revocable; do not redisplay plaintext |
| OTP seed | Protect as a high-value reversible secret with encryption, key separation, restricted access, and revocation; hashing alone cannot support ordinary verification |
| WebAuthn credential | Store the credential identifier, public key, and required metadata; the relying party does not receive the credential private key |
| opaque reset, invitation, session, or trusted-device token | Scope and expire it; store a one-way server verifier where the design permits |
| transient OTP or confirmation output | Minimize retention, bind it to the transaction, limit attempts, expire it, and reject replay |

Two screens, two codes, or two steps are not necessarily independent factors.
Determine which authenticators were actually proven and whether recovery,
remembered-device, or factor-change routes bypass policy.

Verify version-, framework-, and authenticator-specific conclusions against
current official specifications and deployed official documentation. Do not
import an assurance level, timeout, or algorithm merely because another system
uses it.
