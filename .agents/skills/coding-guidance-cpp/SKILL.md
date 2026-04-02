---
name: coding-guidance-cpp
description: C++ implementation and review skill. Use when writing, modifying, or reviewing C++ code — feature work, bug fixes, refactors, or code review. Portable across C++ repos and build systems.
---

# C++ Coding Guidance

Read `AGENTS.md` first. This skill adds C++ implementation and review guidance.

## Adjacent Skills

This skill provides portable C++ engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific build/test commands)

## Implementation Workflow

1. Read the touched code, build shape, and existing tests.
2. Identify the narrowest change that solves the problem.
3. Implement with simple, behavior-oriented interfaces.
4. Add or update tests using the repo's established test framework, close to the
   changed behavior.
5. Run the repo's formatter, then run relevant build, test, and analyzer targets.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` > `Suggestion`.
3. Prioritize: bugs and regressions, ownership/lifetime issues, missing
   validation or error handling, missing tests, security or performance risks
   with real impact.
4. Report findings first. Skip praise unless the change is notably well-done.

## C++ Rules

### First tier — causes bugs

- Treat raw pointers and references as non-owning; make ownership transfer
  explicit in the type or documented in a comment
- Avoid `new`/`delete` — use RAII wrappers and smart pointers
- Prefer `std::unique_ptr` by default when single ownership is intended; use
  `std::shared_ptr` only when shared lifetime is a real requirement
- Avoid unchecked bounds access — prefer `.at()`, range-for, or
  iterator patterns over raw indexing when bounds are uncertain
- Avoid silent narrowing conversions — use explicit casts or `narrow_cast`

### Second tier — prevents mistakes

- Avoid C-style casts — use `static_cast`, `const_cast`, `reinterpret_cast`
  to make intent visible
- Prefer rule-of-zero types; if you write a destructor, justify it
- Prefer `std::array` over C arrays, `std::string_view` and, where available,
  `std::span` over raw pointer-plus-length pairs when lifetime rules are clear
- Prefer explicit helper structs over ambiguous adjacent parameters of the
  same type
- Use `[[nodiscard]]` on functions where ignoring the return value is a bug
- Avoid unnecessary copies in range-for — use `const auto&` by default, but
  prefer value iteration for cheap copy types or when ownership transfer is the
  point
- Keep warnings at zero in repo-owned code

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change touches more than 3 public interfaces, stop and
  plan before continuing — the change is bigger than it looks.
- **Ownership clarity:** if resource ownership is not obvious from the type
  signature alone, add a one-line comment documenting the contract.
- **Repo conventions:** if the repo has established rules for exceptions,
  ownership types, containers, or error handling, follow them unless they cause
  a correctness or safety problem.
- **Test setup size:** if test setup exceeds ~20 lines, extract a fixture — but
  only if the setup is reused by at least 2 tests.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style, prefer narrowness unless
  explicitly time-boxed for cleanup.
- **Refactor boundary:** when modifying a file, fix at most one small adjacent
  issue. Do not refactor unrelated code in the same change.
- **Abstraction threshold:** three similar code blocks is a pattern; two is
  coincidence. Do not extract a helper until the third occurrence unless the
  duplication crosses a module boundary.

## Validation

A change is done when:

- the code compiles without new warnings, unless the repo explicitly treats a
  known warning set as baseline debt outside the change
- existing tests pass
- new or changed behavior has test coverage
- the repo's formatter has been run
- static analyzers (if configured) report no new findings
- review findings at `Critical` and `Important` severity are addressed
