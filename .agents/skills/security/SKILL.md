---
name: security
description: Security skill for threat modeling, secure defaults, and security-focused code review in generic software projects.
---

# Security

Read `AGENTS.md` first. This skill adds security-specific guidance.

## Default Stance

- prioritize realistic attacker goals and concrete impact
- ground claims in actual code, entrypoints, data flows, and deployment shape
- prefer secure defaults that do not silently break intended behavior

## Threat-Model Workflow

1. Identify components, entrypoints, trust boundaries, assets, and attacker goals.
2. Separate runtime behavior from build/test/dev tooling.
3. Enumerate a small set of high-quality abuse paths.
4. Rank findings by likelihood and impact with explicit assumptions.
5. Recommend mitigations tied to concrete boundaries or components.

## Secure-Review Workflow

When reviewing code for security:

- look for auth/authz gaps, unsafe parsing, command execution, path traversal,
  injection, secrets exposure, weak validation, and denial-of-service risks
- note where types/contracts could make misuse harder
- distinguish critical findings from hygiene improvements

## Reporting Rules

- findings first, ordered by severity
- include concrete file references and impacted asset/boundary
- make assumptions explicit
- avoid generic checklist noise when the repo evidence does not support it
