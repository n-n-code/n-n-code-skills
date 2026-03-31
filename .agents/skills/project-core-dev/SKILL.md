---
name: project-core-dev
description: Generic core-dev overlay for repo-owned C++ code, tests, and top-level CMake changes.
---

# Project Core Dev

Read `AGENTS.md` first. Use this skill for normal feature work and bug fixes in
repo-owned C++ code.

## Focus

- preserve buildability, tests, docs, and analyzer cleanliness
- keep changes narrow and behavior-oriented
- prefer app-side fixes before widening platform or vendor boundaries

## Validation

- prefer `cmake --preset dev` for development builds
- run `ctest --output-on-failure` for covered changes
- run `cmake --build "$BUILD_DIR" --target format-check` before committing
- run `frame_cli --help` as a lightweight smoke test
- add docs/analyzer/Valgrind validation when the change surface justifies it
- run `cppcheck` target when available for additional static analysis
