---
name: project-config-and-tests
description: Generic overlay for config contracts, defaults, path helpers, and deterministic test coverage.
---

# Project Config And Tests

Read `AGENTS.md` first. Use this skill when the main task is config behavior or
small deterministic test coverage.

## Focus

- keep config parsing non-fatal where that preserves recovery/help paths
- keep defaults, example config, and docs aligned
- prefer deterministic tests around parsing, normalization, and helper seams
  using `frame_test.h` macros
- keep WHAT/HOW/WHY commentary current in repo-owned tests
- add benchmarks for performance-sensitive helpers using `frame_bench.h`
- use the `coverage` preset and target to verify test coverage for new code
