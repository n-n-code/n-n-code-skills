# Service boundaries

Use this reference only when the Python task crosses a real I/O boundary such
as HTTP, queues, cron jobs, subprocesses, or persistent workers.

## Use when

- implementing or reviewing Python service handlers, workers, scheduled jobs,
  subprocess orchestration, or long-lived processes
- changing retries, timeouts, idempotency, backpressure, logging, metrics, or
  trace context
- deciding what belongs in core logic versus framework, transport, or
  persistence edges

Do not load this reference for local pure-function work or scripts whose only
observable contract is command-line input/output.

## Rules

- Emit enough structured logs, metrics, or trace context to explain what
  happened without redeploying for diagnosis
- Use stable, bounded log and metric fields; do not emit high-cardinality
  labels such as raw user IDs into metrics
- Distinguish expected operational events from real failures; do not log normal
  validation or user mistakes as `ERROR`
- Be explicit about timeouts, retries, idempotency, and backpressure at I/O
  boundaries
- Retry only transient failures, with bounded attempts and jittered backoff
- Keep retry ownership in one layer; double-retry behavior is usually a bug
- Keep domain decisions testable without running the transport, scheduler, or
  worker framework when the domain itself does not require that machinery
