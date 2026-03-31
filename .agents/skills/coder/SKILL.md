---
name: coder
description: Implementation skill for C++-first repos. Merges C++ engineering, code review discipline, optional backend layering guidance, and optional UI/frontend quality guidance.
---

# Coder

Read `AGENTS.md` first. This skill adds implementation guidance only.

## Default Stance

- C++/CMake/testing are the primary focus
- Preserve buildability, deterministic tests, and analyzer cleanliness
- Prefer small explicit abstractions, RAII, const-correctness, narrow types,
  and clear ownership boundaries
- Run the smallest validation set that proves the change, then extend as needed

## Core Workflow

1. Inspect the touched code, build shape, and tests.
2. Keep interfaces simple and behavior-oriented.
3. Implement the narrowest change that solves the problem.
4. Add or update tests close to the changed behavior using `frame_test.h`
   macros (`FRAME_TEST`, `FRAME_EXPECT_EQ`, `FRAME_EXPECT_TRUE`, etc.).
5. Run `format` before committing, then run relevant build/test/analyzer
   targets.

## C++ Rules

- Prefer rule-of-zero types and RAII over manual cleanup
- Treat raw pointers and references as non-owning unless ownership transfer is
  explicit
- Avoid `new`/`delete`, C-style casts, silent narrowing, and unchecked bounds
- Prefer standard library value types, `std::array`, and explicit helper
  structs over ambiguous adjacent parameters
- Keep warnings at zero in repo-owned code

## Review Mindset

When reviewing, prioritize findings over praise:

- bugs and regressions
- ownership/lifetime issues
- missing validation or error handling
- missing tests
- security or performance risks with real impact

Use severity ordering: `Critical`, `Important`, `Suggestion`.

## Optional Backend Guidance

If the repo contains networked or layered backend code:

- keep routing/transport thin
- keep business logic in services/core modules
- keep data access isolated
- validate external input early
- use dependency injection where it simplifies tests

## Optional UI/Frontend Guidance

If the repo includes UI work:

- preserve the existing design language unless asked to redesign
- prefer intentional visual direction over generic defaults
- make accessibility, layout stability, and responsive behavior part of done
- do not let styling work bypass tests/build hygiene
