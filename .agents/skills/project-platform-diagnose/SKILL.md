---
name: project-platform-diagnose
description: Generic overlay for environment-sensitive diagnosis such as service startup, install issues, platform integration, and runtime smoke checks.
---

# Project Platform Diagnose

Read `AGENTS.md` first. Use this skill for environment-sensitive debugging.

## Focus

- separate build/install failures from runtime failures
- separate environment limits from app regressions
- prefer built-in diagnostics and reproducible smoke checks before guessing
- treat headless/container failures carefully when the feature expects a richer
  desktop or service environment
