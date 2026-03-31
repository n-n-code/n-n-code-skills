---
name: project-vendor-boundary
description: Generic overlay for app-owned versus vendored dependency boundaries.
---

# Project Vendor Boundary

Read `AGENTS.md` first. Use this skill when work touches vendored dependencies
or their integration boundary.

## Focus

- prefer app-side integration changes before editing vendored code
- treat vendored code as subtree/vendor content, not normal project code
- keep notices, provenance, and install rules aligned with vendor changes
- avoid unrelated churn inside vendor trees
