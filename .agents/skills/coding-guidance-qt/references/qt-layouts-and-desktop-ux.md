# Qt Layouts And Desktop UX

Open this reference when the task is mainly widget composition, dialog design,
panel layout, or desktop ergonomics.

## Layout defaults

- layouts own geometry; do not hand-place widgets unless there is a real custom
  rendering need
- prefer `QFormLayout` for forms, `QGridLayout` for true grids, and `QSplitter`
  for user-resizable panel balance
- be deliberate with margins, spacing, stretch factors, and `QSizePolicy`

## Useful patterns

### Forms

- use `QFormLayout` for label-field alignment
- use `QDialogButtonBox` for accept/reject flows

### Panels

- use `QDockWidget` only for real dockable panels
- use `QGroupBox` when visual grouping materially improves scanability
- persist `QSplitter` state for long-lived multi-panel screens

### Accessibility and keyboard flow

- set accessible names for important controls
- keep tab order sensible
- make important actions keyboard reachable

### Native desktop conventions

- prefer `QDialogButtonBox` standard roles and platform-native button ordering
  over custom accept/cancel layouts
- prefer Qt standard shortcuts, icons, and dialogs before inventing custom
  desktop conventions
- use Qt-provided standard paths and file dialogs instead of hard-coded
  platform-specific locations

## Layout debugging

- if a widget is zero-size, check minimum size, size hint, attached layout, and
  size policy
- if the layout ignores size changes, inspect stretch factors and whether the
  widget is `Fixed` when it should expand
- if the screen looks cramped, inspect margins and spacing before rewriting the
  hierarchy
