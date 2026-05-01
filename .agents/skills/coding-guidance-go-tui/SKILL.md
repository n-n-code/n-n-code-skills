---
name: coding-guidance-go-tui
description: Go terminal UI implementation and review skill. Use when writing, modifying, refactoring, testing, or reviewing interactive Go TUIs built with Charmbracelet Bubble Tea, Bubbles, Lip Gloss, embedded Huh forms, Charm stack v2, tea.Model, tea.Cmd, key bindings, focus state, terminal layouts, or terminal screen state machines. Portable across Go TUI repos.
---

# Go TUI Coding Guidance

Portable implementation, refactoring, testing, and review guidance for
interactive Go terminal user interfaces built with Charmbracelet Bubble Tea,
Bubbles, Lip Gloss, embedded Huh forms, and related Charm libraries.

## Adjacent Skills

Use this as the default principle skill for Charmbracelet Go TUI work. Compose
with:

- **Workflow:** `thinking` for planning, `recursive-thinking` for
  stress-testing, `tester-mindset` for validation strategy, and `security` for
  sensitive input, shell execution, token display, or filesystem access
- **Project overlays:** `project-core-dev` for repo validation,
  `project-config-and-tests` for config and deterministic tests, and
  `project-platform-diagnose` for terminal capability, piped stdio, SSH,
  alt-screen, shell, platform, install, or runtime smoke issues
- **Go depth:** `coding-guidance-go` only when the non-TUI Go package design,
  concurrency, service boundary, profiling, or module behavior is the main
  risk

Use `coding-guidance-go` instead when the task is a non-interactive Go CLI,
library, worker, service, or test change with no terminal UI state machine.

## Reference Map

Load references only when the task needs that depth:

- [references/charmbracelet-patterns.md](references/charmbracelet-patterns.md)
  for version-specific Bubble Tea APIs, Bubbles component integration, Huh form
  integration, Lip Gloss APIs, key binding patterns, and upstream example
  routing
- [references/tui-layout-and-production.md](references/tui-layout-and-production.md)
  for layout arithmetic, responsive panels, mouse hit testing, screen/focus
  state machines, production polish, performance, noninteractive fallbacks, and
  Bubble Tea code-review false positives

## When Not to Lean on This Skill

- non-Go terminal UI frameworks such as ncurses, Textual, blessed, termbox, or
  curses-style wrappers unless only the generic TUI UX ideas apply
- simple command-line flag parsing, one-shot command output, or prompt-only
  flows that do not maintain an interactive screen
- shell-only prompt polish with Gum, VHS, Mods, or plain shell unless the user
  is explicitly converting the flow into a Go Bubble Tea TUI
- web, mobile, or graphical desktop UI work; use the appropriate UI or platform
  guidance instead
- broad Go backend, package architecture, or performance work where Bubble Tea,
  Bubbles, and Lip Gloss are incidental

## Implementation Workflow

1. Inspect `go.mod`, imports, nearby models, Bubbles and Huh components, Lip
   Gloss styles, examples, tests, and docs before editing. Preserve the repo's
   current Charmbracelet major version and import path unless the task is
   explicitly an upgrade. Check upstream Charm examples when the component
   pattern is unfamiliar.
2. Identify the app mode: inline or full-screen, alternate screen or normal
   output, keyboard and mouse expectations, input/output streams, width and
   height constraints, external commands, background work, noninteractive or
   `--no-tui` fallback, and error states.
3. Model the TUI as an explicit state machine: screen or mode, focus target,
   previous screen or return path, dimensions, data loading state, request or
   stale-result marker, domain state, selected item, cursor or scroll position,
   pending command, error/status message, and child component state.
4. Keep `Update` deterministic and fast. Represent side effects as `tea.Cmd`
   values that return typed `tea.Msg` values; do not block on filesystem,
   network, subprocess, timers, or heavy rendering work inside `Update` or
   `View`. Use `tea.Batch` for independent commands and `tea.Sequence` only
   when ordering is observable behavior.
5. Compose Bubbles and Huh components deliberately. Store component models in
   the parent model, route key and resize messages by focus or mode, assign
   updated component values back to the parent, collect returned commands, and
   keep child widths, heights, styles, and focus state synchronized.
6. Render from state only. `View` should not mutate state, start work, read
   files, call services, log, or depend on wall-clock time. Build terminal
   layouts with Lip Gloss styles, cell-aware helpers, `strings.Builder`, and
   caches for expensive derived text instead of ad hoc ANSI string arithmetic.
7. Design terminal UX as product behavior: clear focus, visible help, safe quit
   and cancel paths, loading and empty states, recoverable errors, accessible
   keyboard shortcuts, resize behavior, narrow-terminal fallbacks, plain-output
   escape hatches, and no mouse-only interactions.
8. Add or update focused tests close to the changed behavior. Prefer model
   transition tests with synthetic messages, command tests around command
   constructors, and stable render assertions for important layout or text
   contracts.
9. Run the narrowest relevant formatter, import formatter, tests, and manual
   smoke command the repo supports. A visible TUI behavior change usually needs
   at least one interactive smoke run or recorded terminal-output check.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current states, messages, commands, key bindings, component
   ownership, render paths, dimensions, and external side effects.
2. Add characterization tests first when state transitions or command behavior
   are unclear.
3. Split tangled root models into screen, component, command, and style helpers
   only when the split makes state ownership and message flow easier to follow.
4. Preserve user-visible key bindings, output text, persisted formats, command
   side effects, and terminal mode choices unless the task explicitly changes
   them.
5. Keep the app runnable after each slice; terminal apps are easy to break with
   a compile-passing render or focus regression.

## Review Workflow

When reviewing, skip implementation steps and use this checklist:

1. Read the full state/message/render loop before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Rank correctness, data-loss, terminal-state, and event-loop defects above
   polish. Layout, color, and help-text issues become higher severity only when
   they block navigation, hide required information, or break supported terminal
   contexts.
4. Prioritize blocking `Update` or `View` work, lost or unordered commands,
   unhandled errors, command goroutine leaks, state mutation during rendering,
   stale window dimensions, unassigned Bubbles component updates, key binding
   conflicts, focus traps, missing quit/cancel behavior, alt-screen cleanup
   hazards, and fragile string-width math.
5. Avoid false positives: helper functions returning `tea.Cmd`, value receivers
   on `Update`, nested child `Update` calls, and `tea.Batch` are normal Bubble
   Tea patterns when no side effect runs before the command is returned.
6. Check whether rendering handles narrow terminals, Unicode width, color
   profiles, no-color environments, redirected input/output, and noninteractive
   CI execution where the repo claims support.
7. State findings with the triggering message or interaction path, the expected
   state transition, and the likely user-visible consequence.

## Bubble Tea Rules

- Treat the Bubble Tea model as the source of truth for UI state. Domain logic
  can live outside the model, but UI state should not be hidden in package
  globals or background goroutines.
- Use typed messages for domain results, errors, timers, subprocess completion,
  and external events. Avoid stringly message channels.
- Return commands explicitly. Use batching for independent follow-up commands
  and sequencing when ordering is part of behavior.
- Keep command constructors small and testable. They should capture immutable
  inputs, do the side effect, and return a typed success or failure message.
- Handle window-size messages at the top level, then propagate computed widths
  and heights to child components.
- Keep quit behavior deliberate. `q`, `esc`, `ctrl+c`, and form-cancel keys
  should match the app's conventions and should not discard work silently.
- Use program options such as custom input/output, context, fixed window size,
  or renderer disabling only when they match the repo's runtime or test seam.
- Keep logs and debug output out of the rendered screen. Route debug logging to
  files or test-only writers when needed.
- For current v2 code, keep terminal features declarative on `tea.View`; for
  older v1 code, preserve the repo's existing command-based terminal mode
  conventions unless the task is an upgrade.

## Bubbles Rules

- Prefer Bubbles components for standard text input, text area, table, progress,
  paginator, viewport, list, file picker, timer, stopwatch, help, spinner, and
  key binding behavior before hand-rolling those widgets. Prefer Huh for
  multi-field forms when the repo already uses it or the form semantics are
  clearer than custom widgets.
- Store every child component's returned model after `Update`; losing that value
  loses cursor position, scroll state, validation errors, and internal timers.
- Route global keys before focused component keys only when global behavior must
  win. Otherwise let focused inputs consume editing keys.
- Use `bubbles/key` bindings and the help component for discoverable shortcuts
  when the screen has more than trivial navigation.
- Do not call blocking form APIs such as `Run()` from inside a Bubble Tea
  `Update`; embed forms through their `Init`, `Update`, and `View` loop.
- Do not copy a component example wholesale into production code without
  reconciling focus rules, width/height updates, styles, validation, and domain
  state ownership.

## Lip Gloss Rules

- Centralize reusable styles, spacing, border, and color decisions. Avoid
  scattering raw ANSI escape codes or one-off magic strings across `View`.
- Measure rendered content with ANSI-aware, cell-aware helpers. Do not use
  `len` for terminal layout width.
- Treat width and height as inputs to rendering. Clamp panes, wrap long text,
  truncate low-value metadata, and provide compact fallbacks for small
  terminals.
- Account for borders, padding, and margins before rendering panels. Use
  frame-size helpers and explicit truncation or wrapping so bordered panels do
  not grow unexpectedly.
- Use proportional weights for split panes and match mouse hit testing to the
  current layout orientation: X coordinates for side-by-side panes, Y
  coordinates for stacked panes.
- Keep color optional and semantic. Preserve readable contrast, respect no-color
  or limited-color environments where the repo supports them, and do not encode
  state only through color.
- Build styles as values and render strings at the edge. Do not use style
  mutation or package-level mutable styles to smuggle runtime state into views.

## Production Runtime Rules

- Detect noninteractive contexts the repo claims to support: piped stdout,
  non-terminal stdin, CI, `TERM=dumb`, `NO_COLOR`, and app-specific `--no-tui`
  or `NO_TUI` flags. Fall back to plain output rather than forcing a full TUI.
- Keep expensive rendering off the hot path. Precompute stable styles, cache
  markdown or syntax-highlighted text by content and width, virtualize large
  lists, and discard stale async results with request IDs, content hashes, or
  version counters.
- Make multi-screen apps navigable: explicit screen or route values,
  breadcrumbs or titles, focus restoration after modals, reset cursor and
  scroll state intentionally on transitions, and show the current sort/filter or
  mode in status text.

## Validation

A Charmbracelet TUI change is done when:

- Go files are formatted with the repo's formatter and import tool
- touched packages compile and affected tests pass
- model transitions are tested with representative key, resize, success, error,
  quit, and cancel messages
- Bubbles component updates are covered where focus, validation, cursor,
  viewport, pagination, or timers changed
- important render output is checked at narrow and normal widths, with stable
  snapshots or focused string assertions when practical
- interactive behavior has been smoke-tested when terminal modes, keyboard
  input, alt screen, subprocess execution, mouse handling, clipboard, or cursor
  behavior changed
- noninteractive fallback is checked when the command can run in pipes, CI, or
  scripts, and narrow-terminal behavior is checked around an 80x24 baseline
- color behavior is checked for both light/dark assumptions and `NO_COLOR` or
  limited-color terminals when the repo supports them
- `go test -race` or equivalent concurrency validation runs when commands,
  goroutines, timers, subprocesses, or shared state changed

## Examples

- `Build a Bubble Tea TUI with a list, details pane, and help bar`
- `Review this Bubble Tea model for command ordering and focus bugs`
- `Refactor these Bubbles text inputs into a multi-step form`
- `Fix this Lip Gloss layout so it survives narrow terminals and Unicode text`
