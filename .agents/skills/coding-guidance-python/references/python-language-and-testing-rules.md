# Python Language And Testing Rules

Read this reference when a Python task materially changes typing, interfaces,
test structure, shared data, module boundaries, or architecture.

## Everyday design

- Prefer small functions and plain data flow before introducing classes.
- Use classes when they model stateful domain objects or a stable behavior
  boundary, not merely to group helpers.
- Prefer `pathlib.Path` over stringly typed path manipulation.
- Prefer `dataclass`, `TypedDict`, `Protocol`, `Enum`, and similar standard
  types when they make contracts clearer.
- Use comprehensions and built-ins when they expose intent; avoid dense
  one-liners that hide control flow.
- Avoid boolean flag parameters when separate functions or a small config type
  would make behavior clearer.
- Introduce no new warnings, lint findings, or type-checker regressions; report
  existing unrelated debt without turning a narrow change into a cleanup.

## Typing and interfaces

- Add type hints to public functions, methods, and non-trivial internal seams
  where they clarify real contracts.
- Prefer concrete types at boundaries and protocols for substitution seams over
  broad `Any`.
- Use `Any` only when the repository needs a dynamic escape hatch and the cost
  is explicit.
- Use union syntax and typing features supported by the repository's minimum
  Python version; prefer explicit narrowing over comments or sentinel-heavy
  conventions.
- Make invalid states hard to represent and expensive work visible to callers.
- When parameters form one concept or call sites cannot communicate their
  meaning, prefer a named type, config object, or split responsibility.
- Make mutation visible in names and interfaces.
- Follow configured type-checking strictness. Tighten a boundary when it catches
  a material defect; do not change module-wide policy solely because tooling
  supports a stricter mode or broadly suppress new errors.

## Tests and verification

- Follow the repository's test framework and style. Do not migrate `unittest`
  to pytest merely because new coverage is needed.
- For pytest-based tests, keep setup, action, and assertions easy to distinguish.
- Use fixtures for reusable setup and teardown, not to hide test meaning.
- Parameterize tests when cases share one contract and assertion path.
- Mock external boundaries rather than the internal behavior being proved.
- Add integration coverage when a change crosses package, transport,
  persistence, or subprocess boundaries.
- Treat coverage as a signal; prioritize meaningful path coverage over a
  percentage target.

## Data, modules, and architecture

- Keep validation, serialization, persistence, and business rules separated
  enough to test directly.
- Replace dict-shaped data that crosses many layers with a named contract.
- Prefer immutable or append-only flow when shared mutation would obscure
  behavior.
- Cache only from measured or repeated cost, with explicit scope and
  invalidation.
- Treat environment reads, current-directory assumptions, and process-global
  configuration as boundary concerns.
- Validate external input at its boundary.
- Prefer narrow modules with clear import direction over utility grab bags.
- Resolve circular imports through clearer lower-level contracts rather than
  habitual late imports.
- Keep CLI, transport, persistence, and domain logic independently testable.
- Expose package APIs deliberately; do not leak internal helpers, framework
  types, or persistence models accidentally.
- Prefer composition over inheritance unless inheritance matches the domain.
- Wait for repeated pressure before extracting registries, factories, or other
  indirection.
- Do not duplicate retry, timeout, or fallback behavior across layers.
- Do not hard-code secrets, production hosts, or environment-specific settings.
- Do not swallow exceptions, hide partial failures, or conceal destructive side
  effects behind benign names.

## Concurrency and resilience

- Keep sync and async entrypoints separate unless the repository has a clear
  bridge.
- Await real work promptly; do not create background tasks without ownership,
  cancellation, and error propagation.
- Protect invariants, not individual fields, when threads or async tasks share
  mutable state.
- Load the service-boundary reference when HTTP, queues, subprocesses, or
  persistent workers make observability, timeout, retry, or cancellation rules
  part of the contract.
