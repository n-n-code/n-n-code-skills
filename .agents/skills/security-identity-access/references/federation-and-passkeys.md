# Federation, Account Linking, And Passkeys

Use this reference with `security-identity-access` for OAuth, OIDC, SAML, SSO,
external identities, account linking, passkeys, or WebAuthn. Use `security` for
evidence, severity, remediation, validation, and reporting.

## Source Policy

Before making a version-, profile-, provider-, or framework-specific claim:

1. Identify the protocol, participant role, flow or profile, library, and
   deployed version when repository evidence exposes them.
2. Consult the current official specification or best-current-practice document
   plus the provider or framework's official documentation.
3. Distinguish a normative protocol requirement from optional hardening or a
   product policy.
4. Record the source and applicable version or retrieval date when the finding
   depends on them.

Useful primary-source indexes include:

- [IETF OAuth working-group documents](https://datatracker.ietf.org/wg/oauth/documents/)
- [OpenID Foundation specifications](https://openid.net/developers/specs/)
- [OASIS SAML specifications](https://docs.oasis-open.org/security/saml/v2.0/)
- [W3C Web Authentication](https://www.w3.org/TR/webauthn/)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)

Prefer maintained protocol libraries over hand-built parsers or cryptographic
verification. Do not present an older review's algorithm, timeout, or assurance
profile as universally current.

## Redirect And Callback Trust

An absolute URI satisfies syntax, not trust. For redirect-based protocols,
verify from the applicable current specification that:

- the provider or authorization server is the configured trusted issuer;
- the redirect target matches the pre-registered target using the required
  comparison rule and only defined exceptions;
- neither participant exposes an open redirect that turns an allowed target
  into an arbitrary destination;
- when the flow has an initiating request, the response is bound to the
  initiating browser, client, issuer, redirect, and transaction; and
- artifacts whose protocol semantics require one-time use are accepted once by
  the intended recipient at the intended endpoint, while reusable tokens use
  the applicable scoping, expiration, revocation, and replay controls.

If a deployed federation profile permits unsolicited responses, require an
explicit policy for that flow plus issuer, destination, audience, time, and
replay validation rather than inventing a missing initiating transaction.

Do not derive a trusted callback from `Host`, forwarded headers, `Origin`, or a
return URL unless the deployment has an explicit validated proxy and origin
trust model. Keep provider-facing redirect URIs separate from application
post-login return destinations and validate each for its own purpose.

Use state, nonce, PKCE, issuer identification, response correlation, and code
binding for the distinct jobs assigned by the deployed protocol. Their mere
presence does not prove transaction integrity. For OAuth and OIDC, inspect
mix-up defenses, exact redirect matching, authorization-code injection,
audience restriction, and refresh-token replay behavior when those surfaces
exist.

## Tokens And Assertions

Anchor trust in configured issuers, clients, relying parties, metadata, and
keys. Do not select an issuer, verification key, algorithm, discovery endpoint,
or token endpoint solely from attacker-controlled token content.

Validate each artifact through the mechanism defined by the deployed flow,
such as signature or MAC verification, token introspection, a protected
backchannel, or an authoritative server-side lookup. Then validate the fields
that apply, including issuer, intended audience or client, authorized-party
semantics, time validity, nonce or response correlation, and recipient or
destination. Bind discovery and key retrieval to the trusted issuer and include
network-fetch and cache boundaries in the review.

For SAML or another signed-document protocol, establish exactly which element
was signed and consumed. Validate issuer, audience, recipient, time, applicable
request correlation, and signature placement with a maintained library; a
valid signature elsewhere does not authenticate the identity element in use.

## Account Linking

- Key an external identity by a protocol-defined stable subject within its
  issuer or security domain, not by display name or email alone.
- Make linking an explicit, transaction-bound action authorized by the account
  holder or another documented high-assurance process.
- If verified email participates in linking, establish provider trust,
  uniqueness and reassignment semantics, conflict handling, and
  account-pre-hijacking defenses. A provider's email-verification claim is not
  a universal account-merging rule.
- Apply equivalent care to unlinking and provider changes; protect the last
  recovery path, re-authenticate when appropriate, notify the owner, and
  invalidate stale linking transactions.
- Map upstream groups or roles to local grants through explicit policy. A valid
  provider identity does not establish local tenant authority.

## Passkeys And WebAuthn

Bind each registration and authentication ceremony to a fresh, single-use
server challenge and the expected relying-party context. Validate origin,
relying-party identifier, ceremony type, challenge, credential association,
signature, and the user-presence or user-verification result required by policy
and the current specification.

Treat registration, deletion, replacement, and recovery as factor lifecycle
transitions. Do not claim every passkey is device-bound or that every synced
credential has the same assurance. Interpret signature counters and attestation
under the authenticator model rather than as universal standalone findings.
