---
name: project-config-and-tests
description: Overlay for config contracts, defaults, path helpers, and deterministic test coverage. Use alongside the repo's principle skill when the main task is config behavior or test coverage.
---

# Project Config And Tests

This is a composable overlay, not a standalone workflow.
Use alongside the repo's principle skill (e.g. **coding-guidance-cpp**) when the
main task is config behavior or test coverage.

## When to use

The task involves config parsing, defaults, path resolution, normalization, or
adding deterministic test coverage around these seams.

## Not for

General feature work (use **project-core-dev**), vendored dependency changes
(use **project-vendor-boundary**), or release/packaging work (use
**project-release-maintainer**).

## Rules

- keep config parsing non-fatal where that preserves recovery/help paths
- keep defaults, example config, and docs aligned
- prefer deterministic tests around parsing, normalization, and helper seams
  using the repo's test framework
- keep WHAT/HOW/WHY commentary current in repo-owned tests
- add benchmarks for performance-sensitive helpers using the repo's benchmark
  framework when available
- use the repo's coverage tooling to verify test coverage for new code
