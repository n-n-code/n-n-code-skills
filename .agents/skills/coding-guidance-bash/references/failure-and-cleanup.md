# Bash Failure And Cleanup

Read this reference when a Bash task changes strict options, failure recovery,
traps, temporary resources, or destructive behavior.

## Failure options

- Treat `set -e` as a control-flow feature with documented exceptions, not a
  substitute for explicit error handling. Its behavior changes in tests,
  lists, pipelines, functions, subshells, and command substitutions.
- Enable `pipefail` when failure in any pipeline component should fail the
  pipeline; handle expected non-zero statuses explicitly.
- Enable `-u` only after optional positional parameters, arrays, and environment
  values have deliberate defaults or guards.
- Use `-E` or `shopt -s inherit_errexit` only when the supported Bash version
  and intended propagation semantics justify them.
- Prefer `if command; then ...`, `command || handle_failure`, or captured status
  when recovery, fallback, or cleanup depends on a particular failure.

## Cleanup and diagnostics

- Validate required environment variables explicitly with
  `: "${VAR:?message}"`.
- Detect required external tools with `command -v` before the path that needs
  them; do not reject optional modes unnecessarily.
- Use `mktemp` for temporary files and directories; never hand-roll shared temp
  paths.
- Register cleanup after a resource is acquired, and keep traps safe when
  setup fails partway through.
- Preserve the original exit status when cleanup runs after failure.
- Use targeted `ERR` diagnostics only when they add actionable line or function
  context without duplicating every error.
- Prefer dry-run modes, idempotency, or disposable fixtures before exercising
  destructive or expensive paths.

Test expected failures as well as success. A script that exits early is not
necessarily correct if it leaks resources, masks the original status, or skips
required rollback.
