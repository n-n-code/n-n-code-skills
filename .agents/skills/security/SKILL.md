---
name: security
description: Security workflow skill for repo-grounded threat modeling, exploit-focused security review, and secure-by-default implementation guidance. Use when the user explicitly asks for security work, or when security properties are the primary concern in a high-risk change. Do not trigger for ordinary code review, routine endpoint work, or general backend implementation just because a repo contains APIs, auth, or secrets.
---

# Security

This skill adds security-specific guidance.

## Default Stance

- prioritize realistic attacker goals, attacker-controlled input, and concrete impact
- ground claims in actual code, entrypoints, data flows, trust boundaries, and deployment shape
- research the broader repo before reporting a vulnerability; do not flag pattern matches in isolation
- report high-confidence exploit paths first and separate them from lower-confidence follow-up checks
- prefer secure defaults that do not silently break intended behavior; call out meaningful tradeoffs
- separate runtime risk from CI/build/dev/test-only concerns

## Use This Skill For

- security reviews, vulnerability audits, OWASP-style review requests, and secure-by-default coding help
- high-risk changes where the main question is whether a boundary is secure: authz, untrusted input, external fetches, uploads, secrets handling, sensitive data, or tenant isolation
- threat modeling a repo, service, or path

## Not For

- ordinary code review with no security angle
- routine endpoint work where security is not the main task or risk
- generic checklist dumping without repo evidence
- reporting hypothetical findings when exploitability is unclear

For auth-heavy systems, load this skill with `security-identity-access`.

## Workflow

### 1. Scope the job

Identify which mode applies:

- `security review`: find concrete vulnerabilities in code or changes
- `threat model`: map assets, boundaries, abuse paths, and mitigations
- `secure implementation`: write or revise code with secure defaults while preserving intended behavior

Clarify in-scope paths, runtime surfaces, and any known deployment or auth assumptions. If material context is missing for a threat model, ask a small number of targeted questions before finalizing.

### 2. Build the system view

1. Identify languages, frameworks, entrypoints, external integrations, and storage layers.
2. Distinguish runtime behavior from tests, examples, and build tooling.
3. Enumerate concrete trust boundaries, assets, attacker goals, and attacker capabilities.
4. For web apps, inspect both frontend and backend surfaces.

### 3. Investigate before reporting

For each suspected issue:

- trace whether the input is attacker-controlled or operator-controlled
- check framework protections, middleware, schema validation, sanitization, and parameterization already in place
- confirm whether the code path is reachable and whether auth or environment assumptions materially reduce impact

Do not report a finding based only on a risky-looking API. Confirm exploitability first.

### 4. Review the highest-value risk areas

Prioritize these categories as applicable:

- authn/authz gaps, IDOR, privilege escalation, tenant-boundary failures
- injection: SQL, NoSQL, command, template, deserialization, path traversal
- XSS, CSRF, unsafe HTML rendering, unsafe redirects
- SSRF and unsafe external requests
- secrets exposure, weak crypto, insecure token/session handling, sensitive-data logging
- uploads, parsers, decoder surfaces, and denial-of-service pressure points
- misconfiguration with real security impact: unsafe defaults, debug exposure, dangerous CORS, missing isolation

Treat framework-safe defaults as safe unless repo evidence shows they were bypassed. Example: ORM parameterization, templating auto-escaping, and config-derived URLs are not findings by themselves.

### 5. Apply secure-by-default implementation rules

When writing or fixing code:

- validate untrusted input with explicit schemas or strict allowlists
- use parameterized queries and typed APIs instead of string-built commands or queries
- store secrets in environment or secret-management systems, never in source
- keep auth tokens in safer storage mechanisms for the deployment model; avoid browser-accessible storage for session secrets when httpOnly cookies fit the design
- redact secrets and sensitive fields from logs and user-facing errors
- add rate limits, size bounds, and fail-closed validation on expensive or dangerous operations
- preserve functionality intentionally; if a fix changes behavior, state the tradeoff before or while making the change

## Threat-Model Workflow

1. Identify components, entrypoints, trust boundaries, assets, and attacker goals.
2. Separate runtime behavior from build/test/dev tooling.
3. Enumerate a small set of high-quality abuse paths.
4. Rank findings by likelihood and impact with explicit assumptions.
5. Recommend mitigations tied to concrete boundaries or components.
6. If key context is missing, summarize the assumptions that drive ranking and ask the user to confirm or correct them before finalizing.

## Secure-Review Workflow

When reviewing code for security:

- look for auth/authz gaps, unsafe parsing, command execution, path traversal,
  injection, secrets exposure, weak validation, and denial-of-service risks
- verify whether attacker-controlled input actually reaches the sink
- distinguish exploitable issues from "needs verification" follow-ups
- note where types/contracts could make misuse harder
- distinguish critical findings from hygiene improvements

## Reporting Rules

- findings first, ordered by severity
- include concrete file references and impacted asset/boundary
- for reviews, default to reporting only high-confidence vulnerabilities; keep lower-confidence items clearly labeled or omit them
- for threat models, keep the threat set small, explicit, and tied to concrete assets and boundaries
- make assumptions explicit
- avoid generic checklist noise when the repo evidence does not support it
- if the user asked for a report file, write concise Markdown with line references and a short executive summary
