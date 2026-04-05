---
name: project-release-maintainer
description: Overlay for release-facing docs, install layout, workflows, licenses, and hygiene scripts. Portable across repos with a release/packaging pipeline. Use for publication-facing changes.
---

# Project Release Maintainer

This is a composable overlay, not a standalone workflow.
Use alongside the repo's implementation skill for publication-facing and
packaging-sensitive changes.

## When to use

The change affects README, release checklists, install rules, shipped assets,
workflows, licenses, or other publication-facing artifacts.

## Not for

Internal code changes that don't affect the shipped surface (use the
implementation skill directly), vendored dependency work (use
**project-vendor-boundary**), or config/test work (use
**project-config-and-tests**).

## Rules

- keep README, release checklist, workflows, install rules, and shipped assets aligned
- validate temporary install trees when install behavior changes
- run hygiene checks on publication-facing changes
- keep docs small, accurate, and consistent with the shipped build
