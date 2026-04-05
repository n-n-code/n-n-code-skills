---
name: project-platform-diagnose
description: Overlay for environment-sensitive diagnosis — service startup, install issues, platform integration, and runtime smoke checks. Portable across C++ projects.
---

# Project Platform Diagnose

This is a diagnostic overlay, not a standalone workflow.
Use alongside the repo's implementation skill when debugging environment-sensitive
issues.

## When to use

The problem involves build/install failures, runtime environment issues, platform
integration, or headless/container behavior.

## Not for

Logic bugs in repo-owned code (use the implementation skill directly), vendored
dependency issues (use **project-vendor-boundary**), or config behavior (use
**project-config-and-tests**).

## Rules

- separate build/install failures from runtime failures
- separate environment limits from app regressions
- prefer built-in diagnostics and reproducible smoke checks before guessing
- treat headless/container failures carefully when the feature expects a richer
  desktop or service environment
