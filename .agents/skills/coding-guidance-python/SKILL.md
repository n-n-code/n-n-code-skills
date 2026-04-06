---
name: coding-guidance-python
description: Python implementation and review skill. Use when writing, modifying, refactoring, or reviewing Python code, especially production Python that needs clear contracts, type safety, testability, and maintainable module boundaries. Portable across Python repos and tooling stacks.
---

# Python Coding Guidance

This skill adds portable Python implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable Python engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **backend-systems-guidance** (stronger backend architecture, reliability, and
  trust-boundary work),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific build/test commands)

Open the bundled references only when the task actually touches package
distribution, entrypoint layout, or a real I/O/service boundary.

## When Not to Lean on This Skill

- non-Python work
- notebook-first exploratory work where reproducibility and module design are
  not the main concern
- one-off throwaway scripts where the repo explicitly does not want production
  Python standards

## Implementation Workflow

1. Read the touched modules, entrypoints, tests, package metadata, and nearby
   docs before editing.
2. Infer intended behavior from existing code, imports, and tests when the
   request is only partially specified. Ask only when multiple plausible
   designs would change semantics.
3. Choose the narrowest change that keeps contracts, side effects, error
   handling, and public API shape explicit.
4. Implement with simple functions, clear module boundaries, explicit types
   where they improve the contract, and production-safe behavior at I/O
   boundaries.
5. Add or update tests close to the changed behavior; prefer pytest-native
   fixtures and parameterization over ad hoc setup.
6. Run the narrowest relevant formatter, linter, type checker, packaging check,
   and test targets the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, side effects, hidden globals, import shape, and
   mutation hotspots.
2. Break the refactor into small slices that preserve behavior.
3. Remove long functions, muddled responsibilities, implicit coupling, and
   anti-patterns one step at a time.
4. Keep tests passing after each slice; add characterization coverage first
   when behavior is unclear.
5. Stop when the code is simpler, more explicit, easier to test, and easier to
   operate.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize bugs and regressions, exception or error-path holes, mutable
   shared-state mistakes, typing and interface mismatches, packaging or import
   breakage, performance mistakes with real impact, security risks, and missing
   tests. Add service-boundary observability, retry, and timeout findings when
   the change actually crosses a real external boundary.
4. State findings with concrete evidence and the likely consequence.

## Python Rules

### First tier - causes bugs

- Keep module side effects minimal; avoid import-time network calls, filesystem
  mutation, or heavy initialization unless the module is explicitly an
  entrypoint
- Prefer explicit parameters and return values over hidden globals, ambient
  context, or mutation of module-level state
- Do not use mutable default arguments
- Treat `None` handling, optional fields, and missing keys as contract design,
  not cleanup for callers to guess
- Preserve exception context; do not catch broadly and discard the original
  failure without adding useful domain context
- Use context managers for files, locks, subprocess pipes, and other resources
  with lifetime rules
- Be explicit about text vs. bytes boundaries, timezone-aware vs. naive
  datetimes, and sync vs. async call paths
- Do not block the event loop with synchronous I/O in async code
- Do not mix sync and async APIs inside one path without a clear boundary

### Second tier - prevents mistakes

- Prefer small functions and plain data flow before introducing classes
- Use classes when they model stateful domain objects or a stable behavior
  boundary, not just to group helpers
- Prefer `pathlib.Path` over stringly typed path manipulation
- Prefer `dataclass`, `TypedDict`, `Protocol`, `Enum`, and other standard
  library types when they make contracts clearer
- Use comprehensions and built-ins when they make intent clearer; avoid dense
  one-liners that hide control flow
- Avoid boolean flag parameters when separate functions or a small config type
  would make behavior clearer
- Keep warnings, lint findings, and type-checker regressions at zero in
  repo-owned code

### Typing and interfaces

- Add type hints to public functions, methods, and non-trivial internal seams
  where they clarify real contracts
- Prefer concrete types at boundaries and protocols for substitution seams
  rather than broad `Any`
- Use `Any` only when the repo truly needs a dynamic escape hatch and the cost
  is explicit
- Prefer modern union syntax and type narrowing over comments or sentinel-heavy
  calling conventions
- Public APIs should make invalid states hard to represent and expensive work
  visible to callers
- If a function takes more than 2-3 meaningful parameters, prefer a named type,
  config object, or split responsibility
- Make mutation visible in names and interfaces; hidden in-place updates are a
  design smell
- Use strict type checking where the repo supports it; if the codebase is not
  yet strict, tighten changed modules instead of broadening exemptions

### Tests and verification

- Prefer pytest-style tests with clear arrange-act-assert flow
- Use fixtures for reusable setup and teardown, not for hiding the meaning of
  a test
- Use parameterized tests when the same contract should hold across multiple
  inputs
- Mock external boundaries, not the internal behavior you are trying to prove
- Add integration coverage when the change crosses package, transport,
  persistence, or subprocess boundaries
- Coverage is a signal, not a goal; prioritize meaningful path coverage over
  percentage chasing

### Data and state discipline

- Keep validation, serialization, persistence, and business rules separated
  enough that each can be tested directly
- Be suspicious of dict-shaped data flowing through many layers without a named
  contract
- Prefer immutable or append-only data flow where shared mutation would make
  behavior harder to reason about
- Cache only when measurement or repeated cost justifies it; make cache scope
  and invalidation rules explicit
- Treat environment-variable reads, current working directory assumptions, and
  process-global configuration as boundary concerns
- Validate external input at the boundary instead of letting malformed data fail
  deep in the call graph

### Modules, structure, and packaging

- Prefer narrow modules with clear import direction over utility grab bags
- Avoid circular imports by moving shared contracts to a lower layer instead of
  using late imports as a default escape hatch
- Keep CLI, transport, persistence, and domain logic separated enough to test
  each piece in isolation
- Prefer shallow directory structures unless there is a real sub-domain split
- Expose public package APIs deliberately; do not leak internal helpers,
  framework types, or persistence models as public contracts by accident
- Packaging-specific guidance that would otherwise bloat this file lives in
  [references/python-packaging-and-layout.md](references/python-packaging-and-layout.md)

### Architecture and anti-patterns

- Prefer composition over inheritance unless inheritance matches the real domain
  model
- Wait for repeated pressure before extracting abstractions; avoid clever
  registries, factories, or framework indirection that do not buy real clarity
- Keep I/O and business logic separated enough that core logic can be tested
  without transport or database setup
- Do not duplicate retry, timeout, or fallback behavior at multiple layers
- Do not hard-code secrets, production hosts, or environment-specific settings
- Do not swallow exceptions, ignore partial failures silently, or hide
  destructive side effects behind benign names

### Concurrency, observability, and resilience

- Keep sync and async entrypoints separate unless the repo already has a clear
  bridging pattern
- In async code, await real work promptly; do not create background tasks
  casually without ownership, cancellation, and error propagation rules
- Protect invariants, not individual fields, when threads or async tasks share
  mutable state
- Service-boundary concerns become first-class only when the task actually
  crosses a real external boundary such as HTTP, queues, subprocesses, or
  persistent workers
- Service-boundary observability and resilience guidance lives in
  [references/python-service-boundaries.md](references/python-service-boundaries.md)

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change touches more than 3 modules or public entrypoints,
  stop and plan before continuing; the change is bigger than it looks.
- **State visibility:** if mutation or side effects are hard to see from the
  function signature, redesign the interface or add a one-line contract comment.
- **Typing pressure:** if `Any`, untyped dicts, or loose tuples start spreading,
  introduce a clearer type boundary before adding more code.
- **Async boundary:** if a change crosses sync and async code, name the boundary
  explicitly and keep adaptation local.
- **Packaging pressure:** if the change affects imports, entrypoints, package
  layout, or published metadata, treat that as a compatibility boundary rather
  than a refactor detail.
- **I/O boundary pressure:** if an external boundary can fail, time out, retry,
  or degrade, make the ownership and diagnostics explicit; local helper code
  usually does not need the same instrumentation.
- **Repo conventions:** if the repo has established formatter, linter, typing,
  or framework conventions, follow them unless they create a correctness or
  maintainability problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or clarity, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.
- **Abstraction threshold:** three similar code blocks or repeated data-shaping
  pain is a pattern; before extracting, check whether a helper function, named
  type, or boundary cleanup is the simpler move.
- **Performance rule:** optimize only after measurement, except for obvious
  algorithmic, allocation, or I/O mistakes on hot paths.
- **Framework pressure:** if a framework convenience hides control flow, data
  ownership, or test seams, prefer the plainer construct.
- **Language-fit check:** if the problem is mostly shell orchestration, keep it
  in shell; if the problem needs rich data shaping, type-safe contracts, or
  non-trivial retry and observability logic, prefer Python over stretching shell
  too far.

## Validation

A change is done when:

- the code passes the repo's formatter or format-check
- lint and static analysis report no new findings
- type checking reports no new regressions where the repo uses type checking
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- changed CLI, import, or service entrypoints have a narrow smoke path
- packaging metadata and import paths are verified when the change affects a
  distributable library or CLI
- review findings at `Critical` and `Important` severity are addressed

## Examples

- `Refactor this Python service module without breaking its typed public API`
- `Review this async Python worker for retry, timeout, and test gaps`
