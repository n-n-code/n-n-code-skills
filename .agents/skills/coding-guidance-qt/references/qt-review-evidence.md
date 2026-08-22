# Qt Review Evidence

Read this reference for Qt-specific code review. Use the matching specialized
reference as well when model/view, layout, Designer, build, or diagnosis depth
is material.

## Hotspots

- missing `Q_OBJECT`, stale moc output, or signal/slot signature mismatch
- wrong QObject ownership, unsafe direct deletion, or deferred deletion that
  the owning event loop will not process
- cross-thread object parenting or GUI-thread violations
- incorrect model notifications, reset behavior, or invalid index handling
- edits to generated `ui_*.h` instead of the underlying `.ui` or wrapper code
- user-visible strings that bypass the repo's translation path
- obsolete Qt APIs or deprecated members introduced in new code
- layout regressions from size policy, stretch, spacing, or minimum-size changes
- Qt5/Qt6 target-family drift in CMake

## Evidence required

- For signal or slot bugs, name the sender, receiver, connection style, and the
  lifetime or signature fact that breaks the path.
- For thread-affinity bugs, name which object lives on which thread and where
  the illegal GUI or parenting access occurs.
- For model/view bugs, name the broken contract: role data, begin/end pairing,
  index validity, reset behavior, or selection and persistent-index handling.
- For layout or `.ui` bugs, name the affected screen path and the geometry or
  form setting that causes the regression.
- For build or generated-code bugs, name the moc, uic, qrc, or CMake input that
  is stale, missing, or version-skewed.

Report findings without editing code unless remediation is explicitly in
scope. An open finding does not make the review incomplete.
