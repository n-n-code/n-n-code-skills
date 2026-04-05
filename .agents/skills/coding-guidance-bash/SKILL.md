---
name: coding-guidance-bash
description: Bash implementation and review skill. Use when writing, modifying, refactoring, or reviewing Bash scripts, especially automation and repo tooling that need defensive error handling, safe quoting, predictable control flow, and maintainable shell boundaries. Portable across Bash-based repos and script stacks.
---

# Bash Coding Guidance

This skill adds portable Bash implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable Bash engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **project-core-dev** (repo-specific build/test commands),
  **project-platform-diagnose** (environment-sensitive diagnosis)

## When Not to Lean on This Skill

- non-shell work
- POSIX `sh` portability work where Bash-only features are not allowed
- large data processing jobs that should realistically move to Python, awk, or
  another language with stronger structure

## Implementation Workflow

1. Read the touched scripts, entrypoints, call sites, and nearby docs before
   editing.
2. Infer the intended contract from current usage text, flags, tests, and
   environment assumptions. Ask only when multiple plausible script behaviors
   would change semantics.
3. Keep the contract narrow: inputs, outputs, exit codes, environment
   dependencies, filesystem effects, and external tool requirements should be
   explicit.
4. Implement with defensive mode, safe quoting, arrays for argv construction,
   functions for meaningful substeps, and cleanup traps for temporary state.
5. Add or update shell tests when the repo has them; otherwise add the smallest
   reproducible validation path you can run directly.
6. Run the narrowest relevant formatter, linter, and script tests the repo
   supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, flags, environment assumptions, platform
   dependencies, and failure modes.
2. Break the refactor into small slices that preserve behavior.
3. Replace copy-pasted command assembly, hidden globals, unsafe loops, and
   tangled control flow one step at a time.
4. Keep tests or runnable validation passing after each slice; add
   characterization coverage first when behavior is unclear.
5. Stop when the script is easier to read, safer to invoke, and easier to
   debug.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize quoting and word-splitting bugs, globbing hazards, accidental
   masking of failing commands, trap and cleanup bugs, unsafe temp-file
   handling, destructive command risks, portability mismatches, environment
   assumptions, and missing tests.
4. State findings with concrete evidence and the likely consequence.

## Bash Rules

### First tier - causes bugs

- Start executable Bash scripts with `#!/usr/bin/env bash` unless the repo has
  a stricter shebang convention
- Use `set -Eeuo pipefail` unless the script has a documented reason to manage
  failures differently; scope exceptions narrowly
- Quote expansions by default: `"$var"`, `"${arr[@]}"`, and `"$(cmd)"`
- Use arrays for argument vectors; do not build command lines with string
  concatenation
- Distinguish stdout data from stderr diagnostics so callers can compose the
  script safely
- Check exit statuses deliberately; do not rely on pipelines, subshells, or
  command substitutions without understanding how failures propagate
- Clean up temp files and directories with `trap` when the script allocates
  them
- Treat `$IFS`, globs, current working directory, and environment variables as
  boundary conditions, not stable ambient assumptions

### Second tier - prevents mistakes

- Prefer functions for meaningful units of behavior; keep top-level script flow
  readable
- Use `local` inside functions unless a variable is intentionally shared
- Prefer `[[ ... ]]` for Bash conditionals and `case` for multi-branch string
  matching
- Prefer `printf` over `echo` when escaping, flags, or portability ambiguity
  matter
- Use command substitution `$()` instead of backticks
- Name flags, env vars, and functions for what they do; shell scripts become
  unreadable quickly when names get vague
- Keep shellcheck findings at zero in repo-owned code unless the script has a
  documented exception

### Defensive patterns

- Consider `shopt -s inherit_errexit` when the Bash version and repo contract
  allow it and command-substitution failures must propagate cleanly
- Validate required env vars explicitly with `: "${VAR:?message}"`
- Detect missing external tools up front with `command -v tool >/dev/null 2>&1`
- Use `mktemp` for temp files and directories; never hand-roll temp paths in
  shared locations
- Prefer dry-run modes and idempotent behavior before destructive or expensive
  operations
- Use `trap` for cleanup and, when helpful, targeted `ERR` reporting with line
  or function context

### Command and process discipline

- Pass user-controlled values as individual argv elements, not through `eval`
  or re-parsed strings
- Avoid `eval` unless the script is explicitly a shell metaprogramming tool and
  the risk is justified
- Prefer explicit path resolution and file existence checks before destructive
  operations
- When calling external tools, preserve argument boundaries and treat tool exit
  codes as part of the contract
- Be deliberate about `cd`; either scope it to a subshell or restore the prior
  directory clearly
- End option parsing with `--` when forwarding user arguments to external
  commands
- If the script spawns background jobs, make ownership explicit: track PIDs,
  aggregate `wait` results deliberately, and forward or handle termination
  signals rather than abandoning children
- Avoid casual parallel destructive work; if concurrency matters, define the
  locking, isolation, or idempotency rule up front
- If concurrent invocations can interfere with each other, use an explicit lock
  strategy such as `flock` or a documented equivalent instead of hoping paths
  or timing stay unique

### Input, output, and contract design

- Provide `--help` or usage text for non-trivial scripts
- Make required env vars, positional args, flags, and side effects explicit
  near the top of the file
- Exit with non-zero status on real failure and reserve zero for success
- Print machine-consumable output in a stable format when other tools are meant
  to parse it
- Avoid silent fallbacks on missing tools or files unless the script is
  explicitly best-effort
- Use stable exit-code meanings when the script is likely to be called by other
  automation

### Safe iteration and file handling

- Prefer `while IFS= read -r line; do ...; done` over loops that split on
  whitespace implicitly
- Use NUL-safe patterns for filenames from `find`, `git`, or similar tools:
  `-print0`, `xargs -0`, or `read -r -d ''`
- Use `readarray` or `mapfile` when populating arrays from command output in
  Bash-specific scripts
- Avoid `for f in $(...)` for filenames or untrusted data; it is usually a bug
- Prefer built-ins and parameter expansion over unnecessary subprocesses when
  they make the script clearer and safer

### Portability and platform fit

- Use Bash-specific features only when the shebang and repo contract allow them
- If the script must run on multiple platforms, check GNU vs. BSD tool
  differences before adding flags with inconsistent behavior
- If platform behavior matters, detect it explicitly instead of assuming Linux
- Prefer the repo's existing helper scripts and path conventions over ad hoc
  temp locations or duplicated wrappers
- Move non-trivial parsing, JSON handling, or data shaping to a better-suited
  language when shell stops being the clearest tool

### Style, testing, and tooling

- Prefer long, readable option names for user-facing interfaces when the repo
  does not already prescribe a short-only style
- Keep functions small enough to understand locally; split when one function
  starts owning parsing, validation, execution, and reporting all at once
- Run `shellcheck` and `shfmt` where the repo uses them
- Prefer Bats or the repo's existing shell-test framework for non-trivial
  scripts
- Document required tools and minimum Bash features when the script depends on
  them

## Decision Heuristics

Use these when the right choice is not obvious:

- **Language fit:** if the task needs nested data structures, complex parsing,
  or large in-memory transforms, shell may be the wrong tool.
- **Quoting pressure:** if command construction becomes hard to reason about,
  switch to arrays or redesign the interface before adding more flags.
- **Failure visibility:** if `set -e` behavior is unclear in a construct, make
  the check explicit rather than assuming the shell will fail the right way.
- **Process ownership:** if the script backgrounds work, define who waits,
  cleans up, and reports failures before adding more parallelism.
- **Portability pressure:** if a script relies on GNU-only flags, a Bash 5.x
  feature, or OS-specific tools, document and validate that boundary instead of
  hiding it.
- **Repo conventions:** if the repo has established patterns for shebangs,
  strict mode, shellcheck, shfmt, or helper libraries, follow them unless they
  create a correctness or safety problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.
- **Abstraction threshold:** three similar command sequences or repeated flag
  parsing pain is a pattern; before extracting, check whether a function, a
  helper script, or a small move to another language is the simpler move.
- **External-tool boundary:** if a script depends on `jq`, `awk`, `sed`, or
  platform-specific tooling, treat that dependency as part of the user-facing
  contract.

## Validation

A change is done when:

- shellcheck or the repo's equivalent linter reports no new findings
- shell formatting is run when the repo has a formatter
- changed `--help`, argument parsing, or top-level script startup paths are
  smoke-tested before deeper functional validation
- existing shell tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- non-trivial scripts have a direct smoke path such as `--help` or a minimal
  fixture invocation
- destructive or environment-mutating paths were verified against a safe test
  fixture rather than assumed correct
- portability-sensitive changes were tested on the affected platform or the
  remaining platform risk was called out explicitly
- review findings at `Critical` and `Important` severity are addressed

## Examples

- `Review this Bash deploy script for quoting, traps, and rollback safety`
- `Refactor this repo automation script to use arrays, safe temp files, and better argument parsing`
