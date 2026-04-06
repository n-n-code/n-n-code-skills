---
name: coding-guidance-qt
description: Qt implementation and review skill. Use when writing, modifying, refactoring, or reviewing Qt C++ QWidget desktop code, especially Widgets, `.ui` forms, Designer-generated UI, models, `QAbstractItemModel`, signals and slots, `eventFilter`, `QThread`, CMake-based Qt5/Qt6 builds, layout-heavy UI, and QObject lifetime or thread-affinity problems. Portable across Qt-based C++ application repos.
---

# Qt Coding Guidance

This skill adds portable Qt implementation, refactoring, and review guidance
for Qt C++ code with a QWidget desktop focus. Widget, dialog, model/view,
Designer, and desktop-UX guidance here is specific to Widgets work; broader
QObject, threading, and build guidance also applies to non-UI Qt C++ code.

## Adjacent Skills

This skill provides portable Qt engineering principles. Compose with:

- **Workflow:** **thinking** (planning), **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **ui-guidance** (ordinary graphical UI work),
  **ui-design-guidance** (stronger design and UX work),
  **project-core-dev** (repo-specific build/test commands),
  **project-platform-diagnose** (environment-sensitive diagnosis)

Use this as the default principle skill for Qt code. Reach for
**coding-guidance-cpp** only when the task is mostly non-Qt C++ or needs deeper
general C++ design judgment than Qt-specific guidance.

## Quick Routing

Open bundled references only when the task actually needs them:

- [references/qt-build-compatibility.md](references/qt-build-compatibility.md)
  for CMake, generated-code, or Qt5/Qt6 compatibility work
- [references/qt-debugging-checklist.md](references/qt-debugging-checklist.md)
  for diagnosis-heavy tasks
- [references/qt-designer-ui-files.md](references/qt-designer-ui-files.md)
  for `.ui` files, Qt Widgets Designer, `uic`, or generated `ui_*.h` code
- [references/qt-layouts-and-desktop-ux.md](references/qt-layouts-and-desktop-ux.md)
  for layout, dialog, panel, and desktop-UX work
- [references/qt-model-view-checklist.md](references/qt-model-view-checklist.md)
  for `QAbstractItemModel`, roles, resets, selections, and model/view contract work

Stay in the main skill when the task is broad Qt implementation or review and
no single failure mode dominates yet.

## When Not to Lean on This Skill

- non-Qt work
- pure backend or library code written in C++ that does not use Qt types,
  eventing, object lifetime, or Qt build tooling
- Qt Quick or QML-first work
- design-only work where no Qt API, object model, build, or code judgment is
  needed

## Implementation Workflow

1. Read the touched widgets, models, controllers, dialogs, `.ui` forms, tests,
   and build files before editing.
2. Infer intended behavior from current signals and slots, ownership, thread
   affinity, layouts, and tests when the request is partially specified. Ask
   only when multiple plausible Qt designs would change semantics.
3. Choose the narrowest change that keeps QObject ownership, event ordering,
   layout behavior, model contracts, and UI-thread rules explicit.
4. Implement with one clear application bootstrap, small widget responsibilities,
   modern typed `connect` usage, minimal GUI-thread work, and narrow seams
   between widgets and domain logic.
5. Add or update deterministic tests close to the changed behavior. Default:
   Qt Test for widget, signal-slot, and model behavior; GoogleTest for pure
   non-Qt domain logic. Do not mix both in the same seam without a reason. If
   the repo already uses Qt Test, use `QSignalSpy`-style assertions for signal
   contracts.
6. Run the narrowest relevant formatter, build, test, and affected-platform
   smoke path the repo supports. If the change touches Qt5/Qt6 compatibility,
   validate each supported build variant.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current ownership, signal flow, event-loop assumptions, thread
   affinity, layout behavior, and model or binding contracts.
2. Break the refactor into small slices that preserve visible behavior.
3. Remove long widget constructors, tangled signal chains, view-model leakage,
   duplicated object wiring, and layout hacks one step at a time.
4. Keep tests or smoke paths passing after each slice; add characterization
   coverage first when behavior is unclear.
5. Stop when the code is simpler, safer around lifetime and threading, and
   easier to reason about.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize ownership and deletion bugs, cross-thread QObject misuse,
   connection lifetime mistakes, GUI-thread blocking, model/view contract
   violations, layout breakage, Qt5/Qt6 build regressions, resource-path and
   platform assumptions, and missing tests.
4. State findings with concrete evidence and the likely consequence.
5. For Qt-specific claims, name the proof: sender/receiver types and lifetimes
   for signal issues, thread affinity for cross-thread issues, begin/end and
   reset boundaries for model issues, and the visible interaction path for
   layout or `.ui` regressions.

## Qt Rules

### First tier - causes bugs

- These rules apply to Qt C++ broadly; Widget-specific rules appear in later
  sections.
- Treat `QObject` ownership, parent-child lifetime, and thread affinity as core
  contracts, not cleanup details
- Every Widgets application gets exactly one `QApplication`; create it before
  any widget, `QPixmap`, `QIcon`, or other GUI object
- Do not copy `QObject` subclasses; keep lifetime and ownership explicit
- Use `deleteLater()` rather than immediate deletion when an object may still be
  participating in the event loop
- Do not touch GUI objects from non-GUI threads
- Bind connection lifetime to a context object when possible so queued work does
  not outlive the receiver
- Prefer the typed `connect` syntax over string-based `SIGNAL` and `SLOT`
  macros unless the repo is constrained by old APIs
- Do not block the GUI thread with filesystem, network, database, or heavy CPU
  work
- When model data changes, emit the correct notifications and bracket
  structural changes with the correct begin/end calls
- Do not hand-place widgets with `setGeometry()` when a real layout should own
  sizing and positioning

### Second tier - prevents mistakes

- Keep widgets, models, delegates, dialogs, and business logic separated
  enough to test behavior without full UI setup
- Prefer explicit ownership and small helper objects over hidden globals or
  wide controller classes
- Keep slot bodies short; move non-trivial work into named helpers, presenters,
  or model logic
- Prefer Qt containers, strings, and utilities where the repo already uses
  them; do not introduce needless conversions at every boundary
- Follow the repo's Qt version and idioms before introducing newer Qt APIs
- Keep compiler, clazy, and Qt-specific warnings at zero in repo-owned code

### Architecture and object lifetime

- This section mixes general Qt lifetime guidance with QWidget screen-structure
  defaults.
- For Widgets apps, keep application bootstrap, main-window construction, and
  signal wiring easy to find
- In `QMainWindow` code, separate central-widget setup, action/menu setup, and
  signal wiring instead of burying everything in one constructor
- Use this default boundary unless the repo already chose differently:
  plain C++ domain logic owns rules and state transitions; Qt-facing models or
  adapters translate domain state for the UI; widgets own presentation, local
  interaction, and signal wiring
- For non-trivial screens, a presenter, controller, or adapter seam is often
  simpler than stuffing decisions into slots
- Parent-child ownership is convenient, but only when the parent truly owns the
  child for the same lifetime
- Use raw pointers for non-owning QObject references only when lifetime is
  obvious; use `QPointer` or a clearer ownership boundary when deletion can race
  with callbacks or queued work
- Avoid parented stack objects and mixed manual-plus-parent ownership
- Make who creates, owns, and tears down long-lived objects obvious near the
  construction site
- Be careful with lambdas connected to signals; capture only what can outlive
  the connection or tie the connection to a context object

### Signals, slots, and events

- These rules apply to Qt C++ broadly, not only Widgets screens.
- Treat signals as contracts; name them for state changes or completed actions,
  not vague implementation detail
- Prefer one clear signal over several partially overlapping ones when callers
  need a stable contract
- Avoid long signal chains that make control flow impossible to follow
- Be explicit about connection type when thread hops or reentrancy matter
- Guard against recursive updates and signal storms when setters feed models,
  bindings, or other observers
- If a signal appears connected but never fires, verify sender lifetime,
  signature compatibility, and that moc ran after the last `Q_OBJECT` change
- Use event filters sparingly; prefer normal event handlers when ownership and
  routing are local

### Models, views, and UI boundaries

- This section is mostly QWidget model/view guidance; use the reference for
  contract-heavy model work.
- Preserve the formal contract of Qt item models; invalid indexes, role names,
  and reset behavior are compatibility boundaries
- Keep view state, model state, and domain state separated enough that each can
  be tested and debugged directly
- Prefer explicit model roles and property names over stringly ad hoc data
  blobs
- Avoid doing heavy logic in delegates, bindings, or paint paths
- When a view needs derived presentation state, prefer a model or adapter seam
  over burying logic in widget callbacks
- In mixed QML/Widgets code, treat binding loops and context-property sprawl as
  design smells; this skill still defaults to the QWidget side
- Detailed model/view rules and review checks live in
  [references/qt-model-view-checklist.md](references/qt-model-view-checklist.md)

### Layouts and desktop UX

- This section is Widgets-specific.
- Layouts own geometry; use real layout types and desktop-native composition
  instead of manual sizing or geometry hacks
- Use `QFormLayout`, `QSplitter`, `QDockWidget`, `QGroupBox`, and
  `QDialogButtonBox` deliberately where their semantics match the screen
- Prefer standard buttons, shortcuts, dialogs, icons, and paths when Qt
  provides them, instead of hard-coding one platform's desktop conventions
- Be deliberate with `QSizePolicy`, stretch factors, margins, spacing,
  accessibility names, and keyboard flow
- Detailed layout and desktop-UX patterns live in
  [references/qt-layouts-and-desktop-ux.md](references/qt-layouts-and-desktop-ux.md)

### Threading, async, and responsiveness

- These rules apply to Qt C++ broadly, not only Widgets screens.
- Move blocking or long-running work off the GUI thread and define how results
  are marshaled back
- Use queued delivery deliberately when crossing thread boundaries; do not
  assume the default connection behavior is always correct
- Do not create children for a parent that lives in another thread
- Do not move an object to another thread unless its ownership, children, and
  event handling model all remain valid there
- Prefer explicit task ownership, cancellation, and teardown rules for timers,
  workers, and asynchronous replies
- Treat shutdown, application quit, and window close paths as lifetime hazards
  for queued callbacks and pending replies

### Build and version compatibility

- These rules apply to Qt C++ broadly; `.ui` guidance is Widgets-specific.
- Respect moc, uic, qrc, and build-system boundaries; file moves or class shape
  changes that affect generated code are not trivial refactors
- Do not edit generated `ui_*.h` files; change the `.ui` form, the wrapper
  widget, or the build inputs that generate them
- When a repo uses Qt Widgets Designer, treat `.ui` XML, form settings, custom
  widget declarations, and generated includes as part of the source contract
- If the repo supports both Qt5 and Qt6, use version-driven CMake patterns
  rather than hard-coded `Qt5::` or `Qt6::` targets
- In Qt6-first CMake repos that are not already standardized on a stable local
  pattern, prefer Qt's own helper commands such as
  `qt_standard_project_setup()` and `qt_add_executable()` over ad hoc target
  setup
- Treat Qt version compatibility as a public build contract; test each claimed
  variant instead of assuming dynamic `find_package` is enough
- Prefer stable resource lookup and path handling over current-working-directory
  assumptions
- Mark user-visible strings for translation through the repo's chosen path,
  `tr()` by default; do not introduce raw UI text that bypasses extraction
- Keep translation keys, object names, and user-visible strings deliberate
  rather than incidental
- Do not introduce obsolete Qt classes or deprecated members in new code when a
  maintained alternative exists; if a touched API is obsolete, treat migration
  pressure as part of the design review
- If a subsystem is mostly plain C++, keep Qt-specific concerns at the boundary
  instead of spreading Qt types everywhere without benefit
- Detailed build and compatibility patterns live in
  [references/qt-build-compatibility.md](references/qt-build-compatibility.md)

### Testing and debugging

- Test visible behavior, model transitions, emitted signals, and lifecycle
  edges, not just private helper functions
- Prefer deterministic UI tests and offscreen smoke paths over fragile timing-
  dependent visual assertions
- Treat build verification as part of test completion; generated or updated
  tests that do not compile are incomplete
- Use `qDebug()` and `qWarning()` deliberately for widget size, object class,
  state transitions, and connection-path diagnostics
- For memory or lifecycle bugs in C++, prefer AddressSanitizer and Qt-aware
  lifetime inspection over guessing
- Detailed failure categorization and diagnosis steps live in
  [references/qt-debugging-checklist.md](references/qt-debugging-checklist.md)

## Review Hotspots

- missing `Q_OBJECT`, stale moc output, or signal/slot signature mismatch
- wrong QObject ownership or `deleteLater()` timing
- cross-thread object parenting or GUI-thread violations
- incorrect model notifications, reset behavior, or invalid index handling
- edits to generated `ui_*.h` instead of the underlying `.ui` or wrapper code
- new user-visible strings that bypass translation or break existing i18n paths
- newly introduced obsolete Qt APIs or deprecated members
- hidden layout regressions from `QSizePolicy`, stretch, spacing, or minimum
  size changes
- Qt5/Qt6 target-family drift in CMake

## Review Evidence

- For signal or slot bugs, name the sender, receiver, connection style, and the
  lifetime or signature fact that breaks the path
- For thread-affinity bugs, name which object lives on which thread and where
  the illegal GUI or parenting access occurs
- For model/view bugs, name which contract breaks: wrong `data()` role,
  missing `begin*/end*`, invalid index handling, reset misuse, or stale
  selection/persistent-index assumptions
- For layout or `.ui` bugs, name the affected screen path and the geometry or
  form-setting change that causes the regression
- For build or generated-code bugs, name the specific moc/uic/qrc or CMake
  input that is stale, missing, or version-skewed

## Decision Heuristics

Use these when the right choice is not obvious:

- **Lifetime pressure:** if it is not obvious who owns a QObject or when it can
  die, redesign the boundary before adding more behavior.
- **Thread-affinity pressure:** if a callback, timer, or reply may arrive on a
  different thread, make that hop explicit and local.
- **Model-contract pressure:** if a change touches model indexes, role names,
  or reset behavior, treat it as a compatibility boundary rather than a local
  cleanup.
- **Layout pressure:** if you are about to use manual geometry, spacer hacks, or
  magic sizes, stop and check whether the right layout type, size policy, or
  stretch factor would solve it cleanly.
- **Build-compatibility pressure:** if a repo claims both Qt5 and Qt6 support,
  do not hard-code one target family or test only one build.
- **Architecture pressure:** if widget code starts owning business rules,
  persistence, and orchestration together, introduce a presenter/controller seam
  before adding more slots.
- **UI responsiveness:** if the feature can stall input, painting, or startup,
  rethink the design before polishing the code.
- **Repo conventions:** if the repo has established patterns for ownership,
  signals and slots, widgets vs. QML, testing, or Qt version support, follow
  them unless they create a correctness problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or lifecycle safety,
  prefer correctness. When it conflicts with style alone, prefer narrowness
  unless the task is explicitly a cleanup.
- **Refactor boundary:** outside explicit refactor work, fix at most one small
  adjacent issue while you are in the file.
- **Abstraction threshold:** three similar widget handlers, signal-wiring paths,
  model-shaping steps, or dialog flows is a pattern; before extracting, check
  whether a small helper, adapter, presenter, or model object is the simpler
  move.
- **Qt vs. plain C++:** if logic does not need the event loop, QObject
  identity, or Qt containers, keep it as plain testable C++ instead of forcing
  Qt into the core domain.

## Validation

A change is done when:

- the code builds without new compiler, moc, or Qt-specific warnings
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- changed signal, layout, model, or thread-hop behavior has a deterministic
  validation path
- UI-facing changes have at least a narrow smoke path on the affected platform
- Qt5/Qt6 compatibility changes were validated on each claimed build variant
- resource paths, generated-code inputs, and translation-sensitive changes were
  verified when touched
- review findings at `Critical` and `Important` severity are addressed

## Examples

- `Review this Qt dialog and layout refactor for ownership, size-policy, and accessibility regressions`
- `Refactor this Qt widget controller so business logic moves out of slots and the UI stays responsive`
- `Fix this Qt CMake setup so the repo can build cleanly against both Qt5 and Qt6`
