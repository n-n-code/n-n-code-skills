# Documentation Templates

Use these as starting points when the repo does not already provide a stronger
local format.

## README

```md
# Project Name

One-line purpose.

## Quick Start

[short runnable steps]

## Key Commands

| Command | Purpose |
|---------|---------|
| `...` | ... |

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `...` | ... | ... |
```

## ADR

```md
# ADR-001: Title

## Status
Accepted

## Context
[why a decision is needed]

## Decision
[what was chosen]

## Consequences
[trade-offs and follow-up]
```

## API Endpoint

```md
## GET /resource/:id

Short purpose.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | `string` | yes | Resource identifier |

### Responses

- `200`: success payload
- `404`: not found
```

## Public API Comment

```ts
/**
 * Brief purpose.
 *
 * @param input - Meaning of the input.
 * @returns Meaning of the result.
 * @throws ErrorName - When it fails.
 * @example
 * const value = fn("x")
 */
```

## Changelog Entry

```md
## [Unreleased]

### Added
- ...

### Changed
- ...

### Fixed
- ...
```
