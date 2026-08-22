# Bash Process And Filesystem Safety

Read this reference when a Bash task constructs commands dynamically, handles
arbitrary filenames, changes directories, launches background work, supports
concurrent invocation, or crosses operating-system tool boundaries.

## Commands and processes

- Pass user-controlled values as individual argv elements, not through `eval`
  or re-parsed strings.
- Avoid `eval` unless the script is explicitly a shell metaprogramming tool and
  the risk is justified.
- Preserve argument boundaries and treat external-tool exit codes as part of
  the script contract.
- End option parsing with `--` when forwarding values that could begin with a
  dash and the receiving tool supports it.
- Scope `cd` to a subshell or restore the previous directory explicitly.
- For background jobs, track PIDs, aggregate `wait` results deliberately, and
  forward or handle termination signals instead of abandoning children.
- Before parallel or concurrent mutation, define locking, isolation, or
  idempotency. Use `flock` or a documented platform equivalent when concurrent
  invocations can interfere.

## Files and iteration

- Resolve and validate explicit target paths before destructive operations.
- Prefer `while IFS= read -r line; do ...; done` over implicit whitespace
  splitting.
- Use NUL-safe filename transport from `find`, `git`, and similar tools with
  `-print0`, `xargs -0`, or `read -r -d ''` where supported.
- Use `readarray` or `mapfile` when populating Bash arrays from line-oriented
  output.
- Avoid `for value in $(...)` for filenames or untrusted data.
- Prefer built-ins and parameter expansion over subprocesses when they improve
  clarity and preserve data boundaries.

## Platform fit

- Use Bash-specific features only when the shebang and repository contract
  allow them.
- Check GNU versus BSD tool differences before adding flags whose behavior is
  inconsistent across supported platforms.
- Detect material platform behavior explicitly instead of assuming Linux.
- Prefer existing helper scripts and path conventions over ad hoc wrappers or
  temporary locations.
- Move non-trivial parsing, JSON handling, or data shaping to a better-suited
  language when shell stops being the clearest tool.
