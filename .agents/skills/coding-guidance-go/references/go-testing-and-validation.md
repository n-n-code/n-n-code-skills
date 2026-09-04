# Go Testing And Validation

Load this reference for Go test implementation, test review, validation command
selection, race checks, fuzzing, benchmarking, or integration-test gating.

## Test Style

- Prefer the standard `testing` package for new tests unless the repo already
  standardizes on testify. Use `go-testing-with-testify` for testify-specific
  assertion, mock, suite, or flake work.
- Use the repo's existing comparison helper. Add or use `cmp.Diff` only when
  complex comparisons justify it or the dependency is already present.
- Write failures that can be diagnosed without rereading the test source:
  include function, inputs, got value, and want value. Print got before want.
- Use `t.Error` when later assertions remain meaningful. Use `t.Fatal` when
  setup failed or continuing would produce misleading failures or unsafe test
  behavior.
- Never call `t.Fatal`, `t.FailNow`, or `require.*` from a goroutine other than
  the test goroutine.

## Table Tests And Subtests

- Use table-driven tests when cases share setup and assertions.
- Split into separate tests when each case needs different setup, mocks,
  branching, or separate oracles.
- Use named fields in table cases when cases span many lines or adjacent fields
  have the same type.
- Use subtests when filtering, parallelism, or scenario names improve
  diagnosis.
- Capture range variables deliberately when using parallel subtests or
  goroutines.

## Helpers And Fixtures

- Call `t.Helper()` in helpers whose failures should point at their caller;
  place it before the helper reports failures.
- Use `t.Cleanup()` for teardown owned by helpers.
- Use `t.TempDir()` and `testdata/` for filesystem fixtures.
- Use golden files only when the expected output is large or intentionally
  reviewed.
- Avoid test helper packages that hide important domain setup or make assertions
  harder to read.

## Error Testing

- Test error semantics with `errors.Is`, `errors.As`, predicates, or error
  presence, not brittle error string equality.
- If callers branch on an error, the test should prove the stable contract.
- If only failure presence matters, assert presence and avoid over-specifying
  the message.

## Boundary Tests

- Prefer real transports such as `httptest.NewServer` at HTTP boundaries when
  protocol behavior is the risk.
- For gRPC or queue boundaries, test deadline propagation, cancellation,
  transport error mapping, and retry/idempotency behavior at the seam.
- Keep business logic testable without the transport by moving it behind a
  service/use-case function.

## Timing And Flake Control

- Avoid `time.Sleep` in tests. Use channels, contexts, fake clocks, polling with
  deadlines, or synchronization points.
- Use `go test -race` when shared state, goroutine lifetime, or synchronization
  changed.
- Use `go test -count=N` for order-dependent or flaky behavior after making the
  test deterministic enough to be meaningful.
- On Go 1.25+, consider `testing/synctest` for compatible in-process concurrent
  code: virtual time and quiescence can replace wall-clock timing guesses.
  Consult the [package contract](https://pkg.go.dev/testing/synctest) for supported
  operations; real external I/O still needs its own evidence.
- On Go 1.24+, `t.Context()` cancels before test cleanup. Cancellation does not
  join a goroutine; wait for owned workers before tearing down their fixtures.
- Use `t.Cleanup` for shared fixtures with parallel subtests. A parent function's
  `defer` runs before paused parallel children resume and may close fixtures early.

## Fuzzing And Benchmarks

- Use fuzz tests when input parsing, validation, encoders/decoders, or protocol
  edge cases are the risk.
- Seed fuzz tests with representative valid and invalid cases.
- Use benchmarks for performance claims, not as a replacement for behavior
  tests.
- For repos targeting Go 1.24 or later, prefer `b.Loop()` for new benchmarks.
  Preserve the repo's existing `b.N` style when compatibility requires it and
  reset timers after expensive setup in that style. Report allocations when
  allocation count is part of the claim.

## Integration Tests

- Put slow integration tests behind the repo's existing mechanism, such as
  `testing.Short()` or build tags.
- Verify tagged paths when behavior depends on tags.
- Keep integration tests explicit about external dependencies, ports,
  credentials, and cleanup.

## Validation Commands

Choose the smallest proof that covers the risk:

- formatting/imports: `gofmt`, `goimports` when available
- compile and behavior: targeted `go test ./path/...`
- static analysis: `go vet`, `staticcheck`, `golangci-lint` when available
- concurrency: `go test -race`
- flake/order sensitivity: `go test -count=N`
- coverage signal: `go test -cover` or repo coverage target
- performance: `go test -bench`, benchmark profiles, `pprof`, traces
- modules and generated code: repo `go generate`, `go mod`, or build-tag
  commands
- security-sensitive code: repo security scan such as `gosec` when available
