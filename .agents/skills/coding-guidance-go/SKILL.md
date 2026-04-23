---
name: coding-guidance-go
description: Go implementation and review skill. Use when writing, modifying, refactoring, testing, optimizing, or reviewing Go code, especially production Go that needs clear errors, context propagation, concurrency safety, interface discipline, package boundaries, REST or gRPC service boundaries, standard-library testing, pprof-backed performance work, logging, and tooling discipline. Portable across Go repos and service stacks.
---

# Go Coding Guidance

Portable Go implementation, refactoring, testing, optimization, and review
guidance.

## Adjacent Skills

Compose with:

- **Workflow:** `thinking` for planning, `recursive-thinking` for
  stress-testing, `security` for threat modeling
- **Domain overlays:** `backend-guidance` for server-side code,
  `backend-systems-guidance` for deeper backend architecture/reliability/trust
  boundaries, `project-core-dev` for repo validation, and
  `project-config-and-tests` for config contracts and deterministic tests
- **Testing:** `go-testing-with-testify` when the main artifact is testify-based
  Go test code, test review, or Go test flake triage

## When Not to Lean on This Skill

- non-Go work
- pure test strategy without implementation code or concrete Go test code; use
  `tester-mindset`
- testify-specific assertion, mock, suite, or flake work; use
  `go-testing-with-testify`
- security as the primary job; use `security` and compose this skill only for
  Go-specific implementation details
- repo-specific framework rules that should live in local docs, generated-code
  policy, linter config, or domain overlays

## Reference Map

Load references only when the task needs that depth:

- [go-concurrency-and-services.md](references/go-concurrency-and-services.md)
  for context, goroutine ownership, shared state, pipelines, backpressure,
  logging, REST/gRPC/CLI/worker boundaries, and transport error mapping
- [go-testing-and-validation.md](references/go-testing-and-validation.md) for
  standard Go tests, comparison choices, helpers, fuzzing, benchmarks, race
  checks, integration-test gating, and validation command selection
- [go-performance-and-modules.md](references/go-performance-and-modules.md)
  for package/module layout, `go.mod`/`go.sum`, `go.work`, vendoring,
  generated code, release metadata, dependency pressure, profiling, and hot-path
  allocation guidance

## Mode Selection

Use the narrowest mode that fits the task:

- **Routine edit:** follow the implementation workflow, then apply only relevant
  rule sections and validation commands.
- **Review:** use the review workflow first; consult references only to verify
  concrete findings.
- **Refactor:** use the refactoring workflow and preserve exported contracts
  unless the task explicitly changes them.
- **Concurrency:** load the concurrency/service reference and focus on context
  ownership, goroutine lifecycle, shared state, backpressure, race validation,
  and shutdown.
- **Service boundary:** use this skill for Go-specific context, error,
  transport, and handler mechanics; add `backend-guidance` or
  `backend-systems-guidance` for architecture, repositories, transactions,
  queues, or cross-service design.
- **Performance:** load the performance/modules reference and require benchmark,
  `pprof`, trace, or allocation evidence before performance-driven rewrites.

## Implementation Workflow

1. Read touched packages, call sites, tests, `go.mod`, `go.sum`, build tags,
   generated or vendored boundaries, and nearby docs before editing.
2. Identify the module Go version, formatter/import tool, linter/test commands,
   service boundary style such as REST, gRPC, CLI, or worker, and existing
   assertion, logging, DI, config, or framework conventions.
3. Infer intended behavior from existing code and tests when the request is
   partially specified. Ask only when multiple plausible Go designs would
   change semantics.
4. Choose the narrowest change that keeps package boundaries, error contracts,
   context ownership, resource lifetime, and concurrency behavior explicit.
5. Implement with small packages, simple functions, explicit dependencies,
   idiomatic error handling, useful zero values, externalized configuration,
   and goroutine ownership that can be tested.
6. Keep generated code, vendored code, API schemas, module paths, public JSON
   tags, CLI flags, and exported identifiers stable unless the task explicitly
   changes that contract.
7. Add or update tests close to the changed behavior. Prefer table-driven tests
   only when cases share the same setup and assertion path.
8. Run the narrowest relevant `gofmt`, `goimports`, `go test`, `go vet`, race,
   lint, module, benchmark, profile, and security commands the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, exported API shape, package dependencies, error
   values, context flow, goroutine ownership, shared state, and import graph.
2. Add characterization tests first when behavior is unclear or risk is high.
3. Break the refactor into small slices that preserve behavior and compile
   after each slice.
4. Remove circular dependencies, vague packages, hidden globals, duplicated
   error handling, and unclear interface seams one step at a time.
5. Keep tests passing after each slice and avoid changing public contracts as an
   incidental cleanup.
6. Stop when package responsibilities, call sites, and failure behavior are
   clearer without making abstractions larger than the code they protect.

## Review Workflow

When reviewing, skip the implementation workflow and use this instead:

1. Read the change in full before commenting.
2. Check mechanical issues first: formatting, imports, generated-code drift,
   module changes, build tags, and obvious compile/test breakage.
3. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
4. Prioritize bugs and regressions, data races, goroutine leaks, context misuse,
   resource leaks, error wrapping or sentinel mismatches, nil pointer or nil map
   hazards, interface overreach, package-cycle pressure, security risks,
   performance mistakes with real impact, and missing tests.
5. Do not spend review budget on nits that `gofmt`, `goimports`, or the repo's
   linter will settle unless they hide a real readability or behavior issue.
6. State findings with concrete evidence and the likely consequence.

## Core Go Rules

- Always run `gofmt`; run `goimports` when imports changed or the repo uses it.
- Handle every error deliberately. Do not discard errors with `_` unless the
  call cannot fail meaningfully or a comment explains why it is safe to ignore.
- Return the `error` interface from exported functions, not concrete error
  pointer types that can become non-nil interfaces.
- Wrap errors with context callers do not already have. Preserve
  machine-checkable causes with `%w` when callers should use `errors.Is` or
  `errors.As`; avoid leaking internals across process, API, or trust
  boundaries.
- Propagate `context.Context` as the first parameter through request-scoped
  blocking work. Do not store contexts in structs or use them for optional
  parameters.
- Always call cancel functions returned by `context.WithCancel`,
  `WithTimeout`, or `WithDeadline` when the current scope owns them.
- Close response bodies, files, rows, tickers, timers, and other resources on
  every path. Check close errors when the close operation can affect persisted
  data.
- Do not launch goroutines without a clear owner, cancellation path, error
  propagation path, and testable shutdown behavior.
- Protect shared mutable state with a clear synchronization rule. Do not copy
  values containing `sync.Mutex`, `sync.WaitGroup`, `bytes.Buffer`, or similar
  pointer-owned state after first use.
- Treat maps, slices, channels, and pointers as nil-capable contracts. Decide
  whether nil and empty are equivalent before exposing them, especially for
  JSON.
- Always assign the result of `append`; the backing array may change.
- Copy slices and maps at API boundaries when caller mutation would violate the
  callee's invariants or returned state should be immutable to callers.
- Use `crypto/rand` for keys, tokens, and security-sensitive randomness. Never
  use `math/rand` for secrets.
- Do not hardcode environment-specific configuration in libraries or deep
  packages. Parse env, flags, and config files at process boundaries, validate
  once, and pass typed configuration inward.
- Keep `panic`, `log.Fatal`, and `os.Exit` out of libraries and non-main code.
  Return errors for ordinary failures; panic only for programmer errors,
  impossible states, or startup failures where recovery is not expected.

## API Shape And Style

- Prefer clarity, simplicity, concision, maintainability, then local
  consistency, in that order.
- Keep the normal path unindented. Handle errors and special cases first; omit
  `else` after `return`, `break`, `continue`, or `goto`.
- Use `if` or `switch` initialization to reduce scope, but avoid `:=`
  shadowing that leaves the outer variable unchanged.
- Use `var` for intentional zero values and package-level declarations. Use
  `:=` for local values with obvious types.
- Use MixedCaps identifiers, consistent initialisms (`URL`, `ID`, `HTTP`), and
  short receiver names that stay consistent across a type's methods.
- Avoid names that repeat package or receiver context: prefer `widget.New()` to
  `widget.NewWidget()` and `p.Name()` to `p.ProjectName()`.
- Document exported packages, types, functions, methods, constants, and
  variables with comments that start with the exported name and read as
  complete sentences.
- Treat exported identifiers, module paths, JSON/database/protobuf/OpenAPI
  tags, CLI flags, file formats, metrics, and log field names as compatibility
  boundaries.
- Define interfaces at the consumer side unless the producer owns a stable
  abstraction used by many consumers.
- Keep interfaces small. One to three methods is a seam; a wide interface is
  often a hidden concrete type.
- Accept interfaces and return concrete types by default. Returning an
  interface is appropriate when the concrete implementation is intentionally
  hidden behind a stable standard or package-owned abstraction.
- Start with concrete code. Add generics only when multiple types share
  identical logic and interfaces do not model the behavior cleanly.
- Keep generic constraints minimal. Prefer standard constraints such as
  `comparable` or `cmp.Ordered` when available; do not over-constrain unions.

## Decision Heuristics

- **Package pressure:** if a package name becomes vague or exported names need
  stuttering to make sense, split responsibilities or rename the package.
- **Interface pressure:** if a new interface mirrors one concrete type exactly,
  it may be a mock seam rather than a design seam.
- **Generics pressure:** if only one concrete type exists today, write concrete
  code first unless the generic API is already part of the public contract.
- **Options pressure:** if optional constructor arguments are few and internal,
  prefer a config struct or explicit parameters; if they are public,
  extensible, and mostly defaulted, prefer functional options.
- **Error pressure:** if callers need to branch on errors, make that contract
  stable with sentinels, typed errors, or predicates before adding more string
  checks.
- **Context pressure:** if a function can block on I/O, locks, remote systems,
  or queues, pass context unless the repo has a narrower convention.
- **Goroutine pressure:** if you cannot say who cancels a goroutine, who waits
  for it, and who observes its error, do not start it yet.
- **Service-boundary pressure:** if a handler, RPC method, or CLI command is
  accumulating business rules, split transport decoding from domain behavior
  before adding more branches.
- **Test-shape pressure:** if a table test needs conditionals for setup or
  assertions, split it; table tests should reduce duplication, not hide logic.
- **Profile pressure:** if a performance change cannot name the measured
  bottleneck, the benchmark/profile used, and the before/after signal, treat it
  as speculative cleanup rather than optimization.
- **Dependency pressure:** if adding a module changes licenses, binary size,
  supply-chain risk, or transitive surface, justify it against standard library
  or repo-local alternatives.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness, resource safety, or race
  safety, prefer correctness.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.

## Validation

A change is done when:

- `gofmt` or the repo's formatter has run on touched Go files
- `goimports` or the repo's import formatter has run when imports changed
- touched packages compile and affected tests pass
- new or changed behavior has tests, or the lack of tests is called out with a
  concrete reason
- `go vet`, `staticcheck`, `golangci-lint`, or the repo's static analysis path
  reports no new findings when available
- `go test -race` is run for touched packages when concurrency, shared state,
  or goroutine lifetime changed
- benchmarks, `pprof`, traces, or allocation profiles back performance-driven
  changes
- module, generated-code, build-tag, and wire-format changes are verified with
  the repo's established commands
- security-sensitive code gets the repo's security scan, such as `gosec`, when
  available
- review findings at `Critical` and `Important` severity are addressed

## Examples

- `Review this Go worker for context cancellation, goroutine leaks, and race risks`
- `Refactor this Go service package without breaking exported API or error contracts`
- `Add a Go HTTP handler and keep business logic testable outside the transport`
- `Add a gRPC method and preserve context deadlines, error mapping, and service-layer tests`
- `Write standard Go tests for this parser, including error semantics and fuzz seeds`
- `Design a constructor for this Go client without adding global mutable state`
- `Optimize this Go hot path using benchmarks and pprof evidence, not speculation`
