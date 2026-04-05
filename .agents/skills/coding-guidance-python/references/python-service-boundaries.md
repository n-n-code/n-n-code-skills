# Service boundaries

Use this reference only when the Python task crosses a real I/O boundary such
as HTTP, queues, cron jobs, subprocesses, or persistent workers.

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
