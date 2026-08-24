# Documentation Templates

Use these only when the repository or supplied project context does not provide
a stronger format. Copy only relevant sections, replace every placeholder, and
remove unused headings. These templates define shape, not facts; preserve native
markup and language conventions.

## README

```md
# Project Name

One-line purpose for the intended audience.

## Quick Start

[Prerequisites and the shortest safe steps to an observable result.]

## Common Tasks

| Task | Command | Notes |
|---|---|---|
| ... | `...` | ... |

## More Information

- [Add only relevant links that exist, such as configuration, contributing, or
  release guidance.]
```

## ADR

```md
# ADR-001: Title

## Status
[Proposed, accepted, superseded, or rejected.]

## Context
[Problem, constraints, and why a decision is needed.]

## Decision
[What was chosen.]

## Consequences
[Benefits, costs, risks, and follow-up.]
```

## API Endpoint

```md
## GET /resources/{id}

Short purpose.

**Authentication:** [scheme or none]

### Parameters

| Name | In | Type | Required | Constraints |
|---|---|---|---|---|
| `id` | path | `string` | yes | Resource identifier |

### Request

[Body, schema, and content type; remove when none.]

### Responses

| Status | Meaning | Body |
|---|---|---|
| `200` | Success | [response shape] |
| `404` | Resource not found | [error shape] |

### Example

[Small redacted request and response; remove when it adds no contract value.]
```

## TypeScript/JSDoc Example

Use the repository's native comment syntax and documentation generator. Describe
only useful contract information such as purpose, invariants, units, ownership
or lifetime, side effects, results, and failure conditions.

```ts
/**
 * Brief purpose.
 *
 * @param input - Meaning of a non-obvious input.
 * @returns Meaning of the result.
 * @throws ErrorName - When the caller needs to handle this failure.
 * @example
 * const value = fn("x")
 */
```

## Changelog Entry

Follow the repository's established changelog format. If an entry is breaking,
state the user-visible effect and upgrade action together; do not invent empty
categories.

```md
## [Unreleased]

### Added

- ...

### Changed

- ...

### Fixed

- ...
```
