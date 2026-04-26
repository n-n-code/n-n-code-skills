# Charmbracelet TUI Patterns

Use this reference when a task needs concrete Bubble Tea, Bubbles, or Lip Gloss
API shape. Check local `go.mod` and imports first; this reference describes
current v2 patterns and decision rules, not permission to upgrade an existing
repo.

## Source Links

- Bubble Tea repository: <https://github.com/charmbracelet/bubbletea>
- Bubble Tea package docs: <https://pkg.go.dev/charm.land/bubbletea/v2>
- Bubble Tea examples: <https://github.com/charmbracelet/bubbletea/tree/main/examples>
- Bubbles repository: <https://github.com/charmbracelet/bubbles>
- Bubbles package docs: <https://pkg.go.dev/charm.land/bubbles/v2>
- Lip Gloss repository: <https://github.com/charmbracelet/lipgloss>
- Lip Gloss package docs: <https://pkg.go.dev/charm.land/lipgloss/v2>
- Huh repository: <https://github.com/charmbracelet/huh>
- Huh package docs: <https://pkg.go.dev/charm.land/huh/v2>

## Version And Import Routing

- Current Charmbracelet v2 module paths use `charm.land/bubbletea/v2`,
  `charm.land/bubbles/v2`, and `charm.land/lipgloss/v2`.
- Older code may use `github.com/charmbracelet/bubbletea`,
  `github.com/charmbracelet/bubbles`, and `github.com/charmbracelet/lipgloss`
  import paths or v1 APIs.
- Preserve the repo's existing major version unless the user explicitly asks for
  an upgrade. Do not mix v1 and v2 examples in the same package.
- Before writing examples, inspect the package's current `View` signature,
  message types, key handling, and Bubbles component APIs. Bubble Tea v2 uses a
  rendered `tea.View` at the root, while many Bubbles and Huh component `View`
  methods still return strings for composition.
- In v2, prefer `tea.KeyPressMsg` and specific mouse messages such as
  `tea.MouseClickMsg`, `tea.MouseWheelMsg`, and `tea.MouseMotionMsg`. In v1,
  expect `tea.KeyMsg`, `tea.MouseMsg`, `View() string`, and command-based
  terminal-mode APIs.
- In v2, terminal features such as alt screen, mouse mode, window title, focus
  reporting, and cursor shape belong on `tea.View`. In v1, repos may still use
  program options or commands for those behaviors.
- In Bubbles v2, prefer constructor options and getter/setter methods where the
  component exposes them. Preserve v1 field-based code unless the task is an
  upgrade.
- In Lip Gloss v2, colors use `image/color.Color`; `AdaptiveColor` is replaced
  by `LightDark` or a compatibility package. Preserve v1 color APIs in v1 code.
- Charm v2 APIs still move across minor and release-candidate versions. When an
  example fails, APIs look mixed, or memory conflicts with the repo, verify the
  local module first with `go list -m`, `go doc`, and compile feedback; use
  `pkg.go.dev` as external confirmation, not as a reason to rewrite a stable
  local pattern.

## Upstream Examples Routing

When the repo does not have a local pattern for a component, inspect upstream
examples before inventing one. Common examples to look for:

- `list` for filtering and selection
- `table` for tabular navigation
- `textinput` and `textarea` for focused input handling
- `viewport` and `paginator` for scrolling and paging
- `spinner`, `progress`, `timer`, and `stopwatch` for time-based components
- `help` and `key` for key binding display
- `tabs` and multi-view examples for routing and focus patterns

## Bubble Tea Shape

Bubble Tea follows an Elm-style model/update/view loop:

```go
type model struct {
	width  int
	height int
	err    error
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
	case tea.KeyPressMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		}
	}
	return m, nil
}

func (m model) View() tea.View {
	return tea.NewView(render(m))
}
```

Use this shape as a starting point, then adapt it to the repo's version. For
older Bubble Tea code, expect `View` and key message APIs to differ.

## Commands And Messages

- A command should do one side effect and return one typed message.
- Keep command inputs explicit and immutable. Prefer constructor functions such
  as `loadItemsCmd(client, filter)` over anonymous closures buried in `Update`.
- Return errors as message fields, not panics or log-only failures.
- Use batching when commands are independent and sequencing when order matters.
- Use context-aware command dependencies when cancellation is part of the app
  contract. For long-running work, define who cancels, who observes completion,
  and what message represents cancellation.
- Do not send messages from unmanaged goroutines unless lifetime, shutdown, and
  backpressure are explicit.

## State And Screen Design

Model fields should make the visible state easy to explain:

- current screen, mode, or route
- focus target and keyboard context
- terminal width and height
- loaded data, pending state, and last error
- selection, cursor, viewport, pagination, and form values
- child Bubbles components
- transient status messages and confirmations

Split a root model only when the split improves ownership. Good seams are
screen-specific models, pure domain services, command constructors, style
helpers, and render helpers. Avoid a package where every file mutates the same
wide model through hidden helper methods.

## Bubbles Component Pattern

For standard widgets, keep the component model as part of the parent model and
assign the updated value back:

```go
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		inputWidth := msg.Width - 4
		if inputWidth < 0 {
			inputWidth = 0
		}
		m.input.SetWidth(inputWidth)
	case tea.KeyPressMsg:
		if key.Matches(msg, m.keys.Quit) {
			return m, tea.Quit
		}
	}

	var cmd tea.Cmd
	m.input, cmd = m.input.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}
```

Apply the same ownership rule to lists, tables, viewports, text areas,
spinners, timers, and progress bars. If a component returns a command for
blinking, ticking, filtering, loading, or animation, return that command from
the parent.

For current v2 Bubbles code, prefer setters such as `SetWidth`, `SetHeight`,
`SetStyles`, and component methods such as a spinner model's `Tick` method when
that is the local API. For older code, preserve the existing API style unless
the task is a migration.

Examples of version-sensitive APIs to verify locally:

- viewport construction may use functional options such as `WithWidth` and
  `WithHeight` in v2
- viewport dimensions may be read and written through `Width`, `Height`,
  `SetWidth`, and `SetHeight` methods in v2
- spinner startup may be a model method such as `m.spinner.Tick()` in v2
- component `View` methods commonly return strings even when the root Bubble
  Tea model returns `tea.View`

## Key Bindings And Help

- Prefer `bubbles/key` bindings over repeated string switches once a screen has
  more than a few shortcuts.
- Keep global, screen-local, and component-local bindings separate.
- Use `key.Matches` in update logic and expose the same bindings through the
  help component so rendered help cannot drift from behavior.
- Disable or hide bindings that do not apply in the current mode instead of
  showing dead shortcuts.
- Avoid stealing text-editing keys from focused text inputs or text areas.

## Huh Forms

Use Huh in this skill when a typed form is being embedded into a Bubble Tea TUI
and the repo already accepts the dependency or asks for Charm forms. Prompt-only
Huh flows are ordinary Go CLI work unless they are being converted into a
maintained terminal screen.

- Standalone `form.Run()` is fine for a simple non-Bubble-Tea prompt, but it is
  blocking and should not be called from a Bubble Tea `Update`.
- Embedded forms should participate in the model loop: call `form.Init()` from
  `Init`, call `form.Update(msg)` from `Update`, assign the returned form back,
  and render `form.View()` from `View`.
- For select, multiselect, and other typed fields, follow the local Huh version:
  some examples use generic type parameters while current APIs may expose
  non-generic constructors with typed options or accessors.
- Pass value pointers into fields, handle user-abort errors deliberately, and
  use dynamic title/options hooks only when their dependencies are explicit.
- Let the form consume Enter, Tab, and validation keys while it has focus.

## Lip Gloss Layout

- Define semantic styles such as title, selected row, muted text, danger,
  status, border, and help. Use them from render helpers instead of constructing
  styles inline in every branch.
- Use Lip Gloss rendering, wrapping, maximum width/height, joining, and
  placement helpers for ANSI-aware layout. Avoid `len`, byte slicing, or manual
  escape-code padding for visual dimensions.
- Treat `tea.WindowSizeMsg` as layout input. Compute available widths after
  borders, margins, and padding, then pass those values to Bubbles components
  and render helpers.
- Keep narrow terminal behavior explicit: collapse side panes, hide secondary
  metadata, shorten help, wrap body text, or show a minimum-size message.
- Use adaptive or semantic colors where possible, and keep critical state
  understandable without color.

## Testing Patterns

- Test `Update` by constructing the model, sending messages, and asserting the
  resulting state and returned command presence.
- Test command constructors by injecting fake dependencies and executing the
  returned command directly.
- Test rendering with focused string assertions for labels, selected rows,
  errors, and empty states. Use golden snapshots only for stable screens.
- Include resize tests for screens that compute pane widths, viewport heights,
  table columns, or help truncation.
- For components with timers or animation, test state transitions and avoid
  wall-clock sleeps unless the repo already has a deterministic clock seam.
- For interactive smoke checks, run the repo's TUI command in a real terminal
  or pseudo-terminal when terminal mode, cursor, alt screen, or key handling is
  part of the change.
