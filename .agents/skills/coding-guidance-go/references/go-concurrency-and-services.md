# Go Concurrency And Services

Load this reference for Go tasks involving context propagation, goroutine
lifecycle, shared state, pipelines, backpressure, logging, REST/gRPC/CLI/worker
boundaries, or transport error mapping.

## Context

- Pass `context.Context` as the first parameter for request-scoped or
  cancellation-aware work.
- Do not store contexts in structs, define custom context interfaces, or use
  context values for optional parameters.
- Derive contexts close to the work that owns the deadline or cancellation, and
  call the returned cancel function in that same ownership scope.
- Return or propagate `ctx.Err()` when cancellation or deadline expiry is the
  reason work stopped.
- Use context values only for request-scoped data such as request IDs, trace
  IDs, auth claims, and request-scoped loggers.

## Goroutine Ownership

- Prefer synchronous APIs. Let callers add concurrency unless the package owns a
  real lifecycle or throughput concern.
- Do not start a goroutine unless you can name who cancels it, who waits for it,
  and who observes its error.
- Use `sync.WaitGroup`, `errgroup`, or equivalent ownership helpers when
  multiple goroutines must finish together.
- Avoid goroutines in `init`; expose `Start`, `Stop`, `Close`, or `Shutdown`
  methods so tests and callers control lifecycle.
- Ensure senders cannot block forever after cancellation. Use select on
  `ctx.Done()` for sends or receives that may outlive the caller.

## Shared State

- Use channels to transfer ownership or events; use mutexes to protect shared
  state. Do not use channels only to avoid a simple lock.
- Do not copy values containing `sync.Mutex`, `sync.WaitGroup`, `bytes.Buffer`,
  or similar pointer-owned state after first use.
- Prefer named mutex fields over embedded mutexes so locking does not become
  part of the public API.
- Use typed atomic values for small state flags or counters when atomics are
  genuinely simpler than a mutex.
- Document thread-safety when read operations mutate internal state, when the
  type provides synchronization, or when callers must provide synchronization.

## Channels And Pipelines

- Close channels only from the sending side that owns completion.
- Specify channel direction in function signatures when possible.
- Default channels to unbuffered or size one. Larger buffers need a documented
  reason, backpressure behavior, and overload expectation.
- For pipelines, make every stage observe cancellation, close only its owned
  outbound channel, and propagate errors without leaving senders or receivers
  blocked.
- For fan-out/fan-in, capture loop variables deliberately and make result
  aggregation safe under concurrency.

## Backpressure

- Use worker pools, semaphores, rate limiters, or queues when the real contract
  is bounded concurrency or throughput.
- Make bounds configurable when they depend on deployment capacity.
- State what happens when the bound is reached: block, reject, drop, retry,
  queue, or shed load.
- Avoid unbounded goroutine, channel, or work-queue growth when input can spike.

## Timers

- Stop tickers and timers when the owner is done.
- Prefer context deadlines for request-scoped timeouts; use timers when the
  timer is local control flow rather than caller-owned cancellation.
- Be explicit about drain behavior when reusing timers in loops.

## Service Boundaries

- At REST, gRPC, CLI, and worker boundaries, convert transport-specific inputs
  into typed domain inputs early and keep business logic testable without the
  transport.
- Pass deadlines and cancellation through every outbound RPC, database call,
  queue operation, subprocess, and long-running loop.
- Keep handlers and RPC methods thin: decode and validate input, call a
  service/use-case layer, map domain errors to transport responses, and log only
  at the boundary where the request outcome is known.
- Do not expose internal error messages, package paths, SQL details, or panic
  values through public API responses.
- Use the repo's established status-code, gRPC status, or CLI exit-code mapping
  before inventing a new error-response scheme.

## Logging

- Prefer the repo's existing logger. For new Go 1.21+ production code without a
  repo convention, prefer `log/slog`.
- Use static log messages with structured key-value attributes. Dynamic data
  belongs in fields, not in `fmt.Sprintf` message strings.
- Use consistent low-cardinality field names such as `request_id`, `user_id`,
  `operation`, `attempt`, `duration`, and `err`.
- Include an `"err"` attribute on error logs. Log or return an error once; do
  not log and re-return the same error at every layer.
- Never log secrets, credentials, tokens, full request or response bodies, PII,
  or unbounded maps/slices.

## Validation

- Run `go test -race` for touched packages when changing goroutine lifetimes,
  shared state, locks, channels, or callbacks.
- Repeat flaky or concurrency-sensitive tests with `-count` when ordering or
  timing is the risk.
- For services, exercise cancellation, timeout, error mapping, and shutdown
  paths, not just the happy path.
