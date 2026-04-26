# TUI Layout And Production Patterns

Use this reference when a Charmbracelet TUI task needs deeper layout,
multi-screen, production, or review guidance than the core skill can afford to
load every time.

## Layout Invariants

- Calculate content size before rendering. Subtract title bars, status bars,
  margins, padding, and border frames before passing dimensions into panels or
  Bubbles components.
- Bordered panels consume extra cells. Prefer filling the inner content to the
  intended height, then let the border render around it, instead of setting an
  explicit panel height and hoping the math lines up.
- Decide whether each region wraps or truncates. Auto-wrap inside bordered
  panels can add hidden lines and misalign adjacent panes; truncate low-value
  labels and wrap only body text that is allowed to grow.
- Use `lipgloss.Width`, `lipgloss.Height`, `lipgloss.Size`, and style frame
  helpers for ANSI-aware and Unicode-aware layout. Do not use `len` for visual
  width.
- Use proportional weights for split panes instead of fixed columns. A focused
  pane can get a larger weight, such as `2:1`, while total width still fits the
  terminal.
- Match pointer hit testing to layout orientation. Side-by-side panes use X
  ranges; stacked panes use Y ranges. Recompute hit zones after every resize.
- Treat emoji and wide glyphs as risky in aligned tables, gutters, and status
  bars. Prefer measured strings, plain fallback glyphs, or explicit terminal
  compatibility checks when alignment matters.

## Screen And Focus State

- Represent screens, routes, modes, and focus with explicit typed values rather
  than scattered booleans or strings.
- Keep the model fields that explain navigation together: current screen,
  previous screen, focus target, selected index, cursor, scroll offset, modal
  stack, and status message.
- Route global keys first only for true global actions such as quit, cancel,
  help, or modal dismissal. Then delegate to the focused screen or component.
- Reset cursor and scroll position intentionally on screen changes. Preserve
  them intentionally when returning to a previous screen.
- For scrollable content, derive visible rows from current height, clamp scroll
  after data or size changes, and test empty, short, exact-fit, and overflow
  content.
- For modal or overlay flows, save prior focus, restore it on dismissal, and
  ensure background components do not consume keys while the overlay owns focus.

## Production Behavior

- Prefer a plain-output path when stdout is piped, stdin is noninteractive, the
  command runs in CI, `TERM=dumb`, or a repo-supported `--no-tui`/`NO_TUI`
  option is set.
- Handle `ctrl+c`, `esc`, and explicit cancel in a way that restores terminal
  state and does not silently discard user work.
- Expose current mode through the UI: title, breadcrumb, status segment,
  selected sort/filter, form progress, or help text.
- Use semantic styles: title, selected, muted, danger, success, warning, help,
  border, and status. Do not encode important state only through color.
- Respect `NO_COLOR` and limited color profiles where the repo supports them.
  Test both light and dark background assumptions when colors communicate
  priority or danger.
- Keep optional integrations graceful. If clipboard, editor dispatch, syntax
  highlighting, markdown rendering, or image preview is unavailable, hide the
  shortcut or show a clear fallback.

## Performance Patterns

- Use `strings.Builder` for non-trivial `View` assembly and call `Grow` when a
  rough size is known.
- Precompute package-level or model-owned styles. Avoid rebuilding the same
  Lip Gloss styles on every frame.
- Cache expensive derived output, such as Glamour-rendered markdown, syntax
  highlighting, filtered result sets, or table layouts, by content and width.
- Virtualize large lists and tables. Render visible rows, not the entire
  dataset, when data can grow.
- Use debounced commands for search or filtering that would otherwise fire on
  every keypress.
- Tag async commands with request IDs, versions, or content hashes so stale
  results cannot overwrite newer state.
- Keep background workers owned by the Bubble Tea program lifecycle. Recover
  and report worker panics as typed messages when the repo has long-running
  goroutines.

## Review False Positives

Do not flag these by themselves:

- `return m, m.loadData()` where `loadData` only constructs and returns a
  `tea.Cmd`
- value receivers on `Update` with local model field assignments that are
  returned as the next state
- nested child component updates such as `m.list, cmd = m.list.Update(msg)`
- `tea.Batch(cmdA, cmdB)` for independent work that can complete in any order
- helper methods that return `tea.Cmd` descriptors without doing side effects
  before the command is returned

Do flag these:

- filesystem, network, subprocess, `time.Sleep`, blocking channel receive, or
  `huh.Form.Run()` directly inside `Update`
- side effects, logging, mutation, I/O, random data, or wall-clock reads inside
  `View`
- commands whose results cannot be cancelled, ignored when stale, or surfaced
  as typed error messages
- Bubbles component `Update` results that are not assigned back to the parent
  model
- key bindings shown in help but not implemented, or implemented but hidden
  from help
- layout math that uses byte length for visible width or ignores frame size

## Validation Prompts

Use these lightweight simulations when changing this skill or applying it:

- `Build a Bubble Tea v2 dashboard with list, detail, search, and help.`
  Expected: use version-aware imports, explicit focus state, Bubbles component
  ownership, debounced search, resize handling, and render/cache guidance.
- `Review this Bubble Tea Update for blocking behavior.`
  Expected: distinguish command constructors from actual blocking calls and
  report only concrete event-loop risks.
- `Fix this Lip Gloss dual-pane layout with mouse selection.`
  Expected: inspect border/frame math, truncation/wrapping, proportional pane
  sizing, and X/Y hit testing based on layout orientation.
- Negative: `Make this Bash deployment script ask one yes/no question.`
  Expected: do not use this Go TUI skill as the primary path.
