# Qt Designer UI Files

Open this reference when the task touches `.ui` forms, Qt Widgets Designer,
`uic`, custom Designer widgets, or generated `ui_*.h` headers.

## Core rules

- Treat `.ui` files as source and generated `ui_*.h` files as build outputs
- Do not hand-edit generated UI headers; make the change in the form, the
  wrapper widget, or the code that consumes the generated UI class
- When a form change affects margins, spacing, or custom widget includes, treat
  the Designer form settings as behavior-affecting inputs, not editor metadata

## Review hotspots

- generated `ui_*.h` checked in with manual edits instead of regenerating
- `.ui` changes that silently alter layout defaults, spacing, or margins
- custom widgets declared in Designer without the includes or build wiring they
  require
- wrapper code that bypasses `setupUi()` assumptions and fights the generated
  layout or object naming

## Validation

- rebuild after every `.ui` or Designer custom-widget change so `uic` reruns
- verify the changed screen through the affected interaction path, not only by
  compiling
- if the repo uses Designer heavily, keep layout ownership in the form unless a
  code-side override is clearly intentional
